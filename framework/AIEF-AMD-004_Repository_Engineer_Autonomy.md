# AIEF-AMD-004 — Architecture Amendment: Repository Engineer Autonomy

**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-02
**Scope:** Repository Engineer contract and LAW-07 only
**Date:** 2026-08-07
**Amends:** `framework/framework.manifest.json`
**Does not amend:** AIEF-FRZ-001 · AMD-001 · AMD-002 · AMD-003 · `SCH-framework-manifest.schema.json`

---

## AMD-11 — Repository Engineer Becomes Permanent Owner of Repository Operations

**Change class:** additive contract extension

The Repository Engineer (A1) is promoted to permanent owner of all repository operations, with authority to execute the full release sequence **automatically once a workflow reaches an approved release gate**, without further prompting.

### Added to `responsibilities`

- Permanent ownership of all repository operations
- Autonomous execution of the release sequence once a workflow reaches an approved release gate
- Post-release repository integrity verification

### Added to `allowed`

- Execute `git status`, stage changes, commit, annotated tag, push, remote verification, release verification and repository integrity verification
- Execute the full release sequence automatically once a release gate is approved, without further prompting

### Added to `forbidden`

- Modify git committer identity
- Overwrite the configured git identity
- Add **generated-by** trailers *(attribution and co-author trailers were already prohibited)*
- Force push unless explicitly authorised by the framework
- **Release without an approved gate disposition**

### Added to `escalation`

- Force push → human
- **Any post-release verification failure → `qa-engineer` as a QA failure**

### Added to `inputs` / `outputs`

Inputs gain the approved release gate disposition. Outputs gain release verification and remote synchronisation records.

> **Human approval authority is unchanged.** Autonomy is granted *downstream* of an approved gate, never in place of one. The new forbidden clause *"Release without an approved gate disposition"* makes that boundary explicit and enforceable: the Repository Engineer may act without prompting, but never without approval.

---

## AMD-12 — LAW-07 Expanded; Violations Become QA Failures

**Change class:** additive clauses plus one new check

The governing `rule` is **unchanged**. Six clauses are added.

| # | Added clause |
|---|---|
| 1 | No generated-by trailers |
| 2 | The configured git identity is preserved and never overwritten |
| 3 | Force push is prohibited unless explicitly authorised by the framework |
| 4 | The repository-engineer owns all repository operations and executes the release sequence automatically once a release gate is approved |
| 5 | After every release the repository-engineer shall verify: clean working tree, remote branch, remote tags, commit SHA, release tag target, repository synchronisation, and author equals committer equals repository owner |
| 6 | **A repository policy violation is a QA failure, never a warning** |

### New validation V-22

| Field | Value |
|---|---|
| Class | Git policy validation |
| Severity | **BLOCKING** |
| Phase | installation |
| Law | LAW-07 |
| Verifies | author == committer == repository owner on every commit and tag; no attribution trailer in **line-anchored trailer form** in any commit message or tag annotation; no AI authorship claim in any tracked artifact; published history not rewritten; post-release working tree clean and synchronised; release tag resolves to the release commit |

`LAW-07.checks` becomes `["V-21", "V-22"]`. Clause 6 is now mechanically enforced rather than declared.

### Correction made during validation — self-referential check defect

The first draft of V-22 verified that certain literal strings appear *nowhere in any tracked artifact*. Validation immediately failed with two hits: `framework.manifest.json` and this document — **both because V-22's own definition names the patterns it prohibits.**

**V-22 as first written could never pass, because writing it down violated it.** A check that cannot pass is worse than no check: it trains the team to disable it, which is failure mode FM-3 anticipated at CDR.

Corrected: V-22 matches an attribution **trailer in line-anchored trailer form** (`^co-authored-by:`, `^generated-by:`), never a bare substring, and explicitly states that prohibition text naming a forbidden pattern is not itself a violation. This is also the technically correct definition — a git trailer *is* a line-anchored `Key: value` at the end of a commit message, not an arbitrary occurrence of a word.

---

## Blast Radius

The manifest is the source of truth. Affected generated artifacts were determined by **full re-render and byte comparison**, not by inspection.

| Result | Count |
|---|---|
| Stage 1 artifacts re-rendered and compared | 58 |
| **Unchanged** | **56** |
| **Changed** | **2** |

| Changed artifact | Cause |
|---|---|
| `.ai/core/agents/AGT-repository-engineer.md` | AMD-11 contract extension |
| `.ai/core/laws/LAW-07_git_configuration.md` | AMD-12 clauses and check binding |

Both were **re-rendered from the amended manifest, not hand-edited.** A full Stage 1 re-render therefore still reproduces the live tree byte-for-byte, so QA-B1 continues to hold.

`core/agents/INDEX.md` and `core/laws/INDEX.md` are unaffected because `capability_tags`, `duty_conflicts` and the LAW-07 `rule` string were deliberately left unchanged. Stage 5 validation artifacts are not yet emitted, so V-22's addition changes no existing file.

**Stage 3 was not regenerated. No project artifact was modified.**

---

## Version Classification

| Question | Ruling |
|---|---|
| Is this a framework version bump? | **No.** AIEF remains **1.0.0** |
| Why? | Consistent with AMD-001, AMD-002 and AMD-003, all of which amended the frozen 1.0.0 without a bump. A version bump would alter `core/VERSION` and the version stamp in every generated file header, forcing a full regeneration of all 58 Stage 1 artifacts — which this amendment is explicitly directed not to do |
| Repository release | **v0.4.0** — repository versioning is independent of framework versioning |

### Finding recorded for the next framework release

> **Four amendments have now accumulated against a "frozen" 1.0.0** (AMD-001 ownership and profiles, AMD-002 dependency defect, AMD-003 two value rulings, AMD-004 contract extension). Under AIEF's own semantics in AIEF-FRZ-001 §13.1, the additive changes in AMD-001 and AMD-004 and the new check V-22 are **MINOR-class**.
>
> The distributed artifact and the amended source have therefore diverged. **Before AIEF is installed into a second repository, the accumulated amendments must be rolled into a 1.1.0 release with a full recompile**, so that "AIEF 1.0.0" means one thing everywhere. This is a real fleet-consistency risk, not bookkeeping — it is the failure mode F-09 anticipated at CDR.
>
> Deferred, not dismissed. Owner: Chief Systems Engineer.

---

## Constraints Observed

| Constraint | Compliance |
|---|---|
| Do not modify engineering documents | `spec/`, `program/`, `implementation/` untouched |
| Do not regenerate Stage 1 or Stage 3 | No stage re-run; 2 files selectively re-rendered, 56 untouched, Stage 3 untouched |
| Modify only directly affected generated files | Exactly 2, both proven by re-render diff |
| Human approval authority unchanged | Autonomy granted downstream of an approved gate only |
| Universal registry unchanged | Still five roles; no role added, renamed or removed |

---

**END OF AIEF-AMD-004**
