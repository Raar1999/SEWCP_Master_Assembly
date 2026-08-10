# ECR-D-003 — The coolant stub interface is undimensioned

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised against the frozen Rev A specification. Blocking `LC-M04-EXIT` criterion `C3`.

```yaml
ecr_id:       ECR-D-003
class:        D                      # defect - LAW-02: a defect stops the affected work
raised_by:    project-manager · S-2026-08-08-01
status:       ENGINEERING-IMPLEMENTED   # NOT CLOSED - awaits C6 independent verification
disposition:  A - COAXIAL PORT, CHANNEL LOCALLY DEEPENED, BIMETALLIC TRANSITION JOINT
ruled_by:     human-owner · S-2026-08-10-01
approval:     approvals/APR-020_Cooling_Plate_coherence_package.md
approval_chain: APR-020
affected_artifacts:
  - spec/01_SEWCP-200_Cooling_Plate.md
evidence:     "See section 3. CP-IF-10 names the fitting and the two clock angles and states
               no bore, no depth, no centreline height, no weld preparation, no tube size and
               no round-to-rectangular transition. No CP-Dxx row existed for the feature."
impact:       "See section 4. Blocks 2 CAD features (HOLD H3) and drawing Section B-B."
requested_action: "See section 5. Dimension the stub interface and rule the joint method."
raised_at:    2026-08-08T01:31:23Z
closed_at:    null
residual:     one - CP-02 pressure drop, shared with ECR-D-002 section 7
```

---

## 1 · Class

**D — defect.** Not an ambiguity: the feature is named and clocked by the frozen specification
and carries no dimension of any kind. Under LAW-02 a defect stops the affected work — a
modeller cannot cut a bore whose diameter, height and breakthrough point are all absent, and
inventing them is a Design Authority act.

## 2 · Affected artifacts

| Artifact | Role in the defect |
|---|---|
| `spec/01_SEWCP-200_Cooling_Plate.md` | Declares `CP-IF-10` and the §6 step 10 weld operation. **Corrected by this disposition.** |

No other volume states anything about this interface. `spec/00` §10 A1 names the operation
(*"orbital-weld VCR stubs"*) without dimensioning it and is unchanged by this disposition.

## 3 · Evidence

**3.1 What is specified.** `CP-IF-10`, verbatim before this disposition:

> *"2× 1/2 in. VCR male gland stubs, orbital-welded, radial at 255° (inlet) / 285° (outlet)"*

**3.2 What is not specified anywhere in the frozen set.** Bore diameter; bore depth and
breakthrough point into the channel; bore centreline height above Datum A; weld preparation
geometry; tube OD and wall; the transition from a round bore to the rectangular channel; and
the stub **material**. No `CP-Dxx` row existed and the feature does not appear in §9.

**3.3 The geometry does not close, and `ECR-D-002` made it tighter.** ½ in. tube OD is
12.70 mm. Measured from Datum A (the bottom face) the plate is:

| Band | Extent above Datum A | Member |
|---|---|---|
| 0.00 – 6.00 | 6.00 | FSW lid (`CP-D08`) |
| 6.00 – 12.00 | 6.00 | Coolant channel (`CP-D06`) — **was 8.00 before ECR-D-002** |
| 12.00 – 20.00 | 8.00 | Channel-to-top-face wall (`CP-D07`) |

**Any round bore larger than the channel height cannot stay inside the channel band.** At the
former 8.00 mm depth the mismatch against a Ø12.70 tube was 4.70 mm; at 6.00 mm it is 6.70 mm.
The `ECR-D-002` disposition therefore **worsened this defect**, which is the physical coupling
between the two and the reason they were dispositioned in that order.

**3.4 The specified joint is not metallurgically possible.** §11 FM #8 names a *"galvanic pair
with SS stubs"*, so the design intent is a stainless stub, and `CP-IF-10` directs an orbital
weld to a 6061 plate. **6061 aluminium cannot be fusion-welded to 316L.** As written the
operation cannot be performed by any process.

**3.5 Radial space is available.** The channel is confined to the Ø60–Ø250 annulus, so its
outer limit is r = 125.00; the plate OD is Ø320.0, r = 160.00. **35 mm** of solid material lies
between them for the bore to traverse.

## 4 · Impact

Blocks SEWCP-200 CAD (HOLD H3, 2 features) and drawing Section B-B. Blocks `LC-M04-EXIT` `C3`.

## 5 · Requested action

Specify the stub bore diameter, depth, centreline height, weld preparation and the
bore-to-channel transition; and rule how a stainless gland is joined to an aluminium plate.

## 6 · Disposition — **A**

