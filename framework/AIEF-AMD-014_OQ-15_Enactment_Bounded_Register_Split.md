# AIEF-AMD-014 — Architecture Amendment: OQ-15 Enacted — the Bounded Register Split, the `BOOT.md` Cap, and the Disposition of CMP-BLOCK-006

**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-02 (disposition of a recorded blocker; and the raising of a class-D defect), LAW-01 + LAW-10 (change to a frozen artifact — `framework/framework.manifest.json`), LAW-12 (open decision with recorded rationale, never assumption)
**Scope:** (i) enactment of the human owner's **OQ-15** decision — option (a), the lossless register split, exactly as `AIEF-AMD-013` §AMD-41 §6 specifies it; (ii) the `BOOT.md` `token_cap` raise to its minimum admissible value; (iii) the aggregate-ceiling charge closing `VER-007` FIND-Q7-3; (iv) the **disposition of CMP-BLOCK-006**; (v) the register corrections `VER-007` FIND-Q7-1, -5, -6 and -7 require; (vi) the raising of **ECR-D-006**, a freeze-registry divergence found while performing (i)–(v). **Nothing else.** No Stage 6 execution, no `core/MANIFEST.lock`, no distributable, no ledger write, no BINDING change, no tag, no commit.
**Date:** 2026-08-08 · **Session:** `S-2026-08-08-12`
**Amends:** `framework/framework.manifest.json` — **eleven** changes, enumerated at full granularity in `APR-014`: four new members or entries, two new dependency edges, one `token_cap` value, and four extensions to existing text
**Does not amend:** `AIEF-FRZ-001` — **no byte, no digest, and no supersession in reading.** §1.8's derivation stands exactly as frozen: the 32,000-token portability floor, the 20% share, the 6,000 ceiling and seven of its eight cap rows are untouched; the eighth, `BOOT.md`, is amended in the manifest under §AMD-50, which is the cure §1.8's own reasoning prescribes and is recorded as a supersession of that one table cell in value, not of the derivation · `AIEF-AMD-001` … `AIEF-AMD-013` · either ADR · `SCH-framework-manifest.schema.json` (the amended manifest passes it unmodified, 0 errors) · `SCH-core-manifest.schema.json`, `SCH-state.schema.json` or any other emitted schema · `tpl-current-state` · any law rule or clause · any role contract · any partition, layer, tier, boot step, compiler stage or lifecycle definition · DC-1, DC-2, DC-3, DC-4, DC-5 · TF-1 and TF-2 · **`version.min_context_window`, `version.boot_ceiling_tokens`, and every `token_cap` other than `files[boot]`**
**Authorising basis:** live human-owner instruction of session `S-2026-08-08-12` (`core/PRECEDENCE.md` rank 1), recorded verbatim at §AMD-49 §1 and per LAW-10 in `project/approvals/APR-014` and `project/approvals/APR-015`

---

## Independence declaration

**OQ-15 is not ruled here.** It was decided by the human owner, whose instruction this instrument enacts. `AIEF-AMD-013` §AMD-41 §§5–7 determined that an architecture amendment was required, ruled out both pure strategies, recorded four lawful options and reserved the choice under LAW-12 — expressly because *"what remains is a genuine choice among lawful architecture alternatives with real trade-offs [and] it is not a determination."* The owner has now made it. This session's task is execution, not selection, and where the existing record fixes a detail this instrument follows it rather than re-deriving it.

`CMP-BLOCK-006` was registered by `project-manager` action at the filing of `VER-006`, on the finding of `qa-engineer · S-2026-08-08-09b`, over evidence produced by `software.platform-engineer · S-2026-08-08-08` and certified by `software.test-engineer · S-2026-08-08-09`. Its determination was filed by `chief-systems-engineer · S-2026-08-08-10` and independently audited by `qa-engineer · S-2026-08-08-11` at `VER-007`, which recomputed every arithmetic sub-claim. The findings dispositioned here were raised by that audit.

This instrument is written by `chief-systems-engineer · S-2026-08-08-12`, a cold session holding no state from any prior session and having authored none of the artifacts named above. Under `AIEF-AMD-008` §AMD-20, agent identity for LAW-02, LAW-04 and LAW-05 independence is the pair (role, session): this session differs from `S-2026-08-08-10` and `S-2026-08-08-11` in session, and from `-08`, `-09` and `-09b` in both role and session. Session id `S-2026-08-08-12` was adopted after confirming from the repository that `-01` … `-11`, with sub-sessions `-03b`, `-03c`, `-04b`, `-05b` and `-09b`, are consumed and `-12` is unused.

**ECR-D-006 is raised, not disposed.** LAW-02 clause 5 — *"No ECR may be closed by the agent that raised it"* — and clause 4 — *"ECR-D disposition requires human involvement and re-gating"* — both apply, and both are honoured: §AMD-53 states the defect and its evidence and recommends a disposition; it decides nothing.

The same-authority ruled-and-applied departure is separately recorded in § *Separation of Duties*.

| Ruling | Subject | Change class |
|---|---|---|
| AMD-49 | OQ-15 enacted — the bounded register split, its `files[]` entries, its index grammar and its 1:1 mapping | Manifest change — `metadata.reproducible.bounded_register_split`; two `files[]` entries; two `dependencies.edges`; `validation[V-03].verifies` |
| AMD-50 | `files[boot].token_cap` 400 → 504 — the minimum admissible value, derived | Manifest change — one `token_cap` |
| AMD-51 | The aggregate-ceiling charge for the deferred lock row, disposing `VER-007` FIND-Q7-3 | Manifest change — `budget_measurement_record.aggregate_ceiling_charge`; `authority` and `verdict_rule` extended; `validation[V-09].verifies` |
| AMD-52 | **CMP-BLOCK-006 disposed**; the register corrections of `VER-007` FIND-Q7-1, -5, -6, -7; OI-C-08 restated and expressly not cured; OI-C-10 raised | Disposition + register corrections. **No manifest change** |
| AMD-53 | **ECR-D-006 raised** — the freeze-registry divergence on `framework/framework.manifest.json` | Finding + recommendation. **No manifest change** |

