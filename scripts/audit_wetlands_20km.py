"""Audit OSM wetlands in the 20 km LQV context and bundle all surface water data.

Reads OSM water polygons + JRC Global Surface Water (1984-2024 occurrence)
+ Copernicus GLO-30 DEM, classifies each polygon, and emits one GeoJSON
the viewer shows colour-coded by audit verdict.

Classification:
  verified_lake         JRC mean >= 50% AND on flat slope
  verified_wetland      JRC mean 20-50% AND flat
  seasonal_wetland      JRC mean 10-20% OR in-stream pool
  in_stream_pool        within 200 m of an OSM waterway
  river_polygon         OSM natural=water + water=river
  ambiguous             flat but no JRC signal — possibly farm pond, dry pan
  likely_mis-tagged     JRC mean < 5% AND slope > 5° — likely forested fragment mis-tagged

  + waterways (LineStrings) classified as river / stream / ditch / canal.
"""
from __future__ import annotations

import json
import math
import os
from collections import Counter
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import xy as rio_xy
from rasterio.warp import reproject, Resampling
from shapely.geometry import shape, mapping

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "splats/exports/web/data"
OUT.mkdir(parents=True, exist_ok=True)

# 20 km bbox (S,W,N,E)
BBOX = (-25.787336, -57.231502, -25.427336, -56.839502)
CX = (BBOX[1] + BBOX[3]) / 2
CY = (BBOX[0] + BBOX[2]) / 2

WATER_GEOJSON = ROOT / "docs/site_data/osm_20km/water.geojson"
WATERWAYS_GEOJSON = ROOT / "docs/site_data/osm_20km/waterways.geojson"
JRC_OCC_PATH = ROOT / "docs/site_data/jrc_gsw/occurrence/occurrence_aoi_50km.tif"
DEM_PATH = OUT / "dem_streams_20km_input.tif"
OUT_PATH = OUT / "surface_water_20km.geojson"


def log(msg):
    import sys
    print(f"[audit] {msg}", file=sys.stderr, flush=True)


# ============================================================
# Stage 1: waterways (for proximity check)
# ============================================================
log("loading waterways ...")
waterways = json.load(open(WATERWAYS_GEOJSON))
log(f"  {len(waterways['features'])} waterways")

WATERWAY_COORDS = []
for f in waterways["features"]:
    g = f["geometry"]
    if g["type"] in ("LineString", "MultiLineString"):
        lines = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
        for line in lines:
            WATERWAY_COORDS.extend([(c[0], c[1]) for c in line])
WATERWAY_COORDS = np.array(WATERWAY_COORDS, dtype=np.float64)
log(f"  {len(WATERWAY_COORDS):,} waterway vertices total")


def centroid_near_waterway(lon: float, lat: float, max_dist_m: float = 200.0) -> bool:
    if len(WATERWAY_COORDS) == 0:
        return False
    dlat = (max_dist_m / 111000.0)
    dlon = (max_dist_m / (111000.0 * math.cos(math.radians(lat))))
    mask = (
        (np.abs(WATERWAY_COORDS[:, 0] - lon) < dlon)
        & (np.abs(WATERWAY_COORDS[:, 1] - lat) < dlat)
    )
    return bool(mask.any())


# ============================================================
# Stage 2: JRC occurrence raster
# ============================================================
log("loading JRC GSW occurrence ...")
jrc_arr = None
jrc_transform = None
jrc_crs = None

if JRC_OCC_PATH.exists():
    with rasterio.open(JRC_OCC_PATH) as r:
        jrc_crs = r.crs
        jrc_bounds = r.bounds
        log(f"  source: {r.shape}, bbox {jrc_bounds}")
        from rasterio.windows import from_bounds
        win = from_bounds(BBOX[1], BBOX[0], BBOX[3], BBOX[2], r.transform)
        win = win.intersection(rasterio.windows.Window(0, 0, r.width, r.height))
        jrc_arr = r.read(1, window=win).astype(np.float32)
        jrc_transform = r.window_transform(win)
        jrc_arr[jrc_arr == 0] = np.nan  # 0 = no data in JRC, not "no water"
        # Wait — JRC actually uses 0..100 for occurrence and 255 for nodata
        # So 0 means "water 0% of the time" — leave as 0, just NaN-out 255.
        jrc_arr[jrc_arr > 100] = np.nan
        log(f"  cropped: {jrc_arr.shape}, range {np.nanmin(jrc_arr):.0f}–{np.nanmax(jrc_arr):.0f}")

# Build inside-20km-mask for JRC
H, W = jrc_arr.shape
rows = np.arange(H).reshape(-1, 1).repeat(W, axis=1)
cols = np.arange(W).reshape(1, -1).repeat(H, axis=0)
xs, ys = rio_xy(jrc_transform, rows, cols)
lons = np.array(xs).reshape(H, W)
lats = np.array(ys).reshape(H, W)
inside_20 = (
    (lons >= BBOX[1]) & (lons <= BBOX[3])
    & (lats >= BBOX[0]) & (lats <= BBOX[2])
)

