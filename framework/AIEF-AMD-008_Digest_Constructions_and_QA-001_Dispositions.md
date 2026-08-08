# AIEF-AMD-008 — Architecture Amendment: Digest Constructions and QA-001 Dispositions

**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-02 (ECR-Q disposition), LAW-01 + LAW-10 (frozen artifact change)
**Scope:** ECR-Q-001, ECR-Q-002, and findings FIND-1, FIND-2, FIND-4, FIND-7 of the independent verification report filed at `project/verification/VER-001`
**Date:** 2026-08-08 · **Session:** `S-2026-08-08-02`
**Amends:** `framework/framework.manifest.json`
**Does not amend:** `AIEF-FRZ-001` · `AIEF-AMD-001` … `AIEF-AMD-007` · `SCH-framework-manifest.schema.json` · any law rule or clause · any role contract · any partition, layer or stage definition
**Authorising basis:** live human-owner instruction (`core/PRECEDENCE.md` rank 1), recorded per LAW-10 in `project/approvals/APR-002` and `project/approvals/APR-003`

**Supersedes nothing.** Seven rulings, AMD-16 through AMD-22.

---

## Reading order

AMD-16 and AMD-17 are prerequisites. Until a digest construction exists, no aggregate is computable and no chain is writable; every other ruling that touches a hash depends on them.

| Ruling | Closes | Change class |
|---|---|---|
| AMD-16 | ECR-Q-001 | Additive — new normative content in `metadata.reproducible` |
| AMD-17 | ECR-Q-002 | Additive — new normative content in `metadata.reproducible` |
| AMD-18 | FIND-1 | Metadata correction — six `depends_on` edges, one `references` edge, four `referenced_by` entries, one `generation_order` output |
| AMD-19 | FIND-1, FIND-2, OI-V-02, ECR-Q-001 §5 | Additive — three check declarations, V-23 · V-24 · V-25 |
| AMD-20 | FIND-7 | Clarifying ruling + one `validation` text extension |
| AMD-21 | FIND-4 | Authority ruling — freeze registry scope. No manifest change |
| AMD-22 | FIND-2 | Authority ruling — `binding` integrity class. **No change**, with reasons |

---

## AMD-16 — Freeze-Set Aggregate Construction (DC-2)

**Disposes:** ECR-Q-001 · **Disposition: A — declare the construction explicitly and recompute from it**
**Ruled by:** `chief-systems-engineer` · `S-2026-08-08-02`, which did not raise ECR-Q-001

### Finding, restated

`project/FROZEN.md` declares a normalisation rule for **per-artifact** digests and records an **aggregate** value under a bare heading with no method. No construction is declared anywhere in the framework: every other use of "aggregate digest" refers to `core/MANIFEST.lock`, a different set and a different artifact. A hash was required, verified against, and depended upon, but never constructed.

### Ruling — what is *not* being done

> **The recorded value `42bce7b0de019f854f99387edfc901b054b540f829bfe365e003be96892d5847` is not recovered, and no attempt is made to recover it.**

Thirteen candidate constructions were tested against it and all thirteen failed. Selecting a construction that reproduces it would be reverse-engineering a number of unknown provenance and would encode whatever accident produced it into the framework permanently. This amendment defines the construction **going forward**. The old value is marked **superseded and not reproducible**, retained at full length in `FROZEN.md` for audit only, and is never again used as a comparison basis.

### Ruling — DC-1, restated unchanged

The per-artifact rule already in force is renamed **DC-1** for citation. It is not modified.

> **DC-1.** SHA-256 over normalised content. Normalisation: decode UTF-8, stripping a byte-order mark if present; convert `CRLF` and lone `CR` to `LF`; strip trailing whitespace from every line; remove trailing blank lines; append exactly one terminal `LF`; encode UTF-8. Output 64 lowercase hexadecimal characters.

Sources: `metadata.reproducible.normalisation`, `AIEF-FRZ-001` §1.7 (OD-2), `project/FROZEN.md` line 8. DC-1 reproduces every registered digest, which is why the aggregate — and only the aggregate — was the defect.

### Ruling — DC-2, the aggregate

> **DC-2.** SHA-256 over the concatenation of one record per registry entry, each record `<path>` `<SP>` `<digest>` `<LF>`, sorted ascending by the UTF-8 byte sequence of `<path>`.

| Element | Definition |
|---|---|
| Algorithm | SHA-256 |
| Covers | Every entry of `project/FROZEN.md` § *Registered artifacts*, as the ordered pair (registered path, DC-1 digest). **Nothing else** — not file contents, not `FROZEN.md` itself, not registry prose, not the registration history |
| Record | `<path>` `<SP>` `<digest>` `<LF>`. `<path>` is the repository-relative POSIX path exactly as registered. `<SP>` is one U+0020. `<digest>` is 64 lowercase hexadecimal characters. `<LF>` is one U+000A |
| Field ordering | Within a record: path, then digest. Fixed |
| Record ordering | Ascending by the UTF-8 octet sequence of `<path>`, compared as unsigned octets, shorter prefix first. **The order of rows in the registry table is not used** and carries no meaning |
| Preimage | The records concatenated in that order. No header, no trailer, no separator beyond each record's own terminal `LF`, no byte-order mark |
| Encoding | UTF-8 throughout |
| Self-exclusion | The aggregate is **not** part of its own preimage |
| Output | 64 lowercase hexadecimal characters, recorded **in full** in `FROZEN.md` § *Aggregate* and in `STATE.frozen_set_hash`. **Truncation is prohibited** |
| Empty registry | SHA-256 of the empty octet string: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Duplicate path | A path registered twice is a registry defect. DC-2 is undefined for it and the V-24 check fails |

