"""Indentured BOM from the observed assembly, never from a typed list.

Sources, in authority order:
  1. The assembly run record's observed occurrences (actual Fusion state).
  2. The component registry (the ten verified designs, cad/DELIVERABLES.md).
  3. The frozen specification: material/finish per volume, the spec/00 §9
     fastener schedule (parsed verbatim), and volume-interface hardware.

Every row carries its provenance and its CAD state, and the builder
cross-checks quantity against the observed occurrence set, so the BOM can
neither contain a component that does not exist nor silently omit one the
assembly contains.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["BomRow", "build_bom", "write_bom_csv", "cross_check"]

ROOT = Path(__file__).resolve().parents[3]

#: Spec-authoritative material and finish per part number - each cited row
#: is the volume's §Materials statement; the model's observed material is
#: recorded alongside and any mismatch becomes a defect note, not a silent
#: substitution.
SPEC_MATERIALS = {
    "SEWCP-200": ("6061-T6", "spec/01 §7", "Hard anodize exc. masks"),
    "SEWCP-300": ("6061-T6", "spec/02 §6", "Clean; no anodize on bond face"),
    "SEWCP-400": ("Al2O3 99.5%", "spec/03 §7", "As-fired; lapped at assy"),
    "SEWCP-500": ("Al2O3 99.6%", "spec/04 §6", "Lapped top; mesa process"),
    "SEWCP-600": ("Al2O3 99.8%", "spec/05 §6", "Ground; Ra ≤ 0.2 tip/shaft"),
    "SEWCP-700": ("Ti-6Al-4V", "spec/06 §6", "Dry film + passivate"),
    "SEWCP-800": ("316L SST", "spec/07 §6", "Electropolish wetted"),
    "SEWCP-901": ("C10100 OFHC", "spec/08 §6", "Ag 8-13 µm direct (DR-7)"),
    "SEWCP-902": ("6061-T6", "spec/08 §5.2", "Alodine 1200"),
    "SEWCP-1000": ("6061-T6", "spec/09 §6", "Alodine 1200"),
}

#: Spec-defined items with no CAD model - deliberate, each with its record.
SPEC_ONLY = [
    ("SEWCP-301", "Thermal choke washer, Ti, 1.50 thk", 16,
     "Ti Grade 2", "spec/00 §4.2 row 3; spec/01 CP-IF-3",
     "Unmodelled by CP package decision: choke pads are treatment zones; "
     "the washer supplies the 1.50 gap represented in the assembly."),
    ("SEWCP-401", "Support ring clamp ring", 1,
     "316L", "spec/03 §5.2",
     "Material corrected 6061-T6 -> 316L per ECR-Q-014: the old row cited "
     "spec/00 §9 and SR-IF-2, neither of which states a material, while "
     "spec/03 §5.2 heads the part '(316L)'. Geometry deferred, and per "
     "ECR-D-016 the tabulated Ø318.0/Ø286.0 form cannot be placed at all - "
     "it intersects the web. Rev B item."),
    ("SEWCP-601", "Lift pin bushing, bore Ø5.60 +0.05/−0", 3,
     "Vespel/PEEK per spec/05", "spec/05 LB-D01 (ECR-Q-009 corrected)",
     "Deferred geometry (drawing-stage register)."),
    ("SEWCP-903", "RF terminal hardware set (4× M6×16 Ag SHCS, 4× Ø16 Ag "
     "washers, 4× Belleville stacks)", 1,
     "A4-70 / Ag plated", "spec/08 §5.3",
     "Hardware set; 6.0 N·m; spec-only."),
    ("SEWCP-904", "Deposition shroud", 1,
     "Ceramic per spec/08", "spec/08 §5.4",
     "NO dimensional authority in spec/08 - requirement gap, carried "
     "(drawing-stage register); not modelled, not drawn."),
]


@dataclass
class BomRow:
    level: int
    part_number: str
    name: str
    qty: int | str
    material: str
    spec_source: str
    cad_state: str
    deliverable: str
    notes: str = ""

    def as_list(self) -> list[str]:
        return [str(self.level), self.part_number, self.name, str(self.qty),
                self.material, self.spec_source, self.cad_state,
                self.deliverable, self.notes]


#: Spec material label -> the Fusion library material realising it.
_MATERIAL_EQUIV = {
    "6061-T6": "Aluminum 6061",
    "Al2O3 99.5%": "Aluminum Oxide",
    "Al2O3 99.6%": "Aluminum Oxide",
    "Al2O3 99.8%": "Aluminum Oxide",
    "Ti-6Al-4V": "Titanium 6Al-4V",
    "316L SST": "Stainless Steel",
    "C10100 OFHC": "Copper",
}


def _material_matches(spec_label: str, observed: str) -> bool:
    want = _MATERIAL_EQUIV.get(spec_label, spec_label)
    return want.lower() in observed.lower() or observed.lower() in want.lower()


def _fastener_rows() -> list[BomRow]:
    """Parse the spec/00 §9 fastener schedule verbatim."""
    text = (ROOT / "spec" /
            "00_SEWCP-ENG-001_Architecture_and_Interface_Control.md"
            ).read_text(encoding="utf-8")
    m = re.search(r"## 9\..*?(?=## 10\.)", text, re.S)
    rows: list[BomRow] = []
    if not m:
        return rows
    for line in m.group(0).splitlines():
        if not line.startswith("|") or "Joint" in line or "---" in line:
            continue
        cells = [c.strip().replace("**", "") for c in
                 line.strip().strip("|").split("|")]
        if len(cells) < 4 or not re.search(r"M\d", cells[1]):
            continue
        joint, fastener, qty, grade = cells[0], cells[1], cells[2], cells[3]
        torque = cells[4] if len(cells) > 4 else ""
        washer = cells[5] if len(cells) > 5 else ""
        rows.append(BomRow(
            1, "HW-" + re.sub(r"[^A-Za-z0-9]+", "", fastener)[:12],
            f"{fastener} — {joint[:60]}", qty, grade,
            "spec/00 §9 (verbatim)", "spec-only",
            "-", f"torque {torque}; {washer}"[:80]))
    return rows


def build_bom(assembly_run: str | Path) -> list[BomRow]:
    run = json.loads(Path(assembly_run).read_text(encoding="utf-8"))
    occs = run["observed_assembly"]["occurrences"]
    counts: dict[str, int] = {}
    observed_material: dict[str, str | None] = {}
    versions: dict[str, set] = {}
    for o in occs:
        design = o.get("source_design") or o.get("component")
        pn = design.split("_")[0]
        counts[pn] = counts.get(pn, 0) + 1
        versions.setdefault(pn, set()).add(o.get("source_version"))

    # Observed materials come from the per-component verified run records,
    # superseded by any later repair record's fresh observation - the run
    # records are immutable evidence, the repair record is newer evidence.
    si = json.loads((ROOT / "cad/runs/SYSTEM_INTERFACES.json"
                     ).read_text(encoding="utf-8"))
    names = {}
    for comp, rid in si["runs"].items():
        pn = comp.split("_")[0]
        names[pn] = comp
        r = json.loads((ROOT / "cad/runs" / rid / "run.json"
                        ).read_text(encoding="utf-8"))
        bodies = r["attempts"][-1]["observed_model"].get("bodies", [])
        observed_material[pn] = bodies[0].get("material") if bodies else None
    for rep in sorted(ROOT.glob("cad/runs/REPAIRS_*.json")):
        body = json.loads(rep.read_text(encoding="utf-8"))
        for row in body.get("material_repairs", []):
            observed_material[row["part"]] = \
                row["observed_after"]["material"]

    # ECR-D-015: the deliverable column names paths INSIDE this repository.
    # It previously named an external output root on one machine, and the
    # assembly cell still read "export pending bridge resume" long after the
    # export existed.
    rows = [BomRow(0, "SEWCP-000", "MASTER ASSEMBLY", 1, "—",
                   "spec/00 §4 / §10", "Fusion assembly (cloud)",
                   "cad/exports/step/SEWCP-000_MASTER_ASSEMBLY.step",
                   f"{len(occs)} occurrences, verified "
                   f"{run['run_id']} {run['verdict']}")]
    for pn in sorted(counts, key=lambda p: (len(p), p)):
        mat, mat_src, finish = SPEC_MATERIALS[pn]
        obs = observed_material.get(pn)
        note = finish
        if pn == "SEWCP-200":
            note += ("; lineage re-homed 2026-08-11 (stuck cloud "
                     "derivative) - REPAIRS_S-2026-08-11-04")
        if obs and not _material_matches(mat, obs):
            note += (f"; DEFECT: model material {obs!r} vs spec {mat!r} - "
                     "repair in BRIDGE_RESUME")
        rows.append(BomRow(
            1, pn, names[pn].split("_", 1)[1].replace("_", " "),
            counts[pn], mat, mat_src,
            f"verified model ({names[pn]})",
            f"cad/exports/step/{names[pn]}.step, cad/exports/stl/{names[pn]}.stl",
            note))
    for pn, name, qty, mat, src, note in SPEC_ONLY:
        rows.append(BomRow(1, pn, name, qty, mat, src, "spec-only", "-", note))
    rows.extend(_fastener_rows())
    rows.append(BomRow(
        1, "SEWCP-100", "BASE PLATE (frozen reference)", "REF", "—",
        "spec/00 §2 FBA", "frozen — not part of deliverable set", "-",
        "Datum A reference; excluded from the assembly by DR-1"))
    return rows


def cross_check(rows: list[BomRow], assembly_run: str | Path) -> list[str]:
    """The four required consistencies; empty list = clean."""
    faults: list[str] = []
    run = json.loads(Path(assembly_run).read_text(encoding="utf-8"))
    occs = run["observed_assembly"]["occurrences"]
    occ_counts: dict[str, int] = {}
    for o in occs:
        pn = (o.get("source_design") or "").split("_")[0]
        occ_counts[pn] = occ_counts.get(pn, 0) + 1
    bom_counts = {r.part_number: r.qty for r in rows if r.level == 1
                  and r.part_number.startswith("SEWCP-")
                  and "verified model" in r.cad_state}
    for pn, n in occ_counts.items():
        if bom_counts.get(pn) != n:
            faults.append(f"{pn}: assembly has {n}, BOM says "
                          f"{bom_counts.get(pn)}")
    for pn in bom_counts:
        if pn not in occ_counts:
            faults.append(f"{pn}: in BOM as modelled but not in the assembly")
    deliverables = (ROOT / "cad/DELIVERABLES.md").read_text(encoding="utf-8")
    for pn in bom_counts:
        if pn not in deliverables:
            faults.append(f"{pn}: no deliverable-manifest row")
    registry = {"SEWCP-200", "SEWCP-300", "SEWCP-400", "SEWCP-500",
                "SEWCP-600", "SEWCP-700", "SEWCP-800", "SEWCP-901",
                "SEWCP-902", "SEWCP-1000"}
    if set(bom_counts) != registry:
        faults.append(f"registry mismatch: {sorted(set(bom_counts) ^ registry)}")
    return faults


HEADER = ["level", "part_number", "name", "qty", "material", "spec_source",
          "cad_state", "deliverable", "notes"]


def write_bom_csv(rows: list[BomRow], path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        for r in rows:
            w.writerow(r.as_list())
    return p
