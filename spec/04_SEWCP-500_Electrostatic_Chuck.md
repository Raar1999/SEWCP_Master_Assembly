# SEWCP-ENG-005 — Electrostatic Chuck (ESC)

**Part Number:** SEWCP-500 · **Volume:** 04 of 09 · **Revision:** A
**Parent:** SEWCP-ENG-001 Architecture & ICD · **Stack position:** 4 (top of stack, wafer-facing)
**Bonded sub-assembly:** SEWCP-350 = SEWCP-300 (Heater Plate) + SEWCP-500

---

## 1. Engineering Purpose

The Electrostatic Chuck is the functional heart of the platform. It performs four jobs that no other component can:

1. **Holds the wafer electrostatically.** Embedded electrodes under a thin dielectric generate a Coulombic attraction that clamps the wafer flat, with no mechanical clamps intruding on the process area and no moving parts above the wafer plane.
2. **Defines the wafer plane.** Its lapped mesa tops are Datum F — the functional output of the entire tolerance stack.
3. **Enables backside gas cooling.** By holding the wafer at a controlled 20 µm standoff and sealing the perimeter, it creates a helium-filled gap that carries heat from the wafer into the chuck at rates a vacuum gap never could.
4. **Couples RF to the plasma.** As a thin dielectric over the powered Cooling Plate, it is the series capacitor through which bias power reaches the wafer.

It is also the **consumable**. Dielectric wear, mesa erosion, and bond fatigue give it a finite life. It is designed to be replaced as a bonded sub-assembly with the Heater Plate, leaving the long-lead Cooling Plate in the chamber.

## 2. Functional Requirements

| ID | Requirement | Value | Verification |
|---|---|---|---|
| EC-01 | Chucking mechanism | Coulombic, bipolar | Design |
| EC-02 | Clamping voltage range | ±500 to ±2000 VDC | Functional |
| EC-03 | Nominal clamping voltage | ±1500 VDC | — |
| EC-04 | Clamping pressure at ±1500 V | **≥ 38 mbar** | Load-cell / pull test |
| EC-05 | Net hold-down at 10 Torr He, ±1500 V | ≥ 25 mbar (≥ 2.5:1 margin) | Derived |
| EC-06 | Backside He pressure range | 5 to 20 Torr | — |
| EC-07 | He leak with bare Si wafer clamped, 10 Torr | < 2.0 sccm | Flow measurement |
| EC-08 | — of which past the 3 lift pin bores | < 0.5 sccm | Sub-test |
| EC-09 | Wafer-to-chuck heat transfer coefficient at 10 Torr | ≥ 1200 W/m²·K | Calorimetric |
| EC-10 | Surface flatness (mesa plane) | ≤ 0.010 mm TIR over Ø297 | Interferometer / CMM |
| EC-11 | Dielectric hipot, electrode to chuck body | 3000 VDC, 60 s, ≤ 10 µA | Hipot |
| EC-12 | Volume resistivity | > 1×10¹⁴ Ω·cm at 20 °C | Sample coupon |
| EC-13 | Dechuck time to release | ≤ 2.0 s | Functional, 100 cycles |
| EC-14 | Dechuck success rate | 100%, zero wafer-stick events in 100 cycles | ATP T17 |
| EC-15 | Maximum operating temperature | 150 °C (bond-limited) | — |
| EC-16 | Particle adders | ≤ 20 per wafer pass, ≥ 0.10 µm | Particle counter |
| EC-17 | Puck thickness | 6.000 ± 0.020 mm | Micrometer |
| EC-18 | Mass | ≤ 1.7 kg | Scale |

### 2.1 Clamping Force Derivation

For a Coulombic chuck with mesas, the wafer sits at mesa height above the dielectric surface. The electrode-to-wafer path is therefore **dielectric in series with a gas gap**, and the effective electrical distance is:

> **d_eff = d_dielectric / ε_r + g_mesa = 0.300 / 9.8 + 0.020 = 0.0306 + 0.020 = 0.0506 mm**

Electrostatic pressure **P = ½ ε₀ (V / d_eff)²**:

| Voltage | Field (V/m) | Pressure (Pa) | Pressure (mbar) | vs. 10 Torr He (13.3 mbar) | vs. 20 Torr He (26.7 mbar) |
|---|---|---|---|---|---|
| ±500 V | 9.88×10⁶ | 432 | 4.3 | **0.3:1 — will not hold** | — |
| ±1000 V | 1.98×10⁷ | 1,729 | 17.3 | 1.3:1 — marginal | — |
| **±1500 V** | **2.96×10⁷** | **3,889** | **38.9** | **2.9:1 ✔** | 1.5:1 — marginal |
| ±1800 V | 3.56×10⁷ | 5,600 | 56.0 | 4.2:1 | **2.1:1 ✔** |
| ±2000 V | 3.95×10⁷ | 6,917 | 69.2 | 5.2:1 | 2.6:1 |

**Operating rules that fall out of this table:**
- **±1500 V is the nominal setting for 10 Torr He operation** (2.9:1 margin).
- **20 Torr He operation requires ≥ ±1800 V.** The control system shall enforce a voltage floor as a function of He setpoint.
- **±500 V cannot hold the wafer against any backside gas** and exists only as a soft pre-clamp / ramp step.

