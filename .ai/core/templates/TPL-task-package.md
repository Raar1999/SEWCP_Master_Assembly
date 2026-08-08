# TPL - Task Package

> **Generated artifact.** Emitted by aief-compile Stage 2 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `tpl-task-package` |
| Layer / partition | L2 / core |
| Tier | T3 |
| Owner | `project-manager` |
| Mutability | immutable |
| Producer | `project-manager` |
| Consumers | assigned agent |
| Filed at | `project/tasks/` |
| Schema | `core/schemas/SCH-task.schema.json` - severity BLOCKING |
| Authority | `LAW-11` Agent Conduct · workflow `WF-02` |

---

The unit of dispatched work. An agent accepts a task package and loads T3 context; **without one there is no assignment**, and an agent acting without an assignment is outside its contract.

## Field schema

```yaml
task_id:              T-nnn
role:                 must resolve in project/ROSTER.md
objective:            single sentence
inputs:               [...]
deliverable:          [...]
acceptance_criteria:  [...]   # binary
forbidden_actions:    [...]
escalation:           [...]
```

## Required sections

### 1 · Task id

`T-nnn`, unique within the project. Cited by the ledger entry and by any artifact the task produces.

### 2 · Role

The assigned role. **Must resolve in `project/ROSTER.md`** - a role marked UNASSIGNED cannot be dispatched, and assignment is a `project-manager` action.

| | |
|---|---|
| Role | |
| Identity | from `ROSTER.md` |
| Authority level | A1 · A2 · A3 · A4 |
| Duty conflicts checked | against the artifact under task |

### 3 · Objective

One sentence: what done looks like. If it needs a paragraph, the task is too large and should be split.

### 4 · Inputs

Everything the agent needs, by path. An input not listed here must be requested, not assumed. Include the tier at which each should be loaded.

### 5 · Deliverable

The artifact or artifacts to be produced, with the template contract each must satisfy and the filing path.

### 6 · Acceptance criteria

**Binary.** Each criterion is testable to PASS or FAIL by someone who did not perform the work.

| # | Criterion | Test |
|---|---|---|

Not acceptable: *high quality*, *comprehensive*, *as appropriate*. These cannot be failed, so they cannot be passed.

### 7 · Forbidden actions

Prohibitions specific to this task, beyond those already in the role contract. Where the task touches a frozen artifact or a protected partition, state the prohibition explicitly rather than relying on the agent to recall it.

### 8 · Escalation

| Condition | Escalate to |
|---|---|

Every foreseeable stop condition has a path. An agent that meets an unlisted stop condition escalates to `project-manager` by default and **does not assume** (`LAW-12`).

## Acceptance conditions

| # | Condition | Test |
|---|---|---|
| 1 | Role resolves in the roster | §2 role appears in `project/ROSTER.md` and is not UNASSIGNED |
| 2 | Acceptance criteria are binary | Every row in §6 is testable to PASS or FAIL |

## Forbidden

| | |
|---|---|
| Dispatching to an UNASSIGNED role | Condition 1 |
| Non-binary acceptance criteria | Condition 2 - `LAW-03` |
| Assigning verification of an artifact to the agent that produced it | `LAW-05` |
| `project-manager` gate-passing its own plan unaided | Separation of duties |
