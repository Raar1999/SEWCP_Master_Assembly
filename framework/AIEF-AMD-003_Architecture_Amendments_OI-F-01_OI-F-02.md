# AIEF-AMD-003 — Architecture Amendment: OI-F-01, OI-F-02

**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-02
**Scope:** OI-F-01 and OI-F-02 only
**Date:** 2026-08-07
**Amends:** `.ai/project/BINDING.md`, `.ai/project/ledger/HEAD` — instance artifacts only
**Does not amend:** AIEF-FRZ-001 · AIEF-AMD-001 · AIEF-AMD-002 · `framework.manifest.json` · `SCH-framework-manifest.schema.json`

---

## AMD-09 — Session Timeout Value

**Closes:** OI-F-01 · **Change class:** value ruling, one line in one instance artifact

### Defect

`SCH-binding` requires the field `session_timeout`. AIEF-FRZ-001 §1.3 states that a lock older than *"the binding's `session_timeout`"* is reclaimable, but no value is declared anywhere in the frozen architecture. Stage 3 recorded the field as `UNSET` rather than inventing one.

### Ruling

> **`session_timeout` default = 14400 seconds (4 hours). Project-overridable in `project/BINDING.md`.**

### Rationale — the failure asymmetry decides it

| Direction of error | Consequence | Severity |
|---|---|---|
| **Too short** | An active long-running session has its lock reclaimed. Two sessions then write `STATE.md` and `HEAD` concurrently. **This is the lost-update failure the lock exists to prevent.** | **Severe — silent corruption** |
| **Too long** | A crashed session blocks the working tree until timeout. A human can force-release at any time. | Annoying — fully recoverable |

The failure modes are not symmetric, so the value errs long. Four hours exceeds any plausible single uninterrupted engineering session while ensuring a crash never blocks a full working day. Two properties bound the residual risk: reclamation is **ledger-recorded and therefore auditable**, and a human may force-release at any time without waiting.

### Scope of change

`session_timeout` is **instance data**, not framework data. It lives in `project/BINDING.md`, which the manifest already declares. **No manifest change and no schema change are required** — the field was always declared; only its value was absent. This is the smallest amendment consistent with the frozen framework.

---

## AMD-10 — Ledger Genesis Semantics

**Closes:** OI-F-02 · **Change class:** semantics ruling, no structural change

### Defect

Boot step B4 performs three checks:

1. The entry named by `HEAD` exists and hashes to `HEAD.entry_hash`
2. No file exists at `HEAD.seq + 1`
3. `STATE.last_ledger_seq` equals `HEAD.seq`

At installation the ledger is empty. **Check 1 has no subject**, and the frozen architecture does not say what B4 should do.

### Ruling

> **`HEAD.state` takes one of two values: `genesis` or `active`.**
>
> - At **`genesis`** — ledger empty, `seq: 0`, `entry_hash: null`, `prev_hash: null`. **B4 check 1 is vacuous by definition.** Checks 2 and 3 apply unchanged and are the operative reconciliation.
> - At **`active`** — all three checks apply unchanged.
> - **The first session close transitions `HEAD.state` from `genesis` to `active`** as part of the close transaction, writing entry `L-0000001` and setting `seq: 1`.
> - The transition occurs **once per repository** and is irreversible.

### Rationale

Two options existed. Emitting a synthetic genesis entry `L-0000000` would remove the special case from B4 entirely — but it requires the manifest to declare an artifact it does not currently declare, and it writes a ledger entry recording nothing. The state-flag ruling changes no structure, adds no artifact, and leaves B4's operative checks untouched.

**B4's anti-drift guarantee is preserved in full.** Checks 2 and 3 are what detect divergence between state and history; check 1 detects a corrupted or missing entry, which cannot exist when no entry exists. The ruling narrows nothing that was previously enforced.

### Scope of change

`HEAD` already carries `state: genesis`, emitted by Stage 3. This amendment formalises its meaning and defines the transition. **No manifest change, no schema change, no structural change.**

---

## Artifacts Modified

| Artifact | Change |
|---|---|
| `.ai/project/BINDING.md` | `session_timeout: UNSET` → `14400` |
| `.ai/project/ledger/HEAD` | Genesis semantics formalised; transition rule stated |
| `.ai/project/OPEN_ITEMS.md` | OI-F-01, OI-F-02 moved to closed |
| `.ai/project/STATE.md` | Two blockers removed from the blocker list |

## Artifacts Not Modified

`AIEF-FRZ-001` · `AIEF-AMD-001` · `AIEF-AMD-002` · `framework.manifest.json` · `SCH-framework-manifest.schema.json` · all 58 Stage 1 artifacts · the remaining 4 Stage 3 artifacts · 13 laws · 5 universal roles · 6 workflows · 6 stages · all ownership assignments.

**Both rulings were resolved without a single change to the framework partition.**

---

**END OF AIEF-AMD-003**
