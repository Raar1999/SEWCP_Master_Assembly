# Exported CAD Deliverables — provenance

External output root: `D:\AIEF_CAD_OUTPUT\SEWCP\` (outside this repository by
rule; the repository records provenance, never duplicates the exports).
Exported by the bridge `export_model` operation from the saved Fusion designs,
2026-08-11, session `S-2026-08-11-05`.

| Component | Design (Fusion) | File | Bytes | sha256 (first 16) |
|---|---|---|---|---|
| SEWCP-200 | `SEWCP-200_COOLING_PLATE` (lifecycle-saved; runs REQ-001..005, evidence `cad/runs/`) | `SEWCP-200\step\SEWCP-200_COOLING_PLATE.step` | 467010 | `9e4b92ea236fa283` |
| SEWCP-200 | same | `SEWCP-200\stl\SEWCP-200_COOLING_PLATE.stl` | 667684 | `8be0a2b2ba77134e` |
| SEWCP-700 | `SEWCP-700_ALIGNMENT_PIN` (first-saved by the lifecycle layer; run `RUN-20260811T180247-cc2a7c`, PASS 25/25) | `SEWCP-700\step\SEWCP-700_ALIGNMENT_PIN.step` | 17750 | `59544dcd1dc1162b` |
| SEWCP-700 | same | `SEWCP-700\stl\SEWCP-700_ALIGNMENT_PIN.stl` | 47484 | `2e11e883034a39ec` |

Re-export at any time: dispatch `export_model` against the adopted design;
digests change only when the model does.
