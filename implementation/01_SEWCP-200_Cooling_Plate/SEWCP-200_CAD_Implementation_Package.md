# SEWCP-200 — Mechanical CAD Implementation Package

**Component:** 01 — Cooling Plate
**Part Number:** SEWCP-200
**Package No.:** SEWCP-200-CAD-001
**Revision:** — (X1, DRAFT — ISSUED WITH HOLD)
**Date:** 2026-08-07
**Issued by:** Lead Mechanical CAD Engineer
**Governing Baseline:** SEWCP Engineering Specification Set Rev A (Vol 00–09), FROZEN

---

> ## ⚠ PACKAGE STATUS — ISSUED WITH HOLD
>
> Four **blocking defects** (ECR-D-001 … ECR-D-004) were identified during baseline review. They are recorded in **§12 Open Questions**.
>
> **Approximately 82% of this part is fully determinate and may be modelled immediately.** Three feature groups are quarantined as **HOLD** and are pre-positioned in the timeline so that no restructuring is required when the defects are dispositioned:
>
> | HOLD | Feature group | Blocked by |
> |---|---|---|
> | **H1** | Coolant channel, FSW lid, channel cross-section | ECR-D-002 |
> | **H2** | 6× kinematic locator features (Ø306 bottom, Ø260 top) | ECR-D-001 |
> | **H3** | 2× coolant stub bores; 16× choke fastener counterbores | ECR-D-003, ECR-D-004 |
>
> **No assumption has been made to close any of these.** Per program rule, geometry that cannot be traced to the frozen baseline does not exist in this package.

---

# 1 Executive Summary


---

> # ⚠ REV X1 IS SUPERSEDED IN PART — READ THIS FIRST
>
> This package was written on **2026-08-07** against the pre-disposition baseline. Since then
> **eight ECRs have been dispositioned, approved, applied to the frozen specification and
> re-registered** (session `S-2026-08-10-01`). The numeric errors that would have misled a
> modeller are corrected in place below, but **this document has not been re-issued**, and a
> full Rev X2 is recorded as `OI-P-03`.
>
> **What changed since Rev X1 was written:**
>
> | ECR | Effect on this package |
> |---|---|
> | `ECR-D-001` | **HOLD H2 discharged.** SEWCP-700 governs: Ø10.0 H7 × 3.00 counterbore, Ø10.000 h6 flange, Ø6.000 h6 boss protruding 2.50 mm |
> | `ECR-D-002` | **HOLD H1 discharged.** `ch_depth` **8.0 → 6.0**; `lid_check` now 0.0; every derived flow value moved (Re ≈ 8,300, h ≈ 6,500, 60 mm², 1.11 m/s) |
> | `ECR-D-003` | **HOLD H3 (stubs) discharged.** `CP-D22`–`CP-D25`: Ø10.0 H9 bore at 11.00 above Datum A, channel locally deepened to 10.00, SEWCP-201 transition joint |
> | `ECR-D-004` | **HOLD H3 (counterbores) discharged.** `CP-D26` 11.0 W × 12.5 L × 2.5 deep, slotted and anodize-masked; **M5 × 25**, not M5 × 30 |
> | `ECR-D-007` | §3.1 gains a kinematic-locator keep-out (8.5 mm radius / 3.5 mm wall); `CP-D09a`/`CP-D10a` tap depths declared; counterbores **Ø12.000 → Ø10.000** |
> | `ECR-D-009` | The locator is now a **one-piece shouldered screw** — no separate M4 fastener. Torque **1.2 N·m** at a 3.0 mm hex socket |
> | `ECR-D-010` | **Top locators re-clocked Ø260 BC to 75°/195°/315°** — they collided with three outer choke stations at 30°/150°/270° |
> | `ECR-D-011` | SEWCP-300 only: heater-groove keep-out at the kinematic slots |
>
> **All three HOLDs are discharged.** §12 and §13 below are the *record of the defects as
> raised* and are accurate as history; they no longer describe the current baseline. Where this
> package and `spec/**` disagree, **`spec/**` governs** — it is the frozen, hash-registered
> authority and this package is not.
>
> **Accuracy note, `VER-016` W10.** An earlier form of this banner said the package's numeric
> errors were "corrected in place". **That was true only of the ECR-D-002 values.** The
> `ang_kin_top_*` parameters, timeline step 11, sketch S11 and step 6.34 still carried the
> superseded **30/150/270** clocking, and `choke_cbore_*` and the stub parameters still read
> `UNSPECIFIED`. A modeller following §6 in order would have built the very collision
> `ECR-D-010` was raised to remove. All of those are corrected now. **`params/generated/SEWCP-200.csv`
> still does not exist** — step 6.02 imports a file that has never been generated, so enter §3
> by hand or generate the CSV first.
>
> Verify the current gate state with `PYTHONPATH=src python -m aief_gate` before modelling.

---

## 1.1 Purpose of the Component

The Cooling Plate is the **thermal ground and RF bias electrode** of the SEWCP pedestal. It performs four concurrent functions (Vol 01 §1):

1. **Heat sink** — removes plasma heat and heater trim power via a closed-loop liquid circuit, establishing the baseline temperature from which the heater works upward.
2. **Structural backbone** — the stiffest member of the thermal stack; its flatness propagates directly to the wafer plane.
3. **RF bias electrode** — the powered 13.56 MHz electrode in Configuration A, capacitively coupled to the plasma through the ESC dielectric.
4. **Utility manifold** — all services to the ESC (helium, HV, lift pins, temperature probes) pass through it.

## 1.2 Role Within the Assembly

Stack position 2 of 5. It sits on the Chuck Support Ring (which isolates it electrically and thermally from the frozen Base Plate) and carries the Heater Plate + ESC sub-assembly through the thermal choke.

It is **the interface hub of the entire platform.** Seven of the nine remaining components inherit geometry from it. It hosts all six kinematic locators, the RF land, three RTD ports, the vacuum port interface, three lift pin bushings, sixteen choke pads, and the Support Ring tapped holes.

Nominal position in assembly: bottom face at **Z = 20.000**, top face at **Z = 40.000** (Vol 00 §4.2).

## 1.3 Interfaces

| IF | Mates To | Nature |
|---|---|---|
| CP-IF-1 | Chuck Support Ring SEWCP-400 | Kinematic locators, Ø306 BC bottom face — **HOLD H2** |
| CP-IF-2 | Chuck Support Ring SEWCP-400 | 8× M6 tapped, Ø302 BC bottom face (RF-side circuit, DR-9) |
| CP-IF-3 | Heater Plate SEWCP-300 | 16× radially slotted M5 clearance; 16× choke washer pads |
| CP-IF-4 | Heater Plate SEWCP-300 | Kinematic locators, Ø260 BC top face — **HOLD H2** |
| CP-IF-5 | Vacuum Port SEWCP-800 | Ø10.0 H8 piloted bore; masked flat sealing face; 4× M4 @ Ø38 BC |
| CP-IF-6 | Lift Pins SEWCP-600/601 | 3× Ø8.0 H8 bore + Ø12 H7 × 6 counterbore @ Ø200 BC |
| CP-IF-7 | ESC HV feed | 2× Ø8.0 alumina-lined bores @ Ø60 BC |
| CP-IF-8 | RF Bracket SEWCP-900 | 60 × 18 mm land @ Ø274 BC / 105°; 2× M6 tapped |
| CP-IF-9 | Temp Sensor SEWCP-1000 | 3× Ø1.7 H8 × 12 blind ports + 6× M4 retainer taps |
| CP-IF-10 | Coolant system | 2× ½ in. VCR stubs, radial @ 255° / 285° — **HOLD H3** |

**No direct contact with the Base Plate.** Electrical isolation depends on this (Vol 01 §4).

## 1.4 Critical Engineering Constraints

| Constraint | Value | Source | Consequence if violated |
|---|---|---|---|
| Overall thickness | 20.000 ± 0.030 | CP-D02 | Wafer plane Z-stack (Vol 00 §5.2) |
| Top face flatness | 0.015 TIR | CP-D03 | Propagates to wafer plane |
| Top-to-bottom parallelism | 0.015 TIR | CP-D04 | Propagates to wafer plane |
| Choke pad coplanarity | 0.010 TIR, set of 16 | CP-D17 | R_choke becomes unpredictable |
| Kinematic locator position | ⌖ Ø0.020 Ⓜ A B C | CP-D11 | Chuck axis concentricity |
| Lift pin bore perpendicularity | 0.030 over 20 mm | CP-D14 | Ceramic pin bind → fracture |
| **Top face NOT anodized** | ε ≤ 0.15 | Vol 01 §8 | Radiative shunt across the thermal choke |
| Coolant channel envelope | Ø60 to Ø250 | Vol 01 §3.1 | Keep-out violation → leak or no thread material |
| Channel turbulence | Re ≈ 8,300 | Vol 01 §2.1 | Uniformity requirement CP-11 lost |
| Mass | ≤ 4.2 kg | CP-15 | — |

**Governing design rule: DR-2** — no fastener penetrates the ESC top surface, therefore all 24 stack fasteners enter from below, therefore the coolant circuit must weave around a fixed fastener pattern. **The keep-out table is satisfied before path length is optimised** (Vol 01 §3.1).

## 1.5 Manufacturing Philosophy

**Two-piece 6061-T651 construction, friction-stir-welded** (Vol 01 §6).

The channel is milled into the **bottom** face and closed by an FSW lid, for two stated reasons: the top face must be lapped to 15 µm with choke pads coplanar to 10 µm (a weld seam there would prevent it), and keeping the weld on the low-stress side means weld distortion is corrected by the final lap rather than propagating to the wafer.

Three sequencing rules bind the CAD model's feature order:

1. **Stress relief is called out twice and is not optional.** Rough machine → relieve → semi-finish → relieve → finish → lap last, after anodize.
2. **No elastomer in the coolant pressure boundary.** The FSW joint is the reason the lid is a discrete body in the model.
3. **Masking is a deliverable, not a note.** Five surfaces are excluded from hard anodize for three different reasons. The masking zones must exist as modelled sketch regions to support the masking drawing sheet.

---

# 2 Engineering Traceability

Nothing in this package exists that is not traceable to the frozen baseline.

