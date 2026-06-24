#!/usr/bin/env bash
# Serial sub-render batch for the 5 new Wesley-phase-2 typology candidates.
# 14 GB host → parallelism = 1 (per feedback_render_parallelism: 3 concurrent
# Blender processes OOM at ~4.3 GB RSS each). 5 assets × A/B/C = 15 renders.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BLENDER="${BLENDER:-/home/ai-whisperers/.local/bin/blender}"
RUN_ID="${RENDER_RUN_ID:-wesley_phase2_2026-06-23}"
LOG_DIR="$ROOT/renders/sub/runs/${RUN_ID}_logs"
mkdir -p "$LOG_DIR"

ASSETS=(
  bamboo_portal
  clay_terracotta_estate
  bamboo_outdoor_shower
  candle_path
  bamboo_curved_roof_villa
)

SAMPLES="${RENDER_SAMPLES:-256}"
RES="${RENDER_RES:-preview}"

echo "[wesley_phase2] run_id=$RUN_ID samples=$SAMPLES res=$RES"

for asset in "${ASSETS[@]}"; do
  for variant in A B C; do
    log="$LOG_DIR/${asset}_${variant}.log"
    printf '[wesley_phase2] %s %s ... ' "$asset" "$variant"
    if RENDER_RUN_ID="$RUN_ID" \
       RENDER_VARIANT="$variant" \
       RENDER_RES="$RES" \
       RENDER_SAMPLES="$SAMPLES" \
       LQV_ALLOW_CPU_FALLBACK="${LQV_ALLOW_CPU_FALLBACK:-1}" \
       PYTHONPATH="$ROOT" \
       "$BLENDER" -b -P "lqv/subscene/${asset}.py" >"$log" 2>&1; then
      echo OK
    else
      echo "FAIL (see $log)"
    fi
  done
done

echo "[wesley_phase2] done — outputs under renders/sub/runs/${RUN_ID}_*"
