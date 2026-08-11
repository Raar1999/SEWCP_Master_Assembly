# Post-Geometry Run — dependency graph and session record

> **Instance artifact.** Partition `project`-adjacent CAD record. Session `S-2026-08-11-02`.
> Geometry-complete baseline: commit `4d03041` — preserved, never rebuilt.
> Mission: continue the autonomous loop through assembly, drawings, BOM,
> manufacturing documentation, open-item disposition, final verification and
> repository stabilization.

## Orientation (boot B8)

- Framework AIEF 1.0.0, thirteen amendments; compiler stages 1–5 complete, Stage 6 NOT authorized (OQ-14, human-owner reservation).
- Lifecycle `LC-M04`, gate `LC-M04-EXIT` computed PASS C1–C7; profile `mechanical`.
- Ledger genesis, seq 0, reconciled. B2a unsatisfiable until Stage 6 — known, recorded.
- Bridge: add-in LIVE (heartbeat < 2 s), Fusion 2704.1.53, protocol `aief-cad/1`.
- All nine component volumes CAD-complete and verified from observed Fusion state;
  system interfaces 12/12 (`cad/runs/SYSTEM_INTERFACES.json`); exports digest-recorded
  (`cad/DELIVERABLES.md`).
- Roles are taken per-activity as the framework's agent contracts require; this record
  names the owning role for every stage below.

## Remaining dependency graph

