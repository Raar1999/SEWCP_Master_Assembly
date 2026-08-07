# SEWCP-ENG-004 — Chuck Support Ring

**Part Number:** SEWCP-400 · **Volume:** 03 of 09 · **Revision:** A
**Parent:** SEWCP-ENG-001 Architecture & ICD · **Stack position:** 1 (directly on the frozen Base Plate)
**Includes:** SEWCP-401 Lower Clamp Ring

---

## 1. Engineering Purpose

The Chuck Support Ring is the most architecturally loaded component in SEWCP. It performs **five** distinct jobs, and the design is a negotiated settlement between them:

1. **Electrical isolation.** It is the only thing separating the RF-hot Cooling Plate from the grounded Base Plate. It must stand off 1500 V peak at 13.56 MHz with a high shunt impedance.
2. **Thermal break.** It must prevent the uncontrolled Base Plate from becoming a parallel heat path that competes with the coolant loop for authority over chuck temperature.
3. **Structural support.** It carries the entire 7.5 kg thermal stack and everything mounted to it.
4. **Interface adapter (DR-1).** It is the sole structural interface to the frozen Base Plate, and absorbs all uncertainty in the Frozen Baseline Assumptions.
5. **Stack-up shim (DR-3).** It is manufactured over-height and lapped at assembly to set the wafer plane, correcting the accumulated tolerance of every part above it.

Jobs 1 and 2 want the ring thin and made of a poor conductor. Job 3 wants it thick. Jobs 4 and 5 want it cheap, quick to re-machine, and non-critical-path. The flanged thin-wall ceramic cylinder specified here satisfies all five.

## 2. Functional Requirements

| ID | Requirement | Value | Verification |
|---|---|---|---|
| SR-01 | Insulation resistance, Cooling Plate to Base Plate | ≥ 1 GΩ at 1000 VDC | Megohmmeter, installed |
| SR-02 | Shunt impedance to ground at 13.56 MHz | ≥ 400 Ω | Network analyzer / calculation |
| SR-03 | Creepage path, RF-hot to grounded hardware | ≥ 20 mm | Drawing verification |
| SR-04 | Clearance, RF-hot to grounded hardware | ≥ 12 mm | Drawing verification |
| SR-05 | Thermal resistance, Cooling Plate to Base Plate | **0.20 ± 0.03 K/W** | Calorimetric test |
| SR-06 | Parasitic heat leak at ΔT = 20 K | ≤ 110 W | Derived from SR-05 |
| SR-07 | Static load capacity | 7.5 kg stack + 5 g in all axes, SF ≥ 3 | Analysis |
| SR-08 | Height, as supplied | 20.300 −0 / +0.050 mm | Micrometer |
| SR-09 | Height, after assembly lap | Per DR-3 calculation, ±0.015 mm | CMM |
| SR-10 | Top-to-bottom face parallelism, after lap | ≤ 0.010 mm TIR | CMM |
| SR-11 | Bottom face flatness, after lap | ≤ 0.010 mm TIR | Optical flat / CMM |
| SR-12 | Kinematic slot radial travel | ≥ ±1.0 mm | Gauge |
| SR-13 | Maximum operating temperature | 200 °C | — |
| SR-14 | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA |
| SR-15 | Mass | ≤ 0.8 kg | Scale |

### 2.1 Thermal and Electrical Performance Derivation

**Geometry:** thin cylindrical web, Ø300.0 OD / Ø294.0 ID (3.0 mm wall, mean Ø297.0), 14.0 mm tall, with integral top and bottom flanges Ø318.0 OD / Ø286.0 ID × 3.0 mm thick. Total height 20.000 mm.

| Term | Calculation | Value |
|---|---|---|
| Web conduction area | π × 0.297 × 0.003 | 2.799×10⁻³ m² |
| Flange annulus area | π/4 × (0.318² − 0.286²) | 1.518×10⁻² m² |
| R, web (14 mm, k = 30 W/m·K) | 0.014 / (30 × 2.799×10⁻³) | 0.167 K/W |
| R, two flanges (3 mm each) | 2 × 0.003 / (30 × 1.518×10⁻²) | 0.013 K/W |
| R, spreading at web/flange junctions | Estimated | 0.015 K/W |
| **R_total** | — | **0.195 K/W** ✔ meets SR-05 |
| Parasitic leak at ΔT = 20 K | 20 / 0.195 | **103 W** ✔ meets SR-06 |
| C, dielectric web | ε₀ε_r A/L = 8.854×10⁻¹² × 9.8 × 2.799×10⁻³ / 0.014 | 17.4 pF |
| **C, stray flange-to-flange (vacuum gap)** | ε₀ × 1.518×10⁻² / 0.014 | **9.6 pF** |
| **C_total** | — | **27.0 pF** |
| **X_C at 13.56 MHz** | 1 / (2πfC) | **435 Ω** ✔ meets SR-02 |

