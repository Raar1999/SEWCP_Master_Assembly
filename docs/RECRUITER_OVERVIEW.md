# AIEF / SEWCP — Recruiter Overview

*Two pages. Every figure is computed by a command named beside it, at release `v0.11.0`,
commit `cad6ced6`.*

---

## What

**An agent-driven engineering system that turns a governed semiconductor-equipment
specification into parametric Fusion 360 CAD, reads the resulting model back out of Fusion, and
verifies the observed geometry against the requirement before anything is saved or released.**

The demonstration hardware is **SEWCP** — a 300 mm bipolar electrostatic chuck pedestal for
RF-biased plasma process equipment. Cooling plate, heater plate, ceramic support ring,
electrostatic chuck, lift pins, alignment pins, vacuum port, RF feedthrough, sensor bracket.

## Why it exists

An LLM can emit CAD API calls, and Fusion will happily execute them. **Execution success is not
engineering correctness** — it only means Fusion accepted the operation. The gap between those
two things is where design defects live.

AIEF closes that gap: after every run it queries the live model for extents, volume, mass,
material, parameters, sketches, planes and the feature list, and compares the *observed* values
to the frozen requirement. A run that executes cleanly and produces the wrong solid **fails**.

## How it works

```
governed requirements → design solution → command sequence → Fusion 360
        ↑                                                        │
        │                                              observed model state
    repair / re-run                                              │
        ↑                                                        ▼
      FAIL ←──────────────── independent verification ────────→ PASS → save + release
```

Full detail: [`ARCHITECTURE.md`](ARCHITECTURE.md).

## Result — verified figures

| | |
|---|---|
| Components specified, frozen Rev A | **9** (137 numbered requirements) |
| Part designs modelled and verified | **10** |
| Master assembly | **19 occurrences**, 7.6997 kg |
| Final system verification | **19 / 19** |
| System interfaces | **12 / 12** |
| Drawings | **11 documents / 14 sheets**, **79 dimensions, 0 unsourced** |
| Registered deliverables | **61 files**, 4,995,097 bytes, digest-checked both directions |
| Test suite | **895 pass** locally · **843 pass, 52 skip, 0 fail** from a clean clone |
| Standing checks | 7 exit 0; 2 exit 1 **by design**, on defects that are real |
| Independent QA rounds | **5**, cold-context; 4 returned `NOT CLEARED` |
| Tracked CAD runs | **36** — 18 PASS and **18 FAIL, kept in the repository** |
| **Physical qualification** | **0 of 91 hardware-verifiable requirements. Not started.** |

## Key technology

Python 3.11 · Autodesk Fusion 360 API and a custom add-in (the CAD bridge) · agent role
orchestration under a file-based governance framework · observation-based geometry verification
· SHA-256 digest provenance and a hash-chained ledger · deterministic SVG/PDF drawing generation
· Git, GitHub Actions CI, digest-registered release manifests.

## Key differentiator

**Design → Execute → Observe → Verify → Repair.**

Most CAD automation stops at *Execute*. This system treats the executed command as an unproven
claim and the observed model as the only evidence. Concretely: two Ø6 hanger taps were cut at
radius **137.000 mm** instead of the ruled **150.000 mm**. Every Fusion operation returned OK.
The run **failed** — because the observed solid retained 173.71 mm³ more material than the
requirement allowed, against a 1 mm³ tolerance. That is
[the whole argument](FAILURE_RECOVERY.md), in one measurement.

## What I actually engineered

- The **CAD bridge**: a Fusion 360 add-in exposing a 16-operation vocabulary + an extension
  module, driven over a file queue, that returns *observed* state rather than acknowledgements.
- The **verification layer**: three independent verifiers (geometry, interface, constraint) that
  score a run from observed model state against requirement-derived acceptance criteria.
- The **document lifecycle**: identity without persistence, first-save only on verified PASS,
  and an explicit failure disposition — which is why the tree carries no blank orphan designs.
- The **governance framework (AIEF)**: 13 laws, 12 role contracts, 25 validation rules, a
  six-stage compiler, a hash-chained ledger, and eight standing checks that compute the
  properties the documents claim.
- The **engineering specification** and the **CAD, drawings, BOM and analyses** produced under it.

## Limitation — stated first, not buried

**Digital release is complete. Physical qualification is not started.** No article has been
built, nothing has been measured, and 91 of the 137 requirements need hardware. Four mass
figures are labelled `MODEL-PREDICTED`, never verified.

**One defect is open against the design itself.** `ECR-D-016` — the Support Ring isolation joint
does not close: creepage 14.00 mm against 20.00 mm required, clearance 8.50 mm against 12.00 mm,
shunt impedance 353.94 Ω against 400 Ω. It was found by a standing check, it is ruled, its
remedy is computed, and it is deliberately **not** implemented, because implementing it is a
specification re-baseline. **Do not build to this baseline.**

Both facts are in the release tag message, the first screen of the README, and
[`RELEASE.md`](RELEASE.md). A design system that hides its open defects is not one I would
want to be judged on.
