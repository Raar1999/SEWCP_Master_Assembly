# ECR-D-016 — The Support Ring isolation joint does not close: SR-02, SR-03 and SR-04 all fail on frozen dimensions

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Found at session `S-2026-08-17-01` by performing the `SR-03`/`SR-04` drawing trace that
> `OI-C-15` §6.2 records as owed and never filed. Computed by
> `PYTHONPATH=src python -m aief_analysis`; attacked by `tests/test_analysis_oi_c_15.py`.

```yaml
ecr_id:       ECR-D-016
class:        D                      # defect - three frozen acceptance criteria fail on frozen dimensions
raised_by:    mechanical.design-engineer · S-2026-08-17-01
status:       DISPOSITIONED
disposition:  A - SEWCP Rev B baseline revision of the isolation joint; both fastener stacks recessed out of the flange gap and the web relocated clear of the bolt circle. RULED here, IMPLEMENTED at Rev B. Hardware build BLOCKED until then; no CAD, drawing or deliverable changed by this ECR
ruled_by:     claude-under-owner-delegation (owner-delegated engineering authority, mission 2026-08-17; NOT a human approval)
ruled_at:     2026-08-17T00:00:00Z
instrument:   .ai/project/decisions/DECISIONS_S-2026-08-17-01.md DEC-13
approval:     none filed - the disposition changes no frozen artifact. spec/03 Rev B is the implementing instrument and requires its own approval
affected_artifacts:
  - spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md
  - spec/03_SEWCP-400_Chuck_Support_Ring.md
  - cad/exports/step/SEWCP-400_SUPPORT_RING.step
  - drawings/parts/SEWCP-400/SEWCP-400-DRW-001_Sh1.pdf
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-17T00:00:00Z
related:      OI-C-15, ECR-Q-014
```

## 1 · Class

**D — defect.** Three frozen acceptance criteria of `spec/03` fail against the frozen
dimensions of `spec/03` itself. Nothing here is a judgement call or a modelling artefact:
every number below is arithmetic over dimensions the specification declares.

| Requirement | Required | Computed | |
|---|---|---|---|
| `SR-04` Clearance, RF-hot to grounded hardware | ≥ 12.00 mm | **8.50 mm** | short by 3.50 |
| `SR-03` Creepage, RF-hot to grounded hardware | ≥ 20.00 mm | **14.00 mm** as modelled, **17.42 mm** at best | short by 6.00 / 2.58 |
| `SR-02` Shunt impedance to ground at 13.56 MHz | ≥ 400 Ω | **353.9 Ω** | short by 46.1 |

## 2 · Evidence

### 2.1 · One omission produces all three

`spec/03` §2.1 computes the stray capacitance across *"the 14 mm vacuum gap"*. §3.1 computes
the `SR-04` clearance as *"the open annular gap between the clamp ring and the Cooling Plate
= 14 mm"*. **Both treat the flange gap as empty.**

§5.2 puts a **6.00 mm** grounded metal ring inside it. `CR-D03` dimensions `SEWCP-401` at
6.00 thick; `SR-IF-2` seats it 0.50 mm into a register in the bottom-flange top face. So
**5.50 mm of the 14.00 mm gap is grounded metal**, and 8.50 mm is what remains.

That single number produces every failure above:

- **`SR-04` = 8.50 mm.** This is the *greatest clearance the joint can offer under any
  hardware choice whatever*, because the RF-hot boundary is placed flush with the ceramic —
  a position no bolted joint can achieve, since something must bear on the flange. **No
  fastener dimension is used to reach this verdict.** It fails by 3.50 mm before a single
  screw is specified.
- **`SR-02` = 353.9 Ω.** The parallel-plate gap in the stray term is 8.50 mm, not 14.00.
  Stray capacitance rises 9.6 → 15.8 pF, total 27.0 → 33.2 pF, `X_C` 435 → 353.9 Ω.
- **`SR-03` = 14.00 mm.** `SEWCP-401` spans Ø318.0/Ø286.0 (`CR-D01`/`CR-D02`) — *exactly*
  the flange annulus — and on the RF-hot side a Ø16 flat washer (`spec/00` §9, mandated for
  both circuits) centred on the Ø302 bolt circle reaches r = 143.0 to r = 159.0, which is
  *also exactly* the annulus. **Neither flange face offers any exposed ceramic to run over**,
  so §3.1's *"down the top flange face (16 mm radial) … out along the bottom flange (16 mm
  radial)"* has nothing to traverse and the path collapses to the web alone.

**The arithmetic is proven against the specification's own published answer.**
`tests/test_analysis_oi_c_15.py::test_the_model_reproduces_spec_03_s2_1` feeds the model
§2.1's own 14 mm gap and requires §2.1's own published 17.4 pF, 9.6 pF and 435 Ω — and gets
them, to the digit. The control passes and the substitution fails, so **the divergence is in
the input, not in the arithmetic.**

