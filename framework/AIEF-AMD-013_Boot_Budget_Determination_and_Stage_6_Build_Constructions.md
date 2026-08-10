# AIEF-AMD-013 — Architecture Amendment: Boot-Budget Determination and Stage 6 Build Constructions

**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-02 (disposition of a recorded blocker and of recorded open questions), LAW-01 + LAW-10 (change to a frozen artifact — `framework/framework.manifest.json`), LAW-12 (open decision with recorded rationale, never assumption; and reservation where the choice is not a determination)
**Scope:** (i) the determination of **CMP-BLOCK-006**, the V-09 token-budget breach that halts the first authoritative Stage 6 build; (ii) the five build open questions **OQ-B1 … OQ-B5** recorded in `project/STAGE-6_BUILD_OPEN_QUESTIONS.md`; (iii) the three lower-order items recorded at the foot of that file. **Nothing else.** No Stage 6 execution, no `core/MANIFEST.lock`, no distributable, no ledger write, no BINDING change, no tag, no commit.
**Date:** 2026-08-08 · **Session:** `S-2026-08-08-10`
**Amends:** `framework/framework.manifest.json` — nine changes, all inside `metadata.reproducible` and one `validation[V-09].verifies` extension, enumerated in `APR-012`
**Does not amend:** `AIEF-FRZ-001` (no byte, no digest, and — expressly — **no supersession in reading**: §1.8's derivation, its cap table and its 6,000 ceiling stand exactly as frozen) · `AIEF-AMD-001` … `AIEF-AMD-012` · either ADR · `SCH-framework-manifest.schema.json` (the amended manifest passes it unmodified) · `SCH-core-manifest.schema.json` or any emitted schema · any law rule or clause · any role contract · any partition, layer, tier, boot step, compiler stage or lifecycle definition · DC-1's normalisation of non-empty content, DC-2, DC-3, DC-4's coverage, grammar, order, preimage, self-exclusion, B2a procedure and worked example, DC-5 · TF-1 and TF-2 · **no `token_cap`, and not the 6,000 boot ceiling**
**Authorising basis:** live human-owner instruction of session `S-2026-08-08-10` (`core/PRECEDENCE.md` rank 1), directing that CMP-BLOCK-006 and OQ-B1…B5 be resolved according to the repository's authoritative records, that A4 independently inspect the V-09 failure and determine whether deterministic content reduction suffices or the frozen budget requires an architecture amendment, that no authoritative content be deleted, summarised, relocated or weakened, and that no assumption stand where the repository records an unresolved question. Recorded per LAW-10 in `project/approvals/APR-012` and `project/approvals/APR-013`

---

## Independence declaration

OQ-B1…OQ-B5 and the three lower-order items were raised by `software.software-engineer · S-2026-08-08-07` during the CMP-BLOCK-004 build and filed by `project-manager` action at rank-1 direction; the filing states expressly that **none may be ruled by the session that raised them**. CMP-BLOCK-006 was registered by `project-manager` action at the filing of VER-006, on the finding of `qa-engineer · S-2026-08-08-09b`, over evidence produced by `software.platform-engineer · S-2026-08-08-08` and certified by `software.test-engineer · S-2026-08-08-09`.

These rulings are made by `chief-systems-engineer · S-2026-08-08-10`, a cold session holding no state from any prior session and having authored none of the artifacts named above. Under AIEF-AMD-008 §AMD-20, agent identity for LAW-02, LAW-04 and LAW-05 independence is the pair (role, session): this session differs from `S-2026-08-08-07` **in both role and session**, and from every other contributing actor in at least session. The identity bar of the raising artifact is therefore satisfied, and it is confirmed here in writing as that artifact requires.

The same-authority ruled-and-applied departure is separately recorded in § *Separation of Duties*.

| Ruling | Subject | Change class |
|---|---|---|
| AMD-41 | CMP-BLOCK-006 — determination; content reduction insufficient; the remedy reserved to the human owner as **OQ-15** | Determination + reservation. **No manifest change** |
| AMD-42 | V-09's measured domain, the totals scope, and the measurement instant | Manifest change — two new `budget_measurement_record` members; `validation[V-09].verifies` extension |
| AMD-43 | OQ-B1 — lock JSON layout | Manifest change — `core_aggregate.lock_json_layout` |
| AMD-44 | OQ-B2 — `build_provenance` content | Manifest change — `metadata.reproducible.build_provenance_record` |
| AMD-45 | OQ-B3 — the lock self-measurement fixed point | Manifest change — `budget_measurement_record.lock_self_measurement` |
| AMD-46 | OQ-B4 — archive entry types and the directory-mode tension | Manifest change — `distributable.entry_types` |
| AMD-47 | OQ-B5 — the BINDING pin-line write form | Manifest change — `metadata.reproducible.binding_pin_write` |
| AMD-48 | DC-1 of empty content; AMD-33 run-fixed timestamp and build id | Manifest change — `per_artifact.empty_content`; `build_time_reproducibility.run_fixed_values` |

---

## AMD-41 — CMP-BLOCK-006: Determination, and the Remedy Reserved

**Disposes:** the *determination* required of A4 by CMP-BLOCK-006 (`project/OPEN_ITEMS.md`, Blocking) and by VER-006 §6a gate 1 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-10` · **No manifest change**

### 1 · Independent re-measurement

The recorded breach was re-measured this session from the repository's own implemented families — `src/aief_stage6/tokenizers.py`, TF-1 `cl100k_base.tiktoken` and TF-2 `spiece.model`, assembled offline from the artifacts in `build/stage6/tokenizer_artifacts/`, artifact pins recomputed raw-octet and matching the trust-on-first-use record. Both pins reproduce: TF-1 `223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7`, TF-2 `d60acb128cf7b7f2536e8f38a5b18a05535c9e14c7a355904270e15b0945ea86`. The full AMD-31 precondition run was executed with output redirected outside the repository; it reproduces V-01…V-08 and V-23…V-25 PASS and V-09 FAIL.

**Measured, this session, over the whole T0 ∪ T1 set** — capped and cap-null, present and absent:

| `files[]` path | Tier | Cap | TF-1 | TF-2 | Governing | Verdict |
|---|---|---|---|---|---|---|
| `BOOT.md` | T0 | 400 | 445 | **504** | 504 | **FAIL** |
| `FRAMEWORK.md` | T1 | 1100 | 652 | 748 | 748 | PASS |
| `core/MANIFEST.lock` | T1 | 200 | — | — | — | not on disk — emitted by Stage 6 |
| `core/PRECEDENCE.md` | T1 | 700 | 341 | 382 | 382 | PASS |
| `core/laws/INDEX.md` | T1 | 900 | 598 | 721 | 721 | PASS |
| `project/BINDING.md` | T1 | 800 | 483 | 574 | 574 | PASS |
| `project/STATE.md` | T1 | 1100 | 1503 | **1747** | 1747 | **FAIL** |
| `project/OPEN_ITEMS.md` | T1 | 600 | 6867 | **8673** | 8673 | **FAIL** |
| `core/workflows/WF-01_session.md` | T1 | null | 359 | 437 | 437 | not measured — cap-null |
| `project/ledger/HEAD` | T1 | null | 411 | 504 | 504 | not measured — cap-null |
| `adapters/INDEX.md` | T1 | null | 539 | 672 | 672 | not measured — cap-null |
| `core/profiles/mechanical/PROFILE.md` | T1 | null | 414 | 527 | 527 | not measured — cap-null |
| `core/profiles/mechanical/lifecycle/INDEX.md` | T1 | null | 398 | 530 | 530 | not measured — cap-null |
| `core/profiles/software/PROFILE.md` · `.../lifecycle/INDEX.md` · both `research` entries | T1 | null | — | — | — | not on disk — deliberately unemitted, AMD-011 §AMD-36 |
| **Measured totals** (capped set, per AMD-42) | | ceiling 6000 | **10889** | **13349** | **13349** | **FAIL** |

### 2 · The recorded values do not reproduce — a finding of the first order

`OPEN_ITEMS.md` records the breach as `BOOT.md` 504, `STATE.md` **1791**, `OPEN_ITEMS.md` **7937**, aggregate **12657** (TF-2) / **10296** (TF-1); TCR-001 §3.2 and VER-006 C4 independently confirmed those figures to the digit, and this session confirms that they agreed with each other and with the platform engineer's diagnostic exactly.

**Five of the eight measured values still reproduce to the digit** — `BOOT.md` 445/504, `FRAMEWORK.md` 652/748, `core/PRECEDENCE.md` 341/382, `core/laws/INDEX.md` 598/721, `project/BINDING.md` 483/574. **Three do not:** `project/STATE.md` 1516/1791 → 1503/1747; `project/OPEN_ITEMS.md` 6261/7937 → 6867/8673; totals 10296/12657 → 10889/13349.

Nothing in the compiler, the tokenizers, the pinned artifacts or the manifest's measurement rules changed between the two measurements. What changed is the content of two `partition: project`, `mutability: mutable`, `lifecycle: instance-created` files, written after the measurement by the sessions that recorded the measurement's own result. The largest single contributor is demonstrable: removing the `CMP-BLOCK-006` row and the `OI-V-09` row — the two rows VER-006's FIND-Q6-1 disposition added — returns `OPEN_ITEMS.md` from 6867/8673 to 6450/8149, the two rows costing 199/233 and 218/291 respectively.

> **The act of recording the budget breach in the authoritative register made the budget breach larger.** That is not a defect of any actor. It is a property of the construction: V-09 is a build gate whose measured domain includes registers that grow when the gate fails.

Both prior measurements were honest and correct at their instant. The disagreement is not a defect in TCR-001 or VER-006; it is evidence about the construction, and it is declared as a recorded property by AMD-42 (`measurement_instant`) so that no future re-measurement mistakes drift for tampering.

### 3 · The membership of the measured set, and who may lawfully change what

The T0 ∪ T1 set has **seventeen** `files[]` members; **eight** carry a non-null `token_cap` and are the measured set (AMD-42); nine are cap-null and are not measured; four of those nine are not on disk by ruling. The measured set partitions by write access, and this is decisive:

| Measured file | Partition | Write access | Mutability | Who may lawfully change its bytes |
|---|---|---|---|---|
| `BOOT.md` | `root` | **framework-only** | immutable | The compiler, by Stage 1 re-emission — **not this session, not any agent, not by hand** |
| `FRAMEWORK.md` | `root` | **framework-only** | immutable | as above |
| `core/PRECEDENCE.md`, `core/laws/INDEX.md` | `core` | **framework-only** | immutable | as above |
| `core/MANIFEST.lock` | `core` | **framework-only** | immutable | Stage 6 only |
| `project/BINDING.md` | `project` | agents-and-humans | mutable | `project-manager` |
| `project/STATE.md` | `project` | agents-and-humans | mutable | `chief-systems-engineer` |
| `project/OPEN_ITEMS.md` | `project` | agents-and-humans | mutable | `project-manager` |

### 4 · The determination

> **Deterministic content reduction is not sufficient, and cannot be made sufficient by any actor available today. CMP-BLOCK-006 requires an amendment to the frozen budget construction. The breach is two distinct defects reported by one check, and they have different cures.**

**Defect class A — a compiler-output cap the compiler's own output cannot meet.** `BOOT.md` governing 504 > cap 400. `BOOT.md` is `framework-only` write access and `mutability: immutable`; no agent may hand-edit it, and changing it is a Stage 1 re-emission, which is CMP-BLOCK-004 — the full compiler that does not exist. A disposition of the form *"reduce `BOOT.md`"* therefore makes Stage 6 unreachable until the whole six-stage compiler is built, which directly contradicts AMD-25's ruling that a Stage-6-only increment is admissible for Stage 6. That reading is not available.

Nor is the cap reachable by rendering. `BOOT.md`'s content is a Stage 1 render of the eleven frozen `boot_sequence` steps plus the frozen tier rule and governing rule. Measured this session under the governing family: the eleven-row boot table alone is **346** TF-2; the tier rule is **47**; the governing rule is **82** — a floor of **475 > 400** for a document that renders only what the frozen architecture declares. Deleting the `Cost` column, which MI-11 requires every boot step to declare, still leaves **436 > 400**. **The 400 cap is unachievable against `BOOT.md`'s own frozen specification.** That is precisely the ground on which `AIEF-FRZ-001` §1.8 itself superseded the Rev A ceiling of 3,900 — *"it was asserted without derivation and was unachievable against its own file specifications."* The defect is in the cap, not in the file. Its cure is a cap amendment.

**Defect class B — a fixed cap on live, monotonically growing project state.** `project/STATE.md` 1747 > 1100 and `project/OPEN_ITEMS.md` 8673 > 600; together they contribute **10,420** of the 13,349 governing total. These are `mutability: mutable`, `lifecycle: instance-created`, `integrity: unhashed` files: the compiler emits their initial instance and every session thereafter writes them under LAW-09, which makes a session *"a transaction [that] reads state at start and writes state at close."* Two consequences follow directly:

1. **The cap is not a constraint the build can satisfy.** DC-4 refuses to cover these files — *"unhashed partitions (project, adapters) are never covered"* — and `FROZEN.md` refuses to register them — *"`project/`, `adapters/` — nothing; mutable by design."* The build would be halted on the state of files that no integrity mechanism of the build binds, and that the build cannot change.
2. **`project/OPEN_ITEMS.md` is authoritative** — *"This register is authoritative; `STATE.md` is a derived cache and `ENGINEERING.md` is an index."* It stands at 8,673 governing tokens against a 600 cap: a factor of **14.5**. Measured this session, a hypothetical register reduced to nothing but its forty-one identifiers and the single word `open` per row already costs **454** TF-2 — 76% of the cap, carrying no item text, no blocking status and no authority, and admitting perhaps a dozen more entries before the bare index itself breaches. Any reduction that brings the real register under 600 destroys or relocates the recorded blockers, findings, dispositions and residuals. Under the directing instruction and under LAW-06, that is a defect, not a fix.

> **A fixed 600-token cap on an authoritative register that grows monotonically with the project's engineering history is itself an architecture defect.** It is not a cap the register can be held to, because the register's size is a function of how much has been recorded, and recording is the register's purpose.

**Content reduction, applied where it is lawful and lossless, does not close the gap.** `project/STATE.md` is the one measured file this session both owns (`owner_role: chief-systems-engineer`) and may reduce without loss, because the file declares itself *"a derived cache."* That reduction was performed and is recorded in § *Content Reduction Performed* below. Even with `STATE.md` inside its cap, the aggregate remains far above 6,000 and `BOOT.md` and `OPEN_ITEMS.md` remain in breach. **This is the demonstration, not the remedy.**

### 5 · What is *not* determined, and why

The determination above fixes that an amendment is required and rules out the two pure strategies:

| Strategy | Judgement |
|---|---|
| Content reduction alone | **Ruled out, determinately.** `BOOT.md` cannot be reduced by any available actor and cannot meet 400 by any conforming render; `OPEN_ITEMS.md` cannot be reduced to 600 without destroying authoritative content |
| Cap and ceiling raise alone | **Ruled out, determinately.** Caps sufficient for the measured values would sum past 13,000, breaching **MI-4** (Σ `token_cap` over T0 ∪ T1 ≤ 6,000) and forcing the ceiling past 40% of the 32,000-token portability floor, destroying the `AIEF-FRZ-001` §1.8 derivation (32,000 × 20%). And because `OPEN_ITEMS.md` grows monotonically, any cap set this way is re-breached by the next session — a cap that must be amended at every session close is not a cap |

What remains is a genuine choice among lawful architecture alternatives with real trade-offs. It is **not** a determination, and under LAW-12 this authority does not make it. Following exactly the precedent of AIEF-AMD-010 §AMD-34, which recorded the OQ-13 options and reserved the choice, the options are recorded and the choice is **reserved to the human owner as OQ-15**.

### 6 · The admissible options — recorded for the owner

The MI-4 arithmetic that binds every option: Σ `token_cap` over T0 ∪ T1 is **5,800** today against a limit of **6,000**, so **200 tokens of cap headroom exist in total** and every raise draws on the same pool.

| Option | Mechanism | Properties |
|---|---|---|
| **(a) Split the authoritative register: bounded T1 index, unbounded body** | Add a `files[]` entry for the full register (e.g. `project/OPEN_ITEMS_REGISTER.md`, tier T4, cap null, partition `project`, generator 3); `project/OPEN_ITEMS.md` becomes a bounded index carrying every identifier, its class and status, and a pointer. Boot step B7 is unchanged — it still reads `project/OPEN_ITEMS.md`. Manifest change; a Stage 3 emission question for the new artifact | **Preserves every authoritative byte** at a declared home, with a 1:1 mapping. It is what the tier architecture is *for* — *"Loading everything is the default failure. Tiers bound the cost of becoming oriented."* Cost: the register is no longer wholly loaded at boot, so a booting session sees the index and must load the body on cause; and the bare index measured at 454 today still leaves only ~150 tokens of growth against the 600 cap, so the index's own cap likely needs raising too (drawing on the 200-token pool) or its row grammar constraining |
| **(b) Re-derive the budget from a current portability floor** | Amend `version.min_context_window` upward from 32,000, re-derive the 6,000 ceiling at the frozen 20% share, and redistribute all eight caps. Manifest change; `AIEF-FRZ-001` §1.8's derivation table superseded in reading, bytes unchanged | Honest and simple, and it is the only option that also cures `BOOT.md` without a re-render. Cost: it raises the declared **portability floor** — the framework then refuses to claim support for a 32,000-token host — which is a product decision, not an engineering one; and it does not stop `OPEN_ITEMS.md` growing past whatever new cap is set |
| **(c) Narrow V-09's build-time domain to the compiler's own output** | Rule that the V-09 *precondition* measures the integrity-hashed, framework-emitted T0 ∪ T1 files (the build's own product), and that the `project`-partition tier caps are enforced at **session close** under LAW-09 tier discipline instead of at build time. Manifest change; a new or extended check | Aligns the build gate with what the build controls and with DC-4's own coverage rule, and makes the measurement reproducible from the build's declared inputs. Cost: **it does not fix the live overrun** — `OPEN_ITEMS.md` at 8,673 tokens genuinely does blow a 6,000-token boot ceiling on a 32,000-token host today — so taken alone it moves the failure out of the build's view without curing it. Admissible only in combination with (a) or (b) |
| **(d) Combination** | Any consistent combination of the above, with `BOOT.md`'s cap raised to at least its measured governing value | The only combinations that close both defect classes are {(a) or (b)} + a `BOOT.md` cap cure; (c) may be added to either |

**`BOOT.md`'s cap, separately.** Raising it alone from 400 to 550 would give Σ = 5,950 ≤ 6,000 and satisfy MI-4 today. This authority declines to rule it in isolation: that raise consumes three quarters of the entire cap headroom, and the headroom is the same pool option (a) needs for the index cap and option (b) redistributes wholesale. Allocating it before the register question is decided would prejudice the owner's choice. The *determination* — that 400 is unachievable and a cap amendment is the cure — stands; the *value* travels with OQ-15.

### 7 · A4 recommendation — recommendation, not decision

**Option (a), combined with a `BOOT.md` cap raise and, if the owner wishes, (c).** Grounds, in order:

1. It is the only option that both preserves every authoritative byte and holds the boot ceiling at its frozen, derived value. Neither the ceiling nor the register's authority has to give way.
2. It uses a mechanism the architecture already declares and already relies on. Tiering the register is the same move the framework makes for the ledger — `HEAD` gives O(1) lookup at B4 and *"body never read at boot"*, with sealed segments T4-only (OD-9). The register is the one authoritative artifact for which that pattern was never applied.
3. It is self-correcting under growth in a way (b) is not: the index grammar bounds per-entry cost, so the register may grow without end while the boot cost stays flat. (b) buys a fixed amount of room once.
4. It does not touch the portability floor, which is a claim to users rather than an internal parameter.

Option (b) is entirely lawful and is the simplest thing that could work; it is ranked below (a) only because it trades a user-facing claim for internal room and does not bound future growth. Option (c) alone is recommended **against**, for the reason stated in the table: it would make the build stop reporting a real operational overrun without curing it, which is the FM-3 pattern `AIEF-FRZ-001` §1.7 exists to prevent.

> **Recorded explicitly: the CHOICE among (a), (b), (c) and their combinations, and the resulting cap values, is the human owner's** (`project/BINDING.md` `approval_authority: human-owner`; every cap and ceiling is frozen architecture, and §1.8's derivation is a ratified product parameter). **OQ-15 is open** until the owner decides. **CMP-BLOCK-006 remains BLOCKING**: until it is disposed, the AMD-31 gate fails, and no conforming `core/MANIFEST.lock` can lawfully exist.

### 8 · What this ruling deliberately does not do

- It does **not** delete, summarise, relocate or weaken any authoritative content. `project/OPEN_ITEMS.md` is not reduced by a single recorded item; every entry it carried before this session it carries after, and this session adds to it.
- It does **not** change any `token_cap` or the 6,000 ceiling, and it supersedes no phrase of `AIEF-FRZ-001` in reading. §1.8 stands as frozen.
- It does **not** narrow V-09's measured set. AMD-42 declares the reading already in force and closes a recorded ambiguity; it excludes nothing that was previously included.
- It does **not** authorise Stage 6, create `core/MANIFEST.lock`, or touch `project/BINDING.md`.

---

## AMD-42 — V-09's Measured Domain, Totals Scope and Measurement Instant

**Disposes:** the recorded lower-order item *"budget totals scope read as capped T0∪T1 files only (cap-null T1 files excluded) — confirm intent"* · **Ruled by:** `chief-systems-engineer · S-2026-08-08-10`

### Question, restated

`budget_measurement_record.content` clause 1 names *"every file carrying a non-null `token_cap` in tiers T0 and T1"*; clause 2 names *"per-family T0 plus T1 totals"* without repeating the qualifier. The implementation reads clause 2 as the total over clause 1's set and disclosed the reading as an open question. Nine T0 ∪ T1 entries carry `token_cap: null`; five of them exist on disk and measure 2,670 TF-2 in total, so the reading is not academic.

### Ruling

> **The measured set is exactly the `files[]` entries whose tier is T0 or T1 and whose `token_cap` is non-null. The per-family totals of clause 2 are the totals over exactly that set. Cap-null tier entries are outside the record. The interim reading is confirmed.**

Grounds, each evaluable from declared text:

1. **It is MI-4's own domain.** MI-4 is *"Σ `token_cap` over T0 ∪ T1 ≤ 6,000"* — a sum over exactly the entries that declare a cap. The measurement side of a budget and the declaration side of the same budget must range over the same set, or the invariant that makes the budget *"close by construction"* is checking a different thing from the check.
2. **It is `AIEF-FRZ-001` §1.8's own arithmetic.** The frozen derivation table lists eight files, sums them to **5,800**, and records **200** of headroom against the 6,000 ceiling. That Sum row is computed over exactly the capped set. Reading the aggregate over all T0 ∪ T1 would make the frozen table's own headroom figure false the moment any cap-null tier file exists — and nine do.
3. **A cap-null entry declares no bound.** There is nothing for a verdict to compare against, and `verdict_rule` speaks only of *"any per-file cap breach or aggregate ceiling breach"*. Admitting unmeasurable files into an aggregate that is compared to a ceiling derived from the sum of caps would compare two different quantities.

### Recorded residual — expressly not closed

Boot demonstrably reads a cap-null file. `boot_sequence[B4].files` names `ledger-head`, and `project/ledger/HEAD` carries `tier: T1`, `token_cap: null`, and measures **411 / 504** today. The boot-loaded set is therefore the eight measured files **plus** `project/ledger/HEAD`; the remaining eight T1 entries are read at no boot step at all. So the measured set under-covers the real boot cost by exactly one file, and over-covers nothing.

This is a genuine exposure and it is **not** cured here: assigning `ledger-head` a cap draws on the same 200-token MI-4 headroom that AMD-41 §6 reserves to OQ-15, and would prejudge it. Recorded as **OI-C-08**, owner A4 with OQ-15, and named in the manifest text so the gap is self-announcing rather than inferred.

### Ruling — the measurement instant

> **The budget record is a measurement of the tree at the instant of the build. It is not a property of the manifest and is not a reproducible constant. A later re-measurement that disagrees with a recorded one is expected drift, not a measurement defect.**

This makes the AMD-41 §2 finding a declared property rather than a discovery waiting to be re-made. It changes no verdict: `verdict_rule` still halts the build on any breach at the instant measured.

### Manifest change

`metadata.reproducible.budget_measurement_record` — two new members, `measurement_domain` and `measurement_instant`; `authority` extended. `validation[V-09].verifies` extended to bind the check to the declared domain — the AMD-19/AMD-26 lesson, *a ruling without a check is a convention*. No schema amendment.

---

## AMD-43 — OQ-B1: Lock JSON Layout

**Disposes:** OQ-B1 · **Interim choice in force:** 2-space indent, LF, one terminal LF, `ensure_ascii` false · **Ruled by:** `chief-systems-engineer · S-2026-08-08-10`

### Ruling

> **The interim choice is adopted as normative and made complete.** `core/MANIFEST.lock` is serialised with two-space indentation per nesting level, LF line endings, exactly one terminal LF, no trailing whitespace on any line, no space before a name separator and exactly one space after it, one member or array element per line, and no escaping beyond what RFC 8259 requires — a non-ASCII character is emitted as itself, never as a `\uXXXX` escape. Declared member order is emission order and is never sorted.

Grounds: the lock is a T1 file bearing a 200-token cap **and** a byte-identity requirement across at least two executions and, at V-10, two platforms. A layout left to the implementation is a layout that may differ between two conforming implementations, which would make `build_time_reproducibility` and V-10 tests of one implementation rather than of the build. Layout is therefore part of the specification. Adopting the interim choice — rather than a different one — is deliberate: it is already implemented, already certified against (TCR-001 C6), and no ground was found to prefer any alternative, so changing it would churn the first integrity baseline for no gain.

The escaping clause is load-bearing: `ensure_ascii` true and false produce different octets for the same JSON value, so leaving it undeclared leaves byte-identity undeclared. Rejected: minified single-line JSON (unreadable at B2a's digest read, and no smaller in tokens where it matters); sorted keys (contradicts the declared member order of `lock_serialisation`, which exists to keep `aggregate_digest` ahead of `files`).

### Manifest change

`metadata.reproducible.digest_constructions.core_aggregate.lock_json_layout` — new member, beside the `lock_serialisation` member it completes. No schema amendment.

---

## AMD-44 — OQ-B2: `build_provenance` Content

**Disposes:** OQ-B2 · **Interim choice in force:** source manifest DC-1, selected profile, stage, build id, run-fixed timestamp · **Ruled by:** `chief-systems-engineer · S-2026-08-08-10`

### Gap, restated

`build_provenance` is a **required** field of `sch-core-manifest`, and no text anywhere declared its content. A required field with undeclared content is the same defect class AMD-27 and AMD-29 closed for the digests: required, verified, never constructed.

### Ruling

> **`build_provenance` carries exactly six members, in this order: `source_manifest`, `source_manifest_dc1`, `selected_profile`, `compiler_stage`, `build_id`, `timestamp`.** The interim choice is adopted and closed, with `source_manifest` made explicit alongside its digest.

| Member | Value | Why it belongs |
|---|---|---|
| `source_manifest` | `framework/framework.manifest.json` | Names the input; the path is fixed but stating it makes the record self-describing |
| `source_manifest_dc1` | DC-1 of that manifest, 64 lowercase hex | **The load-bearing member.** It binds the lock to the manifest revision it was built from — the manifest is the single source of truth, and without this the lock records an aggregate whose coverage definition is unrecoverable |
| `selected_profile` | `BINDING.active_profile` at build time | With `files[]` and `enabled_agents`, this determines the covered set (AMD-27, AMD-39). A lock whose coverage input is unrecorded cannot be audited |
| `compiler_stage` | `6` | The emitting stage, per AIEF-AMD-007's rule that stage is declared, never inferred |
| `build_id`, `timestamp` | the run-fixed pair of AMD-48 | The provenance of the release run; the only two members not derived from files |

> **The set is closed.** Every value is a function of the manifest, of `project/BINDING.md`, or of the run-fixed pair. **Host name, user name, working directory, tool or interpreter versions, per-execution wall-clock time and any environment capture are prohibited** — each varies across the executions and platforms that `build_time_reproducibility` and V-10 require to agree octet for octet, so admitting any of them would make byte-identity unreachable by construction. The conventional build-provenance habit of capturing the environment is exactly wrong here.

Recorded, unchanged: `build_provenance` is one of the lock members the BINDING pin does not bind (AMD-27 *recorded_residual*). Tamper on it is detected by V-12 and version control, not by B2a.

### Manifest change

`metadata.reproducible.build_provenance_record` — new object. No schema amendment: `sch-core-manifest` requires the field and constrains no property of it.

---

## AMD-45 — OQ-B3: The Lock Self-Measurement Fixed Point

**Disposes:** OQ-B3 · **Interim choice in force:** lock row marked DEFERRED; emitted lock cap-checked post-serialisation, breach halts · **Ruled by:** `chief-systems-engineer · S-2026-08-08-10`

### Gap, restated

`files[manifest-lock]` carries `token_cap: 200`, so the lock is inside the measured set (AMD-42). But the budget record lives inside the lock, so the lock's own count inside its own record is a fixed point: writing the count changes the text whose count was written. No declared text resolves it.

### Ruling

> **The lock's per-file row is emitted with null counts, a null governing value and verdict `DEFERRED-SELF-MEASURED`, and contributes nothing to the per-family totals. The serialised lock octets are then measured under both families against the 200 cap after serialisation and before the archive is built; a breach halts the build exactly as an in-record breach does.** The deferral is keyed on the path `core/MANIFEST.lock` and on nothing else.

The interim behaviour is adopted with **one substantive correction**. The implementation defers on *absence from the tree* rather than on identity — the condition TCR-001 recorded as finding F1: *"the deferral is keyed on absence, not on identity. If a second capped file were ever absent it would defer rather than fail."* That is a latent fail-open: a measured file deleted from the tree would be silently deferred instead of halting the build. **Keying the deferral on the path closes it**, and the rule states expressly that any other measured file absent from the tree is a build defect that must halt. This disposes TCR-001 F1.

Why the cap is not simply dropped from the lock, and why the fixed point is not iterated:

| Alternative | Why rejected |
|---|---|
| Remove `token_cap` from `files[manifest-lock]` | The 200-token cap is frozen at `AIEF-FRZ-001` §1.8's table, and B2a's *"digest read"* is the reason `lock_serialisation` puts `aggregate_digest` before `files`. Dropping the cap would thaw frozen text and discard the constraint that shapes the lock's member order |
| Iterate to a fixed point (write count, re-measure, re-write until stable) | May not converge, and where it does the converged value depends on the iteration order — a construction whose output depends on how it was computed is not a construction. It also makes the lock's bytes a function of a search, defeating byte-identity |
| Record a placeholder digit inside the record | AMD-27 rejected alternative C in the same terms: a placeholder is the *required-but-never-constructed* defect class, and the value would be unverifiable by the construction containing it |

Post-serialisation measurement has the property the others lack: it is a **single-pass, terminating check on the final octets** — the very octets a booting session reads at B2a — and it enforces the cap fully. The record honestly says the row was deferred rather than asserting a number it cannot know.

### Manifest change

`metadata.reproducible.budget_measurement_record.lock_self_measurement` — new member. No schema amendment.

---

## AMD-46 — OQ-B4: Archive Entry Types

**Disposes:** OQ-B4 · **Interim choice in force:** file-only tar entries; directory-mode rule treated as vacuous · **Ruled by:** `chief-systems-engineer · S-2026-08-08-10`

### Tension, restated

`distributable.contents` says the archive holds the DC-4 covered set plus the lock and *"nothing else"*; `distributable.determinism` declares *"mode 0644 for regular files and 0755 for directories"*, which appears to contemplate directory entries the contents clause excludes.

### Ruling

> **Regular file entries only.** The archive carries one entry per member of `contents` and no directory entry, no symbolic link, no hard link and no device entry; an extractor creates directories from the entry paths. **The `contents` clause governs; the directory-mode clause is vacuous for a conforming archive** — it constrains any directory entry a future ruling might require, and is never a licence to add one.

There is no real conflict to resolve. `contents` is an enumeration of members and `determinism` is a table of header field values; an enumeration that says *"nothing else"* is not overridden by a mode value stated for an entry type the enumeration does not admit. Reading it the other way would add entries to the archive that DC-4 does not cover and `contents` excludes — and every added entry is an octet in the archive that DC-5 binds, so the reading is not cosmetic.

The vacuous clause is retained rather than deleted: deleting it would remove the declared mode for any future entry type, and re-deriving it later is exactly the kind of undeclared-value defect this amendment series exists to prevent.

### Manifest change

`metadata.reproducible.distributable.entry_types` — new member. No schema amendment.

---

## AMD-47 — OQ-B5: The BINDING Pin-Line Write Form

**Disposes:** OQ-B5 · **Interim choice in force:** value-token-only replacement · **Ruled by:** `chief-systems-engineer · S-2026-08-08-10`

### Ruling

> **Exactly one line of `project/BINDING.md` matches `core_digest_pin` followed by a colon. The build replaces the value token on that line with the 64-lowercase-hexadecimal DC-4 `aggregate_digest` and preserves every other octet of the file** — the leading indentation, the whitespace run between the colon and the value, any inline comment following the value, that line ending, and every other line unchanged. **Zero matching lines, more than one matching line, or a candidate pin value that is not 64 lowercase hexadecimal characters halts the build.**

Grounds: `generation_order[6].outputs` already classifies this output as *"a field write into an already-emitted instance artifact, **not** a re-emission of the project partition"*. A write that also realigned the line or dropped its inline comment would make the diff of an integrity-critical field larger than the field itself, and would put the compiler in the business of formatting an artifact in a partition it does not own — `project` is `agents-and-humans` write access and `never-touched` on upgrade. Preserving the inline comment matters concretely: `BINDING.md` today carries `core_digest_pin: PENDING-STAGE-6   # emitted by Compiler Stage 6`, and that comment is the human-readable record of which stage owns the field.

The three halt conditions are stated so the writer is a total function: a pin line that is absent, duplicated, or receiving a malformed value are all states in which the correct behaviour is to stop, not to guess.

### Manifest change

`metadata.reproducible.binding_pin_write` — new object. No schema amendment.

---

## AMD-48 — DC-1 of Empty Content; the Run-Fixed Timestamp and Build Id

**Disposes:** the two remaining lower-order items recorded at the foot of `project/STAGE-6_BUILD_OPEN_QUESTIONS.md` · **Ruled by:** `chief-systems-engineer · S-2026-08-08-10`

### Ruling — DC-1 of a zero-length file

> **A file whose normalised content is empty — no line survives the trailing-blank-line removal — has the empty octet string as its DC-1 preimage. Its DC-1 digest is therefore `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, the SHA-256 of zero octets.**

DC-1's *"append exactly one terminal LF"* step applies to surviving content, not to emptiness. Appending an LF to nothing would give an empty file and a file holding one blank line the same digest, collapsing two distinct states into one — and a construction that cannot distinguish two files it is asked to distinguish is a weaker construction for no benefit. The chosen reading is also already consistent with DC-2's declared `empty_registry` value, which is the SHA-256 of the empty preimage under the same reasoning; one framework, one treatment of emptiness.

**No non-empty digest changes.** Every digest recorded anywhere in this repository is unaffected: the rule defines a case that was undefined, and no covered or registered artifact is empty today. Stated expressly: **this defines the digest of an empty file; it does not licence one.** An emitted or registered artifact with no content remains a defect under the zero-dead-file rule of `AIEF-FRZ-001` §1.5.

### Ruling — AMD-33 run-fixed values

> **The Stage 6 build identifier and the measurement timestamp are captured once per release run, before its first execution, and are supplied unchanged to every execution of that run. They are inputs to the executions and never outputs of them.**

AMD-33 requires *"every execution [to yield] a byte-identical distributable"*. `build_provenance` and the budget record both carry a timestamp and a build id. A timestamp taken per execution would place a differing octet in every lock, hence in every archive, hence in every DC-5 — making byte-identity unreachable by construction and turning AMD-33's halt into a permanent one. Capturing them once per run is therefore not an implementation convenience; it is the only reading under which AMD-33 is satisfiable at all.

It follows that **the release run, not any single execution, is the unit of provenance** — which is precisely why those two values, and no other environment fact, are admitted to `build_provenance` (AMD-44). The rule applies equally to V-10's two-platform executions, where the same pair is carried across platforms.

### Manifest change

`metadata.reproducible.digest_constructions.per_artifact.empty_content` — new member, with the `status` member extended to point at it; `metadata.reproducible.build_time_reproducibility.run_fixed_values` — new member, with `authority` extended. No schema amendment.

---

## Content Reduction Performed

One reduction was performed, on the one measured file this session both owns and may reduce without loss. It is recorded here in full, per the directing instruction.

| | |
|---|---|
| File | `project/STATE.md` (`owner_role: chief-systems-engineer`; `mutability: mutable`; partition `project`) |
| Authority to reduce | The file's own declaration: *"This register is authoritative; **`STATE.md` is a derived cache**"* (`project/OPEN_ITEMS.md`). Nothing is recorded in `STATE.md` alone |
| Constraint honoured | `tpl-current-state` required sections all retained: Lifecycle stage, Active gate, Compiler stage, Last ledger sequence, Open blockers, Active tasks, Frozen set hash, Next action |
| Method | Narrative prose that restated content held authoritatively elsewhere was replaced by a pointer to its authoritative home. No blocker, open item, digest, count or lineage value was dropped |

The before-and-after measurement is recorded in `APR-012` § *The reduction performed*, and not here: a file inside the freeze registry cannot carry a number that a later measurement of a mutable file would falsify, and a file inside the measured set cannot state its own post-reduction count without changing it. `project/STATE.md` § *Budget* carries the standing verdict and points at `APR-012`.

**The reduction does not close the breach**, and it is not offered as a remedy: `BOOT.md` and `project/OPEN_ITEMS.md` remain in breach and the aggregate remains far above 6,000. It is the demonstration that supports AMD-41 §4 — the one lawful, lossless reduction available to this session, performed in full, and still insufficient.

**No reduction of `project/OPEN_ITEMS.md` was performed, deliberately.** It is the authoritative register; no reduction of it to 600 tokens is possible without destroying or relocating recorded content, and the relocation option is reserved to the owner as OQ-15 option (a). This session **added** to that register and reduced nothing in it.

---

## Blast Radius

Determined by inspecting what renders each changed manifest section, following the AMD-008/AMD-009/AMD-012 method.

| Changed section | Rendered by | Effect |
|---|---|---|
| `metadata.reproducible.*` — seven additive members, two `authority`/`status` extensions | `.ai/FRAMEWORK.md` § Integrity renders DC-1's headline rule only, unchanged | **None** |
| `validation[V-09].verifies` | `core/validation/CHECKS.md` and `core/validation/MANIFEST` — Stage 5 output emitted at `S-2026-08-08-03` | **Already stale in this exact field** (OI-V-07, from AMD-010). This extension deepens the existing staleness; it creates no new stale artifact and no new open item. Check count unchanged at 25. Re-emission is Stage 5 compiler work under CMP-BLOCK-004 |
| `adapters/ADP-ci.md` | Already stale (OI-C-02); check count unchanged | **No new staleness** |
| `src/aief_stage6/**` | Not rendered from the manifest; it *implements* it | **Implementation delta owed**, recorded as OI-C-09: one substantive change (AMD-45 — key the lock deferral on the path, not on absence; TCR-001 F1) plus conformance re-certification of the layout, provenance and pin-write rules against their now-normative texts. `src/` is PR-controlled; **not performed here** — A4 does not implement what it ruled (SOD-1) |
| `tests/**` | Not rendered from the manifest; it *asserts against* it | **Three assertions are now stale**, observed on a full-suite run at this session's close (114 tests: 111 pass, 3 fail; **no implementation defect**). `test_stage6_certification_evidence.py::TestV09Recomputation` pins the S-08 measurement of two `mutable` project files as constants — `project/STATE.md` 1791 and the totals 10296 / 12657 — which AMD-42 `measurement_instant` declares are not constants; `test_stage6_coverage_and_build.py::test_v24_live_registry` pins the registry at 28 members while V-24 itself **passes** at 29. Each failure is the ruling and the registry working, asserted against by a snapshot. Folded into OI-C-09; test maintenance belongs with the re-certification and is **not performed here** |

| Artifact | Change | Method |
|---|---|---|
| `framework/framework.manifest.json` | The nine changes of AMD-42…AMD-48 | Surgical edit under `APR-012`; re-registered in `FROZEN.md` at the new DC-1 |
| `framework/AIEF-AMD-013_…` | **NEW** — this instrument | Registered in `FROZEN.md` under `APR-013` (AMD-21 criterion) |
| `project/FROZEN.md` | Manifest row re-registered; this instrument added, 28 → 29; aggregate recomputed under DC-2 | Registry edit under `APR-012`/`APR-013` |
| `project/OPEN_ITEMS.md` | CMP-BLOCK-006 disposition status; OQ-B1…B5 closed; OQ-15, OI-C-08, OI-C-09 opened; TCR-001 F1 disposed under OI-V-09 | Register edit — **additive only** |
| `project/STATE.md` | `frozen_set_hash`; blockers; open items; `next_action`; § Budget; the AMD-41 reduction | Session write |
| `project/STAGE-6_BUILD_OPEN_QUESTIONS.md` | Disposition column added; the file marked ruled, contents preserved | Register edit |
| `ENGINEERING.md` | Index rows only: amendment count, §5 row, §7 registry count and item lists, §8 gate list | Index edit |
| `project/approvals/APR-012`, `APR-013` | **NEW** — the two recorded approvals | LAW-10 |

**Deliberately not touched:** every `.ai/core/**` byte and `.ai/adapters/**` byte · `.ai/BOOT.md` (the subject of AMD-41 §4 defect class A — **framework-only write access; not edited, and the determination says so**) · `project/BINDING.md` · `project/ledger/**` (`HEAD` remains at `genesis`, `seq 0`; `L-0000001` does not exist) · `core/MANIFEST.lock` (**not created** — Stage 6 remains unauthorized, OQ-14) · the distributable (**not created**) · `src/aief_stage6/**` and `tests/**` · `spec/**`, `AIEF-FRZ-001`, AMD-001…AMD-012, both ADRs, every schema, `ECR-D-001…004` · git history, tags, author or committer identity — no commit, tag or push is made by this session, and no attribution trailer of any kind is written anywhere.

---

## Separation of Duties — Recorded Tension

`core/agents/INDEX.md`: **`chief-systems-engineer` may not implement what it approved.** This instrument was ruled, and its manifest, registry and index edits applied, by the same authority (`chief-systems-engineer · S-2026-08-08-10`) at the direction of the human owner — `core/PRECEDENCE.md` rank 1, which outranks the rank-6 agent specification. Identical in form to the departures recorded in AMD-008 through AMD-012 §§ *Separation of Duties*; identically **authorised, not erased** (SOD-1).

| | |
|---|---|
| Duty separated | A4 rules and approves; A1 implements |
| Departure | A4 both ruled and applied |
| Authority for the departure | Live human-owner instruction of `S-2026-08-08-10`, rank 1, recorded per LAW-10 in APR-012 and APR-013 |
| Not departed from | The implementation delta AMD-45 requires in `src/aief_stage6/**` was **not** performed by this session. It is recorded as OI-C-09 for an A1 role. A4 ruling a construction and then writing the code that implements it is the departure this table exists to bound, and it was declined here |
| Mitigating control | Independent cold-context `qa-engineer` audit of this session's work — dispatched by the same directing authority; open until filed |
| Not mitigated by | Anything this document says about itself. Under LAW-05 an authority's assertion about its own work carries no evidentiary weight. In particular, AMD-41's re-measurement is this session's own evidence about a prior session's evidence, and needs independent recomputation before it is relied upon |

---

## Approvals Required and Recorded

| Change | Approval | Bound to |
|---|---|---|
| The manifest amendment of AMD-42…AMD-48, and re-registration of the manifest in `FROZEN.md` at its post-change digest | `project/approvals/APR-012` | the post-change manifest DC-1 digest (`subject_hash`), with the pre-change digest as `prior_hash` |
| Freeze-registry addition of this document (AMD-21 criterion: authorising instrument for a change to a frozen artifact) | `project/approvals/APR-013` | this document's DC-1 digest |

AMD-41 requires no approval of its own: it changes no frozen artifact. It is a determination and a reservation, and its authority is LAW-02 and LAW-12.

Per the AMD-16 design property, neither this document's own digest nor the post-registration DC-2 aggregate appears in this document; both live in the registry and the approval artifacts.

---

**END OF AIEF-AMD-013**
