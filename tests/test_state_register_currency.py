"""No state register may assert, in its own voice, a value another artifact governs.

**Five independent rounds found one defect, and two checks written to end it
did not.** Round 4 found the first: a line-scoped regex against a defect whose
phrasing spans lines. Round 5 found the second: of **thirteen** sequence
phrasings it constructed, **twelve got through** - including
`last_ledger_seq: 2`, the field's own name.

Round 5 also named the reason the tests did not notice, and it is the reason
this file is written the way it is: **`test_..._verbatim_is_caught` injected a
line `seq 2` that never existed in the register, and passed only because of
it.** A test that feeds the pattern a string built for the pattern proves
nothing. So every phrasing below is one that **round 5 actually ran against the
live check and got past it**, transcribed from its report - not invented here.

The rule that replaced the patterns is structural, and the parametrised lists
are its proof: a section named for a governed field may contain **no numeral
and no written number**, so there is no phrasing to find.
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

from aief_register.check import (  # noqa: E402
    SCOPE,
    VALUE_FREE_SECTIONS,
    check,
    current_results,
    ledger_seq,
)

REPO = Path(__file__).resolve().parent.parent
REGISTER = ".ai/project/STATE_REGISTER.md"
STATE = ".ai/project/STATE.md"

#: Every sequence phrasing round 5 ran against the previous check. It caught
#: one of thirteen. Transcribed from the round's report, not invented.
ROUND_5_SEQUENCE_EVASIONS = [
    "the second entry",
    "entry two",
    "the close before last",
    "`2`",
    "The sequence is 2.",
    "L0000002",
    "last_ledger_seq: 2",
    "`2`, reconciled with `HEAD.seq`.",
    "The head entry is `L-0000002`.",
    "It stands at two.",
    "seq 2",
    "2",
    "The ledger is at entry number 2.",
]

#: Every exec-head phrasing rounds 4 and 5 ran. The first check caught two.
ROUND_5_HEAD_EVASIONS = [
    "The head is `R-025`.",
    "`R-025` is current.",
    "The record of record is `R-023`.",
    "The record pinning `src/aief_exec/**` is `R-023`.",
    "Currently at the head: `R-025`.",
    "The unsuperseded results are `R-021`, `R-023` and `R-025`.",
    "the result superseding R-014",
    "R-017",
]

#: Round 5: 7 of 9 governing sections were unscanned, so a stale assertion in
#: any of them was invisible.
GOVERNING_SECTIONS = [
    "blockers", "compiler_stage", "frozen_set_hash", "next_action",
    "active_gate", "lifecycle_stage", "open_non_blocking", "Notes",
]


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


def _inject(root: Path, rel: str, section: str, payload: str) -> None:
    p = root / rel
    text = p.read_text(encoding="utf-8")
    assert f"## {section}\n" in text, section
    p.write_text(text.replace(f"## {section}\n", f"## {section}\n\n{payload}\n", 1),
                 encoding="utf-8", newline="\n")


# -- the live tree ---------------------------------------------------------

def test_the_live_registers_assert_nothing_governed() -> None:
    rep = check(REPO)
    assert rep.ok, "\n".join(str(f) for f in rep.findings)
    assert rep.scanned == list(SCOPE)


def test_state_md_and_head_agree_on_the_sequence() -> None:
    declared = int(re.search(r"^last_ledger_seq:\s*(\d+)",
                             (REPO / STATE).read_text(encoding="utf-8"), re.M).group(1))
    assert declared == ledger_seq(REPO)


def test_there_is_something_to_check() -> None:
    assert current_results(REPO)
    assert ledger_seq(REPO) >= 1
    assert VALUE_FREE_SECTIONS


# -- every phrasing that beat the previous check ---------------------------

@pytest.mark.parametrize("phrasing", ROUND_5_SEQUENCE_EVASIONS)
def test_every_sequence_phrasing_round_5_got_past_is_caught(repo: Path, phrasing: str) -> None:
    """Round 5 caught 1 of these 13. All 13 must fail now.

    None is invented: each is transcribed from the round's report, which is the
    difference between this module and the one it replaces.
    """
    _inject(repo, REGISTER, "last_ledger_seq", phrasing)
    assert not check(repo).ok, phrasing


@pytest.mark.parametrize("phrasing", ROUND_5_HEAD_EVASIONS)
def test_every_head_phrasing_the_rounds_got_past_is_caught(repo: Path, phrasing: str) -> None:
    _inject(repo, REGISTER, "active_tasks", phrasing)
    assert not check(repo).ok, phrasing


@pytest.mark.parametrize("section", GOVERNING_SECTIONS)
def test_a_stale_head_in_any_governing_section_is_caught(repo: Path, section: str) -> None:
    """Round 5: restricting scope to two sections left seven unscanned."""
    _inject(repo, REGISTER, section, "The current head is `R-017`.")
    assert not check(repo).ok, section


def test_a_stale_id_inside_the_fenced_yaml_is_caught(repo: Path) -> None:
    """Round 5: the fenced block was skipped entirely, and in `STATE.md` that
    block IS the governed state. Only a governed field stating its own value is
    exempt now."""
    p = repo / STATE
    t = p.read_text(encoding="utf-8")
    seq = ledger_seq(repo)
    p.write_text(t.replace(f"last_ledger_seq:  {seq}",
                           f"last_ledger_seq:  {seq}\n  stale_note:     see L-0000002"),
                 encoding="utf-8", newline="\n")
    assert not check(repo).ok


def test_a_stale_id_in_a_heading_is_caught(repo: Path) -> None:
    """Headings were never scanned."""
    _inject(repo, REGISTER, "active_tasks", "### The head, `R-017`")
    assert not check(repo).ok


# -- and it must not punish the record for being honest --------------------

def test_a_blockquote_recounting_the_defect_is_not_a_finding(repo: Path) -> None:
    """The first attempt flagged thirty assertions, almost all of them a
    register *recording* the defect. A rule that cannot tell 'X is current'
    from 'X was wrongly called current' is a trap for the honest."""
    _inject(repo, REGISTER, "active_tasks",
            "> This section named `R-017`, then `R-023`/`R-025`, each stale within\n"
            "> the commit that wrote it, and `last_ledger_seq` read `1`, then `2`.")
    rep = check(repo)
    assert rep.ok, [str(f) for f in rep.findings]


def test_the_findings_record_is_out_of_scope_entirely() -> None:
    """`OPEN_ITEMS_REGISTER.md` records findings and must be free to quote what
    a finding was about. Scanning it produced 27 false positives."""
    assert ".ai/project/OPEN_ITEMS_REGISTER.md" not in SCOPE


def test_the_governed_field_may_state_its_own_value(repo: Path) -> None:
    """`STATE.md`'s own `last_ledger_seq:` line is the artifact doing its job,
    not a register reciting someone else's value. It must not be flagged."""
    assert check(repo).ok
    assert re.search(r"^last_ledger_seq:\s*\d+",
                     (repo / STATE).read_text(encoding="utf-8"), re.M)


