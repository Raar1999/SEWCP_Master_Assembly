"""The observed model - what Fusion actually built.

This is deliberately a *separate* type from `DesignSolution`. The solution says
what should exist; this says what does. Verification is the comparison of the
two, and it can only be honest if neither can be mistaken for the other.

Absence is represented as absence. A body Fusion did not report is `None`, not
an empty body with zero volume - a zero that stands in for "not measured" turns
a missing feature into a satisfied one on any comparison that uses a tolerance.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterable

from aief_cad import CadError

__all__ = [
    "ObservationError",
    "ObservedParameter",
    "ObservedBody",
    "ObservedSketch",
    "ObservedPlane",
    "ObservedModel",
    "merge_observations",
]


class ObservationError(CadError):
    """An observation payload cannot be read as a model state."""


def _num(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


@dataclass(frozen=True)
class ObservedParameter:
    name: str
    value: float | None
    unit: str | None = None
    expression: str | None = None

    @property
    def is_literal_expression(self) -> bool:
        """True when Fusion holds a bare number where a derivation was asked for."""
        if self.expression is None:
            return False
        try:
            float(self.expression.replace("mm", "").replace("deg", "").strip())
        except (TypeError, ValueError):
            return False
        return True


@dataclass(frozen=True)
class ObservedBody:
    name: str
    volume_mm3: float | None = None
    area_mm2: float | None = None
    mass_kg: float | None = None
    material: str | None = None
    bbox_min: tuple[float, float, float] | None = None
    bbox_max: tuple[float, float, float] | None = None

    def extent(self, axis: int) -> float | None:
        if self.bbox_min is None or self.bbox_max is None:
            return None
        return self.bbox_max[axis] - self.bbox_min[axis]

    @property
    def dx(self) -> float | None:
        return self.extent(0)

    @property
    def dy(self) -> float | None:
        return self.extent(1)

    @property
    def dz(self) -> float | None:
        return self.extent(2)


@dataclass(frozen=True)
class ObservedSketch:
    name: str
    plane: str | None = None
    fully_constrained: bool | None = None
    curves: int | None = None
    profiles: int | None = None
    construction_curves: int | None = None
    #: Per-curve geometry in model-space mm, as the add-in reported it:
    #: {"type": "line", "start": [x,y], "end": [x,y], "construction": bool}
    #: {"type": "arc"|"circle", "center": [x,y], "radius": r, ...}.
    #: Empty when the observing add-in predates curve reporting - verifiers
    #: treat that as *unmeasured*, and a check that needs geometry fails
    #: rather than passes.
    curve_geometry: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class ObservedPlane:
    name: str
    offset_mm: float | None = None
    base: str | None = None


@dataclass(frozen=True)
class ObservedModel:
    """Model state as reported by Fusion."""

    document: dict[str, Any] = field(default_factory=dict)
    component: dict[str, Any] = field(default_factory=dict)
    parameters: tuple[ObservedParameter, ...] = ()
    bodies: tuple[ObservedBody, ...] = ()
    sketches: tuple[ObservedSketch, ...] = ()
    planes: tuple[ObservedPlane, ...] = ()
    features: tuple[dict[str, Any], ...] = ()
    material: dict[str, Any] | None = None
    source_command: str | None = None

    # -- lookup ------------------------------------------------------------

    def parameter(self, name: str) -> ObservedParameter | None:
        for p in self.parameters:
            if p.name == name:
                return p
        return None

    def body(self, name: str | None = None) -> ObservedBody | None:
        if name is None:
            return self.bodies[0] if self.bodies else None
        for b in self.bodies:
            if b.name == name:
                return b
        return None

    def sketch(self, name: str) -> ObservedSketch | None:
        for s in self.sketches:
            if s.name == name:
                return s
        return None

    def plane(self, name: str) -> ObservedPlane | None:
        for p in self.planes:
            if p.name == name:
                return p
        return None

    @property
    def units(self) -> str | None:
        return self.document.get("units")

    @property
    def is_empty(self) -> bool:
        return not (self.parameters or self.bodies or self.sketches or self.planes)

    def as_dict(self) -> dict[str, Any]:
        return {
            "document": self.document,
            "component": self.component,
            "parameters": [
                {"name": p.name, "value": p.value, "unit": p.unit,
                 "expression": p.expression}
                for p in self.parameters
            ],
            "bodies": [
                {"name": b.name, "volume_mm3": b.volume_mm3, "area_mm2": b.area_mm2,
                 "mass_kg": b.mass_kg, "material": b.material,
                 "bbox_min": list(b.bbox_min) if b.bbox_min else None,
                 "bbox_max": list(b.bbox_max) if b.bbox_max else None}
                for b in self.bodies
            ],
            "sketches": [
                {"name": s.name, "plane": s.plane,
                 "fully_constrained": s.fully_constrained, "curves": s.curves,
                 "profiles": s.profiles,
                 "construction_curves": s.construction_curves,
                 "curve_geometry": list(s.curve_geometry)}
                for s in self.sketches
            ],
            "planes": [
                {"name": p.name, "offset_mm": p.offset_mm, "base": p.base}
                for p in self.planes
            ],
            "features": list(self.features),
            "material": self.material,
        }


#: Exactly Fusion's saved-document display decoration - one space, lowercase
#: "v", digits, end of string. Anything looser would rewrite legitimate names
#: ("Bracket V2", "Housing v2.1", "Plate rev3", "Platev2").
_FUSION_VERSION_SUFFIX = re.compile(r"^(?P<name>.+) v\d+$")


def _component_view(raw: Any) -> dict[str, Any]:
    """Component state with `name` carrying the persisted design name.

    Fusion binds the root component name to the document's *display* name,
    which gains a version suffix ("<name> v<N>") on every save; the persisted
    design name never carries it. `component.name` in an acceptance criterion
    means the persisted name - ruled by the owner on ACC-NAME (Option 1,
    2026-08-11), requirement unweakened, verifier untouched.

    Preference order:
      1. `persisted_name` as reported by the add-in from Fusion's data file -
         authoritative, and the only source that can keep a design
         legitimately named like "Bracket v2" intact;
      2. strict normalization of the display name, stripping exactly the
         Fusion suffix pattern - documented fallback for observations made by
         an add-in that predates `persisted_name`;
      3. the display name unchanged.

    `name_source` records which path produced `name`; `display_name` keeps
    the raw display string as evidence. The transform is idempotent, so a
    recorded observation replays to the same model state.
    """
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ObservationError(
            f"observed.component is {type(raw).__name__}, not an object"
        )
    out = dict(raw)
    persisted = out.get("persisted_name")
    if isinstance(persisted, str) and persisted:
        out["display_name"] = out.get("display_name") or out.get("name")
        out["name"] = persisted
        out["name_source"] = "data_file"
        return out
    if out.get("name_source") == "display_normalized":
        return out  # already normalized once; replay must not re-judge it
    name = out.get("name")
    if isinstance(name, str):
        m = _FUSION_VERSION_SUFFIX.match(name)
        if m:
            out["name"] = m.group("name")
            out["display_name"] = name
            out["name_source"] = "display_normalized"
        else:
            out["name_source"] = "display"
    return out


def _xyz(value: Any) -> tuple[float, float, float] | None:
    if not isinstance(value, (list, tuple)) or len(value) != 3:
        return None
    out = [_num(v) for v in value]
    if any(v is None for v in out):
        return None
    return (out[0], out[1], out[2])  # type: ignore[index]


def parse(observed: dict[str, Any], command_id: str | None = None) -> ObservedModel:
    """Read an `observed` payload into a model state."""
    if not isinstance(observed, dict):
        raise ObservationError(
            f"observed payload is {type(observed).__name__}, not an object"
        )

    def rows(key: str) -> list[dict[str, Any]]:
        v = observed.get(key) or []
        if isinstance(v, str) or not isinstance(v, list):
            raise ObservationError(f"observed.{key} is {type(v).__name__}, not a list")
        bad = [e for e in v if not isinstance(e, dict)]
        if bad:
            raise ObservationError(f"observed.{key} holds a non-object entry")
        return v

    return ObservedModel(
        document=observed.get("document") or {},
        component=_component_view(observed.get("component")),
        parameters=tuple(
            ObservedParameter(
                name=r.get("name", ""),
                value=_num(r.get("value")),
                unit=r.get("unit"),
                expression=r.get("expression"),
            )
            for r in rows("parameters")
            if r.get("name")
        ),
        bodies=tuple(
            ObservedBody(
                name=r.get("name", ""),
                volume_mm3=_num(r.get("volume_mm3")),
                area_mm2=_num(r.get("area_mm2")),
                mass_kg=_num(r.get("mass_kg")),
                material=r.get("material"),
                bbox_min=_xyz(r.get("bbox_min")),
                bbox_max=_xyz(r.get("bbox_max")),
            )
            for r in rows("bodies")
        ),
        sketches=tuple(
            ObservedSketch(
                name=r.get("name", ""),
                plane=r.get("plane"),
                fully_constrained=r.get("fully_constrained"),
                curves=r.get("curves"),
                profiles=r.get("profiles"),
                construction_curves=r.get("construction_curves"),
                curve_geometry=tuple(
                    e for e in (r.get("curve_geometry") or [])
                    if isinstance(e, dict)
                ),
            )
            for r in rows("sketches")
        ),
        planes=tuple(
            ObservedPlane(
                name=r.get("name", ""),
                offset_mm=_num(r.get("offset_mm")),
                base=r.get("base"),
            )
            for r in rows("planes")
        ),
        features=tuple(rows("features")),
        material=observed.get("material"),
        source_command=command_id,
    )


def merge_observations(observations: Iterable[Any]) -> ObservedModel:
    """Take the model state from the last observation that carried one.

    Intermediate operations report a partial payload; the terminal `observe`
    reports the whole model. The last complete payload wins, and a run with no
    payload at all yields an empty model - which every verifier fails, rather
    than passing vacuously.
    """
    latest: ObservedModel | None = None
    for obs in observations:
        payload = getattr(obs, "observed", None)
        if not payload:
            continue
        model = parse(payload, getattr(obs, "command_id", None))
        if model.is_empty and latest is not None:
            continue
        latest = model
    return latest or ObservedModel()
