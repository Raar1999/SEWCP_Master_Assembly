# ECR-Q-001 — Freeze-set aggregate construction is undefined

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised during execution of ECR-D-005 disposition A, session `S-2026-08-08-01`.

```yaml
ecr_id:       ECR-Q-001
class:        Q                      # ambiguity - LAW-02
raised_by:    role-unrecorded · S-2026-08-08-01
status:       CLOSED
disposition:  A - DECLARE THE CONSTRUCTION EXPLICITLY
ruled_by:     chief-systems-engineer · S-2026-08-08-02
instrument:   AIEF-AMD-008 §AMD-16
approval:     approvals/APR-002_Amend_Framework_Manifest_AMD-008.md
affected_artifacts:
  - framework/framework.manifest.json
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-08T01:31:23Z
closed_at:    2026-08-08T02:36:52Z
```

> **`raised_by` was recorded as `claude-code session S-2026-08-08-01`.** Corrected under `AIEF-AMD-008` §AMD-20: an actor-provenance field names a framework role and a session, never a model, vendor, product or host adapter — and `tpl-ecr` already declared the grammar `role, identity, session`. The role is recorded as `role-unrecorded` because **no role assignment for session `S-2026-08-08-01` is recoverable from the repository**: `project/sessions/` is empty and no session summary was filed. It is not guessed. Recorded as **OI-P-01**.

---

## 1 · Class

**Q — ambiguity.** No specification exists for how the freeze-set aggregate is constructed. Nothing is contradictory and nothing is provably wrong; the method is simply absent. Under LAW-02 an ambiguity is raised as ECR-Q and does not by itself stop unrelated work.

## 2 · Affected artifacts

| Artifact | Role |
|---|---|
| `.ai/project/FROZEN.md` § Aggregate | Records an aggregate value with no declared construction |
| `.ai/project/STATE.md` field `frozen_set_hash` | Mirrors the first 32 characters of that value |
| `core/schemas/SCH-state.schema.json` | Declares `frozen_set_hash` **required**, severity BLOCKING |

## 3 · Evidence

### 3.1 The recorded value is not reproducible

Thirteen candidate constructions were computed over the **registered** (pre-ECR-D-005) digest set and compared against the recorded aggregate `42bce7b0de019f854f99387edfc901b054b540f829bfe365e003be96892d5847`:

| Family | Constructions tested | Result |
|---|---|---|
| Concatenated hex digests | registry order · sorted by digest · sorted by path | no match |
| Newline-joined digests | as-is · sorted | no match |
| Path + digest lines | `path digest\n` · `digest  path\n` | no match |
| Raw 32-byte digests | registry order · sorted | no match |
| Concatenated normalised file **contents** | at `a45823d` and at `HEAD`, registry order and sorted | no match |
| `FROZEN.md` self-hash | at `a45823d` and at `HEAD` | no match |

**Thirteen of thirteen fail.** The per-artifact normalisation, by contrast, reproduces 15 of 16 registered digests exactly (16 of 16 after ECR-D-005 disposition A), which establishes that the hashing method and tooling are sound. The failure is specific to the aggregate.

### 3.2 No construction is declared anywhere

A repository-wide search for `aggregate` and `frozen_set_hash` returns:

- `FROZEN.md` — declares normalisation for **per-artifact** hashes only, then states the aggregate value under a bare `## Aggregate` heading with no method.
- Every other hit — `.ai/FRAMEWORK.md`, `AIEF-FRZ-001` §§ 1.7 / B2a / V-10, `BOOT.md`, `SCH-core-manifest`, `framework.manifest.json` — refers to the aggregate digest of **`core/MANIFEST.lock`**, emitted by Compiler Stage 6 and covering the `core/` partition. That is a different set and a different artifact.
- `SCH-state.schema.json` — requires the field, describes it only as "Required field of sch-state".

The project freeze set has no declared aggregate construction, and no check binds it. Note the coverage gap this exposes: **B2a guards `core/` only.** The `framework/` and `spec/` artifacts are guarded solely by `FROZEN.md`, whose aggregate is unverifiable — which is precisely why ECR-D-005 went undetected across three releases.

## 4 · Impact

### 4.1 Blocks completion of ECR-D-005 disposition A

Disposition A comprised four actions. Two are complete, two are held by this ECR:

| # | Action | Status |
|---|---|---|
| 1 | Record human approval bound to content hash | ✅ `approvals/APR-001` |
| 2 | Update the `FROZEN.md` per-artifact entry | ✅ 16 of 16 now verify |
| 3 | Recompute the aggregate | ⛔ **held — no defined method** |
| 4 | Update `STATE.frozen_set_hash` | ⛔ **held — derived from (3)** |

Producing a value for (3) would require selecting a construction, which is resolving an ambiguity by assumption. LAW-12 forbids it, and any value so produced would be indistinguishable from the unreproducible one it replaced.

### 4.2 A BLOCKING schema field currently has no authoritative value

`sch-state` declares `frozen_set_hash` required at severity BLOCKING. The field is populated, but its value is superseded and its construction unknown. It is retained verbatim rather than altered, so no information is lost.

### 4.3 Not a stop condition for Stage 2

Compiler Stage 2 consumes `manifest.templates`, `manifest.agents` and `manifest.runtime_sequence`. Its integrity dependency was on the **per-artifact** digest of `framework.manifest.json`, which now verifies. The aggregate is a property of the registry, not an input to Stage 2. **Stage 2 is released from the ECR-D-005 stop** and does not wait on this ECR.

