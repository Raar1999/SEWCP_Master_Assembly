# ECR-Q-011 — FSW internal-rib passes: is there a minimum rib width for tool shoulder engagement?

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised exactly as `MDR-001` §5 prescribed: a manufacturing input the record did not have,
> raised rather than assumed. Session `S-2026-08-11-01`.

```yaml
ecr_id:       ECR-Q-011
class:        Q                      # ambiguity / missing input - LAW-02
raised_by:    mechanical.cad-engineer · S-2026-08-11-01
status:       OPEN
disposition:  null
ruled_by:     null
ruled_at:     null
instrument:   null
approval:     null
affected_artifacts:
  - implementation/01_SEWCP-200_Cooling_Plate/cad/SEWCP-200_MDR-001_Coolant_Channel_Routing_Topology.md
  - implementation/01_SEWCP-200_Cooling_Plate/requirements/SEWCP-200_coolant_channel.requirements.json
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-11T00:00:00Z
related:      MDR-001 §5
```

---

## 1 · Class

**Q — missing manufacturing input.** No frozen artifact constrains the rib width between
adjacent channel passes. `spec/01` §6 step 5 requires *"circumferential + internal rib passes"*
of friction stir welding, and FSW tool shoulders have engagement-width requirements this
repository does not state. Nothing is provably wrong; an input is absent. Under LAW-02 the
affected item holds only if the answer exceeds the design value; unrelated work proceeds.

## 2 · Evidence

- `MDR-001` §5: *"Rib width between adjacent channel passes is not constrained by any frozen
  artifact. If the FSW internal-rib passes require a minimum rib for tool shoulder engagement,
  that is a manufacturing input this record does not have, and it will be raised as an ECR-Q
  rather than assumed."* This record is that ECR-Q.
- `SEWCP-200-REQ-002` routes the channel with a **design rib of 5.0 mm** — the illustrative
  figure `MDR-001` §4 itself uses. It is a free design choice inside current constraints, not a
  claim about FSW feasibility.

## 3 · Impact

If the FSW supplier's minimum rib exceeds 5.0 mm, the pass schedule derived for sketch `S3`
must be re-routed at the larger pitch (the router re-derives deterministically from the
updated value), the developed path shortens further against the §2.1 ≈2.2 m design basis, and
`CP-11` margin shrinks — which the thermal map verification would have to absorb or an ECR-D
against the schedule would follow.

## 4 · Requested action

State the minimum rib width (mm) between adjacent channel walls that the selected FSW process
requires for the internal rib passes, with its source (tool specification or supplier input).
Disposition options: **(a)** 5.0 mm is acceptable — record and close; **(b)** a larger minimum
governs — state it, and `SEWCP-200-REQ-002` re-routes at that value.
