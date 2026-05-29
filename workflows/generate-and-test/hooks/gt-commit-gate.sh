#!/usr/bin/env bash
# Generate-and-Test harness — COMMIT GATE (PreToolUse: Bash) — the HARD enforcement.
# Blocks `git commit` while any STAGED artifact still has an unmet skill-test.
# Fires once per commit attempt (no auto-retry) => loop-proof.

input="$(cat 2>/dev/null)"
proj="${CLAUDE_PROJECT_DIR:-$PWD}"
ledger="$proj/.claude/state/gt_ledger.jsonl"

cmd="$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null)"
# Only intercept git commit; let everything else through instantly.
printf '%s' "$cmd" | grep -qE '(^|[;&| ])git[[:space:]]+commit([[:space:]]|$)' || exit 0
[ -f "$ledger" ] || exit 0

gitroot="$( { cd "$proj" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null; } )"
[ -z "$gitroot" ] && gitroot="$proj"
staged_rel="$(git -C "$gitroot" diff --cached --name-only 2>/dev/null)"
[ -z "$staged_rel" ] && exit 0

# owed = pending artifacts (latest entry per path) that match a staged file.
# Match by repo-relative suffix so path-canonicalization differences never matter.
tab="$(printf '\t')"
pend="$(jq -rs 'group_by(.path) | map(.[-1]) | map(select(.status=="pending")) | .[] | "\(.type)\t\(.path)"' "$ledger" 2>/dev/null)"
owed="$(printf '%s\n' "$pend" | while IFS="$tab" read -r t p; do
  [ -z "$p" ] && continue
  printf '%s\n' "$staged_rel" | while IFS= read -r rel; do
    [ -z "$rel" ] && continue
    if [ "${p%/$rel}" != "$p" ] || [ "$p" = "$rel" ]; then printf '%s\t%s\n' "$t" "$p"; fi
  done
done | sort -u)"
[ -z "$owed" ] && exit 0

list="$(printf '%s' "$owed" | awk -F'\t' '
  function skill(t){
    if(t=="code")    return "/code-review";
    if(t=="idea")    return "/find-redflag + /manage-refs + /check-facts";
    if(t=="bib")     return "/find-redflag + /manage-refs + /check-facts";
    if(t=="figure")  return "/roast-figure";
    if(t=="writing") return "/find-redflag + /check-facts (+ /manage-refs if it cites sources)";
    return "?"}
  { n=split($2,a,"/"); printf "  • %s  →  run %s\n", a[n], skill($1) }')"

reason="$(printf 'BLOCKED by Generate-and-Test gate. Staged artifacts have not passed their skill-test:\n%s\nFor each: run the skill on the artifact, then:\n  bash ~/.claude/hooks/gt-mark.sh verified <path>\nIf a test genuinely does not apply, log an AUDITED skip (never silent):\n  bash ~/.claude/hooks/gt-mark.sh skip <path> "why it does not apply"\nThen retry the commit.' "$list")"

jq -n --arg r "$reason" \
  '{hookSpecificOutput:{hookEventName:"PreToolUse", permissionDecision:"deny", permissionDecisionReason:$r}}'
exit 0
