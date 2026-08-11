"""Wire format for the Fusion automation boundary.

Three facts, three fields, never merged:

    Command                     an agent REQUESTED an operation
    Observation.executed        Fusion PERFORMED it
    (verify.Verdict)            the model SATISFIES the requirement

`executed` is reported by the party that did the work, so it is evidence for
the second fact and for nothing else. `observed` - the model state Fusion read
back after the operation - is the only input verification is allowed to use.

`status` distinguishes three outcomes that a single boolean would flatten:

    OK        the operation ran and the model changed as the operation asked
    ERROR     the operation ran and Fusion raised
    REJECTED  the add-in refused it - unknown op, bad protocol, bad argument

REJECTED is not a Fusion failure. Reporting it as one would send the repair
loop looking for a geometry problem that does not exist.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any

from aief_cad import PROTOCOL_VERSION, CadError
from aief_cad.digest import canonical_json, digest_of

__all__ = [
    "BridgeError",
    "ProtocolError",
    "STATUSES",
    "Command",
    "Observation",
    "encode_command",
    "decode_observation",
]


class BridgeError(CadError):
    """Transport fault: the bridge is absent, stalled, or unreachable."""


class ProtocolError(CadError):
    """An envelope is malformed or announces a protocol this layer cannot read."""


STATUSES = ("OK", "ERROR", "REJECTED")


@dataclass(frozen=True)
class Command:
    """One requested operation, addressed to one model."""

    command_id: str
    op: str
    args: dict[str, Any]
    issued_by: str
    session: str
    solution_id: str
    model_target: dict[str, Any]
    idempotency_key: str
    timeout_s: float = 120.0
    op_id: str | None = None
    feature: str | None = None
    issued_at: float = field(default_factory=time.time)

    def as_dict(self) -> dict[str, Any]:
        return {
            "protocol": PROTOCOL_VERSION,
            "command_id": self.command_id,
            "op": self.op,
            "args": self.args,
            "issued_by": self.issued_by,
            "session": self.session,
            "solution_id": self.solution_id,
            "model_target": self.model_target,
            "idempotency_key": self.idempotency_key,
            "timeout_s": self.timeout_s,
            "op_id": self.op_id,
            "feature": self.feature,
            "issued_at": self.issued_at,
        }

    @property
    def digest(self) -> str:
        return digest_of(canonical_json(self.as_dict()))


@dataclass(frozen=True)
class Observation:
    """What Fusion reported back. The sole evidence base for verification."""

    command_id: str
    status: str
    executed: bool
    observed: dict[str, Any]
    fusion: dict[str, Any]
    error: dict[str, Any] | None = None
    started_at: float | None = None
    finished_at: float | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        """The operation ran without raising. **Not** a verification result."""
        return self.status == "OK" and self.executed

    @property
    def rejected(self) -> bool:
        return self.status == "REJECTED"

    @property
    def duration_s(self) -> float | None:
        if self.started_at is None or self.finished_at is None:
            return None
        return self.finished_at - self.started_at

    def error_message(self) -> str:
        if not self.error:
            return ""
        return f"{self.error.get('kind', 'error')}: {self.error.get('message', '')}"


def encode_command(cmd: Command) -> bytes:
    """Canonical bytes for the queue file. Sorted keys, UTF-8, one newline."""
    return canonical_json(cmd.as_dict()) + b"\n"


def _require(d: dict[str, Any], key: str, where: str) -> Any:
    if key not in d:
        raise ProtocolError(f"{where}: missing required field {key!r}")
    return d[key]


def decode_observation(data: bytes | str) -> Observation:
    """Parse and validate an observation envelope.

    A malformed observation is a protocol fault, never an empty result: an
    unreadable answer must not be allowed to look like a model with no bodies
    in it.
    """
    if isinstance(data, bytes):
        try:
            data = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ProtocolError(f"observation is not UTF-8: {exc}") from exc
    try:
        d = json.loads(data)
    except json.JSONDecodeError as exc:
        raise ProtocolError(f"observation is not JSON: {exc}") from exc
    if not isinstance(d, dict):
        raise ProtocolError(f"observation top level is {type(d).__name__}, not an object")

    proto = d.get("protocol")
    if proto != PROTOCOL_VERSION:
        raise ProtocolError(
            f"observation announces protocol {proto!r}; this layer implements "
            f"{PROTOCOL_VERSION!r}. A mismatched envelope is refused rather "
            f"than read field-by-field on the assumption the parts overlap"
        )

    status = _require(d, "status", "observation")
    if status not in STATUSES:
        raise ProtocolError(f"observation status {status!r} not in {list(STATUSES)}")
    executed = _require(d, "executed", "observation")
    if not isinstance(executed, bool):
        raise ProtocolError(
            f"observation executed is {type(executed).__name__}, not a boolean"
        )
    if status == "OK" and not executed:
        raise ProtocolError(
            "observation claims status OK with executed=false; the two fields "
            "disagree about whether anything happened"
        )
    observed = d.get("observed") or {}
    if not isinstance(observed, dict):
        raise ProtocolError(
            f"observation observed is {type(observed).__name__}, not an object"
        )
    err = d.get("error")
    if err is not None and not isinstance(err, dict):
        raise ProtocolError(f"observation error is {type(err).__name__}, not an object")
    if status in ("ERROR", "REJECTED") and not err:
        raise ProtocolError(
            f"observation status {status} carries no error object; a failure "
            f"with no stated cause cannot be diagnosed or repaired"
        )

    return Observation(
        command_id=_require(d, "command_id", "observation"),
        status=status,
        executed=executed,
        observed=observed,
        fusion=d.get("fusion") or {},
        error=err,
        started_at=d.get("started_at"),
        finished_at=d.get("finished_at"),
        raw=d,
    )
