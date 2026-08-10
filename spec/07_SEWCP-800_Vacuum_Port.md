# SEWCP-ENG-008 — Vacuum Port Assembly

**Part Number:** SEWCP-800 · **Volume:** 07 of 09 · **Revision:** A
**Parent:** SEWCP-ENG-001 Architecture & ICD
**Sub-parts:** SEWCP-801 Port Body · SEWCP-802 Orifice Restrictor · SEWCP-803 O-Ring · SEWCP-804 VCR Gland Stub

---

## 0. Scope Clarification

In an electrostatic chuck there is no "vacuum chucking." The wafer is held electrostatically, and the port on the chuck axis serves the **backside gas plenum** — the sealed volume between the wafer backside and the ESC mesa field. That volume is alternately:

- **pressurised** with helium at 5–20 Torr during processing, to conduct heat from the wafer into the chuck; and
- **evacuated** to chamber pressure before dechucking, so residual gas does not blow the wafer off the pins.

SEWCP-800 is therefore a **bidirectional gas/vacuum service port**, and both directions are functional requirements. It is specified as one assembly because a single bore serves both, with the branch valving located off-platform.

## 1. Engineering Purpose

1. **Deliver backside helium** to the ESC plenum at a controlled pressure, sealed against chamber vacuum.
2. **Evacuate the plenum** on demand, so the dechuck sequence begins from chamber pressure.
3. **Limit the consequences of a broken wafer.** A cracked wafer removes the seal, and the plenum vents directly into the chamber. An integral orifice restrictor bounds that flow (§2.1) — and makes the event instantly detectable.
4. **Maintain the vacuum boundary** between an internally pressurised gas line and a 10⁻⁶ Torr chamber, across the full thermal range.
5. **Preserve RF isolation** — the port body is bolted to the RF-hot Cooling Plate, so the gas line leaving it is an RF path to ground unless deliberately broken.

## 2. Functional Requirements

| ID | Requirement | Value | Verification |
|---|---|---|---|
| VP-01 | Backside He pressure range | 5 to 20 Torr, regulated | Transducer |
| VP-02 | He pressure control accuracy | ±0.5 Torr | Transducer |
| VP-03 | Plenum evacuation | To chamber pressure in ≤ 3 s | Functional |
| VP-04 | **Orifice-limited flow at 20 Torr into vacuum** | **≤ 150 sccm (choked)** | Flow test |
| VP-05 | Normal operating leak (wafer clamped, 10 Torr) | < 2.0 sccm total | Flow measurement |
| VP-06 | Broken-wafer detection threshold | > 20 sccm sustained ⇒ abort | Functional |
| VP-07 | External leak rate, port to chamber | < 1×10⁻⁹ mbar·L/s He | Mass spectrometer |
| VP-08 | Proof pressure | 3.0 bar, 15 min | Hydrostatic / pneumatic |
| VP-09 | Operating temperature range | **−20 °C to +150 °C** | — |
| VP-10 | RF isolation of the gas line | Ceramic line break within 150 mm of the port | Design verification |
| VP-11 | Base Plate pass-through clearance | ≥ 2 mm radial (DR-1) | Drawing |
| VP-12 | Trapped volumes | **None** (DR-6) | Drawing review |
| VP-13 | Internal surface finish | Ra ≤ 0.4 µm, electropolished | Sample |
| VP-14 | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA |

### 2.1 Orifice Restrictor Sizing — the Broken-Wafer Case

If the wafer cracks, the mesa-field plenum is open to the chamber. Without a restrictor, the full Ø4.0 mm bore would vent.

**Choked (sonic) flow through the Ø0.50 mm orifice**, helium at 20 Torr (2,666 Pa), 300 K, γ = 1.667, R = 2,077 J/kg·K, C_d = 0.85:

> ṁ = C_d · A · P₀ · √(γ/RT) · (2/(γ+1))^((γ+1)/2(γ−1))
> A = π/4 × (0.5×10⁻³)² = 1.963×10⁻⁷ m²
> ṁ = 0.85 × 1.963×10⁻⁷ × 2666 × 1.636×10⁻³ × 0.5625 = **4.09×10⁻⁷ kg/s**
> → **≈ 138 sccm**

