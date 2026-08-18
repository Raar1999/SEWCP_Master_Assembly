# Verification

*What was verified, how, and — stated with equal weight — what was not.*

All figures measured at release `v0.11.0`, commit `cad6ced6`.

---

## 1 · The distinction this document exists to protect

| | |
|---|---|
| **CAD / software verification** | **COMPLETE.** Every property that follows from geometry, material density and the repository's own artifacts is computed from observed evidence and reproduces from a clean clone |
| **Physical qualification** | **NOT STARTED.** No article has been built. 0 of 91 hardware-verifiable requirements verified |

These are not two degrees of the same thing. A model establishes *geometry and the properties
that follow from geometry and a density*. It establishes **nothing** about pressure drop, heat
transfer coefficient, leak rate, temperature uniformity, contact resistance, inductance,
particle generation, outgassing, cycle life, dielectric strength or dechuck behaviour.
Ninety-one of the 137 requirements are of that second kind (`PVR-001`).

---

## 2 · Observation-based verification

A verifier never reads whether the CAD command succeeded. It reads what Fusion says the model
*is*:

```
observed_model:
  bodies:     name · bbox_min · bbox_max · volume_mm3 · area_mm2 · mass_kg · material
  document:   name · persisted_name · units · design_type · saved
  component:  name · name_source · display_name
  parameters: name · expression · value · is_derived
  sketches · planes · features
```

Two rules make it honest:

1. **Absence is absence.** A body Fusion did not report is `None`, not a zero-volume body.
   A check over an absent subject reports `not present in the observed model. A check that
   cannot be evaluated has not passed.`
2. **No verifier reads `Observation.executed`.** A successful API call is the executing party's
   report on its own work.

---

## 3 · Acceptance criteria

Every finding is a five-field record, and they are all in the tracked run file:

| Field | Example |
|---|---|
| `id` | `ACC-VOL` |
| `subject` | `body:CP_BODY.volume_mm3` |
| `expected` | `1479108.9` |
| `observed` | `1479108.8648750156` |
| `requirement` | `CP-HANGER-TAP` |

`expected` is derived from the requirement package, never typed next to the answer. `observed`
comes back from Fusion. Neither can be edited into agreement without moving a digest.

### 3.1 Geometry verification

Bounding-box extents (`dx`, `dy`, `dz`), body count, volume, mass, material. Tolerances are
explicit and tight — the cooling plate volume check runs at **1 mm³ on a 1.48 × 10⁶ mm³ part**
(0.00007 %). Beyond the declared acceptance conditions, the verifier adds intrinsic checks —
*a solid was declared, so a body must exist; an extrude declared 8.0 mm, so `dz` must be 8.0* —
so a solution that declares no acceptance conditions is still not vacuously verified.

### 3.2 Interface verification

Named construction planes exist at their declared offsets; the locating sketches that later
features derive from exist and are fully constrained. A construction plane declared and absent
is reported as *"every feature that locates against it is unlocated"*.

An interface that the current bounded run does not build is reported **`deferred`** and named —
never silently passed. Where a run realises no interface at all, the verifier says so explicitly
rather than reporting a vacuous pass.

### 3.3 Parameter verification

`python -m aief_params check` → **105 parameters derived from §3**, exit 0.

At run time the constraint verifier adds three checks a value comparison alone would miss:

- every solution parameter **exists** in the model (`CON-PARAM-PRESENT`);
- every parameter **equals its resolved expression** (`CON-PARAM-VALUE`);
- a parameter the solution declares as a **derivation is still a derivation**
  (`CON-PARAM-DERIVED`) — a literal that happens to be numerically right has stopped tracking
  its source, and will not move when the source does.

Plus `CON-UNITS` — *"a document in another unit silently rescales every dimension in the
solution"* — and `CON-SKETCH-CONSTRAINED`.

### 3.4 System-level verification

