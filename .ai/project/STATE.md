# Current State

> **Instance artifact**, partition `project`, owner `chief-systems-engineer`, mutable, per `tpl-current-state`.
> **Authoritative resume point**, read at B3. [`OPEN_ITEMS.md`](OPEN_ITEMS.md) is the authoritative register; this file indexes it.

```yaml
lifecycle_stage:  LC-M04   # Implementation (mechanical profile)
active_gate:      LC-M04-EXIT   # terminal
compiler_stage:
  next:           6              # Generate Release - NOT authorized (OQ-14)
  complete:       [1, 2, 3, 4, 5]
  outstanding:    [6]
last_ledger_seq:  0
frozen_set_hash:  73911786c0795f20b5c5ea5b9ae4a9254d306abaccd9cc9ce54fc55a5d5bc3c2
active_tasks:     []
blockers:
  - ECR-D-006        # framework manifest drift. NOT under spec/**, not an LC-M04 criterion
  - CMP-BLOCK-004    # Stage 6 increment certified; full compiler absent
  - CMP-BLOCK-005    # Stage 6 slice delivered; campaign infrastructure absent
  - C-4              # LICENSE placeholder
open_non_blocking:
  - ECR-D-001..004, 007..012   # all dispositioned, approved, applied, registered
  - ECR-Q-009, ECR-Q-010
  - OQ-14                      # human-owner reservation: Stage 6 authorization
  - OI-V-02..10, OI-V-12       # OI-V-11 closed by VER-017
  - OI-C-01,02,04,05,07..11,13
  - OI-P-01..03, OI-R-01
next_action: |
  LC-M04-EXIT PASSED, C1-C7. Verify: PYTHONPATH=src python -m aief_gate

  SEWCP-200 model (REQ-001..005) and SEWCP-700 pin complete, verified
  from observed Fusion state; evidence cad/runs/, cad/DELIVERABLES.md.

  NEXT: SEWCP-300 heater plate, or the SEWCP-200 drawing stage.

  Open: ECR-Q-011 (rib 5.0 provisional), path 1.64 vs ~2.2 m, CP-02.
  NOT now: Stage 6 (OQ-14), ECR-D-006, ledger, tag, push before 2026-09-01.
```

## Notes — each resolves in full at the artifact cited

- **The gate is computed, never asserted.** Four hand-written labels went stale before the
  criteria were executable (`VER-014` R3-F1). Read no status sentence as authority.
- **Approvals and verification reports are superseded, not void** — both ruled by the human owner,
  stated at [`GATES.md`](GATES.md), computed by `aief_approval` and `aief_gate`. The verification
  relation is **sealed**: `C6` reads `VER-017`, which retires `VER-014`/`-015`/`-016` by pinning
  their bytes, so they keep their verdicts and editing one now **fails**.
- **`ECR-D-006` is the one live registry defect** — the framework manifest, not under `spec/**`,
  excluded by name in `GATES.md`. It is why 28 of 29 rows verify, why 2 of 622 tests fail, and why
  `aief_approval verify` exits 1 (`VER-017` N-4). Every `spec/**` row and chain resolves, and
  `spec/**` is unchanged since `5e7ac74`.
- **Compiler stage** declared, never inferred. B2a awaits Stage 6. `CMP-BLOCK-006` closed.
- **Budget.** 1100 cap, breached and reduced twice. `OI-C-10` holds the runway.
