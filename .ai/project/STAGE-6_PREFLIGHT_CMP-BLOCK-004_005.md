# Stage 6 Pre-Flight Requirements Determination — CMP-BLOCK-004 / CMP-BLOCK-005

> **Instance artifact.** Partition `project`. Planning report, authority A3.
>
> **Filing note.** Produced by a cold-context `project-manager` subagent (`project-manager · S-2026-08-08-03c`), dispatched at live human-owner direction (rank 1) during session `S-2026-08-08-03` after the Release 0.10 close (`3792a93`, tag `v0.10.0`). Filed **verbatim** by that session; the analyst neither filed nor attested to the filing. This is a requirements determination, not a gate disposition, not an implementation, and not a Stage 6 execution. Per the project-manager contract the analyst cannot verify its own plan; the citations are the evidence, reproducible from the repository alone.

---

**Identity:** `project-manager · S-2026-08-08-03c` (A3) — cold context, no state from prior sessions.

**Independence / method declaration.** I read, in full or in the cited sections: `framework/AIEF-FRZ-001_Framework_Architecture_Freeze_1.0.0.md` (all 544 lines), `framework/framework.manifest.json` (all 517 lines), `framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md` (all 589 lines), `.ai/project/OPEN_ITEMS.md`, `.ai/project/BINDING.md`, `.ai/project/STATE.md`, `.ai/BOOT.md`, `.ai/FRAMEWORK.md`, `.ai/core/validation/CHECKS.md`, `.ai/core/validation/MANIFEST`, `.ai/core/schemas/SCH-core-manifest.schema.json`, `.ai/adapters/ADP-ci.md`, `ENGINEERING.md` §7–8, plus repository-wide greps for `tokenizer` and `release digest|distributable`. I confirmed repository HEAD is `3792a93` ("Release 0.10"). Git use was read-only (`git log`, `git status`). **I created, modified and deleted nothing in the repository.** This is a planning report under A3 authority; per the PM contract I cannot verify my own plan (`framework.manifest.json:412,414`), and nothing below is a gate disposition. This report does not execute Stage 6, does not touch the ledger, and implements nothing.

---

## 1. CMP-BLOCK-004 — deterministic compiler (`aief-compile`)

Blocker of record: *"aief-compile not implemented as deterministic software — Blocks: Compiler Stage 6, V-10 — Authority: Software"* (`.ai/project/OPEN_ITEMS.md:18`).

### 1.a Deterministic compiler execution

**Reproducibility requirement, exact wording** (`AIEF-FRZ-001` Part 4, line 383):

> "**Reproducibility requirement:** identical manifest + identical profile selection ⇒ **byte-identical output and identical aggregate digest.**"

Compiler identity (line 381): *"`aief-compile` · Input: `framework.manifest.json` + profile selection · Output: versioned distributable + integrity manifest."* Echoed at `.ai/FRAMEWORK.md:37`: *"Reproducible build required: identical manifest yields identical aggregate digest,"* and in `metadata.reproducible.required: true` (`framework.manifest.json:14`).

**What already exists on disk vs. what must run.** `STATE.md:13-16` declares, explicitly and not by inference (AIEF-AMD-007): `compiler_stage.complete: [1,2,3,4,5]`, `outstanding: [6]`. Stages 1–5 output exists in the tree and Stage 5's output was independently verified (VER-003, cited at `ENGINEERING.md:160`). Stage 6's declared inputs are *"Complete output of Stages 1–5"* (`AIEF-FRZ-001:439`) / `["all stage 1 to 5 output", "metadata.reproducible", "version"]` (`framework.manifest.json:515`). A minimal Stage-6-only implementation must therefore be able to: read the stage 1–5 tree, measure T0/T1 tokens under two tokenizer families, compute DC-1 digests per `core/` file plus the aggregate, emit `MANIFEST.lock` with build provenance, stamp version and budget measurement, write the `BINDING` pin, and emit the distributable and release digest (`AIEF-FRZ-001:440-441`; §1.b–1.d below).