### Worked example — synthetic, fixed, publishable

Two entries, chosen so a third party can verify an implementation without repository access:

```
path  a/alpha.md   digest 0000000000000000000000000000000000000000000000000000000000000000
path  b/beta.md    digest 1111111111111111111111111111111111111111111111111111111111111111
```

Preimage, 151 octets — 76 for the first record, 75 for the second:

```
a/alpha.md 0000000000000000000000000000000000000000000000000000000000000000
b/beta.md 1111111111111111111111111111111111111111111111111111111111111111
```

DC-2 digest:

```
8de12581a7d3aef29454fcdfd696a71e4d5c1a0352f69c7a6b03b167d0f5f1b3
```

Any implementation that does not produce exactly this value for exactly this input is non-conforming.

### Why the aggregate value is not stated in this amendment

This document is itself a member of the freeze registry under AMD-21. An aggregate printed here would cover this document's own digest, which would change on printing it. **The live aggregate is recorded in the registry and in `STATE.md`, never in a registered artifact.** That is a property of the design, not an omission.

### Rejected alternatives

| # | Alternative | Why rejected |
|---|---|---|
| B | Adopt whatever construction Stage 6 uses for `MANIFEST.lock` | Stage 6 is blocked by CMP-BLOCK-004 and does not exist. Adopting a construction that has not been written defers resolution indefinitely and is not a ruling |
| C | Remove the aggregate; rely on per-artifact digests | `sch-state` declares `frozen_set_hash` required at severity BLOCKING. Removing it is a wider amendment than the defect warrants, and a set digest is genuinely useful: it detects addition and removal of registry members, which per-artifact digests cannot |
| — | Reverse-engineer the superseded value | Encodes an unknown accident into the framework. Explicitly refused above |

### Manifest change

`metadata.reproducible.digest_constructions.frozen_set_aggregate` — new object carrying the normative definition. `metadata.reproducible` does not constrain additional properties in `SCH-framework-manifest`, so **no schema amendment is required.**

---

## AMD-17 — Ledger Entry-Hash Chain Construction (DC-3)

**Disposes:** ECR-Q-002 · **Disposition: A — declare the construction explicitly**
**Ruled by:** `chief-systems-engineer` · `S-2026-08-08-02`, which did not raise ECR-Q-002

### Finding, restated

`SCH-ledger-entry` requires `entry_hash` and `prev_hash`. `AIEF-FRZ-001` §1.2 requires a chain. `BOOT.md` B4 verifies that the named entry "hashes to `HEAD.entry_hash`". None of them says how. Five properties were each independently outcome-changing and each undeclared: covered fields, serialisation, ordering, self-exclusion, and whether `prev_hash` feeds the successor digest.

The choice is **irreversible** — the first close seeds the chain permanently — which is why ECR-Q-002 correctly refused to invent one.

### Ruling — DC-3

> **DC-3.** SHA-256 over the concatenation of one record per covered field, each record `<field-name>` `<SP>` `<value>` `<LF>`, in the field order declared by `schemas[sch-ledger-entry].required_fields` with `entry_hash` omitted.

| Element | Definition |
|---|---|
| Algorithm | SHA-256 |
| Covered fields | Exactly `schemas[sch-ledger-entry].required_fields` **minus `entry_hash`**: `seq`, `timestamp`, `session_id`, `actor`, `action`, `artifacts`, `prev_hash` — seven fields |
| Field order | The declared order of `required_fields`, `entry_hash` omitted. **Not alphabetical. Not file order.** The manifest is the source of the order |
| Self-exclusion | `entry_hash` is excluded from its own preimage |
| Undeclared fields | **Excluded** from the preimage. A digest that varied with content not declared in the manifest would not be reproducible from the manifest alone. Consequence, stated plainly: any field an entry carries beyond the declared seven is **not protected by the chain** |
| Record | `<field-name>` `<SP>` `<value>` `<LF>`. `<SP>` is one U+0020, `<LF>` is one U+000A |
| Encoding | UTF-8, no byte-order mark |
| Preimage | The seven records concatenated in declared order. No header, no trailer, no separator beyond each record's terminal `LF` |
| Digest domain | The canonical preimage above — **never the entry file's on-disk octets**. File layout, key order, comments and whitespace do not affect the digest, exactly as DC-1 decouples a file digest from its line endings |
| Output | 64 lowercase hexadecimal characters |

#### Value serialisation

| Field | Canonical value form |
|---|---|
| `seq` | Decimal integer. No sign, no leading zeros, no digit separators. The filename `L-0000007` is zero-padded; the **value** is `7` |
| `timestamp` | `YYYY-MM-DDTHH:MM:SSZ`. UTC only, second precision, literal `T` and `Z`. No fractional seconds, no numeric offset form |
| `session_id` | As recorded, e.g. `S-2026-08-08-02` |
| `actor` | The **role token only**, per AMD-20: a `roleId` registered in `core/agents/INDEX.md`, or the reserved token `boot` or `role-unrecorded`. The session is carried by `session_id` and is **never duplicated** here |
| `action` | The recorded string, single line |
| `artifacts` | Repository-relative POSIX paths, sorted ascending by UTF-8 octets, joined by one `,` (U+002C) with **no** surrounding space. The empty list serialises to the **empty string** |
| `prev_hash` | 64 lowercase hexadecimal characters, or the literal four-character token `null` |