| # | Feature | Source Doc | Section | Engineering Requirement | Interface Ref |
|---|---|---|---|---|---|
| F01 | Outside diameter Ø320.0 ±0.10 | SEWCP-ENG-002 | §5 CP-D01 | Envelope; ≥5 mm wall to channel | — |
| F02 | Overall thickness 20.000 ±0.030 | SEWCP-ENG-002 | §5 CP-D02 | Wafer-plane Z-stack element 2 | Vol 00 §4.2 |
| F03 | Top face, flat 0.015, parallel 0.015 | SEWCP-ENG-002 | §5 CP-D03/D04 | Flatness budget 15 µm allocation | Vol 00 §5.1 |
| F04 | Bottom face = Datum A, flat 0.015 | SEWCP-ENG-002 | §9 | Primary datum; seats on Support Ring | SR-IF-3 |
| F05 | Coolant channel 10.0 W × 6.0 D | SEWCP-ENG-002 | §5 CP-D05/D06, §2.1 | Re ≈ 8,300 at 4 L/min | CP-IF-10 |
| F06 | Channel-to-top-face wall 8.00 ±0.20 *(was H1 — discharged)* | SEWCP-ENG-002 | §5 CP-D07 | Thermal path 0.00068 K/W | Vol 00 §4.3 |
| F07 | FSW lid 6.00 ±0.10 *(was H1 — discharged)* | SEWCP-ENG-002 | §5 CP-D08, §6 | Pressure boundary, no elastomer | — |
| F08 | Channel envelope Ø60–Ø250 | SEWCP-ENG-002 | §3.1 | Solid material under RF land | CP-IF-8 |
| F09 | Channel keep-out table, 8 classes | SEWCP-ENG-002 | §3.1 | DR-2 consequence | Vol 00 §4.4 |
| F10 | 8× M6×1.0 tapped, 12 deep, Ø302 BC, 22.5°+n·45°, bottom face | SEWCP-ENG-002 | §3 CP-IF-2, §5 CP-D20 | Upper RF-side bolt circuit, DR-9 | SR-IF-3 |
| F11 | 6× kinematic locator, Ø306 btm / Ø260 top *(was H2 — discharged)* | SEWCP-ENG-002 / -007 | CP-IF-1/4, CP-D09/D10/D11 / AP-IF-1 | Kinematic centering, ⌖Ø0.020 | SR-IF-4, HP-IF-3 |
| F12 | 16× M5 radial slots 5.5 W × 7.0 L (12 @ Ø270, 4 @ Ø90) | SEWCP-ENG-002 | §3 CP-IF-3 | Allows 0.399 mm radial growth | HP-IF-2 |
| F13 | 16× choke washer pads Ø22, coplanar 0.010, top face | SEWCP-ENG-002 | §5 CP-D17, §8 | R_choke = 0.1009 K/W | HP-IF-1 |
| F14 | Central bore Ø10.000 H8 | SEWCP-ENG-002 | §5 CP-D15, CP-IF-5 | Vacuum port pilot spigot | VP-IF-1 |
| F15 | Vacuum sealing face, flat 0.010, Ra 0.8–1.6, Ø18–Ø32 masked | SEWCP-ENG-002 | §5 CP-D16, CP-IF-5 | Face seal integrity | VP-IF-1/2 |
| F16 | 4× M4 tapped, 10 deep, Ø38 BC, bottom face | SEWCP-ENG-002 | §3 CP-IF-5 | Vacuum port retention | VP-IF-1 |
| F17 | 3× Ø8.000 H8 bores @ Ø200 BC, 30/150/270 | SEWCP-ENG-002 | §5 CP-D12/D13 | Lift pin pass-through | LP-IF-4 |
| F18 | 3× Ø12 H7 × 6 deep counterbore, bottom face | SEWCP-ENG-002 | §3 CP-IF-6 | SEWCP-601 bushing seat | LP-IF-4 |
| F19 | Lift pin bore perpendicularity 0.030 | SEWCP-ENG-002 | §5 CP-D14, §9 | Prevents ceramic pin bind | LP-IF-3 |
| F20 | 2× Ø8.0 bores @ Ø60 BC, 0°/180° | SEWCP-ENG-002 | §3 CP-IF-7 | ESC HV feed, alumina-lined | HP-IF-6 |
| F21 | RF land 60 circ × 18 radial, Ø274 BC @ 105°, flat 0.020 | SEWCP-ENG-002 | §3 CP-IF-8, §5 CP-D18 | Contact R ≤ 0.5 mΩ | RF-IF-1 |
| F22 | 2× M6 tapped, 12 deep, r=137, 98.7°/111.3° | SEWCP-ENG-002 | §3 CP-IF-8 | RF strap terminal | RF-IF-1 |
| F23 | 3× Ø1.700 H8 × 12 blind, r=40@75°, 100@165°, 140@225° | SEWCP-ENG-002 | §3 CP-IF-9, §5 CP-D19 | RTD response ≤ 5 s | TS-IF-3 |
| F24 | 3× cross-vent to RTD blind bores | SEWCP-ENG-002 | §3 CP-IF-9 | **DR-6 / DR-13** — no virtual leaks | Vol 09 §3 |
| F25 | 6× M4 tapped, 8 deep, ±9 mm flanking RTD ports | SEWCP-ENG-002 | §3 CP-IF-9 | Sensor retainer mounting | TS-IF-1 |
| F26 | 2× VCR stub interface @ 255°/285° *(was H3 — discharged)* | SEWCP-ENG-002 | §3 CP-IF-10 | Coolant supply/return | — |
| F27 | Masking zone: top face + 16 pads | SEWCP-ENG-002 | §8 | ε ≤ 0.15; conduction path | Vol 00 §8 |
| F28 | Masking zone: RF land, Alodine 1200 only | SEWCP-ENG-002 | §8 | Conductive joint | RF-IF-1 |
| F29 | Masking zone: channel interior | SEWCP-ENG-002 | §8 | Anodize flakes foul the loop | — |
| F30 | Masking zone: vacuum sealing face | SEWCP-ENG-002 | §8 | Anodize is a poor sealing surface | Vol 07 §8 |
| F31 | Masking zone: locator bores *(was H2 — discharged)* | SEWCP-ENG-002 | §8 | Locator fit integrity | — |
| F32 | Type III hard anodize 50 µm, bottom face + OD | SEWCP-ENG-002 | §8 | Plasma/handling durability | — |
| F33 | Datum frame A / B / C | SEWCP-ENG-002 | §9 | GD&T reference | — |

**Traceability exceptions:** none. Every feature above cites a frozen source. Features declared elsewhere but **not** carried into Vol 01 (Vol 08 RF-IF-3 bracket mounting holes) are **not modelled** — see ECR-Q-006.

---

# 3 Parameters

**Rule applied:** every dimension that appears in the frozen specification is a named user parameter. Every dimension derivable from another is an expression, never a literal. Fusion units set to **mm**; angular units **deg**.

## 3.1 Global Envelope

| Name | Description | Expression | Units | Design Intent | Dependency |
|---|---|---|---|---|---|
| `cp_od` | Plate outside diameter | `320.0` | mm | CP-D01 envelope | — |
| `cp_thk` | Overall thickness | `20.0` | mm | **Z-stack element 2, CP-D02** | Drives all Z references |
| `cp_mass_max` | Mass limit for verification | `4.2` | kg | CP-15 | Check only |

## 3.2 Coolant Circuit — **HOLD H1**

| Name | Description | Expression | Units | Design Intent | Dependency |
|---|---|---|---|---|---|
| `ch_width` | Channel width | `10.0` | mm | CP-D05; flow area | `ch_depth` |
| `ch_depth` | Channel depth | `6.0` | mm | CP-D06; Re ≈ 8,300 (ECR-D-002, APR-019) | `ch_width` |
| `ch_top_wall` | Channel to top face | `8.0` | mm | CP-D07; thermal path | `cp_thk` |
| `lid_thk` | FSW lid thickness | `6.0` | mm | CP-D08 | — |
| `ch_z_top` | Channel top surface Z | `cp_thk - ch_top_wall` | mm | Derived | `cp_thk`, `ch_top_wall` |
| `ch_z_btm` | Channel bottom surface Z | `ch_z_top - ch_depth` | mm | Derived | `ch_z_top`, `ch_depth` |
| `lid_check` | **Arithmetic consistency check** | `ch_z_btm - lid_thk` | mm | **Must equal 0. Now evaluates to 0.0.** | ECR-D-002 closed by APR-019 |
| `ch_env_id` | Channel envelope inner Ø | `60.0` | mm | Vol 01 §3.1 | — |
| `ch_env_od` | Channel envelope outer Ø | `250.0` | mm | Vol 01 §3.1; solid under RF land | — |
| `ch_bend_r` | Minimum bend radius | `5.0` | mm | Vol 01 §6 step 3; erosion | — |
| `ch_corner_r` | Minimum corner fillet | `3.0` | mm | Vol 01 §6 step 3 | — |

> `lid_check` is deliberately included as a live parameter. It now evaluates to **0.0 mm**, as required. **Keep it.** It was what made ECR-D-002 visible in the model, and it is what will catch the same defect if any of the four Z dimensions is ever edited independently of the others.

## 3.3 Bolt Circles and Clocking

| Name | Description | Expression | Units | Design Intent | Dependency |
|---|---|---|---|---|---|
| `bc_ring` | Support Ring tapped BC | `302.0` | mm | CP-IF-2 | SR-IF-3 |
| `ang_ring_0` | Ring hole start angle | `22.5` | deg | Vol 00 §3.2 | — |
| `ang_ring_step` | Ring hole increment | `45.0` | deg | Vol 00 §3.2 (8 off) | — |
| `bc_kin_btm` | Kinematic locator BC, bottom | `306.0` | mm | CP-D09/D11 | SR-IF-4 |
| `bc_kin_top` | Kinematic locator BC, top | `260.0` | mm | CP-D10/D11 | HP-IF-3 |
| `ang_kin_btm_1/2/3` | Bottom locator angles | `60.0` / `180.0` / `300.0` | deg | Vol 00 §3.2 | Datum B/C |
| `ang_kin_top_1/2/3` | Top locator angles | `75.0` / `195.0` / `315.0` | deg | Vol 00 §3.2, re-clocked by ECR-D-010 | — |
| `bc_choke_out` | Outer choke fastener BC | `270.0` | mm | CP-IF-3 | HP-IF-2 |
| `ang_choke_out_0` | Outer choke start angle | `0.0` | deg | Vol 00 §3.2 | — |
| `ang_choke_out_step` | Outer choke increment | `30.0` | deg | 12 off | — |
| `bc_choke_in` | Inner choke fastener BC | `90.0` | mm | CP-IF-3 | HP-IF-2 |
| `ang_choke_in_0` | Inner choke start angle | `45.0` | deg | Vol 00 §3.2 | — |
| `ang_choke_in_step` | Inner choke increment | `90.0` | deg | 4 off | — |
| `bc_liftpin` | Lift pin bolt circle | `200.0` | mm | CP-D13 | LP-IF-4 |
| `ang_liftpin_1/2/3` | Lift pin angles | `30.0` / `150.0` / `270.0` | deg | Vol 00 §3.2 | Robot sector at 210° |
| `bc_hv` | HV feed bolt circle | `60.0` | mm | CP-IF-7 | HP-IF-6 |
| `ang_hv_1/2` | HV feed angles | `0.0` / `180.0` | deg | Vol 00 §3.2 | — |
| `bc_vac` | Vacuum port tapped BC | `38.0` | mm | CP-IF-5 | VP-IF-1 |
| `bc_rf` | RF land bolt circle | `274.0` | mm | CP-IF-8 | RF-IF-1 |
| `ang_rf_land` | RF land centre angle | `105.0` | deg | Vol 00 §3.2 | — |
| `ang_coolant_in` | Coolant inlet angle | `255.0` | deg | CP-IF-10 | **HOLD H3** |
| `ang_coolant_out` | Coolant outlet angle | `285.0` | deg | CP-IF-10 | **HOLD H3** |

## 3.4 Feature Dimensions

