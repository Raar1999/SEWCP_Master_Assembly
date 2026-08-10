# ECR-D-004 — The choke counterbore is undimensioned and the specified bolt does not fit the stack

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised against the frozen Rev A specification. Blocking `LC-M04-EXIT` criterion `C4`.

```yaml
ecr_id:       ECR-D-004
class:        D                      # defect - LAW-02: a defect stops the affected work
raised_by:    project-manager · S-2026-08-08-01
status:       ENGINEERING-IMPLEMENTED   # NOT CLOSED - awaits C6 independent verification
disposition:  A - SLOTTED MASKED COUNTERBORE 11.0 x 12.5 x 2.5, M5 x 25, HP-D12 BLIND 6.50
ruled_by:     human-owner · S-2026-08-10-01
approval:     approvals/APR-020_Cooling_Plate_coherence_package.md
approval_chain: APR-020 spec/01; APR-021 spec/00 section 9; APR-022 spec/02 HP-D12
affected_artifacts:
  - spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md
  - spec/01_SEWCP-200_Cooling_Plate.md
  - spec/02_SEWCP-300_Heater_Plate.md
evidence:     "See section 3. CP-IF-3 says 'counterbored' and dimensions no counterbore;
               spec/00 section 9 specifies M5 x 30 against a 29.500 mm stack; CP-D21 and
               HP-D12 point at each other and neither states a thread depth."
impact:       "See section 4. Blocks 16 CAD features (HOLD H3) and drawing DET-3, and as
               specified drives a bolt into the ESC bond line."
requested_action: "See section 5. Dimension the counterbore, confirm the fastener length,
               and state the thread depth in the Heater Plate."
raised_at:    2026-08-08T01:31:23Z
closed_at:    null
residual:     none
```

---

## 1 · Class

**D — defect.** Three separate failures in one joint: a feature declared and undimensioned, a
fastener that cannot be installed, and a dimension that no volume states because two volumes
each delegate it to the other.

## 2 · Affected artifacts

| Artifact | Role in the defect |
|---|---|
| `spec/01_SEWCP-200_Cooling_Plate.md` | `CP-IF-3` declares the counterbore; `CP-D21` delegates the thread depth. **Corrected.** |
| `spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md` | §9 specifies `M5 × 30`. **Corrected.** |
| `spec/02_SEWCP-300_Heater_Plate.md` | `HP-IF-2` / `HP-D12` host the thread and state no depth. **Corrected.** |

## 3 · Evidence

**3.1 The counterbore is declared and undimensioned.** `CP-IF-3` reads *"16× M5
**counterbored** radially slotted clearance holes, 5.5 W × 7.0 L"*. The **slot** is dimensioned;
the **counterbore** has no diameter, no depth, and no statement of whether it is itself slotted.
No `CP-Dxx` row existed.

It must be slotted. The joint is a Belleville-preloaded slip joint: `spec/00` §4.4 requires it
to allow *"0.4 mm radial growth differential at ΔT = 130 K"*, the bolt is fixed in the Heater
Plate and therefore travels radially **relative to the Cooling Plate**, and the existing slot
carries 7.0 − 5.5 = 1.5 mm of travel. A round counterbore would jam the head against its wall
at the extreme of that travel.

**3.2 The specified bolt does not fit, at any counterbore depth.** Grip, from the bolt-head
bearing face to the first engaged thread, with counterbore depth `d` and a Belleville working
height of 0.6 mm:

> grip = 0.6 + (20.000 − d) + 1.500 = **22.100 − d**
> engagement `e` = L − grip = **L − 22.100 + d**

At `L = 30` and `d = 0` — the most favourable case for the specified bolt — `e = 7.90 mm` into
a Heater Plate `HP-D02` **8.000 mm** thick, leaving **0.10 mm** before the `HP-IF-4` ESC bond
face. Any counterbore at all makes it worse, and the raising record's own figure of 0.500 mm of
protrusion assumed the head bore directly on the plate with no Belleville. **`M5 × 30` is
unbuildable in this joint under every reading.**

**3.3 The thread depth is specified nowhere, by a closed loop.** `CP-D21` reads *"M5 tapped
depth (into Heater Plate side) — **See SEWCP-300**"*. `HP-D12` in SEWCP-300 reads *"M5 × 0.8,
insert"* and states **no depth**. Each volume defers to the other and the value does not exist.

**3.4 The depth budget is severely constrained.** `HP-IF-2` requires **stainless helical
inserts**, and the hole is blind because breaking through would open into the 0.400 mm ESC
bond line over Ø297 — forbidden by DR-2's intent and destructive of `HP-IF-4`. A 1.5×D M5
insert (7.5 mm) plus tap run-out needs about 9.0 mm in an 8.000 mm plate and **does not fit**.

## 4 · Impact

Blocks SEWCP-200 CAD (HOLD H3, 16 features) and drawing DET-3. Blocks `LC-M04-EXIT` `C4`. As
specified it drives a fastener into the ESC bond line, which is a build-stopping conflict
rather than a documentation one.

## 5 · Requested action

