"""C1-C7 as executable predicates. Pure: reads the repository, writes nothing."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent
if str(_SRC) not in sys.path:  # pragma: no cover - import plumbing
    sys.path.insert(0, str(_SRC))

from aief_approval.chain import (  # noqa: E402
    State,
    ecr_approval_states,
    load_approvals,
    verify,
)
from aief_stage6.digests import dc1_digest  # noqa: E402

ECR_DIR = ".ai/project/ecr"
SCHEMA = ".ai/core/schemas/SCH-ecr.schema.json"
INDEX = ".ai/project/OPEN_ITEMS.md"
FROZEN = ".ai/project/FROZEN.md"
VERIF = ".ai/project/verification"

GATED_ECRS = ("ECR-D-001", "ECR-D-002", "ECR-D-003", "ECR-D-004")

_YAML = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
_KEY = re.compile(r"^([a-z_]+):[ \t]*(.*)$")
_ITEM = re.compile(r"^\s*-\s+(.*\S)\s*$")
_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`\s*\|")


@dataclass
class Criterion:
    id: str
    title: str
    verdict: str  # PASS | FAIL | NOT VERIFIED
    evidence: list[str] = field(default_factory=list)
    residue: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.verdict == "PASS"


@dataclass
class GateReport:
    criteria: list[Criterion] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return bool(self.criteria) and all(c.ok for c in self.criteria)


def _yaml_of(text: str) -> dict[str, object]:
    m = _YAML.search(text)
    if not m:
        return {}
    out: dict[str, object] = {}
    key: str | None = None
    for line in m.group(1).splitlines():
        item = _ITEM.match(line)
        if item and key:
            # A key introduced with an empty value and followed by `- ` items is a
            # list. Without this promotion the empty string set below wins and the
            # items are silently dropped - which is how `affected_artifacts` came
            # back undecidable on the first run of this checker.
            if not isinstance(out.get(key), list):
                out[key] = []
            out[key].append(item.group(1))  # type: ignore[union-attr]
            continue
        km = _KEY.match(line)
        if not km:
            continue
        key = km.group(1)
        value = re.split(r"\s+#", km.group(2), maxsplit=1)[0].strip().strip('"')
        out[key] = value if value not in ("", "null", "~") else ""
    return out


def _ecr_records(repo: Path) -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for path in sorted((repo / ECR_DIR).glob("ECR-*.md")):
        data = _yaml_of(path.read_text(encoding="utf-8"))
        eid = str(data.get("ecr_id") or path.name.split("_")[0])
        data["_path"] = path.relative_to(repo).as_posix()
        out[eid] = data
    return out


def _blocking_ids(repo: Path) -> list[str]:
    text = (repo / INDEX).read_text(encoding="utf-8")
    section = re.search(r"^## Blocking\s*$(.*?)^## ", text, re.S | re.M)
    if not section:
        return []
    return [ln.strip() for ln in section.group(1).splitlines() if ln.strip()]


def _c1_to_c4(repo: Path, records, states, index: int) -> Criterion:
    ecr = GATED_ECRS[index - 1]
    cid = f"C{index}"
    title = f"{ecr} carries an approved disposition"
    required = json.loads((repo / SCHEMA).read_text(encoding="utf-8"))["required"]
    evidence: list[str] = []

    record = records.get(ecr)
    if record is None:
        return Criterion(cid, title, "FAIL", [f"{ecr}: no record under {ECR_DIR}"])
    evidence.append(f"record {record['_path']}")

    missing = [k for k in required if k not in record]
    if missing:
        return Criterion(
            cid, title, "FAIL", evidence, [f"{ecr}: SCH-ecr fields missing: {missing}"]
        )
    evidence.append(f"conforms to SCH-ecr ({len(required)} required fields present)")

    if not str(record.get("disposition") or "").strip():
        return Criterion(cid, title, "FAIL", evidence, [f"{ecr}: disposition empty"])
    evidence.append(f"disposition: {str(record['disposition'])[:56]}")

    bound = states.get(ecr)
    if bound is None:
        return Criterion(
            cid, title, "FAIL", evidence, [f"{ecr}: no approval names this ECR"]
        )
    approval_id, state = bound
    if state not in (State.LIVE, State.SUPERSEDED_VALID):
        return Criterion(
            cid, title, "FAIL", evidence,
            [f"{ecr}: approval {approval_id} is {state.value}"],
        )

    # VER-015 F-19: binding the ECR to ONE approval is too weak. `states` picks
    # the strongest-then-highest id, so C2 certified ECR-D-002 on APR-026, whose
    # entire scope is a single `Re` value in spec/README, while the substantive
    # change lived in spec/01 under APR-020. The criterion now requires EVERY
    # approval naming this ECR to be non-VOID and lists all of them, so the
    # evidence cannot rest on an arbitrary thin member of the set.
    approvals, _ = load_approvals(repo)
    chains = verify(repo)
    naming = [
        a for a in approvals
        if ecr in [e.strip() for e in (a.ecr or "").split(",")]
    ]
    void = [
        a for a in naming
        if (chains.state_of(a.approval_id) or State.VOID) is State.VOID
    ]
    if void:
        return Criterion(
            cid, title, "FAIL", evidence,
            [f"{ecr}: approval {a.approval_id} on {a.subject_path} is VOID - "
             f"the artifact moved without a superseding approval" for a in void],
        )
    evidence.append(
        "all "
        + str(len(naming))
        + " approval(s) naming this ECR are non-VOID: "
        + ", ".join(
            f"{a.approval_id} on {a.subject_path.split('_')[0]}"
            for a in sorted(naming, key=lambda x: x.approval_id)
        )
    )
    return Criterion(cid, title, "PASS", evidence)


def _c5(repo: Path, records) -> Criterion:
    """The frozen specification reflects every approved disposition."""
    evidence: list[str] = []
    residue: list[str] = []
    text = (repo / FROZEN).read_text(encoding="utf-8")
    registry = {}
    for line in text.splitlines():
        m = _ROW.match(line.strip())
        if m:
            registry.setdefault(m.group(1), m.group(2))

    spec_paths = {p for p in registry if p.startswith("spec/")}
    for path in sorted(spec_paths):
        target = repo / path
        if not target.is_file():
            residue.append(f"{path}: registered but absent")
            continue
        actual = dc1_digest(target.read_bytes())
        if actual != registry[path]:
            residue.append(
                f"{path}: DC-1 {actual[:12]}... != registered {registry[path][:12]}..."
            )
    evidence.append(f"{len(spec_paths)} spec/** artifacts registered; "
                    f"{len(spec_paths) - len(residue)} reproduce")

    # Every artifact an approved ECR names must itself be registered.
    for eid, record in sorted(records.items()):
        if not str(record.get("disposition") or "").strip():
            continue
        for artifact in record.get("affected_artifacts", []) or []:
            a = str(artifact)
            if a.startswith("spec/") and a not in registry:
                residue.append(f"{eid}: names {a}, which is not registered in FROZEN.md")
    evidence.append("every spec/** artifact named by an approved ECR is registered")

    chains = verify(repo, sorted(spec_paths))
    for path in sorted(spec_paths):
        chain = chains.chains.get(path)
        if chain and not chain.ok:
            residue.extend(chain.failures)
    evidence.append("approval chains reproduce on every spec/** path")
    return Criterion("C5", "Frozen spec reflects every approved disposition",
                     "PASS" if not residue else "FAIL", evidence, residue)


def _c6(repo: Path, records) -> Criterion:
    """Independent verification is recorded per disposition."""
    evidence: list[str] = []
    residue: list[str] = []
    # A report counts only if it DECLARES the ECR as its subject. Matching anywhere
    # in the body passes on a passing mention - the first run of this checker
    # reported C6 PASS for ECR-D-003 and ECR-D-004 on exactly that, before either
    # had ever been verified. That is the false-verification defect this gate
    # exists to catch, so the predicate is the declared subject, not the text.
    reports: dict[str, dict[str, object]] = {}
    for p in sorted((repo / VERIF).glob("VER-*.md")):
        data = _yaml_of(p.read_text(encoding="utf-8"))
        data["_name"] = p.name
        reports[p.name] = data

    for ecr in GATED_ECRS:
        record = records.get(ecr, {})
        if not str(record.get("disposition") or "").strip():
            residue.append(f"{ecr}: no disposition, so nothing to verify")
            continue
        naming = sorted(
            n for n, d in reports.items() if ecr in str(d.get("subject", ""))
        )
        # VER-016 finding 1: requiring EVERY report naming the ECR to clear made
        # C6 unsatisfiable. VER-015's recorded FAIL would block LC-M04-EXIT
        # permanently, because a later clearing report could not displace it. The
        # approvals layer was given a supersession relation and the verification
        # layer was not - the same asymmetry, in the same session, by the same
        # author. A report that is superseded by name is historical evidence and
        # no longer gates; supersession must be DECLARED, never inferred from
        # ordering, for the reason APR-019 already demonstrates.
        superseded = {
            s.strip()
            for d in reports.values()
            for s in str(d.get("supersedes", "")).split(",")
            if s.strip()
        }
        naming = [
            n for n in naming
            if str(reports[n].get("verification_id", "")).strip() not in superseded
        ] or naming
        if not naming:
            residue.append(
                f"{ecr}: no verification report declares it as subject "
                f"(a mention in the body is not verification)"
            )
            continue
        for n in naming:
            d = reports[n]
            verifier = str(d.get("verifier_role", "")).strip()
            author = str(d.get("author_role", "")).strip()
            if verifier and author and verifier == author:
                residue.append(
                    f"{ecr}: {n} verifier_role == author_role ({verifier}) - LAW-05"
                )
            # VER-015 section 0a disclosed this hole before anything else: the
            # predicate was existence plus role-distinctness, so merely FILING a
            # report - even one whose own verdict is FAIL - flipped C6 to PASS.
            # A criterion that cannot read the verdict of the report it rests on
            # is not a criterion. The report's declared status now governs.
            status = str(d.get("status", "")).strip()
            if not status:
                residue.append(f"{ecr}: {n} declares no status")
            elif re.search(r"\bFAIL\b|NOT CLEARED|NOT VERIFIED", status, re.I):
                residue.append(
                    f"{ecr}: {n} declares '{status}' - the report does not clear"
                )
        evidence.append(f"{ecr}: subject of {', '.join(naming)}")
    return Criterion(
        "C6", "Independent verification recorded per disposition",
        "PASS" if not residue else "FAIL", evidence,
        residue + [
            "MACHINE LIMIT: existence and ECR coverage are checked here. That the "
            "verifier obtained its evidence itself, and authored none of the work, "
            "is a LAW-05 reading and is dispositioned in the report, not here"
        ],
    )


def _c7(repo: Path, records) -> Criterion:
    """No ECR against the frozen specification remains undispositioned."""
    residue: list[str] = []
    blocking = _blocking_ids(repo)

    # VER-015 F-18: reading only the Blocking section made C7 evadable. The
    # verifier filed an OPEN, undispositioned ECR against spec/01, left it out of
    # OPEN_ITEMS.md, and C7 still passed - because the index is hand-maintained
    # and omission was invisible. The predicate is now the RECORDS: every ECR-D
    # artifact on disk is examined, whatever the index says. The index is then
    # checked against them, so a divergence is reported rather than exploited.
    for eid, record in sorted(records.items()):
        if not eid.startswith("ECR-D-"):
            continue
        artifacts = [str(a) for a in (record.get("affected_artifacts") or [])]
        spec_artifacts = [a for a in artifacts if a.startswith("spec/")]
        if not artifacts:
            residue.append(f"{eid}: no affected_artifacts - C7 is undecidable")
            continue
        if not spec_artifacts:
            continue
        if not str(record.get("disposition") or "").strip():
            residue.append(
                f"{eid}: UNDISPOSITIONED against {spec_artifacts} "
                f"(record {record['_path']}); listed in OPEN_ITEMS Blocking: "
                f"{eid in blocking}"
            )

    known = set(records)
    for item in blocking:
        if item.startswith("ECR-D-") and item not in known:
            residue.append(f"{item}: listed Blocking with no record - C7 is undecidable")
    for eid, record in sorted(records.items()):
        if not eid.startswith("ECR-D-"):
            continue
        undisposed = not str(record.get("disposition") or "").strip()
        if undisposed and eid not in blocking:
            residue.append(
                f"{eid}: undispositioned but absent from OPEN_ITEMS.md Blocking - "
                f"the index does not describe the records it indexes"
            )

    spec_scoped = [
        e for e, r in records.items()
        if e.startswith("ECR-D-")
        and any(str(a).startswith("spec/") for a in (r.get("affected_artifacts") or []))
    ]
    evidence = [
        f"{len(records)} ECR records on disk examined directly, not via the index",
        f"{len(spec_scoped)} bear on spec/**; all carry a non-empty disposition",
        f"OPEN_ITEMS.md Blocking holds {len(blocking)} ids and is consistent with them",
    ]
    return Criterion("C7", "No ECR against the frozen spec remains undispositioned",
                     "PASS" if not residue else "FAIL", evidence, residue)


def evaluate(repo: Path) -> GateReport:
    records = _ecr_records(repo)
    states = ecr_approval_states(repo)
    report = GateReport()
    for index in (1, 2, 3, 4):
        report.criteria.append(_c1_to_c4(repo, records, states, index))
    report.criteria.append(_c5(repo, records))
    report.criteria.append(_c6(repo, records))
    report.criteria.append(_c7(repo, records))
    return report
