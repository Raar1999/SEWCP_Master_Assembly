# History Remap — the `ECR-D-018` publication-safety sanitization

> **Instance artifact.** Partition `project`. Owner `repository-engineer`. Mutability append-only in effect: rows are added when history is rewritten and never edited afterwards.
> **Authority:** [`ecr/ECR-D-018`](ecr/ECR-D-018_Local_Account_Name_Becomes_New_Public_Information_At_Publication.md), ruled at [`decisions/DECISIONS_S-2026-08-18-02.md`](decisions/DECISIONS_S-2026-08-18-02.md) DEC-22/23/24, override recorded at [`approvals/APR-039`](approvals/APR-039_Rank-1_Override_LAW-07_For_ECR-D-018_Sanitization.md).

---

**This file is the resolver for every commit hash written before `2026-08-18`.** A citation
elsewhere in this repository naming a pre-rewrite hash is **not stale and must not be edited**:
it correctly names the object that carried the statement when the statement was made. Resolve
it here.

## 1 · What the rewrite changed, and what it did not

**Changed:** the local Windows account-name segment of a filesystem path, replaced by the
neutral placeholder `<user>`, in **53** occurrences across **11** blobs — the ten
`cad/runs/RUN-*/run.json` failure records and the `DEC-21` text in
`decisions/DECISIONS_S-2026-08-17-01.md`.

**Not changed, and measured rather than asserted** (see [`results/R-032.md`](results/R-032.md)):
author identity, committer identity, author and committer timestamps, commit messages, tag
annotations with their tagger and date, file modes, path names, and every other byte of every
file. Traceback structure, exception types, exception messages, module names, line numbers,
run ids, operation ids and Fusion build identifiers are all byte-identical. **No failure was
hidden, softened or deleted.**

## 2 · Commits that did **not** change

**29 of 54.** Everything before `2026-08-11` is untouched, which is why the approval-provenance
chain survives intact: `d07e931`, `655aa75`, `be75798` and `8546960` all keep their hashes, and
the `ECR-D-006` attribution and the `APR-002`/`-004`/`-005` subject recovery are unaffected.

Ten of the eleven annotated tags are likewise unmoved: `baseline/spec-revA`, `v0.1.0`,
`v0.3.0` … `v0.10.0` all resolve exactly as before.

## 3 · Commit remap — 25 rows, oldest first

| Pre-rewrite | Post-rewrite | Date | Subject |
|---|---|---|---|
| `7ba0b7545859` | `b71d5ad989e8` | 2026-08-11 | Build and verify the SEWCP-200 CAD increments through the agent-driven p |
| `9b28dd686682` | `c3933061c499` | 2026-08-11 | Design and build the SEWCP-200 below-face features through the agent pip |
| `038c4e5ce12e` | `7d02fae18aa9` | 2026-08-11 | Complete the SEWCP-200 CAD model: DR-6 vents, material, mass; automate t |
| `ac67ca824260` | `1c23fe6cbff4` | 2026-08-11 | Trim the STATE.md next-action block back inside its V-09 token cap |
| `45805b8d2fea` | `8d9751af5960` | 2026-08-11 | Build and verify SEWCP-700 through the autonomous loop; export deliverab |
| `6f3f973880ab` | `9fe8232b8b13` | 2026-08-11 | Hold STATE.md inside its V-09 cap after the SEWCP-700 status update |
| `df77294bb324` | `f400685d317d` | 2026-08-11 | Autonomous loop: SEWCP-600, SEWCP-1000 and SEWCP-800 designed, built, ve |
| `d5475845bbca` | `e10c2043ba91` | 2026-08-11 | Autonomous loop: SEWCP-901 strap and SEWCP-902 saddle built, verified, e |
| `d2cade97e163` | `6aaec3bf1935` | 2026-08-11 | Autonomous loop: SEWCP-400 support ring built, verified, exported |
| `3889a48e806b` | `97d6b4459a52` | 2026-08-11 | Spiral routing for the heater grooves: exact keep-out projection, arc-ch |
| `4d03041d4a9b` | `04c016be81ce` | 2026-08-11 | Complete the defined SEWCP CAD design: all nine component volumes verifi |
| `fc2a336b3a3a` | `cbee971cdb79` | 2026-08-11 | Post-geometry completion: assembly built and verified, drawing set, BOM, |
| `1c07cf882a37` | `b36591e4ab79` | 2026-08-11 | Document-creation lifecycle repair: identity without persistence, save o |
| `7b743a9b54b7` | `efc1f4e50476` | 2026-08-11 | Bridge resumed: orphans deleted, lifecycle validated live, CP lineage re |
| `baf843a0edc7` | `1ab47aa4aa7d` | 2026-08-11 | Delegated-authority engineering resolution: ECR-D-013/Q-011/Q-012 and th |
| `8aa5b77e67a0` | `11122a3521af` | 2026-08-12 | Release-readiness audit: ECR-D-006 and ECR-D-014 dispositioned, five def |
| `2c334ae32c3e` | `e480aa58bf21` | 2026-08-12 | Stage 6 canonical closeout: B2a proven, OQ-14 closed, ledger genesis to  |
| `c55ecafaa823` | `700fb3db4f97` | 2026-08-17 | Public release preparation: licence ratified, deliverables brought into  |
| `1c1581884774` | `2f829c7c24c8` | 2026-08-17 | Second independent QA round: canonical-path enforcement repaired, four f |
| `6d403bf7982e` | `3b0a662e68ae` | 2026-08-17 | Third independent QA round: enforcement condition discharged, register s |
| `f3e3b7cfa16d` | `263f5f6fffb0` | 2026-08-17 | Fourth independent QA round: the check written to end a recurring defect |
| `f8ff028d56ae` | `cad6ced67c67` | 2026-08-17 | ECR-D-014 closed on the fifth independent round; register check rebuilt  |
| `3a0656d20076` | `de3f87e6a0e2` | 2026-08-18 | Add portfolio documentation set and rewrite README for a general reader |
| `4f20ef1b67d0` | `748c6c5be902` | 2026-08-18 | Supersede R-030 with R-031 and close the portfolio governance gap |
| `cf2163b3830b` | `ad50aebf1b20` | 2026-08-18 | Reopen DEC-21 and authorise the publication-safety history sanitization |

