# SEWCP-ENG-002 — Cooling Plate

**Part Number:** SEWCP-200 · **Volume:** 01 of 09 · **Revision:** A
**Parent:** SEWCP-ENG-001 Architecture & ICD · **Stack position:** 2 (above Support Ring, below Heater Plate)

---

## 1. Engineering Purpose

The Cooling Plate is the **thermal ground of the platform and the RF bias electrode of the chuck**. It performs four jobs simultaneously, and every feature on it traces to one of them:

1. **Heat sink.** It removes plasma-deposited heat and heater trim power from the stack via a closed-loop liquid circuit, establishing the baseline temperature from which the heater works upward.
2. **Structural backbone.** It is the stiffest member of the thermal stack and carries the Heater Plate and ESC. Its flatness propagates directly to the wafer plane.
3. **RF bias electrode.** In Configuration A it is the powered 13.56 MHz electrode, capacitively coupled to the plasma through the ESC dielectric.
4. **Utility manifold.** All services to the ESC — helium, HV, lift pins, temperature probes — pass through it.

It is deliberately *not* in intimate thermal contact with the Heater Plate. The thermal choke between them is what makes closed-loop wafer temperature control possible (SEWCP-ENG-001 §4.3).

## 2. Functional Requirements

| ID | Requirement | Value | Verification |
|---|---|---|---|
| CP-01 | Heat removal capacity | ≥ 3000 W | Calorimetric test |
| CP-02 | Coolant flow rate at rated ΔP | 4.0 L/min at ΔP < 1.5 bar | Flow bench |
| CP-03 | Coolant temperature range | −20 °C to +80 °C | — |
| CP-04 | Coolant fluid | 50/50 water-glycol (baseline); Galden HT-135 (alt) | — |
| CP-05 | Proof pressure | 6.0 bar, 30 min, no permanent deformation | Hydrostatic |
| CP-06 | Burst pressure | ≥ 15 bar | Sample test, 1 per lot |
| CP-07 | Coolant circuit leak rate | < 1×10⁻⁹ mbar·L/s He | Mass spec |
| CP-08 | Top face flatness | ≤ 0.015 mm TIR over Ø300 | CMM |
| CP-09 | Top-to-bottom parallelism | ≤ 0.015 mm TIR | CMM |
| CP-10 | Overall thickness | 20.000 ± 0.030 mm | Micrometer, 8 points |
| CP-11 | Radial temperature uniformity of top face | ≤ 1.5 °C across Ø280 at 3 kW | Thermal map |
| CP-12 | Electrical isolation from Base Plate (installed) | ≥ 1 GΩ at 1000 VDC | Megohmmeter |
| CP-13 | RF strap contact resistance at land | ≤ 0.5 mΩ | 4-wire micro-ohmmeter |
| CP-14 | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA |
| CP-15 | Mass | ≤ 4.2 kg | Scale |

### 2.1 Coolant Circuit Sizing (design basis)

| Parameter | Value | Derivation |
|---|---|---|
| Channel cross-section | 10.0 mm W × 8.0 mm D | Selected |
| Flow area | 80 mm² = 8.0×10⁻⁵ m² | — |
| Volumetric flow | 4.0 L/min = 6.67×10⁻⁵ m³/s | CP-02 |
| Mean velocity | **0.83 m/s** | Q/A |
| Hydraulic diameter | 8.89 mm | 4A/P |
| Reynolds number | **≈ 7,400** | ρvD/µ — **turbulent**, as required for high h |
| Convective coefficient | ≈ 5,000 W/m²·K | Dittus-Boelter |
| Developed path length | ≈ 2.2 m | Serpentine layout |
| Wetted area | ≈ 0.09 m² | Path × perimeter |
| Coolant ΔT at 3 kW | **10.8 K** | Q / (ṁ·c_p), ṁ = 0.0667 kg/s |

Turbulence is a **requirement, not an outcome.** If flow drops below ≈ 2 L/min the channel goes transitional, h collapses, and the top-face uniformity requirement (CP-11) is lost. A minimum-flow interlock is required at the system level.

## 3. Mechanical Interfaces

