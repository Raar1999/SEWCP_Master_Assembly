"""The Fusion boundary, the verifiers, the verdict and the bounded repair loop.

`FakeFusion` is a substitute **only at the adapter boundary** - it answers a
`Command` with an `Observation`, exactly as the add-in does, and every layer
above it is the real one. Nothing here is evidence that the real add-in works:
that is what the end-to-end run against Fusion is for, and this file makes no
claim about it.

The transport itself is tested against the real `FileQueueBridge` with the
add-in's side of the exchange simulated by writing observation files, which is
the only part a unit test can stand in for.
"""

from __future__ import annotations

import json
import math
import threading
import time
from pathlib import Path

import pytest

from aief_cad import PROTOCOL_VERSION, REPO_ROOT
from aief_cad.agents import select_agents
from aief_cad.bridge.client import BridgeNotRunning, BridgeTimeout, FileQueueBridge
from aief_cad.bridge.protocol import Command, ProtocolError, decode_observation
from aief_cad.loop import NoProgress, diagnose, propose_repair, sequence_digest
from aief_cad.observe import ObservationError, ObservedModel, merge_observations, parse
from aief_cad.ops import Op, compile_solution
from aief_cad.orchestrator import Orchestrator, OrchestratorError
from aief_cad.requirements import load_package
from aief_cad.solution import resolve
from aief_cad.verify import run_all

SEWCP_PACKAGE = (
    REPO_ROOT / "implementation" / "01_SEWCP-200_Cooling_Plate" / "requirements"
    / "SEWCP-200_base_and_datums.requirements.json"
)


def build_solution(package_path=SEWCP_PACKAGE, solution_id="S1"):
    pkg = load_package(package_path)
    return pkg, resolve(pkg, [a.contribute(pkg) for a in select_agents(pkg)], solution_id)


# --------------------------------------------------------------------------
# The substitute, at the boundary and nowhere deeper
# --------------------------------------------------------------------------

