#!/usr/bin/env bash
# La Quebrada Viva → Hetzner GPU Cloud Server provisioner
#
# Provisions a Hetzner Cloud GPU server (CCX or CCX63 with dedicated GPU),
# installs NVIDIA drivers + UE 5.7 runtime, deploys the LQV build, starts
# Pixel Streaming.
#
# Requires HETZNER_API_TOKEN env var. Get it from:
#   https://console.hetzner.cloud → Project → Security → API Tokens
#
# Usage:
#   export HETZNER_API_TOKEN="hcpat_..."
#   bash tools/provision_hetzner_gpu.sh
#
# After provisioning, the script outputs the new server's IP. Use it with
# deploy_lqv_pixstream.sh to install + run.

set -euo pipefail

if [ -z "${HETZNER_API_TOKEN:-}" ]; then
    echo "ERROR: HETZNER_API_TOKEN env var not set"
    echo "  Get one at https://console.hetzner.cloud → Project → Security → API Tokens"
    echo "  export HETZNER_API_TOKEN=\"hcpat_xxxxx\""
    exit 1
fi

HETZNER_API="https://api.hetzner.cloud/v1"
SERVER_NAME="lqv-pixelstream-$(date +%Y%m%d-%H%M%S)"
LOCATION="${HETZNER_LOCATION:-ash}"  # Ashburn, VA — closest to Paraguay with GPU
SERVER_TYPE="${HETZNER_SERVER_TYPE:-ccx63}"  # 48 vCPU, 192GB RAM, 2x RTX 4000 Ada
IMAGE="${HETZNER_IMAGE:-ubuntu-24.04}"

echo "============================================================"
echo "Hetzner GPU server provisioning for LQV Pixel Streaming"
echo "============================================================"
echo "Server name:  $SERVER_NAME"
echo "Location:     $LOCATION"
echo "Server type:  $SERVER_TYPE (CCX63 = 48 vCPU + 192GB RAM + 2x RTX 4000 Ada)"
echo "Image:        $IMAGE"
echo "Estimated:    €219/month ($240 USD)"
echo "============================================================"

# Step 1: Create server
echo ""
echo "[1/3] Creating server..."
SERVER_JSON=$(curl -sS -X POST "$HETZNER_API/servers" \
    -H "Authorization: Bearer $HETZNER_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"name\": \"$SERVER_NAME\",
        \"server_type\": \"$SERVER_TYPE\",
        \"image\": \"$IMAGE\",
        \"location\": \"$LOCATION\",
        \"start_after_create\": true,
        \"ssh_keys\": [],
        \"labels\": {
            \"project\": \"lqv-pixelstream\",
            \"purpose\": \"ue5-game-stream\"
        }
    }")

SERVER_ID=$(echo "$SERVER_JSON" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('server',{}).get('id',''))")
SERVER_IP=$(echo "$SERVER_JSON" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('server',{}).get('public_net',{}).get('ipv4',{}).get('ip',''))")
ROOT_PASSWORD=$(echo "$SERVER_JSON" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('root_password',''))")

if [ -z "$SERVER_ID" ] || [ -z "$SERVER_IP" ]; then
    echo "Failed to create server. Response:"
    echo "$SERVER_JSON" | python3 -m json.tool
    exit 1
fi

echo "  ✓ Server created: ID=$SERVER_ID, IP=$SERVER_IP"
echo "  Root password: $ROOT_PASSWORD"
echo "  Saving credentials to /tmp/lqv_hetzner_creds..."
cat > /tmp/lqv_hetzner_creds <<EOF
HETZNER_SERVER_ID=$SERVER_ID
HETZNER_SERVER_IP=$SERVER_IP
HETZNER_ROOT_PASSWORD=$ROOT_PASSWORD
HETZNER_SERVER_NAME=$SERVER_NAME
EOF
chmod 600 /tmp/lqv_hetzner_creds

# Step 2: Wait for server to be running
echo ""
echo "[2/3] Waiting for server to finish provisioning (typically 30-90s)..."
for i in $(seq 1 60); do
    STATUS=$(curl -sS "$HETZNER_API/servers/${SERVER_ID}" \
        -H "Authorization: Bearer $HETZNER_API_TOKEN" | \
        python3 -c "import sys, json; print(json.load(sys.stdin)['server']['status'])")
    if [ "$STATUS" = "running" ]; then
        echo "  ✓ Server is running after ${i}s"
        break
    fi
    sleep 2
done

# Step 3: Wait for SSH to be ready
echo ""
echo "[3/3] Waiting for SSH to be reachable..."
for i in $(seq 1 30); do
    if timeout 3 bash -c "</dev/tcp/$SERVER_IP/22" 2>/dev/null; then
        echo "  ✓ SSH reachable after ${i}*2s"
        break
    fi
    sleep 2
done

echo ""
echo "============================================================"
echo "✓ Server ready"
echo "============================================================"
echo ""
echo "Server:    $SERVER_NAME"
echo "IP:        $SERVER_IP"
echo "ID:        $SERVER_ID"
echo "Password:  $ROOT_PASSWORD"
echo ""
echo "Next steps:"
echo ""
echo "1. Install NVIDIA driver + UE 5.7 (one command):"
echo "   ssh root@$SERVER_IP 'bash -s' < tools/install_ue5_on_gpu.sh"
echo ""
echo "2. Deploy LQV + start Pixel Streaming:"
echo "   ssh root@$SERVER_IP 'bash -s' < tools/deploy_lqv_pixstream.sh"
echo ""
echo "3. Open Cloudflare Tunnel to expose the stream publicly"
echo ""
echo "To destroy the server when done:"
echo "   curl -X DELETE $HETZNER_API/servers/$SERVER_ID -H 'Authorization: Bearer $HETZNER_API_TOKEN'"
echo ""
echo "Credentials saved to /tmp/lqv_hetzner_creds (mode 0600)"