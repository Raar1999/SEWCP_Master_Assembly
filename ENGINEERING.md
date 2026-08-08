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
| **Governing framework** | AIEF 1.0.0 — **FROZEN**, nine amendments |
| **Active profile** | `mechanical` |
| **Active host adapter** | `claude-code` |
| **Repository release** | **v0.9.0** — annotated tag on the state-synchronization commit after `655aa75`, verified by `git describe --tags --exact-match HEAD` |

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
| 5 | Generate Validation | ⏳ **outstanding — NEXT** |
| 6 | Generate Release | ⏳ outstanding — **gates boot step B2a** |

## 7 · Engineering Status

> **Authoritative source: [`.ai/project/STATE.md`](.ai/project/STATE.md).** The table below is a convenience pointer. Where they differ, `STATE.md` governs.

| Item | State |
|---|---|
| Lifecycle stage | `LC-M04` Implementation · gate `LC-M04-EXIT` **BLOCKED** |
| Specification | Rev A frozen, 9 components, 142 requirements |
| Framework | AIEF 1.0.0 frozen, **nine amendments**; Stages 1, 2, 3, 4 emitted |
| Agents | 5 universal + 4 `mechanical` profile, all persisted on disk |
| Frozen set | **25** artifacts hash-registered in [`.ai/project/FROZEN.md`](.ai/project/FROZEN.md); aggregate computed under DC-2 |
| Ledger | genesis, `HEAD.seq = 0`, reconciled with `STATE`. No LAW-09 close has been performed |
| Repository | **v0.9.0**, `HEAD == origin/main`. All session work through AIEF-AMD-009 and VER-002 is committed: `d07e931` (Release 0.8 — Stage 2 templates + AMD-008 state, manifest at APR-002's subject `636cf22b…`) and `655aa75` (AMD-009 state, manifest at APR-004's subject `9611d547…`, AMD-009 at APR-005's subject `86c8be7f…`) |

> **Approval provenance.** Each approval's subject is recoverable as a git object: `git show d07e931:framework/framework.manifest.json` normalises to APR-002's `subject_hash`; `git show 655aa75:framework/framework.manifest.json` to APR-004's; `git show 655aa75:framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md` to APR-005's. This discharges VER-002 findings FIND-Q2-2 and FIND-Q2-3.

**Open items — authoritative list: [`.ai/project/OPEN_ITEMS.md`](.ai/project/OPEN_ITEMS.md)**

| ID | Item | Blocks |
|---|---|---|
| ECR-D-001…004 | Defects in the frozen SEWCP specification, recorded in [`implementation/01_SEWCP-200_Cooling_Plate/SEWCP-200_CAD_Implementation_Package.md`](implementation/01_SEWCP-200_Cooling_Plate/SEWCP-200_CAD_Implementation_Package.md) §12 | CAD modelling of SEWCP-200 |
| CMP-BLOCK-004 / -005 | Compiler not implemented as software; verification infrastructure absent | Stage 6, V-09/V-12/V-15/V-18 |
| C-4 | `LICENSE` is an unresolved placeholder | Public or external release |
| CDR-C3 | Independent cold-context ratification of the AIEF CDR not performed | Recorded residual risk, AIEF-FRZ-001 §6.2 |

**Open, not blocking** — `OI-V-02` (`V-24` declared but not implemented), `OI-V-03` (all session `S-2026-08-08-02` work is unverified), `OI-R-01` (no `v0.2.0` tag), `OI-C-01…02` (ledger schema; `ADP-ci` stale at 22 checks), `OI-C-04…05` (`implementation/` BOMs; `referenced_by` completeness undeclared), `OI-P-01…02` (session records absent; roster roles UNASSIGNED), `SOD-1` (A4 both ruled and applied, at rank-1 direction, sessions `-02` and `-03`).

**Recently closed** — `ECR-Q-003` and `OI-C-03`, jointly, by [`framework/AIEF-AMD-009`](framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md) §§AMD-23/24 (approvals `APR-004`/`APR-005`): the Stage 1 barrier now protects the Stage 1 output set — Stage 5 lawfully emits `core/validation/**` — and MI-3's strict `files[]`-id namespace governs, with the manifest passing it. Earlier: `ECR-Q-001` and `ECR-Q-002` by [`framework/AIEF-AMD-008`](framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md) §§AMD-16/17; `OI-V-01` by [`.ai/project/verification/VER-001`](.ai/project/verification/VER-001_Independent_Verification_ECR-D-005_and_Stage_2.md) — 10 criteria, 10 PASS — dispositioned at [`.ai/project/reviews/DR-001`](.ai/project/reviews/DR-001_QA-001_Finding_Dispositions.md); `ECR-D-005` fully closed; `OI-F-01`, `OI-F-02` by AIEF-AMD-003; `CMP-BLOCK-014` by AIEF-AMD-002.

## 8 · Next Engineering Activity

> ### Framework Compiler Stage 5 — Generate Validation
>
> **Both gating dispositions are complete** (AIEF-AMD-009, approvals APR-004/APR-005): `ECR-Q-003` is closed — the Stage 1 barrier protects the Stage 1 output set, so Stage 5 lawfully emits `core/validation/**`, its own declared subtree — and `OI-C-03` is closed — the manifest now passes `MI-3` under the governing strict reading, so `V-01` no longer halts.
>
> Emit `core/validation/CHECKS.md` and `core/validation/MANIFEST` from `manifest.validation`, **25 checks**. Stage barrier: *a law declared machine-checkable with no bound check halts the build.* Note **CMP-BLOCK-005** — the tokenizer, multi-platform and concurrency infrastructure that several checks depend on is absent.
>
> Stage 5 is where three declared-but-unimplemented checks become real: **V-23** stage monotonicity, **V-24** freeze registry (**OI-V-02**), **V-25** encoding conformance. All three are declared in the manifest by AIEF-AMD-008 §AMD-19 and none is implemented.

**Then: Stage 6 Release** (emits `core/MANIFEST.lock`, satisfying boot step B2a, and writes `BINDING.core_digest_pin`).

**Neither ECR-D-005 nor Stage 2 will unblock the `LC-M04-EXIT` gate.** That gate is held by ECR-D-001…004 — four defects in the frozen SEWCP specification — which are Design Authority decisions, not compiler work.

---

## Maintenance

| Rule | |
|---|---|
| **No duplicated content** | This file indexes; it never restates a law, rule, specification or decision |
| **Not an authority** | Cite the canonical artifact, never this file |
| **Upgrade-durable** | Outside every framework partition; no upgrade can touch it |
| **Version-agnostic** | References `.ai/BOOT.md` and canonical indexes, never framework internals that change between versions |
| **Update trigger** | Compiler stage change · lifecycle stage change · open item opened or closed. After Stage 3, most of §7 becomes a pointer to `.ai/project/STATE.md` |
