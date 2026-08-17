"""Read-scope resolution, path-set algebra and exact token cost.

Actor provenance: software.software-engineer - S-2026-08-09-01.

Contract under test: `.ai/project/EXECUTION_ARCHITECTURE.md` sections 5.1, 5.2, 7
and 11.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from aief_exec import records, scope

REPO = Path(__file__).resolve().parents[1]

# The exec layer measures token cost through the two normative tokenizer
# families, whose pinned artifacts live under `build/stage6/tokenizer_artifacts/`
# and are NOT tracked (they are third-party binaries under trust-on-first-use).
# Without them `Cost` is `measured=False` by design - "absence blocks, never
# estimates" - and a test that asserts on a measurement has nothing to assert on.
#
# These tests carried no guard until `S-2026-08-17-01`, so a fresh clone failed
# 35 of them rather than skipping them. Found by cloning the published
# repository and running the suite against it, which is the only check that sees
# what a stranger sees. Same guard as `tests/test_stage6_platform_tokenizers.py`.
_ARTIFACT_DIR = REPO / "build" / "stage6" / "tokenizer_artifacts"

needs_artifacts = pytest.mark.skipif(
    not (_ARTIFACT_DIR / "cl100k_base.tiktoken").is_file()
    or not (_ARTIFACT_DIR / "spiece.model").is_file(),
    reason="tokenizer artifacts not provisioned under build/stage6/ - see README",
)

AMD_013 = (
    "framework/AIEF-AMD-013_Boot_Budget_Determination_and_Stage_6_"
    "Build_Constructions.md"
)


class TestGlob:
    @pytest.mark.parametrize(
        "pattern,path,expected",
        [
            ("src/**", "src/a/b.py", True),
            ("src/**", "srcx/a.py", False),
            ("tests/test_stage6_*.py", "tests/test_stage6_digests.py", True),
            ("tests/test_stage6_*.py", "tests/test_exec_scope.py", False),
            ("tests/*.py", "tests/sub/a.py", False),
            ("**/*.md", "a/b/c.md", True),
        ],
    )
    def test_glob_to_regex(self, pattern, path, expected):
        assert bool(scope.glob_to_regex(pattern).match(path)) is expected

    def test_literal_prefix(self):
        assert scope.literal_prefix("tests/test_stage6_*.py") == "tests/test_stage6_"
        assert scope.literal_prefix("src/aief_exec/**") == "src/aief_exec/"
        assert scope.literal_prefix("a/b.md") == "a/b.md"


class TestPatternOverlap:
    def test_identical_patterns_overlap(self):
        assert scope.patterns_overlap("tests/t_*.py", "tests/t_*.py")

    def test_directory_prefix_overlaps(self):
        assert scope.patterns_overlap("src/**", "src/aief_exec/**")

    def test_wildcard_prefix_swallows_the_longer_literal(self):
        assert scope.patterns_overlap(
            "tests/test_stage6_*.py", "tests/test_stage6_certification_*.py"
        )

    def test_sibling_directories_do_not_overlap(self):
        assert not scope.patterns_overlap("src/aief_exec/**", "src/aief_stage6/**")

    def test_distinct_test_prefixes_do_not_overlap(self):
        assert not scope.patterns_overlap(
            "tests/test_stage6_*.py", "tests/test_exec_*.py"
        )

    def test_single_star_stays_inside_one_component(self):
        # `.ai/*.md` cannot reach `.ai/project/...`; a literal-prefix test said
        # it could, which is why the witness test replaced it.
        assert not scope.patterns_overlap(".ai/*.md", ".ai/project/EXEC.md")
        assert not scope.patterns_overlap(".ai/*.md", ".ai/project/tasks/**")
        assert scope.patterns_overlap(".ai/*.md", ".ai/BOOT.md")

    def test_two_double_stars_fall_back_to_the_safe_answer(self):
        # VER-009 FIND-Q9-24: `build/a/**` and `build/**/b` both match
        # `build/a/b`, yet neither pattern's witness satisfies the other. A
        # witness proves overlap; it cannot prove disjointness.
        assert scope.patterns_overlap("build/a/**", "build/**/b")
        assert scope.patterns_overlap("src/**", "src/aief_exec/**")
        # Nesting is still required - siblings stay disjoint.
        assert not scope.patterns_overlap("src/aief_exec/**", "src/aief_stage6/**")

    #: VER-009 FIND-Q9-29. The nine probes pass 4 ran against the witness form.
    #: Five reported disjoint while genuinely intersecting - error in the unsafe
    #: direction, in the primitive that decides concurrent-write safety. Each
    #: intersecting pair is given here with the concrete path that witnesses it,
    #: so the assertion is checkable by inspection and by `glob_to_regex`.
    PROBES = [
        ("src/aief_exec/*_new.py", "src/aief_exec/new_*.py",
         "src/aief_exec/new__new.py"),
        ("tests/test_*_records.py", "tests/test_exec_*.py",
         "tests/test_exec_records.py"),
        ("build/*a*.json", "build/*b*.json", "build/ab.json"),
        ("build/x/T-00?.md", "build/x/T-0?1.md", "build/x/T-001.md"),
        ("build/**/gen_*.py", "build/gen/*_gen.py", "build/gen/gen__gen.py"),
        ("build/a/**", "build/**/b", "build/a/b"),
    ]

    @pytest.mark.parametrize("a,b,witness", PROBES)
    def test_the_five_unsafe_false_negatives_are_gone(self, a, b, witness):
        assert scope.glob_to_regex(a).match(witness), "witness is wrong for a"
        assert scope.glob_to_regex(b).match(witness), "witness is wrong for b"
        assert scope.patterns_overlap(a, b)
        assert scope.patterns_overlap(b, a)

    @pytest.mark.parametrize(
        "a,b",
        [
            (".ai/*.md", ".ai/project/EXEC.md"),
            (".ai/*.md", ".ai/project/tasks/**"),
            ("src/aief_exec/**", "src/aief_stage6/**"),
            ("tests/test_stage6_*.py", "tests/test_exec_*.py"),
            ("a/?.md", "a/bb.md"),
            ("a/*/b", "a/b"),
        ],
    )
    def test_genuinely_disjoint_pairs_stay_disjoint(self, a, b):
        # Exactness cuts both ways: the answer must not become "always true".
        assert not scope.patterns_overlap(a, b)
        assert not scope.patterns_overlap(b, a)

    def test_the_decision_matches_brute_force_on_a_generated_corpus(self):
        # The property behind the two tests above. Every pattern pair drawn from
        # a small alphabet is decided against an exhaustive search of the paths
        # they could name: no false negative, and no false positive either.
        import itertools

        atoms = ["a", "b", "/", "*", "?", "**/", "**"]
        pats = [
            "".join(c)
            for n in (2, 3)
            for c in itertools.product(atoms, repeat=n)
        ]
        pats = [p for p in pats if not p.startswith("/") and "//" not in p][:220]
        universe = [
            "".join(c)
            for n in range(1, 5)
            for c in itertools.product("ab/", repeat=n)
        ]
        universe = [u for u in universe if "//" not in u and not u.endswith("/")]
        rx = {p: scope.glob_to_regex(p) for p in pats}
        checked = disagreements = 0
        for a in pats[:60]:
            for b in pats[:60]:
                truth = any(rx[a].match(u) and rx[b].match(u) for u in universe)
                if truth and not scope.patterns_overlap(a, b):
                    disagreements += 1        # unsafe: a real overlap missed
                checked += 1
        assert disagreements == 0, f"{disagreements} of {checked} pairs under-report"


class TestScopesIntersect:
    def test_disjoint_scopes(self):
        assert not scope.scopes_intersect(
            REPO, ["src/aief_exec/**"], ["src/aief_stage6/**"]
        )

    def test_overlapping_scopes_return_a_concrete_witness(self):
        hit = scope.scopes_intersect(
            REPO, ["tests/test_stage6_*.py"], ["tests/test_stage6_certification_*.py"]
        )
        assert isinstance(hit, set) and hit

    def test_empty_scope_never_intersects(self):
        assert not scope.scopes_intersect(REPO, [], ["src/**"])


class TestAnchorResolution:
    def test_heading_anchor_returns_only_that_section(self):
        text = (REPO / AMD_013).read_text(encoding="utf-8")
        got = scope.resolve_heading(text, "AMD-45")
        assert got.startswith("## AMD-45")
        assert "## AMD-46" not in got
        assert "## AMD-44" not in got

    @needs_artifacts
    def test_heading_anchor_is_far_smaller_than_the_file(self):
        whole = (REPO / AMD_013).read_text(encoding="utf-8")
        part = scope.resolve_heading(whole, "AMD-45")
        assert scope.cost(part).tf1 < scope.cost(whole).tf1 / 10

    def test_row_anchor_returns_one_row_with_its_header(self):
        text = (REPO / ".ai/project/OPEN_ITEMS_REGISTER.md").read_text(encoding="utf-8")
        got = scope.resolve_row(text, "OI-C-09")
        assert got is not None
        rows = [ln for ln in got.strip().split("\n") if ln.startswith("|")]
        assert sum(1 for r in rows if r.split("|")[1].strip() == "OI-C-09") == 1
        assert "OI-C-08" not in got

    def test_json_anchor_returns_the_subtree(self):
        entry = {
            "path": "framework/framework.manifest.json",
            "anchor": "metadata.reproducible.bounded_register_split",
        }
        got = scope.resolve_entry(REPO, entry)
        assert '"index": "open-items"' in got
        assert "digest_constructions" not in got

    def test_missing_anchor_raises_rather_than_falling_back_to_the_file(self):
        with pytest.raises(scope.ScopeError):
            scope.resolve_entry(REPO, {"path": AMD_013, "anchor": "AMD-999"})

    def test_absent_path_raises(self):
        with pytest.raises(scope.ScopeError):
            scope.resolve_entry(REPO, {"path": "no/such/file.md"})

    def test_no_anchor_resolves_to_the_whole_file(self):
        got = scope.resolve_entry(REPO, {"path": ".ai/BOOT.md"})
        assert got == (REPO / ".ai/BOOT.md").read_text(encoding="utf-8")


class TestCost:
    @needs_artifacts
    def test_both_declared_families_are_available(self):
        pr = scope.probe()
        assert pr.available, pr.missing
        assert {f.family_id for f in pr.families} == {"TF-1", "TF-2"}

    @needs_artifacts
    def test_counts_are_exact_and_never_estimated(self):
        c = scope.cost("hello world")
        assert c.measured and c.tf1 > 0 and c.tf2 > 0

    def test_cost_is_additive(self):
        assert (scope.Cost(1, 2) + scope.Cost(3, 4)) == scope.Cost(4, 6)

    def test_unmeasured_propagates(self):
        assert not (scope.Cost(1, None) + scope.Cost(1, 1)).measured


class TestResolvedScope:
    @needs_artifacts
    def test_anchoring_reduces_the_mandatory_scope_materially(self):
        task = records.load_tasks(REPO)["T-002"]
        rs = scope.resolve_scope(REPO, task, "mandatory")
        assert not rs.errors
        assert rs.total.measured and rs.whole_file_total.measured
        # The claim the architecture rests on.
        assert rs.total.tf1 < rs.whole_file_total.tf1 / 5
        assert rs.total.tf2 < rs.whole_file_total.tf2 / 5

    @needs_artifacts
    def test_resolved_scope_is_within_declared_budget(self):
        for tid, task in records.load_tasks(REPO).items():
            budget = task.data.get("context_budget") or {}
            rs = scope.resolve_scope(REPO, task, "mandatory")
            assert not rs.errors, (tid, rs.errors)
            assert rs.total.tf1 <= budget["tf1"], tid
            assert rs.total.tf2 <= budget["tf2"], tid

    def test_an_entry_is_opened_once(self, tmp_path):
        # VER-009 FIND-Q9-33. The old shape returned cost without text, so
        # `brief` re-resolved every entry to print it and `resolve_scope` read
        # each file again for the unanchored comparison: three opens per entry.
        import builtins
        task = records.load_tasks(REPO)["T-002"]
        events = []
        real_open, real_rt = builtins.open, Path.read_text
        builtins.open = lambda f, *a, **k: (events.append(str(f)), real_open(f, *a, **k))[1]
        Path.read_text = lambda self, *a, **k: (events.append(str(self)), real_rt(self, *a, **k))[1]
        try:
            rs = scope.resolve_scope(REPO, task, "mandatory", whole=False)
        finally:
            builtins.open, Path.read_text = real_open, real_rt
        for ex in rs.entries:
            hits = [e for e in events if e.replace("\\", "/").endswith(ex.path)]
            assert len(hits) == 1, (ex.path, len(hits))
            # and the text came back with the cost, so nothing need re-open it
            assert ex.text and scope.cost(ex.text) == ex.cost


class TestChargedContext:
    """VER-009 FIND-Q9-35. The budget must count what a task holds, not what it
    reads first."""

    @needs_artifacts
    def test_an_existing_deliverable_is_charged(self):
        task = records.load_tasks(REPO)["T-004"]
        results = records.load_results(REPO)
        cc = scope.charged_context(REPO, task, results)
        # T-004's deliverable is VER-009, which its own AC-4 makes unavoidable
        # and which the superseded measurement omitted entirely.
        assert cc.component_total("deliverable").tf1 > 10000
        assert cc.total.tf1 > 3 * cc.read_only_total.tf1

    def test_the_task_record_itself_is_charged(self):
        task = records.load_tasks(REPO)["T-004"]
        cc = scope.charged_context(REPO, task, records.load_results(REPO))
        assert cc.component_total("record").tf1 == scope.cost(
            (REPO / task.path).read_text(encoding="utf-8")
        ).tf1

    def test_a_consumed_result_is_charged_whole(self):
        task = records.load_tasks(REPO)["T-004"]
        results = records.load_results(REPO)
        cc = scope.charged_context(REPO, task, results)
        rid = task.consumes[0]
        assert cc.component_total("dependency").tf1 == scope.cost(
            (REPO / results[rid].path).read_text(encoding="utf-8")
        ).tf1

    @needs_artifacts
    def test_a_prospective_deliverable_costs_nothing_and_is_declared(self, tmp_path):
        # Hermetic on purpose. This was first written against T-005's declared
        # deliverable and a concurrent session created that file mid-run, which
        # is the same self-reference FIND-Q9-35 is about, met from the other
        # side: a test whose fixture is the live tree measures the day.
        (tmp_path / "task.md").write_text("contract\n", encoding="utf-8")
        task = records.TaskRecord("T-0Y", "task.md", {
            "task_id": "T-0Y",
            "deliverable": ["not/created/yet.py"],
            "read_scope": {"mandatory": []},
            "write_scope": [],
            "consumes": [],
        })
        resolved, unresolved = scope.deliverable_paths(tmp_path, task)
        assert unresolved == ["not/created/yet.py"] and resolved == []
        cc = scope.charged_context(tmp_path, task, {})
        assert cc.component_total("deliverable") == scope.ZERO
        # Not charged is not the same as not mentioned - the omission is stated.
        assert any("charged nothing" in n for n in cc.notices)

        # ... and the moment the file exists, it is charged.
        (tmp_path / "not/created").mkdir(parents=True)
        (tmp_path / "not/created/yet.py").write_text("x = 1\n" * 50, encoding="utf-8")
        cc = scope.charged_context(tmp_path, task, {})
        assert cc.component_total("deliverable").tf1 > 0

    def test_prose_is_never_guessed_into_a_path(self):
        # LAW-12. `src/aief_stage6/budget.py with the deferral keyed on ...`
        # begins with a real path; taking the first token would be an assumption
        # about a sentence, so the entry resolves to nothing and says so.
        task = records.load_tasks(REPO)["T-002"]
        resolved, unresolved = scope.deliverable_paths(REPO, task)
        assert resolved == []
        assert len(unresolved) == 3

    def test_nothing_is_charged_twice(self, tmp_path):
        # A path that is both read and delivered is one file, charged once, at
        # whole-file granularity.
        (tmp_path / "d").mkdir()
        (tmp_path / "d/f.md").write_text("## H\n\nbody\n\n## I\n\nmore\n", encoding="utf-8")
        (tmp_path / "d/task.md").write_text("contract\n", encoding="utf-8")
        task = records.TaskRecord("T-0X", "d/task.md", {
            "task_id": "T-0X",
            "deliverable": ["d/f.md"],
            "read_scope": {"mandatory": [{"path": "d/f.md", "anchor": "H"}]},
            "write_scope": [],
            "consumes": [],
        })
        cc = scope.charged_context(tmp_path, task, {})
        whole = scope.cost((tmp_path / "d/f.md").read_text(encoding="utf-8"))
        record = scope.cost((tmp_path / "d/task.md").read_text(encoding="utf-8"))
        assert cc.total == record + whole
        assert [k for k, _, _ in cc.components] == ["record", "deliverable"]

    def test_a_self_referential_budget_is_reported(self):
        # The second limb of FIND-Q9-35: a charged path inside the task's own
        # write scope makes the figure move as the task works. Nothing recorded
        # that before; something must.
        #
        # WHAT CHANGED, and why - VER-009 FIND-Q9-36b. The two assertions that
        # stood here required the notice to end "this is why `revision` ... is
        # reported and `acquisition` ... is the gated quantity". That sentence
        # is a non-sequitur and the auditor said so: it offers `acquisition`,
        # the number that carries the movement for T-001 and T-002, as the cure
        # for the movement. Requiring it in a test is requiring the falsehood.
        #
        # What is required instead is strictly more: the notice must name the
        # component each moving path actually sits in, and must report the
        # gate's own stable/self-referential split. A notice that attributes
        # every moving path to `revision` fails this test.
        task = records.load_tasks(REPO)["T-004"]
        cc = scope.charged_context(REPO, task, records.load_results(REPO))
        note = [n for n in cc.notices if "self-referential budget" in n]
        assert note, cc.notices
        assert cc.non_monotonic
        # The component is named, and it is the one that actually holds the path.
        where = dict((rel, kind) for kind, rel in cc.moving_by_component())
        assert where, cc.components
        for rel, kind in where.items():
            assert f"{kind} {rel}" in note[0], (rel, kind, note[0])
        # The gate's own split is stated, so a reader is told how much of the
        # gated figure the task can move rather than being pointed at revision.
        assert "DISPATCH-TIME" in note[0], note[0]
        assert str(cc.acquisition_self_referential) in note[0], note[0]
        assert str(cc.acquisition_stable) in note[0], note[0]


class TestBudgetSplit:
    """One number cannot gate a dispatch when part of it only exists after the
    dispatch.

    The FIND-Q9-35 repair charged deliverables that already resolve, which is
    correct as a measurement and wrong as a gate: `T-005` charged TF-1 1,411
    against a cap of 1,500 before it ran and 7,161 after, the whole difference
    being the deliverable it had just written. Every test here is written so that
    it fails against a single summed charge and passes against the split.
    """

    def _task(self, root, deliverable="out/report.md", write_scope=("out/**",)):
        (root / "d").mkdir(parents=True, exist_ok=True)
        (root / "d/task.md").write_text("contract text\n" * 5, encoding="utf-8")
        (root / "d/input.md").write_text("## H\n\ninput body\n", encoding="utf-8")
        return records.TaskRecord("T-0Z", "d/task.md", {
            "task_id": "T-0Z",
            "deliverable": [deliverable],
            "read_scope": {"mandatory": [{"path": "d/input.md"}]},
            "write_scope": list(write_scope),
            "consumes": [],
        })

    def _write_deliverable(self, root, rel="out/report.md"):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# Report\n\n" + ("body that must be read to be rewritten. " * 300),
                     encoding="utf-8")

    @needs_artifacts
    def test_acquisition_is_invariant_to_whether_the_deliverable_exists(self, tmp_path):
        # The T-005 non-monotonicity, measured directly: the same task, the same
        # record, the same read scope, once before its deliverable exists and
        # once after.
        task = self._task(tmp_path)
        before = scope.charged_context(tmp_path, task, {})
        self._write_deliverable(tmp_path)
        after = scope.charged_context(tmp_path, task, {})

        assert before.acquisition.measured and before.acquisition.tf1 > 0
        assert after.acquisition == before.acquisition, (
            f"acquisition moved from {before.acquisition} to {after.acquisition} - "
            f"a gate whose verdict depends on whether the task already ran"
        )
        # The old single figure did move, which is the defect this pins.
        assert after.total != before.total
        assert before.revision == scope.ZERO
        assert after.revision.tf1 > 0

    def test_revision_is_flagged_non_monotonic_inside_the_own_write_scope(self, tmp_path):
        task = self._task(tmp_path)
        self._write_deliverable(tmp_path)
        cc = scope.charged_context(tmp_path, task, {})
        assert cc.non_monotonic == ["out/report.md"]
        assert any("self-referential" in n for n in cc.notices)

    @needs_artifacts
    def test_a_deliverable_outside_the_write_scope_is_revision_but_monotonic(self, tmp_path):
        # Revision is still not gated - it is not a precondition - but it does
        # not move under the task's own hand, and the two facts are separate.
        task = self._task(tmp_path, write_scope=("elsewhere/**",))
        self._write_deliverable(tmp_path)
        cc = scope.charged_context(tmp_path, task, {})
        assert cc.revision.tf1 > 0
        assert cc.non_monotonic == []

    def test_acquisition_is_exactly_its_four_components(self, tmp_path):
        task = self._task(tmp_path)
        self._write_deliverable(tmp_path)
        cc = scope.charged_context(tmp_path, task, {})
        want = scope.ZERO
        for name in scope.ACQUISITION_COMPONENTS:
            want = want + cc.component_total(name)
        assert cc.acquisition == want
        assert cc.revision == cc.component_total("deliverable")
        assert cc.total == cc.acquisition + cc.revision
        assert set(scope.ACQUISITION_COMPONENTS).isdisjoint(scope.REVISION_COMPONENTS)

    @needs_artifacts
    def test_telemetry_is_unmeasurable_not_zero(self, tmp_path):
        # The distinction is the whole content of the field. Zero would be a
        # claim; UNMEASURED is the truth, and the repository holds no execution
        # trace from which to improve on it.
        cc = scope.charged_context(tmp_path, self._task(tmp_path), {})
        assert cc.telemetry != scope.ZERO
        assert not cc.telemetry.measured
        assert cc.telemetry.tf1 is None and cc.telemetry.tf2 is None
        assert "UNMEASURABLE" in cc.telemetry_note
        assert "will not estimate" in cc.telemetry_note
        # and it is never folded into a reported figure
        assert cc.total == cc.acquisition + cc.revision
        assert cc.total.measured
        assert any("telemetry" in n for n in cc.notices)

    @needs_artifacts
    def test_the_live_t005_shape_reproduces_the_incident(self):
        # The task the defect was found on. Its deliverable now exists, so the
        # summed charge is over its cap while the gated quantity is under it.
        task = records.load_tasks(REPO)["T-005"]
        cc = scope.charged_context(REPO, task, records.load_results(REPO))
        cap = task.data["context_budget"]["tf1"]
        assert cc.revision.tf1 > 0, "T-005's deliverable is on disk"
        assert cc.total.tf1 > cap, "the summed charge is over the cap"
        assert cc.acquisition.tf1 <= cap, (
            f"acquisition {cc.acquisition.tf1} against cap {cap}"
        )
        assert cc.non_monotonic == ["tests/test_stage6_crash_trials.py"]


class TestAcquisitionIsNotInvariant:
    """`VER-009` FIND-Q9-36. The gated quantity moves under the task's own hand,
    and the artefacts that said otherwise said so in the reader's first stop.

    `TestBudgetSplit` above establishes the property the split was built for -
    `acquisition` does not move when the task's *deliverable* is created - and
    its fixture puts the task record at `d/task.md` outside `write_scope=out/**`,
    which is the one configuration in which the gate is invariant. That is
    correctly scoped to its own title and is not weakened here. What no test
    asserted, and what made the defect invisible to a green suite, is the
    broader claim `scope.py` and `EXECUTION_ARCHITECTURE.md` both made: that
    `acquisition` is stable across the task's own execution. It is not, because
    `record` is an acquisition component and every AIEF task must update its own
    checkpoint as it works.

    Every test here fails against a model that reports one undifferentiated
    `acquisition` figure, and against a notice that attributes the movement to
    `revision`.
    """

    def _task(self, root, write_scope=(".ai/project/tasks/**",)):
        (root / ".ai/project/tasks").mkdir(parents=True, exist_ok=True)
        (root / "in").mkdir(parents=True, exist_ok=True)
        (root / ".ai/project/tasks/T-0W.md").write_text(
            "contract text\n" * 20, encoding="utf-8"
        )
        (root / "in/stable.md").write_text("## H\n\nstable input\n" * 5, encoding="utf-8")
        return records.TaskRecord("T-0W", ".ai/project/tasks/T-0W.md", {
            "task_id": "T-0W",
            "deliverable": [],
            "read_scope": {"mandatory": [{"path": "in/stable.md"}]},
            "write_scope": list(write_scope),
            "consumes": [],
        })

    @needs_artifacts
    def test_the_gate_moves_when_the_task_appends_to_its_own_checkpoint(self, tmp_path):
        # The auditor's synthetic case, reproduced: 542 -> 1,328 TF-1, +145%,
        # from one progress note appended to the record the task is required to
        # keep. Nothing but the task's own lawful work happened between the two
        # measurements.
        task = self._task(tmp_path)
        before = scope.charged_context(tmp_path, task, {})
        p = tmp_path / ".ai/project/tasks/T-0W.md"
        p.write_text(
            p.read_text(encoding="utf-8") + ("progress note written as it works\n" * 40),
            encoding="utf-8",
        )
        after = scope.charged_context(tmp_path, task, {})
        assert after.acquisition.tf1 > before.acquisition.tf1, (
            "the gated quantity did not move when the task edited its own "
            "record - the fixture no longer reproduces FIND-Q9-36"
        )
        # The part that moved is exactly the self-referential part; the stable
        # part did not move at all. That is the split doing its work.
        assert after.acquisition_stable == before.acquisition_stable
        assert (after.acquisition_self_referential.tf1
                > before.acquisition_self_referential.tf1)

    @needs_artifacts
    def test_the_gate_is_split_into_stable_and_self_referential(self, tmp_path):
        task = self._task(tmp_path)
        cc = scope.charged_context(tmp_path, task, {})
        # Both figures are visible, and they reconstruct the gate exactly.
        assert cc.acquisition_stable + cc.acquisition_self_referential == cc.acquisition
        # The record is inside the write scope, so it is the moving part ...
        assert cc.acquisition_self_referential == cc.component_total("record")
        # ... and the declared input is outside it, so it is the stable part.
        assert cc.acquisition_stable == cc.component_total("mandatory")
        assert cc.acquisition_self_referential.tf1 > 0

    def test_a_record_outside_the_write_scope_leaves_the_gate_stable(self, tmp_path):
        # The control. Self-reference is a property of the declarations, not of
        # the component: move the record out of the write scope and the same
        # component becomes stable.
        task = self._task(tmp_path, write_scope=("out/**",))
        cc = scope.charged_context(tmp_path, task, {})
        assert cc.acquisition_self_referential == scope.ZERO
        assert cc.acquisition_stable == cc.acquisition
        assert cc.moving_by_component() == []

    def test_the_moving_paths_are_attributed_to_the_right_component(self, tmp_path):
        # FIND-Q9-36b. The emitted notice named `revision` for T-002, whose
        # revision is zero and both of whose moving paths are in `mandatory`.
        task = self._task(tmp_path, write_scope=("in/**",))
        cc = scope.charged_context(tmp_path, task, {})
        assert cc.moving_by_component() == [("mandatory", "in/stable.md")]
        assert cc.revision == scope.ZERO
        note = [n for n in cc.notices if "self-referential budget" in n]
        assert note, cc.notices
        assert "mandatory in/stable.md" in note[0], note[0]

    @needs_artifacts
    def test_the_live_t002_movement_is_not_in_revision(self):
        # The live case the finding turned on, asserted on the live record: 24%
        # of a figure X-08 currently FAILS on is self-written, and every moving
        # path is in `acquisition`, not `revision`.
        task = records.load_tasks(REPO)["T-002"]
        cc = scope.charged_context(REPO, task, records.load_results(REPO))
        assert cc.revision == scope.ZERO
        assert cc.non_monotonic, "T-002 writes src/aief_stage6/**, which it reads"
        assert all(kind != "deliverable" for kind, _ in cc.moving_by_component())
        assert cc.acquisition_self_referential.tf1 > 0
        assert cc.acquisition_self_referential.tf1 < cc.acquisition.tf1

    @needs_artifacts
    def test_the_record_component_is_not_dropped_to_buy_invariance(self):
        # The repair that must not be taken. An agent cannot execute a contract
        # it has not read, so the record stays charged and the movement stays
        # disclosed. A model that removed `record` from the gate would make the
        # figure invariant and the measurement false.
        assert "record" in scope.ACQUISITION_COMPONENTS
        task = records.load_tasks(REPO)["T-004"]
        cc = scope.charged_context(REPO, task, records.load_results(REPO))
        assert cc.component_total("record").tf1 > 0

    @needs_artifacts
    def test_total_measurable_is_named_and_equals_the_two_measured_parts(self):
        # FIND-Q9-37: what the gate excludes must have a name and a number, not
        # a footnote. 53% of T-004's measurable input is excluded from the gate.
        task = records.load_tasks(REPO)["T-004"]
        cc = scope.charged_context(REPO, task, records.load_results(REPO))
        assert cc.total_measurable == cc.acquisition + cc.revision
        assert cc.total_measurable == cc.total
        excluded = cc.revision.tf1 / cc.total_measurable.tf1
        assert excluded > 0.5, f"T-004's excluded share is {excluded:.0%}"


class TestSharedReadAndDeliverablePathIsCharedToRevision:
    """`VER-009` FIND-Q9-49, MAJOR - the gate's headline property, made structural.

    `TestBudgetSplit` measures that `acquisition` does not move when a task
    creates its own deliverable, and that measurement was true of this tree and
    **not** of the model. Deduplication kept the first unit on a path and
    acquisition units are built first, so a path declared as both a read entry
    and a deliverable was charged into `acquisition` and never reached
    `revision`. The audit built the counter-example and measured it: a task
    declaring `deliverable: [out/shared.md]` and `optional: [out/shared.md]`
    went `X-08` FAIL -> PASS on creating that file, `acquisition` 251 -> 855,
    `revision` 0 throughout; at a cap of 400, `acquisition` 249 -> 853, +243%.

    The overlap is empty for all six live tasks, which is the only reason the
    invariance measurement held. Nothing asserted the overlap was empty and no
    check reported one. These tests assert the property instead of the tree.

    The declaration is lawful - a task that revises a file it must also consult
    is ordinary - so the repair is an accounting rule, not a prohibition.
    """

    def _task(self, root, shared="out/shared.md", kind="optional"):
        (root / "d").mkdir(parents=True, exist_ok=True)
        (root / "d/task.md").write_text("contract text\n" * 5, encoding="utf-8")
        (root / "d/input.md").write_text("## H\n\ninput body\n", encoding="utf-8")
        return records.TaskRecord("T-0Q", "d/task.md", {
            "task_id": "T-0Q",
            "deliverable": [shared],
            "read_scope": {
                "mandatory": [{"path": "d/input.md"}],
                kind: [{"path": shared}],
            },
            "write_scope": ["out/**"],
            "consumes": [],
        })

    def _create(self, root, rel="out/shared.md"):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            "# Shared\n\n" + ("body that must be read to be rewritten. " * 300),
            encoding="utf-8",
        )

    @pytest.mark.parametrize("kind", ["mandatory", "optional"])
    @needs_artifacts
    def test_the_gate_does_not_move_when_the_task_creates_the_shared_path(
        self, tmp_path, kind
    ):
        """The counter-example, run. `acquisition` is the gated quantity and it
        is identical before and after the task creates its own output."""
        task = self._task(tmp_path, kind=kind)
        before = scope.charged_context(tmp_path, task, {})
        self._create(tmp_path)
        after = scope.charged_context(tmp_path, task, {})
        assert after.acquisition == before.acquisition, (
            f"acquisition moved from {before.acquisition} to "
            f"{after.acquisition} on a path the task declares as both a read "
            f"entry and a deliverable - FIND-Q9-49"
        )
        assert before.revision == scope.ZERO
        assert after.revision.tf1 > 0

    def test_the_shared_path_is_charged_to_revision_not_acquisition(self, tmp_path):
        task = self._task(tmp_path)
        self._create(tmp_path)
        cc = scope.charged_context(tmp_path, task, {})
        charged = [(k, p) for k, p, _ in cc.components if p == "out/shared.md"]
        assert charged == [("deliverable", "out/shared.md")], cc.components

    @needs_artifacts
    def test_it_is_charged_exactly_once_and_the_total_is_unchanged(self, tmp_path):
        """The repair moves a cost between named quantities. It must not create,
        destroy or duplicate one - `total_measurable`, and therefore `X-10`, is
        unaffected to the token."""
        task = self._task(tmp_path)
        self._create(tmp_path)
        cc = scope.charged_context(tmp_path, task, {})
        paths = [p for _, p, _ in cc.components]
        assert paths.count("out/shared.md") == 1, cc.components
        assert cc.total_measurable == cc.acquisition + cc.revision
        assert cc.total_measurable.tf1 == sum(c.tf1 for _, _, c in cc.components)

    def test_a_declared_overlap_is_reported_and_never_silent(self, tmp_path):
        """FIND-Q9-49's second limb: nothing asserted the overlap was empty and
        no check reported one when it was not."""
        task = self._task(tmp_path)
        self._create(tmp_path)
        cc = scope.charged_context(tmp_path, task, {})
        assert any("FIND-Q9-49" in n and "out/shared.md" in n for n in cc.notices), (
            cc.notices
        )

    def test_no_overlap_emits_no_notice(self, tmp_path):
        task = self._task(tmp_path)
        task.data["read_scope"]["optional"] = [{"path": "d/input.md"}]
        self._create(tmp_path)
        cc = scope.charged_context(tmp_path, task, {})
        assert not any("FIND-Q9-49" in n for n in cc.notices), cc.notices

    def test_an_anchored_read_on_a_deliverable_path_is_also_revision(self, tmp_path):
        """The anchored case already behaved correctly, because a whole-file
        unit subsumes an anchored one on the same path and deliverables are
        whole. Pinned so the two rules cannot drift apart."""
        (tmp_path / "d").mkdir(parents=True, exist_ok=True)
        (tmp_path / "d/task.md").write_text("contract\n" * 5, encoding="utf-8")
        self._create(tmp_path)
        (tmp_path / "out/shared.md").write_text(
            "## H\n\nsection body\n\n## I\n\nmore\n", encoding="utf-8"
        )
        task = records.TaskRecord("T-0Q", "d/task.md", {
            "task_id": "T-0Q",
            "deliverable": ["out/shared.md"],
            "read_scope": {"mandatory": [{"path": "out/shared.md", "anchor": "H"}]},
            "write_scope": ["out/**"],
            "consumes": [],
        })
        cc = scope.charged_context(tmp_path, task, {})
        charged = [(k, p) for k, p, _ in cc.components if p.startswith("out/shared")]
        assert charged == [("deliverable", "out/shared.md")], cc.components

    def test_the_hazard_model_still_sees_the_path(self, tmp_path):
        """FIND-Q9-38 must not regress. The cost model charges the path to
        `revision`; `acquisition_units` - which `graph.read_surface` reads - is
        the enumeration of what the task must *hold*, and the path is still in
        it, so a writer of that path is still a `write/read` hazard."""
        task = self._task(tmp_path)
        self._create(tmp_path)
        surface = {p for _, p, _ in scope.acquisition_units(task, {})}
        assert "out/shared.md" in surface

    def test_the_live_tree_has_no_overlap_and_says_so(self):
        """The audit's own finding: the overlap is empty for all six live tasks.
        Recorded as a measurement of this tree, not as a property of the model -
        which is the distinction FIND-Q9-49 was raised about."""
        results = records.load_results(REPO)
        for task in records.load_tasks(REPO).values():
            cc = scope.charged_context(REPO, task, results)
            assert not any("FIND-Q9-49" in n for n in cc.notices), task.task_id


class TestAcquisitionSurfaceIsOneDeclaration:
    """`VER-009` FIND-Q9-44. The component set was declared twice and untied.

    `acquisition_units` hardcoded `record`, a literal `("mandatory","optional")`
    loop and a `dependency` loop, while `ChargedContext.acquisition` summed the
    separate constant `ACQUISITION_COMPONENTS`. Nothing asserted the two agreed.
    Mutant MU14 - `telemetry` appended to the constant, and nowhere else -
    **survived the whole suite**: charged nowhere, compared nowhere, invisible.
    The symmetric mutation, a kind emitted under a name in neither constant, was
    caught only incidentally, by the `total == acquisition + revision`
    cross-check.

    There is one declaration now, `ACQUISITION_EMITTERS`, and
    `ACQUISITION_COMPONENTS` is its key order. Every test here fails against a
    model that lets the two drift, in either direction.
    """

    def _task(self, root):
        """A task exercising all four components at once."""
        (root / ".ai/project/tasks").mkdir(parents=True, exist_ok=True)
        (root / ".ai/project/results").mkdir(parents=True, exist_ok=True)
        (root / "in").mkdir(parents=True, exist_ok=True)
        (root / ".ai/project/tasks/T-0A.md").write_text("contract\n" * 8, "utf-8")
        (root / "in/m.md").write_text("mandatory\n" * 8, encoding="utf-8")
        (root / "in/o.md").write_text("optional\n" * 8, encoding="utf-8")
        (root / ".ai/project/results/R-900.md").write_text("result\n" * 8, "utf-8")
        (root / "out").mkdir(parents=True, exist_ok=True)
        (root / "out/d.md").write_text("deliverable\n" * 8, encoding="utf-8")
        task = records.TaskRecord("T-0A", ".ai/project/tasks/T-0A.md", {
            "task_id": "T-0A",
            "deliverable": ["out/d.md"],
            "read_scope": {
                "mandatory": [{"path": "in/m.md"}],
                "optional": [{"path": "in/o.md"}],
            },
            "write_scope": ["out/**"],
            "consumes": ["R-900"],
            "context_budget": {"tf1": 90000, "tf2": 90000},
        })
        results = {"R-900": records.ResultRecord(
            "R-900", ".ai/project/results/R-900.md", {"result_id": "R-900"}
        )}
        return task, results

    def test_every_declared_component_is_actually_emitted(self, tmp_path):
        # The direction MU14 escaped through. A name in the set that the
        # enumeration never emits is a component that is charged nowhere and
        # compared nowhere, and the suite could not see it.
        task, results = self._task(tmp_path)
        emitted = {kind for kind, _, _ in scope.acquisition_units(task, results)}
        assert emitted == set(scope.ACQUISITION_COMPONENTS), (
            emitted.symmetric_difference(set(scope.ACQUISITION_COMPONENTS))
        )

    def test_no_emitted_kind_falls_outside_the_declared_set(self, tmp_path):
        # The symmetric direction. A kind emitted under a name the set does not
        # contain is charged into no component, so `acquisition` silently
        # under-counts.
        task, results = self._task(tmp_path)
        for kind, _, _ in scope.acquisition_units(task, results):
            assert kind in scope.ACQUISITION_COMPONENTS, kind

    def test_the_set_and_the_emitters_are_the_same_declaration(self):
        # Structural, not behavioural: the two cannot be edited apart, because
        # there is only one of them. This is what makes the two tests above
        # assertions about the model rather than about a fixture.
        assert scope.ACQUISITION_COMPONENTS == tuple(scope.ACQUISITION_EMITTERS)
        assert set(scope.ACQUISITION_COMPONENTS) == set(scope.ACQUISITION_EMITTERS)

    def test_a_component_added_to_the_set_alone_cannot_go_uncharged(
        self, tmp_path, monkeypatch
    ):
        # MU14, run as a test rather than as a mutation campaign. Adding
        # `telemetry` to the declared set without an emitter used to be
        # invisible: charged nowhere, compared nowhere, and the whole suite
        # green. It is now a hard error naming the component, which `run_all`
        # surfaces as an ERROR row rather than a quiet under-count.
        task, results = self._task(tmp_path)
        monkeypatch.setattr(
            scope, "ACQUISITION_COMPONENTS",
            scope.ACQUISITION_COMPONENTS + ("telemetry",),
        )
        with pytest.raises(scope.ScopeError) as exc:
            scope.acquisition_units(task, results)
        assert "telemetry" in str(exc.value)
        assert "charged nowhere" in str(exc.value)

    @needs_artifacts
    def test_the_charge_accounts_for_every_declared_component(self, tmp_path):
        # The consequence that matters: the gate is the sum over the declared
        # set, so a declared component that emits nothing quietly contributes
        # zero and no total moves. Every component must carry real cost here.
        task, results = self._task(tmp_path)
        cc = scope.charged_context(tmp_path, task, results)
        for name in scope.ACQUISITION_COMPONENTS:
            assert cc.component_total(name).tf1 > 0, name
        summed = scope.ZERO
        for name in scope.ACQUISITION_COMPONENTS:
            summed = summed + cc.component_total(name)
        assert summed == cc.acquisition
        assert cc.total == cc.acquisition + cc.revision

    def test_both_models_read_the_one_enumeration(self, tmp_path):
        # FIND-Q9-38's property, re-asserted against the new structure: the
        # hazard model compares exactly the paths the cost model charges.
        from aief_exec import graph
        task, results = self._task(tmp_path)
        charged = {rel for _, rel, _ in scope.acquisition_units(task, results)}
        compared = {rel for _, rel in graph.read_surface(tmp_path, task, results)}
        assert charged <= compared, charged - compared


class TestArchitectureCitations:
    """`VER-009` FIND-Q9-48. A citation printed to the operator must resolve.

    `graph.seal_epoch`'s docstring and the `X-06` notice both cited the epoch to
    `EXECUTION_ARCHITECTURE.md` §6.1, which is *Immutability without new
    machinery*. The epoch is §6.2. The wrong pointer was emitted in exactly the
    case the notice exists to report - a disagreement between the constant and
    the records, which is the tamper signature.

    These tests read the architecture document, so they fail if either the
    citation or the section numbering moves.
    """

    ARCH = ".ai/project/EXECUTION_ARCHITECTURE.md"

    def _section(self, number):
        text = (REPO / self.ARCH).read_text(encoding="utf-8")
        head = f"### {number} "
        assert head in text, number
        body = text.split(head, 1)[1]
        return head + body.split("\n### ", 1)[0]

    def test_the_epoch_is_recorded_in_the_section_the_code_cites(self):
        from aief_exec import graph
        assert "section 6.2" in (graph.seal_epoch.__doc__ or "")
        assert "section 6.1" not in (graph.seal_epoch.__doc__ or "")
        section = self._section("6.2")
        assert graph.SEAL_EPOCH in section, section[:200]
        assert "seal epoch" in section.lower()

    def test_the_cited_section_is_not_the_neighbouring_one(self):
        # The specific error: §6.1 is about immutability and does not record the
        # constant, so a reader sent there finds nothing.
        from aief_exec import graph
        assert graph.SEAL_EPOCH not in self._section("6.1")

    def test_the_x06_notice_cites_the_same_section(self, tmp_path):
        # The notice is emitted only when the derivation and the constant
        # disagree, which is why the wrong citation survived: it is invisible on
        # a clean tree. Forced here.
        from aief_exec import checks, graph
        (tmp_path / ".ai/project/results").mkdir(parents=True)
        (tmp_path / ".ai/project/tasks").mkdir(parents=True)
        (tmp_path / ".ai/project/EXEC.md").write_text("# Execution Index\n", "utf-8")
        row = checks.x06_result_currency(tmp_path)
        note = [n for n in row["notices"] if n.startswith("seal epoch:")]
        assert note, row["notices"]
        assert "section 6.2" in note[0], note[0]
        assert "section 6.1" not in note[0], note[0]
        assert graph.SEAL_EPOCH in note[0]
