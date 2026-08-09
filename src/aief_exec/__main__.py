"""Command line: aief-exec.

Actor provenance: software.software-engineer - S-2026-08-09-01.

    python -m aief_exec status              the plan: states, blockers, dispatch groups
    python -m aief_exec scope T-002         resolved read scope with exact cost
    python -m aief_exec classify T-002 T-003   pair classification with reasons
    python -m aief_exec brief T-002         the minimum context for one task
    python -m aief_exec check                X-01 to X-10
    python -m aief_exec audit [T-nnn]        changes outside a declared write scope
    python -m aief_exec measure [T-nnn]      reproduce the route comparison
"""

from __future__ import annotations

import sys
from pathlib import Path

from aief_exec import checks, graph, records, scope


def _repo() -> Path:
    return Path(__file__).resolve().parents[2]


def cmd_status(repo: Path, _: list[str]) -> int:
    plan = graph.build_plan(repo)
    tasks = records.load_tasks(repo)
    print("TASK STATES")
    for tid in sorted(plan.states):
        state = plan.states[tid]
        obj = str(tasks[tid].data.get("objective") or "")
        print(f"  {tid}  {state:<18} {obj[:64]}")
        for reason in plan.blocked.get(tid, []):
            print(f"        - {reason}")
    if plan.cycles:
        print("\nCYCLES")
        for c in plan.cycles:
            print("  " + " -> ".join(c))
    print("\nRESULT CURRENCY")
    for rid, curr in sorted(plan.currency.items()):
        print(f"  {rid}  {curr.status}")
        for d in curr.drifted:
            print(f"        - {d}")
    print("\nDISPATCH GROUPS  (members are pairwise PARALLEL - safe to run together)")
    for i, group in enumerate(plan.parallel_sets(), 1):
        print(f"  group {i}: {', '.join(group)}")
    return 0


