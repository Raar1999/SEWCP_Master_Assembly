"""Execution checks X-01 to X-09, on the live repository and against induced
faults.

Actor provenance: software.software-engineer - S-2026-08-09-01.

A check that has never failed has not been shown to bite. Every check below is
exercised twice: once against the live repository, where it must PASS, and once
against a minimal repository carrying the exact fault it exists to catch, where
it must FAIL.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from aief_exec import checks, graph, records

REPO = Path(__file__).resolve().parents[1]

ROSTER = """# Project Roster

| Role | Authority | Assigned identity |
|---|---|---|
| `qa-engineer` | A2 | Someone <someone@example.invalid> |
| `chief-systems-engineer` | A4 | Someone <someone@example.invalid> |
| `software.software-engineer` | A1 | Someone <someone@example.invalid> |
| `software.test-engineer` | A1 | UNASSIGNED |
"""

OPEN_ITEMS = """# Open Items

## Blocking

C-4

## Open, not blocking

OQ-14

## Closed

OQ-15
"""

TASK = """# {tid}

```yaml
task_id:    {tid}
role:       {role}
objective:  {objective}
status:     {status}
inputs:     [x]
deliverable: [y]
acceptance_criteria:
  - id: AC-1
    criterion: c
    test: t
forbidden_actions: [none]
escalation:
  - condition: c
    to: project-manager
depends_on:  {depends_on}
consumes:    {consumes}
produces:    {produces}
blocked_by:  {blocked_by}
read_scope:
  mandatory:
{mandatory}
  optional: []
  dependency: []
  forbidden: []
write_scope:
{write_scope}
qa:
  verifier_role: {verifier}
  report:        r.md
context_budget:
  tf1: {tf1}
  tf2: {tf2}
checkpoint:
  phase: p
  completed: []
  pending: []
  next_action: n
  decision: null
```
"""


def build_repo(tmp_path, tasks, index=None, results=None, extra=None):
    """A minimal repository carrying only what the checks read."""
    (tmp_path / ".ai/project/tasks").mkdir(parents=True)
    (tmp_path / ".ai/project/results").mkdir(parents=True)
    (tmp_path / ".ai/project/OPEN_ITEMS.md").write_text(OPEN_ITEMS, encoding="utf-8")
    (tmp_path / ".ai/project/ROSTER.md").write_text(ROSTER, encoding="utf-8")
    for name, body in (extra or {}).items():
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")

    rendered = {}
    for spec in tasks:
        opts = {
            "role": "software.software-engineer",
            "objective": "o",
            "status": "READY",
            "depends_on": "[]",
            "consumes": "[]",
            "produces": "[]",
            "blocked_by": "[]",
            "mandatory": "    - path: .ai/project/OPEN_ITEMS.md",
            "write_scope": "  - out/**",
            "verifier": "qa-engineer",
            "tf1": 9000,
            "tf2": 12000,
        }
        opts.update(spec)
        tid = opts["tid"]
        rendered[tid] = opts["status"]
        (tmp_path / f".ai/project/tasks/{tid}.md").write_text(
            TASK.format(**opts), encoding="utf-8"
        )

    for name, body in (results or {}).items():
        (tmp_path / f".ai/project/results/{name}.md").write_text(body, encoding="utf-8")

    if index is None:
        sections = {}
        for tid, status in rendered.items():
            heading = {
                "ACTIVE": "Active",
                "READY": "Ready",
                "BLOCKED": "Blocked",
                "AWAITING-DECISION": "Awaiting decision",
                "COMPLETE": "Complete",
            }[status]
            sections.setdefault(heading, []).append(tid)
        body = "# Execution Index\n"
        for heading in ("Active", "Ready", "Blocked", "Awaiting decision", "Complete"):
            body += f"\n## {heading}\n\n"
            body += "".join(f"{t}\n" for t in sections.get(heading, []))
        index = body
    (tmp_path / ".ai/project/EXEC.md").write_text(index, encoding="utf-8")
    return tmp_path


RESULT = """# {rid}

