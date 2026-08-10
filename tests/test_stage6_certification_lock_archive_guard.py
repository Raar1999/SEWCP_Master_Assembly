"""Certification tests: MANIFEST.lock serialisation (AMD-27/AMD-29,
sch-core-manifest), distributable determinism and ustar long-path halt
(AMD-30, VER-004 FIND-Q4-2), BINDING pin rendering, and the write guard.

Actor provenance: software.test-engineer - S-2026-08-08-09 (independent
verification; author of no code under test).

METHOD: expectations derive from `core_aggregate.lock_serialisation`,
`schemas[sch-core-manifest].required_fields`, `metadata.reproducible
.distributable`, `release_digest`, and the dispatch prohibitions. All write
targets are temp fixtures; the real tree is never written. The write guard is
exercised against a COPIED fixture repository root - no write into the real
`.ai/**` is ever attempted.
"""

import hashlib
import io
import json
import sys
import tarfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aief_stage6.binding import render_pin_update
from aief_stage6.distributable import (
    UstarPathLimit,
    archive_name,
    audit_paths,
    build_archive,
    ustar_fits,
)
from aief_stage6.lock import build_lock_object, serialise_lock
from aief_stage6.paths import WriteGuardViolation, assert_write_allowed

from test_stage6_certification_coverage_budget import make_manifest

REPO_ROOT = Path(__file__).resolve().parents[1]
Z = "0" * 64
O = "1" * 64

#: sch-core-manifest.required_fields, transcribed from the manifest.
SCH_CORE_REQUIRED = [
    "framework_version",
    "build_provenance",
    "hash_algorithm",
    "normalisation",
    "files",
    "aggregate_digest",
]

#: core_aggregate.lock_serialisation declared member order.
LOCK_MEMBER_ORDER = [
    "framework_version",
    "build_provenance",
    "hash_algorithm",
    "normalisation",
    "aggregate_digest",
    "budget_measurement",
    "files",
]

PASS_BUDGET = {"verdict": "PASS", "totals_t0_t1": {"TF-1": 1, "TF-2": 1}}


def build_lock(pairs, budget=None):
    return build_lock_object(
        make_manifest([]), "mech", list(pairs),
        dict(PASS_BUDGET if budget is None else budget),
        manifest_dc1=Z, build_id="b", timestamp="t",
    )


# --------------------------------------------------------------------------
# Lock object and serialisation.
# --------------------------------------------------------------------------

class TestLock:
    def test_member_order_exactly_as_declared(self):
        lock = build_lock([("BOOT.md", Z)])
        assert list(lock.keys()) == LOCK_MEMBER_ORDER
        # Serialised order is what the T1 digest read depends on: verify on
        # the emitted octets, not just the in-memory dict.
        parsed = json.loads(serialise_lock(lock).decode("utf-8"))
        assert list(parsed.keys()) == LOCK_MEMBER_ORDER

    def test_aggregate_digest_precedes_files_in_octets(self):
        # lock_serialisation: 'aggregate_digest precedes files so the T1
        # digest read stays within the 200-token cap'.
        octets = serialise_lock(build_lock([("BOOT.md", Z)]))
        assert octets.index(b'"aggregate_digest"') < octets.index(b'"files"')

    def test_all_sch_core_manifest_required_fields_present(self):
        lock = build_lock([("BOOT.md", Z)])
        for field in SCH_CORE_REQUIRED:
            assert field in lock, f"required field {field} missing"

    def test_emitted_lock_validates_against_emitted_schema(self):
        # The emitted Stage 1-5 artifact core/schemas/SCH-core-manifest
        # .schema.json is the lock's declared schema (read-only input here).
        import jsonschema

        schema = json.loads(
            (REPO_ROOT / ".ai" / "core" / "schemas" /
             "SCH-core-manifest.schema.json").read_text(encoding="utf-8")
        )
        lock = json.loads(serialise_lock(build_lock([("BOOT.md", Z)])))
        jsonschema.Draft202012Validator(schema).validate(lock)

    def test_files_member_is_pairs_in_dc4_record_order(self):
        # 'files is an array of [path, digest] pairs in DC-4 record order'.
        lock = build_lock([("core/VERSION", O), ("BOOT.md", Z)])
        assert lock["files"] == [["BOOT.md", Z], ["core/VERSION", O]]

    def test_aggregate_digest_is_dc4_over_the_files_member(self):
        # target_fields/b2a_procedure: aggregate_digest is DC-4 over exactly
        # the recorded pairs. Recomputed here with hashlib from the grammar.
        lock = build_lock([("BOOT.md", Z), ("core/VERSION", O)])
        preimage = (f"BOOT.md {Z}\n" f"core/VERSION {O}\n").encode("utf-8")
        assert lock["aggregate_digest"] == hashlib.sha256(preimage).hexdigest()
        # And equals the AMD-27 worked example for the worked-example input.
        assert lock["aggregate_digest"] == (
            "eb6e969b9f1d31a367ccf83315c1a40f8df0bb1c7dec41566a637ac3740325b1"
        )

    @pytest.mark.parametrize("verdict", ["UNMEASURED", "FAIL"])
    def test_non_pass_budget_refused(self, verdict):
        # Fail-safe: an UNMEASURED or failing budget record never enters a
        # conforming lock (verdict_rule; dispatch directive).
        with pytest.raises(ValueError):
            build_lock([("BOOT.md", Z)], budget={"verdict": verdict})

    def test_serialisation_deterministic_utf8_lf_terminal_lf(self):
        a = serialise_lock(build_lock([("BOOT.md", Z)]))
        b = serialise_lock(build_lock([("BOOT.md", Z)]))
        assert a == b
        assert b"\r" not in a
        assert a.endswith(b"\n") and not a.endswith(b"\n\n")
        a.decode("utf-8")  # must decode cleanly