> **Note the stray term.** The two mounting flanges form a parallel-plate capacitor across the 14 mm vacuum gap, contributing 9.6 pF — 36% of the total. It is invisible if you model only the ceramic web, and it is the reason the flanges are dimensioned no wider than the bolt circle requires. Widening the flanges to Ø330 for "extra safety margin" would add another 5 pF and cost 70 Ω of shunt impedance for no structural benefit.

### 2.2 Structural Margin (the ring is not strength-driven)

The two bolt circuits are **locally self-reacting**: bolt → Base Plate → ceramic bottom flange → clamp ring, and bolt → Cooling Plate → ceramic top flange. Neither preload circuit passes through the web. The web therefore carries only service loads.

| Load case | Stress in web | Alumina capability | Margin |
|---|---|---|---|
| Stack dead weight, 74 N compression | 0.026 MPa | 2,500 MPa (compressive) | ~96,000× |
| 5 g lateral, moment at web root | 0.079 MPa | 350 MPa (flexural) | ~4,400× |
| Bolt preload bearing on flange (3 kN, Ø16 washer) | 17.8 MPa | 2,500 MPa (compressive) | 140× |

**The ring is dimensioned by thermal, electrical, and manufacturing constraints — not by stress.** The 3.0 mm wall is set by the minimum thickness that can be reliably ground and handled in 99.5% alumina at Ø300, not by load. This is why it can be made so thin, and it is the single fact that makes requirements SR-02 and SR-05 achievable simultaneously.

## 3. Mechanical Interfaces

| IF | Interface | Type | Detail |
|---|---|---|---|
| SR-IF-1 | To Base Plate (SEWCP-100) | Clamped, compression | Bottom flange face on Datum A; 8× Ø7.0 clearance holes at Ø302 BC, 22.5°+n·45° |
| SR-IF-2 | To Lower Clamp Ring (SEWCP-401) | Clamped, compression | 0.50 mm deep × Ø318/Ø286 register counterbore in the bottom flange top face; clamp ring seats in it |
| SR-IF-3 | To Cooling Plate (SEWCP-200) — fastening | Bolted | 8× Ø7.0 clearance holes at Ø302 BC in the **top** flange, clocked coincident with SR-IF-1; M6 bolts pass upward into tapped holes in the Cooling Plate bottom face |
| SR-IF-4 | To Cooling Plate — location | **Kinematic** | 3× radial slots, 6.05 H8 W × 8.0 L (radial), at Ø306 BC on 60°/180°/300° in the top flange upper face, engaging Ø6 h6 dowels pressed into the Cooling Plate |
| SR-IF-5 | Central bore | Clearance | Ø286 minimum clear through the ring for all utility routing (He, HV, RF, lift actuator) |

### 3.1 Two-Circuit Bolting Scheme

> **DR-9: No fastener shall bridge the insulating web.** The lower bolt set is entirely below the web and sits at ground potential. The upper bolt set is entirely above the web and sits at RF potential. The only connection between them is the ceramic.

| Bolt set | Qty | Path | Potential | Torque |
|---|---|---|---|---|
| **Lower** | 8× M6 × 40 | From beneath the Base Plate, through the Base Plate, through the ceramic bottom flange, into tapped holes in SEWCP-401 | **Ground** | 6.0 N·m |
| **Upper** | 8× M6 × 16 | From beneath the ceramic top flange, upward into tapped holes in the Cooling Plate | **RF-hot** | 6.0 N·m |

**Creepage path** from the upper (RF) bolt heads to the lower (grounded) clamp ring: down the top flange face (16 mm radial), along the 14 mm web, and out along the bottom flange (16 mm radial) = **≥ 40 mm** ✔ against the 20 mm requirement (SR-03). **Clearance** across the open annular gap between the clamp ring and the Cooling Plate = 14 mm ✔ against 12 mm (SR-04).

This scheme eliminates the insulating shoulder bushings required by the superseded single-bolt concept (§12), removes eight ceramic parts from the bill of materials, and removes the exposed RF-live bolt heads beneath the Base Plate that would otherwise have needed protective caps and a grounded safety skirt.

## 4. Mating Components

