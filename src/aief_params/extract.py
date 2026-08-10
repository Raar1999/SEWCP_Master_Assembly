"""The SEWCP-200 parameter master, read from the package it is declared in.

`ECR-D-012` is not the authority here; `VER-016` F-06 is. Step 6.02 of
`implementation/01_SEWCP-200_Cooling_Plate/SEWCP-200_CAD_Implementation_Package.md`
instructs the modeller to import `params/generated/SEWCP-200.csv`, and that file
had never been generated - the directory held only `.gitkeep`. The modeller then
necessarily falls back to typing section 3 by hand, which is exactly where the
30/150/270 transcription this session spent its time removing entered in the
first place.

**Section 3 remains the master.** This module derives the CSV from it and
`python -m aief_params check` fails when the two disagree, so the derivation is
checked rather than being a second place to edit. Nothing here interprets a
value, converts a unit or supplies a missing one: a parameter absent from
section 3 is absent from the CSV.
"""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from pathlib import Path

PACKAGE = (
    "implementation/01_SEWCP-200_Cooling_Plate/"
    "SEWCP-200_CAD_Implementation_Package.md"
)
CSV_PATH = "params/generated/SEWCP-200.csv"
HEADER = ("Name", "Unit", "Expression", "Comment")

_SECTION = re.compile(r"^##\s+(3\.\d+)\s+(.*?)\s*$")
_STOP = re.compile(r"^#\s+4\s")
_START = re.compile(r"^#\s+3\s+Parameters\s*$")
_SEP = re.compile(r"^\|[\s:|-]+\|$")
# `10.0` (H8)  ->  expression 10.0, note H8
_ANNOTATED = re.compile(r"^(.*?)\s*\(([^)]*)\)\s*$")
# ang_kin_top_1/2/3  ->  stem ang_kin_top_, suffixes 1 2 3
_MULTI = re.compile(r"^(.*?)((?:\d/)+\d)$")


@dataclass(frozen=True)
class Parameter:
    name: str
    unit: str
    expression: str
    comment: str
    section: str


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _clean(cell: str) -> str:
    """Strip the markdown a table cell carries, never the content."""
    text = cell.replace("**", "").replace("`", "")
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return text.strip()


def _split_annotation(expression: str) -> tuple[str, str]:
    m = _ANNOTATED.match(expression)
    if not m or not m.group(1):
        return expression, ""
    return m.group(1).strip(), m.group(2).strip()


def parse(text: str) -> list[Parameter]:
    """Every named parameter declared in section 3, in document order."""
    out: list[Parameter] = []
    section = ""
    inside = False
    for raw in text.replace("\r\n", "\n").split("\n"):
        if _START.match(raw):
            inside = True
            continue
        if not inside:
            continue
        if _STOP.match(raw):
            break
        heading = _SECTION.match(raw)
        if heading:
            section = f"{heading.group(1)} {_clean(heading.group(2))}".strip()
            continue
        if not raw.startswith("|") or _SEP.match(raw):
            continue
        cells = _cells(raw)
        if not cells or cells[0].strip().strip("|") in ("Name", ""):
            continue
        name = _clean(cells[0])
        if not name or " " in name:
            continue

        if len(cells) >= 6:  # 3.1 - 3.5
            description = _clean(cells[1])
            expression = _clean(cells[2])
            unit = _clean(cells[3]) or "mm"
            intent = _clean(cells[4])
        elif len(cells) == 3:  # 3.6, tolerance reference
            description = "Tolerance reference, non-driving"
            expression = _clean(cells[1])
            unit = "mm"
            intent = _clean(cells[2])
        else:
            continue

        expression, annotation = _split_annotation(expression)
        comment = "; ".join(p for p in (description, intent, annotation) if p)

        multi = _MULTI.match(name)
        if multi and "/" in expression:
            stem = multi.group(1)
            suffixes = multi.group(2).split("/")
            values = [v.strip() for v in expression.split("/")]
            if len(values) == len(suffixes):
                for suffix, value in zip(suffixes, values):
                    out.append(
                        Parameter(f"{stem}{suffix}", unit, value, comment, section)
                    )
                continue
        out.append(Parameter(name, unit, expression, comment, section))
    return out


def read_package(repo: Path) -> list[Parameter]:
    return parse((repo / PACKAGE).read_text(encoding="utf-8"))


def to_csv(parameters: list[Parameter]) -> str:
    """Fusion 360 'Change Parameters -> Import' order: Name, Unit, Expression, Comment.

    Written with LF endings and no byte-order mark so the file is byte-identical
    on every platform, which is what lets `check` be a standing check rather than
    a diff of line endings.
    """
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(HEADER)
    for p in parameters:
        writer.writerow([p.name, p.unit, p.expression, p.comment])
    return buffer.getvalue()


def duplicates(parameters: list[Parameter]) -> list[str]:
    seen: set[str] = set()
    return sorted({p.name for p in parameters if p.name in seen or seen.add(p.name)})
