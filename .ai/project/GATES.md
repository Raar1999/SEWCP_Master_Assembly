# Project Gates

> **Instance artifact.** Emitted by aief-compile Stage 3 from `framework.manifest.json` and live repository state.
> Partition `project` — never touched by framework upgrade. Owner `project-manager`. Mutability mutable.

---

Profile `mechanical`. Gate topology **terminal**. Disposition is binary per `core/laws/LAW-03_release_gates.md`.

| Gate | Stage | Topology | Status |
|---|---|---|---|
| LC-M01-EXIT | Idea | terminal | PASSED |
| LC-M02-EXIT | Architecture | terminal | PASSED |
| LC-M03-EXIT | Specification | terminal | PASSED |
| LC-M04-EXIT | Implementation | terminal | **ACTIVE - BLOCKED** |
| LC-M05-EXIT | Verification | terminal | pending |
| LC-M06-EXIT | Validation | terminal | pending |
| LC-M07-EXIT | Release | terminal | pending |
| LC-M08-EXIT | Maintenance | terminal | pending |
| LC-M09-EXIT | Revision | terminal | pending |
| LC-M10-EXIT | Archive | terminal | pending |

## Active gate

`LC-M04-EXIT` (Implementation) is **BLOCKED** by ECR-D-001 through ECR-D-004 against the frozen specification.

A gate may pass with actions only if no action is on the critical path. All four defects are on it.

## Criteria

Gate criteria are project-declared. None recorded yet — a `project-manager` action.
