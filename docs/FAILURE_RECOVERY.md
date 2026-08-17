# Failure → Recovery → Verification

*Two real failures from the tracked record. No example here is invented; every figure is quoted
from a file in this repository, and each file is named.*

The repository tracks **36 component CAD runs — 18 PASS and 18 FAIL**. The failures are
committed on purpose. A design system whose record contains only successes has not shown you its
verification working; it has shown you its verification never firing.

---

## Case 1 — The two taps that Fusion built perfectly, and that were wrong

**The one that justifies the whole architecture.** Every CAD operation succeeded. Nothing errored.
The part was wrong, and the only thing that noticed was a number read back out of the model.

### Initial design and action

`ECR-Q-012` ruled a plate-hung RF hanger, which required two new M6 × 12 bracket taps in the
Cooling Plate's bottom face. The specification's own interface requirement **`RF-IF-3` gave a
literal placement window: "Ø274 BC ± 40 mm"**. The design agent placed the taps by that literal
reading — **r = 137 mm, at 88.27° and 121.73°** — and the placement was reviewed and approved
(`APR-029`).

Run `RUN-20260811T224345-ff189f` dispatched eight operations:

```
new_document · set_parameters · rename_component
create_sketch  S6_HANGER_TAP
sketch_circle  centre (  4.132869, 136.937648)  Ø6.0     ← r = 137.0000, θ =  88.2713°
sketch_circle  centre (-72.047994, 116.525047)  Ø6.0     ← r = 137.0000, θ = 121.7287°
extrude        cut, 12.0 mm
observe
```

### Observed failure

```
dispatched: 8   executed: 8   execution_halt: null
```

**Fusion executed all eight and reported no error.** A pipeline that trusts command success ships
this part.

The verifier read the model back and returned `FAIL`, 9 checks, 1 failed:

| | |
|---|---|
| `id` | `ACC-VOL` |
| `subject` | `body:CP_BODY.volume_mm3` |
| `requirement` | `CP-HANGER-TAP` |
| `expected` | `1479108.9` |
| `observed` | `1479282.6100163697` |
| `detail` | `delta 173.71 exceeds tolerance 1` |

A discrepancy of **0.012 %** of the part volume, caught against a **1 mm³** tolerance on a
1.48 × 10⁶ mm³ solid.

### Root-cause classification

`_classify` maps subject `body:*` to *"the solid was not created, or its extent does not match the
distance the solution declares"* → **repairable, re-dispatch the profile and extrude operations.**
So the loop tried.

- Attempt 2: a 5-operation repair sequence, digest `sha256:fc10713e…`
- Attempt 3: the same repair, same digest, same finding
- Escalation recorded: `attempt limit 3 reached with 1 check(s) still failing`

**The loop stopped rather than degrading into a pass.** That is the second guarantee in
`loop.py` — *"On exhaustion the loop stops and reports the surviving findings, which is a real
outcome; it does not degrade into a pass."*

### Owning layer — and this is the interesting part

Re-dispatch could never have fixed it, because **the defect was not in the CAD layer at all.**

The engineering diagnosis, recorded at `DEC-02 addendum`: the taps at r = 137 **intersect the
90°/120° outer choke through-slots** (Ø270 BC, 5.5 × 7.0). Two blind M6 × 12 taps should have
removed **678.6 mm³**; because they broke into existing voids they removed only **504.8 mm³** —
and 678.6 − 504.8 = **173.8 mm³**, which is the delta `ACC-VOL` reported.

A feasibility sweep was then run across the whole approved window:

> *"the slot at 90° and the land edge at 93° close the lower window; 117°–120° closes the upper
> one — **no compliant position exists inside ±40 mm**. RF-IF-3's window is itself infeasible;
> nothing at Ø274 BC was ever clearance-checked for bracket taps."*

**The requirement was wrong, not the model.** The owning layer was the specification.

### Rollback

Before anything else, the failure disposition ran. The run record shows it attempting
`discard_document` and being **refused by contract**:

```
discard_document: 'SEWCP-200_COOLING_PLATE' is persisted;
a saved design is never discarded by recovery - use revert_document
```

That refusal is the document-lifecycle policy firing in production: *an authoritative design can
never be destroyed by a failure path.* It fell back to `revert_document`, which restored the
previously verified plate automatically (`DEC-02 addendum`; `cad/POST_GEOMETRY_RUN.md`). Across
all three attempts the failing document was **never saved** — `saved: false` throughout.

### Repair

Corrected placement **r = 150 mm, at 88° and 122°**, and — because the first placement had been
approved on an unchecked window — the new one was cleared against nine named neighbours before
it was dispatched: choke slots (15.8 mm centre distance against 8.4 needed), ring bolts at
112.5°/67.5° (24.9 mm), locator slots (74 mm), land outer radius 146 against tap inner edge 147,
channel envelope (125), RTD ports, coolant stubs, plate OD (foot edge 159 < 160), and the
top-face ring taps. Both specification rows were re-issued under `APR-031`/`APR-032`.

### Re-execution and independent verification

Run `RUN-20260811T224915-001c51` — a **different requirement package and a different design
solution**, which the record proves: `package_digest` and `solution_digest` both differ from the
failed run's. The correction was made in the layer that owned it.

```
sketch_circle  centre (  5.234925, 149.908624)  ← r = 150.0000, θ =  88.0000°
sketch_circle  centre (-79.48789,  127.207214)  ← r = 150.0000, θ = 122.0000°
```

