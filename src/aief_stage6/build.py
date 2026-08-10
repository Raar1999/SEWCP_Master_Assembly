"""Stage 6 build driver - preview-only in this dispatch.

Actor provenance: software.software-engineer - S-2026-08-08-07.

Pipeline per generation_order[6] and its barrier (AMD-25/AMD-31/AMD-33):

  1. AMD-31 preconditions (compile-time class except V-10) against the
     manifest and the Stage 1-5 tree; any non-PASS halts before emission.
  2. DC-4 covered-set resolution (AMD-39) and hashing (DC-1).
  3. ustar path audit (halting; VER-004 FIND-Q4-2 discipline).
  4. Budget measurement under TF-1/TF-2 (AMD-26/AMD-29) - or the fail-safe
     halt with an UNMEASURED record when the families are not in hand.
  5. core/MANIFEST.lock (AMD-27 lock_serialisation) - PREVIEW path only.
  6. Distributable archive + DC-5 sidecar (AMD-30/AMD-28).
  7. BINDING pin preview (generation_order[6] pin write output; preview file,
     never the real .ai/project/BINDING.md in this dispatch).
  8. build_time_reproducibility (AMD-33): the whole emission pipeline runs
     N >= 2 times into separate directories; any byte divergence of
     distributable, lock or sidecar halts with diagnostics.

All outputs land under build/stage6/** and carry PREVIEW markers. Nothing is
written into .ai/**, framework/** or spec/** (paths.assert_write_allowed).
"""

from __future__ import annotations

import datetime as _dt
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import binding as binding_mod
from . import budget as budget_mod
from . import coverage as coverage_mod
from . import distributable as dist_mod
from . import lock as lock_mod
from . import preconditions as pre_mod
from .digests import dc1_digest, dc4_digest, dc5_digest, dc5_sidecar_text
from .manifest import load_manifest
from .paths import assert_write_allowed, find_repo_root
from .tokenizers import TokenizerProbe, probe


@dataclass
class BuildOutcome:
    status: str  # "OK" | "PRECONDITION-FAIL" | "FAIL-SAFE-BLOCKED" | "HALT"
    preconditions: list[dict[str, Any]] = field(default_factory=list)
    dc4_aggregate: str | None = None
    dc5_release_digest: str | None = None
    covered_count: int = 0
    max_archive_path_octets: int = 0
    max_archive_path: str = ""
    notes: list[str] = field(default_factory=list)


