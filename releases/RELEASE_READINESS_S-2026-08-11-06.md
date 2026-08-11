# SEWCP Release-Readiness Report — `S-2026-08-11-06`

> **Instance artifact.** Partition `releases`. Audit of the engineering baseline at checkpoint
> `baf843a`. Every figure below is **computed**, never asserted; the command that computes it is
> named beside it.
>
> **No verified CAD geometry was modified by this audit**, and none needed to be. Every
> `spec/**` digest is unchanged from the incoming baseline.

---

## 1 · Verdict

# NOT READY — BLOCKERS REMAIN

**Two blockers, neither of them an engineering defect.** Every engineering item within the
delegated authority was resolved, implemented and verified; what remains is one act the host
permission layer refused, and one act that by law requires a second party.

| # | Blocker | Class | What clears it |
|---|---|---|---|
| **B1** | **Compiler Stage 6 canonical emission not performed.** `.ai/core/MANIFEST.lock` is not written and `BINDING.core_digest_pin` is still `PENDING-STAGE-6`, so **boot step B2a cannot execute** and core integrity cannot be *proven*. The `OQ-14` authorization **has been given** by the human owner and every engineering precondition passes: the preview build is `OK`, 12/12 AMD-31 compile-time checks PASS, byte-identical across two executions, lock boot-read prefix 69/200, DC-4 and DC-5 computed. **The build was refused by the host permission layer, not by any engineering condition** | **Environmental** | One permitted execution of the canonical build. §7 |
| **B2** | **`OI-V-13` — independent cold-context QA audit of this session, not performed.** This session raised `ECR-D-014`, ruled it and `ECR-D-006`, authored `AIEF-AMD-015`, applied it to the frozen manifest, implemented it in `src/**`, and wrote its own tests. LAW-05 bars self-verification; LAW-02 clause 5 bars closure by the raiser and **is not satisfied for `ECR-D-014`**. `ECR-D-006` and `ECR-D-014` are dispositioned and applied but **NOT CLOSED** — `closed_at` is `null` on both | **Governance, non-delegable** | A `qa-engineer` audit in a distinct cold session |

Neither blocker is a defect in the design, the specification, the CAD or the deliverables.

---

## 2 · Release-readiness matrix

| ITEM | STATUS | EVIDENCE | BLOCKER? |
|---|---|---|---|
| **CAD — nine components** | **COMPLETE** | `cad/runs/**` per-component records; 11 authoritative Fusion lineages observed | No |
| **Assembly** | **COMPLETE** | `ASSEMBLY_S-2026-08-11-05` PASS, 19 occurrences, 7.6997 kg | No |
| **Interfaces** | **COMPLETE** | `SYSTEM_INTERFACES.json` 12/12; `FINAL_SYSTEM_VERIFICATION.json` **19/19 PASS** | No |
| **Gate `LC-M04-EXIT`** | **PASS** | `python -m aief_gate` → `LC-M04 CAD-READY: YES`, exit 0 | No |
| **Feature clearance** | **PASS** | `python -m aief_clearance` → `CLEARANCE OK` | No |
| **Parameter master** | **PASS** | `python -m aief_params check` → 105 derived | No |
| **Engineering decisions** | **COMPLETE, fully provenanced** | `DECISIONS_S-2026-08-11-05` DEC-01…04; `DECISIONS_S-2026-08-11-06` DEC-05…10 | No |
| **Approval chains** | **CLEAN — first time in this repository's history** | `python -m aief_approval verify` → `APPROVAL CHAINS OK`, exit 0 | No |
| **Freeze registry** | **31 of 31 verify** | `V-24` PASS, aggregate `701db1fd…f618aa50` | No |
| **Drawings** | **COMPLETE** | 11 documents / 14 sheets, SVG + PDF + provenance JSON; `FSV-DRAWINGS` 79 dims, 0 unsourced | No |
| **BOM** | **COMPLETE** | `SEWCP-000_BOM_RevA.csv`, digest `bca24310b3bdd083`, `FSV-BOM` clean 4 ways | No |
| **Manufacturing documentation** | **COMPLETE** | Masking sheet, FSW tool envelope, flat pattern with bend stations, finishes as drawing notes | No |
| **Deliverables** | **COMPLETE — 62 / 62 digests match, bi-directionally** | §5 | No |
| **`ECR-D-006`** | **DISPOSITIONED A, applied, verified — NOT CLOSED** | `APR-033`/`APR-034`; registry 29 → 30 | **No** (B2 gates closure) |
| **`ECR-D-014`** *(new)* | **RAISED + DISPOSITIONED A, applied, verified — NOT CLOSED** | `AIEF-AMD-015`; `APR-035`/`APR-036`; registry 30 → 31 | **No** (B2 gates closure) |
| **`OI-CAD-03`** | **DISPOSITIONED — all four PRESERVE, none deleted. OPEN, OWNER-RESERVED** | `cad/LINEAGE_CENSUS.md`; `LINEAGE_ROSTER_S-2026-08-11-06.json` | **No** |
| **`OQ-14`** | **AUTHORIZATION GIVEN by the human owner** | `DECISIONS_S-2026-08-11-06` DEC-10, verbatim | No — but see B1 |
| **Stage 6 — preview** | **OK, 12/12 preconditions PASS** | `python -m aief_stage6` | No |
| **Stage 6 — canonical** | **NOT PERFORMED** | §7 | **YES — B1** |
| **Boot step `B2a`** | **CANNOT EXECUTE** | No `core/MANIFEST.lock`; pin `PENDING-STAGE-6` | **YES — B1** |
| **Physical verification** | **0 of 91 verified. NOT VERIFIED — HARDWARE REQUIRED** | `PVR-001` | **Not for release; YES for build** |
| **`CP-02`** | **NOT VERIFIED — flow bench.** Margin direction **corrected**: −53 %, not +25 % | `PVR-001` §3; DEC-07 | Build release only |
| **`CP-11`** | **NOT VERIFIED — thermal map.** Film ΔT **8.79 K**, 14 % above the recorded figure | `PVR-001` §4 | Build release only |
| **Repository** | **CLEAN — 799 tests pass, 0 fail** | `pytest tests/ -q` | No |
| **`OI-V-13`** | **OWED, NOT PERFORMED** | §1 B2 | **YES — B2** |
| **GitHub** | **NOT PUSHED, correctly.** 30 commits ahead of `origin/main` | Push date **2026-09-01** stands | Deliberate |

