"""Reader for `.ai/project/BINDING.md` and the Stage 6 pin-write capability.

Actor provenance: software.software-engineer - S-2026-08-08-07.

DC-4 takes `BINDING.active_profile` and `BINDING.enabled_agents` as inputs
(core_aggregate.enabled_role_coverage.determinism: 'the covered set is a
function of files[], the selected profile and project/BINDING.md
enabled_agents alone'). generation_order[6].outputs declare the pin write:
'project/BINDING.md core_digest_pin (integrity pin write ...; a field write
into an already-emitted instance artifact, not a re-emission of the project
partition; the pin value is the DC-4 aggregate_digest)'.

In this dispatch the pin write is PREVIEW-ONLY: `render_pin_update` returns
the updated content; writing it to the real `.ai/project/BINDING.md` is
refused by the paths.assert_write_allowed guard, by direction of the
dispatching instruction (Stage 6 execution remains unauthorized, OQ-14).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_PIN_LINE = re.compile(r"^(core_digest_pin:\s*)(\S+)(.*)$", re.MULTILINE)
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class Binding:
    path: Path
    text: str
    core_digest_pin: str
    active_profile: str
    enabled_agents: tuple[str, ...]


def _yaml_block(text: str) -> str:
    """Extract the fenced yaml block BINDING.md carries (sch-binding target)."""
    m = re.search(r"```yaml\n(.*?)```", text, re.DOTALL)
    if not m:
        raise ValueError("BINDING.md: no fenced yaml block found")
    return m.group(1)


def load_binding(repo_root: Path) -> Binding:
    """Parse the sch-binding required fields this package consumes.

    A deliberately narrow parser: BINDING is instance YAML with inline `#`
    comments; only `core_digest_pin`, `active_profile` and `enabled_agents`
    are read (the DC-4 inputs plus the pin field Stage 6 writes).
    """
    path = repo_root / ".ai" / "project" / "BINDING.md"
    text = path.read_text(encoding="utf-8")
    block = _yaml_block(text)

    def scalar(key: str) -> str:
        m = re.search(rf"^{key}:\s*([^#\n]+)", block, re.MULTILINE)
        if not m:
            raise ValueError(f"BINDING.md: required field {key} not found")
        return m.group(1).strip()

    agents: list[str] = []
    in_list = False
    for line in block.split("\n"):
        if re.match(r"^enabled_agents:\s*(#.*)?$", line):
            in_list = True
            continue
        if in_list:
            m = re.match(r"^\s+-\s*([^#\s]+)", line)
            if m:
                agents.append(m.group(1))
            elif line.strip() and not line.startswith((" ", "\t")):
                in_list = False
    if not agents:
        raise ValueError("BINDING.md: enabled_agents empty or unparsed")

    return Binding(
        path=path,
        text=text,
        core_digest_pin=scalar("core_digest_pin"),
        active_profile=scalar("active_profile"),
        enabled_agents=tuple(agents),
    )


def render_pin_update(binding_text: str, dc4_aggregate: str) -> str:
    """Return BINDING.md content with `core_digest_pin` set to the DC-4 value.

    Per core_aggregate.self_exclusion: 'The lock is bound ... by the BINDING
    pin: core_digest_pin equals aggregate_digest, per AIEF-FRZ-001 section 1.7
    F-06'. The value token on the `core_digest_pin:` line is replaced; every
    other byte of BINDING.md is preserved (the Stage 6 output is 'a field
    write into an already-emitted instance artifact', generation_order[6]).

    Open Question (recorded in the dispatch report, not silently decided):
    no normative text declares the post-write layout of the line (alignment,
    retention of the inline comment). Minimal deterministic choice: replace
    the value token only.
    """
    if not _HEX64.match(dc4_aggregate):
        raise ValueError("pin value must be the 64-lowercase-hex DC-4 aggregate")
    matches = _PIN_LINE.findall(binding_text)
    if len(matches) != 1:
        raise ValueError(
            f"BINDING content has {len(matches)} core_digest_pin lines; exactly one required"
        )
    return _PIN_LINE.sub(rf"\g<1>{dc4_aggregate}\g<3>", binding_text, count=1)
