# ECR-D-017 — `metadata.license` is a release placeholder, and two clauses AMD-015 amended do not cite it

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised at session `S-2026-08-17-01` — the first at which a public release is actually
> imminent, which is what makes a `TBD-at-release` value a defect rather than a plan.

```yaml
ecr_id:       ECR-D-017
class:        D                      # defect - a frozen artifact carries a placeholder into a public release
raised_by:    repository-engineer · S-2026-08-17-01
status:       DISPOSITIONED
disposition:  A - two actions. Set metadata.license to the ratified dual-license expression; append the AIEF-AMD-015 citation to the two authority fields it amended. Re-register, recompute DC-2, re-emit Stage 6
ruled_by:     claude-under-owner-delegation (owner-delegated repository and license authority, mission 2026-08-17; NOT a human approval)
ruled_at:     2026-08-17T00:00:00Z
instrument:   .ai/project/decisions/DECISIONS_S-2026-08-17-01.md DEC-11 and DEC-15
approval:     APR-037
affected_artifacts:
  - framework/framework.manifest.json
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-17T00:00:00Z
related:      C-4, ECR-D-006
```

## 1 · Class

**D — defect, in two parts, both in one artifact.**

**(a) `metadata.license` reads `"TBD-at-release"`.** It is release day. A frozen artifact that
will be published to a public repository states that its own licensing is unresolved, while the
repository it describes now carries a ratified `LICENSE` at its root. That is a stale
release-state statement in the one file the framework calls *"the single source of truth from
which the entire framework is generated"*.

**(b) Two clauses `AIEF-AMD-015` amended do not name it in their `authority`.**
`…digest_constructions.core_aggregate.authority` and
`…budget_measurement_record.authority` were both amended by `AIEF-AMD-015`, and both still
cite only AMD-010/012/013/014. `AIEF-AMD-012`, `-013` and `-014` each extended the `authority`
field of every clause they touched — verifiable in the `8546960 → baf843a` diff. AMD-015 broke
the pattern, and its citations live only inside the clause bodies. Raised by the `OI-V-13`
independent cold audit as **FIND-11**.

## 2 · Evidence

```
$ python -c "import json; print(json.load(open('framework/framework.manifest.json'))['metadata']['license'])"
TBD-at-release

$ … ['metadata']['reproducible']['digest_constructions']['core_aggregate']['authority']
AIEF-AMD-010 AMD-27, disposing Stage 6 pre-flight OPEN-QUESTION 4 and OPEN-QUESTION 5;
coverage extended to enabled-role agent artifacts by AIEF-AMD-012 AMD-39, disposing OI-C-06
                                                    # no AIEF-AMD-015, which amended lock_serialisation
```

`C-4` has recorded the repository-level placeholder since Release 0.1 preparation. **This is
its second instance, in a different partition, and it was never registered** — `C-4` names
`LICENSE`, not the manifest. Closing `C-4` without this would have left the repository
licensed and the framework it ships still saying otherwise.

## 3 · Impact

**Bounded and entirely inside `framework/framework.manifest.json`.**

- No `spec/**` artifact, no CAD model, no drawing, no deliverable and no `.ai/core/**` file is
  touched, so **DC-4, `MANIFEST.lock.aggregate_digest` and `BINDING.core_digest_pin` do not
  move and B2a is unaffected** — the covered set is `.ai/core/**` plus three root files, and
  the manifest is in none of it.
- `FROZEN.md` registers this path, so its DC-1 moves and the registry row must be re-registered
  under an approval, exactly as `ECR-D-005` and `ECR-D-006` were. `V-24` fails until it is, and
  that is the mechanism working.
- `core/MANIFEST.lock.build_provenance.source_manifest_dc1` pins the manifest's DC-1, so the
  lock becomes stale and **Stage 6 must be re-emitted** under the standing `OQ-14`
  authorization. The re-emission changes `source_manifest_dc1` and the run-scoped
  `budget_measurement` fields, and nothing else — `aggregate_digest` is computed over content
  this ECR does not touch.
- `LC-M04-EXIT` is unaffected: `GATES.md` excludes this path from the gate by name.

## 4 · Requested action

**(a)** Rule the license, or record that it cannot be ruled. **(b)** Cite AMD-015 where AMD-015
amended.

**Alternatives for (a):**

| | Verdict |
|---|---|
| **A — set it to the ratified repository expression, `MIT AND CC-BY-4.0`** | **SELECTED.** The manifest describes a framework distributed *from this repository*, under this repository's licence. Any other value would put the framework and its own repository under different terms with no instrument creating that split |
| B — leave `TBD-at-release` and note it in the release documentation | Rejected. A note beside a placeholder is not a resolution, and §21 of the release brief forbids shipping a stale release-state statement. The whole point of `C-4` is that absence of a licence is not an implicit grant |
| C — set it to `MIT` alone | Rejected. It would be false: the framework's own artifacts — `AIEF-FRZ-001`, the fifteen amendments, `.ai/**` — are documents, and the repository licenses documents under CC-BY-4.0 |
| D — a separate licence for the framework distributable | Rejected. It is a real option for a framework intended to travel independently, and it is a decision with consequences beyond this release. Nothing requires it now, and inventing a second licensing regime on release day is how a repository acquires a licensing defect rather than resolving one |

**Alternatives for (b)** were not enumerated: an amendment citing itself where it amended is a
correction of an omission, not a choice between options.

## 5 · Disposition A, as executed

| Action | Change |
|---|---|
| 1 | `metadata.license`: `"TBD-at-release"` → `"MIT AND CC-BY-4.0 - see LICENSE at the repository root, which declares the path boundary. Code MIT; documents, engineering artifacts and generated design data CC-BY-4.0. Ratified S-2026-08-17-01 under owner-delegated licence authority (DECISIONS_S-2026-08-17-01 DEC-11), closing C-4"` |
| 2 | `…core_aggregate.authority`: append `"; lock_serialisation member order amended and the measured quantity scoped to the boot-read prefix by AIEF-AMD-015 AMD-54 and AMD-55, disposing ECR-D-014"` |
| 3 | `…budget_measurement_record.authority`: append `"; lock_self_measurement scoped to the boot-read prefix by AIEF-AMD-015 AMD-54, disposing ECR-D-014"` |

**Three leaves. Zero removals. No `token_cap`, no `files[]` entry, no dependency edge, no
`validation` entry and no digest construction changed** — none of the three values is read by
any construction, and all three are prose. Verified by structural diff, not by inspection.

Bound by [`APR-037`](../approvals/APR-037_Reregister_Framework_Manifest_ECR-D-017.md).
Registry re-registered at the measured post-change digest; `DC-2` recomputed;
`STATE.frozen_set_hash` follows; Stage 6 re-emitted so `source_manifest_dc1` names the artifact
that now exists.
