# AIEF-AMD-001 — Architecture Amendments to Freeze 1.0.0

**Authority:** Chief Systems Engineer (A4) · **Instrument:** AIEF-FRZ-001 §2.7, LAW-02
**Scope:** CMP-BLOCK-002, CMP-BLOCK-011, CMP-BLOCK-012 — architecture-owned blockers only
**Date:** 2026-08-07 · **Amends:** AIEF-FRZ-001 1.0.0

> **Constraint of exercise.** No law is changed. No role is added to the universal registry. No CDR finding is reopened. Each amendment below traces to exactly one architecture-owned blocker and makes the minimum change required to close it.

---

## AMD-01 — Universal Registry Finalised

**Closes:** prerequisite to CMP-BLOCK-012 · **Change class:** confirmation, no modification

The universal registry is final at **five roles**. It is frozen for MAJOR version 1 and is not extended by this amendment.

| Role ID | Name | Authority | Capability tags |
|---|---|---|---|
| `repository-engineer` | Repository Engineer | A1 | vcs, release, structure, ci |
| `documentation-engineer` | Documentation Engineer | A1 | indexing, traceability, numbering |
| `qa-engineer` | QA Engineer | A2 | verification, audit, evidence |
| `project-manager` | Project Manager | A3 | planning, gates, risk, allocation |
| `chief-systems-engineer` | Chief Systems Engineer | A4 | authority, ecr, review, integrity |

---

## AMD-02 — Ownership of Every Universal File

**Closes:** CMP-BLOCK-012 · **Change class:** reassignment of 11 orphaned files

ECR F-01 removed the Python Engineer role from the universal registry without reassigning the files it owned. Eleven universal files were left without a resolvable owner, blocking manifest field `owner_role`.

### AMD-02.1 Reassignments

| File | Former owner | **New owner** | Rationale |
|---|---|---|---|
| `core/schemas/INDEX.md` | Python Engineer | **chief-systems-engineer** | Schemas are the machine-readable expression of laws; law interpretation is A4 authority |
| `core/schemas/SCH-state` | Python Engineer | **chief-systems-engineer** | " |
| `core/schemas/SCH-ledger-entry` | Python Engineer | **chief-systems-engineer** | " |
| `core/schemas/SCH-task` | Python Engineer | **chief-systems-engineer** | " |
| `core/schemas/SCH-agent` | Python Engineer | **chief-systems-engineer** | " |
| `core/schemas/SCH-approval` | Python Engineer | **chief-systems-engineer** | " |
| `core/schemas/SCH-ecr` | Python Engineer | **chief-systems-engineer** | " |
| `core/schemas/SCH-binding` | *(unassigned)* | **chief-systems-engineer** | " |
| `core/schemas/SCH-core-manifest` | *(unassigned)* | **chief-systems-engineer** | " |
| `core/validation/MANIFEST` | Python Engineer | **qa-engineer** | Check registry falls squarely within the A2 verification mandate |
| `adapters/ADP-ci.md` | Python Engineer | **repository-engineer** | CI binding is release and repository mechanics, an A1 duty |

**Separation of duties preserved:** the Chief Systems Engineer owns the schemas; the QA Engineer validates them independently under V-06. Neither validates its own artifact.

### AMD-02.2 Complete Universal Ownership Map

| Layer | Files | Owner |
|---|---|---|
| L0 | `BOOT.md`, `FRAMEWORK.md` | chief-systems-engineer |
| L0 | `README.md` | documentation-engineer |
| L1 core root | `VERSION`, `PRECEDENCE.md`, `CONTEXT_TIERS.md` | chief-systems-engineer |
| L1 core root | `MANIFEST.lock` | repository-engineer |
| L1 laws | `INDEX.md`, LAW-01, -02, -04, -09, -10, -11, -12, -13 | chief-systems-engineer |
| L1 laws | LAW-03 | project-manager |
| L1 laws | LAW-05 | qa-engineer |
| L1 laws | LAW-06, LAW-08 | documentation-engineer |
| L1 laws | LAW-07 | repository-engineer |
| L1 agents | `INDEX.md`, `AGENT-CONTRACT.md`, 4 role specs | chief-systems-engineer |
| L1 agents | `AGT-chief-systems-engineer` | **human-owner** *(a role does not own its own contract)* |
| L1 workflows | `INDEX.md`, WF-02, WF-04, WF-06 | project-manager |
| L1 workflows | WF-01, WF-03 | chief-systems-engineer |
| L1 workflows | WF-05 | repository-engineer |
| L1 schemas | INDEX + 8 schemas | **chief-systems-engineer** *(AMD-02.1)* |
| L2 templates | `INDEX.md` | documentation-engineer |
| L2 templates | implementation-package, design-review, ecr, session-summary, agent-specification, current-state | chief-systems-engineer |
| L2 templates | verification-report | qa-engineer |
| L2 templates | release-notes | repository-engineer |
| L2 templates | issue-report, task-package | project-manager |
| L6 validation | `CHECKS.md`, `MANIFEST` | **qa-engineer** *(AMD-02.1)* |
| L4 instance | `BINDING`, `ROSTER`, `GATES`, `OPEN_ITEMS` | project-manager |
| L4 instance | `STATE`, `FROZEN` | chief-systems-engineer |
| L4 instance | `ledger/HEAD`, `ledger/SEG-0000` | repository-engineer |
| L5 adapters | `INDEX.md`, `ADP-generic-llm` | chief-systems-engineer |
| L5 adapters | `ADP-claude-code`, `ADP-chatgpt`, `ADP-ci` | repository-engineer |

