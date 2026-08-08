# TPL - Issue Report

> **Generated artifact.** Emitted by aief-compile Stage 2 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `tpl-issue-report` |
| Layer / partition | L2 / core |
| Tier | T3 |
| Owner | `project-manager` |
| Mutability | immutable |
| Producer | any agent |
| Consumers | `project-manager` |
| Filed at | `project/issues/` |
| Authority | workflow `WF-02` |

---

For observations that are **not** challenges to an authority. Where a finding contradicts a frozen artifact, a law or a specification, the instrument is an **ECR**, not an issue report.

| Use an issue report for | Use an ECR for |
|---|---|
| Tooling, process and infrastructure friction | Ambiguity in an authority - **ECR-Q** |
| Housekeeping and hygiene | Defect in an authority - **ECR-D** |
| Anything with no authority conflict | Anything requiring a ruling |

## Required sections

### 1 · Description

What was observed, factually. Separate observation from interpretation; the two are not equally reliable and a reader must be able to tell them apart.

### 2 · Severity

| Severity | Meaning | Response |
|---|---|---|
| **Critical** | Work cannot proceed | Immediate `project-manager` attention |
| **Major** | Work proceeds with material friction or risk | Scheduled |
| **Minor** | Inconvenience; no risk to deliverables | Backlog |
| **Observation** | Recorded for pattern detection | None required |

Severity is always assigned. An unassigned severity cannot be triaged and will be ignored.

### 3 · Reproduction

The steps that produce the observation, with environment and inputs. Where the issue is not reproducible, **declare that explicitly** - an intermittent issue that says so is actionable, one that stays silent is not.

### 4 · Affected artifacts

| Path | Effect |
|---|---|

Where nothing in the repository is affected, state the affected process or tooling instead.

### 5 · Proposed disposition

What the raiser suggests. Advisory only: disposition belongs to `project-manager`. Where the proposal turns out to require a ruling against an authority, the issue is **converted to an ECR** and this file records the conversion.

## Acceptance conditions

| # | Condition | Test |
|---|---|---|
| 1 | Severity assigned | §2 states one of the four levels |
| 2 | Reproduction stated or declared unavailable | §3 gives steps or explicitly declares non-reproducibility |

## Forbidden

| | |
|---|---|
| Using an issue report to challenge a frozen artifact | That requires an ECR - `LAW-02` |
| Filing without a severity | Condition 1 |
| Treating a proposed disposition as a decision | Disposition is `project-manager` authority |
