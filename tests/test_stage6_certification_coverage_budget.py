"""Certification tests: DC-4 covered-set rule (AIEF-AMD-012 AMD-39) and the
budget measurement semantics (AMD-26/AMD-29, V-09).

Actor provenance: software.test-engineer - S-2026-08-08-09 (independent
verification; author of no code under test).

METHOD: expected behaviour is transcribed from the machine-followable
covered-set procedure of AIEF-AMD-012 and from
`metadata.reproducible.budget_measurement_record` / `tokenizer_families`.
All fixtures are synthetic (temp dirs); the repository tree is never
mutated. Fake tokenizer families are used so budget arithmetic is
spec-driven, not artifact-driven.
"""

import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aief_stage6.binding import Binding
from aief_stage6.budget import (
    AGGREGATE_CEILING,
    LOCK_DEFERRED_VERDICT,
    LOCK_PATH,
    BudgetBreach,
    BudgetSourceMissing,
    BudgetUnmeasured,
    measure,
    measure_text,
)
from aief_stage6.coverage import (
    CoverageDefect,
    hash_covered_set,
    resolve_covered_set,
)
from aief_stage6.manifest import Manifest
from aief_stage6.tokenizers import TokenizerProbe, probe

Z = "0" * 64


def make_manifest(files, semver="1.0.0"):
    return Manifest(
        path=Path("synthetic-manifest"),
        raw=b"{}",
        data={
            "version": {"semver": semver},
            "metadata": {
                "reproducible": {
                    "hash_algorithm": "SHA-256",
                    "normalisation": {"encoding": "UTF-8", "line_ending": "LF"},
                }
            },
            "files": files,
        },
    )


def make_binding(active_profile, enabled_agents):
    return Binding(
        path=Path("synthetic-binding"),
        text="core_digest_pin: PENDING-STAGE-6\n",
        core_digest_pin="PENDING-STAGE-6",
        active_profile=active_profile,
        enabled_agents=tuple(enabled_agents),
    )


def hashed(path, **kw):
    return {"id": path, "path": path, "integrity": "hashed", **kw}


def unhashed(path, **kw):
    return {"id": path, "path": path, "integrity": "none", **kw}


BASE_FILES = [
    hashed("BOOT.md"),
    hashed("FRAMEWORK.md"),
    hashed("README.md"),
    hashed("core/VERSION"),
    hashed("core/templates/TPL-x.md"),
    hashed("core/validation/CHECKS.md"),
    hashed("core/MANIFEST.lock"),                       # self-exclusion target
    hashed("core/profiles/mech/PROFILE.md"),            # selected profile
    hashed("core/profiles/mech/agents/AGT-a.md"),
    hashed("core/profiles/soft/agents/AGT-b.md"),       # non-selected profile
    hashed("core/profiles/soft/PROFILE.md"),            # non-selected, no token
    unhashed("adapters/ADP-x.md"),                      # unhashed partition
    unhashed("project/BINDING.md"),                     # unhashed partition
    hashed("project/HYPOTHETICAL.md"),                  # hashed but not emitted
]


# --------------------------------------------------------------------------
# AMD-39 term (i): hashed AND emitted for the selected profile.
# --------------------------------------------------------------------------

class TestCoveredSetTermOne:
    def test_baseline_covered_set(self):
        covered = resolve_covered_set(
            make_manifest(BASE_FILES), make_binding("mech", ["qa-engineer"])
        )
        assert covered.paths == (
            "BOOT.md",
            "FRAMEWORK.md",
            "README.md",
            "core/VERSION",
            "core/profiles/mech/PROFILE.md",
            "core/profiles/mech/agents/AGT-a.md",
            "core/templates/TPL-x.md",
            "core/validation/CHECKS.md",
        )

    def test_lock_self_exclusion(self):
        # core_aggregate.self_exclusion: 'core/MANIFEST.lock is not a member
        # of its own files list and contributes no record'.
        covered = resolve_covered_set(
            make_manifest(BASE_FILES), make_binding("mech", ["qa-engineer"])
        )
        assert "core/MANIFEST.lock" not in covered.paths

    def test_unhashed_partitions_never_covered(self):
        # covers: 'unhashed partitions (project, adapters) are never covered'.
        covered = resolve_covered_set(
            make_manifest(BASE_FILES), make_binding("mech", ["qa-engineer"])
        )
        assert not any(p.startswith(("adapters/", "project/")) for p in covered.paths)

    def test_hashed_but_not_emitted_for_selected_not_covered(self):
        # A hashed path outside the AMD-27 emission clause (project/**,
        # non-selected core/profiles/**) is not in term (i).
        covered = resolve_covered_set(
            make_manifest(BASE_FILES), make_binding("mech", ["qa-engineer"])
        )
        assert "project/HYPOTHETICAL.md" not in covered.paths
        assert "core/profiles/soft/agents/AGT-b.md" not in covered.paths
        assert "core/profiles/soft/PROFILE.md" not in covered.paths


