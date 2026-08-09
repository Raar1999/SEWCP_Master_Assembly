# APR-011 — Registration of `AIEF-AMD-012` in the freeze registry

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the freeze-registry addition required by AIEF-AMD-008 §AMD-21.

```yaml
approval_id:   APR-011
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-08T09:06:50Z
subject_path:  framework/AIEF-AMD-012_DC-4_Coverage_of_Enabled_Role_Artifacts.md
subject_hash:  12b7f1b003fd190d99948e378a630d85e405e3c041da31eb8204bb00e702f1d0
prior_hash:    null                   # not previously registered
scope:         Addition of the named artifact to the FROZEN.md registry at the stated hash,
               under the AMD-21 registration criterion.
session:       S-2026-08-08-06
applied_by:    chief-systems-engineer · S-2026-08-08-06
basis:         live human-owner instruction, core/PRECEDENCE.md rank 1
```

---

## Subject

`framework/AIEF-AMD-012_DC-4_Coverage_of_Enabled_Role_Artifacts.md`, at DC-1 normalised SHA-256
`12b7f1b003fd190d99948e378a630d85e405e3c041da31eb8204bb00e702f1d0`.

**This approval is void if the subject changes.** It grants nothing beyond this one path at this one digest, and does not authorise the registration of any future artifact.

## Rationale

AMD-21 rules the registration criterion: *an artifact is registered if it is an authorising instrument for a change to a frozen artifact, or the record of the authority under which such a change was made.* `AIEF-AMD-012` is the authorising instrument for the manifest change approved in `APR-010`. An unregistered authorising instrument is the exact exposure AMD-21 closed: the defence for a guarded artifact must itself be guarded, or it proves nothing (the APR-001/ECR-D-005 lesson).

## Consequences

| | |
|---|---|
| Registry membership | 27 → **28** |
| `framework/` coverage | 16 of 17 → **17 of 18** (all but the superseded `AIEF-ARCH-001`, ruled out by AMD-21) |
| Freeze-set aggregate | Recomputed under DC-2 over the 28-member registry; recorded in full in `FROZEN.md` § *Aggregate* and `STATE.frozen_set_hash` |
| Standing check | Still none — `V-24` remains declared and emitted, not implemented (OI-V-02). This registry remains verified only by hand until the CMP-BLOCK-004/-005 infrastructure exists |

## Verification status

Applied by `chief-systems-engineer · S-2026-08-08-06` at the direction of the human owner. Under LAW-05 this session cannot verify its own work; the independent cold-context `qa-engineer` audit dispatched later this phase by the same directing authority is the mitigating control.

## Authority chain

| | |
|---|---|
| `core/PRECEDENCE.md` rank 1 | Live human instruction — the authorising basis |
| LAW-01 | Every frozen artifact is registered with a normalised SHA-256 content hash |
| LAW-10 | Approval is an artifact bound to a content hash |
| AIEF-AMD-008 §AMD-21 | The registration criterion this approval applies |
| `project/BINDING.md` | `approval_authority: human-owner` |
