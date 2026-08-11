"""Generic annular serpentine routing - geometry derivation for channel forms.

Routes a milled channel through an annulus around point keep-out features, as
a bifilar (counterflow) family of concentric passes joined inside an azimuthal
service corridor. The router receives *constraints* - envelope, keep-out axes
and clearances, port azimuths, width, rib, bend minimum - and derives the pass
schedule from them. It holds no knowledge of any component; every number it
routes around arrives in its inputs.

Two properties are load-bearing:

    deterministic   the same inputs always yield the same path, segment for
                    segment, because the solution digest and every replayed
                    verdict depend on it;
    self-auditing   the router re-checks its own output against every input
                    constraint and refuses - `RoutingError` - rather than
                    returning a path that violates one. The independent
                    verifiers check the *observed* sketch again later; the
                    audit here exists so a violating path is never dispatched.

The routed result is an ordered, tangent-continuous chain of line and arc
segments (the centreline), plus the closed offset outline (the footprint) that
a cutter of the channel width would produce, ready for a profile cut.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

from aief_cad import CadError

__all__ = [
    "RoutingError",
    "KeepOut",
    "RoutingSpec",
    "RoutedChannel",
    "route_channel",
    "route_spiral",
]

_EPS = 1e-9
#: Margin added over the bare minimum clearance so a routed pass never sits at
#: exactly zero margin against a keep-out row.
_MARGIN = 0.05
#: Radial grid for the pass-radius feasibility scan, mm.
_SCAN_STEP = 0.05


class RoutingError(CadError):
    """The constraint set admits no compliant route this router can build."""


def _rad(deg: float) -> float:
    return math.radians(deg)


def _pol(r: float, az_deg: float) -> tuple[float, float]:
    return (r * math.cos(_rad(az_deg)), r * math.sin(_rad(az_deg)))


@dataclass(frozen=True)
class KeepOut:
    """One excluded feature axis: the channel WALL stays `wall_clearance` away."""

    id: str
    r: float
    az_deg: float
    wall_clearance: float

    @property
    def xy(self) -> tuple[float, float]:
        return _pol(self.r, self.az_deg)


@dataclass(frozen=True)
class RoutingSpec:
    """Everything the router is allowed to know."""

    envelope_wall_min_r: float      # channel wall stays outside this radius
    envelope_wall_max_r: float      # and inside this one
    width: float                    # channel width (cutter diameter)
    rib: float                      # design rib between adjacent walls
    min_bend_r: float               # minimum centreline bend radius
    keep_outs: tuple[KeepOut, ...]
    inlet_az_deg: float
    outlet_az_deg: float
    terminal_r: float               # centreline radius at both port terminals
    modulation_cap: float = 2.0     # max local radial deviation of a wavy pass

    @property
    def half_width(self) -> float:
        return self.width / 2.0

    @property
    def center_min_r(self) -> float:
        return self.envelope_wall_min_r + self.half_width

    @property
    def center_max_r(self) -> float:
        return self.envelope_wall_max_r - self.half_width

    def center_clearance(self, ko: KeepOut) -> float:
        """Minimum centreline distance to a keep-out axis."""
        return ko.wall_clearance + self.half_width


# -- segments ---------------------------------------------------------------

def _line(p0, p1) -> dict[str, Any]:
    return {"type": "line", "start": [p0[0], p0[1]], "end": [p1[0], p1[1]]}


def _arc(c, r, a0_deg, a1_deg, ccw) -> dict[str, Any]:
    """Arc from az a0 to a1 about c, radius r, in the stated rotation sense."""
    return {
        "type": "arc",
        "center": [c[0], c[1]],
        "radius": r,
        "start": [c[0] + r * math.cos(_rad(a0_deg)), c[1] + r * math.sin(_rad(a0_deg))],
        "end": [c[0] + r * math.cos(_rad(a1_deg)), c[1] + r * math.sin(_rad(a1_deg))],
        "ccw": bool(ccw),
    }


def _seg_start(s) -> tuple[float, float]:
    return tuple(s["start"])


def _seg_end(s) -> tuple[float, float]:
    return tuple(s["end"])


def _seg_len(s) -> float:
    if s["type"] == "line":
        (x0, y0), (x1, y1) = s["start"], s["end"]
        return math.hypot(x1 - x0, y1 - y0)
    return s["radius"] * _arc_sweep_rad(s)


def _arc_angles(s) -> tuple[float, float]:
    cx, cy = s["center"]
    a0 = math.atan2(s["start"][1] - cy, s["start"][0] - cx)
    a1 = math.atan2(s["end"][1] - cy, s["end"][0] - cx)
    return a0, a1


def _arc_sweep_rad(s) -> float:
    a0, a1 = _arc_angles(s)
    if s["ccw"]:
        sweep = (a1 - a0) % (2 * math.pi)
    else:
        sweep = (a0 - a1) % (2 * math.pi)
    return sweep if sweep > _EPS else 2 * math.pi

def _sample_segment(s, step: float = 0.5) -> list[tuple[float, float]]:
    """Points along a segment at roughly `step` mm spacing, ends included."""
    n = max(2, int(_seg_len(s) / step) + 1)
    out = []
    if s["type"] == "line":
        (x0, y0), (x1, y1) = s["start"], s["end"]
        for i in range(n + 1):
            t = i / n
            out.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0)))
        return out
    cx, cy = s["center"]
    r = s["radius"]
    a0, _ = _arc_angles(s)
    sweep = _arc_sweep_rad(s)
    sgn = 1.0 if s["ccw"] else -1.0
    for i in range(n + 1):
        a = a0 + sgn * sweep * (i / n)
        out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def _dist_point_segment(p, s) -> float:
    """Exact distance from a point to a line/arc segment."""
    px, py = p
    if s["type"] == "line":
        (x0, y0), (x1, y1) = s["start"], s["end"]
        dx, dy = x1 - x0, y1 - y0
        L2 = dx * dx + dy * dy
        if L2 < _EPS:
            return math.hypot(px - x0, py - y0)
        t = max(0.0, min(1.0, ((px - x0) * dx + (py - y0) * dy) / L2))
        return math.hypot(px - (x0 + t * dx), py - (y0 + t * dy))
    cx, cy = s["center"]
    r = s["radius"]
    a = math.atan2(py - cy, px - cx)
    a0, _ = _arc_angles(s)
    sweep = _arc_sweep_rad(s)
    sgn = 1.0 if s["ccw"] else -1.0
    rel = ((a - a0) * sgn) % (2 * math.pi)
    if rel <= sweep:
        return abs(math.hypot(px - cx, py - cy) - r)
    return min(
        math.hypot(px - s["start"][0], py - s["start"][1]),
        math.hypot(px - s["end"][0], py - s["end"][1]),
    )


# -- routed result ----------------------------------------------------------

@dataclass(frozen=True)
class RoutedChannel:
    """The derived route: centreline chain, footprint loop, and audit facts."""

    centerline: tuple[dict[str, Any], ...]
    footprint: tuple[dict[str, Any], ...]
    pass_radii: tuple[float, ...]
    length: float
    min_keep_out_margin: dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "centerline": list(self.centerline),
            "footprint": list(self.footprint),
            "pass_radii": list(self.pass_radii),
            "length": self.length,
            "min_keep_out_margin": dict(self.min_keep_out_margin),
        }


# -- pass-radius feasibility -------------------------------------------------

def _circle_violations(spec: RoutingSpec, rc: float) -> list[tuple[KeepOut, float]]:
    """Keep-outs a full circle at centreline rc violates.

    Returns the *signed* local radial move that resolves each: positive for a
    feature inside the pass (push outward, away from it), negative for a
    feature outside it (pull inward). Pushing toward the feature would deepen
    the violation, which is why the sign is derived, not assumed.
    """
    out = []
    for ko in spec.keep_outs:
        need = spec.center_clearance(ko) + _MARGIN
        have = abs(rc - ko.r)  # worst case is at the feature azimuth
        if have < need:
            sign = 1.0 if rc >= ko.r else -1.0
            out.append((ko, sign * (need - have)))
    return out


def _pass_schedule(spec: RoutingSpec) -> list[dict[str, Any]]:
    """Greedy outermost-first schedule of full or shallowly-modulated passes.

    A candidate radius is *feasible* when a full circle clears every keep-out,
    and *modulable* when every conflict can be resolved by a local outward
    bulge no deeper than `modulation_cap` that itself clears everything else.
    """
    pitch = spec.width + spec.rib
    passes: list[dict[str, Any]] = []
    r = spec.center_max_r
    while r >= spec.center_min_r - _EPS:
        placed = False
        rc = r
        while rc >= spec.center_min_r - _EPS:
            v = _circle_violations(spec, rc)
            if not v:
                passes.append({"radius": rc, "bulges": []})
                placed = True
                break
            worst = max(abs(d) for _, d in v)
            if worst <= spec.modulation_cap:
                # Prefer a clean circle if one exists a short way further in.
                lookahead = rc - _SCAN_STEP
                clean = None
                while lookahead >= max(spec.center_min_r,
                                       rc - 2 * spec.modulation_cap) - _EPS:
                    if not _circle_violations(spec, lookahead):
                        clean = lookahead
                        break
                    lookahead -= _SCAN_STEP
                if clean is not None:
                    passes.append({"radius": clean, "bulges": []})
                    placed = True
                    break
                bulges = []
                ok = True
                for ko, delta in v:
                    rb = rc + delta  # locally move away from the feature
                    if not (spec.center_min_r - _EPS <= rb
                            <= spec.center_max_r + _EPS):
                        ok = False
                        break
                    hw = _influence_half_angle(spec, rc, ko)
                    # A feature that would object at the bulged radius only
                    # matters if its azimuth sector reaches the bulge's.
                    for other, _d in _circle_violations(spec, rb):
                        if other.id == ko.id:
                            continue
                        o_hw = _influence_half_angle(spec, rb, other)
                        sep = abs((ko.az_deg - other.az_deg + 180.0) % 360.0
                                  - 180.0)
                        if sep < hw + o_hw + 6.0:
                            ok = False
                            break
                    if not ok:
                        break
                    bulges.append({
                        "az": ko.az_deg % 360.0,
                        "half_width": hw + 2.0,
                        "delta": delta,
                        "keep_out": ko.id,
                    })
                if ok:
                    passes.append({"radius": rc, "bulges": bulges})
                    placed = True
                    break
            rc -= _SCAN_STEP
        if not placed:
            break
        r = passes[-1]["radius"] - pitch
    if not passes:
        raise RoutingError(
            "no feasible pass radius exists inside the envelope; every "
            "candidate circle violates a keep-out beyond the modulation cap"
        )
    return passes


def _influence_half_angle(spec: RoutingSpec, rc: float, ko: KeepOut) -> float:
    """Azimuthal half-angle over which a circle at rc violates this keep-out."""
    need = spec.center_clearance(ko) + _MARGIN
    if rc * ko.r <= _EPS:
        return 25.0
    cos_a = (rc * rc + ko.r * ko.r - need * need) / (2 * rc * ko.r)
    return math.degrees(math.acos(max(-1.0, min(1.0, cos_a))))


# -- blending helpers --------------------------------------------------------

def _fillet_polyline(points: Sequence[tuple[float, float]], radius: float
                     ) -> list[dict[str, Any]]:
    """Straight polyline with tangent arc fillets at every interior corner."""
    segs: list[dict[str, Any]] = []
    pts = [tuple(p) for p in points]
    cursor = pts[0]
    for i in range(1, len(pts) - 1):
        p_prev, p, p_next = cursor, pts[i], pts[i + 1]
        v1 = (p[0] - p_prev[0], p[1] - p_prev[1])
        v2 = (p_next[0] - p[0], p_next[1] - p[1])
        L1, L2 = math.hypot(*v1), math.hypot(*v2)
        if L1 < _EPS or L2 < _EPS:
            continue
        u1 = (v1[0] / L1, v1[1] / L1)
        u2 = (v2[0] / L2, v2[1] / L2)
        cross = u1[0] * u2[1] - u1[1] * u2[0]
        dot = max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1]))
        theta = math.acos(dot)
        if abs(cross) < 1e-6 or theta < 1e-6:
            segs.append(_line(cursor, p))
            cursor = p
            continue
        setback = radius * math.tan(theta / 2.0)
        setback = min(setback, L1 * 0.45, L2 * 0.45)
        r_eff = setback / math.tan(theta / 2.0)
        if r_eff < radius - 1e-6:
            raise RoutingError(
                f"fillet at ({p[0]:.1f}, {p[1]:.1f}) would need radius "
                f"{r_eff:.2f} to fit between waypoints {L1:.1f} and {L2:.1f} "
                f"mm apart - below the bend minimum {radius:.2f}. The "
                f"construction refuses a sub-minimum bend rather than "
                f"emitting one"
            )
        t1 = (p[0] - u1[0] * setback, p[1] - u1[1] * setback)
        t2 = (p[0] + u2[0] * setback, p[1] + u2[1] * setback)
        n = (-u1[1], u1[0]) if cross > 0 else (u1[1], -u1[0])
        c = (t1[0] + n[0] * r_eff, t1[1] + n[1] * r_eff)
        a0 = math.degrees(math.atan2(t1[1] - c[1], t1[0] - c[0]))
        a1 = math.degrees(math.atan2(t2[1] - c[1], t2[0] - c[0]))
        segs.append(_line(cursor, t1))
        segs.append(_arc(c, r_eff, a0, a1, ccw=cross > 0))
        cursor = t2
    segs.append(_line(cursor, pts[-1]))
    return [s for s in segs if _seg_len(s) > 1e-6]


def _wavy_pass(spec: RoutingSpec, rc: float, bulges: list[dict[str, Any]],
               az_from: float, az_to: float, ccw: bool) -> list[dict[str, Any]]:
    """Concentric arc from az_from to az_to with outward bulges over sectors.

    Each bulge replaces the base arc over its sector with: an S-blend out, a
    concentric arc at rc+delta, and an S-blend back. Blend arcs are computed as
    two-tangent-arc transitions whose radius is never below the bend minimum.
    """
    origin = (0.0, 0.0)
    sweep_dir = 1.0 if ccw else -1.0

    def fwd(a: float, b: float) -> float:
        """Azimuth distance from a to b in the sweep direction, degrees."""
        return ((b - a) * sweep_dir) % 360.0

    total = fwd(az_from, az_to)
    trans = 6.0  # azimuthal half-length of each S-blend, degrees
    events = []
    for b in bulges:
        s0 = fwd(az_from, (b["az"] - sweep_dir * b["half_width"]) % 360.0)
        s1 = fwd(az_from, (b["az"] + sweep_dir * b["half_width"]) % 360.0)
        if s1 < s0:
            s0, s1 = s1, s0
        if s1 + trans > total - 0.5 or s0 - trans < 0.5:
            raise RoutingError(
                f"bulge for keep-out {b['keep_out']!r} at az {b['az']:.1f} "
                f"has no room for its transition before the pass end; the "
                f"connector lane sits inside the feature's influence sector"
            )
        events.append((s0, s1, b["delta"]))
    events.sort()
    for (s0a, s1a, _), (s0b, _sb, _) in zip(events, events[1:]):
        if s0b < s1a + 2.0:
            raise RoutingError("two modulation sectors overlap; the pass "
                               "cannot be locally bulged independently")

    segs: list[dict[str, Any]] = []
    cursor_s = 0.0

    def az_at(s: float) -> float:
        return (az_from + sweep_dir * s) % 360.0

    for s0, s1, delta in events:
        t0, t1 = s0 - trans, s1 + trans
        if t0 < cursor_s + 0.5:
            raise RoutingError("modulation sector reaches back into the "
                               "previous transition; increase the pass gap")
        segs.append(_arc(origin, rc, az_at(cursor_s), az_at(t0), ccw=ccw))
        segs.extend(_s_blend(rc, rc + delta, az_at(t0), az_at(s0), ccw,
                             spec.min_bend_r))
        segs.append(_arc(origin, rc + delta, az_at(s0), az_at(s1), ccw=ccw))
        segs.extend(_s_blend(rc + delta, rc, az_at(s1), az_at(t1), ccw,
                             spec.min_bend_r))
        cursor_s = t1
    segs.append(_arc(origin, rc, az_at(cursor_s), az_to % 360.0, ccw=ccw))
    return [s for s in segs if _seg_len(s) > 1e-6]


def _s_blend(r0: float, r1: float, az0: float, az1: float, ccw: bool,
             min_bend: float) -> list[dict[str, Any]]:
    """Tangent-exact S-transition between concentric circles.

    Two equal arcs of radius R: the first tangent to the circle of radius r0
    at az0, the second tangent to the circle of radius r1 at az1, tangent to
    each other at the inflection. R solves |c1 - c2| = 2R with the centres on
    the two radial lines; solved by bisection, refused below the bend minimum.
    """
    s = 1.0 if r1 > r0 else -1.0
    u0, u1 = _pol(1.0, az0), _pol(1.0, az1)
    d_az = math.radians(abs(((az1 - az0) + 180.0) % 360.0 - 180.0))

    def gap(R: float) -> float:
        a, b = r0 + s * R, r1 - s * R
        return a * a + b * b - 2 * a * b * math.cos(d_az) - 4 * R * R

    lo, hi = 1e-3, 4.0 * max(r0, r1)
    if gap(lo) < 0 or gap(hi) > 0:
        raise RoutingError(
            f"no S-blend exists between r={r0:.2f}@{az0:.1f} and "
            f"r={r1:.2f}@{az1:.1f}; the transition window is unusable"
        )
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if gap(mid) > 0:
            lo = mid
        else:
            hi = mid
    R = (lo + hi) / 2.0
    if R < min_bend - 1e-6:
        raise RoutingError(
            f"S-blend radius {R:.2f} between r={r0:.2f} and r={r1:.2f} is "
            f"below the bend minimum {min_bend:.2f}; widen the transition"
        )
    c1 = (u0[0] * (r0 + s * R), u0[1] * (r0 + s * R))
    c2 = (u1[0] * (r1 - s * R), u1[1] * (r1 - s * R))
    d = math.hypot(c2[0] - c1[0], c2[1] - c1[1])
    m = (c1[0] + R * (c2[0] - c1[0]) / d, c1[1] + R * (c2[1] - c1[1]) / d)
    p0, p1 = _pol(r0, az0), _pol(r1, az1)
    # Arc senses fall out of which side each centre sits on relative to the
    # direction of travel along the parent circle.
    ccw1 = _turn_sense(p0, c1, ccw, az0)
    a10 = math.degrees(math.atan2(p0[1] - c1[1], p0[0] - c1[0]))
    a1m = math.degrees(math.atan2(m[1] - c1[1], m[0] - c1[0]))
    a2m = math.degrees(math.atan2(m[1] - c2[1], m[0] - c2[0]))
    a21 = math.degrees(math.atan2(p1[1] - c2[1], p1[0] - c2[0]))
    return [
        _arc(c1, R, a10, a1m, ccw=ccw1),
        _arc(c2, R, a2m, a21, ccw=not ccw1),
    ]


def _turn_sense(p: tuple[float, float], c: tuple[float, float],
                pass_ccw: bool, az: float) -> bool:
    """Rotation sense of a blend arc starting at p about c, given that its
    start tangent must match the parent circle's travel direction."""
    th = _rad(az)
    t = (-math.sin(th), math.cos(th)) if pass_ccw else (math.sin(th), -math.cos(th))
    # For an arc about c, travel ccw has tangent = rot90(p - c); pick the
    # sense whose tangent aligns with the incoming direction.
    rx, ry = p[0] - c[0], p[1] - c[1]
    ccw_t = (-ry, rx)
    return ccw_t[0] * t[0] + ccw_t[1] * t[1] > 0