| Scenario | Flow | Chamber pressure rise at 1,000 L/s pumping |
|---|---|---|
| Normal operation, wafer clamped | < 2 sccm | negligible |
| **Broken wafer, Ø0.50 orifice** | **138 sccm = 1.75 Torr·L/s** | **≈ 1.75 mTorr** — survivable |
| Broken wafer, no orifice (Ø4.0 bore) | ~8,800 sccm = 112 Torr·L/s | ≈ 112 mTorr — major excursion |

**The orifice buys 64× of protection** (the bore-to-orifice area ratio) for the cost of one machined insert. It is sized to sit in a deliberate window:

- **Large enough** that the plenum still fills and evacuates within the required times, and that normal operation is unaffected.
- **Small enough** that a full-bore vent is a survivable pressure bump rather than a chamber-crash.
- **Detectable:** 138 sccm against a < 2 sccm normal signature is a **69× step change** — unmissable to a mass-flow controller, and the basis of the broken-wafer interlock (VP-06).

> **DR-10: Helium mass flow exceeding 20 sccm sustained, with the clamp energised, shall be interpreted as a broken wafer and shall abort the process, disable helium, and inhibit lift-pin motion.** This is one of the highest-value interlocks on the platform: it detects a broken wafer from a gas-flow signature before any mechanical motion can grind the fragments.

### 2.2 Paschen Analysis of the Gas Path

The gas path runs at 5–20 Torr helium through an assembly containing a 1,500 V electrode. Each segment is checked:

| Segment | Dimension | p·d at 10 Torr | vs. He minimum (≈4 Torr·cm, 155 V) | Exposed conductor in the gas? | Verdict |
|---|---|---|---|---|---|
| Port body bore, Ø4.0 | 0.40 cm | 4.0 Torr·cm | **At the minimum** | No — bore is entirely within parts at a single RF potential; **no potential difference exists across this gas** | **Safe** |
| Transfer tube through Heater Plate, Ø4.0 | 0.40 cm | 4.0 Torr·cm | At the minimum | No — same potential throughout | Safe |
| ESC central port, Ø1.5 | 0.15 cm | 1.5 Torr·cm | Left of minimum, but V_bd only ≈ 200–250 V | **No — the bipolar electrodes are fully encapsulated in dielectric; the ±1500 V conductors never contact the gas column** | **Safe** |
| Mesa-field gap, 20 µm | 0.002 cm | 0.02 Torr·cm | Far left | No | Safe |
| Lift pin annulus, 0.10 mm | 0.01 cm | 0.10 Torr·cm | Far left | No | Safe (DR-4) |

> **The governing insight is that a Paschen risk requires two things: an unfavourable p·d *and* a potential difference across that gas.** Two segments of this path sit at the helium Paschen minimum, and both are safe — because every conductor bounding them is either at a single potential or fully encapsulated in dielectric. This is why the ESC's electrodes are buried rather than surface-printed, and it is why the HV feed bores are routed in the chamber-vacuum region (p·d ≈ 10⁻⁶ Torr·cm) and never share a bore with the helium path.

## 3. Mechanical Interfaces

| IF | Interface | Type | Detail |
|---|---|---|---|
| VP-IF-1 | To Cooling Plate (SEWCP-200) | **Piloted, sealed, bolted** | Ø9.9 h8 pilot spigot × 8.0 into the Ø10.0 H8 central bore; face seal on the flange top face; 4× M4 × 16 SHCS at Ø38 BC, 1.8 N·m |
| VP-IF-2 | Seal | Face seal | FKM O-ring, 22.0 ID × 2.50 CS, **in a groove machined in the 316L port flange** (not in the aluminium plate — §12) |
| VP-IF-3 | To Heater Plate transfer tube | Bore continuity | Ø4.0 bore aligns with the Heater Plate's floating 316L transfer tube (HP-IF-5), which carries 2× FKM O-rings and 0.5 mm of float |
| VP-IF-4 | To ESC (SEWCP-500) | Gas path | Terminates at the ESC central Ø1.5 port; sealed by the bond land and a secondary FKM O-ring (HP-IF-5 / EC-IF-6) |
| VP-IF-5 | Through the Base Plate | **Clearance only** | Ø6.35 tube stub through the central aperture, **≥ 2 mm radial clearance in all directions (DR-1)** — no locating or sealing function at the Base Plate |
| VP-IF-6 | To facility gas panel | Face seal fitting | 1/4 in. VCR male gland, orbital-welded to the tube stub |

