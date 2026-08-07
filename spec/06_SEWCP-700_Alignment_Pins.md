# SEWCP-ENG-007 — Alignment Pins

**Part Number:** SEWCP-700 · **Volume:** 06 of 09 · **Revision:** A
**Parent:** SEWCP-ENG-001 Architecture & ICD
**Quantity:** 6 off (3 at the Support Ring interface, 3 at the Heater Plate interface)

---

## 0. Scope Clarification

"Alignment pins" in SEWCP means the **inter-plate locating features that establish the concentricity of the thermal stack**. They are not wafer-alignment features — wafer centring is performed by the robot, and wafer clocking (notch orientation) is handled upstream by an aligner. Both are outside SEWCP scope.

They are also **not conventional dowel pins.** They are **shouldered, screw-retained cylindrical locators engaging radial slots** — a pin-in-slot kinematic coupling. The reasons for both departures from the obvious solution are the substance of this volume.

## 1. Engineering Purpose

The alignment pins establish and maintain the **radial position of each plate in the thermal stack relative to the chuck axis**, while imposing essentially zero constraint force on the joints they locate.

That second clause is the entire design problem. The stack contains an alumina ring (CTE 7.2 ppm/K), two aluminium plates (23.6 ppm/K) that operate at temperatures up to 130 K apart, and an alumina puck. Across the operating range, adjacent members move relative to one another by **0.3 to 0.4 mm**. A conventional dowel scheme would fight that motion, and something would give — a sheared dowel, a bowed plate, a cracked ceramic ring, or a delaminated bond.

The alignment pins therefore have two jobs that are normally in conflict:

1. **Locate** — hold the chuck axis to within 0.05 mm at each interface, so the wafer sits concentric with the ESC.
2. **Release** — permit unrestricted radial growth, so no thermal stress is transmitted between plates.

The pin-in-radial-slot coupling does both, because it constrains the tangential direction while leaving the radial direction free.

## 2. Functional Requirements

| ID | Requirement | Value | Verification |
|---|---|---|---|
| AP-01 | Quantity and arrangement | 3 per interface, at 120°; 2 interfaces | Design |
| AP-02 | **Centring accuracy per interface** | ≤ 0.050 mm | CMM |
| AP-03 | **Centre stability over the full operating range** | ≤ 0.020 mm | Thermal test / analysis |
| AP-04 | Radial travel available | ≥ ±1.0 mm | Gauge |
| AP-05 | Radial travel required — Ring↔Cooling Plate | 0.326 mm (Al vs Al₂O₃, Ø306, ΔT 130 K) | Calculation |
| AP-06 | Radial travel required — Cooling↔Heater Plate | 0.399 mm (Al vs Al, Ø260, ΔT 130 K) | Calculation |
| AP-07 | Radial constraint force imposed | **≈ 0** (free sliding) | Free-slide check at assembly |
| AP-08 | Lateral load capacity | 5 g on the 7.5 kg stack = 123 N per pin | Analysis |
| AP-09 | Positive retention | Screw-retained; shall not migrate or fall out | Design |
| AP-10 | Serviceability | Field-replaceable without disturbing any bonded joint | Design |
| AP-11 | Maximum operating temperature | 200 °C | — |
| AP-12 | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA |

### 2.1 Required Travel Derivation

| Interface | BC | Materials | ΔT | Radial differential |
|---|---|---|---|---|
| Support Ring ↔ Cooling Plate | Ø306 | Al₂O₃ (7.2) vs 6061 (23.6) | 130 K | 153 × 16.4×10⁻⁶ × 130 = **0.326 mm** |
| Cooling Plate ↔ Heater Plate | Ø260 | 6061 vs 6061, **different temperatures** | 130 K | 130 × 23.6×10⁻⁶ × 130 = **0.399 mm** |