**Note how strongly the mesa gap dominates.** The 20 µm gas gap contributes 0.020 mm of the 0.0506 mm effective distance — 40% — while 0.300 mm of alumina contributes only 0.0306 mm because permittivity divides it by 9.8. **Mesa height is a first-order determinant of clamping force**, which is why it is toleranced to ±3 µm on a part where most features are toleranced in tens of microns. A 10 µm mesa-height error changes clamping pressure by roughly 30%.

### 2.2 Dielectric Margin

| Parameter | Value |
|---|---|
| Dielectric thickness over electrode | 0.300 mm |
| Al₂O₃ dielectric strength | ~15 kV/mm |
| Withstand capability | 4.5 kV |
| Applied at ±2000 V (worst case) | 2.0 kV → 6.67 kV/mm |
| **Margin** | **2.25×** |
| Hipot acceptance (EC-11) | 3.0 kV |

A 2.25× margin is deliberately modest. Increasing dielectric thickness would improve it but reduce clamping force quadratically — at 0.6 mm the effective distance rises to 0.081 mm and clamping pressure at ±1500 V falls from 38.9 to 15.2 mbar, which will not hold the wafer at 10 Torr. **Dielectric thickness is the direct trade between clamping force and breakdown margin**, and 0.300 mm is where that trade lands for this voltage range.

### 2.3 Backside Gas Physics — Why 20 µm

Helium mean free path at 10 Torr (1,333 Pa), 300 K, d_He = 2.18×10⁻¹⁰ m:

> λ = kT / (√2 · π · d² · P) = (1.38×10⁻²³ × 300) / (1.414 × π × (2.18×10⁻¹⁰)² × 1333) ≈ **14.7 µm**

With a 20 µm gap, **Knudsen number Kn = λ/g = 0.74** — squarely in the **transition/slip regime**, not continuum.

Consequences that drive the design:
- Heat transfer is **not** governed by bulk gas conduction. In this regime h scales roughly with pressure and is limited by thermal accommodation at the two surfaces, which is why h ≈ 1200 W/m²·K rather than the ~4,000 W/m²·K continuum conduction would predict for helium across 20 µm.
- **Helium is chosen because it has the highest thermal conductivity and smallest molecular diameter of the inert gases** — it gives the best heat transfer at the lowest pressure, and lower pressure means less clamping voltage needed.
- Making the gap smaller would raise h but demands tighter mesa tolerance and worsens particle sensitivity; making it larger drops h and raises the required clamping voltage. 20 µm is the standard industry compromise and is adopted here for the same reasons.

## 3. Mechanical Interfaces

| IF | Interface | Type | Detail |
|---|---|---|---|
| EC-IF-1 | To Heater Plate (SEWCP-300) | **Permanent elastomer bond** | Full-face, 0.400 ± 0.050 mm, over Ø297; edge fillet required |
| EC-IF-2 | To wafer | Non-contact electrostatic + mesa contact | Mesa field Ø290 + seal band Ø291–297; 20 µm standoff |
| EC-IF-3 | To backside He supply | Central port | Ø1.5 mm through the puck on axis, feeding the distribution network |
| EC-IF-4 | To HV supply | Metallized pads | 2× Ø12 W/Ni/Au pads on the underside at Ø60 BC, 0°/180°; spring-loaded contact pins from the Heater Plate |
| EC-IF-5 | To Lift Pins (SEWCP-600) | Guided through-bores | 3× Ø5.200 H8 through-bores at Ø200 BC, 30°/150°/270°; 0.3 × 45° chamfer both ends, **no counterbore** |
| EC-IF-6 | To secondary He seal | O-ring land | Flat, lapped annular land Ø8–14 on the underside, on axis, bearing the Heater Plate's FKM O-ring |

### 3.1 Wafer-Facing Surface Architecture

| Zone | Radial extent | Feature | Height above field |
|---|---|---|---|
| Central He inlet | Ø0–1.5 | Through-port | — (recessed) |
| **Mesa field** | Ø4 to Ø290 | Ø0.8 mm mesas, 6.0 mm hexagonal pitch | **+0.020 mm** |
| He distribution grooves | within the field | 1.0 mm W × 0.5 mm D, 12 radial + 1 annular at Ø150 | −0.500 mm |
| Lift pin bores | Ø200 BC, 3 places | Ø5.2 through, chamfered | — |
| Field (between mesas) | Ø4 to Ø290 | Lapped flat | 0 (reference) |
| **Seal band** | **Ø291 to Ø297** | Continuous annular land, 3.0 mm wide | **+0.020 mm** |
| Outer edge | Ø297 | 0.5 × 45° chamfer | — |

**Contact area budget:**

| Contributor | Area (mm²) | % of Ø297 face |
|---|---|---|
| Mesas: Ø0.8 at 6 mm hex pitch over Ø290 | 1,071 | 1.55% |
| Seal band: annulus Ø291–297 | 2,771 | 4.00% |
| **Total wafer backside contact** | **3,842** | **5.55%** |

The mesa field alone contacts **1.6%** of the wafer backside. That number is the entire reason mesas exist (§12).

