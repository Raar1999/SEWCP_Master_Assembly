# VER-015 — Independent Verification of ECR-D-002, ECR-D-003, ECR-D-004 and the LC-M04 Specification Coherence Package

> **Instance artifact.** Partition `project`. Owner `qa-engineer`.
> One cold-context round against session `S-2026-08-10-01`. Every number below was
> recomputed by this verifier from repository bytes. No claim in any record was adopted.

```yaml
verification_id: VER-015
subject:         ECR-D-002, ECR-D-003 and ECR-D-004 dispositions and their implementation, together with the LC-M04 specification coherence package APR-020..APR-026 and the ECR-D-007, ECR-D-009, ECR-D-010, ECR-D-011 dispositions carried in it
verifier_role:   qa-engineer
author_role:     chief-systems-engineer
law:             LAW-05 - the verifier authored none of the work under audit and obtained its own evidence
status:          VERIFIED WITH FINDINGS - NOT CLEARED. 7 PASS, 4 FAIL
session:         S-2026-08-10-02
```

---

## 0 · Measurement instant, and a warning about it

**The repository was not quiescent during this audit.** `.ai/project/FROZEN.md` was rewritten at
`10:38:11 IST` and `.ai/project/STATE.md` at `10:37:01 IST`, both **after** this session began
reading them. A measurement taken at the start of this session found `FROZEN.md` publishing an
aggregate (`c56e75bc…`) that disagreed with `STATE.md` (`55904b93…`); a measurement taken at
`10:46` found them agreeing at `55904b93…`, with `c56e75bc…` demoted to a recorded prior value.
The defect was real when measured and was repaired under this verifier's feet.

Every disposition below is therefore taken against an **immutable snapshot** of the working tree
copied out at **`2026-08-10T05:16:21Z`** (`10:46:21 IST`). All tool runs and all recomputations
reported below were executed against that snapshot unless explicitly stated. A reader who
re-runs these numbers against a later tree may get different answers; that is a property of the
repository, not of this report.

**This is itself a finding (F-14).** A gate whose evidence is produced by a verifier reading a
tree that a second party is concurrently editing is not evidence of the tree that will be
modelled.

## 0a · What filing this report does to the gate, stated before anything else

`aief_gate` `C6` passes an ECR when *some* `VER-*.md` file declares that ECR in its `subject`
field and its `verifier_role` differs from its `author_role`. Both conditions are satisfied by
the yaml block above. **Filing this file will therefore flip `C6` to PASS and the gate line to
`LC-M04 CAD-READY: YES`, while this report records four FAIL dispositions.**

That is a machine limit the checker itself declares (`C6` residue line: *"MACHINE LIMIT …"*), not
an endorsement. **This verification does not clear `LC-M04-EXIT`.** The four FAILs at §5, §8, §9
and §11 stand and are owned as listed in the findings table. The same limit already applies to
`ECR-D-001`, whose `C6` evidence is `VER-014` — a report whose own four rounds are recorded
`FAIL` and whose §6 verdict reads *"ECR-D-001 is NOT CLOSED after four rounds."*

## 1 · Scope and method

| In scope | Out of scope |
|---|---|
| `spec/**` as it stands, all eleven volumes | CAD, Fusion 360, the implementation packages |
| `ECR-D-002`, `-003`, `-004`, `-007`, `-009`, `-010`, `-011`; `APR-016`…`APR-026` | The Stage 6 compiler track, except where its checks bear on the freeze registry |
| `FROZEN.md`, `STATE.md`, `OPEN_ITEMS*.md`, the `aief_*` tooling | The engineering *choices* — only whether they reproduce and were applied |

Method: recomputation. DC-1 and DC-2 were re-implemented from the construction text in
`FROZEN.md` § *Hash constructions* in a standalone script, not by calling the repository's own
`aief_stage6.digests`, so a defect in that module cannot hide behind itself. Geometry, stress and
torque were recomputed from first principles with this verifier's own assumptions, stated where
they matter. Gate and clearance behaviour were probed by mutation in a temporary copy under
`%TEMP%`; **the repository was not modified by this session other than by the creation of this
one file.**

---

## 2 · V1 — ECR-D-002 completion

### What I did

Read `spec/01` §6 step 3 directly; swept all eleven `spec/**` volumes for each stale token named
in the criterion; recomputed `spec/00` §4.3 row by row and summed the column myself.

### Evidence

**§6 step 3 (`spec/01` line 173)** reads:

> `10 W × 6 D (CP-D05 × CP-D06), R5 minimum bend radius … Deepen to 10 D at the two port pockets per CP-D25, ramped back to 6 D over 15 mm`

**6 D, not 8 D.** The machining instruction now agrees with `CP-D06`.

**Sweep.** `grep` over `spec/**` for `8 D`, `80 mm²`, `0.83`, `7,400`/`7400`, `8.89`, `5,000 W`/
`5000 W`, `0.09 m`, `0.18 L`, `3.9 kg`, `8.0 mm D`, `8.00 mm D` returns **zero hits**. Every
survivor of a broader `× 8` sweep is legitimate and I cleared each by inspection:

| Survivor | Why it is not stale |
|---|---|
| `CP-D07` = 8.00, and `spec/00` §4.3 *"Cooling Plate to channel, 8 mm"* | Channel-to-top-face wall. Independently confirmed: `R = 0.008/(167 × 0.0707) = 0.000678` reproduces the tabulated `0.00068` |
| `HP-D02` = 8.000, `Ø300 × 8.00` in the `spec/00` and `spec/README` stack diagrams | Heater Plate thickness |
| `6.05 H8 W × 8.0 L` in `spec/02`, `spec/03`, `spec/06` | Kinematic slot radial length |
| `M4 × 8 deep` (`CP-IF-9`), `Ø9.9 h8 pilot spigot × 8.0` (`VP-IF-1`), `× 8,000 kg/m³` (`spec/09`) | Unrelated features and a density |

**`spec/00` §4.3, recomputed:**

- `R_conv = 1/(6500 × 0.080) = 0.00192308` → tabulated **0.00192** ✔
- `ΔT = 0.00192 × 300 = 0.576` → tabulated **0.6 K** ✔
- Column sum `0.0118 + 0.00283 + 0.00377 + 0.00068 + 0.100 + 0.00068 + 0.00192` = **0.12168** → tabulated **0.1217** ✔
- `ΔT_total = 0.12168 × 300 = 36.504` → tabulated **36.5 K** ✔
- `0.1217` rounds to **0.122 K/W**, which is what `spec/00` §4.3's governing relation, `spec/README` and `program/SEDEP-PMP-001/-002` all quote ✔

### Finding raised while doing this

**F-01 (LOW).** The `0.080 m²` wetted area does not reproduce from its own stated derivation.
`spec/01` §2.1 gives the derivation as *"Path × perimeter (perimeter 36 → 32 mm)"* with path
**≈ 2.2 m**; `2.2 × 0.032 = 0.0704 m²`, not 0.080. The 0.080 is the superseded `0.09` scaled by
`32/36 = 0.889` — consistent with the same section's *"wetted area falls ≈ 11 %"* note, but not
with the derivation column. The pre-change `0.09` was itself 14 % above `2.2 × 0.036 = 0.0792`,
so this is a **pre-existing inaccuracy carried forward at scale, not one introduced here**.
Effect: at `A = 0.0704`, `R_conv = 0.002185` and the column total becomes `0.12195` → `0.1219`,
which **still rounds to 0.122**. No downstream figure moves.

