# APR-024 — Support Ring - closing the ECR-D-001 recorded residual

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the dispositions named below.

```yaml
approval_id:   APR-024
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-10T00:00:00Z
subject_path:  spec/03_SEWCP-400_Chuck_Support_Ring.md
subject_hash:  a2f951a1c749b688141d8245f8575ed6aabf28df03b55788a0d762f4e6c7dcbf
prior_hash:    b00d52899f36f0bfe6a05cc209ca40876ba5fa6fac9169e5d100bc5346a62655
ecr:           ECR-D-001
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

`SR-IF-4` instructed *"Ø6 h6 dowels **pressed into** the Cooling Plate"* while the governing
volume forbids press tooling absolutely (`spec/06` §10 step 3, §11 FM #5). `ECR-D-001` §7
recorded this as a knowingly-accepted residual because those volumes were outside `APR-016`'s
scope. **A live interface statement directing a prohibited process is not a residual that can
be carried into CAD**, so it is closed here, together with five nomenclature references to
"dowels" that now read "locator bosses".


## How the approver was consulted

The dispositions above were put to the human owner as selectable options in session
`S-2026-08-10-01`, each with its recommendation, engineering consequences, reversibility and
gate impact stated. The selected option is recorded in each ECR record at its Disposition
section, together with the options presented and **not** approved. **This artifact binds those
selections to the bytes that resulted from them**; the hash was computed after the edits, which
is why it could not have been quoted at the moment of selection.
