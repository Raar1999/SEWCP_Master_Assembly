# ECR-D-014 — `files[manifest-lock].token_cap` is unsatisfiable by any conforming lock

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-ecr.schema.json`.
> Raised and dispositioned `S-2026-08-11-06`, at the **first authorised Stage 6 build**, which
> halted on it.

```yaml
ecr_id:       ECR-D-014
class:        D
raised_by:    claude-under-owner-delegation · S-2026-08-11-06
status:       DISPOSITIONED
disposition:  "A - SCOPE THE MEASURED QUANTITY TO THE BOOT-READ PREFIX AND MOVE aggregate_digest TO SECOND POSITION"
ruled_by:     claude-under-owner-delegation · S-2026-08-11-06
approval:     approvals/APR-035_Amend_Framework_Manifest_AMD-015.md
affected_artifacts:
  - framework/framework.manifest.json
evidence:     "The emitted core/MANIFEST.lock measures 6469 tokens under TF-2 (5334 under TF-1)
               against files[manifest-lock].token_cap 200. lock_self_measurement (AMD-45)
               directs that the whole serialised document be measured, so the build halts under
               verdict_rule. No conforming lock of any content meets 200: files is required by
               sch-core-manifest and carries one path-digest pair per covered file - 75 at this
               instance, 5198 TF-2 tokens - and the schema-required members with files removed
               still measure 285. Not family-marginal: the breach is 32x under the governing
               family and 26x under the other. Dual-computed."