| Name | Description | Expression | Units | Design Intent | Dependency |
|---|---|---|---|---|---|
| `ring_tap_size` | Ring tapped hole | `6.0` (M6×1.0) | mm | CP-IF-2 | — |
| `ring_tap_depth` | Ring tap depth | `12.0` | mm | CP-IF-2 / CP-D20 | `cp_thk` |
| `choke_slot_w` | Choke slot width | `5.5` | mm | CP-IF-3; M5 clearance | — |
| `choke_slot_l` | Choke slot length, radial | `7.0` | mm | CP-IF-3; ±0.75 mm travel | HP thermal growth 0.399 |
| `choke_cbore_w` | Choke counterbore slot width | `11.0` | mm | CP-D26 (ECR-D-004) | `choke_slot_w` |
| `choke_cbore_l` | Choke counterbore slot length, radial | `12.5` | mm | CP-D26 (ECR-D-004) | `choke_cbore_w` |
| `choke_cbore_dep` | Choke counterbore depth | `2.5` | mm | CP-D26 (ECR-D-004) | `lid_thk` |
| `kin_cbore_d` | Kinematic locator counterbore Ø | `10.0` | mm | CP-D09/CP-D10 (ECR-D-007) | — |
| `kin_cbore_dep` | Kinematic locator counterbore depth | `3.0` | mm | CP-D09/CP-D10 | — |
| `kin_tap_dep` | Locator M4 tap, full thread | `5.0` | mm | CP-D09a/CP-D10a | `kin_cbore_dep` |
| `stub_bore_d` | Coolant stub bore Ø | `10.0` | mm | CP-D22 (ECR-D-003) | — |
| `stub_bore_z` | Stub centreline above Datum A | `11.0` | mm | CP-D23 | `stub_bore_d` |
| `stub_wp_d` | Stub weld-prep counterbore Ø | `14.0` | mm | CP-D24 | `stub_bore_d` |
| `stub_wp_dep` | Stub weld-prep counterbore depth | `4.0` | mm | CP-D24 | — |
| `ch_depth_port` | Channel local depth at ports | `10.0` | mm | CP-D25 | `ch_depth` |
| `choke_pad_dia` | Choke washer pad Ø | `22.0` | mm | CP-D17; = SEWCP-301 OD | ECR-Q-007 |
| `he_bore` | Central He / pilot bore | `10.0` (H8) | mm | CP-D15; VP pilot Ø9.90 h8 | VP-IF-1 |
| `vac_seal_id` | Sealing face inner Ø | `18.0` | mm | CP-IF-5 masked annulus | — |
| `vac_seal_od` | Sealing face outer Ø | `32.0` | mm | CP-IF-5 masked annulus | — |
| `vac_tap_size` | Vacuum port tap | `4.0` (M4×0.7) | mm | CP-IF-5 | VP-D11 |
| `vac_tap_depth` | Vacuum port tap depth | `10.0` | mm | CP-IF-5 | — |
| `lp_bore` | Lift pin bore Ø | `8.0` (H8) | mm | CP-D12 | LP-IF-2 |
| `lp_cbore` | Bushing counterbore Ø | `12.0` (H7) | mm | CP-IF-6 | LB-D02 |
| `lp_cbore_dep` | Bushing counterbore depth | `6.0` | mm | CP-IF-6; = bushing length | LB-D03 |
| `hv_bore` | HV feed bore Ø | `8.0` | mm | CP-IF-7 | — |
| `rf_land_circ` | RF land circumferential | `60.0` | mm | CP-IF-8 | RF strap 50 mm wide |
| `rf_land_rad` | RF land radial width | `18.0` | mm | CP-IF-8 | — |
| `rf_tap_size` | RF land tap | `6.0` (M6×1.0) | mm | CP-IF-8 | RF-IF-1 |
| `rf_tap_depth` | RF land tap depth | `12.0` | mm | CP-IF-8 | — |
| `rf_tap_pitch` | RF tap circumferential pitch | `30.0` | mm | Derived from 98.7°/111.3° | `bc_rf` |
| `rtd_bore` | RTD blind bore Ø | `1.7` (H8) | mm | CP-D19 | TS-IF-3 |
| `rtd_depth` | RTD blind bore depth | `12.0` | mm | CP-D19 | Probe 30 mm long |
| `rtd_r_1/2/3` | RTD radii | `40.0` / `100.0` / `140.0` | mm | CP-IF-9 | TS-01 |
| `rtd_ang_1/2/3` | RTD angles | `75.0` / `165.0` / `225.0` | deg | CP-IF-9; clears RF land | — |
| `rtd_vent_dia` | Cross-vent bore Ø | `1.5` | mm | **DR-6 / DR-13** | — |
| `rtd_tap_size` | Retainer tap | `4.0` (M4×0.7) | mm | CP-IF-9 | TS-IF-1 |
| `rtd_tap_depth` | Retainer tap depth | `8.0` | mm | CP-IF-9 | — |
| `rtd_tap_offset` | Retainer tap offset | `9.0` | mm | CP-IF-9 (±9 mm) | — |

## 3.5 Derived Geometry

| Name | Description | Expression | Units | Design Intent | Dependency |
|---|---|---|---|---|---|
| `rf_land_r_mean` | RF land mean radius | `bc_rf / 2` | mm | = 137.0 | `bc_rf` |
| `rf_land_r_in` | RF land inner radius | `rf_land_r_mean - rf_land_rad / 2` | mm | = 128.0 | — |
| `rf_land_r_out` | RF land outer radius | `rf_land_r_mean + rf_land_rad / 2` | mm | = 146.0 | — |
| `rf_land_half_ang` | RF land half-angle | `(rf_land_circ / 2) / rf_land_r_mean * 180 / PI` | deg | = 12.547° | Land spans 92.45–117.55° |
| `rf_tap_half_ang` | RF tap half-angle | `(rf_tap_pitch / 2) / rf_land_r_mean * 180 / PI` | deg | = 6.273° | → 98.73° / 111.27° |
| `rf_tap_ang_1` | RF tap 1 angle | `ang_rf_land - rf_tap_half_ang` | deg | = 98.73° (spec: 98.7°) | — |
| `rf_tap_ang_2` | RF tap 2 angle | `ang_rf_land + rf_tap_half_ang` | deg | = 111.27° (spec: 111.3°) | — |
| `z_top` | Top face Z (part local) | `cp_thk` | mm | Datum A at Z=0 | `cp_thk` |
| `asm_z_offset` | Assembly Z placement | `20.0` | mm | Vol 00 §4.2 | Assembly only |

## 3.6 Tolerance Reference Parameters (non-driving, for drawing)

| Name | Expression | Source |
|---|---|---|
| `tol_thk` | `0.030` | CP-D02 |
| `tol_flat_face` | `0.015` | CP-D03/D04 |
| `tol_pad_coplanar` | `0.010` | CP-D17 |
| `tol_pos_kin` | `0.020` | CP-D11 |
| `tol_pos_liftpin` | `0.050` | CP-D13 |
| `tol_perp_liftpin` | `0.030` | CP-D14 |
| `tol_pos_choke` | `0.200` | Vol 01 §9 |
| `tol_pos_he` | `0.100` | Vol 01 §9 |
| `tol_flat_rf` | `0.020` | CP-D18 |
| `tol_flat_seal` | `0.010` | CP-D16 |
| `tol_runout_od` | `0.200` | Vol 01 §9 |

---

# 4 Feature Strategy

Timeline order. **Order is binding** — it mirrors the manufacturing sequence so that suppressing a HOLD group does not orphan downstream features.

| # | Feature | Purpose | Parent | Referenced Geometry | Manufacturing Reason | Downstream Dependency |
|---|---|---|---|---|---|---|
| 01 | User parameters import | Establish single source of truth | — | — | All dims traceable | Every feature |
| 02 | Sketch S1 — outer profile | Plate envelope | Origin XY | Origin point | Rough turn OD | 03 |
| 03 | Extrude `cp_thk` (+Z, New Body) → `CP_BODY` | Base solid | 02 | S1 profile | Plate stock | All |
| 04 | Construction plane `PL_TOP` @ `cp_thk` | Top-face work plane | 03 | XY offset | Choke side | 13, 20, 21 |
| 05 | Sketch S2 — datum & clocking construction | Bolt circles + angular rays, construction only | Origin XY | Origin, axes | Establishes Datums B/C reference | 06–24 |
| 06 | *(was H1 — discharged)* Sketch S3 — channel centreline | Serpentine path | Origin XY | S2 circles Ø60/Ø250 | Milled into bottom face | 07 |
| 07 | *(was H1 — discharged)* Sweep/pocket channel | Coolant circuit | 06 | S3 path, `ch_width`, `ch_depth` | CNC mill | 08, 26 |
| 08 | *(was H1 — discharged)* Lid body `CP_LID` | FSW closure | 07 | Channel footprint, `lid_thk` | FSW, no filler | 26 |
| 09 | Ring tapped holes, 8× | Support Ring upper circuit | 03 | S2 `bc_ring`, `ang_ring_0`+n·45 | Tapped from bottom | Assembly |
| 10 | *(was H2 — discharged)* Kinematic locators, bottom 3× | Ring centering | 03 | S2 `bc_kin_btm`, 60/180/300 | Precision bore/counterbore | **Datums B, C** |
| 11 | *(was H2 — discharged)* Kinematic locators, top 3× | Heater Plate centering | 04 | S2 `bc_kin_top`, **75/195/315** | Same setup as 10 | Assembly |
| 12 | Choke slots, 16× radial | M5 clearance with radial float | 03 | S2 `bc_choke_out`/`bc_choke_in` | Slot mill | 13 |
| 13 | *(was H3 — discharged)* Choke counterbores, 16× | M5 head + Belleville seat | 12 | Coaxial with 12 | Counterbore | Assembly |
| 14 | Central bore Ø10.0 H8 | Vacuum port pilot | 03 | Origin axis | Reamed | 15, 16 |
| 15 | Vacuum sealing face (Ø18–Ø32 flat) | Face-seal land | 03 | Bottom face annulus | Lapped, masked | Masking |
| 16 | Vacuum port taps, 4× M4 | Port retention | 03 | S2 `bc_vac` | Tapped | Assembly |
| 17 | Lift pin bores, 3× Ø8.0 H8 | Pin pass-through | 03 | S2 `bc_liftpin` | Honed, 0.030 perp | 18 |
| 18 | Bushing counterbores, 3× Ø12 H7 × 6 | SEWCP-601 seat | 17 | Coaxial with 17 | Counterbore from below | Assembly |
| 19 | HV feed bores, 2× Ø8.0 | ESC HV routing | 03 | S2 `bc_hv` | Drilled, alumina-lined | Assembly |
| 20 | RF land pocket | Flat conductive land | 03 | S2 `bc_rf`, `ang_rf_land` | Face mill, masked | 21, Masking |
| 21 | RF taps, 2× M6 | Strap terminal | 20 | `rf_tap_ang_1/2` @ `rf_land_r_mean` | Tapped into solid material | Assembly |
| 22 | RTD blind bores, 3× Ø1.7 × 12 | Sensor ports | 03 | S2 `rtd_r_n` / `rtd_ang_n` | Drilled | 23 |
| 23 | RTD cross-vents, 3× | **DR-6 / DR-13** no virtual leak | 22 | Intersecting 22 | Cross-drilled | Pump-down qual |
| 24 | RTD retainer taps, 6× M4 | Sensor retainer mounting | 03 | ±`rtd_tap_offset` from each port | Tapped | Assembly |
| 25 | *(was H3 — discharged)* Coolant stub bores, 2× | VCR gland interface | 07 | Radial @ 255°/285° | Bored, orbital-weld prep | 26 |
| 26 | *(was H1 — discharged)* Combine `CP_BODY` + `CP_LID` | Represent welded assembly | 08, 25 | Both bodies | FSW joint | Mass, assembly |
| 27 | Edge breaks / deburr features | Handling, particle control | 26 | All external edges | Deburr | — |
| 28 | Sketch S9 — top-face masking zones | 16× Ø22 pads + full top face | 04 | S2 choke BCs | **Masking drawing sheet** | Drawing |
| 29 | Sketch S10 — bottom-face masking zones | RF land, sealing face, locator bores | 03 | 15, 20 | **Masking drawing sheet** | Drawing |
| 30 | Appearance / physical material 6061-T6 | Mass verification | 26 | Body | Vol 01 §7 | Mass ≤ 4.2 kg |

