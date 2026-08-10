"""Planar pairwise clearance over the spec/00 section 3.2 clocking map."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path

ICD = "spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md"

# Footprint half-extents, each traced to the artifact that states it. `radial` and
# `tangential` are half-extents in mm from the feature axis; the effective
# footprint radius is their vector sum, which is exact for a circle and
# conservative for a radial slot. `wall` is the minimum material this feature
# demands between itself and a neighbour ON THE SAME FACE.
#
# NOTE: this is NOT spec/01 section 3.1's "min wall to channel". That column
# governs separation from the coolant circuit, which is an internal feature and
# is not in this planar map at all. An early version of this check used those
# values as feature-to-feature ligaments and reported a false interference
# between the RF land and an M6 ring tapping. The default here is 1.5 mm of
# machined ligament, raised only where a specific artifact demands more.
FOOTPRINTS: dict[str, dict[str, object]] = {
    # The choke fastener has DIFFERENT footprints on the two faces: the O22
    # washer pad is top-face only, the CP-D26 counterbore bottom-face only.
    # Collapsing them into one disc was the first version of this check and it
    # produced three false failures.
    "Thermal-choke fasteners (inner)": {
        "face": "both", "radial": 6.25, "tangential": 5.5, "wall": 1.5,
        "top_radial": 11.0, "top_tangential": 11.0,
        "cite": "spec/01 CP-D26 11.0 W x 12.5 L bottom; CP-D17 O22 pad top",
    },
    "Thermal-choke fasteners (outer)": {
        "face": "both", "radial": 6.25, "tangential": 5.5, "wall": 1.5,
        "top_radial": 11.0, "top_tangential": 11.0,
        "cite": "spec/01 CP-D26 11.0 W x 12.5 L bottom; CP-D17 O22 pad top",
    },
    "Kinematic locators (Cooling Plate<->Heater Plate)": {
        "face": "top", "radial": 5.0, "tangential": 5.0, "wall": 1.5,
        "cite": "spec/01 CP-D10 O10.000 counterbore (ECR-D-007 action 3)",
    },
    "Kinematic radial slots (Ring<->Cooling Plate)": {
        "face": "bottom", "radial": 5.0, "tangential": 5.0, "wall": 1.5,
        "cite": "spec/01 CP-D09 O10.000 counterbore (ECR-D-007 action 3)",
    },
    "RF strap land (Cooling Plate)": {
        # spec/01 section 3.1 declares the KEEP-OUT envelope as r 128-146,
        # 93-117 deg. That envelope governs CAD, so it is what is checked -
        # not the nominal 60 mm arc, which subtends 24.5 deg and disagrees with
        # the declared 24 deg by 0.55 deg (recorded as ECR-Q-010).
        "face": "bottom", "radial": 9.0, "tangential": 30.0, "wall": 1.5,
        "half_angle": 12.0,
        "cite": "spec/01 section 3.1 RF land envelope r 128-146, 93-117 deg",
    },
    "RTD blind ports (Cooling Plate)": {
        "face": "bottom", "radial": 9.9, "tangential": 9.9, "wall": 1.5,
        "cite": "spec/01 CP-IF-9, port plus retainer taps at +/-9 mm",
    },
    "Lift pin bores": {
        "face": "both", "radial": 6.0, "tangential": 6.0, "wall": 1.5,
        "cite": "spec/01 CP-IF-6 O12 bushing counterbore",
    },
    "Support Ring fasteners (two independent circuits, DR-9)": {
        "face": "bottom", "radial": 3.0, "tangential": 3.0, "wall": 1.5,
        "cite": "spec/01 CP-IF-2 M6 x 1.0 tapped, thread major O6.0, no counterbore",
    },
    "ESC HV electrode feed contacts": {
        "face": "both", "radial": 4.0, "tangential": 4.0, "wall": 1.5,
        "cite": "spec/01 CP-IF-7 O8.0 bore",
    },
    "Coolant inlet / outlet": {
        "face": "internal", "radial": 7.0, "tangential": 7.0, "wall": 1.5,
        "cite": "spec/01 CP-D24 O14.0 weld-prep counterbore",
    },
    "He / vacuum central port": {
        "face": "both", "radial": 16.0, "tangential": 16.0, "wall": 1.5,
        "cite": "spec/01 CP-IF-5 O32 sealing annulus",
    },
}

_ROW = re.compile(r"^\|\s*(?:\*\*)?([^|*]+?)(?:\*\*)?\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")
_BC = re.compile(r"Ø\s*([0-9.]+)\s*BC")
_ANGLE = re.compile(r"([0-9.]+)\s*°")
_NPLUS = re.compile(r"([0-9.]+)\s*°?\s*\+\s*n·\s*([0-9.]+)\s*°")


@dataclass
class Feature:
    name: str
    radius: float
    angles: list[float]
    face: str
    radial: float
    tangential: float
    wall: float
    cite: str
    half_angle: float | None = None

    def extent(self, face: str) -> tuple[float, float]:
        """(radial half-extent, tangential half-extent) on the given face."""
        return (self.radial, self.tangential)

    def r_span(self) -> tuple[float, float]:
        return (self.radius - self.radial, self.radius + self.radial)

    def theta_half(self) -> float:
        """Angular half-extent in degrees."""
        if self.half_angle is not None:
            return self.half_angle
        ratio = min(1.0, self.tangential / self.radius) if self.radius else 1.0
        return math.degrees(math.asin(ratio))


def _angular_gap(a_centre: float, a_half: float, b_centre: float, b_half: float) -> float:
    """Smallest angular separation between two sectors, in degrees. 0 if they overlap."""
    delta = abs((a_centre - b_centre + 180.0) % 360.0 - 180.0)
    return max(0.0, delta - a_half - b_half)


@dataclass
class Finding:
    a: str
    b: str
    angle_a: float
    angle_b: float
    distance: float
    required: float

    @property
    def shortfall(self) -> float:
        return self.required - self.distance


@dataclass
class Report:
    features: list[Feature] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.findings


def _angles(cell: str) -> list[float]:
    span = _NPLUS.search(cell)
    if span:
        start, step = float(span.group(1)), float(span.group(2))
        if step <= 0:
            return []
        return [(start + i * step) % 360.0 for i in range(int(round(360.0 / step)))]
    return [float(m.group(1)) % 360.0 for m in _ANGLE.finditer(cell)]


def load_map(repo: Path) -> tuple[list[Feature], list[str]]:
    """Parse the section 3.2 clocking table. The frozen spec is the input."""
    text = (repo / ICD).read_text(encoding="utf-8")
    block = re.search(r"### 3\.2 Feature Clocking Map(.*?)^### ", text, re.S | re.M)
    if not block:
        return [], ["spec/00 section 3.2 not found"]
    features: list[Feature] = []
    skipped: list[str] = []
    for line in block.group(1).splitlines():
        m = _ROW.match(line.strip())
        if not m:
            continue
        name, circle, angle_cell, _qty = (g.strip() for g in m.groups())
        if name.lower() in ("feature",) or set(name) <= set("-: "):
            continue
        name = name.replace("↔", "<->").replace("Ø", "O")
        key = next((k for k in FOOTPRINTS if k.lower() == name.lower()), None)
        bc = _BC.search(circle.replace("O", "Ø"))
        angles = _angles(angle_cell)
        if key is None:
            skipped.append(f"{name}: no declared footprint - not checked")
            continue
        if not bc or not angles:
            skipped.append(f"{name}: no bolt circle or no angles - not checked")
            continue
        fp = FOOTPRINTS[key]
        features.append(
            Feature(
                name=name, radius=float(bc.group(1)) / 2.0, angles=angles,
                face=str(fp["face"]), radial=float(fp["radial"]),  # type: ignore[arg-type]
                tangential=float(fp["tangential"]), wall=float(fp["wall"]),  # type: ignore[arg-type]
                cite=str(fp["cite"]),
                half_angle=(float(fp["half_angle"]) if "half_angle" in fp else None),  # type: ignore[arg-type]
            )
        )
    return features, skipped


def _shares_face(a: Feature, b: Feature) -> bool:
    if "both" in (a.face, b.face):
        return not (a.face == "internal" or b.face == "internal")
    return a.face == b.face


def check(repo: Path) -> Report:
    """Two features interfere when their radial bands and their angular sectors
    BOTH come within the declared minimum wall. Separation in either dimension
    alone is sufficient clearance - which is why the earlier centre-distance
    test over-reported on radially separated features."""
    features, skipped = load_map(repo)
    report = Report(features=features, skipped=skipped)
    for i, a in enumerate(features):
        for b in features[i + 1:]:
            if not _shares_face(a, b):
                continue
            wall = max(a.wall, b.wall)
            a_lo, a_hi = a.r_span()
            b_lo, b_hi = b.r_span()
            radial_gap = max(b_lo - a_hi, a_lo - b_hi, 0.0)
            if radial_gap >= wall:
                continue
            mean_r = (a.radius + b.radius) / 2.0
            worst: Finding | None = None
            for ang_a in a.angles:
                for ang_b in b.angles:
                    gap_deg = _angular_gap(ang_a, a.theta_half(), ang_b, b.theta_half())
                    gap_mm = math.radians(gap_deg) * mean_r
                    clearance = max(radial_gap, gap_mm)
                    if clearance >= wall:
                        continue
                    if worst is None or clearance < worst.distance:
                        worst = Finding(a.name, b.name, ang_a, ang_b, clearance, wall)
            if worst is not None:
                report.findings.append(worst)
    report.findings.sort(key=lambda f: -f.shortfall)
    return report