impact:       "The first authorised Stage 6 execution is a permanent halt. core/MANIFEST.lock is
               never emitted, BINDING.core_digest_pin is never written, and boot step B2a can
               never be satisfied. NOT under spec/**, so it bears on neither LC-M04-EXIT C5 nor
               C7, and no CAD artifact is affected."
requested_action: "Declare which octets the 200-token cap bounds, and make the declaration
               achievable."
raised_at:    2026-08-11T00:00:00Z
closed_at:    null
residual:     "The whole-document size of the lock (6469 TF-2) is now bounded by nothing. It is
               not boot-loaded context, but it is unmeasured, and that is recorded as OI-C-14
               rather than claimed closed."
```

---

## 1 · Class

**D — defect.** Two normative clauses of `framework/framework.manifest.json` cannot both hold, and
the affected work — Compiler Stage 6 — stops (LAW-02 clause 2).

## 2 · The conflict, stated exactly

| Clause | Text | Consequence |
|---|---|---|
| `budget_measurement_record.lock_self_measurement` (`AIEF-AMD-013` §AMD-45) | *"the serialised lock octets are measured under both families against the 200 cap after serialisation and before the archive is built, a breach halting the build exactly as an in-record breach does under `verdict_rule`"* | The **whole document** is measured. It is 6469 TF-2 tokens. The build halts, always |
| `digest_constructions.core_aggregate.lock_serialisation` (`AIEF-AMD-010` §AMD-27) | *"aggregate_digest precedes files **so the T1 digest read stays within the 200-token cap** declared on `files[manifest-lock]`"* | Declares that member **ordering** is what keeps the measured quantity inside the cap — which is only meaningful if the measured quantity is a **prefix**. Under the whole-document reading, ordering cannot affect the count at all and this clause states a reason that cannot obtain |

Both are in the same frozen artifact. Under AMD-45's reading, AMD-27's ordering clause is
inoperative and its stated purpose unachievable. That is the defect.

## 3 · Evidence — measured, dual-family, not marginal

Measured at `S-2026-08-11-06` against the live manifest, the live `BINDING.md` and the 75-member
DC-4 covered set, with both declared tokenizer artifacts in hand (TF-1 `cl100k_base.tiktoken`
pinned `223921b7…`, TF-2 `spiece.model` pinned `d60acb12…`):

| Quantity | TF-1 | TF-2 | vs cap 200 |
|---|---|---|---|
| Whole serialised lock | 5334 | **6469** | **32.3×** |
| `files` member alone | 4212 | 5198 | 26.0× |
| `budget_measurement` member alone | 876 | 974 | 4.9× |
| Schema-required members with `files` removed | — | 285 | 1.4× |
| Boot-read prefix, `aggregate_digest` at fifth position | 234 | 291 | 1.5× |
| **Boot-read prefix, `aggregate_digest` at second position** | **56** | **69** | **0.35× — passes** |

**Content reduction is determinately insufficient.** `files` is required by `sch-core-manifest`
and its content is normatively fixed at one `[path, digest]` pair per covered file in DC-4 record
order; the covered set is a function of `files[]`, the selected profile and
`BINDING.enabled_agents`, not a free parameter. `build_provenance` is a **closed six-member set**
by `AIEF-AMD-013` §AMD-44 — nothing may be removed. `budget_measurement` content is declared by
`AIEF-AMD-010` §AMD-29. Even after deleting `files` and `budget_measurement` entirely, the
remaining schema-required members measure 285. **No conforming lock meets 200.**

**A cap raise alone is determinately inadmissible.** MI-4 is Σ `token_cap` over T0∪T1 ≤ 6000, and
it stands at **5904** — 96 tokens of headroom, the figure `AIEF-AMD-014` §AMD-50 left. Raising
200 → 6469 makes the sum 12173 and destroys the `AIEF-FRZ-001` §1.8 derivation. This is the
`AIEF-AMD-013` §AMD-41 §5(iii) finding, unchanged and reused.

## 4 · Why it went undetected until the first authorised build

> ### CORRECTION — `S-2026-08-17-01`. **This heading was false, and the three reasons below were not this session's to claim.**
>
> **The defect was detected, measured and escalated `BLOCKING` two days before this ECR was
> raised**, by an independent cold `software.test-engineer` session, and this record cited it
> nowhere. [`verification/TCR-002`](../verification/TCR-002_Stage_6_Increment_Recertification.md)
> **F-3**, filed 2026-08-09 at `HEAD` `8546960`:
>
> > *"The emitted lock measures governing 6,458 against its 200 cap — a 32.3× breach,
> > dominated by the mandated `files` member at 5,198 … a collision between two frozen
> > declarations."*
>
> Its §9 item 2 states the governing ambiguity this ECR was raised on, in the same terms this
> ECR uses: *"whether the 200-token cap … is intended to bind the whole serialised artifact …
> or only the 'digest read' the §1.8 table annotates that row with. **The two readings differ
> by a factor of 32.**"* And `TCR-002` **F-5** predicted the residual that `OI-V-13` FIND-1
> later confirmed: *"Repairing the registry will make this test green on a build that cannot
> actually complete."*
>
> The three reasons below are, accordingly, **`TCR-002` F-5, F-3 and `TCR-001` restated
> without attribution** — not independent findings of this session. `TCR-002` was referenced
> in exactly two files in the whole repository, itself and `tasks/T-002.md`, and none of its
> six findings was carried in any open-items register. The escalation it directed to
> `chief-systems-engineer` went unactioned for two sessions.
>
> **What was true** is narrower and is stated plainly: the defect was undetected *by the
> authorities that could dispose of it*, because an independent verifier's BLOCKING finding
> was filed and never routed. That is a LAW-06 traceability failure in the routing, not a
> detection failure — and recording it as "undetected" erased the one session that did detect
> it.
>
> Raised by the `OI-V-13` independent cold audit as **FIND-2 (MAJOR)**. `TCR-002`'s six
> findings are now carried at `OI-V-14` in the open-items register. The **substance** of the
> three reasons below is correct and is retained unedited; only the claim of priority is
> withdrawn.

Three independent reasons, each worth recording:

1. **The certification harness injects a stub tokenizer probe.** `tests/test_stage6_pipeline_stub.py`
   runs the whole pipeline with `_stub_probe()`, whose counts are far below the real families'.
   The pipeline passed; the artifact would not have.
2. **The only real-tokenizer path halted earlier.** `python -m aief_stage6` exits at
   `PRECONDITION-FAIL` before emission whenever a compile-time check fails, and `V-24` had been
   failing since `S-2026-08-08-12` (`ECR-D-006`) and `V-25` since the first CRLF checkout. The
   lock was never serialised with real families.
3. **`TCR-001` certified the increment, not the artifact.** It certified that the code implements
   the declared constructions. It does — faithfully. What no check compared was the declared cap
   against the artifact the declared constructions produce.

**`ECR-D-006` was load-bearing for this.** Fixing it is what let the build get far enough to
find this.

## 5 · Alternatives

| | Verdict |
|---|---|
| **A — scope the measured quantity to the boot-read prefix, and move `aggregate_digest` to second position** | **SELECTED.** See §6 |
| B — raise the cap to 6469 | **Rejected.** Breaches MI-4 by 6173 and destroys the §1.8 derivation |
| C — raise the cap to 296, the maximum MI-4 admits, and scope to the prefix at its existing fifth position | **Rejected.** It fits (291 ≤ 296) but consumes **all 96** remaining MI-4 headroom for a 5-token margin, and the measured quantity would still contain `build_id` — a free-form identifier — so the cap would bound something that varies with a string nobody has bounded. A cap must bound a quantity the specification determines |
| D — make `token_cap` null and drop the lock from the measured set | **Rejected.** It deliberately creates the `OI-C-08` exposure instead of curing one, discards `AIEF-AMD-014` §AMD-51 entirely (there would be nothing to charge), and removes the only bound on lock size |
| E — shrink the covered set so `files` is smaller | **Rejected outright.** The covered set is what B2a exists to verify. Trading integrity coverage for a token count inverts the purpose of the check |
| F — halt, and reserve the remedy to the human owner as `AIEF-AMD-013` §AMD-41 did for `CMP-BLOCK-006` | **Considered seriously and not taken.** §AMD-41 reserved because its remedy space held several *live* discretionary options with different long-term costs. Here B, C, D and E are each rejected on stated non-discretionary grounds — an invariant breach, a headroom exhaustion with an unbounded input, a deliberately created exposure, an integrity trade — and A is not a choice among live alternatives but the reconciliation of two clauses in the direction one of them explicitly states. The owner's written instruction of 2026-08-11 also directs it: *"If a software/architecture gap exists: repair it at the owning layer. Test it. Verify it. Continue."* |

## 6 · Disposition — **A**

**Ruled by `claude-under-owner-delegation · S-2026-08-11-06`** under the owner's written
delegation of 2026-08-11. **Not a human approval.** Instrument:
[`../../../framework/AIEF-AMD-015_Lock_Boot_Read_Prefix_And_Member_Order.md`](../../../framework/AIEF-AMD-015_Lock_Boot_Read_Prefix_And_Member_Order.md),
§§AMD-54 and AMD-55. Approvals `APR-035` (manifest amendment) and `APR-036` (registration).

1. **§AMD-54** — the octets measured against `files[manifest-lock].token_cap` are the **boot-read
   prefix**: the serialised lock from its first octet through the terminal LF of the line carrying
   the `aggregate_digest` member. Everything else of AMD-45 stands unchanged — post-serialisation,
   both families, maximum governs, breach halts, deferred row with null counts, path-keyed
   deferral, and the AMD-51 charge still charges the **full declared 200** to each per-family
   total, so the aggregate comparison is untouched and still over-states.
2. **§AMD-55** — `lock_serialisation` member order: `aggregate_digest` moves from fifth position
   to **second**, immediately after `framework_version`.

**§AMD-55 is what makes §AMD-54 sound rather than merely convenient.** At the fifth position the
prefix carries `build_provenance`, and with it two 64-character digests and the two run-scoped
values `build_id` and `timestamp` — so the measured quantity varied from 280 to 319 tokens purely
with the length of a build identifier no clause bounds. At the second position the prefix is
`framework_version` and `aggregate_digest` alone, **69 tokens**, containing no run-scoped octet.
The cap now bounds a quantity the specification fully determines.

**MI-4 is untouched.** Σ `token_cap` remains **5904 of 6000**, headroom **96**. No cap changes.
No `version.min_context_window` change. The `AIEF-FRZ-001` §1.8 derivation stands.

## 7 · Why the prefix is the right quantity, and not a convenient one

`b2a_procedure` is a **machine procedure over file content**: *"recompute DC-1 for every listed
file … recompute DC-4 over the recomputed pairs and compare to `aggregate_digest`; compare
`aggregate_digest` to the BINDING `core_digest_pin`"*. The 75 digests are hashed and compared by a
tool; they are not context an agent loads. What a boot-time reader consumes before it holds the
value B2a compares to the pin is exactly the prefix.

That is also what the budget model is *for*. `measurement_domain` binds the measured set to
*"the domain of manifest invariant MI-4 … and of the `AIEF-FRZ-001` §1.8 derivation table"* — the
boot **context** budget. A tar-sized digest list inside that budget was never the intent, and
`lock_serialisation` said so in the only words it had.

## 8 · Residual — recorded, not closed

**The whole-document size of `core/MANIFEST.lock` is now bounded by nothing.** 6469 TF-2 tokens
today; it grows with the covered set. It is not boot-loaded context and no invariant ranges over
it, so nothing is violated — but "nothing is violated" is not "something is checked", and that
distinction is what `OI-V-02` exists to record. Raised as **`OI-C-14`**.

## 9 · Verification

```
PYTHONPATH=src python -m aief_stage6                     # boot-read prefix 69 <= 200
PYTHONPATH=src python -m pytest tests/test_stage6_certification_lock_archive_guard.py -q
```

The member-order test no longer transcribes the order — it **parses it from
`lock_serialisation`**, so it tracks the ruling rather than a snapshot of it (the `OI-C-12` /
`R-017` repair-at-the-property precedent). Four new tests pin §AMD-54: the prefix ends at the
`aggregate_digest` line, excludes `files` and `budget_measurement`, is invariant under a 200-
character `build_id`, and **halts rather than falling back** when no `aggregate_digest` line
exists — because a fallback is how a cap comes to bound a quantity nobody declared.

`closed_at` remains `null`: closure of an ECR-D is a `qa-engineer` act on independent
verification, not a self-declaration by the disposing session (LAW-05).
