"""Engineering requirement ingestion - the general-purpose top-level input.

A requirement package describes *an engineering problem*, not a CAD model and
not a Fusion document. It may describe a heat exchanger plate, a mounting
bracket, a vacuum component, a fixture - anything whose requirements can be
stated in the vocabulary below. The orchestrator determines which domain agents
are needed by reading the requirement kinds present, never by knowing what the
component is.

Serialisation is JSON, for two reasons that both matter: the Fusion add-in runs
in Fusion's embedded interpreter and can take no third-party dependency, and a
canonical byte form is what lets a package be digest-pinned into a result
record the way `LAW-10` pins an approval subject.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aief_cad import CadError
from aief_cad.digest import canonical_json, digest_of

__all__ = [
    "KINDS",
    "Requirement",
    "Parameter",
    "Interface",
    "Material",
    "ManufacturingConstraint",
    "Acceptance",
    "RequirementPackage",
    "RequirementError",
    "load_package",
]


class RequirementError(CadError):
    """A requirement package is absent, malformed, or internally inconsistent."""


#: The requirement vocabulary. A `kind` is what routes a requirement to a
#: domain agent, so this tuple - not a component name - is the extension point
#: for a new engineering domain.
KINDS: tuple[str, ...] = (
    "geometry",       # envelope, dimensions, form
    "structural",     # stiffness, load, deflection, mass
    "thermal",        # heat, temperature, flow, cooling
    "interface",      # mating, fastening, alignment to another component
    "manufacturing",  # process, access, producibility
    "material",       # material and finish
    "electrical",     # conduction, isolation, RF
)

_REQUIRED_TOP = ("package_id", "component", "authority", "requirements")


def _require(data: dict[str, Any], keys: tuple[str, ...], where: str) -> None:
    missing = [k for k in keys if k not in data]
    if missing:
        raise RequirementError(
            f"{where}: missing required key(s) {', '.join(missing)}"
        )


def _as_list_of_dict(value: Any, where: str) -> list[dict[str, Any]]:
    """Reject a bare string where a list is declared.

    A string is iterable, so a coercing reader silently turns ``"CP-01"`` into
    five one-character entries. `aief_exec.records` was bitten by exactly this
    and the same guard is owed here.
    """
    if value is None:
        return []
    if isinstance(value, str) or not isinstance(value, list):
        raise RequirementError(
            f"{where}: expected a list of objects, got {type(value).__name__}"
        )
    for n, entry in enumerate(value):
        if not isinstance(entry, dict):
            raise RequirementError(
                f"{where}[{n}]: expected an object, got {type(entry).__name__}"
            )
    return value


@dataclass(frozen=True)
class Requirement:
    """One stated engineering requirement, with its verification and source."""

    id: str
    kind: str
    statement: str
    source: str
    value: float | str | None = None
    unit: str | None = None
    verification: str | None = None

    @staticmethod
    def from_dict(d: dict[str, Any], n: int) -> "Requirement":
        _require(d, ("id", "kind", "statement", "source"), f"requirements[{n}]")
        if d["kind"] not in KINDS:
            raise RequirementError(
                f"requirements[{n}] ({d['id']}): kind {d['kind']!r} is not one "
                f"of {', '.join(KINDS)}. A new domain is added by extending "
                f"KINDS and supplying an agent that owns it, never by widening "
                f"an existing kind to mean something else"
            )
        return Requirement(
            id=d["id"],
            kind=d["kind"],
            statement=d["statement"],
            source=d["source"],
            value=d.get("value"),
            unit=d.get("unit"),
            verification=d.get("verification"),
        )


@dataclass(frozen=True)
class Parameter:
    """A named driving value. `expression` may reference other parameters."""

    name: str
    expression: str
    unit: str
    source: str
    comment: str = ""

    @property
    def is_literal(self) -> bool:
        """True when the expression is a bare number, not a derivation."""
        try:
            float(self.expression)
        except (TypeError, ValueError):
            return False
        return True

    @staticmethod
    def from_dict(d: dict[str, Any], n: int) -> "Parameter":
        _require(d, ("name", "expression", "unit"), f"parameters[{n}]")
        return Parameter(
            name=d["name"],
            expression=str(d["expression"]),
            unit=d["unit"],
            source=d.get("source", ""),
            comment=d.get("comment", ""),
        )


@dataclass(frozen=True)
class Interface:
    """A mating relationship to another component."""

    id: str
    mates_to: str
    nature: str
    features: tuple[dict[str, Any], ...] = ()
    source: str = ""

    @staticmethod
    def from_dict(d: dict[str, Any], n: int) -> "Interface":
        _require(d, ("id", "mates_to", "nature"), f"interfaces[{n}]")
        return Interface(
            id=d["id"],
            mates_to=d["mates_to"],
            nature=d["nature"],
            features=tuple(_as_list_of_dict(d.get("features"), f"interfaces[{n}].features")),
            source=d.get("source", ""),
        )


@dataclass(frozen=True)
class Material:
    name: str
    density: float | None = None
    source: str = ""
    properties: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "Material":
        _require(d, ("name",), "material")
        return Material(
            name=d["name"],
            density=d.get("density"),
            source=d.get("source", ""),
            properties=d.get("properties", {}),
        )


@dataclass(frozen=True)
class ManufacturingConstraint:
    id: str
    statement: str
    source: str = ""
    process: str | None = None

    @staticmethod
    def from_dict(d: dict[str, Any], n: int) -> "ManufacturingConstraint":
        _require(d, ("id", "statement"), f"manufacturing[{n}]")
        return ManufacturingConstraint(
            id=d["id"],
            statement=d["statement"],
            source=d.get("source", ""),
            process=d.get("process"),
        )


@dataclass(frozen=True)
class Acceptance:
    """A machine-checkable condition on the built model.

    `check` names a verifier family; `subject` and the comparison fields are
    interpreted by that verifier. The package states the condition; it does not
    state how to measure it.
    """

    id: str
    check: str
    subject: str
    expect: Any
    tolerance: float | None = None
    unit: str | None = None
    requirement: str | None = None

    @staticmethod
    def from_dict(d: dict[str, Any], n: int) -> "Acceptance":
        _require(d, ("id", "check", "subject", "expect"), f"acceptance[{n}]")
        return Acceptance(
            id=d["id"],
            check=d["check"],
            subject=d["subject"],
            expect=d["expect"],
            tolerance=d.get("tolerance"),
            unit=d.get("unit"),
            requirement=d.get("requirement"),
        )


@dataclass(frozen=True)
class RequirementPackage:
    """The authoritative input. Immutable once loaded, and digest-identified."""

    package_id: str
    component: str
    authority: tuple[str, ...]
    requirements: tuple[Requirement, ...]
    parameters: tuple[Parameter, ...]
    interfaces: tuple[Interface, ...]
    manufacturing: tuple[ManufacturingConstraint, ...]
    acceptance: tuple[Acceptance, ...]
    material: Material | None
    scope: dict[str, Any]
    digest: str
    source_path: Path | None = None

    # -- domain routing ----------------------------------------------------

    def domains(self) -> tuple[str, ...]:
        """Derive the engineering domains present, in `KINDS` order.

        This is the whole of the orchestrator's domain determination: it reads
        the kinds actually stated and nothing else. A package with no thermal
        requirement does not summon a thermal agent, whatever the component is
        called.
        """
        present = {r.kind for r in self.requirements}
        present |= {"manufacturing"} if self.manufacturing else set()
        present |= {"material"} if self.material else set()
        present |= {"interface"} if self.interfaces else set()
        return tuple(k for k in KINDS if k in present)

    def by_kind(self, kind: str) -> tuple[Requirement, ...]:
        return tuple(r for r in self.requirements if r.kind == kind)

    def parameter(self, name: str) -> Parameter | None:
        for p in self.parameters:
            if p.name == name:
                return p
        return None

    def requirement(self, rid: str) -> Requirement | None:
        for r in self.requirements:
            if r.id == rid:
                return r
        return None


def _check_internal_consistency(pkg: RequirementPackage) -> None:
    """Reject a package that contradicts itself, before any agent reads it."""
    seen: dict[str, str] = {}
    for group, items in (
        ("requirement", [r.id for r in pkg.requirements]),
        ("parameter", [p.name for p in pkg.parameters]),
        ("interface", [i.id for i in pkg.interfaces]),
        ("acceptance", [a.id for a in pkg.acceptance]),
    ):
        for ident in items:
            if ident in seen and seen[ident] == group:
                raise RequirementError(
                    f"{group} id {ident!r} is declared twice; which one governs "
                    f"is undefined and taking the first is a tie-break, not a "
                    f"reading (LAW-12)"
                )
            seen[ident] = group

    names = {p.name for p in pkg.parameters}
    for a in pkg.acceptance:
        if a.requirement and pkg.requirement(a.requirement) is None:
            raise RequirementError(
                f"acceptance {a.id} cites requirement {a.requirement!r}, which "
                f"this package does not declare"
            )
        # `parameter:<name>.<attr>` is the only subject form that names a
        # parameter. `parameters.count` and every other aggregate subject
        # names none, so only the qualified form is checked - a check that
        # rejected the aggregates would reject correct packages.
        if a.subject.startswith("parameter:"):
            pname = a.subject.split(":", 1)[1].split(".", 1)[0]
            if pname not in names:
                raise RequirementError(
                    f"acceptance {a.id} checks parameter {pname!r}, which this "
                    f"package does not declare"
                )


_PARAM_COLUMNS = ("Name", "Unit", "Expression")


def _parameters_from_master(package_path: Path, ref: str, source: str) -> list[Parameter]:
    """Read the parameter set from an external parameter master.

    A package that restated a parameter master inline would *be* a second
    master, and two masters disagree the moment one of them is edited. The
    reference keeps one governing source; this reads it and never writes it.
    """
    master = (package_path.parent / ref).resolve()
    if not master.is_file():
        raise RequirementError(
            f"{package_path}: parameters_from names {ref!r}, which resolves to "
            f"{master} and does not exist"
        )
    with master.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in _PARAM_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise RequirementError(
                f"{master}: parameter master is missing column(s) "
                f"{', '.join(missing)}; found {reader.fieldnames}"
            )
        out: list[Parameter] = []
        for n, row in enumerate(reader):
            name = (row.get("Name") or "").strip()
            if not name:
                raise RequirementError(f"{master}: row {n + 2} has no Name")
            out.append(
                Parameter(
                    name=name,
                    expression=(row.get("Expression") or "").strip(),
                    unit=(row.get("Unit") or "").strip(),
                    source=source,
                    comment=(row.get("Comment") or "").strip(),
                )
            )
    if not out:
        raise RequirementError(f"{master}: parameter master is empty")
    return out


def load_package(path: str | Path) -> RequirementPackage:
    """Read, validate and digest-identify a requirement package."""
    p = Path(path)
    if not p.is_file():
        raise RequirementError(f"requirement package not found: {p}")
    raw = p.read_bytes()
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RequirementError(f"{p}: not readable as UTF-8 JSON - {exc}") from exc
    if not isinstance(data, dict):
        raise RequirementError(f"{p}: top level is {type(data).__name__}, not an object")

    _require(data, _REQUIRED_TOP, str(p))
    authority = data["authority"]
    if isinstance(authority, str) or not isinstance(authority, list) or not authority:
        raise RequirementError(
            f"{p}: authority must be a non-empty list of source citations. A "
            f"package that cites nothing cannot be traced to an engineering "
            f"baseline (LAW-06)"
        )

    inline = [
        Parameter.from_dict(d, n)
        for n, d in enumerate(_as_list_of_dict(data.get("parameters"), "parameters"))
    ]
    ref = data.get("parameters_from")
    if ref and inline:
        raise RequirementError(
            f"{p}: declares both parameters_from and an inline parameters list. "
            f"Which governs is undefined, and a package with two parameter "
            f"sources is the second-master defect it exists to avoid"
        )
    parameters = (
        _parameters_from_master(p, str(ref), data.get("parameters_source", str(ref)))
        if ref
        else inline
    )

    pkg = RequirementPackage(
        package_id=data["package_id"],
        component=data["component"],
        authority=tuple(authority),
        requirements=tuple(
            Requirement.from_dict(d, n)
            for n, d in enumerate(_as_list_of_dict(data.get("requirements"), "requirements"))
        ),
        parameters=tuple(parameters),
        interfaces=tuple(
            Interface.from_dict(d, n)
            for n, d in enumerate(_as_list_of_dict(data.get("interfaces"), "interfaces"))
        ),
        manufacturing=tuple(
            ManufacturingConstraint.from_dict(d, n)
            for n, d in enumerate(
                _as_list_of_dict(data.get("manufacturing"), "manufacturing")
            )
        ),
        acceptance=tuple(
            Acceptance.from_dict(d, n)
            for n, d in enumerate(_as_list_of_dict(data.get("acceptance"), "acceptance"))
        ),
        material=Material.from_dict(data["material"]) if data.get("material") else None,
        scope=data.get("scope", {}),
        # The digest covers the resolved parameter set, not merely the
        # reference to it. Pinning the reference alone would let the parameter
        # master move underneath an unchanged package digest, which is exactly
        # the drift a digest exists to make visible.
        digest=digest_of(
            canonical_json(
                {
                    "package": data,
                    "parameters": [
                        {"name": q.name, "unit": q.unit, "expression": q.expression}
                        for q in parameters
                    ],
                }
            )
        ),
        source_path=p,
    )
    if not pkg.requirements:
        raise RequirementError(f"{p}: declares no requirements")
    _check_internal_consistency(pkg)
    return pkg
