"""Bind `cad/DELIVERABLES.md` to the tree, in both directions.

The register was true and unreachable for four sessions: every digest in it
reproduced, and every file it named lived outside the repository on one
machine (`ECR-D-015`). A register that cannot be checked against the thing it
registers proves nothing; it only looks as though it does. This is the
standing check that the register and the tree agree - the `OI-V-02` lesson
applied to the deliverable set.

Both directions are checked because only one of them catches each failure:

  * register -> tree  catches a deleted, moved or rewritten deliverable
  * tree -> register  catches a deliverable added without being registered,
                      which is how an unverified artifact ships

Digests are raw SHA-256 over the file octets. NOT DC-1: DC-1 normalises line
endings and trailing whitespace, which is exactly right for a text artifact
whose meaning survives it and exactly wrong for a PDF. These files are
declared `-text` in `.gitattributes` for the same reason.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

REGISTER = Path("cad/DELIVERABLES.md")

#: The subtrees the register is exhaustive over. A file here is a deliverable.
SUBTREES = (
    "cad/exports/step",
    "cad/exports/stl",
    "cad/bom",
    "drawings/assembly",
    "drawings/parts",
)

#: Present because Fusion holds the parametric source of record and
#: `SEDEP-PMP-002` section 3.1 keeps it there. Not a deliverable of this tree.
EXCLUDED_SUFFIXES = (".f3d", ".f3z", ".f2d")

_ROW = re.compile(
    r"^\|\s*`(?P<path>[^`]+)`\s*\|\s*(?P<bytes>\d+)\s*\|\s*`(?P<sha>[0-9a-f]{64})`\s*\|\s*$"
)


@dataclass(frozen=True)
class Row:
    path: str
    size: int
    sha256: str


@dataclass
class Report:
    rows: list[Row] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)          # registered, not on disk
    size_mismatch: list[tuple[str, int, int]] = field(default_factory=list)
    digest_mismatch: list[tuple[str, str, str]] = field(default_factory=list)
    unregistered: list[str] = field(default_factory=list)     # on disk, not registered
    total_bytes: int = 0

    @property
    def ok(self) -> bool:
        return not (
            self.missing or self.size_mismatch or self.digest_mismatch or self.unregistered
        )


def parse_register(text: str) -> list[Row]:
    """Every table row of the register, in file order.

    A row is recognised by shape - backticked path, decimal byte count,
    64 hex digits - so prose, headings and the narrative tables around it are
    ignored without needing to be enumerated.
    """
    rows: list[Row] = []
    for line in text.splitlines():
        m = _ROW.match(line)
        if m:
            rows.append(Row(m["path"], int(m["bytes"]), m["sha"]))
    return rows


def on_disk(repo: Path) -> list[str]:
    """Every deliverable present in the tree, as repo-relative posix paths."""
    found: list[str] = []
    for sub in SUBTREES:
        base = repo / sub
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            if p.name == ".gitkeep" or p.suffix in EXCLUDED_SUFFIXES:
                continue
            found.append(p.relative_to(repo).as_posix())
    return found


def check(repo: Path) -> Report:
    register = repo / REGISTER
    if not register.is_file():
        raise FileNotFoundError(f"{REGISTER} is absent - nothing binds the deliverables")

    rep = Report(rows=parse_register(register.read_text(encoding="utf-8")))
    registered = {r.path for r in rep.rows}

    if len(registered) != len(rep.rows):
        seen: set[str] = set()
        for r in rep.rows:
            if r.path in seen:
                rep.digest_mismatch.append((r.path, "DUPLICATE ROW", r.sha256))
            seen.add(r.path)

    for row in rep.rows:
        f = repo / row.path
        if not f.is_file():
            rep.missing.append(row.path)
            continue
        octets = f.read_bytes()
        rep.total_bytes += len(octets)
        if len(octets) != row.size:
            rep.size_mismatch.append((row.path, row.size, len(octets)))
        actual = hashlib.sha256(octets).hexdigest()
        if actual != row.sha256:
            rep.digest_mismatch.append((row.path, row.sha256, actual))

    rep.unregistered = [p for p in on_disk(repo) if p not in registered]
    return rep
