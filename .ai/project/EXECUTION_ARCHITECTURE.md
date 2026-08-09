# Execution Architecture

> **Instance artifact.** Partition `project` — never touched by framework upgrade.
> Owner `project-manager`. Mutability mutable. Tier **T4** — load on cause, never at boot.
> Authority: rank-1 live human instruction, decision `EXEC-D-001`, recorded at
> [`tasks/T-001.md`](tasks/T-001.md) §Checkpoint. Selected option: **A — project partition only**.

---

Bounded, deterministic dispatch of engineering work to agents that share **results, not context**.

This document is the contract. `src/aief_exec/` implements it and `tests/test_exec_*.py` verifies it.

## 1 · Why this exists

Measured on this repository with its own declared tokenizer families TF-1 (`cl100k_base`)
and TF-2 (SentencePiece), per `metadata.reproducible.tokenizer_families`:

| Measurement | TF-1 | TF-2 |
|---|---:|---:|
| Readable corpus, 244 text files | 486,267 | 593,719 |
| `.ai/` + `framework/` alone | 288,954 | 364,842 |
| Boot T0+T1, 8 files | 4,306 | 5,058 |

The corpus is **2.4x a 200,000-token context window**; the framework alone exceeds one.
Boot is bounded and cheap. Everything after boot was not.

For the representative backlog item `OI-C-09`, reaching the first line of work cost
**128,236 TF-1 tokens** by citation chain and **328,585** by unbounded sweep, against a
**10,347** minimum — 12.4x and 31.8x. Seventy-one percent of the authority chain sat in
three monolithic files from which the agent needed one register row, one section and a
few keys.

**Root cause: the repository had no addressable unit smaller than a file, and no unit of
work larger than a file.** This architecture supplies both.

## 2 · What it extends, and what it does not add

Every mechanism here already existed in ratified form. Four were unused; one needed its
domain widened, not its shape changed.

| Need | Existing mechanism extended | Nothing new because |
|---|---|---|
| Task identity | `core/schemas/SCH-task.schema.json`, `core/templates/TPL-task-package.md`, `project/tasks/` | The schema declares `additionalProperties: true`, so the added fields conform **with no schema change** |
| Bounded index over a growing register | `AIEF-AMD-014` §AMD-49 bounded-register split | Ratified for this exact pathology; `EXEC.md` reuses its `index_grammar` verbatim |
| Result provenance and immutability | `LAW-10` content-hash-bound approvals; DC-1 | A result pinning its inputs by DC-1 is the approval construction applied to a result |
| Cross-session communication | `project/ledger/` — `HEAD` at O(1), body T4 | Already the durable channel; §10 binds to it |
| Graph soundness | `V-02` acyclicity and topological sort, `V-23` monotonicity | The same properties, checked over task edges |
| QA isolation | `adapters/ADP-claude-code.md` subagent dispatch; `LAW-05` `duty_conflicts` | The independence model was already sound; only its evidence model was not |
| Honest token budget | `src/aief_stage6/tokenizers.py` TF-1/TF-2 | Both families are live, so counts are exact and never estimated |

**No `.ai/core/**` file is edited. No manifest field changes. No frozen artifact changes.**
This architecture is entirely instance data in partition `project` plus tooling in `src/`.

## 3 · Artifact classes

| Path | Class | Tier | Read when |
|---|---|---|---|
| `project/EXEC.md` | Bounded execution index | T2 | After boot, on role assignment |
| `project/tasks/T-nnn.md` | Task record | T3 | On task acceptance — **one file** |
| `project/results/R-nnn.md` | Result record | T3 | When a dependency declares it |
| `project/EXECUTION_ARCHITECTURE.md` | This contract | T4 | On cause only |

`T-nnn` and `R-nnn` records are **not** `manifest.files[]` entries. They are instance
records inside a declared register class, exactly as ledger entries `L-nnnnnnn` are not
individually registered. This preserves invariant **MI-3** — every `depends_on` and
`referenced_by` target remains a `files[]` id — and means **no manifest amendment is
required per task**.

## 4 · The index — `project/EXEC.md`

Grammar is `AIEF-AMD-014` §AMD-49 `index_grammar`: a title, the instance-artifact
provenance header, a preamble naming its register, then level-2 headings each followed by
**one identifier per line, nothing else on that line**. Per-entry cost is the identifier
alone and is therefore bounded under unbounded task growth.

Headings are the task states: `Active`, `Ready`, `Blocked`, `Awaiting decision`, `Complete`.

**Mapping**, bijective by identifier and checked by `X-02`: every id in `EXEC.md` is the
`task_id` of exactly one record under `project/tasks/`, and every such record's id appears
exactly once in the index.

## 5 · The task record

Conforms to `SCH-task` — `task_id`, `role`, `objective`, `inputs`, `deliverable`,
`acceptance_criteria`, `forbidden_actions`, `escalation` — and adds the following under
`additionalProperties: true`.

```yaml
status:          READY | ACTIVE | BLOCKED | AWAITING-DECISION | COMPLETE
depends_on:      [T-nnn, ...]        # task -> task, serialising edge
consumes:        [R-nnn, ...]        # task -> result, the dependency read
produces:        [R-nnn, ...]        # task -> result, published on completion
blocked_by:      [OI-C-09, ...]      # open-item ids from OPEN_ITEMS.md
read_scope:
  mandatory:     [{path, anchor?}]   # must read; anchor narrows to a section
  dependency:    [{result}]          # consume the result, never its inputs
  optional:      [{path, anchor?}]   # may read on cause
  forbidden:     [glob, ...]         # must not read
write_scope:     [glob, ...]         # the only paths this task may modify
observes:        [glob, ...]         # optional; the residue of the derived
                                     # observation surface - see 5.3
qa:
  verifier_role: qa-engineer         # must differ from role - LAW-05
  report:        path
context_budget:  {tf1: N, tf2: N}    # cap on resolved mandatory read scope
checkpoint:
  phase:         <string>
  completed:     [...]
  pending:       [...]
  next_action:   <string>
  decision:      null | {id, question, options, recommendation, status, resolution}
```

### 5.1 · Read scope and the anchor

`anchor` is what makes the scope smaller than a file. It resolves against the target:

| Target | Anchor form | Resolves to |
|---|---|---|
| Markdown | heading substring, e.g. `AMD-45` | that heading through to the next heading of the same or higher level |
| Markdown table register | row key, e.g. `OI-C-09` | the single table row whose leading cell matches, plus the table header |
| JSON | dotted key path, e.g. `metadata.reproducible.digest_constructions` | that subtree, re-serialised |

