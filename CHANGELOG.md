# Changelog

All notable changes to this repository are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows the release tag scheme in `releases/TAGS.md`.

---

## [0.11.0] — 2026-08-17 — Public release: CAD and software complete

> **Three independent cold-context QA rounds ran against this release.** Two returned
> `NOT CLEARED` and each found a real defect in a repair that looked complete; the third
> declared the `ECR-D-014` enforcement condition fully discharged after fifteen source
> mutations, and refused closure on record accuracy alone. Every finding is recorded, and the
> corrections below are the result. `ECR-D-014` is left **open** because LAW-05 bars a session
> from certifying its own repair — three times running.

### Corrected after the second and third rounds
- The `ECR-D-014` ruling was enforced **only on the preview path**; a canonical build could
  have emitted a 249-token prefix against a cap of 200. `run()` now re-derives the measurement
  from the octets it emitted and halts on disagreement. **Fifteen mutations die.**
- `TCR-002` has **eight** findings, three BLOCKING — not six and two. `F-7` repaired, `F-6`
  and `F-8` carried.
- `ECR-D-015`'s byte-identity claim was false of the final state and its byte total was
  derived from the source rather than measured. Corrected at the ECR **and** at
  `cad/DELIVERABLES.md`, which had kept publishing the withdrawn claim.
- `README.md` claimed a reproducibility never tested from outside: a clone failed 35 tests.
  Now **821 passed, 52 skipped, 0 failed**, measured from a clone of the published repository.
- `LICENSE` §2's *"nothing in the set is copyleft"* was wrong — `certifi` is MPL-2.0. The
  conclusion survives on the correct ground: nothing is vendored, modified or redistributed.
- `STATE_REGISTER.md` recited three values that its own session's close moved, three sessions
  running. **Cured procedurally**: the recitals are removed and
  `tests/test_state_register_currency.py` fails if any governed value it states goes stale.
- **`OI-C-10` arrived.** Raising one more open item took the bounded index to 602 tokens
  against its 600 cap and halted `V-09`. The identifier was withdrawn and the finding folded,
  recorded at both rows as forced by the budget rather than by the merits. **No session-level
  action remains**; the next distinct finding cannot be folded.

**The repository becomes public.** Every CAD-verifiable property is verified and reproducible
from a clean clone; **nothing physical has been built or measured**, and one defect is open
against the design itself. Session `S-2026-08-17-01`; decisions at
`.ai/project/decisions/DECISIONS_S-2026-08-17-01.md`.

### Added
- **`LICENSE`, resolved — `MIT AND CC-BY-4.0`, boundary by path** (closes **`C-4`**, DEC-11).
  Code MIT; documents, engineering artifacts and generated design data CC-BY-4.0. Full MIT text
  and the full CC BY 4.0 legal code embedded verbatim so the licence survives without a network.
  §3 states expressly that **no patent and no trademark licence is granted**, and that the
  design is not qualified hardware. Third-party licences were read from each installed
  distribution's own metadata, never assumed; nothing in the set is copyleft. No per-file
  header is used or permitted — one would move a registered DC-1 digest and halt boot step B2a.
- **The CAD deliverables are in the repository** (**`ECR-D-015`**, DEC-12): 61 files mirrored in
  byte-identically to `cad/exports/`, `cad/bom/` and `drawings/`. Previously a clone contained a
  register of 62 digests naming files on one machine. Byte identity proven by SHA-256 before and
  after and again through a clean `git checkout-index`.
- `python -m aief_deliverables` — bi-directional standing check binding the register to the
  tree, with 12 adversarial tests.
- `python -m aief_analysis` — the two `OI-C-15` desk analyses, computed and tested (16 tests).
- `.ai/project/STATE_REGISTER.md` — declared in the frozen manifest since 2026-08-08 and never
  written (`OI-V-13` FIND-3; `TCR-002` F-2, filed BLOCKING eight days earlier and unactioned).
- `requirements.txt`, with each dependency's licence recorded beside it.
- `tests/test_stage6_prefix_enforcement.py` — pins the `ECR-D-014` ruling **at the pipeline**,
  not at the function. 47 tests added overall; suite 799 → 873.

### Fixed
- **`V-03` enforced half its declared domain and reported green.** The state register pair was
  skipped by a branch that sat *before* the existence test, so a declared register could be
  absent while `V-03` passed. Both pairs are now checked; `register_pairs` 1 → 2.
