# TPL - Verification Report

> **Generated artifact.** Emitted by aief-compile Stage 2 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `tpl-verification-report` |
| Layer / partition | L2 / core |
| Tier | T3 |
| Owner | `qa-engineer` |
| Mutability | immutable |
| Producer | `qa-engineer` |
| Consumers | `project-manager`, gate |
| Filed at | `project/verification/` |
| Authority | `LAW-05` Verification and Reproducibility · workflow `WF-04` |

---

**No agent may verify an artifact it produced.** Self-verification is invalid regardless of rigour, and no amount of care substitutes for independence.

## Required sections

### 1 · Criteria

Every criterion, each traceable to an authority - a requirement, a law, or a declared acceptance condition. Criteria are fixed **before** evidence is gathered; a criterion adjusted after seeing the result is not a criterion.

| # | Criterion | Authority |
|---|---|---|

### 2 · Method

How each criterion was tested. Sufficient for an independent party to repeat the verification and obtain the same result. State tools, versions, inputs and environment.

Where a criterion could not be tested, say so and mark it **NOT VERIFIED** - never infer a pass from absence of evidence.

### 3 · Evidence

Per criterion, the evidence obtained. Independent of the artifact under test and independent of this report's own assertions. Admissible: tool output, content hashes, measurements, quoted source with citation, reproducible commands.

### 4 · Per-criterion pass or fail

| # | Criterion | Result | Evidence |
|---|---|---|---|
| | | **PASS** / **FAIL** / **NOT VERIFIED** | |

Every criterion carries a binary result. **Partial**, *mostly* and *acceptable* are not results.

| Summary | |
|---|---|
| Criteria | n |
| Pass · Fail · Not verified | n · n · n |
| Overall | **PASS** only if every criterion passed |

### 5 · Independence declaration

| | |
|---|---|
| Verifier | role, identity |
| Producer of the artifact under test | role, identity |
| Independent | verifier ≠ producer - **confirmed** |
| Context | cold subagent · serial adoption |

Where the host declares `subagents: yes`, `qa-engineer` **shall** be dispatched as a subagent whenever it audits work produced in the current session. Independence is a property of the context, not of intent.

## Acceptance conditions

| # | Condition | Test |
|---|---|---|
| 1 | Independence declaration present | §5 exists and confirms verifier ≠ producer |
| 2 | Every criterion has a binary result | §4 has no empty or non-binary result cell |

## Forbidden

| | |
|---|---|
| Verifying an artifact one produced | `LAW-05` |
| Inferring a pass from absence of evidence | Mark NOT VERIFIED |
| Weakening a criterion so it passes | The criterion set is fixed before testing |
| Reporting an overall pass with any criterion failing | §4 |
