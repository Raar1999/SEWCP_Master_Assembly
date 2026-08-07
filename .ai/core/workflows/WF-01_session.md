# WF-01 - Session

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `wf-01` |
| Layer / partition | L1 / core |
| Tier | T1 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |

---

Covers 3 runtime phase(s).

## Phase 1 - Session Start

| | |
|---|---|
| Entry | Any invocation |
| Exit | B1-B9 complete; orientation declared |
| Produces | session id, ledger BEGIN |
| Blocking condition | **Staleness at B4** |

## Phase 2 - Context Loading

| | |
|---|---|
| Entry | Orientation declared |
| Exit | Required tiers loaded and declared |
| Produces | tier declaration |
| Blocking condition | **Tier budget exceeded** |

## Phase 11 - Session End

| | |
|---|---|
| Entry | Any session termination |
| Exit | Entry written, HEAD updated, STATE written, lock released |
| Produces | STATE, session summary, ledger COMMIT |
| Blocking condition | **Cannot be skipped** |

## Session transaction

| Database concept | Framework equivalent |
|---|---|
| BEGIN | Boot B1-B9; ledger BEGIN entry |
| COMMIT | Entry written, HEAD updated, STATE written, lock released - in that order |
| ROLLBACK | Session abandoned: STATE unchanged, no ledger entry, repository consistent |

**An abandoned session leaves the repository exactly as it found it.**
