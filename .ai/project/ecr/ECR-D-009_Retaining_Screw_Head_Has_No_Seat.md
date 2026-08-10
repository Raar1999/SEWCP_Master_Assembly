# ECR-D-009 — The alignment-pin retaining screw head has nowhere to bear

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised on `VER-014` F8, confirmed in `VER-014`.

```yaml
ecr_id:       ECR-D-009
class:        D                      # defect - LAW-02
raised_by:    software.software-engineer · S-2026-08-09-14
status:       ENGINEERING-IMPLEMENTED
disposition:  A - INTEGRAL SHOULDERED LOCATOR SCREW; AP-D07 AND AP-D08 STRUCK
ruled_by:     human-owner · S-2026-08-10-01
approval:     approvals/APR-027_Alignment_Pin_torque_correction.md   # terminal on spec/06; supersedes APR-023
affected_artifacts:
  - spec/06_SEWCP-700_Alignment_Pins.md
  - spec/01_SEWCP-200_Cooling_Plate.md
evidence:     "See section 3."
impact:       "See section 4."
requested_action: "See section 5."
raised_at:    2026-08-09T00:00:00Z
closed_at:    null
residual:     none
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

**A — recorded in full at §8.**

## 7 · Relationship to LC-M04-EXIT

An undispositioned ECR against `spec/**`. **Blocks `C7`.**

## 8 · Disposition — **A**

**The locator becomes a one-piece shouldered screw.** Ruled by `human-owner`,
`S-2026-08-10-01`, approval [`APR-023`](../approvals/APR-023_Alignment_Pin_coherence_package.md).

**The two-piece architecture is what fails, and the head diameters prove it.** Against a Ø6.000
h6 boss (5.992 min), with a head counterbore of dk + 0.3:

| Screw | Standard | dk | Wall each side |
|---|---|---|---|
| M4 | ISO 4762 socket head | 7.00 | **−0.65 — impossible** |
| M4 | DIN 6912 / 7984 low head | 7.00 | −0.65 |
| M4 | ISO 7380 button | 7.60 | −0.95 |
| M4 | ISO 10642 countersunk | 8.96 | −1.48 |
| M3 | ISO 4762 | 5.50 | +0.10 — a 0.1 mm rim on the ground centring surface |

**No standard M4 head fits, and M3 leaves nothing.** `AP-D08` cannot be relocated; it has to go.

### The part

Ø6.000 h6 boss carrying a **`AP-D14` 3.0 mm A/F hex socket** in its free end; integral
**Ø12.000 h6** flange; **`AP-D13` M4 × 0.7 × 4.00** threaded spigot below it. `AP-D07` and
`AP-D08` are struck. `AP-D12` overall length 5.50 → **9.50**.

**Drive capacity at the socket, computed rather than assumed.** Across corners 3.464 mm, so the
boss wall is (5.992 − 3.464)/2 = **1.264 mm**. Force per flat = 2500/(6 × 1.5) = 278 N, giving
53.5 MPa of bearing against a Ti bearing yield of order 1,232 MPa (**23×**); hoop tension in the
wall 73 MPa (**12×**); torsion of the boss annulus 66.6 MPa against `spec/06` §2.3's own
550 MPa shear figure (**8.3×**). A 3 mm key is what a standard M4 socket head already uses at
this torque.

### Two consequences, both stated rather than left to be discovered

**`AP-D03` k6 → h6.** A part that is screwed in cannot be an interference fit — rotating a k6
flange inside an H7 bore is `spec/06` FM #5 verbatim, *"Galling on installation"*, whose own
mitigation reads *"transition fit, not press; no press tooling permitted"*. Clearance becomes 0
to 0.029. Against §9's own budget the RSS moves 0.0401 → **0.0422** of the 0.050 allocation,
still passing, and §9 already states that the 0.038 mm slot clearance dominates. At ΔT = 130 K
the Al/Ti fit opens by 0.0234 mm in any case — **nearly twice the maximum interference** — so
the interference was absent at temperature and was carrying nothing.

**Torque 2.5 → 1.2 N·m.** The old figure was wrong for the old screw too: an M4 A4-70 bearing on
the boss end reaches a von Mises stress of ≈512 MPa against a 450 MPa yield — **114 % of
yield**. The integral spigot bears at the flange face (r_b = 4.5 mm), where 1.2 N·m gives
≈1,095 N of preload and ≈190 MPa in Ti-6Al-4V, a margin above 4×.

**Three sites carried the old value, and all three are corrected**: `spec/01` §6 step 12,
`spec/01` §10 step 3, and — in the **governing** volume — `spec/06` §4 Retention and `spec/06`
§10 step 5, under [`APR-027`](../approvals/APR-027_Alignment_Pin_torque_correction.md).

> **Correction recorded `S-2026-08-10-04`.** This paragraph read *"`spec/01` §6 step 12 and §10
> step 3 both carried the old value; **both are corrected**"*. That enumeration was complete for
> `spec/01` and silently excluded `spec/06`, which was **not** corrected at the time — so the
> frozen set carried two contradictory torques for one joint, both citing this ECR, and the
> sentence's confident *"both"* is what made the omission invisible. Found by independent
> verification, not by the author: `VER-015` F-08, confirmed at `VER-016` W1. This is the third
> consecutive instance in this repository of a disposition applied to some of its sites and
> announced as applied to all of them, which is why the enumeration is now explicit about which
> volume governs.

Options **B** (boss to Ø10.000, which propagates into the alumina Support Ring slot that
ECR-D-001 deliberately avoided touching), **C** (M3, a 0.1 mm rim) and **D** (retention from the
opposite face, six new through-penetrations of a pressure boundary) were presented and not
approved.