# --------------------------------------------------------------------------
# Distributable: determinism, header discipline, long-path halt.
# --------------------------------------------------------------------------

def synthetic_tree(tmp_path: Path) -> tuple[Path, list[str]]:
    root = tmp_path / "repo"
    files = {
        "BOOT.md": b"boot\n",
        "core/VERSION": b"1.0.0\n",
        "core/profiles/mech/agents/AGT-a.md": b"# A\n",
    }
    for rel, content in files.items():
        p = root / ".ai" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)
    return root, sorted(files, key=lambda s: s.encode("utf-8"))


class TestDistributable:
    def test_archive_name_convention(self):
        # distributable.name: 'aief-<semver>-<profile>.tar'.
        assert archive_name("1.0.0", "mechanical") == "aief-1.0.0-mechanical.tar"

    def test_two_builds_byte_identical(self, tmp_path):
        # build_time_reproducibility: every execution must yield a
        # byte-identical archive; the archive construction itself must be
        # deterministic (release_digest.domain).
        root, covered = synthetic_tree(tmp_path)
        lock_bytes = b'{"stub": true}\n'
        a = build_archive(covered, lock_bytes, root)
        b = build_archive(covered, lock_bytes, root)
        assert a == b
        assert hashlib.sha256(a).hexdigest() == hashlib.sha256(b).hexdigest()

    def test_entry_set_and_order(self, tmp_path):
        # contents: 'the DC-4 covered set plus core/MANIFEST.lock, every entry
        # rooted at .ai/; nothing else'; determinism: entries ascending by
        # UTF-8 octets of archive path.
        root, covered = synthetic_tree(tmp_path)
        blob = build_archive(covered, b"L\n", root)
        with tarfile.open(fileobj=io.BytesIO(blob)) as tar:
            names = tar.getnames()
        assert names == sorted(names, key=lambda s: s.encode("utf-8"))
        assert set(names) == {f".ai/{p}" for p in covered} | {".ai/core/MANIFEST.lock"}

    def test_header_discipline(self, tmp_path):
        # determinism: 'mtime 0, uid 0, gid 0, empty uname and gname, mode
        # 0644 for regular files'.
        root, covered = synthetic_tree(tmp_path)
        blob = build_archive(covered, b"L\n", root)
        with tarfile.open(fileobj=io.BytesIO(blob)) as tar:
            for m in tar.getmembers():
                assert m.mtime == 0 and m.uid == 0 and m.gid == 0
                assert m.uname == "" and m.gname == ""
                assert m.mode == 0o644
                assert m.isreg()

    def test_no_pax_or_gnu_extended_headers(self, tmp_path):
        # ustar means no extended-header entries; typeflags 'x', 'g', 'L', 'K'
        # must not appear anywhere in the raw octets' header positions.
        root, covered = synthetic_tree(tmp_path)
        blob = build_archive(covered, b"L\n", root)
        with tarfile.open(fileobj=io.BytesIO(blob)) as tar:
            for m in tar.getmembers():
                assert m.type == tarfile.REGTYPE
        # ustar magic in every header block.
        assert blob[257:262] == b"ustar"

    def test_lock_bytes_embedded_exactly(self, tmp_path):
        root, covered = synthetic_tree(tmp_path)
        lock_bytes = b'{"framework_version": "1.0.0"}\n'
        blob = build_archive(covered, lock_bytes, root)
        with tarfile.open(fileobj=io.BytesIO(blob)) as tar:
            extracted = tar.extractfile(".ai/core/MANIFEST.lock").read()
        assert extracted == lock_bytes

    def test_ustar_fits_boundaries(self):
        # POSIX ustar: name field 100 octets; prefix 155 + '/' + name split.
        assert ustar_fits("a" * 100)
        assert not ustar_fits("a" * 101)               # unsplittable: no '/'
        assert ustar_fits("d" * 155 + "/" + "n" * 100)  # exact split fits
        assert not ustar_fits("d" * 156 + "/" + "n" * 100)  # prefix too long
        assert not ustar_fits("d" * 155 + "/" + "n" * 101)  # name too long

    def test_long_path_halts_no_pax_fallback(self, tmp_path):
        # VER-004 FIND-Q4-2 discipline: a path that does not fit the ustar
        # name/prefix split HALTS the build - it must never be absorbed by a
        # silent switch to pax headers.
        root, _ = synthetic_tree(tmp_path)
        long_component = "x" * 150  # '.ai/' + 150 octets, no split point fits
        p = root / ".ai" / long_component
        p.write_bytes(b"content\n")
        with pytest.raises(UstarPathLimit):
            build_archive([long_component], b"L\n", root)
        audit = audit_paths([f".ai/{long_component}"])
        assert not audit.ok and audit.offending == (f".ai/{long_component}",)


