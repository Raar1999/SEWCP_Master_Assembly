# LAW-10 - Human Approval

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-10` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |

---

## Rule

> **Approval is an artifact bound to a content hash, never a remembered assent.**

## Clauses

1. An approval that does not name what it approved is void.
2. An approval is invalidated automatically when the bound content hash changes.
3. Freeze and thaw are human authority only.
4. A verbal override must be recorded before dependent work is committed.

## Enforcement

| | |
|---|---|
| Machine-checkable | full |
| Bound checks | V-06 |
| Binding on | chief-systems-engineer, human-owner |
| Owner | `chief-systems-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
