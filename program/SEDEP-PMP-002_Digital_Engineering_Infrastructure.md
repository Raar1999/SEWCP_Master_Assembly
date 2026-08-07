# SEDEP-PMP-002 — Digital Engineering Infrastructure & Release Plan

**Program:** SEDEP — Semiconductor Equipment Digital Engineering Platform
**Product Baseline:** SEWCP Engineering Specification Set, Rev A (Vol 00–09) — **FROZEN**
**Plan Revision:** 1.0
**Issued:** 2026-08-07
**Companion to:** SEDEP-PMP-001 Program Management Plan

---

## 0. Purpose

This document defines the infrastructure the program executes on: repository structure, notebook discipline, CAD hierarchy, software architecture, documentation control, and the closeout deliverables. It is the **how it is organised** to SEDEP-PMP-001's **what is done when**.

**Governing principle: single source of truth.** Every number in this program originates in the frozen specification, flows into the parameter master, and is consumed by CAD, analysis, and drawings. **No number is ever typed twice.** Every structure below exists to enforce that.

---

## 1. GitHub Repository Structure

**Repository:** `sewcp-sedep` · **Default branch:** `main` (protected) · **Visibility:** public at M8

```
sewcp-sedep/
│
├── README.md                          # Landing page: dashboard embed, quick nav, program status
├── LICENSE                            # MIT (code) / CC-BY-4.0 (documentation)
├── CONTRIBUTING.md                    # Branch model, PR gates, commit conventions
├── CODEOWNERS                         # spec/** requires Design Authority approval
├── CHANGELOG.md                       # Release history, keyed to milestone tags
├── pyproject.toml                     # Package metadata, tool config
│
├── .github/
│   ├── workflows/
│   │   ├── validate.yml               # Validator suite — BLOCKING on PR
│   │   ├── test.yml                   # Unit tests + coverage gate (85%)
│   │   ├── dashboard.yml              # Regenerate dashboard on push to main + Monday cron
│   │   └── docs.yml                   # Build and publish documentation site
│   ├── ISSUE_TEMPLATE/
│   │   ├── ecr-query.md               # ECR-Q — specification ambiguity
│   │   ├── ecr-defect.md              # ECR-D — specification defect (BLOCKING)
│   │   ├── rev-b-backlog.md           # Improvement ideas — parked, never implemented
│   │   └── risk.md                    # New risk entry
│   └── pull_request_template.md       # Gate checklist, RTM impact, review type
│
├── spec/                              # ═══ FROZEN — Rev A — CODEOWNERS PROTECTED ═══
│   ├── README.md
│   ├── 00_SEWCP-ENG-001_Architecture_and_Interface_Control.md
│   ├── 01_SEWCP-200_Cooling_Plate.md
│   ├── 02_SEWCP-300_Heater_Plate.md
│   ├── 03_SEWCP-400_Chuck_Support_Ring.md
│   ├── 04_SEWCP-500_Electrostatic_Chuck.md
│   ├── 05_SEWCP-600_Lift_Pins.md
│   ├── 06_SEWCP-700_Alignment_Pins.md
│   ├── 07_SEWCP-800_Vacuum_Port.md
│   ├── 08_SEWCP-900_RF_Feedthrough_Bracket.md
│   └── 09_SEWCP-1000_Temperature_Sensor_Bracket.md
│
├── program/                           # Program management artefacts
│   ├── SEDEP-PMP-001_Program_Management_Plan.md
│   ├── SEDEP-PMP-002_Digital_Engineering_Infrastructure.md
│   ├── wbs.csv                        # Machine-readable WBS: id, task, hours, predecessor, review
│   ├── milestones.yaml                # Gate definitions, dates, acceptance criteria
│   ├── risks.yaml                     # Risk register — dashboard source
│   ├── open_items.md                  # OI-1…OI-5 status
│   ├── assumptions.md                 # FBA register and derived assumptions
│   ├── timelog.csv                    # Effort actuals — earned value source
│   └── gates/
│       ├── G0_baseline_freeze.md      # Agenda, evidence, disposition, actions
│       └── … G1 … G7
│
├── params/                            # ═══ SINGLE SOURCE OF TRUTH ═══
│   ├── README.md                      # Rule: every value cites volume + table
│   ├── global.yaml                    # Datums, clocking map, Z stack, materials
│   ├── requirements.yaml              # All numbered functional requirements
│   ├── dimensions.yaml                # All critical dimensions, by criticality
│   ├── design_rules.yaml              # DR-1…DR-13 with predicates
│   ├── parts/
│   │   ├── SEWCP-200_cooling_plate.yaml
│   │   ├── SEWCP-300_heater_plate.yaml
│   │   ├── SEWCP-400_support_ring.yaml
│   │   ├── SEWCP-500_esc.yaml
│   │   ├── SEWCP-600_lift_pin.yaml
│   │   ├── SEWCP-700_alignment_pin.yaml
│   │   ├── SEWCP-800_vacuum_port.yaml
│   │   ├── SEWCP-900_rf_bracket.yaml
│   │   └── SEWCP-1000_sensor_bracket.yaml
│   └── generated/                     # Fusion user-parameter CSVs — DO NOT EDIT
│
├── src/sedep/                         # Python package — see §4
│
├── tests/
│   ├── test_params/                   # Parameter integrity, units, source citations
│   ├── test_validators/
│   │   └── fixtures/                  # The 3 historical conflicts — regression guards
│   ├── test_analysis/                 # Back-validation against spec hand calculations
│   └── test_reports/
│
├── notebook/                          # Engineering Notebook — see §2
│
├── cad/
│   ├── README.md                      # Fusion hierarchy map — see §3
│   ├── exports/
│   │   ├── step/                      # SEWCP-200_revA.step …
│   │   ├── stl/
│   │   └── screenshots/               # Model conformance evidence
│   ├── conformance/                   # Per-part dimensional conformance reports
│   └── scripts/                       # Symlink → src/sedep/cad
│
├── drawings/
│   ├── parts/                         # SEWCP-200_revA.pdf + .dwg …
│   ├── assembly/
│   ├── icd/
│   ├── templates/
│   └── redlines/                      # Check markups + disposition log
│
├── analysis/
│   ├── SEDEP-RPT-001_tolerance_stack/
│   ├── SEDEP-RPT-002_thermal/
│   ├── SEDEP-RPT-003_structural/
│   ├── SEDEP-RPT-004_electrical_rf/
│   ├── SEDEP-RPT-005_flow/
│   └── SEDEP-RPT-006_open_item_closure/
│
├── traceability/
│   ├── rtm.csv                        # Requirement → part → feature → drawing → verification
│   └── rtm_report.md                  # Rendered, generated
│
├── manufacturing/
│   ├── rfq/
│   │   └── SEWCP-200/                 # drawing, step, material, finish, inspection
│   ├── supplier_capability.csv
│   ├── long_lead.md
│   ├── inspection_plans/
│   └── ATP_SEDEP-PRC-001.md           # T1–T21
│
├── dashboard/
│   ├── DASHBOARD.md                   # Generated — never hand-edited
│   └── history/                       # Weekly snapshots, for trend
│
└── portfolio/
    ├── renders/
    ├── one_pager.pdf
    ├── resume_bullets.md
    └── interview_pack.pdf
```

