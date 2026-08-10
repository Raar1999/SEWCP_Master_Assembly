# AIEF-AMD-011 — Architecture Amendment: Software Role Enablement

**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-01 + LAW-10 (change to the frozen core partition by addition), LAW-02 (disposition of the OQ-13 reservation), LAW-12 (every question disposed by open decision, never assumption)
**Scope:** Enactment of the human owner's OQ-13 decision — enable the three `software.*` roles in this SEWCP instance. **Nothing else.** No Stage 6 execution, no compiler implementation, no profile switch, no lifecycle change.
**Date:** 2026-08-08 · **Session:** `S-2026-08-08-05`
**Amends:** the enabled agent set of this instance (`project/BINDING.md` `enabled_agents`, `project/ROSTER.md`) and the core partition **by addition only** — three role artifacts rendered into `core/profiles/software/agents/`
**Does not amend:** `framework/framework.manifest.json` (see AMD-37) · `AIEF-FRZ-001` · `AIEF-AMD-001` … `AIEF-AMD-010` · either ADR · any schema · any law rule or clause · any existing role contract, universal or mechanical · any partition, layer, tier, boot step, stage or lifecycle definition · DC-1 … DC-5, TF-1/TF-2 — all preserved exactly as declared
**Authorising basis:** the human owner's recorded OQ-13 decision (verbatim below), `core/PRECEDENCE.md` rank 1, recorded per LAW-10 in `project/approvals/APR-008` and `project/approvals/APR-009`

---

## The human decision this instrument enacts

Recorded verbatim; the decision is the human owner's, not this instrument's:

> **"ENABLE the three software.\* roles for this SEWCP instance, following the existing AMD-006 profile-activation pattern. Do not activate them silently. The three software roles must be explicitly defined and persisted before implementation begins."**

This decides OQ-13 among the three admissible options recorded at `AIEF-AMD-010` §AMD-34 — it is option (a), the A4-recommended option. The decision closes OQ-13. It allocates no task, executes no Stage 6 work and starts no implementation; CMP-BLOCK-004 and CMP-BLOCK-005 remain open as implementation blockers.

## Independence declaration

OQ-13 was raised by `project-manager · S-2026-08-08-03c` (A3) and analysed, with the choice reserved, by `chief-systems-engineer · S-2026-08-08-04` (AMD-34). The choice itself was made by the human owner. This enactment is performed by `chief-systems-engineer · S-2026-08-08-05`, a cold session holding no state from any prior session. Under AMD-20, agent identity is the pair (role, session); raiser, analyst and enactor all differ in session, and the deciding authority is the human owner. The same-authority ruled-and-applied departure is separately recorded in § *Separation of Duties*.

| Ruling | Subject | Change class |
|---|---|---|
| AMD-35 | Enablement mechanism | Instance change — `BINDING.enabled_agents` extended additively; `active_profile` unchanged |
| AMD-36 | Persistence of the three role definitions | Additive core-partition render — three agent artifacts emitted |
| AMD-37 | Manifest | **No manifest change**, with reasons |
| AMD-38 | Roster propagation and dispatch | Instance change — `ROSTER.md` extended; dispatch precondition restated |

---

## AMD-35 — Enablement Mechanism: Additive Role Enablement, Profile Unchanged

### Ruling

> **This instance keeps `active_profile: mechanical`. The three `software.*` roles are enabled additively in `BINDING.enabled_agents`. Enabling agents is not switching the profile.**

Precisely:

1. **What changes.** `project/BINDING.md` `enabled_agents` gains `software.software-engineer`, `software.test-engineer` and `software.platform-engineer`, each at the authority level the manifest declares — **A1 for all three** (`agents.profile`, ids `software.software-engineer`, `software.test-engineer`, `software.platform-engineer`). No other BINDING field changes.
2. **What does not change.** `active_profile` remains `mechanical`; `lifecycle_stage` remains `LC-M04`; the gate topology remains terminal. The software lifecycle (LC-S01…LC-S06, recurring gates) is **not instantiated** — no `software` lifecycle artifact is emitted and no software gate exists in this instance. The compiler work the roles will eventually accept is governed by the universal laws, by `project/GATES.md` administration, and by the task packages that allocate it — not by a second, parallel lifecycle.
3. **Lawfulness.** `sch-binding` requires `enabled_agents` and constrains its content in no way; nothing binds the enabled set to the active profile's agent list — the AMD-006 precedent already extended it beyond the profile's original three roles. The change authority is settled by AMD-34: an A4 instrument plus a recorded LAW-10 human approval, then the BINDING edit. Both are present (this document; `APR-008`).