| IF | Interface | Type | Detail |
|---|---|---|---|
| CP-IF-1 | To Chuck Support Ring (SEWCP-400) | Kinematic, load-bearing | 3× Ø6 h6 dowels press-fit into the bottom face at Ø306 BC, 60°/180°/300°, engaging radial slots in the Ring's top flange |
| CP-IF-2 | To Chuck Support Ring — fastening | Fastened, RF-side circuit | 8× **M6 × 1.0 tapped holes**, 12 mm deep, in the bottom face at Ø302 BC, 22.5°+n·45°; upper-circuit bolts enter from beneath the Ring's top flange (DR-9 — these bolts never reach the Base Plate) |
| CP-IF-3 | To Heater Plate (SEWCP-300) | Thermal choke + fastened | 16× M5 counterbored **radially slotted** clearance holes, 5.5 W × 7.0 L (12 at Ø270 BC, 4 at Ø90 BC), bolts from below into Heater Plate threads; 16× Ti washer seats on the top face |
| CP-IF-4 | To Heater Plate | Kinematic | 3× Ø6 h6 dowels press-fit into the top face at Ø260 BC, 30°/150°/270°, engaging radial slots in the Heater Plate |
| CP-IF-5 | To Vacuum Port (SEWCP-800) | Sealed, piloted bore | Central Ø10.0 H8 bore (receives the port-body pilot spigot); flat lapped sealing face on the bottom face, **masked from anodize**, Ø18–Ø32 annulus; 4× M4 × 10 deep tapped holes at Ø38 BC. **The O-ring groove is in the 316L port flange, not in this plate** (see Volume 07 §12) |
| CP-IF-6 | To Lift Pins (SEWCP-600) | **Loose lateral support** | 3× Ø8.0 H8 bores at Ø200 BC, counterbored Ø12 × 6 deep from below for the SEWCP-601 bushing (bushing bore Ø5.60 — deliberately loose; the pin is guided by the ESC bore, see Volume 05 §12) |
| CP-IF-7 | To ESC HV feed | Insulated bore | 2× Ø8.0 bores at Ø60 BC, alumina-tube-lined, 0°/180° |
| CP-IF-8 | To RF Bracket (SEWCP-900) | Bolted electrical land | Machined flat land, **60 mm circumferential × 18 mm radial, mean radius 137 mm (Ø274 BC), centred at 105°**, on the bottom face; **anodize-masked, Alodine 1200 only**; 2× M6 × 12 deep tapped at r = 137, 98.7° and 111.3° |
| CP-IF-9 | To Temp Sensor Retainers (SEWCP-1000) | Blind probe ports + retainer mounts | 3× Ø1.7 H8 × 12 deep blind holes entering the bottom face at **r = 40 @ 75°, r = 100 @ 165°, r = 140 @ 225°** (clocked clear of the RF land at 105°); **each cross-vented per DR-6**; plus 2× M4 × 8 deep tapped holes flanking each port at ±9 mm |
| CP-IF-10 | To coolant system | Fluid | 2× 1/2 in. VCR male gland stubs, orbital-welded, radial at 255° (inlet) / 285° (outlet) |

### 3.1 Coolant Channel Keep-Out Zones

The channel is confined to the **Ø60 to Ø250 annulus** (outer limit pulled in from Ø260 to leave solid material under the RF land) and shall maintain the following minimum wall thicknesses from every feature:

| Feature | Keep-out radius from feature axis | Min. wall to channel |
|---|---|---|
| Central He bore (Ø10) | 15 mm | 5.0 mm |
| Lift pin bores (Ø8, at Ø200 BC) | 12 mm | 4.0 mm |
| HV feed bores (Ø8, at Ø60 BC) | 12 mm | 4.0 mm |
| Choke fastener holes (M5, Ø90 & Ø270 BC) | 8 mm | 3.5 mm |
| Support Ring tapped holes (M6, Ø302 BC) | 9 mm | 3.5 mm |
| RTD blind ports | 6 mm | 3.0 mm |
| **RF land envelope** (r = 128 to 146, 93°–117°) | — | **No channel permitted; solid material required for M6 threads** |
| Plate OD and any external surface | — | 5.0 mm |

