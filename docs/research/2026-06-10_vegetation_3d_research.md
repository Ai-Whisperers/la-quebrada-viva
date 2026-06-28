# Vegetation 3D Research — Atlantic Forest (La Quebrada Viva)

Date: 2026-06-10
Project: house-field (La Quebrada Viva)
Scope: Identify ready-to-use 3D assets for the 7 procedural species already wired in `lqv/flora/` (pindo, lapacho, mango, fern, bamboo, agave, anthurium), pick a Sketchfab download pipeline, and produce a reproducible batch-fetch script.

> **Headline finding:** 7 of the 10 GitHub repos in the original research list are **404 (deleted or moved)**. The project already has a curated Sketchfab shortlist for **6/7 species** in `CREDITS.md` — the real gap is **lapacho** and the **download pipeline itself** (the historical `nicoptere/sketchfab_downloader` is gone). The correct tool is the **Sketchfab Data API v3**, scripted in Python.

---

## 1. Repo inventory (18 entries: 15 GitHub + 3 web)

Verdict legend: **ADOPT** = use as-is, **REFERENCE** = read/study code but don't depend, **SKIP** = dead, wrong target, or stale.

### GitHub repos (research-targeted + discovered)

| # | Repo | URL | Last activity | Stars | License | One-liner | Verdict |
|---|------|-----|--------------|------:|---------|-----------|---------|
| 1 | `MaximeHerpin/modular_tree` | https://github.com/MaximeHerpin/modular_tree | 2021-12-11 (v4.0.2) | 1.3k | GPL-3.0 | "Mtree" — C++ + Python tree-mesh library with Blender addon. Function-tree → ManifoldMesher pipeline. Gold standard. | **ADOPT** |
| 2 | `friggog/tree-gen` | https://github.com/friggog/tree-gen | 2025-07-11 (active) | 938 | GPL-3.0 (code) / unrestricted (output) | Procedural tree models via parametric L-system + leaf shapes, full UI. Models generated are free for any use. | **ADOPT** |
| 3 | `Poly-Haven/polyhavenassets` | https://github.com/Poly-Haven/polyhavenassets | 2025-11-26 (v1.2.1) | 488 | GPL-3.0 | Blender add-on integrating Poly Haven into Asset Browser. Paid via Patreon/Superhive; unlocks free at 5000 patrons. | **ADOPT** |
| 4 | `aachman98/Sorcar` | https://github.com/aachman98/Sorcar | 2020-09-14 (v3.2.1) | 1.2k | GPL-3.0 | Houdini-style procedural node editor for Blender. 250+ nodes. No new release in 5y but code still works on Blender 2.81+. | **REFERENCE** |
| 5 | `Poly-Haven/Public-API` | https://github.com/Poly-Haven/Public-API | active (223 commits) | 59 | AGPL-3.0 | Public REST API powering polyhaven.com. Use for scripted CC0 download, not for scraping the JS site. | **ADOPT** |
| 6 | `PacktPublishing/Blender-to-Unreal-Engine---3D-Plants-and-Vegetation` | https://github.com/PacktPublishing/Blender-to-Unreal-Engine---3D-Plants-and-Vegetation | 2025-06-04 | 5 | repo:CC (book assets) | Packt book companion: Blender→UE pipeline for plants. Code samples for LOD, instancing, wind shaders. | **REFERENCE** |
| 7 | `jacobcjohnston/Easy-Tree` | https://github.com/jacobcjohnston/Easy-Tree | 2025-07-18 | 14 | GPL-3.0 | Geometry Nodes tree generator, Blender 4.5+, ships CC0 bark/leaf textures from ambientCG. | **REFERENCE** |
| 8 | `YuutoSeki/treegen-llm` | https://github.com/YuutoSeki/treegen-llm | 2025-09-09 | 3 | (check) | LLM-prompt → tree geometry via Geometry Nodes. Cool, but experimental. | **SKIP** (too speculative) |
| 9 | `kinotus/MaisemaBIM` | https://github.com/kinotus/MaisemaBIM | 2023-12-16 | 2 | (check) | Vegetation model alternative versions, GLB format, tagged `blender/vegetation/glb`. Useful as a multi-LOD dataset. | **REFERENCE** |
| 10 | `ZAKFUN35/FractalForge` | https://github.com/ZAKFUN35/FractalForge | 2026-05-01 (vP-A.0.0.1) | 1 | (check) | Blender 4.0+ procedural vegetation addon: grass/clover/chamomile patches, LOD generator, foliage auto-normals, butcher tool. Newest entry. | **REFERENCE** |
| 11 | `iLambda/polyflora` | https://github.com/iLambda/polyflora | 2024-11-06 | 1 | (check) | TypeScript low-poly tree/vegetation generator. Browser output, low-poly style. | **REFERENCE** (stylized only) |
| 12 | `SimonFinnie/Procedurally-Generated-Tree-Houses` | https://github.com/SimonFinnie/Procedurally-Generated-Tree-Houses | 2017-11-18 | 6 | (check) | Procedural tree-houses, LotR-flavored. | **SKIP** (off-topic, ancient) |
| 13 | `Kevin-Caldwell/Procedural-Trees` | https://github.com/Kevin-Caldwell/Procedural-Trees | 2022-02-06 | 1 | (check) | Tiny Blender addon. | **SKIP** (stale, 1★) |
| 14 | `Tyler-Duckworth/mtree` | https://github.com/Tyler-Duckworth/mtree | 2021-04-26 | 2 | (check) | Procedural tree node solution. **Superseded by #1** (MaximeHerpin/modular_tree is the maintained version — same lineage). | **SKIP** |
| 15 | `benspinelli/PGTP` | https://github.com/benspinelli/PGTP | 2014-05-27 | 2 | (check) | Old procedural tree plugin. | **SKIP** (11y old) |
| – | `nicoptere/sketchfab_downloader` | https://github.com/nicoptere/sketchfab_downloader | **404 — deleted** | – | – | Was the canonical Python Sketchfab scraper. No longer available; gone from PyPI too. | **SKIP** (use Data API instead) |
| – | `poly-haven/asset-packs` | https://github.com/poly-haven/asset-packs | **404** | – | – | Never existed; assets are served via polyhaven.com + Public-API, not a git repo. | **SKIP** |
| – | `nicoptere/blosm` | https://github.com/nicoptere/blosm | **404** | – | – | Was OSM building-from-OSM Blender addon (off-topic anyway). | **SKIP** |
| – | `bnpr/Blender-Asset-Creator` | https://github.com/bnpr/Blender-Asset-Creator | **404** | – | – | Likely renamed. Use Sorcar (#4) instead. | **SKIP** |
| – | `Handiboi/blender-vegetation-tools` | https://github.com/Handiboi/blender-vegetation-tools | **404** | – | – | No longer exists. | **SKIP** |
| – | `vegetation-team` (org) | https://github.com/vegetation-team | **404** | – | – | Org never existed or was deleted. | **SKIP** |
| – | `baumerjakob/leaf-plant` + `baumerjakob/plant-3d` | https://github.com/baumerjakob | **404 (user gone)** | – | – | Account deleted; no archive found. | **SKIP** |