**Value constraints.** A value contains no `LF`, no `CR`, and no leading or trailing U+0020. A value violating this is a BLOCKING schema error and is rejected — it is **not** silently normalised, because silent normalisation would make two different entries hash alike.

**Empty `artifacts`.** The record is exactly eleven octets: `artifacts`, U+0020, U+000A. The space is significant and must not be stripped by an implementation.

#### Chain rule

> **`prev_hash` is one of the seven covered fields, therefore it *is* an input to the successor's digest.**

Altering entry *n* changes `entry_hash(n)`, which is `prev_hash(n+1)`, which changes `entry_hash(n+1)`, and so on to the head. This is what makes the ledger tamper-evident rather than merely sequential. A construction that excluded `prev_hash` would give a list of independent digests with a decorative chain field, which is not what `AIEF-FRZ-001` §1.2 requires.

#### Genesis values

| Position | Value |
|---|---|
| `HEAD` while `state: genesis` | `seq: 0`, `entry_hash: null`, `prev_hash: null` — unchanged from AIEF-AMD-003 §AMD-10 |
| First entry `L-0000001` | `prev_hash` is the literal token `null`; `seq` is `1` |
| `HEAD` after the first close | `state: active`, `seq: 1`, `entry_hash` = DC-3 of `L-0000001`, `prev_hash: null` |

`HEAD.entry_hash` is always the DC-3 digest of the entry at `HEAD.seq`; `HEAD.prev_hash` is always that entry's `prev_hash`. Boot step B4 check 1 recomputes DC-3 over the named entry and compares.

### Worked example — synthetic, fixed, publishable

Entry at sequence 1. Preimage:

```
seq 1
timestamp 2026-01-01T00:00:00Z
session_id S-2026-01-01-01
actor chief-systems-engineer
action example
artifacts a/alpha.md,b/beta.md
prev_hash null
```

DC-3 digest:

```
cb8e79720632c4f3bb0050a181ae0bffe2189f629b7fb7bfb1e3d8457d8259e0
```

Successor at sequence 2, empty `artifacts`, chaining on the value above. Preimage — note the significant trailing space on the `artifacts` line:

```
seq 2
timestamp 2026-01-01T00:00:00Z
session_id S-2026-01-01-01
actor chief-systems-engineer
action example-successor
artifacts 
prev_hash cb8e79720632c4f3bb0050a181ae0bffe2189f629b7fb7bfb1e3d8457d8259e0
```

DC-3 digest:

```
66e51617abb575133fa7bea5ace6b220f9d8feb4e3911a3d81cd158718f8195b
```

Any implementation that does not produce exactly these two values for exactly these two inputs is non-conforming.

### Not applied

**No ledger entry is written by this amendment.** `L-0000001` is not created and `HEAD` remains at `genesis`. DC-3 is *defined*; the `genesis → active` transition is irreversible and belongs to a session that performs a full LAW-09 close, not to the session that defines the construction.

### Manifest change

`metadata.reproducible.digest_constructions.ledger_entry_hash` — new object carrying the normative definition. No schema amendment required, for the reason given in AMD-16.

### Residual, recorded

`SCH-ledger-entry.schema.json` declares `additionalProperties: true`. Combined with the exclusion rule above, an entry may carry unprotected fields. Tightening it to `false` would remove the exposure entirely and is a Stage 1 re-emission. **Deferred and recorded as OI-C-01** — not silently accepted.

---

## AMD-18 — Dependency Edge Correction: Stage Monotonicity

**Closes:** FIND-1 · **Change class:** metadata correction

### Defect

Six `files[].depends_on` edges name a target emitted at a **later** compiler stage than the source:

```
wf-02     (stage 1) depends_on tpl-task-package    (stage 2)
prof-mech (stage 1) depends_on binding             (stage 3)
prof-soft (stage 1) depends_on binding             (stage 3)
prof-res  (stage 1) depends_on binding             (stage 3)
binding   (stage 3) depends_on manifest-lock       (stage 6)
adp-ci    (stage 4) depends_on validation-manifest (stage 5)
```

Independently reproduced by this authority over all 106 `files[]` entries: **six, exactly the six reported.** `AIEF-AMD-002` §AMD-07 rules that `depends_on` means *the target must exist before the source is emitted*. No execution of the declared `generation_order` satisfies any of the six. **V-02 cannot see them** — it tests acyclicity, and all six are acyclic.

This is the CMP-BLOCK-014 defect class recurring: a citation or runtime relation encoded as a build-order edge. AMD-07 was written to prevent recurrence and did not, because it declared the *semantics* without declaring a *check*.

### Ruling — each edge judged on its merits

The two admissible answers are *the edge is right and `generation_order` is wrong*, or *the edge is wrong*. They do not all get the same answer by default; each was tested against what the source artifact actually needs at emission time.

