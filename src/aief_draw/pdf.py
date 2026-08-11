"""PDF renderer - the print form, from the same drawing model as SVG.

matplotlib is used purely as a vector canvas; conventions (weights,
dashes, provenance discipline) are the model's, not matplotlib's.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import patches  # noqa: E402

from aief_draw.model import (  # noqa: E402
    Arc, Circle, Dim, Drawing, Hatch, Line, Polyline, Sheet, Table, Text, View,
)

__all__ = ["render_drawing_pdf"]

_LW = {"outline": 1.0, "hidden": 0.5, "center": 0.35,
       "phantom": 0.5, "dim": 0.35}
_DASH = {"outline": "solid", "hidden": (0, (4, 2.4)),
         "center": (0, (12, 2, 2, 2)), "phantom": (0, (9, 2, 2, 2, 2, 2)),
         "dim": "solid"}


def _t(view: View, p):
    ox, oy = view.origin
    return ox + p[0] * view.scale, oy - p[1] * view.scale


def _seg(ax, a, b, layer):
    ax.plot([a[0], b[0]], [a[1], b[1]], color="black",
            lw=_LW[layer], linestyle=_DASH[layer], solid_capstyle="butt")


def _entity(ax, view, e):
    if isinstance(e, Line):
        _seg(ax, _t(view, e.p1), _t(view, e.p2), e.layer)
    elif isinstance(e, Circle):
        c = _t(view, e.center)
        ax.add_patch(patches.Circle(c, e.diameter / 2 * view.scale,
                                    fill=False, ec="black",
                                    lw=_LW[e.layer], ls=_DASH[e.layer]))
    elif isinstance(e, Arc):
        c = _t(view, e.center)
        r = e.radius * view.scale
        ax.add_patch(patches.Arc(c, 2 * r, 2 * r,
                                 theta1=-e.end_deg, theta2=-e.start_deg,
                                 ec="black", lw=_LW[e.layer]))
    elif isinstance(e, Polyline):
        pts = [_t(view, p) for p in e.points]
        if e.closed:
            pts.append(pts[0])
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color="black",
                lw=_LW[e.layer], linestyle=_DASH[e.layer])
    elif isinstance(e, Hatch):
        pts = [_t(view, p) for p in e.points]
        ax.add_patch(patches.Polygon(
            pts, closed=True, fill=False, ec="black", lw=0.6,
            hatch="xx" if e.style == "cross" else "//"))
        if e.label:
            cx = sum(p[0] for p in pts) / len(pts)
            cy = sum(p[1] for p in pts) / len(pts)
            ax.text(cx, cy, e.label, fontsize=6, ha="center", va="center")
    elif isinstance(e, Text):
        p = _t(view, e.at)
        ax.text(p[0], p[1], e.text, fontsize=e.height * 2.83 * 0.9,
                ha={"start": "left", "middle": "center",
                    "end": "right"}[e.anchor], va="baseline",
                family="monospace")


def _dim(ax, view, d: Dim):
    def arrow(a, b):
        ax.annotate("", xy=a, xytext=b,
                    arrowprops=dict(arrowstyle="->", lw=0.5, color="black"))
    if d.kind == "linear":
        p1, p2 = _t(view, d.p1), _t(view, d.p2)
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        q1 = (p1[0] + nx * d.offset, p1[1] + ny * d.offset)
        q2 = (p2[0] + nx * d.offset, p2[1] + ny * d.offset)
        _seg(ax, p1, q1, "dim")
        _seg(ax, p2, q2, "dim")
        arrow(q1, q2)
        arrow(q2, q1)
        ang = math.degrees(math.atan2(q2[1] - q1[1], q2[0] - q1[0]))
        if not -90 <= ang <= 90:
            ang += 180
        ax.text((q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2 - 1.2, d.label(),
                fontsize=6, ha="center", rotation=ang,
                rotation_mode="anchor", family="monospace")
    elif d.kind in ("diameter", "radius"):
        c = _t(view, d.p1)
        r = (d.value / 2 if d.kind == "diameter" else d.value) * view.scale
        a = math.radians(-d.angle_deg)
        tip = (c[0] + r * math.cos(a), c[1] + r * math.sin(a))
        end = (tip[0] + 8 * math.cos(a), tip[1] + 8 * math.sin(a))
        arrow(tip, end)
        ha = "left" if math.cos(a) >= 0 else "right"
        ax.text(end[0], end[1] - 1, d.label(), fontsize=6, ha=ha,
                family="monospace")
    elif d.kind == "angular":
        c = _t(view, d.p1)
        amid = math.radians(-((d.a1 or 0) + (d.a2 or 0)) / 2)
        ax.text(c[0] + (d.offset + 3) * math.cos(amid),
                c[1] + (d.offset + 3) * math.sin(amid), d.label(),
                fontsize=6, ha="center", family="monospace")
    elif d.kind == "note":
        p = _t(view, d.p1)
        a = math.radians(-d.angle_deg)
        end = (p[0] + 10 * math.cos(a), p[1] + 10 * math.sin(a))
        arrow(p, end)
        ha = "left" if math.cos(a) >= 0 else "right"
        ax.text(end[0], end[1] - 1, d.label(), fontsize=5.5, ha=ha,
                family="monospace")


def render_drawing_pdf(drawing: Drawing, out_dir: str | Path) -> list[Path]:
    drawing.validate()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for i, sheet in enumerate(drawing.sheets, start=1):
        w, h = sheet.wh
        fig, ax = plt.subplots(figsize=(w / 25.4, h / 25.4))
        ax.set_xlim(0, w)
        ax.set_ylim(h, 0)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(patches.Rectangle((10, 10), w - 20, h - 20, fill=False,
                                       ec="black", lw=1.2))
        for view in sheet.views:
            for e in view.entities:
                _entity(ax, view, e)
            for d in view.dims:
                _dim(ax, view, d)
            if view.caption:
                ax.text(view.origin[0], view.origin[1] + 6, view.caption,
                        fontsize=8, ha="center", family="monospace")
        for tb in sheet.tables:
            x0, y0 = tb.at
            y = y0
            if tb.title:
                ax.text(x0, y - 1.5, tb.title, fontsize=7, family="monospace")
            for row in tb.rows:
                x = x0
                for c, cell in enumerate(row):
                    ax.add_patch(patches.Rectangle(
                        (x, y), tb.col_widths[c], tb.row_height, fill=False,
                        ec="black", lw=0.3))
                    ax.text(x + 1.0, y + tb.row_height - 1.4, cell,
                            fontsize=tb.text_height * 2.4, family="monospace")
                    x += tb.col_widths[c]
                y += tb.row_height
        if sheet.notes:
            ax.text(14, 18, "NOTES:", fontsize=7, family="monospace")
            for j, note in enumerate(sheet.notes):
                ax.text(14, 22 + j * 4, f"{j + 1}. {note}", fontsize=6,
                        family="monospace")
        fields = {**drawing.fields, **sheet.fields}
        tb_rows = [("TITLE", f"{drawing.title} — {sheet.title}"),
                   ("NUMBER", sheet.number), ("REV", drawing.revision),
                   ("MATERIAL", fields.get("material", "—")),
                   ("FINISH", fields.get("finish", "—")),
                   ("SCALE", fields.get("scale", "—")),
                   ("UNITS", "mm"), ("DATE", fields.get("date", "—")),
                   ("ORIGIN", fields.get("origin", "AIEF autonomous run"))]
        bw, bh = 180.0, 30.0
        x0, y0 = w - 10 - bw, h - 10 - bh
        cw, ch = bw / 3, bh / 3
        ax.add_patch(patches.Rectangle((x0, y0), bw, bh, fill=False,
                                       ec="black", lw=0.8))
        for k, (key, val) in enumerate(tb_rows):
            cx, cy = x0 + (k % 3) * cw, y0 + (k // 3) * ch
            ax.add_patch(patches.Rectangle((cx, cy), cw, ch, fill=False,
                                           ec="black", lw=0.3))
            ax.text(cx + 1.2, cy + 3.2, key, fontsize=4.5, family="monospace")
            ax.text(cx + 1.2, cy + 8.0, val, fontsize=6, family="monospace")
        p = out / f"{drawing.number}_Sh{i}.pdf"
        fig.savefig(p, format="pdf", bbox_inches=None, pad_inches=0)
        plt.close(fig)
        written.append(p)
    return written
