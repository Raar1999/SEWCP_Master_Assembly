# SEWCP-ENG-003 — Heater Plate

**Part Number:** SEWCP-300 · **Volume:** 02 of 09 · **Revision:** A
**Parent:** SEWCP-ENG-001 Architecture & ICD · **Stack position:** 3 (above Cooling Plate, below ESC)
**Includes:** SEWCP-301 Thermal Choke Washer (16 off)

---

## 1. Engineering Purpose

The Heater Plate is the **temperature control actuator** of the platform. The Cooling Plate sets a cold, stable boundary condition; the Heater Plate pushes the ESC and wafer upward from it under closed-loop control.

Its second, equally important function is to be a **heat spreader**. A resistive element is a line source; the wafer requires a uniform plane source. The plate converts one into the other, and its thickness is chosen for that conversion rather than for strength.

Its third function is **mechanical carrier for the ESC**. The ESC is bonded to its top face, so the Heater Plate's flatness and its coefficient of thermal expansion directly determine bond-line stress — the dominant life-limiting mechanism of the whole assembly.

**Critically, this part only works because it is thermally isolated from the Cooling Plate.** Bolted flat against a 3 kW heat sink with a conventional thermal interface, a 2 kW heater would raise the plate less than 1 K. The thermal choke (§3.1) is therefore specified here, as an integral part of this component's function.

## 2. Functional Requirements

| ID | Requirement | Value | Verification |
|---|---|---|---|
| HP-01 | Total heater power | 2000 W at 208 VAC, 2 zones | Power measurement |
| HP-02 | Inner zone (r = 0–75 mm) | 500 W ± 5%, R = 86.5 Ω ± 5% | 4-wire resistance |
| HP-03 | Outer zone (r = 75–150 mm) | 1500 W ± 5%, R = 28.8 Ω ± 5% | 4-wire resistance |
| HP-04 | Surface power density | 28.3 kW/m² (2.83 W/cm²), uniform between zones | Design calculation |
| HP-05 | Sheath watt density | ≤ 2.1 W/cm² | Design calculation |
| HP-06 | Maximum operating temperature | 150 °C (bond-line limited) | — |
| HP-07 | Over-temperature trip | 175 °C, independent hardware thermostat | Functional test |
| HP-08 | Top-face temperature uniformity | ≤ ±1.5 °C across Ø290 at 150 °C | Thermal map, instrumented |
| HP-09 | Thermal ramp rate | ≥ 40 K/min at full power | Step response test |
| HP-10 | Thermal time constant | 280 s ± 20% | Step response test |
| HP-11 | Insulation resistance, element to sheath | > 100 MΩ at 500 VDC, hot and cold | Megohmmeter |
| HP-12 | Hipot, element to sheath | 1500 VAC, 60 s, no breakdown | Hipot tester |
| HP-13 | Bond face flatness | ≤ 0.015 mm TIR over Ø297 | CMM |
| HP-14 | Choke face flatness | ≤ 0.015 mm TIR | CMM |
| HP-15 | Overall thickness | 8.000 ± 0.020 mm | Micrometer, 8 points |
| HP-16 | Choke thermal resistance (with SEWCP-301) | **0.100 ± 0.030 K/W** | Calorimetric test |
| HP-17 | Choke face emissivity | ≤ 0.15 | Witness coupon |
| HP-18 | Mass (plate only) | ≤ 1.6 kg | Scale |
| HP-19 | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA |

### 2.1 Zone Power Balance

| Zone | Radial extent | Area (m²) | Power (W) | Density (kW/m²) |
|---|---|---|---|---|
| Inner | r = 0 to 75 mm | 0.01767 | 500 | 28.3 |
| Outer | r = 75 to 150 mm | 0.05301 | 1500 | 28.3 |
| **Total** | **Ø300** | **0.07069** | **2000** | **28.3** |

Zones are **power-density matched at nominal**, not power-matched. The outer zone retains independent trim authority to compensate for edge heat loss — radial losses at the plate perimeter always exceed the center, so the outer zone will run above nominal in service. Sizing both zones to the same nominal density gives the controller symmetric headroom in both directions.

### 2.2 Heater Element Sizing

| Zone | Groove path length | Sheath area | Watt density |
|---|---|---|---|
| Inner (spiral, r = 15→72, 6 mm pitch, 9.5 turns) | 2.60 m | 0.0245 m² | **20.4 kW/m² = 2.04 W/cm²** |
| Outer (spiral, r = 78→145, 6 mm pitch, 11.2 turns) | 7.85 m | 0.0740 m² | **20.3 kW/m² = 2.03 W/cm²** |

