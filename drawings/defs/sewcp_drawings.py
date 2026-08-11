"""SEWCP drawing definitions - Rev A part drawing set.

Every graphical dimension sources a requirement-package parameter (which
is spec-anchored in its package) or a frozen spec anchor directly; the
critical-dimensions table on each drawing is parsed verbatim from the
frozen volume. See sewcp_common for the provenance vocabulary.
"""

from __future__ import annotations

import math

from sewcp_common import (
    IMPL, STANDARD_NOTES, TODAY, load_params, spec_dim_table,
)

from aief_draw import Circle, Dim, Drawing, Hatch, Line, Polyline, Sheet, Text, View
from aief_draw.model import Table, bolt_circle


def _pol(r: float, deg: float) -> tuple[float, float]:
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a))


def _dim_table(sheet: Sheet, rows, at=(14, 40), title="CRITICAL DIMENSIONS (frozen spec, verbatim)") -> None:
    if rows:
        sheet.tables.append(Table(
            at=at, col_widths=(18, 62, 30, 32),
            rows=tuple(rows), title=title, row_height=4.2))


def _std(drawing: Drawing, material: str, finish: str, scale: str) -> Drawing:
    drawing.fields.update({"material": material, "finish": finish,
                           "scale": scale, "date": TODAY})
    return drawing


# ---------------------------------------------------------------- SEWCP-200

def cp_drawing() -> Drawing:
    P = load_params(IMPL / "01_SEWCP-200_Cooling_Plate/requirements/SEWCP-200_base_and_datums.requirements.json")
    src = lambda n: f"parameter:{n} (params/generated/SEWCP-200.csv)"

    top = View("TOP", origin=(215, 125), scale=0.36)
    top.add(Circle((0, 0), P["cp_od"]))
    top.add(Line((-170, 0), (170, 0), layer="center"),
            Line((0, -170), (0, 170), layer="center"))
    top.add(*bolt_circle((0, 0), P["bc_ring"],
                         [22.5 + 45 * i for i in range(8)], 7.0))
    top.add(*bolt_circle((0, 0), P["bc_kin_btm"], [60, 180, 300], 10.0,
                         layer="hidden"))
    top.add(*bolt_circle((0, 0), P["bc_kin_top"], [75, 195, 315], 10.0))
    top.add(*bolt_circle((0, 0), P["bc_choke_out"],
                         [30 * i for i in range(12)], 5.5))
    top.add(*bolt_circle((0, 0), P["bc_choke_in"],
                         [45 + 90 * i for i in range(4)], 5.5))
    top.add(*bolt_circle((0, 0), 200.0, [30, 150, 270], 8.0))
    top.add(Circle((0, 0), P["ch_env_id"], layer="phantom"),
            Circle((0, 0), P["ch_env_od"], layer="phantom"))
    for r, ang in ((P["rtd_r_1"], P["rtd_ang_1"]), (P["rtd_r_2"], P["rtd_ang_2"]),
                   (P["rtd_r_3"], P["rtd_ang_3"])):
        top.add(Circle(_pol(r, ang), 1.7, layer="hidden"))
    # RF land arc on the bottom face, 93..117 deg envelope
    top.add(Polyline((_pol(P["rf_land_r_in"], 93), _pol(P["rf_land_r_out"], 93),
                      _pol(P["rf_land_r_out"], 117), _pol(P["rf_land_r_in"], 117)),
                     closed=True, layer="hidden"))
    top.add(Dim("diameter", (0, 0), value=P["cp_od"], source=src("cp_od"),
                angle_deg=200, text=f"⌀{P['cp_od']:g} (CP-D01)"))
    top.add(Dim("diameter", (0, 0), value=P["bc_ring"], source=src("bc_ring"),
                angle_deg=22.5, text=f"⌀{P['bc_ring']:g} BC 8× M6 (CP-IF-2)"))
    top.add(Dim("diameter", (0, 0), value=P["bc_kin_top"], source=src("bc_kin_top"),
                angle_deg=75, text=f"⌀{P['bc_kin_top']:g} BC locators 75°/195°/315° (ECR-D-010)"))
    top.add(Dim("diameter", (0, 0), value=P["bc_choke_out"], source=src("bc_choke_out"),
                angle_deg=330, text=f"⌀{P['bc_choke_out']:g} BC 12× choke (CP-IF-3)"))
    top.add(Dim("diameter", (0, 0), value=200.0,
                source="spec/00 §3.2 lift-pin bores ⌀200 BC",
                angle_deg=150, text="⌀200 BC 3× lift pin"))
    top.add(Dim("note", _pol(P["rf_land_r_mean"], 105),
                source="spec/01 CP-IF-8; ECR-Q-010 envelope governs",
                text="RF LAND 93°–117° (BOTTOM FACE, MASKED)", angle_deg=105))
    top.add(Dim("note", _pol(P["cp_od"] / 2, 255),
                source="spec/00 §3.2 coolant 255°(in)/285°(out)",
                text="COOLANT IN 255° / OUT 285°, RADIAL", angle_deg=255))

    side = View("SECTION A-A", origin=(90, 245), scale=0.36)
    od = P["cp_od"] / 2
    side.add(Polyline(((-od, 0), (od, 0), (od, P["cp_thk"]), (-od, P["cp_thk"])),
                      closed=True))
    z_top = P["ch_z_top"]
    z_btm = P["ch_z_btm"]
    for x0 in (-P["ch_env_od"] / 2, P["ch_env_id"] / 2):
        side.add(Polyline(((x0, z_btm), (x0 + P["ch_env_od"] / 2 - P["ch_env_id"] / 2, z_btm),
                           (x0 + P["ch_env_od"] / 2 - P["ch_env_id"] / 2, z_top),
                           (x0, z_top)), closed=True, layer="hidden"))
    side.add(Dim("linear", (od + 6, 0), p2=(od + 6, P["cp_thk"]),
                 source=src("cp_thk"), text=f"{P['cp_thk']:g} ±0.030 (CP-D02)",
                 offset=6))
    side.add(Dim("linear", (-od, z_top), p2=(-od, P["cp_thk"]),
                 source=src("ch_top_wall"),
                 text=f"{P['ch_top_wall']:g} (CP-D07)", offset=10))
    side.add(Dim("linear", (-od - 14, 0), p2=(-od - 14, P["lid_thk"]),
                 source=src("lid_thk"), text=f"{P['lid_thk']:g} FSW lid (CP-D08)",
                 offset=4))

    sh1 = Sheet("SEWCP-200-DRW-001 Sh 1", "Geometry", views=[top, side],
                notes=STANDARD_NOTES + [
        "COOLANT CHANNEL PER MDR-001; RIB 5.0 CONFIRMED (ECR-Q-011 DEC-03): FSW RIB PASSES — TAPERED PROBE TIP ⌀≤4.0, TRACKING ≤±0.5, PENETRATION 6.5–7.0.",
        "FSW LID PER spec/01 §6 STEP 5; RADIOGRAPH PER PROCESS NOTES.",
        "CLOCKING PER spec/00 §3.2 — BINDING; DO NOT RE-CLOCK.",
        "2× M6×12 BRACKET TAPS AT r=150, 88°/122°, BOTTOM FACE (CP-IF-8 AS AMENDED, APR-031).",
    ])
    _dim_table(sh1, spec_dim_table("01_SEWCP-200_Cooling_Plate.md", "CP-D")[:24],
               at=(14, 58))

    # Sheet 2 - masking
    mtop = View("BOTTOM FACE MASKS", origin=(120, 130), scale=0.33)
    mtop.add(Circle((0, 0), P["cp_od"]))
    mtop.add(Hatch((_pol(P["rf_land_r_in"], 93), _pol(P["rf_land_r_out"], 93),
                    _pol(P["rf_land_r_out"], 117), _pol(P["rf_land_r_in"], 117)),
                   label="M1"))
    for ang in (60, 180, 300):
        c = _pol(P["bc_kin_btm"] / 2, ang)
        s = 6.0
        mtop.add(Hatch(((c[0] - s, c[1] - s), (c[0] + s, c[1] - s),
                        (c[0] + s, c[1] + s), (c[0] - s, c[1] + s)),
                       label="M2", style="cross"))
    mtop.add(Hatch(((-14, -14), (14, -14), (14, 14), (-14, 14)), label="M3"))
    mtop2 = View("TOP FACE MASKS", origin=(300, 130), scale=0.33)
    mtop2.add(Circle((0, 0), P["cp_od"]))
    for i in range(12):
        c = _pol(P["bc_choke_out"] / 2, 30 * i)
        mtop2.add(Hatch(((c[0] - 11, c[1] - 11), (c[0] + 11, c[1] - 11),
                         (c[0] + 11, c[1] + 11), (c[0] - 11, c[1] + 11)),
                        label="M4"))
    for i in range(4):
        c = _pol(P["bc_choke_in"] / 2, 45 + 90 * i)
        mtop2.add(Hatch(((c[0] - 11, c[1] - 11), (c[0] + 11, c[1] - 11),
                         (c[0] + 11, c[1] + 11), (c[0] - 11, c[1] + 11)),
                        label="M4"))
    mtop.add(Dim("note", (0, -P["cp_od"] / 2), angle_deg=270,
                 source="spec/01 §8 masking table",
                 text="ANODIZE MASK ZONES — SEE NOTES"))
    sh2 = Sheet("SEWCP-200-DRW-001 Sh 2", "Masking (S9/S10)",
                views=[mtop, mtop2], notes=[
        "HARD ANODIZE ALL OVER EXCEPT MASKED ZONES M1–M5 (spec/01 §8, ECR-D-004).",
        "M1 RF LAND 93°–117°: MASK; ALODINE 1200 ONLY; Ra ≤ 0.8 (CP-D18, spec/08 §7).",
        "M2 LOCATOR COUNTERBORES + M4 THREADS (BOTH FACES): MASK (spec/01 §7 STEP 13).",
        "M3 VACUUM-PORT SEALING FACE + O-RING LAND: MASK (CP-IF-5).",
        "M4 16× CHOKE PADS + CP-D26 COUNTERBORE FLOORS: MASK — BELLEVILLE SLIP, ECR-D-004.",
        "M5 CHANNEL INTERIOR AND PORT POCKETS: MASK (spec/01 §7 STEP 13).",
        "RTD PORTS CROSS-VENTED PER DR-6; VENTS ⌀1.7 INTO ADJACENT CHOKE-SIDE RELIEF (CP-IF-9).",
    ])
    d = Drawing("SEWCP-200-DRW-001", "COOLING PLATE SEWCP-200", "A",
                sheets=[sh1, sh2])
    return _std(d, "6061-T6", "HARD ANODIZE 25–50 µm EXC. MASKS", "1:2.8")


