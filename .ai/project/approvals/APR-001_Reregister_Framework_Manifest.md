# APR-001 — Re-registration of `framework.manifest.json` in the freeze registry

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for ECR-D-005 disposition A.

```yaml
approval_id:   APR-001
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-08T01:31:23Z
subject_path:  framework/framework.manifest.json
subject_hash:  f72485c24a21f8ebe7c8eb9a4a75615e7e0af2341f19184d4cd3228007f31467
prior_hash:    c33e574a3bc16eec79bcd078d7e04402709d274ba3421cd428f94691fed01799
scope:         Re-registration of the named artifact in FROZEN.md at the stated subject_hash.
               Disposition A of ECR-D-005.
session:       S-2026-08-08-01
```

---

## Subject

`framework/framework.manifest.json`, at normalised SHA-256 `f72485c24a21f8ebe7c8eb9a4a75615e7e0af2341f19184d4cd3228007f31467`.

Normalisation as declared in `FROZEN.md`: UTF-8, LF line endings, trailing whitespace stripped, terminal newline enforced.

**This approval is bound to that hash.** Per LAW-10, it is void if the subject content changes, and it names precisely what it approves.

## Scope

| In scope | Out of scope |
|---|---|
| Replacing the registered digest for `framework/framework.manifest.json` in `FROZEN.md` with `subject_hash` | The aggregate digest of the freeze set — construction undefined, held by **ECR-Q-001** |
| Recording ECR-D-005 disposition as **A — re-register** | `STATE.frozen_set_hash` — derived from the aggregate, therefore also held |
| | Any change to the manifest's *content*, which is not modified by this approval |

## Rationale

The registered digest was correct when `FROZEN.md` was written at commit `a45823d`. The artifact was subsequently amended three times, at `a1df1a6`, `7c530f4` and `6ce3508`. `FROZEN.md` was never updated to follow.

`git diff a45823d HEAD -- framework/framework.manifest.json` yields 15 insertions and 12 deletions, and **every hunk maps to an amendment already approved under A4 authority**:

| Change | Authorising amendment |
|---|---|
| `repository-engineer` contract expansion; LAW-07 clauses; check `V-22` | AIEF-AMD-004 |
| `mechanical.cad-engineer` agent, file entry, profile list, `file_count` 15 → 16 | AIEF-AMD-006 |
| `compiler_stage` in `tpl-current-state` and `sch-state.required_fields` | AIEF-AMD-007 |

No unattributed change exists. The substance was authorised; only the registration lapsed. This approval supplies the missing record, restoring the LAW-01 evidence chain without altering any approved work.

Disposition B (revert) was rejected because it would discard three approved amendments. Disposition C (waive) was rejected because Compiler Stage 6 would then seal an unproven provenance chain.

## Verification status

Re-registration was performed by the same session that raised ECR-D-005. Under LAW-05 an agent may not verify an artifact it produced, so this change **has not been independently verified**. Independent confirmation by `qa-engineer` from a cold context remains outstanding and is recorded as an open item.

The underlying evidence is nonetheless independently reproducible by any third party from the repository alone:

```
git show a45823d:framework/framework.manifest.json   # hashes to prior_hash
git diff a45823d HEAD -- framework/framework.manifest.json
```

## Authority chain

| | |
|---|---|
| LAW-01 | A frozen artifact is changed only by an approved ECR and a recorded human approval |
| LAW-10 | Approval is an artifact bound to a content hash; freeze and thaw are human authority only |
| `core/PRECEDENCE.md` rank 1 | Live human instruction — the disposition selection that authorises this record |
| `project/BINDING.md` | `approval_authority: human-owner` |
| ECR-D-005 | The change request this approval dispositions |

---

## Addendum — 2026-08-08, `chief-systems-engineer` · `S-2026-08-08-02`

**Appended, not edited.** No text above this rule is altered. The approval itself, its scope and its hash binding stand exactly as written.

### Provenance fields — no correction required

`AIEF-AMD-008` §AMD-20 rules the authoritative representation for actor-provenance fields: a framework role and a session, never a model, vendor, product or host adapter. **This artifact already conforms.** `approver: human-owner` is a `roleId` registered in `core/agents/INDEX.md` at authority level **H**, and `session: S-2026-08-08-01` is a session identifier. No AI attribution is present anywhere in this file. The three ECRs of the same session did not conform and were corrected; this one needed nothing.

### Verification status — now satisfied

The § *Verification status* section above records that this change had not been independently verified. **It now has been.** A cold-context `qa-engineer` audit recomputed `subject_hash`, `prior_hash` and all sixteen registered digests independently, mapped every diff hunk to its authorising amendment, and returned **PASS** on that criterion. Filed at [`../verification/VER-001_Independent_Verification_ECR-D-005_and_Stage_2.md`](../verification/VER-001_Independent_Verification_ECR-D-005_and_Stage_2.md). `OI-V-01` is closed.

### Subject hash superseded — this approval is now spent

`framework/framework.manifest.json` has since been amended under `AIEF-AMD-008` and re-registered at `636cf22b9080b5d5178542fc42b618fc75033129a5932167d3b12e3214b38d3c`, approved by [`APR-002`](APR-002_Amend_Framework_Manifest_AMD-008.md).

Per LAW-10 clause 2, *"an approval is invalidated automatically when the bound content hash changes."* **This approval no longer authorises the current content and is not cited as doing so.** It remains the valid and permanent record of what it did authorise: the re-registration from `c33e574a…fed01799` to `f72485c2…07f31467`. `APR-002` covers the state that followed. The chain has no gap.
