"""Final system verification - every check recomputed from evidence on disk.

    PYTHONPATH=src python cad/scripts/final_system_verification.py

Writes cad/runs/FINAL_SYSTEM_VERIFICATION.json. Consumes: run records
(observed Fusion state), the assembly package, the BOM builder, drawing
provenance sidecars, and the deliverable manifest. Asserts nothing it does
not compute.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

# ECR-D-015: the deliverables live in this repository now. This script
# read the external generation root, so it verified a copy no clone has -
# and went on reporting PASS after the in-repo BOM and drawings had moved.
STEP_DIR = ROOT / "cad/exports/step"
BOM_CSV = ROOT / "cad/bom/SEWCP-000_BOM_RevA.csv"
DRAWING_DIR = ROOT / "drawings"


def _drawing_dir(pn: str) -> Path:
    return DRAWING_DIR / ("assembly" if pn == "SEWCP-000" else f"parts/{pn}")
ASM_RUN = ROOT / "cad/runs/ASSEMBLY_S-2026-08-11-05/run.json"

REGISTRY = {"SEWCP-200", "SEWCP-300", "SEWCP-400", "SEWCP-500", "SEWCP-600",
            "SEWCP-700", "SEWCP-800", "SEWCP-901", "SEWCP-902", "SEWCP-1000"}

#: spec/00 §4.2 nominal bands the assembly must realise (observed bbox z).
Z_BANDS = {
    "SEWCP-400": (-0.3, 20.0),    # as-supplied 20.30 placed top-at-20 (DR-3)
    "SEWCP-200": (20.0, 40.0),
    "SEWCP-300": (41.5, 49.5),
    "SEWCP-500": (49.9, 55.9),
}

KNOWN_DEFECTS: set[str] = set()   # OI-CAD-01/-02 repaired - REPAIRS_S-2026-08-11-04


def main() -> int:
    checks: list[dict] = []

    def check(cid: str, passed: bool, statement: str, detail: str = "") -> None:
        checks.append({"id": cid, "passed": bool(passed),
                       "statement": statement, "detail": detail})

    # -- component existence and identity (last document listing) ---------
    obs_files = sorted((ROOT / "cad/bridge/obs").glob("ADM-*list_documents*.obs.json"))
    listing = json.loads(obs_files[-1].read_text(encoding="utf-8"))["observed"]
    saved = {r["name"].split("_")[0] for r in listing["saved_designs"]
             if r["name"].startswith("SEWCP-")}
    check("FSV-REGISTRY", REGISTRY <= saved,
          "all ten registry designs exist in the Fusion project",
          f"missing: {sorted(REGISTRY - saved)}" if REGISTRY - saved else
          f"present ({len(REGISTRY)})")

    # -- assembly: verdict, occurrence count, placement, stack-ups --------
    run = json.loads(ASM_RUN.read_text(encoding="utf-8"))
    check("FSV-ASM-VERDICT", run["verdict"] == "PASS",
          "assembly verification verdict is PASS", run["verdict"])
    occs = run["observed_assembly"]["occurrences"]
    check("FSV-ASM-COUNT", len(occs) == 19, "19 occurrences observed",
          str(len(occs)))
    for pn, (lo, hi) in Z_BANDS.items():
        o = next(o for o in occs
                 if (o.get("source_design") or "").startswith(pn))
        ok = abs(o["bbox_min"][2] - lo) <= 0.05 and \
            abs(o["bbox_max"][2] - hi) <= 0.05
        check(f"FSV-Z-{pn}", ok,
              f"{pn} occupies [{lo}, {hi}] (spec/00 §4.2)",
              f"observed [{o['bbox_min'][2]:.3f}, {o['bbox_max'][2]:.3f}]")
    sb = next(o for o in occs
              if (o.get("source_design") or "").startswith("SEWCP-902"))
    check("FSV-Z-SEWCP-902",
          abs(sb["bbox_min"][2] - 8.0) <= 0.05 and
          abs(sb["bbox_max"][2] - 20.0) <= 0.05,
          "hanger occupies [8.0, 20.0] (SB-D04 minimum to ground)",
          f"observed [{sb['bbox_min'][2]:.3f}, {sb['bbox_max'][2]:.3f}]")
    ec = next(o for o in occs
              if (o.get("source_design") or "").startswith("SEWCP-500"))
    check("FSV-WAFER-PLANE", abs(ec["bbox_max"][2] - 55.9) <= 0.05,
          "stack top at 55.900; wafer plane 55.920 via 0.020 mesa (callout)",
          f"{ec['bbox_max'][2]:.3f}")

    # -- system interfaces evidence ---------------------------------------
    si = json.loads((ROOT / "cad/runs/SYSTEM_INTERFACES.json"
                     ).read_text(encoding="utf-8"))
    n_pass = sum(1 for c in si["checks"] if c["passed"])
    check("FSV-INTERFACES", n_pass == len(si["checks"]) == 12,
          "system interfaces 12/12 (component-level evidence)",
          f"{n_pass}/{len(si['checks'])}")

    # -- materials ---------------------------------------------------------
    from sedep.bom import build_bom
    from sedep.bom.builder import cross_check
    rows = build_bom(ASM_RUN)
    defects = [r.part_number for r in rows if "DEFECT" in r.notes]
    check("FSV-MATERIALS", defects == [],
          "model materials match spec (OI-CAD-01 repaired, "
          "REPAIRS_S-2026-08-11-04)",
          f"defect rows: {defects or 'none'}")

    # -- BOM / model / registry / manifest consistency ---------------------
    faults = cross_check(rows, ASM_RUN)
    check("FSV-BOM", not faults, "BOM cross-checks clean (4 ways)",
          "; ".join(faults) or "clean")

    # -- drawings: existence and provenance completeness -------------------
    missing, unsourced = [], 0
    n_dims = 0
    for pn in sorted(REGISTRY | {"SEWCP-000"}):
        d = _drawing_dir(pn)
        sidecars = list(d.glob("*.provenance.json"))
        svgs = list(d.glob("*.svg"))
        pdfs = list(d.glob("*.pdf"))
        if not (sidecars and svgs and pdfs and len(svgs) == len(pdfs)):
            missing.append(pn)
            continue
        prov = json.loads(sidecars[0].read_text(encoding="utf-8"))
        for row in prov["dimensions"]:
            n_dims += 1
            if not str(row.get("source", "")).strip():
                unsourced += 1
    check("FSV-DRAWINGS", not missing and unsourced == 0,
          "11 drawings rendered (SVG+PDF) with fully-sourced dimensions",
          f"missing: {missing}; unsourced dims: {unsourced}; "
          f"dims total: {n_dims}")

    # -- deliverable digests reproduce -------------------------------------
    manifest = (ROOT / "cad/DELIVERABLES.md").read_text(encoding="utf-8")
    bom_path = BOM_CSV
    bom_hash = hashlib.sha256(bom_path.read_bytes()).hexdigest()[:16]
    check("FSV-MANIFEST-BOM", bom_hash in manifest,
          "BOM digest recorded in the deliverable manifest", bom_hash)
    strap = STEP_DIR / "SEWCP-901_RF_STRAP.step"
    strap_hash = hashlib.sha256(strap.read_bytes()).hexdigest()[:16]
    check("FSV-MANIFEST-STRAP", strap_hash in manifest,
          "re-issued strap STEP digest recorded", strap_hash)
    hanger = STEP_DIR / "SEWCP-902_SADDLE.step"
    hanger_hash = hashlib.sha256(hanger.read_bytes()).hexdigest()[:16]
    check("FSV-MANIFEST-HANGER", hanger_hash in manifest,
          "hanger STEP digest recorded", hanger_hash)
    asm = STEP_DIR / "SEWCP-000_MASTER_ASSEMBLY.step"
    asm_hash = hashlib.sha256(asm.read_bytes()).hexdigest()[:16]
    check("FSV-MANIFEST-ASM", asm_hash in manifest,
          "assembly STEP exported and digest recorded", asm_hash)
    final_obs = run["observed_assembly"]
    cp = next(o for o in final_obs["occurrences"]
              if (o.get("source_design") or "").startswith("SEWCP-200"))
    check("FSV-CP-CONTENT", abs(cp.get("mass_kg", 0) - 3.9936) < 0.001,
          "assembly CP occurrence carries the verified content (with taps)",
          f"mass {cp.get('mass_kg', 0):.4f} kg")

    # -- open residues are recorded, not silent ----------------------------
    open_items = (ROOT / ".ai/project/OPEN_ITEMS.md").read_text(encoding="utf-8")
    ids = ["ECR-D-013", "ECR-Q-012", "OI-CAD-01", "OI-CAD-02"]
    check("FSV-RESIDUES", all(i in open_items for i in ids),
          "every residue of this run is registered as an open item",
          ", ".join(ids))

    passed = all(c["passed"] for c in checks)
    body = {"checks": checks, "passed": passed,
            "known_defects_carried": sorted(KNOWN_DEFECTS),
            "assembly_run": run["run_id"],
            "note": ("PASS here means: every CAD-verifiable property of the "
                     "final design verifies from observed evidence, and every "
                     "non-verifiable or blocked item is explicitly carried.")}
    out = ROOT / "cad/runs/FINAL_SYSTEM_VERIFICATION.json"
    out.write_text(json.dumps(body, indent=1) + "\n", encoding="utf-8")
    for c in checks:
        print(("PASS " if c["passed"] else "FAIL ") + c["id"].ljust(22)
              + c["detail"][:70])
    print(("\nFINAL SYSTEM VERIFICATION: " +
           ("PASS" if passed else "FAIL")) + f"  ({len(checks)} checks)")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