# --------------------------------------------------------------------------
# AMD-39 term (ii): enabled-role agent artifacts.
# --------------------------------------------------------------------------

class TestCoveredSetTermTwo:
    def test_non_selected_profile_token_adds_agent_artifact(self):
        covered = resolve_covered_set(
            make_manifest(BASE_FILES), make_binding("mech", ["soft.b"])
        )
        assert "core/profiles/soft/agents/AGT-b.md" in covered.paths
        # scope_limit: 'agent artifacts only; PROFILE.md ... remain uncovered'
        assert "core/profiles/soft/PROFILE.md" not in covered.paths

    def test_undotted_token_adds_nothing(self):
        # AMD-39 point 2: universal token resolves under core/**, no new entry.
        one = resolve_covered_set(
            make_manifest(BASE_FILES), make_binding("mech", ["qa-engineer"])
        )
        two = resolve_covered_set(
            make_manifest(BASE_FILES),
            make_binding("mech", ["repository-engineer", "qa-engineer"]),
        )
        assert one.paths == two.paths

    def test_selected_profile_token_adds_nothing(self):
        # 'a token of the selected profile adds no entry - already covered'.
        a = resolve_covered_set(
            make_manifest(BASE_FILES), make_binding("mech", ["mech.a"])
        )
        b = resolve_covered_set(
            make_manifest(BASE_FILES), make_binding("mech", ["qa-engineer"])
        )
        assert a.paths == b.paths

    def test_unresolvable_token_halts(self):
        # enabled_role_coverage.rule: 'a token that resolves to no such entry
        # is a coverage defect that halts the build'.
        with pytest.raises(CoverageDefect):
            resolve_covered_set(
                make_manifest(BASE_FILES), make_binding("mech", ["soft.nonexistent"])
            )

    def test_token_resolving_to_unhashed_entry_halts(self):
        # rule: 'that entry must exist in files[] and be declared integrity
        # hashed' - existing-but-unhashed is equally a coverage defect.
        files = BASE_FILES + [unhashed("core/profiles/res/agents/AGT-c.md")]
        with pytest.raises(CoverageDefect):
            resolve_covered_set(
                make_manifest(files), make_binding("mech", ["res.c"])
            )

    def test_working_tree_is_never_an_input_to_coverage(self):
        # determinism: 'the covered set is a function of files[], the selected
        # profile and ... enabled_agents alone' - resolution succeeds with no
        # filesystem at all.
        covered = resolve_covered_set(
            make_manifest(BASE_FILES), make_binding("mech", ["soft.b"])
        )
        assert covered.paths  # resolved without any tree access


# --------------------------------------------------------------------------
# List-vs-tree discipline: hashing the covered set over a fixture tree.
# --------------------------------------------------------------------------

class TestHashCoveredSet:
    FILES = [hashed("BOOT.md"), hashed("core/VERSION")]

    def _fixture(self, tmp_path: Path, omit: str | None = None) -> Path:
        ai = tmp_path / ".ai"
        for name, content in (("BOOT.md", b"boot\n"), ("core/VERSION", b"1.0.0\n")):
            if name == omit:
                continue
            target = ai / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        return tmp_path

    def test_pairs_are_dc1_digests(self, tmp_path):
        root = self._fixture(tmp_path)
        covered = resolve_covered_set(
            make_manifest(self.FILES), make_binding("mech", ["qa-engineer"])
        )
        pairs = dict(hash_covered_set(covered, root))
        # Expected values computed here with hashlib over the DC-1 normal
        # form (content already normalised in the fixture).
        assert pairs["BOOT.md"] == hashlib.sha256(b"boot\n").hexdigest()
        assert pairs["core/VERSION"] == hashlib.sha256(b"1.0.0\n").hexdigest()

    def test_covered_file_absent_from_tree_halts(self, tmp_path):
        # enabled_role_coverage.determinism: 'an enabled-role artifact absent
        # from the tree is a B2a coverage failure, halting, never a silent
        # exclusion'; b2a_procedure: 'no covered-scope file is absent'.
        root = self._fixture(tmp_path, omit="core/VERSION")
        covered = resolve_covered_set(
            make_manifest(self.FILES), make_binding("mech", ["qa-engineer"])
        )
        with pytest.raises(CoverageDefect, match="core/VERSION"):
            hash_covered_set(covered, root)