### 3.1 Off-Platform Manifold — Interface Control Requirements

The valve manifold is **outside SEWCP scope** but the following are binding:

| Req | Requirement |
|---|---|
| M-1 | **Ceramic gas-line break within 150 mm of the VCR gland** — the port body is RF-hot |
| M-2 | RF choke on the gas line downstream of the break |
| M-3 | He supply branch: mass-flow controller, 0–200 sccm range, with flow readback for DR-10 |
| M-4 | Vacuum branch: isolation valve to the chamber foreline |
| M-5 | Capacitance manometer, 0–50 Torr, on the plenum side |
| M-6 | Interlock: He enable requires clamp ON **and** lift pins full-down (DR-5) |
| M-7 | Interlock: He flow > 20 sccm sustained with clamp ON ⇒ abort (DR-10) |
| M-8 | Interlock: He setpoint > 10 Torr requires clamp voltage ≥ ±1800 V (Volume 04 §2.1) |
| M-9 | Leak-check access port upstream of the isolation valves |

## 4. Mating Components

| Mates To | Part No. | Interface | Nature |
|---|---|---|---|
| Cooling Plate | SEWCP-200 | VP-IF-1, -2 | Piloted, sealed, bolted; the port is at Cooling Plate (RF) potential |
| Heater Plate transfer tube | SEWCP-300 | VP-IF-3 | Floating tube bridges the 1.5 mm thermal choke gap |
| Electrostatic Chuck | SEWCP-500 | VP-IF-4 | Terminal destination of the gas path |
| Base Plate | SEWCP-100 | VP-IF-5 | **Clearance pass-through only** |
| Facility gas panel | — | VP-IF-6 | Via a mandatory ceramic RF line break |

## 5. Critical Dimensions

### 5.1 SEWCP-801 Port Body (316L)

| Ref | Dimension | Nominal | Tolerance | Criticality |
|---|---|---|---|---|
| VP-D01 | Flange diameter | Ø50.0 | ±0.20 | Low |
| VP-D02 | Flange thickness | 10.00 | ±0.10 | Low |
| VP-D03 | **Pilot spigot diameter** | **Ø9.90** | **h8** | **Critical — alignment to the transfer tube** |
| VP-D04 | Pilot spigot length | 8.00 | ±0.10 | Medium |
| VP-D05 | **Central bore** | **Ø4.00** | **H9** | High — flow, Paschen |
| VP-D06 | **O-ring groove mean diameter** | **Ø24.50** | **±0.05** | **Critical — seal** |
| VP-D07 | **O-ring groove width** | **3.20** | **+0.10 / −0** | **Critical — fill ratio** |
| VP-D08 | **O-ring groove depth** | **1.90** | **±0.03** | **Critical — squeeze** |
| VP-D09 | Groove corner radii | R0.3 max | — | High — O-ring damage |
| VP-D10 | Flange sealing face flatness | — | 0.010 TIR | **Critical — seal** |
| VP-D11 | Bolt clearance holes | 4× Ø4.5 at Ø38 BC | ⌖ Ø0.30 Ⓜ | Low |
| VP-D12 | Orifice seat bore | Ø6.00 | H7 | High — restrictor fit |
| VP-D13 | Tube stub OD × wall | Ø6.35 × 1.00 | ±0.05 | Medium |
| VP-D14 | Tube stub length | 100.0 | ±2.0 | Low |

**Seal design check (VP-D06 to VP-D08), FKM O-ring 22.0 ID × 2.50 CS:**

| Parameter | Calculation | Value | Criterion |
|---|---|---|---|
| Squeeze | (2.50 − 1.90) / 2.50 | **24.0%** | 20–30% for a static face seal ✔ |
| O-ring section area | π/4 × 2.50² | 4.91 mm² | — |
| Groove section area | 3.20 × 1.90 | 6.08 mm² | — |
| **Groove fill** | 4.91 / 6.08 | **81%** | ≤ 85% required, to leave room for thermal expansion ✔ |

> **Groove width is the callout most often got wrong.** A groove sized at the O-ring cross-section (2.50 mm wide) would give a 109% fill — the O-ring has nowhere to go under squeeze, extrudes, and the joint leaks or the ring is destroyed on the first thermal cycle. Face-seal grooves must be roughly 1.3× the cord diameter.

