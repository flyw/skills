#!/usr/bin/env python3
"""Download and normalize mattpocock's skills repository."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent
SOURCE_URL = "https://github.com/mattpocock/skills"
INSTALL_NAME = "mattpocock"
SOURCE_LIST = REPOSITORY_ROOT / "skills-sources.json"
GITIGNORE = REPOSITORY_ROOT / ".gitignore"
IGNORED_CATEGORIES = {"deprecated", "in-progress", "misc"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and normalize mattpocock skills."
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


def flatten_skills(checkout: Path) -> None:
    skills_dir = checkout / "skills"
    if not skills_dir.is_dir():
        return

    categories = [
        path
        for path in skills_dir.iterdir()
        if path.is_dir()
        and not path.is_symlink()
        and path.name not in IGNORED_CATEGORIES
        and not (path / "SKILL.md").is_file()
        and any(
            child.is_dir() and (child / "SKILL.md").is_file()
            for child in path.iterdir()
        )
    ]
    for category_name in IGNORED_CATEGORIES:
        ignored_category = skills_dir / category_name
        if ignored_category.is_dir() and not ignored_category.is_symlink():
            shutil.rmtree(ignored_category)

    skill_dirs = [
        skill_dir
        for category in categories
        for skill_dir in category.iterdir()
        if skill_dir.is_dir() and not skill_dir.is_symlink()
    ]
    destinations = [skills_dir / skill_dir.name for skill_dir in skill_dirs]
    if len(set(destinations)) != len(destinations) or any(
        destination.exists() for destination in destinations
    ):
        raise SystemExit("cannot flatten mattpocock skills: duplicate skill name")

    for skill_dir, destination in zip(skill_dirs, destinations):
        shutil.move(str(skill_dir), str(destination))
    for category in categories:
        shutil.rmtree(category)


def create_plugin_configs(checkout: Path) -> None:
    version_file = checkout / "installed_version.json"
    version_file.write_text('{"version": "1.0.0"}\n', encoding="utf-8")

    plugin_file = checkout / "plugin.json"
    plugin_data = {
        "name": INSTALL_NAME,
        "version": "1.0.0",
        "description": "Curated engineering skills for TDD, code review, codebase design, bug diagnosis, domain modeling, and prototyping.",
        "author": {
            "name": INSTALL_NAME
        },
        "license": "Apache-2.0",
        "keywords": [
            "engineering",
            "tdd",
            "code-review",
            "codebase-design",
            "debugging",
            "domain-modeling",
            "prototyping",
            "refactoring",
            "skills"
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

        flatten_skills(checkout)
        create_plugin_configs(checkout)
        if destination.exists():
            shutil.rmtree(destination)
        checkout.rename(destination)

    register_source()
    print("installed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
