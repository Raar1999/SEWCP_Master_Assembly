# Release — `v0.11.0`

*State of the published repository. Every row was verified during this documentation pass by
running the command named beside it, or by querying the remote.*

---

## 1 · Identity

| | |
|---|---|
| **Release** | `v0.11.0` — *public release: CAD and software complete* |
| **Tag** | annotated, `v0.11.0` → commit `f8ff028d56aee3004b5d41eb1a3d5c3e8f579270` |
| **Commit** | `f8ff028` — *"ECR-D-014 closed on the fifth independent round; register check rebuilt by forbidding the value"* |
| **Branch** | `main`, 0 ahead / 0 behind `origin/main` |
| **Remote** | `git ls-remote origin HEAD` → `f8ff028…` — **identical to local `HEAD`** |
| **Authorising report** | [`releases/RELEASE_READINESS_v0.11.0.md`](../releases/RELEASE_READINESS_v0.11.0.md) |
| **Engineering baseline** | SEWCP Rev A, Volumes 00–09 — **FROZEN** |
| **Governing framework** | AIEF 1.0.0 — **FROZEN**, fifteen amendments |
| **Tag scheme** | `releases/TAGS.md`. All tags annotated; never force-moved. `v1.0.0` is reserved for G7 program closeout |

## 2 · Verdict, as the release report states it

# RELEASED — CAD AND SOFTWARE COMPLETE · PHYSICAL QUALIFICATION NOT STARTED · HARDWARE BUILD BLOCKED

Three statements, all true at once, and the release is honest only if all three are read.

## 3 · State at the tag

| Item | Status | How verified |
|---|---|---|
| Gate `LC-M04-EXIT` | **PASS** C1–C7 | `python -m aief_gate` → `LC-M04 CAD-READY: YES`, exit 0 |
| Feature clearance | **PASS** | `python -m aief_clearance` → `CLEARANCE OK`, exit 0 |
| Parameter master | **PASS**, 105 derived | `python -m aief_params check`, exit 0 |
| Approval chains | **CLEAN** | `python -m aief_approval verify`, exit 0 |
| State registers | **OK** | `python -m aief_register`, exit 0 |
| Deliverables | **61 registered, 61 reproduce, 0 unregistered**, 4,995,097 bytes | `python -m aief_deliverables`, bi-directional, exit 0 |
| Freeze registry | **31 of 31 verify** | `V-24`; DC-2 `1f32489a…8d45cc4b` |
| Boot step **B2a** (core integrity) | **PASS 75/75** | recomputed without importing `src/aief_stage6` |
| Stage 6 build | **PASS**, `V-25` 252 files checked | `python -m aief_stage6`, exit 0 *with* tokenizer artifacts; **exit 1 from a clean clone**, refusing to estimate |
| Assembly | **19 occurrences**, 7.6997 kg | `cad/runs/ASSEMBLY_S-2026-08-11-05/run.json` — PASS |
| System interfaces | **12 / 12** | `cad/runs/SYSTEM_INTERFACES.json` |
| Final system verification | **19 / 19**, `known_defects_carried: []` | `cad/runs/FINAL_SYSTEM_VERIFICATION.json` |
| Drawings | **11 documents / 14 sheets**, 79 dimensions, **0 unsourced** | provenance sidecars; `FSV-DRAWINGS` |
| BOM | Rev A, cross-checked four ways | `cad/bom/SEWCP-000_BOM_RevA.csv` |
| Tests | **895 local · 843 from a clean clone**, 0 fail | measured both ways during this pass |
| CI | GitHub Actions `validate` on push, PR and dispatch | `.github/workflows/validate.yml` |
| Licence | **`MIT AND CC-BY-4.0`**, boundary by path | [`LICENSE`](../LICENSE) |
| **Physical verification** | **0 of 91 — NOT VERIFIED, HARDWARE REQUIRED** | `PVR-001` |
| **`ECR-D-016`** | **OPEN** — blocks hardware build | `python -m aief_analysis`, exit 1 |
| `ECR-D-014` | **CLOSED** — five independent rounds | `.ai/project/OPEN_ITEMS.md` |
| `CMP-BLOCK-004` / `-005` | **OPEN** — they gate **AIEF framework Release 1.0.0**, a different release of a different thing | `DEC-18` |

### Standing-check exit codes, measured at `f8ff028`

```
aief_gate          0      aief_register      0
aief_clearance     0      aief_stage6        0   (1 from a clean clone — see below)
aief_params check  0      aief_analysis      1   ← by design
aief_approval      0      aief_exec check    1   ← 7 of 10 PASS, 3 conditions open
aief_deliverables  0
```

