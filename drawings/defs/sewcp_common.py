"""Shared loaders for the SEWCP drawing definitions.

Dimension provenance sources used by every definition:
  - "spec/NN <ID>"            a frozen critical-dimension row
  - "parameter:<name>"        the component's requirement-package parameter
                              (itself spec-anchored in the package)
  - "observed:<run> <what>"   verified Fusion observation
  - "decision:<note>"         a recorded engineering decision

The critical-dimensions tables are parsed from the frozen spec volumes at
generation time - never retyped - so the drawing's table is the spec's
table by construction.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from aief_cad.expr import evaluate  # noqa: E402

SPEC = ROOT / "spec"
IMPL = ROOT / "implementation"
RUNS = ROOT / "cad" / "runs"

TODAY = "2026-08-11"


def load_params(*package_paths: str | Path) -> dict[str, float]:
    """Resolve every parameter of the given requirement packages to a
    float, in declaration order, so later packages may reference earlier
    ones."""
    env: dict[str, float] = {}
    for path in package_paths:
        body = json.loads(Path(path).read_text(encoding="utf-8"))
        rows = body.get("parameters") or []
        if not rows and body.get("parameters_from"):
            csv_path = (Path(path).parent / body["parameters_from"]).resolve()
            import csv as _csv
            with open(csv_path, newline="", encoding="utf-8-sig") as fh:
                for r in _csv.DictReader(fh):
                    rows.append({"name": r["Name"],
                                 "expression": r["Expression"]})
        for p in rows:
            try:
                env[p["name"]] = evaluate(str(p["expression"]), env)
            except Exception:
                pass
    return env


_DIM_ROW = re.compile(r"^\|\s*([A-Z]{2,3}-D\d+[a-z]?)\s*\|")


def spec_dim_table(volume_filename: str,
                   prefix: str | None = None) -> list[tuple[str, ...]]:
    """Extract (id, name, nominal, tolerance) rows from a frozen volume's
    critical-dimension tables, verbatim apart from markdown emphasis."""
    rows: list[tuple[str, ...]] = []
    for line in (SPEC / volume_filename).read_text(encoding="utf-8").splitlines():
        m = _DIM_ROW.match(line)
        if not m:
            continue
        if prefix and not m.group(1).startswith(prefix):
            continue
        cells = [c.strip().replace("**", "").replace("*", "")
                 for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4:
            rows.append((cells[0], cells[1][:44], cells[2][:20], cells[3][:22]))
    return rows


def observed_bodies(run_id: str) -> list[dict]:
    r = json.loads((RUNS / run_id / "run.json").read_text(encoding="utf-8"))
    return r["attempts"][-1]["observed_model"].get("bodies", [])


def system_runs() -> dict[str, str]:
    si = json.loads((RUNS / "SYSTEM_INTERFACES.json").read_text(encoding="utf-8"))
    return si["runs"]


STANDARD_NOTES = [
    "INTERPRET PER ASME Y14.5-2018. UNITS mm. UNLESS NOTED: X.X ±0.2, X.XX ±0.05.",
    "BREAK ALL EDGES 0.2-0.4 UNLESS NOTED. NO BURRS.",
    "VENT ALL BLIND HOLES IN VACUUM-EXPOSED PARTS PER DR-6 (spec/00).",
    "PROVENANCE: EVERY DIMENSION TRACES PER THE SIDECAR "
    "PROVENANCE FILE OF THIS DRAWING (AIEF).",
]