| Record | Result |
|---|---|
| `cad/runs/SYSTEM_INTERFACES.json` | **12 / 12** — each with the computed gap, e.g. `IF-AP-CB` "AP flange Ø10.000 h6 in CP Ø10.000 H7 counterbore", gap +0.000 |
| `cad/runs/ASSEMBLY_S-2026-08-11-05/run.json` | **PASS** — 19 occurrences, each placed, grounded, with source design + version, observed bbox and mass; total **7.6997 kg** |
| `cad/runs/FINAL_SYSTEM_VERIFICATION.json` | **19 / 19**, `known_defects_carried: []` |

The 19 final checks cover the design registry, the assembly verdict and occurrence count, the
Z-station of every element of the stack against `spec/00` §4.2 (`SEWCP-400` [−0.3, 20.0],
`SEWCP-200` [20.0, 40.0], `SEWCP-300` [41.5, 49.5], `SEWCP-500` [49.9, 55.9], hanger [8.0, 20.0]),
the wafer plane at 55.920, the 12 interfaces, materials against spec, the four-way BOM
cross-check, the drawing set, four export digests recorded in the deliverable manifest, the
cooling-plate occurrence content, and — deliberately — that **every residue of the run is
registered as an open item**.

Its own definition of PASS is written into the file:

> *"PASS here means: every CAD-verifiable property of the final design verifies from observed
> evidence, and every non-verifiable or blocked item is explicitly carried."*

### 3.5 Feature clearance

`python -m aief_clearance` → **CLEARANCE OK**, exit 0. Checks `spec/00` §3.2 pair by pair on
bolt circles and angular positions, and **states what it skipped and why** — *"skip He / vacuum
central port: no bolt circle or no angles — not checked"*. A clearance check that silently omits
a pair is worse than one that omits it loudly.

---

## 4 · Provenance

| Layer | Construction |
|---|---|
| CAD commands, observations, verdicts | SHA-256 over a canonical byte form (UTF-8, sorted keys, no insignificant whitespace) |
| Run records | `sequence_digest`, `solution_digest`, `package_digest`, `record_digest` per run |
| Drawings | a provenance sidecar per document: **every dimension names its source** — `parameter:cp_od (params/generated/SEWCP-200.csv)` or `spec/00 §3.2 coolant 255°(in)/285°(out)`. **79 dimensions, 0 unsourced** |
| Deliverables | 61 files digest-registered in `cad/DELIVERABLES.md`, checked **both directions** |
| Freeze registry | 31 of 31 verify; DC-2 aggregate `1f32489a…8d45cc4b` |
| Framework core | boot step **B2a**: DC-1 over 75 covered files, DC-4 against the lock and `BINDING.core_digest_pin` — **75/75**, recomputed without importing the code being audited |
| History | hash-chained ledger, each entry linking `prev_hash` |

---

## 5 · Independent QA

LAW-05: **no role verifies its own output.** Independence is supplied by a **cold-context
session** that reconstructs every fact from the repository, imports nothing from the code it is
auditing, and writes no repository file — or the item stays open.

Five rounds ran against this release. **Four returned `NOT CLEARED`**, and each found a real
defect in a repair that looked complete. Two of their recomputations contradicted the repository
and were right. Full account: [`QA.md`](QA.md).

---

## 6 · Release verification

Reproduce from a clean clone:

```bash
PYTHONPATH=src python -m aief_gate            # LC-M04 CAD-READY: YES              exit 0
PYTHONPATH=src python -m aief_clearance       # CLEARANCE OK                       exit 0
PYTHONPATH=src python -m aief_params check    # PARAMETERS OK  105                 exit 0
PYTHONPATH=src python -m aief_approval verify # APPROVAL CHAINS OK                 exit 0
PYTHONPATH=src python -m aief_deliverables    # 61 registered, 61 reproduce        exit 0
PYTHONPATH=src python -m aief_register        # REGISTERS OK                       exit 0
PYTHONPATH=src python -m pytest tests/ -q     # 843 passed, 52 skipped, 0 failed
PYTHONPATH=src python -m aief_analysis        # 4 of 5 FAIL — ECR-D-016            exit 1
PYTHONPATH=src python -m aief_stage6          # HALTS: tokenizer artifacts absent  exit 1
PYTHONPATH=src python -m aief_exec check      # 7 of 10 PASS                       exit 1
```

