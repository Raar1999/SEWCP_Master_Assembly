"""CLI: `python -m aief_approval verify` / `states`.

Exit 0 when every chain holds, 1 otherwise. The non-zero exit is what makes this
a standing check rather than a report: `OI-V-02` records that a property with no
check is a property that drifts.
"""

from __future__ import annotations

import sys
from pathlib import Path

from .chain import State, ecr_approval_states, verify


def _repo() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".ai" / "project").is_dir():
            return parent
    return Path.cwd()


def cmd_verify(repo: Path, argv: list[str]) -> int:
    report = verify(repo, argv or None)
    for failure in report.failures:
        print(f"FAIL   {failure}")
    for subject_path in sorted(report.chains):
        chain = report.chains[subject_path]
        status = "PASS" if chain.ok else "FAIL"
        head = chain.tree_digest[:12] + "..." if chain.tree_digest else "ABSENT"
        print(f"{status}   {subject_path}  tree={head}  approvals={len(chain.approvals)}")
        for approval in chain.approvals:
            state = chain.states.get(approval.approval_id, State.VOID)
            marker = "  " if state is not State.VOID else "!!"
            ecr = f" [{approval.ecr}]" if approval.ecr else ""
            print(f"     {marker} {approval.approval_id}{ecr}: {state.value}")
        for note in chain.notes:
            print(f"     note {note}")
        for failure in chain.failures:
            print(f"     FAIL {failure}")
    print()
    print("APPROVAL CHAINS OK" if report.ok else "APPROVAL CHAIN INTEGRITY FAILED")
    return 0 if report.ok else 1


def cmd_states(repo: Path, _: list[str]) -> int:
    states = ecr_approval_states(repo)
    if not states:
        print("no ECR-bound approvals found")
        return 1
    worst = 0
    for ecr in sorted(states):
        approval_id, state = states[ecr]
        ok = state in (State.LIVE, State.SUPERSEDED_VALID)
        worst = max(worst, 0 if ok else 1)
        print(f"{'PASS' if ok else 'FAIL'}   {ecr}  {approval_id}  {state.value}")
    return worst


COMMANDS = {"verify": cmd_verify, "states": cmd_states}


def main(argv: list[str]) -> int:
    if not argv or argv[0] not in COMMANDS:
        print(f"usage: python -m aief_approval {{{'|'.join(COMMANDS)}}} [paths...]")
        return 2
    return COMMANDS[argv[0]](_repo(), argv[1:])


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
