# VER-016 — Confirmatory round on the VER-015 repairs

> **Instance artifact.** Partition `project`. Independent verification under `LAW-05`.
> Confirmatory round on the repairs dispositioned in
> [`DR-004`](../reviews/DR-004_VER-015_Disposition.md) against
> [`VER-015`](VER-015_Independent_Verification_ECR-D-002_003_004_and_the_Coherence_Package.md).

```yaml
verification_id: VER-016
subject:         the repairs claimed in DR-004 against the VER-015 findings on the ECR-D-002, ECR-D-003 and ECR-D-004 dispositions and the LC-M04 specification coherence package, together with the C1-C7 instrument changes made to close VER-015 F-18, F-19 and the disclosed C6 hole
verifier_role:   qa-engineer
author_role:     chief-systems-engineer
law:             LAW-05 - the verifier authored none of the work under audit and obtained every figure below by executing the repository, not by reading a claim about it
status:          VERIFIED WITH FINDINGS - NOT CLEARED. 6 PASS, 4 FAIL
session:         S-2026-08-10-03
```

---

## 0 · Scope, method and the instant

**This round is not a re-run of `VER-015`.** Its arithmetic findings reproduced and are not in
question here. This round decides one thing: **are the claimed repairs real, and does anything
remain that should stop `LC-M04-EXIT`?**

**Measurement instant: `2026-08-10T05:39:53Z`**, repository at `HEAD = 7a36ff2`. The tree was
quiescent throughout; the instant is recorded regardless, per `AMD-42` — a property of a tree at
an instant is not a constant. Git state was not altered by this round and no file outside this
report was written.

**Method.** Every digest below was recomputed by an implementation of `DC-1` and `DC-2` written
for this round from the normative text in `AIEF-AMD-008` §AMD-16 and `FROZEN.md` §*Hash
constructions*, in the system temp directory, **without importing `src/aief_*`** — the point of
a confirmatory round is not to trust the instrument under audit. Adversarial trials W4, W5 and
W6 were run in throwaway **copies** of the repository in the system temp directory.

---

## W1 — F-08, the torque · **PASS**

**Both volumes now agree.** `spec/06` §4 Retention row (line 116) and §10 step 5 (line 246) read
**1.2 N·m**; `spec/01` §6 step 12 (line 182) and §10 step 3 (line 271) read **1.2 N·m**.

**No live 2.5 N·m locator torque survives in `spec/**`.** One `2.5 N·m` token remains, in
`spec/06`:116, inside an explicit historical clause — *"The former 2.5 N·m put an M4 A4-70 at
~114 % of yield"*. That is a record of the superseded value, not an instruction. The other
`2.5 N` hits in `spec/**` are all in `spec/09` and are spring **forces** (`7.5 ± 2.5 N`), not
torques.

**The change is bound.** Recomputed independently:

| Claim | Value | Verdict |
|---|---|---|
| `APR-027` exists | `.ai/project/approvals/APR-027_Alignment_Pin_torque_correction.md` | ✔ |
| `APR-027.prior_hash` = `APR-023.subject_hash` | both `da702fe05f41b1bac39c3ca507c090a7f7e7258ae18db38addb4d079d755edc6` | ✔ |
| `APR-027.subject_hash` = current DC-1 of `spec/06` | both `75cda88184e5ae50acd05fb86dfb61ffc6238219462e8854120c05f14d04f396` | ✔ |
| `FROZEN.md` registers that digest | line 44, same 64 characters | ✔ |

**The two recorded aggregates now agree — checked, because VER-015 found them disagreeing once.**
My own `DC-2` over the 29 registry rows (sorted by the UTF-8 octets of `<path>`, records
`<path> <SP> <digest> <LF>`, no header, no trailer):

```
recomputed  73911786c0795f20b5c5ea5b9ae4a9254d306abaccd9cc9ce54fc55a5d5bc3c2
FROZEN.md   73911786c0795f20b5c5ea5b9ae4a9254d306abaccd9cc9ce54fc55a5d5bc3c2   § Aggregate
STATE.md    73911786c0795f20b5c5ea5b9ae4a9254d306abaccd9cc9ce54fc55a5d5bc3c2   frozen_set_hash
```

All three identical at full length. No path is registered twice; no registered path is absent.

