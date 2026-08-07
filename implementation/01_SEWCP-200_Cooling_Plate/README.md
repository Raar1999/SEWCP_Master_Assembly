# SEWCP-200 — Cooling Plate

**Component:** 01 of 09 · **Part Number:** SEWCP-200 · **WBS:** 3.2
**Status:** CAD package Rev X1 issued - ON HOLD (4 open ECR-D)

> **PLACEHOLDER.** This directory was created during Release 0.1 infrastructure
> preparation. It contains no implementation instructions and no engineering
> content. Populating it is a Phase P2 activity under WBS 3.2.

---

## Governing Specification

**FROZEN — read only.** All geometry, tolerances, materials and interfaces for
this component are defined in:

- [`spec/01_SEWCP-200_Cooling_Plate.md`](../../spec/01_SEWCP-200_Cooling_Plate.md) — component specification
- [`spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md`](../../spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md) — datums, clocking map, Z-stack, design rules DR-1…DR-13

No dimension, interface or material may be introduced here that is not traceable
to those documents.

---

## Directory Purpose

| Path | Holds | Status |
|---|---|---|
| `cad/` | CAD implementation package, modelling records, conformance evidence | Empty |
| `params/` | Component parameter file, Fusion user-parameter export | Empty |
| `drawings/` | Drawing sheets, redlines, check records | Empty |
| `verification/` | Dimensional conformance, inspection and analysis records | Empty |

---

## Entry Conditions

This directory is not worked until:

1. Program gate **G1** (Digital Foundation Review) has passed.
2. The parameter master for SEWCP-200 exists under `params/parts/`.
3. WBS 3.2 predecessors are complete per SEDEP-PMP-001 §3.1.

---

## Change Control

Governed by SEDEP-PMP-001 §0.1. Any discrepancy found against the frozen
specification is raised as an **ECR**, never resolved at working level.