| Mates To | Part No. | Interface | Nature |
|---|---|---|---|
| Base Plate | SEWCP-100 | SR-IF-1 | **Sole structural interface to the frozen part (DR-1)** |
| Lower Clamp Ring | SEWCP-401 | SR-IF-2 | Captures the bottom flange in compression |
| Cooling Plate | SEWCP-200 | SR-IF-3, SR-IF-4 | Carries it; centers it kinematically; isolates it electrically |
| Alignment Pins | SEWCP-700 | SR-IF-4 | Receives 3 dowels in radial slots |
| All utilities | SEWCP-800/900/1000, -600 | SR-IF-5 | Clearance pass-through only, ≥ 2 mm radial float each |

## 5. Critical Dimensions

### 5.1 SEWCP-400 Chuck Support Ring (Al₂O₃)

| Ref | Dimension | Nominal | Tolerance | Criticality |
|---|---|---|---|---|
| SR-D01 | **Overall height, as supplied** | **20.300** | **−0 / +0.050** | **Critical — lap stock (DR-3)** |
| SR-D02 | **Overall height, after assembly lap** | Per DR-3 | ±0.015 | **Critical — wafer plane** |
| SR-D03 | Bottom face flatness (post-lap) | — | 0.010 TIR | **Critical** |
| SR-D04 | Top-to-bottom parallelism (post-lap) | — | 0.010 TIR | **Critical** |
| SR-D05 | Web outside diameter | Ø300.0 | ±0.15 | Medium — RF/thermal |
| SR-D06 | Web inside diameter | Ø294.0 | ±0.15 | Medium — RF/thermal |
| SR-D07 | **Web wall thickness** | **3.00** | **±0.15** | **Critical — SR-02, SR-05** |
| SR-D08 | Web height | 14.00 | ±0.10 | High — SR-02, SR-05 |
| SR-D09 | Flange outside diameter | Ø318.0 | ±0.15 | High — stray capacitance |
| SR-D10 | Flange inside diameter | Ø286.0 | ±0.15 | Medium |
| SR-D11 | Flange thickness (each) | 3.00 | ±0.05 | High |
| SR-D12 | Web-to-flange fillet | R3.0 | +0.5 / −0 | **Critical — ceramic stress riser** |
| SR-D13 | Bolt clearance holes (16 total, 8 per flange) | Ø7.0 | +0.2 / −0 | Medium |
| SR-D14 | Bolt hole circle | Ø302.0 | ⌖ Ø0.30 | Medium |
| SR-D15 | Bolt hole edge chamfer, both sides | 0.3 × 45° | ±0.15 | **Critical — ceramic edge chipping** |
| SR-D16 | Clamp ring register counterbore | Ø318.5 / Ø285.5 × 0.50 deep | +0.10 / −0 | Medium |
| SR-D17 | Kinematic slot width | 6.05 | H8 | **Critical — centering** |
| SR-D18 | Kinematic slot length (radial) | 8.00 | +0.20 / −0 | **Critical — thermal float** |
| SR-D19 | Kinematic slot depth | 3.00 | ±0.10 | High |
| SR-D20 | Kinematic slot position | Ø306 BC | ⌖ Ø0.050 Ⓜ | **Critical** |
| SR-D21 | All external edges | 0.3 × 45° min | — | **Critical — handling** |

### 5.2 SEWCP-401 Lower Clamp Ring (316L)

| Ref | Dimension | Nominal | Tolerance |
|---|---|---|---|
| CR-D01 | Outside diameter | Ø318.0 | −0.10 / −0.25 (clears the register) |
| CR-D02 | Inside diameter | Ø286.0 | +0.25 / +0.10 |
| CR-D03 | Thickness | 6.00 | ±0.05 |
| CR-D04 | Tapped holes | M6 × 1.0, 8 off at Ø302 BC | ⌖ Ø0.20 |
| CR-D05 | Flatness, both faces | — | 0.020 TIR |
| CR-D06 | Bearing face finish | Ra ≤ 0.8 µm | — |

**Mass:** alumina ring ≈ 0.62 kg (ρ = 3,900 kg/m³); clamp ring ≈ 0.36 kg. Ring meets SR-15.

## 6. Manufacturing Method

**SEWCP-400: dry-pressed or isostatically pressed 99.5% alumina, sintered, then diamond ground.**

