# ENGINEERING.md

**Canonical entry point for this repository.**
Read this first, then the canonical artifacts it references.

> **This file is an index, not an authority.** It holds no rule, no law, no specification and no decision. Where it disagrees with a canonical artifact, **the canonical artifact governs.** Nothing here may be cited as a source.
>
> It sits at the repository root, outside `.ai/`, so that no framework upgrade can invalidate it (AIEF-AMD-002 §AMD-08).

---

## 1 · Project Identity

| | |
|---|---|
| **Project** | SEWCP — Semiconductor Electrostatic Wafer Chuck Platform |
| **Product** | 300 mm bipolar electrostatic chuck pedestal for RF-biased plasma process equipment |
| **Engineering baseline** | SEWCP Rev A — **FROZEN** |
| **Governing framework** | AIEF 1.0.0 — **FROZEN**, thirteen amendments |
| **Active profile** | `mechanical` |
| **Active host adapter** | `claude-code` |
| **Repository release** | Last tag **v0.10.0**, on the Stage 5 release commit. **`HEAD` is past it** — `git describe --tags` reports `v0.10.0-16-g5e7ac74`, and `--exact-match` therefore *fails*. Corrected `S-2026-08-10-04`: this row published the `--exact-match` form as a passing verification, and it has not passed since the first commit after the tag |

## 2 · Startup Sequence

**Every session begins here. No session depends on prior conversation.**

| Step | Action |
|---|---|
| 1 | Read this file — orientation only |
| 2 | Read [`.ai/BOOT.md`](.ai/BOOT.md) — the framework entry point |
| 3 | Execute the boot sequence declared in `BOOT.md` (B1–B9) |
| 4 | **Stop at B9. Declare orientation. Await role assignment.** Do not act before a role is assigned |

`BOOT.md` carries the authoritative boot sequence, tier rules and load order. **This file does not restate them.**

## 3 · Continuation Sequence

Recovering an in-progress project without conversation history:

| Step | Source | Status |
|---|---|---|
| 1 | [`.ai/BOOT.md`](.ai/BOOT.md) — boot procedure | ✅ available |
| 2 | [`.ai/project/STATE.md`](.ai/project/STATE.md) — **authoritative resume point**, stage, next action | ✅ available |
| 3 | [`.ai/project/ledger/HEAD`](.ai/project/ledger/HEAD) — staleness check (B4) | ✅ available |
| 4 | [`.ai/project/BINDING.md`](.ai/project/BINDING.md) — stage, gate, profile, authority | ✅ available |
| 5 | [`.ai/project/OPEN_ITEMS.md`](.ai/project/OPEN_ITEMS.md) — blockers and deviations | ✅ available |
| 6 | [`.ai/project/FROZEN.md`](.ai/project/FROZEN.md) — hash-registered frozen authorities | ✅ available |

> **Repository-driven continuation is operational.** `.ai/project/STATE.md` is now **authoritative** for engineering status; §7 below is a convenience pointer only and `STATE.md` governs where they differ.
>
> **One boot step is not yet satisfied: B2a** (`core/MANIFEST.lock`, Compiler Stage 6). B2a is the *core integrity* check — it verifies `core/` has not been tampered with. Its absence does not impede information recovery; it means integrity cannot yet be **proven**.

## 4 · Repository Structure

| Path | Contents | Change control |
|---|---|---|
| `spec/` | Engineering specification, Volumes 00–09 | **FROZEN** — specification revision only |
| `program/` | Program management and infrastructure plans | PR |
| `implementation/` | Per-component implementation packages (9 components) | PR |
| `framework/` | AIEF architecture, manifest, schema, amendments | **FROZEN** — A4 authority only |
| `.ai/` | The installed AIEF framework | Generated — never hand-edited |
| `cad/` · `drawings/` · `analysis/` | Engineering artifacts | PR |
| `params/` · `src/` · `tests/` | Parameter master and tooling | PR |
| `releases/` · `traceability/` · `notebook/` | Release, trace and record keeping | Per law |

## 5 · Canonical Documents

**Product**

| Document | Path |
|---|---|
| Specification index | [`spec/README.md`](spec/README.md) |
| Architecture & Interface Control (parent of all volumes) | [`spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md`](spec/00_SEWCP-ENG-001_Architecture_and_Interface_Control.md) |
| Component volumes 01–09 | `spec/01_…` through `spec/09_…` |
| Master document index | [`INDEX.md`](INDEX.md) |

