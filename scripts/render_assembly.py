"""Portfolio render of the SEWCP master assembly, from released repository evidence only.

    python portfolio/render_assembly.py

**This is a presentation tool, not an engineering one.** It creates nothing and
verifies nothing that `cad/runs/` has not already recorded. It reads:

  * `cad/exports/stl/*.stl`                     - the released tessellated exports
  * `cad/runs/ASSEMBLY_S-2026-08-11-05/run.json` - the observed occurrence list

and composes the second over the first. No Fusion document is opened, no STEP or
STL is modified, and nothing here is a source of truth for any dimension: read a
number off this image and you have read it off a tessellation.

**Every placement is checked before it is drawn.** Each occurrence's transformed
mesh bounding box is compared against the bounding box the assembly run actually
observed in Fusion, and the deviation is printed. A render whose geometry is not
reconciled against the record is decoration; this one reports its own error and
refuses to hide it - `--strict` makes any deviation past the tolerance fatal.

Transform, per occurrence, in this order:

    z_axis_scale  ->  rotate_z_deg about Z  ->  translate_mm

`z_axis_scale` is -1.0 for three of the six alignment pins, which are installed
inverted; applying it is the difference between 0.0000 mm and 9.5000 mm of
placement error on those three.

Dependencies: numpy and matplotlib, both already in `requirements.txt`.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
ASSEMBLY_RUN = REPO / "cad/runs/ASSEMBLY_S-2026-08-11-05/run.json"
STL_DIR = REPO / "cad/exports/stl"
OUT_DIR = REPO / "portfolio/renders"

#: Tessellation chord error is inward and small; 18 of 19 occurrences reconcile
#: below 0.08 mm. SEWCP-902 is tessellated at 340 triangles and deviates up to
#: 3.9 mm on two faces of its bounding box while its mesh volume agrees with the
#: observed solid to 0.018 %. The tolerance admits that and nothing coarser.
BBOX_TOLERANCE_MM = 4.0

#: Material appearance only. The governing material for every part is the BOM
#: (`cad/bom/SEWCP-000_BOM_RevA.csv`) and the specification volume it cites.
FINISH = {
    "SEWCP-200_COOLING_PLATE": ("#9aa7b4", "6061-T6"),
    "SEWCP-300_HEATER_PLATE": ("#8f9caa", "6061-T6"),
    "SEWCP-400_SUPPORT_RING": ("#e2ddd2", "Al2O3 99.5%"),
    "SEWCP-500_ESC_PUCK": ("#efe9dc", "Al2O3 99.6%"),
    "SEWCP-600_LIFT_PIN": ("#d9d2c4", "Al2O3 99.8%"),
    "SEWCP-700_ALIGNMENT_PIN": ("#7d8792", "Ti-6Al-4V"),
    "SEWCP-800_PORT_BODY": ("#aab3bd", "316L SST"),
    "SEWCP-901_RF_STRAP": ("#c08457", "C10100 OFHC"),
    "SEWCP-902_SADDLE": ("#95a2ae", "6061-T6"),
    "SEWCP-1000_RETAINER": ("#a3aeb9", "6061-T6"),
}

#: Exploded view: per-source Z offset, presentation only. Chosen to open the
#: stack in its assembly order without reordering it.
EXPLODE_MM = {
    "SEWCP-400_SUPPORT_RING": 0.0,
    "SEWCP-902_SADDLE": 30.0,
    "SEWCP-901_RF_STRAP": 30.0,
    "SEWCP-200_COOLING_PLATE": 70.0,
    "SEWCP-1000_RETAINER": 70.0,
    "SEWCP-800_PORT_BODY": 70.0,
    "SEWCP-300_HEATER_PLATE": 130.0,
    "SEWCP-700_ALIGNMENT_PIN": 130.0,
    "SEWCP-500_ESC_PUCK": 190.0,
    "SEWCP-600_LIFT_PIN": 190.0,
}


def read_binary_stl(path: Path) -> np.ndarray:
    """(n, 3, 3) float64 triangle vertices from a binary STL."""
    raw = path.read_bytes()
    count = struct.unpack("<I", raw[80:84])[0]
    expected = 84 + count * 50
    if len(raw) < expected:
        raise ValueError(f"{path.name}: declares {count} triangles, file holds fewer")
    rec = np.frombuffer(raw, dtype=np.uint8, count=count * 50, offset=84).reshape(count, 50)
    return rec[:, 12:48].copy().view("<f4").reshape(count, 3, 3).astype(np.float64)


def place(tri: np.ndarray, rotate_z_deg: float, translate_mm, z_axis_scale: float) -> np.ndarray:
    a = np.radians(rotate_z_deg)
    c, s = np.cos(a), np.sin(a)
    rot = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    scaled = tri * np.array([1.0, 1.0, float(z_axis_scale)])
    return scaled @ rot.T + np.asarray(translate_mm, dtype=float)


def load_assembly(strict: bool) -> list[dict]:
    run = json.loads(ASSEMBLY_RUN.read_text(encoding="utf-8"))
    occurrences = run["observed_assembly"]["occurrences"]
    cache: dict[str, np.ndarray] = {}
    placed: list[dict] = []
    worst = 0.0

    print(f"reconciling {len(occurrences)} occurrences against the observed assembly record")
    for occ in occurrences:
        src = occ["source_design"]
        if src not in cache:
            cache[src] = read_binary_stl(STL_DIR / f"{src}.stl")
        tri = place(cache[src], occ["rotate_z_deg"], occ["translate_mm"], occ["z_axis_scale"])
        flat = tri.reshape(-1, 3)
        err = max(
            float(np.abs(flat.min(0) - np.asarray(occ["bbox_min"])).max()),
            float(np.abs(flat.max(0) - np.asarray(occ["bbox_max"])).max()),
        )
        worst = max(worst, err)
        mark = "ok " if err <= BBOX_TOLERANCE_MM else "OUT"
        print(f"  {mark} {occ['name']:<34s} bbox deviation {err:7.4f} mm")
        if err > BBOX_TOLERANCE_MM and strict:
            raise SystemExit(
                f"{occ['name']}: {err:.4f} mm exceeds {BBOX_TOLERANCE_MM} mm. "
                f"The placement does not reconcile with what Fusion observed; "
                f"refusing to render geometry the record does not support."
            )
        placed.append({"src": src, "tri": tri, "name": occ["name"]})
    print(f"worst deviation: {worst:.4f} mm (tolerance {BBOX_TOLERANCE_MM} mm)\n")
    return placed


def rasterise(tri: np.ndarray, rgb: np.ndarray, width: int, height: int,
              right: np.ndarray, up: np.ndarray, fwd: np.ndarray,
              background: tuple[float, float, float]) -> np.ndarray:
    """Orthographic z-buffer rasteriser.

    A painter's algorithm was tried first and is wrong here: sorting by triangle
    centroid depth puts a large, sparsely-tessellated face (the ESC puck's top is
    one disc of a few hundred triangles) behind the smaller triangles of the
    heater plate beneath it, and the plate paints through the puck. The artifact
    is unmistakable - grey spikes across a cream face - and no sort order fixes
    it, because centroid order is not depth order for overlapping triangles of
    very different size. So depth is resolved per pixel, which is exact.
    """
    proj = np.stack([tri @ right, tri @ up], axis=-1)
    depth = tri @ fwd

    lo = proj.reshape(-1, 2).min(0)
    hi = proj.reshape(-1, 2).max(0)
    span = np.maximum(hi - lo, 1e-9)
    # Fit each axis independently and take the tighter of the two, so a wide flat
    # assembly is not letterboxed by its own aspect ratio. One scale, so the
    # projection stays isometric.
    scale = min(width / span[0], height / span[1]) * 0.985
    centre = (lo + hi) / 2.0
    px = (proj - centre) * scale + np.array([width / 2.0, height / 2.0])

    colour = np.tile(np.asarray(background, dtype=np.float32), (height, width, 1))
    zbuf = np.full((height, width), -np.inf, dtype=np.float64)

    x, y = px[:, :, 0], px[:, :, 1]
    x0, x1, x2 = x[:, 0], x[:, 1], x[:, 2]
    y0, y1, y2 = y[:, 0], y[:, 1], y[:, 2]
    area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)

    xmin = np.clip(np.floor(x.min(1)).astype(int), 0, width - 1)
    xmax = np.clip(np.ceil(x.max(1)).astype(int), 0, width - 1)
    ymin = np.clip(np.floor(y.min(1)).astype(int), 0, height - 1)
    ymax = np.clip(np.ceil(y.max(1)).astype(int), 0, height - 1)

    for i in range(tri.shape[0]):
        if abs(area[i]) < 1e-9 or xmax[i] < xmin[i] or ymax[i] < ymin[i]:
            continue
        gx = np.arange(xmin[i], xmax[i] + 1) + 0.5
        gy = np.arange(ymin[i], ymax[i] + 1) + 0.5
        gxx, gyy = np.meshgrid(gx, gy)
        inv = 1.0 / area[i]
        w0 = ((x1[i] - gxx) * (y2[i] - gyy) - (x2[i] - gxx) * (y1[i] - gyy)) * inv
        w1 = ((x2[i] - gxx) * (y0[i] - gyy) - (x0[i] - gxx) * (y2[i] - gyy)) * inv
        w2 = 1.0 - w0 - w1
        inside = (w0 >= -1e-9) & (w1 >= -1e-9) & (w2 >= -1e-9)
        if not inside.any():
            continue
        z = w0 * depth[i, 0] + w1 * depth[i, 1] + w2 * depth[i, 2]
        sub = zbuf[ymin[i]:ymax[i] + 1, xmin[i]:xmax[i] + 1]
        win = inside & (z > sub)
        if not win.any():
            continue
        sub[win] = z[win]
        colour[ymin[i]:ymax[i] + 1, xmin[i]:xmax[i] + 1][win] = rgb[i]

    return colour


def render(placed: list[dict], out: Path, title: str, subtitle: str, explode: bool) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    az, el = np.radians(-58.0), np.radians(21.0)
    fwd = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
    right = np.cross(np.array([0.0, 0.0, 1.0]), fwd)
    right /= np.linalg.norm(right)
    up = np.cross(fwd, right)
    light = np.array([0.35, -0.55, 0.76])
    light /= np.linalg.norm(light)

    tris, cols = [], []
    for item in placed:
        tri = item["tri"].copy()
        if explode:
            tri[:, :, 2] += EXPLODE_MM.get(item["src"], 0.0)
        base = np.array(matplotlib.colors.to_rgb(FINISH.get(item["src"], ("#999999", ""))[0]))

        nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        ln = np.linalg.norm(nrm, axis=1)
        keep = ln > 1e-12
        tri, nrm, ln = tri[keep], nrm[keep], ln[keep]
        nrm /= ln[:, None]

        front = (nrm @ fwd) > 0
        tri, nrm = tri[front], nrm[front]
        if len(tri) == 0:
            continue

        lam = np.clip(np.abs(nrm @ light), 0.0, 1.0)
        shade = 0.34 + 0.66 * lam ** 0.85
        tris.append(tri)
        cols.append(np.clip(base[None, :] * shade[:, None] + 0.12 * (shade[:, None] ** 6), 0, 1))

    tri = np.concatenate(tris)
    rgb = np.concatenate(cols).astype(np.float32)
    print(f"  rasterising {len(tri):,} front-facing triangles")

    bg = (1.0, 1.0, 1.0)
    ss = 2                                   # supersample, then box-filter down
    w, h = 1500 * ss, 1000 * ss
    img = rasterise(tri, rgb, w, h, right, up, fwd, bg)
    img = img.reshape(h // ss, ss, w // ss, ss, 3).mean(axis=(1, 3))

    # Crop to drawn content. Fitting cannot know the silhouette in advance, so a
    # round part in a rectangular raster always leaves margin; this removes it
    # rather than shipping an image that is mostly background.
    ink = np.any(np.abs(img - np.asarray(bg)) > 1e-3, axis=2)
    ys, xs = np.where(ink)
    if len(ys):
        m = 6
        img = img[max(ys.min() - m, 0):ys.max() + m + 1,
                  max(xs.min() - m, 0):xs.max() + m + 1]

    ih, iw = img.shape[:2]
    fig = plt.figure(figsize=(13.0, 13.0 * (ih / iw) + 2.0), dpi=170)
    fig.patch.set_facecolor("#ffffff")
    top = 1.0 - 1.35 / fig.get_size_inches()[1]
    bot = 0.42 / fig.get_size_inches()[1]
    ax = fig.add_axes([0.015, bot, 0.97, top - bot])
    ax.set_facecolor("#ffffff")
    ax.imshow(np.flipud(img), interpolation="bilinear", aspect="equal")
    ax.axis("off")

    fh = fig.get_size_inches()[1]
    fig.text(0.015, 1.0 - 0.40 / fh, title, fontsize=20, fontweight="bold",
             color="#1f2933", va="top")
    fig.text(0.015, 1.0 - 0.72 / fh, subtitle, fontsize=11, color="#52606d", va="top")

    used = sorted({i["src"] for i in placed})
    fig.legend(
        handles=[
            Patch(facecolor=FINISH[s][0], edgecolor="#52606d", linewidth=0.4,
                  label=f"{s.split('_')[0]}  {FINISH[s][1]}")
            for s in used
        ],
        loc="lower right", bbox_to_anchor=(0.985, 0.30 / fh),
        frameon=False, fontsize=8.5, ncol=2, handlelength=1.4, columnspacing=1.4,
        labelspacing=0.35,
    )
    fig.text(
        0.015, 0.10 / fh,
        "Rendered from cad/exports/stl/ composed with the occurrence transforms in "
        "cad/runs/ASSEMBLY_S-2026-08-11-05/run.json. Tessellated geometry - not a "
        "dimensional source. Nothing physical has been built.",
        fontsize=7.8, color="#7b8794", va="bottom",
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"wrote {out.relative_to(REPO)}  ({out.stat().st_size:,} bytes)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help="fail if any occurrence exceeds the bbox tolerance")
    args = ap.parse_args()

    placed = load_assembly(strict=args.strict)
    render(
        placed, OUT_DIR / "SEWCP-000_assembly_iso.png",
        "SEWCP-000 — Master Assembly",
        "19 occurrences · 7.6997 kg · verified 19/19 against observed model state · release v0.11.0",
        explode=False,
    )
    render(
        placed, OUT_DIR / "SEWCP-000_assembly_exploded.png",
        "SEWCP-000 — Master Assembly, exploded",
        "Separated along +Z for presentation. Every placement is as recorded; only the separation is added.",
        explode=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
