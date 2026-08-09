# APR-009 — Registration of `AIEF-AMD-011` in the freeze registry

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the freeze-registry addition required by AIEF-AMD-008 §AMD-21.

```yaml
approval_id:   APR-009
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-08T08:33:10Z
subject_path:  framework/AIEF-AMD-011_Software_Role_Enablement.md
subject_hash:  59ecb5eb922f44a55cc42e51663dae9ee251269790958ee27ad93c1ba2ebaa53
prior_hash:    null                   # not previously registered
scope:         Addition of the named artifact to the FROZEN.md registry at the stated hash,
               under the AMD-21 registration criterion.
session:       S-2026-08-08-05
applied_by:    chief-systems-engineer · S-2026-08-08-05
basis:         the human owner's recorded OQ-13 decision, core/PRECEDENCE.md rank 1
```

---

## Subject

`framework/AIEF-AMD-011_Software_Role_Enablement.md`, at DC-1 normalised SHA-256
`59ecb5eb922f44a55cc42e51663dae9ee251269790958ee27ad93c1ba2ebaa53`.

**This approval is void if the subject changes.** It grants nothing beyond this one path at this one digest, and does not authorise the registration of any future artifact.

## Rationale

AMD-21 rules the registration criterion: *an artifact is registered if it is an authorising instrument for a change to a frozen artifact, or the record of the authority under which such a change was made.* `AIEF-AMD-011` is the authorising instrument for a change to the frozen core partition (LAW-01 clause 2) — the addition of the three `software.*` role artifacts approved in `APR-008` — and the record of the authority for the enabled-agent-set change. An unregistered authorising instrument is the exact exposure AMD-21 closed: the defence for a guarded artifact must itself be guarded, or it proves nothing.

Unlike APR-005 and APR-007, no manifest re-registration accompanies this instrument: `framework/framework.manifest.json` is **not amended** by AIEF-AMD-011 (AMD-37) and its registered digest `ae16ccaca5746b81a2a992841fc1d239fd1c8b0c34657c05611e025a9d8395aa` stands.

## Consequences

| | |
|---|---|
| Registry membership | 26 → **27** |
| `framework/` coverage | 15 of 16 → **16 of 17** (all but the superseded `AIEF-ARCH-001`, ruled out by AMD-21) |
| Freeze-set aggregate | Recomputed under DC-2 over the 27-member registry; recorded in full in `FROZEN.md` § *Aggregate* and `STATE.frozen_set_hash` |
| Standing check | Still none — `V-24` remains declared and emitted, not implemented (OI-V-02). This registry remains verified only by hand until the CMP-BLOCK-004/-005 infrastructure exists |

## Verification status

Applied by `chief-systems-engineer · S-2026-08-08-05` at the direction of the human owner. Under LAW-05 this session cannot verify its own work; the independent cold-context `qa-engineer` audit dispatched by the same directing authority is the mitigating control.

## Authority chain

| | |
|---|---|
| `core/PRECEDENCE.md` rank 1 | The human owner's recorded OQ-13 decision — the authorising basis |
| LAW-01 | Every frozen artifact is registered with a normalised SHA-256 content hash |
| LAW-10 | Approval is an artifact bound to a content hash |
| AIEF-AMD-008 §AMD-21 | The registration criterion this approval applies |
| `project/BINDING.md` | `approval_authority: human-owner` |
