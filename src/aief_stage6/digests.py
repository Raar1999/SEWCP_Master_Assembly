"""Digest constructions DC-1, DC-2/DC-4 (shared grammar) and DC-5.

Actor provenance: software.software-engineer - S-2026-08-08-07.

Every rule here is a restatement of `framework/framework.manifest.json`
`metadata.reproducible.digest_constructions`; the citation for each construct
is on the implementing function. DC-2 and DC-4 share one record grammar by
ruling ("One grammar for both set digests" - AIEF-AMD-010 AMD-27), so a single
`aggregate_digest` implements both.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class DuplicatePathError(ValueError):
    """digest_constructions.core_aggregate.duplicate_path / frozen_set_aggregate
    .duplicate_path: 'a path listed twice is a build defect; DC-4 is undefined
    for it and the build halts' (and the registry analogue for DC-2/V-24)."""


class EmptySetError(ValueError):
    """digest_constructions.core_aggregate.empty_set: 'never lawful - a build
    emitting zero covered files is a failed build, not an empty aggregate'.
    Applies to DC-4 only; DC-2 declares an explicit empty_registry value."""


def dc1_normalise(raw: bytes) -> bytes:
    """DC-1 normalisation, per digest_constructions.per_artifact.normalisation:

    'decode UTF-8 stripping any byte-order mark; convert CRLF and lone CR to
    LF; strip trailing whitespace from every line; remove trailing blank
    lines; append exactly one terminal LF; encode UTF-8'
    """
    text = raw.decode("utf-8")
    if text.startswith("\ufeff"):
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    if not lines:
        # Zero-content edge: no covered or registered artifact is empty; the
        # construction's line-wise wording does not define this case, so the
        # SHA-256 of the empty preimage is used and the case is flagged in the
        # dispatch report as an Open Question rather than silently decided.
        return b""
    return ("\n".join(lines) + "\n").encode("utf-8")


def dc1_digest(raw: bytes) -> str:
    """DC-1: 'SHA-256 [over] normalised file content', output '64 lowercase
    hexadecimal characters' (digest_constructions.per_artifact)."""
    return hashlib.sha256(dc1_normalise(raw)).hexdigest()


def aggregate_preimage(pairs: Iterable[tuple[str, str]]) -> bytes:
    """The shared DC-2/DC-4 preimage.

    Record grammar (core_aggregate.record, identical to frozen_set_aggregate
    .record): '<path> <SP> <digest> <LF>'; record order (.record_order):
    'ascending by the UTF-8 octet sequence of <path>, compared as unsigned
    octets, shorter prefix first'; preimage: 'the records concatenated in that
    order; no header, no trailer, no separator beyond each record terminal LF,
    no byte-order mark'; encoding UTF-8.
    """
    seen: set[str] = set()
    encoded: list[tuple[bytes, bytes]] = []
    for path, digest in pairs:
        if not _HEX64.match(digest):
            raise ValueError(
                f"digest for {path!r} is not 64 lowercase hex (truncation is "
                f"prohibited): {digest!r}"
            )
        if path in seen:
            raise DuplicatePathError(f"path listed twice: {path!r}")
        seen.add(path)
        encoded.append((path.encode("utf-8"), digest.encode("ascii")))
    encoded.sort(key=lambda item: item[0])
    return b"".join(p + b" " + d + b"\n" for p, d in encoded)


def aggregate_digest(pairs: Iterable[tuple[str, str]], *, allow_empty: bool) -> str:
    """DC-2 (allow_empty=True: frozen_set_aggregate declares empty_registry =
    SHA-256 of the empty preimage) or DC-4 (allow_empty=False: core_aggregate
    .empty_set is 'never lawful')."""
    preimage = aggregate_preimage(pairs)
    if not preimage and not allow_empty:
        raise EmptySetError("DC-4 over an empty covered set is never lawful")
    return hashlib.sha256(preimage).hexdigest()


def dc2_digest(pairs: Iterable[tuple[str, str]]) -> str:
    """DC-2, digest_constructions.frozen_set_aggregate."""
    return aggregate_digest(pairs, allow_empty=True)


def dc4_digest(pairs: Iterable[tuple[str, str]]) -> str:
    """DC-4, digest_constructions.core_aggregate."""
    return aggregate_digest(pairs, allow_empty=False)


def dc5_digest(raw: bytes) -> str:
    """DC-5, digest_constructions.release_digest: 'SHA-256 over the raw octets
    of the distributable archive exactly as emitted; no normalisation of any
    kind'."""
    return hashlib.sha256(raw).hexdigest()


def dc5_sidecar_text(digest: str, archive_name: str) -> str:
    """DC-5 sidecar, digest_constructions.release_digest.recording: 'a sidecar
    file <archive-name>.sha256 ... containing exactly <digest> <SP> <SP>
    <archive-name> <LF> in the sha256sum text convention'."""
    if not _HEX64.match(digest):
        raise ValueError("sidecar digest must be 64 lowercase hex")
    return f"{digest}  {archive_name}\n"
