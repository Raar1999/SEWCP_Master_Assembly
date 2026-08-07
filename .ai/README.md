# AIEF - AI Engineering Framework

Version 1.0.0. Repository-driven, model-agnostic operating system for AI-assisted engineering projects.

> **This file is for humans. Agents never read it.** Agents enter at `BOOT.md`.

## What this is

A repository-resident operating system for AI-assisted engineering. It exists so that engineering work survives the end of a conversation: state lives in the repository, not in a model's memory, and any session on any model can resume by reading files.

## Layout

```
.ai/
  BOOT.md            entry point - agents start here
  FRAMEWORK.md       identity, version, partitions
  README.md          this file
  core/              framework - read-only, replaced wholesale on upgrade
    laws/            13 engineering laws
    agents/          5 universal role contracts
    workflows/       6 workflows covering 12 phases
    schemas/         8 artifact schemas
    profiles/        discipline profiles - only the selected one is installed
  project/           instance data - never touched by upgrade (Stage 3)
  adapters/          host bindings (Stage 4)
```

## Principles

| | |
|---|---|
| Repository is truth | No decision exists unless it is a committed file |
| Memory is never trusted | Every session boots cold from disk |
| Every session is restartable | Session is a transaction; abandonment rolls back cleanly |
| AI assists, never replaces | AI inference is the lowest precedence rank |

## Do not

Edit anything under `core/`. It is integrity-verified at boot and replaced on upgrade.
Changes are made by amending the manifest and recompiling.