---

## AMD-49 — OQ-15 Enacted: the Bounded Register Split

**Enacts:** the human owner's OQ-15 decision · **Disposes:** OQ-15 (`project/OPEN_ITEMS_REGISTER.md`, Open not blocking) · **Applied by:** `chief-systems-engineer · S-2026-08-08-12`

### 1 · The instruction, verbatim

> "Rule OQ-15 = OPTION (a). Implement the lossless register split exactly as specified in the existing OQ-15/A4 record: bounded T1 OPEN_ITEMS.md index; full authoritative register in the declared cap-null T4 files[] location; deterministic 1:1 mapping; preserve all information; raise BOOT.md cap only to the minimum required value; apply the same required bounded-register treatment to STATE.md. Use the existing architecture and OQ-15 record as authority. Do not redesign it."

`core/PRECEDENCE.md` rank 1. It outranks the rank-3 freeze registry; clause 4 and LAW-10 clause 4 require the override be recorded before dependent work is committed, and `APR-014`/`APR-015` are that record.

### 2 · What option (a) already fixed, and is therefore followed rather than re-decided

`AIEF-AMD-013` §AMD-41 §6 option (a) reads, in full: *"Add a `files[]` entry for the full register (e.g. `project/OPEN_ITEMS_REGISTER.md`, tier T4, cap null, partition `project`, generator 3); `project/OPEN_ITEMS.md` becomes a bounded index carrying every identifier, its class and status, and a pointer. Boot step B7 is unchanged — it still reads `project/OPEN_ITEMS.md`."* Its cost clause adds: *"the bare index measured at 454 today still leaves only ~150 tokens of growth against the 600 cap, so the index's own cap likely needs raising too (drawing on the 200-token pool) **or its row grammar constraining**."* The OQ-15 reservation's closing observation adds: *"under (a) that means **an index grammar bounding per-entry cost in both registers**."*

Every one of those is a fixed detail and is implemented as written. The path, tier, cap, partition and generator of the new entry are taken from the text; the index keeps its id, path, tier, cap, owner and boot step; and because the owner's instruction raises **only** `BOOT.md`'s cap, the disjunct the record itself offers — constraining the row grammar rather than raising the index's cap — is the one that is available, and it is taken.

### 3 · Ruling

> **A project register whose authoritative content grows monotonically with the engineering history is split into two `files[]` entries: a bounded *index* that keeps the original id, path, tier, `token_cap`, `owner_role` and boot step, and a *register* that carries the full authoritative content at tier T4 with `token_cap: null`. The index is the file boot reads; the register is where authority lives. Two pairs are declared: `open-items` ↔ `open-items-register` and `state` ↔ `state-register`.**

| New `files[]` entry | Path | Tier | Cap | Layer / partition | Owner | Mutability / integrity | Generator |
|---|---|---|---|---|---|---|---|
| `open-items-register` | `project/OPEN_ITEMS_REGISTER.md` | **T4** | **null** | L4 / `project` | `project-manager` | mutable / unhashed | 3 |
| `state-register` | `project/STATE_REGISTER.md` | **T4** | **null** | L4 / `project` | `chief-systems-engineer` | mutable / unhashed | 3 |

Each declares `depends_on: []` and `referenced_by: ["<its index>"]`, both `files[]` ids, so **MI-3 strict** — targets range over `files[]` ids only, `AIEF-AMD-009` §AMD-24 — is satisfied. Neither introduces a `depends_on` edge, so **V-23** stage monotonicity is untouched: there is no new same-stage ordering constraint to satisfy. The citation is additionally recorded as a `dependencies.edges` `references` edge in each direction of use, keeping V-02 and V-03 able to see the relation.

**Tier T4 is the whole mechanism.** `core/CONTEXT_TIERS.md` declares T4 *"Explicit request only — unbounded"*, and `BOOT.md`'s own tier rule declares *"T4 only on explicit request."* No boot step names a register; `boot_sequence[B3].files` is `["state"]` and `boot_sequence[B7].files` is `["open-items"]`, both unchanged. That, and nothing else, is what bounds the boot cost while the register grows without limit. It is the mechanism the architecture already applies to the ledger — `HEAD` is read at B4 for O(1) lookup while *"body never read at boot"* and sealed segments are T4-only (OD-9) — and AMD-41 §7 ground 2 named that precedent expressly: *"the register is the one authoritative artifact for which that pattern was never applied."*

### 4 · The index grammar, and why the cost it bounds is the right cost

> **The index carries a title, the emitted instance-artifact provenance header, a preamble naming its register and stating the mapping, and level-2 headings each followed by identifiers — one identifier per line, nothing else on that line. Recorded item text never enters the index. A register row key is a compact identifier: a row whose pre-split leading cell was a phrase carries a compact key and retains that phrase verbatim at the head of its first content cell.**

The per-entry cost of the index is therefore the identifier alone — measured at this session's close, about six tokens under the governing family — and it is *independent of how much has been recorded about that item*. That is the property AMD-41 §4 identified as missing: *"the register's size is a function of how much has been recorded, and recording is the register's purpose."* After the split the index's size is a function of how many things have been recorded, not of how much; the volume goes to a file no boot step reads.

