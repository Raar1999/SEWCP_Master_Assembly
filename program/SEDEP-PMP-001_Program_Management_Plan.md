# SEDEP-PMP-001 — Program Management Plan

**Program:** SEDEP — Semiconductor Equipment Digital Engineering Platform
**Product Baseline:** SEWCP Engineering Specification Set, Rev A (Vol 00–09) — **FROZEN**
**Plan Revision:** 1.0
**Issued:** 2026-08-07
**Program Start:** 2026-08-10 (W1)
**Program Finish:** 2026-12-11 (W18)
**Prepared by:** Chief Engineering Program Manager

---

## 0. Basis of Plan

### 0.1 Configuration Control Statement

> **The SEWCP engineering specification is frozen at Rev A.** This plan converts that baseline into executed engineering artefacts. **No task in this plan authorises a design change.** Any discrepancy discovered during execution shall be raised as an **Engineering Change Request (ECR)** against SEDEP-PMP-002 §5 change control and dispositioned by the Design Authority. It shall not be resolved at the workstation.

Three classes of finding are anticipated and pre-dispositioned:

| Finding class | Disposition | Authority |
|---|---|---|
| **Modelling clarification** — spec is unambiguous, CAD needs a construction decision | Record in the Engineering Notebook; proceed | Lead Engineer |
| **Specification ambiguity** — two readings possible, both spec-compliant | Raise ECR-Q (query); Design Authority rules; RTM updated | Design Authority |
| **Specification defect** — geometry cannot be built as dimensioned | **STOP the affected task.** Raise ECR-D (defect). Gate review required before rework | Design Authority + Gate |

### 0.2 Resourcing Model

| Role | Code | Scope |
|---|---|---|
| Chief Engineering Program Manager | **PM** | Plan, gates, risk, dashboard, change control |
| Lead Design Engineer | **LE** | Modelling, drawings, execution |
| Design Authority | **DA** | Gate approval, ECR disposition, technical sign-off |
| Analysis Engineer | **AN** | Tolerance, thermal, structural, RF verification |
| Drawing Checker | **CK** | Independent drawing check (shall not be the originator) |
| Configuration Manager | **CM** | Repository, baselines, release control |

> **Baseline execution model:** all roles are discharged by the Lead Engineer except **DA** and **CK**, which are performed by an independent reviewer at each gate. Role separation is retained in the plan because gate criteria must remain objective, and because the plan must scale to a team without restructuring. **A drawing shall never be checked by its originator** — this is the one role separation that is not negotiable.

### 0.3 Effort and Schedule Basis

| Quantity | Value |
|---|---|
| Total estimated effort | **280 engineering hours** |
| Calendar duration | **18 weeks** (2026-08-10 → 2026-12-11) |
| Assumed availability | 15.6 h/week |
| Schedule reserve held at program level | 12% (34 h), unallocated |
| Estimating basis | Analogous, from the Rev A specification content: 10 released parts, 4 sub-assemblies, 1 master assembly, 12 drawings, 6 analysis reports |

Effort by phase:

| Phase | Title | Hours | % | Weeks |
|---|---|---|---|---|
| P0 | Program Setup & Baseline Control | 16 | 6% | W1 |
| P1 | Digital Engineering Foundation | 46 | 16% | W2–W4 |
| P2 | Part Modelling — Detailed Design Execution | 78 | 28% | W4–W10 |
| P3 | Assembly Integration & Digital Mock-Up | 30 | 11% | W10–W12 |
| P4 | Engineering Analysis & Verification | 44 | 16% | W11–W14 |
| P5 | Drawing & Documentation Release | 36 | 13% | W13–W16 |
| P6 | Manufacturing Readiness | 12 | 4% | W16–W17 |
| P7 | Program Closeout & Portfolio Release | 18 | 6% | W17–W18 |
| — | **Total** | **280** | **100%** | **18** |

---

## 1. Phase Structure

| Phase | Entry Criterion | Exit Gate | Governing Question |
|---|---|---|---|
| **P0** Program Setup & Baseline Control | Rev A spec issued | **G0 — Baseline Freeze Review** | Is the baseline under configuration control and fully traced? |
| **P1** Digital Engineering Foundation | G0 passed | **G1 — Digital Foundation Review** | Can the parameter master and validators reproduce every number in the spec? |
| **P2** Part Modelling | G1 passed | **G2 — Model Design Review** | Does every solid model match its released dimensions? |
| **P3** Assembly Integration | G2 passed | **G3 — Critical Design Review** | Do the parts assemble, and do all interfaces close? |
| **P4** Analysis & Verification | G2 passed (P4 overlaps P3) | **G4 — Analysis Verification Review** | Does analysis confirm the budgets the spec asserts? |
| **P5** Drawing & Documentation Release | G3 + G4 passed | **G5 — Drawing Release Review** | Is the drawing set manufacturable and independently checked? |
| **P6** Manufacturing Readiness | G5 passed | **G6 — Manufacturing Readiness Review** | Could a supplier quote and build from this package unaided? |
| **P7** Closeout & Portfolio Release | G6 passed | **G7 — Program Closeout Review** | Is the program complete, released, and defensible? |

**Note on P3/P4 overlap:** analysis begins at W11 on parts already frozen at G2, in parallel with assembly integration. This is a deliberate 2-week schedule compression and is the plan's primary parallelism opportunity outside P2. It carries risk R-06 (see §10).

---

## 2. Work Breakdown Structure

Notation — **Rev** = review type required: `—` none · `PR` peer review · `DAR` Design Authority review · `CR` independent checker · `GR` gate review.

### 1.0 — Phase P0: Program Setup & Baseline Control · 16 h · W1

| WBS | Task / Step | Hrs | Rev |
|---|---|---|---|
| **1.1** | **Repository & Configuration Management Establishment** | **6** | **PR** |
| 1.1.1 | Create GitHub repository `sewcp-sedep`; apply branch protection on `main` (no direct push, PR + 1 approval) | 1 | — |
| 1.1.2 | Commit the frozen specification set Vol 00–09 unmodified; apply immutable tag `baseline/spec-revA` | 1 | — |
| 1.1.3 | Create the full directory scaffold per SEDEP-PMP-002 §1 with README stubs | 1.5 | — |
| 1.1.4 | Configure CI workflow skeleton: lint, validator suite, unit tests, documentation build | 2 | — |
| 1.1.5 | Create CODEOWNERS, PR template carrying the gate checklist, and issue templates for ECR-Q / ECR-D | 0.5 | — |
| **1.2** | **Baseline Extraction & Requirements Traceability** | **6** | **DAR** |
| 1.2.1 | Extract all numbered functional requirements (CP-01…, HP-01…, SR-01…, EC-01…, LP-01…, AP-01…, VP-01…, RF-01…, TS-01…) into `requirements.yaml` | 1.5 | — |
| 1.2.2 | Extract all critical dimensions (CP-D01…, HP-D01… etc.) into `dimensions.yaml`, flagged by criticality | 1.5 | — |
| 1.2.3 | Extract Design Rules DR-1 … DR-13 into `design_rules.yaml` with machine-checkable predicates where possible | 1 | — |
| 1.2.4 | Build the **Requirements Traceability Matrix** skeleton: Requirement → Part → Model feature → Drawing → Verification method → Status | 1.5 | — |
| 1.2.5 | Completeness audit: extracted count reconciled line-by-line against source volumes; zero orphans permitted | 0.5 | — |
| **1.3** | **Open Item Disposition** | **4** | **DAR** |
| 1.3.1 | Raise **OI-1** (confirm FBA-1…FBA-8 against the actual Base Plate) as a **blocking** action on 3.3 Support Ring | 1 | — |
| 1.3.2 | Raise **OI-2** (Configuration A vs B) as a **blocking** action on 3.9 RF Bracket | 1 | — |
| 1.3.3 | Disposition OI-3 (choke tuning), OI-4 (lift pin BC vs robot), OI-5 (bond elastomer) to Phase P4 | 1 | — |
| 1.3.4 | Publish the Assumptions Register; every assumption carries an owner and a closure date | 1 | — |

**→ GATE G0 — Baseline Freeze Review** · W1 Fri · `GR`

---

### 2.0 — Phase P1: Digital Engineering Foundation · 46 h · W2–W4

