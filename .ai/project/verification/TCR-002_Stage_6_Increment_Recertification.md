# TCR-002 — Test Certification: Stage 6 Increment Recertification (T-002 / OI-C-09)

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-verification-report`.
>
> **Filing note.** Produced and filed by `software.test-engineer · S-2026-08-09-TCR-002`, a cold session dispatched under `project/ROSTER.md` (rank-1 human-owner assignment, 2026-08-08) to discharge the `qa` block of `project/tasks/T-002.md`. The verifier authored none of the code under test and repaired none of it: every defect below is recorded, not fixed (LAW-05).

| | |
|---|---|
| Subject | `src/aief_stage6/budget.py` and `lock.py` as delivered by T-002, plus the `tests/test_stage6_*.py` assertions T-002 superseded |
| Task | `project/tasks/T-002.md` — objective, three acceptance criteria, `qa.report` naming this file |
| Producer of the subject | `software.software-engineer` (T-002 execution session) — a distinct (role, session) identity from the verifier, satisfying LAW-05 and the ROSTER constraint |
| Verifier | `software.test-engineer · S-2026-08-09-TCR-002` |
| Authority for what is owed | `project/OPEN_ITEMS_REGISTER.md` row **OI-C-09** |
| Normative basis | `framework/framework.manifest.json` → `metadata.reproducible` (`digest_constructions.per_artifact`, `.core_aggregate.lock_serialisation`, `.core_aggregate.lock_json_layout`, `budget_measurement_record`, `build_provenance_record`, `distributable`, `binding_pin_write`, `bounded_register_split`), `validation[V-03]`, `[V-09]`, `[V-24]`; `framework/AIEF-AMD-013` §§AMD-42…AMD-48; `framework/AIEF-AMD-014` §§AMD-49…AMD-52 |
| Repository state | branch `main`, HEAD `8546960`, unchanged throughout. No git command that mutates state was executed |
| Date | 2026-08-09 |

**Session-id note.** `ROSTER.md` line 39 requires that "each dispatch carries its own session id" but declares no allocator. The id above is self-declared at dispatch and is distinct from every id appearing in the repository. Recorded, not resolved (LAW-12).

---

## 1. Verdict

> ## CERTIFIED WITH FINDINGS

**Priority 1 is complete and passes.** All three of T-002's acceptance criteria are met, verified by evidence this session generated rather than by reading the author's claims. TCR-001 finding **F1 is CLOSED**.

**Priority 2 is not fully certifiable.** Six of the eight conformance items are CERTIFIED. Two are **NOT CERTIFIED**, and both are substantive rather than clerical:

- the AMD-49 bounded-register 1:1 mapping is **not implemented** in `check_v03` at all, although `validation[V-03]` declares it BLOCKING; and
- one of the two new `files[]` entries, `files[state-register]`, points at `project/STATE_REGISTER.md`, which **does not exist in the working tree**, and no precondition detects it.

The certification is qualified, not withheld, because neither defect lies inside the delta T-002 was asked to deliver. T-002's own scope is clean. The findings are recorded against the artifacts that own them, for disposition by `project-manager` and `chief-systems-engineer`.

**Separately: Stage 6 cannot complete a build today**, for a reason independent of T-002. The emitted lock exceeds its own `token_cap` by a factor of ~32. This is confirmed below with a measured number and is escalated as **F-3 (BLOCKING)**.

---

## 2. Method and independence

Every number in this report was computed by this session. Where the subject package was invoked, it was invoked as the *object of measurement*; where a value had to be independently reproduced, it was re-implemented from the normative text without importing `aief_stage6`.

Nothing was written except this file. Specifically: Compiler Stage 6 was **not** executed; `core/MANIFEST.lock` was **not** emitted; no archive, DC-5 sidecar, BINDING pin write or ledger entry `L-0000001` was produced. The one simulation that exercises the build driver (§6.2) ran with `build._write` replaced by a no-op recorder, so its eight would-be writes were counted and discarded. Nothing under `src/aief_exec/**`, `tests/test_exec_*.py`, `project/EXECUTION_ARCHITECTURE.md` or `project/results/**` was read or touched; a concurrent session owns those.

Baseline suite, unmodified tree:

```
$ PYTHONPATH=src python -m pytest tests/test_stage6_*.py -q
2 failed, 123 passed in 1.26s
```

---

## 3. Priority 1 — T-002 acceptance criteria

### 3.1 AC-1 — the deferral is keyed on the path, never on absence — **PASS**

> *Criterion:* the budget deferral is keyed on the path, never on absence from the tree.
> *Test:* a measured file absent from the tree other than `core/MANIFEST.lock` halts.

`budget.measure` (`src/aief_stage6/budget.py:117-134`) branches on `path == LOCK_PATH` **before** it touches the filesystem, and the filesystem branch raises `BudgetSourceMissing` unconditionally on `not fs_path.is_file()`. There is no path from an absent non-lock file to a deferral.

Verified by construction rather than by reading. Synthetic manifests were built against a temporary tree and driven through `budget.measure` with a deterministic stub family (1 token per whitespace-delimited word for TF-1, 2 for TF-2), so every count is hand-checkable:

| # | Construction | Expected | Observed | |
|---|---|---|---|---|
| 1 | capped **T1** entry `p/absent.md`, not on tree | halt | `BudgetSourceMissing: p/absent.md: measured file absent from the tree - build halts (AMD-45: only core/MANIFEST.lock defers, and it defers on its path)` | PASS |
| 2 | capped **T0** entry `p/absent0.md`, not on tree | halt | `BudgetSourceMissing` | PASS |
| 3 | capped entry whose path resolves to a **directory** | halt | `BudgetSourceMissing` (`is_file()` rejects directories, so a directory cannot masquerade as a deferral) | PASS |

Test 3 was not required by AC-1; it was added because `is_file()` rather than `exists()` is the discriminating call, and a weaker predicate would have re-opened the same class of fail-open. It holds.

**AC-1 PASS.**

### 3.2 AC-2 — the lock cap is charged before the ceiling comparison — **PASS**

> *Criterion:* the lock `token_cap` is added to per-family totals when the row is `DEFERRED-SELF-MEASURED`.
> *Test:* the aggregate ceiling comparison includes the lock cap.

`budget.py:150-158` computes `charged_totals` from `totals` plus `lock_charge`, takes `aggregate_governing` from the **charged** map, and compares that to `AGGREGATE_CEILING`. The measured `totals_t0_t1` are preserved separately in the record, so the measured domain and the compared quantity are both reconstructible — which `aggregate_ceiling_charge` requires.

The decisive test is not that the arithmetic is recorded but that it *gates*. A construction was built in which the measured total passes the ceiling and only the charged total breaches it:

| # | Construction | Expected | Observed | |
|---|---|---|---|---|
| 4 | lock row cap 200 + one file measuring TF-1 3 / TF-2 6 | charge recorded = 200 | `aggregate_ceiling_charge: 200` | PASS |
| 5 | same | charged = `{TF-1: 203, TF-2: 206}` | `{TF-1: 203, TF-2: 206}` | PASS |
| 6 | same | governing = 206, i.e. the **charged** maximum | `206` | PASS |
| 7 | file measuring TF-2 **5802** (passes 6000 uncharged) + lock cap 200 | **halt** | `BudgetBreach: aggregate: charged governing 6002 (measured 5802 + lock charge 200) > ceiling 6000` | PASS |
| 8 | file measuring TF-2 **5800** + lock cap 200 → exactly 6000 | pass, no off-by-one | `governing 6000`, verdict `PASS` | PASS |
| 9 | manifest with **no** lock row | charge 0, charged == measured | `charge=0`, maps equal | PASS |

Test 7 is the one that would have failed before the delta: the pre-AMD-51 comparison of un-charged totals would have returned `PASS` at 5802. Test 8 confirms the gate is `>` and not `>=`, matching "at most 6000".

Recomputed against the live tree with the real declared families (`cl100k_base.tiktoken` pin `223921b7…`, `spiece.model` pin `d60acb12…`):

```
measured totals : {'TF-1': 3895, 'TF-2': 4554}
charge          : 200
charged totals  : {'TF-1': 4095, 'TF-2': 4754}
governing max   : 4754  /  ceiling 6000        verdict PASS
```

Per-file, all PASS: `BOOT.md` 504/504, `FRAMEWORK.md` 748/1100, `core/PRECEDENCE.md` 382/700, `core/laws/INDEX.md` 721/900, `project/BINDING.md` 574/800, `project/STATE.md` 1083/1100, `project/OPEN_ITEMS.md` 542/600, `core/MANIFEST.lock` `DEFERRED-SELF-MEASURED`. The three breaches OI-C-09 recorded from `S-2026-08-08-08` are cured; V-09 passes on the charged comparison. `BOOT.md` sits **exactly** at its amended cap with zero headroom — noted as F-8 (INFO), not a defect.

**AC-2 PASS.**

### 3.3 AC-3 — TCR-001 finding F1 is disposed — **PASS. F1 is CLOSED.**

F1 as recorded at `TCR-001` line 170:

> `budget.measure` treats any capped T0/T1 file absent from the tree as `DEFERRED-EMITTED-THIS-BUILD`. … the deferral is keyed on **absence, not on identity**. If a second capped file were ever absent it would defer rather than fail.

The author of T-002 correctly recorded AC-3 as NOT VERIFIED, since it is discharged only by a distinct test-engineer session. This is that session, and F1 requires evidence in **two** directions. Halting on an absent file (§3.1) is necessary but not sufficient: an implementation that keyed on absence *and* happened to have the lock always absent would pass §3.1 tests 1–3 unchanged. The discriminating case is the converse.

| # | Construction | Absence-keying would… | Path-keying must… | Observed | |
|---|---|---|---|---|---|
| 10 | `core/MANIFEST.lock` **written into the tree** with known content (5 words), then measured | **measure** it: row TF-1 5 / TF-2 10, verdict PASS | still defer | `{"path": "core/MANIFEST.lock", "token_cap": 200, "counts": null, "governing": null, "verdict": "DEFERRED-SELF-MEASURED"}` | PASS |
| 11 | same construction, totals inspection | totals would include the lock's 5/10 | totals must exclude them entirely | `totals_t0_t1 = {'TF-1': 3, 'TF-2': 6}` — the sibling file alone; the on-tree lock contributed nothing | PASS |

Test 10 is the direct refutation of F1's premise. A present, readable, non-empty `core/MANIFEST.lock` is still deferred with null counts, so the branch cannot be keyed on absence. Test 11 confirms `contributes nothing to the per-family totals` holds even when the octets are available to be counted. Together with tests 1–3, the deferral is keyed on the path and on nothing else, in both directions.

**F1 is CLOSED.** The latent fail-open it described no longer exists, and its "worth tightening to an explicit path allowlist" recommendation is satisfied by `LOCK_PATH` at `budget.py:51`.

### 3.4 T-002 deliverable 3 — superseded test assertions

OI-C-09 named three stale assertions. All three are now de-pinned and green in the baseline run:

- `test_stage6_certification_evidence.py::TestV09Recomputation::test_three_breaching_files_confirmed` and `::test_totals_and_governing_family` — the S-08 snapshot constants are removed and retained as commentary; the class now asserts the V-09 *properties*. Correct under AMD-42 `measurement_instant`.
- `test_stage6_coverage_and_build.py::test_v24_live_registry` — the `registered == 28` pin is removed. The replacement asserts the V-24 properties plus `counts["registered"] > 0`, which closes the "a registry that verifies nothing satisfies the equalities" hole. Good practice; the test's present redness is not this assertion's fault (§6).

---

## 4. Priority 2 — conformance re-certification

Re-certification only. No clause was redesigned or reinterpreted; each was read from the manifest and checked against the artifact the build actually produces.

| # | Item | Verdict |
|---|---|---|
| P2-1 | **AMD-43** lock JSON layout, incl. the RFC 8259 escaping clause | **CERTIFIED** |
| P2-2 | **AMD-44** `build_provenance` as a closed six-member set | **CERTIFIED** |
| P2-3 | **AMD-46** `entry_types` | **CERTIFIED** |
| P2-4 | **AMD-47** `binding_pin_write` halt conditions | **CERTIFIED** |
| P2-5 | **AMD-48** `empty_content` | **CERTIFIED** |
| P2-6 | **AMD-48** `run_fixed_values` | **CERTIFIED** |
| P2-7 | **AMD-49** bounded-register 1:1 mapping **as bound into `V-03`** | **NOT CERTIFIED — F-1** |
| P2-8a | new `files[]` entry `open-items-register` | **CERTIFIED** |
| P2-8b | new `files[]` entry `state-register` | **NOT CERTIFIED — F-2** |
| P2-9 | amended `files[boot].token_cap` = 504 | **CERTIFIED** (with F-4 recorded against the §1.8 derivation table) |

Nothing in Priority 2 was left unreached; the two negatives are findings, not budget exhaustion.

### P2-1 — AMD-43 `lock_json_layout` — CERTIFIED

Checked against the 13,277 octets the build actually serialises, not against the source:

two-space indent at every nesting level; no CR anywhere; exactly one terminal LF (and not two); no trailing whitespace on any line; no space before a name separator and exactly one after; one member or element per line; declared member order `framework_version, build_provenance, hash_algorithm, normalisation, aggregate_digest, budget_measurement, files` preserved, `aggregate_digest` preceding `files`, never sorted (`sort_keys` is not passed).

The escaping clause — *"no escaping beyond what RFC 8259 requires — a non-ASCII character is emitted as itself, never as a `\u` escape"* — was checked twice. The live lock contains **zero** backslash escapes of any kind and no `\u` sequence. An adversarial probe serialising `"café — <U+2028>"` confirms `ensure_ascii=False` emits each non-ASCII character as itself, including U+2028, which is legal unescaped under RFC 8259 §7. Conformant.

### P2-2 — AMD-44 `build_provenance` closed six-member set — CERTIFIED

Emitted members, in order: `source_manifest`, `source_manifest_dc1`, `selected_profile`, `compiler_stage`, `build_id`, `timestamp` — exactly the declared `member_order`, six and no more. `compiler_stage` is the integer `6`. The prohibitions were checked as prohibitions, not as absences of the six: `src/aief_stage6/lock.py` contains no reference to `socket`, `getpass`, `os.environ`, `platform`, `sys.version` or `getcwd`, so host, user, working directory, interpreter version and environment capture cannot enter the member by any route in that module.

### P2-3 — AMD-46 `entry_types` — CERTIFIED

An archive was built in memory over the live covered set. 76 entries (75 covered + the lock), **every one** `isreg()`; zero directory, symlink, hard-link, character-device, block-device or FIFO entries. Determinism fields hold on every entry: `mtime 0`, `uid 0`, `gid 0`, empty `uname`/`gname`, mode `0644`. The vacuous 0755 directory clause is retained in the manifest and, correctly, exercises nothing.

### P2-4 — AMD-47 `binding_pin_write` — CERTIFIED

`binding.render_pin_update` performs a value-token-only replacement. Given `core_digest_pin:` + three spaces + a 64-hex value + three spaces + `# inline comment`, the output preserves the indentation, both whitespace runs, the inline comment, the line ending and every other line, changing only the value token. All three declared halt conditions raise:

- zero matching lines → raises
- more than one matching line → raises
- candidate value not 64 lowercase hex → raises

### P2-5 / P2-6 — AMD-48 `empty_content` and `run_fixed_values` — CERTIFIED

`dc1_digest(b"")` = `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, the SHA-256 of zero octets, as declared. Content that normalises to empty (`b"\n\n\n"`, `b"   \n"`) yields the same digest, confirming the "append exactly one terminal LF applies to surviving content, not to emptiness" reading is implemented rather than merely documented.

`run_fixed_values`: `build.run` captures `timestamp` and `build_id` **once**, before the `for i in range(1, max(2, runs) + 1)` emission loop, and threads both into every `_emit_once` call; `budget.measure` and `lock.build_lock_object` accept them as parameters and never call a clock. Two independent serialisations with the same run-fixed pair are byte-identical. AMD-33 is satisfiable by construction.

### P2-7 — AMD-49 bounded-register mapping as bound into V-03 — **NOT CERTIFIED**

See **F-1**. `validation[V-03].verifies` was amended by AMD-49 to require, at BLOCKING severity, that "for every pair declared in `metadata.reproducible.bounded_register_split.pairs` the declared mapping holds in both directions … and the index conforms to `index_grammar`."

`check_v03` (`src/aief_stage6/preconditions.py:341`) implements only the pre-AMD-014 sentence. Its docstring quotes `validation[V-03].verifies` as *"Every law, agent, template, schema, workflow and check reference resolves"* — full stop — and stops there. The strings `bounded_register_split`, `mapping_open_items`, `mapping_state` and `index_grammar` appear **nowhere** in `src/aief_stage6/preconditions.py`, nor anywhere in `src/aief_stage6/`.

V-03 therefore returns `PASS` with `{"roles": 15, "laws": 13, "checks": 25}` while a BLOCKING clause of its own declared contract goes unevaluated. This is a silent partial implementation, which is worse than an unimplemented check: the AMD-31 precondition gate reports a green V-03 and a reader has no signal that half of it was never run.

### P2-8 — the two new `files[]` entries

| id | path | tier | token_cap | on tree | |
|---|---|---|---|---|---|
| `open-items-register` | `project/OPEN_ITEMS_REGISTER.md` | T4 | `null` | yes | **CERTIFIED** |
| `state-register` | `project/STATE_REGISTER.md` | T4 | `null` | **no** | **NOT CERTIFIED** |

Both are declared exactly as `bounded_register_split.rule` requires — T4, `token_cap` null, index retaining the original id/path/tier/cap/owner/boot-step. `open-items-register` is present and 51,666 octets. `project/STATE_REGISTER.md` **does not exist**, so `mapping_state` cannot hold, and the register half of the state pair carries no authority because there is no file to carry it. See **F-2**.

Neither register is inside the DC-4 covered set — but neither are `project/OPEN_ITEMS.md` nor `project/STATE.md`, so this is the covered set's ordinary treatment of the `project` partition and not a finding.

### P2-9 — `files[boot].token_cap` = 504 — CERTIFIED, with F-4

`files[boot].token_cap` is `504` and `BOOT.md` measures governing 504 against it: PASS, exactly at the cap. The amendment does what AMD-50 intended. The consequence for the §1.8 derivation table is recorded as **F-4**.

---

## 5. The evidence module's independence claim — **HOLDS**

`tests/test_stage6_certification_evidence.py` claims to recompute "without importing the `aief_stage6` package". Verified rather than accepted:

- the only module-level imports are `ast`, `hashlib`, `inspect`, `json`, `re`, `pathlib`, `pytest`;
- `tiktoken` and `sentencepiece` are imported inside functions;
- the literal `aief_stage6` occurs exactly once in the whole file — in the docstring at line 11, describing the abstention;
- there is no `importlib`, no `sys.path` manipulation, no `exec`, no `eval`.

The one construct that could have smuggled the subject in is `inspect`, used at line 214 as `inspect.getsource(op.cl100k_base)`. That reads **tiktoken's own installed source** to extract the TF-1 pre-tokenisation pattern, which is precisely what the docstring says it does ("extracted from the installed tiktoken distribution's own source, not from the implementation's transcription") and is the stronger choice: it pins the pattern to upstream rather than to the implementation's transcription of upstream. No route from the test module to `aief_stage6` exists.

Agreement between that module and the builders is therefore evidence of independent reproduction, not self-confirmation. The claim holds.

---

## 6. The two red tests — **a real registry defect**

`tests/test_stage6_coverage_and_build.py::test_v24_live_registry` and `tests/test_stage6_pipeline_stub.py::test_full_pipeline_with_stub_families`.

### 6.1 Root cause — independently reproduced

The author's account was treated as unverified input. DC-1 and DC-2 were re-implemented from `digest_constructions.per_artifact.normalisation` and `.core_aggregate.record`/`.record_order` in a standalone script that imports nothing from `aief_stage6`, and `project/FROZEN.md` was re-parsed independently. Results:

```
registry rows parsed: 29
verified: 28 of 29
  DRIFT  framework/framework.manifest.json
         actual     920eb6eec217732152c452d51f01e471940df6f2e2ffe608c377fccc37814090
         registered 8af8971b78d762e5db2879e50585a78f4e6d497ea707c664a9c06e1ba7e42ff7
unregistered AMD-21 candidates: ['framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md']
rows owed = 30
```

This reproduces `check_v24`'s output digit for digit. The author's three claims are **all confirmed**: registered DC-1 `8af8971b…7e42ff7`, actual `920eb6ee…37814090`, 29 rows where 30 are owed.

One correction of precision. The claim that "the recorded DC-2 aggregate needs replacing" is true *prospectively* but is not a present failure. The recorded aggregate is currently **internally consistent**:

```
recomputed DC-2 over the 29 registered rows: 339581565141702a2f5a79f531efa6c745b1af10bf2ccac4f6651af3053d30dc
STATE.frozen_set_hash                      : 339581565141702a2f5a79f531efa6c745b1af10bf2ccac4f6651af3053d30dc
appears verbatim in FROZEN.md              : True
```

`aggregate_match` is `1`. V-24's DC-2 leg **passes**. Only two of its four legs fail — the DC-1 identity leg and the AMD-21 completeness leg. The aggregate will need replacing as a *consequence* of repairing the rows, not as an independent defect. For whoever performs that repair, the two values are recorded here as computed evidence, not as instruction:

- DC-1 of the unregistered `framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md` = `07ced7582c7dafc8649eb8ac0736d1587ba4cc38c30f11c929240809be639945`
- DC-2 over the repaired 30-row registry = `692521430cbaf7a9cca160d7b658107c408ef8b0eb0a470d7dfc0d9235ccdf16`

**Verdict: a real registry defect.** `project/FROZEN.md` is stale after AIEF-AMD-014. V-24 genuinely FAILS and is correct to fail. Both tests share this single root cause: the pipeline test halts at the AMD-31 gate with `status='PRECONDITION-FAIL'`, `notes=['V-24 FAIL']`, and V-24 is the *only* FAIL among the preconditions. Neither red test indicates any defect in the AMD-45 or AMD-51 delta T-002 delivered.

### 6.2 But the pipeline test is also masking something — F-5

The dispatch asked whether these are a real registry defect *or* a masked implementation defect. The honest answer is that the first test is purely the former and the second is **both**.

Simulated with `check_v24` stubbed to PASS and all writes suppressed:

| tokenizers used | outcome |
|---|---|
| stub families (what `test_full_pipeline_with_stub_families` injects) | `status: OK`, no precondition FAILs, `covered: 75`, DC-5 emitted |
| the real declared TF-1 / TF-2 | **uncaught `BudgetBreach`: `core/MANIFEST.lock: governing 6484 > cap 200 - build halts`** |

So repairing the registry *will* turn the pipeline test green — and the green will be false. The stub families defined at `tests/test_stage6_pipeline_stub.py:29-42` count `len(text) // scale + 1`, giving 133 / 111 tokens for the same 13,277-octet lock that the real families measure at 5,314 / 6,458 — an undercount of roughly **58×**. The stub therefore slides under the 200-token cap and the AMD-45 post-serialisation gate never fires.

The module's own docstring says the stubs exist "ONLY to exercise the emission mechanics", which is a fair scoping. The defect is not that stubs are used; it is that the test asserts `outcome.status == "OK"` — a whole-pipeline success claim — on a tokenizer substitution that structurally disables a BLOCKING gate. Recorded as **F-5**.

---

## 7. The lock self-cap measurement — **CONFIRMED, and understated**

Built in memory from the live tree: the real budget record, the real covered set, `lock.build_lock_object` and `lock.serialise_lock` as `build._emit_once` calls them. Nothing written.

```
files[manifest-lock].token_cap = 200
serialised lock: 13277 octets, 75 files[] entries

WHOLE LOCK   TF-1 5314   TF-2 6458   governing 6458  vs cap 200   -> BREACH (32.3x)

  framework_version      TF-1   14   TF-2   15
  build_provenance       TF-1  114   TF-2  149
  hash_algorithm         TF-1   12   TF-2   19
  normalisation          TF-1   48   TF-2   59
  aggregate_digest       TF-1   45   TF-2   60
  budget_measurement     TF-1  881   TF-2  979
  files                  TF-1 4212   TF-2 5198

measure_text(lock, cap=200)  ->  HALT: core/MANIFEST.lock: governing 6458 > cap 200 - build halts
```

**Confirmed.** The author's specific claim — `budget_measurement` measuring **869 TF-1 / 962 TF-2** on its own — is substantively correct; this session measures **881 / 979**. The ~1.5% divergence is expected AMD-42 `measurement_instant` drift (the record embeds live counts of mutable `project` files) and is not a discrepancy of kind.

**But the claim understates the problem by a factor of six.** The dominant term is not `budget_measurement` at 979; it is `files` at **5,198** — 76 `[path, digest]` pairs at ~69 TF-2 tokens each. Even a `budget_measurement` member reduced to nothing would leave the lock at ~5,479 TF-2 against a 200 cap. The breach is structural in `lock_serialisation` itself, which mandates that `files` carry the full DC-4 pair list inside the 200-capped artifact.

Two consequences worth putting on the record:

1. The whole lock at governing 6,458 exceeds not only its own 200 cap but the **6,000 aggregate boot ceiling** on its own.
2. `budget.py:148-149` states as rationale that *"The cap is an upper bound on the omitted quantity, so the gate over-states and never under-states."* The omitted quantity is measured here at 6,458 against a charge of 200. The rationale is factually false. The **code is nonetheless conformant** — AMD-51 mandates "the charge is the declared cap, never an estimate", and the code charges exactly the declared cap — so this is a defective comment asserting a safety property that does not hold, not a defective implementation. Recorded as **F-6** because a future reader could rely on it.

No repair attempted. The 200 cap is frozen at AIEF-FRZ-001 §1.8 and `framework/**` is outside this session's write scope.

---

## 8. Findings

| id | sev | location | finding |
|---|---|---|---|
| **F-1** | **BLOCKING** | `src/aief_stage6/preconditions.py:341` (`check_v03`) | The AMD-49 bounded-register clause of `validation[V-03].verifies` is **not implemented**. `bounded_register_split`, `mapping_open_items`, `mapping_state` and `index_grammar` appear nowhere in `src/aief_stage6/`. V-03 returns `PASS` without evaluating a clause its own contract declares BLOCKING. Silent partial implementation: the AMD-31 gate reports green with no signal that half the check never ran. Disposes P2-7 as NOT CERTIFIED |
| **F-2** | **BLOCKING** | `framework/framework.manifest.json` `files[state-register]` → `.ai/project/STATE_REGISTER.md` (absent) | The declared register file does not exist in the working tree. `mapping_state` cannot hold and the state pair's authority half is missing. Aggravated by F-1: the check that exists to catch exactly this is the one not implemented. No other precondition detects it either — a full `run_preconditions` sweep produces **no** detail mentioning `STATE_REGISTER`. Disposes P2-8b as NOT CERTIFIED |
| **F-3** | **BLOCKING** | `src/aief_stage6/build.py:85` → `budget.measure_text`; cap at `framework.manifest.json` `files[manifest-lock].token_cap` | The emitted lock measures governing **6,458** against its **200** cap — a 32.3× breach, dominated by the mandated `files` member at 5,198. Once V-24 clears, Stage 6 halts here. The lock as specified by `lock_serialisation` cannot meet the cap declared on it. Not a defect in T-002's delta; a collision between two frozen declarations. Escalation to `chief-systems-engineer` indicated |
| **F-4** | MAJOR | `framework/AIEF-FRZ-001…md:139-140`; `framework.manifest.json` `budget_measurement_record.measurement_domain` | AMD-50's `files[boot].token_cap` 400 → 504 moves the MI-4 sum over the eight capped T0∪T1 entries to **5,904** and the headroom to **96**. The §1.8 derivation table still reads `BOOT.md 400`, `Sum 5,800`, `Headroom 200`, and the manifest's own `measurement_domain` text still cites "whose Sum row of 5800 and Headroom row of 200 are computed over exactly these entries". FRZ-001's DC-1 verifies against FROZEN.md, so the table was deliberately not amended. Whether AMD-50 supersedes the frozen table implicitly is **not resolved here** (LAW-12) |
| **F-5** | MAJOR | `tests/test_stage6_pipeline_stub.py:29-42, 48` | The injected stub families undercount by ~58× on the lock text (133/111 vs 5,314/6,458), which structurally disables the AMD-45 post-serialisation cap gate. The test nonetheless asserts `outcome.status == "OK"`. Proven by simulation: with V-24 stubbed PASS the stub run returns OK while the real-family run raises `BudgetBreach`. Repairing the registry will make this test green on a build that cannot actually complete |
| **F-6** | MINOR | `src/aief_stage6/budget.py:148-149` | Comment asserts "The cap is an upper bound on the omitted quantity, so the gate over-states and never under-states." Measured, the omitted quantity is 6,458 against a 200 charge, so the gate under-states by ~6,258. The code conforms to AMD-51 as written; the stated rationale does not survive measurement and should not be relied on |
| **F-7** | MINOR | `src/aief_stage6/build.py:85` vs `:141-156` | `BudgetBreach` from `measure_text` propagates **uncaught** out of `run()`, whereas the ustar-audit and precondition failures return a structured `BuildOutcome(status="HALT" / "PRECONDITION-FAIL")`. Both halt, but a caller reading `BuildOutcome` cannot distinguish "not run" from "halted on a cap breach". Inconsistent halt contract |
| **F-8** | INFO | `framework.manifest.json` `files[boot]` | `BOOT.md` measures governing **504** against its amended cap of **504** — zero headroom. Any edit to `BOOT.md` breaches V-09 immediately. Not a defect; a fragility worth an owner's attention |

Findings F-1 through F-8 are recorded, not repaired. QA does not fix (LAW-05). None of F-1, F-2, F-4, F-5, F-7 or F-8 lies within `src/aief_stage6/budget.py` or `lock.py` as delivered by T-002.

## 9. Ambiguities recorded, not resolved (LAW-12)

1. **F-4** — whether AIEF-AMD-014 §AMD-50 implicitly amends the AIEF-FRZ-001 §1.8 derivation table, or whether the table's `Sum 5,800` / `Headroom 200` rows are now stale against a manifest that still cites them. Not resolvable from the texts in scope. For `chief-systems-engineer`.
2. **F-3** — whether the 200-token cap on `core/MANIFEST.lock` is intended to bind the whole serialised artifact (the plain reading of `lock_self_measurement`, and what the code implements) or only the "digest read" the §1.8 table annotates that row with. The two readings differ by a factor of 32 and decide whether Stage 6 can ever complete. Not resolved here.
3. **Session-id allocation** — `ROSTER.md` requires a per-dispatch session id but declares no allocator (§ header note).

## 10. Scope this certification does not cover

Stated plainly so the verdict is not read as broader than it is. This report certifies T-002's three acceptance criteria and the nine Priority-2 conformance items enumerated in §4. It does **not** cover: the `src/aief_exec/**` execution layer, `tests/test_exec_*.py`, `project/EXECUTION_ARCHITECTURE.md` or `project/results/**` (owned by a concurrent session; not read); any Stage 1–5 compiler behaviour; V-01…V-25 other than V-03, V-09 and V-24; the eighteen other `files[]` entries absent from the tree (unbuilt `software` and `research` profiles, which are expected absences under the active `mechanical` profile and were not investigated); and the correctness of the OI-C-09 row's own narrative beyond the claims tested above.

---

## 11. Reproduction

```
cd "D:/Fusion Projects/SEWCP_Master_Assembly"
PYTHONPATH=src python -m pytest tests/test_stage6_*.py -q      # 2 failed, 123 passed
```

The four evidence scripts this session wrote are session-scratch, outside the repository, and are not framework artifacts: an independent DC-1/DC-2 registry recomputation importing nothing from `aief_stage6`; a 12-case adversarial probe of AC-1/AC-2/F1 over synthetic manifests; an in-memory lock assembly and dual-family measurement; and a write-suppressed pipeline simulation with V-24 stubbed PASS. Every number quoted above is reproducible from the tree at HEAD `8546960` plus the tokenizer artifacts under `build/stage6/tokenizer_artifacts/`.

**Files written by this session: this file only.**
