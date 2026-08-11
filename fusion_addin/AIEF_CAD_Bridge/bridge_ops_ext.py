"""Hot-reloadable operation extension for AIEF_CAD_Bridge.

Loaded (and re-loaded on change) by the shell's `_ext_op` hook, so the
operations here deploy without an add-in restart. Handlers are
self-contained: they fetch the application themselves and raise plain
RuntimeError - the shell converts exceptions to ERROR observations.

Lifecycle operations live here: the session-automation layer the
orchestrator drives so a human never has to click Save or recover a
failed increment by hand.
"""

import adsk.core
import adsk.fusion


def _app():
    return adsk.core.Application.get()


def _persisted_name(doc):
    try:
        if doc is not None and doc.isSaved:
            data_file = doc.dataFile
            return data_file.name if data_file is not None else None
    except Exception:
        pass
    return None


def _find_document(name):
    app = _app()
    active = app.activeDocument
    if active is not None and _persisted_name(active) == name:
        return active
    for i in range(app.documents.count):
        doc = app.documents.item(i)
        if _persisted_name(doc) == name:
            return doc
    return None


def op_save_document(args):
    """Save the named (or active) design, committing a new version."""
    app = _app()
    name = args.get("name")
    doc = _find_document(name) if name else app.activeDocument
    if doc is None:
        raise RuntimeError("save_document: no open document named %r" % name)
    if not doc.isSaved:
        if not name:
            raise RuntimeError(
                "save_document: an unnamed never-saved document cannot be "
                "first-saved safely"
            )
        _first_save(doc, name)
        data_file = doc.dataFile
        return {"document": {"name": _persisted_name(doc), "saved": True,
                             "first_saved": True,
                             "version": data_file.versionNumber
                             if data_file else None}}
    if doc.isModified:
        doc.save(args.get("description") or "AIEF verified increment")
    data_file = doc.dataFile
    return {"document": {
        "name": _persisted_name(doc),
        "saved": True,
        "version": data_file.versionNumber if data_file else None,
    }}


def op_revert_document(args):
    """Discard unsaved changes: close without saving, reopen the saved
    version, and activate it - the safe recovery from a failed increment."""
    app = _app()
    name = args["name"]
    doc = _find_document(name)
    if doc is None:
        raise RuntimeError("revert_document: no open document named %r" % name)
    if not doc.isSaved:
        raise RuntimeError("revert_document: %r has no saved version" % name)
    data_file = doc.dataFile
    doc.close(False)  # discard unsaved changes
    reopened = app.documents.open(data_file, True)
    if reopened is None:
        raise RuntimeError("revert_document: reopen failed for %r" % name)
    return {"document": {
        "name": _persisted_name(reopened),
        "reverted": True,
        "version": data_file.versionNumber if data_file else None,
    }}


def _home_folder():
    """The data folder to first-save new designs into: the folder holding
    any already-saved open design, else the active project root."""
    app = _app()
    for i in range(app.documents.count):
        doc = app.documents.item(i)
        try:
            if doc.isSaved and doc.dataFile is not None:
                return doc.dataFile.parentFolder
        except Exception:
            continue
    return app.data.activeProject.rootFolder


def _first_save(doc, name):
    doc.saveAs(name, _home_folder(), "AIEF first save", "")
    return doc


def op_rename_component(args):
    """Component identity under the ruled persisted-name semantics.

    Overrides the shell op: on a never-saved document the identity is
    realised by performing the first save under the required name - the
    lifecycle action Fusion ties naming to - instead of failing against
    the display-name binding.
    """
    app = _app()
    doc = app.activeDocument
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        raise RuntimeError("rename_component: no active design")
    root = design.rootComponent
    name = args["name"]
    if _persisted_name(doc) == name:
        return {"component": {"name": root.name, "persisted_name": name}}
    if doc is not None and not doc.isSaved:
        _first_save(doc, name)
        return {"component": {"name": root.name,
                              "persisted_name": _persisted_name(doc),
                              "first_saved": True}}
    root.name = name
    return {"component": {"name": root.name}}


