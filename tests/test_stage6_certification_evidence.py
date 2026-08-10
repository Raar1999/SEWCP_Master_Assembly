"""Certification tests: independent recomputation of the Stage 6 builders'
claimed evidence values against the REAL repository tree.

Actor provenance: software.test-engineer - S-2026-08-08-09 (independent
verification; author of no code under test).

METHOD: everything in this module is recomputed from first principles -
DC-1 normalisation, the AMD-39 covered-set procedure, DC-4, the raw-octet
artifact pins, and the V-09 dual-family measurement are all re-implemented
HERE, in the test, from the normative texts, without importing the
`aief_stage6` package. Agreement with the builders' recorded numbers is then
evidence of independent reproduction, not self-confirmation. The TF-1
pre-tokenisation pattern is extracted from the installed tiktoken
distribution's own source (not from the implementation's transcription).

Read-only with respect to the repository: nothing is written anywhere.
"""

import ast
import hashlib
import inspect
import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = REPO_ROOT / "build" / "stage6" / "tokenizer_artifacts"

# ------------------------- builders' claimed values -----------------------
CLAIMED_TF1_PIN = "223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7"
CLAIMED_TF2_PIN = "d60acb128cf7b7f2536e8f38a5b18a05535c9e14c7a355904270e15b0945ea86"
CLAIMED_DC4 = "2180df021b892ee0c19d7bc164713e46b1003bfb193497cad06b6c20f5ac92f0"
CLAIMED_COVERED_COUNT = 75

# NO TOKEN COUNT IS PINNED AS A CLAIMED VALUE HERE, BY RULING.
#
# This module previously pinned the S-2026-08-08-08 measurement as constants:
#   CLAIMED_TOTALS   = {"TF-1": 10296, "TF-2": 12657}
#   CLAIMED_BREACHES = BOOT.md 504 > cap 400; project/STATE.md 1791 > 1100;
#                      project/OPEN_ITEMS.md 7937 > 600
# AIEF-AMD-013 AMD-42 measurement_instant rules those are not constants: 'the
# record is a measurement of the tree as it stands at the instant of the
# build ... Measured entries of partition project carry mutability mutable ...
# so their counts move between builds by design. A later re-measurement that
# disagrees with a recorded one is expected drift, not a measurement defect -
# the recorded numbers are evidence about one build.' Re-pinning the current
# numbers would reproduce the same defect one revision later, so
# TestV09Recomputation asserts the V-09 PROPERTIES instead of a snapshot.
#
# The three breaches were cured by AIEF-AMD-014 AMD-50 (BOOT.md cap amended to
# the measurement, now 504) and AMD-49 (both registers became bounded
# indexes); AMD-52 disposes CMP-BLOCK-006 with 'V-09 passes'. The superseded
# numbers survive here as a comment - evidence about a past build, not an
# assertion about this one.

# files[manifest-lock].path. AMD-45: 'the deferral is keyed on the path
# core/MANIFEST.lock and on nothing else'.
LOCK_PATH = "core/MANIFEST.lock"
AGGREGATE_CEILING = 6000  # version.boot_ceiling_tokens; V-09 'at most 6000'

needs_artifacts = pytest.mark.skipif(
    not (ARTIFACT_DIR / "cl100k_base.tiktoken").is_file()
    or not (ARTIFACT_DIR / "spiece.model").is_file(),
    reason="tokenizer artifacts not provisioned",
)


# ------------------- independent re-implementations -----------------------

def ind_dc1(raw: bytes) -> str:
    """DC-1 re-implemented from digest_constructions.per_artifact."""
    text = raw.decode("utf-8")
    if text.startswith("﻿"):
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    normal = ("\n".join(lines) + "\n").encode("utf-8") if lines else b""
    return hashlib.sha256(normal).hexdigest()


def load_manifest_data() -> dict:
    return json.loads(
        (REPO_ROOT / "framework" / "framework.manifest.json").read_text(
            encoding="utf-8"
        )
    )


def load_binding_fields() -> tuple[str, list[str]]:
    """active_profile and enabled_agents parsed directly from BINDING.md."""
    text = (REPO_ROOT / ".ai" / "project" / "BINDING.md").read_text(
        encoding="utf-8"
    )
    profile = re.search(r"^active_profile:\s*(\S+)", text, re.M).group(1)
    tokens = re.findall(r"^\s{2}-\s*(\S+)", text, re.M)
    return profile, tokens


