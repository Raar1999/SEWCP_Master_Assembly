"""`python -m aief_gate` - print the LC-M04-EXIT disposition. Exit 0 iff C1-C7 all PASS."""

from __future__ import annotations

import sys
from pathlib import Path

from .criteria import evaluate


def _repo() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".ai" / "project").is_dir():
            return parent
    return Path.cwd()


def main() -> int:
    report = evaluate(_repo())
    print("LC-M04-EXIT — computed from repository bytes\n")
    for c in report.criteria:
        print(f"{c.id}  {c.verdict:<12} {c.title}")
        for line in c.evidence:
            print(f"       + {line}")
        for line in c.residue:
            print(f"       ! {line}")
    print()
    print(f"LC-M04 CAD-READY: {'YES' if report.ok else 'NO'}")
    return 0 if report.ok else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
