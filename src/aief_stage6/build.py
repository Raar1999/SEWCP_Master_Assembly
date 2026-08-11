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


@dataclass(frozen=True)
class Authorization:
    """The OQ-14 record a canonical Stage 6 execution must carry.

    `OQ-14` reserves Stage 6 execution to the human owner: *"Stage 6 does not
    execute without explicit human authorization, independent of every
    specification ruling"*. That authorization is not a flag an agent may set
    for itself, so it is carried as evidence: **who** authorized, **when**, and
    the **instruction verbatim**. All three are required and are written into
    the run record; an incomplete record is refused before any canonical byte
    is written.

    This type does not decide OQ-14 and cannot. It records that the owner did,
    and makes the record travel with the build that relied on it.
    """

    authority: str        # who authorized - the roleId, e.g. "human-owner"
    recorded_at: str      # when, YYYY-MM-DD
    instruction: str      # the authorizing words, verbatim, not paraphrased

    def __post_init__(self) -> None:
        missing = [f for f in ("authority", "recorded_at", "instruction")
                   if not str(getattr(self, f)).strip()]
        if missing:
            raise ValueError(
                "Stage 6 authorization incomplete - missing "
                + ", ".join(missing)
                + ". OQ-14 requires explicit human authorization; a canonical "
                  "build carries the record or does not run"
            )

    def as_record(self) -> dict[str, str]:
        return {"authority": self.authority, "recorded_at": self.recorded_at,
                "instruction": self.instruction}


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
    mode: str = "PREVIEW"          # "PREVIEW" | "CANONICAL"
    canonical_writes: list[str] = field(default_factory=list)
    lock_prefix_measurement: dict[str, Any] | None = None


def _write(path: Path, data: bytes, repo_root: Path,
           canonical_stage6: bool = False) -> None:
    assert_write_allowed(path, repo_root, canonical_stage6=canonical_stage6)
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
    canonical: bool = False,
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
    # Post-serialisation cap check on the lock's BOOT-READ PREFIX - the
    # quantity AMD-54 declares the 200 cap bounds (see budget.measure_text
    # and lock.boot_read_prefix). The label names the measured region so no
    # report can be read as a whole-document count.
    prefix_measurement = budget_mod.measure_text(
        tokenizers, lock_mod.boot_read_prefix(lock_bytes.decode("utf-8")),
        manifest.files_by_id["manifest-lock"]["token_cap"],
        "core/MANIFEST.lock boot-read prefix",
    )

    name = dist_mod.archive_name(manifest.semver, selected_profile)
    archive = dist_mod.build_archive(
        [p for p, _ in covered_pairs], lock_bytes, repo_root
    )
    sidecar = dc5_sidecar_text(dc5_digest(archive), name).encode("utf-8")

    lock_file = "MANIFEST.lock" if canonical else "MANIFEST.lock.PREVIEW.json"
    _write(out_dir / lock_file, lock_bytes, repo_root)
    _write(out_dir / name, archive, repo_root)
    _write(out_dir / f"{name}.sha256", sidecar, repo_root)
    return {"lock": lock_bytes, name: archive, f"{name}.sha256": sidecar,
            "__prefix_measurement__": json.dumps(prefix_measurement,
                                                 sort_keys=True).encode("utf-8")}


def run(repo_root: Path | None = None, out_root: Path | None = None,
        spiece_model_path: Path | None = None, runs: int = 2,
        tokenizers: TokenizerProbe | None = None,
        authorization: Authorization | None = None) -> BuildOutcome:
    """Execute the Stage-6-only increment.

    `tokenizers` may be injected (test/certification harnesses); by default
    the declared families are probed from the environment.

    **Mode.** Without `authorization` this is the preview build: everything
    lands under `build/stage6/**` and not one byte of `.ai/`, `framework/` or
    `spec/` is written. With an `Authorization` - the OQ-14 record - the build
    additionally performs the two canonical writes `generation_order[6]`
    declares, and only those two: `.ai/core/MANIFEST.lock`, and the
    `core_digest_pin` field of `.ai/project/BINDING.md`.

    **The canonical writes happen last, and only after everything has passed.**
    Preconditions, the ustar audit, the budget verdict, the boot-read prefix
    cap check and the AMD-33 byte-identity comparison across >= 2 executions all
    complete first, into the preview tree. A canonical byte is written only
    against octets that have already been produced identically twice.
    """
    repo_root = repo_root or find_repo_root()
    out_root = out_root or repo_root / "build" / "stage6"
    outcome = BuildOutcome(status="OK",
                           mode="CANONICAL" if authorization else "PREVIEW")

    manifest = load_manifest(repo_root)
    binding = binding_mod.load_binding(repo_root)
    tokenizers = tokenizers if tokenizers is not None else probe(spiece_model_path)

    # 1. AMD-31 preconditions.
    checks = pre_mod.run_preconditions(manifest, binding, repo_root, tokenizers)
    outcome.preconditions = checks
    _write(
        out_root / "preconditions.json",
        (json.dumps({"note": f"{outcome.mode} - AMD-31 precondition run",
                     "authorization": (authorization.as_record()
                                       if authorization else None),
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
    # Rendered here in both modes: in CANONICAL mode this is the dry run of the
    # field write, and it is compared against the octets actually written.
    pin_preview = binding_mod.render_pin_update(binding.text, outcome.dc4_aggregate)
    _write(out_root / ("canonical" if authorization else "preview")
           / "BINDING.md.PREVIEW", pin_preview.encode("utf-8"), repo_root)

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
    build_id = ("stage6-" if authorization else "stage6-preview-") + timestamp
    run_root = out_root / ("canonical" if authorization else "preview")
    emissions: list[dict[str, bytes]] = []
    for i in range(1, max(2, runs) + 1):
        emissions.append(_emit_once(
            run_root / f"run{i}", repo_root, manifest,
            covered_pairs, covered.selected_profile, tokenizers,
            build_id, timestamp, canonical=authorization is not None,
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
    outcome.lock_prefix_measurement = json.loads(
        first["__prefix_measurement__"].decode("utf-8"))

    if authorization is None:
        return outcome

    # ------------------------------------------------------------------
    # Canonical emission. Reached only with an OQ-14 authorization record and
    # only after every check above has passed and the octets below have been
    # produced identically by >= 2 independent executions.
    # ------------------------------------------------------------------
    lock_bytes = first["lock"]
    _write(repo_root / ".ai" / "core" / "MANIFEST.lock", lock_bytes, repo_root,
           canonical_stage6=True)
    outcome.canonical_writes.append(".ai/core/MANIFEST.lock")

    # The pin write is a FIELD write into an already-emitted instance artifact
    # (generation_order[6].outputs), never a re-emission. render_pin_update
    # replaces the value token on the single core_digest_pin line and preserves
    # every other octet including the inline comment - binding_pin_write
    # (AMD-47), whose halt conditions render_pin_update raises on.
    pin_written = binding_mod.render_pin_update(binding.text, outcome.dc4_aggregate)
    _write(binding.path, pin_written.encode("utf-8"), repo_root,
           canonical_stage6=True)
    outcome.canonical_writes.append(".ai/project/BINDING.md")
    outcome.notes.append(
        f"CANONICAL emission under OQ-14 authorization recorded "
        f"{authorization.recorded_at} by {authorization.authority}: "
        f"core/MANIFEST.lock written, BINDING.core_digest_pin set to the DC-4 "
        f"aggregate. Boot step B2a is now satisfiable."
    )
    return outcome
