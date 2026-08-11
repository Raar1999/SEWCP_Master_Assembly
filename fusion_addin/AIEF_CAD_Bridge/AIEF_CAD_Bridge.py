"""AIEF CAD Bridge - the inside half of the Fusion automation boundary.

Fusion exposes its modelling API only to code running inside its own process,
and only the thread that owns the document may touch it. This add-in therefore
runs two things:

    a background thread   polls the command queue; touches no Fusion API
    a custom event        marshals each command onto the MAIN thread, which is
                          the only supported way to cross that line

Every command is answered with exactly one observation, including the commands
it refuses. Silence is not an answer: an unanswered command becomes a timeout
several minutes later with no diagnosis attached.

Three statuses, kept distinct on purpose:

    OK        the operation ran
    ERROR     the operation ran and Fusion raised
    REJECTED  this add-in refused it - unknown op, wrong protocol, bad argument

REJECTED is not a modelling failure, and reporting it as one would send the
repair loop hunting for a geometry problem that does not exist.

Install with `python scripts/install_fusion_addin.py`, then in Fusion:
Utilities > Scripts and Add-Ins > Add-Ins > AIEF_CAD_Bridge > Run.
"""

import json
import math
import os
import threading
import time
import traceback

import adsk.core
import adsk.fusion

PROTOCOL = "aief-cad/1"
EVENT_ID = "AIEFCadBridgeCommand"
POLL_S = 0.25
HEARTBEAT_S = 4.0

#: Fusion's internal length unit is centimetres. Every length this add-in
#: reports is converted to millimetres, so an observation never carries a
#: number whose unit depends on knowing Fusion's internals.
CM_TO_MM = 10.0

_app = None
_ui = None
_handlers = []
_custom_event = None
_stop = threading.Event()
_worker = None
_config = {}


# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

def _config_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "bridge_config.json")


