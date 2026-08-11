"""Interface verifier - are the mating features where the interfaces say?

Owns acceptance conditions of check family `interface`, and adds intrinsic
checks over the datum and locating geometry a solution declares: named
construction planes at their declared offsets, and the locating sketches that
later features are required to derive from.

An interface the current bounded run does not build is reported as `deferred`
and is not counted as a pass. Silently passing an interface nobody built is how
a partial model comes to look complete.
"""

from __future__ import annotations

from aief_cad.observe import ObservedModel
from aief_cad.solution import DesignSolution

__all__ = ["verify_interfaces", "deferred_interfaces"]


def _built_feature_ids(solution: DesignSolution) -> set[str]:
    return {f.id for f in solution.features}


def deferred_interfaces(solution: DesignSolution) -> tuple[str, ...]:
    """Interfaces declared by the package that this solution does not realise."""
    realised: set[str] = set()
    for f in solution.features:
        realised |= set(f.satisfies)
        ref = f.params.get("interface")
        if isinstance(ref, str):
            realised.add(ref)
    return tuple(i.id for i in solution.interfaces if i.id not in realised)


def verify_interfaces(solution: DesignSolution, model: ObservedModel):
    from aief_cad.verify import Finding, VerifierReport, _acceptance_findings

    area = "interface"
    findings = list(_acceptance_findings(solution, model, ("interface",), area))

    # -- intrinsic: every declared construction plane exists at its offset --
    for feat in solution.features:
        if feat.kind != "offset_plane":
            continue
        name = str(feat.params.get("name", ""))
        offset_param = feat.params.get("offset")
        expected = (
            solution.resolved.get(offset_param) if isinstance(offset_param, str) else None
        )
        observed_plane = model.plane(name)
        if observed_plane is None:
            findings.append(
                Finding(
                    id=f"IF-PLANE-{feat.id}",
                    passed=False,
                    subject=f"plane:{name}.exists",
                    expected=True,
                    observed=False,
                    detail=(
                        f"construction plane {name!r} is declared by the solution "
                        f"and absent from the model; every feature that locates "
                        f"against it is unlocated"
                    ),
                    area=area,
                )
            )
            continue
        if expected is None:
            continue
        got = observed_plane.offset_mm
        ok = got is not None and abs(got - float(expected)) <= 1e-4
        findings.append(
            Finding(
                id=f"IF-PLANE-{feat.id}",
                passed=ok,
                subject=f"plane:{name}.offset_mm",
                expected=float(expected),
                observed=got,
                detail="" if ok else (
                    f"{name} should sit at {float(expected):g} mm "
                    f"({offset_param}); it reports "
                    f"{'nothing' if got is None else format(got, '.4f')}"
                ),
                area=area,
            )
        )

    # -- intrinsic: locating sketches exist ---------------------------------
    for feat in solution.features:
        if feat.kind not in ("sketch", "construction_sketch"):
            continue
        name = str(feat.params.get("name") or feat.params.get("sketch", ""))
        if not name:
            continue
        present = model.sketch(name) is not None
        if feat.kind == "construction_sketch" and not present:
            findings.append(
                Finding(
                    id=f"IF-SKETCH-{feat.id}",
                    passed=False,
                    subject=f"sketch:{name}.exists",
                    expected=True,
                    observed=False,
                    detail=(
                        f"locating sketch {name!r} is absent; it is the single "
                        f"source of angular and radial position for every "
                        f"feature declared to derive from it"
                    ),
                    area=area,
                )
            )

    if not findings:
        findings.append(
            Finding(
                id="IF-NONE-IN-SCOPE",
                passed=True,
                subject="solution.interfaces",
                expected="no interface realised in this bounded solution",
                observed=len(deferred_interfaces(solution)),
                detail=(
                    "this solution realises no interface feature, so there is "
                    "nothing for this verifier to check. Deferred interfaces: "
                    + (", ".join(deferred_interfaces(solution)) or "none")
                ),
                area=area,
            )
        )
    return VerifierReport(verifier="interface", findings=tuple(findings))
