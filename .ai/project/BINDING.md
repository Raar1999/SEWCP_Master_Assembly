# Project Binding

> **Instance artifact.** Emitted by aief-compile Stage 3 from `framework.manifest.json` and live repository state.
> Partition `project` — never touched by framework upgrade. Owner `project-manager`. Mutability mutable.

---

Schema: `core/schemas/SCH-binding.schema.json`

```yaml
framework_version_pin: ">=1.0.0 <2.0.0"
core_digest_pin:       PENDING-STAGE-6   # emitted by Compiler Stage 6
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
```

## Notes

- `core_digest_pin` is set by Compiler Stage 6. Boot step **B2a cannot execute until then**.
- `host_adapter` is `claude-code`; binding specified in `adapters/ADP-claude-code.md`, host hook installed at `CLAUDE.md`.
- `session_timeout` is 4 hours per AIEF-AMD-003 §AMD-09. Reclamation of a stale lock is **ledger-recorded**; a human may force-release at any time without waiting. Projects may override this value.
