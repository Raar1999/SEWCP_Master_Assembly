# APR-003 — Registration of eight `framework/` artifacts in the freeze registry

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the freeze-registry scope expansion ruled by AIEF-AMD-008 §AMD-21.

```yaml
approval_id:   APR-003
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-08T02:36:52Z
subject_path:
  - framework/AIEF-ADR-001_Authority_Decision_Record.md
  - framework/AIEF-ADR-002_Authority_Decision_Record.md
  - framework/AIEF-AMD-003_Architecture_Amendments_OI-F-01_OI-F-02.md
  - framework/AIEF-AMD-004_Repository_Engineer_Autonomy.md
  - framework/AIEF-AMD-005_Host_Bootstrap_Artifacts.md
  - framework/AIEF-AMD-006_Mechanical_CAD_Engineer.md
  - framework/AIEF-AMD-007_Compiler_Stage_State_Field.md
  - framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md
subject_hash:
  - 935d169d0bbfd11c9d73c9f256de710d3b67477ebc1c458b6aa07c5e6a2362cb
  - e79e9fc8b0e0b9e07493d50c203084391802eb096ee2239693c229efdec696f3
  - d1d2cf76425974cc8b7804005d7e5a52f90ad8be16edfbd5480c03709fcc5e4b
  - 9171059e930cca9365abd0c2bad5db01fa3a790733c6f663ef93cc79de255dac
  - f8a4ab53eec480e951fe17cb6590b16fd311ce4e2639a83d2d8bab6fd05f946a
  - ece7c0c780ffd0c006f508ddcc624a416d1f11ff24d4addb3dc9be61c36f38e9
  - 860a1c7e8f18a05d032fe21cd2dfaeac4580765de1d225f9c260def8484caa9e
  - 192ff86128dadfc8382f1894e1a38713f7321ee83aff7891d7e885c31c9dd71e
prior_hash:    null                   # none of the eight was previously registered
scope:         Addition of the eight named artifacts to the FROZEN.md registry at the
               stated hashes, and declaration of the registry's covered scope.
               AIEF-AMD-008 ruling AMD-21.
session:       S-2026-08-08-02
applied_by:    chief-systems-engineer · S-2026-08-08-02
basis:         live human-owner instruction, core/PRECEDENCE.md rank 1
```

---

## Subject

Eight artifacts, each at its DC-1 normalised SHA-256. **Each is named individually and bound individually.**

| # | Path | DC-1 digest | Class |
|---|---|---|---|
| 1 | `framework/AIEF-ADR-001_Authority_Decision_Record.md` | `935d169d0bbfd11c9d73c9f256de710d3b67477ebc1c458b6aa07c5e6a2362cb` | Authority record |
| 2 | `framework/AIEF-ADR-002_Authority_Decision_Record.md` | `e79e9fc8b0e0b9e07493d50c203084391802eb096ee2239693c229efdec696f3` | Authority record |
| 3 | `framework/AIEF-AMD-003_Architecture_Amendments_OI-F-01_OI-F-02.md` | `d1d2cf76425974cc8b7804005d7e5a52f90ad8be16edfbd5480c03709fcc5e4b` | Amendment |
| 4 | `framework/AIEF-AMD-004_Repository_Engineer_Autonomy.md` | `9171059e930cca9365abd0c2bad5db01fa3a790733c6f663ef93cc79de255dac` | Amendment |
| 5 | `framework/AIEF-AMD-005_Host_Bootstrap_Artifacts.md` | `f8a4ab53eec480e951fe17cb6590b16fd311ce4e2639a83d2d8bab6fd05f946a` | Amendment |
| 6 | `framework/AIEF-AMD-006_Mechanical_CAD_Engineer.md` | `ece7c0c780ffd0c006f508ddcc624a416d1f11ff24d4addb3dc9be61c36f38e9` | Amendment |
| 7 | `framework/AIEF-AMD-007_Compiler_Stage_State_Field.md` | `860a1c7e8f18a05d032fe21cd2dfaeac4580765de1d225f9c260def8484caa9e` | Amendment |
| 8 | `framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md` | `192ff86128dadfc8382f1894e1a38713f7321ee83aff7891d7e885c31c9dd71e` | Amendment |

