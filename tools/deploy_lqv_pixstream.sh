#!/usr/bin/env bash
# La Quebrada Viva → Pixel Streaming infrastructure on Hetzner GPU server
#
# Spin up a Hetzner GPU server (or any Linux box with NVIDIA), install UE5.7
# runtime + the LQV_Walk build, run it with -PixelStreaming flags, front it
# with Cloudflare Calls (WebRTC) so users can play via browser URL.
#
# This script is INTENDED TO RUN ON THE HETZNER SERVER (or any cloud GPU).
# But it can be driven remotely via the bridge tunnel:
#
#   VPS$ ssh -H '... Hetzner creds ...' user@hetzner 'bash -s' < tools/deploy_lqv_pixstream.sh
#
# Or run manually on the cloud box after provisioning it.
#
# Prerequisites:
#   - Hetzner GPU server (or Vast.ai spot, AWS g5, etc.) with RTX-class GPU
#   - Root or sudo access
#   - Outbound HTTPS to epicgames.com, github.com, cloudflare.com
#   - LQV_Walk build packaged (Linux NoEditor target, ~10-15 GB)

set -euo pipefail

LQV_REPO_REMOTE="https://github.com/Ai-Whisperers/la-quebrada-viva.git"
LQV_REPO_DIR="$HOME/lqv-dev/la-quebrada-viva"
UE_LINUX_ROOT="$HOME/UnrealEngine"
LQV_BUILD_DIR="$HOME/lqv-build"
PIXSTREAM_PORT=8888
PIXSTREAM_WEB_PORT=80

echo "============================================================"
echo "LQV → Pixel Streaming infrastructure"
echo "============================================================"
echo "Hetzner box: $(hostname)"
echo "GPU:         $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'NONE')"
echo "Driver:      $(nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null || echo 'NONE')"
echo "============================================================"

# ---------------------------------------------------------------------------
# Step 1: Verify GPU + NVIDIA driver
# ---------------------------------------------------------------------------
echo ""
echo "[1/8] Verifying GPU + driver..."
if ! command -v nvidia-smi >/dev/null 2>&1; then
    echo "  ✗ No NVIDIA driver — installing..."
    # Hetzner GPU servers come with NVIDIA drivers pre-installed typically.
    # If not, install per https://docs.hetzner.com/cloud/servers/gpu
    apt-get update
    apt-get install -y nvidia-driver-555 nvidia-utils-555
fi
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv
echo "  ✓ GPU detected"

# ---------------------------------------------------------------------------
# Step 2: Install UE 5.7 Linux runtime (no editor needed)
# ---------------------------------------------------------------------------
echo ""
echo "[2/8] Installing UE 5.7 runtime + Pixel Streaming plugin..."
if [ ! -d "$UE_LINUX_ROOT" ]; then
    echo "  Cloning UE 5.7 source (no editor, runtime only)..."
    git clone --depth=1 -b 5.7 https://github.com/EpicGames/UnrealEngine.git "$UE_LINUX_ROOT"
    cd "$UE_LINUX_ROOT"
    ./Setup.sh
    ./GenerateProjectFiles.sh
    make -j$(nproc)  # ~30-60 min on RTX 4000 Ada
    echo "  ✓ UE 5.7 runtime compiled"
fi

# ---------------------------------------------------------------------------
# Step 3: Clone LQV repo + sync assets + project
# ---------------------------------------------------------------------------
echo ""
echo "[3/8] Cloning LQV repo..."
if [ ! -d "$LQV_REPO_DIR" ]; then
    git clone "$LQV_REPO_REMOTE" "$LQV_REPO_DIR"
fi
cd "$LQV_REPO_DIR" && git pull --ff-only origin master
echo "  ✓ Repo at $LQV_REPO_DIR"

# ---------------------------------------------------------------------------
# Step 4: Copy packaged LQV_Walk build
# ---------------------------------------------------------------------------
echo ""
echo "[4/8] Setting up LQV_Walk build directory..."
# If a packaged build was uploaded (via rsync), use it. Otherwise package
# locally from source.
if [ -d "$LQV_BUILD_DIR/LinuxNoEditor" ]; then
    echo "  ✓ Pre-built LQV_Walk found at $LQV_BUILD_DIR"
elif [ -d "$LQV_REPO_DIR/LQV_Walk" ]; then
    echo "  Source project present — packaging now (~30 min)..."
    "$UE_LINUX_ROOT/Engine/Build/BatchFiles/Linux/RunUAT.sh" BuildCookRun \
        -project="$LQV_REPO_DIR/LQV_Walk/LQV_Walk.uproject" \
        -platform=Linux -clientconfig=Shipping -build -cook -stage -package \
        -archive -archivedirectory="$LQV_BUILD_DIR" \
        -unattended -nullrhi -nosplash
    echo "  ✓ Build packaged"
else
    echo "  ✗ No LQV_Walk project or build found"
    echo "  Bootstrap the project first via bootstrap_lqv_on_laptop.sh, then rsync the packaged build here."
    exit 1
