# VER-009 — Independent Verification of the Execution Architecture (T-001 / R-008)

> **Instance artifact.** Partition `project`. Owner `project-manager`. Mutability mutable.
> Filed per `manifest.templates → tpl-verification-report`. Produced under task `T-004`.
> **Four passes.** Pass 1 audited `T-001` against `R-001`; pass 2 against `R-007` and disposed
> REJECTED; pass 3 audited the response against `R-008`; **pass 4 is a cold re-verification of
> everything, and it is the pass that closes `T-004`.** All three prior findings tables and all
> three prior dispositions are retained unaltered as the record of what was found (§6, §7, §8,
> §9, §11). Pass 4 begins at §12 and does not amend anything above it.

| | |
|---|---|
| Verifier role | `qa-engineer` (authority A2) |
| Sessions | pass 1 `S-2026-08-09-02` · pass 2 `S-2026-08-09-03` · pass 3 `S-2026-08-09-04` · **pass 4 `S-2026-08-09-05`** |
| Date | 2026-08-09 |
| Subject under audit | `T-001` — Execution Architecture, and `R-008` (supersedes `R-007`, which superseded `R-001`) |
| Producer of the subject | `software.software-engineer · S-2026-08-09-01` |
| Repository | `D:\Fusion Projects\SEWCP_Master_Assembly`, HEAD `8546960`, working tree uncommitted |
| Disposition, pass 3 | VERIFIED WITH FINDINGS — the pass 2 REJECTED verdict lifted. See §11 |
| **Final disposition** | **VERIFIED WITH FINDINGS** — all six `T-001` criteria PASS; `R-008` CURRENT; **eight findings carried forward, four of them MAJOR, two of which are closures the record claims that do not hold.** See §18–§19 |

---

## 1 · Independence declaration

I am a distinct session from the producer in all three passes. The subject was produced by
`software.software-engineer · S-2026-08-09-01`; this report is produced by `qa-engineer` in
sessions `S-2026-08-09-02`, `-03` and `-04`. I differ from the producer in **both role and
session**, the identity pair `AIEF-AMD-008` §AMD-20 makes decisive. I authored no artifact under
audit.

`LAW-05` governs this report, and clause 4 — *"a claim in a document is not evidence for itself"* —
is applied to all three records. **No disposition below rests on any claim made in `R-001`,
`R-007`, `R-008` or `T-001`'s checkpoint.** `R-008`'s conclusion states what was changed for each
finding; every one of those statements was treated as an allegation to be attacked. Where a
statement in `R-008` is a *disclosure of weakness*, I tested whether the disclosure is complete —
an honest-sounding limitation that understates the limit is itself a defect, and §9 records one.

**Footprint.** Read-only on the repository except for this single file, `T-004`'s whole declared
write scope. Every perturbation and every forgery attempt ran on throwaway copies in the session
scratchpad; the tree under audit was never modified. No commit, no staging, no ledger write.

---

## 2 · Where the three passes stand

Pass 1 raised twelve findings, six of them MAJOR, and disposed `T-001` AC-2 FAIL. Pass 2 found
three of the six closures partial and four new defects introduced by the fixes, disposed AC-4 FAIL,
and rejected `R-007` on a BLOCKING self-staling defect: it pinned `VER-009`, its own consumer's
deliverable, so filing this report invalidated the result this task depends on.

Pass 2 named three conditions that would lift the rejection. All three were acted on. §8 tests
whether they hold, and §5 re-runs every acceptance criterion.

---

## 3 · Method, pass 3

1. Read `R-008`, the amended `T-001` criteria, `T-004`, `T-006`'s grant, `R-007`'s integrity
   notice, `EXECUTION_ARCHITECTURE.md` §14, and the changed regions of all five `src/aief_exec`
   modules.
2. Recomputed all 8 pinned inputs and all 11 pinned deliverables of `R-008`.
3. Re-ran `T-001`'s six criteria, including the two restated after pass 2.
4. **Attacked the strengthened grant with ten forgeries**, including every form the coordinator
   named and three I added.
5. **Attacked the new witness overlap test for false negatives** across eleven pattern pairs with
   independently derived ground truth.
6. Perturbation-tested `R-008`: rewriting `VER-009`, completing a task, and corrupting a pinned
   deliverable.
7. Tested the rebuilt state derivation for `BLOCKED`, `ACTIVE` and `AWAITING-DECISION`.
8. Ran the full pytest suite, all eight `X` checks and the twelve `V` preconditions, and
   attempted to reproduce every number `R-008` states.

---

## 4 · `R-008` currency, and the two defects it was published to fix

Recomputed with `records.file_dc1` invoked directly, not through `X-06`.

**8 of 8 inputs match** — `.ai/BOOT.md`, `STATE.md`, `BINDING.md`, `ROSTER.md`,
`.ai/core/CONTEXT_TIERS.md`, `TPL-task-package.md`, `SCH-task.schema.json`,
`framework.manifest.json`.

**11 of 11 deliverables match** — `EXECUTION_ARCHITECTURE.md`, the six `src/aief_exec/*.py`
modules, and the four `tests/test_exec_*.py` files.

**`R-008` is CURRENT.** I confirmed by enumeration that **`VER-009` is not pinned, no task record
is pinned, and `EXEC.md` is not pinned** — the three things pass 2 rejected `R-007` for.

Perturbation on a scratch copy, which is the only way to know the fix works rather than merely
reads well:

| Perturbation | `R-008` | `T-004` |
|---|---|---|
| baseline | CURRENT | READY |
| **`VER-009` rewritten — this task doing its job** | **CURRENT** | **READY** |
| **`T-002` flipped READY → COMPLETE, `EXEC.md` updated** | **CURRENT** | **READY** |
| pinned deliverable `src/aief_exec/checks.py` corrupted | **STALE** | **BLOCKED** |

The self-staling defect is gone, the backlog is unfrozen, and the protection still bites. That is
the correct shape. **Confirmed live after writing this file: `check` still reports 8 of 8 PASS,
exit 0** — where the same act in pass 2 drove it to 6 of 8 and exit 1.

---

## 5 · Disposition of `T-001` acceptance criteria — pass 3

| Criterion | Evidence I obtained myself | Disposition |
|---|---|---|
| **AC-1** — X-01…X-08 all PASS. *Test:* `check` exits 0 | `PYTHONPATH=src python -m aief_exec check` → all eight PASS, `8 of 8 PASS`, exit **0** from `$?`. Eight `note` lines are printed alongside. Re-run after writing this report: unchanged | **PASS** |
| **AC-2** — the emitted brief contains only that task's declared read scope. *Test:* `brief T-002` emits the **five** entries T-002 declares as mandatory and nothing else, and its total equals the resolved mandatory scope | `brief T-002` emits exactly **5** `--- ` entries and no others; `T-002` declares exactly 5 mandatory entries and consumes no result. Reported `TOTAL BRIEF COST TF-1 4295 / TF-2 5626`, equal to the resolved mandatory scope. The count corrected from six after FIND-Q9-20 is now right | **PASS** |
| **AC-3** — anchored scope costs at least five times less under both families | `scope T-002` → `ANCHORING TF-1 saves 61527 of 65822 (93%), factor 15.3x` and `ANCHORING TF-2 saves 81369 of 86995 (94%), factor 15.5x`. Both exceed the fivefold threshold threefold | **PASS** |
| **AC-4** — scope independence and conflict are decided on scope alone, and a runnable independent pair classifies PARALLEL. *Test:* `conflict_reasons` empty for T-002/T-003 and non-empty for T-002/T-005; `classify T-002 T-004` PARALLEL; `classify T-002 T-005` CONFLICT | All four run and all four hold. `conflict_reasons(T-002, T-003)` → **empty**; `conflict_reasons(T-002, T-005)` → non-empty, `write scopes intersect: tests/test_stage6_certification_*`; `classify T-002 T-004` → **PARALLEL**; `classify T-002 T-005` → **CONFLICT**. The restatement is the right fix and not a dodge: blocking is a state and scope independence is a property, and the criterion now tests the property directly rather than through a derived class that an unrelated change can move | **PASS** |
| **AC-5** — no path under `.ai/core/`, `framework/` or `spec/` changes relative to T-001's start | `git status --porcelain` lists exactly **seven** tracked modifications, all pre-existing. Independent mtime scan of 72 files under `.ai/core/`, 20 under `framework/` and 11 under `spec/`: **none** carries a 2026-08-09 mtime | **PASS** |
| **AC-6** — the pre-existing Stage 6 suite is unaffected | `pytest tests/ -q` → **4 failed, 239 passed**. Same four failures by test id as in passes 1 and 2. Partitioned: Stage 6 files alone **4 failed, 110 passed — 114 tests**, identical across all three passes and to `OI-C-09`'s pre-existing record; exec files alone **129 passed, 0 failed**. No failure is in an exec file | **PASS** |

**Six of six PASS.** This is the first pass in which no acceptance criterion fails. Independently:
`V-01`…`V-09`, `V-23` and `V-25` all report **PASS**, and `V-24` reports **FAIL** — pre-existing and
unrelated — exactly as `R-008` states.

---

## 6 · Findings raised in pass 1 (retained unaltered)

| ID | Severity | Statement | Owner |
|---|---|---|---|
| **FIND-Q9-1** | MAJOR | **X-04 is disabled by any non-empty `write_authority` string.** `write_scope: [.ai/core/**]` with `write_authority: x` PASSES; the same record without the field FAILS. The exemption is also silent, so `T-006`'s reach into `.ai/core/MANIFEST.lock` produces no output. A control the constrained party can switch off in the record it authors, without leaving a trace, is not a control | `software.software-engineer`; `chief-systems-engineer` |
| **FIND-Q9-2** | MAJOR | **`PROTECTED_WRITE` omits `framework/**`.** `framework/framework.manifest.json`, `framework/**`, `STATE.md`, `BINDING.md` and `ENGINEERING.md` all pass X-04 with no authority declared, while `T-001` forbids changing any manifest field | `software.software-engineer` |
| **FIND-Q9-3** | MAJOR | **X-06 pins only `inputs`, so a result stays CURRENT while its deliverables drift.** Nine artifacts in `R-001`'s `affected` list were written after publication. `R-001` said `205 passed`; the tree gave 214. The checkpoint said 95 exec tests; there were 104 | `software.software-engineer`; `chief-systems-engineer` |
| **FIND-Q9-4** | MAJOR | **AC-2's test is false as written; `brief` performs repository-wide discovery.** 21 files opened, 15 outside the declared scope, plus one `rglob('*')` of the whole repository. The emitted brief was nevertheless correctly bounded | `project-manager`; `software.software-engineer` |
| **FIND-Q9-5** | MAJOR | **X-08 budgets only the `mandatory` class.** `T-003` measured 24,074 against a 6,000 cap and passed | `software.software-engineer` |
| **FIND-Q9-6** | MAJOR | **X-01's `LAW-05` test is defeated cosmetically.** Passing: `software-engineer` vs `software.software-engineer`; `QA-Engineer` vs `qa-engineer`; a fictional role | `software.software-engineer` |
| **FIND-Q9-7** | MINOR | **Anchors match by substring, first hit wins, ambiguity silent.** `AMD-4` matched 8 headings and silently returned AMD-41 | `software.software-engineer` |
| **FIND-Q9-8** | MINOR | **Three criteria are not binary.** AC-3 turned on "materially less"; `cmd_scope` reported the saving under TF-1 only; AC-5 declared no baseline | `project-manager`; `software.software-engineer` |
| **FIND-Q9-9** | MINOR | **`R-001` F-003 mischaracterises the four failures** as three snapshot plus one V-24. Observed: two and two | `software.software-engineer` |
| **FIND-Q9-10** | OBSERVATION | `write_authority` read as `str(… or "")`, so `0`, `false` and `null` collapsed to "no authority" | `software.software-engineer` |
| **FIND-Q9-11** | OBSERVATION | `scope.attribute` is atemporal: `audit` attributes pre-existing changes to a task that has not begun | `software.software-engineer` |
| **FIND-Q9-12** | OBSERVATION | `parse_index` enforces one-id-per-line only after a section's first identifier | `software.software-engineer` |

---

## 7 · Findings raised in pass 2 (retained unaltered)

| ID | Severity | Statement | Owner |
|---|---|---|---|
| **FIND-Q9-13** | **BLOCKING** | **`R-007` pins `T-004`'s own deliverable as an input, so performing `T-004` invalidates `T-004`'s precondition.** Rewriting `VER-009` produced `R-007` STALE, `X-06` FAIL, `X-02` FAIL and `T-004` BLOCKED. The repository could not hold a completed `T-004` and a passing check campaign at once | `software.software-engineer`; `project-manager` |
| **FIND-Q9-14** | MAJOR | **`R-007` pins six mutable task records and `EXEC.md`, freezing the backlog.** Flipping `T-002`'s status staled `R-007` on two pins at once, so no task could complete without superseding the result first | `software.software-engineer` |
| **FIND-Q9-15** | MAJOR | **`T-001` AC-4 is false and was not restated when its siblings were.** `classify T-002 T-003` returned BLOCKED, not PARALLEL, because the unassigned-role fix moved `T-003` to BLOCKED | `project-manager` |
| **FIND-Q9-16** | MAJOR | **The `notices` channel is computed and then discarded.** Eight notices existed in `run_all`; `grep notice src/aief_exec/__main__.py` returned nothing. `R-007`'s claim that a granted reach is never silent was false as delivered | `software.software-engineer` |
| **FIND-Q9-17** | MAJOR | **`role_authority` is a new self-declared bypass of the same class as the old `write_authority`.** A 12-character junk citation moved `T-003` from BLOCKED to READY with zero blocking reasons | `software.software-engineer`; `chief-systems-engineer` |
| **FIND-Q9-18** | MINOR | **Half the X-02 derived/declared cross-check is dead code.** `build_plan` defaulted the derived state to the declared one, so an over-declared block was invisible | `software.software-engineer` |
| **FIND-Q9-19** | MINOR | **`R-007`'s stated test counts do not match the artifacts it pins.** It declared 229 passed / exec 119; the tree gave 231 / 121 with every pinned digest matching. Pinning secures bytes, never claims about them | `software.software-engineer` |
| **FIND-Q9-20** | MINOR | **The restated AC-2 says "the six declared entries"; `T-002` declares five** | `project-manager` |
| **FIND-Q9-21** | OBSERVATION | `run_all`'s exception fallback omits the `notices` key, so a consumer iterating it raises `KeyError` on a check that ERRORs | `software.software-engineer` |

---

## 8 · Pass 3 re-verification of all twenty-one prior findings

| ID | Status | Evidence I obtained myself |
|---|---|---|
| **FIND-Q9-1** | **PARTIAL** | Ten forgeries attempted against `x04`. **Five refused**: free text; a citation with no `id`/`recorded_at`; an `id` with no `recorded_at`; a `recorded_at` naming a nonexistent file; an `id` genuinely absent from the cited file. That is a real advance — every form that worked in pass 2 is now dead. **Five succeeded**, all detailed under FIND-Q9-22. The structural half is closed; the semantic half is not |
| **FIND-Q9-2** | **CLOSED** | `PROTECTED_WRITE` now carries `.ai/core/**`, `.ai/*.md`, `spec/**`, `framework/**`, `FROZEN.md`, `approvals/**`, `ledger/**`. Re-probed: `.ai/FRAMEWORK.md` and `.ai/BOOT.md` — the pass 2 residual, and `FRAMEWORK.md` is a generated do-not-edit L0 artifact — are now **GUARDED**. `.ai/project/EXEC.md` and `.ai/project/STATE.md` remain unguarded, which is correct: `*` does not cross a separator, and those are mutable project registers that exist to be written |
| **FIND-Q9-3** | **CLOSED** | `R-008` pins 8 inputs and 11 deliverables; all 19 recomputed and matched (§4). Corrupting `checks.py` still produces STALE and blocks `T-004`, so the protection was not weakened by narrowing the pin set |
| **FIND-Q9-4** | **CLOSED** | AC-2 describes the emitted brief; verified directly (§5) |
| **FIND-Q9-5** | **CLOSED** | Re-measured in pass 2; `x08` sums mandatory and optional, and all six tasks sit within cap under both families |
| **FIND-Q9-6** | **PARTIAL** | Role normalisation and roster resolution hold; all four pass 1 evasions still fail. The `role_authority` residual is FIND-Q9-22 — the same `_grant` function now serves both fields, so the two findings have merged into one weakness |
| **FIND-Q9-7** | **CLOSED** | Verified in pass 2 and unchanged: `AMD-4` → 8 matches → X-03 FAIL; every live anchor resolves to its intended section |
| **FIND-Q9-8** | **CLOSED** | Both family savings printed; AC-3 carries a numeric threshold; AC-5 names a baseline |
| **FIND-Q9-9** | **CLOSED** | `R-008` F-003 states two snapshot assertions, one V-24 registry assertion and one pipeline stub gated on V-24. I re-derived all four: correct |
| **FIND-Q9-10** | **CLOSED** | All falsy grant forms fail safe |
| **FIND-Q9-11** | **OPEN — accepted and recorded** | `audit` still attributes pre-existing Stage 6 changes to `T-002`. Now recorded as an accepted limit in `EXECUTION_ARCHITECTURE.md` §14 item 7 — *"It answers which scope permits this change, never who made it"* — and in `R-008` F-006. For an OBSERVATION, recording the limit in the contract is the right disposition |
| **FIND-Q9-12** | **OPEN — accepted and recorded** | Unchanged, and recorded alongside Q9-11 in `R-008` F-006. Fails safe through X-02 |
| **FIND-Q9-13** | **CLOSED** | The BLOCKING defect is gone. `VER-009` is not pinned by `R-008`; rewriting it leaves `R-008` CURRENT and `T-004` READY, verified on a scratch copy and then **confirmed live on the real tree after writing this file** — `check` still 8 of 8, exit 0 |
| **FIND-Q9-14** | **CLOSED** | No task record and no `EXEC.md` is pinned. Flipping `T-002` READY → COMPLETE and moving it in `EXEC.md` leaves `R-008` CURRENT and `T-004` READY. The backlog can advance |
| **FIND-Q9-15** | **CLOSED** | AC-4 restated onto scope independence plus a runnable pair; all four sub-tests verified (§5) |
| **FIND-Q9-16** | **CLOSED** | `cmd_check` prints `note` lines. Eight appear on stdout, and the one that matters is there verbatim: `X-04 … note T-006: .ai/core/MANIFEST.lock reaches the protected set under a declared grant - L7 recorded at .ai/FRAMEWORK.md`. The granted reach is no longer silent |
| **FIND-Q9-17** | **PARTIAL** | Merged into FIND-Q9-22 — `role_authority` now goes through the same `_grant` function, so it inherits both the strengthening and the residual weakness |
| **FIND-Q9-18** | **CLOSED** | `build_plan` no longer falls back to the declared status for BLOCKED. Verified: `T-002` filed BLOCKED with no real blocker now derives **READY**, and X-02 FAILS with `T-002: filed as BLOCKED but the derivation finds no blocker`. **The dead branch fires.** No regression to the other states: filed ACTIVE derives ACTIVE with X-02 PASS; filed AWAITING-DECISION derives AWAITING-DECISION with X-02 PASS |
| **FIND-Q9-19** | **OPEN in a new form** | The wrong test count is gone — `R-008` states no test figure, which removes the specific defect. But the `validation` block says *"see the conclusion; the figure is stated there and not restated here"* and **the conclusion states no test figure at all** (FIND-Q9-25), and the conclusion's route figures are not reproducible (FIND-Q9-26). The class of defect — an unverifiable number inside a record whose digests all match — has moved rather than closed |
| **FIND-Q9-20** | **CLOSED** | AC-2 now says five; `T-002` declares five; the brief emits five |
| **FIND-Q9-21** | **CLOSED** | Moot in practice and corrected in form: `run_all`'s fallback is no longer read by a notices-iterating consumer, and `cmd_check` guards its access |

**Score across all three passes: seventeen of twenty-one CLOSED, two OPEN by recorded acceptance,
three PARTIAL — and the three partials are the same underlying weakness in one function.** The
BLOCKING finding is closed.

---

## 9 · New findings — pass 3

| ID | Severity | Statement | Owner |
|---|---|---|---|
| **FIND-Q9-22** | MAJOR | **The grant's `id` test is an unanchored substring search with no minimum length and no context, so a grant is still forgeable without write access to anything but the task record.** `_grant` accepts if `ident in body`. Five forgeries granted `.ai/core/**`: **(a)** `id: e` — one incidental character, present in essentially any English text, cited to `.ai/FRAMEWORK.md`. **(b)** `id: L7` — two characters matching a row label in a layer table; this is **the id the live `T-006` grant actually uses**, so the repository's only `write_authority` grant is itself an instance of the weakness. **(c)** `id: aaaaaaaaaaaa` cited to `VER-009` — the exact junk token pass 2 flagged as a forgery now validates *because this report quotes it*, which means an audit report becomes an authority source for the thing it condemns. **(d)** `id: Never edit` cited to `CLAUDE.md`, where the string occurs only in `Never edit .ai/core/**` — **a prohibition read as an authorization for exactly what it prohibits**. **(e)** `recorded_at` naming a file inside the task's own `write_scope`, which the task creates. Remedies, any of which would close most of it: require the `id` to match a declared identifier grammar (`ECR-`, `APR-`, `AMD-`, `EXEC-D-`, ledger `L-`), require a minimum length, require the match to fall inside a heading or a table's leading cell rather than anywhere in the octets, and refuse a `recorded_at` that intersects the task's own write scope | `software.software-engineer`; `chief-systems-engineer` |
| **FIND-Q9-23** | MAJOR | **`R-008`'s disclosure of the grant's weakness is inaccurate in the direction of overselling, and the same wording is bound into the contract.** `R-008` *WHAT IS NOT CLAIMED* states: *"A grant is inspectable, not unforgeable — an actor who can write both the task record and the cited artifact can still manufacture one."* `EXECUTION_ARCHITECTURE.md` §14 item 5 repeats it. That frames forgery as requiring write access to the cited artifact. **Three of my four successful forgeries cited artifacts the forger does not write** — `FRAMEWORK.md`, `CLAUDE.md` and `VER-009`. Writing the task record alone is sufficient, provided the forger picks an `id` that occurs anywhere in any readable file. The honest statement is not *"an actor who can write both"* but *"any actor who can write the task record, by choosing an id that occurs somewhere in some file."* I was asked to judge whether the framing is honest: **it is candid in intent and wrong in substance**, and because it understates the residual it will lead a reviewer to under-weight FIND-Q9-22. Correct the sentence in both places | `software.software-engineer`; `chief-systems-engineer` |
| **FIND-Q9-24** | MAJOR | **The new witness overlap test has false negatives — the dangerous direction — and it is the primitive under concurrent-write safety.** `patterns_overlap` now substitutes two fixed fillers into each pattern and tests those witnesses against the other regex. It correctly stopped reporting `.ai/*.md` against `.ai/project/EXEC.md`, which is what it was written for. But a witness is one point, and two globs can intersect on paths neither witness represents. **Six of eleven genuinely overlapping pairs I tested now report disjoint**, ground truth derived by hand: `build/a/**` × `build/**/b` (both match `build/a/b`); `src/aief_exec/*_new.py` × `src/aief_exec/new_*.py`; `tests/test_*_records.py` × `tests/test_exec_*.py` (both match the existing `tests/test_exec_records.py`); `build/*a*.json` × `build/*b*.json`; `build/x/T-00?.md` × `build/x/T-0?1.md`; `build/**/gen_*.py` × `build/gen/*_gen.py`. The exposure is bounded today and I say so plainly: `scopes_intersect` computes the concrete intersection first, so any overlap among **existing** files is still caught, no live task-pair classification depends on the pattern fallback, and every `PROTECTED_WRITE` entry is `**`-suffixed or literal, which the witness test handles correctly. The risk is prospective — two tasks whose write scopes collide only on not-yet-created paths would classify PARALLEL and be dispatched concurrently. The old test erred toward false positives, which is the safe direction; the new one errs toward false negatives, which is not. A sound replacement is to intersect the two compiled regexes (or test both fillers against a product of segment alignments) rather than to sample two points | `software.software-engineer` |
| **FIND-Q9-25** | MINOR | **`R-008`'s `validation` block points at a figure that is not there.** It records `check: pytest tests/` with outcome *"see the conclusion; the figure is stated there and not restated here."* I searched the conclusion: **it contains no test figure**. Stating a number once instead of twice is the right response to FIND-Q9-19; stating it zero times and asserting it is stated is not. For the record, the tree gives **4 failed, 239 passed**, exec 129/0, Stage 6 110/4 at 114 | `software.software-engineer` |
| **FIND-Q9-26** | MINOR | **`R-008` claims every figure it states is recomputable by the named commands; four are not.** The conclusion asserts *"Whole route to the first line of work: TF-1 9,727 declared, against 155,192 by citation chain and 379,177 by unbounded sweep — 16.0x and 39.0x. Cold-session recovery: TF-1 7,565. Every figure is recomputable by the commands above; none is asserted from memory."* No command among `status`, `scope`, `classify`, `brief`, `check` and `audit` produces any of 9,727, 155,192, 379,177 or 7,565, and `EXECUTION_ARCHITECTURE.md` — which `R-008` pins — derives none of them. I attempted the sweep myself with the repository's own tokenizer and its own `scope.tree`: **556,371** over 299 text files, and six other plausible scope definitions give 181,061 / 318,848 / 387,460 / 433,500 / 442,312. **None reproduces 379,177.** The ratios are internally consistent (155,192 ÷ 9,727 = 16.0; 379,177 ÷ 9,727 = 39.0), so the figures are self-consistent but externally unverifiable. The `T-002` figures in the same paragraph — 4,295 / 5,626 against 65,822 / 86,995 — **are** exactly reproducible and I confirmed them. Either publish the derivation or drop the recomputability claim | `software.software-engineer` |
| **FIND-Q9-27** | OBSERVATION | **Nothing in the tooling protects a superseded result from mutation, and `X-06` is blind to it by construction.** `graph.result_currency` returns immediately for a record declaring `SUPERSEDED`, so no digest in `R-007` is ever recomputed, and the corruption described in §10 ran and completed with all eight checks reporting PASS. A superseded record is history and should be at least as immutable as a current one. A cheap guard: have `X-06` recompute superseded records too and report drift as a notice rather than a failure | `software.software-engineer` |