def cmd_scope(repo: Path, args: list[str]) -> int:
    tasks = records.load_tasks(repo)
    tid = args[0]
    task = tasks[tid]
    total_narrow = scope.ZERO
    total_whole = scope.ZERO
    for kind in ("mandatory", "optional"):
        rs = scope.resolve_scope(repo, task, kind)
        if not rs.entries and not rs.errors:
            continue
        print(f"{kind.upper()} READ SCOPE")
        for ex in rs.entries:
            shown = f"{ex.path}" + (f"  #{ex.anchor}" if ex.anchor else "")
            print(f"  {str(ex.cost):<28} {shown}")
        for e in rs.errors:
            print(f"  UNRESOLVED  {e}")
        print(f"  {'-' * 28}")
        print(f"  {str(rs.total):<28} resolved")
        print(f"  {str(rs.whole_file_total):<28} same files unanchored")
        if kind == "mandatory":
            total_narrow = rs.total
            total_whole = rs.whole_file_total
        print()
    for entry in task.read_entries("dependency"):
        print(f"DEPENDENCY  {entry.get('result')}  (read the conclusion, not its inputs)")
    results = records.load_results(repo)

    # The publication channel, derived and displayed - never granted. Whether
    # `produces` carries an implicit write grant is open decision A4; X-04 keeps
    # testing the declared scope alone and this block settles nothing.
    print("\nWRITE SCOPE declared (this is what X-04 tests)")
    for pattern in task.write_scope:
        print(f"            {pattern}")
    derived = [p for p in task.effective_write_scope if p not in task.write_scope]
    print("DERIVED     result paths implied by `produces` - "
          "DERIVED, NOT GRANTED (open decision A4)")
    for rid, rel in zip(task.produces, task.result_paths):
        covered = any(scope.glob_to_regex(p).match(rel) for p in task.write_scope)
        print(f"            {rel}   [{rid}: "
              f"{'covered by declared write scope' if covered else 'NOT COVERED'}]")
    if not task.produces:
        print("            (this task declares no produces)")
    print(f"EFFECTIVE   declared + derived = {len(task.effective_write_scope)} "
          f"pattern(s); the {len(derived)} derived one(s) are displayed, not granted")

    surface = graph.observed_surface(repo, task, results)
    print("OBSERVED    derived observation surface - write scope + resolved "
          "deliverables + consumed-result deliverables + declared `observes`")
    for pattern in surface:
        print(f"            {pattern}")
    for note in graph.undeclared_observation(task):
        print(f"            note  {note}")

    budget = task.data.get("context_budget") or {}
    print(f"\nBUDGET      declared TF-1 {budget.get('tf1')} / TF-2 {budget.get('tf2')}")
    print(f"MANDATORY   resolved {total_narrow}")
    # VER-009 FIND-Q9-35 and its own correction: the resolved read scope is not
    # the charge, and the charge is not one number. Three quantities, named.
    cc = scope.charged_context(repo, task, results)
    print(f"ACQUISITION {cc.acquisition}   "
          f"GATED - this is what X-08 compares against the cap")
    # VER-009 FIND-Q9-36: the gate is exact at dispatch time and is not an
    # invariant of the task's execution. How much of it the task itself moves is
    # printed beside it rather than left to be discovered.
    print(f"  stable    {str(cc.acquisition_stable):<28} "
          f"outside this task's own write scope")
    print(f"  self-ref  {str(cc.acquisition_self_referential):<28} "
          f"INSIDE it - this much of the gate moves as the task works")
    for name in scope.ACQUISITION_COMPONENTS:
        c = cc.component_total(name)
        if c.tf1 or c.tf2:
            print(f"            {str(c):<28} {name}")
    print(f"REVISION    {cc.revision}   reported, not gated")
    for name in scope.REVISION_COMPONENTS:
        c = cc.component_total(name)
        if c.tf1 or c.tf2:
            print(f"            {str(c):<28} {name}")
    # FIND-Q9-36b: the moving paths get their own block and are named with the
    # component that holds them. They used to decorate the REVISION line, which
    # was false for every task whose movement is in `acquisition` - for T-002 it
    # printed "revision ... NON-MONOTONIC in 2 path(s)" beside a revision of
    # zero, about two paths in `mandatory`.
    moving = cc.moving_by_component()
    print(f"NON-MONOTON {len(moving)} charged path(s) inside this task's own write "
          f"scope - the figure moves as it works" if moving
          else "NON-MONOTON none - no charged path lies inside this task's own "
               "write scope")
    for kind, rel in moving:
        print(f"            {kind:<11} {rel}")
    print(f"TELEMETRY   {cc.telemetry}   {cc.telemetry_note}")
    # FIND-Q9-46 in the CLI: this line named X-08 and asserted the breach "fails
    # separately", which after FIND-Q9-45 is the wrong check and was never a
    # claim about this tree. It names the check that owns the comparison and
    # asserts no verdict; the verdict is X-10's row.
    print(f"TOTAL       {cc.total_measurable}   total_measurable = acquisition + "
          f"revision. X-10 compares this against the same declared cap, as a "
          f"NON-MONOTONIC bound and not the dispatch gate (FIND-Q9-37, -45); "
          f"telemetry cannot be added to it")
    for note in cc.notices:
        print(f"            note  {note}")
    # VER-009 FIND-Q9-8: the saving was reported under TF-1 only, while AC-3
    # requires both families. Both are printed.
    if total_narrow.measured and total_whole.measured:
        for fam, narrow, whole in (
            ("TF-1", total_narrow.tf1, total_whole.tf1),
            ("TF-2", total_narrow.tf2, total_whole.tf2),
        ):
            if not whole:
                continue
            saved = whole - narrow
            print(
                f"ANCHORING   {fam} saves {saved} of {whole} "
                f"({100.0 * saved / whole:.0f}%), factor {whole / narrow:.1f}x"
            )
    return 0


#: What each verdict means, named where the verdict is printed. A verdict that
#: does not say what class of hazard it found - or, for PARALLEL, what it looked
#: for and did not find - is an assertion the reader cannot check.
VERDICT_CLASS = {
    graph.PARALLEL: "no hazard found in any of the three classes compared below",
    graph.CONFLICT: "scope hazard - the class is named in each reason",
    graph.SERIAL: "serial/dependency - an edge orders these two",
    graph.BLOCKED: "blocked/precondition - not a scope hazard; a precondition is unmet",
}


def cmd_classify(repo: Path, args: list[str]) -> int:
    a, b = args[0], args[1]
    plan = graph.build_plan(repo)
    tasks = records.load_tasks(repo)
    results = records.load_results(repo)
    paths = scope.tree(repo)
    kind, why = plan.pairs[tuple(sorted((a, b)))]
    print(f"{a} x {b}  ->  {kind}")
    print(f"  hazard class : {VERDICT_CLASS.get(kind, 'unclassified')}")
    for reason in why:
        print(f"  - {reason}")
    if kind == graph.PARALLEL:
        # A bare PARALLEL is not an answer. Print the working: which surfaces
        # were compared, and that each intersection was empty.
        print("  WHY SAFE - every comparison the verdict rests on:")
        for line in graph.safety_explanation(
            repo, tasks[a], tasks[b], paths, results, plan.surfaces
        ):
            print(f"    {line}")
    print("  OBSERVED SURFACE (derived; write scope + resolved deliverables + "
          "consumed-result deliverables + declared `observes`)")
    for tid in (a, b):
        surface = plan.surfaces.get(tid) or []
        print(f"    {tid}: {', '.join(surface) or '(empty)'}")
    for tid in (a, b):
        for note in graph.undeclared_observation(tasks[tid]):
            print(f"  note   {note}")
    return 0


