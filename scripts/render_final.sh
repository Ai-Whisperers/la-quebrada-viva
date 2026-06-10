#!/usr/bin/env bash
# Usage: scripts/render_final.sh <A|B> <hero|stream_up|terrace|cliff|dusk|petal_macro>
# Samples policy: hero cam 512 @ 2560x1440, all others 256 @ 1920x1080.
set -euo pipefail
cd "$(dirname "$0")/.."

variant="${1:?usage: render_final.sh <A|B> <cam>}"
cam="${2:?usage: render_final.sh <A|B> <cam>}"
case "$variant" in
  A|B) ;;
  *) echo "Variant '$variant' not supported (C is not implemented — see STATUS.md)" >&2; exit 1 ;;
esac

if [ "$cam" = "hero" ]; then
  samples=512; res=hero
else
  samples=256; res=final
fi

[ -f scene.blend ] && cp scene.blend scene.blend.session-backup

RENDER_VARIANT="$variant" RENDER_CAM="$cam" RENDER_SAMPLES="$samples" RENDER_RES="$res" \
  blender --background --python build_scene.py

out="renders/${variant}_${cam}.png"
[ -f "$out" ] || { echo "FAILED: expected output $out not found" >&2; exit 1; }
echo "FINAL OK: $out (${samples} samples, ${res})"
