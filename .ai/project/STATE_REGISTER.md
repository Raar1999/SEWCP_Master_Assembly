# Current State — Register

> **Instance artifact.** Emitted by aief-compile Stage 3 from `framework.manifest.json` and live repository state.
> Partition `project` — never touched by framework upgrade. Owner `chief-systems-engineer`. Mutability mutable.
> **Tier T4**, `token_cap: null` — `files[state-register]`. Loaded on explicit request, never at boot.

---

**This register is the detail behind [`STATE.md`](STATE.md).** `STATE.md` remains the file
boot reads at **B3** and remains authoritative for the eight `sch-state` required field
*values*; this register carries their detail, rationale and pointers. The split was enacted by
[`AIEF-AMD-014`](../../framework/AIEF-AMD-014_OQ-15_Enactment_Bounded_Register_Split.md)
§AMD-49 under the human owner's OQ-15 decision, option (a).

**Mapping — normative**, declared at `metadata.reproducible.bounded_register_split.mapping_state`
and checked by `V-03`: *every key of the YAML block of `project/STATE.md` appears exactly once
as a level-2 heading below, and every level-2 heading below is either such a key or the literal
heading `Notes`.*

> **This file did not exist until `S-2026-08-17-01`.** `files[state-register]` was added to the
> frozen manifest by `AIEF-AMD-014` §AMD-49 on 2026-08-08 and the file was never written.
> `V-03` was declared BLOCKING over both pairs and `check_v03` implemented only the
> `open-items` pair — with the *existence* test sitting behind the pair-specific branch, so the
> absence could not be seen. `V-03` reported PASS over `register_pairs: 1` of 2 for four
> sessions. `TCR-002` F-2 recorded the missing file as **BLOCKING** on 2026-08-09 and was
> never actioned; the residual was recorded only in a Python docstring. Found by the
> `OI-V-13` independent cold audit as **FIND-3**, and repaired here together with the check.

## lifecycle_stage

`LC-M04` — Implementation, `mechanical` profile. The stage has not moved since the CAD
authorisation; nothing in this session's work is a lifecycle transition.

## active_gate

`LC-M04-EXIT`, terminal. **Computed, never asserted** — `PYTHONPATH=src python -m aief_gate`
prints `LC-M04 CAD-READY: YES` and exits 0. Four hand-written labels went stale before the
criteria were executable (`VER-014` R3-F1); read no status sentence anywhere as authority,
including this one. `C6` reads `VER-017` under the sealed supersession relation ruled at
`ECR-D-012` and bound by `APR-028`.

The gate is the design-authority **precondition for CAD**, not the stage exit — see
[`GATES.md`](GATES.md) § *Deferred*.

## compiler_stage

All six emitted. Stage 6's canonical emission ran 2026-08-12 under the owner's `OQ-14`
authorization, writing exactly two files — `core/MANIFEST.lock` and the
`BINDING.core_digest_pin` line. **Boot step `B2a` executes and passes**: 75 of 75 DC-1 records
reproduce, DC-4 over them equals `MANIFEST.lock.aggregate_digest`, and that equals
`BINDING.core_digest_pin`. Re-verified independently at `S-2026-08-17-01` by the `OI-V-13`
auditor, who recomputed all three without importing `src/aief_stage6` and derived the covered
set from `files[].integrity` plus `enabled_role_coverage` rather than reading the lock's list —
expected 75, listed 75, symmetric difference empty.

`CMP-BLOCK-004` and `CMP-BLOCK-005` stand and are untouched by the emission: the full
six-stage compiler and the validation-campaign infrastructure are still absent. They gate
**AIEF framework Release 1.0.0**, which is a different release from this repository's — see
§ *blockers*.

## last_ledger_seq

**The value is on `STATE.md` and in `ledger/HEAD`, and it is deliberately not repeated here.**

