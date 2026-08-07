# SEWCP-ENG-010 — Temperature Sensor Bracket

**Part Number:** SEWCP-1000 · **Volume:** 09 of 09 · **Revision:** A
**Parent:** SEWCP-ENG-001 Architecture & ICD
**Sub-parts:** SEWCP-1000 Probe Retainer (5 off) · SEWCP-1001 Harness Routing Bracket (1 off) · SEWCP-1002 Side-Load Clip (5 off) · SEWCP-1003 Fibre-Optic Probe Mount (1 off)

---

## 1. Engineering Purpose

Everything in the thermal architecture — the 3 kW coolant loop, the 0.10 K/W thermal choke, the two-zone heater — is a control system, and a control system is only as good as its feedback. These brackets hold that feedback in place.

Their jobs:

1. **Maintain repeatable thermal contact** between each temperature probe and the part it measures. Contact conductance, not sensor accuracy, dominates the measurement.
2. **Hold sensors at defined radial positions**, so the two-zone heater controller can see the radial profile it exists to correct.
3. **Preserve measurement integrity in an RF environment.** The Cooling Plate is a 13.56 MHz electrode. Any wire leaving it is an antenna, and any grounded sensor junction is a direct RF injection path into the controller.
4. **Strain-relieve and route the harness**, so the leads survive thermal cycling and never load the probe.
5. **Enable an independent safety channel.** The over-temperature trip must not depend on the same sensors, wiring, or controller as the closed-loop control.

> **The failure that this component exists to prevent is a probe that loses contact and reads low.** A heater controller responding to a falsely low reading drives *more* power into a part that is already hot. That is thermal runaway by instrumentation failure, and it is the reason for the preload requirement, the independent thermostat, and the RF immunity measures.

## 2. Functional Requirements

| ID | Requirement | Value | Verification |
|---|---|---|---|
| TS-01 | Cooling Plate sensors | 3× Pt100 Class A, 4-wire, at r = 40, 100, 140 mm | Design |
| TS-02 | Heater Plate zone sensors | 2× Pt100 Class A, 4-wire, at r = 45, 115 mm | Design |
| TS-03 | ESC / wafer-plane sensor | 1× fibre-optic (fluoroptic) probe | Design |
| TS-04 | Over-temperature protection | 1× independent hardware thermostat, trip 175 °C | Functional |
| TS-05 | Sensor accuracy | Class A: ±(0.15 + 0.002·\|t\|) °C → ±0.45 °C at 150 °C | Calibration certificate |
| TS-06 | **Thermal response time (63%)** | **≤ 5.0 s** | Step response |
| TS-07 | **Probe contact preload** | **5 to 10 N, maintained over life** | Force gauge at assembly |
| TS-08 | Measurement configuration | **4-wire**, all Pt100 channels | Design |
| TS-09 | **Sensor junction** | **Ungrounded (isolated from sheath)** | Sensor specification |
| TS-10 | Insulation resistance, element to sheath | > 100 MΩ at 500 VDC | Megohmmeter |
| TS-11 | RF-induced measurement error | ≤ 0.2 °C with 1000 W RF applied | Plasma-on comparison test |
| TS-12 | Harness strain relief | ≥ 20 N pull without transmitting load to the probe | Pull test |
| TS-13 | Serviceability | Probe replaceable without disturbing the thermal stack | Design |
| TS-14 | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA |
| TS-15 | Vacuum compatibility | All parts on the vacuum side of the Base Plate | Design |

### 2.1 Response Time — Why the Interface Is Grease-Free

Probe: Ø1.6 mm × 30 mm Inconel 600 MI sheath.
Thermal capacity: V = π/4 × (1.6×10⁻³)² × 0.030 = 6.03×10⁻⁸ m³ × 8,000 kg/m³ × 450 J/kg·K = **C ≈ 0.217 J/K**

| Interface method | Conductance G | τ = C/G | Verdict |
|---|---|---|---|
| **Bare probe in a Ø1.7 hole, air/vacuum gap** | 0.031 W/K | **6.9 s** | ✘ Fails TS-06 |
| **Spring side-load clip, metal-to-metal line contact (selected)** | 0.048 W/K | **4.5 s** | ✔ Meets TS-06 |
| Apiezon H vacuum grease in the annulus | 3.62 W/K | 0.06 s | ✔ Far exceeds — but outgasses |

