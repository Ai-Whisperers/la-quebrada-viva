#!/usr/bin/env bash
# Usage: scripts/render_preview.sh <A|B|C> <hero|stream_up|terrace|cliff|dusk|petal_macro>
# 1280x720, 128 samples -> renders/_preview_<V>_<cam>.png
set -euo pipefail
cd "$(dirname "$0")/.."

variant="${1:?usage: render_preview.sh <A|B|C> <cam>}"
cam="${2:?usage: render_preview.sh <A|B|C> <cam>}"
case "$variant" in
  A|B|C) ;;
  *) echo "Variant '$variant' not supported (A/B/C only)" >&2; exit 1 ;;
esac

[ -f scene.blend ] && cp scene.blend scene.blend.session-backup

RENDER_VARIANT="$variant" RENDER_CAM="$cam" RENDER_SAMPLES=128 RENDER_RES=preview \
  blender --background --python build_scene.py

out="renders/_preview_${variant}_${cam}.png"
[ -f "$out" ] || { echo "FAILED: expected output $out not found" >&2; exit 1; }
echo "PREVIEW OK: $out"