### Web sources (not GitHub but central to the asset pipeline)

| # | Source | URL | License | Pack(s) relevant to Atlantic Forest | Verdict |
|---|--------|-----|---------|------------------------------------|---------|
| 16 | Quaternius | https://quaternius.com/ | **CC0** | Ultimate Nature (150), Ultimate Stylized Nature (63 textured), Ultimate Crops (102, 5 growth stages), Stylized Tree, Ultimate Modular Ruins (trees subset), Pirate Kit (trees+vegetation) | **ADOPT** |
| 17 | Kenney — Nature Kit | https://kenney.nl/assets/nature-kit | **CC0** | One 3D nature kit, low-poly. Small but solid filler. | **REFERENCE** |
| 18 | Poly Haven | https://polyhaven.com/models | **CC0** | ~500 hyperreal models (incl. trees, plants). Use `api.polyhaven.com` for scripted fetch. | **ADOPT** |

---

## 2. Top 3 sources for Atlantic Forest vegetation 3D

Ranked by **species match → license → render quality → scriptability**.

1. **Sketchfab CC-BY search** — already curated into `CREDITS.md` (6/7 species picked, UIDs documented). Best for **species-specific real-world models** (pindo palm, Guadua bamboo, Anthurium plowmanii) where Quaternius/Poly Haven are generic. Free, downloadable, attribution-only. Use the **Data API v3** for scripted batch download.
2. **Quaternius.com (CC0)** — best **filler / stylized** source. Ultimate Nature (150 models, FBX/OBJ/Blend), Ultimate Stylized Nature (63 with PBR textures + glTF), Ultimate Crops (102 across 5 growth stages — good for sapling→mature lapacho/mango). Zero attribution required.
3. **Poly Haven (CC0, ~500 models)** — best **photoreal hero assets**. Trees and plants are sparse but high-quality. Use the official `api.polyhaven.com` REST API (search by `category=nature&type=model`) to script the download. CC0, no attribution legally required (do it anyway for traceability).

