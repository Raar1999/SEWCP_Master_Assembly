# Validation Checks

> **Generated artifact.** Emitted by aief-compile Stage 5 from `framework.manifest.json`.
> Do not edit. Regenerate from the manifest.

| | |
|---|---|
| Framework | AIEF 1.0.0 |
| File id | `checks` |
| Layer / partition | L6 / core |
| Tier | none |
| Owner | `qa-engineer` |
| Mutability | immutable |

---

**25 checks.** Every check is severity BLOCKING. Source of truth: `manifest.validation`.

## Register

| ID | Class | Phase | Law | Target |
|---|---|---|---|---|
| V-01 | Manifest validation | compile-time | — | `framework.manifest.json` |
| V-02 | Dependency validation | compile-time | — | `dependencies` |
| V-03 | Cross-reference validation | compile-time | LAW-06 | `all sections` |
| V-04 | Law validation | compile-time | — | `laws` |
| V-05 | Agent validation | compile-time | LAW-04 | `agents` |
| V-06 | Schema validation | compile-time | LAW-10 | `schemas` |
| V-07 | Template validation | compile-time | — | `templates` |
| V-08 | Profile validation | compile-time | — | `profiles` |
| V-09 | Token budget validation | compile-time | — | `files` |
| V-10 | Compiler validation | compile-time | LAW-05 | `distributable` |
| V-11 | Boot validation | runtime | LAW-09 | `boot_sequence` |
| V-12 | Core integrity validation | runtime | LAW-01 | `manifest-lock` |
| V-13 | Ledger validation | runtime | LAW-09 | `ledger-head` |
| V-14 | Crash validation | runtime | LAW-09 | `ledger-head` |
| V-15 | Concurrency validation | runtime | LAW-09 | `state` |
| V-16 | Content trust validation | runtime | LAW-13 | `LAW-13` |
| V-17 | Runtime sequence validation | runtime | LAW-09 | `runtime_sequence` |
| V-18 | Multi-discipline install | installation | — | `profiles` |
| V-19 | Lifecycle validation | installation | LAW-03 | `profiles` |
| V-20 | Path validation | installation | LAW-08 | `files` |
| V-21 | Upgrade validation | installation | LAW-01 | `partitions` |
| V-22 | Git policy validation | installation | LAW-07 | `repository` |
| V-23 | Stage monotonicity validation | compile-time | — | `files.depends_on` |
| V-24 | Freeze registry validation | compile-time | LAW-01 | `project/FROZEN.md` |
| V-25 | Encoding conformance validation | compile-time | — | `files` |

## Law bindings

| Law | Bound checks |
|---|---|
| LAW-01 | V-12, V-21 |
| LAW-02 | V-06 |
| LAW-03 | V-19 |
| LAW-04 | V-05 |
| LAW-05 | V-05, V-10 |
| LAW-06 | V-03 |
| LAW-07 | V-21, V-22 |
| LAW-08 | V-03, V-20 |
| LAW-09 | V-11, V-13, V-14, V-15, V-17 |
| LAW-10 | V-06 |
| LAW-11 | V-05 |
| LAW-12 | V-16 |
| LAW-13 | V-16 |

Checks with `law_ref: null` and no law binding are **structural**: V-01, V-02, V-04, V-07, V-08, V-09, V-18, V-23, V-25.
Checks carrying a one-way `law_ref` (MI-5 satisfied without altering the law record): V-24.

## Check specifications, verbatim

### Phase: compile-time

#### V-01 — Manifest validation

Severity **BLOCKING** · law_ref `none` · target `framework.manifest.json`

> Manifest conforms to SCH-framework-manifest; invariants MI-1 to MI-12 satisfied. MI-3 namespace, per AIEF-AMD-009 AMD-24: every depends_on and referenced_by target is a files[] id; no other namespace satisfies MI-3. Stage-output disjointness, per AIEF-AMD-009 AMD-23: the outputs of generation_order stages are pairwise disjoint path sets after applying declared exclusions; a declared field write into an already-emitted artifact is not an emission

#### V-02 — Dependency validation

Severity **BLOCKING** · law_ref `none` · target `dependencies`

> Dependency graph acyclic; every edge target exists; topological sort succeeds

#### V-03 — Cross-reference validation

Severity **BLOCKING** · law_ref `LAW-06` · target `all sections`

> Every law, agent, template, schema, workflow and check reference resolves

#### V-04 — Law validation

Severity **BLOCKING** · law_ref `none` · target `laws`

> Thirteen laws present; every machine-checkable law bound to at least one check; no orphan law

#### V-05 — Agent validation

Severity **BLOCKING** · law_ref `LAW-04` · target `agents`

> Every role conforms to SCH-agent; at least one forbidden action per role; no unassigned duty conflict; no discipline tag on a universal role

#### V-06 — Schema validation

Severity **BLOCKING** · law_ref `LAW-10` · target `schemas`

> All eight schemas valid JSON Schema 2020-12; every target artifact has a schema

#### V-07 — Template validation

Severity **BLOCKING** · law_ref `none` · target `templates`

> Every template resolves producer and consumer roles and declares acceptance conditions

#### V-08 — Profile validation

Severity **BLOCKING** · law_ref `none` · target `profiles`

> Every profile declares a complete agent set and lifecycle stage set; zero universal-scope discipline leakage

#### V-09 — Token budget validation

Severity **BLOCKING** · law_ref `none` · target `files`

> Per-file caps respected; T0 plus T1 at most 6000 tokens under both tokenizer families

