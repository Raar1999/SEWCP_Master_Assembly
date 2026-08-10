"""Platform tests for the tokenizer wiring (TF-1/TF-2 per AMD-26).

Actor provenance: software.platform-engineer - S-2026-08-08-08.

Covers the platform slice of CMP-BLOCK-005 Stage 6: artifact custody,
raw-octet pin computation, FIND-Q4-1 trust-on-first-use enforcement,
special-token disablement, offline assembly determinism, and the fail-safe
(absence blocks, never estimates). Tests that need the real artifacts skip
when `build/stage6/tokenizer_artifacts/` is not provisioned - they never
fetch anything.
"""

import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from aief_stage6.tokenizers import (
    CL100K_PAT_STR,
    TOFU_RECORD_NAME,
    probe,
    raw_octet_sha256,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = REPO_ROOT / "build" / "stage6" / "tokenizer_artifacts"

needs_artifacts = pytest.mark.skipif(
    not (ARTIFACT_DIR / "cl100k_base.tiktoken").is_file()
    or not (ARTIFACT_DIR / "spiece.model").is_file(),
    reason="tokenizer artifacts not provisioned under build/stage6/",
)


@needs_artifacts
def test_probe_assembles_both_families_with_pins():
    p = probe(artifact_dir=ARTIFACT_DIR)
    assert p.available, p.missing
    by_id = {f.family_id: f for f in p.families}
    assert set(by_id) == {"TF-1", "TF-2"}
    # pin_value_rule: the pin is computed from the artifact in hand.
    assert by_id["TF-1"].artifact_pin == raw_octet_sha256(
        ARTIFACT_DIR / "cl100k_base.tiktoken"
    )
    assert by_id["TF-2"].artifact_pin == raw_octet_sha256(
        ARTIFACT_DIR / "spiece.model"
    )
    for pin in (by_id["TF-1"].artifact_pin, by_id["TF-2"].artifact_pin):
        assert isinstance(pin, str) and len(pin) == 64
        int(pin, 16)


@needs_artifacts
def test_special_tokens_disabled_and_empty_text_zero():
    """tf-1/tf-2 special_tokens 'disabled - measurement tokenises file text
    only; no special token is injected'."""
    p = probe(artifact_dir=ARTIFACT_DIR)
    assert p.available, p.missing
    for fam in p.families:
        assert fam.count("") == 0  # nothing injected on empty text
        # A special-token literal is ordinary text: several pieces, never one
        # reserved id's worth.
        assert fam.count("<|endoftext|>") > 1


@needs_artifacts
def test_counts_deterministic_across_assemblies():
    """tf-1/tf-2 .determinism: fixed artifact => fixed segmentation."""
    sample = (REPO_ROOT / ".ai" / "BOOT.md").read_text(encoding="utf-8")
    runs = []
    for _ in range(2):
        p = probe(artifact_dir=ARTIFACT_DIR)
        assert p.available, p.missing
        runs.append({f.family_id: f.count(sample) for f in p.families})
    assert runs[0] == runs[1]
    assert all(n > 0 for n in runs[0].values())


@needs_artifacts
def test_offline_tf1_matches_installed_tiktoken_definition():
    """CL100K_PAT_STR is transcribed from tiktoken_ext.openai_public; detect
    drift against the installed package source instead of absorbing it."""
    import inspect

    import tiktoken_ext.openai_public as pub

    src = inspect.getsource(pub.cl100k_base)
    assert CL100K_PAT_STR in src, (
        "installed tiktoken cl100k_base pat_str differs from the transcribed "
        "CL100K_PAT_STR - reconcile before measuring"
    )


@needs_artifacts
def test_tofu_record_matches_artifacts_in_hand():
    """FIND-Q4-1: the acquisition record's corroborated hashes equal the
    artifacts actually in custody."""
    record_path = ARTIFACT_DIR / TOFU_RECORD_NAME
    if not record_path.is_file():
        pytest.skip("no trust-on-first-use record present")
    record = json.loads(record_path.read_text(encoding="utf-8"))
    for name, entry in record["artifacts"].items():
        assert entry["sha256_raw_octets"] == raw_octet_sha256(ARTIFACT_DIR / name)


def test_probe_fail_safe_when_artifacts_absent(tmp_path):
    """Absence blocks: no family, no availability, no estimate."""
    p = probe(artifact_dir=tmp_path)
    assert not p.available
    assert len(p.missing) == 2
    assert any("TF-1" in m for m in p.missing)
    assert any("TF-2" in m for m in p.missing)


@needs_artifacts
def test_tofu_mismatch_blocks_family(tmp_path):
    """A tampered artifact against the acquisition record is a loud failure,
    never a silent re-pin (FIND-Q4-1)."""
    shutil.copy2(ARTIFACT_DIR / "cl100k_base.tiktoken", tmp_path / "cl100k_base.tiktoken")
    shutil.copy2(ARTIFACT_DIR / "spiece.model", tmp_path / "spiece.model")
    tampered = (tmp_path / "spiece.model").read_bytes() + b"\x00"
    (tmp_path / "spiece.model").write_bytes(tampered)
    record = {
        "artifacts": {
            "cl100k_base.tiktoken": {
                "sha256_raw_octets": raw_octet_sha256(tmp_path / "cl100k_base.tiktoken")
            },
            "spiece.model": {
                # The record carries the pre-tamper (corroborated) hash.
                "sha256_raw_octets": raw_octet_sha256(ARTIFACT_DIR / "spiece.model")
            },
        }
    }
    (tmp_path / TOFU_RECORD_NAME).write_text(json.dumps(record), encoding="utf-8")
    p = probe(artifact_dir=tmp_path)
    assert not p.available
    assert any("TF-2" in m and "trust-on-first-use" in m for m in p.missing)
    # TF-1 is intact and still assembles.
    assert [f.family_id for f in p.families] == ["TF-1"]


@needs_artifacts
def test_artifact_sizes_and_known_counts():
    """Sanity anchors: artifact octet sizes as published upstream; a fixed
    two-word string is two tokens under both families."""
    assert (ARTIFACT_DIR / "cl100k_base.tiktoken").stat().st_size == 1681126
    assert (ARTIFACT_DIR / "spiece.model").stat().st_size == 791656
    p = probe(artifact_dir=ARTIFACT_DIR)
    assert p.available, p.missing
    for fam in p.families:
        assert fam.count("hello world") == 2
