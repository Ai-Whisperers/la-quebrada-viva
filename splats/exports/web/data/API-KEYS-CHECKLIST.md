# LQV / Paraguay-AI · API Keys Checklist

**Last updated 2026-06-30 00:10 UTC.** Pasted keys go to `~/.lqv/splats.env` (mode 0600).

**Status: production-ready** — VastAI smoke rental verified end-to-end (launched + SSH'd + gsplat importable + destroyed cleanly). Cesium ion wired into the buyer viewer. R2 S3 pipeline operational. The remaining unblocked work is non-key: see the "what else to ship" section.


---

## Status table (verified working)

| Key | Status | Last verified |
|---|---|---|
| **VASTAI_API_KEY** | ✅ verified | 2026-06-29 23:30 — returns GPU offers, account $10 credit, balance $0, smoke rental 43154112 launched+destroyed |
| **SSH key on vast.ai** | ✅ verified | 2026-06-29 23:30 — id 1033107 in vast.ai account |
| **R2 S3 keys** | ✅ verified | 2026-06-29 — list/upload/download/delete all work via boto3 |
| **CESIUM_ION_TOKEN** | ✅ verified | 2026-06-29 23:25 — returns 11 assets. Now wired into the page: "Explore in 3D" panel with Cesium World Terrain + Esri satellite imagery |
| **Cloudflare account ID** | ✅ known | `9eb1832f3e42a1dbd6ba854f8d6a1cb2` |
| **Sentinel Hub client** | ❌ deprecated 2026 | Migrated to Planet Insights; deferring |
| **Google Maps API key** | ⏳ operator-side secret | Two keys visible in console ("New Maps Platform API Key" May 11 + "Maps Platform API Key" Apr 14); need actual secret value |
| **NASA FIRMS key** | ⏳ optional | Free, unlocks fire overlay |
| **SSH key on vast.ai account** | ✅ verified | 2026-06-29 23:30 — launched rental 43154112, SSH'd in, ran tooling, destroyed |
| **R2 S3 keys** | ✅ verified | 2026-06-29 23:00 — list/upload/download/delete cycle works via boto3 |
| **Cloudflare account ID** | ✅ known | `9eb1832f3e42a1dbd6ba854f8d6a1cb2` |
| **CESIUM_ION_TOKEN** | ✅ verified | 2026-06-29 23:25 — returns 11 assets. Now wired into the page: "Explore in 3D" panel with Cesium World Terrain + Esri satellite imagery |
| **Google Maps API key** | ⏳ awaiting paste | Your project "Veterinaria" is set up |
| **Sentinel Hub client_id + secret** | ⏳ awaiting paste | Your account is linked; OAuth client not generated yet |

---

## ✅ Already done — the pipeline is now end-to-end verified

### Vast.ai (full pipeline)
- **Account:** weissvanderpol.ivan@gmail.com (Paraguay)
- **API key:** saved as `VASTAI_API_KEY` in `~/.lqv/splats.env` (chmod 600)
- **SSH key registered:** `ed25519 hermes-agent@deploy` — id 1033107 in the vast.ai account
- **Verified end-to-end on 2026-06-29 23:30 UTC:**
  - Launched rental ID **43154112** (Tesla V100 32GB, $0.0297/hr)
  - SSH'd in via `ssh3.vast.ai:34112` (BatchMode auth worked)
  - Confirmed: `nvidia-smi` shows GPU, `torch.cuda.is_available() = True`
  - Installed and imported `gsplat` + `pycolmap` (both load cleanly)
  - Destroyed rental cleanly (no charge yet — Vast bills weekly)
- **CLI:** `vastai` v1.1.3 installed at `/root/.lqv/splat_venv/bin/vastai`
- **Tool:** `splats/tools/self_host_train.py` has `status`, `submit`, `fetch` subcommands

### Cloudflare R2 (wes3dassets bucket)
- **S3-compatible keys** generated at https://dash.cloudflare.com → R2 → Manage R2 API Tokens
- **Token:** `[REDACTED — paste in chat to receive]` (`R2_MGMT_TOKEN`, dashboard-level)
- **Access Key ID:** `[REDACTED — paste in chat to receive]` (`R2_ACCESS_KEY_ID`, S3)
- **Secret Access Key:** `[REDACTED — paste in chat to receive]` (`R2_SECRET_ACCESS_KEY`)
- **Endpoint:** `https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com`
- **Bucket:** `wes3dassets` (created today, empty)
- **Verified end-to-end:** upload → read back → delete all work via boto3
- **Other buckets on this account:** ai-whisperers-backups, magnolia-peluqueria, tony-video-assets
- **Three.js export wired:** `python3 threejs_export.py --upload-to-r2 --r2-prefix splats/lqv` uploads outputs to R2

### Cesium ion
- **Token:** saved as `CESIUM_ION_TOKEN` in `splats.env`
- **Account:** ivan-weiss (Cesium ID 450528)
- **Scopes:** archives:r/w, assets:read/limited-list/list/source/write, exports:r/w, geocode, labels:r/w, profile:read, tokens:r/w
- **Verified:** 11 assets available (Cesium World Terrain, Bing Maps Aerial, Bing Aerial with Labels, etc.)
- **Use case:** 3D Tiles streaming + high-res LiDAR terrain for the buyer viewer (currently flat 2D composite)
- **Note:** This is **free tier 5 GB/mo** — enough for the low-traffic buyer pre-sales page

### SSH key
- **Public key** at `/root/.ssh/id_ed25519.pub` — registered with vast.ai (id 1033107)
- **`ssh -p <port> root@<host>`** works (verified end-to-end 2026-06-29 23:30)

---

## ⏳ Operator actions needed (in order of unlock value)

### ~~1. Sentinel Hub OAuth client~~ — DEPRECATED 2026

Sentinel Hub Dashboard is being deprecated. Migrating workflows to Planet Insights Platform if needed. For now, the 0.25%-sample canopy dataset is what we have; full reclassification is deferred until/unless Planet integration is needed.

### 1. Google Maps API key (P3 — 5 minutes, blocks no current work)
1. Visit https://console.cloud.google.com/google/maps-apis/credentials
2. Select project "Veterinaria" (your existing project)
3. APIs → enable "Maps JavaScript API" and "Street View Static API"
4. Create credentials → API key
5. Restrict to your domain (e.g. *.paragu-ai.com)
6. Paste here: `GOOGLE_MAPS_API_KEY=...`

### 2. (Optional) NASA FIRMS Map Key (free, 5 minutes)
1. Visit https://firms.modaps.eosdis.nasa.gov/api/
2. Click "Request API key" → enter email → get the key
3. Paste: `FIRMS_MAP_KEY=...`

---

## 🔐 Security

| Item | Action |
|---|---|
| **R2 S3 keys** in `splats.env` | Full object R/W on all 4 buckets (wes3dassets, ai-whisperers-backups, magnolia-peluqueria, tony-video-assets). Consider **rotating** after the rental dry-run (1-click in the R2 Tokens UI) |
| **VastAI API key** | Has full account scope. Don't paste in shell history. |
| **Cesium ion token** | Free tier, 5 GB/mo quota. Manage scopes at https://ion.cesium.com |
| **`splats.env` permissions** | `chmod 600`, owned by root, only readable by Hermes agent |

---

## 🔐 Paste protocol

When you have a key, **paste it directly in chat**. I'll move it into `~/.lqv/splats.env` (chmod 600) within ~30 seconds and run a verification call.

**Never paste keys in shell-history-exposing form** (e.g. `KEY=*** echo $KEY`). Plain text is fine; the agent picks it up and writes it to disk.

```bash
VASTAI_API_KEY=abc123def456...
```

---

## 📊 Key reference — what each key unlocks

| Priority | Service | Sign-up URL | What it unlocks | Cost | Status |
|---|---|---|---|---|---|
| **P0** | Vast.ai (GPU rental) | https://vast.ai/account | Trains Gaussian Splatting models | ~$0.40/hr | ✅ Done |
| **P0** | Vast.ai SSH key | https://vast.ai/account → SSH Keys | Worker can deploy + run gsplat | Free | ✅ Done |
| **P1** | Cesium ion | https://ion.cesium.com/ | 3D Tiles streaming + LiDAR terrain | Free 5 GB/mo | ✅ Done |
| ~~P1~~ | ~~Sentinel Hub~~ | ~~DEPRECATED 2026 — moved to Planet Insights Platform~~ | Migrated to Planet if needed; for now use existing 0.25%-sample canopy | $100/mo if reactivated | ❌ deprecated |
| **P1** | Cloudflare R2 S3 keys | https://dash.cloudflare.com → R2 → Manage R2 API Tokens | Free egress for 20-50 MB splat outputs | Free 10 GB + 10M reads | ✅ Done |
| **P2** | Maxar/DigitalGlobe | https://discover.digitalglobe.com/ | Sub-1m satellite imagery | $2,800/tasking | 💰 defer |
| **P2** | NASA FIRMS | https://firms.modaps.eosdis.nasa.gov/api/ | Fire hotspot overlay | Free | ⏳ optional |
| **P3** | Google Maps (Veterinaria) | https://console.cloud.google.com/google/maps-apis/credentials | Street View of approach road | Free $200/mo credit | ⏳ awaiting |

---

## ✅ What's now end-to-end runnable

```bash
# After SSH key is added to vast.ai account, this works:
source /root/.lqv/splats.env
vastai show user                               # ✓ returns account info
vastai show instances                           # ✓ 0 (rental destroyed)
vastai search offers 'rentable=true' --limit 10 # ✓ cheapest V100 at $0.021/hr
vastai create instance 38450935 \
  --image pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime \
  --disk 30 --ssh                                # ✓ SSH-mode rental launched
ssh -p <port> -i /root/.ssh/id_ed25519 root@ssh3.vast.ai  # ✓ auth works
vastai destroy instance <id>                     # ✓ destroyed cleanly

# gsplat pipeline (verified 23:30 UTC on the smoke test rental)
pip install gsplat pycolmap
python3 -c "from gsplat.rendering import rasterization; import pycolmap"  # ✓ works

# R2 pipeline
python3 threejs_export.py --upload-to-r2 --r2-prefix splats/lqv  # ✓ uploads outputs

# Cesium pipeline (for the Three.js buyer viewer)
curl https://api.cesium.com/v1/assets -H "Authorization: Bearer $CESIUM_ION_TOKEN"  # ✓ returns 11 assets

# Cloudflare Pages deploy (every asset 200 OK)
curl https://lqv-walkthrough.pages.dev  # ✓ buyer page live
```


---

## 🚧 What's worth shipping WITHOUT new keys

The Cesium viewer is now live in the page. These are the next non-key improvements:

| Item | Effort | Impact |
|---|---|---|
| Crop `polygon_ndvi_quicklook.webp` to remove the 64% white margins | 5 min | Card image ratio improves |
| Add a real "share this view" link using `?layer=trees_estimated,streams` URL params | 15 min | Sales outreach can send specific views |
| Add a footer/imprint (operator's name, contact, "this is not a binding offer") | 15 min | Polish for first real buyer view |
| Build a "data freshness" badge per data card (last updated, source date) | 20 min | Trust signal — buyers see the data isn't 5 years stale |
| Wire `self_host_train.py` to auto-trigger when captures arrive in `splats/captures/<new_date>/` | 30 min | Wes arrives → 30s later training launches |
| Set up `splats.lqv.paragu-ai.com` as a R2 CDN-backed custom domain | 1 hr | 10× faster page load + future .ply file hosting |
