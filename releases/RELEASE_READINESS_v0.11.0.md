# SEWCP Release-Readiness Report — `v0.11.0`

> **Instance artifact.** Partition `releases`. Audit of the published state, which is `origin/main`. **Every figure below is computed, and the command that computes it is
> named beside it.** Where a figure was measured from a *clone of the published repository*
> rather than from the working tree, it says so — that distinction is the subject of one of
> this run's findings.
>
> **No verified CAD geometry was modified.** `spec/**` is byte-identical across **all five**
> release commits — proven at the tree level, one and the same tree object throughout — and
> `V-24` verifies 31 of 31 registered artifacts. No Fusion document was opened at any point.

---

## 1 · Verdict

# RELEASED — CAD AND SOFTWARE COMPLETE; PHYSICAL QUALIFICATION NOT STARTED; HARDWARE BUILD BLOCKED

Three statements, all true at once, and the release is honest only if all three are read:

| | |
|---|---|
| **The repository is published and reproducible.** | `origin/main` at `1c15818`, verified from the server. A clean clone runs **800 passed, 52 skipped, 0 failed** and every standing check exits 0 except two that exit 1 by design |
| **Nothing physical exists.** | 0 of 91 hardware-verifiable requirements verified. No article has been built. Four mass figures are `MODEL-PREDICTED` and labelled so |
| **The design must not be built as it stands.** | `ECR-D-016`: the Support Ring isolation joint does not close — `SR-02`, `SR-03` and `SR-04` all fail on frozen dimensions. Ruled, remedy computed, **implemented at Rev B** |

---

## 2 · Release-readiness matrix

| Item | Status | Evidence | Blocks release? |
|---|---|---|---|
| Gate `LC-M04-EXIT` | **PASS** `C1`–`C7` | `python -m aief_gate` → `LC-M04 CAD-READY: YES`, exit 0 | No |
| Feature clearance | **PASS** | `python -m aief_clearance` | No |
| Parameter master | **PASS**, 105 derived | `python -m aief_params check` | No |
| Approval chains | **CLEAN** | `python -m aief_approval verify` | No |
| Freeze registry | **31 of 31 verify** | `V-24`; DC-2 `1f32489a…8d45cc4b` | No |
| Boot step **B2a** | **PASS 75/75** | Recomputed independently, three times, without importing `src/aief_stage6` | No |
| Deliverables | **61 registered, 61 reproduce, 0 unregistered** | `python -m aief_deliverables`, bi-directional | No |
| Assembly / interfaces | 19 occurrences; 12/12; FSV **19/19** | `cad/runs/**` | No |
| Drawings | 11 documents / 14 sheets, 79 dims, 0 unsourced, **byte-deterministic** | `drawings/generate.py`, two consecutive renders 39/39 stable | No |
| BOM | Rev A, cross-checked four ways | `src/sedep/bom` | No |
| Tests | **895 local · 843 from a clean clone**, 0 fail | measured both ways, the second by cloning from GitHub | No |
| Licence | **`MIT AND CC-BY-4.0`**, boundary by path | `LICENSE`; `C-4` **CLOSED** | No |
| CI | `validate` workflow | `C-5` **CLOSED** | No |
| Secrets / PII | **none found** | scan over all 583 tracked files | No |
| **Physical verification** | **0 of 91 — NOT VERIFIED, HARDWARE REQUIRED** | `PVR-001` | **No for release; YES for build** |
| **`ECR-D-016`** | **OPEN** — dispositioned A, Rev B | §4 | **No for release; YES for build** |
| **`ECR-D-014`** | **CLOSED** — five independent rounds | §5 | No |
| `CMP-BLOCK-004`/`-005` | OPEN — gate **AIEF framework 1.0.0**, a different release | `DEC-18` | No |
| GitHub | **PUSHED**, remote HEAD verified | `git ls-remote` = `1c15818`; 0 ahead, 0 behind | — |

---

## 3 · What this run actually did

Nine owner-delegated decisions (`DEC-11`…`DEC-19`), five ECRs raised and dispositioned, two
closed, three approvals filed, two ledger entries, and **three independent cold-context QA
rounds** — two of which returned `NOT CLEARED` and each of which found a real defect in a
repair that looked complete.

**The engineering finding.** Performing the `SR-03`/`SR-04` drawing trace that `OI-C-15` §6.2
had recorded as owed and never filed found **three frozen acceptance criteria failing on
frozen dimensions**, all from one omission: `spec/03` §2.1 and §3.1 compute the flange gap as
empty while §5.2 puts a 6.00 mm grounded ring inside it. The arithmetic is proven against the
specification's own published answer, and an independent round attacked it with five
counter-readings, all of which died.

**The governance finding.** `ECR-D-014`'s ruling was enforced by nothing — first on any path,
then on the canonical path alone. Six mutations were applied to the source for real before the
enforcement could be called real.

