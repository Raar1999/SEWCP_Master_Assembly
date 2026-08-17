# Freeze Registry

> **Instance artifact.** Emitted by aief-compile Stage 3 from `framework.manifest.json` and live repository state.
> Partition `project` — never touched by framework upgrade. Owner `chief-systems-engineer`. Mutability mutable.

---

Governed by `core/laws/LAW-01_architecture_freeze.md`.

A change to any registered artifact without an approved ECR and a human approval artifact is a **freeze violation**.

## Scope

Declared by `AIEF-AMD-008` §AMD-21. **This registry covers the repository partitions outside `.ai/` that are declared frozen: `spec/` and `framework/`.**

| Partition | Covered by | Not by |
|---|---|---|
| `spec/`, `framework/` | **this registry** | — |
| `core/` | `core/MANIFEST.lock` and boot step B2a (Compiler Stage 6) | this registry |
| `project/`, `adapters/` | nothing — mutable by design | this registry |

**Registration criterion** for `framework/` (AMD-21): an artifact is registered if it is an *authorising instrument* for a change to a frozen artifact, or the *record of the authority* under which such a change was made.

## Hash constructions

Both are declared normatively in `framework.manifest.json` → `metadata.reproducible.digest_constructions`. Restated here at the point of use.

**DC-1 — per artifact.** SHA-256 over normalised content: decode UTF-8 stripping any byte-order mark; convert `CRLF` and lone `CR` to `LF`; strip trailing whitespace from every line; remove trailing blank lines; append exactly one terminal `LF`; encode UTF-8. Output 64 lowercase hex.

**DC-2 — set aggregate.** SHA-256 over the concatenation of one record per registered artifact, each record `<path>` `<SP>` `<digest>` `<LF>`, records sorted ascending by the UTF-8 octet sequence of `<path>`. UTF-8, no header, no trailer, no BOM. The aggregate is not part of its own preimage. Empty registry: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

> **The order of rows in the table below is not the hashing order.** DC-2 sorts by path. The table is grouped for reading.

## Registered artifacts (31)

