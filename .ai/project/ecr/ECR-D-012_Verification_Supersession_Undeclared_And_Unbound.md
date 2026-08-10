# ECR-D-012 — The C6 verification-supersession relation is computed but undeclared, and is bound to nothing

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-ecr.schema.json`.
> Record filed `S-2026-08-10-04`. Raised on [`VER-016`](../verification/VER-016_Confirmatory_Round_On_VER-015_Repairs.md)
> finding **F-01** (HIGH) and finding **F-12** (LOW), which that report assigned to
> `chief-systems-engineer + A4` and for which it named the remedy in terms:
> *"an instrument change to `C6` (an ECR and an approval)"*.

```yaml
ecr_id:       ECR-D-012
class:        D
raised_by:    chief-systems-engineer · S-2026-08-10-04
status:       CLOSED
disposition:  A - DECLARE THE RELATION AND BIND IT WITH A SEAL; STATUS BECOMES A CLOSED VOCABULARY
ruled_by:     human-owner · S-2026-08-10-04 · interactive decision pause
approval:     approvals/APR-028_Verification_Supersession_Relation.md
affected_artifacts:
  - .ai/project/GATES.md
  - src/aief_gate/criteria.py
  - tests/test_verification_chain.py
evidence:     "VER-016 W6 demonstrated in a temp copy that a clearing VER-016 filed alongside an
               unmodified VER-015 still fails C6, and concluded 'LC-M04-EXIT is currently
               structurally unreachable, and that is an instrument defect, not an engineering
               one'. HEAD 5e7ac74 then added a supersession filter to criteria.py:240-257 which
               GATES.md does not declare anywhere, and which binds supersession to nothing: the
               superseded set is assembled globally from every report's `supersedes` field, so a
               bare line in any report retires any audit, of any subject, without proof that the
               superseding verifier ever read the bytes it displaced. Separately VER-016 F-12
               showed C6 refuses a genuinely clearing status reading '11 PASS, 0 FAIL' on the
               token FAIL, the `status` field being an undocumented keyword slot."