class FakeFusion:
    """An in-memory modeller that answers the same envelopes the add-in does."""

    def __init__(self, defects: dict | None = None):
        self.defects = defects or {}
        self.doc = {}
        self.component = {}
        self.parameters: dict[str, dict] = {}
        self.sketches: dict[str, dict] = {}
        self.planes: dict[str, dict] = {}
        self.bodies: dict[str, dict] = {}
        self.sent: list[Command] = []
        self.repairs = 0

    def available(self, max_age_s: float = 15.0) -> bool:
        return True

    # -- helpers ---------------------------------------------------------
    def _value(self, expression: str) -> float:
        from aief_cad.expr import evaluate
        env = {n: p["value"] for n, p in self.parameters.items()}
        return evaluate(expression, env)

    def send(self, command: Command, reuse: bool = True):
        self.sent.append(command)
        if (command.op_id or "").startswith("RP"):
            self.repairs += 1
        try:
            observed = self._exec(command)
            status, executed, error = "OK", True, None
        except _Reject as exc:
            observed, status, executed = {}, "REJECTED", False
            error = {"kind": "bad_argument", "message": str(exc)}
        except Exception as exc:  # pragma: no cover - defensive
            observed, status, executed = {}, "ERROR", False
            error = {"kind": type(exc).__name__, "message": str(exc)}
        raw = {
            "protocol": PROTOCOL_VERSION,
            "command_id": command.command_id,
            "status": status,
            "executed": executed,
            "observed": observed,
            "error": error,
            "fusion": {"version": "FAKE", "document": self.doc.get("name")},
            "started_at": 0.0,
            "finished_at": 0.01,
        }
        return decode_observation(json.dumps(raw))

    def _exec(self, cmd: Command) -> dict:
        op, a = cmd.op, cmd.args
        if op == "ping":
            return {"addin": "FakeFusion", "protocol": PROTOCOL_VERSION}
        if op == "new_document":
            self.doc = {"name": a["name"], "units": self.defects.get("units", a.get("units", "mm"))}
            return {"document": dict(self.doc)}
        if op == "rename_component":
            self.component = {"name": a["name"]}
            return {"component": dict(self.component)}
        if op == "set_parameters":
            skip = self.defects.get("drop_parameters", set())
            flatten = self.defects.get("flatten_parameters", set())
            if self.repairs:  # a repair heals the injected defect
                skip, flatten = set(), set()
            from aief_cad.expr import resolve_all

            class _P:
                def __init__(self, n, e):
                    self.name, self.expression = n, e

            resolved = resolve_all([_P(p["name"], p["expression"]) for p in a["parameters"]])
            for p in a["parameters"]:
                if p["name"] in skip:
                    continue
                expression = p["expression"]
                if p["name"] in flatten:
                    expression = repr(round(resolved[p["name"]], 6))
                self.parameters[p["name"]] = {
                    "name": p["name"], "unit": p["unit"], "expression": expression,
                    "value": resolved[p["name"]],
                }
            return {"parameters_applied": len(self.parameters)}
        if op == "create_sketch":
            self.sketches[a["name"]] = {
                "name": a["name"], "plane": a["plane"], "fully_constrained": True,
                "curves": 0, "construction_curves": 0, "profiles": 0,
            }
            return {"sketch": dict(self.sketches[a["name"]])}
        if op == "sketch_circle":
            sk = self.sketches.get(a["sketch"])
            if sk is None:
                raise _Reject(f"sketch {a['sketch']!r} not found")
            sk["curves"] += 1
            sk["profiles"] = 1
            sk["diameter"] = self._value(a["diameter"])
            return {"sketch": dict(sk)}
        if op == "sketch_construction":
            sk = self.sketches.get(a["sketch"])
            if sk is None:
                raise _Reject(f"sketch {a['sketch']!r} not found")
            n = len(a.get("circles", [])) + len(a.get("rays", []))
            if self.defects.get("short_construction") and not self.repairs:
                n -= 1
            sk["curves"] += n
            sk["construction_curves"] += n
            return {"sketch": dict(sk)}
        if op == "offset_plane":
            if self.defects.get("skip_plane") and not self.repairs:
                return {"plane": None}
            self.planes[a["name"]] = {
                "name": a["name"], "base": a.get("base", "XY"),
                "offset_mm": self._value(a["offset"]),
            }
            return {"plane": dict(self.planes[a["name"]])}
        if op == "extrude":
            sk = self.sketches.get(a["sketch"])
            if sk is None or not sk.get("profiles"):
                raise _Reject(f"sketch {a['sketch']!r} yields no profile")
            d = sk["diameter"]
            h = self._value(a["distance"])
            name = a.get("body_name", "Body1")
            self.bodies[name] = {
                "name": name,
                "volume_mm3": math.pi * (d / 2) ** 2 * h,
                "area_mm2": 2 * math.pi * (d / 2) ** 2 + math.pi * d * h,
                "bbox_min": [-d / 2, -d / 2, 0.0],
                "bbox_max": [d / 2, d / 2, h],
                "material": None,
            }
            return {"extrude": {"bodies": 1, "body_name": name}}
        if op == "observe":
            return {
                "document": dict(self.doc),
                "component": dict(self.component),
                "parameters": list(self.parameters.values()),
                "bodies": list(self.bodies.values()),
                "sketches": list(self.sketches.values()),
                "planes": list(self.planes.values()),
                "features": [],
            }
        raise _Reject(f"unknown op {op!r}")


class _Reject(Exception):
    pass


# --------------------------------------------------------------------------
# H. Transport behaviour, against the real FileQueueBridge
# --------------------------------------------------------------------------

def make_command(cid="C-1", op="ping", args=None, timeout=2.0):
    return Command(
        command_id=cid, op=op, args=args or {}, issued_by="test", session="S",
        solution_id="S1", model_target={}, idempotency_key=f"key-{cid}",
        timeout_s=timeout,
    )


def observation_body(cid, status="OK", executed=True, observed=None, error=None):
    return json.dumps({
        "protocol": PROTOCOL_VERSION, "command_id": cid, "status": status,
        "executed": executed, "observed": observed or {"document": {"units": "mm"}},
        "error": error, "fusion": {"version": "test"},
    }).encode("utf-8")