### 5.2 SEWCP-802 Orifice Restrictor (316L)

| Ref | Dimension | Nominal | Tolerance | Criticality |
|---|---|---|---|---|
| OR-D01 | **Orifice diameter** | **Ø0.500** | **±0.020** | **Critical — VP-04, DR-10** |
| OR-D02 | Orifice length | 1.00 | ±0.10 | High — discharge coefficient |
| OR-D03 | Disc outside diameter | Ø6.00 | h7 (light press into H7) |Medium |
| OR-D04 | Disc thickness | 3.00 | ±0.05 | Low |
| OR-D05 | Orifice inlet edge | Sharp, deburred, no radius | — | High — C_d repeatability |

### 5.3 SEWCP-803 O-Ring

| Item | Specification |
|---|---|
| Size | 22.0 mm ID × 2.50 mm CS |
| **Baseline material** | **FKM, low-temperature grade (GFLT type), −40 °C to +200 °C** |
| Alternate | FFKM (perfluoroelastomer) for plasma exposure or > 200 °C |
| Hardness | 75 ± 5 Shore A |
| Lubrication | Vacuum-grade fluorinated grease, **trace only** on installation |

> **The low-temperature grade is not optional.** Standard FKM has a glass transition around −18 to −25 °C, and the coolant loop operates to −20 °C (VP-09). A standard FKM ring would stiffen at the cold end of the range and leak precisely when the chuck is coldest. A GFLT-type grade extends the limit to −40 °C and restores margin.

## 6. Manufacturing Method

| Step | Operation | Notes |
|---|---|---|
| 1 | Machine SEWCP-801 body from 316L bar: flange, pilot spigot, bores, O-ring groove, bolt holes | Single setup for the spigot, bore, and groove — concentricity matters |
| 2 | Finish the O-ring groove with a form tool; R0.3 max corners | Sharp groove corners cut O-rings on assembly |
| 3 | Lap the flange sealing face to 0.010 TIR, Ra 0.8–1.6 µm | Circumferential lay only — **no radial scratches** |
| 4 | EDM-drill the SEWCP-802 orifice, Ø0.500 | EDM holds small-diameter tolerance and leaves a sharp inlet edge |
| 5 | Deburr the orifice; **do not break the inlet edge** | A radiused inlet raises C_d unpredictably and invalidates the VP-04 flow figure |
| 6 | Press and seal-weld the restrictor into the body bore | Weld is a secondary seal; press fit alone is not relied upon |
| 7 | Orbital-weld the Ø6.35 tube stub to the body | Full penetration, internally smooth, no filler |
| 8 | Orbital-weld the VCR gland (SEWCP-804) to the tube | |
| 9 | **Electropolish all internal surfaces to Ra ≤ 0.4 µm** | Reduces outgassing area and particle retention |
| 10 | Passivate | |
| 11 | **Proof test at 3.0 bar, 15 min** | |
| 12 | **He leak test, < 1×10⁻⁹ mbar·L/s** | |
| 13 | **Flow-verify the orifice**: measured choked flow at 20 Torr = 138 ± 15 sccm | Direct verification of the design basis, not just the hole diameter |
| 14 | Ultrasonic clean, DI rinse, vacuum bake 150 °C / 4 h | |
| 15 | Cap both ends; bag for cleanroom delivery | |

**Design alternatives considered:**

| Approach | Verdict |
|---|---|
| **Bolted 316L flange with an elastomer face seal (selected)** | Serviceable, tolerant of the Al/316L dissimilar-metal interface, no welding to the aluminium plate, replaceable seal |
| All-metal seal (CF or metal C-ring) | Lower leak rate and no elastomer, but needs far higher bolt load into aluminium and is not re-usable — over-specified for a 5–20 Torr gas service |
| Explosion-bonded Al/SS transition, welded to the plate | Eliminates the elastomer entirely, but makes the port non-serviceable and puts a weld into the Cooling Plate after it has been leak-qualified |
| Direct compression fitting into a tapped aluminium port | Cheapest; thread sealing into aluminium is unreliable in a thermally cycled vacuum joint, and creates a trapped volume at the thread |
| No orifice restrictor | Saves one part and forfeits 64× of broken-wafer protection and the DR-10 detection signature — **rejected** |

## 7. Material