| WBS | Task / Step | Hrs | Rev |
|---|---|---|---|
| **2.1** | **Parameter Master Development** | **12** | **DAR** |
| 2.1.1 | Author `params/global.yaml`: datum frame, clocking map (all 10 feature families), Z-stack, material property table | 3 | — |
| 2.1.2 | Author `params/<part>.yaml` for all 10 parts from the Critical Dimensions tables | 4 | — |
| 2.1.3 | Implement the derived-parameter resolver (e.g. `H_ring = 55.920 − Σ(measured elements)` per DR-3) | 2 | — |
| 2.1.4 | Unit and dimensional-consistency checking; every parameter carries units and a source citation (volume + table ref) | 2 | — |
| 2.1.5 | Emit Fusion 360 user-parameter CSV per part | 1 | — |
| **2.2** | **Geometric Validator Suite** | **14** | **DAR** |
| 2.2.1 | Clocking-map conflict checker — angular/radial collision detection across all feature families at all bolt circles | 4 | — |
| 2.2.2 | Coolant keep-out validator for the Cooling Plate (Ø60–Ø250 envelope + 7 keep-out classes) | 3 | — |
| 2.2.3 | Datum scheme validator — every part declares A/B/C; every position callout references a valid frame | 2 | — |
| 2.2.4 | Design-rule checker for the machine-checkable subset of DR-1…DR-13 (DR-1 clearance, DR-2 no top-face penetration, DR-4 pin engagement, DR-6/DR-13 blind-hole venting) | 3 | — |
| 2.2.5 | Regression fixtures built from the three conflicts found during specification development (ring bolt/wall, RF land collision, RTD/RF land) — the suite must **reproduce and catch** all three | 2 | — |
| **2.3** | **Engineering Calculation Library** | **12** | **DAR** |
| 2.3.1 | Tolerance stack engine — worst-case and RSS; Z-stack and concentricity chains | 2.5 | — |
| 2.3.2 | Thermal resistance network solver — 7-element chain, target 0.122 K/W | 2.5 | — |
| 2.3.3 | Electrostatic clamping model — `d_eff`, pressure-vs-voltage table | 1.5 | — |
| 2.3.4 | Paschen `p·d` evaluator across all declared gas gaps | 1.5 | — |
| 2.3.5 | RF model — skin depth, strap AC resistance, loop inductance | 1.5 | — |
| 2.3.6 | Coolant flow model — Reynolds, ΔP, convective coefficient | 1 | — |
| 2.3.7 | **Back-validation:** every function reproduces the corresponding hand calculation in Vol 00–09 to 3 significant figures, as unit tests | 1.5 | — |
| **2.4** | **CAD Automation Scripts** | **8** | **PR** |
| 2.4.1 | Fusion 360 parameter-push script (YAML → user parameters) | 2 | — |
| 2.4.2 | Mesa array generator — Ø0.8 at 6.0 mm hex pitch over Ø290, with lift-pin and port keep-outs | 3 | — |
| 2.4.3 | Feature pattern generator driven by the clocking map | 2 | — |
| 2.4.4 | Export automation — STEP / PDF / BOM | 1 | — |

**→ GATE G1 — Digital Foundation Review** · W4 Fri · `GR`

---

### 3.0 — Phase P2: Part Modelling · 78 h · W4–W10

| WBS | Task / Step | Hrs | Rev |
|---|---|---|---|
| **3.1** | **Reference & Skeleton Model** — *critical path origin* | **6** | **DAR** |
| 3.1.1 | Model the frozen Base Plate envelope per FBA-1…FBA-8; mark component **FROZEN — REFERENCE ONLY**, lock read-only | 2 | — |
| 3.1.2 | Build the datum skeleton — Datum A plane, B/C axes, 0° clocking reference | 1.5 | — |
| 3.1.3 | Build the Z-stack skeleton — all 8 stack planes at nominal | 1.5 | — |
| 3.1.4 | Publish skeleton as the linked reference consumed by every part design | 1 | — |
| **3.2** | **SEWCP-200 Cooling Plate** — *critical path; interface hub* | **16** | **DAR** |
| 3.2.1 | Body Ø320 × 20.000; establish datums A/B/C | 2 | — |
| 3.2.2 | Coolant serpentine within the Ø60–Ø250 envelope; run keep-out validator to closure | 4 | — |
| 3.2.3 | FSW lid modelled as a discrete body/component (6.00 mm) | 1.5 | — |
| 3.2.4 | 16 choke pads; 16 M5 slotted clearance holes; 6 kinematic dowel counterbores (Ø306 bottom, Ø260 top) | 3 | — |
| 3.2.5 | 3 lift pin bores + bushing counterbores; 2 HV feed bores; central Ø10 He bore | 2 | — |
| 3.2.6 | RF land (60 × 18 at Ø274 BC, 105°); 3 RTD ports (r=40@75°, r=100@165°, r=140@225°); vacuum port interface (Ø10 pilot, 4× M4 at Ø38 BC); 8× M6 tapped at Ø302 BC | 2 | — |
| 3.2.7 | Anodize mask zones modelled as a discrete appearance/body set (5 masked surfaces) | 1 | — |
| 3.2.8 | Run full validator suite; verify mass ≤ 4.2 kg | 0.5 | — |
| **3.3** | **SEWCP-400 Chuck Support Ring** — *blocked by OI-1* | **8** | **DAR** |
| 3.3.1 | Flanged cylinder: web Ø300/Ø294 × 14.0; flanges Ø318/Ø286 × 3.0; total 20.300 as-supplied | 2.5 | — |
| 3.3.2 | 16 bolt clearance holes (8 per flange) at Ø302 BC; R3 web-to-flange fillets | 2 | — |
| 3.3.3 | 3 kinematic radial slots (6.05 × 8.0 × 3.0) at Ø306 BC, 60°/180°/300° | 1.5 | — |
| 3.3.4 | Clamp ring register counterbore; SEWCP-401 clamp ring (316L) | 1.5 | — |
| 3.3.5 | Model the DR-3 lap condition as a configuration variant (as-supplied 20.300 / as-lapped nominal) | 0.5 | — |
| **3.4** | **SEWCP-300 Heater Plate** | **10** | **DAR** |
| 3.4.1 | Body Ø300 × 8.000; datums; bond face and choke face | 2 | — |
| 3.4.2 | Two-zone spiral heater grooves (3.2 × 3.2 at 6.0 pitch); verify HP-D08 4.6 mm minimum spreading thickness | 3 | — |
| 3.4.3 | 16 M5 tapped (insert) positions; 3 kinematic radial slots at Ø260 BC | 2 | — |
| 3.4.4 | He transfer bore + secondary O-ring groove; 2 HV feed bores; 3 lift pin clearance bores; 2 RTD ports | 2 | — |
| 3.4.5 | SEWCP-301 thermal choke washer (Ø22.0/Ø10.5 × 1.500), 16 off | 1 | — |
| **3.5** | **SEWCP-500 Electrostatic Chuck** | **12** | **DAR** |
| 3.5.1 | Puck Ø297 × 6.000; underside bond face; outer 0.5 × 45° chamfer | 2 | — |
| 3.5.2 | **Mesa field via script 2.4.2** — Ø0.8 at 6.0 hex over Ø290, 20 µm; verify 1.55% contact area | 3 | — |
| 3.5.3 | Seal band Ø291–297, 3.0 wide, coplanar with mesas | 1.5 | — |
| 3.5.4 | He distribution grooves — 12 radial + 1 annular at Ø150 | 2 | — |
| 3.5.5 | Buried bipolar electrode geometry (D-pattern, 3.0 pole gap, 0.300 dielectric) as a discrete internal body | 2 | — |
| 3.5.6 | 3 lift pin bores Ø5.200 with 0.3 × 45° chamfer, **no counterbore** (DR-4/Paschen); central Ø1.5 He port; 2 HV pads | 1.5 | — |
| **3.6** | **SEWCP-600 / -601 Lift Pin & Bushing** | **5** | **PR** |
| 3.6.1 | Pin: Ø5.000 × 95.0, R50 crown, Ø8 foot, R1.0 fillets | 2 | — |
| 3.6.2 | Bushing SEWCP-601 (Vespel, Ø12 OD, Ø5.60 bore) | 1 | — |
| 3.6.3 | Model full-up / full-down travel positions as configurations | 1.5 | — |
| 3.6.4 | Verify DR-4 engagement at both extremes | 0.5 | — |
| **3.7** | **SEWCP-700 Alignment Pin** | **4** | **PR** |
| 3.7.1 | Shouldered locator: Ø6.000 h6 boss × 2.50 protrusion, Ø12.000 k6 flange × 3.00, R0.4 fillet | 2 | — |
| 3.7.2 | Verify AP-D02 boss/slot bottom clearance = 0.50 mm at both interfaces | 1 | — |
| 3.7.3 | Verify ±1.0 mm radial travel against the 0.326 / 0.399 mm requirements | 1 | — |
| **3.8** | **SEWCP-800 Vacuum Port Assembly** | **6** | **PR** |
| 3.8.1 | SEWCP-801 body: Ø50 flange × 10, Ø9.90 pilot, Ø4.0 bore | 2 | — |
| 3.8.2 | O-ring groove Ø24.50 × 3.20 W × 1.90 D; verify 24% squeeze / 81% fill in the calc library | 1.5 | — |
| 3.8.3 | SEWCP-802 orifice restrictor Ø0.500; SEWCP-803 O-ring; SEWCP-804 VCR stub | 1.5 | — |
| 3.8.4 | Verify ≥ 2 mm Base Plate aperture clearance (DR-1) | 1 | — |
| **3.9** | **SEWCP-900 RF Bracket Assembly** — *blocked by OI-2* | **7** | **DAR** |
| 3.9.1 | SEWCP-901 strap: 50.0 W × 0.50, R20 compliance loop, 50 × 18 terminal pads | 2.5 | — |
| 3.9.2 | SEWCP-902 support bracket; saddle sets installed height 8.0 ± 1.0 mm | 2 | — |
| 3.9.3 | SEWCP-904 deposition shroud with anti-tracking grooves | 1.5 | — |
| 3.9.4 | Verify DR-12 (shroud does not bridge) and ≥ 8 mm vacuum-side clearance throughout the run | 1 | — |
| **3.10** | **SEWCP-1000 Temperature Sensor Bracket Set** | **4** | **PR** |
| 3.10.1 | SEWCP-1000 retainer (5 off) with vent slot | 1.5 | — |
| 3.10.2 | SEWCP-1002 side-load clip; SEWCP-1001 harness bracket; SEWCP-1003 fibre mount | 1.5 | — |
| 3.10.3 | Verify DR-13 vent alignment at all 5 ports | 1 | — |

