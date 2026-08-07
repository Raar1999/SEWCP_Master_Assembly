# LAW-12 - Ambiguity and Stop Conditions

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-12` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |

---

## Rule

> **Assumption is never a resolution method. Producing Open Questions and stopping is a compliant deliverable.**

## Clauses

1. Findings are classified as clarification, ambiguity or defect.
2. A clarification is logged and work proceeds.
3. An ambiguity raises ECR-Q.
4. A defect stops the affected work and raises ECR-D.
5. An Open Questions section is required whenever any finding is open.

## Enforcement

| | |
|---|---|
| Machine-checkable | partial |
| Bound checks | V-16 |
| Binding on | all |
| Owner | `chief-systems-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
