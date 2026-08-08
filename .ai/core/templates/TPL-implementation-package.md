# TPL - Implementation Package

> **Generated artifact.** Emitted by aief-compile Stage 2 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `tpl-implementation-package` |
| Layer / partition | L2 / core |
| Tier | T3 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |
| Producer | discipline engineer |
| Consumers | `chief-systems-engineer`, `qa-engineer` |
| Filed at | `project/` |
| Authority | `LAW-06` Traceability · workflow `WF-04` |

---

The bridge from a **frozen specification** to executable engineering work. It adds no engineering content of its own: it restates frozen requirements in implementable form and shows, line by line, where each one came from.

## Required sections

All eight are mandatory. An omitted section fails the contract.

### 1 · Executive summary

What is being implemented, against which frozen baseline, and the current disposition in one paragraph. State the component identifier and specification revision.

### 2 · Traceability matrix

Every feature to be implemented, against the frozen source that authorises it.

| Feature | Requirement | Frozen source | Verification |
|---|---|---|---|
| … | … | `spec/…` § … | … |

**A row without a frozen source is a defect, not an omission.** Raise ECR-D.

### 3 · Parameters

The parameter set the implementation is driven by, with the authority for each value. Parameters are declared once and referenced thereafter; a value restated inline is a divergence risk.

| Parameter | Value | Unit | Source |
|---|---|---|---|

### 4 · Feature strategy

How each feature will be realised, and why that approach. Records the reasoning that would otherwise be lost between sessions.

### 5 · Implementation sequence

Ordered steps with their dependencies. A step that cannot proceed carries an explicit **HOLD** and names the blocking item.

### 6 · Verification checklist

Per feature, the check that will demonstrate conformance and who performs it. Under `LAW-05` the performer may not be the producer.

### 7 · Open questions

Every unresolved finding, classified per `LAW-12`:

| Class | Meaning | Effect |
|---|---|---|
| Clarification | Logged; work proceeds | none |
| Ambiguity | Raises **ECR-Q** | that item holds |
| Defect | Raises **ECR-D** | affected work **stops** |

**Required whenever any finding is open.** Stating open questions and stopping is a compliant deliverable, not a failure.

### 8 · Release gate

The disposition. Binary, per `LAW-03`.

| | |
|---|---|
| Disposition | **PASS** or **FAIL** |
| Evaluated by | role, identity |
| Date | |
| Blocking items | listed, or explicitly none |

## Acceptance conditions

| # | Condition | Test |
|---|---|---|
| 1 | Every feature traces to a frozen source | No row in §2 has an empty source |
| 2 | Open questions section present when any finding is open | §7 exists and is non-empty whenever any ECR is open against the package |
| 3 | Release gate states a binary disposition | §8 reads exactly PASS or FAIL |

*Substantially complete* is not a disposition (`LAW-03`).

## Forbidden

| | |
|---|---|
| Changing a frozen dimension, tolerance or interface | Raise ECR-D |
| Inventing a value the specification does not state | Raise ECR-D |
| Resolving a specification ambiguity by assumption | Raise ECR-Q - `LAW-12` |
| Proceeding past a defect | The affected work stops - `LAW-02` |
