# Contributing — PLACEHOLDER

**Status:** Placeholder issued during Release 0.1 infrastructure preparation. Sections marked *TBD* require repository owner ratification.

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

---

## 3. Branch Model — TBD

Proposed in SEDEP-PMP-002 §1.1, pending ratification:

| Element | Proposed |
|---|---|
| Default branch | `main`, protected |
| Feature branches | `wbs/<id>-<slug>` |
| Merge | PR + 1 approval + green CI |

---

## 4. Commit Convention — TBD

Proposed format:

```
[WBS-<id>] <imperative summary>

<body — what changed and why, referencing spec section or ECR>
```

Subject line ≤ 72 characters. Body wrapped at 79.

**No trailers of any kind.** See P-1, P-2, P-3.

---

## 5. Directory Ownership — TBD

| Path | Owner | Change Control |
|---|---|---|
| `spec/` | Design Authority | Frozen — specification revision only |
| `program/` | Program Manager | PR |
| `implementation/` | Lead CAD Engineer | PR |
| `params/` | Lead CAD Engineer | PR + Design Authority for driving dimensions |
| `src/`, `tests/` | Software | PR + green CI |
| `releases/` | Configuration Manager | Tag-gated |

---

## 6. Review Requirements — TBD

Ratified in SEDEP-PMP-002 §5.3. The one non-negotiable rule already in force:

> **A drawing shall never be checked by its originator.**

---

## 7. Open Items for Ratification

| # | Item | Owner |
|---|---|---|
| C-1 | Confirm branch model and protection rules | Repository owner |
| C-2 | Confirm commit convention | Repository owner |
| C-3 | Confirm directory ownership matrix | Program Manager |
| C-4 | Resolve `LICENSE` placeholder | Repository owner |
| C-5 | Populate CI workflows in `.github/workflows/` | Software |
