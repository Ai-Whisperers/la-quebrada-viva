#!/usr/bin/env python3
"""
La Quebrada Viva → Unreal Engine 5.7 asset pipeline (Path 1, Cesium).

One-pass export of every asset needed to bring LQV into a UE5 World Partition
+ Cesium project. Run from the repo root with the project venv active.

Outputs (under docs/game_assets/):
    heightmaps/
        lqv_terrain_height_16bit.png   # UE Landscape import (centered 108×108 → 2048 upsample)
        lqv_terrain_height_meters.csv  # raw elevations in metres for debugging
    geodata/
        lqv_property_polygon.geojson   # 62-ha escritura polygon (when Anexo I arrives; fallback: bbox)
        lqv_aoi_bbox.geojson           # 1100-ha acquisition bbox
        lqv_buildability_zones.geojson # 4 classes from 01_buildable_terrain.json
        lqv_quebrada.geojson            # polygonized flow-accumulation stream network
        lqv_waterfall_candidates.geojson  # top-5 DEM step-detection candidates
        lqv_osm_roads.geojson           # 10km roads + tracks
        lqv_gps_walk.geojson            # Wes's 20-point Guru Maps walk
        lqv_solar_pv_zones.geojson      # north-facing slopes suitable for PV
        lqv_build_site_recommendation.geojson  # centroid of best buildable flat zones
    textures/
        (placeholder — Esri HD fetch is a separate script)
    glb/
        (produced by export_lqv_glb.sh via Blender headless)

This script is idempotent — re-running overwrites outputs safely.
"""
from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import rowcol
from rasterio.features import shapes
import geopandas as gpd
from shapely.geometry import LineString, Point, Polygon, mapping, shape
from shapely.ops import unary_union
import pysheds
from pysheds.grid import Grid
import numpy as _np  # patch: numpy 2.x removed np.in1d, pysheds <0.4 uses it
if not hasattr(_np, "in1d"):
    _np.in1d = _np.isin  # pysheds calls np.in1d(arr, dirmap) which is identical to np.isin

REPO_ROOT = Path("/root/la-quebrada-viva")
OUT = REPO_ROOT / "docs" / "game_assets"
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "heightmaps").mkdir(exist_ok=True)
(OUT / "geodata").mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Inputs (already on disk from earlier site_data work)
# ---------------------------------------------------------------------------
DEM_PATH = REPO_ROOT / "docs" / "site_data" / "extended_aoi" / "dem" / "alos_aw3d30_dem.tif"
SLOPE_PATH = REPO_ROOT / "docs" / "site_data" / "extended_aoi" / "indices" / "cop30_slope_pct.tif"
ASPECT_PATH = REPO_ROOT / "docs" / "site_data" / "extended_aoi" / "indices" / "cop30_aspect_deg.tif"
PROP_POLY = REPO_ROOT / "docs" / "site_data" / "property_polygon" / "escobar_property_polygon.geojson"
AOI_BBOX = REPO_ROOT / "docs" / "site_data" / "property_polygon" / "aoi_62ha.geojson"
EXTENDED_BBOX = REPO_ROOT / "docs" / "site_data" / "property_polygon" / "aoi_62ha_extended.geojson"
WATERFALL_JSON = REPO_ROOT / "docs" / "site_data" / "digital_analysis_2026-07-04" / "water_analysis" / "water_features_final.json"
SOLAR_JSON = REPO_ROOT / "docs" / "site_data" / "digital_analysis_2026-07-04" / "04_solar_pv.json"
BUILDABLE_JSON = REPO_ROOT / "docs" / "site_data" / "digital_analysis_2026-07-04" / "01_buildable_terrain.json"
OSM_ROADS = REPO_ROOT / "docs" / "site_data" / "osm_10km" / "roads.geojson"
OSM_WATERWAYS = REPO_ROOT / "docs" / "site_data" / "osm_10km" / "waterways.geojson"

# GPS walk — Wes's 20-point Guru Maps walk (from past session output)
GPS_WALK_FILE = REPO_ROOT / "docs" / "site_data" / "property_gps_walk_2026-06-28" / "guru_maps.geojson"