**Full compiler vs. Stage-6-only increment:** the frozen text defines `aief-compile` as a six-stage pipeline (Part 4, lines 385–443) and V-10 verifies *"Build reproducible: identical input yields identical aggregate digest across at least two executions and two platforms"* (`framework.manifest.json:491`) against target `distributable`. Nothing in FRZ-001, the manifest, or the amendments states whether stages may be implemented incrementally, or whether hand-emitted Stages 1–5 satisfy "the build" for V-10 purposes. Precedent cuts both ways: stages 1–5 *were* executed as sessions and accepted, but CMP-BLOCK-004's own text says the compiler is "not implemented as deterministic software" and OPEN_ITEMS binds it to Stage 6 and V-10 only. **OPEN-QUESTION 1.** Note also Stage 6's own failure row — *"Non-reproducible digest halts the build"* (`AIEF-FRZ-001:443`) — makes at least a repeat-execution reproducibility check part of Stage 6 itself, independent of V-10; the number of executions/platforms required *at build time* is not declared. **OPEN-QUESTION 10.**

### 1.b MANIFEST.lock generation

- **Required fields** (`sch-core-manifest`, `framework.manifest.json:478`, and the emitted schema `.ai/core/schemas/SCH-core-manifest.schema.json:7-14`): `framework_version`, `build_provenance`, `hash_algorithm`, `normalisation`, `files`, `aggregate_digest` — severity BLOCKING. `additionalProperties: true`.
- **Coverage:** F-06 (`AIEF-FRZ-001:97-107`): *"`.ai/core/MANIFEST.lock` — per-file digest plus aggregate digest plus build provenance"*; Stage 6 process: *"Compute normalised SHA-256 per `core/` file and the aggregate digest"* (`:440`). `core/` includes `core/profiles/<selected>/` (partition table, `framework.manifest.json:125-126`, both `integrity_verified: true`). However, the L0 root files (`BOOT.md`, `FRAMEWORK.md`, `README.md`) carry `integrity: hashed` in `files[]` (`framework.manifest.json:183-185`) and the `root` partition declares `integrity_verified: true` (`:124`), yet B2a verifies only the *"core/ aggregate digest"*. Whether MANIFEST.lock's `files` list must include the root files is not declared. **OPEN-QUESTION 5.**
- **Hash algorithm and normalisation:** DC-1, normative at `framework.manifest.json:24-32` (restated unchanged by AMD-16, `AIEF-AMD-008:45-51`): SHA-256 over normalised content — decode UTF-8 stripping BOM; CRLF/CR→LF; strip trailing whitespace per line; remove trailing blank lines; exactly one terminal LF; encode UTF-8; 64 lowercase hex. Raw-byte hashing is explicitly rejected (`AIEF-FRZ-001:109-113`).
- **Aggregate digest construction — undeclared.** DC-2 covers *only* the FROZEN.md registry (`framework.manifest.json:33-58`); AMD-16 itself states *"every other use of 'aggregate digest' refers to `core/MANIFEST.lock`, a different set and a different artifact"* (`AIEF-AMD-008:37`). No DC defines the core aggregate's record format, ordering, or self-exclusion (MANIFEST.lock is itself under `core/` and marked `integrity: hashed` at `framework.manifest.json:188`). This **conflicts** with the digest_constructions note: *"Every digest the framework requires, verifies or depends upon is constructed here"* (`framework.manifest.json:23`). I report the conflict; I do not resolve it. **OPEN-QUESTION 4.**
- **B2a consumption** (`.ai/BOOT.md:11`; `AIEF-FRZ-001:205`): *"Verify core/ aggregate digest against MANIFEST.lock; verify MANIFEST.lock against BINDING pin — O(n) hash, no content load — Mismatch → halt, blocking."* F-06 defines the pin as *"the expected aggregate digest"* (`AIEF-FRZ-001:105`). MANIFEST.lock carries a T1 token cap of 200 for the *"digest read"* (`AIEF-FRZ-001:135`; `framework.manifest.json:188`), so the emitted format must let boot read the aggregate within 200 tokens.
- **Pin write:** `generation_order[6].outputs` includes *"project/BINDING.md core_digest_pin (integrity pin write, per AIEF-FRZ-001 Part 4 Stage 6; a field write into an already-emitted instance artifact, not a re-emission of the project partition)"* (`framework.manifest.json:515`, added by AMD-18, `AIEF-AMD-008:297-305`). Today `BINDING.md:12` holds `core_digest_pin: PENDING-STAGE-6`, and `BINDING.md:33` records *"B2a cannot execute until then."*
- **Barrier:** *"MANIFEST.lock is emitted only here. No other stage and no consumer may generate it"* (`AIEF-FRZ-001:442`); repository-engineer is explicitly forbidden to *"Generate MANIFEST.lock outside Compiler Stage 6"* (`framework.manifest.json:379`); V-12 requires project-level regeneration to be *impossible* (§2).