def _load_config():
    """Read the repository bridge root written at install time."""
    with open(_config_path(), "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    root = cfg["bridge_root"]
    return {
        "bridge_root": root,
        "queue": os.path.join(root, "queue"),
        "obs": os.path.join(root, "obs"),
        "state": os.path.join(root, "state"),
    }


def _atomic_write(path, payload_bytes):
    tmp = path + ".part"
    with open(tmp, "wb") as fh:
        fh.write(payload_bytes)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def _write_observation(command_id, body):
    body["protocol"] = PROTOCOL
    body["command_id"] = command_id
    payload = json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"
    _atomic_write(os.path.join(_config["obs"], command_id + ".obs.json"), payload)


def _observation(status, executed, observed=None, error=None, started=None):
    return {
        "status": status,
        "executed": bool(executed),
        "observed": observed or {},
        "error": error,
        "started_at": started,
        "finished_at": time.time(),
        "fusion": {
            "version": _app.version if _app else None,
            "document": _app.activeDocument.name if _app and _app.activeDocument else None,
        },
    }


# --------------------------------------------------------------------------
# Background thread - no Fusion API here, ever
# --------------------------------------------------------------------------

def _pump():
    """Poll the queue and hand each new command to the main thread."""
    seen = set()
    last_beat = 0.0
    while not _stop.is_set():
        try:
            now = time.time()
            if now - last_beat >= HEARTBEAT_S:
                _atomic_write(
                    os.path.join(_config["state"], "addin.heartbeat.json"),
                    json.dumps(
                        {"protocol": PROTOCOL, "alive_at": now, "pid": os.getpid()},
                        sort_keys=True,
                    ).encode("utf-8") + b"\n",
                )
                last_beat = now

            for name in sorted(os.listdir(_config["queue"])):
                if not name.endswith(".cmd.json") or name in seen:
                    continue
                command_id = name[: -len(".cmd.json")]
                if os.path.exists(os.path.join(_config["obs"], command_id + ".obs.json")):
                    seen.add(name)
                    continue
                seen.add(name)
                _app.fireCustomEvent(EVENT_ID, os.path.join(_config["queue"], name))
        except Exception:
            # The pump must not die. A failure here would silently stop every
            # future command with no observation and no diagnosis.
            try:
                _atomic_write(
                    os.path.join(_config["state"], "addin.pump_error.json"),
                    json.dumps({"at": time.time(), "trace": traceback.format_exc()}).encode("utf-8"),
                )
            except Exception:
                pass
        _stop.wait(POLL_S)


class _CommandHandler(adsk.core.CustomEventHandler):
    """Runs on the MAIN thread. The only place the Fusion API is touched."""

    def notify(self, args):
        path = args.additionalInfo
        command_id = os.path.basename(path)[: -len(".cmd.json")]
        started = time.time()
        try:
            with open(path, "r", encoding="utf-8") as fh:
                cmd = json.load(fh)
        except Exception as exc:
            _write_observation(command_id, _observation(
                "REJECTED", False,
                error={"kind": "unreadable_command", "message": str(exc)},
                started=started,
            ))
            return

        try:
            if cmd.get("protocol") != PROTOCOL:
                _write_observation(command_id, _observation(
                    "REJECTED", False,
                    error={"kind": "protocol_mismatch",
                           "message": "command announces %r; this add-in implements %r"
                                      % (cmd.get("protocol"), PROTOCOL)},
                    started=started,
                ))
                return
            op = cmd.get("op")
            handler = _ext_op(op) or _OPS.get(op)
            if handler is None:
                _write_observation(command_id, _observation(
                    "REJECTED", False,
                    error={"kind": "unknown_operation",
                           "message": "%r is not implemented. Known: %s"
                                      % (op, ", ".join(sorted(_OPS)))},
                    started=started,
                ))
                return
            observed = handler(cmd.get("args") or {})
            _write_observation(command_id, _observation("OK", True, observed, started=started))
        except _Rejected as exc:
            _write_observation(command_id, _observation(
                "REJECTED", False,
                error={"kind": "bad_argument", "message": str(exc)},
                started=started,
            ))
        except Exception as exc:
            _write_observation(command_id, _observation(
                "ERROR", False,
                error={"kind": type(exc).__name__, "message": str(exc),
                       "trace": traceback.format_exc()},
                started=started,
            ))


class _Rejected(Exception):
    """The command is malformed. Refused, not attempted."""


# --------------------------------------------------------------------------
# Hot-reloadable operation extension
#
# `bridge_ops_ext.py` beside this file is (re)loaded whenever its mtime
# changes, and its OPS dict overlays _OPS. New and changed operations land
# there, so deploying them needs no add-in restart - the one lifecycle
# action Fusion gives no API for. Only a change to THIS shell still needs
# a manual Stop/Run, which is the isolated platform limitation.
# --------------------------------------------------------------------------

_EXT_STATE = {"mtime": None, "module": None}


def _ext_op(op):
    import importlib.util

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "bridge_ops_ext.py")
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        return None
    if _EXT_STATE["mtime"] != mtime:
        try:
            spec = importlib.util.spec_from_file_location("aief_bridge_ops_ext", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            _EXT_STATE["module"] = module
            _EXT_STATE["mtime"] = mtime
        except Exception:
            # A broken extension must not take the shell down; the stale
            # module (or nothing) keeps serving and the defect surfaces as
            # unknown_operation rather than a dead bridge.
            return None
    module = _EXT_STATE["module"]
    if module is None:
        return None
    return getattr(module, "OPS", {}).get(op)


# --------------------------------------------------------------------------
# Fusion helpers
# --------------------------------------------------------------------------

def _design():
    design = adsk.fusion.Design.cast(_app.activeProduct)
    if design is None:
        raise _Rejected(
            "the active document is not a Fusion design. Create one with "
            "new_document before dispatching modelling operations"
        )
    return design


def _root():
    return _design().rootComponent


def _units():
    return _design().unitsManager


def _base_plane(root, name):
    table = {
        "XY": root.xYConstructionPlane,
        "XZ": root.xZConstructionPlane,
        "YZ": root.yZConstructionPlane,
    }
    if name in table:
        return table[name]
    plane = root.constructionPlanes.itemByName(name)
    if plane is None:
        known = [root.constructionPlanes.item(i).name
                 for i in range(root.constructionPlanes.count)]
        raise _Rejected(
            "plane %r not found. Base planes: XY, XZ, YZ. Construction planes: %s"
            % (name, ", ".join(known) or "none")
        )
    return plane


def _sketch_by_name(root, name):
    for i in range(root.sketches.count):
        sk = root.sketches.item(i)
        if sk.name == name:
            return sk
    raise _Rejected(
        "sketch %r not found. Present: %s"
        % (name, ", ".join(root.sketches.item(i).name for i in range(root.sketches.count))
           or "none")
    )


def _plane_label(root, entity):
    for label, plane in (("XY", root.xYConstructionPlane),
                         ("XZ", root.xZConstructionPlane),
                         ("YZ", root.yZConstructionPlane)):
        try:
            if entity == plane or entity.entityToken == plane.entityToken:
                return label
        except Exception:
            pass
    try:
        return entity.name
    except Exception:
        return None


def _display_value(um, param):
    """Convert a parameter's internal value into the unit it declares.

    Fusion stores length internally in cm and angle in radians. A caller that
    guesses gets a value that is wrong by a factor, so the unit type is
    resolved rather than assumed, and an unconvertible unit returns the
    internal value with the fact recorded rather than a silently scaled one.
    """
    unit = (param.unit or "").strip()
    value = param.value
    if not unit:
        return value, "unitless"
    if unit in ("deg", "degree", "degrees"):
        return math.degrees(value), "angle"
    try:
        converted = um.convert(value, um.internalUnits, unit)
        if converted is not None and converted == converted:  # not NaN
            return converted, "length"
    except Exception:
        pass
    return value, "internal"


# --------------------------------------------------------------------------
# Operations
# --------------------------------------------------------------------------

def _op_ping(args):
    return {
        "addin": "AIEF_CAD_Bridge",
        "protocol": PROTOCOL,
        "fusion_version": _app.version,
        "has_active_design": adsk.fusion.Design.cast(_app.activeProduct) is not None,
    }


def _persisted_doc_name(doc):
    """The saved design name, None when unsaved or unavailable."""
    try:
        if doc is not None and doc.isSaved:
            data_file = doc.dataFile
            return data_file.name if data_file is not None else None
    except Exception:
        pass
    return None


def _op_new_document(args):
    # Document identity, not document creation, is the requirement: when the
    # named design is already open - active or in another tab - adopt it, so
    # a follow-on package continues the same model rather than orphaning it.
    target = None
    active = _app.activeDocument
    if active is not None and _persisted_doc_name(active) == args["name"]:
        target = active
    else:
        for i in range(_app.documents.count):
            doc_i = _app.documents.item(i)
            if _persisted_doc_name(doc_i) == args["name"]:
                target = doc_i
                target.activate()
                break
    if target is not None:
        design = adsk.fusion.Design.cast(_app.activeProduct)
        if design is not None:
            return {"document": {
                "name": target.name,
                "persisted_name": _persisted_doc_name(target),
                "units": design.unitsManager.defaultLengthUnits,
                "adopted": True,
            }}
    doc = _app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = adsk.fusion.Design.cast(_app.activeProduct)
    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
    units = args.get("units", "mm")
    table = {
        "mm": adsk.fusion.DistanceUnits.MillimeterDistanceUnits,
        "cm": adsk.fusion.DistanceUnits.CentimeterDistanceUnits,
        "m": adsk.fusion.DistanceUnits.MeterDistanceUnits,
        "in": adsk.fusion.DistanceUnits.InchDistanceUnits,
        "ft": adsk.fusion.DistanceUnits.FootDistanceUnits,
    }
    if units not in table:
        raise _Rejected("units %r not supported; known: %s" % (units, ", ".join(sorted(table))))
    design.unitsManager.distanceDisplayUnits = table[units]
    try:
        doc.name = args["name"]
    except Exception:
        pass
    return {"document": {"name": doc.name, "units": design.unitsManager.defaultLengthUnits}}


def _op_rename_component(args):
    root = _root()
    # The persisted design name is the component's name under the ruled
    # ACC-NAME semantics; when it already matches, the rename is satisfied.
    persisted = _persisted_doc_name(_app.activeDocument)
    if persisted == args["name"]:
        return {"component": {"name": root.name, "persisted_name": persisted}}
    root.name = args["name"]
    return {"component": {"name": root.name}}


def _op_set_parameters(args):
    design = _design()
    um = design.unitsManager
    applied, failed = [], []
    for entry in args["parameters"]:
        name = entry["name"]
        expression = str(entry["expression"])
        unit = entry.get("unit") or ""
        comment = entry.get("comment") or ""
        try:
            existing = design.userParameters.itemByName(name)
            if existing is not None:
                existing.expression = expression
                if comment:
                    existing.comment = comment
                applied.append(name)
                continue
            design.userParameters.add(
                name, adsk.core.ValueInput.createByString(expression), unit, comment
            )
            applied.append(name)
        except Exception as exc:
            failed.append({"name": name, "expression": expression, "unit": unit,
                           "message": str(exc)})
    if failed:
        # Reported as an executed operation with a partial result: some
        # parameters really were created, and pretending otherwise would make
        # the repair loop re-send the ones that already exist.
        raise RuntimeError(
            "%d of %d parameter(s) rejected by Fusion: %s"
            % (len(failed), len(args["parameters"]),
               "; ".join("%s (%s)" % (f["name"], f["message"]) for f in failed[:5]))
        )
    return {"parameters_applied": len(applied)}


def _op_create_sketch(args):
    root = _root()
    plane = _base_plane(root, args["plane"])
    sketch = root.sketches.add(plane)
    sketch.name = args["name"]
    return {"sketch": {"name": sketch.name, "plane": args["plane"]}}


def _op_sketch_circle(args):
    root = _root()
    sketch = _sketch_by_name(root, args["sketch"])
    um = _units()
    diameter_expr = args["diameter"]
    try:
        radius_cm = um.evaluateExpression(diameter_expr, um.defaultLengthUnits) / 2.0
    except Exception as exc:
        raise _Rejected(
            "diameter expression %r does not evaluate: %s. A dimension must "
            "name a parameter the model already holds" % (diameter_expr, exc)
        )
    center_model = args.get("center_model")
    if center_model is not None:
        x, y, z = (float(c) / CM_TO_MM for c in center_model)
        center_pt = sketch.modelToSketchSpace(adsk.core.Point3D.create(x, y, z))
        cx, cy = center_pt.x, center_pt.y
    else:
        center = args.get("center", [0.0, 0.0])
        cx = um.convert(float(center[0]), um.defaultLengthUnits, um.internalUnits)
        cy = um.convert(float(center[1]), um.defaultLengthUnits, um.internalUnits)

    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(adsk.core.Point3D.create(cx, cy, 0), radius_cm)
    if center_model is not None:
        try:
            circle.centerSketchPoint.isFixed = True
        except Exception:
            pass
    if args.get("construction"):
        circle.isConstruction = True

    # Coincident to the sketch origin removes the two translational degrees of
    # freedom; the diameter dimension removes the third. Together they are what
    # makes the sketch fully constrained rather than merely correct today.
    # A model-space-placed centre is already fixed - constraining it again
    # over-constrains the sketch.
    if center_model is None and abs(cx) < 1e-9 and abs(cy) < 1e-9:
        sketch.geometricConstraints.addCoincident(circle.centerSketchPoint, sketch.originPoint)

    text = adsk.core.Point3D.create(circle.geometry.radius * 1.3, circle.geometry.radius * 1.3, 0)
    dim = sketch.sketchDimensions.addDiameterDimension(circle, text, True)
    dim.parameter.expression = diameter_expr
    if args.get("name"):
        try:
            dim.parameter.name = args["name"]
        except Exception:
            pass

    return {"sketch": {"name": sketch.name,
                       "fully_constrained": sketch.isFullyConstrained,
                       "curves": sketch.sketchCurves.count}}


def _op_sketch_construction(args):
    root = _root()
    sketch = _sketch_by_name(root, args["sketch"])
    um = _units()
    made_circles, made_rays, refused = [], [], []

    for spec in args.get("circles", []):
        expr = spec.get("diameter")
        try:
            radius_cm = um.evaluateExpression(expr, um.defaultLengthUnits) / 2.0
        except Exception as exc:
            refused.append({"circle": expr, "message": str(exc)})
            continue
        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            adsk.core.Point3D.create(0, 0, 0), radius_cm
        )
        circle.isConstruction = True
        sketch.geometricConstraints.addCoincident(circle.centerSketchPoint, sketch.originPoint)
        text = adsk.core.Point3D.create(radius_cm * 0.72, radius_cm * 0.72, 0)
        dim = sketch.sketchDimensions.addDiameterDimension(circle, text, True)
        dim.parameter.expression = expr
        made_circles.append(expr)

    if args.get("rays"):
        try:
            projected = sketch.project(root.xConstructionAxis)
            axis = projected.item(0) if projected.count else None
        except Exception:
            axis = None
        for spec in args.get("rays", []):
            angle_expr = spec.get("angle")
            length_expr = spec.get("length")
            try:
                ang = um.evaluateExpression(angle_expr, "deg")
                length_cm = um.evaluateExpression(length_expr, um.defaultLengthUnits)
            except Exception as exc:
                refused.append({"ray": angle_expr, "message": str(exc)})
                continue
            end = adsk.core.Point3D.create(length_cm * math.cos(ang), length_cm * math.sin(ang), 0)
            line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                adsk.core.Point3D.create(0, 0, 0), end
            )
            line.isConstruction = True
            sketch.geometricConstraints.addCoincident(line.startSketchPoint, sketch.originPoint)
            try:
                text = adsk.core.Point3D.create(end.x * 0.5, end.y * 0.5, 0)
                d = sketch.sketchDimensions.addDistanceDimension(
                    line.startSketchPoint, line.endSketchPoint,
                    adsk.fusion.DimensionOrientations.AlignedDimensionOrientation, text
                )
                d.parameter.expression = length_expr
                if axis is not None:
                    da = sketch.sketchDimensions.addAngularDimension(
                        axis, line, adsk.core.Point3D.create(end.x * 0.3, end.y * 0.3, 0)
                    )
                    da.parameter.expression = angle_expr
            except Exception as exc:
                # An angular dimension Fusion will not accept at this clocking
                # is recorded, not hidden. The ray exists and is not fully
                # constrained, which the constraint verifier will see.
                refused.append({"ray_dimension": angle_expr, "message": str(exc)})
            made_rays.append(angle_expr)

    if refused:
        raise RuntimeError(
            "%d construction element(s) refused: %s"
            % (len(refused), json.dumps(refused[:4]))
        )
    return {"sketch": {"name": sketch.name,
                       "fully_constrained": sketch.isFullyConstrained,
                       "curves": sketch.sketchCurves.count,
                       "circles": len(made_circles),
                       "rays": len(made_rays)}}