| Path | DC-1 digest |
|---|---|
| `spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md` | `fa2a84ccf3a837176eade00c502916a7a1492c9c58785448a4c26ba0fbaab95d` |
| `spec/01_SEWCP-200_Cooling_Plate.md` | `a3afa3eb41ee2aba7181fc4ae778a29d12c396194f1252640cc4e02e4b9f2230` |
| `spec/02_SEWCP-300_Heater_Plate.md` | `0290580066829963de1c9bbbd059f5f088e442031d679cf4ddf5046693d66aef` |
| `spec/03_SEWCP-400_Chuck_Support_Ring.md` | `a2f951a1c749b688141d8245f8575ed6aabf28df03b55788a0d762f4e6c7dcbf` |
| `spec/04_SEWCP-500_Electrostatic_Chuck.md` | `4a8c39325a2edd0e03ba06b802afb5f7aaf9bb6c4552b22b3b72a67121afaca1` |
| `spec/05_SEWCP-600_Lift_Pins.md` | `39a841104a2752d9d0dd7e309e599f7735ae74cb919739e5edb3975d8470873d` |
| `spec/06_SEWCP-700_Alignment_Pins.md` | `75cda88184e5ae50acd05fb86dfb61ffc6238219462e8854120c05f14d04f396` |
| `spec/07_SEWCP-800_Vacuum_Port.md` | `7558bc5b0f613ab9184d66dba6afd6674214d33302775eee2515bd25c8122afe` |
| `spec/08_SEWCP-900_RF_Feedthrough_Bracket.md` | `710f6e14bf8b40498a4ec91ea65b760fc55eea99507513a93feb85bb6aa55414` |
| `spec/09_SEWCP-1000_Temperature_Sensor_Bracket.md` | `391e5e6b403e17be30028d28875a2b291a100b7a05e7038645353e78b63764dd` |
| `spec/README.md` | `1d7720723ddd42028a9536ec20cfb50a9a8b803bc3172423b31f108a7f93416c` |
| `framework/AIEF-FRZ-001_Framework_Architecture_Freeze_1.0.0.md` | `a1b0a51c58138156a18598c2cb9bcb3a6066b0fcd35ea10203d5d17c450023f4` |
| `framework/AIEF-ADR-001_Authority_Decision_Record.md` | `935d169d0bbfd11c9d73c9f256de710d3b67477ebc1c458b6aa07c5e6a2362cb` |
| `framework/AIEF-ADR-002_Authority_Decision_Record.md` | `e79e9fc8b0e0b9e07493d50c203084391802eb096ee2239693c229efdec696f3` |
| `framework/AIEF-AMD-001_Architecture_Amendments_1.0.0.md` | `1d3c42d48f366a1be02c6fe3bd9281c356fd1063ec3c4c4b179efc9fb8744329` |
| `framework/AIEF-AMD-002_Architecture_Amendments_CMP-BLOCK-014.md` | `83a69de9e6b9e0a6d2dc5f46614bcd0a8170882c4d0d900a9872442d9b382591` |
| `framework/AIEF-AMD-003_Architecture_Amendments_OI-F-01_OI-F-02.md` | `d1d2cf76425974cc8b7804005d7e5a52f90ad8be16edfbd5480c03709fcc5e4b` |
| `framework/AIEF-AMD-004_Repository_Engineer_Autonomy.md` | `9171059e930cca9365abd0c2bad5db01fa3a790733c6f663ef93cc79de255dac` |
| `framework/AIEF-AMD-005_Host_Bootstrap_Artifacts.md` | `f8a4ab53eec480e951fe17cb6590b16fd311ce4e2639a83d2d8bab6fd05f946a` |
| `framework/AIEF-AMD-006_Mechanical_CAD_Engineer.md` | `ece7c0c780ffd0c006f508ddcc624a416d1f11ff24d4addb3dc9be61c36f38e9` |
| `framework/AIEF-AMD-007_Compiler_Stage_State_Field.md` | `860a1c7e8f18a05d032fe21cd2dfaeac4580765de1d225f9c260def8484caa9e` |
| `framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md` | `192ff86128dadfc8382f1894e1a38713f7321ee83aff7891d7e885c31c9dd71e` |
| `framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md` | `86c8be7f0eafb441c55ad5d5033f6e8e4e684350da262557539e6291b68f2c97` |
| `framework/AIEF-AMD-010_Stage_6_Constructions_and_Preflight_Dispositions.md` | `486be10eb3bea89fb8c6c99949f1bb48e884cb556879e594cdd778dac5b0b829` |
| `framework/AIEF-AMD-011_Software_Role_Enablement.md` | `59ecb5eb922f44a55cc42e51663dae9ee251269790958ee27ad93c1ba2ebaa53` |
| `framework/AIEF-AMD-012_DC-4_Coverage_of_Enabled_Role_Artifacts.md` | `12b7f1b003fd190d99948e378a630d85e405e3c041da31eb8204bb00e702f1d0` |
| `framework/AIEF-AMD-013_Boot_Budget_Determination_and_Stage_6_Build_Constructions.md` | `3d1e6b60c9e9c3ebda88cd073f0a717dc6506cc41388f0568eede8d0a6b99e78` |
| `framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md` | `07ced7582c7dafc8649eb8ac0736d1587ba4cc38c30f11c929240809be639945` |
| `framework/AIEF-AMD-015_Lock_Boot_Read_Prefix_And_Member_Order.md` | `195302214a14ab38d9c595dee35c5eb6a930f5f90c4c70854488ff62207c6ae4` |
| `framework/SCH-framework-manifest.schema.json` | `ee3d0bdf37156541c13ece46fec9172dabd93e98f32cb88c0ae7a2adff4bb25f` |
| `framework/framework.manifest.json` | `759f774b727c43a0f96845aa5ac12a05a1158b60c27ba8b31d963a33cde74e3b` |

**Not registered, by ruling.** `framework/AIEF-ARCH-001_AI_Engineering_Framework_Architecture.md` — superseded by `AIEF-FRZ-001`, authorises nothing, cited by nothing as a live authority (AMD-21, APR-003).

Per-artifact verification after this change: **29 of 29 verified at the time of that change.**

