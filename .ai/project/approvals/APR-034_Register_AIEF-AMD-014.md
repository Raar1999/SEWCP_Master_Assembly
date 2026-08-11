# APR-034 — Registration of `AIEF-AMD-014` in the freeze registry

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-approval requirement of LAW-01 and LAW-10 for the freeze-registry addition required by `AIEF-AMD-008` §AMD-21.

```yaml
approval_id:   APR-034
approver:      claude-under-owner-delegation   # NOT a human approval - see AUTHORITY
timestamp:     2026-08-11T00:00:00Z
subject_path:  framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md
subject_hash:  07ced7582c7dafc8649eb8ac0736d1587ba4cc38c30f11c929240809be639945
prior_hash:    null                   # not previously registered
ecr:           ECR-D-006
session:       S-2026-08-11-06
applied_by:    claude-under-owner-delegation · S-2026-08-11-06
scope:         Addition of the named artifact to the FROZEN.md registry at the stated hash,
               under the AMD-21 registration criterion. No byte of the subject is modified.
               AUTHORITY - "Owner-delegated engineering authority exercised by Claude" under
               the owner's written delegation of 2026-08-11. It is NOT an actual human approval
               and is never to be cited as one. Provenance record -
               .ai/project/decisions/DECISIONS_S-2026-08-11-06.md DEC-05.
```

---

**Liveness is not asserted here.** Determine it with `python -m aief_approval verify`.

## Subject

`framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md`, at DC-1 normalised SHA-256

```
07ced7582c7dafc8649eb8ac0736d1587ba4cc38c30f11c929240809be639945
```

Dual-computed, as for `APR-033`. **This approval is void if the subject changes.** It grants
nothing beyond this one path at this one digest and authorises no future registration.

## Rationale — why this was owed and never filed

`AIEF-AMD-008` §AMD-21 states the registration criterion for the `framework/` partition: an
artifact is registered if it is *an authorising instrument for a change to a frozen artifact, or
the record of the authority under which such a change was made.* `AIEF-AMD-014` is both. It
authorises eleven changes to `framework/framework.manifest.json` — a registered artifact — and it
is the record of the human owner's OQ-15 decision.

`AIEF-AMD-014` says so itself, twice: § *Blast Radius* lists *"`framework/AIEF-AMD-014_…` —
**NEW** — this instrument — Registered in `FROZEN.md` under `APR-015` (AMD-21 criterion)"*, and
§ *Approvals Required and Recorded* names the same. **Neither `APR-015` nor `APR-014` was ever
filed**, and the registry addition they were to authorise was never made: `FROZEN.md` stood at
29 rows with `AIEF-AMD-014` absent, and `check_v24` names the omission in terms —
*"AMD-21 criterion candidate unregistered: framework/AIEF-AMD-014_…"*.

This is the second half of the ECR-D-006 defect and was not in the ECR record as filed. It was
found by this session's audit, is recorded on the ECR record, and is repaired here.

## Why `APR-034` and not `APR-015`

`AIEF-AMD-014` is a **frozen instrument** and its text is not edited by this session. That text
describes `APR-014` and `APR-015` with specific content — in particular an `APR-014` whose
`prior_hash` is the measured pre-change digest `e87ae68e…`. Filing artifacts under those
identifiers today, with different content and a different basis, would make a frozen instrument
misdescribe two live records, and would leave a reader unable to tell that the originals were
never written.

The originals were never written. **That fact is evidence and is preserved.** The approval series
therefore continues at its own high-water mark: `APR-033` and `APR-034`, filed
`S-2026-08-11-06`. The identifiers `APR-014` and `APR-015` are hereby recorded as **never
filed** — not reserved, not lost, not superseded, and not to be issued to anything else.

## Registry effect

| | |
|---|---|
| Rows | 29 → **30** |
| Added | `framework/AIEF-AMD-014_…` at `07ced758…be639945` |
| Also changed in the same atomic edit | the `framework/framework.manifest.json` row, under `APR-033` |
| DC-2 aggregate | `e558734052f3…f592ddf` → `19989657464c…8ddc07e` — recomputed over the 30 rows, dual-computed |
| `STATE.frozen_set_hash` | follows the aggregate |
| Verification after the change | **30 of 30 reproduce**, computed not asserted: `python -m aief_stage6` precondition `V-24` |

## Authority chain

| | |
|---|---|
| `AIEF-AMD-008` §AMD-21 | The registration criterion this artifact meets |
| LAW-01 clause 5 | Hash registry is updated atomically with any approved change |
| LAW-10 | Approval is an artifact bound to a content hash |
| `core/PRECEDENCE.md` rank 1 | The owner's written delegation of 2026-08-11 |
| ECR-D-006 | The change request this approval dispositions, jointly with `APR-033` |
