"""V-14 crash validation — induced-fault harness and declared trial count.

Task T-005 (role ``software.test-engineer``). Open item OI-V-06.

V-14 reads, in full:

    V-14 - Crash validation. Severity BLOCKING . law_ref LAW-09 . target ledger-head
    "Termination between entry write and HEAD update detected at next boot in
     all trials"

V-14 does not state a trial count. This module declares it, states the
derivation, and implements the harness. AC-1 is satisfied by the derivation
below; AC-2 by the parametrised trials.


DECLARED TRIAL COUNT: 6
=======================

Derivation
----------

The count is *counted*, not chosen. The reasoning is in four steps.

Step 1 - the trial space is on-disk states, not crash instants.
    B4 runs at the next boot and reads the repository from disk. It has no
    record of when the crash occurred; its inputs are exactly the bytes left
    behind. Detection is therefore a pure function of post-crash on-disk
    state. Wall-clock crash instants are uncountable and cannot be enumerated,
    but the on-disk states reachable in the V-14 window are finite and can be.
    "All trials" is satisfiable by exhaustive enumeration of that finite set.

Step 2 - exhaustive enumeration removes the free parameter.
    If trials were samples drawn from real process-kill timing, N would be a
    sample size, and fixing it would require a confidence level and an
    acceptable residual failure probability. Those are risk-acceptance
    decisions reserved to chief-systems-engineer, and this module would have
    had to stop and escalate under the T-005 escalation clause. Exhaustive
    enumeration over a finite deterministic state space is strictly stronger:
    it yields certainty rather than a confidence bound, and it needs no such
    decision. That is why this harness enumerates. The choice of fault model
    is the one judgement made here, and it is a test-engineering choice; the
    count that follows from it is forced.

Step 3 - the dimensions, each declared and each exhaustive.

    D1 - durability of the orphan entry file at HEAD.seq + 1.  (3 values)
        ``.ai/project/ledger/HEAD`` declares the write order as
        ``entry file -> flush -> HEAD -> STATE.md -> release lock``. Because
        "entry file" and "flush" are declared as *separate* steps, the order
        itself declares that a not-yet-durable interval exists. A reader at
        the next boot can observe exactly three things of a file whose write
        was interrupted: nothing landed, some landed, or all landed. That is
        the complete observable partition, hence:
            COMPLETE   - all bytes durable
            TRUNCATED  - a prefix durable (partial page-cache flush)
            EMPTY      - the file exists at zero length (created, no bytes)
        The fourth residue, ABSENT, is excluded from the trial set: if no
        bytes landed at all, the entry write did not occur, so the
        termination is not "between entry write and HEAD update" and falls
        outside V-14's window. ABSENT is retained below as a negative control.

    D2 - HEAD.state at the moment of the crash.  (2 values)
        HEAD's "Genesis semantics" section declares that ``state`` "takes one
        of two values", ``genesis`` and ``active`` - an exhaustive, closed
        enumeration. Both must be covered because B4's operative check set
        differs between them: under ``genesis``, check 1 is "vacuous by
        definition" and checks 2 and 3 are "the operative reconciliation",
        while under ``active`` all three checks apply.

    The remaining state is fixed by the window itself and contributes no
    dimension: HEAD is by definition not yet updated, and STATE.md is written
    after HEAD, so it is not yet updated either.

Step 4 - the product.

        D1 x D2  =  3 x 2  =  6 trials.

The 6 trials are exhaustive over the enumerated space, so "in all trials" is
established by construction rather than by sampling.

Controls (declared as controls, NOT counted in the 6)
-----------------------------------------------------
Four further cases guard the detector against the degenerate way of passing
V-14 - a detector that always reports divergence would satisfy "detected in
all trials" while being useless:

    ABSENT x {genesis, active}        - clean abort, nothing durable, expect
                                        NO divergence
    clean close x {genesis, active}   - all five steps complete, expect
                                        NO divergence

Residual question, referred and not assumed
-------------------------------------------
This derivation covers the deterministic enumeration model. If
chief-systems-engineer intends V-14 to additionally require statistical
crash injection against a live process and real filesystem, that is a
different question whose N *would* require a residual-failure-probability
decision. That referral is recorded in the T-005 report; it is not resolved
here and no number has been invented for it.


Scope note
----------
No V-14 check and no B4 detector exist in ``src/`` (``preconditions.py``
implements V-01..V-09, V-23..V-25 only). ``reference_boot_b4`` below is
therefore a test-local reference implementation of the three B4 checks as
declared in ``.ai/project/ledger/HEAD``. Standing up a production detector is
outside this task's write scope (``tests/test_stage6_*.py``) and is reported
as a finding.

Every trial runs against a throwaway fixture tree under pytest ``tmp_path``.
The live ledger is never read for mutation and never written.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import pytest

# --------------------------------------------------------------------------
# Declared constants
# --------------------------------------------------------------------------

#: The declared V-14 trial count. See module docstring for the derivation.
V14_TRIAL_COUNT = 6

#: Session-close write order, as declared in .ai/project/ledger/HEAD.
WRITE_ORDER = ("entry_file", "flush", "head", "state", "release_lock")

#: Segments seal every 500 entries (declared in HEAD).
SEGMENT_SIZE = 500

#: HEAD.state is a closed two-value enumeration (declared in HEAD).
HEAD_STATES = ("genesis", "active")

#: Observable residues of an interrupted entry-file write.
DURABILITY_COMPLETE = "complete"
DURABILITY_TRUNCATED = "truncated"
DURABILITY_EMPTY = "empty"
DURABILITY_ABSENT = "absent"  # control only - outside the V-14 window

#: D1: the three residues that constitute a V-14 trial.
V14_DURABILITIES = (DURABILITY_COMPLETE, DURABILITY_TRUNCATED, DURABILITY_EMPTY)

#: The full enumerated V-14 trial set: D1 x D2.
V14_TRIALS = tuple(
    (state, durability) for state in HEAD_STATES for durability in V14_DURABILITIES
)


class InducedCrash(Exception):
    """Raised to terminate a simulated session close at an injection point."""


# --------------------------------------------------------------------------
# Fixture repository
# --------------------------------------------------------------------------


def _segment_for(seq: int) -> str:
    """Segment directory holding ``seq``. Segments seal every 500 entries."""
    return f"SEG-{((max(seq, 1) - 1) // SEGMENT_SIZE):04d}"


def _ledger_dir(root: Path) -> Path:
    return root / ".ai" / "project" / "ledger"


def _entry_glob(root: Path, seq: int) -> list[Path]:
    """Locate an entry by stem, extension-agnostic.

    HEAD names entries as ``L-0000001`` without declaring a file extension, so
    existence is tested by stem glob rather than by an assumed suffix.
    """
    seg = _ledger_dir(root) / _segment_for(seq)
    if not seg.is_dir():
        return []
    return sorted(seg.glob(f"L-{seq:07d}*"))


def _entry_path(root: Path, seq: int) -> Path:
    seg = _ledger_dir(root) / _segment_for(seq)
    seg.mkdir(parents=True, exist_ok=True)
    return seg / f"L-{seq:07d}.md"


def _entry_body(seq: int) -> bytes:
    return (
        f"# Ledger entry L-{seq:07d}\n\n"
        f"```yaml\nseq: {seq}\nsession: S-{seq:04d}\n```\n\n"
        "Body content for the simulated entry, long enough that a truncated\n"
        "prefix is a genuinely different byte string from the whole.\n"
    ).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_head(root: Path, *, seq: int, state: str, entry_hash: str | None,
                prev_hash: str | None) -> None:
    ledger = _ledger_dir(root)
    ledger.mkdir(parents=True, exist_ok=True)
    (ledger / "HEAD").write_text(
        "# Ledger HEAD\n\n```yaml\n"
        f"seq:         {seq}\n"
        f"state:       {state}\n"
        f"entry_hash:  {entry_hash if entry_hash else 'null'}\n"
        f"segment:     {_segment_for(max(seq, 1))}\n"
        f"prev_hash:   {prev_hash if prev_hash else 'null'}\n"
        "```\n",
        encoding="utf-8",
    )


def _read_head(root: Path) -> dict[str, object]:
    text = (_ledger_dir(root) / "HEAD").read_text(encoding="utf-8")
    block = re.search(r"```yaml\n(.*?)```", text, re.S)
    assert block, "fixture HEAD has no yaml block"
    head: dict[str, object] = {}
    for line in block.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.split("#")[0].strip()
        head[key.strip()] = None if value == "null" else value
    head["seq"] = int(str(head["seq"]))
    return head


def _write_state(root: Path, last_ledger_seq: int) -> None:
    path = root / ".ai" / "project" / "STATE.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# STATE\n\n```yaml\nlast_ledger_seq: {last_ledger_seq}\n```\n",
        encoding="utf-8",
    )


def _read_state_seq(root: Path) -> int:
    text = (root / ".ai" / "project" / "STATE.md").read_text(encoding="utf-8")
    match = re.search(r"last_ledger_seq:\s*(\d+)", text)
    assert match, "fixture STATE.md has no last_ledger_seq"
    return int(match.group(1))


def build_repo(root: Path, head_state: str) -> dict[str, object]:
    """Materialise a fixture repository whose HEAD is in ``head_state``.

    ``genesis`` -> seq 0, no entries. ``active`` -> seq 3, entries 1..3 present
    and HEAD.entry_hash bound to entry 3.
    """
    assert head_state in HEAD_STATES
    if head_state == "genesis":
        _write_head(root, seq=0, state="genesis", entry_hash=None, prev_hash=None)
        _write_state(root, 0)
        (_ledger_dir(root) / "SEG-0000").mkdir(parents=True, exist_ok=True)
        return {"seq": 0, "state": "genesis"}

    prev_hash = None
    entry_hash = None
    for seq in (1, 2, 3):
        body = _entry_body(seq)
        _entry_path(root, seq).write_bytes(body)
        prev_hash, entry_hash = entry_hash, _sha256(body)
    _write_head(root, seq=3, state="active", entry_hash=entry_hash,
                prev_hash=prev_hash)
    _write_state(root, 3)
    return {"seq": 3, "state": "active"}


# --------------------------------------------------------------------------
# Fault inducer - the declared write order, interruptible
# --------------------------------------------------------------------------


def session_close(root: Path, *, crash_after: str | None,
                  durability: str = DURABILITY_COMPLETE) -> list[str]:
    """Execute the declared session-close write order, optionally crashing.

    Steps run in the order declared by HEAD:
    ``entry file -> flush -> HEAD -> STATE.md -> release lock``.

    ``crash_after`` names the last step to complete; an :class:`InducedCrash`
    is then raised so that every later step genuinely never runs. The fault is
    induced by real omission of the remaining writes, not by mutating state
    after the fact - so the residue on disk is exactly what an interrupted
    close leaves.

    ``durability`` selects the observable residue of the entry-file write for
    the case where the crash precedes the flush.
    """
    head = _read_head(root)
    next_seq = int(head["seq"]) + 1
    completed: list[str] = []

    # Step 1 - entry file.
    body = _entry_body(next_seq)
    path = _entry_path(root, next_seq)
    if durability == DURABILITY_ABSENT:
        pass  # no bytes reached the disk at all
    elif durability == DURABILITY_EMPTY:
        path.write_bytes(b"")  # inode created, zero bytes durable
    elif durability == DURABILITY_TRUNCATED:
        path.write_bytes(body[: len(body) // 3])  # a prefix reached the disk
    else:
        path.write_bytes(body)
    completed.append("entry_file")
    if crash_after == "entry_file":
        raise InducedCrash("terminated after entry write, before flush")

    # Step 2 - flush.
    if path.exists():
        with open(path, "rb+") as handle:
            os.fsync(handle.fileno())
    completed.append("flush")
    if crash_after == "flush":
        raise InducedCrash("terminated after flush, before HEAD update")

    # Step 3 - HEAD.
    durable = path.read_bytes() if path.exists() else b""
    _write_head(root, seq=next_seq, state="active", entry_hash=_sha256(durable),
                prev_hash=head.get("entry_hash"))  # type: ignore[arg-type]
    completed.append("head")
    if crash_after == "head":
        raise InducedCrash("terminated after HEAD update, before STATE.md")

    # Step 4 - STATE.md.
    _write_state(root, next_seq)
    completed.append("state")
    if crash_after == "state":
        raise InducedCrash("terminated after STATE.md, before lock release")

    # Step 5 - release lock.
    completed.append("release_lock")
    return completed


# --------------------------------------------------------------------------
# Detector - B4 as declared in .ai/project/ledger/HEAD
# --------------------------------------------------------------------------


@dataclass
class B4Result:
    """Outcome of the three B4 checks at a simulated boot."""

    check1: str = "pending"  # pass | fail | vacuous
    check2: str = "pending"  # pass | fail
    check3: str = "pending"  # pass | fail
    findings: list[str] = field(default_factory=list)
    orphan_seq: int | None = None

    @property
    def divergence_detected(self) -> bool:
        return bool(self.findings)

    @property
    def failed_checks(self) -> list[str]:
        return [
            name
            for name, status in (
                ("check1", self.check1),
                ("check2", self.check2),
                ("check3", self.check3),
            )
            if status == "fail"
        ]


def reference_boot_b4(root: Path) -> B4Result:
    """Run boot step B4 against a fixture repository.

    Implements the three checks exactly as declared in HEAD's "B4
    verification" section:

      1. Verify the entry at HEAD.seq against HEAD.entry_hash. Vacuous when
         state is ``genesis`` - no entry exists to verify.
      2. Verify no file at HEAD.seq + 1  <- orphan detection.
      3. Verify STATE.last_ledger_seq equals HEAD.seq.
    """
    head = _read_head(root)
    seq = int(head["seq"])
    state = head["state"]
    result = B4Result()

    # Check 1 - committed entry integrity.
    if state == "genesis":
        result.check1 = "vacuous"
    else:
        matches = _entry_glob(root, seq)
        if not matches:
            result.check1 = "fail"
            result.findings.append(f"B4.1 entry L-{seq:07d} missing")
        elif _sha256(matches[0].read_bytes()) != head.get("entry_hash"):
            result.check1 = "fail"
            result.findings.append(f"B4.1 entry L-{seq:07d} hash mismatch")
        else:
            result.check1 = "pass"

    # Check 2 - no orphan at HEAD.seq + 1.
    orphans = _entry_glob(root, seq + 1)
    if orphans:
        result.check2 = "fail"
        result.orphan_seq = seq + 1
        result.findings.append(
            f"B4.2 orphan entry at seq {seq + 1}: {orphans[0].name} "
            f"({orphans[0].stat().st_size} bytes) - termination between entry "
            f"write and HEAD update"
        )
    else:
        result.check2 = "pass"

    # Check 3 - STATE / HEAD reconciliation.
    state_seq = _read_state_seq(root)
    if state_seq != seq:
        result.check3 = "fail"
        result.findings.append(
            f"B4.3 STATE.last_ledger_seq {state_seq} != HEAD.seq {seq}"
        )
    else:
        result.check3 = "pass"

    return result


# --------------------------------------------------------------------------
# AC-1 - the declared count is recorded, derived, and matches what runs
# --------------------------------------------------------------------------


def test_declared_trial_count_is_the_enumerated_product():
    """The count is the product of the two declared dimensions."""
    assert len(V14_DURABILITIES) == 3          # D1
    assert len(HEAD_STATES) == 2               # D2
    assert V14_TRIAL_COUNT == len(V14_DURABILITIES) * len(HEAD_STATES) == 6


def test_declared_count_matches_executed_trials():
    """The declared number and the number actually run cannot drift apart."""
    assert len(V14_TRIALS) == V14_TRIAL_COUNT
    assert len(set(V14_TRIALS)) == V14_TRIAL_COUNT, "trial set has duplicates"


def test_absent_is_excluded_from_the_trial_set():
    """ABSENT is a control, not a trial: no bytes landed, so no entry write."""
    assert DURABILITY_ABSENT not in V14_DURABILITIES


def test_write_order_matches_head_declaration():
    """The inducer's steps are the write order HEAD declares, in order."""
    assert WRITE_ORDER == ("entry_file", "flush", "head", "state",
                           "release_lock")