---

## 3 · What this audit found — five defects, four repaired

The incoming baseline reported "2 known pre-existing `ECR-D-006` failures". **That count was
low.** Both are gone, and three further defects were found beneath them.

### 3.1 · `ECR-D-006` was two defects, and only one was on record

The ECR names the manifest digest divergence. The audit found a second, never recorded: **the
`AIEF-AMD-014` change set had been applied with every record of its authority omitted.**
`APR-014` and `APR-015` were never filed; the registry row was never re-registered; and
`AIEF-AMD-014` itself was never added to the registry under the AMD-21 criterion **its own
§ *Blast Radius* declares**. `check_v24` names the omission in terms. It stood undetected for
three sessions.

**Disposition A**, under owner-delegated authority. The attribution rests on a **git object**,
not a reconstruction: `git show 8546960:framework/framework.manifest.json` reproduces
`ae16ccac…9d8395aa`, `APR-006`'s `subject_hash`, recorded four sessions before the defect. The
delta was taken structurally over the parsed JSON — **27 changed leaves, zero removals, every
leaf carrying its own authorising citation**, counts matching each instrument's own enumeration
(3 / 13 / 11, the eleven partitioning 4 + 2 + 1 + 4 exactly as `AIEF-AMD-014` declares).

**One departure from the recommendation, on evidentiary grounds.** `AIEF-AMD-014` §AMD-53
directs `prior_hash` be the measured `e87ae68e…`. `APR-033` records `8af8971b…` instead, strictly
as a chain link. `e87ae68e…` is another session's reconstruction of bytes never committed; **this
session has not measured it and cannot**, and signing a measurement not taken is the failure the
ECR exists to record.

**Not repaired, and recorded as such:** the `AIEF-AMD-013` intermediate state is unreproducible
and always will be.

### 3.2 · `ECR-D-014` — the first authorised Stage 6 build halted, correctly

```
aief_stage6.budget.BudgetBreach: core/MANIFEST.lock: governing 6469 > cap 200
```

Two clauses of the same frozen artifact cannot both hold. `lock_self_measurement` (AMD-45)
measures the whole document; `lock_serialisation` (AMD-27) says *"aggregate_digest precedes files
**so the T1 digest read stays within the 200-token cap**"* — which is a statement that the cap
bounds a **prefix**, and the only reading under which member ordering can bear on the count.

