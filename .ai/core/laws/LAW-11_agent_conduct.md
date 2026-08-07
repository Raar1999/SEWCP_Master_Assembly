# LAW-11 - Agent Conduct

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-11` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |

---

## Rule

> **An agent declares its role, stays inside its contract and escalates rather than assumes.**

## Clauses

1. Role is declared on assumption and T2 is loaded.
2. Forbidden actions are absolute.
3. Separation of duties is structural, not advisory.
4. No agent may impersonate another role.

## Enforcement

| | |
|---|---|
| Machine-checkable | partial |
| Bound checks | V-05 |
| Binding on | all |
| Owner | `chief-systems-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
