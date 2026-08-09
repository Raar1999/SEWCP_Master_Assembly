# VER-005 — Independent QA Audit of `S-2026-08-08-05` (AIEF-AMD-011 / OQ-13 enactment)

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-verification-report`.
>
> **Filing note.** Produced by a cold-context `qa-engineer` subagent (`qa-engineer · S-2026-08-08-05b`), dispatched at live human-owner direction (rank 1) as the mitigating control for the separation-of-duties departure recorded in `AIEF-AMD-011` § *Separation of Duties*. Filed **verbatim** by the coordinating session `S-2026-08-08-03` (which produced neither the audited artifacts — author `chief-systems-engineer · S-2026-08-08-05`, a distinct cold agent — nor the audit); the qa-engineer neither filed nor attested to the filing (VER-001 precedent). This filing discharges the audit's own item (b)(6).

---

## 1 · Independence declaration

I am `qa-engineer · S-2026-08-08-05b`, a cold session holding no state from any prior session. I authored none of the audited work. Under AMD-20 (identity = role × session) I differ from the enacting session (`chief-systems-engineer · S-2026-08-08-05`) in both role and session. I ran READ-ONLY: no repository file was created, modified, or deleted; no mutating git command was executed. All hash tooling is my own fresh implementation, written in the session scratchpad from the normative DC-1/DC-2 texts in `framework/framework.manifest.json` / AMD-008 / `FROZEN.md`, and self-validated before use:

- DC-2 two-record worked example → `8de12581a7d3aef29454fcdfd696a71e4d5c1a0352f69c7a6b03b167d0f5f1b3` — exact match
- Empty registry → `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` — exact match

## 2 · Method

Booted from `ENGINEERING.md` and the project artifacts (repository as sole source). Parsed `framework/framework.manifest.json` myself (agents, profiles, files[], schemas, digest_constructions). Recomputed all 27 FROZEN rows, the DC-2 aggregate, and all three lineage aggregates from their superseded memberships. Diffed every touched file against HEAD `8546960` (`git show`/`git diff`), enumerated the full working-tree change set with `-uall`, quote-compared the three emitted role files against the manifest contracts and against the mechanical sibling (`AGT-cad-engineer.md`) and `TPL-agent-specification.md`, inspected `git show 7c530f4 --stat` for the AMD-006 precedent, and ran my own V-25 (encoding/BOM/LF/mojibake) and AMD-20 attribution scans over all twelve touched artifacts.

## 3 · Criteria

| # | Criterion | Verdict | Evidence (one line) |
|---|---|---|---|
| C1 | OQ-13 authorization chain | **PASS** | APR-008 records the decision verbatim as rank-1 basis, `approver: human-owner`; AMD-010 §AMD-34 verifiably reserved the choice ("the CHOICE among (a),(b),(c) is the human owner's"); OPEN_ITEMS Closed row and STATE.next_action carry the decision text; `7c530f4` confirms the AMD-006 mechanism (instrument + approval + agent file + BINDING + ROSTER) is faithfully followed, with the manifest divergence correctly ruled in AMD-37 and the INDEX.md divergence disclosed (see FIND-Q5-1) |
| C2 | Software-role definitions | **PASS** | All three files exist at claimed paths; field-by-field identical to the manifest's twelve-field contracts (all forbidden actions verbatim; `software.test-engineer` carries "May not test code it authored" under Separation of duties, exactly as `duty_conflicts` declares); authority A1/A1/A1 matches; format identical to mechanical siblings incl. all `tpl-agent-specification` required sections (Authority level + Capability tags in header, the sibling convention); only additions are the honest provenance header ("Rendered from … under AIEF-AMD-011 (approval APR-008); not a Stage 1 emission") and the sibling-standard footer |
| C3 | BINDING consistency | **PASS** | `git diff 8546960` shows exactly three added `enabled_agents` lines, each `# A1 - AIEF-AMD-011`; `active_profile: mechanical` and `core_digest_pin: PENDING-STAGE-6` unchanged; all nine `sch-binding` required fields present; the three ids exactly equal the manifest's `software.*` agent ids |
| C4 | Roster consistency | **PASS** | Diff shows exactly one new section with three UNASSIGNED rows in the file's existing table format; no identities invented; standing rule ("A role marked UNASSIGNED cannot be dispatched. Assignment is a `project-manager` action.") restated not weakened; OI-P-02 referenced as the covering item |
| C5 | Manifest integrity | **PASS** | Working-tree manifest byte-identical to `git show 8546960:…`; my DC-1 = `ae16ccaca5746b81a2a992841fc1d239fd1c8b0c34657c05611e025a9d8395aa` (exact); schema byte-identical to HEAD; I independently found all three twelve-field `agents.profile` contracts, `profiles[software]` complete (3 agents, 6 lifecycle stages — MI-9 claim TRUE), and three `files[]` entries (`soft-agt-software/-test/-platform`, generator 1, `profile_scope: ["software"]`, `integrity: hashed`) whose declared paths `core/profiles/software/agents/AGT-*.md` match the emitted `.ai/core/profiles/software/agents/AGT-*.md` exactly (files[] paths are `.ai/`-relative, per DC-4's record definition and every sibling) — no mismatch |
| C6 | Freeze registry / hashes | **PASS** | 27/27 rows recompute exactly; aggregate recomputes to `f605e92232a8bb50ba241dc6444df5a922c68b0008ded09d2e7134d85f2bd83d` == `STATE.frozen_set_hash` in full; APR-009 subject == my AMD-011 DC-1 `59ecb5eb922f44a55cc42e51663dae9ee251269790958ee27ad93c1ba2ebaa53`; APR-008's three bound agent digests all recompute exactly; lineage independently reproduced — 26-member `80cd3ebe0ce971b079fe598bac401ab959f77c7c900a54caa6e0a09963fdf2e8`, 25-member `4a9e88d91fea4f7b52c2371cbc5438071625b7dd0074ad389f9f9f47b128fc22`, 24-member `080771b0e26e365decebaa4118a27b4a46c73b7beeb3fb599009ce4ef6b6367a` |
| C7 | Ownership / no profile leakage | **PASS** | All three new files live under `.ai/core/profiles/software/agents/`; `git diff --stat 8546960` shows zero changes under `.ai/core/**` (incl. `agents/INDEX.md`, mechanical profile, laws, workflows, templates) and `framework/` except the new AMD-011; software roles referenced as enabled only in BINDING/ROSTER/STATE/OPEN_ITEMS/ENGINEERING; emitted headers' `Owner: chief-systems-engineer` == `files[].owner_role` |
| C8 | Git / attribution policy | **PASS** | HEAD `8546960ea4e0c433e992aeb5b6c934c92b4ed877` == `origin/main`; no tag on HEAD, tag list unchanged (…v0.10.0); working-tree change set is exactly the enumerated blast radius — 6 modified + 6 created files, nothing else (`git status --porcelain -uall`); attribution scan across all twelve touched artifacts finds no AI/model/vendor/product name in any actor field and no trailer forms; my V-25 implementation passes all twelve (UTF-8, no BOM, LF-only, single terminal LF, no mojibake) |
| C9 | Honest residuals | **PASS** | OI-C-06 TRUE: manifest DC-4 `covers` reads `core/profiles/<selected>/**` and selected = mechanical, so the three files sit outside declared coverage; OI-C-07 TRUE: `.ai/core/agents/INDEX.md` has no software rows in its role tables (only the SoD line 56, pre-existing) and was not edited (empty diff vs HEAD); SoD departure recorded in AMD-011 § Separation of Duties and appended to SOD-1; every reference to this audit says "dispatched … open until filed" — no verdict pre-recorded anywhere |

## 4 · Findings

| ID | Severity | Finding | Disposition needed |
|---|---|---|---|
| FIND-Q5-1 | INFO | The AMD-006 release (`7c530f4`) additionally updated `.ai/core/agents/INDEX.md` (+3), `PROFILE.md`, and the manifest. AMD-011 diverges on all three — each divergence is *ruled and disclosed* (AMD-37: contracts pre-exist in the manifest, correct; OI-C-07: INDEX.md deliberately not hand-edited; AMD-36 ¶4: software PROFILE.md deliberately not emitted, zero-dead-file). "Following the AMD-006 pattern" is accurate for the enablement mechanism; it is not byte-level pattern identity. | None — already carried as OI-C-06/OI-C-07 |
| FIND-Q5-2 | INFO | The 24-member lineage aggregate `080771b0…` reproduces only with the manifest membership at its pre-APR-004 digest `636cf22b9080b5d5178542fc42b618fc75033129a5932167d3b12e3214b38d3c`; FROZEN.md's lineage prose does not state which manifest digest each superseded membership contains. I reproduced all three from the registration history; a future auditor must do the same reconstruction. | None required; optional clarity edit at next FROZEN touch |
| FIND-Q5-3 | INFO | My dispatch briefing said the change set is "EXACTLY the 10 claimed paths"; the enumerated blast radius is 12 paths (6 created + 6 modified) and the repository matches the enumerated 12 exactly. Briefing arithmetic slip, not a repository discrepancy. | None |

No MAJOR or MINOR findings. No criterion failed.

## 5 · Overall verdict

**VERIFIED** — 9 criteria, 9 PASS; three informational findings, none requiring disposition. All digests claimed by `S-2026-08-08-05` reproduce exactly under independently written, worked-example-validated tooling. The session did exactly what it claimed, nothing more, and its residuals are honestly recorded.

**(a) Are the three software roles lawfully enabled and defined such that implementation work can be assigned?** Yes. The authorization chain is complete and rank-correct (human-owner decision → AMD-011 instrument → APR-008/APR-009 approvals → BINDING/ROSTER edits), and the three contracts are persisted, manifest-conformant, and integrity-bound by DC-1 in APR-008. **The single remaining block on assignment is roster state, not lawfulness:** all three rows are UNASSIGNED, and the standing rule bars dispatch until either the `project-manager` records an assignment or a rank-1 live human instruction directs a dispatch (OI-P-02 pattern). One structural constraint on allocation: `software.test-engineer` may not test code it authored, so compiler implementation and its test certification must land on different identities/sessions.

**(b) Exact prerequisites remaining before Stage 6 authorization/execution:**
1. **OQ-14** — explicit human-owner authorization of Stage 6 (reserved; independent of all specification rulings).
2. **CMP-BLOCK-004** — a deterministic Stage 6 implementation must exist (and **CMP-BLOCK-005** for the V-09/V-12/V-15/V-18 infrastructure) — this is the work the enabled roles will perform, preceded by the assignment/dispatch in (a).
3. **OI-C-06** — before Stage 6 *executes*: an A4 ruling extending DC-4 coverage to enabled-role artifacts, or folding the enablement into the build's emitted set (otherwise `MANIFEST.lock`/B2a will not bind the three software files).
4. **OI-V-06** — V-14 trial count must be declared with the validation-campaign design before any V-14 implementation.
5. **VER-004 residuals** — FIND-Q4-1 (tokenizer trust-on-first-use comparison at the first authoritative build) and FIND-Q4-2 (ustar long-path verification) before the first release build.
6. **SOD-1 mitigating control for `-05`** — this audit; discharged in substance by this report, but its filing as a repository verification record (VER-005 analog) is a write the directing authority must arrange — I am read-only.

**(c) Is the next step compiler implementation?** In substance yes, with one administrative step first: per `STATE.next_action`, the immediate next action is **allocation** — project-manager assignment of the UNASSIGNED software roster rows (or rank-1 dispatch) — then **compiler implementation** (CMP-BLOCK-004/-005) by the enabled `software.*` roles. Stage 6 *execution* itself remains NOT authorized (OQ-14) and remains held by CMP-BLOCK-004 regardless.

**Computed digests (full):**
- Manifest DC-1: `ae16ccaca5746b81a2a992841fc1d239fd1c8b0c34657c05611e025a9d8395aa`
- AMD-011 DC-1: `59ecb5eb922f44a55cc42e51663dae9ee251269790958ee27ad93c1ba2ebaa53`
- AGT-software-engineer: `6bc734d47ceacbc8f9e2a5c31b41fac31083dc0f6dcaee47191053aaf19ce717` · AGT-test-engineer: `bb8cebd57b65091774182ecef56991ffb50564bbefa6dda47b3ccc63227127d8` · AGT-platform-engineer: `96e5680c1edb51b960afe410b3482e1c331e9a818764e7b8ff00548560c3e4fd`
- BINDING fingerprint: `64a9ca216606e502ca186985dc4ef22d5f7fd0504ed281b392c84910ac81a15f` · ROSTER fingerprint: `2443cf4928fc659437c6d64d195e97d092b670e29ea971d5c385161576ba2947`
- Aggregate (27): `f605e92232a8bb50ba241dc6444df5a922c68b0008ded09d2e7134d85f2bd83d` · lineage (26/25/24): `80cd3ebe0ce971b079fe598bac401ab959f77c7c900a54caa6e0a09963fdf2e8` / `4a9e88d91fea4f7b52c2371cbc5438071625b7dd0074ad389f9f9f47b128fc22` / `080771b0e26e365decebaa4118a27b4a46c73b7beeb3fb599009ce4ef6b6367a`
- Tooling self-validation: `8de12581a7d3aef29454fcdfd696a71e4d5c1a0352f69c7a6b03b167d0f5f1b3` (worked example) · `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty registry)

*(Transcription note, preserved from the auditor's transmission: two digest lines in the original terminal transmission carried presentation-level transcription slips which the auditor itself corrected inline against tool output; the values above are the corrected, computed values, which match the repository's claims exactly.)*
