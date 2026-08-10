# Project Gates

> **Instance artifact.** Emitted by aief-compile Stage 3 from `framework.manifest.json` and live repository state.
> Partition `project` — never touched by framework upgrade. Owner `project-manager`. Mutability mutable.

---

Profile `mechanical`. Gate topology **terminal**. Disposition is binary per `core/laws/LAW-03_release_gates.md`.

| Gate | Stage | Topology | Status |
|---|---|---|---|
| LC-M01-EXIT | Idea | terminal | PASSED |
| LC-M02-EXIT | Architecture | terminal | PASSED |
| LC-M03-EXIT | Specification | terminal | PASSED |
| LC-M04-EXIT | Implementation | terminal | **ACTIVE - BLOCKED** |
| LC-M05-EXIT | Verification | terminal | pending |
| LC-M06-EXIT | Validation | terminal | pending |
| LC-M07-EXIT | Release | terminal | pending |
| LC-M08-EXIT | Maintenance | terminal | pending |
| LC-M09-EXIT | Revision | terminal | pending |
| LC-M10-EXIT | Archive | terminal | pending |

## Active gate

`LC-M04-EXIT` (Implementation) is **BLOCKED** by ECR-D-001 through ECR-D-004 against the frozen specification.

A gate may pass with actions only if no action is on the critical path. All four defects are on it.

**Disposition, session `S-2026-08-10-01`.** All four ECRs are now dispositioned, approved,
applied and registered. The criteria are **computed, not asserted** — run:

```
PYTHONPATH=src python -m aief_gate
```

It prints one line per criterion with the evidence each rests on and exits non-zero unless all
seven PASS. **That command is the authority for this gate's status**, in preference to any
sentence in this file, because a sentence does not recompute itself. `C6` is the one criterion
that is not fully mechanical: the checker confirms a verification report exists and **declares**
each disposition as its subject, and that verifier identity differs from author identity, but
whether the verifier obtained its evidence itself is a `LAW-05` reading dispositioned in the
report. The checker says so rather than implying a judgement it did not make.

## Criteria

**Declared by the human owner (rank-1), session `S-2026-08-09-14`, option C.** Recorded by
`software.software-engineer` on that instruction; `project-manager` (A3) is UNASSIGNED in
[`ROSTER.md`](ROSTER.md) and the role gap is recorded rather than papered over. Criteria are
binary and evidence-based per `core/laws/LAW-03_release_gates.md`; the framework delegates
their content to this file (`core/profiles/mechanical/lifecycle/LC-M04_implementation.md`,
`core/profiles/mechanical/PROFILE.md` §Freeze points).

**Scope of this gate as declared.** These criteria constitute the **design-authority
precondition for SEWCP-200 CAD**: the frozen specification is coherent and every defect
raised against it is dispositioned, approved, applied and independently verified. See
*Deferred* below for what they deliberately do **not** cover.

| ID | Criterion | PASS | FAIL |
|---|---|---|---|
| **C1** | `ECR-D-001` carries an approved disposition | An ECR record exists, conforms to `SCH-ecr` with `disposition` non-empty, and a human approval artifact is content-hash-bound to it under `LAW-10` — **`LIVE` or `SUPERSEDED-VALID` per the supersession rule below** | Any of these absent, or the approval is **`VOID`** |
| **C2** | `ECR-D-002` carries an approved disposition | as C1 | as C1 |
| **C3** | `ECR-D-003` carries an approved disposition | as C1 | as C1 |
| **C4** | `ECR-D-004` carries an approved disposition | as C1 | as C1 |
| **C5** | The frozen specification reflects every approved disposition | Each disposition requiring a specification change is present in `spec/**` and the affected artifacts are re-registered in [`FROZEN.md`](FROZEN.md) with reproducing digests | Any approved disposition unapplied, or any registered digest that does not reproduce |
| **C6** | Independent verification is recorded per disposition | A verification report exists for each, produced by a role that authored none of the work, disposing every acceptance point `PASS`/`FAIL` on self-obtained evidence (`LAW-05`) | Report missing, or verifier identity equals author identity |
| **C7** | No ECR against the frozen specification remains undispositioned | The `Blocking` section of [`OPEN_ITEMS.md`](OPEN_ITEMS.md) contains no `ECR-D-*` whose `affected_artifacts` lie under `spec/**` | Any such item present |

