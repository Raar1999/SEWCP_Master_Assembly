# APR-031 - Cooling Plate bracket taps re-placed to r = 150, 88/122 deg

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.

```yaml
approval_id:   APR-031
approver:      claude-under-owner-delegation   # NOT a human approval - see APR-029 scope
timestamp:     2026-08-11T00:00:00Z
subject_path:  spec/01_SEWCP-200_Cooling_Plate.md
subject_hash:  a3afa3eb41ee2aba7181fc4ae778a29d12c396194f1252640cc4e02e4b9f2230
prior_hash:    9e825580133ec41c9d44236b68ebbb22d02285fa1be11e21e3daa7a2059b6956
supersedes:    APR-029
ecr:           ECR-Q-012
session:       S-2026-08-11-05
scope:         One cell only. The CP-IF-8 bracket taps move from r = 137,
               88.27/121.73 deg to r = 150, 88/122 deg. The first placement -
               RF-IF-3's literal window - intersects the 90/120 deg choke
               slots; the ACC-VOL build check caught it and the feasibility
               sweep proved the whole +/-40 mm window occupied. Provenance -
               DECISIONS_S-2026-08-11-05 DEC-02 addendum. Owner-delegated
               engineering authority exercised by Claude.
```

**Liveness is not asserted here.** Determine it with python -m aief_approval verify.