| Stage | Class | Owner role | Depends on | Work |
|---|---|---|---|---|
| G0 Fusion tree cleanup | J | mechanical.cad-engineer | bridge ext: `list_documents` | Enumerate open/saved docs; classify REQUIRED / HISTORICAL / TEMPORARY / ORPHAN; remove only proven-safe; re-verify registry |
| G1 Assembly | B | mechanical.cad-engineer + design-engineer | G0; bridge ext: assembly ops | Master assembly from saved verified designs by native insert; placements from spec/00 §3.2 clocking + §4.2 Z build; observed verification; save; export |
| G2 Drawings | C | mechanical.cad-engineer + manufacturing-engineer | drawing layer (`src/aief_draw`); assembly drawing needs G1 | 10 part drawings + assembly drawing + masking sheet (S9/S10, DR-6) + SEWCP-901 flat pattern; every dimension provenance-tagged to parameter master / spec anchor / observed geometry |
| G3 BOM | D | mechanical.design-engineer | G1 | Indentured BOM from observed assembly occurrences + spec/00 §9 fastener schedule + volume sub-part tables; cross-checked 4 ways; CSV per PMP D4.7 |
| G4 Masks/edges/flat patterns | C/E | manufacturing-engineer | folds into G2 | Governing register (`cad/DELIVERABLES.md`): edge breaks/finishes are drawing callouts, not geometry; masking as drawn views; no un-authorized geometry injected |
| G5 Open items | F/G/H/I | per item | — | ECR-Q-011, coolant path 1.64 vs ≈2.2 m, CP-02, ECR-D-006, SR-D16, SEWCP-904, EC-D14 — disposition or preserve explicitly (§ below) |
| G6 Final deliverables | J | cad-engineer | G1–G3 | ASSEMBLY/, DRAWINGS/, BOM/, FINAL_PACKAGE/ under `D:\AIEF_CAD_OUTPUT\SEWCP\`; digests recorded in `cad/DELIVERABLES.md` |
| G7 Final system verification | I | qa-engineer discipline | G1–G6 | Observed-state verification: identities, placement, interfaces, stack-ups, materials, drawing/model, BOM/model, deliverable/registry consistency |
| G8 Stabilization | J/K | repository-engineer | G7 | Full test suite, gates, provenance, STATE.md, clean tree, local checkpoint commit. **No push before 2026-09-01.** |

## Deliverable authority

- Drawing set: PMP-001 §6 (P5) — 10 part drawings, master assembly drawing with
  balloons + indentured BOM, fastener/torque schedule sheet; drawing-stage register in
  `cad/DELIVERABLES.md`. ICD (D6.6), sequence sheets (D6.4), analysis reports (M5) and
  RFQ folders (M7) belong to later program gates (G5–G6 human review gates) and are
  NOT fabricated by this run beyond what the register carries.
- BOM: PMP-001 D4.7 (indentured CSV); content from observed assembly + spec §9.
- Formats: SVG (canonical, diffable) + PDF (matplotlib render) for drawings; CSV for BOM.

## G0 — Fusion tree cleanup (COMPLETE)

Observed via the new `list_documents` bridge op (hot-deployed extension,
canonical source `fusion_addin/AIEF_CAD_Bridge/bridge_ops_ext.py`).

| Artifact | Evidence | Class | Action |
|---|---|---|---|
| `SEWCP-300_HEATER_PLATE` lineage `…zyiGS3GmRO-n4u7QSfHLYQ` (v1, created 18:41:37) | Opened and observed: **0 bodies, 0 sketches**, 23 parameters — a first-save that landed before geometry; the verified PASS run `RUN-20260811T190752-d6ed1a` first-saved a *fresh* document (lineage `…t6Fu9jXoSIuqLifomxpPbQ`) whose observed `HP_BODY` volume 456 966.6 mm³ matches the run record exactly | ORPHAN — blank saved shell | **Renamed** to `ZZ-ORPHAN-BLANK-SHELL_SEWCP-300-20260811` — removed from the operational namespace, history preserved. Deletion dispatch was withheld (host permission layer refused it); rename is the safe equivalent and reversible |
| Open document `Untitled` (never saved, unmodified) | `list_documents`: saved=false, modified=false, blank | TEMPORARY | Closed without saving |
| Ten registry designs (`SEWCP-200_COOLING_PLATE` v5 … `SEWCP-1000_RETAINER` v2) | Present, uniquely named after cleanup; re-listed and verified | REQUIRED | Untouched |

Post-cleanup verification: 10/10 registry designs present with unique names;
no required occurrence or dependency existed against the removed items
(no assembly document existed yet). Bridge op additions this stage:
`list_documents`, `open_document`, `close_document`, `rename_data_file`,
`delete_data_file` (guarded), `insert_occurrence`, `transform_occurrence`,
`delete_occurrence`, `observe_assembly` — generic vocabulary, no component
knowledge, deployed via `scripts/install_fusion_addin.py`.

## G1 — Assembly (COMPLETE; two residues in controlled recovery)

- Bridge vocabulary extended (generic): `insert_occurrence` (+`use_latest_version`),
  `transform_occurrence`, `delete_occurrence`, `observe_assembly`, `update_references`,
  `data_file_info`, plus the document-management set from G0 and `rotate_x/z` placement
  math. Client layer: `src/aief_cad/assembly.py` (package loader, runner, observed-state
  verifier), CLI `assembly` + `op` subcommands, `tests/test_cad_assembly.py` (10 tests).
- **Integration findings while building** (each at the owning layer):
  - SEWCP-901 free-state neutral-S could not mate the CP-IF-8 land (pad at z=48/r=148
    vs land at z=20/r=128–146, sweep through the HP band). **Repaired** as a design-solution
    correction: installed-form S (aperture leg, R20 bend, run at 8.0, 45.069° arcs,
    pad ending at the land outer radius), RS-D03=180.0 closed exactly.
    Re-run `RUN-20260811T200254-ca7080` **PASS 15/15**, saved, re-exported.
  - **ECR-D-013** raised (strap hole pitch vs plate tap clocking) — owner-reserved.
  - **ECR-Q-012** raised (saddle mounting architecture) — owner-reserved.
- Master assembly `SEWCP-000_MASTER_ASSEMBLY` built from the ten saved verified designs
  by native insert: **19 occurrences, verification PASS**
  (`cad/runs/RUN-20260811T200919-f6cb5e/run.json`), grounded, saved to cloud.
  Every placement provenance-tagged in
  `cad/assembly/SEWCP-000_MASTER_ASSEMBLY.assembly.json`.
- **Residues (controlled recovery, `cad/BRIDGE_RESUME.md`):** OI-CAD-02 (CP occurrence
  rebind to the verified V5 + assembly STEP/f3d export) and OI-CAD-01 (SEWCP-600
  material repair) — blocked by the bridge outage after the programmatic Fusion restart;
  the add-in run state is a per-user Fusion setting no API or UI-automation path reached.
  One human click resumes; all subsequent commands are scripted.
- The CP data-loss incident is fully reconstructed in OI-CAD-02's register row: the
  17:35 save reported success but the cloud kept pre-vents/steel content; the verified
  state was rebuilt through the standard pipeline (`RUN-20260811T201850-e4b939`,
  **PASS 19/19**) and round-trip-verified as V5.

## G2 — Drawings (COMPLETE)

- Generic layer `src/aief_draw/` (model with **mandatory dimension provenance**,
  SVG + PDF renderers, provenance sidecars), `tests/test_draw_layer.py`.
- Definitions `drawings/defs/` + generator `drawings/generate.py`.
- Rendered to `D:\AIEF_CAD_OUTPUT\SEWCP\DRAWINGS\`: **10 part drawings**
  (SEWCP-200 two sheets incl. the masking sheet S9/S10 + DR-6 notes; SEWCP-901
  installed form + **flat pattern** with bend stations; each sheet carries its
  volume's critical-dimensions table parsed **verbatim** from the frozen spec)
  and the **master assembly drawing** (plan + observed-elevation + indentured
  BOM sheet + spec/00 §9 fastener/torque schedule sheet). 75 provenanced
  dimensions total; every one traces to a package parameter, spec anchor,
  observation or recorded decision via the sidecars.

## G3 — BOM (COMPLETE)

- `src/sedep/bom/builder.py` (SEDEP-PMP-002 §3 layout) builds the indentured BOM
  from the observed assembly + registry + frozen spec (fastener schedule parsed
  verbatim from spec/00 §9). Cross-checked four ways — occurrences, registry,
  deliverable manifest, quantities — **clean**. `tests/test_bom_builder.py`
  (7 tests, incl. omission/invention/quantity detection).
- `D:\AIEF_CAD_OUTPUT\SEWCP\BOM\SEWCP-000_BOM_RevA.csv` — 25 rows: 10 modelled
  parts (19 occurrences), 5 spec-only parts, 8 verbatim fastener rows, frozen
  Base Plate reference row. SEWCP-600 material defect flagged, not hidden.

## G5 — Open-item dispositions (this session)

| Item | Class | Disposition |
|---|---|---|
| ECR-Q-011 FSW rib | G/I | OPEN — supplier input; drawing carries the provisional-rib note; blocks build release only |
| Coolant path 1.64 m vs ≈2.2 m basis | F | Recorded deviation (MDR-001); consumed by the M5 analysis gate (thermal map / CP-11), not a CAD item; preserved |
| CP-02 flow-bench ΔP | G | **NOT CAD-VERIFIABLE** — physical verification carried, shared residual of ECR-D-002/-003 |
| ECR-D-006 manifest digest | H | Owner-reserved, untouched, excluded from LC-M04 by GATES.md |
| SR-D16 register degeneracy | F | Preserved as tabulated; candidate ECR-Q noted on the SEWCP-400 drawing; not raised without re-verification of the rows |
| SEWCP-904 shroud envelope | I | No dimensional authority in spec/08 — carried; BOM + drawing notes state it |
| EC-D14 He groove layout | I | No geometric authority in spec/04 — carried; EC drawing notes it |
| ECR-D-013 (new) | H | OPEN — owner ruling on 25.0 vs tap chord; both parts stay to their own volumes meanwhile. **`LC-M04-EXIT` C7 now computes FAIL on it, by construction** — an undispositioned ECR-D against `spec/**` fails the criterion, so the gate honestly reads NO until the owner rules. Listed under OPEN_ITEMS Blocking; index verified consistent by the gate |
| ECR-Q-012 (new) | H | OPEN — owner ruling on the saddle architecture; assembly placement marked provisional |
| OI-CAD-01 (new) | B | SEWCP-600 material repair scripted in BRIDGE_RESUME |
| OI-CAD-02 (new) | B/G | CP rebind + assembly export scripted in BRIDGE_RESUME |

## G7 — Final system verification (COMPLETE — 15/15 PASS)

`cad/scripts/final_system_verification.py` → `cad/runs/FINAL_SYSTEM_VERIFICATION.json`.
Every check recomputed from evidence: registry existence (10/10), assembly
verdict + 19 occurrences + §4.2 z-bands + wafer plane, interfaces 12/12,
materials (single known defect OI-CAD-01, flagged), BOM 4-way cross-check,
11 drawings with 75/75 sourced dimensions, manifest digests reproduce,
all four residues registered. PASS means: every CAD-verifiable property
verifies, and every non-verifiable or blocked item is explicitly carried.

## G8 — Stabilization (this checkpoint)

- Test suite: **744 pass, 2 fail** — the two pre-existing `ECR-D-006`
  failures (V-24/V-25 consume the drifted framework manifest; recorded at
  `VER-017` N-4). No test weakened, deleted or skipped; 21 tests added.
- `aief_gate`: C1–C6 PASS; **C7 FAIL on ECR-D-013 by design** (see G5).
  `aief_clearance` OK; `aief_params check` OK — 105 parameters.
- STATE.md boot budget: breached transiently by this session's additions
  (1309 > 1100), compressed back under cap; the V-09 recomputation test
  passes again.
- External deliverables verified outside git under `D:\AIEF_CAD_OUTPUT\SEWCP\`;
  digests in `cad/DELIVERABLES.md`; no generated artifact tracked.
- Push remains deferred until **2026-09-01** by standing instruction.

## Physical-verification boundary (unchanged by this run)

- CP-02 flow-bench ΔP: **NOT CAD-VERIFIABLE** — carried.
- FSW minimum rib (ECR-Q-011): supplier input — carried OPEN.
- Hardware mass confirmation, bond C-scan, CMM stack measurement: physical — carried.

## S-2026-08-11-05 — Owner-delegated engineering resolution (final)

Under the owner's written delegation (mission 2026-08-11 §1), all four
carried engineering items were resolved with full provenance
(`.ai/project/decisions/DECISIONS_S-2026-08-11-05.md`, APR-029…APR-032):

- **ECR-D-013 → A**: strap holes tap-coincident (29.94 centres); SEWCP-901
  rebuilt PASS 15/15, re-exported.
- **ECR-Q-012 → plate-hung hanger**: SEWCP-902 re-architected Rev B and
  built PASS 15/15; CP gains 2 bracket taps. The first tap placement
  (RF-IF-3's literal window) was caught **by the ACC-VOL check** colliding
  with the choke slots; the feasibility sweep proved the whole ±40 mm
  window occupied and the corrected r = 150, 88°/122° placement was
  re-issued (DEC-02 addendum). The failed attempt auto-reverted the plate
  (failure disposition in production).
- **ECR-Q-011 → rib 5.0 confirmed** with an FSW tool-envelope constraint
  (spec/01 §6 step 5); channel unchanged.
- **Coolant path → design-basis estimate, 1.64 m accepted** with margin
  derivation; CP-02/CP-11 remain CAD COMPLETE — PHYSICAL VERIFICATION
  REQUIRED.

Assembly re-integrated (19 occurrences, **PASS**, 7.6997 kg, saved,
STEP+f3d re-exported); drawings 200/901/902(Rev B)/000 regenerated; BOM
regenerated CLEAN against `cad/runs/ASSEMBLY_S-2026-08-11-05/`.
**FINAL SYSTEM VERIFICATION: 19/19 PASS.** Gate: `LC-M04 CAD-READY: YES`
(C1–C7). Transport-layer `drain()` id-parsing defect found and fixed with
the historical queue sweep recorded.
