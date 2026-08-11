# APR-035 — Amendment of `framework.manifest.json` under AIEF-AMD-015 (ECR-D-014 disposition A)

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-approval requirement of LAW-01 and LAW-10 for the manifest change made by AIEF-AMD-015.

```yaml
approval_id:   APR-035
approver:      claude-under-owner-delegation   # NOT a human approval - see AUTHORITY
timestamp:     2026-08-11T00:00:00Z
subject_path:  framework/framework.manifest.json
subject_hash:  5b78d25b00a405c61715752e6aad1084dc7852048c0074d9c3c948ffbbd6b652
prior_hash:    920eb6eec217732152c452d51f01e471940df6f2e2ffe608c377fccc37814090
supersedes:    APR-033
ecr:           ECR-D-014
session:       S-2026-08-11-06
applied_by:    claude-under-owner-delegation · S-2026-08-11-06
scope:         Amendment of the named artifact by AIEF-AMD-015 rulings AMD-54 and AMD-55, and
               re-registration in FROZEN.md at the stated subject_hash. Two normative clause
               bodies change - budget_measurement_record.lock_self_measurement and
               digest_constructions.core_aggregate.lock_serialisation - and nothing else. No
               token_cap changes; MI-4 is unchanged at 5904 of 6000. AUTHORITY - "Owner-delegated
               engineering authority exercised by Claude" under the owner's written instruction
               of 2026-08-11: "If a software/architecture gap exists: repair it at the owning
               layer. Test it. Verify it. Continue." It is NOT an actual human approval and is
               never to be cited as one. Provenance record -
               .ai/project/decisions/DECISIONS_S-2026-08-11-06.md DEC-06.
```

---

**Liveness is not asserted here.** Determine it with `python -m aief_approval verify`.

## Subject

`framework/framework.manifest.json`, at DC-1 normalised SHA-256

```
5b78d25b00a405c61715752e6aad1084dc7852048c0074d9c3c948ffbbd6b652
```

Dual-computed — once by `src/aief_stage6/digests.py`, once by an independent implementation
written from the manifest's own DC-1 text importing nothing from `src/`. The two agree.

`prior_hash` is `920eb6ee…37814090`, the state `APR-033` bound. **Unlike `APR-033`'s own
`prior_hash`, this one is a measurement**: it was measured from the working tree at the start of
this session and is the DC-1 of the `HEAD` blob at `5e7ac74`, recoverable with
`git show 5e7ac74:framework/framework.manifest.json`. The chain from here back to `APR-006`'s
`ae16ccac…` is reproducible from git alone.

## What is approved — three changes, and no others

| # | Location | Change | Ruling |
|---|---|---|---|
| 1 | `metadata.reproducible.budget_measurement_record.lock_self_measurement` | The existing text is retained **verbatim and entire**; the boot-read-prefix declaration is **appended** to it | `AIEF-AMD-015` §AMD-54 |
| 2 | `metadata.reproducible.digest_constructions.core_aggregate.lock_serialisation` | The member-order list is amended — `aggregate_digest` moves from fifth position to second — and the amendment is appended with its reason and measurements. The `aggregate_digest precedes files` clause and the `files is an array of [path, digest] pairs in DC-4 record order` clause are retained **verbatim** | `AIEF-AMD-015` §AMD-55 |
| 3 | *(carried inside change 1)* | The `lock_self_measurement` authority citation gains `AIEF-AMD-015 AMD-54` | — |

**Explicitly unchanged, and each was checked after the edit:**

| | |
|---|---|
| `files[manifest-lock].token_cap` | **200** |
| Every other `token_cap` | unchanged |
| MI-4 = Σ `token_cap` over T0∪T1 | **5904 ≤ 6000**, headroom **96** |
| `version.min_context_window` | unchanged — the ratified 32,000-token portability floor is untouched |
| `files[]` count | 108 |
| `dependencies.edges` count | 33 |
| `validation` count | 25 — **`V-09.verifies` is not amended**, because it already points at `lock_self_measurement` by name and the pointer carries the new content |
| `generation_order` | unchanged |
| DC-1, DC-2, DC-3, DC-4, DC-5 constructions | unchanged |

## Why this is not a cap raise in disguise

A reader is entitled to suspect that "re-scope the measured quantity" is "raise the cap" with
better manners. It is not, and the arithmetic is the answer:

- A cap raise would move MI-4. **MI-4 does not move.** It is 5904 before and after, and the
  headroom is 96 before and after.
- A cap raise would have to reach **6469** to admit the artifact, putting Σ at 12173 against a
  6000 ceiling. That is `AIEF-AMD-013` §AMD-41 §5(iii)'s determinately-inadmissible finding.
- The *only* cap value MI-4 admits is 296, and 296 was **rejected** at `ECR-D-014` §5 alternative
  C — it fits by five tokens, consumes all remaining headroom, and would leave the cap bounding a
  region containing `build_id`, a string no clause bounds.

The ruling instead identifies which octets the existing 200 was always stated to bound —
`lock_serialisation` says so in terms — and moves one member so that the bound is met with a
2.9× margin by a quantity the specification fully determines.

## Measured consequence

| | TF-1 | TF-2 (governing) | Cap | Verdict |
|---|---|---|---|---|
| Lock boot-read prefix, after both rulings | 56 | **69** | 200 | **PASS** |
| Lock boot-read prefix, before AMD-55 (AMD-54 alone) | 234 | 291 | 200 | FAIL |
| Whole serialised lock | 5334 | 6469 | — | unbounded, recorded as `OI-C-14` |
| Charged aggregate (AMD-51, charge = declared 200) | 4140 | **4758** | 6000 | **PASS** |

## Alternatives rejected

Recorded in full at [`../ecr/ECR-D-014_Lock_Token_Cap_Unsatisfiable_By_Any_Conforming_Lock.md`](../ecr/ECR-D-014_Lock_Token_Cap_Unsatisfiable_By_Any_Conforming_Lock.md) §5:
B (raise to 6469 — breaches MI-4), C (raise to 296 — exhausts headroom, bounds a free-form
string), D (null cap — creates the `OI-C-08` exposure and discards AMD-51), E (shrink the covered
set — trades integrity for a token count), F (halt and reserve to the owner — considered
seriously; the owner's instruction directs otherwise and the remedy space holds no live
discretionary alternative).

## Residual, recorded and not closed

The whole-document size of `core/MANIFEST.lock` is now bounded by nothing. Raised as `OI-C-14`.
This approval does not close it and does not assert that it is harmless — only that no invariant
ranges over it today.

## Authority chain

| | |
|---|---|
| LAW-01 | A frozen artifact is changed only by an approved ECR and a recorded approval; clause 5, the registry updates atomically |
| LAW-02 clauses 2, 4, 5 | ECR-D stops the affected work — Stage 6 halted; disposition requires human involvement and re-gating; not closable by the raiser. **The raiser of `ECR-D-014` is this session.** LAW-02 clause 5 is therefore **NOT satisfied on its own terms** for this ECR, and that is recorded rather than finessed: the owner's delegation supplies clause 4's human involvement, and clause 5's independence is owed as the `OI-V-13` cold audit |
| LAW-10 | Approval is an artifact bound to a content hash |
| `core/PRECEDENCE.md` rank 1 | The owner's written instruction of 2026-08-11 |
| `AIEF-AMD-008` §AMD-21 | The registration criterion |
| ECR-D-014 | The change request this approval dispositions |
