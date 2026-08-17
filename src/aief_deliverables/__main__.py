"""`python -m aief_deliverables` - check the deliverable register against the tree."""

from __future__ import annotations

from pathlib import Path

from .check import SUBTREES, check


def _repo() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".ai" / "project").is_dir():
            return parent
    return Path.cwd()


def main() -> int:
    rep = check(_repo())

    print(f"registered deliverables: {len(rep.rows)}")
    print(f"subtrees checked:        {', '.join(SUBTREES)}")
    print(f"octets accounted for:    {rep.total_bytes}")
    print()

    for p in rep.missing:
        print(f"MISSING       {p}  - registered, absent from the tree")
    for p, want, got in rep.size_mismatch:
        print(f"SIZE          {p}  - register {want}, disk {got}")
    for p, want, got in rep.digest_mismatch:
        print(f"DIGEST        {p}")
        print(f"              register {want}")
        print(f"              disk     {got}")
    for p in rep.unregistered:
        print(f"UNREGISTERED  {p}  - present in the tree, named by no row")

    if rep.ok:
        print(f"DELIVERABLES OK - {len(rep.rows)} registered, {len(rep.rows)} reproduce, "
              "0 unregistered; the agreement is bi-directional")
        return 0

    n = (len(rep.missing) + len(rep.size_mismatch)
         + len(rep.digest_mismatch) + len(rep.unregistered))
    print(f"\n{n} DELIVERABLE DEFECT(S)")
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