### 3.2 Wafer Overhang

Wafer Ø300 on a Ø297 puck gives **1.5 mm of overhang per side**. This is deliberate:

- It guarantees the seal band (OD Ø297) is **always fully covered** by the wafer, even at the 0.20 mm worst-case placement error — a 7.5× margin. An uncovered seal band is an immediate, total loss of backside gas.
- It moves the wafer edge away from the dielectric edge, where field concentration and the triple point (ceramic / vacuum / conductor) would otherwise promote edge arcing.
- It provides the space a focus/edge ring would occupy in a production configuration.

## 4. Mating Components

| Mates To | Part No. | Interface | Nature |
|---|---|---|---|
| Heater Plate | SEWCP-300 | EC-IF-1, -4, -6 | **Permanently bonded** — never separated after cure |
| Wafer | — | EC-IF-2 | Electrostatically clamped, mesa-supported |
| Lift Pins | SEWCP-600 | EC-IF-5 | Guided through-bores; pins never fully withdraw (DR-4) |
| Vacuum Port (He path) | SEWCP-800 | EC-IF-3 | Receives He via the Heater Plate transfer tube |
| Cooling Plate | SEWCP-200 | Indirect | RF coupling through the dielectric; no mechanical contact |

## 5. Critical Dimensions

| Ref | Dimension | Nominal | Tolerance | Criticality |
|---|---|---|---|---|
| EC-D01 | Puck outside diameter | Ø297.0 | ±0.10 | High — seal band coverage |
| EC-D02 | **Puck thickness** | **6.000** | **±0.020** | **Critical — Z stack** |
| EC-D03 | **Dielectric thickness over electrode** | **0.300** | **±0.020** | **Critical — clamp force & breakdown** |
| EC-D04 | **Mesa height above field** | **0.020** | **±0.003** | **Critical — clamp force, h, Z stack** |
| EC-D05 | Mesa diameter | Ø0.80 | ±0.05 | Medium |
| EC-D06 | Mesa pitch (hexagonal) | 6.00 | ±0.10 | Medium — uniformity of support |
| EC-D07 | **Mesa plane flatness** | — | **0.010 TIR over Ø297** | **Critical — wafer plane** |
| EC-D08 | Seal band width | 3.00 | ±0.10 | High — leak rate |
| EC-D09 | Seal band height (= mesa height) | 0.020 | ±0.002 | **Critical — coplanar with mesas** |
| EC-D10 | Seal band outside diameter | Ø297.0 | ±0.10 | High |
| EC-D11 | Electrode outside diameter | Ø291.0 | ±0.20 | High — edge field control |
| EC-D12 | Electrode thickness (metallization) | 0.020 | ±0.005 | Low |
| EC-D13 | Bipolar pole gap | 3.00 | ±0.20 | High — inter-pole breakdown |
| EC-D14 | He distribution groove | 1.00 W × 0.50 D | ±0.05 | Medium |
| EC-D15 | Central He port | Ø1.50 | +0.10 / −0 | Medium |
| EC-D16 | Lift pin bore | Ø5.200 | H8 | **Critical — Paschen (DR-4)** |
| EC-D17 | Lift pin bore position | Ø200 BC | ⌖ Ø0.100 Ⓜ | High |
| EC-D18 | Lift pin bore perpendicularity | — | 0.030 over 6 mm | **Critical — pin bind** |
| EC-D19 | Lift pin bore chamfer, both ends | 0.3 × 45° | ±0.15 | **Critical — no counterbore (Paschen)** |
| EC-D20 | HV pad diameter | Ø12.0 | ±0.30 | Medium |
| EC-D21 | Underside bond-face flatness | — | 0.020 TIR | High — bond line uniformity |
| EC-D22 | Outer edge chamfer | 0.5 × 45° | ±0.2 | High — bond fillet, handling |

**Mass:** π/4 × 0.297² × 0.006 × 3,900 = **1.62 kg** ✔ meets EC-18.

> **EC-D04 is the tightest tolerance in the entire program (±3 µm) on a 297 mm part.** It is justified in §2.1: mesa height contributes 40% of the effective electrical gap, so a 10 µm error moves clamping pressure by ~30%. It also sits directly in the wafer-plane Z stack.

## 6. Manufacturing Method

**Co-fired multilayer alumina with buried tungsten electrodes.**

