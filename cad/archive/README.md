# cad/archive/

Superseded CAD artefacts retained for traceability.

---

## Purpose

When a released model or export is superseded, the previous version is moved here rather than deleted. Git history preserves the content; this directory preserves **discoverability** — a reviewer can see what a part used to be without walking the log.

---

## What Belongs Here

| Artefact | Archive? |
|---|---|
| Superseded STEP exports from a passed gate | **Yes** |
| Superseded drawing PDFs after a revision | **Yes** |
| Superseded conformance reports | **Yes** |
| Fusion working files | **No** — ignored by git, cloud-versioned |
| Scratch or experimental geometry | **No** — never committed |

---

## Naming Convention

```
<PART-NUMBER>_<rev>_<YYYY-MM-DD>_superseded-by-<rev>.<ext>
```

Example:

```
SEWCP-200_revX1_2026-10-16_superseded-by-revA.step
```

---

## Rules

1. Archived files are **never edited**.
2. Nothing is archived until its replacement is released.
3. An archived file must state what superseded it, in its filename.
4. This directory is append-only.