**Critical strategy note — features 28/29:** the choke pads (CP-D17) are **not raised geometry.** The SEWCP-301 washers are 1.50 mm thick and sit directly on the flat top face, creating the 1.50 mm vacuum gap (Vol 00 §4.2; HP-IF-1). The pads are **surface-treatment and coplanarity zones**, not extrusions. Modelling them as raised bosses would introduce a 1.50 mm error into the Z-stack. They are captured as sketch regions for the masking drawing only.

---

# 5 Sketch Plan

| Sketch | Plane | Projected Geometry | Construction Geometry | Driving Dimensions | Constraints | Reference Parameters | Expected Status |
|---|---|---|---|---|---|---|---|
| **S1** Outer profile | XY (bottom face, Z=0) | Origin point | — | Ø`cp_od` | Concentric to origin | `cp_od` | **Fully constrained** |
| **S2** Datum & clocking | XY | Origin point, X axis | 9 construction circles (`bc_*`); 3 construction circles at `rtd_r_n`; angular construction lines at every clocked position | All BC diameters; all angles from +X | Circles concentric to origin; lines coincident to origin, angle-dimensioned to X axis | All `bc_*`, all `ang_*`, all `rtd_r_*` | **Fully constrained** |
| **S3** Channel centreline *(was H1 — discharged)* | XY | S2 circles Ø`ch_env_id`, Ø`ch_env_od`; all keep-out feature centres | Serpentine polyline/arc chain | Arc radii ≥ `ch_bend_r`; keep-out offsets per Vol 01 §3.1 | Tangent continuity at every junction; symmetric where applicable | `ch_env_id`, `ch_env_od`, `ch_bend_r` | **Fully constrained — BLOCKED** |
| **S4** Lid profile *(was H1 — discharged)* | XY | Channel footprint from S3 | — | `lid_thk` (extrusion) | Offset from channel profile | `lid_thk` | **discharged** — ECR-D-002 dispositioned |
| **S5** Bottom pattern A | XY | S2 `bc_ring`, `bc_vac`, `rtd_r_n` circles + angular rays | — | 8× M6 @ `bc_ring`; 4× M4 @ `bc_vac`; 3× Ø`rtd_bore` | Point-on-circle + coincident to angular ray | `bc_ring`, `bc_vac`, `rtd_*` | **Fully constrained** |
| **S6** Bottom pattern B | XY | S2 `bc_liftpin`, `bc_hv` circles + rays; origin | — | 3× Ø`lp_bore`; 2× Ø`hv_bore`; 1× Ø`he_bore` | Point-on-circle + ray; He bore concentric to origin | `bc_liftpin`, `bc_hv`, `he_bore` | **Fully constrained** |
| **S7** Choke slot pattern | XY | S2 `bc_choke_out`, `bc_choke_in` + 16 rays | Radial slot centrelines | `choke_slot_w` × `choke_slot_l`, radial orientation | Slot centreline collinear with radial ray; symmetric about BC | `bc_choke_*`, `choke_slot_*` | **Fully constrained** |
| **S8** RF land | XY | S2 `bc_rf` circle, `ang_rf_land` ray | Radial bounds `rf_land_r_in` / `rf_land_r_out`; angular bounds ±`rf_land_half_ang` | Land boundary arcs and radial edges; 2× M6 at `rf_tap_ang_1/2` | Arcs concentric to origin; symmetric about the 105° ray | `bc_rf`, `rf_land_*`, `rf_tap_*` | **Fully constrained** |
| **S9** Top masking zones | `PL_TOP` | S2 `bc_choke_out`, `bc_choke_in` + 16 rays | — | 16× Ø`choke_pad_dia`; full-face boundary Ø`cp_od` | Concentric to each choke position | `choke_pad_dia`, `bc_choke_*` | **Fully constrained** |
| **S10** Bottom masking zones | XY | RF land boundary (S8); sealing annulus Ø`vac_seal_id`/Ø`vac_seal_od`; locator bores | — | Annulus diameters | Concentric to origin | `vac_seal_id`, `vac_seal_od` | **Fully constrained** (locator zones **HOLD H2**) |
| **S11** Kinematic locators *(was H2 — discharged)* | XY and `PL_TOP` | S2 `bc_kin_btm`, `bc_kin_top` + 6 rays | — | **Ø10.000 H7 × 3.00 counterbore + coaxial M4 × 0.7 tap.** Bottom Ø306 BC @ 60/180/300; top Ø260 BC @ **75/195/315** | Point-on-circle + ray | `bc_kin_btm`, `bc_kin_top` | **discharged** — ECR-D-001 A, ECR-D-007 action 3, ECR-D-010 |
| **S12** Coolant stubs *(was H3 — discharged)* | Radial planes @ 255°, 285° | Channel cross-section from S3 | Stub bore axis | Ø10.0 H9 at 11.00 above Datum A; Ø14.0 H8 × 4.0 weld prep at the OD | **Coaxial** with the locally deepened channel | `ang_coolant_*` | **discharged** — CP-D22…CP-D25 |

**Sketch discipline:** every sketch fully constrained before the next feature is created. No sketch consumes a face of a HOLD feature. S2 is the single source of all angular and radial location — no sketch re-derives a bolt circle independently.

---

# 6 Fusion 360 Modeling Sequence

| # | Operation | Selections | Parameters | Fusion Command | Expected Result | Verification Checkpoint |
|---|---|---|---|---|---|---|
| 6.01 | Create design | — | Units mm | File → New Design; Document Settings → mm | Empty design, mm | Units display "mm" |
| 6.02 | Import parameters | `params/generated/SEWCP-200.csv` | §3 table | Modify → Change Parameters → Import | All §3 params listed, no errors | Parameter count matches §3; `lid_check` = **0.0** |
| 6.03 | Rename component | Root | — | Browser → rename → `SEWCP-200_COOLING_PLATE` | Named component | Name matches part number |
| 6.04 | Sketch S1 | XY plane | `cp_od` | Create Sketch → Center Diameter Circle | Ø320 circle | Sketch fully constrained (black) |
| 6.05 | Extrude base | S1 profile | `cp_thk`, direction +Z | Create → Extrude, Operation: New Body | Ø320 × 20 disc | Body name `CP_BODY`; height = `cp_thk` |
| 6.06 | Construction plane | XY plane | offset `cp_thk` | Construct → Offset Plane | `PL_TOP` at Z=20 | Plane coincident with top face |
| 6.07 | Sketch S2 | XY plane | All `bc_*`, `ang_*`, `rtd_r_*` | Create Sketch → construction circles + lines | Full clocking framework | **Fully constrained; visually verify no two features co-located** |
| 6.08 | **HOLD H1 — suppress** | — | — | Insert placeholder group, mark suppressed | Timeline placeholder for 6.09–6.12 | Group labelled `HOLD_H1_ECR-D-002` |
| 6.09 | *(H1)* Sketch S3 channel | XY plane | `ch_env_id`, `ch_env_od`, `ch_bend_r` | Create Sketch → path | Serpentine centreline | **discharged** |
| 6.10 | *(H1)* Channel pocket | S3 path | `ch_width`, `ch_depth`, `ch_z_btm` | Create → Sweep / Extrude Cut | Channel in bottom face | **discharged** |
| 6.11 | *(H1)* Sketch S4 + lid | Channel footprint | `lid_thk` | Create → Extrude, New Body | `CP_LID` | **discharged** |
| 6.12 | *(H1)* Channel fillets | Channel edges | `ch_corner_r` | Modify → Fillet | R3 min all corners | **discharged** |
| 6.13 | Sketch S5 | XY (bottom face) | `bc_ring`, `bc_vac`, `rtd_*` | Create Sketch, project S2 | Hole centres placed | Fully constrained |
| 6.14 | Ring tapped holes | 8 points from S5 | M6×1.0, `ring_tap_depth` | Create → Hole, Type: Tapped, ISO Metric Profile | 8× M6 × 12 deep, bottom face | Count = 8; angles 22.5+n·45; depth = 12 |
| 6.15 | Vacuum port taps | 4 points from S5 | M4×0.7, `vac_tap_depth` | Create → Hole, Tapped | 4× M4 × 10 deep @ Ø38 BC | Count = 4; BC = 38 |
| 6.16 | RTD blind bores | 3 points from S5 | Ø`rtd_bore` H8, `rtd_depth` | Create → Hole, Simple, Flat bottom | 3× Ø1.7 × 12 blind | Radii 40/100/140; angles 75/165/225 |
| 6.17 | RTD cross-vents | 3 radial sketches | Ø`rtd_vent_dia`, through to OD or channel-free face | Create → Hole, Simple, To Object | 3 vents intersecting each blind bore | **DR-6/DR-13: every blind bore vented** |
| 6.18 | RTD retainer taps | 6 points, ±`rtd_tap_offset` | M4×0.7, `rtd_tap_depth` | Create → Hole, Tapped | 6× M4 × 8 deep | 2 per RTD port, ±9 mm |
| 6.19 | Sketch S6 | XY (bottom face) | `bc_liftpin`, `bc_hv`, `he_bore` | Create Sketch, project S2 | Bore centres placed | Fully constrained |
| 6.20 | Central He bore | Origin point | Ø`he_bore` H8, through | Create → Hole, Simple, All | Ø10.0 through, on axis | Concentric to origin within 0.000 |
| 6.21 | Vacuum sealing face | Bottom face annulus | Ø`vac_seal_id` – Ø`vac_seal_od` | Create → Extrude Cut, 0.1 relief *or* face split | Defined flat land Ø18–Ø32 | Face isolated for masking + flatness callout |
| 6.22 | Lift pin bores | 3 points from S6 | Ø`lp_bore` H8, through | Create → Hole, Simple, All | 3× Ø8.0 through | BC 200; angles 30/150/270 |
| 6.23 | Bushing counterbores | Coaxial with 6.22 | Ø`lp_cbore` H7, `lp_cbore_dep` | Create → Hole, Counterbore, from bottom | 3× Ø12 × 6 deep | Depth = 6.0 = bushing length |
| 6.24 | HV feed bores | 2 points from S6 | Ø`hv_bore`, through | Create → Hole, Simple, All | 2× Ø8.0 through @ Ø60 BC | Angles 0/180 |
| 6.25 | Sketch S7 | XY (bottom face) | `bc_choke_*`, `choke_slot_*` | Create Sketch → slot profiles | 16 radial slots | Fully constrained; slot axes radial |
| 6.26 | Choke slots | 16 profiles from S7 | Through all | Create → Extrude Cut, All | 16× 5.5 × 7.0 radial slots | Count = 16 (12 @ Ø270, 4 @ Ø90) |
| 6.27 | **HOLD H3 — suppress** | — | — | Placeholder group | Timeline placeholder for 6.28 | Group labelled `HOLD_H3_ECR-D-003/004` |
| 6.28 | *(H3)* Choke counterbores | Coaxial with 6.26, **bottom face** | `choke_cbore_w` × `choke_cbore_l` × `choke_cbore_dep`, **radially slotted** | Extrude Cut from a slot sketch | 16 slotted counterbores | **discharged** — CP-D26; anodize-masked floors |
| 6.29 | Sketch S8 | XY (bottom face) | `rf_land_*`, `rf_tap_*` | Create Sketch, project S2 | RF land boundary + 2 tap points | Fully constrained; symmetric about 105° |
| 6.30 | RF land pocket | S8 land profile | Depth 0.5 relief (face definition) | Create → Extrude Cut | Isolated flat land, 60 × 18 | Land spans r 128–146, 92.45°–117.55° |
| 6.31 | RF taps | 2 points from S8 | M6×1.0, `rf_tap_depth` | Create → Hole, Tapped | 2× M6 × 12 deep | Angles 98.73° / 111.27° at r = 137 |
| 6.32 | **HOLD H2 — suppress** | — | — | Placeholder group | Timeline placeholder for 6.33–6.34 | Group labelled `HOLD_H2_ECR-D-001` |
| 6.33 | *(H2)* Locators, bottom 3× | S11 @ `bc_kin_btm` | **RESOLVED** | Create → Hole | 3 features @ 60/180/300 | **Establishes Datums B/C** — discharged |
| 6.34 | *(H2)* Locators, top 3× | S11 @ `bc_kin_top` | Ø`kin_cbore_d` H7 × `kin_cbore_dep`, then M4 × 0.7 tap | Create → Hole | 3 features @ **75/195/315** | **discharged** — ECR-D-010 re-clocked these off the choke rays |
| 6.35 | *(H3)* Coolant stub bores | S12 radial planes | Ø`stub_bore_d` at `stub_bore_z`, then Ø`stub_wp_d` × `stub_wp_dep` at the OD | Create → Hole | 2 radial bores @ 255°/285° | **discharged** — CP-D22/D23/D24; channel locally deepened to `ch_depth_port` |
| 6.36 | *(H1)* Combine bodies | `CP_BODY` + `CP_LID` | Operation: Join | Modify → Combine | Single welded solid | **discharged** |
| 6.37 | Edge breaks | All external edges | 0.5 × 45° | Modify → Chamfer | Deburred edges | No sharp external edges |
| 6.38 | Sketch S9 top masking | `PL_TOP` | `choke_pad_dia`, `bc_choke_*` | Create Sketch, project S2 | 16× Ø22 pad zones + full-face zone | **Pads are zones, NOT extrusions** — verify no material added |
| 6.39 | Sketch S10 bottom masking | XY | RF land, sealing annulus | Create Sketch | Masking zones defined | Zones match 6.21, 6.30 |
| 6.40 | Assign material | Body | 6061-T6, ρ = 2700 | Modify → Physical Material | Aluminium 6061 | — |
| 6.41 | Mass check | Body | — | Inspect → Physical Properties | Mass reported | **≤ `cp_mass_max` (4.2 kg); spec estimate 4.0 kg** |
| 6.42 | Save + version | — | — | File → Save, milestone `gate/G2` | Versioned design | Version named to match Git tag |
| 6.43 | Export STEP | Body | — | File → Export → STEP | `SEWCP-200_revX1.step` | Committed to `cad/exports/step/` |