| # | Edge | Test applied | Judgement |
|---|---|---|---|
| 1 | `wf-02 → tpl-task-package` | `wf-02` renders from `content_ref: runtime_sequence`. The emitted `WF-02_task.md` contains phases 3 and 4 and does not reproduce any content of the task-package template. Phase 4's entry condition is *"task package read"* — a condition on the **agent at runtime**, not on the compiler at emission | **Edge is wrong.** Citation, not build order |
| 2 | `prof-mech → binding` | `prof-mech` renders from `content_ref: profiles`. Stage 1 inputs are `metadata, version, layers, partitions, profiles, files, boot_sequence, agents, laws` — `binding` is not among them. Profile *selection* is a compiler input (`AIEF-FRZ-001` Part 4, Stage 1: *"manifest + profile selection"*); `BINDING.active_profile` **records** the selection afterwards, at Stage 3. The emitted `PROFILE.md` does not cite `BINDING.md` at all | **Edge is wrong.** Reference, not build order |
| 3 | `prof-soft → binding` | As #2 | **Edge is wrong** |
| 4 | `prof-res → binding` | As #2 | **Edge is wrong** |
| 5 | `binding → manifest-lock` | `binding` is emitted at Stage 3 with `core_digest_pin: PENDING-STAGE-6`. It emits successfully **without** `manifest-lock`, which is proof the dependency is not an emission dependency. The true relation runs the other way in time: `AIEF-FRZ-001` Part 4 Stage 6 process includes *"Write the `BINDING` integrity pin"* — Stage 6 **fills a field in an already-emitted artifact** | **Edge is wrong, and `generation_order` is incomplete.** Both corrected |
| 6 | `adp-ci → validation-manifest` | Stage 4 inputs are `layers, version` only. The emitted `ADP-ci.md` states its own handling of absence: *"Emitted by Compiler Stage 5, not yet present. Until Stage 5 runs, CI enforcement is unavailable."* An artifact that documents its behaviour when the target is missing cannot require the target to exist before it is emitted | **Edge is wrong.** Runtime read, not build order |

**All six are miscodings. `generation_order` is not wrong about stage sequence** — it is incomplete about one Stage 6 output, corrected below.

### Corrections

| Artifact | Field | Before | After |
|---|---|---|---|
| `wf-02` | `depends_on` | `["LAW-11", "tpl-task-package"]` | `["LAW-11"]` |
| `prof-mech` | `depends_on` | `["binding"]` | `[]` |
| `prof-soft` | `depends_on` | `["binding"]` | `[]` |
| `prof-res` | `depends_on` | `["binding"]` | `[]` |
| `binding` | `depends_on` | `["sch-binding", "version-file", "manifest-lock"]` | `["sch-binding", "version-file"]` |
| `adp-ci` | `depends_on` | `["adapters-index", "validation-manifest"]` | `["adapters-index"]` |

### Semantic preservation — no relationship is lost

Following the `AIEF-AMD-002` §AMD-06 precedent exactly: build order and citation are different relations, and removing one must not remove the other.

| Relation | Already present as | Action |
|---|---|---|
| `prof-mech` ↔ `binding` | `references` edge | **unchanged** — already in `dependencies.edges` |
| `prof-soft` ↔ `binding` | `references` edge | **unchanged** |
| `prof-res` ↔ `binding` | `references` edge | **unchanged** |
| `binding` ↔ `manifest-lock` | `validates` edge | **unchanged** — AMD-07 rules `validates` non-build-order |
| `adp-ci` ↔ `validation-manifest` | `reads` edge | **unchanged** — AMD-07 rules `reads` non-build-order |
| `wf-02` ↔ `tpl-task-package` | **nothing** | **`references` edge added** — `{ "from": "wf-02", "to": "tpl-task-package", "type": "references" }` |

Five of the six removed edges were **duplicates of a typed edge that AMD-07 had already declared non-build-order.** The manifest was carrying the same relation twice, once correctly and once as a build constraint. Only edge 1 needed a new edge.

`referenced_by`, which records *"file ids that cite it"*, gains the citers it was missing:

| Artifact | `referenced_by` before | after |
|---|---|---|
| `binding` | `["boot"]` | `["boot", "prof-mech", "prof-soft", "prof-res"]` |

`tpl-task-package.referenced_by` already contained `wf-02`; `manifest-lock.referenced_by` already contained `binding`; `validation-manifest.referenced_by` already contained `adp-ci`. No change to any of them.

### `generation_order` correction

Stage 6 writes the binding integrity pin (`AIEF-FRZ-001` Part 4, Stage 6) but does not declare it as an output. That omission is what made edge 5 look like a build dependency. Corrected:

```
generation_order[stage 6].outputs  +=  "project/BINDING.md core_digest_pin (integrity pin write)"
```

This is a field write into an already-emitted instance artifact. It is **not** a re-emission of the `project` partition and does not touch the Stage 3 barrier.

### Post-correction state

Executed against the amended manifest before this document was hashed.

| Assertion | Result |
|---|---|
| Backward `depends_on` edges | **0** — was 6 |
| `depends_on` edges total | 125 — was 131; six removed, none added |
| Every `depends_on` target resolves | 125 of 125 |
| V-02 build-order graph acyclic | **PASS** — 125 build edges, 0 cycles |
| V-02 topological sort | **PASS** — 106 nodes |
| `references` edges | 21 — was 20 |
| V-01 conformance to `SCH-framework-manifest` | **PASS** — validated with a JSON Schema 2020-12 validator against the unmodified frozen schema |
| MI-1 unique file ids | **PASS** — 106, 0 duplicates |

**MI-3 carries one pre-existing condition, unchanged by this amendment.** `boot.referenced_by` contains `framework` and `sch-state.referenced_by` contains `V-06`; neither is a `files[]` id. Both are present identically at commit `6ce3508` and neither was introduced here. Reported as FIND-9. Under a strict reading — *`referenced_by` ranges over `files[]` ids only* — this fails MI-3 and therefore V-01; under a wider reading it is a namespace mix and MI-3 holds. **This authority does not rule on it: it was not within the directed scope, and resolving it would change the manifest a second time without a directed basis.** Recorded as **OI-C-03**, and flagged as a strict-reading obstacle to any Stage 1 re-emission or V-01 execution.