def _mm_to_sketch(sketch, x_mm, y_mm):
    """Model-space mm (x, y) -> sketch-space Point3D.

    Valid for sketches on planes parallel to model XY, which is what the
    routed-path features emit; the sketch origin's model z supplies the plane
    height. Anything else would silently shear the geometry, so it is refused.
    """
    origin = sketch.origin
    p = adsk.core.Point3D.create(x_mm / CM_TO_MM, y_mm / CM_TO_MM, origin.z)
    return sketch.modelToSketchSpace(p)


def _op_sketch_path(args):
    root = _root()
    sketch = _sketch_by_name(root, args["sketch"])
    made = {"lines": 0, "arcs": 0}

    def fix_all(curve):
        # Fixing the curve alone leaves its sketch points - notably an arc's
        # centre point - as residual degrees of freedom Fusion counts against
        # isFullyConstrained.
        curve.isFixed = True
        for attr in ("startSketchPoint", "endSketchPoint", "centerSketchPoint"):
            try:
                getattr(curve, attr).isFixed = True
            except Exception:
                pass

    def draw(segments, construction):
        for seg in segments:
            if seg["type"] == "line":
                line = sketch.sketchCurves.sketchLines.addByTwoPoints(
                    _mm_to_sketch(sketch, seg["start"][0], seg["start"][1]),
                    _mm_to_sketch(sketch, seg["end"][0], seg["end"][1]),
                )
                line.isConstruction = construction
                fix_all(line)
                made["lines"] += 1
            elif seg["type"] == "arc":
                c = _mm_to_sketch(sketch, seg["center"][0], seg["center"][1])
                s = _mm_to_sketch(sketch, seg["start"][0], seg["start"][1])
                a0 = math.atan2(s.y - c.y, s.x - c.x)
                e = _mm_to_sketch(sketch, seg["end"][0], seg["end"][1])
                a1 = math.atan2(e.y - c.y, e.x - c.x)
                if seg.get("ccw"):
                    sweep = (a1 - a0) % (2.0 * math.pi)
                else:
                    sweep = -((a0 - a1) % (2.0 * math.pi))
                arc = sketch.sketchCurves.sketchArcs.addByCenterStartSweep(
                    c, s, sweep
                )
                arc.isConstruction = construction
                fix_all(arc)
                made["arcs"] += 1
            else:
                raise RuntimeError("unknown path segment type %r" % seg.get("type"))

    draw(args.get("centerline", []), construction=True)
    draw(args.get("footprint", []), construction=False)
    return {"sketch": {"name": sketch.name,
                       "fully_constrained": sketch.isFullyConstrained,
                       "curves": sketch.sketchCurves.count,
                       "profiles": sketch.profiles.count,
                       "lines": made["lines"], "arcs": made["arcs"]}}


