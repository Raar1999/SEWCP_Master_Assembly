# SEWCP-ENG-001 — Architecture & Interface Control Document

**Program:** Simplified Electrostatic Wafer Chuck Platform (SEWCP)
**Volume:** 00 of 09 — Architecture, Datums, Budgets, Interface Control
**Revision:** A (Specification Freeze Candidate)
**Date:** 2026-08-07
**Prepared by:** Lead Mechanical Design Engineer
**Status:** FOR SPECIFICATION FREEZE — CAD release authorized against this baseline

---

## 1. Scope and Purpose

This document set defines the complete engineering specification for all SEWCP components **except the Base Plate, which is frozen and shall not be redesigned.** The specification is written to a level of detail sufficient that CAD may be executed directly, without design iteration.

This volume (00) establishes the shared framework — coordinate system, datums, stack-up, thermal/RF/vacuum budgets, tolerance allocation, fastener schedule, master assembly sequence, and interface control. Volumes 01–09 specify each component against this framework.

**No CAD, no modeling steps, and no code are contained in this document set.** This is engineering documentation only.

### 1.1 Document Set

| Vol | Document | Part No. | Component |
|-----|----------|----------|-----------|
| 00 | SEWCP-ENG-001 | — | Architecture & Interface Control (this document) |
| — | *(frozen)* | SEWCP-100 | Base Plate — **FROZEN, NOT IN SCOPE** |
| 01 | SEWCP-ENG-002 | SEWCP-200 | Cooling Plate |
| 02 | SEWCP-ENG-003 | SEWCP-300 | Heater Plate |
| 03 | SEWCP-ENG-004 | SEWCP-400 | Chuck Support Ring |
| 04 | SEWCP-ENG-005 | SEWCP-500 | Electrostatic Chuck |
| 05 | SEWCP-ENG-006 | SEWCP-600 | Lift Pins (+601 Bushing, +602 Lift Yoke IF) |
| 06 | SEWCP-ENG-007 | SEWCP-700 | Alignment Pins |
| 07 | SEWCP-ENG-008 | SEWCP-800 | Vacuum Port Assembly |
| 08 | SEWCP-ENG-009 | SEWCP-900 | RF Feedthrough Bracket Assembly |
| 09 | SEWCP-ENG-010 | SEWCP-1000 | Temperature Sensor Bracket |

### 1.2 Platform Definition

SEWCP is a 300 mm wafer electrostatic chuck platform representative of the pedestal architecture used in capacitively-coupled plasma etch and PECVD tools. It is a **development and demonstration platform**, not a production process module: process heat loads, RF power, and throughput requirements are scaled down, while all architectural principles, interfaces, and failure modes are retained at production fidelity.

| Parameter | Value |
|---|---|
| Wafer size | 300 mm dia. × 775 µm, SEMI M1 |
| Chucking principle | Coulombic, bipolar DC |
| Clamping voltage | ±500 to ±2000 VDC (nominal ±1500 VDC) |
| Backside gas | Helium, 5–20 Torr |
| Wafer temperature range | 20 °C to 150 °C |
| Wafer temperature uniformity | ±2.0 °C across Ø300 (3σ), steady state |
| Process heat load (design point) | 300 W (0–500 W range) |
| Heater trim power | 0–2000 W, 2 zones |
| Coolant capacity | 3 kW |
| RF bias | 13.56 MHz, ≤1000 W, ≤1500 V peak |
| Chamber base pressure | 1×10⁻⁶ Torr |
| Assembly He leak rate | < 1×10⁻⁹ mbar·L/s |

---

## 2. Frozen Baseline Assumptions (FBA)

**The Base Plate (SEWCP-100) is frozen.** No Base Plate drawing or datum sheet exists in the project repository at the time of this freeze. The following interface parameters are therefore **declared assumptions**. They are the *only* Base Plate characteristics this specification depends on.

| ID | Assumption | Consequence if Incorrect |
|----|-----------|--------------------------|
| FBA-1 | Base Plate top face is flat within 0.05 mm TIR and is the assembly's primary datum (Datum A), at Z = 0.000. | Support Ring bottom face is lapped to match; no other part affected. |
| FBA-2 | Base Plate OD ≥ Ø340 mm, thickness ≥ 20 mm, material 6061-T6 or 304/316L. | Affects Support Ring bolt-circle only. |
| FBA-3 | Base Plate carries 8× Ø7.0 (minimum) clearance through-holes on a Ø302.00 mm bolt circle at 22.5° + n·45°. | Support Ring flange hole pattern changes; no other part affected. |
| FBA-4 | Base Plate carries 2× Ø8 H7 dowel holes at Ø302 BC, 0° and 180° (Datums B and C). | Datum transfer moves to the Support Ring bolt pattern; see §4.4. |
| FBA-5 | Base Plate carries a central clearance aperture ≥ Ø60 mm for utility pass-through (He/vacuum, HV, RF, lift actuator). | Utility routing re-clocked; Vacuum Port, RF Bracket and Lift Pin actuator interfaces are clearance-only and tolerate ±2 mm variation by design. |
| FBA-6 | Base Plate is electrically bonded to chamber ground, ≤ 2 mΩ DC. | RF return path re-defined; see §6. |
| FBA-7 | Base Plate is at 20–40 °C during operation (chamber-wall coupled, not actively controlled). | Parasitic heat leak recalculated; Support Ring wall thickness is the tuning variable. |
| FBA-8 | **The Base Plate is the vacuum boundary.** Everything above it (Support Ring, Cooling Plate, Heater Plate, ESC, lift pins, RF strap, sensor harness) is in chamber vacuum; everything below it is at atmosphere. | Determines Paschen analysis (Vol 08 §2.3), the grease-free sensor interface (Vol 09 §2.1), and which side of each utility needs a vacuum seal. If the boundary is elsewhere, re-run those three analyses only. |

### 2.1 Architectural Firewall — Design Rule DR-1

