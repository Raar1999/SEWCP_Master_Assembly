"""Developer sanity tests: covered-set resolution (AMD-39), pin preview,
ustar audit, write guard, lock serialisation order, live-tree V-24.

Actor provenance: software.software-engineer - S-2026-08-08-07.
"""

import json
import sys
import tarfile
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from aief_stage6.binding import load_binding, render_pin_update
from aief_stage6.coverage import CoverageDefect, hash_covered_set, resolve_covered_set
from aief_stage6.digests import dc4_digest
from aief_stage6.distributable import audit_paths, build_archive, ustar_fits
from aief_stage6.manifest import load_manifest
from aief_stage6.paths import WriteGuardViolation, assert_write_allowed, find_repo_root
from aief_stage6.preconditions import check_v24

REPO = find_repo_root(Path(__file__).resolve())


@pytest.fixture(scope="module")
def manifest():
    return load_manifest(REPO)


@pytest.fixture(scope="module")
def binding():
    return load_binding(REPO)


def test_covered_set_composition(manifest, binding):
    covered = resolve_covered_set(manifest, binding)
    # AMD-39 for this instance: three software.* tokens contribute exactly
    # the three enabled-role agent artifacts; mechanical.* and undotted
    # tokens contribute nothing beyond terms already covered.
    assert "core/profiles/software/agents/AGT-software-engineer.md" in covered.paths
    assert "core/profiles/software/agents/AGT-test-engineer.md" in covered.paths
    assert "core/profiles/software/agents/AGT-platform-engineer.md" in covered.paths
    # Self-exclusion and unhashed partitions.
    assert "core/MANIFEST.lock" not in covered.paths
    assert not any(p.startswith(("project/", "adapters/")) for p in covered.paths)
    # No non-selected-profile artifact beyond the three agent files
    # (scope_limit: PROFILE.md / lifecycle stay uncovered and unemitted).
    assert "core/profiles/software/PROFILE.md" not in covered.paths
    assert not any(p.startswith("core/profiles/research/") for p in covered.paths)
    # Deterministic count for this manifest + BINDING: 3 roots + 53 core +
    # 16 mechanical + 3 enabled-role = 75.
    assert len(covered.paths) == 75


def test_covered_set_hashes_and_dc4(manifest, binding):
    covered = resolve_covered_set(manifest, binding)
    pairs = hash_covered_set(covered, REPO)
    assert len(pairs) == 75
    digest = dc4_digest(pairs)
    assert len(digest) == 64
    # Determinism: a second resolution and hash yields the identical value.
    assert digest == dc4_digest(hash_covered_set(covered, REPO))


def test_unresolvable_enabled_agent_token_halts(manifest, binding):
    import dataclasses

    broken = dataclasses.replace(
        binding, enabled_agents=binding.enabled_agents + ("software.nonexistent",)
    )
    with pytest.raises(CoverageDefect):
        resolve_covered_set(manifest, broken)


def test_pin_preview_replaces_only_the_value(binding):
    dc4 = "e" * 64
    updated = render_pin_update(binding.text, dc4)
    assert dc4 in updated
    assert "PENDING-STAGE-6" not in updated
    # Single-line change, all other lines byte-identical.
    diff = [
        (a, b)
        for a, b in zip(binding.text.split("\n"), updated.split("\n"))
        if a != b
    ]
    assert len(diff) == 1 and diff[0][0].startswith("core_digest_pin:")


def test_write_guard_refuses_readonly_partitions():
    for target in (
        REPO / ".ai" / "project" / "BINDING.md",
        REPO / ".ai" / "core" / "MANIFEST.lock",
        REPO / "framework" / "x.json",
        REPO / "spec" / "x.md",
    ):
        with pytest.raises(WriteGuardViolation):
            assert_write_allowed(target, REPO)
    assert assert_write_allowed(REPO / "build" / "stage6" / "x", REPO)


def test_ustar_audit(manifest, binding):
    covered = resolve_covered_set(manifest, binding)
    audit = audit_paths([f".ai/{p}" for p in covered.paths] + [".ai/core/MANIFEST.lock"])
    assert audit.ok, audit.offending
    assert audit.max_len <= 100  # everything fits the plain name field today
    assert not ustar_fits("x" * 101 + "/" * 0)  # no split point
    assert ustar_fits(("p" * 150) + "/" + ("n" * 90))  # prefix/name split fits


def test_archive_deterministic_and_ustar(tmp_path, manifest, binding):
    covered = resolve_covered_set(manifest, binding)
    pairs = hash_covered_set(covered, REPO)
    lock_bytes = b'{"aggregate_digest": "preview"}\n'
    a1 = build_archive([p for p, _ in pairs], lock_bytes, REPO)
    a2 = build_archive([p for p, _ in pairs], lock_bytes, REPO)
    assert a1 == a2  # byte-identity across executions
    with tarfile.open(fileobj=io.BytesIO(a1)) as tar:
        names = tar.getnames()
        infos = tar.getmembers()
    assert names == sorted(names, key=lambda n: n.encode("utf-8"))
    assert names[-1] != names[0] and len(names) == 76  # 75 covered + lock
    assert all(i.mtime == 0 and i.uid == 0 and i.gid == 0 and i.uname == ""
               and i.gname == "" and i.mode == 0o644 for i in infos)


def test_v24_live_registry():
    # THE REGISTERED COUNT IS NOT PINNED HERE, BY RULING.
    #
    # This test previously asserted `registered == 28`. The freeze registry is
    # live, monotonically growing project state: it stood at 28, went to 29
    # with AIEF-AMD-013 and is owed a 30th row for AIEF-AMD-014. AMD-42
    # measurement_instant governs the same defect class - a property of the
    # tree at an instant is not a constant - so the pin is superseded by the
    # V-24 properties themselves, which is what validation[V-24].verifies
    # actually states: every registered path exists and its DC-1 equals the
    # registered digest; the recomputed DC-2 aggregate equals the recorded
    # one; every AMD-21 candidate is registered; no path is registered twice.
    result = check_v24(REPO)
    counts = result["counts"]
    assert counts["registered"] == counts["verified"], json.dumps(result, indent=2)
    assert counts["aggregate_match"] == 1, json.dumps(result, indent=2)
    assert result["status"] == "PASS", json.dumps(result, indent=2)
    # A registry that verifies nothing would satisfy the equalities above.
    assert counts["registered"] > 0