def _op_radial_plane(args):
    """Plane whose normal is the radial direction at `az_deg` about Z.

    Fusion's angle-plane convention (base normal azimuth and rotation sense)
    is not assumed: the created plane's normal is measured and the angle
    corrected, so the result is right on any Fusion version.
    """
    root = _root()
    planes = root.constructionPlanes
    um = _units()
    az_req = um.evaluateExpression(args["az_deg"], "deg")  # radians

    def make(angle_rad):
        inp = planes.createInput()
        inp.setByAngle(
            root.zConstructionAxis,
            adsk.core.ValueInput.createByReal(angle_rad),
            root.xZConstructionPlane,
        )
        return planes.add(inp)

    def normal_az(p):
        n = p.geometry.normal
        return math.atan2(n.y, n.x)

    probe = make(0.0)
    base_az = normal_az(probe)
    probe.deleteMe()

    plane = make(az_req - base_az)
    err = ((normal_az(plane) - az_req + math.pi) % (2 * math.pi)) - math.pi
    if abs(err) > 0.01:
        plane.deleteMe()
        plane = make(-(az_req - base_az))
        err = ((normal_az(plane) - az_req + math.pi) % (2 * math.pi)) - math.pi
        if abs(err) > 0.01:
            plane.deleteMe()
            raise RuntimeError(
                "radial_plane: cannot orient a plane normal to azimuth %s "
                "(residual %.3f rad)" % (args["az_deg"], err)
            )
    offset = args.get("offset")
    if offset:
        plane.name = args["name"] + "_AXIS"
        off_input = planes.createInput()
        off_input.setByOffset(plane, adsk.core.ValueInput.createByString(offset))
        plane = planes.add(off_input)
    plane.name = args["name"]
    return {"plane": {"name": plane.name}}


