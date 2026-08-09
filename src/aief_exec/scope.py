"""Read-scope resolution, path-set algebra and exact token cost.

Actor provenance: software.software-engineer - S-2026-08-09-01.

Implements EXECUTION_ARCHITECTURE.md sections 5.1, 5.2, 7 (intersection) and 11.

Token counts come from the repository's own declared families TF-1 and TF-2
(`metadata.reproducible.tokenizer_families`) via `aief_stage6.tokenizers`. When a
family is unavailable the cost is reported UNMEASURED and never estimated, per
that module's fail-safe rule and LAW-12.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, NamedTuple

from aief_stage6 import tokenizers as _tok

_PROBE: Any = None


def probe() -> Any:
    global _PROBE
    if _PROBE is None:
        _PROBE = _tok.probe()
    return _PROBE


class ScopeError(ValueError):
    """A read-scope entry does not resolve."""


# --------------------------------------------------------------------------
# Glob handling - section 7
# --------------------------------------------------------------------------

_WILD = re.compile(r"[*?\[]")


def glob_to_regex(pattern: str) -> re.Pattern[str]:
    """POSIX-relative glob. `**` crosses separators, `*` and `?` do not."""
    out: list[str] = []
    i = 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:[^/]+/)*")
            i += 3
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def literal_prefix(pattern: str) -> str:
    m = _WILD.search(pattern)
    return pattern if not m else pattern[: m.start()]


def _has_wildcard(pattern: str) -> bool:
    return bool(_WILD.search(pattern))


SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules", "build"}


def tree(repo: Path) -> list[str]:
    """POSIX-relative paths of the working tree, excluding build output and VCS."""
    out: list[str] = []
    for p in repo.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(repo).as_posix()
        if any(part in SKIP_DIRS for part in rel.split("/")):
            continue
        out.append(rel)
    return sorted(out)


def expand(repo: Path, patterns: list[str], paths: list[str] | None = None) -> set[str]:
    """Concrete working-tree paths matched by any pattern."""
    universe = paths if paths is not None else tree(repo)
    rx = [glob_to_regex(p) for p in patterns]
    return {p for p in universe if any(r.match(p) for r in rx)}


# --- Exact glob intersection -----------------------------------------------
#
# VER-009 FIND-Q9-24 then FIND-Q9-29. Two forms failed here before this one.
#
#   1. Literal-prefix comparison. Over-reported: `.ai/*.md` and
#      `.ai/project/EXEC.md` share the prefix `.ai/` and no path satisfies both.
#   2. Witness probing plus a nesting fallback. Under-reported: a witness proves
#      overlap and can never prove disjointness, and the fallback it was given
#      repaired one of the six pairs pass 3 named. Five pattern pairs still
#      reported disjoint while genuinely intersecting - error in the *unsafe*
#      direction, inside the primitive that decides concurrent-write safety.
#
# Neither heuristic is repaired below; both are replaced by a decision
# procedure. Each glob compiles to a Thompson NFA over three character classes -
# one literal character, any character except `/`, any character at all - and
# the two automata are intersected by product reachability. The languages of two
# globs intersect exactly when the product accepts, so the answer is not
# conservative, not optimistic, and not a heuristic: it is the answer.
#
# The tokenisation is the one `glob_to_regex` compiles, so the pattern algebra
# and the concrete matcher cannot disagree about what a pattern means.

_LIT, _ONE, _STAR, _DSTAR, _DSTARSLASH = "lit", "one", "star", "dstar", "dstarslash"

#: A character class. `("c", ch)` is the single character `ch`; `("N",)` is any
#: character except the separator; `("A",)` is any character.
_ANY: tuple[str, ...] = ("A",)
_NONSEP: tuple[str, ...] = ("N",)


def _tokens(pattern: str) -> list[tuple[str, str]]:
    """Tokenise exactly as `glob_to_regex` compiles."""
    out: list[tuple[str, str]] = []
    i = 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append((_DSTARSLASH, ""))
            i += 3
        elif pattern.startswith("**", i):
            out.append((_DSTAR, ""))
            i += 2
        elif pattern[i] == "*":
            out.append((_STAR, ""))
            i += 1
        elif pattern[i] == "?":
            out.append((_ONE, ""))
            i += 1
        else:
            out.append((_LIT, pattern[i]))
            i += 1
    return out


def _build_nfa(
    pattern: str,
) -> tuple[dict[int, set[int]], dict[int, list[tuple[tuple[str, ...], int]]], int, int]:
    """Thompson NFA for one glob. Returns (epsilon, labelled moves, start, accept)."""
    eps: dict[int, set[int]] = {}
    moves: dict[int, list[tuple[tuple[str, ...], int]]] = {}
    counter = 0

    def new() -> int:
        nonlocal counter
        s = counter
        counter += 1
        eps[s] = set()
        moves[s] = []
        return s

    start = cur = new()
    for kind, ch in _tokens(pattern):
        if kind == _LIT:
            nxt = new()
            moves[cur].append((("c", ch), nxt))
            cur = nxt
        elif kind == _ONE:
            nxt = new()
            moves[cur].append((_NONSEP, nxt))
            cur = nxt
        elif kind == _STAR:                      # [^/]*
            nxt = new()
            eps[cur].add(nxt)
            moves[nxt].append((_NONSEP, nxt))
            cur = nxt
        elif kind == _DSTAR:                     # .*
            nxt = new()
            eps[cur].add(nxt)
            moves[nxt].append((_ANY, nxt))
            cur = nxt
        else:                                    # (?:[^/]+/)*
            seg = new()
            eps[cur].add(seg)
            mid = new()
            moves[seg].append((_NONSEP, mid))
            moves[mid].append((_NONSEP, mid))
            moves[mid].append((("c", "/"), seg))
            cur = seg
    return eps, moves, start, cur


def _closure(states: set[int], eps: dict[int, set[int]]) -> set[int]:
    seen = set(states)
    stack = list(states)
    while stack:
        s = stack.pop()
        for t in eps.get(s, ()):
            if t not in seen:
                seen.add(t)
                stack.append(t)
    return seen


def _class_meet(x: tuple[str, ...], y: tuple[str, ...]) -> bool:
    """Whether two character classes share a character."""
    if x[0] == "c" and y[0] == "c":
        return x[1] == y[1]
    if x[0] == "c":
        return y[0] == "A" or x[1] != "/"
    if y[0] == "c":
        return x[0] == "A" or y[1] != "/"
    return True                                  # N/N, N/A and A/A always meet


@lru_cache(maxsize=4096)
def patterns_overlap(a: str, b: str) -> bool:
    """Whether two globs could ever name the same path. Exact, not conservative.

    Decided by product reachability over the two globs' automata: the languages
    intersect exactly when some accepting pair is reachable. `VER-009`
    FIND-Q9-29 - the predecessor was a witness probe with a nesting fallback and
    reported disjoint for five of six pattern pairs that genuinely intersect.
    """
    if a == b:
        return True
    ea, ma, sa, fa = _build_nfa(a)
    eb, mb, sb, fb = _build_nfa(b)
    start = [
        (p, q) for p in _closure({sa}, ea) for q in _closure({sb}, eb)
    ]
    seen = set(start)
    stack = list(start)
    while stack:
        p, q = stack.pop()
        if p == fa and q == fb:
            return True
        for ca, p2 in ma.get(p, ()):
            for cb, q2 in mb.get(q, ()):
                if not _class_meet(ca, cb):
                    continue
                for p3 in _closure({p2}, ea):
                    for q3 in _closure({q2}, eb):
                        if (p3, q3) not in seen:
                            seen.add((p3, q3))
                            stack.append((p3, q3))
    return False


def scopes_intersect(
    repo: Path, a: list[str], b: list[str], paths: list[str] | None = None
) -> set[str] | bool:
    """Concrete intersection if any; otherwise the conservative pattern test.

    Returns the intersecting path set (truthy) or True for a pattern-level
    overlap with no existing witness, or False for disjoint.
    """
    if not a or not b:
        return False
    common = expand(repo, a, paths) & expand(repo, b, paths)
    if common:
        return common
    for pa in a:
        for pb in b:
            if patterns_overlap(pa, pb):
                return True
    return False


# --------------------------------------------------------------------------
# Anchor resolution - section 5.1
# --------------------------------------------------------------------------

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def resolve_heading(text: str, anchor: str) -> str | None:
    """A heading containing `anchor`, through to the next heading of the same or
    higher level."""
    lines = text.replace("\r\n", "\n").split("\n")
    start = level = None
    for i, line in enumerate(lines):
        m = _HEADING.match(line)
        if not m:
            continue
        if start is None:
            if anchor in m.group(2):
                start, level = i, len(m.group(1))
            continue
        if len(m.group(1)) <= level:
            return "\n".join(lines[start:i]).rstrip() + "\n"
    if start is None:
        return None
    return "\n".join(lines[start:]).rstrip() + "\n"


def heading_matches(text: str, anchor: str) -> int:
    """How many headings contain `anchor`. More than one means the anchor does
    not identify a section - VER-009 FIND-Q9-7."""
    n = 0
    for line in text.replace("\r\n", "\n").split("\n"):
        m = _HEADING.match(line)
        if m and anchor in m.group(2):
            n += 1
    return n


def resolve_row(text: str, anchor: str) -> str | None:
    """The single table row whose leading cell matches `anchor`, with the header
    of the table it belongs to."""
    lines = text.replace("\r\n", "\n").split("\n")
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        lead = cells[0].strip("`*_ ")
        if lead != anchor:
            continue
        head = i
        while head > 0 and lines[head - 1].lstrip().startswith("|"):
            head -= 1
        header = lines[head : min(head + 2, i)]
        return "\n".join([*header, line]).rstrip() + "\n"
    return None


def resolve_json(text: str, anchor: str) -> str | None:
    """Dotted key path into a JSON document."""
    node: Any = json.loads(text)
    for part in anchor.split("."):
        if isinstance(node, list):
            try:
                node = node[int(part)]
                continue
            except (ValueError, IndexError):
                return None
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return json.dumps(node, indent=1, ensure_ascii=False) + "\n"


def resolve_entry(repo: Path, entry: dict[str, Any]) -> str:
    """Resolve one read-scope entry to its excerpt text.

    Order, deterministic: JSON targets take the anchor as a dotted key path;
    every other target tries a heading match first, then a table row. An entry
    with no anchor resolves to the whole file.
    """
    rel = str(entry.get("path") or "")
    if not rel:
        raise ScopeError(f"read-scope entry has no path: {entry!r}")
    p = repo / rel
    if not p.is_file():
        raise ScopeError(f"read-scope path does not exist: {rel}")
    text = p.read_text(encoding="utf-8")
    anchor = entry.get("anchor")
    if not anchor:
        return text
    anchor = str(anchor)
    if rel.endswith(".json"):
        got = resolve_json(text, anchor)
        if got is None:
            raise ScopeError(f"anchor {anchor!r} does not resolve in {rel}")
        return got
    got = resolve_heading(text, anchor)
    if got is None:
        got = resolve_row(text, anchor)
    if got is None:
        raise ScopeError(f"anchor {anchor!r} does not resolve in {rel}")
    if not got.strip():
        raise ScopeError(f"anchor {anchor!r} resolves empty in {rel}")
    return got


# --------------------------------------------------------------------------
# Cost - section 11
# --------------------------------------------------------------------------

@dataclass
class Cost:
    tf1: int | None
    tf2: int | None

    @property
    def measured(self) -> bool:
        return self.tf1 is not None and self.tf2 is not None

    def __add__(self, other: "Cost") -> "Cost":
        def add(a: int | None, b: int | None) -> int | None:
            return None if a is None or b is None else a + b
        return Cost(add(self.tf1, other.tf1), add(self.tf2, other.tf2))

    def __str__(self) -> str:
        if not self.measured:
            return "UNMEASURED"
        return f"TF-1 {self.tf1} / TF-2 {self.tf2}"


ZERO = Cost(0, 0)


def cost(text: str) -> Cost:
    """Exact count under both declared families; UNMEASURED if either is absent."""
    pr = probe()
    fams = {f.family_id: f for f in pr.families}
    tf1 = fams["TF-1"].count(text) if "TF-1" in fams else None
    tf2 = fams["TF-2"].count(text) if "TF-2" in fams else None
    return Cost(tf1, tf2)


def attribute(
    repo: Path, changed: list[str], tasks: dict[str, Any]
) -> dict[str, list[str]]:
    """Map each changed path to the tasks whose write_scope covers it.

    Section 5.2 / Requirement D: a path covered by no task's write scope is an
    unattributed modification. Detection is after the fact - the host cannot
    intercept a write - but an unattributed change is visible in review.
    """
    out: dict[str, list[str]] = {}
    for path in changed:
        owners = [
            tid
            for tid, task in sorted(tasks.items())
            if any(glob_to_regex(p).match(path) for p in task.write_scope)
        ]
        out[path] = owners
    return out


class Excerpt(NamedTuple):
    """One resolved read-scope entry, carrying the text it resolved to.

    `VER-009` FIND-Q9-33: the first form returned the cost and discarded the
    text, so `brief` re-resolved every entry to print it and `resolve_scope`
    read every file a second time for the unanchored comparison - three opens
    per entry where one is needed. The excerpt is evidence; it is kept.
    """

    path: str
    anchor: str
    cost: Cost
    text: str


@dataclass
class ResolvedScope:
    entries: list[Excerpt]
    total: Cost
    errors: list[str]
    whole_file_total: Cost = field(default_factory=lambda: ZERO)


def resolve_scope(
    repo: Path, task: Any, kind: str = "mandatory", whole: bool = True
) -> ResolvedScope:
    """Resolve every entry of one read-scope class and measure it.

    `whole` also measures each entry's file unanchored, for the AC-3 comparison.
    It costs one extra read per entry and callers that do not print the
    comparison pass `whole=False` - FIND-Q9-33.
    """
    entries: list[Excerpt] = []
    errors: list[str] = []
    total = ZERO
    whole_total = ZERO
    for entry in task.read_entries(kind):
        label = str(entry.get("path") or "")
        anchor = entry.get("anchor")
        try:
            text = resolve_entry(repo, entry)
        except ScopeError as exc:
            errors.append(str(exc))
            continue
        c = cost(text)
        total = total + c
        if whole:
            full = (repo / label).read_text(encoding="utf-8")
            whole_total = whole_total + cost(full)
        entries.append(Excerpt(label, str(anchor) if anchor else "", c, text))
    return ResolvedScope(
        entries=entries, total=total, errors=errors, whole_file_total=whole_total
    )


# --------------------------------------------------------------------------
# What a task is actually charged - section 11, VER-009 FIND-Q9-35
# --------------------------------------------------------------------------

#: One unit of the acquisition surface: `(component, path, anchor or None)`.
Unit = tuple[str, str, "str | None"]


def _units_record(task: Any, results: dict[str, Any]) -> list[Unit]:
    """The task's own contract. Always exactly one unit, always charged."""
    return [("record", task.path, None)]