### 1.c Token-budget measurement

- Stage 6 process: *"Measure T0 and T1 token counts with two tokenizer families; take the maximum; verify against per-file caps and the 6,000 aggregate ceiling"* (`AIEF-FRZ-001:440`); failure: *"Budget overrun on any tokenizer halts the build"* (`:443`). V-09: *"Per-file caps respected; T0 plus T1 at most 6000 tokens under both tokenizer families"* (`framework.manifest.json:490`; `CHECKS.md:126`).
- Ceiling and caps: 6,000 = 32,000 × 20% (MI-4: *"Σ token_cap over T0 ∪ T1 ≤ 6,000"*, `AIEF-FRZ-001:367`); per-file caps sum 5,800, headroom 200 (`AIEF-FRZ-001:127-139`); caps are also in `files[]` (`token_cap` per entry). *"Measurement is performed with two tokenizer families; the maximum governs"* (`AIEF-FRZ-001:142`).
- **Which families:** nowhere declared. A repository-wide grep for `tokenizer` finds only "two/both tokenizer families" with no family named; VER-001 used non-authoritative *estimators* ("GPT-style regex pre-tokenizer", `VER-001:228`) and itself flags *"no authoritative measurement is possible"* (`VER-001:231`). **OPEN-QUESTION 2.**
- **Budget measurement record:** it is a declared Stage 6 output (`framework.manifest.json:515`; `AIEF-FRZ-001:441` "budget measurement record") and Stage 6 must *"Stamp version and budget measurement"* (`:440`) — but no schema, path, or content specification exists for it, it has no `files[]` entry, and `sch-core-manifest` lists no budget field (though `additionalProperties: true` would admit one). What the record must contain, and where it lives, is underspecified. **OPEN-QUESTION 6.**

### 1.d Release digest / distributable archive

`generation_order[6].outputs`: `MANIFEST.lock`, budget measurement record, **distributable archive**, **release digest**, pin write (`framework.manifest.json:515`; `AIEF-FRZ-001:441`). L7 = *"MANIFEST.lock, budget stamp, distributable"* (`AIEF-FRZ-001:197`). The compiler's overall output is *"versioned distributable + integrity manifest"* (`:381`), and Stage 1's zero-dead-file rule constrains its content: universal core plus selected profile only (`:80`). Beyond that:

- **"Release digest" is defined nowhere.** No construction, coverage, or recording location; not obviously identical to `aggregate_digest` and not covered by DC-1/DC-2/DC-3. **OPEN-QUESTION 3.**
- **Distributable archive format, path, and disposition** (archive format, whether tracked in-repo, relation to the installed tree) are undeclared. **OPEN-QUESTION 7.**

---

## 2. CMP-BLOCK-005 — verification infrastructure

