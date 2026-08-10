"""Deterministic distributable archive per AMD-30 and DC-5 sidecar per AMD-28.

Actor provenance: software.software-engineer - S-2026-08-08-07.

metadata.reproducible.distributable declares:
  - format: 'uncompressed POSIX ustar tar archive'
  - name: 'aief-<semver>-<profile>.tar'
  - contents: 'exactly the emitted install set for the selected profile: the
    DC-4 covered set plus core/MANIFEST.lock, every entry rooted at .ai/;
    nothing else'
  - determinism: 'entries sorted ascending by the UTF-8 octet sequence of the
    archive path; mtime 0, uid 0, gid 0, empty uname and gname, mode 0644 for
    regular files and 0755 for directories, no extended headers beyond those
    pax requires for long paths'

VER-004 FIND-Q4-2 (ustar long-path verification) is implemented as a HALTING
pre-check: any archive path that does not fit the POSIX ustar name(100)/
prefix(155) split halts the build with the measured lengths - this build
never emits pax extended headers, so an unsplittable path must halt rather
than silently change header format.

Open Question (recorded, minimal deterministic choice): the contents clause
says 'nothing else', while the determinism clause declares a directory mode.
This build emits regular-file entries only (strict 'nothing else' reading);
the 0755 directory mode rule is then vacuous. Flagged for A4 in the report.
"""

from __future__ import annotations

import io
import tarfile
from dataclasses import dataclass
from pathlib import Path

USTAR_NAME_MAX = 100
USTAR_PREFIX_MAX = 155


class UstarPathLimit(RuntimeError):
    """Halting defect per VER-004 FIND-Q4-2 discipline: no pax fallback."""


@dataclass(frozen=True)
class PathAudit:
    max_len: int
    max_path: str
    offending: tuple[str, ...]  # paths that do not fit ustar name/prefix

    @property
    def ok(self) -> bool:
        return not self.offending


def ustar_fits(name: str) -> bool:
    """True when `name` fits a POSIX ustar header: full name <= 100 octets, or
    splittable at a '/' into prefix <= 155 and name <= 100 octets."""
    encoded = name.encode("utf-8")
    if len(encoded) <= USTAR_NAME_MAX:
        return True
    # Try every split point; ustar stores prefix + '/' + name.
    for i, ch in enumerate(encoded):
        if ch == 0x2F:  # '/'
            prefix, rest = encoded[:i], encoded[i + 1 :]
            if len(prefix) <= USTAR_PREFIX_MAX and 0 < len(rest) <= USTAR_NAME_MAX:
                return True
    return False


def audit_paths(archive_paths: list[str]) -> PathAudit:
    max_len, max_path = 0, ""
    offending = []
    for p in archive_paths:
        n = len(p.encode("utf-8"))
        if n > max_len:
            max_len, max_path = n, p
        if not ustar_fits(p):
            offending.append(p)
    return PathAudit(max_len=max_len, max_path=max_path, offending=tuple(offending))


def archive_name(semver: str, profile: str) -> str:
    """distributable.name: 'aief-<semver>-<profile>.tar'."""
    return f"aief-{semver}-{profile}.tar"


def build_archive(
    covered_paths: list[str],
    lock_bytes: bytes,
    repo_root: Path,
) -> bytes:
    """Emit the archive octets deterministically.

    Entry set: the DC-4 covered set plus core/MANIFEST.lock, each archive
    path '.ai/' + files[].path (contents: 'every entry rooted at .ai/').
    Entry order: 'ascending by the UTF-8 octet sequence of the archive path'.
    Headers: mtime 0, uid 0, gid 0, empty uname/gname, mode 0644 (regular
    files; this build emits no directory entries - see module Open Question).
    Covered-file content is the working-tree octets; V-25 (a passed AMD-31
    precondition) guarantees those are already in DC-1 normal form, so the
    archive is platform-independent.
    """
    entries: list[tuple[str, bytes]] = [
        (f".ai/{p}", (repo_root / ".ai" / Path(p)).read_bytes())
        for p in covered_paths
    ]
    entries.append((".ai/core/MANIFEST.lock", lock_bytes))
    entries.sort(key=lambda e: e[0].encode("utf-8"))

    audit = audit_paths([name for name, _ in entries])
    if not audit.ok:
        raise UstarPathLimit(
            "archive path(s) exceed the POSIX ustar name/prefix limits and pax "
            "headers are not emitted - build halts: "
            + ", ".join(audit.offending)
            + f" (max path {audit.max_len} octets: {audit.max_path})"
        )

    buffer = io.BytesIO()
    with tarfile.open(
        fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT, encoding="utf-8"
    ) as tar:
        for name, content in entries:
            info = tarfile.TarInfo(name=name)
            info.size = len(content)
            info.mtime = 0
            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            info.mode = 0o644
            info.type = tarfile.REGTYPE
            tar.addfile(info, io.BytesIO(content))
    return buffer.getvalue()