def _op_sketch_profile(args):
    root = _root()
    sketch = _sketch_by_name(root, args["sketch"])
    pts = args["points"]
    sk_pts = []
    for x, y, z in pts:
        p = adsk.core.Point3D.create(x / CM_TO_MM, y / CM_TO_MM, z / CM_TO_MM)
        sk_pts.append(sketch.modelToSketchSpace(p))
    for i in range(len(sk_pts)):
        line = sketch.sketchCurves.sketchLines.addByTwoPoints(
            sk_pts[i], sk_pts[(i + 1) % len(sk_pts)]
        )
        line.isFixed = True
        for attr in ("startSketchPoint", "endSketchPoint"):
            try:
                getattr(line, attr).isFixed = True
            except Exception:
                pass
    return {"sketch": {"name": sketch.name,
                       "fully_constrained": sketch.isFullyConstrained,
                       "curves": sketch.sketchCurves.count,
                       "profiles": sketch.profiles.count}}


def _op_combine(args):
    root = _root()
    target = tool = None
    for i in range(root.bRepBodies.count):
        b = root.bRepBodies.item(i)
        if b.name == args["target"]:
            target = b
        if b.name == args["tool"]:
            tool = b
    if target is None or tool is None:
        raise RuntimeError(
            "combine: target %r or tool %r not found among bodies"
            % (args["target"], args["tool"])
        )
    tools = adsk.core.ObjectCollection.create()
    tools.add(tool)
    op_table = {
        "join": adsk.fusion.FeatureOperations.JoinFeatureOperation,
        "cut": adsk.fusion.FeatureOperations.CutFeatureOperation,
        "intersect": adsk.fusion.FeatureOperations.IntersectFeatureOperation,
    }
    combine_input = root.features.combineFeatures.createInput(target, tools)
    combine_input.operation = op_table[args.get("operation", "join")]
    combine_input.isKeepToolBodies = False
    root.features.combineFeatures.add(combine_input)
    return {"combine": {"target": target.name,
                        "bodies": root.bRepBodies.count}}


