# SEDEP-RPT-003 — `SR-07` / `AP-08` re-run at the as-modelled stack mass

> **Instance artifact.** Partition `analysis`. Filed `S-2026-08-17-01`, discharging
> `OI-C-15` §6.1 (`PVR-001` §6.1).
>
> **Computed, not transcribed.** Every figure below is produced by
> `PYTHONPATH=src python -m aief_analysis` from `src/aief_analysis/loads.py`, and is attacked
> by `tests/test_analysis_oi_c_15.py`. **This is an analysis, not a physical verification** —
> `SR-07` and `AP-08` declare method *Analysis*, which is why they are dischargeable at the
> desk, and nothing in this report is evidence about a physical article.

---

## 1 · Why this was owed

`SR-07` (*static load capacity — 7.5 kg stack + 5 g in all axes, SF ≥ 3*) and `AP-08`
(*lateral load capacity — 5 g on the 7.5 kg stack = 123 N per pin*) are both declared
**Analysis**, and both analyses of record were run against a **7.5 kg** design-basis stack.

The assembly models to **7.69973 kg** — `cad/runs/ASSEMBLY_S-2026-08-11-05/run.json`, 19
occurrences, verdict PASS, read here as the sum of the per-occurrence masses and checked
against the record's own `total_mass_kg` before use. That is **+2.66 %**, and the analyses of
record were never re-run at it. `PVR-001` §6.1 recorded the gap; this report closes it.

## 2 · The load

| | Design basis | As modelled |
|---|---|---|
| Stack mass | 7.50000 kg | **7.69973 kg** |
| Stack weight | 73.58 N | **75.53 N** |
| Lateral load at 5 g | 367.88 N | **377.68 N** |
| **Per pin**, 3 per interface (`AP-01`) | **122.62 N** | **125.89 N** |

`g = 9.81 m/s²`, and it is **derived rather than chosen**: `spec/06` `AP-08` states *"5 g on
the 7.5 kg stack = 123 N per pin"*, and 7.5 × g × 5 / 3 = 123 fixes g at 9.81. The model
reproducing 122.62 N is the first control — it recovers the specification's own published
figure before it is used on anything new.

## 3 · Results at the as-modelled mass

| Req | Case | Stress | Capability | Margin | **Mass at SF = 3** |
|---|---|---|---|---|---|
| `SR-07` | Ring web, dead weight (compression) | 0.0267 MPa | 2 500 MPa | 93 660× | 240 400 kg |
| `SR-07` | Ring web, 5 g lateral at the web root (flexure) | 0.0811 MPa | 350 MPa | 4 316× | 11 076 kg |
| `AP-08` | Pin shear, Ti-6Al-4V | 4.453 MPa | 550 MPa | 124× | 317 kg |
| `AP-08` | Bearing on slot wall, Al₂O₃ (ring interface) | 8.393 MPa | 2 500 MPa | 298× | 764 kg |
| **`AP-08`** | **Bearing on slot wall, 6061 (heater interface)** | **8.393 MPa** | **276 MPa** | **32.9×** | **84.4 kg** |

Capabilities and areas are `spec/06` §2.3's and `spec/03` §2.2's, cited at the constant in the
source. Two further controls: the ring cases reproduce `spec/03` §2.2's published *"~96,000×"*
and *"~4,400×"* at the design basis, to within the precision those figures are stated at.

## 4 · The figure that settles it

**The governing case does not reach SF = 3 until 84.4 kg** — **eleven times** the as-modelled
stack mass.

That is the answer to the question `OI-C-15` actually asked. The concern was not that 2.66 %
might fail the requirement; it was that the analysis of record had not been run at the mass
the design has, *and that the unmodelled `spec-only` BOM lines would push it higher still*.
Both are disposed of by the same number:

- **The +2.66 % is immaterial**: the governing margin moves 33.7× → 32.9×.
- **No bound on the unmodelled mass is needed, and none is asserted.** `SEWCP-301` (16 Ti
  washers), `SEWCP-401`, `SEWCP-601` (3 bushings), `SEWCP-903` and ~40 A4-70 fasteners would
  have to add **76.7 kg** to threaten the governing case. Two of those parts — `SEWCP-401` and
  `SEWCP-904` — have no dimensional authority at all, so their mass **cannot** be computed
  without inventing dimensions, and this report does not. It does not need to.

`SR-07`'s own governing case is three orders further away still, at ~11 tonnes.

## 5 · A correction to `PVR-001` §6.1's reasoning

§6.1 says the 2.66 % is *"absorbed by `ECR-D-007`'s recorded 4.4–6.9× margin"`*. **That margin
does not apply here.** It is the hoop stress in the counterbore ligament arising from a
Ø12.000 **k6 interference fit** — and `ECR-D-009`'s disposition removed the interference, the
flange becoming `h6` clearance, *"so the stress term goes to zero"* (`ECR-D-007` §9). The
applicable margins are `spec/06` §2.3's, recomputed above.

**§6.1's conclusion was right and one of its citations was not**, which is worth recording
because a reader checking the cited margin would have found a number that no longer describes
the design.

## 6 · Verdict, and its exact scope

**`SR-07` and `AP-08` are DISCHARGED at the as-modelled mass**, by analysis, with an eleven-fold
margin in mass terms on the governing case.

**What this does not establish.** Nothing physical. `SR-07`'s capability figures are handbook
values for 99.5 % alumina and `AP-08`'s for Ti-6Al-4V, applied to as-modelled geometry; the
ring's actual flexural strength, the actual bearing behaviour of an anodised 6061 slot wall,
and the actual preload the Belleville stacks deliver are all properties of an article that does
not exist. `PVR-001` continues to record them as such.
