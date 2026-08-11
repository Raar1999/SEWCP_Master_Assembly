"""Document-creation lifecycle: a failed attempt persists nothing.

The defect class under regression: setup-time first-saves left blank or
interim designs saved in the cloud whenever a run failed or died
(ZZ-ORPHAN-BLANK-SHELL, ZZ-INTERIM-ATTEMPT). The repaired lifecycle binds
identity without persistence, saves only on verified PASS, and disposes
of the document (discard unsaved / revert saved) on failure.

Client-side proofs run against fakes at the bridge seam; the Fusion-side
contract is proven structurally against the add-in source, which is the
single deployed artifact.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "tests"))

from aief_cad.assembly import AssemblyRunner, load_assembly_package  # noqa: E402
from aief_cad.bridge.protocol import PROTOCOL_VERSION, decode_observation  # noqa: E402
from aief_cad.orchestrator import Orchestrator  # noqa: E402

from test_cad_bridge import SEWCP_PACKAGE, FakeFusion  # noqa: E402

EXT_SOURCE = (REPO / "fusion_addin/AIEF_CAD_Bridge/bridge_ops_ext.py"
              ).read_text(encoding="utf-8")
SHELL_SOURCE = (REPO / "fusion_addin/AIEF_CAD_Bridge/AIEF_CAD_Bridge.py"
                ).read_text(encoding="utf-8")


def _ops_sent(fake) -> list[str]:
    return [c.op for c in fake.sent]


class FailingFusion(FakeFusion):
    """Answers every modelling op OK but observes an empty model, so
    verification always fails - the shape of a genuinely failed attempt."""

    def _exec(self, cmd):
        if cmd.op == "observe":
            return {"document": {"name": "Untitled", "persisted_name": None,
                                 "saved": False, "units": "mm"},
                    "parameters": [], "bodies": [], "sketches": [],
                    "planes": [], "features": []}
        if cmd.op == "discard_document":
            self.doc = {}
            return {"document": {"name": cmd.args.get("name"),
                                 "discarded": True}}
        if cmd.op == "revert_document":
            return {"document": {"name": cmd.args.get("name"),
                                 "reverted": True}}
        return super()._exec(cmd)


def test_failed_run_discards_and_never_saves(tmp_path):
    fake = FailingFusion()
    orch = Orchestrator(bridge=fake, runs_dir=tmp_path, max_attempts=1,
                        save_on_pass=True)
    record = orch.run(SEWCP_PACKAGE)
    ops = _ops_sent(fake)
    assert record.verdict != "PASS"
    assert "save_document" not in ops, \
        "a failed attempt must never persist a document"
    assert "discard_document" in ops, \
        "a failed attempt must dispose of its document"
    assert ops.index("discard_document") > ops.index("observe")


def test_repeated_failures_accumulate_nothing(tmp_path):
    fake = FailingFusion()
    orch = Orchestrator(bridge=fake, runs_dir=tmp_path, max_attempts=1,
                        save_on_pass=True)
    for _ in range(3):
        orch.run(SEWCP_PACKAGE)
    ops = _ops_sent(fake)
    assert ops.count("save_document") == 0
    assert ops.count("discard_document") == 3


class SavedBaselineFusion(FailingFusion):
    """The failing attempt runs inside an adopted, already-saved design:
    discard must refuse and the disposition must fall through to revert."""

    def _exec(self, cmd):
        if cmd.op == "discard_document":
            raise RuntimeError(
                "discard_document: %r is persisted; a saved design is "
                "never discarded by recovery - use revert_document"
                % cmd.args.get("name"))
        return super()._exec(cmd)


def test_adopted_saved_document_is_reverted_not_discarded(tmp_path):
    fake = SavedBaselineFusion()
    orch = Orchestrator(bridge=fake, runs_dir=tmp_path, max_attempts=1,
                        save_on_pass=True)
    record = orch.run(SEWCP_PACKAGE)
    ops = _ops_sent(fake)
    assert "revert_document" in ops
    assert "save_document" not in ops
    assert not any("neither discard nor revert" in e
                   for e in record.escalations)


def test_passing_run_saves_exactly_once(tmp_path):
    fake = FakeFusion()
    orch = Orchestrator(bridge=fake, runs_dir=tmp_path, max_attempts=1,
                        save_on_pass=True)
    record = orch.run(SEWCP_PACKAGE)
    assert record.verdict == "PASS"
    ops = _ops_sent(fake)
    assert ops.count("save_document") == 1
    assert "discard_document" not in ops
    assert ops.index("save_document") > ops.index("observe"), \
        "persistence must follow verification, never precede it"


# -- assembly runner --------------------------------------------------------

def _assembly_package(tmp_path) -> Path:
    body = {"package_id": "T-ASM-LC", "document": "T_ASM_DOC",
            "units": "mm", "authority": ["test"],
            "occurrences": [{"occurrence_id": "A", "design": "D1",
                             "translate_mm": [0, 0, 0],
                             "provenance": "test"}]}
    p = tmp_path / "asm.json"
    p.write_text(json.dumps(body), encoding="utf-8")
    return p


class FakeAssemblyBridge:
    def __init__(self, observed_occurrences):
        self.observed = observed_occurrences
        self.sent = []

    def available(self, max_age_s: float = 15.0) -> bool:
        return True

    def send(self, command, reuse=True):
        self.sent.append(command)
        op = command.op
        if op == "observe_assembly":
            observed = {"document": {"persisted_name": "T_ASM_DOC",
                                     "saved": False},
                        "occurrences": self.observed}
        elif op == "discard_document":
            observed = {"document": {"name": command.args.get("name"),
                                     "discarded": True}}
        else:
            observed = {"ok": True}
        raw = {"protocol": PROTOCOL_VERSION, "command_id": command.command_id,
               "status": "OK", "executed": True, "observed": observed,
               "error": None, "fusion": {"version": "FAKE", "document": "x"},
               "started_at": 0.0, "finished_at": 0.01}
        return decode_observation(json.dumps(raw))


def test_failed_assembly_attempt_discards_and_never_saves(tmp_path):
    pkg = load_assembly_package(_assembly_package(tmp_path))
    bridge = FakeAssemblyBridge(observed_occurrences=[])  # missing occurrence
    runner = AssemblyRunner(bridge=bridge, runs_dir=tmp_path / "runs")
    record = runner.run(pkg, save_on_pass=True)
    ops = [c.op for c in bridge.sent]
    assert record["verdict"] == "FAIL"
    assert "save_document" not in ops
    assert "discard_document" in ops


def test_passing_assembly_saves(tmp_path):
    pkg = load_assembly_package(_assembly_package(tmp_path))
    bridge = FakeAssemblyBridge(observed_occurrences=[
        {"name": "D1:1", "component": "D1", "source_design": "D1",
         "source_version": 1, "grounded": True,
         "translate_mm": [0.0, 0.0, 0.0], "rotate_z_deg": 0.0,
         "z_axis_scale": 1.0}])
    runner = AssemblyRunner(bridge=bridge, runs_dir=tmp_path / "runs")
    record = runner.run(pkg, save_on_pass=True)
    ops = [c.op for c in bridge.sent]
    assert record["verdict"] == "PASS"
    assert ops.count("save_document") == 1
    assert "discard_document" not in ops


# -- structural contracts on the deployed add-in source ---------------------

def _function_source(module_source: str, name: str) -> str:
    tree = ast.parse(module_source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(module_source, node)
    raise AssertionError(f"{name} not found")


def test_setup_time_identity_binding_cannot_first_save():
    src = _function_source(EXT_SOURCE, "op_rename_component")
    assert "_first_save" not in src and "saveAs" not in src, \
        "rename_component persisting a document is the blank-shell defect"
    assert "intended_name" in src


def test_only_the_verified_save_path_may_first_save():
    callers = []
    tree = ast.parse(EXT_SOURCE)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            src = ast.get_source_segment(EXT_SOURCE, node)
            if "_first_save(" in src and node.name != "_first_save":
                callers.append(node.name)
    assert callers == ["op_save_document"], callers


def test_discard_refuses_persisted_documents():
    src = _function_source(EXT_SOURCE, "op_discard_document")
    assert "isSaved" in src and "RuntimeError" in src and \
        "revert_document" in src


def test_delete_guard_protects_authoritative_designs():
    src = _function_source(EXT_SOURCE, "op_delete_data_file")
    assert "protected" in src
    assert "_find_document" in src, "an open document must refuse deletion"


def test_shell_reports_intended_identity_without_claiming_persistence():
    assert "_intended_doc_name" in SHELL_SOURCE
    src = _function_source(SHELL_SOURCE, "_persisted_doc_name")
    assert "_intended_doc_name" in src
