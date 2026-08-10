"""Certification tests: digest constructions DC-1, DC-2, DC-4, DC-5.

Actor provenance: software.test-engineer - S-2026-08-08-09 (independent
verification; author of no code under test - AGT-test-engineer separation
of duties).

METHOD: every expected value below is derived from the NORMATIVE TEXTS -
`framework/framework.manifest.json` `metadata.reproducible.digest_constructions`
(DC-1, DC-2, DC-4, DC-5) and AIEF-AMD-010 AMD-27/AMD-28 - or computed in the
test itself with `hashlib` directly over a preimage constructed by hand from
the declared grammar. Nothing is derived from reading the implementation.
"""

import hashlib
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aief_stage6.digests import (
    DuplicatePathError,
    EmptySetError,
    aggregate_preimage,
    dc1_digest,
    dc1_normalise,
    dc2_digest,
    dc4_digest,
    dc5_digest,
    dc5_sidecar_text,
)

# Published worked examples (normative constants, transcribed from the
# manifest / AMD-010; any implementation must reproduce them exactly).
DC2_WORKED = "8de12581a7d3aef29454fcdfd696a71e4d5c1a0352f69c7a6b03b167d0f5f1b3"
DC4_WORKED = "eb6e969b9f1d31a367ccf83315c1a40f8df0bb1c7dec41566a637ac3740325b1"
DC2_EMPTY = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
DC5_ABC = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

Z = "0" * 64
O = "1" * 64


# --------------------------------------------------------------------------
# DC-1: 'decode UTF-8 stripping any byte-order mark; convert CRLF and lone CR
# to LF; strip trailing whitespace from every line; remove trailing blank
# lines; append exactly one terminal LF; encode UTF-8'
# --------------------------------------------------------------------------

class TestDc1Normalisation:
    def test_terminal_lf_appended_exactly_once(self):
        # 'append exactly one terminal LF'
        assert dc1_normalise(b"abc") == b"abc\n"
        assert dc1_normalise(b"abc\n") == b"abc\n"

    def test_bom_stripped(self):
        # 'stripping any byte-order mark'
        assert dc1_normalise(b"\xef\xbb\xbfabc") == b"abc\n"
        assert dc1_digest(b"\xef\xbb\xbfabc") == dc1_digest(b"abc")

    def test_crlf_converted(self):
        # 'convert CRLF ... to LF'
        assert dc1_normalise(b"a\r\nb") == b"a\nb\n"

    def test_lone_cr_converted(self):
        # 'convert ... lone CR to LF'
        assert dc1_normalise(b"a\rb") == b"a\nb\n"

    def test_mixed_cr_crlf_lf(self):
        assert dc1_normalise(b"a\r\nb\rc\nd") == b"a\nb\nc\nd\n"

    def test_trailing_whitespace_stripped_every_line(self):
        # 'strip trailing whitespace from every line' (spaces and tabs)
        assert dc1_normalise(b"a  \nb\t\nc \t ") == b"a\nb\nc\n"

    def test_leading_whitespace_preserved(self):
        # Only TRAILING whitespace is declared stripped.
        assert dc1_normalise(b"  a\n\tb") == b"  a\n\tb\n"

    def test_interior_blank_lines_preserved(self):
        # Only TRAILING blank lines are declared removed.
        assert dc1_normalise(b"a\n\nb") == b"a\n\nb\n"

    def test_trailing_blank_lines_removed(self):
        assert dc1_normalise(b"a\n\n\n") == b"a\n"
        # blank lines that are whitespace-only become blank after the strip
        # step and are then trailing blank lines - removed.
        assert dc1_normalise(b"a\n   \n\t\n") == b"a\n"

    def test_idempotent(self):
        raw = b"\xef\xbb\xbfline one  \r\nline two\r\n\r\n"
        once = dc1_normalise(raw)
        assert dc1_normalise(once) == once

    def test_digest_is_sha256_of_normalised_content(self):
        # DC-1: SHA-256 over normalised content, 64 lowercase hex. The
        # expected value is computed here with hashlib over the hand-built
        # normal form - independent of the module's own hashing path.
        raw = b"alpha \r\nbeta\r"
        expected = hashlib.sha256(b"alpha\nbeta\n").hexdigest()
        got = dc1_digest(raw)
        assert got == expected
        assert len(got) == 64 and got == got.lower()

    def test_non_utf8_input_rejected_not_absorbed(self):
        # 'decode UTF-8' - a non-decodable artifact has no DC-1 normal form;
        # silent replacement would make two different byte streams hash alike.
        with pytest.raises(UnicodeDecodeError):
            dc1_normalise(b"\xff\xfe\x00A")


# --------------------------------------------------------------------------
# DC-2 / DC-4 shared record grammar: '<path> <SP> <digest> <LF>', ascending
# UTF-8 octet order of <path>, no header/trailer/BOM, UTF-8.
# --------------------------------------------------------------------------