**F-02 (LOW, outside `spec/**`).** `program/SEDEP-PMP-001_Program_Management_Plan.md` line 655
still reads `Re 7,400` and line 257 still reads *"the 36.6 K rise at 300 W"*. Both are superseded
(`8,300` and `36.5 K`). `program/` is PR-controlled, not frozen, and no approval covered it.

### Disposition

Every element the criterion names reproduces and the sweep is clean.

**PASS**

---

## 3 · V2 — ECR-D-003 arithmetic

### What I did

Built the through-thickness band table from `spec/01` §5 alone, without reading ECR-D-003's own
version of it; then tested each claim against it.

### Evidence

From `CP-D08` = 6.00 (FSW lid), `CP-D06` = 6.00 (channel), `CP-D07` = 8.00 (wall to top face),
`CP-D02` = 20.000 (overall). Datum A is the bottom face (`spec/01` §9). The channel is milled
into the **body's** bottom face and closed from below by the lid, so above Datum A:

| Band | Extent | Member | Check |
|---|---|---|---|
| 0.00 – 6.00 | 6.00 | FSW lid `CP-D08` | |
| 6.00 – 12.00 | 6.00 | Channel `CP-D06` | |
| 12.00 – 20.00 | 8.00 | Wall `CP-D07` | |
| | **20.00** | | **= `CP-D02` 20.000 ✔ the Z stack closes** |

- **Bore span.** `CP-D23` = 11.00, Ø10.0 → `11.00 ± 5.00` = **6.00 to 16.00**.
- **Deepened channel.** `CP-D25` = 10.00 measured from the same datum as `CP-D06`, i.e. from z = 6.00 → **6.00 to 16.00**. **Identical. Coaxial, no step.** ✔
- **FSW lid.** Lid occupies 0.00–6.00. Bore bottom sits at exactly 6.00. At **nominal** the bore does not penetrate the lid. ✔
- **Local top wall.** `20.00 − 16.00` = **4.00 mm** ✔
- **Bending stress.** `p = 6 bar = 0.6 N/mm²`, `L = 10`, `t = 4.00`. `M = pL²/8 = 0.6 × 100/8 = 7.5 N·mm/mm` ✔. `σ = 6M/t² = 45/16 = ` **2.8125 MPa** → the spec's **2.8 MPa** ✔. Against 276 MPa yield that is **98×**, i.e. the spec's *"order 100×"* ✔
- **Flow area.** `π × 5² = ` **78.54 mm²** > the channel's **60 mm²** ✔ — the port is not the restriction, as claimed

### Finding raised while doing this

**F-03 (MEDIUM).** *"The bore therefore never penetrates the lid"* (`ECR-D-003` §6.2) is a
**nominal** statement and no tolerance analysis supports it. `CP-D23` is **11.00 ± 0.10** and
`CP-D22` is **Ø10.0 H9** (`+0.036/0`, so radius up to 5.018). Worst case the bore's lower edge
sits at `11.00 − 0.10 − 5.018 = 5.882`, and `CP-D08` is **6.00 ± 0.10** so the lid's upper
surface can be as high as 6.10. **At the tolerance limits the bore cuts up to 0.218 mm into the
FSW lid — through the weld plane, in the pressure boundary, at the two coolant ports.** The
volume treats that plane as significant everywhere else it is crossed (`CP-D09a`'s note requires
a circumferential weld pass at or outboard of its bolt circle for exactly this reason). Nothing
in `spec/01` or `ECR-D-003` addresses it at the ports. Owner: Design Authority.

### Disposition

Every arithmetic claim the criterion names reproduces exactly.

**PASS** — with F-03 recorded against the tolerance case, which is not what the criterion asked
and is not what the record claims to have analysed.

---

## 4 · V3 — ECR-D-004 arithmetic

### What I did

Reproduced the grip relation from `CP-D02` and the stated stack terms; checked both fastener
lengths; checked the `HP-D12` depth budget, the counterbore keep-out and both `spec/00` §9 rows.

### Evidence

`grip = 0.6 (Belleville working height) + (20.000 − d) + 1.500 (Ti choke washer) = 22.100 − d`,
`e = L − grip = L − 22.100 + d`.

| Case | grip | `e` | Verdict |
|---|---|---|---|
| `d = 2.5`, `L = 25` | 19.600 | **5.400 mm** | ✔ reproduces the record exactly |
| `d = 0`, `L = 30` | 22.100 | **7.900 mm** | ✔ into an `HP-D02` 8.000 mm plate — **0.100 mm** of material left |

**`M5 × 30` is unbuildable at every counterbore depth.** `e = 7.900 + d` is monotonically
increasing in `d`, so `d = 0` is the *best* case and it already leaves 0.100 mm before the
`HP-IF-4` bond face. Any counterbore makes it worse. The record's central claim is confirmed
independently.

- **`HP-D12`.** `8.000 − 6.50 = ` **1.50 mm** to the bond face ✔ — and `spec/02` `HP-D12` now states exactly that, blind from the choke face, criticality High.
- **`CP-D26` keep-out.** Slot half-length `12.5 / 2 = ` **6.25 mm** < the §3.1 *"Choke fastener holes … 8 mm"* keep-out radius ✔ — the counterbore fits inside the keep-out already declared, so **coolant routing is unaffected**.
- **`spec/00` §9.** Both choke rows now read **`M5 × 25 SHCS`** — outer (12 off) and inner (4 off) ✔. The false *"Slotted clearance holes in Heater Plate"* note is corrected to the Cooling Plate ✔.
- **Cross-checks I ran that the criterion did not ask for, all reproducing:** head protrusion `5.0 + 0.6 − 2.5 = 3.1 mm`; counterbore half-angle at Ø270 BC `asin(5.5/135) = 2.3349°`, so the 90° station reaches `92.335°` and clears the RF land at 93° by `0.665° = 1.567 mm` at r = 135 (record: 0.67° ≈ 1.58 mm).

### Finding raised while doing this

**F-04 (MEDIUM).** The new stack engages **5.400 mm** = **1.08 × D** of thread. `spec/01` §11
FM #11's mitigation column — unchanged by this package and still live in the same frozen volume —
reads *"min **2×D** thread engagement"*, i.e. 10 mm for M5. The insert-to-aluminium path over the
6.50 mm tapped depth is 1.3 × D, also short. `ECR-D-004` §6.2 computes thread shear
(≈ 42 mm²) and pull-out and concludes the insert is not the weak element, but **it never
reconciles the change with FM #11's standing rule and no approval amends that row.** A frozen
volume now carries a mitigation its own approved fastener stack does not meet. Owner: Design
Authority — either amend FM #11 or record the departure.

### Disposition

Every number the criterion names reproduces to the digit.

**PASS**

---

## 5 · V4 — ECR-D-007

### What I did

Recomputed the §3.1 keep-out row, the channel limit, the tap-drill wall, the tap-depth allowance
and the annular wall from `spec/01`'s own dimensions; then compared the specification against the
`ECR-D-007` record.

### Evidence — the specification

