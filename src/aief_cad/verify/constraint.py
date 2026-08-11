"""Constraint verifier - are the governing values and constraints actually held?

Owns acceptance conditions of check families `constraint` and `parameter`, and
adds three intrinsic checks that catch the failure modes a dimension check
alone does not see:

    1. every solution parameter exists in the model, and holds the value the
       expression resolves to;
    2. a parameter the solution declares as a derivation is a derivation in the
       model, not a literal that happens to agree today. A literal that matches
       is the defect, because it stops tracking its source on the next edit;
    3. a sketch the solution requires to be fully constrained is.
"""

from __future__ import annotations

from aief_cad.observe import ObservedModel
from aief_cad.solution import DesignSolution

__all__ = ["verify_constraints"]

#: Fusion reports an angle in degrees and a length in millimetres when the
#: document is millimetre-based. A tolerance below this is inside its own
#: display rounding and would fail on a correct model.
VALUE_TOL = 1e-4


def verify_constraints(solution: DesignSolution, model: ObservedModel):
    from aief_cad.verify import Finding, VerifierReport, _acceptance_findings

    area = "constraint"
    findings = list(
        _acceptance_findings(solution, model, ("constraint", "parameter"), area)
    )

    declared = {p.name: p for p in solution.parameters}

    # -- 1. presence and value --------------------------------------------
    missing = [n for n in declared if model.parameter(n) is None]
    findings.append(
        Finding(
            id="CON-PARAM-PRESENT",
            passed=not missing,
            subject="parameters.count",
            expected=len(declared),
            observed=len(model.parameters),
            detail="" if not missing else (
                f"{len(missing)} declared parameter(s) absent from the model: "
                + ", ".join(sorted(missing)[:8])
                + (" ..." if len(missing) > 8 else "")
            ),
            area=area,
        )
    )

    wrong: list[str] = []
    for name, param in declared.items():
        observed = model.parameter(name)
        if observed is None or observed.value is None:
            continue
        expected = solution.resolved.get(name)
        if expected is None:
            continue
        if abs(observed.value - float(expected)) > VALUE_TOL:
            wrong.append(
                f"{name}: expected {float(expected):g}, model holds {observed.value:g}"
            )
    findings.append(
        Finding(
            id="CON-PARAM-VALUE",
            passed=not wrong,
            subject="parameter:*.value",
            expected="every parameter equals its resolved expression",
            observed=f"{len(wrong)} mismatched",
            detail="; ".join(wrong[:6]) + (" ..." if len(wrong) > 6 else ""),
            area=area,
        )
    )

    # -- 2. a derivation must stay a derivation ----------------------------
    flattened: list[str] = []
    for name, param in declared.items():
        if param.is_literal:
            continue
        observed = model.parameter(name)
        if observed is None:
            continue
        if observed.is_literal_expression:
            flattened.append(
                f"{name}: solution declares {param.expression!r}, model holds "
                f"the literal {observed.expression!r}"
            )
    findings.append(
        Finding(
            id="CON-PARAM-DERIVED",
            passed=not flattened,
            subject="parameter:*.is_derived",
            expected="every declared derivation is an expression in the model",
            observed=f"{len(flattened)} flattened to literals",
            detail="; ".join(flattened[:6]) + (
                "" if len(flattened) <= 6 else " ..."
            ) + ("" if not flattened else (
                ". A literal that agrees today stops agreeing the moment its "
                "source parameter moves, and nothing reports that it has"
            )),
            area=area,
        )
    )

    # -- 3. declared sketch constraint state -------------------------------
    unconstrained: list[str] = []
    for feat in solution.features:
        if feat.kind not in ("sketch", "sketch_circle", "construction_sketch"):
            continue
        if not feat.params.get("fully_constrained", False):
            continue
        name = str(feat.params.get("name") or feat.params.get("sketch", ""))
        sk = model.sketch(name)
        if sk is None or sk.fully_constrained is not True:
            unconstrained.append(
                f"{name}: {'absent' if sk is None else 'not fully constrained'}"
            )
    if any(
        f.params.get("fully_constrained")
        for f in solution.features
        if f.kind in ("sketch", "sketch_circle", "construction_sketch")
    ):
        findings.append(
            Finding(
                id="CON-SKETCH-CONSTRAINED",
                passed=not unconstrained,
                subject="sketch:*.fully_constrained",
                expected=True,
                observed=f"{len(unconstrained)} not constrained",
                detail="; ".join(unconstrained[:6]),
                area=area,
            )
        )

    # -- 4. units ----------------------------------------------------------
    expected_units = None
    for feat in solution.features:
        if feat.kind == "document":
            expected_units = feat.params.get("units", "mm")
    if expected_units:
        got = model.units
        findings.append(
            Finding(
                id="CON-UNITS",
                passed=got == expected_units,
                subject="document.units",
                expected=expected_units,
                observed=got,
                detail="" if got == expected_units else (
                    "every dimension in the solution is stated in the declared "
                    "unit; a document in another unit silently rescales all of them"
                ),
                area=area,
            )
        )

    return VerifierReport(verifier="constraint", findings=tuple(findings))
