# APR-033 — Re-registration of `framework.manifest.json` at its measured digest (ECR-D-006 disposition A)

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-approval requirement of LAW-01 and LAW-10 for ECR-D-006 disposition A.

```yaml
approval_id:   APR-033
approver:      claude-under-owner-delegation   # NOT a human approval - see AUTHORITY
timestamp:     2026-08-11T00:00:00Z
subject_path:  framework/framework.manifest.json
subject_hash:  920eb6eec217732152c452d51f01e471940df6f2e2ffe608c377fccc37814090
prior_hash:    8af8971b78d762e5db2879e50585a78f4e6d497ea707c664a9c06e1ba7e42ff7
supersedes:    APR-012
ecr:           ECR-D-006
session:       S-2026-08-11-06
applied_by:    claude-under-owner-delegation · S-2026-08-11-06
scope:         Re-registration of the named artifact in FROZEN.md at the stated subject_hash,
               and re-affirmation of the AIEF-AMD-012, AIEF-AMD-013 and AIEF-AMD-014 manifest
               change sets that produced it. Disposition A of ECR-D-006. No byte of the
               manifest is modified by this approval. AUTHORITY - this approval records
               "Owner-delegated engineering authority exercised by Claude" under the owner's
               written delegation of 2026-08-11, which names ECR-D-006 expressly ("the owner
               has now explicitly delegated engineering decision authority to Claude for this
               run"). It is NOT an actual human approval and is never to be cited as one.
               Provenance record - .ai/project/decisions/DECISIONS_S-2026-08-11-06.md DEC-05.
```

---

**Liveness is not asserted here.** Determine it with `python -m aief_approval verify`.

## Subject

`framework/framework.manifest.json`, at DC-1 normalised SHA-256

```
920eb6eec217732152c452d51f01e471940df6f2e2ffe608c377fccc37814090
```

Normalisation per `metadata.reproducible.digest_constructions.per_artifact` (DC-1). The value
was computed **twice by independent means** — once by an implementation written this session
from the manifest's own normative text importing nothing from `src/`, and once by
`src/aief_stage6/digests.py`. The two agree. **This approval is bound to that hash** and is void
if the subject content changes.

## What is approved

1. **Re-registration.** `project/FROZEN.md` replaces the registered digest for this path,
   `8af8971b…a7e42ff7`, with the measured `920eb6ee…37814090`, and the DC-2 aggregate is
   recomputed over the resulting registry.
2. **Re-affirmation of the change sets.** The twenty-seven discrete changes between the last
   git-recoverable approved state of this artifact and its current content are re-affirmed as
   the approved content. They are enumerated below and each is attributed.

**Not approved, and not done:** any change to the manifest's content. The artifact is not
touched by this approval.

## Why `prior_hash` is `8af8971b…` — read this before citing it

`prior_hash` here names **`APR-012`'s declared subject state**, so that the recorded chain
`APR-001 → APR-002 → APR-004 → APR-006 → APR-010 → APR-012 → APR-033` is unbroken and the
supersession relation resolves without a fork.

**It is not a measurement, and this approval does not assert that the artifact ever normalised
to that value.** It demonstrably did not reproduce to it — that non-reproduction *is* ECR-D-006.
The pre-`AIEF-AMD-014` bytes were never committed (`OI-V-08`, `VER-007` FIND-Q7-8), so no
surviving artifact can be measured to settle it, and no session can now recover it.

The two alternatives were examined and rejected:

| Candidate `prior_hash` | Rejected because |
|---|---|
| `ae16ccac…9d8395aa` — the last state that both reproduces and carries an approval | `APR-010` already declares that state as its `prior_hash`. A second approval declaring it forks the history, which `aief_approval` fails as ambiguous, correctly |
| `e87ae68e…5a12cf892` — the value `AIEF-AMD-014` §AMD-53 §5 recommended | It is another session's reconstruction of bytes that no longer exist. **This session has not measured it and cannot.** Writing it here would be signing a measurement not taken — the precise thing §AMD-53 warns against when it says a hash is never invented. The recommendation is departed from on that ground, and the departure is recorded rather than silent |

## Evidence — the current bytes are the approved content

The attribution rests on a **git object**, not on a reconstruction. `AIEF-AMD-014` §AMD-53 §5's
second recommendation — *"commit before the next multi-session phase"* — was acted on at
`5e7ac74`, and that is what makes the following a two-command check rather than an inversion of
remembered edits:

```
git show 8546960:framework/framework.manifest.json   # DC-1 ae16ccaca5746b81…9d8395aa
```

`ae16ccac…` is `APR-006`'s `subject_hash`, the AIEF-AMD-010 state, and the value `VER-007` §5c
independently recorded four sessions before this one. The entire delta from it to the current
artifact was taken structurally — leaf by leaf over the parsed JSON, with `files[]` and
`dependencies.edges` compared as sets rather than by position — and every leaf maps to a named
ruling:

