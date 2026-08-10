"""Adversarial tests for the C6 verification-supersession relation.

ECR-D-012 disposition A, ruled by the human owner S-2026-08-10-04 and declared
in `GATES.md` section *Supersession of verification reports*.

The point of this file is NOT to show that C6 passes on today's repository. A
check that only passes today is the defect it was written to prevent. Each test
attacks the relation through a different representation, and the two that matter
most are `test_unsealed_supersession_does_not_retire_a_report` and
`test_rewriting_a_sealed_report_breaks_the_seal`: without those the relation
would be a way to retire an adverse audit by asserting that one had read it.

Written in the manner of `test_approval_chain.py`, against the same standard the
approvals layer is held to, because these are the same invariant in two layers.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aief_gate.criteria import (  # noqa: E402
    _load_reports,
    _verdict_of,
    evaluate,
)
from aief_stage6.digests import dc1_digest  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
VERIF = ".ai/project/verification"
GATED = ("ECR-D-001", "ECR-D-002", "ECR-D-003", "ECR-D-004")


# --------------------------------------------------------------------------
# Fixtures: a throwaway copy of the repository, so every attack below runs
# against the real checker and the real record set, never against a mock.
# --------------------------------------------------------------------------


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A copy of the repository holding only what C6 reads."""
    dst = tmp_path / "repo"
    for rel in (VERIF, ".ai/project/ecr", ".ai/project/approvals",
                ".ai/core/schemas"):
        shutil.copytree(REPO / rel, dst / rel)
    for rel in (".ai/project/OPEN_ITEMS.md", ".ai/project/FROZEN.md"):
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, dst / rel)
    shutil.copytree(REPO / "spec", dst / "spec")
    return dst


def _report(
    repo: Path,
    ver_id: str,
    subject: str,
    status: str = "CLEARED - synthetic",
    supersedes: str | None = None,
    seals: dict[str, str] | None = None,
    verifier: str = "qa-engineer",
    author: str = "chief-systems-engineer",
) -> Path:
    lines = [
        f"verification_id: {ver_id}",
        f"subject:         {subject}",
        f"verifier_role:   {verifier}",
        f"author_role:     {author}",
        f"status:          {status}",
    ]
    if supersedes is not None:
        lines.append(f"supersedes:      {supersedes}")
    if seals is not None:
        lines.append("supersedes_seal:")
        lines.extend(f"  - {k} {v}" for k, v in seals.items())
    path = repo / VERIF / f"{ver_id}_synthetic.md"
    path.write_text(
        f"# {ver_id}\n\n```yaml\n" + "\n".join(lines) + "\n```\n",
        encoding="utf-8",
    )
    return path


def _dc1(path: Path) -> str:
    return dc1_digest(path.read_bytes())


def _c6(repo: Path):
    return next(c for c in evaluate(repo).criteria if c.id == "C6")


def _residue_for(repo: Path, ecr: str) -> list[str]:
    return [r for r in _c6(repo).residue if r.startswith(f"{ecr}:")]


# --------------------------------------------------------------------------
# The verdict vocabulary - VER-016 F-12, and the defect it did not find
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "status,expected",
    [
        ("CLEARED", "CLEARED"),
        ("CLEARED - 11 PASS, 0 FAIL", "CLEARED"),
        ("cleared. everything reproduces", "CLEARED"),
        ("NOT CLEARED", "NOT CLEARED"),
        ("NOT CLEARED - 6 PASS, 4 FAIL", "NOT CLEARED"),
        ("not  cleared", "NOT CLEARED"),
    ],
)
def test_the_declared_vocabulary_parses(status: str, expected: str) -> None:
    assert _verdict_of(status) == expected


def test_a_passing_tally_containing_the_token_fail_still_clears() -> None:
    """VER-016 F-12 exactly: this status was refused on the word FAIL."""
    assert _verdict_of("CLEARED - 11 PASS, 0 FAIL") == "CLEARED"


@pytest.mark.parametrize(
    "status",
    [
        "",
        "VERIFIED",
        "ECR-D-001 NOT CLOSED",
        "PASSED",
        "OK",
        "COMPLETE - no findings",
    ],
)
def test_an_unrecognised_status_never_clears(status: str) -> None:
    """The vocabulary cannot be widened by writing something new.

    `ECR-D-001 NOT CLOSED` is not hypothetical - it is VER-014's declared
    status. The predicate it faced was a scan for FAIL / NOT CLEARED / NOT
    VERIFIED, none of which it contains, so C6 passed ECR-D-001 for as long as
    that predicate stood, on a report whose section 6 reads "ECR-D-001 is NOT
    CLOSED after four rounds. LC-M04-EXIT C6 is not satisfied for it."
    VER-016 F-12 called that predicate fail-safe. It was not.
    """
    assert _verdict_of(status) != "CLEARED"