**Why not others:** Poly Haven and Quaternius are CC0 (no attribution red tape); Kenney's "Nature Kit" is a single small pack, useful only as filler; Sketchfab CC-BY requires attribution and per-asset UIDs, which is what your `CREDITS.md` already manages.

---

## 3. The right Sketchfab downloader tool

**The `nicoptere/sketchfab_downloader` referenced in the original list is gone** (repo 404, not on PyPI). There is no maintained standalone Python Sketchfab scraper.

**Use the official Sketchfab Data API v3** (`https://api.sketchfab.com/v3/`). It's a plain REST/JSON API, no auth required for **read** (search + metadata), and you need a free personal access token only for **download** (a per-user OAuth token from https://sketchfab.com/settings/account → "Password & API").

| Operation | Endpoint | Auth | Notes |
|-----------|----------|------|-------|
| Search downloadable CC0/CC-BY models | `GET /v3/search?type=models&downloadable=true&license=cc0&archives_flavour=true&q=...` | none | Returns up to 24/page; iterate `?cursor=...` |
| Get model metadata (incl. license) | `GET /v3/models/{uid}` | none | Has `license.label` field — verify before download |
| Get download URL for a uid | `GET /v3/models/{uid}/download` | **Bearer token required** | Returns `gltf` / `usdz` URL pointing to signed S3 link; link expires |
| List user/library | `GET /v3/me/library` | Bearer | Useful for re-fetching your own downloads |

**Decision: build a small in-house Python client** (no third-party dep). It is ~80 lines, has no transitive deps, and respects rate limits + the 24-per-page cap. Use the existing `lqv/asset_loader.py` as the entry point.

**Why not `sketchfab` PyPI package / `sketchpy` / `sketchfab-api`:** all abandoned, last release 2019-2021, hit the now-deprecated v1 API. Don't reintroduce them.

---

## 4. CC0 / CC-BY plant models for the 7 species

This is the actual species → model table. The project already has the Sketchfab shortlist for 6/7; the gap is **lapacho**.

| Species | Source | UID / URL | License | Status | Notes |
|---------|--------|-----------|---------|--------|-------|
| Pindo palm (*Syagrus romanzoffiana*) | Sketchfab | `1fba8da266bc428ebfe8fe8a4f4df987` (drooping fronds) | CC-BY-4.0 | ✅ in `CREDITS.md` | CC-BY-4.0, attribution required |
| Mango (*Mangifera indica*, 5-pack) | Sketchfab | `6997814540f14929bf13cf3828b5dc90` (Jagobo) | CC-BY-4.0 | ✅ in `CREDITS.md` | dominant canopy backdrop |
| Tree fern (*Dicksonia / Cyathea*) | Sketchfab | `c6bc31d122c043a19346c90f5cbde40e` (b_nealie) | CC-BY-4.0 | ✅ in `CREDITS.md` | riparian shade understory |
| Bamboo (*Guadua angustifolia*) | Sketchfab | `3c13dc82ffb54d079a71fb8160d0cf90` (local.yany) | CC-BY-4.0 | ✅ in `CREDITS.md` | decimate 1.5M → ~50k tris |
| Agave americana | Sketchfab | `efe126efa459471c81cfc3132357b1b6` (LucaDubs) | CC-BY-4.0 | ✅ in `CREDITS.md` | decimate 1M → ~50k tris |
| Anthurium plowmanii | Sketchfab | `e6a92c1ddb8941e9b8aa92dc1f0f3c18` (Lassi Kaukonen) | CC-BY-4.0 | ✅ in `CREDITS.md` | species verification pending |
| **Lapacho (*Handroanthus impetiginosus*)** | **— GAP —** | needs search | CC-BY-4.0 target | ❌ not in `CREDITS.md` | see search recipe below |

