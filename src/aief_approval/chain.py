"""The approval-chain relation and its standing check.

See the package docstring for why this exists. This module is pure: it reads the
repository and returns a report. It never writes.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Iterable

# DC-1 has exactly one implementation in this repository, declared normatively in
# framework.manifest.json. Importing it is deliberate: a second copy is the drift
# defect ECR-D-005 and ECR-D-006 already record. If the module is absent we fail
# loudly rather than silently substituting a second construction.
_SRC = Path(__file__).resolve().parent.parent
if str(_SRC) not in sys.path:  # pragma: no cover - import plumbing
    sys.path.insert(0, str(_SRC))
from aief_stage6.digests import dc1_digest  # noqa: E402

_YAML_BLOCK = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
_SCALAR = re.compile(r"^([a-z_]+):[ \t]*(.*)$")
_SEQ_ITEM = re.compile(r"^[ \t]+-[ \t]+(.*)$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_REGISTRY_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`\s*\|")

APPROVAL_DIR = ".ai/project/approvals"
FROZEN = ".ai/project/FROZEN.md"


class State(str, Enum):
    LIVE = "LIVE"
    SUPERSEDED_VALID = "SUPERSEDED-VALID"
    VOID = "VOID"


@dataclass(frozen=True)
class ApprovalRecord:
    approval_id: str
    subject_path: str
    subject_hash: str
    prior_hash: str | None
    ecr: str | None
    supersedes: str | None
    source: str

    @property
    def sort_key(self) -> tuple[str, str]:
        return (self.subject_path, self.approval_id)


@dataclass
class PathChain:
    """Every approval bearing on one subject_path, plus the derived states."""

    subject_path: str
    exists: bool
    tree_digest: str | None
    registered_digest: str | None
    approvals: list[ApprovalRecord] = field(default_factory=list)
    states: dict[str, State] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


@dataclass
class ChainReport:
    chains: dict[str, PathChain] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures and all(c.ok for c in self.chains.values())

    def state_of(self, approval_id: str) -> State | None:
        """The state of an approval across every subject it binds.

        A multi-subject approval is **void if any one of its subjects changes** -
        the LAW-10 clause 2 reading `APR-003` states of itself - so the weakest
        state across its bindings governs. For the single-subject case, which is
        every other approval on disk, this is the state itself.
        """
        rank = {State.VOID: 0, State.SUPERSEDED_VALID: 1, State.LIVE: 2}
        found = [c.states[approval_id] for c in self.chains.values()
                 if approval_id in c.states]
        return min(found, key=lambda s: rank[s]) if found else None


def _strip_comment(value: str) -> str:
    """Drop a trailing ` # ...` comment. Values here are paths, ids and hex
    digests, none of which contain a hash preceded by whitespace."""
    cut = re.split(r"\s+#", value, maxsplit=1)[0]
    return cut.strip()


def _parse_yaml_block(text: str) -> dict[str, str | list[str]]:
    """Read the first fenced yaml block as `key: value` scalars and block
    sequences.

    Indented continuation lines that are not sequence items belong to a
    multi-line scalar and are skipped - every scalar field this module needs is
    single-line. A hand parser is used rather than a yaml dependency because the
    check must run on a bare interpreter.

    **Block sequences are read, not discarded.** An approval may lawfully bind
    several subjects in one instrument - `APR-003` binds eight, and says why in
    its own body - and LAW-10 clause 1 asks that an approval *name what it
    approved*, not that it name exactly one thing. Reading such a value as an
    empty scalar reported a LAW-10 violation that no rule produces, and skipped
    the record, so its bindings went unchecked entirely. Found `S-2026-08-11-06`.
    """
    match = _YAML_BLOCK.search(text)
    if not match:
        return {}
    out: dict[str, str | list[str]] = {}
    current_key: str | None = None
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = _SEQ_ITEM.match(line)
        if item and current_key is not None:
            seq = out.get(current_key)
            if not isinstance(seq, list):
                seq = []
                out[current_key] = seq
            seq.append(_strip_comment(item.group(1)))
            continue
        if line.startswith((" ", "\t")):
            continue
        m = _SCALAR.match(line)
        if not m:
            current_key = None
            continue
        key, raw = m.group(1), _strip_comment(m.group(2))
        current_key = key
        if raw in {"", "null", "~"}:
            # Either a null scalar or the header of a block sequence. Seed it as
            # the empty scalar; a following sequence item replaces it with a
            # list, and none leaves it null - which is what both mean.
            out[key] = ""
        else:
            out[key] = raw
            current_key = None
    return out


def _as_list(value: str | list[str] | None) -> list[str]:
    if value is None or value == "":
        return []
    return list(value) if isinstance(value, list) else [value]


def _scalar(value: str | list[str] | None) -> str:
    """A field this module reads as a scalar. A sequence where a scalar is
    required is not silently collapsed - it returns empty, and the caller's
    own required-field failure fires."""
    return value if isinstance(value, str) else ""


def load_approvals(repo: Path) -> tuple[list[ApprovalRecord], list[str]]:
    """Parse every approval artifact. Returns (records, structural failures)."""
    failures: list[str] = []
    records: list[ApprovalRecord] = []
    directory = repo / APPROVAL_DIR
    if not directory.is_dir():
        return [], [f"{APPROVAL_DIR}: not a directory"]

    seen: dict[str, str] = {}
    for path in sorted(directory.glob("APR-*.md")):
        rel = path.relative_to(repo).as_posix()
        fields = _parse_yaml_block(path.read_text(encoding="utf-8"))
        approval_id = _scalar(fields.get("approval_id"))
        subject_paths = _as_list(fields.get("subject_path"))
        subject_hashes = _as_list(fields.get("subject_hash"))

        if not approval_id:
            failures.append(f"{rel}: no approval_id")
            continue
        if approval_id in seen:
            failures.append(
                f"{approval_id}: declared twice, in {seen[approval_id]} and {rel} - "
                f"an approval id must identify exactly one artifact"
            )
            continue
        seen[approval_id] = rel
        if not subject_paths:
            failures.append(f"{approval_id} ({rel}): no subject_path - LAW-10 clause 1")
            continue
        # A multi-subject approval binds each subject individually and is void if
        # any one of them changes - the LAW-10 clause 2 reading APR-003 states of
        # itself. Pairing is positional, so an unequal count is not a formatting
        # slip: it leaves at least one named subject with no digest bound to it,
        # which is exactly the clause 1 defect.
        if len(subject_hashes) != len(subject_paths):
            failures.append(
                f"{approval_id}: {len(subject_paths)} subject_path entries against "
                f"{len(subject_hashes)} subject_hash entries - every named subject "
                f"must carry its own bound digest, LAW-10 clause 1"
            )
            continue
        # OI-V-13 FIND-8(a): pairing is positional, so the SAME path named twice
        # produces two records - and `PathChain.states` is keyed by approval id,
        # so whichever is processed last silently overwrites the other. A
        # fabricated binding paired with a correct one therefore reported LIVE
        # with report.ok True. A path an approval binds twice binds it to two
        # different digests, which cannot both be the state the approver signed.
        duplicates = sorted({p for p in subject_paths
                             if subject_paths.count(p) > 1})
        if duplicates:
            failures.append(
                f"{approval_id}: subject_path names {', '.join(duplicates)} more "
                f"than once - one approval binds one digest per path, and a "
                f"repeated path would let one binding mask the other"
            )
            continue

        # OI-V-13 FIND-8(b): a block-sequence `prior_hash` was read as an empty
        # scalar and became None, silently making the approval a chain root -
        # the same swallow the multi-subject repair fixed for subject_path, one
        # field over. `prior_hash` is a scalar or null and nothing else.
        raw_prior = fields.get("prior_hash")
        if isinstance(raw_prior, list):
            failures.append(
                f"{approval_id}: prior_hash is a block sequence with "
                f"{len(raw_prior)} entries - it is a single digest or null, and "
                f"reading a sequence as null would silently root the chain"
            )
            continue
        prior = _scalar(raw_prior) or None
        if prior is not None and not _HEX64.match(prior):
            failures.append(
                f"{approval_id}: prior_hash {prior!r} is not 64 lowercase hex or null"
            )
            prior = None

        malformed = False
        for subject_hash in subject_hashes:
            if not _HEX64.match(subject_hash):
                failures.append(
                    f"{approval_id}: subject_hash {subject_hash!r} is not 64 lowercase hex"
                )
                malformed = True
        if malformed:
            continue

        for subject_path, subject_hash in zip(subject_paths, subject_hashes):
            records.append(
                ApprovalRecord(
                    approval_id=approval_id,
                    subject_path=subject_path,
                    subject_hash=subject_hash,
                    prior_hash=prior,
                    ecr=_scalar(fields.get("ecr")) or None,
                    supersedes=_scalar(fields.get("supersedes")) or None,
                    source=rel,
                )
            )
    return records, failures


def load_registry(repo: Path) -> dict[str, str]:
    """Read FROZEN.md's registry rows as {path: registered digest}."""
    text = (repo / FROZEN).read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for line in text.splitlines():
        m = _REGISTRY_ROW.match(line.strip())
        if m:
            out.setdefault(m.group(1), m.group(2))
    return out