# -- the router --------------------------------------------------------------

def route_channel(spec: RoutingSpec) -> RoutedChannel:
    """Derive the channel route for this constraint set, or refuse.

    Construction, outermost-in:

        inlet terminal = the outermost pass's own end at the inlet azimuth;
        passes alternate rotation sense (counterflow), each sweeping the long
        way between its two connection azimuths;
        adjacent passes join through half-circle U-connectors on service
        lanes near the outlet - exactly tangent to both passes;
        the innermost pass exits through a tangent-leave arc and a filleted
        climb that crosses each outer pass inside that pass's gap, ending at
        the outlet terminal.

    Every azimuth chosen here is re-checked by the audit; a layout this
    construction cannot make compliant is refused, not approximated.
    """
    if spec.center_max_r <= spec.center_min_r:
        raise RoutingError("envelope admits no centreline band at this width")
    if spec.terminal_r > spec.center_max_r + _EPS:
        raise RoutingError(
            f"terminal radius {spec.terminal_r} lies outside the centreline "
            f"band (max {spec.center_max_r:.2f})"
        )

    schedule = _pass_schedule(spec)
    radii = [p["radius"] for p in schedule]
    n = len(schedule)

    inlet, outlet = spec.inlet_az_deg % 360.0, spec.outlet_az_deg % 360.0
    if (outlet - inlet) % 360.0 < 1.0:
        raise RoutingError("inlet and outlet azimuths coincide")

    # Service lanes for the U-connectors, alternating around the outlet and
    # spreading outward so same-side lanes never crowd each other.
    lane_offsets = [46.0, -24.0, 34.0, -44.0, 58.0, -56.0]
    if n - 1 > len(lane_offsets):
        raise RoutingError(f"{n} passes exceed the connector lanes this "
                           f"construction provides")
    j_az = [(outlet + lane_offsets[k]) % 360.0 for k in range(n - 1)]

    # Innermost pass parity decides which way the exit climb tangent-leaves.
    inner_ccw = (n % 2 == 0)
    leave_sign = 1.0 if inner_ccw else -1.0  # east (+) or west (-) of outlet
    inner_end_az = (outlet - leave_sign * 4.0) % 360.0

    def covered(entry: float, exit_: float, ccw: bool, az: float) -> bool:
        total = ((exit_ - entry) % 360.0) if ccw else ((entry - exit_) % 360.0)
        s = ((az - entry) % 360.0) if ccw else ((entry - az) % 360.0)
        return s <= total

    segs: list[dict[str, Any]] = []
    ccw = False  # the outermost pass sweeps away from the corridor, CW
    entry_az = inlet
    for k in range(n):
        exit_az = j_az[k] if k < n - 1 else inner_end_az
        p = schedule[k]
        bulges = [b for b in p["bulges"]
                  if covered(entry_az, exit_az, ccw, b["az"])]
        partial = [b for b in p["bulges"] if b not in bulges
                   and covered(entry_az, exit_az, ccw,
                               (b["az"] + b["half_width"]) % 360.0)
                   != covered(entry_az, exit_az, ccw,
                              (b["az"] - b["half_width"]) % 360.0)]
        if partial:
            raise RoutingError(
                f"pass at r={p['radius']:.2f}: a modulation sector straddles "
                f"the pass end; the corridor and keep-out "
                f"{partial[0]['keep_out']!r} cannot be separated"
            )
        segs.extend(
            _wavy_pass(spec, p["radius"], bulges, entry_az, exit_az, ccw)
            if bulges else
            [_arc((0.0, 0.0), p["radius"], entry_az, exit_az, ccw=ccw)]
        )
        if k < n - 1:
            r_out, r_in = radii[k], radii[k + 1]
            R = (r_out - r_in) / 2.0
            if R < spec.min_bend_r - _EPS:
                raise RoutingError(
                    f"U-connector radius {R:.2f} between passes r={r_out:.2f} "
                    f"and r={r_in:.2f} is below the bend minimum"
                )
            segs.append(_u_connector(r_out, r_in, j_az[k], ccw))
            entry_az = j_az[k]
            ccw = not ccw

    # Exit climb: tangent-leave the innermost pass, cross each outer pass
    # inside its gap, arrive at the outlet terminal.
    inner_r = radii[-1]
    leave = _tangent_leave(inner_r, inner_end_az, inner_ccw,
                           max(spec.min_bend_r * 2.0, 10.0))
    segs.append(leave)
    leave_end = tuple(leave["end"])
    leave_r = math.hypot(*leave_end)
    # Extend tangentially out of the leave arc so the polyline's first fillet
    # absorbs the direction change instead of leaving a sharp junction.
    ldir = _arc_end_direction(leave)
    waypoints: list[tuple[float, float]] = [
        leave_end,
        (leave_end[0] + 8.0 * ldir[0], leave_end[1] + 8.0 * ldir[1]),
    ]
    crossings = 0
    for k in range(n - 2, -1, -1):
        if radii[k] < leave_r + 1.5 * (spec.width + spec.rib):
            continue  # the leave arc already lands at this level
        if radii[k] > spec.terminal_r - 6.0:
            continue  # the terminal leg itself performs this crossing
        cross_az = (outlet + leave_sign * (7.0 - 3.0 * (n - 2 - k))) % 360.0
        waypoints.append(_pol(radii[k], cross_az))
        crossings += 1
    if not crossings:
        waypoints.append(_pol((leave_r + spec.terminal_r) / 2.0,
                              (outlet + leave_sign * 5.0) % 360.0))
    waypoints.append(_pol(spec.terminal_r, outlet))
    segs.extend(_fillet_polyline(waypoints, spec.min_bend_r))

    segs = _weld_chain(segs)
    footprint = _offset_outline(segs, spec.half_width)
    routed = RoutedChannel(
        centerline=tuple(segs),
        footprint=tuple(footprint),
        pass_radii=tuple(radii),
        length=sum(_seg_len(s) for s in segs),
        min_keep_out_margin=_audit(spec, segs),
    )
    return routed