An entry without an anchor resolves to the whole file. **Resolution is deterministic and
its cost is measurable before execution** — this is what removes the 71%.

An anchor matching **more than one** heading is a defect, not a first-hit-wins selection:
`AMD-4` matches eight headings in `AIEF-AMD-013` and identifies none of them. `X-03`
rejects it.

### 5.2 · Write scope

Globs, POSIX-relative to the repository root. A task may modify **only** these paths.
`X-04` rejects any write scope reaching the framework-protected set — `.ai/core/**`,
`.ai/*.md`, `spec/**`, `framework/**`, `project/FROZEN.md`, `project/approvals/**`,
`project/ledger/**` — which `AGENT-CONTRACT.md` §Prohibition, `LAW-01` and the
`partitions` write-access rules already forbid.

#### Authority grants

A lawful reach into that set — Compiler Stage 6 must write `core/MANIFEST.lock` — is
declared, never assumed:

```yaml
write_authority:
  paths:       [.ai/core/MANIFEST.lock]   # exactly what is granted, nothing wider
  id:          L7                          # the token the authority is recorded under
  recorded_at: .ai/FRAMEWORK.md            # where it is recorded; must exist
  citation:    <prose>
```

`role_authority` takes the same shape over `roles`, for dispatching a role that
`ROSTER.md` marks UNASSIGNED under a higher-ranked instruction.

**Why the shape is this strict.** `VER-009` raised the same defect twice — once against
`write_authority`, once against `role_authority` after it was introduced: *a control whose
exemption is written by the party it constrains and validated only for shape.* Its closing
judgment is the specification: **until a citation resolves against an approval, decision
record or ledger entry, these fields record an intention rather than establish an
authority.** So `recorded_at` must exist and must actually contain `id`. A grant may not be
wider than the scope it qualifies, and every granted reach is printed as a notice on every
run — an exemption nobody sees is not an exemption, it is a hole.

**This does not make a grant unforgeable, and forging one needs less than writing both
files.** `id` is matched as a substring of any *readable* file, so a forger needs the task
record it already writes plus any file that happens to contain the token: three of the
four forgeries `VER-009` FIND-Q9-22 landed cited files the forger does not write, one of
them reading a prohibition as the authorization for the thing it prohibits. What the shape
buys is that a grant is *inspectable*: the reviewer is pointed at the artifact that is
supposed to carry the authority, and its absence there is a check failure rather than a
matter of trust. Every version of this control has checked that a citation has a **form**,
never that it has a **referent**; closing that is `F-007`, escalated to
`chief-systems-engineer` and open. §14 item 5 carries the detail.

### 5.3 · `observes` — the observation surface

The **observation surface** is the tree state a task must observe *stably* for its
acceptance criteria to remain valid. It is not the read scope: a verifier that reproduces a
producer's suite reads no file it writes, yet its evidence is worthless if the suite moves
while it runs. Two tasks can therefore contaminate each other's evidence without either
writing what the other reads — the `write/observe` hazard class in §7, distinct from
`write/write` and `write/read`.

**It is mostly derived, not declared.** `graph.observation_surface` unions three terms
computed from records already present:

`write_scope` ∪ deliverable entries that resolve to real paths today ∪ every path pinned in
the `deliverables` of each consumed result.

The third term is the one no task states about itself: a consumer never names those paths,
the *result it consumes* does, and they are exactly the paths its conclusion depends on.
`observes` is the optional fourth term — **only the residue the derivation cannot reach**,
such as a suite named in prose inside `acceptance_criteria[].test`. A record that declares
nothing still has a surface; declaring is not what creates it.

What is *undeclared* stays undetectable. The repository holds no execution trace, so
`graph.undeclared_observation` can only notice that a `test` string names a tree-reading
command (`pytest`, `git status`, `git diff`, `python -m`) while the record declares no
`observes`. That is a heuristic notice, printed by `X-07`. It is not a claim that an
undeclared observation was found, and its absence is not a claim that none exists.

## 6 · The result record

```yaml
result_id:    R-nnn
produced_by:  {task: T-nnn, role: <registered role>, session: S-YYYY-MM-DD-nn}
status:       CURRENT | STALE | SUPERSEDED
supersedes:   R-nnn | null
inputs:       [{path, digest}]        # DC-1 of every input, pinned at publication
deliverables: [{path, digest}]        # DC-1 of every output, pinned at publication
validation:   [{check, outcome}]
conclusion:   |                       # the consumable payload
findings:     [{id, severity, statement, owner}]
```

**What may be pinned, and what may not.** Pins are for artifacts that are *settled* when the
result is published. Two classes must stay out, both learned the hard way:

| Never pin | Why |
|---|---|
| A deliverable of a task that **consumes** this result | The consumer's own output would stale the result it depends on. `R-007` pinned `VER-009`, which is `T-004`'s deliverable; `T-004` filing its report immediately staled `R-007` and blocked `T-004` on itself |
| A **mutable register** — task records, `EXEC.md` | Pinning the backlog freezes it. `R-007` pinned six task records, so no task could change status without first superseding the result |

`conclusion` is the point of the whole architecture. A downstream task declares
`consumes: [R-nnn]` and reads **the conclusion**, not the upstream task's inputs and not
its conversation.

### 6.1 · Immutability without new machinery

A result pins the DC-1 digest of every input **and every deliverable** at publication.
`X-06` recomputes them against the working tree:

- all match — result is **CURRENT**, consumers may proceed;
- any differs — result is **STALE**, and every task consuming it becomes **BLOCKED**.

This is `DC-2`'s construction applied to a result's input set, and `LAW-10`'s
content-hash binding applied to a result instead of an approval. Nothing is invented.
Correction is by **supersession**, never by mutation: a new record sets
`supersedes: R-nnn` and the old one moves to `SUPERSEDED`.

At supersession the successor pins `supersedes_seal: {path, digest}` — the DC-1 of the
predecessor's whole file, taken **after** the predecessor's own closing edit. From then on
any edit to the predecessor moves its digest and `X-06` raises
`REWRITTEN AFTER SUPERSESSION`. The evidence is in a different file from the one it
protects, which is the only reason it protects anything.

### 6.2 · The seal epoch — `S-2026-08-09-06`, declared