---

# 7 Manufacturing Review

| Feature | Manufacturing Process | Tool Accessibility | Tolerance Sensitivity | Inspection Method | Why the Feature Exists |
|---|---|---|---|---|---|
| **Plate OD Ø320** | Rough turn → finish turn | Unobstructed | Low (±0.10) | CMM / micrometer | Envelope; ≥5 mm wall from channel to external surface |
| **Overall thickness 20.000** | Grind / lap after anodize | Both faces open | **Very high (±0.030)** — Z-stack element | Micrometer, 8 points at 45°, Ø280 BC | Sets wafer plane height; feeds DR-3 Support Ring lap calculation |
| **Top face flat 0.015 / parallel 0.015** | Final lap, performed **after** anodize (Vol 01 §6 step 14) | Full face open | **Very high** — propagates directly to wafer plane | CMM, optical flat | 15 µm of the 50 µm wafer-plane flatness budget |
| **Coolant channel *(was H1)*** | CNC mill into bottom face, R5 min bend, R3 min corners | Open face before FSW — this is why the channel is on the bottom | Medium (+0.20/−0) | Borescope; flow test; radiography of weld | Re ≈ 8,300 turbulent flow; 3 kW heat removal |
| **FSW lid *(was H1)*** | Friction stir weld, circumferential + internal rib passes | Requires flat, rigid backing | Medium (±0.10) | Dye penetrant + radiography; 6 bar proof; He leak | Eliminates elastomer from the coolant pressure boundary (catastrophic-severity failure mode) |
| **Choke pads, 16× Ø22** | Lapped with the top face, masked from anodize | Same setup as top face | **High** — coplanar 0.010 TIR as a set | CMM height map across all 16 | Contact conductance is 53% of R_choke; anodize would make it unpredictable |
| **Choke slots, 16× 5.5 × 7.0** | Slot mill, through | Bottom face, unobstructed | **Deliberately low (⌖ Ø0.200)** | Pin gauge / CMM | Allows 0.399 mm radial growth of the Heater Plate without over-constraining the joint |
| **Ring taps, 8× M6 × 12** | Drill + tap, bottom face | Unobstructed | Low (⌖ Ø0.30) | Thread gauge | RF-side bolt circuit (DR-9); never reaches the Base Plate |
| **Kinematic locators, 6× *(was H2)*** | Precision bore/counterbore, single setup | Both faces — **must be same setup to hold ⌖ Ø0.020** | **Highest positional on the part** | CMM | Chuck axis concentricity; Datums B and C |
| **Lift pin bores, 3× Ø8.0 H8** | Drill → ream → hone | Through, unobstructed | High (perpendicularity 0.030) | Bore gauge; perpendicularity on CMM | Pin pass-through; **perpendicularity prevents ceramic pin bind and fracture** |
| **Bushing counterbores, 3× Ø12 H7 × 6** | Counterbore from bottom | Unobstructed | High (H7 press fit) | Bore gauge | Seats SEWCP-601 Vespel bushing; depth = bushing length exactly |
| **Central bore Ø10.0 H8** | Drill → ream | On axis, unobstructed | Medium | Bore gauge | Receives the Ø9.90 h8 vacuum port pilot spigot |
| **Vacuum sealing face Ø18–Ø32** | Face mill → lap, masked | Bottom face, unobstructed | **High** (flat 0.010, Ra 0.8–1.6) | Optical flat; surface roughness | Face seal against the 316L port flange O-ring; **anodize here is a rejection** |
| **RF land 60 × 18** | Face mill, masked, Alodine only | Bottom face, unobstructed | High (flat 0.020) | Surface plate; contact resistance 4-wire | Contact resistance ≤ 0.5 mΩ at 13.56 MHz; **anodize would open-circuit the joint** |
| **RF taps, 2× M6 × 12** | Drill + tap into solid material | Requires channel keep-out — this is why the envelope was pulled to Ø250 | Medium | Thread gauge | RF strap terminal; needs solid metal, not lid material |
| **RTD blind bores, 3× Ø1.7 × 12** | Small-diameter drill, flat bottom | Bottom face; high L/D (7:1) — **peck drilling required** | High (H8) | Pin gauge; borescope | RTD probe response ≤ 5 s |
| **RTD cross-vents, 3×** | Cross-drill intersecting each blind bore | Radial access | Low | Airflow / borescope | **DR-6 / DR-13** — a Ø1.7 × 12 blind bore with a Ø1.6 probe in it is a near-perfect virtual leak |
| **HV feed bores, 2× Ø8.0** | Drill through | Unobstructed | Low | Bore gauge | ESC HV routing; alumina-lined after machining |
| **Coolant stubs, 2× *(was H3)*** | Deep radial bore through 35 mm of solid; orbital weld | Radial from OD; deep-hole drilling | Ø10.0 H9, CL 11.00 above A; Ø14.0 × 4.0 weld prep | He leak test | SEWCP-201 transition joint, then ½ in. VCR |
| **Hard anodize, 50 µm** | Type III, sealed, after all machining, **before** final lap | Masked: top face, 16 pads, RF land, channel interior, sealing face, locator bores | Medium | Coating thickness; borescope of channel | Plasma and handling durability of the RF-hot body |

**Overriding manufacturing constraint (Vol 01 §6):** *stress relief is called out twice and is not optional.* A 20 mm 6061 plate with a channel milled through most of its lower face will move. The sequence is rough → relieve → semi-finish → relieve → finish → anodize → lap. **The final lap is the last operation.**

---

# 8 Failure Prevention

## 8.1 Common Modeling Mistakes

| Mistake | Detection | Recovery |
|---|---|---|
| **Modelling choke pads as raised bosses** | Top face is not planar; Inspect → Section shows 1.5 mm steps; assembly Z-stack off by 1.5 mm | Delete the extrusion. Pads are surface-treatment zones only (S9). The 1.5 mm gap comes from the SEWCP-301 washer thickness, not from plate geometry. |
| Sketching the RF land at 75° | Land overlaps outer choke fasteners at 60°/90° | Vol 00 §3.2 **table** is controlling: 105°. The §3.2 narrative paragraph is stale (ECR-Q-003). |
| RTD ports placed at 105°/225°/345° | Port at r=140/105° collides with the RF land | Vol 00 §3.2 **table** and Vol 01 CP-IF-9 are controlling: 75°/165°/225°. |
| Kinematic locators at Ø288 BC | Locators miss the Support Ring slots at Ø306 | Vol 00 §3.1 Datum E is stale (ECR-Q-001). Ø306 is confirmed by Vol 00 §3.2, Vol 01, Vol 03 SR-IF-4, Vol 06 §3.1. |
| Modelling an O-ring groove on the bottom face | Groove interferes with the port flange groove | The groove is in the 316L port flange (CP-IF-5, Vol 07 §12). Vol 01 §6 step 9 and §9 are stale (ECR-Q-004). |
| Choke slots oriented tangentially | Heater Plate cannot grow radially; joint over-constrains | Slot major axis must be **radial**. Verify each slot centreline is collinear with its radial ray in S7. |
| RTD blind bores left unvented | Passes CAD, fails pump-down qualification | DR-6/DR-13 — 6.17 is mandatory, not optional. |

## 8.2 Assembly Mistakes

| Mistake | Detection | Recovery |
|---|---|---|
| Cooling Plate placed at Z=0 in the assembly | Wafer plane lands at 35.920 instead of 55.920 | Bottom face at **Z = 20.000** (Vol 00 §4.2), on the Support Ring top face. |
| Rigid joints at the kinematic locators | Motion study shows no radial freedom; thermal growth over-constrains | Locators must be **slider** joints with ≥ ±1.0 mm radial travel (Vol 06 §2.1). |
| Choke fasteners modelled as rigid | Heater Plate cannot float | Slotted holes + Belleville — the joint is located by the locators, not the fasteners. |
| Plate contacts the Base Plate | Isolation destroyed; DR-1 violated | **No direct contact.** Load path is Base Plate → Support Ring → Cooling Plate only. |
| Choke washers omitted from the stack | Heater Plate sits on the top face; 1.5 mm gap lost | 16× SEWCP-301 at 1.500 mm between the plates. |

## 8.3 Dimension Mistakes

| Mistake | Detection | Recovery |
|---|---|---|
| Channel + wall + lid ≠ plate thickness | `lid_check` parameter is non-zero | The 8+8+6=22 form was ECR-D-002 and is **closed**: 6 + 8 + 6 = 20.000 (APR-019). The guard stays — a non-zero `lid_check` means someone has edited one Z dimension without the others. |
| Locator protrusion greater than the 3.00 mm slot depth | Locator bottoms out; mating faces held apart | **Closed** — ECR-D-001 disposition A: `AP-D02` = 2.50 ± 0.05 governs and `spec/01` §10 step 3 now agrees. The guard stays; `spec/06` §5.1 calls this the callout most likely to be got wrong. |
| RF tap angles entered as literals | Drift from `bc_rf` if the BC ever changes | Use `rf_tap_ang_1/2` expressions; they resolve to 98.73°/111.27° against the spec's rounded 98.7°/111.3°. |
| Ring taps at Ø296 BC | Misses the Support Ring flange holes | Ø302 BC (CP-IF-2, FBA-3, SR-IF-3). Vol 00 §3.1 Datum B/C at Ø296 is stale (ECR-Q-002). |
| Bushing counterbore depth ≠ 6.0 | Bushing proud or recessed | Depth = bushing length (LB-D03) exactly. |