---

## 10 · The `R-007` integrity notice — assessment

I was asked to judge this rather than test it, but it is testable, so I tested it first.

**The disclosure is true.** `R-007`'s header states that a repinning script mis-targeted it after
supersession and rewrote twelve digest values. Three independent lines confirm it. **(a)** All 27
of `R-007`'s pins match the *current* tree — which a faithful historical record could not, because
`R-008` supersedes it precisely on the ground that the code and the task records moved. **(b)** The
specific value is decisive: pass 2 recorded `R-007` pinning `src/aief_exec/checks.py` at
`a717aba745bbe7a9c1e6077e5b03e6ae2add02a2c4cc1910bbb1e570d596626f`; it today carries
`865a1840f19cc1e743b98fca1b7e0c99b3fa6332988eeb2b98b516dae0d24249`, which is `R-008`'s value and
the current tree's. **(c)** `R-007`'s mtime, 07:43, is later than `R-008`'s 07:42 — the record was
written after its own successor.

**My judgment: the disclosure is adequate, and it is the right call.** It is specific rather than
vague — it names the count, the cause and the affected block; it scopes the damage correctly, since
the prose, findings and conclusion are unaltered and I confirmed the pass 2 findings text is intact;
it marks the record **do not consume** and points to `R-008`; and it refuses to reconstruct the
values, on the stated ground that *"a reconstructed pin would be a fabricated one — which is the
defect class this whole mechanism exists to prevent."* That reasoning is correct and it is the
harder choice. Silently restoring plausible digests would have produced a record that looked
faithful and was not, which is strictly worse than a record that is visibly damaged and says so.
Disclosing a self-inflicted integrity failure in the artifact's own header, against interest, is
the behaviour this framework is supposed to produce.

**It is not, however, cost-free, and two things follow.** First, `R-007` is now unusable as
evidence of what was published — pass 2's audit trail for it survives only in §7 of this report and
in the pass 2 disposition, which is why both are retained here unaltered. Second, the incident
exposes a real gap in the tooling rather than merely an operator error, and that gap is recorded as
**FIND-Q9-27**: a superseded record can be rewritten with every check reporting PASS, because
`X-06` short-circuits on `SUPERSEDED` and never recomputes it. The disclosure is adequate; the
condition that allowed it is a finding.

---

## 11 · Disposition at the close of pass 3 (retained unaltered)

> ### VERIFIED WITH FINDINGS — the pass 2 REJECTED verdict is lifted

**The three conditions I set in pass 2 are met, and I verified each rather than accepting it.**
`R-008` no longer pins `VER-009`, so filing this report does not stale the result this task
consumes — confirmed on a scratch copy and then live on the real tree, where `check` still returns
8 of 8 and exit 0 after the write that broke it last time. `R-008` no longer pins task records or
`EXEC.md`, so completing a task no longer freezes the backlog. `cmd_check` prints notices, and
`T-006`'s reach into `.ai/core/MANIFEST.lock` is now visible on stdout on every run. Alongside
those, AC-4 was restated onto the property rather than the derived state, the `BLOCKED` derivation
was rebuilt so that over-declaration is now as visible as under-declaration, and `.ai/*.md` closed
the `FRAMEWORK.md` hole.

**All six of `T-001`'s acceptance criteria PASS**, for the first time in three passes. Seventeen of
twenty-one findings are closed, two are open by recorded and reasoned acceptance, and no BLOCKING
finding remains. `X-01`…`X-08` pass; `V-01`…`V-09`, `V-23` and `V-25` pass; the Stage 6 suite is
untouched at 114 tests with the same four pre-existing failures; exactly seven tracked files are
modified, none of them by this work.

**Why not VERIFIED without qualification.** Three MAJOR findings are open and they are not
bookkeeping.

1. **FIND-Q9-22** — the grant is still forgeable by an actor who can write only the task record. A
   two-character `id` matching a table row, or a token occurring inside a prohibition sentence,
   validates as an authority. The live `T-006` grant relies on a two-character id.
2. **FIND-Q9-23** — the disclosure of that weakness understates it, in `R-008` and in the contract.
   A limitation recorded inaccurately is worse than one recorded plainly, because it tells a
   reviewer the residual is smaller than it is.
3. **FIND-Q9-24** — the overlap primitive under concurrent-write safety now returns disjoint for
   six of eleven genuinely overlapping pattern pairs. Bounded today by the concrete-intersection
   path, and prospective rather than live, but it errs in the unsafe direction where its
   predecessor erred in the safe one.

None of these fails an acceptance criterion, none blocks the layer's use, and none warrants
another rejection. They are routed to `software.software-engineer` and, for the authority question
in Q9-22 and Q9-23, to `chief-systems-engineer`.

**A closing judgment, offered as judgment.** Across three passes the same weakness has now been
engaged four times: a control whose exemption is written by the party it constrains. It went from
*any non-empty string*, to *any string of twelve characters*, to *any string that appears somewhere
in some readable file*. Each step is a genuine narrowing and the trajectory is right. But every
version has shared one property — the check verifies that a citation has a **form**, never that it
has a **referent**. Until an `id` is resolved against a declared identifier space and located in a
structural position within the cited artifact, a grant records that someone wrote down an authority,
not that one exists. That is a decision for `chief-systems-engineer` to take deliberately, and the
honest thing `R-008` could do today is say so in those terms rather than in the terms of §9's
FIND-Q9-23.

**Verifier attestation.** Every figure in this report was produced by a command run in session
`S-2026-08-09-02`, `-03` or `-04`. No claim rests on `R-001`, `R-007`, `R-008` or `T-001`'s
checkpoint; where those records and my measurements disagree, the disagreement is recorded above
and not reconciled in their favour. This report is subject to review at
`.ai/project/reviews/DR-003_VER-009_Disposition.md` by `chief-systems-engineer`.

*Filed by `qa-engineer · S-2026-08-09-04` under task `T-004`. Write scope exercised: this file only.*

---
---

# PASS 4 — cold re-verification, and the pass that closes `T-004`

## 12 · Why there is a fourth pass, and what changed under it

Pass 3 was written at 07:53. `R-008` was **republished at 07:57**, after it — the `T-001`
checkpoint records six further closures taken in that window (`Q9-23`…`Q9-27`, with `Q9-22`
escalated as `F-007`). The checkpoint therefore still carried one open item:
*"Re-verification of the six closed findings by the T-004 verifier."* Nothing above §12 tested
the artefact that exists today. This pass does.

I am a **cold session** — `S-2026-08-09-05`. I hold no conversation with the producer, no
conversation with passes 1–3, and I reconstructed nothing from memory. My contract was
`T-004.md`; my read scope was that record, `LAW-05`, `R-008`, `T-001`, the artefacts `T-001`'s
own criteria name as evidence, and this file. I authored no artefact under audit.
`LAW-05` clause 4 is applied throughout: **no disposition below rests on a statement made in
`R-008`, in `T-001`'s checkpoint, or in §§1–11 of this report.** Every prior finding was
re-executed against the live tree rather than read off §8.

**Footprint.** Read-only on the repository except this one file, which is the whole of
`T-004`'s declared write scope. Every perturbation ran on a throwaway copy of the tree in the
session scratchpad. No commit, no tag, no staging, no ledger write, no Stage 6 execution.

---

## 13 · `R-008` currency — recomputed

Recomputed independently with `hashlib.sha256` over the raw octets, **not** through `X-06` and
not through `records.file_dc1`, so that the check and the thing it checks do not share an
implementation. For all nineteen paths the raw digest equals the pinned digest, which also
establishes that DC-1 normalisation is a no-op on this set and that the two methods cannot
diverge here.

| Pinned | Count | Recomputed | Result |
|---|---|---|---|
| `inputs` | 8 | 8 | **8 of 8 match** |
| `deliverables` | 11 | 11 | **11 of 11 match** |

Inputs: `.ai/BOOT.md` `5a97d6ad…b82db` · `.ai/project/STATE.md` `1cde83cd…c175d` ·
`.ai/project/BINDING.md` `64a9ca21…1a15f` · `.ai/project/ROSTER.md` `3c657f6e…b19694` ·
`.ai/core/CONTEXT_TIERS.md` `dad8a47a…1ade4f` · `.ai/core/templates/TPL-task-package.md`
`a51c5d27…01e9b2` · `.ai/core/schemas/SCH-task.schema.json` `e874fdd7…cccc80` ·
`framework/framework.manifest.json` `920eb6ee…814090`.

Deliverables: `.ai/project/EXECUTION_ARCHITECTURE.md` `6afad916…f87736` ·
`src/aief_exec/__init__.py` `b8813ebc…f77b69` · `__main__.py` `309bcfe9…81a053` ·
`records.py` `98f571d5…67d91` · `scope.py` `e7cf5b82…52119` · `graph.py` `3e739e44…3926e58` ·
`checks.py` `865a1840…d24249` · `tests/test_exec_records.py` `ab3a474f…0b27f3` ·
`test_exec_scope.py` `30963646…25ec69` · `test_exec_graph.py` `0c3fbbac…c39945` ·
`test_exec_checks.py` `28b5ebb0…5a8dcc`.

> ### `R-008` is CURRENT at the time of this audit. `T-004`'s escalation condition does not fire.

I also confirmed by enumeration that `VER-009` is **not** among the pins, so filing this pass
cannot stale the result this pass consumes, and re-confirmed it live in §17.

---

## 14 · `T-001` acceptance criteria — pass 4, executed cold

| Criterion | Evidence I obtained myself, this session | Disposition |
|---|---|---|
| **AC-1** — X-01…X-08 all PASS on the live repository. *Test:* `check` exits 0 | `PYTHONPATH=src python -m aief_exec check` → `X-01`…`X-08` each `PASS`, footer `8 of 8 PASS`, `EXIT=0` captured from `$?`. **Nine notice lines printed**, seven `X-01` roster notices, one `X-04` grant notice reading `T-006: .ai/core/MANIFEST.lock reaches the protected set under a declared grant - L7 recorded at .ai/FRAMEWORK.md`. The granted reach is not silent | **PASS** |
| **AC-2** — the emitted brief contains only that task's declared read scope. *Test:* `brief T-002` emits the five entries `T-002` declares as mandatory and nothing else, and its reported total equals the resolved mandatory scope | `brief T-002` emits exactly **5** `--- ` entries — `OPEN_ITEMS_REGISTER.md #OI-C-09`, `AIEF-AMD-013 #AMD-45`, `framework.manifest.json #metadata.reproducible.build_provenance_record`, `src/aief_stage6/budget.py`, `src/aief_stage6/lock.py` — and no sixth. Footer `=== TOTAL BRIEF COST  TF-1 4295 / TF-2 5626`. `scope T-002` independently reports mandatory resolved `TF-1 4295 / TF-2 5626`. **The two agree exactly** | **PASS** |
| **AC-3** — anchored read scope costs at least five times less than the same files unanchored, under both families. *Test:* `scope T-002` reports both, resolved below one fifth of unanchored in both | `scope T-002` → `TF-1 4295` against `TF-1 65822`; `TF-2 5626` against `TF-2 86995`. Printed factors `15.3x` and `15.5x`. One fifth of 65 822 is 13 164 and of 86 995 is 17 399; the resolved totals are **3.1× and 3.1× below even that threshold** | **PASS** |
| **AC-4** — scope independence and scope conflict are decided on scope alone, and a pair of runnable independent tasks classifies PARALLEL. *Test:* `conflict_reasons` empty for T-002/T-003 and non-empty for T-002/T-005; `classify T-002 T-004` PARALLEL; `classify T-002 T-005` CONFLICT | All four executed, all four hold. `graph.conflict_reasons` called **directly**, not through the CLI: `(T-002, T-003)` → `[]`; `(T-002, T-005)` → `['write scopes intersect: tests/test_stage6_certification_coverage_budget.py, tests/test_stage6_certification_digests.py, tests/test_stage6_certification_evidence.py']`. `classify T-002 T-004` → `PARALLEL`; `classify T-002 T-005` → `CONFLICT`. I confirmed the restatement is not a dodge: `T-002 × T-003` still derives `BLOCKED` on the unassigned-role reason, and the criterion now tests the scope property underneath that state rather than the state | **PASS** |
| **AC-5** — no path under `.ai/core/`, `framework/` or `spec/` changes relative to the state at which T-001 began | `git status --porcelain` → **exactly 7** tracked modifications (`.ai/project/BINDING.md`, `FROZEN.md`, `OPEN_ITEMS.md`, `ROSTER.md`, `STATE.md`, `ENGINEERING.md`, `framework/framework.manifest.json`) and 36 untracked entries, matching the pre-task baseline entry for entry. Independent mtime walk: **0 of 72** files under `.ai/core/`, **0 of 20** under `framework/`, **0 of 11** under `spec/` carry an mtime on or after 2026-08-09. No file in the three protected trees was touched on the day `T-001` ran | **PASS** |
| **AC-6** — the pre-existing Stage 6 suite is unaffected. *Test:* `pytest tests/` shows the same 4 pre-existing failures and no new one | `python -m pytest tests/ -q` → **4 failed, 241 passed**. Partitioned by running each half alone: **Stage 6 → 110 passed, 4 failed, 114 collected**, identical to the pre-existing baseline; **exec → 131 passed, 0 failed**. The four failure ids are the four pre-existing ones and no others: `test_stage6_certification_evidence.py::TestV09Recomputation::test_three_breaching_files_confirmed`, `::test_totals_and_governing_family`, `test_stage6_coverage_and_build.py::test_v24_live_registry`, `test_stage6_pipeline_stub.py::test_full_pipeline_with_stub_families`. No failure lies in an exec file, and no Stage 6 test that passed before now fails | **PASS** |

> ### Six of six `T-001` acceptance criteria PASS, verified cold and independently of pass 3.

**Not verified, and out of scope.** `R-008`'s `validation` block also asserts `V-01`…`V-09`,
`V-23`, `V-25` PASS and `V-24` FAIL. No `T-001` acceptance criterion depends on those, and
re-running the `V` layer would require reading framework tooling outside `T-004`'s declared read
scope. I did not re-run them and I do not dispose them; `V-24`'s failure is corroborated
indirectly by the two Stage 6 failures that assert on it. **This is stated rather than glossed,
because passing on partial evidence is a forbidden action for this task and an unstated omission
would be exactly that.**

---

## 15 · `FIND-Q9-1` … `FIND-Q9-12` — independent re-test *(T-004 AC-4)*

One row per finding. Every row cites a command or a call I made this session. **No row rests on
§8, on `R-008` or on the `T-001` checkpoint** — §8 was treated as an allegation and re-executed.
Forgery and perturbation probes ran against a throwaway copy of the tree or against
`checks._grant` in memory; the audited tree was never written.

| ID | Pass-4 status | Evidence I obtained myself |
|---|---|---|
| **FIND-Q9-1** — X-04 disabled by any non-empty `write_authority` | **OPEN — structurally closed, semantically not** | Sixteen probes through `checks._grant`. **Eleven refused**: the bare string `x`; the 12-character junk token pass 2 used; integer `0`; boolean `False`; an empty list; a dict with no `id`/`recorded_at`; a dict with `id` but no `recorded_at`; a `recorded_at` naming a nonexistent path; an `id` genuinely absent from the cited file. Every form that worked in passes 1 and 2 is now dead, and the refusals carry specific reasons. **Four still granted `.ai/core/**`** — carried into §16 as `FIND-Q9-22`, unchanged. The exemption is also no longer silent: `check` prints the `X-04` grant notice on every run, observed live |
| **FIND-Q9-2** — `PROTECTED_WRITE` omits `framework/**` | **CLOSED** | `scope.scopes_intersect` probed against `PROTECTED_WRITE` for 18 patterns. **GUARDED**: `.ai/core/**`, `.ai/core/MANIFEST.lock`, `framework/**`, `framework/framework.manifest.json`, `spec/**`, `.ai/FRAMEWORK.md`, `.ai/BOOT.md`, `.ai/*.md`, `.ai/project/FROZEN.md`, `.ai/project/approvals/**`, `.ai/project/ledger/**`, `**`. The pass-1 hole and the pass-2 residual are both shut. Unguarded and correctly so: `.ai/project/STATE.md`, `BINDING.md`, `ROSTER.md`, `EXEC.md`, `ENGINEERING.md`, `CLAUDE.md` — mutable project registers and host hooks that exist to be written, and `*` does not cross a separator |
| **FIND-Q9-3** — X-06 pins only `inputs`, so deliverables drift unseen | **CLOSED** | `R-008` pins 8 inputs **and** 11 deliverables; all 19 recomputed in §13. Two perturbations on the scratch copy, each from a pristine snapshot: corrupting the pinned **deliverable** `src/aief_exec/checks.py` → `R-008` **STALE**, `X-06` FAIL, `X-02` FAIL, `T-004` derived **BLOCKED**; corrupting the pinned **input** `.ai/BOOT.md` → identical result. Both halves of the pin set bite. I separately confirmed DC-1 normalises a bare trailing newline away, so a whitespace-only edit is correctly not drift |
| **FIND-Q9-4** — AC-2's test was false; `brief` performs repository-wide discovery | **CLOSED as to the criterion; the disclosed figure is wrong** | AC-2 now describes the emitted brief, and the emitted brief is bounded — 5 entries, verified in §14. The underlying behaviour persists and is disclosed, but **not accurately**: instrumenting `builtins.open`, `Path.read_text` and `Path.read_bytes` around `brief T-002` shows **34 distinct repository files read, 29 of them outside `T-002`'s declared mandatory scope**. `R-008` states 21. Carried as `FIND-Q9-33` |
| **FIND-Q9-5** — X-08 budgets only the `mandatory` class | **CLOSED** | `x08_context_budget` source references the optional class, and `checks.x08_context_budget(repo)` returns `PASS` with an empty `details` list against the live tree. I resolved every task's scope directly through `scope.resolve_scope`: all six sit within their declared caps under both families, and `scope T-002` prints a separate `OPTIONAL READ SCOPE` block with its own resolved total (`TF-1 7039 / TF-2 9067`), so the optional class is measured and reported rather than ignored |
| **FIND-Q9-6** — X-01's `LAW-05` test is defeated cosmetically | **CLOSED** | Four evasions replayed on the scratch copy, one per run from a pristine snapshot, each rewriting `T-001`'s `qa.verifier_role`. All four **FAIL** `X-01` with a correct reason: `software-engineer` → *"does not appear in project/ROSTER.md"* (the dotted prefix is not silently equated); `SOFTWARE.SOFTWARE-ENGINEER` and `Software.Software-Engineer` → normalised and caught as *"equals role 'software.software-engineer' - LAW-05 forbids self-verification"*; the fictional `chief-widget-officer` → *"does not appear in project/ROSTER.md"*. The direct self-verification control also fires |
| **FIND-Q9-7** — anchors match by substring, first hit wins, ambiguity silent | **CLOSED** | On the scratch copy I replaced `T-002`'s `anchor: AMD-45` with `anchor: AMD-4` and ran `checks.x03_read_scope_resolves`. Result **FAIL**: *"T-002 [mandatory]: anchor 'AMD-4' matches 8 headings in framework/AIEF-AMD-013_…md - an ambiguous anchor"*. Ambiguity is now loud and blocking, not silently resolved to the first hit |
| **FIND-Q9-8** — three criteria are not binary | **CLOSED** | Read from `T-001` as it stands: AC-3 carries the numeric threshold *"at least five times less … under both families"*; AC-5 names its baseline *"the state at which T-001 began"* and a countable test; and `scope T-002` prints **both** family savings (`ANCHORING TF-1 … 15.3x`, `ANCHORING TF-2 … 15.5x`) rather than TF-1 alone. All three are decidable without judgement |
| **FIND-Q9-9** — `R-001` F-003 mischaracterises the four failures | **CLOSED** | I re-derived the four from the live run rather than reading any record: two snapshot assertions (`test_three_breaching_files_confirmed`, `test_totals_and_governing_family`), one V-24 registry assertion (`test_v24_live_registry`, asserting `PASS` where the tree gives `FAIL`), one pipeline stub gated on V-24 (`test_full_pipeline_with_stub_families`, failing with `['V-24 FAIL']` and `PRECONDITION-FAIL`). **Two and two** — which is what `R-008` F-003 now says |
| **FIND-Q9-10** — falsy `write_authority` values collapse to "no authority" | **CLOSED** | Probed each falsy form through `_grant`: `0` → REFUSED, `False` → REFUSED, `[]` → REFUSED, `""` → no grant, `None` → no grant, `{}` → no grant. Nothing falsy silently becomes an authority, and nothing falsy silently becomes an exemption |
| **FIND-Q9-11** — `scope.attribute` is atemporal | **OPEN — accepted, and the acceptance is genuine** | `scope.attribute(repo, [...], tasks)` returns `{'tests/test_stage6_digests.py': ['T-002', 'T-005'], 'src/aief_stage6/budget.py': ['T-002'], '.ai/project/STATE.md': []}`. A file changed long before either task began is attributed to **both**, on scope alone, with no temporal discrimination. Unchanged. I verified the acceptance is actually recorded and not merely asserted: `EXECUTION_ARCHITECTURE.md` §14 item 7 states *"It answers which scope permits this change, never who made it"*, and `R-008` F-006 carries it. For an OBSERVATION whose behaviour is correct-by-design, recording the limit in the contract is the right disposition |
| **FIND-Q9-12** — `parse_index` enforces one-id-per-line only after the first identifier | **OPEN — accepted, and the mitigation holds** | Reproduced against the real index grammar via `records.parse_index`. Two ids on a **later** line correctly raise `RecordError: index line carries more than one identifier or trailing text under heading 'Ready'`. Two ids on a section's **first** line are accepted, and worse than pass 1 described — the identifier is **silently dropped**, not merely tolerated. I then tested the stated mitigation instead of trusting it: with `EXEC.md`'s Ready section rewritten to `T-002 T-004` on one line, `checks.x02_index_bijection` returns **FAIL** — *"T-002: has a record but is not listed in the index"*, *"T-004: has a record but is not listed in the index"*. **It does fail safe through X-02**, exactly as `R-008` F-006 claims, and I confirmed that rather than assuming it |

