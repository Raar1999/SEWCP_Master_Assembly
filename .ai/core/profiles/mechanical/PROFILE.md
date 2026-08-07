# Profile - Mechanical Engineering

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `prof-mech` |
| Layer / partition | L3 / profile |
| Tier | T1 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |

---

| Profile id | `mechanical` |
| Discipline tags | mechanical, hardware, semiconductor, npi |
| Gate topology | **terminal** |
| Files | 15 |

## Agents

| Role | Specification |
|---|---|
| `mechanical.design-engineer` | `agents/AGT-design-engineer.md` |
| `mechanical.manufacturing-engineer` | `agents/AGT-manufacturing-engineer.md` |
| `mechanical.simulation-engineer` | `agents/AGT-simulation-engineer.md` |

## Lifecycle

| Stage | Name | Gate |
|---|---|---|
| LC-M01 | Idea | terminal |
| LC-M02 | Architecture | terminal |
| LC-M03 | Specification | terminal |
| LC-M04 | Implementation | terminal |
| LC-M05 | Verification | terminal |
| LC-M06 | Validation | terminal |
| LC-M07 | Release | terminal |
| LC-M08 | Maintenance | terminal |
| LC-M09 | Revision | terminal |
| LC-M10 | Archive | terminal |

## Freeze points

- Architecture at LC-M02 exit
- Specification at LC-M03 exit
- Design at LC-M04 exit
- Release at LC-M07

Gate criteria are project-declared in `project/GATES.md` (Stage 3, owned by `project-manager`).
