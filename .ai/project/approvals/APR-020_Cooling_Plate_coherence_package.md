# APR-020 — Cooling Plate coherence package

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the dispositions named below.

```yaml
approval_id:   APR-020
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-10T00:00:00Z
subject_path:  spec/01_SEWCP-200_Cooling_Plate.md
subject_hash:  55b47ca30eeac99ca231d960a1066411b827bf6da139d5e7d178db6a182c3a39
prior_hash:    36e8d35b1004c22279abc67fe81447632d87a934bf057e8366e5f5a1160abdda
ecr:           ECR-D-002, ECR-D-003, ECR-D-004, ECR-D-007, ECR-D-009, ECR-D-010
session:       S-2026-08-10-01
scope:         Only the changes enumerated below, in this one artifact. Every other
               byte of this file is unchanged and no other volume is approved here.
```

---

**Liveness is not asserted in this file.** Determine it with
`python -m aief_approval verify`, which computes the supersession relation the human owner
ruled in session `S-2026-08-10-01` and which `GATES.md` records: an approval is **LIVE** when
its `subject_hash` equals the current DC-1 of `subject_path`, **SUPERSEDED-VALID** when an
unbroken chain of approvals on that path reaches a LIVE one, and **VOID** otherwise. A
hand-written status label went stale four times in this repository before that rule existed.

## What is approved

Six dispositions land in this volume and are enumerated so that nothing rides along:

| ECR | What changed |
|---|---|
| `ECR-D-002` | **The unapplied half of an already-approved disposition.** §6 step 3 still directed *"10 W x 8 D"* after `APR-019` reduced `CP-D06` to 6.00. That is the machining instruction; a shop following it would have re-cut the 2.00 mm Z-stack error `APR-019` was issued to close |
| `ECR-D-003` | `CP-IF-10` dimensioned; `CP-D22`-`CP-D25` added; §3.1 port exception; §4 SEWCP-201 row; §6 steps 3 and 10; §9 controls; FM #8 restated |
| `ECR-D-004` | `CP-IF-3` counterbore dimensioned and declared slotted and masked; `CP-D26` added; `CP-D21` closed loop broken; §6 step 13 mask list; §9 position control |
| `ECR-D-007` | §3.1 kinematic-locator keep-out row; `CP-D09a` / `CP-D10a` tap depths; `CP-D09` / `CP-D10` reduced to O10.000 |
| `ECR-D-009` | `CP-IF-1` / `CP-IF-4` integral locator; §6 step 12 and §10 step 3 torque 2.5 -> 1.2 N.m |
| `ECR-D-010` | `CP-IF-4` and `CP-D10` re-clocked to 75/195/315 |


## How the approver was consulted

The dispositions above were put to the human owner as selectable options in session
`S-2026-08-10-01`, each with its recommendation, engineering consequences, reversibility and
gate impact stated. The selected option is recorded in each ECR record at its Disposition
section, together with the options presented and **not** approved. **This artifact binds those
selections to the bytes that resulted from them**; the hash was computed after the edits, which
is why it could not have been quoted at the moment of selection.
