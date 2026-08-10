"""`python -m aief_clearance` - compute the spec/00 section 3.2 clearance claim."""

from __future__ import annotations

from pathlib import Path

from .check import check


def _repo() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".ai" / "project").is_dir():
            return parent
    return Path.cwd()


def main() -> int:
    report = check(_repo())
    print(f"features resolved from spec/00 section 3.2: {len(report.features)}")
    for f in report.features:
        print(f"  {f.name:52} r={f.radius:6.1f} n={len(f.angles):2}  span={f.r_span()[0]:6.1f}-{f.r_span()[1]:6.1f} +/-{f.theta_half():5.2f}deg  [{f.cite}]")
    for s in report.skipped:
        print(f"  skip {s}")
    print()
    for f in report.findings:
        print(f"FAIL  {f.a} @ {f.angle_a:g} deg  vs  {f.b} @ {f.angle_b:g} deg")
        print(f"      clearance {f.distance:.2f} mm, minimum wall {f.required:.2f} mm, short by {f.shortfall:.2f} mm")
    print("CLEARANCE OK" if report.ok else f"{len(report.findings)} INTERFERENCE(S)")
    return 0 if report.ok else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
