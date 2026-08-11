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


def _design_of(doc):
    try:
        return adsk.fusion.Design.cast(
            doc.products.itemByProductType("DesignProductType"))
    except Exception:
        return None


def _intended_name(doc):
    """Identity bound at setup on a not-yet-persisted document."""
    try:
        design = _design_of(doc)
        if design is None:
            return None
        attr = design.attributes.itemByName("aief", "intended_name")
        return attr.value if attr is not None else None
    except Exception:
        return None


def _persisted_name(doc):
    """Saved design name, else the bound-but-unsaved intended identity.

    Lifecycle rule: identity binds early, persistence happens only at the
    verified save (`save_document`). Nothing else may first-save."""
    try:
        if doc is not None and doc.isSaved:
            data_file = doc.dataFile
            if data_file is not None:
                return data_file.name
    except Exception:
        pass
    return _intended_name(doc)


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
    """Save the named (or active) design, committing a new version.

    The ONLY operation allowed to first-save: persistence is the reward of
    a verified increment, dispatched by the lifecycle layer on PASS."""
    app = _app()
    name = args.get("name")
    doc = _find_document(name) if name else app.activeDocument
    if doc is None:
        raise RuntimeError("save_document: no open document named %r" % name)
    if not doc.isSaved:
        first_name = name or _intended_name(doc)
        if not first_name:
            raise RuntimeError(
                "save_document: an unnamed never-saved document cannot be "
                "first-saved safely"
            )
        _first_save(doc, first_name)
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

    Overrides the shell op. On a never-saved document the identity is
    BOUND (an `aief:intended_name` design attribute) but NOT persisted -
    the previous form first-saved here, which is exactly how failed runs
    left blank persistent designs behind (the ZZ-ORPHAN-BLANK-SHELL /
    ZZ-INTERIM defect class). Persistence now happens only at the
    verified `save_document`.
    """
    app = _app()
    doc = app.activeDocument
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        raise RuntimeError("rename_component: no active design")
    root = design.rootComponent
    name = args["name"]
    if _persisted_name(doc) == name:
        return {"component": {"name": root.name, "persisted_name": name,
                              "saved": bool(doc.isSaved) if doc else None}}
    if doc is not None and not doc.isSaved:
        try:
            existing = design.attributes.itemByName("aief", "intended_name")
            if existing is not None:
                existing.value = name
            else:
                design.attributes.add("aief", "intended_name", name)
        except Exception as exc:
            raise RuntimeError(
                "rename_component: could not bind the intended identity: %s"
                % exc)
        return {"component": {"name": root.name, "persisted_name": name,
                              "identity_bound": True, "saved": False}}
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
    if found is None and args.get("density"):
        # The library lacks the stated material: create it at the stated
        # density, copied from any available base - the density is what a
        # mass verification measures, and the requirement states it.
        base = None
        for i in range(app.materialLibraries.count):
            lib = app.materialLibraries.item(i)
            if lib.materials.count:
                base = lib.materials.item(0)
                break
        if base is not None:
            existing = design.materials.itemByName(args["material"])
            if existing is not None:
                found = existing
            else:
                found = design.materials.addByCopy(base, args["material"])
                try:
                    prop = found.materialProperties.itemByName("Density")
                    prop.value = float(args["density"])  # kg/m^3
                except Exception:
                    pass
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


# --------------------------------------------------------------------------
# Document-management and assembly vocabulary
#
# Generic by construction: identity is a persisted design name, placement is
# a stated transform, observation is actual state. No component knowledge.
# --------------------------------------------------------------------------

MM_PER_CM = 10.0


def _find_data_file(name, file_id=None):
    """Resolve a saved design. An id pins the exact file; a bare name must be
    unique - two files sharing a name is exactly the ambiguity that must
    refuse rather than guess."""
    folder = _home_folder()
    files = folder.dataFiles
    names = []
    matches = []
    for i in range(files.count):
        df = files.item(i)
        names.append(df.name)
        if file_id is not None:
            try:
                if df.id == file_id:
                    return df
            except Exception:
                pass
        elif df.name == name:
            matches.append(df)
    if file_id is not None:
        raise RuntimeError("no saved design with id %r in folder %r"
                           % (file_id, folder.name))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise RuntimeError("ambiguous: %d saved designs named %r; "
                           "select by id" % (len(matches), name))
    raise RuntimeError("no saved design named %r in folder %r; present: [%s]"
                       % (name, folder.name, ", ".join(sorted(names))))


def op_list_documents(args):
    """Enumerate open documents and the home folder's saved designs - the
    observation orphan classification consumes."""
    app = _app()
    open_docs = []
    for i in range(app.documents.count):
        doc = app.documents.item(i)
        row = {"display_name": doc.name,
               "persisted_name": _persisted_name(doc),
               "saved": bool(doc.isSaved)}
        try:
            row["modified"] = bool(doc.isModified)
        except Exception:
            row["modified"] = None
        try:
            df = doc.dataFile if doc.isSaved else None
            row["version"] = df.versionNumber if df is not None else None
        except Exception:
            row["version"] = None
        open_docs.append(row)
    folder = _home_folder()
    saved = []
    files = folder.dataFiles
    for i in range(files.count):
        df = files.item(i)
        row = {"name": df.name}
        try:
            row["version"] = df.versionNumber
        except Exception:
            row["version"] = None
        try:
            row["id"] = df.id
        except Exception:
            row["id"] = None
        try:
            row["created"] = df.dateCreated
        except Exception:
            row["created"] = None
        saved.append(row)
    return {"open_documents": open_docs,
            "folder": {"name": folder.name},
            "saved_designs": saved}


def op_open_document(args):
    """Open (and activate) a saved design by its persisted name or id."""
    app = _app()
    name = args.get("name")
    if name and not args.get("id"):
        doc = _find_document(name)
        if doc is not None:
            doc.activate()
            return {"document": {"name": name, "opened": False,
                                 "activated": True}}
    df = _find_data_file(name, args.get("id"))
    opened = app.documents.open(df, True)
    if opened is None:
        raise RuntimeError("open_document: open failed for %r" % name)
    return {"document": {"name": _persisted_name(opened), "opened": True,
                         "activated": True, "version": df.versionNumber}}


def op_close_document(args):
    """Close a named open document, discarding unsaved changes.

    Display name is matched before persisted name: display names carry the
    version suffix and stay unique when two files share a persisted name."""
    name = args["name"]
    app = _app()
    doc = None
    for i in range(app.documents.count):
        d = app.documents.item(i)
        if d.name == name:
            doc = d
            break
    if doc is None:
        doc = _find_document(name)
    if doc is None:
        raise RuntimeError("close_document: no open document named %r" % name)
    closed_display = doc.name
    doc.close(False)
    return {"document": {"name": closed_display, "closed": True}}


def op_discard_document(args):
    """Close a never-persisted document, discarding it entirely - the
    failure-recovery primitive. Refuses a saved document (that is
    revert_document's job), so an authoritative design can never be
    discarded by a failure path."""
    app = _app()
    name = args.get("name")
    doc = None
    if name:
        for i in range(app.documents.count):
            d = app.documents.item(i)
            if d.name == name or _persisted_name(d) == name:
                doc = d
                break
    else:
        doc = app.activeDocument
    if doc is None:
        # Nothing to discard is success for a recovery path: the goal is
        # the absence of the artifact.
        return {"document": {"name": name, "discarded": False,
                             "absent": True}}
    if doc.isSaved:
        raise RuntimeError(
            "discard_document: %r is persisted; a saved design is never "
            "discarded by recovery - use revert_document" % name)
    display = doc.name
    doc.close(False)
    return {"document": {"name": name or display, "discarded": True}}


def op_delete_data_file(args):
    """Delete a saved design by exact name (or pinned id). Refuses protected
    names and open documents - deletion is dispatched only after
    classification proves it safe, and this guard holds that proof at the
    boundary."""
    name = args["name"]
    protected = set(args.get("protected") or [])
    if name in protected:
        raise RuntimeError("delete_data_file: %r is protected" % name)
    if _find_document(name) is not None:
        raise RuntimeError("delete_data_file: %r is open; close it first" % name)
    df = _find_data_file(name, args.get("id"))
    ok = df.deleteMe()
    if not ok:
        raise RuntimeError("delete_data_file: Fusion refused to delete %r "
                           "(referenced by another design?)" % name)
    return {"deleted": {"name": name}}


def op_rename_data_file(args):
    """Rename a saved design, pinned by id - the non-destructive resolution
    of a name collision: history is preserved, ambiguity is removed."""
    df = _find_data_file(args.get("name"), args.get("id"))
    old = df.name
    df.name = args["new_name"]
    return {"renamed": {"from": old, "to": df.name, "id": args.get("id")}}


def _matrix_from_args(args):
    """Placement = Rz(rotate_z) . Rx(rotate_x), then translation (mm).

    rotate_x supports flipped installations (a pin entered from the far
    face); rotate_z is the clocking rotation the azimuth maps demand."""
    import math

    core = adsk.core
    origin = core.Point3D.create(0, 0, 0)
    matrix = core.Matrix3D.create()
    rot_x = float(args.get("rotate_x_deg") or 0.0)
    if rot_x:
        matrix.setToRotation(math.radians(rot_x),
                             core.Vector3D.create(1, 0, 0), origin)
    rot_z = float(args.get("rotate_z_deg") or 0.0)
    if rot_z:
        mz = core.Matrix3D.create()
        mz.setToRotation(math.radians(rot_z),
                         core.Vector3D.create(0, 0, 1), origin)
        matrix.transformBy(mz)
    t = args.get("translate_mm") or [0.0, 0.0, 0.0]
    matrix.translation = core.Vector3D.create(
        float(t[0]) / MM_PER_CM, float(t[1]) / MM_PER_CM,
        float(t[2]) / MM_PER_CM)
    return matrix


def _capture_position(design):
    try:
        if design.snapshots.hasPendingSnapshot:
            design.snapshots.add()
    except Exception:
        pass


def op_insert_occurrence(args):
    """Insert a saved design into the active design as a referenced
    occurrence at a stated transform - the native assembly primitive.
    Verified component geometry is reused, never remodelled."""
    app = _app()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        raise RuntimeError("insert_occurrence: no active design")
    df = _find_data_file(args["name"], args.get("id"))
    if args.get("use_latest_version"):
        # The session's lineage cache can serve a stale tip after an
        # out-of-session save; the explicit latest-version object bypasses
        # it (found repairing a v4-bound insert whose true tip was v5).
        try:
            lv = df.latestVersion
            if lv is not None:
                df = lv
        except Exception:
            pass
    matrix = _matrix_from_args(args)
    occ = design.rootComponent.occurrences.addByInsert(df, matrix, True)
    if occ is None:
        raise RuntimeError("insert_occurrence: Fusion returned no occurrence "
                           "for %r" % args["name"])
    if args.get("ground"):
        occ.isGrounded = True
    _capture_position(design)
    return {"occurrence": {
        "name": occ.name,
        "component": occ.component.name,
        "source_design": args["name"],
        "grounded": bool(occ.isGrounded),
    }}


def _find_occurrence(design, name):
    occs = design.rootComponent.occurrences
    names = []
    for i in range(occs.count):
        occ = occs.item(i)
        names.append(occ.name)
        if occ.name == name or occ.component.name == name:
            return occ
    raise RuntimeError("no occurrence named %r; present: [%s]"
                       % (name, ", ".join(names)))


def op_transform_occurrence(args):
    """Re-place a named occurrence at a stated transform."""
    app = _app()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        raise RuntimeError("transform_occurrence: no active design")
    occ = _find_occurrence(design, args["name"])
    was_grounded = bool(occ.isGrounded)
    if was_grounded:
        occ.isGrounded = False
    matrix = _matrix_from_args(args)
    try:
        occ.transform2 = matrix
    except Exception:
        occ.transform = matrix
    if was_grounded or args.get("ground"):
        occ.isGrounded = True
    _capture_position(design)
    return {"occurrence": {"name": occ.name, "transformed": True}}


def op_delete_occurrence(args):
    """Remove a named occurrence from the active design."""
    app = _app()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        raise RuntimeError("delete_occurrence: no active design")
    occ = _find_occurrence(design, args["name"])
    name = occ.name
    if not occ.deleteMe():
        raise RuntimeError("delete_occurrence: Fusion refused to delete %r"
                           % name)
    return {"deleted": {"name": name}}


def op_data_file_info(args):
    """Diagnostic: what the data platform reports for one saved design -
    tip version, version list, and whether a newer version is visible."""
    df = _find_data_file(args.get("name"), args.get("id"))
    out = {"name": df.name}
    for attr in ("versionNumber", "latestVersionNumber", "isCloudOnly"):
        try:
            out[attr] = getattr(df, attr)
        except Exception as exc:
            out[attr] = "ERR:%s" % exc
    try:
        versions = df.versions
        out["versions"] = [versions.item(i).versionNumber
                           for i in range(versions.count)]
    except Exception as exc:
        out["versions"] = "ERR:%s" % exc
    try:
        lv = df.latestVersion
        out["latest_version_number"] = lv.versionNumber if lv else None
    except Exception as exc:
        out["latest_version_number"] = "ERR:%s" % exc
    return {"data_file": out}


def op_update_references(args):
    """Bring every referenced design in the active document up to its
    latest version - the repair for an insert that bound a stale one."""
    app = _app()
    doc = app.activeDocument
    if doc is None:
        raise RuntimeError("update_references: no active document")
    ok = doc.updateAllReferences()
    return {"references": {"updated": bool(ok)}}


def op_observe_assembly(args):
    """Actual assembly state: every occurrence with identity, source design,
    transform, assembly-space bounds and mass. The only input to assembly
    verification - intent is never consulted."""
    import math

    app = _app()
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        raise RuntimeError("observe_assembly: no active design")
    doc = app.activeDocument
    root = design.rootComponent
    occs = root.occurrences
    rows = []
    for i in range(occs.count):
        occ = occs.item(i)
        row = {"name": occ.name, "component": occ.component.name,
               "grounded": bool(occ.isGrounded)}
        try:
            src_doc = occ.component.parentDesign.parentDocument
            src_df = src_doc.dataFile if src_doc.isSaved else None
            row["source_design"] = src_df.name if src_df is not None else None
            row["source_version"] = (src_df.versionNumber
                                     if src_df is not None else None)
        except Exception:
            row["source_design"] = None
        try:
            m = occ.transform2
        except Exception:
            m = occ.transform
        cells = m.asArray()
        row["translate_mm"] = [cells[3] * MM_PER_CM, cells[7] * MM_PER_CM,
                               cells[11] * MM_PER_CM]
        row["rotate_z_deg"] = math.degrees(math.atan2(cells[4], cells[0]))
        # m22: +1 upright, -1 flipped by Rx(180) - the two placements the
        # vocabulary can command.
        row["z_axis_scale"] = cells[10]
        try:
            props = occ.physicalProperties
            row["mass_kg"] = props.mass
            row["volume_mm3"] = props.volume * (MM_PER_CM ** 3)
        except Exception:
            pass
        bmin = [None, None, None]
        bmax = [None, None, None]
        bodies = 0
        for j in range(occ.component.bRepBodies.count):
            body = occ.component.bRepBodies.item(j)
            try:
                proxy = body.createForAssemblyContext(occ)
                bb = proxy.boundingBox
                lo = [bb.minPoint.x, bb.minPoint.y, bb.minPoint.z]
                hi = [bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z]
            except Exception:
                continue
            bodies += 1
            for k in range(3):
                v_lo = lo[k] * MM_PER_CM
                v_hi = hi[k] * MM_PER_CM
                if bmin[k] is None or v_lo < bmin[k]:
                    bmin[k] = v_lo
                if bmax[k] is None or v_hi > bmax[k]:
                    bmax[k] = v_hi
        row["bodies"] = bodies
        if bmin[0] is not None:
            row["bbox_min"] = bmin
            row["bbox_max"] = bmax
        rows.append(row)
    persisted = _persisted_name(doc)
    return {"document": {"name": doc.name if doc else None,
                         "persisted_name": persisted,
                         "saved": bool(doc.isSaved) if doc else None},
            "occurrences": rows}


OPS = {
    "extrude": op_extrude,
    "assign_material": op_assign_material,
    "save_document": op_save_document,
    "discard_document": op_discard_document,
    "revert_document": op_revert_document,
    "rename_component": op_rename_component,
    "export_model": op_export_model,
    "list_documents": op_list_documents,
    "rename_data_file": op_rename_data_file,
    "open_document": op_open_document,
    "close_document": op_close_document,
    "delete_data_file": op_delete_data_file,
    "insert_occurrence": op_insert_occurrence,
    "update_references": op_update_references,
    "data_file_info": op_data_file_info,
    "transform_occurrence": op_transform_occurrence,
    "delete_occurrence": op_delete_occurrence,
    "observe_assembly": op_observe_assembly,
}
