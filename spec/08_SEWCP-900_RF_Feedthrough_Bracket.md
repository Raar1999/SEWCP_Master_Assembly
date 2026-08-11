# SEWCP-ENG-009 — RF Feedthrough Bracket Assembly

**Part Number:** SEWCP-900 · **Volume:** 08 of 09 · **Revision:** A
**Parent:** SEWCP-ENG-001 Architecture & ICD
**Sub-parts:** SEWCP-901 RF Strap · SEWCP-902 Strap Support Bracket · SEWCP-903 Terminal Hardware Set · SEWCP-904 Deposition Shroud
**Applicability:** Configuration A (RF-hot chuck) only. **In Configuration B (grounded chuck) this entire assembly is deleted.**

---

## 1. Engineering Purpose

This assembly carries 13.56 MHz bias power from the chamber-mounted RF vacuum feedthrough to the Cooling Plate, which is the powered bias electrode.

It looks like a bracket. It is actually **a length of transmission line with a mechanical support**, and every requirement on it is electrical:

1. **Carry RF current with minimum loss.** At 13.56 MHz, current flows in the outer ~18 µm of the conductor, so surface geometry — not cross-sectional area — determines resistance.
2. **Present minimum series inductance.** Any reactance between the match network and the electrode shifts the match point, wastes power, and makes tuning drift with temperature.
3. **Hold that inductance constant.** Inductance is a function of geometry. If the strap can move, the impedance of the RF path moves with it, and the plasma changes. **The bracket's primary function is to make the strap's geometry repeatable and immovable.**
4. **Maintain isolation from ground** — clearance, creepage, and immunity to process deposition building a conductive path.
5. **Provide a low-resistance, stable bolted joint** at the electrode. A degrading RF joint is a thermal-runaway mechanism, not merely a loss.
6. **Absorb thermal and assembly movement** without transmitting load into the chuck or the ceramic support ring.

## 2. Functional Requirements

| ID | Requirement | Value | Verification |
|---|---|---|---|
| RF-01 | Frequency | 13.56 MHz | — |
| RF-02 | Power handling | ≤ 1000 W forward | — |
| RF-03 | Peak voltage | ≤ 1500 V | — |
| RF-04 | RMS current capability | ≥ 40 A | Analysis + thermal test |
| RF-05 | **Series inductance, feedthrough to electrode** | **≤ 35 nH** | Network analyser |
| RF-06 | **Inductance repeatability after service** | **±5%** | Network analyser, before/after |
| RF-07 | Strap AC resistance | ≤ 3 mΩ | 4-wire at frequency / calculation |
| RF-08 | **Terminal joint contact resistance** | **≤ 0.5 mΩ** | 4-wire micro-ohmmeter |
| RF-09 | Clearance to ground, vacuum side | ≥ 8 mm (with DR-11 in force) | Drawing + inspection |
| RF-10 | Clearance to ground, atmosphere side | ≥ 12 mm | Drawing |
| RF-11 | Creepage over any solid surface | ≥ 20 mm | Drawing |
| RF-12 | Compliance travel, all axes | ≥ ±3 mm at ≤ 5 N reaction | Force gauge |
| RF-13 | Base Plate pass-through | Clearance only, ≥ 2 mm radial (DR-1) | Drawing |
| RF-14 | Maximum strap temperature rise at rated power | ≤ 20 K | Thermal test |
| RF-15 | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA |

### 2.1 Skin Effect — Why the Conductor Is a Strap

Skin depth **δ = √(ρ / π f µ)** at 13.56 MHz:

| Material | ρ (Ω·m) | µ_r | δ | Surface resistance R_s = ρ/δ |
|---|---|---|---|---|
| **Silver** | 1.59×10⁻⁸ | 1 | **17.2 µm** | **9.23×10⁻⁴ Ω/sq** |
| **Copper (OFHC)** | 1.68×10⁻⁸ | 1 | **17.7 µm** | **9.49×10⁻⁴ Ω/sq** |
| **Nickel** | 6.99×10⁻⁸ | ~100 | **3.6 µm** | **1.94×10⁻² Ω/sq** |

**Nickel is 20× more resistive per square than copper at this frequency.** It is both more resistive *and* ferromagnetic, so its skin depth collapses and the current is forced into a thin, lossy layer.

Because current occupies only the outer ~18 µm, **conductor perimeter determines resistance, not area**:

| Conductor | Perimeter | AC resistance over 150 mm |
|---|---|---|
| Ø10 mm round rod | 31.4 mm | 4.5 mΩ |
| **50 × 0.5 mm strap** | **101 mm** | **1.4 mΩ** |

The strap has 3.2× the conducting perimeter of the rod at less than one-third of the mass.