Blocker of record: *"Tokenizer, multi-platform, concurrency infrastructure absent — Blocks: V-09, V-12, V-15, V-18 — Authority: Software"* (`.ai/project/OPEN_ITEMS.md:19`). Emitted Stage 5 declarations at HEAD `3792a93`: `.ai/core/validation/CHECKS.md` and `.ai/core/validation/MANIFEST` (25 checks, all BLOCKING).

**V-09 — Token budget validation** (`CHECKS.md:126`; `framework.manifest.json:490`)
> "Per-file caps respected; T0 plus T1 at most 6000 tokens under both tokenizer families"

Minimum infrastructure: **two tokenizer families** (identities undeclared — OPEN-QUESTION 2), applied per-file against `files[].token_cap` and in aggregate against 6,000, taking the maximum (`AIEF-FRZ-001:142,440`). This is the *same* tokenizer capability Stage 6 itself needs (§1.c) — the one part of CMP-BLOCK-005 that is on Stage 6's own path.

**V-12 — Core integrity validation** (`CHECKS.md:164`; `framework.manifest.json:493`)
> "Tamper on any core file detected; project-level regeneration of MANIFEST.lock impossible; zero false positives across three platforms"

FRZ-001 names the three: *"zero false positives across Windows, Linux, macOS with mixed line endings"* (`AIEF-FRZ-001:471`). Minimum infrastructure: an existing `MANIFEST.lock` (i.e., Stage 6 has run — V-12 cannot execute before it), a tamper-injection harness over `core/**`, a demonstration that project-level tooling cannot regenerate the lock, and **execution environments on all three named platforms** with mixed line-ending fixtures (exercising DC-1 normalisation). Shares platform infrastructure with **V-10** (*"at least two executions and two platforms"*, `framework.manifest.json:491` — the two platforms are unnamed; **OPEN-QUESTION 12**).

**V-15 — Concurrency validation** (`CHECKS.md:182`; `framework.manifest.json:496`)
> "At N of 2, 5 and 10 concurrent sessions: zero lost state updates, zero ledger gaps, deterministic conflict outcome, STATE regenerable from ledger"

Minimum infrastructure: a **concurrency harness at N = 2, 5, 10** driving full session transactions (lock acquisition per §1.3, branch-per-session, ledger append with DC-3 chaining per `framework.manifest.json:60-98`, STATE regeneration from ledger per `AIEF-FRZ-001:48-49`). Shares session/ledger machinery with **V-13** (ledger harness at depths 10 / 1,000 / 100,000 with segment sealing at 500, `CHECKS.md:170`), **V-14** (fault injection killing between entry write and HEAD update, detection at next boot *"in all trials"* — trial count undeclared, `CHECKS.md:176`; FRZ says "100% of trials", `AIEF-FRZ-001:473`; **OPEN-QUESTION 11**), **V-17** (12-phase traversal with ordered session close, `CHECKS.md:194`), and **V-11** (B1–B9 in order with induced-fault halts at B2a/B4/B4a, `CHECKS.md:158`) — all five are LAW-09-bound (`CHECKS.md:61`). Note V-14/V-11 additionally require a **fault-injection capability**, and V-11's B2a fault case requires Stage 6 output to exist.

**V-18 — Multi-discipline install** (`CHECKS.md:202`; `framework.manifest.json:499`)
> "Install onto mechanical, software and research reference projects with zero dead files and zero core edits required"

Minimum infrastructure: **three reference projects** (mechanical, software, research — none exists in this repository) and an install harness driving the compiler per-profile — which presupposes at minimum Stage 1's profile-selective emission and Stage 3's install-refusal semantics, i.e., more than a Stage-6-only compiler (feeds OPEN-QUESTION 1). Shares reference-project/install infrastructure with **V-19** (full lifecycle per profile) and **V-21** (upgrade wholesale-replacement test).

