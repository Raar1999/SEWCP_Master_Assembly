# Interview Story

*Answers are grounded in the actual architecture. Every figure is verifiable from the repository.
Where an answer would be stronger if overstated, it is not overstated — that is deliberate, and
an interviewer will test it.*

---

## 30-second version

> "I built an agent-driven engineering pipeline that turns a governed semiconductor-equipment
> specification into parametric Fusion 360 CAD — and then, critically, reads the model back out
> of Fusion and verifies the *observed* geometry against the requirement before anything is
> saved. Because a Fusion command succeeding only means Fusion accepted it; it says nothing about
> whether the part is right. I demonstrated it on SEWCP, a 300 mm electrostatic chuck pedestal:
> nine components, a nineteen-occurrence assembly, eleven drawings, all verified from observed
> model state, released at v0.11.0. Physical qualification hasn't started — nothing has been
> built or measured, and I keep that boundary explicit."

---

## 2-minute version

> "The problem I was interested in isn't 'can an LLM write CAD API calls'. It can, and Fusion
> will execute them. The problem is that **executing successfully and being engineering-correct
> are different things**, and most CAD automation conflates them.
>
> So the architecture keeps three facts apart and never lets them merge: an agent *requested* an
> operation; Fusion *performed* it; and the model *satisfies* the requirement. That third one is
> the only one that matters, and it's decided by verifiers that read the observed model — extents,
> volume, mass, material, the parameter table, the sketch and feature list — and never look at
> whether the API call returned OK.
>
> The concrete example is my favourite thing in the project. Two M6 hanger taps in the cooling
> plate. Every Fusion operation succeeded — eight dispatched, eight executed, no error. The run
> **failed**, because the observed solid had 173.71 mm³ more material in it than the requirement
> allowed, against a 1 mm³ tolerance. Chasing that number down showed the taps were breaking into
> the outer thermal-choke slots. And then the interesting part: a feasibility sweep proved no
> compliant position existed anywhere inside the placement window the *specification* had given.
> The requirement was wrong, not the model. That's not something a system that trusts command
> success can ever find.
>
> Around that sits the governance: a frozen specification, ECRs instead of in-place edits, roles
> that can't verify their own output, eight standing checks that compute the properties the
> documents claim, and a hash-chained ledger. Independent QA ran in cold contexts that
> reconstruct everything from the repository — five rounds, four came back NOT CLEARED, and they
> found real defects, including in my own repairs.
>
> Released at v0.11.0. Digital work is complete and reproduces from a clean clone. Physical
> qualification is zero of ninety-one requirements, and there's one open defect against the
> design itself that blocks any hardware build. Both of those are on the first screen of the
> README, not in an appendix."

---

## 5–10 minute technical walkthrough

**1 · The input.** A frozen specification — Volumes 00–09, 137 numbered component requirements,
hash-registered. Volume 00 is the parent: coordinate system, datums, feature clocking map, Z
stack-up, thermal/RF/vacuum budgets, tolerance allocation, fastener schedule, 13 binding Design
Rules. Nothing downstream may contradict it, and it is never edited to fix a defect — a defect
becomes an ECR.

**2 · Requirement packages.** The executable form is a JSON requirement package describing *an
engineering problem*, not a CAD model. The CAD layer holds no SEWCP knowledge at all — it would
happily take a heat exchanger plate or a fixture. That separation is what makes it a platform
rather than a script.

**3 · Agents.** Domain agents own requirement *kinds* and return a contribution bounded by a
declared write scope. An agent reaching outside its domain is rejected at merge rather than
merged and audited later.

**4 · Design solution.** The controlled handoff. It states what should be built. It does not say
how Fusion will build it, and it does not say what Fusion did build. Three separate types, kept
separate on purpose — because a layer that lets them blur will eventually report the intent as
the outcome.

**5 · The bridge.** Fusion 360 has no external automation API. No Design Automation engine; the
Data API is read-only metadata. The only supported route is code inside Fusion's own process, and
the only way onto the thread that owns the document is a registered custom event. So I wrote an
add-in that polls a file queue, executes one operation, and writes back what it *observed*.
Thirty-two operations across the shell and its extension module — sixteen geometric, the rest
document lifecycle, assembly and data-file work. The queue is transport; the tracked run record
is the evidence.

**6 · Observation.** A separate type from the solution, with one rule that carries a lot of
weight: **absence is represented as absence**. A body Fusion didn't report is `None`, not a body
of volume zero. That's why a failed run reports *"not present in the observed model — a check
that cannot be evaluated has not passed"*, instead of comparing 0 to 0 and passing on an empty
document.

