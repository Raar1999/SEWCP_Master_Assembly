"""Drawing data model. Millimetres everywhere; view space is model space
scaled onto the sheet. Y is up in model space; renderers flip as needed.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Literal

__all__ = ["DrawError", "Line", "Circle", "Arc", "Polyline", "Hatch", "Text",
           "Dim", "Table", "View", "Sheet", "Drawing", "SHEET_SIZES"]

SHEET_SIZES = {"A3": (420.0, 297.0), "A2": (594.0, 420.0)}

Layer = Literal["outline", "hidden", "center", "hatch", "phantom"]


class DrawError(Exception):
    """The drawing definition is malformed - refused, not rendered."""


@dataclass(frozen=True)
class Line:
    p1: tuple[float, float]
    p2: tuple[float, float]
    layer: Layer = "outline"


@dataclass(frozen=True)
class Circle:
    center: tuple[float, float]
    diameter: float
    layer: Layer = "outline"


@dataclass(frozen=True)
class Arc:
    center: tuple[float, float]
    radius: float
    start_deg: float
    end_deg: float          # counter-clockwise from start to end
    layer: Layer = "outline"


@dataclass(frozen=True)
class Polyline:
    points: tuple[tuple[float, float], ...]
    closed: bool = False
    layer: Layer = "outline"


@dataclass(frozen=True)
class Hatch:
    """A hatched region - the masking-sheet primitive."""
    points: tuple[tuple[float, float], ...]
    label: str = ""
    style: Literal["lines", "cross"] = "lines"


@dataclass(frozen=True)
class Text:
    at: tuple[float, float]
    text: str
    height: float = 2.5
    anchor: Literal["start", "middle", "end"] = "start"


@dataclass(frozen=True)
class Dim:
    """A dimension with mandatory provenance.

    kind:
      linear    p1..p2 measured, dimension line offset by `offset`
                perpendicular (sign = side); text overridable
      diameter  circle at p1 with value `value`; leader at `angle_deg`
      radius    arc centre p1, value; leader at angle
      angular   vertex p1, from angle a1 to a2 (deg), arc at offset radius
      note      leader note at p1, text only
    """
    kind: Literal["linear", "diameter", "radius", "angular", "note"]
    p1: tuple[float, float]
    source: str
    p2: tuple[float, float] | None = None
    value: float | None = None
    text: str | None = None
    offset: float = 8.0
    angle_deg: float = 30.0
    a1: float | None = None
    a2: float | None = None
    tol: str = ""

    def __post_init__(self) -> None:
        if not self.source or not str(self.source).strip():
            raise DrawError(
                f"dimension {self.kind} at {self.p1} carries no source - "
                "every drawing dimension must trace to a governing "
                "specification, parameter, observation or recorded decision")
        if self.kind == "linear" and self.p2 is None:
            raise DrawError("linear dimension needs p2")
        if self.kind in ("diameter", "radius") and self.value is None:
            raise DrawError(f"{self.kind} dimension needs value")
        if self.kind == "angular" and (self.a1 is None or self.a2 is None):
            raise DrawError("angular dimension needs a1 and a2")
        if self.kind == "note" and not self.text:
            raise DrawError("note dimension needs text")

    def label(self) -> str:
        if self.text:
            return self.text
        if self.kind == "linear":
            assert self.p2 is not None
            d = math.dist(self.p1, self.p2)
            return f"{d:.2f}".rstrip("0").rstrip(".") + (f" {self.tol}" if self.tol else "")
        if self.kind == "diameter":
            return f"⌀{self.value:g}" + (f" {self.tol}" if self.tol else "")
        if self.kind == "radius":
            return f"R{self.value:g}" + (f" {self.tol}" if self.tol else "")
        if self.kind == "angular":
            return f"{abs(self.a2 - self.a1):g}°"
        return self.text or ""


@dataclass(frozen=True)
class Table:
    at: tuple[float, float]           # sheet mm, top-left
    col_widths: tuple[float, ...]
    rows: tuple[tuple[str, ...], ...]
    title: str = ""
    row_height: float = 5.0
    text_height: float = 2.2


@dataclass
class View:
    name: str
    origin: tuple[float, float]       # sheet mm of model (0,0)
    scale: float = 1.0
    caption: str = ""
    entities: list[Any] = field(default_factory=list)
    dims: list[Dim] = field(default_factory=list)

    def add(self, *items: Any) -> "View":
        for it in items:
            (self.dims if isinstance(it, Dim) else self.entities).append(it)
        return self


@dataclass
class Sheet:
    number: str                        # e.g. "SEWCP-200-DRW-001 Sh 1/3"
    title: str
    size: str = "A3"
    views: list[View] = field(default_factory=list)
    tables: list[Table] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    fields: dict[str, str] = field(default_factory=dict)  # title block extras

    @property
    def wh(self) -> tuple[float, float]:
        return SHEET_SIZES[self.size]


@dataclass
class Drawing:
    number: str
    title: str
    revision: str
    sheets: list[Sheet] = field(default_factory=list)
    #: shared title-block fields: material, finish, mass, scale, author role
    fields: dict[str, str] = field(default_factory=dict)

    def provenance(self) -> list[dict[str, str]]:
        rows = []
        for sh in self.sheets:
            for v in sh.views:
                for d in v.dims:
                    rows.append({
                        "sheet": sh.number, "view": v.name,
                        "kind": d.kind, "label": d.label(),
                        "source": d.source,
                    })
        return rows

    def validate(self) -> None:
        if not self.sheets:
            raise DrawError(f"{self.number}: drawing has no sheets")
        for row in self.provenance():
            if not row["source"].strip():
                raise DrawError(f"{self.number}: dimension without source")


def bolt_circle(center: tuple[float, float], bc_diameter: float,
                azimuths_deg: list[float], hole_diameter: float,
                layer: Layer = "outline") -> list[Any]:
    """The recurring pattern of this product family: a construction circle
    and its clocked holes."""
    cx, cy = center
    out: list[Any] = [Circle(center, bc_diameter, layer="center")]
    r = bc_diameter / 2.0
    for az in azimuths_deg:
        a = math.radians(az)
        out.append(Circle((cx + r * math.cos(a), cy + r * math.sin(a)),
                          hole_diameter, layer=layer))
    return out
