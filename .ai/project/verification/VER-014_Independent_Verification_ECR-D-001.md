# VER-014 — Independent Verification of ECR-D-001 Disposition A

> **Instance artifact.** Partition `project`. Owner `qa-engineer`.
> Four cold-context rounds against `.ai/project/ecr/ECR-D-001_Alignment_Pin_Interface_Two_Geometries.md`.
> Filed at **`VER-014`**. `VER-008` is **reserved by `T-003`** for the SOD-1 cold audit of
> session `S-2026-08-08-10` (`T-003` deliverable and write scope); this report was first filed
> there in error — `VER-014` R3-F5, the same identifier-collision defect this report records at
> R10(c) for the approvals, committed by the report itself.

```yaml
verification_id: VER-014
subject:         ECR-D-001 disposition A, and its implementation in spec/01_SEWCP-200_Cooling_Plate.md
verifier_role:   qa-engineer            # cold context, no access to the implementer's conclusions
author_role:     software.software-engineer
law:             LAW-05 - verifier authored none of the work under audit
round_1:         FAIL
round_2:         FAIL
round_3:         FAIL
round_4:         FAIL
label_scheme:    findings are prefixed by round - R1-F*, R3-F*, R4-M* - because
                 round-1 CRITERIA were labelled V1..V10 and round-3 FINDINGS were
                 also labelled V1..V13, so a bare `V2` resolved to two different
                 things. VER-014 R3 records that collision.
status:          ECR-D-001 NOT CLOSED
session:         S-2026-08-09-14
```

---

## 0 · Why this file exists, and the defect that produced it

The finding set was cited by name in **five** artifacts — `ECR-D-001`, `ECR-D-007`, `APR-017`,
`FROZEN.md` and `OPEN_ITEMS_REGISTER.md` — as the authority for findings F1…F15, **while no
such report existed anywhere in the repository.** Round 2 recorded that as a blocker in its own
right (`R10`): `GATES.md` C6 requires that *a verification report exists*, and a finding set
cited but not filed is unauditable. Three findings (F6, F8, F12) were reachable from no
artifact at all.

The report is filed here. The citations were then found still dangling — they named
`VER-ECR-D-001`, an identifier no artifact carried, so `VER-014` R3-F4 recorded the
cited-but-unfiled defect as still present under a different name. Every citation is now
rewritten to `VER-014` and resolves. Both rounds are recorded, including the
round-1 findings that round 2 then found unrepaired — this file is not a summary of what
survived.

## 1 · Scope

| In scope | Out of scope |
|---|---|
| `spec/01` as changed; `spec/06`, `spec/03`, `spec/02` as controls | Every other volume |
| `ECR-D-001`, `APR-016`, `APR-017`, `ECR-D-007` | ECR-D-002…004; the geometry decision itself |
| `FROZEN.md`, `STATE.md`, `OPEN_ITEMS*`, `GATES.md` | CAD, Stage 6, the ledger, execution architecture |

## 2 · Round 1 — FAIL

Dispositions: V1 PASS, V2 PASS, V3 **FAIL**, V4 PASS, V5 PASS, V6 PASS, V7 **FAIL**,
V8 (drift), V9 PASS, V10 **FAIL**.

| ID | Finding | Rating | Blocked closure |
|---|---|---|---|
| F1 | `spec/01` §8 surface-finish table retained `\| Dowel bores \| … \| Press-fit dimensional integrity \|` — the superseded geometry, inside a manufacturing table, contradicting §6 step 13 | MAJOR | **yes** |
| F2 | `ECR-D-001` asserted *"the word dowel does not appear in spec/01"* — **false**; produced by a case-sensitive `grep -c "dowel"` against text reading `Dowel` | MAJOR | **yes** |
| F3 | §3.1 keep-out table has no kinematic-locator row; the Ø12.000 counterbore's inner edge at Ø260 BC sits 1.00 mm inside the declared Ø250 channel annulus | MAJOR | **yes** |
| F4 | The M4 leaves 3.35 mm of wall to the channel against the 3.5 mm demanded of the M5/M6 analogues; the constraint was recorded only in the ECR, not the specification | MAJOR | **yes** |
| F5 | The ECR's interference check cited *"a plate of 26.00 mm overall (`CP-D01`)"*. `CP-D01` is the **outside diameter**; thickness is `CP-D02` = 20.000; 26.00 appears nowhere. The only check performed on the added feature overstated available material by 30 % | MAJOR | no |
| F6 | `GATES.md` C1 requires the approval bound **to the ECR**; both approvals bind to the **artifact** per the `APR-001` precedent. Binding judged defensible; the wording conflict is unreconciled | MAJOR | blocks C1 |
| F7 | `framework.manifest.json` does not reproduce; *"29 of 29 verify"* false in `FROZEN.md` and `STATE.md` | MAJOR | pre-existing; blocks C5 |
| F8 | `AP-D08` specifies a Ø8.0 head counterbore in a Ø6.000 boss — cannot exist | MAJOR | no |
| F9 | 1.00 mm (0.95 mm min) annular wall at Ø306 BC carrying a Ø12.000 k6 interference flange with 50 µm anodize, unassessed by any volume | MAJOR | no |
| F10 | The ECR claimed `HP-D09`–`HP-D11` specify a 3.00 mm slot depth. They specify none | MAJOR | no |
| F11 | `residual: none` — three residuals exist | MINOR | no |
| F12 | M4 engagement 4.50–6.70 mm; the FMEA was not extended to the six new threads | MINOR | no |
| F13 | Two executed edits absent from the §6.1a disclosure table | MINOR | no |
| F14 | Section-number citations wrong throughout | MINOR | no |
| F15 | Freeze-registry bookkeeping: orphaned table row, authority chain stale | MINOR | no |

