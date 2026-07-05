"""Build a unified 'woodland + forest' polygon layer for the LQV 20 km
box by fusing MULTIPLE data sources:

  1. MapBiomas Paraguay 2023 classes 3 (Forest Formation) + 6 (Flooded Forest)
  2. MapBiomas class 9 (Forest Plantation, palm monocultures)
  3. Hansen GFC treecover2000 (≥30% canopy in 2000) — at 30m raster,
     polygonised; provides the "ever-was-forest" baseline.
  4. OSM natural=wood (real woodland polygons from the mapper community,
     filtered to drop admin-boundary tags).

We DO NOT trust OSM landuse=forest alone because earlier audits
showed those are mostly admin boundary lines tagged incorrectly.

The merged layer adds a 'forest_source' property to every feature so the
viewer can colour-code by source if desired and the user can audit
which polygons came from where.
"""
import sys
import json
from pathlib import Path
import math
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from rasterio.features import shapes as rio_shapes
from shapely.geometry import shape, mapping
from shapely.validation import make_valid

ROOT = Path("/root/la-quebrada-viva")
OUT = ROOT / "splats/exports/web/data"

# 20 km box (S, W, N, E)
BBOX_S_W_N_E = (-25.787336, -57.231502, -25.427336, -56.839502)
# STAC / rasterio bounds (W, S, E, N)
BBOX_WSEN = (BBOX_S_W_N_E[1], BBOX_S_W_N_E[0], BBOX_S_W_N_E[3], BBOX_S_W_N_E[2])


def log(m):
    print(f"[merge_forest] {m}", file=sys.stderr, flush=True)


def crop_to_20km(path):
    """Return (arr, transform) cropped to the 20 km box."""
    with rasterio.open(str(path)) as ds:
        win = from_bounds(*BBOX_WSEN, ds.transform)
        r0, c0 = max(0, int(win.row_off)), max(0, int(win.col_off))
        r1 = min(ds.height, int(win.row_off + win.height))
        c1 = min(ds.width, int(win.col_off + win.width))
        if r1 <= r0 or c1 <= c0:
            return None, None
        arr = ds.read(1, window=((r0, r1), (c0, c1)))
        tf = rasterio.windows.transform(((r0, r1), (c0, c1)), ds.transform)
        return arr, tf


def polygonise_mask(arr, tf, threshold, name, color, source, descr,
                    min_pixels=10, min_ha=0.5):
    """Polygonise a boolean mask. Returns list of feature dicts."""
    out = []
    mask = arr >= threshold
    n_px = int(mask.sum())
    log(f"  {name}: {n_px} px ≥ {threshold}")
    if n_px < min_pixels:
        return out
    for geom, val in rio_shapes(arr.astype(np.int32), mask=mask,
                                connectivity=8, transform=tf):
        try:
            g = shape(geom)
            if g.is_empty:
                continue
            if not g.is_valid:
                g = make_valid(g)
            if g.is_empty or g.area < 1e-8:
                continue
            # Area in ha (lat-aware)
            try:
                c_lat = g.centroid.y
                deg_lat_m = 111320
                deg_lon_m = 111320 * math.cos(math.radians(c_lat))
                area_ha = (g.area * deg_lat_m * deg_lon_m) / 10000
            except Exception:
                area_ha = 0
            if area_ha < min_ha:
                continue
            g_simple = g.simplify(0.0001, preserve_topology=True)
            if g_simple.is_empty:
                continue
            out.append({
                "type": "Feature",
                "properties": {
                    "category": "woodland",
                    "woodland_kind": name,
                    "forest_source": source,
                    "color": color,
                    "description": descr,
                    "pixel_count": n_px,
                    "area_ha": round(area_ha, 2),
                },
                "geometry": mapping(g_simple),
            })
        except Exception:
            continue
    log(f"    → kept {len(out)} polygons after size filter ≥{min_ha} ha")
    return out