Also relevant: V-23/V-24/V-25 (AMD-19, `AIEF-AMD-008:326-365`) are declared and emitted but *"not implemented as software — execution requires CMP-BLOCK-004/-005 infrastructure"* (OI-V-02, `.ai/project/OPEN_ITEMS.md:26`). V-24 requires only DC-1 + DC-2 (both fully specified with published worked examples that any implementation must reproduce exactly: DC-2 at `AIEF-AMD-008:75-93` / `framework.manifest.json:47-53`; DC-3 at `AIEF-AMD-008:173-211` / `framework.manifest.json:91-96` — *"Any implementation that does not produce exactly this value for exactly this input is non-conforming"*).

**CI adapter:** `ADP-ci.md` describes the intended execution: CI reads `core/validation/MANIFEST`, runs compile-time checks on every push, runtime checks at gates, installation checks at release; *"CI shall never write to the repository"* (`ADP-ci.md:34-41,49`). It is **stale** — "All 22 checks are BLOCKING" and phase ranges omitting V-23/24/25 (OI-C-02, `.ai/project/OPEN_ITEMS.md:30`; blast radius at `AIEF-AMD-008:535`) — and requires a Stage 4 re-emission before it can bind an implementation. **Feeds OPEN-QUESTION 9.**

---

## 3. Dependency and sequencing analysis

**Declared execution order** (`AIEF-FRZ-001` §6.4, line 538, quoted exactly):

> "**Execution order:** author `framework.manifest.json` → Compiler Stage 1 → 2 → 3 → 4 → 5 → 6 → execute V-01…V-21 → Release 1.0.0."

And Part 5's preamble (line 449): *"Every check below must pass before Framework Release 1.0.0."*

**Reading of the frozen text:** the validation campaign sits *after* Stage 6 and *before* Release 1.0.0. On that text, Stage 6 emission does **not** wait for the campaign, and most of CMP-BLOCK-005 gates Release 1.0.0, not Stage 6. This matches the blocker ledger: CMP-BLOCK-004 blocks "Compiler Stage 6, V-10"; CMP-BLOCK-005 blocks "V-09, V-12, V-15, V-18" — not Stage 6 (`.ai/project/OPEN_ITEMS.md:18-19`).

**Gates Stage 6 execution itself:**
1. Deterministic Stage 6 implementation — DC-1 hashing, core aggregate (construction open, OQ-4), `MANIFEST.lock` per `sch-core-manifest`, pin write, distributable + release digest (§1.a–1.d) — CMP-BLOCK-004.
2. Dual-tokenizer measurement capability — Stage 6's own process and failure condition (`AIEF-FRZ-001:440,443`); nominally filed under CMP-BLOCK-005 but on Stage 6's critical path. Families undeclared (OQ-2).
3. Build-time reproducibility check — *"Non-reproducible digest halts the build"* (`AIEF-FRZ-001:443`); method underspecified (OQ-10).
4. **Explicit human authorization** — standing instruction of `S-2026-08-08-03` (`ENGINEERING.md:158,162`; `STATE.md:14`). Not an engineering item; a rank-1 authority item.

**Gates only the full campaign / Release 1.0.0:** multi-platform environments (V-10 two platforms, V-12 three), concurrency harness N=2/5/10 (V-15), ledger-depth and crash/fault harnesses (V-13, V-14, V-11), 12-phase traversal (V-17), adversarial corpus (V-16), three reference projects and install/lifecycle/upgrade harnesses (V-18, V-19, V-21), path/git-policy checks (V-20, V-22).

**Residual ambiguity, reported not resolved:** (i) V-09 and V-10 are declared `phase: compile-time` (`framework.manifest.json:490-491`), and AMD-19 rules V-24 compile-time *because* *"the check must run before that [a build consuming a frozen input], not after release"* (`AIEF-AMD-008:345`) — yet §6.4 places the whole campaign after Stage 6, and Stage 6's frozen process does not list executing any V-check. Whether a conforming Stage 6 run must first execute the compile-time checks (V-01–V-10, V-23–V-25) is therefore not decidable from the text — **OPEN-QUESTION 8**; this determines exactly how much of CMP-BLOCK-005 gates Stage 6 at all. (ii) §6.4 says "V-01…V-21" and FRZ-001 was not amended (`AIEF-AMD-008:7` "Does not amend AIEF-FRZ-001"), while the emitted Stage 5 register declares 25 BLOCKING checks (`CHECKS.md:17`) — **OPEN-QUESTION 9**.

