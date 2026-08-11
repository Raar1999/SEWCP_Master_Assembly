"""Geometry verifier - does the built solid match the required form?

Reads the observed bounding box, volume and body inventory. Owns acceptance
conditions of check family `geometry` and `mass`, and adds intrinsic checks
derived from the solution itself so that a solution with no acceptance
conditions is still not vacuously verified.
"""

from __future__ import annotations

import math

from aief_cad.observe import ObservedModel
from aief_cad.solution import DesignSolution

__all__ = ["verify_geometry"]


def _curve_points(curve: dict, step: float = 0.5) -> list[tuple[float, float]]:
    """Sample an observed curve. Deliberately reimplemented here rather than
    imported from the routing layer: the verifier measures with its own
    ruler, not the producer's."""
    kind = curve.get("type")
    if kind == "line":
        (x0, y0), (x1, y1) = curve["start"], curve["end"]
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        return [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n)
                for i in range(n + 1)]
    if kind in ("arc", "circle"):
        cx, cy = curve["center"]
        r = float(curve["radius"])
        if kind == "circle":
            n = max(8, int(2 * math.pi * r / step))
            return [(cx + r * math.cos(2 * math.pi * i / n),
                     cy + r * math.sin(2 * math.pi * i / n))
                    for i in range(n + 1)]
        a0 = math.atan2(curve["start"][1] - cy, curve["start"][0] - cx)
        a1 = math.atan2(curve["end"][1] - cy, curve["end"][0] - cx)
        sweep = (a1 - a0) % (2 * math.pi)
        mid = curve.get("mid")
        if mid is not None:
            am = math.atan2(mid[1] - cy, mid[0] - cx)
            if (am - a0) % (2 * math.pi) > sweep:
                sweep = sweep - 2 * math.pi  # the arc runs the other way
        if abs(sweep) < 1e-9:
            sweep = 2 * math.pi
        n = max(2, int(abs(sweep) * r / step))
        return [(cx + r * math.cos(a0 + sweep * i / n),
                 cy + r * math.sin(a0 + sweep * i / n))
                for i in range(n + 1)]
    return []


def _path_findings(feat, model: ObservedModel, area: str):
    """Constraint re-checks for one routed-path feature, from observation."""
    from aief_cad.verify import Finding

    p = feat.params
    name = p.get("sketch", "")
    sk = model.sketch(name)
    geometry = tuple(sk.curve_geometry) if sk is not None else ()
    if not geometry:
        yield Finding(
            id=f"GEO-PATH-OBSERVED-{feat.id}",
            passed=False,
            subject=f"sketch:{name}.curve_geometry",
            expected="curve geometry reported by the observing add-in",
            observed="absent" if sk is not None else "sketch not observed",
            detail=(
                "the routed path cannot be verified without observed curve "
                "geometry; unmeasured is not compliant"
            ),
            area=area,
        )
        return
    wall = [c for c in geometry if not c.get("construction")]
    center = [c for c in geometry if c.get("construction")]
    wall_pts = [pt for c in wall for pt in _curve_points(c)]

    for ko in p.get("keep_outs", []):
        ax = ko["r"] * math.cos(math.radians(ko["az_deg"]))
        ay = ko["r"] * math.sin(math.radians(ko["az_deg"]))
        d = min((math.hypot(x - ax, y - ay) for x, y in wall_pts),
                default=None)
        need = float(ko["wall_clearance"])
        ok = d is not None and d >= need - 0.01
        yield Finding(
            id=f"GEO-KEEPOUT-{feat.id}-{ko['id']}",
            passed=ok,
            subject=f"sketch:{name}.wall_clearance:{ko['id']}",
            expected=f">= {need}",
            observed=None if d is None else round(d, 3),
            detail="" if ok else (
                f"channel wall approaches keep-out {ko['id']!r} to "
                f"{'nothing measured' if d is None else format(d, '.3f')} mm "
                f"against a required {need} mm"
            ),
            requirement=feat.satisfies[0] if feat.satisfies else None,
            area=area,
        )

    r_min = p.get("envelope_wall_min_r")
    r_max = p.get("envelope_wall_max_r")
    if r_min is not None and r_max is not None and wall_pts:
        radii = [math.hypot(x, y) for x, y in wall_pts]
        lo, hi = min(radii), max(radii)
        ok = lo >= float(r_min) - 0.01 and hi <= float(r_max) + 0.01
        yield Finding(
            id=f"GEO-ENVELOPE-{feat.id}",
            passed=ok,
            subject=f"sketch:{name}.envelope",
            expected=f"wall within [{r_min}, {r_max}]",
            observed=f"[{lo:.2f}, {hi:.2f}]",
            detail="" if ok else "channel wall leaves the declared annulus",
            requirement=feat.satisfies[0] if feat.satisfies else None,
            area=area,
        )

    min_bend = p.get("min_bend_r")
    if min_bend is not None:
        bends = [float(c["radius"]) for c in center if c.get("type") == "arc"]
        worst = min(bends, default=None)
        ok = worst is not None and worst >= float(min_bend) - 0.01
        yield Finding(
            id=f"GEO-BEND-{feat.id}",
            passed=ok,
            subject=f"sketch:{name}.min_bend_radius",
            expected=f">= {min_bend}",
            observed=None if worst is None else round(worst, 3),
            detail="" if ok else (
                "no centreline arc observed" if worst is None else
                f"tightest observed centreline bend {worst:.2f} mm is below "
                f"the minimum {min_bend} mm"
            ),
            requirement=feat.satisfies[0] if feat.satisfies else None,
            area=area,
        )


