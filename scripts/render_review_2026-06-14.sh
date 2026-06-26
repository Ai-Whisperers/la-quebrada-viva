#!/usr/bin/env bash
# Phase 3 batch: 17 assets x 3 variants = 51 sub-renders for the
# 2026-06-14 review gallery. Cap-4 parallelism via xargs -P4.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BLENDER="${BLENDER:-/home/ai-whisperers/.local/bin/blender}"
LOG_DIR="$ROOT/renders/sub/runs/review_2026-06-14_logs"
mkdir -p "$LOG_DIR"

export ROOT BLENDER LOG_DIR

ASSETS=(
  bamboo_beton_28
  bamboo_beton_30
  bamboo_beton_family_curved
  bamboo_beton_family_rectangular
  bamboo_boomhut_treehouse
  bamboo_container_4pax
  bamboo_river_house
  bamboo_wigwam_lodge
  container_river_house
  hobbit_house
  italian_river_house_4pax
  italian_stone_small_v1
  italian_stone_small_v2
  eco_pool
  eco_retreat_modern_oasis
  floating_dining
  labrisa_lounge
)

# Emit "asset variant" pairs, feed to xargs cap-4.
# Inline body avoids the `export -f` + xargs+bash -c env-propagation bug
# that killed the prior run (every job died at "environment: line 2:").
{
  for asset in "${ASSETS[@]}"; do
    for variant in A B C; do
      printf '%s %s\n' "$asset" "$variant"
    done
  done
} | xargs -n 2 -P 4 bash -c '
  asset="$1"
  variant="$2"
  log="$LOG_DIR/${asset}_${variant}.log"
  if RENDER_RUN_ID=review_2026-06-14 \
     RENDER_VARIANT="$variant" \
     RENDER_FLORA_PHOTOREAL=1 \
     RENDER_RES=preview \
     RENDER_SAMPLES=64 \
     PYTHONPATH="$ROOT" \
     "$BLENDER" -b -P "lqv/subscene/${asset}.py" >"$log" 2>&1; then
    echo "OK   $asset $variant"
  else
    echo "FAIL $asset $variant (see $log)"
  fi
' _

echo "[review_2026-06-14] all 51 jobs dispatched"
