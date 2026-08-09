# APR-012 — Amendment of `framework.manifest.json` under AIEF-AMD-013

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the manifest change made by AIEF-AMD-013.

```yaml
approval_id:   APR-012
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-08T10:41:00Z
subject_path:  framework/framework.manifest.json
subject_hash:  8af8971b78d762e5db2879e50585a78f4e6d497ea707c664a9c06e1ba7e42ff7
prior_hash:    f06125d2f9bd0860ab72c73f7dd11318d5d4f3169ded23b86f33e9c469707638
scope:         Amendment of the named artifact by AIEF-AMD-013 rulings AMD-42 through AMD-48,
               and re-registration in FROZEN.md at the stated subject_hash.
session:       S-2026-08-08-10
applied_by:    chief-systems-engineer · S-2026-08-08-10
basis:         live human-owner instruction, core/PRECEDENCE.md rank 1
```

---

## Subject

`framework/framework.manifest.json`, at normalised SHA-256 (DC-1)
`8af8971b78d762e5db2879e50585a78f4e6d497ea707c664a9c06e1ba7e42ff7`.

Normalisation per `metadata.reproducible.digest_constructions.per_artifact` (DC-1).

**This approval is bound to that hash.** Per LAW-10 it is void if the subject content changes, and it names precisely what it approves.

## Authorising basis

The human owner, `BINDING.approval_authority: human-owner`, issued a live instruction in session `S-2026-08-08-10` assigning the Chief Systems Engineer in a cold context and directing that CMP-BLOCK-006 and the five build open questions OQ-B1…OQ-B5 be resolved according to the repository's authoritative records; that A4 independently inspect the V-09 failure and determine whether deterministic content reduction suffices or the frozen budget construction requires an architecture amendment; that no authoritative content be deleted, summarised, relocated or weakened; that the resolutions be deterministic and reproducible; that every ruling be recorded through the proper A4 approval and amendment mechanism; and that no assumption stand where the repository records an unresolved question.

That instruction is `core/PRECEDENCE.md` **rank 1** and outranks the rank-3 freeze registry. `core/PRECEDENCE.md` clause 4 and LAW-10 clause 4 require such an override be recorded before dependent work is committed. This artifact is that record. The authority is the human owner's; this file is its written form.

## Scope

| In scope | Out of scope |
|---|---|
| The manifest changes enumerated below, and no others | Any change to `SCH-framework-manifest.schema.json` — not amended; the amended manifest passes it unmodified (verified, Draft 2020-12: 0 errors) |
| Replacing the registered digest for `framework/framework.manifest.json` in `FROZEN.md` with `subject_hash` | **Any `token_cap` value and the 6000 boot ceiling — unchanged.** MI-4 sum is 5800 before and after |
| | Any change to DC-1's normalisation of non-empty content, DC-2, DC-3, DC-4's coverage, grammar, order, preimage, self-exclusion, B2a procedure, `lock_serialisation` member order or worked example, DC-5, TF-1 or TF-2 |
| | Any law rule or clause, role contract, partition, layer, tier, boot step, compiler stage or lifecycle definition |
| | Registration of `AIEF-AMD-013` itself — separate instrument, `APR-013` |
| | Execution of Compiler Stage 6; creation of `core/MANIFEST.lock` or the distributable; any write to `BINDING.core_digest_pin` or any other BINDING field; any change to `src/aief_stage6/**` |
| | Any ledger write, any git commit, tag or push |
| | **The disposition of CMP-BLOCK-006.** AMD-41 is a determination and a reservation; it changes no frozen artifact and requires no approval. The remedy is reserved to the human owner as OQ-15 |

## The change, enumerated