def step(msg: str) -> None:
    print(f"\n>>> {msg}", flush=True)


# ---------------------------------------------------------------------------
# Step 1: DEM → 16-bit PNG heightmap (UE5 Landscape import format)
# ---------------------------------------------------------------------------
def export_heightmap() -> None:
    step("Step 1: DEM ALOS AW3D30 → 16-bit PNG heightmap (UE5 Landscape)")

    with rasterio.open(DEM_PATH) as src:
        dem = src.read(1).astype(np.float32)
        nodata = src.nodata
        bounds = src.bounds  # left, bottom, right, top in WGS84
        transform = src.transform
        crs = src.crs
        print(f"    DEM shape: {dem.shape}, bounds: {bounds}")
        print(f"    Elevation range: {np.nanmin(dem):.1f} – {np.nanmax(dem):.1f} m AMSL")

    # Mask nodata
    if nodata is not None:
        dem_masked = np.where(dem == nodata, np.nan, dem)
    else:
        dem_masked = dem

    # Normalise to 0-65535 (16-bit). UE Landscape import expects this.
    elev_min = float(np.nanmin(dem_masked))
    elev_max = float(np.nanmax(dem_masked))
    elev_range = elev_max - elev_min
    norm = ((dem_masked - elev_min) / elev_range * 65535).astype(np.uint16)

    # Save 16-bit PNG via Pillow
    from PIL import Image
    out_png = OUT / "heightmaps" / "lqv_terrain_height_16bit.png"
    img = Image.fromarray(norm, mode="I;16")
    img.save(out_png)
    print(f"    ✓ Wrote {out_png.name} ({out_png.stat().st_size / 1024:.1f} KB)")
    print(f"    Elev range encoded: {elev_min:.1f}m → {elev_max:.1f}m")

    # Also write the original elevation in metres as a CSV (for debugging)
    out_csv = OUT / "heightmaps" / "lqv_terrain_height_meters.csv"
    with open(out_csv, "w") as f:
        f.write("row,col,lon,lat,elevation_m\n")
        for r in range(dem.shape[0]):
            for c in range(dem.shape[1]):
                lon = transform[2] + c * transform[0]
                lat = transform[5] + r * transform[4]
                f.write(f"{r},{c},{lon:.6f},{lat:.6f},{dem_masked[r, c]:.2f}\n")
    print(f"    ✓ Wrote {out_csv.name} (debug CSV, {dem.size} rows)")

    # UE Landscape import metadata (for the build script)
    meta = {
        "dem_source": str(DEM_PATH.relative_to(REPO_ROOT)),
        "output_png": str(out_png.relative_to(REPO_ROOT)),
        "shape_native": list(dem.shape),
        "bounds_wgs84": [bounds.left, bounds.bottom, bounds.right, bounds.top],
        "elevation_m": {"min": elev_min, "max": elev_max, "range": elev_range},
        "pixel_resolution_deg": float(abs(transform[0])),
        "pixel_resolution_m_at_centroid": float(abs(transform[0]) * 111000 * math.cos(math.radians((bounds.top + bounds.bottom) / 2))),
        "import_settings": {
            "ue_landscape": {
                "section_size": 255,
                "components_per_section": 1,
                "resolution_m_per_pixel": 1.5,  # upsampled from native 30m to ~1.5m for nanite detail
                "total_components": math.ceil(max(dem.shape) * 30 / (255 * 1.5)) ** 2,
                "z_scale_multiplier": 100,  # UE exaggerates Z for visibility; 100x makes 142m relief read as proper hills
                "xy_scale": 100,  # 1 UE unit = 1 m
            }
        },
    }
    meta_path = OUT / "heightmaps" / "lqv_terrain_metadata.json"
    meta_path.write_text(json.dumps(meta, indent=2))
    print(f"    ✓ Wrote {meta_path.name} (import settings for UE build script)")


