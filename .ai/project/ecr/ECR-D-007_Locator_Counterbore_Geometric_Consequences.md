# ECR-D-007 — Geometric consequences of the Ø12.000 locator counterbore are unassessed

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Split from ECR-D-001 by human-owner decision, session `S-2026-08-09-14`, Option B, approval [`APR-017`](../approvals/APR-017_Alignment_Pin_Clerical_Correction.md).

```yaml
ecr_id:       ECR-D-007
class:        D                      # defect - LAW-02: a defect stops the affected work
raised_by:    software.software-engineer · S-2026-08-09-14   # on VER-014 findings F3, F4, F9, F10
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

**D — defect.** The alignment-pin interface geometry is now coherent across the frozen set
(ECR-D-001, disposition A), but the feature that geometry requires — a **Ø12.000 H7 × 3.00
counterbore with an M4 × 0.7 retention thread of undetermined depth**, at Ø306 BC and Ø260 BC in the Cooling
Plate — has **never been assessed against that plate's own keep-out rules**, under either the
superseded or the current geometry. Under LAW-02 a defect stops the affected work: SEWCP-200
CAD cannot route the coolant circuit without the missing values.

**This is not a consequence of ECR-D-001's decision being wrong.** The counterbore is declared
by `AP-IF-1` in SEWCP-700, the governing volume, and pre-dates this session. It was invisible
while `spec/01` disagreed with SEWCP-700; correcting that disagreement made it visible.

## 2 · Affected artifacts

| Artifact | Role |
|---|---|
| `spec/01_SEWCP-200_Cooling_Plate.md` | §3.1 keep-out table has no kinematic-locator row; hosts all six counterbores |
| `spec/06_SEWCP-700_Alignment_Pins.md` | Declares the Ø12.000 k6 flange and the counterbore it seats in |
| `spec/02_SEWCP-300_Heater_Plate.md` | States no kinematic slot depth |

## 3 · Evidence

All figures below are computed from values quoted out of the frozen volumes. Radii are from
the chuck axis.

**3.1 The §3.1 keep-out table has no row for the locators.** `spec/01` §3.1 gives a keep-out
radius and a minimum wall to channel for the He bore, lift-pin bores, HV feed bores, M5 choke
holes, M6 ring holes, RTD ports, the RF land and the plate OD. It has **no row for the
kinematic locators**, and never had one for the superseded Ø6 bores either. §3.1 closes:
*"CAD shall route the serpentine to satisfy the table **before** optimizing for path length."*
A modeller has no number to satisfy.

**3.2 The counterbore now overlaps the declared channel annulus radially.** The channel is
*"confined to the **Ø60 to Ø250 annulus**"* → outer limit **r = 125.00**.

| | Ø6.000 bore (superseded) | Ø12.000 counterbore (current) |
|---|---|---|
| Top locator axis, Ø260 BC | r = 130.00 | r = 130.00 |
| Inner edge of the feature | r = **127.00** — clear by 2.00 mm | r = **124.00** — **1.00 mm inside the annulus** |

The counterbore is 3.00 mm deep and the channel-to-top-face wall (`CP-D07`) is 8.00 ± 0.20 mm,
so **there is no axial intersection**; the overlap is of plan-view footprint against a
declared keep-out zone. Whether that is acceptable is an engineering judgement no volume makes.

**3.3 The M4 thread's wall to the channel is below the value demanded of its analogues.**
M4 × 0.7 tap drill Ø3.30 at Ø260 BC → inner edge **r = 128.35**. Channel outer limit r =
125.00 → **3.35 mm** of wall. §3.1 demands **3.5 mm** of the M5 choke holes and the M6 support
ring holes — the two most similar features. **3.35 < 3.5**, by 0.15 mm.

The M4's **depth is undetermined** — `CP-D09a`/`CP-D10a` read `depth TBD — ECR-D-007` since
`APR-018`. The first form of this paragraph computed *"8.0 mm deep beneath a 3.00 mm
counterbore = 11.0 mm below the top face"* from a value an implementing agent had set with no
authority (`VER-014` R10(a)); that value is struck and the arithmetic with it. What stands is
the **conditional**: any tap depth exceeding **5.00 mm** below the counterbore floor puts the
thread past `CP-D07`'s 8.00 mm channel-to-top-face wall, after which it is kept clear of the
circuit only by the 3.35 mm radial wall questioned above. The depth is requested action 5.

**3.4 The bottom locator leaves 1.00 mm of wall to the plate OD.** Ø306 BC → axis r = 153.00.
Ø12.000 counterbore → outer edge **r = 159.00**. Plate OD `CP-D01` Ø320.0 ± 0.10 → r = 160.00,
**159.95 at minimum**.

| | Ø6.000 bore (superseded) | Ø12.000 counterbore (current) |
|---|---|---|
| Annular wall to OD | **4.00 mm** | **1.00 mm** nominal, **0.95 mm** at minimum OD |

Into that wall goes a **Ø12.000 k6** titanium flange — a transition fit carrying up to
**0.012 mm interference** (`AP-D03`) — and §8 specifies 50 µm Type III hard anodize on the OD.
No volume assesses hoop stress, anodize growth into the fit, or breakout risk at 0.95 mm.

**3.5 The Heater Plate states no slot depth.** `HP-D09`–`HP-D11` give width, length and
position. No depth row exists, and `HP-IF-3` gives none. The only source of 3.0 D at Ø260 BC is
`AP-IF-3` in SEWCP-700. Boss/slot clearance at that interface is therefore **undecidable from
the host volume**. (At the Ø306 BC interface `SR-D19` states 3.00 ± 0.10 and the clearance
closes at 0.35 mm worst case.)

## 4 · Impact

Blocks SEWCP-200 CAD: the coolant serpentine cannot be routed to a table that does not
constrain the locators, and the modeller would have to invent the keep-out values — which is a
Design Authority act. Does **not** invalidate ECR-D-001: the geometry conflict it resolved is
resolved, and the interface is coherent.

## 5 · Requested action

Four values or rulings, each of which is an engineering decision:

1. **A kinematic-locator row for the §3.1 keep-out table** — keep-out radius from the feature
   axis, and minimum wall to channel, for the Ø12.000 counterbore and the M4 thread.
2. **Accept, or reject, the 3.35 mm channel wall** against the 3.5 mm demanded of the M5/M6
   analogues.
3. **Accept, or reject, the 1.00 mm (0.95 mm minimum) annular wall to the plate OD** carrying
   a k6 interference flange with 50 µm anodize. If rejected, the Ø306 BC bolt circle or the
   flange diameter must move — which reopens `AP-IF-1`/`AP-D03` in SEWCP-700.
4. **A slot depth for SEWCP-300**, or a recorded ruling that `AP-IF-3` governs it.
5. **The M4 retention tap depth** for `CP-D09a`/`CP-D10a`. Constraints: an `M4 × 10` screw
   traversing a 5.50 mm locator needs **4.50–6.70 mm** of engagement; any depth beyond
   **5.00 mm** below the counterbore floor crosses `CP-D07`'s 8.00 mm wall into the channel
   band, where item 2's 3.35 mm radial margin becomes the only separation. Added by `APR-018`
   after an unauthorised 8.0 mm was struck from `spec/01`.

## 6 · Disposition

**None. OPEN.** No option is recommended in this record: item 3 in particular may require
changing the governing volume, and enumerating options before the constraint set is settled
would prejudge it. An analyst package will be prepared when this ECR is scheduled.

## 7 · Relationship to LC-M04-EXIT

`C7` requires that *no ECR against the frozen specification remains undispositioned* at gate
time. **This ECR is such an item and therefore blocks `C7` until dispositioned.** It is
recorded here rather than deferred, because deferring it would clear the gate against the four
known defects while a fifth sat open — which is the precise failure `C7` exists to prevent.
