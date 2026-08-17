# Documentation Findings — portfolio pass, 2026-08-17

*Raised during the portfolio and documentation pass over `v0.11.0` (`f8ff028`). This pass had
**no authority to change engineering artifacts**, and it changed none. Each finding below is
recorded rather than repaired, except where the corrected artifact is itself a documentation
artifact this pass owns (`README.md`, `docs/**`) — those are marked **corrected here**.*

Verification method for every finding: the command or query is named. Nothing below is inferred
from a previous session's summary.

---

## 1 · Publication state contradicts the release language — **NOT CORRECTED**

**Severity: high for a portfolio; none for the engineering record.**

| Claim in the repository | Measured |
|---|---|
| `CHANGELOG.md` [0.11.0]: *"**The repository becomes public.**"* | `gh api repos/Raar1999/SEWCP_Master_Assembly` → **`"private": true`** |
| `releases/RELEASE_READINESS_v0.11.0.md` §2: *"GitHub — **PUSHED**, remote HEAD verified"* | confirmed: `git ls-remote origin HEAD` → `f8ff028…`, identical to local `HEAD` |
| Tag `v0.11.0` pushed | confirmed: `refs/tags/v0.11.0` present on the remote |
| — | `gh api repos/…/releases` → **`0`** — no GitHub **Release** object exists for any tag |

**Consequence.** `README.md`'s reproduction section instructs a reader to
`git clone https://github.com/Raar1999/SEWCP_Master_Assembly.git`. Today that succeeds only for
an account with access. The whole portfolio is unreadable by its intended audience until
visibility changes.

**Why not corrected here.** Repository visibility and Release-page creation are owner actions.
Neither is a documentation edit, and neither should be taken on someone's behalf.

**Owner action:** (a) set visibility to public, or accept that the portfolio is a private
artifact and share it another way; (b) optionally create a GitHub Release for `v0.11.0` — the tag
message is already written for it and states the physical-qualification boundary and
`ECR-D-016` explicitly.

---

## 2 · `README.md` clean-clone test count was stale — **CORRECTED HERE**

The previous `README.md` published **821 passed, 52 skipped** for a clean clone, and *"821 tests
pass there, 873 with the tokenizer artifacts"*.

Measured this pass by cloning `origin` into a scratch directory and running the suite:

| Environment | Measured |
|---|---|
| Clean clone at `f8ff028` | **843 passed, 52 skipped, 0 failed** |
| Clean clone + both tokenizer artifacts + `TRUST_ON_FIRST_USE.json` | **894 passed, 1 skipped, 0 failed** |
| Working tree | **895 passed, 0 skipped, 0 failed** |

`821 + 52 = 873`, which was the suite total *before* round 5 added 22 tests; the total is now 895
and the clone figure moved with it. `CHANGELOG.md` and `releases/RELEASE_READINESS_v0.11.0.md`
§2 both already publish **843**, so the README was the outlier. Corrected in the rewritten
`README.md`; the two engineering documents needed no change.

