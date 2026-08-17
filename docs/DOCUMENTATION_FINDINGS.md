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

## 3 · Stale cross-references in engineering documents — **NOT CORRECTED**

These are internal staleness in artifacts this pass does not own. None of them affects a
verified engineering property; each is a number or pointer that another artifact governs and
that has since moved.

| Artifact | Says | Authoritative value |
|---|---|---|
| `README.md` (previous) §Status | *"`ECR-D-014` **OPEN** — awaiting one fresh independent QA round"* | **CLOSED** — `.ai/project/OPEN_ITEMS.md` *Closed* section; closed by the fifth round at `f8ff028`. *(Corrected in the rewritten README.)* |
| `ENGINEERING.md` §1 | *"Repository release — Last tag **v0.10.0**"* | `v0.11.0`, applied at `f8ff028` |
| `releases/RELEASE_READINESS_v0.11.0.md` §1 | *"`origin/main` at `1c15818`"*; *"a clean clone runs **800 passed, 52 skipped**"* | `origin/main` is `f8ff028`; a clean clone runs **843 passed, 52 skipped**. **§2 of the same document already states 843** — the staleness is confined to §1's lead |
| `releases/RELEASE_READINESS_v0.11.0.md` §6 | *"**852** tests pass"* | **895** local |
| `releases/RELEASE_READINESS_v0.11.0.md` §2 | *"scan over all **583** tracked files"* | `git ls-files` → **597** tracked today. The scan's result is not disputed; its denominator has moved |
| `releases/RELEASE_READINESS_v0.11.0.md` §3 | *"**three** independent cold-context QA rounds"*; `CHANGELOG.md` [0.11.0] lead, same | **five** rounds — §5 of the same report tabulates all five. Both leads were written before rounds 4 and 5 ran |

**Pattern.** Every one is a *count or pointer restated in a second place*, which is precisely the
defect class `python -m aief_register` was built to forbid — *"no state register asserts a value
another artifact governs."* That check's scope is `.ai/project/STATE.md` and
`.ai/project/STATE_REGISTER.md`. The findings above sit outside its scope, in `ENGINEERING.md`,
`releases/**` and `CHANGELOG.md`.

**Suggested disposition (an owner/engineering decision, not a documentation one):** either widen
the register check's declared scope to cover release and index documents, or record explicitly
that narrative release documents are historical snapshots as-written and are not maintained
against later state. The second is defensible — a release report *should* describe the state it
audited — but it should be *stated*, because right now §1 and §2 of one document disagree.

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

## 6 · Rewriting `README.md` stales result record `R-030` — **DISCLOSED, NOT REPAIRED**

**Severity: blocks pushing this commit. Not an engineering defect — the mechanism working.**

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

**Why not repaired here.** The remedy is a superseding result record (`R-031`) recomputing the
sealed digests, with the ledger entry and session close that go with it. That is a governance act
under `EXECUTION_ARCHITECTURE.md` §6, requiring an assigned role — squarely outside a
documentation pass, and squarely inside what this pass was instructed not to touch.

**Consequence for publication.** `.github/workflows/validate.yml` runs `pytest tests/ -q` on every
push to `main`. Pushing this commit before `R-030` is republished would turn the published CI
signal red. **The documentation commit is therefore left local and unpushed**, which is the
finding's practical cost and the reason it is stated here rather than in a footnote.

**Owner action:** dispatch a session with a role assignment to republish `R-030` → `R-031` against
the new `README.md` digest, then push. Until then, `X-06` FAIL is expected and correct.

---

## 7 · Visual assets

No rendered images, screenshots or photographs exist in the repository; `portfolio/renders/`
contains only a `.gitkeep`. The available visuals are the **14 generated drawing sheets** (SVG
and PDF), which are genuine project artifacts and are used as such. **Nothing was fabricated,
and no stock or generic image was substituted.** What still needs manual capture is listed in
[`PORTFOLIO_ASSETS.md`](PORTFOLIO_ASSETS.md) §3.

The portfolio is textually and technically complete; it is **not visually complete** until a
shaded assembly render exists.
