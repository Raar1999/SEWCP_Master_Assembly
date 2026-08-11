"""Specialized design agents - the engineering reasoning layer.

Each agent owns a set of requirement kinds and reasons only within them. It
receives the requirement package and returns a `DesignContribution` bounded by
a declared write scope over the solution, so an agent that reaches outside its
domain is rejected by `DesignContribution.validate` rather than merged.

None of these agents certifies CAD. They say what should be built; whether the
built model satisfies the requirement is decided in `verify/`, by code that
never sees a contribution.

`ModelSetupAgent` is deliberately *not* an engineering agent. It transcribes
document identity, the parameter master and the material the package already
carries. It holds no authority and makes no choice; it exists so that the
orchestrator does not have to author solution content itself and thereby
become the engineering authority for every domain.
"""

from __future__ import annotations

from typing import Any, Protocol, Sequence

from aief_cad import CadError
from aief_cad.expr import resolve_all
from aief_cad.requirements import Requirement, RequirementPackage
from aief_cad.routing import KeepOut, RoutingSpec, route_channel
from aief_cad.solution import DesignContribution, FeatureSpec

__all__ = [
    "AgentError",
    "DesignAgent",
    "ModelSetupAgent",
    "MechanicalDesignAgent",
    "ThermalInterfaceAgent",
    "ManufacturingAgent",
    "AGENT_REGISTRY",
    "select_agents",
]


class AgentError(CadError):
    """An agent cannot reason about a requirement it has been given."""


class DesignAgent(Protocol):
    name: str
    domain: str
    owns: tuple[str, ...]

    def contribute(self, package: RequirementPackage) -> DesignContribution:
        ...  # pragma: no cover - protocol


def _param_ref(req: Requirement, key: str, form: dict[str, Any]) -> str:
    """Read a parameter reference out of a requirement's form block.

    A form must name a *parameter*, never carry a number. A literal here would
    reintroduce exactly the hardcoded dimension the parameter master exists to
    prevent, one layer further up where it is harder to see.
    """
    value = form.get(key)
    if not isinstance(value, str) or not value.strip():
        raise AgentError(
            f"{req.id}: form.{key} must name a parameter; got {value!r}. A "
            f"dimension stated here as a number would bypass the parameter "
            f"master, which is where dimensions are governed"
        )
    return value


class ModelSetupAgent:
    """Non-engineering transcription of package-level identity and parameters."""

    name = "model-setup"
    domain = "model"
    owns: tuple[str, ...] = ()

    def contribute(self, package: RequirementPackage) -> DesignContribution:
        doc_name = str(package.scope.get("document_name") or package.component)
        units = str(package.scope.get("units") or "mm")

        features: list[FeatureSpec] = [
            FeatureSpec(
                id="setup.document",
                kind="document",
                params={"name": doc_name, "units": units},
                rationale="Document identity and length unit, from the package scope.",
            ),
            FeatureSpec(
                id="setup.parameters",
                kind="parameters",
                params={},
                depends_on=("setup.document",),
                rationale=(
                    "The parameter master is imported before any geometry, so "
                    "every later dimension is a reference and never a literal."
                ),
            ),
            FeatureSpec(
                id="setup.component",
                kind="component_name",
                params={"name": doc_name},
                depends_on=("setup.parameters",),
                rationale="Root component named for the component identity.",
            ),
        ]
        writes = ["feature:setup.*"]

        if package.material is not None:
            features.append(
                FeatureSpec(
                    id="setup.material",
                    kind="material",
                    params={"material": package.material.name},
                    depends_on=("setup.component",),
                    rationale=(
                        "Physical material assigned so a mass acceptance "
                        "condition measures something real."
                    ),
                )
            )
        return DesignContribution(
            agent=self.name,
            domain=self.domain,
            writes=tuple(writes),
            features=tuple(features),
            notes=(
                "Holds no engineering authority. Every value here is transcribed "
                "from the requirement package.",
            ),
        )


