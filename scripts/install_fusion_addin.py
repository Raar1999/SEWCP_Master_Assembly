"""Deploy the AIEF CAD Bridge add-in into Fusion's add-in directory.

The add-in source is version-controlled here; Fusion loads it from a
user-profile directory outside the repository. This script copies it there and
writes `bridge_config.json` naming this repository's bridge root, so a deployed
add-in always knows which repository it is serving and two checkouts cannot
quietly drive each other's models.

    python scripts/install_fusion_addin.py            # install or update
    python scripts/install_fusion_addin.py --status   # report, change nothing
    python scripts/install_fusion_addin.py --uninstall

Deploying writes **outside the repository**, into the user profile. That is
stated here rather than buried, because it is the one thing this repository
does that a `git clean` will not undo.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys
from pathlib import Path

ADDIN_NAME = "AIEF_CAD_Bridge"


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in here.parents:
        if (candidate / ".ai").is_dir() and (candidate / "src").is_dir():
            return candidate
    raise SystemExit("repository root not found from " + str(here))


def fusion_addins_dir() -> Path:
    system = platform.system()
    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise SystemExit("APPDATA is not set; cannot locate the Fusion add-in directory")
        return Path(appdata) / "Autodesk" / "Autodesk Fusion 360" / "API" / "AddIns"
    if system == "Darwin":
        return (Path.home() / "Library" / "Application Support" / "Autodesk"
                / "Autodesk Fusion 360" / "API" / "AddIns")
    raise SystemExit(
        f"unsupported platform {system!r}: Fusion 360 runs on Windows and macOS only"
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--status", action="store_true", help="report and change nothing")
    ap.add_argument("--uninstall", action="store_true", help="remove the deployed add-in")
    args = ap.parse_args(argv)

    root = repo_root()
    source = root / "fusion_addin" / ADDIN_NAME
    addins = fusion_addins_dir()
    target = addins / ADDIN_NAME
    bridge_root = root / "cad" / "bridge"

    if args.status:
        print(f"repository      {root}")
        print(f"add-in source   {source}  {'present' if source.is_dir() else 'MISSING'}")
        print(f"Fusion AddIns   {addins}  {'present' if addins.is_dir() else 'MISSING'}")
        print(f"deployed        {target}  {'yes' if target.is_dir() else 'no'}")
        cfg = target / "bridge_config.json"
        if cfg.is_file():
            served = json.loads(cfg.read_text(encoding="utf-8")).get("bridge_root")
            print(f"serving         {served}")
            if Path(served) != bridge_root:
                print("  WARNING: the deployed add-in serves a different repository")
        print(f"bridge root     {bridge_root}  {'present' if bridge_root.is_dir() else 'absent'}")
        hb = bridge_root / "state" / "addin.heartbeat.json"
        print(f"heartbeat       {'present' if hb.is_file() else 'absent'}")
        return 0

    if args.uninstall:
        if target.is_dir():
            shutil.rmtree(target)
            print(f"removed {target}")
        else:
            print(f"nothing to remove at {target}")
        return 0

    if not source.is_dir():
        raise SystemExit(f"add-in source not found at {source}")
    if not addins.is_dir():
        addins.mkdir(parents=True, exist_ok=True)
        print(f"created {addins}")

    if target.is_dir():
        shutil.rmtree(target)
    shutil.copytree(source, target)

    for d in ("queue", "obs", "state"):
        (bridge_root / d).mkdir(parents=True, exist_ok=True)

    (target / "bridge_config.json").write_text(
        json.dumps({"bridge_root": str(bridge_root), "repository": str(root)}, indent=2)
        + "\n",
        encoding="utf-8",
    )

    print(f"installed {ADDIN_NAME} -> {target}")
    print(f"serving   {bridge_root}")
    print()
    print("In Fusion 360: Utilities > ADD-INS > Scripts and Add-Ins > Add-Ins tab")
    print(f"               select {ADDIN_NAME} > Run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
