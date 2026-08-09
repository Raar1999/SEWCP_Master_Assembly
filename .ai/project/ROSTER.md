# Project Roster

> **Instance artifact.** Emitted by aief-compile Stage 3 from `framework.manifest.json` and live repository state.
> Partition `project` — never touched by framework upgrade. Owner `project-manager`. Mutability mutable.

---

Roles enabled for this project. Registry: `core/agents/INDEX.md`. Contracts are canonical there; this file assigns only.

## Universal

| Role | Authority | Assigned identity |
|---|---|---|
| `repository-engineer` | A1 | Raar1999 <91361865+Raar1999@users.noreply.github.com> |
| `documentation-engineer` | A1 | Raar1999 <91361865+Raar1999@users.noreply.github.com> |
| `qa-engineer` | A2 | UNASSIGNED |
| `project-manager` | A3 | UNASSIGNED |
| `chief-systems-engineer` | A4 | UNASSIGNED |

## Profile `mechanical`

| Role | Authority | Assigned identity |
|---|---|---|
| `mechanical.design-engineer` | A1 | UNASSIGNED |
| `mechanical.cad-engineer` | A1 | UNASSIGNED |
| `mechanical.manufacturing-engineer` | A1 | UNASSIGNED |
| `mechanical.simulation-engineer` | A1 | UNASSIGNED |

## Profile `software` — roles enabled by AIEF-AMD-011

Enabled additively by `AIEF-AMD-011` (approval `APR-008`); `active_profile` remains `mechanical`. Contracts: `core/profiles/software/agents/AGT-*.md`.

| Role | Authority | Assigned identity | Assigned workstream |
|---|---|---|---|
| `software.software-engineer` | A1 | Raar1999 <91361865+Raar1999@users.noreply.github.com> | CMP-BLOCK-004 — deterministic Stage 6 compiler increment per AIEF-AMD-010 |
| `software.test-engineer` | A1 | Raar1999 <91361865+Raar1999@users.noreply.github.com> | Independent verification implementation and test certification |
| `software.platform-engineer` | A1 | Raar1999 <91361865+Raar1999@users.noreply.github.com> | CMP-BLOCK-005 Stage 6 slice — tokenizer/platform infrastructure |

Assigned 2026-08-08 by rank-1 live human-owner instruction (session `S-2026-08-08-03`), recorded by `project-manager` action at that direction. Human identity is canonical per OD-8; agent identity for independence tests is the (role, session) pair per AIEF-AMD-008 §AMD-20 — each dispatch carries its own session id. **LAW-05 / contract constraint, restated at assignment:** `software.test-engineer` may not test or certify code authored by its own (role, session) identity; certification of the software-engineer's and platform-engineer's output must come from a distinct cold test-engineer session.

## Separation of duties

Human identity is canonical per AIEF-FRZ-001 section 1.9 (OD-8). Reviewer independence is checked against these identities.

> **A role marked UNASSIGNED cannot be dispatched.** Assignment is a `project-manager` action.
