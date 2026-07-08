#!/usr/bin/env bash
# La Quebrada Viva → UE5.7 + Cesium + project bootstrap
#
# Runs on the gaming laptop after the LQV bridge tunnel is established.
# Installs UE5.7 via Epic Games Launcher, installs Cesium for Unreal plugin,
# creates the LQV_Walk.uproject, syncs assets from the VPS repo, runs the
# build script inside the UE editor.
#
# This script is INTENDED TO RUN ON THE LAPTOP, not the VPS. But it can be
# driven remotely from the VPS via the bridge tunnel:
#
#   VPS$ ssh -p 2222 root@localhost 'bash -s' < tools/bootstrap_lqv_on_laptop.sh
#
# Or copy to laptop and run manually. PowerShell variant:
#   tools/bootstrap_lqv_on_laptop.ps1

set -euo pipefail

LQV_REPO_REMOTE="https://github.com/Ai-Whisperers/la-quebrada-viva.git"
LQV_REPO_DIR="${LQV_DIR:-$HOME/lqv-dev/la-quebrada-viva}"
UE_ROOT="${UE_ROOT:-C:\\Program Files\\Epic Games\\UE_5.7}"  # Windows default
UE_LINUX_ROOT="${UE_LINUX_ROOT:-$HOME/UnrealEngine}"          # Linux alternative
PROJECT_DIR="$LQV_REPO_DIR/LQV_Walk"

echo "============================================================"
echo "LQV → UE5.7 + Cesium bootstrap"
echo "============================================================"
echo "Repo dir:    $LQV_REPO_DIR"
echo "UE root:     $UE_ROOT"
echo "Project dir: $PROJECT_DIR"
echo "============================================================"

# ---------------------------------------------------------------------------
# Step 1: Clone the LQV repo (or pull if exists)
# ---------------------------------------------------------------------------
echo ""
echo "[1/6] Cloning LQV repo..."
if [ -d "$LQV_REPO_DIR" ]; then
    cd "$LQV_REPO_DIR"
    git pull --ff-only origin master
    echo "  ✓ Repo updated"
else
    mkdir -p "$(dirname "$LQV_REPO_DIR")"
    git clone "$LQV_REPO_REMOTE" "$LQV_REPO_DIR"
    echo "  ✓ Repo cloned"
fi

# ---------------------------------------------------------------------------
# Step 2: Detect UE installation
# ---------------------------------------------------------------------------
echo ""
echo "[2/6] Detecting Unreal Engine installation..."
UE_BIN=""
if [ -f "$UE_ROOT/Engine/Binaries/Win64/UnrealEditor-Cmd.exe" ]; then
    UE_BIN="$UE_ROOT/Engine/Binaries/Win64/UnrealEditor-Cmd.exe"
    echo "  ✓ Windows UE found: $UE_BIN"
elif [ -f "$UE_LINUX_ROOT/Engine/Binaries/Linux/UnrealEditor-Cmd" ]; then
    UE_BIN="$UE_LINUX_ROOT/Engine/Binaries/Linux/UnrealEditor-Cmd"
    echo "  ✓ Linux UE found: $UE_BIN"
elif command -v UnrealEditor >/dev/null 2>&1; then
    UE_BIN="$(command -v UnrealEditor)"
    echo "  ✓ UE found in PATH: $UE_BIN"
else
    echo "  ✗ UE 5.7 not installed"
    echo ""
    echo "  Install via Epic Games Launcher (recommended for Windows):"
    echo "    1. Download Epic Games Launcher: https://www.epicgames.com/store/en-US/download"
    echo "    2. Sign in with your Epic account (or create one — it's free)"
    echo "    3. Unreal Engine → Library → Install 5.7.x (latest 5.7)"
    echo "       - Target directory: $UE_ROOT"
    echo "       - Options: Editor + Linux Build Support (for headless packaging)"
    echo "    4. Re-run this script"
    echo ""
    echo "  Or on Linux: clone the source build"
    echo "    git clone --depth=1 -b 5.7 https://github.com/EpicGames/UnrealEngine.git $UE_LINUX_ROOT"
    echo "    cd $UE_LINUX_ROOT && ./Setup.sh && ./GenerateProjectFiles.sh && make"
    echo "    (this takes 1-2 hours on a gaming laptop, 30-60 GB disk)"
    exit 1
fi

# ---------------------------------------------------------------------------
# Step 3: Install Cesium for Unreal plugin
# ---------------------------------------------------------------------------
echo ""
echo "[3/6] Installing Cesium for Unreal plugin..."
# Cesium for Unreal is distributed via the Fab marketplace inside UE
# Easiest path: download the plugin from the GitHub release and extract into
# the project's Plugins/ directory. This avoids needing the Fab plugin
# manager (which requires Epic Launcher login).

