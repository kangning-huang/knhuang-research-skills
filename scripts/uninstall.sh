#!/usr/bin/env bash
# Uninstall Lu Lab research skills.
# Only removes symlinks pointing into this repo; leaves everything else alone.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
SKILLS_DST="$HOME/.claude/skills"

removed=0

for skill_dir in "$SKILLS_SRC"/*/; do
  skill_name="$(basename "$skill_dir")"
  target="$SKILLS_DST/$skill_name"

  if [[ -L "$target" ]]; then
    current="$(readlink "$target")"
    if [[ "$current" == "$skill_dir"* ]]; then
      rm "$target"
      echo "  removed: $skill_name"
      removed=$((removed + 1))
    fi
  fi
done

echo ""
echo "Done. $removed symlinks removed."
