# ECR-D-011 — The Ø260 BC kinematic slots cut the outer heater spiral

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-ecr.schema.json`.
> Raised `S-2026-08-10-01` while dispositioning ECR-D-007 requested action 4.

```yaml
ecr_id:       ECR-D-011
class:        D
raised_by:    chief-systems-engineer · S-2026-08-10-01
status:       ENGINEERING-IMPLEMENTED
disposition:  A - HEATER-GROOVE KEEP-OUT, SPIRAL ROUTED TANGENTIALLY, HP-08 RE-VERIFIED
ruled_by:     human-owner · S-2026-08-10-01
approval:     approvals/APR-022_Heater_Plate_coherence_package.md
affected_artifacts:
  - spec/02_SEWCP-300_Heater_Plate.md
evidence:     "See section 3. The outer spiral r 78-145 at 6.00 mm pitch and the kinematic
               slots are milled into the same face; the slot spans r 126-134 and turn centres
               fall at r 126 and r 132."
impact:       "See section 4. A slot of any depth severs brazed MI heater cable at three places."
requested_action: "See section 5."
raised_at:    2026-08-10T00:00:00Z
closed_at:    null
residual:     one - HP-08 re-verification against the as-routed spiral
```

---

## 1 · Class

**D — defect.** Two features are machined into the same face at the same location, and one of
them contains a brazed heater element.

## 2 · Affected artifacts

`spec/02_SEWCP-300_Heater_Plate.md` — §2.2, §3 (new §3.2), §5 (`HP-D09a`), §6 step 3.

## 3 · Evidence

Both quotations are from the same volume. §6 step 3 mills the 2-zone spiral grooves into the
**bottom** face; `HP-IF-3` places the kinematic slots in the **bottom** face.

| | |
|---|---|
| Outer zone (§2.2) | spiral **r = 78 → 145**, **6.00 mm pitch**, 11.2 turns |
| Groove (`HP-D06`) | 3.20 W × **3.20 D** |
| Slot at Ø260 BC (`HP-D10`) | 8.00 L radial → **r 126.0 – 134.0** |
| Turn centres, 78 + 6n | …, 120, **126**, **132**, 138, … |
| Groove envelope at those turns | 124.4–127.6 and 130.4–133.6 — **both inside the slot** |

A `HP-D09a` slot 3.00 mm deep therefore opens a 3.20 mm deep groove containing MI cable, at each
of the three slot positions.

**Neither obvious escape works, and the arithmetic is why.** *Shortening:* `AP-06` requires
0.399 mm of thermal travel on a 6.068 mm boss, so the minimum slot length is **6.87 mm** against
a **6.00 mm** pitch. *Relocating:* the only clear annulus between the two zones is r 72–78,
**6.00 mm** wide against a **6.05 mm** slot. Both fail on arithmetic, not on judgement.

## 4 · Impact

Blocks SEWCP-300 manufacture and, through it, the thermal stack. Blocks `LC-M04-EXIT` `C7`.
It does **not** block SEWCP-200 CAD — no Cooling Plate feature changes.

## 5 · Requested action

Rule how the heater element and the kinematic slots share the bottom face.

## 6 · Disposition — **A**

**Declared keep-out, spiral routed tangentially, `HP-08` re-verified.** Ruled by `human-owner`,
`S-2026-08-10-01`. A new `spec/02` §3.2 declares a keep-out of **≥ 12 mm radial × ≥ 10 mm
tangential** centred on each `HP-D09a` slot, containing no heater groove, with the outer spiral
routed **tangentially around** it. §6 step 3 carries the manufacturing instruction.

**Why tangentially rather than radially.** A tangential detour distorts pitch locally; a radial
detour leaves a void the width of the keep-out. `HP-D08`'s own rationale fixes surface ripple
against 4.6 mm of spreading material at 6 mm pitch, so a local pitch distortion is the smaller
of the two perturbations.

`HP-D09a` slot depth is **3.00 ± 0.10**, matching `SR-D19` and `AP-IF-3` and giving 0.35 mm
worst-case clearance on the 2.50 ± 0.05 boss. **The depth was never the defect** — ECR-D-007
requested action 4 asked only for a depth, and a depth alone would have frozen a slot that
severs the heater.

## 7 · Residual

**One, and it is a measurement rather than a waiver.** `HP-08` (≤ ±1.5 °C across Ø290) shall be
re-verified by instrumented thermal map against the as-routed spiral, by its own declared
verification method. **No uniformity figure is asserted for the detoured routing, and none is
invented here.** Owner: Design Authority, at heater qualification.

## 8 · Relationship to `LC-M04-EXIT`

Blocks `C7` until dispositioned. Dispositioned here; the residual is a later-lifecycle test and
is recorded as such rather than folded into the gate.
