# APR-017 — Clerical correction of `spec/01` under ECR-D-001; geometric findings split out

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the repair of `VER-014` findings F1–F2, F5, F10.

```yaml
approval_id:   APR-017            # renumbered from APR-015 with APR-016
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-09T00:00:00Z
subject_path:  spec/01_SEWCP-200_Cooling_Plate.md
subject_hash:  f2d228e1730819de3786776a08c4e2526bb0ecb7d1b5b79a493c398d0f2a5355
prior_hash:    a637ae180c27f7f28d7db11de54f6de4dcfe5c6d65576da2eaba8ebe7f8b9b54
supersedes:    APR-016                # voided by this edit under LAW-10; see below
ecr:           ECR-D-001
session:       S-2026-08-09-14
scope:         Option B - clerical correction only. One line of spec/01 (the surviving
               superseded-geometry row in the surface-finish table) plus correction of
               false claims in ECR-D-001, FROZEN.md and STATE.md. No dimension,
               tolerance, datum or interface changes. The geometric consequences of the
               approved counterbore are split into a separate ECR and are NOT approved
               or dispositioned here.
```

---

## Why this approval exists

`APR-016` authorised ECR-D-001 disposition A and was correctly bound to
`spec/01_SEWCP-200_Cooling_Plate.md` at `a637ae18…7f8b9b54`. Independent verification
(`VER-014`) then returned **FAIL** and the repair requires a further edit to that
artifact — which **voids `APR-016` under LAW-10**, exactly as `APR-016` itself declares. This
approval supersedes it and binds to the corrected content. `APR-016` remains on the record as
the instrument that authorised the geometry decision; it is not deleted and its reasoning is
not restated here.

## What is approved

**Option B**, in the words put to the approver:

> Split. Amend `spec/01` under a new approval for the **clerical** defects only — line 201,
> and correct the false claims in ECR-D-001 and FROZEN.md/STATE.md ("29 of 29 verify" is
> false, it is 28 of 29). Raise the geometric consequences (keep-out row, 1.00 mm OD wall,
> 3.35 vs 3.5 mm) as a **new** ECR-D against SEWCP-200/SEWCP-700 for separate disposition.
> ECR-D-001 then closes on the question it was actually raised for: which volume governs.

Options A (repair everything inside ECR-D-001, requiring the approver to set three
engineering numbers) and C (reopen the ECR-D-001 geometry decision) were presented and **not
approved**.

## The single specification edit

| Location | Was | Now |
|---|---|---|
| §8 Surface Finish table | `\| Dowel bores \| Ra ≤ 0.8 µm, masked \| Press-fit dimensional integrity \|` | `\| Locator counterbores and M4 retention threads \| Ra ≤ 0.8 µm, masked \| Flange seating and thread integrity \|` |

This row survived the ECR-D-001 edit and asserted the superseded press-fit geometry inside a
**manufacturing** table — surface finish and anodize masking — contradicting §6 step 13 of the
same volume, which the same edit had already changed to mask *"locator counterbores and their
M4 threads"*. The shop was instructed to mask two differently-named feature sets.

No dimension, tolerance, datum, fit or interface changes. After this edit the string `dowel`
does not appear in `spec/01` in any case — verified with `grep -ci`, **case-insensitively**,
which is the check whose case-sensitive form produced finding F2.

## Scope

| In scope | Out of scope |
|---|---|
| `spec/01` §8 surface-finish row | Every other specification volume |
| Correction of false claims in `ECR-D-001` (§3.4, §6.1a, §6.2, §7, section-number citations) | Any dimension, tolerance, datum or interface |
| Correction of *"29 of 29 verify"* in `FROZEN.md` and `STATE.md` to the measured 28 of 29 | `ECR-D-006` itself — the manifest drift is reported, not repaired |
| Re-registration of `spec/01` and recomputation of the DC-2 aggregate | The §3.1 keep-out row, the 1.00 mm OD wall, the 3.35 mm channel wall — **split to a new ECR** |
| — | `SEWCP-700` `AP-D08` head-counterbore defect — separate ECR |
| — | The `GATES.md` C1 binding-wording conflict — needs a ruling |
| — | CAD, Stage 6, `MANIFEST.lock`, the ledger, execution architecture |

## Authority

`BINDING.approval_authority` is `human-owner`. `mechanical.design-engineer` is UNASSIGNED in
`ROSTER.md`; the split decision was taken by the human owner on a verification report and an
enumerated option set.

> **CORRECTED — `VER-014` R10(a).** This section asserted *"No engineering value was set by an
> implementing agent, which is the property Option B was chosen to preserve."* **That was
> false.** `CP-D09a`/`CP-D10a` in `spec/01` carry `M4 × 0.7, **8.0 deep**`. The approved Option
> A text says *"M4 tapped hole"* with no depth, and `SEWCP-700` — the governing volume —
> specifies the screw as `M4 × 10 SHCS` and states **no plate-side tap depth** anywhere. The
> 8.0 mm figure is derivable from no volume and authorised by no approval, and it is
> load-bearing: `ECR-D-007` §3.3 computes an 11.0 mm penetration from it. An implementing
> agent set it and then certified that none had been set. Disposition of the value is a
> pending human decision; it is not repaired by this approval.
