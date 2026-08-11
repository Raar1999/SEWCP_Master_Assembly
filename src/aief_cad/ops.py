"""The CAD operation vocabulary - *how* Fusion will build the solution.

An operation is a bounded, validated, single-purpose instruction. The vocabulary
is deliberately small and geometric; it names no component and encodes no
engineering judgement. Anything an operation cannot express is a gap in this
module, to be closed here, not worked around by widening an argument to carry a
special case.

Every operation is validated **before dispatch**. A malformed operation is
rejected by this layer and never reaches Fusion, and the add-in rejects it a
second time on arrival - the boundary is checked from both sides because only
one of the two is under this repository's control at run time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

from aief_cad import CadError
from aief_cad.digest import canonical_json, digest_of
from aief_cad.solution import DesignSolution, FeatureSpec

__all__ = ["OpError", "Op", "OP_SPECS", "compile_solution", "validate_sequence"]


class OpError(CadError):
    """An operation is unknown, malformed, or carries an unusable argument."""


Validator = Callable[[Any], bool]


def _is_str(v: Any) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _is_num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _is_expr(v: Any) -> bool:
    """A dimension is a parameter name or an expression - never a bare number.

    Hardcoding a literal where the parameter master declares a value is the
    defect `AGT-cad-engineer` lists under forbidden actions, so the vocabulary
    makes it unrepresentable rather than merely discouraged.
    """
    return _is_str(v)


def _is_list_of_dict(v: Any) -> bool:
    return isinstance(v, list) and all(isinstance(e, dict) for e in v)


def _is_point2(v: Any) -> bool:
    return isinstance(v, list) and len(v) == 2 and all(_is_num(e) for e in v)


@dataclass(frozen=True)
class OpSpec:
    """The contract for one operation name."""

    required: dict[str, Validator]
    optional: dict[str, Validator] = field(default_factory=dict)
    #: True when the operation changes model state. Read-only operations are
    #: safe to repeat and are excluded from the no-progress check in `loop`.
    mutating: bool = True
    doc: str = ""


OP_SPECS: dict[str, OpSpec] = {
    "ping": OpSpec(
        required={},
        mutating=False,
        doc="Liveness and version handshake. Executes no model change.",
    ),
    "new_document": OpSpec(
        required={"name": _is_str},
        optional={"units": _is_str},
        doc="Create a design document and set its length units.",
    ),
    "rename_component": OpSpec(
        required={"name": _is_str},
        doc="Rename the root component.",
    ),
    "set_parameters": OpSpec(
        required={"parameters": _is_list_of_dict},
        doc="Create or update user parameters. Expressions, never literals.",
    ),
    "create_sketch": OpSpec(
        required={"name": _is_str, "plane": _is_str},
        doc="Create a named sketch on a base plane or a named construction plane.",
    ),
    "sketch_circle": OpSpec(
        required={"sketch": _is_str, "diameter": _is_expr},
        optional={"center": _is_point2, "construction": lambda v: isinstance(v, bool),
                  "name": _is_str,
                  "center_model": lambda v: isinstance(v, list) and len(v) == 3
                  and all(_is_num(c) for c in v)},
        doc=(
            "Add a centre-diameter circle, dimensioned by expression. "
            "`center_model` positions it by model-space mm coordinates, for "
            "sketches on planes whose axes are not the model's."
        ),
    ),
    "sketch_construction": OpSpec(
        required={"sketch": _is_str},
        optional={"circles": _is_list_of_dict, "rays": _is_list_of_dict},
        doc="Add construction circles and angular rays that locate later features.",
    ),
    "sketch_path": OpSpec(
        required={"sketch": _is_str, "centerline": _is_list_of_dict,
                  "footprint": _is_list_of_dict},
        doc=(
            "Add a routed path: the centreline as fixed construction geometry "
            "and its closed offset outline as fixed profile geometry. "
            "Coordinates are model-space millimetres; every curve is fixed, "
            "which is what constrains a derived chain."
        ),
    ),
    "offset_plane": OpSpec(
        required={"name": _is_str, "base": _is_str, "offset": _is_expr},
        doc="Create a named construction plane offset from a base plane.",
    ),
    "radial_plane": OpSpec(
        required={"name": _is_str, "az_deg": _is_expr},
        optional={"offset": _is_expr},
        doc=(
            "Create a named construction plane whose normal is the radial "
            "direction at the given azimuth about Z, optionally offset from "
            "the origin along that normal. Parametric: an angle plane about "
            "the Z axis, then an offset plane from it."
        ),
    ),
    "sketch_profile": OpSpec(
        required={"sketch": _is_str,
                  "points": lambda v: isinstance(v, list) and len(v) >= 3
                  and all(isinstance(p, list) and len(p) == 3
                          and all(_is_num(c) for c in p) for p in v)},
        doc=(
            "Add a closed, fixed polygon profile from model-space mm points "
            "to a named sketch on any plane. The general 3D counterpart of "
            "sketch_path's XY-parallel chains."
        ),
    ),
    "combine": OpSpec(
        required={"target": _is_str, "tool": _is_str},
        optional={"operation": _is_str},
        doc="Boolean-combine a tool body into a target body (default join).",
    ),
    "extrude": OpSpec(
        required={"sketch": _is_str, "distance": _is_expr},
        optional={"profile": lambda v: _is_num(v) or v in ("all", "smallest", "largest"),
                  "direction": _is_str,
                  "operation": _is_str, "body_name": _is_str},
        doc="Extrude a sketch profile. `operation` is new_body | join | cut.",
    ),
    "assign_material": OpSpec(
        required={"material": _is_str},
        optional={"body": _is_str, "density": _is_num},
        doc=(
            "Assign a physical material, which is what makes a mass check "
            "real. `density` (kg/m^3) lets the bridge create the stated "
            "material when the host library lacks it."
        ),
    ),
    "observe": OpSpec(
        required={},
        optional={"scope": lambda v: isinstance(v, list) and all(_is_str(e) for e in v)},
        mutating=False,
        doc="Return actual model state. Changes nothing. The only input to verification.",
    ),
}

_DIRECTIONS = {"positive", "negative", "symmetric"}
_OPERATIONS = {"new_body", "join", "cut", "intersect"}


@dataclass(frozen=True)
class Op:
    """One requested operation. Carries provenance back to the design solution."""

    op_id: str
    op: str
    args: dict[str, Any] = field(default_factory=dict)
    feature: str | None = None
    satisfies: tuple[str, ...] = ()
    note: str = ""

    @property
    def mutating(self) -> bool:
        return OP_SPECS[self.op].mutating

    def as_dict(self) -> dict[str, Any]:
        return {
            "op_id": self.op_id,
            "op": self.op,
            "args": self.args,
            "feature": self.feature,
            "satisfies": list(self.satisfies),
            "note": self.note,
        }

    def idempotency_key(self) -> str:
        """Identity of the *effect*, not of the request.

        Two dispatches of the same operation with the same arguments against
        the same model are the same effect. The bridge uses this to answer a
        repeat from the recorded observation instead of executing twice, which
        is what makes a resumed run safe.
        """
        return digest_of(canonical_json({"op": self.op, "args": self.args}))

    def validate(self) -> None:
        spec = OP_SPECS.get(self.op)
        if spec is None:
            raise OpError(
                f"{self.op_id}: unknown operation {self.op!r}. Known: "
                f"{', '.join(sorted(OP_SPECS))}"
            )
        if not isinstance(self.args, dict):
            raise OpError(f"{self.op_id}: args is {type(self.args).__name__}, not an object")

        for key, check in spec.required.items():
            if key not in self.args:
                raise OpError(f"{self.op_id} ({self.op}): missing required argument {key!r}")
            if not check(self.args[key]):
                raise OpError(
                    f"{self.op_id} ({self.op}): argument {key!r} has unusable "
                    f"value {self.args[key]!r}"
                )
        for key, value in self.args.items():
            if key in spec.required:
                continue
            if key not in spec.optional:
                raise OpError(
                    f"{self.op_id} ({self.op}): unknown argument {key!r}. An "
                    f"argument this layer does not know is one Fusion will "
                    f"ignore, so it is rejected rather than dropped"
                )
            if not spec.optional[key](value):
                raise OpError(
                    f"{self.op_id} ({self.op}): optional argument {key!r} has "
                    f"unusable value {value!r}"
                )

        if self.op == "extrude":
            d = self.args.get("direction", "positive")
            if d not in _DIRECTIONS:
                raise OpError(f"{self.op_id}: direction {d!r} not in {sorted(_DIRECTIONS)}")
            o = self.args.get("operation", "new_body")
            if o not in _OPERATIONS:
                raise OpError(f"{self.op_id}: operation {o!r} not in {sorted(_OPERATIONS)}")
        if self.op == "set_parameters":
            for n, p in enumerate(self.args["parameters"]):
                for k in ("name", "unit", "expression"):
                    if k not in p or not _is_str(str(p[k])):
                        raise OpError(
                            f"{self.op_id}: parameters[{n}] missing or empty {k!r}"
                        )


def validate_sequence(ops: Iterable[Op]) -> tuple[Op, ...]:
    """Validate every operation and reject duplicate identifiers."""
    seq = tuple(ops)
    seen: set[str] = set()
    for op in seq:
        op.validate()
        if op.op_id in seen:
            raise OpError(f"duplicate op_id {op.op_id!r} in the dispatched sequence")
        seen.add(op.op_id)
    return seq


# --------------------------------------------------------------------------
# Compiler: design solution -> operation sequence
# --------------------------------------------------------------------------

def _op_id(n: int) -> str:
    return f"OP-{n:04d}"


#: Feature kind -> the operations that realise it. A kind absent from this map
#: is a compiler gap and is raised as one; it is never silently skipped, which
#: would produce a model missing a feature the solution required while every
#: operation reported success.
_COMPILERS: dict[str, str] = {
    "document": "new_document",
    "component_name": "rename_component",
    "parameters": "set_parameters",
    "sketch": "create_sketch",
    "sketch_circle": "sketch_circle",
    "construction_sketch": "sketch_construction",
    "sketch_path": "sketch_path",
    "sketch_profile": "sketch_profile",
    "offset_plane": "offset_plane",
    "radial_plane": "radial_plane",
    "extrude": "extrude",
    "combine": "combine",
    "material": "assign_material",
}


def compile_solution(solution: DesignSolution) -> tuple[Op, ...]:
    """Turn *what should be built* into *how Fusion will build it*.

    The sequence always ends with an `observe`, because a run that does not
    observe has produced no evidence and cannot be verified - only claimed.
    """
    ops: list[Op] = []
    n = 0

    for feat in solution.ordered_features():
        kind = feat.kind
        if kind not in _COMPILERS:
            raise OpError(
                f"feature {feat.id}: no compiler for kind {kind!r}. Known kinds: "
                f"{', '.join(sorted(_COMPILERS))}. A solution may not be "
                f"dispatched with a feature no operation realises"
            )
        n += 1
        args = _args_for(kind, feat, solution)
        ops.append(
            Op(
                op_id=_op_id(n),
                op=_COMPILERS[kind],
                args=args,
                feature=feat.id,
                satisfies=feat.satisfies,
                note=feat.rationale,
            )
        )

    n += 1
    ops.append(
        Op(
            op_id=_op_id(n),
            op="observe",
            args={"scope": ["document", "parameters", "bodies", "sketches", "planes",
                            "features", "material"]},
            note="Evidence for independent verification. Reads; changes nothing.",
        )
    )
    return validate_sequence(ops)


def _args_for(kind: str, feat: FeatureSpec, solution: DesignSolution) -> dict[str, Any]:
    """Build the operation arguments for one feature."""
    p = dict(feat.params)

    if kind == "parameters":
        return {
            "parameters": [
                {
                    "name": param.name,
                    "unit": param.unit,
                    "expression": param.expression,
                    "comment": param.comment,
                }
                for param in solution.parameters
            ]
        }
    if kind == "material":
        material = solution.material
        if material is None and "material" not in p:
            raise OpError(
                f"feature {feat.id}: material feature declared but the solution "
                f"carries no material"
            )
        args = {"material": p.get("material", material.name if material else "")}
        if material is not None and material.density:
            args["density"] = float(material.density)
        return args
    if kind == "document":
        return {"name": p["name"], "units": p.get("units", "mm")}
    if kind == "component_name":
        return {"name": p["name"]}
    if kind == "sketch":
        return {"name": p["name"], "plane": p["plane"]}
    if kind == "sketch_circle":
        args: dict[str, Any] = {"sketch": p["sketch"], "diameter": p["diameter"]}
        for k in ("center", "construction", "name", "center_model"):
            if k in p:
                args[k] = p[k]
        return args
    if kind == "construction_sketch":
        args = {"sketch": p["sketch"]}
        for k in ("circles", "rays"):
            if k in p:
                args[k] = p[k]
        return args
    if kind == "sketch_path":
        return {"sketch": p["sketch"], "centerline": p["centerline"],
                "footprint": p["footprint"]}
    if kind == "sketch_profile":
        return {"sketch": p["sketch"], "points": p["points"]}
    if kind == "radial_plane":
        args = {"name": p["name"], "az_deg": p["az_deg"]}
        if "offset" in p:
            args["offset"] = p["offset"]
        return args
    if kind == "combine":
        args = {"target": p["target"], "tool": p["tool"]}
        if "operation" in p:
            args["operation"] = p["operation"]
        return args
    if kind == "offset_plane":
        return {"name": p["name"], "base": p.get("base", "XY"), "offset": p["offset"]}
    if kind == "extrude":
        args = {"sketch": p["sketch"], "distance": p["distance"]}
        for k in ("profile", "direction", "operation", "body_name"):
            if k in p:
                args[k] = p[k]
        return args
    raise OpError(f"feature {feat.id}: unhandled kind {kind!r}")