- **Keep-out radius.** `spec/01` §3.1: *"**8.5 mm** from the feature axis (5.0 counterbore radius + 3.5 wall)"*. `CP-D09`/`CP-D10` are **Ø10.000** → radius 5.0; `5.0 + 3.5 = 8.5` ✔ Constructed on the same basis as the M5 choke row (8 mm) and the M6 ring row (9 mm) ✔
- **Channel limit.** Locator axis at Ø260 BC → r = 130. `130 − 8.5 = ` **r ≤ 121.5** ✔
- **Tap-drill wall.** Ø3.30 tap drill → radius 1.65; inner edge `130 − 1.65 = ` **128.35** ✔. Wall `128.35 − 121.5 = ` **6.85 mm** ✔
- **Tap callout.** `5.00 + 0.99 + 1.05 + 0.70 = ` **7.74**, specified **7.80 max** ✔. Each allowance independently checks: a Ø3.30 drill at 118° gives a point length of `1.65 / tan 59° = ` **0.9914** ✔; a bottoming tap chamfer of 1.5 threads is `1.5 × 0.7 = ` **1.05** ✔; chip relief of one pitch is **0.70** ✔
- **`CP-D09` / `CP-D10`.** Both read **Ø10.000 H7** ✔
- **Annular wall at Ø306 BC.** Axis r = 153; plate OD Ø320.0 ±0.10 → r = 160.00 ±0.05. Counterbore outer edge `153 + 5.0 = 158.00`; wall `160.00 − 158.00 = ` **2.00 mm nominal** ✔. Worst case with OD at 159.95, H7 at `+0.015` (radius `+0.0075`) and `CP-D11` position `Ø0.020` (radial 0.010): `159.95 − 158.0075 − 0.010 = ` **1.9325 → 1.93 mm** ✔

Every specification-side number the criterion names reproduces.

### Findings raised while doing this — the record does not match the specification

**F-05 (HIGH).** `ECR-D-007` §8's disposition table states numbers the specification does not
carry, and states an outcome the specification contradicts:

| `ECR-D-007` §8 says | `spec/01` §3.1 / §5 says |
|---|---|
| keep-out radius **9.5 mm** (**6.0** counterbore radius + 3.5 wall) | **8.5 mm** (**5.0** + 3.5) |
| channel outer limit **r ≤ 120.5** | **r ≤ 121.5** |
| tap-drill wall **7.85 mm** | **6.85 mm** |
| action 3 (the 1.00 mm annular wall) **"Rejected — and split out"**, carried by `ECR-D-012` | `CP-D09`: *"**Reduced from Ø12.000 by ECR-D-007 action 3**"* — i.e. **implemented** |

The §8 table is written for the **Ø12.000** counterbore, which action 3 replaced. §9 then argues
the rejection from *"Hoop stress from the Ø12.000 k6 interference"* — a fit that `ECR-D-009`
struck. The record and the frozen artifact disagree about what was decided.

**F-06 (HIGH).** **`ECR-D-012` does not exist.** `ECR-D-007` names it four times — in the yaml
`residual` field, in the §8 action-3 row, in the §9 heading and in §9's closing sentence — as the
carrier of a rejected requested action. There is no `.ai/project/ecr/ECR-D-012*` file, no entry in
`OPEN_ITEMS.md` and no entry in `OPEN_ITEMS_REGISTER.md`. This is the *cited-but-not-filed*
defect `VER-014` §0 exists to record, recurring. Owner: `chief-systems-engineer`.

### Disposition

The criterion is scoped to the specification's arithmetic, and all of it reproduces.

**PASS** — F-05 and F-06 are dispositioned under V11, where record accuracy is the criterion.

---

## 6 · V5 — ECR-D-009

### What I did

Checked every head diameter against the published standards; recomputed the boss wall; and
recomputed both torque claims under **my own** friction assumptions rather than adopting any.
Then checked whether the ruled torque is actually in the specification.

### Evidence — head diameters

| Screw | Standard | dk (published) | `ECR-D-009` | Counterbore at dk + 0.3 | Wall each side of Ø5.992 |
|---|---|---|---|---|---|
| M4 | ISO 4762 socket head cap | 7.00 | 7.00 ✔ | 7.30 | `(5.992 − 7.30)/2 = ` **−0.654** ✔ record: −0.65 |
| M4 | DIN 6912 / DIN 7984 low head | 7.00 | 7.00 ✔ | 7.30 | **−0.654** ✔ record: −0.65 |
| M4 | ISO 7380 button head | 7.60 | 7.60 ✔ | 7.90 | **−0.954** ✔ record: −0.95 |
| M4 | ISO 10642 countersunk | 8.96 | 8.96 ✔ | 9.26 | **−1.634** ✘ record: **−1.48** |
| M3 | ISO 4762 | 5.50 | 5.50 ✔ | 5.80 | **+0.096** ✔ record: +0.10 |

**Every published head diameter in the table is correct, and the conclusion — no standard M4 head
fits a Ø6.000 h6 boss — is confirmed independently.** One row's arithmetic does not follow the
table's own declared `dk + 0.3` basis: the ISO 10642 figure of −1.48 is `(5.992 − 8.96)/2`, i.e.
computed without the 0.3 clearance. Recorded as F-07 (LOW); the conclusion is unaffected and is
in fact understated.

### Evidence — boss wall

A 3.0 mm A/F hex measures `3.0 × 2/√3 = 3.46410` across corners.
`(5.992 − 3.46410)/2 = ` **1.263949 mm** → the claimed **1.264 mm** ✔ **exact.**

*Not reproducible:* the 53.5 MPa bearing figure. `F = 2500/(6 × 1.5) = 277.8 N` reproduces, but
no bearing area is stated; on a 3.0 A/F × 2.0 deep socket the flat area is
`(3.0/√3) × 2.0 = 3.46 mm²`, giving **80 MPa**, not 53.5. The margin against ≈1,232 MPa is then
15×, not 23× — still large. Recorded inside F-07.

### Evidence — torque, under my own assumptions

**2.5 N·m on an M4 A4-70.** M4 × 0.7: `d = 4.0`, `d₂ = 3.545`, `A_s = 8.78 mm²`, A4-70 proof
`R_p0.2 = 450 MPa`. Using `T = K·d·F` and adding thread torsion as `σ_v ≈ 1.28σ` (τ ≈ 0.5σ):

| K (nut factor) | F (N) | σ on `A_s` | σ_v | % of 450 MPa |
|---|---|---|---|---|
| 0.15 (dry film, low) | 4167 | 475 MPa | 608 MPa | **135 %** |
| **0.18** | 3472 | 395 MPa | **506 MPa** | **112 %** |
| 0.20 (dry steel) | 3125 | 356 MPa | 456 MPa | 101 % |
| 0.24 (dry, high) | 2604 | 297 MPa | 380 MPa | **84 %** |

The record's *"≈512 MPa … 114 % of yield"* **reproduces at K ≈ 0.18**, which is a defensible value
given DR-8's mandatory anti-galling dry film. **But the ECR states no friction coefficient, and
the claim reverses at K ≥ 0.19** — at an ordinary dry-assembly K = 0.24 the bolt sits at 84 % of
yield, which is normal practice. The claim is **assumption-dependent and the assumption is not
recorded.** Recorded inside F-07.

**1.2 N·m on the `AP-D13` integral spigot.** Full torque balance
`T = F[0.16p + 0.58 μ d₂ + μ r_b]` with `p = 0.7`, `d₂ = 3.545`, `r_b = 4.5` and μ = 0.15:
`T = F × 1.095`, so `F = 1200/1.095 = ` **1096 N** → the record's **≈1,095 N**, reproducing to
1 N at a friction coefficient I chose independently. On the M4 root area (7.75 mm²) that is
141 MPa direct, `σ_v ≈ 184 MPa` → the record's **≈190 MPa**. Against Ti-6Al-4V Grade 5 yield of
830 MPa the margin is **4.5×** → *"a margin above 4×"* ✔ **1.2 N·m is appropriate.**

### The defect that decides this criterion

**F-08 (HIGH). The ruled torque is not in the governing volume.** `ECR-D-009` §8 states:

> *"`spec/01` §6 step 12 and §10 step 3 both carried the old value; **both are corrected**, not only the one this ECR named in §2."*

