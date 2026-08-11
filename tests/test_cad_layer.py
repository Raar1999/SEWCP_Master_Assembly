"""Requirement ingestion, routing, scope, solution resolution and command validation.

Covers the layers above the Fusion boundary. Nothing here mocks anything: every
object under test is the real one. The Fusion boundary itself is exercised in
`test_cad_bridge.py`, which is the only place a substitute appears.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from aief_cad import REPO_ROOT
from aief_cad.agents import (
    AgentError,
    ManufacturingAgent,
    MechanicalDesignAgent,
    ModelSetupAgent,
    ThermalInterfaceAgent,
    select_agents,
    unroutable_kinds,
)
from aief_cad.expr import ExpressionError, evaluate, resolve_all
from aief_cad.ops import Op, OpError, compile_solution, validate_sequence
from aief_cad.requirements import Parameter, RequirementError, load_package
from aief_cad.solution import (
    DesignConflict,
    DesignContribution,
    FeatureSpec,
    SolutionError,
    resolve,
)

SEWCP_PACKAGE = (
    REPO_ROOT
    / "implementation"
    / "01_SEWCP-200_Cooling_Plate"
    / "requirements"
    / "SEWCP-200_base_and_datums.requirements.json"
)


def write_package(tmp_path: Path, **overrides) -> Path:
    body = {
        "package_id": "TEST-001",
        "component": "TEST_PART",
        "authority": ["test fixture"],
        "requirements": [
            {
                "id": "R-1",
                "kind": "geometry",
                "statement": "a disc",
                "source": "fixture",
                "value": {
                    "form": "disc",
                    "plane": "XY",
                    "sketch": "SK1",
                    "diameter": "d_out",
                    "thickness": "t",
                    "body": "BODY",
                },
            }
        ],
        "parameters": [
            {"name": "d_out", "expression": "50.0", "unit": "mm"},
            {"name": "t", "expression": "5.0", "unit": "mm"},
        ],
        "acceptance": [
            {"id": "A-1", "check": "geometry", "subject": "bodies.count", "expect": 1}
        ],
    }
    body.update(overrides)
    p = tmp_path / "pkg.requirements.json"
    p.write_text(json.dumps(body), encoding="utf-8")
    return p


# --------------------------------------------------------------------------
# A. Requirement ingestion
# --------------------------------------------------------------------------

class TestRequirementIngestion:
    def test_a_real_package_loads_and_is_digest_identified(self):
        pkg = load_package(SEWCP_PACKAGE)
        assert pkg.package_id == "SEWCP-200-REQ-001"
        assert pkg.digest.startswith("sha256:")
        assert len(pkg.parameters) == 105

    def test_the_digest_covers_the_referenced_parameter_master(self, tmp_path):
        """A reference that is pinned only by its path lets the master drift."""
        master = tmp_path / "m.csv"
        master.write_text("Name,Unit,Expression,Comment\na,mm,1.0,x\n", encoding="utf-8")
        p = write_package(
            tmp_path,
            parameters=[],
            parameters_from="m.csv",
            requirements=[{"id": "R", "kind": "geometry", "statement": "s", "source": "f"}],
            acceptance=[],
        )
        first = load_package(p).digest
        master.write_text("Name,Unit,Expression,Comment\na,mm,2.0,x\n", encoding="utf-8")
        assert load_package(p).digest != first

    def test_two_parameter_sources_are_refused(self, tmp_path):
        (tmp_path / "m.csv").write_text("Name,Unit,Expression\na,mm,1\n", encoding="utf-8")
        p = write_package(tmp_path, parameters_from="m.csv")
        with pytest.raises(RequirementError, match="second-master"):
            load_package(p)

    def test_a_bare_string_is_not_read_as_a_list(self, tmp_path):
        p = write_package(tmp_path, requirements="R-1")
        with pytest.raises(RequirementError, match="expected a list"):
            load_package(p)

    def test_an_unknown_kind_is_refused(self, tmp_path):
        p = write_package(
            tmp_path,
            requirements=[{"id": "R", "kind": "vibes", "statement": "s", "source": "f"}],
        )
        with pytest.raises(RequirementError, match="not one of"):
            load_package(p)

    def test_a_package_citing_no_authority_is_refused(self, tmp_path):
        p = write_package(tmp_path, authority=[])
        with pytest.raises(RequirementError, match="non-empty list of source citations"):
            load_package(p)

    def test_acceptance_citing_an_undeclared_parameter_is_refused(self, tmp_path):
        p = write_package(
            tmp_path,
            acceptance=[{"id": "A", "check": "parameter",
                         "subject": "parameter:nope.value", "expect": 1}],
        )
        with pytest.raises(RequirementError, match="does not declare"):
            load_package(p)


# --------------------------------------------------------------------------
# C. Agent routing - derived from stated kinds, never from the component
# --------------------------------------------------------------------------

class TestAgentRouting:
    def test_domains_are_derived_from_the_kinds_present(self, tmp_path):
        pkg = load_package(write_package(tmp_path))
        assert pkg.domains() == ("geometry",)
        assert [a.name for a in select_agents(pkg)] == [
            "model-setup", "mechanical.design-engineer"
        ]

    def test_a_thermal_requirement_summons_the_thermal_agent(self, tmp_path):
        p = write_package(
            tmp_path,
            requirements=[
                {"id": "T", "kind": "thermal", "statement": "cool it", "source": "f"}
            ],
            acceptance=[],
        )
        pkg = load_package(p)
        assert "thermal" in pkg.domains()
        assert any(a.domain == "thermal-interface" for a in select_agents(pkg))

    def test_no_thermal_requirement_summons_no_thermal_agent(self, tmp_path):
        pkg = load_package(write_package(tmp_path))
        assert not any(a.domain == "thermal-interface" for a in select_agents(pkg))

    def test_a_kind_no_agent_owns_is_reported(self, tmp_path):
        p = write_package(
            tmp_path,
            requirements=[
                {"id": "E", "kind": "electrical", "statement": "conduct", "source": "f"}
            ],
            acceptance=[],
        )
        assert unroutable_kinds(load_package(p)) == ("electrical",)

    def test_the_real_package_routes_to_four_agents(self):
        pkg = load_package(SEWCP_PACKAGE)
        assert [a.name for a in select_agents(pkg)] == [
            "model-setup",
            "mechanical.design-engineer",
            "mechanical.simulation-engineer",
            "mechanical.manufacturing-engineer",
        ]


# --------------------------------------------------------------------------
# D/O. Scope enforcement - an agent may not widen its own authority
# --------------------------------------------------------------------------

class TestScopeEnforcement:
    def test_a_contribution_outside_its_declared_scope_is_refused(self):
        bad = DesignContribution(
            agent="rogue",
            domain="mechanical",
            writes=("feature:mech.*",),
            features=(FeatureSpec(id="thermal.sneaky", kind="sketch"),),
        )
        with pytest.raises(SolutionError, match="may not widen its own scope"):
            bad.validate()

    def test_a_contribution_inside_its_scope_is_accepted(self):
        DesignContribution(
            agent="mech",
            domain="mechanical",
            writes=("feature:mech.*",),
            features=(FeatureSpec(id="mech.ok", kind="sketch"),),
        ).validate()

    def test_the_manufacturing_agent_produces_no_geometry(self):
        pkg = load_package(SEWCP_PACKAGE)
        c = ManufacturingAgent().contribute(pkg)
        assert c.features == ()
        assert c.constraints
        assert c.writes == ("constraint:con.*",)

    def test_every_real_agent_contribution_validates(self):
        pkg = load_package(SEWCP_PACKAGE)
        for agent in select_agents(pkg):
            agent.contribute(pkg).validate()


# --------------------------------------------------------------------------
# E/F. Contribution merge, conflict detection, solution validation
# --------------------------------------------------------------------------

class TestSolutionResolution:
    def test_two_agents_writing_the_same_key_differently_is_a_conflict(self, tmp_path):
        pkg = load_package(write_package(tmp_path))
        a = DesignContribution(
            agent="A", domain="x", writes=("feature:f.*",),
            features=(FeatureSpec(id="f.1", kind="sketch", params={"name": "S", "plane": "XY"}),),
        )
        b = DesignContribution(
            agent="B", domain="y", writes=("feature:f.*",),
            features=(FeatureSpec(id="f.1", kind="sketch", params={"name": "S", "plane": "XZ"}),),
        )
        with pytest.raises(DesignConflict, match="escalated, not merged"):
            resolve(pkg, [a, b], "S1")

    def test_identical_content_from_two_agents_is_not_a_conflict(self, tmp_path):
        pkg = load_package(write_package(tmp_path))
        f = FeatureSpec(id="f.1", kind="sketch", params={"name": "S", "plane": "XY"})
        a = DesignContribution(agent="A", domain="x", writes=("feature:f.*",), features=(f,))
        b = DesignContribution(agent="B", domain="y", writes=("feature:f.*",), features=(f,))
        assert resolve(pkg, [a, b], "S1").features == (f,)

    def test_a_feature_claiming_an_undeclared_requirement_is_refused(self, tmp_path):
        pkg = load_package(write_package(tmp_path))
        c = DesignContribution(
            agent="A", domain="x", writes=("feature:f.*",),
            features=(FeatureSpec(id="f.1", kind="sketch", satisfies=("R-999",)),),
        )
        with pytest.raises(SolutionError, match="does not declare"):
            resolve(pkg, [c], "S1")

    def test_a_feature_dependency_cycle_is_refused(self, tmp_path):
        pkg = load_package(write_package(tmp_path))
        c = DesignContribution(
            agent="A", domain="x", writes=("feature:f.*",),
            features=(
                FeatureSpec(id="f.1", kind="sketch", depends_on=("f.2",)),
                FeatureSpec(id="f.2", kind="sketch", depends_on=("f.1",)),
            ),
        )
        with pytest.raises(SolutionError, match="cyclic feature dependency"):
            resolve(pkg, [c], "S1")

    def test_no_contribution_is_an_error_not_an_empty_solution(self, tmp_path):
        pkg = load_package(write_package(tmp_path))
        with pytest.raises(SolutionError, match="nothing to resolve"):
            resolve(pkg, [], "S1")

    def test_provenance_names_the_producer_of_every_feature(self):
        pkg = load_package(SEWCP_PACKAGE)
        sol = resolve(pkg, [a.contribute(pkg) for a in select_agents(pkg)], "S1")
        for f in sol.features:
            assert sol.provenance[f"feature:{f.id}"]
        assert "mechanical.design-engineer" in sol.provenance["feature:mech.CP-D01.extrude"]
        assert "simulation-engineer" in sol.provenance["feature:thermal.CP-IF-4.plane"]

    def test_ordering_respects_declared_dependencies(self):
        pkg = load_package(SEWCP_PACKAGE)
        sol = resolve(pkg, [a.contribute(pkg) for a in select_agents(pkg)], "S1")
        order = [f.id for f in sol.ordered_features()]
        assert order.index("setup.parameters") < order.index("mech.CP-D01.circle")
        assert order.index("mech.CP-D01.extrude") < order.index("thermal.CP-IF-4.plane")


# --------------------------------------------------------------------------
# Expression resolution
# --------------------------------------------------------------------------

class TestExpressions:
    def test_the_real_parameter_set_resolves(self):
        pkg = load_package(SEWCP_PACKAGE)
        r = resolve_all(pkg.parameters)
        assert r["cp_thk"] == 20.0
        assert r["lid_check"] == pytest.approx(0.0, abs=1e-12)
        assert r["rf_tap_ang_1"] == pytest.approx(98.7267, abs=1e-3)
        assert r["rf_tap_ang_2"] == pytest.approx(111.2733, abs=1e-3)

    def test_a_cycle_names_its_members(self):
        with pytest.raises(ExpressionError, match="cyclic"):
            resolve_all([Parameter("a", "b", "mm", ""), Parameter("b", "a", "mm", "")])

    def test_an_undeclared_reference_is_refused(self):
        with pytest.raises(ExpressionError, match="undeclared"):
            resolve_all([Parameter("a", "missing + 1", "mm", "")])

    def test_executable_constructs_are_refused(self):
        for hostile in ("__import__('os')", "(lambda: 1)()", "[1,2][0]", "a if a else 0"):
            with pytest.raises(ExpressionError):
                evaluate(hostile, {"a": 1.0})

    def test_trigonometry_is_in_degrees(self):
        assert evaluate("sin(30)", {}) == pytest.approx(0.5)


# --------------------------------------------------------------------------
# G/P. Command validation - malformed operations never reach Fusion
# --------------------------------------------------------------------------

class TestOperationValidation:
    def test_an_unknown_operation_is_refused(self):
        with pytest.raises(OpError, match="unknown operation"):
            Op("OP-1", "teleport", {}).validate()

    def test_a_missing_required_argument_is_refused(self):
        with pytest.raises(OpError, match="missing required argument"):
            Op("OP-1", "extrude", {"sketch": "S1"}).validate()

    def test_an_unknown_argument_is_refused_not_dropped(self):
        with pytest.raises(OpError, match="unknown argument"):
            Op("OP-1", "create_sketch", {"name": "S", "plane": "XY", "colour": "red"}).validate()

    def test_a_numeric_dimension_is_refused_in_favour_of_a_parameter(self):
        with pytest.raises(OpError, match="unusable value"):
            Op("OP-1", "extrude", {"sketch": "S1", "distance": 20.0}).validate()

    def test_a_bad_enum_is_refused(self):
        with pytest.raises(OpError, match="direction"):
            Op("OP-1", "extrude", {"sketch": "S", "distance": "t", "direction": "sideways"}).validate()

    def test_duplicate_op_ids_are_refused(self):
        a = Op("OP-1", "ping", {})
        with pytest.raises(OpError, match="duplicate op_id"):
            validate_sequence([a, a])

    def test_idempotency_is_the_identity_of_the_effect_not_the_request(self):
        a = Op("OP-1", "create_sketch", {"name": "S", "plane": "XY"})
        b = Op("OP-9", "create_sketch", {"name": "S", "plane": "XY"})
        c = Op("OP-1", "create_sketch", {"name": "T", "plane": "XY"})
        assert a.idempotency_key() == b.idempotency_key()
        assert a.idempotency_key() != c.idempotency_key()


# --------------------------------------------------------------------------
# B. Decomposition
# --------------------------------------------------------------------------

class TestCompilation:
    def test_the_real_package_compiles_to_a_valid_sequence(self):
        pkg = load_package(SEWCP_PACKAGE)
        sol = resolve(pkg, [a.contribute(pkg) for a in select_agents(pkg)], "S1")
        ops = compile_solution(sol)
        assert [o.op for o in ops] == [
            "new_document", "set_parameters", "rename_component",
            "create_sketch", "sketch_circle", "extrude",
            "create_sketch", "sketch_construction", "offset_plane", "observe",
        ]
        assert len(ops[1].args["parameters"]) == 105

    def test_every_sequence_ends_by_observing(self):
        pkg = load_package(SEWCP_PACKAGE)
        sol = resolve(pkg, [a.contribute(pkg) for a in select_agents(pkg)], "S1")
        ops = compile_solution(sol)
        assert ops[-1].op == "observe"
        assert not ops[-1].mutating

    def test_a_feature_kind_with_no_compiler_halts_the_run(self, tmp_path):
        pkg = load_package(write_package(tmp_path))
        c = DesignContribution(
            agent="A", domain="x", writes=("feature:f.*",),
            features=(FeatureSpec(id="f.1", kind="loft"),),
        )
        with pytest.raises(OpError, match="no compiler for kind"):
            compile_solution(resolve(pkg, [c], "S1"))

    def test_an_unknown_form_is_an_escalation_not_a_guess(self, tmp_path):
        p = write_package(
            tmp_path,
            requirements=[{"id": "R", "kind": "geometry", "statement": "s", "source": "f",
                           "value": {"form": "torus"}}],
            acceptance=[],
        )
        with pytest.raises(AgentError, match="not one this agent reasons about"):
            MechanicalDesignAgent().contribute(load_package(p))

    def test_a_literal_dimension_in_a_form_is_refused(self, tmp_path):
        p = write_package(
            tmp_path,
            requirements=[{"id": "R", "kind": "geometry", "statement": "s", "source": "f",
                           "value": {"form": "disc", "diameter": 50.0, "thickness": "t"}}],
            acceptance=[],
        )
        with pytest.raises(AgentError, match="must name a parameter"):
            MechanicalDesignAgent().contribute(load_package(p))


# --------------------------------------------------------------------------
# The general-purpose property, asserted against the source
# --------------------------------------------------------------------------

class TestGeneralPurpose:
    """The engine must carry no knowledge of any particular component.

    Asserted mechanically rather than claimed in a docstring: a SEWCP
    identifier reaching `src/aief_cad/**` would make the engine a SEWCP CAD
    generator, which is the one thing this architecture is not.
    """

    FORBIDDEN = ("SEWCP", "sewcp", "cooling plate", "Cooling Plate", "CP-D0", "CP-IF")

    def test_no_component_identifier_appears_in_the_engine(self):
        offenders = []
        for path in sorted((REPO_ROOT / "src" / "aief_cad").rglob("*.py")):
            text = path.read_text(encoding="utf-8")
            for token in self.FORBIDDEN:
                if token in text:
                    offenders.append(f"{path.relative_to(REPO_ROOT)}: {token!r}")
        assert not offenders, (
            "the general-purpose CAD engine names a specific component:\n  "
            + "\n  ".join(offenders)
        )

    def test_the_addin_carries_no_component_identifier_either(self):
        addin = REPO_ROOT / "fusion_addin" / "AIEF_CAD_Bridge" / "AIEF_CAD_Bridge.py"
        text = addin.read_text(encoding="utf-8")
        assert not [t for t in self.FORBIDDEN if t in text]

    def test_a_wholly_different_component_runs_the_same_path(self, tmp_path):
        """A bracket, not a plate: same orchestration, no code change."""
        p = write_package(
            tmp_path,
            package_id="BRACKET-001",
            component="GENERIC_BRACKET",
            requirements=[
                {"id": "B-1", "kind": "geometry", "statement": "a round boss",
                 "source": "fixture",
                 "value": {"form": "disc", "plane": "XZ", "sketch": "BOSS",
                           "diameter": "boss_d", "thickness": "boss_t", "body": "BOSS_BODY"}},
                {"id": "B-2", "kind": "manufacturing",
                 "statement": "drill access from one side only", "source": "fixture"},
            ],
            parameters=[
                {"name": "boss_d", "expression": "24.0", "unit": "mm"},
                {"name": "boss_t", "expression": "boss_d / 4", "unit": "mm"},
            ],
            acceptance=[{"id": "B-A1", "check": "geometry", "subject": "bodies.count",
                         "expect": 1}],
        )
        pkg = load_package(p)
        sol = resolve(pkg, [a.contribute(pkg) for a in select_agents(pkg)], "S1")
        ops = compile_solution(sol)
        assert sol.resolved["boss_t"] == 6.0
        assert [o.op for o in ops] == [
            "new_document", "set_parameters", "rename_component",
            "create_sketch", "sketch_circle", "extrude", "observe",
        ]
        assert ops[3].args["plane"] == "XZ"


# --------------------------------------------------------------------------
# Channel routing and the annular_channel form
# --------------------------------------------------------------------------

CHANNEL_PACKAGE = (
    REPO_ROOT
    / "implementation"
    / "01_SEWCP-200_Cooling_Plate"
    / "requirements"
    / "SEWCP-200_coolant_channel.requirements.json"
)


def _routing_spec(**overrides):
    from aief_cad.routing import KeepOut, RoutingSpec

    kos = [KeepOut("center", 0.0, 0.0, 15.0),
           KeepOut("pin_a", 100.0, 30.0, 12.0),
           KeepOut("pin_b", 100.0, 150.0, 12.0),
           KeepOut("pin_c", 100.0, 270.0, 12.0),
           KeepOut("outer_a", 130.0, 75.0, 8.5),
           KeepOut("outer_b", 130.0, 195.0, 8.5),
           KeepOut("outer_c", 130.0, 315.0, 8.5)]
    base = dict(envelope_wall_min_r=30.0, envelope_wall_max_r=125.0,
                width=10.0, rib=5.0, min_bend_r=5.0, keep_outs=tuple(kos),
                inlet_az_deg=255.0, outlet_az_deg=285.0, terminal_r=120.0)
    base.update(overrides)
    return RoutingSpec(**base)


class TestChannelRouting:
    def test_the_route_is_deterministic(self):
        from aief_cad.routing import route_channel

        a, b = route_channel(_routing_spec()), route_channel(_routing_spec())
        assert a.as_dict() == b.as_dict()

    def test_every_keep_out_margin_is_positive(self):
        from aief_cad.routing import route_channel

        routed = route_channel(_routing_spec())
        assert routed.min_keep_out_margin
        assert all(m >= 0 for m in routed.min_keep_out_margin.values()), (
            routed.min_keep_out_margin
        )

    def test_the_footprint_closes(self):
        import math

        from aief_cad.routing import route_channel

        fp = list(route_channel(_routing_spec()).footprint)
        for a, b in zip(fp, fp[1:] + fp[:1]):
            gap = math.hypot(b["start"][0] - a["end"][0],
                             b["start"][1] - a["end"][1])
            assert gap < 0.02, "footprint gap %.4f" % gap

    def test_the_centreline_is_continuous(self):
        import math

        from aief_cad.routing import route_channel

        cl = list(route_channel(_routing_spec()).centerline)
        for a, b in zip(cl, cl[1:]):
            gap = math.hypot(b["start"][0] - a["end"][0],
                             b["start"][1] - a["end"][1])
            assert gap < 0.01

    def test_an_impossible_envelope_is_refused(self):
        from aief_cad.routing import RoutingError, route_channel

        with pytest.raises(RoutingError):
            route_channel(_routing_spec(envelope_wall_min_r=118.0,
                                        envelope_wall_max_r=125.0,
                                        terminal_r=120.0))

    def test_a_saturating_keep_out_field_is_refused(self):
        from aief_cad.routing import KeepOut, RoutingError, route_channel

        blockers = tuple(
            KeepOut("b%d_%d" % (r, a), float(r), float(a), 20.0)
            for r in range(30, 130, 20) for a in range(0, 360, 30)
        )
        with pytest.raises(RoutingError):
            route_channel(_routing_spec(keep_outs=blockers))

    def test_adjacent_passes_are_counterflow(self):
        from aief_cad.routing import route_channel

        routed = route_channel(_routing_spec())
        pass_radii = {round(r, 1) for r in routed.pass_radii}
        senses = {}
        for s in routed.centerline:
            if (s["type"] == "arc" and round(s["radius"], 1) in pass_radii
                    and abs(s["center"][0]) < 1e-6
                    and abs(s["center"][1]) < 1e-6):
                senses.setdefault(round(s["radius"], 1), s["ccw"])
        radii = sorted(senses)
        assert len(radii) >= 2
        for r0, r1 in zip(radii, radii[1:]):
            assert senses[r0] != senses[r1], "adjacent passes co-rotate"


class TestChannelPackage:
    def test_the_package_loads_and_routes_offline(self):
        pkg = load_package(CHANNEL_PACKAGE)
        agents = select_agents(pkg)
        contributions = [a.contribute(pkg) for a in agents]
        solution = resolve(pkg, contributions, solution_id="T.S1")
        kinds = [f.kind for f in solution.ordered_features()]
        assert "sketch_path" in kinds
        ops = compile_solution(solution)
        names = [o.op for o in ops]
        assert "sketch_path" in names
        cuts = [o for o in ops if o.op == "extrude"
                and o.args.get("operation") == "cut"]
        assert len(cuts) == 2  # channel pocket + lid split

    def test_the_faying_plane_precedes_the_channel_sketch(self):
        pkg = load_package(CHANNEL_PACKAGE)
        agents = select_agents(pkg)
        solution = resolve(pkg, [a.contribute(pkg) for a in agents],
                           solution_id="T.S2")
        order = [f.id for f in solution.ordered_features()]
        assert order.index("thermal.CP-FAY.plane") < order.index("mech.CP-CH.sketch")

    def test_the_routed_path_cites_its_constraints(self):
        pkg = load_package(CHANNEL_PACKAGE)
        solution = resolve(pkg, [a.contribute(pkg) for a in select_agents(pkg)],
                           solution_id="T.S3")
        path = next(f for f in solution.features if f.kind == "sketch_path")
        assert len(path.params["keep_outs"]) == 36
        assert path.params["width"] == 10.0
        assert path.params["length"] > 1000.0


class TestPathVerification:
    def _feat(self, **param_overrides):
        params = {
            "sketch": "S3",
            "keep_outs": [{"id": "pin", "r": 100.0, "az_deg": 0.0,
                           "wall_clearance": 12.0}],
            "envelope_wall_min_r": 30.0,
            "envelope_wall_max_r": 125.0,
            "width": 10.0,
            "min_bend_r": 5.0,
        }
        params.update(param_overrides)
        return FeatureSpec(id="mech.T.path", kind="sketch_path", params=params)

    def _model(self, curves):
        from aief_cad.observe import parse

        return parse({"sketches": [{"name": "S3", "curve_geometry": curves}]})

    def test_unmeasured_geometry_fails_rather_than_passes(self):
        from aief_cad.verify.geometry import _path_findings

        found = list(_path_findings(self._feat(), self._model([]), "geometry"))
        assert len(found) == 1 and not found[0].passed

    def test_a_wall_inside_a_keep_out_is_caught(self):
        from aief_cad.verify.geometry import _path_findings

        # A wall circle of radius 95 about the origin passes 5 mm from the
        # pin axis at (100, 0) - far inside its 12 mm clearance.
        curves = [{"type": "circle", "center": [0.0, 0.0], "radius": 95.0,
                   "construction": False}]
        found = {f.id: f for f in
                 _path_findings(self._feat(), self._model(curves), "geometry")}
        assert not found["GEO-KEEPOUT-mech.T.path-pin"].passed

    def test_a_compliant_wall_passes_every_derived_check(self):
        from aief_cad.verify.geometry import _path_findings

        curves = [
            {"type": "circle", "center": [0.0, 0.0], "radius": 60.0,
             "construction": False},
            {"type": "circle", "center": [0.0, 0.0], "radius": 50.0,
             "construction": False},
            {"type": "arc", "center": [0.0, 0.0], "radius": 55.0,
             "start": [55.0, 0.0], "end": [-55.0, 0.0], "mid": [0.0, 55.0],
             "construction": True},
        ]
        found = list(_path_findings(self._feat(), self._model(curves),
                                    "geometry"))
        assert found and all(f.passed for f in found), [
            f.as_dict() for f in found if not f.passed
        ]

    def test_a_sub_minimum_centreline_bend_is_caught(self):
        from aief_cad.verify.geometry import _path_findings

        curves = [
            {"type": "circle", "center": [0.0, 0.0], "radius": 60.0,
             "construction": False},
            {"type": "arc", "center": [50.0, 0.0], "radius": 2.0,
             "start": [52.0, 0.0], "end": [48.0, 0.0], "mid": [50.0, 2.0],
             "construction": True},
        ]
        found = {f.id: f for f in
                 _path_findings(self._feat(), self._model(curves), "geometry")}
        assert not found["GEO-BEND-mech.T.path"].passed