Both zones are held near 2.0 W/cm² sheath loading — well below the 10–30 W/cm² capability of mineral-insulated cable in an aluminum heat sink. **Conservative sheath loading is deliberate:** MI heater life is governed by sheath temperature, and the failure mode (element burnout) requires a full teardown to the bonded ESC sub-assembly to repair.

## 3. Mechanical Interfaces

| IF | Interface | Type | Detail |
|---|---|---|---|
| HP-IF-1 | To Cooling Plate — thermal | **Thermal choke** | 16× SEWCP-301 Ti washers, Ø22.0 OD × Ø10.5 ID × 1.50 thk, on lapped pads; 1.50 mm vacuum gap elsewhere |
| HP-IF-2 | To Cooling Plate — fastening | Bolted, floating | 16× M5 threaded holes (12 at Ø270 BC on 30° multiples, 4 at Ø90 BC at 45°+n·90°), **stainless helical inserts, 1×D**, **blind from the choke face, `HP-D12` 6.50 deep** — the hole **shall not break into the HP-IF-4 bond face**, which leaves 1.50 mm of material. **M5 × 25** bolts enter from below and engage 5.40 mm; clearance holes **and their counterbores** in the Cooling Plate are slotted (ECR-D-004) |
| HP-IF-3 | To Cooling Plate — location | Kinematic | 3× radial slots, 6.05 H8 W × 8.0 L × **3.00 D** (`HP-D09a`), at Ø260 BC on **75°/195°/315°** (re-clocked off the outer choke rays — ECR-D-010) in the bottom face, engaging the Ø6.000 h6 bosses of the SEWCP-700 locators hosted in the Cooling Plate |
| HP-IF-4 | To ESC (SEWCP-500) | Bonded | Full-face elastomer bond, 0.400 ± 0.050 mm, over Ø297 |
| HP-IF-5 | To ESC — He port | Sealed transfer | Central Ø6.0 H8 bore; 316L transfer tube with 2× FKM O-rings (Ø4 × 1.5 CS) giving 0.5 mm axial/radial float; secondary FKM O-ring Ø8 × 1.5 in a top-face groove |
| HP-IF-6 | To ESC — HV feeds | Insulated bores | 2× Ø8.0 bores at Ø60 BC, 0°/180°, alumina-tube-lined; spring-loaded contact pins bear on ESC underside metallization |
| HP-IF-7 | To Lift Pins | Clearance bores | 3× Ø6.0 H8 through-bores at Ø200 BC, 30°/150°/270° |
| HP-IF-8 | To Temp Sensor Bracket | Blind probe ports | 2× Ø1.7 H8 × 6.0 deep blind bores at r = 45 and r = 115 mm, 195°, entering from the bottom face; **cross-vented per DR-6** |
| HP-IF-9 | To heater power feed | Sealed terminations | 2× MI cable cold-lead exits at the OD, 165° and 195°, transitioning to a ceramic-insulated terminal block; RF filter box downstream |

### 3.1 Thermal Choke Design (SEWCP-301)

The choke is the defining feature of this interface and is specified quantitatively.

**Geometry:** 16× washers, Ti-6Al-4V Grade 5, Ø22.0 OD × Ø10.5 ID × 1.500 ± 0.010 mm.

| Term | Calculation | Value |
|---|---|---|
| Area per washer | π/4 × (22.0² − 10.5²) | 293.5 mm² |
| Total contact area, 16 washers | — | 4,696 mm² = 4.696×10⁻³ m² |
| Bulk conduction, Ti | R = L/(k·A) = 0.0015 / (6.7 × 4.696×10⁻³) | **0.0477 K/W** |
| Contact resistance, 2 interfaces | R = 2 / (h_c·A), h_c ≈ 8,000 W/m²·K | **0.0532 K/W** |
| **Total R_choke** | — | **0.1009 K/W** ✔ meets HP-16 |
| Parallel radiation path (ε ≤ 0.15, ΔT = 130 K) | Q_rad ≈ 4 W | Negligible |

**Why titanium:** Ti-6Al-4V has k = 6.7 W/m·K — 25× lower than aluminum — so a thin, mechanically robust washer produces the required resistance. An aluminum standoff of the same geometry would give R_bulk = 0.0019 K/W, effectively no choke at all. Titanium is also vacuum-compatible, non-magnetic, strong enough to carry bolt preload without creeping, and has a CTE (8.6 ppm/K) that does not add stress at the joint.

**Tuning variable (OI-3):** contact resistance is the uncertain term (h_c is preload- and finish-dependent). If measured R_choke falls outside 0.100 ± 0.030 K/W at qualification, the correction is **washer thickness** (linear in R_bulk) or **washer count**. No other component is affected — the choke is deliberately the tunable element of the thermal chain.