def test_the_legacy_non_clearing_form_is_read_as_substance() -> None:
    assert _verdict_of("VERIFIED WITH FINDINGS - NOT CLEARED. 6 PASS, 4 FAIL") == (
        "NOT CLEARED"
    )


# --------------------------------------------------------------------------
# The seal - a supersession that proves nothing retires nothing
# --------------------------------------------------------------------------


def test_a_sealed_supersession_retires_its_predecessor(repo: Path) -> None:
    victim = _report(repo, "VER-900", "ECR-D-002 synthetic", status="NOT CLEARED - x")
    assert "VER-900" in " ".join(_residue_for(repo, "ECR-D-002"))
    _report(
        repo, "VER-901", "ECR-D-002 synthetic",
        supersedes="VER-900", seals={"VER-900": _dc1(victim)},
    )
    residue = " ".join(_residue_for(repo, "ECR-D-002"))
    assert "VER-900" not in residue
    # The evidence names every retired report, so the assertion is on membership
    # rather than on adjacency - the live VER-017 already retires three others and
    # the list is sorted.
    evidence = [e for e in _c6(repo).evidence if e.startswith("ECR-D-002:")]
    assert evidence and "superseding" in evidence[0]
    assert "VER-900" in evidence[0].split("superseding")[1]


def test_unsealed_supersession_does_not_retire_a_report(repo: Path) -> None:
    """The whole point. A bare claim is not evidence that anything was read."""
    _report(repo, "VER-900", "ECR-D-002 synthetic", status="NOT CLEARED - x")
    _report(repo, "VER-901", "ECR-D-002 synthetic", supersedes="VER-900")
    residue = " ".join(_residue_for(repo, "ECR-D-002"))
    assert "no supersedes_seal entry" in residue
    assert "unproved" in residue
    assert "VER-900" in residue


def test_a_seal_over_the_wrong_bytes_does_not_retire(repo: Path) -> None:
    _report(repo, "VER-900", "ECR-D-002 synthetic", status="NOT CLEARED - x")
    _report(
        repo, "VER-901", "ECR-D-002 synthetic",
        supersedes="VER-900", seals={"VER-900": "0" * 64},
    )
    assert "has been\nrewritten" in " ".join(
        _residue_for(repo, "ECR-D-002")
    ).replace("  ", " ") or "rewritten" in " ".join(_residue_for(repo, "ECR-D-002"))


def test_rewriting_a_sealed_report_breaks_the_seal(repo: Path) -> None:
    """After supersession the predecessor is MORE protected, not less."""
    victim = _report(repo, "VER-900", "ECR-D-002 synthetic", status="NOT CLEARED - x")
    _report(
        repo, "VER-901", "ECR-D-002 synthetic",
        supersedes="VER-900", seals={"VER-900": _dc1(victim)},
    )
    assert "VER-900" not in " ".join(_residue_for(repo, "ECR-D-002"))
    victim.write_text(
        victim.read_text(encoding="utf-8").replace(
            "NOT CLEARED - x", "NOT CLEARED - findings silently deleted"
        ),
        encoding="utf-8",
    )
    assert "rewritten" in " ".join(_residue_for(repo, "ECR-D-002"))


def test_superseding_a_report_that_does_not_exist_fails(repo: Path) -> None:
    _report(
        repo, "VER-901", "ECR-D-002 synthetic",
        supersedes="VER-899", seals={"VER-899": "a" * 64},
    )
    assert "not\na verification report on disk" in " ".join(
        _residue_for(repo, "ECR-D-002")
    ).replace("  ", " ") or "not a verification report on disk" in " ".join(
        _residue_for(repo, "ECR-D-002")
    )


def test_a_seal_without_a_matching_supersedes_declaration_fails(repo: Path) -> None:
    """FIND-Q9-51's shape: deleting `supersedes` must not disarm the seal."""
    victim = _report(repo, "VER-900", "ECR-D-002 synthetic", status="NOT CLEARED - x")
    _report(
        repo, "VER-901", "ECR-D-002 synthetic",
        supersedes=None, seals={"VER-900": _dc1(victim)},
    )
    residue = " ".join(_residue_for(repo, "ECR-D-002"))
    assert "the two declarations disagree" in residue
    assert "VER-900" in residue


# --------------------------------------------------------------------------
# Forks, cycles, self-reference - ambiguity is a failure, not a preference
# --------------------------------------------------------------------------