# ---------------------------------------------------------------- SEWCP-300

def hp_drawing() -> Drawing:
    P = load_params(IMPL / "02_SEWCP-300_Heater_Plate/requirements/SEWCP-300_heater_plate.requirements.json")
    src = lambda n: f"parameter:{n} (SEWCP-300-REQ-001)"
    top = View("TOP", origin=(210, 120), scale=0.36)
    top.add(Circle((0, 0), P["hp_od"]))
    top.add(Line((-160, 0), (160, 0), layer="center"),
            Line((0, -160), (0, 160), layer="center"))
    top.add(*bolt_circle((0, 0), P["hp_slot_bc"], [75, 195, 315],
                         P["hp_slot_w"]))
    top.add(*bolt_circle((0, 0), 270.0, [30 * i for i in range(12)], 5.0,
                         layer="hidden"))
    top.add(*bolt_circle((0, 0), 90.0, [45 + 90 * i for i in range(4)], 5.0,
                         layer="hidden"))
    top.add(*bolt_circle((0, 0), 200.0, [30, 150, 270], P["hp_lp_d"]))
    top.add(Circle((0, 0), 2 * P["hp_sp_in_r0"], layer="phantom"),
            Circle((0, 0), 2 * P["hp_sp_in_r1"], layer="phantom"),
            Circle((0, 0), 2 * P["hp_sp_out_r0"], layer="phantom"),
            Circle((0, 0), 2 * P["hp_sp_out_r1"], layer="phantom"))
    top.add(Dim("diameter", (0, 0), value=P["hp_od"], source=src("hp_od"),
                angle_deg=200, text=f"⌀{P['hp_od']:g} (HP-D01)"))
    top.add(Dim("diameter", (0, 0), value=P["hp_slot_bc"], source=src("hp_slot_bc"),
                angle_deg=75, text=f"⌀{P['hp_slot_bc']:g} BC 3× slot {P['hp_slot_w']:g} H8 (HP-IF-3)"))
    top.add(Dim("note", _pol(P["hp_sp_out_r1"], 45), angle_deg=45,
                source="cad/runs spiral routing record (commit 3889a48); parameters hp_gr_*",
                text=f"HEATER GROOVE SPIRALS w{P['hp_gr_w']:g}×d{P['hp_gr_d']:g} p{P['hp_gr_pitch']:g} (BOTTOM)"))
    side = View("SECTION", origin=(90, 235), scale=0.36)
    od = P["hp_od"] / 2
    side.add(Polyline(((-od, 0), (od, 0), (od, P["hp_thk"]), (-od, P["hp_thk"])),
                      closed=True))
    side.add(Dim("linear", (od + 6, 0), p2=(od + 6, P["hp_thk"]),
                 source=src("hp_thk"), text=f"{P['hp_thk']:g} ±0.020 (HP-D02)",
                 offset=6))
    side.add(Dim("note", (0, 0), angle_deg=300,
                 source="spec/02 M5 blind depth vs bond face; IF-HP-M5 verified +1.50",
                 text=f"16× M5×{P['hp_m5_dep']:g} BLIND — 1.5 MIN TO BOND FACE"))
    sh = Sheet("SEWCP-300-DRW-001 Sh 1", "Geometry", views=[top, side],
               notes=STANDARD_NOTES + [
        "MI HEATER ELEMENT GROOVES: TWO COUNTER-SPIRALS, BOTTOM FACE; EXACT PATH PER ROUTING RECORD.",
        "BOND FACE (TOP): Ra ≤ 0.8, FLAT 0.05 — ESC ELASTOMER BOND (HP-IF-4).",
        "KINEMATIC SLOTS RE-CLOCKED 75°/195°/315° PER ECR-D-010.",
    ])
    _dim_table(sh, spec_dim_table("02_SEWCP-300_Heater_Plate.md", "HP-D")[:20],
               at=(14, 58))
    d = Drawing("SEWCP-300-DRW-001", "HEATER PLATE SEWCP-300", "A", sheets=[sh])
    return _std(d, "6061-T6", "CLEAN PER SEMI; NO ANODIZE ON BOND FACE", "1:2.8")


