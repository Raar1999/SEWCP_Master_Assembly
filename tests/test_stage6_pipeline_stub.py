"""Developer sanity test: full emission pipeline with STUB tokenizer families.

Actor provenance: software.software-engineer - S-2026-08-08-07.

The stubs exist ONLY to exercise the emission mechanics (lock serialisation
order, archive determinism, AMD-33 double-run byte-compare) inside a test.
They are never offered as TF-1/TF-2: production measurement requires the
declared artifacts (tokenizer_families.pin_value_rule), and the driver's
default path stays FAIL-SAFE-BLOCKED until the platform-engineer provisions
them. Outputs go to a pytest tmp_path, never to build/stage6/.
"""

import io
import json
import sys
import tarfile
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aief_stage6.build import run
from aief_stage6.paths import find_repo_root
from aief_stage6.tokenizers import TokenizerProbe

REPO = find_repo_root(Path(__file__).resolve())


@dataclass
class _StubFamily:
    family_id: str
    scale: int
    artifact_name: str = "stub"
    artifact_pin: str = "0" * 64

    def count(self, text: str) -> int:
        return len(text) // self.scale + 1


def _stub_probe() -> TokenizerProbe:
    return TokenizerProbe(
        families=[_StubFamily("TF-1-STUB", 100), _StubFamily("TF-2-STUB", 120)],
        missing=[],
    )


def test_full_pipeline_with_stub_families(tmp_path):
    outcome = run(repo_root=REPO, out_root=tmp_path, tokenizers=_stub_probe(),
                  runs=2)
    assert outcome.status == "OK", outcome.notes
    assert outcome.covered_count == 75
    assert outcome.dc5_release_digest and len(outcome.dc5_release_digest) == 64

    run1, run2 = tmp_path / "preview" / "run1", tmp_path / "preview" / "run2"
    name = "aief-1.0.0-mechanical.tar"
    for fname in ("MANIFEST.lock.PREVIEW.json", name, f"{name}.sha256"):
        assert (run1 / fname).read_bytes() == (run2 / fname).read_bytes()

    lock = json.loads((run1 / "MANIFEST.lock.PREVIEW.json").read_text("utf-8"))
    # sch-core-manifest required members all present.
    for member in ("framework_version", "build_provenance", "hash_algorithm",
                   "normalisation", "files", "aggregate_digest"):
        assert member in lock
    # core_aggregate.lock_serialisation member order.
    assert list(lock) == ["framework_version", "build_provenance",
                          "hash_algorithm", "normalisation", "aggregate_digest",
                          "budget_measurement", "files"]
    assert lock["aggregate_digest"] == outcome.dc4_aggregate
    assert len(lock["files"]) == 75
    paths = [p for p, _ in lock["files"]]
    assert paths == sorted(paths, key=lambda p: p.encode("utf-8"))
    assert "core/MANIFEST.lock" not in paths  # self-exclusion
    assert lock["budget_measurement"]["verdict"] == "PASS"

    # Sidecar binds the archive octets (DC-5 recording convention).
    sidecar = (run1 / f"{name}.sha256").read_text("utf-8")
    digest, _, listed = sidecar.rstrip("\n").partition("  ")
    assert listed == name and digest == outcome.dc5_release_digest

    # Archive: 75 covered + the lock, ustar, deterministic headers.
    with tarfile.open(run1 / name) as tar:
        members = tar.getmembers()
        assert len(members) == 76
        lock_member = tar.extractfile(".ai/core/MANIFEST.lock").read()
    assert lock_member == (run1 / "MANIFEST.lock.PREVIEW.json").read_bytes()

    # BINDING pin preview carries the DC-4 aggregate.
    preview = (tmp_path / "preview" / "BINDING.md.PREVIEW").read_text("utf-8")
    assert outcome.dc4_aggregate in preview
    # The real BINDING is untouched (PENDING-STAGE-6 still pinned).
    real = (REPO / ".ai" / "project" / "BINDING.md").read_text("utf-8")
    assert "PENDING-STAGE-6" in real