### 2.2 · A hard radial collision, independent of every number above

`SEWCP-401` at Ø318.0/Ø286.0 seats on the **bottom-flange top face**. The web at
Ø300.0/Ø294.0 (`SR-D05`/`SR-D06`) rises from **that same face**. Their footprints intersect
over **3.00 mm of radius — the entire web wall**. The specified clamp ring cannot be placed.

It cannot simply be re-shaped, either: it must carry the M6 taps at Ø302 BC (`CR-D04`), so
it must occupy r ≈ 147.5–154.5, which *is* where the web is. And the bolt circle cannot
move — `FBA-3` freezes the Base Plate's clearance holes at Ø302 BC, and `DR-1` makes the
ring the part that adapts.

### 2.3 · The cross-section is over-constrained, and the model already showed it

| | |
|---|---|
| Flange radial width available | (318.0 − 286.0)/2 = **16.00 mm** |
| Ø7.0 bolt hole | 7.00 |
| 3.0 mm web wall | 3.00 |
| Two R3.0 web-to-flange fillets (`SR-D12`, *Critical — ceramic stress riser*) | 6.00 |
| **Demanded** | **16.00 mm** |

**Zero margin, before any edge distance at all** — and `SR-D15` requires a 0.3 × 45°
chamfer on every bolt-hole edge and `SR-D21` on every external edge, both *Critical*.

The Ø7.0 hole at Ø302 BC spans r = 147.5–154.5; the web wall spans r = 147.0–150.0.
**2.50 mm of the 3.00 mm web wall stands directly over the bolt-hole footprint.** The web is
seated on a ring of holes at eight stations.

**The as-built model corroborates this rather than contradicting it.** The observed
operation list of `cad/runs/RUN-20260811T183556-788260` (SEWCP-400, verdict PASS, 40 ops)
contains **no fillet operation, no chamfer operation and no register counterbore** — so
`SR-D12`, `SR-D15`, `SR-D16` and `SR-D21`, four rows of which three are marked *Critical*,
are absent from the verified model. `sr_reg_od`, `sr_reg_id` and `sr_reg_dep` were
*declared as parameters and never cut*. The fillets are not missing by oversight: **there is
no radial room to put them in.** `cad/POST_GEOMETRY_RUN.md` §G5 recorded *"SR-D16 register
degeneracy … candidate ECR-Q noted on the SEWCP-400 drawing; **not raised without
re-verification of the rows**"*. The rows are now re-verified, and this is the raise that
note anticipated.

### 2.4 · Why nothing caught it

`SR-03` and `SR-04` are declared **Drawing verification** — the only two requirements in the
volume whose method is a path trace — and no path trace was ever filed. `python -m
aief_clearance` checks `spec/00` §3.2 *feature* clearance, a different property: it asks
whether two features collide in plan, not how far a conductor is from ground. `SR-02` is
*"Network analyzer / calculation"* and the calculation of record is §2.1's, which assumed the
empty gap. The gate never looked, and the one place a human would have looked — §3.1's
prose — carried a number that was wrong in the reader's favour.

## 3 · Impact

**On the design: the joint as frozen cannot be built and would not perform if it were.**

- `SR-04` fails by 3.50 mm at best. Adding the hardware `spec/00` §9 mandates — an M6 socket
  head, a Ø16 flat washer and a Belleville stack, protruding roughly 9 mm below the top
  flange — exceeds the 8.50 mm that remains, so **the specified assembly interferes.** The
  interference threshold is published: any RF-hot protrusion beyond 8.50 mm.
- `SR-03` at 14.00 mm halves the creepage that FMEA row 3 (*insulation failure, RPN 81*)
  names as its mitigation — *"40 mm creepage (2× requirement)"*. The named mechanism is
  deposition bridging, and the mitigation is now absent.
- `SR-02` at 353.9 Ω is a real RF power loss to ground, not a paper margin.

**On the release: none.** No CAD model, drawing, BOM row or deliverable is changed by this
ECR. The gate is unaffected — `C7` requires a non-empty disposition, which this record
carries. What it changes is what may be claimed: **SEWCP hardware build is blocked until
Rev B**, and no reader may take the CAD baseline as a manufacturable design of this joint.

**On what was already known:** `PVR-001` records 0 of 91 hardware-verifiable requirements
verified, because no article exists. This ECR is consistent with that and sharpens it — the
article should not be built to the present baseline.

## 4 · Requested action

**Option A — Rev B revision of the isolation joint. SELECTED.**
Recess **both** fastener stacks out of the flange gap, and relocate the web clear of the
bolt circle. The gap then contains no conductor, which restores all three requirements at
once, because all three failed for the one reason.

