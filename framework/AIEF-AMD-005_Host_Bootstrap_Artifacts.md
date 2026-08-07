# AIEF-AMD-005 — Architecture Amendment: Host Bootstrap Artifacts

**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-02
**Scope:** Host hook placement only
**Date:** 2026-08-07
**Amends:** nothing. This amendment applies an existing precedent to a new artifact class.

---

## AMD-13 — Host Bootstrap Hooks Are Root-Level Project Artifacts

### Problem

Stage 4 must deliver the workflow *"user opens Claude Code → `ENGINEERING.md` is loaded automatically."*

Claude Code auto-loads **`CLAUDE.md`** from the repository root. It does not auto-load `ENGINEERING.md`. Without a host hook the chain never starts and the stated requirement cannot be met.

`CLAUDE.md` is not a record in `framework.manifest.json`, which raised an apparent conflict with the standing rule *"no undeclared artifacts."*

### Ruling

> **Host bootstrap hooks are root-level project artifacts, outside `.ai/` and outside manifest governance — exactly as `ENGINEERING.md` is under AMD-08.**
>
> - The **adapter** (`.ai/adapters/ADP-<host>.md`) is the manifest-declared *specification* of the binding.
> - The **hook** (`CLAUDE.md`, `AGENTS.md`, …) is the *installation* of that binding at the host's discovery path.

### Rationale

`framework.manifest.json` governs `.ai/**`. AMD-08 already established that a root-level artifact serving as an entry point sits outside that governance, and placed `ENGINEERING.md` accordingly for a reason that applies identically here: every partition inside `.ai/` except `project` is **replaced wholesale on upgrade**. A host hook placed in `.ai/` would be destroyed by the first framework upgrade — and a hook that vanishes on upgrade is worse than no hook, because the failure is silent.

The repository root is covered by no partition, so hook durability is guaranteed **by construction**, not by policy.

### Constraints on a hook

| Constraint | Reason |
|---|---|
| Carries **no authority** | It is a discovery mechanism, not a source |
| Duplicates **no content** | Points only; laws, precedence and contracts stay canonical |
| Minimal | It is loaded into every session; token cost is permanent |
| Declares itself non-authoritative | Where it conflicts with a canonical artifact, the artifact governs |

### Installed at Stage 4

| Host | Hook | Status |
|---|---|---|
| Claude Code | `CLAUDE.md` | **Installed** — active host per `project/BINDING.md` |
| ChatGPT / Codex | `AGENTS.md` | Specified in `ADP-chatgpt.md`, **not installed** — install when `host_adapter: chatgpt` |
| Generic LLM | none | Paste-boot; no discovery mechanism exists |
| CI | none | Reads the validation manifest directly |

Only the **active** host's hook is installed. An inactive hook is a dead file, which is the condition ECR F-01 exists to prevent.

### Side effect

`project/BINDING.md` field `host_adapter` moves from `PENDING-STAGE-4` to `claude-code`. This is Stage 4 populating a field the manifest already declared, not a schema change.

---

## Artifacts Not Modified

`AIEF-FRZ-001` · `AMD-001` … `AMD-004` · `framework.manifest.json` · `SCH-framework-manifest.schema.json` · all 58 Stage 1 artifacts · 7 of 8 Stage 3 artifacts · 13 laws · 5 universal roles.

**No manifest change was required.**

---

**END OF AIEF-AMD-005**