def _resolve_states(chain: PathChain) -> None:
    """Derive LIVE / SUPERSEDED-VALID / VOID for one subject_path.

    The chain is walked forward from each approval along prior_hash linkage. A
    fork - two approvals declaring the same prior_hash - makes history ambiguous
    and is a failure, not a preference. A cycle is bounded by a visited set so a
    malformed record cannot hang the check.
    """
    approvals = chain.approvals
    if not approvals:
        return

    by_prior: dict[str, list[ApprovalRecord]] = {}
    by_subject: dict[str, list[ApprovalRecord]] = {}
    for a in approvals:
        if a.prior_hash:
            by_prior.setdefault(a.prior_hash, []).append(a)
        by_subject.setdefault(a.subject_hash, []).append(a)

    for prior, group in sorted(by_prior.items()):
        if len(group) > 1:
            ids = ", ".join(sorted(x.approval_id for x in group))
            chain.failures.append(
                f"{chain.subject_path}: FORK - {ids} all declare prior_hash "
                f"{prior[:12]}..., so the approved history of this artifact is "
                f"ambiguous. Exactly one approval may supersede a given state"
            )
    for digest, group in sorted(by_subject.items()):
        if len(group) > 1:
            ids = ", ".join(sorted(x.approval_id for x in group))
            chain.notes.append(
                f"{chain.subject_path}: {ids} bind the same subject_hash "
                f"{digest[:12]}... - lawful when several ECRs are approved against "
                f"one state, but each must still reach the live head"
            )

    live_ids = {
        a.approval_id for a in approvals if chain.tree_digest and a.subject_hash == chain.tree_digest
    }

    for a in approvals:
        if a.approval_id in live_ids:
            chain.states[a.approval_id] = State.LIVE
            continue
        # Walk forward: who supersedes this state, and does that path reach LIVE?
        seen: set[str] = set()
        frontier = list(by_prior.get(a.subject_hash, []))
        reached = False
        while frontier:
            nxt = frontier.pop()
            if nxt.approval_id in seen:
                continue
            seen.add(nxt.approval_id)
            if nxt.approval_id in live_ids:
                reached = True
                break
            frontier.extend(by_prior.get(nxt.subject_hash, []))
        chain.states[a.approval_id] = (
            State.SUPERSEDED_VALID if reached else State.VOID
        )

    if chain.tree_digest and not live_ids:
        chain.failures.append(
            f"{chain.subject_path}: the working tree is at DC-1 "
            f"{chain.tree_digest[:12]}... and NO approval binds that state. Either "
            f"the artifact was changed without an approval - a LAW-01 freeze "
            f"violation - or the approving artifact was not filed. Every approval "
            f"on this path is VOID in consequence"
        )

    roots = [a for a in approvals if not a.prior_hash or a.prior_hash not in by_subject]
    for r in roots:
        if r.prior_hash:
            chain.notes.append(
                f"{chain.subject_path}: {r.approval_id} roots the chain at prior_hash "
                f"{r.prior_hash[:12]}..., which no filed approval produces - this is "
                f"the pre-approval baseline unless an earlier approval is missing"
            )