def verify_geometry(solution: DesignSolution, model: ObservedModel):
    from aief_cad.verify import Finding, VerifierReport, _acceptance_findings

    area = "geometry"
    findings = list(_acceptance_findings(solution, model, ("geometry", "mass"), area))

    # -- intrinsic: a solution that extrudes must produce a solid -----------
    extrudes = [f for f in solution.features if f.kind == "extrude"
                and f.params.get("operation", "new_body") in ("new_body", "join")]
    if extrudes:
        findings.append(
            Finding(
                id="GEO-BODY-PRESENT",
                passed=bool(model.bodies),
                subject="bodies.count",
                expected=">= 1",
                observed=len(model.bodies),
                detail="" if model.bodies else (
                    "the solution extrudes a solid but the model reports no body"
                ),
                area=area,
            )
        )

    # -- intrinsic: extrude distance appears as a real extent ---------------
    # Valid only for new_body extrudes, and only when no join later extends
    # the body - a joined stack's extent belongs to the whole stack, which
    # the package's own acceptance states, not to any single extrude.
    axis_of = {"X": 0, "Y": 1, "Z": 2}
    has_joins = any(f.params.get("operation") == "join" for f in extrudes)
    for feat in [f for f in extrudes
                 if not has_joins
                 and f.params.get("operation", "new_body") == "new_body"]:
        distance = feat.params.get("distance")
        expected = solution.resolved.get(distance) if isinstance(distance, str) else None
        if expected is None:
            continue
        body = model.body(feat.params.get("body_name"))
        if body is None:
            findings.append(
                Finding(
                    id=f"GEO-EXTENT-{feat.id}",
                    passed=False,
                    subject=f"body:{feat.params.get('body_name', '')}.dz",
                    expected=expected,
                    observed=None,
                    detail="named body is not present in the observed model",
                    area=area,
                )
            )
            continue
        # An extrude on a planar sketch grows along the plane normal; for the
        # base planes this layer emits, that is the axis the sketch does not lie in.
        normal = {"XY": "Z", "XZ": "Y", "YZ": "X"}.get(
            _plane_of(solution, feat.params.get("sketch", "")), "Z"
        )
        got = body.extent(axis_of[normal])
        ok = got is not None and abs(got - float(expected)) <= 1e-3
        findings.append(
            Finding(
                id=f"GEO-EXTENT-{feat.id}",
                passed=ok,
                subject=f"body:{body.name}.d{normal.lower()}",
                expected=float(expected),
                observed=got,
                detail="" if ok else (
                    f"extrude {feat.id} declares distance {distance}="
                    f"{float(expected):g}; the body measures "
                    f"{'nothing' if got is None else format(got, '.4f')} along {normal}"
                ),
                area=area,
            )
        )

    # -- intrinsic: a routed path is re-verified against its constraints ----
    for feat in solution.features:
        if feat.kind == "sketch_path":
            findings.extend(_path_findings(feat, model, area))

    if not findings:
        findings.append(
            Finding(
                id="GEO-NO-CHECKS",
                passed=False,
                subject="solution.acceptance",
                expected="at least one geometry check",
                observed=0,
                detail=(
                    "no geometry acceptance condition and no extrude to derive "
                    "one from. An unverified solution is not a passed one"
                ),
                area=area,
            )
        )
    return VerifierReport(verifier="geometry", findings=tuple(findings))


def _plane_of(solution: DesignSolution, sketch_name: str) -> str:
    for f in solution.features:
        if f.kind == "sketch" and f.params.get("name") == sketch_name:
            return str(f.params.get("plane", "XY"))
    return "XY"
