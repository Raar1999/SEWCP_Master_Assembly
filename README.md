# SEWCP — Semiconductor Electrostatic Wafer Chuck Platform

**Repository status:** Release 0.1 — infrastructure baseline
**Engineering baseline:** SEWCP Rev A, Volumes 00–09 — **FROZEN**
**Program:** SEDEP — Semiconductor Equipment Digital Engineering Platform

---

## What This Is

A 300 mm bipolar electrostatic chuck pedestal for RF-biased plasma process equipment: engineering specification, program plan, and the digital engineering infrastructure to execute it.

The **Base Plate (SEWCP-100) is frozen and out of scope.** Nine components are specified for implementation.

---

## Start Here

| If you want to… | Go to |
|---|---|
| Find any document | [`INDEX.md`](INDEX.md) |
| Read the engineering baseline | [`spec/README.md`](spec/README.md) |
| Understand the architecture, datums, budgets | [`spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md`](spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md) |
| See the execution plan | [`program/SEDEP-PMP-001_Program_Management_Plan.md`](program/SEDEP-PMP-001_Program_Management_Plan.md) |
| See repository / tooling conventions | [`program/SEDEP-PMP-002_Digital_Engineering_Infrastructure.md`](program/SEDEP-PMP-002_Digital_Engineering_Infrastructure.md) |
| See how documents depend on each other | [`traceability/DOCUMENT_DEPENDENCY_MAP.md`](traceability/DOCUMENT_DEPENDENCY_MAP.md) |
| Check release status | [`releases/README.md`](releases/README.md) |
| Contribute | [`CONTRIBUTING.md`](CONTRIBUTING.md) |

---

## Directory Layout

| Path | Contents | Change Control |
|---|---|---|
| `spec/` | Engineering specification, Volumes 00–09 | **FROZEN** — specification revision only |
| `program/` | Program management and infrastructure plans | PR |
| `implementation/` | Per-component implementation packages (9 components) | PR |
| `cad/` | Neutral geometry exports, Fusion working files, archive | PR |
| `params/` | Parameter master — single source of truth for dimensions | PR + Design Authority |
| `src/sedep/` | Python digital engineering platform | PR + CI |
| `tests/` | Test suite | PR + CI |
| `analysis/` | Engineering analysis reports | PR |
| `drawings/` | Drawing set | PR + independent check |
| `traceability/` | Document and requirement traceability | Generated |
| `notebook/` | Engineering notebook — append-only | Append only |
| `manufacturing/` | RFQ packages, inspection plans | PR |
| `dashboard/` | Generated program dashboard | Generated |
| `releases/` | Release manifests and readiness reports | Tag-gated |
| `portfolio/` | Communication assets | PR |

---

## Repository Policy

Binding, in force now:

- **No AI attribution** in any commit, file, or document.
- **No `Co-authored-by`** trailers.
- **Git author information is never modified.**
- `spec/` is frozen; defects are raised as ECR, never edited in place.
- No engineering decision is made in a commit.

Full text: [`CONTRIBUTING.md`](CONTRIBUTING.md) §1.

---

## Known Open Items

| ID | Item | Blocks |
|---|---|---|
| C-4 | `LICENSE` is an unresolved placeholder | **Public release** |
| C-5 | CI workflows not populated | Automated verification |
| ECR-D-001…004 | Four defects in the frozen baseline, recorded during Cooling Plate CAD preparation | CAD modelling of SEWCP-200 |

`ECR-D-001…004` are **pre-existing engineering findings**, not infrastructure defects. They are recorded in `implementation/01_SEWCP-200_Cooling_Plate/SEWCP-200_CAD_Implementation_Package.md` §12 and do not affect Release 0.1.
