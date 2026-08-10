# APR-026 — Specification index - derived value

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the dispositions named below.

```yaml
approval_id:   APR-026
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-10T00:00:00Z
subject_path:  spec/README.md
subject_hash:  1d7720723ddd42028a9536ec20cfb50a9a8b803bc3172423b31f108a7f93416c
prior_hash:    95da15c691bac4ab61c3450efdc71428a5807fec1c3a32b81213f3490181370c
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

The summary line carried `Re ~ 7,400`, superseded by `APR-019` to `Re ~ 8,300`.
No other change.


## How the approver was consulted

The dispositions above were put to the human owner as selectable options in session
`S-2026-08-10-01`, each with its recommendation, engineering consequences, reversibility and
gate impact stated. The selected option is recorded in each ECR record at its Disposition
section, together with the options presented and **not** approved. **This artifact binds those
selections to the bytes that resulted from them**; the hash was computed after the edits, which
is why it could not have been quoted at the moment of selection.
