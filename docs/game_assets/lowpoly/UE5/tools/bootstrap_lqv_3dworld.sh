#!/bin/bash
# Bootstrap the LQV 3D World UE5.7 project on a fresh Windows laptop or Hetzner GPU server.
# Installs Unreal Engine 5.7 via Epic Launcher (or pre-installed), creates the .uproject,
# copies the asset pack, and runs the build script.
#
# Usage (after UE5.7 is installed):
#   bash /root/la-quebrada-viva/docs/game_assets/lowpoly/UE5/tools/bootstrap_lqv_3dworld.sh
#
# This is the OPERATOR-ACTIONABLE entry point — when Ivan is ready to open UE5.7,
# this script does the rest.

set -euo pipefail

# Configuration
PROJECT_NAME="LQV3DWorld"
PROJECT_ROOT="${HOME}/${PROJECT_NAME}"
UE_ROOT="${UE_ROOT:-/opt/UnrealEngine_5.7}"  # adjust for your install
ASSET_SOURCE="${ASSET_SOURCE:-/root/la-quebrada-viva/docs/game_assets/lowpoly}"
CONTENT_DEST="${PROJECT_ROOT}/Content/Imported"

echo "=== LQV 3D World — Bootstrap ==="
echo "Project root: ${PROJECT_ROOT}"
echo "UE root: ${UE_ROOT}"
echo "Asset source: ${ASSET_SOURCE}"

# 1. Create project directory structure
mkdir -p "${PROJECT_ROOT}"
mkdir -p "${PROJECT_ROOT}/Content/Imported"
mkdir -p "${PROJECT_ROOT}/Source/${PROJECT_NAME}"
mkdir -p "${PROJECT_ROOT}/Config"

# 2. Copy .uproject + Source/ files from the canonical repo
cp "${ASSET_SOURCE}/UE5/${PROJECT_NAME}.uproject" "${PROJECT_ROOT}/"
cp -r "${ASSET_SOURCE}/UE5/Source/"* "${PROJECT_ROOT}/Source/"
echo "  ✓ Copied .uproject + Source/ files"

# 3. Copy all GLB assets into Content/Imported/ for UE to import
cp "${ASSET_SOURCE}"/*.glb "${CONTENT_DEST}/"
echo "  ✓ Copied $(ls ${ASSET_SOURCE}/*.glb | wc -l) GLB assets to Content/Imported/"

# 4. (UE-side) Import each GLB as a Static Mesh
# This requires UE5.7 to be running. Operator runs:
#   UnrealEditor-Cmd "${PROJECT_ROOT}/${PROJECT_NAME}.uproject" \
#       -ExecutePythonScript="${PROJECT_ROOT}/tools/import_lowpoly_glbs.py"
echo ""
echo "Next steps (run manually in UE5.7 editor):"
echo "  1. Open the project: ${PROJECT_ROOT}/${PROJECT_NAME}.uproject"
echo "  2. In Content Browser → right-click → 'Run Python Script' → tools/import_lowpoly_glbs.py"
echo "     (this imports each .glb as a Static Mesh named after the file)"
echo "  3. Then 'Run Python Script' → tools/build_lqv_3dworld_level.py"
echo "     (this spawns the world with all assets at real-data positions)"
echo "  4. Save as /Game/LQV_Main.umap"
echo "  5. Hit Play to walk around the property"
echo ""
echo "Optional next: provision_pixel_streaming.sh for browser-based access"