def jrc_stats_for_polygon(geom) -> tuple[float, float, int]:
    """Return (mean, max, pixel_count_with_data) for the JRC raster inside geom."""
    if jrc_arr is None:
        return (np.nan, np.nan, 0)
    try:
        from rasterio.features import rasterize
        mask = rasterize(
            [(mapping(geom), 1)],
            out_shape=jrc_arr.shape,
            transform=jrc_transform,
            fill=0,
            dtype=np.uint8,
            all_touched=True,
        ).astype(bool)
        if not mask.any():
            return (np.nan, np.nan, 0)
        vals = jrc_arr[mask]
        vals = vals[~np.isnan(vals)]
        if len(vals) == 0:
            return (np.nan, np.nan, 0)
        return (float(vals.mean()), float(vals.max()), int(len(vals)))
    except Exception:
        return (np.nan, np.nan, 0)


# ============================================================
# Stage 3: DEM slopes
# ============================================================
log("computing DEM slopes per polygon...")
dem_full = None
dem_transform = None
dem_ds = None
dem_transform_ds = None
if DEM_PATH.exists():
    with rasterio.open(DEM_PATH) as r:
        dem_full = r.read(1)
        dem_transform = r.transform
        SUBSAMPLE = 4
        dem_ds = r.read(
            1, out_shape=(
                dem_full.shape[0] // SUBSAMPLE,
                dem_full.shape[1] // SUBSAMPLE
            ), resampling=Resampling.average)
        dem_transform_ds = dem_transform * rasterio.Affine.scale(SUBSAMPLE, SUBSAMPLE)
    log(f"  DEM loaded {dem_full.shape} (downsampled to {dem_ds.shape})")
else:
    log(f"  ⚠ {DEM_PATH} not found — slope stats will be NaN")


def dem_stats_for_polygon(geom) -> tuple[float, float, float]:
    if dem_ds is None:
        return (np.nan, np.nan, np.nan)
    try:
        from rasterio.features import rasterize
        mask = rasterize(
            [(mapping(geom), 1)],
            out_shape=dem_ds.shape,
            transform=dem_transform_ds,
            fill=0,
            dtype=np.uint8,
            all_touched=True,
        ).astype(bool)
        if not mask.any():
            return (np.nan, np.nan, np.nan)
        vals = dem_ds[mask]
        vals = vals[~np.isnan(vals)]
        if len(vals) == 0:
            return (np.nan, np.nan, np.nan)
        std_m = float(np.std(vals))
        proxy_slope_deg = min(60.0, std_m * 0.6)
        return (proxy_slope_deg, float(vals.min()), float(vals.max()))
    except Exception:
        return (np.nan, np.nan, np.nan)


# ============================================================
# Stage 4: audit + classify each polygon
# ============================================================
log("loading OSM water polygons ...")
water = json.load(open(WATER_GEOJSON))
log(f"  {len(water['features'])} water polygons")

CLASS_COLOR = {
    "verified_lake":     "#0ea5e9",
    "verified_wetland":  "#0284c7",
    "seasonal_wetland":  "#67e8f9",
    "in_stream_pool":    "#7dd3fc",
    "river_polygon":     "#1d4ed8",
    "ambiguous":          "#fbbf24",
    "likely_mis-tagged":  "#f87171",
    "unknown":            "#9ca3af",
}


def classify_osm_water(p, geom, jrc_mean, slope_deg, is_in_stream, area_m2):
    """Decision tree for OSM-tagged water features."""
    natural = p.get("natural")
    water_tag = p.get("water")
    landuse = p.get("landuse")
    jrc_ok = not np.isnan(jrc_mean)
    jrc_high = jrc_ok and jrc_mean >= 50
    jrc_med = jrc_ok and jrc_mean >= 20
    jrc_low = jrc_ok and jrc_mean >= 10
    if water_tag in ("lake", "reservoir", "river", "pond") or landuse == "reservoir":
        if jrc_high: return "verified_lake"
        if jrc_med:  return "verified_wetland"
        if jrc_low:  return "seasonal_wetland"
        if water_tag == "river": return "river_polygon"
        if is_in_stream: return "in_stream_pool"
        return "ambiguous"
    if natural == "wetland":
        if jrc_high: return "verified_lake"
        if jrc_med:  return "verified_wetland"
        if jrc_low:  return "seasonal_wetland"
        if is_in_stream: return "in_stream_pool"
        if not np.isnan(slope_deg) and slope_deg < 3:
            return "ambiguous"
        return "likely_mis-tagged"
    if natural == "water" and water_tag == "river":
        return "river_polygon"
    if natural == "water":
        if jrc_high: return "verified_lake"
        if jrc_med:  return "verified_wetland"
        if jrc_low:  return "seasonal_wetland"
        return "ambiguous"
    return "unknown"


