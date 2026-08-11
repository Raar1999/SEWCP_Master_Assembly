"""Command line: aief-cad.

    python -m aief_cad status <package>     bridge health and deployment
    python -m aief_cad ping                 handshake with the running add-in
    python -m aief_cad plan <package>       ingest -> agents -> solution -> ops
    python -m aief_cad run <package>        the whole path, against real Fusion
    python -m aief_cad replay <run.json>    re-verify a recorded run

`plan` reaches no further than the bridge and is the safe way to inspect what a
package would dispatch. `run` requires the add-in to be live; it refuses to
queue commands nobody is reading.

`replay` re-runs verification against the observations already recorded. It
proves a verdict is reproducible from evidence rather than from the run that
produced it.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from aief_cad import BRIDGE_ROOT, CadError
from aief_cad.agents import select_agents
from aief_cad.bridge.client import BridgeNotRunning, FileQueueBridge
from aief_cad.bridge.protocol import Command
from aief_cad.digest import short
from aief_cad.observe import merge_observations, parse as parse_observed
from aief_cad.ops import compile_solution
from aief_cad.orchestrator import Orchestrator
from aief_cad.requirements import load_package
from aief_cad.solution import resolve
from aief_cad.verify import run_all


def _bar(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


def cmd_status(args) -> int:
    bridge = FileQueueBridge()
    live = bridge.available()
    print(f"bridge root     {BRIDGE_ROOT}")
    print(f"queue           {len(list(bridge.queue_dir.glob('*.cmd.json')))} pending command file(s)")
    print(f"observations    {len(list(bridge.obs_dir.glob('*.obs.json')))} recorded")
    print(f"add-in          {'LIVE' if live else 'NOT RUNNING'}")
    if not live:
        print("                start Fusion 360, then Utilities > Scripts and Add-Ins")
        print("                > Add-Ins > AIEF_CAD_Bridge > Run")
    if args.package:
        pkg = load_package(args.package)
        print(f"package         {pkg.package_id}  {short(pkg.digest)}")
        print(f"component       {pkg.component}")
        print(f"domains         {', '.join(pkg.domains())}")
    return 0 if live else 1


def cmd_ping(args) -> int:
    bridge = FileQueueBridge()
    cmd = Command(
        command_id=f"PING-{int(time.time())}",
        op="ping",
        args={},
        issued_by="mechanical.cad-engineer",
        session=args.session,
        solution_id="-",
        model_target={},
        idempotency_key="ping",
        timeout_s=args.timeout,
    )
    try:
        obs = bridge.send(cmd, reuse=False)
    except BridgeNotRunning as exc:
        print(f"NOT RUNNING: {exc}")
        return 1
    print(json.dumps(obs.raw, indent=2, sort_keys=True))
    return 0 if obs.ok else 1


def _plan(package_path: str):
    pkg = load_package(package_path)
    agents = select_agents(pkg)
    contributions = [a.contribute(pkg) for a in agents]
    solution = resolve(pkg, contributions, solution_id="PLAN.S1")
    return pkg, agents, contributions, solution, compile_solution(solution)


def cmd_plan(args) -> int:
    pkg, agents, contributions, solution, ops = _plan(args.package)

    _bar("REQUIREMENTS")
    print(f"package     {pkg.package_id}   digest {short(pkg.digest)}")
    print(f"component   {pkg.component}")
    print(f"authority   {'; '.join(pkg.authority)}")
    print(f"requirements {len(pkg.requirements)}   parameters {len(pkg.parameters)}"
          f"   acceptance {len(pkg.acceptance)}")

    _bar("DOMAINS AND AGENTS")
    print(f"domains     {', '.join(pkg.domains())}")
    for a, c in zip(agents, contributions):
        print(f"  {a.name:38s} {a.domain:18s} "
              f"{len(c.features)} feature(s), {len(c.constraints)} constraint(s)")

    _bar("DESIGN SOLUTION")
    print(f"solution    {solution.solution_id}   digest {short(solution.digest)}")
    for f in solution.ordered_features():
        print(f"  {f.id:34s} {f.kind:20s} <- {solution.provenance.get('feature:' + f.id, '')}")

    _bar("COMPILED OPERATIONS")
    for op in ops:
        detail = {k: v for k, v in op.args.items() if k != "parameters"}
        if "parameters" in op.args:
            detail["parameters"] = f"<{len(op.args['parameters'])} parameters>"
        print(f"  {op.op_id}  {op.op:22s} {json.dumps(detail, sort_keys=True)[:96]}")

    _bar("ACCEPTANCE")
    for a in solution.acceptance:
        tol = "" if a.tolerance is None else f" +/- {a.tolerance:g}"
        print(f"  {a.id:22s} [{a.check:10s}] {a.subject} == {a.expect!r}{tol}")
    print()
    print(f"{len(ops)} operation(s) would be dispatched. Nothing was sent.")
    return 0


def cmd_revert(args) -> int:
    """Recover the package's document to its last saved version."""
    pkg = load_package(args.package)
    name = str(pkg.scope.get("document_name") or pkg.component)
    bridge = FileQueueBridge()
    cmd = Command(
        command_id=f"REVERT-{int(time.time())}",
        op="revert_document",
        args={"name": name},
        issued_by="mechanical.cad-engineer",
        session=args.session,
        solution_id="-",
        model_target={"document": name},
        idempotency_key=f"revert-{int(time.time())}",
    )
    obs = bridge.send(cmd, reuse=False)
    print(json.dumps(obs.raw, indent=2, sort_keys=True))
    return 0 if obs.ok else 1


