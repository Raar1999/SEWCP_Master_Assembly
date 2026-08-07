# Release 0.1.0 — Manifest

**Release:** 0.1.0 · **Tag:** `v0.1.0` · **Date:** 2026-08-07
**Scope:** Repository infrastructure baseline
**Authorised by:** `RELEASE_0.1_READINESS_REPORT.md`

---

## 1. Scope Statement

Release 0.1 establishes version control and repository structure for the SEWCP program.

**Explicitly excluded from this release:**
- No engineering content created, modified, reviewed, or decided.
- No CAD work.
- No implementation instructions.
- No specification change of any kind.

The engineering baseline (`spec/`, SEWCP Rev A, Volumes 00–09) was **migrated unchanged** and remains frozen.

---

## 2. Contents

### 2.1 Repository Governance
| File | Status |
|---|---|
| `README.md` | New |
| `INDEX.md` | New |
| `CHANGELOG.md` | New |
| `CONTRIBUTING.md` | New — placeholder, policy sections binding |
| `LICENSE` | New — **placeholder, unresolved** |
| `.gitignore` | New — Fusion 360 / Python / VS Code / OS / CAE |

### 2.2 Engineering Baseline — migrated, unchanged
| File | Origin |
|---|---|
| `spec/README.md` | `docs/README.md` |
| `spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md` | `docs/` |
| `spec/01_SEWCP-200_Cooling_Plate.md` | `docs/` |
| `spec/02_SEWCP-300_Heater_Plate.md` | `docs/` |
| `spec/03_SEWCP-400_Chuck_Support_Ring.md` | `docs/` |
| `spec/04_SEWCP-500_Electrostatic_Chuck.md` | `docs/` |
| `spec/05_SEWCP-600_Lift_Pins.md` | `docs/` |
| `spec/06_SEWCP-700_Alignment_Pins.md` | `docs/` |
| `spec/07_SEWCP-800_Vacuum_Port.md` | `docs/` |
| `spec/08_SEWCP-900_RF_Feedthrough_Bracket.md` | `docs/` |
| `spec/09_SEWCP-1000_Temperature_Sensor_Bracket.md` | `docs/` |

### 2.3 Program Documents — unchanged, in place
| File |
|---|
| `program/SEDEP-PMP-001_Program_Management_Plan.md` |
| `program/SEDEP-PMP-002_Digital_Engineering_Infrastructure.md` |

### 2.4 Implementation Structure
| Path | Contents |
|---|---|
| `implementation/01_SEWCP-200_Cooling_Plate/` | README + 4 sub-dirs + migrated CAD package |
| `implementation/02_SEWCP-300_Heater_Plate/` | README + 4 sub-dirs |
| `implementation/03_SEWCP-400_Chuck_Support_Ring/` | README + 4 sub-dirs |
| `implementation/04_SEWCP-500_Electrostatic_Chuck/` | README + 4 sub-dirs |
| `implementation/05_SEWCP-600_Lift_Pins/` | README + 4 sub-dirs |
| `implementation/06_SEWCP-700_Alignment_Pins/` | README + 4 sub-dirs |
| `implementation/07_SEWCP-800_Vacuum_Port/` | README + 4 sub-dirs |
| `implementation/08_SEWCP-900_RF_Feedthrough_Bracket/` | README + 4 sub-dirs |
| `implementation/09_SEWCP-1000_Temperature_Sensor_Bracket/` | README + 4 sub-dirs |

### 2.5 Traceability
| File |
|---|
| `traceability/DOCUMENT_DEPENDENCY_MAP.md` |
| `traceability/DOCUMENT_TRACEABILITY_MATRIX.md` |

### 2.6 Release Control
| File |
|---|
| `releases/README.md` |
| `releases/TAGS.md` |
| `releases/v0.1/MANIFEST.md` (this file) |
| `releases/v0.1/RELEASE_0.1_READINESS_REPORT.md` |

### 2.7 CAD Structure
| Path | Purpose |
|---|---|
| `cad/fusion/` | Fusion working files — **ignored by git**, cloud-versioned |
| `cad/archive/` | Superseded neutral geometry, retained |
| `cad/exports/{step,stl,screenshots}` | Neutral geometry record |
| `cad/conformance/` | Dimensional conformance reports |
| `cad/scripts/` | CAD automation |

---

## 3. Integrity Statement

Each assertion below states its **verification method**. Evidence is recorded against the `v0.1.0` release commit and is reproducible from the repository.

| Assertion | Verification Method |
|---|---|
| Specification content unmodified | 11 files relocated by `Move-Item` only. No write operation was performed against any path under `spec/` at any point. Reproducible: compare `spec/` blobs against the `baseline/spec-revA` tag. |
| No AI attribution added | Inspect the release commit message and body. Repository policy P-1. |
| No `Co-authored-by` trailer | Inspect the release commit trailers. Repository policy P-2. |
| Git author unmodified | No `git config` write was executed at any point. Pre-existing global identity used unchanged. Repository policy P-3. |
| No engineering decision made | Task scope limited to filesystem and version-control operations. No `spec/` content was read for engineering purposes, interpreted, or acted upon. |

**Verification status:** performed and recorded in [`RELEASE_0.1_READINESS_REPORT.md`](RELEASE_0.1_READINESS_REPORT.md) §3, checks V-11 through V-14.

> **Note.** An earlier draft of this section asserted "commit inspected" before any commit existed. That was identified as blocking finding **F-02** by independent audit and corrected. The finding and its remediation are recorded in the readiness report §4 rather than removed.

---

## 4. Known Unresolved

| ID | Item | Blocks |
|---|---|---|
| C-4 | `LICENSE` placeholder unresolved | Public / external release |
| C-5 | CI workflows not populated | Automated verification |
| C-1…C-3 | `CONTRIBUTING.md` sections pending ratification | Nothing — defaults documented |

**Pre-existing engineering findings, carried forward, not introduced by this release:**

| ID | Against | Recorded In |
|---|---|---|
| ECR-D-001…004 | Frozen baseline | `implementation/01_SEWCP-200_Cooling_Plate/SEWCP-200_CAD_Implementation_Package.md` §12 |
| ECR-Q-001…008 | Frozen baseline | Same, §12.2 |
