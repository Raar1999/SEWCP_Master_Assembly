"""Record parsing: the bounded index, task records and result records.

Actor provenance: software.software-engineer - S-2026-08-09-01.

Implements EXECUTION_ARCHITECTURE.md sections 4, 5 and 6.

No YAML library is available in this environment and the repository declares no
such dependency, so this module implements a **restricted subset** of the block
grammar the repository already uses in STATE.md, BINDING.md and ledger/HEAD.
The parser raises `RecordError` on anything outside that subset rather than
guessing - LAW-12: assumption is never a resolution method.

Supported: nested mappings by indentation, block sequences, flow sequences
`[a, b]`, flow mappings `{k: v}`, literal block scalars `|`, quoted scalars,
`null`/`true`/`false`/integers, and `#` comments outside quotes.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aief_stage6.digests import dc1_digest

TASK_ID = re.compile(r"^T-\d{3}$")
RESULT_ID = re.compile(r"^R-\d{3}$")
SESSION_ID = re.compile(r"^S-\d{4}-\d{2}-\d{2}-\d{2}$")

#: SCH-task.schema.json `required` - the eight fields the schema mandates.
SCH_TASK_REQUIRED = (
    "task_id",
    "role",
    "objective",
    "inputs",
    "deliverable",
    "acceptance_criteria",
    "forbidden_actions",
    "escalation",
)

#: EXECUTION_ARCHITECTURE.md section 5 - the extension fields carried under
#: SCH-task's `additionalProperties: true`.
EXTENSION_REQUIRED = (
    "status",
    "read_scope",
    "write_scope",
    "qa",
    "checkpoint",
)


class RecordError(ValueError):
    """A record does not conform to the declared grammar or contract."""


# --------------------------------------------------------------------------
# Restricted block-mapping parser
# --------------------------------------------------------------------------

def _strip_comment(line: str) -> str:
    """Remove a trailing `#` comment that is not inside quotes."""
    out = []
    quote = None
    for i, ch in enumerate(line):
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "'\"":
            quote = ch
            out.append(ch)
            continue
        if ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _scalar(raw: str) -> Any:
    """Parse a scalar. Flow collections are handled here so that a value may be
    written inline, as STATE.md and BINDING.md already do."""
    text = raw.strip()
    if text == "" or text in ("null", "~"):
        return None
    if text == "true":
        return True
    if text == "false":
        return False
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "'\"":
        return text[1:-1]
    if text.startswith("[") and text.endswith("]"):
        return [_scalar(p) for p in _split_flow(text[1:-1])] if text[1:-1].strip() else []
    if text.startswith("{") and text.endswith("}"):
        body = text[1:-1].strip()
        if not body:
            return {}
        out: dict[str, Any] = {}
        for part in _split_flow(body):
            if ":" not in part:
                raise RecordError(f"flow mapping entry without ':': {part!r}")
            k, _, v = part.partition(":")
            put(out, k, _scalar(v), f"flow mapping {body!r}")
        return out
    # JSON's number grammar: no leading zeros. A token like an all-digit SHA-256
    # digest, a zero-padded id or a segment name is an identifier, not an integer,
    # and must survive as text.
    if re.fullmatch(r"-?(0|[1-9]\d*)", text):
        return int(text)
    return text


def _split_flow(body: str) -> list[str]:
    """Split a flow collection body on top-level commas."""
    parts, depth, quote, cur = [], 0, None, []
    for ch in body:
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "'\"":
            quote = ch
            cur.append(ch)
            continue
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
            continue
        cur.append(ch)
    if cur:
        parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


#: Every character that is whitespace but is **not** the space the block grammar
#: is defined in terms of. `VER-013` L6-3: the first form of `_indent` rejected
#: `\t` alone, so U+00A0, `\v`, `\f`, U+2007, U+200B and the rest each survived
#: `lstrip(" ")`, failed the `\t` test, yielded indent 0 and reproduced L5-B's
#: exact parse - child hoisted to top level, parent key silently `None`. U+00A0
#: is invisible in every editor and is a routine copy-paste artifact.
#:
#: Rejecting one character of a class is the enumeration error this whole repair
#: exists to stop, committed inside the repair. The class is rejected.
#: Unicode general categories that are separators, controls or invisible format
#: characters. `\s` is not enough: U+200B ZERO WIDTH SPACE and U+FEFF are `Cf`,
#: not whitespace, so a `\s`-based rule admitted them and they hoisted the line
#: exactly as a tab did. Enumerating characters was the first mistake here and
#: enumerating a *regex class* was the second; the property is what matters.
AMBIGUOUS_INDENT_CATEGORIES = frozenset({"Zs", "Zl", "Zp", "Cc", "Cf"})


def _is_ambiguous_indent(ch: str) -> bool:
    return unicodedata.category(ch) in AMBIGUOUS_INDENT_CATEGORIES


def put(out: dict[str, Any], key: str, value: Any, where: str) -> None:
    """**The one insertion point for every mapping this parser builds.**

    `VER-013` L6-1, L6-2, L6-4. The duplicate-key guard was added to
    `_parse_map` only, so the *other three* mapping-construction sites - flow
    mappings, the inline first key of a sequence item, and the `entry.update()`
    that merges its siblings - still resolved a duplicate by last-wins, in
    silence. One of them, the flow mapping, is the syntax this repair's own
    regression suite certifies as the lawful control, and a duplicate `digest:`
    inside it rewrote a superseded record at `X-06 PASS` for **one edit in one
    file** - the cheapest attack in the whole history.

    Guarding one site per kind is the same enumeration error as guarding one
    interpretation site per kind, one level up. There is one site now and every
    construction path goes through it, so a fourth path cannot be added without
    passing through the guard.

    Keys are normalised before comparison: `'k':` and `k:` are one key, because
    they are one key to a reader. `VER-013` L6-4 recorded them resolving as two.
    """
    k = _scalar(key) if key[:1] in ("'", '"') else key
    k = str(k).strip()
    if k in out:
        raise RecordError(
            f"{where}: duplicate key {k!r}. The document declares it more than "
            f"once, so which declaration governs is undefined and choosing one "
            f"is a tie-break, not a reading (LAW-12). A reader of the file and "
            f"a reader of the parse would disagree. Repair: delete the "
            f"declaration that does not govern"
        )
    out[k] = value


def _indent(line: str) -> int:
    """Indentation depth in spaces. **Any other whitespace is a parse error.**

    `VER-012` L5-B. This counted spaces only, so a tab-indented child line had
    depth 0: it hoisted itself to top level and its parent key silently became
    `None`. Two whitespace-only edits to a record - no line deleted, no value
    changed - restructured the document and rewrote a superseded result at
    `X-06 PASS`.

    A tab's width is a display convention, not a fact about the document, so
    there is no correct number to return here. Returning one would be the
    assumption LAW-12 forbids, and returning zero was the one that produced the
    defect. The line is rejected instead.
    """
    stripped = line.lstrip(" ")
    if stripped and _is_ambiguous_indent(stripped[0]):
        raise RecordError(
            f"indentation character {stripped[0]!r} (U+{ord(stripped[0]):04X}) "
            f"is not the space this block grammar is defined in terms of and "
            f"has no defined width, so the nesting this line declares is "
            f"ambiguous (LAW-12): {line!r}. Repair: indent with spaces"
        )
    return len(line) - len(stripped)


def parse_block(text: str) -> dict[str, Any]:
    """Parse the restricted block grammar into a dict."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    value, consumed = _parse_map(lines, 0, 0)
    # Trailing blank or comment lines are permitted.
    for line in lines[consumed:]:
        if _strip_comment(line).strip():
            raise RecordError(f"unparsed trailing content: {line!r}")
    return value


