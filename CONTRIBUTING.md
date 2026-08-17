# Contributing

**Status:** Ratified `S-2026-08-17-01` under owner-delegated repository authority
(`.ai/project/decisions/DECISIONS_S-2026-08-17-01.md` DEC-20). The sections that were marked
*TBD* since Release 0.1 are settled below; §1 and §2 were binding throughout and are unchanged.

> **Read `ENGINEERING.md` before you change anything.** This repository is governed by AIEF:
> state lives in files, not in conversation, and a session begins by booting from
> [`.ai/BOOT.md`](.ai/BOOT.md). Most of what looks like a convention here is a *checked*
> property, and the check will find you.

---

## 1. Repository Policy — BINDING

These rules are in force now and are not placeholders.

| # | Rule |
|---|---|
| **P-1** | **Never add AI attribution to any commit, file, or document.** |
| **P-2** | **Never add `Co-authored-by` trailers to commit messages.** |
| **P-3** | **Never modify git author information** (`user.name`, `user.email`, `--author`, `--amend --author`, or any rewrite of authorship). |
| **P-4** | The engineering specification in `spec/` is **FROZEN**. It is changed only by an approved specification revision, never at working level. |
| **P-5** | No engineering decision is made in a commit. Ambiguity is raised as an ECR, not resolved in place. |

---

## 2. Specification Freeze

`spec/` holds the frozen engineering baseline (SEWCP Rev A, Volumes 00–09).

- Content is **read-only** to all contributors.
- A defect found in the baseline is raised as **ECR-D**; a query as **ECR-Q**.
- Neither is fixed by editing `spec/` directly.
- Governing statement: SEDEP-PMP-001 §0.1.

**This is enforced, not requested.** Every `spec/**` artifact is registered in
[`.ai/project/FROZEN.md`](.ai/project/FROZEN.md) under DC-1, and `V-24` recomputes all 31 rows
against the tree. An edit without an approved ECR and a recorded approval moves the digest,
voids the approval bound to it under LAW-10 clause 2, and fails the gate.

---

## 3. Branch Model — RATIFIED

| Element | Rule |
|---|---|
| Default branch | `main` |
| Feature branches | `wbs/<id>-<slug>` |
| Merge | PR with the `validate` workflow green |
| History | **Never rewritten on `main`.** Corrections are new commits, never `--force` |

**Branch protection is not currently configured on the remote**, and this document does not
pretend otherwise — the rule above is the intent, and configuring it is a repository-owner
action on GitHub that no file in this tree can perform. Recorded rather than assumed.

---

## 4. Commit Convention — RATIFIED

```
<imperative summary, <= 72 characters>

<body: what changed and why, citing the spec section, ECR or open item that
authorises it. Wrapped at 79. State what was NOT done as well as what was.>
```

**No trailers of any kind.** See P-1, P-2, P-3. A `[WBS-<id>]` prefix is optional and is used
only where a WBS task actually governs the change; the repository's real traceability is the
ECR and approval records, not a subject-line tag.

**A commit message is a record, not an announcement.** If a change leaves something broken,
open, or unverified, the message says so. Several commits in this history do exactly that, and
they are the useful ones.

---

## 5. Directory Ownership — RATIFIED

| Path | Owner | Change Control |
|---|---|---|
| `spec/` | Design Authority | **Frozen** — approved ECR + recorded approval only |
| `framework/` | A4 / `chief-systems-engineer` | **Frozen** — architecture amendment only |
| `.ai/core/` | Framework | **Never hand-edited.** Replaced wholesale by the compiler |
| `.ai/project/` | Per artifact `owner_role`, declared in `framework.manifest.json` | Mutable, but approvals and the ledger are append-only |
| `.ai/adapters/` | Repository owner | Human write access only |
| `program/`, `implementation/` | Program Manager / Lead CAD Engineer | PR |
| `params/` | Lead CAD Engineer | PR + Design Authority for driving dimensions |
| `src/`, `tests/` | Software | PR + green CI |
| `cad/`, `drawings/` | Lead CAD Engineer | PR. Deliverables are digest-registered — see §6 |
| `releases/` | Configuration Manager | Tag-gated |

---

## 6. Review Requirements — RATIFIED

The non-negotiable rule, in force throughout:

> **A drawing shall never be checked by its originator.**

Its general form is **LAW-05: no role verifies its own output**, and it is the rule this
repository takes most seriously. It is why `ECR-D-014` is open at the time of writing: its
defect was repaired, and the session that repaired it may not certify the repair.

**Independent verification is a cold context**, one that reconstructs every fact from the
repository rather than inheriting a narrative. When it disagrees, it wins: the most recent
round returned `NOT CLEARED` and found a blocking defect in a ruling that had passed 799 tests.

**If you change a digest-registered artifact**, the approval bound to it becomes void and
`python -m aief_approval verify` will say so immediately. That is the mechanism working. File
the ECR and the succeeding approval; do not revert a true correction to keep a chain green.

---

## 7. Before you open a PR

```
PYTHONPATH=src python -m aief_gate            # C1-C7
PYTHONPATH=src python -m aief_clearance
PYTHONPATH=src python -m aief_params check
PYTHONPATH=src python -m aief_approval verify
PYTHONPATH=src python -m aief_deliverables
PYTHONPATH=src python -m pytest tests/ -q
```

`python -m aief_analysis` exits **1** by design while `ECR-D-016` is open. Do not "fix" it.

**Adding a check is worth more than adding a feature here.** Every defect class that went
unnoticed in this repository's history was a declared property with nothing computing it. If
you rule something, check it.

---

## 8. Open items for ratification

| # | Item | Owner | Status |
|---|---|---|---|
| C-1 | Branch model and protection rules | Repository owner | **RATIFIED** §3. Remote branch protection remains an owner action on GitHub |
| C-2 | Commit convention | Repository owner | **RATIFIED** §4 |
| C-3 | Directory ownership matrix | Program Manager | **RATIFIED** §5 |
| C-4 | Resolve `LICENSE` placeholder | Repository owner | **CLOSED** — `MIT AND CC-BY-4.0`, boundary by path. See [`LICENSE`](LICENSE) |
| C-5 | Populate CI workflows | Software | **CLOSED** — `.github/workflows/validate.yml`. Coverage is the checks implemented as software, not the full V-01…V-25 campaign, which `CMP-BLOCK-005` blocks |