| Step | Operation | Notes |
|---|---|---|
| 1 | Isostatic press a near-net cylindrical blank, oversized ~20% for sintering shrinkage | Isostatic pressing gives more uniform density than dry pressing for a thin-wall part |
| 2 | Green machine the bore, OD, and flange profile | Far cheaper than grinding sintered alumina — remove ~90% of stock here |
| 3 | Sinter at 1,600 °C | ~20% linear shrinkage; distortion is expected and corrected by grinding |
| 4 | Diamond grind OD, ID, flange faces, and both end faces | Rigid fixture; light passes on the thin wall |
| 5 | Diamond core-drill / ultrasonic machine the 16 bolt clearance holes | **Drill from both faces, meeting mid-thickness**, to avoid exit-side chipping |
| 6 | Diamond grind the 3 kinematic slots | Form wheel; maintain slot-width tolerance H8 |
| 7 | Grind the clamp ring register counterbore | |
| 8 | Chamfer **every** edge and hole, 0.3 × 45° minimum | Ceramic fails from edge flaws — this is a functional operation, not cosmetic |
| 9 | Grind both end faces to 20.300 −0/+0.050 | Leave lap stock per DR-3 |
| 10 | Dye-penetrant / fluorescent inspection for cracks and chips | 100%, with particular attention to the web-to-flange fillets |
| 11 | Proof load test: 30 kN axial through the flanges, 60 s | Verifies no sintering flaw in the bolt-bearing regions; 1.25× the total assembled preload |
| 12 | Ultrasonic clean, DI rinse, vacuum bake 200 °C / 4 h | |
| 13 | Inspect and package in a dedicated foam-lined fixture | Handling damage is the dominant scrap mode |
| — | **Final lap to height performed at assembly, not at the vendor** | See §10 |

**SEWCP-401: conventional CNC turning and drilling from 316L bar or plate.** Deburr thoroughly, passivate, electropolish or bead-blast to Ra ≤ 0.8 µm, ultrasonic clean, vacuum bake.

**Manufacturing alternatives considered:**

| Approach | Verdict |
|---|---|
| **Green-machine + sinter + diamond grind (selected)** | Standard for technical ceramics; lowest cost route to a ground thin-wall part |
| Grind entirely from a sintered blank | 5–10× the grinding time and cost; no benefit |
| Injection-moulded ceramic | Only economic at high volume; wall-thickness limits |
| Two-piece (ceramic web + brazed metal flanges) | Would allow conventional flange machining, but introduces a braze joint in the isolation path and a CTE mismatch at the joint — **rejected** |

## 7. Material

**SEWCP-400: 99.5% Al₂O₃ (aluminium oxide) technical ceramic.**
**SEWCP-401: 316L stainless steel.**

| Property | Al₂O₃ 99.5% | Relevance |
|---|---|---|
| Thermal conductivity | 30 W/m·K | Thermal break (SR-05) |
| Volume resistivity | > 10¹⁴ Ω·cm at 20 °C | Insulation (SR-01) |
| Dielectric strength | ~15 kV/mm | 1500 V across 14 mm = 0.11 kV/mm → **136× margin** |
| Relative permittivity | 9.8 | Shunt capacitance (SR-02) |
| Loss tangent at 1 MHz | 0.0002 | Negligible RF heating |
| Flexural strength | 350 MPa | Structural (huge margin, §2.2) |
| Compressive strength | 2,500 MPa | Bolt bearing |
| CTE | 7.2 ppm/K | Drives the kinematic constraint scheme |
| Density | 3,900 kg/m³ | Mass |
| Max service temperature | > 1,500 °C | Enormous margin over 200 °C |
| Vacuum / plasma compatibility | Excellent | Standard semiconductor material |

**Material trade (closed, documented):**

| Candidate | k (W/m·K) | R_th (K/W) | ε_r | C (pF) | X_C (Ω) | Verdict |
|---|---|---|---|---|---|---|
| **Al₂O₃ 99.5%** | 30 | 0.195 | 9.8 | 27.0 | 435 | **Selected** — best overall balance; mature supply chain; standard in semiconductor tools |
| Y-TZP zirconia | 2.2 | 2.55 | 30 | 62 | 189 | 13× better thermal break, but 2.3× worse RF shunt and ~3× the cost. Reconsider only if parasitic heat leak becomes the binding constraint. |
| Virgin PEEK | 0.25 | 22.4 | 3.2 | 15 | 783 | Best thermal *and* electrical numbers, but **creeps under sustained bolt preload at 150 °C** — preload relaxation would loosen the entire stack. Rejected on that basis alone. |
| Fused silica | 1.4 | 4.0 | 3.8 | 17 | 691 | Excellent electrically and thermally; low fracture toughness and poor thermal-shock margin in a structural role |
| Ti-6Al-4V | 6.7 | 0.87 | — | short | 0 | **Rejected** — conductive; defeats Configuration A entirely |

