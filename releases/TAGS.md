# Release Tag Scheme

Defines the git tag namespace for this repository. Infrastructure document — no engineering content.

---

## 1. Namespaces

| Namespace | Pattern | Purpose | Mutability |
|---|---|---|---|
| `baseline/` | `baseline/<artefact>-<rev>` | Immutable record of a frozen input | **Never moved or deleted** |
| `gate/` | `gate/G<n>` | State of the repository at a program gate exit | Never moved |
| `v` | `v<major>.<minor>.<patch>` | Released package | Never moved |
| `rc/` | `rc/v<x.y.z>-<n>` | Release candidate under QA | May be deleted after promotion |

All tags are **annotated** (`git tag -a`). Lightweight tags are not permitted — a tag without a message carries no provenance.

---

## 2. Version Semantics

| Field | Increments when |
|---|---|
| `major` | The frozen engineering baseline is superseded by a new specification revision |
| `minor` | A program gate (G0…G7) is passed and its deliverables are released |
| `patch` | Correction to released artefacts with no gate change |

`v0.x` denotes pre-gate infrastructure and work-in-progress. **`v1.0.0` is reserved for G7 program closeout** per SEDEP-PMP-002 §5.4.

---

## 3. Planned Tag Sequence

| Tag | Meaning | Status |
|---|---|---|
| `baseline/spec-revA` | SEWCP engineering specification Rev A, Volumes 00–09, frozen | **APPLIED** |
| `v0.1.0` | Repository infrastructure baseline | **APPLIED** |
| `v0.11.0` | Public release — CAD and software complete; physical qualification not started; hardware build blocked by `ECR-D-016` | **APPLIED**, authorised by [`RELEASE_READINESS_v0.11.0.md`](RELEASE_READINESS_v0.11.0.md) |
| `gate/G0` | Baseline Freeze Review passed | Pending |
| `gate/G1` | Digital Foundation Review passed | Pending |
| `gate/G2` | Model Design Review passed | Pending |
| `gate/G3` | Critical Design Review passed | Pending |
| `gate/G4` | Analysis Verification Review passed | Pending |
| `gate/G5` | Drawing Release Review passed | Pending |
| `gate/G6` | Manufacturing Readiness Review passed | Pending |
| `gate/G7` + `v1.0.0` | Program closeout and release | Pending |

---

## 4. Rules

1. A tag is applied **only** after the corresponding gate or readiness report records a pass.
2. Tags are never force-moved. A mistake is corrected by a new tag, not by rewriting an old one.
3. `baseline/*` tags are protected. They are the evidence that a frozen input was frozen.
4. Every tag message states **what** is being tagged and **which** report authorises it.
5. Tag application is a Configuration Manager action.

---

## 5. Applied Tag Messages

Reproduced **verbatim** from the applied annotations. Authoritative source is the tag object itself — verify with `git tag -l <tag> --format="%(contents)"`.

**`baseline/spec-revA`** → `88ec4cb`

```
SEWCP engineering specification Rev A - frozen baseline.

Volumes 00-09, 11 files under spec/.
Content migrated from docs/ unchanged at repository initialisation.
This tag is protected and is never moved or deleted.
```

**`v0.1.0`** → `88ec4cb`

```
Release 0.1.0 - repository infrastructure baseline.

Authorised by releases/v0.1/RELEASE_0.1_READINESS_REPORT.md.
Infrastructure only. No engineering content created or modified.
Conditional restriction: open item C-4 (unresolved LICENSE) blocks
public or external distribution.
```

> **Correction note.** The v0.1.0 release commit carried a paraphrased version of these messages that omitted the protection statement and the C-4 restriction. Independent audit flagged the drift; this section was corrected post-tag. Per §4 rule 2 the tags were **not** moved — `v0.1.0` remains at `88ec4cb`, and this correction lands after it.