**→ GATE G2 — Model Design Review** · W10 Fri · `GR`

---

### 4.0 — Phase P3: Assembly Integration & Digital Mock-Up · 30 h · W10–W12

| WBS | Task / Step | Hrs | Rev |
|---|---|---|---|
| **4.1** | **Sub-Assembly Builds** | **8** | **PR** |
| 4.1.1 | SEWCP-350 bonded sub-assembly (Heater Plate + ESC + 0.400 bond layer as a modelled body) | 3 | — |
| 4.1.2 | Support Ring + Cooling Plate sub-assembly per Vol 03 §10 Phase 1 (inverted build) | 2 | — |
| 4.1.3 | Vacuum Port and RF Bracket sub-assemblies | 2 | — |
| 4.1.4 | Lift pin + bushing + yoke interface sub-assembly | 1 | — |
| **4.2** | **Master Assembly & Joint Definition** | **10** | **DAR** |
| 4.2.1 | Insert frozen Base Plate reference; ground it as the assembly datum | 1 | — |
| 4.2.2 | Build the stack in the released assembly order (Vol 00 §10 C1–C7) | 3 | — |
| 4.2.3 | Define joints: rigid at bolted interfaces, **slider at the 6 kinematic radial slots**, slider at lift pins | 3 | — |
| 4.2.4 | Install utilities: vacuum port, RF bracket, sensor retainers | 2 | — |
| 4.2.5 | Apply the released fastener schedule and torque table as assembly metadata | 1 | — |
| **4.3** | **Interference & Clearance Audit** | **6** | **DAR** |
| 4.3.1 | Full interference check, all bodies, zero-tolerance | 1.5 | — |
| 4.3.2 | **DR-1 audit** — verify ≥ 2 mm radial float at all four non-Ring Base Plate touchpoints | 1.5 | — |
| 4.3.3 | RF clearance audit — ≥ 8 mm vacuum side over the entire strap run (DR-12) | 1.5 | — |
| 4.3.4 | Creepage audit — ≥ 20 mm across the Support Ring web (target 40 mm per Vol 03 §3.1) | 1 | — |
| 4.3.5 | Robot end-effector envelope sweep in the 210° clear sector | 0.5 | — |
| **4.4** | **Motion Study — Lift Pin Travel** | **4** | **DAR** |
| 4.4.1 | Drive lift pins through 20.0 mm travel | 1 | — |
| 4.4.2 | **Verify DR-4** — pin fills the full 6 mm ESC bore at every position; ≥ 10 mm below the ESC underside at full-up | 1.5 | — |
| 4.4.3 | Verify full-down tip 0.05–0.15 mm below the mesa plane | 1 | — |
| 4.4.4 | Verify no collision with He grooves, HV bores, or coolant circuit through travel | 0.5 | — |
| **4.5** | **Mass Properties & Configuration Audit** | **2** | **PR** |
| 4.5.1 | Extract mass and CG; reconcile against the 7.5 kg stack figure used in Vol 03 §2.2 | 1 | — |
| 4.5.2 | BOM generation; part-number and quantity audit against all volumes | 1 | — |

**→ GATE G3 — Critical Design Review** · W12 Fri · `GR`

---

### 5.0 — Phase P4: Engineering Analysis & Verification · 44 h · W11–W14

| WBS | Task / Step | Hrs | Rev |
|---|---|---|---|
| **5.1** | **Tolerance Stack Verification** | **8** | **DAR** |
| 5.1.1 | Z-stack: reproduce WC ±0.153 and RSS ±0.069 from as-modelled values | 2 | — |
| 5.1.2 | Demonstrate DR-3 lap-to-fit closes the WC shortfall to ±0.020 | 2 | — |
| 5.1.3 | Flatness/parallelism budget: reproduce 34.6 µm RSS against the 50 µm requirement | 2 | — |
| 5.1.4 | Concentricity budget: reproduce 0.137 mm RSS against 0.20 mm | 1 | — |
| 5.1.5 | Monte Carlo (10⁴ runs) on the Z stack; report Cpk against ±0.150 | 1 | — |
| **5.2** | **Thermal Verification** | **12** | **DAR** |
| 5.2.1 | Network model: reproduce the 0.122 K/W chain and the 36.6 K rise at 300 W | 2 | — |
| 5.2.2 | FEA — steady-state stack thermal at the 300 W design point | 3 | — |
| 5.2.3 | FEA — wafer-plane uniformity against ±2.0 °C; correlate with the two-zone split | 3 | — |
| 5.2.4 | Thermal choke sensitivity study: R_choke 0.07 / 0.10 / 0.13 K/W (**OI-3 closure**) | 2 | — |
| 5.2.5 | Transient: verify τ ≈ 280 s and ≥ 40 K/min ramp | 2 | — |
| **5.3** | **Structural Verification** | **10** | **DAR** |
| 5.3.1 | FEA — Support Ring under 8× 6.0 N·m preload; confirm compression-only loading and the §2.2 margins | 3 | — |
| 5.3.2 | FEA — Cooling Plate gravity + preload deflection against the 15 µm flatness allocation | 2.5 | — |
| 5.3.3 | FEA — ESC bond shear at 55% strain, 20 → 150 °C (**OI-5 input**) | 2.5 | — |
| 5.3.4 | Hand-check: lift pin Hertzian contact 77.5 MPa; Euler margin | 1 | — |
| 5.3.5 | Bolted-joint analysis: Belleville preload retention over ΔT = 130 K | 1 | — |
| **5.4** | **Electrical & RF Verification** | **6** | **DAR** |
| 5.4.1 | Reproduce Support Ring R_th 0.195 K/W and C 27.0 pF / X_C 435 Ω, including the 9.6 pF stray flange term | 1.5 | — |
| 5.4.2 | Reproduce clamping pressure table; confirm the ±1800 V floor for 20 Torr He | 1.5 | — |
| 5.4.3 | Paschen sweep across all declared gaps; confirm DR-4, DR-5, DR-11 coverage | 1.5 | — |
| 5.4.4 | Strap inductance from as-modelled geometry; confirm ≤ 35 nH | 1.5 | — |
| **5.5** | **Flow Verification** | **4** | **PR** |
| 5.5.1 | Reproduce Re ≈ 7,400 at 4 L/min from as-modelled channel geometry | 1 | — |
| 5.5.2 | Developed path length and ΔP estimate against the < 1.5 bar requirement | 1.5 | — |
| 5.5.3 | Verify the 2.5 L/min turbulence-loss interlock threshold | 0.5 | — |
| 5.5.4 | Orifice choked-flow check: 138 sccm at 20 Torr | 1 | — |
| **5.6** | **Residual Open Item Closure** | **4** | **DAR** |
| 5.6.1 | **OI-3** closed by 5.2.4 | 1 | — |
| 5.6.2 | **OI-4** — lift pin Ø200 BC against the robot envelope; wafer sag estimate | 1.5 | — |
| 5.6.3 | **OI-5** — bond elastomer selection and 100-cycle durability rationale | 1.5 | — |