def _skip(lines: list[str], i: int) -> int:
    while i < len(lines) and not _strip_comment(lines[i]).strip():
        i += 1
    return i


def _parse_map(lines: list[str], i: int, level: int) -> tuple[dict[str, Any], int]:
    out: dict[str, Any] = {}
    while True:
        i = _skip(lines, i)
        if i >= len(lines):
            return out, i
        raw = lines[i]
        stripped = _strip_comment(raw)
        if not stripped.strip():
            i += 1
            continue
        ind = _indent(raw)
        if ind < level:
            return out, i
        if ind > level:
            raise RecordError(f"unexpected indent at line {i + 1}: {raw!r}")
        body = stripped.strip()
        if body.startswith("- "):
            return out, i
        if ":" not in body:
            raise RecordError(f"line {i + 1} is not a mapping entry: {raw!r}")
        key, _, rest = body.partition(":")
        key = key.strip()
        rest = rest.strip()
        # `VER-012` L5-A. This was `out[key] = ...` with no duplicate check, so a
        # document declaring the same key twice had two meanings and the parser
        # picked one - the last - without saying so. That is precisely the
        # resolution-by-assumption LAW-12 forbids, and the meaning it picked
        # satisfied every check: appending a second `supersedes_seal` block
        # carrying a tampered digest to a successor rewrote its predecessor with
        # X-06 PASS and detail AND notice sets byte-identical to a clean run,
        # while the file still displayed the correct digest to a human reader.
        #
        # A document that says a thing twice is not a document that says it
        # once. Which of the two a reader believes is exactly the ambiguity this
        # parser's contract says it will refuse to resolve.
        i += 1
        if rest == "|":
            block, i = _parse_literal(lines, i, level)
            put(out, key, block, f"line {i}")
        elif rest:
            put(out, key, _scalar(rest), f"line {i}")
        else:
            j = _skip(lines, i)
            if j < len(lines) and _indent(lines[j]) > level:
                child_ind = _indent(lines[j])
                if _strip_comment(lines[j]).strip().startswith("- "):
                    sub, i = _parse_seq(lines, j, child_ind)
                else:
                    sub, i = _parse_map(lines, j, child_ind)
                put(out, key, sub, f"line {i}")
            else:
                put(out, key, None, f"line {i}")
                i = j
    return out, i