## 8.4 Reference Mistakes

| Mistake | Detection | Recovery |
|---|---|---|
| Sketches referencing model faces instead of S2 | Edits cascade unpredictably; features drift | All angular/radial location derives from **S2 only**. Project S2, never a face edge. |
| Downstream sketch consuming a HOLD feature's face | Suppressing H1/H2/H3 breaks the timeline | Verify by suppressing each HOLD group — nothing downstream may error. |
| Hardcoded literals in place of parameters | Parameter change does not propagate | Modify → Change Parameters, alter `cp_od` by 1 mm, confirm the model updates, then undo. |
| Cross-referencing another part's model | Circular dependency between components | This part is the interface hub — it **exports** geometry, never imports it. |

## 8.5 Timeline Mistakes

| Mistake | Detection | Recovery |
|---|---|---|
| Fillets applied before hole features | Fillet fails or produces bad geometry when holes intersect | Fillets last (6.37), after all cutting features. |
| Combine (6.36) executed before stub bores (6.35) | Stub bores cannot break into the channel | Order is binding: stubs → combine. |
| HOLD placeholders deleted rather than suppressed | Timeline must be restructured when ECRs close | Keep suppressed placeholder groups; they preserve insertion position. |
| Masking sketches created before their parent faces | Zones do not match the machined land boundaries | S9/S10 after 6.21 and 6.30. |

---

# 9 Verification Checklist

All items **PASS / FAIL**. No partial states.

## 9.1 Geometry Verification

| # | Check | Criterion | Status |
|---|---|---|---|
| G-01 | Body count | 1 (or 2 pre-Combine) | ☐ |
| G-02 | Overall diameter | Ø320.0 | ☐ |
| G-03 | Overall thickness | 20.000 | ☐ |
| G-04 | Top face planar, no raised pads | 0 steps | ☐ |
| G-05 | Ring taps | 8, Ø302 BC, 22.5°+n·45°, M6 × 12 | ☐ |
| G-06 | Choke slots | 16 (12 @ Ø270 + 4 @ Ø90), radial orientation | ☐ |
| G-07 | Lift pin bores | 3, Ø8.0, Ø200 BC, 30/150/270 | ☐ |
| G-08 | Bushing counterbores | 3, Ø12 × 6 deep, from bottom | ☐ |
| G-09 | HV bores | 2, Ø8.0, Ø60 BC, 0/180 | ☐ |
| G-10 | Central bore | Ø10.0, on axis | ☐ |
| G-11 | Vacuum taps | 4, M4 × 10, Ø38 BC | ☐ |
| G-12 | Sealing face | Isolated flat, Ø18–Ø32 | ☐ |
| G-13 | RF land | 60 circ × 18 radial, r 128–146, centred 105° | ☐ |
| G-14 | RF taps | 2, M6 × 12, r=137, 98.73°/111.27° | ☐ |
| G-15 | RTD bores | 3, Ø1.7 × 12 blind, r=40/100/140 @ 75/165/225 | ☐ |
| G-16 | **RTD cross-vents** | 3, every blind bore vented (DR-6/DR-13) | ☐ |
| G-17 | RTD retainer taps | 6, M4 × 8, ±9 mm | ☐ |
| G-18 | No feature collisions | Zero interference between any two features | ☐ |
| G-19 | *(was H1)* Channel within Ø60–Ø250 envelope | No violation | ☐ |
| G-20 | *(was H1)* Keep-out table, all 8 classes | No violation | ☐ |
| G-21 | *(was H2)* Kinematic locators | 6, Ø306 btm / Ø260 top | ☐ |
| G-22 | *(was H3)* Coolant stubs | 2, @ 255°/285° | ☐ |

## 9.2 Parameter Verification

| # | Check | Criterion | Status |
|---|---|---|---|
| P-01 | All §3 parameters present | Count matches | ☐ |
| P-02 | Zero hardcoded dimensions | All driven by parameters | ☐ |
| P-03 | Derived params are expressions | `rf_tap_ang_*`, `rf_land_r_*`, `ch_z_*` | ☐ |
| P-04 | `rf_tap_ang_1` | 98.73° | ☐ |
| P-05 | `rf_tap_ang_2` | 111.27° | ☐ |
| P-06 | `rf_land_half_ang` | 12.547° | ☐ |
| P-07 | **`lid_check`** | **Must = 0.** Now 0.0 | ☐ |
| P-08 | Parameter propagation test | Change `cp_od`, model rebuilds, undo | ☐ |
| P-09 | Every parameter cites a spec source | Comment field populated | ☐ |

## 9.3 Assembly Verification

| # | Check | Criterion | Status |
|---|---|---|---|
| A-01 | Bottom face at assembly Z | 20.000 | ☐ |
| A-02 | Top face at assembly Z | 40.000 | ☐ |
| A-03 | Ring taps align to SR-IF-3 clearance holes | 8/8 | ☐ |
| A-04 | Choke slots align to HP-IF-2 tapped holes | 16/16 | ☐ |
| A-05 | Choke pads receive SEWCP-301 washers | 16/16, Ø22 on Ø22 | ☐ (see ECR-Q-007) |
| A-06 | Central bore receives Ø9.90 h8 pilot | Clearance present | ☐ |
| A-07 | Lift pin bores align to ESC Ø5.200 bores | 3/3 concentric within tolerance | ☐ |
| A-08 | Bushing seats receive Ø12.00 bushing | Press fit achievable | ☐ |
| A-09 | No contact with Base Plate | Zero | ☐ |
| A-10 | *(was H2)* Locators engage Ring slots (Ø306) and Heater slots (Ø260) | 6/6, slider joints, ±1.0 mm travel | ☐ |

## 9.4 Manufacturing Verification

| # | Check | Criterion | Status |
|---|---|---|---|
| M-01 | All tapped holes ≥ 2×D engagement | Yes | ☐ |
| M-02 | All blind bores vented | 3/3 | ☐ |
| M-03 | Tool access to every feature | No enclosed volumes requiring EDM | ☐ |
| M-04 | Masking zones defined | 5 zones (top face+pads, RF land, channel, sealing face, locator bores) | ☐ |
| M-05 | Mass | ≤ 4.2 kg | ☐ |
| M-06 | Material assigned | 6061-T6, ρ 2700 | ☐ |
| M-07 | *(was H1)* Channel min wall to every feature | Per keep-out table | ☐ |
| M-08 | *(was H3)* Coolant stub weld access | Orbital weld head clearance | ☐ |

## 9.5 Drawing Readiness

| # | Check | Criterion | Status |
|---|---|---|---|
| D-01 | Datum A/B/C definable on the model | **Requires H2 resolution** | ☐ |
| D-02 | All CP-D01…D21 dimensionable | Yes | ☐ |
| D-03 | Masking sheet geometry available | S9, S10 complete | ☐ |
| D-04 | Section planes identified | Channel, RF land, RTD port | ☐ |
| D-05 | Detail views identified | RF land, RTD port + vent, bushing counterbore | ☐ |

## 9.6 Release Readiness

| # | Check | Criterion | Status |
|---|---|---|---|
| R-01 | Zero open ECR-D | **4 open** | ☐ **FAIL** |
| R-02 | All HOLD groups resolved and unsuppressed | 3 open | ☐ **FAIL** |
| R-03 | Model rebuilds with zero errors/warnings | Yes | ☐ |
| R-04 | STEP exported and committed | Yes | ☐ |
| R-05 | Conformance report generated vs. §5 of Vol 01 | Yes | ☐ |
| R-06 | Design Authority review complete | WBS 3.2 requires DAR | ☐ |

---

# 10 Drawing Package Requirements

**Drawing number:** SEWCP-200 · **Standard:** ASME Y14.5-2018 · **Sheets:** 4

## 10.1 Sheet Structure

| Sheet | Title | Scale | Content |
|---|---|---|---|
| 1 | Geometry & Datums | 1:2 | Principal views, datums, envelope, thickness |
| 2 | **Masking & Surface Treatment** | 1:2 | All five non-anodize zones — **mandatory sheet** |
| 3 | Coolant Circuit | 1:2 | Channel routing, sections, FSW joint, stubs |
| 4 | Feature Detail & Hole Schedule | 1:1 / details | Hole table, detail views, GD&T |

## 10.2 Views

| View | Sheet | Purpose |
|---|---|---|
| Bottom face (primary) | 1 | Datum A face; majority of features enter from below |
| Top face | 1 | Choke pads, un-anodized zone |
| Front elevation | 1 | Thickness, stub positions |
| Isometric (shaded) | 1 | Orientation reference only, undimensioned |
| Bottom face — masking overlay | 2 | RF land, sealing face, locator bores |
| Top face — masking overlay | 2 | Full top face + 16 pads |
| Bottom face — channel superimposed (hidden) | 3 | Routing and keep-out compliance |

## 10.3 Sections

| Section | Sheet | Cuts Through | Shows |
|---|---|---|---|
| A-A | 3 | Diametral, through channel and both stubs | Channel cross-section, wall thicknesses, lid, FSW joint |
| B-B | 3 | Radial at 255° | Stub bore to channel transition |
| C-C | 1 | Through a lift pin station | Bore + bushing counterbore |
| D-D | 4 | Through an RTD port | Blind bore + cross-vent intersection |
| E-E | 1 | Through the RF land | Land depth, tap depth, solid material below |

## 10.4 Detail Views

| Detail | Sheet | Scale | Subject |
|---|---|---|---|
| DET-1 | 4 | 5:1 | RF land boundary, tap positions, flatness, Alodine note |
| DET-2 | 4 | 5:1 | RTD blind bore + cross-vent, DR-6/DR-13 note |
| DET-3 | 4 | 2:1 | Choke slot geometry, radial orientation, counterbore *(was H3)* |
| DET-4 | 4 | 2:1 | Lift pin bore + bushing counterbore, perpendicularity |
| DET-5 | 4 | 5:1 | Vacuum sealing face, flatness, lay direction, masking |
| DET-6 | 3 | 2:1 | FSW joint preparation and weld zone *(was H1)* |
| DET-7 | 4 | 5:1 | Kinematic locator feature **[discharged]** |

## 10.5 Dimensions

Every dimension in Vol 01 §5 (CP-D01 … CP-D21) appears. Placement:

| Sheet | Dimensions |
|---|---|
| 1 | CP-D01 OD, CP-D02 thickness, CP-D03/D04 flatness & parallelism, CP-D16 sealing face, CP-D18 RF land flatness, full datum frame |
| 3 | CP-D05 channel W, CP-D06 channel D, CP-D07 top wall, CP-D08 lid **[all H1]** |
| 4 | CP-D09/D10/D11 locators *(was H2)*, CP-D12/D13/D14 lift pin, CP-D15 central bore, CP-D17 pad coplanarity, CP-D19 RTD, CP-D20 ring taps |

Hole schedule table on Sheet 4: ID, Ø, depth, thread, quantity, bolt circle, angular positions, tolerance, source reference.

## 10.6 Notes

