# PVR-001 — Physical Verification Record and Test Matrix

> **Instance artifact.** Partition `project`. Owner `qa-engineer`. Mutability mutable.
> Opened `S-2026-08-11-06` by the release-readiness audit, under owner-delegated engineering
> authority. **This record contains no test result.** No hardware exists.

---

## 0 · The rule this record exists to enforce

> **Nothing here is marked PASS without physical evidence, and no measured value appears in this
> file that was not measured.**

Every row below is `NOT VERIFIED — HARDWARE REQUIRED` today. That is not a defect and not a
failure: it is the correct state of a design that has completed CAD and has not been built. The
purpose of this record is to make the boundary between *what the model has established* and
*what only hardware can establish* explicit, countable and impossible to blur.

**Status vocabulary — closed set.**

| Status | Meaning |
|---|---|
| `NOT VERIFIED — HARDWARE REQUIRED` | The declared method needs a physical article. No article exists |
| `MODEL-PREDICTED` | A model value exists and is recorded **as a prediction**. It is never a verification, whatever its margin |
| `DESK-DISCHARGEABLE` | The declared method is a drawing, a design statement or an analysis, and needs no article |
| `VERIFIED` | Physical evidence exists, is traceable, and meets the acceptance value. **Used nowhere in this file** |

## 1 · Census — derived from the frozen specification, not recalled

Parsed mechanically from the requirement tables of `spec/01`…`spec/09` at
`frozen_set_hash = 701db1fd…f618aa50`:

| | Count | |
|---|---|---|
| Numbered component requirements, nine volumes | **137** | `spec/01` 15 · `spec/02` 19 · `spec/03` 15 · `spec/04` 18 · `spec/05` 14 · `spec/06` 12 · `spec/07` 14 · `spec/08` 15 · `spec/09` 15 |
| **`DESK-DISCHARGEABLE`** | **46** | declared method is Design, Drawing, Analysis, Calculation, Derived, Material selection, or none |
| **Hardware required** | **91** | declared method needs a physical article. 46 + 91 = 137, and the two classes partition the set |
| — of which **hybrid** | **7** | declared method names both an instrument and an analysis. **Counted inside the 91**, because the instrument half still needs an article |
| **Verified by physical evidence today** | **0** | no article exists |

`spec/00` carries system-level interface and design rules rather than a numbered requirement
table; it is verified through `spec/00` §3.2 clearance (`python -m aief_clearance`) and the
component volumes.

## 2 · What the CAD baseline **does** establish — and its exact limit

The verified baseline at checkpoint `baf843a` establishes, by observation of the models:

| Established | Evidence |
|---|---|
| Every dimension, feature and interface of nine components | `cad/runs/` per-component run records; `LC-M04-EXIT` C1–C7 PASS |
| The twelve system interfaces close | `cad/runs/SYSTEM_INTERFACES.json` 12/12 |
| The Z stack closes at every station | `FINAL_SYSTEM_VERIFICATION.json` FSV-Z-* |
| Feature clearance against `spec/00` §3.2, pair by pair | `python -m aief_clearance` |
| Nineteen occurrences assemble without interference | `ASSEMBLY_S-2026-08-11-05` PASS |
| Model materials match the specification | FSV-MATERIALS, after `OI-CAD-01` |

**Its limit is absolute and worth stating plainly.** A model establishes *geometry and the
properties that follow from geometry and a material density*. It establishes **nothing** about
pressure drop, heat transfer coefficient, leak rate, temperature uniformity, contact resistance,
inductance, particle generation, outgassing, cycle life, dielectric strength or dechuck
behaviour. Ninety-one of the 137 requirements are of that second kind.

### 2.1 · The four mass rows are `MODEL-PREDICTED`, not verified

The declared method for all four is **Scale**. A scale needs a part.

| ID | Limit | Model | Margin | Status |
|---|---|---|---|---|
| `CP-15` | ≤ 4.2 kg | 3.9936 kg | −4.9 % | `MODEL-PREDICTED` |
| `HP-18` | ≤ 1.6 kg | 1.2338 kg | −22.9 % | `MODEL-PREDICTED` |
| `SR-15` | ≤ 0.8 kg | 0.5168 kg | −35.4 % | `MODEL-PREDICTED` |
| `EC-18` | ≤ 1.7 kg | 1.6196 kg | −4.7 % | `MODEL-PREDICTED` |

