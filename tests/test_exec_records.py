"""Record grammar: the restricted block parser, the bounded index and the
task/result records.

Actor provenance: software.software-engineer - S-2026-08-09-01.

Contract under test: `.ai/project/EXECUTION_ARCHITECTURE.md` sections 4, 5 and 6.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from aief_exec import records

REPO = Path(__file__).resolve().parents[1]


class TestBlockParser:
    def test_flat_mapping(self):
        got = records.parse_block("a: 1\nb: two\nc: null\nd: true\n")
        assert got == {"a": 1, "b": "two", "c": None, "d": True}

    def test_comments_are_stripped_outside_quotes(self):
        got = records.parse_block("a: 1   # trailing\n# whole line\nb: 'x # y'\n")
        assert got == {"a": 1, "b": "x # y"}

    def test_nested_mapping(self):
        got = records.parse_block("qa:\n  verifier_role: qa-engineer\n  report: p.md\n")
        assert got == {"qa": {"verifier_role": "qa-engineer", "report": "p.md"}}

    def test_block_sequence_of_scalars(self):
        got = records.parse_block("write_scope:\n  - src/**\n  - tests/*.py\n")
        assert got == {"write_scope": ["src/**", "tests/*.py"]}

    def test_block_sequence_of_mappings(self):
        text = (
            "mandatory:\n"
            "  - path: a.md\n"
            "    anchor: AMD-45\n"
            "  - path: b.md\n"
        )
        assert records.parse_block(text) == {
            "mandatory": [
                {"path": "a.md", "anchor": "AMD-45"},
                {"path": "b.md"},
            ]
        }

    def test_flow_sequence_and_mapping(self):
        got = records.parse_block("deps: [T-001, T-002]\nbudget: {tf1: 10, tf2: 20}\n")
        assert got == {"deps": ["T-001", "T-002"], "budget": {"tf1": 10, "tf2": 20}}

    def test_empty_flow_sequence(self):
        assert records.parse_block("deps: []\n") == {"deps": []}

    def test_literal_block_scalar(self):
        got = records.parse_block("conclusion: |\n  line one\n  line two\nnext: 1\n")
        assert got == {"conclusion": "line one\nline two\n", "next": 1}

    def test_leading_zero_tokens_stay_text(self):
        # An all-digit SHA-256 digest or a zero-padded id is an identifier, not
        # an integer. JSON's number grammar forbids leading zeros; so does this.
        got = records.parse_block(
            "digest: " + "0" * 64 + "\nseg: 0000\nseq: 0\ncap: 504\n"
        )
        assert got["digest"] == "0" * 64
        assert got["seg"] == "0000"
        assert got["seq"] == 0
        assert got["cap"] == 504

    def test_unparsable_line_raises_rather_than_guessing(self):
        # LAW-12: assumption is never a resolution method.
        with pytest.raises(records.RecordError):
            records.parse_block("this line has no colon\n")

    def test_bad_indent_raises(self):
        with pytest.raises(records.RecordError):
            records.parse_block("a: 1\n    b: 2\n")


class TestFence:
    def test_extracts_first_yaml_fence(self):
        md = "# T\n\n```yaml\na: 1\n```\n\ntext\n"
        assert records.extract_fence(md).strip() == "a: 1"

    def test_absent_fence_raises(self):
        with pytest.raises(records.RecordError):
            records.extract_fence("no fence here\n")


class TestIndexGrammar:
    def test_one_identifier_per_line(self):
        idx = records.parse_index("## Ready\n\nT-001\nT-002\n", "x")
        assert idx.sections["Ready"] == ["T-001", "T-002"]

    def test_trailing_text_after_identifiers_is_rejected(self):
        # AIEF-AMD-014 AMD-49 index_grammar: nothing else on that line.
        with pytest.raises(records.RecordError):
            records.parse_index("## Ready\n\nT-001\nT-002 and a note\n", "x")

    def test_preamble_prose_before_identifiers_is_allowed(self):
        idx = records.parse_index("## Ready\n\nsome preamble\n\nT-001\n", "x")
        assert idx.sections["Ready"] == ["T-001"]


class TestPublicationDerivations:
    """`produces` names a record; nothing computed where that record has to go.

    Until these existed the layer could not state, let alone check, that a task
    contracted to publish `R-002` had no write scope covering
    `.ai/project/results/R-002.md`. They are derivations only - see
    `TestX09PublicationReachability` for the check, and note that neither is
    enforced anywhere: open decision A4.
    """

    def _task(self, **kw):
        data = {"task_id": "T-0A", "produces": [], "write_scope": []}
        data.update(kw)
        return records.TaskRecord("T-0A", "tasks/T-0A.md", data)

    def test_result_paths_align_with_produces(self):
        task = self._task(produces=["R-002", "R-003"])
        assert task.result_paths == [
            ".ai/project/results/R-002.md",
            ".ai/project/results/R-003.md",
        ]

    def test_a_task_producing_nothing_derives_nothing(self):
        assert self._task().result_paths == []

    def test_effective_write_scope_is_the_union_and_preserves_declaration_order(self):
        task = self._task(produces=["R-002"], write_scope=["src/**"])
        assert task.effective_write_scope == ["src/**", ".ai/project/results/R-002.md"]
        # The declared scope is untouched - X-04 keeps testing that and only that.
        assert task.write_scope == ["src/**"]

    def test_an_already_covered_result_path_is_not_duplicated(self):
        task = self._task(
            produces=["R-002"], write_scope=[".ai/project/results/R-002.md"]
        )
        assert task.effective_write_scope == [".ai/project/results/R-002.md"]

    def test_a_glob_that_already_covers_the_result_path_closes_the_gap(self):
        # The union is over paths, not over pattern strings. T-001's shape.
        task = self._task(
            produces=["R-001", "R-007"], write_scope=[".ai/project/results/**"]
        )
        assert task.effective_write_scope == [".ai/project/results/**"]

    def test_observes_defaults_to_empty_and_is_never_required(self):
        assert self._task().observes == []
        assert "observes" not in records.SCH_TASK_REQUIRED
        assert "observes" not in records.EXTENSION_REQUIRED

    def test_observes_is_read_when_declared(self):
        assert self._task(observes=["tests/**", " docs/** "]).observes == [
            "tests/**",
            "docs/**",
        ]

    def test_the_live_gap_between_declared_and_effective_is_five_tasks(self):
        # The reproduced defect, at the level of the derivation: six live tasks
        # declare `produces` and five of them declare no write scope that reaches
        # the record they are contracted to publish.
        tasks = records.load_tasks(REPO)
        producers = [t for t in tasks.values() if t.produces]
        assert len(producers) == 6
        gapped = [
            t.task_id
            for t in producers
            if t.effective_write_scope != t.write_scope
        ]
        assert gapped == ["T-002", "T-003", "T-004", "T-005", "T-006"], gapped


class TestLiveRecords:
    def test_every_task_record_loads(self):
        tasks = records.load_tasks(REPO)
        assert set(tasks) == {"T-001", "T-002", "T-003", "T-004", "T-005", "T-006"}

    def test_index_and_records_are_bijective(self):
        idx = records.load_index(REPO)
        tasks = records.load_tasks(REPO)
        assert sorted(idx.ids) == sorted(tasks)

    def test_index_section_matches_record_status(self):
        idx = records.load_index(REPO)
        for tid, task in records.load_tasks(REPO).items():
            assert idx.state_of(tid) == task.status, tid

    def test_sch_task_required_fields_present(self):
        for tid, task in records.load_tasks(REPO).items():
            for field in records.SCH_TASK_REQUIRED:
                assert task.data.get(field) not in (None, "", [], {}), f"{tid}.{field}"

    def test_open_items_parses_and_excludes_closed(self):
        ids = records.open_item_ids(REPO)
        assert "OQ-14" in ids
        assert "OI-C-09" in ids
        # OQ-15 and CMP-BLOCK-006 are listed under Closed by AIEF-AMD-014.
        assert "OQ-15" not in ids
        assert "CMP-BLOCK-006" not in ids

    def test_dc1_of_a_known_file_is_stable(self):
        a = records.file_dc1(REPO, ".ai/BOOT.md")
        b = records.file_dc1(REPO, ".ai/BOOT.md")
        assert a == b and len(a) == 64 and a == a.lower()

    def test_dc1_of_absent_path_is_none(self):
        assert records.file_dc1(REPO, "does/not/exist.md") is None