## 3 · Human disposition between rounds

Option **B** (human-owner, `S-2026-08-09-14`): repair the clerical defects; **split** F3, F4
and F9 into a separate ECR for Design Authority disposition. Recorded at `APR-017`.
`ECR-D-007` was filed accordingly.

## 4 · Round 2 — FAIL

Dispositions: R1 PASS, R2 PASS, R3 **FAIL**, R4 PASS, R5 PASS, R6 PASS, R7 PASS, R8 **FAIL**,
R9 PASS, R10 **blockers**.

**What round 2 confirmed by independent re-derivation.** F1 fixed (`grep -ci dowel` → 0 over
the whole file). F2 corrected candidly rather than deleted. F5 withdrawn **and not replaced**
by another unsupported figure. F3/F4 genuinely split: every figure in `ECR-D-007` recomputed
from the frozen volumes and **not one failed to reproduce** — r = 124.00, r = 128.35, 3.35 mm,
1.00/0.95 mm, 0.35 mm worst-case clearance. `spec/06`, `spec/03`, `spec/02` byte-identical
across `HEAD~1`, `HEAD` and the working tree. All four approval-hash links reproduce. The
freeze registry now publishes the **measured** 28 of 29, and both retained prior aggregates
reproduce from their declared memberships.

**Round-2 blockers.**

| ID | Finding | Rating |
|---|---|---|
| R3/F11 | `residual: none` **still in the YAML header** while §7 of the same file reads *"Not none."* The prose was rewritten; the machine-read field was not. The artifact contradicted itself | MAJOR |
| R8(a) | `ECR-D-001`'s `approval:` field pointed at `APR-016`, which its own successor declares **void under LAW-10**. An assessor following the ECR's pointer lands on a failing hash | MAJOR |
| R8(b) | `ECR-D-001` §7 stated the material conflict *"is raised separately"*. **No such ECR existed.** A status claim published without the fact behind it — the F2 failure class, repeated | MAJOR |
| R10(a) | `CP-D09a`/`CP-D10a` carry `M4 × 0.7, **8.0 deep**`. The approved option text says *"M4 tapped hole"* with no depth; `SEWCP-700` states **no plate-side tap depth**. An implementing agent set an engineering value, froze it into a registered artifact, and `APR-017` then certified *"No engineering value was set by an implementing agent"* | MAJOR |
| R10(b) | `VER-014` cited in five artifacts, filed nowhere | MAJOR |
| R10(c) | `APR-014` identifier collision: a prior session had already reserved it for the manifest re-registration | MAJOR |

## 5 · Repairs applied after round 2

| Finding | Repair | Requires authority |
|---|---|---|
| R3/F11 | `residual:` field corrected to `three - see §7` | no |
| R8(a) | `approval:` → `APR-018` (terminal); `approval_chain:` records `APR-016 → APR-017 → APR-018`. **Liveness is no longer asserted** — the field says to determine it by recomputing the terminal approval's `subject_hash`. `VER-014` R3-F1: the first two repairs each named the approval that the *next* edit voided, and each labelled it `LIVE` | no |
| R8(b) | **`ECR-D-008`** filed (316L vs Ti-6Al-4V) and **`ECR-D-009`** filed (`AP-D08` head seat). Both registered; both block `C7` | no |
| R10(b) | **this file** | no |
| R10(c) | `APR-014`/`APR-015` renumbered to **`APR-016`/`APR-017`** | no |
| R10(a) | `APR-017`'s false certification corrected in place | no |
| R10(a) | The 8.0 mm depth **struck** from `spec/01` under `APR-018` (Option A, human-owner). `CP-D09a`/`CP-D10a` now read `depth TBD — ECR-D-007`; the determination is `ECR-D-007` requested action 5 | **decided** |

## 5a · Round 3 — FAIL

Dispositions: T1 **FAIL**, T2 **FAIL**, T3 PASS, T4 PASS, T5 PASS, T6 PASS, T7 PASS,
T8 **FAIL**, T9 NO.