Note that PEEK wins on both primary performance metrics and is still rejected. Creep under preload is a mechanism that does not appear in any steady-state performance calculation, and it would fail the assembly slowly and invisibly over months.

## 8. Surface Finish

| Surface | Finish | Reason |
|---|---|---|
| Bottom face (Datum A interface) | **Lapped Ra ≤ 0.4 µm**, flat 0.010 TIR | Primary datum transfer; also maximises real contact area for repeatable R_th |
| Top face (Cooling Plate interface) | **Lapped Ra ≤ 0.4 µm** | Same |
| Web OD and ID | As-ground Ra ≤ 0.8 µm | Reduces surface flaw population — thin-wall ceramic strength is surface-controlled |
| Flange faces (bolt bearing) | Ground Ra ≤ 0.8 µm, flat 0.020 | Even bearing under preload; prevents point loading |
| Bolt holes | As-drilled, **both ends chamfered 0.3 × 45°** | Edge chipping at hole mouths is the primary crack initiation site |
| Kinematic slots | Ground Ra ≤ 0.8 µm | Free sliding of the dowel without stick-slip |
| Web-to-flange fillets | R3.0 minimum, ground, no undercut | Stress concentration control |
| **All edges** | **0.3 × 45° minimum chamfer** | Handling damage control |
| Clamp ring (SEWCP-401) | Ra ≤ 0.8 µm bearing face, passivated | Even bearing on ceramic; corrosion resistance |

> **Every edge on this part is chamfered, and the drawing says so as a general note.** Technical ceramics do not fail from bulk stress — they fail from surface and edge flaws under stress concentration. A sharp, chipped hole mouth under 3 kN of bolt preload is how an alumina ring with a 140× compressive margin cracks anyway.

## 9. Tolerances

**GD&T scheme:**
- **Datum A** — bottom flange face (mates to Base Plate Datum A), flatness 0.010 after lap.
- **Datum B** — kinematic slot at 60°, Ø306 BC.
- **Datum C** — kinematic slot at 180°, Ø306 BC.

| Control | Feature | Tolerance |
|---|---|---|
| Flatness | Bottom face (A), post-lap | 0.010 |
| Parallelism | Top face to A, post-lap | 0.010 |
| Position | Kinematic slots | ⌖ Ø0.050 Ⓜ A B C |
| Position | Bolt clearance holes | ⌖ Ø0.30 Ⓜ A |
| Concentricity | Web ID to OD | 0.20 |
| Runout | Flange OD to A | 0.30 |
| Wall thickness | 3.00 ±0.15 | Measured at 8 positions, 45° apart |
| Height, as supplied | 20.300 −0/+0.050 | 8 points |
| Height, post-lap | Per DR-3, ±0.015 | 8 points |

**Tolerance philosophy for ceramic:** only the two lapped faces and the three kinematic slots are tight. Bolt holes are at ⌖ Ø0.30 — an order of magnitude looser than a comparable metal part — because ceramic hole position is expensive to control, the holes have Ø0.4 mm of designed clearance on M6, and **their position has no functional consequence.** Location comes from the kinematic slots, not the bolts. Specifying ⌖ Ø0.05 on ceramic bolt holes is a common and costly mistake.

## 10. Assembly Sequence

**This part is installed differently from every other component: it is machined to final height *during* assembly, after everything above it has been measured.**

**Phase 1 — Sub-assembly with the Cooling Plate (off-tool, inverted):**

1. Verify incoming ring: dye-penetrant inspection, dimensional check, no chips at any hole or edge.
2. Invert the Cooling Plate on a clean, padded fixture, bottom face up.
3. Place the Support Ring onto the Cooling Plate bottom face, engaging the 3 kinematic dowels into the ring's radial slots.
4. **Confirm all 3 dowels slide freely in their slots.** A bound locator here will crack the ring on the first thermal cycle.
5. Install the 8 upper M6 × 16 bolts through the ring's top flange into the Cooling Plate, with Ø16 flat washers and Belleville stacks. Torque in 3 passes (30 / 70 / 100%), star pattern, to **6.0 N·m**.
6. Place SEWCP-401 clamp ring into the register counterbore on the bottom flange.

**Phase 2 — Height determination (DR-3):**

