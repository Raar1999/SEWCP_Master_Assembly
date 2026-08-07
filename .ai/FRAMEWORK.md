# AIEF - Framework Identity

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `framework-md` |
| Layer / partition | L0 / root |
| Tier | T1 (cap 1100 tok) |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |

---

Repository-driven, model-agnostic operating system for AI-assisted engineering projects.

## Identity

| | |
|---|---|
| Framework | AI Engineering Framework (`AIEF`) |
| Version | 1.0.0 |
| Released | 2026-08-07 |
| Compatibility | `>=1.0.0 <2.0.0` |
| Min context window | 32000 tok |
| Boot ceiling | 6000 tok |
| Frozen by | Chief Systems Engineer (A4) |
| Freeze document | AIEF-FRZ-001 Framework Architecture Freeze 1.0.0 |
| Amendments | AIEF-AMD-001 Architecture Amendments 1.0.0 |

## Integrity

Hash: **SHA-256 over normalised content** (UTF-8, LF line endings, trailing whitespace stripped, terminal newline enforced).

Reproducible build required: identical manifest yields identical aggregate digest.

## Partitions

| Partition | Path | Write access | Upgrade | Integrity verified |
|---|---|---|---|---|
| `root` | `.ai/` | framework-only | replaced-wholesale | yes |
| `core` | `.ai/core/` | framework-only | replaced-wholesale | yes |
| `profile` | `.ai/core/profiles/` | framework-only | replaced-wholesale | yes |
| `project` | `.ai/project/` | agents-and-humans | never-touched | no |
| `adapters` | `.ai/adapters/` | human-only | merged-additively | no |

## Layers

| Layer | Name | Partition | Emitted by stage | Replaced on upgrade |
|---|---|---|---|---|
| L0 | Entry | `root` | 1 | yes |
| L1 | Universal Core | `core` | 1 | yes |
| L2 | Templates | `core` | 2 | yes |
| L3 | Profile | `profile` | 1 | yes |
| L4 | Instance | `project` | 3 | no |
| L5 | Adapters | `adapters` | 4 | no |
| L6 | Validation | `core` | 5 | yes |
| L7 | Release | `core` | 6 | yes |

## Upgrade rule

`core/` is replaced **wholesale**. `project/` is **never touched**. `adapters/` is merged additively.
A MAJOR version mismatch against the `project/BINDING.md` pin **halts boot**.
