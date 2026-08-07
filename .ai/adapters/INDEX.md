# Adapters - Index

> **Generated artifact.** Emitted by aief-compile Stage 4 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `adapters-index` |
| Layer / partition | L5 / adapters |
| Owner | `chief-systems-engineer` |
| Upgrade | merged additively; never replaces project data |

---

An adapter maps AIEF concepts onto one host. The core is portable; only adapters change.

## Registry

| Adapter | Host | Subagents | Boot entry |
|---|---|---|---|
| `ADP-claude-code` | Claude Code | yes | CLAUDE.md (auto-loaded at repository root) |
| `ADP-chatgpt` | ChatGPT / Codex | no | AGENTS.md (repository root) |
| `ADP-generic-llm` | Any LLM | no | paste BOOT.md |
| `ADP-ci` | CI runner (no model) | n/a | core/validation/MANIFEST |

## Capability matrix

| Capability | claude-code | chatgpt | generic-llm | ci |
|---|---|---|---|---|
| `file_read` | yes | yes | human-mediated | yes |
| `file_write` | yes | yes | human-mediated | no |
| `subagents` | yes | no | no | n/a |
| `tool_calling` | yes | yes | no | n/a |
| `ci` | yes | no | no | yes |
| `boot_entry` | CLAUDE.md (auto-loaded at repository root) | AGENTS.md (repository root) | paste BOOT.md | core/validation/MANIFEST |

## Degradation ladder

Ceremony degrades with host capability. **Discipline never does.**

| Host capability | Adaptation | Discipline |
|---|---|---|
| Subagents + tools + CI | Parallel agents, automated gates, CI enforcement | Full |
| Tools, no subagents | Serial role adoption with declared switches; QA runs as a separate cold session | **Full** - independence via context, not process |
| Chat only | Human mediates file I/O; boot by paste | Full, with human in the loop |
| No CI | Validation run manually at gates; results recorded as evidence | Full, more slowly |

## Active host

Declared in `project/BINDING.md` field `host_adapter`.