---

## AMD-19 — Stage 5 Check Requirements: V-23, V-24, V-25

**Closes:** the recurrence path of FIND-1; discharges ECR-Q-001 §5 (*"bind a standing verification check"*); gives OI-V-02 a home
**Change class:** additive — three declarations in `manifest.validation`

AMD-07 ruled the semantics and the defect recurred anyway. A ruling without a check is a convention; only a check is a control. Three checks are declared. **None is implemented here — Compiler Stage 5 is not executed by this amendment.**

### V-23 — Stage monotonicity

> For every `files[]` entry *S* and every id *T* in `S.depends_on`: `generator(T) ≤ generator(S)`, and *T* exists. Where `generator(T) = generator(S)`, the intra-stage emission order is a topological order of the same-stage `depends_on` subgraph.

Distinct from V-02, which tests acyclicity. **A backward edge is acyclic**, which is precisely why V-02 passed on all six defects. Severity BLOCKING, phase compile-time.

### V-24 — Freeze registry

> Every path registered in `project/FROZEN.md` exists in the working tree and its DC-1 digest equals the registered digest. The DC-2 aggregate recomputed over the registry equals the value in `FROZEN.md` § *Aggregate* and the value in `STATE.frozen_set_hash`, both recorded at full 64-character length. Every artifact meeting the AMD-21 registration criterion is registered. No path is registered twice.

This is the check whose absence let ECR-D-005 persist across three releases, and the check ECR-Q-001 §5 required as a condition of any disposition. Severity BLOCKING, phase compile-time, `law_ref: LAW-01`.

Compile-time, not installation: the ECR-D-005 scenario is a build consuming a frozen input that does not verify. The check must run before that, not after release.

### V-25 — Encoding conformance

> Every text artifact under `.ai/` and every artifact registered in `project/FROZEN.md` decodes as UTF-8 without error, carries no byte-order mark, uses `LF` line endings exclusively, ends with exactly one terminal `LF`, and contains no **mojibake sequence** outside quoted evidence.
>
> **Mojibake sequence**, normatively: a maximal run of non-ASCII characters that, re-encoded as CP1252 and decoded as UTF-8, both succeed and yield a strictly shorter string. Such a run is a double-encoding artifact and is a defect.
>
> **Quoted-evidence exclusion:** such a sequence occurring inside a Markdown code span or fenced code block is quoted evidence and is **not** a violation.

Severity BLOCKING, phase compile-time. The definition is a decision procedure, not a blocklist: it requires no table of known-bad sequences and cannot be evaded by an unlisted one.

**The exclusion was added after the first draft failed.** V-25 as first written flagged `project/verification/VER-001` — because FIND-2 quotes the corrupt sequences as evidence, inside code spans. A check that convicts a report for citing the defect it found is a check that punishes correct behaviour, which is the FM-3 failure mode named in `AIEF-FRZ-001` §1.7. V-22 already carries exactly this narrowing for prohibition text; V-25 now carries it for quoted bytes. **Recorded rather than quietly patched**, because a check specification that needed correcting on first execution is itself evidence about how easily this class of defect is written.

### Out of V-25's declared scope, recorded

Nine `implementation/**/README.md` files carry a UTF-8 byte-order mark. They lie outside `.ai/` and are not registered, so V-25 as scoped does not reach them, and they are **not** repaired here — `implementation/` is PR-controlled, not A4-controlled. Recorded as **OI-C-04** so the observation is not lost.

### Not bound into any law record

None of the three is added to a law's `checks` array. `V-23` and `V-25` carry `law_ref: null`, consistent with the nine existing structural checks that do; `V-24` carries `law_ref: LAW-01` as a one-way reference, which satisfies MI-5 (*every law referenced by a check exists*) without altering LAW-01's record. **No emitted law artifact is made stale by this ruling.**

---

## AMD-20 — Actor-Provenance Representation

**Closes:** FIND-7 · **Change class:** clarifying ruling plus one `validation` text extension

### The reported collision

| Requirement | Text | Severity |
|---|---|---|
| LAW-07 clause 1 | *"No AI attribution in any commit, tag, file or document."* | BLOCKING |
| `SCH-ecr.required_fields` | `raised_by` is required | BLOCKING |

The three open ECRs carry `raised_by: claude-code session S-2026-08-08-01`. They are untracked today, so nothing is yet violated; committing them writes that string into tracked artifacts, and the `repository-engineer` would then be choosing between two BLOCKING requirements.

### Ruling — there was never a collision

> **`tpl-ecr` already declares the field's grammar: `raised_by: role, identity, session`. The value `claude-code session S-2026-08-08-01` conforms to neither that grammar nor LAW-07. The collision is an artifact of a non-conforming value, not of two requirements in conflict.**

`claude-code` is not a role. It is the value of `BINDING.host_adapter` — an execution-environment configuration fact — placed in an actor field. No requirement ever asked for it.

### What each requirement actually demands

| | Demands | Does **not** demand |
|---|---|---|
| **LAW-07 cl. 1** — read with its own rule (*"Author identity is never modified…"*) and its bound check V-22 (*"no AI **authorship claim** appears in any tracked artifact"*) | That no AI system be credited as author or co-author of repository content | That the repository be silent about which actor performed an action. Authorship and agency are different claims |
| **Auditability** — LAW-04, LAW-05, LAW-09, `tpl-ecr` condition 3, `sch-ledger-entry.actor` | That the **accountable framework actor** and the **session** be recorded, so that reviewer independence (*ruled-by ≠ raised-by*) is machine-checkable | A model name, a vendor, a product, or a host adapter. None of those is an accountable actor: none appears in `core/agents/INDEX.md`, none can hold a role, none can be assigned a duty |