**The bare, unpreloaded probe fails the response requirement.** That single result is why this component exists as a designed part rather than as "drop the probe in the hole."

**Baseline is the grease-free spring side-load clip.** The SEWCP-1002 clip forces the probe sheath against one wall of the bore along its full 12 mm engagement, converting a 0.05 mm vacuum gap into a high-pressure metal-to-metal line contact. It meets TS-06 with margin, adds nothing to the vacuum outgassing budget, and is serviceable.

**Apiezon H grease is listed as a qualified alternate**, giving a two-decade improvement in response, for applications where a small outgassing load in a blind hole is acceptable. It is **not** the baseline: every probe port opens into the chamber-vacuum volume between the Base Plate and the Cooling Plate, and a grease film there is a permanent, un-bakeable source term.

### 2.2 Why 4-Wire Measurement

Pt100 sensitivity is **0.385 Ω/°C**. Harness lead resistance over ~2 m of fine-gauge wire is roughly 0.1 Ω per conductor.

> 2-wire: 2 × 0.1 Ω = 0.2 Ω of lead resistance read as signal → **0.52 °C error**, drifting with harness temperature.

That error alone exceeds the ±0.45 °C Class A sensor accuracy — the wiring would be the dominant error term. Four-wire measurement drives current through one pair and senses voltage through the other, so lead resistance cancels entirely. **Specifying a Class A sensor and then wiring it 2-wire wastes the sensor.**

### 2.3 Sensor Placement — Why Three Different Radii

The heater is zoned **radially** (inner r = 0–75, outer r = 75–150), because heat loss from a disc is edge-dominated. A controller correcting a radial profile must be able to *see* a radial profile.

| Sensor | Radius | Purpose |
|---|---|---|
| Cooling Plate, r = 40 | Inner | Coolant inlet-side reference; inner-zone boundary condition |
| Cooling Plate, r = 100 | Mid | Mid-radius sink temperature |
| Cooling Plate, r = 140 | Outer | Edge sink temperature; detects flow degradation and edge loss |
| Heater Plate, r = 45 | Inner zone | **Inner zone closed-loop control** |
| Heater Plate, r = 115 | Outer zone | **Outer zone closed-loop control** |
| ESC / wafer plane (fibre-optic) | Central | Process reference; RF-immune |

Placing all sensors at one radius — the tidy, symmetric arrangement — would make the two-zone controller blind to the exact quantity it was built to control. **The instrumentation layout must mirror the control topology.**

### 2.4 RF Immunity — Three Independent Measures

| Measure | Reason |
|---|---|
| **Ungrounded sensor junction (TS-09)** | A grounded-junction probe bonds the sensing element to the sheath, which contacts the RF-hot Cooling Plate. That injects 13.56 MHz directly into the measurement leads. An ungrounded junction is galvanically isolated from the sheath — **this is the single most important sensor specification in the volume.** |
| **Shielded twisted pair, shield grounded at the controller end only** | Grounding a shield at both ends creates a loop that carries RF current and couples it into the signal pair. Single-point grounding breaks the loop. |
| **Common-mode ferrite chokes at the feedthrough** | Attenuates common-mode RF picked up along the harness run before it reaches the instrument. |
| **Fibre-optic probe for the wafer-plane measurement** | Not a mitigation but an elimination: a dielectric fibre carries no current and cannot couple to RF at all. |

## 3. Mechanical Interfaces

