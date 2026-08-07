# LAW-04 - Design Review

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-04` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |

---

## Rule

> **A reviewer may never be the originator.**

## Clauses

1. Review classes are peer, checker, design authority and gate.
2. Checker identity must differ from originator identity.
3. Every review records a binary disposition.
4. Actions carry an owner and a due date.

## Enforcement

| | |
|---|---|
| Machine-checkable | full |
| Bound checks | V-05 |
| Binding on | chief-systems-engineer, qa-engineer, all |
| Owner | `chief-systems-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