# ---------------------------------------------------------------- SEWCP-400

def sr_drawing() -> Drawing:
    P = load_params(IMPL / "03_SEWCP-400_Chuck_Support_Ring/requirements/SEWCP-400_support_ring.requirements.json")
    src = lambda n: f"parameter:{n} (SEWCP-400-REQ-001)"
    top = View("TOP", origin=(210, 120), scale=0.36)
    for dname in ("sr_fl_od", "sr_web_od", "sr_web_id", "sr_fl_id"):
        top.add(Circle((0, 0), P[dname]))
    top.add(*bolt_circle((0, 0), P["sr_bolt_bc"],
                         [22.5 + 45 * i for i in range(8)], P["sr_bolt_d"]))
    top.add(*bolt_circle((0, 0), P["sr_slot_bc"], [60, 180, 300],
                         P["sr_slot_w"]))
    top.add(Dim("diameter", (0, 0), value=P["sr_fl_od"], source=src("sr_fl_od"),
                angle_deg=200, text=f"⌀{P['sr_fl_od']:g} FLANGE"))
    top.add(Dim("diameter", (0, 0), value=P["sr_web_od"], source=src("sr_web_od"),
                angle_deg=160, text=f"⌀{P['sr_web_od']:g}/⌀{P['sr_web_id']:g} WEB (3.0 WALL)"))
    top.add(Dim("diameter", (0, 0), value=P["sr_slot_bc"], source=src("sr_slot_bc"),
                angle_deg=60, text=f"⌀{P['sr_slot_bc']:g} BC 3× SLOT {P['sr_slot_w']:g} H8"))
    top.add(Dim("diameter", (0, 0), value=P["sr_bolt_bc"], source=src("sr_bolt_bc"),
                angle_deg=22.5, text=f"⌀{P['sr_bolt_bc']:g} BC 8+8 ⌀{P['sr_bolt_d']:g} (DR-9 TWO CIRCUITS)"))
    side = View("SECTION", origin=(90, 235), scale=0.5)
    fo, fi = P["sr_fl_od"] / 2, P["sr_fl_id"] / 2
    wo, wi = P["sr_web_od"] / 2, P["sr_web_id"] / 2
    fh, h = P["sr_fl_h"], P["sr_h_supplied"]
    for sgn in (1, -1):
        pts = [(sgn * fi, 0), (sgn * fo, 0), (sgn * fo, fh), (sgn * wo, fh),
               (sgn * wo, h - fh), (sgn * fo, h - fh), (sgn * fo, h),
               (sgn * fi, h), (sgn * fi, h - fh), (sgn * wi, h - fh),
               (sgn * wi, fh), (sgn * fi, fh)]
        side.add(Polyline(tuple(pts), closed=True))
    side.add(Dim("linear", (fo + 6, 0), p2=(fo + 6, h),
                 source=src("sr_h_supplied"),
                 text=f"{P['sr_h_supplied']:g} AS-SUPPLIED — LAP TO 20.000 AT ASSY (DR-3)",
                 offset=6))
    side.add(Dim("linear", (-fo, 0), p2=(-fo, fh), source=src("sr_fl_h"),
                 text=f"{P['sr_fl_h']:g} FLANGE", offset=10))
    sh = Sheet("SEWCP-400-DRW-001 Sh 1", "Geometry (as-supplied / as-lapped)",
               views=[top, side], notes=STANDARD_NOTES + [
        "CERAMIC: COMPRESSION ONLY, NO THREADS (spec/00 §9 CERAMIC JOINT RULE).",
        "TOP FACE LAPPED AT ASSEMBLY FROM AS-BUILT STACK DATA (spec/00 §5.3, DR-3).",
        "REGISTER REBATE PER SR-D16 REGISTER — DEGENERATE ROWS TABULATED, CANDIDATE ECR-Q (CARRIED).",
        "EDGE BREAK ALL CERAMIC EDGES 0.3–0.5 × 45° (CERAMIC EDGE-BREAK STANDARD NOTE).",
    ])
    _dim_table(sh, spec_dim_table("03_SEWCP-400_Chuck_Support_Ring.md", "SR-D")[:20],
               at=(14, 58))
    d = Drawing("SEWCP-400-DRW-001", "CHUCK SUPPORT RING SEWCP-400", "A",
                sheets=[sh])
    return _std(d, "Al2O3 99.5%", "AS-FIRED; LAPPED FACES PER NOTE", "1:2.5 / 1:2")


