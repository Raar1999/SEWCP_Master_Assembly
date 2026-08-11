"""The bounded PASS/FAIL redesign loop.

    DESIGN -> EXECUTE -> OBSERVE -> VERIFY -> PASS? -> NEXT
                  ^                            |
                  |                            v
                  +--------- REDESIGN / REPAIR (bounded)

Two properties this module exists to guarantee:

**No blind retry.** A repair must change the dispatched operation sequence. The
digest of the repair sequence is compared with the digest of the attempt that
failed, and an identical sequence is refused with `NO-PROGRESS` rather than
sent again. Re-running an operation that already produced the observed state
cannot produce a different one.

**No infinite repair.** Attempts are capped. On exhaustion the loop stops and
reports the surviving findings, which is a real outcome; it does not degrade
into a pass.

A diagnosis names five things, because a failure that names fewer cannot be
acted on: the failed requirement, the observed evidence, the responsible design
area, the likely cause, and the proposed correction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from aief_cad import CadError
from aief_cad.digest import canonical_json, digest_of
from aief_cad.ops import Op
from aief_cad.solution import DesignSolution
from aief_cad.verify import Finding, Verdict

__all__ = [
    "LoopError",
    "NoProgress",
    "Diagnosis",
    "RepairPlan",
    "diagnose",
    "propose_repair",
    "sequence_digest",
]


class LoopError(CadError):
    """The repair loop cannot continue."""


class NoProgress(LoopError):
    """A repair would dispatch the identical sequence that just failed."""


#: Which agent owns a repair, by the area the finding came from. A repair
#: routed to the wrong owner is a patch; routed to the owner it is a fix.
_AREA_OWNER = {
    "geometry": "mechanical.design-engineer",
    "interface": "mechanical.simulation-engineer",
    "constraint": "model-setup",
}


@dataclass(frozen=True)
class Diagnosis:
    """Why one check failed, and what would have to change."""

    finding_id: str
    failed_requirement: str
    evidence: str
    responsible_area: str
    responsible_agent: str
    likely_cause: str
    proposed_correction: str
    repairable: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "finding": self.finding_id,
            "failed_requirement": self.failed_requirement,
            "evidence": self.evidence,
            "responsible_area": self.responsible_area,
            "responsible_agent": self.responsible_agent,
            "likely_cause": self.likely_cause,
            "proposed_correction": self.proposed_correction,
            "repairable": self.repairable,
        }


@dataclass(frozen=True)
class RepairPlan:
    """A bounded, non-identical re-dispatch."""

    attempt: int
    ops: tuple[Op, ...]
    diagnoses: tuple[Diagnosis, ...]
    rationale: str = ""

    @property
    def repairable(self) -> bool:
        return bool(self.ops) and any(d.repairable for d in self.diagnoses)

    def as_dict(self) -> dict[str, Any]:
        return {
            "attempt": self.attempt,
            "ops": [o.as_dict() for o in self.ops],
            "diagnoses": [d.as_dict() for d in self.diagnoses],
            "rationale": self.rationale,
        }


def sequence_digest(ops: Sequence[Op]) -> str:
    """Identity of a dispatched sequence, ignoring operation identifiers.

    Identifiers change on every attempt; the *effects* are what must differ for
    a retry to be anything other than a repeat.
    """
    return digest_of(canonical_json([{"op": o.op, "args": o.args} for o in ops]))


def _evidence(f: Finding) -> str:
    return (
        f"{f.subject}: expected {f.expected!r}, observed {f.observed!r}"
        + (f" ({f.detail})" if f.detail else "")
    )


def diagnose(verdict: Verdict, solution: DesignSolution) -> tuple[Diagnosis, ...]:
    """Turn failing findings into actionable diagnoses."""
    out: list[Diagnosis] = []
    for f in verdict.failures:
        area = f.area or "constraint"
        owner = _AREA_OWNER.get(area, "mechanical.design-engineer")
        cause, correction, repairable = _classify(f, solution)
        out.append(
            Diagnosis(
                finding_id=f.id,
                failed_requirement=f.requirement or f.subject,
                evidence=_evidence(f),
                responsible_area=area,
                responsible_agent=owner,
                likely_cause=cause,
                proposed_correction=correction,
                repairable=repairable,
            )
        )
    return tuple(out)


def _classify(f: Finding, solution: DesignSolution) -> tuple[str, str, bool]:
    """Name the cause and the correction for one finding."""
    sub = f.subject

    if sub.startswith("parameter") or f.id.startswith("CON-PARAM"):
        if f.id == "CON-PARAM-PRESENT" or f.observed in (None, False, 0):
            return (
                "the parameter set was not applied, or was applied to a "
                "different document than the one observed",
                "re-dispatch set_parameters for the full solution parameter set",
                True,
            )
        if f.id == "CON-PARAM-DERIVED":
            return (
                "a declared derivation reached the model as a literal, so it no "
                "longer tracks the parameter it was derived from",
                "re-dispatch set_parameters so the expression, not its current "
                "value, is what the model holds",
                True,
            )
        return (
            "the model holds a different value than the solution resolves to",
            "re-dispatch set_parameters; if the value is still wrong the "
            "expression itself disagrees with the requirement and that is an "
            "engineering escalation, not a repair",
            True,
        )

    if sub.startswith("plane:"):
        return (
            "the construction plane is absent or sits at the wrong offset",
            "re-dispatch the offset_plane operation for this datum",
            True,
        )
    if sub.startswith("sketch:"):
        if "fully_constrained" in sub:
            return (
                "the sketch carries degrees of freedom the solution requires it "
                "not to have; a later feature located against it can move",
                "re-dispatch the sketch and its dimensioning operations",
                True,
            )
        return (
            "the sketch is absent from the model",
            "re-dispatch the sketch creation operation",
            True,
        )
    if sub.startswith("body") or sub.startswith("bodies"):
        return (
            "the solid was not created, or its extent does not match the "
            "distance the solution declares",
            "re-dispatch the profile and extrude operations for this body",
            True,
        )
    if sub == "document.units":
        return (
            "the document was created in a different length unit, which "
            "rescales every dimension in the solution",
            "the document unit cannot be corrected in place without "
            "reinterpreting existing geometry - escalate",
            False,
        )
    return (
        "no rule in this layer classifies this failure",
        "escalate to the responsible agent; an unclassified failure is not "
        "repaired by guessing",
        False,
    )


#: Finding id or subject prefix -> the feature kinds whose operations repair it.
_REPAIR_KINDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("CON-PARAM", ("parameters",)),
    ("CON-UNITS", ()),
    ("IF-PLANE", ("offset_plane",)),
    ("IF-SKETCH", ("sketch", "construction_sketch")),
    ("CON-SKETCH", ("sketch", "sketch_circle", "construction_sketch")),
    ("GEO-", ("sketch", "sketch_circle", "extrude")),
)


def _kinds_for(finding_id: str, subject: str) -> tuple[str, ...]:
    for prefix, kinds in _REPAIR_KINDS:
        if finding_id.startswith(prefix):
            return kinds
    if subject.startswith("parameter"):
        return ("parameters",)
    if subject.startswith("plane:"):
        return ("offset_plane",)
    if subject.startswith("sketch:"):
        return ("sketch", "sketch_circle", "construction_sketch")
    if subject.startswith("body"):
        return ("sketch", "sketch_circle", "extrude")
    return ()


def propose_repair(
    verdict: Verdict,
    solution: DesignSolution,
    previous_ops: Sequence[Op],
    attempt: int,
) -> RepairPlan:
    """Build a bounded repair sequence for the findings that failed.

    The repair re-dispatches only the operations whose feature kinds bear on a
    failed check, plus a terminal `observe`. It is not a re-run of the whole
    solution: repeating operations that already succeeded adds risk without
    adding information.
    """
    from aief_cad.ops import compile_solution, validate_sequence

    diagnoses = diagnose(verdict, solution)
    kinds: set[str] = set()
    for f in verdict.failures:
        kinds |= set(_kinds_for(f.id, f.subject))

    if not kinds or not any(d.repairable for d in diagnoses):
        return RepairPlan(
            attempt=attempt,
            ops=(),
            diagnoses=diagnoses,
            rationale=(
                "no repairable finding: every failure is an engineering "
                "escalation, not a re-dispatch"
            ),
        )

    full = compile_solution(solution)
    selected = [o for o in full if o.op != "observe" and _kind_of(o, solution) in kinds]
    if not selected:
        return RepairPlan(
            attempt=attempt,
            ops=(),
            diagnoses=diagnoses,
            rationale=(
                "the failing checks map to feature kinds this solution does not "
                "build; nothing can be re-dispatched to correct them"
            ),
        )

    repair_ops = [
        Op(
            op_id=f"RP{attempt}-{o.op_id}",
            op=o.op,
            args=o.args,
            feature=o.feature,
            satisfies=o.satisfies,
            note=f"repair attempt {attempt}: {o.note}",
        )
        for o in selected
    ]
    repair_ops.append(
        Op(
            op_id=f"RP{attempt}-OBSERVE",
            op="observe",
            args={"scope": ["document", "parameters", "bodies", "sketches", "planes",
                            "features", "material"]},
            note="Re-observe after repair. Verification reads this, not the repair.",
        )
    )
    ops = validate_sequence(repair_ops)

    if sequence_digest(ops) == sequence_digest(previous_ops):
        raise NoProgress(
            f"attempt {attempt}: the proposed repair dispatches the identical "
            f"operation sequence that produced the failing state. Re-running it "
            f"cannot produce a different model. The failure is in the solution "
            f"or in the requirement, not in the execution, and is escalated"
        )

    return RepairPlan(
        attempt=attempt,
        ops=ops,
        diagnoses=diagnoses,
        rationale=(
            f"re-dispatching {len(ops) - 1} operation(s) of kind(s) "
            f"{', '.join(sorted(kinds))} that bear on "
            f"{len(verdict.failures)} failed check(s)"
        ),
    )


def _kind_of(op: Op, solution: DesignSolution) -> str:
    if op.feature is None:
        return ""
    feat = solution.feature(op.feature)
    return feat.kind if feat else ""
