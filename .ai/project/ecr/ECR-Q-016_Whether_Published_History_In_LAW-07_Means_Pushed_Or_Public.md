# ECR-Q-016 — `LAW-07` clause 6 forbids rewriting *published* history and the framework never says whether "published" means pushed or public

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised at `S-2026-08-18-02` while planning the `ECR-D-018` sanitization, because the answer
> determines whether that act needs an override at all. Filed under `LAW-12`: the ambiguity is
> **not** resolved by assumption.

```yaml
ecr_id:       ECR-Q-016
class:        Q                      # query - an undefined term in a BLOCKING law
raised_by:    repository-engineer · S-2026-08-18-02
status:       OPEN
disposition:  null                   # LAW-02 clause 3 - only the chief-systems-engineer rules
ruled_by:     null
ruled_at:     null
instrument:   null
approval:     null
affected_artifacts:
  - .ai/core/laws/LAW-07_git_configuration.md
  - .ai/core/validation/CHECKS.md
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-18T00:00:00Z
related:      ECR-D-018, LAW-07, V-22
```

## 1 · Class

**Q — query.** `LAW-07` clause 6 reads, in full:

> **6. Published history is never rewritten.**

`V-22`, severity **BLOCKING**, restates it as a checked property: *"…published history is not
rewritten…"*. Neither the law, nor `V-22`, nor `AIEF-FRZ-001`, nor any of the fifteen
amendments defines **published**. Two readings are available and they are not equivalent:

| Reading | "Published" means | Does it bind this repository today? |
|---|---|---|
| **Narrow** | made publicly visible | **No.** `STATE.md` records the repository as PRIVATE; the visibility gate is unclosed |
| **Broad** | pushed to any remote | **Yes.** `origin/main` is at `f8ff028` on a private GitHub remote |

## 2 · Evidence

```
$ git remote -v
origin  https://github.com/Raar1999/SEWCP_Master_Assembly.git (fetch/push)
$ git rev-parse origin/main
f8ff028d56aee3004b5d41eb1a3d5c3e8f579270
```

`STATE.md` `next_action`: *"TWO OWNER GATES, closable by no session: repository PRIVATE, no
GitHub Release object."* `ENGINEERING.md` §7 says `Repository | **PUBLIC.**`, which is a
separate defect recorded at `ECR-D-018` §2.3 — and which is itself evidence that the two
senses are being conflated in this repository's own prose.

## 3 · Impact — **none on the act, and that is why work proceeds**

Under the **narrow** reading, clause 6 does not bind and the `ECR-D-018` rewrite needs no
override. Under the **broad** reading it binds, and the owner's rank-1 live instruction of
`S-2026-08-18-02` overrides it, recorded at `APR-039` per `PRECEDENCE` §4 and `LAW-10`
clause 4.

**The outcome is invariant under both readings**, so `LAW-02` clause 1 applies — *"work
proceeds under the ruling"* — and this query blocks nothing. It is filed because the term is
undefined in a BLOCKING check and the next session to meet it should not have to re-derive
that the answer did not matter this time. It may matter next time.

## 4 · Requested action

Rule which sense clause 6 carries, and state it in the amendment that rules it. If the broad
sense is intended, `V-22`'s implementation — when one is written, `CMP-BLOCK-005` — needs a
declared notion of what makes history published, since a check cannot observe a remote's
visibility from the working tree alone.

Two secondary clauses were engaged by the same act and are recorded here for the same reason:

- **clause 7**, *"Tags are annotated and never moved"* — `v0.11.0` must be re-pointed at the
  rewritten commit. Its annotation, tagger and timestamp are preserved byte-for-byte; only the
  `object` line changes. Whether re-pointing under a rank-1 override is "moving" is the same
  species of question.
- **clause 8**, *"Force push is prohibited unless explicitly authorised by the framework"* —
  note **by the framework**, not by the owner. No push is performed by this session, so the
  clause is not yet reached; it will be reached at the publication gate.