# ---------------------------------------------------------------- SEWCP-500

def ec_drawing() -> Drawing:
    P = load_params(IMPL / "04_SEWCP-500_Electrostatic_Chuck/requirements/SEWCP-500_esc_puck.requirements.json")
    src = lambda n: f"parameter:{n} (SEWCP-500-REQ-001)"
    top = View("TOP", origin=(210, 120), scale=0.36)
    top.add(Circle((0, 0), P["ec_od"]))
    top.add(*bolt_circle((0, 0), P["ec_lp_bc"], [30, 150, 270], P["ec_lp_d"]))
    top.add(Circle((0, 0), P["ec_he_d"], layer="hidden"))
    top.add(*bolt_circle((0, 0), 60.0, [0, 180], 8.0, layer="hidden"))
    top.add(Dim("diameter", (0, 0), value=P["ec_od"], source=src("ec_od"),
                angle_deg=200, text=f"⌀{P['ec_od']:g} (EC-D01)"))
    top.add(Dim("diameter", (0, 0), value=P["ec_lp_bc"], source=src("ec_lp_bc"),
                angle_deg=150, text=f"⌀{P['ec_lp_bc']:g} BC 3× ⌀{P['ec_lp_d']:g} H8 LIFT (EC-D16)"))
    top.add(Dim("diameter", (0, 0), value=P["ec_he_d"], source=src("ec_he_d"),
                angle_deg=45, text=f"⌀{P['ec_he_d']:g} He FEED (AXIS)"))
    side = View("SECTION", origin=(90, 225), scale=0.36)
    od = P["ec_od"] / 2
    side.add(Polyline(((-od, 0), (od, 0), (od, P["ec_thk"]), (-od, P["ec_thk"])),
                      closed=True))
    side.add(Dim("linear", (od + 6, 0), p2=(od + 6, P["ec_thk"]),
                 source=src("ec_thk"), text=f"{P['ec_thk']:g} ±0.020 (EC-D02)",
                 offset=6))
    sh = Sheet("SEWCP-500-DRW-001 Sh 1", "Geometry / surface architecture",
               views=[top, side], notes=STANDARD_NOTES + [
        "MESA PATTERN H 0.020 ±0.003: SURFACE ARCHITECTURE — MFG PROCESS DEFINITION, NOT SOLID GEOMETRY (spec/04; deferred-feature register).",
        "BIPOLAR BURIED ELECTRODES: CO-FIRED; SEE spec/04 ELECTRODE ARCHITECTURE — NOT DIMENSIONED HERE.",
        "EC-D14 He DISTRIBUTION GROOVE LAYOUT: NO GEOMETRIC AUTHORITY IN spec/04 — CARRIED OPEN (drawing-stage register).",
        "CERAMIC EDGE BREAK 0.2–0.3 × 45° ALL EDGES; NO METAL WITHIN 10 mm OF TOP SURFACE AT ASSY.",
    ])
    _dim_table(sh, spec_dim_table("04_SEWCP-500_Electrostatic_Chuck.md", "EC-D")[:20],
               at=(14, 58))
    d = Drawing("SEWCP-500-DRW-001", "ESC PUCK SEWCP-500", "A", sheets=[sh])
    return _std(d, "Al2O3 99.6%", "LAPPED TOP; SEE MESA NOTE", "1:2.5")


# --------------------------------------------------------------- small parts

def lp_drawing() -> Drawing:
    P = load_params(IMPL / "05_SEWCP-600_Lift_Pins/requirements/SEWCP-600_lift_pin.requirements.json")
    src = lambda n: f"parameter:{n} (SEWCP-600-REQ-001)"
    v = View("SIDE", origin=(140, 220), scale=1.8)
    sh_r = P["lp_shaft_d"] / 2
    f_r = P["lp_foot_d"] / 2
    v.add(Polyline(((-f_r, 0), (f_r, 0), (f_r, P["lp_foot_h"]),
                    (sh_r, P["lp_foot_h"]), (sh_r, P["lp_len"] - 2),
                    (-sh_r, P["lp_len"] - 2), (-sh_r, P["lp_foot_h"]),
                    (-f_r, P["lp_foot_h"])), closed=True))
    v.add(Line((0, -4), (0, P["lp_len"] + 4), layer="center"))
    from aief_draw.model import Arc as _Arc
    v.add(_Arc((0, P["lp_len"] - 50.0), 50.0, 86.5, 93.5))
    v.add(Dim("linear", (12, 0), p2=(12, P["lp_len"]), source=src("lp_len"),
              text=f"{P['lp_len']:g} ±0.05 (LP-D02)", offset=6))
    v.add(Dim("linear", (-12, 0), p2=(-12, P["lp_foot_h"]),
              source=src("lp_foot_h"), text=f"{P['lp_foot_h']:g} FOOT (LP-D07)",
              offset=4))
    v.add(Dim("note", (sh_r, 50), source=src("lp_shaft_d"),
              text=f"⌀{P['lp_shaft_d']:g} h6 SHAFT (LP-D01)", angle_deg=15))
    v.add(Dim("note", (f_r, 1.5), source=src("lp_foot_d"),
              text=f"⌀{P['lp_foot_d']:g} FOOT (LP-D06)", angle_deg=340))
    v.add(Dim("note", (0, P["lp_len"]), source="spec/05 LP-D04 crown R50",
              text="R50 ±5 CROWN, Ra ≤ 0.2 (LP-D04/LP-D10)", angle_deg=60))
    sh = Sheet("SEWCP-600-DRW-001 Sh 1", "Lift pin", views=[v],
               notes=STANDARD_NOTES + [
        "MATCHED SET OF 3, LENGTH GRADE ±0.01 WITHIN SET (spec/05 MATCHED-SET NOTE).",
        "CENTRELESS GRIND SHAFT; STRAIGHTNESS 0.020/95 (LP-D03).",
        "CROWN-TO-SHAFT BLEND R1.0 MIN, NO UNDERCUT (LP-D05).",
        "SEWCP-601 BUSHING: SEPARATE PART, ⌀5.60 +0.05/−0 BORE (ECR-Q-009 CORRECTED) — NO CAD MODEL, SPEC-ONLY (BOM).",
    ])
    _dim_table(sh, spec_dim_table("05_SEWCP-600_Lift_Pins.md", "LP-D")[:14],
               at=(230, 60))
    d = Drawing("SEWCP-600-DRW-001", "LIFT PIN SEWCP-600", "A", sheets=[sh])
    return _std(d, "Al2O3 (shaft/crown) per spec/05 §6", "SEE NOTES", "1.8:1")