**7 · Verification.** Three verifiers, one verdict, none of which reads whether the command
executed. Geometry: extents, body count, volume, mass, material — plus intrinsic checks derived
from the solution, so a solution with no acceptance conditions still isn't vacuously verified.
Interface: declared construction planes at declared offsets, locating sketches, and interfaces
not built in this bounded run reported as *deferred* rather than passed. Constraint: every
parameter exists, equals its resolved expression, and — the subtle one — a declared *derivation*
is still a derivation, because a literal that happens to be right today has stopped tracking its
source.

**8 · Failure handling.** A diagnosis names five things: failed requirement, observed evidence,
responsible area, likely cause, proposed correction. A classifier decides the owning layer. Two
guarantees: no blind retry — the repair sequence's digest must differ from the failed one, or
it's refused with NO-PROGRESS; and no infinite repair — attempts are capped, and on exhaustion it
reports the surviving findings rather than degrading into a pass.

**9 · Persistence.** Documents are saved only on verified PASS. That came from a real defect:
`rename_component` had to `saveAs`, because Fusion refuses to rename an unsaved root component —
so persistence preceded geometry, and failed runs left saved blank documents behind. The fix
binds identity as a design attribute without persisting, moves first-save into `save_document`
alone, and gives failures an explicit disposition. `discard_document` refuses a saved design by
contract, so a failure path can never destroy an authoritative model.

**10 · Above the CAD layer.** Thirteen laws, twelve role contracts, twenty-five validation rules,
a six-stage compiler, a hash-chained ledger, and eight standing checks. Then independent QA in
cold contexts that recompute without importing the code under audit.

**11 · Output.** Ten verified part designs, a nineteen-occurrence assembly, eleven drawing
documents over fourteen sheets with 79 dimensions and zero unsourced, an indentured BOM
cross-checked four ways, sixty-one digest-registered deliverables, and analyses. 895 tests; 843
from a clean clone.

**12 · What I did not do.** Build anything. Zero of ninety-one hardware-verifiable requirements
are physically verified. And `ECR-D-016` is open against the design itself.

---

## "What did YOU actually build?"

The parts that are mine, concretely:

- The **Fusion 360 add-in** and the file-queue protocol — the only mechanism in this project that
  can drive Fusion at all, and the decision that it returns *observed state* rather than
  acknowledgements.
- The **verification layer** — three verifiers, the acceptance-condition model, the intrinsic
  checks, and the rule that no verifier reads `executed`.
- The **failure classifier and bounded repair loop**, including the no-blind-retry digest check
  and the attempt cap.
- The **document lifecycle** — root-caused from a real defect and rebuilt around
  identity-without-persistence and save-on-PASS-only.
- The **standing checks** — eight modules that compute properties the documents assert, and the
  tests that attack them by constructing the defect and requiring failure.
- The **AIEF governance framework** — laws, role contracts, gates, approval chains, ledger,
  compiler.
- The **SEWCP specification** and the resulting CAD, drawings, BOM and analyses.

The parts I'd name honestly as *not* mine: Fusion 360's geometry kernel, and the physics — the
thermal, RF and structural relations come from published practice and are cited to it.

---

## "Why not just use an LLM to generate CAD?"

Because that solves the easy half.

An LLM will emit a plausible sequence of Fusion API calls, and Fusion will execute most of them.
What you get back is a document. What you don't get is any basis for believing the document
satisfies the requirement — and in this project the disagreement between those two was
**173.71 mm³**, on a run where nothing errored.

Three specific things generation alone doesn't give you:

1. **A comparison.** Something has to hold the requirement-derived expected value and compare it
   to what the model actually is. That means acceptance conditions derived from requirements, not
   written next to the answer.
2. **A representation of absence.** If a feature didn't get built, the checks over it must fail,
   not evaluate to zero and pass.
3. **An owning layer for the mistake.** When it fails, is that a re-dispatch or is the
   specification wrong? Case 1 above was the specification. No amount of better prompting reaches
   that.

The LLM is the reasoning layer. It is not the evidence layer, and the value of the project is in
refusing to let it be both.

---

## "How do you know the geometry is correct?"

Two answers, and the honest one is the second.

**What I can prove:** every CAD-verifiable property is computed from observed model state and
reproduces from a clean clone. Extents, volume, mass and material per body; 105 parameters
present and equal to their resolved expressions; construction planes at declared offsets; feature
clearance pair by pair against `spec/00` §3.2; twelve system interfaces with computed gaps; the Z
stack station by station; nineteen assembly occurrences placed and grounded; nineteen of nineteen
final system checks; 79 drawing dimensions each naming its source parameter or spec clause. The
evidence is tracked run records, not summaries of them.

