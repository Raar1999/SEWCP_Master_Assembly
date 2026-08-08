# APR-004 — Amendment of `framework.manifest.json` under AIEF-AMD-009

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the manifest change made by AIEF-AMD-009.

```yaml
approval_id:   APR-004
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-08T05:51:32Z
subject_path:  framework/framework.manifest.json
subject_hash:  9611d547aab51475e3b57a255af52d47972e4024c896edb5c210cf8f9813e557
prior_hash:    636cf22b9080b5d5178542fc42b618fc75033129a5932167d3b12e3214b38d3c
scope:         Amendment of the named artifact by AIEF-AMD-009 rulings AMD-23 and AMD-24,
               and re-registration in FROZEN.md at the stated subject_hash.
session:       S-2026-08-08-03
applied_by:    chief-systems-engineer · S-2026-08-08-03
basis:         live human-owner instruction, core/PRECEDENCE.md rank 1
```

---

## Subject

`framework/framework.manifest.json`, at normalised SHA-256 (DC-1)
`9611d547aab51475e3b57a255af52d47972e4024c896edb5c210cf8f9813e557`.

Normalisation per `metadata.reproducible.digest_constructions.per_artifact` (DC-1).

**This approval is bound to that hash.** Per LAW-10 it is void if the subject content changes, and it names precisely what it approves.

## Authorising basis

The human owner, `BINDING.approval_authority: human-owner`, issued a live instruction in session `S-2026-08-08-03` assigning the Chief Systems Engineer in a cold context and directing, among its terms: *"derive the ruling from the repository's authoritative artifacts; record the required amendment/approval artifacts; update the manifest only if the ruling requires it; recompute affected DC-1/DC-2 hashes."*

That instruction is `core/PRECEDENCE.md` **rank 1** and outranks the rank-3 freeze registry. `core/PRECEDENCE.md` clause 4 and LAW-10 clause 4 require such an override be recorded before dependent work is committed. This artifact is that record. The authority is the human owner's; this file is its written form.

## Scope

| In scope | Out of scope |
|---|---|
| The four manifest changes enumerated below, and no others | Any change to `SCH-framework-manifest.schema.json` — not amended |
| Replacing the registered digest for `framework/framework.manifest.json` in `FROZEN.md` with `subject_hash` | Any change to a law rule or clause, a role contract, a schema, a partition, layer, tier, boot step or compiler stage definition |
| | Registration of `AIEF-AMD-009` itself — separate instrument, `APR-005` |
| | Execution of Compiler Stage 5 or Stage 6; resolution of CMP-BLOCK-004 or CMP-BLOCK-005 |
| | Any ledger write, any git commit, tag or push |

## The change, enumerated

| # | Manifest location | Change | Ruling |
|---|---|---|---|
| 1 | `generation_order[stage 1].barrier` | Superseded wording *"No later stage may emit into core"* replaced with the precise Stage-1-output-set protection rule, evaluable as pairwise disjointness of declared outputs | AMD-23, disposing ECR-Q-003 (disposition A) |
| 2 | `generation_order[stage 1].outputs` | `"core/**"` qualified with the three later-stage exclusions (`core/templates/**`, `core/validation/**`, `core/MANIFEST.lock`), making the declared output sets disjoint as written | AMD-23 |
| 3 | `files[boot].referenced_by` `["framework"]` → `[]`; `files[sch-state].referenced_by` `["state", "V-06"]` → `["state"]` | The two tokens that fail MI-3 under the strict reading removed; no semantic relation is lost — the check→schema relation lives in `validation[V-06]` and MI-7 | AMD-24, disposing OI-C-03 |
| 4 | `validation[V-01].verifies` | Extended with the MI-3 namespace rule and the stage-output disjointness predicate, binding both rulings to the declared BLOCKING compile-time check | AMD-23, AMD-24 |

## Verification status

Ruled and applied by the same authority, `chief-systems-engineer` · `S-2026-08-08-03`, at the direction of the human owner. The separation-of-duties departure is recorded in AIEF-AMD-009 § *Separation of Duties*. Under LAW-05 this session cannot verify its own work; an independent cold-context `qa-engineer` audit of this session's work is dispatched by the same directing instruction.

Reproducible by a third party from the repository alone: the pre-change manifest at `git show 6ce3508:framework/framework.manifest.json` hashes to a value superseded by APR-002's subject; the working-tree manifest before this amendment hashed to `prior_hash`; after, to `subject_hash`; the diff is the four changes above and no others.

## Authority chain

| | |
|---|---|
| `core/PRECEDENCE.md` rank 1 | Live human instruction — the authorising basis |
| LAW-01 | A frozen artifact is changed only by an approved ECR and a recorded human approval |
| LAW-10 | Approval is an artifact bound to a content hash |
| LAW-02 | ECR-Q-003 dispositioned by a session that did not raise it (AMD-20 identity rule) |
| `project/BINDING.md` | `approval_authority: human-owner` |
| AIEF-AMD-009 | The amendment this approval authorises |