| IF | Interface | Type | Detail |
|---|---|---|---|
| TS-IF-1 | Retainer to Cooling Plate | Bolted | 2× M4 × 12 SHCS at ±9 mm flanking each blind port, 1.8 N·m; 3 locations at r = 40 @ 75°, r = 100 @ 165°, r = 140 @ 225° |
| TS-IF-2 | Retainer to Heater Plate | Bolted | 2× M4 × 10 SHCS flanking each blind port; 2 locations at r = 45 and r = 115, 195° |
| TS-IF-3 | Probe to blind bore | **Spring side-load** | Ø1.6 probe in Ø1.700 H8 × 12 deep bore; SEWCP-1002 clip provides 5–10 N lateral preload |
| TS-IF-4 | Probe axial retention | Spring plunger | Compression spring in the retainer body, 5–10 N axial, allowing thermal float |
| TS-IF-5 | Harness to routing bracket | Clamped, strain-relieved | SEWCP-1001 collects all 6 channels; P-clips at ≤ 100 mm intervals |
| TS-IF-6 | Fibre-optic probe to ESC region | Clipped mount | SEWCP-1003, non-contact or edge-mounted; **no metal within 10 mm of the ESC surface** |
| TS-IF-7 | Harness through the Base Plate | **Clearance only** | Via the central aperture, ≥ 2 mm radial clearance (DR-1); ferrite chokes at the feedthrough |

> **DR-13: Every temperature-sensor blind bore shall be cross-vented (DR-6), and the vent shall not be blocked by the retainer.** A Ø1.7 × 12 mm blind hole with a Ø1.6 probe in it is a near-perfect virtual leak — a 0.05 mm annulus 12 mm long, with essentially no pumping conductance. This is the highest-count trapped-volume feature in the assembly (5 off) and the most easily overlooked.

## 4. Mating Components

| Mates To | Part No. | Interface | Nature |
|---|---|---|---|
| Cooling Plate | SEWCP-200 | TS-IF-1, -3 | 3 probe ports; retainers bolt to the bottom face |
| Heater Plate | SEWCP-300 | TS-IF-2, -3 | 2 zone-control probe ports |
| Electrostatic Chuck | SEWCP-500 | TS-IF-6 | Fibre-optic probe views the wafer-plane region; no mechanical contact |
| Base Plate | SEWCP-100 | TS-IF-7 | **Harness clearance pass-through only** |
| Heater controller / instrument | External | — | 4-wire inputs, single-point shield ground |
| Safety interlock chain | External | — | Independent thermostat, hard-wired trip |

## 5. Critical Dimensions

### 5.1 SEWCP-1000 Probe Retainer (5 off)

| Ref | Dimension | Nominal | Tolerance | Criticality |
|---|---|---|---|---|
| TR-D01 | Body envelope | 24 × 16 × 12 | ±0.2 | Low |
| TR-D02 | **Probe bore** | **Ø1.75** | **+0.05 / −0** | High — probe guidance |
| TR-D03 | **Probe bore concentricity to the plate bore** | — | **0.10 TIR** | **Critical — probe must not be side-loaded at entry** |
| TR-D04 | Mounting hole spacing | 18.0 | ±0.1 | High |
| TR-D05 | **Spring plunger preload** | **7.5 N** | **±2.5 N** | **Critical — TS-07** |
| TR-D06 | Spring working travel | 2.0 min | — | **Critical — maintains preload through ΔT** |
| TR-D07 | Strain-relief clamp bore | Ø3.0 | +0.1 / −0 | Medium |
| TR-D08 | **Vent slot (clears the plate cross-vent)** | 2.0 W × 1.0 D | +0.2 / −0 | **Critical — DR-13** |

### 5.2 SEWCP-1002 Side-Load Clip (5 off)

| Ref | Dimension | Nominal | Tolerance | Criticality |
|---|---|---|---|---|
| SC-D01 | Material | Inconel 718, spring temper | — | **Critical — no relaxation at 150 °C** |
| SC-D02 | Free height | 2.30 | ±0.05 | **Critical — sets preload** |
| SC-D03 | Installed height (in a Ø1.70 bore on a Ø1.60 probe) | 2.05 | — | — |
| SC-D04 | **Lateral force at installed height** | **7.5 N** | **±2.5 N** | **Critical — TS-07, TS-06** |
| SC-D05 | Contact length | 10.0 | ±0.5 | High — conductance |
| SC-D06 | Thickness | 0.10 | ±0.01 | High |

### 5.3 Sensor Specifications

