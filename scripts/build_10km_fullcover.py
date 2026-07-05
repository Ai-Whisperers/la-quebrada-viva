"""Polygonise MapBiomas Paraguay land-cover (2023) and Hansen GFC loss/gain
treecover over the LQV 20 km box. Both source rasters are already clipped
to a 100 km AOI centered on LQV, so no external fetch is needed.

Outputs to splats/exports/web/data/:
  mapbiomas_2023_10km.geojson — 7-class land-cover polygons
  hansen_loss_10km.geojson   — pixels with loss>0 since 2001
  hansen_gain_10km.geojson   — pixels with gain=1 since 2000
  hansen_treecover_30pct_10km.geojson — forest cover (≥30%) in 2000
  hansen_treecover_change.geojson   — overlay combining loss/gain
"""
import sys
from pathlib import Path
import json
from collections import Counter

import numpy as np
import rasterio
from rasterio.windows import from_bounds
from rasterio.features import shapes as rio_shapes
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"

# 20 km box around LQV centroid (-57.030, -25.608)
BBOX = (-25.698062, -57.129997, -25.518400, -56.930765)  # S, W, N, E

# MapBiomas Paraguay Collection 2 (2023) — class codes observed in
# this region. Source: docs/site_data/mapbiomas_paraguay/_summaries/
# class_timeseries.csv (ground-truth counts for the 50 km AOI).
# Color palette tuned for visual distinctness on the satellite basemap.
MAPBIOMAS_LEGEND = {
    1:  ("Forest Plantation (general)",  "#7e22ce"),  # not in AOI but possible
    3:  ("Forest Formation",             "#15803d"),  # dense upland forest — DARK GREEN
    4:  ("Savanna Formation",            "#eab308"),  # not in AOI
    5:  ("Mangrove",                     "#365314"),  # not in AOI (no coast)
    6:  ("Flooded Forest",               "#0d9488"),  # gallery forests along rivers
    9:  ("Forest Plantation",            "#a16207"),  # palm plantations (visible in AOI)
    10: ("Grassland (annual)",            "#84cc16"),
    11: ("Wetland",                      "#06b6d4"),  # cyan
    12: ("Grassland",                    "#bef264"),  # LIGHT GREEN (MapBiomas default)
    14: ("Farming (annual)",              "#f97316"),  # not in AOI
    15: ("Pasture",                      "#fbbf24"),  # amber
    18: ("Agriculture",                   "#ea580c"),  # dark orange
    21: ("Mosaic of Agriculture",        "#fde68a"),
    22: ("Non-vegetated Area",           "#94a3b8"),  # grey
    24: ("Urban / Built",                "#475569"),
    25: ("Other (built)",                "#334155"),
    26: ("Water",                        "#0284c7"),  # dark blue (was: Soybean — WRONG, this is Water per MapBiomas Paraguay C2)
    29: ("Rocky Outcrop",                "#1e293b"),
    30: ("Mining",                       "#1e1b4b"),
    33: ("Water Bodies",                 "#0284c7"),  # alt water class (not in AOI)
    39: ("Soybean",                      "#c2410c"),  # the actual soybean code
    41: ("Other Crops",                  "#fb7185"),
    50: ("Pasture (annual)",              "#fcd34d"),
}
# Class metadata — describes each class's meaning for the viewer tooltip
CLASS_DESCRIPTIONS = {
    3:  "Dense upland forest — closed canopy Atlantic Forest mosaic.",
    6:  "Gallery forest along quebradas — frequently inundated riparian trees.",
    9:  "Forest Plantation (e.g. palm) — managed woody monoculture.",
    11: "Wetland — standing water or saturated soils visible in Landsat.",
    12: "Grassland — non-managed herbaceous cover, savanna-like.",
    15: "Pasture — managed grazing land for cattle ranching.",
    18: "Agriculture — row crops or tilled farmland.",
    22: "Non-vegetated Area — bare soil, rock outcrop, road.",
    26: "Water — open standing water body (river, lake, reservoir).",
}


