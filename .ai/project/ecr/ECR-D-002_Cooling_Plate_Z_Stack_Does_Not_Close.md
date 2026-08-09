# ECR-D-002 — The Cooling Plate Z stack does not close

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised against the frozen Rev A specification. Blocking `LC-M04-EXIT` criterion `C2`.

```yaml
ecr_id:       ECR-D-002
class:        D                      # defect - LAW-02: a defect stops the affected work
raised_by:    project-manager · S-2026-08-08-01
status:       ENGINEERING-IMPLEMENTED   # NOT CLOSED - awaits C6 independent verification
disposition:  A - REDUCE THE CHANNEL DEPTH 8.00 -> 6.00
ruled_by:     human-owner · S-2026-08-09-14
approval:     approvals/APR-019_Cooling_Plate_Channel_Depth.md
approval_chain: APR-019   # terminal; determine liveness by recomputing its subject_hash
raised_at:    2026-08-08T01:31:23Z
closed_at:    null
residual:     one - CP-02 pressure drop, see §7
```

---

## 1 · Class

**D — defect.** Four declared dimensions cannot all hold. Under LAW-02 a defect stops the
affected work: SEWCP-200 CAD cannot model a plate whose through-thickness arithmetic is
inconsistent.

## 2 · Affected artifacts

`spec/01_SEWCP-200_Cooling_Plate.md` — corrected. No other volume: the channel is internal and
the ICD's `Z = 20.0` is preserved by this disposition rather than changed.

## 3 · Evidence

**3.1 The arithmetic.** The channel is machined into the **bottom** face and closed by a
friction-stir-welded lid (§13; §6 steps 4–5). Through-thickness, top face downward:

| Ref | Dimension | Value | Criticality |
|---|---|---|---|
| `CP-D07` | Channel-to-top-face wall | 8.00 ± 0.20 | Medium — thermal |
| `CP-D06` | Coolant channel depth | **8.00** +0.20/−0 | Medium |
| `CP-D08` | FSW lid thickness | 6.00 ± 0.10 | Medium |
| | **Sum** | **22.00** | |
| `CP-D02` | **Overall thickness** | **20.000 ± 0.030** | **Critical — Z stack** |

**Over by 2.00 mm.**

**3.2 Which value governs, on the record.** `20.000` is corroborated **six** times: `CP-D02`;
requirement `CP-10` (*"Overall thickness 20.000 ± 0.030 mm — Micrometer, 8 points"*); the ICD
assembly diagram (*"Ø320 × 20.00 … Z = 20.0"*); the ICD tolerance-allocation table (row 2,
*"Cooling Plate thickness 20.000 / 0.030 / 40.000"*); the §11 inspection plan; and the mass
estimate. The three sub-dimensions are stated once each and are all **Medium**.

**3.3 The depth was derived, not arbitrary.** §2.1 sizes the channel *"backwards from the
Reynolds number, not from pressure drop"*: 10.0 × 8.0 = 80 mm² → 0.83 m/s → Re ≈ 7,400,
h ≈ 5,000 W/m²·K. §2.1 states *"Turbulence is a requirement, not an outcome."*

## 4 · Impact

Blocks SEWCP-200 CAD and `LC-M04-EXIT` `C2`. Shares the Z arithmetic with `ECR-D-004`
(M5×30 against a 29.5 mm stack) and with `ECR-D-007` action 5 (M4 tap depth).

## 5 · Requested action

Rule which of the four dimensions is corrected.

## 6 · Disposition — **A**

**Channel depth 8.00 → 6.00.** Ruled by `human-owner`, `S-2026-08-09-14`, approval
[`APR-019`](../approvals/APR-019_Cooling_Plate_Channel_Depth.md). Options B (top wall), C (FSW
lid) and D (overall thickness) were presented and not approved.

**Basis.** `CP-D02` governs on the record (§3.2), so a sub-dimension must give. Of the three,
reducing the depth is the only one that **improves** the margin on its own governing
constraint — Re rises rather than falls — while B attacks the Critical `CP-08` flatness
requirement and C narrows a weld process window guarding a leak-into-vacuum failure.

### 6.1 Executed changes — `spec/01` only

| Location | Was | Now |
|---|---|---|
| `CP-D06` | 8.00 | **6.00**, criticality annotated *"set by the Z stack, ECR-D-002"* |
| §2.1 cross-section | 10.0 × 8.0 mm, *"Selected"* | 10.0 × **6.0** mm, derivation now cites the Z-stack identity |
| §2.1 flow area | 80 mm² | **60 mm²** |
| §2.1 mean velocity | 0.83 m/s | **1.11 m/s** |
| §2.1 hydraulic diameter | 8.89 mm | **7.50 mm** |
| §2.1 Reynolds number | ≈ 7,400 | **≈ 8,300** |
| §2.1 convective coefficient | ≈ 5,000 W/m²·K | **≈ 6,500 W/m²·K** |
| §2.1 wetted area | ≈ 0.09 m² | **≈ 0.080 m²** |
| §5 mass estimate | channel ≈ 0.18 L, ≈ 3.9 kg | channel ≈ **0.13 L**, ≈ **4.0 kg** |
| §13 rationale heading | *"Why 10 × 8 mm channel"* | *"Why 10 × 6 mm channel"* |
| §13 rationale, §14 talking point | 0.83 m/s, Re ≈ 7,400 | **1.11 m/s, Re ≈ 8,300** |

Every derived value was recomputed from §2.1's own parameters at Q = 4.0 L/min:
A = 60 mm²; v = Q/A = 1.11 m/s; D_h = 4A/P = 240/32 = 7.50 mm; Re ∝ vD_h → 7,400 × 1.125;
h ∝ Re⁰·⁸/D_h → 5,000 × 1.099 × 1.185; wetted area ∝ perimeter, 36 → 32 mm.
**Enumerated before editing and re-checked after** — the check found two stale values
(§13 heading, and a `Re ≈ 7,400` a substitution had stopped short of) which are included above.

### 6.2 Net effect on the governing requirements

| Requirement | Direction |
|---|---|
| `CP-01` ≥ 3000 W, `CP-11` ≤ 1.5 °C | **Improved.** h rises ≈ 30 %, wetted area falls ≈ 11 % → hA ≈ +16 % |
| Turbulence (§2.1's stated requirement) | **Improved.** Re 7,400 → 8,300; further from the ≈ 2 L/min collapse threshold |
| `CP-15` mass ≤ 4.2 kg | **Still met**, margin 0.3 → 0.2 kg |
| `CP-02` 4.0 L/min at ΔP < 1.5 bar | **ADVERSE AND OPEN — see §7** |

## 7 · Residual — `CP-02` pressure drop

**One residual, and it is not closed by this disposition.** Reducing the depth raises velocity
and lowers hydraulic diameter, so ΔP rises materially. **No ΔP value is asserted anywhere in
this change.** The specification states none, `CP-02`'s declared verification method is a
**flow bench**, and inventing a figure here would be the defect class `VER-014` recorded four
times against `ECR-D-001`.

A note is placed in `spec/01` §2.1, in the frozen volume where a reader will meet it:
**`CP-02` shall be verified before build release.** The analyst estimate offered to the
approver — ΔP roughly 2.2× — was explicitly flagged as a derivation and not a specification
value, and it is recorded here as an estimate, not adopted.

**Owner:** Design Authority, by flow-bench test or delegated hydraulic analysis.