| Item | Specification |
|---|---|
| Pt100 probes (5 off) | Class A, **4-wire**, **ungrounded junction**, Ø1.6 mm × 30 mm, Inconel 600 sheath, MgO insulated, −50 to +250 °C |
| Fibre-optic probe (1 off) | Fluoroptic / phosphor-decay type, PTFE or polyimide-jacketed fibre, 0 to 200 °C, ±0.5 °C, **fully dielectric** |
| Over-temperature thermostat (1 off) | Bimetallic or thermistor type, **hard-wired**, normally closed, opens at 175 °C ±5 °C, **independent of the control system** |
| Harness | Shielded twisted pair per channel, PTFE-insulated, vacuum-rated, **shield grounded at the controller end only** |
| Ferrite chokes | Common-mode, one per channel, at the feedthrough |

## 6. Manufacturing Method

| Step | Operation | Notes |
|---|---|---|
| 1 | CNC machine SEWCP-1000 retainers from 6061-T6 bar | 5 identical parts, one setup |
| 2 | Ream the probe bore Ø1.75 | Concentricity to the mounting holes carries TR-D03 |
| 3 | Machine the vent slot | **Must clear the plate's cross-vent (DR-13)** |
| 4 | Deburr thoroughly | A burr in a Ø1.75 bore will score the probe sheath |
| 5 | **Alodine 1200 chromate conversion** | Conductive coating — the retainer is bolted to an RF-hot plate and should not float |
| 6 | Form SEWCP-1002 clips from 0.10 mm Inconel 718 sheet | Photo-etch or fine blank; no burrs |
| 7 | **Heat-treat clips to spring temper (precipitation age)** | Inconel 718 retains spring force at 150 °C indefinitely; spring steel and beryllium copper relax |
| 8 | **100% force-test each clip at installed height: 7.5 ± 2.5 N** | Preload is a functional characteristic, not a dimension |
| 9 | CNC machine SEWCP-1001 harness bracket; Alodine | |
| 10 | Assemble spring plungers into retainers; verify axial preload | |
| 11 | Clean all parts: ultrasonic, DI, IPA, vacuum bake 150 °C / 4 h | |
| 12 | Procure and calibration-certify all sensors | Class A certificates retained in the build package |

**Interface method alternatives considered:**

| Approach | Verdict |
|---|---|
| **Spring side-load clip, grease-free (selected)** | Meets 5 s response with no outgassing; serviceable; preload holds via Inconel spring temper |
| Apiezon H vacuum grease | 75× faster response; qualified alternate; rejected as baseline because every port opens into chamber vacuum |
| Press-fit probe | Excellent contact; **not serviceable** — a failed probe would require removing the thermal stack |
| Indium foil at the tip | Good conformable contact; melts at 156 °C against a 150 °C ceiling — **no margin** |
| Conical seated tip, spring-loaded | Elegant and grease-free, but the contact area is ~1 mm², giving τ ≈ 21 s — **fails TS-06** |
| Surface-mounted RTD with a clamp | Simplest; measures the clamp as much as the plate, and is exposed to RF |

## 7. Material

| Part | Material | Rationale |
|---|---|---|
| SEWCP-1000 Retainer | 6061-T6, Alodine 1200 | Light, machinable; conductive coating keeps it bonded to the RF-hot plate rather than floating |
| SEWCP-1001 Harness Bracket | 6061-T6, Alodine 1200 | Same |
| **SEWCP-1002 Side-Load Clip** | **Inconel 718, spring temper** | **Retains spring force at 150 °C for the life of the tool** |
| Probe sheath | Inconel 600 | Standard MI sheath; corrosion-resistant; matched to the clip material |
| Harness insulation | PTFE | Vacuum-rated, high-temperature, low outgassing |
| Fasteners | A4-70 with anti-galling dry film | DR-8 |

**Why Inconel 718 for the clip and not spring steel or beryllium copper.** The clip must hold 7.5 N continuously at up to 150 °C for years. Carbon spring steel corrodes and is unsuitable in vacuum. Beryllium copper is the usual instinct for a small spring contact — but it stress-relaxes significantly above about 120 °C, so its force would decay over months, the contact conductance would fall, the response time would lengthen, and the probe would begin reading low. **That is precisely the failure this component exists to prevent, arriving through the spring instead of the assembly.** Inconel 718 in the precipitation-aged condition holds its load at 150 °C indefinitely.