@pytest.fixture
def bridge(tmp_path):
    b = FileQueueBridge(tmp_path / "queue", tmp_path / "obs", tmp_path / "state", poll_s=0.02)
    return b


def beat(bridge: FileQueueBridge):
    bridge.heartbeat_path().write_text(json.dumps({"alive_at": time.time()}), encoding="utf-8")


def _answer(bridge: FileQueueBridge, command_id: str, payload: bytes):
    """Stand in for the add-in: answer once the command file appears.

    The answer cannot be pre-written, because `send` clears any stale
    observation for the id it is about to dispatch - which is itself the
    behaviour that stops a previous run's answer being read as this run's.
    """
    def responder():
        for _ in range(400):
            if bridge.command_path(command_id).is_file():
                bridge.observation_path(command_id).write_bytes(payload)
                return
            time.sleep(0.01)

    t = threading.Thread(target=responder, daemon=True)
    t.start()
    return t


class TestTransport:
    def test_no_heartbeat_means_nothing_is_dispatched(self, bridge):
        with pytest.raises(BridgeNotRunning, match="not reporting a live heartbeat"):
            bridge.send(make_command())
        assert list(bridge.queue_dir.glob("*.cmd.json")) == []

    def test_a_stale_heartbeat_counts_as_absent(self, bridge):
        beat(bridge)
        import os
        old = time.time() - 3600
        os.utime(bridge.heartbeat_path(), (old, old))
        assert bridge.available() is False

    def test_a_command_is_written_and_the_observation_is_read_back(self, bridge):
        beat(bridge)
        cmd = make_command("C-7")

        def responder():
            for _ in range(200):
                if bridge.command_path("C-7").is_file():
                    bridge.observation_path("C-7").write_bytes(observation_body("C-7"))
                    return
                time.sleep(0.01)

        t = threading.Thread(target=responder, daemon=True)
        t.start()
        obs = bridge.send(cmd)
        t.join(timeout=3)
        assert obs.ok
        payload = json.loads(bridge.command_path("C-7").read_text(encoding="utf-8"))
        assert payload["protocol"] == PROTOCOL_VERSION
        assert payload["op"] == "ping"

    def test_a_silent_bridge_times_out_and_does_not_retry(self, bridge):
        beat(bridge)
        with pytest.raises(BridgeTimeout, match="not retried automatically"):
            bridge.send(make_command("C-8", timeout=1.0))
        assert bridge.command_path("C-8").is_file()

    def test_an_identical_effect_is_answered_from_the_record(self, bridge):
        beat(bridge)
        cmd = make_command("C-9", op="create_sketch", args={"name": "S", "plane": "XY"})
        _answer(bridge, "C-9", observation_body("C-9"))
        first = bridge.send(cmd)
        assert first.ok
        again = Command(**{**cmd.__dict__, "command_id": "C-10"})
        second = bridge.send(again)
        assert second.command_id == "C-9"
        assert not bridge.command_path("C-10").exists()

    def test_an_observation_answering_another_command_is_refused(self, bridge):
        beat(bridge)
        _answer(bridge, "C-11", observation_body("C-99"))
        with pytest.raises(ProtocolError, match="answers"):
            bridge.send(make_command("C-11", timeout=2.0))