Measured three ways at `cad6ced6`:

| Environment | Result |
|---|---|
| Clean clone of the published repository | **843 passed, 52 skipped, 0 failed** |
| Clean clone + both tokenizer artifacts + TOFU record | **894 passed, 1 skipped, 0 failed** |
| Working tree (artifacts and `build/stage6/detcheck/` present) | **895 passed, 0 skipped, 0 failed** |

The 52 skips measure token budgets through two normative tokenizer families whose artifacts are
third-party binaries and are not tracked. Nothing estimates in their absence —
`budget_measurement_record` rules that absence **blocks** rather than estimates — so they skip
rather than guess. One test needs `build/stage6/detcheck/`, which is gitignored and which no
code in the repository creates, so it is unreachable from a clone by any route; it is the single
remaining skip once the tokenizers are provisioned.

**This gap was itself a defect, found the only way it could be.** Until session `S-2026-08-17-01`
these tests had no skip guard and **failed** on a clone while passing at the desk — so the
README claimed a reproducibility that had never been tested from outside. Recorded as `OI-V-16`;
the GitHub Actions `validate` workflow now runs the battery on a runner, where there is no
author's machine to be lucky on.

**What a clone cannot reproduce at all.** The Fusion designs live in Autodesk cloud versioning,
so regenerating `cad/` requires Fusion 360 with the add-in installed. Everything else — every
gate, every digest, the drawing set, the BOM and the whole test suite — runs offline.

---

## 7 · Physical qualification — the boundary, stated plainly

`PVR-001` is the record, and it contains **no test result**, because no hardware exists.

| | Count |
|---|---|
| Numbered component requirements, Volumes 01–09 | **137** |
| `DESK-DISCHARGEABLE` — method is design, drawing, analysis or calculation | **46** |
| **Hardware required** | **91** (46 + 91 = 137; the classes partition the set) |
| — of which hybrid (instrument *and* analysis) | 7, counted inside the 91 |
| **Verified by physical evidence today** | **0** |

Its status vocabulary is a closed set, and `VERIFIED` is **used nowhere in the file**.

### The four mass rows are predictions, and are labelled as such

| ID | Limit | Model | Margin | Status |
|---|---|---|---|---|
| `CP-15` | ≤ 4.2 kg | 3.9936 kg | −4.9 % | `MODEL-PREDICTED` |
| `HP-18` | ≤ 1.6 kg | 1.2338 kg | −22.9 % | `MODEL-PREDICTED` |
| `SR-15` | ≤ 0.8 kg | 0.5168 kg | −35.4 % | `MODEL-PREDICTED` |
| `EC-18` | ≤ 1.7 kg | 1.6196 kg | −4.7 % | `MODEL-PREDICTED` |

The declared verification method for all four is **Scale**. A scale needs a part. Two of the
four sit within 5 % of their limit, so machining tolerance and surface treatment mass are
consumable margin, not comfortable margin — and the record says so.

### One defect is open against the design itself

`ECR-D-016` — the Support Ring isolation joint does not close. Computed by
`python -m aief_analysis`:

| | Required | Computed |
|---|---|---|
| `SR-04` clearance | ≥ 12.00 mm | **8.50 mm** — the greatest value any hardware choice can offer |
| `SR-03` creepage | ≥ 20.00 mm | **14.00 mm** as modelled; **17.42 mm** with `SR-D12`'s R3.0 fillets present |
| `SR-02` shunt impedance at 13.56 MHz | ≥ 400 Ω | **353.94 Ω** |

One root cause: `spec/03` §2.1 and §3.1 compute the flange gap as empty while §5.2 puts a
6.00 mm grounded ring inside it. The arithmetic was proven against the specification's own
published answer, and an independent round attacked it with five counter-readings — all five
died. Ruled **disposition A: Rev B baseline revision**, remedy computed and published *with its
own defects recorded*, and **deliberately not implemented**, because implementing it is a
specification re-baseline rather than a release action.

**Do not build to this baseline.**
