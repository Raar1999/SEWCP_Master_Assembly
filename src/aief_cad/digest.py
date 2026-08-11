"""Canonical serialisation and content digests.

Every artifact this layer emits is identified by the SHA-256 of a canonical
byte form, so a run can be replayed and compared without trusting any claim
written inside the artifact. This is the `LAW-10` construction - approval bound
to a content hash - applied to CAD commands, observations and verdicts.

Canonical form: UTF-8, sorted keys, no insignificant whitespace, `\\n` endings,
one terminal newline when written to a file. `float` is emitted through
`repr`-equivalent JSON so a value that round-trips in Python round-trips here.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

__all__ = ["canonical_json", "digest_of", "short"]


def canonical_json(obj: Any) -> bytes:
    """Serialise deterministically. The same object always yields the bytes."""
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest_of(data: bytes | str) -> str:
    """SHA-256, lowercase hex, prefixed so a bare hash is never mistaken for one."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def short(digest: str, n: int = 12) -> str:
    """First `n` hex characters, for human-readable logs only. Never compared."""
    return digest.split(":", 1)[-1][:n]