> **DR-1: The Chuck Support Ring (SEWCP-400) is the sole structural interface between the frozen Base Plate and the thermal stack. All Base Plate uncertainty is absorbed by this single part.**

Only five features touch the Base Plate:

1. **Chuck Support Ring** — structural, located, torqued. *(The adapter.)*
2. **Vacuum Port stub** — passes through the central aperture with radial clearance; no locating function.
3. **RF Feedthrough Bracket** — passes through the central aperture with radial clearance; grounded clamp is fastened to the Base Plate via a floating slotted foot.
4. **Lift Pin actuator interface** — passes through the central aperture with radial clearance; the actuator is chamber-mounted, not Base-Plate-located.
5. **Temperature sensor harness** — pass-through only, no mechanical constraint.

Items 2–5 are **clearance-only interfaces with ≥ 2 mm radial float in every direction.** Consequently, if any FBA proves incorrect, the corrective action is confined to re-machining the Support Ring — a single, low-cost, non-critical-path ceramic part — and the remaining eight components require no change.

The Support Ring additionally serves as the **stack-up shim** (§5.3) and the **electrical isolator** (§6). Concentrating adaptation, adjustment, and isolation into one deliberately-sacrificial part is the central architectural decision of SEWCP.

---

## 3. Coordinate System, Datums, and Clocking

### 3.1 Datum Reference Frame

| Datum | Definition | Establishes |
|---|---|---|
| **A** | Base Plate top mounting face | Primary plane, Z = 0.000, wafer-plane parallelism |
| **B** | Base Plate primary dowel, Ø8 H7 @ Ø296 BC, 0° | X–Y origin (translation) |
| **C** | Base Plate secondary (diamond) dowel @ Ø296 BC, 180° | Clocking (rotation about Z) |
| **D** | Chuck Support Ring top face (lapped at assembly) | Transferred plane for the thermal stack |
| **E** | Cooling Plate kinematic locator circle, Ø288 BC | Thermal-stack centering axis |
| **F** | ESC mesa plane | Wafer seating plane — the functional output datum |

Axis convention: **+Z** is up, away from the Base Plate, toward the wafer. **+X** is the 0° clocking reference, coincident with Datum B. Angles increase counter-clockwise viewed from +Z.

### 3.2 Feature Clocking Map

All angular positions are referenced to the 0° / +X axis (Datum B). This map is binding on every component; CAD shall not re-clock features.

| Feature | Bolt Circle / Radius | Angular Positions | Qty |
|---|---|---|---|
| He / vacuum central port | Ø0 (axis) | — | 1 |
| ESC HV electrode feed contacts | Ø60 BC | 0°, 180° | 2 |
| Thermal-choke fasteners (inner) | Ø90 BC | 45°, 135°, 225°, 315° | 4 |
| Lift pin bores | Ø200 BC | 30°, 150°, 270° | 3 |
| RF strap land (Cooling Plate) | Ø274 BC | 105° (60 circ. × 18 radial land) | 1 |
| Thermal-choke fasteners (outer) | Ø270 BC | 0° + n·30° | 12 |
| RTD blind ports (Cooling Plate) | r = 40 @ 75°; r = 100 @ 165°; r = 140 @ 225° | (re-clocked to clear the RF land at 105°) | 3 |
| Kinematic radial slots (Ring↔Cooling Plate) | Ø306 BC | 60°, 180°, 300° | 3 |
| Support Ring fasteners (two independent circuits, DR-9) | Ø302 BC | 22.5° + n·45° | 8 + 8 |
| Coolant inlet / outlet | Ø320 OD, radial | 255° (in), 285° (out) | 2 |

**Clocking clearance verification:** RTD ports at 105°/225°/345° avoid the outer choke fasteners (30° multiples). The RF strap land at 75° falls between choke fasteners at 60° and 90°. Coolant ports at 255°/285° fall between choke fasteners at 240°/270°/300°. Lift pins (r = 100) and inner choke fasteners (r = 45) are radially separated. **No conflicts.**

### 3.3 Wafer Handoff Clocking

Lift pins at 30°/150°/270° leave a 120° clear sector centered on **210°** for robot end-effector entry. The end-effector envelope (blade width ≤ 60 mm, thickness ≤ 4 mm) shall be verified clear of the Support Ring OD and all utilities in that sector.

---

## 4. Assembly Architecture

### 4.1 Stack-Up (schematic, not to scale)

```
                     Ø300 WAFER  (0.775 thk)
        ─────────────────────────────────────────────  Z = 56.695
        ═════════════════════════════════════════════  Z = 55.920  ← wafer backside / Datum F
         ▲ 0.020 mesa gap (He-filled)
    ┌───────────────────────────────────────────────┐
    │  SEWCP-500  ELECTROSTATIC CHUCK   Ø297 × 6.00 │  Al₂O₃ 99.6%, bipolar
    └───────────────────────────────────────────────┘  Z = 49.900
      ░░░░░░░░ elastomer bond 0.40 ░░░░░░░░░░░░░░░░░
    ┌───────────────────────────────────────────────┐
    │  SEWCP-300  HEATER PLATE          Ø300 × 8.00 │  6061-T6 + MI heater
    └───────────────────────────────────────────────┘  Z = 41.500
      ▫  THERMAL CHOKE: 16× Ti washers 1.50 thk     ▫  vacuum gap elsewhere
    ┌───────────────────────────────────────────────┐
    │  SEWCP-200  COOLING PLATE        Ø320 × 20.00 │  6061-T6, FSW-sealed channel
    └───────────────────────────────────────────────┘  Z = 20.000
    ┌──┐                                         ┌──┐
    │  │  SEWCP-400  CHUCK SUPPORT RING          │  │  Al₂O₃ 99.5%, flanged
    │  │  web Ø300/Ø294 (3.0 wall) × H 20.00     │  │  (lapped to fit at assembly)
    └──┘                                         └──┘  Z = 0.000  ← Datum A
    ═══════════════════════════════════════════════════
       SEWCP-100  BASE PLATE   ***FROZEN — NO CHANGE***
    ═══════════════════════════════════════════════════
```