Every prediction is inside its limit. `EC-18` and `CP-15` sit within 5 % of theirs, so ordinary
machining tolerance and any added surface treatment mass are consumable margin, not comfortable
margin. Source: `cad/runs/ASSEMBLY_S-2026-08-11-05/run.json`, total 7.6997 kg over 19
occurrences.

---

## 3 · `CP-02` — Coolant flow rate at rated ΔP

> `spec/01` §2: **4.0 L/min at ΔP < 1.5 bar** · Verification: **Flow bench**

### 3.1 · What must be physically measured

| # | Measurement | Instrument | Acceptance |
|---|---|---|---|
| 1 | Volumetric flow through the assembled circuit, inlet stub to outlet stub | Calibrated turbine or Coriolis meter, ≤ ±1 % of reading | Set to **4.0 L/min** |
| 2 | Differential pressure across the same two ports at that flow | Two calibrated transducers or one ΔP cell, ≤ ±1 % FS, ports at the `CP-D` stub centrelines | **< 1.5 bar** |
| 3 | Fluid identity and temperature at the inlet | Per `CP-04` 50/50 water-glycol baseline; RTD at inlet | Recorded, not assumed — **ΔP is strongly temperature-dependent through viscosity** |
| 4 | Reynolds number, derived from 1 and 3 | — | **≥ 4000**, so the channel is turbulent as `spec/01` §2.1 requires. *"Turbulence is a requirement, not an outcome"* |
| 5 | ΔP at the `≈ 2.5 L/min` minimum-flow interlock point | as 1–2 | Records the interlock's operating margin |

The article must be the **FSW-closed plate**, not a machined open channel with a bolted lid: the
friction factor of the as-welded internal ribs and the lid-side surface is part of what is being
measured, and `spec/01` §6 step 5's FSW pass leaves a root profile no model predicts.

### 3.2 · What CAD evidence already establishes

Geometry, and only geometry: channel section **10.0 W × 6.0 D**, flow area 60 mm², perimeter
32.0 mm, hydraulic diameter **7.500 mm**, and the as-routed developed path **1.64 m**
(`MDR-001`, the routing authority). Mean velocity at 4.0 L/min is **1.111 m/s**, which is
arithmetic on the section, not a measurement of anything.

### 3.3 · What remains unverified — and the margin direction, corrected

**No ΔP value is asserted here.** `spec/01` states none, `ECR-D-002` forbids inventing one, and
this record does not.

What *is* derivable without a bench is the **ratio** between the as-built circuit and the sizing
basis `spec/01` §2.1 describes, because in a ratio the fluid properties and the friction-model
constant cancel — no temperature and no viscosity assumption enters. Darcy–Weisbach with a
Blasius friction factor:

| Term | Ratio | |
|---|---|---|
| **Section** — depth 8.0 → 6.0 (`ECR-D-002`) | **2.046** | **+105 %** — velocity rises 4/3, hydraulic diameter falls 8.889 → 7.500 mm |
| **Length** — 2.20 → 1.64 m (as-routed) | **0.745** | **−25 %** |
| **Net, as-built against the sizing basis** | **1.525** | **+53 %** |

> **Correction of record.** [`DECISIONS_S-2026-08-11-05`](../decisions/DECISIONS_S-2026-08-11-05.md)
> DEC-04 states *"ΔP **falls** roughly with length (−25 %), **increasing** CP-02 margin against
> the < 1.5 bar limit."* The −25 % is correct **for the length term in isolation** and is
> reproduced above. Read as a statement about `CP-02` margin it is **the wrong sign**: it omits
> the section term `ECR-D-002` introduced, which is +105 % and dominates. **`CP-02` margin
> decreased by roughly half again against the sizing basis; it did not increase.**
>
> `spec/01` — which governs — says the correct thing and always did: *"so ΔP rises materially …
> The hydraulic direction is adverse and is open. `CP-02` shall be verified before build
> release."* DEC-04's **conclusion** stands unchanged and was right: accept the 1.64 m routing,
> assert no ΔP value, keep `CP-02` as physical verification. Only its stated reason was wrong,
> and correcting it changes no geometry, no dimension and no disposition. Recorded as
> [`DECISIONS_S-2026-08-11-06`](../decisions/DECISIONS_S-2026-08-11-06.md) DEC-07.

