#!/usr/bin/env bash
# v5 redesign batch — 3 views × A/B/C at 1920×1080 / 256 samples.
# Fixes vs v4: stream rides sampled surface (no vertical wall), pool moved
# inward off NE parcel edge, rectangular cob-house platforms with gable
# roofs, trunk+crown trees anchored on relief, north arrow on the surface,
# gradient sky world, satellite albedo gain bumped 5.5→9.0.
set -euo pipefail

cd "$(dirname "$0")/.."

export RENDER_RUN_ID="20260611_dt_run_v5"
export RENDER_RES="final"
export RENDER_SAMPLES="256"

for view in birdseye plan oblique; do
  for variant in A B C; do
    echo "=== view=${view} variant=${variant} ==="
    RENDER_CAM_VIEW="${view}" RENDER_VARIANT="${variant}" \
      blender --background --python lqv/subscene/terrain_62ha.py 2>&1 \
      | grep -E "^\[(subscene|render|terrain|cycles)" || true
  done
done

echo "=== ALL V5 RENDERS COMPLETE ==="
