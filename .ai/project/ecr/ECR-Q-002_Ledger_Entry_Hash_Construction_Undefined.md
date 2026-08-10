# ECR-Q-002 — Ledger entry-hash construction is undefined

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised at attempted session close, session `S-2026-08-08-01`.

```yaml
ecr_id:       ECR-Q-002
class:        Q                      # ambiguity - LAW-02
raised_by:    role-unrecorded · S-2026-08-08-01
status:       CLOSED
disposition:  A - DECLARE THE CONSTRUCTION EXPLICITLY
ruled_by:     chief-systems-engineer · S-2026-08-08-02
instrument:   AIEF-AMD-008 §AMD-17
approval:     approvals/APR-002_Amend_Framework_Manifest_AMD-008.md
affected_artifacts:
  - framework/framework.manifest.json
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-08T01:31:23Z
closed_at:    2026-08-08T02:36:52Z
related:      ECR-Q-001              # same root cause; resolved jointly, as recommended
```

> **`raised_by` was recorded as `claude-code session S-2026-08-08-01`.** Corrected under `AIEF-AMD-008` §AMD-20, on the same basis stated in ECR-Q-001. The role is `role-unrecorded` because no role assignment for `S-2026-08-08-01` is recoverable from the repository. Recorded as **OI-P-01**.

---

## 1 · Class

**Q — ambiguity.** The ledger requires an `entry_hash` and a `prev_hash` chain, but no artifact declares **how `entry_hash` is computed**. Nothing is contradictory; the method is absent.

## 2 · Affected artifacts

| Artifact | Role |
|---|---|
| `.ai/project/ledger/SEG-0000/L-0000001` | The genesis entry, not yet written |
| `.ai/project/ledger/HEAD` | Would record `entry_hash` and transition `genesis → active` |
| `core/schemas/SCH-ledger-entry.schema.json` | Requires `entry_hash` and `prev_hash`; defines neither |

## 3 · Evidence

Repository-wide search for `entry_hash`, `prev_hash` and *chain hash* across `framework/`, `.ai/core/` and `.ai/BOOT.md` returns only **requirements**, never a **construction**:

| Source | States | Declares construction |
|---|---|---|
| `AIEF-FRZ-001` §1.2 | "Every entry carries `prev_hash` of its predecessor" | no |
| `AIEF-FRZ-001` §1.4 | "confirm the entry it names exists and hashes to `HEAD.entry_hash`" | no |
| `SCH-ledger-entry.schema.json` | `entry_hash`, `prev_hash` required; description is "Required field of sch-ledger-entry" | no |
| `BOOT.md` B4 | "verify named entry exists and hashes" | no |

Unspecified and each independently outcome-changing: which fields are covered, their serialisation and ordering, whether `entry_hash` excludes itself, the normalisation rule, and whether `prev_hash` is an input to its successor's digest.

`FROZEN.md` declares a normalisation rule for its own per-artifact hashes; **the ledger declares nothing equivalent.**

## 4 · Impact

### 4.1 Blocks the LAW-09 session close

`LAW-09` fixes the close order: *entry file → flush → `HEAD` → `STATE.md` → release lock.* The first step cannot be performed without the construction.

### 4.2 The choice would be irreversible

Per `AIEF-AMD-003` §AMD-10, the first session close transitions `genesis → active`, "occurs once per repository and is **irreversible**." Any construction adopted to write `L-0000001` would seed the chain permanently and bind every subsequent entry. An invented construction is therefore worse here than in ECR-Q-001: it cannot be corrected by re-registration.

### 4.3 Current position is consistent, not corrupt

The ledger remains at genesis. `STATE.last_ledger_seq` (0) equals `HEAD.seq` (0), so **boot step B4 continues to pass**:

| B4 check | Status |
|---|---|
| 1 · Named entry exists and hashes | vacuous at genesis — AMD-003 §AMD-10 |
| 2 · No orphan at `HEAD.seq + 1` | passes — no file at seq 1 |
| 3 · `STATE.last_ledger_seq` == `HEAD.seq` | passes — 0 == 0 |

The work of this session is recorded in `STATE.md`, `OPEN_ITEMS.md`, `FROZEN.md`, two ECRs and one approval. **It is not lost — it is unlogged.** The audit trail is weaker than the framework intends, which is the substance of this ECR.

## 5 · Requested action

Ruling by `chief-systems-engineer` (A4). Declare the construction explicitly, in `SCH-ledger-entry.schema.json` or a ledger specification, covering at minimum:

| Element | Must state |
|---|---|
| Covered fields | Which fields enter the digest, and in what order |
| Serialisation | Canonical form of the entry before hashing |
| Self-exclusion | That `entry_hash` is excluded from its own preimage |
| Normalisation | Encoding and line-ending rule — `FROZEN.md`'s rule is the obvious precedent |
| Chain rule | Whether `prev_hash` is an input to the successor digest |
| Genesis | The `prev_hash` value at seq 1 — `null` per current `HEAD` |

Suggested, consistent with the per-artifact rule already in force: **SHA-256 over the canonical YAML serialisation of the entry with `entry_hash` omitted, UTF-8, LF, trailing whitespace stripped, terminal newline enforced, `prev_hash` included as a field.**

