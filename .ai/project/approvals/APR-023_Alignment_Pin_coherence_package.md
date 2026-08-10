# APR-023 — Alignment Pin coherence package

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the dispositions named below.

```yaml
approval_id:   APR-023
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-10T00:00:00Z
subject_path:  spec/06_SEWCP-700_Alignment_Pins.md
subject_hash:  da702fe05f41b1bac39c3ca507c090a7f7e7258ae18db38addb4d079d755edc6
prior_hash:    0d2aa747fcca37574090ebff022f51924e66c7c845ecb9e2c0fea991155dcdc2
ecr:           ECR-D-002, ECR-D-007, ECR-D-009, ECR-D-010
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

| ECR | What changed |
|---|---|
| `ECR-D-002` | Two rationale references to a 3.9 kg plate -> 4.0 kg |
| `ECR-D-007` | `AP-D03` flange Ø12.000 -> **Ø10.000**; §8 and §9 datum and fit-stack terms follow |
| `ECR-D-009` | `AP-IF-1` rewritten; `AP-D03` k6 -> h6; `AP-D07` and `AP-D08` struck; `AP-D12` 5.50 -> 9.50; `AP-D13` spigot and `AP-D14` hex socket added; §6 steps 2, 4, 7; §10 steps 3 and 5 |
| `ECR-D-010` | `AP-IF-3` re-clocked to 75/195/315 |


## How the approver was consulted

The dispositions above were put to the human owner as selectable options in session
`S-2026-08-10-01`, each with its recommendation, engineering consequences, reversibility and
gate impact stated. The selected option is recorded in each ECR record at its Disposition
section, together with the options presented and **not** approved. **This artifact binds those
selections to the bytes that resulted from them**; the hash was computed after the edits, which
is why it could not have been quoted at the moment of selection.