> **Superseded by measurement, 2026-08-09 (VER-014 F7).** The registry now verifies **28 of 29**. `framework/framework.manifest.json` is registered at `8af8971b…a7e42ff7` and the artifact normalises to `920eb6ee…37814090` — this is the open defect **ECR-D-006**, raised 2026-08-08, and it pre-dates the spec/01 re-registration below. The DC-2 aggregate is computed over the **registry rows**, not the tree, so it reproduces exactly while one registered artifact has drifted. A reader who checks only `frozen_set_hash` — which is what `STATE.md` exposes at boot — gets a green result over content that has changed. That is the failure mode `OI-V-02` predicts and it is now realised; `V-24` remains declared but unimplemented.
>
> **Superseded again by measurement, 2026-08-11 (`S-2026-08-11-06`).** The paragraph above is retained verbatim; it was true when written and its two closing clauses have since been overtaken — `V-24` **is** implemented, and it is what found the second half of the defect. The registry now verifies **30 of 30**. `ECR-D-006` is **dispositioned A** under owner-delegated engineering authority: the manifest row is re-registered at its measured `920eb6ee…37814090` (`APR-033`) and `AIEF-AMD-014` is registered at `07ced758…be639945` (`APR-034`), which `AIEF-AMD-014` § *Blast Radius* required under the AMD-21 criterion and which **was never done** — `APR-014` and `APR-015` were never filed. **One thing the paragraph above said is still true and is not repaired:** the `AIEF-AMD-013` intermediate state `8af8971b…a7e42ff7` remains unreproducible, because the bytes it names were never committed. That residual is recorded, not closed. Full record: [`ecr/ECR-D-006`](ecr/ECR-D-006_Framework_Manifest_Registry_Divergence.md) §§8–10.

## Registration history

| Date | Artifact | Change | Authority |
|---|---|---|---|
| 2026-08-07 | all 16 | Initial registration | Release 0.3, commit `a45823d` |
| 2026-08-08 | `framework/framework.manifest.json` | `c33e574a…fed01799` → `f72485c2…07f31467` | ECR-D-005 disposition A, approval [`approvals/APR-001_Reregister_Framework_Manifest.md`](approvals/APR-001_Reregister_Framework_Manifest.md) |
| 2026-08-08 | `framework/framework.manifest.json` | `f72485c2…07f31467` → `636cf22b…14b38d3c` | AIEF-AMD-008 rulings AMD-16…AMD-20, approval [`approvals/APR-002_Amend_Framework_Manifest_AMD-008.md`](approvals/APR-002_Amend_Framework_Manifest_AMD-008.md) |
| 2026-08-08 | ADR-001, ADR-002, AMD-003…AMD-008 | **8 added** — registry scope expansion | AIEF-AMD-008 §AMD-21, approval [`approvals/APR-003_Register_Framework_Amendments_and_ADRs.md`](approvals/APR-003_Register_Framework_Amendments_and_ADRs.md) |
| 2026-08-08 | § Aggregate | Construction declared; aggregate recomputed for the first time under a declared method | AIEF-AMD-008 §AMD-16, disposing ECR-Q-001 |
| 2026-08-08 | `framework/framework.manifest.json` | `636cf22b…14b38d3c` → `9611d547…9813e557` | AIEF-AMD-009 rulings AMD-23/AMD-24, disposing ECR-Q-003 and OI-C-03; approval [`approvals/APR-004_Amend_Framework_Manifest_AMD-009.md`](approvals/APR-004_Amend_Framework_Manifest_AMD-009.md) |
| 2026-08-08 | `framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md` | **1 added** — authorising instrument, AMD-21 criterion | Approval [`approvals/APR-005_Register_AIEF-AMD-009.md`](approvals/APR-005_Register_AIEF-AMD-009.md) |
| 2026-08-08 | `framework/framework.manifest.json` | `9611d547…9813e557` → `ae16ccac…9d8395aa` | AIEF-AMD-010 rulings AMD-25…AMD-33, disposing Stage 6 pre-flight OQ-1…OQ-10 and OQ-12; approval [`approvals/APR-006_Amend_Framework_Manifest_AMD-010.md`](approvals/APR-006_Amend_Framework_Manifest_AMD-010.md) |
| 2026-08-08 | `framework/AIEF-AMD-010_Stage_6_Constructions_and_Preflight_Dispositions.md` | **1 added** — authorising instrument, AMD-21 criterion | Approval [`approvals/APR-007_Register_AIEF-AMD-010.md`](approvals/APR-007_Register_AIEF-AMD-010.md) |
| 2026-08-08 | `framework/AIEF-AMD-011_Software_Role_Enablement.md` | **1 added** — authorising instrument, AMD-21 criterion; no manifest re-registration accompanies it (AMD-37 — manifest not amended) | Approval [`approvals/APR-009_Register_AIEF-AMD-011.md`](approvals/APR-009_Register_AIEF-AMD-011.md) |
| 2026-08-08 | `framework/framework.manifest.json` | `ae16ccac…9d8395aa` → `f06125d2…69707638` | AIEF-AMD-012 ruling AMD-39, disposing OI-C-06 — DC-4 coverage of enabled-role agent artifacts; approval [`approvals/APR-010_Amend_Framework_Manifest_AMD-012.md`](approvals/APR-010_Amend_Framework_Manifest_AMD-012.md) |
| 2026-08-08 | `framework/AIEF-AMD-012_DC-4_Coverage_of_Enabled_Role_Artifacts.md` | **1 added** — authorising instrument, AMD-21 criterion | Approval [`approvals/APR-011_Register_AIEF-AMD-012.md`](approvals/APR-011_Register_AIEF-AMD-012.md) |
| 2026-08-08 | `framework/framework.manifest.json` | `f06125d2…69707638` → `8af8971b…a7e42ff7` | AIEF-AMD-013 rulings AMD-42…AMD-48 — V-09 measured domain, lock JSON layout, `build_provenance` content, lock self-measurement, archive entry types, BINDING pin write, DC-1 empty content, AMD-33 run-fixed values; approval [`approvals/APR-012_Amend_Framework_Manifest_AMD-013.md`](approvals/APR-012_Amend_Framework_Manifest_AMD-013.md) |
| 2026-08-08 | `framework/AIEF-AMD-013_Boot_Budget_Determination_and_Stage_6_Build_Constructions.md` | **1 added** — authorising instrument, AMD-21 criterion; also the record of the CMP-BLOCK-006 determination and of the OQ-15 reservation (AMD-41, which itself amends nothing) | Approval [`approvals/APR-013_Register_AIEF-AMD-013.md`](approvals/APR-013_Register_AIEF-AMD-013.md) |