## 8. Surface Finish

| Surface | Finish | Reason |
|---|---|---|
| Retainer probe bore | Ra ≤ 0.8 µm, fully deburred | A burr scores the probe sheath during installation and creates particles |
| **Plate blind bore (host part)** | **Ra ≤ 0.8 µm** | Contact conductance depends on real contact area at the line contact |
| **Clip contact faces** | **Ra ≤ 0.4 µm, no burrs, edges radiused** | This surface *is* the thermal path — its finish sets the conductance that sets the response time |
| Retainer seating face | Ra ≤ 1.6 µm, flat | Even seating |
| All retainer surfaces | Alodine 1200 | Conductive; no floating metal near RF |
| Harness bracket | Alodine 1200, all edges radiused R1 min | Wire chafe protection |

> **The clip's contact faces are a thermal interface disguised as a spring.** They carry the entire measurement path, and the response-time budget in §2.1 assumes a clean, high-pressure metal-to-metal line contact. A burred or oxidised clip halves the conductance and doubles the time constant.

## 9. Tolerances

| Control | Feature | Tolerance |
|---|---|---|
| Position | Retainer probe bore to mounting holes | ⌖ Ø0.10 Ⓜ |
| Concentricity | Retainer bore to plate bore, installed | 0.10 TIR |
| Diameter | Retainer probe bore | Ø1.75 +0.05/−0 |
| **Force** | **Clip lateral load at installed height** | **7.5 ±2.5 N** |
| **Force** | **Retainer axial plunger preload** | **7.5 ±2.5 N** |
| Free height | Clip | 2.30 ±0.05 |
| Thickness | Clip | 0.10 ±0.01 |

**The two most important characteristics on this component are forces, not dimensions.** Both are 100% verified at manufacture and re-verified at assembly. Contact preload determines contact conductance, which determines response time and — through the loss-of-contact failure mode — whether the heater controller can be trusted at all. Toleranced dimensions on the retainer body are secondary and are opened accordingly.

## 10. Assembly Sequence

**Corresponds to SEWCP-ENG-001 §10 step D5 — installed last, after all utilities.**

1. Verify each blind bore: correct depth, Ra ≤ 0.8 µm, **cross-vent present and clear (DR-13)**, no chips.
2. Verify each probe's calibration certificate and, critically, that it is **ungrounded-junction** type. A grounded-junction probe fitted here will corrupt every reading under RF and is difficult to diagnose after the fact.
3. Measure probe insulation resistance: > 100 MΩ at 500 VDC.
4. Fit an SEWCP-1002 clip into each blind bore, oriented so the spring bears against the bore wall.
5. Insert the probe. **Verify insertion force is smooth** — a stepped or gritty feel means a burr or a mis-seated clip.
6. Fit the SEWCP-1000 retainer; align its bore concentric to the plate bore within 0.10 TIR before torquing.
7. Torque 2× M4 to **1.8 N·m**. **Verify the retainer vent slot lines up with the plate cross-vent.**
8. **Verify axial spring preload 5–10 N** with a force gauge at the probe tail.
9. Repeat for all 5 Pt100 locations.
10. Install the SEWCP-1003 fibre-optic probe mount. Verify no metal within 10 mm of the ESC surface.
11. Install the independent over-temperature thermostat on the Heater Plate. **Verify it is hard-wired into the interlock chain and not routed through the controller.**
12. Route the harness through SEWCP-1001, P-clipped at ≤ 100 mm intervals, with a service loop at each probe.
13. **Verify strain relief: 20 N pull on the harness transmits no load to the probe.**
14. Route through the Base Plate central aperture with ≥ 2 mm radial clearance.
15. Fit common-mode ferrite chokes at the feedthrough, one per channel.
16. **Confirm each shield is grounded at the controller end ONLY.** Verify no continuity from shield to chuck at the platform end.
17. Perform a 4-wire resistance check on all 5 channels; compare against ambient reference.
18. **Response test:** apply a heater step and verify τ₆₃ ≤ 5.0 s at each channel.
19. **RF immunity test:** compare readings with RF off and 1000 W RF on. Deviation ≤ 0.2 °C. A larger shift indicates a grounded junction, a double-grounded shield, or a missing choke.
20. **Functionally test the over-temperature trip** by simulated resistance injection.