**Residuals recorded, not blocking (F-09, F-10 below).** `FROZEN.md` § *Registration history*
carries **no row** for the `APR-027` re-registration — the last `spec/06` row is
`0d2aa747… → da702fe0…` under `APR-023`. The event survives only as prose in § *Aggregate*.
Separately, `ECR-D-009` still points `approval:` at the **superseded** `APR-023`, never mentions
`APR-027`, and its §*Torque* paragraph still reads *"`spec/01` §6 step 12 and §10 step 3 both
carried the old value; **both are corrected**"* — the sentence whose enumeration made F-08
invisible, with the third site still unnamed. The specification is repaired; the record that
misled is not.

---

## W2 — F-22, the references · **FAIL**

Fourteen records under `.ai/project/ecr/`, both halves tested mechanically.

**The nine `spec/**`-bearing records pass both halves** — `ECR-D-001`, `-002`, `-003`, `-004`,
`-007`, `-008`, `-009`, `-010`, `-011`: `approval:` resolves and the named approval's `ecr:`
lists the ECR. That is what `DR-004` actually repaired.

**`ECR-D-006` is not a failure:** `approval: null` is correct for an `OPEN` record reserved to
the human owner.

**Four records fail the back-reference half, and one of those also fails the existence half.**

| Record | `approval:` | Path resolves | Named approval lists the ECR |
|---|---|---|---|
| `ECR-D-005` | `approvals/APR-001_…` | ✔ | ✘ — `APR-001` has no `ecr:` field |
| `ECR-Q-001` | `approvals/APR-002_…` | ✔ | ✘ — `APR-002` has no `ecr:` field |
| `ECR-Q-002` | `approvals/APR-002_…` | ✔ | ✘ — `APR-002` has no `ecr:` field |
| `ECR-Q-003` | `project/approvals/APR-004_…` | **✘** | ✘ — `APR-004` has no `ecr:` field |

`ECR-Q-003` uses a path grammar no other record uses. The other thirteen are relative to
`.ai/project/`; under that grammar this one resolves to `.ai/project/project/approvals/…`, and
`.ai/project/project/` **does not exist**. It is a surviving instance of exactly the F-22 class.

`APR-001` … `APR-013` — thirteen approvals — carry no `ecr:` field at all; the field enters the
convention at `APR-016`.

**`DR-004`'s claim is false as written.** *"All nine ECR records re-pointed at the filed
artifacts; every reference now resolves and every named approval lists the ECR"* — the first
clause is true, the second and third are true **only of those nine**. Five of fourteen records
fail one half or both. None is under `spec/**`, so `LC-M04-EXIT` is not gated on this; the
overstatement is the finding.

---

## W3 — F-05 and F-06 · **PASS**

**`ECR-D-007` §8/§9 now describe the geometry the specification implements.**

| Quantity | `ECR-D-007` §8/§9 | `spec/01` §3.1 (lines 104–111) | Agree |
|---|---|---|---|
| Locator keep-out radius | **8.5 mm** (5.0 + 3.5 wall) | **8.5 mm** | ✔ |
| Channel outer limit at Ø260 BC | **r ≤ 121.5** | **r ≤ 121.5** | ✔ |
| M4 tap-drill wall | **6.85 mm** | **6.85 mm** | ✔ |
| Wall to OD at Ø306 BC | **2.00 mm** (1.93 worst) | **2.00 mm** (1.93 worst) | ✔ |
| Counterbore | **Ø12.000 → Ø10.000** | `CP-D09`/`CP-D10` **Ø10.000** H7; `spec/06` `AP-D03` Ø10.000 h6 | ✔ |

The superseded Ø12 arithmetic (9.5 / r ≤ 120.5 / 7.85) is gone from the record.

**Action 3 is no longer claimed to have been split out.** §8 now rules it *"Rejected, and
**dispositioned here**"*; §9 closes with *"**No `ECR-D-012` was raised.**"* and explains that
splitting it out would have been the manoeuvre `C7` exists to prevent.

**No live claim that `ECR-D-012` exists remains.** Repository-wide, the identifier occurs in
exactly three places: `ECR-D-007`:203 as the explicit denial, and `DR-004`:41 and `VER-015` as
the record of the finding itself. No record file, no index entry, no register row.

---

## W4 — F-18, the C7 evasion · **PASS**

