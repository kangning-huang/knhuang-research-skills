#!/usr/bin/env bash
# Uninstall the Generate-and-Test harness:
#   1. remove the three gt-* hook entries from ~/.claude/settings.json (backed up)
#   2. remove the four gt-*.sh scripts from ~/.claude/hooks/
# Leaves any existing non-gt hooks and your project ledgers untouched.
set -euo pipefail

HOOKS_DST="$HOME/.claude/hooks"
SETTINGS="$HOME/.claude/settings.json"

# 1. Strip the gt-* hook entries from settings.json
if [[ -f "$SETTINGS" ]]; then
  python3 - "$SETTINGS" <<'PY'
import json, os, sys, shutil

settings_path = sys.argv[1]
shutil.copy(settings_path, settings_path + ".bak")
with open(settings_path) as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        print("error: ~/.claude/settings.json is not valid JSON; aborting.", file=sys.stderr)
        sys.exit(1)

hooks = data.get("hooks", {})
removed = 0
for event, arr in list(hooks.items()):
    kept = []
    for group in arr:
        inner = [h for h in group.get("hooks", []) if "/gt-" not in h.get("command", "")]
        if not inner:
            removed += 1
            continue
        if len(inner) != len(group.get("hooks", [])):
            removed += 1
        group["hooks"] = inner
        kept.append(group)
    if kept:
        hooks[event] = kept
    else:
        del hooks[event]

if not hooks:
    data.pop("hooks", None)

with open(settings_path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print(f"  removed {removed} gt-* hook entr{'y' if removed == 1 else 'ies'} from settings.json")
PY
else
  echo "  no settings.json found — nothing to unwire"
fi

# 2. Remove the hook scripts
for f in gt-classify.sh gt-stop-gate.sh gt-commit-gate.sh gt-mark.sh; do
  if [[ -e "$HOOKS_DST/$f" ]]; then
    rm "$HOOKS_DST/$f"
    echo "  removed hook: $f"
  fi
done

echo ""
echo "Done. Restart Claude Code. Project ledgers (.claude/state/gt_*) were left in place."