**SEWCP-801, -802, -804: 316L stainless steel. SEWCP-803: FKM (GFLT grade).**

| Property | 316L | Relevance |
|---|---|---|
| Vacuum compatibility | Excellent, low outgassing when electropolished | VP-14 |
| Corrosion resistance | Excellent against He, moisture, process gases | Life |
| Weldability | Excellent (orbital, autogenous) | Hermetic joints |
| Magnetic permeability | Low (≤ 1.05 when properly annealed and lightly worked) | Plasma tool compatibility |
| Thermal conductivity | 16 W/m·K | **Bonus:** poor conductor, so the port adds little parasitic heat leak from the Cooling Plate |
| CTE | 16.0 ppm/K | vs 6061 at 23.6 — see §12 |

**Galvanic note:** 316L bolted to 6061 is a moderately active couple (≈ 0.3 V). It is acceptable here because there is **no liquid electrolyte** — the joint operates in vacuum or in dry cleanroom air. The requirement it does impose is that the assembly must not be exposed to condensing humidity during storage, and the O-ring must not trap moisture at the interface. Both are addressed by capping and dry storage.

## 8. Surface Finish

| Surface | Finish | Reason |
|---|---|---|
| **All internal gas-wetted surfaces** | **Electropolished, Ra ≤ 0.4 µm** | Minimises outgassing area, particle retention, and moisture adsorption; standard for semiconductor gas delivery |
| **Flange sealing face** | **Ra 0.8–1.6 µm, circumferential lay only, flat 0.010 TIR** | A radial scratch across a face seal is a leak path straight from ID to OD. Lay direction is a functional requirement, not a finish preference. |
| O-ring groove surfaces | Ra ≤ 1.6 µm, corners R0.3 max, no burrs | Sharp corners nick the O-ring during installation |
| Pilot spigot | Ra ≤ 1.6 µm | Slip fit |
| Orifice bore | As-EDM'd, **sharp inlet edge preserved** | Discharge coefficient repeatability |
| External surfaces | As-machined, passivated | — |
| Cooling Plate mating face | **Masked from anodize**, lapped flat 0.010 | Anodize is porous, friable, and an unreliable sealing surface (§12) |

## 9. Tolerances

**GD&T scheme:** Datum A = flange sealing face. Datum B = pilot spigot Ø9.90.

| Control | Feature | Tolerance |
|---|---|---|
| Flatness | Flange sealing face (A) | 0.010 |
| Perpendicularity | Pilot spigot to A | 0.020 |
| Concentricity | Central bore to B | 0.050 |
| Profile | O-ring groove | 0.050 |
| Position | Bolt holes | ⌖ Ø0.30 Ⓜ A B |
| Diameter | Orifice | Ø0.500 ±0.020 |

**Where the tolerance actually matters:** the three groove dimensions and the flange flatness carry the entire sealing function; the orifice diameter carries the entire protection function. Everything else — flange OD, stub length, bolt hole position — is open, because the port is piloted by its spigot and the assembly floats through the Base Plate aperture with 2 mm of clearance.

## 10. Assembly Sequence

**Corresponds to SEWCP-ENG-001 §10 step D1 — installed after the thermal stack is fully torqued.**

1. Verify the Cooling Plate sealing face: **masked from anodize** (bare aluminium), flat, clean, no radial scratches. An anodized face here is a rejection.
2. Verify the Heater Plate transfer tube is installed with both O-rings and has 0.5 mm of float.
3. Inspect the SEWCP-803 O-ring: correct material grade (GFLT), no nicks, no flash. Apply a **trace** of vacuum-grade fluorinated grease.
4. Fit the O-ring into the port flange groove; confirm it is seated and not twisted.
5. Offer the port body up, engaging the Ø9.90 pilot spigot into the Cooling Plate Ø10.0 bore. **The spigot must enter freely** — it aligns the bore to the transfer tube.
6. Install 4× M4 × 16 SHCS with anti-galling dry film. Torque in **two opposing passes to 1.8 N·m**. Even seating matters more than absolute torque on a face seal.
7. Route the tube stub through the Base Plate central aperture. **Verify ≥ 2 mm radial clearance in all directions** — the tube must not touch the grounded Base Plate at any point (RF short and vibration path).
8. Connect the VCR gland to the ceramic RF line break. Verify the break is within 150 mm.
9. **He leak test the assembly: < 1×10⁻⁹ mbar·L/s.**
10. Pressurise the plenum to 20 Torr with the chamber under vacuum and no wafer present; **verify choked flow of 138 ± 15 sccm.** This directly confirms the orifice and the DR-10 detection threshold in one measurement.
11. Install a bare Si wafer, clamp at ±1500 V, set He to 10 Torr; **verify total leak < 2.0 sccm.**
12. Verify plenum evacuation to chamber pressure in ≤ 3 s.
13. Verify interlocks M-6, M-7, M-8 functionally.

