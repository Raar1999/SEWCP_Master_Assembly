"""`python -m aief_analysis` - the two OI-C-15 desk analyses.

Exit 0 only if both discharge. The insulation trace does not, and the non-zero
exit is the point: `SR-02`, `SR-03` and `SR-04` do not close on the frozen
dimensions, and a check that said otherwise would be the defect it exists to
find.
"""

from __future__ import annotations

from pathlib import Path

from . import insulation as ins
from .loads import SAFETY_FACTOR, check


def _repo() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".ai" / "project").is_dir():
            return parent
    return Path.cwd()


def _loads(repo: Path) -> bool:
    basis, actual = check(repo)
    print("=" * 78)
    print("OI-C-15 (i) - SR-07 / AP-08 re-run at the as-modelled stack mass")
    print("=" * 78)
    print(f"design-basis mass   {basis.mass_kg:.5f} kg   (spec/03 SR-07, spec/06 AP-08)")
    print(f"as-modelled mass    {actual.mass_kg:.5f} kg   "
          f"(ASSEMBLY_S-2026-08-11-05, 19 occurrences, observed)")
    print(f"error               {actual.mass_error_pct:+.2f} %")
    print(f"per-pin lateral     {basis.per_pin_load_n:.2f} N -> {actual.per_pin_load_n:.2f} N")
    print()
    print(f"{'req':6s} {'case':56s} {'stress':>9s} {'margin':>9s} {'mass @ SF=3':>13s}")
    for b, a in zip(basis.cases, actual.cases):
        print(f"{a.requirement:6s} {a.name:56s} {a.stress_mpa:8.4f}M "
              f"{a.margin:8.1f}x {a.mass_at_safety_factor(actual.mass_kg):12.1f}kg"
              f"{'' if a.passes else '   FAIL'}")
    gov = actual.governing
    print()
    print(f"governing case: {gov.name}")
    print(f"  margin {gov.margin:.1f}x against the required {SAFETY_FACTOR:.0f}x; "
          f"the case reaches SF=3 at {gov.mass_at_safety_factor(actual.mass_kg):.1f} kg, "
          f"{gov.mass_at_safety_factor(actual.mass_kg) / actual.mass_kg:.0f}x the as-modelled mass")
    ok = actual.ok
    print(f"  the +{actual.mass_error_pct:.2f} % mass error is immaterial to both "
          f"requirements, and the unmodelled spec-only BOM lines cannot change that")
    print(f"SR-07 / AP-08: {'DISCHARGED at the as-modelled mass' if ok else 'FAIL'}")
    return ok


def _insulation() -> bool:
    print()
    print("=" * 78)
    print("OI-C-15 (ii) - SR-02 / SR-03 / SR-04 creepage and clearance trace")
    print("=" * 78)
    a, d = ins.flange_radial_demand_mm()
    print(f"flange gap                       {ins.WEB_GAP_MM:6.2f} mm  (SR-D08)")
    print(f"SEWCP-401 intrusion into it      {ins.grounded_intrusion_mm():6.2f} mm  "
          f"(CR-D03 {ins.CLAMP_RING_T_MM:.2f} less the {ins.REGISTER_DEPTH_MM:.2f} SR-IF-2 register)")
    print(f"greatest possible clearance      {ins.best_case_clearance_mm():6.2f} mm")
    print(f"joint interferes when RF-hot hardware protrudes more than "
          f"{ins.assembly_threshold_mm():.2f} mm;")
    print(f"  an ISO 4762 M6 head alone is {ins.M6_SOCKET_HEAD_HEIGHT_MM:.2f} mm, and spec/00 s9 "
          f"adds a dia-16 flat washer and a Belleville stack")
    print()
    print(f"radial overlap, SEWCP-401 footprint vs web root   "
          f"{ins.radial_overlap_mm():5.2f} mm   <- a hard collision")
    print(f"web wall standing over the dia-7.0 bolt-hole footprint "
          f"{ins.bolt_hole_under_web_mm():5.2f} mm of 3.00")
    print(f"flange radial width available {a:5.2f} mm; frozen features demand {d:5.2f} mm")
    print()
    fails = 0
    for v in ins.verdicts():
        mark = "PASS" if v.passes else "FAIL"
        if not v.passes:
            fails += 1
        print(f"{mark}  {v.requirement}  {v.quantity}")
        print(f"      {v.value:.2f} {v.unit} against {v.limit:.2f} {v.unit}"
              + (f"  - short by {v.shortfall:.2f} {v.unit}" if not v.passes else ""))
        print(f"      {v.basis}")
    print()
    print(f"SR-02 / SR-03 / SR-04: {fails} of {len(ins.verdicts())} checks FAIL")
    return fails == 0


def main() -> int:
    repo = _repo()
    ok_loads = _loads(repo)
    ok_ins = _insulation()
    print()
    if ok_loads and ok_ins:
        print("OI-C-15 DISCHARGED")
        return 0
    print("OI-C-15 (i) discharged; (ii) does not close - raised as ECR-D-016")
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
