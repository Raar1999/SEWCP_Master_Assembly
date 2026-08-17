# ECR-Q-014 — SEWCP-401 Lower Clamp Ring material is specified two ways

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Found at session `S-2026-08-17-01` while performing the `OI-C-15` §6.2 creepage trace.

```yaml
ecr_id:       ECR-Q-014
class:        Q                      # query - two records of the same part disagree
raised_by:    mechanical.design-engineer · S-2026-08-17-01
status:       DISPOSITIONED
disposition:  spec/03 s5.2 governs - 316L. The BOM row is the derived artifact and is corrected; no spec/** byte moves
ruled_by:     claude-under-owner-delegation (owner-delegated engineering authority, mission 2026-08-17; NOT a human approval)
ruled_at:     2026-08-17T00:00:00Z
instrument:   .ai/project/decisions/DECISIONS_S-2026-08-17-01.md DEC-14
approval:     none required - the correction is to a generated deliverable, not to a registered artifact
affected_artifacts:
  - cad/bom/SEWCP-000_BOM_RevA.csv
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-17T00:00:00Z
related:      ECR-D-008, ECR-D-016
```

## 1 · Class

**Q — query.** Not a defect in the design: a divergence between the governing volume and a
derived record. `spec/03` §5.2 is headed **"SEWCP-401 Lower Clamp Ring (316L)"**. The
indentured BOM carries `6061-T6` on the same part number.

## 2 · Evidence

```
spec/03_SEWCP-400_Chuck_Support_Ring.md:134
    ### 5.2 SEWCP-401 Lower Clamp Ring (316L)

cad/bom/SEWCP-000_BOM_RevA.csv
    1,SEWCP-401,Support ring clamp ring,1,6061-T6,spec/00 §9 lower circuit; spec/03 SR-IF-2,spec-only,-,…
```

The BOM row cites `spec/00` §9 and `spec/03` `SR-IF-2` as its sources. **Neither states a
material** — §9 is the fastener and torque schedule, `SR-IF-2` is the register interface.
The only place `SEWCP-401`'s material is stated is §5.2's heading, and the BOM did not read
it. So this is not two authorities disagreeing; it is one authority and one unsourced value.

## 3 · Impact

Small but not nil, and worth stating rather than waving away. The two candidates differ in
every property that matters at this joint:

| | 316L | 6061-T6 |
|---|---|---|
| CTE | ≈ 16 ppm/K | ≈ 23.6 ppm/K |
| Modulus | ≈ 193 GPa | ≈ 69 GPa |

`SEWCP-401` clamps an alumina flange (7.2 ppm/K) through a Belleville stack sized so that
*"differential thermal expansion across the joint … changes preload by less than ±20%"*
(`spec/00` §9). Substituting an aluminium clamp ring for a stainless one changes both the
CTE mismatch driving that preload change and the stiffness through which it acts, and the
Belleville selection is sized against the stainless case. FMEA row 4 — *preload relaxation*
— carries the highest RPN in `spec/03` at **140**.

Nothing at `LC-M04-EXIT`: the part is `spec-only`, unmodelled, and no `spec/**` byte moves
under this disposition.

## 4 · Requested action and disposition

`spec/03` §5.2 is the governing volume for `SEWCP-401` — the part is declared in `spec/03`'s
own title block (*"Includes: SEWCP-401 Lower Clamp Ring"*) and dimensioned in its §5.2.
**316L governs.** The BOM is the derived artifact and is corrected to `316L`, with its
`spec_source` cell corrected to cite `spec/03` §5.2, which is where the value actually
lives. The `ECR-D-008` precedent applies: where an interface record and a governing volume
disagree, the governing volume rules and the derived record is repaired.

**Not repaired here:** `SEWCP-401` remains *"Deferred geometry"* and, per
[`ECR-D-016`](ECR-D-016_Support_Ring_Isolation_Joint_Does_Not_Close.md), the form it is
given cannot be placed at all. Its material is now unambiguous; its geometry is Rev B work.
