# TPL - Engineering Change Request

> **Generated artifact.** Emitted by aief-compile Stage 2 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `tpl-ecr` |
| Layer / partition | L2 / core |
| Tier | T3 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |
| Producer | any agent |
| Consumers | `chief-systems-engineer`, `human-owner` |
| Filed at | `project/ecr/` |
| Schema | `core/schemas/SCH-ecr.schema.json` - severity BLOCKING |
| Authority | `LAW-02` Engineering Change Request · workflow `WF-04` |

---

The **only** instrument by which a lower authority may challenge a higher one. Under `core/PRECEDENCE.md` an AI conclusion is rank 7 and overrides nothing; raising an ECR is its sole sanctioned path.

## Field schema

```yaml
ecr_id:       ECR-<CLASS>-nnn
class:        Q | D
raised_by:    role, identity, session
status:       OPEN | CLOSED | CLOSED-PARTIAL
disposition:  PENDING | <ruling>
raised_at:    ISO-8601 UTC
```

## Required sections

### 1 · Class

| Class | Trigger | Effect on work |
|---|---|---|
| **Q** | Ambiguity - the authority is silent or admits more than one reading | The affected item **holds**; unrelated work proceeds |
| **D** | Defect - the authority is wrong, self-contradictory or impossible | The affected work **STOPS** |

Class is Q or D. There is no third class, and a finding that is merely inconvenient is neither.

### 2 · Affected artifacts

Every artifact touched by the request, with its role in the change. Paths are repository-relative. Where an artifact is frozen, say so.

### 3 · Evidence

**Evidence must be independent of the claim.** A statement by the raising agent is not evidence for itself (`LAW-05`). Admissible: content hashes, git objects, quoted specification text with citation, reproducible commands, tool output.

State the method so a third party can reproduce the finding from the repository alone.

### 4 · Impact

What is blocked, what is merely held, and what is unaffected. Name the gates and the downstream artifacts. If the ECR blocks nothing, say that plainly - it changes the disposition urgency.

### 5 · Requested action

The resolutions admissible to the disposing authority. Give a recommendation and the reasoning; the ruling is not the raiser's to make. Record rejected alternatives and why, so the decision is auditable later.

### 6 · Disposition

| | |
|---|---|
| Disposition | the ruling, or **PENDING** |
| Ruled by | role, identity - **not** the raiser |
| Approval artifact | `project/approvals/APR-nnn`, where human authority is required |
| Date | |

Where the disposition changes a frozen artifact, `LAW-01` requires **both** an approved ECR and a recorded human approval bound to a content hash (`LAW-10`).

## Acceptance conditions

| # | Condition | Test |
|---|---|---|
| 1 | Class is Q or D | §1 states exactly one of them |
| 2 | Evidence is independent of the claim | §3 cites a source other than the raiser's assertion |
| 3 | Disposition recorded by an agent that did not raise it | §6 *Ruled by* ≠ `raised_by` |

## Forbidden

| | |
|---|---|
| Ruling on one's own ECR | Condition 3 |
| Resolving the underlying ambiguity by assumption while the ECR is open | `LAW-12` |
| Proceeding with work stopped by a class-D ECR | `LAW-02` |
| Editing a frozen artifact in anticipation of a favourable ruling | `LAW-01` |