**What I cannot prove, and say so:** that it *works*. A model establishes geometry and the
properties that follow from geometry and a density. It establishes nothing about pressure drop,
heat transfer coefficient, leak rate, temperature uniformity, contact resistance, inductance,
particle generation, outgassing, cycle life, dielectric strength or dechuck behaviour. Ninety-one
of the 137 requirements are that kind, and zero are verified. The four mass figures are labelled
`MODEL-PREDICTED` — the declared verification method is *Scale*, and a scale needs a part.

And one thing I can prove is *wrong*: `ECR-D-016`. The Support Ring isolation joint doesn't close
— creepage 14.00 mm against 20.00 required, clearance 8.50 against 12.00, shunt impedance
353.94 Ω against 400. Found by a standing check, ruled, remedy computed, not implemented, because
implementing it is a specification re-baseline.

---

## "What happens when the agent makes a mistake?"

It gets caught by something that didn't make the mistake, and then the system decides who owns it.

Walk through the real one. Verification fails on observed volume. The classifier maps the subject
`body:*` to *repairable — re-dispatch profile and extrude*, so the loop tries. Attempt 2 and
attempt 3 produce identical repair sequences and identical findings. The attempt cap fires and it
**escalates with the finding still open, rather than declaring success**. Meanwhile the failure
disposition tries to discard the document and is **refused by contract** — `a saved design is
never discarded by recovery` — so it reverts to the last verified state instead. Nothing was
saved; no orphan was left.

The escalation went to the engineering layer, which found the specification's placement window
was infeasible everywhere, ruled a new position, cleared it against nine neighbouring features,
re-issued the affected specification rows under approval, and re-ran. Pass on the first attempt.
The record proves the fix happened upstream: the requirement package digest and the solution
digest both changed.

Total elapsed between the failing run and the passing one: five minutes thirteen seconds.

And when I'm the one who makes the mistake, the same principle applies with independent QA:
five cold-context rounds, four `NOT CLEARED`, and **four consecutive repair sessions each
introduced a defect of the class they were repairing.** That's recorded as an open process
finding, not quietly closed.

---

## "How is this different from ordinary CAD automation?"

Ordinary CAD automation is *open-loop*: a script drives the modeller, the modeller reports
success, and the script believes it. It is very good at doing the same correct thing repeatedly.

| | Ordinary automation | This |
|---|---|---|
| Input | a parameter set or a recorded macro | a governed requirement package with acceptance conditions |
| Success means | the API calls returned | the observed model satisfies the requirement |
| On failure | exception, or a wrong part | classified by owning layer; bounded repair, or escalation |
| Retry | re-run the same thing | refused unless the dispatched sequence actually changed |
| Evidence | logs, usually discarded | tracked run records — commands, observations, findings, escalations, including 18 failures |
| Persistence | whatever the script saved | first-save only on verified PASS; failures reverted or discarded |
| Provenance | filename and date | SHA-256 over canonical bytes, digest-registered deliverables, per-dimension drawing sources |

The honest framing: this is **not** more autonomous than a good CAD macro. It is more
*sceptical*. The value is that it can tell you it produced the wrong thing.

---

## "What would you improve next?"

Five, in the order I'd actually do them.

1. **Close `ECR-D-016` properly.** The Rev B remedy is computed and published *with its own
   defects recorded at §7* — the ≈22 mm creepage doesn't reproduce and the relocated web recreates
   the conflict in miniature. It is a starting point, not a design. That is a specification
   re-baseline and real engineering work.
2. **Get hardware.** Ninety-one requirements are waiting on an article. The most valuable next
   result in this whole project is a CMM report that disagrees with the model.
3. **Extend verification to what geometry can't reach.** Pressure drop, thermal resistance and
   RF impedance are computed today as desk analyses; wiring them to solvers and treating solver
   output as observed state — with the same "unmeasured is not compliant" discipline — is the
   natural next layer.
4. **Fix the process finding, not just its instances.** `OI-V-17`: four consecutive repair
   sessions each reintroduced the defect class they were repairing. The pattern was always *a
   claim with no standing check*. The generalisation is to make "you asserted a property; where
   is the check?" mechanical rather than cultural.
5. **Unblock `OI-C-10`.** A bounded index at 597 of a 600-token cap is now suppressing findings
   from getting their own identifier. Three in three sessions. That is an architecture decision
   about budget allocation, and it needs making before it costs a real finding.

And one I'd resist: making the agent more autonomous. The interesting frontier here is better
evidence, not fewer humans.
