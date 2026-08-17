# SEDEP-RPT-004 — Support Ring isolation: the `SR-02` / `SR-03` / `SR-04` path trace

> **Instance artifact.** Partition `analysis`. Filed `S-2026-08-17-01`, discharging
> `OI-C-15` §6.2 in part and raising
> [`ECR-D-016`](../../.ai/project/ecr/ECR-D-016_Support_Ring_Isolation_Joint_Does_Not_Close.md).
>
> **Computed, not transcribed** — `PYTHONPATH=src python -m aief_analysis`, source
> `src/aief_analysis/insulation.py`, attacked by `tests/test_analysis_oi_c_15.py`.
> **The trace does not close.** Three frozen acceptance criteria fail on frozen dimensions.

---

## 1 · What was owed, and what a trace is

`SR-03` (*creepage, RF-hot to grounded hardware, ≥ 20 mm*) and `SR-04` (*clearance, ≥ 12 mm*)
are the only two requirements in `spec/03` whose declared method is **Drawing verification** —
a path trace. `OI-C-15` §6.2 recorded that no such trace had ever been filed, and noted why the
existing tooling did not cover it: `python -m aief_clearance` checks `spec/00` §3.2 *feature*
clearance, which asks whether two features collide in plan. **That is a different property from
how far a conductor is from ground.**

- **Clearance** — the shortest distance through space, conductor to conductor.
- **Creepage** — the shortest path over the surface of the solid insulator between them.

## 2 · The joint

`spec/03` §3.1, two circuits, and the reason the architecture exists (`DR-9`: *no fastener
bridges the insulating web*):

| Circuit | Fastener | Route | Potential |
|---|---|---|---|
| **Lower** | 8 × M6 × 40 | From beneath the Base Plate, through it, through the ceramic bottom flange, into tapped holes in `SEWCP-401` | **Ground** |
| **Upper** | 8 × M6 × 16 | From beneath the ceramic top flange, upward into the Cooling Plate | **RF-hot** |

Both at Ø302 BC, clocked coincident (`SR-IF-3`). Both carry a Ø16 flat washer and a Belleville
stack (`spec/00` §9). Geometry: flanges Ø318.0/Ø286.0 × 3.00, web Ø300.0/Ø294.0 × 14.00 tall,
total height 20.000.

## 3 · The omission

`spec/03` **§2.1** computes the stray flange-to-flange capacitance across *"the 14 mm vacuum
gap"*. **§3.1** computes the `SR-04` clearance as *"the open annular gap between the clamp ring
and the Cooling Plate = 14 mm"*.

**Both treat the gap as empty. §5.2 puts a 6.00 mm grounded metal ring inside it.**

`CR-D03` dimensions `SEWCP-401` at 6.00 thick; `SR-IF-2` seats it 0.50 into a register in the
bottom-flange top face. **5.50 mm of the 14.00 mm gap is grounded metal**, and 8.50 mm is what
remains.

## 4 · Results

| Req | Required | Computed | |
|---|---|---|---|
| `SR-04` | ≥ 12.00 mm | **8.50 mm** | short by **3.50** |
| `SR-03` | ≥ 20.00 mm | **14.00 mm** as modelled, **17.42** at best | short by **6.00** / **2.58** |
| `SR-02` | ≥ 400 Ω | **353.9 Ω** | short by **46.1** |

**`SR-04` = 8.50 mm is the greatest value the joint can offer under any hardware choice
whatever.** The RF-hot boundary is placed *flush with the ceramic* — a position no bolted joint
can achieve, since something must bear on the flange. **No fastener dimension is used to reach
this verdict**, and it fails by 3.50 mm before a single screw is specified. Applying the
hardware `spec/00` §9 mandates — an M6 socket head, a Ø16 washer and a Belleville stack,
roughly 9 mm — exceeds the 8.50 mm remaining, so **the specified assembly interferes.** The
threshold is published rather than a value: any RF-hot protrusion beyond 8.50 mm.