**Sorting requirement:** the 16 washers shall be supplied as a **thickness-sorted matched set with total variation ≤ 5 µm**, to protect the flatness budget (SEWCP-ENG-001 §5.1).

### 3.2 Heater-Groove Keep-Out at the Kinematic Slots (ECR-D-011)

The outer heater spiral (§2.2, **r = 78 → 145, 6.00 mm pitch**) and the `HP-IF-3` kinematic
slots are **machined into the same face** — §6 step 3 mills the grooves into the bottom face,
and `HP-IF-3` places the slots there too. Routed radially, the spiral and the slots intersect:

| | |
|---|---|
| Slot radial extent at Ø260 BC | r = 130 ± 4.0 → **126.0 to 134.0** |
| Outer-zone turn centres, 78 + 6n | …, 120, **126**, **132**, 138, … |
| Groove envelope at those turns (3.20 W) | 124.4–127.6 and 130.4–133.6 — **both inside the slot** |

A `HP-D09a` slot 3.00 mm deep therefore cuts a 3.20 mm deep groove containing brazed MI heater
cable, at **each of the three slot positions**. Neither shortening nor relocating the slot
escapes it: `AP-06` requires 0.399 mm of thermal travel on a 6.068 mm boss, so the minimum slot
length is **6.87 mm** against a 6.00 mm pitch, and the only clear annulus between the two zones
is r = 72–78, **6.00 mm** wide against a 6.05 mm slot.

> **Keep-out.** A volume of **≥ 12 mm radial × ≥ 10 mm tangential**, centred on each `HP-D09a`
> slot and extending the full groove depth, shall contain **no heater groove**. The outer
> spiral shall be routed **tangentially around** each keep-out, not interrupted and not
> detoured radially.

**Why tangentially.** A tangential detour distorts pitch locally; a radial detour leaves a void
the width of the keep-out. `HP-D08`'s rationale fixes the surface ripple at 4.6 mm of spreading
material and 6 mm of pitch, so pitch distortion is the smaller perturbation of the two — but it
is **not zero**, and it is not asserted to be. **`HP-08` (≤ ±1.5 °C across Ø290) shall be
re-verified by instrumented thermal map against the as-routed spiral**, per its own declared
verification method. This is a re-verification action, not a waiver.

## 4. Mating Components

| Mates To | Part No. | Interface | Nature |
|---|---|---|---|
| Cooling Plate | SEWCP-200 | HP-IF-1/2/3 | Supported on, through the choke; kinematically centered; free to grow radially |
| Thermal Choke Washers | SEWCP-301 | HP-IF-1 | 16 off, matched set |
| Electrostatic Chuck | SEWCP-500 | HP-IF-4/5/6 | **Permanently bonded** — forms a non-separable sub-assembly |
| Lift Pins | SEWCP-600 | HP-IF-7 | Clearance pass-through only; no guidance function |
| Vacuum Port (He path) | SEWCP-800 | HP-IF-5 | Receives the floating transfer tube |
| Temperature Sensor Bracket | SEWCP-1000 | HP-IF-8 | Zone control RTDs |
| Alignment Pins | SEWCP-700 | HP-IF-3 | Receives 3 locator bosses in radial slots |
| Base Plate | SEWCP-100 | None | No interface |

> **The Heater Plate and ESC are procured, bonded, tested, and replaced as a single field-replaceable sub-assembly (SEWCP-350).** They are never separated after bonding.

## 5. Critical Dimensions