# --------------------------------------------------------------------------
# Budget: maximum governs; verdicts; fail-safe.
# --------------------------------------------------------------------------

@dataclass
class FakeFamily:
    """Deterministic stand-in family: count = multiplier * character count.
    Lets the tests drive exact arithmetic without the real artifacts."""

    family_id: str
    multiplier: int
    artifact_name: str = "fake.artifact"
    artifact_pin: str = Z

    def count(self, text: str) -> int:
        return self.multiplier * len(text)


def fake_probe(m1=1, m2=2) -> TokenizerProbe:
    return TokenizerProbe(
        families=[FakeFamily("TF-1", m1), FakeFamily("TF-2", m2)], missing=[]
    )


def budget_fixture(tmp_path: Path, content: str = "abcde") -> Path:
    ai = tmp_path / ".ai"
    ai.mkdir()
    (ai / "BOOT.md").write_text(content, encoding="utf-8")
    return tmp_path


# files[manifest-lock] as the live manifest declares it (path, tier, cap).
LOCK_FILE_ENTRY = {"id": "manifest-lock", "path": LOCK_PATH, "tier": "T1",
                   "token_cap": 200, "integrity": "hashed"}


def capped_manifest(cap: int, tier: str = "T0", extra_files=()):
    files = [
        {"id": "boot", "path": "BOOT.md", "tier": tier, "token_cap": cap,
         "integrity": "hashed"},
        *extra_files,
    ]
    return make_manifest(files)