## 11. Failure Modes

| # | Failure Mode | Cause | Effect | S | O | D | RPN | Mitigation |
|---|---|---|---|---|---|---|---|---|
| 1 | **Probe loses contact → reads low → heater thermal runaway** | Clip relaxation, spring set, probe backed out, harness pulled | Controller drives more power into an already-hot part; **ESC bond over-temperature, possible dielectric damage** | 9 | 3 | **6** | **162** | Inconel 718 spring temper (no relaxation at 150 °C), 5–10 N preload verified, strain relief, **independent hardware over-temperature trip at 175 °C** |
| 2 | **RF pickup corrupts readings** | Grounded-junction probe, shield grounded at both ends, missing ferrite | Erratic control, oscillation, possible instrument damage; often misdiagnosed as a process problem for weeks | 7 | 4 | 6 | **168** | Ungrounded junction (TS-09), single-point shield ground, ferrite chokes, **RF-on/RF-off comparison test in the ATP** |
| 3 | **Virtual leak from probe bores** | Cross-vent missing, blocked by the retainer, or omitted in CAD | Fails pump-down qualification; **5 instances, the highest count of any trapped-volume feature** | 5 | 5 | 6 | **150** | DR-6 and **DR-13**; retainer vent slot; vent alignment verified at installation step 7 |
| 4 | Slow response from poor contact | Burred bore, oxidised clip, clip mis-seated, low preload | Control loop sluggish; overshoot; poor uniformity during ramps | 6 | 4 | 4 | **96** | Ra 0.8 bore / Ra 0.4 clip, smooth-insertion check, τ₆₃ verified per channel in the ATP |
| 5 | Wrong probe type fitted at service | Grounded-junction or 2-wire probe substituted | Reintroduces FM #2 or a 0.5 °C lead-resistance offset | 7 | 4 | 5 | **140** | Probe type stated on the drawing and in the service procedure; RF-on/off check mandated after any probe replacement |
| 6 | Over-temperature trip routed through the controller | Wiring error; "simplification" during commissioning | **The safety channel shares a failure mode with the control channel it protects** | 10 | 2 | 4 | **80** | Hard-wired requirement; verified independently at step 11; functional trip test at step 20 |
| 7 | Harness fatigue / chafe | Insufficient service loop, no P-clips, sharp bracket edges | Open or intermittent channel; controller fault | 6 | 3 | 3 | **54** | Service loop at each probe, P-clips ≤ 100 mm, all bracket edges R1 minimum, PTFE insulation |
| 8 | Probe sheath scored on installation | Burr in the retainer or plate bore | Particles; degraded contact | 5 | 3 | 3 | **45** | Thorough deburring, smooth-insertion check |
| 9 | Sensors all placed at one radius | Layout "tidied" during CAD | Two-zone controller blind to the radial profile it controls | 7 | 2 | 3 | **42** | Radial positions specified with rationale (§2.3); clocking map is binding |
| 10 | Grease used in a grease-free design | Assembler substitutes thermal compound to "improve" contact | Permanent outgassing source in chamber vacuum | 5 | 3 | 5 | **75** | Baseline stated as grease-free; Apiezon H is the *only* approved alternate, and only where authorised |

**The top three RPNs — RF pickup (168), loss of contact (162), and virtual leaks (150) — all have detection ratings of 6.** None fails visibly at installation. A probe reading two degrees low, a channel with RF riding on it, and a blind hole that will not pump down all look identical to a working assembly on a bench. That is why this volume's acceptance tests are functional (response time, RF-on/RF-off comparison, trip test) rather than dimensional, and why FM #1's mitigation of last resort is a hardware thermostat that shares nothing with the control loop.

## 12. Design Rationale

**Why this is a designed component and not a hole with a probe in it.** A bare probe in a Ø1.7 bore has a 6.9 s time constant and fails the response requirement outright. The entire component exists to convert a 0.05 mm vacuum gap into a metal-to-metal contact. Once that is recognised, the clip's spring force becomes the governing specification and everything else — bore finish, deburring, spring material — follows from it.