| Ref | Dimension | Nominal | Tolerance | Criticality |
|---|---|---|---|---|
| HP-D01 | Outside diameter | Ø300.0 | ±0.10 | Low |
| HP-D02 | **Overall thickness** | **8.000** | **±0.020** | **Critical — Z stack** |
| HP-D03 | Bond face flatness | — | 0.015 TIR | **Critical — bond & wafer plane** |
| HP-D04 | Choke face flatness | — | 0.015 TIR | **Critical — R_choke** |
| HP-D05 | Bond-face to choke-face parallelism | — | 0.015 TIR | **Critical** |
| HP-D06 | Heater groove | 3.20 W × 3.20 D | +0.10 / −0 | High — braze fill |
| HP-D07 | Groove pitch | 6.00 | ±0.10 | High — uniformity |
| HP-D08 | Groove to bond face (min material) | 4.60 min | — | **Critical — spreading** |
| HP-D09 | Kinematic slot width | 6.05 | H8 | **Critical — centering** |
| HP-D10 | Kinematic slot length (radial) | 8.00 | +0.20 / −0 | **Critical — thermal float** |
| HP-D09a | **Kinematic slot depth** | **3.00** | **±0.10** | **High — 0.35 mm worst-case clearance on the 2.50 ±0.05 boss; matches `SR-D19` and `AP-IF-3` (ECR-D-007 action 4)** |
| HP-D11 | Kinematic slot position | Ø260 BC **@ 75°/195°/315°** | ⌖ Ø0.030 Ⓜ A B C | **Critical** (re-clocked, ECR-D-010) |
| HP-D12 | M5 tapped holes (16×), **blind from the choke face** | M5 × 0.8, 1×D (5.0) stainless helical insert; tapped depth **6.50 +0.30 / −0**, leaving **1.50 mm min** to the bond face | ⌖ Ø0.200 Ⓜ A B C | **High — must not reach HP-IF-4** |
| HP-D13 | Lift pin clearance bores | Ø6.000 | H8, ⌖ Ø0.100 Ⓜ | Medium |
| HP-D14 | He transfer bore | Ø6.000 | H8 | High — seal |
| HP-D15 | HV feed bores | Ø8.000 | H8, ⌖ Ø0.200 Ⓜ | Medium |
| HP-D16 | Secondary He O-ring groove (top face) | Ø8.0 × 1.90 W × 1.15 D | ±0.05 | **Critical — seal** |
| HP-D17 | RTD blind bore | Ø1.700 | H8, depth 6.0 ±0.2 | High — response |
| HP-D18 | Bond-face edge break | 0.5 × 45° | ±0.2 | High — bond fillet |
| HP-D19 | Choke washer thickness (SEWCP-301) | 1.500 | ±0.010, set variation ≤0.005 | **Critical — Z stack & R_choke** |

**HP-D08 rationale:** the 4.6 mm minimum aluminum thickness between the heater groove and the bond face is the **heat-spreading length**. Thinning it would print the heater spiral onto the wafer as a periodic temperature ripple; thickening it improves uniformity but raises thermal mass and slows response. 4.6 mm at 6 mm groove pitch keeps the surface ripple below 0.5 °C.

## 6. Manufacturing Method

**Machined 6061 plate with vacuum-brazed mineral-insulated heater cable, followed by full T6 re-heat-treatment.**

| Step | Operation | Notes |
|---|---|---|
| 1 | Procure 6061-T651 plate, Ø310 × 14 rough | Certified, UT inspected |
| 2 | Rough machine; stress relieve | |
| 3 | CNC mill the 2-zone spiral grooves into the **bottom** face, 3.2 × 3.2, 6 mm pitch | Grooves on the choke side, away from the bond face. **Route the outer spiral tangentially around each `HP-D09a` kinematic-slot keep-out — see §3 (ECR-D-011)** |
| 4 | Form and fit the MI heater cable (Ø3.0, Inconel 600 sheath, MgO, NiCr conductor) into the grooves | Cold-lead transitions at the OD |
| 5 | **Vacuum braze** with Al-Si 4047 filler at 595 °C | Full groove fill; no voids — voids are hot spots |
| 6 | **Re-heat-treat to T6:** solution 530 °C, controlled polymer quench, age 175 °C / 8 h | Restores temper lost during brazing |
| 7 | Stress relieve; check for distortion | Expect movement — this is why finish machining follows |
| 8 | Semi-finish both faces | |
| 9 | Finish machine: bores, slots, tapped holes, O-ring groove, RTD ports | Single setup to hold HP-D11 |
| 10 | Install stainless helical inserts in all 16 M5 holes | Robustness against soft base metal and repeated service |
| 11 | Electrical qualification: zone resistance, IR, hipot | Per HP-02/03/11/12 |
| 12 | Lap the bond face and the choke face | HP-D03/D04/D05 |
| 13 | **No anodize.** Choke face left bright (ε ≤ 0.15); bond face left bare for adhesion | See §8 |
| 14 | Clean and vacuum bake 120 °C / 4 h | |
| 15 | CMM inspection; record as-built thickness for the DR-3 lap calculation | |
| 16 | **Bond ESC** per SEWCP-ENG-005 §10 — becomes SEWCP-350 | Point of no return |

**Braze/heat-treat trade (documented, not open):**

| Approach | Verdict |
|---|---|
| **Al-Si 4047 vacuum braze + T6 re-heat-treat (selected)** | Best thermal contact between element and plate; fully dense; vacuum-clean. Cost: an extra heat-treat cycle and mandatory finish machining afterward. |
| Low-temperature Zn-Al braze (~400 °C) | Avoids re-heat-treat, but leaves 6061 over-aged (yield drops from 276 to ~150 MPa) and the joint is weaker |
| Mechanical swage with peened retaining strip | Cheapest, no thermal cycle, but contact conductance is variable part-to-part — makes HP-08 uniformity unrepeatable |
| Cast-in element | Excellent thermal contact, but casting alloys have lower k and porosity risk in a vacuum part |
| Bonded polyimide etched-foil heater | **Rejected** — outgasses, 200 °C limit, and cannot survive the bake-out |

