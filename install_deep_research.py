#!/usr/bin/env python3
"""Download Weizhena's Deep-Research-skills repository."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent
SOURCE_URL = "https://github.com/Weizhena/Deep-Research-skills"
INSTALL_NAME = "DeepResearch"
SKILLS_VARIANT = "research-codex-en"
SOURCE_LIST = REPOSITORY_ROOT / "skills-sources.json"
GITIGNORE = REPOSITORY_ROOT / ".gitignore"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Deep Research skills."
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=REPOSITORY_ROOT,
        help=f"Installation parent (default: {REPOSITORY_ROOT})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be installed without downloading or changing files.",
    )
    return parser.parse_args()


def register_source() -> None:
    sources: list[dict[str, str]] = []
    if SOURCE_LIST.exists():
        try:
            sources = json.loads(SOURCE_LIST.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise SystemExit(f"Invalid source list: {SOURCE_LIST}") from error
    sources = [entry for entry in sources if entry.get("name") != INSTALL_NAME]
    sources.append({"name": INSTALL_NAME, "url": SOURCE_URL})
    sources.sort(key=lambda entry: entry["name"])
    SOURCE_LIST.write_text(
        json.dumps(sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    ignore_entry = f"/{INSTALL_NAME}/"
    existing = GITIGNORE.read_text(encoding="utf-8") if GITIGNORE.exists() else ""
    if ignore_entry not in existing.splitlines():
        with GITIGNORE.open("a", encoding="utf-8") as gitignore:
            if existing and not existing.endswith("\n"):
                gitignore.write("\n")
            gitignore.write(f"{ignore_entry}\n")


def select_codex_skills(checkout: Path) -> None:
    """Keep only skills/research-codex-en as the installed skills directory."""
    skills_dir = checkout / "skills"
    selected = skills_dir / SKILLS_VARIANT
    if not selected.is_dir():
        raise SystemExit(f"missing skills variant: {selected}")

    temporary_selected = checkout / f".{SKILLS_VARIANT}-selected"
    selected.rename(temporary_selected)
    shutil.rmtree(skills_dir)
    temporary_selected.rename(skills_dir)


def create_plugin_configs(checkout: Path) -> None:
    version_file = checkout / "installed_version.json"
    version_file.write_text('{"version": "1.0.0"}\n', encoding="utf-8")

    plugin_file = checkout / "plugin.json"
    plugin_data = {
        "name": INSTALL_NAME,
        "version": "1.0.0",
        "description": INSTALL_NAME,
        "author": {
            "name": INSTALL_NAME
        },
        "license": "Apache-2.0",
        "keywords": [
            "android",
            "mobile",
            "device",
            "sdk",
            "journeys",
            "device"
        ]
    }
    plugin_file.write_text(
        json.dumps(plugin_data, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    args = parse_args()
    destination = args.target_dir.expanduser() / INSTALL_NAME
    print(f"source:      {SOURCE_URL}")
    print(f"destination: {destination}")
    if args.dry_run:
        print("dry run: no files downloaded or changed")
        return 0

    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=f".{INSTALL_NAME}-", dir=destination.parent
    ) as temporary_dir:
        checkout = Path(temporary_dir) / INSTALL_NAME
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", SOURCE_URL, str(checkout)],
                check=True,
            )
        except FileNotFoundError as error:
            raise SystemExit("git is required but was not found on PATH") from error
        except subprocess.CalledProcessError as error:
            raise SystemExit(
                f"git clone failed with exit code {error.returncode}"
            ) from error

        select_codex_skills(checkout)
        create_plugin_configs(checkout)
        if destination.exists():
            shutil.rmtree(destination)
        checkout.rename(destination)

    register_source()
    print("installed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
