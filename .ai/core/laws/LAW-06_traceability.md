# LAW-06 - Traceability

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-06` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `documentation-engineer` |
| Mutability | immutable |

---

## Rule

> **Every artifact cites its authority; every requirement maps to a verification.**

## Clauses

1. No orphan artifacts are permitted.
2. Every relative reference must resolve.
3. Requirement to verification coverage is reported at every gate.
4. Authority chains must be unbroken to a frozen source.

## Enforcement

| | |
|---|---|
| Machine-checkable | full |
| Bound checks | V-03 |
| Binding on | documentation-engineer, all |
| Owner | `documentation-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
