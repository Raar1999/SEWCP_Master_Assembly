# ECR-D-018 — the local account name in the tracked run records becomes **new** public information at publication, and `DEC-21` preserved it on a factual basis that is wrong in both halves

> **Instance artifact.** Partition `project`. Filed per `manifest.templates → tpl-ecr`, schema `core/schemas/SCH-ecr.schema.json`.
> Raised at session `S-2026-08-18-02`, the session at which the owner reopened `DEC-21`. The
> defect is not that the records carry the name — that was known and ruled. The defect is that
> the ruling's stated grounds do not hold, so the disclosure was never actually weighed.

```yaml
ecr_id:       ECR-D-018
class:        D                      # defect - a standing decision rests on two false premises
raised_by:    repository-engineer · S-2026-08-18-02
status:       DISPOSITIONED
disposition:  B - sanitize before publication. Normalise the account-name segment to the neutral placeholder <user> across all reachable history, preserving separator form and every other byte. DEC-21 is superseded, not deleted; the ten run records and the DEC-21 text remain in place with their evidence intact
ruled_by:     human-owner · S-2026-08-18-02
ruled_at:     2026-08-18T00:00:00Z
instrument:   .ai/project/decisions/DECISIONS_S-2026-08-18-02.md DEC-22, DEC-23, DEC-24
approval:     APR-039
affected_artifacts:
  - cad/runs/RUN-20260811T144928-5ab8e1/run.json
  - cad/runs/RUN-20260811T161532-c7d1e5/run.json
  - cad/runs/RUN-20260811T164300-21fa2b/run.json
  - cad/runs/RUN-20260811T171559-874bdd/run.json
  - cad/runs/RUN-20260811T175856-8b8da6/run.json
  - cad/runs/RUN-20260811T181657-7889f4/run.json
  - cad/runs/RUN-20260811T182806-c1ba11/run.json
  - cad/runs/RUN-20260811T183336-a70c01/run.json
  - cad/runs/RUN-20260811T190655-d6ed1a/run.json
  - cad/runs/RUN-20260811T224345-ff189f/run.json
  - .ai/project/decisions/DECISIONS_S-2026-08-17-01.md
evidence:     "See the evidence section."
impact:       "See the impact section."
requested_action: "See the requested-action section."
raised_at:    2026-08-18T00:00:00Z
related:      DEC-21, ECR-Q-016, LAW-07
```

## 1 · Class

**D — defect, and specifically a defect of *grounds*, not of *outcome*.**

`DEC-21` (`DECISIONS_S-2026-08-17-01.md`) ruled **A — preserve unchanged**, and gave two
reasons of fact for why the exposure was bounded. An independent public-release review of
`S-2026-08-18-02` measured both and found both false. A decision whose stated grounds are
false has not been made; it has been recorded. That is the defect.

`DEC-21` was also right about one thing and this ECR does not disturb it: these are **tracked
failure evidence**, and nothing here deletes, hides, softens or re-words a failure.

## 2 · Evidence

### 2.1 · The count in `DEC-21` is wrong

`DEC-21` records the account name appearing *"41 times"*. Measured over the raw object bytes
of every affected blob, the true figure is **52** in the ten run records, in **three** distinct
path forms — plus one further occurrence in `DEC-21`'s own prose, for **53** in total:

| Form, as a reader of the traceback sees it | Occurrences |
|---|---:|
| `C:/Users/<user>/AppData/Roaming/Autodesk/…` | 33 |
| `C:\Users\<user>\AppData\Roaming\Autodesk\…` | 11 |
| `C:\Users/<user>/AppData/Local/Autodesk/webdeploy/…` | 8 |
| `DEC-21` prose, the name quoted as a code span | 1 |
| **Total** | **53** |

`41` is `33 + 8` — the two forms whose separator is a forward slash in the raw JSON bytes. The
eleven fully-backslashed occurrences appear in the file as `Users\\<user>` and were not
counted. The undercount is **exactly the class `OI-V-17` records**: a figure asserted rather
than measured.

### 2.2 · The commit history does **not** already publish the name

`DEC-21` reasons that the exposure is bounded because the name is *"an account name that the
repository's own commit history already associates with this project."*

```
$ git log --all --format="%an <%ae>" | sort -u
Raar1999 <91361865+Raar1999@users.noreply.github.com>
$ git log --all --format="%cn <%ce>" | sort -u
Raar1999 <91361865+Raar1999@users.noreply.github.com>
$ git grep -il "<the personal name the account name abbreviates>" -- .
(no output)
```

> The search term is written as a placeholder deliberately. Spelling the personal name into
> this ECR would introduce a stronger identifier than the one the ECR exists to remove, and
> would then itself require sanitizing. The measurement was run with the literal name and
> returned no tracked file.

Every commit is authored and committed under a GitHub **noreply** address. The account name is
**net-new information** that publication would introduce, not a restatement of something
already published. It links the public handle to a Windows account name that is a plausible
personal-name prefix.

