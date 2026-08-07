# Context Tiers

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `context-tiers` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |
| Content source | AIEF-FRZ-001 section 2.5 (frozen) |

---

Loading everything is the default failure. Tiers bound the cost of becoming oriented.

| Tier | Trigger | Budget |
|---|---|---|
| T0 | Always, first action | 400 tok |
| T1 | Always | 5,400 tok |
| T2 | Role assignment | 2,500 tok |
| T3 | Task acceptance | 6,000 tok |
| T4 | Explicit request only | unbounded |

**T0 + T1 ceiling: 6000 tokens**, enforced per-file and in aggregate.

## Per-file caps

| File | Tier | Cap |
|---|---|---|
| `BOOT.md` | T0 | 400 |
| `FRAMEWORK.md` | T1 | 1100 |
| `core/MANIFEST.lock` | T1 | 200 |
| `core/PRECEDENCE.md` | T1 | 700 |
| `core/laws/INDEX.md` | T1 | 900 |
| `project/BINDING.md` | T1 | 800 |
| `project/STATE.md` | T1 | 1100 |
| `project/OPEN_ITEMS.md` | T1 | 600 |
| **Sum** | | **5800** |

Headroom against ceiling: **200 tokens**.

## Discipline

Loading T4 without cause burns the budget verification needs. Tier discipline is enforced by LAW-09.
