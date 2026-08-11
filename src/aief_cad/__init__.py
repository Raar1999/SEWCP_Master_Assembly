"""General-purpose agent-driven CAD orchestration.

This package holds **no knowledge of any particular engineering problem.** It
ingests a requirement package, routes it to domain agents, resolves their
contributions into a design solution, compiles that solution into a bounded CAD
operation sequence, dispatches the sequence across the Fusion automation
boundary, and verifies what Fusion actually built.

Any particular engineering problem is an *input* to it, carried entirely in
`implementation/**/requirements/*.requirements.json`. Nothing under
`src/aief_cad/**` may import, name or special-case a project identifier -
`tests/test_cad_layer.py::TestGeneralPurpose` asserts that against the source,
so the property is checked rather than claimed.

Three facts are kept distinct throughout, because conflating any two of them is
how a CAD automation layer reports success it did not achieve:

    1. an agent REQUESTED an operation        -> `bridge.protocol.Command`
    2. Fusion PERFORMED the operation         -> `Observation.executed`
    3. the model SATISFIES the requirement    -> `verify.Verdict`

`(2)` is reported by the party that did the work and is therefore never
evidence for `(3)`. Verification reads `Observation.observed` - the model state
Fusion reported back - and never reads `executed`.

Actor provenance: `mechanical.cad-engineer`, under rank-1 instruction.
"""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "PROTOCOL_VERSION",
    "REPO_ROOT",
    "BRIDGE_ROOT",
    "QUEUE_DIR",
    "OBS_DIR",
    "STATE_DIR",
    "RUNS_DIR",
    "CadError",
]

#: Wire format identity. Bumped only on a breaking change to the envelope shape.
#: The add-in refuses a command whose ``protocol`` it does not implement, rather
#: than guessing at a field it does not know.
PROTOCOL_VERSION = "aief-cad/1"


def _find_repo_root(start: Path | None = None) -> Path:
    """Walk up to the directory holding `.ai/`. Never guess the CWD."""
    here = (start or Path(__file__).resolve()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / ".ai").is_dir() and (candidate / "src").is_dir():
            return candidate
    raise CadError(
        "repository root not found: no ancestor of "
        f"{here} holds both .ai/ and src/"
    )


class CadError(Exception):
    """Base for every fault this package raises."""


REPO_ROOT = _find_repo_root()

#: The transport. Chosen at rank-1 direction over a localhost socket precisely
#: because it makes every command and every observation a durable repository
#: artifact: the audit trail is the transport, not a parallel journal of it.
BRIDGE_ROOT = REPO_ROOT / "cad" / "bridge"
QUEUE_DIR = BRIDGE_ROOT / "queue"
OBS_DIR = BRIDGE_ROOT / "obs"
STATE_DIR = BRIDGE_ROOT / "state"

#: One directory per orchestrated run, holding the solution, the dispatched
#: operations, the observations and the verdict. This is what makes a run
#: reproducible without conversational memory.
RUNS_DIR = REPO_ROOT / "cad" / "runs"
