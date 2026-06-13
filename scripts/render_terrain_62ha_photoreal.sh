#!/usr/bin/env bash
# Photoreal LQV terrain — 3 views × A/B/C exposures at 1920×1080 / 256 samples.
# Replaces the v5 cartoon platforms / icosphere trees / emission stream with:
#   * Poly Haven HDRI (qwantani_sunset_puresky_4k, sun rotated NW)
#   * PBR ground blend (cracked_red_ground uplands + muddy_tracks streambed)
#   * Real Sentinel-2 albedo as tint layer over the PBR base
#   * jacaranda_tree_4k linked from .blend, ~70 scatter on relief
#   * rock_moss_set_02_4k + boulder_01_4k along the streamline / pool
# Driver: lqv/subscene/terrain_62ha_photoreal.py
set -euo pipefail

cd "$(dirname "$0")/.."

export RENDER_RUN_ID="20260611_dt_run_photoreal"
export RENDER_RES="final"
export RENDER_SAMPLES="256"

for view in birdseye oblique plan; do
  for variant in A B C; do
    echo "=== view=${view} variant=${variant} ==="
    RENDER_CAM_VIEW="${view}" RENDER_VARIANT="${variant}" \
      blender --background --python lqv/subscene/terrain_62ha_photoreal.py 2>&1 \
      | grep -E "^\[(subscene|render|terrain|cycles|asset|scatter)" || true
  done
done

echo "=== ALL PHOTOREAL RENDERS COMPLETE ==="
echo "Output: renders/sub/runs/${RENDER_RUN_ID}_terrain_62ha_photoreal_*/<A|B|C>.png"