| # | Change | Ruling | Approval |
|---|---|---|---|
| 1 | `…core_aggregate.enabled_role_coverage` — new object, 5 members | `AIEF-AMD-012` §AMD-39 | `APR-010` |
| 2 | `…core_aggregate.authority` — extended | `AIEF-AMD-012` §AMD-39 | `APR-010` |
| 3 | `…core_aggregate.covers` — extended | `AIEF-AMD-012` §AMD-39 | `APR-010` |
| 4 | `…core_aggregate.lock_json_layout` — new | `AIEF-AMD-013` §AMD-43 (OQ-B1) | `APR-012` |
| 5 | `…per_artifact.empty_content` — new | `AIEF-AMD-013` §AMD-48 | `APR-012` |
| 6 | `…per_artifact.status` — extended | `AIEF-AMD-013` §AMD-48 | `APR-012` |
| 7 | `build_provenance_record` — new object, 12 leaves | `AIEF-AMD-013` §AMD-44 (OQ-B2) | `APR-012` |
| 8 | `binding_pin_write` — new object, 4 leaves | `AIEF-AMD-013` §AMD-47 (OQ-B5) | `APR-012` |
| 9 | `distributable.entry_types` — new | `AIEF-AMD-013` §AMD-46 (OQ-B4) | `APR-012` |
| 10 | `budget_measurement_record.measurement_domain` — new | `AIEF-AMD-013` §AMD-42 | `APR-012` |
| 11 | `budget_measurement_record.measurement_instant` — new | `AIEF-AMD-013` §AMD-42 | `APR-012` |
| 12 | `budget_measurement_record.lock_self_measurement` — new | `AIEF-AMD-013` §AMD-45 (OQ-B3) | `APR-012` |
| 13 | `budget_measurement_record.authority` — extended | `AIEF-AMD-013` §§AMD-42/45 | `APR-012` |
| 14 | `build_time_reproducibility.run_fixed_values` — new | `AIEF-AMD-013` §AMD-48 | `APR-012` |
| 15 | `build_time_reproducibility.authority` — extended | `AIEF-AMD-013` §AMD-48 | `APR-012` |
| 16 | `validation[V-09].verifies` — extended | `AIEF-AMD-013` §§AMD-42/45 | `APR-012` |
| 17 | `metadata.reproducible.bounded_register_split` — new object, 11 leaves | `AIEF-AMD-014` §AMD-49 | **this approval** |
| 18 | `files[open-items-register]` — new entry, 14 fields | `AIEF-AMD-014` §AMD-49 | **this approval** |
| 19 | `files[state-register]` — new entry, 14 fields | `AIEF-AMD-014` §AMD-49 | **this approval** |
| 20 | edge `state → state-register` (`references`) | `AIEF-AMD-014` §AMD-49 | **this approval** |
| 21 | edge `open-items → open-items-register` (`references`) | `AIEF-AMD-014` §AMD-49 | **this approval** |
| 22 | `files[boot].token_cap` 400 → 504 | `AIEF-AMD-014` §AMD-50 | **this approval** |
| 23 | `validation[V-03].verifies` — extended | `AIEF-AMD-014` §AMD-49 | **this approval** |
| 24 | `validation[V-09].verifies` — extended again | `AIEF-AMD-014` §AMD-51 | **this approval** |
| 25 | `budget_measurement_record.aggregate_ceiling_charge` — new | `AIEF-AMD-014` §AMD-51 | **this approval** |
| 26 | `budget_measurement_record.verdict_rule` — extended | `AIEF-AMD-014` §AMD-51 | **this approval** |
| 27 | `budget_measurement_record.authority` — extended again | `AIEF-AMD-014` §AMD-51 | **this approval** |

Three independent corroborations that the enumeration is complete:

1. **Nothing was removed.** Zero leaves, zero `files[]` entries, zero `dependencies.edges`
   deleted. `files[]` 106 → 108, edges 31 → 33, `validation` 25 → 25.
2. **The manifest is self-attributing.** Every one of the extended text values names its own
   authorising amendment inside the value — *"per AIEF-AMD-014 AMD-51"*, *"declared by
   AIEF-AMD-013 AMD-48"*, *"extended … by AIEF-AMD-012 AMD-39"*. An unattributed extension would
   be visible as an extension carrying no citation. None is.
3. **The counts match the instruments' own enumerations, exactly.** `AIEF-AMD-012` declares
   three changes; rows 1–3 are three. `APR-012` declares thirteen; rows 4–16 are thirteen.
   `AIEF-AMD-014` declares *"eleven changes … four new members or entries, two new dependency
   edges, one `token_cap` value, and four extensions to existing text"*; rows 17–27 are eleven,
   and they partition exactly 4 / 2 / 1 / 4.

**No unauthorised member, value, entry, edge or cap is present.**

## What this approval does not repair

`APR-012`'s binding to the digest it names remains unreproducible. Re-registration repairs the
*registry*; it does not retroactively supply a reproducible binding for a state that was never
committed. `AIEF-AMD-014` §AMD-53 §4 said so, and it is still true. What has changed since is
that the artifact's **current** state is now a git object with a complete, mechanical attribution
back to an approved state that is also a git object — so the gap is bounded, named, and cannot
grow.