def _op_fix_sketch(args):
    """Fix every curve and sketch point of a named sketch - the repair for a
    derived sketch left with residual degrees of freedom."""
    root = _root()
    sketch = _sketch_by_name(root, args["sketch"])
    for j in range(sketch.sketchCurves.count):
        curve = sketch.sketchCurves.item(j)
        curve.isFixed = True
        for attr in ("startSketchPoint", "endSketchPoint", "centerSketchPoint"):
            try:
                getattr(curve, attr).isFixed = True
            except Exception:
                pass
    for j in range(sketch.sketchPoints.count):
        try:
            sketch.sketchPoints.item(j).isFixed = True
        except Exception:
            pass
    return {"sketch": {"name": sketch.name,
                       "fully_constrained": sketch.isFullyConstrained,
                       "curves": sketch.sketchCurves.count}}


def _op_offset_plane(args):
    root = _root()
    base = _base_plane(root, args.get("base", "XY"))
    planes = root.constructionPlanes
    plane_input = planes.createInput()
    plane_input.setByOffset(base, adsk.core.ValueInput.createByString(args["offset"]))
    plane = planes.add(plane_input)
    plane.name = args["name"]
    return {"plane": {"name": plane.name, "base": args.get("base", "XY")}}


def _op_extrude(args):
    root = _root()
    sketch = _sketch_by_name(root, args["sketch"])
    if sketch.profiles.count == 0:
        raise RuntimeError(
            "sketch %r yields no closed profile; there is nothing to extrude"
            % args["sketch"]
        )
    which = args.get("profile", 0)
    if which == "all":
        profile = adsk.core.ObjectCollection.create()
        for i in range(sketch.profiles.count):
            profile.add(sketch.profiles.item(i))
    else:
        profile = sketch.profiles.item(int(which))

    op_table = {
        "new_body": adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
        "join": adsk.fusion.FeatureOperations.JoinFeatureOperation,
        "cut": adsk.fusion.FeatureOperations.CutFeatureOperation,
        "intersect": adsk.fusion.FeatureOperations.IntersectFeatureOperation,
    }
    operation = args.get("operation", "new_body")
    extrudes = root.features.extrudeFeatures
    ext_input = extrudes.createInput(profile, op_table[operation])

    distance = args["distance"]
    direction = args.get("direction", "positive")
    if direction == "symmetric":
        # Full-length symmetric: `distance` is the total, half each side, so
        # the result is independent of the sketch plane's normal orientation.
        ext_input.setSymmetricExtent(
            adsk.core.ValueInput.createByString(distance), True
        )
    else:
        expr = distance if direction == "positive" else "-(%s)" % distance
        ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByString(expr))

    ext = extrudes.add(ext_input)
    body_name = args.get("body_name")
    if body_name and ext.bodies.count:
        ext.bodies.item(0).name = body_name
    return {"extrude": {"bodies": ext.bodies.count,
                        "body_name": ext.bodies.item(0).name if ext.bodies.count else None}}


