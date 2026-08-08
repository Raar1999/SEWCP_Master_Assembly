# Output Contracts - Index

> **Generated artifact.** Emitted by aief-compile Stage 2 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `templates-index` |
| Layer / partition | L2 / core |
| Tier | none |
| Owner | `documentation-engineer` |
| Mutability | immutable |
| Content source | `manifest.templates` (10 contracts) |

---

Ten output contracts. A template declares **required sections** and **acceptance conditions**; it is a contract, not a suggestion. An artifact that omits a required section or fails an acceptance condition is **not acceptable**, irrespective of quality.

| Contract | Title | Producer | Filed at |
|---|---|---|---|
| `tpl-implementation-package` | [Implementation Package](TPL-implementation-package.md) | discipline engineer | `project/` |
| `tpl-design-review` | [Design Review](TPL-design-review.md) | reviewer | `project/reviews/` |
| `tpl-ecr` | [Engineering Change Request](TPL-engineering-change-request.md) | any agent | `project/ecr/` |
| `tpl-session-summary` | [Session Summary](TPL-session-summary.md) | session closer | `project/sessions/` |
| `tpl-verification-report` | [Verification Report](TPL-verification-report.md) | `qa-engineer` | `project/verification/` |
| `tpl-release-notes` | [Release Notes](TPL-release-notes.md) | `repository-engineer` | `project/releases/` |
| `tpl-issue-report` | [Issue Report](TPL-issue-report.md) | any agent | `project/issues/` |
| `tpl-agent-specification` | [Agent Specification](TPL-agent-specification.md) | `chief-systems-engineer` | `core/agents/` |
| `tpl-task-package` | [Task Package](TPL-task-package.md) | `project-manager` | `project/tasks/` |
| `tpl-current-state` | [Current State](TPL-current-state.md) | session closer | `project/STATE.md` |

## Stage 2 barrier - role resolution

> Stage 2 barrier: *every template producer and consumer role must resolve against Stage 1 output.* An unresolved role reference halts the build.

Manifest role references are of two kinds. **Role literals** name an entry in `core/agents/INDEX.md` directly. **Role classes** and **consumer contexts** are abstractions that resolve to a registered role, an authority level, or a declared framework mechanism. Both are resolved below; none is left dangling.

| Reference | Kind | Resolves to |
|---|---|---|
| `qa-engineer` · `project-manager` · `repository-engineer` · `chief-systems-engineer` | literal | `core/agents/INDEX.md`, universal registry |
| `human-owner` | literal | Authority level **H**, `core/agents/INDEX.md` |
| discipline engineer | class | The A1 profile roles of the active profile. Under `mechanical`: `design-engineer`, `cad-engineer`, `manufacturing-engineer`, `simulation-engineer` |
| reviewer | class | Any registered role permitted to review under `LAW-04`, constrained by *reviewer identity differs from originator identity* |
| any agent | class | Every role in the universal registry and in the active profile |
| session closer | class | The role holding the session lock at close, per `LAW-09` |
| assigned agent | class | The role named in the `Role` field of the governing task package |
| gate | context | A gate evaluation under `LAW-03`; consumes the artifact, does not author it |
| framework | context | The compiler and boot machinery; consumes the artifact as build input |
| next session · next session boot | context | Boot steps B3-B7 of the following session |

**All 10 contracts resolve. Barrier satisfied.**

## Filing rule

`filing_path` is normative. An artifact filed elsewhere is not discoverable by the boot sequence and does not exist as far as the framework is concerned.

## Precedence

A template is an **agent specification** artifact, rank 6. It is outranked by engineering laws (rank 4) and by the freeze registry (rank 3). Where a template appears to permit what a law forbids, **the law governs**.
