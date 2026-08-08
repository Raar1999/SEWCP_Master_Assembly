# AIEF-AMD-010 — Architecture Amendment: Stage 6 Constructions and Pre-Flight Dispositions

**Authority:** Chief Systems Engineer (A4) · **Instrument:** LAW-02 (specification-gap disposition), LAW-01 + LAW-10 (frozen artifact change), LAW-12 (open decision, never assumption)
**Scope:** The Stage 6 pre-flight specification gaps recorded in `project/STAGE-6_PREFLIGHT_CMP-BLOCK-004_005.md` (commit `dc811a6`): OPEN-QUESTIONS 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, and the authority analysis of OPEN-QUESTION 13. **Nothing else** — directed scope, live human-owner instruction of session `S-2026-08-08-04`. OPEN-QUESTION 11 is left open with an owner; OPEN-QUESTION 14 and the OPEN-QUESTION 13 choice are reserved to the human owner and are not ruled here.
**Date:** 2026-08-08 · **Session:** `S-2026-08-08-04`
**Amends:** `framework/framework.manifest.json`
**Does not amend:** `AIEF-FRZ-001` (three phrases superseded in reading, bytes untouched — see AMD-27, AMD-31, AMD-32) · `AIEF-AMD-001` … `AIEF-AMD-009` · either ADR · `SCH-framework-manifest.schema.json` · `SCH-core-manifest.schema.json` or any emitted schema · any law rule or clause · any role contract · any partition, layer, tier, boot step or stage definition · DC-1, DC-2 or DC-3, which are preserved exactly as declared
**Authorising basis:** live human-owner instruction (`core/PRECEDENCE.md` rank 1), recorded per LAW-10 in `project/approvals/APR-006` and `project/approvals/APR-007`

**Supersedes:** the reading of three frozen phrases, each identified in its ruling, under the AIEF-AMD-009 §AMD-23 supersession-in-reading mechanism. Ten rulings, AMD-25 through AMD-34.

---

## Independence declaration

The pre-flight report was produced by `project-manager · S-2026-08-08-03c` (A3), which raised the open questions and, per its contract, could not rule on them. These rulings are made by `chief-systems-engineer · S-2026-08-08-04`, a cold session holding no state from any prior session. Under AMD-20, agent identity is the pair (role, session); raiser and ruler differ in both role and session, satisfying LAW-02 clause 5 and `tpl-ecr` acceptance condition 3. The same-authority ruled-and-applied departure is separately recorded in § *Separation of Duties*.

## Reading order

AMD-27 (DC-4) is the prerequisite: until a core aggregate construction exists, `MANIFEST.lock`, the `BINDING` pin, B2a, and the release digest are all uncomputable. AMD-26 (tokenizers) and AMD-29 (budget record) are mutually dependent and are read together. Every construction follows the DC discipline of AMD-16/AMD-17: deterministic, reproducible, with a published worked example that any implementation must reproduce exactly.

| Ruling | Disposes | Change class |
|---|---|---|
| AMD-25 | OQ-1 | Authority ruling + one `generation_order[6].barrier` extension |
| AMD-26 | OQ-2 | Additive — `metadata.reproducible.tokenizer_families`; `validation[V-09]` text extension |
| AMD-27 | OQ-4, OQ-5 | Additive — DC-4 in `metadata.reproducible.digest_constructions` |
| AMD-28 | OQ-3 | Additive — DC-5 in `metadata.reproducible.digest_constructions` |
| AMD-29 | OQ-6 | Additive — `metadata.reproducible.budget_measurement_record` |
| AMD-30 | OQ-7 | Additive — `metadata.reproducible.distributable` |
| AMD-31 | OQ-8 | Interpretation ruling + `generation_order[6].barrier` extension |
| AMD-32 | OQ-9 | Authority ruling — supersession in reading. No manifest change |
| AMD-33 | OQ-10, OQ-12 | Additive — `metadata.reproducible.build_time_reproducibility`; `validation[V-10]` text extension |
| AMD-34 | OQ-13 (analysis and recommendation only) | Authority analysis. **No manifest change, no BINDING change** |

---

## AMD-25 — Compiler Scope: Stage-6-Only Increment Admissible