def _parse_seq(lines: list[str], i: int, level: int) -> tuple[list[Any], int]:
    out: list[Any] = []
    while True:
        i = _skip(lines, i)
        if i >= len(lines):
            return out, i
        raw = lines[i]
        ind = _indent(raw)
        if ind < level:
            return out, i
        body = _strip_comment(raw).strip()
        if not body.startswith("- "):
            if ind == level:
                return out, i
            raise RecordError(f"line {i + 1} is not a sequence item: {raw!r}")
        item = body[2:].strip()
        i += 1
        if ":" in item and not item.startswith(("[", "{", "'", '"')):
            # Inline first key of a mapping item; its siblings are indented to
            # the column where that key started.
            key, _, rest = item.partition(":")
            entry: dict[str, Any] = {}
            child_level = ind + 2
            if rest.strip():
                put(entry, key, _scalar(rest), f"line {i}")
            else:
                j = _skip(lines, i)
                if j < len(lines) and _indent(lines[j]) > child_level - 1:
                    sub, i = _parse_map(lines, j, _indent(lines[j]))
                    put(entry, key, sub, f"line {i}")
                else:
                    put(entry, key, None, f"line {i}")
            j = _skip(lines, i)
            while j < len(lines) and _indent(lines[j]) == child_level:
                nxt = _strip_comment(lines[j]).strip()
                if nxt.startswith("- "):
                    break
                more, i = _parse_map(lines, j, child_level)
                for mk, mv in more.items():
                    put(entry, mk, mv, f"line {i} (sequence item)")
                j = _skip(lines, i)
            out.append(entry)
        else:
            out.append(_scalar(item))
    return out, i


def _parse_literal(lines: list[str], i: int, level: int) -> tuple[str, int]:
    body: list[str] = []
    inner = None
    while i < len(lines):
        raw = lines[i]
        if not raw.strip():
            body.append("")
            i += 1
            continue
        ind = _indent(raw)
        if ind <= level:
            break
        if inner is None:
            inner = ind
        body.append(raw[inner:])
        i += 1
    while body and body[-1] == "":
        body.pop()
    return "\n".join(body) + "\n", i


def extract_fence(text: str, lang: str = "yaml") -> str:
    """Return **the** fenced block of the given language.

    `VER-012` L5-E. This returned the **first** match, so a decoy fence inserted
    above a record's real block was parsed instead of it and the real block was
    never read - `X-06 PASS`, detail and notice sets byte-identical to a clean
    run. "First" is a tie-break, and a tie-break is an assumption about which of
    two documents the author meant (LAW-12).

    A record carries one document. Two is ambiguous and is rejected.
    """
    body = text.replace("\r\n", "\n")
    pattern = re.compile(r"^```" + lang + r"\s*$(.*?)^```\s*$", re.M | re.S)
    found = pattern.findall(body)
    if not found:
        raise RecordError(f"no ```{lang} block found")
    if len(found) > 1:
        raise RecordError(
            f"{len(found)} ```{lang} blocks found; a record carries exactly "
            f"one. Which document governs is undefined and taking the first is "
            f"a tie-break, not a reading (LAW-12). Repair: remove the blocks "
            f"that are not the record"
        )
    return found[0]


