# APR-022 — Heater Plate coherence package

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the dispositions named below.

```yaml
approval_id:   APR-022
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-10T00:00:00Z
subject_path:  spec/02_SEWCP-300_Heater_Plate.md
subject_hash:  0290580066829963de1c9bbbd059f5f088e442031d679cf4ddf5046693d66aef
prior_hash:    ab36e082749fa4ea08c9f0f6a6c98cb481491cb601dc4c5cc947ba3634537608
ecr:           ECR-D-004, ECR-D-007, ECR-D-010, ECR-D-011
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
| `ECR-D-004` | `HP-D12` gains a depth at last - blind, 6.50 +0.30/-0, 1xD insert, 1.50 mm min to the bond face, criticality Low -> High; `HP-IF-2` and §10 step 13 restated |
| `ECR-D-007` | `HP-D09a` kinematic slot depth 3.00 +/-0.10 |
| `ECR-D-010` | `HP-IF-3` and `HP-D11` re-clocked to 75/195/315 |
| `ECR-D-011` | New §3.2 heater-groove keep-out; §6 step 3 routing instruction |


## How the approver was consulted

The dispositions above were put to the human owner as selectable options in session
`S-2026-08-10-01`, each with its recommendation, engineering consequences, reversibility and
gate impact stated. The selected option is recorded in each ECR record at its Disposition
section, together with the options presented and **not** approved. **This artifact binds those
selections to the bytes that resulted from them**; the hash was computed after the edits, which
is why it could not have been quoted at the moment of selection.
