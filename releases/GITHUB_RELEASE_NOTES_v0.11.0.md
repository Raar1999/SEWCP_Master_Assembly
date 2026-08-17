# GitHub Release notes — `v0.11.0` (PREPARED, NOT PUBLISHED)

> **Instance artifact.** Partition `releases`. Owner `repository-engineer`.
>
> **Publication is gated and this file does not release anything.** At the time of writing, the
> repository is **private** and **no GitHub Release object exists for any tag**
> (`gh api repos/…/releases` → `0`). Creating a Release page and changing visibility are both
> owner actions on GitHub that no file in this tree can perform.
>
> The tag `v0.11.0` **is** pushed and its annotation already states the physical-qualification
> boundary and `ECR-D-016`. The body below is prepared so that publication, if the owner chooses
> it, is a paste rather than a rewrite — and so that the release page cannot say something the
> repository does not support.
>
> **Prerequisite before publishing:** the safety audit at
> [`../docs/DOCUMENTATION_FINDINGS.md`](../docs/DOCUMENTATION_FINDINGS.md) must have no
> unresolved finding, and the repository must be public — a Release page on a private repository
> is visible to no one and creates the impression of publication without it.

---

## Release title

    v0.11.0 — CAD and software complete; physical qualification not started

## Release body

<!-- everything below this line is the intended Release body, verbatim -->

**An agent-driven engineering pipeline that converts governed semiconductor-equipment
requirements into parametric Fusion 360 designs, verifies the resulting geometry against the
requirement from the model Fusion actually built, and iterates through failure-recovery loops
before release.**

Demonstration hardware: **SEWCP**, a 300 mm bipolar electrostatic chuck pedestal for RF-biased
plasma process equipment.

### Read this first

This release is a **design and process artifact, not a qualified product.**

- **Nothing physical has been built or measured.** 0 of 91 hardware-verifiable requirements are
  verified. Four mass figures are labelled `MODEL-PREDICTED`; the declared method is a scale, and
  a scale needs a part.
- **One defect is open against the design itself.** `ECR-D-016` — the Support Ring isolation joint
  does not close: creepage 14.00 mm against 20.00 mm required, clearance 8.50 against 12.00, shunt
  impedance 353.94 Ω against 400. It is ruled, its remedy is computed, and it is deliberately not
  implemented, because implementing it is a specification re-baseline. **Do not build to this
  baseline.**

### What is in the release

| | |
|---|---|
| Components specified, frozen Rev A | **9** — 137 numbered requirements |
| Part designs modelled and verified | **10**, plus a **19-occurrence** master assembly, 7.6997 kg |
| Final system verification | **19 / 19** · system interfaces **12 / 12** |
| Drawings | **11 documents / 14 sheets** — 79 dimensions, **0 unsourced** |
| Deliverables | **61 files**, 4,995,097 bytes, digest-registered and checked both directions |
| Tests | **895** in the working tree · **843 passed, 52 skipped, 0 failed** from a clean clone |
| Independent QA | **5 cold-context rounds**, 4 returned `NOT CLEARED` |
| Tracked CAD runs | **36 — 18 PASS and 18 FAIL**, failures committed on purpose |

### The idea

> A CAD operation succeeding is not evidence that it worked.

`extrude(...)` returning OK means Fusion accepted the operation. Three facts are kept apart and
never merged: an agent **requested** an operation; Fusion **performed** it; the model **satisfies**
the requirement. Only the third is acceptance, and it is decided by verifiers that read observed
model state — extents, volume, mass, material, parameters, sketches, planes, features — and never
read whether the call returned OK.

Worked example, from the tracked record: two Ø6 hanger taps, eight operations dispatched, eight
executed, zero Fusion errors. The run **failed** — the observed solid carried **173.71 mm³** more
material than the requirement allowed against a **1 mm³** tolerance. Root cause was not the model
but the specification: no compliant tap position existed anywhere inside the placement window the
requirement gave.

### Verification and its boundary

Every CAD-verifiable property is computed from observed evidence and reproduces from a clean
clone. Two standing checks exit non-zero **and are meant to** — `aief_analysis`, because
`ECR-D-016` does not close, and `aief_exec check`, which reports three open exec-layer conditions
of its own. A check reporting PASS on an open defect would itself be the defect.

**CAD/software verification is not physical qualification.** A model establishes geometry and the
properties that follow from geometry and a density. It establishes nothing about pressure drop,
heat transfer coefficient, leak rate, temperature uniformity, contact resistance, inductance,
particle generation, outgassing, cycle life, dielectric strength or dechuck behaviour.

### Known open

- `ECR-D-016` — blocks hardware build; Rev B baseline revision required.
- `PVR-001` — 0 of 91 hardware-verifiable requirements verified.
- `OI-V-17` — four consecutive repair sessions each introduced a defect of the class they were
  repairing. A process finding, recorded and not closed.
- `CMP-BLOCK-004` / `-005` — gate **AIEF framework** Release 1.0.0, a different release of a
  different thing.

Full register: [`.ai/project/OPEN_ITEMS.md`](../.ai/project/OPEN_ITEMS.md).

### Licence

`MIT AND CC-BY-4.0`, boundary by path — MIT for software, CC-BY-4.0 for documents, engineering
artifacts and generated design data. **No patent and no trademark licence is granted, and the
design is not qualified hardware.** See [`LICENSE`](../LICENSE), which is authoritative.

<!-- end of intended Release body -->

---

## Publication checklist — owner

1. [ ] Repository visibility set to **public** (or a deliberate decision that it stays private,
       in which case **do not** create a Release page).
2. [ ] `docs/DOCUMENTATION_FINDINGS.md` carries no unresolved security or licensing finding.
3. [ ] `main` carries the governance closeout and the `validate` workflow is green on it.
4. [ ] Release created against the **existing** annotated tag `v0.11.0` — the tag is never
       moved, per `TAGS.md` §4 rule 2.
5. [ ] Release marked as **not a pre-release**; the digital release is complete on its own terms.
6. [ ] No binary attached beyond what the repository already tracks. The 61 deliverables are in
       the tree and digest-registered; a second copy on a release page is a second thing to keep
       in agreement.

**Nothing in this file authorises step 1.** That transition is the owner's.