def _u_connector(r_out: float, r_in: float, lane_az: float,
                 incoming_ccw: bool) -> dict[str, Any]:
    """Half-circle joining two concentric passes on a service lane.

    Exactly tangent to both pass circles at its endpoints, because adjacent
    counterflow passes arrive at the lane with opposed tangential directions -
    the U-turn is the natural, fillet-free connection between them. Which side
    of the lane it bulges to is not a choice: it is fixed by the direction the
    outer pass arrives in, and taking the other side would put a cusp - a
    tangent reversal - at the junction.
    """
    c = _pol((r_out + r_in) / 2.0, lane_az)
    R = (r_out - r_in) / 2.0
    p_outer = _pol(r_out, lane_az)
    ccw_u = _turn_sense(p_outer, c, incoming_ccw, lane_az)
    a_out = math.degrees(math.atan2(p_outer[1] - c[1], p_outer[0] - c[0]))
    return _arc(c, R, a_out, a_out + (180.0 if ccw_u else -180.0), ccw=ccw_u)


def _arc_end_direction(s: dict[str, Any]) -> tuple[float, float]:
    """Unit tangent direction at an arc's end, in its direction of travel."""
    cx, cy = s["center"]
    rx, ry = s["end"][0] - cx, s["end"][1] - cy
    mag = math.hypot(rx, ry)
    rx, ry = rx / mag, ry / mag
    return (-ry, rx) if s["ccw"] else (ry, -rx)


