"""Tests for the two `OI-C-15` desk analyses.

The load-bearing test in this module is `test_the_model_reproduces_spec_03_s2_1`.
Everything the insulation trace concludes rests on one substitution - 8.50 mm of
conductor gap where `spec/03` §2.1 assumed 14.00 - so the only way the finding
can be wrong is if the electrical model itself is wrong. That test feeds the
model the specification's own input and requires it to return the
specification's own published answer, to the digit it published. If the control
passes and the substitution fails, the divergence is in the input, which is
exactly the claim.

The rest hold the arithmetic against mutation, and pin the two dispositions:
`SR-07`/`AP-08` discharge, `SR-02`/`SR-03`/`SR-04` do not.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aief_analysis import insulation as ins  # noqa: E402
from aief_analysis.loads import (  # noqa: E402
    DESIGN_BASIS_MASS_KG,
    SAFETY_FACTOR,
    analyse,
    check,
    observed_assembly_mass,
)

REPO = Path(__file__).resolve().parent.parent


# ── OI-C-15 (i) — SR-07 / AP-08 ────────────────────────────────────────────

def test_the_model_reproduces_ap_08s_own_stated_load() -> None:
    """Control: at the design basis the model must return spec/06 AP-08's 123 N."""
    assert analyse(DESIGN_BASIS_MASS_KG).per_pin_load_n == pytest.approx(122.62, abs=0.01)


def test_the_model_reproduces_spec_03_s2_2_margins() -> None:
    """Control: the ring cases must return spec/03 §2.2's published margins."""
    cases = {c.name: c for c in analyse(DESIGN_BASIS_MASS_KG).cases}
    compressive = cases["Support ring web, stack dead weight (compression)"]
    flexural = cases["Support ring web, 5 g lateral moment at web root (flexure)"]
    assert compressive.margin == pytest.approx(96_154, rel=0.01)   # spec says "~96,000x"
    assert flexural.margin == pytest.approx(4_430, rel=0.01)       # spec says "~4,400x"


def test_the_observed_mass_comes_from_the_record_and_is_self_consistent() -> None:
    assert observed_assembly_mass(REPO) == pytest.approx(7.69973, abs=1e-5)


def test_sr07_and_ap08_discharge_at_the_as_modelled_mass() -> None:
    _, actual = check(REPO)
    assert actual.mass_error_pct == pytest.approx(2.66, abs=0.01)
    assert actual.ok, [c.name for c in actual.cases if not c.passes]
    assert actual.governing.margin == pytest.approx(32.9, rel=0.01)


def test_the_conclusion_survives_an_order_of_magnitude_of_unmodelled_mass() -> None:
    """The point of the analysis: the 2.66 % error cannot matter, and neither
    can the unmodelled spec-only BOM lines, because the governing case does not
    reach SF=3 until 84 kg."""
    gov = analyse(7.69973).governing
    assert gov.mass_at_safety_factor(7.69973) == pytest.approx(84.4, rel=0.01)
    assert analyse(7.69973 * 10).ok, "a tenfold mass would still pass"


def test_the_analysis_does_fail_when_it_should() -> None:
    """Adversarial: an absurd mass must break it, or the check checks nothing."""
    assert not analyse(200.0).ok


# ── OI-C-15 (ii) — SR-02 / SR-03 / SR-04 ───────────────────────────────────

def test_the_model_reproduces_spec_03_s2_1() -> None:
    """THE CONTROL. Given spec/03 §2.1's own 14 mm gap, the model must return
    §2.1's own published 17.4 pF, 9.6 pF and 435 ohm. If this passes and the
    8.50 mm case fails, the divergence is in the input, not the arithmetic."""
    c_web, c_stray, x_c = ins.shunt_impedance_ohm(ins.WEB_GAP_MM / 1000.0)
    assert c_web * 1e12 == pytest.approx(17.4, abs=0.1)
    assert c_stray * 1e12 == pytest.approx(9.6, abs=0.1)
    assert x_c == pytest.approx(435.0, abs=1.0)


def test_sewcp_401_occupies_five_and_a_half_mm_of_the_gap() -> None:
    assert ins.grounded_intrusion_mm() == pytest.approx(5.50)
    assert ins.best_case_clearance_mm() == pytest.approx(8.50)


def test_sr04_cannot_be_met_under_any_hardware_choice() -> None:
    """The clearance verdict needs no fastener dimension: even with the RF-hot
    boundary flush against the ceramic, 8.50 < 12.00."""
    v = next(v for v in ins.verdicts()
             if v.requirement == "SR-04" and v.limit == ins.SR04_MIN_CLEARANCE_MM)
    assert not v.passes
    assert v.shortfall == pytest.approx(3.50)


def test_sr03_fails_even_with_the_fillets_the_model_omits() -> None:
    creep = [v for v in ins.verdicts() if v.requirement == "SR-03"]
    assert len(creep) == 2
    assert all(not v.passes for v in creep)
    assert ins.creepage_mm(with_fillets=False) == pytest.approx(14.00)
    assert ins.creepage_mm(with_fillets=True) == pytest.approx(17.42, abs=0.01)


def test_sr02_falls_below_its_floor_once_the_clamp_ring_is_counted() -> None:
    v = next(v for v in ins.verdicts() if v.requirement == "SR-02")
    assert not v.passes
    assert v.value == pytest.approx(353.9, abs=0.5)


def test_the_clamp_ring_collides_with_the_web() -> None:
    """Independent of every electrical number: the two footprints intersect."""
    assert ins.radial_overlap_mm() == pytest.approx(3.00)


def test_the_bolt_holes_undercut_the_web_wall() -> None:
    assert ins.bolt_hole_under_web_mm() == pytest.approx(2.50)


def test_the_flange_has_no_radial_room_for_its_own_features() -> None:
    """16.00 mm of flange against 16.00 mm of demand - zero margin, before any
    edge distance. This is why the R3.0 fillets are absent from the model."""
    available, demand = ins.flange_radial_demand_mm()
    assert available == pytest.approx(16.00)
    assert demand == pytest.approx(16.00)
    assert demand >= available


def test_a_clamp_ring_that_fitted_would_pass_sr04() -> None:
    """Adversarial: the check must be sensitive to the input it blames.
    Shrink the intrusion to zero and SR-04 clears, which proves the verdict is
    driven by CR-D03 and not by a coding error."""
    original = ins.CLAMP_RING_T_MM
    try:
        ins.CLAMP_RING_T_MM = 0.50           # flush with the register, zero intrusion
        assert ins.best_case_clearance_mm() == pytest.approx(14.00)
        v = next(v for v in ins.verdicts()
                 if v.requirement == "SR-04" and v.limit == ins.SR04_MIN_CLEARANCE_MM)
        assert v.passes
    finally:
        ins.CLAMP_RING_T_MM = original


def test_safety_factor_is_the_specifications_and_not_a_local_choice() -> None:
    assert SAFETY_FACTOR == 3.0