**No conforming lock of any content meets 200**: `files` is schema-required at one path-digest
pair per covered file (75 here, 5198 TF-2 tokens), and the schema-required members **with `files`
removed** still measure 285. A raise to 6469 puts MI-4 at 12173 against a 6000 ceiling.

**Disposition A** (`AIEF-AMD-015` §§AMD-54/55): the measured quantity is the **boot-read prefix**,
and `aggregate_digest` moves to second position so that prefix contains no run-scoped octet.
**69 TF-2 against 200 — a 2.9× margin. MI-4 unchanged at 5904 of 6000. No `token_cap` altered.**

**Why nobody had seen it:** the certification harness injects a stub tokenizer probe; the only
real-tokenizer path halted at `PRECONDITION-FAIL` while `V-24` and `V-25` were failing; and
`TCR-001` certified that the code implements the declared constructions — which it does — while
nothing compared the declared cap against the artifact those constructions produce. **Fixing
`ECR-D-006` is what let the build get far enough to find this.**

### 3.3 · `V-25` — a recorded prediction, realised

62 files carried CR in the working tree. `OI-V-05` FIND-Q3-4 predicted it in terms. Cured by a
`.gitattributes` declaration over the whole `V-25` domain; **no registered digest moved** —
verified by comparing all 62 DC-1 values before and after, and by an empirical checkout test.

### 3.4 · `V-03`'s bounded-register half — declared BLOCKING, implemented by nothing

`AIEF-AMD-014` §AMD-49 bound the index↔register mapping into `V-03` and declared a break of it
BLOCKING. `check_v03` implemented only the cross-reference half. **The moment the missing half
was implemented it found two live breaks** — five register rows carrying a decorated leading cell
instead of a bare identifier, and two rows in a section the index disagreed with. `V-03` had been
reporting PASS throughout. Both repaired; ten adversarial tests added.

### 3.5 · `aief_approval` reported a LAW-10 violation no rule produces

`APR-003` binds eight framework artifacts in one instrument and says why in its own body. The
flat YAML parser read its block-sequence `subject_path` as empty, reported *"no subject_path —
LAW-10 clause 1"*, and **skipped the record — so all eight bindings went unchecked.** Repaired:
the parser reads block sequences, unequal path/hash counts are rejected, and a multi-subject
approval is void if **any** binding breaks. All eight now verify LIVE. This is why
`aief_approval verify` exits 0 for the first time.

---

## 4 · Physical verification — honest, and unchanged by any of the above

**`PVR-001`** is filed, and its matrix is **derived from the frozen specification** by
`tests/test_physical_verification_record.py`, not transcribed.

| | |
|---|---|
| Numbered component requirements | **137** |
| Dischargeable at the desk | **46** |
| **Require physical hardware** | **91** (7 hybrid) |
| **Verified by physical evidence** | **0** — no article exists |

**Nothing is marked PASS anywhere.** The four mass rows are `MODEL-PREDICTED` and labelled so; a
scale needs a part.

### Two corrections of record, neither changing any geometry

1. **`CP-02` margin direction was recorded backwards.** `DECISIONS_S-2026-08-11-05` DEC-04 says
   ΔP *"falls roughly with length (−25 %), **increasing** CP-02 margin"*. The −25 % is correct for
   the length term alone; it omits the `ECR-D-002` section term, which is **+105 %**. Net against
   the sizing basis: **+53 %. `CP-02` margin decreased.** `spec/01` — which governs — always said
   so: *"the hydraulic direction is adverse and is open"*. DEC-04's **conclusion** stands; only
   its reason was wrong. **`CP-02` is the requirement most at risk in the specification and
   should be the first bench test on the first FSW-closed article.**
2. **`spec/01` §2.1's wetted-area row is stale after `ECR-D-002`** — 0.080 m² implies a 36.4 mm
   perimeter against the channel's actual 32.0 mm. Correct as-routed value **0.0525 m²**; film ΔT
   at 3 kW **8.79 K**, 14 % above DEC-04 and 51 % above what §2.1 implies. Raised as
   **`ECR-Q-013`** and **deliberately not applied** — §2.1 is a design-basis table, no acceptance
   criterion moves, and the `ECR-Q-010` precedent governs.

### Two desk items that are not discharged and need no hardware — `OI-C-15`