### 1.1 Branch and Commit Model

| Element | Rule |
|---|---|
| `main` | Protected. No direct push. PR + 1 approval + green CI. |
| Feature branches | `wbs/3.2-cooling-plate`, `analysis/5.2-thermal`, `drawing/6.2.1-cooling-plate` |
| Commit format | `[WBS-3.2.2] Route coolant serpentine within Ø60–Ø250 envelope` |
| Tags | `baseline/spec-revA` · `gate/G2` … · `release/v1.0` |
| **Blocking CI** | Validator suite, unit tests, coverage ≥ 85%. **A red validator cannot be merged.** |

### 1.2 Two Structural Decisions Worth Stating

**`spec/` is CODEOWNERS-protected and requires Design Authority approval to modify.** This makes the configuration control statement in SEDEP-PMP-001 §0.1 mechanically enforced rather than merely declared. Under normal execution the folder receives **zero commits** for the whole program.

**`params/` is the only place a dimension is written.** CAD reads generated CSVs, analysis imports the YAML, drawings inherit from the model. If a number needs to change, exactly one file changes and everything downstream follows. This is what makes the "no number typed twice" rule enforceable rather than aspirational.

---

## 2. Engineering Notebook Structure

The notebook is the program's contemporaneous record. It is **append-only**: entries are never edited after commit; corrections are made by a later entry referencing the earlier one. This preserves the evidentiary property of a bound paper notebook in a digital form.

