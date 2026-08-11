# ECR-D-006 — The framework manifest does not reproduce against its registered digest

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-ecr.schema.json`.
> Record filed `S-2026-08-10-01`. The full derivation has lived in
> [`../OPEN_ITEMS_REGISTER.md`](../OPEN_ITEMS_REGISTER.md) since `S-2026-08-08-12`; **no ECR
> record existed**, and its absence made `LC-M04-EXIT` `C7` *undecidable* rather than merely
> unsatisfied, because `C7` is evaluated over `affected_artifacts` and there was nothing to read.

```yaml
ecr_id:       ECR-D-006
class:        D
raised_by:    chief-systems-engineer · S-2026-08-08-12
status:       DISPOSITIONED
disposition:  "A - RE-REGISTER AT THE MEASURED DIGEST AND RE-AFFIRM THE CHANGE SETS"
ruled_by:     claude-under-owner-delegation · S-2026-08-11-06
approval:     approvals/APR-033_Reregister_Framework_Manifest_ECR-D-006.md
affected_artifacts:
  - framework/framework.manifest.json
  - framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md
evidence:     "The registry carries 8af8971b78d7... and the artifact normalises under DC-1 to a
               different value. Nine alternative constructions were tested and none reproduces
               the recorded value, so this is a content divergence, not a construction
               disagreement. Full dual-computed derivation at OPEN_ITEMS_REGISTER.md row
               ECR-D-006, including the control that reproduces APR-010 subject_hash exactly."