### Lapacho search recipe (Data API v3)

```bash
# Search candidates — try these queries; sort by likes (most-liked first)
curl -sG 'https://api.sketchfab.com/v3/search' \
  --data-urlencode 'type=models' \
  --data-urlencode 'downloadable=true' \
  --data-urlencode 'archives_flavour=true' \
  --data-urlencode 'sort_by=-likeCount' \
  --data-urlencode 'q=tabebuia tree'   # botanical synonym — wider net

curl -sG 'https://api.sketchfab.com/v3/search' \
  --data-urlencode 'type=models' \
  --data-urlencode 'downloadable=true' \
  --data-urlencode 'archives_flavour=true' \
  --data-urlencode 'sort_by=-likeCount' \
  --data-urlencode 'q=lapacho'

curl -sG 'https://api.sketchfab.com/v3/search' \
  --data-urlencode 'type=models' \
  --data-urlencode 'downloadable=true' \
  --data-urlencode 'archives_flavour=true' \
  --data-urlencode 'sort_by=-likeCount' \
  --data-urlencode 'q=handroanthus'

curl -sG 'https://api.sketchfab.com/v3/search' \
  --data-urlencode 'type=models' \
  --data-urlencode 'downloadable=true' \
  --data-urlencode 'archives_flavour=true' \
  --data-urlencode 'sort_by=-likeCount' \
  --data-urlencode 'q=ipê rosa'        # Portuguese name — Brazilian community likely has it
```

Then **manually** pick the best match (verify: license.label contains "CC" or "Public Domain", face count ≤ 200k, and the model actually shows a pink/purple flowering canopy). Update `CREDITS.md` once chosen.

### CC0 fallbacks (Quaternius / Poly Haven)

If a Sketchfab CC-BY pick is too heavy or wrong species, use Quaternius **Ultimate Stylized Nature** (CC0, glTF, ~63 models incl. broadleaf trees + palm + fern) or **Ultimate Crops** (CC0, 102 models incl. tree saplings in 5 growth stages — useful for mature lapacho silhouette). These will read as "stylized" not photoreal; blend with post.

---

## 5. Recommended download script

Saves models into `assets/sketchfab/<uid>/`, writes a per-asset `LICENSE.txt` and `ATTRIBUTION.txt`, and updates `CREDITS.md`. Idempotent (skips already-downloaded). Token read from `~/.config/sketchfab/token` or env `SKETCHFAB_TOKEN`.

