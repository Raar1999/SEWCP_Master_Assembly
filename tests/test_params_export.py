"""The SEWCP-200 parameter CSV is derived from section 3, and the derivation is checked.

`VER-016` F-06: step 6.02 of the CAD package imports `params/generated/SEWCP-200.csv`
and the file had never existed, so the modeller necessarily fell back to typing
section 3 by hand. `VER-016` F-02 is what hand-typing produced last time - the
superseded 30/150/270 locator clocking surviving in the parameter master after
`ECR-D-010` removed it, in the one artifact the project's own `next_action`
directs a modeller to open.

Generating the CSV would create a second place to edit, which is worse, unless
the two are held together by a check that can fail. These tests are that check,
and the ones that matter are at the bottom: the emitter must refuse a section 3
that still says UNSPECIFIED, and `check` must fail on a CSV that has drifted.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aief_params.__main__ import cmd_check, cmd_emit  # noqa: E402
from aief_params.extract import (  # noqa: E402
    CSV_PATH,
    HEADER,
    PACKAGE,
    duplicates,
    parse,
    read_package,
    to_csv,
)

REPO = Path(__file__).resolve().parent.parent


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    dst = tmp_path / "repo"
    (dst / ".ai" / "project").mkdir(parents=True)
    (dst / Path(PACKAGE).parent).mkdir(parents=True)
    shutil.copy2(REPO / PACKAGE, dst / PACKAGE)
    (dst / "params" / "generated").mkdir(parents=True)
    shutil.copy2(REPO / CSV_PATH, dst / CSV_PATH)
    return dst


def _by_name(repo_root: Path) -> dict[str, str]:
    return {p.name: p.expression for p in read_package(repo_root)}


# --------------------------------------------------------------------------
# The live repository
# --------------------------------------------------------------------------


def test_the_committed_csv_reproduces_from_section_3() -> None:
    """The standing check, run against the real repository."""
    assert cmd_check(REPO) == 0


def test_the_csv_carries_the_declared_header() -> None:
    first = (REPO / CSV_PATH).read_text(encoding="utf-8").split("\n")[0]
    assert first == ",".join(HEADER)


def test_no_parameter_is_unspecified() -> None:
    for p in read_package(REPO):
        assert p.expression.upper() != "UNSPECIFIED", p.name


def test_no_duplicate_parameter_names() -> None:
    assert duplicates(read_package(REPO)) == []


# --------------------------------------------------------------------------
# The values ECR-D-004, -007 and -010 fixed, held against silent regression
# --------------------------------------------------------------------------


def test_top_locators_carry_the_reclocked_angles() -> None:
    """ECR-D-010. The collision `aief_clearance` found, and must not return."""
    p = _by_name(REPO)
    assert (p["ang_kin_top_1"], p["ang_kin_top_2"], p["ang_kin_top_3"]) == (
        "75.0", "195.0", "315.0"
    )


def test_the_superseded_clocking_is_not_on_the_top_locators() -> None:
    p = _by_name(REPO)
    assert {p["ang_kin_top_1"], p["ang_kin_top_2"], p["ang_kin_top_3"]} & {
        "30.0", "150.0", "270.0"
    } == set()
    # 30/150/270 is still correct for the lift pins - the point is which feature
    # carries it, not that the numbers are forbidden.
    assert (p["ang_liftpin_1"], p["ang_liftpin_2"], p["ang_liftpin_3"]) == (
        "30.0", "150.0", "270.0"
    )


def test_choke_counterbore_is_dimensioned() -> None:
    """ECR-D-004: HOLD H3 discharged at 11.0 W x 12.5 L x 2.5 deep."""
    p = _by_name(REPO)
    assert p["choke_cbore_w"] == "11.0"
    assert p["choke_cbore_l"] == "12.5"
    assert p["choke_cbore_dep"] == "2.5"


def test_locator_counterbore_is_the_ten_millimetre_form() -> None:
    """ECR-D-007 action 3 took the counterbore 12.000 -> 10.000."""
    assert _by_name(REPO)["kin_cbore_d"] == "10.0"


def test_the_z_stack_closes() -> None:
    """ECR-D-002. `lid_check` is an expression, and its inputs are the ruled ones."""
    p = _by_name(REPO)
    assert p["ch_depth"] == "6.0"
    assert p["lid_check"] == "ch_z_btm - lid_thk"
    assert p["ch_z_top"] == "cp_thk - ch_top_wall"
    assert p["ch_z_btm"] == "ch_z_top - ch_depth"
    values = {"cp_thk": 20.0, "ch_top_wall": 8.0, "ch_depth": 6.0, "lid_thk": 6.0}
    for name, expected in values.items():
        assert float(p[name]) == expected
    z_top = values["cp_thk"] - values["ch_top_wall"]
    assert z_top - values["ch_depth"] - values["lid_thk"] == 0.0


# --------------------------------------------------------------------------
# The parse itself
# --------------------------------------------------------------------------


def test_compound_names_expand_one_parameter_per_value() -> None:
    p = _by_name(REPO)
    for name in ("ang_kin_btm_1", "ang_kin_btm_2", "ang_kin_btm_3",
                 "rtd_r_1", "rtd_r_2", "rtd_r_3",
                 "rtd_ang_1", "rtd_ang_2", "rtd_ang_3",
                 "ang_hv_1", "ang_hv_2"):
        assert name in p
    assert "ang_kin_btm_1/2/3" not in p


def test_an_expression_with_a_slash_is_not_split() -> None:
    """`bc_rf / 2` is arithmetic; only a compound NAME licenses a split."""
    assert _by_name(REPO)["rf_land_r_mean"] == "bc_rf / 2"


def test_thread_and_fit_annotations_move_to_the_comment() -> None:
    params = {p.name: p for p in read_package(REPO)}
    assert params["he_bore"].expression == "10.0"
    assert "H8" in params["he_bore"].comment
    assert params["ring_tap_size"].expression == "6.0"
    assert "M6" in params["ring_tap_size"].comment


def test_tolerance_reference_parameters_are_included() -> None:
    p = _by_name(REPO)
    assert p["tol_thk"] == "0.030"
    assert p["tol_pos_kin"] == "0.020"


def test_every_parameter_cites_a_source() -> None:
    """Package section 9.2 P-09: the comment field must be populated."""
    for p in read_package(REPO):
        assert p.comment.strip(), p.name


def test_emission_is_deterministic() -> None:
    assert to_csv(read_package(REPO)) == to_csv(read_package(REPO))
    committed = (REPO / CSV_PATH).read_bytes().decode("utf-8-sig")
    assert to_csv(read_package(REPO)) == committed.replace("\r\n", "\n")


def test_the_emitter_writes_no_bom_and_lf_endings() -> None:
    """What the EMITTER guarantees, which is not what the working tree shows.

    `core.autocrlf=true` rewrites the checkout, so asserting the working-tree
    bytes here would be asserting a property of git rather than of this code -
    and it did fail exactly that way after a stash round-trip. `.gitattributes`
    pins the committed artifact to LF so Fusion imports what was emitted; this
    test holds the emitter to it at the source.
    """
    emitted = to_csv(read_package(REPO)).encode("utf-8")
    assert not emitted.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" not in emitted
    assert emitted.endswith(b"\n")


def test_the_committed_csv_carries_no_byte_order_mark() -> None:
    """A BOM would survive `.gitattributes` and would reach Fusion."""
    assert not (REPO / CSV_PATH).read_bytes().startswith(b"\xef\xbb\xbf")


# --------------------------------------------------------------------------
# The checks must be able to fail
# --------------------------------------------------------------------------


def test_check_fails_when_the_csv_drifts(repo: Path, capsys) -> None:
    target = repo / CSV_PATH
    target.write_text(
        target.read_text(encoding="utf-8").replace("75.0", "30.0", 1),
        encoding="utf-8",
    )
    assert cmd_check(repo) == 1
    assert "does not reproduce" in capsys.readouterr().out


def test_check_fails_when_the_csv_is_absent(repo: Path, capsys) -> None:
    (repo / CSV_PATH).unlink()
    assert cmd_check(repo) == 1
    assert "absent" in capsys.readouterr().out


def test_emission_refuses_an_unspecified_parameter(repo: Path, capsys) -> None:
    """A HOLD declared discharged while the value is still the word UNSPECIFIED.

    This is VER-016 F-03 exactly, and the emitter must refuse rather than write
    the word into a file a modeller imports.
    """
    package = repo / PACKAGE
    package.write_text(
        package.read_text(encoding="utf-8").replace("| `11.0` |", "| `UNSPECIFIED` |", 1),
        encoding="utf-8",
    )
    assert cmd_emit(repo) == 1
    out = capsys.readouterr().out
    assert "UNSPECIFIED" in out
    assert "REFUSED" in out


def test_emission_refuses_a_duplicate_name(repo: Path, capsys) -> None:
    package = repo / PACKAGE
    text = package.read_text(encoding="utf-8")
    row = "| `cp_od` | Plate outside diameter | `320.0` | mm | CP-D01 envelope | — |"
    package.write_text(text.replace(row, row + "\n" + row, 1), encoding="utf-8")
    assert cmd_emit(repo) == 1
    assert "duplicate" in capsys.readouterr().out


def test_a_changed_section_3_changes_the_csv(repo: Path) -> None:
    """The derivation is live, not a snapshot taken once."""
    before = to_csv(parse((repo / PACKAGE).read_text(encoding="utf-8")))
    package = repo / PACKAGE
    package.write_text(
        package.read_text(encoding="utf-8").replace("| `320.0` |", "| `321.0` |", 1),
        encoding="utf-8",
    )
    after = to_csv(parse(package.read_text(encoding="utf-8")))
    assert before != after
    assert "cp_od,mm,321.0" in after