**Consequence for the bench.** `CP-02` is the requirement most at risk in the whole
specification and should be scheduled **first**, on the first FSW-closed article, because it is
the only open item whose failure would force a change to the most expensive part in the stack.

### 3.4 · Does `CP-02` block anything today?

| | |
|---|---|
| Compiler **Stage 6** | **NO.** Stage 6's preconditions are the AMD-31 compile-time checks over the manifest and the Stage 1–5 tree. No `spec/**` requirement is among them |
| `LC-M04-EXIT` (the CAD gate) | **NO.** C1–C7 are ECR-disposition and freeze-registry criteria, computed by `python -m aief_gate` |
| **CAD release** | **NO.** The geometry is complete, verified and internally consistent |
| **Build release** | **YES.** `spec/01` §2.1: *"`CP-02` shall be verified before build release"* |
| **Final physical qualification** | **YES**, necessarily |

---

## 4 · `CP-11` — Radial temperature uniformity of the top face

> `spec/01` §2: **≤ 1.5 °C across Ø280 at 3 kW** · Verification: **Thermal map**

### 4.1 · What must be physically measured

| # | Measurement | Instrument | Acceptance |
|---|---|---|---|
| 1 | Top-face temperature field across Ø280 with 3 kW dissipated | Calibrated IR camera with a measured-emissivity reference, **or** a bonded thermocouple/RTD array of ≥ 9 radial stations at r = 0, 35, 70, 105, 140 mm on ≥ 3 azimuths | **max − min ≤ 1.5 °C** |
| 2 | Coolant flow and inlet temperature during the map | as `CP-02` §3.1 items 1 and 3 | 4.0 L/min at the `CP-03` range; **recorded, not assumed** |
| 3 | Applied thermal load | Calibrated resistive load or the `SEWCP-300` heater at measured power | **3.0 kW ± 2 %** |
| 4 | Azimuthal scan at the serpentine turn radii | as 1 | Detects the rib-shadow signature the serpentine produces; a radial-only scan can miss it |
| 5 | Steady state confirmed before recording | dT/dt at every station | < 0.05 K/min |

The map must be taken with the **as-routed** channel, because the requirement is about the
thermal footprint of a specific serpentine, and with the **coolant circuit at rated flow**,
because uniformity collapses below the turbulent threshold.

### 4.2 · What CAD evidence already establishes

The wetted geometry — path 1.64 m, perimeter 32.0 mm — and that the channel keeps its declared
keep-outs from every counterbore, locator, choke station and port. **Nothing thermal.** No
conjugate heat-transfer analysis has been run in this project, and none is claimed.

### 4.3 · What remains unverified — with a corrected derived quantity

`spec/01` §2.1's `h ≈ 6500 W/m²·K` is section-driven and unchanged by the routing. The wetted
area is not:

| | Wetted area | Film ΔT at 3 kW = Q/(h·A) |
|---|---|---|
| `spec/01` §2.1 as written | 0.080 m² | 5.77 K |
| **The same row, computed from its own stated geometry** | **0.0704 m²** (2.20 m × 32.0 mm) | 6.56 K |
| `DECISIONS_S-2026-08-11-05` DEC-04 | ≈ 0.060 m² | ≈ 7.7 K |
| **As-routed, from the governing routing** | **0.0525 m²** (1.64 m × 32.0 mm) | **8.79 K** |

> **Two arithmetic defects, both recorded, neither applied to the frozen specification.**
>
> 1. **`spec/01` §2.1's wetted-area row is stale after `ECR-D-002`.** It states 0.080 m², which
>    requires a perimeter of **36.4 mm**; the 10.0 × 6.0 channel has a perimeter of **32.0 mm**.
>    The row's own parenthetical — *"(perimeter 36 → 32 mm)"* — shows the change was known, and
>    the product was not recomputed. `ECR-D-002`'s disposition enumerated *"all nine derived
>    values recomputed"*; this was a tenth, and it was missed. Raised as **`ECR-Q-013`**.
> 2. **DEC-04 inherited it**, reaching ≈ 0.060 m² by scaling the stale 0.080 by the length ratio
>    0.745 rather than recomputing from the section. The as-routed value is **0.0525 m²**, and
>    the film ΔT the thermal map must confirm is **8.79 K — 14 % higher than DEC-04 recorded and
>    51 % higher than `spec/01` §2.1 implies.**
>
> **Neither is applied to `spec/**`, deliberately.** §2.1 is a *design-basis* table, not a
> numbered requirement — DEC-04 established that classification and it is not disturbed. The
> governing acceptance criteria are `CP-01` (calorimetric) and `CP-11` (thermal map), both
> physical, and neither takes its acceptance value from §2.1. Correcting a derived cell in a
> frozen volume would move `spec/01`'s digest, re-open its approval chain and its registration,
> and change no acceptance criterion. The `ECR-Q-010` precedent governs: **state the governing
> reading, record the correction, resolve at the next baseline correction.**

