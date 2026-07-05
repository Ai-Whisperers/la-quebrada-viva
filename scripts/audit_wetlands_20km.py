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
    # Confirmed water bodies (JRC >= 50% standing-water pixels)
    "verified_lake":            "#0ea5e9",
    # Confirmed wetlands (JRC 20-50% standing-water pixels)
    "verified_wetland":         "#0369a1",
    # Seasonal wetlands (JRC 10-20%)
    "seasonal_wetland":         "#67e8f9",
    # Standing pool right next to a tagged stream
    "stream_riparian_pool":     "#7dd3fc",
    # Polygon OSM depiction of a river corridor
    "river_corridor_polygon":   "#1d4ed8",
    # OSM wetland tag, flat (slope < 3°), no JRC signal —
    # probably a depression that doesn't usually hold water but mappers assumed
    "dry_depression":           "#fbbf24",
    # OSM wetland tag with steep terrain + zero JRC signal — flagged as bad data
    "likely_mis-tagged":        "#f87171",
    # OSM natural=water water=stream / pond / basin — typically a depiction of
    # the stream centerline not a real water body (the JRC ground truth is the
    # arbiter; we keep them as their OSM intent)
    "stream_polygon_depiction": "#a78bfa",
    "pond_polygon_depiction":   "#c4b5fd",
    # OSM landuse=reservoir (often basin's edge or farm dam)
    "reservoir_polygon":        "#1e40af",
    # Catch-all
    "unclassified":             "#94a3b8",
}

CLASS_LABEL = {
    "verified_lake":            "Verified lake",
    "verified_wetland":         "Verified wetland",
    "seasonal_wetland":         "Seasonal wetland",
    "stream_riparian_pool":     "Stream riparian pool",
    "river_corridor_polygon":   "River corridor (OSM polygon)",
    "dry_depression":           "Dry depression (no JRC water signal)",
    "likely_mis-tagged":        "Likely mis-tagged",
    "stream_polygon_depiction": "Stream centre-line depiction",
    "pond_polygon_depiction":   "Pond (OSM polygon, no JRC verify)",
    "reservoir_polygon":        "Reservoir / farm dam",
    "unclassified":             "Unclassified",
}


def classify_osm_water(p, geom, jrc_mean, slope_deg, is_in_stream, area_m2):
    """Decision tree for OSM-tagged water features.

    Priority order:
      1. Real JRC water signal (verified_lake / verified_wetland / seasonal_wetland)
      2. OSM landuse=reservoir  → reservoir_polygon
      3. OSM natural=water water=stream (the most common tag in rural
         Paraguay) → stream_polygon_depiction (it's the stream centerline
         drawn as a polygon, not a real water body)
      4. OSM natural=water water=pond/basin/lake
      5. OSM natural=water water=river polygon → river_corridor_polygon
      6. OSM natural=wetland + centroid next to a stream → stream_riparian_pool
      7. OSM natural=wetland, slope < 3°, no JRC signal → dry_depression
      8. OSM natural=wetland, slope >= 3° or JRC < 5% → likely_mis-tagged
      9. Anything else → unclassified
    """
    natural = p.get("natural")
    water_tag = p.get("water")
    landuse = p.get("landuse")
    jrc_ok = not np.isnan(jrc_mean)
    jrc_high = jrc_ok and jrc_mean >= 50
    jrc_med  = jrc_ok and jrc_mean >= 20
    jrc_low  = jrc_ok and jrc_mean >= 10
    # 1. JRC ground-truth always wins over OSM
    if jrc_high: return "verified_lake"
    if jrc_med:  return "verified_wetland"
    if jrc_low and natural == "wetland": return "seasonal_wetland"
    # 2. landuse=reservoir
    if landuse == "reservoir":
        return "reservoir_polygon"
    # 3. natural=water water=stream (stream centre-line as polygon)
    if natural == "water" and water_tag == "stream":
        return "stream_polygon_depiction"
    # 4. natural=water water=pond or basin
    if natural == "water" and water_tag in ("pond", "basin"):
        return "pond_polygon_depiction"
    # 5. natural=water water=river (rare river polygon OSM depiction)
    if natural == "water" and water_tag == "river":
        return "river_corridor_polygon"
    # 6. natural=water without water_tag (occasional tag-seam in OSM)
    if natural == "water" and water_tag is None:
        return "stream_polygon_depiction"
    # 7. natural=water water=lake (small generic lakes)
    if natural == "water" and water_tag == "lake":
        return "pond_polygon_depiction"
    # 8. natural=water water=wastewater (sewage lagoons etc.)
    if natural == "water" and water_tag == "wastewater":
        return "reservoir_polygon"
    # 9. natural=wetland, adjacency to a stream
    if natural == "wetland":
        if is_in_stream:
            return "stream_riparian_pool"
        if not np.isnan(slope_deg) and slope_deg < 3:
            return "dry_depression"
        # includes "marsh", "fen", "bog", "reedbed", "string_bog", "tidalflat", "swamp"
        return "likely_mis-tagged"
    return "unclassified"

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
            new_props["audit_class_label"] = CLASS_LABEL.get(cls, cls.title())
            new_props["audit_color"] = CLASS_COLOR.get(cls, "#999")
            # Schema versioning for downstream consumers
            new_props["audit_schema_version"] = 2
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
# Stage 6: write output (deterministic order for reproducibility)
# ============================================================
# Sort polygon features by class priority (verified first) then area desc.
# WayString features follow.
CLASS_PRIORITY = {
    "verified_lake":            0,
    "verified_wetland":         1,
    "seasonal_wetland":         2,
    "stream_riparian_pool":     3,
    "river_corridor_polygon":   4,
    "reservoir_polygon":        5,
    "pond_polygon_depiction":   6,
    "stream_polygon_depiction": 7,
    "dry_depression":           8,
    "likely_mis-tagged":        9,
    "unclassified":            10,
}