| ID | Finding | Rating | Blocked |
|---|---|---|---|
| R3-F1 | `ECR-D-001`'s `approval:` field named `APR-017`, voided by `APR-018`, and labelled it `# LIVE`. **Round 2's R8(a) relocated, not removed** — the repair pointed the field at the next approval to be voided | MAJOR | yes |
| R3-F2 | §6.1 executed-changes table still recorded the 8.0 mm tap depth as an executed change after `APR-018` struck it | MAJOR | yes |
| R3-F3 | §6.3 still handed SEWCP-200 CAD the struck value — the exact number `APR-018` was issued to remove | MAJOR | yes |
| R3-F4 | This report claimed *"the citations resolve"*; six artifacts cited `VER-ECR-D-001`, an identifier no artifact carried | MAJOR | no |
| R3-F5 | This report occupied `VER-008`, reserved by `T-003` — **the identifier-collision defect it records at R10(c), committed by itself** | MAJOR | no |
| R3-F6 | §5 certified `approval: → APR-017 (live)` two rows above recording the edit that voids APR-017 | MAJOR | no |
| R3-F8 | §7 of `ECR-D-001` announced two adjacent defects and described one | MINOR | no |
| R3-F9/10/11/12 | `STATE.md` blockers omitted ECR-D-006…009; `FROZEN.md` authority chain stale; `APR-016` §-number citations; `a637ae18…` reproducible from no committed state | MINOR | no |

## 5b · Round 4 — FAIL

Dispositions: W1 PASS, W2 PASS, W3 **FAIL**, W4 PASS, W5 PASS, W6 PASS, W7 PASS,
W8 **FAIL**, W9 PASS, W10 NO.

Round 4 confirmed by independent re-derivation that the struck value is gone from every live
statement, the approval pointer is fixed and `APR-018` is terminal and live, the chain
reproduces at all four links, the repair commit changed no specification content, the registry
is honest at 28 of 29 with a reproducing aggregate, and the controls are byte-identical.

| ID | Finding | Rating | Blocked |
|---|---|---|---|
| R4-M1 | This report took **`VER-010`** — reserved by `T-005` (READY) and cited five times by `R-014` for an unrelated finding set. **The collision moved a fourth time**, and `R-014`'s citations went from dangling to resolving to the *wrong* artifact | MAJOR | yes |
| R4-M2 | `round_3: FAIL` was recorded with **no round-3 section**, while its findings were cited seven times under labels `V1…V8` that collide with §2's round-1 criteria labels `V1…V10` | MAJOR | yes |
| R4-M3 | The round-3 repair commit claimed `FROZEN.md`'s authority chain was corrected. **It was not** — the substitution never matched and the script asserted nothing, so it reported success. Fourth consecutive round with a false completeness claim, inside the commit titled *"stop relocating defects instead of removing them"* | MAJOR | no |
| R4-M4 | This report said *"six artifacts"* and listed five; *"Two cold-context rounds"* while recording three | MINOR | no |
| R4-M5 | `ECR-D-001` §6.1a publishes `git diff --name-only spec/` with an output that command does not produce at HEAD (the true form is `git diff --name-only 70ce9e6 HEAD -- spec/`) | MINOR | no |

**Repairs after round 4:** renumbered to `VER-014`, the first free identifier — `VER-008`
(`T-003`), `VER-010` (`T-005`, `R-014`), `VER-011` (`T-006`), `VER-012`/`VER-013` (`R-014`,
`EXECUTION_ARCHITECTURE.md`) are all taken. Round-3 and round-4 sections added with
round-prefixed labels. `FROZEN.md` authority chain corrected **with an assertion on the
substitution**, which is what its absence caused.

## 6 · Verdict

**ECR-D-001 is NOT CLOSED after four rounds.** `LC-M04-EXIT` C6 is not satisfied for it.

The engineering survived **all four** rounds intact and was re-derived independently each time. Every
blocker in both rounds was **record integrity**: a false completeness claim, a fabricated
dimension reference, a falsified field left standing, a pointer to a void approval, a claimed
filing that did not exist, an unauthorised value, and a missing report. The implementing agent
wrote a false claim into a record in three consecutive rounds.

That pattern is recorded here as the finding of this verification, not as an aside. A repair
process whose engineering is sound and whose records are not is a process whose gate evidence
cannot be trusted, and `C6` exists to catch exactly that.

## 7 · Open against this subject

`ECR-D-007` (geometric consequences), `ECR-D-008` (material), `ECR-D-009` (screw seat) — all
OPEN, all blocking `C7`. F6 (the `GATES.md` C1 binding wording) needs a ruling. F7/ECR-D-006
blocks `C5` independently. F12 (FMEA not extended to the six M4 threads) is open and
unassigned. The tap depth is `ECR-D-007` requested action 5.
