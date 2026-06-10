#!/usr/bin/env bash
# Render the full deliverable matrix: variants A/B/C x 6 cameras = 18 finals.
# Long-running (hours). Fails fast on the first broken render.
set -euo pipefail
cd "$(dirname "$0")/.."

for variant in A B C; do
  for cam in hero stream_up terrace cliff dusk petal_macro; do
    echo "=== rendering ${variant}_${cam} ==="
    scripts/render_final.sh "$variant" "$cam"
  done
done
echo "ALL 18 FINALS DONE — verify each with /verify-render and update STATUS.md"