class TestProtocol:
    def test_a_mismatched_protocol_is_refused(self):
        with pytest.raises(ProtocolError, match="announces protocol"):
            decode_observation(json.dumps({"protocol": "other/9", "command_id": "C",
                                           "status": "OK", "executed": True}))

    def test_ok_with_executed_false_is_refused(self):
        with pytest.raises(ProtocolError, match="disagree about whether"):
            decode_observation(json.dumps({"protocol": PROTOCOL_VERSION, "command_id": "C",
                                           "status": "OK", "executed": False}))

    def test_a_failure_with_no_stated_cause_is_refused(self):
        with pytest.raises(ProtocolError, match="no stated cause"):
            decode_observation(json.dumps({"protocol": PROTOCOL_VERSION, "command_id": "C",
                                           "status": "ERROR", "executed": False}))

    def test_unparseable_json_is_a_protocol_fault_not_an_empty_model(self):
        with pytest.raises(ProtocolError, match="not JSON"):
            decode_observation(b"{not json")

    def test_rejected_is_distinguishable_from_error(self):
        r = decode_observation(json.dumps({
            "protocol": PROTOCOL_VERSION, "command_id": "C", "status": "REJECTED",
            "executed": False, "error": {"kind": "unknown_operation", "message": "x"}}))
        assert r.rejected and not r.ok


# --------------------------------------------------------------------------
# I. Observation parsing
# --------------------------------------------------------------------------

class TestObservationParsing:
    def test_a_non_object_payload_is_refused(self):
        with pytest.raises(ObservationError):
            parse(["not", "an", "object"])  # type: ignore[arg-type]

    def test_a_string_where_a_list_belongs_is_refused(self):
        with pytest.raises(ObservationError, match="not a list"):
            parse({"bodies": "CP_BODY"})

    def test_absence_is_absence_not_zero(self):
        m = parse({"bodies": [{"name": "B"}]})
        assert m.body("B").volume_mm3 is None
        assert m.body("B").dz is None

    def test_the_last_complete_payload_wins(self):
        class O:
            def __init__(self, observed):
                self.observed, self.command_id = observed, "C"
        merged = merge_observations([
            O({"sketches": [{"name": "S1"}]}),
            O({"parameters": [{"name": "a", "value": 1.0}], "bodies": [{"name": "B"}]}),
        ])
        assert merged.parameter("a").value == 1.0

    def test_no_payload_at_all_yields_an_empty_model(self):
        assert merge_observations([]).is_empty


class TestComponentNameObservation:
    """`component.name` is the persisted design name, not Fusion's versioned
    display string - ruled by the owner on ACC-NAME (Option 1, 2026-08-11).
    The display string is kept as evidence, never as the observation."""

    def test_the_data_file_name_is_authoritative(self):
        m = parse({"component": {"name": "PLATE v1", "persisted_name": "PLATE"}})
        assert m.component["name"] == "PLATE"
        assert m.component["display_name"] == "PLATE v1"
        assert m.component["name_source"] == "data_file"

    def test_only_the_data_file_name_can_keep_a_version_looking_name(self):
        # A design legitimately named "Bracket v2" is indistinguishable from
        # version 2 of "Bracket" by its display string alone. With the
        # persisted name present, it survives intact - which is why the
        # fallback below is a fallback and not the design.
        m = parse({"component": {"name": "Bracket v2 v5",
                                 "persisted_name": "Bracket v2"}})
        assert m.component["name"] == "Bracket v2"
        assert m.component["name_source"] == "data_file"

    def test_the_fallback_strips_exactly_the_fusion_suffix(self):
        for n in (1, 2, 3, 27):
            m = parse({"component": {"name": f"SEWCP-200_COOLING_PLATE v{n}"}})
            assert m.component["name"] == "SEWCP-200_COOLING_PLATE"
            assert m.component["display_name"] == f"SEWCP-200_COOLING_PLATE v{n}"
            assert m.component["name_source"] == "display_normalized"

    def test_an_unversioned_name_passes_through_unchanged(self):
        m = parse({"component": {"name": "SEWCP-200_COOLING_PLATE"}})
        assert m.component["name"] == "SEWCP-200_COOLING_PLATE"
        assert m.component["name_source"] == "display"
        assert "display_name" not in m.component

    def test_numbers_in_legitimate_names_are_not_versions(self):
        for name in ("SEWCP-200_COOLING_PLATE", "Bracket 2024", "Adapter-3"):
            assert parse({"component": {"name": name}}).component["name"] == name

    def test_version_lookalikes_are_not_stripped(self):
        # Everything the strict pattern must NOT match: capital V, dotted
        # version, no digits, no space, trailing text, suffix mid-string.
        for name in ("Bracket V2", "Housing v2.1", "Plate v", "Platev2",
                     "Plate v2x", "My Plate v1 final", "Plate rev3"):
            m = parse({"component": {"name": name}})
            assert m.component["name"] == name, name
            assert m.component["name_source"] == "display", name

    def test_a_missing_or_empty_data_file_name_falls_back(self):
        for comp in ({"name": "PLATE v1"},
                     {"name": "PLATE v1", "persisted_name": None},
                     {"name": "PLATE v1", "persisted_name": ""}):
            m = parse({"component": dict(comp)})
            assert m.component["name"] == "PLATE"
            assert m.component["name_source"] == "display_normalized"

    def test_a_component_that_is_not_an_object_is_refused(self):
        with pytest.raises(ObservationError, match="component"):
            parse({"component": ["PLATE"]})

    def test_a_non_string_name_is_left_alone(self):
        assert parse({"component": {"name": 7}}).component["name"] == 7

    def test_an_absent_component_stays_absent(self):
        assert parse({}).component == {}
        assert parse({"component": {}}).component == {}

    def test_normalization_is_idempotent_so_replay_reproduces(self):
        fallback = parse({"component": {"name": "PLATE v1"}})
        assert parse(fallback.as_dict()).component == fallback.component
        authoritative = parse({"component": {"name": "PLATE v1",
                                             "persisted_name": "PLATE"}})
        assert parse(authoritative.as_dict()).component == authoritative.component
        plain = parse({"component": {"name": "PLATE"}})
        assert parse(plain.as_dict()).component == plain.component