`SR-07`/`AP-08` analyses of record were run at **7.5 kg** against an as-modelled **7.6997 kg**
(+2.66 %, per-pin lateral 122.62 → 125.89 N, absorbed by `ECR-D-007`'s 4.4–6.9× margin but not
re-run); and the five `SR-03`/`SR-04`/`RF-09`/`RF-10`/`RF-11` creepage/clearance drawing traces
have never been filed.

---

## 5 · Deliverable audit — `D:\AIEF_CAD_OUTPUT\SEWCP\`

**62 files, 5,054,400 bytes. 62 digests recorded in `cad/DELIVERABLES.md`. 62 match. Zero
unmatched, zero unrecorded — the agreement is bi-directional.**

| Class | Count | |
|---|---|---|
| STEP | 11 | 10 components + assembly |
| STL | 10 | one per component |
| F3D | 1 | assembly |
| Drawings | 39 | 14 SVG + 14 PDF + 11 provenance JSON, over 11 documents |
| BOM | 1 | indentured Rev A |

Flat pattern with bend stations is carried as `SEWCP-901` drawing content, as designed. No
deliverable was moved into git.

---

## 6 · `OI-CAD-03` — four lineages, all PRESERVE, none deleted

Roster confirmed by observation: **15 = 11 authoritative + 4 quarantined**, matching the
register's count. **Not one quarantined lineage is referenced by the assembly, the assembly run
record, `FINAL_SYSTEM_VERIFICATION`, `SYSTEM_INTERFACES`, the BOM, or any deliverable.**

`ZZ-DERIVATIVE-STUCK_SEWCP-200` is at **v7** — the only lineage above v2 in the project — and
holds the **entire modelling history of the Cooling Plate**. The re-homed replacement is at v2
and carries the verified content with **none** of the history. **Deleting it destroys required
engineering history irrecoverably**, and the same is true of the free-S strap. The other two are
recorded in full at `ECR-D-013` and `ECR-Q-012`, so deletion is defensible and still not
recommended.

**Nothing was deleted. `OI-CAD-03` remains OPEN, OWNER-RESERVED and NON-BLOCKING.**

---

## 7 · Stage 6 — what was done, and the one thing that was not

| | |
|---|---|
| `OQ-14` authorization | **GIVEN, by the human owner**, in this run's written instruction, quoted verbatim at `DECISIONS_S-2026-08-11-06` DEC-10. Recorded as the owner's act, **not** as delegated authority — an authorization is not an engineering judgement |
| Preview build | **`OK`.** 12/12 AMD-31 compile-time preconditions PASS; ≥ 2 executions byte-identical; covered set 75; lock boot-read prefix **69/200**; DC-4 and DC-5 computed |
| Canonical write surface | **Exactly two paths**, both declared outputs of `generation_order[6]`: `.ai/core/MANIFEST.lock` and `.ai/project/BINDING.md`. Everything else in every read-only partition is refused exactly as before; four tests hold the boundary, one asserting the default is still refused |
| **Canonical emission** | **NOT PERFORMED.** The command was refused by the host permission layer. **No engineering condition blocks it** |
| Consequence | `core/MANIFEST.lock` does not exist; `BINDING.core_digest_pin` is `PENDING-STAGE-6`; **boot step B2a cannot execute**, so core integrity cannot be *proven* |

**To clear B1**, one execution of:

```
PYTHONPATH=src python -m aief_stage6 --authorize \
  "human-owner" "2026-08-11" \
  "If Stage 6 can be executed without changing verified CAD: execute it autonomously."
```

It writes those two paths and nothing else, after every check above has passed and the octets
have been produced identically twice.

---

## 8 · GitHub

**Not pushed. 30 commits ahead of `origin/main`.** The standing push date **2026-09-01** is
unchanged and was not approached. Everything required for the eventual push is prepared: the tree
is consistent, every check computes green, and the line-ending policy now survives a checkout so
a fresh clone reproduces this state byte for byte.

**`C-4` (LICENSE placeholder) remains a blocker to any public or external release** and is
untouched — it is an owner decision, not an engineering one.

---

## 9 · What a reader should not conclude

This audit made the repository greener than it has ever been: every standing check exits 0 and
799 tests pass. **That is not the same as ready.** Nothing physical has been built or measured;
91 requirements await hardware; the framework's own integrity pin does not yet exist; and the
session that made these judgements has not been independently audited. The green is real and it
is narrow.