```
notebook/
├── README.md                          # Conventions, entry template, numbering
├── INDEX.md                           # Generated: all entries, date, WBS, tags
│
├── entries/
│   ├── 2026/
│   │   ├── 2026-08-10_ENB-0001.md
│   │   ├── 2026-08-11_ENB-0002.md
│   │   └── …
│
├── decisions/                         # Architecture Decision Records
│   ├── ADR-001_parameter_master_format.md
│   ├── ADR-002_mesa_array_representation.md
│   ├── ADR-003_skeleton_model_strategy.md
│   └── …
│
├── calculations/                      # Numbered, independently reproducible
│   ├── CR-001_z_stack_as_modelled.md
│   ├── CR-002_thermal_chain_verification.md
│   ├── CR-003_monte_carlo_z_stack.md
│   └── …
│
├── queries/                           # ECR-Q log with DA rulings
│   └── ECRQ-001_ring_slot_depth_datum.md
│
├── redlines/
│   └── RL-001_SEWCP-200_check_markup.md
│
└── gate_records/
    └── G0_2026-08-14_disposition.md
```

### 2.1 Entry Template

```markdown
# ENB-0042 · 2026-09-22 · Lead Engineer

**WBS:** 3.2.2 — Coolant serpentine routing
**Phase:** P2  ·  **Hours:** 3.5  ·  **Tags:** cooling-plate, keep-out, validator

## Objective
Route the serpentine within Ø60–Ø250 satisfying all 8 keep-out classes.

## Work Performed
[What was actually done, in sequence]

## Results
[Measured/observed outcomes. Numbers, not adjectives.]

## Decisions
[Any choice made, with the reason. Promote to an ADR if it affects other tasks.]

## Issues Raised
[ECR-Q / ECR-D / risk. Reference the issue number.]

## Next
[The next concrete action.]

---
Entries are append-only. Corrections are issued as a new entry referencing this one.
```

### 2.2 Notebook Discipline

| Rule | Rationale |
|---|---|
| One entry per working session, minimum | Gaps > 5 working days fail acceptance criterion A8.3 |
| Entries committed same-day | A notebook written retrospectively is a report, not a record |
| **Numbers, not adjectives** | "Rebuild 48 s" not "rebuild is slow" — the record must be usable as evidence later |
| Decisions affecting other tasks → **ADR** | Keeps cross-cutting decisions findable outside the chronological stream |
| Calculations → numbered **CR**, independently reproducible | Analysis reports cite CR numbers; a reviewer can re-run any of them |
| Failures and dead ends recorded | The record of what did not work is the most valuable and most commonly discarded content |

### 2.3 Architecture Decision Record Format

Each ADR states: **Context** (what forced the decision) · **Options** considered · **Decision** · **Consequences** (including what this makes harder) · **Status** (Proposed / Accepted / Superseded by ADR-nnn).

ADRs are the mechanism that keeps modelling decisions from silently becoming design decisions. When a decision cannot be made without changing a released dimension, the ADR is closed and an **ECR-D is raised instead**.

---

## 3. Fusion 360 File Hierarchy

**Fusion Team Project:** `SEWCP_Master_Assembly`