```yaml
result_id: {rid}
produced_by: {{task: T-001, role: software.software-engineer, session: S-2026-08-09-01}}
status: {status}
supersedes: null
inputs:
  - path: {path}
    digest: {digest}
deliverables:
  - path: {path}
    digest: {digest}
affected: []
validation: []
conclusion: |
  c
findings: []
```
"""


ENUMERATED = (
    "write_authority:\n"
    "  paths:\n"
    "    - .ai/core/MANIFEST.lock\n"
    "  id: OQ-14\n"
    "  recorded_at: .ai/project/OPEN_ITEMS.md\n"
    "  citation: Compiler Stage 6 is the emitting authority for layer L7\n"
)


@pytest.fixture(scope="module")
def rows():
    return {r["id"]: r for r in checks.run_all(REPO)}


class TestLiveRepository:
    """The checks that pass on the repository as it stands."""

    @pytest.mark.parametrize(
        "cid", ["X-01", "X-03", "X-04", "X-05", "X-07"],
    )
    def test_check_passes(self, rows, cid):
        assert rows[cid]["status"] == "PASS", rows[cid]["details"]

    def test_no_check_errors(self, rows):
        # A check must report, never abort the campaign.
        assert [r["id"] for r in rows.values() if r["status"] == "ERROR"] == []


class TestLiveRepositoryOpenFailures:
    """X-08 and X-09 fail on the live repository, and this records exactly why
    rather than asserting a state that does not hold. X-02 and X-06 were also
    open here until `R-011` closed them; the two tests that recorded them are
    retained in place, restated onto the closed state.

    Each assertion names the repair that clears it, so the test turns red when
    the repair lands and forces this file to be updated deliberately - which is
    the point. `VER-009` pass 4's judgement was that a closure asserted rather
    than demonstrated is the recurring defect of this audit; an open failure
    recorded as passing would be the same defect wearing green.

    Both remaining repairs lie outside this layer's own write scope: X-08's is
    the declared caps, a project-manager decision; X-09's is open architecture
    decision A4.
    """

    def test_x02_open_on_the_consumer_of_a_staled_result(self, rows):
        # NAME RETAINED DELIBERATELY. This node id is the one `R-010` U-3 names
        # as red, so it is kept addressable rather than renamed; what it asserts
        # has moved to the closed state and the name is now history, not a
        # description. `R-011` records the same mapping.
        #
        # WHAT CHANGED, and why. The previous form asserted X-02 FAIL on T-004
        # alone, because R-009 pinned `src/aief_exec/**` and `tests/test_exec_*.py`
        # as its deliverables, the repair pass rewrote them, and so the result
        # T-004 consumed was STALE and T-004 derived BLOCKED while the index
        # filed it READY. The named repair - supersede the staled record with a
        # sealed successor pinning the repaired layer, and re-point T-004 in the
        # same act - has now landed three times: R-010 superseded R-009, R-011
        # superseded R-010, and R-012 supersedes R-011 pinning the layer as the
        # FIND-Q9-36..42 repair pass left it. So X-02 passes.
        #
        # WHY THIS STILL BITES. It does not assert a bare PASS. The consumer
        # chain is asserted end to end: T-004 consumes exactly the CURRENT
        # record, that record is unstaled, and the derived state therefore
        # agrees with the filed one. Touch `src/aief_exec/**` or
        # `tests/test_exec_*.py` without republishing, and the current record
        # goes STALE, T-004 derives BLOCKED against a READY index entry, and
        # this test is red again - which is the regression it exists to catch.
        # It went red exactly that way during the FIND-Q9-36..42 pass, which is
        # why the record is now R-012.
        #
        # WHAT ELSE CHANGED: the record id is no longer written into the
        # assertion. It is derived - the one CURRENT result T-001 produces - so
        # the test cannot go stale on a supersession while still describing the
        # relation it is about.
        details = rows["X-02"]["details"]
        assert rows["X-02"]["status"] == "PASS", details
        assert details == [], details
        results = records.load_results(REPO)
        tasks = records.load_tasks(REPO)
        # The consumer names the current record, not a superseded ancestor.
        current = sorted(
            rid for rid in tasks["T-001"].produces
            if graph.derived_status(results, results[rid]) == "CURRENT"
        )
        assert len(current) == 1, current
        assert tasks["T-004"].consumes == current, (tasks["T-004"].consumes, current)
        # ... and that record is not stale, so nothing derives BLOCKED from it.
        curr = graph.result_currency(REPO, results[current[0]], results)
        assert curr.status == "CURRENT" and curr.usable, curr
        assert curr.drifted == [], curr.drifted
        plan = graph.build_plan(REPO)
        assert plan.states["T-004"] == tasks["T-004"].status == "READY"
        assert plan.blocked["T-004"] == [], plan.blocked["T-004"]

    def test_x06_open_on_the_result_that_pins_the_layer_it_describes(self, rows):
        # NAME RETAINED DELIBERATELY, as above: this is the node id `R-010` U-3
        # names as red.
        #
        # WHAT CHANGED, and why. The previous form asserted X-06 FAIL because
        # R-009 declared CURRENT while pinning DC-1 digests of `src/aief_exec/**`
        # and `tests/test_exec_*.py` that the repair pass had moved. R-010
        # superseded R-009 with recomputed digests; restating this very file then
        # staled R-010 in turn, and R-011 superseded R-010 with the digests taken
        # after that restatement. The two acts landed together, which is the only
        # ordering that terminates: the tests are the last thing to change, so the
        # successor record stays current. The FIND-Q9-36..42 pass moved the layer
        # again and R-012 supersedes R-011 under the same ordering.
        #
        # WHY THIS STILL BITES. A bare PASS would be worth nothing here - X-06's
        # whole job is to notice drift. What is asserted is that the record which
        # pins the layer still matches the layer, and that **every** superseded
        # ancestor still matches the digest its successor sealed - the chain is
        # walked, not a fixed list of ids, so a new supersession is covered the
        # day it lands rather than the day someone remembers to add it:
        #
        #   * move any file under `src/aief_exec/` or `tests/test_exec_*.py`
        #     without republishing -> the current record STALE -> X-06 FAIL;
        #   * edit any superseded ancestor -> REWRITTEN AFTER SUPERSESSION ->
        #     X-06 FAIL -> red here.
        details = rows["X-06"]["details"]
        assert rows["X-06"]["status"] == "PASS", details
        assert details == [], details
        results = records.load_results(REPO)
        current = [
            rid for rid in sorted(results)
            if graph.derived_status(results, results[rid]) == "CURRENT"
        ]
        assert len(current) == 1, current
        # The current record still pins the layer it describes - the property
        # that made the old failure possible is not what was removed.
        pinned = {e["path"] for e in results[current[0]].deliverables}
        assert any(p.startswith("src/aief_exec/") for p in pinned), pinned
        assert any(p.startswith("tests/test_exec_") for p in pinned), pinned
        curr = graph.result_currency(REPO, results[current[0]], results)
        assert curr.status == "CURRENT" and curr.drifted == [], curr
        # Every supersession from the seal epoch onward is sealed, and each seal
        # matches the predecessor's bytes as they stand. Derived from the chain.
        sealed_links = [
            rid for rid in sorted(results)
            if graph.successor_of(results, rid)
            and str(results[graph.successor_of(results, rid)]
                    .produced_by.get("session") or "") >= graph.SEAL_EPOCH
        ]
        assert len(sealed_links) >= 3, sealed_links
        for rid in sealed_links:
            successor, sealed = graph.supersession_seal(results, rid)
            assert len(sealed) == 64, (rid, successor, sealed)
            assert sealed == records.file_dc1(REPO, results[rid].path), rid
            assert graph.result_currency(REPO, results[rid], results).drifted == []
        # No record is accused of being rewritten after supersession, and the
        # two historical unsealed supersessions are reported, never failed.
        assert not any("REWRITTEN" in d for d in details)
        assert not any("pins no supersedes_seal" in d for d in details), details
        assert any("pins no supersedes_seal" in n for n in rows["X-06"]["notices"])

    def test_x08_open_because_the_measurement_is_now_honest(self, rows):
        # FIND-Q9-35 and its own correction. Repair: the declared caps, which
        # live in task records and are a project-manager decision.
        #
        # WHAT CHANGED: the gated quantity is `acquisition`, not the summed
        # charge, so every gate failure says `acquisition` and its breakdown
        # carries only the four pre-dispatch components.
        #
        # WHAT CHANGED AGAIN - FIND-Q9-37. The previous form asserted that
        # *every* X-08 detail is an acquisition breach. That became false when
        # the excluded `revision` was given a verdict, because excluding it
        # excluded 53% of T-004's measurable input, 85% of T-001's and 80% of
        # T-005's, and an excluded cost reported only as a footnote is an
        # invisible cost.
        #
        # WHAT CHANGED A THIRD TIME - FIND-Q9-45, and it restores the original
        # assertion with a reason rather than by accident. Two verdicts against
        # the same cap in one `details` list made X-08 fail *iff* some
        # `total_measurable` breached, so the gate contributed nothing to the
        # boolean and the only discriminator between the two kinds of row was
        # the English substring `NON-MONOTONIC BOUND`. The bound is now X-10.
        # So: every X-08 detail is an acquisition breach again - because the
        # bound is somewhere else, not because it is invisible - and this test
        # asserts the partition across the two checks rather than inside one.
        details = rows["X-08"]["details"]
        assert rows["X-08"]["status"] == "FAIL"
        assert details and all("exceeds declared cap" in d for d in details)
        gate = [d for d in details if ": acquisition " in d]
        assert gate and len(gate) == len(details), details
        # Nothing that belongs to the bound is left in the gate's list.
        assert not any(": total_measurable " in d for d in details), details
        assert not any("NON-MONOTONIC BOUND" in d for d in details), details
        # The gate rows: breakdown printed, so no cap is disputed blind ...
        assert all("record " in d for d in gate), gate
        # ... and no gated figure includes a deliverable.
        assert not any("deliverable" in d for d in gate), gate

    def test_x10_open_on_the_cost_the_gate_excludes(self, rows):
        # FIND-Q9-37, now carried by its own check - FIND-Q9-45. The bound rows
        # moved out of X-08 verbatim; every assertion the old test made about
        # them is made here, against `rows["X-10"]`, plus the two the split
        # makes possible: the check has its own boolean, and its own id.
        bound = rows["X-10"]["details"]
        assert rows["X-10"]["status"] == "FAIL"
        assert bound and all("exceeds declared cap" in d for d in bound)
        assert all(": total_measurable " in d for d in bound), bound
        # Labelled as the non-monotonic quantity, said in words a reader cannot
        # mistake for the gate, and each names its own revision.
        assert all("NON-MONOTONIC BOUND" in d for d in bound), bound
        assert all("not the acquisition gate" in d for d in bound), bound
        assert all("revision" in d for d in bound), bound
        # It is a failure, not a notice. That is the whole of FIND-Q9-37 - with
        # the one exception the gate already makes for the same reason: a
        # COMPLETE task has no dispatch to refuse, so its breach is demoted, and
        # every demoted row says so in the same words the gate uses.
        demoted = [n for n in rows["X-10"]["notices"] if "NON-MONOTONIC BOUND" in n]
        assert demoted, rows["X-10"]["notices"]
        assert all("not gated" in n and "COMPLETE" in n for n in demoted), demoted

    def test_the_gate_and_the_bound_decide_their_own_booleans(self, rows):
        # FIND-Q9-45, stated as the property rather than as a case. The two
        # checks must be separable by a machine, not only by a reader: X-08's
        # status is a function of acquisition breaches alone and X-10's of
        # total_measurable breaches alone, and each row is reachable by id.
        #
        # The live tree proves they are not the same boolean by proving they are
        # not over the same task set: T-005 breaches the bound and not the gate,
        # so it appears in X-10's details and nowhere in X-08's.
        gate_tasks = {d.split(":")[0] for d in rows["X-08"]["details"]}
        bound_tasks = {d.split(":")[0] for d in rows["X-10"]["details"]}
        assert "T-005" in bound_tasks, rows["X-10"]["details"]
        assert "T-005" not in gate_tasks, rows["X-08"]["details"]
        assert gate_tasks < bound_tasks, (gate_tasks, bound_tasks)
        # And no row of either check can be mistaken for a row of the other.
        assert all(": acquisition " in d for d in rows["X-08"]["details"])
        assert all(": total_measurable " in d for d in rows["X-10"]["details"])

    def test_x08_no_longer_gates_a_complete_task(self, rows):
        # T-001 is COMPLETE and charges TF-1 ~35,000 against a cap of 6,000,
        # almost all of it its own finished deliverables. It will not be
        # dispatched again, so there is no dispatch to refuse: reported, not
        # gated. Under the summed form this was one of the failures.
        assert not any(d.startswith("T-001:") for d in rows["X-08"]["details"])
        assert any(
            d.startswith("T-001:") and "not gated" in d and "COMPLETE" in d
            for d in rows["X-08"]["notices"]
        ), [n for n in rows["X-08"]["notices"] if n.startswith("T-001")]

    def test_x08_still_reports_the_deliverable_that_dominates_a_qa_task(self, rows):
        # The specific number the finding turned on: X-08 certified T-004 at
        # TF-1 2,519 against a cap of 8,000 while omitting VER-009, which T-004's
        # own AC-4 makes mandatory.
        #
        # WHAT CHANGED: the deliverable is `revision` now, so it no longer moves
        # the gate. It must still be *visible* - an invisible component was the
        # whole of FIND-Q9-35 - so it is asserted in the notices instead, beside
        # the gated figure, and the gated figure must itself still exceed the cap
        # on the strength of the read scope alone.
        gated = [d for d in rows["X-08"]["details"] if d.startswith("T-004: acquisition")]
        assert gated, rows["X-08"]["details"]
        assert "deliverable" not in gated[0]
        charged = int(gated[0].split("TF1 ")[1].split(" ")[0])
        assert charged > 3 * 2519, gated[0]
        split = [n for n in rows["X-08"]["notices"] if n.startswith("T-004 [")]
        assert split, rows["X-08"]["notices"]
        assert "revision" in split[0] and "deliverable" in split[0]
        assert "UNMEASURABLE" in split[0]

    def test_x09_open_on_five_tasks_that_cannot_publish_what_they_produce(self, rows):
        # The reproduced defect. Repair: either add the result path to each
        # task's write_scope, or settle open decision A4 so that `produces`
        # carries the grant. Both are outside this layer - one is a task-record
        # write, the other an architecture decision.
        #
        # WHAT CHANGED - FIND-Q9-42. The previous form asserted that T-001
        # appears in no X-09 detail, on the reasoning that "T-001 declares four
        # produces and a write scope that covers all of them". That is true of
        # the direction mode 1 tests and it was the wrong test to conclude
        # silence from: T-001's write scope also reaches five result records it
        # does **not** produce, and nothing looked. The mode 1 offender set is
        # unchanged and still asserted here; T-001's absence from it is now
        # asserted against mode 1 specifically rather than against the whole
        # check, and the converse mode has its own test below.
        details = rows["X-09"]["details"]
        assert rows["X-09"]["status"] == "FAIL"
        mode1 = [d for d in details if "no write_scope pattern matches" in d]
        offenders = sorted({d.split(":")[0] for d in mode1})
        assert offenders == ["T-002", "T-003", "T-004", "T-005", "T-006"], offenders
        # T-001 declares its produces and a write scope that covers all of them,
        # so it cannot fail the direction mode 1 tests.
        assert not any(d.startswith("T-001") for d in mode1)
        # Every failure, in every mode, states its repair.
        assert all("Repair:" in d for d in details), details

    def test_x09_guards_the_publication_channel_in_both_directions(self, rows):
        # FIND-Q9-42, live. X-09 verified that a declared producer *can* write
        # its record and never that a non-producer *cannot*. T-001 holds
        # `.ai/project/results/**`, which reaches R-002..R-006 - five records
        # declared by five other tasks - and the check said nothing. Combined
        # with FIND-Q9-38 H1 that was concrete rather than theoretical:
        # `T-001 x T-002` classified PARALLEL, so T-001 could publish R-002
        # beside its declared producer with all nine checks clean.
        details = rows["X-09"]["details"]
        converse = [d for d in details if "does not declare produces" in d]
        assert converse, details
        assert all(d.startswith("T-001:") for d in converse), converse
        reached = sorted(d.split("results/")[1].split(".md")[0] for d in converse)
        assert reached == ["R-002", "R-003", "R-004", "R-005", "R-006"], reached
        # Each row names the task that does declare it, so the reader is not
        # left to look the owner up.
        tasks = records.load_tasks(REPO)
        for rid, owner in zip(reached, ["T-002", "T-003", "T-004", "T-005", "T-006"]):
            row = [d for d in converse if f"{rid}.md" in d][0]
            assert f"- {owner} does" in row, row
            assert rid in tasks[owner].produces
        # A4 is reported, never decided: the repair names both declarations.
        assert all("does not decide A4" in d for d in converse), converse
        assert all("narrow" in d and "or add" in d for d in converse), converse
        # And the guard does not fire on what T-001 does produce.
        for rid in tasks["T-001"].produces:
            assert not any(f"{rid}.md but T-001" in d for d in converse), rid

    def test_x09_names_the_structural_deadlock_reachable_from_it(self, rows):
        # T-006 consumes R-002 and R-003. Both have declared producers, so no
        # `consumes` limb fires - but neither producer can write the record it
        # produces, so no lawful dispatch sequence makes T-006 runnable. The two
        # facts are reported separately and both are present.
        details = rows["X-09"]["details"]
        assert any("T-002: produces R-002" in d for d in details), details
        assert any("T-003: produces R-003" in d for d in details), details
        tasks = records.load_tasks(REPO)
        assert sorted(tasks["T-006"].consumes) == ["R-002", "R-003"]

    def test_x09_reports_the_derived_grant_without_applying_it(self, rows):
        # A4. The effective write scope is displayed and never enforced: X-04,
        # which tests the declared scope, still passes.
        notices = rows["X-09"]["notices"]
        assert any("DERIVED, NOT GRANTED" in n for n in notices), notices
        assert any("A4" in n for n in notices)
        assert rows["X-04"]["status"] == "PASS"


class TestInducedFaults:
    """Each check fails on the exact fault it exists to catch."""

    def test_x01_catches_a_missing_required_field(self, tmp_path):
        repo = build_repo(tmp_path, [{"tid": "T-001"}])
        body = (repo / ".ai/project/tasks/T-001.md").read_text(encoding="utf-8")
        body = body.replace("objective:  o\n", "")
        (repo / ".ai/project/tasks/T-001.md").write_text(body, encoding="utf-8")
        assert checks.x01_record_conformance(repo)["status"] == "FAIL"

    def test_x01_catches_self_verification(self, tmp_path):
        # LAW-05: no agent may verify an artifact it produced.
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001", "verifier": "software.software-engineer"}],
        )
        row = checks.x01_record_conformance(repo)
        assert row["status"] == "FAIL"
        assert any("LAW-05" in d for d in row["details"])

    def test_x02_catches_a_record_missing_from_the_index(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001"}, {"tid": "T-002"}],
            index="# Execution Index\n\n## Ready\n\nT-001\n",
        )
        row = checks.x02_index_bijection(repo)
        assert row["status"] == "FAIL"
        assert any("T-002" in d for d in row["details"])

    def test_x02_catches_a_status_mismatch(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001", "status": "READY"}],
            index="# Execution Index\n\n## Blocked\n\nT-001\n",
        )
        assert checks.x02_index_bijection(repo)["status"] == "FAIL"

    def test_x03_catches_an_unresolvable_anchor(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [
                {
                    "tid": "T-001",
                    "mandatory": (
                        "    - path: .ai/project/OPEN_ITEMS.md\n"
                        "      anchor: NO-SUCH-ANCHOR"
                    ),
                }
            ],
        )
        row = checks.x03_read_scope_resolves(repo)
        assert row["status"] == "FAIL"
        assert any("NO-SUCH-ANCHOR" in d for d in row["details"])

    def test_x03_catches_a_read_scope_path_that_does_not_exist(self, tmp_path):
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "mandatory": "    - path: gone/missing.md"}]
        )
        assert checks.x03_read_scope_resolves(repo)["status"] == "FAIL"

    def test_x04_catches_an_undeclared_write_into_core(self, tmp_path):
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "write_scope": "  - .ai/core/laws/**"}]
        )
        row = checks.x04_write_scope_containment(repo)
        assert row["status"] == "FAIL"
        assert any("protected set" in d for d in row["details"])

    def test_x04_catches_a_write_into_the_frozen_specification(self, tmp_path):
        repo = build_repo(tmp_path, [{"tid": "T-001", "write_scope": "  - spec/**"}])
        assert checks.x04_write_scope_containment(repo)["status"] == "FAIL"

    def _with_authority(self, repo, block):
        p = repo / ".ai/project/tasks/T-001.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace("qa:\n", block + "qa:\n"),
            encoding="utf-8",
        )
        return checks.x04_write_scope_containment(repo)

    def test_x04_allows_an_enumerated_grant(self, tmp_path):
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "write_scope": "  - .ai/core/MANIFEST.lock"}]
        )
        row = self._with_authority(repo, ENUMERATED)
        assert row["status"] == "PASS"

    def test_x04_grant_is_never_silent(self, tmp_path):
        # VER-009 FIND-Q9-1: an exemption that produces no output is a silent
        # exemption.
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "write_scope": "  - .ai/core/MANIFEST.lock"}]
        )
        row = self._with_authority(repo, ENUMERATED)
        assert any("declared grant" in n for n in row["notices"])

    def test_x04_rejects_free_text_authority(self, tmp_path):
        # The original form: any non-empty string disabled the check wholesale.
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "write_scope": "  - .ai/core/MANIFEST.lock"}]
        )
        row = self._with_authority(repo, "write_authority: x\n")
        assert row["status"] == "FAIL"
        assert any("must enumerate" in d for d in row["details"])

    def test_x04_grant_does_not_cover_a_different_path(self, tmp_path):
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "write_scope": "  - .ai/core/laws/**"}]
        )
        row = self._with_authority(repo, ENUMERATED)
        assert row["status"] == "FAIL"

    def test_x04_rejects_a_grant_without_a_citation(self, tmp_path):
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "write_scope": "  - .ai/core/MANIFEST.lock"}]
        )
        row = self._with_authority(
            repo,
            "write_authority:\n  paths:\n    - .ai/core/MANIFEST.lock\n"
            "  citation: ok\n",
        )
        assert row["status"] == "FAIL"

    def test_x04_rejects_a_grant_naming_no_recorded_authority(self, tmp_path):
        # VER-009 second pass, FIND-Q9-1 residual: a citation validated only for
        # length let `aaaaaaaaaaaa` grant .ai/core/**.
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "write_scope": "  - .ai/core/MANIFEST.lock"}]
        )
        row = self._with_authority(
            repo,
            "write_authority:\n  paths:\n    - .ai/core/MANIFEST.lock\n"
            "  citation: aaaaaaaaaaaaaaaaaaaa\n",
        )
        assert row["status"] == "FAIL"
        assert any("recorded authority" in d for d in row["details"])

    def test_x04_rejects_a_grant_whose_record_does_not_exist(self, tmp_path):
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "write_scope": "  - .ai/core/MANIFEST.lock"}]
        )
        row = self._with_authority(
            repo,
            "write_authority:\n  paths:\n    - .ai/core/MANIFEST.lock\n"
            "  id: OQ-14\n  recorded_at: nowhere/absent.md\n  citation: x y z\n",
        )
        assert row["status"] == "FAIL"
        assert any("does not exist" in d for d in row["details"])

    def test_x04_rejects_a_grant_whose_id_is_not_in_the_record(self, tmp_path):
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "write_scope": "  - .ai/core/MANIFEST.lock"}]
        )
        row = self._with_authority(
            repo,
            "write_authority:\n  paths:\n    - .ai/core/MANIFEST.lock\n"
            "  id: NOT-RECORDED-ANYWHERE\n"
            "  recorded_at: .ai/project/OPEN_ITEMS.md\n  citation: x y z\n",
        )
        assert row["status"] == "FAIL"
        assert any("not recorded there" in d for d in row["details"])

    def test_x04_covers_the_framework_partition(self, tmp_path):
        # VER-009 FIND-Q9-2: framework/** was absent from PROTECTED_WRITE.
        for pattern in ("framework/**", "framework/framework.manifest.json"):
            repo = build_repo(
                tmp_path / pattern.replace("/", "_").replace("*", "x"),
                [{"tid": "T-001", "write_scope": f"  - {pattern}"}],
            )
            assert checks.x04_write_scope_containment(repo)["status"] == "FAIL", pattern

    def test_x04_covers_the_ledger(self, tmp_path):
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "write_scope": "  - .ai/project/ledger/**"}]
        )
        assert checks.x04_write_scope_containment(repo)["status"] == "FAIL"

    def test_x05_catches_a_dependency_cycle(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "depends_on": "[T-002]"},
                {"tid": "T-002", "depends_on": "[T-001]"},
            ],
        )
        row = checks.x05_graph_sound(repo)
        assert row["status"] == "FAIL"
        assert any("cycle" in d for d in row["details"])

    def test_x05_catches_a_dangling_dependency(self, tmp_path):
        repo = build_repo(tmp_path, [{"tid": "T-001", "depends_on": "[T-099]"}])
        assert checks.x05_graph_sound(repo)["status"] == "FAIL"

    def test_x06_catches_a_result_whose_input_drifted(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001"}],
            results={
                "R-001": RESULT.format(
                    rid="R-001",
                    status="CURRENT",
                    path=".ai/project/OPEN_ITEMS.md",
                    digest="0" * 64,
                )
            },
        )
        row = checks.x06_result_currency(repo)
        assert row["status"] == "FAIL"
        assert any("STALE" in d for d in row["details"])

    def test_x06_catches_a_truncated_digest(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001"}],
            results={
                "R-001": RESULT.format(
                    rid="R-001",
                    status="CURRENT",
                    path=".ai/project/OPEN_ITEMS.md",
                    digest="abc123",
                )
            },
        )
        assert checks.x06_result_currency(repo)["status"] == "FAIL"

    def test_x06_passes_when_the_pinned_digest_matches(self, tmp_path):
        repo = build_repo(tmp_path, [{"tid": "T-001"}])
        digest = records.file_dc1(repo, ".ai/project/OPEN_ITEMS.md")
        (repo / ".ai/project/results/R-001.md").write_text(
            RESULT.format(
                rid="R-001",
                status="CURRENT",
                path=".ai/project/OPEN_ITEMS.md",
                digest=digest,
            ),
            encoding="utf-8",
        )
        assert checks.x06_result_currency(repo)["status"] == "PASS"

    def test_x07_never_groups_conflicting_tasks(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "write_scope": "  - out/shared/**"},
                {"tid": "T-002", "write_scope": "  - out/shared/**"},
            ],
        )
        # The grouping refuses to co-schedule them, so X-07 stays PASS and the
        # plan shows two groups rather than one.
        from aief_exec import graph
        plan = graph.build_plan(repo)
        assert plan.pairs[("T-001", "T-002")][0] == graph.CONFLICT
        assert len(plan.parallel_sets()) == 2
        assert checks.x07_no_concurrent_write_conflict(repo)["status"] == "PASS"

    def test_x08_catches_a_budget_breach(self, tmp_path):
        repo = build_repo(tmp_path, [{"tid": "T-001", "tf1": 1, "tf2": 1}])
        row = checks.x08_context_budget(repo)
        assert row["status"] == "FAIL"
        assert any("exceeds declared cap" in d for d in row["details"])

    def test_x08_catches_an_undeclared_budget(self, tmp_path):
        repo = build_repo(tmp_path, [{"tid": "T-001"}])
        p = repo / ".ai/project/tasks/T-001.md"
        body = p.read_text(encoding="utf-8").replace("  tf1: 9000\n", "")
        p.write_text(body, encoding="utf-8")
        row = checks.x08_context_budget(repo)
        assert row["status"] == "FAIL"
        assert any("not declared" in d for d in row["details"])


class TestVer009Regressions:
    """Each finding VER-009 raised, pinned so it cannot return."""

    def test_x01_law05_survives_a_case_change(self, tmp_path):
        # FIND-Q9-6: raw string equality let `QA-Engineer` verify `qa-engineer`.
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001", "role": "qa-engineer", "verifier": "QA-Engineer"}],
        )
        row = checks.x01_record_conformance(repo)
        assert row["status"] == "FAIL"
        assert any("LAW-05" in d for d in row["details"])

    def test_x01_rejects_an_unregistered_verifier(self, tmp_path):
        # FIND-Q9-6: `not-a-real-role-at-all` passed.
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "verifier": "not-a-real-role-at-all"}]
        )
        row = checks.x01_record_conformance(repo)
        assert row["status"] == "FAIL"
        assert any("ROSTER" in d for d in row["details"])

    def test_unassigned_role_blocks_dispatch(self, tmp_path):
        # TPL-task-package acceptance condition 1. software.test-engineer is
        # UNASSIGNED in the fixture roster.
        from aief_exec import graph
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "role": "software.test-engineer"}]
        )
        plan = graph.build_plan(repo)
        assert plan.states["T-001"] == graph.BLOCKED
        assert any("UNASSIGNED" in r for r in plan.blocked["T-001"])

    def _role_grant(self, tmp_path, block):
        from aief_exec import graph
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "role": "software.test-engineer"}]
        )
        p = repo / ".ai/project/tasks/T-001.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace("qa:\n", block + "qa:\n"),
            encoding="utf-8",
        )
        return repo, graph.build_plan(repo)

    def test_role_authority_grant_releases_an_unassigned_role(self, tmp_path):
        from aief_exec import graph
        _, plan = self._role_grant(
            tmp_path,
            "role_authority:\n  roles:\n    - software.test-engineer\n"
            "  id: OQ-14\n  recorded_at: .ai/project/OPEN_ITEMS.md\n"
            "  citation: rank-1 live human instruction\n",
        )
        assert plan.states["T-001"] != graph.BLOCKED

    def test_role_authority_junk_citation_does_not_release(self, tmp_path):
        # VER-009 second pass, FIND-Q9-17: a 12-character junk citation moved a
        # task from BLOCKED to READY. role_authority is validated exactly as
        # write_authority is.
        from aief_exec import graph
        repo, plan = self._role_grant(
            tmp_path,
            "role_authority:\n  roles:\n    - software.test-engineer\n"
            "  citation: aaaaaaaaaaaaaaaa\n",
        )
        assert plan.states["T-001"] == graph.BLOCKED
        assert checks.x01_record_conformance(repo)["status"] == "FAIL"

    def test_role_authority_unrecorded_id_does_not_release(self, tmp_path):
        from aief_exec import graph
        _, plan = self._role_grant(
            tmp_path,
            "role_authority:\n  roles:\n    - software.test-engineer\n"
            "  id: NEVER-RECORDED\n  recorded_at: .ai/project/OPEN_ITEMS.md\n"
            "  citation: rank-1 live human instruction\n",
        )
        assert plan.states["T-001"] == graph.BLOCKED

    def test_over_declared_block_is_caught(self, tmp_path):
        # VER-009 second pass, FIND-Q9-18: build_plan defaulted the derived state
        # to the declared one, so this branch of X-02 was dead code.
        repo = build_repo(tmp_path, [{"tid": "T-001", "status": "BLOCKED"}])
        row = checks.x02_index_bijection(repo)
        assert row["status"] == "FAIL"
        assert any("no blocker" in d for d in row["details"])

    def test_notices_reach_the_operator(self, tmp_path):
        # VER-009 second pass, FIND-Q9-16: notices were computed and discarded.
        import io
        import contextlib
        from aief_exec import __main__ as cli
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "write_scope": "  - .ai/core/MANIFEST.lock"}]
        )
        p = repo / ".ai/project/tasks/T-001.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace("qa:\n", ENUMERATED + "qa:\n"),
            encoding="utf-8",
        )
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cli.cmd_check(repo, [])
        assert "note" in buf.getvalue()
        assert ".ai/core/MANIFEST.lock" in buf.getvalue()

    def test_x08_charges_optional_scope(self, tmp_path):
        # FIND-Q9-5: a task could declare four times its cap as optional.
        repo = build_repo(tmp_path, [{"tid": "T-001", "tf1": 400, "tf2": 500}])
        p = repo / ".ai/project/tasks/T-001.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace(
                "  optional: []",
                "  optional:\n    - path: .ai/project/OPEN_ITEMS_REGISTER.md",
            ),
            encoding="utf-8",
        )
        (repo / ".ai/project/OPEN_ITEMS_REGISTER.md").write_text(
            "# Register\n\n" + ("filler text for the budget. " * 400) + "\n",
            encoding="utf-8",
        )
        row = checks.x08_context_budget(repo)
        assert row["status"] == "FAIL"
        assert any("exceeds declared cap" in d for d in row["details"])

    def test_x08_measures_an_existing_deliverable_without_gating_on_it(self, tmp_path):
        # FIND-Q9-35: the measurement modelled a task as what it reads to start,
        # so a task that must rewrite a large existing artifact passed on a
        # figure that omitted it entirely.
        #
        # WHAT CHANGED: the omitted component must be *visible*, which was the
        # finding; it must not be *gated*, which was the defect the fix for the
        # finding introduced. `out/big.md` is inside T-001's write scope, so
        # charging it would make the verdict depend on whether the task had
        # already written it. The check now reports it as `revision` and gates
        # `acquisition`, which does not move.
        repo = build_repo(tmp_path, [{"tid": "T-001", "tf1": 800, "tf2": 1000}])
        p = repo / ".ai/project/tasks/T-001.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace(
                "deliverable: [y]", "deliverable: [out/big.md]"
            ),
            encoding="utf-8",
        )
        # WHAT CHANGED AGAIN - FIND-Q9-37. This asserted `after["status"] ==
        # "PASS"`, i.e. that the *whole check row* is unmoved by the task's own
        # output. That can only stay true while the excluded cost is invisible,
        # which is the finding. `total_measurable` was given its own verdict, so
        # the row moved - deliberately.
        #
        # WHAT CHANGED A THIRD TIME - FIND-Q9-45, and this test was named in the
        # finding as one of the two that locked the defect in as intended. What
        # it asserted was that X-08's *status* flips from PASS to FAIL when the
        # task writes its own deliverable, with the gate under cap both times.
        # That is a check verdict a task moves by doing its own work - the
        # FIND-Q9-35 defect at the boolean instead of at the number - and
        # asserting it made the suite the reason it survived.
        #
        # Restated onto the split. The flip is real and belongs to X-10, whose
        # name says it is non-monotonic; X-08's status is now asserted to be
        # **identical before and after**, which is the property a dispatch gate
        # has to have and which no prior form of this test ever checked.
        before8 = checks.x08_context_budget(repo)
        before10 = checks.x10_non_monotonic_measurable_bound(repo)
        (repo / "out").mkdir(parents=True, exist_ok=True)
        (repo / "out/big.md").write_text(
            "# Report\n\n" + ("prose that must be read to be rewritten. " * 400),
            encoding="utf-8",
        )
        after8 = checks.x08_context_budget(repo)
        after10 = checks.x10_non_monotonic_measurable_bound(repo)

        # THE GATE does not move - neither its details nor, now, its verdict.
        assert not any(": acquisition " in d for d in before8["details"]), before8
        assert not any(": acquisition " in d for d in after8["details"]), after8
        assert before8["status"] == "PASS", before8["details"]
        assert after8["status"] == "PASS", after8["details"]
        assert before8["details"] == after8["details"] == []
        # THE BOUND does: the deliverable is 3,000-odd TF-1 against a cap of 800,
        # and that is a failure of X-10, in X-10's own boolean.
        assert before10["status"] == "PASS", before10["details"]
        assert after10["status"] == "FAIL", after10["details"]
        assert all(": total_measurable " in d for d in after10["details"]), after10
        assert all("NON-MONOTONIC BOUND" in d for d in after10["details"]), after10
        # The cost is measured, not merely alleged, and it is in the split too.
        assert not any("revision TF-1 0" in n for n in after8["notices"])
        split = [n for n in after8["notices"] if n.startswith("T-001 [")]
        assert split and "deliverable" in split[0], after8["notices"]
        assert "non-monotonic" in split[0], split[0]
        # and the gated figure is identical either way round.
        def gated(row):
            return [n for n in row["notices"] if n.startswith("T-001 [")][0].split(
                "GATED"
            )[0]
        assert gated(before8) == gated(after8)

    def test_x08_does_not_charge_a_deliverable_that_does_not_exist(self, tmp_path):
        repo = build_repo(tmp_path, [{"tid": "T-001", "tf1": 800, "tf2": 1000}])
        p = repo / ".ai/project/tasks/T-001.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace(
                "deliverable: [y]", "deliverable: [out/not-written-yet.md]"
            ),
            encoding="utf-8",
        )
        row = checks.x08_context_budget(repo)
        assert row["status"] == "PASS", row["details"]
        assert any("charged nothing" in n for n in row["notices"])

    def test_x10_fails_on_the_cost_the_gate_excludes(self, tmp_path):
        # FIND-Q9-37. `revision` is real, mandatory, pre-dispatch cost - the
        # class's own docstring concedes it - and the gate excludes it: 19,049
        # TF-1 for T-004, 53% of its measurable total, and the excluded item is
        # the very report its AC-4 makes mandatory reading. A cap bounding 47% of
        # an agent's required input with nothing bounding the rest is not a
        # budget, and a notice is not a bound.
        #
        # This test fails against a check that reports the exclusion as a notice
        # and passes against one that fails on it. The gate must stay separate:
        # folding `revision` into `acquisition` would clear the total_measurable
        # row and reintroduce FIND-Q9-35's non-monotonic gate, so the test
        # asserts the absence of an acquisition breach as well as the presence
        # of the bound breach.
        #
        # WHAT CHANGED - FIND-Q9-45. Named in the finding as the second of the
        # two tests that locked the conflation in. It asserted the bound row and
        # the absence of an acquisition row **in one check's details list**,
        # which is exactly the arrangement that let one boolean carry two
        # quantities: it passed just as happily when X-08's FAIL was caused
        # entirely by the non-monotonic bound. Restated onto the split, with the
        # separation asserted structurally instead of by substring - the bound
        # is X-10's whole details list, and X-08 PASSes at the same instant.
        # Every original assertion survives; `row` is simply two rows now.
        repo = build_repo(tmp_path, [{"tid": "T-001", "tf1": 900, "tf2": 1200}])
        p = repo / ".ai/project/tasks/T-001.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace(
                "deliverable: [y]", "deliverable: [out/prior.md]"
            ),
            encoding="utf-8",
        )
        (repo / "out").mkdir(parents=True, exist_ok=True)
        (repo / "out/prior.md").write_text(
            "# Prior\n\n" + ("an artifact that must be read to be rewritten. " * 500),
            encoding="utf-8",
        )
        row = checks.x10_non_monotonic_measurable_bound(repo)
        assert row["status"] == "FAIL", row["notices"]
        # It is a DETAIL, not a notice. That is the requirement.
        bound = [d for d in row["details"] if ": total_measurable " in d]
        assert bound, row["details"]
        assert not any("total_measurable" in n and "exceeds" in n
                       for n in row["notices"]), row["notices"]
        # Labelled so a reader can tell it from the gate, and told which
        # quantity is the non-monotonic one.
        assert all("NON-MONOTONIC BOUND, not the acquisition gate" in d
                   for d in bound), bound
        assert all("revision" in d for d in bound), bound
        # The gate itself is untouched: the read scope is inside the cap, so no
        # acquisition row appears, `revision` has not been folded in, and the
        # gate's own boolean says so rather than being outvoted by the bound.
        gate = checks.x08_context_budget(repo)
        assert not any(": acquisition " in d for d in gate["details"]), gate["details"]
        assert gate["status"] == "PASS", gate["details"]

    def test_the_gate_verdict_does_not_move_when_the_task_writes_its_own_work(
        self, tmp_path
    ):
        # FIND-Q9-45, as the property rather than as a symptom. This is the
        # regression test for the finding: it fails against a check that carries
        # the `total_measurable` bound in the same boolean as the gate.
        #
        # The live incident, reproduced: T-005's gate was under cap both before
        # and after it wrote `tests/test_stage6_crash_trials.py`, and X-08 went
        # from zero rows to two FAILs anyway, because the bound shared its
        # verdict. A dispatch gate whose answer changes when the task does its
        # own work is not a gate, and the check id is what a machine reads.
        repo = build_repo(tmp_path, [{"tid": "T-001", "tf1": 800, "tf2": 1000}])
        p = repo / ".ai/project/tasks/T-001.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace(
                "deliverable: [y]", "deliverable: [out/written-by-this-task.md]"
            ),
            encoding="utf-8",
        )
        before = checks.x08_context_budget(repo)
        (repo / "out").mkdir(parents=True, exist_ok=True)
        (repo / "out/written-by-this-task.md").write_text(
            "# Output\n\n" + ("the deliverable this task was dispatched to write. "
                              * 400),
            encoding="utf-8",
        )
        after = checks.x08_context_budget(repo)

        # The gate's whole verdict is unmoved - status, details and the gated
        # figure - by the task doing exactly what it was dispatched to do.
        assert before["status"] == after["status"] == "PASS", (before, after)
        assert before["details"] == after["details"], (before, after)
        # The cost is not hidden to achieve that. It moved; it is X-10's, and
        # X-10 says so in its own boolean.
        assert checks.x10_non_monotonic_measurable_bound(repo)["status"] == "FAIL"
        # And the movement is visible in X-08's own reporting, as a measurement.
        split = [n for n in after["notices"] if n.startswith("T-001 [")][0]
        assert "revision" in split and "deliverable" in split, split

    def test_the_split_notice_asserts_no_verdict_it_did_not_emit(self, tmp_path):
        # FIND-Q9-46, the regression test. The notice used to append
        # "total_measurable {...} BOUNDED by the same cap and failed separately"
        # to every task in every state, unconditionally - no test on a breach,
        # none on the suppression that then existed. It was live-false for
        # T-002, T-003 and T-006, which breached and for which no separate
        # failure was emitted, and false again for any task under cap, for which
        # there was nothing to fail. A control that misreports is worse than no
        # control.
        #
        # This test fails against any notice that claims a failure: the task
        # here breaches nothing, so no verdict of any kind exists to report.
        repo = build_repo(tmp_path, [{"tid": "T-001", "tf1": 90000, "tf2": 90000}])
        gate = checks.x08_context_budget(repo)
        bound = checks.x10_non_monotonic_measurable_bound(repo)
        assert gate["status"] == "PASS" and bound["status"] == "PASS"
        split = [n for n in gate["notices"] if n.startswith("T-001 [")]
        assert split, gate["notices"]
        note = split[0]
        # The number is still reported - the finding is about the claim, not
        # about visibility, and removing the figure would trade one defect for
        # another.
        assert "total_measurable" in note, note
        # No verdict is asserted, in either direction.
        assert "failed" not in note, note
        assert "failed separately" not in note, note
        # What it does say is checkable, and is checked here: that X-10 compares
        # this quantity against this same cap.
        assert "X-10" in note, note
        assert any("total_measurable" in n and n.startswith("T-001 [")
                   for n in bound["notices"]), bound["notices"]

    def test_the_bound_is_not_suppressed_when_revision_is_zero(self, tmp_path):
        # WHAT CHANGED - FIND-Q9-45. This was
        # `test_x08_does_not_double_report_when_revision_is_zero`, and it
        # asserted a suppression: where `revision` is zero the bound and the
        # gate are the same number over the same cap, so the bound row was not
        # emitted, on the ground that one overrun printed twice in one details
        # list reads as two findings.
        #
        # That ground died with the split - the rows are in different checks
        # now, and `row["id"]` tells them apart. Keeping the suppression would
        # have made X-10's *boolean* a function of whether `revision` happened
        # to be zero, and `revision` is the non-monotonic quantity: the check
        # would have gone silent on a real breach because the task had not yet
        # written a deliverable. So the suppression is gone, and the assertion
        # is inverted deliberately rather than dropped.
        #
        # Nothing is double-reported and nothing is hidden: X-08 fails on the
        # gate, X-10 fails on the bound, both rows state the number they used,
        # and X-10's row says in terms that it equals the gate.
        repo = build_repo(tmp_path, [{"tid": "T-001", "tf1": 10, "tf2": 10}])
        gate = checks.x08_context_budget(repo)
        bound = checks.x10_non_monotonic_measurable_bound(repo)
        assert gate["status"] == "FAIL"
        assert all(": acquisition " in d for d in gate["details"]), gate["details"]
        assert not any(": total_measurable " in d for d in gate["details"])
        # The bound is reported, not suppressed, and says why it is the same
        # number as the gate rather than leaving a reader to work it out.
        assert bound["status"] == "FAIL"
        assert all(": total_measurable " in d for d in bound["details"]), bound
        assert all("equal to the acquisition gate, because revision is zero" in d
                   for d in bound["details"]), bound["details"]
        # `total_measurable` is still reported for the task in X-08's split
        # notice, so a reader of the gate alone still sees the number.
        split = [n for n in gate["notices"] if n.startswith("T-001 [")]
        assert split and "total_measurable" in split[0], gate["notices"]

    def test_x08_reports_how_much_of_the_gate_the_task_itself_moves(self, tmp_path):
        # FIND-Q9-36 / 36b, through the check. The split notice must carry the
        # stable/self-referential decomposition of the gated figure, and must
        # attribute each moving path to the component that holds it. The
        # predecessor of this line appended the moving-path count to the
        # *revision* clause: for T-002, whose revision is zero and both of whose
        # moving paths are in `mandatory`, X-08 printed "revision TF-1 0 ...
        # non-monotonic in 2 path(s) ... (nothing charged)".
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001", "write_scope": "  - .ai/project/**"}],
        )
        row = checks.x08_context_budget(repo)
        split = [n for n in row["notices"] if n.startswith("T-001 [")]
        assert split, row["notices"]
        note = split[0]
        # Both halves of the gate are visible.
        assert "= stable " in note and "+ self-referential " in note, note
        # The movement is attributed by component, and the component is right:
        # the record and the mandatory input both live under .ai/project/**.
        assert "by component:" in note, note
        assert "record .ai/project/tasks/T-001.md" in note, note
        assert "mandatory .ai/project/OPEN_ITEMS.md" in note, note
        # Revision is zero here, so nothing may attribute the movement to it.
        assert "revision TF-1 0" in note, note
        assert "revision TF-1 0 / TF-2 0 reported, non-monotonic" not in note, note

    def test_x06_fails_on_a_record_rewritten_after_supersession(self, tmp_path):
        # FIND-Q9-28, end to end through the check. The guard this replaces went
        # *quiet* under exactly this perturbation.
        repo = build_repo(tmp_path, [{"tid": "T-001"}])
        digest = records.file_dc1(repo, ".ai/project/OPEN_ITEMS.md")
        old = repo / ".ai/project/results/R-100.md"
        old.write_text(
            RESULT.format(rid="R-100", status="SUPERSEDED",
                          path=".ai/project/OPEN_ITEMS.md", digest=digest),
            encoding="utf-8",
        )
        seal = records.file_dc1(repo, ".ai/project/results/R-100.md")
        (repo / ".ai/project/results/R-101.md").write_text(
            RESULT.format(rid="R-101", status="CURRENT",
                          path=".ai/project/OPEN_ITEMS.md", digest=digest)
            .replace("supersedes: null",
                     "supersedes: R-100\nsupersedes_seal:\n"
                     "  path: .ai/project/results/R-100.md\n"
                     f"  digest: {seal}"),
            encoding="utf-8",
        )
        assert checks.x06_result_currency(repo)["status"] == "PASS"
        old.write_text(
            old.read_text(encoding="utf-8").replace("conclusion: |\n  c", "conclusion: |\n  edited"),
            encoding="utf-8",
        )
        row = checks.x06_result_currency(repo)
        assert row["status"] == "FAIL"
        assert any("REWRITTEN AFTER SUPERSESSION" in d for d in row["details"])

    def test_x06_reports_an_unsealed_predecessor_without_accusing_it(self, tmp_path):
        repo = build_repo(tmp_path, [{"tid": "T-001"}])
        digest = records.file_dc1(repo, ".ai/project/OPEN_ITEMS.md")
        (repo / ".ai/project/results/R-100.md").write_text(
            RESULT.format(rid="R-100", status="SUPERSEDED",
                          path=".ai/project/OPEN_ITEMS.md", digest=digest),
            encoding="utf-8",
        )
        row = checks.x06_result_currency(repo)
        assert row["status"] == "PASS", row["details"]
        assert any("unsealed" in n for n in row["notices"])

    def test_measure_reports_unmeasured_rather_than_crashing(self, tmp_path, monkeypatch):
        # FIND-Q9-34: `scope.cost` is documented to return None per family, and
        # cmd_measure formatted it with `:>10,` - a partial report then a raw
        # TypeError, in the command R-008 names as its reproducibility path.
        import io
        import contextlib
        from aief_exec import __main__ as cli
        from aief_exec import scope

        monkeypatch.setattr(scope, "cost", lambda text: scope.Cost(None, None))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = cli.cmd_measure(REPO, ["T-002"])
        out = buf.getvalue()
        assert rc == 0
        assert "UNMEASURED" in out
        assert "Traceback" not in out

    def test_measure_states_that_the_sweep_is_not_a_constant(self):
        # FIND-Q9-31: the envelope contains the result and verification
        # registers, so the sweep moves whenever an audit is filed - it was
        # demonstrated moving 9,396 TF-1 by the filing of the audit that
        # measured it. The command must say so where the number is printed.
        import io
        import contextlib
        from aief_exec import __main__ as cli
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cli.cmd_measure(REPO, ["T-002"])
        out = buf.getvalue()
        assert "NOT A CONSTANT" in out
        assert ".ai/project/results/" not in out.split("NOT A CONSTANT")[0]
        assert "registers" in out

    def test_x03_rejects_an_ambiguous_anchor(self, tmp_path):
        # FIND-Q9-7: substring anchors matched first-hit-wins, silently.
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001", "mandatory": "    - path: doc.md\n      anchor: AMD-4"}],
            extra={"doc.md": "## AMD-41 one\n\ntext\n\n## AMD-42 two\n\ntext\n"},
        )
        row = checks.x03_read_scope_resolves(repo)
        assert row["status"] == "FAIL"
        assert any("ambiguous" in d for d in row["details"])

    def test_x03_accepts_an_unambiguous_anchor(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001", "mandatory": "    - path: doc.md\n      anchor: AMD-41"}],
            extra={"doc.md": "## AMD-41 one\n\ntext\n\n## AMD-42 two\n\ntext\n"},
        )
        assert checks.x03_read_scope_resolves(repo)["status"] == "PASS"

    def test_index_and_derivation_cannot_disagree(self, tmp_path):
        # A task filed READY that the derivation blocks is an index defect.
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001", "status": "READY", "blocked_by": "[OQ-14]"}],
        )
        row = checks.x02_index_bijection(repo)
        assert row["status"] == "FAIL"
        assert any("derived BLOCKED" in d for d in row["details"])


class TestX09PublicationReachability:
    """A declared `produces` must be writable and a declared `consumes` must be
    meetable. Neither field was validated anywhere before X-09 existed.

    Every test here fails against a layer without X-09 - the function is absent -
    and each covers one of the five modes on synthetic records.
    """

    PUBLISHER = "  - .ai/project/results/**"

    def test_a_well_formed_channel_passes(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "status": "COMPLETE", "produces": "[R-001]",
                 "write_scope": self.PUBLISHER},
                {"tid": "T-002", "consumes": "[R-001]", "depends_on": "[T-001]"},
            ],
            results={
                "R-001": RESULT.format(
                    rid="R-001", status="CURRENT",
                    path=".ai/project/OPEN_ITEMS.md", digest="0" * 64,
                )
            },
        )
        row = checks.x09_publication_reachability(repo)
        assert row["status"] == "PASS", row["details"]

    def test_mode_1_produces_outside_the_write_scope(self, tmp_path):
        # The live defect: contracted to publish a record it may not create.
        repo = build_repo(tmp_path, [{"tid": "T-001", "produces": "[R-001]"}])
        row = checks.x09_publication_reachability(repo)
        assert row["status"] == "FAIL"
        assert len(row["details"]) == 1, row["details"]
        d = row["details"][0]
        assert "no write_scope pattern matches .ai/project/results/R-001.md" in d
        assert "Repair:" in d and "T-001.write_scope" in d and "T-001.produces" in d

    def test_mode_1_is_cleared_by_a_covering_pattern(self, tmp_path):
        for pattern in ("  - .ai/project/results/**",
                        "  - .ai/project/results/R-001.md"):
            repo = build_repo(
                tmp_path / pattern.strip().replace("/", "_").replace("*", "x"),
                [{"tid": "T-001", "produces": "[R-001]", "write_scope": pattern}],
            )
            assert checks.x09_publication_reachability(repo)["status"] == "PASS", pattern

    def test_mode_2_consumes_a_result_no_task_produces(self, tmp_path):
        # The record exists on disk but no task owns it, so nothing can refresh
        # it when it goes stale.
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001", "consumes": "[R-001]"}],
            results={
                "R-001": RESULT.format(
                    rid="R-001", status="CURRENT",
                    path=".ai/project/OPEN_ITEMS.md", digest="0" * 64,
                )
            },
        )
        row = checks.x09_publication_reachability(repo)
        assert row["status"] == "FAIL"
        assert any("no task declares produces: R-001" in d for d in row["details"])
        assert any("exists on disk with no owning task" in d for d in row["details"])
        # Not the deadlock wording - the record is there today.
        assert not any("never become runnable" in d for d in row["details"])

    def test_mode_3_two_tasks_produce_the_same_result(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "produces": "[R-001]", "write_scope": self.PUBLISHER},
                {"tid": "T-002", "produces": "[R-001]", "write_scope": self.PUBLISHER},
            ],
        )
        row = checks.x09_publication_reachability(repo)
        assert row["status"] == "FAIL"
        assert any(
            "declared in produces by T-001, T-002" in d for d in row["details"]
        ), row["details"]
        assert any("produced_by" in d for d in row["details"])

    def test_mode_5_a_non_producer_reaching_a_result_record(self, tmp_path):
        # FIND-Q9-42, the converse of mode 1. Modes 1 and 3 both protect "a
        # result has exactly one producer" and both tested it against `produces`
        # declarations only. A task that can write a record it never declared is
        # a second producer in fact, and the check was silent on it.
        #
        # T-001 declares and can publish R-001; T-002 declares nothing and holds
        # a write scope over the whole result register. Mode 1 passes on T-001,
        # mode 3 sees one declared producer, and nothing else looked.
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "produces": "[R-001]", "write_scope": self.PUBLISHER},
                {"tid": "T-002", "write_scope": self.PUBLISHER},
            ],
        )
        row = checks.x09_publication_reachability(repo)
        assert row["status"] == "FAIL", row["details"]
        converse = [d for d in row["details"] if "does not declare produces" in d]
        assert len(converse) == 1, row["details"]
        d = converse[0]
        assert d.startswith("T-002:"), d
        assert ".ai/project/results/R-001.md" in d
        assert "T-001 does" in d
        assert "Repair:" in d and "narrow T-002.write_scope" in d
        # The declared producer is not accused of anything by this mode.
        assert not any(x.startswith("T-001:") and "does not declare" in x
                       for x in row["details"])

    def test_mode_5_is_silent_on_the_declared_producer(self, tmp_path):
        # The control. Reach plus declaration is the lawful configuration and
        # must stay clean, or the mode would make mode 1's repair impossible.
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001", "produces": "[R-001]", "write_scope": self.PUBLISHER}],
        )
        assert checks.x09_publication_reachability(repo)["status"] == "PASS"

    def test_mode_5_covers_an_orphaned_record_on_disk(self, tmp_path):
        # A record nobody declares is mode 2's business, but an undeclared
        # writer of it is the same hazard, not a lesser one: it can be rewritten
        # by a task that never claimed it and nothing derives `produced_by`.
        repo = build_repo(
            tmp_path,
            [{"tid": "T-001", "write_scope": self.PUBLISHER}],
            results={
                "R-050": RESULT.format(
                    rid="R-050", status="CURRENT",
                    path=".ai/project/OPEN_ITEMS.md", digest="0" * 64,
                )
            },
        )
        row = checks.x09_publication_reachability(repo)
        assert row["status"] == "FAIL"
        d = [x for x in row["details"] if "does not declare produces" in x]
        assert len(d) == 1 and "R-050" in d[0], row["details"]
        assert "no task does" in d[0], d[0]

    def test_mode_4_consumes_a_result_that_is_nowhere(self, tmp_path):
        repo = build_repo(tmp_path, [{"tid": "T-001", "consumes": "[R-099]"}])
        row = checks.x09_publication_reachability(repo)
        assert row["status"] == "FAIL"
        assert any("never become runnable" in d for d in row["details"]), row["details"]
        assert any(
            "neither on disk at .ai/project/results/R-099.md" in d
            for d in row["details"]
        ), row["details"]

    def test_the_derived_grant_is_reported_and_never_applied(self, tmp_path):
        # A4 is not pre-empted: X-09 reports the gap, X-04 keeps testing the
        # declared scope, and neither widens anything.
        repo = build_repo(tmp_path, [{"tid": "T-001", "produces": "[R-001]"}])
        row = checks.x09_publication_reachability(repo)
        assert any("DERIVED, NOT GRANTED" in n for n in row["notices"])
        task = records.load_tasks(repo)["T-001"]
        assert task.write_scope == ["out/**"]
        assert task.effective_write_scope == [
            "out/**", ".ai/project/results/R-001.md",
        ]

    def test_x09_is_registered_in_the_campaign(self, tmp_path):
        # WHAT CHANGED - FIND-Q9-45 added X-10, the first two-digit check. The
        # id is asserted in its zero-padded two-digit form for every check, so a
        # tenth that formats itself as `X10` fails here rather than in a
        # consumer.
        repo = build_repo(tmp_path, [{"tid": "T-001"}])
        ids = [r["id"] for r in checks.run_all(repo)]
        assert ids == [f"X-{i:02d}" for i in range(1, 11)], ids


class TestX06SealEpoch:
    """A supersession published from the seal epoch onward must carry a seal;
    one published before it is history and is reported, not failed.

    `R-001` and `R-007` are superseded by records that pin no digest of them, so
    a rewrite of either after supersession is undetectable. Failing them would be
    applying a rule backwards - the field post-dates the records.

    WHAT CHANGED, and why - `VER-009` FIND-Q9-39. The discriminator used to be
    derived from the records: `min()` over the sessions of the records that
    carry a seal. That made the rule a function of the data it polices, and the
    auditor switched it off by deleting three fields. It is now the declared
    constant `graph.SEAL_EPOCH`, and the derivation is retained as evidence
    only, under `graph.derived_seal_epoch`, with X-06 printing any disagreement.
    Two tests below were restated onto that; the tamper is now a test of its own.
    """

    SEALED = """# {rid}

