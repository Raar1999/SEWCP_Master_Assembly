# Freeze Registry

> **Instance artifact.** Emitted by aief-compile Stage 3 from `framework.manifest.json` and live repository state.
> Partition `project` — never touched by framework upgrade. Owner `chief-systems-engineer`. Mutability mutable.

---

Governed by `core/laws/LAW-01_architecture_freeze.md`. Hash: **SHA-256 over normalised content** (UTF-8, LF line endings, trailing whitespace stripped, terminal newline enforced).

A change to any registered artifact without an approved ECR and a human approval artifact is a **freeze violation**.

## Registered artifacts (16)

| Path | Normalised SHA-256 |
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
| `framework/AIEF-AMD-001_Architecture_Amendments_1.0.0.md` | `1d3c42d48f366a1be02c6fe3bd9281c356fd1063ec3c4c4b179efc9fb8744329` |
| `framework/AIEF-AMD-002_Architecture_Amendments_CMP-BLOCK-014.md` | `83a69de9e6b9e0a6d2dc5f46614bcd0a8170882c4d0d900a9872442d9b382591` |
| `framework/AIEF-FRZ-001_Framework_Architecture_Freeze_1.0.0.md` | `a1b0a51c58138156a18598c2cb9bcb3a6066b0fcd35ea10203d5d17c450023f4` |
| `framework/framework.manifest.json` | `c33e574a3bc16eec79bcd078d7e04402709d274ba3421cd428f94691fed01799` |
| `framework/SCH-framework-manifest.schema.json` | `ee3d0bdf37156541c13ece46fec9172dabd93e98f32cb88c0ae7a2adff4bb25f` |

## Aggregate

`42bce7b0de019f854f99387edfc901b054b540f829bfe365e003be96892d5847`

Recorded in `STATE.md` as `frozen_set_hash` (first 32 chars).
