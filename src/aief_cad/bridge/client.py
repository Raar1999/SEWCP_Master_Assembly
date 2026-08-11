"""File-queue transport to the Fusion add-in.

    orchestrator                              Fusion 360
    ------------                              ----------
    write  cad/bridge/queue/NNNN.cmd.json  ->  add-in background thread polls
                                                       |
                                               fireCustomEvent(payload)
                                                       |
                                               MAIN THREAD executes the op
                                                       v
    read   cad/bridge/obs/NNNN.obs.json    <-  add-in writes observation

Writes are atomic: the payload lands on a temporary name in the same directory
and is then renamed. A poller that reads a half-written command is a fault mode
this transport must not have, and rename is the only primitive that reliably
avoids it on Windows and POSIX alike.

`AgentBridge` is the abstract seam. `FileQueueBridge` is the real transport;
`tests/` substitutes a fake at this same seam and nowhere deeper, so a test
that passes has still exercised every layer above the boundary.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Protocol

from aief_cad import OBS_DIR, QUEUE_DIR, STATE_DIR, CadError
from aief_cad.bridge.protocol import (
    BridgeError,
    Command,
    Observation,
    ProtocolError,
    decode_observation,
    encode_command,
)

__all__ = ["AgentBridge", "FileQueueBridge", "BridgeTimeout", "BridgeNotRunning"]


class BridgeTimeout(BridgeError):
    """No observation appeared within the command's declared timeout."""


class BridgeNotRunning(BridgeError):
    """The add-in is not answering, so nothing can be dispatched."""


class AgentBridge(Protocol):
    """The seam between the agent system and Fusion."""

    def send(self, command: Command) -> Observation:  # pragma: no cover - protocol
        ...

    def available(self) -> bool:  # pragma: no cover - protocol
        ...


def _atomic_write(path: Path, payload: bytes) -> None:
    tmp = path.with_name(path.name + ".part")
    tmp.write_bytes(payload)
    os.replace(tmp, path)


class FileQueueBridge:
    """Durable, replayable transport whose audit trail is the transport itself."""

    def __init__(
        self,
        queue_dir: Path | None = None,
        obs_dir: Path | None = None,
        state_dir: Path | None = None,
        poll_s: float = 0.25,
    ) -> None:
        self.queue_dir = Path(queue_dir or QUEUE_DIR)
        self.obs_dir = Path(obs_dir or OBS_DIR)
        self.state_dir = Path(state_dir or STATE_DIR)
        self.poll_s = poll_s
        for d in (self.queue_dir, self.obs_dir, self.state_dir):
            d.mkdir(parents=True, exist_ok=True)

    # -- health ------------------------------------------------------------

    def heartbeat_path(self) -> Path:
        return self.state_dir / "addin.heartbeat.json"

    def available(self, max_age_s: float = 15.0) -> bool:
        """True when the add-in wrote a heartbeat recently enough to be live.

        A stale heartbeat is treated as absent. Dispatching into a queue no one
        is reading produces a timeout several minutes later with no diagnosis;
        failing here names the cause immediately.
        """
        hb = self.heartbeat_path()
        if not hb.is_file():
            return False
        try:
            age = time.time() - hb.stat().st_mtime
        except OSError:
            return False
        return age <= max_age_s

    # -- idempotency -------------------------------------------------------

    def _recorded(self, key: str) -> Path:
        return self.state_dir / f"idem-{key.split(':', 1)[-1][:32]}.json"

    def recorded_observation(self, command: Command) -> Observation | None:
        """Return the observation of an identical earlier effect, if any.

        Identity is the effect - operation plus arguments - not the request, so
        a resumed run does not re-execute work already recorded.
        """
        p = self._recorded(command.idempotency_key)
        if not p.is_file():
            return None
        try:
            return decode_observation(p.read_bytes())
        except ProtocolError:
            return None

    # -- dispatch ----------------------------------------------------------

    def command_path(self, command_id: str) -> Path:
        return self.queue_dir / f"{command_id}.cmd.json"

    def observation_path(self, command_id: str) -> Path:
        return self.obs_dir / f"{command_id}.obs.json"

    def send(self, command: Command, *, reuse: bool = True) -> Observation:
        """Dispatch one operation and wait for the observation."""
        if reuse and command.op != "observe":
            prior = self.recorded_observation(command)
            if prior is not None:
                return prior

        if not self.available():
            raise BridgeNotRunning(
                "the AIEF_CAD_Bridge add-in is not reporting a live heartbeat at "
                f"{self.heartbeat_path()}. Start Fusion 360 and run the add-in "
                "(Utilities > Scripts and Add-Ins > Add-Ins > AIEF_CAD_Bridge > Run). "
                "Nothing is dispatched into a queue with no reader"
            )

        obs_path = self.observation_path(command.command_id)
        if obs_path.exists():
            obs_path.unlink()
        _atomic_write(self.command_path(command.command_id), encode_command(command))

        deadline = time.time() + max(1.0, command.timeout_s)
        while time.time() < deadline:
            if obs_path.is_file():
                # The add-in writes atomically too, so a visible file is whole.
                observation = decode_observation(obs_path.read_bytes())
                if observation.command_id != command.command_id:
                    raise ProtocolError(
                        f"observation at {obs_path} answers "
                        f"{observation.command_id!r}, not {command.command_id!r}"
                    )
                if observation.ok and command.op != "observe":
                    _atomic_write(
                        self._recorded(command.idempotency_key), obs_path.read_bytes()
                    )
                return observation
            time.sleep(self.poll_s)

        raise BridgeTimeout(
            f"{command.command_id} ({command.op}): no observation within "
            f"{command.timeout_s:g}s. The command file is left at "
            f"{self.command_path(command.command_id)} for inspection; it is not "
            f"retried automatically, because a timed-out mutating operation may "
            f"or may not have changed the model and only observation can say which"
        )

    def drain(self) -> int:
        """Remove stale command files with no matching observation. Returns count."""
        n = 0
        for p in sorted(self.queue_dir.glob("*.cmd.json")):
            if not self.observation_path(p.name.split(".", 1)[0]).exists():
                p.unlink()
                n += 1
        return n