**→ GATE G4 — Analysis Verification Review** · W14 Fri · `GR`

---

### 6.0 — Phase P5: Drawing & Documentation Release · 36 h · W13–W16

| WBS | Task / Step | Hrs | Rev |
|---|---|---|---|
| **6.1** | **Drawing Standard & Template** | **4** | **DAR** |
| 6.1.1 | Title block, revision block, sheet sizes, standard notes | 1.5 | — |
| 6.1.2 | GD&T standard declaration (ASME Y14.5-2018); default tolerance block | 1 | — |
| 6.1.3 | **Standard note set:** DO NOT ANODIZE, anti-galling, vent-all-blind-holes, ceramic edge break, masking callout | 1.5 | — |
| **6.2** | **Part Drawings ×10** | **20** | **CR** |
| 6.2.1 | SEWCP-200 Cooling Plate (multi-sheet: geometry, **masking sheet**, channel) | 4 | `CR` |
| 6.2.2 | SEWCP-300 Heater Plate (+ SEWCP-301 washer) | 2.5 | `CR` |
| 6.2.3 | SEWCP-400 Support Ring (+ SEWCP-401 clamp ring), incl. as-supplied/as-lapped condition | 2.5 | `CR` |
| 6.2.4 | SEWCP-500 ESC (multi-sheet: geometry, surface architecture, buried electrode) | 3.5 | `CR` |
| 6.2.5 | SEWCP-600 / -601 Lift Pin & Bushing, incl. matched-set note | 1.5 | `CR` |
| 6.2.6 | SEWCP-700 Alignment Pin | 1 | `CR` |
| 6.2.7 | SEWCP-800 Vacuum Port Assembly | 2 | `CR` |
| 6.2.8 | SEWCP-900 RF Bracket Assembly | 2 | `CR` |
| 6.2.9 | SEWCP-1000 Sensor Bracket set | 1 | `CR` |
| **6.3** | **Assembly Drawing & BOM** | **5** | **CR** |
| 6.3.1 | Master assembly drawing with balloons and indentured BOM | 2 | — |
| 6.3.2 | Assembly sequence sheets reproducing Vol 00 §10 | 2 | — |
| 6.3.3 | Fastener and torque schedule sheet | 1 | — |
| **6.4** | **Interface Control Drawing** | **3** | **DAR** |
| 6.4.1 | ICD sheet 1 — frozen Base Plate interface, all five touchpoints, DR-1 float callouts | 1.5 | — |
| 6.4.2 | ICD sheet 2 — external interfaces (coolant, He, RF, heater, sensors, lift actuator) | 1.5 | — |
| **6.5** | **Check & Redline Cycle** | **4** | **CR** |
| 6.5.1 | Independent check of all 12 drawings; redlines logged | 2 | — |
| 6.5.2 | Redline incorporation and back-check | 1.5 | — |
| 6.5.3 | RTM closure: every requirement mapped to a drawing or an analysis report | 0.5 | — |

**→ GATE G5 — Drawing Release Review** · W16 Fri · `GR`

---

### 7.0 — Phase P6: Manufacturing Readiness · 12 h · W16–W17

| WBS | Task / Step | Hrs | Rev |
|---|---|---|---|
| **7.1** | **RFQ Package Assembly** | **4** | **PR** |
| 7.1.1 | Per-part RFQ folders: drawing PDF, STEP, material spec, finish spec, inspection requirements | 2 | — |
| 7.1.2 | Process-critical notes extracted per part (FSW + radiography; braze + T6 re-heat-treat; co-fire in reducing atmosphere; green-machine + lap) | 1.5 | — |
| 7.1.3 | Quantity and spares schedule | 0.5 | — |
| **7.2** | **Supplier Capability Matrix** | **3** | **PR** |
| 7.2.1 | Map each part to a required process capability class (FSW aluminium / technical ceramic / co-fired ceramic / precision CNC / orbital weld / EDM) | 1.5 | — |
| 7.2.2 | Identify single-source and long-lead items — ESC co-fire, Support Ring, MI heater braze | 1.5 | — |
| **7.3** | **Inspection & Acceptance Test Plan** | **3** | **DAR** |
| 7.3.1 | Per-part first-article inspection plan keyed to critical dimensions | 1.5 | — |
| 7.3.2 | Assembly ATP procedure reproducing Vol 00 §12 T1–T21 | 1.5 | — |
| **7.4** | **Long-Lead & Procurement Schedule** | **2** | **PR** |
| 7.4.1 | Lead-time estimates and a notional procurement Gantt | 2 | — |

**→ GATE G6 — Manufacturing Readiness Review** · W17 Thu · `GR`

---

### 8.0 — Phase P7: Program Closeout & Portfolio Release · 18 h · W17–W18

| WBS | Task / Step | Hrs | Rev |
|---|---|---|---|
| **8.1** | **Documentation Release** | **5** | **DAR** |
| 8.1.1 | Promote all documents to Released per SEDEP-PMP-002 §5 | 1.5 | — |
| 8.1.2 | Apply release tag `release/v1.0`; generate the immutable release bundle | 1 | — |
| 8.1.3 | Publish the final RTM with 100% closure | 1.5 | — |
| 8.1.4 | Archive the Engineering Notebook | 1 | — |
| **8.2** | **Visual & Communication Assets** | **5** | **PR** |
| 8.2.1 | Rendered stack exploded view, section view, wafer-handoff sequence | 2.5 | — |
| 8.2.2 | Annotated thermal and tolerance-budget diagrams | 1.5 | — |
| 8.2.3 | Lift-pin travel animation | 1 | — |
| **8.3** | **Resume & Portfolio Deliverables** | **5** | **DAR** |
| 8.3.1 | Program one-pager | 1.5 | — |
| 8.3.2 | Resume bullet set with quantified outcomes | 1.5 | — |
| 8.3.3 | Interview asset pack — top 12 talking points with supporting figures | 2 | — |
| **8.4** | **Program Closeout** | **3** | **GR** |
| 8.4.1 | Closeout report: planned vs actual effort, schedule variance, gate history | 1.5 | — |
| 8.4.2 | Lessons learned; ECR log summary | 1.5 | — |

**→ GATE G7 — Program Closeout Review** · W18 Fri · `GR`

---

## 3. Dependency Network

### 3.1 Dependency Table

Type: **FS** finish-to-start · **SS** start-to-start · **FF** finish-to-finish