**Loss check:** at 40 A RMS, P = I²R = 1600 × 1.4×10⁻³ = **2.2 W** — trivially handled.
**Joint check:** the same 40 A through a degraded 10 mΩ joint dissipates **16 W into a contact patch a few square millimetres in area.** That is the failure mechanism that matters (§11 FM #1), and it is why RF-08 is specified at 0.5 mΩ.

### 2.2 Inductance — the Governing Electrical Requirement

For a flat strap of width *w* at height *h* above a ground plane, over length *l*:

> **L ≈ µ₀ · l · h / w**

| Configuration | l | h | w | L | X_L at 13.56 MHz |
|---|---|---|---|---|---|
| Ø10 rod, 30 mm above ground | 150 mm | 30 mm | — | **74.5 nH** | **6.35 Ω** |
| 50 mm strap, 12 mm above ground | 150 mm | 12 mm | 50 mm | 45.2 nH | 3.85 Ω |
| **50 mm strap, 8 mm above ground (selected)** | **150 mm** | **8 mm** | **50 mm** | **30.2 nH** | **2.57 Ω** ✔ |
| 100 mm strap, 8 mm above ground | 150 mm | 8 mm | 100 mm | 15.1 nH | 1.29 Ω |

The selected configuration gives **2.5× lower reactance than a round rod.** Note the last row: doubling the strap width would halve the inductance again — but a 100 mm strap **cannot pass through the Ø60 mm Base Plate aperture** (FBA-5). The strap width is set by an aperture in a frozen part, not by the electrical optimum. This is stated plainly because it is the kind of constraint that gets discovered in CAD if it is not written down at freeze.

**Why inductance matters mechanically.** L depends on *h* and *w* — both geometric. A strap that sags, shifts, or is re-routed differently after maintenance changes the impedance the match network sees. RF-06 requires ±5% repeatability after service, and the only way to achieve that is to make the strap's position **mechanically determinate**. That is the bracket's real job.

### 2.3 Paschen Analysis — the Interlock That Falls Out of It

| Condition | Pressure | Gap | p·d | V_bd | vs. 1500 V |
|---|---|---|---|---|---|
| Atmosphere (vented, service) | 760 Torr | 12 mm | 912 Torr·cm | ≈ 36 kV | ✔ Safe |
| Process vacuum | 50 mTorr | 8 mm | 0.04 Torr·cm | ≫ 10 kV | ✔ Safe |
| **Pump-down / vent transient** | **≈ 0.5 Torr** | **8 mm** | **0.4 Torr·cm** | **≈ 330 V** | ✘ **HAZARD** |

> **DR-11: RF power shall be inhibited whenever chamber pressure lies between 10 Torr and 10 mTorr.** The transition band spans the air Paschen minimum, where an 8–12 mm gap breaks down at roughly 330 V — a fifth of the operating voltage.

**This is the most important electrical safety result in the volume.** The gap is safe at atmosphere and safe at process pressure, and the chamber passes through the unsafe band **twice per pump/vent cycle**. No amount of additional clearance fixes it — increasing the gap moves the hazardous pressure *lower*, into the range the chamber actually operates near. The correct countermeasure is a pressure interlock, not more space.

### 2.4 Why the Deposition Shroud Must Not Bridge the Gap

Process deposition builds conductive films on every exposed surface, gradually shorting clearance gaps. The instinctive fix — a ceramic sleeve spanning from the strap to the grounded structure — is **wrong**.

**In vacuum, the surface flashover voltage of a solid insulator is substantially lower than the breakdown voltage of the equivalent vacuum gap.** Bridging an RF-hot conductor to ground with a dielectric creates a flashover path that did not previously exist, and deposition on that dielectric makes it worse over time.

> **DR-12: No solid insulator shall bridge between the RF conductor and any grounded surface.** Isolation is maintained by vacuum clearance. The deposition shroud (SEWCP-904) **shields** line-of-sight deposition without spanning the gap, and carries anti-tracking grooves so that any film that does form is interrupted rather than continuous.

## 3. Mechanical Interfaces

| IF | Interface | Type | Detail |
|---|---|---|---|
| RF-IF-1 | Strap to Cooling Plate (SEWCP-200) | **Bolted electrical joint** | 60 × 18 mm land at Ø274 BC, 105°; 2× M6 × 16 silver-plated SHCS at r = 137, 98.7°/111.3°; **6.0 N·m**; silver-plated washers + Belleville |
| RF-IF-2 | Strap to RF vacuum feedthrough | **Bolted electrical joint** | 2× M6 to the feedthrough terminal; silver-plated hardware; **6.0 N·m** (feedthrough is chamber-mounted, external scope) |
| RF-IF-3 | Bracket to Cooling Plate | Bolted, structural | 2× M6 × 16 at **r = 150, 105° ± 17° (88°/122°)** — the former Ø274 BC ±40 mm window is fully occupied by the 30°-pitch choke stations and the land (found by the ACC-VOL check, DEC-02 addendum); **the bracket mounts to the RF-hot plate, not to ground** (§12) |
| RF-IF-4 | Bracket to strap | Saddle clamp | Non-conductive-critical clamp capturing the strap at mid-span, setting h = 8.0 mm above the Base Plate |
| RF-IF-5 | Through the Base Plate | **Clearance only** | Strap passes the central aperture with **≥ 2 mm radial clearance (DR-1)** and **≥ 8 mm to any grounded surface (RF-09)** |
| RF-IF-6 | Deposition shroud to bracket | Clipped | SEWCP-904 attaches to the bracket only; **does not touch grounded structure (DR-12)** |

### 3.1 RF Return Path — an Interface Requirement, Not an Assumption

The strap is only half the circuit. The return path is **chamber ground → Base Plate → chamber wall → plasma**, and the loop area between the outgoing strap and the return determines the inductance calculated in §2.2.

| Req | Requirement |
|---|---|
| R-1 | Base Plate bonded to chamber ground, ≤ 2 mΩ DC (FBA-6) |
| R-2 | The Base Plate directly beneath the strap run shall be **continuous, unbroken conductive surface** — the h = 8 mm figure assumes it is the return plane |
| R-3 | No slots, apertures, or non-conductive coatings in the Base Plate region directly under the strap, other than the central utility aperture |
| R-4 | RF feedthrough ground shell bonded to the Base Plate with the shortest practicable strap |

> **If the return path is routed the long way round, the loop area — and therefore the inductance — can be several times the calculated value regardless of how well the outgoing strap is designed.** Inductance is a property of the loop, not of the conductor.

## 4. Mating Components

| Mates To | Part No. | Interface | Nature |
|---|---|---|---|
| Cooling Plate | SEWCP-200 | RF-IF-1, -3 | Electrical termination **and** mechanical mounting; both on the RF-hot side |
| RF vacuum feedthrough | External | RF-IF-2 | Chamber-mounted; not SEWCP scope |
| Base Plate | SEWCP-100 | RF-IF-5 | **Clearance pass-through and RF return plane only** — no mechanical attachment |
| Chuck Support Ring | SEWCP-400 | None | **No contact permitted** — the bracket must not load the ceramic |
| Matching network | External | Via feedthrough | Sees the 30 nH of this assembly in series |

## 5. Critical Dimensions

### 5.1 SEWCP-901 RF Strap

| Ref | Dimension | Nominal | Tolerance | Criticality |
|---|---|---|---|---|
| RS-D01 | **Strap width** | **50.0** | **±0.5** | **Critical — inductance, aperture fit** |
| RS-D02 | Strap thickness | 0.50 | ±0.05 | Medium (skin effect ⇒ thickness is nearly irrelevant electrically) |
| RS-D03 | Developed length | 180.0 | ±2.0 | Medium |
| RS-D04 | **Installed height above the Base Plate** | **8.0** | **±1.0** | **Critical — inductance (RF-05)** |
| RS-D05 | Compliance loop radius | R20 | ±2 | **Critical — RF-12** |
| RS-D06 | Terminal pad, chuck end | 50 × 18 | ±0.5 | High |
| RS-D07 | Terminal bolt holes | 2× Ø6.6, **coincident with the CP-IF-8 taps** (r = 137 at 98.7°/111.3° → 29.94 mm centres in the pad plane; pad centred on the land) — *ECR-D-013 disposition A, DEC-01* | ⌖ Ø0.5 Ⓜ | High |
| RS-D08 | **Silver plating thickness** | **8 to 13 µm** | — | **Critical — RF-07, oxidation** |
| RS-D09 | **Underplate** | **NONE — silver directly on copper** | — | **Critical (DR-7)** |
| RS-D10 | Terminal pad flatness | 0.05 TIR | — | **Critical — contact resistance** |
| RS-D11 | All edges | Deburred, R0.5 min | — | High — field concentration |

### 5.2 SEWCP-902 Strap Support Bracket

| Ref | Dimension | Nominal | Tolerance | Criticality |
|---|---|---|---|---|
| SB-D01 | Strap bearing plane (sets RS-D04) | Bearing face **8.25** above the Base Plate, on the strap **top** face → strap mid-plane 8.0 | ±0.3 | **Critical — inductance** |
| SB-D02 | Bracket form | **Plate-hung hanger** (ECR-Q-012 disposition, DEC-02): one-piece 6061 U-plate, 5.0 web, mounted to the Cooling Plate bottom face (Z = 20); rails 10 wide at ±(34.4…44.4) from the strap axis, radial 68→140; saddle drop at radial 68–76 bearing at 8.25; cheeks to 8.0 guiding the 50.0 strap at 50.5 | ±0.3 form | High |
| SB-D03 | Mounting hole positions | 2× Ø6.6 clearance **at the CP-IF-8 bracket taps** (r = 150, 88°/122°); M6 × 16 SHCS, 6.0 N·m | ⌖ Ø0.5 Ⓜ | Medium |
| SB-D04 | Minimum clearance, any bracket surface to Base Plate | 8.0 min — satisfied by construction (minimum Z = 8.0 at the cheek tips; the bracket is RF-hot, mounted to the hot plate per RF-IF-3) | — | **Critical — RF-09** |

### 5.3 SEWCP-903 Terminal Hardware Set

| Item | Specification |
|---|---|
| Bolts | 4× M6 × 16 SHCS, A4-70, **silver-plated 5–8 µm** |
| Washers | 4× Ø16 flat, **silver-plated copper or silver-plated stainless** |
| Springs | 4× Belleville stacks, maintaining 6.7 kN ±20% over ΔT = 130 K |
| **Torque** | **6.0 N·m** (see §9) |

### 5.4 SEWCP-904 Deposition Shroud

| Ref | Dimension | Nominal | Criticality |
|---|---|---|---|
| DS-D01 | Material | Al₂O₃ 99.5% | — |
| DS-D02 | Anti-tracking grooves | 3 off, 3.0 W × 2.0 D | High |
| DS-D03 | **Minimum gap, shroud to any grounded surface** | **≥ 8.0 mm** | **Critical (DR-12 — must not bridge)** |
| DS-D04 | Creepage over shroud surface | ≥ 20 mm including grooves | High |

## 6. Manufacturing Method

**SEWCP-901 RF Strap:**

| Step | Operation | Notes |
|---|---|---|
| 1 | Blank 0.50 mm OFHC C10100 copper sheet to developed profile | Laser or die blanking |
| 2 | Deburr; radius all edges R0.5 minimum | Sharp edges concentrate field and initiate arcs |
| 3 | Form the compliance loop on a mandrel, R20 | Single forming operation; no work-hardening from repeated bending |
| 4 | Anneal if required to restore ductility | The strap must flex ±3 mm without fatigue |
| 5 | Clean and acid-pickle | |
| 6 | **Electroplate silver 8–13 µm, directly on copper. NO NICKEL UNDERPLATE.** | DR-7 — see §2.1 for the 20× loss penalty |
| 7 | Flatten and inspect terminal pads to 0.05 TIR | Contact resistance depends on real contact area |
| 8 | 4-wire resistance check | ≤ 3 mΩ |
| 9 | Clean, vacuum bake 150 °C / 4 h, bag | Silver tarnishes; handle with gloves only |

**SEWCP-902 Bracket:** CNC machined from 6061-T6; deburr; **Alodine 1200 chromate conversion coating (conductive) — not anodize**; clean; bake.

**SEWCP-904 Shroud:** green-machined and sintered 99.5% alumina; grind the anti-tracking grooves; chamfer all edges 0.3 × 45°; clean; bake 200 °C.

**Conductor alternatives considered:**

| Approach | Verdict |
|---|---|
| **Silver-plated OFHC copper strap (selected)** | Best perimeter-to-mass ratio; silver oxide is conductive, copper oxide is not; standard for RF busbar |
| Bare copper strap | Copper oxide is an insulator and grows over time — joint resistance rises steadily. **Rejected for the joint faces**, marginal elsewhere |
| Silver over nickel over copper | The default plating shop specification. **Explicitly prohibited** — nickel is ferromagnetic, R_s is 20× copper, and it sits exactly where the current flows |
| Ø10 silver-plated copper rod | 3.2× the AC resistance and 2.5× the inductance; simpler to route |
| Braided flexible strap | Excellent compliance, but strand-to-strand contact resistance is unstable at RF and the effective perimeter is poorly defined |
| Aluminium strap | Lighter and cheaper; 1.6× the resistivity, and aluminium oxide is a hard insulator that makes bolted RF joints unreliable |

## 7. Material

| Part | Material | Rationale |
|---|---|---|
| SEWCP-901 Strap | **OFHC copper C10100, silver-plated 8–13 µm** | Highest practical conductivity; silver prevents the oxide problem |
| SEWCP-902 Bracket | **6061-T6, Alodine 1200** | Light, machinable, and the conversion coating stays conductive (anodize would not) |
| SEWCP-903 Hardware | **A4-70 stainless, silver-plated** | Corrosion resistance with a low, stable contact interface |
| SEWCP-904 Shroud | **Al₂O₃ 99.5%** | Vacuum- and plasma-compatible insulator; low loss tangent (0.0002) so it does not heat in the RF field |

**The silver plating is primarily an oxidation countermeasure, not a conductivity improvement.** Silver's conductivity is only marginally better than copper's. What matters is that **silver oxide is electrically conductive while copper oxide is an insulator.** A bare copper bolted RF joint has a resistance that climbs steadily over months as oxide forms under the contact — the exact slow-degradation path to thermal runaway described in §11. Silver plating removes the mechanism.

**Why not PTFE for the shroud:** PTFE has an excellent loss tangent (0.0002) but creeps badly under any sustained load, cold-flows at temperature, and is a poor structural material in vacuum. **Why not PEEK:** vacuum-compatible and tough, but its loss tangent (~0.003) is 15× alumina's, so it heats in the RF field. Alumina is the correct choice for anything sitting in a high-field RF region.

## 8. Surface Finish

| Surface | Finish | Reason |
|---|---|---|
| **Strap terminal pads** | **Silver-plated, flat to 0.05 TIR, Ra ≤ 0.8 µm** | Contact resistance depends on real (asperity) contact area under preload |
| Strap general surface | Silver-plated, bright, no scratches through to copper | Any exposed copper oxidises and becomes a local resistance |
| **Strap edges** | **Deburred, R0.5 minimum** | Sharp edges concentrate electric field and are arc initiation sites at 1500 V |
| Cooling Plate RF land | **Masked from anodize; Alodine 1200 only**; flat 0.020 TIR, Ra ≤ 0.8 µm | Anodize is a dielectric — it would open-circuit the joint. Alodine is conductive. |
| Bracket | Alodine 1200, all over | Conductive, corrosion-resistant |
| Shroud | As-ground Ra ≤ 0.8 µm, all edges chamfered 0.3 × 45° | Ceramic edge-flaw control; smooth surfaces resist film adhesion |
| Fasteners and washers | Silver-plated 5–8 µm | Stable low-resistance interface at every current-carrying contact |

> **Every current-carrying surface in this assembly is silver-plated, including the bolts and washers.** The bolted joint's resistance is the sum of several interfaces in series, and plating only the strap while using bare stainless hardware leaves the highest-resistance interfaces untouched.

## 9. Tolerances

| Control | Feature | Tolerance |
|---|---|---|
| Width | Strap | 50.0 ±0.5 |
| **Installed height above the return plane** | Strap run | **8.0 ±1.0** |
| Flatness | Terminal pads | 0.05 TIR |
| Position | Terminal bolt holes | ⌖ Ø0.5 Ⓜ |
| Thickness | Silver plating | 8–13 µm |
| Clearance | Any RF surface to ground, vacuum side | **8.0 minimum** |
| Clearance | Shroud to any grounded surface | 8.0 minimum |

**Tolerance philosophy.** Almost nothing on this assembly is dimensionally tight, because almost nothing is dimensionally critical. Two exceptions carry the whole design:

- **Installed height, 8.0 ±1.0 mm.** Inductance is linear in *h*, so ±1 mm on 8 mm is ±12.5% on L — which lands directly against the ±5% repeatability requirement (RF-06) and consumes most of it. This is why the bracket sets the height with a hard saddle rather than leaving the strap to be dressed by hand.
- **Terminal pad flatness, 0.05 TIR.** Contact resistance is set by real contact area, which is set by flatness under preload.

Strap thickness, by contrast, is toleranced loosely at ±0.05 mm on 0.5 mm — a 10% variation that is electrically **irrelevant**, because at 17.7 µm skin depth the current never reaches the middle of the strap. Recognising which dimensions the physics actually cares about is the whole exercise.

## 10. Assembly Sequence

**Corresponds to SEWCP-ENG-001 §10 step D4 — installed after the thermal stack and vacuum port are complete.**

1. Confirm the platform is built to **Configuration A**. In Configuration B this assembly is not installed.
2. Verify the Cooling Plate RF land: **masked from anodize**, Alodine-coated, flat, clean, no oxide film. An anodized land is a rejection — the joint would be open-circuit.
3. Verify the Base Plate return-plane requirements R-1 to R-4, particularly that the region beneath the strap run is unbroken conductive surface.
4. Handle the strap with clean gloves only. **Do not touch the silver-plated terminal pads.**
5. Mount SEWCP-902 bracket to the Cooling Plate; torque 2× M6 to 6.0 N·m.
6. Route the strap from the feedthrough, through the Base Plate central aperture, to the land. **Verify ≥ 2 mm radial clearance at the aperture and ≥ 8 mm to every grounded surface along the entire run.**
7. Seat the strap in the bracket saddle. **Verify installed height 8.0 ± 1.0 mm above the Base Plate** — this sets the inductance.
8. Assemble the chuck-end terminal joint: silver-plated washer, Belleville stack, silver-plated M6 bolts.
9. **Torque to 6.0 N·m** in two alternating passes. *Note this is lower than the 6.0 N·m used elsewhere for the same size for a different reason:* silver plating drops the nut factor to K ≈ 0.15, so 6.0 N·m produces ≈ 6.7 kN — about 74% of A4-70 yield. Applying a dry-thread torque of 8.0 N·m to a silver-plated bolt would take it to ~99% of yield.
10. Repeat for the feedthrough-end terminal joint.
11. **Measure contact resistance across each terminal joint, 4-wire: ≤ 0.5 mΩ.** This is a go/no-go — a joint out of specification will not improve in service.
12. Verify strap compliance: displace the chuck end ±3 mm in each axis; reaction force ≤ 5 N; confirm no load is transmitted to the Support Ring.
13. Install SEWCP-904 shroud on the bracket. **Verify ≥ 8 mm gap to every grounded surface — the shroud must not bridge (DR-12).**
14. **Measure the assembly's series inductance with a network analyser; record as the baseline for RF-06.**
15. Verify DR-11 interlock function: RF inhibited between 10 Torr and 10 mTorr.
16. Verify insulation: no DC continuity from strap to Base Plate.

**Service note:** after any maintenance that disturbs the strap, steps 7, 11, and 14 shall be repeated. Inductance is a geometric property and a re-dressed strap is a different component electrically.

## 11. Failure Modes

| # | Failure Mode | Cause | Effect | S | O | D | RPN | Mitigation |
|---|---|---|---|---|---|---|---|---|
| 1 | **RF joint resistance rise → thermal runaway** | Preload relaxation, oxide growth, anodize on the land, unplated hardware, vibration | 40 A into a degrading joint: resistance rises → I²R heating → more oxidation → more resistance. Ends in a glowing joint or an arc. | 9 | 3 | 4 | **108** | Silver plating on **every** contact surface including bolts and washers; 6.7 kN preload with Bellevilles; Alodine-only land; 4-wire acceptance at ≤ 0.5 mΩ; PM re-measurement |
| 2 | **Arc during pump-down or vent** | Chamber transits the Paschen minimum with RF live | Strap and chuck damage; chamber contamination; possible feedthrough destruction | 9 | 3 | 3 | **81** | **DR-11** pressure interlock (RF inhibited 10 Torr to 10 mTorr); R0.5 edge radii; no sharp features |
| 3 | **Inductance drift after service** | Strap re-dressed by hand to a different height or route | Match point shifts; plasma changes; process drift blamed on chemistry for weeks | 7 | 5 | 7 | **245** | Hard saddle sets h = 8.0 ±1.0; installed height and inductance both verified and **recorded** at every service; documented service note |
| 4 | **Flashover across the deposition shroud** | Insulator bridging RF to ground; conductive film build-up | Loss of isolation; arc tracking; carbonised path that cannot be cleaned | 8 | 3 | 4 | **96** | **DR-12** — shroud never bridges; ≥ 8 mm gap maintained; anti-tracking grooves; ≥ 20 mm creepage |
| 5 | Nickel underplate applied by the plating vendor | Default shop practice; specification not read | 20× surface resistance where the current flows; heating and loss | 8 | 4 | 6 | **192** | DR-7 written on the drawing in prohibition form; **plating certificate required per lot**; cross-section verification on a witness coupon |
| 6 | Strap fatigue at the compliance loop | Repeated thermal cycling, poor forming, work-hardened material | Open circuit; loose conductor at 1500 V inside the chamber | 8 | 2 | 4 | **64** | R20 forming radius, annealed after forming, ±3 mm at ≤ 5 N, single forming operation |
| 7 | Strap contacts the Base Plate | Sag, routing error, thermal movement, vibration | Direct RF short to ground; loss of bias; possible generator fault | 9 | 2 | 2 | **36** | Bracket sets and holds position; ≥ 8 mm verified at installation; compliance loop absorbs movement |
| 8 | Return path routed long | Base Plate slotted or coated beneath the strap; poor feedthrough shell bond | Loop area grows; actual inductance several times the calculated value | 7 | 4 | 7 | **196** | Return-path requirements R-1 to R-4 written as binding ICD items; measured inductance (step 14) catches it |
| 9 | Bracket loads the Support Ring | Routing or mounting error | Stress into the alumina ring → cracking | 9 | 2 | 3 | **54** | Bracket mounts to the Cooling Plate only; no-contact requirement stated; compliance check at step 12 |
| 10 | Anodize on the RF land | Masking error on the Cooling Plate | Open-circuit joint; discovered only at RF power-on | 8 | 3 | 2 | **48** | Cooling Plate masking drawing; visual verification as installation step 2 |
| 11 | Silver tarnish before assembly | Storage in sulphur-bearing air; bare handling | Elevated joint resistance from the first day | 5 | 4 | 5 | **100** | Bagged storage, glove-only handling, contact resistance verified at assembly |

**The top three RPNs — inductance drift after service (245), return path routed long (196), and nickel underplate (192) — are all "the part is built correctly and the system still doesn't work" failures.** None of them is a broken component. All three are invisible to dimensional inspection, have detection ratings of 6 or 7, and manifest as process drift rather than hardware failure. That is the characteristic risk profile of RF hardware, and it is why this volume specifies *measurements* (contact resistance, installed height, inductance) as acceptance criteria rather than dimensions alone.

## 12. Design Rationale

**Why a strap and not a rod.** At 13.56 MHz the current lives in the outer 17.7 µm, so resistance scales with perimeter, not area. A 50 × 0.5 mm strap has 3.2× the perimeter of a Ø10 rod at less than a third of the mass, and — because inductance scales as h/w — 2.5× lower reactance. A rod is easier to route and worse in every electrical respect.

**Why the strap width is 50 mm and not 100 mm.** Purely because of the Ø60 mm Base Plate aperture (FBA-5). Doubling the width would halve the inductance to 15 nH. The electrical optimum is unreachable through a frozen part's aperture, and stating that constraint at freeze is the difference between a known limitation and a CAD-stage surprise.

**Why the bracket mounts to the Cooling Plate rather than to the Base Plate.** Three independent reasons converge. It honours **DR-1** — only the Support Ring structurally engages the frozen Base Plate, so no new Base Plate features are assumed. It removes any need for an insulating standoff, because bracket and strap are both at RF potential and there is no potential difference to stand off. And it guarantees the bracket **cannot load the ceramic Support Ring**, which the strap route passes near. A grounded bracket with an insulating column would have been the conventional answer, and it would have added a ceramic part, a new Frozen Baseline Assumption, and a flashover path.

**Why the bracket's real function is dimensional, not structural.** The strap weighs under 100 g and needs almost no support. What it needs is to be in the *same place* every time, because inductance is a geometric property. RF-06 demands ±5% inductance repeatability after service; the height tolerance of ±1 mm on 8 mm already consumes ±12.5%. A hand-dressed strap would not come close. The saddle exists to make an electrical parameter mechanically determinate.

**Why silver, and why the reasoning is about oxide rather than conductivity.** Silver's conductivity advantage over copper is marginal — about 5%. The decisive property is that **silver oxide conducts and copper oxide does not.** A bare copper bolted RF joint degrades continuously as oxide grows under the contact, which is precisely the slow-onset thermal-runaway mechanism in FM #1. Plating removes the mechanism rather than managing it.

**Why nickel underplate is prohibited rather than discouraged.** Silver-over-nickel-over-copper is the *default* specification at most plating shops, and it will be applied unless the drawing forbids it explicitly. Nickel is ferromagnetic, so at 13.56 MHz its skin depth collapses to 3.6 µm while its resistivity is 4.2× copper's — giving a surface resistance 20× worse, in exactly the layer that carries the current. An 8 µm nickel layer is more than two skin depths, so it would carry essentially all of it. This is why DR-7 is written in prohibition form and backed by a per-lot plating certificate.

**Why a pressure interlock instead of more clearance.** The gap is safe at 760 Torr and safe at 50 mTorr, and unsafe at roughly 0.5 Torr — which the chamber crosses twice per wafer cycle. Increasing the clearance does not remove the hazard; it moves the hazardous pressure *lower*, toward the range the chamber actually operates in. The only correct countermeasure is to forbid RF in the transition band. This is a case where the mechanical instinct (add margin) actively makes the problem worse.

**Why the shroud must not bridge the gap.** Surface flashover along a solid insulator in vacuum occurs at a substantially lower voltage than breakdown across the equivalent vacuum gap. A ceramic sleeve spanning from the strap to ground — the obvious way to guard against deposition shorting the gap — would create a flashover path that did not exist before, and deposition on the ceramic would steadily worsen it. The shroud shields line-of-sight deposition while remaining electrically clear of ground, and its anti-tracking grooves interrupt any film that does form.

**Why the return path is specified as an interface requirement.** Inductance is a property of the *loop*, not the conductor. A beautifully executed 30 nH strap over a Base Plate that has been slotted or coated beneath it can present several times that inductance, and nothing about the strap will reveal it. R-1 to R-4 exist because the half of the circuit that is not this assembly's hardware still determines this assembly's performance.

## 13. Why Semiconductor Tools Use This Design

- **Wide, thin, silver-plated straps are the standard RF conductor** in plasma tools, from the match network output to the electrode. The reasoning — skin effect makes perimeter matter and area irrelevant, and silver oxide conducts while copper oxide does not — is universal across RF power engineering, and it is why RF hardware looks so different from DC power hardware carrying the same current.

- **Minimising the RF loop area is a first-order design rule.** Production tools route the RF feed close and parallel to its ground return for exactly the h/w reason quantified in §2.2. Series inductance between the match and the electrode limits how well the match can tune, wastes power, and makes the tune point drift with temperature.

- **RF path geometry is treated as a controlled configuration item.** Production maintenance procedures specify how a strap is routed and dressed, and re-verify the match after service, because a re-dressed conductor is electrically a different component. Process engineers chasing an unexplained drift after a PM are very often chasing a strap that was put back three millimetres higher.

- **RF-off interlocks tied to chamber pressure are standard safety practice.** Every plasma tool inhibits RF outside its process pressure window, and the Paschen transition band is one of the main reasons. Arcing during pump-down damages feedthroughs, straps, and chuck surfaces, and the resulting contamination is expensive to clean.

- **Bolted RF joints are treated as maintenance-critical items** with specified torque, spring washers, plated hardware, and periodic resistance measurement. A high-current RF joint that degrades is a genuine fire and arcing hazard, not merely a loss of efficiency.

- **Dielectrics are kept out of high-field vacuum gaps.** The surface-flashover phenomenon is well known in RF and high-voltage vacuum design, and hardware is arranged so that insulators shield or support without spanning the gap they are protecting.

## 14. Interview Talking Points

1. **"This looks like a bracket, but every requirement on it is electrical."** At 13.56 MHz it's a length of transmission line. Its most important job isn't carrying load — the strap weighs under 100 grams — it's making the strap's *position* repeatable, because inductance is a function of height above the ground plane. A ±1 mm height variation on an 8 mm standoff is ±12.5% on inductance, against a ±5% repeatability requirement. The saddle exists to make an electrical parameter mechanically determinate.

2. **"Skin depth is 17.7 microns, so the strap thickness is nearly irrelevant and I toleranced it loosely on purpose."** Current never reaches the middle of a 0.5 mm strap. What matters is perimeter: 101 mm for a 50 × 0.5 strap versus 31 mm for a Ø10 rod — 3.2× the conductor at a third of the mass, and 2.5× lower inductance because L scales as h/w. Knowing which dimensions the physics cares about is what lets you spend tolerance where it counts.

3. **"Silver plating is about oxide chemistry, not conductivity."** Silver is only about 5% better than copper as a conductor. The decisive fact is that silver oxide conducts and copper oxide is an insulator. A bare copper bolted RF joint climbs in resistance for months as oxide forms under the contact — and 40 amps into a degrading joint is I²R heating, which drives more oxidation, which raises the resistance further. That's my highest-severity failure mode and plating removes the mechanism instead of managing it.

4. **"I banned nickel underplate on the drawing, because otherwise I'd have got it."** Silver-over-nickel-over-copper is the default at most plating shops. Nickel is ferromagnetic, so at 13.56 MHz its skin depth collapses to 3.6 microns while its resistivity is 4.2× copper's — a surface resistance 20× worse, sitting exactly where the current flows. Eight microns of nickel is more than two skin depths, so it would carry essentially all of it. The requirement is written as a prohibition with a per-lot plating certificate, because a preference would have been overridden by shop habit.

5. **"More clearance would have made the arcing hazard worse."** The gap is safe at atmosphere and safe at process vacuum. It's unsafe at about half a Torr, where p·d lands on the air Paschen minimum and an 8 mm gap breaks down around 330 volts against my 1500 volt operating level — and the chamber passes through that band twice per wafer cycle. Adding clearance just moves the dangerous pressure lower, toward where the tool actually runs. The fix is a pressure interlock, not space. It's the clearest case I have of a mechanical instinct being exactly backwards.

6. **"I deliberately did not put a ceramic sleeve across the gap, even though deposition will eventually short it."** In vacuum, surface flashover along a solid insulator happens at a lower voltage than breakdown across the equivalent vacuum gap. Bridging RF to ground with ceramic creates a path that didn't exist, and deposition on that ceramic makes it steadily worse. So the shroud shields line-of-sight deposition without spanning the gap, and carries anti-tracking grooves to interrupt any film that does form.

7. **"My three highest risks are all cases where the part is built perfectly and the system still doesn't work."** Inductance drift after a maintenance re-dress, the ground return being routed the long way round, and a nickel underplate. None is a broken component; all three are invisible to dimensional inspection and show up as process drift that gets blamed on chemistry for weeks. That's why acceptance for this assembly is *measurements* — contact resistance, installed height, and a network-analyser inductance baseline — rather than dimensions.

8. **"Inductance belongs to the loop, not to the conductor."** I can build a perfect 30 nH strap and get several times that if the base plate under it is slotted or coated, because the return path defines the loop area. So the return-path requirements are written as binding interface items — unbroken conductive plane beneath the run, shortest practicable feedthrough shell bond — even though none of that hardware is mine. Specifying the half of the circuit you don't own is part of owning the half you do.

9. **"I lowered the torque on the highest-preload joint in the assembly."** Silver plating drops the nut factor from about 0.2 to 0.15, so the 8 N·m I'd use on a dry M6 would put a plated bolt at roughly 99% of yield. At 6.0 N·m it lands at 6.7 kN — about 74%, which is where you want a joint that has to hold preload through 130 K of thermal cycling on Belleville washers. Torque tables assume a friction condition; changing the surface treatment changes the answer.

---

**END OF VOLUME 08**

*Next: Volume 09 — SEWCP-1000 Temperature Sensor Bracket*