def op_export_model(args):
    """Export the active design to absolute paths outside the repository.

    formats: subset of step, stl, f3d. Returns the files written with
    sizes, so provenance can record them.
    """
    import os

    app = _app()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        raise RuntimeError("export_model: no active design")
    out_dir = args["directory"]
    base = args.get("basename") or (_persisted_name(app.activeDocument)
                                    or "design")
    os.makedirs(out_dir, exist_ok=True)
    mgr = design.exportManager
    written = []
    for fmt in args.get("formats", ["step"]):
        path = os.path.join(out_dir, base + {"step": ".step", "stl": ".stl",
                                             "f3d": ".f3d"}[fmt])
        if fmt == "step":
            ok = mgr.execute(mgr.createSTEPExportOptions(path))
        elif fmt == "stl":
            opts = mgr.createSTLExportOptions(design.rootComponent, path)
            ok = mgr.execute(opts)
        else:
            ok = mgr.execute(mgr.createFusionArchiveExportOptions(path))
        written.append({"format": fmt, "path": path, "ok": bool(ok),
                        "bytes": os.path.getsize(path)
                        if os.path.isfile(path) else 0})
    return {"exported": written}


def op_assign_material(args):
    """Assign a physical material - component-level when no body exists yet.

    Overrides the shell op: on a fresh design the material lands on the root
    component, which every later body inherits ('From Component' is Fusion's
    default body material source), so setup-time assignment is valid before
    geometry.
    """
    app = _app()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        raise RuntimeError("assign_material: no active design")
    root = design.rootComponent
    wanted = args["material"].strip().lower()
    found = None
    for i in range(app.materialLibraries.count):
        lib = app.materialLibraries.item(i)
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
        raise RuntimeError("no material matching %r in any loaded library"
                           % args["material"])
    target = args.get("body")
    applied = []
    for i in range(root.bRepBodies.count):
        body = root.bRepBodies.item(i)
        if target and body.name != target:
            continue
        body.material = found
        applied.append(body.name)
    if not applied:
        root.material = found
        applied = ["<component>"]
    return {"material": {"name": found.name, "applied_to": applied}}


def op_extrude(args):
    """Extrude with deterministic profile selection.

    Overrides the shell op to add area-based selection: 'smallest' and
    'largest' pick a profile by area - the deterministic way to cut an
    annular groove from a two-circle sketch, where index order is not
    guaranteed by Fusion.
    """
    app = _app()
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    sketch = None
    for i in range(root.sketches.count):
        if root.sketches.item(i).name == args["sketch"]:
            sketch = root.sketches.item(i)
            break
    if sketch is None:
        raise RuntimeError(
            "extrude: sketch %r not found; visible: [%s] in doc %r"
            % (args["sketch"],
               ", ".join(root.sketches.item(i).name
                         for i in range(root.sketches.count)),
               app.activeDocument.name if app.activeDocument else None))
    if sketch.profiles.count == 0:
        raise RuntimeError("sketch %r yields no closed profile" % args["sketch"])

    which = args.get("profile", 0)
    if which == "all":
        profile = adsk.core.ObjectCollection.create()
        for i in range(sketch.profiles.count):
            profile.add(sketch.profiles.item(i))
    elif which in ("smallest", "largest"):
        ranked = sorted(
            (sketch.profiles.item(i) for i in range(sketch.profiles.count)),
            key=lambda p: p.areaProperties().area,
        )
        profile = ranked[0] if which == "smallest" else ranked[-1]
    else:
        profile = sketch.profiles.item(int(which))

    op_table = {
        "new_body": adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
        "join": adsk.fusion.FeatureOperations.JoinFeatureOperation,
        "cut": adsk.fusion.FeatureOperations.CutFeatureOperation,
        "intersect": adsk.fusion.FeatureOperations.IntersectFeatureOperation,
    }
    extrudes = root.features.extrudeFeatures
    ext_input = extrudes.createInput(profile, op_table[args.get("operation", "new_body")])
    distance = args["distance"]
    direction = args.get("direction", "positive")
    if direction == "symmetric":
        ext_input.setSymmetricExtent(
            adsk.core.ValueInput.createByString(distance), True)
    else:
        expr = distance if direction == "positive" else "-(%s)" % distance
        ext_input.setDistanceExtent(False, adsk.core.ValueInput.createByString(expr))
    ext = extrudes.add(ext_input)
    body_name = args.get("body_name")
    if body_name and ext.bodies.count:
        ext.bodies.item(0).name = body_name
    return {"extrude": {"bodies": ext.bodies.count,
                        "body_name": ext.bodies.item(0).name
                        if ext.bodies.count else None}}


OPS = {
    "extrude": op_extrude,
    "assign_material": op_assign_material,
    "save_document": op_save_document,
    "revert_document": op_revert_document,
    "rename_component": op_rename_component,
    "export_model": op_export_model,
}