# --------------------------------------------------------------------------
# Records
# --------------------------------------------------------------------------

def _check_shapes(
    rid: str, data: dict[str, Any], shapes: tuple[tuple[str, str], ...]
) -> None:
    """Reject a structurally malformed record. One function, both record classes.

    `VER-013`. Shape is well-formedness; *content* - which fields must be
    present and what they must say - is `EXECUTION_ARCHITECTURE.md` §5 and §6,
    enforced by `X-01` and `X-06`. Restating those field lists here would be the
    second declaration `FIND-Q9-44` was raised about, so this table says only
    what KIND of thing each field is when it is present.

    `mapping`  - a mapping.
    `mappings` - a sequence whose every element is a mapping.
    `sequence` - a sequence. A bare string is the dangerous case: it is
                 iterable, so a coercing consumer silently reads it as a list of
                 characters (`write_scope: not-a-list` became ten one-character
                 patterns).
    `scalar`   - not a collection.
    """
    for name, shape in shapes:
        v = data.get(name)
        if v is None:
            continue
        bad = (
            (shape == "mapping" and not isinstance(v, dict))
            or (shape in ("mappings", "sequence") and not isinstance(v, list))
            or (shape == "scalar" and isinstance(v, (dict, list)))
        )
        if bad:
            raise RecordError(
                f"{rid}: {name} is {type(v).__name__}, not a {shape}. It is "
                f"declared and cannot be read as declared, which is not the "
                f"same as absent and must not be silently treated as absent "
                f"(VER-012/013)"
            )
        if shape == "mappings":
            for n, entry in enumerate(v):
                if not isinstance(entry, dict):
                    raise RecordError(
                        f"{rid}: {name}[{n}] is {type(entry).__name__}, not a "
                        f"mapping. A malformed entry used to be dropped from "
                        f"the set in silence (VER-012/013)"
                    )


