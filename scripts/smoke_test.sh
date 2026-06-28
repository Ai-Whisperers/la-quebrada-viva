#!/usr/bin/env bash
# Build the full scene without rendering. Run after any code edit.
set -euo pipefail
cd "$(dirname "$0")/.."

[ -f scene.blend ] && cp scene.blend scene.blend.session-backup

# build_scene.py does not invoke lqv.subscene.base directly today, but several
# audit-tier modules (and any future smoke render) do. lqv.subscene.base now
# requires RENDER_RUN_ID or LQV_ALLOW_TIMESTAMP_RUN_ID=1 (see docs/render-runs.md).
# A smoke test isn't a real batch — give it a stable id so any sub-render
# byproducts (if a future driver chains here) land in a predictable folder.
export RENDER_RUN_ID="${RENDER_RUN_ID:-smoke_$(date +%Y%m%d_%H%M%S)}"

log=$(mktemp)
# Build + audit in one Blender session. --python-expr runs after --python so
# ten_rules_check inspects the actually-built scene; sys.exit(1) on real
# violations propagates back as a non-zero exit from Blender.
audit='from lqv.util import ten_rules_check; import sys; v = ten_rules_check.run(); sys.exit(2 if v else 0)'
if ! RENDER_SKIP=1 RENDER_RES=preview RENDER_VARIANT="${RENDER_VARIANT:-A}" \
     LQV_ALLOW_CPU_FALLBACK="${LQV_ALLOW_CPU_FALLBACK:-1}" \
     blender --background --python build_scene.py --python-expr "$audit" 2>&1 | tee "$log"; then
  rc=${PIPESTATUS[0]}
  if [ "$rc" = "2" ]; then
    echo "SMOKE TEST FAILED: ten_rules_check found design-rule violations (see [ten_rules_check] lines above)" >&2
  else
    echo "SMOKE TEST FAILED: blender exited $rc" >&2
  fi
  exit 1
fi
if grep -q "Traceback (most recent call last)" "$log"; then
  echo "SMOKE TEST FAILED: Python traceback during build (see output above)" >&2
  exit 1
fi

# CC-TOOL.4: catch import / build-time regressions across the 50+ subscene
# drivers without burning render samples. Pick N at random per smoke run, run
# each headless with RENDER_SKIP=1 so save_subrender short-circuits. Exclude
# drivers that bypass base.run (need DEM/HDRI/asset prep we don't gate on
# here), plus base/__init__/services infrastructure modules. Opt out via
# LQV_SMOKE_SUBSCENE_SAMPLE=0 for fast-path runs.
if [ "${LQV_SMOKE_SUBSCENE_SAMPLE:-1}" = "1" ]; then
  EXCLUDE='base|__init__|services|terrain_62ha|terrain_62ha_photoreal|hdri_dusk_compare|material_wall_compare'
  SAMPLE_N="${LQV_SMOKE_SUBSCENE_N:-4}"
  mapfile -t DRIVERS < <(ls lqv/subscene/*.py 2>/dev/null \
                        | xargs -n1 basename \
                        | sed 's/\.py$//' \
                        | grep -Ev "^(${EXCLUDE})$" \
                        | shuf -n "${SAMPLE_N}")
  if [ "${#DRIVERS[@]}" -gt 0 ]; then
    echo "[smoke] subscene sample (${#DRIVERS[@]}/${SAMPLE_N}): ${DRIVERS[*]}"
    for asset in "${DRIVERS[@]}"; do
      echo "[smoke] subscene driver: $asset"
      sublog=$(mktemp)
      if ! RENDER_SKIP=1 RENDER_VARIANT=A \
           LQV_ALLOW_CPU_FALLBACK="${LQV_ALLOW_CPU_FALLBACK:-1}" \
           blender --background --python "lqv/subscene/${asset}.py" 2>&1 | tee "$sublog"; then
        echo "SMOKE TEST FAILED: subscene driver '$asset' exited non-zero" >&2
        exit 1
      fi
      if grep -q "Traceback (most recent call last)" "$sublog"; then
        echo "SMOKE TEST FAILED: traceback in subscene driver '$asset' (see output above)" >&2
        exit 1
      fi
    done
  else
    echo "[smoke] subscene sample: no eligible drivers found (skipping)" >&2
  fi
fi

echo "SMOKE TEST PASSED"
