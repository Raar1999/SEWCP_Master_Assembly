# Fusion Lineage Census and OI-CAD-03 Deletion Recommendation

> **Instance artifact.** Partition `cad`. Compiled `S-2026-08-11-06` by the release-readiness
> audit. **No lineage is deleted by this document.** It recommends; deletion is a separate,
> guarded act.

---

## 0 · Provenance of this census, and its one limit

Every fact below is read from **recorded bridge evidence**, never from memory and never from a
live query. The authoritative roster is `observed.saved_designs` of the last
`list_documents` observation:

| | |
|---|---|
| Observation | `cad/bridge/obs/ADM-1786469127-list_documents.obs.json` |
| Observed at | **2026-08-11T17:25:29Z** |
| Fusion build | 2704.1.53, folder `Automata` |
| Roster size | **15 lineages** |

> **That observation is under a gitignored path** (`.gitignore` ignores
> `cad/bridge/queue|obs|state`, and `git ls-files cad/bridge` returns nothing), so a clone of
> this repository does not carry it and could not reproduce the census from the citation alone.
> The roster is therefore **distilled into a tracked record**:
> [`runs/LINEAGE_ROSTER_S-2026-08-11-06.json`](runs/LINEAGE_ROSTER_S-2026-08-11-06.json), which
> carries all 15 name/version/URN triples and the **raw-octet SHA-256 of the source
> observation**, `29985f6968fef271…`, so the distillation can be checked against the original
> wherever the original still exists.

> **The limit, stated plainly: the bridge is not live in this session, so this is the roster as
> *last observed*, not as *now*.** Nothing in this document should be read as a claim about the
> present contents of the Fusion project. Anyone acting on it should re-run `list_documents`
> first and confirm the four `id` URNs below still resolve to the four names below. **Deleting a
> lineage by name against a stale roster is exactly how the wrong document gets destroyed** —
> which is why every recommendation below is keyed on the **lineage URN**, not the name.

## 1 · The roster — 11 authoritative + 4 quarantined = 15

### Authoritative

| # | Name | v | Lineage URN |
|---|---|---|---|
| 1 | `SEWCP-000_MASTER_ASSEMBLY` | 6 | `urn:adsk.wipprod:dm.lineage:mrzDte2jQPmpOUjkHtqdwg` |
| 2 | `SEWCP-200_COOLING_PLATE` | 2 | `urn:adsk.wipprod:dm.lineage:Bv-XxqZ6St-HOhXhFEaWaw` |
| 3 | `SEWCP-300_HEATER_PLATE` | 2 | `urn:adsk.wipprod:dm.lineage:t6Fu9jXoSIuqLifomxpPbQ` |
| 4 | `SEWCP-400_SUPPORT_RING` | 2 | `urn:adsk.wipprod:dm.lineage:pcZtbk4zRJ6XeA_kqWXXcw` |
| 5 | `SEWCP-500_ESC_PUCK` | 2 | `urn:adsk.wipprod:dm.lineage:J4N_VRDwQR-NlQR5Sl9pFg` |
| 6 | `SEWCP-600_LIFT_PIN` | 2 | `urn:adsk.wipprod:dm.lineage:AC0d1piXT3uIZ-r4LAeuiw` |
| 7 | `SEWCP-700_ALIGNMENT_PIN` | 2 | `urn:adsk.wipprod:dm.lineage:hD6s1e5fQO2y_3bMi4s0Uw` |
| 8 | `SEWCP-800_PORT_BODY` | 2 | `urn:adsk.wipprod:dm.lineage:57nBymVUSoCGUNrj50FRiA` |
| 9 | `SEWCP-901_RF_STRAP` | 1 | `urn:adsk.wipprod:dm.lineage:scDapbt6Q-GB_IVL7wVLKg` |
| 10 | `SEWCP-902_SADDLE` | 1 | `urn:adsk.wipprod:dm.lineage:LSt7GS_WReSy6gzDGpZYEA` |
| 11 | `SEWCP-1000_RETAINER` | 2 | `urn:adsk.wipprod:dm.lineage:OgxUY0d9SK2YkEPXUz5HIA` |

### Quarantined — `OI-CAD-03`

| # | Name | v | Lineage URN |
|---|---|---|---|
| Q1 | `ZZ-DERIVATIVE-STUCK_SEWCP-200-20260811` | **7** | `urn:adsk.wipprod:dm.lineage:WoAxyypMTw6xu9URnJdThg` |
| Q2 | `ZZ-SUPERSEDED-FREE-S_SEWCP-901-20260811` | 2 | `urn:adsk.wipprod:dm.lineage:VGIDVJ6bSv2906tGL6aHhQ` |
| Q3 | `ZZ-SUPERSEDED-HOLES25_SEWCP-901-20260811` | 2 | `urn:adsk.wipprod:dm.lineage:g7BHnQL5T7ymp5uO0DNuCA` |
| Q4 | `ZZ-SUPERSEDED-BLOCK_SEWCP-902-20260811` | 2 | `urn:adsk.wipprod:dm.lineage:HrY3qvIYTQOVErReu60G7Q` |