| # | Manifest location | Change | Ruling |
|---|---|---|---|
| 1 | `metadata.reproducible.digest_constructions.per_artifact.empty_content` | **New** — DC-1 of content that normalises to empty is the SHA-256 of zero octets, `e3b0c442…7852b855`; the terminal-LF step applies to surviving content, not to emptiness | AMD-48 |
| 2 | `metadata.reproducible.digest_constructions.per_artifact.status` | Extended to point at member 1 and to state that no non-empty digest changes | AMD-48 |
| 3 | `metadata.reproducible.digest_constructions.core_aggregate.lock_json_layout` | **New** — the lock's JSON layout: two-space indent, LF, one terminal LF, no trailing whitespace, one space after the name separator, one member per line, RFC 8259 escaping only, emission order never sorted | AMD-43 |
| 4 | `metadata.reproducible.budget_measurement_record.authority` | Extended to cite AMD-42 and AMD-45 | AMD-42, AMD-45 |
| 5 | `metadata.reproducible.budget_measurement_record.measurement_domain` | **New** — the measured set is exactly the non-null-`token_cap` T0/T1 entries; clause 2's totals are the totals over that set; the cap-null boot-loaded exposure is named as OI-C-08 and expressly not closed | AMD-42 |
| 6 | `metadata.reproducible.budget_measurement_record.measurement_instant` | **New** — the record is a measurement of the tree at the build instant, not a reproducible constant; disagreement on re-measurement is expected drift | AMD-42 |
| 7 | `metadata.reproducible.budget_measurement_record.lock_self_measurement` | **New** — the lock's row is `DEFERRED-SELF-MEASURED` with null counts, contributing nothing to totals; the serialised octets are cap-checked post-serialisation; **the deferral is keyed on the path, never on absence from the tree** | AMD-45 |
| 8 | `metadata.reproducible.build_provenance_record` | **New** — the six closed members of `build_provenance`, their order, and the prohibition on host, user, directory, tool-version, per-execution-time and environment capture | AMD-44 |
| 9 | `metadata.reproducible.distributable.entry_types` | **New** — regular file entries only; the directory-mode clause is vacuous for a conforming archive and is retained, not deleted | AMD-46 |
| 10 | `metadata.reproducible.build_time_reproducibility.authority` | Extended to cite AMD-48 | AMD-48 |
| 11 | `metadata.reproducible.build_time_reproducibility.run_fixed_values` | **New** — build id and timestamp captured once per release run and supplied to every execution; the run, not the execution, is the unit of provenance | AMD-48 |
| 12 | `metadata.reproducible.binding_pin_write` | **New** — value-token-only replacement on the single `core_digest_pin` line, every other octet preserved; three declared halt conditions | AMD-47 |
| 13 | `validation[V-09].verifies` | Extended: the measured set and totals scope are `budget_measurement_record.measurement_domain`, and the lock's row follows `lock_self_measurement` | AMD-42, AMD-45 |

Counted as nine changes in AIEF-AMD-013 § header (seven new members plus the `V-09` extension and the accompanying `authority`/`status` housekeeping); enumerated at full granularity here.

No other member of the manifest changes. DC-1's normalisation of non-empty content, DC-2, DC-3, DC-4's coverage and worked example `eb6e969b…40325b1`, DC-5's worked example `ba7816bf…f20015ad`, TF-1 and TF-2 and every `token_cap` are untouched.

## Verification status

Ruled and applied by the same authority, `chief-systems-engineer · S-2026-08-08-10`, at the direction of the human owner. The separation-of-duties departure is recorded in AIEF-AMD-013 § *Separation of Duties*. Under LAW-05 this session cannot verify its own work; an independent cold-context `qa-engineer` audit of this session's work is the mitigating control and is open until filed.

Reproducible by a third party from the repository alone. Checks performed this session and independently repeatable:

| Check | Result |
|---|---|
| Pre-change manifest normalises to `prior_hash` | Confirmed indirectly and strongly: the AMD-31 precondition run executed **before** any edit of this session reported **V-24 PASS**, which recomputes every registered DC-1 including the manifest's against `FROZEN.md`'s then-recorded `f06125d2…69707638` |
| Post-change manifest normalises to `subject_hash` | `8af8971b78d762e5db2879e50585a78f4e6d497ea707c664a9c06e1ba7e42ff7` |
| Schema conformance of the amended manifest against the unmodified frozen `SCH-framework-manifest.schema.json`, JSON Schema 2020-12 | **PASS**, 0 errors |
| MI-4 (Σ `token_cap` over T0 ∪ T1 ≤ 6000) | **5800** before, **5800** after |
| MI-1 (unique ids and paths over 106 `files[]` entries) | 0 duplicate ids, 0 duplicate paths |
| AMD-31 precondition run after the edit | V-01…V-08, V-23, V-25 **PASS**; V-09 **FAIL** (CMP-BLOCK-006, undisposed by design); V-24 **FAIL** until `FROZEN.md` is re-registered by this approval — the registry check correctly detecting the amendment |
| Manifest remains pure ASCII | Confirmed — 0 non-ASCII code points |

## The reduction performed

Recorded here rather than in AIEF-AMD-013, which is inside the freeze registry, or in `project/STATE.md`, which cannot state its own post-reduction count without changing it. Measured with the repository's own implemented families from the pinned artifacts, TF-1 and TF-2, the maximum governing.