def _write(path: Path, data: bytes, repo_root: Path) -> None:
    assert_write_allowed(path, repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _emit_once(
    out_dir: Path,
    repo_root: Path,
    manifest,
    covered_pairs: list[tuple[str, str]],
    selected_profile: str,
    tokenizers: TokenizerProbe,
    build_id: str,
    timestamp: str,
) -> dict[str, bytes]:
    """One deterministic emission: lock, archive, sidecar. Returns the three
    artifacts' octets keyed by filename (for the AMD-33 byte-compare)."""
    budget = budget_mod.measure(
        manifest, repo_root, tokenizers, build_id=build_id, timestamp=timestamp
    )
    manifest_dc1 = dc1_digest(manifest.raw)
    lock_obj = lock_mod.build_lock_object(
        manifest, selected_profile, covered_pairs, budget.record,
        manifest_dc1=manifest_dc1, build_id=build_id, timestamp=timestamp,
    )
    lock_bytes = lock_mod.serialise_lock(lock_obj)
    # Post-emission cap check on the lock itself (see budget.measure_text).
    budget_mod.measure_text(
        tokenizers, lock_bytes.decode("utf-8"),
        manifest.files_by_id["manifest-lock"]["token_cap"], "core/MANIFEST.lock",
    )

    name = dist_mod.archive_name(manifest.semver, selected_profile)
    archive = dist_mod.build_archive(
        [p for p, _ in covered_pairs], lock_bytes, repo_root
    )
    sidecar = dc5_sidecar_text(dc5_digest(archive), name).encode("utf-8")

    _write(out_dir / "MANIFEST.lock.PREVIEW.json", lock_bytes, repo_root)
    _write(out_dir / name, archive, repo_root)
    _write(out_dir / f"{name}.sha256", sidecar, repo_root)
    return {"MANIFEST.lock.PREVIEW.json": lock_bytes, name: archive,
            f"{name}.sha256": sidecar}


def run(repo_root: Path | None = None, out_root: Path | None = None,
        spiece_model_path: Path | None = None, runs: int = 2,
        tokenizers: TokenizerProbe | None = None) -> BuildOutcome:
    """Execute the Stage-6-only increment in preview mode.

    `tokenizers` may be injected (test/certification harnesses); by default
    the declared families are probed from the environment.
    """
    repo_root = repo_root or find_repo_root()
    out_root = out_root or repo_root / "build" / "stage6"
    outcome = BuildOutcome(status="OK")

    manifest = load_manifest(repo_root)
    binding = binding_mod.load_binding(repo_root)
    tokenizers = tokenizers if tokenizers is not None else probe(spiece_model_path)

    # 1. AMD-31 preconditions.
    checks = pre_mod.run_preconditions(manifest, binding, repo_root, tokenizers)
    outcome.preconditions = checks
    _write(
        out_root / "preconditions.json",
        (json.dumps({"note": "PREVIEW - AMD-31 precondition run, "
                             "software.software-engineer - S-2026-08-08-07",
                     "checks": checks}, indent=2) + "\n").encode("utf-8"),
        repo_root,
    )

    # 2. Covered set + DC-4 (computable regardless; DC-4 is a pure function
    # of files[], BINDING and the tree - AMD-39 determinism clause).
    covered = coverage_mod.resolve_covered_set(manifest, binding)
    covered_pairs = coverage_mod.hash_covered_set(covered, repo_root)
    outcome.covered_count = len(covered_pairs)
    outcome.dc4_aggregate = dc4_digest(covered_pairs)

    # 3. ustar path audit over the would-be archive entry set.
    entry_paths = [f".ai/{p}" for p, _ in covered_pairs] + [".ai/core/MANIFEST.lock"]
    audit = dist_mod.audit_paths(entry_paths)
    outcome.max_archive_path_octets = audit.max_len
    outcome.max_archive_path = audit.max_path
    if not audit.ok:
        outcome.status = "HALT"
        outcome.notes.append("ustar path limit exceeded: " + ", ".join(audit.offending))
        return outcome

    # AMD-31 gate: any FAIL halts before any preview emission artifact.
    hard_failures = [c for c in checks if c["status"] == "FAIL"]
    if hard_failures:
        outcome.status = "PRECONDITION-FAIL"
        outcome.notes += [f"{c['id']} FAIL" for c in hard_failures]
        return outcome

    # BINDING pin preview (DC-4 exists even when the lock cannot be emitted).
    pin_preview = binding_mod.render_pin_update(binding.text, outcome.dc4_aggregate)
    _write(out_root / "preview" / "BINDING.md.PREVIEW",
           pin_preview.encode("utf-8"), repo_root)

    if not tokenizers.available:
        # Fail-safe path: no conforming lock, no archive, no sidecar.
        timestamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        record = budget_mod.unmeasured_record(
            tokenizers, build_id="preview-failsafe", timestamp=timestamp)
        _write(out_root / "preview" / "FAILSAFE_BUDGET_UNMEASURED.json",
               (json.dumps(record, indent=2) + "\n").encode("utf-8"), repo_root)
        outcome.status = "FAIL-SAFE-BLOCKED"
        outcome.notes.append(
            "tokenizer families not in hand; lock/distributable/DC-5 emission "
            "refused (budget UNMEASURED, counts never fabricated)")
        return outcome

    # 5-8. Full emission, executed `runs` times (AMD-33: at least twice),
    # with one run-fixed build id and timestamp so byte-identity is possible.
    timestamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    build_id = f"stage6-preview-{timestamp}"
    emissions: list[dict[str, bytes]] = []
    for i in range(1, max(2, runs) + 1):
        emissions.append(_emit_once(
            out_root / "preview" / f"run{i}", repo_root, manifest,
            covered_pairs, covered.selected_profile, tokenizers,
            build_id, timestamp,
        ))
    first = emissions[0]
    for i, emission in enumerate(emissions[1:], start=2):
        for key, blob in first.items():
            if emission.get(key) != blob:
                outcome.status = "HALT"
                outcome.notes.append(
                    f"build_time_reproducibility violation: run1/{key} != run{i}/{key}"
                    " - non-reproducible digest halts the build (AMD-33)")
        if outcome.status == "HALT":
            return outcome

    name = dist_mod.archive_name(manifest.semver, covered.selected_profile)
    outcome.dc5_release_digest = dc5_digest(first[name])
    return outcome