```python
#!/usr/bin/env python3
"""
fetch_vegetation.py — batch-download CC-BY 3D models from Sketchfab Data API v3.

Targets the 6 species already in CREDITS.md + the lapacho gap (once chosen).

Usage:
    export SKETCHFAB_TOKEN="<paste from https://sketchfab.com/settings/account>"
    python3 scripts/fetch_vegetation.py            # download all
    python3 scripts/fetch_vegetation.py --only lapacho
    python3 scripts/fetch_vegetation.py --dry-run
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlencode

import urllib.request
import urllib.error

API = "https://api.sketchfab.com/v3"

# 6 known-good UIDs from CREDITS.md; add the lapacho UID here once picked.
SHORTLIST: dict[str, dict] = {
    "pindo_palm": {
        "uid": "1fba8da266bc428ebfe8fe8a4f4df987",
        "author": "drooping-fronds artist (verify on download)",
        "species": "Syagrus romanzoffiana",
    },
    "mango_5pack": {
        "uid": "6997814540f14929bf13cf3828b5dc90",
        "author": "Jagobo",
        "species": "Mangifera indica",
    },
    "tree_fern": {
        "uid": "c6bc31d122c043a19346c90f5cbde40e",
        "author": "b_nealie",
        "species": "Dicksonia / Cyathea",
    },
    "bamboo_guadua": {
        "uid": "3c13dc82ffb54d079a71fb8160d0cf90",
        "author": "local.yany",
        "species": "Guadua angustifolia",
    },
    "agave_americana": {
        "uid": "efe126efa459471c81cfc3132357b1b6",
        "author": "LucaDubs",
        "species": "Agave americana",
    },
    "anthurium_plowmanii": {
        "uid": "e6a92c1ddb8941e9b8aa92dc1f0f3c18",
        "author": "Lassi Kaukonen",
        "species": "Anthurium plowmanii",
    },
    # ── lapacho gap: uncomment once UID is picked ──
    # "lapacho": {
    #     "uid": "<TODO>",
    #     "author": "<TODO>",
    #     "species": "Handroanthus impetiginosus",
    # },
}


def http_json(url: str, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def get_metadata(uid: str) -> dict:
    return http_json(f"{API}/models/{uid}")


def get_download_url(uid: str, token: str) -> str:
    """Authenticated — returns the signed S3 URL for the GLB archive."""
    data = http_json(
        f"{API}/models/{uid}/download",
        headers={"Authorization": f"Token {token}"},
    )
    # Prefer gltf; fall back to first available format
    for fmt in ("gltf", "usdz", "source"):
        if fmt in data:
            return data[fmt]["url"]
    raise RuntimeError(f"No download format for {uid}: {data}")


def download_to(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"  already have {dest}")
        return
    with urllib.request.urlopen(url, timeout=120) as r, open(dest, "wb") as f:
        while chunk := r.read(64 * 1024):
            f.write(chunk)
    print(f"  → {dest}  ({dest.stat().st_size // 1024} KB)")


def write_attribution(uid: str, meta: dict, dest_dir: Path) -> None:
    lic = (meta.get("license") or {}).get("label", "Unknown")
    user = meta.get("user", {}).get("username", "unknown")
    display = meta.get("user", {}).get("displayName", user)
    title = meta.get("name", uid)
    url = f"https://sketchfab.com/3d-models/{uid}"
    cc_url = (meta.get("license") or {}).get("url", "")

    (dest_dir / "ATTRIBUTION.txt").write_text(
        f"Title: {title}\n"
        f"Author: {display} (@{user})\n"
        f"UID: {uid}\n"
        f"Source: {url}\n"
        f"License: {lic}\n"
        f"License URL: {cc_url}\n"
        f"Fetched: {time.strftime('%Y-%m-%d')}\n"
    )
    (dest_dir / "LICENSE.txt").write_text(
        f"This asset is licensed under {lic}.\n"
        f"Full text: {cc_url}\n"
        f"\nSee ATTRIBUTION.txt for author + source URL.\n"
    )
    print(f"  wrote ATTRIBUTION.txt + LICENSE.txt ({lic})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated keys to fetch (default: all)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--root", default="assets/sketchfab", help="output root (default: assets/sketchfab)"
    )
    args = ap.parse_args()

    token = os.environ.get("SKETCHFAB_TOKEN", "").strip()
    if not token:
        token_path = Path.home() / ".config/sketchfab/token"
        if token_path.exists():
            token = token_path.read_text().strip()
    if not token:
        print("error: set SKETCHFAB_TOKEN env or write to ~/.config/sketchfab/token",
              file=sys.stderr)
        return 2

    keys = (
        [k.strip() for k in args.only.split(",") if k.strip()]
        if args.only
        else list(SHORTLIST)
    )
    missing = [k for k in keys if k not in SHORTLIST]
    if missing:
        print(f"error: unknown keys: {missing}", file=sys.stderr)
        return 2

    root = Path(args.root)
    rc = 0
    for key in keys:
        info = SHORTLIST[key]
        uid = info["uid"]
        print(f"[{key}] uid={uid} species={info['species']}")
        dest_dir = root / uid

        if args.dry_run:
            print(f"  would fetch to {dest_dir}")
            continue

        try:
            meta = get_metadata(uid)
            write_attribution(uid, meta, dest_dir)
            signed = get_download_url(uid, token)
            ext = "glb" if signed.endswith(".glb") or "gltf" in signed else "zip"
            download_to(signed, dest_dir / f"source.{ext}")
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code} {e.reason} — skipping", file=sys.stderr)
            rc = 1
        except Exception as e:
            print(f"  {type(e).__name__}: {e} — skipping", file=sys.stderr)
            rc = 1
        time.sleep(1)  # be polite to the API

    return rc


if __name__ == "__main__":
    sys.exit(main())
```