# -- the check's own machinery, mutated ------------------------------------

@pytest.mark.parametrize("mutation", [
    "no_scan", "no_files", "no_value_free", "no_ledger_rule", "no_result_rule",
])
def test_disabling_any_rule_blinds_the_check(repo: Path, mutation: str) -> None:
    """Each structural rule is pinned by disabling it and requiring the check to
    go blind on a defect it otherwise catches. If a rule can be removed with no
    effect, it was not the rule doing the work - which is how round 5's three
    surviving mutations were all lexical."""
    import importlib

    mod = importlib.import_module("aief_register.check")
    saved = (mod.SCOPE, mod.VALUE_FREE_SECTIONS, mod._LEDGER_ID, mod._RESULT_ID)
    _inject(repo, REGISTER, "last_ledger_seq", "entry two")
    _inject(repo, REGISTER, "active_tasks", "The head is `R-025`.")
    assert not check(repo).ok, "the fixture must be defective before it is blinded"
    try:
        if mutation == "no_scan":
            mod.SCOPE = ()
        elif mutation == "no_files":
            mod.SCOPE = (".ai/project/nonexistent.md",)
        elif mutation == "no_value_free":
            mod.VALUE_FREE_SECTIONS = ()
            mod._RESULT_ID = re.compile(r"(?!x)x")
        elif mutation == "no_ledger_rule":
            mod.VALUE_FREE_SECTIONS = ()
            mod._RESULT_ID = re.compile(r"(?!x)x")
            mod._LEDGER_ID = re.compile(r"(?!x)x")
        elif mutation == "no_result_rule":
            mod.VALUE_FREE_SECTIONS = ()
            mod._RESULT_ID = re.compile(r"(?!x)x")
            mod._LEDGER_ID = re.compile(r"(?!x)x")
        assert check(repo).ok, (
            f"mutation {mutation!r} did not blind the check - the rule it "
            "disables is not the rule doing the work"
        )
    finally:
        mod.SCOPE, mod.VALUE_FREE_SECTIONS, mod._LEDGER_ID, mod._RESULT_ID = saved


def test_removing_the_blockquote_exemption_breaks_the_converse(repo: Path) -> None:
    """The exemption is load-bearing in the other direction: without it, a
    register recounting the defect is flagged, which is the trap this rule was
    redesigned to avoid."""
    import importlib

    mod = importlib.import_module("aief_register.check")
    _inject(repo, REGISTER, "active_tasks",
            "> historical: `R-017` was once called the head.")
    assert check(repo).ok
    original = mod.scan_lines

    def no_skip(text):
        section = None
        fenced = False
        for i, line in enumerate(text.split(chr(10)), start=1):
            if line.lstrip().startswith("```"):
                fenced = not fenced
                continue
            if line.startswith("## "):
                section = line[3:].strip()
            yield i, line, section

    try:
        mod.scan_lines = no_skip
        assert not check(repo).ok, (
            "without the blockquote exemption the honest record is flagged"
        )
    finally:
        mod.scan_lines = original