**None of this predicts failure of `CP-11`.** Film ΔT is not radial non-uniformity — the plate's
20 mm of 6061 is a strong isothermaliser and the requirement is on the *spread* across Ø280, not
on the absolute rise. What it does mean is that the thermal budget is **tighter than the
specification's own table suggests**, and that `CP-11` must be treated as a genuinely open
requirement rather than a formality. `ECR-D-011`'s residual — *"`HP-08` re-verified by thermal
map against the as-routed spiral — a measurement, not a waiver"* — is the same instruction for
the heater side and is unchanged.

### 4.4 · Does `CP-11` block anything today?

Identically to `CP-02` §3.4: **not Stage 6, not `LC-M04-EXIT`, not CAD release; yes for build
release and final physical qualification.** `CP-11` additionally gates `HP-08`'s companion map
and the `ECR-D-011` residual.

---

## 5 · The full matrix — 91 rows requiring hardware

`P` = physical article required. `H` = hybrid; the analysis half is dischargeable at the desk,
the instrument half is not. **Every row's status is `NOT VERIFIED — HARDWARE REQUIRED`.**

### `spec/01` SEWCP-200 Cooling Plate — 13

| ID | Requirement | Acceptance value | Declared method | Class |
|---|---|---|---|---|
| `CP-01` | Heat removal capacity | ≥ 3000 W | Calorimetric test | P |
| `CP-02` | Coolant flow rate at rated ΔP | 4.0 L/min at ΔP < 1.5 bar | Flow bench | P |
| `CP-05` | Proof pressure | 6.0 bar, 30 min, no permanent deformation | Hydrostatic | P |
| `CP-06` | Burst pressure | ≥ 15 bar | Sample test, 1 per lot | P |
| `CP-07` | Coolant circuit leak rate | < 1×10⁻⁹ mbar·L/s He | Mass spec | P |
| `CP-08` | Top face flatness | ≤ 0.015 mm TIR over Ø300 | CMM | P |
| `CP-09` | Top-to-bottom parallelism | ≤ 0.015 mm TIR | CMM | P |
| `CP-10` | Overall thickness | 20.000 ± 0.030 mm | Micrometer, 8 points | P |
| `CP-11` | Radial temperature uniformity of top face | ≤ 1.5 °C across Ø280 at 3 kW | Thermal map | P |
| `CP-12` | Electrical isolation from Base Plate (installed) | ≥ 1 GΩ at 1000 VDC | Megohmmeter | P |
| `CP-13` | RF strap contact resistance at land | ≤ 0.5 mΩ | 4-wire micro-ohmmeter | P |
| `CP-14` | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA | P |
| `CP-15` | Mass | ≤ 4.2 kg | Scale | P |

### `spec/02` SEWCP-300 Heater Plate — 16

| ID | Requirement | Acceptance value | Declared method | Class |
|---|---|---|---|---|
| `HP-01` | Total heater power | 2000 W at 208 VAC, 2 zones | Power measurement | P |
| `HP-02` | Inner zone (r = 0–75 mm) | 500 W ± 5%, R = 86.5 Ω ± 5% | 4-wire resistance | P |
| `HP-03` | Outer zone (r = 75–150 mm) | 1500 W ± 5%, R = 28.8 Ω ± 5% | 4-wire resistance | P |
| `HP-07` | Over-temperature trip | 175 °C, independent hardware thermostat | Functional test | P |
| `HP-08` | Top-face temperature uniformity | ≤ ±1.5 °C across Ø290 at 150 °C | Thermal map, instrumented | P |
| `HP-09` | Thermal ramp rate | ≥ 40 K/min at full power | Step response test | P |
| `HP-10` | Thermal time constant | 280 s ± 20% | Step response test | P |
| `HP-11` | Insulation resistance, element to sheath | > 100 MΩ at 500 VDC, hot and cold | Megohmmeter | P |
| `HP-12` | Hipot, element to sheath | 1500 VAC, 60 s, no breakdown | Hipot tester | P |
| `HP-13` | Bond face flatness | ≤ 0.015 mm TIR over Ø297 | CMM | P |
| `HP-14` | Choke face flatness | ≤ 0.015 mm TIR | CMM | P |
| `HP-15` | Overall thickness | 8.000 ± 0.020 mm | Micrometer, 8 points | P |
| `HP-16` | Choke thermal resistance (with SEWCP-301) | 0.100 ± 0.030 K/W | Calorimetric test | P |
| `HP-17` | Choke face emissivity | ≤ 0.15 | Witness coupon | P |
| `HP-18` | Mass (plate only) | ≤ 1.6 kg | Scale | P |
| `HP-19` | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA | P |

