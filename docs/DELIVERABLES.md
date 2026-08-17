# Engineering Deliverables

*What was actually produced. 61 files, 4,995,097 bytes, every digest registered in
[`cad/DELIVERABLES.md`](../cad/DELIVERABLES.md) and checked in **both directions** by
`python -m aief_deliverables` — the register must reproduce the tree, and the tree must contain
nothing unregistered.*

```
$ PYTHONPATH=src python -m aief_deliverables
registered deliverables: 61
subtrees checked:        cad/exports/step, cad/exports/stl, cad/bom, drawings/assembly, drawings/parts
octets accounted for:    4995097
DELIVERABLES OK - 61 registered, 61 reproduce, 0 unregistered; the agreement is bi-directional
```

---

## 1 · Composition

| Class | Count | Bytes | Location |
|---|---:|---:|---|
| Neutral geometry — **STEP** | 11 | 2,481,057 | `cad/exports/step/` |
| Tessellated — **STL** | 10 | 1,698,540 | `cad/exports/stl/` |
| Drawing sheets — **SVG** | 14 | 315,916 | `drawings/assembly/`, `drawings/parts/` |
| Drawing sheets — **PDF** | 14 | 477,697 | `drawings/assembly/`, `drawings/parts/` |
| Drawing **provenance sidecars** | 11 | — | alongside each drawing document |
| **BOM** — indentured, Rev A | 1 | 4,859 | `cad/bom/SEWCP-000_BOM_RevA.csv` |
| **Total** | **61** | **4,995,097** | |

## 2 · Component CAD — 10 part designs

Verified against observed Fusion model state; each has a STEP, an STL and a drawing document.

| Part | Name | Qty | Material | Spec |
|---|---|---:|---|---|
| `SEWCP-200` | Cooling Plate | 1 | 6061-T6 | `spec/01` |
| `SEWCP-300` | Heater Plate | 1 | 6061-T6 | `spec/02` |
| `SEWCP-400` | Support Ring | 1 | Al₂O₃ 99.5 % | `spec/03` |
| `SEWCP-500` | ESC Puck | 1 | Al₂O₃ 99.6 % | `spec/04` |
| `SEWCP-600` | Lift Pin | 3 | Al₂O₃ 99.8 % | `spec/05` |
| `SEWCP-700` | Alignment Pin | 6 | Ti-6Al-4V | `spec/06` |
| `SEWCP-800` | Port Body | 1 | 316L SST | `spec/07` |
| `SEWCP-901` | RF Strap | 1 | C10100 OFHC | `spec/08` |
| `SEWCP-902` | Saddle | 1 | 6061-T6 | `spec/08` §5.2 |
| `SEWCP-1000` | Retainer | 3 | 6061-T6 | `spec/09` |

Nine specified components; `SEWCP-900` (RF Feedthrough Bracket) is realised as two designs,
`-901` and `-902`. `SEWCP-100` Base Plate is **frozen and out of scope** — it appears in the BOM
as a `REF` datum reference and is excluded from the assembly by Design Rule DR-1.

## 3 · Assembly — `SEWCP-000_MASTER_ASSEMBLY`

| | |
|---|---|
| Occurrences | **19**, each placed, grounded, with source design and version |
| Total mass | **7.6997 kg** (observed, summed over occurrences) |
| Verification | `ASSEMBLY_S-2026-08-11-05` → **PASS**; interfaces **12/12**; final system verification **19/19** |
| Neutral geometry | `cad/exports/step/SEWCP-000_MASTER_ASSEMBLY.step`, 1,262,728 bytes, digest `8a53f53f0e64d372` |

The Z stack verifies station by station against `spec/00` §4.2: `SEWCP-400` [−0.3, 20.0],
`SEWCP-200` [20.0, 40.0], `SEWCP-300` [41.5, 49.5], `SEWCP-500` [49.9, 55.9], hanger [8.0, 20.0],
wafer plane at 55.920 via a 0.020 mesa.