### 2.3 · The repository is **not** public

`DEC-21` opens: *"The repository is public."* `STATE.md` — authoritative at boot step B3 —
records the opposite, and the owner's instruction of `S-2026-08-18-02` confirms it:

```
TWO OWNER GATES, closable by no session: repository PRIVATE, no GitHub
Release object.
NEXT: PRIVATE -> PUBLIC; then OI-C-10; then Rev B for ECR-D-016.
```

`ENGINEERING.md` §7 states `Repository | **PUBLIC.**`, conflating *pushed to `origin`* with
*public visibility*. `origin/main` is at `f8ff028` on a **private** GitHub repository.

**This is the consequential half.** `DEC-21` was ruled as a disclosure that had already
happened and was irreversible. It has not happened. The remedy is available now, costs a
bounded history rewrite, and is **unavailable later** — a public repository is cloned, forked,
mirrored and indexed, and no subsequent scrub recalls what was already fetched.

### 2.4 · Nothing else personal is present

Measured across all ten records: **0** email addresses, **0** IP addresses, **0** URLs, **0**
GUIDs, **0** credential keywords, **0** other user names, **0** host or environment
identifiers. One non-personal identifier recurs — the Autodesk webdeploy build hash
`61bf25b2…225d9a1e`, present on every Fusion 360 installation of that build. The account name
is the whole of the exposure.

## 3 · Impact

**No gate, no deliverable, no requirement and no geometry.** The account name is load-bearing
for nothing:

| Binding candidate | Covers these bytes? |
|---|---|
| `.ai/project/FROZEN.md` (31 artifacts) | **No** — the registry holds no `cad/` path |
| `core/MANIFEST.lock` / `BINDING.core_digest_pin` / B2a | **No** — 75 files, all `BOOT.md`, `FRAMEWORK.md`, `README.md`, `core/**` |
| Deliverables register (61/61) | **No** — subtrees are `cad/exports/**`, `cad/bom`, `drawings/**` |
| Result-record `inputs:` pins | **The run records, no.** `DECISIONS_S-2026-08-17-01.md`, **yes** — see §5 |
| Ledger DC-3 | **No** — entries do not hash run records |
| Code and tests | **No** — nothing reads `error.trace` |

## 4 · Requested action — the approved transformation

Replace **only** the account-name segment, everywhere it occurs in reachable history, with the
neutral placeholder `<user>`. Separator form is captured and re-emitted verbatim, so each of
the three path forms keeps its own slashes and backslashes:

```
C:/Users/<name>/…   ->  C:/Users/<user>/…
C:\Users\<name>\…   ->  C:\Users\<user>\…
C:\Users/<name>/…   ->  C:\Users/<user>/…
```

**Nothing else changes.** Not traceback structure, not exception types, not exception
messages, not module names, not line numbers, not timestamps, not run ids, not operation ids,
not Fusion build identifiers, not any other evidence, not any engineering content. Each
affected record must still show the same exception raised at the same line of the same module
during the same operation of the same run, and must still record that the operation **failed**.

**This is a privacy-preserving normalisation of a local filesystem account identifier. It is
not an alteration of engineering failure evidence.** The objective is not to hide a failure;
the failures are the point of the records and they remain, in full, unchanged.

## 5 · Two consequences that are declared here rather than discovered later

**(a) `DEC-21`'s own prose carries the name once**, quoted as a code span. It is in scope: a
single surviving occurrence identifies exactly as well as fifty-two. Normalising the quoted
token to `<user>` leaves the sentence's meaning intact, and `DEC-21` remains present, readable
and citable as historical evidence. It is **superseded, never deleted, and never re-worded.**

**(b) That file is pinned by `R-031`**, the only `CURRENT` result, at DC-1
`d0af3de0…0ecc5bd3`. Changing its bytes stales `R-031` and `X-06` will fail — which is the
drift detector working, not a defect. The architecture's remedy is stated in one sentence at
`EXECUTION_ARCHITECTURE.md` §6.1: **correction is by supersession, never by mutation.**
`R-032` republishes the pins and seals `R-031` at the DC-1 it then stands at. This is the same
mechanism, for the same reason, as the `R-030 → R-031` supersession of the preceding session.

## 6 · What this ECR does not do

It does not find `DEC-21`'s *reasoning about evidence* wrong — redacting a verbatim capture is
a real cost and `DEC-21` named it correctly. It finds that the cost was weighed against two
facts that are not true, and that the balance changes when the true ones are substituted. It
does not close itself: `LAW-02` clause 5 forbids that, and the disposition above is the
**owner's**, recorded at `DECISIONS_S-2026-08-18-02` DEC-22.

It also does not certify the repair. `LAW-05` bars this session from verifying its own work.
The independent round is **owed** and is recorded as owed, not supplied.
