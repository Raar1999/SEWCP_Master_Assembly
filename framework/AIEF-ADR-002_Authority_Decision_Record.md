# AIEF-ADR-002 — Authority Decision Record

**Instrument:** Architecture Authority action under LAW-02 (ECR-D disposition)
**Exercised by:** Chief Systems Engineer (A4)
**Date:** 2026-08-07
**Scope:** CMP-BLOCK-014, plus one separately directed action
**Precedence rank exercised:** 4 — no rank-1, -2 or -3 authority invoked

---

## 1 · Decisions

| # | Decision | Closes | Instrument |
|---|---|---|---|
| D-06 | `LAW-11.depends_on` reduced to `["laws-index"]`; citation preserved as a `references` edge | **CMP-BLOCK-014** | AMD-06 |
| D-07 | Edge-type semantics ruled: only `depends_on` and `emits` constrain build order | recurrence prevention | AMD-07 |
| D-08 | `ENGINEERING.md` placed at repository root, outside `.ai/` | directed action | AMD-08 |

## 2 · Rationale — Direction of the Retained Edge

Removing a cycle requires choosing which direction survives. The choice was not arbitrary.

Laws are **rank-4 authority** and foundational; the agent contract derives from them. In the manifest, all twelve sibling laws depend only on `laws-index` and, where applicable, other laws or `precedence`. **None depends on an agent artifact.** `LAW-11` was the sole outlier.

Retaining `agent-contract → LAW-11` and dropping `LAW-11 → agent-contract` therefore restores consistency with every other law rather than introducing a special case. The build order that results — laws first, then the contract that cites them — matches the authority hierarchy.

## 3 · Semantic Preservation

The user instruction required that all semantic relationships and documentation links be preserved. Verified:

| Relationship | Before | After |
|---|---|---|
| `agent-contract` cites LAW-11 | `references` edge | **unchanged** |
| LAW-11 cites `agent-contract` | *(only as a build dependency)* | **`references` edge added** |
| `LAW-11.referenced_by` | `[]` | `["agent-contract"]` |
| Rendered file cross-links | resolve | **unchanged — not regenerated** |

**No documentation link was lost.** The bidirectional citation now exists as two `references` edges, which AMD-07 explicitly permits to be cyclic.

## 4 · Constraints Observed

| Constraint | Compliance |
|---|---|
| Resolve only CMP-BLOCK-014 | Two data edits to one file; one clarifying ruling |
| Do not change laws | 13 laws unchanged in id, title, rule and clauses |
| Do not change roles | 5 universal + 8 profile contracts unchanged |
| Do not change workflows | 6 workflows, 12 phases unchanged |
| Do not change stages | `generation_order` unchanged, 6 stages |
| Do not change ownership | All 105 `owner_role` values unchanged |
| Do not modify emitted Stage 1 artifacts | **58 artifacts untouched; no regeneration performed** |
| Schema change only if required | **Not required.** JSON Schema cannot express acyclicity; V-02 enforces it |

## 5 · Verification

**V-02 executed in isolation, as directed. No other check run.**

| Assertion | Result |
|---|---|
| All edge targets resolve | **PASS** |
| Build-order graph acyclic — 130 edges, 0 cycles | **PASS** |
| Topological sort succeeds — 105 nodes ordered | **PASS** |
| LAW-11 ↔ agent-contract preserved bidirectionally as `references` | **PASS** |
| files 105 · laws 13 · universal agents 5 · stages 6 | unchanged |
| **V-02** | **PASS** |

## 6 · Process Finding

The defect reached the compiler because the CSE pre-handoff check in AIEF-ADR-001 §6 verified **MI-1, MI-3, MI-4, MI-5, MI-8 and MI-9 — but not MI-2.**

V-02 found it exactly where it should have, and the compiler correctly refused to self-amend. The two-party separation held: the compiler detected, the architecture authority corrected.

**Recorded for 1.1:** the pre-handoff check should assert the full invariant set MI-1…MI-12, not a subset. This is a process improvement, not a framework defect, and does not block Release 1.0.

## 7 · `ENGINEERING.md` — Decision Basis

The requirement *"shall remain valid regardless of future framework upgrades"* was decisive and eliminated every location inside `.ai/`:

- `.ai/` root, `core/` and `profiles/` are all **replaced-wholesale** on upgrade — the file would be destroyed on the first upgrade.
- It would additionally be an undeclared file in an integrity-verified partition, failing **V-03a** and **V-12**.

Repository root sits outside every framework partition, so upgrade durability is guaranteed **by construction** rather than by policy. The manifest is not amended: `framework.manifest.json` governs `.ai/**`, and `ENGINEERING.md` is a project artifact.

The file is explicitly declared **not an authority** in its own opening paragraph, satisfying the no-duplicated-authority requirement.

## 8 · Artifacts Produced

| Artifact | Path |
|---|---|
| Architecture amendment | `framework/AIEF-AMD-002_Architecture_Amendments_CMP-BLOCK-014.md` |
| Updated manifest | `framework/framework.manifest.json` (2 edits) |
| Manifest schema | **unchanged** |
| Authority decision record | `framework/AIEF-ADR-002_Authority_Decision_Record.md` |
| Canonical entry point | `ENGINEERING.md` (repository root) |

## 9 · Residual Risk

The independence waiver at AIEF-FRZ-001 §6.2 remains open and is **not** discharged. CDR Condition 3 has still not been performed, and this decision record was authored by the same authority that authored the architecture it amends. **Four consecutive artifacts now carry this exposure.**

## 10 · Handoff

CMP-BLOCK-014 is closed. V-02 passes. **The repository returns to the Framework Compiler for a full Stage 1 QA re-run.** Stage 2 is not authorised until that suite passes.

---

**END OF AIEF-ADR-002**
