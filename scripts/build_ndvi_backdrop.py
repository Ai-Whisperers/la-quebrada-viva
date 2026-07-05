"""Build a continuous NDVI grayscale raster (800x800 PNG) by
rasterising the existing MapBiomas 2023 polygons.

The Sentinel-2 NDVI polygons (ndvi_canopy_10km.geojson) only
include ~743 polygons at class boundaries — the contiguous
forest inside the parcel doesn't show as a polygon because
it's a single mass with no edge. This produces a continuous
backdrop raster so the parcel itself shows as "dense forest"
at any zoom level.

NDVI values per MapBiomas class (calibrated to local Sentinel-2
L2A NDVI percentiles observed in the 10 km box):
  3 (Forest Formation)   → 0.75
  6 (Flooded Forest)     → 0.75
  9 (Forest Plantation)  → 0.65
 11 (Wetland)            → 0.55
 12 (Grassland)          → 0.45
 15 (Pasture)            → 0.40
 18 (Agriculture)        → 0.35
 22 (Non-vegetated)      → 0.15
 26 (Water)              → 0.05
 default (no class)      → 0.20
"""
import json
import numpy as np
from PIL import Image
from pathlib import Path
from shapely.geometry import shape, Point

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"

LON_W, LAT_S, LON_E, LAT_N = -57.130, -25.698, -56.931, -25.518
W, H = 800, 800

NDVI_BY_CLASS = {
    3: 0.75, 6: 0.75, 9: 0.65, 11: 0.55,
    12: 0.45, 15: 0.40, 18: 0.35, 22: 0.15,
    26: 0.05,
}


def lonlat_to_px(lon, lat):
    x = int((lon - LON_W) / (LON_E - LON_W) * W)
    y = int((LAT_N - lat) / (LAT_N - LAT_S) * H)
    return max(0, min(W-1, x)), max(0, min(H-1, y))


def main():
    print("Loading MapBiomas polygons...")
    mb = json.load(open(OUT / "mapbiomas_2023_10km.geojson"))
    arr = np.full((H, W), 20, dtype=np.uint8)

    print(f"Rasterising {len(mb['features'])} polygons at {W}x{H}...")
    for feat in mb['features']:
        cls = feat['properties']['class_code']
        val = int(NDVI_BY_CLASS.get(cls, 20) * 100)
        g = shape(feat['geometry'])
        polys = ([g] if g.geom_type == 'Polygon'
                 else list(g.geoms) if g.geom_type == 'MultiPolygon'
                 else [])
        for poly in polys:
            minx, miny, maxx, maxy = poly.bounds
            px0, py1 = lonlat_to_px(minx, maxy)
            px1, py0 = lonlat_to_px(maxx, miny)
            if px1 < px0 or py0 < py1:
                continue
            for y in range(py0, py1 + 1):
                for x in range(px0, px1 + 1):
                    lon = LON_W + (x / W) * (LON_E - LON_W)
                    lat = LAT_N - (y / H) * (LAT_N - LAT_S)
                    if poly.contains(Point(lon, lat)):
                        arr[y, x] = val

    img = Image.fromarray(arr, mode='L')
    out_png = OUT / "ndvi_canopy_10km.png"
    img.save(out_png, optimize=True)
    print(f"wrote {out_png} ({img.size}, mode=L, "
          f"{out_png.stat().st_size/1024:.1f} KB)")

    bounds = [[LAT_S, LON_W], [LAT_N, LON_E]]
    bounds_path = OUT / "ndvi_canopy_bounds.json"
    bounds_path.write_text(json.dumps(bounds))
    print(f"wrote {bounds_path}")


if __name__ == "__main__":
    main()