**Why grease-free is the baseline despite being 75× slower.** Apiezon H would give a 0.06 s response instead of 4.5 s. But every probe port opens into the chamber-vacuum volume between the Base Plate and Cooling Plate, and a grease film there is a permanent, un-bakeable source term in a 10⁻⁶ Torr system. The grease-free clip meets the requirement with margin, so the extra performance buys nothing and costs vacuum integrity. Grease is retained as a qualified alternate, not as a default.

**Why Inconel 718 and not beryllium copper.** The clip must hold 7.5 N at 150 °C for years. BeCu is the reflexive choice for a small spring contact, and it stress-relaxes above roughly 120 °C. Its force would decay over months; contact conductance would fall; response would lengthen; and the probe would begin reading low — which is FM #1, the failure the whole component exists to prevent, arriving through the spring instead of the assembly. Inconel 718 in the aged condition does not relax at this temperature.

**Why the ungrounded junction matters more than the sensor class.** A grounded-junction probe bonds its sensing element to a sheath that is in intimate contact with a 13.56 MHz electrode. That is a direct RF injection path into the instrument, and it produces readings that are wrong in a way that looks like process variation. A Class A sensor with a grounded junction under RF is less useful than a Class B sensor with an isolated one. **Junction type is the first specification to check on any sensor going into RF hardware.**

**Why the over-temperature trip is hard-wired and independent.** The control channel and the safety channel must not share a failure mode. If the trip ran through the same controller reading the same sensors, then FM #1 — a probe reading low — would disable the protection at exactly the moment it was needed, because the controller would see a comfortable temperature while the part cooked. An independent thermostat with its own sensing element and its own wiring is the only arrangement that breaks that coupling.

**Why sensor radii mirror the heater zones.** The two-zone heater exists because heat loss from a disc is edge-dominated and the radial profile needs correcting. A controller can only correct what it can observe. Sensors at r = 45 and r = 115 in the Heater Plate give each zone its own feedback; three Cooling Plate sensors across r = 40 to 140 characterise the sink profile and provide early warning of coolant flow degradation, which shows up first as a rising outer-radius reading.

**Why forces are toleranced and dimensions are not.** The two characteristics that determine whether this component works — clip lateral load and plunger axial preload — are both forces, both 100% tested at manufacture, and both re-verified at assembly. The retainer body's dimensions are opened up because nothing about them is functionally critical. It is worth stating explicitly, because a drawing full of tight linear tolerances and a loose note about "spring force approx. 7 N" would be exactly backwards.

**Why the probe ports were re-clocked.** The original layout placed a probe at r = 140, 105° — which collided with the RF land after that feature was widened and relocated to accommodate the strap geometry. The probes moved rather than the RF land, because probe radial position is the functional requirement and probe *angular* position is arbitrary. Knowing which coordinate of a feature is functional and which is free is what makes late-stage layout conflicts cheap to resolve.

## 13. Why Semiconductor Tools Use This Design

- **Multi-point, multi-radius temperature instrumentation is standard on production pedestals.** Zoned heaters require zoned feedback, and tools with many heater zones carry correspondingly many sensors. The instrumentation layout always mirrors the control topology.

- **Ungrounded-junction sensors are the norm in RF process chambers**, for the reason given above. It is one of the standard specification items on any thermocouple or RTD going into a plasma tool, alongside sheath material and dimensions.

- **Fluoroptic (fibre-optic) probes exist because of this exact problem.** They were developed for measurements in strong RF and microwave fields where any metallic sensor either perturbs the field or picks up power from it. Their use in electrostatic chucks and RF-biased pedestals is routine, and they are the standard tool for wafer-plane and ceramic-surface temperature measurement with plasma on.

- **Independent hardware over-temperature protection is a safety requirement, not an option.** Interlock chains in semiconductor equipment are built so that safety functions do not depend on the control system, and thermal protection on heated chucks is a canonical example — a runaway heater can destroy a chuck, contaminate a chamber, and start a fire.

