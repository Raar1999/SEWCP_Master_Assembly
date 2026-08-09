"""Execution checks X-01 to X-10.

Actor provenance: software.software-engineer - S-2026-08-09-01.

Implements EXECUTION_ARCHITECTURE.md section 12. `V-01`...`V-25` is the manifest's
namespace and adding to it would require an amendment; these checks are separate,
project-scoped, and add nothing to `manifest.validation`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from aief_exec import PROTECTED_WRITE, RESULTS_DIR, STATE_HEADINGS, records, scope
from aief_exec import graph as _graph


def _result(
    cid: str, name: str, details: list[str], notices: list[str] | None = None
) -> dict[str, Any]:
    """`notices` carry facts a reviewer must see even when the check passes.

    VER-009 FIND-Q9-1: an exemption that produces no output is a silent
    exemption. A granted reach into the protected set is lawful, but it is never
    invisible.
    """
    return {
        "id": cid,
        "name": name,
        "status": "FAIL" if details else "PASS",
        "details": details,
        "notices": notices or [],
    }


def _grant(task: Any, field: str, repo: Path) -> tuple[set[str], str, str | None]:
    """An enumerated authority grant.

        {paths|roles: [...], id: <token>, recorded_at: <path>, citation: "..."}

    VER-009 raised the same defect twice - FIND-Q9-1 against `write_authority`
    and FIND-Q9-17 against `role_authority`: an exemption written by the party
    it constrains and validated only for shape. Its closing judgment is the
    specification for this function: *"until a citation resolves against an
    approval, decision record or ledger entry, these fields record an intention
    rather than establish an authority."*

    So a grant must now name **where** the authority is recorded, that path must
    exist, and the declared `id` must actually appear in it. A grant whose
    citation cannot be found in the artifact it names is not an authority.

    Returns (covered, citation, error).
    """
    raw = task.data.get(field)
    if raw in (None, "", {}):
        return set(), "", None
    if not isinstance(raw, dict):
        return set(), "", (
            f"{field} must enumerate what it grants as "
            f"{{paths|roles: [...], id: ..., recorded_at: ..., citation: ...}}, "
            f"not free text"
        )
    key = "paths" if field == "write_authority" else "roles"
    covered = {str(x) for x in (raw.get(key) or [])}
    citation = str(raw.get("citation") or "").strip()
    ident = str(raw.get("id") or "").strip()
    recorded_at = str(raw.get("recorded_at") or "").strip()
    if not covered:
        return set(), "", f"{field} declares no {key}"
    if not citation:
        return set(), "", f"{field} carries no citation"
    if not ident or not recorded_at:
        return set(), "", (
            f"{field} must declare `id` and `recorded_at` - a citation that "
            f"names no recorded authority is an intention, not an authority"
        )
    target = repo / recorded_at
    if not target.is_file():
        return set(), "", (
            f"{field}.recorded_at {recorded_at!r} does not exist, so the "
            f"authority it claims cannot be inspected"
        )
    try:
        body = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return set(), "", f"{field}.recorded_at is unreadable: {exc}"
    if ident not in body:
        return set(), "", (
            f"{field}.id {ident!r} does not appear in {recorded_at} - the "
            f"cited authority is not recorded there"
        )
    return covered, f"{ident} recorded at {recorded_at}", None


def x01_record_conformance(repo: Path) -> dict[str, Any]:
    """Every task record parses and carries the SCH-task required fields plus the
    extension fields."""
    details: list[str] = []
    notices: list[str] = []
    try:
        tasks = records.load_tasks(repo)
        known = {r.strip().lower(): ok for r, ok in records.roster(repo).items()}
    except (records.RecordError, OSError) as exc:
        return _result("X-01", "Record conformance", [str(exc)])
    if not tasks:
        details.append("no task records found")
    for tid, task in sorted(tasks.items()):
        for fld in records.SCH_TASK_REQUIRED:
            if task.data.get(fld) in (None, "", [], {}):
                details.append(f"{tid}: SCH-task required field {fld!r} is absent or empty")
        for fld in records.EXTENSION_REQUIRED:
            if task.data.get(fld) in (None, ""):
                details.append(f"{tid}: extension field {fld!r} is absent")
        if task.status and task.status not in STATE_HEADINGS.values():
            details.append(f"{tid}: status {task.status!r} is not a declared state")

        # VER-009 FIND-Q9-6: the first form compared raw strings, so a rename or
        # a case change defeated LAW-05 and an unregistered verifier passed.
        # Roles are now normalised and both ends must resolve in the roster.
        role = str(task.data.get("role") or "").strip().lower()
        qa = task.data.get("qa") or {}
        verifier = str(qa.get("verifier_role") or "").strip().lower()
        if not verifier:
            details.append(f"{tid}: qa.verifier_role is absent")
        elif verifier == role:
            details.append(
                f"{tid}: qa.verifier_role equals role {verifier!r} - LAW-05 forbids "
                f"self-verification"
            )

        granted, citation, err = _grant(task, "role_authority", repo)
        if err:
            details.append(f"{tid}: {err}")
            granted = set()
        # An unregistered role is a record defect. An UNASSIGNED one is a state
        # fact - TPL-task-package says such a role "cannot be dispatched", which
        # is dispatchability, not conformance - so it is derived as a blocking
        # reason in graph.blocked_reasons and reported here only as a notice.
        for label, value in (("role", role), ("qa.verifier_role", verifier)):
            if not value:
                continue
            if value not in known:
                details.append(
                    f"{tid}: {label} {value!r} does not appear in project/ROSTER.md"
                )
            elif not known[value]:
                if value in {g.strip().lower() for g in granted}:
                    notices.append(
                        f"{tid}: {label} {value} is UNASSIGNED and dispatched under a "
                        f"declared role_authority - {citation}"
                    )
                else:
                    notices.append(
                        f"{tid}: {label} {value} is UNASSIGNED in project/ROSTER.md "
                        f"(OI-P-02) - the task is blocked until a project-manager "
                        f"assigns it"
                    )
    return _result("X-01", "Record conformance", details, notices)


def x02_index_bijection(repo: Path) -> dict[str, Any]:
    """EXEC.md and tasks/ are bijective by identifier, and the index conforms to
    the AIEF-AMD-014 AMD-49 grammar."""
    details: list[str] = []
    try:
        idx = records.load_index(repo)
        tasks = records.load_tasks(repo)
    except (records.RecordError, OSError) as exc:
        return _result("X-02", "Index bijection", [str(exc)])
    listed = idx.ids
    for tid in listed:
        if listed.count(tid) > 1:
            details.append(f"{tid}: listed {listed.count(tid)} times in the index")
    for tid in sorted(set(listed)):
        if tid not in tasks:
            details.append(f"{tid}: in the index with no record under tasks/")
    for tid in sorted(tasks):
        if tid not in listed:
            details.append(f"{tid}: has a record but is not listed in the index")
            continue
        want = idx.state_of(tid)
        got = tasks[tid].status
        if want != got:
            details.append(f"{tid}: index section says {want}, record says {got}")
    for heading in idx.sections:
        if heading not in STATE_HEADINGS:
            details.append(f"index heading {heading!r} is not a declared state")

    # The declared status and the derived state must agree. Without this the
    # index could file a task as READY while the derivation blocks it, and a
    # dispatcher reading only the index would act on the stale side.
    plan = _graph.build_plan(repo)
    for tid, derived in sorted(plan.states.items()):
        declared = tasks[tid].status
        if derived == _graph.BLOCKED and declared != _graph.BLOCKED:
            details.append(
                f"{tid}: derived BLOCKED ({plan.blocked[tid][0]}) but filed as "
                f"{declared}"
            )
        if declared == _graph.BLOCKED and derived != _graph.BLOCKED:
            details.append(
                f"{tid}: filed as BLOCKED but the derivation finds no blocker"
            )
    return _result("X-02", "Index bijection", sorted(set(details)))


def x03_read_scope_resolves(repo: Path) -> dict[str, Any]:
    """Every mandatory and optional read-scope entry resolves, and each anchor
    yields a non-empty excerpt."""
    details: list[str] = []
    tasks = records.load_tasks(repo)
    paths = scope.tree(repo)
    for tid, task in sorted(tasks.items()):
        forbidden = task.forbidden_reads
        for kind in ("mandatory", "optional"):
            for entry in task.read_entries(kind):
                try:
                    scope.resolve_entry(repo, entry)
                except scope.ScopeError as exc:
                    details.append(f"{tid} [{kind}]: {exc}")
                    continue
                rel = str(entry.get("path") or "")
                if forbidden and scope.scopes_intersect(repo, [rel], forbidden, paths):
                    details.append(
                        f"{tid} [{kind}]: {rel} is inside this task's own forbidden "
                        f"read scope - a task may not widen its scope by declaring it"
                    )
                # VER-009 FIND-Q9-7: substring anchors matched first-hit-wins and
                # ambiguity was silent. An anchor that selects more than one
                # section does not identify a section.
                anchor = entry.get("anchor")
                if anchor and not rel.endswith(".json"):
                    n = scope.heading_matches(
                        (repo / rel).read_text(encoding="utf-8"), str(anchor)
                    )
                    if n > 1:
                        details.append(
                            f"{tid} [{kind}]: anchor {anchor!r} matches {n} headings "
                            f"in {rel} - an ambiguous anchor identifies nothing"
                        )
        for entry in task.read_entries("dependency"):
            rid = str(entry.get("result") or "")
            if not rid:
                details.append(f"{tid}: dependency read entry names no result")
            elif rid not in task.consumes:
                details.append(
                    f"{tid}: dependency read names {rid} which is not in consumes"
                )
    return _result("X-03", "Read-scope resolution", details)


def x04_write_scope_containment(repo: Path) -> dict[str, Any]:
    """No write scope reaches the framework-protected set **undeclared**.

    A reach that is declared with a cited `write_authority` is lawful - Compiler
    Stage 6 is the emitting authority for layer L7 and must write
    `core/MANIFEST.lock`. The defect this check exists to catch is the silent
    reach, not the authorised one.
    """
    details: list[str] = []
    notices: list[str] = []
    tasks = records.load_tasks(repo)
    paths = scope.tree(repo)
    for tid, task in sorted(tasks.items()):
        if not task.write_scope:
            details.append(f"{tid}: write_scope is empty")
            continue
        granted, citation, err = _grant(task, "write_authority", repo)
        if err:
            details.append(f"{tid}: {err}")
            granted = set()
        for pattern in task.write_scope:
            hit = scope.scopes_intersect(repo, [pattern], list(PROTECTED_WRITE), paths)
            if not hit:
                continue
            witness = sorted(hit)[:3] if isinstance(hit, set) else ["pattern-level"]
            if pattern not in granted:
                details.append(
                    f"{tid}: write_scope {pattern!r} reaches the protected set "
                    f"({', '.join(witness)}) and is not enumerated in "
                    f"write_authority.paths"
                )
            else:
                # Lawful, but never silent - FIND-Q9-1.
                notices.append(
                    f"{tid}: {pattern} reaches the protected set under a declared "
                    f"grant - {citation}"
                )
        for pattern in granted:
            if pattern not in task.write_scope:
                details.append(
                    f"{tid}: write_authority grants {pattern!r} which is not in "
                    f"write_scope - a grant may not exceed the scope it qualifies"
                )
        for pattern in task.forbidden_reads:
            hit = scope.scopes_intersect(repo, task.write_scope, [pattern], paths)
            if hit:
                details.append(
                    f"{tid}: write_scope intersects its own forbidden read {pattern!r}"
                )
    return _result("X-04", "Write-scope containment", details, notices)


def x05_graph_sound(repo: Path) -> dict[str, Any]:
    """Acyclic; every depends_on, consumes and produces target exists."""
    details: list[str] = []
    tasks = records.load_tasks(repo)
    results = records.load_results(repo)
    for cycle in _graph.cycles(tasks):
        details.append("cycle: " + " -> ".join(cycle))
    for tid, task in sorted(tasks.items()):
        for dep in task.depends_on:
            if dep not in tasks:
                details.append(f"{tid}: depends_on {dep} does not exist")
        for rid in task.consumes:
            if rid not in results:
                producers = [t for t in tasks.values() if rid in t.produces]
                if not producers:
                    details.append(
                        f"{tid}: consumes {rid} which no task produces and no record exists"
                    )
        for rid in task.produces:
            if rid in results:
                owner = results[rid].produced_by.get("task")
                if owner != tid:
                    details.append(
                        f"{tid}: produces {rid} but that record names producer {owner}"
                    )
    return _result("X-05", "Graph soundness", details)


# FIND-Q9-51. `_corroborates` stood here: a **second** definition of what a
# successor link is, accepting `supersedes` or a seal path while
# `graph.successor_of` accepted `supersedes` alone. Two definitions of one
# relationship is what the finding was, and adding a third here - even a correct
# one - would repeat it. The definition is `graph.link_of`, and this check reads
# it through `graph.is_successor_link` exactly as the seal machinery does.


def x06_result_currency(repo: Path) -> dict[str, Any]:
    """Every CURRENT result's pinned input digests match the working tree.

    Also: **a supersession published from the seal epoch onward must carry a
    seal.** `R-001` and `R-007` have successors that pin no digest of them, so a
    post-supersession rewrite of either is undetectable. That is reported as a
    notice and is deliberately not a failure - the seal did not exist when those
    successors were written, and a rule applied backwards fails records for
    omitting a field that post-dates them.

    The discriminator is `graph.seal_epoch`, a **declared constant**. At or
    after that session the convention was demonstrably in use, so a missing seal
    is an omission and this check fails on the **successor** that omitted it.
    The predecessor-side notice is untouched and still says what it always said,
    so the two historical records stay reported rather than accused.

    `VER-009` FIND-Q9-39: the epoch used to be `min()` over the records that
    carried a seal, which meant deleting every seal emptied the epoch and made
    the rule vacuous for all six records at once - X-06 PASS, zero details,
    after a three-record tamper. A rule derived from the data it polices can be
    switched off by editing that data. The rule is now a constant and the
    derivation is retained only as **evidence**: `graph.derived_seal_epoch` is
    recomputed on every run and any disagreement with the constant is printed
    as a notice, in both directions. A derivation that has gone empty while the
    constant stands is exactly the tamper signature, and it is now visible
    instead of silencing.

    **`VER-009` FIND-Q9-43: the link is declared twice, and both declarations
    are now read.** Pinning the epoch hardened the *discriminator* and left the
    *trigger* under the tamperer's hand: the rule above is guarded by
    `if result.supersedes and not <seal>`, and `result.supersedes` is a line in
    a file the tampering party is already editing. Deleting `supersedes: R-011`
    and its seal from `R-012` - two lines, one record - returned this check to
    PASS with a single notice, after which appending `TAMPERED: ...` to `R-011`
    raised nothing at all.

    The repository already held the contradicting evidence and discarded it.
    `R-011` carries `superseded_by: R-012`; every superseded record here
    carries the field, and no code read it. So the predecessor's declaration is
    now compared against the successor's, in both directions:

    * `A` declares `superseded_by: B` and no record `B` exists - **FAIL**.
    * `A` declares `superseded_by: B`, `B` exists, and `B` neither declares
      `supersedes: A` nor pins a `supersedes_seal` naming `A` - **FAIL**. Two
      records disagree about whether a supersession happened, and the check
      does not get to choose which one is lying.
    * `B` declares `supersedes: A` while `A` declares `superseded_by: C`,
      `C != B` - **FAIL**, the same disagreement from the other side.
    * `A` is superseded and declares no `superseded_by` at all - **notice**. A
      missing back-link is not a contradiction, it is this control going blind
      for that link, and saying so is not the same as saying nothing is wrong.
      Requiring the field would be a schema change and is not this check's to
      make (LAW-12).

    **`VER-009` FIND-Q9-51 and FIND-Q9-52: the repair above created the next
    bypass, and this is its closure.** The cross-check was given its own
    predicate, `_corroborates`, which accepted `supersedes` **or** a
    `supersedes_seal.path` naming the predecessor. `graph.successor_of` accepted
    `supersedes` alone. One relationship, two definitions, and the difference
    between them was a one-line disarm: delete `supersedes:  R-012` from
    `R-013`, leave the seal block and its correct digest of `R-012` in place, and
    the cross-check saw a link while the seal machinery saw none - `X-06 PASS`,
    then `R-012` rewritten with no alarm. Cheaper than the two-line attack the
    predecessor of this docstring had just closed. On an interior link
    (`R-011`/`R-012`) it broke no test either.

    There is one definition now - `graph.link_of` - and it reads **both** fields.
    Three consequences, and they are the closure:

    * A seal-only successor is a successor. `graph.successor_of` follows the
      link, `supersession_seal` returns the digest, and `result_currency`
      compares it. The digest that FIND-Q9-51 observed "sitting in the
      repository with no code path comparing it" is compared.
    * A record whose `supersedes` and seal name **different** predecessors is a
      self-contradiction and fails, above. Two representations of one link may
      no longer disagree quietly, which is the property FIND-Q9-51 was raised
      about.
    * This check no longer holds a private opinion about what a link is. It asks
      `graph.is_successor_link`, the same function `successor_of` is built from,
      so the two halves of the mechanism cannot drift apart again.

    **Why the seal limb is kept rather than deleted.** MU30 - deleting the
    seal-path limb of `_corroborates` - survived the suite, and the audit read
    that as evidence the limb should go. Deleting it would have restored one
    definition by making `supersedes` the sole field again, which is the
    condition every one of the four recorded disarms depends on: *one editable
    line, and the seal machinery is blind*. Unifying upward instead makes the
    seal load-bearing, so the field that carries the evidence is also a field
    that establishes the link, and neither can be removed without the other
    becoming visible. The limb is not redundant under the unified relationship -
    it is the half that survives the deletion attack - and the check that made it
    redundant-looking is the one that was removed.

    **What `R-001` and `R-007` cost.** They declare their supersessions and pin
    no digest, because the convention post-dates them. Reading the seal as a link
    does not touch them: they have no seal, so their link is the declaration
    alone, exactly as before, and the epoch rule still reports rather than fails
    them (§6.2).

    **Residual, stated rather than hidden - and corrected.** The predecessor of
    this paragraph claimed the remaining attack cost "three edits across two
    files rather than two edits in one". FIND-Q9-51 falsified that: at the time
    it was written the cost was **one edit in one file**. The claim was wrong and
    is withdrawn. What stands now: stripping `superseded_by` from the
    predecessor *and* both `supersedes` and the seal from the successor removes
    every assertion that the link existed, and the records no longer contradict
    each other. What remains is `A` declaring `status: SUPERSEDED` with no
    successor anywhere - reported by `result_currency` as unsealed and not
    failed, because a record may be retired without a successor and deciding
    otherwise is a schema question (LAW-12). That is three edits across two
    files, **measured, not asserted**: `TestSupersessionLinkIsOneDefinition`
    executes the one- and two-edit attacks and requires `X-06` to fail on both,
    and executes the three-edit attack and records that it passes. It is a
    narrowing, not a closure, and the boundary is now a test rather than a
    sentence.
    """
    details: list[str] = []
    notices: list[str] = []
    results = records.load_results(repo)
    epoch = _graph.seal_epoch(results)
    derived = _graph.derived_seal_epoch(results)
    if derived != epoch:
        notices.append(
            f"seal epoch: declared {epoch} (graph.SEAL_EPOCH, recorded at "
            f"EXECUTION_ARCHITECTURE.md section 6.2); earliest seal actually "
            f"present in the records is "
            f"{derived or 'NONE - no record carries a supersedes_seal'}. The "
            f"declared value governs and the records do not move it. Reported "
            f"because the two disagreeing is itself evidence: a derivation "
            f"earlier than the constant means the constant is late, and one "
            f"that has emptied while sealed supersessions existed means seals "
            f"have been removed"
        )
    for rid, result in sorted(results.items()):
        link = _graph.link_of(result)
        # FIND-Q9-51, the divergence case the two definitions could never see.
        # A record asserting `supersedes: A` and sealing `B` contradicts itself
        # about which record it closed. Under one definition it is a successor of
        # both, so `produced_by` provenance forks at this record. The check does
        # not pick a side.
        if link.divergent:
            details.append(
                f"{rid}: declares supersedes {link.declared} but pins a "
                f"supersedes_seal over {RESULTS_DIR}/{link.sealed}.md - one "
                f"record, two different predecessors. The declaration and the "
                f"seal are the two halves of one link (FIND-Q9-51) and they "
                f"disagree, so which record {rid} closed is underivable and its "
                f"seal protects neither. Repair: set {rid}.supersedes and "
                f"{rid}.supersedes_seal.path to the same record"
            )
        # V-2 and V-4. A seal block that names nothing, and a seal block whose
        # path is not where its predecessor lives, were both silent. Silence is
        # what made them attacks: a two-character edit to the path voided the
        # seal limb while leaving a block a reviewer reads as a correct,
        # digested seal, and renaming the predecessor's file left the seal
        # pointing at a path that does not exist with nothing reporting it.
        # A declared seal must name a result record, and it must name the file
        # that record is actually in.
        #
        # VER-010 F-1 and F-2. The guard was `if _graph.seal_path(result)`, and
        # that function returns "" for a declared path that canonicalises to
        # nothing as well as for no declaration at all. So `./`, `.`, `..`,
        # `/`, `//`, `../..` and whitespace-only were read as "no seal here" and
        # skipped the check in silence - the V-2 attack, reproduced inside the
        # V-2 repair. Declaredness is now read from the raw declaration and from
        # the block, neither of which any canonicalisation can empty.
        declared_raw = _graph.seal_declared(result)
        declared_path = _graph.seal_path(result)
        if _graph.seal_declared_block(result) and not declared_raw:
            details.append(
                f"{rid}: carries a supersedes_seal block that declares no path "
                f"- {sorted(result.supersedes_seal)} and no usable `path`. A "
                f"seal names the record it seals; this one names nothing, so "
                f"its digest is over an unstated subject and nothing can be "
                f"compared against it (F-2). Repair: set "
                f"{rid}.supersedes_seal.path, or remove the block if {rid} "
                f"supersedes nothing"
            )
        elif declared_raw and not link.sealed:
            details.append(
                f"{rid}: pins a supersedes_seal over {declared_raw!r}"
                + (
                    f" (canonically {declared_path!r})"
                    if declared_path and declared_path != declared_raw
                    else ""
                )
                + f", which names no result record - a result file is "
                f"{RESULTS_DIR}/R-nnn.md and this is not one. The block carries "
                f"a digest and establishes no link, so it reads as a seal and "
                f"protects nothing (V-2, F-1). A path is not canonical if it "
                f"needs `..` resolved, starts at the filesystem root, or "
                f"differs in case - each names a different file to a reader, or "
                f"a different file from where the reader stands. Repair: set "
                f"{rid}.supersedes_seal.path to "
                f"{RESULTS_DIR}/{link.declared or 'R-nnn'}.md, or remove the "
                f"block if {rid} supersedes nothing"
            )
        elif link.sealed in results and results[link.sealed].path != declared_path:
            details.append(
                f"{rid}: pins a supersedes_seal whose path is {declared_path!r}, "
                f"but {link.sealed} is at {results[link.sealed].path!r}. The "
                f"digest is taken over the record's real file while the seal "
                f"declares a different one, so the subject of the seal and the "
                f"file actually compared are not reconciled (V-4). Repair: set "
                f"{rid}.supersedes_seal.path to {results[link.sealed].path}"
            )
        # The symmetric half of the `superseded_by` existence check below, which
        # the link direction never had. A record claiming to supersede something
        # that is not in the repository has closed nothing, and its seal - if it
        # carries one - protects a file no result record corresponds to.
        for target in link.targets:
            if target not in results:
                details.append(
                    f"{rid}: declares that it supersedes {target}, but no such "
                    f"result record exists. A supersession names a record that "
                    f"can be read; this one names nothing, so nothing was "
                    f"closed and no seal over it can be verified. Repair: "
                    f"correct {rid}.supersedes and {rid}.supersedes_seal.path, "
                    f"or clear both if {rid} supersedes nothing"
                )
        # The successor side of FIND-Q9-28. `result_currency` reports the
        # predecessor's blind spot; nothing reported the record that created it.
        #
        # FIND-Q9-51: the guard was `if result.supersedes`, a single editable
        # field, so deleting that line skipped the epoch rule entirely. It is the
        # link that triggers the rule now, and the link survives the deletion.
        if link.exists and not str(result.supersedes_seal.get("digest") or ""):
            session = str(result.produced_by.get("session") or "")
            if epoch and records.SESSION_ID.match(session) and session >= epoch:
                details.append(
                    f"{rid}: supersedes {link.target} and pins no "
                    f"supersedes_seal, but was published at session {session}, at "
                    f"or after {epoch} - the session in which a seal was first "
                    f"published, so the convention was in use. Repair: set "
                    f"{rid}.supersedes_seal to {{path: "
                    f"{RESULTS_DIR}/{link.target}.md, digest: <DC-1 of that "
                    f"file as published>}}"
                )
            else:
                notices.append(
                    f"{rid}: supersedes {link.target} and pins no "
                    f"supersedes_seal. Session {session or 'unset'} predates "
                    f"{epoch or 'any sealed supersession'}, so this is history and "
                    f"is reported, not failed - the predecessor's rewrite window "
                    f"stays open and undetectable"
                )
    # FIND-Q9-43. The predecessor's half of the link, read for the first time
    # and compared against the successor's. Both directions, so neither record
    # can retire the control by editing itself.
    for rid, result in sorted(results.items()):
        declared_successor = result.superseded_by
        found = _graph.successors_of(results, rid)
        actual_successor = found[0] if found else ""
        # FIND-Q9-51. Two records asserting they closed the same predecessor is
        # a fork in the chain, and `successor_of` returning the first in sort
        # order would choose between them silently. Reported here whether or not
        # the predecessor carries a back-link, because the contradiction is
        # between the successors and does not need the predecessor's help.
        if len(found) > 1:
            details.append(
                f"{rid}: {' and '.join(found)} each assert that they supersede "
                f"{rid} - competing successors. A record has one successor; "
                f"`produced_by` provenance for the chain past {rid} is "
                f"underivable while they disagree, and only one of their seals "
                f"can be the seal that closed it. Repair: withdraw the "
                f"supersession the chain did not take"
            )
        if declared_successor:
            other = results.get(declared_successor)
            if other is None:
                details.append(
                    f"{rid}: declares superseded_by {declared_successor}, but no "
                    f"such result record exists. A supersession names a record "
                    f"that can be read; this one names nothing. Repair: publish "
                    f"{declared_successor}, or correct {rid}.superseded_by"
                )
            elif not _graph.is_successor_link(other, rid):
                details.append(
                    f"{rid}: declares superseded_by {declared_successor}, but "
                    f"{declared_successor} declares supersedes "
                    f"{other.supersedes or 'nothing'} and carries no "
                    f"supersedes_seal over {rid}. The two records contradict "
                    f"each other about "
                    f"whether this supersession happened, and deleting the "
                    f"successor's half is exactly how the seal is disarmed "
                    f"(FIND-Q9-43): with no `supersedes` there is no seal to "
                    f"require, and {rid} becomes rewritable undetected. Repair: "
                    f"set {declared_successor}.supersedes to {rid} and pin "
                    f"{declared_successor}.supersedes_seal over "
                    f"{RESULTS_DIR}/{rid}.md, or clear {rid}.superseded_by if "
                    f"the supersession did not happen - one of the two "
                    f"declarations is wrong"
                )
            elif actual_successor and actual_successor != declared_successor:
                details.append(
                    f"{rid}: declares superseded_by {declared_successor}, but "
                    f"{actual_successor} is the record that declares it "
                    f"supersedes {rid}. Two successors is no successor: "
                    f"`produced_by` provenance for the chain is underivable "
                    f"while they disagree"
                )
        elif actual_successor:
            notices.append(
                f"{rid}: {actual_successor} declares that it supersedes this "
                f"record, and {rid} declares no superseded_by. The link is "
                f"asserted by one record only, so the cross-check that detects "
                f"a deleted `supersedes` (FIND-Q9-43) is blind for this link. "
                f"Reported, not failed: requiring the back-link is a schema "
                f"change and not this check's to make (LAW-12)"
            )
    for rid, result in sorted(results.items()):
        curr = _graph.result_currency(repo, result, results)
        derived = _graph.derived_status(results, result)
        # Supersession is established by the successor, so a record still
        # declaring itself CURRENT under one is a declared/derived disagreement -
        # the defect class X-02 already fails on for task states.
        if derived == "SUPERSEDED" and result.status != "SUPERSEDED":
            details.append(
                f"{rid}: {_graph.successor_of(results, rid)} declares that it "
                f"supersedes {rid}, but {rid} still declares status "
                f"{result.status or 'unset'!r} - closing the superseded record is "
                f"what supersession consists of"
            )
        elif result.status == "CURRENT" and curr.status != "CURRENT":
            details.append(f"{rid}: declared CURRENT but is {curr.status}")
            details.extend(f"  {d}" for d in curr.drifted)
        # FIND-Q9-28: a historical record altered after supersession is an
        # integrity failure. An unsealed one is a control that cannot see, which
        # is reported and does not fail - saying "undecidable" is the point.
        if derived == "SUPERSEDED":
            for d in curr.drifted:
                (details if d.startswith(_graph.REWRITTEN) else notices).append(
                    f"{rid}: {d}"
                )
        for label, entries in (
            ("input", result.inputs),
            ("deliverable", result.deliverables),
        ):
            for entry in entries:
                digest = str(entry.get("digest") or "")
                if len(digest) != 64 or digest != digest.lower():
                    details.append(
                        f"{rid}: {label} {entry.get('path')} digest is not 64 "
                        f"lowercase hex (truncation is prohibited)"
                    )
        # FIND-Q9-3: a result that pins no deliverable cannot detect that its own
        # output moved after publication.
        if derived == "CURRENT" and not result.deliverables:
            details.append(
                f"{rid}: declares no pinned deliverables, so deliverable drift "
                f"after publication is undetectable"
            )
    return _result("X-06", "Result currency", details, notices)


def x07_no_concurrent_write_conflict(repo: Path) -> dict[str, Any]:
    """No two tasks dispatched together conflict on write, read or observation.

    The pairing itself is decided in `graph.conflict_reasons`, across three
    hazard classes; this check confirms the grouping honoured it and reports the
    limit of what the grouping can know.

    That limit is real and is stated as a notice rather than left implicit: an
    **undeclared** observation is undetectable. A task that runs `pytest tests/`
    without declaring `observes` has an evidence surface no comparison here can
    see, and a PARALLEL verdict for such a task is safe only with respect to what
    the record declares. See `graph.undeclared_observation` - the notice is a
    heuristic on the acceptance-criteria text, not a detection.
    """
    details: list[str] = []
    notices: list[str] = []
    plan = _graph.build_plan(repo)
    tasks = records.load_tasks(repo)
    for group in plan.parallel_sets():
        for i, a in enumerate(group):
            for b in group[i + 1 :]:
                kind, why = plan.pairs[tuple(sorted((a, b)))]
                if kind != _graph.PARALLEL:
                    details.append(
                        f"{a} and {b} share a dispatch group but classify {kind}: "
                        f"{'; '.join(why)}"
                    )
    for tid, task in sorted(tasks.items()):
        surface = plan.surfaces.get(tid) or []
        if task.observes:
            notices.append(
                f"{tid}: observation surface {len(surface)} pattern(s), including "
                f"{len(task.observes)} declared via `observes`"
            )
        notices.extend(_graph.undeclared_observation(task))
    return _result("X-07", "Concurrent write safety", details, notices)


def x08_context_budget(repo: Path) -> dict[str, Any]:
    """**One verdict, one quantity: the `acquisition` dispatch gate.**

    ``acquisition`` - the record, the resolved mandatory and optional read
        scope, and every consumed result record: what an agent must hold before
        it can start. A breach is a failure and refuses the dispatch. It is
        exact at dispatch time, it does **not** move when the task's deliverable
        is created, and it is not invariant across the task's own execution in
        the narrower sense described below.

    `revision` and `total_measurable` are measured here, reported here, and
    **gated nowhere in this check**. The bound on `total_measurable` is
    `X-10`, a separate check with a separate verdict.

    **VER-009 FIND-Q9-45 - why the bound left this check.** It used to be a
    second verdict here, against the same cap, appended to the same `details`
    list. `total_measurable >= acquisition` always, so `X-08` failed **iff**
    some task's `total_measurable` breached: the gate contributed nothing to
    the boolean that the bound did not already contribute, and the only thing
    separating the two rows was the English substring `NON-MONOTONIC BOUND`
    inside a detail string. A consumer of `X-08["status"]` could not tell them
    apart at all.

    The consequence was live and was the exact defect the acquisition/revision
    split had been built to retire, reinstated one level up at the check's
    verdict. `T-005` had **zero** rows here before it wrote
    `tests/test_stage6_crash_trials.py` and **two FAILs** after, with its
    acquisition gate under cap in both states. A check verdict that a task
    moves by doing its own work is not a dispatch gate.

    Splitting them, rather than folding them back together or inventing a
    second cap, is what makes each boolean mean something:

    * `X-08` fails iff an `acquisition` figure breaches - monotone with respect
      to deliverable creation, which is the property a dispatch gate needs.
    * `X-10` fails iff a `total_measurable` figure breaches - non-monotonic,
      and says so in its own name.

    Both can fail independently, and `row["id"]` tells a machine which did.
    Neither cap was changed to achieve this; the numbers are the same numbers.

    Four measurements, each wrong in a way the next repairs:

    VER-009 FIND-Q9-5. The first measured `mandatory` alone, so a task could
    declare four times its cap as `optional` and pass.

    VER-009 FIND-Q9-35. The second measured the resolved read scope and stopped,
    modelling a task as *what it reads to start*. It certified `T-004` at TF-1
    2,519 against a cap of 8,000 while the pass consumed roughly 22,000, because
    the dominant cost was `T-004`'s own deliverable.

    The third - the fix for FIND-Q9-35 - summed the two and gated the sum. That
    made the gate depend on whether the task had already run. `T-005` charged
    TF-1 1,411 against a cap of 1,500 before it ran and 7,161 after, the entire
    difference being the deliverable it had just written. A dispatch gate cannot
    be a function of the dispatch it gates, so the sum was split and only the
    part that does not move with the deliverable was gated.

    The fourth measured the right things and put two of them in one verdict;
    the fifth is this one, which keeps the measurement and separates the
    verdicts.

    **VER-009 FIND-Q9-37 - the gate bounds a minority of the cost, and that is
    `X-10`'s business now.** Excluding `revision` excludes 19,049 TF-1 for
    `T-004` (53% of its measurable total), 37,211 for `T-001` (85%) and 5,750
    for `T-005` (80%). For `T-004` the excluded item is `VER-009` itself, which
    `T-004`'s own AC-4 makes mandatory reading. A cap bounding 47% of an
    agent's required input with nothing bounding the rest is not a budget, and
    a footnote is not visibility - so the rest **is** bounded, by `X-10`, and
    `revision` is still not folded into this gate. Folding it in would restore
    the non-monotonicity the split was built to remove and refuse dispatches on
    a number the dispatch itself moves.

    **VER-009 FIND-Q9-36 / 36b - the gate is not invariant either, and the
    notice said the wrong thing about it.** `record` is an acquisition
    component and every task must update its own checkpoint, so wherever a
    task's record lies inside its own write scope the gated figure moves as the
    task works: 34% of `T-001`'s and 24% of `T-002`'s gated figures are
    self-written, and `T-002` is a live failure on a number it moves itself.
    Every task's charge is therefore reported as
    `acquisition = stable + self-referential`, both figures visible, and the
    moving paths are attributed to the component that actually holds them. The
    predecessor of this line appended the moving-path count to the *revision*
    clause, printing for `T-002` - whose revision is zero - "revision TF-1 0 ...
    non-monotonic in 2 path(s) ... (nothing charged)" about two paths in
    `mandatory`.

    `record` is not dropped from the gate to buy invariance. An agent genuinely
    must read its contract; removing real cost to make a number behave is the
    defect, not the repair.

    A task whose derived state is `COMPLETE` is measured and reported but not
    gated - it will not be dispatched again, so there is no dispatch to refuse.
    Every other derived state is pending dispatch.

    The correction is to the **measurement**, not to the numbers it is compared
    against. Caps live in task records and are a project-manager decision. Where
    an honest charge exceeds a cap, this check fails, and the failure is the
    finding rather than a defect in it.
    """
    details: list[str] = []
    notices: list[str] = []
    for row in _charged_rows(repo):
        tid, cc, budget, state, gated = row
        if not _measurable(row, "acquisition", details):
            continue
        _cap_verdict(
            row,
            "acquisition",
            cc.acquisition,
            f"({_breakdown(cc, scope.ACQUISITION_COMPONENTS)})",
            details,
            notices,
        )
        # Never a bare number, and never a merged one. The full split is printed
        # for every task whether or not it breached, because a reviewer cannot
        # judge a cap without seeing what it does and does not bound - and,
        # after FIND-Q9-36, without seeing how much of the gate the task itself
        # can move.
        #
        # FIND-Q9-46. This clause used to read "total_measurable {...} BOUNDED
        # by the same cap and failed separately", unconditionally, for every
        # task in every state - with no test on a breach and none on the
        # suppression that then existed. Live it was false for `T-002`, `T-003`
        # and `T-006`, whose `total_measurable` breached and for which no
        # separate failure was emitted, and false again for any task under cap,
        # for which there was nothing to fail. It now states only what is true
        # of every task in every state: the number, and which check compares it.
        # Whether that comparison failed is X-10's row to report, and a reader
        # who wants the verdict reads the verdict.
        notices.append(
            f"{tid} [{state}]: acquisition {cc.acquisition} GATED "
            f"({_breakdown(cc, scope.ACQUISITION_COMPONENTS)}) = stable "
            f"{cc.acquisition_stable} + self-referential "
            f"{cc.acquisition_self_referential} | revision {cc.revision} "
            f"measured and not gated here "
            f"({_breakdown(cc, scope.REVISION_COMPONENTS)}) | "
            f"total_measurable {cc.total_measurable} is compared against this "
            f"same cap by X-10, whose verdict is separate from this one "
            f"(FIND-Q9-45) | {_moving_clause(cc)} | telemetry "
            f"{cc.telemetry_note} - excluded from all three"
        )
        if cc.acquisition != cc.read_only_total:
            notices.append(
                f"{tid}: the read-scope-only measurement this replaces reported "
                f"{cc.read_only_total}"
            )
        notices.extend(cc.notices)
    return _result("X-08", "Context budget - acquisition gate", details, notices)


def x10_non_monotonic_measurable_bound(repo: Path) -> dict[str, Any]:
    """`acquisition + revision` against the declared cap. **NON-MONOTONIC.**

    The name is the warning. This check's verdict **moves when a task does its
    own work**: `revision` charges deliverables that already exist, so a task
    that writes the artifact it was contracted to write increases the quantity
    bounded here. `T-005` has no row at all before it creates
    `tests/test_stage6_crash_trials.py` and two failures after, on a cap it
    never approached before running. That is a property of the quantity, not a
    defect in the measurement, and it is the reason this bound is **not** a
    dispatch gate and must never be read as one. The gate is `X-08`.

    **Why it exists.** VER-009 FIND-Q9-37: the gate bounds a minority of what an
    agent must actually load - 47% for `T-004`, 15% for `T-001`, 20% for
    `T-005`. An excluded cost that appears only in a footnote is an invisible
    cost, so it is bounded, as a **detail** and never a notice, and the breach
    is a finding about the caps rather than about the measurement.

    **Why it is its own check.** VER-009 FIND-Q9-45: it used to be a second
    verdict inside `X-08`, against the same cap, in the same `details` list.
    Since `total_measurable >= acquisition` always, `X-08` then failed iff some
    `total_measurable` breached - the gate added nothing to the boolean - and
    the only discriminator between the two kinds of row was an English
    substring. Machines read `row["status"]`. Two checks, two ids, two
    booleans; a consumer that cares about dispatch reads `X-08` and a consumer
    that cares about total load reads this. Both may fail, independently, and
    which failed is now structural rather than lexical.

    **The same cap, deliberately.** The repository declares one
    `context_budget` per task and no second bound. Inventing one here would be
    resolving an ambiguity by assumption (LAW-12). Whether a distinct cap
    should exist for total load is a `project-manager` decision, and it is
    escalated, not pre-empted. Nothing in this repair changed a cap.

    **No suppression.** The predecessor emitted this verdict only where
    `revision` was non-zero, to avoid printing one overrun twice in one list.
    That reason died with the split - the rows are in different checks now -
    and keeping it would have made *this check's boolean* a function of whether
    `revision` happened to be zero, which is itself the non-monotonic quantity.
    A check whose verdict is a pure function of its own quantity is the whole
    point of the split. Where `revision` is zero the bound and the gate are the
    same number, both rows say so, and `X-08` and `X-10` fail together and
    honestly.

    A `COMPLETE` task is measured and reported but not failed, exactly as in
    `X-08`: there is no dispatch to refuse.
    """
    details: list[str] = []
    notices: list[str] = []
    for row in _charged_rows(repo):
        tid, cc, budget, state, gated = row
        if not _measurable(row, "total_measurable", details):
            continue
        same = " - equal to the acquisition gate, because revision is zero" if (
            cc.revision == scope.ZERO
        ) else ""
        _cap_verdict(
            row,
            "total_measurable",
            cc.total_measurable,
            f"(acquisition {cc.acquisition} + revision {cc.revision}, of "
            f"which {_breakdown(cc, scope.REVISION_COMPONENTS)}){same} - "
            f"NON-MONOTONIC BOUND, not the acquisition gate: `revision` is "
            f"real cost an agent must load, excluded from the gate because "
            f"the task's own output moves it, and bounded here rather than "
            f"left invisible. Repair: a cap decision, not a measurement "
            f"defect - the gate verdict for {tid} is X-08's",
            details,
            notices,
        )
        notices.append(
            f"{tid} [{state}]: total_measurable {cc.total_measurable} = "
            f"acquisition {cc.acquisition} + revision {cc.revision} "
            f"({_breakdown(cc)}), compared against the same declared cap "
            f"tf1={budget.get('tf1')} / tf2={budget.get('tf2')} that X-08's "
            f"gate uses, because the repository declares no second cap "
            f"(LAW-12) | {_moving_clause(cc)} | telemetry {cc.telemetry_note} "
            f"- excluded from this bound as well as from the gate"
        )
    return _result(
        "X-10", "Non-monotonic bound on total measurable context", details, notices
    )


#: One measured task: `(tid, charged context, declared budget, derived state,
#: whether a breach fails rather than merely reports)`.
Row = tuple[str, "scope.ChargedContext", dict[str, Any], str, bool]


def _charged_rows(repo: Path) -> list[Row]:
    """Every task, measured once, for both budget checks.

    FIND-Q9-45 split one check into two. The measurement is not split with it:
    `X-08` and `X-10` compare **the same numbers** against **the same caps**
    and differ only in which quantity each one's verdict is a function of. A
    second enumeration here would be a second place for the two to drift, which
    is the defect FIND-Q9-44 was raised about one module over.
    """
    tasks = records.load_tasks(repo)
    results = records.load_results(repo)
    paths = scope.tree(repo)
    states = _graph.build_plan(repo).states
    out: list[Row] = []
    for tid, task in sorted(tasks.items()):
        cc = scope.charged_context(repo, task, results, paths)
        state = states.get(tid) or "unknown"
        out.append(
            (tid, cc, task.data.get("context_budget") or {}, state, state != "COMPLETE")
        )
    return out


def _measurable(row: Row, quantity: str, details: list[str]) -> bool:
    """Whether `row` can be compared at all; records why not, and fails.

    A check that cannot evaluate its own quantity must not report PASS, so an
    unresolvable read scope, an unavailable tokenizer family or an undeclared
    cap is a failure in **both** budget checks. Each states it in terms of the
    quantity it was going to compare - two checks blinded by one record defect
    is two facts, not one repeated.
    """
    tid, cc, budget, state, _ = row
    if cc.errors:
        details.extend(f"{tid}: {e}" for e in cc.errors)
        return False
    if not cc.acquisition.measured:
        details.append(
            f"{tid}: {quantity} UNMEASURED - a tokenizer family is unavailable"
        )
        return False
    for fam in ("tf1", "tf2"):
        if budget.get(fam) is None:
            # A record without a cap is a record defect in any state.
            details.append(
                f"{tid}: context_budget.{fam} is not declared, so {quantity} "
                f"has nothing to be compared against"
            )
    # A partly-declared budget is still worth comparing on the family that does
    # have a cap, so an undeclared cap records the defect and does not
    # short-circuit the verdict.
    return True


def _cap_verdict(
    row: Row,
    label: str,
    value: scope.Cost,
    tail: str,
    details: list[str],
    notices: list[str],
) -> None:
    """Compare one quantity against the declared cap, per tokenizer family."""
    tid, _, budget, state, gated = row
    for fam, got in (("tf1", value.tf1), ("tf2", value.tf2)):
        cap = budget.get(fam)
        if cap is None or got is None or got <= int(cap):
            continue
        breach = (
            f"{tid}: {label} {fam.upper()} {got} exceeds declared cap {cap} {tail}"
        )
        if gated:
            details.append(breach)
        else:
            notices.append(
                f"{breach} - reported and not gated: {tid} is {state} and "
                f"will not be dispatched again"
            )


def _moving_clause(cc: scope.ChargedContext) -> str:
    """Which charged paths the task itself can move. FIND-Q9-36b."""
    where = cc.moving_by_component()
    if not where:
        return "no charged path lies inside this task's own write scope"
    return (
        f"non-monotonic in {len(where)} path(s) inside this task's own write "
        f"scope, by component: "
        + "; ".join(f"{kind} {rel}" for kind, rel in where[:4])
        + (" ..." if len(where) > 4 else "")
    )


def _breakdown(cc: scope.ChargedContext, names: tuple[str, ...] | None = None) -> str:
    parts = []
    for name in names or (*scope.ACQUISITION_COMPONENTS, *scope.REVISION_COMPONENTS):
        c = cc.component_total(name)
        if c.tf1:
            parts.append(f"{name} {c.tf1}")
    return (" + ".join(parts) + " TF-1") if parts else "nothing charged"


def x09_publication_reachability(repo: Path) -> dict[str, Any]:
    """A declared `produces` can be written, and a declared `consumes` can be met.

    Reproduced defect. `produces: [R-nnn]` appears in six task records. In five
    of them no `write_scope` pattern matches `.ai/project/results/R-nnn.md`, so
    the task is contracted to publish a record it is forbidden to create. `T-006`
    then consumes `R-002` and `R-003`, whose producers are in exactly that
    position: a structural deadlock, in which no lawful sequence of dispatches
    can ever make `T-006` runnable.

    Nothing saw it. `produces` and `consumes` are in neither
    `records.SCH_TASK_REQUIRED` nor `records.EXTENSION_REQUIRED`, so X-01 never
    looks at them; X-05 checks that their targets *exist* as graph nodes, which
    is a different question from whether the channel between them can carry
    anything. This check is that question.

    Five failure modes, each stated with the exact repair:

    1. `produces: R` with no `write_scope` pattern matching `R`'s record path.
    2. `consumes: R` where no task anywhere declares `produces: R` - the result
       can never be refreshed or republished, whatever is on disk today.
    3. Two tasks declaring `produces` of the same `R` - an ambiguous producer,
       so `produced_by` cannot be derived and neither can precedence between
       two writers of one record.
    4. `consumes: R` where `R` is neither on disk nor produced by anything -
       the strictly stronger case of 2, and a deadlock rather than a fragility.
       X-05 reports the same fact as graph unsoundness; the wording here is the
       publication channel's, and the two are meant to agree.
    5. **The converse of 1** - `write_scope` reaching an `R` the task does not
       declare in `produces`. `VER-009` FIND-Q9-42: modes 1 and 3 protect the
       invariant that *"a result has exactly one producer"*, and both tested it
       against `produces` **declarations** while nothing tested it against
       `write_scope` **reach**. Live, `T-001.write_scope` reaches `R-002`
       through `R-006`, five records it does not produce, and X-09 emitted
       nothing. Compounded by FIND-Q9-38 that was concrete: `T-001 x T-002` was
       PARALLEL, so `T-001` could publish `R-002` beside its declared producer
       with all nine checks clean. Mode 1 asks whether the declared producer
       *can* write; mode 5 asks whether anyone else *can*, and one direction is
       not a guard.

       Open decision A4 is load-bearing here and is not pre-empted: this mode
       reports an undeclared writer, it does not rule on whether `produces`
       implies a grant. Either declaration may be the wrong one and the repair
       names both.

    Mode 1 is the one that fires on the live tree. It is **not** repaired by
    widening `write_scope` from here: whether `produces` should carry an implicit
    write grant is open architecture decision A4, and `records.TaskRecord.
    effective_write_scope` computes what that grant would be without applying it.
    X-04 keeps testing the declared scope alone.
    """
    details: list[str] = []
    notices: list[str] = []
    try:
        tasks = records.load_tasks(repo)
        results = records.load_results(repo)
    except (records.RecordError, OSError) as exc:
        return _result("X-09", "Publication reachability", [str(exc)])

    producers: dict[str, list[str]] = {}
    for tid, task in sorted(tasks.items()):
        for rid in task.produces:
            producers.setdefault(str(rid), []).append(tid)

    for tid, task in sorted(tasks.items()):
        for rid, rel in zip(task.produces, task.result_paths):
            if any(scope.glob_to_regex(p).match(rel) for p in task.write_scope):
                continue
            details.append(
                f"{tid}: produces {rid} but no write_scope pattern matches {rel}, "
                f"so the task cannot lawfully publish the record it is contracted "
                f"to publish. Repair: add {rel!r} to {tid}.write_scope, or remove "
                f"{rid} from {tid}.produces - one of the two declarations is wrong"
            )

    # Mode 5, the converse of mode 1 - FIND-Q9-42. Every result the layer knows
    # about: declared by some `produces`, or present on disk. A record on disk
    # with no declared producer is already mode 2's business; it is included
    # here because an undeclared writer of an orphaned record is the same
    # hazard, not a lesser one.
    known = sorted(set(producers) | set(results))
    for tid, task in sorted(tasks.items()):
        declared = {str(r) for r in task.produces}
        for rid in known:
            if rid in declared:
                continue
            rel = f"{RESULTS_DIR}/{rid}.md"
            if not any(scope.glob_to_regex(p).match(rel) for p in task.write_scope):
                continue
            owner = ", ".join(producers.get(rid, [])) or "no task"
            details.append(
                f"{tid}: write_scope reaches {rel} but {tid} does not declare "
                f"produces: {rid} - {owner} does. A result has exactly one "
                f"producer, and a second task able to write it defeats that "
                f"invariant whether or not it declares the intent: `produced_by` "
                f"is then underivable from the records. Repair: narrow "
                f"{tid}.write_scope so it does not reach {rel}, or add {rid} to "
                f"{tid}.produces if {tid} is in fact its producer - one of the "
                f"two declarations is wrong. This reports the reach; it does not "
                f"decide A4"
            )

    for rid, owners in sorted(producers.items()):
        if len(owners) > 1:
            details.append(
                f"{rid}: declared in produces by {', '.join(owners)} - a result has "
                f"exactly one producer, and with two the `produced_by` a consumer "
                f"checks cannot be derived. Repair: keep {rid} in produces for the "
                f"one task that publishes it and remove it from the others"
            )

    for tid, task in sorted(tasks.items()):
        for rid in task.consumes:
            rid = str(rid)
            if rid in producers:
                continue
            on_disk = rid in results
            details.append(
                f"{tid}: consumes {rid} but no task declares produces: {rid}, so "
                f"nothing can publish or refresh it"
                + (
                    f" - the record exists on disk with no owning task, so it can "
                    f"go stale with no task able to repair it"
                    if on_disk
                    else ""
                )
                + f". Repair: add {rid} to the produces of the task that owns it, "
                f"or remove it from {tid}.consumes"
            )
            if not on_disk:
                details.append(
                    f"{tid}: consumes {rid}, which is neither on disk at "
                    f"{RESULTS_DIR}/{rid}.md nor produced by any task - {tid} can "
                    f"never become runnable by any sequence of dispatches. Repair: "
                    f"declare a task that produces {rid} and can write its record, "
                    f"or remove {rid} from {tid}.consumes"
                )

    # Derived, reported, not enforced - A4. The gap between what a task declares
    # it may write and what it would need in order to publish what it declares.
    for tid, task in sorted(tasks.items()):
        extra = [p for p in task.effective_write_scope if p not in task.write_scope]
        if extra:
            notices.append(
                f"{tid}: effective write scope = declared + {', '.join(extra)} "
                f"(DERIVED, NOT GRANTED - X-04 tests the declared scope only; "
                f"whether produces implies a write grant is open decision A4)"
            )
    return _result("X-09", "Publication reachability", details, notices)


ALL: tuple[Callable[[Path], dict[str, Any]], ...] = (
    x01_record_conformance,
    x02_index_bijection,
    x03_read_scope_resolves,
    x04_write_scope_containment,
    x05_graph_sound,
    x06_result_currency,
    x07_no_concurrent_write_conflict,
    x08_context_budget,
    x09_publication_reachability,
    x10_non_monotonic_measurable_bound,
)


def run_all(repo: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for fn in ALL:
        try:
            out.append(fn(repo))
        except Exception as exc:  # a check must report, never abort the campaign
            out.append(
                {
                    # `X-10` is the first two-digit check. The predecessor of
                    # this line was `.replace("X0", "X-0")`, which silently
                    # produced `X10` for it - an id no consumer would match.
                    "id": f"X-{fn.__name__.split('_')[0][1:]}",
                    "name": fn.__name__,
                    "status": "ERROR",
                    "details": [f"{type(exc).__name__}: {exc}"],
                    "notices": [],
                }
            )
    return out
