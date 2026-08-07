# Lifecycle - Mechanical Engineering

> **Generated artifact.** Emitted by aief-compile Stage 1 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `mech-lc-index` |
| Layer / partition | L3 / profile |
| Tier | T1 |
| Owner | `project-manager` |
| Mutability | immutable |

---

Ten stages. Gate topology: **terminal**.

| Stage | Name | Gate | File |
|---|---|---|---|
| LC-M01 | Idea | terminal | `LC-M01_idea.md` |
| LC-M02 | Architecture | terminal | `LC-M02_architecture.md` |
| LC-M03 | Specification | terminal | `LC-M03_specification.md` |
| LC-M04 | Implementation | terminal | `LC-M04_implementation.md` |
| LC-M05 | Verification | terminal | `LC-M05_verification.md` |
| LC-M06 | Validation | terminal | `LC-M06_validation.md` |
| LC-M07 | Release | terminal | `LC-M07_release.md` |
| LC-M08 | Maintenance | terminal | `LC-M08_maintenance.md` |
| LC-M09 | Revision | terminal | `LC-M09_revision.md` |
| LC-M10 | Archive | terminal | `LC-M10_archive.md` |

## Transition rules

- **Forward** only via a passed gate recorded in `project/GATES.md`.
- **Backward** only via a human approval artifact; the ledger records the regression and its cause.
- **Skip** prohibited without human approval. Verification can never be skipped.
- **Terminal** stage is absorbing; exiting requires creating a new project.

Gate disposition is binary (LAW-03). Substantially complete is not a disposition.