7. Retrieve the recorded as-built values for the Cooling Plate (20.000 ±0.030), choke washer set (1.500), Heater Plate (8.000 ±0.020), bond line (0.400 ±0.050), ESC (6.000 ±0.020), and mesa height (0.020).
8. Compute **H_ring = 55.920 − Σ(measured elements)**.
9. Remove the ring from the Cooling Plate. Lap the **bottom** face to H_ring, holding ±0.015 mm and 0.010 TIR parallelism.
10. Re-verify height at 8 points; record on the build traveller.
11. Re-clean and re-inspect for lap-induced edge damage; re-chamfer if required.
12. Repeat steps 2–6 to re-establish the sub-assembly.

**Phase 3 — Installation onto the frozen Base Plate:**

13. Clean the Base Plate top face (Datum A); verify no particles or burrs.
14. Lower the Cooling Plate + Ring + Clamp Ring assembly onto the Base Plate, aligning the 8 bolt holes.
15. From beneath the Base Plate, install 8× M6 × 40 with Ø16 washers; thread into SEWCP-401.
16. Torque in 3 passes (30 / 70 / 100%), star pattern, to **6.0 N·m**. **Never fully torque one bolt before the others** — asymmetric preload on a thin-wall ceramic ring is the fastest way to crack it.
17. Measure insulation resistance, Cooling Plate → Base Plate: **≥ 1 GΩ at 1000 VDC**. Failure indicates a crack, a conductive particle bridging the web, or a misplaced washer — stop and disassemble.
18. Verify clearance ≥ 12 mm and creepage ≥ 20 mm by inspection.
19. Proceed to Heater Plate installation (Volume 02).

> **Handling rule:** the ring is transported and stored only in its dedicated foam-lined fixture, and is never set down on a bare bench. Between steps 9 and 12 it is at its most vulnerable — freshly lapped, unsupported, and with newly created edges.

## 11. Failure Modes

| # | Failure Mode | Cause | Effect | S | O | D | RPN | Mitigation |
|---|---|---|---|---|---|---|---|---|
| 1 | Ring fracture during assembly | Asymmetric torque, particle under the flange, dropped part, chipped hole edge | Stack collapse; full teardown | 10 | 3 | 3 | **90** | 3-pass star torque, Ø16 washers, 0.3 chamfer on every edge, dedicated handling fixture, dye-penetrant at receipt |
| 2 | Ring fracture in service | Bound kinematic slot → thermal stress; preload relaxation → fretting | Stack collapse; possible wafer and chamber damage | 10 | 2 | 5 | **100** | Free-slide verification at steps 4 and 16, Belleville preload maintenance, R3 fillets, proof load test at manufacture |
| 3 | Insulation failure (RF short to ground) | Crack through the web; conductive particle or film bridging; deposition build-up over time | Loss of RF bias; possible power supply damage; arcing | 9 | 3 | 3 | **81** | 40 mm creepage (2× requirement), IR test at assembly and periodically, web geometry that discourages line-of-sight deposition |
| 4 | Preload relaxation | Differential thermal expansion Al vs Al₂O₃ across the joint; ceramic seating | Joint looseness, fretting, position drift, eventual FM #2 | 7 | 4 | 5 | **140** | Belleville stacks sized for ≤ ±20% preload change over ΔT = 130 K; re-torque at first scheduled maintenance |
| 5 | Height error after lap | Wrong measurement input, lap taper, measurement at the wrong temperature | Wafer plane out of specification; requires re-lap or re-work | 6 | 4 | 2 | **48** | Independent verification of the DR-3 calculation, 8-point post-lap check, 20 °C metrology |
| 6 | Chipping at bolt holes | Drilling exit damage, sharp-edged washer, over-torque | Crack initiation site → FM #1 or #2 | 8 | 4 | 4 | **128** | Drill from both faces meeting mid-thickness, 0.3 chamfer both ends, large flat deburred washers, torque control |
| 7 | Thermal break degraded | Wrong material substituted; wall thicker than specified | Parasitic heat leak; chuck temperature follows chamber temperature | 6 | 2 | 6 | **72** | Wall thickness measured at 8 points; calorimetric R_th verification in ATP |
| 8 | Base Plate does not match the FBAs | Frozen part differs from assumption | Ring does not fit | 5 | 5 | 1 | **25** | **DR-1 by design: this part is the designated adapter.** Re-machine the ring only; the other 8 components are unaffected. Detection = 1 (immediately obvious at first fit). |
| 9 | Kinematic slot binds | Slot narrow, dowel oversized, particle, corrosion | Over-constraint → thermal stress → FM #2 | 8 | 3 | 4 | **96** | H8 slot on h6 dowel, 8 mm slot length for ±1.0 mm travel, explicit free-slide checks, clean assembly |
| 10 | Stray capacitance higher than modelled | Flanges widened in CAD; unmodelled adjacent grounded hardware | Reduced RF shunt impedance; power loss to ground | 5 | 4 | 5 | **100** | Flange OD dimensioned and flagged; RF impedance verified on the assembled stack |