| Step | Operation | Notes |
|---|---|---|
| 1 | Tape-cast 99.6% Al₂O₃ green sheets | Multiple layers; thickness controlled for post-shrink dielectric target |
| 2 | Screen-print the two D-shaped tungsten electrodes onto the interface layer | 3.0 mm pole gap; W is one of the few metals that survives alumina sintering |
| 3 | Print and via the electrode take-outs down to the underside pad locations | Ø60 BC, 0°/180° |
| 4 | Laminate the stack; form the central He port and lift pin bores in the green state | Green machining is far cheaper than diamond grinding sintered alumina |
| 5 | **Co-fire at ~1600 °C in a reducing (H₂/N₂) atmosphere** | Reducing atmosphere is mandatory — tungsten oxidizes and is destroyed in air at this temperature |
| 6 | Optional HIP (hot isostatic press) | Closes residual porosity; raises dielectric strength and reduces the flaw population |
| 7 | Diamond grind OD, underside, and top face to near-final | ~20% linear shrinkage occurred at sintering; all precision comes from here |
| 8 | Verify dielectric thickness over the electrode ultrasonically or by capacitance | **EC-D03 is buried and cannot be measured directly after firing — this is a process-control characteristic** |
| 9 | Lap the top face flat | Establishes the reference plane for mesa formation |
| 10 | Grind the He distribution grooves | Form wheel |
| 11 | **Form the mesa field and seal band by micro-abrasive blasting through a photolithographic mask** | Field is removed 20 µm; mesas and seal band are masked and remain |
| 12 | **Final-lap the mesa tops and seal band together** | Guarantees EC-D09 coplanarity — they must be lapped in one operation, or the seal band will not seal at the same height the mesas support |
| 13 | Metallize the underside HV pads: W base, Ni barrier, Au flash | Solderable/contactable, oxidation-resistant |
| 14 | Chamfer all edges and both ends of every bore, 0.3 × 45° minimum | Ceramic edge-flaw control; **no counterbore at the lift pin bores** |
| 15 | Electrical qualification: hipot 3 kV / 60 s, IR, inter-pole isolation | Per EC-11 |
| 16 | Dimensional inspection: flatness interferometry, mesa height by profilometry (min. 25 sites) | Per §5 |
| 17 | Ultrasonic clean, DI rinse, vacuum bake 200 °C / 4 h | |
| 18 | Package in a dedicated fixture, wafer-side protected | Handling damage is the dominant scrap mode |

**Mesa formation alternatives:**

| Method | Verdict |
|---|---|
| **Micro-abrasive blast through a photomask (selected)** | Standard industry method; parallel process over the whole face; naturally produces the slightly rounded mesa edges that reduce backside particle generation |
| Diamond grinding the field away | Feasible but slow — 98.4% of the field must be removed by 20 µm; also leaves sharper mesa edges |
| Laser ablation | Excellent geometric control; heat-affected zone and recast risk in alumina |

**Construction alternatives:**

| Approach | Verdict |
|---|---|
| **Co-fired bulk alumina with buried W electrodes (selected)** | Highest dielectric integrity, fully dense, no bond line inside the dielectric, best life |
| Plasma-sprayed Al₂O₃ over an aluminium base with a sprayed electrode | Substantially cheaper and widely used in production tools; lower dielectric strength, higher porosity, shorter life, and the sprayed coating's resistivity is harder to control (drifts toward Johnsen–Rahbek behaviour) |
| Bonded alumina wafer over a printed electrode on the carrier | Simplest to prototype; the bond line sits inside the dielectric stack and becomes the breakdown-limiting element — **rejected** |

## 7. Material

**99.6% Al₂O₃ (alumina), co-fired, with tungsten electrode metallization.**

| Property | Value | Relevance |
|---|---|---|
| Volume resistivity | > 10¹⁴ Ω·cm at 20 °C | **Defines Coulombic operation (§12)** |
| Dielectric strength | ~15 kV/mm | Breakdown margin |
| Relative permittivity | 9.8 | Effective gap, RF coupling |
| Loss tangent at 13.56 MHz | ~0.0002 | Negligible RF heating |
| Thermal conductivity | 30 W/m·K | Heat path to the heater plate |
| CTE | 7.2 ppm/K | **Bond shear strain (§12)** |
| Flexural strength | 350 MPa | Handling, mesa integrity |
| Density | 3,900 kg/m³ | Mass |
| Plasma erosion resistance | Good (fluorine/chlorine chemistries) | Consumable life |

**Why 99.6% and not 96%:** lower-purity alumina contains more glassy grain-boundary phase, which lowers volume resistivity, raises loss tangent, and — critically — makes resistivity strongly temperature-dependent. A 96% chuck can drift from Coulombic toward Johnsen–Rahbek behaviour as it heats, changing clamping force and dechuck behaviour mid-process. 99.6% keeps the operating mechanism stable across 20–150 °C.

**Alternative dielectric — AlN (aluminium nitride):** k = 170 W/m·K (5.7× better), CTE 4.5 ppm/K. Used in high-power production chucks where thermal performance dominates. Not selected here because its lower CTE *worsens* the bond mismatch against an aluminium heater plate, its resistivity is more temperature-sensitive, and its cost is several times that of alumina — none of which is justified at SEWCP's 500 W process load.

## 8. Surface Finish

