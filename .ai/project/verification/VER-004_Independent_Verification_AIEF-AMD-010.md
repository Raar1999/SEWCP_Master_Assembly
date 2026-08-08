# VER-004 — Independent Verification of the AIEF-AMD-010 Session Work

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-verification-report`.
>
> **Filing note.** The report below was produced by a cold-context `qa-engineer` subagent (`qa-engineer · S-2026-08-08-04b`), dispatched at live human-owner direction (rank 1) as the mitigating control for the separation-of-duties departure recorded in `AIEF-AMD-010` § *Separation of Duties*. The body is filed **verbatim** by the coordinating session `S-2026-08-08-03`, which neither produced the audited artifacts (author: `chief-systems-engineer · S-2026-08-08-04`, a distinct cold agent) nor the audit; the qa-engineer neither filed nor attested to the filing (VER-001 precedent). FIND-Q4-3's disposition — the one-line `STATE.md` `open_non_blocking` sync — was applied by the filer at this filing, in-role as `repository-engineer`, as the finding itself directs.

---

# QA Audit Report — `qa-engineer · S-2026-08-08-04b` (cold, serial adoption)

## 1. Independence declaration

I am a cold-context QA session holding no state from any prior session. I derived every conclusion below from repository artifacts at `D:\Fusion Projects\SEWCP_Master_Assembly` (HEAD `dc811a61c20728e58976a45a10ef4e7ebaa16bcc` == `origin/main`) and from tooling I wrote fresh this session in my scratchpad (`qa_audit.py`) from the normative DC definitions in `framework/framework.manifest.json`. No pre-existing helper script was reused. I created, modified, and deleted nothing in the repository; all git use was read-only (`status`, `rev-parse`, `show`, `diff`, `tag`, `log`). I differ from the audited party (`chief-systems-engineer · S-2026-08-08-04`) in both role and session — the AMD-20 identity pair — satisfying LAW-05 independence. Nothing in my dispatch briefing was trusted unverified; every claimed digest was recomputed.

## 2. Method

(1) Live `git status --porcelain -uall`, HEAD/origin/tag survey. (2) Full read of AMD-010, APR-006, APR-007, the pre-flight report, and the working-tree diffs of all five modified files. (3) Fresh Python implementations of DC-1 (normalise: strip BOM, CRLF/CR→LF, strip trailing whitespace per line, drop trailing blank lines, one terminal LF, UTF-8, SHA-256) and the DC-2/DC-4 shared record grammar (`<path>` `<SP>` `<digest>` `<LF>`, ascending UTF-8-octet path order), self-validated against all published worked examples before use. (4) Recomputation of all 26 registry rows, the aggregate and its full lineage, and both APR subjects. (5) JSON Schema 2020-12 validation (jsonschema 4.26.0) of the amended manifest against the byte-unchanged frozen schema; MI-1/MI-3-strict/V-23 checks over all 106 `files[]` entries. (6) Structural diff of the manifest JSON (flattened path comparison HEAD vs working tree) mapped against APR-006's enumeration. (7) Line-exact quote checks in AIEF-FRZ-001, AMD-008, AMD-009, `SCH-core-manifest.schema.json`, `BOOT.md`, `CHECKS.md`. (8) Encoding (V-25), attribution, ledger, and prohibited-artifact checks.

## 3. Criteria table

| # | Criterion | Verdict | Evidence (one line) |
|---|---|---|---|
| C1 | Ruling completeness, non-assumption | **PASS** | OQ-1→AMD-25, OQ-2→26, OQ-3→28, OQ-4/5→27, OQ-6→29, OQ-7→30, OQ-8→31, OQ-9→32, OQ-10/12→33, OQ-13→34 (analysis only); OQ-11 explicitly not-ruled with reason → OI-V-06; every contested ruling carries rationale + rejected-alternatives table; spot-checked citations all exact: FRZ-001:142 ("two tokenizer families; the maximum governs", in §1.8 as the manifest cites), :538 ("execute V-01…V-21"), :487 ("21 blocking validations"), :105 (F-06 pin = "the expected aggregate digest"), :205 (B2a "core/ aggregate digest"), :383, :443, :449, :80; `SCH-core-manifest` truly declares `additionalProperties: true` with the six required fields |
| C2 | Digest verification | **PASS** | Fresh DC-2 reproduces the AMD-008 example `8de12581…`; all 26 FROZEN rows recompute 26/26; aggregate recomputes to `80cd3ebe0ce971b079fe598bac401ab959f77c7c900a54caa6e0a09963fdf2e8` == STATE.frozen_set_hash at full 64; APR-006 subject `ae16ccac…` and prior `9611d547…` both recompute; APR-007 subject `486be10e…` recomputes; retained lineage independently reproduced — 25-member `4a9e88d9…` and 24-member `080771b0…` both recompute exactly from superseded memberships |
| C3 | Worked examples | **PASS** | My independent DC-4 implementation yields `eb6e969b9f1d31a367ccf83315c1a40f8df0bb1c7dec41566a637ac3740325b1` and DC-5("abc") yields `ba7816bf…f20015ad` (FIPS 180 vector); both constructions state record grammar, order, encoding, and self-exclusion explicitly; DC-1/DC-2/DC-3 manifest sections structurally identical to `git show dc811a6:` (only the shared `note` changed, declared as APR-006 change 1) |
| C4 | Manifest/schema integrity | **PASS** | JSON parses; valid against unmodified 2020-12 schema (0 errors, real validator); schema file byte-identical to HEAD; MI-1 106 unique ids; MI-3 strict 0 dangling; V-23 0 backward edges; flattened diff shows only additions under the 6 new `metadata.reproducible` objects + `note` + `validation[V-09/V-10].verifies` + `generation_order[6].outputs/.barrier` — every changed path maps to APR-006's 11 enumerated changes, zero undeclared changes, zero removals |
| C5 | Tokenizer spec (OQ-2) | **PASS** | TF-1/TF-2 are concrete, deterministic, publicly specified, distinct algorithm families; the only 64-hex values in all new manifest sections are the two worked examples and the synthetic all-0/all-1 inputs — **no fabricated pin value anywhere**; the pending-pin mechanism is explicit ("recorded at the first authoritative Stage 6 measurement, verified before every subsequent measurement") with a LAW-12 justification; V-09's extension cites, not restates, "the maximum governs" (see FIND-Q4-1) |
| C6 | Budget record + distributable (OQ-6/OQ-7) | **PASS** | `budget_measurement` content list is implementable (per-file counts per family, totals, governing maxima, verdicts, artifact pins, timestamp, build id) and admitted by `additionalProperties: true`; tar spec declares entry ordering, mtime/uid/gid/uname/gname/mode zeroing, and naming; contents = DC-4 set + lock only (zero-dead-file); no frozen text contradicted (see FIND-Q4-2 on the pax edge) |
| C7 | Sequencing (OQ-8/9/1) | **PASS** | V-10 exclusion justified (a check on the build cannot precede the build); AMD-32 uses the AMD-009 §AMD-23 supersession-in-reading mechanism with FRZ-001 and AMD-001…009 all hashing to their registered values (in the 26/26); AMD-25 quotes FRZ-001:383 verbatim and retains the full-pipeline requirement for Release 1.0.0; `.ai/core/validation/CHECKS.md` + `MANIFEST` byte-identical to HEAD (no diff) while the manifest V-09/V-10 texts did change — OI-V-07's staleness claim is true; OI-C-02 consequence-recording present in OPEN_ITEMS diff |
| C8 | Allocation (OQ-13) | **PASS** | `BINDING.md` byte-identical to HEAD (`core_digest_pin: PENDING-STAGE-6`, `enabled_agents` untouched); no software agent file exists in the change set; AMD-34 header states "No manifest change. No BINDING change… choice is reserved to the human owner"; the option-(a) preference is expressly labeled "recommendation, not decision" |
| C9 | No unauthorized modification | **PASS** | Live change set is exactly the 8 claimed paths (5 modified, 3 untracked-new); `.ai/core/**`, `.ai/adapters/**`, `spec/**`, `BINDING.md`, `.gitignore`, all prior AMDs/ADRs, VER-001..003, and the pre-flight report show zero diff vs HEAD; no `core/MANIFEST.lock`; ledger = `HEAD` (seq 0, genesis, entry_hash null) + `SEG-0000/.keep` only; HEAD == origin/main, tag list unchanged (v0.1.0–v0.10.0 + baseline, no new tag); attribution grep (co-authored/generated/AI/product names, trailer forms) exits empty on all three new artifacts, which attribute by AMD-20 role·session pairs; V-25 encoding (UTF-8 no BOM, LF-only, single terminal LF) passes on all 8 touched files |

## 4. Findings

| ID | Severity | Finding | Needed disposition |
|---|---|---|---|
| FIND-Q4-1 | **INFO** | The tokenizer pin is trust-on-first-use: at the *first* authoritative Stage 6 measurement there is no pre-recorded value to verify against, so artifact authenticity at that one moment rests on the build's human approval, not on a recorded pin. This is explicit, LAW-12-justified, and freezes correctly thereafter via the approval-bound lock — not silently unpinned. | At the first Stage 6 build, the human owner (or QA) should compare the measured artifact hashes against independently published upstream values before approving the lock. No artifact change needed now. |
| FIND-Q4-2 | **MINOR** | AMD-30/`metadata.reproducible.distributable` permits "extended headers … pax requires for long paths" inside a declared *POSIX ustar* archive. Pax extended headers are a pax-format feature, and their own block metadata (synthetic entry name, its mtime/uid/gid, keyword ordering) is not canonicalized — a residual determinism gap in exactly the long-path case. Likely moot (all declared `.ai/` paths fit ustar name+prefix limits). | Before the first release build: either verify no emitted path exceeds ustar limits and forbid extended headers outright, or specify pax-header canonicalization. A4 ruling or implementation-spec note; not a re-ruling of OQ-7. |
| FIND-Q4-3 | **MINOR** | `STATE.md` `open_non_blocking` was not extended with `OI-V-06`/`OI-V-07` (nor the OQ-13/OQ-14 reservations), which appear in `OPEN_ITEMS.md`, `ENGINEERING.md` §7, and STATE's own `next_action` prose. Register drift between the structured STATE list and the OPEN_ITEMS register of record. | One-line STATE.md list update at the next lawful STATE write (repository-engineer/PM). Does not void any approval — STATE's registered role is `frozen_set_hash` mirror + blockers, both correct. |

No BLOCKING and no MAJOR findings.

## 5. Overall verdict: **VERIFIED WITH FINDINGS** (3 findings: 2 MINOR, 1 INFO — none voids any digest, approval, or ruling)

All digests I computed, full 64 chars:

- DC-2 worked example (self-validation): `8de12581a7d3aef29454fcdfd696a71e4d5c1a0352f69c7a6b03b167d0f5f1b3`
- DC-2 empty-registry constant: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- DC-4 worked example (independent recompute), exact value: `eb6e969b9f1d31a367ccf83315c1a40f8df0bb1c7dec41566a637ac3740325b1`
- DC-5 worked example SHA-256("abc"): `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`
- Working-tree manifest DC-1 (== APR-006 subject): `ae16ccaca5746b81a2a992841fc1d239fd1c8b0c34657c05611e025a9d8395aa`
- HEAD (`dc811a6`) manifest DC-1 (== APR-006 prior): `9611d547aab51475e3b57a255af52d47972e4024c896edb5c210cf8f9813e557`
- AMD-010 DC-1 (== APR-007 subject, == FROZEN row), exact value: `486be10eb3bea89fb8c6c99949f1bb48e884cb556879e594cdd778dac5b0b829`
- 26-member DC-2 aggregate (== FROZEN §Aggregate, == STATE.frozen_set_hash): `80cd3ebe0ce971b079fe598bac401ab959f77c7c900a54caa6e0a09963fdf2e8`
- Reproduced 25-member prior aggregate: `4a9e88d91fea4f7b52c2371cbc5438071625b7dd0074ad389f9f9f47b128fc22`
- Reproduced 24-member prior aggregate: `080771b0e26e365decebaa4118a27b4a46c73b7beeb3fb599009ce4ef6b6367a`

(The auditor's original transmission carried two mid-list line-wrap artifacts, flagged by the auditor as presentation-only; the "exact value" strings above are the computed digests as the auditor stated them.)

### (a) Exact remaining prerequisites for Stage 6 execution

1. **Human decision — OQ-13 allocation** (open, human-owner): choose (a) enable `software.*` roles / (b) separate software-profile project / (c) external contract. AMD-34 recommends (a). Until chosen, no actor may lawfully accept the implementation work; if (a), it additionally requires an A4 amendment + LAW-10 approval + BINDING `enabled_agents` edit (AMD-006 pattern).
2. **Implementation — CMP-BLOCK-004 (Stage-6-only increment now sufficient per AMD-25)**: deterministic software that reads the verified Stage 1–5 tree, computes DC-1 per covered file and DC-4, emits `MANIFEST.lock` per the declared serialisation, produces the `budget_measurement` member, builds the deterministic ustar distributable, computes DC-5 + sidecar, writes the BINDING pin, and self-executes the AMD-33 two-run byte-identity check.
3. **Implementation — CMP-BLOCK-005, Stage-6 slice only**: the dual-tokenizer measurement capability (TF-1 `cl100k_base` + TF-2 T5 `spiece.model`, artifacts in hand, pins measured at first build — FIND-Q4-1 disposition applies here).
4. **Precondition run — AMD-31**: every compile-time check except V-10 (V-01…V-09, V-23…V-25) implemented far enough to pass against the manifest + Stage 1–5 output immediately before emission (V-01…V-08/V-23…V-25 need no new infrastructure beyond DC-1/DC-2 implementations; V-09 rides on item 3).
5. **Human decision — OQ-14 / explicit Stage 6 authorization** (standing instruction of `S-2026-08-08-03`, expressly preserved by AMD-010).

Not prerequisites for Stage 6 (they gate the campaign/Release 1.0.0 only): full six-stage compiler, V-10 two-platform evidence, V-11…V-21 harnesses, three reference projects, OI-V-06 (V-14 trial count), OI-V-07/OI-C-02 re-emissions.

### (b) Is human authorization now the ONLY remaining gate?

**No.** The specification layer is complete — after these rulings no specification gap blocks Stage 6 — but **three distinct things remain**: (1) an open human *decision* prior to authorization: the OQ-13 allocation choice, without which no one may lawfully build the compiler increment; (2) substantial *implementation work*: the deterministic Stage-6 increment plus the tokenizer capability plus the compile-time precondition checks (items 2–4 above), none of which exists as software today; and (3) the OQ-14 *authorization* itself. Human authorization becomes the sole remaining gate only after the allocation choice is made and the CMP-BLOCK-004/-005 Stage-6-slice implementation exists and passes its AMD-31 preconditions.