def _units_declared_reads(kind: str) -> Callable[[Any, dict[str, Any]], list[Unit]]:
    """`mandatory` and `optional` differ only in the key they are read from."""

    def emit(task: Any, results: dict[str, Any]) -> list[Unit]:
        out: list[Unit] = []
        for entry in task.read_entries(kind):
            rel = str(entry.get("path") or "").strip()
            if not rel:
                continue
            anchor = entry.get("anchor")
            out.append((kind, rel, str(anchor) if anchor else None))
        return out

    return emit


def _units_dependency(task: Any, results: dict[str, Any]) -> list[Unit]:
    """Consumed result records that are on disk. See `acquisition_units`."""
    out: list[Unit] = []
    for rid in getattr(task, "consumes", []):
        result = results.get(rid)
        if result is not None:
            out.append(("dependency", result.path, None))
    return out


#: **The one declaration of the acquisition surface**, component name to the
#: function that emits its units. `VER-009` FIND-Q9-44: this used to be two
#: declarations - a literal tuple summed by `ChargedContext.acquisition`, and a
#: hardcoded body inside `acquisition_units` - with nothing tying them
#: together. Adding `telemetry` to the tuple alone was charged nowhere,
#: compared nowhere, and survived the entire test suite (mutant MU14). A name
#: cannot now be added to the set without an emitter, because the set **is**
#: the emitter table's key order.
ACQUISITION_EMITTERS: dict[str, Callable[[Any, dict[str, Any]], list[Unit]]] = {
    "record": _units_record,
    "mandatory": _units_declared_reads("mandatory"),
    "optional": _units_declared_reads("optional"),
    "dependency": _units_dependency,
}