## 11. Failure Modes

| # | Failure Mode | Cause | Effect | S | O | D | RPN | Mitigation |
|---|---|---|---|---|---|---|---|---|
| 1 | **O-ring leak to chamber** | Compression set, wrong FKM grade at −20 °C, radial scratch on the sealing face, groove over-fill, pinched ring | Loss of backside gas control; chamber contamination by He; process drift | 7 | 4 | 3 | **84** | GFLT low-temperature grade, 24% squeeze / 81% fill, circumferential lay only, R0.3 groove corners, leak test at assembly and PM |
| 2 | **Orifice blockage** | Particle from the gas line, corrosion product, machining debris | Loss of wafer cooling; wafer over-temperature; **and loss of the broken-wafer detection signal** | 8 | 3 | 4 | **96** | Inlet filter on the gas panel, electropolished internals, flow verification in ATP and at PM, He flow readback monitored continuously |
| 3 | Broken wafer, undetected | Flow interlock disabled, MFC readback failed | Fragments ground by lift pins; chamber contamination; multi-hour recovery | 9 | 2 | 3 | **54** | DR-10 interlock, 69× flow step change, orifice bounds the excursion to ~1.75 mTorr |
| 4 | **RF path to ground via the gas line** | Ceramic break omitted, installed too far away, or bypassed by a metal bracket | RF power loss to ground; erratic plasma; possible arcing at the line break | 8 | 3 | 4 | **96** | M-1 (break within 150 mm), M-2 RF choke, ≥ 2 mm clearance at the Base Plate pass-through, verified at installation |
| 5 | Tube stub contacts the Base Plate | Routing error, thermal movement, vibration | RF short to ground; fretting; possible tube fatigue | 7 | 3 | 2 | **42** | ≥ 2 mm radial clearance specified and verified (VP-IF-5); flexible routing downstream |
| 6 | Weld defect at the stub or gland | Poor orbital weld, contamination | External leak; He into the chamber | 8 | 2 | 3 | **48** | Orbital welding, full penetration, 3 bar proof, He leak test at 10⁻⁹ |
| 7 | Anodize on the Cooling Plate sealing face | Masking error | Porous, friable sealing surface; unreliable seal that degrades over cycles | 7 | 3 | 4 | **84** | Explicit masking on the Cooling Plate drawing; visual verification as step 1 of installation |
| 8 | Transfer tube misalignment | Pilot spigot not engaged, tube float exhausted | Tube O-rings loaded off-axis; leak into the choke gap | 6 | 3 | 4 | **72** | Ø9.90 h8 pilot spigot, 0.5 mm designed float on the tube, free-entry check at step 5 |
| 9 | Galling of the M4 fasteners | 316L into 6061 without dry film | Non-serviceable port; damaged threads in an expensive plate | 6 | 3 | 3 | **54** | DR-8 anti-galling dry film mandatory; helical inserts on rework |
| 10 | Virtual leak at the flange or bolt holes | Trapped volume under the O-ring or in blind bolt holes | Fails pump-down qualification; slow, hard-to-find | 5 | 4 | 6 | **120** | DR-6 all blind holes vented; groove designed to 81% fill, not 100% |
| 11 | Condensation / galvanic attack at the Al–316L joint | Storage in humid air; vent-to-atmosphere with a cold plate | Corrosion at the sealing face; leak | 5 | 2 | 5 | **50** | Capped and dry storage; no condensing operation; passivation |

**Highest RPNs: virtual leaks (120), orifice blockage (96), and RF path to ground (96).** Note that orifice blockage is doubly severe — it removes wafer cooling *and* silently disables the broken-wafer detection that would otherwise catch the consequence. That coupling is the reason orifice flow is re-verified at every PM rather than only at build.

## 12. Design Rationale