`spec/01` is corrected — lines 182 and 271 read **1.2 N·m**. But `spec/06`, which the ECR lists
**first** in `affected_artifacts` and which is the governing volume for SEWCP-700, still reads
**2.5 N·m in two places**:

- `spec/06` line 116, §4 Mating Components: *"No separate fastener. **2.5 N·m** through the `AP-D14` hex socket … (ECR-D-009)"*
- `spec/06` line 246, §10 Installation step 5: *"torque the locator to **2.5 N·m** through the `AP-D14` 3.0 mm hex socket … (ECR-D-009)"*

Both cite ECR-D-009 while carrying the value ECR-D-009 struck. `APR-023`'s *What is approved*
table lists *"§10 steps 3 and 5"* as changed — step 5 **was** rewritten (screw → spigot) and the
torque inside it was left alone. **The frozen specification now carries two contradictory torque
values for the same operation on the same part, in two volumes, both attributed to the ECR that
was supposed to remove the contradiction.** A shop reading the component volume torques to 2.5.

**F-09 (LOW).** `spec/06` §8 still gives the reason for the flange-OD anti-galling treatment as
*"**Transition fit**; titanium galls without treatment"*, and §11 FM #5's mitigation still reads
*"transition fit, not press"*. `AP-D03` is now **h6 clearance** (0 to 0.024) precisely because,
in `ECR-D-009`'s words, *"a part that is screwed in cannot be an interference fit."* Residue.

### Disposition

The head-fit and boss-wall arithmetic reproduce; the torque values are sound where applied. But
the disposition's central corrective number is **absent from the volume the ECR names first**,
and the record's claim that both instances were corrected is false against the bytes.

**FAIL**

---

## 7 · V6 — ECR-D-010, and the check that prevents its recurrence

### What I did

Read `spec/00` §3.2; proved the 15° bound myself; checked the rejected triads against the same
table; ran `aief_clearance`; then restored the old clocking in a temp copy and confirmed the
checker fails.

### Evidence

- **`spec/00` §3.2** now carries the row *"**Kinematic locators (Cooling Plate↔Heater Plate)** | **Ø260 BC** | **75°, 195°, 315°** | **3**"* ✔ and *"Thermal-choke fasteners (outer) | Ø270 BC | 0° + n·30° | 12"* ✔
- **15° is provably the maximum.** For a triad `{θ, θ+120, θ+240}`, `120 mod 30 = 0` and `240 mod 30 = 0`, so all three members share the residue `θ mod 30`. Separation from the nearest 30° ray is `min(θ mod 30, 30 − θ mod 30)`, maximised at `θ mod 30 = 15` giving **15°**. ✔ Proven, not asserted.
- **Rejected triads land on the coolant rays.** `spec/00` §3.2 puts the coolant inlet at **255°** and the outlet at **285°**. `{15, 135, 255}` contains 255 ✔; `{45, 165, 285}` contains 285 ✔. Both collide with `CP-D22`'s Ø10.0 stub bore spanning z 6–16, which the M4 tap at z 12–17 would meet. Confirmed.
- **`python -m aief_clearance` → `CLEARANCE OK`, exit 0** ✔ Eight features resolved from the §3.2 table, three skipped for want of a bolt circle or angles.

### Adversarial test

In a temp copy at `%TEMP%\…\scratchpad\adv` (the real repository untouched), I restored
`30°, 150°, 270°` in the §3.2 locator row and re-ran the checker:

```
FAIL  Thermal-choke fasteners (outer) @ 30 deg  vs  Kinematic locators (Cooling Plate<->Heater Plate) @ 30 deg
      clearance 0.00 mm, minimum wall 1.50 mm, short by 1.50 mm
1 INTERFERENCE(S)                                          EXIT CODE: 1
```

**The check is real.** It reads the frozen table as its input, it finds the defect it was written
after, and it exits non-zero.

### Findings raised while doing this

**F-10 (LOW).** The §6 candidate-triad table in `ECR-D-010` enumerates **three** of the **four**
triads at 15° offset. `{105, 225, 345}` is omitted. It is correctly excluded — 105° is the RF
strap land centre and 225° is an RTD blind port at r = 140 — but the enumeration is presented as
exhaustive and is not.

**F-11 (LOW).** Two numbers in the `spec/00` §3.2 verification paragraph do not reproduce:
*"34.97 mm of centre distance"* — I compute
`√(130² + 135² − 2·130·135·cos 15°) = ` **34.9429 mm**; and *"17.0 mm required"* is
`11.0 + 6.0`, the **Ø12.000** clearance requirement. With `CP-D10` at Ø10.000 the requirement is
`11.0 + 5.0 = ` **16.0 mm**. Both errors are conservative and the conclusion is unaffected. The
adjacent *"15.4° clear of the RF land envelope"* is likewise a Ø12 figure; at Ø10.000 the
clearance is `93 − 75 − asin(5.0/130) = ` **15.80°**.

**F-12 (MEDIUM).** I computed every pairwise margin the checker evaluates, not just the failures
it prints. **The tightest pair in the whole map is the RF strap land @105° against the outer
choke station @90°, at 1.579 mm against a 1.50 mm declared wall — a margin of 0.079 mm.** That is
a 5 % margin on a machined ligament, it is the binding constraint on the entire clocking scheme,
and it is remarked nowhere — not in `spec/00` §3.2, not in `ECR-D-004` §6.4 (which computes the
same 1.58 mm and presents it as clearance), and not in the checker's output, which prints only
failures. A `CP-D26` counterbore at its `+0.20` limit consumes more than the whole margin.

### Disposition

Every element the criterion names reproduces, and the adversarial test confirms the checker is a
real check rather than a decoration.

**PASS**

---

## 8 · V7 — ECR-D-011

### What I did

Recomputed the outer-spiral turn centres and the slot span from `spec/02` §2.2 and `HP-D10`;
then tested both escapes with my own arithmetic.

### Evidence

- **Turn centres.** Outer spiral r 78 → 145 at 6.00 mm pitch → `78 + 6n` = 78, 84, 90, 96, 102, 108, 114, 120, **126**, **132**, 138, 144. `(145 − 78)/6 = 11.17` turns, matching the *"11.2 turns"* of §2.2 ✔
- **Slot span.** `HP-D10` = 8.00 L radial at Ø260 BC (r = 130) → **r 126.0 to 134.0** ✔
- **Collision.** `HP-D06` groove is 3.20 W → envelopes `124.4–127.6` (turn at 126) and `130.4–133.6` (turn at 132). The second lies wholly inside the slot; the first overlaps it over 126.0–127.6. **Both collide.** A 3.00 mm `HP-D09a` slot opens a 3.20 mm groove containing brazed MI cable at each of three positions ✔ **The claimed collision at r = 126 and r = 132 is confirmed.**
- **Escape 1 — shortening.** `AP-06` = 0.399 mm travel; boss `Ø6.000 h6` at max material 6.000, plus the slot must clear both extremes: `6.068 + 2 × 0.399 = ` **6.866 → 6.87 mm** minimum slot length ✔. A 6.87 mm radial window against a 6.00 mm pitch **must** contain at least one turn centre. **Closed.** ✔
- **Escape 2 — relocating.** The inter-zone gap is r 72 (inner spiral end) to r 78 (outer spiral start) = **6.00 mm**, and a relocated slot would need its **radial** extent inside it — 8.00 nominal, 6.87 minimum. **Closed by 0.87 mm.** ✔

### Finding raised while doing this

