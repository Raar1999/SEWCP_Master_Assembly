# Open Items

> **Instance artifact.** Emitted by aief-compile Stage 3 from `framework.manifest.json` and live repository state.
> Partition `project` — never touched by framework upgrade. Owner `project-manager`. Mutability mutable.

---

Read at boot step B7. Every blocker in `STATE.md` resolves here. **This register is authoritative;** `STATE.md` is a derived cache and `ENGINEERING.md` is an index.

## Blocking

| ID | Item | Blocks | Authority |
|---|---|---|---|
| ECR-D-001 | Alignment pin interface: two mutually exclusive geometries | CAD modelling of SEWCP-200 | Design Authority |
| ECR-D-002 | Channel cross-section does not close: 8+8+6=22 against 20.000 | CAD modelling of SEWCP-200 | Design Authority |
| ECR-D-003 | Coolant stub interface undimensioned | CAD modelling of SEWCP-200 | Design Authority |
| ECR-D-004 | Choke counterbore undimensioned; M5x30 exceeds 29.5 mm stack | CAD modelling of SEWCP-200 | Design Authority |
| CMP-BLOCK-004 | aief-compile not implemented as deterministic software | Compiler Stage 6, V-10 | Software |
| CMP-BLOCK-005 | Tokenizer, multi-platform, concurrency infrastructure absent | V-09, V-12, V-15, V-18 | Software |
| C-4 | LICENSE is an unresolved placeholder | Public or external release | Repository owner |

## Open, not blocking

| ID | Item | Authority |
|---|---|---|
| OI-V-02 | No **standing** check binds `FROZEN.md` to the working tree. `V-24` is now **declared** by AIEF-AMD-008 §AMD-19 but **not implemented** — Stage 5 has not run. The registry is still verified only by hand. This is the root cause of ECR-D-005 and of FIND-4 | qa-engineer + A4 |
| OI-V-03 | **Everything session `S-2026-08-08-02` produced is unverified.** AIEF-AMD-008, the manifest amendment, APR-002, APR-003, the recomputed aggregate, the eight registry additions, the `BINDING.md` repair, the ECR dispositions and the VER-001 filing all post-date the VER-001 audit and are outside its scope. LAW-05 bars self-verification. Needs an independent cold-context audit | qa-engineer |
| OI-R-01 | **No `v0.2.0` tag exists**, though `a403059` is "Release 0.2". Tags jump `v0.1.0` → `v0.3.0` and `releases/TAGS.md` does not mention it. Not a LAW-07 breach — LAW-07 governs tag form, not coverage. **No tag is to be created retroactively and no history rewritten** without a human ruling; the gap is recorded so it is not mistaken for a lost release. FIND-8 | repository-engineer |
| OI-C-01 | `SCH-ledger-entry.schema.json` declares `additionalProperties: true`. DC-3 (AMD-17) covers only the seven declared fields, so any additional field an entry carries is **not protected by the chain**. Tightening to `false` removes the exposure and is a Stage 1 re-emission | chief-systems-engineer |
| OI-C-02 | `adapters/ADP-ci.md` is **stale**: it states *"All 22 checks are BLOCKING"* and lists phase ranges `V-01 .. V-10` / `V-18 .. V-21` that omit `V-23`, `V-24`, `V-25`. Requires a Stage 4 re-emission. The `adapters` partition is human-only write access and was deliberately not hand-edited | repository-engineer |
| OI-C-05 | **`referenced_by` completeness is undeclared.** MI-3 tests resolution, not completeness (AIEF-AMD-009 §AMD-24): `BOOT.md` is cited by `adp-claude-code`, `adp-chatgpt`, `adp-generic-llm`, `readme` and `core/CONTEXT_TIERS.md`, yet `boot.referenced_by` is empty and nothing makes that a defect. The three adapters' `depends_on: ["adapters-index", "boot"]` edges may themselves be citations miscoded as build order — the FIND-1 class, forward-directed and therefore V-23-invisible. Observed while ruling AMD-24; outside its directed scope; recorded so it is not lost | A4 ruling, later session |
| OI-C-04 | Nine `implementation/**/README.md` files carry a UTF-8 **byte-order mark**. They lie outside `.ai/` and are not registered, so `V-25` as scoped does not reach them, and they were **not** repaired — `implementation/` is PR-controlled. Found while validating V-25; recorded so the observation is not lost | documentation-engineer |
| OI-P-01 | **Session-record gaps.** `project/sessions/` is empty: session `S-2026-08-08-01` filed no session summary, so its role assignments are unrecoverable and its ECRs carry `role-unrecorded`. That session performed no LAW-09 close and its work is permanently unlogged — a close cannot be performed retroactively by a later session. The VER-001 audit declared no session identifier and is unnumbered. No `.session.lock` exists (DEV-02) | project-manager |
| OI-V-04 | **VER-002 residual: FIND-Q2-1 only.** `AIEF-FRZ-001` Part 4 Stage 1 still carries the superseded barrier wording with no in-document errata pointer (A4, next amendment). FIND-Q2-2 and FIND-Q2-3 are **dispositioned** by the human-owner's commit-granularity ruling of `S-2026-08-08-03`, executed by `repository-engineer`: commits `d07e931` (AMD-008 state) and `655aa75` (AMD-009 state) make every approval subject recoverable as a git object — `636cf22b…` at `d07e931`, `9611d547…` and `86c8be7f…` at `655aa75` — and place all three sessions' registered work in git history. Report at [`verification/VER-002`](verification/VER-002_Independent_Verification_AIEF-AMD-009.md); filed verbatim by the audited party, VER-001 precedent | A4 |
| OI-P-02 | `ROSTER.md` marks `qa-engineer`, `project-manager` and `chief-systems-engineer` **UNASSIGNED**, and states *"A role marked UNASSIGNED cannot be dispatched."* Three such roles have been dispatched. The dispatches are authorised at `core/PRECEDENCE.md` rank 1 by live human instruction, which outranks the roster — but the roster record is stale and reviewer-independence cannot be checked against identities that are not recorded. Assignment is a project-manager action and was **not** self-assigned | project-manager |

