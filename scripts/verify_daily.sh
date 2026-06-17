#!/usr/bin/env bash
# Daily VERIFY.sh wrapper for the T-9 → T-1 closing-prep window.
# Runs the 3-check protocol against the frozen bundle + deck, appends a
# timestamped line to dist/print_pack_2026-06-27/audit_log.txt, and exits non-zero
# if any of the 3 checks fail (so cron + the morning-of glance both work).
#
# Usage:
#   bash scripts/verify_daily.sh                   # prints + appends
#   bash scripts/verify_daily.sh --quiet           # only appends; cron-friendly
#   bash scripts/verify_daily.sh --since 2026-06-17  # tails audit_log entries since date
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACK_DIR="$REPO_ROOT/dist/print_pack_2026-06-27"
LOG="$PACK_DIR/audit_log.txt"
VERIFY="$PACK_DIR/VERIFY.sh"

QUIET=0
SINCE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --quiet) QUIET=1; shift ;;
    --since) SINCE="${2:-}"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -n "$SINCE" ]]; then
  awk -v since="$SINCE" '$0 ~ since,0' "$LOG"
  exit 0
fi

if [[ ! -x "$VERIFY" ]]; then
  echo "FATAL: $VERIFY missing or not executable" >&2
  exit 3
fi

TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
HOST="$(hostname -s 2>/dev/null || echo unknown)"
OUT="$(bash "$VERIFY" 2>&1)" && STATUS=0 || STATUS=$?

# Pass/fail accounting: VERIFY.sh emits one "OK" per check line and "All checks passed."
# at the end when all 3 succeed; on any failure it exits non-zero with shasum's "FAILED".
PASS_N="$(printf '%s\n' "$OUT" | grep -cE '(: OK$|^OK:)' || true)"
FAIL_N="$(printf '%s\n' "$OUT" | grep -cE '(FAILED|^FAIL )' || true)"
SUMMARY="$(printf '%s\n' "$OUT" | tail -1 | tr -d '\n' | cut -c1-80)"
LINE="$TS host=$HOST exit=$STATUS pass=$PASS_N fail=$FAIL_N tail=\"$SUMMARY\""

printf '%s\n' "$LINE" >> "$LOG"

if [[ $QUIET -eq 0 ]]; then
  printf '%s\n' "$OUT"
  printf 'logged: %s\n' "$LINE"
fi

exit "$STATUS"
