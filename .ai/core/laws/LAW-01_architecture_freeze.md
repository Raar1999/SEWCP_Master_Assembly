# LAW-01 - Architecture Freeze

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-01` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |

---

## Rule

> **A frozen artifact is changed only by an approved ECR and a recorded human approval.**

## Clauses

1. Every frozen artifact is registered with a normalised SHA-256 content hash.
2. Freeze extends to the framework core partition, verified at boot step B2a.
3. A freeze violation is a build failure, never a warning.
4. Thaw requires an approved ECR and a human approval artifact.
5. Hash registry is updated atomically with any approved change.

## Enforcement

| | |
|---|---|
| Machine-checkable | full |
| Bound checks | V-12, V-21 |
| Binding on | all |
| Owner | `chief-systems-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