class MechanicalDesignAgent:
    """Owns mechanical geometry, structural form and manufacturable shape."""

    name = "mechanical.design-engineer"
    domain = "mechanical"
    owns = ("geometry", "structural")

    #: Primitive forms this agent can reason about. A form it does not know is
    #: an escalation, never a best guess at what the author meant.
    FORMS = ("disc", "plate", "locating_sketch", "annular_channel",
             "port_stub", "body_combine", "axial_hole_pattern",
             "slot_pattern", "transverse_drill", "profile_cut", "ring_groove",
             "swept_strip")

    def contribute(self, package: RequirementPackage) -> DesignContribution:
        features: list[FeatureSpec] = []
        constraints: list[dict[str, Any]] = []
        prior = "setup.material" if package.material is not None else "setup.component"
        self._package_parameters = package.parameters

        for req in package.requirements:
            if req.kind not in self.owns:
                continue
            form = req.value if isinstance(req.value, dict) else None
            if form is None:
                # A stated requirement with no buildable form is a constraint on
                # the design, recorded so a verifier can see it was not dropped.
                constraints.append(
                    {
                        "id": f"con.{req.id}",
                        "kind": req.kind,
                        "statement": req.statement,
                        "source": req.source,
                        "owner": self.name,
                    }
                )
                continue
            kind = form.get("form")
            if kind not in self.FORMS:
                raise AgentError(
                    f"{req.id}: form {kind!r} is not one this agent reasons "
                    f"about ({', '.join(self.FORMS)}). Adding a form is an "
                    f"engineering extension of this agent, not a widening of an "
                    f"existing one"
                )
            features.extend(self._build(req, form, prior))
            if features:
                prior = features[-1].id

        return DesignContribution(
            agent=self.name,
            domain=self.domain,
            writes=("feature:mech.*", "constraint:con.*"),
            features=tuple(features),
            constraints=tuple(constraints),
            consumed=tuple(
                r.id for r in package.requirements if r.kind in self.owns
            ),
        )

    def _build(
        self, req: Requirement, form: dict[str, Any], prior: str
    ) -> list[FeatureSpec]:
        base = f"mech.{req.id}"
        plane = str(form.get("plane", "XY"))

        if form["form"] == "disc":
            diameter = _param_ref(req, "diameter", form)
            thickness = _param_ref(req, "thickness", form)
            sketch = str(form.get("sketch", f"{base}.profile"))
            return [
                FeatureSpec(
                    id=f"{base}.sketch",
                    kind="sketch",
                    params={"name": sketch, "plane": plane, "fully_constrained": True},
                    satisfies=(req.id,),
                    # `after` is additive: a disc on a derived plane needs
                    # both its build-order anchor and the plane's feature.
                    depends_on=(prior,) + tuple(form.get("after", ())),
                    rationale=f"Profile sketch for {req.id} on {plane}.",
                ),
                FeatureSpec(
                    id=f"{base}.circle",
                    kind="sketch_circle",
                    params={"sketch": sketch, "diameter": diameter,
                            "center": [0.0, 0.0], "fully_constrained": True},
                    satisfies=(req.id,),
                    depends_on=(f"{base}.sketch",),
                    rationale=(
                        f"Outer profile dimensioned by {diameter}; centred on the "
                        f"origin so the part axis is the document axis."
                    ),
                ),
                FeatureSpec(
                    id=f"{base}.extrude",
                    kind="extrude",
                    params={
                        "sketch": sketch,
                        "distance": thickness,
                        "direction": str(form.get("direction", "positive")),
                        "operation": str(form.get("operation", "new_body")),
                        **({"body_name": str(form["body"])} if "body" in form
                           else ({"body_name": f"{base}.body"}
                                 if form.get("operation", "new_body")
                                 == "new_body" else {})),
                    },
                    satisfies=(req.id,),
                    depends_on=(f"{base}.circle",),
                    rationale=(
                        f"Solid of thickness {thickness}. Built from the datum "
                        f"face upward so the primary datum sits at zero."
                        if form.get("operation", "new_body") == "new_body" else
                        f"Removal of thickness {thickness}, as the requirement "
                        f"states."
                    ),
                ),
            ]

        if form["form"] == "annular_channel":
            return self._build_channel(req, form, prior)

        if form["form"] == "port_stub":
            return self._build_port_stub(req, form, prior)

        if form["form"] == "axial_hole_pattern":
            return self._build_axial_holes(req, form, prior)

        if form["form"] == "transverse_drill":
            return self._build_transverse_drills(req, form, prior)

        if form["form"] == "swept_strip":
            return self._build_swept_strip(req, form, prior)

        if form["form"] == "ring_groove":
            base_id = f"mech.{req.id}"
            from aief_cad.expr import evaluate
            env = resolve_all(self._package_parameters)
            mean = float(evaluate(str(_param_ref(req, "mean_diameter", form)), env))
            width = float(evaluate(str(_param_ref(req, "groove_width", form)), env))
            z = float(evaluate(str(form.get("plane_z", "0")), env))
            sketch = str(form["sketch"])

            def circle(d):
                r = d / 2.0
                return [
                    {"type": "arc", "center": [0.0, 0.0], "radius": r,
                     "start": [r, 0.0], "end": [-r, 0.0], "ccw": True},
                    {"type": "arc", "center": [0.0, 0.0], "radius": r,
                     "start": [-r, 0.0], "end": [r, 0.0], "ccw": True},
                ]

            return [
                FeatureSpec(
                    id=f"{base_id}.sketch", kind="sketch",
                    params={"name": sketch, "plane": str(form.get("plane", "XY"))},
                    satisfies=(req.id,),
                    depends_on=(prior,) + tuple(form.get("after", ())),
                ),
                FeatureSpec(
                    id=f"{base_id}.rings", kind="sketch_path",
                    params={"sketch": sketch, "centerline": [],
                            "footprint": circle(mean - width)
                            + circle(mean + width)},
                    satisfies=(req.id,), depends_on=(f"{base_id}.sketch",),
                    rationale=(
                        f"Annular groove walls at O{mean - width:g} and "
                        f"O{mean + width:g} (mean O{mean:g}, width {width:g}); "
                        f"the ring is cut by smallest-area profile selection, "
                        f"leaving the inner sealing land intact."
                    ),
                ),
                FeatureSpec(
                    id=f"{base_id}.cut", kind="extrude",
                    params={"sketch": sketch,
                            "distance": _param_ref(req, "depth", form),
                            "direction": str(form.get("direction", "negative")),
                            "operation": "cut", "profile": "smallest"},
                    satisfies=(req.id,), depends_on=(f"{base_id}.rings",),
                ),
            ]

        if form["form"] == "profile_cut":
            base_id = f"mech.{req.id}"
            from aief_cad.expr import evaluate
            env = resolve_all(self._package_parameters)
            pts = [[round(float(evaluate(str(c), env)), 6) for c in p]
                   for p in form["points"]]
            sketch = str(form["sketch"])
            return [
                FeatureSpec(
                    id=f"{base_id}.sketch", kind="sketch",
                    params={"name": sketch, "plane": str(form["plane"])},
                    satisfies=(req.id,),
                    depends_on=(prior,) + tuple(form.get("after", ())),
                ),
                FeatureSpec(
                    id=f"{base_id}.profile", kind="sketch_profile",
                    params={"sketch": sketch, "points": pts},
                    satisfies=(req.id,), depends_on=(f"{base_id}.sketch",),
                    rationale=form.get("rationale", ""),
                ),
                FeatureSpec(
                    id=f"{base_id}.cut", kind="extrude",
                    params={"sketch": sketch,
                            "distance": _param_ref(req, "depth", form),
                            "direction": str(form.get("direction", "negative")),
                            "operation": str(form.get("operation", "cut")),
                            **({"body_name": str(form["body"])}
                               if "body" in form else {})},
                    satisfies=(req.id,), depends_on=(f"{base_id}.profile",),
                ),
            ]

        if form["form"] == "slot_pattern":
            return self._build_slots(req, form, prior)

        if form["form"] == "body_combine":
            return [
                FeatureSpec(
                    id=f"{base}.combine",
                    kind="combine",
                    params={"target": str(form["target"]),
                            "tool": str(form["tool"]),
                            "operation": str(form.get("operation", "join"))},
                    satisfies=(req.id,),
                    depends_on=tuple(form.get("after", ())) or (prior,),
                    rationale=(
                        f"Boolean {form.get('operation', 'join')} of "
                        f"{form['tool']} into {form['target']}, representing "
                        f"the joined state the requirement describes."
                    ),
                ),
            ]

        if form["form"] == "plate":
            raise AgentError(
                f"{req.id}: form 'plate' is declared in FORMS but has no builder "
                f"yet. Closing it is an extension of this agent"
            )

        # locating_sketch: construction geometry that later features derive from
        sketch = str(form.get("sketch", f"{base}.locating"))
        return [
            FeatureSpec(
                id=f"{base}.sketch",
                kind="sketch",
                params={"name": sketch, "plane": plane, "fully_constrained": True},
                satisfies=(req.id,),
                depends_on=(prior,),
                rationale=f"Locating sketch for {req.id}.",
            ),
            FeatureSpec(
                id=f"{base}.construction",
                kind="construction_sketch",
                params={
                    "sketch": sketch,
                    "circles": list(form.get("circles", [])),
                    "rays": list(form.get("rays", [])),
                    "fully_constrained": True,
                },
                satisfies=(req.id,),
                depends_on=(f"{base}.sketch",),
                rationale=(
                    "Single source of angular and radial location. Later features "
                    "project this sketch rather than re-deriving a bolt circle, so "
                    "one edit propagates instead of drifting."
                ),
            ),
        ]


    def _build_channel(
        self, req: Requirement, form: dict[str, Any], prior: str
    ) -> list[FeatureSpec]:
        """Derive a routed annular channel and emit its features.

        The requirement supplies constraints - envelope and cross-section as
        parameter names, keep-out axes and port azimuths as cited data - and
        the routing derivation runs here, in the engineering reasoning layer.
        The routed geometry is audited by the router itself and verified
        again, independently, against the observed sketch.
        """
        base = f"mech.{req.id}"
        resolved = resolve_all(self._package_parameters)
        def val(key: str) -> float:
            name = _param_ref(req, key, form)
            if name not in resolved:
                raise AgentError(
                    f"{req.id}: form.{key} names parameter {name!r}, which "
                    f"the package does not declare"
                )
            return resolved[name]

        keep_outs = tuple(
            KeepOut(
                id=str(k["id"]),
                r=float(k["r"]),
                az_deg=float(k["az_deg"]),
                wall_clearance=float(k["wall_clearance"]),
            )
            for k in form.get("keep_outs", [])
        )
        if not keep_outs:
            raise AgentError(
                f"{req.id}: annular_channel declares no keep_outs. A channel "
                f"routed with no exclusions is almost certainly a package "
                f"authoring error, and routing one would hide it"
            )
        ports = form.get("ports") or {}
        spec = RoutingSpec(
            envelope_wall_min_r=val("envelope_inner_diameter") / 2.0,
            envelope_wall_max_r=val("envelope_outer_diameter") / 2.0,
            width=val("width"),
            rib=float(form.get("rib", 0.0)),
            min_bend_r=val("min_bend_radius"),
            keep_outs=keep_outs,
            inlet_az_deg=float(ports.get("inlet_az_deg", 0.0)),
            outlet_az_deg=float(ports.get("outlet_az_deg", 0.0)),
            terminal_r=float(ports.get("terminal_r", 0.0)),
        )
        if spec.rib <= 0:
            raise AgentError(f"{req.id}: annular_channel requires a positive rib")
        routed = route_channel(spec)

        sketch = str(form.get("sketch", f"{base}.path"))
        plane = str(form.get("plane", "XY"))
        depth = _param_ref(req, "depth", form)
        return [
            FeatureSpec(
                id=f"{base}.sketch",
                kind="sketch",
                params={"name": sketch, "plane": plane, "fully_constrained": True},
                satisfies=(req.id,),
                depends_on=tuple(form.get("after", ())) or (prior,),
                rationale=f"Channel sketch for {req.id} on {plane}.",
            ),
            FeatureSpec(
                id=f"{base}.path",
                kind="sketch_path",
                params={
                    "sketch": sketch,
                    "centerline": list(routed.centerline),
                    "footprint": list(routed.footprint),
                    "fully_constrained": True,
                    # Constraint data the independent verifier re-checks
                    # against the observed sketch; stated, never re-derived.
                    "keep_outs": [
                        {"id": k.id, "r": k.r, "az_deg": k.az_deg,
                         "wall_clearance": k.wall_clearance}
                        for k in keep_outs
                    ],
                    "envelope_wall_min_r": spec.envelope_wall_min_r,
                    "envelope_wall_max_r": spec.envelope_wall_max_r,
                    "width": spec.width,
                    "min_bend_r": spec.min_bend_r,
                    "pass_radii": list(routed.pass_radii),
                    "length": routed.length,
                },
                satisfies=(req.id,),
                depends_on=(f"{base}.sketch",),
                rationale=(
                    f"Routed serpentine: {len(routed.pass_radii)} passes at "
                    f"{', '.join(f'{r:.2f}' for r in routed.pass_radii)} mm, "
                    f"developed length {routed.length:.0f} mm, audited "
                    f"against every stated keep-out"
                ),
            ),
            FeatureSpec(
                id=f"{base}.cut",
                kind="extrude",
                params={
                    "sketch": sketch,
                    "distance": depth,
                    "direction": str(form.get("direction", "positive")),
                    "operation": "cut",
                },
                satisfies=(req.id,),
                depends_on=(f"{base}.path",),
                rationale=(
                    f"Channel pocket, depth {depth} from the sketch plane."
                ),
            ),
        ]

    def _build_port_stub(
        self, req: Requirement, form: dict[str, Any], prior: str
    ) -> list[FeatureSpec]:
        """Radial port stub: ramped access pocket, coaxial bore, weld-prep
        counterbore - derived from parameters and cited port data.

        Cuts use symmetric extents so the geometry is independent of a
        construction plane's normal orientation, which Fusion does not expose
        offline: a symmetric cut of the full stated distance is the same
        geometry whichever way the plane faces.
        """
        import math as _m

        base = f"mech.{req.id}"
        resolved = resolve_all(self._package_parameters)

        def val(key: str) -> float:
            name = _param_ref(req, key, form)
            if name not in resolved:
                raise AgentError(
                    f"{req.id}: form.{key} names parameter {name!r}, which "
                    f"the package does not declare"
                )
            return resolved[name]

        outer_r = val("outer_diameter") / 2.0
        channel_outer_r = val("channel_envelope_outer_diameter") / 2.0
        width = val("channel_width")
        floor_z = val("pocket_floor_z")
        roof_z = val("pocket_roof_z")
        deep_z = floor_z + val("pocket_depth")
        axis_z = val("bore_axis_z")
        bore_d = val("bore_diameter")
        ramp = float(form.get("ramp_length", 0.0))
        full_len = float(form.get("pocket_full_length", bore_d / 2.0 + 1.0))
        if ramp <= 0:
            raise AgentError(f"{req.id}: port_stub requires a positive ramp_length")
        if not (floor_z <= axis_z - bore_d / 2.0 + 1e-6
                and axis_z + bore_d / 2.0 <= deep_z + 1e-6):
            raise AgentError(
                f"{req.id}: the bore (z {axis_z - bore_d / 2.0:.2f}.."
                f"{axis_z + bore_d / 2.0:.2f}) does not sit inside the pocket "
                f"(z {floor_z:.2f}..{deep_z:.2f}); the stub cannot be coaxial "
                f"with the deepened channel"
            )

        features: list[FeatureSpec] = []
        for port in form.get("ports", []):
            pid = str(port["id"]).upper()
            az = float(port["az_deg"])
            u = (_m.cos(_m.radians(az)), _m.sin(_m.radians(az)))
            pb = f"{base}.{pid}"

            def at(r: float, z: float) -> list[float]:
                return [r * u[0], r * u[1], z]

            r_f = channel_outer_r - full_len
            polygon = [
                at(r_f - ramp, roof_z),
                at(r_f, deep_z),
                at(channel_outer_r, deep_z),
                at(channel_outer_r, floor_z),
                at(r_f - ramp, floor_z),
            ]
            profile_plane = f"PL_STUB_{pid}_PROF"
            tangent_plane = f"PL_STUB_{pid}_OD"
            wedge_sketch = f"{form.get('sketch_prefix', 'S12')}_{pid}_WEDGE"
            cb_sketch = f"{form.get('sketch_prefix', 'S12')}_{pid}_CB"
            bore_sketch = f"{form.get('sketch_prefix', 'S12')}_{pid}_BORE"
            features.extend([
                FeatureSpec(
                    id=f"{pb}.prof_plane", kind="radial_plane",
                    params={"name": profile_plane,
                            "az_deg": f"{az + 90.0} deg"},
                    satisfies=(req.id,), depends_on=(prior,),
                    rationale=f"Axis plane of the {pid} stub at {az} deg.",
                ),
                FeatureSpec(
                    id=f"{pb}.wedge_sketch", kind="sketch",
                    params={"name": wedge_sketch, "plane": profile_plane},
                    satisfies=(req.id,), depends_on=(f"{pb}.prof_plane",),
                    rationale="Pocket section sketch on the stub axis plane.",
                ),
                FeatureSpec(
                    id=f"{pb}.wedge_profile", kind="sketch_profile",
                    params={"sketch": wedge_sketch, "points": polygon,
                            "ramp_length": ramp,
                            "provenance_note": (
                                "pocket deepened for bore coaxiality, ramped "
                                "back over the stated length")},
                    satisfies=(req.id,), depends_on=(f"{pb}.wedge_sketch",),
                    rationale=(
                        f"Ramped pocket section at {az} deg: full depth to "
                        f"z={deep_z:g} over {full_len:g} mm, ramp back to the "
                        f"channel roof over {ramp:g} mm."
                    ),
                ),
                FeatureSpec(
                    id=f"{pb}.wedge_cut", kind="extrude",
                    params={"sketch": wedge_sketch,
                            "distance": _param_ref(req, "channel_width", form),
                            "direction": "symmetric", "operation": "cut"},
                    satisfies=(req.id,), depends_on=(f"{pb}.wedge_profile",),
                    rationale="Pocket cut, one channel width, centred on the axis.",
                ),
                FeatureSpec(
                    id=f"{pb}.od_plane", kind="radial_plane",
                    params={"name": tangent_plane, "az_deg": f"{az} deg",
                            "offset": f"{form['outer_diameter']} / 2"},
                    satisfies=(req.id,), depends_on=(f"{pb}.wedge_cut",),
                    rationale=f"OD-tangent plane at {az} deg for the stub bores.",
                ),
                FeatureSpec(
                    id=f"{pb}.cb_sketch", kind="sketch",
                    params={"name": cb_sketch, "plane": tangent_plane},
                    satisfies=(req.id,), depends_on=(f"{pb}.od_plane",),
                ),
                FeatureSpec(
                    id=f"{pb}.cb_circle", kind="sketch_circle",
                    params={"sketch": cb_sketch,
                            "diameter": _param_ref(req, "counterbore_diameter", form),
                            "center_model": at(outer_r, axis_z)},
                    satisfies=(req.id,), depends_on=(f"{pb}.cb_sketch",),
                    rationale="Weld-prep counterbore on the stub axis.",
                ),
                FeatureSpec(
                    id=f"{pb}.cb_cut", kind="extrude",
                    params={"sketch": cb_sketch,
                            "distance": f"2 * ({form['counterbore_depth']})",
                            "direction": "symmetric", "operation": "cut"},
                    satisfies=(req.id,), depends_on=(f"{pb}.cb_circle",),
                    rationale=(
                        "Counterbore, symmetric twice the depth: the outboard "
                        "half cuts air, so the geometry is orientation-proof."
                    ),
                ),
                FeatureSpec(
                    id=f"{pb}.bore_sketch", kind="sketch",
                    params={"name": bore_sketch, "plane": tangent_plane},
                    satisfies=(req.id,), depends_on=(f"{pb}.cb_cut",),
                ),
                FeatureSpec(
                    id=f"{pb}.bore_circle", kind="sketch_circle",
                    params={"sketch": bore_sketch,
                            "diameter": _param_ref(req, "bore_diameter", form),
                            "center_model": at(outer_r, axis_z)},
                    satisfies=(req.id,), depends_on=(f"{pb}.bore_sketch",),
                    rationale="Stub bore on the axis, from the OD to the pocket.",
                ),
                FeatureSpec(
                    id=f"{pb}.bore_cut", kind="extrude",
                    params={"sketch": bore_sketch,
                            "distance": (
                                f"({form['outer_diameter']}) - "
                                f"({form['channel_envelope_outer_diameter']})"),
                            "direction": "symmetric", "operation": "cut"},
                    satisfies=(req.id,), depends_on=(f"{pb}.bore_circle",),
                    rationale=(
                        "Bore, symmetric across the OD plane: inboard half "
                        "runs exactly to the pocket wall, outboard half air."
                    ),
                ),
            ])
            prior = features[-1].id
        if not features:
            raise AgentError(f"{req.id}: port_stub declares no ports")
        return features

    def _positions(self, req: Requirement, form: dict[str, Any]
                   ) -> list[tuple[float, float]]:
        """Resolve a pattern's hole/slot centres to model XY, mm.

        Accepts a bolt circle with listed azimuth expressions, a bolt circle
        with start/step/count, or explicit (radius, azimuth) points with an
        optional tangential offset - every value an expression over the
        parameter master, so positions stay governed, not restated.
        """
        import math as _m

        from aief_cad.expr import evaluate

        env = resolve_all(self._package_parameters)

        def num(expr: Any) -> float:
            return float(evaluate(str(expr), env))

        out: list[tuple[float, float]] = []
        pos = form.get("positions") or {}
        if "bolt_circle_diameter" in pos:
            r = num(pos["bolt_circle_diameter"]) / 2.0
            if "azimuths" in pos:
                az_list = [num(a) for a in pos["azimuths"]]
            else:
                start = num(pos["azimuth_start"])
                step = num(pos["azimuth_step"])
                az_list = [start + step * i for i in range(int(pos["count"]))]
            for az in az_list:
                out.append((r * _m.cos(_m.radians(az)),
                            r * _m.sin(_m.radians(az))))
        for p in pos.get("points", []):
            r, az = num(p["radius"]), num(p["azimuth"])
            x, y = r * _m.cos(_m.radians(az)), r * _m.sin(_m.radians(az))
            if "tangential_offset" in p:
                t = num(p["tangential_offset"])
                tx, ty = -_m.sin(_m.radians(az)), _m.cos(_m.radians(az))
                x, y = x + t * tx, y + t * ty
            out.append((x, y))
        if not out:
            raise AgentError(f"{req.id}: pattern declares no positions")
        return out

    def _build_axial_holes(
        self, req: Requirement, form: dict[str, Any], prior: str
    ) -> list[FeatureSpec]:
        """Pattern of coaxial round holes cut along Z from a stated plane."""
        base = f"mech.{req.id}"
        from aief_cad.expr import evaluate

        env = resolve_all(self._package_parameters)
        centres = self._positions(req, form)
        sketch = str(form["sketch"])
        plane = str(form.get("plane", "XY"))
        z = float(evaluate(str(form.get("plane_z", "0")), env))
        diameter = _param_ref(req, "diameter", form)
        depth = _param_ref(req, "depth", form)

        features = [
            FeatureSpec(
                id=f"{base}.sketch", kind="sketch",
                params={"name": sketch, "plane": plane},
                satisfies=(req.id,),
                depends_on=tuple(form.get("after", ())) or (prior,),
                rationale=f"Hole pattern sketch for {req.id} on {plane}.",
            )
        ]
        for i, (x, y) in enumerate(centres, start=1):
            features.append(FeatureSpec(
                id=f"{base}.h{i}", kind="sketch_circle",
                params={"sketch": sketch, "diameter": diameter,
                        "center_model": [round(x, 6), round(y, 6), z]},
                satisfies=(req.id,), depends_on=(features[-1].id,),
                rationale=f"Hole {i} of {len(centres)}, centre governed by "
                          f"the pattern's parameters.",
            ))
        features.append(FeatureSpec(
            id=f"{base}.cut", kind="extrude",
            params={"sketch": sketch, "distance": depth,
                    "direction": str(form.get("direction", "positive")),
                    "operation": "cut", "profile": "all"},
            satisfies=(req.id,), depends_on=(features[-1].id,),
            rationale=f"{len(centres)} hole(s) O({diameter}) x {depth}.",
        ))
        return features

    def _build_swept_strip(
        self, req: Requirement, form: dict[str, Any], prior: str
    ) -> list[FeatureSpec]:
        """A formed constant-thickness strip: side profile swept across a width.

        The side path (lines and arcs in the (u, z) plane at a stated azimuth)
        is offset by half the thickness on each side using the routing layer's
        tangent-offset machinery, capped, tessellated to a polygon, and
        extruded symmetrically to the strip width - the general form of bent
        straps, clips and formed brackets.
        """
        import math as _m

        from aief_cad import routing as _rt
        from aief_cad.expr import evaluate

        base = f"mech.{req.id}"
        env = resolve_all(self._package_parameters)

        def num(expr: Any) -> float:
            return float(evaluate(str(expr), env))

        thickness = num(_param_ref(req, "thickness", form))
        az = num(form.get("plane_az_deg", 0.0))
        segs = []
        for s in form["side_path"]:
            if s["type"] == "line":
                segs.append({"type": "line",
                             "start": [num(s["start"][0]), num(s["start"][1])],
                             "end": [num(s["end"][0]), num(s["end"][1])]})
            else:
                segs.append({"type": "arc",
                             "center": [num(s["center"][0]), num(s["center"][1])],
                             "radius": num(s["radius"]),
                             "start": [num(s["start"][0]), num(s["start"][1])],
                             "end": [num(s["end"][0]), num(s["end"][1])],
                             "ccw": bool(s["ccw"])})
        outline = _rt._offset_outline(segs, thickness / 2.0)
        pts_2d = []
        for s in outline:
            pts_2d.extend(_rt._sample_segment(s, step=1.0)[:-1])
        ux, uy = _m.cos(_m.radians(az)), _m.sin(_m.radians(az))
        points = [[round(u * ux, 5), round(u * uy, 5), round(z, 5)]
                  for u, z in pts_2d]
        sketch = str(form["sketch"])
        plane = str(form.get("plane", f"PL_{req.id}"))
        return [
            FeatureSpec(
                id=f"{base}.plane", kind="radial_plane",
                params={"name": plane, "az_deg": f"{az + 90.0} deg"},
                satisfies=(req.id,),
                depends_on=(prior,) + tuple(form.get("after", ())),
                rationale="Side-profile plane containing the strip path.",
            ),
            FeatureSpec(
                id=f"{base}.sketch", kind="sketch",
                params={"name": sketch, "plane": plane},
                satisfies=(req.id,),
                depends_on=(f"{base}.plane",),
            ),
            FeatureSpec(
                id=f"{base}.profile", kind="sketch_profile",
                params={"sketch": sketch, "points": points,
                        "side_path_provenance": form.get("rationale", "")},
                satisfies=(req.id,), depends_on=(f"{base}.sketch",),
                rationale=(
                    f"Strip side profile: {len(segs)} path segment(s) at "
                    f"thickness {thickness:g}, tessellated to "
                    f"{len(points)} points."
                ),
            ),
            FeatureSpec(
                id=f"{base}.extrude", kind="extrude",
                params={"sketch": sketch,
                        "distance": _param_ref(req, "width", form),
                        "direction": "symmetric", "operation": "new_body",
                        "body_name": str(form.get("body", f"{base}.body"))},
                satisfies=(req.id,), depends_on=(f"{base}.profile",),
            ),
        ]

    def _build_transverse_drills(
        self, req: Requirement, form: dict[str, Any], prior: str
    ) -> list[FeatureSpec]:
        """Small horizontal drills on stated axes - vents and cross-drills.

        Each entry states its axis by the normal azimuth of its sketch plane,
        the plane's offset from the origin, the drill centre in model space
        and a symmetric length, all as expressions over the parameter master.
        The symmetric cut makes the result independent of plane orientation.
        """
        import math as _m

        from aief_cad.expr import evaluate

        base = f"mech.{req.id}"
        env = resolve_all(self._package_parameters)

        def num(expr: Any) -> float:
            return float(evaluate(str(expr), env))

        features: list[FeatureSpec] = []
        for entry in form.get("drills", []):
            did = str(entry["id"]).upper()
            az = num(entry["plane_az_deg"])
            offset = num(entry["plane_offset"])
            cx, cy, cz = (num(v) for v in entry["center"])
            plane = f"PL_{did}"
            sketch = f"{form.get('sketch_prefix', 'SV')}_{did}"
            pb = f"{base}.{did}"
            depends = (features[-1].id,) if features else (
                tuple(form.get("after", ())) or (prior,))
            features.extend([
                FeatureSpec(
                    id=f"{pb}.plane", kind="radial_plane",
                    params={"name": plane, "az_deg": f"{az} deg",
                            **({"offset": str(entry["plane_offset"])}
                               if abs(offset) > 1e-9 else {})},
                    satisfies=(req.id,), depends_on=depends,
                    rationale=entry.get("rationale", f"Axis plane for {did}."),
                ),
                FeatureSpec(
                    id=f"{pb}.sketch", kind="sketch",
                    params={"name": sketch, "plane": plane},
                    satisfies=(req.id,), depends_on=(f"{pb}.plane",),
                ),
                FeatureSpec(
                    id=f"{pb}.circle", kind="sketch_circle",
                    params={"sketch": sketch,
                            "diameter": _param_ref(req, "diameter", form),
                            "center_model": [round(cx, 6), round(cy, 6),
                                             round(cz, 6)]},
                    satisfies=(req.id,), depends_on=(f"{pb}.sketch",),
                ),
                FeatureSpec(
                    id=f"{pb}.cut", kind="extrude",
                    params={"sketch": sketch,
                            "distance": str(entry["length"]),
                            "direction": "symmetric", "operation": "cut"},
                    satisfies=(req.id,), depends_on=(f"{pb}.circle",),
                    rationale=entry.get("rationale", ""),
                ),
            ])
        if not features:
            raise AgentError(f"{req.id}: transverse_drill declares no drills")
        return features

    def _build_slots(
        self, req: Requirement, form: dict[str, Any], prior: str
    ) -> list[FeatureSpec]:
        """Pattern of radially-oriented obround slots cut along Z."""
        import math as _m

        from aief_cad.expr import evaluate

        base = f"mech.{req.id}"
        env = resolve_all(self._package_parameters)

        def num(expr: Any) -> float:
            return float(evaluate(str(expr), env))

        centres = self._positions(req, form)
        width = num(_param_ref(req, "width", form))
        length = num(_param_ref(req, "length", form))
        if length <= width:
            raise AgentError(f"{req.id}: slot length must exceed its width")
        half_w = width / 2.0
        half_span = (length - width) / 2.0
        sketch = str(form["sketch"])
        depth = _param_ref(req, "depth", form)

        outlines: list[dict[str, Any]] = []
        for x, y in centres:
            az = _m.atan2(y, x)
            u = (_m.cos(az), _m.sin(az))       # radial - the slot's long axis
            v = (-_m.sin(az), _m.cos(az))      # tangential
            c1 = (x - u[0] * half_span, y - u[1] * half_span)
            c2 = (x + u[0] * half_span, y + u[1] * half_span)

            def pt(c, s_v):
                return [round(c[0] + s_v * v[0] * half_w, 6),
                        round(c[1] + s_v * v[1] * half_w, 6)]

            outlines.extend([
                {"type": "line", "start": pt(c1, 1), "end": pt(c2, 1)},
                {"type": "arc", "center": [round(c2[0], 6), round(c2[1], 6)],
                 "radius": half_w, "start": pt(c2, 1), "end": pt(c2, -1),
                 "ccw": False},
                {"type": "line", "start": pt(c2, -1), "end": pt(c1, -1)},
                {"type": "arc", "center": [round(c1[0], 6), round(c1[1], 6)],
                 "radius": half_w, "start": pt(c1, -1), "end": pt(c1, 1),
                 "ccw": False},
            ])
        return [
            FeatureSpec(
                id=f"{base}.sketch", kind="sketch",
                params={"name": sketch, "plane": str(form.get("plane", "XY"))},
                satisfies=(req.id,),
                depends_on=tuple(form.get("after", ())) or (prior,),
                rationale=f"Slot pattern sketch for {req.id}.",
            ),
            FeatureSpec(
                id=f"{base}.outlines", kind="sketch_path",
                params={"sketch": sketch, "centerline": [],
                        "footprint": outlines},
                satisfies=(req.id,), depends_on=(f"{base}.sketch",),
                rationale=(
                    f"{len(centres)} radially-oriented obround(s) "
                    f"{length:g} x {width:g}, ends fully rounded."
                ),
            ),
            FeatureSpec(
                id=f"{base}.cut", kind="extrude",
                params={"sketch": sketch, "distance": depth,
                        "direction": str(form.get("direction", "positive")),
                        "operation": "cut", "profile": "all"},
                satisfies=(req.id,), depends_on=(f"{base}.outlines",),
                rationale=f"Slot cut, depth {depth}.",
            ),
        ]

    #: Set per contribute() call so _build_channel can resolve parameter
    #: values without threading the package through every _build signature.
    _package_parameters: tuple = ()


