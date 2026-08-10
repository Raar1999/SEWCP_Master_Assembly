# ECR-D-008 — Alignment pin material specified two ways

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised on `VER-014`. ECR-D-001 §7 previously asserted this was "raised separately" when it was not; that claim is corrected and this is the filing.

```yaml
ecr_id:       ECR-D-008
class:        D                      # defect - LAW-02
raised_by:    software.software-engineer · S-2026-08-09-14
status:       ENGINEERING-IMPLEMENTED
disposition:  A - SEWCP-700 GOVERNS; THE ICD MATERIAL CELL IS CORRECTED
ruled_by:     human-owner · S-2026-08-10-01
approval:     approvals/APR-021_ICD_coherence_package.md
affected_artifacts:
  - spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md
  - spec/06_SEWCP-700_Alignment_Pins.md
evidence:     "See section 3."
impact:       "See section 4."
requested_action: "See section 5."
raised_at:    2026-08-09T00:00:00Z
closed_at:    null
residual:     none
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

**A — recorded in full at §8.** No option is recommended here: the ICD may be the errant document, or the ICD
may record a later decision the part volume never absorbed. Determining which is a Design
Authority act, and enumerating options before that is settled would prejudge it.

## 7 · Relationship to LC-M04-EXIT

An undispositioned ECR against `spec/**`. **Blocks `C7`.**

## 8 · Disposition — **A**

**`spec/06` governs; the ICD cell is corrected.** Ruled by `human-owner`, `S-2026-08-10-01`,
approval [`APR-021`](../approvals/APR-021_ICD_coherence_package.md).

`spec/00` §8, the SEWCP-700 row, was `316L (metal/metal); Al₂O₃ (ceramic IF)` and now reads
**`Ti-6Al-4V Grade 5`**.

**The whole cell was replaced, not the word "316L".** The parenthetical mandated a material
split by interface type, which requires two part numbers, against `spec/06` §3.1's *"All six are
the same part number."* Substituting the metal alone would have left that contradiction frozen.
`spec/06` §6 rejects **both** materials the cell names, on quantified grounds: 316L at ~150 HV
against a 1,600 HV alumina slot, and a ceramic pin as brittle in shear and unnecessary against
the 128× margin. **This ECR as raised recorded only the 316L half of the conflict.**

**Zero cascade.** No requirement, margin, budget or dimension in the frozen set derives from the
ICD cell. Every material-derived value — the §2.3 128× shear margin, the §3.3 fit stack, the §9
0.041 RSS positional budget, FM #4 / #5 / #8, the 6.7 W/m·K parasitic claim — is already
computed against Ti-6Al-4V and is untouched. The ICD's own `Ra 0.4 µm` finish cell already
agreed with `spec/06` §8, which is the signature of a single-cell error rather than of a later
decision recorded in one place only.

Options **B** (rewrite `spec/06` to 316L, which re-opens a positional budget carrying 0.009 mm
of margin and leaves a volume arguing against its own material) and **C** (two part variants)
were presented and not approved.
