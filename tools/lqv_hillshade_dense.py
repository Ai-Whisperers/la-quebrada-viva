#!/usr/bin/env python3
"""
Generate a dense hillshade composite (hillshade + slopeshade + contour overlay)
at 2048x2048 over the LQV parcel. Vertical exaggeration of 500× makes the
57m of relief visible in dense texture.

Output: docs/game_assets/heightmaps/lqv_hillshade_dense.png + .bounds.json
"""
from __future__ import annotations
import math, json, sys
from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject
from PIL import Image, ImageDraw, ImageFilter

REPO = Path("/root/la-quebrada-viva")
DEM = REPO / "docs/site_data/extended_aoi/dem/alos_aw3d30_dem.tif"
OUT = REPO / "docs/game_assets/heightmaps"
LITE = REPO / "splats/exports/web/game_assets_lite/assets/heightmaps"
OUT.mkdir(parents=True, exist_ok=True); LITE.mkdir(parents=True, exist_ok=True)

CENTROID_LON, CENTROID_LAT = -57.030, -25.630
HALF_EXTENT_M = 750  # 1.5 km square — full parcel

def meters_to_deg(m, lat):
    return m / (111000 * math.cos(math.radians(lat)))

def main():
    west = CENTROID_LON - meters_to_deg(HALF_EXTENT_M, CENTROID_LAT)
    east = CENTROID_LON + meters_to_deg(HALF_EXTENT_M, CENTROID_LAT)
    south = CENTROID_LAT - meters_to_deg(HALF_EXTENT_M, CENTROID_LAT)
    north = CENTROID_LAT + meters_to_deg(HALF_EXTENT_M, CENTROID_LAT)

    # Read DEM
    with rasterio.open(DEM) as src:
        from rasterio.windows import from_bounds
        win = from_bounds(west, south, east, north, src.transform).round_offsets()
        dem_raw = src.read(1, window=win).astype(np.float32)
        src_tr = src.window_transform(win)

    # Replace nodata with mean
    nodata = (dem_raw == src.nodata) if src.nodata is not None else np.zeros_like(dem_raw, dtype=bool)
    dem_raw[nodata] = np.nan
    if np.isnan(dem_raw).any():
        # Fill NaN with elevation mean
        dem_raw[np.isnan(dem_raw)] = np.nanmean(dem_raw)

    # Up-sample to 2048x2048 via reproject/bilinear
    target_h = target_w = 2048
    dst = np.zeros((target_h, target_w), dtype=np.float32)
    reproject(
        source=dem_raw, destination=dst,
        src_transform=src_tr, dst_transform=rasterio.transform.from_bounds(west, south, east, north, target_w, target_h),
        src_crs=src.crs, dst_crs=src.crs,
        resampling=Resampling.bilinear,
    )
    dem = dst
    print(f"DEM upsampled to {dem.shape}, range {dem.min():.1f} – {dem.max():.1f} m")

    # Apply vertical exaggeration 500× for visual density
    emean = dem.mean()
    dem_exag = emean + (dem - emean) * 500.0  # 500x exaggeration

    # Generate hillshade (Horn's method) with multiple sun azimuths
    cell_m_x = (east - west) / 2048 * 111000 * math.cos(math.radians(CENTROID_LAT))
    cell_m_y = (north - south) / 2048 * 111000

    def horn(elev, sun_az, sun_alt):
        sun_az_rad = math.radians(sun_az)
        sun_z = math.sin(math.radians(sun_alt))
        cos_sun_z = math.cos(math.radians(sun_alt))
        # Gradients
        dzdx = np.zeros_like(elev)
        dzdy = np.zeros_like(elev)
        dzdx[1:-1, 1:-1] = ((elev[1:-1, 2:] - elev[1:-1, :-2]) / (2 * cell_m_x))
        dzdy[1:-1, 1:-1] = ((elev[:-2, 1:-1] - elev[2:, 1:-1]) / (2 * cell_m_y))
        slope = np.arctan(np.sqrt(dzdx**2 + dzdy**2))
        aspect = np.arctan2(dzdy, -dzdx)
        # Hillshade
        hs = (cos_sun_z * np.cos(slope) +
              sun_z * np.sin(slope) * np.cos(sun_az_rad - aspect))
        hs = np.clip(hs, 0, 1)
        return hs

    # 3 hillshades averaged for richer shading
    h1 = horn(dem_exag, 315, 45)  # NW
    h2 = horn(dem_exag, 225, 35)  # SW
    h3 = horn(dem_exag, 90, 60)   # East
    hs_rgb = np.stack([h1, (h1+h2)/2, h2], axis=-1)  # R=NW, G=mix, B=SW
    hs_img = (hs_rgb * 255).astype(np.uint8)

    # Add subtle contour lines (every 5m)
    contours_e = np.linspace(dem.min(), dem.max(), int((dem.max()-dem.min())/5)+1)
    img = Image.fromarray(hs_img)
    draw = ImageDraw.Draw(img)
    for e in contours_e[::2]:  # every other contour to avoid clutter
        mask = (np.abs(dem - e) < 0.4).astype(np.uint8) * 255
        cimg = Image.fromarray(mask)
        cimg = cimg.filter(ImageFilter.FIND_EDGES)
        # Convert non-zero mask to dark line
        arr = np.array(img).copy()
        cmask = np.array(cimg) > 100
        arr[cmask] = arr[cmask] * 0.55 + np.array([40, 30, 10]) * 0.45
        img = Image.fromarray(arr.astype(np.uint8))
        draw = ImageDraw.Draw(img)

    # Boost saturation/contrast (visual punch)
    from PIL import ImageEnhance
    img = ImageEnhance.Contrast(img).enhance(1.4)
    img = ImageEnhance.Color(img).enhance(1.3)

    out_png = OUT / "lqv_hillshade_dense.png"
    img.save(out_png, optimize=True)
    print(f"wrote {out_png} {img.size} {out_png.stat().st_size/1024/1024:.1f}MB")

    bp = OUT / "lqv_hillshade_dense_bounds.json"
    bp.write_text(json.dumps({
        "west": west, "south": south, "east": east, "north": north,
        "width": img.size[0], "height": img.size[1],
        "source": "ALOS AW3D30 + 500x v.exag + 3-azimuth horn hillshade + 5m contours",
    }, indent=2))

    import shutil
    shutil.copy(out_png, LITE / "lqv_hillshade_dense.png")
    shutil.copy(bp, LITE / "lqv_hillshade_dense_bounds.json")
    print(f"copied to {LITE}")

if __name__ == "__main__":
    main()