---

## 4. Allocation gap

`BINDING.enabled_agents` (`.ai/project/BINDING.md:19-28`) enables the five universal roles plus four `mechanical.*` roles. **No `software.*` role is enabled**, and under the zero-dead-file rule (`AIEF-FRZ-001:80`) the software profile's agent files are not even installed in this repository. Both blockers carry Authority "Software" (`OPEN_ITEMS.md:18-19`) — as installed, **no enabled role may lawfully accept the implementation work**, and universal roles cannot absorb it: the PM is forbidden to *"Make engineering decisions"* (`framework.manifest.json:412`), the QA engineer to author what it validates, the repository-engineer to *"Generate MANIFEST.lock outside Compiler Stage 6"* (`:379`).

What the manifest's software profile declares, if activated (`framework.manifest.json:151-165`): agents `software.software-engineer`, `software.test-engineer`, `software.platform-engineer` (contracts at `:433-435`), recurring-gate lifecycle LC-S01–LC-S06.

**Whose decision:** `BINDING.approval_authority: human-owner` (`BINDING.md:16`); `project/BINDING` declares the active profile (`AIEF-FRZ-001:77`); profile/agent-set changes have required an A4 manifest amendment plus human approval in every precedent (AIEF-AMD-006 added `mechanical.cad-engineer`; Release 0.6). Whether to (a) enable software roles in this instance, (b) run the compiler build as a separate software-profile project, or (c) contract the work outside the framework is a **human-owner / A4 decision**. This report, at A3, can only allocate against roles that exist and are enabled — none qualifies today. **OPEN-QUESTION 13.**

Separately noted for the owner: OI-P-02 — `ROSTER.md` marks `project-manager` (this role) UNASSIGNED; dispatches rest on rank-1 live instruction (`OPEN_ITEMS.md:36`).

## 5. Open questions

Each is decidable by the human owner or A4; none is resolved by assumption here (LAW-12).

