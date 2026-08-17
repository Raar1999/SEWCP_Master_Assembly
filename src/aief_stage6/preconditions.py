"""AMD-31 compile-time precondition checks for Stage 6.

Actor provenance: software.software-engineer - S-2026-08-08-07.

AIEF-AMD-010 AMD-31 / generation_order[6].barrier: 'every validation check
declared phase compile-time except V-10 passes against the manifest and the
complete Stage 1 to 5 output immediately before emission; V-10 is evaluated
on the Stage 6 build itself, never before it.'

Compile-time class (core/validation/CHECKS.md register): V-01..V-09,
V-23..V-25 (V-10 excluded per AMD-31). Check texts are taken from
framework.manifest.json validation[] - per OI-V-07 the manifest V-09/V-10
texts are newer than the emitted CHECKS.md and THE MANIFEST TEXTS GOVERN.

Interpretations resolved from repository records (not by assumption):

- V-02 acyclicity is evaluated over the files[].depends_on build-order graph.
  The `dependencies.edges` citation graph deliberately carries the
  bidirectional LAW-11 <-> agent-contract `references` pair: CMP-BLOCK-014
  (OPEN_ITEMS.md Closed: 'depends_on corrected; citation preserved as
  bidirectional references edges'), confirmed by DR-001 FIND-1 disposition
  ('0 backward edges, V-02 still passes') and VER-002 C4 ('MI-2: DFS over
  125 depends_on edges finds no cycle'). Edge-target existence is checked on
  BOTH graphs.
- V-07 role resolution follows VER-001 criterion 5: producer_role /
  consumer_roles are typed plain strings by SCH-framework-manifest
  (descriptive designators admissible); owner_role is a strict roleId.
- MI-10 (precedence total order) is not represented in the manifest; it is
  evaluated against the Stage 1 emission core/PRECEDENCE.md rank table.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .digests import dc1_digest, dc2_digest
from .manifest import Manifest
from .binding import Binding
from .tokenizers import TokenizerProbe

Check = dict[str, Any]


def _result(check_id: str, name: str, status: str, counts: dict[str, int],
            details: list[str]) -> Check:
    return {"id": check_id, "name": name, "status": status,
            "counts": counts, "details": details}


def _role_ids(manifest: Manifest) -> set[str]:
    agents = manifest.data["agents"]
    ids = {a["id"] for a in agents["universal"]}
    ids |= {a["id"] for a in agents["profile"]}
    return ids


def _all_agents(manifest: Manifest) -> list[dict[str, Any]]:
    agents = manifest.data["agents"]
    return list(agents["universal"]) + list(agents["profile"])


# --------------------------------------------------------------------------
# V-01 - Manifest validation
# --------------------------------------------------------------------------

_STAGE1_ROOTS = ("BOOT.md", "FRAMEWORK.md", "README.md")


def _emitting_stage_for_path(path: str) -> int:
    """The stage-output ownership map, from generation_order[].outputs after
    the declared exclusions (generation_order[1].barrier, AIEF-AMD-009
    AMD-23): Stage 1 owns the roots, core/** minus templates/validation/lock,
    and core/profiles/**; Stage 2 core/templates/**; Stage 3 project/**;
    Stage 4 adapters/**; Stage 5 core/validation/**; Stage 6 the lock."""
    if path in _STAGE1_ROOTS:
        return 1
    if path == "core/MANIFEST.lock":
        return 6
    if path.startswith("core/templates/"):
        return 2
    if path.startswith("core/validation/"):
        return 5
    if path.startswith("core/"):
        return 1  # includes core/profiles/**
    if path.startswith("project/"):
        return 3
    if path.startswith("adapters/"):
        return 4
    raise ValueError(f"path outside every declared stage output: {path}")


def check_v01(manifest: Manifest, repo_root: Path) -> Check:
    """V-01: 'Manifest conforms to SCH-framework-manifest; invariants MI-1 to
    MI-12 satisfied. MI-3 namespace, per AIEF-AMD-009 AMD-24 ... Stage-output
    disjointness, per AIEF-AMD-009 AMD-23 ...' (validation[V-01].verifies;
    MI table at AIEF-FRZ-001 Part 3)."""
    details: list[str] = []
    failures: list[str] = []
    counts: dict[str, int] = {}

    # Schema conformance (JSON Schema 2020-12).
    schema_path = repo_root / "framework" / "SCH-framework-manifest.schema.json"
    try:
        import jsonschema

        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(manifest.data), key=str)
        counts["schema_errors"] = len(errors)
        if errors:
            failures += [f"schema: {e.message}" for e in errors[:10]]
        else:
            details.append("SCH-framework-manifest: conforms (Draft 2020-12)")
    except ImportError:
        failures.append("jsonschema package unavailable - schema conformance unevaluated")

    files = manifest.files
    ids = [f["id"] for f in files]
    id_set = set(ids)

    # MI-1: every file id unique and stable.
    counts["files"] = len(files)
    dup = [i for i in id_set if ids.count(i) > 1]
    if dup:
        failures.append(f"MI-1: duplicate ids {dup}")
    dup_paths = {p for p in (f["path"] for f in files)
                 if [f["path"] for f in files].count(p) > 1}
    if dup_paths:
        failures.append(f"MI-1: duplicate paths {sorted(dup_paths)}")

    # MI-3 strict namespace (AMD-24): every depends_on and referenced_by
    # target is a files[] id; no other namespace satisfies MI-3.
    bad_refs = [
        f"{f['id']}.{field} -> {t}"
        for f in files
        for field in ("depends_on", "referenced_by")
        for t in f.get(field, [])
        if t not in id_set
    ]
    counts["mi3_bad_targets"] = len(bad_refs)
    if bad_refs:
        failures.append(f"MI-3: unresolved targets {bad_refs}")

    # MI-2: depends_on graph acyclic (shared with V-02; evaluated here too
    # because MI-2 is a V-01 invariant).
    cycle = _find_cycle({f["id"]: [t for t in f.get("depends_on", []) if t in id_set]
                         for f in files})
    if cycle:
        failures.append(f"MI-2: depends_on cycle {cycle}")

    # MI-4: sum(token_cap) over T0 u T1 <= 6000.
    capped = [f for f in files if f.get("tier") in ("T0", "T1")
              and f.get("token_cap") is not None]
    total = sum(f["token_cap"] for f in capped)
    counts["mi4_cap_sum"] = total
    if total > 6000:
        failures.append(f"MI-4: cap sum {total} > 6000")

    # MI-5: every law referenced by an agent, workflow or check exists.
    law_ids = {l["id"] for l in manifest.data["laws"]}
    law_refs: set[str] = set()
    for v in manifest.validation:
        if v.get("law_ref"):
            law_refs.add(v["law_ref"])
    for a in _all_agents(manifest):
        for text in a.get("inputs", []):
            law_refs |= set(re.findall(r"\bLAW-\d{2}\b", text))
    for f in files:
        law_refs |= {t for t in f.get("depends_on", []) if re.fullmatch(r"LAW-\d{2}", t)}
    missing_laws = sorted(law_refs - law_ids)
    if missing_laws:
        failures.append(f"MI-5: referenced laws missing {missing_laws}")

    # MI-6: every template referenced by a workflow exists (workflow file
    # entries' tpl-* targets; target existence itself is MI-3).
    wf_tpl = [t for f in files if f["id"].startswith("wf-")
              for t in f.get("depends_on", []) + f.get("referenced_by", [])
              if t.startswith("tpl-")]
    missing_tpl = [t for t in wf_tpl if t not in id_set]
    if missing_tpl:
        failures.append(f"MI-6: workflow template refs missing {missing_tpl}")

    # MI-7: every schema referenced by a check exists.
    schema_ids = {s["id"] for s in manifest.data["schemas"]}
    for v in manifest.validation:
        for tok in re.findall(r"\bsch-[a-z-]+\b", v["verifies"]):
            if tok not in schema_ids:
                failures.append(f"MI-7: check {v['id']} references unknown schema {tok}")
        for tok in re.findall(r"\bSCH-[A-Za-z-]+", v["verifies"]):
            if tok == "SCH-framework-manifest":
                if not (repo_root / "framework" / "SCH-framework-manifest.schema.json").is_file():
                    failures.append("MI-7: SCH-framework-manifest file absent")
            elif tok.lower().replace("sch-", "sch-") not in schema_ids and \
                    f"sch-{tok[4:].lower()}" not in schema_ids:
                failures.append(f"MI-7: check {v['id']} references unknown schema {tok}")

    # MI-8: no universal-scope role carries a discipline tag.
    discipline = {t for p in manifest.data["profiles"] for t in p["discipline_tags"]}
    for a in manifest.data["agents"]["universal"]:
        leak = set(a["capability_tags"]) & discipline
        if leak:
            failures.append(f"MI-8: universal role {a['id']} carries discipline tags {sorted(leak)}")

    # MI-9: every profile declares a complete agent set and lifecycle set.
    profile_agent_ids = {a["id"] for a in manifest.data["agents"]["profile"]}
    for p in manifest.data["profiles"]:
        declared = set(p["agents"])
        contracted = {a for a in profile_agent_ids if a.startswith(p["id"] + ".")}
        if declared != contracted:
            failures.append(
                f"MI-9: profile {p['id']} agents {sorted(declared)} != contracts {sorted(contracted)}")
        if not p.get("lifecycle"):
            failures.append(f"MI-9: profile {p['id']} lifecycle empty")

    # MI-10: precedence ranks form a total order with no gaps - evaluated
    # against core/PRECEDENCE.md (Stage 1 emission; not in the manifest).
    prec = (repo_root / ".ai" / "core" / "PRECEDENCE.md").read_text(encoding="utf-8")
    ranks = sorted({int(m) for m in re.findall(r"^\|\s*\**(\d+)\**\s*\|", prec, re.MULTILINE)})
    counts["mi10_ranks"] = len(ranks)
    if not ranks or ranks != list(range(1, len(ranks) + 1)):
        failures.append(f"MI-10: ranks not a gapless total order: {ranks}")

    # MI-11: every boot step declares cost class and failure behaviour.
    for step in manifest.data["boot_sequence"]:
        if not step.get("cost_class") or not step.get("failure"):
            failures.append(f"MI-11: boot step {step.get('step')} incomplete")

    # MI-12: every partition declares write access and upgrade semantics.
    for part in manifest.data["partitions"]:
        if not part.get("write_access") or not part.get("upgrade_semantics"):
            failures.append(f"MI-12: partition {part.get('id')} incomplete")

    # Stage-output disjointness (AMD-23): every files[] path is owned by
    # exactly one stage's declared output set, and that stage is its
    # generator. The BINDING pin write is a declared field write, 'not an
    # emission' (validation[V-01].verifies), so it claims no path.
    mismatches = []
    for f in files:
        try:
            owner = _emitting_stage_for_path(f["path"])
        except ValueError as exc:
            mismatches.append(str(exc))
            continue
        if owner != f["generator"]:
            mismatches.append(
                f"{f['path']}: generator {f['generator']} but stage-output owner {owner}")
    counts["stage_disjointness_mismatches"] = len(mismatches)
    if mismatches:
        failures.append(f"stage-output disjointness: {mismatches}")

    status = "PASS" if not failures else "FAIL"
    return _result("V-01", "Manifest validation", status, counts, details + failures)


def _find_cycle(graph: dict[str, list[str]]) -> list[str] | None:
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {n: WHITE for n in graph}
    stack: list[str] = []

    def visit(n: str) -> list[str] | None:
        colour[n] = GREY
        stack.append(n)
        for m in graph.get(n, []):
            if colour.get(m, BLACK) == GREY:
                return stack[stack.index(m):] + [m]
            if colour.get(m, BLACK) == WHITE:
                found = visit(m)
                if found:
                    return found
        colour[n] = BLACK
        stack.pop()
        return None

    for n in graph:
        if colour[n] == WHITE:
            found = visit(n)
            if found:
                return found
    return None


def _toposort(graph: dict[str, list[str]]) -> list[str] | None:
    """Kahn topological sort; None when a cycle prevents completion."""
    indeg = {n: 0 for n in graph}
    for n, targets in graph.items():
        for t in targets:
            if t in indeg:
                indeg[t] += 1
    queue = sorted(n for n, d in indeg.items() if d == 0)
    order: list[str] = []
    while queue:
        n = queue.pop(0)
        order.append(n)
        for t in graph.get(n, []):
            if t in indeg:
                indeg[t] -= 1
                if indeg[t] == 0:
                    queue.append(t)
        queue.sort()
    return order if len(order) == len(graph) else None


def check_v02(manifest: Manifest) -> Check:
    """V-02: 'Dependency graph acyclic; every edge target exists; topological
    sort succeeds' (validation[V-02].verifies). Acyclicity over the
    files[].depends_on build-order graph per the recorded CMP-BLOCK-014 /
    DR-001 / VER-002 interpretation (module docstring)."""
    failures: list[str] = []
    files = manifest.files
    id_set = set(manifest.files_by_id)

    dep_graph = {f["id"]: list(f.get("depends_on", [])) for f in files}
    missing = [f"{n}->{t}" for n, ts in dep_graph.items() for t in ts if t not in id_set]
    if missing:
        failures.append(f"depends_on targets missing: {missing}")

    edges = manifest.data["dependencies"]["edges"]
    edge_types = set(manifest.data["dependencies"]["edge_types"])
    for e in edges:
        if e["from"] not in id_set or e["to"] not in id_set:
            failures.append(f"dependencies.edges endpoint missing: {e}")
        if e["type"] not in edge_types:
            failures.append(f"dependencies.edges undeclared type: {e}")

    cycle = _find_cycle({n: [t for t in ts if t in id_set] for n, ts in dep_graph.items()})
    if cycle:
        failures.append(f"depends_on cycle: {cycle}")
    topo = _toposort({n: [t for t in ts if t in id_set] for n, ts in dep_graph.items()})
    if topo is None:
        failures.append("topological sort failed")

    counts = {"depends_on_edges": sum(len(ts) for ts in dep_graph.values()),
              "dependencies_edges": len(edges)}
    return _result("V-02", "Dependency validation",
                   "PASS" if not failures else "FAIL", counts, failures)


def check_v03(manifest: Manifest, repo_root: Path) -> Check:
    """V-03: 'Every law, agent, template, schema, workflow and check reference
    resolves' (validation[V-03].verifies), PLUS the bounded-register split
    half AIEF-AMD-014 AMD-49 bound into this check - see
    `_bounded_register_split`."""
    failures: list[str] = []
    roles = _role_ids(manifest) | {"human-owner"}
    law_ids = {l["id"] for l in manifest.data["laws"]}
    check_ids = {v["id"] for v in manifest.validation}
    schema_ids = {s["id"] for s in manifest.data["schemas"]}
    file_ids = set(manifest.files_by_id)
    file_paths = set(manifest.files_by_path)

    for l in manifest.data["laws"]:
        for c in l["checks"]:
            if c not in check_ids:
                failures.append(f"law {l['id']} check {c} unresolved")
        if l["owner_role"] not in roles:
            failures.append(f"law {l['id']} owner_role {l['owner_role']} unresolved")
    for v in manifest.validation:
        if v.get("law_ref") and v["law_ref"] not in law_ids:
            failures.append(f"check {v['id']} law_ref {v['law_ref']} unresolved")
    for t in manifest.data["templates"]:
        if t["owner_role"] not in roles:
            failures.append(f"template {t['id']} owner_role unresolved")
    for s in manifest.data["schemas"]:
        if s["owner_role"] not in roles:
            failures.append(f"schema {s['id']} owner_role unresolved")
        if s["path"] not in file_paths:
            failures.append(f"schema {s['id']} path {s['path']} not in files[]")
        _ = schema_ids
    for f in manifest.files:
        if f["owner_role"] not in roles:
            failures.append(f"file {f['id']} owner_role {f['owner_role']} unresolved")
    for p in manifest.data["profiles"]:
        for a in p["agents"]:
            if a not in _role_ids(manifest):
                failures.append(f"profile {p['id']} agent {a} unresolved")
    for step in manifest.data["boot_sequence"]:
        for fid in step.get("files", []):
            if fid not in file_ids:
                failures.append(f"boot step {step['step']} file {fid} unresolved")
    for phase in manifest.data["runtime_sequence"]:
        if phase["workflow"] not in file_ids:
            failures.append(f"runtime phase {phase['phase']} workflow unresolved")

    split = _bounded_register_split(manifest, repo_root)
    failures += split.failures

    return _result("V-03", "Cross-reference validation",
                   "PASS" if not failures else "FAIL",
                   {"roles": len(roles), "laws": len(law_ids),
                    "checks": len(check_ids),
                    "register_pairs": split.pairs,
                    "mapped_identifiers": split.identifiers},
                   failures)


@dataclass(frozen=True)
class _SplitResult:
    pairs: int
    identifiers: int
    failures: list[str]


_INDEX_ID = re.compile(r"^[A-Za-z][A-Za-z0-9-]*(?:…[A-Za-z0-9-]+)?$")
_REGISTER_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|")


def _md_sections(text: str, *, rows: bool) -> dict[str, list[str]]:
    """Level-2 headings to their identifiers, under the AMD-49 grammar.

    `rows=False` reads an index: one identifier per line, nothing else on that
    line. `rows=True` reads a register: the leading cell of each table row.
    """
    out: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.split("\n"):
        if line.startswith("## "):
            current = line[3:].strip()
            out[current] = []
            continue
        if current is None:
            continue
        if rows:
            if (line.startswith("|") and not line.startswith("|---")
                    and not re.match(r"^\|\s*ID\s*\|", line)):
                m = _REGISTER_ROW.match(line)
                if m:
                    out[current].append(m.group(1).strip())
        else:
            s = line.strip()
            if s and not s.startswith((">", "|", "#", "-", "*", "`")):
                out[current].append(s)
    return out


def _bounded_register_split(manifest: Manifest, repo_root: Path) -> _SplitResult:
    """The half of validation[V-03] that AIEF-AMD-014 AMD-49 declared and that
    was never implemented.

    validation[V-03].verifies: 'for every pair declared in
    metadata.reproducible.bounded_register_split.pairs the declared mapping
    holds in both directions - for the open-items pair the identifier bijection
    of mapping_open_items ... - and the index conforms to index_grammar. A
    missing, duplicated or section-mismatched identifier on either side, or an
    index line carrying anything beyond one identifier, is a BLOCKING defect'.

    Implemented S-2026-08-11-06. It was declared BLOCKING by an approved
    amendment and checked by nothing for four sessions, and it found two live
    breaks the moment it ran: five register rows carrying a decorated leading
    cell instead of a bare identifier, and two rows sitting in a register
    section the index did not agree with. A ruling without a check is a
    convention - the AMD-19/AMD-26 lesson, applied to AMD-49.

    **The state pair is now checked too.** It was not, and the residual was
    recorded only in this docstring - in no ECR, no register row and no
    verification report. `OI-V-13`'s independent audit found the consequence:
    the skip sat *before* the existence check, so `project/STATE_REGISTER.md`
    could be declared in `files[]` and absent from the tree while V-03 reported
    PASS over `register_pairs: 1` of 2 declared pairs. A BLOCKING clause
    enforced for half its declared domain reports green for the other half,
    which is the `OI-V-02` failure mode one level up. `TCR-002` F-2 recorded
    the missing file as BLOCKING on 2026-08-09 and was never actioned.

    `mapping_state` is a different relation from `mapping_open_items` - a
    section-name correspondence over a YAML block, not an identifier bijection -
    so it gets its own comparison rather than being forced through the wrong
    one. What both pairs now share is the part that never depended on the
    relation at all: **both files must exist.**
    """
    declared = manifest.reproducible.get("bounded_register_split")
    if not declared:
        return _SplitResult(0, 0, [])
    failures: list[str] = []
    pairs = declared.get("pairs", [])
    checked = 0
    identifiers = 0

    for pair in pairs:
        index_id, register_id = pair.get("index"), pair.get("register")
        entry_i = manifest.files_by_id.get(index_id)
        entry_r = manifest.files_by_id.get(register_id)
        if not entry_i or not entry_r:
            failures.append(
                f"bounded_register_split pair {index_id}/{register_id}: "
                f"a member does not resolve in files[]")
            continue
        # Existence first, and for EVERY pair. This check used to sit behind
        # the open-items branch, so a declared register could be missing from
        # the tree without V-03 noticing (OI-V-13 FIND-3, TCR-002 F-2).
        checked += 1
        p_i = repo_root / ".ai" / entry_i["path"]
        p_r = repo_root / ".ai" / entry_r["path"]
        for role, p, entry in (("index", p_i, entry_i), ("register", p_r, entry_r)):
            if not p.is_file():
                failures.append(
                    f"bounded_register_split pair {index_id}/{register_id}: "
                    f"{role} {entry['path']} is declared in files[] and absent "
                    f"from the tree")
        if not (p_i.is_file() and p_r.is_file()):
            continue

        if index_id == "state":
            failures += _mapping_state(entry_i, entry_r, p_i, p_r)
            continue
        if index_id != "open-items":
            failures.append(
                f"bounded_register_split pair {index_id}/{register_id}: no "
                f"mapping is implemented for this pair - a declared pair that "
                f"nothing compares is the defect this check exists to prevent")
            continue
        idx = _md_sections(p_i.read_text(encoding="utf-8"), rows=False)
        reg = _md_sections(p_r.read_text(encoding="utf-8"), rows=True)

        for section, ids in idx.items():
            for token in ids:
                if not _INDEX_ID.match(token):
                    failures.append(
                        f"{entry_i['path']} section '{section}': index line "
                        f"{token!r} carries more than one identifier - "
                        f"index_grammar requires one id per line")
            dupes = sorted({t for t in ids if ids.count(t) > 1})
            if dupes:
                failures.append(
                    f"{entry_i['path']} section '{section}': duplicated "
                    f"identifier(s) {dupes}")
            identifiers += len(ids)

        for section in sorted(set(idx) | set(reg)):
            a, b = idx.get(section), reg.get(section)
            if a is None or b is None:
                failures.append(
                    f"bounded_register_split: section '{section}' exists in "
                    f"{'the register' if a is None else 'the index'} only - "
                    f"the mapping is section-wise and a heading must appear in both")
                continue
            for missing in sorted(set(a) - set(b)):
                failures.append(
                    f"section '{section}': {missing} is in the index and is not "
                    f"the leading cell of any register row")
            for extra in sorted(set(b) - set(a)):
                failures.append(
                    f"section '{section}': {extra} leads a register row and is "
                    f"not in the index")
            rdupes = sorted({t for t in b if b.count(t) > 1})
            if rdupes:
                failures.append(
                    f"section '{section}': duplicated register leading cell(s) "
                    f"{rdupes}")

    return _SplitResult(checked, identifiers, failures)


_YAML_BLOCK = re.compile(r"```yaml\n(.*?)```", re.S)
_YAML_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):")


def _mapping_state(entry_i, entry_r, p_i: Path, p_r: Path) -> list[str]:
    """`mapping_state`, verbatim from the manifest declaration:

        'Every key of the YAML block of project/STATE.md appears exactly once
        as a level-2 heading of project/STATE_REGISTER.md, and every level-2
        heading of that register is either such a key or the literal heading
        Notes.'

    Top-level keys only - a nested key is part of its parent's value, not a
    key of the block.
    """
    failures: list[str] = []
    m = _YAML_BLOCK.search(p_i.read_text(encoding="utf-8"))
    if not m:
        return [f"{entry_i['path']}: no fenced yaml block - mapping_state is "
                f"defined over its keys and there are none to map"]

    keys: list[str] = []
    for line in m.group(1).split("\n"):
        k = _YAML_KEY.match(line)
        if k:
            keys.append(k.group(1))

    headings = [ln[3:].strip() for ln in p_r.read_text(encoding="utf-8").split("\n")
                if ln.startswith("## ")]

    for key in keys:
        n = headings.count(key)
        if n == 0:
            failures.append(
                f"{entry_r['path']}: STATE.md key '{key}' has no level-2 heading "
                f"- mapping_state requires exactly one")
        elif n > 1:
            failures.append(
                f"{entry_r['path']}: key '{key}' appears as {n} level-2 headings "
                f"- mapping_state requires exactly one")
    for heading in headings:
        if heading != "Notes" and heading not in keys:
            failures.append(
                f"{entry_r['path']}: level-2 heading '{heading}' is neither a "
                f"STATE.md key nor the literal heading Notes")
    return failures


def check_v04(manifest: Manifest) -> Check:
    """V-04: 'Thirteen laws present; every machine-checkable law bound to at
    least one check; no orphan law' (validation[V-04].verifies)."""
    failures: list[str] = []
    laws = manifest.data["laws"]
    check_ids = {v["id"] for v in manifest.validation}
    if len(laws) != 13:
        failures.append(f"law count {len(laws)} != 13")
    for l in laws:
        if l.get("checkable") in ("full", "partial") and not l.get("checks"):
            failures.append(f"checkable law {l['id']} bound to no check")
        for c in l.get("checks", []):
            if c not in check_ids:
                failures.append(f"law {l['id']} bound to unknown check {c}")
        if not l.get("checks"):
            failures.append(f"orphan law {l['id']}")
    return _result("V-04", "Law validation", "PASS" if not failures else "FAIL",
                   {"laws": len(laws)}, failures)


def check_v05(manifest: Manifest, repo_root: Path) -> Check:
    """V-05: 'Every role conforms to SCH-agent; at least one forbidden action
    per role; no unassigned duty conflict; no discipline tag on a universal
    role' (validation[V-05].verifies). SCH-agent required fields per
    schemas[sch-agent].required_fields."""
    failures: list[str] = []
    required = next(s for s in manifest.data["schemas"] if s["id"] == "sch-agent")[
        "required_fields"]
    agents = _all_agents(manifest)
    for a in agents:
        for field in required:
            if field not in a or a[field] in (None, "", []):
                # `duty_conflicts: []` is a lawful declaration; only the
                # SCH-agent required fields are mandatory-non-empty.
                if field in a and field == "duty_conflicts":
                    continue
                failures.append(f"agent {a.get('id')}: required field {field} missing/empty")
        if not a.get("forbidden"):
            failures.append(f"agent {a.get('id')}: no forbidden action")
        if "duty_conflicts" not in a:
            failures.append(f"agent {a.get('id')}: duty_conflicts undeclared")
    discipline = {t for p in manifest.data["profiles"] for t in p["discipline_tags"]}
    for a in manifest.data["agents"]["universal"]:
        leak = set(a["capability_tags"]) & discipline
        if leak:
            failures.append(f"universal role {a['id']} discipline tags {sorted(leak)}")

    # Structural conformance of each record against the emitted SCH-agent.
    try:
        import jsonschema

        sch = json.loads((repo_root / ".ai" / "core" / "schemas" /
                          "SCH-agent.schema.json").read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(sch)
        for a in agents:
            for e in validator.iter_errors(a):
                failures.append(f"agent {a['id']}: SCH-agent violation: {e.message}")
    except ImportError:
        failures.append("jsonschema unavailable for SCH-agent conformance")

    return _result("V-05", "Agent validation", "PASS" if not failures else "FAIL",
                   {"agents": len(agents)}, failures)


def check_v06(manifest: Manifest, repo_root: Path) -> Check:
    """V-06: 'All eight schemas valid JSON Schema 2020-12; every target
    artifact has a schema' (validation[V-06].verifies)."""
    failures: list[str] = []
    schemas = manifest.data["schemas"]
    if len(schemas) != 8:
        failures.append(f"schema count {len(schemas)} != 8")
    try:
        import jsonschema

        for s in schemas:
            path = repo_root / ".ai" / Path(s["path"])
            if not path.is_file():
                failures.append(f"{s['id']}: file absent at {s['path']}")
                continue
            try:
                doc = json.loads(path.read_text(encoding="utf-8"))
                jsonschema.Draft202012Validator.check_schema(doc)
            except Exception as exc:
                failures.append(f"{s['id']}: not a valid 2020-12 schema: {exc}")
            if not s.get("target_artifact"):
                failures.append(f"{s['id']}: no target artifact")
    except ImportError:
        failures.append("jsonschema unavailable")
    return _result("V-06", "Schema validation", "PASS" if not failures else "FAIL",
                   {"schemas": len(schemas)}, failures)


def check_v07(manifest: Manifest) -> Check:
    """V-07: 'Every template resolves producer and consumer roles and declares
    acceptance conditions' (validation[V-07].verifies). Role typing per the
    VER-001 criterion-5 precedent (module docstring)."""
    failures: list[str] = []
    roles = _role_ids(manifest) | {"human-owner"}
    for t in manifest.data["templates"]:
        if not t.get("producer_role"):
            failures.append(f"{t['id']}: producer_role empty")
        if not t.get("consumer_roles") or any(not c for c in t["consumer_roles"]):
            failures.append(f"{t['id']}: consumer_roles empty/blank")
        if not t.get("acceptance_conditions"):
            failures.append(f"{t['id']}: no acceptance conditions")
        if t.get("owner_role") not in roles:
            failures.append(f"{t['id']}: owner_role {t.get('owner_role')} not a roleId")
    return _result("V-07", "Template validation", "PASS" if not failures else "FAIL",
                   {"templates": len(manifest.data["templates"])}, failures)


def check_v08(manifest: Manifest) -> Check:
    """V-08: 'Every profile declares a complete agent set and lifecycle stage
    set; zero universal-scope discipline leakage' (validation[V-08]
    .verifies). Completeness of the agent set = exact match with the declared
    agents.profile contracts; file_count cross-checked against files[]
    profile_scope."""
    failures: list[str] = []
    profile_agent_ids = {a["id"] for a in manifest.data["agents"]["profile"]}
    for p in manifest.data["profiles"]:
        declared = set(p["agents"])
        contracted = {a for a in profile_agent_ids if a.startswith(p["id"] + ".")}
        if declared != contracted:
            failures.append(f"{p['id']}: agent set incomplete: {sorted(declared ^ contracted)}")
        if not p.get("lifecycle"):
            failures.append(f"{p['id']}: lifecycle set empty")
        lc_ids = [s["id"] for s in p.get("lifecycle", [])]
        if len(lc_ids) != len(set(lc_ids)):
            failures.append(f"{p['id']}: duplicate lifecycle ids")
        actual = sum(1 for f in manifest.files
                     if f.get("profile_scope") == [p["id"]])
        if actual != p.get("file_count"):
            failures.append(f"{p['id']}: file_count {p.get('file_count')} != files[] {actual}")
    discipline = {t for p in manifest.data["profiles"] for t in p["discipline_tags"]}
    for a in manifest.data["agents"]["universal"]:
        if set(a["capability_tags"]) & discipline:
            failures.append(f"universal leakage on {a['id']}")
    return _result("V-08", "Profile validation", "PASS" if not failures else "FAIL",
                   {"profiles": len(manifest.data["profiles"])}, failures)


def check_v09(manifest: Manifest, repo_root: Path, tokenizers: TokenizerProbe) -> Check:
    """V-09: 'Per-file caps respected; T0 plus T1 at most 6000 tokens under
    both tokenizer families. The two families are TF-1 and TF-2 as declared in
    metadata.reproducible.tokenizer_families ... the maximum governs ...'
    (validation[V-09].verifies - manifest text, which GOVERNS over the stale
    CHECKS.md emission per OI-V-07).

    Fail-safe: with the families not in hand the check is BLOCKED - reported,
    never silently skipped and never passed (dispatch directive)."""
    if not tokenizers.available:
        return _result(
            "V-09", "Token budget validation", "BLOCKED",
            {"families_available": len(tokenizers.families)},
            ["BLOCKED pending platform-engineer tokenizer provisioning: "]
            + tokenizers.missing,
        )
    from . import budget as budget_mod

    try:
        result = budget_mod.measure(
            manifest, repo_root, tokenizers,
            build_id="v09-precondition", timestamp="1970-01-01T00:00:00Z",
        )
        rec = result.record
        # AMD-51: the ceiling comparison is the CHARGED comparison, so the
        # evidence V-09 reports is the charged totals plus the charge itself.
        counts = {k: int(v) for k, v in rec["charged_totals_t0_t1"].items()}
        counts.update({f"measured_{k}": int(v)
                       for k, v in rec["totals_t0_t1"].items()})
        counts["lock_ceiling_charge"] = int(rec["aggregate_ceiling_charge"])
        return _result("V-09", "Token budget validation", "PASS", counts, [])
    except Exception as exc:
        return _result("V-09", "Token budget validation", "FAIL", {}, [str(exc)])


def check_v23(manifest: Manifest) -> Check:
    """V-23: 'For every files[] entry S and every id T in S.depends_on: T
    exists and generator(T) is less than or equal to generator(S). Where
    generator(T) equals generator(S), the intra-stage emission order is a
    topological order of the same-stage depends_on subgraph.'
    (validation[V-23].verifies)."""
    failures: list[str] = []
    by_id = manifest.files_by_id
    backward = 0
    same_stage_graph: dict[int, dict[str, list[str]]] = {}
    for f in manifest.files:
        for t in f.get("depends_on", []):
            if t not in by_id:
                failures.append(f"{f['id']}: depends_on target {t} absent")
                continue
            gs, gt = f["generator"], by_id[t]["generator"]
            if gt > gs:
                backward += 1
                failures.append(f"backward edge {f['id']}(g{gs}) -> {t}(g{gt})")
            elif gt == gs:
                same_stage_graph.setdefault(gs, {}).setdefault(f["id"], []).append(t)
    for stage, graph in sorted(same_stage_graph.items()):
        nodes = {n for n in graph} | {t for ts in graph.values() for t in ts}
        full = {n: graph.get(n, []) for n in nodes}
        if _toposort(full) is None:
            failures.append(f"stage {stage}: same-stage subgraph has no topological order")
    return _result("V-23", "Stage monotonicity validation",
                   "PASS" if not failures else "FAIL",
                   {"backward_edges": backward}, failures)


_FROZEN_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`\s*\|\s*$",
                         re.MULTILINE)


def parse_frozen_registry(repo_root: Path) -> tuple[list[tuple[str, str]], str]:
    """Rows and recorded aggregate of project/FROZEN.md (registry table +
    section 'Aggregate')."""
    text = (repo_root / ".ai" / "project" / "FROZEN.md").read_text(encoding="utf-8")
    section = text.split("## Registered artifacts", 1)[1]
    table = section.split("##", 1)[0]
    rows = _FROZEN_ROW.findall(table)
    agg_section = text.split("## Aggregate", 1)[1]
    m = re.search(r"^\s*([0-9a-f]{64})\s*$", agg_section, re.MULTILINE)
    if not m:
        raise ValueError("FROZEN.md: aggregate value not found")
    return rows, m.group(1)


def check_v24(repo_root: Path) -> Check:
    """V-24: 'Every path registered in project/FROZEN.md exists in the working
    tree and its DC-1 digest equals the registered digest. The DC-2 aggregate
    recomputed over the registry equals the value recorded in FROZEN.md and
    the value in STATE.frozen_set_hash, both at full 64-character length.
    Every artifact meeting the AIEF-AMD-008 AMD-21 registration criterion is
    registered. No path is registered twice.' (validation[V-24].verifies).

    AMD-21 membership is machine-evaluated on the registry's declared scope
    (FROZEN.md section Scope: partitions spec/ and framework/): every file in
    those partitions is registered, except the single artifact ruled out by
    APR-003 (AIEF-ARCH-001, 'superseded ... authorises nothing')."""
    failures: list[str] = []
    rows, recorded_aggregate = parse_frozen_registry(repo_root)
    counts = {"registered": len(rows), "verified": 0}

    paths = [p for p, _ in rows]
    if len(paths) != len(set(paths)):
        failures.append("duplicate registered path")

    for path, digest in rows:
        fs = repo_root / Path(path)
        if not fs.is_file():
            failures.append(f"{path}: absent from working tree")
            continue
        actual = dc1_digest(fs.read_bytes())
        if actual != digest:
            failures.append(f"{path}: DC-1 {actual} != registered {digest}")
        else:
            counts["verified"] += 1

    recomputed = dc2_digest(rows)
    state_text = (repo_root / ".ai" / "project" / "STATE.md").read_text(encoding="utf-8")
    m = re.search(r"frozen_set_hash:\s*([0-9a-f]{64})", state_text)
    state_hash = m.group(1) if m else "<absent>"
    if recomputed != recorded_aggregate:
        failures.append(f"DC-2 {recomputed} != FROZEN.md {recorded_aggregate}")
    if recomputed != state_hash:
        failures.append(f"DC-2 {recomputed} != STATE.frozen_set_hash {state_hash}")
    counts["aggregate_match"] = int(recomputed == recorded_aggregate == state_hash)

    ruled_out = {"framework/AIEF-ARCH-001_AI_Engineering_Framework_Architecture.md"}
    registered = set(paths)
    for partition in ("spec", "framework"):
        for fs in sorted((repo_root / partition).rglob("*")):
            if not fs.is_file():
                continue
            rel = fs.relative_to(repo_root).as_posix()
            if rel not in registered and rel not in ruled_out:
                failures.append(f"AMD-21 criterion candidate unregistered: {rel}")
    for rel in registered:
        if not (rel.startswith("spec/") or rel.startswith("framework/")):
            failures.append(f"registered path outside declared scope: {rel}")

    return _result("V-24", "Freeze registry validation",
                   "PASS" if not failures else "FAIL", counts,
                   failures + [f"recomputed DC-2 aggregate: {recomputed}"])


_NON_ASCII_RUN = re.compile(r"[^\x00-\x7f]+")
_FENCE = re.compile(r"^(```|~~~).*?$.*?^(```|~~~)\s*$", re.MULTILINE | re.DOTALL)
_CODESPAN = re.compile(r"`[^`\n]*`")


def _mojibake_runs(prose: str) -> list[str]:
    """validation[V-25].verifies mojibake rule: 'a maximal run of non-ASCII
    characters that, re-encoded as CP1252 and decoded as UTF-8, both succeed
    and yield a strictly shorter string'."""
    hits = []
    for run in _NON_ASCII_RUN.findall(prose):
        try:
            decoded = run.encode("cp1252").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if len(decoded) < len(run):
            hits.append(run)
    return hits


def check_v25(repo_root: Path) -> Check:
    """V-25: 'Every text artifact under .ai/ and every artifact registered in
    project/FROZEN.md decodes as UTF-8 without error, carries no byte-order
    mark, uses LF line endings exclusively, ends with exactly one terminal
    LF, and contains no mojibake sequence outside quoted evidence.'
    (validation[V-25].verifies). Quoted-evidence exclusion: code spans and
    fenced blocks are masked before the mojibake scan."""
    failures: list[str] = []
    scope: list[Path] = sorted(p for p in (repo_root / ".ai").rglob("*") if p.is_file())
    rows, _ = parse_frozen_registry(repo_root)
    scope += [repo_root / Path(p) for p, _ in rows]

    checked = 0
    for fs in scope:
        rel = fs.relative_to(repo_root).as_posix()
        raw = fs.read_bytes()
        checked += 1
        if raw.startswith(b"\xef\xbb\xbf"):
            failures.append(f"{rel}: byte-order mark")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            failures.append(f"{rel}: not UTF-8 ({exc})")
            continue
        if b"\r" in raw:
            failures.append(f"{rel}: CR line ending")
        if not raw.endswith(b"\n"):
            failures.append(f"{rel}: no terminal LF")
        elif raw.endswith(b"\n\n"):
            failures.append(f"{rel}: more than one terminal LF")
        prose = _CODESPAN.sub("", _FENCE.sub("", text))
        for run in _mojibake_runs(prose):
            failures.append(f"{rel}: mojibake outside quoted evidence: {run!r}")

    return _result("V-25", "Encoding conformance validation",
                   "PASS" if not failures else "FAIL",
                   {"files_checked": checked}, failures)


def run_preconditions(
    manifest: Manifest,
    binding: Binding,
    repo_root: Path,
    tokenizers: TokenizerProbe,
) -> list[Check]:
    """The AMD-31 precondition suite: the compile-time class except V-10
    ('V-10 is evaluated on the Stage 6 build itself, never before it' -
    generation_order[6].barrier)."""
    del binding  # V-checks read BINDING through their own parsers where needed
    return [
        check_v01(manifest, repo_root),
        check_v02(manifest),
        check_v03(manifest, repo_root),
        check_v04(manifest),
        check_v05(manifest, repo_root),
        check_v06(manifest, repo_root),
        check_v07(manifest),
        check_v08(manifest),
        check_v09(manifest, repo_root, tokenizers),
        check_v23(manifest),
        check_v24(repo_root),
        check_v25(repo_root),
    ]


def all_pass(checks: list[Check]) -> bool:
    """AMD-31 gate: every check PASS; a BLOCKED V-09 is not a pass and
    therefore blocks emission (fail-safe)."""
    return all(c["status"] == "PASS" for c in checks)