impact:       "Re-affirmation of the AIEF-AMD-013 manifest change; Compiler Stage 6 execution.
               NOT under spec/**, so it bears on neither LC-M04-EXIT C5 nor C7."
requested_action: "Human-owner re-affirmation of the AIEF-AMD-013 bytes."
raised_at:    2026-08-08T00:00:00Z
closed_at:    null
residual:     null
```

---

## 1 · Class

**D — defect.** A registered frozen artifact does not reproduce against its registered digest,
so LAW-01's *"changed only by an approved ECR and a recorded human approval"* is unsatisfied for
whatever bytes differ, and under LAW-10 clause 2 `APR-012`'s binding to its subject is void as
recorded.

## 2 · Affected artifacts

`framework/framework.manifest.json` — **and nothing under `spec/**`.** That fact decides this
ECR's relationship to the LC-M04 gate and is why it is recorded rather than resolved here.

## 3 · Evidence

The dual-computed derivation, the three-way method check, the control that reproduces `APR-010`'s
`subject_hash` to the digit, and the nine rejected alternative constructions are all in
[`../OPEN_ITEMS_REGISTER.md`](../OPEN_ITEMS_REGISTER.md) row `ECR-D-006`. They are **not**
restated here; duplicating a derivation is how two versions of it come to disagree.

**Independently reproduced this session.** `python -m aief_approval verify` reports
`framework/framework.manifest.json` as the single registered path carrying **no LIVE approval**,
with `APR-001`, `-002`, `-004`, `-006`, `-010` and `-012` all **VOID** in consequence, and
separately reports the registry/tree mismatch. That tool was written to check approval chains
and had no knowledge of this ECR; it derived the same conclusion from repository bytes alone.

## 4 · Impact

Blocks re-affirmation of the `AIEF-AMD-013` manifest change and Compiler Stage 6 execution.

**Does not block `LC-M04-EXIT`.** `C5` is scoped to *"the frozen specification"* and this
artifact is not part of it; `C7` is scoped to ECR-D items *"whose `affected_artifacts` lie under
`spec/**`"* and this one's do not. [`../GATES.md`](../GATES.md) records the same exclusion
positively and by name.

## 5 · Requested action

Human-owner re-affirmation of the `AIEF-AMD-013` bytes. **Root cause is `OI-V-02`** — no standing
check bound the registry to the tree, which is precisely what `ECR-D-005` recorded and what left
this undetected for two sessions. That gap is now partly closed: `aief_approval` fails non-zero
on exactly this condition, and `tests/test_approval_chain.py` holds it there.

## 6 · Disposition

~~**None. OPEN.** Reserved to the human owner; **not closable by the raiser** (LAW-02 clause 5).~~

**Superseded 2026-08-11 by §9 below.** The text above is retained verbatim as the record of the
state this ECR stood in from `S-2026-08-08-12` to `S-2026-08-11-06`. Nothing above this line is
edited.

## 7 · Relationship to `LC-M04-EXIT`

**Not a criterion of this gate.** Recorded here so that `C7` is decidable rather than undefined.

---

# Addendum — `S-2026-08-11-06`, under owner-delegated engineering authority

**Appended, not edited.** No text above this rule is altered. The finding, the evidence, the
method and the reservation stand exactly as they were written.

## 8 · What this session found that §3 did not record

§3 records **one** defect: the registered digest `8af8971b…a7e42ff7` does not reproduce against
the artifact. Auditing the current repository for release readiness found a **second**, of the
same class and never recorded:

**The `AIEF-AMD-014` change set is applied, unapproved and unregistered.**

| Owed by `AIEF-AMD-014` | State on disk at `S-2026-08-11-06` |
|---|---|
| `project/approvals/APR-014` — the manifest amendment approval | **Does not exist.** The approvals directory runs `APR-013` → `APR-016` |
| `project/approvals/APR-015` — the `AIEF-AMD-014` registration approval | **Does not exist** |
| `FROZEN.md` manifest row re-registered at the post-change digest | **Not done.** The row still carried `8af8971b…`, the pre-AMD-014 recorded value |
| `FROZEN.md` gains `AIEF-AMD-014`, 29 → 30 rows | **Not done.** 29 rows; `check_v24` names the omission: *"AMD-21 criterion candidate unregistered"* |
| The eleven manifest changes of §§AMD-49…AMD-51 | **Done.** All eleven are present in the artifact |

So the substance was applied and every record of its authority was omitted. The consequence is
the one `aief_approval verify` reports without knowing any of this history: the working tree is
at `920eb6ee…37814090` and **no approval binds that state**, which voids `APR-001`, `-002`,
`-004`, `-006`, `-010` and `-012` in consequence.

**Root cause is the same `OI-V-02` this ECR already names**, one turn deeper: no standing check
bound the registry to the tree, so a session could declare a registry edit in its own instrument
and not perform it, and nothing would notice. `V-24` now exists as software and does notice.

## 9 · Disposition — **A — re-register at the measured digest and re-affirm the change sets**

**Ruled by `claude-under-owner-delegation · S-2026-08-11-06`** under the owner's written
delegation of 2026-08-11, which names this ECR expressly: *"ECR-D-006 is currently listed as
owner-reserved, but the owner has now explicitly delegated engineering decision authority to
Claude for this run."*

**This is not a human approval and is never to be cited as one.** It is
`OWNER-DELEGATED ENGINEERING AUTHORITY EXERCISED BY CLAUDE`, recorded at
[`../decisions/DECISIONS_S-2026-08-11-06.md`](../decisions/DECISIONS_S-2026-08-11-06.md) DEC-05.
LAW-02 clause 5 is satisfied on its own terms — the raiser is
`chief-systems-engineer · S-2026-08-08-12`, and this is a different session in a different role.
LAW-02 clause 4's human involvement is the delegation itself, at `core/PRECEDENCE.md` rank 1.

### What was decided

1. `framework/framework.manifest.json` is re-registered at its **measured** DC-1
   `920eb6eec217732152c452d51f01e471940df6f2e2ffe608c377fccc37814090`, dual-computed.
2. `framework/AIEF-AMD-014_…` is registered at its measured DC-1
   `07ced7582c7dafc8649eb8ac0736d1587ba4cc38c30f11c929240809be639945`, under the AMD-21
   criterion.
3. The DC-2 aggregate is recomputed over the resulting **30** rows:
   `19989657464cd9dfae3668addbb7e8bec6dcd47f7cd6cfda35ea819448ddc07e`. `STATE.frozen_set_hash`
   follows.
4. The three change sets — `AIEF-AMD-012` (3 changes), `AIEF-AMD-013` (13) and `AIEF-AMD-014`
   (11) — are re-affirmed as the approved content, on the enumeration at
   [`../approvals/APR-033_Reregister_Framework_Manifest_ECR-D-006.md`](../approvals/APR-033_Reregister_Framework_Manifest_ECR-D-006.md).
5. `APR-014` and `APR-015` are recorded as **never filed**. The identifiers are not reissued.

### Why this disposition and not another

`AIEF-AMD-014` §AMD-53 §5 recommended exactly this — disposition **A**, the `ECR-D-005`/`APR-001`
precedent — and one thing has changed since that makes the recommendation stronger rather than
weaker. §AMD-53's own second recommendation, *"commit before the next multi-session phase"*, was
acted on at `5e7ac74`. The consequence is that the attribution no longer rests on inverting
remembered edits: `git show 8546960:framework/framework.manifest.json` is the `AIEF-AMD-010`
state, it reproduces to `ae16ccac…9d8395aa` — `APR-006`'s `subject_hash`, recorded four sessions
before the defect — and the whole delta from it to the current artifact is one structural diff
in which **every one of twenty-seven changed leaves carries its own authorising citation and
nothing was removed**. The counts match each instrument's own enumeration: 3, 13 and 11, and the
eleven partition 4 new members/entries + 2 edges + 1 cap + 4 text extensions exactly as
`AIEF-AMD-014` declares.

Alternatives B (revert), C (waive), D (register the unreproducible value) and E (repair only the
manifest row) are examined and rejected at `APR-033` § *Alternatives rejected*.

### One departure from the recommendation, and its ground

§AMD-53 §5 directs that `prior_hash` be the **measured** `e87ae68e…5a12cf892`. `APR-033` records
`8af8971b…` instead. The reason is stated at `APR-033` § *Why `prior_hash` is `8af8971b…`* and is
not a preference: `e87ae68e…` is another session's reconstruction of bytes that were never
committed and no longer exist, **this session has not measured it and cannot**, and signing a
measurement not taken is the very failure this ECR exists to record. `8af8971b…` is used strictly
as a chain link to `APR-012`'s *declared* predecessor state, with the approval stating in terms
that it asserts no measurement of it.

### What remains true, and open

**The `AIEF-AMD-013` intermediate state is still unreproducible and always will be.** No
disposition can recover bytes that were never written to git. Re-registration repairs the
registry and binds the current artifact; it does not manufacture a reproducible binding for a
state that no longer exists. That residual is recorded here, at `APR-033` § *What this approval
does not repair*, and in `FROZEN.md`'s registration history, and it is **not** claimed closed.

## 10 · Verification of the disposition

Computed, never asserted:

```
python -m aief_stage6 preflight        # V-24 PASS, 30 of 30 registered rows reproduce
PYTHONPATH=src python -m aief_approval verify   # APPROVAL CHAIN INTEGRITY OK
PYTHONPATH=src python -m aief_gate     # C1..C7, LC-M04 CAD-READY: YES
PYTHONPATH=src python -m pytest tests/ -q
```

`closed_at` remains `null`: the disposition is made and applied, and closure of an ECR-D is a
`qa-engineer` act on independent verification, not a self-declaration by the disposing session
(LAW-05).
