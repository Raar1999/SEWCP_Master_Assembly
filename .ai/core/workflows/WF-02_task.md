# WF-02 - Task

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `wf-02` |
| Layer / partition | L1 / core |
| Tier | T3 |
| Owner | `project-manager` |
| Mutability | immutable |

---

Covers 2 runtime phase(s).

## Phase 3 - Agent Creation

| | |
|---|---|
| Entry | Task exists |
| Exit | Role assigned; T2 loaded; contract acknowledged |
| Produces | role declaration |
| Blocking condition | **Separation-of-duty conflict** |

## Phase 4 - Task Execution

| | |
|---|---|
| Entry | Role assigned; task package read |
| Exit | Deliverable meets template contract |
| Produces | deliverable |
| Blocking condition | **LAW-12 stop condition** |
