# APR-019 — Cooling Plate channel depth 8.00 → 6.00 (ECR-D-002 disposition A)

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for ECR-D-002 disposition A.

```yaml
approval_id:   APR-019
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-09T00:00:00Z
subject_path:  spec/01_SEWCP-200_Cooling_Plate.md
subject_hash:  36e8d35b1004c22279abc67fe81447632d87a934bf057e8366e5f5a1160abdda
prior_hash:    a39e4b24c02b6b61ed74f93f661e0ed74f0323133e62297d51e5390c536b7db5
supersedes:    APR-018                # voided by this edit under LAW-10
ecr:           ECR-D-002
session:       S-2026-08-09-14
scope:         Disposition A of ECR-D-002 - the coolant channel depth is reduced from
               8.00 to 6.00 mm so the Z stack closes at CP-D02 20.000, and every value
               derived from the depth in spec/01 is recomputed. No other volume changes.
               CP-02 pressure drop is NOT dispositioned and remains open.
```

---

**Liveness is not asserted here.** Determine it by recomputing the DC-1 of `subject_path` and
comparing with `subject_hash`. `VER-014` R3-F1 records why: a hand-written `LIVE` label went
stale twice and was twice repaired by relabelling rather than by removing the claim.

## What is approved

**Option A**, in the words put to the approver:

> Channel depth 8.00 → 6.00. Flow area 80 → 60 mm². Re rises to ~8,300 (turbulence margin
> improves). Pressure drop rises ~2.2× and must be checked against `CP-02`'s 1.5 bar budget.

Options **B** (top wall 8.00 → 6.00; attacks the Critical `CP-08` flatness), **C** (FSW lid
6.00 → 4.00; narrows the weld window on the vacuum-facing pressure boundary) and **D**
(overall thickness 20.000 → 22.000; changes the Critical value, propagates into the ICD stack,
breaches `CP-15`) were presented and **not approved**.

## Scope

| In scope | Out of scope |
|---|---|
| `spec/01` `CP-D06` and the nine values derived from the depth (§2.1 sizing table, §5 mass estimate, §13/§14 rationale) | Every other specification volume |
| The `CP-02` note placed in §2.1 recording that ΔP must be re-verified | **Any ΔP value.** None is asserted, adopted or frozen |
| Re-registration of `spec/01`; DC-2 aggregate; `STATE.md` | ECR-D-001, ECR-D-003, ECR-D-004, ECR-D-006…009 |
| — | CAD, Stage 6, `MANIFEST.lock`, the ledger |

## The one thing this approval deliberately does not do

The approver selected Option A on an analyst package that **named the pressure-drop estimate
as a derivation, not a specification value**, and flagged that `CP-02`'s 1.5 bar budget could
be breached. That question is **not** resolved by this approval and is recorded as
`ECR-D-002` §7 with the Design Authority as owner and the flow bench as the method.

The estimate offered was *"roughly 2.2×"*. It is recorded as an estimate and **is not written
into the specification**, because `CP-02` is verified by test and this repository has four
recorded instances of an authored number being mistaken later for a measured one.

## Authority

`BINDING.approval_authority` is `human-owner`. `mechanical.design-engineer` is UNASSIGNED in
`ROSTER.md`. The engineering value in this change — the 6.00 mm depth — follows arithmetically
from the two dimensions left unchanged and the Critical total: 20.000 − 8.00 − 6.00 = 6.00. It
is determined, not chosen.