Standard notes, all sheets:
1. INTERPRET PER ASME Y14.5-2018.
2. DIMENSIONS IN MILLIMETRES.
3. MATERIAL: 6061-T651 PER VOL 01 §7.
4. BREAK ALL SHARP EDGES 0.5 × 45° MIN.
5. **ALL BLIND HOLES SHALL BE VENTED — DR-6.**
6. **DO NOT ANODIZE SURFACES INDICATED ON SHEET 2.**
7. FINAL LAP OF TOP FACE SHALL BE THE LAST OPERATION, AFTER ANODIZE.
8. STRESS RELIEVE PER VOL 01 §6 STEPS 2 AND 8 — MANDATORY.
9. NO ELASTOMER PERMITTED IN THE COOLANT PRESSURE BOUNDARY.
10. RECORD AS-BUILT THICKNESS AT 8 POINTS — FEEDS DR-3 SUPPORT RING LAP.

Sheet 2 notes:
11. TYPE III HARD ANODIZE 50 µm SEALED, EXCEPT WHERE MASKED.
12. MASKED ZONES: TOP FACE (ALL), 16× Ø22 CHOKE PADS, RF LAND, COOLANT CHANNEL INTERIOR, VACUUM SEALING FACE, LOCATOR BORES.
13. RF LAND: ALODINE 1200 CHROMATE CONVERSION ONLY.
14. TOP FACE EMISSIVITY ε ≤ 0.15 — BRIGHT AS-LAPPED.

Sheet 3 notes:
15. FRICTION STIR WELD PER VOL 01 §6 STEP 5. NO FILLER, NO FLUX.
16. NDT: DYE PENETRANT + RADIOGRAPHY.
17. HYDROSTATIC PROOF 6 BAR / 30 MIN BEFORE FINISH MACHINING.
18. HELIUM LEAK TEST < 1×10⁻⁹ mbar·L/s.
19. CHANNEL INTERIOR Ra ≤ 3.2 µm, DEBURRED.

## 10.7 Balloons and BOM

Balloons appear on the **assembly** drawing (SEWCP-000), not on the part drawing.

Items ballooned to this part in the assembly BOM:

| Item | Part No. | Description | Qty |
|---|---|---|---|
| 2 | SEWCP-200 | Cooling Plate, 6061-T651 | 1 |
| 2.1 | SEWCP-200-L | FSW Lid *(was H1)* | 1 |
| 2.2 | SEWCP-601 | Lift Pin Bushing, Vespel SP-1 | 3 |
| 2.3 | SEWCP-700 | Alignment Pin *(was H2)* | 6 |
| 2.4 | — | Alumina liner tube, HV bore | 2 |
| 2.5 | — | VCR gland stub, ½ in., 316L *(was H3)* | 2 |

BOM reference on the part drawing: material callout and finish specification only.

---

# 11 Git Commit Package

## 11.1 Suggested Commit Message

```
[WBS-3.2] SEWCP-200 Cooling Plate — CAD implementation package (X1, HOLD)

Issues the Mechanical CAD Implementation Package for Component 01,
Cooling Plate, against frozen baseline SEWCP Rev A.

Package is COMPLETE but ISSUED WITH HOLD. Baseline review identified
four blocking defects that prevent full model release:

  ECR-D-001  Alignment pin locator interface — Vol 01 and Vol 06
             specify mutually exclusive geometries at 6 locations.
             Blocks Datums B and C.
  ECR-D-002  Channel cross-section arithmetic — CP-D06 + CP-D07 +
             CP-D08 = 22.00 mm against CP-D02 = 20.000 mm.
  ECR-D-003  Coolant stub interface undimensioned in all volumes.
  ECR-D-004  Choke fastener counterbore undimensioned; specified
             M5 x 30 exceeds the 29.5 mm stack by 0.5 mm.

Eight non-blocking documentation defects logged as ECR-Q-001..008.

Approximately 82% of the part is fully determinate. Three HOLD groups
(H1 channel/lid, H2 locators, H3 stubs/counterbores) are pre-positioned
as suppressed timeline placeholders so no restructuring is required
once dispositioned.

No assumption has been made to close any defect. No dimension has been
changed. No interface has been invented.

Refs: SEWCP-ENG-002 Rev A, SEDEP-PMP-001 sec 0.1
```

## 11.2 Files Expected to Change

| Path | Action | Notes |
|---|---|---|
| `cad/SEWCP-200_CAD_Implementation_Package.md` | **add** | This document |
| `params/parts/SEWCP-200_cooling_plate.yaml` | **add** | §3 parameter master |
| `params/generated/SEWCP-200.csv` | **add** | Fusion import; `lid_check` included |
| `notebook/entries/2026/2026-08-07_ENB-0001.md` | **add** | Baseline review record |
| `notebook/queries/ECRD-001_alignment_pin_interface.md` | **add** | Blocking |
| `notebook/queries/ECRD-002_channel_cross_section.md` | **add** | Blocking |
| `notebook/queries/ECRD-003_coolant_stub_interface.md` | **add** | Blocking |
| `notebook/queries/ECRD-004_choke_counterbore_bolt_length.md` | **add** | Blocking |
| `notebook/queries/ECRQ-001..008_*.md` | **add** | Non-blocking |
| `program/open_items.md` | **modify** | Add 4 blocking ECR-D to the log |
| `program/risks.yaml` | **modify** | Raise R-16: baseline internal inconsistency |
| `traceability/rtm.csv` | **modify** | 33 features traced; 6 flagged BLOCKED |
| `dashboard/DASHBOARD.md` | **regenerate** | Change panel → RED (open ECR-D) |

**Files deliberately NOT changed:** `spec/**` — CODEOWNERS-protected. Defect correction requires a Design Authority-approved specification revision, not a working-level edit.

## 11.3 Engineering Release Notes

**SEWCP-200-CAD-001, Revision X1 — DRAFT, ISSUED WITH HOLD**

*Scope.* Complete CAD implementation package for the Cooling Plate: traceability matrix (33 features), parameter master (78 parameters), feature strategy (30 timeline entries), sketch plan (12 sketches), Fusion modelling sequence (43 operations), manufacturing review, failure prevention, verification checklist (6 categories), and drawing package definition (4 sheets).

*Status.* **Not released.** Four blocking defects identified in the frozen baseline. Modelling may proceed on the determinate 82% of the part; three HOLD groups are quarantined.

*Impact assessment.*
- **ECR-D-002** is the most serious. The channel cross-section does not close arithmetically. It affects the highest-effort feature on the part (WBS 3.2.2, 4 h) and the FSW lid design. Every downstream operation involving the channel is blocked.
- **ECR-D-001** blocks the part's Datum B and C, and therefore the drawing's entire GD&T scheme. It also affects Vol 03 and Vol 06, which contradict each other on the same interface. **Resolution must be applied to all three volumes simultaneously.**
- **ECR-D-003** and **ECR-D-004** are undimensioned interfaces rather than contradictions; they are lower-risk to disposition.
- Program impact: WBS 3.2 (Cooling Plate, 16 h, **critical path**) cannot complete. Per SEDEP-PMP-001 §3.3, tasks 3.7, 3.8, 3.10 have 16–20 h of float and should be re-sequenced forward while these ECRs are dispositioned. **Program risk R-02 (critical path slip) is now active.**

*Configuration statement.* No dimension has been changed. No interface has been invented. No architecture has been modified. Where the baseline is ambiguous or self-contradictory, the ambiguity is recorded in §12 rather than resolved at the workstation, per SEDEP-PMP-001 §0.1.

---

# 12 Open Questions

## 12.1 Blocking Defects — ECR-D Class

### ECR-D-001 — Alignment pin locator interface: two mutually exclusive geometries

**Affected features:** 6 locations (3 × Ø306 BC bottom face, 3 × Ø260 BC top face)

| Source | Specified Geometry |
|---|---|
| Vol 01 CP-IF-1, CP-IF-4 | "3× **Ø6 h6 dowels press-fit** into the … face" |
| Vol 01 CP-D09, CP-D10 | "Kinematic dowel bore … **Ø6.000 · H7 / press M6**" |
| Vol 01 §4, §6 step 12, §8, §10 step 3 | "Hosts 6 **press-fit** dowels"; "**Press-fit** 6× alignment dowels"; "Dowel bores … press-fit dimensional integrity" |
| Vol 03 SR-IF-4 | "engaging Ø6 h6 dowels **pressed into** the Cooling Plate" |
| **Vol 06 AP-IF-1** | "**Ø12.0 k6 flange in a Ø12.0 H7 × 3.0 counterbore**; **M4 × 10 SHCS** through the pin into the plate for retention" |
| **Vol 06 §5.1 (mating slot table)** | "Counterbore in Cooling Plate · **Ø12.0 H7 × 3.0** · ⌖ Ø0.020 Ⓜ · **CP-D09 / CP-D11**" |
| **Vol 06 §6, §10 step 3, §11 FM-5** | Press fit **"Rejected on thermal grounds"**; "a press is **not required and must not be used**"; "no press tooling permitted" |

**Nature of the conflict.** Vol 06 explicitly rejects, on stated engineering grounds, the press fit that Vol 01 and Vol 03 specify. The two geometries are not variants of one another — they differ in diameter (Ø6.000 vs Ø12.0), depth (through/blind bore vs 3.0 mm counterbore), and content (Vol 06 additionally requires an M4 tapped hole at each of the 6 locations, which appears nowhere in Vol 01).

**Secondary conflict — protrusion, with a geometric impossibility:**

| Source | Value |
|---|---|
| Vol 01 §10 step 3 | Dowel protrusion **5.0 ± 0.1 mm** |
| Vol 06 AP-D02 | Boss protrusion **2.50 ± 0.05 mm** |
| Vol 03 SR-D19 / Vol 02 HP-IF-3 | Mating slot depth **3.00 mm** |

A 5.0 mm protrusion into a 3.00 mm deep slot bottoms out by 2.0 mm and holds the mating faces apart — the exact failure Vol 06 §5.1 identifies as "the callout most likely to be got wrong."

**CAD impact.** Blocks 6 features. Blocks **Datum B and Datum C** (Vol 01 §9 defines both as "the Ø306 BC kinematic dowel"), and therefore the entire GD&T scheme and drawing Sheet 1. Also blocks the ⌖ Ø0.020 positional callout, which is the tightest positional tolerance on the part.

**Question for the Design Authority.** Which geometry is controlling at the 6 Cooling Plate locations — Vol 01 (Ø6.000 H7 bore, press-fit) or Vol 06 (Ø12.0 H7 × 3.0 counterbore + M4 tap, screw-retained)? **Resolution must be applied to Vol 01, Vol 03, and Vol 06 in a single change**, and must also fix the 5.0 / 2.50 protrusion conflict. Additionally: is the plate's Datum B/C feature the locator bore/counterbore itself, or the installed pin's Ø6 boss?

---

### ECR-D-002 — Coolant channel cross-section does not close arithmetically

| Ref | Dimension | Value |
|---|---|---|
| CP-D07 | Channel-to-top-face wall | 8.00 ±0.20 |
| CP-D06 | Channel depth | 8.00 +0.20/−0 |
| CP-D08 | FSW lid thickness | 6.00 ±0.10 |
| | **Sum** | **22.00 mm** |
| CP-D02 | **Overall thickness** | **20.000 ±0.030** |
| | **Discrepancy** | **2.00 mm** |

**Corroboration.** Vol 00 §4.3 independently confirms the 8 mm top wall ("Cooling Plate to channel, 8 mm, k = 167 W/m·K"). Vol 01 §2.1 independently confirms the 10 × 8 channel via the Reynolds number derivation. CP-D02 is a Z-stack-critical dimension confirmed in Vol 00 §4.2. **Three of the four values are corroborated by independent derivations; CP-D08 (lid = 6.00) is the only uncorroborated term.**