def verify(repo: Path, paths: Iterable[str] | None = None) -> ChainReport:
    """Check approval-chain integrity across the frozen registry.

    `paths` restricts the check to the given subject paths; by default every
    registered path and every path any approval names is covered.
    """
    report = ChainReport()
    approvals, failures = load_approvals(repo)
    report.failures.extend(failures)

    try:
        registry = load_registry(repo)
    except OSError as exc:
        report.failures.append(f"{FROZEN}: unreadable ({exc})")
        registry = {}

    subject_paths = {a.subject_path for a in approvals} | set(registry)
    if paths is not None:
        subject_paths &= set(paths)

    for subject_path in sorted(subject_paths):
        target = repo / subject_path
        exists = target.is_file()
        tree_digest = dc1_digest(target.read_bytes()) if exists else None
        chain = PathChain(
            subject_path=subject_path,
            exists=exists,
            tree_digest=tree_digest,
            registered_digest=registry.get(subject_path),
            approvals=sorted(
                (a for a in approvals if a.subject_path == subject_path),
                key=lambda a: a.approval_id,
            ),
        )
        if not exists:
            chain.failures.append(
                f"{subject_path}: named by an approval or the registry but absent "
                f"from the tree"
            )
        else:
            if chain.registered_digest and chain.registered_digest != tree_digest:
                chain.failures.append(
                    f"{subject_path}: FROZEN.md registers {chain.registered_digest[:12]}"
                    f"... but the tree is at {tree_digest[:12]}... - the registry does "
                    f"not describe the artifact it names"
                )
            _resolve_states(chain)
        report.chains[subject_path] = chain

    return report


def ecr_approval_states(repo: Path) -> dict[str, tuple[str, State]]:
    """Map each ECR id to (approval_id, state) for its terminal approval.

    This is what gate criteria C1-C4 consume: an ECR passes when its approval is
    LIVE or SUPERSEDED-VALID.
    """
    report = verify(repo)
    approvals, _ = load_approvals(repo)
    out: dict[str, tuple[str, State]] = {}
    rank = {State.LIVE: 2, State.SUPERSEDED_VALID: 1, State.VOID: 0}
    for a in approvals:
        if not a.ecr:
            continue
        state = report.state_of(a.approval_id) or State.VOID
        # One approval may carry several dispositions: LAW-10 binds it to one
        # content hash, but that content can embody more than one ECR, and it
        # commonly does when several defects land in the same volume.
        for ecr in (e.strip() for e in a.ecr.split(",")):
            if not ecr:
                continue
            current = out.get(ecr)
            # Prefer the strongest state, then the highest approval id - the
            # terminal approval of a chain is the one filed last.
            if current is None or (rank[state], a.approval_id) > (
                rank[current[1]],
                current[0],
            ):
                out[ecr] = (a.approval_id, state)
    return out
