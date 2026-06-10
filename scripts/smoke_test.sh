#!/usr/bin/env bash
# Build the full scene without rendering. Run after any code edit.
set -euo pipefail
cd "$(dirname "$0")/.."

[ -f scene.blend ] && cp scene.blend scene.blend.session-backup

log=$(mktemp)
if ! RENDER_SKIP=1 RENDER_RES=preview RENDER_VARIANT="${RENDER_VARIANT:-A}" \
     blender --background --python build_scene.py 2>&1 | tee "$log"; then
  echo "SMOKE TEST FAILED: blender exited non-zero" >&2
  exit 1
fi
if grep -q "Traceback (most recent call last)" "$log"; then
  echo "SMOKE TEST FAILED: Python traceback during build (see output above)" >&2
  exit 1
fi
echo "SMOKE TEST PASSED"
