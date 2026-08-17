# ECR-D-015 — The neutral geometry record and the drawing set are absent from the repository

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Found at the public-release readiness sweep, session `S-2026-08-17-01`, on inspecting what a
> clone of this repository would actually contain.

```yaml
ecr_id:       ECR-D-015
class:        D                      # defect - a repository artifact asserts a rule that contradicts the governing plan
raised_by:    repository-engineer · S-2026-08-17-01
status:       DISPOSITIONED
disposition:  A - mirror every deliverable except the parametric source into the repository at the paths SEDEP-PMP-002 declares, byte-identical, and correct cad/DELIVERABLES.md
ruled_by:     claude-under-owner-delegation (owner-delegated engineering and repository authority, mission 2026-08-17; NOT a human approval)
ruled_at:     2026-08-17T00:00:00Z
instrument:   .ai/project/decisions/DECISIONS_S-2026-08-17-01.md DEC-12
approval:     none required - no artifact registered in project/FROZEN.md and no spec/** artifact is touched
affected_artifacts:
  - cad/DELIVERABLES.md
  - cad/exports/step/
  - cad/exports/stl/
  - cad/bom/
  - drawings/parts/
  - drawings/assembly/
  - .gitattributes
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-17T00:00:00Z
related:      OI-CAD-03
```

## 1 · Class

**D — defect.** `cad/DELIVERABLES.md` line 3 states:

> External output root: `D:\AIEF_CAD_OUTPUT\SEWCP\` (outside this repository by
> rule; the repository records provenance, never duplicates the exports).

**No authority states that rule, and three statements of the governing plan state the
opposite.** `program/SEDEP-PMP-002_Digital_Engineering_Infrastructure.md`:

| Where | What it says |
|---|---|
| §3.1, working-rules table | *"STEP exported at each gate, **committed to `cad/exports/step/`**"* — reason column: *"Git holds the neutral geometry record; Fusion holds the parametric one"* |
| §3, Fusion project tree | `07_EXPORTS/` … `STEP/ PDF/ STL/ RENDERS/` — annotated **`[Generated — mirrored to repo]`** |
| §1, repository tree | `cad/exports/{step,stl,screenshots}/`, `drawings/{parts,assembly,icd,templates,redlines}/` |
| §6 metrics | *"Released parts | 10 | `cad/exports/step/`"* |

`.gitignore` restates the same policy in its own header — *"Git holds the neutral geometry
record (STEP) and documentation only. Policy reference: SEDEP-PMP-002 §3.1"* — and carries
explicit negations `!cad/exports/step/*.step` and `!drawings/**/*.pdf`, which exist for no
other purpose than to keep those artifacts tracked.

**The negations have never had anything to negate.** `cad/exports/step/`,
`cad/exports/stl/`, `cad/exports/screenshots/`, `drawings/parts/` and `drawings/assembly/`
contain nothing but `.gitkeep`.

## 2 · Evidence

Observed, not asserted.

```
$ find cad/exports drawings/parts drawings/assembly -type f
drawings/assembly/.gitkeep
drawings/parts/.gitkeep
                                    # cad/exports/{step,stl,screenshots}: empty

$ python - <<'…'  # over D:\AIEF_CAD_OUTPUT\SEWCP\
TOTAL FILES 62 BYTES 5054400
```

All 62 exist outside the repository, on one machine, at an absolute path on a `D:` drive.
All 62 digests reproduce against the register in `cad/DELIVERABLES.md` — the register is
correct; what it points at is unreachable.

`releases/RELEASE_READINESS_S-2026-08-11-06.md` §5 records the state in terms:
*"**No deliverable was moved into git.**"* It records it as a property, not as a finding,
because that audit was scoped to a local baseline where the distinction did not bite.

## 3 · Impact

**Confined to distribution, and total there.**

- A clone of this repository contains **no geometry and no drawings**. Not one STEP body,
  not one drawing sheet, not one BOM row. It contains a table of 62 digests naming files
  the cloner cannot obtain.
- Every provenance claim in `cad/DELIVERABLES.md` becomes unverifiable by anyone but the
  owner of that one machine. A digest register whose subjects are unreachable proves
  nothing; it merely looks as though it does, which is worse than an honest absence.
- No engineering property moves. Every model is verified, every drawing generated, every
  digest recorded and matched. **This is a packaging defect, not a design defect**, and it
  is raised as `D` because a repository artifact states a rule that no authority states and
  the release consequence is complete.

Nothing at `LC-M04-EXIT`: this ECR bears on no `spec/**` artifact, so it is outside `C5`
and outside `C7`'s ten. The gate reads exactly as before.

## 4 · Requested action

Rule one of:

**(a) Mirror the deliverables into the repository**, at the paths `SEDEP-PMP-002` declares,
byte-identical, excluding only `*.f3d` — which the same plan assigns to Fusion cloud
versioning and `.gitignore` excludes by name. 61 of 62 files, 4,995,497 bytes, against a
present `.git` of 3.3 MB. Correct `cad/DELIVERABLES.md` to record paths inside the
repository and retain the external root as the point of generation.

**(b) Keep the deliverables external** and amend `SEDEP-PMP-002` §3.1 to say so, deleting
the two `.gitignore` negations that exist only to track them, and state in `README.md`
that the repository ships no geometry.

**(c) Mirror only the STEP set**, on the ground that §3.1's working-rule names STEP alone.

**Recommendation of the raising agent: (a).** (b) inverts the governing plan to match an
undocumented practice and leaves a public repository whose central deliverable is a
promissory note; (c) splits a register that is verified bi-directionally as one set of 62,
and would leave the drawing set — the thing a manufacturer actually reads — outside.

**One thing (a) requires that is not optional.** `.gitattributes` declares `* text eol=lf`
over every path, and its own comment says *"There is no binary content to damage. **Re-run
that check before adding any.**"* The check was re-run: of the 61 files, **14 PDF and 10
STL contain NUL octets and do not decode as UTF-8**, and the remaining 37 (STEP, SVG,
provenance JSON, BOM CSV) are UTF-8 but carry CRLF. Under the blanket rule git would
corrupt the 24 binaries outright and rewrite the 37 text files to LF — **moving every one
of the 61 recorded digests**. The disposition therefore declares the four deliverable
subtrees `-text`, which preserves the octets exactly and keeps the register true. No
existing path changes class, and the `V-25` domain is untouched: no deliverable is under
`.ai/` and none is registered in `project/FROZEN.md`.