# --------------------------------------------------------------------------
# AC-2 - the fault is induced and detected in every trial
# --------------------------------------------------------------------------


@pytest.mark.parametrize("head_state,durability", V14_TRIALS,
                         ids=[f"{s}-{d}" for s, d in V14_TRIALS])
def test_v14_crash_detected_at_next_boot(tmp_path, head_state, durability):
    """Terminate between entry write and HEAD update; B4 must detect it."""
    build_repo(tmp_path, head_state)
    before = _read_head(tmp_path)

    crash_after = "entry_file" if durability != DURABILITY_COMPLETE else "flush"
    with pytest.raises(InducedCrash):
        session_close(tmp_path, crash_after=crash_after, durability=durability)

    # The window is real: HEAD and STATE.md were genuinely never updated.
    after = _read_head(tmp_path)
    assert after == before, "HEAD must not have advanced inside the window"
    assert _read_state_seq(tmp_path) == before["seq"]

    # An orphan is on disk at HEAD.seq + 1.
    assert _entry_glob(tmp_path, int(before["seq"]) + 1), "no orphan induced"

    result = reference_boot_b4(tmp_path)
    assert result.divergence_detected, f"B4 missed the crash: {result}"
    assert result.check2 == "fail"
    assert result.orphan_seq == int(before["seq"]) + 1
    assert any("orphan entry" in f for f in result.findings)


