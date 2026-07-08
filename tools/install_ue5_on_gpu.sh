#!/usr/bin/env bash
# La Quebrada Viva → UE 5.7 + NVIDIA driver + dev tools installer (Ubuntu 24.04)
#
# Run on a fresh Hetzner/Vast.ai GPU server with NVIDIA RTX-class GPU.
# This is the "what bootstrap_lqv_on_laptop.sh does for Windows, but for
# a Linux GPU server".
#
# Steps:
#   1. Update apt + install dev tools (build-essential, cmake, git, etc.)
#   2. Install NVIDIA driver (proprietary, latest stable)
#   3. Install CUDA toolkit 12.x (for UE shader compilation)
#   4. Clone UE 5.7 source (Linux runtime, no editor)
#   5. Run Setup.sh + GenerateProjectFiles.sh
#   6. Compile UE5 runtime (make -j$(nproc), ~30 min on RTX 4000 Ada)
#   7. Clone LQV repo
#   8. Bootstrap the LQV_Walk project
#
# Total time: ~45-60 min on RTX 4000 Ada / RTX 4090
# Disk: ~50 GB after install
#
# Run:
#   ssh root@<server-ip> 'bash -s' < tools/install_ue5_on_gpu.sh

set -euo pipefail

echo "============================================================"
echo "LQV → UE5.7 install on GPU server (Ubuntu 24.04)"
echo "============================================================"

# Step 1: Dev tools
echo ""
echo "[1/8] Installing dev tools..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y --no-install-recommends \
    build-essential cmake git wget curl ca-certificates \
    python3 python3-pip python3-venv \
    libvulkan1 mesa-utils \
    clang llvm \
    unzip p7zip-full \
    htop nvtop
echo "  ✓ Dev tools installed"

# Step 2: NVIDIA driver
echo ""
echo "[2/8] Installing NVIDIA driver..."
if ! command -v nvidia-smi >/dev/null 2>&1; then
    apt-get install -y --no-install-recommends nvidia-driver-555 nvidia-utils-555
fi
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv
echo "  ✓ NVIDIA driver installed"

# Step 3: CUDA toolkit (for UE shader compilation)
echo ""
echo "[3/8] Installing CUDA toolkit 12.x..."
if [ ! -d /usr/local/cuda ]; then
    wget -q https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb
    dpkg -i cuda-keyring_1.1-1_all.deb
    apt-get update -y
    apt-get install -y --no-install-recommends cuda-toolkit-12-6
    rm cuda-keyring_1.1-1_all.deb
fi
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> /etc/profile.d/cuda.sh
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> /etc/profile.d/cuda.sh
source /etc/profile.d/cuda.sh
nvcc --version | head -3
echo "  ✓ CUDA installed"

# Step 4: UE 5.7 source
echo ""
echo "[4/8] Cloning UE 5.7 source..."
UE_ROOT="$HOME/UnrealEngine"
if [ ! -d "$UE_ROOT" ]; then
    # UE source requires Epic Games account linked to GitHub
    # If the server doesn't have it, this will fail with auth error
    git clone --depth=1 -b 5.7 https://github.com/EpicGames/UnrealEngine.git "$UE_ROOT"
fi
echo "  ✓ UE source at $UE_ROOT"

# Step 5: Setup UE
echo ""
echo "[5/8] Running UE Setup.sh..."
cd "$UE_ROOT"
./Setup.sh 2>&1 | tail -20
echo "  ✓ UE setup complete"

# Step 6: Generate project files
echo ""
echo "[6/8] Generating project files..."
./GenerateProjectFiles.sh 2>&1 | tail -10
echo "  ✓ Project files generated"

# Step 7: Compile UE5 (long-running)
echo ""
echo "[7/8] Compiling UE5 runtime (this takes 20-40 min)..."
make -j$(nproc) 2>&1 | tail -20
echo "  ✓ UE5 compiled"

# Step 8: Clone LQV repo
echo ""
echo "[8/8] Cloning LQV repo..."
LQV_DIR="$HOME/lqv-dev/la-quebrada-viva"
if [ ! -d "$LQV_DIR" ]; then
    mkdir -p "$(dirname "$LQV_DIR")"
    git clone https://github.com/Ai-Whisperers/la-quebrada-viva.git "$LQV_DIR"
fi
cd "$LQV_DIR" && git pull --ff-only origin master

echo ""
echo "============================================================"
echo "✓ UE 5.7 + NVIDIA + CUDA + LQV repo all installed"
echo "============================================================"
echo ""
echo "Next: bootstrap the LQV_Walk project"
echo "  cd $LQV_DIR"
echo "  bash tools/bootstrap_lqv_on_laptop.sh"
echo ""
echo "Then package for Pixel Streaming"
echo "  bash tools/deploy_lqv_pixstream.sh"
echo "============================================================"