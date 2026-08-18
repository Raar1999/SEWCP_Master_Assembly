# APR-039 — Rank-1 override of `LAW-07` clauses 6, 7 and 8 for the `ECR-D-018` publication-safety sanitization

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies `core/PRECEDENCE.md` §4 — *"A rank-1 override … must be recorded as an approval artifact before dependent work is committed"* — and `LAW-10` clause 4, *"A verbal override must be recorded before dependent work is committed."*

```yaml
approval_id:   APR-039
approver:      human-owner
timestamp:     2026-08-18T00:00:00Z
subject_path:  .ai/project/ecr/ECR-D-018_Local_Account_Name_Becomes_New_Public_Information_At_Publication.md
subject_hash:  764bf92a654a93f6a8377f046cd55aab86addb52d1ab71086cbc37dfdd32d525
prior_hash:    null                   # not previously approved
ecr:           ECR-D-018
session:       S-2026-08-18-02
applied_by:    repository-engineer · S-2026-08-18-02
scope:         Authorises exactly one act - rewriting reachable git history to replace the local
               Windows account-name segment with the neutral placeholder <user>, preserving
               separator form and every other byte - and the consequent re-pointing of the
               annotated tag v0.11.0 at the rewritten release commit. Overrides LAW-07 clauses
               6, 7 and 8 for this act and no other. Grants NO authority to push, to force-update
               any remote ref, to merge, to create a GitHub Release object, or to change
               repository visibility. LAW-07 clauses 1-5 are not overridden and are not touched.
```

---

**Liveness is not asserted here.** Determine it with `python -m aief_approval verify`.

## Subject

`.ai/project/ecr/ECR-D-018_Local_Account_Name_Becomes_New_Public_Information_At_Publication.md`,
at DC-1 normalised SHA-256

```
764bf92a654a93f6a8377f046cd55aab86addb52d1ab71086cbc37dfdd32d525
```

**This approval is void if the subject changes.** It authorises the one transformation that ECR
declares, in the scope that ECR declares, and nothing beyond it.

## Authority

**The human owner's own written instruction of `S-2026-08-18-02`**, `core/PRECEDENCE.md` rank 1
— *live human instruction*. This is **not** an owner-delegated decision taken by an agent and
must never be cited as one. The instruction chose the sanitization option in terms (*"I CHOOSE
OPTION C"*), set the transformation, enumerated what must not be altered, and fixed the stop
line: *"stop before force-pushing or making the repository public."*

Provenance record: [`../decisions/DECISIONS_S-2026-08-18-02.md`](../decisions/DECISIONS_S-2026-08-18-02.md)
DEC-22, DEC-23 and DEC-24.

## What is overridden, stated plainly

| Clause | Text | Engaged how |
|---|---|---|
| `LAW-07` 6 | *Published history is never rewritten* | 25 commits are rewritten. Whether *"published"* even reaches a private remote is undefined and is raised as `ECR-Q-016`; the override is recorded so the act is lawful under **either** reading |
| `LAW-07` 7 | *Tags are annotated and never moved* | `v0.11.0` is re-pointed at the rewritten release commit. It **remains annotated**; tagger, timestamp and the full annotation message are preserved byte-for-byte, and only the `object` line changes |
| `LAW-07` 8 | *Force push is prohibited unless explicitly authorised by the framework* | **Not reached by this session.** No push is performed. The required force-update is computed and reported for the owner at the publication gate |

`V-22`, severity BLOCKING, restates clause 6 as a checked property. **No check is weakened,
skipped, relaxed or deleted to accommodate this override.** `V-22` has no executable
implementation in this repository — `CMP-BLOCK-005` — and that fact is recorded here rather
than relied on: the override stands on rank-1 authority, not on the absence of an enforcer.

## What is preserved, and verified rather than asserted

Author identity, committer identity, author and committer timestamps, commit messages, tag
annotations with tagger and date, file modes, path names, and every byte of every file except
the approved account-name substitution. The four approval-provenance commits `d07e931`,
`655aa75`, `be75798` and `8546960` all precede the first affected commit and are **not
rewritten**; the `ECR-D-006` attribution and the `APR-002`/`-004`/`-005` subject recovery are
untouched.

Every claim in that paragraph is measured after the act by
[`../results/R-032.md`](../results/R-032.md) and recorded at
[`../ledger/SEG-0000/L-0000008`](../ledger/SEG-0000/L-0000008), never asserted from this file.

## What this approval does not grant

It does not approve publication. It does not approve a push, a merge, a remote force-update, a
GitHub Release object, or a visibility change. It does not certify the repair — `LAW-05` bars
the performing session from verifying its own work, and the independent cold-context round is
recorded as **owed**.