@dataclass
class TaskRecord:
    task_id: str
    path: str
    data: dict[str, Any]

    #: `VER-013` L6-6. The result record got an admission gate and the task
    #: record did not, so `read_entries` kept the exact
    #: `[e for e in ... if isinstance(e, dict)]` pattern that
    #: `ResultRecord.validate_shape`'s docstring names as the mechanism. On the
    #: live `T-001`, replacing one `- path:` mapping with a bare scalar dropped
    #: it silently - six entries became five, `X-01` and `X-03` both PASS,
    #: nothing named it - and moved `acquisition`, the quantity the `X-08`
    #: dispatch gate is a function of, from TF-1 6744 to 6436.
    #:
    #: Guarding one record class is the enumeration error again. Both are
    #: guarded, by the same function.
    SHAPES: tuple[tuple[str, str], ...] = (
        ("read_scope", "mapping"),
        ("qa", "mapping"),
        ("checkpoint", "mapping"),
        ("acceptance_criteria", "mappings"),
        ("write_scope", "sequence"),
        ("depends_on", "sequence"),
        ("consumes", "sequence"),
        ("produces", "sequence"),
        ("blocked_by", "sequence"),
        ("deliverable", "sequence"),
        ("inputs", "sequence"),
        ("forbidden_actions", "sequence"),
        ("status", "scalar"),
        ("role", "scalar"),
        ("task_id", "scalar"),
    )

    def validate_shape(self) -> None:
        _check_shapes(self.task_id, self.data, self.SHAPES)

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    @property
    def status(self) -> str:
        return str(self.data.get("status") or "")

    @property
    def depends_on(self) -> list[str]:
        return list(self.data.get("depends_on") or [])

    @property
    def consumes(self) -> list[str]:
        return list(self.data.get("consumes") or [])

    @property
    def produces(self) -> list[str]:
        return list(self.data.get("produces") or [])

    @property
    def blocked_by(self) -> list[str]:
        return list(self.data.get("blocked_by") or [])

    @property
    def write_scope(self) -> list[str]:
        return list(self.data.get("write_scope") or [])

    @property
    def observes(self) -> list[str]:
        """The optional declared extension to the derived observation surface.

        A task's *observation surface* is the tree state it must observe stably
        for its acceptance criteria to hold - the evidence it takes, as opposed
        to the paths it reads as input or writes as output. Most of that surface
        is derivable (`graph.observed_surface`); this field exists for the part
        that is not, so a task can name a tree it watches without pretending to
        write it or to read it as an input.

        Absent from `SCH_TASK_REQUIRED` and from `EXTENSION_REQUIRED` on purpose:
        it is an extension a record may carry, not one every record must.
        """
        return [str(p).strip() for p in (self.data.get("observes") or []) if str(p).strip()]

    @property
    def result_paths(self) -> list[str]:
        """The `.ai/project/results/R-nnn.md` path implied by each `produces` entry.

        **Derived and reported only.** Whether declaring `produces: R` carries an
        implicit grant to write `R`'s record is an open architecture decision
        (A4) and this property does not settle it: it computes where the record
        would have to go, nothing more. `X-04` continues to test the **declared**
        `write_scope` alone, and `X-09` reports the gap between the two rather
        than closing it by assumption - LAW-12.

        Positionally aligned with `produces`, so the two may be zipped.
        """
        from aief_exec import RESULTS_DIR
        return [f"{RESULTS_DIR}/{rid}.md" for rid in self.produces]

    @property
    def effective_write_scope(self) -> list[str]:
        """`write_scope` union `result_paths` - **displayed, never enforced.**

        The set a task would need in order to publish everything it declares. It
        is printed by `aief_exec scope` labelled derived-not-granted so the gap
        is visible; no check compares anything against it, because doing so would
        pre-empt A4.

        A union over *paths*, not over pattern strings: a result path already
        matched by a declared pattern is already in the set and adds no pattern
        to it. `T-001` declares `.ai/project/results/**` and four `produces`, and
        its effective scope is therefore its declared scope - the gap is zero,
        which is the answer, not a rounding of it.
        """
        from aief_exec import scope as _scope
        out = list(self.write_scope)
        for rel in self.result_paths:
            if rel in out:
                continue
            if any(_scope.glob_to_regex(p).match(rel) for p in self.write_scope):
                continue
            out.append(rel)
        return out

    def read_entries(self, kind: str) -> list[dict[str, Any]]:
        """`kind` in mandatory | optional | dependency."""
        rs = self.data.get("read_scope") or {}
        entries = rs.get(kind) or []
        return [e for e in entries if isinstance(e, dict)]

    @property
    def forbidden_reads(self) -> list[str]:
        rs = self.data.get("read_scope") or {}
        return list(rs.get("forbidden") or [])

    @property
    def checkpoint(self) -> dict[str, Any]:
        return dict(self.data.get("checkpoint") or {})


