# APR-021 — ICD coherence package

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the dispositions named below.

```yaml
approval_id:   APR-021
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-10T00:00:00Z
subject_path:  spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md
subject_hash:  fa2a84ccf3a837176eade00c502916a7a1492c9c58785448a4c26ba0fbaab95d
prior_hash:    baf9ae50cd3d34a522b9998fc0f9420746ccf57c3b27f358ff0270024d9e2721
ecr:           ECR-D-002, ECR-D-004, ECR-D-008, ECR-D-010, ECR-Q-009
session:       S-2026-08-10-01
scope:         Only the changes enumerated below, in this one artifact. Every other
               byte of this file is unchanged and no other volume is approved here.
```

---

**Liveness is not asserted in this file.** Determine it with
`python -m aief_approval verify`, which computes the supersession relation the human owner
ruled in session `S-2026-08-10-01` and which `GATES.md` records: an approval is **LIVE** when
its `subject_hash` equals the current DC-1 of `subject_path`, **SUPERSEDED-VALID** when an
unbroken chain of approvals on that path reaches a LIVE one, and **VOID** otherwise. A
hand-written status label went stale four times in this repository before that rule existed.

## What is approved

| ECR | What changed |
|---|---|
| `ECR-D-002` | §4.3 coolant-convection row: h 5000 -> 6500, A 0.09 -> 0.080, R 0.00222 -> 0.00192, total 0.1220 -> 0.1217 K/W and 36.6 -> 36.5 K. **`R_total` still rounds to the 0.122 K/W quoted elsewhere**, so no downstream figure moves |
| `ECR-D-004` | §9 fastener schedule: `M5 x 30` -> `M5 x 25`, both choke rows; the *"Slotted clearance holes in Heater Plate"* note corrected to the Cooling Plate, which contradicted DR-2, `CP-IF-3` and `HP-IF-2` |
| `ECR-D-008` | §8 SEWCP-700 material cell replaced in full |
| `ECR-D-010` | §3.2 gains the missing O260 BC locator row; the false *"No conflicts"* paragraph replaced by a computed statement |
| `ECR-Q-009` | §10 A2: bushing bore Ø5.05 H7 -> **Ø5.60 +0.05/-0**, against six corroborating statements |


## How the approver was consulted

The dispositions above were put to the human owner as selectable options in session
`S-2026-08-10-01`, each with its recommendation, engineering consequences, reversibility and
gate impact stated. The selected option is recorded in each ECR record at its Disposition
section, together with the options presented and **not** approved. **This artifact binds those
selections to the bytes that resulted from them**; the hash was computed after the edits, which
is why it could not have been quoted at the moment of selection.