def ap_drawing() -> Drawing:
    P = load_params(IMPL / "06_SEWCP-700_Alignment_Pins/requirements/SEWCP-700_alignment_pin.requirements.json")
    src = lambda n: f"parameter:{n} (SEWCP-700-REQ-001)"
    v = View("SIDE", origin=(150, 190), scale=8.0)
    sp_r, fl_r, b_r = P["ap_spigot_d"] / 2, P["ap_flange_d"] / 2, P["ap_boss_d"] / 2
    z1, z2, z3 = P["ap_spigot_l"], P["ap_spigot_l"] + P["ap_flange_h"], P["ap_len"]
    v.add(Polyline(((-sp_r, 0), (sp_r, 0), (sp_r, z1), (fl_r, z1), (fl_r, z2),
                    (b_r, z2), (b_r, z3), (-b_r, z3), (-b_r, z2), (-fl_r, z2),
                    (-fl_r, z1), (-sp_r, z1)), closed=True))
    v.add(Line((0, -2), (0, z3 + 2), layer="center"))
    v.add(Dim("linear", (fl_r + 2, z1), p2=(fl_r + 2, z2), source=src("ap_flange_h"),
              text=f"{P['ap_flange_h']:g} ±0.02 (AP-D04)", offset=3))
    v.add(Dim("linear", (b_r + 2, z2), p2=(b_r + 2, z3), source=src("ap_boss_h"),
              text=f"{P['ap_boss_h']:g} ±0.05 (AP-D02)", offset=5))
    v.add(Dim("linear", (-fl_r - 2, 0), p2=(-fl_r - 2, z3), source=src("ap_len"),
              text=f"{P['ap_len']:g} ±0.05 (AP-D12)", offset=4))
    v.add(Dim("note", (sp_r, z1 / 2), source="spec/06 AP-D13 M4×0.7×4.00 spigot",
              text="M4×0.7 INTEGRAL SPIGOT (AP-D13)", angle_deg=340))
    v.add(Dim("note", (b_r, z2 + 1.2), source=src("ap_boss_d"),
              text=f"⌀{P['ap_boss_d']:g} h6 BOSS (AP-D01)", angle_deg=20))
    v.add(Dim("note", (fl_r, z1 + 1.5), source=src("ap_flange_d"),
              text=f"⌀{P['ap_flange_d']:g} h6 FLANGE (AP-D03)", angle_deg=0))
    v.add(Dim("note", (0, z3), source="spec/06 AP-D14 hex 3.0 A/F × 2.0",
              text="HEX 3.0 A/F × 2.0 DP (AP-D14)", angle_deg=90))
    sh = Sheet("SEWCP-700-DRW-001 Sh 1", "Alignment locator", views=[v],
               notes=STANDARD_NOTES + [
        "THE LOCATOR IS THE FASTENER — NO SEPARATE SCREW (ECR-D-009). TORQUE 1.2 N·m.",
        "GRIND BOSS AND FLANGE (POSITIONAL BUDGET); CONCENTRICITY 0.010 TIR (AP-D09).",
        "ANTI-GALLING DRY FILM ON FLANGE OD AND SPIGOT THREADS; PASSIVATE.",
        "BOSS SHORTER THAN SLOT DEPTH BY DESIGN — DO NOT 'MATCH' TO 3.0 (spec/06 §5 WARNING).",
    ])
    _dim_table(sh, spec_dim_table("06_SEWCP-700_Alignment_Pins.md", "AP-D")[:14],
               at=(230, 60))
    d = Drawing("SEWCP-700-DRW-001", "ALIGNMENT LOCATOR SEWCP-700", "A",
                sheets=[sh])
    return _std(d, "Ti-6Al-4V", "DRY FILM + PASSIVATE", "8:1")