## 4 · Tag and ref remap

| Ref | Pre-rewrite | Post-rewrite |
|---|---|---|
| `refs/heads/main` | `f8ff028d56ae` | `cad6ced67c67` |
| `refs/heads/docs/portfolio-presentation-pass` | `cf2163b3830b` | *(advances with this session's close)* |
| `refs/tags/v0.11.0` — tag object | `055fee8299b5` | `abe7f0fbc0c1` |
| `refs/tags/v0.11.0` — target commit | `f8ff028d56ae` | `cad6ced67c67` |

**`v0.11.0` remains the engineering release `v0.11.0`.** No new version number is created: the
git object hashes moved, the release did not. The tag is still annotated; its tagger, its
timestamp and the entire annotation message are byte-identical, and only the `object` line
differs.

## 5 · Citations resolved by this table

Seven distinct pre-rewrite hashes are cited **40 times across 20 tracked files**. Every one of
them is a historical statement — *"measured at X"*, *"the baseline at X"*, *"verifiable in the
X → Y diff"* — and every one is **left exactly as written**, per the owner's instruction that
historical records are not rewritten to look current.

| Cited hash | Resolves to | Cited in |
|---|---|---|
| `f8ff028` | `cad6ced6` | `ledger/SEG-0000/L-0000007`, `results/R-031.md`, `sessions/S-2026-08-18-01.md`, `CHANGELOG.md`, `README.md`, `docs/DOCUMENTATION_FINDINGS.md`, `docs/README.md`, `docs/RECRUITER_OVERVIEW.md`, `docs/RELEASE.md`, `docs/VERIFICATION.md`, `releases/RELEASE_READINESS_v0.11.0.md` |
| `baf843a` | `1ab47aa4` | `ecr/ECR-D-017…`, `results/R-022.md`, `verification/PVR-001…`, `releases/RELEASE_READINESS_S-2026-08-11-06.md` |
| `1c15818` | `2f829c7c` | `CHANGELOG.md`, `LICENSE`, `docs/DOCUMENTATION_FINDINGS.md`, `releases/RELEASE_READINESS_v0.11.0.md` |
| `4d03041` | `04c016be` | `cad/DOCUMENT_LIFECYCLE.md`, `cad/POST_GEOMETRY_RUN.md` |
| `3889a48` | `97d6b445` | `drawings/defs/sewcp_drawings.py`, `drawings/parts/SEWCP-300/SEWCP-300-DRW-001.provenance.json` |
| `6d403bf` | `3b0a662e` | `LICENSE` |
| `f8ff028d56aee3004b5d41eb1a3d5c3e8f579270` | `cad6ced67c675611620519fc9986ba861703c315` | `docs/RELEASE.md` |

**`ledger/SEG-0000/L-0000007` is append-only and was not edited.** Its reference to `f8ff028`
resolves through this table, which is the whole reason this table exists.

## 6 · The remote has **not** been updated

`origin/main` still stands at the **pre-rewrite** `f8ff028`, and the remote-tracking refs in
this repository still point there, because that is the truth about the remote until a
force-update is performed. **The pre-rewrite objects therefore remain reachable in this local
clone** through `refs/remotes/origin/*`, and the account name is still present in them.

That is a correct and deliberate state, not a residue: nothing has been published, and the
divergence is exactly what the publication gate exists to close. A clean clone of the
publishable refs — `refs/heads/*` and `refs/tags/*` — contains **zero** occurrences.

The required force-update is stated at [`results/R-032.md`](results/R-032.md) and is
**reserved to the owner**. `APR-039` grants no authority to perform it.
