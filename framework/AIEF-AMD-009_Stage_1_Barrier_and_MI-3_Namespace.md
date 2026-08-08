# AIEF-AMD-009 — Architecture Amendment: Stage 1 Emission Barrier and MI-3 Namespace

**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-02 (ECR-Q disposition), LAW-01 + LAW-10 (frozen artifact change)
**Scope:** ECR-Q-003 and OI-C-03 (FIND-9). **Nothing else** — directed scope, live human-owner instruction of session `S-2026-08-08-03`
**Date:** 2026-08-08 · **Session:** `S-2026-08-08-03`
**Amends:** `framework/framework.manifest.json`
**Does not amend:** `AIEF-FRZ-001` (one row is superseded in reading, not edited — see AMD-23) · `AIEF-AMD-001` … `AIEF-AMD-008` · `SCH-framework-manifest.schema.json` · any law rule or clause · any role contract · any partition, layer, tier, boot step or stage definition
**Authorising basis:** live human-owner instruction (`core/PRECEDENCE.md` rank 1), recorded per LAW-10 in `project/approvals/APR-004` and `project/approvals/APR-005`

**Supersedes:** the reading of one barrier row of `AIEF-FRZ-001` Part 4 Stage 1, as ruled in AMD-23. Two rulings, AMD-23 and AMD-24.

---

## Independence declaration

ECR-Q-003 was raised by `chief-systems-engineer` · `S-2026-08-08-02`. OI-C-03 was recorded by the same session (AMD-008 §AMD-18, FIND-9), which explicitly declined to rule on it. Under AMD-20, agent identity for LAW-02 independence is the pair **(role, session)**. This ruling is made by `chief-systems-engineer` · `S-2026-08-08-03`, a cold session holding no inherited state from `S-2026-08-08-01` or `-02`. The independence requirement of `tpl-ecr` acceptance condition 3 and LAW-02 clause 5 is satisfied. The residual weakness of a same-role, different-session ruling recorded in AMD-20 applies here identically; the mitigating control is the independent cold-context QA audit of this session's work, dispatched by the same human instruction that directed these dispositions.

---

## AMD-23 — Stage 1 Emission Barrier

**Disposes:** ECR-Q-003 · **Disposition: A — the barrier protects the Stage 1 output set, not the `core/` prefix**
**Ruled by:** `chief-systems-engineer` · `S-2026-08-08-03`

### Finding, restated

`generation_order[stage 1].barrier` declared *"No later stage may emit into core"*. The manifest's own `generation_order` declares `core/templates/**` (Stage 2), `core/validation/**` (Stage 5) and `core/MANIFEST.lock` (Stage 6) as later-stage outputs, corroborated by `files[]` entries carrying `partition: core` with `generator: 2`, `5` and `6`. Under the literal reading, Stage 2 — recorded complete with its barrier satisfied — retrospectively violated the Stage 1 barrier, and Stages 5 and 6 cannot run at all. `AIEF-FRZ-001` Part 4 Stage 1 carries the same wording (*"No later stage may emit into `core/`"*).

### Ruling

> **The barrier protects Stage 1's output set from later modification. It was never a prohibition on later stages emitting into their own declared `core/` subtrees.**
>
> Precisely: no later stage may emit into or modify any path Stage 1 emits. Stage 1 owns `BOOT.md`, `FRAMEWORK.md`, `README.md`, `core/profiles/<selected>/**`, and `core/**` **excluding** the later-stage subtrees `core/templates/**` (Stage 2), `core/validation/**` (Stage 5) and `core/MANIFEST.lock` (Stage 6). Each stage emits only into its own declared outputs.

The predicate is compiler-evaluable: **the `outputs` path sets of the six stages are pairwise disjoint after applying the declared exclusions.** A declared field write into an already-emitted artifact — the Stage 6 `core_digest_pin` write into `project/BINDING.md`, declared as such by AMD-18 — is not an emission and does not violate disjointness.

### Why A and not B or C

| # | Resolution | Judgement |
|---|---|---|
| A | Barrier protects the Stage 1 output set | **Adopted.** The only reading consistent with every declared output, with the layer table (`FRAMEWORK.md` § Layers: L2, L6, L7 live in `core` and are emitted by Stages 2, 5, 6), with the completed and verified Stage 2, and with Stage 6's own barrier (*"`MANIFEST.lock` is emitted only here"*), which is meaningless unless Stage 6 may emit into `core/` |
| B | Literal reading; the outputs of Stages 2, 5, 6 are wrong | **Rejected.** Retroactively invalidates Stage 2's verified completion (VER-001, 10/10 PASS), contradicts the frozen layer model, and leaves L2, L6 and L7 with no emission target. A reading that convicts the architecture's own declared structure is not an interpretation of it |
| C | Strike the barrier | **Rejected.** Loses the real protection: without it a later stage may overwrite Stage 1 output. The defect was imprecision, not wrongness; the cure is precision, not deletion |

