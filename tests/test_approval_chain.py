"""Adversarial tests for the approval-supersession relation.

The point of this file is NOT to show that the check passes on today's
repository. A check that only passes today is the defect it was written to
prevent. Each test below attacks the invariant through a different
representation, and the one that matters most is `test_future_edit_*`: an
artifact changed without an approval must collapse the whole chain, or the
relation would be a way to launder unapproved edits.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aief_approval.chain import (  # noqa: E402
    State,
    ecr_approval_states,
    load_approvals,
    verify,
)
from aief_stage6.digests import dc1_digest  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
SUBJECT = "spec/synthetic.md"


def _approval(
    repo: Path,
    approval_id: str,
    subject_hash: str,
    prior_hash: str | None = None,
    subject_path: str = SUBJECT,
    ecr: str | None = None,
    omit_subject_path: bool = False,
) -> None:
    lines = [f"approval_id:   {approval_id}", "approver:      human-owner"]
    if not omit_subject_path:
        lines.append(f"subject_path:  {subject_path}")
    lines.append(f"subject_hash:  {subject_hash}")
    lines.append(f"prior_hash:    {prior_hash if prior_hash else 'null'}")
    if ecr:
        lines.append(f"ecr:           {ecr}")
    body = "\n".join(lines)
    target = repo / ".ai" / "project" / "approvals" / f"{approval_id}_synthetic.md"
    target.write_text(
        f"# {approval_id}\n\n```yaml\n{body}\n```\n", encoding="utf-8"
    )


def _registry(repo: Path, rows: dict[str, str]) -> None:
    body = ["# Freeze Registry", "", "| Artifact | Digest |", "|---|---|"]
    for path, digest in sorted(rows.items()):
        body.append(f"| `{path}` | `{digest}` |")
    (repo / ".ai" / "project" / "FROZEN.md").write_text(
        "\n".join(body) + "\n", encoding="utf-8"
    )


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    (tmp_path / ".ai" / "project" / "approvals").mkdir(parents=True)
    (tmp_path / "spec").mkdir()
    return tmp_path


def _write_subject(repo: Path, text: str) -> str:
    target = repo / SUBJECT
    target.write_text(text, encoding="utf-8")
    return dc1_digest(target.read_bytes())


def _build_chain(repo: Path, revisions: list[str]) -> list[str]:
    """Write each revision in order, filing an approval that binds it."""
    digests: list[str] = []
    prior: str | None = None
    for index, text in enumerate(revisions, start=1):
        digest = _write_subject(repo, text)
        _approval(
            repo,
            f"APR-{index:03d}",
            digest,
            prior,
            ecr=f"ECR-D-{index:03d}",
        )
        digests.append(digest)
        prior = digest
    _registry(repo, {SUBJECT: digests[-1]})
    return digests


# --------------------------------------------------------------------------
# Nominal
# --------------------------------------------------------------------------


def test_nominal_chain_head_live_rest_superseded_valid(repo: Path) -> None:
    _build_chain(repo, ["rev one\n", "rev two\n", "rev three\n", "rev four\n"])
    report = verify(repo)
    chain = report.chains[SUBJECT]
    assert report.ok, chain.failures
    assert chain.states["APR-004"] is State.LIVE
    for earlier in ("APR-001", "APR-002", "APR-003"):
        assert chain.states[earlier] is State.SUPERSEDED_VALID


def test_every_ecr_in_the_chain_satisfies_the_gate(repo: Path) -> None:
    """C1-C4 must all pass at once. That is the whole reason the relation exists."""
    _build_chain(repo, ["a\n", "b\n", "c\n", "d\n"])
    states = ecr_approval_states(repo)
    assert set(states) == {f"ECR-D-{i:03d}" for i in range(1, 5)}
    assert all(
        state in (State.LIVE, State.SUPERSEDED_VALID)
        for _, state in states.values()
    )


def test_single_approval_is_live(repo: Path) -> None:
    _build_chain(repo, ["only\n"])
    assert verify(repo).chains[SUBJECT].states["APR-001"] is State.LIVE


def test_registered_and_unchanged_with_no_approvals_passes(repo: Path) -> None:
    digest = _write_subject(repo, "never changed\n")
    _registry(repo, {SUBJECT: digest})
    report = verify(repo)
    assert report.ok
    assert report.chains[SUBJECT].approvals == []


# --------------------------------------------------------------------------
# The future-edit case - the attack the relation must not admit
# --------------------------------------------------------------------------


def test_future_edit_without_approval_collapses_the_whole_chain(repo: Path) -> None:
    _build_chain(repo, ["a\n", "b\n", "c\n"])
    # Someone edits the frozen artifact and files nothing.
    _write_subject(repo, "unapproved edit\n")
    report = verify(repo)
    chain = report.chains[SUBJECT]
    assert not report.ok
    assert all(state is State.VOID for state in chain.states.values())
    assert any("NO approval binds that state" in f for f in chain.failures)


def test_future_edit_is_repaired_by_appending_a_link(repo: Path) -> None:
    """The relation must stay satisfiable: filing the approval restores it."""
    _build_chain(repo, ["a\n", "b\n"])
    head = verify(repo).chains[SUBJECT]
    previous = head.tree_digest
    new_digest = _write_subject(repo, "c\n")
    _approval(repo, "APR-003", new_digest, previous, ecr="ECR-D-003")
    _registry(repo, {SUBJECT: new_digest})
    report = verify(repo)
    assert report.ok, report.chains[SUBJECT].failures
    assert report.chains[SUBJECT].states["APR-003"] is State.LIVE
    assert report.chains[SUBJECT].states["APR-001"] is State.SUPERSEDED_VALID


def test_reverting_the_bytes_without_a_record_does_not_relive_an_old_approval(
    repo: Path,
) -> None:
    """Rolling a file back to an earlier approved state makes that approval LIVE
    again - which is correct - but the later approvals must then be VOID, not
    silently still valid."""
    digests = _build_chain(repo, ["a\n", "b\n", "c\n"])
    _write_subject(repo, "a\n")
    _registry(repo, {SUBJECT: digests[0]})
    chain = verify(repo).chains[SUBJECT]
    assert chain.states["APR-001"] is State.LIVE
    assert chain.states["APR-002"] is State.VOID
    assert chain.states["APR-003"] is State.VOID


# --------------------------------------------------------------------------
# Malformed and adversarial records
# --------------------------------------------------------------------------


def test_broken_link_orphans_everything_before_it(repo: Path) -> None:
    digests = _build_chain(repo, ["a\n", "b\n", "c\n"])
    # Sever APR-002 from APR-001 by pointing it at a hash nobody produced.
    _approval(repo, "APR-002", digests[1], "f" * 64, ecr="ECR-D-002")
    chain = verify(repo).chains[SUBJECT]
    assert chain.states["APR-001"] is State.VOID
    assert chain.states["APR-002"] is State.SUPERSEDED_VALID
    assert chain.states["APR-003"] is State.LIVE


def test_fork_is_a_failure_not_a_preference(repo: Path) -> None:
    digests = _build_chain(repo, ["a\n", "b\n"])
    # A second approval claims to supersede the same state as APR-002.
    _approval(repo, "APR-900", "e" * 64, digests[0], ecr="ECR-D-900")
    report = verify(repo)
    assert not report.ok
    assert any("FORK" in f for f in report.chains[SUBJECT].failures)


def test_cycle_terminates_and_does_not_hang(repo: Path) -> None:
    digest_a = _write_subject(repo, "a\n")
    fake = "b" * 64
    _approval(repo, "APR-001", digest_a, fake)
    _approval(repo, "APR-002", fake, digest_a)
    _registry(repo, {SUBJECT: digest_a})
    chain = verify(repo).chains[SUBJECT]
    assert chain.states["APR-001"] is State.LIVE
    assert chain.states["APR-002"] is State.SUPERSEDED_VALID


def test_self_referential_approval_terminates(repo: Path) -> None:
    digest = _write_subject(repo, "a\n")
    _approval(repo, "APR-001", digest, digest)
    _registry(repo, {SUBJECT: digest})
    assert verify(repo).chains[SUBJECT].states["APR-001"] is State.LIVE


def test_missing_subject_path_is_rejected(repo: Path) -> None:
    digest = _write_subject(repo, "a\n")
    _approval(repo, "APR-001", digest, omit_subject_path=True)
    _registry(repo, {SUBJECT: digest})
    _, failures = load_approvals(repo)
    assert any("no subject_path" in f for f in failures)
    assert not verify(repo).ok


def test_non_hex_subject_hash_is_rejected(repo: Path) -> None:
    _write_subject(repo, "a\n")
    _approval(repo, "APR-001", "not-a-digest")
    _registry(repo, {SUBJECT: dc1_digest(b"a\n")})
    assert not verify(repo).ok


def test_uppercase_digest_is_rejected(repo: Path) -> None:
    """DC-1 declares 64 lowercase hex. Accepting uppercase would let two spellings
    of one digest fail to link."""
    digest = _write_subject(repo, "a\n")
    _approval(repo, "APR-001", digest.upper())
    _registry(repo, {SUBJECT: digest})
    assert not verify(repo).ok


def test_duplicate_approval_id_is_rejected(repo: Path) -> None:
    digest = _write_subject(repo, "a\n")
    _approval(repo, "APR-001", digest)
    duplicate = repo / ".ai" / "project" / "approvals" / "APR-001_other.md"
    duplicate.write_text(
        "```yaml\napproval_id:   APR-001\nsubject_path:  spec/synthetic.md\n"
        f"subject_hash:  {digest}\nprior_hash:    null\n```\n",
        encoding="utf-8",
    )
    _registry(repo, {SUBJECT: digest})
    _, failures = load_approvals(repo)
    assert any("declared twice" in f for f in failures)


def test_registry_disagreeing_with_the_tree_is_a_failure(repo: Path) -> None:
    _build_chain(repo, ["a\n", "b\n"])
    _registry(repo, {SUBJECT: "c" * 64})
    report = verify(repo)
    assert not report.ok
    assert any("does not describe" in f for f in report.chains[SUBJECT].failures)


def test_approval_naming_an_absent_path_is_a_failure(repo: Path) -> None:
    _approval(repo, "APR-001", "a" * 64, subject_path="spec/ghost.md")
    _registry(repo, {})
    report = verify(repo)
    assert not report.ok
    assert any("absent from the tree" in f for f in report.chains["spec/ghost.md"].failures)


def test_inline_comment_after_a_value_does_not_corrupt_the_link(repo: Path) -> None:
    """The real approvals carry trailing `# ...` comments on these very fields."""
    digest = _write_subject(repo, "a\n")
    target = repo / ".ai" / "project" / "approvals" / "APR-001_commented.md"
    target.write_text(
        "```yaml\napproval_id:   APR-001   # first\n"
        "subject_path:  spec/synthetic.md   # the volume\n"
        f"subject_hash:  {digest}   # measured\n"
        "prior_hash:    null   # baseline\n"
        "ecr:           ECR-D-001   # defect\n```\n",
        encoding="utf-8",
    )
    _registry(repo, {SUBJECT: digest})
    report = verify(repo)
    assert report.ok, report.failures
    assert report.chains[SUBJECT].states["APR-001"] is State.LIVE


# --------------------------------------------------------------------------
# The live repository
# --------------------------------------------------------------------------


def test_live_repository_spec01_chain_resolves(  ) -> None:
    """Regression lock on the real invariant: ECR-D-001's approvals were voided by
    ECR-D-002's lawful edit to the same volume, and the relation is what makes C1
    and C2 both satisfiable."""
    report = verify(REPO, ["spec/01_SEWCP-200_Cooling_Plate.md"])
    chain = report.chains["spec/01_SEWCP-200_Cooling_Plate.md"]
    assert chain.ok, chain.failures
    assert State.LIVE in chain.states.values()
    assert all(state is not State.VOID for state in chain.states.values())


def test_live_repository_every_spec_volume_is_accounted_for() -> None:
    """No spec/** volume may sit at bytes no approval reaches."""
    report = verify(REPO)
    for path, chain in report.chains.items():
        if not path.startswith("spec/"):
            continue
        assert chain.ok, f"{path}: {chain.failures}"