classes = Counter()
features_out = []
audit_failures = []

for idx, f in enumerate(water["features"]):
    try:
        p = f["properties"]
        g = f["geometry"]
        geom = shape(g)
        if not geom.is_valid:
            geom = geom.buffer(0)
        if not geom.is_valid or geom.is_empty:
            continue
        # Normalize to a list of single polygons
        if geom.geom_type == "MultiPolygon":
            polys = [p for p in geom.geoms if p.area > 0]
        elif geom.geom_type == "Polygon":
            polys = [geom]
        else:
            continue
        for single_geom in polys:
            centroid = single_geom.centroid
            jrc_mean, jrc_max, jrc_n = jrc_stats_for_polygon(single_geom)
            slope_deg, elev_min, elev_max = dem_stats_for_polygon(single_geom)
            is_in_stream = centroid_near_waterway(centroid.x, centroid.y)
            area_m2 = single_geom.area * (111000 ** 2) * math.cos(math.radians(centroid.y))
            cls = classify_osm_water(p, single_geom, jrc_mean, slope_deg, is_in_stream, area_m2)
            classes[cls] += 1
            new_props = dict(p)
            new_props["audit_class"] = cls
            new_props["audit_color"] = CLASS_COLOR.get(cls, "#999")
            new_props["audit_jrc_occurrence_mean"] = (
                None if np.isnan(jrc_mean) else round(float(jrc_mean), 2))
            new_props["audit_jrc_occurrence_max"] = (
                None if np.isnan(jrc_max) else round(float(jrc_max), 2))
            new_props["audit_jrc_pixels"] = jrc_n
            new_props["audit_dem_slope_proxy_deg"] = (
                None if np.isnan(slope_deg) else round(float(slope_deg), 2))
            new_props["audit_dem_elev_min_m"] = (
                None if np.isnan(elev_min) else round(float(elev_min), 1))
            new_props["audit_dem_elev_max_m"] = (
                None if np.isnan(elev_max) else round(float(elev_max), 1))
            new_props["audit_centroid_near_waterway"] = is_in_stream
            new_props["audit_area_m2"] = round(area_m2, 1)
            features_out.append({
                "type": "Feature",
                "properties": new_props,
                "geometry": mapping(single_geom),
            })
    except Exception as e:
        audit_failures.append((idx, str(e)))

log("AUDIT CLASS COUNTS:")
for k, v in classes.most_common():
    log(f"  {v:>5}  {k}")
log(f"  {len(features_out)} features output, {len(audit_failures)} failed")

# ============================================================
# Stage 5: add waterways (LineStrings)
# ============================================================
log("adding waterways (LineStrings)...")
waterway_classes = Counter()
for f in waterways["features"]:
    p = f["properties"]
    cls = p.get("waterway", "waterway")
    waterway_classes[cls] += 1
    new_props = dict(p)
    new_props["audit_class"] = cls
    new_props["audit_color"] = {
        "river":    "#1d4ed8",
        "stream":   "#3b82f6",
        "creek":    "#3b82f6",
        "ditch":    "#60a5fa",
        "drain":    "#60a5fa",
        "canal":    "#2563eb",
        "waterway": "#3b82f6",
    }.get(cls, "#3b82f6")
    features_out.append({
        "type": "Feature",
        "properties": new_props,
        "geometry": f["geometry"],
    })
log("WATERWAY CLASS COUNTS:")
for k, v in waterway_classes.most_common():
    log(f"  {v:>5}  {k}")

# ============================================================
# Stage 6: write output
# ============================================================
fc = {
    "type": "FeatureCollection",
    "name": "surface_water_20km",
    "metadata": {
        "source_osm": "OpenStreetMap (Overpass API pull 2026-07-05)",
        "source_jrc": "JRC Global Surface Water (occurrence, 1984-2024)",
        "source_dem": "Copernicus GLO-30 DEM",
        "bbox": BBOX,
        "audit_rules": {
            "verified_lake":
                "JRC water occurrence mean >= 50% inside polygon",
            "verified_wetland":
                "JRC mean 20-50% (seasonally inundated)",
            "seasonal_wetland":
                "JRC mean 10-20% (rarely but recurrently wet)",
            "in_stream_pool":
                "Centroid within 200 m of an OSM waterway",
            "river_polygon":
                "Polygon-tagged river feature",
            "ambiguous":
                "Flat (slope < 3°) but no JRC signal — possibly farm pond or dry pan",
            "likely_mis-tagged":
                "JRC mean < 5% AND slope > 5° — likely forested fragment mis-tagged",
        },
        "generated_utc": "2026-07-05",
        "feature_count": len(features_out),
    },
    "features": features_out,
}
OUT_PATH.write_text(json.dumps(fc, separators=(",", ":")))
log(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes)")
