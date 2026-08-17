"""No state register may assert, in its own voice, a value another artifact governs.

**This module exists because four independent rounds found one defect, and the
third repair of it was itself defective.** `STATE_REGISTER.md` recited
`last_ledger_seq` as `1`, then `2`, and named `R-017`, then `R-023`/`R-025`, as
the current exec-layer head - each written before the close that moved it.

Round 4 then found that **the first version of this module did not catch the
defect in its own historical phrasing**. Its regex was line-bounded and the
register's real wording put the heading and the value two lines apart, so the
verbatim round-3 defect passed all seven tests while four artifacts claimed
"both were caught". That is the failure this repository names most often: a
property asserted as checked and not checked.

So the tests below **replay the defect in the phrasings that actually
occurred**, not in phrasings written to suit a pattern. The first version's
self-test was circular - it validated the regex against a string built for the
regex - which is exactly why it passed while the real thing walked through.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aief_register.check import SCOPE, check, current_results, ledger_seq  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
REGISTER = ".ai/project/STATE_REGISTER.md"
STATE = ".ai/project/STATE.md"


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """A copy of the tree sufficient to run the check. The real repository is
    never written."""
    root = tmp_path / "repo"
    (root / ".ai" / "project" / "ledger").mkdir(parents=True)
    for rel in (REGISTER, STATE, ".ai/project/ledger/HEAD"):
        shutil.copy2(REPO / rel, root / rel)
    for sub in ("tasks", "results"):
        shutil.copytree(REPO / ".ai/project" / sub, root / ".ai/project" / sub)
    shutil.copytree(REPO / "src", root / "src",
                    ignore=shutil.ignore_patterns("__pycache__"))
    return root


def _edit(root: Path, rel: str, fn) -> None:
    p = root / rel
    p.write_text(fn(p.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")


# -- the live tree ---------------------------------------------------------

def test_the_live_registers_assert_nothing_governed() -> None:
    rep = check(REPO)
    assert rep.ok, "\n".join(str(f) for f in rep.findings)
    assert rep.scanned == list(SCOPE), "a file dropping out of scope would go unchecked"


def test_state_md_and_head_agree_on_the_sequence() -> None:
    """B4 check 3, asserted where a test can see it."""
    declared = int(re.search(r"^last_ledger_seq:\s*(\d+)",
                             (REPO / STATE).read_text(encoding="utf-8"), re.M).group(1))
    assert declared == ledger_seq(REPO)


def test_there_is_something_to_check() -> None:
    """Guard on the guard: an empty CURRENT set makes the head half vacuous."""
    assert current_results(REPO)
    assert ledger_seq(REPO) >= 1


# -- the defects, replayed verbatim ----------------------------------------

def test_the_round_3_sequence_defect_verbatim_is_caught(repo: Path) -> None:
    """**The mutation the first version of this module let through.**

    Heading on one line, value two lines below, in the register's own wording
    at commit `1c15818`. A line-scoped pattern cannot see it.
    """
    _edit(repo, REGISTER, lambda s: s.replace(
        "## last_ledger_seq\n",
        "## last_ledger_seq\n\n`2`, reconciled with `HEAD.seq`.\n\nseq 2\n", 1))
    rep = check(repo)
    assert not rep.ok, "the verbatim round-3 defect walked through again"
    assert any("sequence" in f.kind for f in rep.findings), \
        [str(f) for f in rep.findings]


def test_the_round_2_head_defect_verbatim_is_caught(repo: Path) -> None:
    _edit(repo, REGISTER, lambda s: s.replace(
        "## active_tasks\n",
        "## active_tasks\n\n`R-017` is the current head of the exec-layer chain "
        "and seals `R-014`.\n", 1))
    rep = check(repo)
    assert not rep.ok
    assert any("superseded result" in f.kind for f in rep.findings)


def test_the_round_3_head_defect_verbatim_is_caught(repo: Path) -> None:
    _edit(repo, REGISTER, lambda s: s.replace(
        "## active_tasks\n",
        "## active_tasks\n\nComputed from `aief_exec.graph`, the CURRENT heads are\n"
        "`R-021`, `R-023` and `R-025`.\n", 1))
    stated = {f.stated for f in check(repo).findings}
    assert {"R-023", "R-025"} <= stated, stated


def test_the_round_4_defect_in_state_md_is_caught(repo: Path) -> None:
    """It was live in the governing file when round 4 ran."""
    _edit(repo, STATE, lambda s: s.replace(
        "- **Ledger `active`.**",
        "- **Ledger `active`**, seq 2 (`L-0000002`).\n- **Ledger `active`.**", 1))
    rep = check(repo)
    assert not rep.ok
    assert any(f.path == STATE for f in rep.findings)


@pytest.mark.parametrize("phrasing", [
    "`2`, reconciled with `HEAD.seq`.\n\nseq 2",
    "The head entry is `L-0000002`.",
    "seq 2 (`L-0000002`)",
    "seq: 2",
    "The ledger is at seq 2.",
])
def test_a_spread_of_sequence_phrasings_is_caught(repo: Path, phrasing: str) -> None:
    """Round 4 found 7 of 9 phrasings evading the first version."""
    _edit(repo, REGISTER, lambda s: s.replace(
        "## last_ledger_seq\n", f"## last_ledger_seq\n\n{phrasing}\n", 1))
    assert not check(repo).ok, phrasing


@pytest.mark.parametrize("phrasing", [
    "The head is `R-025`.",
    "`R-025` is current.",
    "The record of record is `R-023`.",
    "The record pinning `src/aief_exec/**` is `R-023`.",
    "Currently at the head: `R-025`.",
    "The unsuperseded results are `R-021`, `R-023` and `R-025`.",
])
def test_every_head_phrasing_round_4_found_is_caught(repo: Path, phrasing: str) -> None:
    """All six survivors round 4 constructed. Naming a superseded id in body
    text now fails whatever the sentence around it says - which is why the rule
    is structural rather than lexical."""
    _edit(repo, REGISTER, lambda s: s.replace(
        "## active_tasks\n", f"## active_tasks\n\n{phrasing}\n", 1))
    assert not check(repo).ok, phrasing


# -- and it must not punish the record for being honest --------------------

def test_a_blockquote_recounting_the_defect_is_not_a_finding(repo: Path) -> None:
    """The first attempt at this rule flagged thirty assertions, almost all of
    them a register *recording* the defect. A rule that cannot tell
    'X is current' from 'X was wrongly called current' is a trap for the
    honest, because the sentence that records a defect looks like the defect."""
    _edit(repo, REGISTER, lambda s: s.replace(
        "## active_tasks\n",
        "## active_tasks\n\n> This section named `R-017`, then `R-023`/`R-025`, and\n"
        "> each was stale within the commit that wrote it. `last_ledger_seq`\n"
        "> read `1`, then `2`.\n", 1))
    rep = check(repo)
    assert rep.ok, [str(f) for f in rep.findings]


def test_the_findings_record_is_out_of_scope_entirely() -> None:
    """`OPEN_ITEMS_REGISTER.md` records findings and is full of historical
    identifiers by design. Scanning it produced 27 false positives."""
    assert ".ai/project/OPEN_ITEMS_REGISTER.md" not in SCOPE


def test_a_section_that_does_not_govern_is_not_scanned(repo: Path) -> None:
    """Only the two sections whose subject is these values are in scope."""
    _edit(repo, REGISTER, lambda s: s.replace(
        "## compiler_stage\n",
        "## compiler_stage\n\nThe `S-2026-08-12-01` close wrote `L-0000001`.\n", 1))
    assert check(repo).ok
