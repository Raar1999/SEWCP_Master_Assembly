# Changelog

All notable changes to this repository are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows the release tag scheme in `releases/TAGS.md`.

---

## [Unreleased]

### Fixed
- `releases/TAGS.md` §5 now reproduces the applied tag annotations **verbatim**. The v0.1.0 release commit carried paraphrased text that omitted the `baseline/spec-revA` protection statement and the `v0.1.0` C-4 distribution restriction. Raised as a MINOR finding by independent audit re-verification. Tags were **not** moved — `v0.1.0` remains at `88ec4cb` per `releases/TAGS.md` §4 rule 2.

---

## [0.1.0] — 2026-08-07 — Infrastructure Baseline

Repository infrastructure only. **No engineering content was created, modified, reviewed, or decided in this release.**

### Added
- Git repository initialised on branch `main`.
- `.gitignore` covering Autodesk Fusion 360, Python, VS Code, OS artefacts and CAE scratch.
- `LICENSE` placeholder — **unresolved, blocks public release**.
- `CONTRIBUTING.md` placeholder carrying the binding repository policy (P-1 … P-5).
- `CHANGELOG.md` (this file).
- `INDEX.md` — master document index.
- Root `README.md` — repository landing page.
- `implementation/` with nine component folders, each containing `cad/`, `params/`, `drawings/`, `verification/` and a placeholder README.
- `releases/` with `TAGS.md` tag scheme and the `v0.1/` manifest.
- `cad/fusion/` and `cad/archive/`.
- `traceability/DOCUMENT_DEPENDENCY_MAP.md`.
- `traceability/DOCUMENT_TRACEABILITY_MATRIX.md`.
- `releases/v0.1/RELEASE_0.1_READINESS_REPORT.md`.
- `.gitkeep` markers in otherwise-empty tracked directories.

### Moved
- `docs/` → `spec/` (11 files). **Content unchanged, byte-for-byte.** Aligns the repository with the structure ratified in SEDEP-PMP-002 §1 and closes the open item raised at program plan issue.
- `cad/SEWCP-200_CAD_Implementation_Package.md` → `implementation/01_SEWCP-200_Cooling_Plate/`. **Content unchanged.**

### Removed
- Empty `docs/` directory after migration.

### Notes
- The engineering baseline `spec/` (SEWCP Rev A, Volumes 00–09) is **FROZEN** and was not altered.
- Four open **ECR-D** defects recorded against the frozen baseline in `implementation/01_SEWCP-200_Cooling_Plate/SEWCP-200_CAD_Implementation_Package.md` §12. These block engineering release, **not** this infrastructure release. See `releases/v0.1/RELEASE_0.1_READINESS_REPORT.md`.

### Unresolved at Release 0.1
| ID | Item | Blocks |
|---|---|---|
| C-4 | `LICENSE` placeholder not resolved | Public / external release |
| C-5 | CI workflows not populated | Automated verification |
| ECR-D-001…004 | Baseline defects (engineering, pre-existing) | CAD modelling of SEWCP-200 |

---

[Unreleased]: ./
[0.1.0]: ./releases/v0.1/
