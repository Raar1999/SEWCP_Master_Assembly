# APR-018 — Strike the unauthorised M4 tap depth from `spec/01`

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies LAW-01 and LAW-10 for the repair of `VER-010` finding R10(a).

```yaml
approval_id:   APR-018
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-09T00:00:00Z
subject_path:  spec/01_SEWCP-200_Cooling_Plate.md
subject_hash:  a39e4b24c02b6b61ed74f93f661e0ed74f0323133e62297d51e5390c536b7db5
prior_hash:    f2d228e1730819de3786776a08c4e2526bb0ecb7d1b5b79a493c398d0f2a5355
supersedes:    APR-017                # voided by this edit under LAW-10
ecr:           ECR-D-001              # repair of a VER-010 finding against its implementation
session:       S-2026-08-09-14
scope:         Option A - strike the 8.0 mm tap depth. CP-D09a and CP-D10a become
               "M4 x 0.7, depth TBD - ECR-D-007". The depth determination moves to
               ECR-D-007 requested action 5. No other change.
```

---

## The defect being repaired

`CP-D09a` and `CP-D10a` carried **`M4 × 0.7, 8.0 deep`**. The approved Option A text of
`APR-016` reads *"Ø12.0 H7 × 3.0 counterbore + M4 tapped hole, protrusion 2.50 ± 0.05"* — **no
depth**. The governing volume `SEWCP-700` specifies the fastener as `M4 × 10 SHCS` and states
**no plate-side tap depth anywhere**. The 8.0 mm figure was derivable from no volume and
authorised by no approval: **an implementing agent chose it**, froze it into a registered
artifact, and `APR-017` then certified that no engineering value had been set.

## What is approved

**Option A**, in the words put to the approver:

> Strike the depth. `CP-D09a`/`CP-D10a` become "M4 × 0.7" with no depth, and the depth is
> added to `ECR-D-007` as a fifth requested action alongside the keep-out row it interacts
> with. Restores the frozen artifact to exactly what was approved.

Options B (authorise 8.0 mm now) and C (authorise a different depth) were presented and **not
approved**.

## Why the value was not simply authorised

Thread engagement for an `M4 × 10` screw traversing a 5.50 mm locator needs only **4.50–6.70
mm**. At 8.0 mm the thread reaches **11.0 mm** below the top face — past the 8.00 mm
channel-to-top-face wall (`CP-D07`) — and is then kept clear of the coolant circuit only by the
**3.35 mm** radial margin that `ECR-D-007` requested action 2 already questions against the
3.5 mm demanded of the M5/M6 analogues. Fixing the depth in isolation would settle one input
to a calculation whose other inputs are open.

## The edit

| Ref | Was | Now |
|---|---|---|
| `CP-D09a` | `M4 × 0.7, **8.0 deep**` | `M4 × 0.7, **depth TBD — ECR-D-007**` |
| `CP-D10a` | `M4 × 0.7, **8.0 deep**` | `M4 × 0.7, **depth TBD — ECR-D-007**` |

Two table cells. No other dimension, tolerance, datum, fit or interface changes. `SEWCP-700`,
`SEWCP-400`, `SEWCP-300` and every other volume are untouched.

**This leaves `spec/01` carrying a declared TBD.** That is deliberate and is the point of
Option A: an explicit, attributed gap that `ECR-D-007` owns is safe, and a number nobody
authorised is not. A CAD modeller reading `depth TBD — ECR-D-007` is stopped; one reading
`8.0 deep` would have proceeded on a value with no authority behind it.

## Authority

`BINDING.approval_authority` is `human-owner`. `mechanical.design-engineer` is UNASSIGNED.
**No engineering value is set by this approval** — it removes one. The claim is checkable: the
diff deletes a number and adds no number.