**Highest RPNs: preload relaxation (140) and bolt-hole chipping (128).** Both are ceramic-specific mechanisms with no analogue in a metal design, and both are slow — they degrade the joint over months rather than failing it on day one. Note FM #8: a Base Plate mismatch has the *lowest* RPN in the table despite being the most likely single discrepancy, precisely because DR-1 made it a fitting problem instead of a redesign.

## 12. Design Rationale

**Superseded concept, and why it failed.** The initial architecture was a plain thin-wall cylinder with eight M6 bolts passing straight through the ceramic from the Base Plate into the Cooling Plate, isolated by alumina shoulder bushings. It does not work. A 3.0 mm wall cannot host a Ø7 mm clearance hole; adding local bosses to accommodate the bolts raised the conduction and dielectric area by 45%, which degraded R_th to 0.137 K/W and dropped the shunt impedance to 554 Ω — sacrificing exactly the two properties the thin wall existed to provide. The scheme also left RF-live bolt heads exposed beneath the grounded Base Plate, requiring protective caps and an interlocked safety skirt. The flanged, two-circuit design solves all of it: bolt loads go through generous flanges, the web stays thin, no fastener bridges the insulator, and eight ceramic bushings leave the bill of materials.

**Why the web is thin and the flanges are not.** Every square millimetre of web cross-section is simultaneously a heat leak and a capacitor plate. Every square millimetre of flange is bolt-bearing area. Separating those two functions into two different geometries — instead of compromising on a single uniform wall — is what allows both R_th = 0.195 K/W and X_C = 435 Ω to be met in one part.

**Why the flanges are no wider than the bolt circle requires.** They are a 9.6 pF parallel-plate capacitor across the vacuum gap, contributing 36% of the total shunt admittance. The instinct to add flange width "for stiffness" would degrade the RF isolation for no structural return, since the structural margin is already four orders of magnitude.

**Why three radial slots instead of two dowels.** Aluminium against alumina at Ø306 across 130 K moves 0.29 mm diametrally. Two rigid dowels would over-constrain that motion and put the ceramic in tension — the one loading mode it cannot tolerate. Three radial slots at 120° let the Cooling Plate expand about a fixed axis, holding concentricity to 20 µm while imposing essentially zero constraint force. **The constraint scheme is what makes a ceramic part survivable here.**

**Why the ring is the sacrificial adapter (DR-1).** The Base Plate was frozen before its interface was documented, so some FBA is likely wrong. Rather than distribute that risk across nine components, it is concentrated in the one part that is cheap relative to the assembly, off the critical path, and already being custom-ground. If FBA-3 is wrong, one ceramic ring is re-drilled.

**Why the ring is also the shim (DR-3).** Worst-case tolerance analysis of the Z stack fails the wafer-plane requirement by 3 µm. The alternatives were to tighten six part tolerances across four vendors, or to add one lapping operation to a part already on a grinder. Lapping the ring is cheaper, faster, and yields a 7× margin instead of a marginal pass — and it converts a statistical argument into a deterministic measurement.

**Why alumina and not PEEK, when PEEK has better numbers.** PEEK beats alumina on both headline metrics: 22 K/W of thermal resistance and 783 Ω of shunt impedance. It is rejected because it creeps under sustained bolt preload at 150 °C. Preload relaxation would loosen the entire stack over months, degrading R_choke, wafer-plane flatness, and RF joint integrity together — a slow, coupled, hard-to-diagnose failure. Steady-state performance calculations do not show this; it has to be caught by asking what the material does over time under load.

## 13. Why Semiconductor Tools Use This Design

- **Ceramic insulating standoffs beneath the pedestal are universal in RF-biased plasma tools.** The wafer pedestal is the powered electrode and must float from the grounded chamber. Alumina is the default choice across Lam, Applied Materials, and ASM equipment because it is a good insulator, a mediocre-but-adequate thermal conductor, structurally strong in compression, dimensionally stable, plasma- and vacuum-compatible, and available from a mature supply chain.

- **The thermal break is as important as the electrical one.** A pedestal thermally shorted to a chamber-temperature base plate cannot hold wafer temperature, because the chamber wall drifts with process history, cleans, and idle time. Isolating the temperature-controlled mass from the uncontrolled structure is what makes the coolant loop the authority.