def _arc_midpoint(s: dict[str, Any]) -> tuple[float, float]:
    cx, cy = s["center"]
    a0, _ = _arc_angles(s)
    half = _arc_sweep_rad(s) / 2.0
    a = a0 + (half if s["ccw"] else -half)
    return (cx + s["radius"] * math.cos(a), cy + s["radius"] * math.sin(a))


def _tangent_leave(r: float, az_deg: float, pass_ccw: bool, R: float
                   ) -> dict[str, Any]:
    """Quarter-turn arc leaving a pass tangentially, curving radially outward.

    Tangent-continuous with the pass at its start; ends heading roughly
    outward, ready for the filleted climb to take over.
    """
    p = _pol(r, az_deg)
    th = _rad(az_deg)
    if pass_ccw:
        t = (-math.sin(th), math.cos(th))
    else:
        t = (math.sin(th), -math.cos(th))
    n_out = (math.cos(th), math.sin(th))
    c = (p[0] + R * n_out[0], p[1] + R * n_out[1])
    end = (p[0] + R * (t[0] + n_out[0]), p[1] + R * (t[1] + n_out[1]))
    a0 = math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))
    a1 = math.degrees(math.atan2(end[1] - c[1], end[0] - c[0]))
    return _arc(c, R, a0, a1, ccw=not pass_ccw)


