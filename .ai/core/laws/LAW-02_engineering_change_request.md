# LAW-02 - Engineering Change Request

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-02` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |

---

## Rule

> **Ambiguity is raised as ECR-Q; a defect is raised as ECR-D and stops the affected work.**

## Clauses

1. ECR-Q is a specification query; work proceeds under the ruling.
2. ECR-D is a specification defect; affected work stops immediately.
3. Only the chief-systems-engineer rules on ECR-Q.
4. ECR-D disposition requires human involvement and re-gating.
5. No ECR may be closed by the agent that raised it.

## Enforcement

| | |
|---|---|
| Machine-checkable | partial |
| Bound checks | V-06 |
| Binding on | all |
| Owner | `chief-systems-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