def main():
    log("=" * 60)
    log("Merge all woodland data sources into one layer")
    log("=" * 60)
    all_feats = []

    # ---- 1. MapBiomas Forest Formation (3) + Flooded Forest (6) ----
    log("MapBiomas Forest + Gallery")
    src = ROOT / "docs/site_data/mapbiomas_paraguay/2023/mapbiomas_2023_aoi_50km.tif"
    arr, tf = crop_to_20km(src)
    if arr is not None:
        for code, label, color, descr in [
            (3, "Forest Formation (upland)", "#15803d",
             "Dense upland Atlantic Forest mosaic"),
            (6, "Flooded Forest (gallery)", "#0d9488",
             "Gallery forest along quebradas"),
        ]:
            mask = (arr == code)
            n_px = int(mask.sum())
            log(f"  class {code} {label}: {n_px} px")
            for geom, val in rio_shapes(arr.astype(np.int32), mask=mask,
                                        connectivity=8, transform=tf):
                try:
                    g = shape(geom)
                    if g.is_empty or g.area < 1e-8:
                        continue
                    if not g.is_valid:
                        g = make_valid(g)
                    try:
                        c_lat = g.centroid.y
                        deg_lat_m = 111320
                        deg_lon_m = 111320 * math.cos(math.radians(c_lat))
                        area_ha = (g.area * deg_lat_m * deg_lon_m) / 10000
                    except Exception:
                        area_ha = 0
                    # Drop tiny fragments (< 0.5 ha) — these are edge
                    # slivers that obscure the larger patches.
                    if area_ha < 0.5:
                        continue
                    g_simple = g.simplify(0.0003, preserve_topology=True)
                    if g_simple.is_empty:
                        continue
                    all_feats.append({
                        "type": "Feature",
                        "properties": {
                            "category": "woodland",
                            "woodland_kind": label,
                            "forest_source": "MapBiomas Paraguay Collection 2 (2023)",
                            "color": color,
                            "description": descr,
                            "class_code": int(code),
                            "area_ha": round(area_ha, 2),
                        },
                        "geometry": mapping(g_simple),
                    })
                except Exception:
                    continue

    # ---- 2. Hansen GFC treecover2000 ≥ 30% (any year-2000 forest baseline) ----
    log("Hansen treecover2000 ≥30%")
    src = ROOT / "docs/site_data/hansen_gfc/treecover2000/treecover2000_aoi_50km.tif"
    arr, tf = crop_to_20km(src)
    if arr is not None:
        for thr in [30, 75]:
            color = "#365314" if thr >= 75 else "#166534"
            descr = (f"Hansen ≥{thr}% canopy in 2000 — "
                     f"{'high-confidence closed canopy' if thr >= 75 else 'open canopy / fragmented forest'}")
            label = f"Hansen ≥{thr}% canopy (2000)"
            new = polygonise_mask(arr, tf, thr, label, color,
                                  "Hansen GFC v1.12 (2000 baseline)",
                                  descr, min_pixels=10)
            all_feats.extend(new)
            log(f"  {label}: +{len(new)} polygons")

    # ---- 3. OSM natural=wood (real mappers' woodland, NOT admin boundaries) ----
    log("OSM natural=wood (filtered to large polygons)")
    src = OUT / "osm_20km/trees.geojson"
    if src.exists():
        d = json.load(open(src))
        kept = 0
        for f in d['features']:
            p = f['properties']
            if p.get('natural') != 'wood':
                continue
            try:
                g = shape(f['geometry'])
                if g.is_empty or g.area < 1e-7:
                    continue
                if not g.is_valid:
                    g = make_valid(g)
                # Drop admin-boundary-style thin elongated polygons
                bbox = g.bounds  # (minx, miny, maxx, maxy)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                # Drop very thin (< 0.001° wide) admin-boundary-like shapes
                if w < 0.0008 or h < 0.0008:
                    continue
                # Compute area
                c_lat = g.centroid.y
                deg_lat_m = 111320
                deg_lon_m = 111320 * math.cos(math.radians(c_lat))
                area_ha = (g.area * deg_lat_m * deg_lon_m) / 10000
                if area_ha < 0.5:
                    continue
                all_feats.append({
                    "type": "Feature",
                    "properties": {
                        "category": "woodland",
                        "woodland_kind": "OSM natural=wood",
                        "forest_source": "OpenStreetMap mapper (Overpass 2026-07-05)",
                        "color": "#22c55e",
                        "description": "OpenStreetMap-tagged woodland, filtered to drop thin admin-boundary tags",
                        "area_ha": round(area_ha, 2),
                        "name": p.get('name', ''),
                    },
                    "geometry": mapping(g),
                })
                kept += 1
            except Exception:
                continue
        log(f"  OSM wood kept: {kept} polygons")

    log(f"\nTotal merged forest polygons: {len(all_feats):,}")

    # Write out
    fc = {
        "type": "FeatureCollection",
        "name": "woodland_merged_20km",
        "metadata": {
            "source": "Merged from MapBiomas Paraguay C2 (2023) + Hansen GFC v1.12 + OSM",
            "bbox": list(BBOX_S_W_N_E),
            "license": "Mixed: MapBiomas CC-BY-SA-4.0, Hansen CC-BY-4.0, ODbL",
            "feature_count": len(all_feats),
            "generated_utc": "2026-07-05",
            "notes": (
                "Per-source polygonisation is intentional — overlapping "
                "polygons are kept separately so the user can audit each "
                "data product independently. MapBiomas is the most "
                "authoritative for 2023 land cover; Hansen treecover is "
                "the historical baseline; OSM is mapper ground truth "
                "(filtered to drop admin-boundary mis-tags)."
            ),
        },
        "features": all_feats,
    }
    out = OUT / "woodland_merged_20km.geojson"
    out.write_text(json.dumps(fc, separators=(",", ":")))
    log(f"wrote {out} ({out.stat().st_size/1024/1024:.2f} MB)")

    # Source breakdown
    from collections import Counter
    sources = Counter(f['properties']['forest_source'].split(' (')[0]
                      for f in all_feats)
    log("Source breakdown:")
    for s, n in sources.most_common():
        log(f"  {s}: {n}")


if __name__ == "__main__":
    main()