Two register rows carried phrases as leading cells. Under the grammar their keys become `OQ-B1…B5` and `OQ-1…OQ-12`, and each row retains its pre-split leading cell verbatim in its first content cell, with the second additionally stating in words which identifiers the range denotes. **No text is lost; a key is renamed and the old key is preserved as content.**

### 5 · The mapping — deterministic, bijective, mechanical

> **`open-items` pair, by identifier.** Every identifier listed in `project/OPEN_ITEMS.md` appears **exactly once** as the leading cell of exactly one table row of `project/OPEN_ITEMS_REGISTER.md`, under the register heading whose text is **identical** to the index heading that lists it; and every such leading cell appears exactly once in the index, under that same heading. **Order carries no meaning on either side and is not part of the mapping.** A missing, duplicated or section-mismatched identifier on either side is a defect.

> **`state` pair, by section name.** Every key of the YAML block of `project/STATE.md` appears **exactly once** as a level-2 heading of `project/STATE_REGISTER.md`, and every level-2 heading of that register is either such a key or the literal heading `Notes`. The `STATE.md` block remains authoritative for the eight `sch-state` required field values and satisfies `tpl-current-state` unchanged; the register carries their detail, rationale and pointers.

Both mappings are evaluable by string equality over declared inputs. Neither admits editorial judgement, neither depends on ordering, and neither requires reading a word of item text. A checker needs the heading text and the leading cells, and nothing more.

**A ruling without a check is a convention** — the AMD-19/AMD-26 lesson, restated at `AIEF-AMD-013` §AMD-42. The mapping is therefore bound into `validation[V-03]`, whose class is *Cross-reference validation* and whose `law_ref` is **LAW-06**, the law that requires *"every relative reference must resolve"* and forbids orphan artifacts. A register row that no index entry reaches is an orphan in exactly LAW-06's sense; an index entry that reaches no row is a broken reference. V-03 is the check that already exists for both.

### 6 · What was preserved, and how it was verified

The instruction says *preserve all information*. The verification is mechanical and is recorded in `APR-014` § *Information preservation*: the identifier set of the pre-split register and the identifier set of the post-split register are equal — **46 in, 46 out, none lost, none invented** — with exactly two identifiers changing section, both by ruling (`CMP-BLOCK-006` and `OQ-15`, from Blocking and from Open-not-blocking to Closed). Every row's pre-split text is carried verbatim; where a row is updated the original wording is retained and the update is appended and attributed. Two identifiers were **added** by this session's own work, `ECR-D-006` and `OI-C-10`, giving 48 rows at the close.

### 7 · Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Keep the index rows as a table with a status column and a per-row pointer | Measured at this session's close, the table form costs about ninety tokens more than the line form for the same identifiers, and the status is already carried by the section heading and the pointer by the single declared mapping rule. Per-row pointers repeat one fact forty-eight times |
| Index only the open items and leave Closed enumerated in the register alone | Cheaper, and it breaks the mapping in one direction: a closed row would be reachable from no index entry. The instruction says *deterministic 1:1 mapping*, and one-directional is not 1:1 |
| Raise `project/OPEN_ITEMS.md`'s own cap instead of constraining the grammar | Not authorised. The instruction raises `BOOT.md`'s cap *only*, and after §AMD-50 the MI-4 headroom is 96 tokens — see §AMD-50 §4. AMD-41 §6 offered the grammar constraint as the alternative to a cap raise for exactly this reason |
| Move the registers outside `.ai/project/` | They are project state and `partition: project` is *never-touched* on upgrade; moving them would place authoritative project content where an upgrade could reach it |

### 8 · Manifest change

`metadata.reproducible.bounded_register_split` — new object, seven members. Two new `files[]` entries. Two new `dependencies.edges`. `validation[V-03].verifies` extended. No schema amendment: `metadata.reproducible` does not declare `additionalProperties: false`, `files[].tier` already admits `T4`, and the amended manifest validates against the byte-unchanged frozen schema with **0 errors**.

---

## AMD-50 — `files[boot].token_cap`: 400 → 504, the Minimum Admissible Value

**Enacts:** the instruction's clause *"raise BOOT.md cap only to the minimum required value"* · **Cures:** AMD-41 §4 defect class A · **Ruled by:** `chief-systems-engineer · S-2026-08-08-12`

### 1 · What "minimum required" resolves to, and why

The V-09 per-file rule is fixed: measure under both declared families, *"the maximum governs"* (`tokenizer_families.governing_rule`, from `AIEF-FRZ-001` §1.8), and the verdict is PASS if and only if the governing value does not exceed the cap. `BOOT.md`'s bytes cannot be changed by any actor available today — `partition: root`, `write_access: framework-only`, `mutability: immutable`, and a re-render is a Stage 1 emission, which is CMP-BLOCK-004. The cap must therefore accommodate the file exactly as it stands.

Measured this session from the pinned artifacts, both families:

| | TF-1 | TF-2 | Governing |
|---|---|---|---|
| `BOOT.md` | 445 | **504** | **504** |

> **The minimum required value is the governing measurement itself: 504.** Any cap below 504 fails V-09 by construction; 504 is the least integer that does not. There is no third quantity to choose between.

