"""The Design Solution - the controlled handoff between reasoning and execution.

The solution states **what should be built**. It does not state how Fusion will
build it (that is `ops.py`) and it certainly does not state what Fusion did
build (that is `observe.py`). Keeping the three apart is the whole point of the
boundary: a layer that lets them blur will eventually report the intent as the
outcome.

A solution is assembled from `DesignContribution`s, one per domain agent. Each
contribution declares the keys it writes, so two agents writing the same key
with different content is a detected conflict rather than a last-writer-wins
merge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

from aief_cad import CadError
from aief_cad.digest import canonical_json, digest_of
from aief_cad.expr import resolve_all
from aief_cad.requirements import RequirementPackage

__all__ = [
    "SolutionError",
    "DesignConflict",
    "FeatureSpec",
    "DesignContribution",
    "DesignSolution",
    "resolve",
]


class SolutionError(CadError):
    """A design solution is incomplete, inconsistent, or unresolvable."""


class DesignConflict(SolutionError):
    """Two agents produced incompatible content for the same key.

    Raised, never averaged. Reconciling two engineering opinions is an
    engineering decision, and this layer holds no authority to take one.
    """


@dataclass(frozen=True)
class FeatureSpec:
    """One thing that must exist in the finished model.

    `kind` is a general geometric category, not a Fusion command. The compiler
    in `ops.py` decides which Fusion operations realise it.
    """

    id: str
    kind: str
    params: dict[str, Any] = field(default_factory=dict)
    satisfies: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    rationale: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "params": self.params,
            "satisfies": list(self.satisfies),
            "depends_on": list(self.depends_on),
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class DesignContribution:
    """One agent's bounded output.

    `writes` is the agent's declared write scope over the solution. It is
    checked against what the contribution actually carries, so an agent cannot
    quietly widen its own authority.
    """

    agent: str
    domain: str
    writes: tuple[str, ...]
    features: tuple[FeatureSpec, ...] = ()
    constraints: tuple[dict[str, Any], ...] = ()
    parameters: tuple[Any, ...] = ()
    notes: tuple[str, ...] = ()
    consumed: tuple[str, ...] = ()

    def content_keys(self) -> set[str]:
        keys = set()
        if self.features:
            keys |= {f"feature:{f.id}" for f in self.features}
        if self.parameters:
            keys |= {f"parameter:{p.name}" for p in self.parameters}
        if self.constraints:
            keys |= {f"constraint:{c['id']}" for c in self.constraints}
        return keys

    def validate(self) -> None:
        declared = set(self.writes)
        actual = self.content_keys()
        outside = {
            k for k in actual
            if not any(k == d or (d.endswith("*") and k.startswith(d[:-1])) for d in declared)
        }
        if outside:
            raise SolutionError(
                f"{self.agent}: contribution writes {', '.join(sorted(outside))}, "
                f"which its declared scope {', '.join(sorted(declared))} does not "
                f"cover. An agent may not widen its own scope by writing outside it"
            )


@dataclass(frozen=True)
class DesignSolution:
    """What should be built, with provenance for every element."""

    solution_id: str
    component: str
    package_id: str
    package_digest: str
    parameters: tuple[Any, ...]
    resolved: dict[str, float]
    features: tuple[FeatureSpec, ...]
    constraints: tuple[dict[str, Any], ...]
    interfaces: tuple[Any, ...]
    material: Any | None
    acceptance: tuple[Any, ...]
    provenance: dict[str, str]
    authority: tuple[str, ...]
    digest: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "solution_id": self.solution_id,
            "component": self.component,
            "package_id": self.package_id,
            "package_digest": self.package_digest,
            "parameters": [
                {
                    "name": p.name,
                    "expression": p.expression,
                    "unit": p.unit,
                    "comment": p.comment,
                    "source": p.source,
                }
                for p in self.parameters
            ],
            "resolved": {k: self.resolved[k] for k in sorted(self.resolved)},
            "features": [f.as_dict() for f in self.features],
            "constraints": list(self.constraints),
            "interfaces": [
                {"id": i.id, "mates_to": i.mates_to, "nature": i.nature,
                 "features": list(i.features)}
                for i in self.interfaces
            ],
            "material": (
                None if self.material is None
                else {"name": self.material.name, "density": self.material.density}
            ),
            "acceptance": [
                {"id": a.id, "check": a.check, "subject": a.subject, "expect": a.expect,
                 "tolerance": a.tolerance, "unit": a.unit, "requirement": a.requirement}
                for a in self.acceptance
            ],
            "provenance": {k: self.provenance[k] for k in sorted(self.provenance)},
            "authority": list(self.authority),
        }

    def feature(self, fid: str) -> FeatureSpec | None:
        for f in self.features:
            if f.id == fid:
                return f
        return None

    def ordered_features(self) -> tuple[FeatureSpec, ...]:
        """Topologically ordered by `depends_on`.

        Feature order is a manufacturing fact, not a convenience: a fillet
        applied before the holes it must meet produces different geometry, and
        `depends_on` is where an agent records that.
        """
        remaining = {f.id: f for f in self.features}
        ordered: list[FeatureSpec] = []
        placed: set[str] = set()
        while remaining:
            ready = [
                f for f in remaining.values()
                if all(d in placed for d in f.depends_on)
            ]
            if not ready:
                raise SolutionError(
                    "cyclic feature dependency among: " + ", ".join(sorted(remaining))
                )
            # Stable: declaration order within a ready set.
            first = min(ready, key=lambda f: [x.id for x in self.features].index(f.id))
            ordered.append(first)
            placed.add(first.id)
            del remaining[first.id]
        return tuple(ordered)


def _merge_conflict_check(contributions: Sequence[DesignContribution]) -> None:
    """Detect two agents claiming the same key with different content."""
    owner: dict[str, tuple[str, bytes]] = {}
    for c in contributions:
        payload: dict[str, bytes] = {}
        for f in c.features:
            payload[f"feature:{f.id}"] = canonical_json(f.as_dict())
        for p in c.parameters:
            payload[f"parameter:{p.name}"] = canonical_json(
                {"expression": p.expression, "unit": p.unit}
            )
        for k in c.constraints:
            payload[f"constraint:{k['id']}"] = canonical_json(k)
        for key, blob in payload.items():
            if key in owner and owner[key][1] != blob:
                raise DesignConflict(
                    f"{key}: {owner[key][0]} and {c.agent} produced different "
                    f"content for the same key. This is an engineering "
                    f"disagreement and is escalated, not merged"
                )
            owner.setdefault(key, (c.agent, blob))


def resolve(
    package: RequirementPackage,
    contributions: Iterable[DesignContribution],
    solution_id: str,
) -> DesignSolution:
    """Reconcile agent contributions into one design solution."""
    contribs = list(contributions)
    if not contribs:
        raise SolutionError("no design contributions: nothing to resolve")
    for c in contribs:
        c.validate()
    _merge_conflict_check(contribs)

    features: list[FeatureSpec] = []
    constraints: list[dict[str, Any]] = []
    provenance: dict[str, str] = {}
    seen_features: set[str] = set()
    seen_constraints: set[str] = set()

    for c in contribs:
        for f in c.features:
            if f.id in seen_features:
                continue
            features.append(f)
            seen_features.add(f.id)
            provenance[f"feature:{f.id}"] = f"{c.agent} ({c.domain})"
        for k in c.constraints:
            if k["id"] in seen_constraints:
                continue
            constraints.append(k)
            seen_constraints.add(k["id"])
            provenance[f"constraint:{k['id']}"] = f"{c.agent} ({c.domain})"

    # Parameters come from the package; an agent may add derived ones but may
    # not restate a package parameter with a different expression - that is
    # caught above as a conflict.
    params = list(package.parameters)
    known = {p.name for p in params}
    for c in contribs:
        for p in c.parameters:
            if p.name not in known:
                params.append(p)
                known.add(p.name)
                provenance[f"parameter:{p.name}"] = f"{c.agent} ({c.domain})"
    for p in package.parameters:
        provenance.setdefault(f"parameter:{p.name}", f"requirement package {package.package_id}")

    resolved = resolve_all(params)

    unsatisfied = [
        s for f in features for s in f.satisfies if package.requirement(s) is None
    ]
    if unsatisfied:
        raise SolutionError(
            "feature(s) claim to satisfy requirement(s) the package does not "
            f"declare: {', '.join(sorted(set(unsatisfied)))}"
        )

    solution = DesignSolution(
        solution_id=solution_id,
        component=package.component,
        package_id=package.package_id,
        package_digest=package.digest,
        parameters=tuple(params),
        resolved=resolved,
        features=tuple(features),
        constraints=tuple(constraints),
        interfaces=package.interfaces,
        material=package.material,
        acceptance=package.acceptance,
        provenance=provenance,
        authority=package.authority,
    )
    solution.ordered_features()  # raises on a cycle, before anything is dispatched
    body = solution.as_dict()
    return DesignSolution(**{**solution.__dict__, "digest": digest_of(canonical_json(body))})