**Note the second row.** Both plates are the same alloy, so the instinct is that there is no CTE problem. There isn't — but there is a **temperature** problem. The thermal choke exists specifically to hold the Heater Plate up to 130 K above the Cooling Plate, so identical materials at different temperatures produce 0.4 mm of differential growth. This is the larger of the two cases and it is entirely a consequence of the deliberate thermal architecture.

The ±1.0 mm slot travel provides **3.1× margin** at the ring interface and **2.5× margin** at the heater interface.

### 2.2 Why Three Radial Slots, Quantified

| Scheme | Centre movement over ΔT = 130 K, ring interface | Verdict |
|---|---|---|
| **3 radial slots at 120° (selected)** | Plate expands symmetrically about the locator centroid → **≤ 0.020 mm**, set only by slot-clearance asymmetry | ✔ Meets AP-03 |
| Round dowel + diamond dowel | Fixed point is at the round dowel; growth accumulates entirely to one side → **0.163 mm** | 8× worse; fails AP-03 |
| Two rigid dowels | No release; 0.326 mm of interference → dowel shear or ceramic fracture | Fails structurally |
| Spigot / register diameter | Rigid; same failure as two dowels, plus it seizes | Fails structurally |

**The three-slot scheme is thermally self-centring.** Because the three constraint directions are tangential and symmetric, the plate grows radially about a fixed axis rather than about a fixed point. That is the single reason the concentricity budget (SEWCP-ENG-001 §5.4) closes.

### 2.3 Load Margins

| Load case | Value | Capability | Margin |
|---|---|---|---|
| Shear, 5 g lateral | 123 N over π/4 × 6² = 28.3 mm² = **4.3 MPa** | Ti-6Al-4V, 550 MPa shear | 128× |
| Bearing on slot wall | 123 N / (6.0 × 2.5) = **8.2 MPa** | Al₂O₃ 2,500 MPa; 6061 276 MPa | > 30× |

**The pins are not strength-driven.** Engagement depth is set at 2.50 mm — short by dowel standards — because it only needs to carry centring and handling loads, not fastener preload. Bolt preload is carried in friction at the joint faces, as it should be.

## 3. Mechanical Interfaces

| IF | Interface | Type | Detail |
|---|---|---|---|
| AP-IF-1 | Locator to Cooling Plate | **Located + retained** | Ø12.0 k6 flange in a Ø12.0 H7 × 3.0 counterbore (transition fit for position); M4 × 10 SHCS through the pin into the plate for retention |
| AP-IF-2 | Locator to Support Ring | **Pin-in-radial-slot** | Ø6.000 h6 boss, 2.50 mm protrusion, in a 6.05 H8 W × 8.0 L × 3.0 D radial slot at Ø306 BC (3 places, 60°/180°/300°) |
| AP-IF-3 | Locator to Heater Plate | **Pin-in-radial-slot** | Ø6.000 h6 boss, 2.50 mm protrusion, in a 6.05 H8 W × 8.0 L × 3.0 D radial slot at Ø260 BC (3 places, 30°/150°/270°) |

### 3.1 Installed Locations

| Set | Qty | Installed in | Face | BC | Clocking | Engages |
|---|---|---|---|---|---|---|
| A | 3 | Cooling Plate | Bottom | Ø306 | 60°, 180°, 300° | Support Ring top-flange slots |
| B | 3 | Cooling Plate | Top | Ø260 | 30°, 150°, 270° | Heater Plate bottom-face slots |

All six are the **same part number**. The Cooling Plate hosts every locator; the mating members carry only slots. This is deliberate — it concentrates the tight positional tolerance (⌖ Ø0.020) into one part on one machine setup, and makes the ring and heater plate cheaper.

### 3.2 Interfaces That Deliberately Have No Alignment Pins