```yaml
result_id: {rid}
produced_by: {{task: T-001, role: software.software-engineer, session: {session}}}
status: {status}
{backlink}supersedes: {supersedes}
{seal}inputs:
  - path: {path}
    digest: {digest}
deliverables:
  - path: {path}
    digest: {digest}
affected: []
validation: []
conclusion: |
  c
findings: []
```
"""

    def _chain(self, root, tail=None):
        """R-100 <- R-101 (unsealed, session -01) <- R-102 (sealed, session -06).

        WHAT CHANGED - FIND-Q9-43. Each superseded record now also carries
        `superseded_by`, the predecessor's half of the link, because every
        superseded record in the live repository has carried it since `R-001`
        and a fixture without it cannot exercise the cross-check that reads it.
        The missing-back-link case is a test of its own rather than the
        fixture's silent default.
        """
        repo = build_repo(root, [{"tid": "T-001"}])
        digest = records.file_dc1(repo, ".ai/project/OPEN_ITEMS.md")
        d = repo / ".ai/project/results"

        def write(rid, status, supersedes, session, seal_of=None, superseded_by=None):
            seal = ""
            if seal_of:
                seal = (
                    f"supersedes_seal:\n"
                    f"  path: .ai/project/results/{seal_of}.md\n"
                    f"  digest: {records.file_dc1(repo, f'.ai/project/results/{seal_of}.md')}\n"
                )
            (d / f"{rid}.md").write_text(
                self.SEALED.format(
                    rid=rid, status=status, supersedes=supersedes, session=session,
                    seal=seal, path=".ai/project/OPEN_ITEMS.md", digest=digest,
                    backlink=(
                        f"superseded_by: {superseded_by}\n" if superseded_by else ""
                    ),
                ),
                encoding="utf-8",
            )

        write("R-100", "SUPERSEDED", "null", "S-2026-08-09-01",
              superseded_by="R-101")
        write("R-101", "SUPERSEDED", "R-100", "S-2026-08-09-01",
              superseded_by="R-102")
        write("R-102", "CURRENT" if not tail else "SUPERSEDED", "R-101",
              "S-2026-08-09-06", seal_of="R-101",
              superseded_by="R-103" if tail else None)
        if tail:
            write("R-103", "CURRENT", "R-102", tail)
        return repo

    def test_the_epoch_is_declared_and_the_derivation_is_only_evidence(self, tmp_path):
        # NAME CHANGED, deliberately, because the property changed. The old node
        # id was `test_the_epoch_is_the_earliest_sealing_session` and that is
        # exactly the property FIND-Q9-39 removed: an epoch that is the earliest
        # sealing session is an epoch a tamperer can raise or empty by editing
        # sealing sessions. What is asserted now is that the two are separate
        # functions and that only one of them decides anything.
        from aief_exec import graph
        results = records.load_results(self._chain(tmp_path))
        # The derivation still reads the records - it is the evidence.
        assert graph.derived_seal_epoch(results) == "S-2026-08-09-06"
        # The rule does not. It is the same value here only because the constant
        # is correct, which is the point of keeping both.
        assert graph.seal_epoch(results) == graph.SEAL_EPOCH == "S-2026-08-09-06"
        # And the rule cannot be moved by the records it is applied to.
        assert graph.seal_epoch({}) == graph.SEAL_EPOCH

    def test_with_no_seal_anywhere_the_rule_is_no_longer_vacuous(self, tmp_path):
        # NAME CHANGED for the same reason: the old node id recorded the
        # residual `seal_epoch` used to disclose - "before any seal exists the
        # epoch is empty and the rule is vacuous". FIND-Q9-39 showed that state
        # is reachable by deletion from a fully sealed chain, not only at the
        # beginning of history, so it is not a residual the rule may keep.
        #
        # These two records are genuinely pre-epoch history, so the *outcome* is
        # unchanged - reported, not failed. What changed is the reason: it is
        # now the session comparison that spares them, not an empty epoch that
        # spares everything.
        from aief_exec import graph
        repo = build_repo(tmp_path, [{"tid": "T-001"}])
        digest = records.file_dc1(repo, ".ai/project/OPEN_ITEMS.md")
        d = repo / ".ai/project/results"
        for rid, status, sup in (("R-100", "SUPERSEDED", "null"),
                                 ("R-101", "CURRENT", "R-100")):
            (d / f"{rid}.md").write_text(
                self.SEALED.format(rid=rid, status=status, supersedes=sup,
                                   session="S-2026-08-09-01", seal="",
                                   backlink="superseded_by: R-101\n" if
                                   rid == "R-100" else "",
                                   path=".ai/project/OPEN_ITEMS.md", digest=digest),
                encoding="utf-8",
            )
        assert graph.derived_seal_epoch(records.load_results(repo)) == ""
        assert graph.seal_epoch(records.load_results(repo)) == graph.SEAL_EPOCH
        row = checks.x06_result_currency(repo)
        assert row["status"] == "PASS", row["details"]
        assert any("pins no supersedes_seal" in n for n in row["notices"])
        # The notice says what it means. Under the derived epoch it read
        # "predates any sealed supersession", which became false the moment the
        # emptiness was caused by deletion rather than by there being no history.
        note = [n for n in row["notices"] if "pins no supersedes_seal" in n][0]
        assert graph.SEAL_EPOCH in note, note
        assert "any sealed supersession" not in note, note

    def test_stripping_every_seal_does_not_disarm_the_rule(self, tmp_path):
        # FIND-Q9-39, the exact perturbation, end to end through the check.
        #
        # The auditor removed the `supersedes_seal` block from R-009, R-010 and
        # R-011 - the successors, which `result_currency` claimed was where the
        # evidence safely lived - and X-06 returned PASS with zero details. The
        # epoch was `min()` over the records that carry a seal, so deleting
        # every seal emptied it, and an empty epoch made the rule vacuous for
        # all six records at once. A guard that rewards the tampering it exists
        # to expose is the FIND-Q9-27 shape, relocated to the epoch.
        #
        # This test fails against that behaviour and passes against a declared
        # constant.
        from aief_exec import graph
        repo = self._chain(tmp_path, tail="S-2026-08-09-07")
        p = repo / ".ai/project/results/R-103.md"
        seal = records.file_dc1(repo, ".ai/project/results/R-102.md")
        p.write_text(
            p.read_text(encoding="utf-8").replace(
                "supersedes: R-102\n",
                "supersedes: R-102\nsupersedes_seal:\n"
                "  path: .ai/project/results/R-102.md\n"
                f"  digest: {seal}\n",
            ),
            encoding="utf-8",
        )
        assert checks.x06_result_currency(repo)["status"] == "PASS"

        # Now strip every seal in the chain - both post-epoch supersessions.
        import re as _re
        stripped = 0
        for rid in ("R-102", "R-103"):
            q = repo / f".ai/project/results/{rid}.md"
            body = q.read_text(encoding="utf-8")
            new = _re.sub(
                r"supersedes_seal:\n  path: [^\n]*\n  digest: [^\n]*\n", "", body
            )
            assert new != body, rid
            q.write_text(new, encoding="utf-8")
            stripped += 1
        assert stripped == 2
        results = records.load_results(repo)
        assert graph.derived_seal_epoch(results) == "", "the tamper did not land"

        row = checks.x06_result_currency(repo)
        assert row["status"] == "FAIL", (
            "stripping every seal returned X-06 to PASS - the epoch is being "
            "derived from the records it polices again"
        )
        offenders = sorted({d.split(":")[0] for d in row["details"]
                            if "pins no supersedes_seal" in d})
        assert offenders == ["R-102", "R-103"], row["details"]
        # And the disagreement between the constant and the records is itself
        # reported, so the tamper leaves a trace beyond the failure.
        disagreement = [n for n in row["notices"] if n.startswith("seal epoch:")]
        assert disagreement, row["notices"]
        assert graph.SEAL_EPOCH in disagreement[0]
        assert "no record carries a supersedes_seal" in disagreement[0]

    def test_deleting_the_successors_supersedes_does_not_disarm_the_seal(
        self, tmp_path
    ):
        # FIND-Q9-43, the exact attack the auditor ran on R-011/R-012, end to
        # end through the check. It is D1 in VER-009 section 31.1.
        #
        # Pinning the epoch (FIND-Q9-39) hardened the discriminator and left the
        # trigger under the tamperer's hand: the rule is guarded by
        # `if result.supersedes and not <seal>`, and `supersedes` is a line in a
        # file the tampering party is already editing. Deleting `supersedes` and
        # the seal from the successor - two lines, one record - returned X-06 to
        # PASS with a single notice, after which the predecessor could be
        # rewritten with no alarm of any kind.
        #
        # This test fails against that behaviour: the predecessor's own
        # `superseded_by` contradicts the successor's silence, and a
        # contradiction between two records is not something either of them can
        # delete alone.
        repo = self._chain(tmp_path, tail="S-2026-08-09-07")
        p = repo / ".ai/project/results/R-103.md"
        seal = records.file_dc1(repo, ".ai/project/results/R-102.md")
        p.write_text(
            p.read_text(encoding="utf-8").replace(
                "supersedes: R-102\n",
                "supersedes: R-102\nsupersedes_seal:\n"
                "  path: .ai/project/results/R-102.md\n"
                f"  digest: {seal}\n",
            ),
            encoding="utf-8",
        )
        assert checks.x06_result_currency(repo)["status"] == "PASS"

        # THE ATTACK, step 1: delete the successor's `supersedes` line and the
        # seal block that hangs off it. R-102 still declares
        # `superseded_by: R-103`, which is the half the tamperer did not think
        # to reach - and which nothing in the layer used to read.
        import re as _re
        body = p.read_text(encoding="utf-8")
        new = _re.sub(r"supersedes: R-102\n", "supersedes: null\n", body)
        new = _re.sub(
            r"supersedes_seal:\n  path: [^\n]*\n  digest: [^\n]*\n", "", new
        )
        assert new != body and "supersedes: R-102" not in new
        p.write_text(new, encoding="utf-8")

        row = checks.x06_result_currency(repo)
        assert row["status"] == "FAIL", (
            "deleting the successor's `supersedes` returned X-06 to PASS - the "
            "seal is still disarmable by the party it constrains"
        )
        contradiction = [d for d in row["details"] if d.startswith("R-102:")]
        assert contradiction, row["details"]
        assert "superseded_by R-103" in contradiction[0], contradiction
        assert "contradict" in contradiction[0], contradiction
        assert "Repair:" in contradiction[0], contradiction

        # THE ATTACK, step 2: with the link denied, rewrite the predecessor.
        # Under the defect this produced no alarm at all. It must still fail,
        # and the failure must still name R-102.
        q = repo / ".ai/project/results/R-102.md"
        q.write_text(
            q.read_text(encoding="utf-8")
            + "\nTAMPERED: this paragraph was appended after supersession.\n",
            encoding="utf-8",
        )
        after = checks.x06_result_currency(repo)
        assert after["status"] == "FAIL", after["details"]
        assert any(d.startswith("R-102:") for d in after["details"]), after["details"]

    def test_a_predecessor_naming_a_successor_that_does_not_exist_fails(
        self, tmp_path
    ):
        # The degenerate form of the same contradiction: `superseded_by` naming
        # nothing at all. A supersession names a record that can be read.
        repo = self._chain(tmp_path)
        p = repo / ".ai/project/results/R-101.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace(
                "superseded_by: R-102", "superseded_by: R-999"
            ),
            encoding="utf-8",
        )
        row = checks.x06_result_currency(repo)
        assert row["status"] == "FAIL", row["details"]
        fail = [d for d in row["details"] if "R-999" in d]
        assert fail and fail[0].startswith("R-101:"), row["details"]
        assert "no such result record exists" in fail[0], fail

    def test_two_records_claiming_the_same_predecessor_disagree_visibly(
        self, tmp_path
    ):
        # The other direction of the cross-check: R-101 declares it supersedes
        # R-100, a second record R-103 declares the same, and R-100 names R-103.
        # Two successors is no successor - `produced_by` provenance for the
        # chain is underivable while the records disagree.
        #
        # R-100 is edited rather than R-101 because R-100 is the unsealed end of
        # this fixture. Editing a sealed record would trip the seal instead,
        # which is a different control and is asserted elsewhere.
        repo = self._chain(tmp_path)
        src = (repo / ".ai/project/results/R-101.md").read_text(encoding="utf-8")
        (repo / ".ai/project/results/R-103.md").write_text(
            src.replace("result_id: R-101", "result_id: R-103")
               .replace("superseded_by: R-102\n", "")
               .replace("status: SUPERSEDED", "status: CURRENT")
               .replace("# R-101", "# R-103"),
            encoding="utf-8",
        )
        p = repo / ".ai/project/results/R-100.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace(
                "superseded_by: R-101", "superseded_by: R-103"
            ),
            encoding="utf-8",
        )
        row = checks.x06_result_currency(repo)
        assert row["status"] == "FAIL", row["details"]
        assert any(d.startswith("R-100:") and "R-103" in d and "R-101" in d
                   for d in row["details"]), row["details"]

    def test_a_missing_back_link_is_reported_as_a_blind_spot_not_failed(
        self, tmp_path
    ):
        # A record may omit `superseded_by` - it is not a required field, and
        # requiring it is a schema change this check does not get to make
        # (LAW-12). What must not happen is silence: the cross-check is blind
        # for that link and says so.
        repo = self._chain(tmp_path)
        p = repo / ".ai/project/results/R-100.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace("superseded_by: R-101\n", ""),
            encoding="utf-8",
        )
        row = checks.x06_result_currency(repo)
        assert row["status"] == "PASS", row["details"]
        blind = [n for n in row["notices"]
                 if n.startswith("R-100:") and "no superseded_by" in n]
        assert blind, row["notices"]
        assert "blind" in blind[0] and "LAW-12" in blind[0], blind

    def test_the_live_chain_declares_the_link_from_both_sides(self):
        # The property the repair depends on, asserted against the live records
        # rather than a fixture: every superseded record here names its
        # successor, so the cross-check has evidence for every link in the
        # chain and is blind for none of them.
        from aief_exec import graph
        results = records.load_results(REPO)
        superseded = [rid for rid in sorted(results)
                      if graph.successor_of(results, rid)]
        assert len(superseded) >= 5, superseded
        for rid in superseded:
            assert results[rid].superseded_by == graph.successor_of(results, rid), rid

    def test_a_supersession_predating_the_epoch_is_reported_not_failed(self, tmp_path):
        row = checks.x06_result_currency(self._chain(tmp_path))
        assert row["status"] == "PASS", row["details"]
        note = [n for n in row["notices"] if "R-101" in n and "supersedes R-100" in n]
        assert note, row["notices"]
        assert "is history" in note[0]

    def test_a_supersession_at_or_after_the_epoch_fails(self, tmp_path):
        for session in ("S-2026-08-09-06", "S-2026-08-09-07", "S-2026-08-10-01"):
            repo = self._chain(tmp_path / session, tail=session)
            row = checks.x06_result_currency(repo)
            assert row["status"] == "FAIL", (session, row["details"])
            fail = [d for d in row["details"] if d.startswith("R-103:")]
            assert fail, row["details"]
            assert "pins no supersedes_seal" in fail[0]
            assert "Repair:" in fail[0] and "supersedes_seal" in fail[0]

    def test_sealing_the_new_supersession_clears_it(self, tmp_path):
        repo = self._chain(tmp_path, tail="S-2026-08-09-07")
        p = repo / ".ai/project/results/R-103.md"
        seal = records.file_dc1(repo, ".ai/project/results/R-102.md")
        p.write_text(
            p.read_text(encoding="utf-8").replace(
                "supersedes: R-102\n",
                "supersedes: R-102\nsupersedes_seal:\n"
                "  path: .ai/project/results/R-102.md\n"
                f"  digest: {seal}\n",
            ),
            encoding="utf-8",
        )
        row = checks.x06_result_currency(repo)
        assert row["status"] == "PASS", row["details"]

    def test_the_historical_live_records_are_never_failed(self, tmp_path):
        # R-007 and R-008 supersede without a seal at session S-2026-08-09-01;
        # the epoch is S-2026-08-09-06, the session that published R-009's seal.
        from aief_exec import graph
        results = records.load_results(REPO)
        assert graph.seal_epoch(results) == "S-2026-08-09-06"
        row = checks.x06_result_currency(REPO)
        assert not any("pins no supersedes_seal" in d for d in row["details"])
        unsealed = [n for n in row["notices"] if "pins no supersedes_seal" in n]
        assert sorted(n.split(":")[0] for n in unsealed) == ["R-007", "R-008"]


class TestEvidenceContaminationRegression:
    """The T-002/T-004-shaped incident, end to end through the plan.

    A verifier consumes a result that pins `tests/**` deliverables; a producer
    writes into `tests/**`. The verifier names no test file, writes no test file
    and reads no test file as a declared input, so both original hazard limbs are
    silent and the pair classified PARALLEL - while the verifier's evidence was
    being taken over a tree the producer was rewriting.
    """

    def _repo(self, tmp_path, **verifier):
        spec = {
            "tid": "T-004",
            "consumes": "[R-001]",
            "depends_on": "[T-001]",
            "write_scope": "  - .ai/project/verification/**",
        }
        spec.update(verifier)
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "status": "COMPLETE", "produces": "[R-001]",
                 "write_scope": "  - .ai/project/results/**"},
                {"tid": "T-002", "write_scope": "  - tests/test_stage6_*.py"},
                spec,
            ],
        )
        (repo / "tests").mkdir(parents=True, exist_ok=True)
        (repo / "tests/test_stage6_crash.py").write_text("x = 1\n", encoding="utf-8")
        digest = records.file_dc1(repo, "tests/test_stage6_crash.py")
        (repo / ".ai/project/results/R-001.md").write_text(
            RESULT.format(rid="R-001", status="CURRENT",
                          path="tests/test_stage6_crash.py", digest=digest),
            encoding="utf-8",
        )
        return repo

    def test_the_incident_pair_is_no_longer_parallel(self, tmp_path):
        from aief_exec import graph
        repo = self._repo(tmp_path)
        plan = graph.build_plan(repo)
        kind, why = plan.pairs[("T-002", "T-004")]
        assert kind == graph.CONFLICT, (kind, why)
        assert any(graph.HZ_WRITE_OBSERVE in r for r in why), why
        assert any("evidence contamination" in r for r in why), why
        assert any("tests/test_stage6_crash.py" in r for r in why), why
        # The two original limbs are still silent - this is a third hazard, not
        # a re-description of either.
        assert not any(graph.HZ_WRITE_WRITE in r for r in why), why
        assert not any(graph.HZ_WRITE_READ in r for r in why), why

    def test_they_never_share_a_dispatch_group(self, tmp_path):
        from aief_exec import graph
        repo = self._repo(tmp_path)
        plan = graph.build_plan(repo)
        home = {t: i for i, g in enumerate(plan.parallel_sets()) for t in g}
        assert home["T-002"] != home["T-004"]
        assert checks.x07_no_concurrent_write_conflict(repo)["status"] == "PASS"

    def test_the_surface_comes_from_the_consumed_result_not_the_record(self, tmp_path):
        from aief_exec import graph
        repo = self._repo(tmp_path)
        task = records.load_tasks(repo)["T-004"]
        # Nothing in T-004's own record names a test file.
        assert not any("test" in p for p in task.write_scope)
        surface = graph.observed_surface(repo, task, records.load_results(repo))
        assert "tests/test_stage6_crash.py" in surface

    def test_a_verifier_consuming_nothing_stays_parallel(self, tmp_path):
        # The control: without the consumed result there is no derived surface,
        # and the pair is genuinely independent.
        from aief_exec import graph
        repo = self._repo(tmp_path, consumes="[]", depends_on="[]")
        kind, why = graph.build_plan(repo).pairs[("T-002", "T-004")]
        assert kind == graph.PARALLEL, (kind, why)

    def test_x07_notices_that_an_undeclared_observation_is_invisible(self, tmp_path):
        # The honest residual, reported where the dispatch decision is made.
        repo = build_repo(tmp_path, [{"tid": "T-001"}])
        p = repo / ".ai/project/tasks/T-001.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace("    test: t", "    test: pytest tests/"),
            encoding="utf-8",
        )
        row = checks.x07_no_concurrent_write_conflict(repo)
        assert row["status"] == "PASS"
        assert any("may exceed what is declared" in n for n in row["notices"])
        assert any("Heuristic" in n for n in row["notices"])


class TestClassifyExplainability:
    """`aief_exec classify` must show its working. A bare PARALLEL is an
    assertion the reader cannot check."""

    def _run(self, repo, a, b):
        import io
        import contextlib
        from aief_exec import __main__ as cli
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cli.cmd_classify(repo, [a, b])
        return buf.getvalue()

    def test_a_parallel_verdict_prints_why_it_is_safe(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "write_scope": "  - a/**"},
                {"tid": "T-002", "write_scope": "  - b/**"},
            ],
        )
        out = self._run(repo, "T-001", "T-002")
        assert "PARALLEL" in out
        assert "WHY SAFE" in out
        assert out.count("intersection EMPTY") == 5, out
        for cls in ("write/write", "write/read", "write/observe"):
            assert cls in out, cls
        assert "OBSERVED SURFACE" in out

    def test_a_conflict_verdict_names_the_hazard_class_and_witnesses(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "write_scope": "  - out/shared/**"},
                {"tid": "T-002", "write_scope": "  - out/shared/**"},
            ],
        )
        out = self._run(repo, "T-001", "T-002")
        assert "CONFLICT" in out
        assert "hazard class" in out
        assert "[write/write]" in out
        assert "[write/observe]" in out

    def test_a_serial_verdict_names_its_class(self, tmp_path):
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "status": "COMPLETE"},
                {"tid": "T-002", "depends_on": "[T-001]"},
            ],
        )
        out = self._run(repo, "T-001", "T-002")
        assert "SERIAL" in out
        assert "serial/dependency" in out

    def test_scope_prints_the_derived_publication_channel_as_ungranted(self, tmp_path):
        import io
        import contextlib
        from aief_exec import __main__ as cli
        repo = build_repo(tmp_path, [{"tid": "T-001", "produces": "[R-001]"}])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cli.cmd_scope(repo, ["T-001"])
        out = buf.getvalue()
        assert "DERIVED, NOT GRANTED" in out
        assert ".ai/project/results/R-001.md" in out
        assert "NOT COVERED" in out
        # and the three budget quantities are named, never merged
        assert "ACQUISITION" in out and "GATED" in out
        assert "REVISION" in out and "not gated" in out
        assert "TELEMETRY" in out and "UNMEASURABLE" in out


class TestReadScopeEnforcement:
    def test_x03_catches_a_task_widening_into_its_own_forbidden_scope(self, tmp_path):
        # An agent may not expand its read scope by declaring a path it has also
        # declared forbidden.
        repo = build_repo(tmp_path, [{"tid": "T-001"}])
        p = repo / ".ai/project/tasks/T-001.md"
        body = p.read_text(encoding="utf-8").replace(
            "  forbidden: []", "  forbidden:\n    - .ai/project/OPEN_ITEMS.md"
        )
        p.write_text(body, encoding="utf-8")
        row = checks.x03_read_scope_resolves(repo)
        assert row["status"] == "FAIL"
        assert any("forbidden read scope" in d for d in row["details"])


class TestWriteAttribution:
    def test_a_change_inside_the_write_scope_is_attributed(self, tmp_path):
        from aief_exec import scope
        repo = build_repo(tmp_path, [{"tid": "T-001", "write_scope": "  - out/**"}])
        tasks = records.load_tasks(repo)
        got = scope.attribute(repo, ["out/a.txt"], tasks)
        assert got["out/a.txt"] == ["T-001"]

    def test_a_change_outside_every_write_scope_is_unattributed(self, tmp_path):
        from aief_exec import scope
        repo = build_repo(tmp_path, [{"tid": "T-001", "write_scope": "  - out/**"}])
        tasks = records.load_tasks(repo)
        got = scope.attribute(repo, ["elsewhere/b.txt"], tasks)
        assert got["elsewhere/b.txt"] == []


class TestResultFanOut:
    def test_one_result_feeds_two_independent_tasks(self, tmp_path):
        """SHARE RESULTS, NOT CONTEXT: R-001 -> T-002 and T-003, which consume the
        conclusion and never the producing task's inputs."""
        from aief_exec import graph
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "status": "COMPLETE", "produces": "[R-001]"},
                {
                    "tid": "T-002",
                    "depends_on": "[T-001]",
                    "consumes": "[R-001]",
                    "write_scope": "  - a/**",
                },
                {
                    "tid": "T-003",
                    "depends_on": "[T-001]",
                    "consumes": "[R-001]",
                    "write_scope": "  - b/**",
                },
            ],
        )
        digest = records.file_dc1(repo, ".ai/project/OPEN_ITEMS.md")
        (repo / ".ai/project/results/R-001.md").write_text(
            RESULT.format(
                rid="R-001",
                status="CURRENT",
                path=".ai/project/OPEN_ITEMS.md",
                digest=digest,
            ),
            encoding="utf-8",
        )
        plan = graph.build_plan(repo)
        assert plan.states["T-002"] == "READY"
        assert plan.states["T-003"] == "READY"
        # The two consumers are independent of each other.
        assert plan.pairs[("T-002", "T-003")][0] == graph.PARALLEL
        assert len(plan.parallel_sets()) == 1

    def test_drift_in_the_shared_result_blocks_both_consumers(self, tmp_path):
        from aief_exec import graph
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "status": "COMPLETE", "produces": "[R-001]"},
                {"tid": "T-002", "depends_on": "[T-001]", "consumes": "[R-001]"},
                {"tid": "T-003", "depends_on": "[T-001]", "consumes": "[R-001]"},
            ],
        )
        (repo / ".ai/project/results/R-001.md").write_text(
            RESULT.format(
                rid="R-001",
                status="CURRENT",
                path=".ai/project/OPEN_ITEMS.md",
                digest="0" * 64,
            ),
            encoding="utf-8",
        )
        plan = graph.build_plan(repo)
        assert plan.states["T-002"] == graph.BLOCKED
        assert plan.states["T-003"] == graph.BLOCKED
        for tid in ("T-002", "T-003"):
            assert any("STALE" in r for r in plan.blocked[tid])


