# ECR-Q-012 — SEWCP-902 saddle mounting architecture is underdefined and internally contradicted

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Found at assembly integration, session `S-2026-08-11-02`. Allocated above the
> ECR-Q high-water mark per the OI-C-11 convention.

```yaml
ecr_id:       ECR-Q-012
class:        Q                      # ambiguity / missing input - LAW-02
raised_by:    mechanical.design-engineer · S-2026-08-11-02
status:       DISPOSITIONED
disposition:  Plate-hung hanger (option a) - support from above at 8.25, all surfaces >= 8.0 from ground, RF-hot by mounting; SB-D01..D04 re-dimensioned; CP-IF-8 gains the two bracket taps; strap seat convention resolved as top-face bearing at 8.25 (mid-plane 8.0)
ruled_by:     claude-under-owner-delegation (owner-delegated engineering authority, mission 2026-08-11 s1; NOT a human approval)
ruled_at:     2026-08-11T00:00:00Z
instrument:   .ai/project/decisions/DECISIONS_S-2026-08-11-05.md DEC-02
approval:     APR-029 (spec/01), APR-030 (spec/08)
affected_artifacts:
  - spec/08_SEWCP-900_RF_Feedthrough_Bracket.md
  - implementation/08_SEWCP-900_RF_Feedthrough_Bracket/requirements/SEWCP-902_saddle.requirements.json
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-11T00:00:00Z
related:      ECR-D-013, SEWCP-904 envelope gap
```

## 1 · Class

**Q — missing input.** `spec/08` states four constraints on the strap support bracket
that do not close into one geometry:

1. `SB-D01`: saddle height "to give RS-D04 = 8.0" — the verified SEWCP-902 model
   realises this as a **7.5-high block seated on the Base Plate** (7.5 + 0.5 strap = 8.0).
2. `SB-D04`: **minimum clearance, any bracket surface to Base Plate, 8.0** — a
   base-seated block violates it by contact.
3. `RF-IF-3`: "**the bracket mounts to the RF-hot plate, not to ground**" — a
   base-seated conductive (6061, Alodine) saddle under an RF-hot strap is a short to
   ground; the bracket must hang from the Cooling Plate.
4. A plate-hung bracket reaching the strap run at z ≈ 8 from the CP bottom face at
   z = 20 is ~12 tall with a cradle — **no dimension in spec/08 defines it**; the 2×
   M6 mounting positions "Ø274 BC ±40 mm circumferential" name taps that no CP
   package realises.

Additionally the two packages disagree by 0.25 on the strap seat plane: SEWCP-902
takes the strap **top** face at 8.0 (seat 7.5); SEWCP-901 takes the **mid-plane** at
8.0 (underside 7.75).

## 2 · Impact

The master assembly places the saddle at its own package's nominal (seated at
Datum A, top at 7.5, under the strap run mid-radius, 105°) and records the placement
as **provisional**. Nothing else consumes the saddle. The SEWCP-902 drawing carries
the same provisional note. Blocks hardware build of the bracket only.

## 3 · Requested action

State the governing bracket architecture: **(a)** plate-hung cradle (RF-IF-3 form) —
supply the drop height, cradle detail and the two CP tap positions, and SEWCP-902
re-models deterministically; or **(b)** base-seated **dielectric** saddle — supply the
material and re-state SB-D04/RF-IF-3. Also state the strap seat convention (top-face
or mid-plane at 8.0). Recommendation of the raising agent: **(a)**, matching the
spec's own §12 rationale.