C_PLUGIN_VERSION="2.16.0"  # Update to latest — check https://github.com/CesiumGS/cesium-unreal/releases
C_PLUGIN_ZIP="$HOME/Downloads/CesiumForUnreal-${C_PLUGIN_VERSION}-win64.zip"
C_PLUGIN_URL="https://github.com/CesiumGS/cesium-unreal/releases/download/v${C_PLUGIN_VERSION}/CesiumForUnreal-${C_PLUGIN_VERSION}-win64.zip"

mkdir -p "$PROJECT_DIR/Plugins"
if [ -d "$PROJECT_DIR/Plugins/CesiumForUnreal" ]; then
    echo "  ✓ Plugin already present in $PROJECT_DIR/Plugins/"
else
    echo "  Downloading CesiumForUnreal v${C_PLUGIN_VERSION}..."
    if command -v curl >/dev/null 2>&1; then
        curl -L --fail --silent --show-error -o "$C_PLUGIN_ZIP" "$C_PLUGIN_URL"
    else
        wget -q -O "$C_PLUGIN_ZIP" "$C_PLUGIN_URL"
    fi
    echo "  Extracting..."
    if command -v unzip >/dev/null 2>&1; then
        unzip -q "$C_PLUGIN_ZIP" -d "$PROJECT_DIR/Plugins/"
    else
        powershell -Command "Expand-Archive -Path '$C_PLUGIN_ZIP' -DestinationPath '$PROJECT_DIR/Plugins/'"
    fi
    rm "$C_PLUGIN_ZIP"
    echo "  ✓ Cesium plugin installed"
fi

# ---------------------------------------------------------------------------
# Step 4: Create the LQV_Walk.uproject
# ---------------------------------------------------------------------------
echo ""
echo "[4/6] Creating LQV_Walk.uproject..."
# Generate a minimal .uproject that enables Cesium + Lumen + Nanite + Python
cat > "$PROJECT_DIR/LQV_Walk.uproject" <<'EOF'
{
    "FileVersion": 3,
    "EngineAssociation": "5.7",
    "Category": "Games",
    "Description": "La Quebrada Viva — walkable 62-ha property in Escobar, Paraguay. Photoreal arch-viz game powered by Cesium for Unreal + Nanite Landscape + Lumen GI.",
    "Modules": [
        {
            "Name": "LQV_Walk",
            "Type": "Runtime",
            "LoadingPhase": "Default",
            "AdditionalDependencies": [
                "Engine",
                "CesiumRuntime",
                "CesiumEditor",
                "CesiumForUnreal",
                "Landscape",
                "Foliage",
                "PythonScriptPlugin"
            ]
        }
    ],
    "Plugins": [
        {"Name": "CesiumForUnreal", "Enabled": true},
        {"Name": "PythonScriptPlugin", "Enabled": true},
        {"Name": "EditorScriptingUtilities", "Enabled": true},
        {"Name": "EnhancedInput", "Enabled": true},
        {"Name": "ModelingToolsEditorMode", "Enabled": true},
        {"Name": "Water", "Enabled": true},
        {"Name": "Niagara", "Enabled": true},
        {"Name": "WorldPartitionEditor", "Enabled": true},
        {"Name": "PixelStreaming", "Enabled": true}
    ],
    "TargetPlatforms": ["Windows", "Linux", "Mac"]
}
EOF

# Create the Source/LQV_Walk/ skeleton
mkdir -p "$PROJECT_DIR/Source/LQV_Walk"
cat > "$PROJECT_DIR/Source/LQV_Walk/LQV_Walk.Build.cs" <<'EOF'
using UnrealBuildTool;

public class LQV_Walk : ModuleRules
{
    public LQV_Walk(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new[] {
            "Core", "CoreUObject", "Engine", "InputCore",
            "CesiumRuntime", "Landscape", "Foliage", "Niagara", "Water",
            "EnhancedInput", "UMG", "Json", "JsonUtilities", "HTTP"
        });
        PrivateDependencyModuleNames.AddRange(new[] {
            "Slate", "SlateCore", "ProceduralMeshComponent"
        });
    }
}
EOF

cat > "$PROJECT_DIR/Source/LQV_Walk/LQV_Walk.cpp" <<'EOF'
// LQV_Walk — game module
#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

