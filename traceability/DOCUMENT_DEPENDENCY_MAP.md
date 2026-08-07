# Document Dependency Map

**Generated:** 2026-08-07 · **Release:** 0.1.0 · **Scope:** document-level only

Records which documents depend on which. **Document-level relationships only — this is not a requirements traceability matrix.** No document content was read for engineering purposes, modified, or interpreted in producing this map.

---

## 1. Dependency Graph

```
                    ┌──────────────────────────────────────┐
                    │  SEWCP-100 BASE PLATE (external)     │
                    │  FROZEN — no volume in repository    │
                    └───────────────┬──────────────────────┘
                                    │ declared via FBA-1…FBA-8
                                    ▼
        ┌───────────────────────────────────────────────────────────┐
        │  Vol 00  SEWCP-ENG-001                                    │
        │  Architecture & Interface Control          ◄── PARENT     │
        │  datums · clocking map · Z-stack · budgets · DR-1…DR-13   │
        └───┬───┬───┬───┬───┬───┬───┬───┬───┬───────────────────────┘
            │   │   │   │   │   │   │   │   │
   ┌────────┘   │   │   │   │   │   │   │   └────────┐
   ▼            ▼   ▼   ▼   ▼   ▼   ▼   ▼            ▼
 Vol 01      Vol 02  Vol 03  Vol 04  Vol 05  Vol 06  Vol 07  Vol 08  Vol 09
 SEWCP-200   -300    -400    -500    -600    -700    -800    -900    -1000
 Cooling     Heater  Ring    ESC     Lift    Align   Vacuum  RF      Temp
 Plate       Plate                   Pins    Pins    Port    Bracket Sensor
   ▲
   └──── referenced by Vol 02, 03, 05, 06, 07, 08, 09  (interface hub)

        ┌───────────────────────────────────────────────────────────┐
        │  SEDEP-PMP-001 Program Management Plan                    │
        │  consumes the full spec set as its product baseline       │
        └───────────────┬───────────────────────────────────────────┘
                        │ companion
                        ▼
        ┌───────────────────────────────────────────────────────────┐
        │  SEDEP-PMP-002 Digital Engineering Infrastructure         │
        └───────────────────────────────────────────────────────────┘

        ┌───────────────────────────────────────────────────────────┐
        │  SEWCP-200-CAD-001 Cooling Plate CAD Implementation Pkg   │
        │  consumes Vol 00, 01, 02, 03, 05, 06, 07, 08, 09          │
        │  governed by SEDEP-PMP-001 §0.1                           │
        └───────────────────────────────────────────────────────────┘
```

---

## 2. Specification Cross-Reference Matrix

Row document references column document. `P` = parent. `X` = interface reference.

| ↓ refs → | V00 | V01 | V02 | V03 | V04 | V05 | V06 | V07 | V08 | V09 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Vol 00** Architecture | — | X | X | X | X | X | X | X | X | X |
| **Vol 01** Cooling Plate | P | — | X | X | X | X | X | X | X | X |
| **Vol 02** Heater Plate | P | X | — | · | X | X | X | X | · | X |
| **Vol 03** Support Ring | P | X | · | — | · | · | X | · | · | · |
| **Vol 04** ESC | P | X | X | · | — | X | · | X | · | · |
| **Vol 05** Lift Pins | P | X | X | · | X | — | · | · | · | · |
| **Vol 06** Alignment Pins | P | X | X | X | · | · | — | · | · | · |
| **Vol 07** Vacuum Port | P | X | X | · | X | X | · | — | · | · |
| **Vol 08** RF Bracket | P | X | · | X | · | · | · | · | — | · |
| **Vol 09** Temp Sensor | P | X | X | · | X | · | · | · | X | — |

**Observation:** Volume 01 (Cooling Plate) is referenced by **every other component volume**. It is the interface hub of the specification set, consistent with its stated role. Any change to Volume 01 has the widest blast radius in the document set.

---

## 3. Program Document Dependencies

| Document | Depends On | Type |
|---|---|---|
| SEDEP-PMP-001 | Spec Vol 00–09 (product baseline) | Consumes |
| SEDEP-PMP-001 | SEDEP-PMP-002 | Companion |
| SEDEP-PMP-002 | SEDEP-PMP-001 | Companion |
| SEDEP-PMP-002 | Spec Vol 00–09 | Governs storage/release of |

---

## 4. Implementation Document Dependencies

| Document | Depends On | Type |
|---|---|---|
| SEWCP-200-CAD-001 | Spec Vol 01 | Primary source |
| SEWCP-200-CAD-001 | Spec Vol 00 | Datums, clocking, Z-stack, design rules |
| SEWCP-200-CAD-001 | Spec Vol 02, 03, 05, 06, 07, 08, 09 | Mating interface constraints |
| SEWCP-200-CAD-001 | SEDEP-PMP-001 §0.1 | Change control authority |

---

## 5. Impact Analysis

If a document changes, these must be re-verified:

| Changed | Re-verify |
|---|---|
| **Vol 00** | All nine component volumes + all implementation packages. Highest impact. |
| **Vol 01** | Vol 02, 03, 05, 06, 07, 08, 09 + SEWCP-200-CAD-001 |
| **Vol 02** | Vol 01, 04, 05, 06, 07, 09 + SEWCP-200-CAD-001 |
| **Vol 03** | Vol 01, 06, 08 |
| **Vol 04** | Vol 02, 05, 07, 09 |
| Vol 05–09 | Vol 01 and Vol 00 only |
| **SEDEP-PMP-001** | SEDEP-PMP-002, all implementation packages |

---

## 6. Orphan and Reachability Check

| Check | Result |
|---|---|
| Documents unreachable from `INDEX.md` | **0** |
| Documents unreachable from `README.md` (≤ 2 hops) | **0** |
| Documents with no inbound reference | **0** |
| Documents referencing a non-existent document | **0** |
| Circular dependencies | **2 — both intentional** (Vol 00 ↔ component volumes; PMP-001 ↔ PMP-002). Parent/companion pairs, not defects. |
