"""Dual-tokenizer measurement interface, TF-1 and TF-2 per AMD-26.

Actor provenance: software.software-engineer - S-2026-08-08-07.

metadata.reproducible.tokenizer_families declares:

- TF-1: byte-level BPE, tiktoken `cl100k_base` vocabulary; special tokens
  disabled ('measurement tokenises file text only; no special token is
  injected').
- TF-2: SentencePiece unigram, T5 `spiece.model` (32000 pieces); special
  tokens disabled.
- pin: 'the raw-octet SHA-256 of the [artifact], recorded in the
  budget_measurement member of core/MANIFEST.lock at the first authoritative
  Stage 6 measurement and verified against that record before every
  subsequent measurement'. Raw octets, never DC-1 (AMD-26: 'DC-1's text
  normalisation must never touch them').

FAIL-SAFE RULE (dispatch directive, consistent with tokenizer_families
.pin_value_rule / LAW-12): when the tokenizer packages or artifacts are not
in hand, the budget is reported UNMEASURED and no conforming lock is emitted.
Counts are never fabricated. This module exposes a single `TokenizerFamily`
protocol and a `probe()` that reports exactly what is missing.

Tokenizer wiring completed by software.platform-engineer - S-2026-08-08-08
(CMP-BLOCK-005 Stage 6 platform slice):

- Artifact custody: both artifacts live in the build-input area
  `build/stage6/tokenizer_artifacts/` (env override
  `AIEF_STAGE6_TOKENIZER_ARTIFACTS`); each family is assembled OFFLINE from
  the artifact in hand and its raw-octet SHA-256 pin is computed from that
  same file. A family whose artifact is absent stays unavailable - absence
  still blocks, never estimates.
- VER-004 FIND-Q4-1 (trust-on-first-use): when the sibling record
  `TRUST_ON_FIRST_USE.json` is present, the computed pin is checked against
  the corroborated hash recorded there at acquisition; a mismatch makes the
  family unavailable (loud halt, no silent re-pin).
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


class TokenizerFamily(Protocol):
    """One declared family. `count` measures file text only (special tokens
    disabled per tokenizer_families tf-1/tf-2 .special_tokens)."""

    family_id: str  # "TF-1" | "TF-2"
    artifact_name: str
    artifact_pin: str | None  # raw-octet SHA-256 of the artifact, if in hand

    def count(self, text: str) -> int: ...


@dataclass
class Tf1Tiktoken:
    """TF-1: 'byte-level BPE with the tiktoken cl100k_base vocabulary'
    (tokenizer_families.tf-1)."""

    encoding: object
    artifact_pin: str | None
    family_id: str = "TF-1"
    artifact_name: str = "cl100k_base.tiktoken"

    def count(self, text: str) -> int:
        # encode_ordinary: no special-token injection or interpretation -
        # tf-1.special_tokens 'disabled - measurement tokenises file text only'.
        return len(self.encoding.encode_ordinary(text))  # type: ignore[attr-defined]


@dataclass
class Tf2SentencePiece:
    """TF-2: 'SentencePiece unigram with the T5 spiece.model'
    (tokenizer_families.tf-2)."""

    processor: object
    artifact_pin: str | None
    family_id: str = "TF-2"
    artifact_name: str = "spiece.model"

    def count(self, text: str) -> int:
        # Plain EncodeAsIds over the text; no BOS/EOS or other special piece
        # is added - tf-2.special_tokens 'disabled'.
        return len(self.processor.encode(text, out_type=int))  # type: ignore[attr-defined]


@dataclass
class TokenizerProbe:
    """Result of attempting to assemble both declared families."""

    families: list[TokenizerFamily] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)

    @property
    def available(self) -> bool:
        return len(self.families) == 2 and not self.missing


def raw_octet_sha256(path: Path) -> str:
    """The AMD-26 pin: raw octets, no normalisation."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


#: Env override for the build-input artifact directory (test isolation and
#: alternative build layouts). Default: build/stage6/tokenizer_artifacts/
#: under the repository root - the gitignored build area.
ARTIFACT_DIR_ENV = "AIEF_STAGE6_TOKENIZER_ARTIFACTS"