- **Ceramic is always loaded in compression, never threaded, never in tension.** This is a rule across the industry. Ceramic components in semiconductor equipment are captured between metal members through clearance holes with large bearing washers and spring preload. Threading a ceramic part, or hanging a load from it in tension, is a design error that shows up as a cracked part in the field.

- **Kinematic and semi-kinematic mounting between dissimilar materials is standard practice** wherever a ceramic and a metal must stay concentric across a wide temperature range — chucks, showerheads, focus rings, window assemblies. Radial slots, spherical seats, and flexure mounts all solve the same problem: hold position without imposing constraint force.

- **Lap-to-fit spacers are common in real tool builds.** Production pedestals routinely carry a shim or a lapped standoff whose final thickness is set from measured build data, because the wafer plane is a tight requirement fed by a long stack of independently manufactured parts. Designing the adjustment in, rather than tightening every upstream tolerance, is the economical answer.

## 14. Interview Talking Points

1. **"One part does five jobs, and three of them are in direct conflict."** It's the insulator, the thermal break, the structural support, the interface adapter to a frozen part, and the assembly shim. Isolation and thermal break want it thin and non-conductive; structure wants it thick. The resolution is geometric — a 3 mm web for the physics, integral flanges for the bolt loads — rather than a compromise wall thickness that would have done both jobs badly.

2. **"My first design didn't work, and the reason is worth explaining."** I started with a plain thin-wall cylinder and bolts straight through the ceramic. A 3 mm wall can't host a Ø7 hole. Adding bosses to make it fit raised conduction and dielectric area 45%, pushing thermal resistance from 0.195 to 0.137 K/W and shunt impedance from 435 to 554 Ω the wrong way — it destroyed the two properties the thin wall existed for. The flanged, two-bolt-circuit design fixed it and removed eight insulating bushings from the BOM at the same time.

3. **"No fastener bridges the insulator."** The lower bolt set is entirely below the ceramic web at ground potential; the upper set is entirely above it at RF potential. The only path between them is 40 mm of ceramic creepage — twice the requirement. The naive alternative, one long bolt through an insulating sleeve, leaves an RF-live bolt head exposed under the grounded base plate and needs protective caps and an interlocked skirt to be safe. Better to make the geometry solve it.

4. **"36% of my shunt capacitance isn't in the ceramic."** The two mounting flanges form a parallel-plate capacitor across the 14 mm vacuum gap — 9.6 pF against 17.4 pF for the dielectric web. If you model only the ceramic you'll be optimistic by a third, and you'll happily widen the flanges for stiffness and lose 70 Ω of isolation for nothing. That's why flange OD is a dimensioned, flagged characteristic on a part with a 4,000× structural margin.

5. **"This part is not strength-driven, and knowing that is what let me make it thin."** The web sees 0.026 MPa from the stack dead weight against 2,500 MPa of compressive capability. Both preload circuits are locally self-reacting, so they never load the web at all. Once you establish that stress isn't the constraint, the wall thickness is set by what can be ground and handled in alumina — and the thermal and RF requirements become achievable simultaneously.

6. **"I rejected the material that won on both performance metrics."** PEEK gives 22 K/W and 783 Ω, comfortably better than alumina's 0.195 K/W and 435 Ω. It creeps under sustained preload at 150 °C. That loosens the whole stack over months, degrading the thermal choke, the wafer-plane flatness, and the RF joints together — a slow, coupled failure that no steady-state calculation reveals. You have to ask what the material does over time under load, not just what it does at t = 0.

7. **"The most likely discrepancy in this whole program has the lowest risk score in my FMEA."** The Base Plate was frozen before its interface was documented, so one of my seven assumptions is probably wrong. Because I made this ring the sole structural interface and gave every other touchpoint 2 mm of float, a mismatch is a fitting problem with a detection rating of 1 — obvious at first fit — and the fix is re-drilling one ceramic ring. Architecture converted the program's biggest unknown into its smallest risk.

8. **"Every edge is chamfered, and that's a functional callout."** Alumina has a 140× compressive margin under bolt preload and still cracks — from a chipped hole mouth, not from bulk stress. Ceramics fail from surface flaws under stress concentration. So the holes are drilled from both faces to meet mid-thickness, both ends are chamfered 0.3 mm, the washers are large and deburred, and the torque is applied in three star-pattern passes. Those are the details that decide whether a ceramic part survives assembly.

---

**END OF VOLUME 03**

*Next: Volume 04 — SEWCP-500 Electrostatic Chuck*