Dimension the counterbore including whether it is slotted; confirm the fastener length for the
29.500 mm stack; and state the thread engagement available in the 8.000 mm Heater Plate.

## 6 · Disposition — **A**

**Shallow slotted masked counterbore, `M5 × 25`, `HP-D12` blind at 6.50.** Ruled by
`human-owner`, `S-2026-08-10-01`, approval
[`APR-020`](../approvals/APR-020_Cooling_Plate_coherence_package.md).

### 6.1 Executed changes

| Artifact | Location | Change |
|---|---|---|
| `spec/01` | `CP-IF-3` | Counterbore dimensioned, declared slotted and anodize-masked; `M5 × 25` named |
| `spec/01` | `CP-D26` (new) | **11.0 W × 12.5 L × 2.5 deep**, +0.20/−0 |
| `spec/01` | `CP-D21` | Closed loop broken: now reads `HP-D12`, 6.50 blind |
| `spec/01` | §6 step 13 | `CP-D26` floors added to the anodize mask list, with the reason |
| `spec/01` | §9 | Position control extended to the counterbores |
| `spec/00` | §9 fastener schedule | `M5 × 30` → **`M5 × 25`**, both rows; the false *"Slotted clearance holes in Heater Plate"* note corrected to the Cooling Plate |
| `spec/02` | `HP-D12` | **Blind, tapped depth 6.50 +0.30/−0, 1×D insert, 1.50 mm min to the bond face**; criticality Low → **High** |
| `spec/02` | `HP-IF-2` | Blind-hole rule and `M5 × 25` stated |
| `spec/02` | §10 step 13 | `M5 × 25`; explicit instruction not to substitute `M5 × 30` |

### 6.2 The arithmetic that fixes the length

With `d = 2.5`: grip = 22.100 − 2.5 = 19.600, so at `L = 25`, **`e` = 5.400 mm**. The `HP-D12`
tapped depth is 6.50 with a 1×D (5.0 mm) insert, so the bolt engages the **full insert** and
runs 0.4 mm into the run-out below it, and 8.000 − 6.50 = **1.50 mm** of material remains to
the bond face.

**Preload and margin.** At 3.5 N·m with anti-galling dry film (DR-8), taking K ≈ 0.18,
F ≈ 3.5 / (0.18 × 0.005) ≈ **3.9 kN**. On the M5 tensile stress area of 14.2 mm² that is
274 MPa, about 61 % of A4-70's 450 MPa proof. Thread shear over 5.40 mm of engagement is of
order π × 5 × 5.40 × 0.5 ≈ 42 mm²; against a stainless insert this is several times the applied
load, and the insert-to-aluminium pull-out area is larger still. **The 1×D insert is not the
weak element at this preload.**

### 6.3 Why the counterbore is 11.0 × 12.5 and masked

**Width 11.0** clears the Ø10.0 Belleville with 0.5 mm to spare. **Length 12.5** carries the
1.5 mm of radial travel while keeping the Belleville fully supported at both extremes
(12.5 − 10.0 = 2.5 > 1.5). **Depth 2.5** keeps the counterbore wholly inside the 6.00 mm FSW
lid, so the weld plane is never machined through — the alternative, a 6.5 mm deep counterbore
taking an `M5 × 20`, would have removed the lid at all 16 positions and seated the bolt across
a machined-through weld region, and its shorter bolt would be stiffer and hold preload less
well across the slip cycle.

**Masked** because this joint slips ≈ 0.4 mm every thermal cycle under ≈ 3.9 kN. Hard anodize
is friable; a Belleville sliding on it generates wear debris above a wafer. The counterbore
floor was not on the §6 step 13 mask list, and would not have been noticed until the first
teardown.

### 6.4 Interference checks performed

| Check | Result |
|---|---|
| §3.1 keep-out, *"Choke fastener holes … 8 mm"* | Slot half-length 6.25 mm < 8 mm — **the counterbore fits inside the existing declared keep-out, so the coolant routing is unaffected** |
| RF land envelope, r = 128–146, 93°–117° | At Ø270 BC the 11.0 mm width subtends ±2.33°; the nearest fasteners at 90° and 120° reach 92.33° and 117.67°, clearing the land by **0.67° ≈ 1.58 mm** |
| Fastener pitch | Ø270 BC: 70.7 mm arc. Ø90 BC: 70.7 mm arc. No overlap |
| Head protrusion | 5.0 head + 0.6 Belleville − 2.5 counterbore = **3.1 mm** below the bottom face, into the open interior of the Support Ring at r = 45 and r = 135. No member occupies that space |

Options **B** (deep counterbore, `M5 × 20`), **C** (no counterbore) and **D** (thicken the
choke washer) were presented and not approved; C is unviable at either bolt length and D moves
two Critical values to avoid changing one fastener.

## 7 · Residual

**None.** The `CP-02` pressure-drop residual is not shared by this joint.

## 8 · Relationship to `LC-M04-EXIT`

`C4` requires an approved disposition; `C5` requires it applied and re-registered; `C6`
requires independent verification. **Not closed until `C6` is satisfied** — see `VER-015`.
