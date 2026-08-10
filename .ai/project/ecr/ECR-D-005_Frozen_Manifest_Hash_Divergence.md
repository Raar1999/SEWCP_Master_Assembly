# ECR-D-005 — Freeze registry does not verify: `framework.manifest.json`

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised at boot step B7/B8 of session `S-2026-08-08-01`.

```yaml
ecr_id:       ECR-D-005
class:        D                      # defect - LAW-02
raised_by:    boot · S-2026-08-08-01           # boot step B7/B8, before role assignment
status:       CLOSED
disposition:  A - RE-REGISTER        # ruled by human-owner, BINDING.approval_authority
ruled_by:     human-owner · S-2026-08-08-01
approval:     approvals/APR-001_Reregister_Framework_Manifest.md
affected_artifacts:
  - framework/framework.manifest.json
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-08T01:31:23Z
closed_at:    2026-08-08T02:36:52Z   # residual ECR-Q-001 discharged; see Execution below
residual:     none                   # ECR-Q-001 closed by AIEF-AMD-008 §AMD-16
```

> **`raised_by` was recorded as `claude-code session S-2026-08-08-01 (pre-role, boot-time integrity check)`.** Corrected under `AIEF-AMD-008` §AMD-20: an actor-provenance field names a framework role and a session, never a model, vendor, product or host adapter. The reserved token `boot` denotes an action taken by the boot sequence before role assignment, steps B1–B8 — which is what this artifact's own header records. **The explanatory text is retained above and no information is lost;** only the machine-read field changed.

---

## 1 · Class

**D — defect.** Not an ambiguity. The substance of every change involved is authorised; the *record that proves it* is absent. A registered frozen artifact no longer matches its registered hash, so `FROZEN.md` currently fails to verify. Under LAW-02 a defect **stops the affected work**.

## 2 · Affected artifacts

| Artifact | Role in the defect |
|---|---|
| `framework/framework.manifest.json` | Registered frozen artifact; content diverges from registered hash |
| `.ai/project/FROZEN.md` | Freeze registry; holds the stale hash and a stale aggregate |
| `.ai/project/STATE.md` field `frozen_set_hash` | Derived from the stale aggregate |

## 3 · Evidence

Evidence is independent of this claim: it is the content of git objects and the recorded registry, not an assertion by the agent that raised the ECR. Every line is reproducible by a third party from the repository alone.

**Normalisation** — as declared in `FROZEN.md`: SHA-256 over UTF-8, LF line endings, trailing whitespace stripped, terminal newline enforced.

### 3.1 Registry verification, all 16 registered artifacts

| Result | Count |
|---|---|
| Verify | **15** |
| Fail | **1** — `framework/framework.manifest.json` |

That 15 of 16 verify establishes the normalisation procedure is correct, so the single failure is a property of the artifact, not of the method.

| | Digest |
|---|---|
| Registered in `FROZEN.md` | `c33e574a3bc16eec79bcd078d7e04402709d274ba3421cd428f94691fed01799` |
| Computed from working tree | `f72485c24a21f8ebe7c8eb9a4a75615e7e0af2341f19184d4cd3228007f31467` |

### 3.2 Divergence located in history

Hashing the artifact at each commit that touched it:

| Commit | Release | Normalised digest | Matches registry |
|---|---|---|---|
| `a45823d` | 0.3 | `c33e574a…fed01799` | **yes** |
| `a1df1a6` | 0.4 | `801b94e0…b622eb26` | no |
| `7c530f4` | 0.6 | `6918ad72…f30056cea9` | no |
| `6ce3508` | HEAD | `f72485c2…07f31467` | no |

`FROZEN.md` was created at `a45823d` and **has not been modified since** (`git log -- .ai/project/FROZEN.md` returns exactly one commit). The registry was correct when written. The artifact moved three times underneath it; the registry never followed.

### 3.3 The divergence is fully attributable to approved amendments

`git diff a45823d HEAD -- framework/framework.manifest.json` → 15 insertions, 12 deletions. Every hunk maps to an A4 amendment already present in `framework/`:

| Hunk | Amendment |
|---|---|
| `repository-engineer` contract expansion; LAW-07 clauses; check `V-22` | AIEF-AMD-004 — Repository Engineer Autonomy |
| `mechanical.cad-engineer` agent; file entry `mech-agt-cad`; profile agents list; `file_count` 15 → 16 | AIEF-AMD-006 — Mechanical CAD Engineer |
| `compiler_stage` in `tpl-current-state` required sections and acceptance conditions; `sch-state.required_fields` | AIEF-AMD-007 — compiler_stage State Field |

**No unattributed change exists.** There is no evidence of tampering. The defect is a failure to re-register, not a failure of authorisation.

## 4 · Impact

### 4.1 Immediate — Compiler Stage 2 is blocked

Stage 2 (`Generate Templates`) declares its inputs as `templates`, `agents`, `runtime_sequence` — **all read from `framework.manifest.json`**, the one artifact that fails verification. Stage 2 emits into `core/`, an integrity-hashed partition, which Stage 6 later seals into `core/MANIFEST.lock`.

Emitting Stage 2 now would build layer L2 on an input whose provenance chain has a documented gap, and Stage 6 would subsequently certify that gap as sound.

### 4.2 The gap cannot be closed by agent analysis

§3.3 shows the drift is *explainable*. It does not make it *approved*. Under `core/PRECEDENCE.md`, an AI conclusion is **rank 7 and overrides nothing**; its only sanctioned path is to raise an ECR. LAW-10 reserves freeze and thaw to human authority, and requires approval bound to a content hash rather than remembered assent. This ECR is therefore the correct and only instrument available to the raising agent.

### 4.3 Standing consequences while OPEN

