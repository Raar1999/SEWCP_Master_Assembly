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

## Registered artifacts (25)

| Path | DC-1 digest |
|---|---|
| `spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md` | `baf9ae50cd3d34a522b9998fc0f9420746ccf57c3b27f358ff0270024d9e2721` |
| `spec/01_SEWCP-200_Cooling_Plate.md` | `3ae384bd82d3d32cedf22c02c58e09fa14a363c8003d05b52ae1f78c0e6a2597` |
| `spec/02_SEWCP-300_Heater_Plate.md` | `ab36e082749fa4ea08c9f0f6a6c98cb481491cb601dc4c5cc947ba3634537608` |
| `spec/03_SEWCP-400_Chuck_Support_Ring.md` | `b00d52899f36f0bfe6a05cc209ca40876ba5fa6fac9169e5d100bc5346a62655` |
| `spec/04_SEWCP-500_Electrostatic_Chuck.md` | `4a8c39325a2edd0e03ba06b802afb5f7aaf9bb6c4552b22b3b72a67121afaca1` |
| `spec/05_SEWCP-600_Lift_Pins.md` | `39a841104a2752d9d0dd7e309e599f7735ae74cb919739e5edb3975d8470873d` |
| `spec/06_SEWCP-700_Alignment_Pins.md` | `0d2aa747fcca37574090ebff022f51924e66c7c845ecb9e2c0fea991155dcdc2` |
| `spec/07_SEWCP-800_Vacuum_Port.md` | `1b7b5914202f4ec631f5fad9daf2e41d215e5d80e07a4e289482c85d6068989f` |
| `spec/08_SEWCP-900_RF_Feedthrough_Bracket.md` | `cfe93cd6c4ef2e6b405909f252a6bd987726b65fdc4a725eb5d36ed453f166b9` |
| `spec/09_SEWCP-1000_Temperature_Sensor_Bracket.md` | `391e5e6b403e17be30028d28875a2b291a100b7a05e7038645353e78b63764dd` |
| `spec/README.md` | `95da15c691bac4ab61c3450efdc71428a5807fec1c3a32b81213f3490181370c` |
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
| `framework/SCH-framework-manifest.schema.json` | `ee3d0bdf37156541c13ece46fec9172dabd93e98f32cb88c0ae7a2adff4bb25f` |
| `framework/framework.manifest.json` | `9611d547aab51475e3b57a255af52d47972e4024c896edb5c210cf8f9813e557` |

**Not registered, by ruling.** `framework/AIEF-ARCH-001_AI_Engineering_Framework_Architecture.md` — superseded by `AIEF-FRZ-001`, authorises nothing, cited by nothing as a live authority (AMD-21, APR-003).

Per-artifact verification after this change: **25 of 25 verify.**

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

## Aggregate

**`frozen_set_hash`**, DC-2 over the 25 registered artifacts above:

```
4a9e88d91fea4f7b52c2371cbc5438071625b7dd0074ad389f9f9f47b128fc22
```

Prior value over the 24-member registry, replaced when AIEF-AMD-009 amended the manifest and joined the registry (APR-004, APR-005): `080771b0e26e365decebaa4118a27b4a46c73b7beeb3fb599009ce4ef6b6367a` — reproducible from the superseded membership, retained for audit.

Mirrored **in full, never truncated** at `STATE.md` field `frozen_set_hash`.

### Superseded value — audit record only

```
42bce7b0de019f854f99387edfc901b054b540f829bfe365e003be96892d5847
```

**SUPERSEDED and not reproducible.** Thirteen candidate constructions were tested against it and none reproduced it (ECR-Q-001 §3.1). DC-2 was defined **going forward** and makes no attempt to recover it. This value is retained for audit only and is never used as a comparison basis.

`STATE.md` previously carried the first 32 characters of this value. That truncation is corrected: DC-2 prohibits truncation, and both records now carry all 64 characters.

### Standing verification

**None yet.** Check `V-24` — *every registered path exists and its DC-1 digest matches; the DC-2 aggregate recomputes; every artifact meeting the AMD-21 criterion is registered* — is declared by `AIEF-AMD-008` §AMD-19 and **emitted** by Compiler Stage 5 into `core/validation/` (`S-2026-08-08-03`), but is **not implemented as software**: execution requires the CMP-BLOCK-004/-005 infrastructure. This registry is still verified only by hand. Recorded as **OI-V-02**.

## Authority chain

| | |
|---|---|
| LAW-01 | A frozen artifact is changed only by an approved ECR and a recorded human approval |
| LAW-10 | Approval is an artifact bound to a content hash |
| ECR-Q-001 | Disposed **A** by AIEF-AMD-008 §AMD-16 — the construction that made this aggregate computable |
| ECR-D-005 | Disposed **A** — the re-registration recorded at APR-001 |
| ECR-Q-003 | Disposed **A** by AIEF-AMD-009 §AMD-23 — Stage 1 barrier protects the Stage 1 output set |
| AIEF-AMD-008 §AMD-21 | Registry scope and registration criterion |
| AIEF-AMD-009 §AMD-24 | MI-3 namespace ruling — the manifest change behind the latest re-registration |
| APR-001 … APR-005 | The five recorded approvals behind the registry changes above |