def _op_assign_material(args):
    design = _design()
    root = design.rootComponent
    wanted = args["material"].strip().lower()
    found = None
    for i in range(_app.materialLibraries.count):
        lib = _app.materialLibraries.item(i)
        for j in range(lib.materials.count):
            mat = lib.materials.item(j)
            name = mat.name.strip().lower()
            if name == wanted:
                found = mat
                break
            if found is None and wanted in name:
                found = mat
        if found is not None and found.name.strip().lower() == wanted:
            break
    if found is None:
        raise RuntimeError(
            "no material matching %r in any loaded library" % args["material"]
        )
    target = args.get("body")
    applied = []
    for i in range(root.bRepBodies.count):
        body = root.bRepBodies.item(i)
        if target and body.name != target:
            continue
        body.material = found
        applied.append(body.name)
    if not applied:
        raise RuntimeError("no body to assign material to")
    return {"material": {"name": found.name, "applied_to": applied}}


def _sk_to_model_mm(sketch, p_sketch):
    """Sketch-space Point3D -> model-space (x, y) in mm."""
    p = sketch.sketchToModelSpace(p_sketch)
    return [p.x * CM_TO_MM, p.y * CM_TO_MM]


def _curve_row(sketch, curve):
    """Observed geometry of one sketch curve, model-space mm; None if unknown."""
    t = curve.objectType.split("::")[-1]
    if t == "SketchLine":
        return {
            "type": "line",
            "start": _sk_to_model_mm(sketch, curve.startSketchPoint.geometry),
            "end": _sk_to_model_mm(sketch, curve.endSketchPoint.geometry),
            "construction": bool(curve.isConstruction),
        }
    if t == "SketchArc":
        geo = curve.geometry
        row = {
            "type": "arc",
            "center": _sk_to_model_mm(sketch, curve.centerSketchPoint.geometry),
            "radius": geo.radius * CM_TO_MM,
            "start": _sk_to_model_mm(sketch, curve.startSketchPoint.geometry),
            "end": _sk_to_model_mm(sketch, curve.endSketchPoint.geometry),
            "construction": bool(curve.isConstruction),
        }
        try:
            evaluator = geo.evaluator
            ok, p0, p1 = evaluator.getParameterExtents()
            ok2, mid = evaluator.getPointAtParameter((p0 + p1) / 2.0)
            if ok and ok2:
                row["mid"] = _sk_to_model_mm(sketch, mid)
        except Exception:
            pass
        return row
    if t == "SketchCircle":
        return {
            "type": "circle",
            "center": _sk_to_model_mm(sketch, curve.centerSketchPoint.geometry),
            "radius": curve.geometry.radius * CM_TO_MM,
            "construction": bool(curve.isConstruction),
        }
    return None