`R-001` and `R-007` are superseded by records published before the seal existed, so they
cannot be retro-sealed and must not be failed for it. The discriminator between history and
a present-tense omission is the **seal epoch**: a supersession published at or after it and
carrying no seal is an `X-06` failure on the successor; one published before it is reported
as a notice and never failed.

**The epoch is `S-2026-08-09-06` and it is a declared constant, `graph.SEAL_EPOCH`.** It was
derived — `min()` over the sessions of the records that carry a seal — until `VER-009`
`FIND-Q9-39` showed that a rule derived from the data it polices can be switched off by
editing that data. Removing the `supersedes_seal` block from `R-009`, `R-010` and `R-011`
emptied the derivation, and an empty epoch made the rule vacuous for all six records at
once: **`X-06` returned PASS with zero details after a three-record tamper.** A constant
cannot be emptied by editing records.

The value's authority is `R-009.produced_by.session` as published — `R-009` carries the
first seal in the chain, over `R-008` — independently recomputed and matched in `VER-009`
§26. It is recorded here as well as in code so that advancing it is a reviewable act in two
places. The old derivation is retained as **evidence only**, as `graph.derived_seal_epoch`,
and `X-06` prints a notice whenever the two disagree: a derivation earlier than the constant
means the constant is late, and one that has emptied while sealed supersessions existed
means seals have been removed.

What the seal guarantees, exactly, since an earlier version of this control claimed more
than it delivered: **per link, once a seal exists**, no edit to the predecessor can reduce
the alarm. **Not across the chain** — the evidence lives in the successor, which a party
editing the chain is already editing, so deleting a successor's seal deletes that link's
alarm along with its failure. What no longer follows is the collapse of every other link.

### 6.3 · The link is declared twice, and both declarations are read

**`VER-009` `FIND-Q9-43`.** Pinning the epoch hardened the *discriminator* and left the
*trigger* under the tamperer's hand. The seal rule is guarded by `if result.supersedes and
not <seal>`, and `supersedes` is a line in a file the tampering party is already editing.
Deleting `supersedes: R-011` and its seal block from `R-012` — **two lines, one record** —
returned `X-06` to PASS with a single notice, after which appending `TAMPERED: …` to `R-011`
raised nothing at all. That is cheaper than emptying the epoch was.

The repository already held the contradicting evidence and discarded it: `R-011` carries
`superseded_by: R-012`, and every superseded record in this chain has carried the field
since `R-001`. Nothing parsed it. So a supersession is now confirmed from **both** ends:

| Records say | `X-06` |
|---|---|
| `A` declares `superseded_by: B`, and `B` declares `supersedes: A` **or** seals `A` | agreed — nothing raised |
| `A` declares `superseded_by: B`, and no record `B` exists | **FAIL** — a supersession names a record that can be read |
| `A` declares `superseded_by: B`, `B` exists and does **neither** | **FAIL** — the two records contradict each other; this is the `FIND-Q9-43` attack |
| `B` declares `supersedes: A` while `A` declares `superseded_by: C` | **FAIL** — two successors is no successor |
| `A` is superseded and declares no `superseded_by` | **notice** — the cross-check is blind for that link and says so. Requiring the field is a schema change (`LAW-12`) |

### 6.4 · One definition of a link — `graph.link_of`

**`VER-009` `FIND-Q9-51` and `FIND-Q9-52`.** The `FIND-Q9-43` repair above introduced its
own bypass, and a cheaper one. The cross-check was given a private predicate,
`checks._corroborates`, which accepted `supersedes` **or** a seal path naming the
predecessor, while `graph.successor_of` accepted `supersedes` alone. **One relationship,
two definitions** — and the gap between them was the attack:

> Delete one line, `supersedes:  R-012`, from `R-013`. Leave the seal block and its correct
> digest of `R-012` exactly where it is. The cross-check saw a link and stayed quiet;
> `successor_of` saw none, so `result_currency` took the *unsealed* branch. `X-06 PASS`.
> `R-012` was then rewritten with no alarm anywhere. **The digest that would have convicted
> the tamperer was in the repository and no code path compared it.** On an interior link
> (`R-011`/`R-012`, with a reseal) the same attack left no signal in check, campaign or
> suite.

`graph.link_of` is the single authoritative reading of a record's successor link, and it
reads **both** fields. `successor_of`, `supersession_seal` and `X-06`'s cross-check all
route through it, so the seal machinery and the check that polices it cannot hold different
beliefs about the same two records.

| Record asserts | Link | `X-06` |
|---|---|---|
| `supersedes: A` and a seal over `A` | `A` | agreed — the ordinary case |
| `supersedes: A`, no seal | `A` | epoch rule §6.2 decides: **FAIL** at or after the epoch, notice before it |
| A seal over `A`, no `supersedes` | `A` | **the link stands.** The seal is compared and a rewrite of `A` fires `REWRITTEN` |
| `supersedes: A` and a seal over `B`, `A ≠ B` | both | **FAIL** — one record, two different predecessors; which record it closed is underivable |
| A link to `A`, and no record `A` exists | `A` | **FAIL** — nothing was closed and no seal over it can be verified |
| Two records both assert they closed `A` | — | **FAIL** — competing successors; only one of their seals can be the seal that closed `A` |

The seal path must be exactly `.ai/project/results/R-nnn.md`. `_corroborates` matched on the
**basename**, which was tolerable while the match only confirmed a link something else had
established; it establishes links now, so `notes/R-011.md` mints none.

**And a seal may not name nothing quietly — `V-2`, `V-4`, then `F-1`…`F-4`.** Independent
verification found the rule above enforced by *silence*: the path was normalised for
backslashes and compared to a literal prefix, so several spellings of a **real, existing**
predecessor file resolved to no link and nothing reported it. Inserting two characters into a
seal path was a way to delete the seal limb while leaving a block that reads as a correct,
digested seal. **A second verification found the first repair had reproduced the same defect
one level in** — canonicalisation mapped a *declared* path to the empty string, and the check
read "canonicalises to nothing" and "nothing was declared" from the same value, so the whole
family `./ . .. / // ../.. ././ ./.` and whitespace-only skipped the check in silence. The
attack ran end to end on the real records at `X-06 PASS` with **zero details**.

Three rules close it. The third is the one both defects turned on:

- **Separator noise is canonicalised**, so a lawfully-spelled path is a link: `./`, `//`,
  interior `.`, backslashes and surrounding whitespace. Collapsing is confined to what cannot
  change *which file is named*.