def independent_covered_pairs() -> list[tuple[str, str]]:
    """The AMD-39 machine-followable procedure, re-implemented verbatim."""
    manifest = load_manifest_data()
    selected, enabled = load_binding_fields()
    files = manifest["files"]
    by_path = {f["path"]: f for f in files}

    covered: dict[str, dict] = {}
    for f in files:
        p = f["path"]
        if f.get("integrity") != "hashed" or p == "core/MANIFEST.lock":
            continue
        if (
            p in ("BOOT.md", "FRAMEWORK.md", "README.md")
            or (p.startswith("core/") and not p.startswith("core/profiles/"))
            or p.startswith(f"core/profiles/{selected}/")
        ):
            covered[p] = f
    for t in enabled:
        if "." not in t:
            continue
        prof, name = t.split(".", 1)
        if prof == selected:
            continue
        target = f"core/profiles/{prof}/agents/AGT-{name}.md"
        entry = by_path.get(target)
        assert entry is not None and entry.get("integrity") == "hashed", (
            f"coverage defect: {t} -> {target}"
        )
        covered[target] = entry

    pairs = []
    for p in sorted(covered, key=lambda s: s.encode("utf-8")):
        fs = REPO_ROOT / ".ai" / Path(p)
        assert fs.is_file(), f"covered file absent from tree: {p}"
        pairs.append((p, ind_dc1(fs.read_bytes())))
    return pairs


# --------------------------------------------------------------------------
# TRUST_ON_FIRST_USE: raw-octet pins recomputed.
# --------------------------------------------------------------------------

class TestArtifactPins:
    @needs_artifacts
    def test_tf1_pin_recomputed(self):
        raw = (ARTIFACT_DIR / "cl100k_base.tiktoken").read_bytes()
        assert hashlib.sha256(raw).hexdigest() == CLAIMED_TF1_PIN

    @needs_artifacts
    def test_tf2_pin_recomputed(self):
        raw = (ARTIFACT_DIR / "spiece.model").read_bytes()
        assert hashlib.sha256(raw).hexdigest() == CLAIMED_TF2_PIN

    @needs_artifacts
    def test_tofu_record_internally_consistent(self):
        record = json.loads(
            (ARTIFACT_DIR / "TRUST_ON_FIRST_USE.json").read_text(encoding="utf-8")
        )
        arts = record["artifacts"]
        assert arts["cl100k_base.tiktoken"]["sha256_raw_octets"] == CLAIMED_TF1_PIN
        assert arts["spiece.model"]["sha256_raw_octets"] == CLAIMED_TF2_PIN
        for name in ("cl100k_base.tiktoken", "spiece.model"):
            assert arts[name]["size_octets"] == (ARTIFACT_DIR / name).stat().st_size


# --------------------------------------------------------------------------
# DC-4 preview aggregate over the real tree, recomputed independently.
# --------------------------------------------------------------------------

class TestDc4Aggregate:
    def test_covered_count_and_aggregate(self):
        pairs = independent_covered_pairs()
        assert len(pairs) == CLAIMED_COVERED_COUNT
        preimage = b"".join(
            p.encode("utf-8") + b" " + d.encode("ascii") + b"\n" for p, d in pairs
        )
        assert hashlib.sha256(preimage).hexdigest() == CLAIMED_DC4

    def test_three_enabled_software_artifacts_are_covered(self):
        # AMD-012's own statement of effect for this instance: exactly the
        # three software.* agent artifacts enter via term (ii).
        paths = {p for p, _ in independent_covered_pairs()}
        assert {
            "core/profiles/software/agents/AGT-software-engineer.md",
            "core/profiles/software/agents/AGT-test-engineer.md",
            "core/profiles/software/agents/AGT-platform-engineer.md",
        } <= paths
        # and no non-agent software-profile artifact is covered (scope_limit)
        assert not any(
            p.startswith("core/profiles/software/") and "/agents/" not in p
            for p in paths
        )

    def test_lock_and_unhashed_partitions_absent(self):
        paths = {p for p, _ in independent_covered_pairs()}
        assert "core/MANIFEST.lock" not in paths
        assert not any(p.startswith(("project/", "adapters/")) for p in paths)


# --------------------------------------------------------------------------
# V-09: dual-family measurement recomputed with independently assembled
# tokenizers over the real capped T0/T1 set.
# --------------------------------------------------------------------------

def assemble_tf1_independent():
    import tiktoken
    import tiktoken_ext.openai_public as op

    # Extract the published pre-tokenisation pattern from the installed
    # distribution's own source text (no call, no network).
    src = inspect.getsource(op.cl100k_base)
    line = next(l for l in src.splitlines() if '"pat_str"' in l)
    pat_str = ast.literal_eval(line.split(":", 1)[1].strip().rstrip(","))

    ranks = {}
    for raw_line in (ARTIFACT_DIR / "cl100k_base.tiktoken").read_bytes().splitlines():
        if raw_line:
            tok, rank = raw_line.split()
            import base64
            ranks[base64.b64decode(tok)] = int(rank)
    return tiktoken.Encoding(
        name="cert-cl100k", pat_str=pat_str, mergeable_ranks=ranks,
        special_tokens={},
    )


def assemble_tf2_independent():
    import sentencepiece

    return sentencepiece.SentencePieceProcessor(
        model_file=str(ARTIFACT_DIR / "spiece.model")
    )


@pytest.fixture(scope="module")
def families():
    return assemble_tf1_independent(), assemble_tf2_independent()