## Closed

| ID | Item | Closed by | Resolution |
|---|---|---|---|
| ECR-Q-003 | Stage 1's barrier *"No later stage may emit into core"* contradicted by the declared outputs of Stages 2, 5 and 6; held one question Compiler Stage 5 had to answer before emitting | Disposition **A**, ruled by `chief-systems-engineer` · `S-2026-08-08-03` — a cold session that did not raise it (AMD-20 identity rule); instrument [`AIEF-AMD-009`](../../framework/AIEF-AMD-009_Stage_1_Barrier_and_MI-3_Namespace.md) §AMD-23; approval [`approvals/APR-004`](approvals/APR-004_Amend_Framework_Manifest_AMD-009.md) | The barrier protects the **Stage 1 output set**, not the `core/` prefix. Later stages emit only into their own declared subtrees; evaluable as pairwise disjointness of `generation_order[].outputs`, now bound into `V-01`. Stage 2's completion is conforming; `AIEF-FRZ-001` Part 4 Stage 1 barrier row superseded in reading, bytes unchanged. **Stage 5 may lawfully emit `core/validation/**`** |
| OI-C-03 | `boot.referenced_by` carried `framework` and `sch-state.referenced_by` carried `V-06`; neither a `files[]` id — strict MI-3 reading failed V-01, halting any Stage 1 re-emission. FIND-9 | Ruled by `chief-systems-engineer` · `S-2026-08-08-03`; instrument `AIEF-AMD-009` §AMD-24; approval `approvals/APR-004` | **Strict reading governs:** MI-3 targets range over `files[]` ids only. Both dangling tokens removed — `framework` unrecoverable and not guessed; the `V-06`→`sch-state` relation preserved in `validation[V-06]` and MI-7. Manifest now **passes MI-3 strictly** over all 106 entries. Residual observation recorded as OI-C-05 |
| ECR-Q-001 | Freeze-set aggregate construction undefined; the recorded value not reproducible by any of thirteen tested constructions | Disposition **A — declare the construction explicitly**, ruled by `chief-systems-engineer` · `S-2026-08-08-02`; instrument [`AIEF-AMD-008`](../../framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md) §AMD-16; approval [`approvals/APR-002`](approvals/APR-002_Amend_Framework_Manifest_AMD-008.md) | **DC-2** declared normatively in the manifest. Aggregate recomputed over the 24-member registry: `080771b0…f6b6367a`, full 64 characters in both `FROZEN.md` and `STATE.md`. The superseded value is **not recovered** and is marked so. Residual: **V-24 declared, not implemented** — OI-V-02 |
| ECR-Q-002 | Ledger `entry_hash` construction undefined; held the LAW-09 close and the irreversible `genesis → active` transition | Disposition **A — declare the construction explicitly**, ruled by `chief-systems-engineer` · `S-2026-08-08-02`; instrument `AIEF-AMD-008` §AMD-17; approval `approvals/APR-002` | **DC-3** declared: seven covered fields, canonical line-oriented preimage, `entry_hash` self-excluded, `prev_hash` feeds the successor digest, genesis `null`, two published worked examples. YAML rejected as the serialisation. **No ledger entry was written**; `HEAD` remains at `genesis` |
| OI-V-01 | Independent QA verification of **ECR-D-005 + Compiler Stage 2** outstanding | Verification report filed at [`verification/VER-001`](verification/VER-001_Independent_Verification_ECR-D-005_and_Stage_2.md) by `chief-systems-engineer` · `S-2026-08-08-02` | Cold-context `qa-engineer` audit: **10 criteria, 10 PASS, 0 fail**. Body filed verbatim; the qa-engineer neither filed nor attested to the filing. Nine findings raised; dispositions at [`reviews/DR-001`](reviews/DR-001_QA-001_Finding_Dispositions.md). Scope reconciled to the wider of the two previously recorded (FIND-6). **Does not extend to `S-2026-08-08-02`** — see OI-V-03 |
| ECR-D-005 | Freeze registry did not verify: `framework.manifest.json` diverged from its registered hash across releases 0.4, 0.6 and commit `6ce3508` | Disposition **A — re-register**, human-owner; approval [`approvals/APR-001`](approvals/APR-001_Reregister_Framework_Manifest.md) | Registered digest updated; **all four execution actions now complete** — the aggregate and `STATE.frozen_set_hash` were released by ECR-Q-001's disposition. Action 5, the standing check, remains OI-V-02. Divergence was fully attributable to approved amendments AMD-004/006/007 |
| OI-F-01 | `session_timeout` had no declared value | AIEF-AMD-003 §AMD-09 | 14400 s (4 h), project-overridable |
| OI-F-02 | Ledger genesis semantics unspecified | AIEF-AMD-003 §AMD-10 | `HEAD.state ∈ {genesis, active}`. At genesis B4 check 1 is vacuous; checks 2 and 3 are operative |
| CMP-BLOCK-014 | Build-order cycle `LAW-11 ↔ agent-contract` | AIEF-AMD-002 §AMD-06 | `depends_on` corrected; citation preserved as bidirectional `references` edges |