```
SEWCP_Master_Assembly/                       [Fusion Team Project]
│
├── 00_REFERENCE/                            [Read-only — locked]
│   ├── SEWCP-100_BASE_PLATE_FROZEN          ★ REFERENCE ONLY — DO NOT EDIT
│   ├── REF_WAFER_300mm                        Ø300 × 0.775 envelope
│   └── REF_ROBOT_ENVELOPE                     End-effector sweep, 210° sector
│
├── 01_SKELETON/                             [Drives everything below]
│   ├── SKL_DATUM_FRAME                        Datum A plane, B/C axes, 0° clocking
│   ├── SKL_Z_STACK                            All 8 stack planes at nominal
│   └── SKL_CLOCKING_MAP                       All 10 feature families as construction geometry
│
├── 02_PARTS/
│   ├── SEWCP-200_COOLING_PLATE
│   ├── SEWCP-300_HEATER_PLATE
│   ├── SEWCP-301_CHOKE_WASHER
│   ├── SEWCP-400_SUPPORT_RING
│   ├── SEWCP-401_CLAMP_RING
│   ├── SEWCP-500_ESC
│   ├── SEWCP-500D_ESC_MESA_DETAIL           ↳ Full mesa array — drawing use only (R-04)
│   ├── SEWCP-600_LIFT_PIN
│   ├── SEWCP-601_LIFT_PIN_BUSHING
│   ├── SEWCP-700_ALIGNMENT_PIN
│   ├── SEWCP-801_VACUUM_PORT_BODY
│   ├── SEWCP-802_ORIFICE_RESTRICTOR
│   ├── SEWCP-804_VCR_STUB
│   ├── SEWCP-901_RF_STRAP
│   ├── SEWCP-902_RF_BRACKET
│   ├── SEWCP-904_DEPOSITION_SHROUD
│   ├── SEWCP-1000_PROBE_RETAINER
│   ├── SEWCP-1001_HARNESS_BRACKET
│   └── SEWCP-1002_SIDE_LOAD_CLIP
│
├── 03_SUBASSEMBLIES/
│   ├── SEWCP-350_ESC_HEATER_BONDED          Heater + bond layer + ESC (never separated)
│   ├── SEWCP-450_RING_COOLING_SUBASM        Vol 03 §10 Phase 1 inverted build
│   ├── SEWCP-800_VACUUM_PORT_ASM
│   ├── SEWCP-900_RF_BRACKET_ASM
│   └── SEWCP-650_LIFT_PIN_ASM
│
├── 04_MASTER_ASSEMBLY/
│   ├── SEWCP-000_MASTER_ASSEMBLY            ★ Top level
│   └── SEWCP-000M_MOTION_STUDY              Lift travel, DR-4 verification
│
├── 05_DRAWINGS/
│   ├── DWG_SEWCP-200 … DWG_SEWCP-1000
│   ├── DWG_SEWCP-000_ASSEMBLY
│   └── DWG_SEWCP-ICD
│
├── 06_SIMULATION/
│   ├── SIM_THERMAL_STEADY_300W
│   ├── SIM_THERMAL_TRANSIENT
│   ├── SIM_STRUCT_SUPPORT_RING_PRELOAD
│   ├── SIM_STRUCT_COOLING_PLATE_DEFLECTION
│   └── SIM_STRUCT_ESC_BOND_SHEAR
│
└── 07_EXPORTS/                              [Generated — mirrored to repo]
    ├── STEP/    PDF/    STL/    RENDERS/
```

### 3.1 Fusion Working Rules

| Rule | Reason |
|---|---|
| **Every part references `01_SKELETON` as an external linked design** | One skeleton edit propagates. Parts never carry their own datum construction. |
| **User parameters imported from `params/generated/`, never typed** | Enforces single source of truth at the CAD boundary |
| **Parameter names match the spec reference** — `CP_D02_thickness`, `EC_D04_mesa_height` | A parameter's name states where its value came from |
| **`SEWCP-100` is locked read-only, marked FROZEN in the description** | Mechanically prevents the one thing this program must not do |
| Distributed design (external references), not monolithic assembly | Parts stay independently versionable; enables PG-2 parallelism |
| **Fusion version milestones named to match gate tags** (`gate/G2`) | Ties CAD versions to the Git history |
| Mesa array carried in `SEWCP-500D` detail design only | Risk R-04 mitigation — master model uses a derived body |
| Joints: rigid at bolted, **slider at all 6 kinematic slots and 3 lift pins** | The joint scheme must express the constraint scheme, or the motion study proves nothing |
| STEP exported at each gate, committed to `cad/exports/step/` | Git holds the neutral geometry record; Fusion holds the parametric one |

