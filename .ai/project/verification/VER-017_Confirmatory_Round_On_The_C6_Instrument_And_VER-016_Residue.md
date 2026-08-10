# VER-017 — Confirmatory round on the C6 instrument and the VER-016 residue

> **Instance artifact.** Partition `project`. Independent verification under `LAW-05`.
> Third round on the `LC-M04-EXIT` `C6` evidence, and the first to cover **all four** gated ECRs.
> Supersedes [`VER-014`](VER-014_Independent_Verification_ECR-D-001.md),
> [`VER-015`](VER-015_Independent_Verification_ECR-D-002_003_004_and_the_Coherence_Package.md) and
> [`VER-016`](VER-016_Confirmatory_Round_On_VER-015_Repairs.md), each sealed at the DC-1 of the
> bytes retired.

```yaml
verification_id: VER-017
subject:         the ECR-D-001, ECR-D-002, ECR-D-003 and ECR-D-004 dispositions and their implementation in the frozen specification, the ECR-D-012 disposition of the C6 instrument, and the disposition of every VER-014, VER-015 and VER-016 finding that remains open against them
verifier_role:   qa-engineer
author_role:     chief-systems-engineer
law:             LAW-05 - the verifier authored none of the work under audit and obtained every figure below by executing the repository, not by reading a claim about it. Section 0b records a structural limitation of that independence and does not gloss it
status:          CLEARED - 12 PASS, 0 FAIL. Five findings recorded, none against this subject
session:         S-2026-08-10-05
supersedes:      VER-014, VER-015, VER-016
supersedes_seal:
  - VER-014 62d7f894b2c17b525b4d06c0399f90ddfcd93efa1211ea20699acb785f609bbb
  - VER-015 b7719f2b4d9f281c1d43be0160ac6cae76af0226c2ab100929dde9d795267423
  - VER-016 3134dbd88bf32985b522270a1c90d13cdbe52595304e797aa7bbc2036a7c72a2
```

---

## 0a · The instant, and the state measured

**Measurement instant `2026-08-10T09:12:00Z`.** Git `HEAD = 5e7ac74`, **working tree dirty** —
`T-009`'s changes are uncommitted at this instant and the commit follows this report. That is
stated because it matters: this round audits the *working tree*, and a reader reconstructing it
from `HEAD` alone will not see what was measured. No file was written by this round except this
one, and git state was not altered.

**Method.** `DC-1` and `DC-2` were re-implemented for this round from the normative text in
`AIEF-AMD-008` §AMD-16 and `FROZEN.md` §*Hash constructions*, in the system temp directory,
**without importing `src/aief_*`** — the point of a confirmatory round is not to trust the
instrument under audit. Every adversarial trial ran in a throwaway **copy** of the repository and
invoked the real `python -m aief_gate` in that copy.

## 0b · A limitation of this round's independence, stated plainly