class TestAggregateGrammar:
    def test_dc2_worked_example(self):
        # frozen_set_aggregate.worked_example - normative.
        pairs = [("a/alpha.md", Z), ("b/beta.md", O)]
        assert dc2_digest(pairs) == DC2_WORKED

    def test_dc4_worked_example(self):
        # core_aggregate.worked_example / AMD-27 - normative.
        pairs = [("BOOT.md", Z), ("core/VERSION", O)]
        assert dc4_digest(pairs) == DC4_WORKED

    def test_worked_examples_from_first_principles(self):
        # Reproduce both digests with hashlib over hand-built preimages,
        # proving the constants above are the grammar's own consequence.
        pre2 = (f"a/alpha.md {Z}\n" f"b/beta.md {O}\n").encode("utf-8")
        assert hashlib.sha256(pre2).hexdigest() == DC2_WORKED
        pre4 = (f"BOOT.md {Z}\n" f"core/VERSION {O}\n").encode("utf-8")
        assert hashlib.sha256(pre4).hexdigest() == DC4_WORKED

    def test_input_order_carries_no_meaning(self):
        # record_order: 'the order of rows in the registry table is not used
        # and carries no meaning' - reversed input, same digest.
        assert dc2_digest([("b/beta.md", O), ("a/alpha.md", Z)]) == DC2_WORKED
        assert dc4_digest([("core/VERSION", O), ("BOOT.md", Z)]) == DC4_WORKED

    def test_octet_order_shorter_prefix_first(self):
        # 'ascending by the UTF-8 octet sequence ... shorter prefix first':
        # b"a" < b"a-x" < b"a/x" (0x2D < 0x2F) < b"a0x".
        pairs = [("a/x", Z), ("a", Z), ("a0x", Z), ("a-x", Z)]
        expected = (f"a {Z}\n" f"a-x {Z}\n" f"a/x {Z}\n" f"a0x {Z}\n").encode()
        assert aggregate_preimage(pairs) == expected

    def test_preimage_exact_bytes_no_header_no_bom(self):
        pre = aggregate_preimage([("p", Z)])
        assert pre == b"p " + Z.encode() + b"\n"
        assert not pre.startswith(b"\xef\xbb\xbf")

    def test_duplicate_path_halts_dc2(self):
        # frozen_set_aggregate.duplicate_path: registry defect, DC-2 undefined.
        with pytest.raises(DuplicatePathError):
            dc2_digest([("a.md", Z), ("a.md", O)])

    def test_duplicate_path_halts_dc4(self):
        # core_aggregate.duplicate_path: build defect, build halts.
        with pytest.raises(DuplicatePathError):
            dc4_digest([("BOOT.md", Z), ("BOOT.md", Z)])

    def test_empty_registry_dc2_declared_value(self):
        # frozen_set_aggregate.empty_registry - SHA-256 of the empty preimage.
        assert dc2_digest([]) == DC2_EMPTY

    def test_empty_set_dc4_never_lawful(self):
        # core_aggregate.empty_set: 'never lawful - a failed build'.
        with pytest.raises(EmptySetError):
            dc4_digest([])

    def test_truncated_digest_prohibited(self):
        # output: '64 lowercase hexadecimal characters ... truncation is
        # prohibited' - a short or uppercase digest must be refused.
        with pytest.raises(ValueError):
            dc4_digest([("BOOT.md", "abc123")])
        with pytest.raises(ValueError):
            dc4_digest([("BOOT.md", "A" * 64)])  # uppercase hex is not lawful

    def test_self_exclusion_is_callers_duty_but_grammar_accepts_any_path(self):
        # Self-exclusion (DC-2: aggregate not part of its own preimage; DC-4:
        # the lock contributes no record) is enforced at set construction -
        # certified in the coverage tests; the grammar itself is path-agnostic.
        assert dc4_digest([("core/MANIFEST.lock", Z)])  # grammar-level: computes


# --------------------------------------------------------------------------
# DC-5: SHA-256 over raw octets, no normalisation; sidecar convention.
# --------------------------------------------------------------------------

class TestDc5:
    def test_fips_abc_vector(self):
        # release_digest.worked_example: 0x61 0x62 0x63 -> published vector.
        assert dc5_digest(b"abc") == DC5_ABC

    def test_no_normalisation_of_any_kind(self):
        # CRLF, BOM, trailing whitespace must all be hashed as-is.
        raw = b"\xef\xbb\xbfa\r\nb  \n\n"
        assert dc5_digest(raw) == hashlib.sha256(raw).hexdigest()
        assert dc5_digest(raw) != dc5_digest(b"a\nb\n")

    def test_sidecar_exact_convention(self):
        # recording: '<digest> <SP> <SP> <archive-name> <LF>' - sha256sum
        # text convention, exactly two spaces, one terminal LF.
        text = dc5_sidecar_text(DC5_ABC, "aief-1.0.0-mechanical.tar")
        assert text == f"{DC5_ABC}  aief-1.0.0-mechanical.tar\n"

    def test_sidecar_refuses_truncated_digest(self):
        with pytest.raises(ValueError):
            dc5_sidecar_text("ba7816bf", "x.tar")