| 2026-08-10 | `spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md` | `baf9ae50…` → `fa2a84cc…` | LC-M04 specification coherence package; approval [`APR-021`](approvals/) |
| 2026-08-11 | `spec/01_SEWCP-200_Cooling_Plate.md` | `9e825580…` → `a3afa3eb…` | ECR-Q-012 DEC-02 addendum — bracket taps re-placed to r = 150, 88°/122° after the ACC-VOL collision with the choke slots; approval [`approvals/APR-031_Cooling_Plate_bracket_taps_replaced.md`](approvals/APR-031_Cooling_Plate_bracket_taps_replaced.md) |
| 2026-08-11 | `spec/08_SEWCP-900_RF_Feedthrough_Bracket.md` | `b69b0c48…` → `710f6e14…` | RF-IF-3 mounting window corrected (same addendum); approval [`approvals/APR-032_RF_Bracket_mounting_window_corrected.md`](approvals/APR-032_RF_Bracket_mounting_window_corrected.md) |
| 2026-08-11 | `spec/01_SEWCP-200_Cooling_Plate.md` | `55b47ca3…` → `9e825580…` | ECR-Q-012 DEC-02 (two RF-hanger bracket taps added to CP-IF-8) and ECR-Q-011 DEC-03 (FSW rib-pass tool envelope, §6 step 5); owner-delegated engineering authority exercised by Claude; approval [`approvals/APR-029_Cooling_Plate_hanger_taps_and_FSW_envelope.md`](approvals/APR-029_Cooling_Plate_hanger_taps_and_FSW_envelope.md) |
| 2026-08-11 | `spec/08_SEWCP-900_RF_Feedthrough_Bracket.md` | `cfe93cd6…` → `b69b0c48…` | ECR-D-013 DEC-01 (RS-D07 holes tap-coincident) and ECR-Q-012 DEC-02 (SB rows re-dimensioned to the plate-hung hanger); owner-delegated engineering authority exercised by Claude; approval [`approvals/APR-030_RF_Bracket_interface_resolution.md`](approvals/APR-030_RF_Bracket_interface_resolution.md) |
| 2026-08-10 | `spec/01_SEWCP-200_Cooling_Plate.md` | `36e8d35b…` → `55b47ca3…` | LC-M04 specification coherence package; approval [`APR-020`](approvals/) |
| 2026-08-10 | `spec/02_SEWCP-300_Heater_Plate.md` | `ab36e082…` → `02905800…` | LC-M04 specification coherence package; approval [`APR-022`](approvals/) |
| 2026-08-10 | `spec/03_SEWCP-400_Chuck_Support_Ring.md` | `b00d5289…` → `a2f951a1…` | LC-M04 specification coherence package; approval [`APR-024`](approvals/) |
| 2026-08-10 | `spec/06_SEWCP-700_Alignment_Pins.md` | `0d2aa747…` → `da702fe0…` | LC-M04 specification coherence package; approval [`APR-023`](approvals/) |
| 2026-08-10 | `spec/07_SEWCP-800_Vacuum_Port.md` | `1b7b5914…` → `7558bc5b…` | LC-M04 specification coherence package; approval [`APR-025`](approvals/) |
| 2026-08-10 | `spec/README.md` | `95da15c6…` → `1d772072…` | LC-M04 specification coherence package; approval [`APR-026`](approvals/) |
| 2026-08-10 | `spec/06_SEWCP-700_Alignment_Pins.md` | `da702fe0…` → `75cda881…` | `VER-015` F-08 — the `ECR-D-009` locator torque 2.5 → 1.2 N·m had been applied to `spec/01` and **not** to the governing volume, leaving two contradictory torques for one joint; approval [`approvals/APR-027_Alignment_Pin_torque_correction.md`](approvals/APR-027_Alignment_Pin_torque_correction.md), superseding `APR-023` |
| 2026-08-09 | `spec/01_SEWCP-200_Cooling_Plate.md` | `f2d228e1…8d0f2a5355` → `a39e4b24…536b7db5` | `VER-014` R10(a) — an unauthorised 8.0 mm M4 tap depth struck; `CP-D09a`/`CP-D10a` now read `depth TBD — ECR-D-007`; approval [`approvals/APR-018_Strike_Unauthorised_Tap_Depth.md`](approvals/APR-018_Strike_Unauthorised_Tap_Depth.md) |
| 2026-08-09 | `spec/01_SEWCP-200_Cooling_Plate.md` | `a637ae18…be7f8b9b54` → `f2d228e1…8d0f2a5355` | ECR-D-001 / `VER-014` F1 — the surviving superseded-geometry row in the §8 surface-finish table; approval [`approvals/APR-017_Alignment_Pin_Clerical_Correction.md`](approvals/APR-017_Alignment_Pin_Clerical_Correction.md) |
| 2026-08-09 | `spec/01_SEWCP-200_Cooling_Plate.md` | `3ae384bd…c0e6a2597` → `a637ae18…be7f8b9b54` | ECR-D-001 disposition A — alignment pin interface: SEWCP-700 governs; the press-fit dowel bore is corrected to a Ø12.0 H7 × 3.0 locator counterbore with an M4 retention thread, and Datums B/C now name a feature of this part; approval [`approvals/APR-016_Alignment_Pin_Interface_Geometry.md`](approvals/APR-016_Alignment_Pin_Interface_Geometry.md) |

