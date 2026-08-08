# TPL - Design Review

> **Generated artifact.** Emitted by aief-compile Stage 2 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `tpl-design-review` |
| Layer / partition | L2 / core |
| Tier | T3 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |
| Producer | reviewer |
| Consumers | `project-manager`, `chief-systems-engineer` |
| Filed at | `project/reviews/` |
| Authority | `LAW-04` Design Review · workflow `WF-03` |

---

**A reviewer may never be the originator.** That is the whole point of the artifact; independence is a property of identity, not of intent.

## Required sections

### 1 · Scope

What was reviewed, at which content hash, and what was deliberately excluded. A review that does not bound itself cannot be relied upon at a gate.

| | |
|---|---|
| Artifacts under review | paths |
| Content hash | normalised SHA-256 |
| Review class | peer · checker · design authority · gate |
| Excluded | explicit, or none |

### 2 · Criteria

The standards applied, each traceable to an authority - a law, a frozen specification, or a declared acceptance condition. Criteria are fixed **before** findings are recorded.

### 3 · Findings with severity

| # | Finding | Severity | Evidence | Criterion |
|---|---|---|---|---|

| Severity | Meaning |
|---|---|
| **Critical** | Blocks disposition. Raises ECR-D |
| **Major** | Must be actioned before the next gate |
| **Minor** | Actioned or accepted with rationale |
| **Observation** | Recorded, no action required |

Every finding cites evidence independent of the reviewer's own assertion (`LAW-05`).

### 4 · Disposition

Binary, per `LAW-04`.

| | |
|---|---|
| Disposition | **APPROVED** or **REJECTED** |
| Reviewer | role, identity |
| Originator | role, identity |
| Independence | reviewer identity **differs** from originator identity - confirmed |
| Date | |

**Approved with comments** is not a disposition. If findings must be actioned first, the disposition is REJECTED.

### 5 · Actions with owners

| # | Action | Owner | Due | Finding |
|---|---|---|---|---|

Every action carries an owner and a due date. An unowned action is not an action.

## Acceptance conditions

| # | Condition | Test |
|---|---|---|
| 1 | Reviewer identity differs from originator | §4 names both; they are not equal |
| 2 | Disposition is binary | §4 reads exactly APPROVED or REJECTED |

## Forbidden

| | |
|---|---|
| Reviewing one's own artifact | `LAW-04` - invalid regardless of rigour |
| A non-binary disposition | `LAW-03` |
| A finding without evidence | `LAW-05` - a claim is not evidence for itself |
| An action without an owner | §5 |