**Disposes:** OQ-1 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-04`

### Question, restated

Does clearing CMP-BLOCK-004 for Stage 6 require the full six-stage `aief-compile` (`AIEF-FRZ-001` Part 4, lines 385–443), or does a Stage-6-only increment suffice, given that Stages 1–5 exist on disk, are declared complete (`STATE.md` `compiler_stage`, AIEF-AMD-007), and Stage 5's emission is independently verified (VER-003)?

### Ruling

> **CMP-BLOCK-004 clearance *for Stage 6 execution* admits a deterministic Stage-6-only compiler increment. CMP-BLOCK-004 clearance *for Framework Release 1.0.0* does not: the full six-stage `aief-compile` remains required.**

Precisely:

1. **The increment's contract.** A Stage-6-only implementation takes as input the verified Stage 1–5 tree, `metadata.reproducible` and `version` — exactly the declared Stage 6 inputs (`framework.manifest.json` `generation_order[6].inputs`; `AIEF-FRZ-001:439`). It must be deterministic software: identical input tree plus identical manifest ⇒ byte-identical `MANIFEST.lock`, byte-identical distributable, identical DC-4 aggregate and identical DC-5 release digest. The reproducibility requirement (`AIEF-FRZ-001:383`) is **not weakened**: it is applied to the increment over its declared input, and enforced at build time by AMD-33.
2. **"Verified input tree" is defined**, not assumed: the compile-time precondition of AMD-31 must pass against the Stage 1–5 output immediately before emission. The increment therefore never lockfiles an unverified tree.
3. **What the increment cannot do**, stated plainly: it cannot produce V-10's evidence in full meaning — V-10's target is the *build*, and "identical manifest ⇒ identical output" across the whole pipeline requires Stages 1–5 to be executable software, as does V-18 (install onto three reference projects presupposes Stage 1 profile-selective emission and Stage 3 install-refusal). The increment can and must satisfy V-10's criterion *over its own input domain* (two executions, two platforms, identical digests); the full-pipeline V-10 and V-18 remain gated on the full compiler.

### Why this and not the alternatives

| # | Alternative | Judgement |
|---|---|---|
| A | Stage-6-only increment for Stage 6; full compiler for Release 1.0.0 | **Adopted.** Matches the blocker ledger exactly — CMP-BLOCK-004 blocks "Compiler Stage 6, V-10" (`OPEN_ITEMS.md:18`) and the campaign sits after Stage 6 (`AIEF-FRZ-001:538`). Stages 1–5 were lawfully executed as sessions, accepted, and are hash-verifiable on disk; requiring their re-implementation before B2a can exist would leave `core/` unprotected for the longest possible time, inverting F-06's purpose |
| B | Full six-stage compiler before any Stage 6 execution | **Rejected.** Nothing in the frozen text requires it for Stage 6 emission; it delays the integrity guarantee (B2a) behind the largest work package while protecting nothing more, and it re-derives outputs that are already verified where verification exists (VER-003) |
| C | Hand-execute Stage 6 as a session, like Stages 1–5 | **Rejected.** Stage 6's own failure semantics ("non-reproducible digest halts the build") require repeat execution with byte-identity — a property of software, not of a session. CMP-BLOCK-004's text is explicit that the deficiency is "not implemented as deterministic software", and Stage 6 is precisely the stage whose output (the integrity baseline) must not depend on an unrepeatable actor |

### Manifest change

`generation_order[6].barrier` — extended with the increment admissibility and its limits (see the barrier text; also carries AMD-31 and AMD-33). No stage definition is modified; the six-stage pipeline remains the declared architecture.

---

## AMD-26 — Tokenizer Families: TF-1 and TF-2

**Disposes:** OQ-2 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-04`

### Gap, restated

`AIEF-FRZ-001:142` freezes the rule — *measurement with two tokenizer families; the maximum governs* — and names no family. V-09 and Stage 6's own budget step are unexecutable until the families are named. VER-001 used estimators and flagged them non-authoritative (`VER-001:231`).

### Ruling

> **TF-1 is byte-level BPE with the tiktoken `cl100k_base` vocabulary. TF-2 is SentencePiece unigram with the T5 `spiece.model` (32,000 pieces, Apache-2.0).** Both are declared normatively at `metadata.reproducible.tokenizer_families`. Special tokens are disabled in both: measurement tokenises file text only.

| Property | TF-1 | TF-2 |
|---|---|---|
| Algorithm family | byte-level BPE, greedy merge over a fixed vocabulary | unigram language model, Viterbi segmentation over a fixed serialised model |
| Artifact | `cl100k_base.tiktoken` vocabulary file | `spiece.model` T5 SentencePiece model |
| Public specification | tiktoken published vocabulary and pre-tokenisation pattern | SentencePiece published format and algorithm |
| Offline | Yes — artifact plus algorithm, no service | Yes — artifact plus algorithm, no service |
| Deterministic | Yes — greedy BPE has a single output per input | Yes — Viterbi has a single output per input under a fixed model |

### Pinning mechanism

Each family is pinned by the **raw-octet SHA-256 of its artifact**, recorded in the `budget_measurement` member of `core/MANIFEST.lock` at the first authoritative Stage 6 measurement and verified before every subsequent measurement. Raw octets, not DC-1: the artifacts are binary/opaque data, and DC-1's text normalisation must never touch them.

**Why the pin values are not written in this amendment:** this authority does not hold the artifacts, and writing a hash it has not computed from the artifact in hand would be an assumption dressed as a ruling — the exact LAW-12 violation this document exists to avoid. The *mechanism* is ruled now; the *values* are measured at first build and are frozen from then on by the lock that records them, which is itself pin-bound and approval-bound. This is the AMD-16 pattern: declare the construction going forward; never reverse-engineer or invent a number.

