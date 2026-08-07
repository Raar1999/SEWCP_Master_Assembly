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
3. No generated-by trailers.
4. Git author and committer identity are never modified.
5. The configured git identity is preserved and never overwritten.
6. Published history is never rewritten.
7. Tags are annotated and never moved.
8. Force push is prohibited unless explicitly authorised by the framework.
9. The repository-engineer owns all repository operations and executes the release sequence automatically once a release gate is approved.
10. After every release the repository-engineer shall verify: clean working tree, remote branch, remote tags, commit SHA, release tag target, repository synchronisation, and author equals committer equals repository owner.
11. A repository policy violation is a QA failure, never a warning.

## Enforcement

| | |
|---|---|
| Machine-checkable | full |
| Bound checks | V-21, V-22 |
| Binding on | repository-engineer |
| Owner | `repository-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