**Possible readings — none adopted.**
(a) CP-D08 is a **pre-weld stock** dimension, finished to 4.00 mm during §6 step 8 semi-finish. Vol 01 §6 step 4 says "Machine the FSW lid, 6.00 mm" (pre-weld), which supports this — but CP-D08 appears in the **Critical Dimensions** table with a finished tolerance of ±0.10, which does not.
(b) The lid seats in a rebate and CP-D07 or CP-D06 is measured differently than assumed.
(c) One of the four values is in error.

**CAD impact.** Blocks HOLD H1 in full: channel sketch, channel pocket, lid body, channel fillets, stub bores, and the Combine operation. This is the highest-effort feature group on the part (WBS 3.2.2, 4 h of a 16 h task) and it sits on the program critical path.

**Question for the Design Authority.** What are the controlling values for channel depth, channel-to-top-face wall, and finished lid thickness such that they sum to 20.000 mm? If CP-D08 is a pre-weld stock dimension, please state the **finished** lid thickness and re-classify CP-D08 accordingly.

---

### ECR-D-003 — Coolant stub interface undimensioned

**Specified:** Vol 01 CP-IF-10 — "2× ½ in. VCR male gland stubs, orbital-welded, radial at 255° (inlet) / 285° (outlet)." Vol 01 §6 step 10 — "Orbital-weld the 2× VCR gland stubs."

**Not specified anywhere in the baseline:**
- Stub bore diameter in the plate
- Bore depth / breakthrough point into the channel
- Bore centreline height above Datum A *(also dependent on ECR-D-002)*
- Weld preparation geometry (counterbore, land, chamfer)
- Tube OD/wall of the stub
- Transition geometry from a round bore to the 10 × 8 rectangular channel

No CP-Dxx entry exists for this feature; it does not appear in Vol 01 §9 tolerances.

**Geometric note — SUPERSEDED, see the banner at the head of this document.** ½ in. tube OD is 12.70 mm. The channel is **6.00 mm** tall after ECR-D-002, which made this defect worse, not better. A Ø12.70 radial bore therefore cannot be coaxial with an 8 mm channel without either a local boss, a stepped transition, or a change of channel section at the ports. The plate provides 35 mm of solid material radially between the channel envelope (r = 125) and the OD (r = 160) for the bore to traverse.

**CAD impact.** Blocks 2 features (HOLD H3) and Section B-B on drawing Sheet 3.

**Question for the Design Authority.** Please specify the stub bore diameter, depth, centreline height, weld preparation, and the bore-to-channel transition geometry.

---

### ECR-D-004 — Choke fastener counterbore undimensioned; specified bolt length exceeds the stack

**Part (a) — undimensioned counterbore.** Vol 01 CP-IF-3 specifies "16× M5 **counterbored** radially slotted clearance holes, 5.5 W × 7.0 L". The slot is dimensioned; **the counterbore is not** — no diameter, no depth, and no statement of whether it is itself slotted (which it must be if the bolt head travels radially with the Heater Plate). No CP-Dxx entry exists.

**Part (b) — bolt length incompatible with the stack.** Vol 00 §9 specifies **M5 × 30 SHCS** for this joint.

| Element | Value |
|---|---|
| Cooling Plate thickness (CP-D02) | 20.000 |
| Choke washer SEWCP-301 (HP-IF-1) | 1.500 |
| Heater Plate thickness (HP-D02) | 8.000 |
| **Total, plate bottom face to Heater Plate top face** | **29.500 mm** |
| Specified bolt length | **30 mm** |
| **Protrusion above the Heater Plate top face** | **0.500 mm** |

The Heater Plate top face is the **ESC bond face** (HP-IF-4). A bolt protruding 0.5 mm into a 0.400 mm bond line is a direct conflict, and any counterbore depth makes it worse (engagement = 8.5 mm + counterbore depth, into an 8.0 mm plate).

**CAD impact.** Blocks 16 counterbore features (HOLD H3) and drawing DET-3.

**Question for the Design Authority.** Please specify the counterbore diameter, depth, and whether it is radially slotted; and confirm the M5 fastener length for a 29.5 mm stack with the required thread engagement in the 8.000 mm Heater Plate.

---

## 12.2 Non-Blocking Documentation Defects — ECR-Q Class

Resolution is unambiguous in each case (a controlling reference exists and is corroborated). Logged for baseline correction; modelling proceeds on the controlling reference shown.

| ID | Defect | Stale Reference | Controlling Reference | Corroboration |
|---|---|---|---|---|
| ECR-Q-001 | Datum E bolt circle | Vol 00 §3.1: "Cooling Plate kinematic locator circle, **Ø288 BC**" | **Ø306 BC** | Vol 00 §3.2 table, Vol 01 CP-D09/D11, Vol 03 SR-IF-4, Vol 06 §3.1 |
| ECR-Q-002 | Base Plate datum bolt circle | Vol 00 §3.1: Datums B/C at "**Ø296 BC**" | **Ø302 BC** | Vol 00 FBA-3/FBA-4, Vol 01 CP-IF-2, Vol 03 SR-IF-3 |
| ECR-Q-003 | Clocking verification narrative contradicts its own table | Vol 00 §3.2 paragraph: "RTD ports at 105°/225°/345°… RF strap land at 75°" | **Table above it:** RTD 75/165/225; RF land 105° | Vol 01 CP-IF-8, CP-IF-9 |
| ECR-Q-004 | O-ring groove attributed to this part | Vol 01 §6 step 9 ("…RF land, **O-ring groove**, tapped holes"); Vol 01 §9 ("Profile · O-ring groove · 0.050") | **Groove is in the 316L port flange, not this plate** | Vol 01 CP-IF-5 (explicit), Vol 07 VP-D06/07/08, Vol 07 §12 |
| ECR-Q-005 | RF land torque | Vol 01 FMEA #6: "**8 N·m** preload" | **6.0 N·m** | Vol 00 §9 (with stated nut-factor rationale), Vol 08 RF-IF-1 |
| ECR-Q-006 | RF bracket mounting holes not carried into Vol 01 | Vol 08 RF-IF-3: "2× M6 × 16 at Ø274 BC **±40 mm circumferential**" | Absent from Vol 01 CP-IF-8, §5, §3.1 keep-out | **Not modelled.** Package will not invent an interface. Positions would resolve to 88.3°/121.7° at r = 137, outside the declared RF land keep-out envelope (93°–117°) |
| ECR-Q-007 | Choke pad Ø equals washer OD exactly | CP-D17 pad Ø22.0; SEWCP-301 washer OD Ø22.0; fastener position ⌖ Ø0.200 | Modelled as specified, Ø22.0 | For information: the washer may overhang the lapped pad by up to 0.2 mm at maximum fastener positional error |
| ECR-Q-008 | Kinematic locators absent from the keep-out table | Vol 01 §3.1 lists 8 keep-out classes; locators are not among them | Moot in practice | Locators at r = 130 and r = 153 lie outside the channel envelope (r ≤ 125). No routing impact. |

## 12.3 Disposition Request

| ID | Class | Blocks | Requested Action | Priority |
|---|---|---|---|---|
| ECR-D-002 | Defect | HOLD H1 — highest-effort feature, critical path | Specify closing channel/wall/lid values | **1** |
| ECR-D-001 | Defect | HOLD H2 — Datums B/C, entire GD&T scheme | Select controlling geometry; correct Vol 01, 03, 06 together | **2** |
| ECR-D-004 | Defect | HOLD H3 — 16 counterbores; ESC bond-line conflict | Dimension counterbore; confirm bolt length | **3** |
| ECR-D-003 | Defect | HOLD H3 — 2 stub bores | Dimension the stub interface | **4** |
| ECR-Q-001…008 | Query | Nothing | Baseline correction at next revision | 5 |

---

# 13 Release Gate

## CURRENT STATE — all four defects dispositioned

**Superseded by session `S-2026-08-10-01`.** The four defects below were real, were correctly
refused, and are now **dispositioned, approved, applied to the frozen specification and
re-registered**. Four more (`ECR-D-007`, `-009`, `-010`, `-011`) were found while resolving
them and are dispositioned in the same package.

| Was blocking | Now |
|---|---|
| `ECR-D-001` | Disposition A — SEWCP-700 governs. `APR-016`→`-017`→`-018`, `spec/03` residual closed by `APR-024` |
| `ECR-D-002` | Disposition A — depth 8.00 → 6.00. `APR-019`; its **unapplied** half (§6 step 3, the machining instruction) completed under `APR-020` |
| `ECR-D-003` | Disposition A — Ø10.0 coaxial port, SEWCP-201 transition joint. `APR-020` |
| `ECR-D-004` | Disposition A — `CP-D26` slotted masked counterbore, `M5 × 25`. `APR-020`/`-021`/`-022` |

**HOLD H1, H2 and H3 are discharged.** The whole part may be modelled.

**The authority for this gate is not this document.** Run
`PYTHONPATH=src python -m aief_gate`, which computes `C1`–`C7` from repository bytes.
`C6` closes on `VER-015`.

**The section that follows is the record of the defects as raised, on 2026-08-07.** It is
retained because it is the evidence the disposition rests on. It does not describe the current
baseline, and where it disagrees with `spec/**`, `spec/**` governs.

---

## ENGINEERING ISSUE DETECTED — *as raised, 2026-08-07; historical*

**Four blocking defects exist in the frozen baseline. This package cannot be released as READY FOR CAD.**

| ID | Defect | Blocks |
|---|---|---|
| **ECR-D-001** | Alignment pin locator interface — Vol 01/Vol 03 specify a press-fit Ø6.000 H7 dowel bore; Vol 06 specifies a Ø12.0 H7 × 3.0 counterbore with an M4 retaining tap and explicitly prohibits press fitting. Protrusion is stated as both 5.0 mm and 2.50 mm, and 5.0 mm is geometrically impossible against the 3.00 mm mating slot. | 6 features; **Datums B and C**; the drawing's entire GD&T scheme |
| **ECR-D-002** | Channel cross-section does not close: CP-D07 (8.00) + CP-D06 (8.00) + CP-D08 (6.00) = 22.00 mm against CP-D02 = 20.000 mm. Discrepancy 2.00 mm. Three of the four values are independently corroborated. | Channel, lid, fillets, stubs, Combine — the highest-effort feature group, on the program critical path |
| **ECR-D-003** | Coolant stub interface is undimensioned in every volume: no bore diameter, depth, centreline height, weld preparation, or round-to-rectangular transition geometry. | 2 features; drawing Section B-B |
| **ECR-D-004** | Choke fastener counterbore is undimensioned. Separately, the specified M5 × 30 exceeds the 29.5 mm stack, placing the bolt 0.5 mm into the ESC bond line. | 16 features; drawing DET-3 |

**No assumption has been made to close any of these.** No dimension has been changed, no interface invented, no architecture modified.

**Authorised to proceed now:** operations 6.01–6.07, 6.13–6.26, 6.29–6.31, 6.37–6.43 — approximately **82% of the part**, comprising the envelope, all bottom-face hole patterns, choke slots, RF land, RTD ports and vents, vacuum port interface, lift pin bores and bushing seats, HV bores, and both masking zone definitions.

**Held pending disposition:** HOLD H1, H2, H3 — pre-positioned as suppressed timeline placeholders requiring no restructuring on release.

**Escalation:** four ECR-D raised against WBS 3.2 (critical path, 16 h). Per SEDEP-PMP-001 §0.1, an ECR-D stops the affected task and re-gates the phase. Program risk **R-02 (Cooling Plate critical-path slip) is now active**; recommend re-sequencing WBS 3.7, 3.8 and 3.10 forward per the float table in §3.3 while disposition proceeds.

---

**END OF PACKAGE SEWCP-200-CAD-001 REV X1**
