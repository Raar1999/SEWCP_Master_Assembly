# AIEF-AMD-007 — Architecture Amendment: `compiler_stage` State Field

**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-02
**Scope:** `SCH-state` and `tpl-current-state` only
**Date:** 2026-08-07
**Origin:** Cold-start acceptance test finding
**Amends:** `framework/framework.manifest.json`

---

## AMD-15 — Compiler Stage Becomes a Declared State Field

### Finding

The cold-start acceptance test recovered every required fact from repository artifacts **except compiler stage completion**, which was obtainable only by inspecting the filesystem for the presence or absence of `core/templates/`, `core/validation/` and `core/MANIFEST.lock`.

**That is inference, and inference is precisely what this framework exists to eliminate.** A fact recoverable only by deduction is a fact that a future session can deduce wrongly.

The gap was masked because `ENGINEERING.md` §6 carried a stage table — but that file is explicitly non-authoritative, and it had gone stale: it reported Stage 4 as *not started* two releases after Stage 4 completed.

### Does the architecture permit the change?

| Question | Answer |
|---|---|
| Is `SCH-state` manifest-declared? | Yes — `schemas[sch-state]` |
| Does adding a required field touch a law, role, workflow, stage or partition? | **No** |
| Change class under AIEF-FRZ-001 §13.1 | **Additive — MINOR** |
| Precedent | AMD-001 and AMD-004 established additive manifest amendment |

**Permitted. An ECR deferral was therefore not raised** — the instruction's fallback was unnecessary.

### Ruling

> **`compiler_stage` is added to `SCH-state.required_fields` and to `tpl-current-state.required_sections`.**

It is a structured field declaring three things explicitly:

```yaml
compiler_stage:
  next:           2           # Generate Templates
  complete:       [1, 3, 4]   # Core, Project Layer, Adapters
  outstanding:    [2, 5, 6]   # Templates, Validation, Release
```

A new acceptance condition is added to `tpl-current-state`:

> *"Compiler stage declares complete and outstanding stages explicitly, never by inference."*

Because the field is **required**, a future `STATE.md` that omits it fails schema validation. The gap cannot silently reopen.

---

## Blast Radius

Determined by full re-render and byte comparison.

| Result | Count |
|---|---|
| Stage 1 artifacts declared | 59 |
| **Unchanged** | **58** |
| **Changed** | **1** |

| Artifact | Cause | Method |
|---|---|---|
| `core/schemas/SCH-state.schema.json` | `required[]` and `properties{}` gain `compiler_stage` | Rendered from manifest |
| `project/STATE.md` | Field populated | Surgical — instance artifact |
| `ENGINEERING.md` | Stale sections synchronised | Surgical — project artifact |

`core/schemas/INDEX.md` renders only id, target, severity and owner — unaffected. `core/templates/TPL-current-state.md` is a Stage 2 artifact and is not yet emitted; it will carry the new section when Stage 2 runs.

**No law, role, workflow, stage, partition or ownership assignment was modified. The five universal agents are untouched.**

---

## Repository State Synchronisation

`ENGINEERING.md` had drifted from the repository across two releases, in violation of its own maintenance rule (*"Update trigger: compiler stage change"*). Corrected:

| Section | Was | Now |
|---|---|---|
| §1 release | v0.1.0 | **v0.6.0**; host adapter added |
| §5 framework docs | AMD-001, AMD-002 | **all seven amendments** |
| §6 stages | Stage 4 *not started* | **1, 3, 4 complete; 2, 5, 6 outstanding**; points at `STATE.compiler_stage` as authoritative |
| §7 status | "amended twice", "uncommitted" | seven amendments; **v0.6.0 pushed, tree clean**; agent counts added |
| §8 next activity | listed Stage 4 as pending | Stage 2, with the gate caveat stated |

> **Root cause is structural, not clerical.** `ENGINEERING.md` restated a fact that had no authoritative home. Now that `compiler_stage` is declared in `STATE.md`, §6 is a pointer rather than a second copy — the class of drift is closed, not merely the instance.

---

**END OF AIEF-AMD-007**