| Surface | Finish | Reason |
|---|---|---|
| **Mesa tops** | **Lapped Ra ≤ 0.4 µm**, coplanar with the seal band within 0.002 mm | These are the only points touching the wafer backside; roughness here becomes backside particles and scratches |
| **Seal band** | **Lapped Ra ≤ 0.4 µm**, coplanar with mesas | Seal quality is a direct function of finish — leak rate scales roughly with the cube of the effective gap |
| Field (between mesas) | Ra ≤ 0.8 µm as-blasted | Not contacted; a slightly rough field is acceptable and marginally increases gas accommodation |
| He distribution grooves | As-ground Ra ≤ 1.6 µm, deburred | Flow path only |
| Lift pin bores | Ra ≤ 0.8 µm, chamfered 0.3 × 45° both ends | Pin travel; chamfer prevents wafer-edge scratching and ceramic chipping |
| Underside bond face | **Ra 0.8–1.6 µm, lightly grit-blasted** | Deliberately *rougher* than a sealing face — mechanical keying improves elastomer adhesion |
| HV pads | Au flash over Ni over W | Low, stable contact resistance; no oxidation over life |
| Outer edge | 0.5 × 45° chamfer, Ra ≤ 1.6 µm | Bond fillet formation; handling damage control |
| All edges and bore mouths | Chamfered ≥ 0.3 × 45° | Ceramic edge-flaw control |

> **Note the deliberate inversion:** the wafer-facing mesa tops are lapped to Ra 0.4 µm, while the bond face on the opposite side is grit-blasted to Ra 0.8–1.6 µm. One surface must be smooth because it touches product; the other must be rough because it must be adhered to. Specifying a uniform fine finish on both faces would produce a weaker bond.

## 9. Tolerances

**GD&T scheme:**
- **Datum A** — the mesa plane (wafer seating plane, Datum F of the assembly), flatness 0.010.
- **Datum B** — puck OD, Ø297.
- **Datum C** — the lift pin bore at 30° (clocking).

| Control | Feature | Tolerance |
|---|---|---|
| Flatness | Mesa plane (A) | 0.010 over Ø297 |
| Profile | Seal band to mesa plane | 0.002 (coplanarity) |
| Flatness | Underside bond face | 0.020 |
| Parallelism | Bond face to A | 0.025 |
| Position | Lift pin bores | ⌖ Ø0.100 Ⓜ A B C |
| Perpendicularity | Lift pin bores to A | 0.030 |
| Position | Central He port | ⌖ Ø0.200 Ⓜ A B |
| Position | HV pads | ⌖ Ø0.500 Ⓜ A B |
| Position | Electrode pattern (process-controlled) | ⌖ Ø0.500 Ⓜ B |
| Thickness | 6.000 ±0.020 | 8 points |
| Mesa height | 0.020 ±0.003 | ≥ 25 sites by profilometry |
| Dielectric over electrode | 0.300 ±0.020 | Process control + capacitance verification |
| Runout | OD to A | 0.20 |

**On buried features:** EC-D03 (dielectric thickness over the electrode) is the single most important electrical dimension on the part and **cannot be inspected directly after firing.** It is controlled by green-sheet thickness and lamination process control, and verified indirectly by capacitance measurement against a calibrated standard. This is normal for co-fired ceramics, and it means the vendor's process qualification — not incoming inspection — is the real control. Specify first-article destructive sectioning and per-lot capacitance verification accordingly.

## 10. Assembly Sequence

**The ESC is bonded to the Heater Plate off-tool, before any stack assembly. This is the highest-risk single operation in the build and is irreversible.**

**Bonding (SEWCP-ENG-001 §10 step A5):**

1. Verify incoming ESC: hipot, flatness, mesa height map, visual inspection for chips at every edge and bore.
2. Prepare the Heater Plate bond face: fine alumina grit blast (25 µm), solvent clean, dry.
3. Prepare the ESC bond face: verify grit-blast texture Ra 0.8–1.6 µm, solvent clean, dry.
4. Apply primer to both faces per the elastomer supplier's specification; observe the flash-off time.
5. Load both parts into the bonding fixture. The fixture shall control **bond-line thickness to 0.400 ± 0.050 mm** by hard stops, and **concentricity to 0.060 mm** (its allocation in the §5.4 concentricity budget).
6. Dispense the elastomer in a pattern that sweeps voids outward from the centre. Mask the central He port and the O-ring land.
7. **Vacuum-debulk** to remove entrained air.
8. Close the fixture to the hard stops; verify a continuous edge fillet has formed around the full Ø297 circumference.
9. Cure at **60 °C** per the supplier's schedule. *(Cure temperature is a design parameter — see §12. It sets the zero-stress datum for the bond.)*
10. **Ultrasonic C-scan the bond: voids < 2% of total area, none larger than Ø3 mm, no void within 10 mm of the outer edge.** Reject on failure — rework is not possible.
11. Re-verify ESC surface flatness post-bond: ≤ 0.010 mm TIR. Bonding can distort the puck.
12. Verify He continuity from the Heater Plate transfer tube through to the mesa field, and leak-check the secondary O-ring land.
13. Verify HV contact continuity to both electrodes and re-hipot at 3 kV.
14. The assembly is now **SEWCP-350** and is handled only by its edges, in a dedicated fixture.

**Installation:** per Volume 02 §10 steps 11–16.

**Wafer operation sequence (functional, not build):**