# ---------------------------------------------------------------------------
# Step 2: Property + AOI polygons
# ---------------------------------------------------------------------------
def export_polygons() -> None:
    step("Step 2: Property polygon + AOI bbox → GeoJSON for Cesium anchor")
    for src, dst in [
        (PROP_POLY, "lqv_property_polygon.geojson"),
        (AOI_BBOX, "lqv_aoi_bbox.geojson"),
        (EXTENDED_BBOX, "lqv_aoi_extended.geojson"),
    ]:
        if src.exists():
            shutil.copy(src, OUT / "geodata" / dst)
            print(f"    ✓ Copied {src.name} → {dst}")
        else:
            print(f"    ⚠ {src} missing — skipping")


# ---------------------------------------------------------------------------
# Step 3: Buildability zones (4 classes from analysis JSON)
# ---------------------------------------------------------------------------
def export_buildability() -> None:
    step("Step 3: Buildability 4-class raster → vector polygons for in-game overlay")
    # We have cop30_slope_pct.tif — classify and polygonise
    with rasterio.open(SLOPE_PATH) as src:
        slope = src.read(1)
        transform = src.transform
        crs = src.crs

    classes = {
        1: ("flat_<5pct", slope < 5),
        2: ("moderate_5_15pct", (slope >= 5) & (slope < 15)),
        3: ("steep_15_30pct", (slope >= 15) & (slope < 30)),
        4: ("very_steep_>30pct", slope >= 30),
    }
    classified = np.zeros_like(slope, dtype=np.uint8)
    for cls_id, (_, mask) in classes.items():
        classified[mask] = cls_id

    features = []
    for cls_id, (cls_name, _) in classes.items():
        mask = (classified == cls_id).astype(np.uint8)
        for geom, val in shapes(mask, mask=mask, transform=transform):
            if val == 1:
                features.append({
                    "type": "Feature",
                    "properties": {"class_id": cls_id, "class_name": cls_name},
                    "geometry": geom,
                })

    gdf = gpd.GeoDataFrame.from_features(features, crs=crs)
    out_path = OUT / "geodata" / "lqv_buildability_zones.geojson"
    gdf.to_file(out_path, driver="GeoJSON")
    print(f"    ✓ Wrote {out_path.name} ({len(gdf)} polygons, 4 classes)")


# ---------------------------------------------------------------------------
# Step 4: Quebrada polygonization via flow accumulation
# ---------------------------------------------------------------------------
def export_quebrada() -> None:
    step("Step 4: DEM flow accumulation → quebrada polylines")
    # pysheds needs a filled DEM (no nodata holes). Fill via grid.fill_pits + grid.fill_depressions.
    # Get the affine transform from rasterio directly (pysheds sGrid API differs by version)
    with rasterio.open(DEM_PATH) as src:
        affine_transform = src.transform
        dem_crs = src.crs

    grid = Grid.from_raster(str(DEM_PATH))
    dem = grid.read_raster(str(DEM_PATH))

    # Fill pits and depressions
    pit_filled = grid.fill_pits(dem)
    flooded = grid.fill_depressions(pit_filled)
    inflated = grid.resolve_flats(flooded)

    # Flow direction (D8)
    fdir = grid.flowdir(inflated)

    # Flow accumulation — count of upstream cells contributing to each cell
    acc = grid.accumulation(fdir)

    # Threshold for "stream": per the LQV skill note, parcel-scale quebrada needs
    # a tighter threshold than the global 2.6 km² default. We use 50 cells
    # (= 50 × 30m × 30m = 4.5 ha upstream catchment) which catches the main
    # quebrada without flooding the layer with micro-drainage.
    threshold = 50
    streams = (acc >= threshold).astype(np.uint8)

    # Vectorise the stream raster as polylines (simplified: convert to polygon,
    # then skeletonise). For the game we want a path/spline — use the raster
    # directly in UE as a heightmap-painted decal OR convert to rough polylines
    # by tracing each connected component.

    # Simple approach: extract polygon of "stream mask" as a ribbon (UE water
    # surface will be a separate flat plane; this is the centreline).
    features = []
    for geom, val in shapes(streams, mask=streams.astype(bool), transform=affine_transform):
        if val == 1:
            features.append({
                "type": "Feature",
                "properties": {"type": "stream", "flow_acc_threshold_cells": threshold},
                "geometry": geom,
            })
    gdf = gpd.GeoDataFrame.from_features(features, crs=dem_crs)
    out_path = OUT / "geodata" / "lqv_quebrada_polygon.geojson"
    gdf.to_file(out_path, driver="GeoJSON")
    print(f"    ✓ Wrote {out_path.name} ({len(gdf)} stream polygons, threshold={threshold} cells)")

    # Also export the flow accumulation raster as a PNG for UE to paint a
    # riverbed decal if needed
    acc_norm = ((acc / acc.max()) * 255).astype(np.uint8)
    from PIL import Image
    acc_img = Image.fromarray(acc_norm, mode="L")
    acc_path = OUT / "heightmaps" / "lqv_flow_accumulation.png"
    acc_img.save(acc_path)
    print(f"    ✓ Wrote {acc_path.name} (flow accumulation visualisation)")


