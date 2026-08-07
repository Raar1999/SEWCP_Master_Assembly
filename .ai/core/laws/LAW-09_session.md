# LAW-09 - Session

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-09` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |

---

## Rule

> **A session is a transaction. It reads state at start and writes state at close.**

## Clauses

1. Session close writes entry, updates HEAD, writes STATE and releases the lock in that order.
2. An abandoned session leaves the repository exactly as it found it.
3. Tier discipline is mandatory; T4 loading requires cause.
4. One active session per working tree.
5. The ledger is authoritative; STATE is a derived cache.

## Enforcement

| | |
|---|---|
| Machine-checkable | partial |
| Bound checks | V-11, V-13, V-14, V-15, V-17 |
| Binding on | all |
| Owner | `chief-systems-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