*(Round 5 had already corrected a different false claim in the same paragraph — "873 passed, 0
skipped", a condition nothing can produce. This is the neighbouring figure it did not reach.)*

---

## 3 · Stale cross-references in engineering documents — **CORRECTED, `S-2026-08-18-01`**

*Raised as `NOT CORRECTED` by the portfolio pass, then repaired by the governance closeout under
owner authority to make ordinary repository decisions. Each correction names its governing
source, and each superseded reading is recorded in the artifact it was corrected in rather than
discarded.*

None of these affects a verified engineering property; each is a number or pointer that another
artifact governs and that had since moved.

| Artifact | Said | Governing source | Verified value | Now |
|---|---|---|---|---|
| `README.md` §Status | *"`ECR-D-014` **OPEN** — awaiting one fresh independent QA round"* | `.ai/project/OPEN_ITEMS.md` *Closed* section | **CLOSED** at `f8ff028` by the fifth round | corrected in the rewritten README |
| `ENGINEERING.md` §1 | *"Last tag **v0.10.0**"* | `git tag`, `git describe --tags f8ff028` → `v0.11.0` | **`v0.11.0`** | corrected, with the superseded reading recorded in the cell |
| `RELEASE_READINESS_v0.11.0.md` §1 | *"`origin/main` at `1c15818`"* · *"a clean clone runs **800 passed, 52 skipped**"* | `git ls-remote origin HEAD`; a clone of `origin` run this pass | **`f8ff028`** · **843 passed, 52 skipped** — §2 of the same document already said 843 | corrected; superseded readings recorded in the header |
| `RELEASE_READINESS_v0.11.0.md` §2 | *"scan over all **583** tracked files"* | `git ls-tree -r --name-only f8ff028 \| wc -l` | **597** at the release commit. The scan's *result* is not disputed; its denominator was | corrected |
| `RELEASE_READINESS_v0.11.0.md` §3 | *"**three** independent cold-context QA rounds"*, *"two … `NOT CLEARED`"* | §5 of the same report, which tabulates the rounds | **five** rounds, **four** `NOT CLEARED` | corrected |
| `RELEASE_READINESS_v0.11.0.md` §6 | *"**852** tests pass"* | `pytest tests/ -q` at `f8ff028` | **895** | corrected |
| `CHANGELOG.md` [0.11.0] lead | *"**Three** independent … rounds"*, *"`ECR-D-014` is left **open**"* | §5 of the release report; `OPEN_ITEMS.md` | **five** rounds; **CLOSED** | corrected, with the superseded lead quoted beneath it |

**What was *not* rewritten.** The body sections of `RELEASE_READINESS_v0.11.0.md` and of
`CHANGELOG.md` [0.11.0] are as written at their rounds and are left so. Only the **leads and
summary cells that make a present-tense claim about the release being certified** were corrected
— a release report is entitled to describe the state it audited, but not to disagree with itself
about which release that is.

**Pattern, and it is the one this repository is organised around.** Every item is a *count or
pointer restated in a second place*, which is precisely the defect class
`python -m aief_register` was built to forbid — *"no state register asserts a value another
artifact governs."* That check's scope is `.ai/project/STATE.md` and
`.ai/project/STATE_REGISTER.md`. Every finding above sat **outside** its scope, in
`ENGINEERING.md`, `releases/**` and `CHANGELOG.md`.

**The residue, and it is not closed by correcting the values.** Correcting six restatements does
nothing to stop the seventh. The lawful successors are an engineering decision, not a
documentation one: either widen the register check's declared scope to reach release and index
documents, or declare narrative release documents to be historical snapshots that are not
maintained against later state. **The second is defensible and would have made five of these
non-findings** — but it has to be *stated*, because a reader cannot tell an intentional snapshot
from a stale cell by looking. Recorded here as owed; **not raised as a new open item, because
`OI-C-10` stands at 597 of a 600-token cap and this pass will not spend the last identifier on
its own finding.**

---

## 4 · Personal path present in tracked run records — **DISPOSITIONED, NOT A NEW FINDING**

Ten tracked CAD run records embed Python tracebacks containing the author's local Windows user
path (`C:/Users/<username>/AppData/Roaming/Autodesk/...`). This pass introduces no new instance
and removes none.

It is already dispositioned as **`DEC-21`: preserve** — *"they are tracked failure evidence and
redacting them would edit the record of what was observed"* — recorded so the owner can revisit
it deliberately. The release report's *"Secrets / PII: none found"* row is consistent with that
disposition: no secret, key or credential was found. A local username in a traceback is a
different category and is handled by its own decision.

**No secrets, API keys, credentials, tokens or private datasets were found** during this pass in
any file referenced by the new documentation.

---

## 5 · Genuine engineering defects — already open, correctly

Not findings of this pass. Listed so a reader of the portfolio can see they were not omitted:

| | |
|---|---|
| `ECR-D-016` | Support Ring isolation joint does not close. **Blocks hardware build.** Rev B revision required |
| `PVR-001` | 0 of 91 hardware-verifiable requirements verified |
| `OI-V-17` | four consecutive repair sessions each introduced a defect of the class they were repairing |
| `OI-C-10` | bounded open-items index at 597 of a 600-token cap; the next finding cannot be given an identifier |
| `CMP-BLOCK-004` / `-005` | gate AIEF framework Release 1.0.0 |

---

## 6 · Rewriting `README.md` staled result record `R-030` — **REPAIRED BY SUPERSESSION, `S-2026-08-18-01`**

**Not an engineering defect — the mechanism working, and then being answered the way the
architecture says to answer it.**

`README.md` is not merely a documentation file in this repository. It is a **pinned deliverable
of the CURRENT result record `R-030`**, which seals its DC-1 digest:

```yaml
result_id: R-030      status: CURRENT      supersedes: R-029
deliverables:
    …
    - path: README.md
      digest: be747001267a066a936e45500cc5120d66fe3c36cc0fd212eb33b41ae290f73f
```

Any byte change to `README.md` therefore moves that digest and marks `R-030` stale. Measured
after the rewrite:

```
$ PYTHONPATH=src python -m pytest tests/ -q
1 failed, 894 passed
  tests/test_exec_checks.py::TestLiveRepositoryOpenFailures
      ::test_x06_open_on_the_result_that_pins_the_layer_it_describes

  X-06 FAIL: R-030: declared CURRENT but is STALE
    deliverable README.md: DC-1 bde3fcf4…5639a != pinned be747001…f73f
```

**This is `X-06` doing its job.** Its stated purpose is to notice drift: *"move any file … without
republishing → the current record STALE → X-06 FAIL"*. A bare PASS there would be worth nothing.

**Isolated to the README alone.** With the original `README.md` restored and the whole of
`docs/**` present, `tests/test_exec_checks.py` runs **107 passed**. The new documentation tree
stales nothing; only the README rewrite does.

### The repair — `R-030` → `R-031`

Performed under `EXECUTION_ARCHITECTURE.md` §6.1: *"Correction is by **supersession**, never by
mutation."* Five acts, in this order, because the order is load-bearing:

| # | Act | Why it must come here |
|---:|---|---|
| 1 | Every content edit finalised first — `docs/**`, `README.md`, `ENGINEERING.md`, `CHANGELOG.md`, the release report | a pin taken before the last edit is stale the moment it is written |
| 2 | `T-009` declares `produces: … R-031` and adds `.ai/project/results/R-031.md` to `write_scope` | **X-09 mode 1**: a task that produces a record it cannot lawfully write is a failure. `T-009` is the producer of `R-022`…`R-030`, so the chain continues where it lives |
| 3 | `R-030`'s **closing edit** — `status: CURRENT` → `SUPERSEDED`, `superseded_by: R-031` | §6.3 requires the link to be declared from **both** ends. This is the only edit `R-030` receives, and it is the edit supersession consists of |
| 4 | `R-031` written, sealing `R-030` at the DC-1 it now stands at, with every input and deliverable recomputed against the finished tree | §6.1: the seal is taken **after** the predecessor's closing edit — the same construction `R-030` used over `R-029`, and `R-029` over `R-028` |
| 5 | Session record, ledger entry `L-0000007`, `HEAD`, `STATE.last_ledger_seq` | LAW-09 close. Written **after** `R-031` so nothing it pins can move underneath it |

**`R-030` is preserved.** It is not rewritten, not deleted, and its content is unchanged apart
from the two-field closing edit the architecture prescribes. From this point any further edit to
it moves its DC-1 away from `R-031`'s seal and `X-06` raises `REWRITTEN AFTER SUPERSESSION` — the
evidence living in a different file from the one it protects, which §6.1 says is the only reason
it protects anything.

**The DC-3 and DC-1 constructions were verified before use, not assumed.** DC-3 was reproduced
against both normative worked examples in `AIEF-AMD-008` §AMD-17 **and** against the live
`L-0000006` entry hash; DC-1 was reproduced against `R-030`'s existing seal over `R-029`. A
digest implementation that has not reproduced a known answer is not a digest implementation.

**Result:** `X-06` **PASS**. The check that correctly refused the portfolio commit now correctly
admits it, and it was neither weakened nor bypassed — `src/aief_exec/**` and
`tests/test_exec_*.py` are untouched by this pass.

---

## 7 · Visual assets

*Raised by the portfolio pass as "no rendered images exist"; **closed by the governance closeout**,
which found that they could be generated from repository evidence rather than captured by hand.*

`scripts/render_assembly.py` composes the released STL exports with the occurrence transforms
in `cad/runs/ASSEMBLY_S-2026-08-11-05/run.json` and produces a shaded isometric and an exploded
view. It is **derived evidence, not illustration**: every occurrence's transformed bounding box is
reconciled against the box Fusion observed before it is drawn, the deviation is printed, and
`--strict` refuses to render past tolerance. 18 of 19 agree to ≤ 0.072 mm; the coarsely
tessellated saddle deviates 3.864 mm inward while its mesh volume agrees to 0.018 %.

Two things this required getting right rather than guessing:

- **`z_axis_scale`.** Three of the six alignment pins are installed inverted and the record says
  so. Ignoring that field placed them 9.5 mm out — which the reconciliation caught, because it
  compares against observed state rather than trusting the transform.
- **Depth resolution.** The first attempt sorted triangles by centroid depth. Centroid order is
  not depth order for overlapping triangles of very different size, so the heater plate painted
  through the ESC puck's top face in visible grey spikes. Replaced with a per-pixel z-buffer,
  which is exact. The wrong version is described in the module docstring rather than quietly
  deleted.

**Nothing was fabricated, and no stock or generic image was substituted.** The remaining gaps —
including that these are tessellations rather than BRep surfaces — are listed at
[`PORTFOLIO_ASSETS.md`](PORTFOLIO_ASSETS.md) §3.