**The attack was re-run, not read about.** In a temp copy I filed
`ECR-D-099`, `status: OPEN`, `disposition: null`, `affected_artifacts: [spec/01_SEWCP-200_Cooling_Plate.md]`,
and deliberately left `OPEN_ITEMS.md` untouched (verified: zero occurrences). Under `VER-015`
this passed. Now:

```
C7  FAIL   No ECR against the frozen spec remains undispositioned
    ! ECR-D-099: UNDISPOSITIONED against ['spec/01_SEWCP-200_Cooling_Plate.md'] …;
      listed in OPEN_ITEMS Blocking: False
    ! ECR-D-099: undispositioned but absent from OPEN_ITEMS.md Blocking -
      the index does not describe the records it indexes
```

The predicate now reads the records on disk and reports the index divergence separately. **The
hole is genuinely closed.**

**The converse also holds.** Adding `ECR-D-098` to `OPEN_ITEMS.md` § *Blocking* with no record
on disk:

```
C7  FAIL   ! ECR-D-098: listed Blocking with no record - C7 is undecidable
```

Reported, not ignored.

**One defect in the repair (F-11 below).** `C7`'s three evidence lines are unconditional prose,
emitted even when the residue contradicts them. In the trial above the checker printed *"10 bear
on `spec/**`; **all carry a non-empty disposition**"* and *"`OPEN_ITEMS.md` Blocking holds 4 ids
and **is consistent with them**"* in the same breath as the two residues proving neither was
true. The verdict is correct; the evidence text is false. A reader who skims evidence and not
residue is misled by the instrument.

---

## W5 — F-19, the thin-approval hole · **PASS**

In a temp copy I appended one comment byte to `spec/README.md` and filed **no** superseding
approval. That is the thin instrument `VER-015` showed `C2` had been resting on: `APR-026`,
whose entire scope is a single `Re` value.

```
APR-026 [ECR-D-002]: VOID
C2  FAIL   ECR-D-002 carries an approved disposition
    ! ECR-D-002: approval APR-026 on spec/README.md is VOID -
      the artifact moved without a superseding approval
```

**Meanwhile every other approval naming `ECR-D-002` remained valid** — `APR-019`
SUPERSEDED-VALID, `APR-020` LIVE, `APR-021` LIVE, `APR-023` SUPERSEDED-VALID, `APR-025` LIVE,
`APR-027` LIVE. `C1`, `C3` and `C4` stayed PASS. The criterion can no longer be satisfied by an
arbitrary thin member of the set, and one VOID member is sufficient to fail it. **Repaired as
claimed.**

---

## W6 — the C6 hole `VER-015` disclosed · **FAIL**

**`C6` does read the declared `status`, and it does refuse a non-clearing report.** On the live
repository, `C6` **FAILS** today:

```
! ECR-D-002: VER-015…md declares 'VERIFIED WITH FINDINGS - NOT CLEARED. 7 PASS, 4 FAIL'
  - the report does not clear                              (identically for -003, -004)
```

**And the gate is genuinely gated on the verifier's verdict.** In a temp copy I rewrote
`VER-015`'s status to a clearing value and changed nothing else:

```
C6  PASS   Independent verification recorded per disposition
LC-M04 CAD-READY: YES
```

That is the repair working. It is also the whole gate hanging on one line of one file that the
verifier writes — which is why the status of this report is written to be read literally.

### The defect this trial exposed

**`C6` has no supersession relation between verification reports.** It collects *every* report
whose `subject` names the ECR and requires **all** of them to clear. `VER-015` will declare
`NOT CLEARED` for as long as it exists. Demonstrated directly — a temp copy holding an unmodified
`VER-015` **plus** a `VER-016` declaring a clearing status:

```
+ ECR-D-002: subject of VER-015…md, VER-016…md
! ECR-D-002: VER-015…md declares 'VERIFIED WITH FINDINGS - NOT CLEARED…' - the report does not clear
LC-M04 CAD-READY: NO
```

**No confirmatory round can ever pass `C6` while `VER-015` remains on disk.** Not this one; not
a perfect one.

`DR-004` §4 states: *"`C6` remains FAIL until a verifier files a report that clears, and no edit
to this file can change that."* **That is false as implemented.** `C6` remains FAIL *even when* a
verifier files a report that clears. The approvals layer was given a supersession relation for
precisely this reason — `APR-023` became `SUPERSEDED-VALID` rather than VOID when `APR-027`
superseded it — and the verification layer was given none. The remaining routes out are an
instrument change to `C6` (an ECR and an approval), or rewriting an audit record's verdict to
open a gate, which is inadmissible. **`LC-M04-EXIT` is currently structurally unreachable, and
that is an instrument defect, not an engineering one.**

