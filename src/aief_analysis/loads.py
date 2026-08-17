"""`SR-07` and `AP-08` re-run at the as-modelled stack mass.

Both requirements are declared `Analysis`, and both analyses of record were run
at the design-basis **7.5 kg** while the assembly models to **7.69973 kg**
(`cad/runs/ASSEMBLY_S-2026-08-11-05/run.json`, 19 occurrences, verdict PASS).
`OI-C-15` records the gap. This module closes it by recomputing rather than
scaling, and by publishing the mass at which each case would actually reach the
declared safety factor - which is the number that says whether 2.66 % matters.

Every capability and every area below is quoted from the frozen specification
and cited at the constant. Nothing here is a handbook value this module
supplied on its own account.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

#: spec/06 AP-08 states "5 g on the 7.5 kg stack = 123 N per pin". With three
#: pins that is 7.5 * g * 5 / 3 = 123, which fixes g at 9.81 and not 9.80665.
#: Derived from the specification's own arithmetic, not chosen.
G = 9.81

DESIGN_BASIS_MASS_KG = 7.5     # spec/03 SR-07, spec/06 AP-08
LATERAL_G = 5.0                # spec/03 SR-07 "5 g in all axes"
SAFETY_FACTOR = 3.0            # spec/03 SR-07 "SF >= 3"

N_PINS_PER_INTERFACE = 3       # spec/06 AP-01 "3 per interface, at 120 deg"

PIN_SHEAR_AREA_MM2 = 28.274    # spec/06 s2.3 "pi/4 * 6^2 = 28.3 mm2"
PIN_BEARING_AREA_MM2 = 15.0    # spec/06 s2.3 "6.0 * 2.5"

TI_SHEAR_MPA = 550.0           # spec/06 s2.3 "Ti-6Al-4V, 550 MPa shear"
AL2O3_BEARING_MPA = 2500.0     # spec/06 s2.3 / spec/03 s2.2
AL6061_BEARING_MPA = 276.0     # spec/06 s2.3 "6061 276 MPa"

#: spec/03 s2.2, at the 7.5 kg design basis. Both scale linearly with mass:
#: the first is stack dead weight, the second the moment it makes at 5 g.
RING_WEB_COMPRESSIVE_MPA_AT_BASIS = 0.026
RING_WEB_FLEXURAL_MPA_AT_BASIS = 0.079
AL2O3_COMPRESSIVE_MPA = 2500.0   # spec/03 s2.2
AL2O3_FLEXURAL_MPA = 350.0       # spec/03 s2.2

ASSEMBLY_RECORD = Path("cad/runs/ASSEMBLY_S-2026-08-11-05/run.json")


@dataclass(frozen=True)
class Case:
    requirement: str
    name: str
    stress_mpa: float
    capability_mpa: float
    governing: bool = False

    @property
    def margin(self) -> float:
        return self.capability_mpa / self.stress_mpa

    @property
    def passes(self) -> bool:
        return self.margin >= SAFETY_FACTOR

    def mass_at_safety_factor(self, mass_kg: float) -> float:
        """The stack mass at which this case reaches SF = 3.

        Every case here is linear in mass, so the limiting mass is the current
        mass scaled by the current margin over the required one. This is the
        figure that decides whether a 2.66 % mass error is worth an argument.
        """
        return mass_kg * self.margin / SAFETY_FACTOR


@dataclass
class Report:
    mass_kg: float
    basis_mass_kg: float
    per_pin_load_n: float
    stack_weight_n: float
    cases: list[Case]

    @property
    def mass_error_pct(self) -> float:
        return 100.0 * (self.mass_kg - self.basis_mass_kg) / self.basis_mass_kg

    @property
    def governing(self) -> Case:
        return min(self.cases, key=lambda c: c.margin)

    @property
    def ok(self) -> bool:
        return all(c.passes for c in self.cases)


def observed_assembly_mass(repo: Path) -> float:
    """The as-modelled mass, read from the observed record - never transcribed."""
    d = json.loads((repo / ASSEMBLY_RECORD).read_text(encoding="utf-8"))
    occ = d["observed_assembly"]["occurrences"]
    total = sum(float(o["mass_kg"]) for o in occ)
    declared = float(d["total_mass_kg"])
    if abs(total - declared) > 5e-4:
        raise ValueError(
            f"assembly record disagrees with itself: occurrences sum to {total:.5f} kg, "
            f"total_mass_kg declares {declared:.5f} kg"
        )
    return total


def analyse(mass_kg: float) -> Report:
    """SR-07 and AP-08 at an arbitrary stack mass."""
    stack_weight_n = mass_kg * G
    lateral_n = stack_weight_n * LATERAL_G
    per_pin_n = lateral_n / N_PINS_PER_INTERFACE
    scale = mass_kg / DESIGN_BASIS_MASS_KG

    cases = [
        Case("SR-07", "Support ring web, stack dead weight (compression)",
             RING_WEB_COMPRESSIVE_MPA_AT_BASIS * scale, AL2O3_COMPRESSIVE_MPA),
        Case("SR-07", "Support ring web, 5 g lateral moment at web root (flexure)",
             RING_WEB_FLEXURAL_MPA_AT_BASIS * scale, AL2O3_FLEXURAL_MPA),
        Case("AP-08", "Alignment pin, 5 g lateral shear (Ti-6Al-4V)",
             per_pin_n / PIN_SHEAR_AREA_MM2, TI_SHEAR_MPA),
        Case("AP-08", "Alignment pin, bearing on slot wall (Al2O3, ring interface)",
             per_pin_n / PIN_BEARING_AREA_MM2, AL2O3_BEARING_MPA),
        Case("AP-08", "Alignment pin, bearing on slot wall (6061, heater interface)",
             per_pin_n / PIN_BEARING_AREA_MM2, AL6061_BEARING_MPA),
    ]
    return Report(mass_kg, DESIGN_BASIS_MASS_KG, per_pin_n, stack_weight_n, cases)


def check(repo: Path) -> tuple[Report, Report]:
    """(analysis of record at 7.5 kg, re-run at the as-modelled mass)."""
    return analyse(DESIGN_BASIS_MASS_KG), analyse(observed_assembly_mass(repo))