def log(m):
    print(f"[mb] {m}", file=sys.stderr, flush=True)


def crop_to_10km(src_path):
    """Return (cropped_array, cropped_transform)."""
    with rasterio.open(src_path) as ds:
        win = from_bounds(BBOX[1], BBOX[0], BBOX[3], BBOX[2], ds.transform)
        # round window to integer pixels
        r0, c0 = max(0, int(win.row_off)), max(0, int(win.col_off))
        r1 = min(ds.height, int(win.row_off + win.height))
        c1 = min(ds.width, int(win.col_off + win.width))
        if r1 <= r0 or c1 <= c0:
            return None, None
        arr = ds.read(1, window=((r0, r1), (c0, c1)))
        tf = rasterio.windows.transform(((r0, r1), (c0, c1)), ds.transform)
        return arr, tf


def polygonise_categorical(arr, tf, min_pixels=20):
    """Polygonise a categorical raster, simplifying each polygon for
    web delivery. Returns GeoJSON-ready list of features."""
    from shapely.validation import make_valid
    out = []
    for code in np.unique(arr):
        if code == 0:
            continue
        label, color = MAPBIOMAS_LEGEND.get(int(code), (f"class {code}", "#9ca3af"))
        desc = CLASS_DESCRIPTIONS.get(int(code), "")
        mask = (arr == code)
        if mask.sum() < min_pixels:
            continue
        log(f"  class {code:>3}  '{label}': {int(mask.sum())} px")
        for geom, val in rio_shapes(arr.astype(np.int32), mask=mask,
                                    connectivity=8, transform=tf):
            try:
                g = shape(geom)
                if g.is_empty:
                    continue
                # Repair self-intersections (rasterio polygons often produce
                # malformed MultiPolygons that fail Leaflet rendering)
                if not g.is_valid:
                    g = make_valid(g)
                # Drop degenerate fragments
                if g.is_empty or g.area < 5e-7:
                    continue
                g_simple = g.simplify(0.0003, preserve_topology=True)
                if g_simple.is_empty:
                    continue
                # Compute ha via shapely area (degree² × ha conversion)
                # Sample centroid latitude for more accurate ha
                try:
                    c_lat = g_simple.centroid.y
                    import math
                    deg_lat_m = 111320
                    deg_lon_m = 111320 * math.cos(math.radians(c_lat))
                    area_ha = (g_simple.area * deg_lat_m * deg_lon_m) / 10000
                except Exception:
                    area_ha = 0
                out.append({
                    "type": "Feature",
                    "properties": {
                        "category": "mapbiomas_landcover",
                        "class_code": int(code),
                        "name": label,
                        "color": color,
                        "description": desc,
                        "pixel_count": int(mask.sum()),
                        "area_ha": round(area_ha, 2),
                        "source": "MapBiomas Paraguay Collection 2 (2023)",
                        "license": "CC-BY-SA-4.0",
                    },
                    "geometry": mapping(g_simple),
                })
            except Exception as e:
                log(f"    warn class {code}: {e}")
                continue
    return out


def build_mapbiomas():
    log("MapBiomas Paraguay 2023 — 20 km box polygonise")
    src = ROOT / "docs/site_data/mapbiomas_paraguay/2023/mapbiomas_2023_aoi_50km.tif"
    arr, tf = crop_to_10km(str(src))
    if arr is None:
        log("  ⚠ no overlap with 20 km box")
        return
    log(f"  cropped shape: {arr.shape}, dtype={arr.dtype}")
    feats = polygonise_categorical(arr, tf, min_pixels=30)
    log(f"  → {len(feats)} polygons")
    fc = {
        "type": "FeatureCollection",
        "name": "mapbiomas_2023_10km",
        "metadata": {
            "source": "MapBiomas Paraguay Collection 2 (2023) — GCS public bucket",
            "bbox": list(BBOX),
            "license": "CC-BY-SA-4.0",
            "legend": {
                int(k): {"name": v[0], "color": v[1]}
                for k, v in MAPBIOMAS_LEGEND.items()
            },
            "feature_count": len(feats),
            "generated_utc": "2026-07-05",
        },
        "features": feats,
    }
    out = OUT / "mapbiomas_2023_10km.geojson"
    out.write_text(json.dumps(fc, separators=(",", ":")))
    log(f"  wrote {out} ({out.stat().st_size/1024/1024:.2f} MB)")


