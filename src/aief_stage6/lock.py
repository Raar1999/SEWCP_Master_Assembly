"""core/MANIFEST.lock generation per sch-core-manifest and AMD-27/AMD-29.

Actor provenance: software.software-engineer - S-2026-08-08-07.

Serialisation is declared by core_aggregate.lock_serialisation:

    'core/MANIFEST.lock is UTF-8 JSON conforming to sch-core-manifest,
    member order framework_version, aggregate_digest, build_provenance,
    hash_algorithm, normalisation, budget_measurement, files;
    aggregate_digest precedes files so the T1 digest read stays within the
    200-token cap declared on files[manifest-lock]; files is an array of
    [path, digest] pairs in DC-4 record order'

AMD-55 (AIEF-AMD-015, disposing ECR-D-014) moved aggregate_digest from
fifth position to second. At the fifth position the boot-read prefix
carried build_provenance - two 64-character digests plus the run-scoped
build_id and timestamp - and measured 291 tokens under TF-2 against the
200 cap, varying with the length of a free-form identifier. At the second
position the prefix is framework_version and aggregate_digest alone: 69
tokens, with no run-scoped octet inside it.

sch-core-manifest (.ai/core/schemas/SCH-core-manifest.schema.json) requires
framework_version, build_provenance, hash_algorithm, normalisation, files,
aggregate_digest; budget_measurement is admitted by additionalProperties true
(budget_measurement_record.location).

Undeclared serialisation details (minimal deterministic choices, RECORDED as
Open Questions in the dispatch report, per the dispatching instruction):
  - JSON layout: 2-space indent, LF line endings, one terminal LF, no
    trailing whitespace, ensure_ascii false.
  - framework_version := version.semver; hash_algorithm :=
    metadata.reproducible.hash_algorithm; normalisation :=
    metadata.reproducible.normalisation (verbatim object).
  - build_provenance content is nowhere declared; chosen minimal
    deterministic member: source manifest DC-1, selected profile, stage
    number, build id, run-fixed timestamp.
"""

from __future__ import annotations

import json
from typing import Any

from .digests import dc4_digest
from .manifest import Manifest


def build_lock_object(
    manifest: Manifest,
    selected_profile: str,
    pairs: list[tuple[str, str]],
    budget_measurement: dict[str, Any],
    *,
    manifest_dc1: str,
    build_id: str,
    timestamp: str,
) -> dict[str, Any]:
    """Assemble the lock in the declared member order.

    `pairs` is the hashed covered set; `files` carries it as [path, digest]
    pairs in DC-4 record order (ascending UTF-8 octets of path) and
    `aggregate_digest` is DC-4 over exactly those records
    (core_aggregate.target_fields / .b2a_procedure).
    """
    ordered = sorted(pairs, key=lambda pd: pd[0].encode("utf-8"))
    aggregate = dc4_digest(ordered)
    if budget_measurement.get("verdict") != "PASS":
        # Fail-safe: an UNMEASURED or failing record never enters a
        # conforming lock (dispatch directive; verdict_rule).
        raise ValueError(
            "refusing to build a conforming lock without a PASS budget verdict"
        )
    # Insertion order IS emission order (lock_json_layout: 'Declared member
    # order is emission order and is never sorted'). AMD-55 order.
    return {
        "framework_version": manifest.semver,
        "aggregate_digest": aggregate,
        "build_provenance": {
            "source_manifest": "framework/framework.manifest.json",
            "source_manifest_dc1": manifest_dc1,
            "selected_profile": selected_profile,
            "compiler_stage": 6,
            "build_id": build_id,
            "timestamp": timestamp,
        },
        "hash_algorithm": manifest.reproducible["hash_algorithm"],
        "normalisation": manifest.reproducible["normalisation"],
        "budget_measurement": budget_measurement,
        "files": [[p, d] for p, d in ordered],
    }


def serialise_lock(lock: dict[str, Any]) -> bytes:
    """UTF-8 JSON, declared member order preserved (dict insertion order),
    LF, one terminal LF."""
    text = json.dumps(lock, ensure_ascii=False, indent=2)
    return (text + "\n").encode("utf-8")


_AGGREGATE_MEMBER = '"aggregate_digest"'


class LockPrefixUndefined(RuntimeError):
    """AMD-54: the measured quantity is the boot-read prefix. A lock with no
    aggregate_digest line has no such prefix, and a build must halt rather
    than fall back to measuring something else - a fallback is how a cap
    comes to bound a quantity nobody declared."""


def boot_read_prefix(lock_text: str) -> str:
    """The octets measured against files[manifest-lock].token_cap.

    lock_self_measurement, as amended by AIEF-AMD-015 AMD-54: 'the octets
    measured against the cap are the boot-read prefix, which is the
    serialised lock from its first octet through the terminal LF of the line
    carrying the aggregate_digest member, and not the whole document'.

    This is the region core_aggregate.lock_serialisation names when it gives
    the member ordering its reason, and after AMD-55 it contains no
    run-scoped value, so the quantity the cap bounds is determined by the
    specification rather than by the length of a build identifier.
    """
    idx = lock_text.find(_AGGREGATE_MEMBER)
    if idx < 0:
        raise LockPrefixUndefined(
            "no aggregate_digest member in the serialised lock - the boot-read "
            "prefix is undefined and the build halts (AMD-54)"
        )
    end = lock_text.find("\n", idx)
    if end < 0:
        raise LockPrefixUndefined(
            "aggregate_digest line is not LF-terminated - lock_json_layout "
            "requires one member per line with LF endings (AMD-54)"
        )
    return lock_text[: end + 1]
