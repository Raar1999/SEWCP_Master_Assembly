"""Assembly packages: declared occurrences of saved designs, verified from
observed state.

The component pipeline builds one design from a requirement package; this
module builds one *assembly document* from an assembly package. The package
declares occurrences - which saved design, at which transform, with which
expected placement band - and every value carries provenance to a governing
source, exactly as component requirement packages do.

Verification consumes only the `observe_assembly` observation: identity is
the referenced design name, placement is the observed transform, and the
z-band check catches a wrong local-frame assumption that a transform
comparison alone would miss. No component knowledge lives here: the module
would assemble a gearbox from the same vocabulary.
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from aief_cad import PROTOCOL_VERSION, RUNS_DIR, CadError
from aief_cad.bridge.client import FileQueueBridge
from aief_cad.bridge.protocol import Command
from aief_cad.digest import canonical_json, digest_of, short

__all__ = ["AssemblyError", "AssemblyPackage", "OccurrenceSpec",
           "load_assembly_package", "AssemblyRunner", "verify_assembly"]

TRANSLATE_TOL_MM = 0.05
ROTATE_TOL_DEG = 0.05
ZBAND_TOL_MM = 0.05


class AssemblyError(CadError):
    """The assembly package is absent, malformed, or cannot be executed."""


@dataclass(frozen=True)
class OccurrenceSpec:
    occurrence_id: str
    design: str
    translate_mm: tuple[float, float, float]
    rotate_z_deg: float
    rotate_x_deg: float
    z_band: tuple[float, float] | None
    provenance: str

    def insert_args(self) -> dict[str, Any]:
        args: dict[str, Any] = {
            "name": self.design,
            "translate_mm": list(self.translate_mm),
            "ground": True,
        }
        if self.rotate_z_deg:
            args["rotate_z_deg"] = self.rotate_z_deg
        if self.rotate_x_deg:
            args["rotate_x_deg"] = self.rotate_x_deg
        return args


@dataclass(frozen=True)
class AssemblyPackage:
    package_id: str
    document: str
    units: str
    authority: tuple[str, ...]
    occurrences: tuple[OccurrenceSpec, ...]
    notes: tuple[str, ...]
    digest: str

    def designs(self) -> tuple[str, ...]:
        return tuple(sorted({o.design for o in self.occurrences}))


def load_assembly_package(path: str | Path) -> AssemblyPackage:
    p = Path(path)
    if not p.is_file():
        raise AssemblyError(f"no assembly package at {p}")
    body = json.loads(p.read_text(encoding="utf-8"))
    for key in ("package_id", "document", "authority", "occurrences"):
        if key not in body:
            raise AssemblyError(f"assembly package lacks required key {key!r}")
    occs: list[OccurrenceSpec] = []
    seen: set[str] = set()
    for row in body["occurrences"]:
        oid = row.get("occurrence_id")
        if not oid or oid in seen:
            raise AssemblyError(f"occurrence_id missing or duplicated: {oid!r}")
        seen.add(oid)
        t = row.get("translate_mm") or [0.0, 0.0, 0.0]
        if len(t) != 3:
            raise AssemblyError(f"{oid}: translate_mm must be [x, y, z]")
        band = row.get("z_band")
        if band is not None and (len(band) != 2 or band[0] > band[1]):
            raise AssemblyError(f"{oid}: z_band must be [lo, hi]")
        if not row.get("provenance"):
            raise AssemblyError(f"{oid}: provenance is required - an assembly "
                                "placement without a source is an assumption")
        occs.append(OccurrenceSpec(
            occurrence_id=oid,
            design=row["design"],
            translate_mm=tuple(float(v) for v in t),
            rotate_z_deg=float(row.get("rotate_z_deg") or 0.0),
            rotate_x_deg=float(row.get("rotate_x_deg") or 0.0),
            z_band=tuple(float(v) for v in band) if band else None,
            provenance=row["provenance"],
        ))
    return AssemblyPackage(
        package_id=body["package_id"],
        document=body["document"],
        units=body.get("units", "mm"),
        authority=tuple(body["authority"]),
        occurrences=tuple(occs),
        notes=tuple(body.get("notes") or ()),
        digest=digest_of(canonical_json(body)),
    )


# -- verification ----------------------------------------------------------

def _ang_delta(a: float, b: float) -> float:
    d = (a - b) % 360.0
    return min(d, 360.0 - d)


def verify_assembly(package: AssemblyPackage,
                    observed: dict[str, Any]) -> dict[str, Any]:
    """Checks against observed assembly state. Pure; testable without Fusion."""
    checks: list[dict[str, Any]] = []

    def check(cid: str, passed: bool, statement: str, detail: str) -> None:
        checks.append({"id": cid, "passed": bool(passed),
                       "statement": statement, "detail": detail})

    doc = observed.get("document") or {}
    check("AS-DOC", doc.get("persisted_name") == package.document,
          f"document is {package.document}",
          f"observed {doc.get('persisted_name')!r}")

    rows = list(observed.get("occurrences") or [])
    check("AS-COUNT", len(rows) == len(package.occurrences),
          f"{len(package.occurrences)} occurrences",
          f"observed {len(rows)}")

    unclaimed = list(rows)
    for spec in package.occurrences:
        best = None
        best_d = None
        for row in unclaimed:
            if row.get("source_design") != spec.design:
                continue
            t = row.get("translate_mm") or [0, 0, 0]
            d = max(abs(t[i] - spec.translate_mm[i]) for i in range(3))
            if best is None or d < best_d:
                best, best_d = row, d
        cid = f"AS-{spec.occurrence_id}"
        if best is None:
            check(cid, False, f"{spec.occurrence_id}: {spec.design} present",
                  "no unclaimed occurrence references this design")
            continue
        unclaimed.remove(best)
        faults: list[str] = []
        if best_d > TRANSLATE_TOL_MM:
            faults.append(f"translate off by {best_d:.3f}")
        if _ang_delta(best.get("rotate_z_deg") or 0.0,
                      spec.rotate_z_deg) > ROTATE_TOL_DEG:
            faults.append(f"rotate_z {best.get('rotate_z_deg'):.3f} "
                          f"vs {spec.rotate_z_deg:.3f}")
        want_flip = abs(spec.rotate_x_deg - 180.0) < 1e-6
        z_scale = best.get("z_axis_scale")
        if z_scale is not None and (z_scale < 0) is not want_flip:
            faults.append(f"z-axis scale {z_scale:+.3f} vs "
                          f"rotate_x {spec.rotate_x_deg}")
        if spec.z_band is not None:
            bmin, bmax = best.get("bbox_min"), best.get("bbox_max")
            if not bmin or not bmax:
                faults.append("no observed bounds")
            else:
                if abs(bmin[2] - spec.z_band[0]) > ZBAND_TOL_MM or \
                   abs(bmax[2] - spec.z_band[1]) > ZBAND_TOL_MM:
                    faults.append(
                        f"z-band [{bmin[2]:.3f}, {bmax[2]:.3f}] vs "
                        f"[{spec.z_band[0]:.3f}, {spec.z_band[1]:.3f}]")
        if not best.get("grounded"):
            faults.append("not grounded")
        if best.get("source_version") is None:
            faults.append("no source version recorded")
        check(cid, not faults,
              f"{spec.occurrence_id}: {spec.design} at "
              f"{list(spec.translate_mm)} rz {spec.rotate_z_deg}"
              + (f" rx {spec.rotate_x_deg}" if spec.rotate_x_deg else ""),
              "; ".join(faults) or
              f"placed, grounded, source v{best.get('source_version')}")

    if unclaimed:
        check("AS-EXTRA", False, "no undeclared occurrences",
              "; ".join(f"{r.get('name')} ({r.get('source_design')})"
                        for r in unclaimed))
    else:
        check("AS-EXTRA", True, "no undeclared occurrences", "none")

    passed = all(c["passed"] for c in checks)
    return {"passed": passed, "checks": checks,
            "package_digest": package.digest}


# -- execution -------------------------------------------------------------

class AssemblyRunner:
    """Dispatches an assembly package across the bridge and verifies it."""

    def __init__(self, bridge: FileQueueBridge | None = None,
                 session: str = "unrecorded-session",
                 issued_by: str = "mechanical.cad-engineer",
                 runs_dir: Path | None = None) -> None:
        self.bridge = bridge or FileQueueBridge()
        self.session = session
        self.issued_by = issued_by
        self.runs_dir = Path(runs_dir or RUNS_DIR)

    def _command(self, rid: str, seq: int, op: str,
                 args: dict[str, Any], timeout_s: float = 240.0) -> Command:
        return Command(
            command_id=f"{rid}-A{seq:04d}-{op}",
            op=op,
            args=args,
            issued_by=self.issued_by,
            session=self.session,
            solution_id=f"{rid}.ASM",
            model_target={"document": "assembly"},
            idempotency_key=digest_of(canonical_json(
                {"assembly": rid, "seq": seq, "op": op, "args": args})),
            timeout_s=timeout_s,
        )

    def run(self, package: AssemblyPackage,
            save_on_pass: bool = True) -> dict[str, Any]:
        rid = f"RUN-{time.strftime('%Y%m%dT%H%M%S')}-{short(package.digest, 6)}"
        record: dict[str, Any] = {
            "protocol": PROTOCOL_VERSION,
            "run_id": rid,
            "package_id": package.package_id,
            "package_digest": package.digest,
            "component": package.document,
            "kind": "assembly",
            "notes": list(package.notes),
            "started_at": time.time(),
            "operations": [],
        }
        seq = 0

        def send(op: str, args: dict[str, Any], timeout_s: float = 240.0):
            nonlocal seq
            seq += 1
            obs = self.bridge.send(
                self._command(rid, seq, op, args, timeout_s), reuse=False)
            record["operations"].append(
                {"op": op, "args": args, "status": obs.raw.get("status"),
                 "ok": obs.ok,
                 "error": (obs.raw.get("error") or {}).get("message")})
            if not obs.ok:
                raise AssemblyError(
                    f"{op} failed: {(obs.raw.get('error') or {}).get('message')}")
            return obs

        try:
            send("new_document", {"name": package.document,
                                  "units": package.units})
            send("rename_component", {"name": package.document})
            for spec in package.occurrences:
                send("insert_occurrence", spec.insert_args(), timeout_s=420.0)
            obs = send("observe_assembly", {}, timeout_s=300.0)
            observed = obs.raw.get("observed") or {}
            record["observed_assembly"] = observed
            verdict = verify_assembly(package, observed)
            record["verdict"] = "PASS" if verdict["passed"] else "FAIL"
            record["verification"] = verdict
            if verdict["passed"] and save_on_pass:
                saved = send("save_document",
                             {"name": package.document,
                              "description": f"AIEF {rid} assembly verified"},
                             timeout_s=420.0)
                record["saved"] = saved.raw.get("observed")
        except AssemblyError as exc:
            record["verdict"] = "ERROR"
            record["error"] = str(exc)
        record["finished_at"] = time.time()
        record["record_digest"] = digest_of(canonical_json(record))
        d = self.runs_dir / rid
        d.mkdir(parents=True, exist_ok=True)
        (d / "run.json").write_bytes(
            json.dumps(record, indent=2, sort_keys=True).encode("utf-8")
            + b"\n")
        return record