def vp_drawing() -> Drawing:
    P = load_params(IMPL / "07_SEWCP-800_Vacuum_Port/requirements/SEWCP-800_port_body.requirements.json")
    src = lambda n: f"parameter:{n} (SEWCP-800-REQ-001)"
    v = View("SECTION", origin=(120, 150), scale=1.1)
    fl_r, sp_r = P["vp_flange_d"] / 2, P["vp_spigot_d"] / 2
    t_r, ti_r, b_r = P["vp_tube_od"] / 2, P["vp_tube_id"] / 2, P["vp_bore_d"] / 2
    for sgn in (1, -1):
        v.add(Polyline(((sgn * b_r, P["vp_spigot_l"]), (sgn * sp_r, P["vp_spigot_l"]),
                        (sgn * sp_r, 0), (sgn * fl_r, 0),
                        (sgn * fl_r, -P["vp_flange_h"]),
                        (sgn * t_r, -P["vp_flange_h"]),
                        (sgn * t_r, -P["vp_flange_h"] - P["vp_tube_l"]),
                        (sgn * ti_r, -P["vp_flange_h"] - P["vp_tube_l"]),
                        (sgn * ti_r, -P["vp_flange_h"] - 5),
                        (sgn * b_r, -P["vp_flange_h"])), closed=True))
    v.add(Line((0, P["vp_spigot_l"] + 4), (0, -P["vp_flange_h"] - P["vp_tube_l"] - 4),
               layer="center"))
    v.add(Dim("linear", (fl_r + 4, 0), p2=(fl_r + 4, -P["vp_flange_h"]),
              source=src("vp_flange_h"), text=f"{P['vp_flange_h']:g} (VP-D02)",
              offset=4))
    v.add(Dim("linear", (sp_r + 3, 0), p2=(sp_r + 3, P["vp_spigot_l"]),
              source=src("vp_spigot_l"), text=f"{P['vp_spigot_l']:g} (VP-D04)",
              offset=8))
    v.add(Dim("note", (sp_r, P["vp_spigot_l"] / 2), source=src("vp_spigot_d"),
              text=f"⌀{P['vp_spigot_d']:g} h8 PILOT (VP-D03)", angle_deg=30))
    v.add(Dim("note", (fl_r, -2), source=src("vp_flange_d"),
              text=f"⌀{P['vp_flange_d']:g} FLANGE (VP-D01)", angle_deg=0))
    v.add(Dim("note", (t_r, -60), source=src("vp_tube_od"),
              text=f"⌀{P['vp_tube_od']:g}×{P['vp_tube_wall']:g} WALL ×{P['vp_tube_l']:g} (VP-D13/14)",
              angle_deg=0))
    v.add(Dim("note", (b_r, 4), source=src("vp_bore_d"),
              text=f"⌀{P['vp_bore_d']:g} H9 BORE (VP-D05)", angle_deg=60))
    top = View("TOP", origin=(300, 105), scale=1.1)
    top.add(Circle((0, 0), P["vp_flange_d"]))
    top.add(Circle((0, 0), P["vp_spigot_d"]))
    top.add(Circle((0, 0), P["vp_groove_mean"], layer="hidden"))
    top.add(*bolt_circle((0, 0), P["vp_bolt_bc"],
                         [45 + 90 * i for i in range(4)], P["vp_bolt_d"]))
    top.add(Dim("diameter", (0, 0), value=P["vp_bolt_bc"], source=src("vp_bolt_bc"),
                angle_deg=45, text=f"⌀{P['vp_bolt_bc']:g} BC 4× ⌀{P['vp_bolt_d']:g} (VP-D11)"))
    top.add(Dim("diameter", (0, 0), value=P["vp_groove_mean"],
                source=src("vp_groove_mean"),
                angle_deg=200,
                text=f"⌀{P['vp_groove_mean']:g} O-RING GROOVE MEAN (VP-D06)"))
    sh = Sheet("SEWCP-800-DRW-001 Sh 1", "Port body", views=[v, top],
               notes=STANDARD_NOTES + [
        f"O-RING GROOVE {P['vp_groove_w']:g} W × {P['vp_groove_dep']:g} DP (VP-D07/08), CORNERS R0.3 MAX (VP-D09); FKM 22.0 ID × 2.50 CS.",
        "SEALING FACE FLAT 0.010 TIR (VP-D10).",
        "ORIFICE SEAT ⌀6.00 H7 × 5.0 (VP-D12) — RESTRICTOR IS SEPARATE HW (SPEC-ONLY, BOM).",
        "ORBITAL-WELD TUBE STUB; ELECTROPOLISH WETTED SURFACES.",
    ])
    _dim_table(sh, spec_dim_table("07_SEWCP-800_Vacuum_Port.md", "VP-D")[:14],
               at=(240, 160))
    d = Drawing("SEWCP-800-DRW-001", "VACUUM PORT BODY SEWCP-800", "A",
                sheets=[sh])
    return _std(d, "316L SST", "ELECTROPOLISH WETTED", "1.1:1")


# --------------------------------------------------------------- SEWCP-901/2

_RS_THETA = 45.06938          # deg - S arc angle, installed form (package)
_RS_LEG = 34.43821            # leg developed length
_RS_STATIONS = (0.0, 34.43821, 65.85414, 108.53564, 124.26989, 140.00414, 180.0)


