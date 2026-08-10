# ECR-D-007 — Geometric consequences of the Ø12.000 locator counterbore are unassessed

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Split from ECR-D-001 by human-owner decision, session `S-2026-08-09-14`, Option B, approval [`APR-017`](../approvals/APR-017_Alignment_Pin_Clerical_Correction.md).

```yaml
ecr_id:       ECR-D-007
class:        D                      # defect - LAW-02: a defect stops the affected work
raised_by:    software.software-engineer · S-2026-08-09-14   # on VER-014 findings F3, F4, F9, F10
status:       ENGINEERING-IMPLEMENTED
disposition:  A - KEEP-OUT ROW ADDED; 3.35 WALL REJECTED; SLOT DEPTH 3.00; TAP 5.00 FULL THREAD
ruled_by:     human-owner · S-2026-08-10-01
approval:     approvals/APR-020_Cooling_Plate_coherence_package.md
affected_artifacts:
  - spec/01_SEWCP-200_Cooling_Plate.md
  - spec/02_SEWCP-300_Heater_Plate.md
  - spec/06_SEWCP-700_Alignment_Pins.md
evidence:     "See section 3."
impact:       "See section 4."
requested_action: "See section 5."
raised_at:    2026-08-09T00:00:00Z
closed_at:    null
residual:     none - requested action 3 is dispositioned at section 9, not deferred
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

**A — recorded in full at §8.** No option is recommended in this record: item 3 in particular may require
changing the governing volume, and enumerating options before the constraint set is settled
would prejudge it. An analyst package will be prepared when this ECR is scheduled.

## 7 · Relationship to LC-M04-EXIT

`C7` requires that *no ECR against the frozen specification remains undispositioned* at gate
time. **This ECR is such an item and therefore blocks `C7` until dispositioned.** It is
recorded here rather than deferred, because deferring it would clear the gate against the four
known defects while a fifth sat open — which is the precise failure `C7` exists to prevent.

## 8 · Disposition — **A**, on the five requested actions

Ruled by `human-owner`, `S-2026-08-10-01`, approval [`APR-020`](../approvals/APR-020_Cooling_Plate_coherence_package.md).

| Action | Ruling | Where it landed |
|---|---|---|
| **1** — keep-out row | **Kinematic locators: keep-out radius 8.5 mm from the feature axis (5.0 counterbore radius + 3.5 wall), minimum wall to channel 3.5 mm.** Built on the same basis the table already uses for the M5 choke and M6 ring holes. The radius follows the Ø10.000 counterbore action 3 settled on | `spec/01` §3.1 |
| **2** — the 3.35 mm wall | **Rejected, and answered rather than excepted.** Satisfying action 1 pulls the channel outer limit to r ≤ 121.5 at the Ø260 BC stations, leaving the M4 tap drill (inner edge r = 128.35) **6.85 mm** of wall. The 3.35 mm figure was measured against a channel limit the new row forbids | `spec/01` §3.1 |
| **3** — the 1.00 mm annular wall to the OD | **Rejected, and dispositioned here** — locator flange and counterbore Ø12.000 → **Ø10.000** at both stations, taking the wall from 1.00 mm (0.95 worst case) to **2.00 mm** (1.93 worst case). See §9 | `spec/01` `CP-D09`/`CP-D10`, `spec/06` `AP-D03` |
| **4** — SEWCP-300 slot depth | **`HP-D09a` = 3.00 ± 0.10**, matching `SR-D19` and `AP-IF-3`, giving 0.35 mm worst-case clearance on the 2.50 ± 0.05 boss. **The depth was not the defect** — see `ECR-D-011` | `spec/02` `HP-D09a` |
| **5** — M4 tap depth | **`CP-D09a` = `CP-D10a` = M4 × 0.7, Ø3.30 drilled 7.80 max to the drill point below the counterbore floor, 5.00 min full thread, bottoming tap** | `spec/01` `CP-D09a`, `CP-D10a` |

**Why 7.80 and not 5.00.** The 5.00 governs the *thread*; the *drill* must go deeper. 0.99 mm
of 118° drill point + 1.05 mm of bottoming-tap chamfer + 0.70 mm of chip relief = 2.74 mm of
allowance. A callout of 5.00 mm alone is not producible, and the gap between thread depth and
drilled depth is exactly where a shop substitutes its own number.

**Both stations, separately checked.** At the **top** locator 5.00 mm of full thread stops
exactly at `CP-D07`'s 8.00 mm wall, and radial separation is action 1's row. At the **bottom**
locator there is no channel at r = 153, but the thread crosses the FSW lid/body plane at
z = 6.00. That is accepted on the precedent already in the volume — `CP-D20` M6 × 12 deep at
r = 151 and `CP-IF-8` M6 × 12 deep at r = 137 both cross it — with a note requiring a
circumferential weld pass at or outboard of that bolt circle, since a thread tapped into an
unwelded faying gap would vent it to vacuum.

## 9 · Requested action 3 — rejected, and why the ground matters

The 1.00 mm nominal / 0.95 mm minimum annular wall is **rejected**, but **not on the ground this
record originally implied**, and the difference is the point. Hoop stress from the Ø12.000 k6
interference computes to **40–63 MPa against 276 MPa yield** — a factor of 4.4 to 6.9. A
reviewer who recomputes the stress will find the wall comfortable and could undo the rejection
in good faith. **The rejection rests on process**, and each ground below is independent of the
fit:

- **Machinability.** The ligament is a 3.00 mm tall cantilever strip. At a 1.00 mm wall it deflects **13–26 µm** under a 50–100 N boring force and its root yields at **92 N**; at the 0.90 mm worst case, 18–36 µm and 75 N. **The Ø12 H7 tolerance band is 18 µm.** An ordinary finishing force consumes the entire band or takes permanent set that no later pass corrects.
- **Masking.** §8 requires the counterbore masked and the OD anodized, with those boundaries 0.90–1.00 mm apart against a practical masking placement of ±0.2–0.5 mm.
- **Anodize integrity.** 50 µm of brittle Type III on a 0.90 mm ligament, hoop-loaded and cycled through 130 K, on the RF-hot body whose dielectric it is.

**`ECR-D-009`'s disposition removes the interference** — the flange became `h6` clearance,
because a part that is screwed in cannot be pressed — so the stress term goes to zero. **None of
the three objections above goes with it.**

### The remedy, ruled by the human owner `S-2026-08-10-01`

**Flange and counterbore Ø12.000 → Ø10.000 at both locator stations**, keeping all six locators
one part number.

| | Ø12.000 | **Ø10.000** |
|---|---|---|
| Bottom-station wall to OD (axis r = 153, OD r = 160 / 159.95 min) | 1.00 / 0.95 | **2.00 / 1.93** |
| Ligament deflection at 100 N | 13–26 µm against an 18 µm band | **≈ 3.3 µm**, under 20 % of the band |
| Top-station counterbore inner edge (axis r = 130) | r = 124.0 — **1.00 mm inside** the Ø250 annulus | **r = 125.0 — flush**, closing the §3.2 overlap |
| Flange fit clearance | h6 in H7, 0 to 0.029 | h6 in H7, **0 to 0.024** — marginally tighter |
| §9 positional RSS | 0.0414 of 0.050 | **0.0414 of 0.050** — unchanged; the 0.038 slot clearance dominates |

**No ceramic drawing changes and no datum moves** — Datums B and C are the Ø306 BC counterbores
themselves, whose bolt circle is untouched. Options **B** (bottom bolt circle Ø306 → Ø300, which
moves Datums B and C and reopens `SR-IF-4`/`SR-D20` in the alumina ring), **C** (both changes,
wall 5.00 mm) and **D** (accept 1.00 mm behind a process qualification) were presented and not
approved.

**No `ECR-D-012` was raised.** An earlier draft of this section proposed splitting action 3 out
as a separate, undispositioned ECR. That would have cleared the gate against eight known defects
while a ninth sat open — the precise manoeuvre `C7` exists to prevent, as `GATES.md` says in
terms. The action is dispositioned here instead.
