#!/usr/bin/env python3
"""Install the bundled Flyw plugin into a local agent plugins directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent
PLUGIN_SOURCE = REPOSITORY_ROOT / "flyw"
DEFAULT_TARGET = Path.home() / ".gemini" / "config" / "plugins"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the bundled plugin without requiring Python dependencies."
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=DEFAULT_TARGET,
        help=f"Plugin directory parent (default: {DEFAULT_TARGET})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing installed plugin.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be installed without changing files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    destination = args.target_dir.expanduser() / PLUGIN_SOURCE.name

    if not PLUGIN_SOURCE.is_dir():
        raise SystemExit(f"Plugin source does not exist: {PLUGIN_SOURCE}")

    if destination.exists() and not args.force:
        raise SystemExit(
            f"Destination already exists: {destination}\n"
            "Use --force to replace it."
        )

    print(f"source:      {PLUGIN_SOURCE}")
    print(f"destination: {destination}")

    if args.dry_run:
        print("dry run: no files changed")
        return 0

    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(PLUGIN_SOURCE, destination)
    print("installed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
