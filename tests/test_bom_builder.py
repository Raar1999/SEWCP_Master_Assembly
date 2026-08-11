"""The BOM builder: observed-state derivation and the four cross-checks."""

import json

from sedep.bom import build_bom
from sedep.bom.builder import BomRow, cross_check

RUN = "cad/runs/RUN-20260811T200919-f6cb5e/run.json"


def test_bom_derives_quantities_from_observed_occurrences():
    rows = build_bom(RUN)
    q = {r.part_number: r.qty for r in rows if "verified model" in r.cad_state}
    assert q["SEWCP-600"] == 3      # lift pins
    assert q["SEWCP-700"] == 6      # three up, three down
    assert q["SEWCP-1000"] == 3     # RTD retainers
    assert q["SEWCP-200"] == 1


def test_cross_checks_are_clean_on_the_real_state():
    rows = build_bom(RUN)
    assert cross_check(rows, RUN) == []


def test_omitting_a_component_is_detected(tmp_path):
    rows = build_bom(RUN)
    rows = [r for r in rows if r.part_number != "SEWCP-800"]
    faults = cross_check(rows, RUN)
    assert any("SEWCP-800" in f for f in faults)


def test_inventing_a_component_is_detected(tmp_path):
    rows = build_bom(RUN)
    rows.append(BomRow(1, "SEWCP-999", "IMAGINARY", 1, "X", "-",
                       "verified model (SEWCP-999_X)", "-", ""))
    faults = cross_check(rows, RUN)
    assert any("SEWCP-999" in f for f in faults)


def test_wrong_quantity_is_detected(tmp_path):
    rows = build_bom(RUN)
    for r in rows:
        if r.part_number == "SEWCP-600":
            r.qty = 2
    faults = cross_check(rows, RUN)
    assert any("SEWCP-600" in f for f in faults)


def test_fastener_schedule_is_parsed_from_the_frozen_spec():
    rows = build_bom(RUN)
    hw = [r for r in rows if r.part_number.startswith("HW-")]
    assert len(hw) >= 4
    assert all(r.spec_source == "spec/00 §9 (verbatim)" for r in hw)


def test_repair_record_supersedes_run_record_material():
    # The SEWCP-600 Steel defect (OI-CAD-01) was repaired in Fusion and the
    # fresh observation recorded in cad/runs/REPAIRS_S-2026-08-11-04.json;
    # the immutable run record still says Steel, the newer evidence wins.
    rows = build_bom(RUN)
    lp = next(r for r in rows if r.part_number == "SEWCP-600")
    assert "DEFECT" not in lp.notes
    assert lp.material == "Al2O3 99.8%"


def test_material_mismatch_detection_still_works():
    from sedep.bom.builder import _material_matches
    assert not _material_matches("Al2O3 99.8%", "Steel")
    assert _material_matches("Al2O3 99.8%", "Aluminum Oxide")
    assert _material_matches("6061-T6", "Aluminum 6061")