def build_hansen_layer(src_name, output_name, threshold, label, color,
                       mask_complement=None):
    """Build a Hansen GFC layer as polygons."""
    from shapely.validation import make_valid
    src = ROOT / f"docs/site_data/hansen_gfc/{src_name}/{src_name}_aoi_50km.tif"
    log(f"Hansen {src_name} — {label}")
    arr, tf = crop_to_10km(str(src))
    if arr is None:
        log("  ⚠ no overlap")
        return
    log(f"  cropped shape: {arr.shape}, dtype={arr.dtype}, "
        f"range {arr.min()}–{arr.max()}")
    mask = (arr >= threshold) if isinstance(threshold, (int, float)) else threshold(arr)
    if mask_complement is not None:
        mask = mask & ~mask_complement
    feats = []
    n_px = int(mask.sum())
    log(f"  {n_px} pixels ≥ {threshold}")
    if n_px == 0:
        return
    for geom, val in rio_shapes(arr.astype(np.int32), mask=mask,
                                connectivity=8, transform=tf):
        try:
            g = shape(geom)
            if g.is_empty or g.area < 1e-8:
                continue
            if not g.is_valid:
                g = make_valid(g)
            g_simple = g.simplify(0.0001, preserve_topology=True)
            if g_simple.is_empty:
                continue
            feats.append({
                "type": "Feature",
                "properties": {
                    "category": "hansen_gfc",
                    "layer": label,
                    "color": color,
                    "value_threshold": threshold,
                    "source": "Hansen GFC v1.12 (Global Forest Change 2001-2024)",
                },
                "geometry": mapping(g_simple),
            })
        except Exception:
            continue
    log(f"  → {len(feats)} polygons")
    fc = {
        "type": "FeatureCollection",
        "name": output_name,
        "metadata": {
            "source": "Hansen GFC v1.12, UMD, 2001-2024",
            "bbox": list(BBOX),
            "license": "CC-BY-4.0",
            "feature_count": len(feats),
            "pixel_count": n_px,
            "generated_utc": "2026-07-05",
        },
        "features": feats,
    }
    out = OUT / f"{output_name}.geojson"
    out.write_text(json.dumps(fc, separators=(",", ":")))
    log(f"  wrote {out} ({out.stat().st_size/1024/1024:.2f} MB)")