@dataclass
class ResultRecord:
    result_id: str
    path: str
    data: dict[str, Any]

    #: The **shape** of every structured field, checked once at admission.
    #:
    #: `VER-012`. Shape is well-formedness and belongs here; *content* - which
    #: fields must be present, what they must say - is
    #: `EXECUTION_ARCHITECTURE.md` §6 and is enforced by `X-01` and `X-06`. The
    #: two are deliberately not merged: restating §6's field list here would
    #: create the second declaration `FIND-Q9-44` was raised about.
    #:
    #: `mapping` - must be a mapping if present.
    #: `mappings` - must be a sequence, every element a mapping.
    SHAPES: tuple[tuple[str, str], ...] = (
        ("produced_by", "mapping"),
        ("supersedes_seal", "mapping"),
        ("inputs", "mappings"),
        ("deliverables", "mappings"),
        ("acceptance", "mappings"),
        ("affected", "sequence"),
        # VER-013: these four were uncovered, and each still coerced a present
        # malformed value onto the same string an absent one produces.
        # `superseded_by: {}` read as "makes no claim" - the FIND-Q9-43 notice
        # branch - while being present and unreadable.
        ("status", "scalar"),
        ("supersedes", "scalar"),
        ("superseded_by", "scalar"),
        ("conclusion", "scalar"),
        ("result_id", "scalar"),
    )

    def validate_shape(self) -> None:
        """Reject a structurally malformed record **at admission**.

        `VER-012` - the root-cause repair. Every accessor below used to coerce:
        `dict(v) if isinstance(v, dict) else {}`, and
        `[e for e in ... if isinstance(e, dict)]`. Both map *present but
        uninterpretable* onto the same value as *absent*, and absent is a
        passing state. That is the single mechanism behind every defect level
        this record class has produced - a seal block written as a sequence
        became "no seal", and a malformed input entry vanished from the pins
        without a word.

        Coercion is not wrong in an accessor; it is wrong as the **only**
        reading. So the accessors keep their shapes - callers still get a
        mapping or a list of mappings and need no isinstance dance - and this
        method guarantees the coercion is never load-bearing, because a record
        whose shape does not match is never admitted.

        Called by `load_results`, so no consumer can obtain an unvalidated
        record through the supported path.
        """
        _check_shapes(self.result_id, self.data, self.SHAPES)

    @property
    def status(self) -> str:
        return str(self.data.get("status") or "")

    @property
    def inputs(self) -> list[dict[str, Any]]:
        return [e for e in (self.data.get("inputs") or []) if isinstance(e, dict)]

    @property
    def deliverables(self) -> list[dict[str, Any]]:
        """VER-009 FIND-Q9-3: the first form pinned only `inputs`, so a result
        could be published mid-stream, its own deliverables could move under it,
        and X-06 still called it CURRENT. Deliverables are pinned too."""
        return [e for e in (self.data.get("deliverables") or []) if isinstance(e, dict)]

    @property
    def supersedes(self) -> str:
        return str(self.data.get("supersedes") or "")

    @property
    def superseded_by(self) -> str:
        """The successor this record names - the **predecessor's** half of the link.

        VER-009 FIND-Q9-43. Every superseded record in this repository has
        carried this field since `R-001`, and until now nothing read it: the
        whole supersession control was driven from the successor's `supersedes`
        alone, which put the trigger in the hand of the party a tamperer is
        already editing. Deleting `supersedes: R-011` and its seal from `R-012`
        returned X-06 to PASS and left `R-011` freely rewritable.

        The link is declared twice, by two records, and the two declarations
        can be compared. That comparison is what `X-06` now does; this property
        is the half it was missing.

        `null`, `~` and an absent key all read as the empty string, which means
        *this record makes no claim* - not *this record claims it has no
        successor*. The difference matters: X-06 reports the absence as a blind
        spot rather than treating it as a denial.
        """
        return str(self.data.get("superseded_by") or "")

    @property
    def supersedes_seal(self) -> dict[str, Any]:
        """`{path, digest}` - the DC-1 of the record this one supersedes, taken at
        supersession.

        VER-009 FIND-Q9-28. A superseded record is retained unedited, and until
        this field existed nothing recorded what "unedited" meant, so the only
        available test was whether the *tree* had moved - which fires on records
        nobody touched and falls silent on the one that was rewritten. The seal
        is written by the successor, over the predecessor's whole file, so the
        evidence is not in the file it protects.
        """
        v = self.data.get("supersedes_seal")
        return dict(v) if isinstance(v, dict) else {}

    @property
    def affected(self) -> list[str]:
        declared = list(self.data.get("affected") or [])
        return declared or [str(e.get("path") or "") for e in self.deliverables]

    @property
    def conclusion(self) -> str:
        return str(self.data.get("conclusion") or "")

    @property
    def produced_by(self) -> dict[str, Any]:
        return dict(self.data.get("produced_by") or {})


@dataclass
class Index:
    path: str
    sections: dict[str, list[str]] = field(default_factory=dict)

    @property
    def ids(self) -> list[str]:
        return [i for ids in self.sections.values() for i in ids]

    def state_of(self, task_id: str) -> str | None:
        from aief_exec import STATE_HEADINGS
        for heading, ids in self.sections.items():
            if task_id in ids:
                return STATE_HEADINGS.get(heading)
        return None


