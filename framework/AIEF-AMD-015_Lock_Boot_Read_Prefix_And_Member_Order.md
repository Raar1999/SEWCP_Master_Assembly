# AIEF-AMD-015 — Architecture Amendment: the Lock's Measured Quantity is the Boot-Read Prefix, and `aggregate_digest` Moves to Second Position

| | |
|---|---|
| **Instrument** | Architecture amendment to AIEF 1.0.0, partition `framework` |
| **Amends** | `framework/framework.manifest.json` — **three** changes: two normative clause bodies and one authority citation |
| **Disposes** | `ECR-D-014` |
| **Raises** | `OI-C-14` |
| **Authorising basis** | The human owner's written instruction of 2026-08-11: *"If a software/architecture gap exists: repair it at the owning layer. Test it. Verify it. Continue."* — `core/PRECEDENCE.md` rank 1, recorded per LAW-10 in `project/approvals/APR-035` and `project/approvals/APR-036` |
| **Authority exercised by** | `claude-under-owner-delegation · S-2026-08-11-06`. **OWNER-DELEGATED ENGINEERING AUTHORITY EXERCISED BY CLAUDE — this is not a human approval and is never to be cited as one** |
| **Provenance record** | [`../.ai/project/decisions/DECISIONS_S-2026-08-11-06.md`](../.ai/project/decisions/DECISIONS_S-2026-08-11-06.md) DEC-06 |

---

## Why this instrument exists

The first authorised Compiler Stage 6 build **halted**, and it halted correctly:

```
aief_stage6.budget.BudgetBreach: core/MANIFEST.lock: governing 6481 > cap 200 - build halts
```

The halt was not a bug. `budget_measurement_record.verdict_rule` requires it, and the
implementation obeyed the clause it was written from. The defect is that the clause it obeyed and
another clause of the same artifact cannot both hold, and the one it obeyed is unsatisfiable by
any conforming lock. `ECR-D-014` records the finding, the measurements and the rejected
alternatives; this instrument makes the ruling.

**Nothing about integrity changes here.** The lock still carries every covered file and its DC-1
digest, `aggregate_digest` is still DC-4 over exactly those records, B2a still recomputes all of
it, and the BINDING pin still binds the aggregate. What changes is which octets a token cap
counts, and where one member sits in a JSON document.

---

## AMD-54 — The Measured Quantity is the Boot-Read Prefix

**Amends** `metadata.reproducible.budget_measurement_record.lock_self_measurement` ·
**Disposes** `ECR-D-014` in part · **Raises** `OI-C-14`

### 1 · The gap

`AIEF-AMD-013` §AMD-45 declared *"the serialised lock octets are measured under both families
against the 200 cap after serialisation"*. It settled **when** the measurement happens
(post-serialisation, before the archive), **under what** (both families), and **what a breach
does** (halts). It did not settle **which octets**, and the natural reading — all of them — is
unsatisfiable.

Measured at `S-2026-08-11-06` with both declared tokenizer artifacts in hand:

| Quantity | TF-1 | TF-2 | vs 200 |
|---|---|---|---|
| Whole serialised lock | 5334 | **6469** | 32.3× |
| `files` alone (75 pairs) | 4212 | 5198 | 26.0× |
| Schema-required members, `files` removed | — | 285 | 1.4× |
| **Boot-read prefix, after §AMD-55** | **56** | **69** | **0.35×** |

The third row is the one that decides it: **even a lock stripped of `files` and
`budget_measurement` breaches 200.** No content reduction reaches the cap, and
`AIEF-AMD-013` §AMD-41 §5(iii)'s finding forecloses raising it — MI-4 stands at 5904 of 6000 and
a raise to 6469 would put the sum at 12173.

### 2 · What the other clause already said

`digest_constructions.core_aggregate.lock_serialisation`, unchanged since `AIEF-AMD-010` §AMD-27:

> *"aggregate_digest precedes files **so the T1 digest read stays within the 200-token cap**
> declared on files[manifest-lock]"*

This is a normative statement that the cap bounds **a read that stops at `aggregate_digest`**.
It is the only reading under which member ordering can bear on the count at all; under the
whole-document reading, ordering is irrelevant to the total and the clause states a purpose it
cannot serve. The two clauses have been in contradiction since AMD-45 was written, and nothing
executed the pair until now.

### 3 · Ruling

**The octets measured against `files[manifest-lock].token_cap` are the boot-read prefix: the
serialised lock from its first octet through the terminal LF of the line carrying the
`aggregate_digest` member.**

Everything else of AMD-45 is unchanged and is restated so nothing is read as relaxed:

| Property | Status |
|---|---|
| Measurement is post-serialisation, before the archive is built | **unchanged** |
| Both families, the maximum governs | **unchanged** |
| A breach halts the build under `verdict_rule` | **unchanged** |
| The lock's per-file row is `DEFERRED-SELF-MEASURED`, null counts, contributing nothing to totals | **unchanged** |
| The deferral is keyed on the path `core/MANIFEST.lock`, never on absence from the tree | **unchanged** (TCR-001 F1 stays disposed) |
| `AIEF-AMD-014` §AMD-51 charges the **full declared 200** to each per-family total | **unchanged** — the charge is the declared cap, not the measurement, so the aggregate comparison still over-states and never under-states |