This measurement is not novel and is not this session's alone. It reproduces to the digit across **five** independent prior recordings: `TCR-001` §3.2 (`software.test-engineer · S-2026-08-08-09`), `VER-006` C4 (`qa-engineer · S-2026-08-08-09b`), `AIEF-AMD-013` §AMD-41 §1, `APR-012` § *The reduction performed*, and `VER-007` §4a/§4c (`qa-engineer · S-2026-08-08-11`, under that auditor's own independently assembled tokenizers). `BOOT.md` is the one measured file every one of those recordings agrees on, in both families, because it is immutable — which is precisely why AMD-41 §2 could use it as the control that separated real drift from measurement error.

### 2 · The frozen render floor is a lower bound, not the answer

`AIEF-AMD-013` §AMD-41 §4 derived, from `BOOT.md`'s own frozen specification, a **render floor of 475 TF-2** — the eleven-row `boot_sequence` table at 346, the tier rule at 47, the governing rule at 82 — and showed that even deleting the `Cost` column MI-11 requires still leaves 436. `VER-007` §4d reproduced all five of those figures to the digit. The floor establishes that **no conforming render of `BOOT.md` can meet 400**, which is the determination; it does not establish the cap, because a cap set at the floor would still fail the actual file. The floor is the proof that the cap is the defect; the measurement is the cap.

### 3 · Why not 550

`AIEF-AMD-013` §AMD-41 §6 observed that *"raising it alone from 400 to 550 would give Σ = 5,950 ≤ 6,000 and satisfy MI-4 today"* and then **declined to set the value**, reserving it to travel with OQ-15 because the headroom is a shared pool. The owner has now allocated it, with the words *only to the minimum required value*. 550 carries 46 tokens of comfort for a file that cannot change; that comfort would be drawn from the same 96 tokens the next authority will need. 550 was illustrative arithmetic, never a proposed value, and it is not adopted.

### 4 · MI-4, before and after

MI-4 is *Σ `token_cap` over T0 ∪ T1 ≤ 6,000*. The two new entries are `token_cap: null` and are outside its domain, exactly as the nine existing cap-null T0/T1 entries are (`budget_measurement_record.measurement_domain`, `AIEF-AMD-013` §AMD-42).

| | `BOOT.md` | `FRAMEWORK.md` | `MANIFEST.lock` | `PRECEDENCE.md` | `laws/INDEX.md` | `BINDING.md` | `STATE.md` | `OPEN_ITEMS.md` | **Σ** | Headroom |
|---|---|---|---|---|---|---|---|---|---|---|
| Before | 400 | 1100 | 200 | 700 | 900 | 800 | 1100 | 600 | **5800** | 200 |
| After | **504** | 1100 | 200 | 700 | 900 | 800 | 1100 | 600 | **5904** | **96** |

`5800 − 400 + 504 = 5904 ≤ 6000`. **MI-4 holds.** `version.boot_ceiling_tokens` remains 6000 and `version.min_context_window` remains 32000, so `AIEF-FRZ-001` §1.8's derivation — 32,000 × 20% — is arithmetically untouched and the ratified portability floor is unchanged. What changes is one cell of its cap table, in the manifest, by the mechanism §1.8's own reasoning prescribes: it superseded the Rev A ceiling of 3,900 on the ground that *"it was asserted without derivation and was unachievable against its own file specifications."* A cap of 400 on a file whose conforming render floor is 475 is that same defect, one row down.

### 5 · Recorded consequence

A cap set at the measurement leaves `BOOT.md` **zero per-file headroom**. That is the direct and intended consequence of *minimum required*, and it is recorded rather than softened: any future Stage 1 re-emission that changes `BOOT.md` by one token breaches its cap and must re-derive it. `BOOT.md` is `lifecycle: framework-versioned`, so that can only happen at a framework re-emission, which is already an event that re-runs V-09.

### 6 · Manifest change

`files[boot].token_cap`: `400` → `504`. One value. No other `token_cap` and no ceiling changes.

---

## AMD-51 — The Aggregate-Ceiling Charge for the Deferred Lock Row

