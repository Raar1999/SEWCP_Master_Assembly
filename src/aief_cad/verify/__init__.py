"""Independent verification of what Fusion actually built.

Three verifiers, one verdict. Each reads only `ObservedModel` - the state
Fusion reported - and the `DesignSolution` it is checked against. **No verifier
reads `Observation.executed`.** A successful API call is the executing party's
report on its own work; treating it as evidence that the model satisfies a
requirement is the exact conflation this architecture exists to prevent.

Two failure modes are treated as failures rather than as absent data:

    unresolvable subject   the model does not carry the attribute the
                           acceptance condition names -> FAIL, not SKIP
    empty model            nothing was observed -> every verifier fails

A check that cannot be evaluated has not passed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

from aief_cad import CadError
from aief_cad.digest import canonical_json, digest_of
from aief_cad.observe import ObservedModel
from aief_cad.solution import DesignSolution

__all__ = [
    "VerificationError",
    "Finding",
    "VerifierReport",
    "Verdict",
    "resolve_subject",
    "compare",
    "run_all",
    "VERIFIERS",
]


class VerificationError(CadError):
    """A verifier could not run at all - distinct from a verifier that failed."""


_UNRESOLVED = object()


@dataclass(frozen=True)
class Finding:
    """One check outcome. `expected` and `observed` are always both recorded."""

    id: str
    passed: bool
    subject: str
    expected: Any
    observed: Any
    detail: str = ""
    requirement: str | None = None
    area: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "passed": self.passed,
            "subject": self.subject,
            "expected": self.expected,
            "observed": self.observed if self.observed is not _UNRESOLVED else None,
            "detail": self.detail,
            "requirement": self.requirement,
            "area": self.area,
        }


@dataclass(frozen=True)
class VerifierReport:
    verifier: str
    findings: tuple[Finding, ...] = ()

    @property
    def passed(self) -> bool:
        return all(f.passed for f in self.findings)

    @property
    def failures(self) -> tuple[Finding, ...]:
        return tuple(f for f in self.findings if not f.passed)

    def as_dict(self) -> dict[str, Any]:
        return {
            "verifier": self.verifier,
            "passed": self.passed,
            "checks": len(self.findings),
            "failed": len(self.failures),
            "findings": [f.as_dict() for f in self.findings],
        }


@dataclass(frozen=True)
class Verdict:
    """The CAD verdict. PASS only when every verifier passes."""

    solution_id: str
    reports: tuple[VerifierReport, ...]
    attempt: int = 1
    digest: str = ""

    @property
    def passed(self) -> bool:
        return bool(self.reports) and all(r.passed for r in self.reports)

    @property
    def verdict(self) -> str:
        return "PASS" if self.passed else "FAIL"

    @property
    def failures(self) -> tuple[Finding, ...]:
        return tuple(f for r in self.reports for f in r.failures)

    @property
    def check_count(self) -> int:
        return sum(len(r.findings) for r in self.reports)

    def as_dict(self) -> dict[str, Any]:
        return {
            "solution_id": self.solution_id,
            "attempt": self.attempt,
            "verdict": self.verdict,
            "checks": self.check_count,
            "failed": len(self.failures),
            "reports": [r.as_dict() for r in self.reports],
        }


# --------------------------------------------------------------------------
# Subject resolution - the shared grammar every verifier reads model state with
# --------------------------------------------------------------------------

def resolve_subject(model: ObservedModel, subject: str) -> Any:
    """Resolve a dotted subject against observed model state.

    Grammar, deliberately small and uniform:

        document.units                  component.name
        bodies.count                    sketches.count      planes.count
        parameters.count
        body.<attr>                     body:<name>.<attr>
        sketch:<name>.<attr>            plane:<name>.<attr>
        parameter:<name>.<attr>

    Returns the sentinel `_UNRESOLVED` when the model does not carry the
    attribute, which every caller turns into a FAIL. It never returns `None`
    for "missing", because `None` is a legitimate observed value.
    """
    if "." not in subject:
        return _UNRESOLVED
    head, _, attr = subject.partition(".")

    if head == "document":
        return model.document.get(attr, _UNRESOLVED)
    if head == "component":
        return model.component.get(attr, _UNRESOLVED)
    if head == "bodies" and attr == "count":
        return len(model.bodies)
    if head == "sketches" and attr == "count":
        return len(model.sketches)
    if head == "planes" and attr == "count":
        return len(model.planes)
    if head == "parameters" and attr == "count":
        return len(model.parameters)
    if head == "features" and attr == "count":
        return len(model.features)

    kind, _, name = head.partition(":")

    if kind == "body":
        body = model.body(name or None)
        if body is None:
            return _UNRESOLVED
        if attr == "exists":
            return True
        return getattr(body, attr, _UNRESOLVED)
    if kind == "sketch":
        sk = model.sketch(name)
        if attr == "exists":
            return sk is not None
        if sk is None:
            return _UNRESOLVED
        return getattr(sk, attr, _UNRESOLVED)
    if kind == "plane":
        pl = model.plane(name)
        if attr == "exists":
            return pl is not None
        if pl is None:
            return _UNRESOLVED
        return getattr(pl, attr, _UNRESOLVED)
    if kind == "parameter":
        pm = model.parameter(name)
        if attr == "exists":
            return pm is not None
        if pm is None:
            return _UNRESOLVED
        if attr == "is_derived":
            return not pm.is_literal_expression
        return getattr(pm, attr, _UNRESOLVED)
    return _UNRESOLVED


#: Default numeric tolerance, in the model's own units. Tight enough that a
#: wrong dimension cannot hide inside it, loose enough to absorb Fusion's
#: internal cm/mm conversion.
DEFAULT_TOL = 1e-6


def compare(observed: Any, expected: Any, tolerance: float | None) -> tuple[bool, str]:
    """Compare one observed value against one expectation."""
    if observed is _UNRESOLVED:
        return False, (
            "not present in the observed model. A check that cannot be "
            "evaluated has not passed"
        )
    if isinstance(expected, bool) or isinstance(observed, bool):
        return (observed == expected), ("" if observed == expected else "boolean mismatch")
    if isinstance(expected, (int, float)) and isinstance(observed, (int, float)):
        tol = DEFAULT_TOL if tolerance is None else abs(tolerance)
        delta = abs(float(observed) - float(expected))
        if delta <= tol:
            return True, ""
        return False, f"delta {delta:.6g} exceeds tolerance {tol:g}"
    if isinstance(expected, (int, float)) != isinstance(observed, (int, float)):
        return False, (
            f"type mismatch: expected {type(expected).__name__}, observed "
            f"{type(observed).__name__}"
        )
    return (observed == expected), ("" if observed == expected else "value mismatch")


def _acceptance_findings(
    solution: DesignSolution,
    model: ObservedModel,
    families: Sequence[str],
    area: str,
) -> list[Finding]:
    """Evaluate every acceptance condition whose `check` this verifier owns."""
    out: list[Finding] = []
    for a in solution.acceptance:
        if a.check not in families:
            continue
        observed = resolve_subject(model, a.subject)
        ok, detail = compare(observed, a.expect, a.tolerance)
        out.append(
            Finding(
                id=a.id,
                passed=ok,
                subject=a.subject,
                expected=a.expect,
                observed=None if observed is _UNRESOLVED else observed,
                detail=detail,
                requirement=a.requirement,
                area=area,
            )
        )
    return out


# Imported after the shared types so the submodules can use them.
from aief_cad.verify.geometry import verify_geometry  # noqa: E402
from aief_cad.verify.interface import verify_interfaces  # noqa: E402
from aief_cad.verify.constraint import verify_constraints  # noqa: E402

VERIFIERS: tuple[Callable[[DesignSolution, ObservedModel], VerifierReport], ...] = (
    verify_geometry,
    verify_interfaces,
    verify_constraints,
)


def run_all(
    solution: DesignSolution, model: ObservedModel, attempt: int = 1
) -> Verdict:
    """Run every verifier and produce the CAD verdict."""
    reports = tuple(v(solution, model) for v in VERIFIERS)
    verdict = Verdict(solution_id=solution.solution_id, reports=reports, attempt=attempt)
    return Verdict(
        solution_id=verdict.solution_id,
        reports=verdict.reports,
        attempt=attempt,
        digest=digest_of(canonical_json(verdict.as_dict())),
    )
