# LAW-03 - Release Gates

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-03` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `project-manager` |
| Mutability | immutable |

---

## Rule

> **A gate produces pass or fail. Substantially complete is not a disposition.**

## Clauses

1. Gate criteria are binary and evidence-based.
2. A gate is declared terminal or recurring; disposition semantics are identical for both.
3. Pass with actions is permitted only when no action is on the critical path.
4. A gate may not be passed by deferral.
5. Gate disposition is recorded before dependent work begins.

## Enforcement

| | |
|---|---|
| Machine-checkable | partial |
| Bound checks | V-19 |
| Binding on | project-manager, chief-systems-engineer |
| Owner | `project-manager` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
