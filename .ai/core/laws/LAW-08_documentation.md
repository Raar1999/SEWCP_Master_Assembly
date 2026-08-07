# LAW-08 - Documentation

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-08` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `documentation-engineer` |
| Mutability | immutable |

---

## Rule

> **A document is released only when it has passed its gate.**

## Clauses

1. Maturity states are draft, preliminary, released and superseded.
2. Every document carries a unique number.
3. Every document is reachable from the index.
4. Released documents change only by ECN.

## Enforcement

| | |
|---|---|
| Machine-checkable | full |
| Bound checks | V-03, V-20 |
| Binding on | documentation-engineer |
| Owner | `documentation-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