class TestBudget:
    def test_maximum_governs_per_file(self, tmp_path):
        # tokenizer_families.governing_rule: 'the maximum governs'. Content of
        # 5 chars: TF-1 counts 5, TF-2 counts 10. Cap 9 must FAIL on TF-2
        # even though TF-1 passes.
        root = budget_fixture(tmp_path)  # 5 characters
        with pytest.raises(BudgetBreach):
            measure(capped_manifest(9), root, fake_probe(),
                    build_id="b", timestamp="t")

    def test_cap_equal_to_governing_passes(self, tmp_path):
        # 'at most' semantics: governing == cap is a PASS, not a breach.
        root = budget_fixture(tmp_path)
        result = measure(capped_manifest(10), root, fake_probe(),
                         build_id="b", timestamp="t")
        rec = result.record
        assert rec["verdict"] == "PASS"
        (entry,) = [e for e in rec["per_file"] if e["path"] == "BOOT.md"]
        assert entry["counts"] == {"TF-1": 5, "TF-2": 10}
        assert entry["governing"] == 10
        assert entry["verdict"] == "PASS"

    def test_aggregate_ceiling_maximum_governs(self, tmp_path):
        # verdict_rule: 'any ... aggregate ceiling breach under either family
        # halts the build'. 3001 chars: TF-1 total 3001 (under 6000), TF-2
        # total 6002 (over) -> halt.
        root = budget_fixture(tmp_path, content="x" * 3001)
        assert AGGREGATE_CEILING == 6000  # V-09: 'at most 6000 tokens'
        with pytest.raises(BudgetBreach, match="aggregate"):
            measure(capped_manifest(100000), root, fake_probe(),
                    build_id="b", timestamp="t")

    def test_only_capped_t0_t1_files_measured(self, tmp_path):
        # budget_measurement_record.content: 'every file carrying a non-null
        # token_cap in tiers T0 and T1' - a T2 file and a null-capped file
        # contribute nothing.
        root = budget_fixture(tmp_path)
        (root / ".ai" / "T2.md").write_text("y" * 10000, encoding="utf-8")
        (root / ".ai" / "NOCAP.md").write_text("z" * 10000, encoding="utf-8")
        extra = (
            {"id": "t2", "path": "T2.md", "tier": "T2", "token_cap": 50,
             "integrity": "hashed"},
            {"id": "nocap", "path": "NOCAP.md", "tier": "T1", "token_cap": None,
             "integrity": "hashed"},
        )
        result = measure(capped_manifest(10, extra_files=extra), root,
                         fake_probe(), build_id="b", timestamp="t")
        measured = {e["path"] for e in result.record["per_file"]}
        assert measured == {"BOOT.md"}
        assert result.record["totals_t0_t1"] == {"TF-1": 5, "TF-2": 10}

    def test_record_carries_declared_content(self, tmp_path):
        # AMD-29 content list: counts per family, totals, governing maxima,
        # verdicts, artifact identifiers with raw-octet pins, timestamp and
        # build identifier.
        root = budget_fixture(tmp_path)
        rec = measure(capped_manifest(10), root, fake_probe(),
                      build_id="BUILD-X", timestamp="2026-08-08T00:00:00Z").record
        fams = {f["id"]: f for f in rec["tokenizer_families"]}
        assert set(fams) == {"TF-1", "TF-2"}
        for f in fams.values():
            assert f["artifact"] and f["artifact_pin_sha256_raw_octets"]
        assert rec["aggregate_governing_maximum"] == max(rec["totals_t0_t1"].values())
        assert rec["aggregate_ceiling"] == 6000
        assert rec["measurement_timestamp"] == "2026-08-08T00:00:00Z"
        assert rec["stage6_build_id"] == "BUILD-X"

    def test_failsafe_unavailable_family_raises_never_estimates(self, tmp_path):
        # Fail-safe: 'with no tokenizers in hand the record is UNMEASURED and
        # lock emission is refused ... counts are never fabricated'
        # (tokenizer_families.pin_value_rule / LAW-12 discipline).
        root = budget_fixture(tmp_path)
        one_family = TokenizerProbe(
            families=[FakeFamily("TF-1", 1)],
            missing=["TF-2 unavailable: artifact not in hand"],
        )
        with pytest.raises(BudgetUnmeasured):
            measure(capped_manifest(10), root, one_family,
                    build_id="b", timestamp="t")

    def test_probe_with_empty_artifact_dir_blocks(self, tmp_path):
        # End-to-end fail-safe: probing an empty artifact directory yields an
        # unavailable probe (absence blocks; nothing is fetched, nothing
        # estimated).
        empty = tmp_path / "no-artifacts"
        empty.mkdir()
        p = probe(artifact_dir=empty)
        assert not p.available
        assert len(p.missing) == 2  # both declared families reported missing

    # ---------------- AMD-45: the deferral is keyed on the path ------------
    # 'The deferral is keyed on the path core/MANIFEST.lock and on nothing
    # else - in particular never on absence from the tree, because any other
    # measured file absent from the tree is a build defect that must halt
    # rather than defer.' Disposes TCR-001 finding F1.

    def test_lock_row_defers_on_its_path_even_when_present(self, tmp_path):
        # Keyed on the path: an on-tree copy of core/MANIFEST.lock changes
        # nothing. Were the key still absence, this row would be measured.
        root = budget_fixture(tmp_path)
        (root / ".ai" / "core").mkdir()
        (root / ".ai" / "core" / "MANIFEST.lock").write_text(
            "x" * 10000, encoding="utf-8"
        )
        rec = measure(capped_manifest(10, extra_files=(LOCK_FILE_ENTRY,)), root,
                      fake_probe(), build_id="b", timestamp="t").record
        (row,) = [e for e in rec["per_file"] if e["path"] == LOCK_PATH]
        assert row["verdict"] == LOCK_DEFERRED_VERDICT
        assert row["counts"] is None and row["governing"] is None
        # ...and the 10000-char on-tree text contributed nothing measured.
        assert rec["totals_t0_t1"] == {"TF-1": 5, "TF-2": 10}

    def test_lock_row_defers_on_its_path_when_absent(self, tmp_path):
        root = budget_fixture(tmp_path)  # no core/MANIFEST.lock on disk
        rec = measure(capped_manifest(10, extra_files=(LOCK_FILE_ENTRY,)), root,
                      fake_probe(), build_id="b", timestamp="t").record
        (row,) = [e for e in rec["per_file"] if e["path"] == LOCK_PATH]
        assert row["verdict"] == LOCK_DEFERRED_VERDICT

    def test_other_measured_file_absent_from_tree_halts(self, tmp_path):
        # AC-1 / TCR-001 F1: the fail-open. Before AMD-45 this deferred.
        root = budget_fixture(tmp_path)
        extra = ({"id": "gone", "path": "GONE.md", "tier": "T1",
                  "token_cap": 100, "integrity": "hashed"},)
        with pytest.raises(BudgetSourceMissing, match="GONE.md"):
            measure(capped_manifest(10, extra_files=extra), root, fake_probe(),
                    build_id="b", timestamp="t")

    def test_deleted_measured_file_halts_and_never_defers(self, tmp_path):
        # The concrete F1 scenario: a capped file deleted from the tree.
        root = budget_fixture(tmp_path)
        (root / ".ai" / "BOOT.md").unlink()
        with pytest.raises(BudgetSourceMissing, match="BOOT.md"):
            measure(capped_manifest(10), root, fake_probe(),
                    build_id="b", timestamp="t")

    # ------------- AMD-51: the lock cap is charged to the totals -----------
    # 'whenever the lock's row is DEFERRED-SELF-MEASURED the aggregate ceiling
    # comparison adds files[manifest-lock] token_cap to each per-family total
    # before comparing to the 6000 ceiling. The charge is the declared cap,
    # never an estimate.'

    def test_lock_cap_charged_to_every_family_total(self, tmp_path):
        root = budget_fixture(tmp_path)  # measured 5 / 10
        rec = measure(capped_manifest(10, extra_files=(LOCK_FILE_ENTRY,)), root,
                      fake_probe(), build_id="b", timestamp="t").record
        assert rec["aggregate_ceiling_charge"] == 200  # the declared cap
        assert rec["totals_t0_t1"] == {"TF-1": 5, "TF-2": 10}
        assert rec["charged_totals_t0_t1"] == {"TF-1": 205, "TF-2": 210}
        # The compared value is the charged maximum, not the measured one.
        assert rec["aggregate_governing_maximum"] == 210

    def test_no_charge_when_no_deferred_lock_row(self, tmp_path):
        # 'whenever the lock's row is DEFERRED-SELF-MEASURED' - and only then.
        root = budget_fixture(tmp_path)
        rec = measure(capped_manifest(10), root, fake_probe(),
                      build_id="b", timestamp="t").record
        assert rec["aggregate_ceiling_charge"] == 0
        assert rec["charged_totals_t0_t1"] == rec["totals_t0_t1"]

    def test_charge_can_turn_a_passing_aggregate_into_a_halt(self, tmp_path):
        # VER-007 FIND-Q7-3: 'a conforming build can report an aggregate of
        # 6000 - PASS - while the true capped T0 union T1 cost is up to 6200'.
        # 2999 chars: measured TF-2 5998 <= 6000 (would PASS un-charged);
        # charged 6198 > 6000 must halt.
        root = budget_fixture(tmp_path, content="x" * 2999)
        assert measure(capped_manifest(100000), root, fake_probe(),
                       build_id="b", timestamp="t").record["verdict"] == "PASS"
        with pytest.raises(BudgetBreach, match="lock charge 200"):
            measure(capped_manifest(100000, extra_files=(LOCK_FILE_ENTRY,)),
                    root, fake_probe(), build_id="b", timestamp="t")

    def test_charge_is_the_declared_cap_never_an_estimate(self, tmp_path):
        # The charge tracks files[manifest-lock].token_cap, whatever it says.
        root = budget_fixture(tmp_path)
        entry = dict(LOCK_FILE_ENTRY, token_cap=350)
        rec = measure(capped_manifest(10, extra_files=(entry,)), root,
                      fake_probe(), build_id="b", timestamp="t").record
        assert rec["aggregate_ceiling_charge"] == 350
        assert rec["charged_totals_t0_t1"] == {"TF-1": 355, "TF-2": 360}

    def test_measure_text_halts_on_breach(self):
        # Post-emission lock cap check follows the same verdict_rule.
        with pytest.raises(BudgetBreach):
            measure_text(fake_probe(), "x" * 300, 200, "core/MANIFEST.lock")
        assert measure_text(fake_probe(), "x" * 100, 200, "lock")["verdict"] == "PASS"