### `spec/03` SEWCP-400 Chuck Support Ring — 10

| ID | Requirement | Acceptance value | Declared method | Class |
|---|---|---|---|---|
| `SR-01` | Insulation resistance, Cooling Plate to Base Plate | ≥ 1 GΩ at 1000 VDC | Megohmmeter, installed | P |
| `SR-02` | Shunt impedance to ground at 13.56 MHz | ≥ 400 Ω | Network analyzer / calculation | H |
| `SR-05` | Thermal resistance, Cooling Plate to Base Plate | 0.20 ± 0.03 K/W | Calorimetric test | P |
| `SR-08` | Height, as supplied | 20.300 −0 / +0.050 mm | Micrometer | P |
| `SR-09` | Height, after assembly lap | Per DR-3 calculation, ±0.015 mm | CMM | P |
| `SR-10` | Top-to-bottom face parallelism, after lap | ≤ 0.010 mm TIR | CMM | P |
| `SR-11` | Bottom face flatness, after lap | ≤ 0.010 mm TIR | Optical flat / CMM | H |
| `SR-12` | Kinematic slot radial travel | ≥ ±1.0 mm | Gauge | P |
| `SR-14` | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA | P |
| `SR-15` | Mass | ≤ 0.8 kg | Scale | P |

### `spec/04` SEWCP-500 Electrostatic Chuck — 12

| ID | Requirement | Acceptance value | Declared method | Class |
|---|---|---|---|---|
| `EC-02` | Clamping voltage range | ±500 to ±2000 VDC | Functional | P |
| `EC-04` | Clamping pressure at ±1500 V | ≥ 38 mbar | Load-cell / pull test | P |
| `EC-07` | He leak with bare Si wafer clamped, 10 Torr | < 2.0 sccm | Flow measurement | P |
| `EC-09` | Wafer-to-chuck heat transfer coefficient at 10 Torr | ≥ 1200 W/m²·K | Calorimetric | P |
| `EC-10` | Surface flatness (mesa plane) | ≤ 0.010 mm TIR over Ø297 | Interferometer / CMM | H |
| `EC-11` | Dielectric hipot, electrode to chuck body | 3000 VDC, 60 s, ≤ 10 µA | Hipot | P |
| `EC-12` | Volume resistivity | > 1×10¹⁴ Ω·cm at 20 °C | Sample coupon | P |
| `EC-13` | Dechuck time to release | ≤ 2.0 s | Functional, 100 cycles | P |
| `EC-14` | Dechuck success rate | 100%, zero wafer-stick events in 100 cycles | ATP T17 | P |
| `EC-16` | Particle adders | ≤ 20 per wafer pass, ≥ 0.10 µm | Particle counter | P |
| `EC-17` | Puck thickness | 6.000 ± 0.020 mm | Micrometer | P |
| `EC-18` | Mass | ≤ 1.7 kg | Scale | P |

### `spec/05` SEWCP-600 Lift Pins — 9

| ID | Requirement | Acceptance value | Declared method | Class |
|---|---|---|---|---|
| `LP-02` | Travel above the mesa plane | 20.0 ± 0.2 mm | Dial indicator | P |
| `LP-03` | Tip position, full-down | 0.05 to 0.15 mm below the mesa plane | Height gauge | P |
| `LP-04` | Tip planarity, 3 pins, full-up | ≤ 0.10 mm | CMM / height gauge | H |
| `LP-05` | Perpendicularity to the mesa plane, over full travel | ≤ 0.05 mm | Indicator over travel | P |
| `LP-07` | He leak past all 3 pins at 10 Torr | < 0.5 sccm | Flow measurement | P |
| `LP-08` | Actuation force, per pin | ≤ 5 N (interlocked limit) | Load cell | P |
| `LP-11` | Particle adders attributable to pins | ≤ 5 per wafer pass, ≥ 0.10 µm | Particle test | P |
| `LP-12` | Cycle life | ≥ 500,000 cycles without fracture or wear-out | Endurance test | P |
| `LP-14` | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA | P |