- **The `ECR-D-014` ruling was enforced by nothing.** Three call-site mutations — measuring the
  whole document instead of the boot-read prefix, substituting the cap, skipping the check and
  fabricating `PASS` — each survived all 799 tests. Each was applied for real and confirmed
  caught. (`OI-V-13` FIND-1, BLOCKING.)
- **`ECR-D-014` §4 stated as fact something the repository contradicts.** The defect was
  measured and escalated BLOCKING two days earlier by an independent cold session (`TCR-002`
  F-3) that this record cited nowhere. Corrected in place, priority claim withdrawn, and
  `TCR-002`'s **eight** findings — three of them BLOCKING — now carried at `OI-V-14`. (FIND-2;
  the count itself corrected from six after round 3 found this line uncorrected.)
- Two silent swallows in the approval-chain parser: a repeated `subject_path` let a good binding
  mask a fabricated one, and a block-sequence `prior_hash` was read as null and silently rooted
  the chain. (FIND-8.)
- `boot_read_prefix` matched a substring where the ruling specifies a member line. (FIND-7.)
- Drawing PDFs are now **byte-deterministic**: matplotlib's wall-clock stamp made every PDF
  differ on every render. Proven over two consecutive renders, 39/39 stable.
- `ENGINEERING.md` §8 told readers to expect two failures a repaired repository does not produce
  (FIND-9); `GATES.md` recited an index section two of its four ids had left (FIND-10,
  `ECR-Q-015`, re-bound by `APR-038` after the edit correctly voided `APR-028`).
- `cad/DELIVERABLES.md`, the BOM builder and `final_system_verification.py` all pointed at an
  external output root; all now read the repository.
- `SEWCP-401` material was specified two ways — `spec/03` §5.2 governs, 316L (**`ECR-Q-014`**).

### Changed
- `framework.manifest.json`: `metadata.license` resolved and two `authority` fields amended by
  `AIEF-AMD-015` now cite it (**`ECR-D-017`**, `APR-037`). Three leaves, zero removals, proven
  by structural diff. Registry re-registered; DC-2 → `1f32489a…8d45cc4b`; Stage 6 re-emitted so
  the lock's `source_manifest_dc1` names the artifact that exists. **DC-4 and
  `BINDING.core_digest_pin` did not move**; B2a re-verified independently at 75/75.
- `.gitattributes`: the four deliverable subtrees are `-text`. The blanket `* text eol=lf` would
  have corrupted 24 binary deliverables and moved every recorded digest — the check that file's
  own comment demanded before adding binary content.

### Engineering findings
- **`ECR-D-016` — the Support Ring isolation joint does not close.** `SR-02` (353.9 Ω vs 400),
  `SR-03` (14.00 mm vs 20) and `SR-04` (≤ 8.50 mm vs 12) all fail on frozen dimensions, for one
  reason: `spec/03` §2.1 and §3.1 compute the flange gap as empty while §5.2 puts a 6.00 mm
  grounded ring inside it. Proven against the specification's own published answer. Ruled
  **disposition A — Rev B baseline revision**, with a feasible Rev B computed and published;
  **implemented at Rev B, not here.** **Blocks hardware build. Blocks no gate and no release.**
- `OI-CAD-04` — four dimensioned `SEWCP-400` features, three marked *Critical*, are absent from
  the verified model. Not a modelling slip: they have no radial room to exist in, which is
  `ECR-D-016` §2.3.
- `SR-07`/`AP-08` re-run at the as-modelled 7.69973 kg (+2.66 %): **both discharge**, and the
  governing case does not reach SF = 3 until 84.4 kg, so no unmodelled BOM line can disturb it.

### Verification
- **Independent cold-context QA (`OI-V-13`) returned `NOT CLEARED`**, with 17 findings. It
  **cleared `ECR-D-006`** — every element reproduced, and it confirmed the recorded residual more
  strongly than the record had — and **refused `ECR-D-014`**. Both grounds are now repaired, and
  **this session may not certify its own repair**: LAW-05 bars it and no delegation of owner
  authority reaches a constitutional separation. `ECR-D-014` stays open awaiting one fresh round.

### Known limitations
- **0 of 91 hardware-verifiable requirements are verified. No article exists.**
- `ECR-D-016` blocks hardware build pending a Rev B baseline revision.
- `CMP-BLOCK-004`/`-005` remain open; they gate **AIEF framework Release 1.0.0**, not this
  repository's release (DEC-18).

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
