# APR-006 — Amendment of `framework.manifest.json` under AIEF-AMD-010

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the manifest change made by AIEF-AMD-010.

```yaml
approval_id:   APR-006
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-08T07:25:46Z
subject_path:  framework/framework.manifest.json
subject_hash:  ae16ccaca5746b81a2a992841fc1d239fd1c8b0c34657c05611e025a9d8395aa
prior_hash:    9611d547aab51475e3b57a255af52d47972e4024c896edb5c210cf8f9813e557
scope:         Amendment of the named artifact by AIEF-AMD-010 rulings AMD-25 through AMD-33,
               and re-registration in FROZEN.md at the stated subject_hash.
session:       S-2026-08-08-04
applied_by:    chief-systems-engineer · S-2026-08-08-04
basis:         live human-owner instruction, core/PRECEDENCE.md rank 1
```

---

## Subject

`framework/framework.manifest.json`, at normalised SHA-256 (DC-1)
`ae16ccaca5746b81a2a992841fc1d239fd1c8b0c34657c05611e025a9d8395aa`.

Normalisation per `metadata.reproducible.digest_constructions.per_artifact` (DC-1).

**This approval is bound to that hash.** Per LAW-10 it is void if the subject content changes, and it names precisely what it approves.

## Authorising basis

The human owner, `BINDING.approval_authority: human-owner`, issued a live instruction in session `S-2026-08-08-04` assigning the Chief Systems Engineer in a cold context and directing the formal resolution of the Stage 6 pre-flight specification gaps (OPEN-QUESTIONS 1–10, 12 and the OQ-13 authority analysis), with the required amendment and approval artifacts recorded and affected DC-1/DC-2 hashes recomputed.

That instruction is `core/PRECEDENCE.md` **rank 1** and outranks the rank-3 freeze registry. `core/PRECEDENCE.md` clause 4 and LAW-10 clause 4 require such an override be recorded before dependent work is committed. This artifact is that record. The authority is the human owner's; this file is its written form.

## Scope

| In scope | Out of scope |
|---|---|
| The manifest changes enumerated below, and no others | Any change to `SCH-framework-manifest.schema.json` or `SCH-core-manifest.schema.json` — not amended |
| Replacing the registered digest for `framework/framework.manifest.json` in `FROZEN.md` with `subject_hash` | Any change to DC-1, DC-2 or DC-3; any law rule or clause, role contract, partition, layer, tier, boot step or compiler stage definition |
| | Registration of `AIEF-AMD-010` itself — separate instrument, `APR-007` |
| | Execution of Compiler Stage 6; creation of `core/MANIFEST.lock`; any write to `BINDING.core_digest_pin` or `BINDING.enabled_agents`; activation of the software profile |
| | Any ledger write, any git commit, tag or push |

## The change, enumerated

| # | Manifest location | Change | Ruling |
|---|---|---|---|
| 1 | `metadata.reproducible.digest_constructions.note` | Updated to name DC-4 and DC-5 alongside DC-1/DC-2/DC-3 | AMD-27, AMD-28 |
| 2 | `metadata.reproducible.digest_constructions.core_aggregate` | **New** — DC-4, the core aggregate construction with coverage (root files included), self-exclusion of `MANIFEST.lock`, B2a procedure, lock serialisation, worked example `eb6e969b…40325b1` | AMD-27, disposing OQ-4 and OQ-5 |
| 3 | `metadata.reproducible.digest_constructions.release_digest` | **New** — DC-5, raw-octet SHA-256 over the distributable archive, distinct from the aggregate, sidecar + release-notes recording, worked example `ba7816bf…f20015ad` | AMD-28, disposing OQ-3 |
| 4 | `metadata.reproducible.tokenizer_families` | **New** — TF-1 (byte-level BPE, `cl100k_base.tiktoken`) and TF-2 (SentencePiece unigram, T5 `spiece.model`), artifact pin mechanism | AMD-26, disposing OQ-2 |
| 5 | `metadata.reproducible.budget_measurement_record` | **New** — the record is the `budget_measurement` member of `core/MANIFEST.lock`; content and verdict rule declared | AMD-29, disposing OQ-6 |
| 6 | `metadata.reproducible.distributable` | **New** — uncompressed POSIX ustar tar `aief-<semver>-<profile>.tar`, deterministic construction, not tracked in-repo | AMD-30, disposing OQ-7 |
| 7 | `metadata.reproducible.build_time_reproducibility` | **New** — at least two executions per Stage 6 run, byte-identity halt condition | AMD-33, disposing OQ-10 |
| 8 | `validation[V-09].verifies` | Extended: families bound to TF-1/TF-2 and the pin verification | AMD-26 |
| 9 | `validation[V-10].verifies` | Extended: platforms (Windows plus at least one of Linux/macOS), DC-4/DC-5 bindings, byte-identity | AMD-33, disposing OQ-12 |
| 10 | `generation_order[6].outputs` | Four output entries made precise (lock serialisation, budget location, distributable naming, release-digest recording); pin entry states the DC-4 value | AMD-27…AMD-30 |
| 11 | `generation_order[6].barrier` | Extended with the AMD-31 compile-time precondition, the AMD-25 increment admissibility and the AMD-33 build-time reproducibility reference | AMD-25, AMD-31, AMD-33, disposing OQ-1 and OQ-8 |

## Verification status

Ruled and applied by the same authority, `chief-systems-engineer · S-2026-08-08-04`, at the direction of the human owner. The separation-of-duties departure is recorded in AIEF-AMD-010 § *Separation of Duties*. Under LAW-05 this session cannot verify its own work; an independent cold-context `qa-engineer` audit of this session's work is dispatched by the same directing instruction as the mitigating control.

Reproducible by a third party from the repository alone: the pre-change manifest at `git show dc811a6:framework/framework.manifest.json` normalises to `prior_hash`; the working-tree manifest after this amendment normalises to `subject_hash`; the diff is the eleven changes above and no others. Schema conformance of the amended manifest was verified against the unmodified frozen `SCH-framework-manifest.schema.json` with a JSON Schema 2020-12 validator: PASS.

## Authority chain

| | |
|---|---|
| `core/PRECEDENCE.md` rank 1 | Live human instruction — the authorising basis |
| LAW-01 | A frozen artifact is changed only by an approved ECR and a recorded human approval |
| LAW-10 | Approval is an artifact bound to a content hash |
| LAW-12 | Every gap disposed by open decision with recorded rationale, never by assumption |
| `project/BINDING.md` | `approval_authority: human-owner` |
| AIEF-AMD-010 | The amendment this approval authorises |
