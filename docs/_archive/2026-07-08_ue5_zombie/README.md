# UE5 / Unreal Engine 5.7 zombie code (archived 2026-07-08)

This directory was created when the LQV viewer pivoted from UE5 + Cesium for
Unreal (Phase 1 of the Wes-aligned plan) to web-only CesiumJS (viewer at
`escobar3d.html`). The UE5 path was never shipped: Phase 1 export scripts
were authored but never run; the build pipeline requires a Windows laptop
(UE5 Editor), a reverse-SSH bridge, and a Hetzner GPU for Pixel Streaming.

This was archived during the **v5 viewer cleanup** session. Decision: LQV's
durable deliverable is the **web viewer**, not a UE5 build. UE5 is dropped
from the roadmap for Q3 2026.

## What's here

```
docs/_archive/2026-07-08_ue5_zombie/
├── tools/                        ← UE5-specific Python + Bash scripts
│   ├── lqv_to_ue.py              ← one-pass asset pipeline (2048 heightmap, GeoJSON exports)
│   ├── build_lqv_level.py        ← UE5 Editor Python: create Cesium3DTileset, World Partition
│   ├── export_lqv_glb.py         ← Blender headless driver for cob/tatakua GLB
│   ├── export_lqv_house_minimal.py ← bypass Cycles/GPU (CPU-only fallback)
│   ├── export_lqv_modular_glb.py ← modular walls/floor/roof separate exports
│   ├── lqv_bridge_windows.ps1    ← PowerShell reverse-tunnel pc-ale → VPS:2222
│   ├── bootstrap_lqv_on_laptop.sh  ← setup UE5 on Wes's laptop
│   ├── deploy_lqv_pixstream.sh   ← Hetzner GPU Pixel Streaming deploy
│   ├── provision_hetzner_gpu.sh  ← one-shot GPU host provisioner
│   └── install_ue5_on_gpu.sh     ← UE5 installer via Epic Launcher
├── glb/                          ← 7 Blender GLB exports (14 MB Riverstone house + modules)
└── handbook/
    └── HANDOFF.md                ← original Phase 1 handoff doc
```

## Why we kept it (not deleted)

Wes + Ivan discussed keeping it because:
1. The asset pipeline (`lqv_to_ue.py` + ALOS DEM + 30m imagery) is **the seed
   of every other thing we did**. If LQV ever scales to a full game or VR
   walkthrough, this is the starting point.
2. The committed history is short (UE5 work was 4 commits July 7-8), so
   it's still easy to revive.
3. Repo is small — 1.5 MB of source code; deleting would erase team
   understanding of why we made the original pivot.

## Decision criteria to revive

Only revive if ALL are true:
- Wes funds Pixel Streaming infrastructure ($300+ USD/month recurring)
- a laptop with UE5 installed is available to maintain the project (Wes's
  or hired contractor)
- site needs > 100 simultaneous viewers (web-viewer ceiling)
- VR/AR deliverable is added to the housing-park scope

Otherwise: keep dormant. Don't accidentally drag UE5 into the web roadmap.

## What replaced it (for current work)

- Web viewer: `docs/game_assets/escobar3d.html` (committed at `9e58c7c`)
- Asset generators: `tools/lqv_fetch_esri_hd.py`, `tools/lqv_esri_z18_lod3.py`,
  `tools/lqv_hillshade_dense.py`, `tools/lqv_heightmap_lods.py`,
  `tools/lqv_lod_imagery.py` (all used by the web viewer)
