# AIEF-AMD-006 — Architecture Amendment: Mechanical CAD Engineer

**Amendment reference:** AMD-014 *(external instruction identifier; recorded here as AMD-14)*
**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-02
**Scope:** Mechanical profile composition only
**Date:** 2026-08-07
**Amends:** `framework/framework.manifest.json`
**Does not amend:** AIEF-FRZ-001 · AMD-001 … AMD-005 · `SCH-framework-manifest.schema.json` · the five universal agents

---

## AMD-14 — Mechanical CAD Engineer Added as a Profile Agent

**Change class:** additive profile composition

### Role

| Field | Value |
|---|---|
| Role id | `mechanical.cad-engineer` |
| Name | Mechanical CAD Engineer |
| Authority | **A1** |
| Scope | **Profile — `mechanical` only. Not a universal agent.** |
| Capability tags | cad, parametric, fusion360, drawings, export |
| Artifact | `core/profiles/mechanical/agents/AGT-cad-engineer.md` |

### Responsibilities

Fusion 360 implementation of released designs · parametric modelling driven by the parameter master · feature timeline discipline and rebuild integrity · component hierarchy and naming · assembly construction, joints and mates · drawing creation from released models · parameter set custody and synchronisation · neutral geometry export (STEP, STL) · CAD standards conformance.

### The governing constraint

> **CAD implementation only. Engineering decisions remain with `mechanical.design-engineer`.**

This separation is the whole point of the role, and it is enforced by the forbidden list rather than by convention:

| Forbidden |
|---|
| Make any engineering decision — that authority belongs to `mechanical.design-engineer` |
| Change any dimension, tolerance or fit |
| Select or substitute a material or finish |
| Invent an interface or feature not in the implementation package |
| Resolve a specification or package ambiguity by assumption |
| Model past a defect |
| **Hardcode a dimension that the parameter master declares** |
| Author or amend the implementation package it implements |

Two duty conflicts are declared: it may not make engineering decisions, and it may not author the package it implements.

### Escalation

Any engineering decision → `mechanical.design-engineer`. Package ambiguity → ECR-Q. Geometric impossibility or contradiction → **STOP**, ECR-D, human. Missing dimension or undeclared parameter → ECR-D. Timeline corruption unrepairable without a dimensional change → `mechanical.design-engineer`.

### Why this separation matters

The SEWCP Cooling Plate CAD package found four blocking specification defects precisely because the implementing role refused to resolve ambiguity by assumption. Splitting *design authority* from *CAD execution* makes that behaviour structural: an agent that cannot change a dimension has no way to paper over a defect, so the defect surfaces.

The `Hardcode a dimension that the parameter master declares` prohibition is the CAD-specific expression of the same principle — a hardcoded value is a silent fork of the parameter master.

---

## Filename Convention — Deviation From the Literal Instruction

The instruction specified `AGT-mechanical-cad-engineer.md`. **The emitted filename is `AGT-cad-engineer.md`.**

| Reason | |
|---|---|
| Sibling consistency | The three existing agents in the same directory are `AGT-design-engineer.md`, `AGT-manufacturing-engineer.md`, `AGT-simulation-engineer.md` — none carries a `mechanical-` prefix |
| Path already namespaces it | The directory is `core/profiles/**mechanical**/agents/`; the prefix would duplicate it |
| Role id carries the namespace | `mechanical.cad-engineer` is fully qualified regardless of filename |
| Compiler purity | The literal name would require a special case in the deterministic renderer. Special cases in a compiler are how drift begins |

If the literal filename is required, it is a one-line change to the manifest `path` field and a re-render. **Flagged rather than silently chosen.**

---

## Blast Radius

Determined by **full re-render and byte comparison**, not inspection.

| Result | Count |
|---|---|
| Stage 1 artifacts declared after amendment | 59 |
| **Unchanged** | **56** |
| **Changed** | **2** |
| **New** | **1** |

| Artifact | Cause | Method |
|---|---|---|
| `core/profiles/mechanical/agents/AGT-cad-engineer.md` | **NEW** — the role contract | Rendered from manifest |
| `core/profiles/mechanical/PROFILE.md` | Agent list 3 → 4; file count 15 → 16 | Rendered from manifest |
| `core/agents/INDEX.md` | Profile registry section and duty-conflict list | Rendered from manifest |
| `project/BINDING.md` | `enabled_agents` gains the role | Surgical edit — instance artifact |
| `project/ROSTER.md` | Profile roster gains the role | Surgical edit — instance artifact |

**All three `core/` artifacts were rendered from the amended manifest, never hand-edited.** A full Stage 1 re-render still reproduces the live tree byte-for-byte.

**The five universal agents are untouched.** `core/agents/AGT-*.md` — zero drift. The universal registry remains frozen at five for MAJOR version 1.

---

## Discipline Leakage Check

| Check | Result |
|---|---|
| New role scoped to `["mechanical"]` only | ✅ profile-scoped |
| New role absent from `agents.universal` | ✅ universal count still 5 |
| No discipline capability tag on any universal role | ✅ MI-8 holds |
| CAD artifact confined to `core/profiles/mechanical/` | ✅ nothing added to universal `core/` |
| `software` and `research` profiles unaffected | ✅ agent sets unchanged |

**A `software` or `research` installation receives no CAD role.** The zero-dead-file guarantee from ECR F-01 is preserved.

---

## Manifest Changes

| Section | Change |
|---|---|
| `agents.profile` | +1 contract, 12 fields, conforms to `SCH-agent` |
| `profiles[mechanical].agents` | 3 → 4 |
| `profiles[mechanical].file_count` | 15 → 16 |
| `files[]` | +1 record `mech-agt-cad`, generator 1, profile-scoped |

Manifest file inventory: 105 → 106. Universal agents: unchanged at 5. Laws, workflows, schemas, stages, ownership: unchanged.

---

**END OF AIEF-AMD-006**