class ThermalInterfaceAgent:
    """Owns thermal requirements, cooling interfaces and mating datums."""

    name = "mechanical.simulation-engineer"
    domain = "thermal-interface"
    owns = ("thermal", "interface")

    def contribute(self, package: RequirementPackage) -> DesignContribution:
        features: list[FeatureSpec] = []
        constraints: list[dict[str, Any]] = []

        for req in package.requirements:
            if req.kind not in self.owns:
                continue
            form = req.value if isinstance(req.value, dict) else None
            if form is not None and form.get("form") == "datum_plane":
                offset = _param_ref(req, "offset", form)
                name = str(form.get("name", f"PL_{req.id}"))
                features.append(
                    FeatureSpec(
                        id=f"thermal.{req.id}.plane",
                        kind="offset_plane",
                        params={
                            "name": name,
                            "base": str(form.get("base", "XY")),
                            "offset": offset,
                            "interface": form.get("interface"),
                        },
                        satisfies=(req.id,),
                        depends_on=tuple(form.get("after", ())),
                        rationale=(
                            f"Mating datum for {form.get('interface') or req.id}, "
                            f"located by {offset} so the interface height moves "
                            f"with the parameter rather than being re-typed."
                        ),
                    )
                )
                continue
            constraints.append(
                {
                    "id": f"con.{req.id}",
                    "kind": req.kind,
                    "statement": req.statement,
                    "source": req.source,
                    "owner": self.name,
                    "envelope": (form or {}).get("envelope"),
                    "keep_out": (form or {}).get("keep_out"),
                }
            )

        return DesignContribution(
            agent=self.name,
            domain=self.domain,
            writes=("feature:thermal.*", "constraint:con.*"),
            features=tuple(features),
            constraints=tuple(constraints),
            consumed=tuple(r.id for r in package.requirements if r.kind in self.owns),
        )