def rs_drawing() -> Drawing:
    P = load_params(IMPL / "08_SEWCP-900_RF_Feedthrough_Bracket/requirements/SEWCP-901_rf_strap.requirements.json")
    src = lambda n: f"parameter:{n} (SEWCP-901-REQ-001)"
    import math as m
    th = m.radians(_RS_THETA)
    form = View("INSTALLED FORM (SIDE)", origin=(105, 165), scale=1.0)
    pts = [(15.0, -46.43821), (15.0, -12.0)]
    for i in range(13):
        a = m.pi + i * (m.pi / 2) / 12
        pts.append((35.0 + 20 * m.cos(a), -12.0 + 20 * m.sin(a)))
    pts.append((77.6815, 8.0))
    for i in range(1, 13):
        a = -m.pi / 2 + th * i / 12
        pts.append((77.6815 + 20 * m.cos(a), 28.0 + 20 * m.sin(a)))
    for i in range(12, 0, -1):
        a = m.pi / 2 + th * i / 12
        pts.append((106.0 + 20 * m.cos(a), -0.25 + 20 * m.sin(a)))
    pts += [(106.0, 19.75), (146.0, 19.75)]
    form.add(Polyline(tuple(pts)))
    form.add(Line((-5, 0), (160, 0), layer="phantom"))
    form.add(Text((-4, 2), "DATUM A (BASE PLATE)", 2.0))
    form.add(Line((-5, 20), (160, 20), layer="phantom"))
    form.add(Text((-4, 22), "CP BOTTOM FACE / RF LAND Z=20", 2.0))
    form.add(Dim("linear", (35, 0), p2=(35, 8), source=src("rs_h"),
                 text="8.0 ±1.0 INSTALLED (RS-D04)", offset=-12))
    form.add(Dim("note", (91.8, 14), source=src("rs_loop_r"),
                 text="R20 S-COMPLIANCE ×2 (RS-D05)", angle_deg=45))
    form.add(Dim("linear", (106, 19.75), p2=(146, 19.75),
                 source="decision: pad flat 40.0 ending at land outer r=146 (repair record, RUN-20260811T200254)",
                 text="PAD FLAT 40.0 TO r=146", offset=8))
    form.add(Dim("note", (136.18, 19.75),
                 source="RS-D07 as amended (APR-032): holes at r=136.18, ±14.97 — tap-coincident",
                 text="2× ⌀6.6 AT TAP POSITIONS (r 136.18)", angle_deg=310))
    flat = View("FLAT PATTERN", origin=(105, 250), scale=1.0)
    wid = P["rs_width"]
    flat.add(Polyline(((0, -wid / 2), (P["rs_dev"], -wid / 2),
                       (P["rs_dev"], wid / 2), (0, wid / 2)), closed=True))
    for s in _RS_STATIONS[1:-1]:
        flat.add(Line((s, -wid / 2), (s, wid / 2), layer="center"))
    for y in (-P["rs_hole_pitch"] / 2, P["rs_hole_pitch"] / 2):
        flat.add(Circle((170.18, y), P["rs_hole_d"]))
    flat.add(Dim("linear", (0, -wid / 2), p2=(P["rs_dev"], -wid / 2),
                 source=src("rs_dev"), text="180.0 ±2.0 DEVELOPED (RS-D03)",
                 offset=8))
    flat.add(Dim("linear", (0, -wid / 2), p2=(0, wid / 2), source=src("rs_width"),
                 text="50.0 ±0.5 (RS-D01)", offset=8))
    flat.add(Dim("note", (170.18, P["rs_hole_pitch"] / 2),
                 source="parameter:rs_hole_pitch (RS-D07 as amended: tap-coincident, ECR-D-013 DEC-01, APR-030/032)",
                 text=f"2× ⌀{P['rs_hole_d']:g} AT {P['rs_hole_pitch']:.2f} CTRS — COINCIDENT WITH CP-IF-8 TAPS",
                 angle_deg=45))
    flat.add(Dim("note", (140.0, -wid / 2),
                 source="decision: bend stations from installed-form derivation (RUN-20260811T200254)",
                 text="BEND STATIONS AT 34.44 / 65.85 / 108.54 / 124.27 / 140.00",
                 angle_deg=300))
    sh = Sheet("SEWCP-901-DRW-001 Sh 1", "RF strap — form and flat pattern",
               views=[form, flat], notes=STANDARD_NOTES + [
        "0.50 C10100 OFHC STRIP; SILVER 8–13 µm DIRECTLY ON COPPER — NO NICKEL (RS-D08/09, DR-7).",
        "FORM ON R20 MANDREL; ANNEAL; FLATTEN PADS 0.05 TIR; 4-WIRE ≤ 3 mΩ.",
        "HOLES COINCIDENT WITH CP-IF-8 TAPS: 29.94 CTRS AT PAD STATION 9.82 FROM END (ECR-D-013 DISPOSITION A, DEC-01).",
        "SEWCP-904 DEPOSITION SHROUD: NO DIMENSIONAL AUTHORITY IN spec/08 — CARRIED (NOT DRAWN).",
    ])
    d = Drawing("SEWCP-901-DRW-001", "RF STRAP SEWCP-901", "A", sheets=[sh])
    return _std(d, "C10100 OFHC + Ag", "SILVER 8–13 µm (DR-7)", "1:1")


def sb_drawing() -> Drawing:
    P = load_params(IMPL / "08_SEWCP-900_RF_Feedthrough_Bracket/requirements/SEWCP-902_saddle.requirements.json")
    src = lambda n: f"parameter:{n} (SEWCP-902-REQ-002)"
    import math as m
    fx = 150.0 * m.cos(m.radians(17.0))
    fy = 150.0 * m.sin(m.radians(17.0))
    x_in, x_out = fx - 9, fx + 9
    y_in, y_out = fy - 9, fy + 9
    ry0, ry1 = fy - 5, fy + 5
    plan = View("PLAN (LOOKING UP AT THE CP FACE)", origin=(105, 118), scale=1.15)
    outline = [(68, -ry1), (x_in, -ry1), (x_in, -y_out), (x_out, -y_out),
               (x_out, -y_in), (x_in, -y_in), (x_in, -ry0), (76, -ry0),
               (76, ry0), (x_in, ry0), (x_in, y_in), (x_out, y_in),
               (x_out, y_out), (x_in, y_out), (x_in, ry1), (68, ry1)]
    plan.add(Polyline(tuple(outline), closed=True))
    plan.add(Polyline(((68, -31), (76, -31), (76, 31), (68, 31)),
                      closed=True, layer="hidden"))
    for sgn in (1, -1):
        plan.add(Polyline(((68, sgn * 25.25), (76, sgn * 25.25),
                           (76, sgn * 30.25), (68, sgn * 30.25)),
                          closed=True, layer="hidden"))
        plan.add(Circle((fx, sgn * fy), P["sb_hole_d"]))
    plan.add(Polyline(((35, -25), (146, -25), (146, 25), (35, 25)),
                      closed=True, layer="phantom"))
    plan.add(Dim("linear", (68, -ry1), p2=(x_out, -ry1),
                 source=src("sb_rail_w"),
                 text=f"{x_out - 68:.2f} OVERALL", offset=10))
    plan.add(Dim("note", (fx, fy), source="spec/08 SB-D03 (APR-032): holes at CP-IF-8 bracket taps r=150, ±17°",
                 text=f"2× ⌀{P['sb_hole_d']:g} AT r=150, 88°/122° TAPS", angle_deg=40))
    plan.add(Dim("note", (72, 28), source="spec/08 SB-D02 (APR-030): cheeks guide the 50.0 strap at 50.5",
                 text="CHEEKS 50.5 GAP", angle_deg=140))
    plan.add(Dim("note", (100, -25), source="observed strap installed form (phantom)",
                 text="SEWCP-901 STRAP (REF)", angle_deg=250))
    side = View("SECTION AT STRAP AXIS", origin=(190, 215), scale=1.4)
    side.add(Polyline(((68, 15), (140.2, 15), (140.2, 20), (68, 20)),
                      closed=True))
    side.add(Polyline(((68, 8.25), (76, 8.25), (76, 15), (68, 15)),
                      closed=True))
    side.add(Polyline(((68, 8.0), (76, 8.0), (76, 8.25), (68, 8.25)),
                      closed=True, layer="hidden"))
    side.add(Line((30, 20), (150, 20), layer="phantom"))
    side.add(Text((32, 21.5), "CP BOTTOM FACE Z=20 (RF-HOT)", 2.0))
    side.add(Line((30, 0), (150, 0), layer="phantom"))
    side.add(Text((32, 1.5), "BASE PLATE Z=0 (GROUND)", 2.0))
    side.add(Polyline(((35, 7.75), (77.7, 7.75), (77.7, 8.25), (35, 8.25)),
                      closed=True, layer="phantom"))
    side.add(Dim("linear", (60, 0), p2=(60, 8.0), source="spec/08 SB-D04 (≥8.0 min to ground)",
                 text="8.0 MIN TO GROUND (SB-D04)", offset=-18))
    side.add(Dim("linear", (66, 8.25), p2=(66, 20), source=src("sb_drop"),
                 text=f"{P['sb_drop']:g} DROP (SB-D01: BEARING 8.25)", offset=-6))
    side.add(Dim("linear", (142, 15), p2=(142, 20), source=src("sb_web"),
                 text=f"{P['sb_web']:g} WEB", offset=4))
    sh = Sheet("SEWCP-902-DRW-001 Sh 1", "Strap support hanger", views=[plan, side],
               notes=STANDARD_NOTES + [
        "PLATE-HUNG HANGER PER ECR-Q-012 DISPOSITION (DEC-02 + ADDENDUM, APR-031/032): MOUNTS TO THE RF-HOT COOLING PLATE — NOT TO GROUND (RF-IF-3).",
        "BEARS ON THE STRAP TOP FACE AT 8.25: RS-D04 MID-PLANE = 8.0 EXACTLY (SB-D01).",
        "ALL SURFACES ≥ 8.0 FROM THE GROUNDED BASE PLATE (SB-D04) — MINIMUM AT THE CHEEK TIPS.",
        "M6 × 16 SHCS, 6.0 N·m INTO THE CP BRACKET TAPS (r=150, 88°/122°); GRIP 5.0, ENGAGEMENT 11.",
        "CNC ONE PIECE FROM 6061-T6 12.7 PLATE; ALODINE 1200 (CONDUCTIVE) — NOT ANODIZE.",
    ])
    d = Drawing("SEWCP-902-DRW-001", "STRAP SUPPORT HANGER SEWCP-902", "B",
                sheets=[sh])
    return _std(d, "6061-T6", "ALODINE 1200", "1.15:1 / 1.6:1")