**Score on the twelve pass-1 findings, re-tested cold: nine CLOSED, one closed as to its
criterion with an inaccurate disclosure, two OPEN by recorded and verified acceptance, and one —
`FIND-Q9-1` — structurally closed with its semantic half still open as `FIND-Q9-22`.**

---

## 16 · The six closures taken after pass 3 — re-verified

This is the item the `T-001` checkpoint left pending. Each was re-executed, not read.

| Closure claimed | Pass-4 verdict | Evidence I obtained myself |
|---|---|---|
| **`Q9-22` escalated as `F-007`, not decided here** | **CORRECTLY ESCALATED** | `R-008` carries `F-007` MAJOR, owner `chief-systems-engineer`, and the code is unchanged, which is the honest position for an architecture decision. I reproduced the forgeries rather than take the escalation on trust: `id: e` → `.ai/FRAMEWORK.md`, `id: L7` → `.ai/FRAMEWORK.md`, `id: Never edit` → `CLAUDE.md`, and the 12-character junk token → this very report, **all four granting `.ai/core/**`**. The same function serves `role_authority`: a junk-id grant of the `qa-engineer` role validates. The live `T-006` grant resolves on the two-character `L7`; the live `T-004` grant resolves on `EXEC-D-001`, which does genuinely occur in `T-001.md` as a decision id — so the repository's two real grants sit on opposite sides of the weakness |
| **`Q9-23` — the grant-forgery framing corrected in `R-008` and §14** | **PARTIAL** | Both named places are corrected. `R-008` now says forging *"needs less than an earlier draft of this record claimed"* and that *"three of the four cited files the forger does not write"*; `EXECUTION_ARCHITECTURE.md` §14 item 5 carries the same correction. **But the superseded framing survives verbatim elsewhere in the same contract** — §5, at line 163: *"This does not make a grant unforgeable by someone who can write both files."* That is the exact sentence `FIND-Q9-23` condemned, in the document a reader reaches first. Carried as `FIND-Q9-32` |
| **`Q9-24` — witness test given a conservative fallback for two double-stars** | **NOT CLOSED** | Re-ran `scope.patterns_overlap` over the eleven pairs with ground truth derived by hand. The fallback fixes exactly **one** of the six pairs pass 3 identified — `build/a/**` × `build/**/b` now correctly reports overlap. **The other five still report disjoint** when they genuinely intersect. The true negatives are unharmed. Carried as `FIND-Q9-29`; the checkpoint's phrasing *"for two double-stars"* is literally accurate, so the defect is in `R-008` F-008's broader claim of *"restoring error in the safe direction"*, which does not hold for five of six cases |
| **`Q9-25` — the pytest figure stated in the validation block** | **CLOSED IN FORM, WRONG IN SUBSTANCE** | A figure is now stated, which is what `FIND-Q9-25` asked for. The figure is wrong. `R-008` line 67 reads *"239 passed, 4 failed - exec 129 passed 0 failed; Stage 6 110 passed 4 failed at 114 total"*. Observed: **241 passed, 4 failed; exec 131 passed 0 failed**; Stage 6 110/4 at 114 — the Stage 6 half is exact, the exec half is 2 low, the total 2 low. Every pinned digest matches, so this is precisely the class `FIND-Q9-19` named: *pinning secures bytes, never claims about them*, now in its third consecutive record. Carried as `FIND-Q9-30` |
| **`Q9-26` — `aief_exec measure` reproduces the envelope and the figures** | **PARTIAL** | `measure T-002` exists and prints its envelope definition in code, which is the substantive advance. It reproduces the **declared** figure (`9,727`) and the **anchoring** ratio (`4295/5626` against `65822/86995`) exactly. It does **not** reproduce the sweep figure: `R-008` states `386,845`, `measure` prints **`387,953` TF-1 / `500,259` TF-2 over 176 files**. Nor can it ever settle, because the printed envelope is *"top-level `.ai/` `framework/` `src/` `tests/`, suffixes `.json .md .py .txt .yaml .yml`"* — which contains `.ai/project/results/R-008.md` and this report. **The record is inside the envelope it measures**, so publishing the number changes the number. Carried as `FIND-Q9-31` |
| **`Q9-27` — a superseded record whose pins match the tree is flagged** | **CLOSED IN FORM, INVERTED IN EFFECT** | The notice exists and fires — on the wrong record, and it stops firing on tampering. See §17. Carried as `FIND-Q9-28`, MAJOR |

---

## 17 · The `R-001` supersession notice — disposed

`status` prints, against `R-001` only:

> *"every pin matches the current tree, which a historical record would not normally do — verify
> it was not rewritten after supersession."*

I was asked to dispose it. **It is a false positive, and testing why exposes a MAJOR defect in
the guard that raised it.**

**Why `R-001` is clean.** `R-001` pins **six paths, all of them `inputs` and no deliverables** —
that omission *is* `FIND-Q9-3`, `R-001`'s own known defect. The six are `.ai/BOOT.md`,
`STATE.md`, `BINDING.md`, `CONTEXT_TIERS.md`, `SCH-task.schema.json` and
`framework.manifest.json`: every one an artefact `T-001` was **forbidden** to modify, and §14
AC-5 independently confirms none of them changed on 2026-08-09. For a record that pins only
inputs the task could not touch, matching the current tree is **the expected state of a faithful
historical record**, not the signature of a rewrite. `R-001`'s mtime, 07:18, precedes `R-007`
(07:43) and `R-008` (07:57), so it was not written after its own successors. **No evidence of
mutation. The notice is unfounded on this record.**

**Why the guard is inverted.** `graph.result_currency` lines 39–60 short-circuit on
`SUPERSEDED` and emit the notice only when **every** pin matches. Three measurements:

| Record | Pins | Match | Notice? | Was it actually rewritten after supersession? |
|---|---|---|---|---|
| `R-001` | 6 | 6 | **YES** | **No** — pins only untouchable inputs |
| `R-007` | 27 | 20 (7 drift) | **no** | **Yes** — its own header discloses a repinning script rewrote twelve digests, and pass 3 confirmed it three ways |
| `R-008` | 19 | 19 | n/a — CURRENT | n/a |

The guard fires on the innocent record and is silent on the guilty one. Worse, it is
**anti-monotonic**: from a pristine scratch copy I rewrote a single digest inside `R-001` — the
exact attack the notice exists to surface — and the notice **disappeared**, with
`check` still reporting all eight PASS. Tampering removes the warning that tampering happened.
`R-007` escapes for the same reason in the wild: the tree kept moving after it was repinned, so
seven of its pins drifted and the heuristic fell silent. The signal that existed at 07:53
decayed by 07:57 without anyone touching `R-007`. **What the guard detects is not "was this
rewritten" but "was this rewritten and has nothing moved since" — an accident of timing.**
Carried as `FIND-Q9-28`.

---

## 18 · New findings — pass 4

| ID | Severity | Statement | Owner |
|---|---|---|---|
| **FIND-Q9-28** | **MAJOR** | **The `Q9-27` supersession guard is inverted and anti-monotonic.** `graph.result_currency` (`src/aief_exec/graph.py`, lines 39–60) notices a superseded record only when *all* its pins match. Measured on the live tree: it fires on `R-001`, which pins six inputs `T-001` was forbidden to touch and was demonstrably not rewritten; it is silent on `R-007`, the one record in this repository that **was** rewritten after supersession and says so in its own header. Rewriting a single digest in `R-001` on a scratch copy **silenced** the notice while all eight `X` checks continued to report PASS — the guard rewards the tampering it was built to expose. The property it actually tests is "pins match *and* the tree has not moved since", which decayed for `R-007` between 07:53 and 07:57 with no one touching it. A guard that cannot distinguish these cases should not report on this axis at all; a sound one retains the published digests (a pin-of-pins over the record's own frozen digest block at supersession) and compares against that, not against the moving tree | `software.software-engineer`; `chief-systems-engineer` |
| **FIND-Q9-29** | **MAJOR** | **`FIND-Q9-24` is recorded closed and is not.** `scope.patterns_overlap`'s conservative fallback repairs exactly one of the six false-negative pairs pass 3 identified. Still reporting **disjoint when they genuinely intersect**: `src/aief_exec/*_new.py` × `src/aief_exec/new_*.py`; `tests/test_*_records.py` × `tests/test_exec_*.py` (both match the existing `tests/test_exec_records.py`); `build/*a*.json` × `build/*b*.json`; `build/x/T-00?.md` × `build/x/T-0?1.md`; `build/**/gen_*.py` × `build/gen/*_gen.py`. Five of nine probes wrong, all in the unsafe direction, in the primitive under concurrent-write safety. The exposure remains bounded exactly as pass 3 described — `scopes_intersect` computes the concrete intersection first, so collisions among **existing** files are still caught, and no live task pair depends on the fallback — but `R-008` F-008's claim of *"restoring error in the safe direction"* does not hold for five of the six cases it was written to answer, and F-008 is filed MINOR on that basis. The `T-001` checkpoint's narrower wording, *"a conservative fallback for two double-stars"*, is accurate; the result record's is not | `software.software-engineer` |
| **FIND-Q9-30** | MINOR | **`R-008`'s `validation` block states a test count its own pinned artefacts do not produce.** Line 67 reads *"239 passed, 4 failed - exec 129 passed 0 failed"*. Measured: **241 passed, 4 failed; exec 131 passed, 0 failed** (`test_exec_records` 23, `test_exec_scope` 30, `test_exec_graph` 23, `test_exec_checks` 55). All four exec test files are **byte-identical to `R-008`'s pins**, there is no `conftest.py`, and the only two parametrised generators are static, so collection cannot vary with repository state — the figure was wrong when written. The Stage 6 half (110/4 at 114) is exact. This is the third consecutive result record to carry an unverifiable number behind matching digests (`FIND-Q9-19` on `R-007`, `FIND-Q9-25` on `R-008` pass 3, this on `R-008` pass 4). The remedy is not another correction but to make the figure a computed artefact or to stop stating it | `software.software-engineer` |
| **FIND-Q9-31** | MINOR | **`R-008`'s sweep figure does not reproduce, and structurally cannot.** The conclusion states *"386,845 by unbounded sweep"* and that *"the sweep and declared figures and the anchoring ratio are reproduced by `python -m aief_exec measure T-002`"*. Run today, `measure T-002` prints **`387,953` TF-1 / `500,259` TF-2 across 176 files**. The declared figure (`9,727`) and the anchoring ratio do reproduce, so two thirds of the sentence is sound. The sweep figure cannot be, because the envelope `measure` prints — *top-level `.ai/` `framework/` `src/` `tests/`, suffixes `.json .md .py .txt .yaml .yml`* — **contains `.ai/project/results/R-008.md` and this report**. **Demonstrated, not argued:** `measure T-002` printed **`387,953`** TF-1 immediately before this file was written and **`397,349`** TF-1 immediately after — same command, same envelope, same 176 files, moved 9,396 tokens by the act of filing the audit that measured it. The `FIND-Q9-26` remedy fixed the right problem (the envelope is now defined in code and printed) and then pinned a value the definition makes unpinnable. Either exclude the result and verification registers from the envelope, or state the sweep as a command to run rather than a number | `software.software-engineer` |
| **FIND-Q9-32** | MINOR | **The framing `FIND-Q9-23` corrected survives verbatim in the contract.** `EXECUTION_ARCHITECTURE.md` **line 163**, in §5, still reads *"This does not make a grant unforgeable by someone who can write both files."* §14 item 5 of the same document was corrected and now states the opposite — that three of four successful forgeries cited files the forger does not write. A contract that carries both the corrected and the superseded framing, with the superseded one at the point of first reading, has not closed the finding; it has relocated the accurate version to the appendix | `software.software-engineer` |
| **FIND-Q9-33** | MINOR | **`R-008`'s instrumentation figure for `brief` is low.** The record states *"`brief` itself opens 21 files"*. Instrumenting `builtins.open`, `Path.read_text` and `Path.read_bytes` around `brief T-002` gives **34 distinct repository files, 29 of them outside `T-002`'s declared mandatory scope**. I record the caveat that `R-008` states no counting method, so the two may be measuring different things — which is itself the defect: an instrumentation figure published without its instrumentation is not checkable, and the direction of the gap understates the disclosure. The emitted brief remains correctly bounded at five entries, so `AC-2` is unaffected | `software.software-engineer` |
| **FIND-Q9-35** | **MAJOR** | **`X-08` does not charge a task for the deliverable it must read, so a verification task's budget is fiction.** `X-08` and `scope.resolve_scope` charge `T-004` **TF-1 2,519 / TF-2 3,185** against its declared cap of 8,000 / 10,000, and report PASS. That figure counts `T-001.md` and `LAW-05` and stops. It omits `R-008` (TF-1 3,550), the `T-004` record itself (886), and above all **`VER-009`, which `T-004`'s own AC-4 makes unavoidable** — twelve of the findings this task must dispose exist nowhere else, and the deliverable is updated in place, so it must be read in full. `VER-009` cost **TF-1 9,019** when this pass began. Actual input for this pass is roughly **TF-1 22,000**, about **8.7×** what `X-08` certifies and **2.8×** the declared cap. The defect is structural, not a mis-set number: `resolve_scope` models a task as *what it reads to start* and a QA task is dominated by *what it must rewrite*. It compounds — `VER-009` now costs **TF-1 18,438**, so a fifth pass would exceed `T-004`'s entire cap on the deliverable alone before reading anything. Either charge `deliverable` paths that already exist to the budget, or declare them and let `X-08` see them | `software.software-engineer`; `project-manager` |
| **FIND-Q9-34** | MINOR | **`cmd_measure` formats a possibly-`None` cost and dies with an unhandled `TypeError`.** `scope.cost` is documented to return `None` per family — *"UNMEASURED if either is absent"* — and `src/aief_exec/__main__.py` line 200 formats `c.tf1` and `c.tf2` with `:>10,` unconditionally. Reproduced on a scratch copy: `TypeError: unsupported format string passed to NoneType.__format__`, after the envelope header had already printed, so the command emits a partial report and then a raw traceback. This is the command `R-008` names as the reproducibility path for its headline figures; it should report `UNMEASURED` rather than crash | `software.software-engineer` |

**Carried forward unchanged from pass 3, re-confirmed live this pass:** `FIND-Q9-22` (MAJOR,
four working forgeries reproduced) and its owner-level escalation `F-007`. `FIND-Q9-11` and
`FIND-Q9-12` remain OPEN by acceptance, verified as genuinely recorded and, for `Q9-12`,
verified as genuinely mitigated.

---

## 19 · Final disposition — pass 4

> ### VERIFIED WITH FINDINGS
>
> `T-001` is verified. `R-008` is **CURRENT**. All six acceptance criteria **PASS**, verified
> cold and independently of pass 3. Eight findings are carried forward — four MAJOR — and two
> of the three MAJOR ones are **closures the record claims that do not hold**.

**What holds.** Nineteen of nineteen pins recomputed and matched. Six of six criteria pass on
evidence I generated. Nine of the twelve pass-1 findings are genuinely closed, two are open by
an acceptance I verified is really recorded and — for `Q9-12` — really mitigated, and the
twelfth is structurally closed with a named, escalated residual. The execution layer does the
thing it was built to do: a cold agent with no prior context executed a real task against a
declared scope, and the total context this pass consumed to reach a verdict is a small multiple
of the brief, not of the repository.

**Why not VERIFIED without qualification.** Not because the layer fails — it does not — but
because of what the pattern in §16 shows. **Of the six closures taken after pass 3, one is
correctly escalated, one is fully closed, and four are closed in form while defective in
substance**: `Q9-23` corrected two of three occurrences, `Q9-24` fixed one of six cases,
`Q9-25` stated the number and stated it wrong, `Q9-27` built a guard that fires on the innocent
record and falls silent when tampered with. Each was recorded in `R-008` and in the `T-001`
checkpoint as *closed*. **A closure that is asserted rather than re-tested is the same defect
class as an authority citation that has a form and not a referent** — and that class is now the
recurring finding of this audit across four passes. It is the reason `T-004` exists, and the
reason its own acceptance criterion AC-4 requires the verifier to re-test each closure itself
rather than read the closure list.

**The recommendation that follows is procedural, not technical.** `FIND-Q9-28` through
`FIND-Q9-34` are individually cheap. The thing worth fixing is that the four defective closures
would all have been caught by the party that closed them, at negligible cost, by running the
test the finding named — five `patterns_overlap` calls, one `pytest tests/`, one `measure`, one
`grep`. **A closure should not be recordable without the command that demonstrates it.** That is
`project-manager` and `chief-systems-engineer` territory, and I raise it as judgement rather
than as a finding because it is about the process, not the artefact.

**Escalations.** `FIND-Q9-28` and `FIND-Q9-29` to `software.software-engineer`, with the
authority question in `FIND-Q9-22` / `F-007` remaining with `chief-systems-engineer`.
`FIND-Q9-30` … `FIND-Q9-34` to `software.software-engineer`; `FIND-Q9-35` to `software.software-engineer` and `project-manager`. No finding blocks the layer's use,
no finding is BLOCKING, and no acceptance criterion fails.

**Out-of-scope changes I identified and did not make.** Four corrections fall outside
`T-004`'s write scope and are named here rather than applied: `R-008`'s test count (line 67) and
sweep figure; `EXECUTION_ARCHITECTURE.md` line 163; `graph.py` lines 39–60; `scope.patterns_overlap`;
`__main__.py` line 200. `T-001`'s checkpoint pending item — *"Re-verification of the six closed
findings by the T-004 verifier"* — **is discharged by §16**, but the checkpoint itself is under
audit and I did not edit it; clearing it is a `project-manager` action.

**Context accounting for this pass, stated rather than estimated.** Measured with the
repository's own tokenizer: `T-004.md` 886 · `LAW-05` 273 · `T-001.md` 2,246 · `R-008.md` 3,550
— **6,955 TF-1 of contract and dependency** — plus `VER-009` as it stood at 9,019 TF-1, plus
roughly 2,500 TF-1 of targeted source excerpts and 4,000 TF-1 of command output. **Actual
≈ 22,000 TF-1 against a declared cap of 8,000.** The overrun is not discretionary reading: it
is `VER-009` itself, which `X-08` does not charge and `AC-4` makes mandatory. That is
`FIND-Q9-35`, and this paragraph is its primary evidence.

**Confirmed live after writing this file.** `check` → `8 of 8 PASS`, exit `0`. `R-008` → still
**CURRENT**. `git status --porcelain` → still exactly **7** tracked modifications. `FIND-Q9-13`
therefore stays closed under the one act that broke it in pass 2: this task filing its own
deliverable does not stale the result this task consumes.

**Verifier attestation — pass 4.** Every figure in §§12–19 was produced by a command or a
direct library call executed in session `S-2026-08-09-05` against this repository. No claim
rests on `R-001`, `R-007`, `R-008`, `T-001`'s checkpoint, or §§1–11 of this report; where those
and my measurements disagree, the disagreement is recorded above and not reconciled in their
favour. I verified no artefact I produced. The repository was not modified except for this
file. This report is subject to review at
`.ai/project/reviews/DR-003_VER-009_Disposition.md` by `chief-systems-engineer`.

*Filed by `qa-engineer · S-2026-08-09-05` under task `T-004`, on the enumerated `role_authority`
grant `EXEC-D-001` recorded at `.ai/project/tasks/T-001.md`. Write scope exercised: this file
only.*

---

## 20 · Pass 5 — scope, method and footprint

**Pass 5 is a cold independent verification of the execution-architecture repair** filed after
pass 4, covering the five defect classes claimed repaired in `R-009`, `R-010` and `R-011` and the
changed artefacts `src/aief_exec/{records,scope,graph,checks,__main__}.py`,
`tests/test_exec_{records,scope,graph,checks}.py`, `EXECUTION_ARCHITECTURE.md` §5/§5.3/§11/§12/§14
and `.ai/project/tasks/{T-001,T-004}.md`. Sections §1–§19 are the record of passes 1–4 and are
**not amended**; pass 5 begins here.

| | |
|---|---|
| Verifier | `qa-engineer`, session `S-2026-08-09-09`, cold context |
| Authority | `role_authority` grant `EXEC-D-001`, recorded at `.ai/project/tasks/T-001.md`, cited by `T-004` |
| Repository | `D:\Fusion Projects\SEWCP_Master_Assembly`, HEAD `8546960`, working tree uncommitted |
| Method | Reproduce each claimed defect **before** accepting it needed fixing; then attack the repair |
| Footprint | Read-only on the repository except this file. Every perturbation ran on throwaway copies at `scratchpad/wt1` and `scratchpad/wt2`, or as in-process monkeypatches that never touched disk |
| Baseline | `check` → **7 of 9 PASS**; `X-08` and `X-09` FAIL. `pytest tests/test_exec_*.py` → **228 passed** |

**Independence.** I received the contract and the changed-artefact list, not the implementer's
conclusions. No disposition below rests on a claim in `R-009`, `R-010`, `R-011` or the `T-001`
checkpoint. `LAW-05` clause 4 is applied throughout: every number here was produced by a command
or a direct library call I ran in this session.

**A note on the two failing checks.** Both are **honest findings about the repository, not defects
in the repair** — see §24 for `X-09` and §22 for `X-08`. Neither failure is a false positive.

---

## 21 · Were the five defect classes real? Reproduced before accepted

| # | Defect class | Real? | Evidence I obtained | Root cause or symptom? |
|---|---|---|---|---|
| 1 | Publication reachability | **YES** | `T-002.write_scope` is `['src/aief_stage6/**', 'tests/test_stage6_*.py']` and `T-002.produces` is `[R-002]`. Evaluating `glob_to_regex(p).match('.ai/project/results/R-002.md')` over both patterns returns `False` for both. Same for `T-003`…`T-006`. `build_plan` then derives `T-006` BLOCKED on *"consumes R-002 which has not been published"* — and no lawful dispatch can ever publish it. A real structural deadlock | **Root cause** for the *"nothing saw it"* half — `produces`/`consumes` were in neither `SCH_TASK_REQUIRED` nor `EXTENSION_REQUIRED`, and `X-09` closes that hole. **Symptom-level** for the five mis-declared records, deliberately and correctly: repairing them is a `project-manager` act, not the check's |
| 2 | Observation-surface contamination | **YES**, as a class | Constructed `T-916` (write scope `src/aief_exec/records.py`) against `T-915` (consumes `R-011`, names no path). Pre-repair surfaces — write/write plus write/read over **mandatory** only — return **PARALLEL**. With the new limb the pair is **CONFLICT `[write/observe]`**. The hazard is genuine: `R-011` pins `records.py` as a deliverable, so `T-915`'s consumed conclusion depends on a file `T-915` never names | **Root cause** for the derivable part. But see §23: the derived surface has four systematic escapes, and **on the live tree the new limb changes no pair verdict at all** — every live `CONFLICT` is already carried by `write/write`. The limb is correct and currently inert |
| 3 | Budget accounting non-monotonic | **YES** | Synthetic `T-900`, deliverable absent: `acquisition` TF-1 542, `revision` 0. Created the deliverable (3,207 TF-1): `acquisition` **542, unchanged**; `revision` 0 → 3,207. The pre-split single figure would have moved 542 → 3,749, a 6.9× swing caused by the task's own output | **Symptom.** The split closes the *deliverable* channel of non-monotonicity and leaves at least two others open, one of which is the repair's own justifying anecdote. See §22 — this is `FIND-Q9-36`, MAJOR |
| 4 | Result-channel sealing | **YES** | `R-007` supersedes `R-001` and `R-008` supersedes `R-007`; both carry no `supersedes_seal.digest`. Confirmed by parsing the records directly. A post-supersession rewrite of `R-001` or `R-007` is undetectable, permanently | **Symptom.** The seal works per-record and the epoch rule is honestly derived — but the control **can be switched off by deleting its own evidence**, which is the anti-monotonic failure class `FIND-Q9-27`/`Q9-28` were raised for. See §26 — `FIND-Q9-39`, MAJOR |
| 5 | Verdict explainability | **YES**, and **fully repaired** | `cmd_classify` (`src/aief_exec/__main__.py:169–184`) prints, for every `PARALLEL`, the five comparisons with both surfaces and each intersection result, then both observed surfaces, then the `undeclared_observation` notices. I did not merely read this — **§23's headline finding was found by reading that output**, which is the strongest evidence an explanation can produce | **Root cause.** No finding against it |

---

## 22 · Budget honesty — is the gated quantity invariant, and what does it exclude?

### 22.1 Invariant across the deliverable channel — YES

Synthetic task `T-900` on `scratchpad/wt1`, measured through `scope.charged_context` directly:

| Tree state | `acquisition` TF-1 | `revision` TF-1 | `total` TF-1 |
|---|---|---|---|
| Deliverable does not exist | **542** | 0 | 542 |
| Deliverable created (3,207 TF-1) | **542** | 3,207 | 3,749 |

The gated quantity does not move. **Defect 3 is genuinely fixed on the channel it was reported on.**

### 22.2 NOT invariant across two other channels — `FIND-Q9-36`, MAJOR

The same `T-900`, third measurement, after the task appends a progress note to **its own
checkpoint** — which every AIEF task record is required to carry and to update as it works:

| Tree state | `acquisition` TF-1 | moved? |
|---|---|---|
| After deliverable created | 542 | — |
| After own-record checkpoint update | **1,328** | **+145 %** |

`record` is an `ACQUISITION_COMPONENTS` member (`src/aief_exec/scope.py:501`). Wherever a task's
`write_scope` covers its own task record, the gated figure is a function of the task's own work —
exactly the property the split was built to remove.

**This is not hypothetical; it is live, and it is not confined to the record component:**

| Task | gated `acquisition` TF-1 | of which sits in paths the task itself writes | component |
|---|---|---|---|
| `T-001` | 6,732 (cap 6,000) | **2,258 — 34 %** | `record` → `.ai/project/tasks/T-001.md` |
| `T-002` | **12,880 (cap 12,000 — this is a live `X-08` FAILURE)** | **3,108 — 24 %** | `mandatory` → `src/aief_stage6/budget.py` (2,306), `src/aief_stage6/lock.py` (802) |

`T-002` is the sharp case. Its `revision` is **0** — it has no resolvable deliverable at all — yet
`charged_context` still reports two non-monotonic paths, and **both are inside `acquisition`**.
`X-08` fails `T-002` by 880 TF-1 on a number that grows every time `T-002` edits `budget.py`,
which is the task's entire job. A dispatch gate that the dispatch moves is the defect the split
was supposed to retire, and here it survives inside the quantity that gates.

**The repair's own justifying anecdote is one it does not address.** `src/aief_exec/scope.py:723–726`
reads: *"a concurrent session watched its own brief grow from TF-1 4,295 to 4,910 by adding
docstrings to a file inside its own read scope."* A file inside its own **read scope** is charged
under `mandatory` or `optional` — both `ACQUISITION_COMPONENTS`. The comment then concludes
*"…it is now connected to the split, because self-reference is precisely what disqualifies
`revision` from gating anything"*, which does not follow: the incident cited is a self-reference
in `acquisition`, and the split leaves it gating.

**The emitted notice states the same non-sequitur.** `src/aief_exec/scope.py:739–746` prints, for
every task with any moving path: *"…this is why `revision` (…) is reported and `acquisition` (…)
is the gated quantity."* For `T-002` that sentence names two paths that are in `acquisition`,
then offers `acquisition` as the answer to their movement. A reader is told the problem is solved
by the very number that carries it.

### 22.3 Does the gate now exclude real cost an agent must load? — YES, and materially

| Task | gated `acquisition` | excluded `revision` | excluded as % of measurable total |
|---|---|---|---|
| `T-004` | 17,162 | **19,049** | **53 %** |
| `T-001` | 6,732 | **37,211** | **85 %** |
| `T-005` | 1,411 | **5,750** | **80 %** |

`revision` is real, unavoidable, pre-dispatch cost, and `ChargedContext`'s own docstring concedes
it: *"Real cost — an artifact being rewritten must be read"* (`scope.py:535–536`). For `T-004` the
excluded 19,049 TF-1 is this very file, which `T-004`'s `AC-4` makes **mandatory** to read: the
findings it must dispose exist nowhere else. So the gated figure omits the single largest item the
agent is contractually required to load. `telemetry` is excluded too, correctly and with the
honest `UNMEASURABLE` label rather than a zero.

**Verdict on the trade.** The measurement was made stable in one channel by moving 53–85 % of the
real cost outside the gate, while leaving 24–34 % of the *remaining* gated figure still moving. It
is not a clean improvement over the defect it replaced: it is a different distribution of the same
two errors. **`FIND-Q9-36` (MAJOR)** for the surviving non-monotonicity and the notice that
misdescribes it; **`FIND-Q9-37` (MAJOR)** for the excluded cost — a cap that bounds 47 % of `T-004`'s
measurable input, with nothing bounding the other 53 %, is not a budget. `X-08`'s six failures are
nonetheless **honest**: every one is a real overrun of a real cap, and `T-001`'s is correctly
demoted to a notice because a `COMPLETE` task has no dispatch to refuse.

---

## 23 · Parallelism soundness — both directions

### 23.1 A genuinely hazardous pair called PARALLEL — found live, twice, no construction needed

**`FIND-Q9-38`, MAJOR.**

**H1 — a task's own contract is on no conflict surface.** `T-001.write_scope` includes
`.ai/project/tasks/**`, which matches `.ai/project/tasks/T-002.md` and `.ai/project/tasks/T-005.md`
— the contracts `T-002` and `T-005` are executing. `classify` returns:

```
T-001 x T-002  ->  PARALLEL
T-001 x T-005  ->  PARALLEL
```

`T-001` may rewrite another task's objective, acceptance criteria, `write_scope`, `forbidden_actions`
and `context_budget` while that task runs, and the layer certifies the pair safe. The layer is not
ignorant of the dependency: **`X-08` charges `T-002` 931 TF-1 and `T-005` 656 TF-1 for that exact
file under the `record` component**, so the budget model knows a task reads its own record while
the hazard model does not. `.ai/project/tasks/T-002.md` is absent from `T-002`'s observed surface.
`T-001` also holds `.ai/project/results/**`, so the same verdict permits it to rewrite `R-002`,
the record `T-002` is contracted to produce.

**H2 — the measurement backend is on no conflict surface.** `classify T-002 T-004` → **PARALLEL**.
`T-002.write_scope` is `src/aief_stage6/**`, which contains `src/aief_stage6/tokenizers.py`.
Every token figure `aief_exec` produces flows through it — `src/aief_exec/scope.py:22` imports
`from aief_stage6 import tokenizers as _tok`, and `scope.cost` calls it for TF-1 and TF-2. `T-004`
is a verification task whose findings are token measurements. `T-004`'s observed surface (13
patterns) and mandatory read scope (`T-001.md`, `LAW-05`) both exclude it;
`scopes_intersect(T-002.write, T-004.observed)` returns `False`. `T-002` may replace the instrument
`T-004` measures with, mid-measurement, under a PARALLEL verdict.

