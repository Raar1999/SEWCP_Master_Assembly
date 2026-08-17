# APR-038 — Re-binding of `project/GATES.md` after the ECR-Q-015 correction

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-approval requirement of LAW-01 and LAW-10 for the `GATES.md` change made under ECR-Q-015.

```yaml
approval_id:   APR-038
approver:      claude-under-owner-delegation   # NOT a human approval - see AUTHORITY
timestamp:     2026-08-17T00:00:00Z
subject_path:  .ai/project/GATES.md
subject_hash:  30b7e801454292a6eb73f6c7669c101fbba86348a17462a7ab03d92b3a6de8c5
prior_hash:    7900c5fc38d07f1638059c318b3d5ef279f940078f337ce168232d93c2d1b65f
supersedes:    APR-028
ecr:           ECR-Q-015
session:       S-2026-08-17-01
applied_by:    claude-under-owner-delegation · S-2026-08-17-01
scope:         One paragraph of section "Excluded - confirmed by the owner" is corrected: it
               recited that four named ids appear under Blocking in OPEN_ITEMS.md, and two of
               them do not. The original wording is retained struck and attributed, and
               ECR-D-016 is added to the same exclusion on the same ground. NO NORMATIVE
               SENTENCE CHANGES - the C1..C7 criteria, the sealed verification-supersession
               relation ECR-D-012 ruled, the CLEARED/NOT CLEARED vocabulary and every
               exclusion are untouched. AUTHORITY - "Owner-delegated engineering authority
               exercised by Claude" under the owner's written instruction of 2026-08-17. It is
               NOT an actual human approval and is never to be cited as one. Provenance record -
               .ai/project/decisions/DECISIONS_S-2026-08-17-01.md DEC-16.
```

---

**Liveness is not asserted here.** Determine it with `python -m aief_approval verify`.

## Why this approval exists at all

Because the mechanism caught the edit. `GATES.md` is bound by `APR-028` under LAW-10 clause 2,
and the moment the correction landed `aief_approval verify` reported:

```
FAIL   .ai/project/GATES.md  tree=30b7e8014542...  approvals=1
     !! APR-028 [ECR-D-012]: VOID
```

A one-sentence factual correction to an approval-bound artifact is still a change to an
approval-bound artifact. The alternative — reverting the correction to keep the chain green —
would have preserved a false statement in a governing document to protect a digest, which is
the wrong way round. `ECR-Q-015` records the correction; this approval re-binds the artifact.

## Chain

`prior_hash` `7900c5fc…c2d1b65f` is `APR-028`'s `subject_hash` — the state `ECR-D-012`'s
disposition bound and the state the artifact stood at until this session. `APR-028` becomes
`SUPERSEDED-VALID`, not void: it keeps its verdict and its binding to the predecessor state,
under the same supersession semantics `GATES.md` itself declares for verification reports.

## What `ECR-D-012` ruled, and that this does not touch

| | |
|---|---|
| The verification-supersession relation | Declared, sealed to the predecessor's DC-1, scoped per gated ECR, fork- and self-reference-guarded, failing closed with no fallback. **Unchanged** |
| The `CLEARED` / `NOT CLEARED` closed vocabulary | **Unchanged** |
| `C1`–`C7` and their evidence | **Unchanged**; `python -m aief_gate` exits 0 before and after |
| The exclusion list itself | **Unchanged in substance.** `ECR-D-016` is added to it, on the ground already stated there: it is dispositioned, so `C7` is satisfied, and what it blocks is the hardware build rather than this gate |

The 29 trials of `tests/test_verification_chain.py` and the 9 required failures of `VER-017`
W1 attack the relation, not this paragraph, and all pass unchanged.

## Authority chain

| Source | What it supplies |
|---|---|
| LAW-01 | A frozen or approval-bound artifact changes only by an approved ECR and a recorded approval |
| LAW-10 | Approval is an artifact bound to a content hash; it is void when the bound content changes |
| `core/PRECEDENCE.md` rank 1 | The owner's written instruction of 2026-08-17 |
| `ECR-Q-015` | The change request this approval dispositions |
| `ECR-D-012` / `APR-028` | The ruling this artifact carries, and the binding this one succeeds |