### Reconciliation with MI-9

MI-9 — *every profile declares a complete agent set and lifecycle stage set* — is a **manifest-declaration invariant** and is untouched: the `software` profile remains completely declared in `framework.manifest.json` (three agents, six lifecycle stages), exactly as it passed MI-9 at AMD-001. Enabling roles in one instance's BINDING changes no profile declaration. MI-8 is likewise untouched: no discipline tag is added to any universal role.

### Reconciliation with the zero-dead-file rule — tension recorded, not glossed

`AIEF-FRZ-001:80`: *"Compiler Stage 1 emits a distributable containing the universal core plus the selected profile only. A software installation therefore contains no mechanical role."*

**The rule constrains what Stage 1 emits for a selected profile.** It governs the compiler's automatic emission, and it is why this mechanical installation was emitted with no `software` artifacts. It does not address, and therefore does not prohibit, an explicit A4-ruled, human-approved role enablement — the AMD-006 mechanism, which is precisely how `mechanical.cad-engineer` entered a tree whose Stage 1 output had three profile roles. The three artifacts emitted here are not dead files in the ECR F-01 sense: each has live consumers — `BINDING.enabled_agents` binds the role, `ROSTER.md` rosters it, and role dispatch loads it as T2.

**The honest tension, recorded rather than glossed:**

| # | Tension | Consequence |
|---|---|---|
| 1 | This tree is no longer byte-identical to a pure mechanical Stage 1 emission: it carries three artifacts the mechanical render does not produce | A future Stage 1 re-render or wholesale core replacement (upgrade) will **not reproduce** the three files; they must be re-emitted under this instrument's authority after any such operation. Recorded as **OI-C-06** |
| 2 | DC-4 as declared covers `core/profiles/<selected>/**` — for this instance, `core/profiles/mechanical/**`. The three software artifacts sit **outside DC-4's declared coverage** | When Stage 6 runs, `core/MANIFEST.lock` and boot step B2a will not bind or verify these three files. Before Stage 6 executes, either a future A4 ruling extends DC-4 coverage to enabled-role artifacts, or the enablement is folded into the build's emitted set. Not resolved here — resolving it belongs with the Stage 6 implementation this enablement exists to staff. Recorded in **OI-C-06** |

Neither consequence is hidden by this instrument; both are carried as open items with owners.

---

## AMD-36 — Persistence: Three Agent Artifacts Rendered Into `core/profiles/software/agents/`

### Ruling

> **The three role definitions are persisted at the exact paths `framework.manifest.json` `files[]` already declares for them** — following where the mechanical profile's agent files live and the structure the AMD-006 release (`7c530f4`) used:

| Manifest `files[]` id | Emitted path |
|---|---|
| `soft-agt-software` | `core/profiles/software/agents/AGT-software-engineer.md` |
| `soft-agt-test` | `core/profiles/software/agents/AGT-test-engineer.md` |
| `soft-agt-platform` | `core/profiles/software/agents/AGT-platform-engineer.md` |

1. **Content is derived, not invented.** Each artifact is rendered solely from its `agents.profile` contract in the manifest — all twelve contract fields, nothing added, nothing softened. Every declared forbidden action is carried verbatim, including `software.test-engineer`'s declared duty conflict: **may not test code it authored** — the structural guarantee that the compiler's tests are not certified by their author.
2. **Format** follows the sibling on-disk agent files (`core/profiles/mechanical/agents/AGT-*.md`) and satisfies every `tpl-agent-specification` required section: Responsibilities, Inputs, Outputs, Allowed actions, Forbidden actions, Escalation rules, Authority level and Capability tags (the latter two in the header tables, as in every sibling), with at least one forbidden action per role and conformance to `SCH-agent`'s required fields.
3. **Header deviation, flagged rather than silently chosen** (AMD-006 deviation-recording precedent): the sibling files carry *"Emitted by aief-compile Stage 1"*. That would be false here — Stage 1 for this instance selected `mechanical`. The three headers state the true provenance: rendered from the manifest under AIEF-AMD-011, approval APR-008. A future full re-render that emits these files as compiler output may restore the standard header line.
4. **What is deliberately not emitted:** `core/profiles/software/PROFILE.md` and the six `lifecycle/LC-S*` artifacts. The software profile is not activated (AMD-35); those artifacts would have no consumer in this instance — exactly the dead-file condition ECR F-01 exists to prevent. If a future decision activates the software lifecycle anywhere, that is a new instrument.

### Change class

