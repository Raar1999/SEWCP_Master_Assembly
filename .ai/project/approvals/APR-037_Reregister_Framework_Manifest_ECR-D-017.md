# APR-037 — Re-registration of `framework.manifest.json` under ECR-D-017 disposition A

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-approval requirement of LAW-01 and LAW-10 for the manifest change made under ECR-D-017.

```yaml
approval_id:   APR-037
approver:      claude-under-owner-delegation   # NOT a human approval - see AUTHORITY
timestamp:     2026-08-17T00:00:00Z
subject_path:  framework/framework.manifest.json
subject_hash:  759f774b727c43a0f96845aa5ac12a05a1158b60c27ba8b31d963a33cde74e3b
prior_hash:    5b78d25b00a405c61715752e6aad1084dc7852048c0074d9c3c948ffbbd6b652
supersedes:    APR-035
ecr:           ECR-D-017
session:       S-2026-08-17-01
applied_by:    claude-under-owner-delegation · S-2026-08-17-01
scope:         Three leaf values change and nothing else - metadata.license, and the authority
               fields of digest_constructions.core_aggregate and budget_measurement_record.
               Zero removals, zero additions, proven by structural diff over the parsed JSON
               rather than by inspection. No token_cap, no files[] entry, no dependency edge,
               no validation entry and no digest construction is touched; MI-4 is unchanged at
               5904 of 6000 and DC-4 is unaffected, because the manifest is not in the covered
               set. AUTHORITY - "Owner-delegated repository and licence authority exercised by
               Claude" under the owner's written instruction of 2026-08-17, which names licence
               selection expressly: "license selection appropriate for the intended release, if
               the governing project state does not already define one". It is NOT an actual
               human approval and is never to be cited as one. Provenance record -
               .ai/project/decisions/DECISIONS_S-2026-08-17-01.md DEC-11 and DEC-15.
```

---

**Liveness is not asserted here.** Determine it with `python -m aief_approval verify`.

## Subject

`framework/framework.manifest.json`, at DC-1 normalised SHA-256

```
759f774b727c43a0f96845aa5ac12a05a1158b60c27ba8b31d963a33cde74e3b
```

`prior_hash` is `5b78d25b…bbd6b652`, which is `APR-035`'s `subject_hash` and the state the
independent `OI-V-13` audit reproduced from the working tree. **This chain link is a measured
value, not a reconstruction** — the distinction `APR-033` had to make, and the reason it
departed from `AIEF-AMD-014` §AMD-53. It does not arise here: the predecessor state was
committed, is in the object graph, and was independently verified two hours before this
approval was written.

## The change, enumerated

| # | Path | Before | After |
|---|---|---|---|
| 1 | `metadata.license` | `"TBD-at-release"` | the ratified dual-licence expression, naming `LICENSE` as the authority for the path boundary and `DEC-11` as the decision |
| 2 | `metadata.reproducible.digest_constructions.core_aggregate.authority` | cites AMD-010 AMD-27 and AMD-012 AMD-39 | **appends** the AMD-015 AMD-54/AMD-55 citation |
| 3 | `metadata.reproducible.budget_measurement_record.authority` | cites AMD-010 AMD-29, AMD-013 AMD-42/45, AMD-014 AMD-51 | **appends** the AMD-015 AMD-54 citation |

**Three leaves, and the count is proven rather than asserted.** The change was applied by
surgical replacement on the raw octets — never by re-serialising the document, which would
have reformatted unrelated lines and made the diff unreviewable — and then verified by walking
both parsed trees to their leaves: **3 changed, 0 removed, 0 added.**

## What does not move, and why it matters

| | |
|---|---|
| `DC-4` / `MANIFEST.lock.aggregate_digest` / `BINDING.core_digest_pin` | **Unchanged.** The covered set is every `.ai/core/**` file except the self-excluded lock, plus three root-partition files. `framework/framework.manifest.json` is in none of it. **B2a is unaffected and continues to pass.** |
| `MI-4` | **5904 of 6000.** No `token_cap` is touched |
| Every digest construction | Untouched. None of the three values is read by DC-1, DC-2, DC-3, DC-4 or DC-5 — all three are prose |
| `LC-M04-EXIT` | Unaffected; `GATES.md` excludes this path from the gate by name |
| `spec/**`, `cad/**`, `drawings/**`, deliverables | Not touched. No verified geometry moved |

## What does move, and is repaired in the same act

| | |
|---|---|
| `FROZEN.md` row for this path | Re-registered at `759f774b…cde74e3b`. `V-24` fails until it is, and that is the mechanism working |
| `FROZEN.md` aggregate and `STATE.frozen_set_hash` | DC-2 recomputed over the 31-member registry |
| `core/MANIFEST.lock.build_provenance.source_manifest_dc1` | Pins the manifest's DC-1, so the lock went stale the moment this change landed. **Stage 6 re-emitted** under the standing `OQ-14` authorization; `source_manifest_dc1` and the run-scoped `budget_measurement` fields change, and nothing else |

## Authority chain

| Source | What it supplies |
|---|---|
| LAW-01 | A frozen artifact changes only by an approved ECR and a recorded approval |
| LAW-10 | Approval is an artifact bound to a content hash |
| `core/PRECEDENCE.md` rank 1 | The owner's written instruction of 2026-08-17, which delegates licence selection in terms |
| `project/BINDING.md` | `approval_authority: human-owner` — **delegated in its exercise for this run, not transferred** |
| `ECR-D-017` | The change request this approval dispositions |
| `AIEF-AMD-008` §AMD-21 | The registration criterion this artifact meets |
| `ECR-D-005` / `APR-001`, `ECR-D-006` / `APR-033` | The disposition-A re-registration precedent followed here |

**This is not a human approval.** It is an owner-delegated act, recorded as such, and the
delegation reaches licence selection because the owner's instruction names it. It does **not**
reach anything the owner reserved: no `OQ` reservation is discharged here, and `OQ-14`'s
authorization is **reused, not re-granted** — the owner's 2026-08-11 instruction authorised
Stage 6 execution, and a re-emission forced by an authorised manifest change is that same
execution, not a new one.
