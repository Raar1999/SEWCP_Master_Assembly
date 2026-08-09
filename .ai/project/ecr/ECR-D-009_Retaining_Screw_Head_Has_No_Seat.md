# ECR-D-009 — The alignment-pin retaining screw head has nowhere to bear

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised on `VER-014` F8, confirmed in `VER-014`.

```yaml
ecr_id:       ECR-D-009
class:        D                      # defect - LAW-02
raised_by:    software.software-engineer · S-2026-08-09-14
status:       OPEN
disposition:  null                   # Design Authority decision required
ruled_by:     null
approval:     null
raised_at:    2026-08-09T00:00:00Z
closed_at:    null
residual:     null
```

---

## 1 · Class

**D — defect.** A specified feature cannot exist in the geometry that must contain it.

## 2 · Affected artifacts

`spec/06_SEWCP-700_Alignment_Pins.md` — `AP-D01`, `AP-D07`, `AP-D08`, `AP-IF-1`, §12 step 5.
Consequentially `spec/01_SEWCP-200_Cooling_Plate.md` §10 step 3, which now instructs the
torque.

## 3 · Evidence

| Ref | States |
|---|---|
| `AP-IF-1` | *"M4 × 10 SHCS **through the pin** into the plate"* |
| `AP-D07` | Screw clearance bore **Ø4.3** through the locator |
| `AP-D08` | **Counterbore for screw head Ø8.0 × 2.2** |
| `AP-D01` | Locating boss diameter **Ø6.000** h6 |

The screw enters from the locator's exposed end, which is the **Ø6.000 boss**. A **Ø8.0 head
counterbore cannot exist in a Ø6.000 boss.** A bare M4 socket-head cap screw is Ø7.0 across
the head and does not fit either.

`spec/01` §10 step 3 now directs *"torque the M4 × 10 SHCS to 2.5 N·m"* — a preload
instruction for a joint whose screw head has no seat.

## 4 · Impact

Blocks SEWCP-700 manufacture and the locator installation step in SEWCP-200 assembly. Does not
invalidate the ECR-D-001 interface decision: the locating geometry — flange, counterbore, boss,
slot — is unaffected. Retention is what fails.

## 5 · Requested action

Determine how the retaining screw is seated. The resolution may be dimensional (flange
diameter, head counterbore location) or architectural (retention from the opposite face), and
either may reopen `AP-IF-1`.

## 6 · Disposition

**None. OPEN.**

## 7 · Relationship to LC-M04-EXIT

An undispositioned ECR against `spec/**`. **Blocks `C7`.**