def parse_index(text: str, path: str) -> Index:
    """EXECUTION_ARCHITECTURE.md section 4 / AIEF-AMD-014 AMD-49 `index_grammar`:
    level-2 headings each followed by one identifier per line, nothing else on
    that line."""
    idx = Index(path=path)
    heading: str | None = None
    in_fence = False
    for raw in text.replace("\r\n", "\n").split("\n"):
        line = raw.rstrip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## "):
            heading = line[3:].strip()
            idx.sections.setdefault(heading, [])
            continue
        if heading is None or not line.strip():
            continue
        if line.startswith("#") or line.startswith(">") or line.startswith("|"):
            continue
        token = line.strip()
        if TASK_ID.match(token):
            idx.sections[heading].append(token)
        elif heading in idx.sections and idx.sections[heading] is not None:
            # Prose is permitted only before the first identifier of a section;
            # once identifiers start, the grammar is one id per line.
            if idx.sections[heading]:
                raise RecordError(
                    f"index line carries more than one identifier or trailing "
                    f"text under heading {heading!r}: {token!r}"
                )
    return idx


def _read(repo: Path, rel: str) -> str:
    return (repo / rel).read_text(encoding="utf-8")


def load_index(repo: Path) -> Index:
    from aief_exec import INDEX_PATH
    return parse_index(_read(repo, INDEX_PATH), INDEX_PATH)


def load_tasks(repo: Path) -> dict[str, TaskRecord]:
    from aief_exec import TASKS_DIR
    out: dict[str, TaskRecord] = {}
    d = repo / TASKS_DIR
    if not d.is_dir():
        return out
    for p in sorted(d.glob("T-*.md")):
        data = parse_block(extract_fence(p.read_text(encoding="utf-8")))
        tid = str(data.get("task_id") or "")
        if not TASK_ID.match(tid):
            raise RecordError(f"{p.name}: task_id {tid!r} is not T-nnn")
        if tid in out:
            raise RecordError(f"duplicate task_id {tid}")
        rel = f"{TASKS_DIR}/{p.name}"
        rec = TaskRecord(task_id=tid, path=rel, data=data)
        rec.validate_shape()
        out[tid] = rec
    return out


def load_results(repo: Path) -> dict[str, ResultRecord]:
    from aief_exec import RESULTS_DIR
    out: dict[str, ResultRecord] = {}
    d = repo / RESULTS_DIR
    if not d.is_dir():
        return out
    for p in sorted(d.glob("R-*.md")):
        data = parse_block(extract_fence(p.read_text(encoding="utf-8")))
        rid = str(data.get("result_id") or "")
        if not RESULT_ID.match(rid):
            raise RecordError(f"{p.name}: result_id {rid!r} is not R-nnn")
        if rid in out:
            raise RecordError(f"duplicate result_id {rid}")
        rel = f"{RESULTS_DIR}/{p.name}"
        rec = ResultRecord(result_id=rid, path=rel, data=data)
        rec.validate_shape()
        out[rid] = rec
    return out


def file_dc1(repo: Path, rel: str) -> str | None:
    """DC-1 of a working-tree path, or None if absent."""
    p = repo / rel
    if not p.is_file():
        return None
    return dc1_digest(p.read_bytes())


def roster(repo: Path) -> dict[str, bool]:
    """Role -> is it assigned. `TPL-task-package.md` acceptance condition 1: the
    role must appear in project/ROSTER.md and must not be UNASSIGNED, because
    'a role marked UNASSIGNED cannot be dispatched'."""
    p = repo / ".ai/project/ROSTER.md"
    if not p.is_file():
        # Absence is reported by X-01 as a conformance failure rather than
        # crashing the plan; an empty roster constrains nothing.
        return {}
    text = p.read_text(encoding="utf-8")
    out: dict[str, bool] = {}
    for raw in text.replace("\r\n", "\n").split("\n"):
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        role = cells[0].strip("`* ")
        if not role or role.lower() in ("role", "---") or set(role) <= {"-"}:
            continue
        out[role] = "UNASSIGNED" not in cells[2].upper()
    return out


def open_item_ids(repo: Path) -> set[str]:
    """Identifiers listed under the open sections of project/OPEN_ITEMS.md.
    `Closed` is excluded - a closed item does not block."""
    text = _read(repo, ".ai/project/OPEN_ITEMS.md")
    out: set[str] = set()
    heading = None
    for raw in text.replace("\r\n", "\n").split("\n"):
        line = raw.strip()
        if line.startswith("## "):
            heading = line[3:].strip()
            continue
        if heading is None or heading.lower() == "closed" or not line:
            continue
        if line.startswith(("#", ">", "|", "*", "-")):
            continue
        if re.fullmatch(r"[A-Z][A-Za-z0-9-]*(…[A-Z0-9-]+)?", line):
            out.add(line)
    return out
