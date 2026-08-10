# ECR-Q-003 — Stage 1's core-emission barrier is contradicted by Stages 2, 5 and 6

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised while ruling on FIND-1 (build order), session `S-2026-08-08-02`.

```yaml
ecr_id:       ECR-Q-003
class:        Q                      # ambiguity - LAW-02
raised_by:    chief-systems-engineer · S-2026-08-08-02
status:       CLOSED
disposition:  A                      # barrier protects the Stage 1 output set
ruled_by:     chief-systems-engineer · S-2026-08-08-03
ruled_at:     2026-08-08T05:51:32Z
instrument:   framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md §AMD-23
approval:     approvals/APR-004_Amend_Framework_Manifest_AMD-009.md
affected_artifacts:
  - framework/AIEF-FRZ-001_Framework_Architecture_Freeze_1.0.0.md
  - framework/framework.manifest.json
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-08T02:36:52Z
related:      FIND-1                 # surfaced while correcting stage-crossing dependencies
```

---

## 1 · Class

**Q — ambiguity.** The barrier admits two readings and the manifest's own data satisfies only one of them. Nothing is provably wrong; the wording does not say which reading governs. Under LAW-02 the affected item **holds**; unrelated work proceeds.

## 2 · Affected artifacts

| Artifact | Role |
|---|---|
| `framework/framework.manifest.json` → `generation_order[stage 1].barrier` | Declares *"No later stage may emit into core"* |
| `framework/framework.manifest.json` → `generation_order[stage 2, 5, 6].outputs` | Declare `core/templates/**`, `core/validation/**`, `core/MANIFEST.lock` |
| `framework/AIEF-FRZ-001` Part 4, Stage 1 | Carries the same barrier wording |
| Compiler Stage 5 | The **next declared engineering activity**, which emits into `core/` |

`framework.manifest.json` and `AIEF-FRZ-001` are both frozen and hash-registered.

## 3 · Evidence

Read directly from the manifest, reproducible by any third party:

| Stage | Declared `outputs` | Emits into `core/`? |
|---|---|---|
| 1 | `BOOT.md`, `FRAMEWORK.md`, `README.md`, `core/**`, `core/profiles/<selected>/**` | yes |
| 2 | `core/templates/**` | **yes** |
| 3 | `project/**` | no |
| 4 | `adapters/**` | no |
| 5 | `core/validation/**` | **yes** |
| 6 | `core/MANIFEST.lock`, … | **yes** |

Corroborated by `files[]`: `tpl-*` entries carry `partition: core, generator: 2`; `checks` and `validation-manifest` carry `partition: core, generator: 5`; `manifest-lock` carries `partition: core, generator: 6`.

**Under the literal reading of the barrier, Stage 2 already violated it** — and Stage 2 is recorded as complete with its barrier satisfied (`STATE.md`). The evidence is the manifest's own content, not an assertion by this authority.

## 4 · Impact

| | |
|---|---|
| Stage 5 | The **next action**. It emits `core/validation/**`. Under the literal reading it cannot run at all. Under the intended reading it runs normally. The compiler needs to know which |
| Stage 6 | Same, for `core/MANIFEST.lock` — which the Stage 6 barrier separately declares *"is emitted only here"*, a statement that only makes sense if Stage 6 may emit into `core/` |
| Stage 2 | Already emitted. If the literal reading governs, a completed stage is retrospectively non-conforming |
| Everything else | Unaffected. The repository is bootable and no other work is held |

**Blocks nothing today.** It holds one question that Stage 5 must answer before it starts.

## 5 · Requested action

Ruling by `chief-systems-engineer` (A4), **in a session that did not raise this ECR**.

| # | Resolution | Note |
|---|---|---|
| A | The barrier means *no later stage may emit into the region of `core/` that Stage 1 owns* — L1 universal core and L3 profile. Later stages emit only into their own declared subtrees (`core/templates/`, `core/validation/`, `core/MANIFEST.lock`) | Consistent with every declared output, with the completed Stages 2–4, and with Stage 6's own barrier. **Recommended**, but the recommendation is not the ruling |
| B | The barrier means what it literally says, and the `outputs` of Stages 2, 5 and 6 are wrong | Would invalidate Stage 2's completion and leave Stages 5 and 6 with nowhere to emit. Recorded for completeness |
| C | The barrier is obsolete and should be struck | Loses the protection the barrier was written to give — that a later stage cannot overwrite Stage 1's output |

Whichever is chosen, the wording should be made precise enough that a compiler can evaluate it, and `AIEF-FRZ-001` Part 4 carries the same text and would need the same treatment — which makes this an amendment to two frozen artifacts, requiring recorded human approval under LAW-01 and LAW-10.

## 6 · Disposition

**CLOSED — Disposition A**, ruled by `chief-systems-engineer` · `S-2026-08-08-03`, a cold session that did not raise this ECR (`tpl-ecr` acceptance condition 3, LAW-02 clause 5, identity per AIEF-AMD-008 §AMD-20).

> The barrier protects the Stage 1 output set from later modification; it was never a prohibition on later stages emitting into their own declared `core/` subtrees. Stage 1 owns `BOOT.md`, `FRAMEWORK.md`, `README.md`, `core/profiles/<selected>/**`, and `core/**` excluding `core/templates/**` (Stage 2), `core/validation/**` (Stage 5) and `core/MANIFEST.lock` (Stage 6). Evaluable as pairwise disjointness of `generation_order[].outputs`.

| | |
|---|---|
| Instrument | `framework/AIEF-AMD-009` §AMD-23 — full ruling, rejected alternatives B and C, and the FRZ-001 supersession treatment |
| Approval | `project/approvals/APR-004`, bound to the manifest's post-amendment DC-1 digest |
| Manifest change | `generation_order[stage 1].barrier` and `.outputs` made precise; `validation[V-01].verifies` extended so the barrier is check-bound |
| `AIEF-FRZ-001` Part 4 Stage 1 | Barrier row superseded **in reading** per the AMD-001 §AMD-04 precedent; the document's bytes and registered digest are unchanged |
| Retrospective effect | Stage 2's completion is conforming; no completed work is invalidated |
| Stage 5 consequence | The question this ECR held for Stage 5 is answered: Stage 5 lawfully emits `core/validation/**`, its own declared subtree |

---

## Authority chain

| | |
|---|---|
| LAW-02 | Ambiguity is raised as ECR-Q; no ECR is closed by the agent that raised it |
| LAW-12 | Assumption is never a resolution method; recording the ambiguity and stopping is a compliant deliverable |
| LAW-01 / LAW-10 | Both affected artifacts are frozen; any correction needs an approved ECR and a recorded human approval |
| AIEF-AMD-002 §AMD-07 | Edge-type and build-order semantics, whose clarification surfaced this |
| AIEF-AMD-008 §AMD-20 | Agent identity is (role, session), which is why a later A4 session may rule on this |
