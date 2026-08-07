# ADP-generic-llm - Fallback Host Binding

> **Generated artifact.** Emitted by aief-compile Stage 4 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `adp-generic-llm` |
| Layer / partition | L5 / adapters |
| Owner | `chief-systems-engineer` |
| Upgrade | merged additively; never replaces project data |

---

## Host capability declaration

| Capability | Value |
|---|---|
| `host` | Any LLM |
| `file_read` | human-mediated |
| `file_write` | human-mediated |
| `subagents` | no |
| `tool_calling` | no |
| `ci` | no |
| `boot_entry` | paste BOOT.md |

## Minimum viable protocol

For any model with no file access. The human is the I/O channel.

| Step | Human | Model |
|---|---|---|
| 1 | Paste `ENGINEERING.md` | Orient |
| 2 | Paste `.ai/BOOT.md` | Execute B1-B9 conceptually |
| 3 | Paste `project/STATE.md`, `BINDING.md`, `ledger/HEAD`, `OPEN_ITEMS.md` | Reconcile B4; declare orientation |
| 4 | Assign a role; paste that agent contract | Load T2; acknowledge contract |
| 5 | Paste the task package and cited artifacts | Execute within contract |
| 6 | Commit the model's output; run git operations | Produce artifacts as text |

## What is preserved

Every law, every contract, every stop condition, the precedence hierarchy and the audit trail. **Only automation is lost.**

## What the human must do

Perform all file writes and all git operations. `repository-engineer` autonomy is not available on a host with no file access; the human executes that contract manually and remains bound by its forbidden actions.
