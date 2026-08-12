# Project Binding

> **Instance artifact.** Emitted by aief-compile Stage 3 from `framework.manifest.json` and live repository state.
> Partition `project` — never touched by framework upgrade. Owner `project-manager`. Mutability mutable.

---

Schema: `core/schemas/SCH-binding.schema.json`

```yaml
framework_version_pin: ">=1.0.0 <2.0.0"
core_digest_pin:       2180df021b892ee0c19d7bc164713e46b1003bfb193497cad06b6c20f5ac92f0   # emitted by Compiler Stage 6
lifecycle_stage:       LC-M04   # Implementation
active_gate:           LC-M04-EXIT   # terminal, BLOCKED
active_profile:        mechanical
approval_authority:    human-owner
host_adapter:          claude-code   # AIEF-AMD-005, Stage 4
session_timeout:       14400   # seconds (4 h) - AIEF-AMD-003 AMD-09
enabled_agents:
  - repository-engineer   # A1
  - documentation-engineer   # A1
  - qa-engineer   # A2
  - project-manager   # A3
  - chief-systems-engineer   # A4
  - mechanical.design-engineer   # A1
  - mechanical.cad-engineer   # A1 - AIEF-AMD-006
  - mechanical.manufacturing-engineer   # A1
  - mechanical.simulation-engineer   # A1
  - software.software-engineer   # A1 - AIEF-AMD-011
  - software.test-engineer   # A1 - AIEF-AMD-011
  - software.platform-engineer   # A1 - AIEF-AMD-011
```

## Notes

- `core_digest_pin` carried the Stage 3 placeholder until **2026-08-12**, when the canonical
  Stage 6 emission set it under the owner's `OQ-14` authorization
  (`decisions/DECISIONS_S-2026-08-11-06` DEC-10). **Boot step B2a executes from that write
  onward**: recompute DC-1 over the 75 files `core/MANIFEST.lock` lists, recompute DC-4 over
  those records, compare to `MANIFEST.lock.aggregate_digest` and to this pin. Not a status
  flag — change one covered byte and B2a halts the boot. The placeholder token itself is
  deliberately not quoted here: `test_pin_preview_replaces_only_the_value` requires it to
  survive nowhere in this file after the pin is written.
- `host_adapter` is `claude-code`; binding specified in `adapters/ADP-claude-code.md`, host hook installed at `CLAUDE.md`.
- `session_timeout` is 4 hours per AIEF-AMD-003 §AMD-09. Reclamation of a stale lock is **ledger-recorded**; a human may force-release at any time without waiting. Projects may override this value.