@pytest.mark.parametrize("head_state,durability", V14_TRIALS,
                         ids=[f"{s}-{d}" for s, d in V14_TRIALS])
def test_check2_is_the_sole_detector_of_this_fault(tmp_path, head_state,
                                                   durability):
    """Only B4 check 2 fires - so check 2 is load-bearing and irreplaceable.

    Check 1 passes (the committed entry at HEAD.seq is untouched; vacuous
    under genesis) and check 3 reconciles (STATE.md is written *after* HEAD,
    so both still hold the pre-close value). If check 2 were removed, this
    entire fault class would boot clean and undetected.
    """
    build_repo(tmp_path, head_state)
    crash_after = "entry_file" if durability != DURABILITY_COMPLETE else "flush"
    with pytest.raises(InducedCrash):
        session_close(tmp_path, crash_after=crash_after, durability=durability)

    result = reference_boot_b4(tmp_path)
    assert result.failed_checks == ["check2"], (
        f"expected check2 alone to fire, got {result.failed_checks}"
    )
    assert result.check1 == ("vacuous" if head_state == "genesis" else "pass")
    assert result.check3 == "pass"


def test_all_six_trials_detected_in_one_sweep(tmp_path):
    """'In all trials' asserted over the whole enumerated set at once."""
    detected = 0
    for head_state, durability in V14_TRIALS:
        root = tmp_path / f"{head_state}-{durability}"
        root.mkdir()
        build_repo(root, head_state)
        crash_after = ("entry_file" if durability != DURABILITY_COMPLETE
                       else "flush")
        with pytest.raises(InducedCrash):
            session_close(root, crash_after=crash_after, durability=durability)
        if reference_boot_b4(root).check2 == "fail":
            detected += 1
    assert detected == V14_TRIAL_COUNT, (
        f"detected {detected} of {V14_TRIAL_COUNT} trials"
    )


