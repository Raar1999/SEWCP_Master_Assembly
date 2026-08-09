"""Negative security suite for the supersession link.

Actor provenance: software.software-engineer - S-2026-08-09-13.

`VER-009` FIND-Q9-51 and FIND-Q9-52. The pass-7 audit recorded four working
disarms of the supersession control across two passes and gave one structural
diagnosis for all of them:

    `successor_of` is the single point of truth for "is there a successor", it
    is derived from one editable field, and every seal comparison hangs off it.
    Nothing derives the link from the seal itself.

`graph.link_of` is the repair - one definition, reading both fields - and this
file is its adversary. Every test here attacks the repaired mechanism; none
asserts that ordinary operation still works, which the rest of the suite covers.

Mutant `MU30` - deleting the seal-path limb - survived the pass-6 suite because
nothing exercised seal-path corroboration at all. The tests below fail if that
limb is removed, which is precisely the coverage whose absence MU30 proved.

The chain is three deep on purpose. FIND-Q9-52 established that the **interior**
link is the invisible one: attacking the head left at least one red test
elsewhere, while attacking an interior link left no signal in check, campaign or
suite. Every attack that can be run on both is run on both.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from aief_exec import checks, graph, records

REPO = Path(__file__).resolve().parents[1]

BODY = (
    "# {rid}\n\n"
    "```yaml\n"
    "result_id:   {rid}\n"
    "produced_by:\n"
    "  task:      T-001\n"
    "  role:      software.software-engineer\n"
    "  session:   S-2026-08-09-12\n"
    "status:      {status}\n"
    "{links}"
    "inputs:      []\n"
    "{deliverables}"
    "conclusion: |\n"
    "  c\n"
    "```\n"
)


def _write(repo, rid, status, links, deliverables=""):
    (repo / f".ai/project/results/{rid}.md").write_text(
        BODY.format(
            rid=rid,
            status=status,
            links=links,
            deliverables=deliverables or "deliverables: []\n",
        ),
        encoding="utf-8",
    )
    return records.file_dc1(repo, f".ai/project/results/{rid}.md")


def chain(root):
    """`R-100 <- R-101 <- R-102`, every link declared twice and sealed.

    Sessions are `S-2026-08-09-12`, at or after `graph.SEAL_EPOCH`, so a missing
    seal here is a present-tense omission and not history - the discriminator
    EXECUTION_ARCHITECTURE.md section 6.2 draws, and the one that keeps `R-001`
    and `R-007` reported rather than accused.
    """
    root.mkdir(parents=True, exist_ok=True)
    (root / ".ai/project/results").mkdir(parents=True)
    (root / "a.txt").write_text("deliverable\n", encoding="utf-8")
    d = records.file_dc1(root, "a.txt")
    seal_100 = _write(root, "R-100", "SUPERSEDED", "superseded_by: R-101\n")
    seal_101 = _write(
        root,
        "R-101",
        "SUPERSEDED",
        "superseded_by: R-102\n"
        "supersedes:  R-100\n"
        "supersedes_seal:\n"
        "  path:   .ai/project/results/R-100.md\n"
        f"  digest: {seal_100}\n",
    )
    _write(
        root,
        "R-102",
        "CURRENT",
        "supersedes:  R-101\n"
        "supersedes_seal:\n"
        "  path:   .ai/project/results/R-101.md\n"
        f"  digest: {seal_101}\n",
        deliverables=f"deliverables:\n    - path: a.txt\n      digest: {d}\n",
    )
    return root


@pytest.fixture
def repo(tmp_path):
    return chain(tmp_path / "repo")


def x06(repo):
    return checks.x06_result_currency(repo)


def edit(repo, rid, old, new=""):
    p = repo / f".ai/project/results/{rid}.md"
    body = p.read_text(encoding="utf-8")
    assert old in body, (rid, old)
    p.write_text(body.replace(old, new, 1), encoding="utf-8")


def drop_seal(repo, rid, pred):
    """Remove the whole `supersedes_seal` block, digest line included."""
    body = (repo / f".ai/project/results/{rid}.md").read_text(encoding="utf-8")
    digest = [ln for ln in body.splitlines() if ln.startswith("  digest: ")][0]
    edit(repo, rid, "supersedes_seal:\n")
    edit(repo, rid, f"  path:   .ai/project/results/{pred}.md\n")
    edit(repo, rid, digest + "\n")


def append(repo, rid, text="\nTAMPERED: appended after supersession.\n"):
    p = repo / f".ai/project/results/{rid}.md"
    p.write_text(p.read_text(encoding="utf-8") + text, encoding="utf-8")


def reseal(repo, successor, predecessor):
    """What a tamperer editing the chain must do anyway - FIND-Q9-52's step 2.

    The control has to catch the tamper, not the tamperer's bookkeeping.
    """
    fresh = records.file_dc1(repo, f".ai/project/results/{predecessor}.md")
    body = (repo / f".ai/project/results/{successor}.md").read_text(encoding="utf-8")
    digest = [ln for ln in body.splitlines() if ln.startswith("  digest: ")][0]
    edit(repo, successor, digest, f"  digest: {fresh}")


def fails_naming(repo, *needles):
    res = x06(repo)
    blob = " ".join(res["details"])
    assert res["status"] == "FAIL", res
    for n in needles:
        assert n in blob, (n, res["details"])
    return res


class TestTheChainIsSoundBeforeAnyAttack:
    def test_the_unattacked_chain_passes(self, repo):
        res = x06(repo)
        assert res["status"] == "PASS", res["details"]

    def test_both_representations_are_read_and_agree(self, repo):
        results = records.load_results(repo)
        for rid, pred in (("R-101", "R-100"), ("R-102", "R-101")):
            link = graph.link_of(results[rid])
            assert link.declared == pred and link.sealed == pred, (rid, link)
            assert not link.divergent and link.target == pred
            assert graph.is_successor_link(results[rid], pred)


class TestM1DeleteSuccessorOf:
    """M1 - delete the field `successor_of` used to be built from.

    FIND-Q9-51's one-line disarm. Before the repair this returned `""` from
    `successor_of`, `result_currency` took the *unsealed* branch, and the digest
    that would convict the tamperer sat in `R-013.supersedes_seal.digest` with no
    code path comparing it.
    """

    @pytest.mark.parametrize("head,pred", [("R-102", "R-101"), ("R-101", "R-100")])
    def test_deleting_supersedes_does_not_orphan_the_seal(self, repo, head, pred):
        edit(repo, head, f"supersedes:  {pred}\n")
        results = records.load_results(repo)
        assert graph.successor_of(results, pred) == head
        assert graph.supersession_seal(results, pred)[1] != ""
        assert graph.derived_status(results, results[pred]) == "SUPERSEDED"

    def test_the_full_attack_on_the_head_is_blocked(self, repo):
        """Delete `supersedes` from the head, then rewrite the predecessor.

        The deletion alone is inert - the link is intact, so there is nothing to
        report - and the rewrite it was supposed to enable is caught.
        """
        edit(repo, "R-102", "supersedes:  R-101\n")
        assert x06(repo)["status"] == "PASS"
        append(repo, "R-101")
        fails_naming(repo, graph.REWRITTEN, "R-101")

    def test_the_same_edit_on_an_interior_record_is_caught_immediately(self, repo):
        """On an interior link the deletion is not even inert.

        `R-101` is itself sealed by `R-102`, so editing it at all - including to
        remove its own `supersedes` line - breaks that seal. FIND-Q9-52's answer
        to this was to reseal, which is the next test; without the reseal the
        tamperer is caught by their own bookkeeping, and the finding said so.
        """
        edit(repo, "R-101", "supersedes:  R-100\n")
        fails_naming(repo, graph.REWRITTEN, "R-101")


class TestM2TheSealPathLimb:
    """M2 - MU30, the limb the audit's evidence said to delete.

    It is kept, and these tests are the reason. Deleting it would restore a
    single-field definition, which is the condition every recorded disarm
    depends on: one editable line, and the seal machinery goes blind. Unifying
    upward instead makes the seal load-bearing - the field that carries the
    evidence is also a field that establishes the link, so neither can be
    removed without the other becoming visible.
    """

    def test_the_seal_path_limb_is_load_bearing(self, repo):
        edit(repo, "R-102", "supersedes:  R-101\n")
        results = records.load_results(repo)
        assert graph.seal_target(results["R-102"]) == "R-101"
        assert graph.link_of(results["R-102"]).exists
        assert graph.successors_of(results, "R-101") == ["R-102"]

    def test_a_seal_outside_the_results_directory_is_not_a_link(self, repo):
        """The limb establishes links now, so its match is anchored to the
        directory results live in. `_corroborates` matched on the basename
        alone, which was tolerable while the match only confirmed a link
        something else had established."""
        edit(
            repo,
            "R-102",
            "  path:   .ai/project/results/R-101.md",
            "  path:   notes/R-101.md",
        )
        results = records.load_results(repo)
        assert graph.seal_target(results["R-102"]) == ""
        assert graph.link_of(results["R-102"]).target == "R-101"

    def test_a_seal_naming_a_non_result_file_is_not_a_link(self, repo):
        edit(
            repo,
            "R-102",
            "  path:   .ai/project/results/R-101.md",
            "  path:   .ai/project/results/NOTES.md",
        )
        results = records.load_results(repo)
        assert graph.seal_target(results["R-102"]) == ""


class TestASealMayNotNameNothingQuietly:
    """`VER-009` V-2 and V-4 - the independent auditor's own attacks.

    `seal_target` normalised backslashes and then compared against a literal
    prefix, so seven spellings of a **real, existing** predecessor file resolved
    to no link - and nothing reported it. Inserting `./` into a seal path was
    therefore a way to delete the seal limb while leaving a block that reads as
    a correct, digested seal: exactly the residue §6.4's table blesses as
    sufficient. Combined with deleting `supersedes` and the back-link it gave a
    silent rewrite at `X-06 PASS`, which falsified the architecture's claim that
    "neither can be removed without the other becoming visible".

    Two rules close it. Separator noise resolves, so a lawful path is a link.
    Anything else that is declared and names no record is a **failure**, because
    the defect was never strictness - it was silence.
    """

    #: Spellings that name the predecessor unambiguously, whatever the
    #: separator noise. These resolve, because the alternative - voiding them -
    #: is what V-2 was.
    #:
    #: A pure-backslash path is **deliberately absent** from this list.
    #: `VER-010` F-5: backslash normalisation pre-dates the V-2 repair - V-2's
    #: own text says the old code "normalised backslashes" - so a parametrised
    #: case for it passes against the pre-fix implementation and constrains
    #: nothing this class exists to constrain. It is retained as behaviour
    #: coverage in `test_backslashes_normalise_which_pre_dates_this_repair`,
    #: named for what it actually is.
    RESOLVING = [
        "./.ai/project/results/R-101.md",
        "././.ai/project/results/R-101.md",
        ".ai/project/results//R-101.md",
        ".ai/project/./results/R-101.md",
        # Quoted, deliberately. `VER-011` C4: an *unquoted* padded scalar is
        # stripped by the record parser before any code here sees it, so it
        # passes against the pre-fix implementation and constrains nothing -
        # the F-5 defect, reintroduced by its own repair. A quoted scalar is
        # the only spelling that actually reaches `canonical_path`'s `.strip()`.
        "'  .ai/project/results/R-101.md  '",
    ]

    #: Spellings that are declared, name no result record, and must therefore
    #: **fail** - never resolve, and never pass in silence. Four families:
    #: canonicalises to nothing (F-1), traversal (F-3, F-4), absolute (F-3),
    #: and simply wrong (case, directory, extension, id form).
    REJECTED = [
        # F-1: declared, canonicalises to the empty string.
        "./", ".", "..", "/", "//", "../..", "././", "./.",
        # F-3/F-4: traversal - `..` is not resolved, so none of these names
        # the file it appears to. The third is the reviewer-deception case:
        # a human reads `R-101.md` and the old code resolved `R-100`.
        ".ai/project/results/../results/R-101.md",
        "../.ai/project/results/R-101.md",
        ".ai/project/results/R-101.md/../R-100.md",
        "a/../.ai/project/results/R-101.md",
        # F-3: absolute - what these name depends on where the reader stands.
        "/.ai/project/results/R-101.md",
        "//.ai/project/results/R-101.md",
        "\\.ai\\project\\results\\R-101.md",
        # Plainly not the required form.
        ".ai/project/Results/R-101.md",
        ".ai/project/results/r-101.md",
        ".ai/project/results/R-101.MD",
        ".ai/project/results/old/R-101.md",
        ".ai/project/results/NOTES.md",
        ".ai/project/results/R-1.md",
        "notes/R-101.md",
        "R-101.md",
    ]

    @staticmethod
    def _spell(repo, spelling):
        edit(repo, "R-102", "  path:   .ai/project/results/R-101.md",
             f"  path:   {spelling}")

    def test_the_canonical_path_is_a_link(self, repo):
        """The control. Everything below is measured against this."""
        results = records.load_results(repo)
        assert graph.seal_target(results["R-102"]) == "R-101"
        assert x06(repo)["status"] == "PASS"

    @pytest.mark.parametrize("spelling", RESOLVING)
    def test_separator_noise_still_names_the_predecessor(self, repo, spelling):
        self._spell(repo, spelling)
        results = records.load_results(repo)
        assert graph.seal_target(results["R-102"]) == "R-101"
        assert graph.successors_of(results, "R-101") == ["R-102"]
        assert x06(repo)["status"] == "PASS", x06(repo)["details"]

    def test_backslashes_normalise_which_pre_dates_this_repair(self, repo):
        """`VER-010` F-5, named honestly.

        Backslash normalisation was in the code V-2 was raised against, so this
        asserts behaviour that the V-2 repair did not introduce and does not
        protect. Kept because the behaviour is real and worth pinning; kept
        **out** of `RESOLVING` because a test that passes against the pre-fix
        implementation is not evidence for the fix, and counting it as such is
        the overstated-evidence defect this chain exists to stop.
        """
        self._spell(repo, ".ai\\project\\results\\R-101.md")
        assert graph.seal_target(records.load_results(repo)["R-102"]) == "R-101"
        assert x06(repo)["status"] == "PASS"

    @pytest.mark.parametrize("spelling", REJECTED)
    def test_a_declared_path_that_names_no_record_fails(self, repo, spelling):
        """Every rejection is a **failure**, never a silence.

        `VER-010` F-1 is the whole point of asserting the verdict rather than
        the absence of a link: before this, eight of these spellings produced
        no link *and no detail*, which reads to every consumer of
        `X-06["status"]` as "nothing is wrong here".
        """
        self._spell(repo, spelling)
        assert graph.seal_target(records.load_results(repo)["R-102"]) == ""
        fails_naming(repo, "names no result record")

    def test_a_declared_path_is_never_read_as_no_declaration(self, repo):
        """F-1 at the seam where it lived: `seal_path` returning `""` must not
        be readable as "this record declared nothing"."""
        self._spell(repo, "./")
        result = records.load_results(repo)["R-102"]
        assert graph.seal_path(result) == ""          # canonicalises to nothing
        assert graph.seal_declared(result) == "./"    # but it WAS declared
        assert graph.seal_declared_block(result)

    def test_a_seal_block_with_no_path_at_all_fails(self, repo):
        """`VER-010` F-2. Delete the `path:` line, keep `digest:`. Three line
        deletions across two files was a **smaller** diff than the residual
        §6.4 discloses, and it was silent."""
        edit(repo, "R-102", "  path:   .ai/project/results/R-101.md\n")
        result = records.load_results(repo)["R-102"]
        assert graph.seal_declared(result) == ""
        assert graph.seal_declared_block(result)
        fails_naming(repo, "declares no path")

    @pytest.mark.parametrize("blank", ["", "   ", "null", "~", "''"])
    def test_a_seal_path_that_parses_to_nothing_fails(self, repo, blank):
        """The same hole reached through the parser rather than the editor: a
        `path:` line whose value is blank, `null` or empty quotes."""
        self._spell(repo, blank)
        fails_naming(repo, "declares no path")

    def test_a_record_with_no_seal_block_is_not_accused(self, repo):
        """The converse, so the rules above cannot be satisfied by failing
        everything. `R-001`, `R-007` and `R-008` carry no seal block and
        pre-date the convention; they must stay reported, never accused."""
        drop_seal(repo, "R-101", "R-100")
        result = records.load_results(repo)["R-101"]
        assert not graph.seal_declared_block(result)
        res = x06(repo)
        assert not any("declares no path" in d for d in res["details"]), res["details"]
        assert not any("names no result record" in d for d in res["details"])

    def test_the_two_character_edit_no_longer_hides_a_rewrite(self, repo):
        """V-2's attack, end to end - **including the rewrite it exists for**.

        `VER-010` F-6: the first form of this test stopped after the three
        edits and never appended to the predecessor, so its name and docstring
        claimed a rewrite it did not perform. The assertion was sound and the
        description was not, which is the exact class FIND-Q9-46 and V-1 were.
        The rewrite is performed now and the test is named for what it does.

        Measured by the independent auditor before the F-1 repair: `X-06 PASS`,
        0 details, detail-set-identical to a clean run, with `R-102` still
        carrying `R-101`'s correct published digest.
        """
        self._spell(repo, "./")
        edit(repo, "R-102", "supersedes:  R-101\n")
        edit(repo, "R-101", "superseded_by: R-102\n")
        append(repo, "R-101")
        res = fails_naming(repo, "names no result record")
        # The seal block is still there, still correct, and now says so.
        seal = records.load_results(repo)["R-102"].supersedes_seal
        assert seal.get("digest") and seal.get("path") == "./"
        assert res["status"] == "FAIL"

    def test_a_seal_pointing_away_from_the_records_file_fails(self, repo):
        """V-4. Renaming the predecessor's file left the seal naming a path
        that does not exist, and nothing reconciled the seal's declared subject
        against the file actually digested."""
        (repo / ".ai/project/results/R-101.md").rename(
            repo / ".ai/project/results/R-101-archived.md"
        )
        fails_naming(repo, "R-101 is at", "not reconciled")


class TestASealBlockThatIsNotAMappingIsNotNoSealBlock:
    """`VER-011` G-1 - the two-facts-one-value defect, found a fourth time.

    `ResultRecord.supersedes_seal` coerces anything that is not a mapping to
    `{}`, and `seal_declared_block` read `bool({})`. So `{}` meant *no block* and
    *a block that did not parse as a mapping*, and both the F-1 and the F-2
    guard - built to close exactly this shape of defect one level up - skipped
    the malformed case in silence.

    The attack needs no exotic syntax. The **sequence** form `- path:` /
    `digest:` is the idiom every `inputs:` and `deliverables:` block in every
    record in this repository already uses, so it is the shape a careless author
    reaches for and the shape a tamperer can claim was a mistake. On the live
    records it rewrote `R-013` at `X-06 PASS` with a detail set byte-identical to
    a clean run, while `R-014` still displayed `R-013`'s correct published digest
    to a human reader.

    Declaredness is read from the parsed value before coercion now, so a
    malformed block is declared **and** malformed - two failures' worth of
    information, and neither of them silence.
    """

    SEQUENCE = (
        "supersedes_seal:\n"
        "    - path:   .ai/project/results/R-100.md\n"
        "      digest: {d}\n"
    )

    def _malform(self, repo, replacement):
        body = (repo / ".ai/project/results/R-101.md").read_text(encoding="utf-8")
        digest = [ln for ln in body.splitlines() if ln.startswith("  digest: ")][0]
        edit(repo, "R-101",
             "supersedes_seal:\n"
             "  path:   .ai/project/results/R-100.md\n" + digest + "\n",
             replacement.format(d=digest.split(": ", 1)[1]))

    def test_the_sequence_form_is_rejected_not_ignored(self, repo):
        self._malform(repo, self.SEQUENCE)
        result = records.load_results(repo)["R-101"]
        assert result.supersedes_seal == {}          # coerced, as before
        assert graph.seal_declared_block(result)     # but still *declared*
        assert graph.seal_block_malformed(result)
        fails_naming(repo, "not a {path, digest} mapping", "parsed as list")

    @pytest.mark.parametrize(
        "shape",
        [
            "supersedes_seal: .ai/project/results/R-100.md\n",
            "supersedes_seal: 12345\n",
            "supersedes_seal:\n    - .ai/project/results/R-100.md\n",
        ],
    )
    def test_any_non_mapping_shape_is_rejected(self, repo, shape):
        self._malform(repo, shape)
        fails_naming(repo, "not a {path, digest} mapping")

    def test_the_full_attack_through_a_malformed_block_is_blocked(self, repo):
        """G-1 end to end: reshape the block, delete `supersedes`, delete the
        back-link, rewrite the predecessor. Measured before the repair as
        `X-06 PASS` with a detail set identical to a clean run."""
        self._malform(repo, self.SEQUENCE)
        edit(repo, "R-101", "supersedes:  R-100\n")
        edit(repo, "R-100", "superseded_by: R-101\n")
        append(repo, "R-100")
        fails_naming(repo, "not a {path, digest} mapping")

    def test_a_record_with_no_block_is_still_not_accused(self, repo):
        """The converse. `R-001`, `R-007` and `R-008` pre-date the seal
        convention and carry no block; the rule must not reach them."""
        drop_seal(repo, "R-101", "R-100")
        result = records.load_results(repo)["R-101"]
        assert not graph.seal_declared_block(result)
        assert not graph.seal_block_malformed(result)
        assert not any(
            "not a {path, digest} mapping" in d for d in x06(repo)["details"]
        )

    def test_the_live_records_carry_well_formed_blocks(self):
        """Asserted against the real tree, because G-1 was demonstrated there
        and a synthetic-only regression test would not have caught it."""
        for rid, result in records.load_results(REPO).items():
            assert not graph.seal_block_malformed(result), rid
            if graph.seal_declared_block(result):
                assert isinstance(graph.seal_block_raw(result), dict), rid


class TestASealOnlyLinkIsStillGovernedByTheEpoch:
    """The mutation campaign's own finding, closed.

    Three mutants survived the first campaign against this repair, and two of
    them shared one uncovered shape: a record linked **only** by its seal path.
    Every test above deletes `supersedes` while leaving a seal *with a digest*,
    so nothing exercised a seal-only link whose digest was missing - and that is
    a live bypass, not a cosmetic gap. Reverting the epoch guard to
    `if result.supersedes` (mutant MU-A5) skipped the missing-seal rule
    entirely for such a record while the back-link cross-check stayed satisfied
    by the surviving path, leaving the predecessor rewritable with `X-06 PASS`.

    Recorded rather than quietly fixed: the campaign found this, the suite did
    not, and the note in `MU-A5` is the reason these tests exist.
    """

    def test_a_seal_without_a_digest_fails_the_epoch_rule(self, repo):
        edit(repo, "R-102", "supersedes:  R-101\n")
        body = (repo / ".ai/project/results/R-102.md").read_text(encoding="utf-8")
        digest = [ln for ln in body.splitlines() if ln.startswith("  digest: ")][0]
        edit(repo, "R-102", digest + "\n")
        results = records.load_results(repo)
        assert graph.link_of(results["R-102"]).exists
        assert graph.link_of(results["R-102"]).target == "R-101"
        fails_naming(repo, "R-102: supersedes R-101 and pins no")

    def test_the_predecessor_is_then_reported_unsealed_not_silently_fine(self, repo):
        edit(repo, "R-102", "supersedes:  R-101\n")
        body = (repo / ".ai/project/results/R-102.md").read_text(encoding="utf-8")
        digest = [ln for ln in body.splitlines() if ln.startswith("  digest: ")][0]
        edit(repo, "R-102", digest + "\n")
        results = records.load_results(repo)
        curr = graph.result_currency(repo, results["R-101"], results)
        assert curr.status == "SUPERSEDED"
        assert any("unsealed" in d for d in curr.drifted), curr.drifted

    def test_the_epoch_derivation_counts_a_seal_only_supersession(self, tmp_path):
        """`derived_seal_epoch` is evidence, never the rule (FIND-Q9-39) - and
        evidence that cannot see a whole class of seal is evidence that reads
        empty exactly when seals have been stripped down to that class."""
        root = tmp_path / "two"
        root.mkdir(parents=True)
        (root / ".ai/project/results").mkdir(parents=True)
        (root / "a.txt").write_text("deliverable\n", encoding="utf-8")
        seal = _write(root, "R-200", "SUPERSEDED", "superseded_by: R-201\n")
        _write(
            root,
            "R-201",
            "CURRENT",
            "supersedes_seal:\n"
            "  path:   .ai/project/results/R-200.md\n"
            f"  digest: {seal}\n",
            deliverables="deliverables:\n    - path: a.txt\n      digest: "
            + records.file_dc1(root, "a.txt")
            + "\n",
        )
        results = records.load_results(root)
        assert graph.successors_of(results, "R-200") == ["R-201"]
        assert graph.derived_seal_epoch(results) == "S-2026-08-09-12"


class TestM3DeleteTheSeal:
    @pytest.mark.parametrize("head,pred", [("R-102", "R-101"), ("R-101", "R-100")])
    def test_deleting_the_seal_fails_on_the_successor(self, repo, head, pred):
        drop_seal(repo, head, pred)
        fails_naming(repo, f"{head}: supersedes {pred} and pins no")

    @pytest.mark.parametrize("head,pred", [("R-102", "R-101"), ("R-101", "R-100")])
    def test_deleting_both_halves_still_fails(self, repo, head, pred):
        """`supersedes` *and* the seal. The predecessor's back-link is the third
        assertion, and it survives any edit confined to the successor."""
        drop_seal(repo, head, pred)
        edit(repo, head, f"supersedes:  {pred}\n")
        fails_naming(repo, f"{pred}: declares superseded_by {head}")


class TestM4M5M6TheTwoRepresentationsDisagree:
    def test_m4_changing_the_declared_target_is_divergence(self, repo):
        edit(repo, "R-102", "supersedes:  R-101", "supersedes:  R-100")
        fails_naming(repo, "one record, two different predecessors")

    def test_m5_changing_the_sealed_target_is_divergence(self, repo):
        edit(
            repo,
            "R-102",
            "  path:   .ai/project/results/R-101.md",
            "  path:   .ai/project/results/R-100.md",
        )
        fails_naming(repo, "one record, two different predecessors")

    @pytest.mark.parametrize(
        "declared,sealed", [("R-100", "R-101"), ("R-101", "R-100")]
    )
    def test_m6_the_two_cannot_disagree_silently(self, repo, declared, sealed):
        """The requirement stated as a property over both fields.

        However the declaration and the seal are pointed at different records,
        `X-06` fails and names the record that contradicts itself. This is the
        case neither definition could see while there were two of them:
        `_corroborates` was satisfied by the seal, `successor_of` followed the
        declaration, and each was satisfied by a *different* predecessor.
        """
        edit(repo, "R-102", "supersedes:  R-101", f"supersedes:  {declared}")
        edit(
            repo,
            "R-102",
            "  path:   .ai/project/results/R-101.md",
            f"  path:   .ai/project/results/{sealed}.md",
        )
        assert graph.link_of(records.load_results(repo)["R-102"]).divergent
        fails_naming(repo, "R-102", "underivable")


class TestM7AlterThePredecessorAfterPublication:
    @pytest.mark.parametrize("pred", ["R-101", "R-100"])
    def test_rewriting_a_superseded_record_fires(self, repo, pred):
        append(repo, pred)
        fails_naming(repo, graph.REWRITTEN, pred)

    def test_the_interior_attack_with_a_reseal_is_caught(self, repo):
        """FIND-Q9-52 exactly: delete the interior `supersedes`, reseal over the
        edited predecessor, then rewrite it. Pass 7 measured `X-06 PASS`, 0
        details, full check byte-identical to baseline, 275 tests green.

        The reseal no longer launders the edit, because deleting `supersedes` no
        longer removes the link that makes the seal be compared.
        """
        edit(repo, "R-101", "supersedes:  R-100\n")
        reseal(repo, "R-102", "R-101")
        append(repo, "R-100")
        fails_naming(repo, graph.REWRITTEN, "R-100")


class TestM8ASuccessorWithoutAValidPredecessor:
    @staticmethod
    def _point_at_nothing(repo):
        edit(repo, "R-102", "supersedes:  R-101", "supersedes:  R-199")
        edit(
            repo,
            "R-102",
            "  path:   .ai/project/results/R-101.md",
            "  path:   .ai/project/results/R-199.md",
        )

    def test_a_link_to_a_record_that_does_not_exist_fails(self, repo):
        self._point_at_nothing(repo)
        fails_naming(repo, "supersedes R-199, but no such result record exists")

    def test_it_holds_without_the_predecessors_back_link(self, repo):
        """The back-link is not doing the work. `superseded_by` is stripped from
        the predecessor first, so the successor's own assertion is the only one
        left - and it is still read."""
        edit(repo, "R-101", "superseded_by: R-102\n")
        self._point_at_nothing(repo)
        fails_naming(repo, "supersedes R-199, but no such result record exists")


class TestM9TwoCompetingSuccessors:
    @staticmethod
    def _claimant(repo, links):
        _write(
            repo,
            "R-103",
            "CURRENT",
            links,
            deliverables="deliverables:\n    - path: a.txt\n      digest: "
            + records.file_dc1(repo, "a.txt")
            + "\n",
        )

    def test_competing_successors_are_not_resolved_silently(self, repo):
        """`successor_of` returns the first in sort order. That choice must
        never be made quietly: two records claiming one predecessor fork the
        chain's provenance, and only one of their seals can be the seal that
        closed it."""
        seal = records.file_dc1(repo, ".ai/project/results/R-101.md")
        self._claimant(
            repo,
            "supersedes:  R-101\n"
            "supersedes_seal:\n"
            "  path:   .ai/project/results/R-101.md\n"
            f"  digest: {seal}\n",
        )
        results = records.load_results(repo)
        assert graph.successors_of(results, "R-101") == ["R-102", "R-103"]
        fails_naming(repo, "competing successors")

    def test_a_seal_only_claimant_also_competes(self, repo):
        """The competing claim is made through the seal alone - invisible to any
        definition that reads `supersedes` only, which is every definition the
        repository had before this repair."""
        seal = records.file_dc1(repo, ".ai/project/results/R-101.md")
        self._claimant(
            repo,
            "supersedes_seal:\n"
            "  path:   .ai/project/results/R-101.md\n"
            f"  digest: {seal}\n",
        )
        fails_naming(repo, "competing successors")


class TestM10AlterAResultAfterPublication:
    def test_editing_the_current_records_deliverable_fails(self, repo):
        (repo / "a.txt").write_text("moved\n", encoding="utf-8")
        fails_naming(repo, "R-102: declared CURRENT but is STALE")

    def test_deleting_a_superseded_record_outright_fails(self, repo):
        (repo / ".ai/project/results/R-101.md").unlink()
        assert x06(repo)["status"] == "FAIL"

    def test_editing_the_head_record_itself_is_not_claimed_to_be_caught(self, repo):
        """Stated as a limit, not a control. Nothing seals the CURRENT record -
        by construction, since the seal is written by a successor and the head
        has none. Its *deliverables* are pinned, so an edit to what it produced
        is caught; an edit to its own prose is not, and this test records that
        rather than leaving a reader to infer coverage that is not there.
        """
        append(repo, "R-102", "\nEdited head prose.\n")
        assert x06(repo)["status"] == "PASS"


class TestTheResidualIsMeasuredNotAsserted:
    def test_the_three_edit_residual_is_where_the_docstring_says_it_is(self, repo):
        """`X-06`'s disclosed residual, executed.

        Strip `superseded_by` from the predecessor **and** `supersedes` and the
        seal from the successor: every assertion that the link existed is gone,
        the records no longer contradict each other, and `X-06` passes.

        This test exists so that the disclosure cannot drift from the behaviour
        again. Pass 6 disclosed the cost as *"three edits across two files"*
        while the true cost was one edit in one file, and no test held the
        sentence to account. The two-edit prefix is required to **fail**, so the
        residual is pinned at exactly three.
        """
        drop_seal(repo, "R-102", "R-101")
        edit(repo, "R-102", "supersedes:  R-101\n")
        fails_naming(repo, "R-101: declares superseded_by R-102")

        edit(repo, "R-101", "superseded_by: R-102\n")
        assert x06(repo)["status"] == "PASS"

        # What it leaves behind, and the reason it is a narrowing rather than a
        # hole: a record whose own status field contradicts the graph.
        results = records.load_results(repo)
        assert results["R-101"].status == "SUPERSEDED"
        assert graph.successors_of(results, "R-101") == []