| WBS | Predecessor(s) | Type | Lag | Rationale |
|---|---|---|---|---|
| 1.2 | 1.1 | FS | 0 | Repository must exist before extraction commits |
| 1.3 | 1.2 | SS | 0 | Open items identified during extraction |
| 2.1 | **G0** | FS | 0 | Parameters derive from the controlled baseline |
| 2.2 | 2.1 | FS | 0 | Validators consume the parameter master |
| 2.3 | 2.1 | SS | 0 | Calc library needs parameters, not validators |
| 2.4 | 2.1 | FS | 0 | Scripts push parameters |
| 3.1 | **G1** | FS | 0 | Skeleton needs a validated parameter master |
| **3.2** | **3.1** | **FS** | **0** | **Cooling Plate consumes the skeleton — critical path** |
| 3.3 | 3.2, **OI-1** | FS | 0 | Ring slots must match Cooling Plate dowels at Ø306; **blocked until OI-1 closes** |
| 3.4 | 3.2 | FS | 0 | Choke pads, slots at Ø260, fastener pattern all inherited |
| 3.5 | 3.4 | FS | 0 | ESC bond face and He/HV port alignment derive from the Heater Plate |
| 3.6 | 3.5 | FS | 0 | Pin fit is set by the ESC Ø5.200 bore |
| 3.7 | 3.2 | FS | 0 | Locator counterbores are in the Cooling Plate |
| 3.8 | 3.2 | FS | 0 | Pilot bore and M4 pattern are in the Cooling Plate |
| 3.9 | 3.2, **OI-2** | FS | 0 | RF land is in the Cooling Plate; **blocked until OI-2 closes** |
| 3.10 | 3.2, 3.4 | FS | 0 | Probe ports in both plates |
| 4.1 | **G2** | FS | 0 | Sub-assemblies need released models |
| 4.2 | 4.1 | FS | 0 | Master assembly consumes sub-assemblies |
| 4.3 | 4.2 | FS | 0 | Audit requires a complete assembly |
| 4.4 | 4.2 | FS | 0 | Motion study requires joints |
| 4.5 | 4.3, 4.4 | FS | 0 | Audits precede the configuration baseline |
| 5.1 | **G2** | FS | 0 | Runs on frozen models, in parallel with P3 |
| 5.2 | **G2** | FS | 0 | " |
| 5.3 | **G2** | FS | 0 | " |
| 5.4 | **G2** | FS | 0 | " |
| 5.5 | 3.2 | FS | 0 | Needs only the Cooling Plate channel |
| 5.6 | 5.2, 5.3 | FS | 0 | OI-3/OI-5 close from thermal and structural results |
| 6.1 | **G3** | FS | 0 | Template settles once the assembly is stable |
| 6.2 | 6.1 | FS | 0 | Drawings need the template |
| 6.3 | 6.2, 4.5 | FS | 0 | Assembly drawing needs part drawings and the BOM |
| 6.4 | 4.3 | FS | 0 | ICD needs the clearance audit |
| 6.5 | 6.2, 6.3, 6.4, **G4** | FS | 0 | Check follows all drawings; RTM needs analysis closed |
| 7.1 | **G5** | FS | 0 | RFQ needs released drawings |
| 7.2 | 7.1 | SS | 0 | — |
| 7.3 | 7.1 | SS | 0 | — |
| 7.4 | 7.2 | FS | 0 | — |
| 8.1 | **G6** | FS | 0 | — |
| 8.2 | **G3** | FS | 0 | **Renders can start early** — geometry is frozen at G3 |
| 8.3 | 8.1, 8.2 | FS | 0 | — |
| 8.4 | 8.3 | FS | 0 | — |

### 3.2 Critical Path

> **1.1 → 1.2 → G0 → 2.1 → 2.2 → G1 → 3.1 → 3.2 → 3.4 → 3.5 → G2 → 4.1 → 4.2 → 4.3 → G3 → 6.1 → 6.2 → 6.5 → G5 → 7.1 → G6 → 8.1 → 8.3 → 8.4 → G7**

**Total critical path effort: 178 h of the 280 h total (64%).**

**The Cooling Plate (3.2) is the single highest-leverage task in the program.** It hosts all six alignment locators, the RF land, three RTD ports, the vacuum port interface, the lift pin bushings, the 16 choke pads, and the Support Ring tapped holes. Seven of the nine remaining parts inherit geometry from it. **A one-week slip on 3.2 is a one-week slip on the program.** It is scheduled with the largest single-task allocation (16 h) and carries a DAR review specifically to prevent rework downstream.

**Secondary critical chain:** 3.2 → 3.4 → 3.5 (Cooling → Heater → ESC) is serial because each inherits its mating face from the one below. This chain accounts for 38 h and cannot be compressed without accepting interface rework risk.

### 3.3 Float Summary

| Chain | Float | Note |
|---|---|---|
| 3.3 Support Ring | 12 h | Blocked by OI-1; float consumed if OI-1 slips past W6 |
| 3.6 Lift Pin | 8 h | Late in the chain but small |
| 3.7 Alignment Pin | 20 h | Highest float; useful schedule buffer |
| 3.8 Vacuum Port | 16 h | — |
| 3.9 RF Bracket | 10 h | Blocked by OI-2 |
| 3.10 Sensor Bracket | 18 h | — |
| 5.x Analysis | 6 h | Compressed by the P3/P4 overlap |
| 8.2 Renders | 30 h | Can be pulled forward from G3 |

---

## 4. Parallelism Plan

| Group | Window | Tasks | Constraint |
|---|---|---|---|
| **PG-1** | W2–W4 | 2.2, 2.3, 2.4 | All start after 2.1; independent of each other |
| **PG-2** | W6–W10 | **3.3, 3.7, 3.8, 3.9, 3.10** | All start after 3.2 releases; **five-way parallel — the widest fan-out in the program** |
| **PG-3** | W7–W10 | 3.4 → 3.5 → 3.6 | Serial chain, runs concurrent with PG-2 |
| **PG-4** | W11–W12 | 4.1–4.5 (P3) ∥ 5.1–5.5 (P4) | **Phase-level parallelism.** Analysis runs on G2-frozen models while assembly integration proceeds |
| **PG-5** | W13–W14 | 6.1, 6.2 (early drawings) ∥ 5.2, 5.3 (analysis completion) | Drawings for parts not under analysis rework |
| **PG-6** | W16–W17 | 7.2, 7.3 | Both start after 7.1 |
| **PG-7** | W13–W18 | 8.2 renders ∥ everything | Geometry frozen at G3; no dependency on drawings |

**Parallelism ceiling:** PG-2 offers five-way fan-out but the baseline resourcing model is a single Lead Engineer, so PG-2 is executed as a **prioritised queue**, not concurrently. It is documented as a parallel group because:

1. It defines the **resource-loading opportunity** if a second engineer is added — adding one engineer at W6 compresses P2 by approximately 3 weeks.
2. It defines the **re-sequencing freedom** available when a task blocks. If OI-1 delays 3.3, the Lead Engineer moves to 3.7/3.8/3.10 with no schedule impact.

> **This distinction matters at gate reviews.** PG-2 tasks have no inter-dependency, so a blockage in one never justifies an idle week.

---

## 5. Design Review Plan

### 5.1 Review Types

| Type | Name | Chair | Duration | Trigger |
|---|---|---|---|---|
| `PR` | Peer Review | LE + one peer | 30 min | Task completion; informal, logged in the Notebook |
| `CR` | Independent Check | CK | 1–2 h | Every drawing. **Checker ≠ originator, mandatory** |
| `DAR` | Design Authority Review | DA | 1 h | Task completion on any task feeding a budget, an interface, or a Design Rule |
| `GR` | Gate Review | PM + DA | 2 h | Phase exit. **Formal go/no-go with recorded disposition** |

### 5.2 Tasks Requiring Review

| Review | WBS Tasks | Count |
|---|---|---|
| **DAR** | 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.9, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4, 5.6, 6.1, 6.4, 7.3, 8.1, 8.3 | **24** |
| **CR** | 6.2 (×9 drawings), 6.3, 6.5 | **11** |
| **PR** | 1.1, 2.4, 3.6, 3.7, 3.8, 3.10, 4.1, 4.5, 5.5, 7.1, 7.2, 7.4, 8.2 | **13** |
| **GR** | G0–G7 | **8** |

**Review selection rationale.** A task requires **DAR** if it satisfies any of:
- It creates or consumes a **shared interface** (3.2, 3.4, 3.5, 4.2)
- It closes an **engineering budget** (5.1–5.4)
- It verifies a **Design Rule** (3.3, 3.9, 4.3, 4.4)
- It establishes a **controlled artefact** others depend on (1.2, 2.1, 2.2, 6.1)

Tasks producing self-contained geometry with no downstream consumers (3.7, 3.10) require only peer review. **All drawings require independent check without exception** — checking one's own drawing is not a check.

### 5.3 Gate Review Standing Agenda

1. Entry criteria confirmation
2. Deliverable walkthrough against acceptance criteria
3. RTM status — new, closed, and at-risk requirements
4. Open ECR log
5. Risk register review — new, changed, retired
6. Dashboard review — schedule, effort, budget health
7. **Disposition:** PASS / PASS WITH ACTIONS / FAIL
8. Actions recorded with owner and due date

> **A gate may pass with actions only if no action is on the critical path.** Otherwise the gate fails and the phase is extended. This rule exists to prevent gate-passing by deferral.

---

## 6. Milestone Schedule

