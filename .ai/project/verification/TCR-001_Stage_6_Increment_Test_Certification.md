# TCR-001 — Test Certification: Stage 6 Compiler Increment

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-verification-report`.
>
> **Filing note.** Produced and filed by `software.test-engineer · S-2026-08-08-09`, a cold session dispatched at rank-1 human-owner instruction per `project/ROSTER.md` for independent verification implementation and test certification of the Stage 6 compiler increment. The verifier authored none of the artifacts under test; filing this report is the verifier's own declared output (test certification), so producer and filer coincide lawfully here.

| | |
|---|---|
| Subject | `src/aief_stage6/**` (13 modules + `tokenizers.py` platform extension) and the Stage 6 build evidence under `build/stage6/**` |
| Producers of the subject | `software.software-engineer · S-2026-08-08-07` (implementation) · `software.platform-engineer · S-2026-08-08-08` (tokenizer wiring, artifacts, evidence) |
| Verifier | `software.test-engineer · S-2026-08-08-09` |
| Normative basis | `framework/framework.manifest.json` `metadata.reproducible` (DC-1, DC-4 incl. AMD-012 `enabled_role_coverage`, DC-5, `tokenizer_families`, `budget_measurement_record`, `distributable`, `build_time_reproducibility`), `schemas[sch-core-manifest]`, `validation` V-01…V-25; `framework/AIEF-AMD-010` §AMD-25…33; `framework/AIEF-AMD-012` §AMD-39/40 |
| Repository state | HEAD `8546960`, unchanged throughout; no mutating git command executed |
| Date | 2026-08-08 |

---

## 1 · Criteria

Fixed before evidence was gathered; each traceable to a normative authority. LAW-03/LAW-05 discipline: every result is binary.

| # | Criterion | Authority |
|---|---|---|
| C1 | DC-1 normalisation implements exactly the declared algorithm (BOM strip, CRLF and lone CR to LF, trailing-whitespace strip per line, trailing-blank-line removal, exactly one terminal LF, UTF-8; non-UTF-8 rejected) | `digest_constructions.per_artifact` |
| C2 | DC-2/DC-4 shared record grammar, octet ordering, preimage form, self-exclusion, duplicate-path halt, empty-set semantics, 64-lowercase-hex output; both published worked examples reproduce exactly | `frozen_set_aggregate`, `core_aggregate`; AMD-010 §AMD-27 |
| C3 | DC-5 is plain SHA-256 over raw archive octets, no normalisation; FIPS `abc` vector reproduces; sidecar in exact `sha256sum` text convention | `release_digest`; AMD-010 §AMD-28 |
| C4 | Covered-set resolution implements the AMD-39 machine-followable procedure: term (i) hashed-and-emitted, term (ii) enabled-role agent artifacts; halts on unresolvable token, on unhashed target, and on a covered file absent from the tree; working tree never an input to coverage; scope limited to agent artifacts | `core_aggregate.covers` / `.enabled_role_coverage`; AMD-012 §AMD-39/40 |
| C5 | Budget measurement: only capped T0/T1 files measured; the maximum governs per file and in aggregate; 6000 ceiling; any breach under either family halts; record carries all five declared content items; fail-safe — an unavailable family yields `BudgetUnmeasured`, never an estimate | `budget_measurement_record`; `tokenizer_families` incl. `pin_value_rule`, `governing_rule`; V-09 |
| C6 | Lock construction: declared member order (`aggregate_digest` before `files`), all `sch-core-manifest` required fields, validates against the emitted `SCH-core-manifest.schema.json`, `files` as [path, digest] pairs in DC-4 record order, `aggregate_digest` = DC-4 over exactly those pairs, refusal to build a conforming lock on a non-PASS budget verdict | `core_aggregate.lock_serialisation`, `.target_fields`; `schemas[sch-core-manifest]`; AMD-029 |
| C7 | Distributable: uncompressed POSIX ustar, `aief-<semver>-<profile>.tar`, entry set = covered set + lock rooted at `.ai/`, ascending octet order, mtime 0 / uid 0 / gid 0 / empty uname,gname / mode 0644, byte-identical across repeat builds; a path that does not fit the ustar name(100)/prefix(155) split HALTS — no pax fallback | `distributable`; `build_time_reproducibility`; AMD-030/033; VER-004 FIND-Q4-2 |
| C8 | BINDING pin rendering is a pure function: value token replaced, every other byte preserved, non-hex64 refused, zero/multiple pin lines refused; the real `.ai/project/BINDING.md` is never touched and still carries `PENDING-STAGE-6` | `core_aggregate.self_exclusion` (F-06 pin); `generation_order[6]` pin write; OQ-14 |
| C9 | Write guard refuses every write into `.ai/**`, `framework/**`, `spec/**` and any canonical `MANIFEST.lock` outside `build/` | dispatch prohibitions; `generation_order[6].barrier`; OQ-14 |
| C10 | The builders' AMD-31 precondition claims reproduce on a fresh run: V-01…V-08, V-23…V-25 PASS; V-09 FAIL with exactly the claimed breaches; driver halts with `PRECONDITION-FAIL`, emitting no lock, no archive, no DC-5 | AMD-010 §AMD-31; V-01…V-09, V-23…V-25 |
| C11 | Tokenizer artifact pins recompute from raw octets and match the trust-on-first-use record | `tokenizer_families` tf-1/tf-2 `.pin`; AMD-026; VER-004 FIND-Q4-1 |
| C12 | The DC-4 preview aggregate and covered count reproduce under a fully independent re-implementation of DC-1 + AMD-39 + DC-4 (no `aief_stage6` import); the three enabled `software.*` agent artifacts are covered, `core/MANIFEST.lock` and unhashed partitions are not | AMD-012 §AMD-39; `core_aggregate` |
| C13 | The V-09 measurement reproduces under independently assembled TF-1/TF-2 (pattern taken from the installed tiktoken distribution's own source, ranks parsed from the artifact in hand; SentencePiece over the artifact in hand): the three per-file breaches, no unclaimed breach, both family totals, TF-2 governing | V-09; `tokenizer_families`; AMD-026 |
| C14 | The two recorded determinism executions (`build/stage6/detcheck/`) are byte-identical and internally coherent with the claimed DC-4 and precondition results | `build_time_reproducibility`; AMD-033 |
| C15 | Verification footprint lawful: HEAD unchanged at `8546960`; no write into `src/**`, `.ai/**` (beyond this report), `framework/**`, `spec/**`; no canonical lock; no BINDING edit; no ledger write; no AI attribution | dispatch prohibitions; V-22; AMD-020 |

## 2 · Method

1. **Certification suite authored from the normative texts first.** The four modules `tests/test_stage6_certification_*.py` (86 tests) were written by transcribing the declared constructions from `framework.manifest.json` `metadata.reproducible`, AMD-010 and AMD-012 into expected behaviour — worked examples as hard constants, preimages hand-built with `hashlib` inside the tests — and only then executed against the implementation. Synthetic manifests/bindings and temp-dir fixtures throughout; the write guard was exercised against a fixture repository copy; no test writes into the real tree.
2. **Independent evidence recomputation.** `tests/test_stage6_certification_evidence.py` re-implements DC-1, the AMD-39 covered-set procedure, DC-4 and the dual-family V-09 measurement inside the test module, without importing `aief_stage6`, and compares against the builders' recorded numbers. Artifact pins additionally recomputed with `sha256sum` at the shell.
3. **Fresh driver run.** `aief_stage6.build.run` executed with output redirected to the session scratchpad (outside the repository); outcome compared with `build/stage6/preconditions.json` and both `detcheck` summaries.
4. **Full suite execution:** `python -m pytest tests/` — 114 tests (86 certification + 28 pre-existing builder tests).
5. **Environment:** Windows 11, Python 3.11, pytest 9.1.1, tiktoken 0.13.0, sentencepiece, jsonschema 4.26.0; artifacts from `build/stage6/tokenizer_artifacts/` only (offline; nothing fetched).

Repeatability: every command above is deterministic given HEAD `8546960` and the provisioned artifacts; an independent party re-running `python -m pytest tests/ -q` obtains the same 114 results.

## 3 · Evidence

### 3.1 · Recomputed digests (all full 64, all recomputed this session)

| Value | Recomputed | Matches claim |
|---|---|---|
| TF-1 pin, raw-octet SHA-256 of `cl100k_base.tiktoken` (1,681,126 octets) | `223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7` | YES (TOFU record, PE claim) |
| TF-2 pin, raw-octet SHA-256 of `spiece.model` (791,656 octets) | `d60acb128cf7b7f2536e8f38a5b18a05535c9e14c7a355904270e15b0945ea86` | YES (TOFU record, PE claim) |
| DC-4 preview aggregate over the real tree (75 covered files, independent re-implementation) | `2180df021b892ee0c19d7bc164713e46b1003bfb193497cad06b6c20f5ac92f0` | YES (SE claim, detcheck exec1 = exec2) |
| DC-2 worked example | `8de12581a7d3aef29454fcdfd696a71e4d5c1a0352f69c7a6b03b167d0f5f1b3` | YES (normative constant) |
| DC-4 worked example | `eb6e969b9f1d31a367ccf83315c1a40f8df0bb1c7dec41566a637ac3740325b1` | YES (normative constant) |
| DC-2 empty registry | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | YES (normative constant) |
| DC-5 FIPS `abc` vector | `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` | YES (normative constant) |
| DC-2 frozen-set aggregate, 28 rows (independent recompute = FROZEN.md = STATE.frozen_set_hash) | `a743cf6fcb9a69b841deaced59cc34fd6adc0a1f31c0c84cab24ab44b80a6a53` | YES (V-24 substance) |

### 3.2 · V-09 recomputation (independent tokenizer assembly)

Per-file, capped T0/T1 set, both families; cap semantics "the maximum governs":

| Path | Cap | TF-1 | TF-2 | Governing | Verdict |
|---|---|---|---|---|---|
| `BOOT.md` | 400 | 445 | 504 | 504 | **FAIL** |
| `FRAMEWORK.md` | 1100 | 652 | 748 | 748 | PASS |
| `core/MANIFEST.lock` | 200 | — | — | — | not on disk (Stage 6 emission) |
| `core/PRECEDENCE.md` | 700 | 341 | 382 | 382 | PASS |
| `core/laws/INDEX.md` | 900 | 598 | 721 | 721 | PASS |
| `project/BINDING.md` | 800 | 483 | 574 | 574 | PASS |
| `project/STATE.md` | 1100 | 1516 | 1791 | 1791 | **FAIL** |
| `project/OPEN_ITEMS.md` | 600 | 6261 | 7937 | 7937 | **FAIL** |
| **Totals (T0+T1)** | ceiling 6000 | **10296** | **12657** | **12657 (TF-2 governs)** | **FAIL** |

Every number equals the PE's diagnostic (`build/stage6/v09_measurement_report.DIAGNOSTIC.json`) exactly. Note: the aggregate breach is not family-marginal — TF-1 alone (10296) also exceeds the 6000 ceiling.

### 3.3 · Fresh driver run (this session, output to scratchpad only)

`status=PRECONDITION-FAIL`; `covered_count=75`; `dc4_aggregate=2180df02…ac92f0`; `dc5=None` (correct — no emission after halt); max archive path 65 octets (`.ai/core/profiles/mechanical/agents/AGT-manufacturing-engineer.md`, well inside ustar limits); V-01…V-08, V-23…V-25 PASS; V-09 FAIL with exactly the three breaches and aggregate of §3.2. Identical to `build/stage6/preconditions.json` and to both `detcheck` summaries, which are byte-identical to each other.

### 3.4 · Test inventory — authored by this session (86 tests, all from normative text)

`tests/test_stage6_certification_digests.py` (28):
TestDc1Normalisation — terminal_lf_appended_exactly_once, bom_stripped, crlf_converted, lone_cr_converted, mixed_cr_crlf_lf, trailing_whitespace_stripped_every_line, leading_whitespace_preserved, interior_blank_lines_preserved, trailing_blank_lines_removed, idempotent, digest_is_sha256_of_normalised_content, non_utf8_input_rejected_not_absorbed.
TestAggregateGrammar — dc2_worked_example, dc4_worked_example, worked_examples_from_first_principles, input_order_carries_no_meaning, octet_order_shorter_prefix_first, preimage_exact_bytes_no_header_no_bom, duplicate_path_halts_dc2, duplicate_path_halts_dc4, empty_registry_dc2_declared_value, empty_set_dc4_never_lawful, truncated_digest_prohibited, self_exclusion_is_callers_duty_but_grammar_accepts_any_path.
TestDc5 — fips_abc_vector, no_normalisation_of_any_kind, sidecar_exact_convention, sidecar_refuses_truncated_digest.

`tests/test_stage6_certification_coverage_budget.py` (20):
TestCoveredSetTermOne — baseline_covered_set, lock_self_exclusion, unhashed_partitions_never_covered, hashed_but_not_emitted_for_selected_not_covered.
TestCoveredSetTermTwo — non_selected_profile_token_adds_agent_artifact, undotted_token_adds_nothing, selected_profile_token_adds_nothing, unresolvable_token_halts, token_resolving_to_unhashed_entry_halts, working_tree_is_never_an_input_to_coverage.
TestHashCoveredSet — pairs_are_dc1_digests, covered_file_absent_from_tree_halts.
TestBudget — maximum_governs_per_file, cap_equal_to_governing_passes, aggregate_ceiling_maximum_governs, only_capped_t0_t1_files_measured, record_carries_declared_content, failsafe_unavailable_family_raises_never_estimates, probe_with_empty_artifact_dir_blocks, measure_text_halts_on_breach.

`tests/test_stage6_certification_lock_archive_guard.py` (28):
TestLock — member_order_exactly_as_declared, aggregate_digest_precedes_files_in_octets, all_sch_core_manifest_required_fields_present, emitted_lock_validates_against_emitted_schema, files_member_is_pairs_in_dc4_record_order, aggregate_digest_is_dc4_over_the_files_member, non_pass_budget_refused[UNMEASURED], non_pass_budget_refused[FAIL], serialisation_deterministic_utf8_lf_terminal_lf.
TestDistributable — archive_name_convention, two_builds_byte_identical, entry_set_and_order, header_discipline, no_pax_or_gnu_extended_headers, lock_bytes_embedded_exactly, ustar_fits_boundaries, long_path_halts_no_pax_fallback.
TestPinRender — value_token_replaced_rest_preserved, rejects_non_hex64_pin, rejects_zero_or_multiple_pin_lines, real_binding_file_untouched_by_render.
TestWriteGuard — readonly_partitions_refused[.ai/core/MANIFEST.lock], [.ai/project/BINDING.md], [.ai/BOOT.md], [framework/framework.manifest.json], [spec/anything.md], canonical_lock_refused_anywhere_outside_build, build_area_and_outside_repo_allowed.

`tests/test_stage6_certification_evidence.py` (10):
TestArtifactPins — tf1_pin_recomputed, tf2_pin_recomputed, tofu_record_internally_consistent.
TestDc4Aggregate — covered_count_and_aggregate, three_enabled_software_artifacts_are_covered, lock_and_unhashed_partitions_absent.
TestV09Recomputation — three_breaching_files_confirmed, no_other_per_file_breach, totals_and_governing_family.
TestDetcheckEvidence — two_execution_summaries_identical.

**Results: 86/86 PASS.** Full tree including the builders' 28 pre-existing tests: **114/114 PASS.** During authoring, two initial failures occurred in the certification suite itself (a vacuous uppercase-digest case built from an all-digits constant); both were test-authoring errors in this suite, corrected to genuinely discriminating inputs, after which the implementation passed. **No implementation defect was found by any test.**

## 4 · Per-criterion pass or fail

| # | Criterion | Result | Evidence |
|---|---|---|---|
| C1 | DC-1 normalisation | **PASS** | §3.4 digests module, 12/12 |
| C2 | DC-2/DC-4 grammar and worked examples | **PASS** | §3.4, 12/12 incl. both worked examples from first principles |
| C3 | DC-5 + sidecar | **PASS** | §3.4, 4/4 incl. FIPS vector |
| C4 | AMD-39 covered set incl. halts | **PASS** | §3.4, 12/12; halts verified on temp fixtures only |
| C5 | Budget semantics + fail-safe | **PASS** | §3.4, 8/8; `BudgetUnmeasured` raised, no estimate path exists |
| C6 | Lock serialisation and refusal | **PASS** | §3.4, 9/9 incl. validation against emitted `SCH-core-manifest.schema.json` |
| C7 | ustar determinism + long-path halt | **PASS** | §3.4, 8/8; byte-identical repeat builds; >100-octet unsplittable path halts, no pax |
| C8 | Pin renderer purity | **PASS** | §3.4, 4/4; real BINDING byte-identical before/after, pin still `PENDING-STAGE-6` |
| C9 | Write guard | **PASS** | §3.4, 7/7 on fixture repo copy |
| C10 | Precondition claims reproduce | **PASS** | §3.3 fresh run identical to recorded evidence |
| C11 | Artifact pins | **PASS** | §3.1 rows 1–2, recomputed twice (shell + test) |
| C12 | DC-4 aggregate independent reproduction | **PASS** | §3.1 row 3; 75 files; three `software.*` agent artifacts covered; lock and unhashed partitions excluded |
| C13 | V-09 independent reproduction | **PASS** | §3.2 — every count, both totals, TF-2 governing, no unclaimed breach |
| C14 | Determinism evidence coherent | **PASS** | detcheck exec1 = exec2 byte-identical; contents match §3.3 |
| C15 | Verification footprint | **PASS** | HEAD `8546960` before and after; footprint = 4 test files + this report + scratchpad only |

| Summary | |
|---|---|
| Criteria | 15 |
| Pass · Fail · Not verified | 15 · 0 · 0 |
| Overall | **PASS** — the implementation is certified correct against the approved constructions |

## 5 · Independence declaration

| | |
|---|---|
| Verifier | `software.test-engineer · S-2026-08-08-09` (A1), cold session, no state from any prior session |
| Producers of the artifacts under test | `software.software-engineer · S-2026-08-08-07` · `software.platform-engineer · S-2026-08-08-08` |
| Independent | Verifier authored no line of `src/**` and none of the builders' tests or evidence; under AMD-20 (identity = role × session) verifier differs from both producers in role and session — **confirmed**. The contract bar "may not test code it authored" (`AGT-test-engineer.md`, Separation of duties) is satisfied. |
| Context | cold subagent dispatch at rank-1 human-owner instruction |
| Method independence | Certification expectations derived from the normative texts before execution; evidence recomputation uses re-implementations written in the test module without importing the package under test; the TF-1 pattern was taken from the installed tiktoken distribution's own source, not from the implementation's transcription |

## 6 · Certification scope — what is and is not certified

**CERTIFIED (implementation correctness vs the approved constructions):**

1. `src/aief_stage6/**` implements DC-1, DC-2/DC-4, DC-5, the AMD-39 covered-set procedure, the AMD-29 budget record with the AMD-26 governing rule and fail-safe, the AMD-27 lock serialisation, the AMD-30 deterministic ustar distributable with the FIND-Q4-2 long-path halt, the AMD-33 in-build determinism check, the preview-only pin rendering, and the read-only write guard — each exactly as declared, at the tested surface.
2. The builders' recorded results are independently reproduced: the AMD-31 precondition table (V-01…V-08, V-23…V-25 PASS), the V-09 FAIL with its three per-file breaches and 12657-vs-6000 aggregate (TF-2 governing), both tokenizer artifact pins, the DC-4 preview aggregate `2180df021b892ee0c19d7bc164713e46b1003bfb193497cad06b6c20f5ac92f0` over 75 covered files, and the two-run byte-identical determinism evidence.
3. The build's halt is **correct behaviour**: with V-09 failing, the driver refuses every conforming emission (no lock, no archive, no DC-5, no pin write) — exactly the AMD-31 gate and the verdict rule.

**NOT CERTIFIED (outside this certification, explicitly):**

1. **The V-09 content breaches themselves.** `BOOT.md` (504 > 400), `project/STATE.md` (1791 > 1100), `project/OPEN_ITEMS.md` (7937 > 600) and the aggregate (12657 > 6000; TF-1 alone 10296 > 6000) are content/architecture facts of the tree, not code defects. Their disposition (content reduction, cap amendment, or other ruling) is an A4/human-owner matter. Until disposed, no conforming `core/MANIFEST.lock` can lawfully exist.
2. **V-10 in full meaning.** Only single-platform (Windows) determinism evidence exists. The two-platform requirement (Windows plus at least one of Linux/macOS, AMD-33) has no recorded evidence and is not certified.
3. **The SE's open questions awaiting A4 disposition**, recorded in the module docstrings (no separately filed dispatch report was found on disk — see Finding F2): DC-1's undefined empty-file case; the undeclared lock JSON layout details and `build_provenance` member content; the lock-inside-its-own-cap fixed point (interim: post-serialisation `measure_text`); the archive "nothing else" vs directory-mode tension (interim: regular-file entries only); the post-write layout of the BINDING pin line. Each interim choice is deterministic and disclosed, but none is normatively ruled; this certification covers their current behaviour, not their normative correctness.
4. **Canonical Stage 6 execution.** Remains unauthorized (OQ-14). Nothing here authorizes emission of a canonical `core/MANIFEST.lock`, a BINDING pin write, or a release archive.
5. **Everything outside the increment:** Stages 1–5 as software (CMP-BLOCK-004 full scope), the campaign checks V-11…V-21, and V-14's trial count (OI-V-06).

## 7 · Findings (informational — no disposition required for certification)

| ID | Severity | Finding |
|---|---|---|
| F1 | INFO | `budget.measure` treats any capped T0/T1 file absent from the tree as `DEFERRED-EMITTED-THIS-BUILD`. Today only `core/MANIFEST.lock` can be absent, and the lock is separately cap-checked post-serialisation, so the behaviour is safe; but the deferral is keyed on absence, not on identity. If a second capped file were ever absent it would defer rather than fail. Worth tightening to an explicit path allowlist when the lock fixed-point question (§6.3) is ruled. |
| F2 | INFO | The "dispatch report" that the SE's docstrings cite as the home of its Open Questions is not on disk; the questions are recoverable only from `src/aief_stage6/*.py` docstrings. Recommend the coordinating session file them as a register entry so the A4 disposition has a single subject artifact. |
| F3 | INFO | Two transient failures during certification authoring were defects of this suite (vacuous uppercase-hex case from an all-digits constant), not of the implementation; corrected before certification. Recorded for completeness under LAW-05 — the suite's own first run is evidence about the suite, not the subject. |

## 8 · Certification disposition

**CERTIFIED — PASS (15/15 criteria).** The Stage 6 compiler increment `src/aief_stage6/**`, as extended by the platform engineer, correctly implements the approved constructions of AMD-010/AMD-012 and the manifest's `metadata.reproducible` declarations at every tested surface, honestly reproduces its recorded evidence, and fails safe everywhere the normative texts demand a halt. The current build outcome — `PRECONDITION-FAIL` on V-09 — is the correct, certified behaviour of correct software confronting non-conforming content; the breaches themselves await an A4/owner disposition and are expressly not certified here.

Actor: `software.test-engineer · S-2026-08-08-09`