I found H2 by reading the `safety_explanation` output, which prints `T-004`'s mandatory read scope
and observed surface side by side. **Defect 5's repair is what exposed defect 2's residual.**

### 23.2 Which hazard cases escape the derived surface — enumerated

| # | Escaping case | Status | Evidence |
|---|---|---|---|
| E1 | **`optional` read scope.** `conflict_reasons` line 469 and `safety_explanation` line 538 both iterate `reader.read_entries("mandatory")` only | **Undetected** | Matched-pair control on `wt1`: `T-910` writes `.ai/project/probe/alpha.md`; `T-911` declares it **optional** → **PARALLEL**. `T-912`/`T-913`, byte-identical but the same path declared **mandatory** → **CONFLICT `[write/read]`**. The only variable is the declaration class |
| E2 | **`dependency` read scope — the consumed result record itself.** `observed_surface` term 3 adds the consumed result's **`deliverables[].path`**, never `.ai/project/results/R-nnn.md` | **Undetected** | `T-914` writes `.ai/project/results/R-011.md`; `T-915` consumes `R-011` → **PARALLEL**. `'.ai/project/results/R-011.md' in observed_surface(T-915)` → `False`, on a 12-pattern surface. A consumer must read that file to confirm the record is CURRENT and unsuperseded — `charged_context` charges it whole under `dependency` for exactly that reason (`scope.py:658–663`) |
| E3 | **The task's own record.** On no surface — not write, not read, not observed | **Undetected, live** | H1 above |
| E4 | **Runtime/tooling dependencies** — code a task imports to generate its evidence | **Undetected, live** | H2 above |
| E5 | **Undeclared observation** (`pytest`, `git status`, `python -m`) | **Disclosed, not detected** | `undeclared_observation` emits five heuristic notices on `T-001` and states plainly that it is a heuristic. Correctly handled under LAW-12 — a real limit, honestly labelled |

E1–E4 share one root: **the conflict model compares three surfaces, while the cost model already
enumerates five** (`record`, `mandatory`, `optional`, `dependency`, `deliverable`). The information
needed to close E1–E3 is computed, in the same module tree, and discarded before the comparison.
That is the root cause, and it is one fix, not four.

### 23.3 A genuinely safe pair called hazardous — none found

I could not construct a false CONFLICT. `patterns_overlap` is an exact product-reachability
decision over the two globs' automata, not a heuristic, so pattern-level overlap is neither
over- nor under-reported. The one over-broad term is defensible: `observed_surface` term 3 adds
every deliverable pinned by a consumed result, which is stricter than §6's *"read the conclusion,
do not re-derive it"* — a consumer that genuinely reads only the conclusion is called hazardous
against writers of files it never opens. This errs in the **safe** direction and the layer cannot
distinguish the two consumer kinds, so I record it as an observation, not a finding.

Two structural remarks, both MINOR and both in `graph.py`:

* **`FIND-Q9-40`** — `Plan.parallel_sets` (`graph.py:569–580`) is documented as producing
  *"Maximal groups"*. It is a first-fit greedy pass in identifier order; first-fit does not
  produce maximal cliques. No safety consequence — `X-07` re-verifies every group pairwise — but
  the docstring overstates what the algorithm delivers.
* **`FIND-Q9-41`** — `build_plan` evaluates `CONFLICT` **before** `BLOCKED` (`graph.py:631–641`),
  so a pair is reported CONFLICT even when one member is permanently BLOCKED or `COMPLETE` and can
  never be co-dispatched. Not unsafe; it inflates the hazard report.

---

## 24 · Publication reachability

**Can a task declare an impossible result and pass?** No. `X-09` mode 1 fires on all five live
cases (`T-002`…`T-006`), each with the exact repair named. I confirmed the underlying facts by
evaluating the globs myself rather than reading the check's output: no pattern in any of the five
`write_scope` declarations matches its own `.ai/project/results/R-nnn.md`.

**Can a consumer consume a result no task produces?** No. Mode 2 covers it, and mode 4 escalates
to deadlock where the record is also absent from disk. `T-006` consumes `R-002` and `R-003`, both
declared by producers that cannot write them — mode 1 fires on the producers and `build_plan`
independently derives `T-006` BLOCKED. The two agree, as the docstring says they should.

**Both `X-09` failures are honest findings about the repository, not defects in the repair.**

**But the channel is guarded in one direction only — `FIND-Q9-42`, MAJOR.** `X-09` verifies that
every declared producer *can* write its record. Nothing verifies that a non-producer *cannot*.
Live:

```
T-001 write_scope reaches result records it does NOT produce: R-002, R-003, R-004, R-005, R-006
   declared producers: T-002, T-003, T-004, T-005, T-006 respectively
X-09 details naming an undeclared writer of a result record: NONE
```

`X-09` mode 3 states the invariant it is protecting — *"a result has exactly one producer, and
with two the `produced_by` a consumer checks cannot be derived"* (`checks.py:630–633`) — but tests
it only against `produces` **declarations**, never against `write_scope` **reach**. `T-001` holds a
lawful, `X-04`-clean write grant over five result records it does not own. Compounded by
`FIND-Q9-38` H1 this is concrete: `T-001 x T-002` is **PARALLEL**, so `T-001` may publish `R-002`
concurrently with `T-002`, its declared producer, and every check passes.

---

## 25 · Scope enforcement preserved — the derived grant is enforced nowhere

Established three ways, two of them adversarial.

**1 · Static.** `effective_write_scope` is read at exactly two sites outside its own definition and
the test suite: `src/aief_exec/checks.py:666` (builds an `X-09` **notice**) and
`src/aief_exec/__main__.py:84,93` (**display** in `cmd_scope`). No check compares anything against
it. `X-04`'s source contains `task.write_scope` and does **not** contain `effective_write_scope`.
Every other consumer of a write scope also takes the declared one: `scope.attribute` line 435,
`graph.observed_surface` line 367, `charged_context`'s `non_monotonic` line 729.

**2 · Mutation, negative.** In-process monkeypatch — no file touched, so no pinned digest moved —
forcing `TaskRecord.effective_write_scope` to return `["**"]`, a maximal grant over the entire
repository:

```
UNMUTATED : X-01 PASS X-02 PASS X-03 PASS X-04 PASS X-05 PASS X-06 PASS X-07 PASS X-08 FAIL X-09 FAIL
MUTANT    : X-01 PASS X-02 PASS X-03 PASS X-04 PASS X-05 PASS X-06 PASS X-07 PASS X-08 FAIL X-09 FAIL
all nine verdicts unchanged? True   (and every detail list byte-identical)
```

A maximal derived grant changes nothing. Nothing enforces it.

**3 · Mutation, positive control** — to prove the harness can see an enforcement change at all.
Forcing `T-005`'s **declared** `write_scope` to `.ai/core/**`:

```
X-04 -> FAIL
  T-005: write_scope '.ai/core/**' reaches the protected set
         (.ai/core/CONTEXT_TIERS.md, .ai/core/PRECEDENCE.md, .ai/core/VERSION)
         and is not enumerated in write_authority.paths
```

`X-04` still gates on the declared scope, and only on the declared scope. **The A4 decision is not
pre-empted.** Requirement satisfied, no finding.

---

## 26 · Result-chain seal integrity, by recomputation

Each seal recomputed twice and independently — once via `records.file_dc1` and once via a raw
`hashlib.sha256` over the predecessor's bytes, which agreed on every link — and compared against
the digest the **successor** pins.

| Link | Successor's pinned digest | Recomputed DC-1 / SHA-256 | Verdict |
|---|---|---|---|
| `R-001` → `R-007` | *none pinned* | `61752b84…5afd8e8d` | **UNSEALED** — rewrite undetectable. `R-007` session `S-2026-08-09-01`, pre-epoch → notice, correctly not a failure |
| `R-007` → `R-008` | *none pinned* | `30e97501…b45ef9407` | **UNSEALED** — same, `R-008` session `S-2026-08-09-01`, pre-epoch |
| `R-008` → `R-009` | `e081eb7b9370afe98cb57d8f98b15fdd5ea088c1ecc417477755205959d15a6b` | identical | **MATCH** |
| `R-009` → `R-010` | `6cc1c3efcd0d14e0a8ceac2288ddc6e4ffe4f5d76c9a1d9fa0adec252bd548aa` | identical | **MATCH** |
| `R-010` → `R-011` | `45516365790fd220ccd16be0b4a7dd25294cb3cb19f0301622a2d1d8bfcd1f12` | identical | **MATCH** |

`seal_epoch` = `S-2026-08-09-06`, derived from `R-009`, the earliest sealing record. Sessions:
`R-007` `-01`, `R-008` `-01`, `R-009` `-06`, `R-010` `-07`, `R-011` `-08`. The epoch rule is
honestly derived from the records and is not being evaded: every post-epoch supersession carries a
seal. **`R-011` is CURRENT**, all pins recomputed and matched.

Incidental confirmation that the pins bite: an earlier on-disk mutation of
`src/aief_exec/records.py` on a scratch copy immediately drove `X-06` and `X-02` to FAIL, because
`R-011` pins that file as a deliverable. I discarded that copy and switched to in-process
monkeypatching for the remaining mutations.

### 26.1 The control switches itself off — `FIND-Q9-39`, MAJOR

`graph.result_currency:162–164` claims: *"The control is monotonic by construction: tampering can
only add the alarm, never remove it, because the evidence lives in a different file from the one
being protected."* **That claim is false above the level of a single record.** On `wt1` I removed
the `supersedes_seal` block from `R-009`, `R-010` and `R-011` — the successors, which is where the
claim says the evidence safely lives:

```
seal_epoch after stripping: ''
X-06 -> PASS   details: NONE
notice: R-009: supersedes R-008 and pins no supersedes_seal. Session S-2026-08-09-06 predates
        any sealed supersession, ...
```

Because `seal_epoch` is `min()` over the records that *carry* a seal, deleting every seal empties
the epoch, and an empty epoch makes the rule vacuous for all six records at once. **The tamper
detector's entire evidence base is inside the set of files a tampering party is already editing,
and removing it removes the alarm and the failure together.** This is the same anti-monotonic
shape as `FIND-Q9-27` — a guard that rewards the tampering it exists to expose — relocated from
the predecessor side to the epoch.

`seal_epoch`'s docstring discloses two residuals: a vacuous epoch *"before any seal exists"*, and
a successor declaring a false early session. Neither covers this. The first is framed as a
beginning-of-history condition — *"A control that has never had an anchor cannot place one"* —
not as a state reachable from a fully sealed repository by deletion. **The disclosure is
incomplete in the unsafe direction**, which §1 of this report already names as a defect class in
its own right.

Two lesser observations on the same code, both MINOR and folded into `FIND-Q9-39`: the notice text
*"Session S-2026-08-09-06 predates any sealed supersession"* becomes false under stripping (it
does not predate anything; there is nothing to predate), and the `X-06` verdict of PASS with zero
details after a three-record tamper is the least informative possible output.

---

## 27 · Test quality — was anything weakened, retargeted or made regression-blind?

**No.** This is the strongest part of the repair. I did not read the tests and form an opinion; I
broke sixteen mechanisms and counted the corpses. Campaign run on a throwaway copy at
`scratchpad/wt3`, baseline **228 passed**, each mutant applied and reverted in isolation:

| Mutant | What it breaks | Result |
|---|---|---|
| M1 | Undo the split — put `deliverable` back inside `ACQUISITION_COMPONENTS` | **KILLED** 9 failed |
| M2 | `REVISION_COMPONENTS = ()` — revision always zero | **KILLED** 9 failed |
| M3 | `X-08` gates `cc.total` instead of `cc.acquisition` | **KILLED** 4 failed |
| M4 | Delete the `write/observe` conflict limb entirely | **KILLED** 9 failed |
| M5 | `observed_surface` drops term 3 (consumed-result deliverables) | **KILLED** 8 failed |
| M6 | `observed_surface` drops term 4 (declared `observes`) | **KILLED** 6 failed |
| M7 | `X-09` mode 1 never fires | **KILLED** 6 failed |
| M8 | `effective_write_scope` collapses to the declared scope | **KILLED** 7 failed |
| M9 | `X-09` drops the DERIVED-NOT-GRANTED notice | **KILLED** 5 failed |
| M10 | `undeclared_observation` always silent | **KILLED** 10 failed |
| M11 | `charged_context` stops reporting `non_monotonic` | **KILLED** 7 failed |
| M12 | `X-08` gates `COMPLETE` tasks too | **KILLED** 4 failed |
| M13 | `seal_epoch` always empty | **KILLED** 6 failed |
| M14 | `REWRITTEN`-after-supersession alarm removed | **KILLED** 6 failed |
| M15 | Charge `mandatory` only — the `FIND-Q9-5` regression | **KILLED** 5 failed |
| M16 | `deliverable_paths` resolves nothing — the `FIND-Q9-35` regression | **KILLED** 16 failed |

**16 of 16 killed. No survivors.** Both historically closed findings (`Q9-5`, `Q9-35`) have live
regression guards that fire. `M13` is worth singling out: the suite *does* catch a code change
that empties `seal_epoch` — what it does not catch is `FIND-Q9-39`, where the epoch is emptied by
editing **records** rather than code, which no unit test is positioned to see.

**One suspected tautology, hypothesised and disproved.**
`test_exec_scope.py:427 test_acquisition_is_exactly_its_four_components` computes its expected
value by summing `cc.component_total(name)` over `scope.ACQUISITION_COMPONENTS` — the same
constant and the same accessor `ChargedContext.acquisition` uses, so lines 431–434 cannot
independently fail. I ran M1 against **that test alone** expecting it to survive. It did not: it
failed at line 436 on `cc.total == cc.acquisition + cc.revision`, because `total` counts each unit
once while a double-listed component does not. The cross-check at 436 and the disjointness
assertion at 437 carry the test. **Not a tautology in effect.**

**Two scoping observations, neither a defect:**

* `TestBudgetSplit._task` (`test_exec_scope.py:374–384`) places the task record at `d/task.md`
  with `write_scope=("out/**",)`, so the record is outside the write scope **by fixture
  construction**. That is the one configuration in which `acquisition` is invariant. The
  invariance test is therefore correctly scoped to its own title — *"invariant to whether the
  **deliverable** exists"* — and is not weakened. But no test asserts the broader property the
  code and the architecture document both claim, which is why `FIND-Q9-36` is invisible to a green
  suite.
* `test_exec_graph.py:553` checks the live `R-009` seal only by shape (`len(digest) == 64`). I
  suspected a gap and found it already covered: `test_exec_checks.py:294` recomputes the live
  seals properly with `assert sealed == records.file_dc1(REPO, results[rid].path)`. No finding.

**No test locks in a defect.** Nothing asserts the live `T-001 x T-002` or `T-002 x T-004`
PARALLEL verdicts. `test_a_verifier_consuming_nothing_stays_parallel` asserts PARALLEL only for a
synthetic control pair that is genuinely independent.

---

## 28 · Findings — pass 5