A framework **role** plus a **session id** satisfies both, and satisfies auditability *better* than a product name does — because a role resolves against the agent registry, and `project/ROSTER.md` maps it to a canonical git identity (`AIEF-FRZ-001` §1.9, OD-8: *"Git identity is canonical"*). A product name resolves against nothing.

### Ruling — the authoritative representation

> **An actor-provenance field names a framework role and a session. It never names a model, a vendor, a product, or a host adapter.**

**Canonical form**

```
<actor> · <session-id>
```

| Element | Admissible values |
|---|---|
| `<actor>` | A `roleId` registered in `core/agents/INDEX.md`, including `human-owner`; **or** one of two reserved tokens |
| Reserved `boot` | The action was taken by the boot sequence before role assignment — steps B1–B8. Resolves to the declared framework mechanism `files[boot]` |
| Reserved `role-unrecorded` | No role assignment is recoverable from the repository for the acting session. Honest, and it makes the gap visible rather than inviting a plausible guess |
| `<session-id>` | `S-YYYY-MM-DD-nn` |
| `identity` | **Carried by reference, never duplicated.** `project/ROSTER.md` maps role to canonical git identity. Duplicating the identity string into every artifact would create a second source of truth that goes stale |

**Fields governed:** `raised_by` and *Ruled by* (`tpl-ecr`, `SCH-ecr`) · `approver` (`SCH-approval`, `tpl-design-review`) · *Reviewer* and *Originator* (`tpl-design-review`) · *Verifier* and *Producer* (`tpl-verification-report` §5) · *Role* (`tpl-session-summary`, `tpl-task-package`) · `actor` (`SCH-ledger-entry`, where the session is carried separately by `session_id` and the role token stands alone).

**Naming the host adapter remains lawful where it is configuration, not attribution.** `BINDING.host_adapter: claude-code`, `adapters/ADP-claude-code.md`, and prose describing the execution environment are configuration facts and are not authorship claims. The line is the field, not the string: a host adapter named in a configuration field is a fact; the same name in an actor field is an attribution.

### Ruling — agent identity for independence tests

`tpl-ecr` acceptance condition 3 and LAW-02 clause 5 require the disposing agent not to be the raising agent. That requires a definition of "agent".

> **Agent identity for LAW-02, LAW-04 and LAW-05 independence is the pair (role, session).**

`tpl-verification-report` §5 already requires *Context* — *"cold subagent · serial adoption"* — as part of the independence declaration, and states that **"independence is a property of the context, not of intent."** A cold session holds no inherited state from the session that produced the artifact and therefore cannot be defending its own work. The session is constitutive of the identity, and the framework already says so.

**Residual, recorded rather than glossed:** a same-role, different-session disposition is weaker than a cross-role one. Where the same role both raises and rules, the mitigating control is an independent cold-context QA audit of the ruling. This applies directly to the dispositions in AMD-16 and AMD-17 and is recorded as **OI-V-03**.

### Making it checkable — V-22 extension

`validation[V-22].verifies` is extended with:

> *"Every actor-provenance field in a tracked project artifact — `raised_by`, `ruled_by`, `approver`, `verifier`, `producer`, `reviewer`, `actor`, `role` — resolves to a role registered in `core/agents/INDEX.md` or to the reserved token `boot` or `role-unrecorded`, optionally followed by a session identifier of the form `S-YYYY-MM-DD-nn`. A model, vendor, product or host-adapter name appearing in such a field is a violation. A host adapter named in a declared configuration field or in prose describing configuration is not a violation."*

This is a resolvable-token test against a declared registry, not a substring blocklist. It preserves V-22's existing narrowing — *"prohibition text that names a forbidden pattern is not itself a violation"* — because it examines fields, not free text.

### Application to existing artifacts

| Artifact | `raised_by` before | after | Basis |
|---|---|---|---|
| `ECR-D-005` | `claude-code session S-2026-08-08-01 (pre-role, boot-time integrity check)` | `boot · S-2026-08-08-01` | The artifact's own §header records the raise at boot step B7/B8, pre-role |
| `ECR-Q-001` | `claude-code session S-2026-08-08-01` | `role-unrecorded · S-2026-08-08-01` | No role assignment for `S-2026-08-08-01` is recoverable: `project/sessions/` is empty and no session summary was filed. **Not guessed** — recorded as OI-P-01 |
| `ECR-Q-002` | `claude-code session S-2026-08-08-01` | `role-unrecorded · S-2026-08-08-01` | As above |
| `APR-001` | `approver: human-owner` | **unchanged** | Already conforms. `human-owner` is a registered `roleId` at authority level H. No AI attribution is present. **No correction is required and none is made** |

The explanatory prose in each ECR header is retained, so no information is lost — only the machine-read field changes.

---

## AMD-21 — Freeze Registry Scope

**Closes:** FIND-4 · **Change class:** authority ruling. **No manifest change**

### Finding, restated

`project/FROZEN.md` registers 5 of the **13** files `framework/` held at the time of the audit. Unregistered: `AIEF-AMD-003` … `AIEF-AMD-007`, `AIEF-ADR-001`, `AIEF-ADR-002`, `AIEF-ARCH-001`. Among them are **the three amendments that authorise the ECR-D-005 re-registration** — the evidence on which APR-001 rests was itself unguarded.