| Interface | How it is located | Why no pins |
|---|---|---|
| Base Plate ↔ Support Ring | 8× M6 bolt clearance | The ceramic ring's own centration is non-critical. Functional centring happens at the ring's *top* face (AP-IF-2), and the ring is bolted to the Cooling Plate **first** (Volume 03 §10 Phase 1), so the pair self-aligns before it ever meets the Base Plate. Pressing dowels into ceramic is also an unnecessary fracture risk. |
| Heater Plate ↔ ESC | Bond fixture | A permanent bonded joint has no relative motion to constrain. Concentricity (0.060 mm) is set by the bonding fixture and is a one-time process control, not a running fit. |

### 3.3 Fit Stack

| Element | Value |
|---|---|
| Pin boss | Ø6.000 h6 (0 / −0.008) |
| Slot width | 6.05 H8 (+0.018 / 0) |
| Total diametral clearance | 0.050 to 0.076 mm |
| **Tangential centring error per pin** | **0.025 to 0.038 mm** ✔ within the 0.050 mm allocation (SEWCP-ENG-001 §5.4) |

## 4. Mating Components

| Mates To | Part No. | Interface | Nature |
|---|---|---|---|
| Cooling Plate | SEWCP-200 | AP-IF-1 | Host part for all 6 locators; screw-retained |
| Chuck Support Ring | SEWCP-400 | AP-IF-2 | 3 radial slots in the ceramic top flange |
| Heater Plate | SEWCP-300 | AP-IF-3 | 3 radial slots in the aluminium bottom face |
| Retaining screws | M4 × 10 SHCS, A4-70 | AP-IF-1 | 6 off, 2.5 N·m, with anti-galling dry film |

## 5. Critical Dimensions

| Ref | Dimension | Nominal | Tolerance | Criticality |
|---|---|---|---|---|
| AP-D01 | **Locating boss diameter** | **Ø6.000** | **h6 (−0 / −0.008)** | **Critical — centring** |
| AP-D02 | **Boss protrusion above the flange face** | **2.50** | **±0.05** | **Critical — must not bottom in the 3.0 mm slot** |
| AP-D03 | Flange diameter | Ø12.000 | k6 (+0.012 / +0.001) | **Critical — position transfer** |
| AP-D04 | Flange thickness | 3.000 | ±0.02 | **Critical — seats flush in the counterbore** |
| AP-D05 | Boss-to-flange fillet | R0.4 | +0.2 / −0 | High — stress riser |
| AP-D06 | Boss end chamfer | 0.5 × 30° | ±0.15 | High — lead-in during assembly |
| AP-D07 | Screw clearance bore | Ø4.3 | +0.1 / −0 | Low |
| AP-D08 | Counterbore for screw head | Ø8.0 × 2.2 | +0.1 / −0 | Low |
| AP-D09 | Boss-to-flange concentricity | — | 0.010 TIR | **Critical — position transfer** |
| AP-D10 | Boss perpendicularity to the flange face | — | 0.010 | **Critical — free sliding** |
| AP-D11 | Boss surface finish | Ra ≤ 0.4 µm | — | High — wear, stick-slip |
| AP-D12 | Overall length | 5.50 | ±0.05 | Medium |

### 5.1 Mating Slot Dimensions (specified in the host volumes, repeated here for control)

| Ref | Feature | Nominal | Tolerance | Host |
|---|---|---|---|---|
| — | Slot width | 6.05 | H8 | SEWCP-400 (SR-D17), SEWCP-300 (HP-D09) |
| — | Slot length, radial | 8.00 | +0.20 / −0 | SR-D18, HP-D10 |
| — | Slot depth | 3.00 | ±0.10 | SR-D19 |
| — | Slot position | Ø306 / Ø260 BC | ⌖ Ø0.030–0.050 Ⓜ | SR-D20, HP-D11 |
| — | Counterbore in Cooling Plate | Ø12.0 H7 × 3.0 | ⌖ Ø0.020 Ⓜ | CP-D09 / CP-D11 |

