# Independent QA

*Five cold-context rounds ran against this release. **Four returned `NOT CLEARED`.** This
document exists to say what they found, not to say that everything was fine.*

---

## 1 · The rule that makes it worth anything

**LAW-05 — no role verifies its own output.**

The failure mode this is aimed at is not dishonesty; it is that the party who repaired a defect
is the worst-placed party to judge whether the repair worked, because they will check for the
defect they were thinking about. So independence is supplied structurally:

| Requirement | How it is met |
|---|---|
| The auditor must not inherit the author's beliefs | a **cold context** that reconstructs every fact from the repository, with no conversation history |
| The auditor must not trust the audited code | it **recomputes** digests, aggregates and counts **without importing** `src/aief_stage6` or the module under review |
| The auditor must not become an author | it **writes no repository file**; it returns a verdict the repairing session did not choose |
| The verdict must be able to be "no" | it was, four times out of five |

Across five rounds, `qa-engineer` was assigned to **none** of the repairing sessions. Each
session record says so explicitly, and says which acts it *was* performing instead.

## 2 · Why QA is not decorative here

Four defect classes went unnoticed for many sessions in this project. **Every one of them was a
declared property with no standing check** — something a document asserted and no code computed.
Independent review is the only instrument that finds that class, because the tests were written
by the same reasoning that wrote the claim.

Two of the rounds' recomputations **contradicted the repository and were right**:

- the deliverables were **not** byte-identical to the generation root, though the record said so;
- the test suite did **not** pass from a clean clone — a clone got **35 failures** while the
  author's desk passed 846.

Both were corrected. The second produced `OI-V-16` and the GitHub Actions `validate` workflow,
whose stated purpose is written into the file: *"CI exists so that a claim in `README.md` is
falsifiable by a stranger, not so that a badge is green."*

---

## 3 · The five rounds

The subject was `ECR-D-014` — a framework ruling capping a boot-read token prefix at 200 tokens.
Small, dull, and exactly the kind of rule a release session could have quietly waved through.

| Round | Verdict | What it found |
|---|---|---|
| **1** | `NOT CLEARED` | Cleared `ECR-D-006`. Refused this one: **the ruling was enforced by nothing.** Three call-site mutations survived all **799** tests |
| **2** | `NOT CLEARED` | The round-1 repair was enforced **only on the preview path**. A mutation skipping the cap check when `canonical` is true survived all **846** tests, and the canonical build then wrote `MANIFEST.lock` with a **249-token prefix against a cap of 200**. Root cause: **no test had ever called `run()` with an `Authorization`** — the path that writes canonical bytes had no end-to-end test at all |
| **3** | `NOT CLEARED` | Enforcement **fully discharged** — it applied fifteen mutations, six of them new (deleting the post-condition, truncating so both derivations agree on a wrong region, returning early, clamping instead of raising, comparing the record to itself, exploiting the stub probe's leniency). **All fifteen die.** Refused closure on record accuracy alone |
| **4** | `NOT CLEARED` | **The check written to end a recurring defect did not catch that defect.** Its pattern was line-scoped and the defect's own phrasing spans two lines, so the *verbatim* historical defect passed all seven tests. Of nine phrasings tried, **2 caught, 7 evaded**. Its self-test was **circular** — validating the pattern against a string written for the pattern |
| **5** | **close** | Re-proved the substance again, and found the rebuilt check *still* incomplete: of **thirteen** phrasings, **twelve got past it** — including `last_ledger_seq: 2`, the field's own name, because there is no word boundary after an underscore. Seven of nine governing sections unscanned; the fenced YAML block that *is* the governed state skipped entirely; and one test still circular. **Recommended closure with named residuals** |

`ECR-D-014` was closed on round 5's own recommendation — a `qa-engineer` act, in a distinct cold
session. The closure basis names all five rounds.

## 4 · What the closure says, and what it does not

**Says:** the ruling is sound and was independently re-proved three times; its enforcement is
real and survived fifteen mutations plus six more; LAW-02 clause 5 and LAW-05 are satisfied
because **no session that repaired it certified its own repair, across four consecutive
attempts.**

**Does not say the repair sessions were clean. They were not.**

> **Four consecutive repair sessions each introduced a defect of the class they were repairing.**

That is a process finding, it is real, it is recorded at `OI-V-17`, and **it is not closed by
this release.** It is written into the release-readiness report and the session summary in those
words. Holding the ECR open a sixth time would have made it the carrier for a defect class it
does not own.

## 5 · Findings the rounds produced that were not about `ECR-D-014`

The rounds audited whatever they found, which is the point of not scoping them narrowly:

- **`LICENSE` §1 asserted the negation of the property the licence turns on.** A half-replaced
  edit left the sentence *"No tracked file falls in exactly one column"*, contradicting §1a in the
  same document. Round 4 caught it by classifying **every tracked file** and measuring 0 in
  neither column and 0 in both.
- **`LICENSE` §2's *"nothing in the set is copyleft"* was wrong** — `certifi` is MPL-2.0. The
  conclusion survived on the correct ground: nothing is vendored, modified or redistributed.
- **`TCR-002` has eight findings, three BLOCKING** — not six and two, as three artifacts said.
  `F-7` and `F-8` had been carried nowhere, dropped by `OI-V-14`, *the item raised to stop
  findings being dropped.*
- **A ledger entry's narrative body was the previous entry's prose with the identifiers
  incremented.** Every field covered by the digest construction is correct, the digest
  recomputes and the chain links — but the human-readable *account* described the wrong session.
  Because the artifact is append-only, **it was left standing, wrong, and annotated** rather
  than rewritten: *"A false account that is left standing and annotated is a smaller failure than
  a corrected one that leaves no trace."*
- **The `README.md` reproduction claim** — corrected twice, and it is corrected again in this
  pass (see [`DOCUMENTATION_FINDINGS.md`](DOCUMENTATION_FINDINGS.md)).

## 6 · The finding the process could not absorb

`.ai/project/OPEN_ITEMS.md` is a bounded index with a **600-token cap**, standing at **597**
against a marginal cost of about five tokens per identifier. Twice, a new open item was raised,
breached the cap, halted validation rule `V-09`, and had to be **withdrawn and folded** into a
row that already carried its class.

**Three findings in three sessions were denied an identifier of their own.** Each fold is
defensible on the merits and each is recorded as **budget-forced rather than chosen** — because
a register that merges findings to stay inside a cap has stopped being a register of findings.

That is `OI-C-10`, and it is honest about being unsolved: no session-level action remains, the
lawful successors are named at the row, and it is now blocking *the next* finding.

---

## 7 · What a reader should take from this

Not *"QA passed."* It mostly did not.

The claim is narrower and more defensible: **an adversarial reviewer, given the repository and
nothing else, was able to falsify the engineering team's conclusions five times running, and the
process recorded every one of them instead of quietly repairing and re-declaring success.**

The release-readiness report puts it in its own words:

> *"Every standing check is green and […] tests pass. **That is not the same as ready.** Nothing
> physical has been built or measured; 91 requirements await hardware; one joint of the design is
> known not to close, and the framework's own `ECR-D-014` is open on a rule this session could
> have quietly ignored. The green is real, it is broader than it was, and it is still narrow."*

*(The elided figure is the suite count as it stood when that section was written; the measured
count at `v0.11.0` is 895 local / 843 from a clean clone, and `ECR-D-014` has since closed —
[`DOCUMENTATION_FINDINGS.md`](DOCUMENTATION_FINDINGS.md) §3.)*