def cmd_brief(repo: Path, args: list[str]) -> int:
    """The minimum context for one task: the record, the resolved excerpts and the
    conclusions of consumed results. Nothing else."""
    tid = args[0]
    tasks = records.load_tasks(repo)
    results = records.load_results(repo)
    task = tasks[tid]
    plan = graph.build_plan(repo)

    print(f"=== TASK {tid} — {plan.states[tid]}")
    print(f"objective : {task.data.get('objective')}")
    print(f"role      : {task.data.get('role')}")
    print(f"verifier  : {(task.data.get('qa') or {}).get('verifier_role')}")
    print(f"write     : {', '.join(task.write_scope)}")
    print(f"forbidden : {', '.join(task.forbidden_reads) or '(none)'}")
    for reason in plan.blocked.get(tid, []):
        print(f"BLOCKED   : {reason}")
    cp = task.checkpoint
    if cp:
        print(f"\n=== CHECKPOINT  phase {cp.get('phase')}")
        for item in cp.get("completed") or []:
            print(f"  done    {item}")
        for item in cp.get("pending") or []:
            print(f"  pending {item}")
        print(f"  next    {cp.get('next_action')}")
        decision = cp.get("decision")
        if decision:
            print(f"  DECISION {decision.get('id')} [{decision.get('status')}]")

    total = scope.ZERO
    # VER-009 FIND-Q9-33: `whole=False` drops the unanchored comparison read that
    # nothing here prints, and the excerpt carries its own text, so each entry is
    # opened once instead of three times.
    rs = scope.resolve_scope(repo, task, "mandatory", whole=False)
    for ex in rs.entries:
        head = f"--- {ex.path}" + (f"  #{ex.anchor}" if ex.anchor else "") + f"   [{ex.cost}]"
        print(f"\n{head}")
        print(ex.text.rstrip())
        total = total + ex.cost
    for rid in task.consumes:
        if rid in results:
            concl = results[rid].conclusion
            c = scope.cost(concl)
            total = total + c
            print(f"\n--- {rid} conclusion   [{c}]")
            print(concl.rstrip())
    print(f"\n=== TOTAL BRIEF COST  {total}")
    return 0


