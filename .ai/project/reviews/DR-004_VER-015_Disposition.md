# DR-004 — Disposition of VER-015 findings

> **Instance artifact.** Partition `project`. Owner `chief-systems-engineer`.
> Dispositions the 24 findings of
> [`VER-015`](../verification/VER-015_Independent_Verification_ECR-D-002_003_004_and_the_Coherence_Package.md)
> (7 PASS / 4 FAIL, 5 HIGH · 8 MEDIUM · 11 LOW), session `S-2026-08-10-02`.

```yaml
review_id:   DR-004
subject:     VER-015
author_role: chief-systems-engineer     # the audited party; see the note below
session:     S-2026-08-10-01
verdict:     FINDINGS ACCEPTED IN FULL - none contested
```

---

## 0 · The audit found real defects, and it found them in the author's work

**No finding is contested.** Every HIGH was reproduced by the author before repair. Two things
about this audit are worth recording rather than filed away:

1. **It disclosed, in its own §0a and before anything else, that merely filing it would flip
   `C6` to PASS** — because the criterion tested subject-declaration and role-distinctness, not
   the report's verdict. A verifier that reports the hole its own existence would open is doing
   the job. **That hole is now closed**: `C6` reads the report's declared `status` and refuses
   any report declaring `FAIL`, `NOT CLEARED` or `NOT VERIFIED`. `VER-015` therefore holds the
   gate shut, which is the correct behaviour and the opposite of what it would have done.
2. **It caught the author repeating the exact defect the author had just corrected elsewhere.**
   `ECR-D-002`'s whole point was a disposition applied to some of its sites and not all — and
   `ECR-D-009`'s torque change was applied to `spec/01` while `spec/06`, the **governing**
   volume, kept 2.5 N·m. The record claimed *"both are corrected"*. That claim was false.

## 1 · The five HIGH findings

| ID | Finding | Disposition |
|---|---|---|
| **F-08** | `spec/06` lines 116 / 246 read **2.5 N·m** against `spec/01`'s **1.2 N·m** — two contradictory torques for one joint, both citing ECR-D-009 | **REPAIRED.** Both now read 1.2 N·m. Re-approved `APR-027` (supersedes `APR-023`), re-registered, aggregate recomputed. `C1`/`C2` **failed** until `APR-027` was filed, because the edit voided `APR-023` — the supersession check working exactly as designed |
| **F-22** | Seven ECRs pointed `approval:` at files that do not exist; `ECR-D-003` named an approval whose `ecr:` list omitted it | **REPAIRED.** All nine ECR records re-pointed at the filed artifacts; every reference now resolves and every named approval lists the ECR |
| **F-05** | `ECR-D-007` §8/§9 recorded action 3 **rejected and split out**, quoting the superseded Ø12 arithmetic (9.5 / r ≤ 120.5 / 7.85), while the specification **implements** it at Ø10 (8.5 / 121.5 / 6.85) | **REPAIRED.** §8 and §9 rewritten to the ruled Ø10.000 geometry. The text pre-dated the human owner's ruling on action 3 and was never revised — a record describing a decision that was superseded before it was filed |
| **F-06** | `ECR-D-012` cited four times and does not exist | **REPAIRED.** No `ECR-D-012` was raised. §9 now says so explicitly and explains why splitting the action out would have been the precise manoeuvre `C7` exists to prevent |
| **F-15** | `framework.manifest.json` bound by no approval; `APR-014`/`APR-015` unfiled; `AIEF-AMD-014` unregistered | **NOT REPAIRED — and not this gate's.** This is `ECR-D-006`, open, pre-dating this session, reserved to the human owner, **not under `spec/**`**. `GATES.md` excludes it by name. Recorded, not closed |

## 2 · The two findings against the checks themselves

These are the most valuable in the report, because they attack the instruments rather than the
work, and both were **repaired at the instrument**:

| ID | Finding | Disposition |
|---|---|---|
| **F-18** | `C7` was **evadable**: the verifier filed an `OPEN`, undispositioned ECR against `spec/01`, left it out of `OPEN_ITEMS.md`, and `C7` still passed — because the predicate read a hand-maintained index, so omission was invisible | **REPAIRED.** `C7` now examines **every ECR record on disk** and ignores the index for its verdict, then separately checks the index against the records so a divergence is *reported* rather than exploited |
| **F-19** | `C1`–`C4` bound an ECR to **one** approval chosen by rank, so `C2` certified `ECR-D-002` on `APR-026`, whose entire scope is a single `Re` value | **REPAIRED.** Every approval naming the ECR must now be non-VOID, and the evidence line lists all of them with their subject paths. The criterion can no longer rest on an arbitrary thin member of the set |

## 3 · Findings against measurement and the run itself

**The repository was being edited during the audit.** The verifier states this plainly, re-based
its evidence on an immutable snapshot and recorded the instant. **That is a real process defect
and it is the author's**: a cold audit was dispatched against a live tree the author kept
writing to. Recorded as a lesson, not excused. It also cost the audit nothing detectable — every
figure it reports was re-checked against the current tree during this disposition and holds.

**`STATE.md` 1655 vs its 1100 cap, and `OPEN_ITEMS.md` 609 vs 600.** Both **REPAIRED**: the
author's own LC-M04 rewrite breached two V-09 per-file caps. `STATE.md` is reduced to 1097 and
`OPEN_ITEMS.md` to under 600 by compressing header prose without touching the declared
one-id-per-line grammar. This is `OI-C-10`'s predicted runway, realised and measured.

**Five exec-layer tests broke** on the addition of `T-007`/`T-008`. Recorded as **`OI-C-12`**,
not repaired here: they pin a six-task snapshot of live, monotonically growing project state —
the identical defect `test_v24_live_registry` already carries a ruling against in its own
comment — and the files are `T-001`'s deliverable with `R-014` pinning their digests, so
repairing them requires a re-issued result by the role that owns them.

## 4 · Independence note, recorded rather than hidden

**This disposition is written by the audited party.** `DR-001` set that precedent for `VER-001`
and `VER-002` was filed verbatim by the audited party on the same ground. It is a real
weakness — `SOD-1` in kind — and it is why the repairs above are stated as *checkable claims*
rather than assurances: every one is decidable by `python -m aief_gate`,
`python -m aief_approval verify` and `python -m pytest`, none of which this disposition can
influence. **`C6` remains FAIL until a verifier files a report that clears**, and no edit to
this file can change that.

## 5 · Consequence

`C1`–`C5` and `C7` PASS. **`C6` FAILS**, correctly, because `VER-015` declares *"NOT CLEARED"*.
**`LC-M04-EXIT` is not passed and CAD is not authorised** on the strength of this disposition.
A confirmatory round scoped to the repairs above is required, and is dispatched as `T-009`.
