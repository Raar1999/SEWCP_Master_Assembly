# ECR-D-013 — RF strap terminal hole pitch (25.0) cannot close against the plate tap clocking (98.73°/111.27°)

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Found at assembly integration, session `S-2026-08-11-02`, while placing the verified
> SEWCP-901 strap against the verified SEWCP-200 plate.

```yaml
ecr_id:       ECR-D-013
class:        D                      # defect - two frozen volumes disagree
raised_by:    mechanical.design-engineer · S-2026-08-11-02
status:       DISPOSITIONED
disposition:  A - strap holes made coincident with the CP-IF-8 taps (29.94 in-plane centres); RS-D07 re-defined; plate unchanged
ruled_by:     claude-under-owner-delegation (owner-delegated engineering authority, mission 2026-08-11 s1; NOT a human approval)
ruled_at:     2026-08-11T00:00:00Z
instrument:   .ai/project/decisions/DECISIONS_S-2026-08-11-05.md DEC-01
approval:     APR-030 (spec/08), APR-029 (spec/01 chain unaffected by this ECR but co-registered)
affected_artifacts:
  - spec/01_SEWCP-200_Cooling_Plate.md
  - spec/08_SEWCP-900_RF_Feedthrough_Bracket.md
  - params/generated/SEWCP-200.csv
  - implementation/08_SEWCP-900_RF_Feedthrough_Bracket/requirements/SEWCP-901_rf_strap.requirements.json
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-11T00:00:00Z
related:      ECR-Q-010   # the same land was already dimensioned two ways
```

## 1 · Class

**D — defect.** `spec/01` CP-IF-8 places the two M6 land taps at **98.7°/111.3° on r = 137**
(chord 29.94 mm, arc 30.0 mm). `spec/08` RS-D07 drills the strap terminal holes at
**25.0 mm centres**. Both are frozen. A Ø6.6 hole over an M6 screw absorbs ±0.3 per side;
a 4.94 mm centre-distance error cannot assemble. Computed, not asserted:
`2·137·sin(6.273°) = 29.94` versus `25.0`.

## 2 · Evidence

- `spec/01` line "2× M6 × 12 deep tapped at r = 137, 98.7° and 111.3°" — realised in the
  verified SEWCP-200 model at 98.73°/111.27° (parameter master `rf_tap_half_ang`,
  `rf_tap_pitch = 30.0`, comment "Derived from 98.7°/111.3°").
- `spec/08` RS-D07 "Terminal bolt holes 2× Ø6.6 at 25 mm centres" — realised in the
  verified SEWCP-901 model at 25.0 centres (`rs_hole_pitch`).
- `ECR-Q-010` already records this land dimensioned two ways (60 mm circ ↔ 93°–117°);
  this is a third, independent inconsistency on the same interface.

## 3 · Impact

Blocks hardware build of the RF joint only; blocks no CAD deliverable. The master
assembly places the strap at its nominal position regardless. Both parts remain
individually conformant to their own volumes.

## 4 · Requested action

Rule one of: **(a)** re-pitch RS-D07 to the tap chord (29.94, or restate as 30.0 arc /
2× at 98.7°/111.3° projected) — one-line change to `spec/08`, strap holes re-drilled in
CAD deterministically; **(b)** re-clock CP-IF-8 taps to 99.77°/110.23° (chord 25.0) —
touches the verified plate model and the clearance framework. Recommendation of the
raising agent: **(a)** — the strap is the adaptable part; the plate taps already clear
the channel keep-out and the RTD/choke patterns at the present clocking.