**Addition to the frozen core partition.** LAW-01 clause 2 extends the freeze to `core/`; B2a does not yet exist (Stage 6 outstanding), but the freeze is a law, not a check. The addition is therefore made only under this approved instrument and the recorded human approval `APR-008` (LAW-01 clause 4 pattern). **Zero existing core bytes change** — the change is three new files; every pre-existing `core/**` artifact is byte-identical before and after.

---

## AMD-37 — Manifest: No Amendment Required

### Ruling

> **`framework/framework.manifest.json` is not amended.** Its registered DC-1 digest `ae16ccaca5746b81a2a992841fc1d239fd1c8b0c34657c05611e025a9d8395aa` is unchanged; `APR-006`'s hash binding remains valid; no re-registration occurs.

Reasons, enumerated against everything an enablement could need:

| Needed for enablement | Manifest state | Amendment needed? |
|---|---|---|
| The three role contracts | `agents.profile` declares all three in full twelve-field form | No |
| The software profile declaration | `profiles[software]` complete — three agents, six lifecycle stages, MI-9 PASS since AMD-001 | No |
| `files[]` entries for the three emitted artifacts | Already declared: `soft-agt-software`, `soft-agt-test`, `soft-agt-platform`, generator 1, profile-scoped `["software"]`, integrity hashed | No |
| Authority levels for the BINDING rows | Declared per contract: A1, A1, A1 | No |
| An enablement mechanism field | Enablement is instance state; `binding` is the declared carrier (`sch-binding.enabled_agents`) | No |

The change is **instance-level**: `BINDING.md`, `ROSTER.md` and the rendering of already-declared artifacts. This follows the AMD-21 and AMD-34 precedent — an authority ruling that requires no manifest change makes none. Contrast AMD-006, which had to amend the manifest because the role it added **did not exist** in it; the three software roles have existed in the manifest since AIEF 1.0.0.

**Residual, stated plainly:** the three `files[]` entries are declared with `generator: 1` and `profile_scope: ["software"]` — the manifest still describes them as Stage 1 output of a software-profile build, not as enabled additions to a mechanical instance. That description is accurate for the framework in general and silent about this instance, as `files[]` is profile-generic by design. No field exists to record per-instance enablement in the manifest, and inventing one would be a schema change this decision does not require. The instance-level record is `BINDING.md`, `ROSTER.md` and this instrument.

---

## AMD-38 — Roster Propagation and the Dispatch Precondition

### Ruling

> **`project/ROSTER.md` gains a `Profile software` section with the three roles, each `UNASSIGNED`** — the roster's own convention, followed exactly. **No human identity is invented.**

1. The roster's standing rule is restated, not weakened: *a role marked UNASSIGNED cannot be dispatched; assignment is a `project-manager` action.* The three roles are therefore **enabled but not dispatchable** until either the project-manager records an assignment or a rank-1 live human instruction directs a dispatch — the OI-P-02 pattern, under which three universal roles have already been lawfully dispatched at rank 1 with the roster gap recorded. OI-P-02 now also covers these three rows.
2. Consequence for the blocker ledger: CMP-BLOCK-004 and CMP-BLOCK-005 keep Authority "Software" in substance but the authority now **resolves to enabled roles** — the work has somewhere lawful to land. The blockers remain OPEN: they are implementation blockers, and this instrument implements nothing.

---

## Blast Radius

| Artifact | Change | Method |
|---|---|---|
| `core/profiles/software/agents/AGT-software-engineer.md` | **NEW** — role contract | Rendered from manifest `agents.profile` |
| `core/profiles/software/agents/AGT-test-engineer.md` | **NEW** — role contract | Rendered from manifest `agents.profile` |
| `core/profiles/software/agents/AGT-platform-engineer.md` | **NEW** — role contract | Rendered from manifest `agents.profile` |
| `project/BINDING.md` | `enabled_agents` 9 → 12 | Surgical edit — instance artifact |
| `project/ROSTER.md` | `Profile software` section, three UNASSIGNED rows | Surgical edit — instance artifact |
| `project/FROZEN.md` | This instrument registered, 26 → 27; aggregate recomputed under DC-2 | Registry edit under APR-009 |
| `project/STATE.md` | `frozen_set_hash`, `open_non_blocking`, `next_action` | Session close write |
| `project/OPEN_ITEMS.md` | OQ-13 closed; OI-C-06/OI-C-07 opened; CMP-BLOCK-004/-005 authority annotated | Register edit |
| `ENGINEERING.md` | Index rows: amendment count, agents count, open/closed lists, next activity | Index edit |
| `project/approvals/APR-008`, `APR-009` | **NEW** — the two recorded approvals | LAW-10 |

