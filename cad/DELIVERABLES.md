# Exported CAD Deliverables — provenance

External output root: `D:\AIEF_CAD_OUTPUT\SEWCP\` (outside this repository by
rule; the repository records provenance, never duplicates the exports).
Exported by the bridge `export_model` operation from the saved Fusion designs.
System-level interface verification from observed evidence:
[`cad/runs/SYSTEM_INTERFACES.json`](runs/SYSTEM_INTERFACES.json) — 12/12 PASS.

| Component | Design | File (under the root) | Bytes | sha256 (first 16) |
|---|---|---|---|---|
| SEWCP-200 | SEWCP-200_COOLING_PLATE | `SEWCP-200\step\...step` | 470846 | `052091ccb79bf447` |
| SEWCP-200 | 〃 | `SEWCP-200\stl\...stl` | 677284 | `e085807e12c33cfb` |
| SEWCP-300 | SEWCP-300_HEATER_PLATE | `SEWCP-300\step\...step` | 303144 | `d07f34d0a0f3904a` |
| SEWCP-300 | 〃 | `SEWCP-300\stl\...stl` | 435084 | `f9749762f3ae1970` |
| SEWCP-400 | SEWCP-400_SUPPORT_RING | `SEWCP-400\step\...step` | 89587 | `ece2b61d354ce6c1` |
| SEWCP-400 | 〃 | `SEWCP-400\stl\...stl` | 221884 | `c0105f5a4d9b93a6` |
| SEWCP-500 | SEWCP-500_ESC_PUCK | `SEWCP-500\step\...step` | 11741 | `b29c8887fa5b6b4d` |
| SEWCP-500 | 〃 | `SEWCP-500\stl\...stl` | 43284 | `2ab6c8ffeaf865fd` |
| SEWCP-600 | SEWCP-600_LIFT_PIN | `SEWCP-600\step\...step` | 7780 | `bfa6610d6272e12c` |
| SEWCP-600 | 〃 | `SEWCP-600\stl\...stl` | 33384 | `157aa14883b13fa7` |
| SEWCP-700 | SEWCP-700_ALIGNMENT_PIN | `SEWCP-700\step\...step` | 17750 | `59544dcd1dc1162b` |
| SEWCP-700 | 〃 | `SEWCP-700\stl\...stl` | 47484 | `2e11e883034a39ec` |
| SEWCP-800 | SEWCP-800_PORT_BODY | `SEWCP-800\step\...step` | 24353 | `2f252ebe73d5f949` |
| SEWCP-800 | 〃 | `SEWCP-800\stl\...stl` | 119084 | `c10b5060b185ec10` |
| SEWCP-900 | SEWCP-901_RF_STRAP | `SEWCP-900\step\...step` | 214269 | `c1465a8f66b1feb7` |
| SEWCP-900 | 〃 | `SEWCP-900\stl\...stl` | 31084 | `523a511231faa6f9` |
| SEWCP-900 | SEWCP-902_SADDLE | `SEWCP-900\step\...step` | 42230 | `9760c381cc8b6c95` |
| SEWCP-900 | 〃 | `SEWCP-900\stl\...stl` | 17084 | `50ee5bcc838a62f0` |
| SEWCP-1000 | SEWCP-1000_RETAINER | `SEWCP-1000\step\...step` | 36629 | `49f6ac15ef110170` |
| SEWCP-1000 | 〃 | `SEWCP-1000\stl\...stl` | 72884 | `673512ab84767231` |

> **ECR-resolution re-issues (`S-2026-08-11-05`).** SEWCP-901 re-drilled
> tap-coincident (ECR-D-013 DEC-01); SEWCP-902 re-architected as the
> plate-hung hanger, Rev B (ECR-Q-012 DEC-02 + addendum); SEWCP-200 gains
> the two bracket taps (APR-031). Superseded lineages quarantined under
> OI-CAD-03. Final integration evidence: `cad/runs/ASSEMBLY_S-2026-08-11-05/`.

> **SEWCP-901 re-issue (`S-2026-08-11-02`).** The free-state neutral-S model
> could not mate the CP-IF-8 land; re-derived to the installed form and
> re-verified (`RUN-20260811T200254-ca7080`, PASS 15/15). Digests above are
> the re-issue. The superseded lineage is preserved in the Fusion project as
> `ZZ-SUPERSEDED-FREE-S_SEWCP-901-20260811`.

## Drawing-stage register — DISCHARGED `S-2026-08-11-02`

The deferred items above are now realised as drawing content (edge breaks and
finishes as standard notes; SEWCP-200 masking S9/S10 + DR-6 as the masking
sheet; SEWCP-901 flat pattern with bend stations; SR-D16 / SEWCP-904 / EC-D14
/ SC spring-clip carried as explicit drawing and BOM notes with their open
records), the indentured BOM, and the Fusion assembly document. Register:

| Deliverable | File (under the root) | Bytes | sha256 (first 16) |
|---|---|---|---|
| Master assembly (Fusion, cloud, v5) | `SEWCP-000_MASTER_ASSEMBLY` — verified `RUN-20260811T200919-f6cb5e` PASS + final re-verification `REPAIRS_S-2026-08-11-04` (19 occurrences, 7.6731 kg, CP lineage re-homed, LP alumina) | — | — |
| Assembly STEP | `ASSEMBLY\SEWCP-000_MASTER_ASSEMBLY.step` | 1262728 | `8a53f53f0e64d372` |
| Assembly f3d | `ASSEMBLY\SEWCP-000_MASTER_ASSEMBLY.f3d` | 58903 | `5aaf518e6128bf96` |
| Indentured BOM Rev A | `BOM\SEWCP-000_BOM_RevA.csv` (regenerated against `ASSEMBLY_S-2026-08-11-05`) | 4295 | `bca24310b3bdd083` |
| Assembly drawing Sh1–3 (regenerated after the ECR resolutions) | `DRAWINGS\SEWCP-000\SEWCP-000-DRW-001_Sh1..3.svg/.pdf` + provenance | 2880–45338 | `9ecc9161c6de4a48` `426433385970a2b4` `1a25f5f18e4173c6` `b24e6d40fcd5b6ef` `6b25165cdb0950d1` `07d61f613492007f` `b7dec6f966171bfe` |
| SEWCP-200 drawing (geometry + masking sheet; bracket taps + FSW envelope) | `DRAWINGS\SEWCP-200\…Sh1,Sh2` | 11474–49371 | `f92e1f17e4e80e46` `02378875ffd48386` `0e10af6f935a36f7` `30a0d4760e7247e6` `081df22f843702ab` |
| SEWCP-300 drawing | `DRAWINGS\SEWCP-300\…Sh1` | 1134–43188 | `a209340591dce845` `c7f54fb3899926f3` `e0215aec84acab6d` |
| SEWCP-400 drawing | `DRAWINGS\SEWCP-400\…Sh1` | 1271–42060 | `688ef989098f788a` `ddd9d48883869a25` `103f2bb2ab5e6e13` |
| SEWCP-500 drawing | `DRAWINGS\SEWCP-500\…Sh1` | 845–39476 | `6ce7130ce15ab448` `11fc34672b791847` `d58fdedff3e47e5d` |
| SEWCP-600 drawing | `DRAWINGS\SEWCP-600\…Sh1` | 1011–30581 | `0550fd378354210b` `b0e8fe35cfdd0584` `a5e21300fc05ce24` |
| SEWCP-700 drawing | `DRAWINGS\SEWCP-700\…Sh1` | 1416–32027 | `15034f04de158209` `e7185078fcd3a5b0` `5f63dbd1b1f9f86c` |
| SEWCP-800 drawing | `DRAWINGS\SEWCP-800\…Sh1` | 1641–37489 | `93cea412e2a555c2` `cc3ab7a0d9601dda` `859995aa9630a8e3` |
| SEWCP-901 drawing (installed form + flat pattern; tap-coincident holes) | `DRAWINGS\SEWCP-901\…Sh1` | 1972–28238 | `c0e2c45d6b104ae2` `3cb824b670d6246c` `f00e9b71f5fd9435` |
| SEWCP-902 drawing **Rev B — plate-hung hanger** (ECR-Q-012 resolved) | `DRAWINGS\SEWCP-902\…Sh1` | 1610–27018 | `9e7a169d17adbc2f` `1c8b3aa7487edb75` `1f4243dbeba642b9` |
| SEWCP-1000 drawing | `DRAWINGS\SEWCP-1000\…Sh1` | 861–29351 | `09ff7019171faec8` `442dc28d2e204300` `1d894f6288db0d1d` |

Every drawing dimension traces via its `.provenance.json` sidecar.
**OI-CAD-01 and OI-CAD-02 closed** by `cad/runs/REPAIRS_S-2026-08-11-04.json`
(LP alumina repair; CP lineage re-home + assembly re-verify + exports).
The SEWCP-200 part exports above predate the re-home and remain valid — the
re-homed lineage carries byte-equivalent verified content (vol 1479787.4,
3.9954 kg). Carried open: ECR-Q-011, ECR-D-013, ECR-Q-012, CP-02 (physical),
SEWCP-904 envelope, EC-D14 layout, SR-D16 degeneracy, OI-CAD-03 (two
quarantined lineages, owner disposition) — see `.ai/project/OPEN_ITEMS.md`.
