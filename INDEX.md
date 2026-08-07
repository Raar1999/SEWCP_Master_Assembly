# Master Document Index

**Generated:** 2026-08-07 · **Release:** 0.1.0 · **Documents indexed:** 14

Every controlled document in this repository. Verified reachable from the repository root.

---

## 1. Engineering Specification — `spec/` — **FROZEN, Rev A**

| Vol | Doc No. | Part No. | Title | File |
|---|---|---|---|---|
| — | — | — | Specification set index | [`spec/README.md`](spec/README.md) |
| 00 | SEWCP-ENG-001 | — | Architecture & Interface Control | [`spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md`](spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md) |
| 01 | SEWCP-ENG-002 | SEWCP-200 | Cooling Plate | [`spec/01_SEWCP-200_Cooling_Plate.md`](spec/01_SEWCP-200_Cooling_Plate.md) |
| 02 | SEWCP-ENG-003 | SEWCP-300 | Heater Plate | [`spec/02_SEWCP-300_Heater_Plate.md`](spec/02_SEWCP-300_Heater_Plate.md) |
| 03 | SEWCP-ENG-004 | SEWCP-400 | Chuck Support Ring | [`spec/03_SEWCP-400_Chuck_Support_Ring.md`](spec/03_SEWCP-400_Chuck_Support_Ring.md) |
| 04 | SEWCP-ENG-005 | SEWCP-500 | Electrostatic Chuck | [`spec/04_SEWCP-500_Electrostatic_Chuck.md`](spec/04_SEWCP-500_Electrostatic_Chuck.md) |
| 05 | SEWCP-ENG-006 | SEWCP-600 | Lift Pins | [`spec/05_SEWCP-600_Lift_Pins.md`](spec/05_SEWCP-600_Lift_Pins.md) |
| 06 | SEWCP-ENG-007 | SEWCP-700 | Alignment Pins | [`spec/06_SEWCP-700_Alignment_Pins.md`](spec/06_SEWCP-700_Alignment_Pins.md) |
| 07 | SEWCP-ENG-008 | SEWCP-800 | Vacuum Port Assembly | [`spec/07_SEWCP-800_Vacuum_Port.md`](spec/07_SEWCP-800_Vacuum_Port.md) |
| 08 | SEWCP-ENG-009 | SEWCP-900 | RF Feedthrough Bracket | [`spec/08_SEWCP-900_RF_Feedthrough_Bracket.md`](spec/08_SEWCP-900_RF_Feedthrough_Bracket.md) |
| 09 | SEWCP-ENG-010 | SEWCP-1000 | Temperature Sensor Bracket | [`spec/09_SEWCP-1000_Temperature_Sensor_Bracket.md`](spec/09_SEWCP-1000_Temperature_Sensor_Bracket.md) |

> **SEWCP-100 Base Plate is frozen and has no specification volume** — it is an external input, declared via Frozen Baseline Assumptions FBA-1…FBA-8 in Volume 00 §2.

---

## 2. Program Management — `program/`

| Doc No. | Title | File |
|---|---|---|
| SEDEP-PMP-001 | Program Management Plan | [`program/SEDEP-PMP-001_Program_Management_Plan.md`](program/SEDEP-PMP-001_Program_Management_Plan.md) |
| SEDEP-PMP-002 | Digital Engineering Infrastructure & Release Plan | [`program/SEDEP-PMP-002_Digital_Engineering_Infrastructure.md`](program/SEDEP-PMP-002_Digital_Engineering_Infrastructure.md) |

---

## 3. Implementation — `implementation/`

| # | Component | Package | Status |
|---|---|---|---|
| 01 | SEWCP-200 Cooling Plate | [`SEWCP-200_CAD_Implementation_Package.md`](implementation/01_SEWCP-200_Cooling_Plate/SEWCP-200_CAD_Implementation_Package.md) | **Rev X1 — issued with HOLD** |
| 02 | SEWCP-300 Heater Plate | — | Not started |
| 03 | SEWCP-400 Chuck Support Ring | — | Not started |
| 04 | SEWCP-500 Electrostatic Chuck | — | Not started |
| 05 | SEWCP-600 Lift Pins | — | Not started |
| 06 | SEWCP-700 Alignment Pins | — | Not started |
| 07 | SEWCP-800 Vacuum Port | — | Not started |
| 08 | SEWCP-900 RF Feedthrough Bracket | — | Not started |
| 09 | SEWCP-1000 Temperature Sensor Bracket | — | Not started |

---

## 4. Traceability — `traceability/`

| Title | File |
|---|---|
| Document Dependency Map | [`traceability/DOCUMENT_DEPENDENCY_MAP.md`](traceability/DOCUMENT_DEPENDENCY_MAP.md) |
| Document Traceability Matrix | [`traceability/DOCUMENT_TRACEABILITY_MATRIX.md`](traceability/DOCUMENT_TRACEABILITY_MATRIX.md) |

---

## 5. Releases — `releases/`

| Title | File |
|---|---|
| Release index | [`releases/README.md`](releases/README.md) |
| Tag scheme | [`releases/TAGS.md`](releases/TAGS.md) |
| Release 0.1 manifest | [`releases/v0.1/MANIFEST.md`](releases/v0.1/MANIFEST.md) |
| Release 0.1 readiness report | [`releases/v0.1/RELEASE_0.1_READINESS_REPORT.md`](releases/v0.1/RELEASE_0.1_READINESS_REPORT.md) |

---

## 6. Repository Governance — root

| Title | File |
|---|---|
| Repository landing page | [`README.md`](README.md) |
| Contribution rules and repository policy | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Changelog | [`CHANGELOG.md`](CHANGELOG.md) |
| License (**placeholder — unresolved**) | [`LICENSE`](LICENSE) |

---

## Numbering Conventions

| Series | Range in use | Meaning |
|---|---|---|
| `SEWCP-ENG-nnn` | 001–010 | Engineering specification volumes |
| `SEWCP-nnn` | 100–1000 | Part numbers |
| `SEDEP-PMP-nnn` | 001–002 | Program management plans |
| `SEWCP-nnn-CAD-nnn` | 200-CAD-001 | CAD implementation packages |
| `ECR-D-nnn` / `ECR-Q-nnn` | 001–004 / 001–008 | Change requests: defect / query |
| Volume prefix `NN_` | 00–09 | Spec file ordering |

**Documented exception:** Volume 00 is filed as `00_SEWCP-ENG-001_…` using its document number, whereas Volumes 01–09 use their part number. This is correct — Volume 00 governs the assembly and has no part number.
