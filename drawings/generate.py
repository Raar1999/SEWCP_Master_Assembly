"""Generate the SEWCP drawing set into the repository.

    python drawings/generate.py [--only SEWCP-200,...] [--out DIR]

Outputs SVG (canonical) + PDF (print) + a provenance sidecar per drawing,
and prints a digest table for the deliverable manifest.

**Output goes into `drawings/`, not to an external root** - `ECR-D-015`. It
used to default to `D:\\AIEF_CAD_OUTPUT\\SEWCP\\DRAWINGS`, so a clone of this
repository could regenerate nothing it could then find. The assembly drawing
goes to `drawings/assembly/` and every part drawing to `drawings/parts/<part>/`,
the layout `SEDEP-PMP-002` §1 declares. `--out` still overrides, for a
scratch render that must not touch the tracked set.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "defs"))
sys.path.insert(0, str(HERE.parent / "src"))

DEFAULT_OUT = HERE          # the repository's own drawings/ tree - ECR-D-015

#: The assembly drawing and the part drawings live in different subtrees, per
#: `SEDEP-PMP-002` §1. Everything not named here is a part.
ASSEMBLY_PART = "SEWCP-000"


def _drawing_dir(out: Path, part: str) -> Path:
    return out / ("assembly" if part == ASSEMBLY_PART else f"parts/{part}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    from sewcp_assembly_drawing import assembly_drawing
    from sewcp_drawings import PART_DRAWINGS
    from aief_draw.pdf import render_drawing_pdf
    from aief_draw.svg import render_drawing_svg

    only = {s.strip() for s in args.only.split(",") if s.strip()}
    out = Path(args.out)
    written: list[Path] = []
    builders = dict(PART_DRAWINGS)
    builders["SEWCP-000"] = assembly_drawing
    for part, builder in builders.items():
        if only and part not in only:
            continue
        drawing = builder()
        drawing.validate()
        d_out = _drawing_dir(out, part)
        written += render_drawing_svg(drawing, d_out)
        written += render_drawing_pdf(drawing, d_out)
        n_dims = len(drawing.provenance())
        print(f"{drawing.number}: {len(drawing.sheets)} sheet(s), "
              f"{n_dims} provenanced dimension(s)")
    print()
    for p in sorted(written):
        h = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
        print(f"  {p.relative_to(out)}  {p.stat().st_size}  {h}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
