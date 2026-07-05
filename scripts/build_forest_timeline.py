"""Compute MapBiomas forest-change timeline for the LQV 10 km box.

For each year (1985, 2000, 2005, 2010, 2015, 2020, 2023):
  - Load MapBiomas raster clipped to 10 km
  - Polygonise Forest Formation (class 3) + Flooded Forest (class 6)
  - Compute area_ha and number of polygons

Output: splats/exports/web/data/mapbiomas_forest_timeline.json
  {
    "years": [1985, 2000, ..., 2023],
    "forest_area_ha": [...],
    "polygon_counts": [...],
    "parcel_inside_ha": [...],
    "parcel_inside_class": [...]
  }
"""
import json
import math
from pathlib import Path
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from rasterio.features import shapes as rio_shapes
from shapely.geometry import shape, mapping
from shapely.validation import make_valid
from pyproj import Geod

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"

BBOX_WSEN = (-57.130, -25.698, -56.931, -25.518)

YEARS = [1985, 2000, 2005, 2010, 2015, 2020, 2023]
FOREST_CLASSES = [3, 6]  # Forest Formation + Flooded Forest

geod = Geod(ellps="WGS84")


def log(m):
    print(f"[mb_timeline] {m}", file=__import__('sys').stderr, flush=True)


def load_year(year):
    src = ROOT / f"docs/site_data/mapbiomas_paraguay/{year}/mapbiomas_{year}_aoi_50km.tif"
    with rasterio.open(src) as ds:
        win = from_bounds(*BBOX_WSEN, ds.transform)
        r0 = max(0, int(win.row_off)); c0 = max(0, int(win.col_off))
        r1 = min(ds.height, int(win.row_off + win.height))
        c1 = min(ds.width, int(win.col_off + win.width))
        if r1 <= r0 or c1 <= c0:
            return None, None
        arr = ds.read(1, window=((r0, r1), (c0, c1)))
        tf = rasterio.windows.transform(((r0, r1), (c0, c1)), ds.transform)
        return arr, tf


def parcel_area_inside(polygons, parcel_geom):
    """Compute total area of polygons intersecting parcel."""
    if not parcel_geom or not polygons:
        return 0
    total = 0
    for g in polygons:
        try:
            inter = parcel_geom.intersection(g)
            if not inter.is_empty:
                m2, _ = geod.geometry_area_perimeter(inter)
                total += abs(m2) / 10000
        except Exception:
            continue
    return total


def main():
    # Load LQV parcel
    parcel_path = OUT / "client_gps/client_gps_polygon.geojson"
    if not parcel_path.exists():
        log("no parcel polygon")
        return
    parcel_fc = json.load(open(parcel_path))
    parcel_geom = shape(parcel_fc['features'][0]['geometry'])
    parcel_area_ha, _ = geod.geometry_area_perimeter(parcel_geom)
    parcel_area_ha = abs(parcel_area_ha) / 10000
    log(f"parcel area: {parcel_area_ha:.2f} ha")

    timeline = {
        "years": YEARS,
        "forest_area_ha": [],
        "polygon_counts": [],
        "parcel_inside_ha": [],
        "parcel_total_ha": parcel_area_ha,
        "bbox_w_s_e_n": list(BBOX_WSEN),
        "notes": "Forest = MapBiomas classes 3 (Forest Formation) + 6 (Flooded Forest)",
    }

    for year in YEARS:
        log(f"year {year}...")
        arr, tf = load_year(year)
        if arr is None:
            log(f"  no data")
            timeline["forest_area_ha"].append(0)
            timeline["polygon_counts"].append(0)
            timeline["parcel_inside_ha"].append(0)
            continue
        mask = np.isin(arr, FOREST_CLASSES)
        n_px = int(mask.sum())
        # Polygonise
        polys = []
        for geom, val in rio_shapes(arr.astype(np.int32), mask=mask,
                                    connectivity=8, transform=tf):
            try:
                g = shape(geom)
                if not g.is_valid:
                    g = make_valid(g)
                if g.is_empty or g.area < 1e-8:
                    continue
                polys.append(g)
            except Exception:
                continue
        # Total forest area
        total_m2 = 0
        for g in polys:
            try:
                m2, _ = geod.geometry_area_perimeter(g)
                total_m2 += abs(m2)
            except Exception:
                continue
        total_ha = total_m2 / 10000
        # Forest inside parcel
        parcel_inside_ha = parcel_area_inside(polys, parcel_geom)
        timeline["forest_area_ha"].append(round(total_ha, 2))
        timeline["polygon_counts"].append(len(polys))
        timeline["parcel_inside_ha"].append(round(parcel_inside_ha, 2))
        log(f"  {n_px} px, {len(polys)} polygons, {total_ha:.0f} ha total, "
            f"{parcel_inside_ha:.1f} ha inside parcel")

    # Compute change
    if len(timeline["forest_area_ha"]) >= 2:
        first = timeline["forest_area_ha"][0]
        last = timeline["forest_area_ha"][-1]
        delta = last - first
        pct = (delta / first * 100) if first else 0
        timeline["change_ha"] = round(delta, 2)
        timeline["change_pct"] = round(pct, 1)
        log(f"1985 → 2023 forest change: {delta:+.0f} ha ({pct:+.1f}%)")

    out_path = OUT / "mapbiomas_forest_timeline.json"
    out_path.write_text(json.dumps(timeline, indent=2))
    log(f"wrote {out_path}")


if __name__ == "__main__":
    main()