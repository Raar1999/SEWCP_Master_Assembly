# cad/fusion/

Local Autodesk Fusion 360 working files.

> **This directory is ignored by git.** See `.gitignore` — `*.f3d`, `*.f3z`, `*.f2d`, `*.f3b`.

---

## Why Fusion Files Are Not Tracked

Policy: **SEDEP-PMP-002 §3.1.**

> Git holds the neutral geometry record; Fusion holds the parametric one.

| Record | System of record | Rationale |
|---|---|---|
| Parametric model | **Fusion Team cloud** | Native versioning, named milestones, branching |
| Neutral geometry | **Git** (`cad/exports/step/`) | Diffable-by-hash, supplier-consumable, permanent |
| Drawings | **Git** (`drawings/`) | Released record |

Fusion binaries are large, opaque to diff, and already versioned in the cloud. Committing them produces repository bloat with no traceability benefit.

---

## Fusion Team Project Structure

The authoritative CAD hierarchy is defined in **SEDEP-PMP-002 §3**:

```
SEWCP_Master_Assembly/          [Fusion Team Project]
  00_REFERENCE/                 Frozen Base Plate, wafer, robot envelope
  01_SKELETON/                  Datum frame, Z-stack, clocking map
  02_PARTS/                     One design per part
  03_SUBASSEMBLIES/
  04_MASTER_ASSEMBLY/
  05_DRAWINGS/
  06_SIMULATION/
  07_EXPORTS/                   Mirrored to cad/exports/
```

---

## Version Correlation

Fusion version milestones are named to match git tags (`gate/G2`, `v1.0.0`) so a repository state can be tied to a CAD state.

At every gate:
1. Name the Fusion version milestone to match the git tag.
2. Export STEP to `cad/exports/step/`.
3. Commit the STEP with the tag.