### 4.2 Nominal Z Build

| # | Element | Nominal (mm) | Tol (±) | Cumulative Z (mm) |
|---|---|---|---|---|
| 0 | Datum A — Base Plate top face | — | — | 0.000 |
| 1 | Chuck Support Ring height | 20.000 | 0.020* | 20.000 |
| 2 | Cooling Plate thickness | 20.000 | 0.030 | 40.000 |
| 3 | Thermal choke washer | 1.500 | 0.010 | 41.500 |
| 4 | Heater Plate thickness | 8.000 | 0.020 | 49.500 |
| 5 | ESC bond line | 0.400 | 0.050 | 49.900 |
| 6 | ESC puck thickness | 6.000 | 0.020 | 55.900 |
| 7 | Mesa height | 0.020 | 0.003 | 55.920 |
| — | **Wafer seating plane (Datum F)** | **55.920** | **see §5.3** | **55.920** |
| 8 | Wafer thickness | 0.775 | 0.020 | 56.695 |

\* Support Ring is supplied at 20.30 nominal and **lapped to final height at assembly** — see §5.3.

### 4.3 Thermal Architecture

The stack implements a **cooled base / thermal choke / trim heater** topology:

- The **Cooling Plate** is the heat sink and sets the baseline temperature.
- The **Thermal Choke** (16 titanium standoff washers + vacuum gap) is a *deliberately introduced* thermal resistance, R_choke ≈ 0.10 K/W, which decouples the heater from the sink.
- The **Heater Plate** is the control actuator, pushing the ESC above coolant temperature.
- The **ESC** is the thermal load path to the wafer.

Governing relation:

> **T_wafer ≈ T_coolant + (Q_heater + Q_process) × R_total**, where **R_total = 0.122 K/W**

| Path element | R (K/W) | ΔT @ 300 W | Basis |
|---|---|---|---|
| Wafer → ESC He gap | 0.0118 | 3.5 K | h = 1200 W/m²·K @ 10 Torr He, A = 0.0707 m² |
| ESC ceramic, 6 mm | 0.00283 | 0.8 K | k = 30 W/m·K (Al₂O₃) |
| Elastomer bond, 0.40 mm | 0.00377 | 1.1 K | k = 1.5 W/m·K |
| Heater Plate, 8 mm | 0.00068 | 0.2 K | k = 167 W/m·K (6061) |
| **Thermal choke** | **0.100** | **30.0 K** | **Ti-6Al-4V washers + 2 contact interfaces** |
| Cooling Plate to channel, 8 mm | 0.00068 | 0.2 K | k = 167 W/m·K |
| Coolant convection | 0.00222 | 0.7 K | h ≈ 5000 W/m²·K, A_wetted = 0.09 m² |
| **Total** | **0.1220** | **36.6 K** | |

Operating envelope: coolant at 20 °C, total power 0–1300 W → wafer 20 °C to 179 °C, **clamped by control to 150 °C** (bond-line limit).

**Thermal time constant:** C_stack = (Heater Plate 1.53 kg × 896) + (ESC 1.62 kg × 880) ≈ 2,800 J/K. τ = R_choke × C = 0.10 × 2800 ≈ **280 s**. Maximum ramp at 2000 W ≈ **43 K/min**.

**Radiation across the choke gap:** with bright as-machined facing surfaces (ε ≤ 0.15), Q_rad ≤ 4 W at ΔT = 100 K — negligible, and the reason those two faces are **explicitly excluded from anodizing** (see §8).

### 4.4 Load Path and Constraint Scheme

| Interface | Constraint Scheme | Rationale |
|---|---|---|
| Base Plate ↔ Support Ring | 8× M6 from below, through the ceramic bottom flange, into the SEWCP-401 clamp ring; ceramic captured in compression | **Two-circuit bolting (DR-9):** no fastener bridges the insulating web |
| Support Ring ↔ Cooling Plate | **3× radial-slot kinematic locators @ 120°** | Thermally centered: plate grows radially about a fixed axis; center stability ≤ 20 µm despite Al/Al₂O₃ CTE mismatch |
| Cooling Plate ↔ Heater Plate | 16× M5 through **radially slotted** clearance holes, Belleville-preloaded; 3× radial-slot locators | Allows 0.4 mm radial growth differential at ΔT = 130 K without bowing or dowel shear |
| Heater Plate ↔ ESC | Elastomer bond, full-face, 0.40 mm | Compliant shear layer absorbs CTE mismatch; no fasteners penetrate the wafer-facing surface |

> **DR-2: No fastener, dowel, or joint shall penetrate the ESC top surface.** All thermal-stack fasteners are installed **from below**, through counterbored clearance holes in the Cooling Plate, into threaded holes in the Heater Plate. This is why the Cooling Plate coolant circuit must be routed around the fastener pattern (§ Volume 01).

---

## 5. Tolerance Allocation

### 5.1 Flatness and Parallelism Budget

Functional requirement: **wafer seating plane (Datum F) parallel to Datum A within 0.050 mm TIR**, and **flat within 0.010 mm TIR over Ø297**.

| Contributor | Allocation (µm TIR) |
|---|---|
| Support Ring top face parallelism to bottom (post-lap) | 10 |
| Cooling Plate top face flatness | 15 |
| Cooling Plate top-to-bottom parallelism | 15 |
| Thermal choke washer thickness variation (16 pcs, sorted) | 5 |
| Heater Plate flatness (both faces) | 15 |
| Bond-line thickness variation | 20 |
| ESC lapped mesa-plane flatness | 10 |
| **RSS total** | **≈ 35 µm** |

RSS = √(10² + 15² + 15² + 5² + 15² + 20² + 10²) = **34.6 µm** ✔ against the 50 µm requirement.
Worst-case sum = 90 µm ✘ — therefore **flatness is controlled by measurement and selective assembly, not by worst-case tolerancing.** The Support Ring lap operation (§5.3) is the correction mechanism.

### 5.2 Wafer Plane Height Stack

