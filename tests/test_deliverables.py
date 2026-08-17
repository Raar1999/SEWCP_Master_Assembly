"""Adversarial tests for the deliverable register check.

The check exists because `cad/DELIVERABLES.md` was true and unreachable for
four sessions - every digest reproduced, and every file it named lived on one
machine outside the repository (`ECR-D-015`). A test suite that only asserts
"the live register passes today" would reproduce that failure exactly: it
would go green while the property rotted underneath it.

So every test below except `test_the_live_register_binds` constructs a defect
and REQUIRES the check to fail on it. One mutation per failure mode, each
named for the mode. If any of these starts passing, the check has stopped
checking.
"""

from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aief_deliverables.check import (  # noqa: E402
    REGISTER,
    SUBTREES,
    check,
    on_disk,
    parse_register,
)

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture()
def sandbox(tmp_path: Path) -> Path:
    """A miniature repository: three deliverables and a register that binds them."""
    (tmp_path / ".ai" / "project").mkdir(parents=True)
    files = {
        "cad/exports/step/PART-A.step": b"ISO-10303-21;\r\nHEADER;\r\nENDSEC;\r\n",
        "cad/exports/stl/PART-A.stl": bytes(range(256)) * 4,        # NUL octets, binary
        "drawings/parts/PART-A/PART-A-DRW-001_Sh1.pdf": b"%PDF-1.4\n\x00\x01binary\n%%EOF\n",
    }
    rows = []
    for rel, octets in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(octets)
        rows.append(f"| `{rel}` | {len(octets)} | `{hashlib.sha256(octets).hexdigest()}` |")

    (tmp_path / REGISTER).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / REGISTER).write_text(
        "# Exported CAD Deliverables\n\n"
        "Prose that is not a row, with a `backticked path` in it.\n\n"
        "| Repository path | Bytes | sha256 |\n|---|---:|---|\n"
        + "\n".join(rows)
        + "\n\nTrailing narrative, also not a row.\n",
        encoding="utf-8",
    )
    return tmp_path


def test_the_live_register_binds() -> None:
    """The one non-adversarial test: the repository's own register reproduces."""
    rep = check(REPO)
    assert rep.ok, (
        f"missing={rep.missing} size={rep.size_mismatch} "
        f"digest={rep.digest_mismatch} unregistered={rep.unregistered}"
    )
    assert rep.rows, "an empty register would pass every other assertion vacuously"


def test_the_live_register_is_exhaustive_over_the_subtrees() -> None:
    """Bi-directional, on the live tree: nothing on disk escapes the register."""
    registered = {r.path for r in check(REPO).rows}
    assert set(on_disk(REPO)) == registered


def test_sandbox_is_green_before_any_mutation(sandbox: Path) -> None:
    rep = check(sandbox)
    assert rep.ok and len(rep.rows) == 3


def test_a_deleted_deliverable_fails(sandbox: Path) -> None:
    (sandbox / "cad/exports/step/PART-A.step").unlink()
    rep = check(sandbox)
    assert not rep.ok
    assert rep.missing == ["cad/exports/step/PART-A.step"]


def test_one_flipped_octet_fails(sandbox: Path) -> None:
    """The failure mode a size check alone cannot see."""
    p = sandbox / "cad/exports/stl/PART-A.stl"
    octets = bytearray(p.read_bytes())
    octets[7] ^= 0x01
    p.write_bytes(bytes(octets))
    rep = check(sandbox)
    assert not rep.ok
    assert not rep.size_mismatch, "same length - only the digest can catch this"
    assert [d[0] for d in rep.digest_mismatch] == ["cad/exports/stl/PART-A.stl"]


def test_crlf_to_lf_normalisation_fails(sandbox: Path) -> None:
    """The exact damage `* text eol=lf` would have done to the 37 text deliverables."""
    p = sandbox / "cad/exports/step/PART-A.step"
    p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n"))
    rep = check(sandbox)
    assert not rep.ok
    assert rep.size_mismatch and rep.digest_mismatch


def test_an_unregistered_deliverable_fails(sandbox: Path) -> None:
    """The direction that catches an artifact shipping without being verified."""
    (sandbox / "drawings/assembly").mkdir(parents=True, exist_ok=True)
    (sandbox / "drawings/assembly/SEWCP-000-DRW-001_Sh1.svg").write_bytes(b"<svg/>\n")
    rep = check(sandbox)
    assert not rep.ok
    assert rep.unregistered == ["drawings/assembly/SEWCP-000-DRW-001_Sh1.svg"]


def test_a_register_row_naming_nothing_fails(sandbox: Path) -> None:
    """A register may not grow rows for files that do not exist."""
    reg = sandbox / REGISTER
    reg.write_text(
        reg.read_text(encoding="utf-8")
        + f"| `cad/exports/step/GHOST.step` | 3 | `{hashlib.sha256(b'abc').hexdigest()}` |\n",
        encoding="utf-8",
    )
    rep = check(sandbox)
    assert not rep.ok and rep.missing == ["cad/exports/step/GHOST.step"]


def test_gitkeep_and_parametric_source_are_not_deliverables(sandbox: Path) -> None:
    """The two documented exclusions, held by test so they cannot drift silently."""
    (sandbox / "cad/exports/step/.gitkeep").write_bytes(b"")
    (sandbox / "cad/exports/step/PART-A.f3d").write_bytes(b"\x00fusion")
    rep = check(sandbox)
    assert rep.ok, f"unregistered={rep.unregistered}"


def test_the_row_grammar_ignores_prose(sandbox: Path) -> None:
    """Backticked paths in narrative must not be mistaken for register rows."""
    rows = parse_register((sandbox / REGISTER).read_text(encoding="utf-8"))
    assert [r.path for r in rows] == [
        "cad/exports/step/PART-A.step",
        "cad/exports/stl/PART-A.stl",
        "drawings/parts/PART-A/PART-A-DRW-001_Sh1.pdf",
    ]


def test_an_absent_register_is_an_error_not_a_pass(tmp_path: Path) -> None:
    """Fail closed. A missing register must never read as 'nothing to check'."""
    (tmp_path / ".ai" / "project").mkdir(parents=True)
    with pytest.raises(FileNotFoundError):
        check(tmp_path)


def test_an_emptied_subtree_fails_rather_than_passing_vacuously(sandbox: Path) -> None:
    """The `ECR-D-015` failure itself: the register intact, the tree emptied."""
    for sub in SUBTREES:
        shutil.rmtree(sandbox / sub, ignore_errors=True)
    rep = check(sandbox)
    assert not rep.ok
    assert len(rep.missing) == 3