**Second-order (F-12 below).** The predicate is a keyword match — `\bFAIL\b|NOT CLEARED|NOT
VERIFIED` — over the raw status string. My first trial used the status *"VERIFIED - CLEARED. 11
PASS, 0 FAIL"* and `C6` refused it on the token `FAIL` in *"0 FAIL"*. The direction is fail-safe,
but the `status` field is a keyword slot, not prose, and nothing in the repository says so.

---

## W7 — the V-09 caps · **PASS**

Measured with the repository's own pinned families — TF-1 `cl100k_base`
(pin `223921b7…b2a7`) and TF-2 `spiece.model` (pin `d60acb12…ea86`), both available, special
tokens disabled. **The maximum governs**, per `AIEF-FRZ-001` §1.8.

| File | Cap | TF-1 | TF-2 | Governing | **Margin** | Verdict |
|---|---|---|---|---|---|---|
| `project/STATE.md` | 1100 | 838 | **1035** | 1035 | **65** | WITHIN |
| `project/OPEN_ITEMS.md` | 600 | 457 | **533** | 533 | **67** | WITHIN |

Both breaches are repaired. For context, every other capped T0/T1 file is also within:
`BOOT.md` 504/504 (**margin 0**), `FRAMEWORK.md` 748/1100, `PRECEDENCE.md` 382/700,
`laws/INDEX.md` 721/900, `BINDING.md` 574/800.

Two notes. `DR-004` quotes *"`STATE.md` is reduced to 1097"*; I measure **1035** governing — same
direction, both within cap, but the author's figure is not reproducible under the declared
dual-family maximum rule. And `.ai/core/CONTEXT_TIERS.md` still publishes `BOOT.md` at cap **400**
with a sum of **5800**, against the manifest's **504** and **5904** (F-14 below) — a generated
artifact awaiting the Stage 1 re-emission that `OQ-14` withholds, not a `V-09` breach.

---

## W8 — regression sweep · **FAIL**

`python -m pytest tests/ -q` → **565 passed, 7 failed.**

**(b) Caused by `T-007`/`T-008` and recorded as `OI-C-12` — four tests.** The register row names
exactly these four, and each fails on a count of live, growing project state:

| Test | Observed |
|---|---|
| `test_every_task_record_loads` | extra `T-007`, `T-008` |
| `test_the_live_gap_between_declared_and_effective_is_five_tasks` | 8 producers against 6 |
| `test_the_live_dependency_state_is_derived_end_to_end` | current = `['R-014','R-015']`, expected 1 |
| `test_x09_guards_the_publication_channel_in_both_directions` | reached includes `R-015`, `R-016` |

**(a) Pre-existing on the Stage 6 track — two tests.**

| Test | Observed |
|---|---|
| `test_v24_live_registry` | `framework.manifest.json` DC-1 `920eb6ee…` != registered `8af8971b…` (**ECR-D-006**), and `AIEF-AMD-014` unregistered (**VER-015 F-15**) |
| `test_full_pipeline_with_stub_families` | `PRECONDITION-FAIL ['V-24 FAIL','V-25 FAIL']` — downstream of the same |

**(c) Something else — one test, and this is the one that matters.**

`test_x06_open_on_the_result_that_pins_the_layer_it_describes`, and `X-06` in
`python -m aief_exec check`:

```
X-06  FAIL   Result currency
      FAIL   R-015: declared CURRENT but is STALE
      FAIL     deliverable spec/06_SEWCP-700_Alignment_Pins.md:
                 DC-1 75cda88184e5… != pinned da702fe05f41…
      FAIL     deliverable src/aief_gate/criteria.py:
                 DC-1 ea31104e6447… != pinned 05ec0d519a08…
```

**Both stale pins were moved by the repairs themselves** — the first by the `APR-027` torque
correction (W1), the second by the `C1`–`C4`, `C6` and `C7` instrument changes (W4, W5, W6).
This is **not** a `T-007`/`T-008` count defect and it is **not** covered by `OI-C-12`, whose row
names four tests, all of the counting class.