**Option B — reduce `CR-D03`.** A clamp ring thin enough to clear the gap cannot carry
8 × 2.5–3.5 kN of Belleville preload without dishing, and the ceramic capture fails. It also
leaves the radial collision and the `SR-03` shortfall untouched. **Rejected.**

**Option C — relax `SR-03`, `SR-04` and `SR-02` to what the joint achieves.** `SR-04` → 8.50
would be *defensible on the specification's own precedent*: `spec/08` `RF-09` sets ≥ 8 mm
for a vacuum-side clearance with `DR-11` in force, and this joint is entirely above the
Base Plate, hence in vacuum per `FBA-8`. But `SR-03` cannot follow it — halving creepage
removes FMEA row 3's stated mitigation against the mechanism it was written for — and
`SR-02` is a performance loss, not a bookkeeping one. **Three waivers to avoid one
redesign, on the part the architecture explicitly calls deliberately sacrificial.
Rejected.**

**Option D — capture the bottom flange from below.** Requires tapping the frozen Base
Plate. Breaks `FBA-3` and the `DR-1` firewall that is the central architectural decision of
SEWCP. **Rejected.**

**Option E — raise the web height to open the gap.** 26.5 mm of web is needed. `R_web`
becomes 0.316 K/W against `SR-05`'s 0.20 ± 0.03, and ring height 20.000 → 32.5 mm breaks
`DR-3` and every downstream Z-stack row. **Rejected on computed grounds.**

## 5 · Disposition A, and what Rev B must achieve

**Ruled: A. Implemented at Rev B, not here.** The ruling is an engineering decision and is
made under delegated authority. The *implementation* is a specification baseline revision —
it re-opens a frozen volume, invalidates a verified CAD model together with its drawing and
its exports, moves the assembly, and needs an independent QA round of its own that `LAW-05`
bars this session from supplying. Executing that inside a release-preparation session would
be reckless, and doing it badly to make a criterion go green is the failure this repository
exists to prevent.

**A feasible Rev B exists. It was computed, so the next authority meets arithmetic rather
than a blank page.** Discrete flange lugs in place of continuous annular flanges, the web
relocated outboard of the Ø302 bolt circle, and both fastener stacks recessed:

| Term | Present | Rev B candidate | Requirement |
|---|---|---|---|
| Web | Ø300.0/Ø294.0, area 2.799×10⁻³ m² | Ø322.0/Ø316.0, area 3.002×10⁻³ m² | — |
| Flange form | continuous annulus, 1.518×10⁻² m² | 8 lugs, ≈ 5.44×10⁻³ m² | — |
| `R_total` | 0.195 K/W | **≈ 0.207 K/W** | `SR-05` 0.20 ± 0.03 ✔ |
| Parasitic leak at ΔT 20 K | 103 W | **≈ 97 W** | `SR-06` ≤ 110 W ✔ |
| `C_stray` across a **clear** 14 mm gap | 9.6 pF | **≈ 3.4 pF** | — |
| `X_C` at 13.56 MHz | 435 Ω (claimed) / **353.9 Ω** (actual) | **≈ 532 Ω** | `SR-02` ≥ 400 Ω ✔ |
| Clearance | **8.50 mm** | **14.00 mm** | `SR-04` ≥ 12 mm ✔ |
| Creepage | **14.00 mm** | **≈ 22 mm** | `SR-03` ≥ 20 mm ✔ |

Cutting the flange area is what buys `SR-02` back, and it is what makes the lugs affordable
to widen — widening a *continuous* flange to Ø330 costs 5 pF and 70 Ω, which §2.1 already
warned about in terms. The remaining Rev B trade, and the reason no dimensions are frozen
here, is **ring height against thermal resistance**: recessing both stacks needs lug
thickness, and every millimetre of it moves `SR-D01`, `DR-3` and the Z-stack. That is a
program trade across volumes 00, 01 and 03, not a deduction from this record.

**Rev B must close, and be shown to close, all of:** `SR-02`, `SR-03`, `SR-04`, `SR-05`,
`SR-06`, `SR-IF-5`'s Ø286 utility bore, `FBA-3`'s Ø302 bolt circle, the `SR-D12`/`SR-D15`/
`SR-D21` features that have no room today, and `DR-3`'s stack-up. It must be re-modelled,
re-drawn, re-exported and independently verified, and this ECR closes only then.

## 6 · Also raised by this trace, and not folded into it

- **`ECR-Q-014`** — `SEWCP-401` material is specified two ways: `spec/03` §5.2 heads it
  *"(316L)"*, the BOM row carries `6061-T6`. The `ECR-D-008` class, on a different part.
- **`SR-D12`, `SR-D15`, `SR-D16`, `SR-D21` are absent from the verified model** and three of
  the four are marked *Critical*. Recorded here as evidence; the CAD conformance gap it
  implies is `OI-CAD-04`.
