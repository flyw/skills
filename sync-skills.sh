#!/usr/bin/env bash
# Synchronize skill folders from this library into a selected local skills or plugins directory.
#
# Each source group directory at <library>/<group> (containing skills/) is synchronized to:
#   1) ~/.agents/skills/<group>-<skill> (flattened copy)
#   2) ~/.codex/skills/<group>-<skill> (flattened copy)
#   3) ~/.gemini/config/plugins/<group> (grouped folder copy)

set -euo pipefail

LIBRARY_DIR="$(cd "$(dirname "$0")" && pwd -P)"

printf 'Where should the skills be installed?\n'
printf '  1) %s/.agents/skills\n' "$HOME"
printf '  2) %s/.codex/skills\n' "$HOME"
printf '  3) %s/.gemini/config/plugins\n' "$HOME"
while true; do
  read -r -p 'Choose [1/2/3]: ' choice
  case "$choice" in
    1)
      MODE="flatten"
      DEST_DIR="$HOME/.agents/skills"
      break
      ;;
    2)
      MODE="flatten"
      DEST_DIR="$HOME/.codex/skills"
      break
      ;;
    3)
      MODE="plugin"
      DEST_DIR="$HOME/.gemini/config/plugins"
      break
      ;;
    *)
      printf 'Please choose 1, 2, or 3.\n' >&2
      ;;
  esac
done

mkdir -p "$DEST_DIR"

if [[ "$MODE" == "plugin" ]]; then
  for group_dir in "$LIBRARY_DIR"/*; do
    [[ -d "$group_dir/skills" && ! -L "$group_dir/skills" ]] || continue

    group_name="${group_dir##*/}"
    target_path="$DEST_DIR/$group_name"

    if [[ -e "$target_path" || -L "$target_path" ]]; then
      rm -rf "$target_path"
      printf 'removed existing plugin: %s\n' "$(basename "$target_path")"
    fi

    cp -R "$group_dir" "$target_path"
    printf 'copied plugin: %s\n' "$(basename "$target_path")"
  done
else
  for group_dir in "$LIBRARY_DIR"/*; do
    [[ -d "$group_dir/skills" && ! -L "$group_dir/skills" ]] || continue

    group_name="${group_dir##*/}"
    for skill_file in "$group_dir"/skills/*/SKILL.md; do
      [[ -f "$skill_file" ]] || continue

      skill_dir="${skill_file%/SKILL.md}"
      skill_name="${skill_dir##*/}"
      target_path="$DEST_DIR/$group_name-$skill_name"

      if [[ -e "$target_path" || -L "$target_path" ]]; then
        rm -rf "$target_path"
        printf 'removed existing: %s\n' "$(basename "$target_path")"
      fi

      cp -R "$skill_dir" "$target_path"
      printf 'copied: %s\n' "$(basename "$target_path")"
    done
  done
fi