def cmd_run(args) -> int:
    orch = Orchestrator(session=args.session, max_attempts=args.max_attempts,
                        save_on_pass=args.save_on_pass)
    record = orch.run(args.package, run_id=args.run_id)

    _bar(f"RUN {record.run_id}")
    print(f"package     {record.package_id}  {short(record.package_digest)}")
    print(f"solution    {record.solution_id}  {short(record.solution_digest)}")
    print(f"agents      {', '.join(record.agents)}")
    for att in record.attempts:
        v = att["verdict"]
        print()
        print(f"attempt {att['attempt']}: dispatched {att['dispatched']}, "
              f"executed {att['executed']}, verdict {v['verdict']} "
              f"({v['checks'] - v['failed']}/{v['checks']} checks)")
        if att.get("execution_halt"):
            print(f"  HALT  {att['execution_halt']}")
        for r in v["reports"]:
            print(f"  {r['verifier']:12s} {'PASS' if r['passed'] else 'FAIL'}  "
                  f"{r['checks'] - r['failed']}/{r['checks']}")
            for f in r["findings"]:
                if not f["passed"]:
                    print(f"      FAIL {f['id']}: {f['subject']} "
                          f"expected {f['expected']!r}, observed {f['observed']!r}")
                    if f["detail"]:
                        print(f"           {f['detail']}")
        if att.get("repair"):
            for d in att["repair"]["diagnoses"]:
                print(f"  DIAGNOSIS {d['finding']} -> {d['responsible_agent']}")
                print(f"      cause      {d['likely_cause']}")
                print(f"      correction {d['proposed_correction']}")

    for e in record.escalations:
        print()
        print(f"ESCALATION  {e}")

    print()
    print(f"VERDICT     {record.verdict}")
    print(f"recorded    cad/runs/{record.run_id}/run.json")
    return 0 if record.verdict == "PASS" else 1


def cmd_replay(args) -> int:
    """Re-verify from recorded evidence, independent of the run that made it."""
    body = json.loads(Path(args.run).read_text(encoding="utf-8"))
    pkg, _agents, _c, solution, _ops = _plan(args.package)
    if solution.package_digest != body["package_digest"]:
        print("package digest differs from the recorded run; the requirement "
              "package has changed since. Replay compares nothing meaningful.")
        return 2
    last = body["attempts"][-1]
    model = parse_observed(last["observed_model"])
    verdict = run_all(solution, model, attempt=last["attempt"])
    print(f"recorded verdict  {last['verdict']['verdict']}")
    print(f"replayed verdict  {verdict.verdict}  "
          f"({verdict.check_count - len(verdict.failures)}/{verdict.check_count})")
    same = verdict.verdict == last["verdict"]["verdict"]
    print("REPRODUCIBLE" if same else "DIVERGENT - the verdict does not reproduce")
    return 0 if same else 1