- **`..` is not resolved and a leading `/` is not discarded** (`F-3`, `F-4`). Both *guess*:
  `../.ai/…` and `/.ai/…` name a file that depends on where the reader stands, and
  `…/results/R-101.md/../R-100.md` resolved to `R-100` while a reviewer reads `R-101.md`.
  The paragraph above refuses to guess at case; refusing for case and guessing for traversal
  in the same function was the inconsistency. They yield no link, and no link that is
  declared is silent.
- **Declaredness is read from the declaration, never from its canonical form** (`F-1`, `F-2`),
  and **never from a coerced one** (`G-1`). A `supersedes_seal.path` that is declared and
  names no result record is a **FAIL**; a seal block that declares no usable path is a
  **FAIL**; a block that is present but is not a `{path, digest}` mapping is a **FAIL**; a
  path naming a record that lives in a different file is a **FAIL**. Four functions, four
  questions: `graph.seal_block_raw` gives the value before coercion,
  `graph.seal_declared_block` answers *was a block declared*, `graph.seal_declared` answers
  *was a path declared*, `graph.seal_path` answers *what does it canonicalise to*, and
  `graph.seal_target` answers *what record does it name*.

**The defect was never strictness — it was that the strict answer was given without saying
so. That has now happened four times, at four different levels of the same value.** `F-1` was
a canonical form that meant both "empty" and "absent". `G-1` was a *coerced* form that meant
both "not a mapping" and "no block": `ResultRecord.supersedes_seal` returns `{}` for either,
and the guard read `bool({})`. Writing the seal in this repository's **own** `- path:` /
`digest:` sequence idiom — the shape every `inputs:` and `deliverables:` block already uses —
rewrote `R-013` on the live records at `X-06 PASS` with a detail set byte-identical to a clean
run, while `R-014` still displayed `R-013`'s correct published digest to a human reader.

So the claim this section is entitled to make is narrow, and is stated narrowly: **each of the
five questions above is now answered by its own function, and every negative answer is a
reported failure.** The stronger sentence that stood here — that the two fields cannot be
removed independently without one becoming visible, asserted as an *enforced rule* — has been
falsified twice by the two audits that followed it, once when it was an assertion and once
when it was thought to be enforced. It is not restated. What replaces it is §6.5: a control
whose evidence lives in mutable records the tampering party edits will keep producing this
shape of defect, and the answer is the ledger, not a fifth adjective.

`tests/test_exec_supersession.py` carries **78 tests** across three classes, the figure
`pytest --collect-only` reports and not an estimate:
`TestASealMayNotNameNothingQuietly` **40** — 1 control, 5 resolving spellings, 1 backslash
case named for pre-dating this repair rather than counted as evidence for it, 23 rejected
spellings across four families, the F-1 seam, 1 deleted-path form, 5 parses-to-nothing forms,
the not-accused converse, the end-to-end attack including the rewrite, and V-4;
`TestASealBlockThatIsNotAMappingIsNotNoSealBlock` **7**; and 31 in the M1–M10 negative suite.

**Why the seal limb is kept and not deleted.** Mutant `MU30` — deleting the seal-path limb —
survived the pass-6 suite, and the audit read that as evidence the limb should go. Deleting
it restores a **single-field** definition, which is the precondition of every one of the
four recorded disarms: one editable line, and the seal machinery goes blind. Unifying upward
instead makes the seal load-bearing — the field that carries the evidence is also a field
that establishes the link, so neither can be removed without the other becoming visible.
What was genuinely redundant, and is removed, is `_corroborates` itself: the *second*
definition.

`R-001` and `R-007` are untouched by this. They carry no seal, so their link is the
declaration alone exactly as before, and §6.2 still reports rather than fails them.

**Residual, measured rather than asserted.** A tamperer who strips `superseded_by` from the
predecessor *as well as* `supersedes` and the seal from the successor removes every
assertion that the link existed, and the records no longer contradict each other. What
remains is a record declaring `status: SUPERSEDED` with no successor anywhere — reported as
unsealed, not failed, because a record may be retired without a successor and deciding
otherwise is a schema question (`LAW-12`).

The cost of **that** attack is three edits across two files. The predecessor of this
paragraph asserted the same number while the true cost was one edit in one file, and no test
held the sentence to account. `tests/test_exec_supersession.py::TestTheResidualIsMeasuredNotAsserted`
executes it and requires the two-edit prefix to **fail**, so that route is pinned at exactly
three by a test rather than by a claim.

**It is not the cheapest route, and this section previously read as though it were — `V-3`.**
Two others are cheaper, both structural rather than repairable here, and both are named so
that no reader takes the number above for a floor:

| Route | Cost | Residue a reviewer could notice | Where it lives |
|---|---|---|---|
| Strip the back-link, `supersedes` and the seal | 3 edits, 2 files | a record declaring `status: SUPERSEDED` with no successor | §6.4, pinned by test |
| **Backdate the successor's session, strip the seal** | **2 edits, 1 file** | one live test red | §6.2 residual 2, unchanged |
| **Rewrite the predecessor, then reseal over it** | **2 edits, 2 files** | **none** | §6.5 — the structural residual |

The third is the honest floor: nothing seals the CURRENT record, because a seal is written by
a successor and the head has none, so a tamperer who edits a predecessor and updates the
successor's digest leaves no trace in this channel at all. No arrangement of fields *inside
the result channel* removes it — which is precisely the argument of §6.5, and the reason
Option B is recorded there as the direction rather than closed here.

All three are narrowings, not closures. The `§6.2` residual is unchanged by this pass.

### 6.5 · Structural future direction — ledger-anchored supersession integrity

**STATUS: FUTURE ARCHITECTURE DIRECTION — NOT IMPLEMENTED.** Recorded here as a decision
about direction, not as work performed. Nothing in this section is built, and §6.4 is what
the repository actually does today.

Four working disarms of the supersession control are on record across audit passes 6 and 7,
each closed by hardening a different field — the epoch, then the back-link, then the link
definition itself. The recurring cause is structural rather than a coding defect: **the
evidence that a result was not rewritten lives inside the set of mutable files the tampering
party is already editing.** §6.4 raises the cost of the attack and pins the residual with a
test; it does not remove that property, and no arrangement of fields *within the result
channel* can.

