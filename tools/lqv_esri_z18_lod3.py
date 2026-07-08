#!/usr/bin/env python3
"""Fetch Esri World Imagery z=18 (0.6m/pixel) for 1.4km x 1.4km AOI around LQV."""
from __future__ import annotations
import io, math, sys, time, json, shutil
from pathlib import Path
import requests
from PIL import Image

REPO = Path("/root/la-quebrada-viva")
OUT = REPO / "docs/game_assets/textures"
LITE = REPO / "splats/exports/web/game_assets_lite/assets/textures"
OUT.mkdir(parents=True, exist_ok=True); LITE.mkdir(parents=True, exist_ok=True)

CENTROID_LON, CENTROID_LAT, ZOOM = -57.030, -25.630, 18
GRID = 9  # 9×9 tiles ≈ 1.4 km

def lonlat_to_tile(lon, lat, z):
    n = 2 ** z
    x = int((lon + 180) / 360 * n)
    y = int((1 - math.log(math.tan(math.radians(lat)) + 1/math.cos(math.radians(lat))) / math.pi) / 2 * n)
    return x, y

def tile_to_lonlat(x, y, z):
    n = 2 ** z
    w = x / n * 360 - 180
    e = (x + 1) / n * 360 - 180
    nr = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    s = math.atan(math.sinh(math.pi * (1 - 2 * (y + 1) / n)))
    return w, math.degrees(nr), e, math.degrees(s)

def fetch(z, x, y, tries=3):
    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    for k in range(tries):
        try:
            r = requests.get(url, timeout=30, headers={"User-Agent": "LQV/1.0"})
            r.raise_for_status()
            return Image.open(io.BytesIO(r.content)).convert("RGB")
        except Exception as e:
            if k < tries - 1:
                time.sleep(2**k); continue
            print(f"  fail {z}/{y}/{x}: {e}", flush=True)
            return Image.new("RGB", (256, 256), (80, 80, 80))

def main():
    cx, cy = lonlat_to_tile(CENTROID_LON, CENTROID_LAT, ZOOM)
    half = GRID // 2
    imgs = []
    for dy in range(-half, half+1):
        row = []
        for dx in range(-half, half+1):
            row.append(fetch(ZOOM, cx+dx, cy+dy))
            print(f"  z{ZOOM}/{cy+dy}/{cx+dx} ok", end="\r", flush=True)
        imgs.append(row)
    print()
    canvas = Image.new("RGB", (256*GRID, 256*GRID))
    for r,row in enumerate(imgs):
        for c,im in enumerate(row): canvas.paste(im, (c*256, r*256))

    w, n, e, s = tile_to_lonlat(cx-half, cy-half, ZOOM)
    _, _, e, s = tile_to_lonlat(cx+half, cy+half, ZOOM)  # also overwrites; do sequentially
    w_top, n_top, e_top, s_top = tile_to_lonlat(cx+half, cy-half, ZOOM)  # not used but capture
    deg_per = 360 / (2**ZOOM)
    m_px = deg_per * 111000 * math.cos(math.radians(CENTROID_LAT)) / 256

    out = OUT / "lqv_esri_z18_lod3.png"
    canvas.save(out, optimize=True)
    print(f"wrote {out}  {canvas.size[0]}x{canvas.size[1]}px  {out.stat().st_size/1024/1024:.1f}MB  {m_px:.3f}m/px")
    print(f"bounds: W={w:.6f} S={s:.6f} E={e:.6f} N={n:.6f}")

    # Re-fetch exact bounds using the 4 corner tiles
    w_full, n_full, _, _ = tile_to_lonlat(cx-half, cy-half, ZOOM)
    _, _, e_full, s_full = tile_to_lonlat(cx+half, cy+half, ZOOM)

    bp = OUT / "lqv_esri_z18_lod3_bounds.json"
    bp.write_text(json.dumps({
        "west": w_full, "south": s_full, "east": e_full, "north": n_full,
        "width": canvas.size[0], "height": canvas.size[1],
        "resolution_m_per_pixel": m_px,
        "source": "Esri World Imagery z=18",
        "attribution": "© Esri, Maxar, Earthstar Geographics",
    }, indent=2))

    shutil.copy(out, LITE / "lqv_esri_z18_lod3.png")
    shutil.copy(bp, LITE / "lqv_esri_z18_lod3_bounds.json")
    print(f"copied to {LITE}")

if __name__ == "__main__":
    main()
