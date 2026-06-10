#!/usr/bin/env bash
# Render the full deliverable matrix: variants A/B x 6 cameras = 12 finals.
# Long-running (hours). Fails fast on the first broken render.
set -euo pipefail
cd "$(dirname "$0")/.."

for variant in A B; do
  for cam in hero stream_up terrace cliff dusk petal_macro; do
    echo "=== rendering ${variant}_${cam} ==="
    scripts/render_final.sh "$variant" "$cam"
  done
done
echo "ALL 12 FINALS DONE — verify each with /verify-render and update STATUS.md"