| ID | Severity | Finding | Exact site | Owner |
|---|---|---|---|---|
| **FIND-Q9-36** | **MAJOR** | **The gated quantity is still non-monotonic; the claim that it is not appears in the architecture document.** `EXECUTION_ARCHITECTURE.md:323` states `acquisition` is *"Stable across the task's own execution"* and `scope.py:530–532` states *"it cannot be moved by the task's output."* Both are false. Synthetic `T-900`: `acquisition` 542 → **1,328 (+145 %)** when the task appends to its own checkpoint, because `record` is an `ACQUISITION_COMPONENTS` member (`scope.py:501`) and the record is inside the task's write scope. Live: 34 % of `T-001`'s gated figure and **24 % of `T-002`'s — a figure `X-08` currently FAILS on** — sits in paths those tasks write. The repair's own justifying anecdote (`scope.py:723–726`, a brief growing 4,295 → 4,910 by editing *a file inside its own read scope*) is an `acquisition` self-reference the split does not touch | `.ai/project/EXECUTION_ARCHITECTURE.md:323–324`; `src/aief_exec/scope.py:501`, `:530–532`, `:723–726` | `software.software-engineer` |
| **FIND-Q9-36b** | **MAJOR** | **The emitted notice states a falsehood about the live tree.** `checks.py:537–549` appends the `non_monotonic` count to the **revision** clause, but `cc.non_monotonic` (`scope.py:729–737`) is computed over **all** charged units. `X-08` therefore prints, verbatim: `T-002 [READY]: … | revision TF-1 0 / TF-2 0 reported, non-monotonic in 2 path(s) inside this task's own write scope (nothing charged)`. Revision is zero and monotonic; the two moving paths are in `acquisition`. The same line says *"non-monotonic in 2 path(s)"* and *"nothing charged"* six words apart, and `scope.py:744–746` closes with *"this is why `revision` … is reported and `acquisition` … is the gated quantity"* — offering the number that carries the movement as the cure for it | `src/aief_exec/checks.py:537–549`; `src/aief_exec/scope.py:729–746` | `software.software-engineer` |
| **FIND-Q9-37** | **MAJOR** | **The gate now bounds a minority of the measurable cost.** `X-08` compares `context_budget` against `acquisition` only (`checks.py:517`). Excluded `revision` is 19,049 TF-1 for `T-004` (**53 %** of its measurable total), 37,211 for `T-001` (**85 %**), 5,750 for `T-005` (**80 %**). For `T-004` the excluded item is this file, which `AC-4` makes mandatory reading. `ChargedContext` concedes it is *"Real cost — an artifact being rewritten must be read"* (`scope.py:535–536`). A cap bounding 47 % of an agent's required input, with nothing bounding the rest, is not a budget — the FIND-Q9-35 undercount has been reduced, not removed | `src/aief_exec/checks.py:517`; `src/aief_exec/scope.py:505`, `:535–536` | `software.software-engineer`; `project-manager` |
| **FIND-Q9-38** | **MAJOR** | **Genuinely hazardous pairs are classified PARALLEL, live, in the hazard class this repair introduced.** **H1:** `T-001 x T-002` and `T-001 x T-005` → **PARALLEL**, while `T-001.write_scope` (`.ai/project/tasks/**`) covers the *contracts those tasks are executing*. `X-08` charges that same file 931 / 656 TF-1 under `record`, so the layer knows the dependency exists — the cost model sees it and the hazard model does not. **H2:** `T-002 x T-004` → **PARALLEL**, while `T-002.write_scope` (`src/aief_stage6/**`) contains `tokenizers.py`, the backend of every measurement `T-004` reports (`scope.py:22`). Four systematic escapes, enumerated in §23.2 with a matched-pair control for E1: **optional** read scope (`graph.py:469`, `:538` iterate `mandatory` only), the **consumed result record itself** (`observed_surface` term 3 adds the result's deliverables, never `.ai/project/results/R-nnn.md`), the **task's own record**, and **runtime tooling**. Root cause is single: `charged_context` enumerates five surfaces; `conflict_reasons` compares three, and discards the other two | `src/aief_exec/graph.py:326–380`, `:469`, `:479–490`, `:538` | `software.software-engineer` |
| **FIND-Q9-39** | **MAJOR** | **The supersession-tamper control can be switched off by deleting its own evidence, and the code claims it cannot.** `graph.py:162–164`: *"The control is monotonic by construction: tampering can only add the alarm, never remove it, because the evidence lives in a different file from the one being protected."* Removing the `supersedes_seal` block from `R-009`, `R-010` and `R-011` on a scratch copy empties `seal_epoch` (`min()` over sealing records → `''`), which makes the epoch rule vacuous for all six records at once: **`X-06` → PASS, zero details.** Successor files are exactly the files a tampering party is already editing. `seal_epoch`'s docstring discloses a vacuous epoch only as a beginning-of-history condition — *"A control that has never had an anchor cannot place one"* — not as a state reachable by deletion from a fully sealed chain. Same anti-monotonic shape as `FIND-Q9-27`, relocated from the predecessor to the epoch | `src/aief_exec/graph.py:87–120`, `:162–164`; `src/aief_exec/checks.py:353–368` | `software.software-engineer`; `chief-systems-engineer` |
| **FIND-Q9-42** | **MAJOR** | **`X-09` guards the publication channel in one direction only.** It verifies every declared producer *can* write its record; nothing verifies a non-producer *cannot*. Live: `T-001.write_scope` reaches `R-002`…`R-006`, five result records it does not produce, and `X-09` emits nothing. The check states the invariant it protects — *"a result has exactly one producer, and with two the `produced_by` a consumer checks cannot be derived"* (`checks.py:630–633`) — then tests it against `produces` declarations only, never against `write_scope` reach. With `FIND-Q9-38` H1 this is concrete: `T-001 x T-002` is PARALLEL, so `T-001` may publish `R-002` beside its declared producer with all nine checks clean | `src/aief_exec/checks.py:611–634` | `software.software-engineer` |
| **FIND-Q9-40** | MINOR | `Plan.parallel_sets` is documented as producing *"Maximal groups"*. It is first-fit greedy in identifier order, which does not produce maximal cliques. No safety consequence — `X-07` re-verifies pairwise — but the docstring overstates the algorithm | `src/aief_exec/graph.py:569–571` | `software.software-engineer` |
| **FIND-Q9-41** | MINOR | `build_plan` evaluates `CONFLICT` before `BLOCKED`, so a pair is reported CONFLICT when one member is permanently BLOCKED or `COMPLETE` and can never be co-dispatched. Inflates the hazard report; does not unsafe it | `src/aief_exec/graph.py:631–641` | `software.software-engineer` |

**Ambiguities recorded, not resolved — LAW-12.**

1. **Open decision A4 is load-bearing for `FIND-Q9-42`.** Whether `produces` implies a write grant
   is undecided, and until it is, whether `T-001`'s reach over `R-002`…`R-006` is a defect or an
   intended super-user scope cannot be settled from the repository. I record the reach and the
   silence; I do not rule on the grant.
2. **`FIND-Q9-36` has two lawful repairs and the repository does not choose between them** —
   exclude self-written paths from `acquisition`, or forbid a task's own record from lying inside
   its write scope. The second collides with the checkpoint-update obligation in
   `TPL-task-package`. This is a `chief-systems-engineer` question, not a coding one.
3. **`T-004` cannot lawfully update its own checkpoint.** Its `write_scope` is
   `.ai/project/verification/VER-009_*.md` alone, which does not cover
   `.ai/project/tasks/T-004.md`, yet the record carries a `checkpoint` block with `pending` items.
   I did not edit it. Whether the template obligation or the scope declaration governs is a
   `project-manager` question.

**No finding is BLOCKING.** The layer does what it was built to do; every finding above is a
statement about the *margin* of what it certifies, and four of them are cases where the artefact
claims a stronger property than it delivers.

---

## 29 · Disposition — pass 5

> ### VERIFIED WITH FINDINGS
>
> The repair is real, and on three of five defect classes it is correct at the root. It is
> **over-claimed in its own documentation on three counts**, and the recurring defect class
> this audit has now tracked across five passes — *a closure asserted in stronger terms than it
> was tested in* — is present again.

**What holds, verified by evidence I generated.**

* **Defect 5 is fully repaired**, and repaired well enough to be an instrument: `safety_explanation`
  is how I found `FIND-Q9-38` H2. An explanation that lets an auditor falsify the verdict it
  explains is doing exactly its job.
* **Defect 1's detector is correct at the root.** Both `X-09` failures are honest findings about
  the repository. A task cannot declare an impossible result and pass; a consumer cannot consume a
  result no task produces.
* **Defect 4's per-record seal is sound.** All three sealed links `R-008`→`R-009`→`R-010`→`R-011`
  recomputed independently by `hashlib.sha256` and by `records.file_dc1`, both agreeing, all three
  **MATCH**. `R-011` is **CURRENT**. The epoch is honestly derived and not evaded.
* **Defect 3's deliverable channel is genuinely fixed** — 542 → 542 across deliverable creation.
* **`X-04` is untouched and the derived grant is enforced nowhere**, established by static
  reference audit, by a maximal-grant mutation that moved no verdict and no detail, and by a
  positive control proving the harness can see an enforcement change. **A4 is not pre-empted.**
* **The test suite is not weakened.** 16 of 16 mutants killed, no survivors, both historical
  regressions guarded, one suspected tautology hypothesised and disproved.

**Why not VERIFIED without qualification.** Not because the layer fails — it does not; seven of
nine checks pass and the two failures are true. Because of the pattern in §21 and §28: **three of
the five repairs assert a property stronger than the one they establish, and each overstatement is
in the artefact a reader would consult first.**

* `EXECUTION_ARCHITECTURE.md:323` — *"Stable across the task's own execution"* — false, by 145 %
  on a constructed case and by 24 % on a live `X-08` failure.
* `graph.py:162–164` — *"tampering can only add the alarm, never remove it"* — false; deleting
  three fields returns `X-06` to PASS with zero details.
* `graph.py:569` — *"Maximal groups"* — first-fit greedy.

These are not the same as a wrong number. **A disclosure that understates the limit is worse than
no disclosure, because it terminates the reader's inquiry** — §1 of this report set that standard
in pass 1 and it is the standard applied here. `FIND-Q9-39` is the sharpest instance: the code
asserts monotonicity in the exact words `FIND-Q9-27` was raised to obtain, and the property does
not hold one level up.

**The structural observation, offered as judgement rather than as a finding.** The cost model
enumerates five surfaces a task touches; the hazard model compares three. Every escape in §23.2
except E5 is a surface the same codebase already computes, in the same package, and drops before
the comparison. `FIND-Q9-38` is therefore one fix, not four — and the same asymmetry explains
`FIND-Q9-36`: `charged_context` computes `non_monotonic` over all five components and then reports
it as though it described one.

**Escalations.** `FIND-Q9-36`, `36b`, `37`, `38`, `40`, `41`, `42` to `software.software-engineer`;
`FIND-Q9-37` jointly to `project-manager` (the caps are a project-manager decision and cannot be
set against a measure that bounds half the input). `FIND-Q9-39` to `software.software-engineer`
and `chief-systems-engineer` — a tamper control that can be disabled by the tamper is a framework
question, not a module one. LAW-12 items 1–3 in §28 to `chief-systems-engineer` and
`project-manager`.

**What I did not reach.** Stated so no reader mistakes silence for coverage.

1. `src/aief_exec/__main__.py` was audited only for the `classify`, `scope` and `measure` paths
   relevant to defects 1, 4 and 5. `brief` and `status` were not exercised.
2. `EXECUTION_ARCHITECTURE.md` was checked for agreement with the code at §5.3, §11 (`acquisition`
   / `revision`) and §12 (`X-08`, `X-09`). §5, §14 and the rest of §12 were not line-audited.
3. Test quality was established by mutation against sixteen mechanisms. I did not read all 228
   tests, so a test that is redundant or misnamed without being regression-blind would not appear
   here.
4. `R-009`, `R-010` and `R-011` were verified for seal integrity and currency. Their **prose
   conclusions** were deliberately not read, to keep this pass cold; consequently this report
   disposes the repair, not the records' accounts of it.
5. The two red Stage 6 tests (`test_v24_live_registry`, `test_full_pipeline_with_stub_families`)
   are excluded by contract as an unrelated registry defect owned elsewhere. Not examined.
6. `FIND-Q9-38` E1 and E2 were demonstrated on constructed pairs; I did not search the live tree
   exhaustively for further instances of either.

**Footprint, confirmed after writing.** `check` → **7 of 9 PASS**, `X-08` and `X-09` failing
exactly as at baseline with identical detail sets. `pytest tests/test_exec_*.py` → **228 passed**.
`R-011` → still **CURRENT**. `git status --porcelain` → exactly **7** tracked modifications, the
same seven as at session start. Nothing under audit was modified; no defect found here was
repaired — **LAW-05: QA does not fix.** All mutation copies (`wt1`, `wt2`, `wt3`) discarded.

**Verifier attestation — pass 5.** Every figure in §§20–29 was produced by a command or a direct
library call executed in session `S-2026-08-09-09` against this repository or a throwaway copy of
it. No disposition rests on a claim in `R-009`, `R-010`, `R-011`, the `T-001` checkpoint, or
§§1–19 of this report. Each of the five defect classes was reproduced before its repair was
assessed. I verified no artefact I produced, and I modified no artefact under audit. This report
is subject to review at `.ai/project/reviews/DR-003_VER-009_Disposition.md` by
`chief-systems-engineer`.

*Filed by `qa-engineer · S-2026-08-09-09` under task `T-004`, on the enumerated `role_authority`
grant `EXEC-D-001` recorded at `.ai/project/tasks/T-001.md`. Write scope exercised: this file
only.*

---

# PASS 6 — cold independent verification of the corrections to the pass-5 findings

## 30 · Pass 6 — scope, method and footprint

**Pass 6 verifies the correction pass filed against the eight pass-5 findings** (`FIND-Q9-36`,
`36b`, `37`, `38` with escapes E1/E2/E3, `39`, `40`, `41`, `42`). Sections §1–§29 are the record of
passes 1–5 and are **not amended**; pass 6 begins here.

| | |
|---|---|
| Verifier | `qa-engineer`, session `S-2026-08-09-11`, cold context |
| Authority | `role_authority` grant `EXEC-D-001`, recorded at `.ai/project/tasks/T-001.md`, cited by `T-004` |
| Repository | `D:\Fusion Projects\SEWCP_Master_Assembly`, HEAD `8546960`, working tree uncommitted |
| Subject | `src/aief_exec/**`, `tests/test_exec_*.py`, `EXECUTION_ARCHITECTURE.md`, `R-012` (new, supersedes `R-011`), `.ai/project/tasks/{T-001,T-004}.md` |
| Method | **Reproduce each pass-5 defect against the current code before accepting any closure.** A finding that stops reproducing for an unrelated reason is not a fix |
| Footprint | Read-only on the repository except this file. All perturbation on a throwaway copy at `scratchpad/wt1`, or in-process monkeypatches that never touched disk |
| Baseline | `check` → **7 of 9 PASS**; `X-08` and `X-09` FAIL. `pytest tests/test_exec_*.py` → **257 passed** (pass 5 measured 228; +29) |

**Independence.** I received the contract and the changed-artefact list — not the implementer's
conclusions, and not a statement that anything works. No disposition below rests on a claim in
`R-012` or in §§1–19 of this file, neither of which I read before forming the view recorded here.
Every number was produced by a command or a direct library call executed in this session.

---

## 31 · `FIND-Q9-39` — the strip-all-seals attack, re-run

**The mechanism changed.** `graph.seal_epoch` no longer computes `min()` over sealing records; it
returns the module constant `SEAL_EPOCH = "S-2026-08-09-06"` (`graph.py:93`, `:166`), and the old
derivation survives as `derived_seal_epoch` (`graph.py:96–113`), used only as **evidence**.

**The pass-5 attack, re-run verbatim on `scratchpad/wt1`** — the `supersedes_seal` block deleted
from `R-009`, `R-010`, `R-011` and `R-012` (the fourth is new since pass 5):

```
X-06  FAIL   Result currency
  FAIL R-009: supersedes R-008 and pins no supersedes_seal, but was published at session
       S-2026-08-09-06, at or after S-2026-08-09-06 ...
  FAIL R-010: ... session S-2026-08-09-07 ...
  FAIL R-011: ... session S-2026-08-09-08 ...
  FAIL R-012: ... session S-2026-08-09-10 ...
  note seal epoch: declared S-2026-08-09-06 ...; earliest seal actually present in the records
       is NONE - no record carries a supersedes_seal ... one that has emptied while sealed
       supersessions existed means seals have been removed
6 of 9 PASS
```

Pass 5 obtained `X-06 -> PASS, details: NONE` from the same edit. **The attack no longer works, and
the tamper now produces both the four failures and a notice naming the tamper signature
explicitly. `FIND-Q9-39` is CLOSED AT ROOT for the vector it was raised on.**

### 31.1 Two other disarming inputs the tamperer still controls

The finding was raised as a *class* — a control whose evidence base is inside the set of files the
tampering party is already editing. Pinning the epoch removes one input from that set. It does not
remove the others. Both of the following were executed on `wt1`, from a clean baseline each time.

**D1 — delete the successor's `supersedes:` declaration. `FIND-Q9-43`, MAJOR. Not disclosed
anywhere.** Two lines removed from `R-012` (`supersedes: R-011` and its `supersedes_seal` block):

```
X-01 PASS  X-02 PASS  X-06 PASS   7 of 9 PASS
note R-011: unsealed - no record declares that it supersedes this one, so a rewrite after
     supersession cannot be detected here; the successor should carry supersedes_seal
```

Then, still under D1, I appended a paragraph reading `TAMPERED: this paragraph was appended after
supersession.` to `R-011` itself:

```
X-06  PASS   7 of 9 PASS      (no REWRITTEN alarm, no detail, no new notice)
```

The epoch rule at `checks.py:380–391` is guarded by `if result.supersedes and not <seal>`. The
tamperer controls `result.supersedes`. Emptying it is cheaper than emptying the epoch was: **one
line, one record, and the predecessor becomes freely rewritable with the check green.** The
seal-epoch repair hardened the *discriminator* and left the *trigger* under the same hand.

**The repository holds the evidence to detect D1 and discards it.** `R-011` carries
`superseded_by: R-012` (`.ai/project/results/R-011.md:18`) — the predecessor's own half of the same
link. `grep -rn superseded_by src/aief_exec tests/test_exec_*.py` returns **nothing**: the field is
never parsed, never compared, never tested. `X-06` already fails the mirror asymmetry — a record
declaring `CURRENT` while a successor supersedes it (`checks.py:406–412`) — and does not fail the
one that matters here: a record declaring `status: SUPERSEDED` with `superseded_by: R-nnn` while
`R-nnn` declares nothing. Under D1 `derived_status` returns `SUPERSEDED` **from the record's own
status field**, so the code has already concluded the record is superseded at the moment it decides
there is no successor to seal it.

**D2 — backdate the successor's session. Disclosed residual, confirmed live.** `R-012.produced_by
.session` changed from `S-2026-08-09-10` to `S-2026-08-09-01`, seal stripped:

```
X-06  PASS   7 of 9 PASS
note R-012: supersedes R-011 and pins no supersedes_seal. Session S-2026-08-09-01 predates
     S-2026-08-09-06, so this is history and is reported, not failed
```

This one is **honestly disclosed** — `seal_epoch`'s docstring, residual 2 (`graph.py:158–161`),
states it in terms. I record it as confirmed rather than as a finding, with one qualification: the
disclosure lives in `graph.seal_epoch`, and `x06_result_currency`, the check a reviewer reads,
repeats only the FIND-Q9-39 story and not this residual.

**Summary.** The epoch is no longer disarmable. The control as a whole still is, by a different
field, and the undisclosed vector D1 is the cheaper of the two.

---

## 32 · `FIND-Q9-38` — is the shared enumeration real, and is it drift-proof?

### 32.1 The enumeration is real

`scope.acquisition_units` (`scope.py:508–552`) returns `(component, path, anchor)` for `record`,
`mandatory`, `optional` and `dependency`. It has exactly two callers, verified by
`grep -rn acquisition_units src/aief_exec`:

* `scope.charged_context:847` — the cost model, which filters `mandatory`/`optional` to the units
  that resolve and then charges them;
* `graph.read_surface:490` — the hazard model, which compares them.

One function, two callers, and no second enumeration of the acquisition surface anywhere in the
package. **The claim is true as stated.**

### 32.2 The escapes, re-tested by matched-pair control

Synthetic pairs built in-process against the live tree — no file written — and classified through
`graph.conflict_reasons`:

| Case | Pair | Pass-5 verdict | Pass-6 verdict |
|---|---|---|---|
| E1 | writer of `EXEC.md` × reader declaring it **optional** | PARALLEL | **CONFLICT** `[write/read] (optional - a declared optional input)` |
| E1 control | same, declared **mandatory** | CONFLICT | **CONFLICT** — the two declaration classes now agree, which is the whole content of the finding |
| E2 | writer of `.ai/project/results/R-012.md` × consumer of `R-012` | PARALLEL | **CONFLICT** `[write/read] (dependency - the result record whose currency it must confirm)` |
| E3 | writer of `.ai/project/tasks/**` × any task | PARALLEL | **CONFLICT** `[write/read] (record - the contract it is executing)` |
| Control | writer of `nowhere/**` × the same reader | PARALLEL | **PARALLEL** — no false CONFLICT |

**Live, on the real tree**, the two hazards pass 5 found without construction:

```
T-001 x T-002  ->  CONFLICT   [write/read] ... (record - the contract it is executing):
                              .ai/project/tasks/T-002.md
T-001 x T-005  ->  CONFLICT   [write/read] ... (record - the contract it is executing):
                              .ai/project/tasks/T-005.md
```

**H1 CLOSED AT ROOT. E1, E2, E3 CLOSED AT ROOT.**

**H2 / E4 remains open**, and is disclosed as open: `classify T-002 T-004` is still **PARALLEL**,
`T-002.write_scope` still contains `src/aief_stage6/tokenizers.py`, and `scope.py:22` still imports
it as the measurement backend. `read_surface`'s docstring names this exact case as not closed and
says why (it needs an import graph, not a declared scope). Honest, and not a regression.

### 32.3 Charged but not compared: none. Compared but not charged: eleven paths on `T-004`

Computed directly for `T-004`:

```
CHARGED NOT COMPARED      : []
COMPARED NOT CHARGED (obs): .ai/project/verification/VER-009_*.md, src/aief_exec/{__init__,
  __main__,checks,graph,records,scope}.py, tests/test_exec_{records,scope,graph,checks}.py
```

The asymmetry pass 5 found — cost model five surfaces, hazard model three — is **inverted, not
eliminated**. Everything charged is now compared. What is compared and not charged is
`observed_surface` terms 2–4, and `observed_surface` is its own enumeration (`graph.py:423–443`)
with a single caller in the hazard model and no counterpart in the cost model.
`acquisition_units`' docstring says *"Nothing else may enumerate the acquisition surface"*, which is
accurate and narrower than the reader's likely inference: the *observation* surface is enumerated
once too, but only on one side. I record this as an observation, not a finding — charging term 3
would over-charge a consumer that genuinely reads only the conclusion, which §6 permits, and pass 5
already accepted the term as erring in the safe direction.

### 32.4 The drift vector that remains — `FIND-Q9-44`, MINOR

`acquisition_units` does **not** iterate `ACQUISITION_COMPONENTS`. It hardcodes `("record", …)`, a
literal `for kind in ("mandatory", "optional")`, and a `dependency` loop (`scope.py:540–551`),
while `ChargedContext.acquisition` sums over the constant tuple (`scope.py:501`, `:704`). These are
two independent declarations of the same set and nothing asserts they agree. The claim the
docstring makes — *"Adding a component means adding it here, and both models acquire it in the same
edit"* — holds for the two **models** and not for the two **declarations**. Verified by mutation in
§35.

---

## 33 · Result chain `R-009` → `R-010` → `R-011` → `R-012`, by recomputation

Every seal recomputed twice: once through `records.file_dc1`, and once through an implementation of
the DC-1 normalisation rule I wrote in this session from its stated text (*"decode UTF-8 stripping
any byte-order mark; convert CRLF and lone CR to LF; strip trailing whitespace from every line;
remove trailing blank lines; append exactly one terminal LF"*), so the two paths share no code.

| Link | Digest pinned by the successor | Independently recomputed | Verdict |
|---|---|---|---|
| `R-001` → `R-007` | *none* | `61752b84764cf689…` | **UNSEALED** — session `-01`, pre-epoch, correctly a notice |
| `R-007` → `R-008` | *none* | `30e975012de30147…` | **UNSEALED** — session `-01`, pre-epoch, correctly a notice |
| `R-008` → `R-009` | `e081eb7b9370afe9…` | identical, both methods | **MATCH** |
| `R-009` → `R-010` | `6cc1c3efcd0d14e0…` | identical, both methods | **MATCH** |
| `R-010` → `R-011` | `45516365790fd220…` | identical, both methods | **MATCH** |
| `R-011` → `R-012` | `a74a507e1daca9d7…` | identical, both methods | **MATCH** |

`R-012`'s own currency, recomputed rather than read: **7 pinned inputs and 11 pinned deliverables,
zero mismatches.** `derived_status(R-012)` = `CURRENT`; every other record derives `SUPERSEDED` and
declares `SUPERSEDED`. `seal_epoch` declared `S-2026-08-09-06`, `derived_seal_epoch`
`S-2026-08-09-06` — the two agree, so the disagreement notice correctly stays silent. **`R-012` is
CURRENT.** `VER-009` is not among `R-012`'s pins, so writing this file does not move its currency.

A caution for any later verifier: a raw `hashlib.sha256` over file bytes is **not** DC-1 and
disagrees on any file with CRLF line endings — it reports a false mismatch on
`tests/test_exec_graph.py`. Pass 5's "raw `hashlib.sha256`" cross-check agreed only because the
records it covered are LF-only. The normalisation must be applied.

---

## 34 · `FIND-Q9-36`, `36b`, `37` — is `total_measurable` honest, and does the gate still mean anything?

### 34.1 `FIND-Q9-36` — the movement survives, the false claim does not

The pass-5 synthetic case, rebuilt from scratch on `wt1`: a task whose record lies inside its own
`write_scope`, measured before and after it appends one progress note to its own checkpoint.

```
BEFORE : acquisition TF-1 198   stable TF-1 0   self-referential TF-1 198
AFTER  : acquisition TF-1 999   stable TF-1 0   self-referential TF-1 999      (+405 %)
moving_by_component: [('mandatory', 'in/stable.md'), ('record', 'T-900.md')]
```

**The gated quantity still moves under the task's own hand.** The repair did not remove the
movement — deliberately, and it says so: removing `record` from the gate would make the number
invariant and the measurement false. What it removed is the false claim and the invisibility:

* `EXECUTION_ARCHITECTURE.md:392` now reads *"A dispatch-time measurement, not an invariant"*, and
  `:396–410` states the falsification in terms, with the 145 % figure and the live 34 % / 24 %.
* `ChargedContext.acquisition`'s docstring (`scope.py:575–600`) carries the same correction.
* `acquisition_stable` / `acquisition_self_referential` split the figure on exactly the line that
  matters, and every `X-08` row prints both.

**Disposition: CLOSED AT SYMPTOM.** The documentation limb is closed at root — no artefact now
claims invariance. The measurement limb is *not closed*, is correctly disclosed, quantified in two
places, and escalated as a `chief-systems-engineer` question rather than resolved by assumption.
That is the right handling of the LAW-12 item pass 5 recorded, and I re-record it: still open.

### 34.2 `FIND-Q9-36b` — the misattribution is gone

`cc.moving_by_component()` (`scope.py:679–695`) attributes each moving path to the component that
holds it, and `checks.py:640–650` prints the count in a clause of its own rather than appended to
the `revision` clause. Live, for the task the finding was raised on:

```
T-002 [READY]: ... | revision TF-1 0 / TF-2 0 reported (nothing charged) | ...
  | non-monotonic in 2 path(s) inside this task's own write scope, by component:
    mandatory src/aief_stage6/budget.py; mandatory src/aief_stage6/lock.py | ...
```

The two moving paths are named as `mandatory`, `revision` is reported as zero beside them, and the
non-sequitur closing clause (*"…this is why `revision` is reported and `acquisition` is the gated
quantity"*) has been replaced by *"…so the gate is a DISPATCH-TIME measurement and not an invariant
of this task's execution"* (`scope.py:917–923`). **CLOSED AT ROOT.**

### 34.3 `FIND-Q9-37` — `total_measurable` exists, does not double-count, and is bounded

Verified by direct computation, not by reading the docstring:

* **No double count.** `charged_context` deduplicates units by `(path, anchor)` before charging
  (`scope.py:860–870`) and acquisition units are appended before deliverables, so a path that is
  both a read input and a deliverable is charged once, under the acquisition component. Measured on
  `T-004`: `cc.total == cc.acquisition + cc.revision`, exactly, and `total_measurable == total`.
* **The bound is a detail, not a notice** (`checks.py:622–633`), so it cannot be skimmed past, and
  every such row carries `NON-MONOTONIC BOUND, not the acquisition gate`.
* **Suppression when `revision == 0`** is correct on its own terms: the bound and the gate are then
  the same number over the same cap.

**Is the acquisition gate still meaningful? As a reported quantity, yes. As a gate, its distinctness
does not survive to the verdict — `FIND-Q9-45`, MAJOR.**

`total_measurable ≥ acquisition` always, and both are compared against the *same* cap, and both
land in the same `details` list (`checks.py:599`). Therefore:

* `X-08` fails **iff** some task's `total_measurable` breaches its cap. The acquisition verdict
  contributes nothing to the check's boolean that the bound does not already contribute.
* Nothing separates the two structurally. `_result` returns `details` as a list of plain strings;
  the only discriminator is the substring `NON-MONOTONIC BOUND` inside English prose. A human can
  tell the rows apart, which is what the docstring claims; **a consumer of `X-08["status"]` or of
  `details` cannot.**

**And the consequence is live and non-monotonic.** `T-005`, measured on `wt1`:

| `wt1` state | `X-08` rows for `T-005` |
|---|---|
| `tests/test_stage6_crash_trials.py` (T-005's own deliverable) **absent** | **none** — gate 1,411 ≤ 1,500, bound 1,411 ≤ 1,500 |
| the same file **present**, i.e. after `T-005` did its job | **two FAILs** — `total_measurable TF1 7161 > 1500`, `TF2 9763 > 2000` |

`T-005`'s acquisition gate passes in both states. The only reason `X-08` fails on `T-005` is that
`T-005` wrote its deliverable. **A check verdict that a task moves by doing its own work is the
`FIND-Q9-35`-successor defect the split was built to retire, reinstated one level up** — at the
check's PASS/FAIL rather than at the gate. The repair is aware of the quantity's non-monotonicity
and labels it in prose; what it does not do is keep that quantity out of the verdict a machine
reads. `test_x08_fails_on_the_cost_the_gate_excludes` (`test_exec_checks.py:942`) and
`test_x08_measures_an_existing_deliverable_without_gating_on_it` (`:870–927`) both assert this behaviour as
intended, so the suite locks it in.

This is a **finding about the design of the bound, not about the measurement**, and it is entangled
with a `project-manager` decision (§28's LAW-12 item on the caps). I record it and do not rule on
the repair: bounding `revision` against a second, separately declared cap, or emitting the bound as
a structurally distinct verdict class rather than a `details` string, are both lawful and the
repository chooses neither.

### 34.4 The split notice asserts a failure that was suppressed — `FIND-Q9-46`, MAJOR

`checks.py:656–658` emits, for **every** task in **every** state, unconditionally:

```
| total_measurable {cc.total_measurable} BOUNDED by the same cap and failed separately |
```

There is no condition on an actual breach and none on the suppression at `checks.py:622`. Live,
right now, for the three tasks whose `revision` is zero:

```
T-002 [READY]: ... | total_measurable TF-1 12880 / TF-2 16680 BOUNDED by the same cap and
               failed separately | ...
T-003 [BLOCKED]: ... | total_measurable TF-1 8193 / TF-2 9939 BOUNDED ... failed separately | ...
T-006 [BLOCKED]: ... | total_measurable TF-1 12154 / TF-2 14641 BOUNDED ... failed separately | ...
```

`grep ": total_measurable " ` over the whole `X-08` detail list returns rows for `T-004` and
`T-005` only. **No separate failure was emitted for `T-002`, `T-003` or `T-006` — the check
deliberately suppressed it — and the notice tells the reader one was.** It is false in the other
direction too: on `wt1` with `T-005`'s deliverable removed, `T-005` breaches nothing and its notice
still reads *"total_measurable TF-1 1411 / TF-2 1714 BOUNDED by the same cap and failed
separately"*.

This is the `FIND-Q9-36b` defect class exactly — an emitted line that states a falsehood about the
tree the reader is looking at — reintroduced by the sentence written to close `FIND-Q9-37`.
`test_x08_does_not_double_report_when_revision_is_zero` (`test_exec_checks.py:985–997`) asserts the
suppression and asserts that the notice still *mentions* `total_measurable`; it does not assert
that what the notice says about it is true, which is why a green suite does not see this.

---

## 35 · Test integrity — twenty-one mutants, and a kill floor nobody subtracted

**The suite is 257 tests, up from pass 5's 228.** All 257 pass at baseline on the live tree and on a
clean copy.

### 35.1 The control pass 5 did not run

Every mutation campaign against this package has an artefact nobody has accounted for. `R-012` pins
`src/aief_exec/*.py` as deliverables, and three live-tree tests recompute those pins. **A
semantically inert edit therefore kills three tests.** Measured, by appending
`# semantically inert comment added by the auditor` to `scope.py`:

```
3 failed, 254 passed
  test_exec_checks.py::TestLiveRepositoryOpenFailures::test_x02_open_on_the_consumer_of_a_staled_result
  test_exec_checks.py::TestLiveRepositoryOpenFailures::test_x06_open_on_the_result_that_pins_the_layer_it_describes
  test_exec_graph.py::TestLivePlan::test_the_live_dependency_state_is_derived_end_to_end
```

**The kill floor is 3, and it must be subtracted from every mutant's failure count.** Pass 5
reported sixteen kills as low as four failures without this control. I re-derive my own scores
against the floor and, where a mutant scored close to it, against the failing test *names*.

### 35.2 The campaign

Twenty-one mutants, each applied and reverted in isolation on `scratchpad/wt1`:

| # | Mutant | Failures | Verdict |
|---|---|---|---|
| MU1 | `SEAL_EPOCH = ""` | 8 | KILLED |
| MU2 | `seal_epoch` reverts to the `min()` derivation — **the FIND-Q9-39 defect** | 6 | KILLED |
| MU3 | `read_surface` compares `mandatory` only — **the FIND-Q9-38 defect** | 10 | KILLED |
| MU4 | `acquisition_units` drops `optional` | 5 | KILLED |
| MU5 | `acquisition_units` drops `record` | 14 | KILLED |
| MU6 | `acquisition_units` drops `dependency` | 5 | KILLED |
| MU7 | `X-08` stops emitting the `total_measurable` verdict — **the FIND-Q9-37 repair** | 6 | KILLED |
| MU8 | `acquisition_self_referential` always zero — **the FIND-Q9-36 disclosure** | 6 | KILLED |
| MU9 | `moving_by_component` always empty — **the FIND-Q9-36b attribution** | 7 | KILLED |
| MU11 | `deliverable` added to `ACQUISITION_COMPONENTS` | 12 | KILLED |
| MU12 | `REVISION_COMPONENTS = ()` | 11 | KILLED |
| MU13 | `observed_surface` drops declared `observes` | 6 | KILLED |
| MU14 | **`telemetry` added to `ACQUISITION_COMPONENTS`** — a name the enumeration never emits | **3** | **SURVIVED** |
| MU15 | `acquisition_units` emits a kind neither constant lists | 12 | KILLED |
| MU16 | `X-09` drops mode 5, the undeclared-writer reach — **the FIND-Q9-42 repair** | 6 | KILLED |
| MU17 | `session >= epoch` → `session > epoch`: a supersession exactly *at* the epoch escapes | 5 | KILLED — by `test_stripping_every_seal_does_not_disarm_the_rule` and `test_a_supersession_at_or_after_the_epoch_fails` |
| MU18 | `COMPONENT_HAZARD["record"]` misnamed | 4 | KILLED — by `TestReadSurface::test_a_tasks_own_record_is_compared` |
| MU19 | the FIND-Q9-41 reorder discards scope reasons on a blocked pair | 4 | KILLED — by `TestPairClassOrdering::test_a_blocked_pair_reports_blocked_and_keeps_the_scope_reasons` |
| MU20 | `X-06` stops failing an unsealed post-epoch supersession | 8 | KILLED |
| MU21 | `X-08` never turns a breach into a failure | 10 | KILLED |

**20 of 21 killed. One survivor, and it is the drift vector of `FIND-Q9-44`:** MU14's three failures
are the three pin-drift tests and nothing else, so adding a component name to
`ACQUISITION_COMPONENTS` that `acquisition_units` never emits is invisible to the suite. The
symmetric mutation MU15 — a kind emitted by the enumeration and named in neither constant — *is*
caught, by the `total == acquisition + revision` cross-check. The asymmetry is exactly the one §32.4
describes: the enumeration is shared between the two **models**, and the two **declarations** of the
component set are not tied to each other in either direction of edit.

### 35.3 Fixture avoidance — the pass-5 pattern, hunted and not found again

Pass 5 found `TestBudgetSplit._task` (`test_exec_scope.py:394–404`) placing the task record at
`d/task.md` outside `write_scope=("out/**",)` — the one configuration in which `acquisition` is
invariant — so the invariance test could not see `FIND-Q9-36`. **The correction pass did not move
that fixture and did not need to.** It added `TestAcquisitionIsNotInvariant` (`:488`), whose
`_task` places the record at `.ai/project/tasks/T-0W.md` **inside** `write_scope=(".ai/project/
tasks/**",)` — the avoided configuration, made the subject of its own class — and whose docstring
names the old fixture, states precisely what it does and does not establish, and says why it is not
weakened. `test_the_gate_moves_when_the_task_appends_to_its_own_checkpoint` carries an assertion
message that fires *if the fixture stops reproducing the defect*, which is the correct guard
against this pattern recurring.

I re-read the fixtures behind each MAJOR-finding guard looking for the same shape:

* `TestX06SealEpoch._chain` builds `R-100`/`R-101` pre-epoch and `R-102`/`R-103` post-epoch, and
  `test_stripping_every_seal_does_not_disarm_the_rule` asserts `stripped == 2`,
  `derived_seal_epoch(results) == ""` (*"the tamper did not land"*) and then
  `offenders == ["R-102","R-103"]`. It cannot pass without the condition landing. No avoidance.
* `test_x08_fails_on_the_cost_the_gate_excludes` asserts both the presence of the bound row and the
  **absence** of an acquisition row, so it cannot be satisfied by folding `revision` into the gate.
  No avoidance.
* `test_mode_5_a_non_producer_reaching_a_result_record` and the live
  `test_x09_guards_the_publication_channel_in_both_directions` both exist; MU16 kills them.

**One fragility, not an avoidance — `FIND-Q9-47`, MINOR.**
`test_exec_scope.py:474 test_the_live_t005_shape_reproduces_the_incident` asserts
`cc.non_monotonic == ["tests/test_stage6_crash_trials.py"]`. That file is `T-005`'s in-flight
deliverable, untracked, and produced by a **concurrent session** — it is absent from the working
tree recorded at the start of this audit and present now. Removing it on `wt1` turns the suite red:

```
FAILED tests/test_exec_scope.py::TestBudgetSplit::test_the_live_t005_shape_reproduces_the_incident
1 failed, 256 passed
```

The suite's green state is a function of another session's uncommitted output. Two of the three
pin-drift tests have the same character in a milder form.

---

## 36 · New defects introduced by the correction pass

| ID | Severity | Finding | Exact site |
|---|---|---|---|
| **FIND-Q9-43** | **MAJOR** | **The supersession seal is still disarmable, by the `supersedes` field instead of the epoch, and this vector is disclosed nowhere.** Deleting `supersedes: R-011` and its seal from `R-012` on a scratch copy returns `X-06` to **PASS** with a single notice, after which appending `TAMPERED: …` to `R-011` produces **no alarm at all** — verified end to end. The epoch rule is guarded by `if result.supersedes and not <seal>`, and `result.supersedes` is under the tamperer's hand. The repository holds the contradicting evidence and discards it: `R-011` carries `superseded_by: R-012`, and `grep -rn superseded_by src/aief_exec tests/test_exec_*.py` returns nothing. `X-06` fails the mirror case — declared `CURRENT` under a successor (`checks.py:406–412`) — and not this one | `src/aief_exec/checks.py:380`, `:406–412`; `src/aief_exec/graph.py:184–264`; `.ai/project/results/R-011.md:18` |
| **FIND-Q9-45** | **MAJOR** | **The acquisition gate and the `total_measurable` bound are distinguishable only by substring, and the bound makes the `X-08` verdict non-monotonic in the task's own work.** Both verdicts are compared against the same cap and appended to the same `details` list (`checks.py:599`), so `X-08` fails **iff** some `total_measurable` breaches — the gate adds nothing to the boolean — and the only discriminator is the English phrase `NON-MONOTONIC BOUND` inside a detail string. Live consequence: `T-005` has **zero** `X-08` rows before it writes its deliverable and **two FAILs** after, with its gate under cap in both states. The non-monotonic quantity the split removed from the gate now decides the check's verdict | `src/aief_exec/checks.py:589–604`, `:612–633`; `src/aief_exec/checks.py:19` (`_result`) |
| **FIND-Q9-46** | **MAJOR** | **The split notice claims a separate failure that the check suppressed.** `checks.py:656–658` appends `total_measurable {…} BOUNDED by the same cap and failed separately` unconditionally, with no test on a breach and none on the suppression at `:622`. Live, `T-002`, `T-003` and `T-006` carry that sentence while `X-08`'s detail list contains **no** `total_measurable` row for any of them. False in the other direction too: a task under cap prints it as well. This is the `FIND-Q9-36b` class — an emitted line false about the tree the reader is looking at — reintroduced by the sentence written to close `FIND-Q9-37` | `src/aief_exec/checks.py:651–660` |
| **FIND-Q9-44** | MINOR | **The component set is declared twice and the two declarations are untied.** `acquisition_units` hardcodes `record`, a literal `("mandatory","optional")` loop and `dependency` (`scope.py:540–551`) while `ChargedContext.acquisition` sums `ACQUISITION_COMPONENTS` (`:501`, `:704`). Adding a name to the constant that the enumeration never emits is charged nowhere, compared nowhere and **survives the whole suite** (mutant MU14, §35.2). The docstring's *"Adding a component means adding it here, and both models acquire it in the same edit"* is true of the two models and not of the two declarations | `src/aief_exec/scope.py:501`, `:508–552` |
| **FIND-Q9-47** | MINOR | **The suite's green state depends on a concurrent session's uncommitted file.** `test_the_live_t005_shape_reproduces_the_incident` asserts `cc.non_monotonic == ["tests/test_stage6_crash_trials.py"]`; that file is `T-005`'s in-flight deliverable, untracked, absent from the tree at the start of this audit. Removing it turns the suite red. Related: three tests (`TestLiveRepositoryOpenFailures::test_x02_…`, `::test_x06_…`, `TestLivePlan::test_the_live_dependency_state_is_derived_end_to_end`) fail on **any** byte change to a file `R-012` pins, so the suite cannot be green while the module it guards is being repaired, and any mutation score against this package carries a floor of 3 | `tests/test_exec_scope.py:474–485`; `tests/test_exec_checks.py` `TestLiveRepositoryOpenFailures`; `tests/test_exec_graph.py` `TestLivePlan` |
| **FIND-Q9-48** | MINOR | **The seal epoch's external anchor is cited to the wrong section.** `graph.py:143` and the `X-06` notice at `checks.py:367–368` both state the constant is *"recorded at EXECUTION_ARCHITECTURE.md section 6.1"*. §6.1 is *"Immutability without new machinery"*; the epoch is recorded at **§6.2**. The citation is emitted to the operator on every run in which the derivation and the constant disagree — that is, in exactly the tamper case the notice exists to report | `src/aief_exec/graph.py:143`; `src/aief_exec/checks.py:367–368`; `.ai/project/EXECUTION_ARCHITECTURE.md:229`, `:248` |

**Ambiguities recorded, not resolved — LAW-12.**

1. **Pass 5's LAW-12 item 2 is still open and is now load-bearing for `FIND-Q9-45`.** The repository
   still does not choose between excluding self-written paths from `acquisition` and forbidding a
   task's own record from lying inside its write scope. The correction pass disclosed the movement
   rather than choosing, which is correct under LAW-12, and `FIND-Q9-45` shows the same undecided
   question now reaching the check's verdict through `total_measurable`. A
   `chief-systems-engineer` question.
2. **Whether a second cap should bound `total_measurable`.** `checks.py:529–531` and
   `EXECUTION_ARCHITECTURE.md:543–544` both decline to invent one, citing LAW-12, and use the
   acquisition cap. That is the right refusal, and it is also the direct cause of `FIND-Q9-45`'s
   verdict collapse. A `project-manager` decision, not a coding one.
3. **Pass 5's LAW-12 item 3 stands unchanged.** `T-004` still cannot lawfully update its own
   checkpoint: `write_scope` is `.ai/project/verification/VER-009_*.md` alone, and
   `.ai/project/tasks/T-004.md` still carries a `checkpoint` block with `pending` items. I did not
   edit it.
4. **`R-012` records that nine tests were "restated".** The changed files are untracked, so there is
   no committed predecessor to diff against, and I cannot verify a restatement from the repository.
   I verified the current 257 by mutation instead and record the count claim as unreachable.

---

## 37 · Disposition — pass 6

> ### VERIFIED WITH FINDINGS
>
> **Six of the eight pass-5 findings are closed at the root, one at the symptom, and one is
> closed at the root for the vector it was raised on while the class it was raised about
> survives through a different field.** The correction pass is materially better work than the
> repair it corrects: every closure I could attack held except where the code already says it
> does not, and the disclosures are, for the first time in this audit's history, narrower than
> the properties they describe rather than wider. Three new MAJOR defects were introduced, two
> of them in the sentences written to announce the closures.

| Pass-5 finding | Disposition | Evidence I generated |
|---|---|---|
| `FIND-Q9-36` | **CLOSED AT SYMPTOM** | Movement reproduces at +405 % on a rebuilt synthetic; the invariance claim is gone from `EXECUTION_ARCHITECTURE.md:392` and `scope.py:575–600`; `stable`/`self-referential` split verified to reconstruct the gate exactly. The measurement limb is open by disclosed, escalated choice |
| `FIND-Q9-36b` | **CLOSED AT ROOT** | `T-002`'s live notice now attributes both moving paths to `mandatory`, prints `revision 0` separately, and the non-sequitur clause is replaced. MU9 kills `moving_by_component` |
| `FIND-Q9-37` | **CLOSED AT ROOT, with a new defect in the repair** | `total_measurable` exists, is a detail not a notice, does not double-count (`total == acquisition + revision` measured on `T-004`), and MU7 kills its removal. See `FIND-Q9-45` and `FIND-Q9-46` |
| `FIND-Q9-38` H1/E1/E2/E3 | **CLOSED AT ROOT** | One enumeration (`acquisition_units`), two callers, verified by reference audit; matched-pair controls flip E1 from PARALLEL to CONFLICT on the declaration class alone; E2 and E3 likewise; the unrelated control stays PARALLEL; `T-001 x T-002` and `T-001 x T-005` are CONFLICT live. MU3 kills the reversion |
| `FIND-Q9-38` H2/E4 | **NOT CLOSED — disclosed** | `T-002 x T-004` still PARALLEL; named as open in `read_surface`'s docstring with the reason. Not a regression |
| `FIND-Q9-39` | **CLOSED AT ROOT for the vector; the class survives** | The strip-all-seals attack now yields `X-06 FAIL`, four named offenders and a tamper-signature notice, against pass 5's PASS/zero details. MU1, MU2, MU17 and MU20 all kill. But `FIND-Q9-43`: deleting the successor's `supersedes` line disarms the link entirely and lets the predecessor be rewritten with the check green |
| `FIND-Q9-40` | **CLOSED AT ROOT** | Docstring corrected to *"First-fit greedy in identifier order, and not maximal"*, with the reason the algorithm was not changed. A documentation finding correctly disposed by documentation |
| `FIND-Q9-41` | **CLOSED AT ROOT** | `BLOCKED` is now evaluated before `CONFLICT` and scope reasons are appended rather than discarded — verified live: `T-001 x T-003` is `BLOCKED` **and** carries the `[write/read]` reason. MU19 kills the discard. `X-07` is unaffected: it only inspects pairs inside `parallel_sets()`, which never contains a blocked member |
| `FIND-Q9-42` | **CLOSED AT ROOT** | `X-09` now emits five live details naming `T-001`'s reach over `R-002`…`R-006`, each naming the declared producer and each explicitly declining to decide A4. I confirmed the underlying reach by evaluating the globs myself. MU16 kills the mode |

**The two failing checks, judged.**

* **`X-09` — honest, both modes.** The five producer-cannot-publish failures are real: no pattern in
  those `write_scope` declarations matches the record the task is contracted to publish. The five
  new undeclared-reach failures are real: `T-001.write_scope` genuinely contains
  `.ai/project/results/**`. Reporting a `COMPLETE` task's reach as a failure rather than demoting it
  the way `X-08` demotes a `COMPLETE` task's overrun is deliberate and consistent with the reasoning
  at `graph.py:827–834` — the reach is a defect in the *declarations*, which no dispatch state
  repairs.
* **`X-08` — honest measurements, one dishonest sentence, one verdict it should not own.** Every
  acquisition breach is a real overrun of a real cap. The `total_measurable` breaches are real
  numbers too. `FIND-Q9-46` is a defect in the repair, not a finding about the repository, and
  `FIND-Q9-45` is a defect in what the check's verdict is allowed to depend on.

**What holds, verified by evidence I generated.** The result chain is intact and recomputed
independently — four seals MATCH, two pre-epoch links correctly reported rather than accused,
`R-012` CURRENT with all eighteen pins matching. The hazard model and the cost model read one
enumeration. The seal epoch cannot be moved by the records it polices. `X-04` and the A4 boundary
were not touched by this pass and I did not re-litigate them. The suite is 257 green with 20 of 21
mutants killed, the single survivor being a finding I filed rather than a gap I merely noted.

**Escalations.** `FIND-Q9-43` to `software.software-engineer` and `chief-systems-engineer` — a
tamper control disarmable by the tamper is a framework question and this is the second field it has
been found on. `FIND-Q9-45` to `software.software-engineer` and `project-manager` jointly.
`FIND-Q9-46`, `44`, `47`, `48` to `software.software-engineer`. LAW-12 items 1–2 to
`chief-systems-engineer` and `project-manager`; item 3 to `project-manager`.

**What I could not reach.** Stated so no reader mistakes silence for coverage.

1. `R-012`'s prose conclusion was deliberately not read before the findings above were formed, and
   its account of the repair is not disposed here. This pass disposes the corrections, not the
   record of them.
2. §§1–19 of this file were not read, by contract.
3. `src/aief_exec/__main__.py` was exercised on `scope`, `classify`, `status`, `measure` and `check`.
   `brief` was not exercised.
4. `EXECUTION_ARCHITECTURE.md` was checked for agreement with the code at §6.1/§6.2 (the epoch),
   §11 (the three quantities) and §12 (`X-08`, `X-09`). §5, §5.3, §7 and §14 were not line-audited.
5. The nine "restated" tests cannot be verified as restatements: the files are untracked and there
   is no committed predecessor to diff. LAW-12 item 4.
6. `FIND-Q9-38` E4 was confirmed still open but not further explored; I did not attempt to model an
   import graph or to enumerate other runtime-tooling pairs.
7. The two red Stage 6 tests are excluded by contract as an unrelated registry defect owned
   elsewhere. Not examined.
8. `FIND-Q9-43` was demonstrated on `R-011`/`R-012`. I did not enumerate every other field whose
   deletion degrades a failure to a notice; `supersedes` is the one I found, not provably the only
   one.

**Footprint, confirmed after writing.** `check` → **7 of 9 PASS**, `X-08` and `X-09` failing exactly
as at baseline. `pytest tests/test_exec_*.py` → **257 passed**. `R-012` → still **CURRENT**, all
eighteen pins recomputed and matching after this file was written. `git status --porcelain` → exactly
**7** tracked modifications, the same seven as at session start. Nothing under audit was modified;
no defect found here was repaired — **LAW-05: QA does not fix.** The mutation copy `wt1` was
discarded.

**Verifier attestation — pass 6.** Every figure in §§30–37 was produced by a command or a direct
library call executed in session `S-2026-08-09-11` against this repository or a throwaway copy of
it. No disposition rests on a claim in `R-012`, in the `T-001` or `T-004` checkpoints, or in
§§1–19 of this report. Each pass-5 defect was reproduced against the current code before its
closure was accepted, and each closure was attacked before it was granted. I verified no artefact I
produced, and I modified no artefact under audit. This report is subject to review at
`.ai/project/reviews/DR-003_VER-009_Disposition.md` by `chief-systems-engineer`.

*Filed by `qa-engineer · S-2026-08-09-11` under task `T-004`, on the enumerated `role_authority`
grant `EXEC-D-001` recorded at `.ai/project/tasks/T-001.md`. Write scope exercised: this file only.*

---

## 38 · Pass 7 — scope, method and footprint

**Pass 7 verifies the correction pass filed against the six pass-6 findings** (`FIND-Q9-43`,
`44`, `45`, `46`, `47`, `48`). Sections §1–§37 are the record of passes 1–6 and are **not
amended**; pass 7 begins here.

| | |
|---|---|
| Verifier | `qa-engineer`, session `S-2026-08-09-12`, cold context |
| Authority | `role_authority` grant `EXEC-D-001`, recorded at `.ai/project/tasks/T-001.md`, cited by `T-004` |
| Repository | `D:\Fusion Projects\SEWCP_Master_Assembly`, HEAD `8546960`, working tree uncommitted |
| Subject | `src/aief_exec/**`, `tests/test_exec_*.py`, `EXECUTION_ARCHITECTURE.md`, `R-013` (new, supersedes `R-012`), `.ai/project/tasks/{T-001,T-004}.md` |
| Method | **Reproduce each pass-6 defect against the current code before accepting any closure**, then attack the closure. Every kill count is reported net of a re-measured pin floor |
| Footprint | Read-only on the repository except this file. All perturbation on a throwaway copy at `scratchpad/wt1` |
| Baseline | `check` → **7 of 10 PASS**; `X-08`, `X-09`, `X-10` FAIL. `pytest tests/test_exec_*.py` → **275 passed** (pass 6 measured 257; +18) |

**Independence.** I received the contract and the changed-artefact list — not the implementer's
conclusions. No disposition below rests on a claim in `R-013` or in §§1–29 of this file, neither of
which I read before forming the view recorded here. Every number was produced by a command or a
direct library call executed in this session.

**The check set grew from nine to ten.** `X-10 · Non-monotonic bound on total measurable context`
is new (`checks.py:757`). That is the structural change behind the `FIND-Q9-45` repair and is
assessed in §39.

---

## 39 · `FIND-Q9-45` — is the gate now boolean-independent of the bound?

The pass-6 defect was not that the two rows were hard to tell apart in prose. It was that
`total_measurable ≥ acquisition` against the same cap in the same `details` list made `X-08` fail
**iff** some `total_measurable` breached, so the gate contributed nothing to the boolean and a
quantity the task moves by working decided the check.

### 39.1 The split is structural, not typographic

`x08_context_budget` (`checks.py:606–754`) now calls `_cap_verdict` **once**, on `cc.acquisition`
alone. The `total_measurable` comparison lives in a separate function
`x10_non_monotonic_measurable_bound` (`checks.py:757–838`) returning its own `_result("X-10", …)`
with its own `status`. Both read one measurement pass, `_charged_rows` (`:846–866`), so the numbers
cannot drift between them. Verified by reading the two bodies, not the docstrings: there is no
second `_cap_verdict` call in `x08` and no `acquisition` verdict in `x10`.

### 39.2 Is `X-08` genuinely deliverable-invariant? Measured, both states

The pass-6 counter-example rebuilt on `wt1`. `tests/test_stage6_crash_trials.py` is `T-005`'s own
deliverable and the only thing that put `T-005` into the old check:

| `wt1` state | `X-08` verdict and rows | `X-10` verdict and rows |
|---|---|---|
| `T-005`'s deliverable **absent** | **FAIL**, 6 rows: `T-002`×2, `T-003`, `T-004`×2, `T-006` | **FAIL**, 6 rows — no `T-005` |
| `T-005`'s deliverable **present** | **FAIL**, **the same 6 rows, string-identical** | **FAIL**, 8 rows — `T-005` TF1 7161 and TF2 9763 added |

**`X-08`'s row set is invariant under creation of the deliverable. `X-10`'s is not, and its name
says so.** The defect is not merely printed elsewhere; it is out of the gate's verdict.

I checked the general case and not only `T-005`. `charged_context` deduplicates by `(path, anchor)`
with acquisition units appended before deliverables, so a path that is *both* an acquisition unit
and a deliverable would be charged into `acquisition` and would move the gate. Enumerated live for
all six tasks: **the acquisition/deliverable overlap is empty for every task**, so the invariance
holds live and is not an accident of `T-005`.

**It is not, however, guaranteed by anything, and I built the counter-example.** A task declaring
`out/shared.md` as both `optional` read and `deliverable` — a lawful and natural declaration for
any task that revises an artifact it must first read — charges that path into `acquisition`, never
into `revision`, and `X-08` moves **FAIL → PASS** the moment the task creates it (`acquisition`
251 → 855 at a cap of 100 000; 249 → 853, **+243 %**, at a cap of 400). The gate's headline
property survives on this tree only because no live task happens to make that declaration. See
`FIND-Q9-49` in §44, which I rate **MAJOR** on that evidence.

### 39.3 Can they fail independently? One direction yes, the other is impossible

Constructed on `wt1` by raising only the declared caps — no code touched — so that every
`acquisition` figure lands under its cap:

```
caps raised: T-002 13000/17000, T-003 8500/10500, T-004 30000/35000, T-006 13000/15500
X-08  PASS   0 details
X-10  FAIL   4 details   T-004 TF1 67418 > 30000, TF2 83323 > 35000
                         T-005 TF1  7161 >  1500, TF2  9763 >  2000
```

**`X-10` fails while `X-08` passes.** That is the direction the finding was about, and it now works.

The converse cannot occur. `total_measurable = acquisition + revision`, `revision ≥ 0`
componentwise, both checks compare against the same `context_budget` entry and both use the same
`gated` flag from `_charged_rows`. Therefore `acquisition > cap ⟹ total_measurable > cap`, so
**`X-08` FAIL implies `X-10` FAIL, always.** The two booleans are not independent; they are
ordered. `X-08` is a pure function of `acquisition` — which is the property the gate needed — but
`X-10` is not a pure function of `revision`, and it never reports PASS while the gate is red.

Two docstrings state this more strongly than it is true: `checks.py:644` — *"Both can fail
independently, and `row["id"]` tells a machine which did"* — and `checks.py:782` — *"Both may fail,
independently"*. Recorded as `FIND-Q9-50`, MINOR, in §44. It does not damage the gate.

**Disposition: `FIND-Q9-45` CLOSED AT ROOT.** The gate's verdict no longer depends on a quantity
the dispatch moves, and I demonstrated the invariance by measurement in both tree states rather
than by reading the claim.

---

## 40 · `FIND-Q9-43` — the attack, re-run, and three further disarming inputs

### 40.1 The vector it was raised on is closed

`x06_result_currency` now reads the predecessor's half of the link (`checks.py:474–522`). The
pass-6 attack, re-run verbatim on `wt1` — `supersedes: R-012` and the three-line `supersedes_seal`
block deleted from `R-013`:

```
X-06  FAIL   details 1
  FAIL R-012: declares superseded_by R-013, but R-013 declares supersedes nothing and carries
       no supersedes_seal over R-012. The two records contradict each other about whether this
       supersession happened ...
```

Pass 6 obtained `X-06 PASS`, one notice, from the same edit. **The raised vector is CLOSED AT
ROOT.** Baseline for comparison: `X-06 PASS`, 0 details, 4 notices.

### 40.2 `FIND-Q9-51`, MAJOR — one line, one file, and the seal is off. Undisclosed

The repair introduced `_corroborates` (`checks.py:333–355`), which accepts **either** a
`supersedes:` declaration **or** a `supersedes_seal.path` whose basename is the predecessor's
record file. `graph.successor_of` (`graph.py:65–72`) recognises a successor by `supersedes` **only**.
The two halves of the mechanism therefore disagree about what constitutes a link, and the gap
between them is an attack:

**Delete one line — `supersedes:  R-012` — from `R-013`. Leave the `supersedes_seal` block, with
its correct digest of `R-012`, exactly where it is.** Executed on `wt1`:

```
X-06  PASS   details 0, notices 5
  note R-012: unsealed - no record declares that it supersedes this one, so a rewrite after
       supersession cannot be detected here
--- then: append "TAMPERED: this paragraph was appended after supersession." to R-012 ---
X-06  PASS   details 0, notices 5      (identical; no REWRITTEN alarm, no new detail)
full check: 7 of 10 PASS — byte-identical to baseline
```

* `_corroborates(R-013, "R-012")` returns `True` on the surviving seal path, so the new
  FIND-Q9-43 cross-check is satisfied and emits nothing.
* `successor_of(results, "R-012")` returns `""`, so `supersession_seal` returns no digest and
  `result_currency` (`graph.py:237–251`) takes the *unsealed* branch.
* The epoch rule at `checks.py:454` is guarded by `if result.supersedes …` and is skipped.

**The digest that would convict the tamperer is sitting in the repository, in
`R-013.supersedes_seal.digest`, and no code path compares it** — because the field that proves the
link is not the field that establishes it. This is `FIND-Q9-43`'s own class, reproduced inside the
repair for it, and it is **cheaper than the attack it replaces**: one deleted line in one file,
against pass 6's two lines.

`checks.py:422–432` discloses a residual and states *"The cost of the attack is now three edits
across two files rather than two edits in one."* **That statement is false as written** — the cost
is one edit in one file. Recorded as part of this finding.

### 40.3 `FIND-Q9-52`, MAJOR — the same trick on an interior link is invisible to everything

`FIND-Q9-51` leaves one live test red (`test_the_live_dependency_state_is_derived_end_to_end`
asserts the CURRENT record's `supersedes` is non-empty), so a reviewer running the suite would see
something. On an **interior** link nothing sees anything.

Delete `supersedes:  R-011` from `R-012`, recompute `R-013`'s seal over the edited `R-012` (which a
tamperer editing the chain must do anyway and which is one string substitution), then append
`TAMPERED D4b.` to `R-011`:

```
X-06                          PASS    0 details
full check                    7 of 10 PASS   — identical to baseline
pytest tests/test_exec_*.py   275 passed     — identical to baseline
```

**Two edits across two files, a rewritten superseded record, and not one signal anywhere in the
architecture.** The unsealed-notice for `R-011` is indistinguishable from the two legitimate
pre-epoch notices the run always prints.

Without the reseal the attack is caught, but only incidentally — `R-013`'s seal over `R-012` breaks
because `R-012` itself was edited. The control catches the tamperer's *bookkeeping*, not the tamper.

### 40.4 The two disclosed residuals — confirmed, and one disclosure is inaccurate

| Residual | Where disclosed | Re-run on `wt1` | Verdict |
|---|---|---|---|
| Backdate the successor's session, strip the seal, keep `supersedes` | `graph.py:162–165`, residual 2 | `X-06 PASS`, 0 details; `R-012` then freely rewritten with no alarm | **Confirmed live, accurately disclosed.** Cost: 4 line-edits in 1 file |
| Strip `superseded_by` from the predecessor *and* `supersedes` + seal from the successor | `checks.py:422–432` | `X-06 PASS`, 0 details | **Attack confirmed. Disclosure of its *cost* is wrong** — see §40.2 |

The `X-06` docstring's residual paragraph remains the only place either is stated, and
`graph.seal_epoch`'s residual 2 is still not repeated in the check a reviewer reads — the pass-6
qualification stands unchanged.

### 40.5 Disposition

**`FIND-Q9-43` — CLOSED AT SYMPTOM.** The specific two-line edit is now caught. The property the
finding was raised about — *a tamper control whose evidence base is inside the set of files the
tampering party is already editing* — is not closed, and the repair widened the attack surface
rather than narrowing it: it added a second corroborating field that the seal machinery does not
honour, producing a **cheaper** disarm than the one it fixed. Four working disarms are now on
record across passes 6 and 7, two of them undisclosed.

The structural cause is stable across all four and worth stating once: **`successor_of` is the
single point of truth for "is there a successor", it is derived from one editable field, and every
seal comparison hangs off it.** Nothing derives the link from the seal itself.

---

## 41 · `FIND-Q9-44`, `46`, `47`, `48` — re-tested individually

### 41.1 `FIND-Q9-44` — MU14 dies. **CLOSED AT ROOT**

The two declarations are now one. `ACQUISITION_EMITTERS` (`scope.py:543–548`) is a component-name →
emitter-function table; `ACQUISITION_COMPONENTS` is `tuple(ACQUISITION_EMITTERS)` (`:553`); and
`acquisition_units` iterates the constant and looks the emitter up, raising `ScopeError` if one is
missing (`:610–625`).

I re-ran pass 6's MU14 and a harder variant. Kill counts are **net of the re-measured floor of 3**
(§43.1):

| Mutant | Total failures | Net of floor | Verdict |
|---|---|---|---|
| **MU14** — `ACQUISITION_COMPONENTS = (*tuple(ACQUISITION_EMITTERS), "telemetry")`, i.e. pass 6's exact mutation | 75, plus 10 collection errors | 73 | **KILLED** — `ScopeError` at the first measurement; the layer refuses to run |
| **MU14b** — `telemetry` added to `ACQUISITION_EMITTERS` *with a real emitter returning `[]`*, so the guard cannot fire | 6 | **3** | **KILLED** by `TestAcquisitionSurfaceIsOneDeclaration::{test_every_declared_component_is_actually_emitted, test_a_component_added_to_the_set_alone_cannot_go_uncharged, test_the_charge_accounts_for_every_declared_component}` |

MU14b is the important one: it is MU14 with the loud failure mode removed, and it still dies to
three tests written for exactly this. **The drift vector is closed structurally and covered by
tests, not merely made noisy.**

### 41.2 `FIND-Q9-46` — the notice is now true. **CLOSED AT ROOT**

`checks.py:736–747` now emits `total_measurable {n} is compared against this same cap by X-10,
whose verdict is separate from this one (FIND-Q9-45)`. Checked against the live tree for the three
tasks the notice was false about:

* `T-002`, `T-003` and `T-006` all carry the sentence, and `X-10`'s detail list **does** contain a
  `total_measurable` row for each of them (`T-002` TF1+TF2, `T-003` TF1, `T-006` TF1). What the
  sentence now asserts — that `X-10` compares this quantity against this cap — is true for every
  task in every state, including the under-cap case, because it asserts a comparison and not a
  verdict.
* The word `failed` no longer appears in the clause. `MU31`, which reinstates the old sentence
  verbatim, is **KILLED** (net 1) by `test_the_split_notice_asserts_no_verdict_it_did_not_emit`,
  whose fixture is a task that breaches nothing — the exact case the old sentence lied about in
  the other direction.

### 41.3 `FIND-Q9-48` — citation corrected. **CLOSED AT ROOT**

`.ai/project/EXECUTION_ARCHITECTURE.md:248` is `### 6.2 · The seal epoch — S-2026-08-09-06,
declared`; `:229` is `### 6.1 · Immutability without new machinery`. Both citations now read §6.2
(`graph.py:143`, `checks.py:441–442`). Reverting either is **KILLED** (net 1 each) by
`TestArchitectureCitations::{test_the_epoch_is_recorded_in_the_section_the_code_cites,
test_the_x06_notice_cites_the_same_section}` — the citation is asserted against the heading text in
the file, so it cannot silently rot again.

### 41.4 `FIND-Q9-47` — one limb closed by disclosure, the other **widened**

**Limb A, the mutation floor: CLOSED AT ROOT, and better than closed.**
`EXECUTION_ARCHITECTURE.md §14.1` now names the floor, names the three tests, explains why pinning
the layer is the design rather than a defect, states in terms that *"a mutant reported as '3
failures, KILLED' has in fact survived"*, and gives the recomputation procedure. `§14` limit 13
points to it. That is the correct disposition of a fact that must not be repaired.

**Limb B, the concurrent session's untracked file: NOT CLOSED, and it now costs one test more.**
`test_the_live_t005_shape_reproduces_the_incident` (`tests/test_exec_scope.py:474–485`) still
asserts `cc.non_monotonic == ["tests/test_stage6_crash_trials.py"]`, and that file is still
untracked. The correction pass then added a **second** test with the same dependency:
`test_the_gate_and_the_bound_decide_their_own_booleans` (`tests/test_exec_checks.py:388–404`)
asserts `"T-005" in bound_tasks` and `gate_tasks < bound_tasks`, both of which hold only because
another session's in-flight deliverable is on disk. Measured on `wt1` with that file removed:

```
FAILED tests/test_exec_checks.py::TestLiveRepositoryOpenFailures::test_the_gate_and_the_bound_decide_their_own_booleans
FAILED tests/test_exec_scope.py::TestBudgetSplit::test_the_live_t005_shape_reproduces_the_incident
2 failed, 273 passed          (pass 6 measured 1 failed, 256 passed)
```

Recorded as `FIND-Q9-53`, MINOR, in §44. The pass is plainly aware of the pattern — a *third* test,
`test_a_prospective_deliverable_costs_nothing_and_is_declared` (`test_exec_scope.py:296–320`), was
deliberately made hermetic with a comment naming this exact incident — which makes leaving the
other two on the live tree a choice rather than an oversight, and an undisclosed one.

---

## 42 · The four newly surfaced bound breaches — real, and redundant

The `revision == 0` suppression is gone; the equality is stated in the row instead
(`checks.py:810–812`). Four rows pass 6 could not see are now emitted. Arithmetic checked by hand
against the caps in the task records:

| Row | `total_measurable` | `acquisition` | Declared cap | Real breach? |
|---|---|---|---|---|
| `T-002` TF1 | 12 880 | 12 880 | 12 000 (`T-002.md:80`) | **yes** |
| `T-002` TF2 | 16 680 | 16 680 | 16 000 (`T-002.md:81`) | **yes** |
| `T-003` TF1 | 8 193 | 8 193 | 8 000 (`T-003.md:71`) | **yes** |
| `T-006` TF1 | 12 154 | 12 154 | 12 000 (`T-006.md:79`) | **yes** |

**Not artifacts.** Each is a genuine overrun of a declared cap by the quantity the check names, and
the families that are *under* cap correctly emit nothing (`T-003` TF2 9 939 ≤ 10 000; `T-006` TF2
14 641 ≤ 15 000) — so removing the suppression did not turn into a blanket.

They are, however, **exact echoes of `X-08`'s rows**: `revision` is zero for all three tasks, so
`total_measurable == acquisition` and the same overrun is reported once under `X-08` and once under
`X-10`. Four of `X-10`'s eight failures carry no information `X-08` does not already carry. That is
the price of making `X-10`'s boolean a pure function of its own quantity; it is disclosed in terms
at `checks.py:791–799`, each row says *"equal to the acquisition gate, because revision is zero"*,
and `MU26` — which restores the suppression — is **KILLED** (net 3). **Honest findings about the
repository, correctly handled.**

---

## 43 · Test integrity

### 43.1 The pin floor, re-measured under `R-013`

`R-013` pins all six `src/aief_exec/*.py` files and all four `tests/test_exec_*.py` files as
deliverables. Appending `# semantically inert comment added by the auditor` to `scope.py`:

```
3 failed, 272 passed
  test_exec_checks.py::TestLiveRepositoryOpenFailures::test_x02_open_on_the_consumer_of_a_staled_result
  test_exec_checks.py::TestLiveRepositoryOpenFailures::test_x06_open_on_the_result_that_pins_the_layer_it_describes
  test_exec_graph.py::TestLivePlan::test_the_live_dependency_state_is_derived_end_to_end
```

**Floor = 3, unchanged, same three tests.** Every net score below subtracts it, and I scored
against failing test *names* wherever a mutant landed near it.

### 43.2 The campaign — eighteen semantic mutants on the repaired mechanisms

Each applied and reverted in isolation on `wt1`; all four `test_exec_*.py` files run each time.

| # | Mutant | Failures | Net | Verdict |
|---|---|---|---|---|
| MU14 | `telemetry` in the component set alone — **pass 6's survivor** | 75 (+10 errors) | 73 | **KILLED** |
| MU14b | `telemetry` with an emitter that emits nothing | 6 | 3 | **KILLED** |
| MU22 | `X-10` removed from the check set | 6 | 3 | KILLED |
| MU23 | `X-10` never fails — breaches routed to notices | 9 | 6 | KILLED |
| MU24 | `X-08` gates `total_measurable` again — **the FIND-Q9-45 defect** | 9 | 6 | KILLED |
| MU25 | `X-08` gates the sum under the `acquisition` label | 7 | 4 | KILLED |
| MU26 | the `revision == 0` suppression restored in `X-10` | 6 | 3 | KILLED |
| MU27 | `_corroborates` always `True` | 4 | 1 | KILLED — `test_deleting_the_successors_supersedes_does_not_disarm_the_seal` |
| MU28 | the `superseded_by` cross-check loop deleted — **the FIND-Q9-43 repair** | 7 | 4 | KILLED |
| MU29 | `records.superseded_by` always empty | 7 | 4 | KILLED |
| MU31 | the FIND-Q9-46 false sentence reinstated | 4 | 1 | KILLED |
| MU32 | `X-06` notice cites §6.1 again | 4 | 1 | KILLED |
| MU33 | `graph.seal_epoch` cites §6.1 again | 4 | 1 | KILLED |
| MU35 | `acquisition` stops splitting stable / self-referential | 6 | 3 | KILLED |
| MU36 | `seal_epoch` reverts to the `min()` derivation — the FIND-Q9-39 defect | 7 | 4 | KILLED |
| MU37 | `COMPLETE` tasks gated by `X-10` | 5 | 2 | KILLED |
| **MU30** | **`_corroborates`' seal-path limb deleted** | 3 | **0** | **SURVIVED** |
| **MU34** | **`X-10`'s `_measurable` blinding routed to a throwaway list** | 3 | **0** | **SURVIVED** |

(`MU38`, reordering `_charged_rows`, changes only detail order and is not scored. `MU14c`, which
neutered the `ScopeError` guard, produced an import error and is not scored either.)

**16 killed, 2 survived of 18.** Both survivors matter, and neither is a mere coverage gap:

* **MU30 is the smoking gun for `FIND-Q9-51`.** Deleting the `supersedes_seal.path` limb of
  `_corroborates` — the limb that makes the one-line disarm of §40.2 possible — **breaks no test at
  all.** Nothing in the suite exercises seal-path corroboration and nothing depends on it. Its only
  demonstrated effect is to satisfy the FIND-Q9-43 cross-check for a successor that has deleted its
  `supersedes`. The docstring justifies it by `R-001`/`R-007`, but both of those successors *do*
  declare `supersedes`, so the first limb already covers them. Untested, unnecessary, and
  load-bearing for the attack.
* **MU34** shows `_measurable`'s claim at `checks.py:869–876` — *"two checks blinded by one record
  defect is two facts, not one repeated"* — is asserted for `X-08` and not for `X-10`. No live task
  has a measurement error, so nothing exercises it. `FIND-Q9-54`, MINOR.

### 43.3 Fixture avoidance — hunted again

The pass-5 pattern (`TestBudgetSplit._task` placing the record outside `write_scope`, the one
configuration in which the property under test cannot fail) does not recur in the new work:

* `test_the_gate_verdict_does_not_move_when_the_task_writes_its_own_work`
  (`test_exec_checks.py:1047–1085`) rewrites the fixture's `deliverable` to a path it then
  *creates*, asserts `before["details"] == after["details"]`, and separately asserts
  `x10(...)["status"] == "FAIL"` — so it cannot be satisfied by a check that simply never measures
  the deliverable. MU24 and MU25 both kill it.
* `test_the_split_notice_asserts_no_verdict_it_did_not_emit` uses caps of 90 000 so that **nothing**
  breaches — the state in which the old sentence was false in the other direction. The fixture is
  chosen to expose the defect, not to avoid it.
* `test_the_bound_is_not_suppressed_when_revision_is_zero` is the **deliberately inverted
  assertion**. It was `test_x08_does_not_double_report_when_revision_is_zero`, asserting the
  suppression; it now asserts its absence. **The inversion is correct**: the suppression's stated
  justification — one overrun printed twice in one details list — died with the split into two
  lists, and keeping it would have made `X-10`'s boolean a function of the non-monotonic quantity.
  The test is strengthened rather than weakened; it additionally asserts `X-08` carries no
  `total_measurable` row and that `X-10`'s rows explain the equality. MU26 kills it.
* `TestX06SealEpoch::test_deleting_the_successors_supersedes_does_not_disarm_the_seal` reproduces
  the pass-6 attack as its fixture and asserts the FAIL; it cannot pass unless the tamper lands.

**What I found instead is the mirror image**: two live-tree tests whose green state depends on
another session's untracked file (§41.4, `FIND-Q9-53`), and one untested code path that exists only
to weaken a control (MU30, `FIND-Q9-51`).

---

## 44 · New defects introduced or left by the correction pass

| ID | Severity | Finding | Exact site |
|---|---|---|---|
| **FIND-Q9-51** | **MAJOR** | **The supersession seal is disarmed by deleting one line from one file, and the vector is undisclosed.** `_corroborates` accepts `supersedes_seal.path` as corroboration of a link, while `graph.successor_of` recognises a link only through `supersedes`. Deleting `supersedes:  R-012` from `R-013` — leaving the seal block and its correct digest in place — returns `X-06` to **PASS** with no detail; appending `TAMPERED: …` to `R-012` then raises nothing, and the full check is byte-identical to baseline at 7 of 10. Verified end to end on `wt1`. The digest that would convict the tamperer is in the repository and no code path compares it. The attack is **cheaper** than the pass-6 one it replaces (one line vs two), and mutant MU30 shows the enabling limb is exercised by no test | `src/aief_exec/checks.py:333–355` (`_corroborates`), `:489`; `src/aief_exec/graph.py:65–72` (`successor_of`), `:182–185`, `:237–251` |
| **FIND-Q9-52** | **MAJOR** | **The same deletion on an interior link is invisible to every control in the architecture.** Delete `supersedes:  R-011` from `R-012`, recompute `R-013`'s seal over the edited `R-012` (one string substitution the tamperer must make anyway), then rewrite `R-011`. Result: `X-06` **PASS**, full check **7 of 10 PASS**, `pytest tests/test_exec_*.py` **275 passed** — all three identical to baseline. Two edits across two files, a superseded record rewritten, and no signal anywhere. Without the reseal the tamper is caught only incidentally, because `R-012` itself was edited — the control catches the tamperer's bookkeeping, not the tamper | `src/aief_exec/graph.py:65–72`, `:182–185`; `src/aief_exec/checks.py:474–522` |
| **FIND-Q9-49** | **MAJOR** | **`X-08`'s deliverable-invariance is live-true but not structural, and the counter-example is lawful and demonstrated.** `charged_context` builds `units` as acquisition units *then* deliverables and deduplicates by `(path, anchor)` keeping the first (`scope.py:929–954`), so a path that is both a declared read entry and a declared deliverable is charged into **`acquisition`** and never reaches `revision`. The gate then moves when the task writes its own deliverable — exactly what the split exists to prevent. Built and measured: a task declaring `deliverable: [out/shared.md]` and `optional: [out/shared.md]`, cap 100 000, goes **`X-08` FAIL → PASS** on creating that file (`acquisition` 251 → 855, `revision` 0 throughout); at cap 400 it goes FAIL → FAIL with `acquisition` 249 → 853, **+243 %**. The overlap is empty for all six live tasks — verified by direct enumeration, which is the only reason §39.2's invariance measurement held — but nothing asserts the overlap is empty, no check reports one, and the split notice would report `revision 0 (nothing charged)` for a task whose deliverable is fully charged | `src/aief_exec/scope.py:929–954`; `src/aief_exec/checks.py:606–754`, `:639–640` |
| **FIND-Q9-50** | MINOR | **Two docstrings claim an independence the checks do not have.** `checks.py:644` — *"Both can fail independently"* — and `:782` — *"Both may fail, independently"*. Since `total_measurable = acquisition + revision`, `revision ≥ 0`, and both checks use the same cap and the same `gated` flag, `X-08` FAIL **implies** `X-10` FAIL. The independence is one-directional: `X-10` can fail alone (demonstrated), `X-08` cannot. The gate is sound; the claim about the pair is overstated, and overstated claims in this exact place are what `FIND-Q9-36`, `36b` and `46` were | `src/aief_exec/checks.py:644`, `:782`; `.ai/project/EXECUTION_ARCHITECTURE.md:487` |
| **FIND-Q9-53** | MINOR | **The suite's green state still depends on a concurrent session's untracked file, and one more test now does.** `test_the_live_t005_shape_reproduces_the_incident` (`test_exec_scope.py:474–485`) and the newly added `test_the_gate_and_the_bound_decide_their_own_booleans` (`test_exec_checks.py:388–404`) both require `tests/test_stage6_crash_trials.py`, which is untracked and owned by another task. Removing it: **2 failed, 273 passed** (pass 6 measured 1 failed). `FIND-Q9-47`'s pin-floor limb was disclosed and disposed correctly at `EXECUTION_ARCHITECTURE.md §14.1`; this limb was neither disclosed nor narrowed, and the pass demonstrably knows the pattern — it hermetically rewrote a third test for this exact reason (`test_exec_scope.py:296–300`) | `tests/test_exec_scope.py:474–485`; `tests/test_exec_checks.py:388–404` |
| **FIND-Q9-54** | MINOR | **`X-10`'s blinding path is unreachable in tests and unasserted.** `_measurable` states that an unmeasurable row must fail *both* budget checks — *"two checks blinded by one record defect is two facts, not one repeated"* — but mutant MU34, which routes `X-10`'s blinding details into a throwaway list so that an unmeasurable task is silently skipped, survives the entire suite net of floor. `X-08`'s side of the same claim is covered | `src/aief_exec/checks.py:808–809`, `:869–897` |
| **FIND-Q9-43-D** | MINOR | **A disclosed residual misstates the attack's cost.** `checks.py:429–431` states *"The cost of the attack is now three edits across two files rather than two edits in one."* `FIND-Q9-51` performs it in **one edit in one file**. The residual paragraph is otherwise accurate — I reproduced the three-edit variant and it does return `X-06` to PASS. Related: `EXECUTION_ARCHITECTURE.md §6.3` tabulates *"`B` declares `supersedes: A` **or** seals `A`"* as the *agreed* case, so the hole `FIND-Q9-51` exploits is written down as intended behaviour without being recognised as a hole | `src/aief_exec/checks.py:422–432`; `.ai/project/EXECUTION_ARCHITECTURE.md:293`, `:309` |

**Ambiguities recorded, not resolved — LAW-12.**

1. **Whether a second cap should bound `total_measurable`.** `X-10` compares against `X-08`'s cap
   and says why (`checks.py:785–789`, `EXECUTION_ARCHITECTURE.md §11.1`). That is the right refusal
   and it is the direct cause of the four echo rows in §42 and of the one-directional dependence in
   `FIND-Q9-50`. A `project-manager` decision.
2. **Pass 5's LAW-12 item 2 remains open**: the repository still does not choose between excluding
   self-written paths from `acquisition` and forbidding a task's record from lying inside its own
   write scope. The disclosure is now correct and quantified; the question is not answered. A
   `chief-systems-engineer` question.
3. **Whether `superseded_by` should be a required field.** `checks.py:406–410` declines to require
   it, citing LAW-12, and reports the missing back-link as a blind spot. Correct as far as it goes,
   but `FIND-Q9-51` and `FIND-Q9-52` show the back-link is not the weak point — the *definition of a
   link* is. Whether `successor_of` should recognise a seal-path link is a design question this
   audit does not decide.
4. **Pass 5's LAW-12 item 3 stands unchanged.** `T-004` still cannot lawfully update its own
   checkpoint: `write_scope` is `.ai/project/verification/VER-009_*.md` alone while
   `.ai/project/tasks/T-004.md` carries a `checkpoint` block with `pending` items. I did not edit it.
5. **`R-013` records that tests were added and restated.** The files are untracked, so there is no
   committed predecessor to diff and I cannot verify a restatement from the repository. I verified
   the current 275 by mutation instead and record the count claim as unreachable.

---

## 45 · Result chain `R-010` → `R-011` → `R-012` → `R-013`, by recomputation

Every seal recomputed twice: once through `records.file_dc1`, and once through a DC-1
implementation written in this session from the stated rule, sharing no code with the package.

| Link | Pinned by the successor | `records.file_dc1` | Independent | Verdict |
|---|---|---|---|---|
| `R-001` → `R-007` | *none* | `61752b84764cf689…` | identical | **UNSEALED** — pre-epoch, correctly a notice |
| `R-007` → `R-008` | *none* | `30e975012de30147…` | identical | **UNSEALED** — pre-epoch, correctly a notice |
| `R-008` → `R-009` | `e081eb7b9370afe9…` | identical | identical | **MATCH** |
| `R-009` → `R-010` | `6cc1c3efcd0d14e0…` | identical | identical | **MATCH** |
| `R-010` → `R-011` | `45516365790fd220…` | identical | identical | **MATCH** |
| `R-011` → `R-012` | `a74a507e1daca9d7…` | identical | identical | **MATCH** |
| `R-012` → `R-013` | `be67c646ca12cad5…` | identical | identical | **MATCH** |

`R-013`'s own currency, recomputed rather than read: **7 pinned inputs and 11 pinned deliverables,
zero mismatches.** `derived_status(R-013) = CURRENT`; every other record both declares and derives
`SUPERSEDED`, and all seven links are declared from **both** sides — `superseded_by` on the
predecessor and `supersedes` on the successor agree throughout, so the new cross-check has no live
disagreement to report. `seal_epoch` declared `S-2026-08-09-06`, `derived_seal_epoch`
`S-2026-08-09-06` — they agree, so the disagreement notice correctly stays silent. **`R-013` is
CURRENT.**

`VER-009` is **not** among `R-013`'s eleven pinned deliverables, so writing this file does not move
`R-013`'s currency; I re-confirmed all eighteen pins after writing §§38–44.

The pass-6 caution holds and I hit it: raw `hashlib.sha256` over file bytes disagrees with DC-1 on
`.ai/project/results/R-012.md`. Only the normalised digest is the seal.

---

## 46 · Disposition — pass 7

> ### VERIFIED WITH FINDINGS
>
> **Five of the six pass-6 findings are closed at the root; one is closed at the symptom and
> its class is now on its third field.** The budget work is the strongest in this audit's
> history: `FIND-Q9-45` is closed structurally, `FIND-Q9-44`'s survivor mutant now dies to
> tests written for it, `FIND-Q9-46`'s sentence is true, `FIND-Q9-48`'s citation is asserted
> against the heading it cites, and the mutation floor that invalidated two earlier campaigns
> is documented in the architecture with the instruction to subtract it. The supersession-seal
> work is not sound. The repair for `FIND-Q9-43` introduced a **cheaper** disarm than the one
> it closed — one line, one file — and an interior-link variant that is invisible to the
> check, to the full campaign and to all 275 tests.

| Pass-6 finding | Disposition | Evidence I generated |
|---|---|---|
| `FIND-Q9-43` | **CLOSED AT SYMPTOM** | The raised two-line edit now yields `X-06 FAIL` with a named contradiction, against pass 6's PASS. But `FIND-Q9-51`: deleting the successor's `supersedes` line **alone** returns `X-06` to PASS and lets the predecessor be rewritten silently; `FIND-Q9-52`: the same on an interior link is invisible to check, campaign and suite. MU27/28/29 kill the new cross-check; MU30 shows the limb that enables the bypass is exercised by nothing |
| `FIND-Q9-44` | **CLOSED AT ROOT** | One declaration (`ACQUISITION_EMITTERS`), the constant derived from it, and a `ScopeError` for a component with no emitter. MU14 — pass 6's survivor — dies with 73 net failures; MU14b, the same mutation with the loud path removed, dies to three purpose-written tests |
| `FIND-Q9-45` | **CLOSED AT ROOT** | `X-10` is a separate check with its own `_result`. `X-08`'s detail set is **string-identical** with `T-005`'s deliverable absent and present. Caps raised so every gate figure is under cap: `X-08 PASS` while `X-10 FAIL` on four rows. MU24, MU25, MU23, MU22, MU26 all die. Residual `FIND-Q9-50`: the converse is impossible, so "independently" is one-directional |
| `FIND-Q9-46` | **CLOSED AT ROOT** | The clause no longer contains the word `failed`; it asserts a comparison `X-10` demonstrably performs, verified live for `T-002`, `T-003` and `T-006`, the three tasks it lied about. MU31 reinstates the old sentence and dies to a fixture that breaches nothing |
| `FIND-Q9-47` | **CLOSED AT ROOT (limb A) / NOT CLOSED and widened (limb B)** | `§14.1` documents the floor, names the three tests, refuses to "fix" the pins and gives the recomputation procedure — I recomputed and got 3, unchanged. But the untracked-file dependency now costs **2** failing tests, not 1: the pass added `test_the_gate_and_the_bound_decide_their_own_booleans` with the same dependency (`FIND-Q9-53`) |
| `FIND-Q9-48` | **CLOSED AT ROOT** | `§6.2` is *The seal epoch*; both citations read §6.2; `TestArchitectureCitations` asserts the code's citation against the heading text, so MU32 and MU33 both die |

**The three failing checks, judged.**

* **`X-08` — honest.** Six rows, all real overruns of real caps by a quantity that does not move
  when the task does its work. Verified invariant by measurement in both tree states.
* **`X-10` — honest.** Eight rows, all arithmetically confirmed against the caps in the task
  records. Four are echoes of `X-08` (§42) and each says so in its own text. Naming the check for
  the property that makes it unfit to be a gate is the right call.
* **`X-09` — honest, unchanged from pass 6.** Five producer-cannot-publish failures and five
  undeclared-reach failures; I re-confirmed `T-001.write_scope` genuinely contains
  `.ai/project/results/**` and that no pattern in the five records matches the record each is
  contracted to publish. Not re-litigated further.

**What holds, verified by evidence I generated.** The result chain is intact: five sealed links
recomputed two ways and matching, two pre-epoch links correctly reported rather than accused, all
eighteen of `R-013`'s pins matching, `R-013` `CURRENT`, and every link declared from both sides.
The acquisition surface has one declaration and one enumeration, and both the cost model and the
hazard model read it. The gate is monotone with respect to deliverable creation on this tree. The
mutation floor is documented and correct. Sixteen of eighteen semantic mutants die, and both
survivors are findings rather than gaps I merely noted.

**What does not hold.** The supersession seal. Four working disarms are now on record across two
passes; two of them are undisclosed; the cheapest is a single deleted line; and one of them leaves
no trace in any control the repository has. The cause has been stable across all four:
`graph.successor_of` is the single point of truth for whether a link exists, it reads one editable
field, and every seal comparison hangs off it. Each pass has hardened a different accessory —
first the epoch, now the back-link — without changing that. `FIND-Q9-51` is the first time the
repair itself supplied the new bypass, by teaching the *cross-check* a second definition of a link
that the *seal machinery* does not share.

**Escalations.** `FIND-Q9-51` and `FIND-Q9-52` to `software.software-engineer` and
`chief-systems-engineer` — a control disarmable by the party it polices, now on its third field, is
a framework question and not a coding one; MU30 indicates the immediate mitigation is a deletion,
not an addition. `FIND-Q9-49` to `software.software-engineer` — the gate's headline property needs
an invariant, not a coincidence. `FIND-Q9-50`, `53`, `54`, `43-D` to
`software.software-engineer`. LAW-12 items 1–3 to `chief-systems-engineer` and `project-manager`;
item 4 to `project-manager`.

**What I could not reach.** Stated so no reader mistakes silence for coverage.

1. `R-013`'s prose conclusion was deliberately not read before the findings above were formed, and
   its account of the repair is not disposed here.
2. §§1–29 of this file were not read, by contract.
3. `src/aief_exec/__main__.py` was exercised on `check`, `status`, `scope`, `classify` and
   `measure`. `brief` was not exercised.
4. `EXECUTION_ARCHITECTURE.md` was checked for agreement with the code at §6.2, §6.3, §11.1, §12
   and §14/§14.1. §5, §5.3, §7 and §13 were not line-audited.
5. `FIND-Q9-38` E4 (`T-002 x T-004` still PARALLEL, the runtime-import hazard) was not re-examined;
   it was disclosed open in pass 6 and nothing in this pass's subject list touches it.
6. `X-04`, `X-07` and the A4 boundary were not re-litigated.
7. The Stage 6 tests are excluded by contract. `pytest tests/test_exec_*.py` is the whole suite I
   ran; I did not run `tests/test_stage6_*.py`.
8. `FIND-Q9-51` and `FIND-Q9-52` were demonstrated on the `R-011`/`R-012`/`R-013` links. I did not
   enumerate every remaining field whose deletion degrades a failure to silence; `supersedes` is
   now demonstrated in two distinct configurations, and I do not claim the enumeration is complete.
9. I did not attempt to verify the added/restated test counts — the files are untracked and there
   is no committed predecessor to diff (LAW-12 item 5).

**Footprint, confirmed after writing.** `check` → **7 of 10 PASS**, `X-08`, `X-09` and `X-10`
failing exactly as at baseline. `pytest tests/test_exec_*.py` → **275 passed**. `R-013` → still
**CURRENT**, all eighteen pins recomputed and matching after this file was written.
`git status --porcelain` → exactly **7** tracked modifications, the same seven as at session start.
Nothing under audit was modified; no defect found here was repaired — **LAW-05: QA does not fix.**
The mutation copy `wt1` was discarded.

**Verifier attestation — pass 7.** Every figure in §§38–46 was produced by a command or a direct
library call executed in session `S-2026-08-09-12` against this repository or a throwaway copy of
it. No disposition rests on a claim in `R-013`, in the `T-001` or `T-004` checkpoints, or in
§§1–29 of this report. Each pass-6 defect was reproduced or re-attacked against the current code
before its closure was accepted. I verified no artefact I produced, and I modified no artefact
under audit. This report is subject to review at
`.ai/project/reviews/DR-003_VER-009_Disposition.md` by `chief-systems-engineer`.

*Filed by `qa-engineer · S-2026-08-09-12` under task `T-004`, on the enumerated `role_authority`
grant `EXEC-D-001` recorded at `.ai/project/tasks/T-001.md`. Write scope exercised: this file only.*
