"""DC-4 covered-set resolution per AIEF-AMD-012 AMD-39 (machine-followable form).

Actor provenance: software.software-engineer - S-2026-08-08-07.

Implements exactly the procedure of AIEF-AMD-012 section 'The Stage 6
implementation's covered-set procedure, machine-followable', as carried
normatively by framework.manifest.json core_aggregate.covers and
core_aggregate.enabled_role_coverage:

    S := selected profile (project/BINDING.md active_profile)
    C := { f in files[] | f.integrity == "hashed"
           and f.path != "core/MANIFEST.lock"
           and f is emitted for S per AMD-27:
               f.path in {BOOT.md, FRAMEWORK.md, README.md}
               or f.path starts with "core/" and not "core/profiles/"
               or f.path starts with "core/profiles/" + S + "/" }
    for each token t in project/BINDING.md enabled_agents:
        if t contains "." :
            (p, n) := t split at the first "."
            if p != S:
                f := files[] entry with path core/profiles/<p>/agents/AGT-<n>.md
                if absent or not hashed: HALT (coverage defect)
                C := C u { f }

The working tree is never an input to coverage (enabled_role_coverage
.determinism); a covered file absent from the tree is a halting coverage
failure, never a silent exclusion.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .binding import Binding
from .digests import dc1_digest
from .manifest import Manifest


class CoverageDefect(RuntimeError):
    """Halting defect per enabled_role_coverage.rule ('a token that resolves
    to no such entry is a coverage defect that halts the build') and
    .determinism (covered file absent from the tree halts)."""


@dataclass(frozen=True)
class CoveredSet:
    """The DC-4 covered set: `.ai/`-relative paths exactly as declared in
    files[].path (core_aggregate.record: '<path> is the emission path relative
    to .ai/ exactly as declared in files[].path, POSIX separators')."""

    selected_profile: str
    paths: tuple[str, ...]  # sorted ascending by UTF-8 octets of path


def resolve_covered_set(manifest: Manifest, binding: Binding) -> CoveredSet:
    selected = binding.active_profile
    covered: dict[str, dict] = {}

    def emitted_for_selected(path: str) -> bool:
        # AMD-27 emission clause, restated by AMD-39 term (i).
        if path in ("BOOT.md", "FRAMEWORK.md", "README.md"):
            return True
        if path.startswith("core/") and not path.startswith("core/profiles/"):
            return True
        if path.startswith(f"core/profiles/{selected}/"):
            return True
        return False

    for f in manifest.files:
        path = f["path"]
        if f.get("integrity") != "hashed":
            continue  # 'unhashed partitions (project, adapters) are never covered'
        if path == "core/MANIFEST.lock":
            continue  # core_aggregate.self_exclusion
        if emitted_for_selected(path):
            if path in covered:
                raise CoverageDefect(f"duplicate covered path in files[]: {path}")
            covered[path] = f

    # Term (ii): enabled-role agent artifacts, AMD-39 / enabled_role_coverage.rule.
    by_path = manifest.files_by_path
    for token in binding.enabled_agents:
        if "." not in token:
            continue  # undotted universal token adds nothing (AMD-39 point 2)
        profile, name = token.split(".", 1)
        if profile == selected:
            continue  # selected-profile token adds nothing (AMD-39 point 2)
        target = f"core/profiles/{profile}/agents/AGT-{name}.md"
        entry = by_path.get(target)
        if entry is None or entry.get("integrity") != "hashed":
            raise CoverageDefect(
                f"enabled_agents token {token!r} resolves to no hashed files[] "
                f"entry at {target!r} - coverage defect, build halts "
                f"(enabled_role_coverage.rule)"
            )
        covered.setdefault(target, entry)

    paths = tuple(sorted(covered, key=lambda p: p.encode("utf-8")))
    return CoveredSet(selected_profile=selected, paths=paths)


def hash_covered_set(
    covered: CoveredSet, repo_root: Path
) -> list[tuple[str, str]]:
    """Compute (path, DC-1) pairs over the working tree for the covered set.

    Halts on any covered file absent from the tree: 'an enabled-role artifact
    absent from the tree is a B2a coverage failure, halting, never a silent
    exclusion' (enabled_role_coverage.determinism); the same list-vs-tree
    discipline as the B2a procedure (core_aggregate.b2a_procedure).
    """
    ai_root = repo_root / ".ai"
    pairs: list[tuple[str, str]] = []
    missing: list[str] = []
    for path in covered.paths:
        fs_path = ai_root / Path(path)
        if not fs_path.is_file():
            missing.append(path)
            continue
        pairs.append((path, dc1_digest(fs_path.read_bytes())))
    if missing:
        raise CoverageDefect(
            "covered-scope file(s) absent from the tree - build halts: "
            + ", ".join(missing)
        )
    return pairs