**Core artifacts deliberately not edited, consequences recorded:**

| Artifact | Status | Consequence |
|---|---|---|
| `core/agents/INDEX.md` | **Not hand-edited** — generated core artifact | Its role tables list only universal + mechanical roles; the three enabled `software.*` roles are absent (its Separation-of-duties list, rendered from the full manifest, already names `software.test-engineer`'s conflict). Until a Stage 1 re-render, a strict V-22 reading — provenance roles must resolve *in `core/agents/INDEX.md`* — does not resolve the three role tokens; they resolve in the manifest, `BINDING.md` and `ROSTER.md`. V-22 is declared, not implemented (CMP-BLOCK-005). Recorded as **OI-C-07**; re-emission path: Stage 1 re-render, compiler work (CMP-BLOCK-004) |
| `core/profiles/mechanical/**` | Untouched | None |
| All other `core/**` | Untouched — zero bytes changed | None |

**The five universal roles and four mechanical roles are untouched. The universal registry remains frozen at five for MAJOR version 1.**

---

## Separation of Duties — Recorded Tension

`core/agents/INDEX.md`: **`chief-systems-engineer` may not implement what it approved.** This instrument was ruled, and its BINDING, roster, registry and emission actions applied, by the same authority (`chief-systems-engineer · S-2026-08-08-05`) at the direction of the human owner — `core/PRECEDENCE.md` rank 1, which outranks the rank-6 agent specification. Identical in form to the departures recorded in AMD-008, AMD-009 and AMD-010 §§ *Separation of Duties*; identically **authorised, not erased** (SOD-1).

| | |
|---|---|
| Duty separated | A4 rules and approves; A1 implements |
| Departure | A4 both ruled and applied |
| Authority for the departure | The human owner's recorded OQ-13 decision, rank 1, recorded per LAW-10 in APR-008 and APR-009 |
| Mitigating control | Independent cold-context `qa-engineer` audit of this session's work — follows immediately, dispatched by the same directing authority |
| Not mitigated by | Anything this document says about itself. Under LAW-05 an authority's assertion about its own work carries no evidentiary weight |

---

## Artifacts Not Modified

| Artifact | Status |
|---|---|
| `framework/framework.manifest.json` | **Unmodified** — AMD-37. DC-1 unchanged; APR-006 binding remains valid |
| `AIEF-FRZ-001` | Unmodified. One phrase's scope clarified in ruling (AMD-35: line 80 constrains Stage 1 emission); **no supersession in reading is required** — the rule is not contradicted, it is inapplicable to an approved enablement. Bytes and DC-1 digest unchanged |
| `AIEF-AMD-001` … `AIEF-AMD-010`, both ADRs | Unmodified |
| `SCH-framework-manifest.schema.json`, every emitted schema | Unmodified |
| DC-1 … DC-5, TF-1/TF-2 | Preserved exactly as declared |
| All 13 laws, 5 universal roles, 4 mechanical roles, 6 workflows, 10 templates | Unmodified |
| Every pre-existing `.ai/core/**` byte, `.ai/adapters/**` | Untouched (three **new** files added under `core/profiles/software/agents/`; re-emission of stale artifacts remains compiler work — OI-C-02, OI-V-07, OI-C-07) |
| `core/MANIFEST.lock` | **Not created.** Compiler Stage 6 is not executed, and remains unauthorized (OQ-14, reserved to the human owner) |
| `project/ledger/**` | **Not written.** `HEAD` remains at `genesis`; `L-0000001` does not exist |
| `spec/**`, every implementation package, all CAD | Not touched |
| Git history, tags, author or committer identity | **Not touched.** No commit, tag or push is made by this session |

## Approvals Required and Recorded

| Change | Approval | Bound to |
|---|---|---|
| The enablement this instrument rules — BINDING edit, roster edit, emission of the three role artifacts | `project/approvals/APR-008` | this document's DC-1 digest; the three emitted artifacts' DC-1 digests enumerated in its body; `BINDING.md` post-change content fingerprint recorded informationally |
| Freeze-registry addition of this document (AMD-21 criterion: authorising instrument for a change to a frozen artifact — the core partition) | `project/approvals/APR-009` | this document's DC-1 digest |

Per the AMD-16 design property, neither this document's own digest nor the post-registration DC-2 aggregate appears in this document; both live in the registry and the approval artifacts.

---

**END OF AIEF-AMD-011**
