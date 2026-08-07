# ADP-chatgpt - ChatGPT / Codex Host Binding

> **Generated artifact.** Emitted by aief-compile Stage 4 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `adp-chatgpt` |
| Layer / partition | L5 / adapters |
| Owner | `repository-engineer` |
| Upgrade | merged additively; never replaces project data |

---

## Host capability declaration

| Capability | Value |
|---|---|
| `host` | ChatGPT / Codex |
| `file_read` | yes |
| `file_write` | yes |
| `subagents` | no |
| `tool_calling` | yes |
| `ci` | no |
| `boot_entry` | AGENTS.md (repository root) |

## Discovery and boot chain

The host hook is `AGENTS.md` at the repository root. It is **not installed by default** - install it when this host becomes active by setting `host_adapter: chatgpt` in `project/BINDING.md`.

```
AGENTS.md -> ENGINEERING.md -> .ai/BOOT.md -> B1..B9
```

The chain after the hook is identical to every other host. Only the hook filename differs.

## Role mapping - no subagents

This host declares `subagents: no`. Roles are adopted **serially**, and every switch is declared in writing.

> **`qa-engineer` shall run as a separate session with a cold context.** Serial adoption inside the same session does not produce independence, and LAW-05 requires it. This is the one place where a missing host capability changes procedure - ceremony degrades, discipline does not.

## Everything else

Tiers, repository operations and prohibitions are identical to `ADP-claude-code`. They are not restated here - see that adapter.
