# APR-027 - Alignment Pin locator torque correction (ECR-D-009)

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.

```yaml
approval_id:   APR-027
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-10T00:00:00Z
subject_path:  spec/06_SEWCP-700_Alignment_Pins.md
subject_hash:  75cda88184e5ae50acd05fb86dfb61ffc6238219462e8854120c05f14d04f396
prior_hash:    da702fe05f41b1bac39c3ca507c090a7f7e7258ae18db38addb4d079d755edc6
supersedes:    APR-023
ecr:           ECR-D-002, ECR-D-007, ECR-D-009, ECR-D-010
session:       S-2026-08-10-01
scope:         Two cells only. The SEWCP-700 retention row and section 10 step 5 still
               read 2.5 N.m while spec/01 read 1.2 N.m for the same joint. Both now
               read 1.2 N.m. No other byte changes.
```

---

**Liveness is not asserted here.** Determine it with `python -m aief_approval verify`.

## What is approved

**`VER-015` finding F-08, corrected.** `ECR-D-009` reduced the locator installation torque from
2.5 to 1.2 N.m, because 2.5 N.m puts an M4 A4-70 at roughly **114 % of yield** and was wrong for
the superseded two-piece screw as well. That disposition was applied to `spec/01` §6 step 12 and
§10 step 3, and the ECR record claimed *"both are corrected"*.

**It was not applied to `spec/06`**, which is the **governing volume** for this part. The frozen
set therefore carried two contradictory torques for one joint, both citing ECR-D-009:

| Location | Was | Now |
|---|---|---|
| `spec/06` §4 Retention row | 2.5 N.m | **1.2 N.m** |
| `spec/06` §10 step 5 | 2.5 N.m | **1.2 N.m** |

The defect was found by independent verification, not by the author. It is the same class the
author had just corrected elsewhere - a disposition applied to some of its sites and not all -
which is precisely why `ECR-D-002`'s unapplied §6 step 3 was worth chasing.

## Why this is a separate approval

`APR-023` bound `spec/06` at the pre-correction bytes. Under the supersession relation ruled in
`S-2026-08-10-01`, editing the artifact made `APR-023` **VOID**, and `python -m aief_gate`
reported `C1` and `C2` FAIL until this approval was filed. The chain is
`APR-023 -> APR-027`, and `APR-023` becomes `SUPERSEDED-VALID` rather than void.