---

## 4. Python Module Hierarchy

**Package:** `sedep` · **Layout:** `src/sedep/` · **Distribution:** editable install, `pyproject.toml`

```
src/sedep/
│
├── __init__.py
├── constants.py                    Physical constants, unit conversions
│
├── params/                         ═══ Load and resolve the parameter master ═══
│   ├── loader.py                   YAML → typed parameter objects
│   ├── schema.py                   Parameter schema; enforces units + source citation
│   ├── resolver.py                 Derived parameters (DR-3 H_ring, RSS chains)
│   ├── registry.py                 Global lookup by ID (CP-D02, EC-D04 …)
│   └── export.py                   → Fusion user-parameter CSV
│
├── validators/                     ═══ Geometric and rule conformance ═══
│   ├── clocking.py                 Angular/radial collision across feature families
│   ├── keepout.py                  Cooling Plate coolant envelope, 8 keep-out classes
│   ├── datum.py                    A/B/C frame declared; position callouts valid
│   ├── design_rules.py             Machine-checkable subset of DR-1…DR-13
│   ├── stackup.py                  Z-stack closure and continuity
│   └── report.py                   Structured pass/fail → CI
│
├── analysis/                       ═══ Engineering calculations ═══
│   ├── tolerance.py                Worst-case, RSS, Monte Carlo, Cpk
│   ├── thermal.py                  Resistance network solver; choke sensitivity
│   ├── electrostatic.py            d_eff, clamping pressure vs voltage
│   ├── paschen.py                  p·d evaluation across declared gaps
│   ├── rf.py                       Skin depth, strap R_ac, loop inductance, shunt C
│   ├── flow.py                     Reynolds, ΔP, convective h, choked orifice flow
│   ├── contact.py                  Hertzian contact, bolted joint preload
│   └── budgets.py                  Rolls all six budgets into a dashboard payload
│
├── cad/                            ═══ Fusion 360 API automation ═══
│   ├── connect.py                  API session, document handling
│   ├── parameters.py               Push parameter set into a design
│   ├── mesa_array.py               Ø0.8 @ 6.0 hex over Ø290 with keep-outs
│   ├── patterns.py                 Feature patterns from the clocking map
│   ├── conformance.py              Extract as-modelled dims → compare to spec
│   └── export.py                   STEP / PDF / STL / screenshot automation
│
├── bom/
│   ├── builder.py                  Indentured BOM from the assembly tree
│   ├── partnum.py                  Part-number scheme validation
│   └── reconcile.py                BOM quantities vs. specification volumes
│
├── traceability/
│   ├── rtm.py                      RTM build, update, closure metrics
│   └── coverage.py                 Requirement → artefact coverage gaps
│
├── reports/
│   ├── dashboard.py                Generates dashboard/DASHBOARD.md
│   ├── earned_value.py             SPI, CPI from timelog vs. WBS baseline
│   ├── conformance.py              Per-part dimensional conformance report
│   └── templates/                  Jinja templates for all generated documents
│
└── io/
    ├── yaml_io.py                  Round-trip preserving comments and citations
    ├── csv_io.py
    └── markdown.py                 Table rendering for generated documents
```

### 4.1 Module Responsibilities

| Package | Owns | Never does |
|---|---|---|
| `params` | Loading, validating, resolving, and exporting the parameter master | Compute engineering results |
| `validators` | Answering "does this conform?" | Change anything |
| `analysis` | Physics and mathematics | Read CAD or write files |
| `cad` | All Fusion API interaction | Contain engineering logic |
| `bom` / `traceability` | Structural bookkeeping | Compute or validate geometry |
| `reports` | Presentation only | Contain a calculation |
| `io` | Serialisation | Interpret content |

