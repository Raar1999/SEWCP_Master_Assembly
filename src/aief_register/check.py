"""No state register may assert, in its own voice, a value another artifact governs.

**Five independent QA rounds found one defect.** `project/STATE_REGISTER.md`
recited `last_ledger_seq` as `1`, then `2`, each written before the session
close that moved it; and named `R-017`, then `R-023`/`R-025`, as the current
exec-layer head, each superseded by the commit that named them. Round 4 found
that the first check written to stop it **did not catch the defect in its own
historical phrasing**. Round 5 found that the *second* one still did not: of
thirteen sequence phrasings it tried, **twelve got through** - including
`last_ledger_seq: 2`, the field's own name, because there is no word boundary
after an underscore.

**Three lessons are built into the rules below, each paid for.**

1. **Do not enumerate phrasings; forbid the value.** A rule that matches
   `seq 2` will be beaten by "the second entry", and a rule that matches both
   will be beaten by "entry two". So a section whose heading *is* a governed
   field name must contain **no numeral at all** - not the live one, not a
   stale one, none. There is nothing to phrase around.
2. **A findings record must be free to quote what a finding was about.** The
   first attempt scanned by keyword window and flagged thirty assertions,
   almost all of them a register *recounting* the defect. A rule that cannot
   tell *"X is current"* from *"X was wrongly called current"* is a trap for
   the honest. So `OPEN_ITEMS_REGISTER.md` is out of scope entirely, and
   within scope a blockquote is a marked account rather than a claim.
3. **Scope by structure, and let it be wide.** Round 5 found that restricting
   the register to two sections left seven governing sections unscanned, and
   that skipping fenced blocks in `STATE.md` exempted the YAML that *is* the
   governed state. Both are closed: every section is scanned, and the fenced
   block is scanned except for its own field lines - a field stating its value
   is the artifact doing its job, not a register reciting someone else's.

The rule, in one line, which is the test of whether it will survive: **outside
a blockquote, an identifier must be the live one; and a section named for a
governed field must state no value at all.**
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

#: Files whose body text speaks for the current state. `STATE.md` is here
#: because round 4 found the recital live in it after it had been removed from
#: the register - the cure had moved the defect rather than ended it.
#: `OPEN_ITEMS_REGISTER.md` is deliberately ABSENT; see lesson 2.
SCOPE: tuple[str, ...] = (
    ".ai/project/STATE.md",
    ".ai/project/STATE_REGISTER.md",
)

#: Sections whose heading is a governed field name. Inside these, no numeral.
VALUE_FREE_SECTIONS = ("last_ledger_seq",)

_LEDGER_ID = re.compile(r"\bL-?0*(\d{1,7})\b")
_RESULT_ID = re.compile(r"\bR-(\d{3})\b")
#: Any standalone small number, for the value-free sections.
#: A trailing period ends a sentence; only a following DIGIT means a decimal.
#: Round 5 phrasings "The sequence is 2." and "entry number 2." both evaded a
#: lookahead that treated any following period as part of a number.
_NUMERAL = re.compile(r"(?<![\w\-/])(?<!\d\.)(\d{1,3})(?![\w\-/%])(?!\.\d)")
_WORD_NUMBER = re.compile(
    r"\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|last)\b",
    re.I)
#: Inside a fenced block, ONLY a governed field stating its own value is exempt.
#: Exempting every field line let a stale id ride in on any other key - round 5
#: put `stale_note: see L-0000002` into the YAML and nothing looked.
_GOVERNED_FIELD = re.compile(r"^\s*(last_ledger_seq|seq)\s*:", re.I)


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


def scan_lines(text: str):
    """Yield `(line-number, line, section)` for text asserted in the file's own voice.

    Headings are yielded, because round 5 put a stale id in one and nothing
    looked. Blockquotes are dropped - they are the marked account of what a
    value once wrongly said. Inside a fenced block only non-field lines are
    yielded: `last_ledger_seq: 5` is the artifact stating its own governed
    value, which is its job, while prose in a fence is still prose.
    """
    section: str | None = None
    fenced = False
    for i, line in enumerate(text.split("\n"), start=1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced and _GOVERNED_FIELD.match(line):
            continue
        if line.lstrip().startswith(">"):
            continue
        if line.startswith("## "):
            section = line[3:].strip()
        yield i, line, section


def check(repo: Path) -> Report:
    rep = Report(ledger_seq=ledger_seq(repo), current_results=current_results(repo))
    live = rep.ledger_seq

    for rel in SCOPE:
        p = repo / rel
        if not p.is_file():
            continue
        rep.scanned.append(rel)

        for lineno, line, section in scan_lines(p.read_text(encoding="utf-8")):
            excerpt = " ".join(line.split())[:130]

            for m in _LEDGER_ID.finditer(line):
                if int(m.group(1)) != live:
                    rep.findings.append(Finding(
                        rel, lineno, "a ledger entry named in the file's own voice",
                        f"L-{int(m.group(1)):07d}", f"L-{live:07d}", excerpt))

            for m in _RESULT_ID.finditer(line):
                rid = f"R-{m.group(1)}"
                if rid not in rep.current_results:
                    rep.findings.append(Finding(
                        rel, lineno, "a superseded result named in the file's own voice",
                        rid, "/".join(sorted(rep.current_results)) or "none", excerpt))

            if section in VALUE_FREE_SECTIONS and not line.startswith("## "):
                for m in _NUMERAL.finditer(line):
                    rep.findings.append(Finding(
                        rel, lineno,
                        f"a numeral in the value-free section '{section}'",
                        m.group(1), "state no value here at all", excerpt))
                for m in _WORD_NUMBER.finditer(line):
                    rep.findings.append(Finding(
                        rel, lineno,
                        f"a written number in the value-free section '{section}'",
                        m.group(1), "state no value here at all", excerpt))

    return rep