class ManufacturingAgent:
    """Owns producibility. Produces constraints and ordering, never geometry.

    This separation is not stylistic. A DFM agent that emits geometry is making
    the mechanical agent's decision, and the conflict detector would then have
    two agents legitimately claiming the same feature key.
    """

    name = "mechanical.manufacturing-engineer"
    domain = "manufacturing"
    owns = ("manufacturing", "material")

    def contribute(self, package: RequirementPackage) -> DesignContribution:
        constraints: list[dict[str, Any]] = []
        for req in package.requirements:
            if req.kind not in self.owns:
                continue
            constraints.append(
                {
                    "id": f"con.{req.id}",
                    "kind": "manufacturing",
                    "statement": req.statement,
                    "source": req.source,
                    "owner": self.name,
                }
            )
        for mc in package.manufacturing:
            constraints.append(
                {
                    "id": f"con.{mc.id}",
                    "kind": "manufacturing",
                    "statement": mc.statement,
                    "source": mc.source,
                    "process": mc.process,
                    "owner": self.name,
                }
            )
        notes = (
            "Feature order is a manufacturing fact: it is carried on "
            "FeatureSpec.depends_on and enforced by DesignSolution.ordered_features.",
        )
        return DesignContribution(
            agent=self.name,
            domain=self.domain,
            writes=("constraint:con.*",),
            constraints=tuple(constraints),
            notes=notes,
            consumed=tuple(mc.id for mc in package.manufacturing),
        )