**Program**

| Document | Path |
|---|---|
| Program management plan | [`program/SEDEP-PMP-001_Program_Management_Plan.md`](program/SEDEP-PMP-001_Program_Management_Plan.md) |
| Digital engineering infrastructure | [`program/SEDEP-PMP-002_Digital_Engineering_Infrastructure.md`](program/SEDEP-PMP-002_Digital_Engineering_Infrastructure.md) |
| Release 0.1 readiness | [`releases/v0.1/RELEASE_0.1_READINESS_REPORT.md`](releases/v0.1/RELEASE_0.1_READINESS_REPORT.md) |

**Framework**

| Document | Path |
|---|---|
| Architecture freeze 1.0.0 | [`framework/AIEF-FRZ-001_Framework_Architecture_Freeze_1.0.0.md`](framework/AIEF-FRZ-001_Framework_Architecture_Freeze_1.0.0.md) |
| AMD-001 — ownership, profiles, role contracts | [`framework/AIEF-AMD-001_Architecture_Amendments_1.0.0.md`](framework/AIEF-AMD-001_Architecture_Amendments_1.0.0.md) |
| AMD-002 — CMP-BLOCK-014 dependency cycle | [`framework/AIEF-AMD-002_Architecture_Amendments_CMP-BLOCK-014.md`](framework/AIEF-AMD-002_Architecture_Amendments_CMP-BLOCK-014.md) |
| AMD-003 — session timeout, ledger genesis | [`framework/AIEF-AMD-003_Architecture_Amendments_OI-F-01_OI-F-02.md`](framework/AIEF-AMD-003_Architecture_Amendments_OI-F-01_OI-F-02.md) |
| AMD-004 — Repository Engineer autonomy | [`framework/AIEF-AMD-004_Repository_Engineer_Autonomy.md`](framework/AIEF-AMD-004_Repository_Engineer_Autonomy.md) |
| AMD-005 — host bootstrap artifacts | [`framework/AIEF-AMD-005_Host_Bootstrap_Artifacts.md`](framework/AIEF-AMD-005_Host_Bootstrap_Artifacts.md) |
| AMD-006 — Mechanical CAD Engineer | [`framework/AIEF-AMD-006_Mechanical_CAD_Engineer.md`](framework/AIEF-AMD-006_Mechanical_CAD_Engineer.md) |
| AMD-007 — compiler_stage state field | [`framework/AIEF-AMD-007_Compiler_Stage_State_Field.md`](framework/AIEF-AMD-007_Compiler_Stage_State_Field.md) |
| AMD-008 — digest constructions, stage monotonicity, provenance, registry scope | [`framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md`](framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md) |
| AMD-009 — Stage 1 emission barrier, MI-3 namespace | [`framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md`](framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md) |
| AMD-010 — Stage 6 constructions (DC-4, DC-5, tokenizers) and pre-flight dispositions | [`framework/AIEF-AMD-010_Stage_6_Constructions_and_Preflight_Dispositions.md`](framework/AIEF-AMD-010_Stage_6_Constructions_and_Preflight_Dispositions.md) |
| AMD-011 — software role enablement (OQ-13 enactment) | [`framework/AIEF-AMD-011_Software_Role_Enablement.md`](framework/AIEF-AMD-011_Software_Role_Enablement.md) |
| AMD-012 — DC-4 coverage of enabled-role artifacts (OI-C-06 disposition) | [`framework/AIEF-AMD-012_DC-4_Coverage_of_Enabled_Role_Artifacts.md`](framework/AIEF-AMD-012_DC-4_Coverage_of_Enabled_Role_Artifacts.md) |
| AMD-013 — boot-budget determination (CMP-BLOCK-006) and Stage 6 build constructions (OQ-B1…B5) | [`framework/AIEF-AMD-013_Boot_Budget_Determination_and_Stage_6_Build_Constructions.md`](framework/AIEF-AMD-013_Boot_Budget_Determination_and_Stage_6_Build_Constructions.md) |
| AMD-014 — OQ-15 enactment, bounded register split | [`framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md`](framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md) |
| Framework manifest — single source of truth | [`framework/framework.manifest.json`](framework/framework.manifest.json) |
| Manifest schema | [`framework/SCH-framework-manifest.schema.json`](framework/SCH-framework-manifest.schema.json) |

