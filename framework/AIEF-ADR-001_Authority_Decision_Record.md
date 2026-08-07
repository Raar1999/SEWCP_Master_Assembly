# AIEF-ADR-001 — Authority Decision Record

**Instrument:** Architecture Authority action under AIEF-FRZ-001 §2.7 and LAW-02
**Exercised by:** Chief Systems Engineer (A4)
**Date:** 2026-08-07
**Scope of authority:** CMP-BLOCK-002, CMP-BLOCK-011, CMP-BLOCK-012 — architecture-owned blockers only
**Precedence rank exercised:** 4 (engineering law) — no rank-1, -2 or -3 authority was invoked

---

## 1. Decisions Taken

| # | Decision | Closes | Instrument |
|---|---|---|---|
| D-01 | Universal registry confirmed final at five roles; not extended | prerequisite | AMD-01 |
| D-02 | Eleven orphaned universal files reassigned; all 105 files given a resolvable owner | **CMP-BLOCK-012** | AMD-02 |
| D-03 | Three profile compositions defined — mechanical, software, research | **CMP-BLOCK-002** | AMD-03 |
| D-04 | Five universal role contracts restated in authoritative form | **CMP-BLOCK-011** | AMD-04 |
| D-05 | Manifest carries structured normative content; compiler renders deterministically | **CMP-BLOCK-011** | AMD-05 |

## 2. Decision Rationale — Load-Bearing Choices

**D-02 · Schemas to Chief Systems Engineer, validation registry to QA Engineer.**
Schemas are the machine-readable expression of laws, and law interpretation is A4 authority. The check registry is verification work and belongs to A2. Splitting them preserves separation of duties: the CSE authors the schemas, QA validates them under V-06, and neither validates its own artifact. Assigning both to one role would have created a self-verification path and violated LAW-05.

**D-02 · CI adapter to Repository Engineer.**
`ADP-ci` is release and repository mechanics. Assigning it to QA would have made the verifier responsible for the machinery that runs its own checks.

**D-03 · Profile roles namespaced, universal registry untouched.**
Defining `mechanical.design-engineer` is populating a slot that AIEF-FRZ-001 §1.5 already mandated, not introducing a universal role. The five-role universal registry is unchanged and remains frozen for MAJOR 1.

**D-05 · Structured content, not inline prose.**
Inline prose in the manifest would be unmaintainable and would not improve determinism. Structured clauses are compact, diffable, machine-validatable, and render identically on every execution — which is what V-10 reproducibility requires.

## 3. Constraints Observed

| Constraint | Compliance |
|---|---|
| Do not redesign architecture | No architectural mechanism altered; only mandated slots populated |
| Do not reopen CDR | No CDR finding revisited; no score adjusted |
| Do not introduce new roles | Universal registry unchanged at five. Profile roles are a frozen slot per §1.5 |
| Do not change laws | All 13 laws carried forward unchanged in rule and clause content |
| Modify frozen architecture only as required | Five amendments, each traced to exactly one architecture-owned blocker |

## 4. Blockers Not Within This Authority

| Blocker | Status | Reason |
|---|---|---|
| CMP-BLOCK-009 | **Closed by withdrawal** | The instruction routed work through the frozen five-role registry under A4 authority rather than through roles absent from it. No non-existent role was instantiated. |
| CMP-BLOCK-010 | **Closed by withdrawal** | Profile enumeration was reassigned from a non-existent role to A4 architecture authority, which is the correct instrument. The instruction self-conflict no longer exists. |
| CMP-BLOCK-001 | **Closed by this action** | `framework.manifest.json` now exists |
| CMP-BLOCK-003 | **Closed by D-05** | Content source established as the manifest's structured sections |
| CMP-BLOCK-004 | **Open — outside authority** | Deterministic software compiler required. Software engineering activity, not architecture. |
| CMP-BLOCK-005 | **Open — outside authority** | Tokenizer, multi-platform and runtime verification infrastructure required. |

## 5. Defect Corrected During Execution

One defect was found and corrected before handoff.

| Item | Detail |
|---|---|
| **Artifact** | `SCH-framework-manifest.schema.json` |
| **Defect** | `agentContract` referenced by `agents.universal` and `agents.profile` but never defined in `$defs`; three stray non-schema keys present |
| **Impact if shipped** | Unresolvable `$ref` — V-06 would have failed at Stage 1, halting the compiler |
| **Correction** | `agentContract` defined with twelve required fields; stray keys removed |
| **Verification** | All 13 `$ref` targets now resolve |

## 6. Pre-Handoff Verification

Mechanical syntax and invariant check executed. **Result: all pass.**

| Check | Result |
|---|---|
| Both artifacts parse as JSON | PASS |
| All schema `$ref` resolve (13) | PASS |
| 15 manifest sections present | PASS |
| files 105 ≥ 70 · laws 13 · templates 10 · schemas 8 · validation 21 · universal agents 5 · profiles 3 | PASS |
| Boot steps 11 · runtime phases 12 · compiler stages 6 | PASS |
| MI-1 unique file ids (105, 0 duplicates) | PASS |
| MI-3 all 29 edges and all `depends_on` resolve | PASS |
| MI-4 boot budget 5,800 ≤ 6,000 (headroom 200) | PASS |
| MI-5 all law-to-check references resolve | PASS |
| MI-8 zero discipline-tag leakage into universal roles | PASS |
| MI-9 all three profiles complete | PASS |
| **CMP-BLOCK-012: all 105 files have a resolvable owner, zero orphans** | **PASS** |
| Profile file counts reconcile with inventory | PASS |

**Authority limit on this verification:** LAW-05 bars the Chief Systems Engineer from validating schemas it authored. The above is a syntax and invariant sanity check performed to avoid handing a known-broken artifact to the compiler. **It is not V-01 or V-06.** Authoritative validation is the compiler's at Stage 1 and QA's under an independent context.

## 7. Artifacts Produced

| Artifact | Path |
|---|---|
| Architecture amendments | `framework/AIEF-AMD-001_Architecture_Amendments_1.0.0.md` |
| Manifest schema | `framework/SCH-framework-manifest.schema.json` |
| Framework manifest | `framework/framework.manifest.json` |
| Authority decision record | `framework/AIEF-ADR-001_Authority_Decision_Record.md` |

## 8. Residual Risk Carried Forward

The independence waiver recorded at AIEF-FRZ-001 §6.2 remains open and is **not** discharged by this action. CDR Condition 3 — independent cold-context ratification — has still not been performed. This decision record was authored by the same authority that authored the architecture it amends.

## 9. Handoff

Architecture-owned blockers are closed. The repository is handed to the **Framework Compiler** for Stage 1 pre-flight, entering at **V-01**.

**Execution-class blockers CMP-BLOCK-004 and CMP-BLOCK-005 remain open and are outside architecture authority.** They gate Stage 6 and post-build validation, not Stage 1.

---

**END OF AIEF-ADR-001**