**This approval is void if any one of the eight changes.** It grants nothing beyond these eight paths at these eight digests. It is not a blanket approval over `framework/`, and it does not authorise the registration of any future artifact — each future registration needs its own record.

## Why one instrument for eight artifacts

LAW-10 requires an approval to **name what it approved** and to be **invalidated when the bound content changes**. Both hold here: every path is named, every digest is bound, and the approval is void on any change to any of them. Splitting this into eight files would satisfy the same two tests eight times with no additional evidentiary strength, and would obscure that the eight additions are one ruling — AMD-21 — applied uniformly by one criterion.

## Authorising basis

The human owner, `BINDING.approval_authority: human-owner`, issued a live instruction authorising this work, including: *"If an amendment is required, author the appropriate ECR/amendment and update the manifest/source of truth."*

`core/PRECEDENCE.md` rank 1. LAW-10 clause 4 requires the override be recorded before dependent work is committed. This artifact is that record.

## Rationale

`FROZEN.md` registered 5 of the 13 `framework/` artifacts present at the time of the QA audit. Unregistered were `AIEF-AMD-003` … `AIEF-AMD-007`, `AIEF-ADR-001`, `AIEF-ADR-002` and `AIEF-ARCH-001`.

**The unguarded set included the three amendments that `APR-001` cites as its own authorising basis.** `APR-001` proves the manifest's divergence was authorised by naming AMD-004, AMD-006 and AMD-007. If those documents can change without detection, `APR-001` proves nothing. ECR-D-005 is the empirical demonstration: the guarded artifact drifted across three releases, and what remained as the defence was itself unguarded.

AMD-21 rules the criterion:

> An artifact is registered if it is an **authorising instrument** for a change to a frozen artifact, or the **record of the authority** under which such a change was made.

Applied: five amendments plus this session's AMD-008 are authorising instruments; two Authority Decision Records are records of the A4 authority under which AMD-01 … AMD-08 were made, and LAW-06 requires the authority chain be traceable — a record of authority that can change silently is not a record.

## Explicitly not registered

`framework/AIEF-ARCH-001_AI_Engineering_Framework_Architecture.md` is **not** registered, and this is a decision rather than an omission.

| Evidence | Source |
|---|---|
| *"Supersedes: AIEF-ARCH-001 Rev A (architecture)"* | `AIEF-FRZ-001` header |
| *"AIEF-ARCH-001 §7.4 is superseded."* | `AIEF-AMD-001` §AMD-04 |
| *"Design only. No framework files are generated by this document."* | `AIEF-ARCH-001` header |

It authorises nothing and is cited by nothing as a live authority. Registering it would assert a currency it does not have.

## Consequences

| | |
|---|---|
| Registry membership | 16 → **24** |
| `framework/` coverage | 5 of 13 → **13 of 14** (all but the superseded `AIEF-ARCH-001`) |
| Freeze-set aggregate | Recomputed under DC-2 over the new membership; recorded in `FROZEN.md` and `STATE.frozen_set_hash` |
| Standing check | **None yet.** `V-24` is declared by AMD-19 as a Stage 5 requirement and is not implemented. Until Stage 5 runs, this registry remains verified only by hand — recorded as OI-V-02 |

## Verification status

Ruled and applied by the same authority, `chief-systems-engineer` · `S-2026-08-08-02`, at the direction of the human owner. Under LAW-05 this session cannot verify its own work. **Independent confirmation is outstanding and recorded as OI-V-03.**

Every digest above is reproducible by a third party from the repository alone, using the DC-1 definition in `metadata.reproducible.digest_constructions.per_artifact`.

## Authority chain

| | |
|---|---|
| `core/PRECEDENCE.md` rank 1 | Live human instruction — the authorising basis |
| LAW-01 | Every frozen artifact is registered with a normalised SHA-256 content hash |
| LAW-06 | Every artifact cites its authority; the chain must be traceable |
| LAW-10 | Approval is an artifact bound to a content hash; freeze and thaw are human authority only |
| `project/BINDING.md` | `approval_authority: human-owner` |
| AIEF-AMD-008 §AMD-21 | The ruling this approval enacts |