> **Why this section states no number.** It stated one three times, and it was wrong three
> times — `1` when the value was 2, then `2` when the value was 3, each written before the
> session close that moved it and each caught by a later independent round (FIND-11, then
> round 3 FIND-1). Three occurrences of one defect is not three mistakes; it is a
> **structural** one: a register drafted before a close cannot recite a field the close
> writes, and no amount of care changes that ordering.
>
> So the recital is gone rather than corrected a fourth time, and
> `tests/test_state_register_currency.py` now **fails** if any section of this file states a
> `last_ledger_seq` value that disagrees with `ledger/HEAD` — the property, checked, instead
> of a convention to be careful.

What this section does record is the part that does not move: the ledger became `active` at
the `S-2026-08-12-01` LAW-09 close, writing `L-0000001` under DC-3 — once per repository,
irreversible. No earlier session wrote an entry, so the trail does not reach back over them
(`OI-P-01`). Each entry's `prev_hash` is a covered DC-3 field, which is what makes the chain
tamper-evident rather than merely sequential.

## frozen_set_hash

DC-2 over the freeze registry, recomputed whenever a registered artifact is re-registered.
Independently reproduced at the `OI-V-13` audit: 31 registered rows, all 31 reproduce, and the
DC-2 aggregate equals the value `STATE.md` carries. The audit also reconstructed both prior
lineage values exactly.

## active_tasks

Empty. Task records at [`tasks/`](tasks/); published results at [`results/`](results/).

**Which result is the current head is computed, not recited here** — `python -m aief_exec
check` derives it, and `X-06` fails if any record declares `CURRENT` over bytes that have
moved.

> This section named `R-017` as the head, then `R-021`/`R-023`/`R-025`; both were stale within
> the commit that wrote them, because publishing a superseding record is exactly what a
> session doing this work does. Same structural defect as § *last_ledger_seq*, same fix:
> `tests/test_state_register_currency.py` fails if this file names a result id as a current
> head that `aief_exec` does not agree is current.

## blockers

Carried on `STATE.md`. The distinction that matters and that no single word conveys:

| Blocker | Gates what |
|---|---|
| `CMP-BLOCK-004` | **AIEF framework Release 1.0.0** — the full six-stage compiler as software. Not this repository's release |
| `CMP-BLOCK-005` | **AIEF framework Release 1.0.0** — validation-campaign infrastructure, V-10/V-12/V-15/V-18 evidence |
| `ECR-D-016` | **SEWCP hardware build.** The Support Ring isolation joint does not close: `SR-02`, `SR-03` and `SR-04` all fail on frozen dimensions. Ruled at `S-2026-08-17-01`, implemented at Rev B. Blocks no gate, no deliverable and no repository release |

## open_non_blocking

The authoritative list is [`OPEN_ITEMS.md`](OPEN_ITEMS.md) (the bounded index read at B7) and
[`OPEN_ITEMS_REGISTER.md`](OPEN_ITEMS_REGISTER.md) (the register). This section does not
duplicate them and never enumerates them — that is the whole point of the split.

What this section records instead is the **shape** of what is open, which the index cannot
carry: the great majority are framework-layer items owed to a Stage 1/4/5 re-emission that
`CMP-BLOCK-004` blocks (`OI-C-02`, `OI-C-07`, `OI-V-07`), or verification residuals whose
findings are dispositioned individually within their own reports. The engineering-layer items
are few and each is named in `blockers` or carries its own ECR.

## next_action

Carried in full on `STATE.md`, which is where a booting session reads it. It is a pointer, not
a plan: the plan is the open-items register and the ECR records.

## Notes

- **The register is the authority for detail; `STATE.md` is the authority for values.** Where
  a field value here disagrees with `STATE.md`, `STATE.md` governs — it is the file `sch-state`
  validates and the file B3 reads. This register may not be cited for a field value.
- **Nothing here is loaded at boot.** Tier T4, `token_cap: null`. That is what bounds boot cost
  under unbounded register growth, and it is why this file may say as much as it needs to.
- **`OI-C-08` remains uncured**: `project/ledger/HEAD` is read at boot step B4 and carries no
  `token_cap`, so the V-09 measured set under-covers the boot-loaded set by exactly one file.
  Slack against MI-4 is 96 tokens, and `HEAD` has now been trimmed twice to stay small — the figure is not quoted here for the same reason as the two sections above. Curing it is a human-owner
  architecture decision, not a repair.
