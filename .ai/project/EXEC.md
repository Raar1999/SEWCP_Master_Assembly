# Execution Index

> **Instance artifact.** Partition `project` — never touched by framework upgrade.
> Owner `project-manager`. Mutability mutable. Tier **T2** — read on role assignment.

**Bounded index.** **Authority: [`tasks/`](tasks/)** — each task's full contract, read scope,
write scope, dependencies and checkpoint. Load the one record you are assigned; load no other.
Contract: [`EXECUTION_ARCHITECTURE.md`](EXECUTION_ARCHITECTURE.md).

**Mapping.** Each id below is the `task_id` of exactly one record under `tasks/`; each such
record's id appears exactly once here, under the heading naming its status.
**Grammar:** one id per line.

## Active

## Ready

T-002
T-004
T-005

## Blocked

T-003
T-006

## Awaiting decision

## Complete

T-001
T-007
T-008