**Manufacturing risk note:** step 6 quenches a plate containing a brazed dissimilar-metal insert. Use a controlled polymer quench, not water, to limit thermal shock cracking at the groove. Include one destructive sectioning sample per lot to verify braze fill ≥ 95% of groove cross-section.

## 7. Material

**Plate: 6061-T6 aluminum (re-heat-treated after braze).**
**Heater element: Inconel 600 sheathed, MgO insulated, NiCr conductor, Ø3.0 mm MI cable.**
**Choke washers (SEWCP-301): Ti-6Al-4V Grade 5.**

| Property | 6061-T6 | Ti-6Al-4V | Relevance |
|---|---|---|---|
| Thermal conductivity | 167 W/m·K | 6.7 W/m·K | Spreading / choking |
| CTE | 23.6 ppm/K | 8.6 ppm/K | Bond stress / joint stress |
| Density | 2,700 kg/m³ | 4,430 kg/m³ | Mass and thermal inertia |
| Specific heat | 896 J/kg·K | 526 J/kg·K | Response time |
| Yield (T6) | 276 MPa | 880 MPa | Preload capacity |
| Max service temp | ~200 °C | ~400 °C | Margin over 150 °C |

**Alternate plate material — AlSiC-9 metal matrix composite (70% SiC):** k ≈ 190 W/m·K, CTE ≈ 8.0 ppm/K. This is the **qualified alternate for high-ΔT operation.** Its CTE nearly matches alumina, which reduces ESC bond shear strain from 55% to 2.7% (see SEWCP-ENG-005 §12). It is not the baseline because it is expensive, hard to machine, and unnecessary at the 150 °C ceiling — but it is the correct answer if the operating range is ever extended.

## 8. Surface Finish

| Surface | Finish | Reason |
|---|---|---|
| **Bond face (top)** | Lapped **Ra 0.4 µm**, bare aluminum, no anodize, no conversion coating | Elastomer adhesion requires a clean, chemically active aluminum surface. Anodize would insulate thermally; a conversion coating would be a weak boundary layer in the bond. Surface is grit-blasted (fine alumina, 25 µm) then solvent-cleaned and primed immediately before bonding. |
| **Choke face (bottom)** | Lapped **Ra 0.4 µm**, bright as-machined, **ε ≤ 0.15**, no anodize | Emissivity control — anodize would raise ε to ~0.8 and add a ~50 W parallel radiation path that partially defeats the thermal choke |
| Choke washer contact zones | Lapped Ra ≤ 0.4 µm | Contact conductance is 53% of R_choke; finish is a first-order term, not cosmetic |
| Heater grooves (post-braze) | Machined flush with the choke face | Proud braze fillets would sit on the choke pads and corrupt R_choke |
| Bores and slots | Ra ≤ 0.8 µm | Free sliding of locator bosses and lift pins |
| O-ring groove | Ra 0.8–1.6 µm, no radial scratches | Seal integrity |
| OD and edges | Ra ≤ 1.6 µm, all edges broken 0.5 × 45° | Particle control; bond fillet formation |

> **This part is not anodized anywhere.** That is deliberate and unusual, and it should be stated explicitly on the drawing with a "DO NOT ANODIZE" note, because the default assumption for an aluminum vacuum part is that it will be. Both faces need bare metal — one for adhesion, one for emissivity.

## 9. Tolerances

**GD&T scheme:**
- **Datum A** — choke face (bottom), flatness 0.015.
- **Datum B** — kinematic slot at 30°, Ø260 BC.
- **Datum C** — kinematic slot at 150°, Ø260 BC.

| Control | Feature | Tolerance |
|---|---|---|
| Flatness | Choke face (A) | 0.015 |
| Flatness | Bond face | 0.015 |
| Parallelism | Bond face to A | 0.015 |
| Position | Kinematic slots | ⌖ Ø0.030 Ⓜ A B C |
| Position | He transfer bore | ⌖ Ø0.050 Ⓜ A B C |
| Position | Lift pin bores | ⌖ Ø0.100 Ⓜ A B C |
| Position | M5 tapped holes | ⌖ Ø0.200 Ⓜ A B C |
| Position | HV feed bores | ⌖ Ø0.200 Ⓜ A B C |
| Profile | Heater groove path | 0.20 |
| Profile | O-ring groove | 0.050 |
| Thickness | 8.000 ±0.020 | 8 points, 45° apart, Ø270 BC |
| Runout | OD to A | 0.20 |

