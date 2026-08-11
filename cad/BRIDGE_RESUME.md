# Bridge resume procedure — one human click, then four commands

> Written by session `S-2026-08-11-02` on entering controlled recovery.
> **The single manual step this run could not remove:** Fusion's per-user
> add-in Run state is a QML control invisible to UI Automation, synthetic
> pointer events did not land, and `runOnStartup` in the manifest is
> overridden by that per-user state. Everything else below is automated.

## Why the bridge is down

Fusion was restarted programmatically (PID 11804 → new instance) to clear a
data-cache fault in which the session served stale v4 content for
`SEWCP-200_COOLING_PLATE` (pre-vents, steel) although the verified state
(1 479 787.4 mm³, 3.9954 kg, Aluminum 6061) had been re-committed and
round-trip-verified as **V5**. The add-in did not auto-start in the new
instance. `runOnStartup: true` is now deployed, which may make future
restarts self-serving.

## Step 1 — human (one click)

In Fusion: **UTILITIES → ADD-INS (Shift+S) → AIEF_CAD_Bridge → Run toggle ON.**
(Recommended: also switch its "Run on Startup" toggle ON.)

## Step 2 — automated (paste as-is)

```
cd /d "D:\Fusion Projects\SEWCP_Master_Assembly"
set PYTHONPATH=src
python -m aief_cad --session S-2026-08-11-03 op open_document --args "{\"name\":\"SEWCP-000_MASTER_ASSEMBLY\"}" --timeout 420
python -m aief_cad --session S-2026-08-11-03 op delete_occurrence --args "{\"name\":\"SEWCP-200_COOLING_PLATE v4:1\"}" --timeout 180
python -m aief_cad --session S-2026-08-11-03 op insert_occurrence --args "{\"name\":\"SEWCP-200_COOLING_PLATE\",\"translate_mm\":[0,0,20.0],\"ground\":true,\"use_latest_version\":true}" --timeout 420
python -m aief_cad --session S-2026-08-11-03 op observe_assembly --timeout 300
```

Verify the observation shows the CP occurrence at **mass 3.9954 kg /
volume 1 479 787.4 mm³** (v5 content). Then:

```
python -m aief_cad --session S-2026-08-11-03 op save_document --args "{\"name\":\"SEWCP-000_MASTER_ASSEMBLY\",\"description\":\"CP reference refreshed to verified V5\"}" --timeout 420
python -m aief_cad --session S-2026-08-11-03 op export_model --args "{\"directory\":\"D:/AIEF_CAD_OUTPUT/SEWCP/ASSEMBLY\",\"basename\":\"SEWCP-000_MASTER_ASSEMBLY\",\"formats\":[\"step\",\"f3d\"]}" --timeout 600
```

Record the export digests in `cad/DELIVERABLES.md` (assembly row is
marked PENDING there).

## Step 3 — automated: lift-pin material repair (defect found at BOM audit)

`SEWCP-600_LIFT_PIN` geometry is verified correct, but the saved model
carries **Steel** (observed mass 15.4 g) where `spec/05` §6 and the
package require **99.8% alumina** (3900 kg/m³ → 7.6 g). LP-10 forbids
metal. The build acceptance checked volume/extents only — the material
row was missing, which is how it slipped. Repair:

```
python -m aief_cad --session S-2026-08-11-03 op open_document --args "{\"name\":\"SEWCP-600_LIFT_PIN\"}" --timeout 300
python -m aief_cad --session S-2026-08-11-03 op assign_material --args "{\"material\":\"Aluminum Oxide\",\"density\":3900}" --timeout 120
python -m aief_cad --session S-2026-08-11-03 op observe --args "{\"scope\":[\"bodies\"]}" --timeout 120
```

Confirm mass ≈ 0.00763 kg, then `save_document` and re-export
STEP/STL to `SEWCP-600\` (digests to `cad/DELIVERABLES.md`).

## What is already verified and saved (not to be redone)

- Master assembly `SEWCP-000_MASTER_ASSEMBLY` (cloud, V3): 19 occurrences,
  placement/identity/z-band verification **PASS**
  (`cad/runs/RUN-20260811T200919-f6cb5e/run.json`); grounded; every
  placement provenance-tagged in
  `cad/assembly/SEWCP-000_MASTER_ASSEMBLY.assembly.json`.
- The only defect is the CP occurrence's stale v4 *reference binding*
  (recorded in the run record and POST_GEOMETRY_RUN.md §G1) — content in
  the cloud is correct at V5; the session cache that served v4 died with
  the old Fusion instance, so the fresh session binds V5.
