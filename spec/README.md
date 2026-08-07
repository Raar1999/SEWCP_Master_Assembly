# SEWCP — Engineering Specification Set

**Simplified Electrostatic Wafer Chuck Platform**
**Revision A — Specification Freeze Candidate · 2026-08-07**

This is the complete engineering specification for the SEWCP 300 mm electrostatic chuck platform. It is written to a level of detail sufficient for CAD to be executed directly, without design iteration.

**The Base Plate (SEWCP-100) is frozen and is not specified here. It shall not be redesigned.**

No CAD steps, no modelling instructions, and no code are contained in this set.

---

## Read This First

**Volume 00 is the parent document.** It defines the coordinate system, datums, feature clocking map, stack-up, thermal/RF/vacuum budgets, tolerance allocation, fastener schedule, master assembly sequence, and the 13 binding Design Rules. Every component volume is written against it. **Do not begin CAD from a component volume alone.**

| Vol | Document | Part No. | Component |
|-----|----------|----------|-----------|
| **00** | **[SEWCP-ENG-001](00_SEWCP-ENG-001_Architecture_and_Interface_Control.md)** | — | **Architecture & Interface Control — START HERE** |
| — | *(frozen)* | SEWCP-100 | Base Plate — **FROZEN, NOT IN SCOPE** |
| 01 | [SEWCP-ENG-002](01_SEWCP-200_Cooling_Plate.md) | SEWCP-200 | Cooling Plate |
| 02 | [SEWCP-ENG-003](02_SEWCP-300_Heater_Plate.md) | SEWCP-300 | Heater Plate (+ thermal choke) |
| 03 | [SEWCP-ENG-004](03_SEWCP-400_Chuck_Support_Ring.md) | SEWCP-400 | Chuck Support Ring |
| 04 | [SEWCP-ENG-005](04_SEWCP-500_Electrostatic_Chuck.md) | SEWCP-500 | Electrostatic Chuck |
| 05 | [SEWCP-ENG-006](05_SEWCP-600_Lift_Pins.md) | SEWCP-600 | Lift Pins |
| 06 | [SEWCP-ENG-007](06_SEWCP-700_Alignment_Pins.md) | SEWCP-700 | Alignment Pins |
| 07 | [SEWCP-ENG-008](07_SEWCP-800_Vacuum_Port.md) | SEWCP-800 | Vacuum Port Assembly |
| 08 | [SEWCP-ENG-009](08_SEWCP-900_RF_Feedthrough_Bracket.md) | SEWCP-900 | RF Feedthrough Bracket Assembly |
| 09 | [SEWCP-ENG-010](09_SEWCP-1000_Temperature_Sensor_Bracket.md) | SEWCP-1000 | Temperature Sensor Bracket |

Every component volume follows the same 14-section structure: Engineering Purpose · Functional Requirements · Mechanical Interfaces · Mating Components · Critical Dimensions · Manufacturing Method · Material · Surface Finish · Tolerances · Assembly Sequence · Failure Modes · Design Rationale · Why Semiconductor Tools Use This Design · Interview Talking Points.

---

## Platform at a Glance

| Parameter | Value |
|---|---|
| Wafer | 300 mm × 775 µm |
| Chucking | Coulombic, bipolar, ±500 to ±2000 VDC (nominal ±1500 V) |
| Clamping pressure at ±1500 V | 38.9 mbar |
| Backside gas | Helium, 5–20 Torr |
| Wafer temperature | 20–150 °C, ±2.0 °C across Ø300 |
| Wafer plane height above Datum A | **55.920 ± 0.150 mm** |
| Thermal chain, wafer to coolant | **0.122 K/W** |
| Thermal choke | **0.100 ± 0.030 K/W** (16× Ti washers) |
| Coolant | 4 L/min, Re ≈ 7,400, 3 kW capacity |
| Heater | 2 zones, 2000 W, 28.3 kW/m² uniform density |
| RF bias | 13.56 MHz, ≤1000 W, ≤1500 V peak |
| Support Ring isolation | 0.195 K/W thermal, 435 Ω at 13.56 MHz |
| Assembly He leak rate | < 1×10⁻⁹ mbar·L/s |

## Stack-Up

```
                     Ø300 WAFER (0.775)          Z = 56.695
        ═════════════════════════════════════    Z = 55.920  ← Datum F, wafer backside
          ▲ 0.020 mesa gap, He-filled
    [ SEWCP-500  ESC          Ø297 × 6.00  ]     Al₂O₃ 99.6%, bipolar
      ░░░ elastomer bond 0.40 ░░░
    [ SEWCP-300  HEATER PLATE Ø300 × 8.00  ]     6061-T6 + MI heater, 2 zones
      ▫ THERMAL CHOKE  16× Ti washers 1.50 ▫     R = 0.100 K/W  ← the key feature
    [ SEWCP-200  COOLING PLATE Ø320 × 20.00]     6061-T6, FSW-sealed channel, RF electrode
    [ SEWCP-400  SUPPORT RING  H 20.00     ]     Al₂O₃ 99.5%, lapped to fit at assembly
    ═════════════════════════════════════════    Z = 0.000  ← Datum A
      SEWCP-100  BASE PLATE  *** FROZEN ***
```

---

## The Five Decisions That Shape Everything Else

1. **The Support Ring absorbs all frozen-baseline risk (DR-1).** The Base Plate was frozen before its interface was documented. Rather than propagate that uncertainty through nine components, one ceramic ring is the sole structural interface and every other touchpoint floats with ≥ 2 mm clearance. The same part is also the electrical isolator and the assembly shim.

2. **A thermal resistance was added on purpose.** A heater bolted flat to a 3 kW chiller rises less than 1 K. The 0.100 K/W titanium-washer choke is what makes the heater an actuator instead of a parasitic load — and it dominates the thermal chain by 10×, which is the point.

3. **Paschen's law drove three mechanical requirements.** Lift pins that never leave their bore (DR-4), helium interlocked to pin position (DR-5), and RF inhibited across the pump-down transition band (DR-11). In the last case, adding clearance makes the hazard *worse*.

4. **Constraint schemes came before tolerance schemes.** Aluminium against alumina across 130 K moves 0.3–0.4 mm. Three radial-slot kinematic locators hold centre to 20 µm while imposing no constraint force; a conventional round-and-diamond dowel pair would have missed by 3×.

5. **Nothing penetrates the wafer-facing surface (DR-2).** All 24 stack fasteners install from below, which is why the coolant serpentine must be routed around a fixed fastener pattern.

---

## Status and Open Items

**Revision A is a specification freeze candidate.** Five open items are listed in Volume 00 §13. The two that gate CAD release:

- **OI-1** — Confirm the eight Frozen Baseline Assumptions (Vol 00 §2) against the actual Base Plate drawing. By DR-1, any discrepancy affects **only** the Support Ring.
- **OI-2** — Confirm Configuration A (RF-hot chuck, specified throughout) versus Configuration B (grounded chuck), which deletes the RF Feedthrough Bracket and simplifies the Support Ring. Required before Volume 08 release.

The remaining three (OI-3 thermal choke tuning, OI-4 lift pin bolt circle vs. robot envelope, OI-5 bond elastomer qualification) are qualification-phase items and do not block CAD.