# --------------------------------------------------------------------------
# J/K/L/M. Verifiers and verdict
# --------------------------------------------------------------------------

class TestVerification:
    def test_an_empty_model_fails_every_verifier(self):
        _pkg, sol = build_solution()
        v = run_all(sol, ObservedModel())
        assert not v.passed
        assert {r.verifier for r in v.reports} == {"geometry", "interface", "constraint"}
        assert all(not r.passed for r in v.reports)

    def test_a_correct_model_passes(self):
        _pkg, sol = build_solution()
        fake = FakeFusion()
        obs = [fake.send(_cmd(op)) for op in compile_solution(sol)]
        v = run_all(sol, merge_observations(obs))
        assert v.passed, [f.as_dict() for f in v.failures]
        assert v.check_count >= 24

    def test_an_unresolvable_subject_fails_rather_than_skips(self):
        _pkg, sol = build_solution()
        model = parse({"document": {"units": "mm"}})
        v = run_all(sol, model)
        ids = {f.id for f in v.failures}
        assert "ACC-BODY-DZ" in ids
        detail = next(f for f in v.failures if f.id == "ACC-BODY-DZ").detail
        assert "has not passed" in detail

    def test_a_wrong_dimension_is_caught_by_geometry(self):
        _pkg, sol = build_solution()
        fake = FakeFusion()
        for op in compile_solution(sol):
            fake.send(_cmd(op))
        fake.bodies["CP_BODY"]["bbox_max"][2] = 19.0
        v = run_all(sol, parse(fake._exec(_cmd(Op("O", "observe", {})))))
        assert not v.passed
        assert any(f.id in ("ACC-BODY-DZ", "GEO-EXTENT-mech.CP-D01.extrude")
                   for f in v.failures)

    def test_a_literal_that_agrees_today_still_fails(self):
        """The value matches; the derivation is gone. That is the defect."""
        _pkg, sol = build_solution()
        fake = FakeFusion(defects={"flatten_parameters": {"lid_check", "rf_tap_ang_1"}})
        obs = [fake.send(_cmd(op)) for op in compile_solution(sol)]
        v = run_all(sol, merge_observations(obs))
        assert not v.passed
        assert {"ACC-LID-DERIVED", "ACC-RFTAP-DERIVED", "CON-PARAM-DERIVED"} & {
            f.id for f in v.failures
        }
        assert v.reports[2].verifier == "constraint"

    def test_the_verifiers_never_read_the_execution_report(self):
        """`executed` is the executing party's account of its own work.

        Checked against the parsed syntax tree rather than the text, so the
        prose that explains the rule does not trip the check that enforces it.
        """
        import ast
        import aief_cad.verify as V

        for module in (V, V.geometry, V.interface, V.constraint):
            tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
            reads = [
                n for n in ast.walk(tree)
                if isinstance(n, ast.Attribute) and n.attr in ("executed", "ok", "status")
            ]
            assert not reads, (
                f"{module.__name__} reads the execution report at line(s) "
                f"{[n.lineno for n in reads]}"
            )

    def test_the_verdict_is_pass_only_if_every_verifier_passes(self):
        _pkg, sol = build_solution()
        fake = FakeFusion(defects={"skip_plane": True})
        obs = [fake.send(_cmd(op)) for op in compile_solution(sol)]
        v = run_all(sol, merge_observations(obs))
        assert v.verdict == "FAIL"
        assert not any(r.verifier == "interface" and r.passed for r in v.reports)