| Step | Action | Interlock |
|---|---|---|
| 1 | Lift pins raise; robot places wafer | He OFF (DR-5) |
| 2 | Lift pins lower to full-down; wafer settles on mesas | Verify pins full-down |
| 3 | Ramp clamp voltage to ±1500 V | — |
| 4 | Confirm clamp (leakage current signature) | — |
| 5 | Enable backside He to setpoint | **Requires clamp ON + pins full-down (DR-5)** |
| 6 | Verify He flow < 2 sccm | **He flow > threshold ⇒ broken wafer ⇒ abort (Volume 07)** |
| 7 | Process | Enforce V ≥ 1800 V if He > 10 Torr |
| 8 | He off; pump the backside volume to chamber pressure | — |
| 9 | **Dechuck:** ramp voltage to zero, then apply a reverse-polarity pulse | — |
| 10 | Dwell 2 s; raise lift pins with force monitoring | **Excess lift force ⇒ wafer stuck ⇒ abort before breakage** |

## 11. Failure Modes

| # | Failure Mode | Cause | Effect | S | O | D | RPN | Mitigation |
|---|---|---|---|---|---|---|---|---|
| 1 | **Bond delamination at the outer edge** | CTE mismatch shear cycling; void at the edge; over-temperature | Loss of thermal contact, local hot spot, wafer temperature excursion, eventual ESC cracking | 9 | 5 | 4 | **180** | 0.40 mm bond (55% strain, not 88%); C-scan with a no-void-within-10-mm-of-edge rule; edge fillet; 100-cycle proof; AlSiC heater plate alternate |
| 2 | **Dielectric breakdown** | Firing flaw, HIP skipped, over-voltage, thinning from wear | Puck destroyed; possible HV supply damage and chamber contamination | 10 | 2 | 3 | **60** | 2.25× design margin, 3 kV hipot at manufacture and after bonding, HIP, voltage limit in the controller |
| 3 | **Wafer stick on dechuck** | Residual charge in the dielectric; JR-mode leakage at elevated temperature | **Wafer breakage on lift** | 8 | 5 | 3 | **120** | Bipolar electrodes; ramped discharge + reverse-polarity pulse; 2 s dwell; lift-force monitoring aborts before breakage |
| 4 | **Arc in a lift pin bore** | Paschen minimum at open-bore p·d; counterbore adding free volume | Dielectric puncture; contamination | 9 | 4 | 5 | **180** | DR-4 (≥10 mm pin engagement), DR-5 (He interlock), **no counterbore**, 0.10 mm annulus, chamfer only |
| 5 | Seal band leak | Mesa/seal-band non-coplanarity; wafer bow; particle on the band; band wear | He leak > 2 sccm; loss of wafer cooling; chamber pressure disturbance | 7 | 4 | 3 | **84** | Mesas and seal band lapped in one operation (0.002 coplanarity); leak test in ATP; 1.5 mm wafer overhang |
| 6 | Mesa wear / erosion | Wafer sliding, plasma erosion, thousands of clamp cycles | Mesa height drops → clamping force rises, gap h changes → temperature drift | 6 | 6 | 5 | **180** | Consumable-life tracking; periodic mesa height mapping; alumina's plasma resistance; replace as a sub-assembly |
| 7 | Backside particle generation | Rough mesa tops, chipped bore edges, mesa fracture | Wafer backside defects; downstream lithography focus errors | 8 | 4 | 5 | **160** | Ra ≤ 0.4 µm lapped mesas, 1.6% contact area, blast-formed rounded mesa edges, all bores chamfered |
| 8 | Insufficient clamping at high He | Voltage floor not enforced; mesa height out of tolerance | Wafer lifts or slips; process loss; possible breakage | 8 | 3 | 3 | **72** | Voltage-vs-He-setpoint interlock; ±3 µm mesa tolerance; clamp verification by leakage signature |
| 9 | Chip / crack from handling | Dropped part, bare bench contact, edge impact | Scrap of the most expensive part in the stack | 8 | 4 | 2 | **64** | Dedicated fixtures, chamfers everywhere, edge-only handling, 100% incoming inspection |
| 10 | Dielectric thickness out of tolerance | Green-sheet or lamination process drift | Clamping force error of ±15%; reduced breakdown margin | 7 | 3 | 7 | **147** | **Buried dimension — vendor process qualification, first-article sectioning, per-lot capacitance verification** |
| 11 | Electrode-to-electrode breakdown across the pole gap | Pole gap too small; contamination in the green lamination | Loss of bipolar function | 8 | 2 | 4 | **64** | 3.0 mm gap buried under 0.3 mm dielectric; inter-pole isolation test |
| 12 | Drift toward Johnsen–Rahbek behaviour | Low-purity alumina; resistivity falling with temperature | Clamping force and dechuck behaviour change with temperature | 6 | 3 | 6 | **108** | 99.6% purity specified; resistivity verified on a sample coupon at temperature |

**Four failure modes tie at RPN 180: bond delamination, lift-pin arcing, mesa wear, and — through detection difficulty — dielectric thickness variation.** The first two are addressed by explicit design rules. The third is managed as consumable life. The fourth is a supply-chain control problem, not a design problem, and is called out as such.

## 12. Design Rationale

**Why Coulombic and not Johnsen–Rahbek.** JR chucks use a semi-conducting dielectric (10¹⁰–10¹³ Ω·cm) so charge migrates to the surface, collapsing the effective gap and producing far more force per volt — attractive at first glance. The cost is that JR clamping force depends strongly on the dielectric's resistivity, which is strongly temperature-dependent, and residual charge takes much longer to bleed off, making dechuck slow and unreliable. For a platform operating from 20 to 150 °C, a Coulombic chuck with >10¹⁴ Ω·cm gives **predictable, temperature-independent force and clean, fast release** — the right trade when the wafer must come off reliably every cycle.

