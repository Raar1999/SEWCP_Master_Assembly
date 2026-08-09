# ECR-D-001 — Alignment pin interface specified two mutually exclusive ways

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised against the frozen Rev A specification. Blocking `LC-M04-EXIT` criterion `C1`.

```yaml
ecr_id:       ECR-D-001
class:        D                      # defect - LAW-02: a defect stops the affected work
raised_by:    project-manager · S-2026-08-08-01
status:       VERIFICATION-PENDING   # not CLOSED until C6 independent verification passes
disposition:  A - SEWCP-700 GOVERNS; CORRECT SEWCP-200
ruled_by:     human-owner · S-2026-08-09-14
approval:       approvals/APR-018_Strike_Unauthorised_Tap_Depth.md
approval_chain: APR-016 -> APR-017 -> APR-018   # each supersedes the last; APR-018 is terminal
# LIVENESS IS NOT ASSERTED HERE. VER-010 V1: this field twice named a superseded approval
# and twice labelled it LIVE, because the label was written by hand and never rechecked when
# the next edit voided it. Determine liveness by recomputing DC-1 of the terminal approval's
# subject_path and comparing with its subject_hash - a claim that cannot go stale.
raised_at:    2026-08-08T01:31:23Z
closed_at:    null                   # set on independent verification PASS
residual:     three - see §7   # VER-010 F11: this field read `none` while §7 read "Not none"
```

---

## 1 · Class

**D — defect.** Not an ambiguity requiring interpretation: two frozen volumes specify
geometry for the same feature on the same face of the same part, and the two cannot both be
machined. Under LAW-02 a defect stops the affected work — here, SEWCP-200 CAD.

## 2 · Affected artifacts

| Artifact | Role in the defect |
|---|---|
| `spec/01_SEWCP-200_Cooling_Plate.md` | Specifies a press-fit dowel bore. **Corrected by this disposition.** |
| `spec/06_SEWCP-700_Alignment_Pins.md` | Specifies a screw-retained shouldered locator. **Governs; unchanged.** |
| `spec/03_SEWCP-400_Chuck_Support_Ring.md` | Carries the mating slot. Consistent with SEWCP-700; unchanged. |
| `spec/02_SEWCP-300_Heater_Plate.md` | Carries the mating slot. Consistent with SEWCP-700; unchanged. |
| `.ai/project/FROZEN.md` | Registers `spec/01`; re-registered at the corrected digest. |
| `.ai/project/STATE.md` `frozen_set_hash` | Derived from the aggregate; recomputed. |

## 3 · Evidence

Every line below is a quotation from the frozen specification and is reproducible from the
repository alone.

**3.1 The two geometries.**

| Volume | Feature | As specified |
|---|---|---|
| SEWCP-200 `CP-D09` / `CP-D10` | Kinematic dowel bore, bottom Ø306 BC / top Ø260 BC | **Ø6.000, H7 / press M6**, Critical |
| SEWCP-200 `CP-IF-1` / `CP-IF-4` | To Support Ring / Heater Plate | *"3× Ø6 h6 dowels **press-fit** into the … face"* |
| SEWCP-700 `AP-IF-1` | Locator to Cooling Plate | **Ø12.0 k6 flange in a Ø12.0 H7 × 3.0 counterbore**; **M4 × 10 SHCS** through the pin into the plate |
| SEWCP-700 `AP-D02` | Boss protrusion | **2.50 ± 0.05 mm** |

A Ø6.000 H7 press bore and a Ø12.0 H7 × 3.0 counterbore over an M4 tapped hole cannot occupy
the same location on the same face.

**3.2 The specification as written could not be assembled.** SEWCP-200 §10 step 3 directs
*"Press-fit the 6 alignment dowels … Verify protrusion **5.0 ± 0.1 mm** each."* The mating
slots are **3.00 mm deep** (`SR-D19`). A 5.0 mm protrusion into a 3.00 mm slot **bottoms out
by 2.0 mm.** SEWCP-700 §5.1 states the consequence in terms: a boss that bottoms *"would hold
the mating faces apart — destroying the thermal choke contact, the flatness budget, and the
joint preload simultaneously."* This is a physical impossibility, not a documentation
mismatch.