def _cmd(op: Op) -> Command:
    return Command(
        command_id=f"T-{op.op_id}", op=op.op, args=op.args, issued_by="test",
        session="S", solution_id="S1", model_target={},
        idempotency_key=op.idempotency_key(),
    )


# --------------------------------------------------------------------------
# N/Q. Diagnosis and the bounded repair loop
# --------------------------------------------------------------------------

class TestRepairLoop:
    def test_a_diagnosis_names_five_things(self):
        _pkg, sol = build_solution()
        fake = FakeFusion(defects={"skip_plane": True})
        obs = [fake.send(_cmd(op)) for op in compile_solution(sol)]
        v = run_all(sol, merge_observations(obs))
        for d in diagnose(v, sol):
            assert d.failed_requirement and d.evidence and d.responsible_area
            assert d.responsible_agent and d.likely_cause and d.proposed_correction

    def test_an_identical_repair_is_refused_as_no_progress(self):
        """The same repair, proposed twice against an unchanged failure."""
        _pkg, sol = build_solution()
        v = run_all(sol, ObservedModel())
        first = propose_repair(v, sol, compile_solution(sol), 2)
        assert first.repairable
        with pytest.raises(NoProgress, match="cannot produce a different model"):
            propose_repair(v, sol, first.ops, 3)

    def test_a_repair_targets_only_the_failing_kinds(self):
        _pkg, sol = build_solution()
        fake = FakeFusion(defects={"skip_plane": True})
        obs = [fake.send(_cmd(op)) for op in compile_solution(sol)]
        v = run_all(sol, merge_observations(obs))
        plan = propose_repair(v, sol, compile_solution(sol), 2)
        assert plan.repairable
        assert {o.op for o in plan.ops} == {"offset_plane", "observe"}

    def test_an_unclassifiable_failure_is_escalated_not_retried(self):
        _pkg, sol = build_solution()
        fake = FakeFusion(defects={"units": "in"})
        obs = [fake.send(_cmd(op)) for op in compile_solution(sol)]
        v = run_all(sol, merge_observations(obs))
        plan = propose_repair(v, sol, compile_solution(sol), 2)
        unit_diag = [d for d in plan.diagnoses if d.finding_id in ("ACC-UNITS", "CON-UNITS")]
        assert unit_diag and not any(d.repairable for d in unit_diag)

    def test_sequence_digest_ignores_identifiers_and_tracks_effects(self):
        a = [Op("OP-0001", "create_sketch", {"name": "S", "plane": "XY"})]
        b = [Op("RP2-OP-0001", "create_sketch", {"name": "S", "plane": "XY"})]
        c = [Op("OP-0001", "create_sketch", {"name": "T", "plane": "XY"})]
        assert sequence_digest(a) == sequence_digest(b)
        assert sequence_digest(a) != sequence_digest(c)


# --------------------------------------------------------------------------
# End to end through the orchestrator, with the boundary substituted
# --------------------------------------------------------------------------