| MS | Gate | Title | Week | Date | Cum. Hours | Cum. % |
|---|---|---|---|---|---|---|
| **M1** | G0 | Baseline Frozen & Traced | W1 | **2026-08-14** | 16 | 6% |
| **M2** | G1 | Digital Foundation Validated | W4 | **2026-09-04** | 62 | 22% |
| **M3** | G2 | All Parts Modelled & Verified | W10 | **2026-10-16** | 140 | 50% |
| **M4** | G3 | Critical Design Review Complete | W12 | **2026-10-30** | 170 | 61% |
| **M5** | G4 | Analysis Verification Complete | W14 | **2026-11-13** | 214 | 76% |
| **M6** | G5 | Drawing Set Released | W16 | **2026-11-27** | 250 | 89% |
| **M7** | G6 | Manufacturing Ready | W17 | **2026-12-04** | 262 | 94% |
| **M8** | G7 | Program Closed & Released | W18 | **2026-12-11** | 280 | 100% |

### 6.1 Schedule Bar

```
        W1  W2  W3  W4  W5  W6  W7  W8  W9  W10 W11 W12 W13 W14 W15 W16 W17 W18
P0      ██
P1          ████████████
P2                  ████████████████████████████
P3                                          ████████████
P4                                      ████████████████████
P5                                                  ████████████████████
P6                                                                  ████████
P7                                                                      ████████
Gates   G0          G1                      G2      G3      G4      G5  G6  G7
Renders                                             ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
```

### 6.2 Interim Checkpoints (non-gate)

| CP | Week | Content | Purpose |
|---|---|---|---|
| CP-1 | W6 | Cooling Plate model complete and DAR-approved | **Critical path health check** — earliest reliable schedule signal |
| CP-2 | W8 | PG-2 at 50% | Fan-out progress |
| CP-3 | W13 | First 3 drawings checked | Validates the drawing effort estimate before committing to the remaining 9 |
| CP-4 | W15 | RTM ≥ 80% closed | Early warning on gate G5 |

---

## 7. Milestone Deliverables

### M1 — Baseline Frozen & Traced (G0)
| # | Deliverable | Format |
|---|---|---|
| D1.1 | GitHub repository with branch protection and CI skeleton | Repo + `baseline/spec-revA` tag |
| D1.2 | `requirements.yaml`, `dimensions.yaml`, `design_rules.yaml` | YAML, version-controlled |
| D1.3 | Requirements Traceability Matrix v0 | CSV + rendered table |
| D1.4 | Assumptions Register (FBA-1…FBA-8 + derived) | Markdown |
| D1.5 | Open Item Log with owners and dates | Markdown |
| D1.6 | Directory scaffold per SEDEP-PMP-002 | Repo tree |

### M2 — Digital Foundation Validated (G1)
| # | Deliverable | Format |
|---|---|---|
| D2.1 | Parameter master — global + 10 part files | YAML |
| D2.2 | Geometric validator suite with regression fixtures | Python package + test report |
| D2.3 | Engineering calculation library | Python package |
| D2.4 | **Back-validation report** — every calc reproduces its spec hand calculation | Markdown + test output |
| D2.5 | Fusion 360 automation scripts | Python |
| D2.6 | Fusion parameter CSVs (10) | CSV |

### M3 — All Parts Modelled & Verified (G2)
| # | Deliverable | Format |
|---|---|---|
| D3.1 | Datum skeleton and frozen Base Plate reference model | Fusion design |
| D3.2 | **10 released part models** | Fusion designs |
| D3.3 | Per-part dimensional conformance report vs. Critical Dimensions tables | Markdown, 10 off |
| D3.4 | Validator clean-run report (clocking, keep-out, datum, design rule) | Test output |
| D3.5 | Per-part mass report vs. spec limits | CSV |
| D3.6 | RTM at ≥ 60% closure | CSV |

### M4 — Critical Design Review Complete (G3)
| # | Deliverable | Format |
|---|---|---|
| D4.1 | 4 sub-assemblies + master assembly | Fusion designs |
| D4.2 | Zero-interference report | PDF |
| D4.3 | **DR-1 clearance audit** — all four non-Ring touchpoints | Markdown + screenshots |
| D4.4 | **DR-4 motion study report** — pin engagement at all travel positions | Markdown + animation |
| D4.5 | RF clearance and creepage audit (DR-12) | Markdown |
| D4.6 | Mass properties and CG report | PDF |
| D4.7 | Indentured BOM | CSV |

### M5 — Analysis Verification Complete (G4)
| # | Deliverable | Format |
|---|---|---|
| D5.1 | Tolerance stack report incl. Monte Carlo and Cpk | PDF |
| D5.2 | Thermal analysis report — network + FEA + choke sensitivity | PDF |
| D5.3 | Structural analysis report — ring, plate, bond, joints | PDF |
| D5.4 | Electrical/RF verification report | PDF |
| D5.5 | Flow verification report | PDF |
| D5.6 | **OI-3, OI-4, OI-5 closure memos** | Markdown |
| D5.7 | RTM at ≥ 90% closure | CSV |

### M6 — Drawing Set Released (G5)
| # | Deliverable | Format |
|---|---|---|
| D6.1 | Drawing standard and template | Fusion template + PDF |
| D6.2 | **10 checked part drawings** | PDF + DWG |
| D6.3 | Master assembly drawing + indentured BOM | PDF |
| D6.4 | Assembly sequence sheets | PDF |
| D6.5 | Fastener & torque schedule sheet | PDF |
| D6.6 | Interface Control Drawing, 2 sheets | PDF |
| D6.7 | **Redline log with dispositions** | Markdown |
| D6.8 | RTM at 100% closure | CSV |

### M7 — Manufacturing Ready (G6)
| # | Deliverable | Format |
|---|---|---|
| D7.1 | 10 per-part RFQ folders (drawing, STEP, material, finish, inspection) | Folder set |
| D7.2 | Process-critical notes per part | Markdown |
| D7.3 | Supplier capability matrix | CSV |
| D7.4 | Long-lead and single-source register | Markdown |
| D7.5 | First-article inspection plans | PDF, 10 off |
| D7.6 | Assembly ATP procedure (T1–T21) | PDF |
| D7.7 | Notional procurement schedule | Gantt |

### M8 — Program Closed & Released (G7)
| # | Deliverable | Format |
|---|---|---|
| D8.1 | Release bundle, tag `release/v1.0` | Git tag + archive |
| D8.2 | Final RTM, 100% closed | CSV |
| D8.3 | Archived Engineering Notebook | Markdown set |
| D8.4 | Render set — exploded, section, sequence | PNG/MP4 |
| D8.5 | Program one-pager | PDF |
| D8.6 | Resume bullet set | Markdown |
| D8.7 | Interview asset pack | PDF |
| D8.8 | Closeout report + lessons learned | Markdown |

---

## 8. Milestone Acceptance Criteria

> Acceptance criteria are **binary and evidence-based.** "Substantially complete" is not a disposition.

### M1 — G0
| # | Criterion | Evidence |
|---|---|---|
| A1.1 | Tag `baseline/spec-revA` exists; spec files byte-identical to Rev A | `git diff` empty |
| A1.2 | 100% of numbered requirements extracted; **zero orphans** | Reconciliation count matches source |
| A1.3 | All 13 Design Rules captured with predicates | `design_rules.yaml` review |
| A1.4 | RTM contains a row for every requirement | Row count = requirement count |
| A1.5 | OI-1 and OI-2 assigned owners and dates | Open Item Log |
| A1.6 | CI runs green on an empty commit | CI badge |
| A1.7 | Branch protection enforced; no direct push to `main` | Repo settings screenshot |

### M2 — G1
| # | Criterion | Evidence |
|---|---|---|
| A2.1 | **Every calculation reproduces its spec hand calculation to 3 s.f.** | Unit test suite green |
| A2.2 | Specifically verified: 0.122 K/W · 0.1009 K/W · 38.9 mbar · 27.0 pF / 435 Ω · Re 7,400 · 30.2 nH · 138 sccm · ±0.069 RSS | Named test cases |
| A2.3 | Validator catches all 3 historical conflicts in regression fixtures | Test output |
| A2.4 | Parameter master has zero unsourced values | Every entry carries a volume + table citation |
| A2.5 | Fusion CSV import succeeds on a trial design | Screenshot |
| A2.6 | Test coverage ≥ 85% on `sedep.analysis` and `sedep.validators` | Coverage report |