def test_a_fork_is_a_failure(repo: Path) -> None:
    victim = _report(repo, "VER-900", "ECR-D-002 synthetic", status="NOT CLEARED - x")
    seal = {"VER-900": _dc1(victim)}
    _report(repo, "VER-901", "ECR-D-002 synthetic", supersedes="VER-900", seals=seal)
    _report(repo, "VER-902", "ECR-D-002 synthetic", supersedes="VER-900", seals=seal)
    assert "fork" in " ".join(_residue_for(repo, "ECR-D-002"))


def test_self_supersession_is_a_failure(repo: Path) -> None:
    _report(
        repo, "VER-901", "ECR-D-002 synthetic",
        supersedes="VER-901", seals={"VER-901": "b" * 64},
    )
    assert "supersedes itself" in " ".join(_residue_for(repo, "ECR-D-002"))


def test_a_graph_with_no_head_fails_closed(repo: Path) -> None:
    """No silent fallback to the unfiltered set.

    The predicate this replaced ended `... ] or naming`, so when every naming
    report was superseded it fell back to reading all of them. Here the only
    naming report is retired by a report on another subject, leaving nothing to
    govern; the criterion must fail rather than pick something.
    """
    victim = _report(repo, "VER-900", "ECR-D-002 synthetic", status="NOT CLEARED - x")
    _report(
        repo, "VER-901", "ECR-D-002 synthetic and nothing else",
        supersedes="VER-900,VER-901", seals={
            "VER-900": _dc1(victim), "VER-901": "c" * 64,
        },
    )
    residue = " ".join(_residue_for(repo, "ECR-D-002"))
    assert "supersedes itself" in residue


# --------------------------------------------------------------------------
# Scope - the set is per-ECR, never global
# --------------------------------------------------------------------------


def test_a_report_on_another_subject_cannot_retire_this_audit(repo: Path) -> None:
    """The global set let a Stage 5 report retire the ECR-D-002 audit."""
    victim = _report(repo, "VER-900", "ECR-D-002 synthetic", status="NOT CLEARED - x")
    _report(
        repo, "VER-901", "some unrelated Stage 5 emission",
        supersedes="VER-900", seals={"VER-900": _dc1(victim)},
    )
    residue = " ".join(_residue_for(repo, "ECR-D-002"))
    assert "VER-900" in residue
    assert "does not clear" in residue


# --------------------------------------------------------------------------
# The properties that were already there, held against regression
# --------------------------------------------------------------------------


def test_a_superseding_report_that_does_not_clear_still_gates(repo: Path) -> None:
    victim = _report(repo, "VER-900", "ECR-D-002 synthetic", status="NOT CLEARED - x")
    _report(
        repo, "VER-901", "ECR-D-002 synthetic", status="NOT CLEARED - still broken",
        supersedes="VER-900", seals={"VER-900": _dc1(victim)},
    )
    assert "does not clear" in " ".join(_residue_for(repo, "ECR-D-002"))


def test_self_verification_still_fails(repo: Path) -> None:
    _report(
        repo, "VER-901", "ECR-D-002 synthetic",
        verifier="chief-systems-engineer", author="chief-systems-engineer",
    )
    assert "LAW-05" in " ".join(_residue_for(repo, "ECR-D-002"))


def test_a_body_mention_is_not_verification(repo: Path) -> None:
    path = repo / VERIF / "VER-903_synthetic.md"
    path.write_text(
        "# VER-903\n\n```yaml\nverification_id: VER-903\n"
        "subject:         something else entirely\n"
        "verifier_role:   qa-engineer\nauthor_role:     chief-systems-engineer\n"
        "status:          CLEARED - synthetic\n```\n\nECR-D-002 is mentioned here.\n",
        encoding="utf-8",
    )
    assert "VER-903" not in " ".join(_c6(repo).evidence)


def test_crlf_reports_parse(repo: Path) -> None:
    """VER-001..VER-014 are CRLF files.

    Parsing the raw decode instead of the DC-1-normalised text dropped every one
    of them, and C6 reported "no verification report declares it as subject" for
    ECR-D-001 - discarding four cold rounds on a line ending.
    """
    path = repo / VERIF / "VER-904_synthetic.md"
    path.write_bytes(
        b"# VER-904\r\n\r\n```yaml\r\nverification_id: VER-904\r\n"
        b"subject:         ECR-D-002 synthetic\r\nverifier_role:   qa-engineer\r\n"
        b"author_role:     chief-systems-engineer\r\n"
        b"status:          CLEARED - synthetic\r\n```\r\n"
    )
    assert _load_reports(repo)["VER-904_synthetic.md"]["verification_id"] == "VER-904"


def test_every_gated_ecr_is_reported_on(repo: Path) -> None:
    """C6 must speak to all four, not silently skip one."""
    text = " ".join(_c6(repo).evidence + _c6(repo).residue)
    for ecr in GATED:
        assert ecr in text
