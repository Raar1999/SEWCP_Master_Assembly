"""No state register may assert, in its own voice, a value another artifact governs.

**Four independent QA rounds found one defect.** `project/STATE_REGISTER.md`
recited `last_ledger_seq` as `1`, then `2`, each written before the session
close that moved it; and named `R-017`, then `R-023`/`R-025`, as the current
exec-layer head, each superseded by the commit that named them. Round 4 then
found that the check written to stop it **did not catch the defect in its own
historical phrasing** - the pattern was line-scoped and the real wording put
the heading and the value two lines apart - and that the same recital was still
live in `project/STATE.md`, the governing file.

**Why a keyword window over prose was the wrong instrument.** The first attempt
at this scanned for identifiers near words like "current". It flagged thirty
assertions, and almost all were the open-items register *recounting the defect*
- "`R-017` named as the exec-layer head when the heads are …". A rule that
cannot tell *"X is current"* from *"X was wrongly called current"* is not a
rule; it is a trap for the honest, because the sentence that records a defect
looks exactly like the defect.

**So the scope is structural, not lexical.** Two things carry it:

1. **Only the sections that govern.** `STATE.md` speaks for the project's
   current state everywhere, so all of it is in scope. In `STATE_REGISTER.md`
   only the two sections whose subject is these values are - and the
   open-items register, which is a record of findings and is full of historical
   identifiers by design, is not scanned at all.
2. **A blockquote is marked history.** Every explanatory note in these files
   is already written as `>`, and a `>` line says "this is the account, not the
   claim". Body text speaks in the register's own voice; quoted text does not.

The rule is then simple enough to state in one line, which is the test of
whether it will survive: **outside a blockquote, in a section that governs, an
identifier must be the live one.**
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

#: Files whose body text speaks for the current state. `STATE.md` is here
#: because round 4 found the recital live in it after it had been removed from
#: the register - the cure had moved the defect rather than ended it.
#: `OPEN_ITEMS_REGISTER.md` is deliberately ABSENT: it records findings, and
#: a findings record must be free to quote the values a finding was about.
SCOPE: dict[str, tuple[str, ...] | None] = {
    ".ai/project/STATE.md": None,                       # None = the whole file
    ".ai/project/STATE_REGISTER.md": ("last_ledger_seq", "active_tasks"),
}

_LEDGER_ID = re.compile(r"\bL-(\d{7})\b")
_RESULT_ID = re.compile(r"\bR-(\d{3})\b")
#: `seq 2`, `seq: 2`, `seq is 2`, `` seq `2` `` - the forms the defect took.
_SEQ_VALUE = re.compile(r"\bseq\b\W{0,6}`?(\d{1,3})`?", re.I)


@dataclass
class Finding:
    path: str
    line: int
    kind: str
    stated: str
    governing: str
    excerpt: str

    def __str__(self) -> str:
        return (f"{self.path}:{self.line}  {self.kind}\n"
                f"      states     {self.stated}\n"
                f"      governing  {self.governing}\n"
                f"      {self.excerpt}")


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    scanned: list[str] = field(default_factory=list)
    ledger_seq: int = 0
    current_results: set[str] = field(default_factory=set)

    @property
    def ok(self) -> bool:
        return not self.findings


def ledger_seq(repo: Path) -> int:
    head = (repo / ".ai/project/ledger/HEAD").read_text(encoding="utf-8")
    return int(re.search(r"^seq:\s*(\d+)", head, re.M).group(1))


def current_results(repo: Path) -> set[str]:
    import sys

    src = str(repo / "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    from aief_exec import records  # noqa: PLC0415

    return {rid for rid, r in records.load_results(repo).items()
            if str(getattr(r, "status", "")).upper() == "CURRENT"}


def _in_scope_lines(text: str, sections: tuple[str, ...] | None):
    """(line-number, line) for body text this file asserts in its own voice.

    Blockquotes are dropped - they are the marked account of what a value once
    wrongly said, and a rule that flagged them would punish the record for
    being honest. Fenced code is dropped for the same reason a schema example
    is not a claim.
    """
    current: str | None = None
    fenced = False
    for i, line in enumerate(text.split("\n"), start=1):
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("## "):
            current = line[3:].strip()
            continue
        if line.lstrip().startswith(">"):
            continue
        if sections is not None and current not in sections:
            continue
        yield i, line


def check(repo: Path) -> Report:
    rep = Report(ledger_seq=ledger_seq(repo), current_results=current_results(repo))
    live = rep.ledger_seq

    for rel, sections in SCOPE.items():
        p = repo / rel
        if not p.is_file():
            continue
        rep.scanned.append(rel)
        text = p.read_text(encoding="utf-8")

        for lineno, line in _in_scope_lines(text, sections):
            excerpt = " ".join(line.split())[:130]

            for m in _LEDGER_ID.finditer(line):
                if int(m.group(1)) != live:
                    rep.findings.append(Finding(
                        rel, lineno, "a ledger entry named in the register's own voice",
                        f"L-{m.group(1)}", f"L-{live:07d}", excerpt))

            for m in _SEQ_VALUE.finditer(line):
                if int(m.group(1)) != live:
                    rep.findings.append(Finding(
                        rel, lineno, "a ledger sequence stated in the register's own voice",
                        m.group(1), str(live), excerpt))

            for m in _RESULT_ID.finditer(line):
                rid = f"R-{m.group(1)}"
                if rid not in rep.current_results:
                    rep.findings.append(Finding(
                        rel, lineno, "a superseded result named in the register's own voice",
                        rid, "/".join(sorted(rep.current_results)) or "none", excerpt))

    return rep
