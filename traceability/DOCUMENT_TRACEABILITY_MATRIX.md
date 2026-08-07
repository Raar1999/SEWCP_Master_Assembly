# Document Traceability Matrix

**Generated:** 2026-08-07 · **Release:** 0.1.0 · **Level:** document

Traces every controlled document to its identifier, location, governing authority, and lifecycle state.

**Scope limit:** document level. A requirement-level RTM (requirement → part → feature → drawing → verification) is a Phase P0 deliverable per SEDEP-PMP-001 WBS 1.2.4 and is **not** produced here. Producing one would require reading and interpreting specification content, which is outside this task's authority.

---

## 1. Matrix

| ID | Doc No. | Title | Path | Rev | State | Governed By | Governs | Change Control |
|---|---|---|---|---|---|---|---|---|
| D-01 | — | Specification set index | `spec/README.md` | A | Frozen | Design Authority | Vol 00–09 navigation | Spec revision |
| D-02 | SEWCP-ENG-001 | Architecture & Interface Control | `spec/00_…md` | A | **Frozen** | Design Authority | All 9 component volumes | Spec revision |
| D-03 | SEWCP-ENG-002 | Cooling Plate | `spec/01_…md` | A | **Frozen** | SEWCP-ENG-001 | SEWCP-200 | Spec revision |
| D-04 | SEWCP-ENG-003 | Heater Plate | `spec/02_…md` | A | **Frozen** | SEWCP-ENG-001 | SEWCP-300, -301 | Spec revision |
| D-05 | SEWCP-ENG-004 | Chuck Support Ring | `spec/03_…md` | A | **Frozen** | SEWCP-ENG-001 | SEWCP-400, -401 | Spec revision |
| D-06 | SEWCP-ENG-005 | Electrostatic Chuck | `spec/04_…md` | A | **Frozen** | SEWCP-ENG-001 | SEWCP-500 | Spec revision |
| D-07 | SEWCP-ENG-006 | Lift Pins | `spec/05_…md` | A | **Frozen** | SEWCP-ENG-001 | SEWCP-600, -601, -602 | Spec revision |
| D-08 | SEWCP-ENG-007 | Alignment Pins | `spec/06_…md` | A | **Frozen** | SEWCP-ENG-001 | SEWCP-700 | Spec revision |
| D-09 | SEWCP-ENG-008 | Vacuum Port Assembly | `spec/07_…md` | A | **Frozen** | SEWCP-ENG-001 | SEWCP-800…-804 | Spec revision |
| D-10 | SEWCP-ENG-009 | RF Feedthrough Bracket | `spec/08_…md` | A | **Frozen** | SEWCP-ENG-001 | SEWCP-900…-904 | Spec revision |
| D-11 | SEWCP-ENG-010 | Temperature Sensor Bracket | `spec/09_…md` | A | **Frozen** | SEWCP-ENG-001 | SEWCP-1000…-1003 | Spec revision |
| D-12 | SEDEP-PMP-001 | Program Management Plan | `program/…001…md` | 1.0 | Released | Program Manager | Program execution, gates G0–G7 | PR |
| D-13 | SEDEP-PMP-002 | Digital Engineering Infrastructure | `program/…002…md` | 1.0 | Released | Program Manager | Repository, CAD, software, release | PR |
| D-14 | SEWCP-200-CAD-001 | Cooling Plate CAD Implementation Package | `implementation/01_…/…md` | X1 | **Draft — HOLD** | SEDEP-PMP-001 §0.1 | SEWCP-200 modelling | PR |

---

## 2. Part Number Coverage

| Part No. | Component | Specification | Implementation Package |
|---|---|---|---|
| SEWCP-100 | Base Plate | **None — frozen external input** (FBA-1…FBA-8) | N/A |
| SEWCP-200 | Cooling Plate | D-03 ✔ | D-14 (Rev X1, HOLD) |
| SEWCP-300 / -301 | Heater Plate / Choke Washer | D-04 ✔ | Not started |
| SEWCP-400 / -401 | Support Ring / Clamp Ring | D-05 ✔ | Not started |
| SEWCP-500 | Electrostatic Chuck | D-06 ✔ | Not started |
| SEWCP-600 / -601 / -602 | Lift Pin / Bushing / Yoke IF | D-07 ✔ | Not started |
| SEWCP-700 | Alignment Pin | D-08 ✔ | Not started |
| SEWCP-800 … -804 | Vacuum Port Assembly | D-09 ✔ | Not started |
| SEWCP-900 … -904 | RF Bracket Assembly | D-10 ✔ | Not started |
| SEWCP-1000 … -1003 | Temperature Sensor Bracket | D-11 ✔ | Not started |

**Specification coverage: 9 of 9 in-scope components — 100%.**
**Implementation coverage: 1 of 9 started, 0 of 9 released — 0%.**

---

## 3. Lifecycle State Summary

| State | Count | Documents |
|---|---|---|
| Frozen | 11 | D-01 … D-11 |
| Released | 2 | D-12, D-13 |
| Draft (HOLD) | 1 | D-14 |
| **Total** | **14** | |

---

## 4. Open Change Requests Against the Baseline

Recorded for traceability. **These are pre-existing engineering findings raised during Cooling Plate CAD preparation. No engineering assessment is made or restated here.**

| ID | Class | Raised In | Against | State |
|---|---|---|---|---|
| ECR-D-001 | Defect | D-14 §12.1 | D-03, D-05, D-08 | Open |
| ECR-D-002 | Defect | D-14 §12.1 | D-03 | Open |
| ECR-D-003 | Defect | D-14 §12.1 | D-03 | Open |
| ECR-D-004 | Defect | D-14 §12.1 | D-03, D-02 | Open |
| ECR-Q-001…008 | Query | D-14 §12.2 | D-02, D-03, D-10 | Open |

**Documents carrying open defects:** D-02, D-03, D-05, D-08, D-10.
**D-03 (Cooling Plate) carries the highest defect count — 4.**

---

## 5. Verification

| # | Check | Result |
|---|---|---|
| T-01 | Every document has a unique ID | **PASS** — 14/14 |
| T-02 | Every document has a lifecycle state | **PASS** — 14/14 |
| T-03 | Every document has a governing authority | **PASS** — 14/14 |
| T-04 | Every in-scope part number has a specification | **PASS** — 9/9 |
| T-05 | No duplicate document numbers | **PASS** |
| T-06 | No orphan documents | **PASS** |
| T-07 | Every path resolves | **PASS** — 14/14 |
