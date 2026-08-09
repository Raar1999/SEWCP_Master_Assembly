# APR-016 — Alignment pin interface geometry: SEWCP-700 governs

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for ECR-D-001 disposition A.

```yaml
approval_id:   APR-016            # renumbered from APR-014: VER-014 R10-c, a prior session had reserved that id
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-09T00:00:00Z
subject_path:  spec/01_SEWCP-200_Cooling_Plate.md
subject_hash:  a637ae180c27f7f28d7db11de54f6de4dcfe5c6d65576da2eaba8ebe7f8b9b54
prior_hash:    3ae384bd82d3d32cedf22c02c58e09fa14a363c8003d05b52ae1f78c0e6a2597
ecr:           ECR-D-001                # the record of the defect and its disposition
scope:         Disposition A of ECR-D-001 - SEWCP-700 governs the alignment pin interface
               geometry; spec/01_SEWCP-200_Cooling_Plate.md is corrected to the
               screw-retained shouldered locator. No other specification volume changes.
session:       S-2026-08-09-14
```

---

## Subject

`spec/01_SEWCP-200_Cooling_Plate.md`, at normalised SHA-256
`a637ae180c27f7f28d7db11de54f6de4dcfe5c6d65576da2eaba8ebe7f8b9b54`,
superseding `3ae384bd82d3d32cedf22c02c58e09fa14a363c8003d05b52ae1f78c0e6a2597`.

Normalisation as declared in `FROZEN.md`: UTF-8, LF line endings, trailing whitespace
stripped, terminal newline enforced.

**This approval is bound to that hash.** Per LAW-10 it is void if the subject content
changes, and it names precisely what it approves.

## What this approval is bound to, and why

**The subject is the specification artifact, not the ECR record** — the `APR-001` precedent,
where `subject_path` is the artifact whose content the approval authorises and `prior_hash`
is what it replaces. Two drafts of this approval bound it to `ECR-D-001` instead; that was
wrong in principle and unworkable in practice, because an ECR record legitimately keeps
changing — disposition text, executed-changes table, `status`, `closed_at` on verification —
and each edit would void the approval that authorises the work it describes.

Recorded rather than quietly rewritten. The ECR is cited above as `ecr:` and is the record of
*why*; this approval is bound to *what changed*, which is stable the moment the change is
made. **The approved option is unchanged throughout**: Option A, in the words put to the
approver and reproduced below.

## What is approved

**Option A**, exactly as presented to the approver:

> SEWCP-700 governs. Correct SEWCP-200 to the screw-retained shouldered locator:
> Ø12.0 H7 × 3.0 counterbore + M4 tapped hole, protrusion 2.50 ± 0.05.
> SEWCP-700 / SEWCP-400 / SEWCP-300 unchanged.

## Scope

| In scope | Out of scope |
|---|---|
| `spec/01_SEWCP-200_Cooling_Plate.md` — `CP-D09`, `CP-D10`, new `CP-D09a`/`CP-D10a`, `CP-IF-1`, `CP-IF-4`, the SEWCP-700 mating-table row, §10 step 12 and §11 step 3 | Every other specification volume |
| Re-registration of `spec/01` in `FROZEN.md` and recomputation of the DC-2 aggregate | The frozen content of any other registered artifact |
| `STATE.md` `frozen_set_hash` | ECR-D-002, ECR-D-003, ECR-D-004 |
| — | The SEWCP-700 material conflict (ICD 316L vs volume Ti-6Al-4V), raised separately |
| — | CAD, Stage 6, `MANIFEST.lock`, the ledger, execution architecture |

## Options presented and not selected

| Option | Disposition |
|---|---|
| **B** — SEWCP-200 governs; SEWCP-700 becomes a plain press-fit dowel; slot depths increase in SEWCP-400 (alumina) and SEWCP-300 | **Not approved** |
| **C** — Integral machined boss on the Cooling Plate | **Not approved**; assessed not viable (unserviceable, scraps a welded 3.9 kg plate, fails AP-10) |

Recorded so that the approval names one option out of an enumerated set, and the set is
recoverable without reading the conversation that produced it.

## Authority

`BINDING.approval_authority` is `human-owner`. The Design Authority role
`mechanical.design-engineer` is UNASSIGNED in `ROSTER.md`; the engineering decision was taken
by the human owner directly, on an analyst package that presented facts, constraints, options
and a recommendation without selecting one. The role gap is recorded rather than implied.
