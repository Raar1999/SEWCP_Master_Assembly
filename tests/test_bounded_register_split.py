"""Adversarial tests for the bounded-register-split half of V-03.

`AIEF-AMD-014` §AMD-49 bound this property into `validation[V-03]` and declared
a break of it BLOCKING. It was then checked by nothing for four sessions. When
the check was finally implemented at `S-2026-08-11-06` it found **two live
breaks immediately**: five register rows carrying a decorated leading cell
instead of a bare identifier, and two rows sitting in a register section the
index disagreed with. V-03 had been reporting PASS throughout.

So the point of this file is NOT that the check passes on today's tree. It is
that each way of breaking the mapping is attacked separately, because a check
that only passes today is the defect it was written to prevent.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aief_stage6.manifest import load_manifest  # noqa: E402
from aief_stage6.preconditions import check_v03  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
INDEX = ".ai/project/OPEN_ITEMS.md"
REGISTER = ".ai/project/OPEN_ITEMS_REGISTER.md"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A copy of the real tree: the manifest, the index and the register. The
    real repository is never written."""
    root = tmp_path / "repo"
    (root / "framework").mkdir(parents=True)
    shutil.copy2(REPO / "framework/framework.manifest.json",
                 root / "framework/framework.manifest.json")
    for rel in (INDEX, REGISTER):
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, dst)
    return root


def _v03(root: Path):
    return check_v03(load_manifest(root), root)


def _edit(root: Path, rel: str, fn) -> None:
    p = root / rel
    p.write_bytes(fn(p.read_text(encoding="utf-8")).encode("utf-8"))


def test_the_live_mapping_holds() -> None:
    """The live tree. If this fails, the index and the register have parted
    company and the register is the authority."""
    result = _v03(REPO)
    assert result["status"] == "PASS", json.dumps(result["details"], indent=2)
    assert result["counts"]["register_pairs"] == 1
    assert result["counts"]["mapped_identifiers"] > 0


def test_the_check_actually_reaches_the_registers(repo: Path) -> None:
    """A check that silently no-ops when its inputs are missing is worse than
    none: it reports PASS forever."""
    assert _v03(repo)["status"] == "PASS"
    (repo / REGISTER).unlink()
    result = _v03(repo)
    assert result["status"] == "FAIL"
    assert any("absent from the tree" in d for d in result["details"])


def test_identifier_in_the_index_with_no_register_row_fails(repo: Path) -> None:
    _edit(repo, INDEX, lambda t: t.replace("## Blocking\n\n",
                                           "## Blocking\n\nXX-NOT-A-REAL-ITEM\n"))
    result = _v03(repo)
    assert result["status"] == "FAIL"
    assert any("XX-NOT-A-REAL-ITEM is in the index" in d for d in result["details"])


def test_register_row_with_no_index_entry_fails(repo: Path) -> None:
    _edit(repo, INDEX, lambda t: t.replace("\nOI-CAD-03\n", "\n"))
    result = _v03(repo)
    assert result["status"] == "FAIL"
    assert any("OI-CAD-03 leads a register row" in d for d in result["details"])


def test_section_mismatch_fails(repo: Path) -> None:
    """The break that was live: a row in one section, its id in another. The
    mapping is section-wise, so moving an id between sections must fail until
    the row follows it."""
    _edit(repo, INDEX, lambda t: t.replace("\nOI-CAD-03\n", "\n")
          .replace("## Closed\n\n", "## Closed\n\nOI-CAD-03\n"))
    result = _v03(repo)
    assert result["status"] == "FAIL"
    joined = " ".join(result["details"])
    assert "OI-CAD-03" in joined


def test_duplicated_index_identifier_fails(repo: Path) -> None:
    _edit(repo, INDEX, lambda t: t.replace("\nOI-CAD-03\n", "\nOI-CAD-03\nOI-CAD-03\n"))
    result = _v03(repo)
    assert result["status"] == "FAIL"
    assert any("duplicated" in d for d in result["details"])


def test_index_line_carrying_more_than_one_identifier_fails(repo: Path) -> None:
    """index_grammar: 'one identifier per line, nothing else on that line'.
    This is the break that was live five times over - a leading cell decorated
    with a disposition summary. Cheap to write, and it silently unbinds the row
    from its index entry."""
    _edit(repo, INDEX,
          lambda t: t.replace("\nOI-CAD-03\n",
                              "\nOI-CAD-03 (DISPOSITIONED, see the register)\n"))
    result = _v03(repo)
    assert result["status"] == "FAIL"
    assert any("carries more than one identifier" in d for d in result["details"])


def test_a_heading_present_on_only_one_side_fails(repo: Path) -> None:
    _edit(repo, INDEX, lambda t: t + "\n## Invented Section\n\nZZ-INVENTED\n")
    result = _v03(repo)
    assert result["status"] == "FAIL"
    assert any("Invented Section" in d for d in result["details"])


def test_the_cross_reference_half_still_runs(repo: Path) -> None:
    """AMD-49 ADDED to V-03; it did not replace it. Break the original half and
    the check must still fail."""
    def break_law_ref(t: str) -> str:
        m = json.loads(t)
        m["laws"][0]["checks"] = ["V-99-DOES-NOT-EXIST"]
        return json.dumps(m, indent=2)

    _edit(repo, "framework/framework.manifest.json", break_law_ref)
    result = _v03(repo)
    assert result["status"] == "FAIL"
    assert any("V-99-DOES-NOT-EXIST" in d for d in result["details"])


def test_the_state_pair_is_declared_unchecked_not_silently_passed(repo: Path) -> None:
    """`bounded_register_split.pairs` declares two pairs; only the open-items
    pair is an identifier bijection. The state pair is a section-name
    correspondence over a YAML block, and asserting the wrong relation is worse
    than asserting none - so it is excluded deliberately and the count says so.
    If a future session implements it, this test should be the one that changes.
    """
    manifest = json.loads(
        (repo / "framework/framework.manifest.json").read_text(encoding="utf-8"))
    declared = manifest["metadata"]["reproducible"]["bounded_register_split"]["pairs"]
    assert len(declared) == 2, declared
    assert _v03(repo)["counts"]["register_pairs"] == 1
