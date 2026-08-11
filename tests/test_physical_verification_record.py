"""PVR-001 is derived from the frozen specification, and stays derived.

A verification matrix that is transcribed by hand goes stale the first time a
requirement moves, and a stale verification matrix is worse than none: it
reports coverage of a specification that no longer exists. These tests re-parse
`spec/01`..`spec/09` on every run and hold PVR-001 to them.

The last assertion is the one that matters most. PVR-001 exists to keep
"the model says so" and "the hardware says so" apart, and this project holds
no test evidence for any requirement. If a row here is ever marked VERIFIED,
either hardware was built and the evidence must be cited, or someone confused
a prediction for a measurement.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PVR = REPO / ".ai" / "project" / "verification" / \
    "PVR-001_Physical_Verification_Record_And_Test_Matrix.md"

_REQ_ROW = re.compile(
    r"^\|\s*([A-Z]{2,3}-\d{2})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")

#: Declared verification methods a drawing, a design statement or an analysis
#: discharges without a physical article. Everything else needs hardware.
DESK_METHODS = {
    "—", "-", "Design", "Design verification", "Design calculation", "Analysis",
    "Calculation", "Derived", "Derived from SR-05", "Hertzian analysis",
    "Material selection", "Sensor specification", "Drawing", "Drawing review",
    "Drawing verification", "Drawing + inspection", "Drawing + travel check",
    "Sub-test",
}


def _spec_requirements() -> dict[str, str]:
    """{requirement id: declared verification method} across the nine volumes."""
    out: dict[str, str] = {}
    for spec in sorted((REPO / "spec").glob("[0-9]*.md")):
        for line in spec.read_text(encoding="utf-8").splitlines():
            m = _REQ_ROW.match(line.strip())
            if m:
                out.setdefault(m.group(1), m.group(4).strip().strip("*"))
    return out


def _hardware_required() -> set[str]:
    return {rid for rid, method in _spec_requirements().items()
            if method not in DESK_METHODS}


def _pvr_matrix_ids() -> set[str]:
    """Requirement ids carried in PVR-001 section 5's tables."""
    text = PVR.read_text(encoding="utf-8")
    body = text.split("## 5 ·", 1)[1].split("\n---", 1)[0]
    return set(re.findall(r"^\|\s*`([A-Z]{2,3}-\d{2})`\s*\|", body, re.MULTILINE))


def test_pvr_exists() -> None:
    assert PVR.is_file(), f"{PVR} is the physical verification record and is missing"


def test_every_hardware_requirement_appears_in_the_matrix() -> None:
    missing = sorted(_hardware_required() - _pvr_matrix_ids())
    assert not missing, (
        "requirements whose declared method needs hardware but which PVR-001 "
        f"section 5 does not carry: {missing}")


def test_the_matrix_invents_no_requirement() -> None:
    known = set(_spec_requirements())
    invented = sorted(_pvr_matrix_ids() - known)
    assert not invented, (
        f"PVR-001 section 5 names requirements no spec volume carries: {invented}")


def test_no_desk_dischargeable_requirement_is_listed_as_hardware() -> None:
    """A matrix that over-claims scope is as misleading as one that under-claims."""
    methods = _spec_requirements()
    wrong = sorted(rid for rid in _pvr_matrix_ids()
                   if methods.get(rid) in DESK_METHODS)
    assert not wrong, (
        f"PVR-001 lists these as hardware-required, but their declared method "
        f"is dischargeable at the desk: {wrong}")


def test_nothing_is_marked_verified_without_evidence() -> None:
    """THE LOAD-BEARING ASSERTION. No article of this design has been built.

    If this fails, do not edit the test. Either hardware now exists and PVR-001
    must cite the evidence for each VERIFIED row - at which point this test is
    replaced by one that checks the citation resolves - or a prediction has been
    written down as a measurement.
    """
    text = PVR.read_text(encoding="utf-8")
    # The status vocabulary table declares the token; a row claiming it would
    # appear inside a table cell.
    claims = [line for line in text.splitlines()
              if line.startswith("|") and re.search(r"\|\s*`?VERIFIED`?\s*\|", line)]
    # The vocabulary table's own definition row is the single lawful mention.
    claims = [c for c in claims if "Used nowhere in this file" not in c]
    assert not claims, (
        "PVR-001 marks a requirement VERIFIED. This project holds no physical "
        f"test evidence for any requirement:\n" + "\n".join(claims))


def test_the_census_counts_are_the_measured_counts() -> None:
    """PVR-001 section 1 states 137 / 46 / 84 / 7. Derive them, do not trust them."""
    methods = _spec_requirements()
    hybrid = {
        "Analysis + thermal test", "Thermal test / analysis",
        "Network analyzer / calculation", "4-wire at frequency / calculation",
        "Optical flat / CMM", "CMM / height gauge", "Interferometer / CMM",
    }
    desk = sum(1 for m in methods.values() if m in DESK_METHODS)
    hyb = sum(1 for m in methods.values() if m in hybrid)
    hardware = len(methods) - desk
    text = PVR.read_text(encoding="utf-8")
    for label, value in (("total", len(methods)), ("desk", desk),
                         ("hardware", hardware), ("hybrid", hyb)):
        assert f"**{value}**" in text, (
            f"PVR-001 section 1 does not state the measured {label} count "
            f"{value}; the record and the specification have parted company")