**`SR-03` = 14.00 mm** because neither flange face offers exposed ceramic to run over.
`SEWCP-401` spans Ø318.0/Ø286.0 (`CR-D01`/`CR-D02`) — *exactly* the flange annulus — and on the
RF-hot side a Ø16 washer centred on Ø302 BC reaches r = 143.0 to 159.0, which is *also* exactly
the annulus. §3.1's *"down the top flange face (16 mm radial) … out along the bottom flange
(16 mm radial)"* has nothing to traverse, and the path collapses to the web. With `SR-D12`'s
R3.0 fillets it recovers to 17.42 mm — the best the cross-section can produce — and still fails.

**`SR-02` = 353.9 Ω** because the parallel-plate gap in the stray term is 8.50 mm, not 14.00:
stray 9.6 → 15.8 pF, total 27.0 → 33.2 pF, `X_C` 435 → 353.9 Ω.

## 5 · The control, which is what makes this a finding rather than an opinion

`tests/test_analysis_oi_c_15.py::test_the_model_reproduces_spec_03_s2_1` feeds the electrical
model **§2.1's own 14 mm gap** and requires **§2.1's own published answer**:

| | `spec/03` §2.1 publishes | Model returns |
|---|---|---|
| `C`, dielectric web | 17.4 pF | **17.4 pF** |
| `C`, stray flange-to-flange | 9.6 pF | **9.6 pF** |
| `X_C` at 13.56 MHz | 435 Ω | **435 Ω** |

**The control passes and the substitution fails. The divergence is in the input, not in the
arithmetic.**

## 6 · Two further findings, independent of every number above

**A radial collision.** `SEWCP-401` at Ø318.0/Ø286.0 seats on the bottom-flange top face; the
web at Ø300.0/Ø294.0 rises from **that same face**. The footprints intersect over **3.00 mm of
radius — the entire web wall.** It cannot be re-shaped out of the way either: it must carry the
M6 taps at Ø302 BC (`CR-D04`), so it must occupy r ≈ 147.5–154.5, which *is* where the web is.
And the bolt circle cannot move — `FBA-3` freezes the Base Plate's clearance holes at Ø302.

**An over-constrained cross-section.** The flange offers **16.00 mm** of radial width. Its own
frozen features demand a Ø7.0 bolt hole (7.00) + a 3.0 mm web wall (3.00) + two R3.0 fillets
(6.00) = **16.00 mm**. Zero margin, before any edge distance — while `SR-D15` and `SR-D21`
both require 0.3 × 45° chamfers and are marked *Critical*.

**The as-built model corroborates this rather than contradicting it.** The observed operation
list of `cad/runs/RUN-20260811T183556-788260` (verdict PASS, 40 ops) contains **no fillet, no
chamfer and no register counterbore**; `sr_reg_od`, `sr_reg_id` and `sr_reg_dep` were declared
as parameters and never cut. **The fillets are not missing by oversight — there is no radial
room to put them in** (`OI-CAD-04`).

## 7 · Not discharged by this trace

`RF-09`, `RF-10` and `RF-11` remain owed. They are `spec/08` bracket geometry — a different
joint — and asserting them from a `spec/03` result would be exactly the error §6.2 exists to
prevent. `OI-C-15` stays open, narrowed to those three.

## 8 · Disposition

`ECR-D-016`, **disposition A — a Rev B baseline revision of the joint**, ruled under delegated
authority and **implemented at Rev B, not here**. Four alternatives were rejected on computed
grounds, and a feasible Rev B is published with its arithmetic — discrete flange lugs, the web
relocated outboard of the bolt circle, both fastener stacks recessed: ≈0.207 K/W (`SR-05` ✔),
≈532 Ω (`SR-02` ✔), 14.00 mm (`SR-04` ✔), ≈22 mm (`SR-03` ✔).

**SEWCP hardware build is blocked until Rev B. No gate, deliverable or repository release is
blocked**, and `python -m aief_gate` exits 0 throughout.
