# ADP-ci - Non-LLM CI Binding

> **Generated artifact.** Emitted by aief-compile Stage 4 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `adp-ci` |
| Layer / partition | L5 / adapters |
| Owner | `repository-engineer` |
| Upgrade | merged additively; never replaces project data |

---

## Host capability declaration

| Capability | Value |
|---|---|
| `host` | CI runner (no model) |
| `file_read` | yes |
| `file_write` | no |
| `subagents` | n/a |
| `tool_calling` | n/a |
| `ci` | yes |
| `boot_entry` | core/validation/MANIFEST |

## Purpose

Enforcement that survives the absence of any model. CI executes the validation manifest deterministically; no inference is involved.

## Execution

| Trigger | Checks | Blocking |
|---|---|---|
| Every push | Compile-time V-01 .. V-10 | yes |
| Every push | Git policy V-22 | yes |
| Gate | Runtime V-11 .. V-17 | yes |
| Release | Installation V-18 .. V-21 | yes |

All 22 checks are BLOCKING. There are no advisory checks.

## Source

`core/validation/MANIFEST` - the machine-readable check registry. **Emitted by Compiler Stage 5, not yet present.** Until Stage 5 runs, CI enforcement is unavailable and checks are executed manually at gates with results recorded as evidence.

## Prohibition

CI shall never write to the repository, never create commits, and never modify git identity. It reads and reports.