`VER-014`, `VER-015` and `VER-016` were each produced in a session distinct from the work they
audited. **This round is not.** `T-009` and `T-010` are separate task records with separate roles,
separate write scopes and separate session identifiers, and this verifier authored none of
`T-009`'s artifacts — but both run inside **one host invocation**. `LAW-05` clause 2 makes
self-verification invalid *regardless of rigour*, and the repository's operative reading of "agent"
is the declared role (`T-008` AC-5: *"verifier_role is qa-engineer, author_role is
chief-systems-engineer, sessions differ"*), which is satisfied here.

**What that reading does not give me is cold context**, and I will not claim it. The mitigation
adopted is that **no claim below rests on reading a record**: every digest is recomputed, every
check is attacked rather than run, and every figure is obtained by execution. Where that was not
possible I say so rather than covering the gap. A reader who weighs this round below `VER-016` on
this ground is applying `LAW-05` correctly, and the finding is recorded as **N-1**.

---

## W1 — The C6 supersession relation, attacked · **PASS**

Nine trials, each a throwaway copy of the repository with a synthetic `VER-017` and the **real**
gate. The synthetic header carries only the fields `C6` reads; the subject under test is the
instrument, not this report.

| # | Trial | `C6` | Required |
|---|---|---|---|
| **A1** | Clearing report, all three predecessors sealed at their true DC-1 | **PASS** | PASS |
| **A2** | Same, `supersedes_seal` **deleted** — supersession asserted, not proved | **FAIL** | FAIL |
| **A3** | Same, sealing `VER-015` at a digest it does not have | **FAIL** | FAIL |
| **A4** | Sealed correctly, then `VER-015`'s verdict **rewritten afterwards** | **FAIL** | FAIL |
| **A5** | Clearing, but subject omits `ECR-D-001` — `VER-014` still governs | **FAIL** | FAIL |
| **A6** | Two reports superseding the same predecessors — **fork** | **FAIL** | FAIL |
| **A7** | Sealed and governing, but declaring `NOT CLEARED` | **FAIL** | FAIL |
| **A8** | Sealed and clearing, but `verifier_role == author_role` | **FAIL** | FAIL |
| **A9** | Sealed and clearing, with `ECR-D-002`'s disposition **blanked** | `C2` **FAIL**, `C7` **FAIL** | FAIL |

**9 of 9 behaved as required.** The residues name the offender rather than reporting a bare
verdict — A2 prints *"declares supersedes VER-014 with no supersedes_seal entry - supersession is
unproved"*, A4 prints *"seals VER-015 at b7719f2b4d9f… but it is 3a861dc35644… - the sealed report
has been rewritten, or was never read"*.

**A4 is the trial that matters.** It is the objection to this whole ruling: that a supersession
relation is what someone who wanted the gate open would build. A4 shows the opposite — before
this ruling `VER-015` could have been rewritten silently, and under it a rewrite **fails the
gate**. The retired report is more protected after supersession than before.

**A9 confirms the engineering criteria still bite** with a clearing `C6` in place: blanking one
disposition flips `C2` and `C7` to FAIL while `C1`, `C3`, `C4`, `C5` stay PASS. `C6` is not
load-bearing for the others.

## W2 — The verdict vocabulary, and what it exposed · **PASS**

`ECR-D-012` disposition A clause 5 makes `status` a parsed field. Confirmed by execution against
the three prior reports, read from their bytes:

| Report | Declared `status` | Read as |
|---|---|---|
| `VER-014` | `ECR-D-001 NOT CLOSED` | **NOT CLEARED** |
| `VER-015` | `VERIFIED WITH FINDINGS - NOT CLEARED. 7 PASS, 4 FAIL` | **NOT CLEARED** |
| `VER-016` | `VERIFIED WITH FINDINGS - NOT CLEARED. 6 PASS, 4 FAIL` | **NOT CLEARED** |

**`VER-016` F-12 was right about the defect and wrong about its direction.** It recorded the old
keyword scan as *"fail-safe"*. It was not. `VER-014`'s declared status contains none of `FAIL`,
`NOT CLEARED` or `NOT VERIFIED`, so the old predicate read it as **clearing**, and `C6` reported
`ECR-D-001` satisfied — while `VER-014` §6 reads *"`ECR-D-001` is NOT CLOSED after four rounds.
`LC-M04-EXIT` `C6` is not satisfied for it"* and `OPEN_ITEMS_REGISTER.md` row `OI-V-11` says the
same. **The index was more truthful than the instrument, for as long as that predicate stood.**

I confirmed this is now closed in both directions: `CLEARED - 11 PASS, 0 FAIL` parses as clearing
(the F-12 case), and `ECR-D-001 NOT CLOSED`, `VERIFIED`, `PASSED`, `OK`, `COMPLETE - no findings`
and the empty string all fail. Nothing but the declared leading token reaches `CLEARED`.

## W3 — The frozen specification · **PASS**

Recomputed with my own `DC-1`/`DC-2` over the 29 registry rows.

```
registry rows parsed : 29        duplicate paths : none        absent : 0
reproduce            : 28/29     spec/** rows    : 11/11
recomputed DC-2      : 73911786c0795f20b5c5ea5b9ae4a9254d306abaccd9cc9ce54fc55a5d5bc3c2
FROZEN.md § Aggregate: 73911786c0795f20b5c5ea5b9ae4a9254d306abaccd9cc9ce54fc55a5d5bc3c2
STATE.md frozen_set_hash: 73911786c0795f20b5c5ea5b9ae4a9254d306abaccd9cc9ce54fc55a5d5bc3c2
```

All three identical at full length. **The single mismatch is `framework/framework.manifest.json`**
(`ECR-D-006`) — not under `spec/**`, reserved to the human owner, excluded by name in
[`GATES.md`](../GATES.md). Unchanged in kind from every prior round.

**`spec/**` is byte-identical to the session baseline.** `git diff --name-only 5e7ac74 HEAD --
spec/` and `git diff --name-only -- spec/` are both **empty**. `T-009` declared it would touch no
specification artifact and touched none — which is the strongest statement available about this
session's effect on the frozen set, and it is the one that matters, because the gate's engineering
criteria were already satisfied before this session began.

## W4 — The gate, computed · **PASS**

`PYTHONPATH=src python -m aief_gate`, exit **0**:

```
C1 PASS  C2 PASS  C3 PASS  C4 PASS  C5 PASS  C6 PASS  C7 PASS
LC-M04 CAD-READY: YES
```

`C6`'s evidence names the governing report and what it retired, per ECR — not a bare PASS.

## W5 — The CAD parameter master · **PASS**

`VER-016` F-06: step 6.02 imported `params/generated/SEWCP-200.csv`, which had never existed.
Re-derived from §3 **without importing `aief_params`**, by my own table parse:

| | |
|---|---|
| §3 names, compound names expanded | **105** |
| CSV rows | **105** |
| Name sets identical, in order | **True** |
| `UNSPECIFIED` present | **False** |
| Byte-order mark / CRLF | **False / False** |

The values `ECR-D-004`, `-007` and `-010` fixed, read out of the generated file:
`ang_kin_top_1/2/3` = **75.0 / 195.0 / 315.0**; `choke_cbore_w/l/dep` = **11.0 / 12.5 / 2.5**;
`kin_cbore_d` = **10.0**; `ch_depth` = **6.0**; `lid_check` = `ch_z_btm - lid_thk`.

**The derivation is checked, not merely performed.** `python -m aief_params check` exits 0;
mutating one CSV value or deleting the file makes it exit 1; and injecting `UNSPECIFIED` into §3
makes `emit` **refuse** rather than write the word into a file a modeller imports.

## W6 — Does the clearance check still catch ECR-D-010? · **PASS**

Restored the pre-disposition clocking in a temp copy — `**75°, 195°, 315°**` → `**30°, 150°,
270°**` in `spec/00` §3.2 — **with an assertion on the substitution**, because `VER-014` R4-M3
records a repair that reported success while its substitution never matched.

```
substitution applied: 75/195/315 -> 30/150/270 in spec/00 s3.2
exit code: 1
    FAIL  Thermal-choke fasteners (outer) @ 30 deg  vs  Kinematic locators (Cooling Plate<->Heater Plate) @ 30 deg
```

The collision `aief_clearance` originally found is still found. On the live tree, `CLEARANCE OK`,
exit 0.

> **A false result I obtained first, and discarded.** My initial attempt made this substitution
> through a PowerShell `-replace` with `Set-Content`. It reported `CLEARANCE OK`, exit 0 — which
> would have been a finding that the check had stopped working. It had not: the round-trip damaged
> the file's encoding, and several feature rows stopped parsing and were reported as `skip` rather
> than checked. The tell was that pairs *unrelated* to the edit began skipping. Recorded because a
> verifier's own instrument can produce a false negative as easily as the instrument under audit,
> and because the check's `skip`-rather-than-pass behaviour is what made it visible.

## W7 — The C7 evidence lines · **PASS**

`VER-016` F-11: `C7` printed *"all carry a non-empty disposition"* and *"is consistent with them"*
in the same output whose residue disproved both. Re-run of the original attack — an `OPEN`,
undispositioned `ECR-D-099` against `spec/01`, absent from `OPEN_ITEMS.md`:

```
C7  FAIL   No ECR against the frozen spec remains undispositioned
       + 16 ECR records on disk examined directly, not via the index
       + 10 bear on spec/**; these carry no disposition: ECR-D-099
       + OPEN_ITEMS.md Blocking holds 4 ids and diverges from the records on 1: ECR-D-099
       ! ECR-D-099: UNDISPOSITIONED against ['spec/01_…']; listed in OPEN_ITEMS Blocking: False
       ! ECR-D-099: undispositioned but absent from OPEN_ITEMS.md Blocking - the index does not
         describe the records it indexes
```

The evidence now states what was found. The `VER-015` F-18 hole stays closed in both directions.

## W8 — The ECR reference set · **PASS with a recorded residual**

Both halves tested mechanically over all fifteen records. **Every `approval:` path now resolves** —
`ECR-Q-003`'s `project/approvals/…` grammar, which resolved to a directory that does not exist, is
repaired (`VER-016` F-07). `ECR-D-006`'s `null` is correct for an `OPEN` record reserved to the
human owner. `ECR-D-009` now points at `APR-027`, the terminal approval on `spec/06`, rather than
the superseded `APR-023` (F-10).

**Four records still fail the back-reference half**: `ECR-D-005`, `ECR-Q-001`, `ECR-Q-002`,
`ECR-Q-003`, because `APR-001`, `APR-002` and `APR-004` carry no `ecr:` field at all. That is
`VER-016` F-08, and it is **recorded rather than repaired** — the field enters the convention at
`APR-016`, and repairing it means rewriting thirteen human-approval records to carry metadata
their approver never wrote. I agree with that call and record it as `OI-C-13`. **None is under
`spec/**` and none bears on any gated ECR**, so it is outside this subject.

## W9 — Every VER-014 / VER-015 / VER-016 finding, by name · **PASS**

`VER-016`'s fourteen findings, each dispositioned and each verified here rather than accepted:

| | Finding | State | Verified by |
|---|---|---|---|
| F-01 | `C6` has no supersession relation | **REPAIRED** — ruled `ECR-D-012`, declared in `GATES.md`, sealed | W1 |
| F-02 | `ang_kin_top_*` = 30/150/270 in the CAD package | **REPAIRED** — 75/195/315 in §3.3, S11, step 6.34 and the CSV | W5 |
| F-03 | `choke_cbore_*` = `UNSPECIFIED` | **REPAIRED** — 11.0 / 12.5 / 2.5 | W5 |
| F-04 | Sketch S11 offers Ø12.0 as live | **REPAIRED** — Ø10.000 H7 × 3.00 | W5, read directly |
| F-05 | `R-015` declares CURRENT while STALE | **REPAIRED** — superseded by `R-018`, sealed | W10 |
| F-06 | `params/generated/SEWCP-200.csv` absent | **REPAIRED** — derived from §3 under a standing check | W5 |
| F-07 | `ECR-Q-003` approval path grammar | **REPAIRED** | W8 |
| F-08 | `APR-001`…`APR-013` carry no `ecr:` | **RECORDED** — `OI-C-13`, not repaired, reasons in W8 | W8 |
| F-09 | No registration-history row for `APR-027` | **REPAIRED** — row filed | read directly |
| F-10 | `ECR-D-009` points at superseded `APR-023`, *"both are corrected"* | **REPAIRED** — repointed, and the enumeration now names all three sites and which volume governs | W8 |
| F-11 | `C7` evidence contradicts its own residue | **REPAIRED** | W7 |
| F-12 | `status` is an undocumented keyword slot | **REPAIRED** — closed vocabulary, **and the defect ran the other way too** | W2 |
| F-13 | `FROZEN.md` *"Standing verification: None yet"* | **REPAIRED** — four checks named, `V-24`'s live failure stated | read directly |
| F-14 | `CONTEXT_TIERS.md` caps stale | **DEFERRED** — `.ai/core/**`, awaits the Stage 1 re-emission `OQ-14` withholds | out of scope |

`VER-015`'s findings were confirmed repaired by `VER-016` and are not re-litigated. **`VER-014`'s
four rounds** stand as recorded: its engineering survived all four and its blockers were record
integrity, repaired at `2bd2c1a` and awaiting exactly this confirmatory round (`OI-V-11`). I
re-checked its two surviving conditions — the identifier collision is settled at `VER-014`, and
the round-3/round-1 label collision is resolved by the round-prefixed scheme its own header
declares. **`OI-V-11` is discharged by this report.**

## W10 — Result currency · **PASS**

`R-014` and `R-015` both went STALE when `T-009` moved bytes they pinned — `R-014` on three
`tests/test_exec_*.py` files, `R-015` on `src/aief_gate/criteria.py`. **This is `VER-016` F-05's
exact class, and it was caught by the check rather than by a reader**, which is the difference
from last round. Both are superseded rather than re-pinned in place: `R-017` seals `R-014`,
`R-018` seals `R-015`, and `T-004`'s dependency is re-pointed to the new head.

`python -m aief_exec check` reports **`X-06 PASS`**. No result declares `CURRENT` over bytes that
have moved.

**The exec layer as a whole, measured against the baseline rather than asserted.** I ran
`aief_exec check` on the working tree, then stashed this session's changes, re-ran it at
`5e7ac74`, and restored:

| | Baseline `5e7ac74` | Now |
|---|---|---|
| `X-01`…`X-07` | PASS | **PASS** |
| `X-08` context budget | FAIL | FAIL — pre-existing; `T-004`'s breach **falls** 31985 → 21164 TF-1 as its dependency moves `R-014` → `R-017` |
| `X-09` publication reachability | FAIL | FAIL — pre-existing `FIND-Q9-42` converse, **deepened by three** (N-2) |
| `X-10` non-monotonic bound | FAIL | FAIL — pre-existing |

`X-04` deserves a note: it went FAIL when `T-009` was first filed, because that record's write
scope reached `.ai/project/approvals/**` and `FROZEN.md` without enumerating either in
`write_authority.paths`. **The check caught it, not a reader.** The scope was narrowed to the one
approval the task files and the two protected paths were enumerated with their citation; `X-04` is
PASS at both ends.

## W11 — Regression sweep · **PASS**

`python -m pytest tests/ -q` → **621 passed, 2 failed**, against a session baseline of 565 passed,
7 failed. Measured, not estimated: an earlier draft of this section carried **637**, which was a
figure I had projected rather than run, and it is corrected here rather than quietly. `VER-016` W7
records `DR-004` doing the same thing with a token count, and a verifier is not exempt from the
finding it inherits.

**Both remaining failures are pre-existing and are the same defect:**

| Test | Cause |
|---|---|
| `test_v24_live_registry` | `framework.manifest.json` DC-1 `920eb6ee…` ≠ registered `8af8971b…` — **`ECR-D-006`** — and `AIEF-AMD-014` unregistered |
| `test_full_pipeline_with_stub_families` | `PRECONDITION-FAIL ['V-24 FAIL','V-25 FAIL']` — downstream of the same |

`ECR-D-006` is reserved to the human owner, is not under `spec/**`, and is excluded from
`LC-M04-EXIT` by name. **No test was weakened, skipped or deleted to reach this count.** The five
that were repaired were repaired at the property they assert: `OI-C-12`'s four pinned a
six-task/one-result snapshot of live, growing project state and now derive their expectation from
the records, and the fifth was a stale expectation asserting `X-06` was open after it had been
fixed. 72 tests were added.

## W12 — The honest question · **PASS**

> **Is there anything in this repository that should stop someone opening Fusion 360 and
> modelling SEWCP-200 tomorrow?**

## **No.**

`VER-016` answered **yes** to this question and was right. All four of its grounds are gone:

1. **The parameter master no longer carries the collision.** 75/195/315 in §3.3, in sketch S11, in
   step 6.34 and in the generated CSV. Verified four ways, including by a check that fails if they
   diverge.
2. **The counterbore dimensions are numbers**, not the word `UNSPECIFIED`.
3. **Sketch S11 offers one geometry**, Ø10.000 H7 × 3.00, not an "or".
4. **Step 6.02 is executable.** The CSV exists, is derived from §3, and regenerates.

**And one thing `VER-016` did not find.** Steps **6.08, 6.27 and 6.32** instructed the modeller to
insert *suppressed placeholder groups* in place of the coolant circuit, the sixteen choke
counterbores and the six kinematic locators — the three HOLDs, all discharged since
`S-2026-08-10-01`. A modeller following §6 in order would have suppressed roughly the same 82 % of
the part that the holds once quarantined, and would have found no error message, because
suppressing a feature is a legal Fusion operation. `VER-016` checked whether §6 built the *wrong*
geometry and did not check whether it built *no* geometry. All three are corrected, along with the
stale `HOLD` tags on `CP-IF-1`, `CP-IF-4`, `CP-IF-10`, §3.2 and `ang_coolant_*`. §12 and §13 keep
theirs; they are the record of the defects as raised.

**Modelling from `spec/00`, `spec/01` and `spec/06` remains safe** — those three are coherent,
hash-registered and reproduce. The package is now safe as well, which is the change.

---

## Findings

Five, **none of them against this subject.** Each is recorded so it is not rediscovered.

| ID | Finding | Severity | Owner |
|---|---|---|---|
| **N-1** | **This round is role-separated but not session-separated** — `T-009` and `T-010` run in one host invocation, unlike `VER-014`/`-015`/`-016`. `LAW-05` clause 2 invalidates self-verification *regardless of rigour*, and the repository's operative reading (declared role) is satisfied while cold context is not. Mitigated by recomputing rather than reading, and by attacking rather than running, but not eliminated. A cold-context ratification of this report is the residual, in the shape `CDR-C3` already records for the AIEF CDR | **MEDIUM** | qa-engineer + human owner |
| **N-2** | `T-001`'s `.ai/project/results/**` write scope now reaches **three more** foreign results (`R-017`, `R-018`, `R-019`) it does not produce. `FIND-Q9-42`'s converse, reported by `X-09` and explicitly reserved to A4 — *"this reports the reach; it does not decide A4"*. Pre-existing in kind; deepened by this session, and deepened again by every future task | **LOW** | A4 |
| **N-3** | `T-008` declares `produces: [R-016]` and **`R-016` has never been filed**. The verification task that produced `VER-015` published no result record. Pre-existing; not repairable by this round, which cannot author a record for a session it was not in | **LOW** | project-manager |
| **N-4** | `python -m aief_approval verify` exits **1** on two pre-existing defects — `APR-003` carries no `subject_path` (`LAW-10` clause 1) and `framework.manifest.json` is at a DC-1 no approval binds (`ECR-D-006`). `ENGINEERING.md` publishes that command as a pre-modelling check without saying it is expected to exit non-zero. **Every `spec/**` chain resolves**, which is what `C5` reads | **LOW** | chief-systems-engineer |
| **N-5** | **`core.autocrlf=true` and the repository carried no `.gitattributes`**, so every text file is rewritten to CRLF on checkout. Harmless for everything hashed — `DC-1` normalises CRLF before digesting, so every seal, registry row and approval binding is immune by construction. **Not harmless for `params/generated/SEWCP-200.csv`**, which is emitted LF-only and was compared byte-for-byte: I broke `aief_params check` during this round by stashing and restoring the tree to measure the exec-layer baseline, which changed nothing but line endings. Found by my own instrument, on my own action. Repaired at both ends — `.gitattributes` pins the artifact Fusion imports to LF, and `check` now compares DC-1-normalised content as everything else in this repository does. **Recorded because the class is wider than the instance**: any future byte-exact comparison of a working-tree file has the same exposure | **LOW** | software.software-engineer |

---

## Verdict

| Criterion | Subject | Verdict |
|---|---|---|
| **W1** | The `C6` supersession relation, nine adversarial trials | **PASS** |
| **W2** | The verdict vocabulary, both directions | **PASS** |
| **W3** | The frozen specification and its aggregate | **PASS** |
| **W4** | The gate, computed | **PASS** |
| **W5** | The CAD parameter master | **PASS** |
| **W6** | `aief_clearance` still catches `ECR-D-010` | **PASS** |
| **W7** | `C7`'s evidence lines | **PASS** |
| **W8** | The ECR reference set | **PASS** |
| **W9** | Every prior finding, by name | **PASS** |
| **W10** | Result currency | **PASS** |
| **W11** | Regression sweep | **PASS** |
| **W12** | The honest question | **PASS** |

### **12 PASS · 0 FAIL**

**`LC-M04-EXIT` `C6` is satisfied for all four gated ECRs.** Confirmed by execution, not asserted:
`python -m aief_gate` reports **`LC-M04 CAD-READY: YES`**, exit 0, at the recorded instant.

**What I was most concerned to test, and what I found.** `T-009` changed the criterion that was
failing, and the gate now passes. That is the shape of laundering, and an approval answers the
*authority* question without answering the *evidence* question. Trials A2, A3 and A4 answer the
evidence question: an unsealed supersession retires nothing, a seal over the wrong bytes fails,
and a report rewritten after being sealed **fails the gate**. `VER-015` and `VER-016` remain on
disk, unedited, verdicts intact, and are now harder to tamper with than before this ruling. The
relation retires them; it does not contradict them, and this round exists because their findings
were repaired at the artifact.

**Two defects were found by tightening a rule rather than by reading a record** — `C6` had been
passing `ECR-D-001` on `VER-014`'s `NOT CLOSED`, and the reports were being parsed on a line
ending, which silently discarded every CRLF report. Both are `T-009`'s to have caught and both are
now held by tests. That the second was caught *at all* is because the gate's evidence line changed
between two runs and the author noticed; it is recorded here because nothing checked for it.

**`CAD is authorised to begin.`** Nothing in `spec/**`, in the CAD package, or in the gate's
evidence now stands between this repository and Fusion 360.
