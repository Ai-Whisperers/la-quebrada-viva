#!/usr/bin/env bash
# PostToolUse hook: syntax-check any edited .py file so broken code is caught
# before a 5-minute Blender build attempts to import it.
set -u

input=$(cat)
file_path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')

[ -z "$file_path" ] && exit 0
case "$file_path" in
  *.py) ;;
  *) exit 0 ;;
esac
[ -f "$file_path" ] || exit 0

if ! err=$(python3 -m py_compile "$file_path" 2>&1); then
  echo "py_compile failed for $file_path:" >&2
  echo "$err" >&2
  exit 2
fi
exit 0