The residual is recorded on the ECR record and in `FROZEN.md`'s registration history. It is not
closed by this approval and is not asserted to be.

## Alternatives rejected

| | |
|---|---|
| **B — revert to `ae16ccac…`** | Discards three approved amendments and every Stage 6 construction they declare: DC-4 enabled-role coverage, the lock JSON layout, `build_provenance`, the BINDING pin write, archive entry types, the budget measured domain, DC-1 of empty content, run-fixed values, the bounded register split and the `BOOT.md` cap. It would un-implement `src/aief_stage6/**`, re-open `CMP-BLOCK-006`, and re-break `V-09`. Rejected |
| **C — waive** | `V-24` is an AMD-31 compile-time precondition; Stage 6 would then seal an unproven provenance chain into `MANIFEST.lock` through `build_provenance.source_manifest_dc1`. Rejected — this is the ECR-D-005 disposition-C reasoning, unchanged |
| **D — re-register at `8af8971b…`** | Would require the artifact to be edited until it hashes to a value no construction of it produces. A hash is never invented. Rejected |
| **E — re-register the manifest only, leaving `AIEF-AMD-014` unregistered** | `V-24` fails on the AMD-21 criterion by name; the repair would be half a repair. Rejected — see `APR-034` |

## Authority chain

| | |
|---|---|
| LAW-01 | A frozen artifact is changed only by an approved ECR and a recorded approval; clause 5, the registry updates atomically with the approved change |
| LAW-02 clauses 4–5 | ECR-D disposition requires human involvement and re-gating; no ECR is closed by the agent that raised it. The raiser is `chief-systems-engineer · S-2026-08-08-12`; this is a different session and a different role, and the human involvement is the owner's written delegation |
| LAW-10 | Approval is an artifact bound to a content hash |
| `core/PRECEDENCE.md` rank 1 | The owner's written delegation of 2026-08-11, which names ECR-D-006 expressly |
| `project/BINDING.md` | `approval_authority: human-owner` — **delegated in its exercise for this run, not transferred** |
| ECR-D-006 | The change request this approval dispositions |
| `AIEF-AMD-008` §AMD-21 | The registration criterion this artifact meets |
| `ECR-D-005` / `APR-001` | The disposition-A precedent followed here |

---

## Corrections of record — `S-2026-08-17-01`

> **Appended, never applied in place.** This approval's `subject_hash` binding, its
> attribution and its disposition are **unchanged and unaffected**: both corrections are to
> the *wording of its corroboration*, not to anything it binds. The
> `.ai/project/verification/` supersession convention is not available here — an approval is
> not a verification report — so the corrections are appended and attributed, which is the
> register's own convention for an updated row.
>
> Both were found by the independent cold-context `qa-engineer` audit that `OI-V-13` owes,
> which reproduced every load-bearing value of this approval **exactly** — the `8546960` git
> object at `ae16ccac…9d8395aa`, the three-approval chain to `5b78d25b…bbd6b652`, zero
> removals, all three DC-2 lineage values, and V-24 at 31/31 — and confirmed the recorded
> residual more strongly than this record does, by enumerating every blob named
> `framework.manifest.json` anywhere in the object graph (ten of them) and showing
> `8af8971b…a7e42ff7` is **not among them**.

**Correction 1 — `OI-V-13` FIND-5. "Twenty-seven changed leaves" is the wrong noun.**
§2's *"The twenty-seven discrete changes"* and the enumeration's row count are **27 authorised
change-events over 25 distinct leaves.** Two leaves are extended twice, once by each of two
instruments: `metadata.reproducible.budget_measurement_record.authority` (rows 13 and 27) and
`validation[V-09].verifies` (rows 16 and 24). Every row is a real, separately authorised
change, and the 3 / 13 / 11 partition against each instrument's own enumeration is
**unaffected** — an instrument that extends a value a second time declares a change, and the
row is that change. What is wrong is calling 27 rows 27 *leaves*. The attribution is complete
and correct; the count of leaves is 25.

**Correction 2 — `OI-V-13` FIND-6. Corroboration 2's universal claim is false for two of
eight.** *"An unattributed extension would be visible as an extension carrying no citation.
None is."* Two carry none:

| Extended value | The extension | Cites |
|---|---|---|
| `…core_aggregate.covers` | *"plus every enabled-role agent artifact resolved per `enabled_role_coverage`"* — a **mid-string insertion**, not an append | no amendment |
| `…budget_measurement_record.verdict_rule` | *"; the aggregate comparison is the charged comparison of `aggregate_ceiling_charge`"* | no amendment |

Attribution survives one hop in both cases — each names a sibling member whose own `authority`
field carries the citation — so **no leaf is unattributable and the disposition does not
move.** The defect is that corroboration 2 was stated as exhaustive and is not, and an
exhaustive claim that is false in two of eight instances is exactly the kind of assurance
this repository has learned to distrust.

**Neither correction disturbs anything this approval binds.** `subject_path`, `subject_hash`,
`prior_hash` and the ruling are untouched; `aief_approval verify` and `V-24` are unaffected
and both continue to pass.