**Why bipolar and not monopolar.** A monopolar chuck completes its circuit through the plasma, so it cannot clamp before plasma ignition or during transfer, and it dumps clamping current through the wafer. A bipolar chuck's two electrodes form a closed circuit through the wafer itself: it clamps **with no plasma present**, holds during pump-down and transfer, and leaves a much smaller residual charge because the two poles can be actively discharged against each other. Bipolar also halves the peak voltage to ground for the same inter-electrode field.

**Why mesas instead of a flat surface.** Three independent reasons, any one of which would justify them:
- **Particles.** Contact area drops from 100% to 1.6%. Backside particles are transferred by contact, and they cause lithography focus errors downstream. A 60× reduction in contact area is a direct 60× reduction in the transfer opportunity.
- **Controlled gap.** Mesas set a deterministic 20 µm standoff for the helium film. Without them, the gap would be whatever the wafer bow and surface roughness happened to produce — unrepeatable wafer to wafer.
- **Contamination tolerance.** A particle on a flat chuck tilts the wafer and ruins flatness. A particle in the 98.4% of the field that is recessed 20 µm does nothing at all.

**Why the seal band and mesas must be lapped in a single operation.** The mesas set the wafer height; the seal band must touch the wafer at exactly that height to seal. If they are formed or lapped separately, a 5 µm mismatch either lifts the seal band off the wafer — total loss of backside gas — or makes it a high spot that tilts the wafer off the mesa plane. The 0.002 mm coplanarity callout is a *process* requirement disguised as a dimension, and the manufacturing sequence enforces it explicitly.

**Why 0.300 mm of dielectric.** It is the balance point between clamping force and breakdown margin, and the relationship is strongly non-linear because permittivity divides the dielectric contribution by 9.8 while the mesa gap is undivided. At 0.300 mm the effective gap is 0.0506 mm, giving 38.9 mbar at ±1500 V with a 2.25× breakdown margin. Doubling the dielectric to 0.6 mm would take breakdown margin to 4.5× but drop clamping pressure to 15.2 mbar — below the 13.3 mbar of 10 Torr helium with essentially no margin. The chuck would be safer and useless.

**Why the bond line is 0.400 mm — an iteration, not a first guess.** Alumina (CTE 7.2) bonded to aluminium (23.6) develops radial differential expansion at the outer edge of:

> Δr = 148.5 mm × (23.6 − 7.2)×10⁻⁶ × ΔT

From the 60 °C cure to 150 °C operating, ΔT = 90 K, giving **Δr = 0.219 mm.** At the initially assumed 0.25 mm bond line that is **88% shear strain**; at 0.40 mm it is **55%**. The cost of the thicker bond is 1.1 K of additional ΔT at the 300 W design point — which the thermal budget absorbs without difficulty. Bond delamination at the outer diameter is the number one field failure of heated electrostatic chucks, and it is decided by this one callout.

**Why the cure temperature is a design parameter.** Curing at 60 °C rather than room temperature moves the bond's zero-stress state up into the operating range, roughly balancing the strain excursion between the cold and hot extremes instead of loading it all at high temperature. Cure temperature is specified on the drawing for this reason, not as a process convenience.

**Why lift pin bores have a chamfer and explicitly no counterbore.** The instinct is to counterbore the bore mouth so the pin head sits flush and the sharp edge is away from the wafer. But a Ø7 × 0.5 mm counterbore at 10 Torr helium gives p·d ≈ 7 Torr·cm — sitting on the helium Paschen minimum of ~155 V, with 1500 V on the electrode 0.3 mm away. A 0.3 × 45° chamfer achieves the same wafer-protection goal while keeping the pin-filled annulus at p·d ≈ 0.3 Torr·cm, more than a decade to the safe side.

## 13. Why Semiconductor Tools Use This Design

- **Electrostatic clamping replaced mechanical clamp rings** across the industry because clamp rings shadow the wafer edge, generate particles, prevent uniform backside gas, and cannot hold the wafer flat against thermal bow. An ESC holds the entire wafer area uniformly with nothing above the wafer plane — which is what makes full-area backside gas cooling possible at all.

- **Mesa (dimple) surfaces are universal on production ESCs.** Contact areas of 1–5% are standard. The driver is backside particle control: particles on the wafer backside cause chucking non-flatness and lithography focus errors at later steps, and reducing contact area is the most effective lever available.

- **Backside helium at 5–20 Torr is the industry-standard wafer cooling method.** Without it, a wafer in vacuum is thermally isolated — radiation alone cannot remove plasma heat, and the wafer would run hundreds of degrees above the chuck. Helium is chosen for its high thermal conductivity and small molecular diameter, which give the best heat transfer per unit pressure and therefore the lowest clamping voltage requirement.

- **Bipolar Coulombic chucks with alumina or AlN dielectrics dominate etch applications** where clean, fast, reliable dechuck matters more than maximum clamping force per volt. JR chucks appear where high force at low voltage is worth the temperature sensitivity.

