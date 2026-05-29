#!/usr/bin/env bash
# Generate-and-Test harness — CLASSIFY (PostToolUse: Edit|Write)
# Records every AI-written artifact to the ledger (the machine-readable co-update record).
# Silent, non-blocking, no LLM. This is the "reflex layer": fast every-turn logging.
#
# Ledger line: {"ts","sid","type","path","sha","status":"pending"}
#   type ∈ code | figure | writing | idea | bib
# A later gt-mark.sh entry with status verified|skipped supersedes (latest-per-path wins).
#
# Config (all optional, via environment):
#   CODE_REVIEW_MIN_LINES   lines threshold for the code-review nudge (default 40)
#   GT_IDEA_DIRS            colon-separated path fragments -> classified as "idea"
#                          e.g. export GT_IDEA_DIRS="notes/ideas:research/concepts"
#   GT_BIB_DIRS            colon-separated path fragments -> classified as "bib"
#                          e.g. export GT_BIB_DIRS="notes/literature:refs"
#   GT_PROSE_EXEMPT        extra space-separated basenames exempt from the prose test
# Leave GT_IDEA_DIRS / GT_BIB_DIRS unset for the generic core (code/figure/prose only).

input="$(cat 2>/dev/null)"
proj="${CLAUDE_PROJECT_DIR:-$PWD}"
state="$proj/.claude/state"
ledger="$state/gt_ledger.jsonl"
mkdir -p "$state" 2>/dev/null

fp="$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)"
sid="$(printf '%s' "$input" | jq -r '.session_id // "?"' 2>/dev/null)"
[ -z "$fp" ] && exit 0

case "$fp" in /*) abs="$fp";; *) abs="$proj/$fp";; esac

# Exclusions: never test the harness itself, vcs internals, deps, or generated state.
case "$abs" in
  */.claude/*|*/.git/*|*/node_modules/*|*/.venv/*|*/build/*|*/dist/*) exit 0;;
esac

base="$(basename "$abs")"

# Optional note-vault classification (only if the user opted in via env).
in_any_dir() {
  # $1 = colon-separated fragments; returns 0 if $abs contains "/<fragment>/" or "/<fragment>" suffix-dir
  local IFS=':' frag
  for frag in $1; do
    [ -z "$frag" ] && continue
    case "$abs" in *"/$frag/"*) return 0;; esac
  done
  return 1
}

typ=""
if printf '%s' "$abs" | grep -qiE '/figures?/|(plot|fig|figure)[^/]*\.(R|r|py|ipynb)$'; then
  typ="figure"
elif printf '%s' "$base" | grep -qiE '\.(py|R|r|ipynb|jl|sh)$'; then
  typ="code"
elif [ -n "${GT_IDEA_DIRS:-}" ] && printf '%s' "$base" | grep -qiE '\.(md|markdown)$' && in_any_dir "$GT_IDEA_DIRS"; then
  typ="idea"
elif [ -n "${GT_BIB_DIRS:-}" ] && printf '%s' "$base" | grep -qiE '\.(md|markdown)$' && in_any_dir "$GT_BIB_DIRS"; then
  typ="bib"
elif printf '%s' "$base" | grep -qiE '\.(md|markdown|tex)$'; then
  # Any authored prose gets the writing test — EXCEPT operational/meta files.
  case "$base" in
    README.md|CLAUDE.md|AGENTS.md|GEMINI.md|CHANGELOG.md|CONTRIBUTING.md|LICENSE.md|LICENSE) typ="";;
    *)
      skip=""
      for ex in ${GT_PROSE_EXEMPT:-}; do [ "$base" = "$ex" ] && skip=1; done
      [ -n "$skip" ] && typ="" || typ="writing"
      ;;
  esac
fi
[ -z "$typ" ] && exit 0

sha="$( { shasum "$abs" 2>/dev/null || echo none; } | cut -c1-12)"
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [ "$typ" = "code" ]; then
  # Code is NOT commit-gated (commits stay fast). Code-review fires IMMEDIATELY on a
  # major creation / refactor / large edit. Logged for the record, never "owed" at commit.
  printf '{"ts":"%s","sid":"%s","type":"code","path":"%s","sha":"%s","status":"logged"}\n' \
    "$ts" "$sid" "$abs" "$sha" >> "$ledger" 2>/dev/null
  : "${CODE_REVIEW_MIN_LINES:=40}"
  lines="$(printf '%s' "$input" | jq -r '
    def nl(s): ((s // "") | split("\n") | length);
    if   .tool_name=="Write"     then nl(.tool_input.content)
    elif .tool_name=="Edit"      then (nl(.tool_input.new_string) + nl(.tool_input.old_string))
    elif .tool_name=="MultiEdit" then ([.tool_input.edits[]? | (nl(.new_string)+nl(.old_string))] | add // 0)
    else 0 end' 2>/dev/null)"
  case "$lines" in ''|*[!0-9]*) lines=0;; esac
  if [ "$lines" -ge "$CODE_REVIEW_MIN_LINES" ]; then
    msg="$(printf '🧪 Generate-and-Test (code reflex): major change to %s (~%s lines). MANDATORY: run /code-review on this change now, before continuing — fix or note findings. (Code is reviewed at creation/refactor time, not at commit.)' "$base" "$lines")"
    jq -n --arg m "$msg" '{hookSpecificOutput:{hookEventName:"PostToolUse", additionalContext:$m}}'
  fi
  exit 0
fi

# idea | bib | writing | figure  ->  "pending" (owed), enforced by the commit gate
printf '{"ts":"%s","sid":"%s","type":"%s","path":"%s","sha":"%s","status":"pending"}\n' \
  "$ts" "$sid" "$typ" "$abs" "$sha" >> "$ledger" 2>/dev/null
exit 0
