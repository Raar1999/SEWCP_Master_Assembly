"""`project/STATE_REGISTER.md` may not recite a value another artifact governs.

**Three independent QA rounds found the same defect in this one file.** Round 2
(FIND-11) found `last_ledger_seq` recorded as `1` when the creating session had
written `L-0000002`, and `R-017` named as the exec-layer head when it had been
superseded twice. Round 3 (FIND-1, FIND-2) found the *corrections* to both
stale again — `2` against a live `3`, and `R-023`/`R-025` named as current by
the very commit that superseded them.

That is not three mistakes. It is one **structural** fact: a register drafted
during a session cannot recite a field that the session's own close writes, and
being more careful does not change the ordering. `V-03` cannot see it either —
`mapping_state` is a section-name correspondence and says nothing about
content, which is `OI-V-17`.

So the recitals were removed and this module makes their absence a checked
property rather than a convention. It does **not** ban prose: it requires that
any governed value the register *does* state be live. Adding the value back
correctly is allowed; adding it back wrongly, or letting a correct one go
stale, fails here.

The three governed facts, and who governs each:

  * `last_ledger_seq`  -> `project/ledger/HEAD.seq`, written at the LAW-09 close
  * the exec-layer head -> `aief_exec.graph`, which derives currency from the
                           supersession chain and the pinned digests
  * `HEAD`'s token cost -> measured, and only with the tokenizer artifacts
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

REPO = Path(__file__).resolve().parent.parent
REGISTER = REPO / ".ai/project/STATE_REGISTER.md"
HEAD = REPO / ".ai/project/ledger/HEAD"
STATE = REPO / ".ai/project/STATE.md"


def _register() -> str:
    return REGISTER.read_text(encoding="utf-8")


def _head_seq() -> int:
    return int(re.search(r"^seq:\s*(\d+)", HEAD.read_text(encoding="utf-8"), re.M).group(1))


def _current_result_ids() -> set[str]:
    from aief_exec import graph, records  # noqa: PLC0415

    for fn in ("current_results", "current", "heads"):
        f = getattr(graph, fn, None)
        if callable(f):
            try:
                got = f(REPO)
            except TypeError:
                continue
            return {getattr(r, "result_id", r) for r in got}
    # Fall back to the records themselves: a result is CURRENT iff it says so.
    res = records.load_results(REPO)
    return {rid for rid, r in res.items()
            if str(getattr(r, "status", "")).upper() == "CURRENT"}


def test_the_register_exists_and_is_substantive() -> None:
    """The guard on the guard. A missing or empty register would make every
    assertion below vacuous - and this file was declared in the frozen manifest
    and absent from the tree for four sessions (`TCR-002` F-2, `OI-V-13` FIND-3)."""
    assert REGISTER.is_file()
    text = _register()
    assert len(text) > 3000, "a shell would satisfy V-03 and say nothing (OI-V-17)"
    assert text.count("\n## ") >= 9


def test_the_register_states_no_stale_last_ledger_seq() -> None:
    """Any `last_ledger_seq` value the register states must be the live one."""
    live = _head_seq()
    text = _register()
    claims = [int(m) for m in re.findall(
        r"last_ledger_seq[^\n]{0,80}?`(\d+)`", text)]
    claims += [int(m) for m in re.findall(
        r"`last_ledger_seq`[^\n]{0,80}?\bis (\d+)\b", text)]
    for c in claims:
        assert c == live, (
            f"STATE_REGISTER.md states last_ledger_seq {c}; ledger/HEAD says {live}. "
            "This is the third-recurrence defect - do not correct the number, "
            "remove the recital."
        )


def test_state_md_and_head_agree_on_the_sequence() -> None:
    """The B4 check-3 reconciliation, asserted where a test can see it."""
    declared = int(re.search(r"^last_ledger_seq:\s*(\d+)",
                             STATE.read_text(encoding="utf-8"), re.M).group(1))
    assert declared == _head_seq()


def test_the_register_names_no_superseded_result_as_current() -> None:
    """Any result id the register presents as a current head must be current."""
    text = _register()
    current = _current_result_ids()
    named: set[str] = set()
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        low = sentence.lower()
        if "current head" in low or "heads are" in low or "head of the exec" in low:
            named |= set(re.findall(r"\bR-\d{3}\b", sentence))
    stale = sorted(named - current)
    assert not stale, (
        f"STATE_REGISTER.md names {stale} as a current exec-layer head; "
        f"aief_exec makes the current set {sorted(current)}. Do not correct the "
        "id - the head moves whenever this session publishes a record, which is "
        "why the recital was removed."
    )


def test_the_removal_actually_happened() -> None:
    """The repair itself, pinned. If a future session reinstates a recital it
    must reinstate a correct one, and the two tests above will say so - but the
    reasoning for the removal must survive, or the defect returns by drift."""
    text = _register()
    assert "deliberately not repeated here" in text
    assert "computed, not recited here" in text


def test_the_check_is_sensitive_to_the_defect_it_exists_for(tmp_path) -> None:
    """Adversarial. Reinstating a stale recital must fail, or this module is
    decoration - which is the `OI-V-02` lesson these rounds keep re-teaching."""
    live = _head_seq()
    stale = live - 1
    doctored = _register() + (
        f"\n\n## Notes\n\n`last_ledger_seq` is `{stale}`, reconciled with `HEAD.seq`.\n")
    claims = [int(m) for m in re.findall(
        r"last_ledger_seq[^\n]{0,80}?`(\d+)`", doctored)]
    assert stale in claims, "the pattern must see a reinstated recital at all"
    assert any(c != live for c in claims), "and must judge it stale"


def test_a_superseded_head_would_be_caught(tmp_path) -> None:
    """The same sensitivity check for the exec-layer half."""
    current = _current_result_ids()
    assert current, "no CURRENT result - the assertion below would be vacuous"
    doctored = "The current heads are R-001 and R-002."
    named = set(re.findall(r"\bR-\d{3}\b", doctored))
    assert named - current, "a superseded id in that sentence must be detectable"