#: The tf-1 'fixed pre-tokenisation pattern' (tokenizer_families.tf-1
#: .determinism). Transcribed verbatim from tiktoken_ext/openai_public.py
#: cl100k_base() as installed (tiktoken 0.13.0) and corroborated against the
#: upstream openai/tiktoken source; cross-checked by
#: tests/test_stage6_platform_tokenizers.py against the installed package so
#: drift is detected, not absorbed.
CL100K_PAT_STR = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}++|\p{N}{1,3}+| ?[^\s\p{L}\p{N}]++[\r\n]*+|\s++$|\s*[\r\n]|\s+(?!\S)|\s"""

#: FIND-Q4-1 custody record written at artifact acquisition, sibling to the
#: artifacts. Optional: on first use with no record the pin is computed from
#: the artifact in hand (pin_value_rule); with a record present, a mismatch
#: is a loud failure, never a silent re-pin.
TOFU_RECORD_NAME = "TRUST_ON_FIRST_USE.json"


def default_artifact_dir() -> Path:
    env = os.environ.get(ARTIFACT_DIR_ENV)
    if env:
        return Path(env)
    from .paths import find_repo_root

    return find_repo_root() / "build" / "stage6" / "tokenizer_artifacts"


def _check_tofu(artifact_dir: Path, artifact_name: str, computed_pin: str) -> None:
    """Verify the computed pin against the acquisition-time corroborated hash
    (VER-004 FIND-Q4-1) when that record exists."""
    record_path = artifact_dir / TOFU_RECORD_NAME
    if not record_path.is_file():
        return
    record = json.loads(record_path.read_text(encoding="utf-8"))
    entry = record.get("artifacts", {}).get(artifact_name)
    if entry is None:
        return
    expected = entry.get("sha256_raw_octets")
    if expected and expected != computed_pin:
        raise ValueError(
            f"{artifact_name}: raw-octet SHA-256 {computed_pin} does not match "
            f"the trust-on-first-use record {expected} ({TOFU_RECORD_NAME}) - "
            "artifact integrity failure, measurement refused"
        )


def _load_cl100k_ranks(path: Path) -> dict[bytes, int]:
    """Parse the .tiktoken vocabulary format (base64 token, rank per line)
    directly from the artifact in hand - offline, no cache, no network
    (tf-1.determinism: 'implementable offline from the pinned artifact
    alone')."""
    ranks: dict[bytes, int] = {}
    for line in path.read_bytes().splitlines():
        if not line:
            continue
        token, rank = line.split()
        ranks[base64.b64decode(token)] = int(rank)
    return ranks


def _assemble_tf1(artifact_dir: Path) -> Tf1Tiktoken:
    import tiktoken  # type: ignore[import-not-found]

    artifact = artifact_dir / "cl100k_base.tiktoken"
    if not artifact.is_file():
        raise FileNotFoundError(
            f"cl100k_base.tiktoken artifact not in hand at {artifact}"
        )
    pin = raw_octet_sha256(artifact)
    _check_tofu(artifact_dir, artifact.name, pin)
    encoding = tiktoken.Encoding(
        name="cl100k_base",
        pat_str=CL100K_PAT_STR,
        mergeable_ranks=_load_cl100k_ranks(artifact),
        # tf-1.special_tokens 'disabled': no special token is even defined;
        # counting additionally uses encode_ordinary.
        special_tokens={},
    )
    return Tf1Tiktoken(encoding=encoding, artifact_pin=pin)


def _assemble_tf2(artifact_dir: Path, spiece_model_path: Path | None) -> Tf2SentencePiece:
    import sentencepiece  # type: ignore[import-not-found]

    artifact = spiece_model_path or artifact_dir / "spiece.model"
    if not artifact.is_file():
        raise FileNotFoundError(
            f"spiece.model artifact not in hand at {artifact} (T5 SentencePiece model)"
        )
    pin = raw_octet_sha256(artifact)
    _check_tofu(artifact.parent, artifact.name, pin)
    processor = sentencepiece.SentencePieceProcessor(model_file=str(artifact))
    return Tf2SentencePiece(processor=processor, artifact_pin=pin)


def probe(spiece_model_path: Path | None = None,
          artifact_dir: Path | None = None) -> TokenizerProbe:
    """Assemble TF-1 and TF-2 if their packages and artifacts are in hand.

    Never substitutes an estimator (AMD-26 rejected alternatives E/F) and
    never asserts a pin it has not computed from the artifact in hand
    (tokenizer_families.pin_value_rule). Any assembly failure - package
    absent, artifact absent, FIND-Q4-1 hash mismatch - leaves that family
    unavailable and therefore blocks measurement (fail-safe).
    """
    result = TokenizerProbe()
    artifact_dir = artifact_dir or default_artifact_dir()

    try:
        result.families.append(_assemble_tf1(artifact_dir))
    except Exception as exc:
        result.missing.append(f"TF-1 unavailable: {exc.__class__.__name__}: {exc}")

    try:
        result.families.append(_assemble_tf2(artifact_dir, spiece_model_path))
    except Exception as exc:
        result.missing.append(f"TF-2 unavailable: {exc.__class__.__name__}: {exc}")

    return result
