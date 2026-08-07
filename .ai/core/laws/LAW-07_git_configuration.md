# LAW-07 - Git and Configuration Control

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-07` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `repository-engineer` |
| Mutability | immutable |

---

## Rule

> **Author identity is never modified and no attribution trailer is ever added.**

## Clauses

1. No AI attribution in any commit, tag, file or document.
2. No co-author trailers.
3. Git author and committer identity are never modified.
4. Published history is never rewritten.
5. Tags are annotated and never moved.

## Enforcement

| | |
|---|---|
| Machine-checkable | full |
| Bound checks | V-21 |
| Binding on | repository-engineer |
| Owner | `repository-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