> **AP-D02 is the callout most likely to be got wrong.** A 2.50 mm boss into a 3.00 mm slot leaves 0.50 mm of bottom clearance. If the boss were made 3.0 mm "to match the slot depth," it would bottom out and hold the mating faces apart — destroying the thermal choke contact, the flatness budget, and the joint preload simultaneously. The boss must always be shorter than the slot is deep.

## 6. Manufacturing Method

**CNC turning from Ti-6Al-4V bar, with ground locating features.**

| Step | Operation | Notes |
|---|---|---|
| 1 | Procure Ti-6Al-4V Grade 5 bar, Ø14 | Certified |
| 2 | CNC turn the flange, boss, screw bore, and head counterbore in one chucking | Single setup is what holds AP-D09 concentricity |
| 3 | Part off and face to length | |
| 4 | **Grind the Ø6.000 h6 boss and the Ø12.000 k6 flange** | Ground, not turned — these are the two fits that carry the whole positional budget |
| 5 | Form the R0.4 fillet and the 0.5 × 30° lead-in chamfer | |
| 6 | Deburr thoroughly | Burrs at the boss root prevent flush flange seating |
| 7 | Apply anti-galling treatment to the flange OD | Titanium galls in press/transition fits |
| 8 | Passivate | |
| 9 | 100% inspect: boss diameter, flange diameter, concentricity, protrusion | |
| 10 | Ultrasonic clean, DI rinse, vacuum bake 200 °C / 4 h | |

**Design alternatives considered:**

| Approach | Verdict |
|---|---|
| **Screw-retained shoulder locator (selected)** | Positive retention independent of temperature; field-replaceable as a wear item; position set by a ground flange in a ground counterbore |
| Plain press-fit dowel | **Rejected on thermal grounds.** A Ti dowel in a 6061 hole loses 5.4 µm of interference over ΔT = 60 K (aluminium hole grows 8.5 µm, titanium pin 3.1 µm). Against a typical 10–20 µm interference band, the joint can approach zero interference hot — and a loose dowel in a vacuum chamber is a migrating hard particle. |
| Press-fit dowel in 316L | Loses only 2.7 µm, but 316L at ~150 HV wears rapidly against a 1,600 HV alumina slot |
| Integral machined boss on the Cooling Plate | Cheapest and eliminates a part, but not replaceable — a worn boss would scrap a 3.9 kg plate with a welded coolant circuit |
| Ceramic locator pin | Excellent wear pair, no galling; brittle in shear and unnecessary given the 128× margin |

## 7. Material

**Ti-6Al-4V Grade 5.**

| Property | Value | Relevance |
|---|---|---|
| CTE | 8.6 ppm/K | **Near-matched to Al₂O₃ (7.2) — the slot fit at the ring interface is nearly temperature-independent** |
| Thermal conductivity | 6.7 W/m·K | **Bonus:** 25× lower than aluminium, so the six locators add negligible parasitic conduction across the ring interface |
| Yield strength | 880 MPa | 128× shear margin |
| Hardness | ~350 HV | Adequate against alumina; harder than 316L |
| Magnetic permeability | ~1.0 (non-magnetic) | No field perturbation near the plasma |
| Galvanic couple with 6061 | Moderate; no liquid electrolyte present in vacuum | Acceptable |
| Vacuum compatibility | Excellent | — |

**Why titanium rather than the obvious hardened stainless.** Three reasons, in order of importance:

1. **CTE.** At 8.6 ppm/K it sits between alumina (7.2) and aluminium (23.6), and is nearly matched to the alumina slots it runs in. A 440C pin (10.3) or 17-4 PH (10.8) would be acceptable; austenitic 316L (16.0) would open the ring-interface fit by roughly 6 µm over the range.
2. **Thermal conductivity.** At 6.7 W/m·K the locators contribute almost nothing to the parasitic heat path across the Support Ring — a small but free win, and the same property that makes Ti the right choice for the thermal choke washers.
3. **Non-magnetic.** 440C and 17-4 PH are martensitic and magnetic. In a plasma tool, magnetic hardware near the wafer plane is avoidable and therefore avoided.