**Framework runtime** — authoritative for all process questions

| Subject | Path |
|---|---|
| Boot procedure | [`.ai/BOOT.md`](.ai/BOOT.md) |
| Conflict resolution | [`.ai/core/PRECEDENCE.md`](.ai/core/PRECEDENCE.md) |
| Engineering laws (13) | [`.ai/core/laws/INDEX.md`](.ai/core/laws/INDEX.md) |
| Agent registry (5 universal + profile) | [`.ai/core/agents/INDEX.md`](.ai/core/agents/INDEX.md) |
| Workflows (12 phases, 6 workflows) | [`.ai/core/workflows/INDEX.md`](.ai/core/workflows/INDEX.md) |
| Active profile | [`.ai/core/profiles/mechanical/PROFILE.md`](.ai/core/profiles/mechanical/PROFILE.md) |

## 6 · Compiler Stage

> **Authoritative source: [`.ai/project/STATE.md`](.ai/project/STATE.md) field `compiler_stage`.** The table below is a convenience pointer.

| Stage | Name | Status |
|---|---|---|
| 1 | Generate Core | ✅ **COMPLETE** — 59 artifacts, signed off |
| 2 | Generate Templates | ✅ **COMPLETE** — 11 artifacts, barrier satisfied *(closes DEV-01)* |
| 3 | Generate Project Layer | ✅ **COMPLETE** — 8 artifacts *(ahead of Stage 2; deviation DEV-01, now closed)* |
| 4 | Generate Adapters | ✅ **COMPLETE** — 5 adapters + `CLAUDE.md` host hook |
| 5 | Generate Validation | ✅ **COMPLETE** — `core/validation/CHECKS.md` + `MANIFEST`, 25 checks, stage barrier PASS; verified by VER-003 |
| 6 | Generate Release | ⏳ outstanding — **gates boot step B2a**; blocked by CMP-BLOCK-004 and **awaiting explicit human authorization** |

## 7 · Engineering Status

> **Authoritative source: [`.ai/project/STATE.md`](.ai/project/STATE.md).** The table below is a convenience pointer. Where they differ, `STATE.md` governs.