**The prefix has no fallback.** A serialised lock with no `aggregate_digest` line, or one whose
`aggregate_digest` line is not LF-terminated, has no boot-read prefix, and the build **halts**. A
fallback to some other region is how a cap comes to bound a quantity nobody declared, which is
the defect class this instrument exists to close, not to repeat.

### 4 · Why this quantity, and not a convenient one

`b2a_procedure` is a machine procedure over file content: recompute DC-1 per listed file,
recompute DC-4, compare to `aggregate_digest`, compare that to `BINDING.core_digest_pin`. The 75
digests are **hashed**, not read. `measurement_domain` binds the measured set to *"the domain of
manifest invariant MI-4 … and of the AIEF-FRZ-001 §1.8 derivation table"* — the boot **context**
budget, which is what a reader must load. The prefix is exactly what a reader loads before it
holds the value B2a compares to the pin. A list of 75 digests was never boot context, and
`lock_serialisation` said as much in the only words it had.

### 5 · Residual — `OI-C-14`, raised and expressly not cured

**The whole-document size of `core/MANIFEST.lock` is now bounded by nothing.** 6469 TF-2 tokens
today, growing with the covered set. No invariant ranges over it and nothing is violated — but
*nothing is violated* is not *something is checked*, which is the `OI-V-02` lesson. Raised as
`OI-C-14`, for an authority that can weigh a whole-document bound against the artifact's purpose.
Not cured here: inventing a second, undeclared cap while disposing a defect about an undeclared
measured quantity would be the same mistake twice.

### 6 · Manifest change

`metadata.reproducible.budget_measurement_record.lock_self_measurement` — the existing text is
retained **verbatim and entire**, and the ruling is appended to it. Nothing AMD-45 wrote is
deleted or reworded.

---

## AMD-55 — `aggregate_digest` Moves to Second Position

**Amends** `metadata.reproducible.digest_constructions.core_aggregate.lock_serialisation` ·
**Disposes** `ECR-D-014` in part

### 1 · Why the ordering is not cosmetic

With §AMD-54 alone and the member order unchanged, the prefix is:

```
{ framework_version, build_provenance{ source_manifest, source_manifest_dc1,
  selected_profile, compiler_stage, build_id, timestamp }, hash_algorithm,
  normalisation{ 4 members }, aggregate_digest }
```

— **291 tokens under TF-2 against a 200 cap.** It would still breach, and the only cap value MI-4
admits is 296, which fits by five tokens and consumes every one of the 96 tokens of headroom
`AIEF-AMD-014` §AMD-50 left.

Worse than tight: **that prefix contains `build_id`**, and `build_provenance_record.content.build_id`
bounds its length not at all. Measured across identifier lengths:

| `build_id` length | 1 | 8 | 27 | 52 | 80 |
|---|---|---|---|---|---|
| Prefix, TF-2 | 280 | 282 | 291 | 306 | 319 |

A cap over that quantity is a cap over a free-form string. It would pass on the release run that
set it and fail on the next one that named its build differently — a check that depends on what
someone types is not a check.

### 2 · Ruling

**Declared member order becomes: `framework_version`, `aggregate_digest`, `build_provenance`,
`hash_algorithm`, `normalisation`, `budget_measurement`, `files`.** `aggregate_digest` moves from
fifth position to second.

The clause *"aggregate_digest precedes files"* is unchanged in words and was already satisfied.
What it could not do at the fifth position was deliver the property it states as its reason.

Resulting prefix:

```json
{
  "framework_version": "1.0.0",
  "aggregate_digest": "<64 lowercase hex>",
```

**69 tokens under TF-2, 56 under TF-1.** Determined entirely by the specification: no `build_id`,
no `timestamp`, no profile name, nothing a caller chooses. A 2.9× margin against the cap, and the
margin does not move when a release run names itself differently.

### 3 · What this does not disturb

| | |
|---|---|
| `files[manifest-lock].token_cap` | **200, unchanged** |
| MI-4 | **5904 of 6000, unchanged. Headroom 96, unchanged** |
| `AIEF-FRZ-001` §1.8 derivation | **unchanged** |
| `version.min_context_window` | **unchanged** — the ratified 32,000-token portability floor is not touched, so OQ-15 option (b)'s cost is not incurred |
| `sch-core-manifest` | **unchanged.** It declares required *fields*, not their order; the emitted lock validates against the emitted schema, and a test asserts it |
| DC-4, `aggregate_digest`'s value, the covered set, `b2a_procedure` | **unchanged** |
| `lock_json_layout` (AMD-43) | **unchanged**, and it is what makes this well-defined: *"Declared member order is emission order and is never sorted"*, one member per line, LF endings |
| Any existing digest | **none.** No `core/MANIFEST.lock` had ever been emitted, so no DC-5 release digest, no `core_digest_pin` and no archive existed to invalidate. The reorder is free precisely because it is being made before the first canonical build, and it could not have been made cheaply after |

