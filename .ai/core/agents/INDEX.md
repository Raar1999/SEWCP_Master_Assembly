# Agent Registry - Index

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `agents-index` |
| Layer / partition | L1 / core |
| Tier | T2 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |

---

Universal registry is **frozen at five roles** for MAJOR version 1. Profile roles are namespaced by profile id.

## Universal

| Role | Authority | Capabilities |
|---|---|---|
| `repository-engineer` | A1 | vcs, release, structure, ci |
| `documentation-engineer` | A1 | indexing, traceability, numbering |
| `qa-engineer` | A2 | verification, audit, evidence |
| `project-manager` | A3 | planning, gates, risk, allocation |
| `chief-systems-engineer` | A4 | authority, ecr, review, integrity |

## Profile: `mechanical`

| Role | Authority | Capabilities |
|---|---|---|
| `mechanical.design-engineer` | A1 | cad, tolerance, gdt |
| `mechanical.manufacturing-engineer` | A1 | producibility, process, inspection |
| `mechanical.simulation-engineer` | A1 | fea, thermal, correlation |

## Authority levels

| Level | Meaning |
|---|---|
| A1 | Produces artifacts within an assigned task |
| A2 | Verifies and may reject others' artifacts |
| A3 | Plans, gates and allocates; cannot verify own plan |
| A4 | Rules on ECRs and approves designs; cannot implement |
| H | Human owner; sole authority for freeze, thaw and architecture change |

## Separation of duties

- `qa-engineer`: May not audit artifacts it produced
- `project-manager`: May not gate-pass its own plan unaided
- `chief-systems-engineer`: May not implement what it approved
- `chief-systems-engineer`: May not validate schemas it authored
- `software.test-engineer`: May not test code it authored