Target: **55.920 ± 0.150 mm** from Datum A.

- Worst-case sum of §4.2 tolerances = ±0.153 mm → **fails by 3 µm.**
- RSS = √(0.020² + 0.030² + 0.010² + 0.020² + 0.050² + 0.020² + 0.003²) = **±0.069 mm** → passes.

Because worst-case marginally fails, the stack **shall not** rely on statistical assembly alone.

### 5.3 Correction Mechanism — Support Ring Lap-to-Fit

> **DR-3: The Chuck Support Ring is manufactured 0.30 mm over-height (20.30 −0/+0.05) and lapped to final height during assembly, after the as-built thickness of the Cooling Plate, choke washers, Heater Plate, bond line, and ESC have been measured.**

Procedure:
1. Measure and record as-built values for stack elements 2–7 (§4.2).
2. Compute required Support Ring height: **H_ring = 55.920 − Σ(measured elements 2–7)**.
3. Lap the Support Ring bottom face to H_ring, tolerance **±0.015 mm**, parallelism **0.010 mm TIR**.
4. Re-verify with the assembled stack on a CMM.

Residual height error after correction: **±0.020 mm** — a 7× margin against the ±0.150 mm requirement. This also recovers the flatness worst-case shortfall in §5.1.

### 5.4 Concentricity Budget

Wafer center to chuck axis: **≤ 0.20 mm**.

| Contributor | Allocation (mm) |
|---|---|
| Base Plate dowel to Support Ring bushing | 0.040 |
| Support Ring to Cooling Plate kinematic locators (incl. thermal) | 0.050 |
| Cooling Plate to Heater Plate locators | 0.030 |
| ESC bond fixture centering | 0.060 |
| Robot placement repeatability (external) | 0.100 |
| **RSS** | **0.137** ✔ |

---

## 6. Electrical Architecture

### 6.1 Potential Map

| Element | Potential |
|---|---|
| Base Plate | **Chamber ground** (≤ 2 mΩ) |
| Chuck Support Ring | **Insulator** — the isolation barrier |
| Cooling Plate | **RF-hot** (13.56 MHz bias electrode), DC-floating |
| Heater Plate | RF-hot (bonded to Cooling Plate potential via choke fasteners); heater element sheath filtered to ground |
| ESC electrodes | **±1500 VDC**, isolated, RF-coupled |
| Wafer | Plasma-referenced |

**Configuration A (baseline): RF-hot chuck.** The Cooling Plate is the powered bias electrode; the Support Ring is the RF standoff.

**Configuration B (alternate): grounded chuck**, with RF applied to an upper electrode. In Configuration B the Support Ring becomes a purely thermal/structural component, all insulating bushings are replaced by plain steel bushings, and the RF Feedthrough Bracket is deleted. **No other component changes.** Configuration A is specified throughout; Configuration B is called out where it materially differs.

### 6.2 Support Ring as RF Standoff

Ring geometry: flanged thin-wall cylinder in Al₂O₃ 99.5% (ε_r = 9.8). Web Ø300.0 OD / Ø294.0 ID (3.0 mm wall, mean Ø297.0) × 14.0 mm tall; integral top and bottom flanges Ø318.0 / Ø286.0 × 3.0 mm. Total height 20.000 mm. **Full derivation in Volume 03 §2.1.**

| Term | Value |
|---|---|
| Web conduction area | 2.799×10⁻³ m² |
| **R_th (web + flanges + spreading)** | **0.195 K/W** |
| Parasitic leak at ΔT = 20 K | **103 W** — 3.4% of coolant capacity |
| C, dielectric web | 17.4 pF |
| **C, stray flange-to-flange across the vacuum gap** | **9.6 pF (36% of total)** |
| **C_total** | **27.0 pF** |
| **X_C at 13.56 MHz** | **435 Ω** shunt to ground |

> The stray flange capacitance is a real and easily-missed term. It is why flange OD is a dimensioned, flagged characteristic on a part with a four-order-of-magnitude structural margin — widening the flanges "for stiffness" costs RF isolation and buys nothing.

**Material trade (documented, not open) — evaluated at the selected geometry:**

| Material | k (W/m·K) | R_th (K/W) | ε_r | C (pF) | X_C (Ω) | Verdict |
|---|---|---|---|---|---|---|
| **Al₂O₃ 99.5%** | 30 | 0.195 | 9.8 | 27.0 | 435 | **Selected** — best RF/thermal/cost balance; mature supply chain |
| Y-TZP zirconia | 2.2 | 2.55 | 30 | 62 | 189 | 13× better thermal break, 2.3× worse RF shunt, ~3× cost |
| PEEK (virgin) | 0.25 | 22.4 | 3.2 | 15 | 783 | Best on both metrics; **rejected — creeps under sustained preload at 150 °C** |
| Fused silica | 1.4 | 4.0 | 3.8 | 17 | 691 | Good numbers; low fracture toughness in a structural role |
| Ti-6Al-4V | 6.7 | 0.87 | — | short | 0 | **Rejected** — conductive, defeats Configuration A |

### 6.3 Isolation and Creepage Requirements

| Requirement | Value |
|---|---|
| Clearance, RF conductor to ground (atmosphere side) | ≥ 12 mm |
| Clearance, RF conductor to ground (vacuum side, with DR-11 in force) | ≥ 8 mm |
| Creepage over insulator surfaces | ≥ 20 mm, with anti-tracking grooves |
| Insulation resistance, Cooling Plate to Base Plate | ≥ 1 GΩ @ 1000 VDC |
| Hipot, ESC electrode to chuck body | 3000 VDC, 60 s, ≤ 10 µA |
| Hipot, heater element to sheath | 1500 VAC, 60 s |

### 6.4 Paschen Compliance — Governing Design Rule

Low-pressure gas gaps are the dominant arcing hazard in this architecture. Helium minimum breakdown is ≈ **155 V at p·d ≈ 4 Torr·cm.**

