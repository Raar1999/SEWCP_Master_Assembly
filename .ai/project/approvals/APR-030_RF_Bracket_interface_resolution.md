# APR-030 - RF bracket volume: strap holes tap-coincident, hanger re-dimensioned

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.

```yaml
approval_id:   APR-030
approver:      claude-under-owner-delegation   # NOT a human approval - see scope
timestamp:     2026-08-11T00:00:00Z
subject_path:  spec/08_SEWCP-900_RF_Feedthrough_Bracket.md
subject_hash:  b69b0c4859bce91505702354e5cacc9af8e4773b395b6c5694fa63142b12b289
prior_hash:    cfe93cd6c4ef2e6b405909f252a6bd987726b65fdc4a725eb5d36ed453f166b9
supersedes:    null
ecr:           ECR-D-013, ECR-Q-012
session:       S-2026-08-11-05
scope:         Five rows only. RS-D07 re-defined - terminal holes coincident with the
               CP-IF-8 taps (29.94 centres in the pad plane; ECR-D-013 DEC-01).
               SB-D01..SB-D04 re-dimensioned to the plate-hung hanger of ECR-Q-012
               DEC-02 (bearing 8.25 from above; 2x O6.6 at the CP bracket taps;
               min Z 8.0 by construction). No other byte changes. AUTHORITY - this
               approval records "Owner-delegated engineering authority exercised by
               Claude" under the owner's written delegation of 2026-08-11 (mission
               section 1). It is NOT an actual human approval and is never to be
               cited as one. Provenance - decisions/DECISIONS_S-2026-08-11-05.md.
```

---

**Liveness is not asserted here.** Determine it with `python -m aief_approval verify`.

## What is approved

1. **ECR-D-013 disposition A / DEC-01.** The two frozen volumes disagreed
   (25.0 centres vs a 29.94 in-plane tap distance). The strap — the
   compliant, adaptable element — moves: RS-D07 holes are now defined by
   coincidence with the plate taps, eliminating the double dimension the
   land already suffered once (ECR-Q-010). Edge distance on the 50-wide
   pad: 10.03 ≥ 1.5 d. The plate keeps its verified clocking.

2. **ECR-Q-012 disposition / DEC-02.** SB-D01..D04 now dimension the
   plate-hung hanger: RF-hot by mounting (RF-IF-3 honoured), supporting
   the strap from above at 8.25 so RS-D04 = 8.0 exactly, every surface
   ≥ 8.0 from the grounded Base Plate (SB-D04 by construction), no
   dielectric bridging (DR-12 honoured), no ground contact.

This is `spec/08`'s first approval; the chain begins here at the
registered prior state.
