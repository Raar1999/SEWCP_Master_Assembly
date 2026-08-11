# APR-029 - Cooling Plate: RF-hanger bracket taps and FSW rib-pass tool envelope

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.

```yaml
approval_id:   APR-029
approver:      claude-under-owner-delegation   # NOT a human approval - see scope
timestamp:     2026-08-11T00:00:00Z
subject_path:  spec/01_SEWCP-200_Cooling_Plate.md
subject_hash:  9e825580133ec41c9d44236b68ebbb22d02285fa1be11e21e3daa7a2059b6956
prior_hash:    55b47ca30eeac99ca231d960a1066411b827bf6da139d5e7d178db6a182c3a39
supersedes:    APR-020
ecr:           ECR-Q-011, ECR-Q-012
session:       S-2026-08-11-05
scope:         Two cells only. CP-IF-8 gains the two M6 x 12 bracket taps at r = 137,
               88.27/121.73 deg (RF-IF-3 hanger mounting, ECR-Q-012 DEC-02). Section 6
               step 5 gains the FSW internal-rib tool-envelope constraint (ECR-Q-011
               DEC-03). No other byte changes. AUTHORITY - this approval records
               "Owner-delegated engineering authority exercised by Claude" under the
               owner's written delegation of 2026-08-11 (mission section 1). It is NOT
               an actual human approval and is never to be cited as one; the BINDING
               approval_authority (human-owner) delegated its exercise for this run.
               Provenance record - .ai/project/decisions/DECISIONS_S-2026-08-11-05.md.
```

---

**Liveness is not asserted here.** Determine it with `python -m aief_approval verify`.

## What is approved

1. **ECR-Q-012 / DEC-02.** RF-IF-3 (`spec/08`) mounts the strap-support
   bracket to the RF-hot Cooling Plate; `spec/01` never carried the taps
   that mounting names. CP-IF-8 now specifies them: 2× M6 × 1.0 × 12,
   bottom face, r = 137 at 88.27° and 121.73° — outside the Ø250 channel
   envelope, 15° clear of the land keep-out edges, clear of the RTD,
   locator, choke and stub patterns (checkable against `spec/00` §3.2 and
   the `aief_clearance` inputs).

2. **ECR-Q-011 / DEC-03.** The FSW internal-rib passes are constrained to
   a tool envelope the 5.0 design rib carries: tapered probe with tip
   Ø ≤ 4.0 (the shoulder rides the continuous 6.00 lid, so shoulder
   engagement does not consume rib width), seam tracking ≤ ±0.5,
   penetration 6.5–7.0. The rib stays 5.0; the channel is unchanged.

The chain is `APR-020 → APR-029`; `APR-020` becomes SUPERSEDED-VALID.
