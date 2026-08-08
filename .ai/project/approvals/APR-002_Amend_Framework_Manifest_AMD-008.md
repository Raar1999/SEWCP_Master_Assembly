# APR-002 — Amendment of `framework.manifest.json` under AIEF-AMD-008

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the manifest change made by AIEF-AMD-008.

```yaml
approval_id:   APR-002
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-08T02:36:52Z
subject_path:  framework/framework.manifest.json
subject_hash:  636cf22b9080b5d5178542fc42b618fc75033129a5932167d3b12e3214b38d3c
prior_hash:    f72485c24a21f8ebe7c8eb9a4a75615e7e0af2341f19184d4cd3228007f31467
scope:         Amendment of the named artifact by AIEF-AMD-008 rulings AMD-16 through AMD-20,
               and re-registration in FROZEN.md at the stated subject_hash.
session:       S-2026-08-08-02
applied_by:    chief-systems-engineer · S-2026-08-08-02
basis:         live human-owner instruction, core/PRECEDENCE.md rank 1
```

---

## Subject

`framework/framework.manifest.json`, at normalised SHA-256 (DC-1)
`636cf22b9080b5d5178542fc42b618fc75033129a5932167d3b12e3214b38d3c`.

Normalisation as declared in `FROZEN.md` and now in `metadata.reproducible.digest_constructions.per_artifact` (DC-1): UTF-8, LF line endings, trailing whitespace stripped, exactly one terminal newline.

**This approval is bound to that hash.** Per LAW-10 it is void if the subject content changes, and it names precisely what it approves.

## Authorising basis

The human owner, `BINDING.approval_authority: human-owner`, issued a live instruction authorising this work, including: *"If an amendment is required, author the appropriate ECR/amendment and update the manifest/source of truth."*

That instruction is `core/PRECEDENCE.md` **rank 1** and outranks the rank-3 freeze registry. `core/PRECEDENCE.md` clause 4 and LAW-10 clause 4 both require that such an override be **recorded before dependent work is committed**. This artifact is that record. It is not self-authorisation: the authority is the human owner's, and this file is its written form.

## Scope

| In scope | Out of scope |
|---|---|
| The five manifest changes enumerated below, and no others | Any change to `SCH-framework-manifest.schema.json` — **not amended**; the manifest validates against it unchanged |
| Replacing the registered digest for `framework/framework.manifest.json` in `FROZEN.md` with `subject_hash` | Any change to a law rule or clause, a role contract, a schema, a partition, layer, tier, boot step or compiler stage definition |
| | Registration of the eight additional `framework/` artifacts — separate instrument, `APR-003` |
| | Execution of Compiler Stage 5 or Stage 6 |
| | Any ledger write |

## The change, enumerated

| # | Manifest location | Change | Ruling |
|---|---|---|---|
| 1 | `metadata.reproducible.digest_constructions` | Added. Declares DC-1 (restated unchanged), DC-2 freeze-set aggregate, DC-3 ledger entry-hash chain — each with covered fields, canonical serialisation, ordering, encoding, self-exclusion, chain rule, genesis values and a published worked example | AMD-16, AMD-17 |
| 2 | `files[].depends_on` × 6 | Six backward stage edges removed: `wf-02→tpl-task-package`, `prof-mech→binding`, `prof-soft→binding`, `prof-res→binding`, `binding→manifest-lock`, `adp-ci→validation-manifest` | AMD-18 |
| 3 | `dependencies.edges`, `files[binding].referenced_by` | One `references` edge added (`wf-02→tpl-task-package`); `binding.referenced_by` gains `prof-mech`, `prof-soft`, `prof-res`. **No semantic relation is lost** | AMD-18 |
| 4 | `generation_order[stage 6].outputs` | Gains the `BINDING.core_digest_pin` write, which `AIEF-FRZ-001` Part 4 already required and the manifest did not declare | AMD-18 |
| 5 | `validation` | `V-22.verifies` extended with the actor-provenance test; `V-23` stage monotonicity, `V-24` freeze registry and `V-25` encoding conformance declared. **Declared only — Stage 5 is not executed** | AMD-19, AMD-20 |

## Rationale

Three defect classes were open against the manifest, each raised by an authority other than the one that ruled on it.

1. **Two required digests had no construction.** `frozen_set_hash` and the ledger `entry_hash` were required by schema, verified by boot step B4, and depended upon by `STATE.md` — and constructed nowhere. ECR-Q-001 and ECR-Q-002 correctly refused to invent one; the refusal held two workstreams and could not be lifted without a ruling. The manifest is the single source of truth, so the construction belongs in it.
2. **Six `depends_on` edges ran backwards across compiler stages.** No execution of `generation_order` satisfies any of them. V-02 cannot detect them because they are acyclic. This is `CMP-BLOCK-014` recurring, and it recurred *because* `AIEF-AMD-002` §AMD-07 declared the semantics without binding a check.
3. **A required provenance field and a BLOCKING law appeared to collide.** They did not: `tpl-ecr` already declares the grammar `role, identity, session`, and the offending values conformed to neither it nor LAW-07.

Every change is additive or a metadata correction. **No approved work is discarded and no capability is removed.**

## Verification status

Ruled and applied by the same authority, `chief-systems-engineer` · `S-2026-08-08-02`, at the direction of the human owner. `core/agents/INDEX.md` records that `chief-systems-engineer` *"may not implement what it approved"*; the departure is authorised at rank 1 and is recorded in AIEF-AMD-008 § *Separation of Duties* rather than left implicit.

Under LAW-05 this session cannot verify its own work. **Independent confirmation is outstanding and recorded as OI-V-03.**

The underlying evidence is reproducible by a third party from the repository alone:

```
git show 6ce3508:framework/framework.manifest.json     # hashes to prior_hash under DC-1
git diff  6ce3508 -- framework/framework.manifest.json # the five changes above, and no others
```

## Authority chain

| | |
|---|---|
| `core/PRECEDENCE.md` rank 1 | Live human instruction — the authorising basis |
| LAW-01 | A frozen artifact is changed only by an approved ECR and a recorded human approval |
| LAW-10 | Approval is an artifact bound to a content hash; a verbal override is recorded before dependent work is committed |
| LAW-02 | ECR-Q-001 and ECR-Q-002 dispositioned by an authority that did not raise them |
| `project/BINDING.md` | `approval_authority: human-owner` |
| AIEF-AMD-008 | The amendment this approval authorises |