| | |
|---|---|
| Verdict | **PASS**, attempt 1, 9 checks, 0 failed |
| `ACC-VOL` | expected `1479108.9` · observed `1479108.8648750156` — **within 0.04 mm³** |
| `saved` | `true`, version 1 — the first and only save, on verified PASS |

Elapsed between the failed run finishing and the corrected run starting: **5 min 13 s**.

### Why this matters in engineering

Two M6 taps breaking into the outer choke slots is not a cosmetic defect on a plasma pedestal.
The choke slots carry the thermal isolation between the heater and the cooling plate; a tap
opening into them puts a fastener path into a thermal break, on a bottom face that is masked
from anodising and sits in the RF return. It would have been found at first article, or at
first thermal characterisation, or later.

It was found in **seventeen seconds** of run time, by comparing a volume against a requirement.

---

## Case 2 — The empty document that could have reported green

**The failure mode this repository is most organised against: a check that cannot be evaluated
being counted as a check that passed.**

### Initial action

Run `RUN-20260811T183336-a70c01` — Support Ring `SEWCP-400`, alumina, 26 acceptance checks.

### Observed failure

```
attempt 1  execution_halt:
  OP-0004 (assign_material) did not execute -
  RuntimeError: no material matching 'Aluminum Oxide' in any loaded library
```

Fusion accepted operations 1–3 and then refused the fourth: the material name in the solution
did not exist in any loaded Fusion material library. The sequence halted, leaving a document with
**0 bodies, 0 parameters and no planes**.

The verifier scored it **22 of 26 failing** — and the interesting thing is *how* it reported the
misses:

```
ACC-BODY-DZ    body:SR_BODY.dz      expected 20.3   observed None
   "not present in the observed model. A check that cannot be evaluated has not passed"

GEO-BODY-PRESENT   bodies.count      expected >= 1   observed 0
   "the solution extrudes a solid but the model reports no body"

IF-PLANE-...       plane:PL_WEB.exists   expected True   observed False
   "construction plane 'PL_WEB' is declared by the solution and absent from the model;
    every feature that locates against it is unlocated"

GEO-PATH-OBSERVED-mech.SR-BFLANGE.rings   sketch:G1_BFL.curve_geometry
   "the routed path cannot be verified without observed curve geometry;
    unmeasured is not compliant"
```

This is `observe.py`'s rule — *absence is represented as absence* — doing the work. Had a missing
body been modelled as a body of volume zero, several numeric checks would have compared 0 to 0
and passed on an empty document.

### Root cause, owning layer, and the bounded repair

Attempts 2 and 3 got past the material and halted further down:
`RuntimeError: sketch 'G1_BFL' yields no closed profile` — a second, independent defect in the
sketch construction, uncovered only because the first was cleared. Failing checks rose to 24 of
26 as more of the sequence executed and more of the model could be checked at all. Escalation:
`attempt limit 3 reached with 24 check(s) still failing`.

Both causes sat in the operation-compilation layer: a material identifier that did not resolve
against Fusion's libraries, and a profile that did not close. Neither is an engineering
escalation, and neither was guessed at — `document.units` and unclassified findings are the two
categories `_classify` refuses to repair, on the stated principle that *"an unclassified failure
is not repaired by guessing."*

### Re-execution and verification

Run `RUN-20260811T183556-788260` — **PASS**. `SEWCP-400_SUPPORT_RING` is in the released set:
STEP, STL, drawing `SEWCP-400-DRW-001`, and BOM line `Al2O3 99.5%`.

---

## The same pattern at three other layers

| Layer | Failure | How it surfaced | Outcome |
|---|---|---|---|
| **Acceptance criteria** | `SEWCP-901` RF strap failed `ACC-BODY-DX` (expected 131.25, observed 131.5) and `ACC-BODY-DZ` (expected 66.438, observed 66.68821) over three attempts | the *criteria* were stale, not the geometry (`cad/DOCUMENT_LIFECYCLE.md` classifies `RUN-20260811T200134-c51fe2` as "verdict FAIL — stale acceptance extents") | criteria re-derived; `RUN-20260811T200254-ca7080` PASS |
| **Architecture** | failed runs were leaving **saved blank Fusion documents** behind | `rename_component` had to `saveAs`, because Fusion refuses to rename an unsaved root component — so persistence preceded geometry, and no failure path disposed of the document | identity bound as a design attribute without persisting; first-save moved into `save_document` alone, dispatched only on verified PASS; enforced by `tests/test_document_lifecycle.py::test_only_the_verified_save_path_may_first_save`. Orphans deleted, not renamed — *"quarantine is not cleanup"* |
| **Escalation, correctly refusing to retry** | `SEWCP-1000` retainer: `ACC-FEATURES` expected 6, observed 5 | the loop declined to re-dispatch at all: `no repairable finding: every failure is an engineering escalation, not a re-dispatch` | escalated on attempt 1; corrected run `RUN-20260811T182006-72bc80` PASS |

---

## What the system is actually built to do

Not *generate CAD commands that succeed*. Any competent LLM can do that, and Fusion will execute
them.

**Discover that a command which succeeded produced the wrong engineering outcome — then say
which layer owns the mistake.** In Case 1 that layer was the frozen specification, and the
evidence that convicted it was 173.71 mm³ of aluminium that should not have been there.

Related: the same discipline applied to the framework's own software produced five independent QA
rounds and four `NOT CLEARED` verdicts — [`QA.md`](QA.md).
