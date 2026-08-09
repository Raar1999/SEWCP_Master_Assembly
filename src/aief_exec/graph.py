"""Task classification: BLOCKED, SERIAL, CONFLICT, PARALLEL.

Actor provenance: software.software-engineer - S-2026-08-09-01.

Implements EXECUTION_ARCHITECTURE.md sections 6.1 and 7. Every classification is
**computed** from declared scopes and edges; none is recorded by hand, so none can
go stale.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aief_exec import RESULTS_DIR, records, scope

BLOCKED = "BLOCKED"
SERIAL = "SERIAL"
CONFLICT = "CONFLICT"
PARALLEL = "PARALLEL"


@dataclass
class Currency:
    result_id: str
    status: str            # CURRENT | STALE | SUPERSEDED | MISSING
    drifted: list[str] = field(default_factory=list)

    @property
    def usable(self) -> bool:
        return self.status == "CURRENT"


#: Prefix of the one drifted-reason string that means a historical record was
#: altered after it was closed. X-06 raises this to a failure; everything else
#: on a superseded record is reported and does not fail.
REWRITTEN = "REWRITTEN AFTER SUPERSESSION"

#: The three hazard classes `conflict_reasons` can report. Every reason string
#: it emits is prefixed with exactly one of these, so a reader - and X-07, and
#: `aief_exec classify` - can tell which hazard fired without parsing prose.
#:
#: ``write/write``    two tasks write the same path: lost update.
#: ``write/read``     one task writes inside the other's *read surface* - every
#:                    component of `acquisition`, not `mandatory` alone: its own
#:                    task record, its mandatory and optional inputs, and the
#:                    result records it consumes. What the reader must hold
#:                    before it acts changes under it. The component that
#:                    carried the hazard is named in the reason.
#: ``write/observe``  one task writes inside the other's *observation surface*:
#:                    the watcher's acceptance evidence is taken over a tree the
#:                    writer is changing. Evidence contamination, not data loss -
#:                    both tasks can succeed and the evidence still be worthless.
HZ_WRITE_WRITE = "write/write"
HZ_WRITE_READ = "write/read"
HZ_WRITE_OBSERVE = "write/observe"

#: Command tokens that read the working tree. Their presence in an acceptance
#: criterion's `test` string is the *only* signal the repository has that a task
#: takes evidence from somewhere it never names. See `undeclared_observation`.
OBSERVATION_TOKENS = ("pytest", "git status", "git diff", "python -m")


@dataclass(frozen=True)
class Link:
    """The successor link a single record asserts, read from both its fields.

    `VER-009` FIND-Q9-51 and FIND-Q9-52. A record states its supersession twice -
    `supersedes: <id>` and `supersedes_seal.path: <that record's file>` - and
    before this class the repository held **two definitions of what a link is**:
    `successor_of` read `supersedes` alone, and `checks._corroborates` accepted
    either field. The gap between them was the attack. Deleting one line,
    `supersedes:  R-012`, from `R-013` left the seal block and its correct digest
    of `R-012` untouched; the cross-check saw the seal and stayed quiet, while
    `successor_of` saw no successor and took the *unsealed* branch, so `R-012`
    became freely rewritable with `X-06 PASS`. The digest that would have
    convicted the tamperer was sitting in the repository and no code compared it.

    There is one definition now and both fields feed it. `declared` and `sealed`
    are the two assertions; `target` is the link; `divergent` is the case where
    the record asserts two different predecessors, which is a contradiction the
    record makes with itself and which `X-06` fails on rather than resolving.
    """

    declared: str
    sealed: str

    @property
    def target(self) -> str:
        """The predecessor, preferring the declaration when both agree."""
        return self.declared or self.sealed

    @property
    def targets(self) -> tuple[str, ...]:
        """Every predecessor this record asserts. More than one is `divergent`."""
        return tuple(dict.fromkeys(t for t in (self.declared, self.sealed) if t))

    @property
    def exists(self) -> bool:
        return bool(self.targets)

    @property
    def divergent(self) -> bool:
        return len(self.targets) > 1


def canonical_path(raw: str) -> str:
    """A declared repository-relative path reduced to one spelling.

    `VER-009` V-2. `seal_target` normalised backslashes and then compared the
    result to a literal prefix, so seven spellings of a **real, existing**
    predecessor file - `./.ai/…`, `.ai/project/results//R-013.md`,
    `…/../results/R-013.md`, and case variants - each yielded no link at all.
    Silently: nothing reported a seal that named nothing. Inserting two
    characters into a seal path was therefore a way to delete the seal limb
    while leaving a block that still *looks* like a correct, digested seal, and
    the record's residue was the exact shape §6.4's table blesses as sufficient.

    Separator noise is collapsed here so those spellings resolve. Case is
    **not** folded: `.ai/project/Results/…` is a different declaration, and the
    answer to a non-canonical spelling is to report it (`X-06`), not to guess at
    it. What must never happen again is neither - resolving nothing and saying
    nothing.
    """
    parts: list[str] = []
    for seg in raw.replace("\\", "/").strip().split("/"):
        if seg in ("", "."):
            continue
        if seg == "..":
            if parts:
                parts.pop()
            continue
        parts.append(seg)
    return "/".join(parts)


def seal_path(result: records.ResultRecord) -> str:
    """The declared `supersedes_seal.path`, canonicalised. `""` if none."""
    raw = str(result.supersedes_seal.get("path") or "").strip()
    return canonical_path(raw) if raw else ""


def seal_target(result: records.ResultRecord) -> str:
    """The predecessor id named by `supersedes_seal.path`, or `""`.

    The path must be exactly `<RESULTS_DIR>/<R-NNN>.md` once canonicalised.
    `_corroborates` matched on the **basename** alone, which was tolerable while
    the match only corroborated a link something else had already established. It
    establishes the link now, so the match is anchored to the directory results
    actually live in and to the result-id form: a seal pointing at
    `notes/R-011.md` names no result record and creates no link.

    Returning `""` is not the end of it. A non-empty path that resolves to no
    result id is a **dangling seal** and `X-06` fails on it - see V-2. This
    function decides what the path names; it does not decide that saying nothing
    is an acceptable answer.
    """
    norm = seal_path(result)
    if not norm:
        return ""
    prefix, suffix = f"{RESULTS_DIR}/", ".md"
    if not (norm.startswith(prefix) and norm.endswith(suffix)):
        return ""
    rid = norm[len(prefix) : -len(suffix)]
    return rid if records.RESULT_ID.match(rid) else ""


def link_of(result: records.ResultRecord) -> Link:
    """**The one authoritative reading of a record's successor link.**

    Nothing else may decide whether a record supersedes another. `successor_of`,
    `supersession_seal` and `X-06`'s cross-check all route through this, so the
    seal machinery and the check that polices it can no longer hold different
    beliefs about the same two records - which is the whole content of
    FIND-Q9-51.
    """
    return Link(declared=result.supersedes, sealed=seal_target(result))


def is_successor_link(result: records.ResultRecord, predecessor_id: str) -> bool:
    """Whether `result` asserts, from its own side, that it supersedes
    `predecessor_id` - under the one definition."""
    return bool(predecessor_id) and predecessor_id in link_of(result).targets


def successors_of(
    results: dict[str, records.ResultRecord], result_id: str
) -> list[str]:
    """Every record asserting itself the successor of `result_id`.

    More than one is *competing successors*: the chain's `produced_by` provenance
    is underivable while they disagree, and `successor_of` picking the first in
    sort order would make the choice silently. `X-06` fails on the list being
    longer than one, so the choice is never silent.
    """
    return [
        rid
        for rid in sorted(results)
        if rid != result_id and is_successor_link(results[rid], result_id)
    ]


def successor_of(
    results: dict[str, records.ResultRecord], result_id: str
) -> str:
    """The record that asserts it supersedes `result_id`, if one exists.

    FIND-Q9-51: this read `supersedes` alone and was the single point of truth
    for the entire seal mechanism, so one deleted line disarmed it. It reads the
    link, not the field. A successor that has deleted `supersedes` but kept its
    seal is still a successor here, and its seal is still compared.
    """
    found = successors_of(results, result_id)
    return found[0] if found else ""


def derived_status(
    results: dict[str, records.ResultRecord], result: records.ResultRecord
) -> str:
    """SUPERSEDED when a successor says so, whatever the record says of itself.

    The same rule FIND-Q9-18 forced on BLOCKED: a state that can be asserted by
    the party it describes is a state that can go stale, and does. Supersession
    is a fact established by the **successor**, so it is read from the successor.
    A record still declaring CURRENT after something supersedes it is then a
    visible disagreement rather than a silent one.
    """
    if successor_of(results, result.result_id):
        return "SUPERSEDED"
    return result.status or "CURRENT"


#: The session from which a supersession must carry a seal. **A declared
#: constant, not a derived value** - see `seal_epoch`.
SEAL_EPOCH = "S-2026-08-09-06"


def derived_seal_epoch(results: dict[str, records.ResultRecord]) -> str:
    """The earliest session that actually published a seal, read off the records.

    **Evidence, never the rule.** This is the derivation `seal_epoch` used to
    be and no longer is; it is retained so `X-06` can report a disagreement
    between what the records show and what `SEAL_EPOCH` declares - a seal
    published earlier than the constant means the constant is late, and a
    derivation that has gone empty while sealed records exist means seals have
    been removed. Both are facts a reviewer should see. Neither decides
    anything, which is the entire point of separating them.
    """
    sessions = [
        str(r.produced_by.get("session") or "")
        for r in results.values()
        if link_of(r).exists and str(r.supersedes_seal.get("digest") or "")
    ]
    sessions = [s for s in sessions if records.SESSION_ID.match(s)]
    return min(sessions) if sessions else ""


def seal_epoch(results: dict[str, records.ResultRecord] | None = None) -> str:
    """The session from which an unsealed supersession is a failure, not history.

    `R-001` and `R-007` are superseded by records that pin no digest of them, so
    a post-supersession rewrite of either is undetectable. That is reported (as a
    notice, by `result_currency`) and must not become a retroactive failure: the
    seal did not exist when those records were written, and failing a record for
    not carrying a field that post-dates it is a rule applied backwards. The
    epoch is the discriminator between *history* and a *present-tense omission*:
    a successor published at or after it and carrying no seal fails X-06; one
    published before it is reported and never failed.

    **`VER-009` FIND-Q9-39: the epoch is declared, not derived.** The
    predecessor of this function took `min()` over the records that carry a
    seal, and `result_currency` claimed in terms that "tampering can only add
    the alarm, never remove it". Both were wrong one level up. Removing the
    `supersedes_seal` block from `R-009`, `R-010` and `R-011` - the successors,
    which is exactly where the claim said the evidence safely lived - emptied
    the derivation, and an empty epoch makes the rule vacuous for **every**
    record at once: `X-06` returned PASS with zero details after a three-record
    tamper. A control whose evidence base is the set of files a tampering party
    is already editing can be switched off by the tampering it exists to expose.

    A constant cannot be emptied by editing records. `SEAL_EPOCH` is
    `S-2026-08-09-06`, the session in which `R-009` published the first seal
    over `R-008`; the authority for that value is `R-009.produced_by.session`
    as published, independently recomputed and matched in `VER-009` section 26,
    and it is recorded in `.ai/project/EXECUTION_ARCHITECTURE.md` section 6.2 so
    that it lives outside this module as well as inside it. (`VER-009`
    FIND-Q9-48: this citation and the `X-06` notice that prints it both said
    §6.1, which is *Immutability without new machinery*. §6.2 is
    *The seal epoch*. The wrong pointer was emitted to the operator in exactly
    the tamper case the notice exists to report.) Advancing it is a
    deliberate act with a reviewable diff, which is what it should always have
    been.

    `results` is accepted and deliberately unused: the signature is kept so that
    no caller can pass a set of records and receive an answer computed from
    them. `derived_seal_epoch` still reads the records, and `X-06` reports where
    the two disagree.

    Three residuals, stated rather than hidden:

    * The constant is a claim about history and is only as good as the review
      that set it. It is checkable - `derived_seal_epoch` recomputes it - and
      `X-06` prints the comparison on every run.
    * A successor that declares a `produced_by.session` earlier than the epoch
      still evades the rule. That evasion is a false session identifier, a
      different defect from an absent seal, and this function does not pretend
      to catch it.
    * The epoch decides *whether an absent seal is a failure*. It does not
      decide whether a present seal matches; that is `result_currency`, and it
      is per-record and unaffected.
    """
    return SEAL_EPOCH


def supersession_seal(
    results: dict[str, records.ResultRecord], result_id: str
) -> tuple[str, str]:
    """The successor of `result_id` and the digest it sealed, if either exists.

    A seal is written by the **successor**, at supersession, over the predecessor
    file as a whole. It cannot be written by the record it protects, which is the
    only reason it protects anything.

    FIND-Q9-51: it is also, now, one of the two fields that *establish* the link
    this function follows. The seal can therefore no longer be orphaned from the
    relationship it seals - deleting the successor's `supersedes` leaves the seal
    standing and the seal alone still names the predecessor, so this returns the
    digest and `result_currency` compares it.
    """
    rid = successor_of(results, result_id)
    if not rid:
        return "", ""
    return rid, str(results[rid].supersedes_seal.get("digest") or "")


def result_currency(
    repo: Path,
    result: records.ResultRecord,
    results: dict[str, records.ResultRecord] | None = None,
) -> Currency:
    """Section 6.1: recompute every pinned input DC-1 against the working tree.
    Any difference makes the result STALE."""
    declared = derived_status(results or {}, result)
    if declared == "SUPERSEDED":
        # VER-009 FIND-Q9-27, then FIND-Q9-28. The predecessor of this branch
        # flagged a superseded record when **all** its pins matched the tree, on
        # the theory that a historical record's pins should have decayed. That
        # test is inverted and anti-monotonic, and pass 4 demonstrated both: it
        # fired on R-001, whose six pins are inputs T-001 was forbidden to touch,
        # and stayed silent on R-007, the one record here that actually was
        # rewritten after supersession. Rewriting a digest in R-001 on a scratch
        # copy *silenced* the notice while all eight checks stayed PASS - the
        # guard rewarded the tampering it existed to expose, because what it
        # really measured was whether the tree had moved, not whether the record
        # had.
        #
        # A record is compared against its own published bytes instead. At
        # supersession the successor seals the predecessor's DC-1; from then on
        # any edit to the predecessor changes its digest and the alarm fires.
        #
        # WHAT IS GUARANTEED, exactly - VER-009 FIND-Q9-39 falsified the
        # stronger claim that stood here. This comment used to read "the control
        # is monotonic by construction: tampering can only add the alarm, never
        # remove it, because the evidence lives in a different file from the one
        # being protected". That is true of one link and false of the chain. The
        # guarantee is:
        #
        #   * **Per link, once a seal exists**: no edit to the predecessor can
        #     reduce the alarm, because the digest it is compared against is in
        #     the successor. `TestSupersessionSeal` asserts this as a property
        #     over arbitrary edits, not as a case.
        #   * **Not** across the chain. The evidence lives in the *successor*,
        #     which is a file, which a tampering party editing the chain is
        #     already editing. Deleting a successor's `supersedes_seal` deletes
        #     that link's alarm along with its failure. What no longer follows
        #     from that deletion is the collapse of every other link:
        #     `seal_epoch` is a declared constant, so a stripped seal published
        #     at or after it is an X-06 failure on the successor whether or not
        #     any seal survives anywhere.
        #
        # Where no seal exists the answer is "this cannot be decided", said out
        # loud. A control that cannot see is not the same as a control that sees
        # nothing wrong, and reporting the difference is the whole lesson of the
        # finding.
        successor, sealed = supersession_seal(results or {}, result.result_id)
        if not sealed:
            why = (
                f"{successor} supersedes it but pins no digest of it"
                if successor
                else "no record declares that it supersedes this one"
            )
            return Currency(
                result.result_id,
                "SUPERSEDED",
                [
                    f"unsealed - {why}, so a rewrite after supersession cannot be "
                    f"detected here; the successor should carry supersedes_seal"
                ],
            )
        actual = records.file_dc1(repo, result.path)
        if actual is None:
            return Currency(
                result.result_id,
                "SUPERSEDED",
                [f"{REWRITTEN}: the record file is absent from the working tree"],
            )
        if actual != sealed:
            return Currency(
                result.result_id,
                "SUPERSEDED",
                [
                    f"{REWRITTEN}: DC-1 {actual} does not match the digest "
                    f"{sealed} that {successor} sealed at supersession"
                ],
            )
        return Currency(result.result_id, "SUPERSEDED")
    drift: list[str] = []
    for label, entries in (
        ("input", result.inputs),
        ("deliverable", result.deliverables),
    ):
        for entry in entries:
            rel = str(entry.get("path") or "")
            pinned = str(entry.get("digest") or "")
            actual = records.file_dc1(repo, rel)
            if actual is None:
                drift.append(f"{label} {rel}: absent from the working tree")
            elif actual != pinned:
                drift.append(f"{label} {rel}: DC-1 {actual} != pinned {pinned}")
    if drift:
        return Currency(result.result_id, "STALE", drift)
    return Currency(result.result_id, "CURRENT")


def currencies(repo: Path, results: dict[str, records.ResultRecord]) -> dict[str, Currency]:
    return {rid: result_currency(repo, r, results) for rid, r in results.items()}


def transitive_deps(tasks: dict[str, records.TaskRecord], task_id: str) -> set[str]:
    """Transitive closure of `depends_on`. Terminates on a cycle rather than
    recursing - `cycles()` reports the cycle separately."""
    seen: set[str] = set()
    stack = list(tasks[task_id].depends_on) if task_id in tasks else []
    while stack:
        nxt = stack.pop()
        if nxt in seen:
            continue
        seen.add(nxt)
        if nxt in tasks:
            stack.extend(tasks[nxt].depends_on)
    return seen


def cycles(tasks: dict[str, records.TaskRecord]) -> list[list[str]]:
    """Section 12 X-05, mirroring V-02: the graph must be acyclic."""
    found: list[list[str]] = []
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {t: WHITE for t in tasks}

    def walk(node: str, path: list[str]) -> None:
        colour[node] = GREY
        for nxt in tasks[node].depends_on:
            if nxt not in tasks:
                continue
            if colour[nxt] == GREY:
                found.append([*path[path.index(nxt):], node, nxt])
            elif colour[nxt] == WHITE:
                walk(nxt, [*path, nxt])
        colour[node] = BLACK

    for t in sorted(tasks):
        if colour[t] == WHITE:
            walk(t, [t])
    return found


def _granted_roles(repo: Path, task: records.TaskRecord) -> set[str]:
    """Mirrors checks._grant: a role grant counts only when the authority it
    cites is recorded somewhere that exists and actually carries the id.
    VER-009 FIND-Q9-17."""
    from aief_exec import checks
    covered, _, err = checks._grant(task, "role_authority", repo)
    if err:
        return set()
    return {str(r).strip().lower() for r in covered}


def blocked_reasons(
    repo: Path,
    task: records.TaskRecord,
    tasks: dict[str, records.TaskRecord],
    results: dict[str, records.ResultRecord],
    curr: dict[str, Currency],
    open_items: set[str],
    roster: dict[str, bool] | None = None,
) -> list[str]:
    """Section 7, BLOCKED."""
    out: list[str] = []
    # TPL-task-package acceptance condition 1: a role marked UNASSIGNED cannot be
    # dispatched. That bars execution of THIS task, so it is a blocking reason.
    # An unassigned verifier bars closure, not execution - verification is a
    # downstream task carrying its own record and its own roster requirement.
    if roster is not None and task.status != "COMPLETE":
        role = str(task.data.get("role") or "").strip().lower()
        if role and role not in _granted_roles(repo, task) and roster.get(role) is False:
            out.append(
                f"role {role} is UNASSIGNED in ROSTER.md (OI-P-02) - "
                f"a role marked UNASSIGNED cannot be dispatched; assignment is a "
                f"project-manager action"
            )
    for dep in task.depends_on:
        if dep not in tasks:
            out.append(f"depends_on {dep} does not exist")
        elif tasks[dep].status != "COMPLETE":
            out.append(f"depends_on {dep} is {tasks[dep].status or 'unset'}, not COMPLETE")
    for rid in task.consumes:
        if rid not in results:
            out.append(f"consumes {rid} which has not been published")
            continue
        c = curr[rid]
        if not c.usable:
            detail = f" ({'; '.join(c.drifted)})" if c.drifted else ""
            # Name the successor. A consumer of a superseded result is blocked
            # deliberately - the successor's conclusion is not guaranteed to say
            # what the predecessor's said, so re-pointing is a decision, not a
            # lookup, and the layer does not take it silently. Naming it costs
            # nothing and turns the block into an instruction.
            successor = successor_of(results, rid) if c.status == "SUPERSEDED" else ""
            fix = (
                f" - re-point consumes to {successor} after reading its conclusion"
                if successor
                else ""
            )
            out.append(f"consumes {rid} which is {c.status}{detail}{fix}")
    for item in task.blocked_by:
        if item in open_items:
            out.append(f"blocked_by open item {item}")
    return out


def observed_surface(
    repo: Path,
    task: records.TaskRecord,
    results: dict[str, records.ResultRecord] | None = None,
    paths: list[str] | None = None,
) -> list[str]:
    """The tree a task must observe stably for its acceptance criteria to hold.

    Write scope and mandatory read scope model *what a task touches*. Neither
    models *what a task looks at to decide it succeeded*, and the two are not the
    same set. A verifier that reproduces a producer's test suite reads no file
    the producer writes and writes no file the producer writes, yet its evidence
    is worthless if the suite moves underneath it while it runs. `T-004`'s
    evidence is `pytest tests/` and `git status --porcelain`; before this
    function existed those appeared in the repository only as English inside
    `acceptance_criteria[].test`, where no comparison could reach them.

    Derived, with an optional declared extension - four terms, unioned:

    1. `write_scope`. A task observes what it writes; that is what makes an
       overlap with another writer a hazard twice over.
    2. Deliverable entries that resolve to real paths today. A task that revises
       an existing artifact is watching it.
    3. Every path pinned in the `deliverables` of each consumed result. This is
       the term that catches the real incident: the consumer never names those
       paths, the *result it consumes* does, and they are exactly the paths whose
       stability the consumed conclusion depends on.
    4. The record's optional declared `observes` list, for surfaces the first
       three cannot reach.

    Returns patterns, not concrete paths - concrete paths are patterns without
    wildcards - so the caller compares with `scope.scopes_intersect` and gets the
    same exact algebra used for write scopes.
    """
    out: list[str] = []

    def add(pattern: object) -> None:
        text = str(pattern or "").strip()
        if text and text not in out:
            out.append(text)

    for pattern in task.write_scope:
        add(pattern)
    resolved, _ = scope.deliverable_paths(repo, task, paths)
    for rel in resolved:
        add(rel)
    for rid in getattr(task, "consumes", []):
        result = (results or {}).get(rid)
        if result is None:
            continue
        for entry in result.deliverables:
            add(entry.get("path"))
    for pattern in task.observes:
        add(pattern)
    return out


def read_surface(
    repo: Path,
    task: records.TaskRecord,
    results: dict[str, records.ResultRecord] | None = None,
) -> list[tuple[str, str]]:
    """`(component, path)` for everything a task must read before it acts.

    **The repair for `VER-009` FIND-Q9-38.** `conflict_reasons` compared three
    surfaces - write scope, mandatory read scope, observation surface - while
    `scope.charged_context` charged five. The cost model therefore *knew about*
    reads the hazard model could not see, and four hazard classes escaped
    through the gap. Three of them were live or demonstrated:

    * **optional read scope.** Never compared. The auditor's matched-pair
      control was byte-identical but for the declaration class: the same path
      declared `optional` classified PARALLEL, declared `mandatory` classified
      CONFLICT. A budget charges both; a hazard model that compares one is
      deciding safety on a label.
    * **the consumed result record itself.** `observed_surface` adds the
      *deliverables* a consumed result pins and never
      `.ai/project/results/R-nnn.md`. A consumer must read that file to
      establish the record is CURRENT and unsuperseded - which is precisely why
      `charged_context` charges it whole under `dependency`.
    * **the task's own record.** On no surface at all: not write, not read, not
      observed. `X-08` charges `T-002` 931 TF-1 and `T-005` 656 TF-1 for exactly
      that file under `record`, while `classify T-001 T-002` returned PARALLEL
      and `T-001.write_scope` covers `.ai/project/tasks/**` - a verdict
      certifying that one task may rewrite another's objective, acceptance
      criteria, write scope and budget while that task executes.

    Because the enumeration is `scope.acquisition_units`, the same call the cost
    model makes, the asymmetry cannot be reintroduced by editing one model: a
    component added to `acquisition` is charged and compared in one edit.

    **What this does not close, stated so no reader mistakes coverage.** Two
    escapes remain open and disclosed. *Runtime tooling* - `T-002` writes
    `src/aief_stage6/tokenizers.py`, the backend every figure `T-004` reports
    flows through, and no declared surface names it, so `T-002 x T-004` is still
    PARALLEL. Closing it means modelling an import graph, which is a different
    kind of artefact from a declared scope. *Undeclared observation* - see
    `undeclared_observation`, which is a heuristic notice and says so.
    """
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for kind, rel, _ in scope.acquisition_units(task, results):
        if rel and rel not in seen:
            seen.add(rel)
            out.append((kind, rel))
    return out


def undeclared_observation(task: records.TaskRecord) -> list[str]:
    """Notices for evidence this layer can see the shape of but not the extent of.

    **A heuristic notice, not a decision procedure.** An acceptance criterion
    reading `pytest tests/` is prose; the repository has no execution trace, no
    tool log and no way to know which files a command touched. What is testable
    is narrow and stated as such: the `test` string contains a token that names a
    tree-reading command, and the record declares no `observes`. That pairing
    means the task's evidence surface *may* exceed what is declared. It is not a
    claim that an undeclared observation was detected, and the absence of a
    notice is not a claim that none exists.

    Deliberately no attempt is made to parse a path, a glob or a target out of
    the surrounding sentence. Guessing `tests/` out of "the same 4 pre-existing
    failures" would be resolving an ambiguity by assumption - LAW-12 - and would
    convert an honest "cannot see" into a confident wrong answer.
    """
    if task.observes:
        return []
    out: list[str] = []
    for entry in task.data.get("acceptance_criteria") or []:
        if not isinstance(entry, dict):
            continue
        text = str(entry.get("test") or "")
        found = sorted({t for t in OBSERVATION_TOKENS if t in text})
        if not found:
            continue
        out.append(
            f"{task.task_id} {entry.get('id') or '?'}: this task's evidence surface "
            f"may exceed what is declared - its acceptance test names "
            f"{', '.join(repr(t) for t in found)}, which reads the working tree, "
            f"and the record declares no `observes`. Heuristic: what that command "
            f"actually reads is not recoverable from the repository"
        )
    return out


#: What each acquisition component means when a writer reaches it. Printed in
#: the `write/read` reason so the three hazard tags stay three while the
#: hazard's *substance* is still named - FIND-Q9-38 kept the taxonomy flat and
#: pushed the detail into the sentence.
COMPONENT_HAZARD = {
    "record": "the contract it is executing",
    "mandatory": "a declared mandatory input",
    "optional": "a declared optional input",
    "dependency": "the result record whose currency it must confirm",
}


def _reached(
    repo: Path,
    write: list[str],
    surface: list[tuple[str, str]],
    paths: list[str] | None = None,
) -> list[tuple[str, str]]:
    """Which entries of a read surface a write scope reaches, entry by entry.

    Deliberately not `scopes_intersect` over the whole surface at once. That
    call answers *whether* the two sets meet and returns concrete witnesses when
    any exist, so an entry that overlaps only at pattern level - a declared read
    of a file that does not exist yet - is invisible whenever some other entry
    happens to exist on disk. The per-entry form loses nothing: its disjunction
    is the same verdict, and it can name every entry and every component that
    was reached rather than the subset that happened to be on disk.
    """
    return [
        (kind, rel)
        for kind, rel in surface
        if scope.scopes_intersect(repo, write, [rel], paths)
    ]


def _components(reached: list[tuple[str, str]]) -> str:
    """Name the acquisition components the reach actually landed in."""
    kinds = sorted({kind for kind, _ in reached})
    return ", ".join(f"{k} - {COMPONENT_HAZARD.get(k, k)}" for k in kinds)


def conflict_reasons(
    repo: Path,
    a: records.TaskRecord,
    b: records.TaskRecord,
    paths: list[str] | None = None,
    results: dict[str, records.ResultRecord] | None = None,
    surfaces: dict[str, list[str]] | None = None,
) -> list[str]:
    """Section 7, CONFLICT. Three hazard classes, separately named.

    The first two are the original test: write scopes intersect (`write/write`),
    or one write scope intersects the other's read surface (`write/read`).

    `write/read` compares `read_surface`, which is every component of
    `acquisition` and not `mandatory` alone - FIND-Q9-38. The three classes are
    kept distinct rather than multiplied: which *component* carried the hazard
    is named inside the reason, so a reader can tell a rewritten contract
    (`record`) from a rewritten input (`mandatory`, `optional`) from a rewritten
    upstream conclusion (`dependency`) without a fourth tag to parse.

    The third is `write/observe` - one task writes inside the other's
    `observed_surface`. It is a distinct hazard, not a variant of the other two:
    no path is lost and no declared input changes, yet the watcher's acceptance
    evidence is taken over a tree the writer is moving, so both tasks can report
    success over evidence that was never valid. Every reason carries its hazard
    class as a prefix so the three stay distinguishable in output.

    Because `observed_surface` includes the task's own write scope, a
    `write/write` pair also reports `write/observe`. That is not double counting:
    an overlapping write scope really is both a lost-update hazard and an
    evidence hazard, and collapsing them would hide one of the two.

    `results` and `surfaces` are caching parameters. Passing neither is correct
    and loads the result records; `build_plan` passes both because it compares
    every pair.
    """
    out: list[str] = []
    if results is None:
        results = records.load_results(repo)

    def witnesses(hit: object) -> str:
        if isinstance(hit, set):
            names = sorted(hit)
            shown = ", ".join(names[:3])
            return shown + (f" (+{len(names) - 3} more)" if len(names) > 3 else "")
        return "pattern-level overlap, no existing witness"

    hit = scope.scopes_intersect(repo, a.write_scope, b.write_scope, paths)
    if hit:
        out.append(
            f"[{HZ_WRITE_WRITE}] lost update - write scopes intersect: "
            f"{witnesses(hit)}"
        )
    for writer, reader in ((a, b), (b, a)):
        surface = read_surface(repo, reader, results)
        reached = _reached(repo, writer.write_scope, surface, paths)
        if reached:
            named = [rel for _, rel in reached]
            shown = ", ".join(named[:3]) + (
                f" (+{len(named) - 3} more)" if len(named) > 3 else ""
            )
            out.append(
                f"[{HZ_WRITE_READ}] input drift - {writer.task_id} writes what "
                f"{reader.task_id} must read before it acts "
                f"({_components(reached)}): {shown}"
            )
    for writer, watcher in ((a, b), (b, a)):
        surface = (surfaces or {}).get(watcher.task_id)
        if surface is None:
            surface = observed_surface(repo, watcher, results, paths)
        hit = scope.scopes_intersect(repo, writer.write_scope, surface, paths)
        if hit:
            out.append(
                f"[{HZ_WRITE_OBSERVE}] evidence contamination - {writer.task_id} "
                f"writes inside {watcher.task_id}'s observation surface, so "
                f"{watcher.task_id}'s acceptance evidence is taken over a tree "
                f"{writer.task_id} is changing: {witnesses(hit)}"
            )
    return out


def safety_explanation(
    repo: Path,
    a: records.TaskRecord,
    b: records.TaskRecord,
    paths: list[str] | None = None,
    results: dict[str, records.ResultRecord] | None = None,
    surfaces: dict[str, list[str]] | None = None,
) -> list[str]:
    """Why a PARALLEL verdict is safe: every surface compared, and the result.

    A bare `PARALLEL` is an assertion. This is the working: the five comparisons
    the verdict rests on, each with the two surfaces that were compared and
    whether their intersection was empty. A reader can disagree with a line of
    it, which is the whole point - an unexplained safe verdict cannot be
    challenged, only trusted. It works: `VER-009`'s pass-5 headline finding was
    obtained by reading this output, so the explanation falsified the verdict it
    was written to explain.

    The `write/read` lines print `read_surface`, component-tagged, so the
    surface a reader is invited to challenge is the same one `X-08` charges -
    FIND-Q9-38. Five lines, one per comparison, unchanged in number: the extra
    surfaces widened each comparison rather than adding new ones.
    """
    if results is None:
        results = records.load_results(repo)
    lines: list[str] = []

    def surface_of(task: records.TaskRecord) -> list[str]:
        got = (surfaces or {}).get(task.task_id)
        return got if got is not None else observed_surface(repo, task, results, paths)

    def show(patterns: list[str]) -> str:
        return "{" + ", ".join(patterns) + "}" if patterns else "{} (empty)"

    def compare(label: str, left: list[str], right: list[str]) -> None:
        hit = scope.scopes_intersect(repo, left, right, paths)
        if not hit:
            verdict = "intersection EMPTY"
        elif isinstance(hit, set):
            verdict = "intersects at " + ", ".join(sorted(hit)[:3])
        else:
            verdict = "intersects at pattern level"
        lines.append(f"{label}: {show(left)} vs {show(right)} -> {verdict}")

    compare(
        f"{HZ_WRITE_WRITE}  {a.task_id}.write x {b.task_id}.write",
        a.write_scope,
        b.write_scope,
    )
    for writer, reader in ((a, b), (b, a)):
        surface = read_surface(repo, reader, results)
        compare(
            f"{HZ_WRITE_READ}   {writer.task_id}.write x "
            f"{reader.task_id}.read (record + mandatory + optional + dependency)",
            writer.write_scope,
            [f"{rel}" for _, rel in surface],
        )
    for writer, watcher in ((a, b), (b, a)):
        compare(
            f"{HZ_WRITE_OBSERVE} {writer.task_id}.write x {watcher.task_id}.observed",
            writer.write_scope,
            surface_of(watcher),
        )
    return lines


@dataclass
class Plan:
    states: dict[str, str]
    blocked: dict[str, list[str]]
    pairs: dict[tuple[str, str], tuple[str, list[str]]]
    cycles: list[list[str]]
    currency: dict[str, Currency]
    #: task id -> its derived observation surface, computed once per plan.
    surfaces: dict[str, list[str]] = field(default_factory=dict)

    def runnable(self) -> list[str]:
        return sorted(t for t, s in self.states.items() if s not in (BLOCKED, "COMPLETE"))

    def parallel_sets(self) -> list[list[str]]:
        """Groups whose members are pairwise PARALLEL. A group is a safe
        concurrent dispatch.

        **First-fit greedy in identifier order, and not maximal.** `VER-009`
        FIND-Q9-40: this said "maximal groups", which first-fit does not
        deliver - a later identifier may be excluded from a group it would fit
        because an earlier one claimed a member it conflicts with. The docstring
        was corrected rather than the algorithm, deliberately:

        * maximal grouping is maximum-clique-cover, NP-hard, and the payoff is a
          possibly larger dispatch batch, not a safer one;
        * **safety does not depend on it.** Every group is pairwise PARALLEL by
          construction and `X-07` re-verifies each group pairwise from the plan,
          so a suboptimal grouping dispatches fewer tasks at once and never an
          unsafe pair.

        What the greedy pass costs is throughput, and what it buys is a
        deterministic, reviewable grouping. Overstating it as maximal cost
        nothing operationally and cost a reader their accuracy, which is the
        defect class this audit has tracked throughout.
        """
        groups: list[list[str]] = []
        for t in self.runnable():
            for g in groups:
                if all(self.pairs[tuple(sorted((t, m)))][0] == PARALLEL for m in g):
                    g.append(t)
                    break
            else:
                groups.append([t])
        return groups


def build_plan(repo: Path) -> Plan:
    tasks = records.load_tasks(repo)
    results = records.load_results(repo)
    open_items = records.open_item_ids(repo)
    curr = currencies(repo, results)
    paths = scope.tree(repo)
    roster = {r.strip().lower(): ok for r, ok in records.roster(repo).items()}

    blocked: dict[str, list[str]] = {}
    states: dict[str, str] = {}
    for tid, task in tasks.items():
        reasons = blocked_reasons(
            repo, task, tasks, results, curr, open_items, roster
        )
        blocked[tid] = reasons
        # VER-009 FIND-Q9-18: the first form fell back to `task.status`, so a
        # record declaring BLOCKED derived BLOCKED whether or not a blocker
        # existed, and half the X-02 cross-check was dead code. BLOCKED is now
        # never taken from the declaration - it is derived, always, so an
        # over-declared block is as visible as an under-declared one.
        if task.status == "COMPLETE":
            states[tid] = "COMPLETE"
        elif reasons:
            states[tid] = BLOCKED
        elif task.status in ("AWAITING-DECISION", "ACTIVE"):
            states[tid] = task.status
        else:
            states[tid] = "READY"

    # Computed once per plan rather than once per pair: `observed_surface`
    # resolves deliverables against the tree, and the pair loop is quadratic.
    surfaces = {
        tid: observed_surface(repo, task, results, paths)
        for tid, task in tasks.items()
    }

    pairs: dict[tuple[str, str], tuple[str, list[str]]] = {}
    ids = sorted(tasks)
    for i, a in enumerate(ids):
        for b in ids[i + 1 :]:
            key = (a, b)
            ta, tb = tasks[a], tasks[b]
            if b in transitive_deps(tasks, a):
                pairs[key] = (SERIAL, [f"[serial/dependency] {a} depends on {b}"])
                continue
            if a in transitive_deps(tasks, b):
                pairs[key] = (SERIAL, [f"[serial/dependency] {b} depends on {a}"])
                continue
            # VER-009 FIND-Q9-41: CONFLICT was evaluated first, so a pair that
            # cannot be co-dispatched at all was reported as a scope hazard. The
            # operative class is now the one that decides dispatchability - a
            # blocked member ends the question - and BLOCKED is tested first.
            #
            # Nothing is lost by the reorder, which is the condition on making
            # it: any scope reasons found are appended to the blocked reasons
            # rather than discarded, so a pair that is both blocked and
            # conflicting reports both facts and the hazard survives the block
            # being cleared.
            #
            # COMPLETE is deliberately NOT folded in. A COMPLETE task cannot be
            # dispatched either, but it also cannot be repaired by clearing a
            # precondition, and calling such a pair BLOCKED would hide a live
            # scope hazard behind a state that will never change: `T-001` is
            # COMPLETE and holds `.ai/project/tasks/**`, and `T-001 x T-002`
            # must read CONFLICT so that the reach over another task's contract
            # is visible. `runnable()` already keeps COMPLETE tasks out of every
            # dispatch group, so no safety rests on the pair class here.
            reasons = conflict_reasons(repo, ta, tb, paths, results, surfaces)
            blockers = [f"[blocked/precondition] {r}"
                        for group in (blocked[a], blocked[b]) for r in group]
            if blockers:
                pairs[key] = (BLOCKED, blockers + reasons)
                continue
            if reasons:
                pairs[key] = (CONFLICT, reasons)
                continue
            pairs[key] = (PARALLEL, [])

    return Plan(
        states=states,
        blocked=blocked,
        pairs=pairs,
        cycles=cycles(tasks),
        currency=curr,
        surfaces=surfaces,
    )


def classify(repo: Path, a: str, b: str) -> tuple[str, list[str]]:
    plan = build_plan(repo)
    return plan.pairs[tuple(sorted((a, b)))]
