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
        raise RuntimeError(
            "save_document: the document has never been saved; the first "
            "save chooses a cloud location and is reserved to the human"
        )
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


OPS = {
    "save_document": op_save_document,
    "revert_document": op_revert_document,
}
