# Exported CAD Deliverables — register and provenance

> **Instance artifact.** Partition `cad`. **Every digest below is computed from
> the file at the repository path beside it**, not transcribed. Regenerate and
> check the whole register with:
>
> ```
> PYTHONPATH=src python -m aief_deliverables
> ```

**The deliverables are in this repository.** They were not, until `ECR-D-015`
(session `S-2026-08-17-01`). This file previously opened by declaring the
external output root *"outside this repository by rule; the repository records
provenance, never duplicates the exports"* — **a rule no authority states.**
`program/SEDEP-PMP-002_Digital_Engineering_Infrastructure.md` §3.1 directs the
opposite in terms — *"STEP exported at each gate, **committed to
`cad/exports/step/`** … Git holds the neutral geometry record; Fusion holds the
parametric one"* — its §3 marks the Fusion export root **`[Generated —
mirrored to repo]`**, and `.gitignore` carries `!cad/exports/step/*.step` and
`!drawings/**/*.pdf` negations that existed for four sessions with nothing to
negate. The consequence was total for distribution and nil for engineering: a
clone contained a register of 62 digests naming files it could not obtain.
`ECR-D-015` disposition A brought 61 of the 62 in.

**They are not byte-identical to the generation root, and are not claimed to be.**
The copy was — 61 of 61, SHA-256 before and after — and then **16 of them were
regenerated in the same session**: 14 PDFs by the `src/aief_draw/pdf.py`
determinism repair, and one SVG and the BOM CSV by `ECR-Q-014`'s `6061-T6` →
`316L` correction. Measured today against `D:\AIEF_CAD_OUTPUT\SEWCP\`:
**45 of 61 identical, 16 differ.** Both differences are improvements this
session made deliberately, and the register below is computed from **what is in
this repository**, which is the authoritative set.

> *This paragraph read "mirrored 61 of the 62 in, byte-identical" and the row
> below claimed the byte identity had been proven twice. `ECR-D-015` §5
> withdrew that at `S-2026-08-17-02` and a third independent round found the
> withdrawal had not reached this file — the register still published the exact
> claim the ECR had retracted. Corrected here, `S-2026-08-17-03`.*

| | |
|---|---|
| **Point of generation** | `D:\AIEF_CAD_OUTPUT\SEWCP\` — where the bridge's `export_model` writes. Retained as provenance; **no longer the place the deliverables live** |
| **In the repository** | **61 files, 4,995,097 bytes** — measured from this tree, and the authoritative set. Every digest below is recomputed from the file beside it by `python -m aief_deliverables`, both directions. The index round-trips them byte-identically through a clean `git checkout-index`, which is the property that matters for a clone; identity with the *generation root* is a different property and does not hold for 16 of them |
| **Excluded, deliberately** | `SEWCP-000_MASTER_ASSEMBLY.f3d` (58,903 bytes) — the **parametric** source. `SEDEP-PMP-002` §3.1 assigns it to Fusion Team cloud versioning and `.gitignore` excludes `*.f3d` by name. It is the one file of the 62 that policy places elsewhere |
| **Line-ending policy** | The four deliverable subtrees are `-text` in `.gitattributes`. 14 PDF and 10 STL carry NUL octets; the other 37 are UTF-8 with CRLF. Under the repository's blanket `* text eol=lf` git would have corrupted the binaries and rewritten the rest to LF, **moving every digest in this register**. Octets in, octets out |
| **System interface verification** | [`cad/runs/SYSTEM_INTERFACES.json`](runs/SYSTEM_INTERFACES.json) — 12/12 PASS; `FINAL_SYSTEM_VERIFICATION` 19/19 PASS |

## Register
### Neutral geometry — STEP — `cad/exports/step/`

| Repository path | Bytes | sha256 |
|---|---:|---|
| `cad/exports/step/SEWCP-000_MASTER_ASSEMBLY.step` | 1262728 | `8a53f53f0e64d3723018dcdcce4590ee60fc221b1a095d3a376440756a33ae0c` |
| `cad/exports/step/SEWCP-1000_RETAINER.step` | 36629 | `49f6ac15ef1101704ea77e01e063a576130c222da2fff55eaff13e354419ddfe` |
| `cad/exports/step/SEWCP-200_COOLING_PLATE.step` | 470846 | `052091ccb79bf4479469bf55b390f66bc1ac6bd95220a40b8bc2bdcd33a18e2e` |
| `cad/exports/step/SEWCP-300_HEATER_PLATE.step` | 303144 | `d07f34d0a0f3904a70a77aeff71798384117d3c71aea814a869fd78498f32dc2` |
| `cad/exports/step/SEWCP-400_SUPPORT_RING.step` | 89587 | `ece2b61d354ce6c11e4e9c017704feb9f6494c6d8f57d452848a46f74ba78011` |
| `cad/exports/step/SEWCP-500_ESC_PUCK.step` | 11741 | `b29c8887fa5b6b4d5b9d5fcee19002321e78b2cd61f3bc65d586653d528b9318` |
| `cad/exports/step/SEWCP-600_LIFT_PIN.step` | 7780 | `bfa6610d6272e12ca6b0c3f123ce685d67bcc0cf2ab45fb8b82baa73f78a85ab` |
| `cad/exports/step/SEWCP-700_ALIGNMENT_PIN.step` | 17750 | `59544dcd1dc1162b2b491645fe3688555860b2a8fbd60a8667e8d547db14a0fc` |
| `cad/exports/step/SEWCP-800_PORT_BODY.step` | 24353 | `2f252ebe73d5f9497a588d4c3b0ae5b4d240af366ab520035fc3980097d36f71` |
| `cad/exports/step/SEWCP-901_RF_STRAP.step` | 214269 | `c1465a8f66b1feb740f3e257d99bb59e5f9f22711e2a49f7e005685b9bdd2c82` |
| `cad/exports/step/SEWCP-902_SADDLE.step` | 42230 | `9760c381cc8b6c951f3ca595e270ef5d62b68fe3b8e138a0a8e5bfd86a7caca0` |

*11 files, 2481057 bytes.*

### Tessellated geometry — STL — `cad/exports/stl/`

| Repository path | Bytes | sha256 |
|---|---:|---|
| `cad/exports/stl/SEWCP-1000_RETAINER.stl` | 72884 | `673512ab84767231e4df9b84fb720d6ba9a5cbd3384aa5a57897069433bf4232` |
| `cad/exports/stl/SEWCP-200_COOLING_PLATE.stl` | 677284 | `e085807e12c33cfb214604789e50074b83eea6125690d81e32e1d39f6cff8690` |
| `cad/exports/stl/SEWCP-300_HEATER_PLATE.stl` | 435084 | `f9749762f3ae1970faaebd906d1f09d3c43aff4a87faaa27ddeadbbbddbdb746` |
| `cad/exports/stl/SEWCP-400_SUPPORT_RING.stl` | 221884 | `c0105f5a4d9b93a675a7024bc5f33a461080a5c8c672d162630350ce0c9750df` |
| `cad/exports/stl/SEWCP-500_ESC_PUCK.stl` | 43284 | `2ab6c8ffeaf865fd6f12e849dfa9beabbc0336320f3671dbb8c2893f1b94a354` |
| `cad/exports/stl/SEWCP-600_LIFT_PIN.stl` | 33384 | `157aa14883b13fa7c99aa3b1f3cc6d8b06d81b449e67a3b8d615391df9a6644b` |
| `cad/exports/stl/SEWCP-700_ALIGNMENT_PIN.stl` | 47484 | `2e11e883034a39ecabc25e9a0b1e1fc027c893ec9d8287ec5d4dadcec840f9da` |
| `cad/exports/stl/SEWCP-800_PORT_BODY.stl` | 119084 | `c10b5060b185ec10a9e29a179be1b82a2ec9dfa9397142edfd5d2c7961eb9ad6` |
| `cad/exports/stl/SEWCP-901_RF_STRAP.stl` | 31084 | `523a511231faa6f9144127078d65833e93ce5c776131088c69a96d6e4be8b0b9` |
| `cad/exports/stl/SEWCP-902_SADDLE.stl` | 17084 | `50ee5bcc838a62f0f37bd36163d35e63ea3c7aaf7dd502222efb7ec3a179c92c` |

*10 files, 1698540 bytes.*

### Indentured BOM — `cad/bom/`

| Repository path | Bytes | sha256 |
|---|---:|---|
| `cad/bom/SEWCP-000_BOM_RevA.csv` | 4859 | `7e32fc72679491240845a02f7cb455092ea3e982fc7978599b88050e79bccbac` |

*1 files, 4859 bytes.*

### Assembly drawing — `drawings/assembly/`

| Repository path | Bytes | sha256 |
|---|---:|---|
| `drawings/assembly/SEWCP-000-DRW-001.provenance.json` | 2880 | `b7dec6f966171bfe748525920535e6da364fbafccb2a6218d69f48e2bfe36939` |
| `drawings/assembly/SEWCP-000-DRW-001_Sh1.pdf` | 29043 | `f5cc1e478aae258bedb742c4da9386952a9108b142bf3e449f3c936ce493308a` |
| `drawings/assembly/SEWCP-000-DRW-001_Sh1.svg` | 13356 | `9ecc9161c6de4a48bb44e874c03430bcba3962d01f5d8f357f4a5117cc421496` |
| `drawings/assembly/SEWCP-000-DRW-001_Sh2.pdf` | 32399 | `6a26bc3eb970a7d6b5ada19f329bb8330184484b69adfebce4a5699cd1d96f1c` |
| `drawings/assembly/SEWCP-000-DRW-001_Sh2.svg` | 45335 | `f0352eb4c1dedaa708aeed29d3c36d56205ab0368871470b14f21ef5e9ce3b28` |
| `drawings/assembly/SEWCP-000-DRW-001_Sh3.pdf` | 27748 | `760e97379e07ca3286a4cb6cbe973080363fe32c0b6694670bdc1e88dd137920` |
| `drawings/assembly/SEWCP-000-DRW-001_Sh3.svg` | 13749 | `6b25165cdb0950d1802e62490a3c23af96109539ee0f84d101dc03663e5920c4` |

*7 files, 164510 bytes.*

### Part drawings — `drawings/parts/`

| Repository path | Bytes | sha256 |
|---|---:|---|
| `drawings/parts/SEWCP-1000/SEWCP-1000-DRW-001.provenance.json` | 861 | `1d894f6288db0d1d501b7e063bcd9ee0f9997ca42a1a992b34c41b36566d6cb0` |
| `drawings/parts/SEWCP-1000/SEWCP-1000-DRW-001_Sh1.pdf` | 29283 | `7854b9aae6b396f17478700b54c5350dbb1f2e3544a590642e5e0a18aaae12bf` |
| `drawings/parts/SEWCP-1000/SEWCP-1000-DRW-001_Sh1.svg` | 15992 | `09ff7019171faec8784af875513c750352b56fafd32b2a349f4fb92fe5e779f9` |
| `drawings/parts/SEWCP-200/SEWCP-200-DRW-001.provenance.json` | 2387 | `081df22f843702abe5deab6e46e59caeef6b588eaed80b09de71fe7fe592c0d4` |
| `drawings/parts/SEWCP-200/SEWCP-200-DRW-001_Sh1.pdf` | 49302 | `e0986b72d7650e2d4fbd2b244c7d35800b89648c9dadeef7e980640ac1f92dcf` |
| `drawings/parts/SEWCP-200/SEWCP-200-DRW-001_Sh1.svg` | 38341 | `f92e1f17e4e80e463ec1033c12f00a09ebb41506844ef40c44091cd0d38b6b96` |
| `drawings/parts/SEWCP-200/SEWCP-200-DRW-001_Sh2.pdf` | 30397 | `bf399b5fd985efab56a05191e21c72f666cb8ca3985517075505d208b8395934` |
| `drawings/parts/SEWCP-200/SEWCP-200-DRW-001_Sh2.svg` | 11474 | `0e10af6f935a36f7595ff8a9ba123f39e6560f6c4a950665afe6700ee75a74b5` |
| `drawings/parts/SEWCP-300/SEWCP-300-DRW-001.provenance.json` | 1134 | `e0215aec84acab6d3b7b84def147e92c59da1c528e731f40eaa81e2677e9f38a` |
| `drawings/parts/SEWCP-300/SEWCP-300-DRW-001_Sh1.pdf` | 43119 | `58b75998ef84b8af4e24af7f4ca22578d0e15f8b01a4e42c2c0df48c1a0f2f55` |
| `drawings/parts/SEWCP-300/SEWCP-300-DRW-001_Sh1.svg` | 30324 | `a209340591dce84569f5628fabb8afe69ab08ccc54cb4f995268c34356e6a7f4` |
| `drawings/parts/SEWCP-400/SEWCP-400-DRW-001.provenance.json` | 1271 | `103f2bb2ab5e6e13f20093a789d2e681603e77db66eab8bcfa9c3dbaa515cec9` |
| `drawings/parts/SEWCP-400/SEWCP-400-DRW-001_Sh1.pdf` | 41991 | `335ad88e54ed6e18eaac3765cede180fb7f40819165b310b3f2e8e5b72d1c14e` |
| `drawings/parts/SEWCP-400/SEWCP-400-DRW-001_Sh1.svg` | 29356 | `688ef989098f788aa8c2da0c99d5e8fbdc3974426e894a7e105980f78ce82226` |
| `drawings/parts/SEWCP-500/SEWCP-500-DRW-001.provenance.json` | 845 | `d58fdedff3e47e5da13a4ea4f04b30480b0d0599454c87adb656fab74d9c5529` |
| `drawings/parts/SEWCP-500/SEWCP-500-DRW-001_Sh1.pdf` | 39407 | `7a854ae5e9796f24c9950d185799826c7faf06fdde9ce145296b7ba432b400b7` |
| `drawings/parts/SEWCP-500/SEWCP-500-DRW-001_Sh1.svg` | 27307 | `6ce7130ce15ab448aa005463d80e20278895c199fd24345d14e6b82b40adc468` |
| `drawings/parts/SEWCP-600/SEWCP-600-DRW-001.provenance.json` | 1011 | `a5e21300fc05ce24154935385d147691405e69aa8c1f6a4fe5b8a97981956f6d` |
| `drawings/parts/SEWCP-600/SEWCP-600-DRW-001_Sh1.pdf` | 30512 | `6b47d18807e7b5cbbebaad0417abb721ae4c9290ecda7cae05c99701c2da2909` |
| `drawings/parts/SEWCP-600/SEWCP-600-DRW-001_Sh1.svg` | 19807 | `0550fd378354210b50dd8a58fb7b53fb5a7e9490bc86b2330a25638fedacfac6` |
| `drawings/parts/SEWCP-700/SEWCP-700-DRW-001.provenance.json` | 1416 | `5f63dbd1b1f9f86c818baecac80922497f006eec3aad5f4046086e1bd99c7d71` |
| `drawings/parts/SEWCP-700/SEWCP-700-DRW-001_Sh1.pdf` | 31958 | `d4bd06867d99cf5d6436bf5d416a1ba7b6c9b9ee9d5fd4713c8427b62c5ba2b8` |
| `drawings/parts/SEWCP-700/SEWCP-700-DRW-001_Sh1.svg` | 22743 | `15034f04de1582096622e32c14dd0fb86f37fe583d70ee03de8ffc4c604ed117` |
| `drawings/parts/SEWCP-800/SEWCP-800-DRW-001.provenance.json` | 1641 | `859995aa9630a8e32c69171ffe25b21bc1c086490d6ab80bfa0631f4c2d14cab` |
| `drawings/parts/SEWCP-800/SEWCP-800-DRW-001_Sh1.pdf` | 37420 | `c5c3139854f8174f5ebc51925e0c4819f04fbd2b9a457da164b40d6747272339` |
| `drawings/parts/SEWCP-800/SEWCP-800-DRW-001_Sh1.svg` | 23673 | `93cea412e2a555c24e7eb14057122723bfce32f8dd72d70007c432d2fb54304b` |
| `drawings/parts/SEWCP-901/SEWCP-901-DRW-001.provenance.json` | 1972 | `f00e9b71f5fd943529d8fe176dfa7f114e8bb3b12e217f354bd8bca973bc0c18` |
| `drawings/parts/SEWCP-901/SEWCP-901-DRW-001_Sh1.pdf` | 28169 | `5d49ec6560ad363021790b66a3526b0158a75a8675fe948039ddf668e55c3c39` |
| `drawings/parts/SEWCP-901/SEWCP-901-DRW-001_Sh1.svg` | 12334 | `c0e2c45d6b104ae230f112cee97bf011180d6477dd7d2ab15e71d2808fb64ac6` |
| `drawings/parts/SEWCP-902/SEWCP-902-DRW-001.provenance.json` | 1610 | `1f4243dbeba642b91c0b7b86bccfcdd0614cf63c1df647e3b3c3f8a3b7eabd1c` |
| `drawings/parts/SEWCP-902/SEWCP-902-DRW-001_Sh1.pdf` | 26949 | `94b689a0cfc6fe143fb01f1dfb6e1fa0dca52f9546825944737eb7ef59542e74` |
| `drawings/parts/SEWCP-902/SEWCP-902-DRW-001_Sh1.svg` | 12125 | `9e7a169d17adbc2fc4146a0c764dd31c63ee2b6191e1936a42bfa0bc41cfd8a8` |

*32 files, 646131 bytes.*

---

## Design lineage behind these files

**ECR-resolution re-issues (`S-2026-08-11-05`).** SEWCP-901 re-drilled
tap-coincident (`ECR-D-013` DEC-01); SEWCP-902 re-architected as the plate-hung
hanger, Rev B (`ECR-Q-012` DEC-02 + addendum); SEWCP-200 gains the two bracket
taps (`APR-031`). Superseded lineages quarantined under `OI-CAD-03`. Final
integration evidence: `cad/runs/ASSEMBLY_S-2026-08-11-05/`.

**SEWCP-901 re-issue (`S-2026-08-11-02`).** The free-state neutral-S model
could not mate the CP-IF-8 land; re-derived to the installed form and
re-verified (`RUN-20260811T200254-ca7080`, PASS 15/15). The digests above are
the re-issue. The superseded lineage is preserved in the Fusion project as
`ZZ-SUPERSEDED-FREE-S_SEWCP-901-20260811`.

**Master assembly.** `SEWCP-000_MASTER_ASSEMBLY`, Fusion cloud v5 — verified
`RUN-20260811T200919-f6cb5e` PASS, plus the final re-verification in
`REPAIRS_S-2026-08-11-04` (19 occurrences, 7.6731 kg, CP lineage re-homed, lift
pin re-assigned to alumina). The `.step` above is that document's export.

**Drawing-stage register — DISCHARGED `S-2026-08-11-02`.** The items deferred
at the drawing stage are realised as drawing content: edge breaks and finishes
as standard notes; SEWCP-200 masking S9/S10 + DR-6 as the masking sheet;
SEWCP-901 flat pattern with bend stations; and SR-D16 / SEWCP-904 / EC-D14 /
the SC spring clip carried as explicit drawing and BOM notes with their open
records. Every drawing dimension traces via its `.provenance.json` sidecar —
79 dimensions, 0 unsourced (`FSV-DRAWINGS`).

**`OI-CAD-01` and `OI-CAD-02` closed** by `cad/runs/REPAIRS_S-2026-08-11-04.json`
(lift-pin alumina repair; CP lineage re-home + assembly re-verify + exports).
The SEWCP-200 part exports predate the re-home and remain valid — the re-homed
lineage carries byte-equivalent verified content (vol 1479787.4 mm³, 3.9954 kg).

## What these deliverables are not

**No article has been built and nothing here is qualified hardware.** 91 of the
137 numbered component requirements require physical evidence and **0 are
verified** — see
[`.ai/project/verification/PVR-001`](../.ai/project/verification/PVR-001_Physical_Verification_Record_And_Test_Matrix.md).
The four mass figures are `MODEL-PREDICTED` and labelled so.

Carried open against this set: `ECR-Q-011` (FSW minimum rib), `CP-02` (ΔP, flow
bench — the requirement most at risk in the specification), `CP-11` (thermal
map), `SEWCP-904` envelope, `EC-D14` layout, `SR-D16` degeneracy, and
`OI-CAD-03` (four quarantined Fusion lineages, all PRESERVE). See
[`.ai/project/OPEN_ITEMS.md`](../.ai/project/OPEN_ITEMS.md).