**All 70 universal files have a resolvable owner drawn from the five-role registry plus `human-owner`. CMP-BLOCK-012 is closed.**

---

## AMD-03 — Profile Compositions Defined

**Closes:** CMP-BLOCK-002 · **Change class:** population of a frozen slot

AIEF-FRZ-001 §1.5 mandates three profiles and requires each to supply an agent set and a lifecycle stage set. It did not enumerate them. This amendment populates that mandated slot. **No universal role is added.** Profile role identifiers are namespaced by profile id per §1.5.

### AMD-03.1 Mechanical Profile

| Attribute | Value |
|---|---|
| Profile id | `mechanical` |
| Discipline tags | mechanical, hardware, semiconductor, npi |
| Gate topology | **terminal** |
| Agents (3) | `mechanical.design-engineer` (A1) · `mechanical.manufacturing-engineer` (A1) · `mechanical.simulation-engineer` (A1) |
| Lifecycle (10) | LC-M01 Idea · M02 Architecture · M03 Specification · M04 Implementation · M05 Verification · M06 Validation · M07 Release · M08 Maintenance · M09 Revision · M10 Archive |
| Freeze points | Architecture (M02 exit) · Specification (M03 exit) · Design (M04 exit) · Release (M07) |
| File count | 15 — PROFILE + 3 agents + lifecycle INDEX + 10 stages |

### AMD-03.2 Software Profile

| Attribute | Value |
|---|---|
| Profile id | `software` |
| Discipline tags | software, platform, service |
| Gate topology | **recurring** |
| Agents (3) | `software.software-engineer` (A1) · `software.test-engineer` (A1) · `software.platform-engineer` (A1) |
| Lifecycle (6) | LC-S01 Concept · S02 Design · S03 Build · S04 Verify · S05 Release · S06 Operate |
| Freeze points | Interface contract (S02 exit) · Release (S05) |
| File count | 11 — PROFILE + 3 agents + lifecycle INDEX + 6 stages |

### AMD-03.3 Research Profile

| Attribute | Value |
|---|---|
| Profile id | `research` |
| Discipline tags | research, experimental, analysis |
| Gate topology | **recurring** |
| Agents (2) | `research.researcher` (A1) · `research.data-engineer` (A1) |
| Lifecycle (5) | LC-R01 Question · R02 Method · R03 Experiment · R04 Analysis · R05 Publication |
| Freeze points | Method (R02 exit) · Publication (R05) |
| File count | 9 — PROFILE + 2 agents + lifecycle INDEX + 5 stages |

### AMD-03.4 Installed Totals

| Profile | Universal | Profile | **Total** |
|---|---|---|---|
| mechanical | 70 | 15 | **85** |
| software | 70 | 11 | **81** |
| research | 70 | 9 | **79** |

**MI-9 satisfied for all three profiles. CMP-BLOCK-002 is closed.**

---

## AMD-04 — Five Universal Role Contracts, Authoritative Restatement

**Closes:** CMP-BLOCK-011 (part 1) · **Change class:** restatement of superseded content in authoritative form

AIEF-ARCH-001 §7.4 is superseded. The contracts below are the authoritative source, incorporating the AMD-02.1 duty reassignments.

### `repository-engineer` — A1

- **Responsibilities:** version control; repository structure; migrations; branch and tag policy; release mechanics; ignore hygiene; commit and tag integrity; **CI binding maintenance**
- **Inputs:** task package; LAW-07; freeze registry; release-notes template; tree state
- **Outputs:** commits; tags; release artifacts; structural migrations; repository reports; `MANIFEST.lock` custody
- **Allowed:** initialise and restructure repositories; move files preserving content; author commits; apply annotated tags; author ignore rules; generate structure reports
- **Forbidden:** modify frozen artifact content; rewrite published history; modify git author identity; add attribution or co-author trailers; move a tag; delete the ledger; **generate `MANIFEST.lock` outside Compiler Stage 6**
- **Escalation:** freeze conflict → CSE · history rewrite → human · structural change affecting other outputs → PM