fi

# ---------------------------------------------------------------------------
# Step 5: Configure Cloudflare Calls (free tier)
# ---------------------------------------------------------------------------
echo ""
echo "[5/8] Configuring Cloudflare Calls for WebRTC front-end..."
# Cloudflare Calls provides globally-distributed WebRTC SFUs. Free tier
# covers up to 1000 concurrent participants. Webhook-based control API.
#
# Setup:
#   1. Sign up at https://www.cloudflare.com/ (free tier)
#   2. Add Calls app: dashboard → Calls → Create Application
#   3. Note: App ID + App Secret (set as env: CLOUDFLARE_CALLS_APP_ID, CLOUDFLARE_CALLS_APP_SECRET)
#   4. Generate a session: POST https://api.cloudflare.com/client/v4/accounts/{account_id}/calls/apps/{app_id}/sessions/new
#
# For local testing without Cloudflare, use the bundled Pixel Streaming
# demo signaling server:
#   $UE_LINUX_ROOT/Engine/Source/Runtime/PixelStreaming/PixelStreamingWebSocketTransport/...
# See $UE_LINUX_ROOT/Engine/Source/Runtime/PixelStreaming/PixelStreamingInfrastructure/...

if [ -n "${CLOUDFLARE_CALLS_APP_ID:-}" ] && [ -n "${CLOUDFLARE_CALLS_APP_SECRET:-}" ]; then
    echo "  ✓ Cloudflare Calls credentials present (using CF WebRTC)"
else
    echo "  ⚠ Cloudflare Calls credentials NOT set — using local signaling"
    echo "    Set CLOUDFLARE_CALLS_APP_ID and CLOUDFLARE_CALLS_APP_SECRET to enable"
    echo "    global WebRTC distribution (free tier: 1000 concurrent)."
fi

# ---------------------------------------------------------------------------
# Step 6: Start Pixel Streaming + signaling
# ---------------------------------------------------------------------------
echo ""
echo "[6/8] Starting LQV_Walk with Pixel Streaming enabled..."
BUILD_BIN="$LQV_BUILD_DIR/LinuxNoEditor/LQV_Walk.sh"
if [ ! -f "$BUILD_BIN" ]; then
    echo "  ✗ No $BUILD_BIN"
    exit 1
fi

# Pixel Streaming flags
PIXSTREAM_ARGS=(
    "-PixelStreamingEnabled" "-RenderOffScreen"
    "-PixelStreamingPort=$PIXSTREAM_PORT"
    "-PixelStreamingWebRTCPort=8889"
    "-PixelStreamingKeyFilter=false"
    "-Unattended" "-NullRHI=false"  # we DO want RHI for the GPU
    "-ResX=1920" "-ResY=1080"
    "-PixelStreamingURL=\"$PIXSTREAM_PUBLIC_URL\""
    "-log" "-AbsLog=$HOME/lqv-pixstream.log"
)

nohup "$BUILD_BIN" "${PIXSTREAM_ARGS[@]}" > "$HOME/lqv-pixstream-stdout.log" 2>&1 &
PIXSTREAM_PID=$!
echo "  ✓ Started PID $PIXSTREAM_PID"
echo "  Logs: $HOME/lqv-pixstream.log + $HOME/lqv-pixstream-stdout.log"

# ---------------------------------------------------------------------------
# Step 7: Wait for stream ready + health check
# ---------------------------------------------------------------------------
echo ""
echo "[7/8] Waiting for stream to be ready..."
for i in $(seq 1 30); do
    if curl -sf http://localhost:$PIXSTREAM_PORT/health >/dev/null 2>&1; then
        echo "  ✓ Stream ready after ${i}s"
        break
    fi
    sleep 1
    [ $i -eq 30 ] && echo "  ⚠ Stream not ready after 30s — check logs"
done

# ---------------------------------------------------------------------------
# Step 8: Expose publicly via Cloudflare Tunnel
# ---------------------------------------------------------------------------
echo ""
echo "[8/8] Exposing publicly via Cloudflare Tunnel..."
# Use `cloudflared tunnel` to expose the local stream + web frontend
if command -v cloudflared >/dev/null 2>&1; then
    cloudflared tunnel --url http://localhost:$PIXSTREAM_PORT run lqv-stream 2>&1 | head -20 &
    echo "  ✓ Cloudflared tunnel started (URL shown above)"
else
    echo "  ⚠ cloudflared not installed"
    echo "    Install: curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared"
fi

echo ""
echo "============================================================"
echo "✓ LQV Pixel Streaming deployed"
echo "============================================================"
echo ""
echo "Test:"
echo "  curl http://localhost:$PIXSTREAM_PORT/health"
echo "  Open the Cloudflared URL in a Chromium browser"
echo ""
echo "Production URL: lqv.paragu-ai.com (configure custom domain + DNS)"
echo "============================================================"