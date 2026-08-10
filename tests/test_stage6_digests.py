"""Developer sanity tests: digest constructions against the published worked
examples. Certification tests are the test-engineer's separate deliverable.

Actor provenance: software.software-engineer - S-2026-08-08-07.

Every expected value below is a normative constant from
framework/framework.manifest.json metadata.reproducible.digest_constructions;
none is produced by the code under test.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from aief_stage6.digests import (
    DuplicatePathError,
    EmptySetError,
    dc1_digest,
    dc1_normalise,
    dc2_digest,
    dc4_digest,
    dc5_digest,
    dc5_sidecar_text,
)

ZERO = "0" * 64
ONE = "1" * 64


def test_dc2_worked_example():
    # digest_constructions.frozen_set_aggregate.worked_example
    pairs = [("a/alpha.md", ZERO), ("b/beta.md", ONE)]
    assert dc2_digest(pairs) == (
        "8de12581a7d3aef29454fcdfd696a71e4d5c1a0352f69c7a6b03b167d0f5f1b3"
    )


def test_dc2_order_independent_of_input_order():
    pairs = [("b/beta.md", ONE), ("a/alpha.md", ZERO)]
    assert dc2_digest(pairs) == (
        "8de12581a7d3aef29454fcdfd696a71e4d5c1a0352f69c7a6b03b167d0f5f1b3"
    )


def test_dc2_empty_registry():
    # frozen_set_aggregate.empty_registry
    assert dc2_digest([]) == (
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )


def test_dc4_worked_example():
    # digest_constructions.core_aggregate.worked_example
    pairs = [("BOOT.md", ZERO), ("core/VERSION", ONE)]
    assert dc4_digest(pairs) == (
        "eb6e969b9f1d31a367ccf83315c1a40f8df0bb1c7dec41566a637ac3740325b1"
    )


def test_dc4_empty_set_never_lawful():
    with pytest.raises(EmptySetError):
        dc4_digest([])


def test_duplicate_path_halts():
    with pytest.raises(DuplicatePathError):
        dc4_digest([("BOOT.md", ZERO), ("BOOT.md", ONE)])


def test_truncated_digest_rejected():
    with pytest.raises(ValueError):
        dc4_digest([("BOOT.md", ZERO[:32])])


def test_dc5_abc_vector():
    # digest_constructions.release_digest.worked_example (FIPS 180 vector)
    assert dc5_digest(b"abc") == (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )


def test_dc5_sidecar_format():
    d = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert dc5_sidecar_text(d, "aief-1.0.0-mechanical.tar") == (
        f"{d}  aief-1.0.0-mechanical.tar\n"
    )


def test_dc1_normalisation_rules():
    # per_artifact.normalisation, clause by clause.
    raw = b"\xef\xbb\xbfline one  \r\nline two\t\rline three\n\n\n"
    assert dc1_normalise(raw) == b"line one\nline two\nline three\n"


def test_dc1_idempotent_on_normal_form():
    normal = b"alpha\nbeta\n"
    assert dc1_normalise(normal) == normal
    assert dc1_digest(normal) == dc1_digest(b"alpha  \r\nbeta\r\n\n")