**Thickness tolerance rationale:** ±0.020 mm on an 8 mm plate is tight for aluminum and is driven purely by the Z stack (SEWCP-ENG-001 §5.2). It is achievable because the plate is lapped, not milled, to final thickness — and because it is lapped *after* the brazing and heat-treatment cycles that would otherwise move it.

## 10. Assembly Sequence

**Sub-assembly (off-tool) — SEWCP-ENG-001 §10 steps A3–A5:**

1. Complete manufacture per §6 through step 15.
2. Record as-built thickness at 8 points (feeds the Support Ring lap calculation, DR-3).
3. Verify both zones: resistance within ±5%, IR > 100 MΩ at 500 VDC, hipot 1500 VAC / 60 s.
4. Install the He transfer tube with its two FKM O-rings; verify 0.5 mm float in both axes.
5. Install alumina liner tubes and spring-loaded HV contact pins in the two feed bores.
6. Fit the secondary He O-ring into the top-face groove.
7. **Bond the ESC** (see SEWCP-ENG-005 §10): grit-blast, clean, prime, dispense, fixture, vacuum-debulk, cure 60 °C.
8. C-scan the bond: voids < 2% of area, none > Ø3 mm. **Reject on failure — no rework is possible.**
9. Re-verify ESC surface flatness post-bond: ≤ 0.010 mm TIR.
10. The assembly is now SEWCP-350 and is handled only by its edges, in a dedicated fixture.

**Installation into the stack — SEWCP-ENG-001 §10 steps C6–C7:**

11. With the 16 sorted choke washers in place on the Cooling Plate pads, lower SEWCP-350 so the 3 kinematic locator bosses enter its radial slots.
12. **Confirm each locator boss is free to slide radially in its slot.** A bound locator will bow the plate and stress the bond.
13. Install 16× **M5 × 25** bolts from below, through Belleville stacks seated in the `CP-D26` counterbores, torquing in 3 passes (30 / 70 / 100%), star pattern, to **3.5 N·m**. **Do not substitute M5 × 30** — it bottoms out and enters the ESC bond line (ECR-D-004).
14. Re-confirm radial freedom after torque by verifying the plate can be nudged and returns.
15. Connect heater cold leads to the terminal block; verify continuity and IR through the RF filter box.
16. Install zone RTDs per Volume 09.

## 11. Failure Modes