The repository already owns a stronger root of trust. `project/ledger/` is hash-chained,
carries `prev_hash`, seals segments every 500 entries and sequences durably (§10, `LAW-09`).
Supersession integrity should ultimately be anchored there rather than reinvented through
mutable result-record seals. **The result channel must not become a second, weaker ledger.**

This is **not** authorised for implementation and must not be implemented incidentally. It
requires, at minimum:

- the appropriate **Class-C / A4 authority path** — a control disarmable by the party it
  polices is a framework question, not a coding one, and `VER-009` escalated it as such;
- lawful ledger initialisation, `genesis` → `active`;
- an **approved construction** for `L-0000001` — not an invented one;
- a migration and compatibility plan for the existing records `R-001`…`R-013`.

Until that authority exists: no ledger entry is created, `HEAD` stays at `seq: 0`, state
`genesis`, and the ledger hash construction is not invented here or anywhere else.

## 7 · Classification — computed, never declared

`src/aief_exec/graph.py` derives the class of every task and every task pair. No human
records a classification, so none can go stale.

| Class | Rule |
|---|---|
| **BLOCKED** | the task's `role` is UNASSIGNED in `ROSTER.md` without a grant, **or** any `depends_on` task is not COMPLETE, **or** any consumed result is missing or STALE, **or** any `blocked_by` id is open in `OPEN_ITEMS.md` |
| **SERIAL** (A before B) | B reaches A through the transitive closure of `depends_on` |
| **CONFLICT** (A, B) | write scopes intersect (`write/write`), **or** one's write scope intersects the other's **read surface** (`write/read`), **or** one's write scope intersects the other's observation surface (`write/observe`, §5.3) |
| **PARALLEL** (A, B) | neither is BLOCKED, no serialising edge either way, and no conflict |

**The read surface is every component of `acquisition`, not `mandatory` alone.** The task's
own record, its mandatory *and optional* read scope, and the record of each result it
consumes. `VER-009` `FIND-Q9-38` traced four independent hazard escapes to one asymmetry:
the cost model in §11 enumerated five surfaces while the hazard model compared three, so a
task was charged for reading files no comparison would defend. The auditor's matched-pair
control was decisive — the same path declared `optional` classified PARALLEL and declared
`mandatory` classified CONFLICT, with nothing else different. Live, `T-001` holds
`.ai/project/tasks/**`, which covers the contracts `T-002` and `T-005` are executing, and
both pairs classified PARALLEL while `X-08` charged those same files under `record`.

`graph.read_surface` and `scope.charged_context` now read one enumeration,
`scope.acquisition_units`, so a component added to the charge is compared in the same edit
and the asymmetry cannot return by editing one model. The taxonomy stays three tags wide;
which component carried the hazard is named inside the reason, so a rewritten contract is
distinguishable from a rewritten input without a fourth class to parse. **Two escapes remain
open**, disclosed in §14 items 10 and 11: runtime tooling a task imports but never declares,
and undeclared observation.

**Ordering of the pair classes.** SERIAL, then BLOCKED, then CONFLICT, then PARALLEL. A
blocked pair cannot be co-dispatched at all, so the block is the operative fact and it is
reported as the class — `FIND-Q9-41`, which found CONFLICT being reported for pairs no
dispatch could ever pick up. Nothing is discarded by the reorder: any scope reasons found
are carried inside the BLOCKED reason list, so the hazard is still readable and is still
there when the block clears. `COMPLETE` is deliberately **not** treated as a pair-level
block: that state never clears, so classing such a pair BLOCKED would bury a live hazard
permanently. `runnable()` already keeps COMPLETE tasks out of every dispatch group.

**Dispatch groups are first-fit greedy, not maximal.** `Plan.parallel_sets` forms groups in
identifier order, so a later task can be excluded from a group it would fit. `FIND-Q9-40`:
the docstring claimed "maximal", which is maximum-clique-cover and NP-hard, and the payoff
would be a larger batch rather than a safer one. Safety does not rest on it — every group is
pairwise PARALLEL by construction and `X-07` re-verifies each group pairwise from the plan.

**BLOCKED is never read from a record.** It is derived on every run, so a record that
declares a block it does not have is as visible as one that omits a block it does have.
`X-02` fails if the declared status and the derived state disagree in either direction.

Intersection expands each glob against the working tree and intersects the concrete path
sets; when that is empty, a **witness test** decides whether the patterns could ever name a
common path, so paths that do not yet exist are still caught. The witness respects glob
semantics — `**` spans a separator, `*` does not — which a literal-prefix test does not:
`.ai/*.md` and `.ai/project/EXEC.md` share the prefix `.ai/` yet no path satisfies both.

**Blocking is a state; scope independence is a property.** They are computed separately and
must not be conflated. Two tasks with disjoint scopes stay scope-independent while one of
them is blocked — the pair simply is not dispatchable yet.

## 8 · Checkpoint, interruption and the decision pause

`checkpoint` is written as work proceeds, not only at close. `WF-01`'s ROLLBACK rule —
*"an abandoned session leaves the repository exactly as it found it"* — is preserved for
`STATE.md` and the ledger; the checkpoint records progress **inside the task record**, which
is instance data the rule does not govern.

Resume is: read `EXEC.md`, read the one ACTIVE record, skip everything in
`checkpoint.completed`, continue at `checkpoint.next_action`. Completed discovery is not
repeated.

A human authority boundary sets `status: AWAITING-DECISION` and populates
`checkpoint.decision` with id, question, options and recommendation. **The task is not
terminated.** When the decision is recorded in `resolution`, status returns to ACTIVE and
work continues from `checkpoint.next_action`. Only a decision that invalidates prior work
causes any of it to be redone.

## 9 · QA handoff

`LAW-05` and the `duty_conflicts` model are unchanged: `qa.verifier_role` must differ from
`role`, and `ADP-claude-code` requires subagent dispatch for a cold context.

What changes is the **evidence**, not the independence. The verifier receives the task
record and the result record. `result.affected` is the changed set, `result.inputs` are the
digest-pinned preconditions, `acceptance_criteria` are already binary per
`TPL-task-package` §6, and `result.validation` names the checks run. The verifier
re-executes the criteria against those paths.

QA no longer rediscovers scope by reading everything. Independence is preserved because the
verifier verifies against **declared criteria and pinned digests**, not against the author's
account of the work.

## 10 · Communication and the ledger

Task and result records are the durable channel and are sufficient on their own — they are
files, so a cold session recovers them without any conversation history.