**Disposes:** `VER-007` FIND-Q7-3 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-12`

### Gap, restated from the audit

`core/MANIFEST.lock` carries `token_cap: 200` and is a member of the AMD-42 measured set; its 200 is one of the eight caps that sum to `AIEF-FRZ-001` §1.8's 5,800 and that MI-4 ranges over. `AIEF-AMD-013` §AMD-45 rules that its row is emitted `DEFERRED-SELF-MEASURED` and *"contributes nothing to the per-family totals"*, and `verdict_rule` then compares those totals to the 6,000 ceiling. `VER-007` FIND-Q7-3: *"A conforming build can therefore report an aggregate of 6,000 — PASS — while the true capped T0 ∪ T1 cost is up to 6,200."*

The audit also observed that this is *"the same shape as the under-coverage the session **did** record as OI-C-08 … raised there with the words 'under-covers the real boot cost by exactly one file and over-covers nothing'"* — and that it went unrecorded.

### Ruling

> **Whenever the lock's per-file row is `DEFERRED-SELF-MEASURED`, the aggregate ceiling comparison adds `files[manifest-lock].token_cap` to each per-family total before comparing to the 6,000 ceiling. The charge is the declared cap, never an estimate. The per-file rows, the per-file verdicts, and the post-serialisation cap check of the emitted lock octets are all unaffected.**

Grounds:

1. **It cannot under-state.** The lock's true count is bounded above by its cap — AMD-45's post-serialisation check halts the build otherwise — so charging the cap is an upper bound on the omitted quantity. A ceiling test that may over-state and can never under-state is sound in the only direction that matters for a blocking gate.
2. **It is one of the two dispositions the audit itself named**, and it is the one that requires no second measurement pass: *"compare the totals to 5,800 whenever the lock row is DEFERRED-SELF-MEASURED"* is arithmetically identical to charging 200 against 6,000, and stating it as a charge keeps the ceiling constant at its frozen value rather than introducing a second, derived ceiling that a reader must reconcile with `version.boot_ceiling_tokens`.
3. **It draws on no MI-4 headroom**, which is why it can be closed here while OI-C-08 cannot. The charge changes an arithmetic comparison, not a declared cap; `Σ token_cap` is unchanged at 5,904.
4. **It keeps the measured domain and the declared domain the same set** — AMD-42's own ground 1: *"the measurement side of a budget and the declaration side of the same budget must range over the same set."* Before this ruling the declaration side counted the lock's 200 and the measurement side did not.

Rejected: adding the lock's post-serialisation count into the totals and re-testing. It is more precise and it re-opens the fixed point AMD-45 closed — the totals would then be a function of the serialised lock whose content contains the totals. AMD-45 rejected iteration for exactly that reason, and precision bought with a fixed point is not precision.

### Manifest change

`metadata.reproducible.budget_measurement_record.aggregate_ceiling_charge` — new member; `authority` extended to cite this ruling; `verdict_rule` extended to name the charged comparison; `validation[V-09].verifies` extended. No schema amendment. **An implementation delta follows** and is added to OI-C-09: `src/aief_stage6/budget.py` `measure()` compares the un-charged totals today.

---

## AMD-52 — CMP-BLOCK-006 Disposed; the Register Corrections; OI-C-08 Restated; OI-C-10 Raised

**Disposes:** CMP-BLOCK-006; `VER-007` FIND-Q7-1, FIND-Q7-5, FIND-Q7-6, FIND-Q7-7 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-12` · **No manifest change**

### 1 · The disposition

> **CMP-BLOCK-006 is DISPOSED. V-09 passes: every per-file cap is respected under both declared families, and the charged aggregate is below the 6,000 ceiling under both.**

The disposition rests on measurement, not on argument. The closing per-file table and the aggregate are recorded in `APR-014` § *The split as measured* — **deliberately not here, and deliberately not in either register**: a file inside the measured set cannot state its own count without changing it, `AIEF-AMD-014` is inside the freeze registry and cannot carry a number a later measurement of a mutable file would falsify, and the bounded index cannot carry prose at all. That is the same reasoning `AIEF-AMD-013` § *Content Reduction Performed* applied to `APR-012`, and it is followed here.

Both defect classes AMD-41 §4 identified are cured, each by the mechanism that class requires:

| Class | Defect | Cure |
|---|---|---|
| **A** | *"a compiler-output cap the compiler's own output cannot meet"* — `BOOT.md` governing 504 against cap 400, with the file immutable and unreachable by any available actor | **§AMD-50.** The cap is amended to the measurement. The file is not touched, and the determination that it could not be touched is what makes the cap the only lawful place to act |
| **B** | *"a fixed cap on live, monotonically growing project state"* — `OPEN_ITEMS.md` at 14.5×, later 21.3×, its cap; `STATE.md` inside its cap only at near-index form with 17 tokens of headroom | **§AMD-49.** Both registers become bounded indexes whose cost is one identifier per item, with the recorded volume moved to cap-null T4 files no boot step reads. The register may now grow without end |

**Nothing was destroyed to achieve it.** §AMD-49 §6 and `APR-014` § *Information preservation* record the mechanical demonstration: 46 identifiers in, 46 out, none lost, two moved by ruling, every row's pre-split text carried verbatim.

### 2 · FIND-Q7-1 — the register's own figures

`VER-007` found that the CMP-BLOCK-006 row asserted three measurements in the present tense — *"today"* — that the session writing them had already superseded before it closed, including a `STATE.md` breach that no longer existed. Its recommended disposition: *"restate the CMP-BLOCK-006 figures at their measured values with an explicit instant, or replace them with a pointer to `APR-012`."*

> **Ruled: every figure in the register that is a measurement carries the instant at which it was measured, and no measurement is stated in the present tense.** The CMP-BLOCK-006 row now carries the full measurement history — four instants, from `S-2026-08-08-08` to the close of `S-2026-08-08-11` — each attributed to the artifact that recorded it, and the closing figures live in `APR-014` rather than in the register.

This is the register-side complement of AMD-42's `measurement_instant`, which declared that the record *"is not a reproducible constant"*. A declaration that measurements drift is not served by a register that writes them as if they did not. The audit's warning is also honoured: *"do not re-measure into the register on a schedule; that is the defect AMD-41 identifies."* The history is closed at this session; it is not a field to be refreshed.

### 3 · FIND-Q7-5 — the role in which a `project-manager`-owned register is edited

> **Ruled: an A4 session editing `files[open-items]` or `files[open-items-register]` records the role in which it did so.** `project/OPEN_ITEMS_REGISTER.md` and `project/OPEN_ITEMS.md` now carry that record at their head, in the `VER-004`/`VER-006` filing form: applied by `chief-systems-engineer · S-2026-08-08-12` in `project-manager` role at rank-1 direction.

The rank-1 instruction authorises the edit and SOD-1 covers it in substance; what was missing was the record, and the established practice is explicit about making it. No content changes.

### 4 · FIND-Q7-6 — `ENGINEERING.md` self-contradiction and the stale `UNASSIGNED` claim

> **Ruled: `ROSTER.md` governs on assignment.** The three `software.*` roster rows are **assigned**, not UNASSIGNED. The `OQ-13` Closed row's *"roster rows added UNASSIGNED"* was true when written and was superseded within the day; it is corrected in place with the original wording struck and retained. `OI-P-02` is narrowed to the three universal rows it actually concerns. `ENGINEERING.md` §6's Stage 6 row is synced with §8's gate list.