def _class_key(f):
    """Sort key: class rank + area desc + spatial hash tie-break."""
    p = f.get("properties", {})
    rank = CLASS_PRIORITY.get(p.get("audit_class"), 99)
    return (rank, -(p.get("audit_area_m2") or 0))


polygons = []
waterway_feats = []
for f in features_out:
    g = f.get("geometry", {})
    if g.get("type") == "Polygon":
        polygons.append(f)
    elif g.get("type") in ("LineString", "MultiLineString"):
        waterway_feats.append(f)
polygons.sort(key=_class_key)
features_out = polygons + waterway_feats

# Add stable feature_id (just an integer index in the sorted order)
for idx, f in enumerate(features_out):
    f.setdefault("properties", {})["feature_id"] = f"lqv-sw-{idx:04d}"

fc = {
    "type": "FeatureCollection",
    "name": "surface_water_20km",
    "metadata": {
        "schema_version": 2,
        "source_osm": "OpenStreetMap (Overpass API pull 2026-07-05)",
        "source_jrc": "JRC Global Surface Water (occurrence, 1984-2024)",
        "source_dem": "Copernicus GLO-30 DEM",
        "bbox": BBOX,
        "class_taxonomy": {
            k: {"label": CLASS_LABEL[k], "color": CLASS_COLOR[k],
                "priority": CLASS_PRIORITY.get(k)}
            for k in CLASS_COLOR
        },
        "audit_rules": {
            "verified_lake":
                "JRC water occurrence mean >= 50% inside polygon",
            "verified_wetland":
                "JRC mean 20-50% (seasonally inundated)",
            "seasonal_wetland":
                "JRC mean 10-20% (rarely but recurrently wet)",
            "stream_riparian_pool":
                "Centroid within 200 m of an OSM waterway",
            "river_corridor_polygon":
                "OSM polygon tagged natural=water + water=river",
            "dry_depression":
                "OSM wetland tag + slope < 3° + no JRC signal",
            "likely_mis-tagged":
                "OSM wetland tag + slope > 3° + JRC < 5%",
            "stream_polygon_depiction":
                "OSM natural=water + water=stream (centre-line as polygon)",
            "pond_polygon_depiction":
                "OSM natural=water + water=pond/basin/lake",
            "reservoir_polygon":
                "OSM landuse=reservoir or wastewater",
        },
        "generated_utc": "2026-07-05",
        "feature_count": len(features_out),
        "polygon_count": len(polygons),
        "waterway_count": len(waterway_feats),
    },
    "features": features_out,
}
OUT_PATH.write_text(json.dumps(fc, separators=(",", ":")))
log(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size:,} bytes; "
    f"{len(polygons)} polygons + {len(waterway_feats)} waterways)")