| Consequence | |
|---|---|
| `FROZEN.md` | Non-verifying; cannot currently evidence LAW-01 for any artifact |
| `STATE.frozen_set_hash` | Stale — derived from an aggregate that no longer describes the set |
| Boot step B2a | Already blocked by CMP-BLOCK-004 (Stage 6). Unaffected in status, but note that B2a covers `core/` only — **it would never have caught this.** `framework/` is guarded solely by `FROZEN.md` |
| ECR-D-001…004 | Unaffected. Independent defects against the SEWCP specification |

### 4.4 Systemic observation

Three consecutive releases amended a frozen artifact without re-registering it. The freeze registry has no automated check binding it to the working tree — the natural home for one is `V-06` (LAW-10) or a new check under Compiler Stage 5, neither of which exists yet (CMP-BLOCK-005). This defect was detected by an opportunistic boot-time check, not by declared machinery. **Recommend a standing check be bound as part of the disposition**, otherwise recurrence is near-certain.

## 5 · Requested action

Ruling by `chief-systems-engineer` (A4), with recorded human approval per LAW-01 and LAW-10. Three admissible dispositions:

| # | Disposition | Action | Consequence |
|---|---|---|---|
| **A** | **Re-register** *(recommended)* | Human approval artifact naming AMD-004, AMD-006, AMD-007 as the authorising basis. Update `FROZEN.md` entry to `f72485c2…07f31467`, recompute the aggregate, update `STATE.frozen_set_hash`. Bind a standing verification check. | Registry verifies; Stage 2 unblocks; recurrence prevented |
| B | Revert | Restore the manifest to `c33e574a…` | **Rejected on its face** — discards three approved amendments. Recorded only for completeness |
| C | Waive | Proceed with Stage 2 against the unverified input, deferring re-registration | Not recommended. Stage 6 would seal an unproven chain, and the waiver must itself be a recorded human override under LAW-10 |

Disposition **A** restores the invariant with no loss of approved work.

## 6 · Disposition

**A — RE-REGISTER.** Ruled by the **human-owner** (`BINDING.approval_authority`), who is not the raising agent, satisfying the `tpl-ecr` acceptance condition. Approval recorded at [`approvals/APR-001_Reregister_Framework_Manifest.md`](../approvals/APR-001_Reregister_Framework_Manifest.md), bound to content hash `f72485c2…07f31467` per LAW-10.

### Execution

| # | Action | Status |
|---|---|---|
| 1 | Human approval artifact naming AMD-004/006/007 as authorising basis | ✅ `APR-001` |
| 2 | `FROZEN.md` entry → `f72485c2…07f31467` | ✅ 16 of 16 verified at the time |
| 3 | Recompute the aggregate | ✅ **discharged 2026-08-08** by AIEF-AMD-008 §AMD-16 (DC-2), closing ECR-Q-001. Value `080771b0…f6b6367a` |
| 4 | Update `STATE.frozen_set_hash` | ✅ same value, full 64 characters |
| 5 | Bind a standing verification check | ◑ **V-24 declared** by AIEF-AMD-008 §AMD-19 as a Compiler Stage 5 requirement; **not implemented**. Remains **OI-V-02** |

Actions 1 and 2 discharged the defect: the registry verified. Actions 3 and 4 were held by ECR-Q-001 and are now complete. **Action 5 is declared but not in effect** — this ECR's own §4.4 warned that without a standing check recurrence is near-certain, and that warning still stands until Stage 5 runs.

> **Note.** The registered digest for `framework/framework.manifest.json` has since moved again, to `636cf22b…14b38d3c`, under AIEF-AMD-008 and approval `APR-002`. That is a separate, approved and registered change — not a recurrence of this defect. Registry membership is now 24 artifacts.

### Correction to §3.2, recorded

§3.2 tabulates four commits under the caption *"each commit that touched it"*. Independent verification (`project/verification/VER-001` §3.3) found **five**: `a403059` (Release 0.2, the creating commit) was omitted. The omission is immaterial to the conclusion — `a403059` precedes the registration at `a45823d` — but the caption overstated the table's coverage. Recorded here rather than left standing.

### Effect on blocked work

**Framework Compiler Stage 2 is RELEASED.** Its integrity dependency was the per-artifact digest of `framework.manifest.json`, which now verifies. ECR-Q-001 concerns the registry aggregate, which is not a Stage 2 input.

### Verification independence

Actions 1 and 2 were executed by the session that raised this ECR. Under LAW-05 that session cannot verify them.

**Independent confirmation is now on record.** A `qa-engineer` audit from a cold context recomputed all 16 registered digests, the attribution chain and the commit history without relying on any assertion in this ECR, and returned **PASS** on every criterion. Filed at [`../verification/VER-001_Independent_Verification_ECR-D-005_and_Stage_2.md`](../verification/VER-001_Independent_Verification_ECR-D-005_and_Stage_2.md). **OI-V-01 closes on that report.**

Actions 3 and 4, and the registry expansion that followed, were performed by session `S-2026-08-08-02` and are **not** covered by that audit — recorded as **OI-V-03**.

---

## Authority chain

| | |
|---|---|
| LAW-01 | Architecture Freeze — a frozen artifact changes only by approved ECR and recorded human approval |
| LAW-02 | Engineering Change Request — a defect is raised as ECR-D and stops the affected work |
| LAW-10 | Human Approval — approval is bound to a content hash; freeze and thaw are human authority only |
| LAW-12 | Ambiguity and Stop Conditions — assumption is never a resolution method |
| `core/PRECEDENCE.md` | AI inference is rank 7 and overrides nothing; raising an ECR is its only path |
| `manifest.templates → tpl-ecr` | Required sections and acceptance conditions |
| `core/schemas/SCH-ecr.schema.json` | Field schema, severity BLOCKING |