# --------------------------------------------------------------- SEWCP-1000

def tr_drawing() -> Drawing:
    P = load_params(IMPL / "09_SEWCP-1000_Temperature_Sensor_Bracket/requirements/SEWCP-1000_retainer.requirements.json")
    src = lambda n: f"parameter:{n} (SEWCP-1000-REQ-001)"
    top = View("TOP", origin=(120, 100), scale=4.0)
    L, W, H = P["tr_len"], P["tr_wid"], P["tr_hgt"]
    top.add(Polyline(((-L / 2, -W / 2), (L / 2, -W / 2), (L / 2, W / 2),
                      (-L / 2, W / 2)), closed=True))
    top.add(Circle((0, 0), P["tr_probe_d"]))
    for x in (-P["tr_mount_pitch"] / 2, P["tr_mount_pitch"] / 2):
        top.add(Circle((x, 0), P["tr_mount_d"]))
    top.add(Dim("linear", (-P["tr_mount_pitch"] / 2, 0),
                p2=(P["tr_mount_pitch"] / 2, 0), source=src("tr_mount_pitch"),
                text=f"{P['tr_mount_pitch']:g} ±0.1 (TR-D04)", offset=-12))
    top.add(Dim("note", (0, P["tr_probe_d"] / 2), source=src("tr_probe_d"),
                text=f"⌀{P['tr_probe_d']:g} +0.05/−0 PROBE BORE (TR-D02)",
                angle_deg=60))
    side = View("SIDE", origin=(280, 100), scale=4.0)
    side.add(Polyline(((-L / 2, 0), (L / 2, 0), (L / 2, H), (-L / 2, H)),
                      closed=True))
    side.add(Polyline(((-P["tr_vent_w"] / 2, H - P["tr_vent_dep"]),
                       (P["tr_vent_w"] / 2, H - P["tr_vent_dep"]),
                       (P["tr_vent_w"] / 2, H), (-P["tr_vent_w"] / 2, H)),
                      closed=True, layer="hidden"))
    side.add(Dim("linear", (L / 2 + 2, 0), p2=(L / 2 + 2, H), source=src("tr_hgt"),
                 text=f"{H:g} (TR-D01)", offset=3))
    side.add(Dim("note", (0, H), source=src("tr_vent_w"),
                 text=f"VENT SLOT {P['tr_vent_w']:g} W × {P['tr_vent_dep']:g} DP (TR-D08, DR-13)",
                 angle_deg=45))
    sh = Sheet("SEWCP-1000-DRW-001 Sh 1", "RTD retainer", views=[top, side],
               notes=STANDARD_NOTES + [
        "PROBE BORE CONCENTRIC TO PLATE BORE 0.10 TIR AT ASSEMBLY (TR-D03).",
        "SPRING PLUNGER PRELOAD 7.5 ±2.5 N, TRAVEL 2.0 MIN (TR-D05/06) — HW IS SPEC-ONLY (BOM).",
        "VENT SLOT MUST ALIGN WITH PLATE CROSS-VENT AT INSTALL (spec/09 §10 STEP 7).",
        "SC SPRING-CLIP DETAIL: DEFERRED-FEATURE REGISTER — SPEC-ONLY HW, NOT DRAWN.",
    ])
    _dim_table(sh, spec_dim_table("09_SEWCP-1000_Temperature_Sensor_Bracket.md", "TR-D")[:10],
               at=(14, 160))
    d = Drawing("SEWCP-1000-DRW-001", "RTD RETAINER SEWCP-1000", "A",
                sheets=[sh])
    return _std(d, "6061-T6", "ALODINE 1200", "4:1")


PART_DRAWINGS = {
    "SEWCP-200": cp_drawing, "SEWCP-300": hp_drawing, "SEWCP-400": sr_drawing,
    "SEWCP-500": ec_drawing, "SEWCP-600": lp_drawing, "SEWCP-700": ap_drawing,
    "SEWCP-800": vp_drawing, "SEWCP-901": rs_drawing, "SEWCP-902": sb_drawing,
    "SEWCP-1000": tr_drawing,
}