### Supersession of approvals — ruled by the human owner, `S-2026-08-10-01`

**The problem this rule answers.** `LAW-10` clause 2 invalidates an approval when the bound
content hash changes, and an approval binds a **whole-file** DC-1. `spec/01` alone carries
dispositions for `ECR-D-001`, `-002`, `-003`, `-004`, `-007`, `-009` and `-010`. Under a literal
reading of the FAIL clause, **at most one of `C1`–`C4` could pass at any instant**, and which one
depended on edit order: `APR-019`'s lawful edit for `ECR-D-002` invalidated `APR-016`/`-017`/
`-018` and put `C1` into FAIL for a purely mechanical reason. The gate was unsatisfiable by
construction, and re-approving every prior ECR at each new digest is O(ECRs × edits) and breaks
again on the next edit.

**The rule.** An approval carries exactly one of three states against the live tree:

| State | Condition |
|---|---|
| **`LIVE`** | `subject_hash` equals the current DC-1 of `subject_path` |
| **`SUPERSEDED-VALID`** | an unbroken chain of approvals on the same `subject_path`, each carrying `prior_hash` equal to its predecessor's `subject_hash`, leads from it to a `LIVE` approval |
| **`VOID`** | neither |

`C1`–`C4` are satisfied by `LIVE` **or** `SUPERSEDED-VALID`. `VOID` fails.

**Why this is safe rather than a loosening.** The relation is stable under future edits — every
lawful change appends a link, so every earlier approval stays reachable — and it cannot launder
an unlawful one: an artifact edited without an approval leaves **no `LIVE` approval on that
path**, and the entire chain collapses to `VOID` at once. A fork (two approvals declaring the
same `prior_hash`) is a failure, not a preference, because it makes the approved history
ambiguous.

**It is computed, not asserted.** `python -m aief_approval verify` decides every state from
repository bytes and exits non-zero on any failure. `tests/test_approval_chain.py` attacks it
directly: unapproved edit, broken link, fork, cycle, self-reference, duplicate id, non-hex and
uppercase digests, registry/tree divergence, and a rollback that must re-`LIVE` an old approval
while voiding the later ones. **No `LIVE`/`VOID` label is written by hand anywhere** — four
hand-written liveness labels went stale in this repository before this rule existed (`VER-014`
R3-F1), which is why the approval artifacts now decline to state their own status.

`C1`–`C4` are **four separate criteria and are not satisfiable by one approval.** Each of the
four is an independent engineering decision owned by the Design Authority, and
[`OPEN_ITEMS_REGISTER.md`](OPEN_ITEMS_REGISTER.md) records all four on the critical path — so
`LAW-03` rule 3 forbids passing this gate with an action outstanding on any of them, and rule
4 forbids passing it by deferring one.

### Deferred — recorded, not omitted

`PROFILE.md` §Freeze points and `LC-M04_implementation.md` both fix the LC-M04 freeze point as
**"Design at LC-M04 exit"**. A criterion requiring the SEWCP-200 CAD to exist and be frozen is
therefore **derivable from the framework and is deliberately not adopted here**, by the
owner's decision: this gate is being used as the design-authority precondition for CAD, and
CAD is the work that follows it.

The consequence is stated plainly rather than left to be discovered: **clearing `C1`–`C7`
does not discharge the recorded freeze-point requirement.** That requirement stands and must
be met before the design is treated as frozen. Whether it is met by a later disposition of
this gate or by a separate checkpoint is an open `project-manager` / rank-1 question.

### Excluded — confirmed by the owner

`ECR-D-006`, `CMP-BLOCK-004`, `CMP-BLOCK-005` and `C-4` appear under `Blocking` in
[`OPEN_ITEMS.md`](OPEN_ITEMS.md) but are **not** criteria of this gate.
[`../../ENGINEERING.md`](../../ENGINEERING.md) records positively that *"Neither `ECR-D-005`
nor Stage 2 will unblock the `LC-M04-EXIT` gate. That gate is held by `ECR-D-001…004`"*, and
`ECR-D-006` is a framework-manifest defect whose class-D scope is the framework work it
affects, not the specification. Stage 6, `MANIFEST.lock` and `L-0000001` are excluded on the
same ground: no recorded criterion cites them.