| `project/STATE.md` | TF-1 | TF-2 | Governing | Cap 1100 |
|---|---|---|---|---|
| Before, at session start | 1503 | 1747 | 1747 | **FAIL** by 647 |
| After the reduction of AIEF-AMD-013 § *Content Reduction Performed*, at session close | **921** | **1083** | **1083** | **PASS**, 17 tokens of headroom |
| Change | −582 | −664 | −664 | |

The 17 tokens of remaining headroom are themselves evidence, and are recorded against OQ-15: the *derived cache* of a single-component project, ten sessions in, sits within 1.5% of its cap after a 38% reduction that removed no recorded fact and left the file at near-index form. The next session's write will consume that margin. `project/STATE.md` is therefore a second, milder instance of the defect class AMD-41 §4 identifies in `project/OPEN_ITEMS.md`, and any OQ-15 remedy must address both.

**Nothing recorded was lost.** Every fact the prior text carried is retained, in place or by pointer to the artifact that holds it authoritatively:

| Prior content | Where it is now |
|---|---|
| All eight `tpl-current-state` required fields | Retained in the YAML block, unchanged in kind |
| Blocker and open-item narratives | Ids retained; substance resolves in `project/OPEN_ITEMS.md`, which is authoritative and which the template directs this section to *index, not duplicate* |
| Frozen-set membership lineage, the four superseded aggregates, the non-reproducible pre-DC-2 value, the truncation note | `project/FROZEN.md` §§ *Registration history*, *Aggregate*, *Superseded value* — all already authoritative there, none unique to `STATE.md` |
| Approval-provenance and re-registration history | `project/FROZEN.md` § *Registration history* and `project/approvals/APR-001…APR-013` |
| Genesis and reconciliation semantics | Retained in condensed form; governed by AIEF-AMD-003 §AMD-10 and `project/ledger/HEAD` |
| `V-24` standing-check absence | Retained, and authoritative at `project/FROZEN.md` § *Standing verification* and OI-V-02 |

**Authority for the reduction.** `project/OPEN_ITEMS.md` declares this file *"a derived cache"*; `tpl-current-state` makes *"Within the 1100 token cap"* acceptance condition 3 and *"Exceeding the 1100 token cap"* a Forbidden, so bringing the file inside its cap is what its own template requires. `owner_role` is `chief-systems-engineer`, the ruling role.

**The reduction does not close CMP-BLOCK-006, and this session's own work moved the aggregate the wrong way.** Measured at the close of this session over the same capped set:

| | TF-1 | TF-2 | Governing | Limit |
|---|---|---|---|---|
| `BOOT.md` | 445 | 504 | 504 | cap 400 — **FAIL**, unchanged and unchangeable by any available actor |
| `FRAMEWORK.md` | 652 | 748 | 748 | cap 1100 — PASS |
| `core/PRECEDENCE.md` | 341 | 382 | 382 | cap 700 — PASS |
| `core/laws/INDEX.md` | 598 | 721 | 721 | cap 900 — PASS |
| `project/BINDING.md` | 483 | 574 | 574 | cap 800 — PASS |
| `project/STATE.md` | 921 | 1083 | 1083 | cap 1100 — **PASS**, reduced this session |
| `project/OPEN_ITEMS.md` | 9428 | 12000 | 12000 | cap 600 — **FAIL**, grown from 6867 / 8673 by this session's additive register work |
| `core/MANIFEST.lock` | — | — | — | cap 200 — not on disk; emitted by Stage 6 |
| **Capped T0 ∪ T1 aggregate** | 12868 | **16012** | 16012 | ceiling 6000 — **FAIL** |

The register grew by more than the reduction saved, because disposing the blocker means recording the disposition. That is the AMD-41 §2 finding restated as arithmetic, and it is the plainest available evidence that the construction, not the content, is what has to change.

## Authority chain

| | |
|---|---|
| `core/PRECEDENCE.md` rank 1 | Live human instruction — the authorising basis |
| LAW-01 | A frozen artifact is changed only by an approved ECR and a recorded human approval |
| LAW-02 | Disposition of the recorded open questions OQ-B1…OQ-B5 and of a recorded blocker |
| LAW-10 | Approval is an artifact bound to a content hash |
| LAW-12 | Every undeclared value disposed by open decision with recorded rationale; where the choice was not a determination it was reserved, not assumed (OQ-15) |
| `project/BINDING.md` | `approval_authority: human-owner` |
| AIEF-AMD-013 | The amendment this approval authorises |