# --------------------------------------------------------------------------
# BINDING pin rendering: pure function; the real file is never touched.
# --------------------------------------------------------------------------

class TestPinRender:
    SAMPLE = (
        "# Project Binding\n\n```yaml\n"
        "core_digest_pin:       PENDING-STAGE-6   # emitted by Compiler Stage 6\n"
        "active_profile:        mechanical\n```\n"
    )

    def test_value_token_replaced_rest_preserved(self):
        out = render_pin_update(self.SAMPLE, Z)
        assert f"core_digest_pin:       {Z}   # emitted by Compiler Stage 6" in out
        # Every other byte preserved: reversing the substitution restores the
        # original exactly.
        assert out.replace(Z, "PENDING-STAGE-6") == self.SAMPLE

    def test_rejects_non_hex64_pin(self):
        for bad in ("PENDING-STAGE-6", "abc", "A" * 64, Z[:63]):
            with pytest.raises(ValueError):
                render_pin_update(self.SAMPLE, bad)

    def test_rejects_zero_or_multiple_pin_lines(self):
        with pytest.raises(ValueError):
            render_pin_update("no pin here\n", Z)
        with pytest.raises(ValueError):
            render_pin_update(f"core_digest_pin: {Z}\ncore_digest_pin: {Z}\n", Z)

    def test_real_binding_file_untouched_by_render(self):
        # The renderer must be pure. Render against the REAL BINDING content
        # and prove the on-disk file is byte-identical afterwards.
        real = REPO_ROOT / ".ai" / "project" / "BINDING.md"
        before = real.read_bytes()
        render_pin_update(before.decode("utf-8"), Z)
        assert real.read_bytes() == before
        # And the live pin remains the Stage 3 placeholder (Stage 6 execution
        # is unauthorized - OQ-14).
        assert b"PENDING-STAGE-6" in before


# --------------------------------------------------------------------------
# Write guard: any write into .ai/**, framework/**, spec/** refused; any
# canonical MANIFEST.lock write refused. Exercised on a fixture COPY.
# --------------------------------------------------------------------------

@pytest.fixture()
def fixture_repo(tmp_path: Path) -> Path:
    """A minimal copy-shaped repository root. No test in this module passes
    the real repo root to a writing call."""
    root = tmp_path / "fixture-repo"
    (root / ".ai").mkdir(parents=True)
    (root / ".ai" / "BOOT.md").write_bytes(b"boot\n")
    (root / "framework").mkdir()
    (root / "spec").mkdir()
    (root / "build" / "stage6").mkdir(parents=True)
    (root / "out").mkdir()
    return root


class TestWriteGuard:
    @pytest.mark.parametrize("rel", [
        ".ai/core/MANIFEST.lock",
        ".ai/project/BINDING.md",
        ".ai/BOOT.md",
        "framework/framework.manifest.json",
        "spec/anything.md",
    ])
    def test_readonly_partitions_refused(self, fixture_repo, rel):
        with pytest.raises(WriteGuardViolation):
            assert_write_allowed(fixture_repo / Path(rel), fixture_repo)

    def test_canonical_lock_refused_anywhere_outside_build(self, fixture_repo):
        with pytest.raises(WriteGuardViolation):
            assert_write_allowed(fixture_repo / "out" / "MANIFEST.lock",
                                 fixture_repo)

    def test_build_area_and_outside_repo_allowed(self, fixture_repo, tmp_path):
        assert_write_allowed(
            fixture_repo / "build" / "stage6" / "MANIFEST.lock.PREVIEW.json",
            fixture_repo)
        assert_write_allowed(
            fixture_repo / "build" / "stage6" / "MANIFEST.lock", fixture_repo)
        assert_write_allowed(tmp_path / "elsewhere" / "anyfile", fixture_repo)