- **Spring-loaded probes in blind wells** are the standard way to instrument a metal body: they give repeatable contact, tolerate differential expansion, and are serviceable. Press-fitting or bonding a probe into an expensive plate is done only where serviceability genuinely does not matter.

- **Backside gas flow, coolant ΔP, and multi-radius plate temperatures are all treated as diagnostic signals**, not just control inputs. A slow drift in the outer-radius sink temperature is one of the earliest indicators of coolant flow degradation — often visible long before the wafer-level uniformity specification is breached.

## 14. Interview Talking Points

1. **"A probe dropped in a hole fails the response requirement, and that's why this part exists."** A Ø1.6 mm probe in a Ø1.7 mm bore with a vacuum gap has a 6.9 second time constant against a 5 second requirement. The whole component is a mechanism for converting a 0.05 mm gap into a metal-to-metal line contact, which brings it to 4.5 seconds. Once you frame it that way, the spring force becomes the governing specification and the bore finish becomes a thermal characteristic rather than a cosmetic one.

2. **"I chose the 75× slower interface on purpose."** Apiezon H grease would give 0.06 seconds instead of 4.5. But every probe port opens into chamber vacuum, and a grease film there is a permanent, un-bakeable source term at 10⁻⁶ Torr. The grease-free clip meets the requirement with margin, so the extra performance buys nothing and costs vacuum integrity. Grease stays on the drawing as a qualified alternate — not as the default.

3. **"Beryllium copper would have failed slowly, in exactly the way the part exists to prevent."** BeCu is the reflex choice for a small spring contact, and it stress-relaxes above about 120 °C. Its force would decay over months; contact conductance falls; response lengthens; the probe starts reading low — and a heater controller responding to a low reading drives *more* power into an already-hot part. That's thermal runaway arriving through the spring material. Inconel 718 in the aged condition holds its load at 150 °C indefinitely.

4. **"Junction type matters more than sensor class in RF hardware."** A grounded-junction probe bonds its sensing element to a sheath that's in intimate contact with a 13.56 MHz electrode — a direct injection path into the instrument, producing errors that look exactly like process variation. A Class A sensor with a grounded junction is less useful under RF than a Class B sensor with an isolated one. It's the first thing I check on any sensor specification going into a plasma tool.

5. **"The safety channel shares nothing with the control channel."** If the over-temperature trip ran through the same controller reading the same probes, then a probe reading low would disable the protection at precisely the moment it was needed — the controller would see a comfortable temperature while the part cooked. An independent hard-wired thermostat with its own sensing element is the only arrangement that breaks that coupling, and it's the mitigation of last resort for my highest-severity failure mode.

6. **"Specifying a Class A sensor and wiring it two-wire throws the sensor away."** Pt100 sensitivity is 0.385 Ω/°C, and two metres of harness gives about 0.2 Ω of lead resistance — a 0.52 °C offset that drifts with harness temperature. That's larger than the ±0.45 °C sensor accuracy I paid for, so the wiring would be the dominant error term. Four-wire cancels it entirely.

7. **"The two most important characteristics on this drawing are forces, not dimensions."** Clip lateral load and plunger axial preload are both 7.5 ±2.5 N, both 100% tested at manufacture, both re-verified at assembly. The retainer body tolerances are deliberately open because nothing about them is functionally critical. A drawing covered in tight linear tolerances with a casual note about "spring force approx. 7 N" would have the priorities exactly inverted.

8. **"My three highest risks all have a detection rating of six."** RF pickup, loss of probe contact, and virtual leaks from five blind bores. None of them fails visibly at installation — a probe reading two degrees low looks identical to a working one. So acceptance for this component is entirely functional: a response-time measurement per channel, an RF-on versus RF-off comparison, and a live trip test. When you can't inspect the failure, you have to test the function.

9. **"When the RF land moved, I moved the sensors, not the land."** Widening the RF strap forced the land to a new position that collided with a probe port. Probe *radial* position is a functional requirement — it has to mirror the heater zones so the controller can see the profile it's correcting. Probe *angular* position is completely arbitrary. Knowing which coordinate of a feature carries the requirement and which is free is what makes a late layout conflict a five-minute fix instead of a redesign.

---

**END OF VOLUME 09 — SPECIFICATION SET COMPLETE**