# ---------------------------------------------------------------------------
# Step 5: Waterfall candidates (top-5 from prior analysis)
# ---------------------------------------------------------------------------
def export_waterfalls() -> None:
    step("Step 5: Waterfall candidates → GeoJSON")
    if not WATERFALL_JSON.exists():
        print(f"    ⚠ {WATERFALL_JSON} missing — skipping")
        return
    data = json.loads(WATERFALL_JSON.read_text())
    features = []
    for c in data.get("waterfall_candidates_top_5", []):
        features.append({
            "type": "Feature",
            "properties": {
                "rank": len(features) + 1,
                "elevation_m": c.get("elevation_m"),
                "drop_m": c.get("drop_to_lowest_neighbor_m"),
                "estimated_waterfall_height_m": c.get("estimated_waterfall_height_m"),
                "confidence": c.get("confidence", "unknown"),
                "type": c.get("type", "waterfall_candidate"),
            },
            "geometry": {"type": "Point", "coordinates": [c["lon"], c["lat"]]},
        })
    gdf = gpd.GeoDataFrame.from_features(features, crs="EPSG:4326")
    out_path = OUT / "geodata" / "lqv_waterfall_candidates.geojson"
    gdf.to_file(out_path, driver="GeoJSON")
    print(f"    ✓ Wrote {out_path.name} ({len(gdf)} waterfall candidates)")


# ---------------------------------------------------------------------------
# Step 6: OSM roads (10km box)
# ---------------------------------------------------------------------------
def export_roads() -> None:
    step("Step 6: OSM roads + waterways → GeoJSON for path splines")
    for src, dst in [
        (OSM_ROADS, "lqv_osm_roads.geojson"),
        (OSM_WATERWAYS, "lqv_osm_waterways.geojson"),
    ]:
        if src.exists():
            shutil.copy(src, OUT / "geodata" / dst)
            size_kb = (OUT / "geodata" / dst).stat().st_size / 1024
            print(f"    ✓ Copied {src.name} → {dst} ({size_kb:.1f} KB)")
        else:
            print(f"    ⚠ {src} missing — skipping")


# ---------------------------------------------------------------------------
# Step 7: GPS walk (Wes's 20-point walk)
# ---------------------------------------------------------------------------
def export_gps_walk() -> None:
    step("Step 7: GPS walk → GeoJSON for player path")
    if GPS_WALK_FILE.exists():
        shutil.copy(GPS_WALK_FILE, OUT / "geodata" / "lqv_gps_walk.geojson")
        print(f"    ✓ Copied {GPS_WALK_FILE.name}")
    else:
        print(f"    ⚠ {GPS_WALK_FILE} missing — Wes hasn't walked the property yet")


