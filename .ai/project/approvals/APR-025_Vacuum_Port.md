# APR-025 — Vacuum Port - derived mass reference

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the dispositions named below.

```yaml
approval_id:   APR-025
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-10T00:00:00Z
subject_path:  spec/07_SEWCP-800_Vacuum_Port.md
subject_hash:  7558bc5b0f613ab9184d66dba6afd6674214d33302775eee2515bd25c8122afe
prior_hash:    1b7b5914202f4ec631f5fad9daf2e41d215e5d80e07a4e289482c85d6068989f
ecr:           ECR-D-002
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

Two rationale references to a 3.9 kg plate -> 4.0 kg, following `APR-019`'s mass estimate.
No dimension, requirement or interface changes.


## How the approver was consulted

The dispositions above were put to the human owner as selectable options in session
`S-2026-08-10-01`, each with its recommendation, engineering consequences, reversibility and
gate impact stated. The selected option is recorded in each ECR record at its Disposition
section, together with the options presented and **not** approved. **This artifact binds those
selections to the bytes that resulted from them**; the hash was computed after the edits, which
is why it could not have been quoted at the moment of selection.
