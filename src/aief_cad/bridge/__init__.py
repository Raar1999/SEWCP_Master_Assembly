"""The Fusion automation boundary.

Fusion 360 has no external automation API. There is no Design Automation engine
for it, and the Fusion Data API is read-only metadata. The **only** supported
way to drive the modeller is code running inside Fusion's own process - a
Script or an Add-In - and the only supported way to move work from a background
thread onto the thread that owns the document is a registered custom event.

This package is the outside half of that boundary. `protocol` defines the wire
format; `client` implements the file-queue transport chosen at rank-1 direction
over a localhost socket, so that every command and every observation is a
durable repository artifact rather than an ephemeral exchange.

The inside half lives at `fusion_addin/AIEF_CAD_Bridge/` and is deployed into
Fusion's add-in directory by `scripts/install_fusion_addin.py`.
"""

from __future__ import annotations

from aief_cad.bridge.protocol import (
    BridgeError,
    Command,
    Observation,
    ProtocolError,
    decode_observation,
    encode_command,
)

__all__ = [
    "BridgeError",
    "ProtocolError",
    "Command",
    "Observation",
    "encode_command",
    "decode_observation",
]