| Location | p·d (Torr·cm) | Position vs. minimum | Assessment |
|---|---|---|---|
| Wafer/ESC mesa gap, 20 µm @ 10 Torr | 0.020 | Far left | **Safe** — V_bd ≫ 2 kV |
| Lift pin bore **with pin present** (0.10 mm annulus @ 10 Torr) | 0.10 | Far left | **Safe** |
| Lift pin bore **if pin withdrawn** (Ø5.2 open @ 10 Torr) | 5.2 | **At the minimum** | **HAZARD** |
| Choke vacuum gap, 1.5 mm @ 1×10⁻⁶ Torr | 1.5×10⁻⁷ | Far left | Safe |

> **DR-4: Lift pin shafts shall never withdraw from the ESC bore.** The pin shall fill the full 6 mm thickness of the ESC bore at **every** travel position, and extend **≥ 10 mm below the ESC underside** at full-up. The ceramic pin itself is the arc suppressor — it reduces the free gap from Ø5.2 mm to a 0.10 mm annulus, moving p·d from the Paschen minimum to a decade and a half below it.

> **DR-5: Backside helium shall be enabled only when the wafer is clamped AND the lift pins are confirmed full-down.** Interlocked in the control system.

### 6.5 RF Isolation of Services

Every utility entering the RF-hot Cooling Plate is an unintended RF path to ground and shall be broken:

| Service | Isolation Method |
|---|---|
| Coolant supply/return | PFA dielectric line break, ≥ 150 mm, both lines |
| Backside He / vacuum | Ceramic gas-line break + RF choke, in-line |
| Heater power (2 zones) | LC low-pass RF filter box at the feedthrough |
| RTD / thermocouple leads | Shielded twisted pair, single-point shield ground at controller, common-mode ferrite chokes |
| ESC HV supply | RF filter integral to the HV supply output |

---

## 7. Vacuum Architecture

| Requirement | Value |
|---|---|
| Total assembly He leak rate | < 1×10⁻⁹ mbar·L/s |
| Coolant circuit leak rate (proof 6 bar) | < 1×10⁻⁹ mbar·L/s |
| Backside He leak into chamber, wafer clamped @ 10 Torr | < 2.0 sccm |
| — of which, past 3× lift pins | < 0.5 sccm |
| Outgassing rate, all exposed materials | < 1×10⁻⁷ Torr·L/s·cm² @ 150 °C |
| Elastomers | FKM (Viton) baseline; FFKM (Kalrez) for > 150 °C or plasma-exposed |
| Trapped volumes | **Prohibited.** All blind fastener holes shall be vented (cross-drilled or vented screws). |

> **DR-6: No trapped volumes.** Every blind hole in a vacuum-exposed part shall be vented. Virtual leaks are the single most common cause of a chuck failing pump-down qualification.

---

## 8. Materials and Finishes Summary

| Part No. | Component | Material | Finish |
|---|---|---|---|
| SEWCP-200 | Cooling Plate | 6061-T6 Al | Type III hard anodize 50 µm, sealed, on exposed surfaces; **masked** on: ESC-side choke contact pads, RF strap land, coolant channel interior, sealing faces |
| SEWCP-300 | Heater Plate | 6061-T6 Al (alt: AlSiC-9 MMC) | Bright as-machined on choke face (ε ≤ 0.15); Ra 0.4 µm on bond face |
| SEWCP-400 | Chuck Support Ring | Al₂O₃ 99.5%, ground | As-ground Ra ≤ 0.8 µm; lapped Ra ≤ 0.4 µm on datum faces |
| SEWCP-500 | Electrostatic Chuck | Al₂O₃ 99.6% co-fired, W electrodes | Lapped Ra 0.4 µm mesa tops; Ra 0.8 µm field |
| SEWCP-600 | Lift Pin | Al₂O₃ 99.8% | Ra 0.2 µm on crown and shaft |
| SEWCP-601 | Lift Pin Bushing | Vespel SP-1 (alt: Al₂O₃) | Ra 0.8 µm bore |
| SEWCP-700 | Alignment Pins | 316L (metal/metal); Al₂O₃ (ceramic IF) | Ra 0.4 µm |
| SEWCP-800 | Vacuum Port | 316L SS | Electropolished Ra ≤ 0.4 µm internal |
| SEWCP-900 | RF Bracket — conductor | OFHC Cu, **silver plated 8–13 µm, NO nickel underplate** | Ag bright |
| SEWCP-904 | RF Bracket — deposition shroud | Al₂O₃ 99.5% (**no PEEK** — 15× the loss tangent, heats in the RF field) | As-ground, anti-tracking grooves |
| SEWCP-900 | RF Bracket — clamp | 6061-T6 Al | Alodine 1200 chromate conversion (conductive) |
| SEWCP-1000 | Temp Sensor Bracket | 6061-T6 Al | Alodine 1200 |
| — | Thermal choke washers | Ti-6Al-4V Grade 5 | As-machined, deburred |
| — | Fasteners | A4-70 / 316 SS | **MoS₂ or silver dry-film anti-galling — mandatory** |

> **DR-7: No nickel underplate on any RF conductor.** Nickel is ferromagnetic (µ_r ≈ 100–600); skin depth at 13.56 MHz falls to ≈ 3.6 µm with 4× the resistivity of copper, creating a lossy, heating layer exactly where current concentrates. Silver plates directly onto copper.

> **DR-8: All stainless fasteners in vacuum shall carry anti-galling dry film.** Austenitic stainless galls readily; a galled fastener in a chuck is a chamber-open event.

---

## 9. Fastener and Torque Schedule

