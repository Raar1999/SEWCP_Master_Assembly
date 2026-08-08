# APR-005 — Registration of `AIEF-AMD-009` in the freeze registry

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the freeze-registry addition required by AIEF-AMD-008 §AMD-21.

```yaml
approval_id:   APR-005
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-08T05:51:32Z
subject_path:  framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md
subject_hash:  86c8be7f0eafb441c55ad5d5033f6e8e4e684350da262557539e6291b68f2c97
prior_hash:    null                   # not previously registered
scope:         Addition of the named artifact to the FROZEN.md registry at the stated hash,
               under the AMD-21 registration criterion.
session:       S-2026-08-08-03
applied_by:    chief-systems-engineer · S-2026-08-08-03
basis:         live human-owner instruction, core/PRECEDENCE.md rank 1
```

---

## Subject

`framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md`, at DC-1 normalised SHA-256
`86c8be7f0eafb441c55ad5d5033f6e8e4e684350da262557539e6291b68f2c97`.

**This approval is void if the subject changes.** It grants nothing beyond this one path at this one digest, and does not authorise the registration of any future artifact.

## Rationale

AMD-21 rules the registration criterion: *an artifact is registered if it is an authorising instrument for a change to a frozen artifact, or the record of the authority under which such a change was made.* `AIEF-AMD-009` is the authorising instrument for the manifest change approved in `APR-004`. An unregistered authorising instrument is the exact exposure AMD-21 closed: the defence for a guarded artifact must itself be guarded, or it proves nothing (the APR-001/ECR-D-005 lesson).

## Consequences

| | |
|---|---|
| Registry membership | 24 → **25** |
| `framework/` coverage | 13 of 14 → **14 of 15** (all but the superseded `AIEF-ARCH-001`, ruled out by AMD-21) |
| Freeze-set aggregate | Recomputed under DC-2 over the 25-member registry; recorded in full in `FROZEN.md` § *Aggregate* and `STATE.frozen_set_hash` |
| Standing check | Still none — `V-24` remains declared, not implemented (OI-V-02). This registry remains verified only by hand until Compiler Stage 5 runs |

## Verification status

Applied by `chief-systems-engineer` · `S-2026-08-08-03` at the direction of the human owner. Under LAW-05 this session cannot verify its own work; the independent cold-context `qa-engineer` audit dispatched by the same instruction is the mitigating control.

## Authority chain

| | |
|---|---|
| `core/PRECEDENCE.md` rank 1 | Live human instruction — the authorising basis |
| LAW-01 | Every frozen artifact is registered with a normalised SHA-256 content hash |
| LAW-10 | Approval is an artifact bound to a content hash |
| AIEF-AMD-008 §AMD-21 | The registration criterion this approval applies |
| `project/BINDING.md` | `approval_authority: human-owner` |
