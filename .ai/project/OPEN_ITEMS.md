# Open Items

> **Instance artifact.** Emitted by aief-compile Stage 3 from `framework.manifest.json` and live repository state.
> Partition `project` — never touched by framework upgrade. Owner `project-manager`. Mutability mutable.

---

Read at boot step B7. Every blocker in `STATE.md` resolves here.

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

## Closed

| ID | Item | Closed by | Resolution |
|---|---|---|---|
| OI-F-01 | `session_timeout` had no declared value | AIEF-AMD-003 §AMD-09 | 14400 s (4 h), project-overridable. Errs long because lock-theft from a live session is silent corruption, whereas a blocked tree is recoverable |
| OI-F-02 | Ledger genesis semantics unspecified | AIEF-AMD-003 §AMD-10 | `HEAD.state ∈ {genesis, active}`. At genesis B4 check 1 is vacuous; checks 2 and 3 are operative. First session close transitions to active |
| CMP-BLOCK-014 | Build-order cycle `LAW-11 ↔ agent-contract` | AIEF-AMD-002 §AMD-06 | `depends_on` corrected; citation preserved as bidirectional `references` edges |

## Recorded risk, not blocking

| ID | Item |
|---|---|
| CDR-C3 | Independent cold-context ratification of the AIEF CDR not performed. Recorded at AIEF-FRZ-001 section 6.2. Four consecutive artifacts carry this exposure. |

## Deviations recorded

| ID | Deviation |
|---|---|
| DEV-01 | Compiler Stage 3 executed before Stage 2 at explicit direction. `state.depends_on` includes `tpl-current-state` (Stage 2), unsatisfied at emission. Content dependency satisfied directly from `manifest.templates`. Stage 2 must run before release. |
| DEV-02 | `project/.session.lock` template not emitted. Not declared in `framework.manifest.json`. Runtime artifact created by boot step B4a; format specified in AIEF-FRZ-001 section 1.3. Emitting it requires an A4 manifest amendment. |