**The register's count is confirmed by observation: 11 + 4 = 15, and the roster holds exactly 15.**

### Already deleted, and correctly — the failure-artifact class

Two further `ZZ-` names appear in the bridge record and are **absent from the roster**, having
been deleted at `S-2026-08-11-04`:

| Name | Deleted by | Why deletion was right |
|---|---|---|
| `ZZ-ORPHAN-BLANK-SHELL_SEWCP-300-20260811` | `ADM-1786464573-delete_data_file` | A blank shell — a document created by the pre-repair lifecycle that bound an identity and then persisted with no geometry. It never held engineering content |
| `ZZ-INTERIM-ATTEMPT_SEWCP-901-20260811` | `ADM-1786464575-delete_data_file` | An interim strap attempt superseded within the same session, before any verification ran against it |

**These two are the whole reason the four below are a different question.** A failure artifact
records nothing; a superseded verified baseline records how the design got where it is.

## 2 · Reference analysis — computed, per lineage

Scanned: every `*.md`, `*.json`, `*.csv` and `*.py` under the repository, and every `*.json` and
`*.csv` under `D:\AIEF_CAD_OUTPUT\SEWCP\`. `cad/bridge/**` is reported separately because it is
the *historical record of the quarantine itself* — a reference there is evidence, never a live
dependency.

| | Q1 stuck CP | Q2 free-S strap | Q3 holes25 strap | Q4 block saddle |
|---|---|---|---|---|
| Master assembly (`.assembly.json`) | **no** | **no** | **no** | **no** |
| Assembly run `ASSEMBLY_S-2026-08-11-05` | **no** | **no** | **no** | **no** |
| `FINAL_SYSTEM_VERIFICATION.json` | **no** | **no** | **no** | **no** |
| `SYSTEM_INTERFACES.json` | **no** | **no** | **no** | **no** |
| BOM (`SEWCP-000_BOM_RevA.csv`) | **no** | **no** | **no** | **no** |
| Any external deliverable | **no** | **no** | **no** | **no** |
| `cad/DELIVERABLES.md` | no | **yes** | no | no |
| `cad/DOCUMENT_LIFECYCLE.md` | **yes** | **yes** | no | no |
| `cad/BRIDGE_RESUME.md` | no | **yes** | no | no |
| `cad/runs/REPAIRS_S-2026-08-11-04.json` | **yes** | no | no | no |
| `OPEN_ITEMS_REGISTER.md` (the `OI-CAD-03` row) | yes | yes | yes | yes |
| `cad/bridge/**` log entries | 15 | 21 | 7 | 7 |

**No quarantined lineage is an active reference of anything.** Not one is bound by the assembly,
named in the BOM, or reachable from a deliverable. Every surviving reference is *narrative* — a
record that the lineage was superseded — and every such reference survives deletion of the
lineage, because it names a history rather than resolving to a document.

## 3 · Per-lineage disposition

### Q1 · `ZZ-DERIVATIVE-STUCK_SEWCP-200-20260811` — **PRESERVE. Do not delete.**

| | |
|---|---|
| What it is | The **original** SEWCP-200 Cooling Plate lineage, quarantined at `ADM-1786465008` when its cloud reference-derivative proved durably stuck at v4 (`OI-CAD-02`) |
| Version depth | **v7** — the only lineage at more than v2 in the entire project |
| What it holds | **The whole modelling history of the Cooling Plate, v1 through v7**: the channel routing, the choke counterbores, the kinematic locators, the ECR-D-002 depth change, the ECR-D-010 re-clocking |
| What replaced it | `SEWCP-200_COOLING_PLATE` (`Bv-XxqZ6…`), the re-homed lineage — **which is at v2** |
| Historical value | **Highest of the four, and not close.** The re-homed lineage carries the verified *content* and none of the *history*. Delete Q1 and the CAD build history of the most expensive, most iterated part in the stack — nine components' worth of dispositioned ECRs land on this one part — ceases to exist anywhere. The repository holds run records of what was built; it does not hold the parametric timeline |
| Deletion would destroy required engineering history | **YES** |
| **Recommendation** | **PRESERVE INDEFINITELY.** This is not "keep it for now" — it is the archival record of how SEWCP-200 was designed, and there is no second copy |

### Q2 · `ZZ-SUPERSEDED-FREE-S_SEWCP-901-20260811` — **PRESERVE.**

| | |
|---|---|
| What it is | The geometry-phase RF strap in its **free-state neutral-S** form, quarantined at `ADM-1786458683` |
| Why superseded | It could not mate the `CP-IF-8` land; re-derived to the installed form (`S-2026-08-11-02`, `RUN-20260811T200254-ca7080`, PASS 15/15) |
| Historical value | **High, and of a specific kind: it is the physical evidence for a design lesson.** The free-state form is the one a reader would naively re-derive; this lineage is the record that it was tried and why it failed. `cad/DELIVERABLES.md` cites it by name as the preserved superseded lineage, and `cad/BRIDGE_RESUME.md` classified it `HISTORICAL/PRESERVE` |
| Deletion would destroy required engineering history | **YES** — the free-state → installed-form derivation exists nowhere else as geometry |
| **Recommendation** | **PRESERVE.** Already classified `HISTORICAL/PRESERVE` and owner-reserved at `S-2026-08-11-04`; that classification is confirmed by this audit, not revisited |

### Q3 · `ZZ-SUPERSEDED-HOLES25_SEWCP-901-20260811` — **PRESERVE, lower value.**

| | |
|---|---|
| What it is | The RF strap at the **pre-`ECR-D-013`** hole pitch — `RS-D07`'s 25.0 mm centres |
| Why superseded | `ECR-D-013` DEC-01 re-pitched the holes tap-coincident (29.94 mm in the pad plane) |
| Historical value | **Moderate.** It is the geometric embodiment of the `ECR-D-013` conflict — the state in which two conforming parts did not fit. The conflict itself is fully recorded in prose and dimensions at `ECR-D-013` and `DECISIONS_S-2026-08-11-05` DEC-01, so unlike Q1 and Q2 the *reasoning* survives without it. What is lost on deletion is the demonstrable article |
| Deletion would destroy required engineering history | **NO** — the ECR record is complete and self-contained |
| **Recommendation** | **PRESERVE.** Deletion is *defensible* here and not required; the storage cost of a v2 lineage is negligible against the value of being able to open the exact state a dispositioned ECR-D describes. If the owner wants the project tidied, this is the first of the four that may lawfully go |

### Q4 · `ZZ-SUPERSEDED-BLOCK_SEWCP-902-20260811` — **PRESERVE, lower value.**

| | |
|---|---|
| What it is | The saddle in its **pre-`ECR-Q-012`** base-seated block form |
| Why superseded | `ECR-Q-012` DEC-02: the base-seated form violates `SB-D04` (≥ 8.0 to Base Plate) and `RF-IF-3` (*"mounts to the RF-hot plate, not to ground"*) — a grounded aluminium saddle under the strap is a **short**. Re-architected as the plate-hung hanger |
| Historical value | **Moderate, and safety-relevant.** This lineage is the article that would have shorted the RF circuit. Keeping it is keeping the counter-example that the disposition exists to prevent |
| Deletion would destroy required engineering history | **NO** — `ECR-Q-012` and DEC-02 carry the full architecture, the rejected alternatives and the DR-12 ground |
| **Recommendation** | **PRESERVE.** Same reasoning as Q3. If the owner elects to delete, Q3 and Q4 are the two that may go; **Q1 and Q2 must not** |

## 4 · Summary recommendation

| | Q1 stuck CP v7 | Q2 free-S strap | Q3 holes25 strap | Q4 block saddle |
|---|---|---|---|---|
| Active references | none | none | none | none |
| Unique engineering history | **irreplaceable** | **irreplaceable** | recorded elsewhere | recorded elsewhere |
| Deletion destroys required history | **YES** | **YES** | no | no |
| **Recommendation** | **PRESERVE INDEFINITELY** | **PRESERVE** | PRESERVE (deletion defensible) | PRESERVE (deletion defensible) |

**This audit deletes nothing and recommends deleting nothing.** All four are HISTORICAL. Two of
them are the only surviving record of how their part came to be.

**`OI-CAD-03` therefore remains OPEN and OWNER-RESERVED**, and it is **NON-BLOCKING**: it blocks
no gate, no deliverable, no verification and no release. Four quarantined lineages sitting in a
cloud project alongside eleven authoritative ones, each named so its status is unmistakable, is a
sound resting state — not a defect awaiting cleanup.

## 5 · If deletion is ever authorised — the guarded procedure

Deletion occurs **only** through the bridge's guarded `delete_data_file` operation, never by hand
in the Fusion UI, so that the act lands in the observation log with a command record. The
procedure that deleted the two failure artifacts at `S-2026-08-11-04` is the precedent
(`ADM-1786464573`, `ADM-1786464575`).

| Step | |
|---|---|
| 1 | Re-run `list_documents`. **Confirm the roster is still 15 and that the target's `id` URN still carries the expected name.** A name-keyed delete against a stale roster is unsafe; the URNs in §1 are the identity |
| 2 | Confirm from the fresh observation that the target is **not** an occurrence of `SEWCP-000_MASTER_ASSEMBLY` |
| 3 | Issue `delete_data_file` keyed on the **URN**, one lineage per command |
| 4 | Re-run `list_documents` and `observe_assembly`; confirm the roster shrank by exactly one and the assembly still verifies 19 occurrences |
| 5 | Record the deletion in this file and in the `OI-CAD-03` register row, retaining the deleted lineage's URN and version depth so the loss is itself a record |

**Nothing in this file authorises step 3.**