**Why a bidirectional port instead of separate gas and vacuum ports.** Two ports would mean two bores through the ESC, two seals, two Paschen paths, and two more features competing with the coolant channel routing. One bore with off-platform branch valving costs nothing in function — the two modes are never simultaneous — and removes an entire penetration from the most sensitive part in the assembly.

**Why the plenum must be evacuated before dechuck.** If helium is still at 10 Torr when clamping voltage is removed, the residual pressure acts across the full wafer area and lifts the wafer off the mesas before the pins engage it. That is 13 mbar over 0.07 m² — about 92 N against a 1.25 N wafer. Evacuating first is not housekeeping; it is what prevents launching the wafer.

**Why the orifice restrictor earns its place.** It is one small machined insert, and it converts an uncontrolled failure into a bounded, instrumented one. A broken wafer without it is a 112 mTorr chamber excursion; with it, 1.75 mTorr. And because normal leakage is under 2 sccm while the orifice passes 138 sccm choked, the failure announces itself as a 69× step on a signal that is already being measured for process control. **Designing the failure mode to be self-announcing on an existing sensor is cheaper than adding a sensor.**

**Why the O-ring groove is in the 316L flange and not in the aluminium plate.** Three reasons. The Cooling Plate is hard-anodized, and anodize is porous and friable — an unreliable sealing surface, so the mating area must be masked anyway; masking a flat annulus is straightforward, masking inside a groove is not. Machining a precision groove in 316L is easier to hold and inspect. And the groove lives on the **serviceable, replaceable** part: if a groove is damaged, a small stainless flange is replaced rather than a 4.0 kg plate with a welded coolant circuit inside it.

**Why groove width is 3.2 mm for a 2.5 mm cord.** An O-ring under 24% squeeze has to displace its material somewhere. A groove machined at the cord diameter gives over 100% fill; the ring extrudes into the joint gap, takes a permanent set, and leaks — usually after a few thermal cycles rather than immediately, which makes it hard to diagnose. Sizing to roughly 1.3× cord diameter gives 81% fill and room for thermal expansion. This is the single most common elastomer seal error.

**Why sealing-face lay direction is specified.** A face seal leaks along a scratch that runs from inside the groove to outside it. Circumferential lay produces scratches that run *around* the seal and go nowhere; radial lay produces scratches that run *across* it. Specifying "circumferential lay only, no radial scratches" costs nothing and eliminates a whole class of intermittent leaks.

**Why the low-temperature FKM grade is mandatory.** The coolant loop specification runs to −20 °C, and standard FKM's glass transition sits at −18 to −25 °C. The seal would stiffen and lose compliance exactly at the cold end of the operating range. A GFLT-type grade moves the limit to −40 °C. This is a case where the component specification looks adequate against the *nominal* condition and fails against the *specified range* — worth checking every elastomer in the assembly against the extremes, not the setpoint.

**Why the tube passes through the Base Plate with clearance and nothing else.** Per DR-1, only the Support Ring may structurally engage the frozen Base Plate. The tube must also stay electrically clear: the port is at RF potential and the Base Plate is ground, so contact is a direct RF short. Two independent requirements — architectural firewall and RF isolation — arrive at the same 2 mm clearance callout.

**Why the CTE mismatch here is acceptable.** 316L at 16.0 ppm/K against 6061 at 23.6 ppm/K, over a Ø38 bolt circle and 130 K, gives about 0.037 mm of differential across the joint. The Ø4.5 bolt clearance on M4 absorbs it without slotting, and a face seal is insensitive to small radial motion because the sealing action is axial. It is worth noting explicitly, because the same mismatch would be unacceptable on a radial (bore) seal.

## 13. Why Semiconductor Tools Use This Design

- **Backside helium is the standard wafer cooling method in every plasma process tool.** A wafer in vacuum is thermally isolated; radiation alone cannot remove plasma heat. Helium at a few Torr in a controlled micro-gap is what makes wafer temperature controllable at all, and the chuck-axis gas port is a universal feature.

- **Orifice restrictors on backside gas lines are standard safety practice.** Every production chuck bounds the flow that a broken wafer can release, precisely because a wafer breaking on the chuck is a routine event over a tool's lifetime and must not become a chamber-crash. The associated flow-based broken-wafer interlock is equally standard.