| Joint | Size | Qty | Grade | Torque | Washer | Notes |
|---|---|---|---|---|---|---|
| **Lower circuit:** Base Plate ↔ Support Ring bottom flange ↔ SEWCP-401 clamp ring | M6 × 40 SHCS | 8 | A4-70 | **6.0 N·m** | Ø16 flat + Belleville stack | At **ground** potential. 3 passes, star pattern, 30/70/100% |
| **Upper circuit:** Support Ring top flange ↔ Cooling Plate | M6 × 16 SHCS | 8 | A4-70 | **6.0 N·m** | Ø16 flat + Belleville stack | At **RF** potential. Never bridges the web (DR-9) |
| Cooling Plate ↔ Heater Plate (outer choke) | M5 × 30 SHCS | 12 | A4-70 | **3.5 N·m** | Ti washer + Belleville | Slotted clearance holes in Heater Plate |
| Cooling Plate ↔ Heater Plate (inner choke) | M5 × 30 SHCS | 4 | A4-70 | **3.5 N·m** | Ti washer + Belleville | Ø90 BC |
| Vacuum Port flange | M4 × 16 SHCS | 4 | A4-70 | **1.8 N·m** | Flat | Even, opposing sequence |
| RF strap to Cooling Plate land | M6 × 16 SHCS | 2 | A4-70, **silver-plated** | **6.0 N·m** | Silver-plated flat + Belleville | High preload (≈6.7 kN, 74% of yield). Torque is *reduced* vs. dry A4-70 because silver plating lowers the nut factor to K ≈ 0.15 — applying 8.0 N·m would yield the bolt |
| RF bracket clamp to Base Plate | M6 × 20 SHCS | 2 | A4-70 | 6.0 N·m | Flat | Slotted foot, floating |
| Temp sensor bracket | M4 × 12 SHCS | 4 | A4-70 | 1.8 N·m | Flat | — |

**Ceramic joint rule:** ceramic is loaded in **compression only**. No threads are cut in any ceramic part. Ceramic parts are captured between metal members through clearance holes, with a Belleville stack to maintain preload through thermal cycling and to limit peak bolt load.

**Belleville selection (Support Ring joint):** stack shall provide 2.5–3.5 kN preload per bolt with ≥ 0.25 mm working deflection, sized so that differential thermal expansion across the joint (Al Cooling Plate vs. Al₂O₃ Ring, ΔT ≤ 130 K) changes preload by less than ±20%.

---

## 10. Master Assembly Sequence

| Step | Operation | Verification |
|---|---|---|
| **A. Sub-assemblies** | | |
| A1 | Cooling Plate: machine channel, FSW-seal lid, orbital-weld VCR stubs | Proof 6 bar / 30 min; He leak < 1×10⁻⁹ mbar·L/s; flow ΔP at 4 L/min |
| A2 | Cooling Plate: install lift pin bushings, kinematic dowels, mask and hard-anodize | Bushing bore Ø5.05 H7; anodize mask verification |
| A3 | Heater Plate: braze MI heater cable into spiral grooves, both zones | Zone resistance ±5%; hipot 1500 VAC; IR > 100 MΩ @ 500 VDC |
| A4 | Heater Plate: finish-machine bond face and choke face | Flatness 15 µm; bond face Ra 0.4 µm; choke face bright, ε ≤ 0.15 |
| A5 | **Bond ESC to Heater Plate** in fixture; vacuum-debulk; cure at 60 °C | Bond line 0.40 ± 0.05 mm; ultrasonic C-scan, voids < 2% area, none > Ø3 mm; ESC flatness 10 µm post-bond |
| A6 | Measure all as-built stack thicknesses per §5.3 step 1 | Record on the build traveller |
| **B. Support Ring correction** | | |
| B1 | Compute H_ring per §5.3 step 2 | Calculation recorded |
| B2 | Lap Support Ring bottom face to H_ring | Height ±0.015; parallelism 0.010 TIR |
| **C. Stack build** | | |
| C1 | Clean all parts: ultrasonic, DI rinse, IPA, vacuum bake 120 °C / 4 h | Particle count; no visible residue |
| C2 | **Inverted, off-tool:** mate Support Ring to the Cooling Plate bottom face, engaging 3 kinematic radial-slot locators; torque the 8× upper M6 × 16 to 6.0 N·m | Locators free to slide radially before and after torque; no bind |
| C3 | Seat SEWCP-401 clamp ring in the bottom-flange register; invert and lower the Cooling Plate + Ring assembly onto the Base Plate | Bolt holes aligned; Datum A clean |
| C4 | From beneath the Base Plate, install and torque the 8× lower M6 × 40 into the clamp ring, 3 passes, star pattern, to 6.0 N·m | Torque log; then IR test Cooling Plate → Base Plate ≥ 1 GΩ; verify creepage ≥ 20 mm, clearance ≥ 12 mm |
| C5 | Fit thermal choke washers (thickness-sorted set) to the Cooling Plate top face | Sorted set total variation ≤ 5 µm |
| C6 | Lower the Heater Plate + ESC sub-assembly, engaging its 3 kinematic locators | Radial slots free |
| C7 | Torque 16× M5 through Belleville stacks to 3.5 N·m, star pattern | Torque log; verify heater plate free to grow radially |
| **D. Utilities** | | |
| D1 | Install Vacuum Port assembly; route He transfer tube with sliding O-ring seals | He leak < 1×10⁻⁹ mbar·L/s; orifice Ø0.50 verified |
| D2 | Install lift pins, bushings, and lift yoke | Tip planarity ≤ 0.10 mm; travel 20.0 mm; full-down tip 0.05–0.15 mm **below** mesa plane; pin fills the ESC bore at every travel position and extends ≥ 10 mm below the ESC underside at full-up (DR-4) |
| D3 | Install ESC HV feed contacts through alumina-lined bores | Continuity to electrodes; hipot 3000 VDC, ≤ 10 µA |
| D4 | Install RF Feedthrough Bracket and silver-plated strap | Strap-to-plate contact resistance ≤ 0.5 mΩ; clearance ≥ 12 mm; creepage ≥ 20 mm |
| D5 | Install Temperature Sensor Bracket and probes with spring preload | Preload 5–10 N per probe; 4-wire resistance check; response < 5 s |
| **E. Acceptance** | | |
| E1 | Full-assembly acceptance test per §12 | ATP data package |

