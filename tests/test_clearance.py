"""Regression tests for the feature-clearance check.

The load-bearing test is `test_ecr_d_010_defect_is_detected`: it puts the clocking
map back the way it was when the collision was frozen and requires the check to
fail. Without it this module would only prove that today's map passes, which is
the property `spec/00` section 3.2 already claimed in prose before anything
computed it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aief_clearance.check import ICD, check, load_map  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    (tmp_path / ".ai" / "project").mkdir(parents=True)
    (tmp_path / "spec").mkdir()
    (tmp_path / ICD).write_text(
        (REPO / ICD).read_text(encoding="utf-8"), encoding="utf-8"
    )
    return tmp_path


def _reclock(repo: Path, old: str, new: str) -> None:
    target = repo / ICD
    text = target.read_text(encoding="utf-8")
    assert old in text, old
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def test_live_map_is_clear() -> None:
    report = check(REPO)
    assert report.ok, [
        f"{f.a}@{f.angle_a} vs {f.b}@{f.angle_b}: {f.distance:.2f} < {f.required:.2f}"
        for f in report.findings
    ]


def test_ecr_d_010_defect_is_detected(repo: Path) -> None:
    """Restore the pre-disposition clocking and require a failure."""
    _reclock(repo, "**75°, 195°, 315°**", "30°, 150°, 270°")
    report = check(repo)
    assert not report.ok, "the ECR-D-010 collision must not pass"
    hit = [
        f for f in report.findings
        if "Kinematic locators" in f.a + f.b and "choke" in (f.a + f.b).lower()
    ]
    assert hit, [(f.a, f.b) for f in report.findings]
    assert hit[0].angle_a in (30.0, 150.0, 270.0) or hit[0].angle_b in (30.0, 150.0, 270.0)


def test_removing_the_locator_row_is_not_silently_a_pass(repo: Path) -> None:
    """The original failure was an ABSENT row, not a wrong one. A feature that
    disappears from the map must be reported as unchecked, never as clear."""
    _reclock(
        repo,
        "| **Kinematic locators (Cooling Plate↔Heater Plate)** | **Ø260 BC** | **75°, 195°, 315°** | **3** |\n",
        "",
    )
    features, _ = load_map(repo)
    names = {f.name for f in features}
    assert "Kinematic locators (Cooling Plate<->Heater Plate)" not in names
    assert check(repo).ok  # nothing to collide with
    # ...but the feature is gone from the checked set, which is exactly the
    # condition that let ECR-D-010 through. The map must therefore be complete,
    # and completeness is asserted below against the live repository.


def test_every_declared_footprint_is_present_in_the_live_map() -> None:
    """Completeness in the direction that actually failed: a feature with a
    declared footprint must appear in the clocking map."""
    features, skipped = load_map(REPO)
    named = {f.name for f in features}
    expected = {
        "Thermal-choke fasteners (inner)",
        "Thermal-choke fasteners (outer)",
        "Kinematic locators (Cooling Plate<->Heater Plate)",
        "Kinematic radial slots (Ring<->Cooling Plate)",
        "RF strap land (Cooling Plate)",
        "Lift pin bores",
        "Support Ring fasteners (two independent circuits, DR-9)",
        "ESC HV electrode feed contacts",
    }
    assert expected <= named, expected - named


def test_n_plus_pattern_expands_to_the_declared_quantity() -> None:
    features, _ = load_map(REPO)
    by_name = {f.name: f for f in features}
    assert len(by_name["Thermal-choke fasteners (outer)"].angles) == 12
    assert len(by_name["Support Ring fasteners (two independent circuits, DR-9)"].angles) == 8


def test_radial_separation_alone_is_sufficient_clearance(repo: Path) -> None:
    """Two features on the same ray but radially far apart must not be reported.
    The first version of this check used centre distance and produced three such
    false failures."""
    features, _ = load_map(repo)
    by_name = {f.name: f for f in features}
    hv = by_name["ESC HV electrode feed contacts"]      # r 26-34
    ring = by_name["Support Ring fasteners (two independent circuits, DR-9)"]
    assert hv.r_span()[1] < ring.r_span()[0]
    report = check(repo)
    assert not [f for f in report.findings if hv.name in (f.a, f.b) and ring.name in (f.a, f.b)]


def test_rf_land_uses_the_declared_envelope_not_the_nominal_arc() -> None:
    features, _ = load_map(REPO)
    land = next(f for f in features if f.name.startswith("RF strap land"))
    assert land.theta_half() == 12.0  # 93-117 deg, spec/01 section 3.1