> **This keep-out table is a direct consequence of DR-2** (no fasteners through the wafer-facing surface). Because all 24 fasteners come from below, the coolant circuit must weave around them. CAD shall route the serpentine to satisfy the table **before** optimizing for path length.

## 4. Mating Components

| Mates To | Part No. | Interface | Nature of Constraint |
|---|---|---|---|
| Chuck Support Ring | SEWCP-400 | CP-IF-1, CP-IF-2 | Supported on; kinematically centered; electrically isolated from ground by it |
| Heater Plate | SEWCP-300 | CP-IF-3, CP-IF-4 | Carries it through the thermal choke; kinematically centered |
| Vacuum Port Assembly | SEWCP-800 | CP-IF-5 | Sealed bolted flange, bottom face |
| Lift Pins / Bushings | SEWCP-600 / -601 | CP-IF-6 | Guides pin travel |
| Electrostatic Chuck | SEWCP-500 | Indirect (via Heater Plate) | No direct contact |
| RF Feedthrough Bracket | SEWCP-900 | CP-IF-8 | Receives RF power at the bolted land |
| Temperature Sensor Bracket | SEWCP-1000 | CP-IF-9 | Receives spring-loaded RTD probes |
| Base Plate | SEWCP-100 | Via SEWCP-400 only | **No direct contact — isolation depends on it** |
| Alignment Pins | SEWCP-700 | CP-IF-1, CP-IF-4 | Hosts 6 press-fit dowels (3 down, 3 up) |

## 5. Critical Dimensions

| Ref | Dimension | Nominal | Tolerance | Criticality |
|---|---|---|---|---|
| CP-D01 | Outside diameter | Ø320.0 | ±0.10 | Low |
| CP-D02 | **Overall thickness** | **20.000** | **±0.030** | **Critical — Z stack** |
| CP-D03 | Top face flatness | — | 0.015 TIR | **Critical — wafer plane** |
| CP-D04 | Top-to-bottom parallelism | — | 0.015 TIR | **Critical — wafer plane** |
| CP-D05 | Coolant channel width | 10.00 | +0.20 / −0 | Medium |
| CP-D06 | Coolant channel depth | 8.00 | +0.20 / −0 | Medium |
| CP-D07 | Channel-to-top-face wall | 8.00 | ±0.20 | Medium — thermal |
| CP-D08 | FSW lid thickness | 6.00 | ±0.10 | Medium |
| CP-D09 | Kinematic dowel bore (bottom), Ø306 BC | Ø6.000 | H7 / press M6 | **Critical — centering** |
| CP-D10 | Kinematic dowel bore (top), Ø260 BC | Ø6.000 | H7 / press M6 | **Critical — centering** |
| CP-D11 | Kinematic dowel bolt-circle position | Ø306 / Ø260 | ⌖ Ø0.020 M @ B,C | **Critical** |
| CP-D12 | Lift pin bore | Ø8.000 | H8 | High — pin alignment |
| CP-D13 | Lift pin bore position | Ø200 BC | ⌖ Ø0.050 M @ A,B,C | High |
| CP-D14 | Lift pin bore perpendicularity to Datum A | — | 0.030 over 20 mm | **Critical — pin bind** |
| CP-D15 | Central He bore | Ø10.000 | H8 | Medium |
| CP-D16 | Vacuum port sealing face (flat, masked, Ø18–Ø32) | Flatness 0.010, Ra 0.8–1.6 | — | **Critical — seal** |
| CP-D17 | Choke washer seat pads (16×) | Ø22 flat, coplanar | 0.010 TIR set | **Critical — R_choke** |
| CP-D18 | RF land flatness | 60 × 18 land, Ø274 BC @ 105° | 0.020 TIR | **Critical — contact R** |
| CP-D19 | RTD blind bore (3×, r = 40/100/140 @ 75°/165°/225°) | Ø1.700 | H8, depth 12 ±0.2 | High — response |
| CP-D20 | M6 tapped holes (Ring upper circuit), Ø302 BC | M6 × 1.0 × 12 deep | ⌖ Ø0.30 Ⓜ | Low |
| CP-D21 | M5 tapped depth (into Heater Plate side) | — | See SEWCP-300 | — |