- **Helium flow is a process-control signal, not just a utility.** Production tools monitor backside flow continuously: it reports seal integrity, wafer presence, wafer breakage, and chuck wear. Designing the mechanical hardware so that failures produce distinctive flow signatures is a deliberate practice.

- **Every service entering an RF-hot pedestal gets a dielectric break.** Gas line breaks, coolant line breaks, and RF filters on electrical services are standard equipment on biased chucks. Omitting one produces a tool that works on the bench and misbehaves under RF.

- **Elastomer face seals with electropolished 316L gas paths are the norm** for low-pressure gas service on chucks. All-metal seals are reserved for UHV boundaries and high-purity process gas; for a few Torr of helium behind a wafer, a serviceable elastomer face seal is the correct engineering and economic choice.

- **The plenum-evacuation step before dechuck is in every tool's wafer sequence** for the reason given above: residual backside pressure will lift a wafer off the chuck the instant the clamp releases.

## 14. Interview Talking Points

1. **"One small insert converts an uncontrolled failure into an instrumented one."** A wafer breaking on the chuck is routine over a tool's life. Without the Ø0.5 mm orifice, the plenum vents through a 4 mm bore — about 8,800 sccm, a 112 mTorr chamber excursion. With it, choked flow caps at 138 sccm and 1.75 mTorr. That's 64× of protection, which is just the area ratio, for the cost of one EDM'd disc.

2. **"I designed the failure to announce itself on a sensor I already had."** Normal backside leak is under 2 sccm; a broken wafer through the orifice is 138 sccm. That's a 69× step change on the mass-flow controller readback, which exists anyway for process control. So the broken-wafer interlock needs no new hardware — just a threshold. Making failure signatures large and distinctive on existing instrumentation is usually cheaper than adding detection.

3. **"Two segments of my gas path sit exactly on the helium Paschen minimum, and both are safe."** p·d comes out at 4 Torr·cm in the Ø4 mm bores — right at the 155 V minimum. They're safe because a Paschen risk needs *two* things: an unfavourable p·d **and** a potential difference across that gas. Those bores are bounded entirely by parts at a single RF potential, and the ESC's ±1500 V electrodes are fully encapsulated in dielectric, so no conductor ever touches the gas column. That's also why the HV feed bores are routed in the chamber-vacuum region and never share a bore with helium.

4. **"The most common O-ring mistake is making the groove as wide as the cord."** It looks correct on a drawing. A 2.5 mm cord in a 2.5 mm wide groove at 24% squeeze gives 109% fill — the ring has nowhere to go, extrudes into the joint gap, takes a set, and leaks after a few thermal cycles rather than immediately, which makes it painful to diagnose. Sizing to 1.3× cord gives 81% fill with room for thermal expansion.

5. **"I specify the lay direction on the sealing face, and that's a functional callout."** A face seal leaks along a scratch that runs from inside the groove to outside it. Circumferential lay makes scratches that run around the seal and go nowhere; radial lay makes scratches that run straight across it. Writing "circumferential lay only" costs nothing and removes an entire class of intermittent leaks that are otherwise nearly impossible to trace.

6. **"Standard Viton would have failed at the cold end of my own specification."** The coolant loop runs to −20 °C and standard FKM's glass transition is −18 to −25 °C. The seal looked fine against the nominal setpoint and stiffened exactly at the specified limit. A GFLT low-temperature grade moves it to −40 °C. It's a good reminder to check every elastomer against the extremes of the range you wrote, not the temperature you expect to run at.

7. **"The groove is in the stainless flange, not the aluminium plate, for three separate reasons."** The plate is hard-anodized and anodize is porous and friable — a bad sealing surface, so it has to be masked either way, and masking a flat annulus is far easier than masking inside a groove. A precision groove is easier to hold in 316L. And the groove ends up on the small, cheap, serviceable part rather than on a 4.0 kg plate with a welded coolant circuit inside it. Put the wear features on the replaceable side of the joint.

8. **"Evacuating the plenum before dechuck isn't housekeeping — it's what stops you launching the wafer."** Ten Torr of helium across 0.07 m² is about 92 N acting on a wafer that weighs 1.25 N. Release the clamp with that still pressurised and the wafer lifts off the mesas before the pins ever reach it. The sequence step exists because of a number, not because of convention.

---

**END OF VOLUME 07**

*Next: Volume 08 — SEWCP-900 RF Feedthrough Bracket Assembly*
