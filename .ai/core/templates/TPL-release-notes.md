# TPL - Release Notes

> **Generated artifact.** Emitted by aief-compile Stage 2 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `tpl-release-notes` |
| Layer / partition | L2 / core |
| Tier | T3 |
| Owner | `repository-engineer` |
| Mutability | immutable |
| Producer | `repository-engineer` |
| Consumers | `human-owner` |
| Filed at | `project/releases/` |
| Authority | `LAW-07` Git and Configuration Control · workflow `WF-05` |

---

`repository-engineer` owns all repository operations and executes the release sequence **automatically once a release gate is approved**. No release occurs without an approved gate disposition.

## Required sections

### 1 · Version

| | |
|---|---|
| Version | semantic |
| Previous version | |
| Date | ISO-8601 UTC |
| Gate disposition | the approved gate authorising this release |

### 2 · Tag

| | |
|---|---|
| Tag | annotated - never lightweight |
| Target commit | full SHA |
| Author = committer = repository owner | **confirmed** |
| Remote | pushed and verified |

Tags are annotated and **never moved**. Published history is never rewritten.

### 3 · Contents

What changed, at the level a human owner needs to make a decision. Group by area; cite artifacts by path. Note anything that changes an interface, a frozen artifact or the framework binding.

### 4 · Integrity statement

**Must state the verification method**, not merely assert that verification occurred.

| Check | Method | Result |
|---|---|---|
| Working tree clean | `git status --porcelain` empty | |
| Remote branch synchronised | | |
| Remote tags present | | |
| Commit SHA verified | | |
| Release tag target verified | | |
| Author = committer = owner | | |
| Frozen set verifies | normalised SHA-256 per `FROZEN.md` | |

Post-release verification is mandatory. **A repository policy violation is a QA failure, never a warning** - enforced by `V-22`.

### 5 · Known open items

Every open item at the moment of release, or **explicitly none**. Silence is not an acceptable value: a reader cannot distinguish *no open items* from *not checked*.

| ID | Item | Blocks |
|---|---|---|

## Acceptance conditions

| # | Condition | Test |
|---|---|---|
| 1 | Integrity statement states verification method | §4 names the method per check, not just a result |
| 2 | Open items listed or explicitly none | §5 is non-empty or states *none* explicitly |

## Forbidden

| | |
|---|---|
| Modifying git author or committer identity | `LAW-07` |
| Adding attribution, co-author or generated-by trailers | `LAW-07` |
| Moving a tag · rewriting published history | `LAW-07` |
| Force push unless explicitly authorised | `LAW-07` - escalate to human |
| Releasing without an approved gate disposition | `LAW-03` |
| Generating `MANIFEST.lock` outside Compiler Stage 6 | Stage 6 barrier |
