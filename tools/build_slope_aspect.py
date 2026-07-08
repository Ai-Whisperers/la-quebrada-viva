#!/usr/bin/env python3
"""Build slope, aspect, and multi-directional hillshade rasters for the 10km box.

Source: /root/.hermes/lqv-splat/exports/web/data/elevation_grid.json
  - 108 x 180 cells, ~206m x 112m cell size
  - Bounds: [-57.13, -25.698, -56.931, -25.518]
  - Elevation range: 116-391 m

Output (to /root/.hermes/lqv-splat/exports/web/data/):
  - slope_10km.jpg + slope_10km.png + slope_10km_bounds.json
  - aspect_10km.jpg + aspect_10km.png + aspect_10km_bounds.json
  - multi_hillshade_10km.jpg + multi_hillshade_10km.png + multi_hillshade_10km_bounds.json
"""
import json, math, os
import numpy as np
from PIL import Image

GRID = "/root/.hermes/lqv-splat/exports/web/data/elevation_grid.json"
OUT  = "/root/.hermes/lqv-splat/exports/web/data"

g = json.loads(open(GRID).read())
W, H = g["width"], g["height"]
b = g["bounds"]
dem = np.array(g["dem"], dtype=np.float32)
print(f"DEM: {W}x{H} bounds={b} elev range: {dem.min():.0f}-{dem.max():.0f}m")

# Cell size in metres
lat0 = (b[1] + b[3]) / 2
dx_m = (b[2] - b[0]) / (W - 1) * 111320 * math.cos(math.radians(lat0))
dy_m = (b[3] - b[1]) / (H - 1) * 110540
print(f"  cell size: {dx_m:.0f}m x {dy_m:.0f}m")

# Mask NaN
dem_nan = np.where(dem == -9999, np.nan, dem)
if not np.any(np.isnan(dem_nan)):
    dem_nan = dem.copy()

# ---- Slope (Horn) ----
def slope_aspect_horn(z, dx, dy):
    """Returns slope_deg, aspect_deg (0=N, 90=E, 180=S, 270=W)."""
    z1 = np.roll(z,  1, 0); z1[0, :]  = np.nan
    z2 = np.roll(z, -1, 0); z2[-1, :] = np.nan
    z3 = np.roll(z,  1, 1); z3[:, 0]  = np.nan
    z4 = np.roll(z, -1, 1); z4[:, -1] = np.nan
    z5 = np.roll(np.roll(z, 1, 0), 1, 1); z5[0, :]=np.nan; z5[:, 0]=np.nan
    z6 = np.roll(np.roll(z, 1, 0),-1, 1); z6[0, :]=np.nan; z6[:, -1]=np.nan
    z7 = np.roll(np.roll(z,-1, 0), 1, 1); z7[-1, :]=np.nan; z7[:, 0]=np.nan
    z8 = np.roll(np.roll(z,-1, 0),-1, 1); z8[-1, :]=np.nan; z8[:, -1]=np.nan

    dz_dx = ((z3 + 2*z4 + z5) - (z6 + 2*z8 + z7)) / (8 * dx)
    dz_dy = ((z5 + 2*z1 + z6) - (z7 + 2*z2 + z8)) / (8 * dy)
    slope_rad = np.arctan(np.hypot(dz_dx, dz_dy))
    aspect_rad = np.arctan2(dz_dy, -dz_dx)  # 0=N, 90=E
    return np.degrees(slope_rad), (np.degrees(aspect_rad) + 360) % 360

slope, aspect = slope_aspect_horn(dem_nan, dx_m, dy_m)
print(f"slope: {np.nanmin(slope):.1f}-{np.nanmax(slope):.1f}° (median {np.nanmedian(slope):.1f}°)")
print(f"aspect: {np.nanmin(aspect):.0f}-{np.nanmax(aspect):.0f}°")

# ---- Hillshade (multi-direction) ----
def hillshade(z, dx, dy, az_deg, alt_deg=45):
    az = math.radians(360 - az_deg + 90)
    alt = math.radians(alt_deg)
    z1 = np.roll(z,  1, 0); z1[0, :]  = np.nan
    z2 = np.roll(z, -1, 0); z2[-1, :] = np.nan
    z3 = np.roll(z,  1, 1); z3[:, 0]  = np.nan
    z4 = np.roll(z, -1, 1); z4[:, -1] = np.nan
    z5 = np.roll(np.roll(z, 1, 0), 1, 1); z5[0, :]=np.nan; z5[:, 0]=np.nan
    z6 = np.roll(np.roll(z, 1, 0),-1, 1); z6[0, :]=np.nan; z6[:, -1]=np.nan
    z7 = np.roll(np.roll(z,-1, 0), 1, 1); z7[-1, :]=np.nan; z7[:, 0]=np.nan
    z8 = np.roll(np.roll(z,-1, 0),-1, 1); z8[-1, :]=np.nan; z8[:, -1]=np.nan
    dz_dx = ((z3 + 2*z4 + z5) - (z6 + 2*z8 + z7)) / (8 * dx)
    dz_dy = ((z5 + 2*z1 + z6) - (z7 + 2*z2 + z8)) / (8 * dy)
    sl = np.arctan(np.hypot(dz_dx, dz_dy))
    asp = np.arctan2(dz_dy, -dz_dx)
    return np.cos(alt)*np.cos(sl) + np.sin(alt)*np.sin(sl)*np.cos(az - asp)

