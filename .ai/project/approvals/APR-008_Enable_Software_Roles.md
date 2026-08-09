# APR-008 — Enablement of the three `software.*` roles under AIEF-AMD-011

> **Instance artifact.** Partition `project`. Schema `core/schemas/SCH-approval.schema.json`, severity BLOCKING.
> Satisfies the recorded-human-approval requirement of LAW-01 and LAW-10 for the OQ-13 enablement enacted by AIEF-AMD-011.

```yaml
approval_id:   APR-008
approver:      human-owner            # BINDING.approval_authority
timestamp:     2026-08-08T08:33:10Z
subject_path:  framework/AIEF-AMD-011_Software_Role_Enablement.md
subject_hash:  59ecb5eb922f44a55cc42e51663dae9ee251269790958ee27ad93c1ba2ebaa53
prior_hash:    null                   # new instrument
scope:         Enactment of the OQ-13 decision per the subject instrument - additive enablement of
               software.software-engineer, software.test-engineer and software.platform-engineer in
               BINDING.enabled_agents; emission of their three role artifacts into
               core/profiles/software/agents/; roster propagation. Nothing else.
session:       S-2026-08-08-05
applied_by:    chief-systems-engineer · S-2026-08-08-05
basis:         the human owner's recorded OQ-13 decision, core/PRECEDENCE.md rank 1
```

---

## The human decision — recorded verbatim as the basis of this approval

> **"ENABLE the three software.\* roles for this SEWCP instance, following the existing AMD-006 profile-activation pattern. Do not activate them silently. The three software roles must be explicitly defined and persisted before implementation begins."**

This is the human owner's disposition of OQ-13 (options and recommendation recorded at `AIEF-AMD-010` §AMD-34; the decision selects option (a)). This artifact is its LAW-10 written form. Not silent: the enablement is carried by a registered instrument, this approval, `BINDING.md`, `ROSTER.md` and the three persisted role contracts.

## Subject

`framework/AIEF-AMD-011_Software_Role_Enablement.md`, at DC-1 normalised SHA-256
`59ecb5eb922f44a55cc42e51663dae9ee251269790958ee27ad93c1ba2ebaa53`.

**This approval is bound to that hash.** Per LAW-10 it is void if the subject content changes, and it names precisely what it approves.

## Every artifact changed or created under this approval

**Frozen-partition additions (core), bound by DC-1:**

| Artifact | DC-1 digest |
|---|---|
| `core/profiles/software/agents/AGT-software-engineer.md` | `6bc734d47ceacbc8f9e2a5c31b41fac31083dc0f6dcaee47191053aaf19ce717` |
| `core/profiles/software/agents/AGT-test-engineer.md` | `bb8cebd57b65091774182ecef56991ffb50564bbefa6dda47b3ccc63227127d8` |
| `core/profiles/software/agents/AGT-platform-engineer.md` | `96e5680c1edb51b960afe410b3482e1c331e9a818764e7b8ff00548560c3e4fd` |

Zero pre-existing `core/**` bytes change; the core-partition change is these three additions only. They are not entered in `project/FROZEN.md` — its declared scope (AMD-21) is `spec/` and `framework/`; `core/` is covered by `core/MANIFEST.lock` and B2a once Stage 6 exists. Until then these digests, recorded here, are their only integrity record (the OI-C-06 residual).

**Mutable instance artifacts (unhashed by declaration; `binding` and `roster` carry `integrity: unhashed`, and AMD-22 rules BINDING mutable and unhashed). Post-change DC-1 content fingerprints recorded informationally — these are NOT freeze registrations and bind nothing:**

| Artifact | Change | Informational content fingerprint (DC-1, post-change) |
|---|---|---|
| `project/BINDING.md` | `enabled_agents` 9 → 12, the three roles added at A1 with `# A1 - AIEF-AMD-011` refs; no other field | `64a9ca216606e502ca186985dc4ef22d5f7fd0504ed281b392c84910ac81a15f` |
| `project/ROSTER.md` | `Profile software` section, three UNASSIGNED rows | `2443cf4928fc659437c6d64d195e97d092b670e29ea971d5c385161576ba2947` |

**Register and index updates executed with the enablement:** `project/FROZEN.md` (via `APR-009`), `project/STATE.md`, `project/OPEN_ITEMS.md` (OQ-13 closed; OI-C-06/OI-C-07 opened), `ENGINEERING.md`.

## Scope

| In scope | Out of scope |
|---|---|
| The changes enumerated above, and no others | Any change to `framework/framework.manifest.json` — **not amended** (AMD-37); its registration and `APR-006` binding stand |
| | Activation of the software profile or lifecycle; any change to `active_profile`, `lifecycle_stage` or `active_gate` |
| | Emission of `core/profiles/software/PROFILE.md` or any `lifecycle/LC-S*` artifact |
| | Registration of `AIEF-AMD-011` itself — separate instrument, `APR-009` |
| | Execution of Compiler Stage 6; creation of `core/MANIFEST.lock`; any write to `BINDING.core_digest_pin`; any compiler implementation work; any task allocation or role assignment |
| | Any ledger write, any git commit, tag or push |

## Verification status

Ruled and applied by the same authority, `chief-systems-engineer · S-2026-08-08-05`, at the direction of the human owner. The separation-of-duties departure is recorded in AIEF-AMD-011 § *Separation of Duties* (SOD-1 pattern). Under LAW-05 this session cannot verify its own work; an independent cold-context `qa-engineer` audit of this session's work is dispatched by the same directing authority as the mitigating control.

Reproducible by a third party from the repository alone: the working-tree subject normalises to `subject_hash` under DC-1; each emitted role artifact normalises to its digest above; each artifact's content is derivable field-by-field from the unchanged manifest's `agents.profile` contracts.

## Authority chain

| | |
|---|---|
| `core/PRECEDENCE.md` rank 1 | The human owner's OQ-13 decision — the authorising basis |
| LAW-01 | A frozen artifact (the core partition, clause 2) is changed only under an approved instrument and a recorded human approval |
| LAW-10 | Approval is an artifact bound to a content hash |
| LAW-12 | The allocation question was held open (OQ-13) until decided, never assumed |
| AIEF-AMD-010 §AMD-34 | The options analysis and mechanism this decision selects from |
| AIEF-AMD-006 | The role-enablement precedent this decision directs following |
| `project/BINDING.md` | `approval_authority: human-owner` |
| AIEF-AMD-011 | The instrument this approval authorises |