### Retrospective consequence, stated plainly

Under this ruling **Stage 2's completion is conforming** — it emitted only `core/templates/**`, its own declared subtree. No completed work is invalidated and no re-emission is required.

### Treatment of `AIEF-FRZ-001`

`AIEF-FRZ-001` Part 4 Stage 1 barrier row carries the superseded wording. Following the supersession precedent of `AIEF-AMD-001` §AMD-04 (which superseded `AIEF-ARCH-001` §7.4 without editing it): **the row's reading is superseded by this ruling; the document is not edited.** Its bytes, its DC-1 digest `a1b0a51c…450023f4` and its registry entry are unchanged. Editing a frozen freeze document in place would destroy the audit record; the amendment mechanism exists precisely so that frozen text is corrected by registered instrument, not by mutation.

### Manifest change

| Location | Change |
|---|---|
| `generation_order[stage 1].barrier` | Replaced with the precise ruling text above |
| `generation_order[stage 1].outputs` | `"core/**"` qualified with the three later-stage exclusions, so the declared output sets are disjoint as written |
| `validation[V-01].verifies` | Extended with the stage-output disjointness predicate, so the barrier is bound to a declared BLOCKING compile-time check rather than left as prose — the AMD-19 lesson: *a ruling without a check is a convention; only a check is a control* |

---

## AMD-24 — MI-3 Namespace

**Disposes:** OI-C-03 (FIND-9) · **Disposition: the strict reading governs**
**Ruled by:** `chief-systems-engineer` · `S-2026-08-08-03`

### Finding, restated

MI-3 (`AIEF-FRZ-001` §3.3): *"Every `depends_on` and `referenced_by` target exists."* The invariant does not declare the namespace in which targets must exist. Two entries fail the strict reading: `files[boot].referenced_by` contained `framework`, which is no id in any declared namespace, and `files[sch-state].referenced_by` contained `V-06`, a validation-check id. Present identically at commit `6ce3508`; introduced by no recent session.

### Ruling

> **MI-3's targets range over `files[]` ids only.** For every `files[]` entry, every member of `depends_on` and every member of `referenced_by` is the `id` of a `files[]` entry. No other namespace — checks, laws, schemas, templates, sections — satisfies MI-3.

Four grounds, each independently sufficient:

1. **`depends_on` is unambiguous already.** AMD-02 §AMD-07 rules `depends_on` a build-order relation between emitted files; its targets can only be `files[]` ids. One invariant sentence governs both fields; a single sentence carries a single domain.
2. **AMD-18 has already construed `referenced_by`** as *"file ids that cite it"* and edited it on that construction (`binding.referenced_by` gained three file ids). The precedent is in force and registered.
3. **A checkable invariant needs a decidable domain.** *"Exists in some namespace"* makes MI-3 satisfiable by coincidence of names across unrelated namespaces — a token `V-06` would pass or fail depending on what checks happen to exist. That is not an integrity property.
4. **`SCH-framework-manifest`** ties MI-3 to the dependency graph over manifest section 7 — a graph whose nodes are files.

### Corrections, each tested on its merits

| Entry | Token | Test applied | Correction |
|---|---|---|---|
| `files[boot].referenced_by` | `framework` | Resolves to no id in any namespace. The nearest candidate, `framework-md`, was tested and **rejected**: the emitted `FRAMEWORK.md` does not cite `BOOT.md`, so substitution would encode a false citation. The intended referent is unrecoverable from the repository and is **not guessed** (AMD-20 discipline) | Removed. `referenced_by: []`. A dangling token resolves to nothing and therefore carries no recoverable information; nothing is lost |
| `files[sch-state].referenced_by` | `V-06` | A real relation in the wrong namespace — the check does cite the schema. The relation is already carried where it belongs: `validation[V-06]` declares the check against its target, and MI-7 (*every schema referenced by a check exists*) governs the check→schema direction | Removed. `referenced_by: ["state"]`. **No relationship is lost** — the AMD-18 preservation discipline holds |

### What is *not* ruled, recorded rather than absorbed

**MI-3 tests resolution, not completeness.** An under-inclusive `referenced_by` violates nothing. Observed while ruling: `BOOT.md` is cited by the emitted content of `adp-claude-code`, `adp-chatgpt`, `adp-generic-llm`, `readme` and `core/CONTEXT_TIERS.md`, yet `boot.referenced_by` is now empty; no completeness invariant exists to make that a defect. Whether `referenced_by` should be complete — and whether the adapters' `depends_on: ["adapters-index", "boot"]` edges are themselves citations miscoded as build order (the FIND-1 class, forward-directed so V-23-invisible) — is outside the directed scope and is **recorded as OI-C-05** for a later authority. Ruling it here would repeat the scope breach this amendment's own independence rests on avoiding.

### Manifest change