**F-13 (MEDIUM).** Escape 2 is closed, but **not by the arithmetic the record quotes.**
`ECR-D-011` §3 and `spec/02` §3.2 both close it as *"the only clear annulus between the two zones
is r 72–78, **6.00 mm** wide against a **6.05 mm** slot."* 6.05 is `HP-D09`, the slot's
**tangential width**; the dimension that must fit inside a **radial** annulus is `HP-D10`, the
radial length. The correct comparison is 6.87 (min) or 8.00 (nominal) against 6.00. Separately,
the *"6.00 mm"* annulus is measured **turn centre to turn centre**; edge to edge, with 3.20 mm
grooves, the true clear span is `76.4 − 73.6 = ` **2.80 mm**. The escape is closed far more
decisively than stated — the conclusion is right and both cited quantities are the wrong ones.

### Disposition

The collision reproduces and both escapes are genuinely closed.

**PASS** — with F-13 recorded: one of the two closure arguments cites a dimension that does not
govern.

---

## 9 · V8 — Approval chain and freeze integrity

### What I did

Ran `python -m aief_approval verify`. Re-implemented DC-1 and DC-2 from the `FROZEN.md`
construction text in a standalone script and recomputed all 29 rows and the aggregate. Recovered
every pre-session digest with `git show HEAD:<path>` and compared it against each approval's
`prior_hash`.

### Evidence — what reproduces

**DC-1, all eleven `spec/**` artifacts, recomputed independently: 11 of 11 match `FROZEN.md`
exactly.**

**DC-2 over the registry rows** = `55904b939054fd78c1df8716b0c50b8a2263c7360e32a8058e68cb89a476030e`
— equal to `FROZEN.md` § *Aggregate* and to `STATE.md` `frozen_set_hash` at the snapshot instant.
(See §0: at the start of this session `FROZEN.md` published `c56e75bc…`, the pre-session
aggregate, and disagreed with `STATE.md`. That was repaired mid-audit. Both values are now
correct and `c56e75bc…` is recorded as a prior value.)

**`prior_hash` chain, all seven new approvals — every one equals the pre-session `HEAD` DC-1:**

| Approval | subject_path | `prior_hash` vs `git show HEAD:` | `subject_hash` vs tree |
|---|---|---|---|
| APR-020 | `spec/01` | `36e8d35b…` **MATCH** | `55b47ca3…` **MATCH** |
| APR-021 | `spec/00` | `baf9ae50…` **MATCH** | `fa2a84cc…` **MATCH** |
| APR-022 | `spec/02` | `ab36e082…` **MATCH** | `02905800…` **MATCH** |
| APR-023 | `spec/06` | `0d2aa747…` **MATCH** | `da702fe0…` **MATCH** |
| APR-024 | `spec/03` | `b00d5289…` **MATCH** | `a2f951a1…` **MATCH** |
| APR-025 | `spec/07` | `1b7b5914…` **MATCH** | `7558bc5b…` **MATCH** |
| APR-026 | `spec/README` | `95da15c6…` **MATCH** | `1d772072…` **MATCH** |

**7 of 7 roots verified against git objects. The spec-side freeze bookkeeping is honest.**

### Evidence — what fails

`python -m aief_approval verify` ends **`APPROVAL CHAIN INTEGRITY FAILED`**, exit 1, on two
counts:

1. `APR-003`: no `subject_path` — LAW-10 clause 1.
2. `framework/framework.manifest.json`: registered at `8af8971b…`, **working tree at
   `920eb6ee…`**, and *"NO approval binds that state … Every approval on this path is VOID in
   consequence."* All six manifest approvals (`APR-001`, `-002`, `-004`, `-006`, `-010`, `-012`)
   compute **VOID**.

I established the provenance myself. At `HEAD` the manifest is `ae16ccac…`; the registry names
`8af8971b…`; the working tree is `920eb6ee…`. So there are **two** distinct divergences: the
recorded one (`ECR-D-006`, raised 2026-08-08, open) and a **further uncommitted edit**.
`framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md` declares itself the author of
eleven manifest changes and names `project/approvals/APR-014` and `APR-015` as its LAW-10
record — **neither file exists** in `.ai/project/approvals/`. `AIEF-AMD-014` is itself
**unregistered** in `FROZEN.md`; the repository's own V-24 check says so:

```
"AMD-21 criterion candidate unregistered: framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md"
"framework/framework.manifest.json: DC-1 920eb6ee… != registered 8af8971b…"
registered 29, verified 28
```

This is **not** work of session `S-2026-08-10-01` — it is dated `S-2026-08-08-12` — but it is the
live state of the tree being audited and it is unresolved.

### Findings

**F-15 (HIGH).** A registered frozen artifact (`framework/framework.manifest.json`) stands at a
content state no filed approval binds, and the two approvals its authorising instrument names
(`APR-014`, `APR-015`) are not filed. `AIEF-AMD-014` is unregistered against the AMD-21 criterion.
Owner: `chief-systems-engineer`. Pre-dates this session; not cured by it.

**F-16 (LOW).** `FROZEN.md` line 70 still reads *"Per-artifact verification after this change:
**29 of 29 verified**"*, contradicted two lines later by its own superseding note and by
`STATE.md`'s *"28 of 29 verify"*. **28 of 29** is what I measured.

**F-17 (LOW).** The seven new registration-history rows were inserted **between** the 2026-08-08
and 2026-08-09 blocks, so the history table now runs 08-08 → **08-10** → 08-09, and the insertion
begins after a blank line, which terminates the preceding markdown table and starts a new,
header-less one. Bookkeeping only.

### Disposition

Everything the criterion asks me to recompute for `spec/**` reproduces exactly — 11 DC-1 values,
the DC-2 aggregate, and 7 of 7 `prior_hash` roots against git objects. But the command the
criterion instructs me to run **fails**, and it fails on a live LAW-01 freeze violation.

**FAIL**

---

## 10 · V9 — No unrelated bytes changed

### What I did

`git status`, `git diff --stat`, then a hunk-by-hunk read of all seven changed `spec/**` files
against the *What is approved* table of the corresponding approval.

### Evidence

`git diff --stat` over `spec/**`: 7 files, 191 insertions, 71 deletions. No `spec/**` file is
added or deleted. `spec/04`, `spec/05`, `spec/08`, `spec/09` are byte-identical to `HEAD` — I
confirmed this by DC-1, not by reading the diff.

**Clean — every hunk enumerated:**

| File | Approval | Result |
|---|---|---|
| `spec/07` | APR-025 | Exactly two `3.9 kg → 4.0 kg` rationale edits, as enumerated. **Clean** |
| `spec/README` | APR-026 | Exactly `Re ≈ 7,400 → 8,300`. **Clean** |
| `spec/03` | APR-024 | `SR-IF-4` press-fit closed + the five *dowel → locator boss* references APR-024 enumerates. **Clean** |

**Riders — hunks that map to no enumerated row:**

| File | Hunk | Enumerated? |
|---|---|---|
| `spec/01` | §8 surface-finish row gains *"Locators are installed **after** the anodize tank — see §6 steps 12–13"* | **No.** APR-020's ECR-D-009 row lists only `CP-IF-1`/`CP-IF-4` and §6 step 12 / §10 step 3 |
| `spec/00` | §4.4 *"without bowing or **dowel** shear"* → *"**locator** shear"* | **No.** APR-021 lists nothing in §4.4 |
| `spec/00` | §10 A2 *"kinematic dowels"* → *"kinematic locators (SEWCP-700)"* | **Partly** — APR-021's ECR-Q-009 row covers only the bushing bore on that line |
| `spec/02` | §4 *"Receives 3 dowels"* → *"3 locator bosses"* | **No** |
| `spec/02` | §8 *"Free sliding of dowels and pins"* → *"locator bosses and lift pins"* | **No** |
| `spec/02` | §10 steps 11 and 12 nomenclature | **No.** APR-022 lists only §10 step 13 |
| `spec/06` | §4 Mating row *Retaining screws* → *Retention* | **No.** APR-023's ECR-D-009 row lists `AP-IF-1`, `AP-D03`, `AP-D07`/`-D08`, `AP-D12`, `AP-D13`/`-D14`, §6 steps 2/4/7, §10 steps 3 and 5 |
| `spec/06` | §5.1 mating-slot table, counterbore `Ø12.0 H7 × 3.0` → `Ø10.0 H7 × 3.00` | **No.** APR-023's ECR-D-007 row says *"§8 and §9 … follow"*; §5.1 is neither |
| `spec/06` | §10 step 1 *"Verify the Ø12.0 H7 counterbore positions"* → `Ø10.0` | **No.** APR-023 lists §10 steps 3 and 5 |

