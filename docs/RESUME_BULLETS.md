# Résumé Material

*Verified metrics only. No performance percentages are claimed, because none were measured. No
manufacturing or physical qualification is claimed, because none occurred.*

---

## Project title

**AIEF / SEWCP — Agent-Driven Semiconductor CAD Engineering and Verification Platform**

Shorter variants:

- *AIEF — Agent-Driven CAD Engineering Platform (SEWCP demonstration)*
- *Requirements-to-Verified-CAD Automation for Semiconductor Equipment*

## One-line description

> An agent-driven engineering pipeline that converts a governed semiconductor-equipment
> specification into parametric Fusion 360 CAD, verifies the resulting geometry against
> requirements from observed model state, and iterates through failure-recovery loops before
> producing traceable engineering deliverables.

## Technology line

`Python 3.11 · Autodesk Fusion 360 API · custom Fusion add-in (CAD bridge) · agent orchestration ·
geometry verification · parametric modelling · GD&T / drawing generation (SVG, PDF, STEP, STL) ·
SHA-256 provenance and hash-chained ledger · pytest · Git · GitHub Actions CI`

---

## Three concise bullets

- Built an agent-driven CAD engineering platform that compiles a governed semiconductor-equipment
  specification into parametric Fusion 360 geometry through a custom add-in and file-queue
  protocol, producing **10 verified part designs and a 19-occurrence master assembly** across
  **9 specified components**.

- Designed an observation-based verification layer that reads geometry, parameters and materials
  back out of Fusion and scores them against requirement-derived acceptance criteria rather than
  API return codes — **19/19 final system verification, 12/12 interfaces, 79 drawing dimensions
  with zero unsourced**, all computed from tracked evidence.

- Implemented a bounded failure-recovery loop with root-cause classification, no-blind-retry
  enforcement and save-on-verified-PASS-only document lifecycle; **36 CAD runs are tracked in the
  repository, 18 of them failures**, including one where an executing-cleanly run was rejected on
  a 173.71 mm³ volume discrepancy that traced to an infeasible specification requirement.

---

## Two stronger technical variants

**A — architecture and correctness**

> Architected and implemented AIEF, a requirements-governed CAD engineering platform for
> semiconductor equipment: a Fusion 360 add-in exposing a 32-operation vocabulary over a
> file-queue transport, three independent verifiers (geometry / interface / constraint) that read
> observed model state and never the API's own success report, and a bounded repair loop with
> digest-enforced no-blind-retry. Demonstrated on a 300 mm bipolar electrostatic chuck pedestal:
> 9 components, 105 driving parameters, 19-occurrence assembly, 11 drawing documents over 14
> sheets, indentured BOM, and 61 digest-registered deliverables verified bi-directionally against
> their register — **895 tests, 843 reproducing from a clean clone of the published repository.**

**B — verification, governance and defect discovery**

> Built the verification and governance layer for an agent-driven CAD system — 13 laws, 12 role
> contracts, 8 standing checks, hash-chained ledger, and a role-separation rule barring any role
> from verifying its own output — then subjected it to **five independent cold-context QA rounds,
> four of which returned NOT CLEARED** and found real defects, including a ruling enforced only on
> a non-canonical code path that survived 846 tests. The same discipline applied to geometry
> caught a specification-level defect in a CAD run where every Fusion operation succeeded: two
> tap features intersecting thermal-choke slots, detected as a **173.71 mm³ deviation against a
> 1 mm³ tolerance**, root-caused to a placement window with no compliant position anywhere inside
> it.

---

## Scope statement — include this if space allows

> Digital release complete (`v0.11.0`, reproducible from a clean clone). **Physical qualification
> not started: 0 of 91 hardware-verifiable requirements verified; no article built.** One defect
> open against the design baseline and documented as blocking hardware build.

Include it. It is short, it is unusual, and in semiconductor equipment engineering it reads as
competence rather than as a caveat — the discipline lives on the distinction between *modelled*
and *qualified*.

---

## Phrases to use, and phrases to avoid

| Use | Avoid |
|---|---|
| agent-driven · requirements-governed · observation-based | *fully autonomous AI engineer* |
| independently verified · provenance-backed · traceable | *revolutionary AI* |
| failure-aware · recoverable · reproducible · release-validated | *AI designed a semiconductor machine* |
| parametric · digest-registered · verified against observed state | *replaced engineers* |
| model-predicted (for anything unmeasured) | *validated* / *qualified* for anything digital |