## 4 · Drawings — 11 documents, 14 sheets

| Document | Sheets | Content |
|---|---:|---|
| `SEWCP-000-DRW-001` | 3 | Sh 1 plan with balloons and occurrence table · Sh 2 section elevation with the Z stack, datums and the indentured BOM · Sh 3 joint / fastener schedule and notes |
| `SEWCP-200-DRW-001` | 2 | Cooling Plate — top and section A-A |
| `SEWCP-300` · `-400` · `-500` · `-600` · `-700` · `-800` · `-901` · `-902` · `-1000` | 1 each | component detail |

Generated deterministically by `drawings/generate.py` — two consecutive renders were verified
byte-stable across 39 files.

**79 dimensions, 0 unsourced.** Every dimension on every sheet carries a provenance entry naming
where the number came from:

```json
{ "sheet": "SEWCP-200-DRW-001 Sh 1", "view": "TOP", "kind": "diameter",
  "label": "Ø320 (CP-D01)",
  "source": "parameter:cp_od (params/generated/SEWCP-200.csv)" }

{ "sheet": "SEWCP-200-DRW-001 Sh 1", "view": "TOP", "kind": "note",
  "label": "COOLANT IN 255° / OUT 285°, RADIAL",
  "source": "spec/00 §3.2 coolant 255°(in)/285°(out)" }
```

A dimension whose source could not be named would fail `FSV-DRAWINGS`, which asserts
`unsourced dims: 0`.

## 5 · BOM — `cad/bom/SEWCP-000_BOM_RevA.csv`

Indentured, Rev A, cross-checked four ways against the assembly run record. Each line carries
part number, quantity, material, **specification source**, CAD state, deliverable path and notes
— including the honest ones:

- `SEWCP-401` clamp ring: *"per `ECR-D-016` the tabulated Ø318.0/Ø286.0 form cannot be placed at
  all — it intersects the web. Rev B item."*
- `SEWCP-904` deposition shroud: *"NO dimensional authority in `spec/08` — requirement gap,
  carried; not modelled, not drawn."*

Of 25 lines: 1 assembly, **10 `verified model`**, **13 `spec-only`** (specified, quantified and
sourced, but with geometry deferred — the fastener schedule and four deferred parts), and 1
frozen reference. The BOM states each line's CAD state explicitly, rather than implying that
everything specified was modelled.

## 6 · Verification evidence (tracked, not deliverables)

| Artifact | Contents |
|---|---|
| `cad/runs/RUN-*/run.json` | **36 component runs — 18 PASS, 18 FAIL.** Every dispatched command, every observation Fusion returned, every acceptance finding, every escalation |
| `cad/runs/ASSEMBLY_S-2026-08-11-05/run.json` | observed occurrence list with per-occurrence bbox, mass, transform and source version |
| `cad/runs/SYSTEM_INTERFACES.json` | 12 interface checks with computed gaps |
| `cad/runs/FINAL_SYSTEM_VERIFICATION.json` | the 19 system-level checks |
| `cad/runs/REPAIRS_S-2026-08-11-04.json` · `LINEAGE_ROSTER_*.json` | repair and document-lineage records |
| `analysis/SEDEP-RPT-001…006` | tolerance stack, thermal, structural, electrical/RF, flow, open-item closure |
| `.ai/project/verification/PVR-001` | physical verification matrix — **containing no test result, because no hardware exists** |

## 7 · What is deliberately absent

| Not here | Why |
|---|---|
| **Parametric `.f3d`** | `SEDEP-PMP-002` §3.1 — the parametric source of record is Fusion cloud versioning; git holds the neutral record. `.f3d`/`.f3z`/`.f2d` are gitignored by policy, not by accident |
| **Tokenizer artifacts** | third-party binaries; pinned by SHA-256 in `core/MANIFEST.lock` and fetched by the operator, never vendored |
| **`cad/bridge/queue|obs|state/`** | transport, not record — every command and observation is copied verbatim into the tracked run files |
| **Physical test data** | none exists |
