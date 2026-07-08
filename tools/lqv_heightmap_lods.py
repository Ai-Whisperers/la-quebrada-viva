#!/usr/bin/env python3
"""
LQV → 3-tier heightmap pipeline for distance-based LOD terrain rendering.

Generates three PNG heightmaps from the ALOS AW3D30 DEM, each at a different
resolution suitable for a different viewing distance:

  LOD0 (parcel scale)   — 0-500m from camera:  1.5 m/pixel, 1024×1024 pixels,
                           covers ~1.5 km × 1.5 km, centered on LQV parcel.
                           Source: bilinear upsample of native DEM.

  LOD1 (Escobar scale)   — 500m-5km: 15 m/pixel, 512×512 pixels,
                           covers ~7.7 km × 7.7 km, centered on LQV parcel.
                           Source: native DEM (30 m → 15 m via bicubic).

  LOD2 (regional scale)  — 5-30 km: 60 m/pixel, 384×384 pixels,
                           covers ~23 km × 23 km, centered on LQV parcel.
                           Source: native DEM averaged into 2×2 blocks then
                           scaled.

All PNGs are 16-bit grayscale (UE5 / CesiumJS standard heightmap format).
Output: docs/game_assets/heightmaps/lod{0,1,2}_terrain.png + bounds JSON.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject
from PIL import Image

REPO = Path("/root/la-quebrada-viva")
DEM_PATH = REPO / "docs" / "site_data" / "extended_aoi" / "dem" / "alos_aw3d30_dem.tif"
OUT_DIR = REPO / "docs" / "game_assets" / "heightmaps"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CENTROID_LON = -57.030
CENTROID_LAT = -25.630


def make_aoi_bbox(center_lon: float, center_lat: float, half_extent_m: float) -> tuple[float, float, float, float]:
    """Return (west, south, east, north) for a square AOI of half-extent in metres."""
    dlat = half_extent_m / 111000
    dlon = half_extent_m / (111000 * math.cos(math.radians(center_lat)))
    return center_lon - dlon, center_lat - dlat, center_lon + dlon, center_lat + dlat


def read_dem_cropped_to_aoi(west: float, south: float, east: float, north: float) -> tuple[np.ndarray, dict]:
    """Read the DEM clipped to the AOI, return array + transform info."""
    with rasterio.open(DEM_PATH) as src:
        from rasterio.windows import from_bounds
        win = from_bounds(west, south, east, north, src.transform)
        win = win.round_offsets()
        dem = src.read(1, window=win)
        src_transform = src.window_transform(win)
        # Build the new transform for the AOI
        res_x = (east - west) / dem.shape[1]
        res_y = (north - south) / dem.shape[0]
        new_transform = rasterio.Affine(res_x, 0, west, 0, -res_y, north)
    return dem.astype(np.float32), {
        "bounds_wgs84": [west, south, east, north],
        "transform": [new_transform.a, new_transform.b, new_transform.c, new_transform.d, new_transform.e, new_transform.f],
        "shape": list(dem.shape),
        "pixel_resolution_deg": abs(res_x),
        "pixel_resolution_m_at_centroid": abs(res_x) * 111000 * math.cos(math.radians(CENTROID_LAT)),
    }


def resample_to_target(dem: np.ndarray, current_res_m: float, target_res_m: float, target_size: tuple[int, int]) -> np.ndarray:
    """Bilinear/bicubic resample DEM to target resolution."""
    from scipy.ndimage import zoom
    # Current shape → target shape
    cur_h, cur_w = dem.shape
    target_h, target_w = target_size
    zoom_y = target_h / cur_h
    zoom_x = target_w / cur_w
    if abs(zoom_y - 1.0) < 0.05 and abs(zoom_x - 1.0) < 0.05:
        return dem
    out = zoom(dem, (zoom_y, zoom_x), order=3)  # bicubic
    return out


def write_heightmap_png(arr: np.ndarray, path: Path, elev_min: float, elev_max: float) -> None:
    """Normalise elevation to 16-bit grayscale PNG."""
    norm = ((arr - elev_min) / (elev_max - elev_min) * 65535).clip(0, 65535).astype(np.uint16)
    img = Image.fromarray(norm, mode="I;16")
    img.save(path, optimize=True)


def _read_full(src_path: Path, west: float, south: float, east: float, north: float) -> tuple[np.ndarray, dict]:
    """Read a wider DEM fully (no window) — for DEMs that already cover the AOI."""
    with rasterio.open(src_path) as src:
        dem = src.read(1).astype(np.float32)
        bounds = src.bounds
        transform = src.transform
        crs = src.crs
    # If the DEM bounds don't cover the full AOI, just use what's there
    if bounds.left > west or bounds.right < east or bounds.bottom > south or bounds.top < north:
        print(f"        ⚠ DEM bounds {bounds} don't cover full AOI")
    # Pad/clip to requested bounds
    from rasterio.windows import from_bounds
    win = from_bounds(west, south, east, north, transform)
    win = win.round_offsets()
    h, w = dem.shape
    win = win.intersection(rasterio.windows.Window(0, 0, w, h))
    if win.width <= 0 or win.height <= 0:
        return dem, _meta_for_arr(dem, transform, west, south, east, north)
    # Read via crop
    with rasterio.open(src_path) as src:
        cropped = src.read(1, window=win)
        new_transform = src.window_transform(win)
    # Pad with mean if needed
    target_w = int(round((east - west) / abs(new_transform.a)))
    target_h = int(round((north - south) / abs(new_transform.e)))
    if target_w > cropped.shape[1] or target_h > cropped.shape[0]:
        padded = np.full((target_h, target_w), float(np.nanmean(cropped)), dtype=np.float32)
        # Calculate offset
        x_off = max(int(round((new_transform.c - west) / abs(new_transform.a))), 0)
        y_off = max(int(round((north - new_transform.f) / abs(new_transform.e))), 0)
        y_end = min(y_off + cropped.shape[0], target_h)
        x_end = min(x_off + cropped.shape[1], target_w)
        padded[y_off:y_end, x_off:x_end] = cropped[:y_end - y_off, :x_end - x_off]
        cropped = padded
    meta = _meta_for_arr(cropped, transform, west, south, east, north)
    return cropped, meta


def _meta_for_arr(arr: np.ndarray, src_transform, west: float, south: float, east: float, north: float) -> dict:
    """Build metadata dict for an array covering the requested AOI."""
    res_x = (east - west) / arr.shape[1] if arr.shape[1] else abs(src_transform.a)
    res_y = (north - south) / arr.shape[0] if arr.shape[0] else abs(src_transform.e)
    return {
        "bounds_wgs84": [west, south, east, north],
        "transform": [res_x, 0, west, 0, -res_y, north],
        "shape": list(arr.shape),
        "pixel_resolution_deg": abs(res_x),
        "pixel_resolution_m_at_centroid": abs(res_x) * 111000 * math.cos(math.radians(CENTROID_LAT)),
    }


def gen_lod0() -> None:
    """0-500m: 1.5 m/pixel, 1024×1024 px, ~1.5 km × 1.5 km, parcel scale."""
    print("\n[LOD0] Parcel scale (0-500m)")
    print("        1.5 m/pixel, 1024×1024 pixels, 1.5 km × 1.5 km")

    half_extent_m = 750  # ±750 m = 1.5 km total → covers parcel + immediate buffer
    west, south, east, north = make_aoi_bbox(CENTROID_LON, CENTROID_LAT, half_extent_m)
    print(f"        AOI: W={west:.6f} S={south:.6f} E={east:.6f} N={north:.6f}")

    dem_native, meta = read_dem_cropped_to_aoi(west, south, east, north)
    print(f"        Native DEM shape: {dem_native.shape}, native res: {meta['pixel_resolution_m_at_centroid']:.1f} m/pixel")

    target_res_m = 1.5
    target_size = (1024, 1024)
    out = resample_to_target(dem_native, meta["pixel_resolution_m_at_centroid"], target_res_m, target_size)

    elev_min, elev_max = float(np.nanmin(out)), float(np.nanmax(out))
    print(f"        Upsampled shape: {out.shape}, target res: {target_res_m} m/pixel")
    print(f"        Elevation range: {elev_min:.1f} – {elev_max:.1f} m AMSL")

    out_path = OUT_DIR / "lod0_terrain.png"
    write_heightmap_png(out, out_path, elev_min, elev_max)
    size_kb = out_path.stat().st_size / 1024
    print(f"        ✓ Wrote {out_path.name} ({size_kb:.1f} KB)")

    meta_out = {
        **meta,
        "lod": 0,
        "view_radius_m": 500,
        "target_resolution_m_per_pixel": target_res_m,
        "target_size_pixels": list(target_size),
        "elevation_m": {"min": elev_min, "max": elev_max, "range": elev_max - elev_min},
        "output_png": str(out_path.relative_to(REPO)),
    }
    (OUT_DIR / "lod0_terrain.json").write_text(json.dumps(meta_out, indent=2))


def gen_lod1() -> None:
    """500m-5km: 15 m/pixel, 512×512 px, ~7.7 km × 7.7 km, Escobar scale."""
    print("\n[LOD1] Escobar scale (500m-5km)")
    print("        15 m/pixel, 512×512 pixels, 7.7 km × 7.7 km")

    half_extent_m = 3850  # ±3.85 km = 7.7 km total → covers Escobar + neighbours
    west, south, east, north = make_aoi_bbox(CENTROID_LON, CENTROID_LAT, half_extent_m)
    print(f"        AOI: W={west:.6f} S={south:.6f} E={east:.6f} N={north:.6f}")

    # Use the extended DEM (real 7.7 km × 7.7 km coverage from AWS terrain-rgb)
    LOD1_DEM = REPO / "docs" / "site_data" / "extended_aoi" / "dem" / "extended_dem_lod1.tif"
    if not LOD1_DEM.exists() or LOD1_DEM.stat().st_size < 1000:
        print(f"        ⚠ Extended LOD1 DEM not found at {LOD1_DEM} — run tools/lqv_fetch_extended_dem.py first")
        print(f"        Falling back to ALOS DEM (limited coverage)")
        LOD1_DEM = DEM_PATH

    if LOD1_DEM == DEM_PATH:
        dem, meta = read_dem_cropped_to_aoi(west, south, east, north)
    else:
        dem, meta = _read_full(LOD1_DEM, west, south, east, north)
    print(f"        Source DEM: {LOD1_DEM.name}")
    print(f"        Source DEM shape: {dem.shape}, native res: {meta['pixel_resolution_m_at_centroid']:.1f} m/pixel")

    target_res_m = 15
    target_size = (512, 512)
    out = resample_to_target(dem.astype(np.float32), meta["pixel_resolution_m_at_centroid"], target_res_m, target_size)

    elev_min, elev_max = float(np.nanmin(out)), float(np.nanmax(out))
    print(f"        Resampled shape: {out.shape}, target res: {target_res_m} m/pixel")
    print(f"        Elevation range: {elev_min:.1f} – {elev_max:.1f} m AMSL")

    out_path = OUT_DIR / "lod1_terrain.png"
    write_heightmap_png(out, out_path, elev_min, elev_max)
    size_kb = out_path.stat().st_size / 1024
    print(f"        ✓ Wrote {out_path.name} ({size_kb:.1f} KB)")

    meta_out = {
        **meta,
        "lod": 1,
        "view_radius_m": 5000,
        "target_resolution_m_per_pixel": target_res_m,
        "target_size_pixels": list(target_size),
        "elevation_m": {"min": elev_min, "max": elev_max, "range": elev_max - elev_min},
        "output_png": str(out_path.relative_to(REPO)),
    }
    (OUT_DIR / "lod1_terrain.json").write_text(json.dumps(meta_out, indent=2))


def gen_lod2() -> None:
    """5-30 km: 60 m/pixel, 384×384 px, ~23 km × 23 km, regional scale."""
    print("\n[LOD2] Regional scale (5-30 km)")
    print("        60 m/pixel, 384×384 pixels, 23 km × 23 km")

    half_extent_m = 11500  # ±11.5 km = 23 km total
    west, south, east, north = make_aoi_bbox(CENTROID_LON, CENTROID_LAT, half_extent_m)
    print(f"        AOI: W={west:.6f} S={south:.6f} E={east:.6f} N={north:.6f}")

    LOD2_DEM = REPO / "docs" / "site_data" / "extended_aoi" / "dem" / "extended_dem_lod2.tif"
    if not LOD2_DEM.exists() or LOD2_DEM.stat().st_size < 1000:
        print(f"        ⚠ Extended LOD2 DEM not found at {LOD2_DEM} — run tools/lqv_fetch_extended_dem.py first")
        print(f"        Falling back to ALOS DEM (very limited coverage)")
        LOD2_DEM = DEM_PATH

    dem, meta = _read_full(LOD2_DEM, west, south, east, north)
    print(f"        Source DEM: {LOD2_DEM.name}")

    res_x = (east - west) / dem.shape[1]
    res_y = (north - south) / dem.shape[0]
    meta = {
        "bounds_wgs84": [west, south, east, north],
        "transform": [res_x, 0, west, 0, -res_y, north],
        "shape": list(dem.shape),
        "pixel_resolution_deg": abs(res_x),
        "pixel_resolution_m_at_centroid": abs(res_x) * 111000 * math.cos(math.radians(CENTROID_LAT)),
    }
    print(f"        Source DEM shape: {dem.shape}, native res: {meta['pixel_resolution_m_at_centroid']:.1f} m/pixel")

    target_res_m = 60
    target_size = (384, 384)
    out = resample_to_target(dem.astype(np.float32), meta["pixel_resolution_m_at_centroid"], target_res_m, target_size)

    elev_min, elev_max = float(np.nanmin(out)), float(np.nanmax(out))
    print(f"        Resampled shape: {out.shape}, target res: {target_res_m} m/pixel")
    print(f"        Elevation range: {elev_min:.1f} – {elev_max:.1f} m AMSL")

    out_path = OUT_DIR / "lod2_terrain.png"
    write_heightmap_png(out, out_path, elev_min, elev_max)
    size_kb = out_path.stat().st_size / 1024
    print(f"        ✓ Wrote {out_path.name} ({size_kb:.1f} KB)")

    meta_out = {
        **meta,
        "lod": 2,
        "view_radius_m": 30000,
        "target_resolution_m_per_pixel": target_res_m,
        "target_size_pixels": list(target_size),
        "elevation_m": {"min": elev_min, "max": elev_max, "range": elev_max - elev_min},
        "output_png": str(out_path.relative_to(REPO)),
    }
    (OUT_DIR / "lod2_terrain.json").write_text(json.dumps(meta_out, indent=2))


def _read_with_padding(src_path: Path, west: float, south: float, east: float, north: float) -> tuple[np.ndarray, "rasterio.Affine"]:
    """Read DEM, pad with zeros if AOI extends beyond coverage."""
    from rasterio.windows import from_bounds
    with rasterio.open(src_path) as src:
        win = from_bounds(west, south, east, north, src.transform)
        win = win.round_offsets()
        full_win = rasterio.windows.Window(0, 0, src.width, src.height)
        clipped = win.intersection(full_win)
        if clipped.width <= 0 or clipped.height <= 0:
            raise ValueError("AOI completely outside DEM coverage")
        dem = src.read(1, window=clipped)
        src_transform = src.window_transform(clipped)
        # Pad back to the AOI shape (west, south, east, north)
        res_x = (east - west) / max(dem.shape[1], 1)
        res_y = (north - south) / max(dem.shape[0], 1)
        target_w = int(round((east - west) / res_x)) if res_x else dem.shape[1]
        target_h = int(round((north - south) / res_y)) if res_y else dem.shape[0]
        if target_w > dem.shape[1] or target_h > dem.shape[0]:
            padded = np.zeros((target_h, target_w), dtype=dem.dtype)
            # Paste into top-left, offset by the clipped window position
            x_off = max(int(round((src_transform.c - west) / res_x)), 0)
            y_off = max(int(round((north - src_transform.f) / res_y)), 0)
            y_end = min(y_off + dem.shape[0], target_h)
            x_end = min(x_off + dem.shape[1], target_w)
            padded[y_off:y_end, x_off:x_end] = dem[:y_end - y_off, :x_end - x_off]
            dem = padded
    return dem, src_transform


def write_manifest() -> None:
    """Write a unified manifest of all 3 LODs for the CesiumJS viewer."""
    manifest = {
        "site_name": "La Quebrada Viva",
        "centroid_wgs84": [CENTROID_LON, CENTROID_LAT],
        "lods": []
    }
    for lod_id in [0, 1, 2]:
        json_path = OUT_DIR / f"lod{lod_id}_terrain.json"
        if json_path.exists():
            d = json.loads(json_path.read_text())
            manifest["lods"].append({
                "lod": lod_id,
                "view_radius_m": d["view_radius_m"],
                "elevation_m": d["elevation_m"],
                "resolution_m_per_pixel": d["target_resolution_m_per_pixel"],
                "size_pixels": d["target_size_pixels"],
                "bounds_wgs84": d["bounds_wgs84"],
                "png": d["output_png"],
            })
    out = OUT_DIR / "lods_manifest.json"
    out.write_text(json.dumps(manifest, indent=2))
    print(f"\n✓ Wrote {out.name}")


def main() -> None:
    print("=" * 60)
    print("LQV → 3-tier heightmap pipeline")
    print(f"DEM source: {DEM_PATH.name}")
    print(f"Output:     {OUT_DIR}")
    print("=" * 60)
    gen_lod0()
    gen_lod1()
    gen_lod2()
    write_manifest()
    print("\n" + "=" * 60)
    print("✓ Done. Use lods_manifest.json to drive the CesiumJS viewer.")
    print("=" * 60)


if __name__ == "__main__":
    main()