"""Budget measurement record per AMD-29 and the V-09 measurement rule.

Actor provenance: software.software-engineer - S-2026-08-08-07.

metadata.reproducible.budget_measurement_record declares the record's home
(the `budget_measurement` member of core/MANIFEST.lock) and content:

  1. 'per-file token count under each family for every file carrying a
     non-null token_cap in tiers T0 and T1'
  2. 'per-family T0 plus T1 totals and the governing maximum per file and in
     aggregate'
  3. 'verdict against every per-file cap and against the 6000 aggregate
     ceiling'
  4. 'tokenizer artifact identifiers with their raw-octet SHA-256 pin values'
  5. 'measurement timestamp and the Stage 6 build identifier'

verdict_rule: 'any per-file cap breach or aggregate ceiling breach under
either family halts the build ...; the aggregate comparison is the charged
comparison of aggregate_ceiling_charge'. 'The maximum governs' -
AIEF-FRZ-001 section 1.8 via tokenizer_families.governing_rule.

lock_self_measurement (AMD-45, disposing TCR-001 F1): the lock's row is
emitted DEFERRED-SELF-MEASURED with null counts; 'the deferral is keyed on
the path core/MANIFEST.lock and on nothing else - in particular never on
absence from the tree, because any other measured file absent from the tree
is a build defect that must halt rather than defer' (BudgetSourceMissing).

aggregate_ceiling_charge (AMD-51, disposing VER-007 FIND-Q7-3): whenever
that row is deferred, files[manifest-lock].token_cap is added to each
per-family total before the ceiling comparison; the charge is the declared
cap, never an estimate. Per-file rows and the post-serialisation lock cap
check are unaffected.

FAIL-SAFE: with no tokenizers in hand the record is UNMEASURED and lock
emission is refused (BudgetUnmeasured) - counts are never fabricated.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .manifest import Manifest
from .tokenizers import TokenizerProbe

AGGREGATE_CEILING = 6000  # version.boot_ceiling_tokens; V-09 'at most 6000'

# AMD-45: the deferral is keyed on THIS PATH and on nothing else. The value is
# files[manifest-lock].path - the one measured artifact this build emits.
LOCK_PATH = "core/MANIFEST.lock"
LOCK_DEFERRED_VERDICT = "DEFERRED-SELF-MEASURED"


class BudgetUnmeasured(RuntimeError):
    """Raised when measurement is impossible; the build must not emit a
    conforming lock (fail-safe directive; tokenizer_families.pin_value_rule -
    a value not measured from the artifact in hand is never asserted)."""


class BudgetBreach(RuntimeError):
    """budget_measurement_record.verdict_rule: any cap or ceiling breach under
    either family halts the build."""


class BudgetSourceMissing(RuntimeError):
    """AMD-45: a measured file absent from the tree is a build defect that
    halts. Only core/MANIFEST.lock defers, and on its path, never on
    absence - the fail-open TCR-001 recorded as F1."""


@dataclass(frozen=True)
class BudgetResult:
    record: dict[str, Any]  # the budget_measurement lock member


def _capped_t0_t1_files(manifest: Manifest) -> list[dict[str, Any]]:
    return [
        f
        for f in manifest.files
        if f.get("tier") in ("T0", "T1") and f.get("token_cap") is not None
    ]


def measure(
    manifest: Manifest,
    repo_root: Path,
    tokenizers: TokenizerProbe,
    *,
    build_id: str,
    timestamp: str,
) -> BudgetResult:
    """Produce the budget_measurement member and enforce the verdict rule.

    `timestamp` and `build_id` are captured once per release run and passed
    in, so that the >=2 executions of build_time_reproducibility serialise
    byte-identical locks (AMD-33: every execution must yield an identical
    distributable; a per-execution timestamp would defeat that by
    construction).
    """
    if not tokenizers.available:
        raise BudgetUnmeasured(
            "budget UNMEASURED - declared tokenizer families not in hand: "
            + "; ".join(tokenizers.missing)
        )

    ai_root = repo_root / ".ai"
    per_file: list[dict[str, Any]] = []
    totals: dict[str, int] = {t.family_id: 0 for t in tokenizers.families}
    breaches: list[str] = []

    lock_charge = 0  # AMD-51: files[manifest-lock].token_cap, or 0 if no row

    for f in _capped_t0_t1_files(manifest):
        path = f["path"]
        cap = f["token_cap"]
        if path == LOCK_PATH:
            # AMD-45: keyed on the PATH, never on absence - the lock is
            # emitted by this build, so no on-tree copy is the text this
            # record describes; `measure_text` caps the emitted octets.
            per_file.append(
                {"path": path, "tier": f["tier"], "token_cap": cap, "counts": None,
                 "governing": None, "verdict": LOCK_DEFERRED_VERDICT}
            )
            lock_charge = cap
            continue
        fs_path = ai_root / Path(path)
        if not fs_path.is_file():
            # AMD-45, closing TCR-001 F1: a measured file absent from the tree
            # is a build defect. It halts; it is never silently deferred.
            raise BudgetSourceMissing(
                f"{path}: measured file absent from the tree - build halts "
                f"(AMD-45: only {LOCK_PATH} defers, and it defers on its path)"
            )
        text = fs_path.read_text(encoding="utf-8")
        counts = {t.family_id: t.count(text) for t in tokenizers.families}
        governing = max(counts.values())  # 'the maximum governs'
        verdict = "PASS" if governing <= cap else "FAIL"
        if verdict == "FAIL":
            breaches.append(f"{path}: governing {governing} > cap {cap}")
        for fam, n in counts.items():
            totals[fam] += n
        per_file.append(
            {"path": path, "tier": f["tier"], "token_cap": cap,
             "counts": counts, "governing": governing, "verdict": verdict}
        )

    # AMD-51: the charged comparison. The cap is an upper bound on the
    # omitted quantity, so the gate over-states and never under-states.
    charged_totals = {fam: n + lock_charge for fam, n in totals.items()}
    aggregate_governing = max(charged_totals.values())
    aggregate_verdict = "PASS" if aggregate_governing <= AGGREGATE_CEILING else "FAIL"
    if aggregate_verdict == "FAIL":
        breaches.append(
            f"aggregate: charged governing {aggregate_governing} "
            f"(measured {max(totals.values())} + lock charge {lock_charge}) "
            f"> ceiling {AGGREGATE_CEILING}"
        )
    if breaches:
        raise BudgetBreach("budget verdict FAIL - build halts: " + "; ".join(breaches))

    record: dict[str, Any] = {
        "tokenizer_families": [
            {
                "id": t.family_id,
                "artifact": t.artifact_name,
                "artifact_pin_sha256_raw_octets": t.artifact_pin,
            }
            for t in tokenizers.families
        ],
        "per_file": per_file,
        "totals_t0_t1": totals,
        # AMD-51: recorded so the comparison is reconstructible.
        # `totals_t0_t1` stays the measured domain;
        # `aggregate_governing_maximum` is the value compared.
        "aggregate_ceiling_charge": lock_charge,
        "charged_totals_t0_t1": charged_totals,
        "aggregate_governing_maximum": aggregate_governing,
        "aggregate_ceiling": AGGREGATE_CEILING,
        "verdict": "PASS",
        "measurement_timestamp": timestamp,
        "stage6_build_id": build_id,
    }
    return BudgetResult(record=record)


def measure_text(
    tokenizers: TokenizerProbe, text: str, cap: int, label: str
) -> dict[str, Any]:
    """Post-emission cap check for text emitted by this build (the lock).

    core/MANIFEST.lock is itself a capped T1 file (files[manifest-lock],
    token_cap 200), but its content contains the budget record - a count of
    the final lock inside the lock is a fixed point no construction defines.
    Resolved normatively by AMD-45 (lock_self_measurement): the emitted lock
    octets are measured under both families against the 200 cap AFTER
    serialisation and before the archive is built, outside the record, and a
    breach halts the build exactly as an in-record breach does
    (budget_measurement_record.verdict_rule). AMD-51 leaves this check
    unaffected; the cap is separately charged to the aggregate comparison in
    `measure`.
    """
    counts = {t.family_id: t.count(text) for t in tokenizers.families}
    governing = max(counts.values())
    if governing > cap:
        raise BudgetBreach(
            f"{label}: governing {governing} > cap {cap} - build halts"
        )
    return {"label": label, "counts": counts, "governing": governing, "cap": cap,
            "verdict": "PASS"}


def unmeasured_record(tokenizers: TokenizerProbe, *, build_id: str, timestamp: str) -> dict[str, Any]:
    """The diagnostic (non-lock) record for the fail-safe path. Explicitly
    marked UNMEASURED; never placed in a conforming MANIFEST.lock."""
    return {
        "verdict": "UNMEASURED",
        "reason": tokenizers.missing,
        "consequence": (
            "no conforming core/MANIFEST.lock may be emitted; V-09 is "
            "BLOCKED pending platform-engineer tokenizer provisioning"
        ),
        "measurement_timestamp": timestamp,
        "stage6_build_id": build_id,
    }