### M3 — G2
| # | Criterion | Evidence |
|---|---|---|
| A3.1 | All 10 part models exist and rebuild without error | Fusion rebuild log |
| A3.2 | **Every critical dimension matches the spec exactly** — zero deviation permitted | Per-part conformance report |
| A3.3 | Validator suite clean on every part | Test output |
| A3.4 | Base Plate model marked FROZEN and read-only | Fusion permissions |
| A3.5 | Masses within spec limits (CP ≤ 4.2 kg, HP ≤ 1.6 kg, ESC ≤ 1.7 kg, Ring ≤ 0.8 kg) | Mass report |
| A3.6 | Every part carries a declared A/B/C datum frame | Datum validator |
| A3.7 | **Zero open ECR-D (defects)** | ECR log |
| A3.8 | RTM ≥ 60% closed | RTM |

### M4 — G3
| # | Criterion | Evidence |
|---|---|---|
| A4.1 | Master assembly rebuilds; **zero interferences** | Interference report |
| A4.2 | **DR-1 satisfied:** ≥ 2 mm radial float at all four non-Ring touchpoints | Measured in CAD |
| A4.3 | **DR-4 satisfied:** pin fills the full 6 mm ESC bore at every travel position; ≥ 10 mm below the ESC underside at full-up | Motion study |
| A4.4 | Full-down tip 0.05–0.15 mm below the mesa plane | Measured |
| A4.5 | RF clearance ≥ 8 mm over the entire strap run | Measured |
| A4.6 | Creepage ≥ 20 mm across the Support Ring web | Measured |
| A4.7 | 6 kinematic joints modelled as sliders with ≥ ±1.0 mm travel | Joint definition |
| A4.8 | Wafer plane at **55.920 mm** nominal from Datum A | Measured |
| A4.9 | Robot sector at 210° clear through the handoff sweep | Sweep study |

### M5 — G4
| # | Criterion | Evidence |
|---|---|---|
| A5.1 | Z-stack RSS ≤ ±0.069 mm; DR-3 lap closes WC to ±0.020 mm | Tolerance report |
| A5.2 | Monte Carlo Cpk ≥ 1.33 against ±0.150 mm | Simulation output |
| A5.3 | Flatness budget RSS ≤ 35 µm vs. 50 µm requirement | Tolerance report |
| A5.4 | Thermal chain 0.122 ± 0.015 K/W confirmed by FEA | Thermal report |
| A5.5 | Wafer uniformity ≤ ±2.0 °C at the 300 W design point | FEA |
| A5.6 | Support Ring stress margin ≥ 100× in every load case | Structural report |
| A5.7 | ESC bond shear strain ≤ 60% at 150 °C | Structural report |
| A5.8 | Paschen sweep shows **no gap within a decade of the minimum** with its interlock inactive | RF report |
| A5.9 | Strap inductance ≤ 35 nH from as-modelled geometry | RF report |
| A5.10 | OI-3, OI-4, OI-5 formally closed | Closure memos |
| A5.11 | RTM ≥ 90% closed | RTM |

### M6 — G5
| # | Criterion | Evidence |
|---|---|---|
| A6.1 | 12 drawings complete, **each independently checked by a non-originator** | Signed check block |
| A6.2 | All redlines dispositioned and back-checked | Redline log |
| A6.3 | Every critical dimension on the drawing carries a tolerance | Drawing audit |
| A6.4 | Standard notes present where applicable: DO NOT ANODIZE (SEWCP-300), masking sheet (SEWCP-200), edge break (ceramics), anti-galling (all fasteners), vent-all-blind-holes | Drawing audit |
| A6.5 | GD&T references a declared datum frame on every drawing | Drawing audit |
| A6.6 | BOM quantities reconcile against all 10 volumes | BOM audit |
| A6.7 | **RTM 100% closed** — every requirement mapped to a drawing or analysis report | RTM |
| A6.8 | Zero open ECR of any class | ECR log |

### M7 — G6
| # | Criterion | Evidence |
|---|---|---|
| A7.1 | Every RFQ folder contains drawing + STEP + material + finish + inspection | Folder audit |
| A7.2 | Process-critical notes present for all 4 special-process parts | Notes audit |
| A7.3 | Every part mapped to a capability class | Capability matrix |
| A7.4 | Long-lead and single-source items identified with lead times | Register |
| A7.5 | ATP procedure covers all 21 acceptance tests | Cross-reference |
| A7.6 | **Independent readability test:** a reviewer unfamiliar with the program can identify what to make from one RFQ folder alone | Reviewer sign-off |

### M8 — G7
| # | Criterion | Evidence |
|---|---|---|
| A8.1 | Tag `release/v1.0` applied; bundle reproducible from the tag | Clean-clone build |
| A8.2 | RTM 100% closed and published | RTM |
| A8.3 | Engineering Notebook complete with no gaps > 5 working days | Notebook audit |
| A8.4 | All render assets produced | Asset folder |
| A8.5 | Resume deliverables reviewed and approved | DA sign-off |
| A8.6 | Closeout report includes planned-vs-actual on effort and schedule | Report |
| A8.7 | **Zero uncommitted work; zero local-only files** | `git status` clean |

---

## 9. Program Controls

### 9.1 Earned Value Metrics

| Metric | Definition | Threshold |
|---|---|---|
| **SPI** | Earned hours ÷ planned hours to date | Green ≥ 0.95 · Amber 0.85–0.95 · Red < 0.85 |
| **CPI** | Earned hours ÷ actual hours to date | Green ≥ 0.90 · Amber 0.80–0.90 · Red < 0.80 |
| **RTM closure** | Closed requirements ÷ total | Tracked against the gate profile (60/90/100%) |
| **ECR-D count** | Open specification defects | **Any open ECR-D is Red at a gate** |
| **Critical path float** | Days of float on the CP | Green > 5 d · Amber 0–5 d · Red < 0 |

### 9.2 Change Control

All changes route through SEDEP-PMP-002 §5. Summary of authority:

| Change class | Approver | Gate impact |
|---|---|---|
| Plan change (schedule, effort, sequencing) | PM | Recorded at next gate |
| ECR-Q (specification query) | DA | None if resolved within phase |
| **ECR-D (specification defect)** | **DA + Gate** | **Affected phase re-gated** |
| Baseline change (product geometry) | **Prohibited under this plan** | Requires a new specification revision and a re-planned program |

---

## 10. Risk Register

Exposure = Probability (1–5) × Impact (1–5). **Red ≥ 15 · Amber 8–14 · Green ≤ 7.**

