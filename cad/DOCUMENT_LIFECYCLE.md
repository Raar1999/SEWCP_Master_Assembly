# Fusion document lifecycle — policy and defect record

> Session `S-2026-08-11-04`. Raised by the owner as an architecture defect:
> the system could create saved blank/interim Fusion designs during failed
> or partial autonomous runs, and quarantine-by-rename is not cleanup.

## Root cause — traced, not guessed

The compiled setup sequence of every component run was:

```
OP-0001 new_document      (unsaved - correct)
OP-0002 set_parameters
OP-0003 rename_component  <- ext op FIRST-SAVED a never-saved document
...geometry...
LC      save_document     (on PASS only)
```

`op_rename_component` performed `saveAs` at **setup time** because Fusion
refuses to rename the root component of an unsaved document. Persistence
therefore preceded geometry, and no failure path disposed of the document.
Evidence per artifact:

| Artifact | Creation path | Evidence |
|---|---|---|
| `ZZ-ORPHAN-BLANK-SHELL_SEWCP-300-20260811` (0 bodies, 0 sketches, 23 parameters, v1) | `rename_component` first-save during an interrupted heater rebuild attempt ≈18:41; the attempt died before geometry and before any run record was written | lineage created 18:41:37; orphan queue file `A1-RUN-20260811T184716-…S1-0001.cmd.json` with **no** `cad/runs/RUN-…184716` record; observed blank on open (`S-2026-08-11-02` G0) |
| `ZZ-INTERIM-ATTEMPT_SEWCP-901-20260811` (geometry present, unverified, v1) | `rename_component` first-save during `RUN-20260811T200134-c51fe2` (verdict FAIL — stale acceptance extents); no failure disposition existed | run record on disk; save obs embedded |
| Second `SEWCP-300_HEATER_PLATE` lineage (the live one) | the later PASS run (`RUN-20260811T190752`) started in a fresh document while the blank shell still held the name → duplicate lineage | run record; `list_documents` observation showing two same-named files |
| `ZZ-SUPERSEDED-FREE-S_SEWCP-901-20260811` (v2) | **not** a failure artifact — the geometry-phase verified strap (exports digest-recorded at `4d03041`), renamed out of the namespace when the installed-form re-issue took the name | `S-2026-08-11-02` G1 record |

## Policy (implemented)

| Class | Persistence | Mechanism |
|---|---|---|
| AUTHORITATIVE | saved, versioned, in the registry | first-save happens **only** in `save_document`, which the lifecycle layer dispatches **on verified PASS** |
| TEMPORARY / TEST | never saved | identity bound without persistence; discarded by recovery |
| FAILED ATTEMPT | never saved (or reverted if it dirtied a saved baseline) | orchestrator/AssemblyRunner failure disposition |

Mechanics:

1. **Identity without persistence.** `rename_component` on a never-saved
   document now binds an `aief:intended_name` design attribute and saves
   nothing. `_persisted_doc_name` (shell) and `_persisted_name` (ext) fall
   back to the intended name, so adoption, observation (`ACC-NAME`) and
   `save_document` all see the identity; `document.saved` keeps the
   persistence truth.
2. **Single persistence point.** `_first_save` is called only from
   `op_save_document` — enforced by
   `tests/test_document_lifecycle.py::test_only_the_verified_save_path_may_first_save`.
3. **Failure disposition.** On any non-PASS outcome the orchestrator and
   the assembly runner dispatch `discard_document` (closes a never-saved
   document; **refuses a saved one by contract**) and fall back to
   `revert_document` for a dirtied saved baseline. An authoritative design
   can therefore never be discarded by a failure path.
4. **Quarantine is not cleanup.** ZZ-renaming remains only the fallback
   when deletion is genuinely unavailable, and each such case must be
   recorded as an open item until deleted.

## Regression tests

`tests/test_document_lifecycle.py` — 11 tests: failed run discards and
never saves; three failure cycles accumulate nothing; adopted saved
baseline reverts instead of discarding; passing run saves exactly once and
only after observation; assembly failure discards / pass saves; structural
contracts on the deployed add-in source (no `saveAs` in the setup path,
single `_first_save` caller, discard refuses persisted documents, delete
guard protects the registry, shell reports intended identity without
claiming persistence).

## ZZ-* disposition (registry state at writing)

| Design | Class | Action |
|---|---|---|
| `ZZ-ORPHAN-BLANK-SHELL_SEWCP-300-20260811` | ORPHAN / DELETE | **DELETED** `S-2026-08-11-04` via the guarded op |
| `ZZ-INTERIM-ATTEMPT_SEWCP-901-20260811` | TEMPORARY / DELETE | **DELETED** `S-2026-08-11-04` via the guarded op |
| `ZZ-SUPERSEDED-FREE-S_SEWCP-901-20260811` | HISTORICAL / PRESERVE | the geometry-phase verified strap; its exports were overwritten by the re-issue, so this design is the last embodiment of the superseded baseline — deletion is an owner decision |

Added `S-2026-08-11-04`: `ZZ-DERIVATIVE-STUCK_SEWCP-200-20260811` —
HISTORICAL / QUARANTINE (OI-CAD-03). The original CP lineage's cloud
reference-derivative durably served v4 content to `addByInsert` while
`documents.open` resolved the verified tip (proven across cold sessions,
update-refs, re-insert, latest-version pinning and two content-neutral
version bumps). The verified content was re-homed to a fresh lineage that
now backs the assembly; the stuck lineage holds the v1..v7 history and
awaits owner disposition. **Live validation of the lifecycle fix**: a
deliberately failing run (`RUN-20260811T213959-12925c`) built geometry,
failed verification, was **discarded** by the failure disposition, and the
saved-design census was identical before and after (12 = 12).

Deletion is dispatched through the guarded `delete_data_file` op
(refuses protected names and open documents). If the host permission layer
again refuses the dispatch, that limitation is recorded and the artifacts
stay quarantined — with the lifecycle fix, **no new ones can appear**.