**3.3 SEWCP-200 encoded the alternative SEWCP-700 had evaluated and rejected.** SEWCP-700 §6:
*"Plain press-fit dowel — **Rejected on thermal grounds.** A Ti dowel in a 6061 hole loses
5.4 µm of interference over ΔT = 60 K … the joint can approach zero interference hot — and a
loose dowel in a vacuum chamber is a migrating hard particle."*

**3.4 The mating volumes already matched SEWCP-700 in the dimensions they state.**
`SR-D17`–`SR-D20` specify 6.05 H8 W × 8.00 L × **3.00 D** slots; `HP-D09`–`HP-D11` specify
6.05 H8 W × 8.00 L and a position, and **state no depth**. Both mate with a Ø6.000 h6 boss and
with nothing else.

> **Corrected, `VER-010` F10.** The first form of this paragraph asserted that
> `HP-D09`–`HP-D11` specify 3.00 D. They do not: the Heater Plate volume states no slot depth
> anywhere, and the only source of 3.0 D at Ø260 BC is `AP-IF-3` in SEWCP-700 itself.
> Clearance at the Ø260 BC interface is therefore **undecidable from the host volume** and is
> verifiable only by importing a number from the governing volume. That is a real gap; it
> pre-dates this ECR, is not created by it, and is carried into the split ECR below.

## 4 · Impact

Blocks SEWCP-200 CAD: a modeller cannot proceed without choosing between two geometries, and
choosing is a Design Authority act. Blocks `LC-M04-EXIT` criterion `C1`.

## 5 · Requested action

Rule which volume governs the alignment-pin interface geometry, and correct the other.

## 6 · Disposition — **A**

**SEWCP-700 governs. SEWCP-200 is corrected to the screw-retained shouldered locator.**
Ruled by `human-owner`, session `S-2026-08-09-14`, approval
[`APR-016`](../approvals/APR-016_Alignment_Pin_Interface_Geometry.md).

**Basis recorded, not inferred.** SEWCP-700 carries the quantified derivation — thermal
interference loss, wear pairing against 1,600 HV alumina, retention, serviceability, and the
128× shear margin that justifies 2.50 mm engagement. SEWCP-200's rows carry no derivation and
encode the rejected alternative. Two further frozen volumes already carry mating geometry
that fits only Option A, so this correction makes one volume consistent with three; the
converse would have propagated into the alumina ring and the heater plate, including
deepening slots in ceramic.

### 6.1 Executed changes — `spec/01_SEWCP-200_Cooling_Plate.md` only

| Ref | Was | Now |
|---|---|---|
| `CP-D09` | Kinematic dowel bore (bottom), Ø6.000, H7 / press M6 | Kinematic locator counterbore (bottom), Ø12.000, H7, × 3.00 deep |
| `CP-D10` | Kinematic dowel bore (top), Ø6.000, H7 / press M6 | Kinematic locator counterbore (top), Ø12.000, H7, × 3.00 deep |
| `CP-D09a` / `CP-D10a` | — | **New.** M4 × 0.7 tapped hole, **depth TBD — `ECR-D-007`**, coaxial under each counterbore. (An 8.0 mm depth was executed here and **struck** under `APR-018`; `VER-010` V2 found this row still stating it.) |
| `CP-IF-1` | 3× Ø6 h6 dowels press-fit into the bottom face | 3× SEWCP-700 locators, flange seated in Ø12.0 H7 × 3.0 counterbores, M4 × 10 SHCS retained |
| `CP-IF-4` | 3× Ø6 h6 dowels press-fit into the top face | as above, top face |
| Mating table | *"Hosts 6 press-fit dowels (3 down, 3 up)"* | *"Hosts 6 screw-retained locators (3 down, 3 up)"* |
| §6 step 12 | Press-fit 6× alignment dowels | Install 6× locators; torque M4 SHCS to 2.5 N·m |
| §10 step 3 | Press-fit … verify protrusion **5.0 ± 0.1** | Install … verify boss protrusion **2.50 ± 0.05** above the seated flange face |

