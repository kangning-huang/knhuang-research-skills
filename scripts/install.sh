#!/usr/bin/env bash
# Install Lu Lab research skills by symlinking into ~/.claude/skills/
# Safe: refuses to overwrite existing non-symlink directories.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
SKILLS_DST="$HOME/.claude/skills"

if [[ ! -d "$SKILLS_SRC" ]]; then
  echo "error: $SKILLS_SRC does not exist. Run from a cloned repo." >&2
  exit 1
fi

mkdir -p "$SKILLS_DST"

installed=0
skipped=0

for skill_dir in "$SKILLS_SRC"/*/; do
  skill_name="$(basename "$skill_dir")"
  target="$SKILLS_DST/$skill_name"

  if [[ -L "$target" ]]; then
    # existing symlink — replace if it points elsewhere
    current="$(readlink "$target")"
    if [[ "$current" == "$skill_dir"* ]]; then
      echo "  already linked: $skill_name"
      skipped=$((skipped + 1))
      continue
    fi
    rm "$target"
  elif [[ -e "$target" ]]; then
    echo "  SKIP: $skill_name (real directory exists — move/remove manually)"
    skipped=$((skipped + 1))
    continue
  fi

  ln -s "$skill_dir" "$target"
  echo "  installed: $skill_name"
  installed=$((installed + 1))
done

echo ""
echo "Done. $installed installed, $skipped skipped."
echo "Restart Claude Code if it is running. Type '/' to see the skills."