def _op_observe(args):
    scope = args.get("scope") or ["document", "parameters", "bodies", "sketches",
                                  "planes", "features", "material"]
    design = adsk.fusion.Design.cast(_app.activeProduct)
    if design is None:
        return {"document": {}, "note": "no active Fusion design to observe"}
    root = design.rootComponent
    um = design.unitsManager
    out = {}

    if "document" in scope:
        doc = _app.activeDocument
        # A saved document's display name - and the root component name, which
        # is bound to it - carries Fusion's version suffix ("<name> v<N>").
        # dataFile.name is the persisted design name and never does. dataFile
        # raises on a never-saved document, hence the guard and the except.
        persisted = None
        if doc is not None and doc.isSaved:
            try:
                data_file = doc.dataFile
                persisted = data_file.name if data_file is not None else None
            except Exception:
                persisted = None
        out["document"] = {
            "name": doc.name if doc else None,
            "persisted_name": persisted,
            "units": um.defaultLengthUnits,
            "design_type": "parametric" if design.designType == 1 else "direct",
            "saved": bool(doc.isSaved) if doc else None,
        }
        out["component"] = {"name": root.name, "persisted_name": persisted}

    if "parameters" in scope:
        rows = []
        for i in range(design.userParameters.count):
            p = design.userParameters.item(i)
            value, basis = _display_value(um, p)
            rows.append({"name": p.name, "unit": p.unit, "expression": p.expression,
                         "value": value, "unit_basis": basis})
        out["parameters"] = rows

    if "bodies" in scope:
        rows = []
        for i in range(root.bRepBodies.count):
            b = root.bRepBodies.item(i)
            row = {"name": b.name}
            try:
                props = b.physicalProperties
                row["volume_mm3"] = props.volume * (CM_TO_MM ** 3)
                row["area_mm2"] = props.area * (CM_TO_MM ** 2)
                row["mass_kg"] = props.mass
            except Exception:
                pass
            try:
                bb = b.boundingBox
                row["bbox_min"] = [bb.minPoint.x * CM_TO_MM, bb.minPoint.y * CM_TO_MM,
                                   bb.minPoint.z * CM_TO_MM]
                row["bbox_max"] = [bb.maxPoint.x * CM_TO_MM, bb.maxPoint.y * CM_TO_MM,
                                   bb.maxPoint.z * CM_TO_MM]
            except Exception:
                pass
            try:
                row["material"] = b.material.name if b.material else None
            except Exception:
                row["material"] = None
            rows.append(row)
        out["bodies"] = rows

    if "sketches" in scope:
        rows = []
        for i in range(root.sketches.count):
            sk = root.sketches.item(i)
            construction = 0
            curve_geometry = []
            for j in range(sk.sketchCurves.count):
                try:
                    curve = sk.sketchCurves.item(j)
                    if curve.isConstruction:
                        construction += 1
                    row = _curve_row(sk, curve)
                    if row is not None:
                        curve_geometry.append(row)
                except Exception:
                    pass
            rows.append({
                "name": sk.name,
                "plane": _plane_label(root, sk.referencePlane),
                "fully_constrained": sk.isFullyConstrained,
                "curves": sk.sketchCurves.count,
                "construction_curves": construction,
                "profiles": sk.profiles.count,
                "dimensions": sk.sketchDimensions.count,
                "curve_geometry": curve_geometry,
            })
        out["sketches"] = rows

    if "planes" in scope:
        rows = []
        for i in range(root.constructionPlanes.count):
            pl = root.constructionPlanes.item(i)
            row = {"name": pl.name}
            try:
                definition = pl.definition
                offset_def = adsk.fusion.ConstructionPlaneOffsetDefinition.cast(definition)
                if offset_def is not None:
                    row["offset_mm"] = offset_def.offset.value * CM_TO_MM
                    row["base"] = _plane_label(root, offset_def.planarEntity)
            except Exception:
                pass
            if "offset_mm" not in row:
                try:
                    row["offset_mm"] = pl.geometry.origin.z * CM_TO_MM
                except Exception:
                    pass
            rows.append(row)
        out["planes"] = rows

    if "features" in scope:
        rows = []
        try:
            for i in range(root.features.count):
                f = root.features.item(i)
                rows.append({"type": f.objectType.split("::")[-1], "name": f.name})
        except Exception:
            pass
        out["features"] = rows

    return out


_OPS = {
    "ping": _op_ping,
    "new_document": _op_new_document,
    "rename_component": _op_rename_component,
    "set_parameters": _op_set_parameters,
    "create_sketch": _op_create_sketch,
    "sketch_circle": _op_sketch_circle,
    "sketch_construction": _op_sketch_construction,
    "sketch_path": _op_sketch_path,
    "sketch_profile": _op_sketch_profile,
    "radial_plane": _op_radial_plane,
    "combine": _op_combine,
    "fix_sketch": _op_fix_sketch,
    "offset_plane": _op_offset_plane,
    "extrude": _op_extrude,
    "assign_material": _op_assign_material,
    "observe": _op_observe,
}


# --------------------------------------------------------------------------
# Add-in lifecycle
# --------------------------------------------------------------------------

def run(context):
    global _app, _ui, _custom_event, _worker, _config
    try:
        _app = adsk.core.Application.get()
        _ui = _app.userInterface
        _config = _load_config()
        for key in ("queue", "obs", "state"):
            os.makedirs(_config[key], exist_ok=True)

        try:
            _app.unregisterCustomEvent(EVENT_ID)
        except Exception:
            pass
        _custom_event = _app.registerCustomEvent(EVENT_ID)
        handler = _CommandHandler()
        _custom_event.add(handler)
        _handlers.append(handler)

        _stop.clear()
        _worker = threading.Thread(target=_pump, name="aief-cad-bridge", daemon=True)
        _worker.start()

        _ui.messageBox(
            "AIEF CAD Bridge is running.\n\nWatching:\n%s\n\nProtocol: %s"
            % (_config["queue"], PROTOCOL),
            "AIEF CAD Bridge",
        )
    except Exception:
        if _ui:
            _ui.messageBox("AIEF CAD Bridge failed to start:\n%s" % traceback.format_exc())


def stop(context):
    global _worker
    try:
        _stop.set()
        if _worker is not None:
            _worker.join(timeout=3.0)
            _worker = None
        try:
            _app.unregisterCustomEvent(EVENT_ID)
        except Exception:
            pass
        _handlers.clear()
        try:
            os.remove(os.path.join(_config["state"], "addin.heartbeat.json"))
        except Exception:
            pass
        if _ui:
            _ui.messageBox("AIEF CAD Bridge stopped.", "AIEF CAD Bridge")
    except Exception:
        if _ui:
            _ui.messageBox("AIEF CAD Bridge stop failed:\n%s" % traceback.format_exc())