`CP-D11`'s positional tolerance (⌖ Ø0.020 Ⓜ) is unchanged in value; it now applies to the
counterbore, which is what `AP-D03`/`AP-D09` were designed to exploit.

### 6.1a Consequential corrections in the same volume — recorded, not silent

The approval names the geometry rows. Nine further references in `spec/01` described the same
feature by its old identity, and leaving them would have made the volume internally
inconsistent and handed the modeller the ambiguity this ECR exists to remove. They are
corrected under the same disposition and listed here so the change set is complete on the
record rather than discoverable only by diff. **`VER-010` F13 found this table itself
incomplete — the `CP-D11` label and the §10 step 7 edits were executed and not listed. Both
are nomenclature-only with no dimensional effect, and both are added above.**

| Location | Was | Now |
|---|---|---|
| §Datums, **Datum B** | *"the Ø306 BC kinematic **dowel** at 60°"* | *"the Ø306 BC kinematic **locator counterbore** at 60°"* |
| §Datums, **Datum C** | *"… **dowel** at 180° (clocking)"* | *"… **locator counterbore** at 180° (clocking)"* |
| §GD&T, Position row | Kinematic **dowel bores** | Kinematic **locator counterbores** |
| §6 step 13 (masking) | mask *"dowel bores"* | mask *"locator counterbores and their M4 threads"* |
| §Critical dimensions, `CP-D11` row label | Kinematic **dowel bolt-circle** position | Kinematic **locator counterbore** position |
| §10 step 7 (assembly) | *"the 3 bottom **dowels** … each **dowel** slides freely"* | *"the 3 bottom **locator bosses** … each **boss** slides freely"* |
| §8 Surface finish table | *"Dowel bores … Press-fit dimensional integrity"* | *"Locator counterbores and M4 retention threads … Flange seating and thread integrity"* — **added under `APR-017`; see F1 below** |
| §Tolerance philosophy | *"kinematic **dowel** position"* | *"kinematic **locator** position"* (2 places) |
| §Design rationale (choke fastener holes) | *"located by the three kinematic **dowels**"* | *"located by the three kinematic **locators**"* |

**Datum B and Datum C are the substantive ones.** A datum must be a feature of the part being
toleranced. Under the superseded text they named a dowel — a *separate part* — which was
already a defect in its own right; under the corrected geometry the plate's own feature is the
counterbore, so the datum now names something the Cooling Plate actually has. The tolerance
values are unchanged.

No other volume is touched: `git diff --name-only spec/` returns
`spec/01_SEWCP-200_Cooling_Plate.md` alone.

> **CORRECTED — `VER-010` F1 and F2, and this is the most important correction in this
> record.** The first form of this paragraph claimed *"After these corrections the word dowel
> does not appear in `spec/01`."* **That was false when written.** §8's surface-finish table
> still read `| Dowel bores | Ra ≤ 0.8 µm, masked | Press-fit dimensional integrity |` — the
> superseded geometry, surviving inside a manufacturing table and contradicting §6 step 13 of
> the same volume.
>
> The claim was produced by a **case-sensitive** `grep -c "dowel"` returning 0 against text
> reading `Dowel`. A completeness assertion was published on the strength of a check too weak
> to support it, and that assertion is precisely what would have stopped a reviewer
> re-checking. The row is corrected under `APR-017`; the claim is re-made only as a
> case-insensitive measurement, `grep -ci` → **0**.

### 6.2 Interference check performed for the added tapped holes