> **Critical sequencing note:** The ESC-to-Heater-Plate bond (A5) is a **point of no return.** It is performed off-tool, before any stack assembly, and is the highest-risk single operation in the build. Bond-line C-scan acceptance is mandatory before the sub-assembly is released to step C6.

---

## 11. FMEA Summary (Assembly Level)

Severity (S), Occurrence (O), Detection (D) on 1–10; RPN = S×O×D. Component-level FMEAs appear in Volumes 01–09.

| # | Failure Mode | Effect | S | O | D | RPN | Mitigation |
|---|---|---|---|---|---|---|---|
| 1 | ESC bond delamination at OD | Loss of thermal contact, wafer temp excursion, ESC crack | 9 | 5 | 4 | **180** | 0.40 mm compliant bond (55% shear strain vs. 88% at 0.25 mm); C-scan; 100-cycle proof; AlSiC alternate |
| 2 | Arc in lift pin bore | ESC dielectric puncture, chamber contamination | 9 | 4 | 5 | **180** | DR-4 (≥10 mm pin engagement), DR-5 (He interlock), 0.10 mm annulus |
| 3 | Wafer dechuck failure (residual charge) | Wafer breakage on lift | 8 | 5 | 3 | **120** | Bipolar electrodes, reverse-polarity dechuck pulse, ramped discharge, lift-force monitoring |
| 4 | Backside He leak (broken wafer) | Chamber pressure excursion, contamination | 8 | 3 | 3 | **72** | Ø0.50 mm orifice restrictor in Vacuum Port; He mass-flow interlock |
| 5 | RF joint contact resistance rise | I²R heating, thermal runaway, arc | 8 | 3 | 4 | **96** | Silver plating, 8 N·m preload, Belleville, no Ni underplate, contact resistance in ATP |
| 6 | Coolant leak into vacuum | Catastrophic chamber contamination | 10 | 2 | 3 | **60** | FSW/brazed channel (no elastomer in the pressure boundary), 6 bar proof, He leak test |
| 7 | Support Ring fracture | Stack collapse | 10 | 2 | 4 | **80** | Compression-only loading, no ceramic threads, Belleville-limited preload, clearance holes |
| 8 | RTD probe lift-off | False low reading → heater thermal runaway | 9 | 3 | 5 | **135** | Spring preload 5–10 N, independent over-temp thermostat trip at 175 °C |
| 9 | Fastener galling in vacuum | Non-serviceable joint, chamber-open event | 6 | 4 | 4 | **96** | DR-8 anti-galling dry film mandatory |
| 10 | Virtual leak from trapped volume | Fails pump-down qualification | 5 | 5 | 6 | **150** | DR-6 all blind holes vented |
| 11 | Thermal choke resistance out of tolerance | Wafer temperature setpoint unreachable | 6 | 5 | 3 | **90** | R_choke verified by test at qualification; washer count/thickness is the tuning variable |
| 12 | Heater plate bowing from over-constraint | Bond stress, flatness loss | 7 | 3 | 4 | **84** | Radially slotted clearance holes + Belleville + kinematic locators |

**Top three risks by RPN: ESC bond delamination, lift-pin bore arcing, and virtual leaks.** All three are addressed by explicit design rules rather than by process control.

---

## 12. Acceptance Test Plan (Assembly Level)

| # | Test | Requirement |
|---|---|---|
| T1 | Dimensional — wafer plane height from Datum A | 55.920 ± 0.150 mm |
| T2 | Dimensional — ESC surface flatness | ≤ 0.010 mm TIR over Ø297 |
| T3 | Dimensional — Datum F parallelism to Datum A | ≤ 0.050 mm TIR |
| T4 | Dimensional — chuck axis concentricity | ≤ 0.20 mm |
| T5 | Lift pin tip planarity and travel | ≤ 0.10 mm; 20.0 ± 0.2 mm |
| T6 | Coolant proof pressure | 6 bar, 30 min, no deformation |
| T7 | Coolant flow / pressure drop | 4 L/min at ΔP < 1.5 bar |
| T8 | Assembly He leak rate | < 1×10⁻⁹ mbar·L/s |
| T9 | Pump-down to 1×10⁻⁶ Torr | ≤ 60 min, no virtual leak signature |
| T10 | Insulation resistance, Cooling Plate → Base Plate | ≥ 1 GΩ at 1000 VDC |
| T11 | ESC hipot | 3000 VDC, 60 s, ≤ 10 µA |
| T12 | Heater hipot / IR | 1500 VAC, 60 s; > 100 MΩ at 500 VDC |
| T13 | Heater zone resistance | Within ±5% of nominal |
| T14 | RF strap contact resistance | ≤ 0.5 mΩ |
| T15 | Clamping force verification | ≥ 40 mbar net at ±1500 V, 10 Torr He |
| T16 | Backside He leak, bare Si wafer clamped | < 2.0 sccm at 10 Torr |
| T17 | Dechuck test, 100 cycles | 100% release, zero wafer-stick events |
| T18 | Thermal uniformity, instrumented wafer | ±2.0 °C across Ø300 at 80 °C setpoint |
| T19 | Thermal ramp rate | ≥ 40 K/min at 2000 W |
| T20 | Thermal cycle endurance | 100 cycles, 20 ↔ 150 °C; re-verify T2, T8, T16 |
| T21 | Particle test | ≤ 20 adders ≥ 0.10 µm per wafer pass |

---

## 12A. Consolidated Design Rules

These rules are binding on all CAD and all assembly work. Each is stated in full in the volume indicated.