| Location | Change |
|---|---|
| `files[boot].referenced_by` | `["framework"]` → `[]` |
| `files[sch-state].referenced_by` | `["state", "V-06"]` → `["state"]` |
| `validation[V-01].verifies` | Extended with the MI-3 namespace rule, binding the ruling to the declared BLOCKING compile-time check |

**Consequence:** the manifest now passes MI-3 under the strict reading — verified over all 106 `files[]` entries, 125 `depends_on` targets and every `referenced_by` member. The V-01 halt condition recorded in OI-C-03 is discharged.

---

## Architecture Decisions versus Implementation

Recorded so the boundary is explicit, per the directing instruction.

| Class | Content | Status |
|---|---|---|
| **Architecture decision** (A4, this instrument) | The barrier's meaning (AMD-23); the supersession of the FRZ-001 Part 4 Stage 1 barrier reading; MI-3's namespace (AMD-24); the V-01 text extensions binding both rulings to a check | **Ruled here** |
| **Implementation applied here** (mechanical application of the rulings) | Four field edits in `framework.manifest.json`; DC-1 recomputation of the manifest and of this document; registry re-registration and DC-2 recomputation; register and state updates | **Applied**, at rank-1 direction — see § Separation of Duties |
| **Implementation deferred downstream** | Compiler evaluation of the barrier predicate and the extended V-01 — requires `aief-compile` as software: **CMP-BLOCK-004**, a Stage 6 / compiler-infrastructure requirement. Implementation of V-23, V-24, V-25 and the tokenizer/multi-platform/concurrency infrastructure several checks need: **CMP-BLOCK-005**, a Stage 5 requirement | **Not resolved here.** Both blocks remain open and blocking exactly as recorded in `OPEN_ITEMS.md`; this amendment neither narrows nor discharges them |

Compiler Stage 5 is **not executed** by this amendment. `core/validation/**` is not emitted, no check is implemented, and no `core/**` path is touched.

---

## Blast Radius

Determined by inspecting what renders each changed manifest section.

| Changed section | Rendered by | Effect |
|---|---|---|
| `generation_order[1].barrier`, `.outputs` | No `files[]` entry carries `content_ref: generation_order` | **None** |
| `files[boot].referenced_by`, `files[sch-state].referenced_by` | Nothing — no emitted artifact renders a dependency or citation list (AMD-008 blast-radius search, still valid) | **None** |
| `validation[V-01].verifies` | `core/validation/CHECKS.md` — **Stage 5, not emitted**. `adapters/ADP-ci.md` is already stale at 22 checks (OI-C-02); check **count** is unchanged at 25, so its staleness is neither created nor worsened here | **None new** |

`ENGINEERING.md` §8 quotes the superseded barrier wording; it is an index, holds no authority, and is updated in the same session as routine index maintenance.

---

## Separation of Duties — Recorded Tension

`core/agents/INDEX.md`: **`chief-systems-engineer` may not implement what it approved.** This amendment was ruled and its manifest edits applied by the same authority (`chief-systems-engineer` · `S-2026-08-08-03`) at the direction of the human owner — rank 1, which outranks the rank-6 agent specification. Identical in form to the departure recorded in AMD-008; identically **authorised, not erased**. Mitigating control: the independent cold-context `qa-engineer` audit of this session's work, dispatched by the same directing instruction, whose report is filed in `project/verification/`. Under LAW-05, nothing this document says about its own correctness is evidence.

---

## Artifacts Not Modified

| Artifact | Status |
|---|---|
| `AIEF-FRZ-001` | **Unmodified.** One barrier row superseded in reading (AMD-23); bytes and digest unchanged |
| `AIEF-AMD-001` … `AIEF-AMD-008`, both ADRs | Unmodified |
| `SCH-framework-manifest.schema.json` | Unmodified — every change lands in existing string fields or arrays the schema already admits |
| All 13 laws, 5 universal roles, 4 profile roles, workflows, schemas, templates | Unmodified |
| `core/**`, `core/validation/**`, `core/MANIFEST.lock` | **Not touched, not created.** Stage 5 and Stage 6 are not executed |
| `project/ledger/**` | **Not written.** `HEAD` remains at `genesis`; `L-0000001` does not exist |
| Git history, tags, author or committer identity | **Not touched.** No commit, tag or push is made by this session |

## Approvals Required and Recorded

| Frozen-artifact change | Approval | Bound to |
|---|---|---|
| `framework/framework.manifest.json`, four field edits | `project/approvals/APR-004` | its post-amendment DC-1 digest |
| Freeze-registry addition of this document (AMD-21 criterion: authorising instrument) | `project/approvals/APR-005` | this document's DC-1 digest |

Per LAW-01, LAW-10 and `core/PRECEDENCE.md` clause 4: a rank-1 override of rank 3 is recorded as an approval artifact before dependent work is committed.

---

**END OF AIEF-AMD-009**