| # | Failure Mode | Cause | Effect | S | O | D | RPN | Mitigation |
|---|---|---|---|---|---|---|---|---|
| 1 | Heater element burnout | Local hot spot from a braze void; over-temperature; sheath corrosion | Zone dead; **full teardown to replace the bonded sub-assembly** | 8 | 4 | 2 | **64** | ≤2.1 W/cm² sheath loading, ≥95% braze fill verified by lot sectioning, over-temp trip at 175 °C |
| 2 | Plate bow from over-constraint | Kinematic slot bound; fastener holes not slotted; uneven torque | Bond shear stress, flatness loss, wafer temperature non-uniformity | 7 | 3 | 4 | **84** | Radial slots + slotted clearance + Belleville; explicit free-slide check at steps 12 and 14 |
| 3 | R_choke out of tolerance | Contact resistance variation, anodize applied in error, braze proud of the pads | Wafer temperature setpoint unreachable or unstable | 6 | 5 | 3 | **90** | Lapped pads, DO-NOT-ANODIZE note, calorimetric verification, washer thickness as the tuning variable |
| 4 | Braze void under the element | Incomplete filler flow | Local hot spot → uniformity loss and eventual burnout (→ FM #1) | 7 | 4 | 5 | **140** | Vacuum braze, groove sizing +0.10/−0, destructive lot sample, thermal map in ATP |
| 5 | Distortion after re-heat-treat | Quench stresses | Fails HP-D02/D03/D05 | 6 | 6 | 2 | **72** | Controlled polymer quench, post-quench stress relief, **all finish machining after heat treat** |
| 6 | Thread stripping in M5 holes | Soft base metal, over-torque | Loss of preload, joint separation | 6 | 3 | 3 | **54** | Stainless helical inserts standard, torque schedule |
| 7 | He leak at transfer tube O-rings | Compression set, insufficient float, misalignment | Loss of backside gas → loss of wafer thermal contact | 7 | 3 | 4 | **84** | Two O-rings in series, secondary top-face O-ring, 0.5 mm designed float, leak test |
| 8 | Element-to-sheath insulation breakdown | MgO moisture absorption during storage | Ground fault, trip, possible RF-path fault | 7 | 3 | 3 | **63** | Sealed cold-lead terminations, bake-out before IR test, IR verified hot and cold |
| 9 | Emissivity drift on choke face | Oxidation, handling, fingerprints, incidental anodize | Radiation path grows, R_choke drifts, temperature control degrades slowly | 5 | 4 | 6 | **120** | Bright finish specified, clean-handling requirement, witness coupon, periodic R_choke re-verification |
| 10 | RF pickup on heater leads | Missing or degraded filter | Erratic control, controller damage, arcing | 7 | 3 | 4 | **84** | LC filter box mandatory (SEWCP-ENG-001 §6.5), single-point grounding |
| 11 | Virtual leak from RTD blind bores | Un-vented blind holes | Fails pump-down qualification | 5 | 5 | 6 | **150** | DR-6: cross-vent |

**Highest RPNs: virtual leaks (150), braze voids (140), and emissivity drift (120).** Note that two of the three top risks are slow-degradation, hard-to-detect mechanisms rather than hard failures — which is why the ATP includes a thermal map and a periodic R_choke re-verification rather than relying on a single acceptance test.

## 12. Design Rationale

**Why a discrete heater plate at all, when production ESCs embed the heater in the ceramic?**
Because SEWCP is a development platform, and a discrete plate is serviceable, instrumentable, and pedagogically legible. The honest cost is two additional thermal interfaces and a thicker stack. In a production tool the heater would be co-fired into the ESC ceramic or brazed into the cooling plate — I am specifying the simplified architecture knowingly, not by default, and the trade is stated here so it is not mistaken for an oversight.

**Why does the heater sit above the cooling plate rather than below it?**
Control authority. If the heater were beneath the sink, all of its power would flow through the coolant before reaching the wafer, and the heater would only be able to warm the coolant — an actuator with almost no gain and a very long delay. Placing the heater between the sink and the load, separated from the sink by a defined resistance, gives a well-conditioned first-order plant with τ ≈ 280 s and a clean operating relation, T_wafer ≈ T_coolant + P·R.

**Why is the thermal choke a set of titanium washers instead of a low-conductivity gasket?**
Three reasons. It is **deterministic** — the resistance is set by geometry and a known bulk conductivity, not by a compressible material's thickness-under-load. It is **tunable** — if the measured R is wrong, washer thickness changes it linearly, with no effect on any other part. And it **carries preload without creeping**, which a polymer gasket at 150 °C for thousands of hours would not.

**Why put the heater grooves on the bottom face rather than nearer the wafer?**
Uniformity. The 4.6 mm of solid aluminum between the groove and the bond face is the spreading length that converts a 6 mm-pitch line source into a uniform plane source. Moving the element closer to the wafer would improve response time slightly and print a visible temperature ripple on the wafer — a bad trade. It also keeps the grooves and braze on the same side as the choke, where the machining is already concentrated.

**Why zone the heater radially, and why 500 W / 1500 W?**
Heat loss from a disc is edge-dominated — radiation and conduction both scale with perimeter, while stored energy scales with area. A single-zone heater will always run the edge cold. Two radial zones with matched *power density* (28.3 kW/m² each) give the controller symmetric authority: at nominal both zones sit at the same duty, and the outer zone has headroom to trim upward against real edge losses without saturating.

**Why is the plate not anodized on either face?**
The bond face must be bare for adhesion; anodize is both a poor adhesion substrate and a thermal insulator in the primary heat path. The choke face must be bare for emissivity; anodize would raise ε from ~0.1 to ~0.8 and open a ~50 W radiative shunt across the choke. Two different physical arguments arrive at the same drawing note, which is why the note deserves to be explicit and prominent.

**Why accept a full re-heat-treatment after brazing?**
Because the alternative is worse. Brazing at 595 °C destroys the T6 temper; skipping the re-heat-treat leaves the plate near annealed (yield ~55 MPa), which cannot hold thread preload or resist handling damage. Using a low-temperature filler avoids the heat-treat but yields a weaker joint and still over-ages the alloy. Accepting the extra cycle — and then doing *all* finish machining afterward so distortion is machined away — is the clean solution.

## 13. Why Semiconductor Tools Use This Design

- **Multi-zone resistive heating with a chilled base is universal** in temperature-controlled wafer pedestals. Etch and deposition processes are strongly temperature-sensitive — etch rate, selectivity, film stress, and critical dimension all move with wafer temperature — so ±1–2 °C across 300 mm is a hard process requirement, not a nicety. Achieving it demands both a stable sink and a zoned actuator.

- **Radial zoning matches the physics of the problem.** Wafer temperature non-uniformity in a plasma tool is overwhelmingly radial: plasma density profiles, edge heat loss, and focus-ring coupling are all axisymmetric. Production chucks use anywhere from 2 to more than 100 zones, but the first and most valuable split is always inner/outer.

- **Mineral-insulated Inconel-sheathed heater cable is the vacuum-compatible standard.** Polyimide etched-foil heaters — the obvious cheap choice — outgas, delaminate, and cannot survive chamber bake-out. MI cable is metallic, hermetic, high-temperature, and can be brazed or cast into a metal body, which is why it appears in essentially every vacuum heater plate.

- **A deliberate thermal break between heater and chiller is standard practice.** It appears in different forms — a machined-down contact land, a gas gap, a low-conductivity standoff set — but it is always present in any pedestal that must both remove kilowatts of plasma heat and hold the wafer above coolant temperature. Engineers new to the field usually try to maximize conduction everywhere and then cannot understand why the heater has no authority.

- **The heater plate and ESC as a bonded, field-replaceable sub-assembly** reflects how these parts are actually serviced. ESCs are consumables with finite life (dielectric wear, mesa erosion, bond fatigue). Tools are designed so that the ceramic-plus-carrier comes out as a unit and the expensive, long-lead cooling base stays in the chamber.

## 14. Interview Talking Points

1. **"The most important feature on this part is a resistance I added on purpose."** Bolt a 2 kW heater flat onto a 3 kW chiller with a good thermal interface and the heater plate rises less than one kelvin — you've built a very expensive parasitic load. The thermal choke, 16 titanium washers at R = 0.10 K/W, is what converts the heater from a passenger into an actuator. I can show the arithmetic: 0.0477 K/W of titanium bulk plus 0.0532 K/W of contact resistance across two interfaces.

2. **"I chose titanium because its conductivity is 25× worse than aluminum, and that was the specification."** It's the only time in the design where I selected a material for being a *bad* conductor. Aluminum standoffs of identical geometry give 0.0019 K/W — no choke at all. Titanium also carries the bolt preload without creeping at 150 °C, which a polymer gasket would not, and its resistance is set by geometry rather than by compression, so it's deterministic and tunable.

3. **"Contact resistance is 53% of the choke, so surface finish is a first-order design variable."** The lapped Ra 0.4 µm callout on the washer pads isn't cosmetic — it's half the thermal budget of the dominant element in the chain. That's also why R_choke is the item I flagged as needing empirical tuning at qualification, and why I made washer thickness the adjustment knob: it's linear in R and affects nothing else.

4. **"This aluminum part is not anodized anywhere, and the drawing says so in capital letters."** Two independent arguments converge. The bond face needs bare, chemically active aluminum for elastomer adhesion. The choke face needs low emissivity — anodize takes ε from about 0.1 to 0.8 and opens a ~50 W radiative shunt straight across the choke I just spent effort designing. The default assumption for an aluminum vacuum part is that it gets hard-anodized, so the note has to be loud.

5. **"The 4.6 mm of aluminum above the heater groove is a heat-spreading length, not a strength dimension."** A heater cable is a line source at 6 mm pitch; the wafer needs a plane source. That thickness is what performs the conversion, and it's dimensioned as minimum material with a criticality flag. Thin it and you print the heater spiral onto the wafer as a periodic temperature ripple — a defect signature that looks like a process problem and is actually a mechanical one.

6. **"I zoned by power density, not by power."** 500 W inner and 1500 W outer both work out to 28.3 kW/m². Heat loss from a disc is edge-dominated, so the outer zone will always run hotter duty in service. Matching nominal density means the controller starts symmetric and the outer zone has room to trim upward without saturating — rather than starting at 90% duty and having nowhere to go.

7. **"Brazing at 595 °C destroys the T6 temper, so the process plan has to earn it back."** Solution treat, controlled polymer quench, age — and then do every finish machining operation afterward, because the quench will move the plate. Sequencing manufacturing around the metallurgy is the part people miss; they draw the part, add "braze heater," and are surprised when the finished plate is soft and bowed.

8. **"My two highest-RPN failures are both slow and invisible."** Virtual leaks from un-vented blind holes, and emissivity drift on the choke face. Neither one fails a functional test on day one. Both show up weeks later as a chamber that won't pump down or a chuck that has quietly lost temperature control. That's why the specification carries a global no-trapped-volumes rule and a periodic R_choke re-verification, instead of trusting a single acceptance measurement.

---

**END OF VOLUME 02**

*Next: Volume 03 — SEWCP-400 Chuck Support Ring*