> **`analysis` has no file I/O and no CAD dependency.** It is pure functions over parameter objects. That is what makes it unit-testable against the specification's hand calculations — acceptance criterion **A2.1**, the single most important test in the program. If the calculation library cannot reproduce the numbers the specification asserts, the specification's numbers were never verified.

### 4.2 Test Strategy

| Layer | Approach | Gate |
|---|---|---|
| `analysis` | **Back-validation** — every function reproduces its spec hand calculation to 3 s.f. | A2.1, A2.2 |
| `validators` | Regression fixtures from the 3 historical conflicts; must reproduce and catch each | A2.3 |
| `params` | Schema, units, source-citation completeness | A2.4 |
| `cad` | Smoke tests only (API-dependent, not CI-runnable) | — |
| Coverage | ≥ 85% on `analysis` and `validators` | A2.6 |

---

## 5. Documentation Release Plan

### 5.1 Document Numbering

| Prefix | Class | Example |
|---|---|---|
| `SEWCP-ENG-nnn` | Engineering specification | SEWCP-ENG-005 — ESC (**frozen Rev A**) |
| `SEDEP-PMP-nnn` | Program management plan | SEDEP-PMP-001 |
| `SEDEP-RPT-nnn` | Analysis report | SEDEP-RPT-002 — Thermal |
| `SEDEP-PRC-nnn` | Procedure | SEDEP-PRC-001 — Assembly ATP |
| `SEWCP-nnn` | Drawing (part number = drawing number) | SEWCP-200 |
| `ENB-nnnn` / `ADR-nnn` / `CR-nnn` | Notebook, decision, calculation record | — |
| `ECRQ-nnn` / `ECRD-nnn` | Change request — query / defect | — |

### 5.2 Maturity Levels

| Level | Marking | Control | Who may change |
|---|---|---|---|
| **Draft** | `X1, X2, X3…` | None; watermarked DRAFT | Originator, freely |
| **Preliminary** | `P1, P2…` | Under review; changes logged | Originator, with review comments |
| **Released** | `A, B, C…` | **Change control — ECN required** | Nobody, without an approved ECN |
| **Superseded** | `A (SUPERSEDED)` | Archived, retained | — |

**Rule:** a document is Released only when it has passed its gate. **Nothing is Released before its gate; nothing survives its gate unreleased.**

### 5.3 Sign-Off Matrix

| Document class | Originator | Checker | Approver | Release |
|---|---|---|---|---|
| Engineering specification | — | — | — | **Frozen — no change permitted** |
| Program plan | PM | DA | PM | G0 |
| Parameter master | LE | DA | DA | G1 |
| Part model | LE | — | DA | G2 |
| Assembly model | LE | — | DA | G3 |
| Analysis report | AN | DA | DA | G4 |
| **Part drawing** | **LE** | **CK (≠ originator)** | **DA** | **G5** |
| Assembly drawing / ICD | LE | CK | DA | G5 |
| RFQ package / ATP | LE | — | DA | G6 |
| Portfolio deliverables | LE | — | DA | G7 |

### 5.4 Release Schedule

| Gate | Date | Documents Released |
|---|---|---|
| G0 | 2026-08-14 | SEDEP-PMP-001 Rev A · SEDEP-PMP-002 Rev A · RTM v0 · Assumptions Register |
| G1 | 2026-09-04 | Parameter master Rev A · Validator suite v1.0 · Calculation library v1.0 · Back-validation report |
| G2 | 2026-10-16 | 10 part models Rev A · 10 conformance reports · Validator clean-run report |
| G3 | 2026-10-30 | Master assembly Rev A · Interference report · DR-1 / DR-4 audit reports · BOM Rev A |
| G4 | 2026-11-13 | SEDEP-RPT-001…006 Rev A · OI closure memos |
| G5 | 2026-11-27 | **12 drawings Rev A** · Redline log · RTM 100% |
| G6 | 2026-12-04 | RFQ package Rev A · SEDEP-PRC-001 ATP Rev A · Inspection plans |
| G7 | 2026-12-11 | Release bundle `v1.0` · Closeout report · Portfolio set |

