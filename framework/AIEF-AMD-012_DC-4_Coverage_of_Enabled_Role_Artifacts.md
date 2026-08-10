# AIEF-AMD-012 — Architecture Amendment: DC-4 Coverage of Enabled-Role Artifacts

**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-01 + LAW-10 (change to a frozen artifact — `framework/framework.manifest.json`), LAW-02 (disposition of a recorded open item), LAW-12 (open decision with recorded rationale, never assumption)
**Scope:** The ruling of open item **OI-C-06** (recorded by AIEF-AMD-011 §AMD-35; cited pre-disposition in § *The item this instrument disposes*), narrowly — whether and how the three `software.*` role artifacts persisted by AIEF-AMD-011 enter DC-4's coverage before Compiler Stage 6 executes. **Nothing else.** No Stage 6 execution, no `core/MANIFEST.lock`, no compiler implementation, no BINDING change, no ledger write.
**Date:** 2026-08-08 · **Session:** `S-2026-08-08-06`
**Amends:** `framework/framework.manifest.json` — three changes, all inside `metadata.reproducible.digest_constructions.core_aggregate`, enumerated in `APR-010`
**Does not amend:** `SCH-framework-manifest.schema.json` (the amended manifest passes it unmodified — `metadata.reproducible` admits additional members) · `AIEF-FRZ-001` · `AIEF-AMD-001` … `AIEF-AMD-011` · either ADR · any law rule or clause · any role contract · any partition, layer, tier, boot step, stage or lifecycle definition · DC-1, DC-2, DC-3, DC-5, TF-1/TF-2 — preserved exactly as declared · DC-4's record grammar, record order, preimage, encoding, self-exclusion, B2a procedure, lock serialisation and worked example — all unchanged; only the coverage term is extended
**Authorising basis:** live human-owner instruction of session `S-2026-08-08-06` (`core/PRECEDENCE.md` rank 1) directing that OI-C-06 be ruled by A4 before Stage 6 execution; recorded per LAW-10 in `project/approvals/APR-010` and `project/approvals/APR-011`

---

## The item this instrument disposes

