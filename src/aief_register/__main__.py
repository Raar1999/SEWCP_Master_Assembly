"""`python -m aief_register` - registers must not assert governed values."""

from __future__ import annotations

from pathlib import Path

from .check import check


def _repo() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".ai" / "project").is_dir():
            return parent
    return Path.cwd()


def main() -> int:
    rep = check(_repo())
    print(f"registers scanned:   {', '.join(rep.scanned)}")
    print(f"governing ledger seq: {rep.ledger_seq}")
    print(f"governing CURRENT results: {', '.join(sorted(rep.current_results)) or 'none'}")
    print()
    for f in rep.findings:
        print(f"STALE {f}")
    if rep.ok:
        print("REGISTERS OK - no register asserts a value another artifact governs")
        return 0
    print(f"\n{len(rep.findings)} STALE ASSERTION(S)")
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