### Rejected alternatives

| # | Alternative | Why rejected |
|---|---|---|
| B | Two tiktoken encodings (e.g. `cl100k_base` + `o200k_base`) | Same algorithm family twice. "Two families" hedges against family-specific undercounting; two BPE vocabularies do not |
| C | Llama/Mistral `tokenizer.model` for TF-2 | License-gated distribution; not freely redistributable with the framework, so an offline implementer cannot lawfully be handed the pinned artifact |
| D | Hub-named tokenizers (`AutoTokenizer.from_pretrained("...")`) without an artifact pin | A mutable remote reference is not version-pinnable and not offline; the same name can resolve to different bytes over time |
| E | The VER-001 regex estimator as a family | Self-declared non-authoritative; not a tokenizer, no artifact to pin |
| F | Word/character counts scaled by a factor | Not a tokenizer family in any host's sense; the ceiling exists to bound real context consumption |

"The maximum governs" is frozen at `AIEF-FRZ-001:142` and is cited, not restated.

### Manifest change

`metadata.reproducible.tokenizer_families` — new object. `validation[V-09].verifies` extended to bind the check to the declared families (the AMD-19 lesson: a ruling without a check is a convention). No schema amendment: `metadata.reproducible` does not constrain additional properties.

---

## AMD-27 — Core Aggregate Construction (DC-4) and Root-File Coverage