| Rule | Statement | Defined in |
|---|---|---|
| **DR-1** | The Chuck Support Ring is the sole structural interface to the frozen Base Plate. All Base Plate uncertainty is absorbed by this one part; every other touchpoint has ≥ 2 mm radial clearance. | Vol 00 §2.1 |
| **DR-2** | No fastener, dowel, or joint shall penetrate the ESC top surface. All thermal-stack fasteners install from below. | Vol 00 §4.4 |
| **DR-3** | The Support Ring is manufactured 0.30 mm over-height and lapped to final height at assembly, from measured as-built stack data. | Vol 00 §5.3 |
| **DR-4** | Lift pins shall fill the full ESC bore at every travel position and extend ≥ 10 mm below the ESC underside at full-up. | Vol 00 §6.4 |
| **DR-5** | Backside helium shall be enabled only with the wafer clamped AND lift pins confirmed full-down. | Vol 00 §6.4 |
| **DR-6** | No trapped volumes. Every blind hole in a vacuum-exposed part shall be vented. | Vol 00 §7 |
| **DR-7** | No nickel underplate on any RF conductor. Silver plates directly onto copper. | Vol 00 §8 |
| **DR-8** | All stainless fasteners in vacuum shall carry anti-galling dry film. | Vol 00 §8 |
| **DR-9** | No fastener shall bridge the Support Ring's insulating web. Two independent bolt circuits, one at ground and one at RF potential. | Vol 03 §3.1 |
| **DR-10** | Helium flow > 20 sccm sustained with the clamp energised shall be treated as a broken wafer: abort, disable He, inhibit lift-pin motion. | Vol 07 §2.1 |
| **DR-11** | RF power shall be inhibited whenever chamber pressure lies between 10 Torr and 10 mTorr (the Paschen transition band). | Vol 08 §2.3 |
| **DR-12** | No solid insulator shall bridge between the RF conductor and any grounded surface. Isolation is by vacuum clearance; the shroud shields without spanning. | Vol 08 §2.4 |
| **DR-13** | Every temperature-sensor blind bore shall be cross-vented, and the vent shall not be blocked by the retainer. | Vol 09 §3 |

## 13. Open Items

| ID | Item | Owner | Required By |
|---|---|---|---|
| OI-1 | Confirm FBA-1 through FBA-7 against the actual frozen Base Plate drawing. **Only the Support Ring is affected by any discrepancy (DR-1).** | Mech Design | Before Support Ring release |
| OI-2 | Confirm Configuration A (RF-hot chuck) vs. Configuration B (grounded chuck) with the process owner. | Systems | Before RF Bracket release |
| OI-3 | Empirically tune R_choke (target 0.10 ± 0.03 K/W) — contact resistance is the uncertain term. Washer count/thickness is the adjustment variable; no other part is affected. | Thermal | Qualification build |
| OI-4 | Confirm lift-pin bolt circle Ø200 against the actual robot end-effector envelope. | Automation | Before ESC release |
| OI-5 | Select bond elastomer and confirm 100-cycle 20↔150 °C durability at 55% shear strain. | Materials | Before A5 |

---

## 14. Consolidated Interview Talking Points — Architecture Level

These are the assembly-level points. Component-specific points appear in Volumes 01–09.

1. **"I isolated all frozen-baseline risk into one part."** The Base Plate was frozen before its interface was documented. Rather than propagate that uncertainty through nine components, I made the Support Ring the sole structural interface and gave every other Base Plate touchpoint ≥ 2 mm of clearance float. If the assumptions are wrong, one ceramic ring gets re-machined and the other eight parts are untouched. That is a deliberate architectural firewall, not a lucky outcome.

2. **"The same part is the adapter, the isolator, and the shim."** The Support Ring adapts to the frozen baseline, provides the 832 Ω RF standoff, and — manufactured 0.30 mm over-height and lapped at assembly — absorbs the entire height stack-up. Worst-case tolerancing failed by 3 µm; lap-to-fit recovered a 7× margin. I'd rather add one assembly operation than tighten six part tolerances.

3. **"I designed a thermal resistance in on purpose."** A heater sandwiched directly onto a chilled plate cannot control anything — with a graphite interface the heater plate sits 0.7 K above the sink at 2 kW. The thermal choke (16 titanium standoffs plus a vacuum gap, R = 0.10 K/W) is what makes the heater an actuator instead of a parasitic load. The choke dominates the thermal chain by 10× — which is the point, because it means wafer temperature is set by heater power, not by interface variability.

4. **"Paschen's law drove a mechanical requirement."** Backside helium at 10 Torr in an open Ø5.2 mm lift-pin bore gives p·d ≈ 5.2 Torr·cm — sitting on the helium breakdown minimum of about 155 V, with 1500 V on the electrode. The fix is mechanical: the ceramic pin never leaves the bore, which collapses the gap to a 0.10 mm annulus and moves p·d three decades to the safe side. That's DR-4, and it's why lift pin length and travel are coupled specifications rather than independent ones.

5. **"I iterated the bond thickness from a shear-strain calculation."** Alumina-to-aluminum across 90 K from cure gives 0.219 mm of radial differential expansion at the ESC edge. At a 0.25 mm bond line that's 88% shear strain; at 0.40 mm it's 55%, at a cost of 1.1 K of additional ΔT — which the budget absorbs easily. Bond delamination at the outer diameter is the number one failure mode of heated electrostatic chucks, and it's won or lost in the bond-line thickness callout.

6. **"Every service into an RF-hot body is an RF leak."** Coolant, helium, heater power, and RTD leads all enter the powered Cooling Plate. Each one gets an explicit break — PFA line breaks, a ceramic gas break, an LC filter box, single-point-grounded shielded pairs. Engineers who forget this build a chuck that works on the bench and arcs in the chamber.

7. **"Constraint scheme before tolerance scheme."** Aluminum against alumina across 130 K moves 0.4 mm radially. Two rigid dowels would shear or crack the ceramic. Three radial-slot kinematic locators let the plate breathe about a fixed axis and hold center to 20 µm. Getting the constraint topology right made the tolerances achievable; no amount of tight tolerancing would have fixed an over-constrained joint.

8. **"Nothing penetrates the wafer-facing surface."** Every thermal-stack fastener is installed from below, into the Heater Plate, which is why the coolant circuit has to be routed around the fastener pattern. That routing constraint is a direct consequence of a wafer-quality decision, and it's the kind of coupling that has to be settled at specification freeze — not discovered in CAD.

---

**END OF VOLUME 00**

*Next: Volume 01 — SEWCP-200 Cooling Plate*