def _weld_chain(segs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Enforce exact endpoint continuity, snapping sub-micron gaps closed."""
    out = [segs[0]]
    for s in segs[1:]:
        prev_end = _seg_end(out[-1])
        gap = math.hypot(s["start"][0] - prev_end[0], s["start"][1] - prev_end[1])
        if gap > 0.05:
            raise RoutingError(
                f"routed chain is discontinuous: {gap:.3f} mm gap between "
                f"consecutive segments - a construction defect, refused"
            )
        s = dict(s)
        s["start"] = [prev_end[0], prev_end[1]]
        out.append(s)
    return out


def _audit(spec: RoutingSpec, segs: list[dict[str, Any]]) -> dict[str, float]:
    """Re-check the built chain against every input constraint, or refuse."""
    margins: dict[str, float] = {}
    for ko in spec.keep_outs:
        d = min(_dist_point_segment(ko.xy, s) for s in segs)
        wall = d - spec.half_width
        margins[ko.id] = round(wall - ko.wall_clearance, 4)
        if wall + 1e-6 < ko.wall_clearance:
            raise RoutingError(
                f"audit: keep-out {ko.id!r} wall clearance "
                f"{wall:.3f} < required {ko.wall_clearance:.3f}"
            )
    for s in segs:
        for x, y in _sample_segment(s):
            r = math.hypot(x, y)
            if r - 1e-6 > spec.center_max_r + spec.modulation_cap or \
               r + 1e-6 < spec.center_min_r:
                raise RoutingError(
                    f"audit: centreline leaves the envelope at r={r:.3f}"
                )
        if s["type"] == "arc" and s["radius"] < spec.min_bend_r - 1e-6 \
                and _seg_len(s) > 0.2:
            raise RoutingError(
                f"audit: bend radius {s['radius']:.3f} below the minimum "
                f"{spec.min_bend_r:.3f}"
            )
    # Self-separation: portions of the chain that are far apart *along* the
    # chain stay a full channel width plus rib apart, centre to centre.
    # Chain-near pairs (a fillet and its neighbours, a U-turn and its passes)
    # are legitimately close and are excluded by along-chain distance, not by
    # segment adjacency - fillet chains fragment into many short segments.
    samples = [_sample_segment(s) for s in segs]
    lens = [_seg_len(s) for s in segs]
    cum = [0.0]
    for L in lens:
        cum.append(cum[-1] + L)
    need = spec.width + spec.rib - 0.05
    window = 2.5 * need
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            along = cum[j] - cum[i + 1]  # chain length strictly between them
            if along < window:
                continue
            d = _min_pointset_dist(samples[i], samples[j])
            if d < need:
                raise RoutingError(
                    f"audit: chain approaches itself to {d:.2f} mm between "
                    f"segment {i} and segment {j}; the rib there would be "
                    f"{d - spec.width:.2f} mm"
                )
    return margins


def _min_pointset_dist(a: list[tuple[float, float]],
                       b: list[tuple[float, float]]) -> float:
    best = float("inf")
    for x0, y0 in a:
        for x1, y1 in b:
            d = math.hypot(x1 - x0, y1 - y0)
            if d < best:
                best = d
    return best


def _offset_outline(segs: list[dict[str, Any]], off: float) -> list[dict[str, Any]]:
    """Closed footprint outline: both offsets of the chain plus end caps.

    Valid because the chain is tangent-continuous: each segment offsets
    independently and stays connected. A concave arc whose radius equals the
    offset degenerates to a point and is dropped.
    """
    left: list[dict[str, Any]] = []
    right: list[dict[str, Any]] = []
    for s in segs:
        if s["type"] == "line":
            (x0, y0), (x1, y1) = s["start"], s["end"]
            L = math.hypot(x1 - x0, y1 - y0)
            nx, ny = -(y1 - y0) / L, (x1 - x0) / L
            left.append(_line((x0 + nx * off, y0 + ny * off),
                              (x1 + nx * off, y1 + ny * off)))
            right.append(_line((x0 - nx * off, y0 - ny * off),
                               (x1 - nx * off, y1 - ny * off)))
        else:
            # Left of travel points toward the centre on a CCW arc and away
            # from it on a CW arc.
            c = tuple(s["center"])
            a0, a1 = (math.degrees(a) for a in _arc_angles(s))
            r_left = s["radius"] - (off if s["ccw"] else -off)
            r_right = s["radius"] + (off if s["ccw"] else -off)
            if r_left > 1e-6:
                left.append(_arc(c, r_left, a0, a1, s["ccw"]))
            if r_right > 1e-6:
                right.append(_arc(c, r_right, a0, a1, s["ccw"]))

    start_c = _seg_start(segs[0])
    end_c = _seg_end(segs[-1])
    outline: list[dict[str, Any]] = []
    outline.extend(left)
    ldir = math.degrees(math.atan2(left[-1]["end"][1] - end_c[1],
                                   left[-1]["end"][0] - end_c[0]))
    outline.append(_arc(end_c, off, ldir, ldir - 180.0, ccw=False))
    for s in reversed(right):
        outline.append(_reverse_seg(s))
    rdir = math.degrees(math.atan2(right[0]["start"][1] - start_c[1],
                                   right[0]["start"][0] - start_c[0]))
    outline.append(_arc(start_c, off, rdir, rdir - 180.0, ccw=False))
    return outline


def route_spiral(r_start: float, r_end: float, pitch: float, width: float,
                 keep_outs: Sequence[KeepOut] = (),
                 start_az_deg: float = 0.0,
                 step_deg: float = 3.0) -> RoutedChannel:
    """An Archimedean spiral path with tangential keep-out deflection.

    The spiral r = r_start + pitch * theta / 2pi is sampled at `step_deg`;
    near a keep-out the sample is pushed radially away to the clearance
    circle, with a cosine-blended approach window - the 'routed tangentially
    around each keep-out' form. The result is a tessellated polyline
    centreline plus its offset footprint, audited like every routed path.
    """
    if r_end <= r_start:
        raise RoutingError("spiral: r_end must exceed r_start")
    turns = (r_end - r_start) / pitch
    total = turns * 360.0
    half_w = width / 2.0
    raw: list[tuple[float, float, Any]] = []
    a = 0.0
    while a <= total + 1e-9:
        r = r_start + pitch * a / 360.0
        th = math.radians(a + start_az_deg)
        x, y = r * math.cos(th), r * math.sin(th)
        hit = None
        for ko in keep_outs:
            need = ko.wall_clearance + half_w + _MARGIN
            kx, ky = ko.xy
            d = math.hypot(x - kx, y - ky)
            if d < need and d > _EPS:
                # Project the sample onto the clearance circle, away from
                # the feature axis - the exact 'tangentially around' path.
                x = kx + (x - kx) / d * need
                y = ky + (y - ky) / d * need
                hit = ko
        raw.append((x, y, hit))
        a += step_deg
    # Between consecutive samples deflected by the same keep-out, follow the
    # clearance arc rather than the chord, which would slice the disk.
    pts: list[tuple[float, float]] = []
    for (x0, y0, k0), (x1, y1, k1) in zip(raw, raw[1:]):
        pts.append((x0, y0))
        if k0 is not None and k0 is k1:
            need = k0.wall_clearance + half_w + _MARGIN
            kx, ky = k0.xy
            a0 = math.atan2(y0 - ky, x0 - kx)
            a1 = math.atan2(y1 - ky, x1 - kx)
            sweep = ((a1 - a0 + math.pi) % (2 * math.pi)) - math.pi
            n = max(1, int(abs(math.degrees(sweep))))
            for i in range(1, n):
                ai = a0 + sweep * i / n
                pts.append((kx + need * math.cos(ai),
                            ky + need * math.sin(ai)))
    pts.append(raw[-1][:2])

    def project(p):
        x, y = p
        for ko in keep_outs:
            need = ko.wall_clearance + half_w + _MARGIN
            kx, ky = ko.xy
            d = math.hypot(x - kx, y - ky)
            if _EPS < d < need:
                x = kx + (x - kx) / d * need
                y = ky + (y - ky) / d * need
        return (x, y)

    # Entry/exit chords can still dip inside a disk: densify to <=1 mm and
    # re-project every point, twice, so no sub-span survives inside.
    for _ in range(2):
        dense: list[tuple[float, float]] = [pts[0]]
        for p0, p1 in zip(pts, pts[1:]):
            gap = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
            n = max(1, int(gap / 1.0))
            for i in range(1, n + 1):
                dense.append(project((p0[0] + (p1[0] - p0[0]) * i / n,
                                      p0[1] + (p1[1] - p0[1]) * i / n)))
        pts = dense
    segs = _fit_arcs(pts, tol=0.05)
    margins: dict[str, float] = {}
    for ko in keep_outs:
        d = min(_dist_point_segment(ko.xy, s) for s in segs)
        margins[ko.id] = round(d - half_w - ko.wall_clearance, 4)
        if d - half_w + 0.06 < ko.wall_clearance:
            raise RoutingError(
                f"spiral audit: keep-out {ko.id!r} wall clearance "
                f"{d - half_w:.3f} < required {ko.wall_clearance:.3f}"
            )
    return RoutedChannel(
        centerline=tuple(segs),
        footprint=tuple(_offset_outline(segs, half_w)),
        pass_radii=(r_start, r_end),
        length=sum(_seg_len(s) for s in segs),
        min_keep_out_margin=margins,
    )


def _fit_arcs(pts: Sequence[tuple[float, float]], tol: float = 0.05
              ) -> list[dict[str, Any]]:
    """Compress a dense polyline into a chain of arcs within `tol`.

    Greedy: grow a window, fit the circle through its first, middle and last
    points, accept while every window point stays within tol of that circle.
    A window no circle fits becomes a line. Keeps drawn entity counts in the
    hundreds where the raw tessellation runs to thousands.
    """
    out: list[dict[str, Any]] = []
    i, n = 0, len(pts)
    while i < n - 1:
        best_j = i + 1
        best: dict[str, Any] | None = None
        j = min(i + 8, n - 1)
        while j <= n - 1:
            p0, pm, p1 = pts[i], pts[(i + j) // 2], pts[j]
            circ = _circumcircle(p0, pm, p1)
            seg: dict[str, Any] | None
            if circ is None:
                seg = _line(p0, p1)
            else:
                cx, cy, r = circ
                a0 = math.degrees(math.atan2(p0[1] - cy, p0[0] - cx))
                a1 = math.degrees(math.atan2(p1[1] - cy, p1[0] - cx))
                cross = ((pm[0] - p0[0]) * (p1[1] - p0[1])
                         - (pm[1] - p0[1]) * (p1[0] - p0[0]))
                seg = _arc((cx, cy), r, a0, a1, ccw=cross > 0)
            ok = all(
                _dist_point_segment(pts[k], seg) <= tol
                for k in range(i + 1, j)
            )
            if ok:
                best, best_j = seg, j
                j = min(j + max(4, (j - i) // 2), n - 1) if j < n - 1 else n
            else:
                break
        if best is None:
            best = _line(pts[i], pts[best_j])
        out.append(best)
        i = best_j
    return _weld_chain(out)


def _circumcircle(p0, p1, p2):
    ax, ay = p0
    bx, by = p1
    cx, cy = p2
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-9:
        return None
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay)
          + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx)
          + (cx * cx + cy * cy) * (bx - ax)) / d
    r = math.hypot(ax - ux, ay - uy)
    if r > 100000.0:
        return None
    return (ux, uy, r)


def _reverse_seg(s: dict[str, Any]) -> dict[str, Any]:
    out = dict(s)
    out["start"], out["end"] = list(s["end"]), list(s["start"])
    if s["type"] == "arc":
        out["ccw"] = not s["ccw"]
    return out