Each of the seven approvals carries the scope clause: *"**Only** the changes enumerated below, in
this one artifact. **Every other byte of this file is unchanged** and no other volume is approved
here."* Nine hunks are outside that enumeration.

**Assessment of severity, stated so the reader can weigh it.** Every rider is either a
nomenclature substitution (*dowel* → *locator boss*) or the direct arithmetic consequence of an
enumerated change (Ø12.0 → Ø10.0 in a repeated-for-control table). **No dimension, requirement,
tolerance, interface or process value rides along that is not traceable to an approved
disposition.** I found nothing substantive smuggled in. But the approvals' own scope clause is a
statement of fact about the bytes, and it is false for four of the seven.

### Disposition

The criterion is *"confirm every hunk maps to a disposition enumerated in the corresponding
approval."* Nine do not.

**FAIL**

---

## 11 · V10 — The gate, and whether it can be trusted

### What I did

Ran `python -m aief_gate` against the snapshot. Then mutated a temp copy four ways and observed
whether the evaluator noticed.

### Evidence — baseline

```
C1 PASS  ECR-D-001 carries an approved disposition       (disposition A; approval APR-024 LIVE)
C2 PASS  ECR-D-002 carries an approved disposition       (disposition A; approval APR-026 LIVE)
C3 PASS  ECR-D-003 carries an approved disposition       (disposition A; approval APR-020 LIVE)
C4 PASS  ECR-D-004 carries an approved disposition       (disposition A; approval APR-022 LIVE)
C5 PASS  11 spec/** registered; 11 reproduce; chains reproduce on every spec/** path
C6 FAIL  ECR-D-002/-003/-004: no verification report declares them as subject
C7 PASS  4 ids in OPEN_ITEMS.md Blocking; 1 is ECR-D-*
LC-M04 CAD-READY: NO                                                        (exit 1)
```

C1–C5 and C7 PASS, verified on the evidence each criterion prints. C6's FAIL is the criterion this
report is filed to satisfy (see §0a).

### Evidence — adversarial mutation, all in a temp copy

| # | Mutation | Result |
|---|---|---|
| **(a)** | Blanked `disposition:` in `ECR-D-003` | **`C3` FAIL — "ECR-D-003: disposition empty"** ✔ and `C6` degraded to *"no disposition, so nothing to verify"* |
| **(b)** | Edited `spec/00` §3.2 with no approval filed | **`C5` FAIL** on three counts — DC-1 mismatch, registry mismatch, and *"NO approval binds that state … a LAW-01 freeze violation"*. `aief_approval verify` computes **`APR-021: VOID`**. Gate exit 1 ✔ |
| **(c)** | Filed a `VER-999` whose body names all three ECRs six times but whose `subject` names none | **`C6` stayed FAIL** — *"a mention in the body is not verification"* ✔ Changing only the `subject` field flipped it to PASS, confirming the predicate is the declared subject |
| **(d)** | Additionally set `verifier_role == author_role` on that report | **`C6` FAIL — "verifier_role == author_role … LAW-05"** ✔ |

**Verdict on the gate: it is a real check, not a decoration.** Every mutation was detected, the
DC-1 comparison is computed from bytes, the approval relation genuinely collapses to VOID, and
C6 genuinely resists the passing-mention attack it was written after.

### Finding raised while doing this

**F-18 (MEDIUM). `C7` is a check of a hand-maintained list, not of the ECR corpus.** I filed
`ECR-D-099` in the temp copy — `status: OPEN`, `disposition: null`, `affected_artifacts:
spec/01_SEWCP-200_Cooling_Plate.md` — and left it out of `OPEN_ITEMS.md` § *Blocking*.
**`C7` still reported PASS.** `_blocking_ids()` reads only the ids listed under `## Blocking` in a
mutable `project` file; an undispositioned ECR against `spec/**` that is absent from that list is
invisible to the criterion.

This matters here because `C7`'s current PASS was obtained by exactly that mechanism: this
session moved `ECR-D-001..004` and `ECR-D-007..011` out of `Blocking` and into `Open, not
blocking`. Those moves are defensible — the ECRs *are* dispositioned — but **`C7` did not verify
that; it verified the edit.** The failure shape is the one `ECR-D-010` §3 names as its own root
cause: *"A prose claim over a subset of pairs, frozen and never recomputed."* Owner:
`software.software-engineer`.

**F-19 (MEDIUM, adjacent).** `ecr_approval_states()` binds each ECR to the single
highest-ranked approval naming it. `C2` therefore certifies `ECR-D-002` on **`APR-026`**, the
`spec/README` approval, whose entire scope is *"`Re ~ 7,400` → `Re ~ 8,300`. No other change."*
The criterion never checks that every artifact the ECR touched carries an approval. An ECR whose
substantive volume was changed without an approval would still pass C1–C4 on a trivial one.

### Disposition

C1–C5 and C7 PASS on evidence; every adversarial mutation of the evaluator was detected.

**PASS** — with F-18 and F-19 recorded as the boundary of what the gate actually proves.

---

## 12 · V11 — Record accuracy

### ECR-D-001 and OI-V-11

**Is ECR-D-001's engineering disposition independently verified? Yes.** `VER-014` ran four cold
rounds and records at §6: *"The engineering survived **all four** rounds intact and was re-derived
independently each time. Every blocker in both rounds was **record integrity**."* Round 4 records
`W9 RECORD ACCURATE: PASS`, controls byte-identical, approval chain reproducing.

**Are the two defects OI-V-11 names repaired? Yes, both.**

- **Identifier collision.** `VER-014` is filed at `VER-014_Independent_Verification_ECR-D-001.md` with `verification_id: VER-014`. It no longer occupies `VER-008` (reserved by `T-003`) or `VER-010` (reserved by `T-005`). I checked every citing artifact: `ECR-D-001`, `ECR-D-002`, `ECR-D-007`, `ECR-D-008`, `ECR-D-009`, `APR-016`…`APR-019`, `FROZEN.md`, `GATES.md`, `STATE.md`, `OPEN_ITEMS_REGISTER.md`, `T-008` — **all fourteen cite `VER-014` and all resolve.** No artifact cites `VER-ECR-D-001`. ✔
- **Label collision.** Round-3 findings are now `R3-F1…R3-F12` and round-4 `R4-M1…R4-M5`, while round-1 criteria remain `V1…V10`. **The namespaces no longer collide**, and the yaml carries a `label_scheme` field declaring the convention. ✔

