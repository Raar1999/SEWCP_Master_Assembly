# APR-010 — Amendment of `framework.manifest.json` under AIEF-AMD-012

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the manifest change made by AIEF-AMD-012.

```yaml
approval_id:   APR-010
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-08T09:06:50Z
subject_path:  framework/framework.manifest.json
subject_hash:  f06125d2f9bd0860ab72c73f7dd11318d5d4f3169ded23b86f33e9c469707638
prior_hash:    ae16ccaca5746b81a2a992841fc1d239fd1c8b0c34657c05611e025a9d8395aa
scope:         Amendment of the named artifact by AIEF-AMD-012 rulings AMD-39 and AMD-40,
               and re-registration in FROZEN.md at the stated subject_hash.
session:       S-2026-08-08-06
applied_by:    chief-systems-engineer · S-2026-08-08-06
basis:         live human-owner instruction, core/PRECEDENCE.md rank 1
```

---

## Subject

`framework/framework.manifest.json`, at normalised SHA-256 (DC-1)
`f06125d2f9bd0860ab72c73f7dd11318d5d4f3169ded23b86f33e9c469707638`.

Normalisation per `metadata.reproducible.digest_constructions.per_artifact` (DC-1).

**This approval is bound to that hash.** Per LAW-10 it is void if the subject content changes, and it names precisely what it approves.

## Authorising basis

The human owner, `BINDING.approval_authority: human-owner`, issued a live instruction in session `S-2026-08-08-06` assigning the Chief Systems Engineer in a cold context and directing that open item OI-C-06 — the three enabled `software.*` role artifacts sitting outside DC-4's declared coverage — be ruled by A4 before Compiler Stage 6 executes, with the required amendment and approval artifacts recorded and affected DC-1/DC-2 hashes recomputed.

That instruction is `core/PRECEDENCE.md` **rank 1** and outranks the rank-3 freeze registry. `core/PRECEDENCE.md` clause 4 and LAW-10 clause 4 require such an override be recorded before dependent work is committed. This artifact is that record. The authority is the human owner's; this file is its written form.

## Scope

| In scope | Out of scope |
|---|---|
| The manifest changes enumerated below, and no others | Any change to `SCH-framework-manifest.schema.json` — not amended; the amended manifest passes it unmodified |
| Replacing the registered digest for `framework/framework.manifest.json` in `FROZEN.md` with `subject_hash` | Any change to DC-1, DC-2, DC-3, DC-5 or TF-1/TF-2; any change to DC-4's record grammar, order, preimage, encoding, self-exclusion, B2a procedure, lock serialisation or worked example; any law rule or clause, role contract, partition, layer, tier, boot step or compiler stage definition |
| | Registration of `AIEF-AMD-012` itself — separate instrument, `APR-011` |
| | Execution of Compiler Stage 6; creation of `core/MANIFEST.lock`; any write to `BINDING.core_digest_pin` or any other BINDING field; any compiler implementation work |
| | Any ledger write, any git commit, tag or push |

## The change, enumerated

| # | Manifest location | Change | Ruling |
|---|---|---|---|
| 1 | `metadata.reproducible.digest_constructions.core_aggregate.authority` | Appended: "coverage extended to enabled-role agent artifacts by AIEF-AMD-012 AMD-39, disposing OI-C-06" | AMD-39 |
| 2 | `metadata.reproducible.digest_constructions.core_aggregate.covers` | One inserted clause: "plus every enabled-role agent artifact resolved per enabled_role_coverage" | AMD-39 |
| 3 | `metadata.reproducible.digest_constructions.core_aggregate.enabled_role_coverage` | **New** — the normative resolution rule (role token `<profile>.<name>` outside the selected profile resolves to the `files[]` entry at `core/profiles/<profile>/agents/AGT-<name>.md`, halt on non-resolution), determinism statement (covered set a function of `files[]`, the selected profile and `BINDING.enabled_agents` alone), scope limit (agent artifacts only) and worked-example status (unchanged) | AMD-39 |

No other member of the manifest changes; DC-4's worked example digest `eb6e969b…40325b1` is untouched and remains normative (AMD-40).

## Verification status

Ruled and applied by the same authority, `chief-systems-engineer · S-2026-08-08-06`, at the direction of the human owner. The separation-of-duties departure is recorded in AIEF-AMD-012 § *Separation of Duties*. Under LAW-05 this session cannot verify its own work; an independent cold-context `qa-engineer` audit of this session's work is dispatched later this phase by the same directing authority as the mitigating control.

Reproducible by a third party from the repository alone: the pre-change manifest at `git show 8546960:framework/framework.manifest.json` normalises to `prior_hash`; the working-tree manifest after this amendment normalises to `subject_hash`; the diff is the three changes above and no others. Schema conformance of the amended manifest was verified against the unmodified frozen `SCH-framework-manifest.schema.json` with a JSON Schema 2020-12 validator: PASS.

## Authority chain

| | |
|---|---|
| `core/PRECEDENCE.md` rank 1 | Live human instruction — the authorising basis |
| LAW-01 | A frozen artifact is changed only by an approved ECR and a recorded human approval |
| LAW-10 | Approval is an artifact bound to a content hash |
| LAW-12 | The coverage gap disposed by open decision with recorded rationale, never by assumption |
| `project/BINDING.md` | `approval_authority: human-owner` |
| AIEF-AMD-012 | The amendment this approval authorises |