`DR-004` §3 says *"**Five** exec-layer tests broke on the addition of `T-007`/`T-008`. Recorded
as `OI-C-12`."* It miscounts — four are recorded — and mis-attributes the fifth. **`R-015`, the
result record that publishes the entire LC-M04 coherence package, currently declares
`status: CURRENT` over a state that no longer exists**, and nothing in the repository records
that. It is the stale-label class this project has already been bitten by four times, reappearing
in the record that certifies the repairs.

---

## W9 — has anything new broken? · **PASS**

**1 · All eleven `spec/**` DC-1 digests still match `FROZEN.md`.** Recomputed with my own DC-1:
29 registry rows parsed, no duplicate path, no registered path absent, **11 of 11 `spec/**` rows
reproduce exactly**. Eleven files exist under `spec/` and eleven are registered — none
unregistered. The single registry mismatch repository-wide remains
`framework/framework.manifest.json` (`ECR-D-006`, not under `spec/**`, excluded by name in
`GATES.md`).

**2 · `python -m aief_clearance` still passes.** `CLEARANCE OK`, exit 0. Eight features resolved
from `spec/00` §3.2 and every declared pair clears, including the re-clocked locators at
r = 130 against the outer choke stations.

**3 · `spec/01` and `spec/02` still agree on the choke fastener** — and `spec/00` agrees with
both:

| | `spec/00` §ICD | `spec/01` | `spec/02` |
|---|---|---|---|
| Fastener | **M5 × 25** SHCS, 12 + 4, 3.5 N·m | `CP-IF-3` **M5 × 25**, *"not M5 × 30"* | §10 step 13 **M5 × 25**, *"Do not substitute M5 × 30"* |
| `CP-D26` | slotted counterbore, Cooling Plate | **11.0 W × 12.5 L × 2.5 deep**, +0.20/−0, masked | referenced, consistent |
| `HP-D12` | helical inserts, Heater Plate | referenced | **6.50 +0.30/−0 deep**, 1.50 mm min to bond face, engages 5.40 mm |

No divergence. Nothing in criteria 1–3 was damaged by the repairs.

---

## W10 — the honest question · **FAIL**

> **Is there anything in this repository that should stop someone opening Fusion 360 and
> modelling SEWCP-200 tomorrow?**

## **Yes.**

**The specification set is not the problem.** I found no contradiction in `spec/**`; W1, W3 and
W9 all hold. The problem is the artifact `STATE.md.next_action` sends the modeller to:
`implementation/01_SEWCP-200_Cooling_Plate/SEWCP-200_CAD_Implementation_Package.md`.

**1 · The parameter master still carries the exact collision `ECR-D-010` exists to prevent.**
§3.3 line 213:

```
| `ang_kin_top_1/2/3` | Top locator angles | `30.0` / `150.0` / `270.0` | deg | Vol 00 §3.2 | — |
```

`spec/00` §3.2 line 119 now reads **75°, 195°, 315°**, and line 125 records what 30°/150°/270°
did: *"sat on three outer choke rays, overlapping the M5 slot by 4.5 mm radially and the Ø22
washer pad almost completely."* The package's **own banner**, line 52, states the re-clocking —
and then its parameter table, its timeline step 11 (line 312) and its modelling step 6.34 (line
395) all still carry 30/150/270. Step 6.34 is labelled *"**discharged**"* while carrying the
colliding number. **A modeller who follows §6 in order builds the collision.** This is the single
most dangerous thing in the repository right now, because it is not a stale note in a history
section — it is the live parameter master, and it cites as its authority a document that now says
the opposite.

**2 · Two dimensions the modeller needs are still the literal string `UNSPECIFIED`.** §3.4 lines
238–239, `choke_cbore_d` and `choke_cbore_dep`, both still tagged **HOLD H3** — when `ECR-D-004`
fixed them at 11.0 W × 12.5 L × 2.5 deep and the banner declares H3 discharged. Timeline step 13
asks for those counterbores. Step 6.02's acceptance criterion is *"Parameter count matches §3"* —
which it does, with two of the values being the word UNSPECIFIED.

