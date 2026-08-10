# ECR-D-010 — Three top locators occupy the same rays as three outer choke stations

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-ecr.schema.json`.
> Raised `S-2026-08-10-01` on a computed clearance sweep of the `spec/00` §3.2 clocking map.

```yaml
ecr_id:       ECR-D-010
class:        D
raised_by:    chief-systems-engineer · S-2026-08-10-01
status:       ENGINEERING-IMPLEMENTED
disposition:  A - RE-CLOCK THE TOP LOCATORS TO 75/195/315
ruled_by:     human-owner · S-2026-08-10-01
approval:     approvals/APR-021_ICD_coherence_package.md
affected_artifacts:
  - spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md
  - spec/01_SEWCP-200_Cooling_Plate.md
  - spec/02_SEWCP-300_Heater_Plate.md
  - spec/06_SEWCP-700_Alignment_Pins.md
evidence:     "See section 3. The locator counterbore at O260 BC spans r 124-136; the outer
               choke M5 slot at O270 BC spans r 131.5-138.5 and its CP-D17 O22 washer pad
               spans r 124-146. Both angle sets contain 30, 150 and 270 degrees."
impact:       "See section 4. Three of sixteen choke stations are unbuildable as clocked."
requested_action: "See section 5."
raised_at:    2026-08-10T00:00:00Z
closed_at:    null
residual:     null
```

---

## 1 · Class

**D — defect.** Two features are declared to occupy overlapping material on the same face.

## 2 · Affected artifacts

`spec/00` §3.2 clocking map · `spec/01` `CP-IF-4`, `CP-D10` · `spec/02` `HP-IF-3`, `HP-D11` ·
`spec/06` `AP-IF-3`.

## 3 · Evidence

| Feature | Bolt circle | Angles | Top-face radial extent |
|---|---|---|---|
| Kinematic locator counterbore Ø12.000 | Ø260 BC | **30° / 150° / 270°** | r 124.0 – 136.0 |
| Outer choke M5 slot, 5.5 W × 7.0 L | Ø270 BC | **0° + n·30°** | r 131.5 – 138.5 |
| Outer choke `CP-D17` Ø22 washer pad | Ø270 BC | 0° + n·30° | r 124.0 – 146.0 |

The two angle sets share **30°, 150° and 270°**. On those three rays the counterbore overlaps
the M5 slot by **4.5 mm** radially, and the Ø22 washer pad over nearly its whole footprint.

**This pre-dates ECR-D-001.** The superseded Ø6.000 bore spanned r 127–133 and still overlapped
the slot by 1.5 mm. Enlarging the feature to Ø12.000 turned a latent defect into a gross one.

**Why it was never caught — the root cause.** `spec/00` §3.2 declares the map *"binding on every
component"* and closed with *"**No conflicts.**"* That line checked four hand-picked pairs — RTD
against choke, RF land against choke, coolant ports against choke, lift pins against inner
choke — and **the Ø260 BC kinematic locators were not in the table at all.** A prose claim over
a subset of pairs, frozen and never recomputed, is the same failure shape as `OI-V-02` (a
registry bound by no check) and as the approval-supersession defect this session also repaired.

## 4 · Impact

Blocks SEWCP-200 CAD: three of sixteen choke stations cannot be modelled as clocked. Blocks
`LC-M04-EXIT` `C7`.

## 5 · Requested action

Rule which pattern moves, and replace the unverified prose claim with a computed one.

## 6 · Disposition — **A**

**Re-clock the top locators and their mating slots to 75° / 195° / 315°.** Ruled by
`human-owner`, `S-2026-08-10-01`.

**Why 75/195/315 is optimal rather than merely adequate.** A 120°-spaced triad has the same
offset modulo 30° at all three positions, so against a 30° choke pattern the achievable
separation is `θ mod 30`, maximised at **15°**. Of the candidate triads at that offset:

| Triad | Verdict |
|---|---|
| 15 / 135 / 255 | **255° is the coolant inlet ray.** The M4 tap at z 12–17 would meet the Ø10.0 stub bore at z 6–16 |
| 45 / 165 / 285 | **285° is the coolant outlet ray.** Same collision |
| **75 / 195 / 315** | **Clear of everything.** 15.4° clear of the RF land envelope (93°–117°); centre distance to the nearest Ø22 choke pad **34.97 mm** against **17.0 mm** required |

**Datums B and C are the Ø306 BC bottom locators and are untouched**, so the datum reference
frame does not move.

### 6.1 Executed changes

`spec/00` §3.2 gains the missing **Ø260 BC locator row**, and its false verification paragraph
is replaced by a computed statement; `spec/01` `CP-IF-4` and `CP-D10`; `spec/02` `HP-IF-3` and
`HP-D11`; `spec/06` `AP-IF-3`.

### 6.2 Root-cause remedy, at the owner of the invariant

`python -m aief_clearance` computes pairwise clearance for every declared feature pair, reading
the §3.2 map itself as its input so the frozen specification stays the source rather than a copy
of it. It exits non-zero on interference. `tests/test_clearance.py` restores the old clocking
and **requires the check to fail**, so the defect cannot return through the obvious alternative
representation; a further test requires every declared footprint to be present in the map, since
the original failure was an **absent row**, not a wrong one.

The check found this defect. It was not told about it.

## 7 · Relationship to `LC-M04-EXIT`

Blocks `C7` until dispositioned. Dispositioned here.
