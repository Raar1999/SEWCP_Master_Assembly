# VER-007 — Independent QA Audit of `S-2026-08-08-10` (AIEF-AMD-013 / CMP-BLOCK-006 determination / OQ-B1…B5)

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-verification-report`.
>
> **Filing note.** Produced by a cold-context `qa-engineer` session (`qa-engineer · S-2026-08-08-11`), dispatched at live human-owner direction (`core/PRECEDENCE.md` rank 1) as the mitigating control for the separation-of-duties departure recorded in `AIEF-AMD-013` § *Separation of Duties* and in `OPEN_ITEMS.md` **SOD-1**, which requires that this audit *"include independent recomputation of the §AMD-41 re-measurement, which is otherwise a session's own evidence about its own finding."* Session id `S-2026-08-08-11` was adopted after confirming from the repository that `-01` … `-10` (with sub-sessions `-03b`, `-03c`, `-04b`, `-05b`, `-09b`) are consumed and `-11` is unused. This report is filed by its author; the only other repository writes made by this session are the single residual row **OI-V-10** in `OPEN_ITEMS.md` and the one-token `STATE.md` range sync that registers it — both expressly permitted by the dispatch and made for no other purpose.

---

# QA Audit Report — `qa-engineer · S-2026-08-08-11` (cold, serial adoption)

**Auditor:** `qa-engineer` (A2), cold context · **Date:** 2026-08-08 · **Repository:** `D:\Fusion Projects\SEWCP_Master_Assembly` at HEAD `8546960ea4e0c433e992aeb5b6c934c92b4ed877` == `origin/main`, working tree carrying the uncommitted output of sessions `-05` … `-10`

## 0 · Boot state recovered

Boot sequence B1–B9 executed from files only, in order: `CLAUDE.md` → `ENGINEERING.md` → `.ai/BOOT.md` (B1) → `.ai/FRAMEWORK.md` (B2, AIEF 1.0.0, pin `>=1.0.0 <2.0.0` — compatible) → **B2a not executable** (`core/MANIFEST.lock` absent; `BINDING.core_digest_pin` = `PENDING-STAGE-6`) → `project/STATE.md` (B3) → `project/ledger/HEAD` (B4: `seq 0`, `genesis`, `entry_hash null`; check 1 vacuous, checks 2 and 3 pass, `STATE.last_ledger_seq` 0 == `HEAD.seq` 0 — **reconciled**) → B4a not executed, no `.session.lock` exists (DEV-02) → `project/BINDING.md` (B5: `LC-M04` / `LC-M04-EXIT` / profile `mechanical` / authority `human-owner` / 12 enabled agents) → `core/PRECEDENCE.md` + `core/laws/INDEX.md` (B6) → `project/OPEN_ITEMS.md` (B7) → orientation declared (B8) → role assigned (B9). Blockers at boot: `ECR-D-001…004`, `CMP-BLOCK-004`, `-005`, `-006`, `C-4`.

## 1 · Independence declaration

I am a cold-context QA session holding no state from any prior session, and I authored none of the artifacts under audit. Under `AIEF-AMD-008` §AMD-20 agent identity for LAW-04/LAW-05 independence is the pair (role, session): I differ from the audited party `chief-systems-engineer · S-2026-08-08-10` **in both role and session**, and from every other contributing actor (`software.software-engineer · -07`, `software.platform-engineer · -08`, `software.test-engineer · -09`, `qa-engineer · -09b`, the `project-manager` filer) in at least session.

Every digest in this report was computed **twice by independent means**: once with an implementation of DC-1/DC-2 written fresh this session in my scratchpad from the normative text of `framework/framework.manifest.json` `metadata.reproducible.digest_constructions`, importing nothing from `src/`; and once with the repository's own `src/aief_stage6/digests.py`. Both agree on every value. Token counts were produced by my own tokenizer assembly (my own transcription of the cl100k pre-tokenisation pattern, my own `.tiktoken` rank parser, SentencePiece over the artifact in hand), and independently corroborated by the repository's own test suite, whose `TestV09Recomputation` recomputation reports the same totals. I did not trust one number in the dispatch order; every figure below is my own.

Footprint: read-only on the repository except for this file and the two register writes named in the filing note. All scratch output routed to the session scratchpad. `HEAD` unchanged before and after (`8546960…`), no commit, no push, no tag, no ledger write, no Stage 6 execution, no `MANIFEST.lock`, no distributable.

## 2 · Method

(1) Booted from files; enumerated the audit subject myself from `git status --porcelain -uall`, working-tree diffs against `HEAD`, and the artifacts' own session attributions — not from the dispatch order. (2) Read `AIEF-AMD-013` (405 lines), `APR-012`, `APR-013`, `STAGE-6_BUILD_OPEN_QUESTIONS.md`, `FROZEN.md`, `STATE.md`, `OPEN_ITEMS.md`, `ENGINEERING.md`, `ROSTER.md`, `BINDING.md`, `TCR-001`, `VER-004`, `VER-005`, `VER-006`, `AIEF-FRZ-001` §1.8 and the MI-1…MI-12 table, `TPL-current-state`, `SCH-state`, and the `src/aief_stage6` modules that implement the audited constructions. (3) Wrote fresh DC-1/DC-2 and re-derived the tokenizer artifact pins raw-octet from `build/stage6/tokenizer_artifacts/`. (4) Re-measured the full T0 ∪ T1 set under TF-1 and TF-2 — capped and cap-null, present and absent — and rebuilt the per-file table from scratch. (5) Recomputed all 29 registry DC-1s, the DC-2 aggregate, and **all five superseded aggregates** by reconstructing their memberships. (6) Validated the amended manifest against the byte-unchanged frozen schema (Draft 2020-12) and re-derived MI-1, MI-3 strict and MI-4 over all 106 `files[]` entries. (7) Structural-diffed the manifest against `git show HEAD:framework/framework.manifest.json` and mapped every hunk to an approval and an amendment section. (8) Item-by-item content-preservation diff of `STATE.md` and `OPEN_ITEMS.md` against `HEAD`, with a survival check for every removed fact. (9) Attempted independent reproduction of every arithmetic sub-claim in AMD-41 §§2, 4, 5 and 6. (10) Ran the full pytest suite and adjudicated each failure myself. (11) Prohibition sweep: lock, distributable, ledger, tags, commits, `ECR-D-001…004`, `.ai/core/**`, `.ai/BOOT.md`, `BINDING.md`, attribution trailers, git identity.

**Scope and its boundary.** The subject is everything session `S-2026-08-08-10` produced. Because sessions `-05` … `-09b` committed nothing, `git show HEAD:` yields a five-session-old baseline, so the working-tree diff of the four mutable tracked registers and of the manifest spans sessions `-05` … `-10`. Where a change belongs to an earlier session I say so and exclude it. Three of AMD-41's numeric claims describe a tree state that no longer exists anywhere in the repository and are therefore unreproducible in principle — recorded as **FIND-Q7-8**, not held against the audited session.

## 3 · Criteria

| # | Criterion | Result | One-line evidence |
|---|---|---|---|
| C1 | **Token measurement.** Every recorded V-09 figure recomputed by me under both normative families from independently re-derived artifact pins; the audited session's claims reproduce | **PARTIAL** | Both pins re-derived raw-octet and MATCH the TOFU record. All eighteen numbers of `APR-012` § *The reduction performed* reproduce **to the digit** (§4 below), as does every AMD-41 §4 sub-derivation (boot table 346, tier rule 47, governing rule 82, floor 475, no-Cost variant 436) and §5's 41.7%-of-32,000 arithmetic. AMD-41 §2's "five of the eight still reproduce" is **confirmed** — I reproduce all five today. **But** the `OPEN_ITEMS.md` CMP-BLOCK-006 row asserts as *"today"* three figures that were already superseded by the same session before it closed — FIND-Q7-1 |
| C2 | **Digests and hashes.** Every digest asserted in `APR-012`, `APR-013`, `FROZEN.md` and `STATE.md` recomputed, full 64 characters, dual-computed | **PASS** | 29/29 registry DC-1s, the DC-2 aggregate, both approval `subject_hash`es, `STATE.frozen_set_hash` and all five superseded aggregates reproduce under two independent implementations that agree on every octet (§5). `APR-012.subject_hash` = the manifest as it sits on disk; `APR-013.subject_hash` = `AIEF-AMD-013` as it sits on disk; `APR-012.prior_hash` corroborated two ways (§5c) |
| C3 | **Freeze registry integrity** | **PASS** | **29 of 29 verify.** DC-2 over exactly the current 29-member membership = `3395815651…3053d30dc` = `FROZEN.md` § *Aggregate* = `STATE.frozen_set_hash`, all 64 characters, no truncation. Five superseded aggregates retained **and independently reproduced** from their reconstructed memberships (28, 27, 26, 25, 24); the non-reproducible pre-DC-2 value `42bce7b0…` retained and correctly marked. Registration history carries both new rows with their approvals |
| C4 | **Manifest integrity** | **PASS** | Draft 2020-12 validation against the byte-unchanged frozen schema: **0 errors**. MI-1: 0 duplicate ids, 0 duplicate paths over 106 entries. MI-3 strict: **0** dangling `depends_on`/`referenced_by`/`references` targets. MI-4: Σ `token_cap` over T0 ∪ T1 = **5800**, unchanged before and after. Manifest pure ASCII (0 non-ASCII code points). Structural diff vs `HEAD` yields exactly sixteen changes: **thirteen** attributable to `AMD-013`/`APR-012`, each mapping 1:1 onto a row of APR-012's enumeration and a cited AMD section, and **three** to `AMD-012`/`APR-010` (session `-06`, pre-dating this audit's subject). **Nothing unauthorised rides along** — DC-1's non-empty normalisation, DC-2, DC-3, DC-4's coverage/grammar/order/preimage/self-exclusion/B2a procedure/`lock_serialisation`/worked example, DC-5, TF-1, TF-2 and every `token_cap` are byte-unchanged |
| C5 | **Content preservation** | **PASS** | `OPEN_ITEMS.md`: **zero** item identifiers removed (37 → 44; 7 added, 0 lost); AMD-41 §8's claim *"every entry it carried before this session it carries after"* verified. `STATE.md`: all eight `tpl-current-state` required fields retained; **every** digest and lineage token in the `HEAD` text survives verbatim in `FROZEN.md` (15/15 checked); every removed narrative fact traced to a cited authoritative home (§6); `open_non_blocking` is now *more* complete than at `HEAD` (`OI-V-05` was previously omitted). One INFO on the dropped provenance header — FIND-Q7-7 |
| C6 | **Determinism and reproducibility** | **PARTIAL** | Each of AMD-43…AMD-48 is evaluable from declared inputs alone; none admits the working tree as an input to a coverage or digest decision, so **B2a is not weakened**. `binding_pin_write` is a total function and matches exactly one line of `BINDING.md` today (verified). **But** AMD-48's stated ground for the empty-content rule is factually false against DC-1's own normalisation (FIND-Q7-2), and AMD-45 leaves up to 200 tokens of the measured domain outside the aggregate ceiling test without recording it (FIND-Q7-3) |
| C7 | **Lawfulness and process** | **PASS** | LAW-01/LAW-10: two approvals, content-hash bound, subjects verified against disk, `prior_hash` corroborated. LAW-12: `OQ-15`, `OI-C-08`, `OI-C-09` reserved or delegated, not assumed; no ambiguity resolved by assumption that I could find. AMD-20 identity: OQ-B1…B5 raised by `software.software-engineer · S-2026-08-08-07`, ruled by `chief-systems-engineer · S-2026-08-08-10` — differs in **both** role and session, satisfying the bar the raising artifact itself set. SOD-1 recorded in the established form, and **narrowed** (the `src/**` delta declined and left to A1). `.ai/core/**` and `.ai/BOOT.md` unmodified; `.ai/project/BINDING.md` carries only session `-05`'s three AMD-011 lines and nothing from `-10`. Amendment sections **AMD-01 … AMD-48 continuous, no gap, no collision**. One MINOR on an unrecorded role — FIND-Q7-5 |
| C8 | **Prohibitions honoured** | **PASS** | No `.ai/core/MANIFEST.lock`. No `*.tar`, no `*.sha256`, no distributable anywhere in the tree. `ledger/HEAD` at `seq 0` / `genesis` / `entry_hash null`; `ledger/SEG-0000/` holds only `.keep`; no `L-0000001`. Tags unchanged (`v0.1.0`…`v0.10.0`, `baseline/spec-revA`); `git describe` = `v0.10.0-2-g8546960`. `HEAD` == `origin/main` == `8546960…`, nothing committed or pushed. `spec/**` and `implementation/**` — including the `ECR-D-001…004` package — **byte-identical to `HEAD`**. Zero hits across all new artifacts for any attribution trailer form, model, vendor or product name (case-insensitive sweep of the LAW-07 forbidden set). `git config user.name`/`user.email` = `Raar1999 <91361865+Raar1999@users.noreply.github.com>`, matching the last commit's author and committer |
| C9 | **Test suite** | **PASS** | 114 collected, **111 pass, 3 fail** in 1.09 s — exactly as `OI-C-09` records. I adjudicated each failure independently: all three are stale snapshot assertions, **no implementation defect** (§7). Corroboration, not sole evidence: the failing tests' own recomputation reports totals `TF-1 12868 / TF-2 16012`, identical to mine and to `APR-012` |
| C10 | **Residual completeness** | **PARTIAL** | `OQ-15`, `OI-C-08` and `OI-C-09` are opened with owners, and I **agree all three reservations are legitimate** (§8). `STATE`/`OPEN_ITEMS` are mutually consistent on ids and blockers; `ENGINEERING.md` retains its non-authority disclaimer. **But** one consequence of AMD-45 is unrecorded (FIND-Q7-3) and `ENGINEERING.md` §6/§7 contradict `ROSTER.md` and the same file's own §8 (FIND-Q7-6) |

**7 PASS · 3 PARTIAL · 0 FAIL.**

## 4 · Recomputed token measurement — both families

Measured by me, this session, from the pinned artifacts. Artifact pins re-derived raw-octet: **TF-1** `223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7` (`cl100k_base.tiktoken`), **TF-2** `d60acb128cf7b7f2536e8f38a5b18a05535c9e14c7a355904270e15b0945ea86` (`spiece.model`) — both MATCH the `TRUST_ON_FIRST_USE.json` custody record.

### 4a · The AMD-42 measured set (capped T0 ∪ T1)

**Measurement instant: the tree as the audited session left it**, before this report's own residual row was written. The post-filing instant is recorded at §4e; per AMD-42 `measurement_instant` both are true of their instant and neither is a constant.

| `files[]` path | Tier | Cap | TF-1 | TF-2 | Governing | Verdict |
|---|---|---|---|---|---|---|
| `BOOT.md` | T0 | 400 | 445 | **504** | 504 | **FAIL** |
| `FRAMEWORK.md` | T1 | 1100 | 652 | 748 | 748 | PASS |
| `core/MANIFEST.lock` | T1 | 200 | — | — | — | not on disk — emitted by Stage 6 |
| `core/PRECEDENCE.md` | T1 | 700 | 341 | 382 | 382 | PASS |
| `core/laws/INDEX.md` | T1 | 900 | 598 | 721 | 721 | PASS |
| `project/BINDING.md` | T1 | 800 | 483 | 574 | 574 | PASS |
| `project/STATE.md` | T1 | 1100 | 921 | 1083 | 1083 | **PASS** |
| `project/OPEN_ITEMS.md` | T1 | 600 | 9428 | **12000** | 12000 | **FAIL** |
| **Totals over the measured set** | | ceiling 6000 | **12868** | **16012** | **16012** | **FAIL** |

### 4b · Cap-null T0 ∪ T1 (outside the record per AMD-42)

| Path | TF-1 | TF-2 |
|---|---|---|
| `core/workflows/WF-01_session.md` | 359 | 437 |
| `project/ledger/HEAD` | **411** | **504** |
| `adapters/INDEX.md` | 539 | 672 |
| `core/profiles/mechanical/PROFILE.md` | 414 | 527 |
| `core/profiles/mechanical/lifecycle/INDEX.md` | 398 | 530 |
| `core/profiles/software/PROFILE.md` · `.../lifecycle/INDEX.md` · both `research` entries | — | not on disk (AMD-011 §AMD-36) |

T0 ∪ T1 has **17** `files[]` members; **8** capped, **9** cap-null; **4** of the cap-null are not on disk by ruling. Σ `token_cap` = **5800**. All three counts confirm AMD-42's own arithmetic and `AIEF-FRZ-001` §1.8's Sum 5,800 / Headroom 200 rows.

### 4c · Reproduction against the four recorded sources

| Row | TCR-001 §3.2 / VER-006 C4 (`S-08`/`-09b`) | `OPEN_ITEMS` CMP-BLOCK-006, asserted *"today"* | `AMD-41` §1, session start | `APR-012`, session close | **VER-007 (me, now)** |
|---|---|---|---|---|---|
| `BOOT.md` TF-1/TF-2 | 445 / 504 | 504 | 445 / 504 | 445 / 504 | **445 / 504 ✔ all** |
| `FRAMEWORK.md` | 652 / 748 | — | 652 / 748 | 652 / 748 | **652 / 748 ✔ all** |
| `core/PRECEDENCE.md` | 341 / 382 | — | 341 / 382 | 341 / 382 | **341 / 382 ✔ all** |
| `core/laws/INDEX.md` | 598 / 721 | — | 598 / 721 | 598 / 721 | **598 / 721 ✔ all** |
| `project/BINDING.md` | 483 / 574 | — | 483 / 574 | 483 / 574 | **483 / 574 ✔ all** |
| `project/STATE.md` | 1516 / 1791 | **1747** | 1503 / 1747 | 921 / **1083** | **921 / 1083** |
| `project/OPEN_ITEMS.md` | 6261 / 7937 | **8673** | 6867 / 8673 | 9428 / **12000** | **9428 / 12000** |
| **Totals** | 10296 / 12657 | **10889 / 13349** | 10889 / 13349 | 12868 / **16012** | **12868 / 16012** |

**Verdict on reproduction.** The five immutable `root`/`core` values reproduce to the digit across all four sources and my own measurement — five of eight, exactly as AMD-41 §2 claims. The three `project`-partition values do not, and each successive measurement instant differs from the last. This is genuine drift in `mutability: mutable`, `lifecycle: instance-created` files and is a declared property under AMD-42 `measurement_instant` — I accept that explanation **for `AIEF-AMD-013` and `TCR-001`/`VER-006`**, which are frozen or historical records of a stated instant. I do **not** accept it for `OPEN_ITEMS.md`, which is the live authoritative register, is re-read at every boot step B7, and asserts its figures with the word *"today"*: those figures were already false when the session that wrote them closed, and the same session recorded the true ones in `APR-012`. See FIND-Q7-1.

### 4d · AMD-41's arithmetic sub-claims, independently reproduced

| Claim (AMD-41) | Recomputed by me | Verdict |
|---|---|---|
| `BOOT.md` eleven-row boot table = 346 TF-2 | header + separator + 11 rows = **309 / 346** | **reproduces to the digit** |
| tier rule = 47 TF-2 | `## Tier rule` section = **45 / 47** | **reproduces** |
| governing rule = 82 TF-2 | `## Governing rule` section to EOF = **58 / 82** | **reproduces** |
| render floor = 475 > 400 | 346 + 47 + 82 = **475** | **reproduces**; the determination that the 400 cap is unachievable by any conforming render **holds** |
| deleting the `Cost` column still leaves 436 | table without the Cost column 307 + 47 + 82 = **436** | **reproduces to the digit** |
| `OPEN_ITEMS.md` at 14.5× its cap | 8673 / 600 = 14.46 at that instant; **20.0× today** (12000 / 600) | reproduces at its instant; understated now |
| cap raise would force the ceiling past 40% of 32,000 | 13349 / 32000 = **41.7%** | **reproduces** |
| Σ `token_cap` = 5800, headroom 200; `BOOT.md` → 550 gives 5950 ≤ 6000 | 5800 confirmed; 5800 − 400 + 550 = **5950** | **reproduces**; the "declines to allocate in isolation" reasoning is arithmetically forced |
| bare-index register ≈ 454 TF-2 | my reconstruction over today's 45 row-leading ids in `\| <id> \| open \|` form = **414 / 455** | **reproduces in method and magnitude**; the exact figure is instant-dependent (41 ids then, 45 now) |
| removing the CMP-BLOCK-006 and OI-V-09 rows returns 6867/8673 → 6450/8149 | internally consistent (6867−199−218 = 6450; 8673−233−291 = 8149) | **arithmetic verified; inputs unrecoverable** — FIND-Q7-8 |

### 4e · The audit's own footprint on the measurement — disclosed

Registering this report's residual as `OI-V-10` enlarged the register again. Re-measured immediately after that write:

| | TF-1 | TF-2 | Governing | Limit |
|---|---|---|---|---|
| `project/OPEN_ITEMS.md` | 9428 → **10065** | 12000 → **12773** | 12773 | cap 600 — **FAIL**, 21.3× |
| `project/STATE.md` | 921 | 1083 | 1083 | cap 1100 — **PASS**; the `OI-V-02..09` → `..10` sync cost **0** tokens, headroom still 17 |
| **Capped T0 ∪ T1 aggregate** | 12868 → **13505** | 16012 → **16785** | 16785 | ceiling 6000 — **FAIL** |

The freeze registry is unaffected: `project/` is unhashed and unregistered, so all 29 DC-1s and the DC-2 aggregate are byte-identical before and after (re-verified: **29 of 29**, aggregate `3395815651…3053d30dc` unchanged, `STATE.frozen_set_hash` unchanged).

This is disclosed rather than avoided, for the same reason `APR-012` disclosed its own +3,327: **the governing aggregate has now risen 13,349 → 16,012 → 16,785 across two consecutive sessions, neither of which added a single unnecessary word.** An independent QA audit of the blocker cannot be filed without enlarging the blocker. That is the third data point for AMD-41 §4's thesis and I regard it as the strongest single piece of evidence in this report that the construction, not the content, is what has to change.

## 5 · Recomputed digest table — full 64 characters, dual-computed

Every value below was computed twice — once by my own scratchpad implementation of DC-1/DC-2 written from the manifest's normative text and importing nothing from `src/`, and once by `src/aief_stage6/digests.py`. **The two implementations agree on every value.**

### 5a · The 29 registered artifacts, in DC-2 hashing order (ascending by UTF-8 octets of `<path>`)

| # | Path | Recomputed DC-1 | vs `FROZEN.md` |
|---|---|---|---|
| 1 | `framework/AIEF-ADR-001_Authority_Decision_Record.md` | `935d169d0bbfd11c9d73c9f256de710d3b67477ebc1c458b6aa07c5e6a2362cb` | MATCH |
| 2 | `framework/AIEF-ADR-002_Authority_Decision_Record.md` | `e79e9fc8b0e0b9e07493d50c203084391802eb096ee2239693c229efdec696f3` | MATCH |
| 3 | `framework/AIEF-AMD-001_Architecture_Amendments_1.0.0.md` | `1d3c42d48f366a1be02c6fe3bd9281c356fd1063ec3c4c4b179efc9fb8744329` | MATCH |
| 4 | `framework/AIEF-AMD-002_Architecture_Amendments_CMP-BLOCK-014.md` | `83a69de9e6b9e0a6d2dc5f46614bcd0a8170882c4d0d900a9872442d9b382591` | MATCH |
| 5 | `framework/AIEF-AMD-003_Architecture_Amendments_OI-F-01_OI-F-02.md` | `d1d2cf76425974cc8b7804005d7e5a52f90ad8be16edfbd5480c03709fcc5e4b` | MATCH |
| 6 | `framework/AIEF-AMD-004_Repository_Engineer_Autonomy.md` | `9171059e930cca9365abd0c2bad5db01fa3a790733c6f663ef93cc79de255dac` | MATCH |
| 7 | `framework/AIEF-AMD-005_Host_Bootstrap_Artifacts.md` | `f8a4ab53eec480e951fe17cb6590b16fd311ce4e2639a83d2d8bab6fd05f946a` | MATCH |
| 8 | `framework/AIEF-AMD-006_Mechanical_CAD_Engineer.md` | `ece7c0c780ffd0c006f508ddcc624a416d1f11ff24d4addb3dc9be61c36f38e9` | MATCH |
| 9 | `framework/AIEF-AMD-007_Compiler_Stage_State_Field.md` | `860a1c7e8f18a05d032fe21cd2dfaeac4580765de1d225f9c260def8484caa9e` | MATCH |
| 10 | `framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md` | `192ff86128dadfc8382f1894e1a38713f7321ee83aff7891d7e885c31c9dd71e` | MATCH |
| 11 | `framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md` | `86c8be7f0eafb441c55ad5d5033f6e8e4e684350da262557539e6291b68f2c97` | MATCH |
| 12 | `framework/AIEF-AMD-010_Stage_6_Constructions_and_Preflight_Dispositions.md` | `486be10eb3bea89fb8c6c99949f1bb48e884cb556879e594cdd778dac5b0b829` | MATCH |
| 13 | `framework/AIEF-AMD-011_Software_Role_Enablement.md` | `59ecb5eb922f44a55cc42e51663dae9ee251269790958ee27ad93c1ba2ebaa53` | MATCH |
| 14 | `framework/AIEF-AMD-012_DC-4_Coverage_of_Enabled_Role_Artifacts.md` | `12b7f1b003fd190d99948e378a630d85e405e3c041da31eb8204bb00e702f1d0` | MATCH |
| 15 | `framework/AIEF-AMD-013_Boot_Budget_Determination_and_Stage_6_Build_Constructions.md` | `3d1e6b60c9e9c3ebda88cd073f0a717dc6506cc41388f0568eede8d0a6b99e78` | MATCH |
| 16 | `framework/AIEF-FRZ-001_Framework_Architecture_Freeze_1.0.0.md` | `a1b0a51c58138156a18598c2cb9bcb3a6066b0fcd35ea10203d5d17c450023f4` | MATCH |
| 17 | `framework/SCH-framework-manifest.schema.json` | `ee3d0bdf37156541c13ece46fec9172dabd93e98f32cb88c0ae7a2adff4bb25f` | MATCH |
| 18 | `framework/framework.manifest.json` | `8af8971b78d762e5db2879e50585a78f4e6d497ea707c664a9c06e1ba7e42ff7` | MATCH |
| 19 | `spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md` | `baf9ae50cd3d34a522b9998fc0f9420746ccf57c3b27f358ff0270024d9e2721` | MATCH |
| 20 | `spec/01_SEWCP-200_Cooling_Plate.md` | `3ae384bd82d3d32cedf22c02c58e09fa14a363c8003d05b52ae1f78c0e6a2597` | MATCH |
| 21 | `spec/02_SEWCP-300_Heater_Plate.md` | `ab36e082749fa4ea08c9f0f6a6c98cb481491cb601dc4c5cc947ba3634537608` | MATCH |
| 22 | `spec/03_SEWCP-400_Chuck_Support_Ring.md` | `b00d52899f36f0bfe6a05cc209ca40876ba5fa6fac9169e5d100bc5346a62655` | MATCH |
| 23 | `spec/04_SEWCP-500_Electrostatic_Chuck.md` | `4a8c39325a2edd0e03ba06b802afb5f7aaf9bb6c4552b22b3b72a67121afaca1` | MATCH |
| 24 | `spec/05_SEWCP-600_Lift_Pins.md` | `39a841104a2752d9d0dd7e309e599f7735ae74cb919739e5edb3975d8470873d` | MATCH |
| 25 | `spec/06_SEWCP-700_Alignment_Pins.md` | `0d2aa747fcca37574090ebff022f51924e66c7c845ecb9e2c0fea991155dcdc2` | MATCH |
| 26 | `spec/07_SEWCP-800_Vacuum_Port.md` | `1b7b5914202f4ec631f5fad9daf2e41d215e5d80e07a4e289482c85d6068989f` | MATCH |
| 27 | `spec/08_SEWCP-900_RF_Feedthrough_Bracket.md` | `cfe93cd6c4ef2e6b405909f252a6bd987726b65fdc4a725eb5d36ed453f166b9` | MATCH |
| 28 | `spec/09_SEWCP-1000_Temperature_Sensor_Bracket.md` | `391e5e6b403e17be30028d28875a2b291a100b7a05e7038645353e78b63764dd` | MATCH |
| 29 | `spec/README.md` | `95da15c691bac4ab61c3450efdc71428a5807fec1c3a32b81213f3490181370c` | MATCH |

**29 of 29 verify.**

### 5b · Aggregates and lineage

| Membership | Manifest row at | Recomputed DC-2 | Recorded at | Verdict |
|---|---|---|---|---|
| **29 (current)** | `8af8971b…a7e42ff7` | `339581565141702a2f5a79f531efa6c745b1af10bf2ccac4f6651af3053d30dc` | `FROZEN.md` § *Aggregate* **and** `STATE.frozen_set_hash` | **MATCH, both, all 64 chars** |
| 28 (superseded) | `f06125d2…69707638` | `a743cf6fcb9a69b841deaced59cc34fd6adc0a1f31c0c84cab24ab44b80a6a53` | `FROZEN.md` | **MATCH** |
| 27 (superseded) | `ae16ccac…9d8395aa` | `f605e92232a8bb50ba241dc6444df5a922c68b0008ded09d2e7134d85f2bd83d` | `FROZEN.md` | **MATCH** |
| 26 (superseded) | `ae16ccac…9d8395aa` | `80cd3ebe0ce971b079fe598bac401ab959f77c7c900a54caa6e0a09963fdf2e8` | `FROZEN.md` | **MATCH** |
| 25 (superseded) | `9611d547…9813e557` | `4a9e88d91fea4f7b52c2371cbc5438071625b7dd0074ad389f9f9f47b128fc22` | `FROZEN.md` | **MATCH** |
| 24 (superseded) | `636cf22b…14b38d3c` | `080771b0e26e365decebaa4118a27b4a46c73b7beeb3fb599009ce4ef6b6367a` | `FROZEN.md` | **MATCH** |
| pre-DC-2 | — | not attempted | `42bce7b0de019f854f99387edfc901b054b540f829bfe365e003be96892d5847` | correctly marked SUPERSEDED and not reproducible |

All five superseded values are **retained, not erased**, and — going beyond the established practice — every one of them **reproduces** from its reconstructed membership. The `VER-005` FIND-Q5-2 reconstruction note that names which manifest digest sits in each superseded set is present and correct.

### 5c · Approval bindings

| Approval | `subject_path` | `subject_hash` | On-disk DC-1 | `prior_hash` | Verdict |
|---|---|---|---|---|---|
| `APR-012` | `framework/framework.manifest.json` | `8af8971b78d762e5db2879e50585a78f4e6d497ea707c664a9c06e1ba7e42ff7` | identical | `f06125d2f9bd0860ab72c73f7dd11318d5d4f3169ded23b86f33e9c469707638` | **subject MATCH**; prior corroborated |
| `APR-013` | `framework/AIEF-AMD-013_…` | `3d1e6b60c9e9c3ebda88cd073f0a717dc6506cc41388f0568eede8d0a6b99e78` | identical | `null` (not previously registered) | **MATCH** |

**On `prior_hash`.** `git show HEAD:framework/framework.manifest.json` normalises to `ae16ccaca5746b81a2a992841fc1d239fd1c8b0c34657c05611e025a9d8395aa`, the AMD-010 digest — the pre-session-`-10` manifest is not a git object, because session `-06` did not commit. `APR-012.prior_hash` is nevertheless corroborated **two independent ways**: (i) it equals `APR-010.subject_hash` byte for byte, an artifact written four sessions earlier; and (ii) substituting it as the manifest row of the reconstructed 28-member registry reproduces `FROZEN.md`'s recorded 28-member aggregate `a743cf6f…` exactly — a value recorded before this session existed. A forged `prior_hash` would have to satisfy a SHA-256 preimage constraint recorded by a prior session. I regard the chain as intact.

### 5d · Constants

| Constant | Value | Source | Verdict |
|---|---|---|---|
| DC-1 of empty normalised content | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | AMD-48, manifest `per_artifact.empty_content` | reproduces under both implementations; equals DC-2 `empty_registry` — one treatment of emptiness, as claimed |
| TF-1 artifact pin | `223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7` | re-derived raw-octet | MATCH TOFU record |
| TF-2 artifact pin | `d60acb128cf7b7f2536e8f38a5b18a05535c9e14c7a355904270e15b0945ea86` | re-derived raw-octet | MATCH TOFU record |

## 6 · Content-preservation verdict — item by item

The binding instruction was: *do not silently delete, summarise, relocate or weaken authoritative content.*

### 6a · `project/OPEN_ITEMS.md` — the self-declared authoritative register

**VERDICT: NOTHING LOST.** Item-identifier set at `HEAD`: 37. Now: 44. **Removed: none.** Added: `CMP-BLOCK-006`, `OI-C-06`, `OI-C-07`, `OI-C-08`, `OI-C-09`, `OI-V-09`, `OQ-15` (the first, fourth, fifth and seventh by the audited session; the rest by sessions `-05`/`-06`/`-09b`). `OQ-13` moved from *Open, not blocking* to *Closed* with **more** content than it carried before, by session `-05`. The only in-place edits attributable to session `-10` are additive in substance: the `OQ-14` row gains *"or AIEF-AMD-013"*, and the `SOD-1` row gains the `-10` departure paragraph. AMD-041 §8's claim — *"`project/OPEN_ITEMS.md` is not reduced by a single recorded item"* — is **verified true**. (Blast Radius calls the edit *"additive only"*; the `OQ-14` in-place edit is a trivial exception in form, not in substance, and I do not raise it.)

### 6b · `project/STATE.md` — reduced 1747 → 1083 TF-2

Every removed fact, and where it survives:

| Removed from `STATE.md` | Survives at | Verified |
|---|---|---|
| `frozen_set_hash` `80cd3ebe…3fdf2e8` (superseded) | `FROZEN.md` § *Aggregate*, retained as the 26-member value — and it **reproduces** (§5b) | ✔ |
| Prior aggregates `4a9e88d9…b128fc22`, `080771b0…f6b6367a` | `FROZEN.md` § *Aggregate* — both retained and both reproduce | ✔ |
| Manifest re-registration digests `ae16ccac…9d8395aa`, `9611d547…9813e557` | `FROZEN.md` § *Registration history* rows, with their approvals | ✔ |
| Pre-DC-2 non-reproducible aggregate and the 32-character truncation note | `FROZEN.md` § *Superseded value — audit record only* | ✔ |
| Registry lineage 16 → 24 → 25 → 26 (approvals `APR-003`/`-005`/`-007`) | `FROZEN.md` § *Registration history*, all rows present, now continued to 29 | ✔ |
| *"`AIEF-ARCH-001` ruled out as superseded"* | `FROZEN.md` § *Not registered, by ruling* (AMD-21, APR-003) | ✔ |
| *"`V-24` declared, not implemented"* + *"no standing check binds this registry"* | Retained in condensed form **and** authoritative at `FROZEN.md` § *Standing verification* and `OI-V-02` | ✔ |
| *"DC-2 prohibits truncation; recorded at full 64 characters"* | `FROZEN.md` § *Aggregate* (*"Mirrored in full, never truncated"*) and the DC-2 construction itself | ✔ |
| *"Neither `S-2026-08-08-01` nor `-02` performed a LAW-09 close"* | Generalised to *"No LAW-09 close"* — a **stronger** statement; the `-01` specifics remain at `OI-P-01` | ✔ |
| *"DC-3 is now defined … the `genesis → active` transition is irreversible and was deliberately not made"* | `OPEN_ITEMS.md` Closed row `ECR-Q-002` (*"No ledger entry was written; `HEAD` remains at `genesis`"*) and `ledger/HEAD` § *Genesis semantics* (*"occurs once per repository and is irreversible"*) | ✔ |
| *"all three B4 checks pass"* | `ledger/HEAD` § *B4 verification*, all three enumerated; STATE retains *"check 1 vacuous at `genesis`"* | ✔ |
| *"Per `tpl-current-state`: Lifecycle stage, Active gate, …"* (the eight required-section list) | `core/templates/TPL-current-state.md` § *Required sections*; STATE now cites `tpl-current-state` by name and **all eight fields remain present in the YAML block** | ✔ |
| `compiler_stage.complete` inline comment *"Core, Templates, Project Layer, Adapters, Validation"* | `ENGINEERING.md` §6 and the manifest `generation_order` | ✔ |
| Old `next_action` prose (AMD-010 summary; VER-004 9/9; OQ-13 pending) | `OPEN_ITEMS.md` Closed rows `OQ-1…OQ-10, OQ-12` and `OQ-13`; `OI-V-08` for VER-004 | ✔ |
| Header *"Emitted by aief-compile Stage 3 from `framework.manifest.json` …"* and *"never touched by framework upgrade"* | Manifest `files[state]` (`generator: 3`, `partition: project`) and `.ai/FRAMEWORK.md` § *Partitions* (`project` … `never-touched`) | ✔ but see **FIND-Q7-7** |

**VERDICT: LOSSLESS.** No recorded fact was destroyed. Every relocated fact has a citable authoritative home, and in the case of the digests I did not merely check that a pointer exists — I recomputed the pointed-to values and they are correct. The reduction is what `tpl-current-state` acceptance condition 3 and its Forbidden clause require of the file's owner, and `chief-systems-engineer` is that owner. `SCH-state` requires eight fields; all eight are present and the schema imposes no further constraint. **`APR-012`'s claim "Nothing recorded was lost" is verified.**

`open_non_blocking` deserves separate note: at `HEAD` it omitted `OI-V-05`; the new range form `OI-V-02..09` covers it. The reduction made the list **more** complete, not less.

## 7 · Test suite

`python -m pytest tests/ -q` → **114 collected, 111 passed, 3 failed, 1.09 s.** I adjudicated each failure myself against the rulings and the tree:

| Failure | My finding | Defect? |
|---|---|---|
| `test_stage6_certification_evidence.py::TestV09Recomputation::test_three_breaching_files_confirmed` | Asserts `project/STATE.md` governing == 1791. The test's own recomputation yields **1083**, identical to mine. 1791 is a snapshot of a `mutability: mutable`, `lifecycle: instance-created` file taken at session `-08`, which AMD-42 `measurement_instant` declares is not a constant | **No.** Stale assertion |
| `…::test_totals_and_governing_family` | Asserts totals `{TF-1: 10296, TF-2: 12657}`. The test's own recomputation yields `{TF-1: 12868, TF-2: 16012}` — **identical to my independent measurement and to `APR-012`**. Same instant-vs-constant category | **No.** Stale assertion — and a **third-implementation corroboration** of my §4a totals |
| `test_stage6_coverage_and_build.py::test_v24_live_registry` | The check itself returns `status: PASS`; the assertion that follows pins `counts.registered == 28` and observes 29. V-24 is passing at the new membership, which is the registry behaving correctly | **No.** Stale assertion |

`OI-C-09`'s characterisation — *"114 tests, 111 pass, 3 fail, no implementation defect"* — is **independently confirmed**. Separately, I confirm the substantive delta `OI-C-09` owes is real and still open: `src/aief_stage6/budget.py` `measure()` still keys the deferral on `if not fs_path.is_file()` (verdict `DEFERRED-EMITTED-THIS-BUILD`) rather than on the path `core/MANIFEST.lock`, so the TCR-001 F1 fail-open is present in the tree exactly as recorded.

## 8 · Findings

| ID | Severity | Finding | Recommended disposition |
|---|---|---|---|
| **FIND-Q7-1** | **MINOR** | **The authoritative register asserts, as *"today"*, three live measurements that were already false when the session that wrote them closed.** `OPEN_ITEMS.md` CMP-BLOCK-006 records *"today `STATE.md` 1747, `OPEN_ITEMS.md` 8673, aggregate 13349 (TF-2) / 10889 (TF-1)"*. My measurement, and `APR-012`'s own close-of-session table written by the same session, give `STATE.md` **1083 — PASS, not a breach at all**, `OPEN_ITEMS.md` **12000**, aggregate **16012 / 12868**. The register therefore understates the live aggregate breach by **2,663 TF-2** and asserts a per-file breach that no longer exists, while the correct figures live only in `APR-012` — an artifact outside the freeze registry, outside the boot-read set, and not pointed to from the CMP-BLOCK-006 row. A cold session at boot step B7 reads the wrong numbers. This is not the AMD-42 `measurement_instant` drift defence: that defence covers records *of a stated instant*; this row claims the present tense | `project-manager`: at the next lawful register write, either restate the CMP-BLOCK-006 figures at their measured values with an explicit instant, or replace them with a pointer to `APR-012` § *The reduction performed* — the pattern `STATE.md` § *Budget* already uses. Do not re-measure into the register on a schedule; that is the defect AMD-41 identifies |
| **FIND-Q7-2** | **MINOR** | **AMD-48's stated ground for the empty-content ruling is factually false, and the false statement is now normative manifest text inside a freeze-registered instrument.** The ruling says appending an LF to nothing *"would make an empty file and a file holding one blank line produce the same digest, collapsing two distinct states into one"*. It does not: DC-1's own *remove trailing blank lines* step already collapses them, under **either** reading. I verified with both implementations — `DC-1(b"")` = `DC-1(b"\n")` = `DC-1(b"\n\n")` = `e3b0c442…7852b855`; under the rejected reading all three would equally be `sha256(b"\n")` = `01ba4719…`. The distinction the ruling claims to preserve does not exist. **The ruling's outcome is correct** and consistent with DC-2's `empty_registry`; only its justification is wrong. The text appears twice: `metadata.reproducible.digest_constructions.per_artifact.empty_content` and `AIEF-AMD-013` §AMD-48 | A4: correct the ground at the next amendment. No digest changes and no re-approval of any existing value is needed. The manifest edit is a LAW-01/LAW-10 change and should ride with the OQ-15 amendment rather than be taken alone |
| **FIND-Q7-3** | **MINOR** | **AMD-45 leaves up to 200 tokens of the measured domain outside the aggregate ceiling test, and the residual is not recorded — although the same ruling recorded its exact analogue.** `core/MANIFEST.lock` is a member of the AMD-42 measured set (`token_cap` 200) and its 200 is one of the eight caps summing to `AIEF-FRZ-001` §1.8's 5,800. AMD-45 rules that its row *"contributes nothing to the per-family totals"*, and `verdict_rule` then compares those totals to the 6,000 ceiling. A conforming build can therefore report an aggregate of 6,000 — PASS — while the true capped T0 ∪ T1 cost is up to **6,200**. This is the same shape as the under-coverage the session **did** record as `OI-C-08` (`project/ledger/HEAD`, cap-null, 504 tokens, read at B4), raised there with the words *"under-covers the real boot cost by exactly one file and over-covers nothing"* | A4: record it beside `OI-C-08`, or close it by one of — compare the totals to 5,800 whenever the lock row is `DEFERRED-SELF-MEASURED`; or add the post-serialisation lock count into the totals before the ceiling test. Either is a manifest change and should travel with OQ-15, since the arithmetic it touches is the same pool |
| **FIND-Q7-4** | **MINOR** | **`APR-012`'s change accounting contradicts itself.** Its enumeration table marks **nine** members *New* (rows 1, 3, 5, 6, 7, 8, 9, 11, 12) and four *Extended*, thirteen in total — which my structural diff confirms exactly. Its reconciling sentence then says *"Counted as nine changes … (seven new members plus the `V-09` extension and the accompanying `authority`/`status` housekeeping)"*: seven is wrong, and 7 + 1 + 2 = 10 ≠ 13 on any reading. `AIEF-AMD-013`'s header *"nine changes"* is correct if read as the nine new members. The LAW-10 binding is to `subject_hash`, which is correct, and the enumeration is complete, so **no approval is void** | None required for validity. Optional clarity correction to the parenthetical at the next approval touch; `APR-012` is not itself hash-bound by anything |
| **FIND-Q7-5** | **MINOR** | **The session edited a `project-manager`-owned register without recording the role in which it did so.** `files[open-items].owner_role` is `project-manager`, and `AIEF-AMD-013` §AMD-41 §3's own table names `project-manager` as the party who *"may lawfully change its bytes"*. The session — `chief-systems-engineer` — then made substantial edits to that file (CMP-BLOCK-006, OQ-15, OI-C-08, OI-C-09, the Closed row, the SOD-1 extension) and its Blast Radius records the edit with no role attribution. Rank-1 instruction authorises it and SOD-1's *"ruled and applied"* departure covers it in substance, but the established practice is explicit: `VER-006`'s filing note records that its register edits were *"applied by the filer, in `project-manager` role at rank-1 direction"*, and `VER-004`'s that FIND-Q4-3's STATE sync was applied *"in-role as `repository-engineer`"* | A4 / `project-manager`: record the role in which the register edit was made, in the established form, at the next touch of `AIEF-AMD-013`'s successor or of `OPEN_ITEMS.md`. No content change |
| **FIND-Q7-6** | **MINOR** | **`ENGINEERING.md` contradicts `ROSTER.md` and contradicts itself, and its §6 omits the governing blocker.** (i) §7 states *"`OI-P-01…02` (session records absent; roster roles UNASSIGNED — now including the three software roles)"* and the `OQ-13` Closed row in `OPEN_ITEMS.md` states *"roster rows added UNASSIGNED"*, while `ROSTER.md` § *Profile `software`* assigns **all three** to a named identity with workstreams, and `ENGINEERING.md` §8 says *"roles assigned in `ROSTER` at rank-1"*. §7 and §8 of the same index cannot both be right. (ii) §6's Stage 6 row still reads *"blocked by CMP-BLOCK-004 and awaiting explicit human authorization"*, omitting **CMP-BLOCK-006**, which the same file's §8 makes gate 1 of four. The audited session edited §1, §5, §7 and §8 and left §6 | `project-manager` / `documentation-engineer`: sync §6's Stage 6 row with §8's gate list, and reconcile §7 and the `OQ-13` Closed row against `ROSTER.md`. `ENGINEERING.md` is an index and carries no authority, so nothing is voided; but `OI-P-02`'s premise (*"roster record is stale"*) now cuts the other way for the software rows |
| **FIND-Q7-7** | **INFO** | **`project/STATE.md` no longer carries the emitted instance-artifact provenance header its five siblings carry.** `BINDING.md`, `FROZEN.md`, `OPEN_ITEMS.md`, `ROSTER.md` and `ledger/HEAD` all open with *"**Instance artifact.** Emitted by aief-compile Stage 3 from `framework.manifest.json` and live repository state. / Partition `project` — never touched by framework upgrade. Owner … Mutability …"*. The reduction replaced it with a one-line form that keeps partition, owner and mutability but drops the generator and the upgrade semantics. **Both dropped facts survive** (`files[state].generator: 3`; `.ai/FRAMEWORK.md` § *Partitions*), so this is not a loss — but it is a divergence from the Stage 3 emission form that a future Stage 3 re-emission would silently revert, taking ~15 tokens of the file's 17-token headroom with it | None now. Flag to A4 as an input to OQ-15: if the remedy involves re-emitting or re-templating the project registers, the header form is part of the token arithmetic |
| **FIND-Q7-8** | **INFO** | **Auditability boundary: the pre-session baseline is unrecoverable, so three of AMD-41's numbers cannot be reproduced by anyone, ever.** `HEAD` is `8546960` — session `-04`'s commit. Sessions `-05` … `-09b` committed nothing, so `git show HEAD:` gives a five-session-old baseline for the four mutable tracked registers and the manifest. The session-start counts `project/STATE.md` 1503/1747 and `project/OPEN_ITEMS.md` 6867/8673, and the two-row removal arithmetic (6867 → 6450, 8673 → 8149, the rows costing 199/233 and 218/291), rest on tree states that no longer exist in the repository or in git. They are internally consistent — I verified the arithmetic closes — and the method reproduces on today's tree, but the inputs are gone. This is the commit-granularity consequence already recorded at `OI-V-04`, not a defect of the audited session | `repository-engineer`, with the human owner: commit before the next multi-session phase, per the `S-2026-08-08-03` commit-granularity ruling that made every approval subject a recoverable git object. The same ruling's benefit was not extended to sessions `-05` … `-10` |

## 9 · Overall verdict

> ## **VERIFIED WITH FINDINGS**
>
> **10 criteria — 7 PASS, 3 PARTIAL, 0 FAIL. 8 findings — 6 MINOR, 2 INFO, 0 MAJOR, 0 BLOCKING. Nothing found voids any digest, any approval, any registry value or any ruling.**

Every hash-bound claim the session made is true: both approval subjects match their files on disk to the octet, the freeze registry verifies 29 of 29, the DC-2 aggregate and its mirror in `STATE.md` are correct, all five superseded aggregates reproduce, the amended manifest passes its unmodified frozen schema with zero errors and satisfies MI-1, MI-3 strict and MI-4, and the enumerated change set is exactly what the approval authorises with nothing riding along. The determination at the heart of the session — that `BOOT.md`'s 400-token cap is unachievable against its own frozen render floor of 475, and that `project/OPEN_ITEMS.md` cannot be brought to 600 without destroying authoritative content — **reproduces to the digit under my own tokenizers**, and I independently reach the same conclusion: `CMP-BLOCK-006` cannot be closed by content reduction, and a cap raise alone is barred by MI-4 and by `AIEF-FRZ-001` §1.8's derivation, which I read in the frozen text. The content-preservation instruction was honoured: **not one recorded item or digest was lost** from either register, and the `STATE.md` reduction is lossless against a fact-by-fact trace.

The findings divide into three classes. Two are wrong statements in normative or authoritative text whose operative rules are nonetheless correct (FIND-Q7-2, FIND-Q7-4). One is a real construction gap the session should have recorded and did not, given that it recorded its exact twin (FIND-Q7-3). The rest are register hygiene and index drift (FIND-Q7-1, FIND-Q7-5, FIND-Q7-6) and disclosure of limits (FIND-Q7-7, FIND-Q7-8). None of them changes a gate, a verdict or a digest.

The two PARTIALs are honest and should not be read as PASS. C1 is PARTIAL because the authoritative register carries live figures that are false in the present tense, not because any measurement was wrong. C6 and C10 are PARTIAL because a normative justification is false and a construction residual went unrecorded, not because any construction is non-deterministic.

## 10 · What is still wrong, unresolved or reserved — and whether I agree

**Reservations. I agree with all three, and they are the correct disposals, not evasions.**

- **`OQ-15` — the CMP-BLOCK-006 remedy, and the resulting cap values.** The determination that an architecture amendment is required *was* made, and both pure strategies *were* ruled out, so this is not a case of a determination dressed as a choice. What remains genuinely trades a user-facing portability claim against boot-load architecture. I verified the arithmetic that forces the reservation: Σ `token_cap` = 5,800 against MI-4's 6,000, so **exactly 200 tokens of cap headroom exist in total**; raising `BOOT.md` alone to 550 consumes 150 of them (Σ = 5,950, still lawful), while option (a)'s bounded index already measures 455 TF-2 against a 600 cap on today's register and would need most of what is left. The options are not independent; allocating any of them in isolation prejudges the rest. **Reserving was correct.**
- **`OI-C-08` — no cap on `project/ledger/HEAD`.** I confirm the exposure: `boot_sequence[B4].files` names `ledger-head`, the file measures **411 / 504** today, and it is outside the measured set. Curing it draws on the same 200-token pool. **Reserving with OQ-15 was correct**, and naming it in the manifest so the gap is self-announcing is the right form.
- **`OI-C-09` — the `src/aief_stage6/**` delta.** A4 declining to write the code implementing its own ruling is the SOD-1 boundary being honoured rather than departed from. I confirm the delta is real and still open in the tree (§7). **Correct.**

**Still wrong or unresolved after this audit** — beyond my eight findings:

1. **`CMP-BLOCK-006` is worse than the register says and is growing monotonically.** The governing aggregate moved **13,349 → 16,012 TF-2 inside the audited session** and **16,012 → 16,785** on the filing of this report's own residual row (§4e) — up 26% across two sessions, neither of which added an unnecessary word, because disposing or auditing the blocker means recording the disposition or the audit. `project/OPEN_ITEMS.md` is now at **21.3×** its cap, not the 14.5× the register states. `project/STATE.md` sits at 1,083 against 1,100 with **17 tokens** of headroom that the next session's write will consume. This is exactly AMD-41's thesis with two further data points, and it argues for treating OQ-15 as time-critical rather than merely open.
2. **`V-24` remains hand-verified only** (`OI-V-02`). This audit is the standing check for one instant. Nothing binds `FROZEN.md` to the tree between audits.
3. **`OI-V-07` deepens.** `validation[V-09].verifies` was extended again; `core/validation/CHECKS.md` and `MANIFEST` were already stale in that field from AMD-010 and are now staler. The session recorded this correctly and did not hand-edit `core`, which is right.
4. **`OI-C-07` is unchanged and now bears on this audit's own subject**: `core/agents/INDEX.md` still lacks the three `software.*` rows, so the provenance tokens in `TCR-001`, `OI-C-09` and `ROSTER.md` do not resolve in the INDEX under a strict V-22 reading.
5. **`FIND-Q4-1` (tokenizer pin, trust-on-first-use) is still open and now has a second corroboration.** I re-derived both pins raw-octet from the artifacts in hand and they MATCH the TOFU record, which itself records upstream corroboration. The pin still does not become authoritative until the first Stage 6 build writes it into `MANIFEST.lock` under human approval.
6. **`SOD-1`'s mitigating control for session `-06` (AMD-012) is still open.** `VER-005` covers `-05`, `VER-006` covers the `-06`…`-09` preparation phase including AMD-012's C8, and this report covers `-10`. Whether `VER-006` C8 discharges the `-06` control is a judgement for A4, not for me; I note it is not recorded as discharged.
7. **`OI-P-01`/`OI-P-02` are untouched.** `project/sessions/` is still empty, no `.session.lock` has ever existed (DEV-02), and `ROSTER.md` still marks `qa-engineer` — my own role — UNASSIGNED while stating that an UNASSIGNED role cannot be dispatched. My dispatch is rank-1 and outranks the roster, as the register already records; but reviewer independence for this report cannot be checked against a recorded identity, only against the (role, session) pair.

**Gate status after this audit, in the dependency order `ENGINEERING.md` §8 and `STATE.next_action` declare:** gate 3 (independent cold-context QA audit of `S-2026-08-08-10`, including recomputation of the §AMD-41 measurement) is **discharged by this report**. Gates 1 (`OQ-15` → `CMP-BLOCK-006`), 2 (`OI-C-09`) and 4 (`OQ-14`) remain open. **Compiler Stage 6 is not authorized and no conforming `core/MANIFEST.lock` can lawfully exist.**

---

**END OF VER-007**