> **WITHDRAWN IN FULL — `VER-010` F5.** The interference check that stood here was
> wrong in its inputs and must not be relied on. It read: *"`CP-D07` fixes the
> channel-to-top-face wall at 8.00 ± 0.20 mm and `CP-D06` the channel depth at 8.00 mm, in a
> plate of **26.00 mm overall (`CP-D01`)**."*
>
> `CP-D01` is **Outside diameter Ø320.0**, not a thickness. Overall thickness is `CP-D02` =
> **20.000 ± 0.030**. The value 26.00 appears nowhere in `spec/01`. The only check this ECR
> performed on the feature it added therefore overstated the available material by 30 %, and
> it was authored, not measured.
>
> It is withdrawn rather than corrected here, because a correct assessment requires
> engineering values this ECR has no authority to set. The geometric consequences of the
> Ø6.000 → Ø12.000 enlargement are split into **ECR-D-007** under `APR-017` (Option B) and
> are dispositioned there, not here.

### 6.3 Constraint passed to SEWCP-200 CAD

> The M4 locator tapped holes at Ø306 BC (bottom, 60°/180°/300°) and Ø260 BC (top,
> 30°/150°/270°), beneath a 3.00 mm counterbore, **shall not break into the coolant
> circuit.** Their **depth is undetermined** — `ECR-D-007` requested action 5 — and the
> channel routing shall be laid out to clear them once it is set.

> **`VER-010` V3.** This constraint previously handed CAD the figure *"8.0 mm deep … =
> 11.0 mm below the top face"* — the exact unauthorised value `APR-018` had been issued to
> strike from `spec/01`. Deleting a number from the specification while leaving it in the
> instruction the modeller reads removes nothing. The number is gone from both.

**This constraint lives in an ECR, and the modeller reads the specification.** `VER-010`
F4 recorded that as a defect in its own right: `spec/01` §3.1 carries a keep-out radius and a
minimum wall for every other feature and **has no row for the kinematic locators** — and never
did, for either geometry. Writing that row requires engineering values, so it is dispositioned
in **ECR-D-007**, not asserted here.

## 7 · Residual

**Not none.** The first form of this section recorded `residual: none`; `VER-010` F11
and F10 falsified that. The residuals are:

| Residual | Nature | Disposition |
|---|---|---|
| `spec/03` `SR-IF-4` and line 103, `spec/02` `HP-IF-3` still describe the locators as *"Ø6 h6 dowels **pressed into** the Cooling Plate"* | Retention **method** stated three ways across the frozen set. The **slot geometry** is consistent, so no geometric ambiguity results | Left unchanged **as the approval requires** (those volumes are out of scope). Recorded as a residual, not as consistency |
| `spec/02` states **no slot depth** at the Ø260 BC interface | Clearance there is undecidable from the host volume | Carried into `ECR-D-007` |
| §3.1 keep-out table has no kinematic-locator row; 1.00 mm OD wall at Ø306 BC; 3.35 mm vs the 3.5 mm demanded of analogous features | Geometric consequences of the approved Ø12.000 counterbore, unassessed by any volume | **Split to `ECR-D-007`** under `APR-017`, Option B |

Two further adjacent defects were found while gathering evidence. They are **not folded in**,
and — `VER-010` R8(b) — the first form of this section claimed one of them was *"raised
separately"* when **no such ECR existed anywhere in the repository**. That was a status claim
published without the fact behind it, which is the same defect as F2 one paragraph earlier.
Both are now actually filed:

* **`ECR-D-008`** — the ICD (`spec/00` §Materials) lists SEWCP-700 as **316L** while
  SEWCP-700 §7 specifies **Ti-6Al-4V Grade 5** and §6 rejects 316L on quantified wear and
  CTE grounds. A material conflict, not geometry, and outside this ECR's requested action.
* **`ECR-D-009`** — `AP-D08` specifies a Ø8.0 × 2.2 screw-head counterbore while the screw
  enters through the `AP-D01` **Ø6.000** boss. A Ø8.0 counterbore cannot exist in a Ø6.000
  boss, and a bare M4 SHCS head is Ø7.0 across. Retention, not locating geometry.

Both are registered in `OPEN_ITEMS.md` and `OPEN_ITEMS_REGISTER.md` and both block `C7`.
`VER-010` V8 found this paragraph spliced mid-sentence, announcing two defects and
describing one.
