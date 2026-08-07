# implementation/

Per-component implementation packages. One directory per in-scope component.

> **Structure only.** All directories were created during Release 0.1 infrastructure preparation and contain placeholders. No implementation instructions exist here except the Cooling Plate CAD package, which was migrated from `cad/` unchanged.

---

## Components

| # | Directory | Part No. | Specification | WBS | Status |
|---|---|---|---|---|---|
| 01 | `01_SEWCP-200_Cooling_Plate/` | SEWCP-200 | [Vol 01](../spec/01_SEWCP-200_Cooling_Plate.md) | 3.2 | **CAD pkg Rev X1 — HOLD** |
| 02 | `02_SEWCP-300_Heater_Plate/` | SEWCP-300 | [Vol 02](../spec/02_SEWCP-300_Heater_Plate.md) | 3.4 | Not started |
| 03 | `03_SEWCP-400_Chuck_Support_Ring/` | SEWCP-400 | [Vol 03](../spec/03_SEWCP-400_Chuck_Support_Ring.md) | 3.3 | Not started |
| 04 | `04_SEWCP-500_Electrostatic_Chuck/` | SEWCP-500 | [Vol 04](../spec/04_SEWCP-500_Electrostatic_Chuck.md) | 3.5 | Not started |
| 05 | `05_SEWCP-600_Lift_Pins/` | SEWCP-600 | [Vol 05](../spec/05_SEWCP-600_Lift_Pins.md) | 3.6 | Not started |
| 06 | `06_SEWCP-700_Alignment_Pins/` | SEWCP-700 | [Vol 06](../spec/06_SEWCP-700_Alignment_Pins.md) | 3.7 | Not started |
| 07 | `07_SEWCP-800_Vacuum_Port/` | SEWCP-800 | [Vol 07](../spec/07_SEWCP-800_Vacuum_Port.md) | 3.8 | Not started |
| 08 | `08_SEWCP-900_RF_Feedthrough_Bracket/` | SEWCP-900 | [Vol 08](../spec/08_SEWCP-900_RF_Feedthrough_Bracket.md) | 3.9 | Not started |
| 09 | `09_SEWCP-1000_Temperature_Sensor_Bracket/` | SEWCP-1000 | [Vol 09](../spec/09_SEWCP-1000_Temperature_Sensor_Bracket.md) | 3.10 | Not started |

**SEWCP-100 Base Plate is frozen and out of scope.** It has no implementation directory.

---

## Naming Convention

```
<NN>_<PART-NUMBER>_<Component_Name>/
```

`NN` matches the governing specification volume number, so `implementation/` and `spec/` sort into the same order.

Component names follow the **specification** part name, not colloquial usage — e.g. `Chuck_Support_Ring`, not `Support_Ring`.

---

## Standard Sub-Structure

Every component directory contains:

| Sub-dir | Holds |
|---|---|
| `cad/` | CAD implementation package, modelling records, conformance evidence |
| `params/` | Component parameter file, Fusion user-parameter export |
| `drawings/` | Drawing sheets, redlines, check records |
| `verification/` | Dimensional conformance, inspection and analysis records |

---

## Rules

1. Nothing in this tree may introduce a dimension, interface, or material not traceable to `spec/`.
2. Discrepancies against the frozen baseline are raised as **ECR**, never resolved here.
3. Work does not begin on a component until program gate **G1** has passed and its parameter master exists.