#: Components of `acquisition` - what a task must load **before** it acts.
#: Derived, not declared: see `ACQUISITION_EMITTERS`. Order is the emission
#: order, which is the order every breakdown prints in.
ACQUISITION_COMPONENTS: tuple[str, ...] = tuple(ACQUISITION_EMITTERS)

#: Components of `revision` - artifacts that already exist and must be read in
#: order to be rewritten. One component, emitted by `deliverable_paths`, which
#: `charged_context` calls directly; there is no second declaration to drift
#: from.
REVISION_COMPONENTS = ("deliverable",)


def acquisition_units(
    task: Any, results: dict[str, Any] | None = None
) -> list[tuple[str, str, str | None]]:
    """`(component, path, anchor)` for every unit `acquisition` covers.

    **The single enumeration of the pre-dispatch surface.** `VER-009`
    FIND-Q9-38 traced four independent hazard escapes to one cause: the cost
    model enumerated five surfaces while the hazard model compared three, and
    the information needed to close the gap was computed in this module and
    discarded before the comparison. It is not discarded now - it is named
    here, and both models read it:

    * `charged_context` measures these units (plus `deliverable`, which is
      `revision`);
    * `graph.read_surface` compares them, so a task that writes what another
      task must load is a `write/read` hazard whichever of the four components
      carries it.

    Nothing else may enumerate the acquisition surface.

    **`VER-009` FIND-Q9-44 - and now nothing else may declare it either.** The
    sentence above used to be followed by *"Adding a component means adding it
    here, and both models acquire it in the same edit"*, which was true of the
    two **models** and false of the two **declarations**: this function
    hardcoded `record`, a literal `("mandatory", "optional")` loop and a
    `dependency` loop, while `ChargedContext.acquisition` summed the separate
    constant `ACQUISITION_COMPONENTS`. Nothing asserted the two agreed, and a
    mutant that added `telemetry` to the constant alone survived every test in
    the suite - charged nowhere, compared nowhere, invisible.

    There is one declaration now, `ACQUISITION_EMITTERS`, and this function
    iterates it. `ACQUISITION_COMPONENTS` is its key order. A component with no
    emitter is unrepresentable, and a kind emitted under a name the set does
    not contain would be charged into no component - which
    `TestAcquisitionSurfaceIsOneDeclaration` asserts against directly, in both
    directions.

    Two deliberate properties, stated rather than left to be discovered:

    * **Anchors are carried but do not narrow the surface.** A hazard is about
      the file: a writer moving any part of an anchored file moves the section
      the reader resolved. The cost model charges the excerpt; the hazard model
      compares the path.
    * **A consumed result that is not on disk contributes nothing**, to either
      model. It cannot be measured and it cannot be intersected. Nothing is
      missed: a task consuming an unpublished result derives BLOCKED, so there
      is no dispatch for a hazard to contaminate.
    """
    out: list[Unit] = []
    for kind in ACQUISITION_COMPONENTS:
        emit = ACQUISITION_EMITTERS.get(kind)
        if emit is None:
            # Unreachable while the set is the table's key order, and loud if
            # anything ever separates them again. Silence is what FIND-Q9-44
            # was: `ChargedContext.acquisition` would have summed a component
            # that emits nothing, reported zero for it, and moved no total.
            raise ScopeError(
                f"acquisition component {kind!r} is declared in "
                f"ACQUISITION_COMPONENTS and has no emitter in "
                f"ACQUISITION_EMITTERS, so it would be charged nowhere and "
                f"compared nowhere (VER-009 FIND-Q9-44)"
            )
        out.extend(emit(task, results or {}))
    return out

