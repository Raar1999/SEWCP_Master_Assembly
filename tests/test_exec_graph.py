"""Classification: BLOCKED, SERIAL, CONFLICT, PARALLEL, and result currency.

Actor provenance: software.software-engineer - S-2026-08-09-01.

Contract under test: `.ai/project/EXECUTION_ARCHITECTURE.md` sections 6.1 and 7.
Every classification is computed; none is read from a record.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from aief_exec import graph, records

REPO = Path(__file__).resolve().parents[1]


def _task(tid, **kw):
    data = {
        "task_id": tid,
        "status": "READY",
        "depends_on": [],
        "consumes": [],
        "produces": [],
        "blocked_by": [],
        "write_scope": [],
        "read_scope": {"mandatory": []},
    }
    data.update(kw)
    return records.TaskRecord(task_id=tid, path=f"tasks/{tid}.md", data=data)


class TestCycles:
    def test_acyclic_graph_reports_none(self):
        tasks = {
            "T-001": _task("T-001"),
            "T-002": _task("T-002", depends_on=["T-001"]),
        }
        assert graph.cycles(tasks) == []

    def test_cycle_is_detected(self):
        tasks = {
            "T-001": _task("T-001", depends_on=["T-002"]),
            "T-002": _task("T-002", depends_on=["T-001"]),
        }
        assert graph.cycles(tasks)

    def test_transitive_deps(self):
        tasks = {
            "T-001": _task("T-001"),
            "T-002": _task("T-002", depends_on=["T-001"]),
            "T-003": _task("T-003", depends_on=["T-002"]),
        }
        assert graph.transitive_deps(tasks, "T-003") == {"T-001", "T-002"}


class TestConflict:
    def test_identical_write_scope_conflicts(self):
        a = _task("T-0A", write_scope=["tests/test_stage6_*.py"])
        b = _task("T-0B", write_scope=["tests/test_stage6_*.py"])
        assert graph.conflict_reasons(REPO, a, b)

    def test_disjoint_write_scope_does_not_conflict(self):
        a = _task("T-0A", write_scope=["src/aief_exec/**"])
        b = _task("T-0B", write_scope=["src/aief_stage6/**"])
        assert not graph.conflict_reasons(REPO, a, b)

    def test_writer_versus_reader_conflicts(self):
        # One task writing what another must read is a conflict even though the
        # write scopes themselves are disjoint.
        a = _task("T-0A", write_scope=["src/aief_stage6/budget.py"])
        b = _task(
            "T-0B",
            write_scope=["docs/**"],
            read_scope={"mandatory": [{"path": "src/aief_stage6/budget.py"}]},
        )
        reasons = graph.conflict_reasons(REPO, a, b)
        assert any("must read" in r for r in reasons)


class TestReadSurface:
    """`VER-009` FIND-Q9-38. The cost model enumerated five surfaces and the
    hazard model compared three, so a task could be charged for reading a file
    that no comparison would defend.

    Every test here fails against a `conflict_reasons` that iterates
    `read_entries("mandatory")` and passes against one that compares
    `read_surface`. The last two are honesty tests for the residual, and fail
    against a layer that claims to have closed it.
    """

    def _reader(self, tid, kind, path, **kw):
        return _task(tid, read_scope={kind: [{"path": path}]}, **kw)

    def test_the_surface_is_exactly_what_acquisition_charges(self):
        # The structural guard, and the reason this is one fix and not four:
        # both models read `scope.acquisition_units`, so a component added to
        # the charge is compared in the same edit. If these two ever disagree
        # the asymmetry is back, whatever the individual limbs assert.
        from aief_exec import scope
        results = records.load_results(REPO)
        for tid, task in sorted(records.load_tasks(REPO).items()):
            cc = scope.charged_context(REPO, task, results)
            charged = {
                label.split("#", 1)[0]
                for kind, label, _ in cc.components
                if kind in scope.ACQUISITION_COMPONENTS
            }
            compared = {rel for _, rel in graph.read_surface(REPO, task, results)}
            assert charged <= compared, (tid, sorted(charged - compared))

    def test_optional_read_scope_is_compared(self):
        # E1, the auditor's matched-pair control. The two pairs below differ in
        # one token - the declaration class of an otherwise identical path - and
        # under the previous limb that token decided the verdict: optional
        # returned PARALLEL, mandatory returned CONFLICT. A budget charges both.
        writer = _task("T-0A", write_scope=["src/aief_exec/records.py"])
        verdicts = {}
        for kind in ("mandatory", "optional"):
            reader = self._reader("T-0B", kind, "src/aief_exec/records.py",
                                  write_scope=["docs/**"])
            verdicts[kind] = graph.conflict_reasons(REPO, writer, reader, results={})
        assert verdicts["mandatory"], "the control itself is broken"
        assert verdicts["optional"], (
            "an optional read is not compared - the declaration class is "
            "deciding safety"
        )
        assert any(graph.HZ_WRITE_READ in r for r in verdicts["optional"])
        assert "optional" in " ".join(verdicts["optional"])

    def test_the_consumed_result_record_itself_is_compared(self):
        # E2. `observed_surface` adds the deliverables a consumed result pins
        # and never the record itself, yet a consumer must read that file to
        # establish the record is CURRENT and unsuperseded - which is exactly
        # why `charged_context` charges it whole under `dependency`.
        writer = _task("T-0A", write_scope=[".ai/project/results/R-011.md"])
        reader = _task("T-0B", write_scope=["docs/**"], consumes=["R-900"])
        results = {"R-900": records.ResultRecord(
            "R-900", ".ai/project/results/R-011.md",
            {"result_id": "R-900", "status": "CURRENT", "deliverables": []},
        )}
        surface = dict((rel, kind) for kind, rel in
                       graph.read_surface(REPO, reader, results))
        assert surface.get(".ai/project/results/R-011.md") == "dependency"
        reasons = graph.conflict_reasons(REPO, writer, reader, results=results)
        assert any(graph.HZ_WRITE_READ in r for r in reasons), reasons
        assert "dependency" in " ".join(reasons)

    def test_a_tasks_own_record_is_compared(self):
        # E3. The task's own contract was on no surface at all - not write, not
        # read, not observed - while X-08 charged it under `record`.
        writer = _task("T-0A", write_scope=["tasks/**"])
        reader = _task("T-0B", write_scope=["docs/**"])
        surface = dict((rel, kind) for kind, rel in graph.read_surface(REPO, reader))
        assert surface.get("tasks/T-0B.md") == "record"
        reasons = graph.conflict_reasons(REPO, writer, reader, results={})
        assert any(graph.HZ_WRITE_READ in r for r in reasons), reasons
        assert "the contract it is executing" in " ".join(reasons)

    def test_the_reason_names_the_component_that_carried_the_hazard(self):
        # The taxonomy stays three tags wide; the substance goes in the
        # sentence. A reader must be able to tell a rewritten contract from a
        # rewritten input without a fourth class to parse.
        writer = _task("T-0A", write_scope=["src/aief_exec/**", "tasks/**"])
        reader = self._reader("T-0B", "mandatory", "src/aief_exec/scope.py",
                              write_scope=["docs/**"])
        reasons = [r for r in graph.conflict_reasons(REPO, writer, reader, results={})
                   if graph.HZ_WRITE_READ in r]
        assert len(reasons) == 1, reasons
        assert "record" in reasons[0] and "mandatory" in reasons[0], reasons[0]
        classes = {c for c in (graph.HZ_WRITE_WRITE, graph.HZ_WRITE_READ,
                               graph.HZ_WRITE_OBSERVE)
                   if any(c in r for r in
                          graph.conflict_reasons(REPO, writer, reader, results={}))}
        assert graph.HZ_WRITE_READ in classes

    def test_the_live_contract_rewrite_pairs_are_no_longer_parallel(self):
        # H1, live and unconstructed. T-001 holds `.ai/project/tasks/**`, which
        # covers the contracts T-002 and T-005 are executing - their objective,
        # acceptance criteria, write scope, forbidden actions and budget - and
        # `classify` certified both pairs safe. X-08 charged T-002 931 TF-1 and
        # T-005 656 TF-1 for that exact file under `record`, so the layer knew.
        tasks = records.load_tasks(REPO)
        results = records.load_results(REPO)
        for other in ("T-002", "T-005"):
            reasons = graph.conflict_reasons(
                REPO, tasks["T-001"], tasks[other], results=results
            )
            assert reasons, other
            read = [r for r in reasons if graph.HZ_WRITE_READ in r]
            assert read, (other, reasons)
            assert f".ai/project/tasks/{other}.md" in read[0], read[0]
            assert "record" in read[0], read[0]

    def test_runtime_tooling_stays_undetected_and_is_disclosed(self):
        # E4, the residual this repair does NOT close, asserted as a residual so
        # that no reader mistakes the fix for a complete one and so that closing
        # it later has to come here and say so.
        #
        # T-002 writes `src/aief_stage6/**`, which holds `tokenizers.py` - the
        # backend every token figure T-004 reports flows through. No declared
        # surface of T-004 names it, because a task's imports are not a declared
        # scope, so the pair stays outside the write/read limb.
        tasks = records.load_tasks(REPO)
        results = records.load_results(REPO)
        surface = {rel for _, rel in graph.read_surface(REPO, tasks["T-004"], results)}
        assert not any(p.startswith("src/aief_stage6/") for p in surface), surface
        assert (REPO / "src/aief_stage6/tokenizers.py").is_file()
        # The limit is stated where a reader of the function will meet it.
        doc = graph.read_surface.__doc__ or ""
        assert "Runtime tooling" in doc or "runtime tooling" in doc.lower(), doc
        assert "tokenizers.py" in doc, doc

    def test_the_surface_carries_no_duplicate_paths(self):
        # Two anchored entries on one file are one file to a writer.
        task = _task("T-0B", read_scope={"mandatory": [
            {"path": "a.md", "anchor": "H"}, {"path": "a.md", "anchor": "I"},
        ]})
        rels = [rel for _, rel in graph.read_surface(REPO, task)]
        assert rels.count("a.md") == 1, rels


def _result_record(rid, deliverables):
    return records.ResultRecord(
        rid,
        f".ai/project/results/{rid}.md",
        {
            "result_id": rid,
            "status": "CURRENT",
            "deliverables": [{"path": p, "digest": "0" * 64} for p in deliverables],
        },
    )


class TestObservationSurface:
    """The third hazard class: what a task must observe stably, as opposed to
    what it reads as input or writes as output.

    `conflict_reasons` compared write against write and write against mandatory
    read. Neither sees a verifier that reproduces a producer's test suite: it
    reads none of the producer's files and writes none of them, and its evidence
    is still worthless if the suite moves while it runs.
    """

    def test_the_surface_starts_from_the_write_scope(self):
        task = _task("T-0A", write_scope=["src/aief_exec/**"])
        assert graph.observed_surface(REPO, task) == ["src/aief_exec/**"]

    def test_a_consumed_results_deliverables_enter_the_surface(self):
        # The term that catches the real incident. T-0B names no test file
        # anywhere; the result it consumes does, and those are exactly the paths
        # whose stability its conclusion depends on.
        task = _task("T-0B", write_scope=["docs/**"], consumes=["R-900"])
        results = {"R-900": _result_record("R-900", ["tests/test_exec_graph.py"])}
        surface = graph.observed_surface(REPO, task, results)
        assert "tests/test_exec_graph.py" in surface
        assert "docs/**" in surface

    def test_a_deliverable_that_resolves_today_enters_the_surface(self):
        task = _task("T-0C", write_scope=[], deliverable=["tests/test_exec_graph.py"])
        assert "tests/test_exec_graph.py" in graph.observed_surface(REPO, task)

    def test_a_prospective_deliverable_does_not(self):
        task = _task("T-0C", write_scope=[], deliverable=["not/written/yet.md"])
        assert graph.observed_surface(REPO, task) == []

    def test_a_declared_observes_extends_the_surface(self):
        bare = _task("T-0D", write_scope=["docs/**"])
        declared = _task("T-0D", write_scope=["docs/**"], observes=["tests/**"])
        assert graph.observed_surface(REPO, bare) == ["docs/**"]
        assert graph.observed_surface(REPO, declared) == ["docs/**", "tests/**"]

    def test_a_write_into_an_observed_surface_is_a_conflict(self):
        writer = _task("T-0A", write_scope=["tests/test_exec_*.py"])
        watcher = _task("T-0B", write_scope=["docs/**"], observes=["tests/**"])
        reasons = graph.conflict_reasons(REPO, writer, watcher, results={})
        assert reasons
        assert any(graph.HZ_WRITE_OBSERVE in r for r in reasons)
        assert any("evidence contamination" in r for r in reasons)
        # and the witness is named, not merely asserted
        assert any("tests/test_exec_graph.py" in r for r in reasons)

    def test_the_hazard_is_symmetric(self):
        # Argument order must not decide safety.
        writer = _task("T-0A", write_scope=["tests/test_exec_*.py"])
        watcher = _task("T-0B", write_scope=["docs/**"], observes=["tests/**"])
        forward = graph.conflict_reasons(REPO, writer, watcher, results={})
        reverse = graph.conflict_reasons(REPO, watcher, writer, results={})
        assert any(graph.HZ_WRITE_OBSERVE in r for r in forward)
        assert any(graph.HZ_WRITE_OBSERVE in r for r in reverse)
        # The same writer is named as the contaminating party either way round.
        assert all("T-0A writes inside T-0B" in r
                   for r in forward + reverse if graph.HZ_WRITE_OBSERVE in r)

    def test_the_three_hazard_classes_are_distinguishable_in_output(self):
        # One pair carrying all three at once. If the wordings collapsed, a
        # reader could not tell which hazard a CONFLICT verdict rested on.
        a = _task(
            "T-0A",
            write_scope=["src/aief_exec/records.py", "src/aief_exec/scope.py"],
        )
        b = _task(
            "T-0B",
            write_scope=["src/aief_exec/records.py"],
            read_scope={"mandatory": [{"path": "src/aief_exec/scope.py"}]},
            observes=["src/aief_exec/**"],
        )
        reasons = graph.conflict_reasons(REPO, a, b, results={})
        classes = {c for c in (graph.HZ_WRITE_WRITE, graph.HZ_WRITE_READ,
                               graph.HZ_WRITE_OBSERVE)
                   if any(c in r for r in reasons)}
        assert classes == {graph.HZ_WRITE_WRITE, graph.HZ_WRITE_READ,
                           graph.HZ_WRITE_OBSERVE}, reasons

    def test_two_independent_tasks_stay_parallel_and_say_why(self):
        a = _task("T-0A", write_scope=["src/aief_exec/**"])
        b = _task("T-0B", write_scope=["src/aief_stage6/**"])
        assert graph.conflict_reasons(REPO, a, b, results={}) == []
        lines = graph.safety_explanation(REPO, a, b, results={})
        # Not a bare verdict: five comparisons, each with both surfaces and an
        # explicit empty result.
        assert len(lines) == 5
        assert all("intersection EMPTY" in line for line in lines), lines
        for cls in (graph.HZ_WRITE_WRITE, graph.HZ_WRITE_READ, graph.HZ_WRITE_OBSERVE):
            assert any(line.startswith(cls) for line in lines), cls
        assert any("src/aief_exec/**" in line for line in lines)

    def test_the_explanation_reports_a_non_empty_intersection_as_such(self):
        a = _task("T-0A", write_scope=["tests/test_exec_*.py"])
        b = _task("T-0B", write_scope=["tests/test_exec_*.py"])
        lines = graph.safety_explanation(REPO, a, b, results={})
        assert any("intersects at" in line for line in lines)


class TestUndeclaredObservation:
    """The honest residual. An observation nobody declared stays invisible; the
    layer says so instead of implying coverage it does not have."""

    def _ac(self, test):
        return _task(
            "T-0A",
            write_scope=["docs/**"],
            acceptance_criteria=[{"id": "AC-1", "criterion": "c", "test": test}],
        )

    @pytest.mark.parametrize(
        "test", ["pytest tests/", "git status --porcelain", "git diff --stat",
                 "python -m aief_exec check exits 0"],
    )
    def test_each_tree_reading_token_raises_a_notice(self, test):
        notes = graph.undeclared_observation(self._ac(test))
        assert len(notes) == 1
        assert "may exceed what is declared" in notes[0]

    def test_the_notice_is_worded_as_a_limit_not_a_detection(self):
        note = graph.undeclared_observation(self._ac("pytest tests/"))[0]
        assert "Heuristic" in note
        assert "not recoverable from the repository" in note
        # It must not claim to have found the surface.
        assert "detected" not in note

    def test_prose_without_a_command_token_raises_nothing(self):
        assert graph.undeclared_observation(
            self._ac("The report carries one disposition row per criterion")
        ) == []

    def test_declaring_observes_silences_it(self):
        task = self._ac("pytest tests/")
        task.data["observes"] = ["tests/**"]
        assert graph.undeclared_observation(task) == []

    def test_it_fires_on_the_live_record_whose_evidence_is_english(self):
        # T-001's acceptance criteria name `pytest tests/`, `git status
        # --porcelain` and `python -m aief_exec check`, and its record declares
        # no `observes`. That surface is real and undeclared.
        notes = graph.undeclared_observation(records.load_tasks(REPO)["T-001"])
        assert notes
        assert any("pytest" in n for n in notes)
        assert any("git status" in n for n in notes)


class TestResultCurrency:
    def test_matching_digest_is_current(self, tmp_path):
        digest = records.file_dc1(REPO, ".ai/BOOT.md")
        r = records.ResultRecord(
            "R-900",
            "results/R-900.md",
            {
                "result_id": "R-900",
                "status": "CURRENT",
                "inputs": [{"path": ".ai/BOOT.md", "digest": digest}],
            },
        )
        assert graph.result_currency(REPO, r).status == "CURRENT"

    def test_drifted_digest_is_stale(self):
        r = records.ResultRecord(
            "R-901",
            "results/R-901.md",
            {
                "result_id": "R-901",
                "status": "CURRENT",
                "inputs": [{"path": ".ai/BOOT.md", "digest": "0" * 64}],
            },
        )
        curr = graph.result_currency(REPO, r)
        assert curr.status == "STALE" and curr.drifted

    def test_absent_input_is_stale(self):
        r = records.ResultRecord(
            "R-902",
            "results/R-902.md",
            {
                "result_id": "R-902",
                "status": "CURRENT",
                "inputs": [{"path": "gone.md", "digest": "0" * 64}],
            },
        )
        assert graph.result_currency(REPO, r).status == "STALE"

    def test_superseded_is_never_usable(self):
        r = records.ResultRecord(
            "R-903", "results/R-903.md",
            {"result_id": "R-903", "status": "SUPERSEDED", "inputs": []},
        )
        assert not graph.result_currency(REPO, r).usable


class TestSupersessionSeal:
    """VER-009 FIND-Q9-28. The guard this replaces fired on the record nobody
    touched and fell silent on the one that was rewritten; rewriting a digest on
    a scratch copy *removed* its notice. Every test here is written so that it
    fails against that behaviour and passes against a seal."""

    OLD = "# R-100\n\n```yaml\nresult_id: R-100\nstatus: SUPERSEDED\nsupersedes: null\ninputs:\n  - path: a.txt\n    digest: {d}\ndeliverables: []\nconclusion: |\n  c\n```\n"
    NEW = "# R-101\n\n```yaml\nresult_id: R-101\nstatus: CURRENT\nsupersedes: R-100\nsupersedes_seal:\n  path: .ai/project/results/R-100.md\n  digest: {seal}\ninputs: []\ndeliverables:\n  - path: a.txt\n    digest: {d}\nconclusion: |\n  c\n```\n"

    def _repo(self, tmp_path, tamper=None, seal=True):
        (tmp_path / ".ai/project/results").mkdir(parents=True)
        (tmp_path / "a.txt").write_text("input\n", encoding="utf-8")
        d = records.file_dc1(tmp_path, "a.txt")
        old = tmp_path / ".ai/project/results/R-100.md"
        old.write_text(self.OLD.format(d=d), encoding="utf-8")
        seal_digest = records.file_dc1(tmp_path, ".ai/project/results/R-100.md")
        body = self.NEW.format(seal=seal_digest if seal else "", d=d)
        if not seal:
            body = body.replace(
                "supersedes_seal:\n  path: .ai/project/results/R-100.md\n"
                "  digest: \n",
                "",
            )
        (tmp_path / ".ai/project/results/R-101.md").write_text(body, encoding="utf-8")
        if tamper:
            old.write_text(tamper(old.read_text(encoding="utf-8")), encoding="utf-8")
        return tmp_path

    def _currency(self, repo, rid="R-100"):
        results = records.load_results(repo)
        return graph.result_currency(repo, results[rid], results)

    def test_an_intact_sealed_record_is_quiet(self, tmp_path):
        curr = self._currency(self._repo(tmp_path))
        assert curr.status == "SUPERSEDED" and curr.drifted == []

    def test_rewriting_a_digest_after_supersession_fires(self, tmp_path):
        # The exact perturbation the auditor ran. Under the guard this replaces
        # it *silenced* the notice; here it raises one.
        repo = self._repo(tmp_path, tamper=lambda s: s.replace("digest: ", "digest: 0", 1))
        curr = self._currency(repo)
        assert curr.drifted and curr.drifted[0].startswith(graph.REWRITTEN)

    def test_the_guard_is_monotonic_under_arbitrary_tampering(self, tmp_path):
        # The property, not a case: no edit to a sealed superseded record can
        # reduce the alarm. Anti-monotonicity was the whole of FIND-Q9-28.
        # Every edit here is one DC-1 can see. The seal inherits DC-1's
        # boundary exactly: DC-1 normalises line endings, strips trailing
        # whitespace from every line and drops trailing blank lines before
        # hashing, so those are by the repository's own definition not changes
        # to content. Stated, not papered over - and asserted below.
        edits = [
            lambda s: s.replace("digest: ", "digest: 0", 1),
            lambda s: s.replace("status: SUPERSEDED", "status: CURRENT"),
            lambda s: s.replace("result_id: R-100", "result_id:  R-100"),
            lambda s: s.replace("  c\n", "  a different conclusion\n"),
            lambda s: s.replace("path: a.txt", "path: b.txt"),
        ]
        for i, edit in enumerate(edits):
            root = tmp_path / f"t{i}"
            root.mkdir()
            curr = self._currency(self._repo(root, tamper=edit))
            assert curr.drifted, f"edit {i} left the guard silent"
            assert curr.drifted[0].startswith(graph.REWRITTEN), curr.drifted

    def test_the_seals_blind_spot_is_exactly_dc1s(self, tmp_path):
        # The residual, named rather than left for an auditor to find: an edit
        # DC-1 normalises away does not move the seal. That is not a hole in the
        # seal, it is the repository's own definition of file content, and the
        # seal must not claim more resolution than the digest it is built on.
        # Line endings are left out deliberately: this host rewrites \n on
        # write, so a CRLF case would be testing the harness, not the seal.
        for i, edit in enumerate((
            lambda s: s + "\n\n",
            lambda s: s.replace("status: SUPERSEDED", "status: SUPERSEDED   "),
        )):
            root = tmp_path / f"b{i}"
            root.mkdir()
            assert self._currency(self._repo(root, tamper=edit)).drifted == []

    def test_an_unsealed_record_says_so_instead_of_guessing(self, tmp_path):
        curr = self._currency(self._repo(tmp_path, seal=False))
        assert curr.status == "SUPERSEDED"
        assert curr.drifted and "unsealed" in curr.drifted[0]

    def test_an_unsealed_record_is_never_accused(self, tmp_path):
        # R-001's six pins are inputs T-001 was forbidden to touch, so all of
        # them match the tree. The guard this replaces read that as evidence of
        # a rewrite. An absent control must report absence, not suspicion.
        curr = self._currency(self._repo(tmp_path, seal=False))
        assert not any(d.startswith(graph.REWRITTEN) for d in curr.drifted)

    def test_supersession_is_derived_from_the_successor(self, tmp_path):
        # A record still declaring CURRENT under a successor is superseded all
        # the same - the FIND-Q9-18 rule applied to results.
        repo = self._repo(tmp_path)
        p = repo / ".ai/project/results/R-100.md"
        p.write_text(
            p.read_text(encoding="utf-8").replace(
                "status: SUPERSEDED", "status: CURRENT"
            ),
            encoding="utf-8",
        )
        results = records.load_results(repo)
        assert graph.derived_status(results, results["R-100"]) == "SUPERSEDED"
        assert not graph.result_currency(repo, results["R-100"], results).usable


class TestPairClassOrdering:
    """`VER-009` FIND-Q9-41. `build_plan` evaluated CONFLICT before BLOCKED, so
    a pair that cannot be co-dispatched at all was reported as a scope hazard.

    The reorder is only lawful if nothing is lost by it, and that is what these
    assert: the reported class is the one that decides dispatchability, and the
    scope reasons survive inside it so the hazard is still readable and still
    there when the block clears.
    """

    def test_a_blocked_pair_reports_blocked_and_keeps_the_scope_reasons(self, tmp_path):
        from test_exec_checks import build_repo
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "write_scope": "  - out/shared/**"},
                {"tid": "T-002", "write_scope": "  - out/shared/**",
                 "blocked_by": "[OQ-14]", "status": "BLOCKED"},
            ],
        )
        plan = graph.build_plan(repo)
        kind, why = plan.pairs[("T-001", "T-002")]
        # The operative class: this pair cannot be dispatched, full stop.
        assert kind == graph.BLOCKED, (kind, why)
        assert any(r.startswith("[blocked/precondition]") for r in why), why
        # And the hazard is not discarded by saying so.
        assert any(graph.HZ_WRITE_WRITE in r for r in why), why

    def test_an_unblocked_conflicting_pair_still_reports_conflict(self, tmp_path):
        from test_exec_checks import build_repo
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "write_scope": "  - out/shared/**"},
                {"tid": "T-002", "write_scope": "  - out/shared/**"},
            ],
        )
        kind, why = graph.build_plan(repo).pairs[("T-001", "T-002")]
        assert kind == graph.CONFLICT, (kind, why)

    def test_a_complete_member_does_not_hide_a_live_scope_hazard(self):
        # COMPLETE is deliberately not folded into the blocked test. A COMPLETE
        # task cannot be dispatched either, but that state will never change, so
        # calling the pair BLOCKED would bury the hazard permanently. T-001 is
        # COMPLETE and holds `.ai/project/tasks/**`; the pair must read CONFLICT
        # so the reach over another task's contract stays visible.
        plan = graph.build_plan(REPO)
        assert plan.states["T-001"] == "COMPLETE"
        kind, why = plan.pairs[("T-001", "T-002")]
        assert kind == graph.CONFLICT, (kind, why)
        assert any(graph.HZ_WRITE_READ in r for r in why), why
        # No safety rests on this: COMPLETE tasks are outside every group.
        assert "T-001" not in plan.runnable()


class TestParallelSetsAreNotMaximal:
    """`VER-009` FIND-Q9-40. `parallel_sets` was documented as producing
    "Maximal groups". It is first-fit greedy in identifier order.

    The docstring was corrected rather than the algorithm - maximal grouping is
    maximum-clique-cover, NP-hard, and buys a larger batch rather than a safer
    one - so the tests are that the claim is accurate and that the safety
    property the claim was standing in for actually holds.
    """

    def _plan(self, tmp_path):
        # T-0A parallel with both others; T-0B and T-0C conflict with each
        # other. First-fit in identifier order puts A with B, which leaves C
        # alone in a group that A could have joined.
        from test_exec_checks import build_repo
        return graph.build_plan(build_repo(
            tmp_path,
            [
                {"tid": "T-001", "write_scope": "  - a/**"},
                {"tid": "T-002", "write_scope": "  - shared/**"},
                {"tid": "T-003", "write_scope": "  - shared/**"},
            ],
        ))

    def test_the_grouping_is_first_fit_and_a_group_is_not_maximal(self, tmp_path):
        plan = self._plan(tmp_path)
        groups = plan.parallel_sets()
        assert plan.pairs[("T-001", "T-002")][0] == graph.PARALLEL
        assert plan.pairs[("T-001", "T-003")][0] == graph.PARALLEL
        assert plan.pairs[("T-002", "T-003")][0] == graph.CONFLICT
        assert groups == [["T-001", "T-002"], ["T-003"]], groups
        # The demonstration: T-001 is pairwise PARALLEL with every member of the
        # second group, so that group could have contained it and does not.
        # "Maximal" is therefore false of this output.
        assert all(plan.pairs[tuple(sorted(("T-001", m)))][0] == graph.PARALLEL
                   for m in groups[1])

    def test_the_docstring_does_not_claim_more_than_the_algorithm(self):
        doc = graph.Plan.parallel_sets.__doc__ or ""
        # The overclaim, gone from the summary line - which is the line a
        # reader and every doc tool actually sees. "Maximal groups" was the
        # exact wording. The body may still quote it, and does, because a
        # correction that erases what it corrected teaches nobody.
        summary = doc.strip().splitlines()[0]
        assert "maximal" not in summary.lower(), summary
        # ... and the accurate claim, present, with the reason safety does not
        # rest on the difference.
        assert "first-fit" in doc.lower(), doc
        assert "not maximal" in doc.lower(), doc
        assert "X-07" in doc, doc

    def test_suboptimal_grouping_is_never_unsafe(self, tmp_path):
        # What the greedy pass costs is throughput. Every group it does form is
        # pairwise PARALLEL, which is the only property dispatch safety needs,
        # and X-07 re-verifies it from the plan independently.
        from aief_exec import checks
        from test_exec_checks import build_repo
        repo = build_repo(
            tmp_path,
            [
                {"tid": "T-001", "write_scope": "  - a/**"},
                {"tid": "T-002", "write_scope": "  - shared/**"},
                {"tid": "T-003", "write_scope": "  - shared/**"},
            ],
        )
        plan = graph.build_plan(repo)
        for group in plan.parallel_sets():
            for i, a in enumerate(group):
                for b in group[i + 1:]:
                    assert plan.pairs[tuple(sorted((a, b)))][0] == graph.PARALLEL
        assert checks.x07_no_concurrent_write_conflict(repo)["status"] == "PASS"


@pytest.fixture(scope="module")
def plan():
    return graph.build_plan(REPO)


class TestLivePlan:
    def test_graph_is_acyclic(self, plan):
        assert plan.cycles == []

    def test_independent_backlog_tasks_are_scope_independent(self, plan):
        # T-002 writes src/aief_stage6 and tests/test_stage6_*; T-004 writes a
        # verification report. Disjoint, no dependency either way.
        #
        # AC-4's property is scope independence, which is what is asserted; the
        # derived class is a fact about the day and has moved repeatedly. It was
        # PARALLEL; then BLOCKED because R-009 superseded R-008 and T-004 had not
        # been re-pointed; then BLOCKED again because the repair pass rewrote
        # `src/aief_exec/**`, which the consumed record pinned as its own
        # deliverables; and it is PARALLEL again now that R-011 is current and
        # T-004 consumes it. Naming any one of those causes was over-fitting to
        # one day. What is asserted here is the property plus the invariant
        # behind it: whatever blocks the pair, it is never a scope conflict.
        #
        # WHAT CHANGED: the R-008/R-009 clause is gone, replaced by an assertion
        # that any non-PARALLEL class is BLOCKED and rests on result currency,
        # not on any of the three scope hazards. The guarded branch names the
        # record T-004 actually consumes rather than a hard-coded id, so it
        # cannot go stale the way the prose above did.
        tasks = records.load_tasks(REPO)
        assert graph.conflict_reasons(REPO, tasks["T-002"], tasks["T-004"]) == []
        # Scope independence now covers the observation surface too: T-004's
        # surface includes everything its consumed result pins, and T-002 writes
        # none of it.
        surface = graph.observed_surface(
            REPO, tasks["T-004"], records.load_results(REPO)
        )
        assert any(p.startswith("src/aief_exec/") for p in surface), surface
        assert not any(p.startswith("src/aief_stage6/") for p in surface), surface
        kind, why = plan.pairs[("T-002", "T-004")]
        if kind != graph.PARALLEL:
            assert kind == graph.BLOCKED
            assert all(r.startswith("[blocked/precondition]") for r in why), why
            assert any(
                rid in r for r in why for rid in tasks["T-004"].consumes
            ), why

    def test_scope_independence_survives_a_blocked_task(self):
        # T-002 and T-003 are scope-independent; T-003 is blocked only because
        # qa-engineer is UNASSIGNED. Blocking is a state, not a scope conflict,
        # and the two must not be confused.
        tasks = records.load_tasks(REPO)
        assert graph.conflict_reasons(REPO, tasks["T-002"], tasks["T-003"]) == []

    def test_overlapping_test_scopes_conflict(self, plan):
        kind, why = plan.pairs[("T-002", "T-005")]
        assert kind == graph.CONFLICT
        assert any("write scopes intersect" in r for r in why)

    def test_dependent_pair_is_serial(self, plan):
        assert plan.pairs[("T-001", "T-004")][0] == graph.SERIAL

    def test_blocked_is_derived_not_declared(self, plan):
        # T-006 is blocked on three independent grounds, each derived from the
        # records rather than asserted in them.
        assert plan.states["T-006"] == graph.BLOCKED
        reasons = plan.blocked["T-006"]
        assert any("depends_on T-002" in r for r in reasons)
        assert any("R-002" in r for r in reasons)
        assert any("OQ-14" in r for r in reasons)

    def test_the_live_dependency_state_is_derived_end_to_end(self, plan):
        # T-004 depends on T-001 and consumes a result T-001 produced. Both ends
        # of that are derived, and nothing here is asserted by hand.
        #
        # WHAT CHANGED, and why. The previous form asserted the pre-closure
        # state unconditionally - R-009 STALE, T-004 BLOCKED - with a comment
        # saying it would "go red the moment R-009 is republished, which forces
        # the next state to be written down rather than inferred". It did, twice,
        # and this is that state written down.
        #
        # The chain: R-009 pinned `src/aief_exec/**` and `tests/test_exec_*.py`
        # as its own deliverables and the repair pass rewrote them, so R-009 went
        # STALE and T-004 derived BLOCKED. R-010 superseded R-009 with recomputed
        # digests and re-pointed T-004 in the same act. But R-010 pinned this
        # file too, so restating this very test staled R-010 - the fixed point
        # R-010 U-3 recorded and could not clear from either side alone. It is
        # cleared by one transaction: restate the tests first, then supersede
        # the record pinning them as restated. That ordering terminates, because
        # the tests are the last thing to change. R-011 did it once and R-012
        # does it again for the FIND-Q9-36..42 repair.
        #
        # WHAT CHANGED THIS TIME: the record ids are no longer written in. The
        # chain is walked - every SUPERSEDED record, and the one CURRENT one -
        # so the test asserts the *relation* rather than the day's identifiers,
        # and a fourth supersession is covered the moment it lands. That is the
        # drift R-011 U-5 records in the task records, met here at the source.
        #
        # WHY THIS STILL BITES. Nothing here is a bare status check. The whole
        # derivation is asserted - currency of the current record, the sealed
        # chain behind it, and the consumer state that falls out of both:
        #
        #   * touch `src/aief_exec/**` or `tests/test_exec_*.py` without
        #     republishing -> the current record STALE -> T-004 BLOCKED -> red;
        #   * edit any superseded ancestor -> the seal alarm fires in
        #     `drifted` -> red here;
        #   * re-point or hand-edit T-004's state -> the derived value is
        #     recomputed from currency and disagrees -> red here.
        assert plan.states["T-001"] == "COMPLETE"
        results = records.load_results(REPO)
        superseded = [rid for rid in sorted(results)
                      if graph.derived_status(results, results[rid]) == "SUPERSEDED"]
        current = [rid for rid in sorted(results)
                   if graph.derived_status(results, results[rid]) == "CURRENT"]
        assert len(current) == 1, current
        assert len(superseded) >= 5, superseded
        # Every superseded ancestor is closed and still matches the digest its
        # successor sealed, or is one of the two pre-epoch records that cannot
        # be sealed at all: SUPERSEDED, never STALE, and never REWRITTEN.
        for rid in superseded:
            curr = plan.currency[rid]
            assert curr.status == "SUPERSEDED", (rid, curr)
            assert not curr.usable, rid
            assert not any(d.startswith(graph.REWRITTEN) for d in curr.drifted), (
                rid, curr.drifted
            )
            _, sealed = graph.supersession_seal(results, rid)
            if sealed:
                assert curr.drifted == [], (rid, curr.drifted)
                assert sealed == records.file_dc1(REPO, results[rid].path), rid
            else:
                assert all("unsealed" in d for d in curr.drifted), (rid, curr.drifted)
        curr = plan.currency[current[0]]
        assert curr.status == "CURRENT", curr
        assert curr.usable
        assert curr.drifted == [], curr.drifted
        # The current record still pins the layer it describes, so the staling
        # relation that produced the old state is intact and simply satisfied.
        pinned = {e["path"] for e in results[current[0]].deliverables}
        assert any(p.startswith("src/aief_exec/") for p in pinned), pinned
        assert any(p.startswith("tests/test_exec_") for p in pinned), pinned
        assert results[current[0]].supersedes in superseded
        # T-004 consumes the current record and derives READY from it - the
        # state is read off currency, never off the task record.
        assert records.load_tasks(REPO)["T-004"].consumes == current
        assert plan.states["T-004"] == "READY"
        assert plan.blocked["T-004"] == [], plan.blocked["T-004"]

    def test_a_superseded_result_is_not_consumable(self, plan):
        assert plan.currency["R-001"].status == "SUPERSEDED"
        assert not plan.currency["R-001"].usable

    def test_the_superseding_result_pins_its_deliverables(self):
        # FIND-Q9-3: R-001 pinned only inputs, so its own outputs could move
        # under it undetected.
        results = records.load_results(REPO)
        assert len(results["R-008"].deliverables) >= 10
        assert results["R-001"].deliverables == []

    @pytest.mark.parametrize("rid", ["R-008", "R-009"])
    def test_the_current_result_pins_neither_its_consumer_nor_the_backlog(self, rid):
        # FIND-Q9-13: R-007 pinned VER-009, T-004's own deliverable, so T-004
        # filing its report staled the result it depended on.
        # FIND-Q9-14: it also pinned six mutable task records plus EXEC.md,
        # freezing the backlog.
        pinned = {e["path"] for e in records.load_results(REPO)[rid].deliverables}
        assert not any(p.startswith(".ai/project/verification/") for p in pinned)
        assert not any(p.startswith(".ai/project/tasks/") for p in pinned)
        assert ".ai/project/EXEC.md" not in pinned

    def test_the_live_record_seals_the_one_it_supersedes(self):
        # FIND-Q9-28: correction is by supersession, and until the successor
        # sealed the predecessor nothing recorded what the predecessor's bytes
        # were, so "retained unedited" was unverifiable.
        results = records.load_results(REPO)
        seal = results["R-009"].supersedes_seal
        assert results["R-009"].supersedes == "R-008"
        assert seal.get("path") == ".ai/project/results/R-008.md"
        assert len(str(seal.get("digest") or "")) == 64

    def test_open_item_blocks_stage_six(self, plan):
        assert plan.states["T-006"] == graph.BLOCKED
        assert any("OQ-14" in r for r in plan.blocked["T-006"])

    def test_dispatch_groups_are_internally_parallel(self, plan):
        for group in plan.parallel_sets():
            for i, a in enumerate(group):
                for b in group[i + 1:]:
                    assert plan.pairs[tuple(sorted((a, b)))][0] == graph.PARALLEL

    def test_conflicting_tasks_never_share_a_group(self, plan):
        groups = plan.parallel_sets()
        home = {t: i for i, g in enumerate(groups) for t in g}
        assert home["T-002"] != home["T-005"]
