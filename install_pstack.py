#!/usr/bin/env python3
"""Download and configure pstack skills repository."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent
SOURCE_URL = "https://github.com/michael-denyer/pstack-claude"
INSTALL_NAME = "pstack"
SOURCE_LIST = REPOSITORY_ROOT / "skills-sources.json"
GITIGNORE = REPOSITORY_ROOT / ".gitignore"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and configure pstack skills."
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


def stage_pstack_plugin(checkout: Path, staged_dest: Path) -> None:
    source_plugin_dir = checkout / "plugins" / "pstack"
    if not source_plugin_dir.is_dir():
        raise SystemExit(f"missing plugin directory: {source_plugin_dir}")

    # Copy plugin directory (includes skills, agents, effort-agents, hooks, assets, pi, models.json, etc.)
    shutil.copytree(source_plugin_dir, staged_dest)

    # Copy license, notices, and version files from repo root if present
    for filename in [
        "LICENSE",
        "LICENSE-cursor-team-kit",
        "LICENSE-thermos",
        "NOTICE.md",
        "NOTICE-skills.md",
        "VERSION",
    ]:
        src = checkout / filename
        if src.is_file():
            shutil.copy2(src, staged_dest / filename)

    # Copy docs if available and not already copied
    src_docs = checkout / "docs"
    if src_docs.is_dir() and not (staged_dest / "docs").exists():
        shutil.copytree(src_docs, staged_dest / "docs")

    # Read version
    version = "1.0.0"
    version_file = checkout / "VERSION"
    if version_file.is_file():
        version = version_file.read_text(encoding="utf-8").strip() or "1.0.0"

    # Ensure installed_version.json
    (staged_dest / "installed_version.json").write_text(
        json.dumps({"version": version}, indent=2) + "\n", encoding="utf-8"
    )

    # Create root plugin.json for Gemini / Antigravity / generic plugin hosts
    plugin_file = staged_dest / "plugin.json"
    if not plugin_file.exists():
        plugin_data = {
            "name": INSTALL_NAME,
            "version": version,
            "description": "If you want to go fast, go deep first. pstack helps you write less, but higher quality code: rigorous agent workflows you can parallelize with confidence. Ported from cursor/plugins/pstack by Lauren Tan (poteto).",
            "author": {
                "name": "Michael Denyer",
                "url": "https://github.com/michael-denyer"
            },
            "homepage": "https://github.com/michael-denyer/pstack-claude",
            "repository": SOURCE_URL,
            "license": "MIT",
            "keywords": [
                "pstack",
                "poteto-mode",
                "workflow",
                "principles",
                "agent-style",
                "subagents",
                "unslop",
                "claude-code",
                "skills",
                "tdd",
                "code-review",
                "parallel-agents",
                "codex",
                "opencode",
                "gemini-cli"
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
        checkout = Path(temporary_dir) / "repo"
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

        staged = Path(temporary_dir) / INSTALL_NAME
        stage_pstack_plugin(checkout, staged)

        if destination.exists():
            shutil.rmtree(destination)
        staged.rename(destination)

    register_source()
    print("installed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
