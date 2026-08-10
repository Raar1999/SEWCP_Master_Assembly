# ECR-D-006 — The framework manifest does not reproduce against its registered digest

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-ecr.schema.json`.
> Record filed `S-2026-08-10-01`. The full derivation has lived in
> [`../OPEN_ITEMS_REGISTER.md`](../OPEN_ITEMS_REGISTER.md) since `S-2026-08-08-12`; **no ECR
> record existed**, and its absence made `LC-M04-EXIT` `C7` *undecidable* rather than merely
> unsatisfied, because `C7` is evaluated over `affected_artifacts` and there was nothing to read.

```yaml
ecr_id:       ECR-D-006
class:        D
raised_by:    chief-systems-engineer · S-2026-08-08-12
status:       OPEN
disposition:  null                   # reserved to the human owner
ruled_by:     null
approval:     null
affected_artifacts:
  - framework/framework.manifest.json
evidence:     "The registry carries 8af8971b78d7... and the artifact normalises under DC-1 to a
               different value. Nine alternative constructions were tested and none reproduces
               the recorded value, so this is a content divergence, not a construction
               disagreement. Full dual-computed derivation at OPEN_ITEMS_REGISTER.md row
               ECR-D-006, including the control that reproduces APR-010 subject_hash exactly."
impact:       "Re-affirmation of the AIEF-AMD-013 manifest change; Compiler Stage 6 execution.
               NOT under spec/**, so it bears on neither LC-M04-EXIT C5 nor C7."
requested_action: "Human-owner re-affirmation of the AIEF-AMD-013 bytes."
raised_at:    2026-08-08T00:00:00Z
closed_at:    null
residual:     null
```

---

## 1 · Class

**D — defect.** A registered frozen artifact does not reproduce against its registered digest,
so LAW-01's *"changed only by an approved ECR and a recorded human approval"* is unsatisfied for
whatever bytes differ, and under LAW-10 clause 2 `APR-012`'s binding to its subject is void as
recorded.

## 2 · Affected artifacts

`framework/framework.manifest.json` — **and nothing under `spec/**`.** That fact decides this
ECR's relationship to the LC-M04 gate and is why it is recorded rather than resolved here.

## 3 · Evidence

The dual-computed derivation, the three-way method check, the control that reproduces `APR-010`'s
`subject_hash` to the digit, and the nine rejected alternative constructions are all in
[`../OPEN_ITEMS_REGISTER.md`](../OPEN_ITEMS_REGISTER.md) row `ECR-D-006`. They are **not**
restated here; duplicating a derivation is how two versions of it come to disagree.

**Independently reproduced this session.** `python -m aief_approval verify` reports
`framework/framework.manifest.json` as the single registered path carrying **no LIVE approval**,
with `APR-001`, `-002`, `-004`, `-006`, `-010` and `-012` all **VOID** in consequence, and
separately reports the registry/tree mismatch. That tool was written to check approval chains
and had no knowledge of this ECR; it derived the same conclusion from repository bytes alone.

## 4 · Impact

Blocks re-affirmation of the `AIEF-AMD-013` manifest change and Compiler Stage 6 execution.

**Does not block `LC-M04-EXIT`.** `C5` is scoped to *"the frozen specification"* and this
artifact is not part of it; `C7` is scoped to ECR-D items *"whose `affected_artifacts` lie under
`spec/**`"* and this one's do not. [`../GATES.md`](../GATES.md) records the same exclusion
positively and by name.

## 5 · Requested action

Human-owner re-affirmation of the `AIEF-AMD-013` bytes. **Root cause is `OI-V-02`** — no standing
check bound the registry to the tree, which is precisely what `ECR-D-005` recorded and what left
this undetected for two sessions. That gap is now partly closed: `aief_approval` fails non-zero
on exactly this condition, and `tests/test_approval_chain.py` holds it there.

## 6 · Disposition

**None. OPEN.** Reserved to the human owner; **not closable by the raiser** (LAW-02 clause 5).

## 7 · Relationship to `LC-M04-EXIT`

**Not a criterion of this gate.** Recorded here so that `C7` is decidable rather than undefined.
