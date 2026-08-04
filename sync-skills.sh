#!/usr/bin/env bash
# Synchronize skill folders from ~/.agents/library into ~/.agents/skills.
#
# Each source at <library>/<group>/skills/<skill>/SKILL.md becomes a symlink:
#   ~/.agents/skills/<group>-<skill> -> <library>/<group>/skills/<skill>

set -euo pipefail

LIBRARY_DIR="$(cd "$(dirname "$0")" && pwd -P)"
SKILLS_DIR="$(cd "$LIBRARY_DIR/.." && pwd -P)/skills"

mkdir -p "$SKILLS_DIR"

is_managed_link() {
  local link_target
  link_target="$(readlink "$1" 2>/dev/null || true)"
  [[ "$link_target" == "$LIBRARY_DIR"/* ]]
}

# Rebuild all library-managed links from scratch on every run. Other skills in
# ~/.agents/skills are left untouched.
for entry in "$SKILLS_DIR"/*; do
  if [[ -L "$entry" ]] && is_managed_link "$entry"; then
    rm "$entry"
    printf 'removed: %s\n' "$(basename "$entry")"
  fi
done

for group_dir in "$LIBRARY_DIR"/*; do
  [[ -d "$group_dir/skills" && ! -L "$group_dir/skills" ]] || continue

  group_name="${group_dir##*/}"
  for skill_file in "$group_dir"/skills/*/SKILL.md; do
    [[ -f "$skill_file" ]] || continue

    skill_dir="${skill_file%/SKILL.md}"
    skill_name="${skill_dir##*/}"
    link_path="$SKILLS_DIR/$group_name-$skill_name"

    if [[ -e "$link_path" || -L "$link_path" ]]; then
      printf 'skipped existing unmanaged path: %s\n' "$link_path" >&2
      continue
    fi

    ln -s "$skill_dir" "$link_path"
    printf 'linked: %s\n' "$(basename "$link_path")"
  done
done