**Coaxial port with the channel locally deepened, fed through a bimetallic transition joint.**
Ruled by `human-owner`, `S-2026-08-10-01`, approval
[`APR-020`](../approvals/APR-020_Cooling_Plate_coherence_package.md).

### 6.1 Executed changes — `spec/01` only

| Location | Change |
|---|---|
| `CP-IF-10` | Rewritten with the full geometry and the SEWCP-201 joint |
| §4 Mating Components | New row: **SEWCP-201** coolant transition joint, 2 off |
| `CP-D22` (new) | Coolant stub bore, **Ø10.0 H9**, 2× radial at 255° / 285° |
| `CP-D23` (new) | Bore centreline **11.00 ± 0.10** above Datum A |
| `CP-D24` (new) | Weld-prep counterbore **Ø14.0 H8 × 4.0 deep** at the OD, coaxial with `CP-D22` |
| `CP-D25` (new) | Channel local depth at the two ports **10.00 +0.20/−0**, ramped to `CP-D06` over 15 mm |
| §3.1 | New **Port exception** paragraph declaring the two bounded departures |
| §6 step 3 | Local deepening added to the channel milling operation |
| §6 step 10 | Weld operation restated as 6061-to-6061 into `CP-D24` |
| §9 | Position ⌖ Ø0.50 Ⓜ A B C and axis parallelism 0.20 over 35 mm |
| §11 FM #8 | Cause and mitigation restated for the transition joint |

### 6.2 Why the numbers are what they are

**The bore is Ø10.0** because the channel's flow area is 60 mm² and a Ø10.0 bore is 78.5 mm² —
larger, so the port is not the restriction. `CP-02`'s pressure drop is already adverse and
open under `ECR-D-002` §7, and a port that necked the circuit would compound it. Ø8.0 would
give 50.3 mm² and restrict; Ø6.0 would give 28.3 mm² and restrict severely.

**The centreline is 11.00 above Datum A** because that places the bore's lower edge at 6.00 —
exactly the channel floor, which is the FSW lid's upper surface and the weld plane. The bore
therefore **never penetrates the lid**, and there is no pocket below the flow path to trap
sediment (§11 FM #8). Centring the bore on the channel's own mid-height of 9.00 would have cut
2.00 mm into the lid and left such a pocket.

**The channel is deepened to 10.00 at the ports** so that the bore and the channel are coaxial
and the section matches: the port pocket is 10.00 W × 10.00 D and the Ø10.0 bore spans exactly
6.00 – 16.00. There is no step at the junction in any direction.

**The consequence is stated, not hidden:** over the two port pockets the channel-to-top-face
wall is 4.00 mm rather than `CP-D07`'s 8.00. At `CP-05` proof pressure of 6 bar a 4.00 mm
ligament spanning the 10 mm bore carries a bending stress of order

> M ≈ pL²/8 = 0.6 × 10²/8 = 7.5 N·mm per mm of width; σ = 6M/t² = 6 × 7.5 / 4.00² = **2.8 MPa**

against 276 MPa yield — a margin of roughly 100×. The reduction is thermally irrelevant: it
covers two pockets of order 15 × 10 mm on a Ø320 plate.

### 6.3 The joint

The 316L VCR gland is **not** welded to the plate. **SEWCP-201** is an explosion-bonded
6061/316L transition joint: its aluminium end is orbital-GTAW welded into `CP-D24` as a
like-to-like 6061 weld, and its stainless end carries the standard ½ in. VCR male gland. This
is the ordinary solution for this joint in semiconductor coolant service, it keeps every fusion
weld between like metals, and it leaves the dissimilar couple as a metallurgical bond over a
short wetted length rather than a fusion weld that cannot be made.

Options **B** (aluminium stub and aluminium gland — the sealing bead galls and takes permanent
set on retorque), **C** (gland machined integrally into the plate OD — same galling objection,
and bead damage then scraps the plate) and **D** (declare 316L now, defer the joint) were
presented and not approved.

## 7 · Residual

**One, and it is shared rather than new.** `CP-02`'s 4.0 L/min at ΔP < 1.5 bar is verified on a
flow bench and remains open from `ECR-D-002` §7. This disposition does not close it and does
not worsen it: the port is larger in area than the channel it feeds, so it adds no restriction.
**No ΔP value is asserted here.** Owner: Design Authority, by flow bench.

## 8 · Relationship to `LC-M04-EXIT`

`C3` requires an approved disposition; `C5` requires it present in `spec/**` and re-registered;
`C6` requires independent verification. Engineering is implemented and registered. **The record
is not closed until `C6` is satisfied** — see `VER-015`.