class FLQV_WalkModule : public FDefaultGameModuleImpl
{
public:
    virtual void StartupModule() override
    {
        UE_LOG(LogTemp, Display, TEXT("[LQV] Game module started"));
    }
};

IMPLEMENT_PRIMARY_GAME_MODULE(FLQV_WalkModule, LQV_Walk, "LQV_Walk");
EOF

cat > "$PROJECT_DIR/Source/LQV_Walk.Target.cs" <<'EOF'
using UnrealBuildTool;
using System.Collections.Generic;

public class LQV_WalkTarget : TargetRules
{
    public LQV_WalkTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.AddRange(new string[] { "LQV_Walk" });
    }
}
EOF

cat > "$PROJECT_DIR/Source/LQV_WalkEditor.Target.cs" <<'EOF'
using UnrealBuildTool;
using System.Collections.Generic;

public class LQV_WalkEditorTarget : TargetRules
{
    public LQV_WalkEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.AddRange(new string[] { "LQV_Walk" });
    }
}
EOF

# Create Config/DefaultEngine.ini with render settings
mkdir -p "$PROJECT_DIR/Config"
cat > "$PROJECT_DIR/Config/DefaultEngine.ini" <<'EOF'
[/Script/Engine.RendererSettings]
r.Nanite.ProjectEnabled=True
r.Nanite.Landscape=True
r.Nanite.Shadows=True
r.Nanite.MaterialID=True
r.Nanite.VirtualHeightfieldMesh=True
r.Nanite.Displacement=True
r.Nanite.Tessellation=True
r.Lumen.HardwareRayTracing=True
r.Lumen.DiffuseIndirect=True
r.Lumen.Reflections=True
r.Lumen.ScreenProbeGather=True
r.GenerateMeshDistanceFields=True
r.DynamicGlobalIlluminationMethod=1
r.ReflectionMethod=1
r.Shadow.Virtual.Enable=1
r.DefaultFeature.AutoExposure.ExtendDefaultLuminanceRange=True
r.SupportAtmosphere=True

[ConsoleVariables]
wp.Runtime.MaxLoadingLevelStreamingCells=64
wp.Runtime.HLOD=0

[CesiumForUnreal]
; Place Cesium ion access token here (sign up free at https://cesium.com/ion/tokens)
DefaultIonAccessToken=
EOF

echo "  ✓ LQV_Walk.uproject + source skeleton created"

# ---------------------------------------------------------------------------
# Step 5: Copy LQV assets into Content/LQV/Assets/
# ---------------------------------------------------------------------------
echo ""
echo "[5/6] Copying LQV assets to Content/LQV/Assets/..."
mkdir -p "$PROJECT_DIR/Content/LQV/Assets"
cp -r "$LQV_REPO_DIR/docs/game_assets/." "$PROJECT_DIR/Content/LQV/Assets/"
ASSETS_SIZE=$(du -sh "$PROJECT_DIR/Content/LQV/Assets/" | cut -f1)
echo "  ✓ Assets copied ($ASSETS_SIZE)"

# ---------------------------------------------------------------------------
# Step 6: Run the level build script inside the UE editor
# ---------------------------------------------------------------------------
echo ""
echo "[6/6] Running build_lqv_level.py inside the UE editor..."
echo "  This will: import heightmap, place Cesium anchor, place cob house,"
echo "  place waterfall, save LQV_Main level."
echo ""

# Build the editor command — runs Python script in editor headless mode
"$UE_BIN" "$PROJECT_DIR/LQV_Walk.uproject" \
    -run=pythonscript \
    -script="$LQV_REPO_DIR/tools/build_lqv_level.py" \
    -unattended \
    -nullrhi \
    -nosplash \
    -log

echo ""
echo "============================================================"
echo "✓ LQV_Walk project ready"
echo "  Project:  $PROJECT_DIR/LQV_Walk.uproject"
echo "  Level:    /Game/LQV_Main"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Open the project in UE editor:"
echo "     $UE_BIN \"$PROJECT_DIR/LQV_Walk.uproject\""
echo ""
echo "  2. (Optional) Package for Pixel Streaming:"
echo "     $UE_BIN \"$PROJECT_DIR/LQV_Walk.uproject\" \\"
echo "         -run=Cook -targetplatform=LinuxNoEditor -unattended -nullrhi"
echo ""
echo "  3. Or test locally:"
echo "     Click Play in editor → walk around LQV"
echo ""
echo "  4. For Cesium ion token (Bing aerial + Cesium World Terrain):"
echo "     Sign up free at https://cesium.com/ion/tokens"
echo "     Set in: Project Settings → Plugins → Cesium for Unreal → Default Ion Access Token"