### `spec/06` SEWCP-700 Alignment Pins — 5

| ID | Requirement | Acceptance value | Declared method | Class |
|---|---|---|---|---|
| `AP-02` | Centring accuracy per interface | ≤ 0.050 mm | CMM | P |
| `AP-03` | Centre stability over the full operating range | ≤ 0.020 mm | Thermal test / analysis | H |
| `AP-04` | Radial travel available | ≥ ±1.0 mm | Gauge | P |
| `AP-07` | Radial constraint force imposed | ≈ 0 (free sliding) | Free-slide check at assembly | P |
| `AP-12` | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA | P |

### `spec/07` SEWCP-800 Vacuum Port — 10

| ID | Requirement | Acceptance value | Declared method | Class |
|---|---|---|---|---|
| `VP-01` | Backside He pressure range | 5 to 20 Torr, regulated | Transducer | P |
| `VP-02` | He pressure control accuracy | ±0.5 Torr | Transducer | P |
| `VP-03` | Plenum evacuation | To chamber pressure in ≤ 3 s | Functional | P |
| `VP-04` | Orifice-limited flow at 20 Torr into vacuum | ≤ 150 sccm (choked) | Flow test | P |
| `VP-05` | Normal operating leak (wafer clamped, 10 Torr) | < 2.0 sccm total | Flow measurement | P |
| `VP-06` | Broken-wafer detection threshold | > 20 sccm sustained ⇒ abort | Functional | P |
| `VP-07` | External leak rate, port to chamber | < 1×10⁻⁹ mbar·L/s He | Mass spectrometer | P |
| `VP-08` | Proof pressure | 3.0 bar, 15 min | Hydrostatic / pneumatic | P |
| `VP-13` | Internal surface finish | Ra ≤ 0.4 µm, electropolished | Sample | P |
| `VP-14` | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA | P |

### `spec/08` SEWCP-900 RF Feedthrough Bracket — 8

| ID | Requirement | Acceptance value | Declared method | Class |
|---|---|---|---|---|
| `RF-04` | RMS current capability | ≥ 40 A | Analysis + thermal test | H |
| `RF-05` | Series inductance, feedthrough to electrode | ≤ 35 nH | Network analyser | P |
| `RF-06` | Inductance repeatability after service | ±5% | Network analyser, before/after | P |
| `RF-07` | Strap AC resistance | ≤ 3 mΩ | 4-wire at frequency / calculation | H |
| `RF-08` | Terminal joint contact resistance | ≤ 0.5 mΩ | 4-wire micro-ohmmeter | P |
| `RF-12` | Compliance travel, all axes | ≥ ±3 mm at ≤ 5 N reaction | Force gauge | P |
| `RF-14` | Maximum strap temperature rise at rated power | ≤ 20 K | Thermal test | P |
| `RF-15` | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA | P |

### `spec/09` SEWCP-1000 Temperature Sensor Bracket — 8

| ID | Requirement | Acceptance value | Declared method | Class |
|---|---|---|---|---|
| `TS-04` | Over-temperature protection | 1× independent hardware thermostat, trip 175 °C | Functional | P |
| `TS-05` | Sensor accuracy | Class A, ±0.45 °C at 150 °C | Calibration certificate | P |
| `TS-06` | Thermal response time (63%) | ≤ 5.0 s | Step response | P |
| `TS-07` | Probe contact preload | 5 to 10 N, maintained over life | Force gauge at assembly | P |
| `TS-10` | Insulation resistance, element to sheath | > 100 MΩ at 500 VDC | Megohmmeter | P |
| `TS-11` | RF-induced measurement error | ≤ 0.2 °C with 1000 W RF applied | Plasma-on comparison test | P |
| `TS-12` | Harness strain relief | ≥ 20 N pull without transmitting load to the probe | Pull test | P |
| `TS-14` | Outgassing | < 1×10⁻⁷ Torr·L/s·cm² at 150 °C | RGA | P |

---

## 6 · Two desk-dischargeable items that are **not** discharged

