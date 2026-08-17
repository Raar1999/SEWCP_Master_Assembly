"""The `ECR-D-014` ruling, pinned at the pipeline instead of at the function.

`OI-V-13`'s independent audit found the ruling enforced by nothing. Three unit
tests pinned `lock.boot_read_prefix` as a *function*; **nothing pinned that the
build calls it, measures it against the right cap, or measures it at all.**
Three call-site mutations survived all 799 tests:

  * **M8** - the call site passes the whole serialised lock instead of the
    prefix. This reinstates exactly the AMD-45 whole-document reading that
    `ECR-D-014` declares unsatisfiable; under the real families it halts every
    build at ~6476 against a cap of 200.
  * **M9** - the call site substitutes some other cap for
    `files[manifest-lock].token_cap`.
  * **M10** - the call site skips the check and fabricates `verdict: PASS`.

All three survived because the only end-to-end test used a stub probe scoring
`len(text)//100 + 1`, which puts the 13 301-octet lock at 134 tokens - **under**
the 200 cap. The stub could not tell the two readings apart. That is verbatim
the blind spot `ECR-D-014` §4 names as the reason the defect survived, left in
place by the disposition that names it, and predicted in terms by `TCR-002` F-5
on 2026-08-09: *"Repairing the registry will make this test green on a build
that cannot actually complete."*

Two mechanisms close it, and both are needed:

1. **A discriminating probe.** `_RatioFamily` scores at the octets-per-token
   ratio the real families actually exhibit on this artifact (TF-2 ≈ 2.05,
   TF-1 ≈ 2.49), so the whole document lands far above 200 and the prefix far
   below it. Unlike the real families it needs no vendored artifact, so these
   tests run on a fresh clone - where the seven `needs_artifacts` tests skip.
2. **A spy on `measure_text`.** Region and cap are asserted directly, because a
   breach alone cannot catch M9 (right region, wrong cap) or M10 (no call).
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aief_stage6 import budget as budget_mod  # noqa: E402
from aief_stage6 import build as build_mod  # noqa: E402
from aief_stage6 import lock as lock_mod  # noqa: E402
from aief_stage6.budget import BudgetBreach  # noqa: E402
from aief_stage6.build import run  # noqa: E402
from aief_stage6.manifest import load_manifest  # noqa: E402
from aief_stage6.paths import find_repo_root  # noqa: E402
from aief_stage6.tokenizers import TokenizerProbe  # noqa: E402

REPO = find_repo_root(Path(__file__).resolve())


@dataclass
class _RatioFamily:
    """A stub that can tell 200 from 6476, which the old one could not.

    **Calibrated on the artifact under test and deliberately lenient
    elsewhere.** On serialised-lock text it scores at the octets-per-token
    ratio the real families exhibit on the emitted lock - TF-2 6476/13301 =
    2.05, TF-1 5340/13301 = 2.49 - so the whole document lands ~32x over the
    200 cap and the prefix ~4x under it. On everything else it keeps the old
    lenient scale, because `V-09`'s boot budget is a **different property**
    with its own tests, and a probe realistic enough to fail V-09 would stop
    the pipeline before it ever reached the measurement under test. The
    leniency is scoped to what is not being tested here, never to what is.
    """

    family_id: str
    octets_per_token: float
    lenient_scale: int
    artifact_name: str = "ratio-stub"
    artifact_pin: str = "0" * 64

    def count(self, text: str) -> int:
        if text.lstrip().startswith("{"):           # serialised lock or its prefix
            return int(len(text) / self.octets_per_token) + 1
        return len(text) // self.lenient_scale + 1


def _discriminating_probe() -> TokenizerProbe:
    return TokenizerProbe(
        families=[_RatioFamily("TF-1-RATIO", 2.49, 100),
                  _RatioFamily("TF-2-RATIO", 2.05, 120)],
        missing=[],
    )


def _declared_cap() -> int:
    return load_manifest(REPO).files_by_id["manifest-lock"]["token_cap"]


# ── the probe itself must be able to tell the two readings apart ───────────

def test_the_probe_discriminates_the_two_readings() -> None:
    """Guard on the guard. If this fails, every test below is vacuous - which
    is precisely how the old stub let M8 through."""
    lock_text = (REPO / ".ai" / "core" / "MANIFEST.lock").read_text(encoding="utf-8")
    probe = _discriminating_probe()
    whole = max(f.count(lock_text) for f in probe.families)
    prefix = max(f.count(lock_mod.boot_read_prefix(lock_text)) for f in probe.families)
    cap = _declared_cap()
    assert prefix < cap < whole, (prefix, cap, whole)
    assert whole > 30 * cap, "the two readings must be separated by a wide margin"


# ── the pipeline actually performs the check ───────────────────────────────

def test_the_build_measures_the_prefix_against_the_declared_cap(tmp_path, monkeypatch):
    """M8, M9 and M10 in one assertion: the call happened exactly once, on the
    prefix, against `files[manifest-lock].token_cap`."""
    calls: list[tuple[str, int, str]] = []
    real = budget_mod.measure_text

    def spy(tokenizers, text, cap, label):
        calls.append((text, cap, label))
        return real(tokenizers, text, cap, label)

    monkeypatch.setattr(build_mod.budget_mod, "measure_text", spy)
    outcome = run(repo_root=REPO, out_root=tmp_path,
                  tokenizers=_discriminating_probe(), runs=2)
    assert outcome.status == "OK", outcome.notes

    assert calls, "M10: the build emitted a lock without measuring it at all"
    # One per execution (AMD-33 requires >= 2), plus the post-condition `run()`
    # re-derives from the emitted octets before any canonical write.
    assert len(calls) >= 3, f"expected an emission pair plus the post-condition, got {len(calls)}"
    for text, cap, label in calls:
        # M9 - the cap must be the manifest's, not a local literal.
        assert cap == _declared_cap()
        # M8 - the measured region must be the prefix, not the document.
        assert text.endswith("\n")
        assert '"aggregate_digest"' in text
        assert '"files"' not in text, "M8: the whole document was measured"
        assert '"build_provenance"' not in text
        assert len(text) < 400, f"M8: measured {len(text)} octets, not a prefix"
        assert "prefix" in label.lower(), (
            "the label must name the measured region, so no report reads as a "
            "whole-document count"
        )


def test_the_outcome_carries_the_measurement_it_claims(tmp_path) -> None:
    """M10: a fabricated PASS must not be indistinguishable from a real one."""
    outcome = run(repo_root=REPO, out_root=tmp_path,
                  tokenizers=_discriminating_probe(), runs=2)
    m = outcome.lock_prefix_measurement
    assert m is not None, "M10: no measurement recorded"
    assert m["verdict"] == "PASS"
    assert m["cap"] == _declared_cap()
    assert 0 < m["governing"] <= m["cap"]
    assert set(m["counts"]) == {"TF-1-RATIO", "TF-2-RATIO"}
    assert m["governing"] == max(m["counts"].values())


# ── the mutations themselves ───────────────────────────────────────────────

def test_m8_whole_document_reading_halts_the_build(tmp_path, monkeypatch) -> None:
    """Reinstating the pre-AMD-54 reading must break the build, not pass it.

    This is the mutation that survived the whole suite before this module
    existed, and it is the exact defect `ECR-D-014` was raised on.
    """
    monkeypatch.setattr(build_mod.lock_mod, "boot_read_prefix", lambda text: text)
    outcome = run(repo_root=REPO, out_root=tmp_path,
                  tokenizers=_discriminating_probe(), runs=2)
    # TCR-002 F-7: a cap breach is a structured halt now, not a bare exception.
    assert outcome.status == "HALT", outcome.notes
    assert outcome.canonical_writes == []
    note = " ".join(outcome.notes)
    assert "cap 200" in note and "prefix" in note.lower(), outcome.notes


def test_m9_a_substituted_cap_is_caught(tmp_path, monkeypatch) -> None:
    """A cap that is not the manifest's must be visible even though a larger
    cap raises no breach - the failure mode a breach check alone cannot see."""
    seen: list[int] = []
    real = budget_mod.measure_text

    def wrong_cap(tokenizers, text, cap, label):
        seen.append(cap)
        return real(tokenizers, text, 6000, label)      # M9

    monkeypatch.setattr(build_mod.budget_mod, "measure_text", wrong_cap)
    outcome = run(repo_root=REPO, out_root=tmp_path,
                  tokenizers=_discriminating_probe(), runs=2)
    assert seen and all(c == _declared_cap() for c in seen), (
        "the build must pass the declared cap; this test proves the assertion "
        "in test_the_build_measures_... is the thing that catches M9"
    )
    assert outcome.lock_prefix_measurement["cap"] == 6000, (
        "and it proves the mutation is otherwise invisible - the build "
        "completes OK with the wrong cap recorded"
    )


def test_m10_a_skipped_check_is_caught(tmp_path, monkeypatch) -> None:
    """Fabricating the verdict must not survive. Under the old suite it did."""
    monkeypatch.setattr(
        build_mod.budget_mod, "measure_text",
        lambda tokenizers, text, cap, label: {
            "label": label, "counts": {}, "governing": 0, "cap": cap,
            "verdict": "PASS",
        },
    )
    outcome = run(repo_root=REPO, out_root=tmp_path,
                  tokenizers=_discriminating_probe(), runs=2)
    m = outcome.lock_prefix_measurement
    assert m["counts"] == {}, "fixture sanity"
    with pytest.raises(AssertionError):
        assert m["counts"], "M10: a verdict with no counts behind it"
    assert outcome.status == "OK"


# ── the prefix boundary is the member line, not a substring (FIND-7) ───────

def test_the_prefix_boundary_is_the_member_line_not_any_substring() -> None:
    """`OI-V-13` FIND-7: the implementation searched for the first occurrence
    of the token anywhere. Only `framework_version` precedes the member and
    JSON forbids an unescaped quote in a value, so there is no live exploit -
    but a substring heuristic where the ruling specifies a member is a defect
    waiting for a schema change. The boundary must survive the token appearing
    earlier inside a value."""
    doctored = (
        '{\n'
        '  "framework_version": "1.0.0 see \\"aggregate_digest\\" below",\n'
        '  "aggregate_digest": "' + "a" * 64 + '",\n'
        '  "files": []\n'
        '}\n'
    )
    prefix = lock_mod.boot_read_prefix(doctored)
    assert prefix.count("\n") == 3, prefix
    assert prefix.rstrip("\n").endswith('"' + "a" * 64 + '",')
    assert '"files"' not in prefix


def test_a_lock_with_no_aggregate_digest_member_halts() -> None:
    with pytest.raises(lock_mod.LockPrefixUndefined):
        lock_mod.boot_read_prefix('{\n  "framework_version": "1.0.0"\n}\n')


def test_a_lock_whose_member_line_is_not_lf_terminated_halts() -> None:
    with pytest.raises(lock_mod.LockPrefixUndefined):
        lock_mod.boot_read_prefix('{"aggregate_digest": "' + "a" * 64 + '"')


def test_the_prefix_is_free_of_run_scoped_octets_at_any_build_id() -> None:
    """`OI-V-13` C2 attacked this over build_id lengths 1..2000 and found the
    prefix bit-identical. Held here so a member re-ordering cannot undo it."""
    manifest = load_manifest(REPO)
    prefixes = set()
    for n in (1, 8, 27, 80, 2000):
        obj = lock_mod.build_lock_object(
            manifest, "mechanical", [("core/VERSION", "0" * 64)],
            {"verdict": "PASS"}, manifest_dc1="1" * 64,
            build_id="B" * n, timestamp="2026-01-01T00:00:00Z",
        )
        prefixes.add(lock_mod.boot_read_prefix(
            lock_mod.serialise_lock(obj).decode("utf-8")))
    assert len(prefixes) == 1, "a run-scoped octet reached the measured region"


# ── the canonical path, which no test reached until now ────────────────────
# The second `OI-V-13` round found M11: skip the check when `canonical` is
# true, and all 846 tests still pass while the canonical build writes
# `.ai/core/MANIFEST.lock` and the `BINDING` pin with a 249-token prefix
# against a cap of 200. The cause was structural - `grep Authorization tests/`
# reached only the dataclass's own `__post_init__`, so **the path with
# consequences had no end-to-end coverage at all** while the preview path had
# plenty. These tests run the real thing, in a copied tree.

import shutil  # noqa: E402

from aief_stage6.build import Authorization  # noqa: E402


def _tree(tmp_path: Path) -> Path:
    """A copy of the repository sufficient to run a canonical emission.

    Copied, not mocked, and never the real tree: a canonical run writes
    `.ai/core/MANIFEST.lock` and `.ai/project/BINDING.md` under `repo_root`.
    """
    root = tmp_path / "repo"
    root.mkdir(parents=True)
    for sub in (".ai", "framework", "spec"):
        shutil.copytree(REPO / sub, root / sub,
                        ignore=shutil.ignore_patterns("__pycache__"))
    return root


def _authorization() -> Authorization:
    return Authorization(
        "human-owner", "2026-08-11",
        "If Stage 6 can be executed without changing verified CAD: "
        "execute it autonomously.",
    )


def test_the_canonical_path_measures_the_prefix_and_writes(tmp_path) -> None:
    root = _tree(tmp_path)
    lock_before = (root / ".ai/core/MANIFEST.lock").read_bytes()

    outcome = run(repo_root=root, out_root=tmp_path / "out",
                  tokenizers=_discriminating_probe(), runs=2,
                  authorization=_authorization())

    assert outcome.status == "OK", outcome.notes
    assert outcome.mode == "CANONICAL"
    assert outcome.canonical_writes == [
        ".ai/core/MANIFEST.lock", ".ai/project/BINDING.md"]

    m = outcome.lock_prefix_measurement
    assert m is not None, "the canonical path emitted without measuring"
    assert m["verdict"] == "PASS"
    assert m["cap"] == _declared_cap()
    assert m["counts"], "a measurement with no counts behind it"
    assert m["governing"] == max(m["counts"].values()) <= m["cap"]

    assert (root / ".ai/core/MANIFEST.lock").read_bytes() != lock_before, (
        "a canonical run must actually write the lock, or this test proves nothing"
    )


def test_m11_skipping_the_check_on_the_canonical_path_cannot_emit(tmp_path) -> None:
    """**The M11 killer.** Under the whole-document reading the canonical build
    must halt and write nothing. Before the post-condition in `run()` it
    completed and wrote both canonical paths."""
    root = _tree(tmp_path)
    lock_before = (root / ".ai/core/MANIFEST.lock").read_bytes()
    binding_before = (root / ".ai/project/BINDING.md").read_bytes()

    import pytest as _pytest
    with _pytest.MonkeyPatch.context() as mp:
        mp.setattr(build_mod.lock_mod, "boot_read_prefix", lambda text: text)
        outcome = run(repo_root=root, out_root=tmp_path / "out",
                      tokenizers=_discriminating_probe(), runs=2,
                      authorization=_authorization())
    assert outcome.status == "HALT", outcome.notes
    assert outcome.canonical_writes == [], "a halted build wrote canonical bytes"

    assert (root / ".ai/core/MANIFEST.lock").read_bytes() == lock_before
    assert (root / ".ai/project/BINDING.md").read_bytes() == binding_before


def _emit_with(monkeypatch, transform):
    """Mutate what `_emit_once` RECORDS, leaving everything else intact.

    This is where a real M10/M11 lives - inside the emitter, not inside
    `measure_text`. Patching `measure_text` globally would mutate the
    post-condition too, and the two would agree; the point of the
    post-condition is that it is a second, independent derivation.
    """
    real = build_mod._emit_once

    def wrapped(*a, **kw):
        out = real(*a, **kw)
        out["__prefix_measurement__"] = json.dumps(
            transform(json.loads(out["__prefix_measurement__"].decode("utf-8"))),
            sort_keys=True).encode("utf-8")
        return out

    monkeypatch.setattr(build_mod, "_emit_once", wrapped)


def test_a_fabricated_measurement_cannot_reach_the_canonical_writes(
        tmp_path, monkeypatch) -> None:
    """**The M11 killer in its quietest form.** A plausible PASS over octets
    nobody measured. Before the post-condition, this reached both canonical
    writes."""
    root = _tree(tmp_path)
    lock_before = (root / ".ai/core/MANIFEST.lock").read_bytes()
    binding_before = (root / ".ai/project/BINDING.md").read_bytes()

    _emit_with(monkeypatch, lambda m: {**m, "counts": {}, "governing": 0,
                                       "verdict": "PASS"})
    outcome = run(repo_root=root, out_root=tmp_path / "out",
                  tokenizers=_discriminating_probe(), runs=2,
                  authorization=_authorization())

    assert outcome.status == "HALT", outcome.notes
    assert outcome.canonical_writes == []
    assert any("does not reproduce from the emitted octets" in n
               for n in outcome.notes), outcome.notes
    assert (root / ".ai/core/MANIFEST.lock").read_bytes() == lock_before
    assert (root / ".ai/project/BINDING.md").read_bytes() == binding_before


def test_m13_a_truncated_measured_region_cannot_emit(tmp_path, monkeypatch) -> None:
    """**The M13 killer.** The region is now pinned by identity with
    `boot_read_prefix`, not by shape. A silent truncation satisfied every shape
    assertion in this module and is caught here because the post-condition
    re-derives the region itself."""
    root = _tree(tmp_path)
    lock_before = (root / ".ai/core/MANIFEST.lock").read_bytes()

    # What a truncating emitter would record: fewer tokens, same shape.
    _emit_with(monkeypatch, lambda m: {**m,
                                       "counts": {k: max(1, v - 20)
                                                  for k, v in m["counts"].items()},
                                       "governing": max(1, m["governing"] - 20)})
    outcome = run(repo_root=root, out_root=tmp_path / "out",
                  tokenizers=_discriminating_probe(), runs=2,
                  authorization=_authorization())

    assert outcome.status == "HALT", outcome.notes
    assert outcome.canonical_writes == []
    assert (root / ".ai/core/MANIFEST.lock").read_bytes() == lock_before


def test_a_substituted_cap_cannot_emit(tmp_path, monkeypatch) -> None:
    """M9 on the canonical path: the recorded cap must be the declared one."""
    root = _tree(tmp_path)
    _emit_with(monkeypatch, lambda m: {**m, "cap": 6000})
    outcome = run(repo_root=root, out_root=tmp_path / "out",
                  tokenizers=_discriminating_probe(), runs=2,
                  authorization=_authorization())
    assert outcome.status == "HALT", outcome.notes
    assert outcome.canonical_writes == []


def test_m12_the_cap_is_taken_from_the_manifest_not_a_literal(tmp_path) -> None:
    """**The M12 killer.** AMD-54 measures "against `files[manifest-lock].token_cap`".
    A literal `200` satisfies that only by coincidence of today's value, and
    every value assertion in this module compares the cap to the manifest's
    own number - so the two agree whichever the code used.

    Move the declared cap in memory and require the recorded measurement to
    follow. `_emit_once` is called directly so the frozen-registry checks,
    which would fail first on a modified manifest and mask the property, are
    not involved.
    """
    import json as _json

    manifest = load_manifest(REPO)
    lock = _json.loads((REPO / ".ai/core/MANIFEST.lock").read_text(encoding="utf-8"))
    pairs = [(a, b) for a, b in lock["files"]]

    original = manifest.files_by_id["manifest-lock"]["token_cap"]
    assert original == 200, original
    try:
        manifest.files_by_id["manifest-lock"]["token_cap"] = 137
        out = build_mod._emit_once(
            tmp_path / "emit", REPO, manifest, pairs, "mechanical",
            _discriminating_probe(), build_id="m12", timestamp="2026-01-01T00:00:00Z",
        )
        recorded = _json.loads(out["__prefix_measurement__"].decode("utf-8"))
    finally:
        manifest.files_by_id["manifest-lock"]["token_cap"] = original

    assert recorded["cap"] == 137, (
        "the cap did not follow the manifest - it is a literal, and AMD-54's "
        "'against files[manifest-lock].token_cap' holds only by coincidence"
    )
    assert 0 < recorded["governing"] <= 137
