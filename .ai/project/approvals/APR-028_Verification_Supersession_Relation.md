# APR-028 - The C6 verification-supersession relation and verdict vocabulary (ECR-D-012)

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.

```yaml
approval_id:   APR-028
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-10T00:00:00Z
subject_path:  .ai/project/GATES.md
subject_hash:  7900c5fc38d07f1638059c318b3d5ef279f940078f337ce168232d93c2d1b65f
prior_hash:    null
supersedes:    null
ecr:           ECR-D-012
session:       S-2026-08-10-04
scope:         The C6 criterion row, the section 'Supersession of verification reports',
               and the sentence describing what the checker decides. The active-gate
               status labels are removed rather than updated - this file no longer
               asserts whether the gate is passed. No criterion is added or removed,
               and C1..C5 and C7 are untouched.
```

---

**Liveness is not asserted here.** Determine it with `python -m aief_approval verify`.

## What is approved

**`ECR-D-012` disposition A**, on `VER-016` findings F-01 (HIGH) and F-12 (LOW). `VER-016` named
the remedy in terms — *"an instrument change to `C6` (an ECR and an approval)"* — and this is the
approval half of it.

| | Before | After |
|---|---|---|
| Supersession of verification reports | Computed by `criteria.py`, **declared nowhere**, bound to nothing, assembled globally | Ruled in `GATES.md`; **sealed** to the predecessor's DC-1; scoped per gated ECR |
| A report's declared verdict | Whole-string scan for `FAIL` / `NOT CLEARED` / `NOT VERIFIED` | Closed vocabulary: `status` opens with `CLEARED` or `NOT CLEARED`; unrecognised fails |
| Governing report underivable | Fell back to reading every naming report | **Fails closed** — no fallback |
| Active-gate status | Two hand-written labels | Removed; the gate computes |

## Why this is not a licence to open the gate

The objection answers itself if the relation is read: **it makes an adverse report harder to
suppress, not easier.** Before this ruling, `VER-015` could have been quietly edited or deleted
and nothing would have noticed. Under it, a report that retires a predecessor must pin that
predecessor's bytes, and any later rewrite of the retired report **fails `C6`**. Supersession
also does not soften a verdict: a superseding report that declares `NOT CLEARED` gates exactly as
its predecessor did, and `VER-015` and `VER-016` remain on disk in full, verdicts intact.

Options **B** (declare the unsealed behaviour as written) and **C** (no supersession at all) were
presented in the decision pause and not approved. **C** is the state `VER-016` measured and called
*"structurally unreachable"*: its only exits are rewriting an audit verdict or deleting an audit,
both of which this approval refuses as firmly as `VER-016` did.

## What this approval found that was not in the raised finding

Applying the closed vocabulary immediately exposed a defect **in the opposite direction** to
F-12, which `VER-016` had not found and had explicitly ruled out — it recorded the old predicate
as *"fail-safe"*.

**`VER-014` declares `status: ECR-D-001 NOT CLOSED`.** That string contains none of `FAIL`,
`NOT CLEARED` or `NOT VERIFIED`, so the old scan read it as clearing and **`C6` passed
`ECR-D-001`** — while `VER-014` §6 reads *"`ECR-D-001` is NOT CLOSED after four rounds.
`LC-M04-EXIT` `C6` is not satisfied for it"*, and `OPEN_ITEMS_REGISTER.md` row `OI-V-11` says the
same. The index was more truthful than the instrument. Under the vocabulary ruled here,
`ECR-D-001` fails `C6` until a governing report clears it, which is what its own evidence has
said all along.

This is recorded as the finding it is: **the gate has been reporting a criterion satisfied that
its own cited evidence contradicted**, and the repair was found by tightening a rule rather than
by reading the report.

## Consequences accepted

`R-015` and `R-016` pin `src/aief_gate/criteria.py`; both are re-pinned this session by the roles
that own them rather than left to be discovered, which is `VER-016` F-05's class. `GATES.md`
becomes an approval-bound artifact: every future edit to it needs a superseding approval, which is
the intended effect for a file carrying human-ruled gate criteria, and is why its two
self-invalidating status labels were removed in the same change.