`ENGINEERING.md` is an index and carries no authority, so nothing was voided by the contradiction; but an index that contradicts itself and the artifact it indexes is a defect in the index, and it is repaired.

### 5 · FIND-Q7-7 — the `STATE.md` provenance header

> **Ruled: the emitted instance-artifact provenance header form is restored** to `project/STATE.md`, matching its five siblings. The audit noted it cost about fifteen of that file's seventeen remaining tokens; inside the split it costs nothing that matters, which is a small demonstration of what the split buys.

### 6 · OI-C-08 — restated, and expressly not cured

`project/ledger/HEAD` is named in `boot_sequence[B4].files`, carries `tier: T1` and `token_cap: null`, and measures 411 / 504 — reproduced this session, unchanged across `-10`, `-11` and `-12`. The measured set under-covers the boot-loaded set by exactly this one file.

> **Not cured, and the arithmetic says why.** After §AMD-50, Σ `token_cap` = 5,904 against MI-4's 6,000: **96 tokens of headroom**, against the **504** a cap on `ledger-head` would require. The owner's instruction allocated the headroom to `BOOT.md` and to nothing else. Curing OI-C-08 now requires either a `token_cap` reduction elsewhere — the option (b) redistribution the owner did not choose — or a ceiling re-derivation, and both are human-owner architecture decisions, not determinations. Under LAW-12 this authority does not make them.

The exposure is unchanged in kind and is not enlarged by anything in this instrument: it under-covers by one file and over-covers nothing, and it remains self-announcing in the manifest at `budget_measurement_record.measurement_domain`. Its twin, FIND-Q7-3, **is** closed at §AMD-51 — the difference is that the charge draws on no headroom and a cap does.

### 7 · OI-C-10 — raised

The split bounds the index's cost to one identifier per recorded item. That is a change of kind — the index no longer grows with the volume of what is recorded — but not a change of order: it still grows with the count of identifiers. At about six governing tokens per identifier against the headroom the 600 cap leaves, the index admits on the order of a dozen further identifiers before it breaches; closing an item costs nothing, since the identifier merely moves section. Recorded as **OI-C-10** with its arithmetic, so that the next authority meets a number rather than a surprise. It is not a defect and it is not cured here, for the same reason as OI-C-08: after §AMD-50 there is no cap headroom left to allocate.

---

## AMD-53 — ECR-D-006 Raised: Freeze-Registry Divergence on the Manifest

**Raises:** ECR-D-006 (LAW-02 class D) · **Found by:** `chief-systems-engineer · S-2026-08-08-12`, while establishing `APR-014`'s `prior_hash` · **No manifest change** · **Disposes nothing**

### 1 · The finding

Before this session's edits, `framework/framework.manifest.json` normalised under DC-1 to

```
e87ae68e87ba1da61f05115d4abbe931808f00c1cecc512168a578e5a12cf892
```

`project/FROZEN.md`, `APR-012` `subject_hash`, and the membership behind `STATE.frozen_set_hash` all carry

```
8af8971b78d762e5db2879e50585a78f4e6d497ea707c664a9c06e1ba7e42ff7
```

They do not agree. **V-24 was failing at the boot of this session**, on exactly one of twenty-nine registered paths. The other twenty-eight verify to the digit.

### 2 · Method, and the control that makes it trustworthy

The pre-change bytes are not in git — sessions `-05` … `-12` are uncommitted, the consequence recorded at OI-V-04 and `VER-007` FIND-Q7-8 — so they were reconstructed by inverting this session's ten manifest edits, and the reconstruction was verified three ways:

1. It differs from the current file by **exactly** those ten edits and nothing else.
2. Reverting the three `AIEF-AMD-012` changes and the thirteen `AIEF-AMD-013` changes from it yields the `HEAD` blob **byte for byte**, whose DC-1 is `ae16ccaca5746b81a2a992841fc1d239fd1c8b0c34657c05611e025a9d8395aa` — the value `VER-007` §5c independently records.
3. **The control.** Reverting only the `AIEF-AMD-013` changes yields DC-1 `f06125d2f9bd0860ab72c73f7dd11318d5d4f3169ded23b86f33e9c469707638` — **exactly** `APR-010` `subject_hash` and `APR-012` `prior_hash`, a value recorded four sessions before this one and reproducible by anyone from `FROZEN.md`'s retained 28-member aggregate.

Control 3 is decisive. It proves the reconstruction pipeline and the DC-1 implementation exact **on this very file**, at a checkpoint recorded by a different session, and it locates the divergence: it is **confined to the `AIEF-AMD-013` change set**.

Nine alternative constructions of the recorded value were tested — raw octets, CRLF, absent and doubled terminal LF, byte-order mark, UTF-16LE, two JSON re-serialisations, and a whitespace variant. **None** reproduces `8af8971b…`. This is a content divergence, not a disagreement about the construction.

Every digest above was computed **twice by independent means**: once with an implementation of DC-1 written this session from the manifest's own normative text, importing nothing from `src/`, and once with `src/aief_stage6/digests.py`. The two agree on every value.

### 3 · What is *not* wrong

The **content** on disk is the approved content. The sixteen hunks between the `HEAD` blob and the pre-change file map 1:1 onto `APR-010`'s three enumerated changes and `APR-012`'s thirteen, with nothing riding along — the same conclusion `VER-007` C4 reached by structural diff. No unauthorised member, value or cap is present. What is missing is a reproducible binding between that content and an approval.