The cost is that titanium galls readily in interference fits, which is why the flange OD carries an anti-galling treatment and the retaining screws carry dry-film lubricant.

## 8. Surface Finish

| Surface | Finish | Reason |
|---|---|---|
| **Locating boss Ø6.000** | **Ground Ra ≤ 0.4 µm** | Slides against the slot wall through every thermal cycle; roughness causes stick-slip, which converts smooth thermal growth into a series of small jerks that load the ceramic |
| **Flange OD Ø12.000** | Ground Ra ≤ 0.8 µm, anti-galling treated | Transition fit; titanium galls without treatment |
| Flange seating face | Ra ≤ 0.8 µm, flat | Must seat flush; a proud flange lifts the joint |
| Boss lead-in chamfer | Ra ≤ 0.8 µm | Assembly lead-in |
| Boss-to-flange fillet | R0.4, blended | Stress riser control |
| Screw bore and counterbore | As-machined, deburred | Non-functional |

> **Stick-slip is the reason for the fine finish, not wear.** These pins slide perhaps a third of a millimetre per thermal cycle. That is far too little to wear out a ground titanium surface — but it is exactly the regime where static friction dominates and motion happens in discrete jumps. Each jump is an impulse into an alumina ring. A smooth, dry, low-friction pair converts thermal growth into continuous creep instead.

## 9. Tolerances

**GD&T scheme:** Datum A = flange seating face. Datum B = flange OD Ø12.000.

| Control | Feature | Tolerance |
|---|---|---|
| Concentricity | Boss Ø6.000 to Datum B | 0.010 TIR |
| Perpendicularity | Boss axis to Datum A | 0.010 |
| Flatness | Flange seating face (A) | 0.010 |
| Diameter | Boss | Ø6.000 h6 |
| Diameter | Flange | Ø12.000 k6 |
| Protrusion | 2.50 ±0.05 | — |

**Positional budget chain (per interface):**

| Contributor | Value (mm) |
|---|---|
| Cooling Plate counterbore position (⌖ Ø0.020) | 0.010 radial |
| Flange-in-counterbore transition fit | 0.006 |
| Boss-to-flange concentricity | 0.005 |
| Boss-in-slot tangential clearance | 0.038 |
| **RSS** | **0.041** ✔ within the 0.050 allocation |

Note that **the slot clearance dominates** at 0.038 mm. Tightening the pin's own tolerances further would buy almost nothing; if this budget ever needed to shrink, the correct lever is the slot width, not the pin.

## 10. Assembly Sequence

**Alignment pins are installed on the Cooling Plate during its sub-assembly, before any stack build.**

**Installation (Volume 01 §10 step 3):**

1. Verify the Ø12.0 H7 counterbore positions on the Cooling Plate by CMM before installing anything.
2. Clean each counterbore; confirm no burrs or chips.
3. Fit each locator flange into its counterbore. It is a transition fit — light tapping with a soft mallet is acceptable; a press is not required and must not be used.
4. **Verify the flange is fully seated and flush.** A locator standing proud by even 0.05 mm will hold the joint open.
5. Install the M4 × 10 retaining screw with anti-galling dry film; torque to **2.5 N·m**.
6. Verify boss protrusion above the plate face: **2.50 ± 0.05 mm** at each of the 6 locations.
7. Record positions on the build traveller.

**Verification during stack build (the checks that matter):**

8. **At the Support Ring interface (Volume 03 §10 step 4):** after seating the ring, confirm **all 3 bosses slide freely in their slots** before torquing anything.
9. **After torquing the ring bolts:** re-confirm free slide. Torque can pinch a slot.
10. **At the Heater Plate interface (Volume 02 §10 steps 12 and 14):** confirm free slide before and after torquing the 16 choke bolts.
11. Any bind at any of these four checks is a **stop condition.** Do not proceed, do not increase torque, and do not "work it in." A bound locator is a stress path into a ceramic ring, and it will find the ceramic on the first thermal cycle.