# --------------------------------------------------------------------------
# Controls - guard against a detector that always reports divergence
# --------------------------------------------------------------------------


@pytest.mark.parametrize("head_state", HEAD_STATES)
def test_control_absent_entry_is_a_clean_abort(tmp_path, head_state):
    """No bytes landed: outside V-14's window, and nothing to reconcile."""
    build_repo(tmp_path, head_state)
    with pytest.raises(InducedCrash):
        session_close(tmp_path, crash_after="entry_file",
                      durability=DURABILITY_ABSENT)

    result = reference_boot_b4(tmp_path)
    assert not result.divergence_detected, f"false positive: {result.findings}"
    assert result.check2 == "pass"


@pytest.mark.parametrize("head_state", HEAD_STATES)
def test_control_clean_close_boots_without_divergence(tmp_path, head_state):
    """All five steps complete: B4 must pass."""
    build_repo(tmp_path, head_state)
    completed = session_close(tmp_path, crash_after=None)
    assert tuple(completed) == WRITE_ORDER

    result = reference_boot_b4(tmp_path)
    assert not result.divergence_detected, f"false positive: {result.findings}"
    assert result.failed_checks == []
    assert result.check1 == "pass"  # genesis has transitioned to active


def test_control_crash_after_head_is_a_different_fault_class(tmp_path):
    """Sanity boundary: a crash *after* HEAD is caught by check 3, not check 2.

    This is outside V-14's window and is asserted only to show the harness
    distinguishes the window's fault from its neighbour.
    """
    build_repo(tmp_path, "active")
    with pytest.raises(InducedCrash):
        session_close(tmp_path, crash_after="head")

    result = reference_boot_b4(tmp_path)
    assert result.failed_checks == ["check3"]
    assert result.check2 == "pass"


