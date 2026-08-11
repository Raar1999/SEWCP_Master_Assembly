# APR-032 - RF bracket volume: RF-IF-3 mounting window corrected

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.

```yaml
approval_id:   APR-032
approver:      claude-under-owner-delegation   # NOT a human approval - see APR-030 scope
timestamp:     2026-08-11T00:00:00Z
subject_path:  spec/08_SEWCP-900_RF_Feedthrough_Bracket.md
subject_hash:  710f6e14bf8b40498a4ec91ea65b760fc55eea99507513a93feb85bb6aa55414
prior_hash:    b69b0c4859bce91505702354e5cacc9af8e4773b395b6c5694fa63142b12b289
supersedes:    APR-030
ecr:           ECR-Q-012
session:       S-2026-08-11-05
scope:         Two cells only. RF-IF-3 mounting re-specified at r = 150,
               105 +/- 17 deg (the former O274 BC +/- 40 mm window is fully
               occupied by the 30-deg choke stations and the land - proven by
               the ACC-VOL collision and the feasibility sweep, DEC-02
               addendum); SB-D03 follows. Owner-delegated engineering
               authority exercised by Claude.
```

**Liveness is not asserted here.** Determine it with python -m aief_approval verify.