class TestOrchestration:
    def test_a_clean_run_passes_in_one_attempt(self, tmp_path):
        orch = Orchestrator(bridge=FakeFusion(), runs_dir=tmp_path, session="T")
        rec = orch.run(SEWCP_PACKAGE, run_id="RUN-TEST-1")
        assert rec.verdict == "PASS"
        assert len(rec.attempts) == 1
        assert rec.attempts[0]["executed"] == rec.attempts[0]["dispatched"] == 10
        assert (tmp_path / "RUN-TEST-1" / "run.json").is_file()

    def test_the_run_record_is_reproducible_and_pins_its_inputs(self, tmp_path):
        orch = Orchestrator(bridge=FakeFusion(), runs_dir=tmp_path, session="T")
        rec = orch.run(SEWCP_PACKAGE, run_id="RUN-TEST-2")
        body = json.loads((tmp_path / "RUN-TEST-2" / "run.json").read_text(encoding="utf-8"))
        assert body["package_digest"].startswith("sha256:")
        assert body["solution_digest"].startswith("sha256:")
        assert body["record_digest"].startswith("sha256:")
        assert body["agents"][0] == "model-setup"

    def test_a_failure_is_diagnosed_repaired_and_passes_on_the_second_attempt(self, tmp_path):
        """The FAIL branch, end to end: FAIL -> diagnose -> repair -> PASS."""
        fake = FakeFusion(defects={"skip_plane": True})
        orch = Orchestrator(bridge=fake, runs_dir=tmp_path, session="T", max_attempts=3)
        rec = orch.run(SEWCP_PACKAGE, run_id="RUN-TEST-3")
        assert len(rec.attempts) == 2
        assert rec.attempts[0]["verdict"]["verdict"] == "FAIL"
        assert rec.attempts[0]["repair"]["diagnoses"]
        assert rec.verdict == "PASS"

    def test_the_attempt_limit_is_honoured_and_does_not_degrade_to_a_pass(self, tmp_path):
        class Stuck(FakeFusion):
            def _exec(self, cmd):
                out = super()._exec(cmd)
                self.planes.clear()  # the repair never takes
                return out

        orch = Orchestrator(bridge=Stuck(defects={"skip_plane": True}),
                            runs_dir=tmp_path, session="T", max_attempts=2)
        rec = orch.run(SEWCP_PACKAGE, run_id="RUN-TEST-4")
        assert rec.verdict == "FAIL"
        assert len(rec.attempts) == 2
        assert any("attempt limit" in e for e in rec.escalations)

    def test_execution_stops_at_the_first_operation_that_did_not_run(self, tmp_path):
        class Broken(FakeFusion):
            def _exec(self, cmd):
                if cmd.op == "extrude":
                    raise _Reject("no profile")
                return super()._exec(cmd)

        orch = Orchestrator(bridge=Broken(), runs_dir=tmp_path, session="T", max_attempts=1)
        rec = orch.run(SEWCP_PACKAGE, run_id="RUN-TEST-5")
        assert rec.verdict == "FAIL"
        assert "did not execute" in rec.attempts[0]["execution_halt"]
        assert rec.attempts[0]["dispatched"] < 10

    def test_a_requirement_no_agent_owns_halts_before_any_dispatch(self, tmp_path):
        body = json.loads(SEWCP_PACKAGE.read_text(encoding="utf-8"))
        body["requirements"].append(
            {"id": "X-1", "kind": "electrical", "statement": "conduct", "source": "f"}
        )
        p = tmp_path / "orphan.requirements.json"
        p.write_text(json.dumps(body), encoding="utf-8")
        # The parameter master reference is relative to the package location.
        body["parameters_from"] = str(
            (SEWCP_PACKAGE.parent / body["parameters_from"]).resolve()
        )
        p.write_text(json.dumps(body), encoding="utf-8")
        fake = FakeFusion()
        orch = Orchestrator(bridge=fake, runs_dir=tmp_path, session="T")
        with pytest.raises(OrchestratorError, match="no registered agent"):
            orch.run(p)
        assert fake.sent == []