| Item | State |
|---|---|
| Lifecycle stage | `LC-M04` Implementation · gate `LC-M04-EXIT` **PASSES `C1`–`C7`** — computed, not asserted: run `PYTHONPATH=src python -m aief_gate`. This is the design-authority **precondition for CAD**, not the stage exit; see `GATES.md` §*Deferred* |
| Specification | Rev A frozen, 9 components, 142 requirements |
| Framework | AIEF 1.0.0 frozen, **thirteen amendments**; Stages 1–5 emitted |
| Agents | 5 universal + 4 `mechanical` + 3 `software` (enabled by AMD-011; `active_profile` unchanged), all persisted on disk |
| Frozen set | **29** artifacts hash-registered in [`.ai/project/FROZEN.md`](.ai/project/FROZEN.md); **28 verify**, the exception being `framework/framework.manifest.json` (ECR-D-006, not under `spec/**`). Seven `spec/**` artifacts re-registered `S-2026-08-10-01` under `APR-020`…`APR-026` |
| Ledger | genesis, `HEAD.seq = 0`, reconciled with `STATE`. No LAW-09 close has been performed |
| Repository | **Local only. `HEAD` is 14 commits ahead of `origin/main`** and push is deferred until **2026-09-01** by standing instruction — verify with `git rev-list --count origin/main..HEAD`, never by reading this cell. Corrected `S-2026-08-10-04`: it read *"`HEAD == origin/main`"*, which had been false since the first unpushed commit. Approval-provenance commits: `d07e931` (Release 0.8 — Stage 2 templates + AMD-008 state, manifest at APR-002's subject `636cf22b…`), `655aa75` (AMD-009 state, manifest at APR-004's subject `9611d547…`, AMD-009 at APR-005's subject `86c8be7f…`), `be75798` (Release 0.9 sync, tag v0.9.0). The Stage 5 release commit adds `core/validation/**`, VER-003 and the `.gitignore` negation |

> **Approval provenance.** Each approval's subject is recoverable as a git object: `git show d07e931:framework/framework.manifest.json` normalises to APR-002's `subject_hash`; `git show 655aa75:framework/framework.manifest.json` to APR-004's; `git show 655aa75:framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md` to APR-005's. This discharges VER-002 findings FIND-Q2-2 and FIND-Q2-3.

**Open items — authoritative list: [`.ai/project/OPEN_ITEMS.md`](.ai/project/OPEN_ITEMS.md)**

| ID | Item | Blocks |
|---|---|---|
| ECR-D-001…004, 007…012 | **All dispositioned, approved, applied and registered.** `C6` closed by `VER-017`; `ECR-D-012` (the `C6` instrument) ruled `S-2026-08-10-04`. **Nothing blocking** — see [`.ai/project/OPEN_ITEMS.md`](.ai/project/OPEN_ITEMS.md) | Nothing |
| CMP-BLOCK-004 / -005 | Compiler not implemented as software; verification infrastructure absent | Stage 6, V-09/V-12/V-15/V-18 |
| ~~CMP-BLOCK-006~~ | **Closed** by [`AIEF-AMD-014`](framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md) §AMD-52 (OQ-15 enacted) | — |
| C-4 | `LICENSE` is an unresolved placeholder | Public or external release |
| CDR-C3 | Independent cold-context ratification of the AIEF CDR not performed | Recorded residual risk, AIEF-FRZ-001 §6.2 |

**Recently closed by `S-2026-08-10-04`/`-05`** — `OI-V-11` (the `VER-014` evidence-integrity
defects blocking `C6` for `ECR-D-001`), discharged by `VER-017`; and `OI-C-12` (four exec-layer
tests pinning a snapshot of live project state), repaired at the property and published at
[`R-017`](.ai/project/results/R-017.md). Newly opened: `OI-C-13` (`APR-001`…`APR-013` carry no
`ecr:` back-reference — a convention boundary, deliberately not repaired by rewriting thirteen
human-approval records).

**Open, not blocking** — `OI-V-02` (`V-24` **is** now implemented and runs in the suite, but has
no validation-campaign infrastructure), `OI-V-03` (all session `S-2026-08-08-02` work is unverified), `OI-V-06` (V-14 trial count undeclared — pre-flight OQ-11), `OI-V-07` (`core/validation/` stale in the V-09/V-10 texts after AMD-010, now also after AMD-013), `OI-R-01` (no `v0.2.0` tag), `OI-C-01…02` (ledger schema; `ADP-ci` stale at 22 checks — required content now fixed by AMD-010 §AMD-32), `OI-C-04…05` (`implementation/` BOMs; `referenced_by` completeness undeclared), `OI-C-07` (`core/agents/INDEX.md` role tables lack the software rows pending a Stage 1 re-render), `OI-C-08` (`project/ledger/HEAD` is read at boot step B4 yet carries no `token_cap`, so the V-09 measured set under-covers the boot-loaded set by one file — AMD-013 §AMD-42, deliberately not cured), `OI-C-09` (the `src/aief_stage6/**` delta AMD-013 §AMD-45 requires, which disposes TCR-001 F1), `OI-P-01…02` (session records absent; roster roles UNASSIGNED — now including the three software roles), `SOD-1` (A4 both ruled and applied, at rank-1 direction, sessions `-02` through `-06` and `-10`), and the two human-owner reservations `OQ-14` (Stage 6 authorization) and `OQ-15` (the CMP-BLOCK-006 remedy).

**Recently closed** — `OQ-B1…OQ-B5` and the three lower-order build items, by [`framework/AIEF-AMD-013`](framework/AIEF-AMD-013_Boot_Budget_Determination_and_Stage_6_Build_Constructions.md) §§AMD-42…AMD-48 (approvals `APR-012`/`APR-013`), ruled by `chief-systems-engineer · S-2026-08-08-10` — a session differing from the raiser `software.software-engineer · S-2026-08-08-07` in both role and session, as that register required: lock JSON layout, `build_provenance` as a closed six-member set, the lock self-measurement fixed point (with the deferral re-keyed on the path, disposing TCR-001 F1), archive entry types, the BINDING pin-line write form, DC-1 of empty content, the budget-totals scope, and AMD-33's run-fixed timestamp and build id. Every interim choice was adopted; one carried a substantive correction; all eight required a manifest change; registry 28 → 29. The same instrument's §AMD-41 determines CMP-BLOCK-006 without disposing it — see §8. Earlier: `OI-C-06`, by [`framework/AIEF-AMD-012`](framework/AIEF-AMD-012_DC-4_Coverage_of_Enabled_Role_Artifacts.md) §§AMD-39/AMD-40 (approvals `APR-010`/`APR-011`): DC-4's covered set now adds the agent artifacts of BINDING-enabled roles outside the selected profile, resolved deterministically from `BINDING.enabled_agents` via the manifest's new `enabled_role_coverage` rule — for this instance, exactly the three `software.*` role files, which `MANIFEST.lock`/B2a will bind once Stage 6 runs; the DC-4 worked example stands unchanged; manifest re-registered, registry 27 → 28. Earlier: `OQ-13`, by the **human owner's** recorded allocation decision, enacted by [`framework/AIEF-AMD-011`](framework/AIEF-AMD-011_Software_Role_Enablement.md) §§AMD-35…AMD-38 (approvals `APR-008`/`APR-009`): the three `software.*` roles are enabled additively in `BINDING.enabled_agents` (option (a) of AMD-010 §AMD-34), their contracts persisted at `.ai/core/profiles/software/agents/`, `active_profile` unchanged at `mechanical`, no manifest change, no implementation started. Earlier: the eleven Stage 6 pre-flight specification gaps `OQ-1…OQ-10, OQ-12`, by [`framework/AIEF-AMD-010`](framework/AIEF-AMD-010_Stage_6_Constructions_and_Preflight_Dispositions.md) §§AMD-25…AMD-33 (approvals `APR-006`/`APR-007`): DC-4 core aggregate (root files covered, lock self-excluded), DC-5 release digest, tokenizer families TF-1/TF-2, budget record in `MANIFEST.lock`, deterministic uncompressed tar distributable, compile-time checks precede Stage 6 emission, campaign scope V-01…V-25, two-execution build-time reproducibility, V-10 platforms — with `AMD-34` recording the allocation options and recommendation while reserving the choice to the human owner. Earlier: `ECR-Q-003` and `OI-C-03`, jointly, by [`framework/AIEF-AMD-009`](framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md) §§AMD-23/24 (approvals `APR-004`/`APR-005`): the Stage 1 barrier now protects the Stage 1 output set — Stage 5 lawfully emits `core/validation/**` — and MI-3's strict `files[]`-id namespace governs, with the manifest passing it. Earlier: `ECR-Q-001` and `ECR-Q-002` by [`framework/AIEF-AMD-008`](framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md) §§AMD-16/17; `OI-V-01` by [`.ai/project/verification/VER-001`](.ai/project/verification/VER-001_Independent_Verification_ECR-D-005_and_Stage_2.md) — 10 criteria, 10 PASS — dispositioned at [`.ai/project/reviews/DR-001`](.ai/project/reviews/DR-001_QA-001_Finding_Dispositions.md); `ECR-D-005` fully closed; `OI-F-01`, `OI-F-02` by AIEF-AMD-003; `CMP-BLOCK-014` by AIEF-AMD-002.

## 8 · Next Engineering Activity

> ### CAD is AUTHORISED — `LC-M04-EXIT` passes `C1`–`C7`
>
> **Next action: OPEN FUSION 360.**
>
> `C6` was closed by [`VER-017`](.ai/project/verification/VER-017_Confirmatory_Round_On_The_C6_Instrument_And_VER-016_Residue.md)
> (`qa-engineer`, `S-2026-08-10-05`, **CLEARED — 12 PASS, 0 FAIL**), which supersedes `VER-014`,
> `VER-015` and `VER-016` under the **sealed** verification-supersession relation ruled at
> [`ECR-D-012`](.ai/project/ecr/ECR-D-012_Verification_Supersession_Undeclared_And_Unbound.md) and
> approved at [`APR-028`](.ai/project/approvals/APR-028_Verification_Supersession_Relation.md).
> The superseded rounds remain on disk with their verdicts intact — supersession pins their bytes,
> so editing one now **fails** the gate rather than passing it.
>
> Session `S-2026-08-10-01` dispositioned nine ECRs against the frozen specification —
> `ECR-D-001`…`-004`, `-007`…`-011` — each ruled by the human owner, applied to `spec/**`,
> re-registered in [`FROZEN.md`](.ai/project/FROZEN.md) and bound by `APR-020`…`APR-027`.
> **All three CAD holds (H1 channel, H2 locators, H3 stubs and counterbores) are discharged.**
> `spec/**` has not changed since; `S-2026-08-10-04` touched no specification artifact.
>
> **Start here:**
> [`implementation/01_SEWCP-200_Cooling_Plate/SEWCP-200_CAD_Implementation_Package.md`](implementation/01_SEWCP-200_Cooling_Plate/SEWCP-200_CAD_Implementation_Package.md) §6.
> Read the superseded-in-part banner at its head first — the package is Rev X1 and a full Rev X2
> re-issue is `OI-P-03`. Steps 6.08, 6.27 and 6.32 no longer suppress the channel, the
> counterbores and the locators; §3.3 carries the re-clocked 75°/195°/315°; and step 6.02's
> parameter import now exists.
>
> **Verify before modelling. Nothing here is asserted; all of it computes:**
>
> ```
> PYTHONPATH=src python -m aief_gate          # C1..C7; exits 0, prints LC-M04 CAD-READY: YES
> PYTHONPATH=src python -m aief_clearance     # spec/00 s3.2 feature clearance; exits 0
> PYTHONPATH=src python -m aief_params emit   # 105 parameters, derived from package section 3
> PYTHONPATH=src python -m pytest tests/ -q   # 621 pass, 2 fail
> PYTHONPATH=src python -m aief_approval verify   # approval-chain integrity
> ```
>
> **Two of those exit non-zero, and are expected to.** The two test failures and
> `aief_approval verify` are all the same defect — `ECR-D-006`, the framework manifest, which is
> not under `spec/**` and is excluded from this gate by name in [`GATES.md`](.ai/project/GATES.md).
> Every `spec/**` row and chain resolves. Recorded at `VER-017` N-4.
>
> Four defect classes that had gone unnoticed for many sessions were each a **declared property
> with no standing check**, and each now has one: approval supersession (`aief_approval`), the
> gate criteria themselves (`aief_gate`), feature clearance (`aief_clearance`) — which found
> `ECR-D-010`, three choke stations colliding with three locators that `spec/00` §3.2 had claimed
> *"No conflicts"* about while omitting the locators from its own map — and the CAD parameter
> master (`aief_params`). `ECR-D-012` closed the **inverse** of that class: a property `C6`
> computed that no authority had declared.

> ### Framework Compiler Stage 6 — Generate Release: **NOT AUTHORIZED**
>
> A **separate lifecycle branch**, and not on the CAD path. The Stage 6 specification and
> increment are complete and certified ([`TCR-001`](.ai/project/verification/TCR-001_Stage_6_Increment_Test_Certification.md),
> [`VER-006`](.ai/project/verification/VER-006_Independent_Verification_Stage_6_Preparation_Phase.md)).
> `CMP-BLOCK-006` is **closed** by [`AIEF-AMD-014`](framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md) §AMD-52.
> Remaining gates, in order: `OI-C-09` (the `src/aief_stage6/**` delta, re-certified by a
> distinct `software.test-engineer` session), a cold QA audit of `S-2026-08-08-10` (SOD-1), and
> **`OQ-14` — explicit human authorization**. Stage 6 emits `core/MANIFEST.lock`, satisfying
> boot step B2a and writing `BINDING.core_digest_pin`.

> ### `ECR-D-006` — reserved to the human owner
>
> `framework/framework.manifest.json` does not reproduce against its registered digest. **Not a
> criterion of `LC-M04-EXIT`** — it is not under `spec/**`, and [`GATES.md`](.ai/project/GATES.md)
> records the exclusion by name. It seeks a human re-affirmation of the `AIEF-AMD-013` bytes.

---

## Maintenance

| Rule | |
|---|---|
| **No duplicated content** | This file indexes; it never restates a law, rule, specification or decision |
| **Not an authority** | Cite the canonical artifact, never this file |
| **Upgrade-durable** | Outside every framework partition; no upgrade can touch it |
| **Version-agnostic** | References `.ai/BOOT.md` and canonical indexes, never framework internals that change between versions |
| **Update trigger** | Compiler stage change · lifecycle stage change · open item opened or closed. After Stage 3, most of §7 becomes a pointer to `.ai/project/STATE.md` |
