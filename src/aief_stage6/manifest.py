"""Loader for `framework/framework.manifest.json` (read-only input).

Actor provenance: software.software-engineer - S-2026-08-08-07.

AIEF-AMD-025/generation_order[6].inputs declare Stage 6's inputs as the
verified Stage 1-5 tree, `metadata.reproducible` and `version`; this module
gives the rest of the package typed access to those sections plus the
`files[]`, `validation[]`, `laws`, `agents`, `profiles`, `schemas`,
`templates`, `dependencies`, `boot_sequence` and `generation_order` sections
the AMD-31 preconditions evaluate.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Manifest:
    """Parsed framework manifest plus its source path and raw octets."""

    path: Path
    raw: bytes
    data: dict[str, Any]

    @property
    def reproducible(self) -> dict[str, Any]:
        return self.data["metadata"]["reproducible"]

    @property
    def digest_constructions(self) -> dict[str, Any]:
        return self.reproducible["digest_constructions"]

    @property
    def files(self) -> list[dict[str, Any]]:
        return self.data["files"]

    @property
    def files_by_id(self) -> dict[str, dict[str, Any]]:
        return {f["id"]: f for f in self.files}

    @property
    def files_by_path(self) -> dict[str, dict[str, Any]]:
        return {f["path"]: f for f in self.files}

    @property
    def semver(self) -> str:
        return self.data["version"]["semver"]

    @property
    def validation(self) -> list[dict[str, Any]]:
        return self.data["validation"]

    @property
    def generation_order(self) -> list[dict[str, Any]]:
        return self.data["generation_order"]


def load_manifest(repo_root: Path) -> Manifest:
    path = repo_root / "framework" / "framework.manifest.json"
    raw = path.read_bytes()
    return Manifest(path=path, raw=raw, data=json.loads(raw.decode("utf-8")))