## Recorded risk, not blocking

| ID | Item |
|---|---|
| CDR-C3 | Independent cold-context ratification of the AIEF CDR not performed. Recorded at AIEF-FRZ-001 section 6.2. Four consecutive artifacts carry this exposure. |
| SOD-1 | **Separation of duties.** `core/agents/INDEX.md` states `chief-systems-engineer` *"may not implement what it approved."* Session `S-2026-08-08-02` both ruled and applied, at the direction of the human owner (`core/PRECEDENCE.md` rank 1, recorded in APR-002 and APR-003). Session `S-2026-08-08-03` repeated the departure in identical form for AIEF-AMD-009 (recorded in APR-004 and APR-005 and at `AIEF-AMD-009` § *Separation of Duties*); its mitigating control **was executed**: independent cold-context QA audit filed at [`verification/VER-002`](verification/VER-002_Independent_Verification_AIEF-AMD-009.md) — 9 criteria, 9 PASS, verdict VERIFIED WITH FINDINGS. The departures are authorised, not erased. Mitigating control for `-02` is OI-V-03, still open. |

## Deviations recorded

| ID | Deviation |
|---|---|
| DEV-01 | ~~Compiler Stage 3 executed before Stage 2 at explicit direction.~~ **CLOSED** 2026-08-08 — Stage 2 emitted `core/templates/TPL-current-state.md`; `state.depends_on → tpl-current-state` is satisfied. |
| DEV-02 | `project/.session.lock` template not emitted. Not declared in `framework.manifest.json`. Runtime artifact created by boot step B4a; format specified in AIEF-FRZ-001 section 1.3. Emitting it requires an A4 manifest amendment. **Consequence observed:** boot step B4a has not executed in any session to date — see OI-P-01. |