def cmd_op(args) -> int:
    """Dispatch one named operation with literal JSON args - the admin and
    lifecycle path (list_documents, open/close, insert_occurrence, exports).
    Solution-compiled geometry still goes through `run`; this never does
    design work, which is why it takes no package."""
    bridge = FileQueueBridge()
    op_args = json.loads(args.args) if args.args else {}
    cmd = Command(
        command_id=f"ADM-{int(time.time())}-{args.op}",
        op=args.op,
        args=op_args,
        issued_by="mechanical.cad-engineer",
        session=args.session,
        solution_id="-",
        model_target={},
        idempotency_key=f"adm-{args.op}-{time.time()}",
        timeout_s=args.timeout,
    )
    try:
        obs = bridge.send(cmd, reuse=False)
    except BridgeNotRunning as exc:
        print(f"NOT RUNNING: {exc}")
        return 1
    print(json.dumps(obs.raw, indent=2, sort_keys=True))
    return 0 if obs.ok else 1


def cmd_assembly(args) -> int:
    """Build (or preview) an assembly package against live Fusion."""
    from aief_cad.assembly import AssemblyRunner, load_assembly_package

    package = load_assembly_package(args.package)
    print(f"assembly    {package.package_id}  {short(package.digest)}")
    print(f"document    {package.document}")
    print(f"occurrences {len(package.occurrences)} of "
          f"{len(package.designs())} designs")
    if args.dry_run:
        for o in package.occurrences:
            rx = f" rx {o.rotate_x_deg}" if o.rotate_x_deg else ""
            print(f"  {o.occurrence_id:12s} {o.design:26s} "
                  f"t {list(o.translate_mm)} rz {o.rotate_z_deg}{rx}")
        print("Nothing was sent.")
        return 0
    runner = AssemblyRunner(session=args.session)
    record = runner.run(package, save_on_pass=not args.no_save)
    verdict = record.get("verdict")
    print(f"verdict     {verdict}")
    for c in (record.get("verification") or {}).get("checks", []):
        mark = "PASS" if c["passed"] else "FAIL"
        if not c["passed"]:
            print(f"  {mark} {c['id']}: {c['statement']} - {c['detail']}")
    print(f"recorded    cad/runs/{record['run_id']}/run.json")
    return 0 if verdict == "PASS" else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="aief-cad", description=__doc__)
    ap.add_argument("--session", default="unrecorded-session")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("op"); p.add_argument("op"); p.add_argument("--args", default="")
    p.add_argument("--timeout", type=float, default=120.0)
    p.set_defaults(fn=cmd_op)
    p = sub.add_parser("assembly"); p.add_argument("package")
    p.add_argument("--no-save", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_assembly)
    p = sub.add_parser("status"); p.add_argument("package", nargs="?"); p.set_defaults(fn=cmd_status)
    p = sub.add_parser("ping"); p.add_argument("--timeout", type=float, default=20.0)
    p.set_defaults(fn=cmd_ping)
    p = sub.add_parser("plan"); p.add_argument("package"); p.set_defaults(fn=cmd_plan)
    p = sub.add_parser("run"); p.add_argument("package")
    p.add_argument("--run-id"); p.add_argument("--max-attempts", type=int, default=3)
    p.add_argument("--save-on-pass", action="store_true")
    p.set_defaults(fn=cmd_run)
    p = sub.add_parser("revert"); p.add_argument("package")
    p.set_defaults(fn=cmd_revert)
    p = sub.add_parser("replay"); p.add_argument("run"); p.add_argument("package")
    p.set_defaults(fn=cmd_replay)

    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except CadError as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