OI-C-06 (recorded, pre-disposition, at `project/OPEN_ITEMS.md:40`; moved to that register's Closed table by this disposition), recorded by AIEF-AMD-011 §AMD-35 (`framework/AIEF-AMD-011_Software_Role_Enablement.md:59-60`) and deliberately left unresolved there, has two prongs:

1. **Reproduction.** The three artifacts at `core/profiles/software/agents/AGT-*.md` are approved additions a mechanical Stage 1 render does not produce; a Stage 1 re-render or wholesale core upgrade will not reproduce them, and re-emission is owed under AMD-011's authority after any such operation.
2. **Coverage.** DC-4 as declared covers `core/profiles/<selected>/**` and the selected profile is `mechanical` (`project/BINDING.md:15`), so the three files sit outside the declared coverage: once Stage 6 runs, `core/MANIFEST.lock` and boot step B2a would not bind them. Until now their only integrity record is the three DC-1 digests bound in `APR-008` (`project/approvals/APR-008_Enable_Software_Roles.md:47`).

VER-005 lists this as an explicit Stage 6 prerequisite: *"before Stage 6 executes: an A4 ruling extending DC-4 coverage to enabled-role artifacts, or folding the enablement into the build's emitted set"* (`project/verification/VER-005_Independent_Verification_AIEF-AMD-011.md:53`).

## Independence declaration

OI-C-06 was recorded by `chief-systems-engineer · S-2026-08-08-05` (AMD-011 §AMD-35), which enacted the enablement and expressly did not resolve the coverage question. This ruling is made by `chief-systems-engineer · S-2026-08-08-06`, a cold session holding no state from any prior session. Under AMD-20, agent identity is the pair (role, session); recorder and ruler differ in session. The human owner directed that this ruling be made by A4, not by the implementation agent. The same-authority ruled-and-applied departure is separately recorded in § *Separation of Duties*.

| Ruling | Subject | Change class |
|---|---|---|
| AMD-39 | DC-4 coverage of enabled-role agent artifacts | Manifest change — the `covers` term extended; one new member `enabled_role_coverage` |
| AMD-40 | Worked-example validity, B2a semantics and closure of OI-C-06 | Consequence ruling — no further manifest change |

---

## AMD-39 — DC-4 Covers Enabled-Role Agent Artifacts, Resolved from `BINDING.enabled_agents`

**Disposes:** OI-C-06 prong 2 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-06`

### Gap, restated

DC-4's coverage term read: *"every files[] entry declared integrity hashed that the build emits for the selected profile - … core/profiles/<selected>/** …"* (`framework/framework.manifest.json` at APR-006's registered digest `ae16ccac…9d8395aa`, the `core_aggregate.covers` member; `framework/AIEF-AMD-010_Stage_6_Constructions_and_Preflight_Dispositions.md:127`). The three enabled-role artifacts are declared in `files[]` with `integrity: hashed` (`framework/framework.manifest.json:374-376`, ids `soft-agt-software`, `soft-agt-test`, `soft-agt-platform`) and sit in the `profile` partition, which declares `integrity_verified: true` (`framework/framework.manifest.json:219`) — yet under the selected profile `mechanical` they fall outside the covered set. A `hashed` declaration in an `integrity_verified` partition that no mechanism verifies is a dead declaration — the same FM-3 pattern AMD-27 closed for the root files (`framework/AIEF-AMD-010_Stage_6_Constructions_and_Preflight_Dispositions.md:162`). The freeze registry cannot absorb them: its declared scope is `spec/` and `framework/`, and `core/` is assigned to `core/MANIFEST.lock` and B2a (`project/FROZEN.md:19`).

### Ruling

> **DC-4's covered set is extended by exactly one term: the agent artifacts of enabled roles outside the selected profile, resolved deterministically from `project/BINDING.md` `enabled_agents`.** The covered set is now:
>
> **(i)** every `files[]` entry declared `integrity: hashed` that the build emits for the selected profile — the L0 root files, `core/**` including `core/templates/**` and `core/validation/**`, and `core/profiles/<selected>/**`, exactly as AMD-27 declared; **plus**
> **(ii)** for every role token of the form `<profile>.<name>` in `project/BINDING.md` `enabled_agents` whose `<profile>` is **not** the selected profile: the `files[]` entry whose `path` equals `core/profiles/<profile>/agents/AGT-<name>.md`.

Precisely, as now carried by the manifest (`metadata.reproducible.digest_constructions.core_aggregate`, members `covers` and `enabled_role_coverage`, `framework/framework.manifest.json:104-111`):

1. **Resolution rule.** A token `<profile>.<name>` resolves to the `files[]` entry at path `core/profiles/<profile>/agents/AGT-<name>.md`. That entry must exist in `files[]` and be declared `integrity: hashed`; a token that resolves to no such entry is a **coverage defect that halts the build** — the same defect discipline as DC-4's duplicate-path rule. The rule is exact today for all nine profile agents declared in `files[]` (mechanical four, software three, research two), and AMD-011 §AMD-36 already ruled that enabled-role artifacts are persisted *"at the exact paths `framework.manifest.json` `files[]` already declares for them"* (`framework/AIEF-AMD-011_Software_Role_Enablement.md:70-76`) — this ruling generalises that recorded correspondence into the coverage definition rather than inventing a new one.
2. **Undotted and selected-profile tokens add nothing.** A universal token (no `.`) resolves to `core/agents/AGT-<name>.md`, already covered under `core/**`; a selected-profile token's artifact is already covered under `core/profiles/<selected>/**`. Term (ii) is therefore additive-only and can never double-count: a path cannot be both inside and outside `core/profiles/<selected>/**`.
3. **Determinism and evaluability.** The covered set is a function of `files[]`, the selected profile and `BINDING.enabled_agents` **alone**. The working tree is never an input to coverage: an enabled-role artifact absent from the tree is a B2a coverage failure ("no covered-scope file is absent from the list and no listed file is absent from the tree" — the AMD-27 procedure, unchanged) and halts, blocking. DC-4 already took `BINDING.active_profile` as an input through `<selected>`; this ruling adds `BINDING.enabled_agents`, a field `sch-binding` requires (`framework/framework.manifest.json:570`, schemas entry `sch-binding`), and nothing else.
4. **B2a is strengthened, not weakened.** Every previously covered file remains covered; three files previously invisible to B2a become bound. The halt conditions are unchanged in kind and extended in reach. No record grammar, order, preimage, self-exclusion or output rule changes — one grammar for DC-2 and DC-4 remains one grammar.
5. **Scope limit — agent artifacts only.** `PROFILE.md` and the lifecycle artifacts of a non-selected profile remain uncovered **and unemitted**: AMD-011 §AMD-36 deliberately withheld them as dead files (`framework/AIEF-AMD-011_Software_Role_Enablement.md:81`), and a coverage term that demanded them would force B2a to fail forever or force their emission against that ruling.

### The Stage 6 implementation's covered-set procedure, machine-followable

For the avoidance of any implementation ambiguity, the covered set is computed thus:

```
S := selected profile (project/BINDING.md active_profile)
C := { f in files[] | f.integrity == "hashed"
       and f.path != "core/MANIFEST.lock"
       and f is emitted for S per AMD-27:
           f.path in {BOOT.md, FRAMEWORK.md, README.md}
           or f.path starts with "core/" and not "core/profiles/"
           or f.path starts with "core/profiles/" + S + "/" }
for each token t in project/BINDING.md enabled_agents:
    if t contains "." :
        (p, n) := t split at the first "."
        if p != S:
            f := the files[] entry with path "core/profiles/" + p + "/agents/AGT-" + n + ".md"
            if f does not exist in files[] or f.integrity != "hashed": HALT (coverage defect)
            C := C ∪ { f }
DC-4 := SHA-256 over the records (f.path, DC-1(f)) of C, per the unchanged grammar and order
```

For this instance today: `S = mechanical`; the twelve `enabled_agents` tokens (`project/BINDING.md:20-31`) contribute five undotted (nothing), four `mechanical.*` (nothing), and three `software.*` tokens resolving to `files[]` ids `soft-agt-software`, `soft-agt-test`, `soft-agt-platform` — exactly the three artifacts of OI-C-06, no more.

### Rejected alternatives

| # | Alternative | Why rejected |
|---|---|---|
| B | Coverage = every `files[]` entry declared `integrity: hashed` **that exists on disk** | Makes the working tree an input to the coverage definition, so the covered set is no longer evaluable from the manifest and BINDING alone; worse, deletion becomes self-excusing — a tampered-away covered file silently exits coverage instead of halting B2a. This *weakens* B2a and is rejected outright |
| C | Coverage = `core/profiles/<selected>/**` plus `core/profiles/<p>/**` wholesale for every profile `p` with an enabled role | Would cover the seven `software` artifacts (`PROFILE.md`, six `LC-S*`) that AMD-011 §AMD-36 deliberately did not emit; B2a would then either fail forever on absent files or force emission of dead files against that ruling. Contradicts AMD-011's recorded mechanism |
| D | Leave DC-4 as-is; bind the three files elsewhere — register them in `project/FROZEN.md`, or emit a second aggregate | `FROZEN.md`'s declared scope (AMD-21) is `spec/` and `framework/`; `core/` is expressly assigned to `MANIFEST.lock`/B2a (`project/FROZEN.md:19`) — registering core files there creates two overlapping integrity regimes with different verification procedures for one partition. A second aggregate is AMD-27 rejected-alternative D again: two aggregates, two pins, two failure modes, no additional protection (`framework/AIEF-AMD-010_Stage_6_Constructions_and_Preflight_Dispositions.md:178`) |
| E | Leave DC-4 as-is; rely on the APR-008 digests as the standing record | An approval is a record, not a verification: nothing recomputes those digests at boot, they go stale the moment the files are lawfully re-emitted after an upgrade, and B2a would continue to assert core integrity while excluding three live role contracts |
| F | Leave the exposure recorded and unbound (status quo) | Role contracts are instruction-channel artifacts, loaded at T2 on every dispatch of the enabled roles — among the highest-value tamper targets in the tree. A B2a that proves "core has not been tampered with" while excluding them proves less than it states, indefinitely. The exposure is exactly the class B2a exists to close, and Stage 6 — which does not yet exist — is the zero-marginal-cost moment to close it |

### Manifest change

Three changes, all inside `metadata.reproducible.digest_constructions.core_aggregate`; enumerated with before/after digests in `APR-010`:

1. `authority` — appended: *"coverage extended to enabled-role agent artifacts by AIEF-AMD-012 AMD-39, disposing OI-C-06"*.
2. `covers` — one inserted clause: *"plus every enabled-role agent artifact resolved per enabled_role_coverage"*.
3. `enabled_role_coverage` — new member carrying the normative resolution rule, determinism statement, scope limit and worked-example status.

No schema amendment: `metadata.reproducible` declares no `additionalProperties: false` and `digest_constructions` is itself an admitted additional member; the amended manifest passes the unmodified `SCH-framework-manifest.schema.json` under a JSON Schema 2020-12 validator (verified: PASS).

---

## AMD-40 — Worked Example Stands; B2a Semantics; Closure of OI-C-06

**Disposes:** OI-C-06 prong 1 consequence and the example-validity question · **Ruled by:** `chief-systems-engineer · S-2026-08-08-06`

### Ruling

1. **The DC-4 worked example stands, unchanged and valid.** It is synthetic and fixed (`framework/AIEF-AMD-010_Stage_6_Constructions_and_Preflight_Dispositions.md:134-156`): its two input pairs are given literally, its preimage and digest `eb6e969b9f1d31a367ccf83315c1a40f8df0bb1c7dec41566a637ac3740325b1` exercise the record grammar and ordering, which this instrument does not touch. The coverage term determines *which* pairs enter a live computation, not *how* pairs are hashed; the example's meaning — "any implementation must reproduce exactly this value for exactly this input" — is unaltered. Stated explicitly per the directing instruction: no coherence update is required.
2. **Prong 1 of OI-C-06 is not erased — it is now enforced.** A Stage 1 re-render or wholesale core upgrade still will not reproduce the three files, and re-emission remains owed under AMD-011's authority. What changes: after Stage 6 exists, their absence is no longer a silent loss — B2a halts on the missing covered files at the next boot. The obligation AMD-011 recorded in prose acquires a mechanism. With prong 2 closed by AMD-39 and prong 1 converted from unmonitored exposure to a halting check plus a recorded re-emission duty, **OI-C-06 closes**; the re-emission duty needs no successor open item because it is now self-announcing.
3. **Interim state, before Stage 6 exists.** B2a still cannot execute (`BINDING.core_digest_pin` is `PENDING-STAGE-6`). Until Stage 6 runs, the three files' integrity record remains the DC-1 digests in `APR-008` — unchanged from AMD-011, now time-bounded by this ruling instead of open-ended.
4. **Consequence for the Stage 6 implementation** (the `software.*` roles, once dispatched): the covered-set procedure of AMD-39 is normative input to CMP-BLOCK-004 work; `core/MANIFEST.lock.files` must list the enabled-role artifacts; V-12's tamper campaign gains three more covered targets. No check text changes: V-01…V-25 are untouched — coverage was always defined by reference to the DC-4 declaration, which is the single home this instrument amended.

---

## Blast Radius

| Artifact | Change | Method |
|---|---|---|
| `framework/framework.manifest.json` | The three `core_aggregate` changes of AMD-39 | Surgical edit under `APR-010`; re-registered in `FROZEN.md` at the new DC-1 |
| `framework/AIEF-AMD-012_DC-4_Coverage_of_Enabled_Role_Artifacts.md` | **NEW** — this instrument | Registered in `FROZEN.md` under `APR-011` (AMD-21 criterion) |
| `project/FROZEN.md` | Manifest row re-registered; this instrument added, 27 → 28; aggregate recomputed under DC-2; lineage retained, with the VER-005 FIND-Q5-2 clarity note added | Registry edit under `APR-010`/`APR-011` |
| `project/STATE.md` | `frozen_set_hash`; `open_non_blocking` OI-C-06 removed; `next_action`; § Frozen set counts | Session write |
| `project/OPEN_ITEMS.md` | OI-C-06 → Closed with resolution | Register edit |
| `ENGINEERING.md` | Index rows: amendment count, §5 row, §7 registry count and open/closed lists | Index edit |
| `project/approvals/APR-010`, `APR-011` | **NEW** — the two recorded approvals | LAW-10 |

**Deliberately not touched:** every `.ai/core/**` byte and `.ai/adapters/**` byte · `project/BINDING.md` (this ruling *reads* it; it does not change it) · `project/ledger/**` (`HEAD` remains at `genesis`) · `core/MANIFEST.lock` (**not created** — Stage 6 remains unauthorized, OQ-14) · `spec/**`, `AIEF-FRZ-001`, AMD-001…AMD-011, both ADRs, every schema · git history, tags, author or committer identity — no commit, tag or push is made by this session.

---

## Separation of Duties — Recorded Tension

`core/agents/INDEX.md`: **`chief-systems-engineer` may not implement what it approved.** This instrument was ruled, and its manifest, registry and index edits applied, by the same authority (`chief-systems-engineer · S-2026-08-08-06`) at the direction of the human owner — `core/PRECEDENCE.md` rank 1, which outranks the rank-6 agent specification. Identical in form to the departures recorded in AMD-008 through AMD-011 §§ *Separation of Duties*; identically **authorised, not erased** (SOD-1).

| | |
|---|---|
| Duty separated | A4 rules and approves; A1 implements |
| Departure | A4 both ruled and applied |
| Authority for the departure | Live human-owner instruction of `S-2026-08-08-06`, rank 1, recorded per LAW-10 in APR-010 and APR-011 |
| Mitigating control | Independent cold-context `qa-engineer` audit of this session's work — dispatched later this phase by the same directing authority |
| Not mitigated by | Anything this document says about itself. Under LAW-05 an authority's assertion about its own work carries no evidentiary weight |

---

## Approvals Required and Recorded

| Change | Approval | Bound to |
|---|---|---|
| The manifest amendment of AMD-39, and re-registration of the manifest in `FROZEN.md` at its post-change digest | `project/approvals/APR-010` | the post-change manifest DC-1 digest (`subject_hash`), with the pre-change digest as `prior_hash` |
| Freeze-registry addition of this document (AMD-21 criterion: authorising instrument for a change to a frozen artifact) | `project/approvals/APR-011` | this document's DC-1 digest |

Per the AMD-16 design property, neither this document's own digest nor the post-registration DC-2 aggregate appears in this document; both live in the registry and the approval artifacts.

---

**END OF AIEF-AMD-012**