#: The third quantity, stated and never estimated. See `ChargedContext.telemetry`.
TELEMETRY_NOTE = (
    "UNMEASURABLE - execution and tool output is not in the repository and this "
    "layer will not estimate it"
)


@dataclass
class ChargedContext:
    """What a task costs, split into quantities that behave differently.

    `VER-009` FIND-Q9-35 corrected an undercount by folding deliverables into a
    single charged figure. That correction introduced a second defect, and this
    class is the repair for it: **one number cannot gate a dispatch when part of
    it only exists after the dispatch.** `T-005` charged TF-1 1,411 against a cap
    of 1,500 before it ran and 7,161 after, because its own new deliverable
    became chargeable the moment it was written. A gate whose verdict depends on
    whether the task already ran is not a gate.

    Three named quantities, reported separately, never silently summed:

    ``acquisition``
        record + mandatory + optional + dependency. Everything the task must
        hold before it can start. **This is the quantity X-08 gates - as a
        dispatch-time measurement, not as an invariant.**

        `VER-009` FIND-Q9-36 falsified the invariance this field used to claim.
        `record` is an acquisition component and every AIEF task is required to
        update its own checkpoint as it works, so wherever a task's own record
        lies inside its own `write_scope` the gated figure moves under the
        task's hand: a synthetic task measured 542 TF-1, then **1,328 (+145%)**
        after appending one progress note to its own checkpoint. It is live too
        - 34% of `T-001`'s gated figure and 24% of `T-002`'s, the latter a
        figure `X-08` currently fails on, lie in paths those tasks write.

        The honest statement is therefore the narrow one: the figure is exact
        and reproducible **at the moment of dispatch**, and it does not move
        when the task's *deliverable* is created, which was the channel
        FIND-Q9-35's repair was reported on. It does move when the task edits
        any charged path it also owns. `acquisition_stable` and
        `acquisition_self_referential` split it on exactly that line so a
        reader can see how much of the gate the task can move, and
        `moving_by_component` names which component carries the movement.

        Dropping `record` from the gate would make the figure invariant and the
        measurement false - an agent genuinely must read its contract - so the
        cost stays charged and the movement stays disclosed.
    ``revision``
        Deliverable paths that already resolve. Real cost - an artifact being
        rewritten must be read - but not a precondition, and **non-monotonic**
        wherever the path lies inside the task's own write scope, because then
        the task's own work moves the figure. Not gated by `context_budget`,
        but not invisible either: FIND-Q9-37 established that it is 53% of
        `T-004`'s measurable total, 85% of `T-001`'s and 80% of `T-005`'s, so
        `total_measurable` is bounded against the same declared cap by `X-10`,
        which fails on a breach of it. `X-08` neither gates nor fails on this
        figure - see `total_measurable`.
    ``telemetry``
        Execution and tool output: command results, diffs, test logs, everything
        a session accumulates by acting. **Not measurable from the repository**,
        which holds no execution trace, so it is represented as unmeasurable and
        excluded rather than estimated or defaulted to zero. It is not small: a
        prior session measured its own telemetry overrun at roughly 52% of a task
        cap. The repository simply cannot see it, and saying so is the only
        honest thing this field can do.

    `total` (and its named alias `total_measurable`) is `acquisition +
    revision` - the two measurable quantities. It excludes telemetry, which
    cannot be added to it.
    """

    components: list[tuple[str, str, Cost]] = field(default_factory=list)
    total: Cost = field(default_factory=lambda: ZERO)
    read_only_total: Cost = field(default_factory=lambda: ZERO)
    errors: list[str] = field(default_factory=list)
    notices: list[str] = field(default_factory=list)
    #: Charged paths inside the task's own write scope - the self-referential
    #: part of the charge, in **every** component and not only `revision`.
    #: FIND-Q9-36b: the notice that reported this used to attribute it to
    #: `revision` alone, which was false for every task whose movement is in
    #: `acquisition`.
    non_monotonic: list[str] = field(default_factory=list)
    #: The task's declared write scope, retained so the self-referential split
    #: can be recomputed per component without re-reading the record.
    write_scope: list[str] = field(default_factory=list)

    def component_total(self, name: str) -> Cost:
        out = ZERO
        for kind, _, c in self.components:
            if kind == name:
                out = out + c
        return out

    def _sum(self, names: tuple[str, ...]) -> Cost:
        out = ZERO
        for kind, _, c in self.components:
            if kind in names:
                out = out + c
        return out

    @staticmethod
    def _path_of(label: str) -> str:
        """The path part of a component label; `path#anchor` charges one file."""
        return label.split("#", 1)[0]

    def is_self_referential(self, label: str) -> bool:
        """Whether this charged unit lies inside the task's own write scope.

        The one line that separates a figure the task can move from one it
        cannot. It is a property of the *declared* write scope, so it is
        decidable before dispatch and does not depend on what the task did.
        """
        rel = self._path_of(label)
        return any(glob_to_regex(p).match(rel) for p in self.write_scope)

    def _split(self, names: tuple[str, ...]) -> tuple[Cost, Cost]:
        stable, moving = ZERO, ZERO
        for kind, label, c in self.components:
            if kind not in names:
                continue
            if self.is_self_referential(label):
                moving = moving + c
            else:
                stable = stable + c
        return stable, moving

    def moving_by_component(self) -> list[tuple[str, str]]:
        """`(component, path)` for every charged unit the task itself writes.

        FIND-Q9-36b. `non_monotonic` records *that* a path moves; this records
        *where*, which is the fact the emitted notice got wrong: for `T-002` it
        named `revision` while both moving paths were in `mandatory`, and
        `revision` was zero.
        """
        out: list[tuple[str, str]] = []
        seen: set[tuple[str, str]] = set()
        for kind, label, _ in self.components:
            rel = self._path_of(label)
            if not self.is_self_referential(label) or (kind, rel) in seen:
                continue
            seen.add((kind, rel))
            out.append((kind, rel))
        return sorted(out)

    @property
    def acquisition(self) -> Cost:
        """The gated quantity: what must be held before dispatch.

        Gated, exact, and **not invariant across the task's own execution** -
        see the class docstring and `acquisition_self_referential`.
        """
        return self._sum(ACQUISITION_COMPONENTS)

    @property
    def acquisition_stable(self) -> Cost:
        """The part of `acquisition` no lawful act of this task can move."""
        return self._split(ACQUISITION_COMPONENTS)[0]

    @property
    def acquisition_self_referential(self) -> Cost:
        """The part of `acquisition` inside the task's own write scope.

        Non-zero means the dispatch gate is a function of the dispatch it
        gates, to this extent. Reported beside the gate rather than removed
        from it: the cost is real and an agent must load it.
        """
        return self._split(ACQUISITION_COMPONENTS)[1]

    @property
    def revision(self) -> Cost:
        """Reported, not gated. Non-monotonic where `non_monotonic` is non-empty."""
        return self._sum(REVISION_COMPONENTS)

    @property
    def total_measurable(self) -> Cost:
        """`acquisition + revision` - everything this layer can actually count.

        Named because FIND-Q9-37 established that what the gate leaves out is
        the majority of the input for three of six live tasks, and an excluded
        cost that is only ever a footnote is an invisible cost. It is bounded
        against the same declared cap by **`X-10`, a check of its own**, and a
        breach is an `X-10` failure.

        FIND-Q9-45: that used to be a second verdict inside `X-08`, and since
        this figure is `>= acquisition` by construction, `X-08` then failed iff
        this figure breached - the gate contributed nothing to the boolean, and
        the two kinds of row were distinguishable only by a substring of
        English. **This quantity is non-monotonic in the task's own work** -
        `revision` charges deliverables that exist - so a check whose verdict it
        decides cannot be a dispatch gate. `X-10` is named for that and `X-08`
        no longer reads this property at all.

        Equal to `total` by construction; the name states the claim.
        """
        return self.acquisition + self.revision

    @property
    def telemetry(self) -> Cost:
        """Always unmeasurable. `Cost(None, None)`, which prints UNMEASURED and is
        not zero - the distinction between 'nothing' and 'cannot see' is the
        entire content of this field."""
        return Cost(None, None)

    @property
    def telemetry_note(self) -> str:
        return TELEMETRY_NOTE


