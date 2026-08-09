# ECR-D-008 — Alignment pin material specified two ways

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised on `VER-014`. ECR-D-001 §7 previously asserted this was "raised separately" when it was not; that claim is corrected and this is the filing.

```yaml
ecr_id:       ECR-D-008
class:        D                      # defect - LAW-02
raised_by:    software.software-engineer · S-2026-08-09-14
status:       OPEN
disposition:  null                   # Design Authority decision required
ruled_by:     null
approval:     null
raised_at:    2026-08-09T00:00:00Z
closed_at:    null
residual:     null
```

---

## 1 · Class

**D — defect.** Two frozen volumes state different materials for the same part.

## 2 · Affected artifacts

| Artifact | States |
|---|---|
| `spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md` §Materials | SEWCP-700 — **316L** (metal/metal); Al₂O₃ (ceramic IF) |
| `spec/06_SEWCP-700_Alignment_Pins.md` §7 | **Ti-6Al-4V Grade 5** |

## 3 · Evidence

`spec/06` §6 evaluates and **rejects** 316L for this part: *"Press-fit dowel in 316L — loses
only 2.7 µm, but 316L at ~150 HV wears rapidly against a 1,600 HV alumina slot."* §7 gives
Ti-6Al-4V at ~350 HV and states its CTE (8.6 ppm/K) *"sits between alumina (7.2) and aluminium
(23.6), and is nearly matched to the alumina slots it runs in"*, adding that *"austenitic 316L
(16.0) would open the ring-interface fit by roughly 6 µm over the range."*

The ICD therefore names the material the part volume rejected, on quantified wear and CTE
grounds, for a component that slides in an alumina slot across a 130 K range.

`spec/06` §2.3 further computes its shear margin against **Ti-6Al-4V, 550 MPa** — so the load
case in the part volume is derived from the material the ICD contradicts.

## 4 · Impact

Blocks SEWCP-700 procurement and any CAD that carries material properties. Does not block the
ECR-D-001 geometry, which is material-independent.

## 5 · Requested action

Rule which volume governs the alignment-pin material, and correct the other.

## 6 · Disposition

**None. OPEN.** No option is recommended here: the ICD may be the errant document, or the ICD
may record a later decision the part volume never absorbed. Determining which is a Design
Authority act, and enumerating options before that is settled would prejudge it.

## 7 · Relationship to LC-M04-EXIT

An undispositioned ECR against `spec/**`. **Blocks `C7`.**
