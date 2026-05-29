#!/usr/bin/env bash
# Install the Generate-and-Test harness:
#   1. copy the four gt-*.sh hooks into ~/.claude/hooks/
#   2. wire three hook entries into ~/.claude/settings.json (idempotent, backed up)
# Safe to re-run. Restart Claude Code afterwards.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_SRC="$SCRIPT_DIR/hooks"
HOOKS_DST="$HOME/.claude/hooks"
SETTINGS="$HOME/.claude/settings.json"

if [[ ! -d "$HOOKS_SRC" ]]; then
  echo "error: $HOOKS_SRC not found. Run from a cloned repo." >&2
  exit 1
fi

# 1. Copy hook scripts
mkdir -p "$HOOKS_DST"
for f in gt-classify.sh gt-stop-gate.sh gt-commit-gate.sh gt-mark.sh; do
  cp "$HOOKS_SRC/$f" "$HOOKS_DST/$f"
  chmod +x "$HOOKS_DST/$f"
  echo "  installed hook: $f"
done

# 2. Merge hook wiring into settings.json (idempotent, backed up)
python3 - "$SETTINGS" "$HOOKS_DST" <<'PY'
import json, os, sys, shutil

settings_path, hooks_dst = sys.argv[1], sys.argv[2]
os.makedirs(os.path.dirname(settings_path), exist_ok=True)

if os.path.exists(settings_path):
    shutil.copy(settings_path, settings_path + ".bak")
    with open(settings_path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("error: ~/.claude/settings.json is not valid JSON; aborting.", file=sys.stderr)
            sys.exit(1)
else:
    data = {}

hooks = data.setdefault("hooks", {})

def cmd(name):
    return f"bash {hooks_dst}/{name}"

# event -> (matcher or None, command, timeout)
entries = [
    ("PreToolUse",  "Bash",       cmd("gt-commit-gate.sh"), 20),
    ("PostToolUse", "Edit|Write", cmd("gt-classify.sh"),    15),
    ("Stop",        None,         cmd("gt-stop-gate.sh"),   15),
]

added = []
for event, matcher, command, timeout in entries:
    arr = hooks.setdefault(event, [])
    marker = command.split()[-1]  # full path to the gt script
    already = any(
        marker in h.get("command", "")
        for group in arr for h in group.get("hooks", [])
    )
    if already:
        continue
    group = {"hooks": [{"type": "command", "command": command, "timeout": timeout}]}
    if matcher is not None:
        group = {"matcher": matcher, **group}
    arr.append(group)
    added.append(event)

with open(settings_path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

if added:
    print("  wired hooks into settings.json:", ", ".join(added))
else:
    print("  hooks already wired in settings.json (nothing to add)")
PY

echo ""
echo "Done. Restart Claude Code for the hooks to take effect."
echo ""
echo "Optional — enable note-vault classification (literature/idea tests):"
echo '  export GT_IDEA_DIRS="notes/ideas"      # files here -> /find-redflag + /manage-refs + /check-facts'
echo '  export GT_BIB_DIRS="notes/literature"  # files here -> same literature test'
echo "Set CODE_REVIEW_MIN_LINES to change the code-review nudge threshold (default 40)."