## 5 · Requested action

Ruling by `chief-systems-engineer` (A4). Candidate resolutions, for A4 to accept, amend or replace:

| # | Resolution | Note |
|---|---|---|
| **A** | **Declare the construction explicitly in `FROZEN.md`** and recompute from it. Suggested, matching the existing per-artifact rule: SHA-256 over the concatenation of `<path> <digest>\n` lines, sorted by path, UTF-8/LF. | Recommended. Makes the value reproducible by any third party and self-documenting at the point of use |
| B | Adopt whatever construction Compiler Stage 6 uses for `MANIFEST.lock`, for consistency across both registries | Requires Stage 6, which is blocked by CMP-BLOCK-004. Defers resolution indefinitely |
| C | Remove the aggregate and rely solely on per-artifact digests | Requires an A4 amendment to `sch-state`, which declares the field BLOCKING |

Whichever is chosen, **bind a standing verification check** so the registry is machine-verified against the working tree. No such check exists: the natural home is a new check under Compiler Stage 5, or an extension of `V-06`. This is the same gap that allowed ECR-D-005 to persist across three releases, and it is recorded as an open item in its own right.

## 6 · Disposition

> ### A — DECLARE THE CONSTRUCTION EXPLICITLY. **CLOSED.**

| | |
|---|---|
| Disposition | **A**, as recommended in §5. The construction is declared normatively in `framework.manifest.json` → `metadata.reproducible.digest_constructions.frozen_set_aggregate`, designated **DC-2** |
| Ruled by | `chief-systems-engineer` · `S-2026-08-08-02` |
| Raised by | `role-unrecorded` · `S-2026-08-08-01` |
| Instrument | [`AIEF-AMD-008`](../../../framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md) §AMD-16 |
| Approval artifact | [`approvals/APR-002`](../approvals/APR-002_Amend_Framework_Manifest_AMD-008.md) — the manifest is frozen; LAW-01 requires both an approved ECR and a recorded human approval |
| Date | 2026-08-08 |

### Acceptance condition 3 — ruled by an agent that did not raise it

`AIEF-AMD-008` §AMD-20 rules that **agent identity for LAW-02, LAW-04 and LAW-05 independence is the pair (role, session)**, on the ground that `tpl-verification-report` §5 already requires *Context* as part of an independence declaration and states that *"independence is a property of the context, not of intent."*

`S-2026-08-08-02` is a cold context with no inherited state from `S-2026-08-08-01`. **Ruled-by ≠ raised-by.** The condition is met.

**Residual, recorded rather than glossed:** where the same role both raises and rules, independence is weaker than a cross-role disposition. Here the raising role is not even recoverable, so the comparison cannot be made. The mitigating control is an independent cold-context `qa-engineer` audit of this ruling — **OI-V-03**, open.

### DC-2, as ruled

SHA-256 over the concatenation of one record per registered artifact, each record `<path>` `<SP>` `<digest>` `<LF>`, sorted ascending by the UTF-8 octet sequence of `<path>`; UTF-8; no header, trailer or BOM; the aggregate excluded from its own preimage; output 64 lowercase hex, **never truncated**. Empty registry: SHA-256 of the empty string. Full normative text, with a published worked example, in AMD-008 §AMD-16.

**The superseded value is not recovered.** §3.1 established it is not reproducible; DC-2 is defined going forward and makes no attempt at recovery. The old value is marked superseded in `FROZEN.md` and retained for audit only.

### §4.1 execution table, now complete

| # | Action | Status |
|---|---|---|
| 1 | Record human approval bound to content hash | ✅ `approvals/APR-001` |
| 2 | Update the `FROZEN.md` per-artifact entry | ✅ 24 of 24 now verify |
| 3 | Recompute the aggregate | ✅ **`080771b0e26e365decebaa4118a27b4a46c73b7beeb3fb599009ce4ef6b6367a`** — DC-2 over the 24-member registry |
| 4 | Update `STATE.frozen_set_hash` | ✅ same value, **full 64 characters** |
| 5 | Bind a standing verification check | ◑ **V-24 declared** by AMD-008 §AMD-19 as a Stage 5 requirement; **not implemented**. Stage 5 is not executed. Remains **OI-V-02** |

Action 5 is the one condition of §5 that is discharged in declaration but not in effect. It is recorded honestly rather than marked complete.

### Effect on held work

**Released.** Recomputation of the freeze-set aggregate and `STATE.frozen_set_hash` proceeded under this disposition. ECR-D-005 residual is discharged.

---

## Authority chain

| | |
|---|---|
| LAW-02 | Ambiguity is raised as ECR-Q; only the chief-systems-engineer rules on ECR-Q; no ECR is closed by the agent that raised it |
| LAW-12 | Assumption is never a resolution method; producing Open Questions and stopping is a compliant deliverable |
| LAW-01 / LAW-10 | Freeze registry content and human approval — the manifest change carries `APR-002` |
| `core/PRECEDENCE.md` rank 1 | Live human-owner instruction authorising the amendment |
| `core/PRECEDENCE.md` rank 7 | AI inference overrides nothing; raising an ECR is its only path |
| ECR-D-005 | The disposition during whose execution this ambiguity surfaced |
| AIEF-AMD-008 §AMD-16, §AMD-20 | The ruling, and the identity definition under which it is admissible |