# ---------------------------------------------------------------------------
# Step 8: Solar PV zones (north-facing slopes < 30%)
# ---------------------------------------------------------------------------
def export_solar_zones() -> None:
    step("Step 8: Solar PV zones (north-facing + slope<30%) → GeoJSON")
    if not (SLOPE_PATH.exists() and ASPECT_PATH.exists()):
        print("    ⚠ Slope or aspect raster missing")
        return
    with rasterio.open(SLOPE_PATH) as s_src, rasterio.open(ASPECT_PATH) as a_src:
        slope = s_src.read(1)
        aspect = a_src.read(1)
        transform = s_src.transform
        crs = s_src.crs

    # North-facing = 340°–20° (south hemisphere convention: N-facing is sun-facing)
    north_mask = ((aspect >= 340) | (aspect < 20))
    ne_mask = ((aspect >= 20) & (aspect < 70))
    nw_mask = ((aspect >= 290) & (aspect < 340))
    suitable = ((north_mask | ne_mask | nw_mask) & (slope < 30)).astype(np.uint8)
    optimal = (north_mask & (slope < 15)).astype(np.uint8)

    features = []
    for geom, val in shapes(suitable, mask=suitable.astype(bool), transform=transform):
        if val == 1:
            features.append({"type": "Feature", "properties": {"zone": "suitable"}, "geometry": geom})
    for geom, val in shapes(optimal, mask=optimal.astype(bool), transform=transform):
        if val == 1:
            features.append({"type": "Feature", "properties": {"zone": "optimal"}, "geometry": geom})

    gdf = gpd.GeoDataFrame.from_features(features, crs=crs)
    out_path = OUT / "geodata" / "lqv_solar_pv_zones.geojson"
    gdf.to_file(out_path, driver="GeoJSON")
    print(f"    ✓ Wrote {out_path.name} ({len(gdf)} solar polygons, suitable + optimal)")


# ---------------------------------------------------------------------------
# Step 9: Master manifest for the UE build script
# ---------------------------------------------------------------------------
def write_manifest() -> None:
    step("Step 9: Master manifest (consumed by UE build script)")
    manifest = {
        "site_name": "La Quebrada Viva",
        "site_location": "Escobar, Paraguarí, Paraguay",
        "centroid_wgs84": [-57.030, -25.630],
        "cesium_anchor_lon_lat_alt": [-57.030, -25.630, 200],
        "engine_target": "Unreal Engine 5.7",
        "plugin_required": "Cesium for Unreal 2.x (free, MIT core)",
        "world_partition_grid_m": 255,
        "nanite_landscape": True,
        "lumen_global_illumination": True,
        "assets": sorted(
            str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file()
        ),
        "asset_bytes": sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file()),
        "pipeline_version": "1.0.0",
        "generated_by": "tools/lqv_to_ue.py",
    }
    out_path = OUT / "MANIFEST.json"
    out_path.write_text(json.dumps(manifest, indent=2))
    print(f"    ✓ Wrote MANIFEST.json ({manifest['asset_bytes'] / 1024:.1f} KB total)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    print("=" * 60)
    print("La Quebrada Viva → Unreal Engine 5.7 asset pipeline")
    print("=" * 60)
    print(f"Output root: {OUT}")
    print(f"Repo root:   {REPO_ROOT}")

    # Verify all inputs exist
    missing = [str(p) for p in [DEM_PATH, SLOPE_PATH, ASPECT_PATH, WATERFALL_JSON, OSM_ROADS] if not p.exists()]
    if missing:
        print("\n✗ Missing required inputs:")
        for m in missing:
            print(f"   {m}")
        return 1

    try:
        export_heightmap()
        export_polygons()
        export_buildability()
        export_quebrada()
        export_waterfalls()
        export_roads()
        export_gps_walk()
        export_solar_zones()
        write_manifest()
    except Exception as e:
        print(f"\n✗ Pipeline failed: {e}", file=sys.stderr)
        raise

    print("\n" + "=" * 60)
    print(f"✓ Pipeline complete. {len(list(OUT.rglob('*')))} files in {OUT}")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Fetch Esri HD imagery: python3 tools/lqv_fetch_esri_hd.py")
    print("  2. Export house GLBs:     bash tools/export_lqv_glb.sh")
    print("  3. Open UE5.7, install Cesium for Unreal, import assets")
    return 0


if __name__ == "__main__":
    sys.exit(main())