The ledger remains the transaction log. When the first session close is lawfully performed,
a task state transition and a result publication are ledger-entry payloads. **No ledger
entry is written by this architecture**; `HEAD` stays at genesis, `seq: 0`.

## 11 · Context budget

Counts are exact, from the pinned tokenizer artifacts; when a family is unavailable the
budget is reported UNMEASURED and never estimated, matching the fail-safe rule in
`src/aief_stage6/tokenizers.py`.

**Three quantities, reported separately and never silently summed.** One number cannot gate
a dispatch when part of it only exists *after* the dispatch: `T-005` charged TF-1 1,411
against a cap of 1,500 before it ran and 7,161 after, because its own new deliverable became
chargeable the moment it was written. A gate whose verdict depends on whether the task
already ran is not a gate.

| Quantity | Components | Treatment |
|---|---|---|
| **`acquisition`** | record + mandatory + optional + dependency | Everything the task must hold before it can start. **A dispatch-time measurement, not an invariant** — see below. **This is what `context_budget.tf1`/`.tf2` gate.** |
| **`revision`** | deliverable paths that already resolve | Real cost — an artifact being rewritten must be read — but not a precondition, and **non-monotonic** wherever the path lies inside the task's own write scope. Not gated, and **not invisible**: it is bounded by `total_measurable` below. |
| **`total_measurable`** | `acquisition + revision` | Everything this layer can count. Compared against the **same** declared cap, by **`X-10`, a check of its own** — a breach is an `X-10` failure and never an `X-08` one. |
| **`telemetry`** | command results, diffs, test logs | **Unmeasurable from the repository, which holds no execution trace. Explicitly excluded from every figure and never estimated.** Not small — a prior session measured its own telemetry overrun at roughly 52% of a task cap. Representing it as unmeasurable rather than as zero is the only honest option available here. |

**The gate is not invariant across the task's own execution, and this document said it was.**
`VER-009` `FIND-Q9-36` falsified the claim that stood in this table. `record` is an
`acquisition` component and `TPL-task-package` requires every task to update its own
checkpoint as it works, so wherever a task's record lies inside its own `write_scope` the
gated figure moves under the task's own hand: a synthetic task measured TF-1 542, then
**1,328 — +145%** — after appending one progress note to its own checkpoint. Live, 34% of
`T-001`'s gated figure and 24% of `T-002`'s are self-written, and `T-002` is a live `X-08`
failure on a number it moves itself.

What is true is narrower and is what is now claimed: the figure is **exact and reproducible
at the moment of dispatch**, and it does not move when the task's *deliverable* is created —
the channel the split was built for. It moves when the task edits a charged path it also
owns. `X-08` therefore reports every task as `acquisition = stable + self-referential`, both
figures visible, and attributes each moving path to the component that holds it. `record` is
**not** dropped from the gate to buy invariance: an agent must read its contract, and
removing real cost to make a number behave is the defect, not the repair.

**Why `revision` is bounded rather than gated or ignored.** `FIND-Q9-37` measured the
excluded `revision` at 53% of `T-004`'s measurable input, 85% of `T-001`'s and 80% of
`T-005`'s — figures that move, because two of those three artifacts are audit files that
grow as they are written, so run `aief_exec scope T-nnn` rather than citing them. For
`T-004` the excluded item is the verification report its own `AC-4` makes mandatory reading.
A cap bounding under half of an agent's required input is not a budget. Folding `revision`
into the gate would restore the non-monotonicity the split removed, so instead
`total_measurable` carries its own verdict against the same declared cap, its breach is a
**failure and not a notice**, and every such row is labelled `NON-MONOTONIC BOUND, not the
acquisition gate`. Re-setting the caps against the whole input is a `project-manager`
decision and is not taken here.

### 11.1 · Two quantities, two checks — `X-08` and `X-10`

**`VER-009` `FIND-Q9-45`.** The bound above used to be a *second verdict inside `X-08`*,
against the same cap, appended to the same `details` list. Since `total_measurable ≥
acquisition` always, `X-08` then failed **if and only if** some task's `total_measurable`
breached: the gate contributed nothing to the check's boolean that the bound did not already
contribute, and the only thing separating the two kinds of row was the English substring
`NON-MONOTONIC BOUND` inside a detail string. A human could tell them apart. A consumer of
`X-08["status"]` could not.

The consequence was live, and it was the defect the `acquisition`/`revision` split had been
built to retire, reinstated one level up at the check's verdict:

| Working-tree state | `X-08` rows for `T-005` |
|---|---|
| `tests/test_stage6_crash_trials.py` — `T-005`'s own deliverable — **absent** | **none**: gate TF-1 1,411 ≤ 1,500, bound 1,411 ≤ 1,500 |
| the same file **present**, i.e. after `T-005` did its job | **two FAILs** on `total_measurable`, gate still under cap |

So the bound is now **`X-10`**, a separate check with a separate verdict:

- **`X-08` — the dispatch gate.** Fails iff an `acquisition` figure breaches. Monotone with
  respect to deliverable creation, which is the property a dispatch gate has to have.
- **`X-10` — the bound.** Fails iff a `total_measurable` figure breaches. **Non-monotonic**,
  and the check's own name and docstring say so.

Both may fail independently, and `row["id"]` tells a machine which did. Neither cap changed
and no measurement changed; only the boolean each quantity feeds. There is deliberately
**no suppression** of the `X-10` row where `revision` is zero: the rows are in different
checks now, so nothing is double-reported, and suppressing would have made `X-10`'s verdict
a function of whether `revision` happened to be zero — which is itself the non-monotonic
quantity. Where `revision` is zero the two figures coincide and `X-10`'s row says so.

That both are compared against the **same** declared cap remains a `project-manager`
question: the repository declares one `context_budget` per task and no second bound, and
inventing one here would be resolving an ambiguity by assumption (`LAW-12`).

### 11.2 · A path declared as both a read entry and a deliverable

**`VER-009` `FIND-Q9-49`.** The gate's headline property — `acquisition` does not move when
the task creates its own deliverable — was **true of this tree and not of the model**.
Charged units are deduplicated by `(path, anchor)` keeping the **first**, and acquisition
units are built before deliverables, so a path declared as both was charged into
`acquisition` and never reached `revision`. The gate then moved on exactly the channel the
split exists to close. Measured on a synthetic task declaring
`deliverable: [out/shared.md]` and `optional: [out/shared.md]`: `X-08` **FAIL → PASS** on
creating that file, `acquisition` 251 → 855 with `revision` 0 throughout; at a cap of 400,
249 → 853, **+243 %**. The declaration is lawful — a task that revises a file it must also
consult is ordinary — and the overlap happened to be empty for all six live tasks, which is
the only reason the invariance measurement held. Nothing asserted it was empty and no check
reported one.