# Mark's multi-directional hillshade (315, 45, 90, 180)
hs_315 = hillshade(dem_nan, dx_m, dy_m, 315, 45)
hs_45  = hillshade(dem_nan, dx_m, dy_m,  45, 45)
hs_90  = hillshade(dem_nan, dx_m, dy_m,  90, 60)
hs_180 = hillshade(dem_nan, dx_m, dy_m, 180, 60)
multi = 0.40 * hs_315 + 0.30 * hs_45 + 0.15 * hs_90 + 0.15 * hs_180

# ---- Save helpers ----
def save_raster(arr, name, colormap="auto"):
    """Save as JPG + PNG. Flip vertically (raster rows top-down → image bottom-up)."""
    a = arr.copy()
    # Fill NaN with neutral (mid-grey or 0)
    nan_mask = np.isnan(a)
    if colormap == "slope":
        # Slope: green→yellow→red
        s = np.clip(np.where(nan_mask, 0, a), 0, 60)
        rc = np.where(s < 15, 100 + (s/15)*155, np.where(s < 30, 255, np.where(s < 45, 255 - (s-30)*5, 150)))
        gc = np.where(s < 15, 180 - (s/15)*30, np.where(s < 30, 180 - (s-15)*4, 150))
        bc = np.where(s < 15, 100 - (s/15)*70, np.where(s < 30, 70 - (s-15)*2, 50))
        rgb = np.stack([rc, gc, bc], axis=-1).astype(np.uint8)
        rgb[nan_mask] = [240, 240, 240]
    elif colormap == "aspect":
        # Aspect: HSV color wheel
        from matplotlib.colors import hsv_to_rgb
        hue = (a % 360) / 360.0
        sat = np.where(nan_mask, 0, 0.7)
        val = np.where(nan_mask, 0, 0.85)
        hsv = np.stack([hue, sat, val], axis=-1)
        rgb = (hsv_to_rgb(hsv) * 255).astype(np.uint8)
        rgb[nan_mask] = [240, 240, 240]
    elif colormap == "hillshade":
        # Stretch to 0-255
        p_lo, p_hi = np.nanpercentile(a, [2, 98])
        s = np.clip((a - p_lo) / (p_hi - p_lo) * 255, 0, 255).astype(np.uint8)
        rgb = np.stack([s, s, s], axis=-1)
        rgb[nan_mask] = [240, 240, 240]
    else:
        # Greyscale
        p_lo, p_hi = np.nanpercentile(a, [2, 98])
        s = np.clip((a - p_lo) / (p_hi - p_lo) * 255, 0, 255).astype(np.uint8)
        rgb = np.stack([s, s, s], axis=-1)
        rgb[nan_mask] = [240, 240, 240]
    rgb = np.flipud(rgb)  # raster top→image bottom
    Image.fromarray(rgb).save(f"{OUT}/{name}.jpg", quality=82)
    Image.fromarray(rgb).save(f"{OUT}/{name}.png", optimize=True)
    # Bounds JSON
    bounds_info = {
        "type": "bounds",
        "bbox": list(map(float, b)),
        "width_px": int(W),
        "height_px": int(H),
        "source": "elevation_grid.json (Copernicus GLO-30 DEM, downsampled to 30\" grid)",
        "method": colormap,
        "cell_size_m": [round(float(dx_m), 1), round(float(dy_m), 1)],
        "elevation_range_m": [round(float(np.nanmin(dem_nan)), 1), round(float(np.nanmax(dem_nan)), 1)],
    }
    with open(f"{OUT}/{name}_bounds.json", "w") as f:
        json.dump(bounds_info, f, indent=2)
    print(f"  wrote {name}.jpg/.png + bounds ({os.path.getsize(f'{OUT}/{name}.jpg')} b)")

save_raster(slope, "slope_10km", colormap="slope")
save_raster(aspect, "aspect_10km", colormap="aspect")
save_raster(multi, "multi_hillshade_10km", colormap="hillshade")

print("\nDone.")