| ID | Risk | Cat | P | I | Exp | Response | Owner | Trigger | Contingency |
|---|---|---|---|---|---|---|---|---|---|
| **R-01** | **OI-1 unresolved: actual Base Plate differs from FBA-1…FBA-8** | Technical | 4 | 4 | **16** | **Mitigate** — DR-1 already confines impact to the Support Ring. Force OI-1 closure by W3, ahead of its W6 need date | DA | No Base Plate drawing by W3 | Model Ring to FBA as-declared; add a parametric bolt-circle variant; re-machine model only |
| **R-02** | **Cooling Plate (3.2) slips — critical path is 64% of program** | Schedule | 3 | 5 | **15** | **Mitigate** — largest single allocation, DAR review, CP-1 checkpoint at W6 | PM | 3.2 incomplete at end W6 | Consume the 12% program reserve; defer 3.10 and 8.2 out of P2 window |
| **R-03** | Coolant serpentine cannot satisfy all 8 keep-out classes as drawn | Technical | 3 | 4 | **12** | **Mitigate** — validator 2.2.2 built before modelling starts, precisely to find this early | LE | Validator fails on first routing attempt | Raise **ECR-Q**: route within the envelope is a modelling decision, not a spec change. If truly infeasible → ECR-D and re-gate |
| **R-04** | ESC mesa array (≈ 8,900 features) degrades Fusion performance | Tool | 4 | 3 | **12** | **Mitigate** — script-generated; evaluate pattern-vs-body strategy at 3.5.2 | LE | Rebuild > 60 s | Represent the mesa field as a single derived body; retain the true array in a separate detail design used only for the drawing |
| **R-05** | OI-2 unresolved: Configuration A vs B | Technical | 3 | 3 | 9 | **Mitigate** — force decision by W5 | DA | No decision by W5 | Proceed with Configuration A as specified; Config B deletes SEWCP-900 and simplifies the Ring — **a subtractive change, low rework** |
| **R-06** | **P3/P4 overlap causes analysis rework** — analysis runs on models that later change in assembly | Schedule | 3 | 4 | **12** | **Accept with control** — models are frozen at G2; only assembly-level changes permitted after | PM | Any ECR-D raised during P3 | Re-run affected analysis only; 6 h float exists in the 5.x chain |
| **R-07** | Drawing effort underestimated at 20 h for 10 parts | Schedule | 3 | 3 | 9 | **Mitigate** — CP-3 at W13 validates the estimate after 3 drawings | PM | First 3 drawings exceed 8 h | Reduce multi-sheet drawings to essential sheets; retain the masking sheet (SEWCP-200) and ESC surface sheet as non-negotiable |
| **R-08** | Independent checker unavailable (single-person execution) | Resource | 4 | 4 | **16** | **Mitigate** — identify and confirm the checker at G0, not at G5 | PM | No named checker at G0 | **Timeboxed self-check with a 72 h cooling-off period and a formal checklist.** Documented as a deviation in the closeout report — this weakens A6.1 and must be declared |
| **R-09** | FEA fidelity insufficient to confirm thermal budgets | Technical | 3 | 3 | 9 | **Mitigate** — network model is the primary evidence; FEA is corroborating | AN | FEA and network disagree > 20% | Report the network model as the verification of record; document FEA as indicative with stated limitations |
| **R-10** | Scope creep — the urge to improve the frozen design during modelling | Process | 4 | 4 | **16** | **Avoid** — §0.1 configuration statement; ECR routing; DAR at every interface task | PM | Any model deviating from a released dimension | Revert to released dimension. **Log the improvement idea in a Rev B backlog — do not implement** |
| **R-11** | Fusion 360 API changes break automation scripts | Tool | 2 | 3 | 6 | **Accept** — pin the API version; scripts are convenience, not critical path | LE | Script failure after update | Manual feature creation; ~6 h impact on 3.5 |
| **R-12** | Data loss — local-only work not committed | Process | 2 | 5 | 10 | **Mitigate** — daily commit discipline; A8.7 acceptance criterion; Fusion cloud versioning | CM | > 2 days without a commit | Restore from the last commit + Fusion version history |
| **R-13** | RTM closure stalls; requirements untraceable to artefacts | Process | 3 | 3 | 9 | **Mitigate** — gate profile 60/90/100%; CP-4 early warning at W15 | PM | RTM < 80% at W15 | Dedicate reserve to closure; accept documented waivers for non-verifiable requirements with DA approval |
| **R-14** | Analysis reveals a budget that does not close | Technical | 2 | 5 | 10 | **Mitigate** — every budget was hand-calculated in the spec; analysis is confirmatory | AN | Any budget missing by > 15% | **STOP. Raise ECR-D.** Re-gate G4. This is the one finding that could invalidate the frozen baseline |
| **R-15** | Portfolio deliverables compressed by schedule pressure at the end | Schedule | 3 | 3 | 9 | **Mitigate** — 8.2 renders start at G3 (W12) with 30 h float, not at W17 | PM | Renders not started by W15 | Reduce to exploded view + section view; drop the animation |

### 10.1 Top Risks

**R-01, R-08, R-10 all score 16.** Each has a different character and a different owner:

- **R-01** is a technical unknown, already architecturally contained by DR-1. The plan's job is to force closure early.
- **R-08** is a resourcing constraint that directly attacks an acceptance criterion. It must be resolved at G0 or declared as a deviation — it cannot be quietly ignored at G5.
- **R-10 is the risk this plan exists to control.** Having just written a specification with documented alternates and rejected options, the strongest pressure during execution will be to revisit them. §0.1 exists specifically to counter it, and the Rev B backlog exists to give good ideas somewhere to go that is not the model.

---

## 11. Project Dashboard

**Artefact:** `dashboard/DASHBOARD.md` — regenerated by `sedep.reports.dashboard` on every push to `main`, and rendered as the repository landing view.

### 11.1 Layout

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  SEDEP — SEWCP DIGITAL ENGINEERING PLATFORM        Week 09/18   2026-10-09   │
│  Phase: P2 Part Modelling            Next Gate: G2 — 2026-10-16  (7 days)    │
├──────────────────────────────────────────────────────────────────────────────┤
│  SCHEDULE                                                                     │
│  SPI 0.97 ● GREEN   │  Earned 118 h / Planned 122 h  │  CP float +4 d ▲AMBER │
│  CPI 0.94 ● GREEN   │  Actual 126 h                  │  Reserve used 8/34 h  │
├──────────────────────────────────────────────────────────────────────────────┤
│  GATES        G0 ✅  G1 ✅  G2 ◔  G3 ○  G4 ○  G5 ○  G6 ○  G7 ○               │
├──────────────────────────────────────────────────────────────────────────────┤
│  PART MODELLING STATUS                            REQUIREMENTS TRACEABILITY   │
│  SEWCP-200 Cooling Plate    ██████████ 100% DAR✅  Total          142         │
│  SEWCP-400 Support Ring     ██████████ 100% DAR✅  Closed          89  (63%)  │
│  SEWCP-300 Heater Plate     ██████████ 100% DAR✅  In work         38  (27%)  │
│  SEWCP-500 ESC              ███████░░░  70% ──     Open            15  (10%)  │
│  SEWCP-600 Lift Pins        ░░░░░░░░░░   0% ──     Gate target ≥60% ● MET     │
│  SEWCP-700 Alignment Pins   ██████████ 100% PR ✅                             │
│  SEWCP-800 Vacuum Port      ██████████ 100% PR ✅  ENGINEERING BUDGETS        │
│  SEWCP-900 RF Bracket       █████░░░░░  50% ──     Z stack RSS   ±0.069  ●    │
│  SEWCP-1000 Sensor Bracket  ░░░░░░░░░░   0% ──     Flatness RSS   34.6µm ●    │
│                                                    Thermal chain 0.122  ○     │
│  VALIDATORS         Clocking ✅ Keep-out ✅         Concentricity 0.137  ●     │
│                     Datum ✅   Design Rules ✅      RF shunt      435 Ω  ●     │
│                     Coverage 91%                   ● verified ○ pending      │
├──────────────────────────────────────────────────────────────────────────────┤
│  RISK        🔴 3   🟡 6   🟢 6      Movers: R-04 ↑ (mesa rebuild 48 s)       │
│  CHANGE      ECR-Q open 2  │  ECR-D open 0 ✅  │  Rev B backlog 4            │
│  OPEN ITEMS  OI-1 ✅ closed W3  OI-2 ✅ closed W5  OI-3/4/5 → P4             │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 11.2 Panel Specification

| Panel | Metrics | Source | RAG Rule |
|---|---|---|---|
| **Header** | Week, phase, next gate, days remaining | Plan + system date | Amber < 7 d to gate with open criteria |
| **Schedule** | SPI, CPI, earned/planned/actual hours, CP float, reserve consumed | `timelog.csv` vs WBS baseline | §9.1 thresholds |
| **Gates** | ✅ passed · ◔ in review · ○ pending · ❌ failed | Gate log | Red on any failed gate |
| **Part Modelling** | % complete and review state per part | Task tracker | Amber if a critical-path part < plan |
| **Validators** | Pass/fail per validator + test coverage | CI output | **Red on any failure — blocks merge** |
| **Traceability** | Total / closed / in-work / open, vs gate profile | `rtm.csv` | Red if below the gate profile |
| **Engineering Budgets** | The six budgets the spec asserts, with verified/pending state | `sedep.analysis` output | Red if any budget fails to close |
| **Risk** | Counts by RAG; movers since last week | `risks.yaml` | Red if any new exposure ≥ 15 |
| **Change** | Open ECR-Q, ECR-D, Rev B backlog depth | Issue labels | **Red on any open ECR-D** |
| **Open Items** | OI-1…OI-5 status | Open Item Log | Red if a blocking OI is past its need date |

### 11.3 Design Notes

- **The Engineering Budgets panel is the most important on the dashboard.** Schedule and effort measure activity; the budgets measure whether the product still works. A program that is green on SPI and red on the thermal chain is failing, and the layout must make that impossible to miss.
- **Any open ECR-D forces the Change panel red regardless of every other metric**, because an open specification defect means the baseline is not what the models are being built to.
- The dashboard is **generated, never hand-edited.** A hand-maintained dashboard reports the state its author believes; a generated one reports the state of the repository.
- Refresh on every push to `main` plus a Monday scheduled run, so the weekly view is current even in an idle week.

---

**END OF SEDEP-PMP-001**

*Companion document: SEDEP-PMP-002 — Digital Engineering Infrastructure & Release Plan (GitHub structure, Engineering Notebook, Fusion 360 hierarchy, Python modules, documentation release plan, resume deliverables).*
