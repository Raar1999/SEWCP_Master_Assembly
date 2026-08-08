# TPL - Current State

> **Generated artifact.** Emitted by aief-compile Stage 2 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `tpl-current-state` |
| Layer / partition | L2 / core |
| Tier | T3 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |
| Producer | session closer |
| Consumers | next session boot |
| Filed at | `project/STATE.md` |
| Schema | `core/schemas/SCH-state.schema.json` - severity BLOCKING |
| Authority | `LAW-09` Session |

---

The **authoritative resume point**. Read at boot step B3, written at every session close. A cold session recovers the entire engineering position from this file and the artifacts it points at - **never from conversation history**.

The ledger is authoritative; `STATE.md` is a derived cache. Where they diverge, boot step B4 halts for human reconciliation.

## Field schema

```yaml
lifecycle_stage:  <id>          # from the active profile
active_gate:      <id>
compiler_stage:
  next:           <n>
  complete:       [...]
  outstanding:    [...]
last_ledger_seq:  <n>
frozen_set_hash:  <digest>
active_tasks:     [...]
blockers:         [...]
next_action:      <explicit and concrete>
```

## Required sections

### 1 · Lifecycle stage

The current stage, from the active profile's declared set. Profiles supply their own lifecycle; a stage id that does not resolve against the active profile is invalid.

### 2 · Active gate

The gate currently in force, with its status. Gate topology and disposition are governed by `LAW-03`; disposition is binary and *substantially complete* is not a disposition.

### 3 · Compiler stage

Complete and outstanding stages, **declared explicitly**.

```yaml
compiler_stage:
  next:           2
  complete:       [1, 3, 4]
  outstanding:    [2, 5, 6]
```

Stage completion is **never** left to be inferred from the presence or absence of files on disk. Inference is what this framework exists to eliminate, so the fact is declared. Where a stage was executed out of order, record the deviation.

### 4 · Last ledger sequence

`last_ledger_seq`, which **must equal** `ledger/HEAD.seq`. This is the reconciliation that boot step B4 checks; a mismatch halts boot.

At genesis (`HEAD.state: genesis`, `seq: 0`) B4 check 1 is vacuous; checks 2 and 3 are operative.

### 5 · Open blockers

Every item preventing progress, by id. Resolves in full against `project/OPEN_ITEMS.md`, which is authoritative - this section is an index into it, not a duplicate.

Distinguish **blocking** from **open but not blocking**: a reader must be able to tell what actually stops work.

### 6 · Active tasks

Task ids currently dispatched, or an empty list. Empty is a valid and meaningful value; absence of the field is not.

### 7 · Frozen set hash

The digest over the registered frozen set, mirroring `project/FROZEN.md`.

The registry declares the construction. **A digest whose construction is not declared cannot be recomputed or verified**, and a value that cannot be reproduced by a third party is not evidence. Where the construction is undeclared, hold the field and raise **ECR-Q** rather than substituting an invented one.

### 8 · Next action

**Explicit and concrete.** The single field the next session acts on. Name the artifact, the operation and the role.

Where work is stopped by a class-D ECR, the next action is the **disposition of that ECR**, not the stopped work.

## Acceptance conditions

| # | Condition | Test |
|---|---|---|
| 1 | Last ledger sequence equals HEAD sequence | §4 `last_ledger_seq` == `ledger/HEAD.seq` |
| 2 | Compiler stage declares complete and outstanding stages explicitly, never by inference | §3 lists both, as literal stage numbers |
| 3 | Within the 1100 token cap | T1 budget; measured at Compiler Stage 6 |

## Forbidden

| | |
|---|---|
| Recording a state that diverges from the ledger | `LAW-09` - the ledger is authoritative |
| Leaving `next_action` implicit or narrative | Defeats cold-start recovery |
| Inferring compiler stage from the filesystem | Condition 2 |
| Exceeding the 1100 token cap | Condition 3 - boot ceiling is 6000 tokens for T0 + T1 |