### 5.5 Change Control

```
Finding during execution
        │
        ├── Modelling clarification ──► Notebook entry ──► proceed          [LE]
        │
        ├── Improvement idea ─────────► Rev B backlog issue ──► PARKED      [LE]
        │                               (never implemented under this plan)
        │
        ├── ECR-Q  specification ─────► DA ruling ──► RTM note ──► proceed  [DA]
        │          ambiguity
        │
        └── ECR-D  specification ─────► STOP affected task
                   defect              ──► DA + PM assessment
                                       ──► re-gate affected phase
                                       ──► if geometry must change:
                                           NEW SPEC REVISION + RE-PLAN      [DA+PM]
```

**The Rev B backlog is a deliberate pressure-release valve.** Executing a specification one has just written generates a continuous stream of improvement ideas. Without somewhere legitimate for them to go, they leak into the models. The backlog captures them, dates them, and defers them — and becomes a genuine input to a future revision.

### 5.6 Distribution

| Audience | Access | Contents |
|---|---|---|
| Program team | Full repository | Everything |
| Suppliers | `manufacturing/rfq/<part>/` only | Drawing, STEP, material, finish, inspection |
| Public (from M8) | Public repository | All except `program/timelog.csv` |
| Portfolio reviewers | `README.md` + `portfolio/` | Curated entry path |

---

## 6. Final Resume Deliverables

> **Release condition:** each item below is authorised for use **only after its supporting milestone closes**. Every claim must be verifiable from the repository by a reader who has never spoken to the author. A bullet that cannot be traced to a committed artefact is not released.

### 6.1 Deliverable Set

| # | Deliverable | Format | Milestone | Purpose |
|---|---|---|---|---|
| P1 | Program one-pager | PDF, 1 page | M8 | Recruiter-facing summary |
| P2 | Resume bullet set | Markdown | M8 | Direct resume insertion |
| P3 | Interview asset pack | PDF, ~15 pages | M8 | Technical interview support |
| P4 | Repository landing README | Markdown | M8 | Public entry point |
| P5 | Render set | PNG / MP4 | M8 | Visual proof of work |
| P6 | Technical narrative | Markdown, ~1500 words | M8 | Long-form portfolio piece |
| P7 | Metrics sheet | CSV | M8 | Quantitative backing for every claim |

### 6.2 Program One-Pager — Required Content

1. **Title:** Semiconductor Electrostatic Wafer Chuck Platform — Design & Digital Engineering Execution
2. **One-line scope:** 300 mm bipolar electrostatic chuck pedestal for RF-biased plasma process equipment — full specification through released drawing set.
3. **Exploded render** with the five-part stack labelled
4. **Key engineering figures:** wafer plane 55.920 ± 0.150 mm · thermal chain 0.122 K/W · clamping 38.9 mbar at ±1500 V · shunt 435 Ω at 13.56 MHz · assembly leak < 1×10⁻⁹ mbar·L/s
5. **Scale:** 10 specification volumes · 10 released parts · 12 drawings · 6 analysis reports · 142 traced requirements · 13 design rules
6. **Three headline engineering decisions** (§6.4)
7. Repository link and QR code

### 6.3 Resume Bullet Set — Draft for Release at M8

Written to be **literally true on completion**, each traceable to a committed artefact:

> **Semiconductor Electrostatic Wafer Chuck Platform (SEWCP) — Lead Mechanical Design Engineer**
>
> - Authored a **10-volume, 142-requirement engineering specification** for a 300 mm bipolar electrostatic chuck pedestal — covering thermal, RF, vacuum, and tolerance architecture — and executed it to a **released 12-drawing manufacturing package** across an 8-gate, 18-week program.
> - Designed a **cooled-base / thermal-choke / trim-heater architecture** achieving a **0.122 K/W wafer-to-coolant chain**, sizing a deliberate 0.10 K/W titanium-standoff thermal break that gives the heater control authority a directly-coupled design cannot provide.
> - Closed a **wafer-plane tolerance stack to ±0.150 mm** where worst-case analysis failed by 3 µm, by introducing a single lap-to-fit component that converted a statistical argument into a deterministic assembly measurement — recovering **7× margin** without tightening six upstream part tolerances.
> - Derived **three mechanical requirements from Paschen breakdown analysis** — lift-pin bore engagement, backside-gas interlocking, and an RF pressure-window inhibit — identifying a hazard band that **increasing clearance makes worse**.
> - Architected the assembly so that **all uncertainty in a frozen upstream interface was absorbed by a single component**, reducing the program's most likely discrepancy from a 9-part redesign to a re-machining of one ceramic ring.
> - Built a **Python digital-engineering platform** (parameter master, geometric validator suite, engineering calculation library) enforcing single-source-of-truth from specification through CAD to drawings, with **85%+ test coverage back-validated against every hand calculation in the specification**.
> - Ran the program as **8 formal design gates** with binary acceptance criteria, a 15-item risk register, and requirements traceability closed to **100%** at drawing release.

### 6.4 Interview Asset Pack — Structure

| Section | Content |
|---|---|
| 1 | Program overview, stack diagram, scope |
| 2 | **Architecture decisions** — thermal choke · frozen-interface firewall · lap-to-fit stack closure |
| 3 | **The three design corrections made during specification** — ring wall vs. bolt geometry · RF strap aperture constraint · RF land / sensor port collision. *Presented as evidence of engineering judgement, not as errors.* |
| 4 | **Quantitative deep-dives** — clamping force derivation · Knudsen/backside-gas physics · Paschen analysis · skin effect and strap inductance · bond shear strain |
| 5 | **Failure mode reasoning** — the four RPN-180 modes and why detection difficulty, not probability, drove the mitigations |
| 6 | **Program execution** — WBS, gates, critical path, earned value, risk register |
| 7 | **Digital engineering** — parameter master, validators, back-validation strategy |
| 8 | Anticipated challenge questions with prepared answers |

### 6.5 Metrics Sheet

| Metric | Value | Source |
|---|---|---|
| Specification volumes | 10 | `spec/` |
| Traced requirements | 142 | `traceability/rtm.csv` |
| Design rules defined | 13 | `params/design_rules.yaml` |
| Released parts | 10 | `cad/exports/step/` |
| Released drawings | 12 | `drawings/` |
| Analysis reports | 6 | `analysis/` |
| Program gates | 8 | `program/gates/` |
| WBS tasks / steps | 42 / 168 | `program/wbs.csv` |
| Estimated effort | 280 h | `program/wbs.csv` |
| Risks managed | 15 | `program/risks.yaml` |
| Test coverage (`analysis`, `validators`) | ≥ 85% | CI |
| Requirements closure at release | 100% | RTM |

### 6.6 What Makes This Portfolio Piece Defensible

Three properties distinguish it from a CAD showcase, and the deliverables above are structured to make each visible in under two minutes:

**It reasons from physics to geometry.** Mesa height is toleranced to ±3 µm because it contributes 40% of the effective electrical gap. Bond thickness is 0.40 mm because 0.25 mm gives 88% shear strain. The strap is 50 mm wide because a wider one will not pass a frozen aperture. Every unusual number has a derivation behind it.

**It shows judgement under constraint, including corrections.** Section 3 of the interview pack deliberately presents the three mid-specification design corrections. A specification with no corrections was either trivial or unexamined; showing the ring redesign — where the obvious thin-wall-with-through-bolts scheme destroyed the two properties the thin wall existed for — demonstrates more than a clean result would.

**It was executed under configuration control.** The specification was frozen, then built to without modification, with changes routed through a defined process and a Rev B backlog holding the deferred improvements. That discipline — building what was specified rather than what became interesting — is the thing production engineering organisations actually screen for.

---

**END OF SEDEP-PMP-002**

*Companion document: SEDEP-PMP-001 — Program Management Plan (WBS, dependencies, parallelism, reviews, milestones, deliverables, acceptance criteria, risk register, dashboard).*
