#!/usr/bin/env bash
# Generate-and-Test harness — MARK (run after a skill-test, or to log an audited skip)
# Usage:
#   bash gt-mark.sh verified <path>
#   bash gt-mark.sh skip <path> "reason it does not apply"
# Appends a superseding ledger entry (latest-per-path wins) + an audit-log line.

action="${1:-}"; path="${2:-}"; reason="${3:-}"
proj="${CLAUDE_PROJECT_DIR:-$PWD}"
state="$proj/.claude/state"
ledger="$state/gt_ledger.jsonl"
audit="$state/gt_audit.log"
mkdir -p "$state" 2>/dev/null

if [ -z "$action" ] || [ -z "$path" ]; then
  echo "usage: gt-mark.sh verified|skip <path> [reason]" >&2; exit 1
fi
case "$path" in /*) abs="$path";; *) abs="$proj/$path";; esac

case "$action" in
  verified) status="verified";;
  skip)     status="skipped"
            [ -z "$reason" ] && { echo "skip requires an audited reason" >&2; exit 1; };;
  *)        echo "unknown action: $action (use verified|skip)" >&2; exit 1;;
esac

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
sha="$( { shasum "$abs" 2>/dev/null || echo none; } | cut -c1-12)"
safe_reason="${reason//\"/\'}"
printf '{"ts":"%s","type":"mark","path":"%s","sha":"%s","status":"%s","note":"%s"}\n' \
  "$ts" "$abs" "$sha" "$status" "$safe_reason" >> "$ledger"
printf '%s\t%s\t%s\t%s\n' "$ts" "$status" "$abs" "$safe_reason" >> "$audit"
echo "✓ marked $status: $abs"