def deliverable_paths(
    repo: Path, task: Any, paths: list[str] | None = None
) -> tuple[list[str], list[str]]:
    """Split `deliverable` into paths that exist today and entries that name none.

    A deliverable entry is charged only when the entry, taken **whole**, is an
    existing file, an existing directory, or a glob matching existing files.
    Anything else is returned unresolved and charged nothing: it is either
    prospective output, which costs a reader nothing, or prose, and guessing a
    path out of prose would be resolving an ambiguity by assumption - LAW-12.
    """
    resolved: list[str] = []
    unresolved: list[str] = []
    for raw in task.data.get("deliverable") or []:
        entry = str(raw).strip()
        if not entry:
            continue
        rel = entry.rstrip("/")
        try:
            if _has_wildcard(entry):
                hits = sorted(expand(repo, [entry], paths))
                (resolved.extend(hits) if hits else unresolved.append(entry))
                continue
            target = repo / rel
            if target.is_file():
                resolved.append(rel)
            elif target.is_dir():
                resolved.extend(
                    p for p in (paths if paths is not None else tree(repo))
                    if p == rel or p.startswith(rel + "/")
                )
            else:
                unresolved.append(entry)
        except OSError:
            unresolved.append(entry)
    return resolved, unresolved


def charged_context(
    repo: Path, task: Any, results: dict[str, Any] | None = None,
    paths: list[str] | None = None,
) -> ChargedContext:
    """The whole context a session executing this task must hold.

    `VER-009` FIND-Q9-35. The superseded model charged the resolved read scope
    and stopped, so it certified `T-004` at TF-1 2,519 against a cap of 8,000
    while the pass actually consumed roughly 22,000 - **8.7x** - because the one
    artifact that dominated the cost was `T-004`'s own **deliverable**, which the
    task must read in full to rewrite in place. A model of a task as *what it
    reads to start* is wrong for every task that revises something that already
    exists.

    Five components, each measured exactly and reported separately:

    ``record``
        The task record. An agent cannot execute a contract it has not read.
    ``mandatory`` / ``optional``
        The resolved read scope, anchored - as before.
    ``dependency``
        Every consumed result record, **whole**. Section 6 tells a consumer to
        read the conclusion and not re-derive it, and `brief` emits only the
        conclusion - but FIND-Q9-35 names `R-008` at TF-1 3,550, the whole file,
        as one of the omissions, and the auditor's actual consumption was the
        whole file. A consumer must at least be able to check that the record it
        consumes is CURRENT and unsuperseded, which the conclusion does not say.
        Charged whole, which is the conservative direction.
    ``deliverable``
        Every deliverable path that **already exists**. A prospective deliverable
        costs a reader nothing and is charged nothing.

    Units are deduplicated by path, and a whole-file charge subsumes an anchored
    charge on the same path, so nothing is counted twice.

    **`VER-009` FIND-Q9-49: a path declared as both wins for `deliverable`.** The
    dedup kept whichever unit was built first, and acquisition is built first, so
    a path that is both a read entry and a deliverable was charged into the
    **gated** quantity - and the gate then moved when the task created its own
    output, which is the one thing the split exists to stop. The classification
    is decided from the declarations now: a declared deliverable is the task's
    own output, its existence at dispatch is the task's to decide, and a quantity
    the task decides has no business inside a dispatch gate. Charged once, to
    `revision`, and the overlap is reported rather than assumed empty.

    The first four components make up `acquisition` and the fifth makes up
    `revision`; see `ChargedContext` for why the two are gated differently and
    why `telemetry` is neither summed nor estimated. The first four are
    enumerated by `acquisition_units`, which `graph.read_surface` also reads -
    FIND-Q9-38, so that the hazard model cannot compare fewer surfaces than the
    cost model charges.
    """
    cc = ChargedContext(write_scope=list(getattr(task, "write_scope", [])))

    # The acquisition surface is enumerated once, by `acquisition_units`, and
    # `graph.read_surface` reads the same enumeration - FIND-Q9-38. What is
    # dropped here and only here is what cannot be *measured*: an entry that
    # does not resolve is an X-03 failure and is reported as an error, not
    # charged. The hazard model still compares it, which is the safe direction.
    resolvable: set[tuple[str, str, str | None]] = set()
    for kind in ("mandatory", "optional"):
        rs = resolve_scope(repo, task, kind, whole=False)
        cc.errors.extend(rs.errors)
        cc.read_only_total = cc.read_only_total + rs.total
        for ex in rs.entries:
            resolvable.add((kind, ex.path, ex.anchor or None))
    units: list[tuple[str, str, str | None]] = [
        unit
        for unit in acquisition_units(task, results)
        if unit[0] not in ("mandatory", "optional") or unit in resolvable
    ]

    resolved, unresolved = deliverable_paths(repo, task, paths)
    # `VER-009` FIND-Q9-49. A path may lawfully be both a declared read entry and
    # a declared deliverable - a task that revises a file it must also consult is
    # the ordinary case. Which component it is charged to is decided here, from
    # the declarations, and not by the order the units happen to be built in;
    # see the dedup below.
    deliverable_set = set(resolved)
    for rel in resolved:
        units.append(("deliverable", rel, None))
    for entry in unresolved:
        cc.notices.append(
            f"{task.task_id}: deliverable {entry!r} names no existing path, so it "
            f"is charged nothing - prospective output, or prose a budget cannot see"
        )

    # A whole-file unit on a path makes every anchored unit on it redundant.
    #
    # `VER-009` FIND-Q9-49, MAJOR. Deduplication kept the **first** unit on a
    # path, and acquisition units are built before deliverables, so a path
    # declared as both a read entry and a deliverable was charged to
    # `acquisition` and never reached `revision`. The consequence is the exact
    # defect the split exists to prevent: `acquisition` is the gated quantity and
    # is supposed not to move when a task creates its own deliverable, and for
    # such a path it moved. Built and measured by the audit - a task declaring
    # `deliverable: [out/shared.md]` and `optional: [out/shared.md]` went
    # `X-08` FAIL -> PASS on creating that file, `acquisition` 251 -> 855 with
    # `revision` 0 throughout. The overlap is empty for all six live tasks, so
    # nothing here was wrong on this tree; the gate's headline property held by
    # coincidence rather than by construction, and a coincidence is not a
    # property.
    #
    # Attribution is decided by what the declarations say, not by build order. A
    # declared deliverable is the task's **own output**: whether it exists at
    # dispatch is decided by the task, which is the defining property of
    # `revision` and the disqualifying property for anything inside a dispatch
    # gate. So the deliverable classification wins on a shared path, wherever the
    # unit came from.
    #
    # This moves no cost and hides none. The unit is charged exactly once either
    # way, so `total_measurable` - and therefore `X-10` - is unchanged to the
    # token; only which of the two named quantities carries it changes. The
    # overlap is reported, because FIND-Q9-49's second limb is that nothing
    # asserted the overlap was empty and no check reported one when it was not.
    whole_paths = {p for _, p, a in units if a is None}
    seen: set[tuple[str, str | None]] = set()
    ordered: list[tuple[str, str, str | None]] = []
    shared: dict[str, str] = {}
    for kind, rel, anchor in units:
        if anchor is not None and rel in whole_paths:
            continue
        if (rel, anchor) in seen:
            continue
        seen.add((rel, anchor))
        if rel in deliverable_set and kind != "deliverable":
            shared[rel] = kind
            kind = "deliverable"
        ordered.append((kind, rel, anchor))
    if shared:
        cc.notices.append(
            f"{task.task_id}: {len(shared)} path(s) are declared both as a read "
            f"entry and as a deliverable and are charged once, to revision, "
            f"because the task's own output is not a precondition of its own "
            f"dispatch (FIND-Q9-49): "
            + "; ".join(f"{k} {p}" for p, k in sorted(shared.items()))
            + " - total_measurable is unaffected; acquisition is lower than a "
            f"read-side reading of the same declarations would give, and does "
            f"not move when {task.task_id} creates these paths"
        )

    for kind, rel, anchor in ordered:
        try:
            text = resolve_entry(repo, {"path": rel, "anchor": anchor})
        except (ScopeError, OSError, UnicodeDecodeError) as exc:
            cc.errors.append(str(exc))
            continue
        c = cost(text)
        cc.total = cc.total + c
        cc.components.append((kind, rel + (f"#{anchor}" if anchor else ""), c))

    # FIND-Q9-35 second limb, corrected by FIND-Q9-36 and FIND-Q9-36b. The
    # measurement is self-referential wherever a charged path is one the task
    # itself writes, and the figure then moves as the task works - a concurrent
    # session watched its own brief grow from TF-1 4,295 to 4,910 by adding
    # docstrings to a file inside its own read scope.
    #
    # The predecessor of this block drew the wrong conclusion from that very
    # anecdote. A file inside a task's own *read* scope is charged under
    # `mandatory` or `optional`, both of which are `acquisition`, so the
    # incident it cited is an acquisition self-reference - and the notice it
    # emitted offered `acquisition` as the answer to it. Worse, it attributed
    # every moving path to `revision`: for `T-002`, whose `revision` is zero,
    # X-08 printed "revision ... non-monotonic in 2 path(s) ... (nothing
    # charged)" about two paths in `mandatory`.
    #
    # The movement is now attributed to the component that actually carries it,
    # and the gate is described as what it is - a dispatch-time measurement, not
    # an invariant.
    write = list(getattr(task, "write_scope", []))
    moving = sorted(
        {
            rel
            for _, rel, _ in ordered
            if any(glob_to_regex(p).match(rel) for p in write)
        }
    )
    cc.non_monotonic = moving
    if moving:
        where = cc.moving_by_component()
        shown = "; ".join(f"{kind} {rel}" for kind, rel in where[:4])
        cc.notices.append(
            f"{task.task_id}: self-referential budget - {len(moving)} charged "
            f"path(s) lie inside this task's own write scope, so the figure "
            f"moves as the task works: {shown}"
            + (" ..." if len(where) > 4 else "")
            + f" - of the gated quantity, acquisition {cc.acquisition}, "
            f"{cc.acquisition_self_referential} is self-written and "
            f"{cc.acquisition_stable} is stable, so the gate is a DISPATCH-TIME "
            f"measurement and not an invariant of this task's execution; "
            f"revision {cc.revision} is reported beside it and "
            f"total_measurable {cc.total_measurable} bounds neither silently"
        )
    cc.notices.append(f"{task.task_id}: telemetry {TELEMETRY_NOTE}")
    return cc
