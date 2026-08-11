# APR-036 — Registration of `AIEF-AMD-015` in the freeze registry

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-approval requirement of LAW-01 and LAW-10 for the freeze-registry addition required by `AIEF-AMD-008` §AMD-21.

```yaml
approval_id:   APR-036
approver:      claude-under-owner-delegation   # NOT a human approval - see AUTHORITY
timestamp:     2026-08-11T00:00:00Z
subject_path:  framework/AIEF-AMD-015_Lock_Boot_Read_Prefix_And_Member_Order.md
subject_hash:  195302214a14ab38d9c595dee35c5eb6a930f5f90c4c70854488ff62207c6ae4
prior_hash:    null                   # not previously registered
ecr:           ECR-D-014
session:       S-2026-08-11-06
applied_by:    claude-under-owner-delegation · S-2026-08-11-06
scope:         Addition of the named artifact to the FROZEN.md registry at the stated hash,
               under the AMD-21 registration criterion. No byte of the subject is modified.
               AUTHORITY - "Owner-delegated engineering authority exercised by Claude" under the
               owner's written instruction of 2026-08-11. It is NOT an actual human approval and
               is never to be cited as one. Provenance record -
               .ai/project/decisions/DECISIONS_S-2026-08-11-06.md DEC-06.
```

---

**Liveness is not asserted here.** Determine it with `python -m aief_approval verify`.

## Subject

`framework/AIEF-AMD-015_Lock_Boot_Read_Prefix_And_Member_Order.md`, at DC-1 normalised SHA-256

```
195302214a14ab38d9c595dee35c5eb6a930f5f90c4c70854488ff62207c6ae4
```

Dual-computed. **This approval is void if the subject changes.** It grants nothing beyond this one
path at this one digest and authorises no future registration.

## Rationale

`AIEF-AMD-008` §AMD-21: an artifact is registered if it is *an authorising instrument for a change
to a frozen artifact, or the record of the authority under which such a change was made.*
`AIEF-AMD-015` is both — it authorises two changes to `framework/framework.manifest.json`, a
registered artifact, and it is the record of the delegated authority under which they were made.

**This registration is filed in the same edit as the change it authorises**, which is what
`AIEF-AMD-014` failed to do and what `ECR-D-006` §8 records. The immediately preceding instrument
of this repository was applied without either of its approvals being filed and without its
registry row being added, and the omission stood undetected for three sessions until `V-24` named
it. LAW-01 clause 5 — *"Hash registry is updated atomically with any approved change"* — is
followed here in the strict sense: `APR-035`, `APR-036`, the two `FROZEN.md` row changes, the
recomputed aggregate and `STATE.frozen_set_hash` are one act.

## Registry effect

| | |
|---|---|
| Rows | 30 → **31** |
| Added | `framework/AIEF-AMD-015_…` at `19530221…207c6ae4` |
| Changed in the same atomic edit | the `framework/framework.manifest.json` row, under `APR-035`, `920eb6ee…` → `5b78d25b…` |
| DC-2 aggregate | `19989657464c…8ddc07e` → `701db1fd2fac…f618aa50`, recomputed over the 31 rows, dual-computed |
| `STATE.frozen_set_hash` | follows the aggregate |
| Verification after the change | **31 of 31 reproduce** — computed, not asserted, by precondition `V-24` |

## Authority chain

| | |
|---|---|
| `AIEF-AMD-008` §AMD-21 | The registration criterion this artifact meets |
| LAW-01 clause 5 | Hash registry is updated atomically with any approved change |
| LAW-10 | Approval is an artifact bound to a content hash |
| `core/PRECEDENCE.md` rank 1 | The owner's written instruction of 2026-08-11 |
| ECR-D-014 | The change request this approval dispositions, jointly with `APR-035` |
