#!/usr/bin/env bash
# Generate-and-Test harness — STOP NUDGE (Stop hook, fires at every turn end)
# Non-blocking by design (no decision:block) => fast, loop-proof. Prints a one-shot
# reminder of artifacts whose skill-test is still OWED. The HARD gate is at commit time.

input="$(cat 2>/dev/null)"
proj="${CLAUDE_PROJECT_DIR:-$PWD}"
ledger="$proj/.claude/state/gt_ledger.jsonl"
[ -f "$ledger" ] || exit 0

# owed = for each path, latest entry has status "pending"
owed="$(jq -rs '
  group_by(.path) | map(.[-1]) | map(select(.status=="pending"))
  | .[] | "\(.type)\t\(.path)"' "$ledger" 2>/dev/null)"
[ -z "$owed" ] && exit 0

list="$(printf '%s' "$owed" | awk -F'\t' '
  function skill(t){
    if(t=="code")    return "/code-review";
    if(t=="idea")    return "/find-redflag + /manage-refs + /check-facts";
    if(t=="bib")     return "/find-redflag + /manage-refs + /check-facts";
    if(t=="figure")  return "/roast-figure";
    if(t=="writing") return "/find-redflag + /check-facts (+ /manage-refs if it cites sources)";
    return "?"}
  { n=split($2,a,"/"); printf "  • %s  →  %s\n", a[n], skill($1) }')"

printf '🧪 Generate-and-Test: untested AI output (skill-test owed before commit):\n%s\n' "$list"
printf '   Run the test, then: bash ~/.claude/hooks/gt-mark.sh verified <path>  (or: skip <path> "reason")\n'
exit 0