**Recommend resolving jointly with ECR-Q-001.** Both are the same root cause — a hash is required, verified and depended upon, but its construction is never declared. A single amendment should declare every digest construction the framework relies on.

## 6 · Disposition

> ### A — DECLARE THE CONSTRUCTION EXPLICITLY. **CLOSED.**

| | |
|---|---|
| Disposition | **A**, and substantially the construction suggested in §5. Declared normatively in `framework.manifest.json` → `metadata.reproducible.digest_constructions.ledger_entry_hash`, designated **DC-3** |
| Ruled by | `chief-systems-engineer` · `S-2026-08-08-02` |
| Raised by | `role-unrecorded` · `S-2026-08-08-01` |
| Instrument | [`AIEF-AMD-008`](../../../framework/AIEF-AMD-008_Digest_Constructions_and_QA-001_Dispositions.md) §AMD-17 |
| Approval artifact | [`approvals/APR-002`](../approvals/APR-002_Amend_Framework_Manifest_AMD-008.md) |
| Date | 2026-08-08 |

Resolved **jointly with ECR-Q-001**, as §5 recommended. One amendment declares every digest construction the framework relies on: DC-1 per artifact, DC-2 set aggregate, DC-3 ledger chain.

### Departure from the §5 suggestion, stated

§5 suggested *"SHA-256 over the canonical YAML serialisation of the entry."* **YAML was rejected as the serialisation.** YAML admits several byte-identical-meaning renderings of the same document — quoting style, flow versus block sequences, key order, comments, anchors — so *"canonical YAML"* would require a canonicalisation specification that does not exist here. DC-3 instead defines its own flat line-oriented preimage, which is unambiguous in one paragraph. The substance of the suggestion — self-exclusion, `prev_hash` included, `FROZEN.md`-consistent normalisation — is adopted in full.

### The six elements §5 required, each answered

| Element | Ruling |
|---|---|
| Covered fields | `schemas[sch-ledger-entry].required_fields` **minus `entry_hash`**: `seq`, `timestamp`, `session_id`, `actor`, `action`, `artifacts`, `prev_hash` — seven fields, in that declared order |
| Serialisation | One record per field, `<field-name>` `<SP>` `<value>` `<LF>`, concatenated. Per-field canonical value forms specified for all seven. Digest domain is the canonical preimage, **never the file's on-disk octets** |
| Self-exclusion | `entry_hash` is excluded from its own preimage. Fields outside the declared seven are also excluded, and are therefore **not protected by the chain** — stated as a consequence, not hidden |
| Normalisation | UTF-8, no BOM. Values carry no `LF`, no `CR`, no leading or trailing space; a violation is rejected as a BLOCKING schema error and **never silently normalised**, because silent normalisation would make two different entries hash alike |
| Chain rule | **`prev_hash` is a covered field and is therefore an input to the successor digest.** Altering entry *n* changes `entry_hash(n)` = `prev_hash(n+1)` and every digest after it. This is what makes the ledger tamper-evident |
| Genesis | `L-0000001` carries `prev_hash` as the literal token `null`; `HEAD` at genesis keeps `seq: 0`, `entry_hash: null`, `prev_hash: null`, unchanged from AIEF-AMD-003 §AMD-10 |

Two worked examples with fixed synthetic inputs and their exact digests are published in AMD-008 §AMD-17, so a third party can validate an implementation without repository access.

### Not applied — deliberately

> **No ledger entry was written. `HEAD` remains at `genesis`.**

§4.2 is right that the choice is irreversible, and that reasoning does not stop at the moment of definition. The session that *defines* a construction is not the right session to *seed* the chain with it: seeding is an operational act that belongs to a session performing a full LAW-09 close, with a lock, an actor and a real action to record. DC-3 is now available; the transition is not made here.

### Effect on held work

| Held item | Status |
|---|---|
| The construction | **Released** — DC-3 is declared |
| The LAW-09 close of `S-2026-08-08-01` | **Cannot be released.** That session ended; a later session cannot close it. Its work is recorded in files and remains permanently unlogged. Recorded as **OI-P-01** |
| `genesis → active` transition | **Not performed.** Available to the next session that performs a full close |

---

## Authority chain

| | |
|---|---|
| LAW-02 | Ambiguity is raised as ECR-Q; only the chief-systems-engineer rules on ECR-Q; no ECR is closed by the agent that raised it |
| LAW-09 | Session close order; the ledger is authoritative and STATE is a derived cache |
| LAW-12 | Assumption is never a resolution method |
| LAW-01 / LAW-10 | The manifest is frozen; the change carries `APR-002` |
| AIEF-AMD-003 §AMD-10 | Ledger genesis semantics; the transition is irreversible and is **not** performed here |
| `core/PRECEDENCE.md` rank 1 | Live human-owner instruction authorising the amendment |
| `core/PRECEDENCE.md` rank 7 | AI inference overrides nothing; raising an ECR is its only path |
| AIEF-AMD-008 §AMD-17, §AMD-20 | The ruling, and the identity definition under which it is admissible |
