"""Repository path resolution and the read-only write guard.

Actor provenance: software.software-engineer - S-2026-08-08-07.

ENGINEERING.md section 4: `.ai/` is generated (never hand-edited), `framework/`
and `spec/` are FROZEN partitions; `src/` and `tests/` are the PR-controlled
tooling area. This dispatch additionally prohibits any write into `.ai/**`,
`framework/**` or `spec/**` and any write of a canonical `core/MANIFEST.lock`;
`assert_write_allowed` enforces that mechanically for every writer in this
package.
"""

from __future__ import annotations

from pathlib import Path


class WriteGuardViolation(RuntimeError):
    """Raised when a write would land in a read-only partition."""


def find_repo_root(start: Path | None = None) -> Path:
    """Locate the repository root: the directory containing `.ai/BOOT.md` and
    `framework/framework.manifest.json` (ENGINEERING.md section 4 layout)."""
    p = (start or Path(__file__)).resolve()
    if p.is_file():
        p = p.parent
    for candidate in (p, *p.parents):
        if (candidate / ".ai" / "BOOT.md").is_file() and (
            candidate / "framework" / "framework.manifest.json"
        ).is_file():
            return candidate
    raise FileNotFoundError(
        "repository root not found (no .ai/BOOT.md + framework/framework.manifest.json)"
    )


#: Repository-root-relative prefixes this package must never write into.
READONLY_PREFIXES = (".ai", "framework", "spec")


def assert_write_allowed(target: Path, repo_root: Path) -> Path:
    """Refuse any write into a read-only partition. Returns the resolved path.

    Also refuses any path whose final component is `MANIFEST.lock` outside the
    build output area: the canonical lock is emitted only by an authorized
    Stage 6 execution (generation_order[6].barrier: 'MANIFEST.lock is emitted
    only here'; OQ-14 keeps that execution unauthorized today).
    """
    resolved = target.resolve()
    root = repo_root.resolve()
    try:
        rel = resolved.relative_to(root)
    except ValueError:
        # Outside the repository (e.g. a temp dir in tests): allowed.
        return resolved
    parts = rel.parts
    if parts and parts[0] in READONLY_PREFIXES:
        raise WriteGuardViolation(
            f"write refused: {rel.as_posix()} is inside a read-only partition "
            f"({parts[0]}/)"
        )
    if resolved.name == "MANIFEST.lock" and (not parts or parts[0] != "build"):
        raise WriteGuardViolation(
            "write refused: canonical MANIFEST.lock emission is not authorized "
            "(OQ-14); preview locks live under build/stage6/"
        )
    return resolved