| 2026-08-09 | `spec/01_SEWCP-200_Cooling_Plate.md` | `a39e4b24…536b7db5` → `36e8d35b…160abdda` | ECR-D-002 disposition A — coolant channel depth 8.00 → 6.00 so the Z stack closes at `CP-D02` 20.000, with all nine derived values recomputed; approval [`approvals/APR-019_Cooling_Plate_Channel_Depth.md`](approvals/APR-019_Cooling_Plate_Channel_Depth.md) |

| 2026-08-11 | `framework/framework.manifest.json` | `8af8971b…a7e42ff7` → `920eb6ee…37814090` | **ECR-D-006 disposition A** — re-registration at the measured DC-1, and re-affirmation of the `AIEF-AMD-012` (3), `AIEF-AMD-013` (13) and `AIEF-AMD-014` (11) change sets, all twenty-seven attributed leaf by leaf against the git object `8546960` (`ae16ccac…9d8395aa`, `APR-006`'s subject). Owner-delegated engineering authority exercised by Claude — **not a human approval**; approval [`approvals/APR-033_Reregister_Framework_Manifest_ECR-D-006.md`](approvals/APR-033_Reregister_Framework_Manifest_ECR-D-006.md). **The superseded value `8af8971b…a7e42ff7` is not reproducible and no attempt is made to recover it**; it was carried in this registry from `S-2026-08-08-10` to `S-2026-08-11-06` |
| 2026-08-11 | `framework/framework.manifest.json` | `920eb6ee…37814090` → `5b78d25b…bbd6b652` | **ECR-D-014 disposition A** — `AIEF-AMD-015` §§AMD-54/AMD-55: the octets measured against `files[manifest-lock].token_cap` are the boot-read prefix, and `aggregate_digest` moves to second position. Raised at the first authorised Stage 6 build, which halted on a 6469 vs 200 breach that no conforming lock could clear. **No `token_cap` changes; MI-4 is 5904 of 6000 before and after.** Owner-delegated engineering authority exercised by Claude — **not a human approval**; approval [`approvals/APR-035_Amend_Framework_Manifest_AMD-015.md`](approvals/APR-035_Amend_Framework_Manifest_AMD-015.md). Unlike the row below, `prior_hash` here is a **measurement** and the predecessor state is a git object |
| 2026-08-11 | `framework/AIEF-AMD-015_Lock_Boot_Read_Prefix_And_Member_Order.md` | **1 added**, 30 → 31 — authorising instrument, AMD-21 criterion, **filed in the same atomic edit as the change it authorises** (LAW-01 clause 5, and the lesson of the row below) | ECR-D-014 disposition A; approval [`approvals/APR-036_Register_AIEF-AMD-015.md`](approvals/APR-036_Register_AIEF-AMD-015.md) |
| 2026-08-11 | `framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md` | **1 added**, 29 → 30 — authorising instrument, AMD-21 criterion. **Owed since `S-2026-08-08-12` and never performed**: the instrument's own § *Blast Radius* required it under `APR-015`, and neither `APR-014` nor `APR-015` was ever filed. Found by `check_v24` (*"AMD-21 criterion candidate unregistered"*) during the `S-2026-08-11-06` release audit | ECR-D-006 disposition A; approval [`approvals/APR-034_Register_AIEF-AMD-014.md`](approvals/APR-034_Register_AIEF-AMD-014.md) |

## Aggregate

**`frozen_set_hash`**, DC-2 over the 31 registered artifacts above:

```
1f32489a4ca0e4064c70679933c77ee339fdc3f68e978244b30e53278d45cc4b
```

Recomputed at `S-2026-08-17-01` over the same 31-member membership after `ECR-D-017` disposition A re-registered `framework/framework.manifest.json` at `759f774b…de74e3b` (`APR-037`; three leaves - `metadata.license` and two `authority` fields - zero removals). Prior value: `701db1fd2facde42c6e0a1a937261e4e48a4fbe587450a2ae58259b8f618aa50` - reproducible from the superseded membership, retained for audit. Dual-computed at `S-2026-08-11-06` — once by `src/aief_stage6/digests.py` and once by an
independent implementation written from the DC-2 text above, importing nothing from `src/`. The
two agree, and all **31** rows reproduce against the tree.

Prior value over the 30-member membership, replaced when `ECR-D-014` was dispositioned A under owner-delegated engineering authority (`APR-035` re-registers the manifest after the `AIEF-AMD-015` amendment; `APR-036` adds `AIEF-AMD-015` under the AMD-21 criterion, 30 → 31): `19989657464cd9dfae3668addbb7e8bec6dcd47f7cd6cfda35ea819448ddc07e` — reproducible from the superseded membership, retained for audit. Prior value over the 29-member membership, replaced when `ECR-D-006` was dispositioned A under owner-delegated engineering authority (`APR-033` re-registers the manifest at its measured digest; `APR-034` adds `AIEF-AMD-014` under the AMD-21 criterion, 29 → 30): `e558734052f3b8114a6c1db8b853cf034429414aedb9b31f7bc2f0572f592ddf` — reproducible from the superseded membership, retained for audit. **Note, and it is the point of `ECR-D-006`:** that superseded membership contains the manifest row at `8af8971b…a7e42ff7`, a digest the artifact never reproduced to. The aggregate is reproducible *from the membership*; the membership was not reproducible *from the tree*. Prior value over the same 29-member membership, replaced by the DEC-02 addendum re-issue (`APR-031`/`APR-032`): `f9e019828b97a7c96ce139448e1af356553df2da288172c4131a519dfd2e0e90` - reproducible, retained for audit. Prior value over the same 29-member membership, replaced when ECR-D-013/ECR-Q-011/ECR-Q-012 were dispositioned under the owner's delegated authority (`APR-029`/`APR-030`, `DECISIONS_S-2026-08-11-05`): `73911786c0795f20b5c5ea5b9ae4a9254d306abaccd9cc9ce54fc55a5d5bc3c2` - reproducible from the superseded membership, retained for audit. Prior value over the same 29-member membership, replaced when VER-015 F-08 was corrected under `APR-027` (the spec/06 locator torque): `55904b939054fd78c1df8716b0c50b8a2263c7360e32a8058e68cb89a476030e` - reproducible from the superseded membership, retained for audit. Prior value over the same 29-member membership, replaced when the LC-M04 specification coherence package re-registered **seven** `spec/**` artifacts under `APR-020`…`APR-026` (ECR-D-002 completion, ECR-D-003, -004, -007, -008, -009, -010, -011 and ECR-Q-009): `c56e75bc919795fb153d25c04705c9255f9ba0d41c5f59f43d76837e15ec2005` — reproducible from the superseded membership, retained for audit. Prior value, replaced when the unauthorised tap depth was struck under `APR-018`: `30be551de28bdff80daa576ca3999730c3982156976623b6809d4c0965e2ab18` — reproducible from the superseded membership, retained for audit. Prior value, replaced when `spec/01` was corrected under ECR-D-001 / `APR-017` (Option B): `94cb09e213127fbabf84b18deb2a7361b2109c5a0092d846d931ccec4bed248d` — reproducible from the superseded membership, retained for audit. Prior value over the same 29-member membership, replaced when `spec/01_SEWCP-200_Cooling_Plate.md` was re-registered under ECR-D-001 disposition A (APR-016): `339581565141702a2f5a79f531efa6c745b1af10bf2ccac4f6651af3053d30dc` — reproducible from the superseded membership, retained for audit. Prior value over the 28-member registry, replaced when AIEF-AMD-013 amended the manifest and joined the registry (APR-012, APR-013): `a743cf6fcb9a69b841deaced59cc34fd6adc0a1f31c0c84cab24ab44b80a6a53` — reproducible from the superseded membership, retained for audit. Earlier value over the 27-member registry, replaced when AIEF-AMD-012 amended the manifest and joined the registry (APR-010, APR-011): `f605e92232a8bb50ba241dc6444df5a922c68b0008ded09d2e7134d85f2bd83d` — reproducible from the superseded membership, retained for audit. Earlier value over the 26-member registry, replaced when `AIEF-AMD-011` joined the registry (APR-008, APR-009): `80cd3ebe0ce971b079fe598bac401ab959f77c7c900a54caa6e0a09963fdf2e8` — reproducible from the superseded membership, retained for audit. Earlier value over the 25-member registry, replaced when AIEF-AMD-010 amended the manifest and joined the registry (APR-006, APR-007): `4a9e88d91fea4f7b52c2371cbc5438071625b7dd0074ad389f9f9f47b128fc22` — reproducible from the superseded membership, retained for audit. Earlier value over the 24-member registry (replaced at APR-004/APR-005): `080771b0e26e365decebaa4118a27b4a46c73b7beeb3fb599009ce4ef6b6367a` — likewise reproducible and retained.

Reconstruction note (VER-005 FIND-Q5-2): each superseded membership contains the manifest row at the digest then registered — `636cf22b…14b38d3c` in the 24-member set, `9611d547…9813e557` in the 25-member set, `ae16ccac…9d8395aa` in both the 26- and 27-member sets, and `f06125d2…69707638` in the 28-member set.

Mirrored **in full, never truncated** at `STATE.md` field `frozen_set_hash`.

### Superseded value — audit record only

```
42bce7b0de019f854f99387edfc901b054b540f829bfe365e003be96892d5847
```

**SUPERSEDED and not reproducible.** Thirteen candidate constructions were tested against it and none reproduced it (ECR-Q-001 §3.1). DC-2 was defined **going forward** and makes no attempt to recover it. This value is retained for audit only and is never used as a comparison basis.

`STATE.md` previously carried the first 32 characters of this value. That truncation is corrected: DC-2 prohibits truncation, and both records now carry all 64 characters.

### Standing verification

**Four, and they compute.** Corrected `S-2026-08-10-04` on `VER-016` F-13 — this paragraph read
*"**None yet** … `V-24` … is **not implemented as software** … This registry is still verified
only by hand"*, which had been false since `V-24` was implemented.

| Check | Command | Covers |
|---|---|---|
| `V-24` | `python -m pytest tests/test_stage6_coverage_and_build.py::test_v24_live_registry` | Every registered path exists, its DC-1 matches, the DC-2 aggregate recomputes, every AMD-21 artifact is registered |
| Approval chains | `python -m aief_approval verify` | Every approval on every registered path resolves `LIVE` or `SUPERSEDED-VALID`, and the tree state is bound |
| `LC-M04-EXIT` `C5` | `python -m aief_gate` | All eleven `spec/**` rows reproduce, and every `spec/**` artifact named by an approved ECR is registered |
| Feature clearance | `python -m aief_clearance` | `spec/00` §3.2's declared map, pair by pair |

`V-24` is declared by `AIEF-AMD-008` §AMD-19, **emitted** by Compiler Stage 5 into
`core/validation/` (`S-2026-08-08-03`), and **implemented** at
`src/aief_stage6/preconditions.py::check_v24`, where it runs in the suite. ~~It currently
**fails**, on the one row `ECR-D-006` names — `framework/framework.manifest.json` — which is the
defect it exists to catch, reserved to the human owner and excluded from `LC-M04-EXIT` by name in
[`GATES.md`](GATES.md).~~ A failing check that names its offender is the working state; the
paragraph it replaced described an absent one.

**Updated `S-2026-08-11-06`.** `V-24` **passes**: 30 registered, 30 verified, aggregate
recomputes, no unregistered AMD-21 candidate. It failed for three sessions on exactly the two
things it exists to catch, and it named both of them — the drifted manifest row *and*
`AIEF-AMD-014` missing from the registry, the latter a defect **no human or agent had noticed**
and which is not in the `ECR-D-006` record as filed. The check was more truthful than every
narrative artifact that described the registry, including this one. `ECR-D-006` is dispositioned
A (`APR-033`, `APR-034`); the `GATES.md` exclusion of this path from `LC-M04-EXIT` is unchanged
and remains correct, because the path is still not under `spec/**`.

**OI-V-02** remains open for what is still true of it: `V-24` has no *campaign* infrastructure
(`CMP-BLOCK-004`/`-005`), so it runs as a test rather than as a validation campaign step.

## Authority chain

| | |
|---|---|
| LAW-01 | A frozen artifact is changed only by an approved ECR and a recorded human approval |
| LAW-10 | Approval is an artifact bound to a content hash |
| ECR-Q-001 | Disposed **A** by AIEF-AMD-008 §AMD-16 — the construction that made this aggregate computable |
| ECR-D-005 | Disposed **A** — the re-registration recorded at APR-001 |
| ECR-Q-003 | Disposed **A** by AIEF-AMD-009 §AMD-23 — Stage 1 barrier protects the Stage 1 output set |
| AIEF-AMD-008 §AMD-21 | Registry scope and registration criterion |
| AIEF-AMD-009 §AMD-24 | MI-3 namespace ruling — an earlier manifest re-registration |
| AIEF-AMD-010 §§AMD-25…AMD-34 | Stage 6 constructions (DC-4, DC-5, TF-1/TF-2) and pre-flight dispositions — the manifest change behind the latest re-registration |
| AIEF-AMD-011 §§AMD-35…AMD-38 | Software role enablement — an earlier registration; no manifest change |
| AIEF-AMD-012 §§AMD-39/AMD-40 | DC-4 coverage of enabled-role agent artifacts, disposing OI-C-06 — an earlier manifest re-registration |
| AIEF-AMD-013 §§AMD-41…AMD-48 | CMP-BLOCK-006 determination and OQ-15 reservation (AMD-41, no manifest change); V-09 measured domain and the Stage 6 build constructions OQ-B1…OQ-B5 and the three lower-order items (AMD-42…AMD-48) — the manifest change behind the latest re-registration |
| APR-001 … APR-013 | The thirteen recorded approvals behind the framework registry changes above |
| APR-016, APR-017, APR-018 | The three approvals behind the `spec/01_SEWCP-200_Cooling_Plate.md` re-registrations of 2026-08-09, under ECR-D-001 disposition A. APR-018 is terminal and the published digest is its `subject_hash`; determine liveness by recomputing it, not by reading this row |
