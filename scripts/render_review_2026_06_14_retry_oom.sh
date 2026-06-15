#!/usr/bin/env bash
# Serial retry of the 6 OOM-killed renders from the main cap-4 batch.
# Waits for the main dispatcher PID to exit, then re-runs failed assets one at a time
# so each amenity gets the full RAM budget instead of fighting cap-4 neighbours.
set -u
ROOT="/home/ai-whisperers/blender-projects/la-quebrada-viva"
BLENDER="/home/ai-whisperers/.local/bin/blender"
RUN_ID="review_2026-06-14"
LOG_DIR="$ROOT/renders/sub/runs/${RUN_ID}_logs"
OUT="/tmp/lqv_review_retry_oom.out"
MAIN_PID="${MAIN_PID:-2891061}"

cd "$ROOT"
mkdir -p "$LOG_DIR"

echo "[$(date -Is)] waiting for main dispatcher PID $MAIN_PID to exit" >>"$OUT"
while kill -0 "$MAIN_PID" 2>/dev/null; do sleep 5; done
echo "[$(date -Is)] main dispatcher exited; starting serial retry" >>"$OUT"

assets=(eco_pool eco_retreat_modern_oasis)
variants=(A B C)

for asset in "${assets[@]}"; do
  for variant in "${variants[@]}"; do
    log="$LOG_DIR/${asset}_${variant}.log"
    echo "[$(date -Is)] retry $asset $variant" >>"$OUT"
    if RENDER_RUN_ID="$RUN_ID" \
       RENDER_VARIANT="$variant" \
       RENDER_FLORA_PHOTOREAL=1 \
       RENDER_RES=preview \
       RENDER_SAMPLES=64 \
       PYTHONPATH="$ROOT" \
       "$BLENDER" -b -P "lqv/subscene/${asset}.py" >"$log" 2>&1; then
      echo "OK   $asset $variant" >>"$OUT"
    else
      echo "FAIL $asset $variant (see $log)" >>"$OUT"
    fi
  done
done
echo "[$(date -Is)] serial retry complete" >>"$OUT"