**3 · The sketch table still offers the superseded Ø12 geometry as a live alternative.** Line
351, sketch S11, marked **RESOLVED**: *"Ø6.000 H7 bore (Vol 01) **or** Ø12.0 H7 × 3.0 counterbore
+ M4 tap (Vol 06)"*. `ECR-D-001` ruled SEWCP-700 governs — it is not an "or" — and `ECR-D-007`
action 3 took Ø12.0 → **Ø10.0**. This is the same superseded Ø12 arithmetic `VER-015` F-05 found
in `ECR-D-007` §8/§9: repaired there, not repaired here.

**4 · The import the procedure depends on does not exist.** Step 6.02 imports
`params/generated/SEWCP-200.csv`. `params/generated/` contains only `.gitkeep`. The modeller
necessarily falls back to typing §3 by hand — the tables in (1) and (2).

**The disclaimer does not discharge this.** The package does say *"Where this package and
`spec/**` disagree, `spec/**` governs"*, and that is honest. But a parameter master exists so
that the modeller does **not** re-derive values from the specification, and §6.02 instructs them
to import it. A disclaimer that requires re-checking every value against the spec makes the
package worthless as a package, and no modeller reads it that way.

**`OI-P-03` claims the package was *"Corrected in this session so the package is usable for
CAD"*, and the banner claims *"the numeric errors that would have misled a modeller are corrected
in place below."* Both claims are false for items 1–3. That is a cosmetic repair presented as a
real one, and it is the finding.**

**Do not open Fusion 360 against this package** until §3.3 `ang_kin_top_*`, §3.4 `choke_cbore_*`,
sketch S11 and step 6.34 are corrected. Modelling directly from `spec/00`, `spec/01` and
`spec/06` is safe today — those three are coherent and hash-registered.

---

## Findings

| ID | Finding | Severity | Owner | Criterion |
|---|---|---|---|---|
| **F-01** | **`C6` has no supersession relation between verification reports.** It requires *every* report naming the ECR to clear, so `VER-015`'s `NOT CLEARED` blocks the gate permanently. Demonstrated: a clearing `VER-016` alongside an unmodified `VER-015` still fails `C6`. **`LC-M04-EXIT` is structurally unreachable.** `DR-004` §4's *"C6 remains FAIL until a verifier files a report that clears"* is false as implemented | **HIGH** | chief-systems-engineer + A4 | W6 |
| **F-02** | **The CAD package's parameter master still carries `ang_kin_top_1/2/3` = 30/150/270**, the clocking `ECR-D-010` was raised to remove, sourced to a `spec/00` §3.2 that now says 75/195/315. Timeline step 11 and modelling step 6.34 carry it too, the latter labelled "discharged". A modeller following §6 builds the collision | **HIGH** | mechanical.cad-engineer | W10 |
| **F-03** | `choke_cbore_d` / `choke_cbore_dep` still read **UNSPECIFIED** and are tagged HOLD H3, though `ECR-D-004` dispositioned them at 11.0 W × 12.5 L × 2.5 deep and the banner declares H3 discharged | **MEDIUM** | mechanical.cad-engineer | W10 |
| **F-04** | Sketch S11 still offers **Ø12.0 H7 × 3.0** as a live alternative marked RESOLVED. Superseded twice over: `ECR-D-001` (SEWCP-700 governs, not an "or") and `ECR-D-007` action 3 (Ø12.0 → Ø10.0) | **MEDIUM** | mechanical.cad-engineer | W10 |
| **F-05** | **`R-015` declares `status: CURRENT` but is STALE** — it pins `spec/06` at `da702fe0…` and `criteria.py` at `05ec0d51…`, both moved by the repairs. Not recorded anywhere; **not** covered by `OI-C-12`, which names four tests of a different class. `DR-004` §3 miscounts five and mis-attributes this one | **MEDIUM** | software.software-engineer | W8 |
| **F-06** | `params/generated/SEWCP-200.csv` does not exist; the directory holds only `.gitkeep`. Step 6.02 is unexecutable as written | **LOW** | mechanical.cad-engineer | W10 |
| **F-07** | `ECR-Q-003`'s `approval:` reads `project/approvals/APR-004_…`, a grammar no other record uses; it resolves to `.ai/project/project/approvals/…`, which does not exist. Surviving F-22 instance | **LOW** | chief-systems-engineer | W2 |
| **F-08** | `APR-001` … `APR-013` carry no `ecr:` field, so `ECR-D-005`, `ECR-Q-001`, `ECR-Q-002` and `ECR-Q-003` have no back-reference. `DR-004`'s *"every named approval lists the ECR"* holds only for the nine `spec/**` records | **LOW** | chief-systems-engineer | W2 |
| **F-09** | `FROZEN.md` § *Registration history* has **no row** for the `APR-027` re-registration of `spec/06`. Every other registry change has one; this event survives only as prose in § *Aggregate* | **LOW** | chief-systems-engineer | W1 |
| **F-10** | `ECR-D-009` still points `approval:` at the superseded `APR-023`, never names `APR-027`, and still asserts *"both are corrected"* enumerating only `spec/01`'s two sites — the sentence that concealed F-08, with the third site still unnamed | **LOW** | chief-systems-engineer | W1 |
| **F-11** | `C7`'s evidence lines are unconditional prose emitted even when the residue contradicts them — printing *"all carry a non-empty disposition"* and *"is consistent with them"* in the same output that disproves both | **LOW** | software.software-engineer | W4 |
| **F-12** | `C6`'s status predicate is a keyword match over the raw string; a genuinely clearing status reading *"… 0 FAIL"* is refused on the token. Fail-safe, but the field is an undocumented keyword slot | **LOW** | software.software-engineer | W6 |
| **F-13** | `FROZEN.md` § *Standing verification* still reads *"**None yet** … `V-24` … is **not implemented as software**"*. `V-24` **is** implemented (`aief_stage6.preconditions.check_v24`) and runs in the suite — where it currently fails on `ECR-D-006` | **LOW** | chief-systems-engineer | W1 · W8 |
| **F-14** | `.ai/core/CONTEXT_TIERS.md` publishes `BOOT.md` cap **400** and sum **5800** against the manifest's **504** and **5904**. Generated artifact awaiting the Stage 1 re-emission `OQ-14` withholds; recorded, not a `V-09` breach | **INFO** | repository-engineer | W7 |