### 4 · Manifest change

`…core_aggregate.lock_serialisation` — the member-order list is amended and the amendment is
appended with its reason and its measurements. The `aggregate_digest precedes files` clause and
the `files is an array of [path, digest] pairs in DC-4 record order` clause are retained verbatim.

---

## Blast Radius

Determined by inspecting what renders or consumes each changed clause, following the
AMD-008/009/012/013/014 method.

| Changed | Rendered or consumed by | Effect |
|---|---|---|
| `lock_self_measurement` | `src/aief_stage6/budget.py` (`measure_text`), `src/aief_stage6/build.py` | **Implementation delta, performed here.** `measure_text` now receives the prefix; `lock.boot_read_prefix` computes it and halts when it is undefined |
| `lock_serialisation` member order | `src/aief_stage6/lock.py` (`build_lock_object`) | **Implementation delta, performed here.** Insertion order is emission order per `lock_json_layout` |
| Both | `tests/test_stage6_certification_lock_archive_guard.py` | **Test delta, performed here.** The transcribed `LOCK_MEMBER_ORDER` constant is replaced by a parse of the clause itself, so the test tracks the ruling rather than a snapshot of it — the `OI-C-12` / `R-017` repair-at-the-property precedent. Four tests added for §AMD-54 |
| Neither | `.ai/core/**` | **None.** No `core/` artifact renders either clause. `core/CONTEXT_TIERS.md` renders the cap **table**, and no cap changes, so it does **not** become stale — unlike `AIEF-AMD-014` §AMD-50, which did stale it |
| Neither | `core/validation/CHECKS.md`, `MANIFEST` | **None.** `validation[V-09].verifies` is **not** amended: it already points at `lock_self_measurement` by name (*"the lock's own row follows lock_self_measurement"*), so the pointer carries the new content without a text change. `OI-V-07` is **not** deepened by this instrument |
| Neither | `adapters/ADP-ci.md` | **None.** Check count unchanged at 25 |
| Neither | `project/FROZEN.md` | Manifest row re-registered at the new DC-1; this instrument added under the AMD-21 criterion. Registry edit under `APR-035`/`APR-036` |

**Deliberately not touched:** every `.ai/core/**` byte except the canonical `core/MANIFEST.lock`
that Stage 6 is authorised to emit · `.ai/adapters/**` · `spec/**` and every CAD artifact,
drawing, BOM and deliverable — **no verified geometry is affected by this instrument in any way**
· `AIEF-FRZ-001`, AMD-001…AMD-014, both ADRs, every schema · `version.*` · any `token_cap` ·
git author or committer identity, and no attribution trailer of any kind is written anywhere.

---

## Separation of Duties — Recorded Tension

`core/agents/INDEX.md`: **`chief-systems-engineer` may not implement what it approved.** This
instrument was written, ruled, applied to the manifest, implemented in `src/aief_stage6/**` and
tested by **one session**, `S-2026-08-11-06`, under the owner's written delegation
(`core/PRECEDENCE.md` rank 1, which outranks the rank-6 agent specification). This is a **wider**
departure than AMD-013's and AMD-014's, both of which expressly **declined** to implement what
they ruled and left the delta to an A1 role as `OI-C-09`.

| | |
|---|---|
| Duty separated | A4 rules and approves; A1 implements; a distinct session verifies |
| Departure | One session ruled, applied, implemented and tested |
| Authority | The owner's written instruction of 2026-08-11, rank 1: *"repair it at the owning layer. Test it. Verify it. Continue."* — which directs the implementation expressly |
| Mitigating control | **NOT EXECUTED, and open.** An independent cold-context `qa-engineer` audit of this session's work is owed. It must independently re-measure the six quantities of §AMD-54 §1 under both families, re-derive the §AMD-55 prefix, and re-attack the four §AMD-54 tests |
| Not mitigated by | Anything this document says about itself. Under LAW-05 an authority's assertion about its own work carries no evidentiary weight — **including its assertion that the boot-read prefix measures 69** |

Recorded at `SOD-1` and at `OI-V-13`.

---

## Approvals Required and Recorded

| Change | Approval | Bound to |
|---|---|---|
| The manifest amendment of AMD-54 and AMD-55, and re-registration of the manifest in `FROZEN.md` at its post-change digest | `project/approvals/APR-035` | the post-change manifest DC-1 (`subject_hash`), with the pre-change DC-1 as `prior_hash` — both measured this session |
| Freeze-registry addition of this document (AMD-21 criterion) | `project/approvals/APR-036` | this document's DC-1 |

Per the AMD-16 design property, neither this document's own digest nor the post-registration DC-2
aggregate appears in this document; both live in the registry and the approval artifacts.
