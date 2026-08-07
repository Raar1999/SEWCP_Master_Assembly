# LAW-05 - Verification and Reproducibility

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `LAW-05` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `qa-engineer` |
| Mutability | immutable |

---

## Rule

> **No agent may verify an artifact it produced. Every claim cites evidence independent of itself.**

## Clauses

1. Verification produces binary pass or fail per criterion.
2. Self-verification is invalid regardless of rigour.
3. Every output declares its inputs, framework version and authority chain.
4. A claim in a document is not evidence for itself.

## Enforcement

| | |
|---|---|
| Machine-checkable | full |
| Bound checks | V-05, V-10 |
| Binding on | qa-engineer, all |
| Owner | `qa-engineer` |

## Violation

A violation of a BLOCKING check is a build failure, never a warning. An agent detecting a violation escalates per `agents/AGENT-CONTRACT.md`.
