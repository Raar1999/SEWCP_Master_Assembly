# releases/

Release records. One directory per release, named `v<major>.<minor>`.

Each release directory holds the **manifest** (what was in the release), the **readiness report** (evidence it was fit to release), and any release-specific artefacts.

Release directories are **append-only**. Once a release is tagged, its directory is not edited — a correction is a new release.

---

## Contents

| Path | Description | Status |
|---|---|---|
| `TAGS.md` | Git tag namespace and version semantics | Active |
| `v0.1/` | Release 0.1 — repository infrastructure baseline | **Released 2026-08-07** |

---

## Release Index

| Release | Date | Tag | Scope | Report |
|---|---|---|---|---|
| 0.1.0 | 2026-08-07 | `v0.1.0` | Repository infrastructure only | [`v0.1/RELEASE_0.1_READINESS_REPORT.md`](v0.1/RELEASE_0.1_READINESS_REPORT.md) |

---

## Adding a Release

1. Create `releases/v<x.y>/`.
2. Add `MANIFEST.md` — what is included, with paths and revisions.
3. Add the readiness report with pass/fail evidence.
4. Update `CHANGELOG.md`.
5. Update the Release Index above.
6. Apply the annotated tag per `TAGS.md` §4.