**Disposes:** OQ-4 and OQ-5 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-04`

### Gap, restated

Every use of "aggregate digest" outside the freeze registry refers to `core/MANIFEST.lock` — a set and artifact DC-2 explicitly does not cover (`AIEF-AMD-008:37`). The `digest_constructions` completeness note promises every required digest is constructed there; the core aggregate was not. Additionally: `MANIFEST.lock` lives under `core/` and is declared `integrity: hashed`, creating a self-coverage question; and the three L0 root files are `integrity: hashed` in a partition declared `integrity_verified: true`, while B2a's wording says "core/ aggregate digest" — a conflict requiring an answer, not silence.

### Ruling — DC-4

> **DC-4.** SHA-256 over the concatenation of one record per covered file, each record `<path>` `<SP>` `<digest>` `<LF>` — the DC-2 record grammar exactly — where `<path>` is the emission path relative to `.ai/` as declared in `files[].path` and `<digest>` is the file's DC-1 digest, records sorted ascending by the UTF-8 octet sequence of `<path>`.

| Element | Definition |
|---|---|
| Covers | Every `files[]` entry declared `integrity: hashed` that the build emits for the selected profile: `BOOT.md`, `FRAMEWORK.md`, `README.md`, `core/**` including `core/templates/**` and `core/validation/**`, and `core/profiles/<selected>/**`. **`core/MANIFEST.lock` excluded** (self-exclusion). Unhashed partitions (`project`, `adapters`) never covered |
| Record / order / preimage / encoding | Identical discipline to DC-2: `<path>` `<SP>` `<digest>` `<LF>`; ascending UTF-8 octet order of `<path>`; no header, no trailer, no BOM; UTF-8. One grammar for both set digests — a second grammar would be a second defect surface with no benefit |
| Self-exclusion | The lock records the aggregate; covering itself would be circular. The lock contributes no record. Its binding is the `BINDING` pin: `core_digest_pin` **equals** `aggregate_digest`, per `AIEF-FRZ-001` §1.7 F-06 ("the expected aggregate digest") — frozen, cited, not re-decided |
| B2a procedure | Recompute DC-1 per listed file and compare; verify list↔tree coverage in both directions; recompute DC-4 and compare to `aggregate_digest`; compare `aggregate_digest` to the pin; any mismatch halts, blocking. O(n) hash, no content load |
| Lock serialisation | UTF-8 JSON per `sch-core-manifest`; member order puts `aggregate_digest` before `files`, so the T1 "digest read" stays within the 200-token cap (`AIEF-FRZ-001:135`) |
| Output | 64 lowercase hex, truncation prohibited. Duplicate path: build defect, DC-4 undefined, build halts. Empty covered set: never lawful — a failed build, not an empty aggregate |

### Worked example — synthetic, fixed, publishable

Two entries:

```
path  BOOT.md        digest 0000000000000000000000000000000000000000000000000000000000000000
path  core/VERSION   digest 1111111111111111111111111111111111111111111111111111111111111111
```

Preimage (`BOOT.md` sorts before `core/VERSION`: `B` = 0x42 < `c` = 0x63):

```
BOOT.md 0000000000000000000000000000000000000000000000000000000000000000
core/VERSION 1111111111111111111111111111111111111111111111111111111111111111
```

DC-4 digest:

```
eb6e969b9f1d31a367ccf83315c1a40f8df0bb1c7dec41566a637ac3740325b1
```

Any implementation that does not produce exactly this value for exactly this input is non-conforming.

### Ruling — root-file coverage (OQ-5)

> **The three L0 root files are covered by DC-4 and listed in `MANIFEST.lock.files`.**

Grounds: `files[boot]`, `files[framework-md]` and `files[readme]` declare `integrity: hashed`; the `root` partition declares `integrity_verified: true`; and a `hashed` declaration verified by nothing is a dead declaration — the manifest would be asserting a protection that no mechanism provides, which is the FM-3 pattern of `AIEF-FRZ-001` §1.7. `BOOT.md` is read at B1, *before* B2a — it is the highest-value tamper target in the tree, and the reading that excludes it protects everything except the entry point.

The narrower reading — `core/` prefix only, root files unverified — is **rejected**: it makes the root partition's `integrity_verified: true` false for three of its members and satisfies the letter of one phrase by breaking two declarations.

**Supersession in reading:** the phrase *"Verify `core/` aggregate digest"* (B2a, `AIEF-FRZ-001:205` and `BOOT.md` line B2a) is superseded in reading as *"verify the aggregate digest recorded in `core/MANIFEST.lock`"*, whose coverage is the integrity-verified emitted set defined by DC-4. Mechanism: AIEF-AMD-009 §AMD-23 precedent; no frozen byte is edited; digests unchanged. The emitted `BOOT.md` needs no re-emission — its B2a row already reads "Verify core aggregate digest against MANIFEST.lock", which under this ruling resolves through the lock's declared coverage.

### Recorded residual — accepted property, not silence

Lock members other than `files` and `aggregate_digest` (`framework_version`, `build_provenance`, `hash_algorithm`, `normalisation`, `budget_measurement`) are **not bound by the pin**, because F-06 freezes the pin as the aggregate digest and this amendment does not thaw frozen text. Tamper on those members is detected by V-12's tamper campaign and by version control, not by B2a. This is an accepted, recorded property of the frozen pin design — recorded here so it is a decision, not an oversight.

### Rejected alternatives

| # | Alternative | Why rejected |
|---|---|---|
| B | Pin = DC-1 of the whole `MANIFEST.lock` file | Stronger binding, but contradicts frozen F-06 ("the pin records the expected **aggregate digest**"). Changing the pin's meaning is a thaw of `AIEF-FRZ-001` §1.7, which this amendment has no basis to perform |
| C | Include `MANIFEST.lock` in its own `files` list with a placeholder digest | Placeholder-digest constructions are exactly the "required but never constructed" defect class; the digest would be unverifiable by the construction that contains it |
| D | A second, root-only aggregate alongside the core aggregate | Two aggregates, two pins, two failure modes, no additional protection over one aggregate with declared coverage |

### Manifest change

`metadata.reproducible.digest_constructions.core_aggregate` — new object carrying the normative definition and worked example. DC-1, DC-2, DC-3 untouched. No schema amendment.

---

## AMD-28 — Release Digest (DC-5)

**Disposes:** OQ-3 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-04`

### Ruling

> **DC-5.** SHA-256 over the raw octets of the distributable archive exactly as emitted. No normalisation of any kind. **The release digest is distinct from `MANIFEST.lock.aggregate_digest`, by construction and by role.**

| Element | Definition |
|---|---|
| Domain | The archive's raw octets. DC-1 normalisation applies to text content, never to a binary container; the container's byte-determinism is guaranteed by AMD-30's construction rules, so raw hashing is reproducible |
| Distinct because | DC-4 binds the *installed tree content* as (path, DC-1 digest) pairs; DC-5 binds the *shipped container*, including archive structure and the contained `MANIFEST.lock` itself. Different domains; equality is meaningless and never expected |
| Both required because | DC-4 authenticates the tree at every boot (B2a). DC-5 authenticates the acquisition — before installation, no tree exists for DC-4 to verify |
| Recording | (i) a sidecar `<archive-name>.sha256` beside the archive, `sha256sum` text convention: `<digest>` `<SP>` `<SP>` `<archive-name>` `<LF>`; (ii) the **Integrity statement** section of the release notes filed per `tpl-release-notes` — an existing required section, so no new artifact class and no template change. Never inside the archive and never inside `MANIFEST.lock`: the archive contains the lock, so either would be circular |
| Output | 64 lowercase hex, truncation prohibited |

### Worked example — fixed, publishable

Input: the three octets `0x61 0x62 0x63`. DC-5 digest:

```
ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
```

This is the published FIPS 180 SHA-256 test vector, chosen deliberately: it proves the digest is plain SHA-256 over raw octets with no normalisation layer, and any implementation can verify against an independent authority.

### Rejected alternatives

| # | Alternative | Why rejected |
|---|---|---|
| B | Release digest ≡ `aggregate_digest` | Leaves the shipped container unbound: a corrupted or substituted archive whose extracted tree is then "fixed up" is undetectable before install; and the frozen output list names them as two outputs (`AIEF-FRZ-001:441`), which reading them as one would collapse |
| C | DC-2/DC-4-style record digest over archive members | Duplicates DC-4 (already inside the lock, inside the archive) while still not binding the container bytes |
| D | Record the release digest inside `MANIFEST.lock` | Circular — the lock is inside the archive the digest covers |

### Manifest change

`metadata.reproducible.digest_constructions.release_digest` — new object. `generation_order[6].outputs` release-digest entry made precise. No schema amendment.

---

## AMD-29 — Budget Measurement Record

**Disposes:** OQ-6 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-04`

### Ruling

> **The budget measurement record is the `budget_measurement` member of `core/MANIFEST.lock`.** It is not a separate file.

| Element | Definition |
|---|---|
| Admissibility | `sch-core-manifest` declares `additionalProperties: true`; the member is schema-admissible today. **No schema amendment required** |
| Content | Per-file token counts under each family for every T0/T1 file with a non-null `token_cap`; per-family T0+T1 totals; the governing maxima; verdict against every per-file cap and the 6,000 ceiling; the tokenizer artifact identifiers with their raw-octet SHA-256 pins (AMD-26); measurement timestamp and Stage 6 build identifier |
| Failure semantics | Any cap or ceiling breach under either family halts the build — the frozen Stage 6 failure row, cited |
| Position | After `aggregate_digest`, before `files` (AMD-27 lock serialisation), preserving the 200-token digest read |

### Why in the lock, and the alternative recorded

"Stamp version and budget measurement" (`AIEF-FRZ-001:440`) — a *stamp* goes onto the emitted artifact. The lock is emitted by the same stage, from the same inputs, at the same instant; the measurement is provenance of exactly that build. The alternative — a separate `core/BUDGET.lock` — was weighed and **rejected**: it would require a `files[]` entry (MI-1/MI-3/V-01 surface), an owner, a schema or a schema exemption, and a consumer; no boot step reads it; it would be a dead file in every install, violating the zero-dead-file rule (`AIEF-FRZ-001:80`). The in-lock member is read by V-09 and by auditors through the lock they already verify. The two options were equally sound only until the dead-file rule was applied; then only one remained.

### Manifest change

`metadata.reproducible.budget_measurement_record` — new object. `generation_order[6].outputs` budget entry made precise. No schema amendment.

---

## AMD-30 — Distributable Archive

**Disposes:** OQ-7 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-04`

### Ruling

> **The distributable is an uncompressed POSIX ustar tar archive named `aief-<semver>-<profile>.tar`, containing exactly the emitted install set for the selected profile — the DC-4 covered set plus `core/MANIFEST.lock`, rooted at `.ai/` — built deterministically, published as a release artifact with its DC-5 sidecar, and not tracked in the instance repository.**

| Element | Definition |
|---|---|
| Format | POSIX ustar tar, uncompressed |
| Contents | The DC-4 covered set plus `core/MANIFEST.lock`, each entry rooted at `.ai/`. Nothing else — zero-dead-file rule, cited (`AIEF-FRZ-001:80`) |
| Determinism | Entries in ascending UTF-8 octet order of archive path; `mtime` 0; `uid`/`gid` 0; empty `uname`/`gname`; mode 0644 files / 0755 directories; no extended headers beyond pax long-path necessities |
| Disposition | **Not tracked in-repo.** The repository *is* the installed tree; tracking a generated container would duplicate every artifact in a second, unverified form and put a build product under source control. Published with the release (release-asset or equivalent), referenced from the release notes, verified by DC-5 |

### Rejected alternatives

| # | Alternative | Why rejected |
|---|---|---|
| B | zip | Per-entry timestamps, per-implementation central-directory variance and compression variance make byte-identity across platforms an implementation accident rather than a property |
| C | tar.gz / tar.zst | Compressor output varies across implementations and versions; byte-identical output (`AIEF-FRZ-001:383`) would then pin a specific compressor binary, which the framework has no mechanism to pin. Consumers may compress for transport outside the framework boundary; such a wrapper has no framework meaning and DC-5 does not cover it |
| D | Track the archive in-repo under `releases/` | Duplicates the tree in unverifiable form; every release grows the repository by a full framework copy; and the in-repo copy would itself need coverage rules no declaration provides |
| E | No archive — "the repo is the distributable" | Contradicts the frozen output list ("distributable archive", `AIEF-FRZ-001:441`) and leaves V-18's install harness with no installable unit |

### Manifest change

`metadata.reproducible.distributable` — new object. `generation_order[6].outputs` distributable entry made precise. No schema amendment.

---

## AMD-31 — Compile-Time Checks Precede Stage 6 Emission

**Disposes:** OQ-8 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-04`

### Conflict, restated

AMD-19 rules V-24 compile-time *because* "the check must run before that [a build consuming a frozen input], not after release" (`AIEF-AMD-008:345`). Yet §6.4 places the whole campaign after Stage 6 (`AIEF-FRZ-001:538`), and the frozen Stage 6 process lists no check execution.

### Ruling

> **Both are right about different things. The `phase: compile-time` declaration is a *precondition class*: every check declared compile-time, except V-10, must pass against the manifest and the complete Stage 1–5 output immediately before Stage 6 emits. §6.4's post-Stage-6 campaign is the *recorded evidence run* of the full suite that gates Framework Release 1.0.0. Stage 6 runs the compile-time checks as build preconditions; the campaign re-runs everything as release evidence.**

- **V-10 is the exception, ruled explicitly:** its subject *is* the Stage 6 build across executions and platforms. A check on the build cannot precede the build. It runs on and after Stage 6, and its two-platform form belongs to the campaign (AMD-33).
- **Coherence with Stage 6's own failure semantics:** the frozen failure row halts the build on budget overrun and non-reproducible digest — Stage 6 already executes V-09's substance and a reproducibility check *inside* the build. This ruling generalises what the frozen text already does for two checks to the whole compile-time class, rather than leaving V-01…V-08 and V-23…V-25 in a limbo where a build may lockfile a tree its own declared BLOCKING compile-time checks would fail.
- **Supersession in reading:** to the extent §6.4's ordering is read as *prohibiting* check execution before Stage 6, that reading is superseded: §6.4 orders the campaign relative to Release 1.0.0 and is silent, not prohibitive, on preconditions. Bytes unchanged.
- **Effect on CMP-BLOCK-005 scope:** only the compile-time class (V-01…V-09, V-23…V-25) gates Stage 6, and of it only V-09 needs CMP-BLOCK-005 infrastructure (the tokenizers, ruled in AMD-26). The runtime/installation harnesses (V-11…V-21 infrastructure) gate the campaign and Release 1.0.0, not Stage 6 — confirming the pre-flight §3 reading.

### Rejected alternatives

| # | Alternative | Why rejected |
|---|---|---|
| B | §6.4 literal: no checks before Stage 6 | Convicts the frozen Stage 6 process itself, which already halts on V-09's substance mid-build; and permits lockfiling a tree that fails V-01 — an integrity baseline built on an invalid manifest |
| C | All 25 checks before Stage 6 | Impossible: V-11's B2a fault case, V-12, and V-10 require Stage 6 output to exist. A precondition that cannot be satisfied is a permanent halt dressed as rigour |

### Manifest change

`generation_order[6].barrier` — extended with the precondition (shared barrier text with AMD-25/AMD-33). No check's phase field is changed; the ruling gives the existing field its operative meaning.

---

## AMD-32 — Campaign Scope: V-01…V-25

**Disposes:** OQ-9 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-04` · **No manifest change**

### Ruling

> **The pre-Release-1.0.0 validation campaign is the entire declared check registry — today V-01…V-25 — not the literal enumeration "V-01…V-21".**

Grounds:

1. **Part 5's own preamble** is set-quantified, not enumerated: *"Every check below must pass before Framework Release 1.0.0"* (`AIEF-FRZ-001:449`). The authoritative "below" is the registry the manifest declares and Stage 5 emits (`core/validation/CHECKS.md`, 25 checks) — the manifest is the single source of truth (`AIEF-FRZ-001` Part 3).
2. **The enumeration was exhaustive when written** — 21 checks existed at freeze. V-22 (git policy, AMD-001-era) and V-23/V-24/V-25 (AMD-19) were added by registered instruments with recorded approvals. An enumeration that was a snapshot of the set is superseded by the set, not the other way around.
3. **The alternative is incoherent:** releasing 1.0.0 with four declared-BLOCKING checks unexecuted contradicts the same section's "21 blocking validations. Zero non-blocking checks" *principle* — that every declared check blocks. The count was true then; the principle governs now.

**Supersession in reading:** the phrases "execute V-01…V-21" (`AIEF-FRZ-001:538`) and "21 blocking validations" (`:487`) are superseded in reading by "execute every check in the declared validation registry, all BLOCKING". Mechanism: AIEF-AMD-009 §AMD-23 precedent. Bytes and digest unchanged.

### Consequence recorded — not performed

`adapters/ADP-ci.md` remains stale (OI-C-02): it enumerates 22 checks and phase ranges omitting V-23…V-25. Under this ruling its required content is now fixed — 25 checks, compile-time range V-01…V-10 plus V-23…V-25, and the AMD-31 precondition semantics. **The Stage 4 re-emission is a compiler/repository action outside this instrument's scope and is not performed here**; OI-C-02's disposition target is updated in `OPEN_ITEMS.md` as consequence-recording only.

---

## AMD-33 — Build-Time Reproducibility and V-10 Platforms

**Disposes:** OQ-10 and OQ-12 · **Ruled by:** `chief-systems-engineer · S-2026-08-08-04`

### Ruling — Stage 6's own reproducibility check (OQ-10)

> **Stage 6 executes the build at least twice on the build platform within one release run, and halts unless every execution yields a byte-identical distributable, an identical DC-4 `aggregate_digest` and an identical DC-5 release digest.**

This makes the frozen failure row — "Non-reproducible digest halts the build" (`AIEF-FRZ-001:443`) — executable, with a declared trial floor and a declared identity criterion. It is deliberately *narrower* than V-10: single platform, part of every build. V-10 remains the campaign check across platforms.

### Ruling — V-10's two platforms (OQ-12)

> **V-10's two platforms are Windows and at least one of Linux or macOS.**

Rationale: the platform axis exists to catch environment-dependent output — and the dominant environment hazard for a text-emitting compiler is line-ending convention, the exact hazard DC-1's normalisation neutralises (`AIEF-FRZ-001:109-113`). Windows (CRLF-native) plus any LF-native platform exercises both conventions; Linux plus macOS would test two LF-native platforms and leave the CRLF path — the one that caused OD-2's rejection of raw-byte hashing — unexercised. V-12's three named platforms (`AIEF-FRZ-001:471`) remain unchanged and are a superset of any V-10 selection.

Rejected: naming exactly two fixed platforms (needlessly forbids a three-platform V-10 run and adds nothing); leaving the pair free (permits the Linux+macOS selection that dodges the CRLF hazard).

### OQ-11 — explicitly not ruled

The V-14 trial count is a campaign-harness parameter with no bearing on any construction ruled here; it does not fall out of these rulings, and a number chosen without an engineering basis would be decoration. **Left open with an owner** — recorded as OI-V-06 in `OPEN_ITEMS.md`, A4 with the campaign design, before V-14 implementation.

### Manifest change

`metadata.reproducible.build_time_reproducibility` — new object. `validation[V-10].verifies` extended with the platform rule and the DC-4/DC-5 bindings. No schema amendment.

---

## AMD-34 — Allocation of the Compiler Work: Analysis and Recommendation Only

**Addresses:** OQ-13 · **Change class:** authority analysis. **No manifest change. No BINDING change. The software profile is not activated. `BINDING.enabled_agents` is not edited. The choice is reserved to the human owner and remains open.**

### What the framework lawfully requires

1. **No enabled role may accept the work today.** `BINDING.enabled_agents` enables the five universal roles and four `mechanical.*` roles; both blockers carry Authority "Software" (`OPEN_ITEMS.md:18-19`); the universal roles are contract-barred (PM: no engineering decisions; QA: may not author what it validates; repository-engineer: may not generate `MANIFEST.lock` outside Stage 6) — the pre-flight §4 analysis is confirmed at A4.
2. **The change authority is settled law, not a new question.** `BINDING.approval_authority: human-owner`; a change to the enabled agent set follows the AMD-006 precedent exactly: an A4 manifest/instrument amendment plus a recorded LAW-10 human approval, then the BINDING edit by its owning role. `project/BINDING` declares the active profile (`AIEF-FRZ-001:77`); nothing permits an agent to self-enable a role.

### The admissible options

| Option | Mechanism | Properties |
|---|---|---|
| (a) Enable the three `software.*` roles in this instance | A4 amendment + human approval (AMD-006/LAW-10 pattern); BINDING `enabled_agents` extended; profile files emitted per the zero-dead-file discipline | Keeps the compiler, its verification and the tree it must verify in one evidence chain, one freeze registry, one ledger. Requires care that `active_profile` semantics (one active lifecycle) are not disturbed — enabling agents is not switching the profile |
| (b) Separate software-profile project for `aief-compile` | New AIEF instance, software profile, its own BINDING/ledger | Clean lifecycle fit (recurring gates), but fragments traceability: the compiler that certifies *this* tree would be governed, versioned and verified elsewhere, and LAW-06's unbroken-authority-chain requirement must then span repositories with no declared mechanism |
| (c) Contract the work outside the framework | Human-owner contract; deliverables verified on intake | Fastest headcount path, but the artifact that guards `core/` integrity would be produced outside every conduct, verification and provenance law the framework has; intake verification would rest on exactly the infrastructure that does not yet exist |

### A4 recommendation — recommendation, not decision

**Option (a).** The compiler's single purpose is to certify this repository's own integrity baseline; the evidence chain from `framework.manifest.json` through `MANIFEST.lock` to B2a should not cross a repository boundary (option b) or a framework boundary (option c) at its most security-relevant link. The AMD-006 precedent shows the mechanism is proven and small. Options (b) and (c) remain lawful; (c) is recommended against for the reason stated, not merely ranked below.

> **Recorded explicitly: the CHOICE among (a), (b), (c) is the human owner's** (`BINDING.approval_authority: human-owner`; profile/agent-set changes are human-approved in every precedent). **OQ-13 remains open** until the owner decides; no implementation allocation exists in the meantime, and this instrument makes none.

---

## Blast Radius

Determined by inspecting what renders each changed manifest section, following the AMD-008/AMD-009 method (their search result — no emitted artifact renders a dependency list — re-checked and still valid).

| Changed section | Rendered by | Effect |
|---|---|---|
| `metadata.reproducible.*` (five new objects, one note edit) | `.ai/FRAMEWORK.md` § Integrity renders DC-1 only, unchanged | **None** |
| `validation[V-09].verifies`, `validation[V-10].verifies` | `core/validation/CHECKS.md` and `MANIFEST` — **Stage 5 output, emitted at `S-2026-08-08-03` from the pre-amendment text.** Check count unchanged at 25 | **STALE in two `verifies` texts.** A Stage 5 re-emission is compiler work (CMP-BLOCK-004) and is not performed here. Recorded as **OI-V-07** |
| `generation_order[6].outputs`, `.barrier` | No `files[]` entry carries `content_ref: generation_order` | **None** |
| `adapters/ADP-ci.md` | Already stale (OI-C-02); check count unchanged; its required content is now fully determined by AMD-32 | **No new staleness**; disposition target updated in OI-C-02 |

**No law rule or clause, no role contract, no schema, no template, no partition, layer, tier, boot step or stage definition is modified. DC-1, DC-2 and DC-3 are byte-for-byte untouched. The five universal roles, four mechanical roles and thirteen laws are untouched.**

---

## Separation of Duties — Recorded Tension

`core/agents/INDEX.md`: **`chief-systems-engineer` may not implement what it approved.** This amendment was ruled, and its manifest edits and register updates applied, by the same authority (`chief-systems-engineer · S-2026-08-08-04`) at the direction of the human owner — `core/PRECEDENCE.md` rank 1, which outranks the rank-6 agent specification. Identical in form to the departures recorded in AMD-008 and AMD-009 §§ *Separation of Duties*; identically **authorised, not erased**.

| | |
|---|---|
| Duty separated | A4 rules and approves; A1 implements |
| Departure | A4 both ruled and applied |
| Authority for the departure | Rank-1 live human instruction, recorded per LAW-10 in APR-006 and APR-007 |
| Mitigating control | Independent cold-context `qa-engineer` audit of this session's work, dispatched by the same directing instruction — follows immediately |
| Not mitigated by | Anything this document says about itself. Under LAW-05 an authority's assertion about its own work carries no evidentiary weight |

---

## Artifacts Not Modified

| Artifact | Status |
|---|---|
| `AIEF-FRZ-001` | **Unmodified.** Three phrases superseded in reading (AMD-27: B2a "core/ aggregate digest"; AMD-31: §6.4 ordering read as prohibition; AMD-32: "V-01…V-21" / "21 blocking validations"); bytes and DC-1 digest unchanged |
| `AIEF-AMD-001` … `AIEF-AMD-009`, both ADRs | Unmodified |
| `SCH-framework-manifest.schema.json` | **Unmodified — no schema amendment required.** Every addition lands in `metadata.reproducible` (additional properties unconstrained) or in existing string fields (`validation[].verifies`, `generation_order[].barrier`, `generation_order[].outputs` items) |
| `SCH-core-manifest.schema.json` and every emitted schema | Unmodified — the budget member is admitted by its existing `additionalProperties: true` |
| DC-1, DC-2, DC-3 | **Preserved exactly as declared.** DC-4 and DC-5 are additions; no existing construction is altered |
| All 13 laws, 5 universal roles, 4 profile roles, 6 workflows, 10 templates | Unmodified |
| `.ai/core/**`, `.ai/adapters/**` | **Not touched.** Re-emission is compiler work (CMP-BLOCK-004/OI-C-02/OI-V-07) |
| `core/MANIFEST.lock` | **Not created.** Compiler Stage 6 is not executed by this amendment |
| `project/BINDING.md` | **Not modified.** No pin write, no agent enablement |
| `project/ledger/**` | **Not written.** `HEAD` remains at `genesis`; `L-0000001` does not exist |
| `spec/**`, every implementation package, all CAD | Not touched |
| Git history, tags, author or committer identity | **Not touched.** No commit, tag or push is made by this session |

## Approvals Required and Recorded

| Frozen-artifact change | Approval | Bound to |
|---|---|---|
| `framework/framework.manifest.json` — the enumerated AMD-010 changes | `project/approvals/APR-006` | its post-amendment DC-1 digest |
| Freeze-registry addition of this document (AMD-21 criterion: authorising instrument) | `project/approvals/APR-007` | this document's DC-1 digest |

Per LAW-01, LAW-10 and `core/PRECEDENCE.md` clause 4: a rank-1 override of rank 3 is recorded as an approval artifact before dependent work is committed. Per the AMD-16 design property, neither this document's own digest nor the post-registration DC-2 aggregate appears in this document; both live in the registry and the approval artifacts.

---

**END OF AIEF-AMD-010**
