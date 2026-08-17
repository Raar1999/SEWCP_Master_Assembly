# ECR-Q-015 — `GATES.md`'s exclusion paragraph names a section two of its four ids no longer sit in

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised by the `OI-V-13` independent cold-context audit as **FIND-10 (MINOR)**; filed at `S-2026-08-17-01`.

```yaml
ecr_id:       ECR-Q-015
class:        Q                      # query - a true exclusion stated against a stale index location
raised_by:    qa-engineer · OI-V-13 independent audit, filed by repository-engineer · S-2026-08-17-01
status:       DISPOSITIONED
disposition:  Correct the sentence in place and re-bind GATES.md under APR-038. The exclusion itself is unchanged; only the index location it recites was stale
ruled_by:     claude-under-owner-delegation (owner-delegated engineering authority, mission 2026-08-17; NOT a human approval)
ruled_at:     2026-08-17T00:00:00Z
instrument:   .ai/project/decisions/DECISIONS_S-2026-08-17-01.md DEC-16
approval:     APR-038
affected_artifacts:
  - .ai/project/GATES.md
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-17T00:00:00Z
related:      ECR-D-012, ECR-D-006
```

## 1 · Class

**Q — query.** `GATES.md` § *Excluded — confirmed by the owner* opened:

> `ECR-D-006`, `CMP-BLOCK-004`, `CMP-BLOCK-005` and `C-4` appear under `Blocking` in
> `OPEN_ITEMS.md` but are **not** criteria of this gate.

Two of the four ids do not appear under `Blocking`. `ECR-D-006` was moved to § *Open, not
blocking* by `S-2026-08-11-06`, and the sentence was not followed through. `C-4` is closed by
`DEC-11` of this session.

**The exclusion is correct and is not in question.** What is stale is the recital of *where in
the index* the excluded ids sit — a fact the exclusion never depended on, which is exactly why
nobody noticed.

## 2 · Evidence

```
$ sed -n '/^## Blocking/,/^##/p' .ai/project/OPEN_ITEMS.md
CMP-BLOCK-004
CMP-BLOCK-005
C-4
```

Three ids, one of which the audit's own baseline shows was already about to move. `ECR-D-006`
appears in § *Open, not blocking*, at line 45 of the index.

## 3 · Impact

**None on any gate result.** `aief_gate` reads the ECR records directly and not this
paragraph — `_c7`'s comment records why in terms (`VER-015` F-18: reading only the `Blocking`
section made `C7` evadable). `C1`–`C7` are unaffected and continue to pass.

The impact is on a reader, and it is the impact this repository takes seriously: a governing
document asserting a repository fact that is false. It is the `FIND-9` class in a second file.

## 4 · Requested action and disposition

Correct the sentence, retain the original wording struck and attributed, and state the
exclusion in terms that do not depend on which index section an id currently occupies.
`ECR-D-016` is added to the same exclusion on the same ground.

**`GATES.md` is bound by `APR-028` under LAW-10, so correcting it voids that binding** — and it
did, immediately: `aief_approval verify` reported `APR-028 [ECR-D-012]: VOID` the moment the
edit landed. That is the mechanism working, not a defect, and it is why this ECR exists rather
than the edit being made silently. Re-bound at the corrected digest by
[`APR-038`](../approvals/APR-038_Rebind_GATES_After_ECR-Q-015.md), which chains from
`APR-028`'s `subject_hash`. **`ECR-D-012`'s ruling, the sealed supersession relation and the
`CLEARED`/`NOT CLEARED` vocabulary are untouched** — no normative sentence of `GATES.md`
changes.
