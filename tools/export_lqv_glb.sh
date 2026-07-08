#!/usr/bin/env bash
# La Quebrada Viva → Blender headless GLB export for Unreal Engine 5.7
#
# Re-uses the existing bpy scripts in lqv/house/ to build the same Cob/Bottle/
# Tatakua/Bamboo house that the Cycles renders use, then exports each scene
# (or selected objects) as a .glb file in docs/game_assets/glb/.
#
# Output:
#   docs/game_assets/glb/riverstone_cob.glb          (~3-8 MB, full U-cob house)
#   docs/game_assets/glb/tatakua.glb                 (~200 KB, oven)
#   docs/game_assets/glb/bamboo_wigwam.glb           (~150 KB, single typology)
#   docs/game_assets/glb/full_scene_riverstone.glb   (~30-60 MB, everything)
#
# Usage:
#   bash tools/export_lqv_glb.sh [variant]   # default A
#
# variant: A (winter golden hour), B (autumn afternoon), C (night blue hour)

set -euo pipefail

REPO_ROOT="/root/la-quebrada-viva"
GLB_DIR="$REPO_ROOT/docs/game_assets/glb"
mkdir -p "$GLB_DIR"

VARIANT="${1:-A}"
echo "Building LQV scene (variant=$VARIANT) → exporting GLB..."

# Run Blender headless, build the scene, export the whole thing as GLB
# (Cesium for Unreal + UE5 want the full scene in one GLB for the house
#  placement; individual props can be exported separately by selecting
#  before exporting)

RENDER_VARIANT="$VARIANT" blender --background \
    --python "$REPO_ROOT/tools/export_lqv_house_minimal.py" \
    --python-exit-code 1 \
    -- \
    --out-dir "$GLB_DIR" --variant "$VARIANT"

echo ""
echo "✓ Wrote $GLB_DIR/full_scene_riverstone_$VARIANT.glb"
ls -lh "$GLB_DIR/"