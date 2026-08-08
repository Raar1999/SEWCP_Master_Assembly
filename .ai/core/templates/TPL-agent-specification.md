# TPL - Agent Specification

> **Generated artifact.** Emitted by aief-compile Stage 2 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `tpl-agent-specification` |
| Layer / partition | L2 / core |
| Tier | T3 |
| Owner | `chief-systems-engineer` |
| Mutability | immutable |
| Producer | `chief-systems-engineer` |
| Consumers | framework |
| Filed at | `core/agents/` |
| Schema | `core/schemas/SCH-agent.schema.json` - severity BLOCKING |
| Authority | `LAW-11` Agent Conduct |

---

A role contract. An agent **declares its role, stays inside its contract and escalates rather than assumes**. What an agent may not do is as much a part of its identity as what it may.

## Required sections

### 1 · Responsibilities

What the role is accountable for. Each responsibility is a standing obligation, not a task.

### 2 · Inputs

What the role consumes: artifacts, laws, templates and state. An input the role may not read is not listed.

### 3 · Outputs

What the role produces, by artifact class. Each output resolves to a template contract or a declared artifact type.

### 4 · Allowed actions

The operations the role may perform. Anything not derivable from this section requires escalation. Where an action touches a protected partition or a frozen artifact, state the precondition.

### 5 · Forbidden actions

**At least one forbidden action is mandatory.** A role with nothing forbidden has no contract, and an agent that cannot say what it must refuse cannot be trusted with what it may do.

State the prohibition, not the rationale - rationale belongs to the law it enforces.

### 6 · Escalation rules

| Condition | Escalate to |
|---|---|

Every forbidden action that an agent may plausibly be asked to perform has a corresponding escalation path. Escalation is the sanctioned alternative to assumption (`LAW-12`).

### 7 · Authority level

| Level | Meaning |
|---|---|
| **A1** | Produces artifacts within an assigned task |
| **A2** | Verifies and may reject others' artifacts |
| **A3** | Plans, gates and allocates; cannot verify own plan |
| **A4** | Rules on ECRs and approves designs; cannot implement |
| **H** | Human owner; sole authority for freeze, thaw and architecture change |

Exactly one level. Declared, never inferred.

### 8 · Capability tags

Machine-readable capability identifiers used for dispatch. Lower case, hyphenated.

### Separation of duties

Where the role carries a duty conflict, state it explicitly - for example *may not verify an artifact it produced*, or *may not make engineering decisions*. Duty conflicts are checked at dispatch.

## Acceptance conditions

| # | Condition | Test |
|---|---|---|
| 1 | At least one forbidden action | §5 is non-empty |
| 2 | Authority level declared | §7 states exactly one of A1, A2, A3, A4, H |
| 3 | Conforms to `SCH-agent` | All required fields present: `id`, `name`, `authority`, `capability_tags`, `responsibilities`, `inputs`, `outputs`, `allowed`, `forbidden`, `escalation` |

## Forbidden

| | |
|---|---|
| A role specification with no forbidden actions | Condition 1 |
| Inferring an authority level from capabilities | Condition 2 - it is declared |
| Granting a role the ability to verify its own output | `LAW-05` |
| Adding a universal role | The universal registry is **frozen at five roles** for MAJOR version 1; profile roles are namespaced |
