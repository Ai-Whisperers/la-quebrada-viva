#!/usr/bin/env bash
# v4 polish batch — 3 views × A/B/C at 1920×1080 / 256 samples.
# Adds cob-silhouette platforms, water-disk pool, riparian tree clusters,
# and Z-exaggerated relief (1.5×) over the v3 HD parcel-focus base.
# Each variant launches its own Blender process so env-vars are honored
# cleanly. RENDER_RUN_ID pins all 9 outputs into one run folder family;
# v3 PNGs are preserved automatically by the run-folder system.
set -euo pipefail

cd "$(dirname "$0")/.."

export RENDER_RUN_ID="20260611_dt_run_v4_polish"
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

echo "=== ALL V4 POLISH RENDERS COMPLETE ==="
