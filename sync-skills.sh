#!/usr/bin/env bash
# Synchronize skill folders from this library into a selected local skills directory.
#
# Each source at <library>/<group>/skills/<skill>/SKILL.md is copied to:
#   ~/.agents/skills/<group>-<skill>

set -euo pipefail

LIBRARY_DIR="$(cd "$(dirname "$0")" && pwd -P)"

printf 'Where should the skills be installed?\n'
printf '  1) %s/.agents/skills\n' "$HOME"
printf '  2) %s/.codex/skills\n' "$HOME"
while true; do
  read -r -p 'Choose [1/2]: ' choice
  case "$choice" in
    1)
      SKILLS_DIR="$HOME/.agents/skills"
      break
      ;;
    2)
      SKILLS_DIR="$HOME/.codex/skills"
      break
      ;;
    *)
      printf 'Please choose 1 or 2.\n' >&2
      ;;
  esac
done

mkdir -p "$SKILLS_DIR"

for group_dir in "$LIBRARY_DIR"/*; do
  [[ -d "$group_dir/skills" && ! -L "$group_dir/skills" ]] || continue

  group_name="${group_dir##*/}"
  for skill_file in "$group_dir"/skills/*/SKILL.md; do
    [[ -f "$skill_file" ]] || continue

    skill_dir="${skill_file%/SKILL.md}"
    skill_name="${skill_dir##*/}"
    target_path="$SKILLS_DIR/$group_name-$skill_name"

    if [[ -e "$target_path" || -L "$target_path" ]]; then
      rm -rf "$target_path"
      printf 'removed existing: %s\n' "$(basename "$target_path")"
    fi

    cp -R "$skill_dir" "$target_path"
    printf 'copied: %s\n' "$(basename "$target_path")"
  done
done