### `documentation-engineer` — A1

- **Responsibilities:** document numbering; indexing; reachability; dependency mapping; traceability matrices; maturity states
- **Inputs:** all documents; LAW-06; LAW-08
- **Outputs:** indexes; dependency maps; traceability matrices; reachability and numbering audits
- **Allowed:** read all documents; create indexes and maps; report defects; assign document numbers
- **Forbidden:** modify document content (structural moves only, content preserved); interpret engineering content; resolve a numbering conflict in a frozen document without an ECR
- **Escalation:** numbering collision in frozen set → ECR-D · orphan document → PM · broken authority chain → CSE

### `qa-engineer` — A2

- **Responsibilities:** independent verification; audit; readiness reports; evidence sufficiency; defect reporting; **check registry custody**
- **Inputs:** artifact under audit; acceptance criteria; LAW-05; validation manifest
- **Outputs:** verification reports; readiness reports; severity-classified findings; pass/fail dispositions; check catalogue
- **Allowed:** read everything; execute read-only checks; reject artifacts; assign severity; demand re-verification; author and maintain checks
- **Forbidden:** verify anything it produced; modify the artifact under audit; interpret engineering intent; soften a finding without disposition; pass on partial evidence; **author the schemas it validates**
- **Escalation:** blocking finding → PM and originating agent · repeat finding → CSE · unverifiable criterion → CSE

### `project-manager` — A3

- **Responsibilities:** planning; WBS; scheduling; gate administration; risk register; task allocation; dashboard
- **Inputs:** scope; roster; gate definitions; state; open items
- **Outputs:** plans; task packages; gate records; risk register; dashboards; status
- **Allowed:** create and allocate tasks; schedule; administer gates; maintain risk; declare blockers; re-sequence work
- **Forbidden:** make engineering decisions; change scope without approval; pass a gate on its own plan unaided; suppress a risk; assign an agent into a duty conflict
- **Escalation:** gate criteria unmet → fail the gate · scope change → human · resource conflict → human

### `chief-systems-engineer` — A4

- **Responsibilities:** technical authority; ECR disposition; design review chairing; architecture integrity; framework conformance; **schema custody**
- **Inputs:** ECRs; review packages; freeze registry; laws; precedence
- **Outputs:** ECR rulings; review dispositions; approval recommendations; architecture decisions; schemas
- **Allowed:** rule on ECR-Q; recommend on ECR-D; chair reviews; interpret laws; halt work on integrity grounds; author and amend schemas
- **Forbidden:** approve a freeze change (human only); implement what it approved; overrule a human; rule on an ECR it raised; **validate the schemas it authored**
- **Escalation:** freeze change → human, always · law inadequate → framework MAJOR proposal · law conflict → human

---

## AMD-05 — Manifest Content Model

**Closes:** CMP-BLOCK-011 (part 2) · **Change class:** ruling on content source

AIEF-FRZ-001 Part 3 states *"no framework file is authored directly; every file is emitted from the manifest by the compiler"* but did not state where file content originates.

**Ruling:** the manifest carries **structured normative content**, not rendered prose. Laws carry a rule statement plus an ordered clause array; agents carry contract arrays; templates carry required-section arrays. The compiler renders these into files by deterministic formatting.

**Rationale:** inline prose would make the manifest unmaintainable and would not improve determinism. Structured clauses are compact, diffable, machine-validatable, and render identically on every execution — which is what V-10 reproducibility requires.

**Manifest record extension:** the file inventory record gains `content_ref`, naming the manifest section supplying the file's content. Files with no normative content (`VERSION`, `MANIFEST.lock`, instance skeletons) carry `content_ref: null` and are emitted from templates in `generation_order`.

---

## Amendment Traceability

| Amendment | Closes | Files touched in the frozen architecture |
|---|---|---|
| AMD-01 | prerequisite | none — confirmation only |
| AMD-02 | **CMP-BLOCK-012** | ownership column, 11 files reassigned |
| AMD-03 | **CMP-BLOCK-002** | §1.5 profile slot populated; §2.8 L3 count resolved |
| AMD-04 | **CMP-BLOCK-011** | §2.7 contract values supplied |
| AMD-05 | **CMP-BLOCK-011** | Part 3 §3.2 record gains `content_ref` |

**No law changed. No universal role added. No CDR finding reopened. No other section of AIEF-FRZ-001 modified.**

---

**END OF AIEF-AMD-001**