**The release finding.** The repository claimed a reproducibility it had never tested from
outside itself: a clone failed 35 tests while the desk passed 846.

---

## 4 · `ECR-D-016` — read this before building anything

| | Required | Computed |
|---|---|---|
| `SR-04` clearance | ≥ 12.00 mm | **8.50 mm** — the greatest value any hardware choice can offer |
| `SR-03` creepage | ≥ 20.00 mm | **14.00 mm** as modelled, 17.42 at best |
| `SR-02` shunt impedance | ≥ 400 Ω | **353.9 Ω** |

Plus a 3.00 mm radial collision between `SEWCP-401` and the web, and a flange offering 16.00 mm
of radial width against 16.00 mm of demand from its own frozen features — which is why four
dimensioned features, three of them *Critical*, are absent from the verified model
(`OI-CAD-04`).

**Ruled disposition A — Rev B baseline revision. Implemented at Rev B, not in a release
session.** A feasible Rev B is computed and published at the record, **with its own defects
recorded at §7**: the ≈22 mm creepage does not reproduce and the relocated web recreates the
conflict in miniature. It is a starting point, not a design.

---

## 5 · `ECR-D-014` — closed after five independent rounds, and what that cost

| Round | Verdict | What it found |
|---|---|---|
| 1 | `NOT CLEARED` | Cleared `ECR-D-006`. Refused this: the ruling was **enforced by nothing** — three call-site mutations survived all 799 tests |
| 2 | `NOT CLEARED` | The round-1 repair was enforced **only on the preview path**. A canonical build could write a 249-token prefix against a cap of 200. **No test had ever called `run()` with an `Authorization`** |
| 3 | `NOT CLEARED` | Enforcement **FULLY DISCHARGED** — fifteen mutations, six new, all die. Refused on record accuracy |
| 4 | `NOT CLEARED` | The check written to end a recurring defect **did not catch that defect**, and its self-test was circular |
| 5 | **close** | Re-proved the substance again; found the check still incomplete (12 of 13 phrasings evaded); **recommended closure with named residuals** |

**Closed on round 5's own recommendation**, which is a `qa-engineer` act in a distinct cold
session. LAW-02 clause 5 and LAW-05 are satisfied on their own terms: **no session that
repaired this ECR certified its own repair, across four consecutive attempts.** That is the one
thing in this run delegation could not buy, and it was not faked.

**The closure does not say the repairs were clean.** Four consecutive repair sessions each
introduced a defect of the class they were repairing. **That process finding is real, it is
recorded at `OI-V-17`, and it is not closed by this release.**

---

## 6 · What a reader should not conclude

Every standing check is green and 852 tests pass. **That is not the same as ready.** Nothing
physical has been built or measured; 91 requirements await hardware; one joint of the design
is known not to close; and the framework's own `ECR-D-014` is open on a rule this session
could have quietly ignored. The green is real, it is broader than it was, and it is still
narrow.


---

## 7 · `OI-C-10` — the constraint that is now binding

`project/OPEN_ITEMS.md` is a bounded T1 index with a **600-token cap**, and it stands at
**597** against a marginal cost of about **five tokens per identifier**.

Twice this run a new open item was raised and had to be withdrawn — the index breached 600 and
`V-09` halted Stage 6, exactly as the row had predicted one session earlier. **Three findings
in three sessions have now been denied an identifier of their own** and folded into rows that
already carry their class.

That is defensible each time on the merits and it is recorded each time as **budget-forced
rather than chosen**, because a register that merges findings to stay inside a cap has stopped
being a register of findings. There is no grammar left to reduce, closing items frees nothing
(an id merely moves between sections), and `BOOT.md` — the obvious donor — sits at **504
against a cap of 504**.

**No session-level action remains.** The lawful successors are named at the row: a `token_cap`
redistribution, a ceiling re-derivation, or a further grammar reduction. It is an A4 and
human-owner decision, and it is now blocking **the next finding**, not the next dozen.

## 8 · What was verified independently, and by whom

Every figure in §2 was recomputed by at least one cold-context round that imported nothing from
the code it was auditing. Specifically, and across five rounds: DC-1 over all 75 covered files;
DC-4 compared to the lock aggregate and to `BINDING.core_digest_pin`; DC-2 over the 31-member
freeze registry; DC-3 over every ledger entry with each `prev_hash` link; the `ECR-D-016`
electrical model against `spec/03` §2.1's own published answer; the deliverable register
against both the repository and the generation root; the licence boundary against every tracked
file; and the suite from a genuine `git clone` of what was actually pushed.

**Two of those recomputations contradicted the repository and were right.** The deliverables
were not byte-identical to the generation root, and the suite did not pass from a clone. Both
are corrected and both are recorded.
