#!/usr/bin/env bash
# v5 arrowfix — re-render birdseye + oblique only (plan unaffected, north arrow
# not visible from straight-down). Shrinks arrow radius 30→15m, depth 70→35m so
# it stops dominating the upper-right corner.
set -euo pipefail

cd "$(dirname "$0")/.."

export RENDER_RUN_ID="20260611_dt_run_v5_arrowfix"
export RENDER_RES="final"
export RENDER_SAMPLES="256"

for view in birdseye oblique; do
  for variant in A B C; do
    echo "=== view=${view} variant=${variant} ==="
    RENDER_CAM_VIEW="${view}" RENDER_VARIANT="${variant}" \
      blender --background --python lqv/subscene/terrain_62ha.py 2>&1 \
      | grep -E "^\[(subscene|render|terrain|cycles)" || true
  done
done

echo "=== ALL V5 ARROWFIX RENDERS COMPLETE ==="
