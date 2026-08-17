# LinkedIn Post

*One post, technically credible, no marketing language. Physical qualification is not claimed.
Suggested visual: the master assembly section elevation, `drawings/assembly/SEWCP-000-DRW-001_Sh2`
— or, better, a shaded Fusion render once captured (see `PORTFOLIO_ASSETS.md` §3).*

---

## Primary version

> **A CAD command succeeding is not evidence that it worked.**
>
> That sentence is the whole reason this project exists, and here is the moment it earned its
> keep.
>
> Two M6 taps in a cooling plate. Eight operations dispatched to Fusion 360, eight executed, zero
> errors. By any normal measure of CAD automation, a clean run.
>
> It failed verification.
>
> The observed solid had **173.71 mm³ more material in it than the requirement allowed** — against
> a 1 mm³ tolerance on a 1.48 million mm³ part. Chasing that number down showed the taps were
> breaking into the outer thermal-choke slots. Then the part I didn't expect: a feasibility sweep
> proved that **no compliant position existed anywhere inside the placement window the
> specification itself had given.** The requirement was wrong, not the model.
>
> ---
>
> I spent the last months building **AIEF** — an agent-driven engineering pipeline that converts a
> governed semiconductor-equipment specification into parametric Fusion 360 CAD, reads the model
> back out of Fusion, and verifies the *observed* geometry against the requirement before anything
> is saved.
>
> The architecture keeps three facts apart that most automation merges into one:
>
> • an agent **requested** an operation
> • Fusion **performed** it
> • the model **satisfies** the requirement
>
> Only the third one matters, and it is decided by verifiers that read extents, volume, mass,
> material, parameters, sketches and features out of the live model — and never read whether the
> API call returned OK.
>
> The demonstration hardware is **SEWCP**, a 300 mm bipolar electrostatic chuck pedestal for
> RF-biased plasma process equipment:
>
> • 9 specified components → 10 verified part designs
> • 19-occurrence master assembly, 19/19 final system verification, 12/12 interfaces
> • 11 drawing documents / 14 sheets — 79 dimensions, **0 unsourced**
> • 61 digest-registered deliverables, checked bi-directionally
> • 895 tests; **843 reproduce from a clean clone**
> • **36 CAD runs tracked — 18 of them failures, committed on purpose**
>
> That last number is the one I'd point at. A design system whose record contains only successes
> hasn't shown you its verification working; it's shown you its verification never firing.
>
> ---
>
> Two things I am **not** claiming.
>
> **Nothing has been built.** 0 of 91 hardware-verifiable requirements are physically verified.
> Four mass figures are labelled MODEL-PREDICTED, because the declared verification method is a
> scale, and a scale needs a part.
>
> **One defect is open against the design itself.** A standing check filed the creepage/clearance
> trace on the ceramic support ring and it does not close — 14.00 mm creepage against 20.00 mm
> required. It is ruled, its remedy is computed, and it is deliberately not implemented, because
> implementing it is a specification re-baseline. Do not build to this baseline.
>
> Independent QA ran in cold contexts that rebuild every fact from the repository and import
> nothing from the code under audit. Five rounds. **Four came back NOT CLEARED** — and four
> consecutive repair sessions each introduced a defect of the class they were repairing. That is
> recorded as an open finding, not quietly closed.
>
> The interesting frontier in AI for engineering isn't generating more CAD faster. It's building
> the evidence layer that can tell you the CAD is wrong.
>
> \#SemiconductorEquipment #DesignEngineering #CAD #Fusion360 #MechanicalEngineering
> #EngineeringVerification #AIinEngineering

---

## Shorter version (if the primary runs long for the feed)

> **A CAD command succeeding is not evidence that it worked.**
>
> Two M6 taps in a cooling plate. Eight Fusion 360 operations dispatched, eight executed, zero
> errors — a clean run by any normal measure of CAD automation.
>
> It failed verification: the observed solid carried **173.71 mm³ more material than the
> requirement allowed**, against a 1 mm³ tolerance. The taps were breaking into the thermal-choke
> slots — and a feasibility sweep then proved no compliant position existed anywhere inside the
> window the *specification* had given. The requirement was wrong, not the model.
>
> I built **AIEF**: an agent-driven pipeline that turns a governed semiconductor-equipment
> specification into parametric Fusion 360 CAD, then reads the model back out and verifies
> observed geometry against the requirement before anything is saved. Demonstrated on SEWCP, a
> 300 mm electrostatic chuck pedestal — 9 components, a 19-occurrence assembly, 11 drawings with
> 79 dimensions and none unsourced, 895 tests, and **36 tracked CAD runs of which 18 are
> failures**, kept in the repository on purpose.
>
> What I am not claiming: nothing has been built. **0 of 91 hardware-verifiable requirements are
> physically verified**, and one defect is open against the design baseline that blocks any
> hardware build.
>
> The frontier isn't generating CAD faster. It's building the evidence layer that can tell you the
> CAD is wrong.

---

## Notes before posting

- Check `DOCUMENTATION_FINDINGS.md` §1 — **the repository is private at the time of writing.** A
  post linking to it will 404 for everyone until visibility changes.
- Lead with the 173.71 mm³ story, not with the architecture. The number is what makes an engineer
  stop scrolling; the architecture is what makes them read the README.
- Keep the "nothing has been built" paragraph. It is the paragraph that makes the rest credible
  to anyone who has worked in semiconductor equipment.