- **Wafer sticking on dechuck is one of the best-known failure modes in the industry**, and the countermeasures specified here — bipolar electrodes, ramped discharge, reverse-polarity pulse, dwell, and lift-force monitoring — are standard practice on production tools. Force monitoring is the last line of defence: it aborts the lift before a stuck wafer is broken.

- **The ESC is a consumable, and tools are architected around that.** Dielectric wear, mesa erosion, and bond fatigue give it a finite life measured in wafer counts. Production pedestals are built so the ceramic and its carrier come out together, leaving the expensive, long-lead cooled base in place — exactly the SEWCP-350 sub-assembly strategy specified here.

## 14. Interview Talking Points

1. **"The tightest tolerance in the program is ±3 µm on mesa height, and I can show you why."** The wafer sits on mesas 20 µm above the dielectric, so the electrode-to-wafer path is 0.300 mm of alumina *in series with* a 20 µm gas gap. Permittivity divides the ceramic's contribution by 9.8, so it contributes only 0.0306 mm of the 0.0506 mm effective gap — the tiny air gap contributes 40%. A 10 µm mesa error moves clamping pressure about 30%. That's why a feature you can barely see carries the tightest tolerance on a 297 mm part.

2. **"Dielectric thickness is a direct trade between holding the wafer and not destroying the chuck."** At 0.300 mm I get 38.9 mbar at ±1500 V with a 2.25× breakdown margin. Double the dielectric and breakdown margin goes to 4.5× while clamping pressure falls to 15.2 mbar — below the 13.3 mbar of the helium I'm trying to hold the wafer against. The safer chuck doesn't work. That non-linearity is the whole design problem in one number.

3. **"I changed the bond line from 0.25 to 0.40 mm because of a shear-strain calculation."** Alumina on aluminium across 90 K from cure gives 0.219 mm of radial differential expansion at the edge — 88% shear strain at 0.25 mm, 55% at 0.40 mm. The cost is 1.1 K of extra ΔT, which the thermal budget absorbs. Edge delamination is the number one field failure of heated ESCs, and it's won or lost in that one callout. I also specify the cure temperature at 60 °C, because that sets the bond's zero-stress datum and balances the strain across the operating range instead of dumping it all at the hot end.

4. **"Mesas solve three different problems at once."** They cut wafer backside contact from 100% to 1.6%, which is a 60× reduction in particle transfer opportunity — and backside particles become lithography focus errors two hundred process steps later. They set a deterministic 20 µm helium gap instead of leaving it to wafer bow. And they make the chuck tolerant of contamination, because a particle sitting in the 98.4% of the surface that's recessed does nothing at all.

5. **"The seal band and the mesas have to be lapped in the same operation."** The mesas define wafer height; the seal band has to touch the wafer at exactly that height. Five microns of mismatch either lifts the seal off — total loss of backside cooling — or makes it a high spot that tilts the wafer off the mesa plane. So the drawing carries a 2 µm coplanarity callout and the process sheet forces them to be lapped together. It's a manufacturing requirement wearing a dimension's clothes.

6. **"I chose the weaker chucking mechanism on purpose."** Johnsen–Rahbek gives far more force per volt. But its force depends on dielectric resistivity, which is strongly temperature-dependent, and it holds residual charge much longer, so dechuck is slow and unreliable. For a chuck running 20 to 150 °C, I want force that doesn't change with temperature and a wafer that releases every single cycle. That's Coulombic with >10¹⁴ Ω·cm — which is also why I specified 99.6% purity rather than 96%, since the glassy phase in lower-purity alumina drags resistivity down as it heats and drifts you toward JR behaviour mid-process.

7. **"The lift pin bores have a chamfer and explicitly no counterbore, and that's a Paschen decision."** Every instinct says counterbore the bore mouth to protect the wafer edge. But a Ø7 × 0.5 mm counterbore at 10 Torr helium gives p·d ≈ 7 Torr·cm, right on the helium breakdown minimum of about 155 V, with 1500 V sitting 0.3 mm below. A 0.3 mm chamfer protects the wafer just as well and keeps the pin-filled annulus more than a decade to the safe side.

8. **"The most important electrical dimension on this part cannot be inspected."** Dielectric thickness over a buried co-fired electrode isn't measurable after firing. It's controlled by green-sheet thickness and lamination, verified indirectly by capacitance, and confirmed by first-article sectioning. So it appears in my FMEA with a detection rating of 7 — the highest on the part — and the real control is vendor process qualification, not incoming inspection. Recognising which characteristics you can't inspect changes how you buy the part.

9. **"Two independent surfaces on this part have opposite finish requirements."** The mesa tops are lapped to Ra 0.4 µm because they touch product. The bond face on the other side is grit-blasted to Ra 0.8–1.6 µm because it has to be adhered to and mechanical keying makes the bond stronger. Specifying a uniform fine finish across the part — the default instinct — would quietly produce a weaker bond on the interface that's already my highest-RPN failure mode.

---

**END OF VOLUME 04**

*Next: Volume 05 — SEWCP-600 Lift Pins*