1. **Compiler scope:** Does clearing CMP-BLOCK-004 require the full six-stage `aief-compile` (Part 4 as written), or does a Stage-6-only increment suffice given Stages 1–5 exist on disk and are verified? The frozen text is silent on incremental implementation; V-18/V-10 arguably need Stages 1+3 executable.
2. **Tokenizer families:** Which two tokenizer families are normative for V-09 and the Stage 6 budget measurement? No source declares them.
3. **Release digest:** What is its construction, coverage, and recording location? Is it identical to `MANIFEST.lock.aggregate_digest` or distinct?
4. **Core aggregate construction:** What are the record format, ordering, and self-exclusion rules for the `core/` aggregate digest? DC-2 covers only the freeze registry; the `digest_constructions` completeness note (`framework.manifest.json:23`) conflicts with this gap. (An A4 amendment in the DC-2 style, with a worked example, would close it — decision, not assumption.)
5. **Root-file coverage:** Must `MANIFEST.lock.files` include the L0 root files (`BOOT.md`, `FRAMEWORK.md`, `README.md` — `integrity: hashed`, root partition `integrity_verified: true`) when B2a verifies only the "core/ aggregate digest"?
6. **Budget measurement record:** What schema/path/content? Is it stamped into `MANIFEST.lock` (admissible under `additionalProperties: true`) or a separate artifact — and if separate, does it need a `files[]` entry (V-01/MI implications)?
7. **Distributable archive:** Format, path, contents, and whether it is tracked in-repo.
8. **Compile-time check ordering:** Must Stage 6 execution be preceded by execution of the compile-time checks V-01–V-10, V-23–V-25 (per AMD-19's "must run before the build" rationale for V-24), or does §6.4's post-Stage-6 campaign ordering govern? This decides how much of CMP-BLOCK-005 gates Stage 6.
9. **Campaign scope:** Is the pre-Release-1.0.0 campaign V-01…V-21 (frozen §6.4, unamended) or V-01…V-25 (emitted CHECKS.md)? Correspondingly, authorize the Stage 4 re-emission of the stale `ADP-ci.md` (OI-C-02) so CI enumerates 25.
10. **Build-time reproducibility method:** How many executions, and on how many platforms, constitute Stage 6's own "non-reproducible digest halts the build" check, as distinct from V-10's ≥2 executions / ≥2 platforms?
11. **V-14 trial count:** "All trials" / "100% of trials" — how many trials?
12. **V-10 platforms:** Which two platforms? (V-12's three are named: Windows, Linux, macOS.)
13. **Allocation:** Enable software roles in this instance, stand up a separate software-profile project for the compiler, or contract the work — human-owner decision (`approval_authority: human-owner`), with any manifest/BINDING change following the AMD-006/LAW-10 pattern.
14. **Stage 6 authorization:** Independent of everything above, Stage 6 execution requires explicit human authorization (standing instruction, `S-2026-08-08-03`).

## 6. Minimum-clearance summary

Scope classes are **engineering judgment (S ≈ days, M ≈ weeks, L ≈ multi-week+), clearly labeled as judgment, not requirement**.

| # | Requirement | Clears | Scope (judgment) | Decision needed from human |
|---|---|---|---|---|
| 1 | Stage 6 core: DC-1 hashing, core aggregate, `MANIFEST.lock` (6 fields), pin write, distributable + release digest | CMP-BLOCK-004 (Stage 6 path) | **S–M** | OQ-1, 3, 4, 5, 6, 7, 14 |
| 2 | Dual-tokenizer budget measurement (per-file caps + 6,000 ceiling, max governs) | Stage 6 process; V-09 | **S** once families chosen | OQ-2 |
| 3 | Build-time reproducibility check (repeat execution, digest compare) | Stage 6 failure condition | **S** | OQ-10 |
| 4 | Full six-stage `aief-compile` (only if OQ-1 answered "full") | CMP-BLOCK-004 entirely; enables V-10/V-18 as specified | **L** | OQ-1 |
| 5 | V-23/V-24/V-25 implementations (DC-1/DC-2 + worked-example conformance) | OI-V-02; compile-time gate if OQ-8 answered "before" | **S** each | OQ-8 |
| 6 | Multi-platform execution: Windows/Linux/macOS, mixed line endings | V-12; V-10 (2 platforms) | **M** | OQ-12 |
| 7 | Concurrency harness N=2/5/10 + session/ledger machinery (DC-3) | V-15; shared with V-13/V-14/V-17 | **M** | OQ-11 |
| 8 | Fault-injection harness (boot halts; entry/HEAD crash window) | V-11, V-14 | **M** (shares #7) | OQ-11 |
| 9 | Three reference projects + install/upgrade harness | V-18; shared with V-19/V-21 | **M** | OQ-1 (needs Stage 1/3 executable) |
| 10 | Role activation or contracting for all software work above | Lawful allocation of #1–#9 | — (authority act, not engineering) | OQ-13 |
| 11 | `ADP-ci.md` Stage 4 re-emission (25 checks) | OI-C-02; CI binding for the campaign | **S** (compiler-dependent) | OQ-9 |

**Minimum to clear CMP-BLOCK-004 for Stage 6 specifically** (on the §6.4 reading, and subject to OQ-1/OQ-8): rows 1–3, plus the human decisions OQ-2/3/4/6/7 which are specification gaps no implementation can lawfully fill by assumption. **CMP-BLOCK-005 in full** (rows 6–9) gates the validation campaign and Release 1.0.0, not — on the frozen execution order — Stage 6 emission itself, with the single exception of the tokenizer capability (row 2), which Stage 6's own process requires.
