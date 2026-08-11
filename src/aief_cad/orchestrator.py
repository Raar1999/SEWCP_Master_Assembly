"""The CAD orchestrator - central coordinator, and authority for nothing.

It receives engineering requirements, determines which domains are involved,
dispatches bounded work to the agents that own those domains, resolves their
contributions into a design solution, compiles the solution into operations,
drives them across the Fusion boundary, collects what Fusion actually built,
dispatches independent verification, and handles the verdict.

What it does **not** do is decide any engineering question. Domain routing is a
lookup against the requirement kinds the package states; every value in the
solution came from an agent or from the package; and the verdict comes from
verifiers it does not implement. It contains no knowledge of any particular
component - `tests/test_cad_general_purpose.py` asserts that as a property of
the source, not as a claim in this docstring.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from aief_cad import PROTOCOL_VERSION, RUNS_DIR, CadError
from aief_cad.agents import select_agents, unroutable_kinds
from aief_cad.bridge.client import AgentBridge, FileQueueBridge
from aief_cad.bridge.protocol import Command, Observation
from aief_cad.digest import canonical_json, digest_of, short
from aief_cad.loop import NoProgress, RepairPlan, propose_repair, sequence_digest
from aief_cad.observe import ObservedModel, merge_observations
from aief_cad.ops import Op, compile_solution
from aief_cad.requirements import RequirementPackage, load_package
from aief_cad.solution import DesignSolution, resolve
from aief_cad.verify import Verdict, run_all

__all__ = ["OrchestratorError", "RunRecord", "Orchestrator"]


class OrchestratorError(CadError):
    """The run cannot proceed."""


@dataclass
class RunRecord:
    """Everything needed to reproduce and audit one orchestrated run."""

    run_id: str
    package_id: str
    package_digest: str
    component: str
    domains: tuple[str, ...]
    agents: tuple[str, ...]
    solution_id: str = ""
    solution_digest: str = ""
    attempts: list[dict[str, Any]] = field(default_factory=list)
    verdict: str = "NOT-RUN"
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None
    escalations: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "protocol": PROTOCOL_VERSION,
            "run_id": self.run_id,
            "package_id": self.package_id,
            "package_digest": self.package_digest,
            "component": self.component,
            "domains": list(self.domains),
            "agents": list(self.agents),
            "solution_id": self.solution_id,
            "solution_digest": self.solution_digest,
            "attempts": self.attempts,
            "verdict": self.verdict,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "escalations": self.escalations,
        }


class Orchestrator:
    """Coordinates one requirement package to a CAD verdict."""

    def __init__(
        self,
        bridge: AgentBridge | None = None,
        runs_dir: Path | None = None,
        session: str = "unrecorded-session",
        issued_by: str = "mechanical.cad-engineer",
        max_attempts: int = 3,
    ) -> None:
        self.bridge = bridge or FileQueueBridge()
        self.runs_dir = Path(runs_dir or RUNS_DIR)
        self.session = session
        self.issued_by = issued_by
        if max_attempts < 1:
            raise OrchestratorError("max_attempts must be at least 1")
        self.max_attempts = max_attempts

    # -- 1..3  ingest, determine domains, decompose ------------------------

    def design(self, package: RequirementPackage, run_id: str) -> DesignSolution:
        """Route to agents and resolve their contributions into a solution."""
        orphans = unroutable_kinds(package)
        if orphans:
            raise OrchestratorError(
                f"{package.package_id}: requirement kind(s) {', '.join(orphans)} "
                f"have no registered agent. A requirement nobody owns is a "
                f"requirement nobody is reasoning about, so the run stops here "
                f"rather than producing a solution that silently omits it"
            )
        agents = select_agents(package)
        contributions = [a.contribute(package) for a in agents]
        return resolve(package, contributions, solution_id=f"{run_id}.S1")

    # -- 9..10  dispatch and collect ---------------------------------------

    def dispatch(
        self, ops: Sequence[Op], solution: DesignSolution, prefix: str = "C"
    ) -> tuple[list[Observation], str | None]:
        """Send each operation and collect what Fusion reported.

        Stops at the first operation that did not execute. Continuing past a
        failed mutating operation builds on a model state nobody has described.
        """
        observations: list[Observation] = []
        target = {"document": _document_name(solution), "solution": solution.solution_id}

        for n, op in enumerate(ops, start=1):
            cmd = Command(
                command_id=f"{prefix}-{solution.solution_id}-{n:04d}",
                op=op.op,
                args=op.args,
                issued_by=self.issued_by,
                session=self.session,
                solution_id=solution.solution_id,
                model_target=target,
                # Salted with the solution id: the same operation against a
                # different run is a different effect, and answering it from
                # another run's recorded observation is stale evidence, not
                # idempotency. Within one run - a resume - reuse still holds.
                idempotency_key=digest_of(
                    canonical_json({"solution": solution.solution_id,
                                    "key": op.idempotency_key()})
                ),
                op_id=op.op_id,
                feature=op.feature,
            )
            obs = self.bridge.send(cmd)
            observations.append(obs)
            if not obs.ok:
                return observations, (
                    f"{op.op_id} ({op.op}) did not execute - "
                    f"{obs.status}: {obs.error_message()}"
                )
        return observations, None

    # -- 11..14  verify, verdict, bounded repair ---------------------------

    def run(self, package_path: str | Path, run_id: str | None = None) -> RunRecord:
        """Requirements in, CAD verdict out."""
        package = load_package(package_path)
        rid = run_id or f"RUN-{time.strftime('%Y%m%dT%H%M%S')}-{short(package.digest, 6)}"
        record = RunRecord(
            run_id=rid,
            package_id=package.package_id,
            package_digest=package.digest,
            component=package.component,
            domains=package.domains(),
            agents=tuple(a.name for a in select_agents(package)),
        )

        solution = self.design(package, rid)
        record.solution_id = solution.solution_id
        record.solution_digest = solution.digest

        ops = compile_solution(solution)
        attempt = 1
        last_ops: tuple[Op, ...] = ops

        while True:
            observations, halt = self.dispatch(ops, solution, prefix=f"A{attempt}")
            model = merge_observations(observations)
            verdict = run_all(solution, model, attempt=attempt)

            record.attempts.append(
                {
                    "attempt": attempt,
                    "ops": [o.as_dict() for o in ops],
                    "sequence_digest": sequence_digest(ops),
                    "execution_halt": halt,
                    "executed": sum(1 for o in observations if o.ok),
                    "dispatched": len(observations),
                    "observations": [o.raw for o in observations],
                    "observed_model": model.as_dict(),
                    "verdict": verdict.as_dict(),
                }
            )
            record.verdict = verdict.verdict

            if verdict.passed and halt is None:
                break
            if attempt >= self.max_attempts:
                record.escalations.append(
                    f"attempt limit {self.max_attempts} reached with "
                    f"{len(verdict.failures)} check(s) still failing"
                )
                break

            try:
                plan: RepairPlan = propose_repair(verdict, solution, last_ops, attempt + 1)
            except NoProgress as exc:
                record.escalations.append(str(exc))
                break
            if not plan.repairable:
                record.escalations.append(plan.rationale)
                record.attempts[-1]["repair"] = plan.as_dict()
                break

            record.attempts[-1]["repair"] = plan.as_dict()
            last_ops = ops
            ops = plan.ops
            attempt += 1

        record.finished_at = time.time()
        self._write(record)
        return record

    # -- persistence -------------------------------------------------------

    def _write(self, record: RunRecord) -> Path:
        d = self.runs_dir / record.run_id
        d.mkdir(parents=True, exist_ok=True)
        body = record.as_dict()
        body["record_digest"] = digest_of(canonical_json(body))
        path = d / "run.json"
        path.write_bytes(json.dumps(body, indent=2, sort_keys=True).encode("utf-8") + b"\n")
        return path


def _document_name(solution: DesignSolution) -> str:
    for f in solution.features:
        if f.kind == "document":
            return str(f.params.get("name", solution.component))
    return solution.component