---

## Verdict

| Criterion | Subject | Verdict |
|---|---|---|
| **W1** | F-08 — the torque, and its binding | **PASS** |
| **W2** | F-22 — the ECR references | **FAIL** |
| **W3** | F-05 / F-06 — `ECR-D-007` §8/§9 and `ECR-D-012` | **PASS** |
| **W4** | F-18 — the `C7` evasion, both directions | **PASS** |
| **W5** | F-19 — the thin-approval hole | **PASS** |
| **W6** | the `C6` hole `VER-015` disclosed | **FAIL** |
| **W7** | the `V-09` caps | **PASS** |
| **W8** | regression sweep | **FAIL** |
| **W9** | has anything new broken | **PASS** |
| **W10** | the honest question | **FAIL** |

### **6 PASS · 4 FAIL**

**The engineering repairs are real.** F-08, F-05, F-06, F-18, F-19 and the `V-09` breaches were
all repaired at the artifact, not at the description of it, and each was confirmed here by
independent recomputation or by re-running the original attack. The two instrument repairs —
`C7` reading the records rather than the index, and `C1`–`C4` requiring every naming approval to
be non-VOID — are the most valuable work in the session and both survive adversarial trial.
`DR-004` contested nothing and that was correct.

**Three things stop this gate.**

1. **`C6` cannot be satisfied by any report.** Absent a supersession relation between
   verification reports, `VER-015`'s recorded verdict blocks `LC-M04-EXIT` permanently. This
   round cannot clear it and neither can a perfect one. **F-01 must be dispositioned before any
   verifier is dispatched again**, or the next round burns for nothing.
2. **The CAD package would mislead a modeller into the `ECR-D-010` collision.** F-02 is a
   correctness defect in the one artifact the project's own `next_action` directs a modeller to
   open. The specification is right; the thing built from it is not.
3. **A repair broke a record and the disposition did not notice.** F-05 — `R-015` is stale, and
   `DR-004`'s account of the test failures is wrong about both the count and the cause.

**`LC-M04-EXIT` is NOT passed. CAD is NOT authorised on the strength of this round.** Confirmed
by execution, not asserted: `python -m aief_gate` reports **`LC-M04 CAD-READY: NO`** with `C6`
FAIL at the recorded instant.

**Nothing in `spec/**` blocks modelling.** Whoever repairs F-02 first should note that the
correct value is already frozen, registered and computed — `spec/00` §3.2 line 119, and
`python -m aief_clearance`.