@pytest.fixture(scope="module")
def measurements(families):
    tf1, tf2 = families
    manifest = load_manifest_data()
    capped = [
        f for f in manifest["files"]
        if f.get("tier") in ("T0", "T1") and f.get("token_cap") is not None
    ]
    rows = {}
    totals = {"TF-1": 0, "TF-2": 0}
    charge = 0
    missing = []
    for f in capped:
        path = f["path"]
        if path == LOCK_PATH:
            # AMD-45, re-implemented from the ruling: the deferral is keyed on
            # THIS PATH and on nothing else - never on absence from the tree.
            # AMD-51: the deferred row still charges its declared cap.
            rows[path] = None
            charge = f["token_cap"]
            continue
        fs = REPO_ROOT / ".ai" / Path(path)
        if not fs.is_file():
            # AMD-45: 'any other measured file absent from the tree is a build
            # defect that must halt rather than defer'.
            missing.append(path)
            continue
        text = fs.read_text(encoding="utf-8")
        c1 = len(tf1.encode_ordinary(text))
        c2 = len(tf2.encode(text, out_type=int))
        rows[path] = {"cap": f["token_cap"], "TF-1": c1, "TF-2": c2,
                      "governing": max(c1, c2)}
        totals["TF-1"] += c1
        totals["TF-2"] += c2
    charged = {fam: n + charge for fam, n in totals.items()}
    return rows, totals, charged, charge, missing


@needs_artifacts
class TestV09Recomputation:

    def test_every_measured_file_is_present_or_the_lock(self, measurements):
        # AMD-45: only core/MANIFEST.lock may be absent from the measured
        # domain without halting, and it is excluded by its PATH. Any other
        # capped T0/T1 file missing from the tree is a build defect.
        _, _, _, _, missing = measurements
        assert missing == [], f"measured files absent from the tree: {missing}"

    def test_lock_row_is_deferred_by_path(self, measurements):
        # Keyed on the path and on nothing else: the row is deferred whether
        # or not an on-tree copy exists.
        rows, _, _, charge, _ = measurements
        assert LOCK_PATH in rows and rows[LOCK_PATH] is None
        assert charge == 200  # files[manifest-lock].token_cap

    def test_no_per_file_cap_breach(self, measurements):
        # V-09 property: 'per-file caps respected ... under both tokenizer
        # families ... the maximum governs'. AMD-52 disposes CMP-BLOCK-006
        # with 'V-09 passes: every per-file cap is respected under both
        # declared families'. Asserted as the property, not as a snapshot.
        rows, _, _, _, _ = measurements
        breaches = {
            p: (r["governing"], r["cap"])
            for p, r in rows.items()
            if r is not None and r["governing"] > r["cap"]
        }
        assert breaches == {}, f"per-file cap breaches: {breaches}"

    def test_governing_is_the_family_maximum(self, measurements):
        # tokenizer_families.governing_rule: 'the maximum governs'.
        rows, _, _, _, _ = measurements
        for path, r in rows.items():
            if r is None:
                continue
            assert r["governing"] == max(r["TF-1"], r["TF-2"]), path

    def test_charged_aggregate_within_ceiling_under_both_families(
        self, measurements
    ):
        # AMD-51: 'whenever the lock's row is DEFERRED-SELF-MEASURED the
        # aggregate ceiling comparison adds files[manifest-lock] token_cap to
        # each per-family total before comparing to the 6000 ceiling'. The
        # ASSERTED quantity is the relation, not either total.
        _, totals, charged, charge, _ = measurements
        assert charged == {f: totals[f] + charge for f in totals}
        for fam, n in charged.items():
            assert n <= AGGREGATE_CEILING, (
                f"{fam}: charged aggregate {n} (measured {totals[fam]} + lock "
                f"charge {charge}) exceeds the {AGGREGATE_CEILING} ceiling"
            )

    def test_the_charge_is_load_bearing_not_decorative(self, measurements):
        # FIND-Q7-3 was that the un-charged comparison can pass where the
        # charged one would not. Assert the charge is actually applied, i.e.
        # the compared value strictly exceeds the measured value.
        _, totals, charged, charge, _ = measurements
        assert charge > 0
        assert max(charged.values()) == max(totals.values()) + charge


# --------------------------------------------------------------------------
# Driver evidence coherence: the two recorded determinism runs.
# --------------------------------------------------------------------------

class TestDetcheckEvidence:
    def test_two_execution_summaries_identical(self):
        d = REPO_ROOT / "build" / "stage6" / "detcheck"
        if not d.is_dir():
            pytest.skip("detcheck evidence not present")
        s1 = (d / "exec1.summary.json").read_bytes()
        s2 = (d / "exec2.summary.json").read_bytes()
        assert s1 == s2, "the two build executions diverged"
        summary = json.loads(s1)
        assert summary["dc4_aggregate"] == CLAIMED_DC4
        assert summary["covered_count"] == CLAIMED_COVERED_COUNT
        assert summary["status"] == "PRECONDITION-FAIL"  # V-09 FAIL, honest halt
        by_id = {c["id"]: c["status"] for c in summary["preconditions"]}
        assert by_id.pop("V-09") == "FAIL"
        assert set(by_id) == {
            "V-01", "V-02", "V-03", "V-04", "V-05", "V-06", "V-07", "V-08",
            "V-23", "V-24", "V-25",
        }
        assert all(v == "PASS" for v in by_id.values())
