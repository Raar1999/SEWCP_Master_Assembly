"""SVG renderer. One sheet -> one SVG file, plus a provenance sidecar.

Print-form conventions: black lines on white, ISO-ish line weights,
sheet coordinates in mm (1 SVG user unit = 1 mm). Model Y is up; SVG Y is
down; views flip about their origin.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

from aief_draw.model import (
    Arc, Circle, Dim, Drawing, Hatch, Line, Polyline, Sheet, Table, Text, View,
)

__all__ = ["render_drawing_svg"]

_STYLE = {
    "outline": 'stroke="#000" stroke-width="0.5" fill="none"',
    "hidden": 'stroke="#000" stroke-width="0.25" stroke-dasharray="2,1.2" fill="none"',
    "center": 'stroke="#000" stroke-width="0.18" stroke-dasharray="8,1.5,1.5,1.5" fill="none"',
    "phantom": 'stroke="#555" stroke-width="0.25" stroke-dasharray="6,1.5,1.5,1.5,1.5,1.5" fill="none"',
    "dim": 'stroke="#000" stroke-width="0.18" fill="none"',
}
_FONT = 'font-family="ISOCPEUR, Consolas, monospace"'


def _t(view: View, p: tuple[float, float]) -> tuple[float, float]:
    ox, oy = view.origin
    return ox + p[0] * view.scale, oy - p[1] * view.scale


def _text(at, s, h=2.5, anchor="start", angle=0.0) -> str:
    x, y = at
    rot = f' transform="rotate({angle:g} {x:g} {y:g})"' if angle else ""
    return (f'<text x="{x:.3f}" y="{y:.3f}" font-size="{h:g}" {_FONT} '
            f'text-anchor="{anchor}"{rot}>{escape(str(s))}</text>')


def _arrow(tip, ang_deg, size=1.2) -> str:
    a = math.radians(ang_deg)
    x, y = tip
    p1 = (x - size * 3 * math.cos(a) + size * math.sin(a),
          y - size * 3 * math.sin(a) - size * math.cos(a))
    p2 = (x - size * 3 * math.cos(a) - size * math.sin(a),
          y - size * 3 * math.sin(a) + size * math.cos(a))
    return (f'<path d="M {x:.3f} {y:.3f} L {p1[0]:.3f} {p1[1]:.3f} '
            f'L {p2[0]:.3f} {p2[1]:.3f} Z" fill="#000" stroke="none"/>')


def _render_entity(view: View, e) -> str:
    if isinstance(e, Line):
        (x1, y1), (x2, y2) = _t(view, e.p1), _t(view, e.p2)
        return (f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" '
                f'y2="{y2:.3f}" {_STYLE[e.layer]}/>')
    if isinstance(e, Circle):
        (cx, cy) = _t(view, e.center)
        r = e.diameter / 2 * view.scale
        return f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}" {_STYLE[e.layer]}/>'
    if isinstance(e, Arc):
        r = e.radius * view.scale
        a1, a2 = math.radians(e.start_deg), math.radians(e.end_deg)
        p1 = _t(view, (e.center[0] + e.radius * math.cos(a1),
                       e.center[1] + e.radius * math.sin(a1)))
        p2 = _t(view, (e.center[0] + e.radius * math.cos(a2),
                       e.center[1] + e.radius * math.sin(a2)))
        sweep = (e.end_deg - e.start_deg) % 360.0
        large = 1 if sweep > 180 else 0
        return (f'<path d="M {p1[0]:.3f} {p1[1]:.3f} A {r:.3f} {r:.3f} 0 '
                f'{large} 0 {p2[0]:.3f} {p2[1]:.3f}" {_STYLE[e.layer]}/>')
    if isinstance(e, Polyline):
        pts = " ".join(f"{x:.3f},{y:.3f}" for x, y in
                       (_t(view, p) for p in e.points))
        tag = "polygon" if e.closed else "polyline"
        return f'<{tag} points="{pts}" {_STYLE[e.layer]}/>'
    if isinstance(e, Hatch):
        pts = " ".join(f"{x:.3f},{y:.3f}" for x, y in
                       (_t(view, p) for p in e.points))
        fill = ("url(#hatchX)" if e.style == "cross" else "url(#hatch)")
        out = (f'<polygon points="{pts}" fill="{fill}" '
               f'stroke="#000" stroke-width="0.3"/>')
        if e.label:
            xs = [_t(view, p)[0] for p in e.points]
            ys = [_t(view, p)[1] for p in e.points]
            out += _text((sum(xs) / len(xs), sum(ys) / len(ys)), e.label,
                         2.0, "middle")
        return out
    if isinstance(e, Text):
        return _text(_t(view, e.at), e.text, e.height, e.anchor)
    raise TypeError(f"unknown entity {e!r}")


def _render_dim(view: View, d: Dim) -> str:
    out: list[str] = []
    if d.kind == "linear":
        p1, p2 = _t(view, d.p1), _t(view, d.p2)
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        off = d.offset
        q1 = (p1[0] + nx * off, p1[1] + ny * off)
        q2 = (p2[0] + nx * off, p2[1] + ny * off)
        for a, b in ((p1, q1), (p2, q2)):
            out.append(f'<line x1="{a[0]:.3f}" y1="{a[1]:.3f}" x2="{b[0]:.3f}" '
                       f'y2="{b[1]:.3f}" {_STYLE["dim"]}/>')
        out.append(f'<line x1="{q1[0]:.3f}" y1="{q1[1]:.3f}" x2="{q2[0]:.3f}" '
                   f'y2="{q2[1]:.3f}" {_STYLE["dim"]}/>')
        ang = math.degrees(math.atan2(q2[1] - q1[1], q2[0] - q1[0]))
        out.append(_arrow(q1, ang + 180))
        out.append(_arrow(q2, ang))
        mid = ((q1[0] + q2[0]) / 2, (q1[1] + q2[1]) / 2 - 1.0)
        t_ang = ang if -90 <= ang <= 90 else ang + 180
        out.append(_text(mid, d.label(), 2.5, "middle", t_ang))
    elif d.kind in ("diameter", "radius"):
        c = _t(view, d.p1)
        r = (d.value / 2 if d.kind == "diameter" else d.value) * view.scale
        a = math.radians(-d.angle_deg)
        tip = (c[0] + r * math.cos(a), c[1] + r * math.sin(a))
        end = (tip[0] + 8 * math.cos(a), tip[1] + 8 * math.sin(a))
        lx = end[0] + (6 if math.cos(a) >= 0 else -6)
        out.append(f'<path d="M {tip[0]:.3f} {tip[1]:.3f} L {end[0]:.3f} '
                   f'{end[1]:.3f} L {lx:.3f} {end[1]:.3f}" {_STYLE["dim"]}/>')
        out.append(_arrow(tip, math.degrees(a) + 180))
        anchor = "start" if math.cos(a) >= 0 else "end"
        out.append(_text((lx + (1 if anchor == "start" else -1), end[1] - 1),
                         d.label(), 2.5, anchor))
    elif d.kind == "angular":
        c = _t(view, d.p1)
        r = d.offset
        a1, a2 = math.radians(-(d.a1 or 0)), math.radians(-(d.a2 or 0))
        p1 = (c[0] + r * math.cos(a1), c[1] + r * math.sin(a1))
        p2 = (c[0] + r * math.cos(a2), c[1] + r * math.sin(a2))
        large = 1 if abs((d.a2 or 0) - (d.a1 or 0)) > 180 else 0
        out.append(f'<path d="M {p1[0]:.3f} {p1[1]:.3f} A {r:.3f} {r:.3f} 0 '
                   f'{large} 1 {p2[0]:.3f} {p2[1]:.3f}" {_STYLE["dim"]}/>')
        amid = (a1 + a2) / 2
        out.append(_text((c[0] + (r + 3) * math.cos(amid),
                          c[1] + (r + 3) * math.sin(amid)),
                         d.label(), 2.5, "middle"))
    elif d.kind == "note":
        p = _t(view, d.p1)
        a = math.radians(-d.angle_deg)
        end = (p[0] + 10 * math.cos(a), p[1] + 10 * math.sin(a))
        out.append(f'<line x1="{p[0]:.3f}" y1="{p[1]:.3f}" x2="{end[0]:.3f}" '
                   f'y2="{end[1]:.3f}" {_STYLE["dim"]}/>')
        out.append(_arrow(p, math.degrees(a) + 180))
        anchor = "start" if math.cos(a) >= 0 else "end"
        out.append(_text((end[0] + (1 if anchor == "start" else -1),
                          end[1] - 1), d.label(), 2.2, anchor))
    return "\n".join(out)


def _title_block(drawing: Drawing, sheet: Sheet) -> str:
    w, h = sheet.wh
    bw, bh = 180.0, 30.0
    x0, y0 = w - 10 - bw, h - 10 - bh
    fields = {**drawing.fields, **sheet.fields}
    rows = [
        ("TITLE", f"{drawing.title} — {sheet.title}"),
        ("NUMBER", sheet.number), ("REV", drawing.revision),
        ("MATERIAL", fields.get("material", "—")),
        ("FINISH", fields.get("finish", "—")),
        ("SCALE", fields.get("scale", "—")),
        ("UNITS", "mm"), ("DATE", fields.get("date", "—")),
        ("ORIGIN", fields.get("origin", "AIEF autonomous run")),
    ]
    out = [f'<rect x="{x0}" y="{y0}" width="{bw}" height="{bh}" '
           f'fill="white" stroke="#000" stroke-width="0.5"/>']
    cw, ch = bw / 3, bh / 3
    for i, (k, v) in enumerate(rows):
        cx = x0 + (i % 3) * cw
        cy = y0 + (i // 3) * ch
        out.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" '
                   f'fill="none" stroke="#000" stroke-width="0.2"/>')
        out.append(_text((cx + 1.2, cy + 3.2), k, 1.8))
        out.append(_text((cx + 1.2, cy + 7.8), v, 2.4))
    return "\n".join(out)


def _table(tb: Table) -> str:
    out = []
    x0, y0 = tb.at
    total_w = sum(tb.col_widths)
    y = y0
    if tb.title:
        out.append(_text((x0, y - 1.5), tb.title, 2.6))
    for r, row in enumerate(tb.rows):
        x = x0
        for c, cell in enumerate(row):
            wcol = tb.col_widths[c]
            out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{wcol:.2f}" '
                       f'height="{tb.row_height}" fill="none" '
                       f'stroke="#000" stroke-width="0.2"/>')
            out.append(_text((x + 1.0, y + tb.row_height - 1.4),
                             cell, tb.text_height))
            x += wcol
        y += tb.row_height
    return "\n".join(out)


def render_sheet_svg(drawing: Drawing, sheet: Sheet) -> str:
    w, h = sheet.wh
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" '
        f'height="{h}mm" viewBox="0 0 {w} {h}">',
        '<defs>'
        '<pattern id="hatch" width="3" height="3" patternTransform="rotate(45)"'
        ' patternUnits="userSpaceOnUse">'
        '<line x1="0" y1="0" x2="0" y2="3" stroke="#000" stroke-width="0.25"/>'
        '</pattern>'
        '<pattern id="hatchX" width="3" height="3" '
        'patternTransform="rotate(45)" patternUnits="userSpaceOnUse">'
        '<line x1="0" y1="0" x2="0" y2="3" stroke="#000" stroke-width="0.25"/>'
        '<line x1="0" y1="1.5" x2="3" y2="1.5" stroke="#000" '
        'stroke-width="0.25"/></pattern>'
        '</defs>',
        f'<rect width="{w}" height="{h}" fill="white"/>',
        f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" '
        f'fill="none" stroke="#000" stroke-width="0.7"/>',
    ]
    for view in sheet.views:
        parts.append(f"<!-- view {escape(view.name)} -->")
        for e in view.entities:
            parts.append(_render_entity(view, e))
        for d in view.dims:
            parts.append(_render_dim(view, d))
        if view.caption:
            parts.append(_text((view.origin[0], view.origin[1]), "", 0.1))
            cap_at = (view.origin[0], view.origin[1] + 6)
            parts.append(_text(cap_at, view.caption, 3.0, "middle"))
    for tb in sheet.tables:
        parts.append(_table(tb))
    if sheet.notes:
        nx, ny = 14, 18
        parts.append(_text((nx, ny), "NOTES:", 2.6))
        for i, note in enumerate(sheet.notes):
            parts.append(_text((nx, ny + 4 + i * 4), f"{i + 1}. {note}", 2.2))
    parts.append(_title_block(drawing, sheet))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def render_drawing_svg(drawing: Drawing, out_dir: str | Path) -> list[Path]:
    """Render every sheet; write the provenance sidecar; return the paths."""
    drawing.validate()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for i, sheet in enumerate(drawing.sheets, start=1):
        p = out / f"{drawing.number}_Sh{i}.svg"
        p.write_text(render_sheet_svg(drawing, sheet), encoding="utf-8")
        written.append(p)
    prov = out / f"{drawing.number}.provenance.json"
    prov.write_text(json.dumps({
        "drawing": drawing.number, "revision": drawing.revision,
        "dimensions": drawing.provenance(),
    }, indent=1), encoding="utf-8")
    written.append(prov)
    return written
