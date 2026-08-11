"""The assembly layer: package discipline and observed-state verification.

Pure tests - no Fusion. The seam is `verify_assembly(package, observed)`,
which must decide from observed state alone, and the loader, which must
refuse a placement without provenance.
"""

import json

import pytest

from aief_cad.assembly import (
    AssemblyError,
    load_assembly_package,
    verify_assembly,
)


def _package(tmp_path, rows=None):
    body = {
        "package_id": "T-ASM-001",
        "document": "T_DOC",
        "units": "mm",
        "authority": ["test"],
        "occurrences": rows if rows is not None else [
            {"occurrence_id": "A", "design": "D1",
             "translate_mm": [0, 0, 5.0], "z_band": [5.0, 15.0],
             "provenance": "test row"},
            {"occurrence_id": "B", "design": "D2",
             "translate_mm": [10.0, 0, 0], "rotate_z_deg": 90.0,
             "rotate_x_deg": 180.0, "provenance": "test row"},
        ],
    }
    p = tmp_path / "asm.json"
    p.write_text(json.dumps(body), encoding="utf-8")
    return load_assembly_package(p)


def _observed(doc="T_DOC", rows=None):
    return {
        "document": {"persisted_name": doc, "saved": True},
        "occurrences": rows if rows is not None else [
            {"name": "D1:1", "component": "D1", "source_design": "D1",
             "source_version": 2, "grounded": True,
             "translate_mm": [0.0, 0.0, 5.0], "rotate_z_deg": 0.0,
             "z_axis_scale": 1.0,
             "bbox_min": [-1, -1, 5.0], "bbox_max": [1, 1, 15.0]},
            {"name": "D2:1", "component": "D2", "source_design": "D2",
             "source_version": 3, "grounded": True,
             "translate_mm": [10.0, 0.0, 0.0], "rotate_z_deg": 90.0,
             "z_axis_scale": -1.0},
        ],
    }


def test_conforming_assembly_passes(tmp_path):
    verdict = verify_assembly(_package(tmp_path), _observed())
    assert verdict["passed"], verdict["checks"]


def test_placement_error_fails(tmp_path):
    obs = _observed()
    obs["occurrences"][0]["translate_mm"] = [0.0, 0.0, 5.2]
    obs["occurrences"][0]["bbox_min"][2] = 5.2
    obs["occurrences"][0]["bbox_max"][2] = 15.2
    verdict = verify_assembly(_package(tmp_path), obs)
    assert not verdict["passed"]
    failing = {c["id"] for c in verdict["checks"] if not c["passed"]}
    assert "AS-A" in failing


def test_wrong_local_frame_is_caught_by_the_z_band(tmp_path):
    # Transform is exactly as commanded, but the body sits elsewhere -
    # the failure a transform comparison alone cannot see.
    obs = _observed()
    obs["occurrences"][0]["bbox_min"] = [-1, -1, -5.0]
    obs["occurrences"][0]["bbox_max"] = [1, 1, 5.0]
    verdict = verify_assembly(_package(tmp_path), obs)
    assert not verdict["passed"]


def test_missing_flip_fails(tmp_path):
    obs = _observed()
    obs["occurrences"][1]["z_axis_scale"] = 1.0
    verdict = verify_assembly(_package(tmp_path), obs)
    assert not verdict["passed"]


def test_undeclared_occurrence_fails(tmp_path):
    obs = _observed()
    obs["occurrences"].append(
        {"name": "STRAY:1", "component": "STRAY", "source_design": "STRAY",
         "source_version": 1, "grounded": True,
         "translate_mm": [0, 0, 0], "rotate_z_deg": 0.0})
    verdict = verify_assembly(_package(tmp_path), obs)
    failing = {c["id"] for c in verdict["checks"] if not c["passed"]}
    assert failing == {"AS-COUNT", "AS-EXTRA"}


def test_missing_occurrence_fails(tmp_path):
    obs = _observed()
    obs["occurrences"].pop(1)
    verdict = verify_assembly(_package(tmp_path), obs)
    failing = {c["id"] for c in verdict["checks"] if not c["passed"]}
    assert "AS-B" in failing


def test_wrong_document_fails(tmp_path):
    verdict = verify_assembly(_package(tmp_path), _observed(doc="OTHER"))
    failing = {c["id"] for c in verdict["checks"] if not c["passed"]}
    assert "AS-DOC" in failing


def test_provenance_is_mandatory(tmp_path):
    with pytest.raises(AssemblyError):
        _package(tmp_path, rows=[
            {"occurrence_id": "A", "design": "D1",
             "translate_mm": [0, 0, 0]}])


def test_duplicate_occurrence_id_refused(tmp_path):
    with pytest.raises(AssemblyError):
        _package(tmp_path, rows=[
            {"occurrence_id": "A", "design": "D1",
             "translate_mm": [0, 0, 0], "provenance": "x"},
            {"occurrence_id": "A", "design": "D1",
             "translate_mm": [1, 0, 0], "provenance": "x"}])


def test_same_design_twice_matches_by_position(tmp_path):
    pkg = _package(tmp_path, rows=[
        {"occurrence_id": "P1", "design": "PIN",
         "translate_mm": [100.0, 0, 0], "provenance": "x"},
        {"occurrence_id": "P2", "design": "PIN",
         "translate_mm": [-100.0, 0, 0], "provenance": "x"}])
    obs = _observed(rows=[
        {"name": "PIN:2", "component": "PIN", "source_design": "PIN",
         "source_version": 1, "grounded": True,
         "translate_mm": [-100.0, 0.0, 0.0], "rotate_z_deg": 0.0,
         "z_axis_scale": 1.0},
        {"name": "PIN:1", "component": "PIN", "source_design": "PIN",
         "source_version": 1, "grounded": True,
         "translate_mm": [100.0, 0.0, 0.0], "rotate_z_deg": 0.0,
         "z_axis_scale": 1.0}])
    verdict = verify_assembly(pkg, obs)
    assert verdict["passed"], verdict["checks"]