impact:       "LC-M04-EXIT C6, and therefore the gate. Two failure modes, opposite in direction.
               Without a supersession relation no verification round can ever clear C6 while an
               adverse predecessor exists on disk. With the relation as implemented at 5e7ac74,
               an adverse verdict is retirable by one unbound line - which is the laundering
               route VER-016 called inadmissible when it appears as rewriting a verdict, and
               which is no more admissible when it appears as asserting supersession. NOT under
               spec/**, so it bears on neither C5 nor C7."
requested_action: "Rule the relation at the authority that ruled the approval-supersession
               relation in S-2026-08-10-01, declare it in GATES.md, and bind it to content."
raised_at:    2026-08-10T00:00:00Z
closed_at:    2026-08-10T00:00:00Z
residual:     null
```

---

## 1 · The defect, stated once

`LAW-05` makes verification the property that no agent verifies what it produced. `C6` is the
criterion that carries `LAW-05` into `LC-M04-EXIT`. Two distinct things were wrong with it.

**(a) The relation was computed and never declared.** [`GATES.md`](../GATES.md) is the authority
for the content of `C1`–`C7`; the framework delegates it there explicitly. Its `C6` row requires
only *"a verification report … produced by a role that authored none of the work, disposing every
acceptance point PASS/FAIL on self-obtained evidence"*. It says nothing about the report's verdict
governing, and nothing about supersession. `src/aief_gate/criteria.py` enforced both. **An
instrument ahead of its declaration is the same defect class this project has been bitten by four
times, run backwards**: not a declared property that nothing computes, but a computed property
that nothing declares. A gate that passes on a rule no authority ever ruled has not been passed.

**(b) Supersession was asserted, never proved.** The approvals layer binds each link to content —
`prior_hash` equals the predecessor's `subject_hash`, so a chain cannot be forged without the
bytes. The results layer binds it with `supersedes_seal`, hardened across six passes of
[`VER-009`](../verification/VER-009_Independent_Verification_Execution_Architecture.md). The
verification layer was given the *word* and neither *binding*:

```python
superseded = {s.strip() for d in reports.values()
              for s in str(d.get("supersedes", "")).split(",") if s.strip()}
```

Three consequences, all reachable in one line of one file:

| | |
|---|---|
| **Unbound** | Nothing ties `supersedes: VER-015` to `VER-015`'s bytes. The superseding verifier need never have read the report it retires |
| **Undetectable rewrite** | After supersession the predecessor may be rewritten freely; no check compares anything against it |
| **Global scope** | The set is assembled from *every* report. A Stage 5 report could retire the ECR-D-002 audit, because the filter never asks whether the superseding report covers the same subject |

## 2 · Why this is not a licence to open the gate

The obvious objection is that a supersession relation is exactly what someone who wanted the gate
open would build. It is answered the same way the approval relation answered it.

**The relation cannot launder an unlawful state.** A superseding report must pin the DC-1 of each
report it displaces. If the displaced report is later rewritten, the seal stops reproducing and
`C6` fails — the predecessor is *more* protected after supersession than before, not less.
Supersession must be **declared, never inferred from ordering**, for the reason `APR-019` already
demonstrates. A fork — two live reports retiring the same predecessor — is a failure, not a
preference, because it makes the verified history ambiguous. And a superseding report that does
not itself clear gates exactly as its predecessor did.

**What it does not do.** It does not make `VER-015` or `VER-016` false, and it does not erase
them. Both remain on disk, in full, with their verdicts intact; `VER-016`'s account of what was
wrong is the reason most of this session's work exists. The relation decides only *which* report
`C6` reads, and it answers: the one that has not been superseded, by a successor that proves it
read what it retired.

**The alternative was tested and rejected.** Options B (declare the unsealed behaviour as-is) and
C (no supersession, `C6` requires every naming report to clear) were both presented. C is the
`VER-016` status quo and makes `LC-M04-EXIT` unreachable by construction — the only exits from it
are rewriting an audit verdict, which `VER-016` calls inadmissible and so does this record, or
deleting an adverse report, which is worse. B leaves the laundering route open.

## 3 · Disposition A, as ruled

1. **`GATES.md` gains a ruled section**, *Supersession of verification reports*, sibling to the
   approval-supersession section and written to the same standard: the states, the conditions, why
   it is safe rather than a loosening, and the command that computes it.
2. **`C6`'s criterion row states what it computes** — that the governing report's declared verdict
   governs, and that a superseded report is historical evidence and does not gate.
3. **The seal.** A report declaring `supersedes:` must carry a `supersedes_seal:` list, one entry
   per superseded report, each `<VER-id> <SP> <DC-1 of that report's file>`. A `supersedes`
   without a matching seal entry, a seal that does not reproduce, a seal naming a report that does
   not exist, a fork, a cycle and a self-reference are each a `C6` failure.
4. **Scope.** The superseded set is computed **per gated ECR**, from reports that declare that ECR
   as subject — never globally.
5. **`status` becomes a closed vocabulary.** The field opens with a verdict token, `CLEARED` or
   `NOT CLEARED`, optionally followed by a separator and free commentary. `C6` parses the leading
   token and ignores the commentary, so *"CLEARED — 11 PASS, 0 FAIL"* is read as clearing and the
   `VER-016` F-12 trap is closed. **An unrecognised or absent token fails**, so the vocabulary
   cannot be widened by writing something new.
6. **Adversarial tests**, `tests/test_verification_chain.py`, in the manner of
   `tests/test_approval_chain.py`: each of the six failure modes above is required to fail, and a
   lawful chain is required to pass.

## 4 · Consequences accepted

**`R-015` and `R-016` pin `src/aief_gate/criteria.py`.** Changing it stales them, which is
`VER-016` F-05's class. Both are re-pinned in this session by the roles that own them rather than
left to be discovered.

**`VER-014` does not carry the new fields and does not need them.** It is the sole report on
`ECR-D-001` and supersedes nothing; a report without `supersedes` is unaffected by this ruling.

**No specification artifact changes.** `affected_artifacts` names no path under `spec/**`, so the
frozen set is untouched, `C5` is untouched, and this ECR is outside `C7`'s predicate by
construction — it is dispositioned here regardless, in the same breath in which it is raised,
because leaving it open would be the manoeuvre `C7` exists to prevent.