### Install / run

```bash
mkdir -p ~/.config/sketchfab
echo "<paste token from https://sketchfab.com/settings/account>" > ~/.config/sketchfab/token
chmod 600 ~/.config/sketchfab/token

# dry run first
python3 scripts/fetch_vegetation.py --dry-run

# then for real
python3 scripts/fetch_vegetation.py

# fetch just one if a UID was changed
python3 scripts/fetch_vegetation.py --only anthurium_plowmanii
```

### After download

For each new asset in `assets/sketchfab/<uid>/`:

1. Drop the GLB into `assets/models/<species>/<uid>.glb` (keep the per-uid folder in `assets/sketchfab/` as the immutable archive + attribution).
2. Decimate if needed (bamboo: 1.5M→50k, agave: 1M→50k) — use Blender's Decimate modifier via `bpy.ops`.
3. Move the entry from `## Sketchfab — CC-BY 4.0` → `## Sketchfab — CC-BY 4.0` + append `[USED]` tag in `CREDITS.md`.
4. Verify the `lqv/flora/<species>.py` script references the local path (e.g. `assets/models/pindo/<uid>.glb`).

### Attribution template (drop into `CREDITS.md` per asset)

```markdown
- **[USED] Lapacho (*Handroanthus impetiginosus*)** — <author displayName> (@<username>) — Sketchfab UID `<uid>` — CC-BY-4.0 — deciduous canopy, pink/purple Tabebuia flowering in spring
```

---

## 6. Recommended follow-ups (in order of impact)

1. **Pick a lapacho UID** by running the 4 curl recipes above, then add it to `SHORTLIST["lapacho"]` in `scripts/fetch_vegetation.py` and re-run.
2. **Commit `scripts/fetch_vegetation.py`** to the repo and add a `make fetch-vegetation` target.
3. **Mirror Quaternius Ultimate Stylized Nature** (CC0, glTF) into `assets/quaternius/stylized-nature/` as a backup for any species that the Sketchfab model is too heavy / wrong LOD for.
4. **Wire `polyhavenassets` addon** as a fallback path for the few photoreal trees Poly Haven has (search `?category=nature&type=model` via their public API at `https://api.polyhaven.com/assets?category=nature&type=model`).
5. **Defer Mtree / tree-gen** — these are reference for the procedural side; the current `lqv/flora/*.py` scripts already produce 7 species procedurally, so Mtree/tree-gen are only worth pulling in if we need 3 more species or want wind animation.
6. **Defer FractalForge + Easy-Tree** — only useful if we add grass/groundcover scattering in `lqv/flora/gn_scatter.py`; the LOD + foliage auto-normals tools would improve that subsystem.

---

## 7. TL;DR

- **7 of 10** repos in the original list are 404 — dead links. The replacements (Mtree, tree-gen, Sorcar, polyhavenassets, Public-API) are the actual gold.
- **The Sketchfab downloader question is the real ask.** The Python `sketchfab_downloader` is gone. Build a ~80-line client on the Data API v3 (script provided, ready to drop into `scripts/fetch_vegetation.py`).
- **6/7 species already have Sketchfab UIDs** in `CREDITS.md`. Only **lapacho** is a gap — search via the 4 API queries in §4, pick, paste UID.
- **Top 3 sources**: Sketchfab CC-BY (your existing shortlist), Quaternius CC0 (filler + stylized), Poly Haven CC0 (hero photoreal, via their Public API).
- **No new dependency, no paid tool, no exotic package.** The whole pipeline is stdlib + Sketchfab token + your existing `lqv/asset_loader.py`.