These carry a `DESK-DISCHARGEABLE` method — so no hardware blocks them — and the analysis has
nevertheless **not been performed at the as-built values**. They are actionable now.

### 6.1 · `SR-07` / `AP-08` — the design-basis stack mass is 2.66 % low

| | |
|---|---|
| `SR-07` | *Static load capacity — 7.5 kg stack + 5 g in all axes, SF ≥ 3* · **Analysis** |
| `AP-08` | *Lateral load capacity — 5 g on the 7.5 kg stack = 123 N per pin* · **Analysis** |
| As-modelled assembly mass | **7.6997 kg** (`ASSEMBLY_S-2026-08-11-05`, 19 occurrences) |
| Per-pin lateral load at 5 g, 3 pins, at 7.5 kg | 122.62 N — reproduces `AP-08`'s stated 123 N |
| Per-pin lateral load at 7.6997 kg | **125.89 N**, **+2.66 %** |

`ECR-D-007` records the locator stress margin as **4.4–6.9×**, which absorbs 2.66 % without
argument. **The item is not that the design fails — it is that the analysis of record was run
against a mass the design no longer has.** `SR-07` and `AP-08` are `Analysis`, so both should be
re-run at 7.6997 kg (plus the `SEWCP-903` hardware set and the unmodelled `spec-only` BOM lines,
which push it higher still) and the result recorded, before the analysis is offered as
verification. Recorded as **`OI-C-15`**.

### 6.2 · `SR-03` / `SR-04` / `RF-09` / `RF-10` / `RF-11` — creepage and clearance by drawing

Declared method is *Drawing* or *Drawing verification*, and the drawing set exists (11 documents,
`FSV-DRAWINGS` PASS with 79 fully-sourced dimensions). **No creepage/clearance path measurement
against those drawings has been recorded** — `python -m aief_clearance` checks `spec/00` §3.2
feature clearance, which is a different property from a dielectric creepage path over a solid
surface. These five are dischargeable from the existing drawings by a documented path trace, and
that trace has not been filed. Recorded as **`OI-C-15`** alongside 6.1.

---

## 7 · Blocking analysis — the whole set

| Gate | Blocked by physical verification? | Why |
|---|---|---|
| `LC-M04-EXIT` C1–C7 | **NO** | Criteria are ECR dispositions, freeze-registry reproduction and verification records. Computed by `python -m aief_gate`, exits 0 |
| Compiler **Stage 6** | **NO** | AMD-31 preconditions are `V-01`…`V-09`, `V-23`…`V-25` over the manifest and the Stage 1–5 tree. No `spec/**` requirement is among them |
| **CAD release** | **NO** | Geometry is complete and verified; the deliverable set is exported and digest-matched |
| **Repository release** | **NO** | The repository records the design and its provenance, not test results |
| **Build release** | **YES** — `CP-02` by name | `spec/01` §2.1: *"`CP-02` shall be verified before build release"* |
| **Final physical qualification** | **YES** — all 91 rows | By construction |

**No physical verification requirement is a blocker to anything this run can complete.** Every
one of them is a blocker to shipping hardware, and this record exists so that the distinction
cannot be lost.

---

## 8 · Findings raised by this record

| ID | Finding | Applied? |
|---|---|---|
| `ECR-Q-013` | `spec/01` §2.1's wetted-area row is stale after `ECR-D-002` — 0.080 m² implies perimeter 36.4 mm against the channel's actual 32.0 mm. Correct as-routed value 0.0525 m² | **No** — design-basis table, no acceptance criterion moves; `ECR-Q-010` precedent, resolve at the next baseline correction |
| DEC-07 | `DECISIONS_S-2026-08-11-05` DEC-04's `CP-02` margin sentence is the wrong sign at the system level | **Correction recorded**, not edited into the historical decision record |
| `OI-C-15` | `SR-07`/`AP-08` analyses of record run at 7.5 kg against an as-modelled 7.6997 kg; and the five creepage/clearance drawing traces are not filed | Open |

## 9 · Maintenance

This record's matrix is **derived from the frozen specification**, not transcribed. It is held
there by `tests/test_physical_verification_record.py`, which re-parses `spec/01`…`spec/09` and
fails if any requirement requiring hardware is missing from §5, if any row here names a
requirement the specification does not carry, or if any row in this file is ever marked
`VERIFIED` while this project holds no test evidence.