### 4 · Consequences, stated plainly

- LAW-10 clause 2: *"An approval is invalidated automatically when the bound content hash changes."* `APR-012`'s binding to its subject is therefore **void as recorded**. `APR-013`, which binds `AIEF-AMD-013` itself, is unaffected and verifies.
- LAW-01: *"A frozen artifact is changed only by an approved ECR and a recorded human approval."* For whatever byte or bytes differ, that is unsatisfied, and the difference is **not recoverable** from any surviving state.
- `VER-007` C2/C3 asserted 29 of 29 verify. That assertion does not reproduce today for this one path, and does reproduce for the other twenty-eight. This instrument records the disagreement; it does not adjudicate the audit, which is a QA artifact and outside A4's reach under LAW-05.
- Root cause is **OI-V-02**: no standing check binds `FROZEN.md` to the tree. `V-24` is declared and emitted but not implemented as software, so the registry is verified only when a session chooses to verify it by hand. That is the exact exposure `ECR-D-005` recorded, and it is why this went undetected for two sessions.

### 5 · Recommendation — a recommendation, not a disposition

A4 may **recommend** on ECR-D and may not rule on it; LAW-02 requires human involvement and re-gating, and clause 5 forbids closure by the raiser. Recommended:

1. **Re-affirm** `AIEF-AMD-013`'s manifest change at the digest now registered. `APR-014` re-registers the manifest at its measured post-change value and thereby restores V-24; what it cannot do is retroactively supply the approval for the `AIEF-AMD-013` bytes. Disposition **A — re-register and re-affirm** is the `ECR-D-005` precedent and needs one human approval artifact.
2. **Commit before the next multi-session phase**, per the `S-2026-08-08-03` commit-granularity ruling that made every approval subject a recoverable git object. Had that ruling been extended to sessions `-05` onward, this would have been a two-command diff instead of a reconstruction. `VER-007` FIND-Q7-8 asked for the same thing for a different reason.
3. **Treat OI-V-02 as promoted in priority.** Two sessions of hand verification did not catch a divergence that a standing V-24 would have caught at the next boot.

`APR-014` records `prior_hash` as the **measured** `e87ae68e…` and never the unreproducible recorded value: a hash is never invented, and an approval that names a digest its subject does not carry would repeat the defect it is recording.

---

## Content Preservation Performed

The directing instruction says *preserve all information*, and permits relocation only under the declared mapping. What was relocated, and to where:

| From | To | Verification |
|---|---|---|
| The entire authoritative content of `project/OPEN_ITEMS.md` — five sections, every table, every row | `project/OPEN_ITEMS_REGISTER.md`, tier T4, cap null | Identifier sets equal: **46 in, 46 out**; zero lost, zero invented; two moved section by ruling. Every row's pre-split text carried verbatim; updates appended and attributed, never substituted |
| Two register row keys that were phrases | Compact keys, with the pre-split leading cell retained verbatim in the row's first content cell | Both phrases present in the register, character for character |
| The narrative `## Notes` of `project/STATE.md` and the long form of `next_action` | `project/STATE_REGISTER.md`, tier T4, cap null, one level-2 section per block key plus `Notes` | Every `sch-state` required field retained in `STATE.md`'s block; `tpl-current-state`'s eight required sections all present; every relocated fact reachable by the declared section-name mapping |

**Nothing was deleted, summarised or weakened.** Two identifiers were added by this session's own findings, `ECR-D-006` and `OI-C-10`. The pre-split register measured 10,065 / 12,773 at the close of `S-2026-08-08-11`; the post-split index measures a fraction of that against the same cap, and **the difference is entirely relocation, not reduction** — the register is larger after this session than before it, because this session added to it.

---

## Blast Radius

Determined by inspecting what renders each changed manifest section, following the AMD-008/AMD-009/AMD-012/AMD-013 method.

| Changed section | Rendered by | Effect |
|---|---|---|
| `metadata.reproducible.bounded_register_split` — new object | `.ai/FRAMEWORK.md` § Integrity renders DC-1's headline rule only, unchanged | **None** |
| `metadata.reproducible.budget_measurement_record.*` — one new member, two extensions | as above | **None** |
| `files[boot].token_cap` 400 → 504 | **`core/CONTEXT_TIERS.md` § *Per-file caps*** renders the cap table: it states `BOOT.md` 400, Sum 5800, Headroom 200, and is now **stale in three cells** | **New staleness, recorded.** `core` is `framework-only` write access and was **not** hand-edited. Re-emission is Stage 1 compiler work under CMP-BLOCK-004. Folded into **OI-V-07**'s class; the correct values are 504 / 5904 / 96 and are stated at §AMD-50 §4 and in `APR-014` |
| two new `files[]` entries, two new `dependencies.edges` | Nothing in `core/` renders `files[]` or `dependencies` | **None** |
| `validation[V-03].verifies`, `validation[V-09].verifies` | `core/validation/CHECKS.md` and `core/validation/MANIFEST` — Stage 5 output emitted at `S-2026-08-08-03` | **Already stale in `V-09`** (OI-V-07, from AMD-010, deepened by AMD-013); `V-03` becomes stale for the first time. Check count unchanged at **25**. Re-emission is Stage 5 compiler work under CMP-BLOCK-004 |
| `adapters/ADP-ci.md` | Already stale (OI-C-02); check count unchanged | **No new staleness** |
| `src/aief_stage6/**` | Not rendered from the manifest; it *implements* it | **Implementation delta owed**, added to OI-C-09: §AMD-51's charged aggregate comparison, which `budget.py` `measure()` does not perform; plus conformance certification of the §AMD-49 mapping now bound into V-03, the two new `files[]` entries and the amended `files[boot].token_cap`. `src/` is PR-controlled; **not performed here** — A4 does not implement what it ruled (SOD-1) |
| `tests/**` | Not rendered from the manifest; it *asserts against* it | The three assertions already recorded as stale at OI-C-09 are superseded again: the registry moves 29 → 30 and the `mutable`-file snapshots move again. Folded into OI-C-09; **not performed here** |

