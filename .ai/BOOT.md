# AIEF BOOT

AIEF 1.0.0. **Single entry point. Read this first, every session.**

## Boot sequence

| Step | Action | Cost | On failure |
|---|---|---|---|
| B1 | Read BOOT.md | O(1) | Absent: framework not installed; halt |
| B2 | Read FRAMEWORK.md; compare version to BINDING pin | O(1) | Incompatible MAJOR: halt |
| B2a | Verify core aggregate digest against MANIFEST.lock; verify MANIFEST.lock against BINDING pin | O(n) | Mismatch: halt, blocking |
| B3 | Read project STATE | O(1) | Absent: uninitialised; enter lifecycle stage 1 |
| B4 | Read ledger HEAD; verify named entry exists and hashes; verify no HEAD.seq+1; compare STATE.last_ledger_seq to HEAD.seq | O(1) | Divergence: halt, human reconciliation |
| B4a | Acquire session lock; detect and record stale-lock reclamation | O(1) | Held and fresh: halt |
| B5 | Read BINDING: stage, gate, profile, authority | O(1) | None |
| B6 | Read laws INDEX and PRECEDENCE | O(1) | None |
| B7 | Read OPEN_ITEMS | O(1) | None |
| B8 | Declare orientation: version, stage, gate, profile, blockers, proposed next action | O(1) | None |
| B9 | Await role assignment. Do not act. | O(1) | None |

## Tier rule

T0 = this file. T1 = orientation, cap 6000 tok total with T0.
Load T2 on role assignment, T3 on task acceptance, T4 only on explicit request.

## Governing rule

**B9: declare orientation, then await role assignment. Do not act before a role is assigned.**

Conflict resolution: `core/PRECEDENCE.md`. Laws: `core/laws/INDEX.md`. Roles: `core/agents/INDEX.md`.