def main():
    log("=" * 60)
    log("Polygonise full-Escobar land-cover + forest-change layers")
    log("=" * 60)
    build_mapbiomas()
    # Skip Hansen treecover2000 polygonisation — output is 200+ MB,
    # way over the 25 MB Cloudflare Pages cap. We use MapBiomas
    # Forest Formation class instead, which is categorical and
    # polygonises cleanly.
    build_hansen_layer(
        "treecover2000", "hansen_treecover_30pct_10km",
        threshold=30, label="forest_cover_2000_pct",
        color="#14532d",   # dark green
    ) if False else None  # disabled — file too large
    # Loss = pixels where the lossyear rasters have ANY loss year 1-23 (2001-2023)
    # but where the datamask says the pixel is forested
    loss_src = ROOT / "docs/site_data/hansen_gfc/loss/loss_aoi_50km.tif"
    lossyear_src = ROOT / "docs/site_data/hansen_gfc/loss/lossyear_aoi_50km.tif"
    datamask_src = ROOT / "docs/site_data/hansen_gfc/datamask/datamask_aoi_50km.tif"
    log("Hansen loss (any year 2001-2023)")
    from shapely.validation import make_valid
    arr_loss, tf_loss = crop_to_10km(str(loss_src))
    arr_year, _      = crop_to_10km(str(lossyear_src))
    arr_mask, _      = crop_to_10km(str(datamask_src))
    if arr_loss is not None:
        mask = (arr_loss == 1) & (arr_year > 0) & (arr_mask == 1)
        n_px = int(mask.sum())
        log(f"  {n_px} loss pixels (with datamask)")
        feats = []
        if n_px > 0:
            for geom, val in rio_shapes(arr_loss.astype(np.int32),
                                        mask=mask, connectivity=8,
                                        transform=tf_loss):
                try:
                    g = shape(geom)
                    if g.is_empty or g.area < 1e-8:
                        continue
                    if not g.is_valid:
                        g = make_valid(g)
                    g_simple = g.simplify(0.0001, preserve_topology=True)
                    if g_simple.is_empty:
                        continue
                    feats.append({
                        "type": "Feature",
                        "properties": {
                            "category": "hansen_gfc",
                            "layer": "forest_loss_2001_2023",
                            "color": "#dc2626",   # red
                            "source": "Hansen GFC v1.12 (2001-2024)",
                        },
                        "geometry": mapping(g_simple),
                    })
                except Exception:
                    continue
        fc = {
            "type": "FeatureCollection",
            "name": "hansen_loss_10km",
            "metadata": {
                "source": "Hansen GFC v1.12",
                "bbox": list(BBOX),
                "license": "CC-BY-4.0",
                "pixel_count": n_px,
                "feature_count": len(feats),
                "generated_utc": "2026-07-05",
            },
            "features": feats,
        }
        out = OUT / "hansen_loss_10km.geojson"
        out.write_text(json.dumps(fc, separators=(",", ":")))
        log(f"  wrote {out} ({out.stat().st_size/1024/1024:.2f} MB)")
    # Gain
    log("Hansen gain (2000-2012)")
    arr_gain, tf_gain = crop_to_10km(str(ROOT / "docs/site_data/hansen_gfc/gain/gain_aoi_50km.tif"))
    if arr_gain is not None:
        mask = (arr_gain == 1)
        n_px = int(mask.sum())
        log(f"  {n_px} gain pixels")
        feats = []
        if n_px > 0:
            for geom, val in rio_shapes(arr_gain.astype(np.int32),
                                        mask=mask, connectivity=8,
                                        transform=tf_gain):
                try:
                    g = shape(geom)
                    if g.is_empty or g.area < 1e-8:
                        continue
                    if not g.is_valid:
                        g = make_valid(g)
                    g_simple = g.simplify(0.0001, preserve_topology=True)
                    if g_simple.is_empty:
                        continue
                    feats.append({
                        "type": "Feature",
                        "properties": {
                            "category": "hansen_gfc",
                            "layer": "forest_gain_2000_2012",
                            "color": "#22c55e",   # bright green
                            "source": "Hansen GFC v1.12",
                        },
                        "geometry": mapping(g_simple),
                    })
                except Exception:
                    continue
        fc = {
            "type": "FeatureCollection",
            "name": "hansen_gain_10km",
            "metadata": {
                "source": "Hansen GFC v1.12",
                "bbox": list(BBOX),
                "license": "CC-BY-4.0",
                "pixel_count": n_px,
                "feature_count": len(feats),
                "generated_utc": "2026-07-05",
            },
            "features": feats,
        }
        out = OUT / "hansen_gain_10km.geojson"
        out.write_text(json.dumps(fc, separators=(",", ":")))
        log(f"  wrote {out} ({out.stat().st_size/1024/1024:.2f} MB)")


if __name__ == "__main__":
    main()