`aief_analysis` exits 1 because it files the `SR-03`/`SR-04` insulation trace and **the trace does
not close**. A check reporting PASS on `ECR-D-016` would be the defect, not the finding.

`aief_stage6` exits 0 here and **halts from a clean clone** with
`tokenizer families not in hand; lock/distributable/DC-5 emission refused (budget UNMEASURED,
counts never fabricated)` — the artifacts are third-party binaries that are not tracked, and the
governing rule makes their absence *block* rather than estimate.

## 4 · Reproducibility, measured three ways

| Environment | Result |
|---|---|
| Clean clone of the published repository | **843 passed, 52 skipped, 0 failed** |
| Clean clone + both tokenizer artifacts + TOFU record | **894 passed, 1 skipped, 0 failed** |
| Working tree (artifacts and `build/stage6/detcheck/` present) | **895 passed, 0 skipped, 0 failed** |

The single irreducible skip needs `build/stage6/detcheck/`, which is gitignored and which no code
in this repository creates — unreachable from a clone by any route.

## 5 · Deliverables

61 files, 4,995,097 bytes, every digest registered in `cad/DELIVERABLES.md` and checked in both
directions. Full breakdown: [`DELIVERABLES.md`](DELIVERABLES.md).

The parametric `.f3d` is deliberately **not** in the repository: `SEDEP-PMP-002` §3.1 places the
parametric source of record in Fusion cloud versioning and git holds the neutral record.

## 6 · Licensing

`SPDX-License-Identifier: MIT AND CC-BY-4.0`. Dual-licensed, and **which licence applies to a
file is determined by its path and by nothing else**:

| Licence | Paths |
|---|---|
| **MIT** — software, everything whose function is to be executed | `src/**`, `tests/**`, `scripts/**`, `drawings/defs/**`, `drawings/generate.py`, `fusion_addin/**`, `cad/scripts/**`, and `*.py` anywhere else |
| **CC-BY-4.0** — documents, engineering artifacts and generated design data; everything whose function is to be read, cited or manufactured from | `spec/**`, `program/**`, and the remaining document and design-data trees |

Both full texts are embedded verbatim so the licence survives without a network. **§3 states
expressly that no patent and no trademark licence is granted, and that the design is not
qualified hardware.** No per-file header is used or permitted — one would move a registered DC-1
digest and halt boot step B2a. `LICENSE` is authoritative; the summary above is not.

## 7 · GitHub state, at the time of this documentation pass

| | |
|---|---|
| Remote | `https://github.com/Raar1999/SEWCP_Master_Assembly.git` |
| Remote `HEAD` | `f8ff028…` — matches local, verified with `git ls-remote` |
| Tag `v0.11.0` | **pushed** |
| GitHub **Release** objects | **none created** — the tag is pushed, but no Release page exists |
| Repository visibility | **private** at the time of this audit (`gh api repos/…` → `"private": true`) |

Both of the last two rows are recorded as documentation findings, not corrected here: creating a
Release page and changing visibility are owner actions, not documentation actions. See
[`DOCUMENTATION_FINDINGS.md`](DOCUMENTATION_FINDINGS.md) §1. Until visibility changes, the clone
instructions in `README.md` will succeed only for accounts with access.

## 8 · What is open, and what it blocks

| Item | Blocks |
|---|---|
| **`ECR-D-016`** — Support Ring isolation joint does not close (creepage 14.00 mm vs 20.00 required; clearance 8.50 vs 12.00; shunt impedance 353.94 Ω vs 400) | **hardware build.** Requires a Rev B baseline revision. **Do not build to this baseline** |
| **`PVR-001`** — 0 of 91 hardware-verifiable requirements verified | physical qualification, which has not started |
| `CMP-BLOCK-004` / `-005` | AIEF **framework** Release 1.0.0 — not this repository's release |
| `OI-C-10` — bounded open-items index at 597 of a 600-token cap | the *next* finding's identifier; an A4 and human-owner decision |

Everything open is indexed at [`.ai/project/OPEN_ITEMS.md`](../.ai/project/OPEN_ITEMS.md) with the
full record at [`OPEN_ITEMS_REGISTER.md`](../.ai/project/OPEN_ITEMS_REGISTER.md). Nothing is hidden
there, including the failures.

## 9 · What this release is not

It is **not qualified hardware**, and it is not a claim that an AI designed a semiconductor
machine unaided. It is a released digital engineering state — specification, models, drawings,
BOM, neutral geometry, analyses, tooling and the governance framework that produced them —
together with the complete record of how it failed along the way.