def cmd_measure(repo: Path, args: list[str]) -> int:
    """Reproduce the route comparison for one task.

    VER-009 FIND-Q9-26: the headline figures were produced by a working script
    outside the repository, so 'recomputable' was a claim nobody could act on and
    an independent sweep landed elsewhere because the envelope was undefined.
    The envelope is defined here, in code, and printed with the numbers.
    """
    tid = args[0] if args else "T-002"
    task = records.load_tasks(repo)[tid]

    boot = [
        ".ai/BOOT.md", ".ai/FRAMEWORK.md", ".ai/project/STATE.md",
        ".ai/project/ledger/HEAD", ".ai/project/BINDING.md",
        ".ai/core/laws/INDEX.md", ".ai/core/PRECEDENCE.md",
        ".ai/project/OPEN_ITEMS.md",
    ]
    ext = {".md", ".json", ".py", ".yaml", ".yml", ".txt"}
    envelope = [
        p for p in scope.tree(repo)
        if p.split("/")[0] in (".ai", "framework", "src", "tests")
        and Path(p).suffix.lower() in ext
    ]

    def total(paths: list[str]) -> scope.Cost:
        out = scope.ZERO
        for p in paths:
            try:
                out = out + scope.cost((repo / p).read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                pass
        return out

    print(f"ENVELOPE DEFINITION  top-level .ai/ framework/ src/ tests/, suffixes "
          f"{sorted(ext)}, excluding {sorted(scope.SKIP_DIRS)}")
    print()
    sweep = total(envelope)
    rs = scope.resolve_scope(repo, task, "mandatory")
    declared = total(boot) + total([".ai/project/EXEC.md", task.path]) + rs.total
    rows = [
        ("unbounded sweep", len(envelope), sweep),
        ("declared scope via aief_exec", len(boot) + 2 + len(rs.entries), declared),
    ]
    print(f"{'route':<34}{'files':>7}{'TF-1':>10}{'TF-2':>10}")
    for name, n, c in rows:
        print(f"{name:<34}{n:>7}{_num(c.tf1):>10}{_num(c.tf2):>10}")
    print()
    print(f"reduction  {_ratio(sweep.tf1, declared.tf1)} TF-1 / "
          f"{_ratio(sweep.tf2, declared.tf2)} TF-2")
    print(f"anchoring  mandatory scope {rs.total} against "
          f"{rs.whole_file_total} unanchored")

    # VER-009 FIND-Q9-31: the sweep is a live measurement of a tree that contains
    # the audit trail describing it, so it is not a constant and must never be
    # pinned as one. Demonstrated by the auditor, not argued: the same command
    # over the same envelope printed 387,953 TF-1 before VER-009 was written and
    # 397,349 after - moved 9,396 by the act of filing the audit that measured
    # it. The moving component is printed here so the reader can see it move.
    trail = [
        p for p in envelope
        if p.startswith((".ai/project/results/", ".ai/project/verification/"))
    ]
    tc = total(trail)
    print()
    print(f"NOT A CONSTANT  the sweep above is measured at run time. "
          f"{len(trail)} of {len(envelope)} envelope files are the result and "
          f"verification registers, {_num(tc.tf1)} TF-1, and they grow every time "
          f"an audit or a result is filed - including by the session reading this.")
    stable = None if sweep.tf1 is None or tc.tf1 is None else sweep.tf1 - tc.tf1
    print(f"                envelope less that trail: {_num(stable)} TF-1. "
          f"Cite this command, never a number it printed once.")
    return 0


def _num(v: int | None) -> str:
    """VER-009 FIND-Q9-34: `scope.cost` is documented to return None per family
    when a tokenizer is unavailable, and this report formatted it with `:>10,`
    unconditionally - so the command printed a partial table and then died with
    `TypeError: unsupported format string passed to NoneType.__format__`. An
    unavailable measurement is reported, never crashed on and never estimated."""
    return "UNMEASURED" if v is None else f"{v:,}"


def _ratio(a: int | None, b: int | None) -> str:
    if a is None or b is None:
        return "UNMEASURED"
    if not b:
        return "undefined (zero denominator)"
    return f"{a / b:.1f}x"


def _changed(repo: Path) -> list[str]:
    """Working-tree changes, from git porcelain. Untracked directories expand."""
    import subprocess
    raw = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=repo, capture_output=True, text=True, check=True,
    ).stdout
    out: list[str] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip().strip('"')
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        out.append(path)
    return sorted(out)


def cmd_audit(repo: Path, args: list[str]) -> int:
    """Detect modifications outside every declared write scope."""
    tasks = records.load_tasks(repo)
    if args:
        tasks = {args[0]: tasks[args[0]]}
    changed = _changed(repo)
    owners = scope.attribute(repo, changed, tasks)
    unattributed = [p for p, who in owners.items() if not who]
    print(f"CHANGED PATHS  {len(changed)}")
    for path, who in sorted(owners.items()):
        mark = ", ".join(who) if who else "UNATTRIBUTED"
        print(f"  {mark:<28} {path}")
    print(f"\n{len(changed) - len(unattributed)} attributed, {len(unattributed)} not")
    return 1 if unattributed else 0


def cmd_check(repo: Path, _: list[str]) -> int:
    rows = checks.run_all(repo)
    worst = 0
    for row in rows:
        print(f"{row['id']}  {row['status']:<6} {row['name']}")
        for d in row["details"]:
            print(f"      FAIL   {d}")
        # VER-009 FIND-Q9-16: notices were computed and discarded, so a granted
        # reach into the protected set was exactly as silent as before the grant
        # existed. A notice the operator never sees is not a notice.
        for n in row.get("notices", []):
            print(f"      note   {n}")
        if row["status"] != "PASS":
            worst = 1
    passed = sum(1 for r in rows if r["status"] == "PASS")
    print(f"\n{passed} of {len(rows)} PASS")
    return worst


COMMANDS = {
    "status": cmd_status,
    "scope": cmd_scope,
    "classify": cmd_classify,
    "brief": cmd_brief,
    "check": cmd_check,
    "audit": cmd_audit,
    "measure": cmd_measure,
}


def main(argv: list[str]) -> int:
    # Excerpts carry the repository's own UTF-8 text; a cp1252 console would
    # raise on the first non-Latin-1 character. Reconfigure rather than lose
    # bytes - the excerpt is evidence.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    if not argv or argv[0] not in COMMANDS:
        print(__doc__)
        return 2
    return COMMANDS[argv[0]](_repo(), argv[1:])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