class TestDecisionPause:
    def test_awaiting_decision_is_a_state_not_a_termination(self, tmp_path):
        from aief_exec import graph
        repo = build_repo(
            tmp_path, [{"tid": "T-001", "status": "AWAITING-DECISION"}]
        )
        plan = graph.build_plan(repo)
        assert plan.states["T-001"] == "AWAITING-DECISION"
        # Not BLOCKED and not COMPLETE - the task is alive and resumable.
        assert plan.states["T-001"] not in (graph.BLOCKED, "COMPLETE")

    def test_checkpoint_survives_the_pause(self, tmp_path):
        repo = build_repo(tmp_path, [{"tid": "T-001", "status": "AWAITING-DECISION"}])
        p = repo / ".ai/project/tasks/T-001.md"
        body = p.read_text(encoding="utf-8").replace(
            "  completed: []", "  completed:\n    - step one\n    - step two"
        ).replace(
            "  decision: null",
            "  decision:\n    id: D-001\n    status: OPEN\n    question: q",
        )
        p.write_text(body, encoding="utf-8")
        task = records.load_tasks(repo)["T-001"]
        assert task.checkpoint["completed"] == ["step one", "step two"]
        assert task.checkpoint["decision"]["status"] == "OPEN"


class TestBlockedDerivation:
    def test_open_item_blocks(self, tmp_path):
        from aief_exec import graph
        repo = build_repo(tmp_path, [{"tid": "T-001", "blocked_by": "[OQ-14]"}])
        plan = graph.build_plan(repo)
        assert plan.states["T-001"] == graph.BLOCKED

    def test_closed_item_does_not_block(self, tmp_path):
        from aief_exec import graph
        repo = build_repo(tmp_path, [{"tid": "T-001", "blocked_by": "[OQ-15]"}])
        plan = graph.build_plan(repo)
        assert plan.states["T-001"] == "READY"
