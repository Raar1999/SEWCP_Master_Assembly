"""`SR-02` / `SR-03` / `SR-04` — the Support Ring isolation joint, computed.

`SR-03` and `SR-04` are declared **Drawing verification** and `OI-C-15` records
that no path trace has ever been filed. This module files it, and the trace
does not close.

**The whole finding turns on one omission.** `spec/03` §2.1 computes the
flange-to-flange stray capacitance across *"the 14 mm vacuum gap"*, and §3.1
computes the `SR-04` clearance as *"the open annular gap between the clamp ring
and the Cooling Plate = 14 mm"*. Both take the gap to be empty. §5.2 puts
`SEWCP-401`, a **6.00 mm** grounded metal ring (`CR-D03`), inside it — seated
0.50 mm into the `SR-IF-2` register, so **5.50 mm of the 14.00 mm gap is
grounded metal**.

Everything below follows from that one number, and none of it needs a fastener
dimension, a handbook value or an assumption:

  * the greatest clearance the joint can ever offer is 14.00 - 5.50 = **8.50 mm**
    against `SR-04`'s 12 mm, taking the RF-hot boundary at the most favourable
    position it could possibly occupy - flush with the ceramic;
  * the parallel-plate gap in the `SR-02` stray term is 8.50 mm, not 14.00, which
    raises stray capacitance and drops shunt impedance below the 400 ohm floor;
  * the creepage path is the exposed ceramic between the two conductor edges, and
    with `SEWCP-401` at dia 318.0/286.0 and the mandated dia-16 washers at Ø302 BC
    both spanning the full 318/286 flange annulus, the only exposed ceramic
    left is the web itself.

The fastener stack is then applied on top, as a **threshold** rather than a
value: the protrusion at which the joint stops assembling at all is published,
so the reader can substitute their own hardware and see where it lands.

There is also a hard radial collision, independent of every number above:
`SEWCP-401` at dia 318.0/286.0 seats on the bottom-flange top face, and the web
at dia 300.0/294.0 rises from that same face.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# ── Frozen dimensions. Every one is cited at its constant. ──────────────────
WEB_GAP_MM = 14.00          # spec/03 SR-D08 web height = the flange-to-flange gap
FLANGE_OD_MM = 318.0        # SR-D09
FLANGE_ID_MM = 286.0        # SR-D10
FLANGE_T_MM = 3.00          # SR-D11
WEB_OD_MM = 300.0           # SR-D05
WEB_ID_MM = 294.0           # SR-D06
WEB_FILLET_R_MM = 3.00      # SR-D12, "Critical - ceramic stress riser"
BOLT_BC_MM = 302.0          # SR-D14, pinned by the frozen Base Plate at FBA-3
BOLT_HOLE_D_MM = 7.0        # SR-D13
REGISTER_DEPTH_MM = 0.50    # SR-IF-2 / SR-D16
CLAMP_RING_T_MM = 6.00      # CR-D03
CLAMP_RING_OD_MM = 318.0    # CR-D01
CLAMP_RING_ID_MM = 286.0    # CR-D02
WASHER_OD_MM = 16.0         # spec/00 §9, both circuits, "dia-16 flat"

# ── Requirements ────────────────────────────────────────────────────────────
SR02_MIN_OHM = 400.0        # spec/03 SR-02, at 13.56 MHz
SR03_MIN_CREEPAGE_MM = 20.0
SR04_MIN_CLEARANCE_MM = 12.0
RF09_VACUUM_CLEARANCE_MM = 8.0   # spec/08 RF-09, the vacuum-side value, with DR-11

# ── Electrical constants ────────────────────────────────────────────────────
EPS0 = 8.854e-12            # F/m, quoted at spec/03 §2.1
EPS_R_AL2O3 = 9.8           # spec/03 §2.1
F_RF_HZ = 13.56e6           # spec/00, spec/03 SR-02

#: ISO 4762 nominal head height for M6. Used ONLY to locate the assembly
#: threshold, never in the SR-02/SR-03/SR-04 verdicts, each of which is reached
#: without it. The threshold is published alongside so the verdict does not
#: depend on this number being right.
M6_SOCKET_HEAD_HEIGHT_MM = 6.00


@dataclass(frozen=True)
class Verdict:
    requirement: str
    quantity: str
    value: float
    limit: float
    unit: str
    sense: str          # ">=" - the value must be at least the limit
    basis: str

    @property
    def passes(self) -> bool:
        return self.value >= self.limit

    @property
    def shortfall(self) -> float:
        return max(0.0, self.limit - self.value)


def grounded_intrusion_mm() -> float:
    """How much of the flange gap SEWCP-401 occupies. The load-bearing number."""
    return CLAMP_RING_T_MM - REGISTER_DEPTH_MM


def best_case_clearance_mm() -> float:
    """The largest clearance the joint could offer under any hardware choice.

    The RF-hot boundary is placed flush with the ceramic top flange - a
    position no bolted joint can actually achieve, since something must bear on
    the ceramic. Everything real is worse than this.
    """
    return WEB_GAP_MM - grounded_intrusion_mm()


def creepage_mm(*, with_fillets: bool) -> float:
    """Exposed-ceramic path from the RF-hot conductor edge to the grounded one.

    Both conductors span the full 318/286 flange annulus - `SEWCP-401` by
    `CR-D01`/`CR-D02`, and the RF-hot side because a dia-16 washer centred on the
    302 bolt circle reaches r = 143.0 to r = 159.0, which is the annulus
    exactly. So no radial run over either flange face is available, and the
    path is the web alone.
    """
    if not with_fillets:
        return WEB_GAP_MM
    # With SR-D12's R3.0 fillets the path leaves the flange face on a quarter
    # arc at each end: two quarter arcs plus the straight remainder.
    straight = WEB_GAP_MM - 2 * WEB_FILLET_R_MM
    arc = (math.pi / 2) * WEB_FILLET_R_MM
    return straight + 2 * arc


def shunt_impedance_ohm(gap_m: float) -> tuple[float, float, float]:
    """(C_web, C_stray, X_C) for a given flange-to-flange conductor gap."""
    web_area = math.pi * (WEB_OD_MM + WEB_ID_MM) / 2 * (WEB_OD_MM - WEB_ID_MM) / 2 / 1e6
    flange_area = math.pi / 4 * (FLANGE_OD_MM ** 2 - FLANGE_ID_MM ** 2) / 1e6
    c_web = EPS0 * EPS_R_AL2O3 * web_area / (WEB_GAP_MM / 1000.0)
    c_stray = EPS0 * flange_area / gap_m
    x_c = 1.0 / (2 * math.pi * F_RF_HZ * (c_web + c_stray))
    return c_web, c_stray, x_c


def radial_overlap_mm() -> float:
    """Interference between the SEWCP-401 footprint and the web root, radially."""
    ring = (CLAMP_RING_ID_MM / 2, CLAMP_RING_OD_MM / 2)
    web = (WEB_ID_MM / 2, WEB_OD_MM / 2)
    return max(0.0, min(ring[1], web[1]) - max(ring[0], web[0]))


def bolt_hole_under_web_mm() -> float:
    """How much of the 3.0 mm web wall stands over the Ø7.0 bolt-hole footprint."""
    lo, hi = BOLT_BC_MM / 2 - BOLT_HOLE_D_MM / 2, BOLT_BC_MM / 2 + BOLT_HOLE_D_MM / 2
    return max(0.0, min(hi, WEB_OD_MM / 2) - max(lo, WEB_ID_MM / 2))


def flange_radial_demand_mm() -> tuple[float, float]:
    """(available flange width, width the frozen features demand of it).

    The demand is the bolt hole, the web wall and one R3.0 fillet on each side
    of the web - the features that must coexist on one flange face.
    """
    available = (FLANGE_OD_MM - FLANGE_ID_MM) / 2
    demand = BOLT_HOLE_D_MM + (WEB_OD_MM - WEB_ID_MM) / 2 + 2 * WEB_FILLET_R_MM
    return available, demand


def assembly_threshold_mm() -> float:
    """RF-hot protrusion below the top flange at which the joint interferes."""
    return best_case_clearance_mm()


def verdicts() -> list[Verdict]:
    clearance = best_case_clearance_mm()
    creep_modelled = creepage_mm(with_fillets=False)
    creep_with_fillets = creepage_mm(with_fillets=True)
    _, _, x_c = shunt_impedance_ohm(clearance / 1000.0)
    return [
        Verdict("SR-04", "Clearance, RF-hot to grounded hardware",
                clearance, SR04_MIN_CLEARANCE_MM, "mm", ">=",
                "gap 14.00 less SEWCP-401's 5.50 intrusion; RF-hot boundary "
                "placed flush with the ceramic, the most favourable position possible"),
        Verdict("SR-04", "Clearance against the vacuum-side value (spec/08 RF-09 precedent)",
                clearance, RF09_VACUUM_CLEARANCE_MM, "mm", ">=",
                "the same quantity against 8 mm, the value spec/08 sets for a "
                "vacuum-side clearance with DR-11 in force"),
        Verdict("SR-03", "Creepage, RF-hot to grounded hardware (as modelled, no fillets)",
                creep_modelled, SR03_MIN_CREEPAGE_MM, "mm", ">=",
                "both conductors span the full flange annulus, so the web is the "
                "whole exposed path; SR-D12's fillets are absent from the model"),
        Verdict("SR-03", "Creepage with SR-D12's R3.0 fillets present",
                creep_with_fillets, SR03_MIN_CREEPAGE_MM, "mm", ">=",
                "straight remainder plus two quarter arcs - the best the "
                "cross-section can produce"),
        Verdict("SR-02", "Shunt impedance to ground at 13.56 MHz",
                x_c, SR02_MIN_OHM, "ohm", ">=",
                "stray term recomputed across the 8.50 mm conductor gap that "
                "SEWCP-401 leaves, not the 14.00 mm spec/03 s2.1 assumes"),
    ]