**The rule.** Attribution is decided from the declarations, not from build order: a declared
deliverable is the task's **own output**, whether it exists at dispatch is the task's to
decide, and a quantity the task decides has no business inside a dispatch gate. On a shared
path the `deliverable` classification wins, and the unit is charged to `revision`.

Three properties, each covered by
`tests/test_exec_scope.py::TestSharedReadAndDeliverablePathIsCharedToRevision`:

- **The unit is charged exactly once.** `total_measurable` — and therefore `X-10` — is
  unchanged to the token. The repair moves a cost between named quantities; it creates,
  destroys and duplicates none.
- **The overlap is reported.** A notice names every shared path and the component it came
  from, so an overlap is never silent — `FIND-Q9-49`'s second limb.
- **The hazard model still sees the path.** `acquisition_units` is the enumeration
  `graph.read_surface` compares (`FIND-Q9-38`), and the path remains in it, so a writer of
  that path is still a `write/read` hazard. The cost model's attribution and the hazard
  model's surface are different questions and stay that way.

Re-measured after the repair on the audit's own counter-example: `acquisition` delta **0**
at both caps; `X-08` PASS → PASS; `X-10` PASS → FAIL at a cap of 400, which is the
non-monotonic bound behaving as §11.1 says it must.

## 12 · Execution checks — the `X` namespace

`V-01`…`V-25` is the manifest's namespace and adding to it would require an amendment.
These checks are separate, project-scoped and implemented in `src/aief_exec/checks.py`.

| ID | Verifies |
|---|---|
| X-01 | Records parse and carry the `SCH-task` required fields plus the extension fields; roles are normalised and both `role` and `qa.verifier_role` resolve in `ROSTER.md`; `LAW-05` verifier distinctness |
| X-02 | `EXEC.md` and `tasks/` are bijective by identifier, the index conforms to the AMD-49 grammar, and declared status agrees with derived state in both directions |
| X-03 | Every mandatory and optional read-scope entry resolves; no anchor is ambiguous; no entry falls inside the task's own forbidden reads |
| X-04 | No write scope reaches the framework-protected set without an enumerated, recorded grant; every granted reach is printed as a notice |
| X-05 | The task graph is acyclic; every `depends_on`, `consumes` and `produces` target exists |
| X-06 | Every CURRENT result's pinned input **and deliverable** digests match the working tree; a CURRENT result pins at least one deliverable; every supersession from the declared seal epoch onward carries a matching `supersedes_seal`, per §6.2; **the two records' declarations of a supersession agree** — a record declaring `superseded_by: B` while `B` neither declares `supersedes` of it nor seals it is a failure, per §6.3; **one record may not assert two different predecessors, two records may not assert the same one, and no link may name a record that does not exist**, per §6.4 |
| X-07 | No two concurrently-runnable tasks conflict on write, read or observation — the three hazard classes of §7, over the full read surface; undeclared observation is noticed, per §5.3 |
| X-08 | **The dispatch gate.** A task's `acquisition` is within `context_budget`. Monotone with respect to the task's own deliverable; `revision`, `total_measurable` and `telemetry` are reported by it and gated by it never, per §11.1 |
| X-09 | **Publication reachability, both directions.** Every `produces: R` has a lawful write path to `.ai/project/results/R.md`; **no `write_scope` reaches an `R` the task does not declare in `produces`**; every `consumes: R` names a result some task produces; no two tasks produce the same `R` |
| X-10 | **The non-monotonic bound.** A task's `total_measurable` (`acquisition + revision`) is within the same declared cap. Its verdict **moves when the task writes its own deliverable** — that is a property of the quantity and the reason it is not the gate, per §11.1 |

Checks emit **failures** and **notices**. A notice records something a reviewer must see
even when the check passes — a granted reach into the protected set, a role dispatched
while UNASSIGNED. Both are printed by `aief_exec check`.

## 13 · The agent's procedure

```
BOOT B1-B9                                     4,306 TF-1 tokens, unchanged
  |
READ project/EXEC.md                           bounded index, one line per task
  |
READ the one assigned tasks/T-nnn.md           the whole contract, one file
  |
RESOLVE read_scope                             anchors -> excerpts, cost measured
  |
READ consumed results' conclusions             never the upstream inputs
  |
CLASSIFY                                       PARALLEL | SERIAL | CONFLICT | BLOCKED
  |
EXECUTE inside write_scope                     X-04 and X-07 bound it
  |
CHECKPOINT as work proceeds                    interruption costs nothing already done
  |
PUBLISH results/R-nnn.md                       conclusion + pinned input digests
  |
QA verifies from the record                    cold, independent, no rediscovery
```

## 14 · Limits

1. **Enforcement is by tooling and tests, not by a manifest check.** Option A adds no
   `V-xx`. `X-01`…`X-10` run from `src/aief_exec/`; nothing in the boot sequence compels
   them. Promotion to a manifest-registered check is available without rework and would
   require an amendment and a recorded approval.
2. **Read scope is advisory to the agent and auditable after the fact.** The host cannot
   intercept a read, so `X-03` and `X-08` bound what a task *declares* it needs; a
   discrepancy is detectable in review, not preventable at the call. `VER-009` confirmed by
   instrumenting `Path.read_text` that `aief_exec brief` itself opens 21 files and walks the
   tree to build a plan. **The brief it emits is bounded; the tool that builds it is not.**
   What an agent loads is the brief.
3. **The conflict test stays conservative for paths that do not yet exist**, as §7 states.
4. **Parallel dispatch is bounded by the global session lock at B4a.** Classification is
   sound and host subagents give isolated contexts, but `LAW-09`'s single-writer
   transaction over `STATE.md` still serialises session close. Concurrent dispatch is safe
   for tasks whose write scopes exclude `STATE.md` and the ledger; `V-15` remains
   unimplemented under `CMP-BLOCK-005`.
