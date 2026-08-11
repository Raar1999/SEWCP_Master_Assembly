"""SEWCP-000 master assembly drawing - from observed assembly state.

Sheet 1: plan with clocked occurrence positions and balloons.
Sheet 2: section elevation - the §4.2 Z build as observed - plus the
         indentured BOM table and the spec/00 §9 fastener schedule.
Every position derives from the assembly package/observation; every
height from the observed occurrence z-bands.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from sewcp_common import ROOT, TODAY

sys.path.insert(0, str(ROOT / "src"))

from aief_draw import Circle, Dim, Drawing, Line, Polyline, Sheet, Text, View
from aief_draw.model import Table, bolt_circle

RUN = ROOT / "cad/runs/RUN-20260811T200919-f6cb5e/run.json"


def assembly_drawing() -> Drawing:
    run = json.loads(RUN.read_text(encoding="utf-8"))
    occs = run["observed_assembly"]["occurrences"]
    obs_src = f"observed:{run['run_id']} (verified PASS)"

    # ---- Sheet 1: plan ---------------------------------------------------
    plan = View("PLAN (TOP)", origin=(150, 150), scale=0.33)
    plan.add(Circle((0, 0), 320.0))                       # CP OD
    plan.add(Circle((0, 0), 300.0, layer="hidden"))       # HP under EC
    plan.add(Circle((0, 0), 297.0))                       # EC OD
    plan.add(Circle((0, 0), 318.0, layer="hidden"))       # SR flange
    plan.add(Line((-175, 0), (175, 0), layer="center"),
             Line((0, -175), (0, 175), layer="center"))
    balloons: list[tuple[str, float, float]] = []
    for o in occs:
        t = o["translate_mm"]
        pn = (o.get("source_design") or "").split("_")[0]
        r = math.hypot(t[0], t[1])
        if r > 1.0:
            plan.add(Circle((t[0], t[1]), 8.0, layer="phantom"))
            balloons.append((pn, t[0], t[1]))
    seen: set[str] = set()
    for pn, x, y in balloons:
        if pn in seen:
            continue
        seen.add(pn)
        plan.add(Dim("note", (x, y), source=obs_src,
                     text=pn, angle_deg=math.degrees(math.atan2(y, x))))
    for pn, label, ang in (("SEWCP-200", "SEWCP-200 CP ⌀320", 200),
                           ("SEWCP-500", "SEWCP-500 ESC ⌀297", 20)):
        plan.add(Dim("note", (160 * math.cos(math.radians(ang)),
                              160 * math.sin(math.radians(ang))),
                     source=obs_src, text=label, angle_deg=ang))
    plan.add(Dim("note", (0, 0), source="spec/00 §3.2 (binding clocking)",
                 text="CLOCKING PER spec/00 §3.2", angle_deg=245))
    occ_rows = [("BALLOON/PN", "OCCURRENCES", "AT")]
    grouped: dict[str, list[str]] = {}
    for pn, x, y in balloons:
        grouped.setdefault(pn, []).append(
            f"({x:.0f},{y:.0f})")
    for pn in sorted(grouped):
        pts = grouped[pn]
        occ_rows.append((pn, str(len(pts)), " ".join(pts)[:52]))
    sh1 = Sheet("SEWCP-000-DRW-001 Sh 1", "Master assembly — plan",
                views=[plan], notes=[
        "POSITIONS ARE OBSERVED FUSION ASSEMBLY STATE, RUN "
        + run["run_id"] + " (VERIFIED PASS, 19 OCCURRENCES).",
        "ASSEMBLE PER spec/00 §10 MASTER SEQUENCE; TORQUES PER §9 SHEET 2.",
        "SEWCP-301 CHOKE WASHERS (16×) SUPPLY THE 1.50 GAP — SPEC-ONLY PART.",
        "SEWCP-902 SADDLE POSITION PROVISIONAL — ECR-Q-012 OPEN.",
    ])
    sh1.tables.append(Table(at=(285, 40), col_widths=(24, 18, 90),
                            rows=tuple(occ_rows),
                            title="OCCURRENCES (observed)", row_height=4.6))

    # ---- Sheet 2: elevation + BOM ---------------------------------------
    elev = View("SECTION ELEVATION", origin=(105, 205), scale=0.9)
    stack = [("SEWCP-400", 318.0, "hidden"), ("SEWCP-200", 320.0, "outline"),
             ("SEWCP-300", 300.0, "outline"), ("SEWCP-500", 297.0, "outline")]
    for pn, od, layer in stack:
        o = next(o for o in occs
                 if (o.get("source_design") or "").startswith(pn))
        z0, z1 = o["bbox_min"][2], o["bbox_max"][2]
        elev.add(Polyline(((-od / 2 * 0.28, z0), (od / 2 * 0.28, z0),
                           (od / 2 * 0.28, z1), (-od / 2 * 0.28, z1)),
                          closed=True, layer=layer))
    elev.add(Line((-60, 0), (60, 0), layer="phantom"))
    elev.add(Text((-59, 1.5), "DATUM A", 2.0))
    for pn, zlabel in (("SEWCP-400", "20.000 (lapped, DR-3)"),
                       ("SEWCP-200", "40.000"),
                       ("SEWCP-300", "49.500"),
                       ("SEWCP-500", "55.900")):
        o = next(o for o in occs
                 if (o.get("source_design") or "").startswith(pn))
        z1 = o["bbox_max"][2]
        elev.add(Dim("linear", (52, 0), p2=(52, z1),
                     source=f"{obs_src}; spec/00 §4.2",
                     text=zlabel, offset=4 + 10 * stack.index(
                         next(s for s in stack if s[0] == pn))))
    elev.add(Dim("note", (0, 41.0), source="spec/00 §4.2 row 3",
                 text="1.50 CHOKE GAP (SEWCP-301 ×16)", angle_deg=15))
    elev.add(Dim("note", (0, 49.7), source="spec/00 §4.2 row 5",
                 text="0.40 BOND LINE", angle_deg=345))
    elev.add(Dim("note", (-30, 55.9), source="spec/00 §4.2 rows 7-8",
                 text="WAFER PLANE 55.920 (MESA 0.020)", angle_deg=160))

    from sedep.bom import build_bom
    bom_rows = build_bom(RUN)
    tbl = [("LVL", "PART NO", "NAME", "QTY", "MATERIAL", "STATE")]
    for r in bom_rows:
        tbl.append((str(r.level), r.part_number, r.name[:34], str(r.qty),
                    r.material[:16], r.cad_state[:18]))
    sh2 = Sheet("SEWCP-000-DRW-001 Sh 2",
                "Elevation + indentured BOM", views=[elev], notes=[
        "HEIGHTS ARE OBSERVED OCCURRENCE BOUNDS; NOMINAL AUTHORITY spec/00 §4.2.",
        "FULL BOM: BOM/SEWCP-000_BOM_RevA.csv (CROSS-CHECKED 4 WAYS).",
        "SEWCP-600 MATERIAL CORRECTED TO 99.8% ALUMINA (REPAIRS_S-2026-08-11-04).",
    ])
    sh2.tables.append(Table(at=(180, 30), col_widths=(10, 26, 62, 12, 30, 34),
                            rows=tuple(tbl), title="INDENTURED BOM (SEWCP-000)",
                            row_height=4.4, text_height=1.9))

    # ---- Sheet 3: fastener and torque schedule ---------------------------
    hw = [("JOINT / FASTENER", "QTY", "GRADE", "NOTES")]
    for r in bom_rows:
        if r.part_number.startswith("HW-"):
            hw.append((r.name[:66], str(r.qty), r.material[:12],
                       r.notes[:56]))
    sh3 = Sheet("SEWCP-000-DRW-001 Sh 3", "Fastener and torque schedule",
                views=[], notes=[
        "SCHEDULE PARSED VERBATIM FROM spec/00 §9 — THE FROZEN AUTHORITY.",
        "CERAMIC JOINT RULE: CERAMIC IN COMPRESSION ONLY; NO THREADS IN CERAMIC (spec/00 §9).",
        "BELLEVILLE SELECTION PER spec/00 §9; RF HARDWARE SILVER-PLATED PER SEWCP-903.",
        "ALIGNMENT LOCATORS ARE THEIR OWN FASTENER — 1.2 N·m (ECR-D-009, spec/06).",
    ])
    sh3.tables.append(Table(at=(16, 60), col_widths=(150, 14, 26, 120),
                            rows=tuple(hw), title="FASTENER SCHEDULE (spec/00 §9)",
                            row_height=5.2, text_height=2.0))

    d = Drawing("SEWCP-000-DRW-001", "SEWCP MASTER ASSEMBLY", "A",
                sheets=[sh1, sh2, sh3])
    d.fields.update({"material": "—", "finish": "—", "scale": "1:3 / 1:1.1",
                     "date": TODAY})
    return d