**Mass estimate:** Ø320 × 20 mm 6061 solid = 4.34 kg; less channel volume (≈ 0.18 L) and bores ≈ **3.9 kg**. Meets CP-15.

## 6. Manufacturing Method

**Two-piece construction, friction-stir-welded.**

| Step | Operation | Notes |
|---|---|---|
| 1 | Procure 6061-T651 plate, Ø330 × 30 rough | Certified, ultrasonically inspected for porosity |
| 2 | Rough machine body OD, faces; stress-relieve | **Mandatory** — 6061 plate carries residual stress that will bow the part after channel machining |
| 3 | CNC mill the serpentine channel into the **bottom** face | 10 W × 8 D, R5 minimum bend radius, all corners filleted R3 minimum |
| 4 | Machine the FSW lid, 6.00 mm, matching profile | Same 6061-T651 lot |
| 5 | **Friction stir weld** the lid to the body | Circumferential + internal rib passes; no filler, no flux, no elastomer in the pressure boundary |
| 6 | NDT the weld — dye penetrant + radiography | Weld defects here are a coolant-into-vacuum event (FMEA #6) |
| 7 | Hydrostatic proof, 6 bar / 30 min | Before any finish machining |
| 8 | Semi-finish all faces; second stress relief | |
| 9 | Finish machine: bores, counterbores, choke pads, RF land, O-ring groove, tapped holes | Single setup where possible to hold CP-D11 |
| 10 | Orbital-weld the 2× VCR gland stubs | Full-penetration, internally smooth |
| 11 | Helium leak test, < 1×10⁻⁹ mbar·L/s | Mass spectrometer, He bagged |
| 12 | Press-fit 6× alignment dowels (SEWCP-700) | 3 bottom, 3 top |
| 13 | **Mask** channel interior, choke pads, RF land, sealing faces, dowel bores; hard anodize | See §8 |
| 14 | Strip masks; final lap the top face | To CP-D03 / CP-D04 |
| 15 | Clean: ultrasonic → DI rinse → IPA → vacuum bake 120 °C / 4 h | Per SEWCP-ENG-001 §10 C1 |
| 16 | Final inspection and CMM report | Full dimensional per §5 |

**Alternative constructions considered:**

| Method | Verdict |
|---|---|
| **Friction stir welding (selected)** | Full-strength joint, no filler, vacuum-clean, proven in semiconductor chuck manufacture |
| Vacuum brazing (Al-Si filler) | Viable alternate; risk of filler flow into the channel and of T6 temper loss requiring re-solutionizing |
| Gun-drilled cross-bores with plugs | Cheapest, but plugs are leak paths and the routing cannot avoid the fastener keep-outs |
| O-ring-sealed bolted lid | **Rejected** — an elastomer in the coolant pressure boundary facing vacuum is an unacceptable single-point contamination risk |

**Stress relief is called out twice and is not optional.** A 20 mm aluminum plate with 60% of its lower face milled into a channel will move. Machining flat and then discovering 80 µm of bow at final inspection is the classic way to scrap this part.

## 7. Material

**6061-T6 / T651 aluminum alloy.**

| Property | Value | Relevance |
|---|---|---|
| Thermal conductivity | 167 W/m·K | Spreads heat; keeps plate-internal ΔT < 1 K |
| Density | 2,700 kg/m³ | Mass budget |
| CTE | 23.6 ppm/K | Drives the kinematic constraint scheme |
| Specific heat | 896 J/kg·K | Thermal time constant |
| Yield strength (T6) | 276 MPa | Pressure boundary, bolt preload |
| Elastic modulus | 68.9 GPa | Stiffness / deflection |
| Vacuum compatibility | Excellent when anodized and cleaned | — |

**Rationale for 6061-T6 over alternatives:**

| Candidate | k (W/m·K) | Why not selected |
|---|---|---|
| **6061-T6** | 167 | **Selected** — best k/machinability/cost/weldability combination; FSW-proven |
| 1100 / 6063 | 222 / 201 | Higher k, but too soft for threads and bolt preload |
| Cu C10100 | 391 | Excellent k, but 3.3× the mass, poor for RF-hot floating body, galvanic and contamination issues |
| 316L SS | 16 | 10× worse k — would destroy CP-11 uniformity |
| AlSiC-9 MMC | ~190 | Excellent, but unnecessary here (the CTE-match problem lives at the ESC bond, not this plate) |

## 8. Surface Finish

| Surface | Finish | Reason |
|---|---|---|
| Top face (choke side) | Lapped Ra ≤ 0.4 µm, **bright, NOT anodized**, emissivity ε ≤ 0.15 | Anodize would raise ε to ~0.8 and add ~50 W of radiative coupling across the choke gap, degrading the deliberate thermal break |
| Choke washer seat pads (16×) | Lapped Ra ≤ 0.4 µm, masked from anodize, coplanar 0.010 TIR | Contact conductance drives R_choke; anodize is an insulator and would make R_choke unpredictable |
| RF land (CP-IF-8) | Ra ≤ 0.8 µm, **masked from anodize**, chromate conversion (Alodine 1200) only | Must be electrically conductive; Alodine is conductive, anodize is not |
| Coolant channel interior | As-milled Ra ≤ 3.2 µm, deburred, **masked from anodize** | Anodize flakes into the coolant loop and blocks the heat exchanger |
| O-ring sealing face | Ra 0.8–1.6 µm, no radial scratches | Seal integrity |
| Lift pin bores | Ra ≤ 0.8 µm, honed | Pin travel without stick-slip or galling |
| Bottom face and OD (exposed) | **Type III hard anodize, 50 µm, sealed** | Plasma and handling durability; dielectric protection of the RF-hot body |
| Dowel bores | Ra ≤ 0.8 µm, masked | Press-fit dimensional integrity |

> **The masking drawing is as important as the machining drawing.** Five distinct surfaces on this part must be excluded from anodize for three different reasons — thermal (choke face), electrical (RF land), and contamination (channel interior). A single missed mask converts a controlled thermal choke into an unknown one.

## 9. Tolerances

**GD&T scheme:**

- **Primary datum A** — bottom face (seats on the Support Ring), flatness 0.015.
- **Datum B** — the Ø306 BC kinematic dowel at 60°.
- **Datum C** — the Ø306 BC kinematic dowel at 180° (clocking).

| Control | Feature | Tolerance |
|---|---|---|
| Flatness | Top face | 0.015 |
| Flatness | Bottom face (Datum A) | 0.015 |
| Parallelism | Top face to A | 0.015 |
| Profile | Choke pad set, coplanar | 0.010 |
| Position | Kinematic dowel bores | ⌖ Ø0.020 Ⓜ A B C |
| Position | Lift pin bores | ⌖ Ø0.050 Ⓜ A B C |
| Perpendicularity | Lift pin bores to A | 0.030 |
| Position | Choke fastener holes | ⌖ Ø0.200 Ⓜ A B C |
| Position | Central He bore | ⌖ Ø0.100 Ⓜ A B C |
| Profile | O-ring groove | 0.050 |
| Runout | OD to A | 0.20 |
| Thickness | 20.000 ±0.030 | Measured at 8 points, 45° apart, Ø280 BC |

**Tolerance philosophy:** only three characteristics on this part are tight — plate thickness, top-face flatness/parallelism, and kinematic dowel position. Everything else is opened deliberately. Choke fastener holes at ⌖ Ø0.200 and lift pin bores at ⌖ Ø0.050 are loose *by design*, because those features are located functionally (by Belleville-preloaded slip joints and by ESC-side bushings respectively), not by the plate.

## 10. Assembly Sequence

**Sub-assembly (off-tool) — corresponds to SEWCP-ENG-001 §10 steps A1–A2:**

1. Complete manufacture per §6 through step 16.
2. Record as-built thickness at 8 points; enter into the build traveller (feeds the Support Ring lap calculation, DR-3).
3. Press-fit the 6 alignment dowels (SEWCP-700): 3 into the bottom face at Ø306 BC, 3 into the top face at Ø260 BC. Verify protrusion 5.0 ± 0.1 mm each.
4. Install lift pin bushings (SEWCP-601) into the bottom counterbores; verify bore Ø5.60 +0.05/−0 after installation.
5. Install alumina liner tubes into the 2 HV feed bores; bond with vacuum-grade epoxy; verify IR > 1 GΩ.
6. Verify VCR stub cleanliness; cap.

**Installation into the stack — corresponds to §10 steps C2–C5:**

7. **Inverted, off-tool:** with the Cooling Plate bottom-face-up on a padded fixture, seat the Support Ring so the 3 bottom dowels enter its top-flange radial slots. **Confirm each dowel slides freely in its slot** — a bound locator means the slots are mis-clocked, and torquing will crack the ceramic on the first thermal cycle.
8. Install the 8× upper-circuit M6 × 16 bolts from beneath the Ring's top flange into the Cooling Plate tapped holes, with Ø16 washers and Belleville stacks. Torque in 3 passes (30 / 70 / 100%), star pattern, to **6.0 N·m**. Re-confirm free slide.
9. After the assembly has been inverted onto the Base Plate and the lower circuit torqued (Volume 03 §10 Phase 3), measure insulation resistance Cooling Plate → Base Plate: **≥ 1 GΩ at 1000 VDC**. A failure here means a cracked web or a conductive particle bridging it — stop and disassemble.
10. Place the thickness-sorted set of 16 titanium choke washers on their pads.
11. Proceed to Heater Plate installation (Volume 02).

**Disassembly note:** the Cooling Plate cannot be removed without first removing the Heater Plate + ESC sub-assembly, because its retaining bolts are captured beneath. This is accepted; the ESC is the life-limited item and is intended to be replaced as a bonded sub-assembly anyway.

## 11. Failure Modes

| # | Failure Mode | Cause | Effect | S | O | D | RPN | Mitigation |
|---|---|---|---|---|---|---|---|---|
| 1 | Coolant leak into vacuum | FSW defect, weld porosity, stub weld crack | **Catastrophic** chamber contamination, full teardown | 10 | 2 | 3 | **60** | FSW (no elastomer/filler), radiography, 6 bar proof, He leak test, burst sample per lot |
| 2 | Plate bow after machining | Residual stress in plate stock | Fails CP-08/09; wafer plane out of spec | 7 | 6 | 2 | **84** | Two stress-relief cycles (§6 steps 2, 8); final lap after anodize |
| 3 | Flow below turbulent threshold | Pump degradation, partial blockage, wrong fluid viscosity | Re drops < 2300, h collapses, CP-11 uniformity lost, local hot spot | 7 | 4 | 4 | **112** | Minimum-flow interlock at 2.5 L/min; ΔP monitoring; inlet strainer |
| 4 | Anodize flakes into coolant loop | Channel interior not masked | Heat exchanger fouling, progressive capacity loss | 6 | 4 | 6 | **144** | Explicit masking drawing; borescope inspection after anodize |
| 5 | Choke pad anodized in error | Masking error | R_choke unpredictable and high; wafer temperature uncontrollable | 7 | 3 | 5 | **105** | Masking drawing; post-anodize contact-resistance check on all 16 pads |
| 6 | RF land contact resistance rise | Anodize on land, low preload, oxidation, thermal cycling | I²R heating → arc → plate damage | 8 | 3 | 4 | **96** | Alodine only on land, 8 N·m preload, Belleville, 4-wire check in ATP |
| 7 | Lift pin bore galling / pin bind | Bore not honed, misalignment, particle ingress | Wafer handling fault, possible wafer breakage | 7 | 4 | 3 | **84** | Ra ≤ 0.8 honed bore, 0.030 perpendicularity, Vespel bushing |
| 8 | Corrosion / erosion of channel | Glycol degradation, galvanic pair with SS stubs, cavitation | Wall thinning → leak (→ FM #1) | 8 | 3 | 6 | **144** | Inhibited glycol, annual fluid analysis, R5 min bend radii to limit erosion, matched-potential stub design |
| 9 | Freeze burst | Chiller fault below fluid freeze point | Channel rupture | 9 | 2 | 3 | **54** | 50/50 glycol (−37 °C protection), low-temperature interlock |
| 10 | Virtual leak from RTD blind bores | Un-vented blind holes | Fails pump-down qualification | 5 | 5 | 6 | **150** | DR-6: cross-vent every blind bore |
| 11 | Thread stripping in M5/M6 tapped holes | Over-torque into aluminum | Loss of preload, joint separation | 6 | 3 | 3 | **54** | Torque schedule, min 2×D thread engagement, consider stainless inserts on rework |

**Highest-RPN items are 10 (virtual leaks), 4 and 8 (both coolant-loop contamination/corrosion), and 3 (loss of turbulence).** Note that the *catastrophic* failure (coolant into vacuum, S=10) has a modest RPN only because the manufacturing controls make occurrence low — which is exactly why FSW plus radiography plus proof plus leak test are all specified rather than any one of them.

## 12. Design Rationale

**Why a liquid-cooled plate rather than conduction to the Base Plate?**
Because the Base Plate is chamber-coupled and uncontrolled (FBA-7). Any architecture that relies on it for heat rejection makes wafer temperature a function of chamber wall temperature — which drifts with process history, chamber cleans, and idle time. A closed-loop liquid circuit makes the chuck's thermal boundary condition an *input* rather than a disturbance.

**Why is the coolant channel in the bottom face with an FSW lid, rather than the top face?**
Two reasons. First, the top face must be lapped flat to 15 µm and hold the choke pads coplanar to 10 µm — putting a weld seam there would make that impossible. Second, keeping the weld on the low-stress side, away from the wafer plane, means weld distortion is corrected by the final lap rather than propagating to the wafer.

**Why 10 × 8 mm channel at 4 L/min?**
The channel is sized backwards from the Reynolds number, not from pressure drop. At 4 L/min the velocity is 0.83 m/s and Re ≈ 7,400 — comfortably turbulent with margin for viscosity increase at low temperature. Sizing for a lower ΔP with a bigger channel would have dropped the flow laminar and cost far more in uniformity than it saved in pump power.

**Why is the plate the RF electrode instead of adding a dedicated one?**
Adding a separate electrode adds a joint, and every RF joint is a contact-resistance and arcing site. The Cooling Plate is already a large, low-impedance aluminum mass directly beneath the ESC dielectric — it *is* the natural electrode. The cost of this decision is that every service entering it needs an RF break (SEWCP-ENG-001 §6.5), which is a well-understood and bounded cost.

**Why deliberately leave the top face un-anodized?**
This is the least obvious decision on the part. Hard anodize raises emissivity from ~0.1 to ~0.8. Across the 1.5 mm choke gap at ΔT = 100 K, that changes radiative coupling from ~4 W to ~50 W — a parallel leak path that partially short-circuits the thermal choke and makes R_choke depend on temperature. Leaving the face bright preserves the choke as a nearly pure conduction element, which is what makes it predictable and tunable.

**Why are the choke fastener holes toleranced so loosely (⌖ Ø0.200)?**
Because they must be loose. The Heater Plate grows 0.4 mm radially relative to this plate across the operating range. Tight fastener holes would either over-constrain the joint (causing bow, FMEA #12 at assembly level) or shear the fasteners. The joint is located by the three kinematic dowels and clamped by Belleville stacks; the fastener holes only need to not interfere.

## 13. Why Semiconductor Tools Use This Design

- **Liquid-cooled aluminum pedestals are the industry standard** in plasma etch and PECVD chambers from Lam, Applied Materials, and ASM. The reasons are the ones above: process heat loads of 1–5 kW must be removed with wafer-temperature stability of ±1 °C, and only a forced-convection liquid loop has both the capacity and the stability to do it.

- **Welded or brazed monolithic channels, never gasketed lids.** In a production chamber, a coolant leak into vacuum is a multi-day recovery and can scrap the chamber's ceramic parts. Every serious chuck vendor eliminates elastomers from the coolant pressure boundary. Friction stir welding in particular became widespread for exactly this application because it joins 6061 at full strength without filler, flux, or a molten pool that could contaminate the channel.

- **The cooled-base / thermal-break / heater topology is how every modern temperature-controlled ESC works.** Whether the heater is a discrete plate (as here), co-fired into the ceramic, or brazed into the base, the architecture is the same: a cold sink at a controlled temperature, a defined thermal resistance, and a heater that trims upward. Tools that omit the thermal break cannot control wafer temperature — the sink simply wins.

- **The pedestal is the RF electrode.** In capacitively-coupled plasma tools the wafer pedestal is the powered (bias) electrode, floating on ceramic standoffs from the grounded chamber, with the ESC dielectric acting as the coupling capacitor. Everything about the mechanical design — the insulating support ring, the isolated fasteners, the line breaks on every utility — follows from that one electrical fact.

- **Anodize masking discipline is a real production practice.** Semiconductor chuck drawings routinely carry a dedicated masking sheet because anodize simultaneously helps (plasma durability, dielectric protection) and hurts (thermal contact, electrical contact, particle shedding). Knowing *where not to anodize* is a signature of someone who has actually built one.

## 14. Interview Talking Points

1. **"I sized the coolant channel from Reynolds number, not pressure drop."** At 4 L/min through a 10 × 8 mm channel, velocity is 0.83 m/s and Re ≈ 7,400 — turbulent with margin. A larger channel would have given a nicer ΔP and quietly dropped the flow laminar, collapsing the convective coefficient and losing the ±1.5 °C uniformity requirement. Turbulence is a design requirement on this part, which is why there's a minimum-flow interlock at 2.5 L/min.

2. **"The masking drawing is as important as the machining drawing."** Five surfaces on this plate are excluded from hard anodize for three different reasons: the choke face and pads because anodize would triple radiative coupling and make contact conductance unpredictable, the RF land because anodize is a dielectric and the joint has to carry 13.56 MHz at under 0.5 mΩ, and the channel interior because flaking anodize fouls the heat exchanger. One missed mask turns a designed thermal choke into an unknown one.

3. **"No elastomer in the coolant pressure boundary."** A friction-stir-welded lid costs more than an O-ring-sealed one. But an O-ring separating pressurized glycol from high vacuum, over 100 thermal cycles, is a catastrophic-severity failure with a slow-degradation mechanism — the worst combination. I moved that risk from an in-service seal to a one-time manufacturing operation that I can radiograph, proof, and leak-test before the part ever ships.

4. **"I toleranced three features tight and everything else loose — on purpose."** Plate thickness, top-face flatness, and kinematic dowel position are the only tight callouts, because those are the only features that propagate to the wafer plane or the chuck axis. The choke fastener holes are at ⌖ Ø0.200 because the Heater Plate moves 0.4 mm relative to this plate across the operating range — tight holes there would over-constrain the joint and bow the stack. Loose tolerances on that pattern aren't sloppiness, they're the constraint scheme.

5. **"Stress relief is called out twice and it isn't optional."** This is a 20 mm 6061 plate with a channel milled through most of its lower face. Machining it flat, then anodizing, then discovering 80 µm of bow at final inspection is the classic way to scrap the most expensive part in the stack. Rough machine, relieve, semi-finish, relieve, finish, and lap last — after anodize.

6. **"The routing of the coolant circuit is downstream of a wafer-quality decision."** Nothing penetrates the ESC top surface, so all 24 stack fasteners come from below, so the serpentine has to weave around a fixed fastener pattern. That's why the specification contains a keep-out table and instructs CAD to satisfy it before optimizing path length. Coupling like that has to be resolved at freeze; if you find it in CAD, you've already drawn the channel twice.

7. **"Loss of turbulence is a higher-probability failure than a leak."** People design chucks against the catastrophic case — coolant into vacuum — and control it well with welded construction and leak testing. The failure that actually bites you in the field is a partially blocked strainer or a degraded pump that drops flow to 2 L/min, goes transitional, and produces a slow, drifting wafer-uniformity problem that nobody attributes to the chiller for weeks. That's why flow and ΔP are interlocked and monitored, not just specified.

---

**END OF VOLUME 01**

*Next: Volume 02 — SEWCP-300 Heater Plate*