**Service:**

12. Locators are wear items. Inspect the boss OD at each major PM; replace the set if boss diameter falls below Ø5.980 or if any scoring is visible.
13. Replacement requires removing the thermal stack but **does not disturb the bonded ESC sub-assembly** — which is the reason for screw retention rather than a press fit.

## 11. Failure Modes

| # | Failure Mode | Cause | Effect | S | O | D | RPN | Mitigation |
|---|---|---|---|---|---|---|---|---|
| 1 | **Slot binds — over-constraint** | Slot too narrow, particle in the slot, boss burr, torque-induced pinching, corrosion | Thermal growth blocked → stress transmitted into the alumina ring or the ESC bond → **cracked ring or delaminated bond** | 9 | 4 | 4 | **144** | H8/h6 fit, ±1.0 mm travel (2.5–3× margin), Ra 0.4 ground boss, **four explicit free-slide checks** at assembly, stop-condition procedure |
| 2 | Boss bottoms in the slot | AP-D02 protrusion made equal to or greater than slot depth | Mating faces held apart → thermal choke contact lost, flatness lost, preload lost | 8 | 3 | 3 | **72** | 2.50 mm boss in a 3.00 mm slot (0.50 mm clearance); protrusion verified at 6 locations at installation |
| 3 | Locator loosens or migrates | Retaining screw backs out; press-fit alternative loses interference when hot | Loss of location; **loose hard particle inside a vacuum chamber** | 8 | 2 | 5 | **80** | Screw retention (temperature-independent, unlike a press fit); dry-film-lubricated screw at controlled torque; inspection at PM |
| 4 | Boss wear / scoring | Stick-slip against an alumina slot over thousands of cycles | Centring degrades; particles generated | 6 | 4 | 5 | **120** | Ground Ra 0.4 boss, near-matched CTE reduces sliding distance, Ti hardness, replaceable wear item, PM inspection with a wear limit |
| 5 | Galling on installation | Titanium flange in an aluminium counterbore | Locator cannot be removed without damaging the Cooling Plate counterbore | 7 | 3 | 3 | **63** | Anti-galling treatment on the flange OD; transition fit, not press; no press tooling permitted |
| 6 | Flange not fully seated | Burr or chip in the counterbore; installation error | Joint held open by 0.05 mm — corrupts the flatness and choke budgets | 7 | 3 | 2 | **42** | Counterbore cleaned and inspected; flush-seating verified; protrusion measured |
| 7 | Wrong clocking at assembly | Slots mis-oriented; locator installed on the wrong bolt circle | Slots not radial → travel unavailable → immediate over-constraint (→ FM #1) | 8 | 2 | 2 | **32** | Clocking map is binding (SEWCP-ENG-001 §3.2); asymmetric 120° pattern makes a wrong build obvious at first fit |
| 8 | Galvanic corrosion, Ti against 6061 | Moisture ingress during storage or a vent-to-atmosphere event | Seizure; loss of free slide | 5 | 2 | 5 | **50** | No liquid electrolyte in vacuum service; passivation; dry storage; PM inspection |

**FM #1 dominates at RPN 144, and its severity is not local.** A bound locator does not fail the pin — the pin is 128× overstrength. It transmits 0.3–0.4 mm of blocked thermal growth into the two most fragile items in the assembly: the alumina Support Ring and the ESC bond line. That is why the assembly procedure contains four separate free-slide verifications and a written stop condition, rather than a single check.

## 12. Design Rationale

**Why pin-in-slot rather than pin-in-hole.** A pin in a hole constrains two degrees of freedom; a pin in a radial slot constrains one. Three slots at 120° therefore constrain exactly the three in-plane degrees of freedom needed — two translations and one rotation — and nothing else. That is the definition of a properly constrained coupling, and it leaves radial growth completely free. A conventional dowel scheme over-constrains by three, and every one of those redundant constraints becomes a stress path when the temperature changes.

**Why three, and why radial.** Three is the minimum that determines a plane's in-plane position without redundancy. Radial orientation is what makes the scheme *thermally self-centring*: because all three constraint directions are tangential and symmetric about the axis, uniform radial growth produces no net force and no centre shift. Orient the same three slots tangentially and you would get a scheme that fixes the centre but constrains rotation redundantly — the opposite of what is needed.

**Why not round-pin-plus-diamond-pin, the standard tooling answer.** It is the right answer for a room-temperature fixture and the wrong one here. A round-and-diamond pair fixes a *point*, not an *axis*. The plate then grows away from that point, and the centre moves by half the total differential — 0.163 mm at the ring interface, against a 0.050 mm requirement. It fails by 3× on a requirement that the three-slot scheme meets with 2.5× margin.

**Why screw retention rather than a press fit.** A press fit's interference is temperature-dependent, and in exactly the wrong direction here: the aluminium host hole grows faster than the titanium pin, so interference is lowest when the tool is hot and vibrating. Against a typical 10–20 µm interference band, a 5.4 µm loss over 60 K is a significant fraction. A loose dowel in a vacuum chamber is a migrating hard particle above a wafer. A screw holds independently of temperature, and — equally important — makes the locator a **replaceable wear item**. An integral machined boss would have been cheaper until the first time one wore, at which point it would scrap a 3.9 kg plate with a welded coolant circuit inside it.

**Why titanium.** Its CTE of 8.6 ppm/K sits close to the alumina slots it runs in, so the ring-interface fit barely changes across the range. Its conductivity of 6.7 W/m·K means six locators add almost nothing to the parasitic heat path — the same property that makes titanium the right choice for the thermal choke washers, applied a second time. And it is non-magnetic, unlike the hardened martensitic stainlesses that would otherwise be the obvious pick.

**Why the surface finish is specified for stick-slip, not wear.** These pins slide about a third of a millimetre per thermal cycle. That will never wear out ground titanium. But it is precisely the regime where static friction dominates and motion happens in discrete jumps — and each jump is a small impulse delivered into an alumina ring. Ra 0.4 µm, dry, with a near-matched CTE pair, converts blocked-then-released motion into continuous creep.

**Why the Cooling Plate hosts every locator.** All six bosses are installed in one part, on one machine setup, holding one tight positional tolerance (⌖ Ø0.020). The Support Ring and Heater Plate carry only slots, which are toleranced an order of magnitude looser. Concentrating precision in the part that can most easily hold it — and which is already the datum-carrying member of the stack — is cheaper than distributing it across a ceramic vendor and two machine shops.

## 13. Why Semiconductor Tools Use This Design

- **Semi-kinematic mounting between dissimilar materials is standard practice** throughout semiconductor equipment: chucks, showerheads, focus rings, viewport assemblies, and every ceramic-to-metal structural interface. Wherever a part must stay concentric across a wide temperature range without transmitting stress, the answer is radial slots, flexures, or spherical seats — never a rigid register.

- **Ceramic components are never rigidly located against metal.** The material cannot yield to relieve an over-constraint; it fractures. Designs that survive in the field always provide an explicit release direction, and the assembly procedure always verifies it before torque is applied.

- **Slotted and floating fastener joints are ubiquitous in heated vacuum hardware** for the same reason. Any two members at different temperatures need somewhere to go, and if the designer does not provide it, the joint provides it as bowing, fretting, or fastener failure.

- **Locating features are treated as replaceable wear items** on production tools, because they slide, and because the parts they are installed in are expensive. Screw-retained locators, replaceable bushings, and bolted wear plates all reflect a design philosophy of putting the sacrificial element where it can be changed cheaply.

- **Loose hardware in a vacuum chamber is a serious event.** A migrated dowel is a hard particle above a wafer and a potential arcing site. Positive retention on anything that could work loose is standard, and it is why press fits alone are viewed with suspicion in thermally cycled vacuum assemblies.

## 14. Interview Talking Points

1. **"The two plates are the same alloy, and they still move 0.4 mm relative to each other."** People check CTE tables, see 6061 against 6061, and conclude there's no differential expansion problem. But the thermal choke exists specifically to hold the heater plate up to 130 K above the cooling plate — so identical materials at different temperatures give 0.4 mm of radial differential at the Ø260 bolt circle. It's the larger of my two cases, and it's created entirely by the thermal architecture I chose.

2. **"Round pin plus diamond pin is the standard answer and it fails here by three times."** That pair fixes a *point*, so the plate grows away from it and the centre moves by half the total differential — 0.163 mm at the ring interface against a 0.050 mm requirement. Three radial slots fix an *axis* instead: because the constraint directions are tangential and symmetric, uniform growth produces no net force and no centre shift. Same part count, 8× better centre stability.

3. **"Three slots constrain exactly three degrees of freedom — no more."** Two in-plane translations and one rotation, which is precisely what locating a plate requires. A conventional dowel scheme over-constrains by three, and every redundant constraint becomes a stress path the moment temperature changes. Getting the constraint count right is what lets me put a brittle alumina ring in a thermally cycled stack at all.

4. **"I rejected a press fit on thermal grounds, and the direction of the error is what matters."** An aluminium host hole grows faster than a titanium pin, so a press fit loses about 5.4 µm of interference over 60 K — meaning it's loosest when the tool is hot and vibrating. Against a 10–20 µm interference band that's a large fraction. A loose dowel in a vacuum chamber is a migrating hard particle above a wafer. A screw holds regardless of temperature and makes the locator replaceable, which matters because an integral boss would have been cheaper right up until the first one wore and scrapped a plate with a welded coolant circuit in it.

5. **"The finish callout is about stick-slip, not wear."** These pins slide a third of a millimetre per thermal cycle — that will never wear out ground titanium. But it's exactly the regime where static friction dominates and motion happens in jumps, and each jump is an impulse into an alumina ring. Ra 0.4 µm, dry, with a nearly CTE-matched pair, turns that into continuous creep. Specifying a finish for the friction regime rather than for the wear rate is the distinction.

6. **"My highest-RPN failure doesn't damage the pin at all."** The pin is 128× overstrength in shear. If a slot binds, what fails is the alumina Support Ring or the ESC bond line — the two most fragile items in the assembly — because 0.4 mm of blocked thermal growth has to go somewhere. That's why the procedure has four separate free-slide checks with a written stop condition, instead of one check at the end. The failure mode analysis pointed at a different part than the one I was designing.

7. **"One part hosts all six locators, and that's a cost decision."** Every boss is installed in the Cooling Plate, on one setup, holding one ⌖ Ø0.020 tolerance. The ceramic ring and the heater plate carry only slots, toleranced an order of magnitude looser. And when I looked at the positional budget, the slot clearance dominates at 0.038 of the 0.041 mm RSS — so tightening the pin further would buy nothing. If that budget ever needs to shrink, the lever is slot width, not pin tolerance.

8. **"The single most likely drawing error on this part is making the boss as deep as the slot."** A 2.50 mm boss in a 3.00 mm slot leaves half a millimetre of bottom clearance. Make them equal — which looks tidy and reads as correct — and the boss bottoms out, holds the mating faces apart, and simultaneously destroys the thermal choke contact, the flatness budget, and the joint preload. It's called out as critical with a verification step at all six locations for that reason.

---

**END OF VOLUME 06**

*Next: Volume 07 — SEWCP-800 Vacuum Port Assembly*