5. **A grant is inspectable, not unforgeable — and forging one needs less than it sounds.**
   `recorded_at` must exist and carry `id`, but `id` is matched as a **substring of any
   readable file**. `VER-009` FIND-Q9-22 landed five working forgeries of `.ai/core/**`
   using only the task record: a one-character `id`; the two-character `L7` the live T-006
   grant uses; a token quoted inside the audit report that condemned it; and
   `id: Never edit` cited to `CLAUDE.md`, where that string occurs only inside
   *"Never edit `.ai/core/**`"* — **a prohibition read as authorization for the thing it
   prohibits.** An earlier draft of this clause said forgery required writing both the task
   record and the cited artifact. That was wrong, and wrong in the direction that makes a
   reviewer under-weight the risk: three of the four successful forgeries cited files the
   forger does not write. Every version of this control so far has checked that a citation
   has a **form**, never that it has a **referent**. Closing that is a
   `chief-systems-engineer` decision, recorded as a finding rather than taken here.
6. **`X-01` cannot see session identity**, which is half the `(role, session)` pair
   `AIEF-AMD-008` §AMD-20 makes decisive for independence. It verifies role distinctness
   only; a same-session verification is not detectable here.
7. **`scope.attribute` is atemporal.** It attributes a working-tree change to any task whose
   write scope covers the path, including a task that has not started. It answers *which
   scope permits this change*, never *who made it*.
8. **Pinning secures bytes, never claims about them.** A digest fixes what a file contained;
   it says nothing about whether a number written *inside* the result is true. `VER-009`
   found `R-007` stating a test count that was already wrong when written, with every pinned
   digest matching.
9. **Open decision A4 — does `produces` carry a write grant?** Whether
   `produces: [R-nnn]` implicitly grants write access to `.ai/project/results/R-nnn.md`, or
   whether that path must be declared in `write_scope` like any other, is **undecided**.
   `X-09` currently fails every task whose `produces` has no matching `write_scope` pattern,
   which is the live state of `T-002`…`T-006`. `records.TaskRecord.effective_write_scope`
   computes what the implicit grant would be and `X-09` prints it as a notice, marked
   `DERIVED, NOT GRANTED`: it is **computed and displayed, never enforced**. `X-04` keeps
   testing the declared scope alone. Until A4 is decided neither repair may be taken
   unilaterally — widening `write_scope` presumes the grant, and dropping `produces`
   discards the contract — so the check is left failing and the decision is owed by
   `project-manager`.
   `project-manager`. **`X-09` now also fails the converse** — a `write_scope` that reaches
   a result the task does not declare in `produces` — which is `FIND-Q9-42` and fires live
   on `T-001` over `R-002`…`R-006`. That mode reports the reach and does not decide A4
   either: its repair names both declarations and prefers neither.
10. **Runtime tooling a task imports is on no declared surface.** `FIND-Q9-38` E4, open and
    live. `T-002` writes `src/aief_stage6/**`, which holds `tokenizers.py`, the backend
    every token figure `T-004` reports flows through — `scope.py` imports it — and no
    declared scope of `T-004` names it, so `classify T-002 T-004` is PARALLEL and `T-002`
    may replace the instrument `T-004` measures with, mid-measurement. Closing it means
    deriving an import graph, which is a different kind of artefact from a declared scope
    and a different decision from widening a comparison. Recorded, not taken.
    `graph.read_surface` states the same residual where a reader of the code will meet it,
    and `tests/test_exec_graph.py::TestReadSurface` asserts it as a residual so that
    closing it later has to come here and say so.
11. **Undeclared observation stays undetectable**, as §5.3 states. `FIND-Q9-38` E5, and the
    one escape that is a genuine limit of the repository rather than of this layer: there
    is no execution trace, so what `pytest tests/` read is not recoverable.
    `graph.undeclared_observation` emits a heuristic notice and says it is one.
12. **`X-08` and `X-10` share one declared cap.** The repository declares exactly one
    `context_budget` per family, so the bound on `total_measurable` is compared against the
    same number as the gate on `acquisition`. That is deliberate under `LAW-12` — inventing
    a second cap here would be resolving by assumption — and it means a task can fail the
    bound while passing the gate, as `T-005` does. Setting caps against a measure that
    bounds the whole input is a `project-manager` decision, escalated jointly with
    `FIND-Q9-37` and not taken here.
13. **Any mutation score against `src/aief_exec/**` carries a kill floor of 3.** See
    §14.1 — subtract it before reading a result.

### 14.1 · The mutation kill floor — subtract 3

**`VER-009` `FIND-Q9-47`.** The current result record pins `src/aief_exec/*.py` and
`tests/test_exec_*.py` as deliverables, and three live-tree tests recompute those pins. A
**semantically inert** edit to any pinned source therefore kills three tests:

| Test | What it recomputes |
|---|---|
| `test_exec_checks.py::TestLiveRepositoryOpenFailures::test_x02_open_on_the_consumer_of_a_staled_result` | `X-02`'s derived state, which depends on the current result being CURRENT |
| `test_exec_checks.py::TestLiveRepositoryOpenFailures::test_x06_open_on_the_result_that_pins_the_layer_it_describes` | every pinned deliverable digest |
| `test_exec_graph.py::TestLivePlan::test_the_live_dependency_state_is_derived_end_to_end` | the plan's currency for the whole chain |

**This is not a defect and must not be "fixed".** Pinning the layer is the design: it is
what makes a change to `src/aief_exec/**` without republishing a *detectable* event rather
than a silent one, and it is the same mechanism §6.1 relies on. Removing the pins to make
mutation scoring tidier would trade a real control for a convenience.

What it does mean is that **every mutant's failure count starts at 3 and the floor must be
subtracted before the mutant is scored.** A mutant reported as "3 failures, KILLED" has in
fact **survived**: the three are the pin-drift tests and say nothing about the mutation.
`FIND-Q9-44`'s MU14 was found exactly this way. Two consequences for a campaign:

- Score against the failing test **names**, not only the count, whenever a mutant lands
  close to the floor.
- The suite cannot be green while the layer it guards is mid-repair, so a repair pass
  measures its own work at `3 failed` and only returns to zero when the successor result
  record is published with recomputed digests.

**Recomputing the floor** — do this whenever the pin set changes, and record the new value
here:

```
append "# inert" to any file the current result pins
PYTHONPATH=src python -m pytest tests/test_exec_*.py -q
revert
```

The failure count is the floor and the failing names are its membership. Measured for
`R-013` at session `S-2026-08-09-12`: **3**, the three tests above. It was also 3 under
`R-012`; the value tracks how many live-tree tests recompute the pins, not how many files
are pinned.
