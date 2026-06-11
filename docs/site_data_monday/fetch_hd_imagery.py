"""Fetch the best-resolution satellite/aerial imagery available for free.
Sources:
  - Esri World Imagery (max ~0.3m in cities, ~0.5-1m rural) — via ArcGIS REST tile service
  - Sentinel-2 10m (already in)
  - Mapbox (needs key)
  - Bing (needs key)

We'll use the ArcGIS REST tile service to get the tightest imagery they have.
The ArcGIS service exposes tiles via /MapServer/tile/{z}/{y}/{x}.
"""
import os, math, requests, time
from PIL import Image
from io import BytesIO
from AOI import BBOX

os.makedirs("hd_imagery", exist_ok=True)
W, S, E, N = BBOX
LAT_C, LON_C = -25.561944, -54.631389

def deg2tile(lat, lon, z):
    n = 2.0 ** z
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n)
    return xtile, ytile

def tile2lonlat(x, y, z):
    n = 2.0 ** z
    lon = x / n * 360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lon, lat

# Use z=17 (best detail). At equator each z17 tile is ~600m wide, so AOI 6km = 10x10 = 100 tiles
# Use z=16 (~1.2km/tile, 5x5 = 25 tiles) for a faster test, then z=17
def fetch_z(z, source="esri"):
    cx, cy = deg2tile(LAT_C, LON_C, z)
    # get 2x2 grid centered on cascade
    print(f"\n=== z={z}  tile center {cx},{cy}  source={source} ===")
    sources = {
        "esri": f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{{y}}/{{x}}",
        "esri_labels": f"https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{{y}}/{{x}}",
    }
    base = sources[source]
    out_dir = f"hd_imagery/{source}_z{z}"
    os.makedirs(out_dir, exist_ok=True)
    tiles = []
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            x, y = cx + dx, cy + dy
            url = base.format(x=x, y=y)
            out = f"{out_dir}/{z}_{x}_{y}.jpg"
            if not os.path.exists(out):
                try:
                    r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
                    if r.status_code == 200 and r.content[:2] == b"\xff\xd8":
                        with open(out, "wb") as f:
                            f.write(r.content)
                    else:
                        print(f"  skip {x},{y} HTTP {r.status_code}")
                except Exception as e:
                    print(f"  fail {x},{y} {e}")
            if os.path.exists(out):
                tiles.append((x, y, out))
    print(f"  fetched {len(tiles)} tiles")
    if not tiles:
        return None
    # stitch
    xs = sorted({t[0] for t in tiles})
    ys = sorted({t[1] for t in tiles})
    tile_w, tile_h = 256, 256
    canvas = Image.new("RGB", (len(xs) * tile_w, len(ys) * tile_h), (0, 0, 0))
    for x, y, path in tiles:
        try:
            img = Image.open(path).convert("RGB")
            if img.size != (tile_w, tile_h):
                img = img.resize((tile_w, tile_h))
            ix = xs.index(x); iy = ys.index(y)
            canvas.paste(img, (ix * tile_w, iy * tile_h))
        except Exception as e:
            print(f"  stitch fail {path}: {e}")
    out_png = f"hd_imagery/{source}_z{z}_stitched.png"
    canvas.save(out_png, optimize=True)
    print(f"  -> {out_png} {os.path.getsize(out_png)//1024} KB  size {canvas.size}")
    # save bounding box
    meta = f"hd_imagery/{source}_z{z}_meta.txt"
    with open(meta, "w") as f:
        l_w, l_n = tile2lonlat(min(xs), min(ys), z)
        l_e, l_s = tile2lonlat(max(xs)+1, max(ys)+1, z)
        f.write(f"stitched {len(xs)}x{len(ys)} tiles at z={z}\n")
        f.write(f"center tile: {cx},{cy}\n")
        f.write(f"bounds WGS84: W={l_w:.6f} S={l_s:.6f} E={l_e:.6f} N={l_n:.6f}\n")
        f.write(f"canvas size: {canvas.size} px\n")
        f.write(f"approx ground res: {((l_e - l_w) * 111000) / canvas.size[0]:.2f} m/pixel at lat {LAT_C}\n")
    print(open(meta).read())
    return out_png

# z=16: ~1.2 m/pixel (Alto Paraná, agricultural, so Esri World Imagery probably 0.5-1m)
fetch_z(16, "esri")
# z=17: ~0.6 m/pixel — bigger but worth it for the cascade
fetch_z(17, "esri")