> **Correction to the source finding, recorded rather than absorbed silently:** FIND-4 states *"5 of 12"*. The directory held **13** files, not 12; `AIEF-ARCH-001` was omitted from the count. The finding's substance stands and its severity is unchanged; the arithmetic is corrected here and the omitted artifact is ruled on below rather than left unaddressed. This document brings the directory to **14**.

### Ruling — the criterion

> **An artifact is registered in the freeze registry if it is an authorising instrument for a change to a frozen artifact, or the record of the authority under which such a change was made.**

Reasoning, in order of authority:

1. **LAW-01 clause 1** — *"Every frozen artifact is registered with a normalised SHA-256 content hash."* The question is therefore which artifacts are frozen, not whether frozen ones are registered.
2. **The evidence chain must not have a soft link.** `APR-001` proves the manifest's divergence was authorised by citing AMD-004, AMD-006 and AMD-007. If those documents can change without detection, `APR-001` proves nothing — the defence is only as strong as the artifact it cites. ECR-D-005 is the empirical case: the guarded artifact drifted and the unguarded defence was what remained.
3. **`ENGINEERING.md` §4 is not the basis.** It declares the whole `framework/` partition FROZEN, but it states of itself that it *"holds no rule… Nothing here may be cited as a source."* It cannot found a freeze. It is corroborating, not authorising.

### Ruling — the scope declaration the registry was missing

The deeper defect is that `FROZEN.md` never declared **what set it covers**. A registry with undeclared scope cannot be under-inclusive in any detectable way. Declared now:

> **The freeze registry covers repository partitions outside `.ai/` that are declared frozen: `spec/` and `framework/`.** The `core/` partition is covered by `core/MANIFEST.lock` and boot step B2a, not by this registry. The `project/` partition is mutable by design and is not covered.

### Ruling — application, artifact by artifact

| Artifact | Class | Registered |
|---|---|---|
| `AIEF-FRZ-001` | Freeze document | **Yes** — already |
| `AIEF-AMD-001` … `AIEF-AMD-002` | Amendment — authorising instrument | **Yes** — already |
| `AIEF-AMD-003` … `AIEF-AMD-007` | Amendment — authorising instrument | **Yes — added** |
| `AIEF-AMD-008` (this document) | Amendment — authorising instrument | **Yes — added** |
| `AIEF-ADR-001`, `AIEF-ADR-002` | Authority Decision Record — the record of the A4 authority under which AMD-01…AMD-08 were made | **Yes — added.** LAW-06 requires the authority chain be traceable; a record of authority that can change silently is not a record |
| `framework.manifest.json`, `SCH-framework-manifest.schema.json` | Source of truth and its schema | **Yes** — already |
| `AIEF-ARCH-001` | **Superseded design specification.** `AIEF-FRZ-001` header: *"Supersedes: AIEF-ARCH-001 Rev A (architecture)"*. `AIEF-AMD-001` §AMD-04: *"AIEF-ARCH-001 §7.4 is superseded."* Its own header: *"Design only. No framework files are generated by this document."* | **No.** It authorises nothing and is cited by nothing as a live authority. Registering it would assert a currency it does not have. **Ruled explicitly so the omission is a decision, not an oversight** |
| `spec/**` (11 files) | Frozen engineering baseline | **Yes** — already |

**Result: 16 → 24 registered artifacts.** Eight additions: AMD-003, AMD-004, AMD-005, AMD-006, AMD-007, AMD-008, ADR-001, ADR-002.

### Approval discipline

Each addition is a freeze-registry change and carries the same discipline as any other: an approval artifact bound to the content hash. All eight are recorded in **`project/approvals/APR-003`**, which names each path with its DC-1 digest individually. A single instrument covering a set is admissible under LAW-10 — the law requires that an approval *name what it approved* and be *invalidated when the bound content changes*; APR-003 names all eight and is void if any one of the eight changes. It is not a blanket approval and it grants nothing beyond the enumerated paths at the enumerated digests.

---

## AMD-22 — `binding` Integrity Class

**Closes:** FIND-2 (the standing question, not the repair) · **Change class:** authority ruling. **No change**

### Question

`.ai/project/BINDING.md` carried two CP1252 double-encoding defects — a mangled em dash on line 4 and a mangled section sign on line 35. It is a **T1 boot-read artifact**, read at boot step B5. The corruption went undetected because `files[binding].integrity` is `unhashed`. Should a T1 boot-critical artifact remain `unhashed`?

### Ruling

> **`binding` remains `integrity: unhashed`. The manifest is not changed.**

Three reasons, each independently sufficient:

1. **A mutable artifact cannot be frozen.** `binding` is `mutability: mutable` and `lifecycle: instance-created`. Its values are *designed* to change: `core_digest_pin` is filled by Stage 6, `session_timeout` is project-overridable, `lifecycle_stage` and `active_gate` advance with the project. LAW-10 clause 2 invalidates an approval automatically when the bound hash changes. Hashing `binding` would void its own approval on every lawful edit — a control that fails on correct behaviour trains people to disable it, which is exactly the failure mode `AIEF-FRZ-001` §1.7 names as FM-3.
2. **It would contradict the partition contract.** The `project` partition declares *integrity verified: **no*** (`.ai/FRAMEWORK.md` § Partitions). Making one project file `hashed` creates a partition whose declared semantics are false for one member. MI-12 requires each partition to declare its semantics; a per-file exception silently unsays it.
3. **It would not have caught this defect.** A freeze hash detects *change*. The mojibake was present from the artifact's creation — it is not a divergence from a registered baseline, it is a **defective baseline**. Hashing it would have registered the corruption and then certified it as intact.

