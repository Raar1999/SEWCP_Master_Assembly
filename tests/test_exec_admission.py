"""The record admission invariant.

Actor provenance: software.software-engineer - S-2026-08-09-14.

THE INVARIANT
-------------
    A record is admitted only if it is UNAMBIGUOUS and STRUCTURALLY
    WELL-FORMED. Anything else is rejected by name. Nothing is reinterpreted,
    defaulted, tie-broken or coerced on the way in.

OWNER: `src/aief_exec/records.py`. The module's own docstring has always claimed
it - *"raises `RecordError` on anything outside that subset rather than guessing
- LAW-12: assumption is never a resolution method"* - and until `VER-012` it did
not enforce it. Ownership was nominal, so the obligation fell to every consumer,
and every consumer discharged it differently.

WHY THIS FILE EXISTS
--------------------
Five successive audits found the same defect at five depths of one value:

    two link definitions          -> one deleted line disarmed the seal
    seal path not matching        -> silently no link
    declared path -> ""           -> indistinguishable from "no path"
    non-mapping block -> {}       -> indistinguishable from "no block"
    duplicate key / tab / fence   -> silently one of two readings

Each repair added a distinguishing predicate at ONE interpretation site. The
number of sites is unbounded, so the next audit picked another. Four of the five
were found in code the previous repair had just written.

The common mechanism is exact: **an input that is present but uninterpretable is
coerced onto the same value as absent, and absent is a passing state.** These
tests pin the invariant that removes the mechanism rather than any one of its
manifestations, which is why they live in their own module and are written
against `records.py` rather than against `X-06`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from aief_exec import records

REPO = Path(__file__).resolve().parents[1]

DOC = (
    "```yaml\n"
    "result_id:   R-100\n"
    "status:      CURRENT\n"
    "{body}"
    "inputs:      []\n"
    "deliverables: []\n"
    "conclusion: |\n"
    "  c\n"
    "```\n"
)


def parse(body=""):
    return records.parse_block(records.extract_fence(DOC.format(body=body)))


class TestAmbiguityIsRejectedNotResolved:
    """L5-A, L5-B, L5-E. Each was a *tie-break*: the parser had two readings and
    silently returned one. A tie-break is an assumption, and LAW-12 forbids
    assumption as a resolution method."""

    def test_a_duplicate_top_level_key_is_rejected(self):
        with pytest.raises(records.RecordError, match="duplicate key 'status'"):
            parse("status:      SUPERSEDED\n")

    def test_a_duplicate_nested_key_is_rejected(self):
        with pytest.raises(records.RecordError, match="duplicate key 'digest'"):
            parse("supersedes_seal:\n  path:   p\n  digest: a\n  digest: b\n")

    def test_last_wins_is_not_the_answer(self):
        """The specific behaviour that made L5-A silent: appending a second
        block carrying a tampered digest overrode the first, and the file still
        displayed the correct digest to a human reader. A reader of the file and
        a reader of the parse disagreed, and nothing said so."""
        with pytest.raises(records.RecordError) as e:
            parse("supersedes_seal:\n  path:   p\n  digest: GOOD\n"
                  "supersedes_seal:\n  path:   p\n  digest: TAMPERED\n")
        assert "undefined" in str(e.value)

    @pytest.mark.parametrize(
        "ws",
        [
            "\t",        # U+0009  L5-B
            "\v",        # U+000B  L6-3
            "\f",        # U+000C  L6-3
            "\u00a0",    # NBSP - invisible, a routine copy-paste artifact
            "\u2007",    # figure space
            "\u200b",    # zero-width space
            "\ufeff",    # BOM
        ],
    )
    def test_non_space_indentation_is_rejected(self, ws):
        """`VER-013` L6-3. The first form of this rule rejected `\\t` alone, so
        every other whitespace character survived `lstrip(" ")`, yielded indent
        0, and reproduced L5-B's exact parse - `{'a': None, 'b': 1}`, child
        hoisted to top level and parent key silently emptied.

        None of these has a defined width in this grammar, so none has a correct
        depth to return; and rejecting one character of a class is the
        enumeration error the whole repair exists to stop.
        """
        with pytest.raises(records.RecordError, match="is not the space"):
            records.parse_block("a:\n" + ws + " b: 1\n")

    def test_mixed_space_then_non_space_is_rejected(self):
        with pytest.raises(records.RecordError, match="is not the space"):
            records.parse_block("a:\n  \tb: 1\n")

    def test_ordinary_space_indentation_is_still_accepted(self):
        assert records.parse_block("a:\n  b: 1\n") == {"a": {"b": 1}}

    @pytest.mark.parametrize(
        "body",
        [
            "s: {p: 1, p: 2}\n",                       # flow mapping      L6-1
            "s: {a: {c: 1, c: 2}}\n",                  # nested flow map   L6-1
            "d:\n    - path: a\n      path: b\n",      # sequence item     L6-2
            "d:\n    - {path: a, path: b}\n",          # flow map in a seq L6-2
            "s: 1\n's': 2\n",                          # quoted vs bare    L6-4
        ],
    )
    def test_a_duplicate_key_in_any_construction_site_is_rejected(self, body):
        """`VER-013` L6-1, L6-2, L6-4 - the enumeration error, one level up.

        The first form of the duplicate-key guard was installed in `_parse_map`
        alone, leaving three other mapping-construction sites resolving by
        last-wins in silence. The flow mapping is the sharpest: it is the syntax
        `test_a_lawful_flow_mapping_is_accepted` certifies as the control, and a
        duplicate `digest:` inside it rewrote a superseded record at `X-06 PASS`
        for **one edit in one file** - the cheapest attack in the whole history.

        Every construction path routes through `records.put` now, so a fourth
        path cannot be added without passing the guard.
        """
        with pytest.raises(records.RecordError, match="duplicate key"):
            records.parse_block(body)

    def test_two_yaml_fences_are_rejected(self):
        with pytest.raises(records.RecordError, match="2 ```yaml blocks"):
            records.extract_fence(DOC.format(body="") + DOC.format(body=""))

    def test_one_fence_is_still_read(self):
        assert parse()["result_id"] == "R-100"


class TestShapeIsValidatedAtAdmission:
    """The coercion sites. `dict(v) if isinstance(v, dict) else {}` and
    `[e for e in ... if isinstance(e, dict)]` both map *malformed* onto
    *absent*. Coercion is not wrong in an accessor; it is wrong as the only
    reading. `validate_shape` makes it never load-bearing."""

    @staticmethod
    def _rec(**data):
        data.setdefault("result_id", "R-100")
        return records.ResultRecord("R-100", "x.md", data)

    @pytest.mark.parametrize("bad", [["a"], "text", 12345, True])
    def test_a_seal_that_is_not_a_mapping_is_rejected(self, bad):
        with pytest.raises(records.RecordError, match="supersedes_seal is"):
            self._rec(supersedes_seal=bad).validate_shape()

    @pytest.mark.parametrize("field", ["inputs", "deliverables"])
    def test_a_malformed_pin_entry_is_rejected_not_dropped(self, field):
        """It used to vanish from the pinned set without a word, which silently
        shrinks the set of digests X-06 compares."""
        with pytest.raises(records.RecordError, match=rf"{field}\[1\] is str"):
            self._rec(**{field: [{"path": "a", "digest": "d"}, "oops"]}).validate_shape()

    def test_produced_by_must_be_a_mapping(self):
        with pytest.raises(records.RecordError, match="produced_by is list"):
            self._rec(produced_by=[{"task": "T-001"}]).validate_shape()

    def test_absent_is_still_absent(self):
        """The converse, so the rule cannot be satisfied by rejecting
        everything. R-001, R-007 and R-008 carry no seal block at all."""
        self._rec().validate_shape()
        self._rec(supersedes_seal=None, inputs=None).validate_shape()

    def test_a_lawful_flow_mapping_is_accepted(self):
        """The invariant is about ambiguity, not spelling. `{k: v}` is in the
        declared grammar and names exactly one reading, so it is admitted."""
        d = parse("supersedes_seal: {path: p, digest: d}\n")
        assert d["supersedes_seal"] == {"path": "p", "digest": "d"}
        records.ResultRecord("R-100", "x.md", d).validate_shape()


class TestAdmissionIsOnTheSupportedPath:
    def test_load_results_validates(self, tmp_path):
        (tmp_path / ".ai/project/results").mkdir(parents=True)
        (tmp_path / ".ai/project/results/R-100.md").write_text(
            DOC.format(body="supersedes_seal:\n    - path: p\n"), encoding="utf-8"
        )
        with pytest.raises(records.RecordError, match="not a mapping"):
            records.load_results(tmp_path)

    def test_the_live_records_are_admitted(self):
        """Migration evidence, asserted rather than assumed: the stricter rule
        rejects nothing that already exists."""
        loaded = records.load_results(REPO)
        assert len(loaded) >= 8
        for rid, rec in loaded.items():
            rec.validate_shape()
            assert rec.result_id == rid

    def test_the_live_task_records_and_index_still_parse(self):
        """The parser is shared. Tightening it for results must not break the
        task records or the bounded index, which use the same grammar."""
        assert len(records.load_tasks(REPO)) >= 6
        assert records.load_index(REPO).ids

    def test_task_records_are_admitted_through_the_same_gate(self):
        """`VER-013` L6-6. The result record got an admission gate and the task
        record did not, so `read_entries` kept the coercion pattern
        `validate_shape` was written to retire. On the live `T-001`, replacing
        one `- path:` mapping with a bare scalar dropped it silently - `X-01`
        and `X-03` both PASS - and moved `acquisition`, which is the quantity
        the `X-08` dispatch gate is a function of."""
        bad = records.TaskRecord("T-900", "x.md", {
            "read_scope": {"mandatory": [{"path": "a"}, "oops"]},
        })
        # The malformed *entry* is inside a mapping value, so it is the
        # read-scope reader's business; what admission owns is the shape of the
        # declared fields themselves.
        records.TaskRecord("T-901", "x.md", {"write_scope": ["a"]}).validate_shape()
        for field, value in (
            ("write_scope", "not-a-list"),
            ("read_scope", ["mandatory"]),
            ("acceptance_criteria", [{"id": "AC-1"}, "oops"]),
            ("consumes", "R-001"),
            ("status", {"READY": True}),
        ):
            with pytest.raises(records.RecordError, match=field):
                records.TaskRecord("T-902", "x.md", {field: value}).validate_shape()
        assert bad.data["read_scope"]["mandatory"][1] == "oops"

    def test_a_string_is_not_a_sequence(self):
        """The dangerous coercion specifically: a bare string is iterable, so a
        consumer reads `write_scope: not-a-list` as ten one-character glob
        patterns rather than as an error."""
        with pytest.raises(records.RecordError, match="write_scope is str"):
            records.TaskRecord("T-903", "x.md", {"write_scope": "src/**"}).validate_shape()
