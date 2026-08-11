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


#: The only two paths a canonical Stage 6 execution may write, and it may write
#: them only when it carries an authorization record. Both are declared outputs
#: of generation_order[6]: `core/MANIFEST.lock` is the stage's product, and the
#: `core_digest_pin` line of `project/BINDING.md` is its pin write. The list is
#: exhaustive by construction - authorization widens the guard by exactly these
#: two entries and by nothing else, so an authorized build cannot reach any
#: other byte of `.ai/`, `framework/` or `spec/`.
CANONICAL_STAGE6_WRITES = (
    ".ai/core/MANIFEST.lock",
    ".ai/project/BINDING.md",
)


def assert_write_allowed(
    target: Path, repo_root: Path, *, canonical_stage6: bool = False
) -> Path:
    """Refuse any write into a read-only partition. Returns the resolved path.

    Also refuses any path whose final component is `MANIFEST.lock` outside the
    build output area: the canonical lock is emitted only by an authorized
    Stage 6 execution (generation_order[6].barrier: 'MANIFEST.lock is emitted
    only here').

    `canonical_stage6` is set **only** by a `build.run` call carrying an
    `Authorization` record, and it widens the guard by exactly the two paths of
    `CANONICAL_STAGE6_WRITES`. It is not a bypass: every other path in every
    read-only partition is refused exactly as before, and the default is
    unchanged, so a caller that does not present an authorization cannot write
    a canonical byte by accident or by omission.

    The reason the guard exists at all is `OQ-14` - the human owner's
    reservation of Stage 6 execution authority. `OQ-14` is not decided by this
    function and cannot be; it is decided by the owner, recorded in an
    `Authorization`, and passed in.
    """
    resolved = target.resolve()
    root = repo_root.resolve()
    try:
        rel = resolved.relative_to(root)
    except ValueError:
        # Outside the repository (e.g. a temp dir in tests): allowed.
        return resolved
    parts = rel.parts
    rel_posix = rel.as_posix()
    if canonical_stage6 and rel_posix in CANONICAL_STAGE6_WRITES:
        return resolved
    if parts and parts[0] in READONLY_PREFIXES:
        raise WriteGuardViolation(
            f"write refused: {rel.as_posix()} is inside a read-only partition "
            f"({parts[0]}/)"
        )
    if resolved.name == "MANIFEST.lock" and (not parts or parts[0] != "build"):
        raise WriteGuardViolation(
            "write refused: canonical MANIFEST.lock emission requires an "
            "authorized Stage 6 execution (OQ-14); preview locks live under "
            "build/stage6/"
        )
    return resolved
