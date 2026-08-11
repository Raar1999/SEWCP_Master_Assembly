"""CLI entry: `python -m aief_stage6` runs the preview Stage 6 pipeline.

Actor provenance: software.software-engineer - S-2026-08-08-07.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .build import Authorization, run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="aief_stage6",
        description="AIEF Compiler Stage 6 increment (PREVIEW mode - no "
                    "canonical emission; outputs under build/stage6/).",
    )
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument("--out-root", type=Path, default=None)
    parser.add_argument("--spiece-model", type=Path, default=None,
                        help="path to the T5 spiece.model artifact (TF-2)")
    parser.add_argument("--runs", type=int, default=2,
                        help="build executions for AMD-33 (minimum 2)")
    parser.add_argument(
        "--authorize", nargs=3, metavar=("AUTHORITY", "RECORDED_AT", "INSTRUCTION"),
        default=None,
        help="CANONICAL mode. Present the OQ-14 record - who authorized, when "
             "(YYYY-MM-DD), and the authorizing instruction verbatim. Without "
             "it the build is preview-only and writes nothing outside "
             "build/stage6/.")
    args = parser.parse_args(argv)

    authorization = Authorization(*args.authorize) if args.authorize else None
    outcome = run(repo_root=args.repo_root, out_root=args.out_root,
                  spiece_model_path=args.spiece_model, runs=args.runs,
                  authorization=authorization)
    print(json.dumps({
        "mode": outcome.mode,
        "status": outcome.status,
        "covered_count": outcome.covered_count,
        "dc4_aggregate": outcome.dc4_aggregate,
        "dc5_release_digest": outcome.dc5_release_digest,
        "lock_prefix_measurement": outcome.lock_prefix_measurement,
        "max_archive_path_octets": outcome.max_archive_path_octets,
        "max_archive_path": outcome.max_archive_path,
        "canonical_writes": outcome.canonical_writes,
        "preconditions": [
            {"id": c["id"], "status": c["status"], "counts": c["counts"]}
            for c in outcome.preconditions
        ],
        "notes": outcome.notes,
    }, indent=2))
    return 0 if outcome.status == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