#: Requirement kind -> the agent that owns it. Domain determination is a lookup
#: in this table against the kinds a package actually states, which is why no
#: component name appears anywhere in the routing path.
AGENT_REGISTRY: dict[str, type] = {
    "geometry": MechanicalDesignAgent,
    "structural": MechanicalDesignAgent,
    "thermal": ThermalInterfaceAgent,
    "interface": ThermalInterfaceAgent,
    "manufacturing": ManufacturingAgent,
    "material": ManufacturingAgent,
}


def select_agents(package: RequirementPackage) -> tuple[Any, ...]:
    """Choose the agents this package needs, from the kinds it declares."""
    chosen: list[Any] = [ModelSetupAgent()]
    seen: set[type] = set()
    for kind in package.domains():
        cls = AGENT_REGISTRY.get(kind)
        if cls is None or cls in seen:
            continue
        seen.add(cls)
        chosen.append(cls())
    return tuple(chosen)


def unroutable_kinds(package: RequirementPackage) -> tuple[str, ...]:
    """Kinds the package states that no registered agent owns.

    Reported by the orchestrator rather than ignored: a requirement nobody owns
    is a requirement nobody is reasoning about.
    """
    return tuple(
        sorted({r.kind for r in package.requirements if r.kind not in AGENT_REGISTRY})
    )