| Artifact | Change | Method |
|---|---|---|
| `framework/framework.manifest.json` | The eleven changes of AMD-49…AMD-51 | Surgical edit under `APR-014`; re-registered in `FROZEN.md` at the new DC-1 |
| `framework/AIEF-AMD-014_…` | **NEW** — this instrument | Registered in `FROZEN.md` under `APR-015` (AMD-21 criterion) |
| `project/FROZEN.md` | Manifest row re-registered; this instrument added, 29 → 30; aggregate recomputed under DC-2; the ECR-D-006 divergence recorded in the registration history | Registry edit under `APR-014`/`APR-015` |
| `project/OPEN_ITEMS.md` | **Becomes the bounded T1 index** | Split under §AMD-49; edited in `project-manager` role at rank-1 direction |
| `project/OPEN_ITEMS_REGISTER.md` | **NEW** — the full authoritative register | as above |
| `project/STATE.md` | **Becomes the bounded T1 index**; `frozen_set_hash`; blockers; open items; `next_action`; sibling provenance header restored | Session write |
| `project/STATE_REGISTER.md` | **NEW** — the full state detail | Session write |
| `ENGINEERING.md` | Index rows only: amendment count, §5 row, §6 Stage 6 row, §7 counts and item lists, §8 gate list | Index edit |
| `project/approvals/APR-014`, `APR-015` | **NEW** — the two recorded approvals | LAW-10 |

**Deliberately not touched:** every `.ai/core/**` byte and `.ai/adapters/**` byte · **`.ai/BOOT.md` — its content is `framework-only` write access and was not edited; §AMD-50 changes the cap in the manifest, which is where caps live, and says so** · `project/BINDING.md` (`core_digest_pin` remains `PENDING-STAGE-6`) · `project/ledger/**` (`HEAD` remains at `genesis`, `seq 0`; `L-0000001` does not exist) · `core/MANIFEST.lock` (**not created** — Stage 6 remains unauthorized, OQ-14) · the distributable (**not created**) · `src/aief_stage6/**` and `tests/**` · `spec/**`, `AIEF-FRZ-001`, AMD-001…AMD-013, both ADRs, every schema, `ECR-D-001…004` · git history, tags, author or committer identity — no commit, tag or push is made by this session, and no attribution trailer of any kind is written anywhere.

---

## Separation of Duties — Recorded Tension

`core/agents/INDEX.md`: **`chief-systems-engineer` may not implement what it approved.** This instrument was written, and its manifest, registry, register and index edits applied, by the same authority (`chief-systems-engineer · S-2026-08-08-12`) at the direction of the human owner — `core/PRECEDENCE.md` rank 1, which outranks the rank-6 agent specification. Identical in form to the departures recorded in AMD-008 through AMD-013 §§ *Separation of Duties*; identically **authorised, not erased** (SOD-1).

| | |
|---|---|
| Duty separated | A4 rules and approves; A1 implements |
| Departure | A4 both ruled and applied |
| Authority for the departure | Live human-owner instruction of `S-2026-08-08-12`, rank 1, recorded per LAW-10 in APR-014 and APR-015 |
| Narrowed, as at `S-2026-08-08-10` | The implementation delta §AMD-51 requires in `src/aief_stage6/**` was **not** performed by this session. It is added to OI-C-09 for an A1 role. A4 ruling a construction and then writing the code that implements it is the departure this table exists to bound, and it was declined here |
| Not departed from | **ECR-D-006 is raised, not disposed.** LAW-02 clause 5 forbids closure by the raiser and clause 4 requires human involvement; §AMD-53 recommends and decides nothing |
| Mitigating control | Independent cold-context `qa-engineer` audit of this session's work — open until filed. It must include independent recomputation of the §AMD-50 measurement, of the §AMD-49 mapping in both directions, and of the §AMD-53 reconstruction and its `f06125d2…` control |
| Not mitigated by | Anything this document says about itself. Under LAW-05 an authority's assertion about its own work carries no evidentiary weight — including its assertion that V-09 now passes, which is this session's own evidence about this session's own change |

---

## Approvals Required and Recorded

| Change | Approval | Bound to |
|---|---|---|
| The manifest amendment of AMD-49…AMD-51, and re-registration of the manifest in `FROZEN.md` at its post-change digest | `project/approvals/APR-014` | the post-change manifest DC-1 digest (`subject_hash`), with the **measured** pre-change digest as `prior_hash` |
| Freeze-registry addition of this document (AMD-21 criterion: authorising instrument for a change to a frozen artifact) | `project/approvals/APR-015` | this document's DC-1 digest |

AMD-52 and AMD-53 require no approval of their own: neither changes a frozen artifact. AMD-52 is a disposition and a set of register corrections; AMD-53 is a finding and a recommendation, and its authority is LAW-02 and LAW-12.

Per the AMD-16 design property, neither this document's own digest nor the post-registration DC-2 aggregate appears in this document; both live in the registry and the approval artifacts.

---

**END OF AIEF-AMD-014**