**But `VER-014` itself records `round_1..round_4: FAIL` and `status: ECR-D-001 NOT CLOSED`, and
its §6 verdict says the gate evidence *"cannot be trusted."* `C6` passes ECR-D-001 on that file
anyway** (F-18's sibling). And `.ai/project/results/R-014.md` still cites `VER-010`, `VER-011`,
`VER-012` and `VER-013` for named findings; **none of those four files exists** — the
cited-but-not-filed defect, in a different corner. Recorded as **F-20 (LOW)**.

### Claims checked against the specification bytes

| Record | Claim | Bytes |
|---|---|---|
| `ECR-D-003` §6.1 | Ten enumerated `spec/01` changes | **All ten present.** `CP-IF-10`, §4 SEWCP-201 row, `CP-D22`–`CP-D25`, §3.1 port exception, §6 steps 3 and 10, §9 two rows, FM #8 ✔ |
| `ECR-D-004` §6.1 | Nine enumerated changes across three volumes | **All nine present** ✔ |
| `ECR-D-010` §6.1 | `spec/00` §3.2; `spec/01` `CP-IF-4`/`CP-D10`; `spec/02` `HP-IF-3`/`HP-D11`; `spec/06` `AP-IF-3` | **All present, all at 75/195/315** ✔ |
| `ECR-D-011` §6 | `spec/02` §3.2 keep-out ≥ 12 × 10 mm; §6 step 3 tangential routing; `HP-D09a` 3.00 ±0.10 | **All present** ✔ |
| `ECR-D-007` §8 | Action 3 **rejected**, split to `ECR-D-012`; keep-out **9.5 mm**; limit **r ≤ 120.5**; wall **7.85 mm** | ✘ **Contradicted.** Spec implements action 3 (`CP-D09`/`CP-D10` Ø12.000 → Ø10.000, attributed to *"ECR-D-007 action 3"* in both `spec/01` and `spec/06`); keep-out is **8.5**, limit **121.5**, wall **6.85**. `ECR-D-012` does not exist — **F-05, F-06** |
| `ECR-D-009` §8 | *"`spec/01` §6 step 12 and §10 step 3 … **both are corrected**"* | ✔ for `spec/01`. ✘ **`spec/06` lines 116 and 246 still read 2.5 N·m** — **F-08** |
| `ECR-D-009` §8 | *"integral **Ø12.000 h6** flange"*; *"Clearance becomes 0 to **0.029**"*; *"RSS moves 0.0401 → **0.0422**"* | ✘ **Stale.** `AP-D03` is **Ø10.000 h6**, clearance **0 to 0.024**, and `spec/06` §9 states the RSS as **0.0414**. All three ECR figures are internally consistent for the Ø12 form and none matches the artifact. **F-21 (MEDIUM)** |

I independently confirmed the RSS the *specification* states:
`√(0.010² + 0.012² + 0.005² + 0.038²) = ` **0.041388 → 0.0414** ✔ within the 0.050 allocation.

### Approval references — every one filed this session is dangling

**F-22 (HIGH).** Seven ECR records point their `approval:` field at approval files that **do not
exist**:

| Record(s) | `approval:` names | Exists? | The real file |
|---|---|---|---|
| `ECR-D-007`, `-008`, `-009`, `-010`, `-011` | `approvals/APR-020_Specification_Coherence_Package.md` | **No** | `APR-020_Cooling_Plate_coherence_package.md` |
| `ECR-D-003` | `approvals/APR-021_Coolant_Stub_Interface.md` | **No** | (`APR-021` is `APR-021_ICD_coherence_package.md`, subject `spec/00`) |
| `ECR-D-004` | `approvals/APR-022_Choke_Fastener_Stack.md` | **No** | `APR-022_Heater_Plate_coherence_package.md` |

Every markdown link in those records' §6 disposition sections dangles with them. `ECR-D-001`,
`-002`, `-005` — filed in earlier sessions — all resolve; **only this session's references are
broken.**

Worse than the filename: **`ECR-D-003` names the wrong approval.** Its `affected_artifacts` is
`spec/01` alone, and its ten executed changes are all in `spec/01`. `APR-021`'s `subject_path` is
`spec/00`, and `APR-021`'s `ecr:` list — `ECR-D-002, ECR-D-004, ECR-D-008, ECR-D-010, ECR-Q-009`
— **does not contain `ECR-D-003` at all.** The approval that actually binds ECR-D-003's changes is
`APR-020`, which the gate finds by scanning `ecr:` fields rather than by following the record's
own pointer. **The `approval:` field of the ECR that C3 gates on points at an approval that does
not cover it.**

### Other coherence residues found

**F-23 (LOW).** `spec/00` §10 A1 still directs *"Cooling Plate: machine channel, FSW-seal lid,
**orbital-weld VCR stubs**"*. `ECR-D-003` removed that operation — the VCR gland is now on the
316L end of the SEWCP-201 transition joint and is never welded to the plate; `spec/01` §6 step 10
is explicit that only 6061-to-6061 fusion occurs. `ECR-D-003` §2 declares `spec/00` §10 A1
*"unchanged by this disposition"*, so this is a knowing omission rather than an oversight — but
the ICD now instructs an operation the component volume forbids.

**F-24 (LOW).** `ECR-D-003`'s yaml `approval_chain` comment reads *"determine liveness by the
`aief_approval` relation"*, which is correct practice; but the field's value, `APR-021`, is the
wrong approval (F-22), so following the instruction returns the liveness of an approval that does
not cover the ECR.

### Disposition

`ECR-D-003`, `-004`, `-010` and `-011` describe their executed changes accurately. `ECR-D-007`
claims a rejection the specification implements and quotes four superseded numbers; `ECR-D-009`
claims a correction that was not applied to the volume it names first and describes a flange
diameter the part does not have; seven records point at approval files that do not exist and one
points at an approval that does not cover it.

**FAIL**

---

## 13 · Findings

| ID | Finding | Severity | Owner | Blocks |
|---|---|---|---|---|
| **F-08** | `spec/06` lines 116 and 246 carry **2.5 N·m** for the locator while `spec/01` carries **1.2 N·m**; `ECR-D-009` claims both instances corrected. Two contradictory values for one operation, in the frozen set, both citing ECR-D-009 | **HIGH** | chief-systems-engineer | ECR-D-009 closure; SEWCP-200 and SEWCP-700 assembly |
| **F-22** | Seven ECR records name approval files that do not exist; `ECR-D-003` names `APR-021`, whose `ecr:` list omits ECR-D-003 and whose subject is a different volume | **HIGH** | chief-systems-engineer | LAW-10 traceability for C3/C4 |
| **F-05** | `ECR-D-007` §8/§9 record action 3 as **rejected** and quote 9.5 / 120.5 / 7.85; the specification **implements** it and reads 8.5 / 121.5 / 6.85 | **HIGH** | chief-systems-engineer | ECR-D-007 closure |
| **F-06** | `ECR-D-012` is cited four times and does not exist — no record, no `OPEN_ITEMS` entry, no register row | **HIGH** | chief-systems-engineer | The residual it is said to carry is unowned |
| **F-15** | `framework/framework.manifest.json` stands at `920eb6ee…`, bound by no approval; `APR-014`/`APR-015` cited by `AIEF-AMD-014` are not filed; `AIEF-AMD-014` is unregistered. `aief_approval verify` exits 1 | **HIGH** | chief-systems-engineer | Not `LC-M04-EXIT` (outside `spec/**`); blocks freeze integrity and Stage 6 |
| **F-14** | The repository was edited by another party during this verification; `FROZEN.md` and `STATE.md` changed mid-audit | **MEDIUM** | project-manager | Evidential integrity of any cold audit |
| **F-03** | *"The bore never penetrates the lid"* holds only at nominal; at the `CP-D23`/`CP-D22`/`CP-D08` limits it cuts up to **0.218 mm** into the FSW lid, in the pressure boundary. No tolerance analysis recorded | **MEDIUM** | Design Authority | SEWCP-200 CAD / weld routing |
| **F-04** | New choke stack engages **1.08 × D**; `spec/01` §11 FM #11's live mitigation still demands **min 2 × D**. Unreconciled and unamended | **MEDIUM** | Design Authority | — |
| **F-12** | Tightest clearance in the whole §3.2 map is **1.579 mm against a 1.50 mm wall** (RF land @105° vs outer choke @90°) — a 0.079 mm margin, remarked nowhere. `CP-D26`'s `+0.20` limit exceeds it | **MEDIUM** | Design Authority | — |
| **F-13** | `ECR-D-011`/`spec/02` §3.2 close the relocation escape by comparing a **6.05 mm tangential width** to a radial annulus; the governing dimension is the 8.00/6.87 mm radial length, and the true clear annulus is 2.80 mm not 6.00 mm | **MEDIUM** | chief-systems-engineer | — |
| **F-18** | `C7` reads only `OPEN_ITEMS.md` § *Blocking*. An undispositioned ECR naming `spec/**` and absent from that list passes `C7` — demonstrated | **MEDIUM** | software.software-engineer | Trust in `C7` |
| **F-19** | `C1`–`C4` bind an ECR to one approval naming it. `C2` certifies ECR-D-002 on `APR-026`, whose whole scope is one `Re` value | **MEDIUM** | software.software-engineer | Trust in `C1`–`C4` |
| **F-21** | `ECR-D-009` §8 describes a **Ø12.000 h6** flange, 0–0.029 clearance and RSS 0.0422; the part is **Ø10.000 h6**, 0–0.024, RSS 0.0414 | **MEDIUM** | chief-systems-engineer | ECR-D-009 closure |
| **F-09** | `AP-D03` is h6 clearance, but `spec/06` §8 and §11 FM #5 still call it a *transition fit* | **LOW** | Design Authority | — |
| **F-01** | `0.080 m²` does not follow from its own *"path × perimeter"* derivation (`2.2 × 0.032 = 0.0704`); it is the old 0.09 scaled. `R_total` unaffected at the quoted precision | **LOW** | Design Authority | — |
| **F-02** | `program/SEDEP-PMP-001` still quotes `Re 7,400` and `36.6 K` | **LOW** | project-manager | — |
| **F-07** | `ECR-D-009`'s ISO 10642 row omits the `dk + 0.3` allowance; its 53.5 MPa bearing figure is not reproducible (I get 80 MPa); its 114 %-of-yield claim states no friction coefficient and reverses at K ≥ 0.19 | **LOW** | chief-systems-engineer | — |
| **F-10** | `ECR-D-010` enumerates three of the four 15°-offset triads; `{105, 225, 345}` is omitted | **LOW** | chief-systems-engineer | — |
| **F-11** | `spec/00` §3.2: *34.97 mm* does not reproduce (**34.943**); *17.0 mm required* and *15.4°* are Ø12-era figures (Ø10 gives 16.0 mm and 15.80°) | **LOW** | chief-systems-engineer | — |
| **F-16** | `FROZEN.md` line 70 still asserts *29 of 29 verified*; the measured value is **28 of 29** | **LOW** | chief-systems-engineer | — |
| **F-17** | The seven new registration-history rows are inserted out of date order and terminate the preceding markdown table | **LOW** | chief-systems-engineer | — |
| **F-20** | `R-014.md` cites `VER-010`…`VER-013` for named findings; none of the four files exists | **LOW** | qa-engineer | — |
| **F-23** | `spec/00` §10 A1 still directs *"orbital-weld VCR stubs"*, an operation `ECR-D-003` removed | **LOW** | Design Authority | — |
| **F-24** | `ECR-D-003`'s `approval_chain` value resolves, via the relation it correctly recommends, to an approval that does not cover it | **LOW** | chief-systems-engineer | — |

**Not raised as findings, recorded for completeness.** `PYTHONPATH=src python -m pytest tests/ -q`
returns **8 failed, 564 passed**. Two bear directly on this audit and are consistent with what I
measured independently: `test_v24_live_registry` fails at *registered 29, verified 28* plus the
unregistered `AIEF-AMD-014` (F-15/F-16), and
`test_stage6_certification_evidence::test_no_per_file_cap_breach` fails with
`{'project/STATE.md': (1655, 1100), 'project/OPEN_ITEMS.md': (609, 600)}` — i.e. this session's
`STATE.md` rewrite exceeds its declared cap by 50 %, while `AIEF-AMD-014` §AMD-52 records
CMP-BLOCK-006 disposed on the ground that *"V-09 passes: every per-file cap is respected."* The
remaining six failures are in the execution-architecture record set (`R-014`/`R-015`, `T-007`/
`T-008`) and are outside this scope.

---

## 14 · Verdict

**The engineering reproduces. The records do not.**

Every dimensional, structural and geometric claim I was asked to recompute came back correct,
most of them to the digit: the Z stack closes at 20.000; the Ø10.0 stub bore spans exactly the
locally deepened channel; σ = 2.8125 MPa; `M5 × 30` is unbuildable at every counterbore depth and
`e = 5.400` at `d = 2.5`; the 8.5 mm keep-out, the r ≤ 121.5 limit, the 6.85 mm tap-drill wall and
the 7.74 → 7.80 tap callout all follow from the plate's own dimensions; 15° is provably the best a
120°-spaced triad can do; the heater spiral really is cut at r = 126 and r = 132 and both escapes
really are closed; the boss wall really is 1.264 mm; 1.2 N·m really does give 1,096 N at μ = 0.15.
Eleven of eleven `spec/**` DC-1 digests and seven of seven approval `prior_hash` roots verified
against git objects. The clearance checker and the gate evaluator both survived deliberate
sabotage.

What fails is the layer that is supposed to describe that engineering. `ECR-D-007` records a
rejection the specification implements and cites a record that does not exist. `ECR-D-009` claims
a correction that never reached the volume it names first, leaving two contradictory torque values
in the frozen set. Seven ECRs point at approval files that were never created, and one points at
an approval that does not cover it. Nine hunks ride outside their approvals' own "only the changes
enumerated below" clause. A frozen framework artifact stands at a state no approval binds. And the
tree was being edited while I audited it.

This is the same pattern `VER-014` recorded four consecutive times against a different subject:
**sound engineering, unsound bookkeeping.** It is not cosmetic. F-08 would send a torque wrench to
the wrong number; F-05/F-06 leave a rejected requested action unowned; F-22 breaks the LAW-10
chain that `C1`–`C4` are supposed to walk.

**`LC-M04-EXIT` is not cleared by this report.** `C6` will compute PASS on this file's existence
(§0a) and the gate line will read `CAD-READY: YES`. **That is a machine limit, not this verifier's
disposition.** Four criteria FAIL. Recommended: dispose F-08, F-22, F-05, F-06 and F-15 before any
CAD work begins, and re-gate.

## 15 · Result

| | |
|---|---|
| V1 ECR-D-002 completion | **PASS** |
| V2 ECR-D-003 arithmetic | **PASS** |
| V3 ECR-D-004 arithmetic | **PASS** |
| V4 ECR-D-007 | **PASS** |
| V5 ECR-D-009 | **FAIL** |
| V6 ECR-D-010 and its checker | **PASS** |
| V7 ECR-D-011 | **PASS** |
| V8 Approval chain and freeze integrity | **FAIL** |
| V9 No unrelated bytes changed | **FAIL** |
| V10 The gate | **PASS** |
| V11 Record accuracy | **FAIL** |

**7 PASS · 4 FAIL** — 24 findings: 5 HIGH, 8 MEDIUM, 11 LOW.