### What the exposure actually is, and its control

The gap is not integrity. It is that **no check asserts encoding conformance on any artifact**, and a corrupted T1 artifact is read at boot by every session. The control is **V-25** (AMD-19), declared as a Stage 5 requirement.

### Repair, performed separately

The two sequences were repaired byte-exactly in the same session, outside this amendment: `C3 A2 E2 82 AC E2 80 9D` → `E2 80 94` (U+2014 EM DASH), `C3 82 C2 A7` → `C2 A7` (U+00A7 SECTION SIGN). File length 1496 → 1489 octets. A round-trip test proved the two substitutions are the only differences. A repository-wide re-scan under the V-25 definition returns **zero** mojibake sequences in any file. Recorded in `project/verification/VER-001` § filing header and in the session record.

---

## Blast Radius

Determined by inspecting every artifact that renders a changed manifest section.

| Changed section | Rendered by | Effect |
|---|---|---|
| `metadata.reproducible.digest_constructions` | `.ai/FRAMEWORK.md` § Integrity renders DC-1 only, which is unchanged | **None** |
| `files[].depends_on`, `.referenced_by`, `dependencies.edges` | **Nothing.** No emitted artifact renders a dependency list — verified by search across `.ai/` | **None** |
| `generation_order[6].outputs` | No `files[]` entry carries `content_ref: generation_order` | **None** |
| `validation` — V-22 text, V-23, V-24, V-25 added | `core/validation/CHECKS.md` and `core/validation/MANIFEST` — **Stage 5, not emitted**. `core/laws/LAW-07_*.md` renders bound-check *ids* only, which are unchanged | **None in `core/`** |
| `validation` — count 22 → 25 | **`adapters/ADP-ci.md`** § Execution: *"All 22 checks are BLOCKING"*, and the phase ranges `V-01 .. V-10` / `V-18 .. V-21` | **STALE.** Requires a Stage 4 re-emission. Recorded as **OI-C-02** |

| Result | Count |
|---|---|
| Emitted artifacts inspected | 87 |
| **Unchanged** | **86** |
| **Stale, recorded** | **1** — `adapters/ADP-ci.md` |
| Edited by this amendment | **0** — no artifact under `.ai/core/**` or `.ai/adapters/**` is hand-edited |

**No law rule or clause, no role contract, no schema, no partition, layer, tier, boot step or compiler stage definition is modified.** The five universal roles and the thirteen laws are untouched.

---

## Separation of Duties — Recorded Tension

`core/agents/INDEX.md` § Separation of duties states: **`chief-systems-engineer`: may not implement what it approved.**

This amendment was authored, and the manifest change applied, by the same authority (`chief-systems-engineer` · `S-2026-08-08-02`) at the direction of the human owner, whose live instruction is `core/PRECEDENCE.md` rank 1 and outranks the rank-6 agent specification. **The direction is authorising; it does not make the tension disappear, and it is recorded here rather than left implicit.**

| | |
|---|---|
| Duty separated | A4 rules and approves; A1 implements |
| Departure | A4 both ruled and applied |
| Authority for the departure | Rank-1 live human instruction, recorded per LAW-10 in APR-002 and APR-003 |
| Mitigating control | Independent cold-context `qa-engineer` audit of this session's work — **OI-V-03**, open |
| Not mitigated by | Any statement in this document. Under LAW-05 an authority's assertion about its own work carries no evidentiary weight |

The same tension attaches to AMD-16 and AMD-17, where a `chief-systems-engineer` session disposes ECRs raised by an earlier session whose role is unrecorded. The identity ruling in AMD-20 makes the two sessions distinct agents; it does not make the disposition independently verified.

---

## Artifacts Not Modified

| Artifact | Status |
|---|---|
| `AIEF-FRZ-001` | Unmodified |
| `AIEF-AMD-001` … `AIEF-AMD-007` | Unmodified |
| `SCH-framework-manifest.schema.json` | **Unmodified — no schema amendment required.** Every addition lands in a subtree that does not constrain additional properties (`metadata.reproducible`), or in an array whose item schema already admits it (`validation`, `dependencies.edges`, `generation_order[].outputs`) |
| `AIEF-ARCH-001` | Unmodified; ruled superseded and unregistered (AMD-21) |
| All 13 laws, 5 universal roles, 4 profile roles, 6 workflows, 8 schemas, 10 templates | Unmodified |
| `core/**` | **Not touched.** Re-emission is a compiler action, blocked by CMP-BLOCK-004 |
| `core/validation/**`, `core/MANIFEST.lock` | **Not created.** Compiler Stages 5 and 6 are not executed by this amendment |
| `project/ledger/**` | **Not written.** `HEAD` remains at `genesis`; `L-0000001` does not exist |

## Approvals Required and Recorded

| Frozen artifact changed | Approval | Bound to |
|---|---|---|
| `framework/framework.manifest.json` | `project/approvals/APR-002` | its post-amendment DC-1 digest |
| Freeze registry membership, eight additions | `project/approvals/APR-003` | each added artifact's DC-1 digest |

Per LAW-01 and LAW-10, and per `core/PRECEDENCE.md` clause 4: *"a rank-1 override of rank 3 must be recorded as an approval artifact before dependent work is committed."*

---

**END OF AIEF-AMD-008**
