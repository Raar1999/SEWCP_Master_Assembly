# TPL - Session Summary

> **Generated artifact.** Emitted by aief-compile Stage 2 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `tpl-session-summary` |
| Layer / partition | L2 / core |
| Tier | T3 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |
| Producer | session closer |
| Consumers | next session |
| Filed at | `project/sessions/` |
| Authority | `LAW-09` Session · workflow `WF-01` |

---

A session is a **transaction**: it reads state at start and writes state at close. This artifact is what the next session inherits. **State lives in files, never in conversation history** - anything not written here is lost.

## Required sections

### 1 · Session id

The identifier, matching the ledger entry written at close. One active session per working tree.

| | |
|---|---|
| Session id | |
| Ledger entry | `L-nnnnnnn` |
| Opened / closed | ISO-8601 UTC |
| Working tree · branch | |

### 2 · Role

The role or roles adopted, declared explicitly, with the point of any switch. `LAW-11` requires an agent to declare its role and stay inside its contract.

### 3 · Work performed

What was done, in order. Sufficient for a cold reader to reconstruct the session without the transcript.

### 4 · Artifacts touched

| Path | Change | Authority |
|---|---|---|

Created, modified and deleted. Where a frozen artifact was touched, cite the ECR and the approval.

### 5 · Decisions

Decisions taken and the reasoning, including alternatives rejected. A decision recorded without its rationale will be re-litigated by a later session that cannot see why.

### 6 · Open items

Opened, closed and carried forward. Must reconcile with `project/OPEN_ITEMS.md`; that file is authoritative and this section points at it.

### 7 · Next action

**Explicit and concrete.** The next session boots cold and acts on this field. Name the artifact, the operation and the role.

> Insufficient: *continue the compiler work.*
> Sufficient: *Execute Compiler Stage 5, emitting `core/validation/CHECKS.md` and `core/validation/MANIFEST` per `manifest.validation`.*

Must agree with `project/STATE.md` field `next_action`; `STATE.md` governs where they differ.

## Acceptance conditions

| # | Condition | Test |
|---|---|---|
| 1 | Next action is explicit and concrete | §7 names artifact, operation and role |
| 2 | Session id matches the ledger entry | §1 `Session id` equals `session_id` of the ledger entry |

## Close order

Per `LAW-09`, non-negotiable:

```
entry file -> flush -> ledger/HEAD -> project/STATE.md -> release lock
```

An abandoned session leaves the repository exactly as it found it.

## Forbidden

| | |
|---|---|
| Closing without writing STATE | `LAW-09` - the transaction is incomplete |
| Recording a next action that requires conversation history to interpret | Defeats cold-start recovery |
| Releasing the lock before STATE is written | Close order |