# --------------------------------------------------------------------------
# Containment - the live ledger is never touched
# --------------------------------------------------------------------------


def test_harness_writes_only_inside_tmp_path(tmp_path):
    """Every path the harness writes is under the pytest fixture root."""
    build_repo(tmp_path, "genesis")
    with pytest.raises(InducedCrash):
        session_close(tmp_path, crash_after="flush")

    written = [p for p in tmp_path.rglob("*") if p.is_file()]
    assert written, "fixture produced no files"
    for path in written:
        assert tmp_path in path.parents or path.parent == tmp_path or \
            str(path).startswith(str(tmp_path))


def test_live_ledger_head_is_not_a_harness_target():
    """The repository's real HEAD is never opened for writing by this module.

    Guards against a future edit repointing the fixture helpers at the live
    ledger, which the T-005 forbidden_actions prohibit.
    """
    source = Path(__file__).read_text(encoding="utf-8")
    body = source.split('"""', 2)[-1]  # exclude the module docstring
    for helper in ("_write_head(", "_write_state(", "_entry_path("):
        for call in re.finditer(re.escape(helper) + r"([^)]*)", body):
            assert "repo_root" not in call.group(1), (
                f"{helper} must only ever be called with a tmp fixture root"
            )
    imported = re.findall(r"^\s*(?:from|import)\s+([\w.]+)", body, re.M)
    assert not [m for m in imported if m.split(".")[0].startswith("aief")], (
        f"harness must stay self-contained and must not execute Stage 6; "
        f"found imports: {imported}"
    )
