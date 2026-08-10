"""CLI: `python -m aief_params [emit|check]`.

`check` exits non-zero when the generated CSV does not reproduce from section 3
of the CAD package. That non-zero exit is the point: `OI-V-02` records that a
property with no check is a property that drifts, and a parameter master
duplicated into a second file is the most drift-prone shape in this repository.
"""

from __future__ import annotations

import sys
from pathlib import Path

from .extract import CSV_PATH, duplicates, read_package, to_csv


def _repo() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".ai" / "project").is_dir():
            return parent
    return Path.cwd()


def _normalise(text: str) -> str:
    """CRLF and lone CR to LF, as DC-1 does, so a checkout cannot fail the check."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _integrity(parameters) -> list[str]:
    problems = [f"duplicate parameter name: {n}" for n in duplicates(parameters)]
    for p in parameters:
        if not p.expression:
            problems.append(f"{p.name}: no expression in section 3")
        if p.expression.upper() == "UNSPECIFIED":
            problems.append(
                f"{p.name}: section 3 still reads UNSPECIFIED - a HOLD that was "
                f"declared discharged is not"
            )
        # Closed set, not a guess: section 3 declares mm and deg throughout, plus
        # kg on cp_mass_max, which is a check-only limit rather than a driving
        # dimension. A unit outside this set means section 3 gained something the
        # emitter has never been shown, and that is worth stopping for.
        if p.unit not in ("mm", "deg", "kg"):
            problems.append(
                f"{p.name}: unit {p.unit!r} is outside the declared set mm/deg/kg"
            )
    return problems


def cmd_emit(repo: Path) -> int:
    parameters = read_package(repo)
    problems = _integrity(parameters)
    for problem in problems:
        print(f"FAIL   {problem}")
    if problems:
        print("\nPARAMETER EXPORT REFUSED")
        return 1
    target = repo / CSV_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(to_csv(parameters).encode("utf-8"))
    print(f"wrote {CSV_PATH}  {len(parameters)} parameters")
    return 0


def cmd_check(repo: Path) -> int:
    parameters = read_package(repo)
    problems = _integrity(parameters)
    target = repo / CSV_PATH
    if not target.is_file():
        problems.append(f"{CSV_PATH}: absent - step 6.02 imports a file that does not exist")
    else:
        # Compare the DC-1-NORMALISED content, which is how everything else in
        # this repository is compared, and for the same reason: `core.autocrlf`
        # rewrites the working tree on checkout. A raw byte comparison here made
        # `check` fail after a stash round-trip that changed nothing but line
        # endings. `.gitattributes` pins this file to LF so the artifact Fusion
        # imports is stable; this comparison is what makes the check survive a
        # checkout that ignores it.
        expected = _normalise(to_csv(parameters))
        actual = _normalise(target.read_bytes().decode("utf-8-sig"))
        if actual != expected:
            problems.append(
                f"{CSV_PATH}: does not reproduce from section 3 of the package - "
                f"regenerate with `python -m aief_params emit`"
            )
    for problem in problems:
        print(f"FAIL   {problem}")
    print()
    if problems:
        print("PARAMETER MASTER DIVERGED")
        return 1
    print(f"PARAMETERS OK   {len(parameters)} derived from section 3")
    return 0


COMMANDS = {"emit": cmd_emit, "check": cmd_check}


def main(argv: list[str]) -> int:
    command = argv[0] if argv else "check"
    if command not in COMMANDS:
        print(f"usage: python -m aief_params {{{'|'.join(COMMANDS)}}}")
        return 2
    return COMMANDS[command](_repo())


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