#### V-10 — Compiler validation

Severity **BLOCKING** · law_ref `LAW-05` · target `distributable`

> Build reproducible: identical input yields identical aggregate digest across at least two executions and two platforms

#### V-23 — Stage monotonicity validation

Severity **BLOCKING** · law_ref `none` · target `files.depends_on`

> For every files[] entry S and every id T in S.depends_on: T exists and generator(T) is less than or equal to generator(S). Where generator(T) equals generator(S), the intra-stage emission order is a topological order of the same-stage depends_on subgraph. Distinct from V-02: a backward edge is acyclic, so acyclicity cannot detect it.

#### V-24 — Freeze registry validation

Severity **BLOCKING** · law_ref `LAW-01` · target `project/FROZEN.md`

> Every path registered in project/FROZEN.md exists in the working tree and its DC-1 digest equals the registered digest. The DC-2 aggregate recomputed over the registry equals the value recorded in FROZEN.md and the value in STATE.frozen_set_hash, both at full 64-character length. Every artifact meeting the AIEF-AMD-008 AMD-21 registration criterion is registered. No path is registered twice.

#### V-25 — Encoding conformance validation

Severity **BLOCKING** · law_ref `none` · target `files`

> Every text artifact under .ai/ and every artifact registered in project/FROZEN.md decodes as UTF-8 without error, carries no byte-order mark, uses LF line endings exclusively, ends with exactly one terminal LF, and contains no mojibake sequence outside quoted evidence. Mojibake sequence, normatively: a maximal run of non-ASCII characters that, re-encoded as CP1252 and decoded as UTF-8, both succeed and yield a strictly shorter string. Quoted-evidence exclusion: such a sequence occurring inside a Markdown code span or fenced code block is quoted evidence and is not a violation - the same narrowing V-22 applies to prohibition text. The check matches prose, never quoted evidence, because a report that cites a corrupt byte sequence as evidence must not thereby become non-conforming.

### Phase: runtime

#### V-11 — Boot validation

Severity **BLOCKING** · law_ref `LAW-09` · target `boot_sequence`

> B1 to B9 execute in order; B2a, B4 and B4a halt correctly on induced fault; orientation at B8 supportable from T1 alone

#### V-12 — Core integrity validation

Severity **BLOCKING** · law_ref `LAW-01` · target `manifest-lock`

> Tamper on any core file detected; project-level regeneration of MANIFEST.lock impossible; zero false positives across three platforms

#### V-13 — Ledger validation

Severity **BLOCKING** · law_ref `LAW-09` · target `ledger-head`

> HEAD lookup constant time at depths 10, 1000 and 100000; chain continuous; sequence monotonic with zero gaps or reuse; segment sealing at 500

#### V-14 — Crash validation

Severity **BLOCKING** · law_ref `LAW-09` · target `ledger-head`

> Termination between entry write and HEAD update detected at next boot in all trials

#### V-15 — Concurrency validation

Severity **BLOCKING** · law_ref `LAW-09` · target `state`

> At N of 2, 5 and 10 concurrent sessions: zero lost state updates, zero ledger gaps, deterministic conflict outcome, STATE regenerable from ledger

#### V-16 — Content trust validation

Severity **BLOCKING** · law_ref `LAW-13` · target `LAW-13`

> Adversarial injection corpus yields full data treatment, zero directive execution and a raised stop condition; framework instruction path unaffected

#### V-17 — Runtime sequence validation

Severity **BLOCKING** · law_ref `LAW-09` · target `runtime_sequence`

> All twelve phases traversable; entry and exit criteria enforced; session close writes entry, HEAD, state and releases lock in order

### Phase: installation

#### V-18 — Multi-discipline install

Severity **BLOCKING** · law_ref `none` · target `profiles`

> Install onto mechanical, software and research reference projects with zero dead files and zero core edits required

#### V-19 — Lifecycle validation

Severity **BLOCKING** · law_ref `LAW-03` · target `profiles`

> Each profile completes a full lifecycle; LAW-03 binary disposition preserved in terminal and recurring gates

#### V-20 — Path validation

Severity **BLOCKING** · law_ref `LAW-08` · target `files`

> Zero hardcoded alternate paths; all validation globs resolve; no project artifact matched by any ignore rule

#### V-21 — Upgrade validation

Severity **BLOCKING** · law_ref `LAW-01` · target `partitions`

> Core wholesale replacement leaves project byte-identical; adapters merge additively; MAJOR mismatch halts boot

#### V-22 — Git policy validation

Severity **BLOCKING** · law_ref `LAW-07` · target `repository`

> Every commit and tag satisfies author equals committer equals repository owner; no attribution trailer appears in line-anchored trailer form in any commit message or tag annotation; no AI authorship claim appears in any tracked artifact; published history is not rewritten; after release the working tree is clean and synchronised with the remote, and the release tag resolves to the release commit. Prohibition text that names a forbidden pattern is not itself a violation - the check matches trailer form, never bare substrings. Every actor-provenance field in a tracked project artifact - raised_by, ruled_by, approver, verifier, producer, reviewer, actor, role - resolves to a role registered in core/agents/INDEX.md or to the reserved token boot or role-unrecorded, optionally followed by a session identifier of the form S-YYYY-MM-DD-nn; a model, vendor, product or host-adapter name appearing in such a field is a violation. A host adapter named in a declared configuration field or in prose describing configuration is not a violation. The check examines declared fields, never free text.
