"""The drawing layer: provenance discipline and both renderers."""

import json

import pytest

from aief_draw import Circle, Dim, Drawing, DrawError, Line, Sheet, View
from aief_draw.model import bolt_circle
from aief_draw.pdf import render_drawing_pdf
from aief_draw.svg import render_drawing_svg


def _drawing():
    view = View("main", origin=(150, 140), scale=0.5)
    view.add(Circle((0, 0), 100))
    view.add(*bolt_circle((0, 0), 80.0, [0, 90, 180, 270], 6.0))
    view.add(Line((-50, 0), (50, 0), layer="center"))
    view.add(Dim("diameter", (0, 0), value=100.0,
                 source="spec/test T-D01", angle_deg=45))
    view.add(Dim("linear", (-50, -60), p2=(50, -60),
                 source="parameter:test_width"))
    sheet = Sheet("T-DRW-001 Sh 1", "Test part", views=[view],
                  notes=["A note."])
    return Drawing("T-DRW-001", "TEST PART", "A", sheets=[sheet],
                   fields={"material": "6061-T6", "scale": "1:2"})


def test_dimension_without_source_is_refused():
    with pytest.raises(DrawError):
        Dim("diameter", (0, 0), value=10.0, source="  ")


def test_svg_renders_and_emits_provenance(tmp_path):
    written = render_drawing_svg(_drawing(), tmp_path)
    svgs = [p for p in written if p.suffix == ".svg"]
    assert len(svgs) == 1 and svgs[0].stat().st_size > 500
    body = svgs[0].read_text(encoding="utf-8")
    assert "<svg" in body and "T-DRW-001" in body
    prov = json.loads((tmp_path / "T-DRW-001.provenance.json").read_text())
    sources = {r["source"] for r in prov["dimensions"]}
    assert sources == {"spec/test T-D01", "parameter:test_width"}


def test_pdf_renders(tmp_path):
    written = render_drawing_pdf(_drawing(), tmp_path)
    assert written[0].suffix == ".pdf"
    assert written[0].stat().st_size > 1000
    assert written[0].read_bytes()[:5] == b"%PDF-"


def test_drawing_without_sheets_is_refused():
    with pytest.raises(DrawError):
        Drawing("X", "X", "A").validate()
