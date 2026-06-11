"""DEM-derived site analysis: slope, aspect, buildability, contours, viewsheds.

Inputs (already in docs/site_data/):
  - alos_aw3d30_dem.tif    (preferred — JAXA, 30 m)
  - cop30_dem.tif         (Copernicus GLO-30, cross-check)
  - srtm_gl1_dem.tif      (SRTM v3 GL1, cross-check)
  - nasadem_dem.tif       (NASADEM, cross-check)

Outputs (in docs/site_data/analysis/):
  - alos_slope.tif / .png          (degrees)
  - alos_aspect.tif / .png         (compass)
  - alos_buildability.tif / .png   (4-class: 0–8% / 8–15% / 15–30% / >30%)
  - alos_contours.geojson          (10 m elevation contours)
  - analysis_summary.txt            (numbers)
  - site_diagnostic.md              (markdown interpretation)
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.transform import rowcol
from dotenv import load_dotenv

HERE = Path(__file__).parent.parent
load_dotenv(dotenv_path=HERE / ".env.local")
SRC_TIF = HERE / "docs" / "site_data" / "alos_aw3d30_dem.tif"
OUT_DIR = HERE / "docs" / "site_data" / "analysis"
OUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("DEM analysis — Escobar / Mbopicuá site diagnostic")
print("=" * 70)

with rasterio.open(SRC_TIF) as src:
    arr = src.read(1).astype(float)
    nodata = src.nodata
    if nodata is not None:
        arr = np.where(arr == nodata, np.nan, arr)
    transform = src.transform
    bounds = src.bounds
    res_x, res_y = src.res
    crs = src.crs
    lat_res = res_x  # in degrees (EPSG:4326)
    lon_res = res_y
    # At lat -25.6, 1° lat ≈ 110.6 km, 1° lon ≈ 99.7 km
    M_PER_DEG_LAT = 110_574.0
    M_PER_DEG_LON = 111_320.0 * np.cos(np.deg2rad(-25.6))
    res_x_m = lon_res * M_PER_DEG_LON
    res_y_m = lat_res * M_PER_DEG_LAT

print(f"DEM: {SRC_TIF.name}  ({arr.shape[0]} × {arr.shape[1]} pixels, {res_x_m:.0f} × {res_y_m:.0f} m per pixel)")
print(f"Bounds: W={bounds.left:.4f}  E={bounds.right:.4f}  S={bounds.bottom:.4f}  N={bounds.top:.4f}")
print(f"Elevation range: {np.nanmin(arr):.1f} – {np.nanmax(arr):.1f} m AMSL  (range {np.nanmax(arr) - np.nanmin(arr):.1f} m)")
print(f"Mean: {np.nanmean(arr):.1f} m  Median: {np.nanmedian(arr):.1f} m  Std: {np.nanstd(arr):.1f} m")

# 1) Slope (degrees and percent)
print("\n[1/5] Computing slope…")
gy, gx = np.gradient(arr, res_y_m, res_x_m)
slope_rad = np.arctan(np.sqrt(gx * gx + gy * gy))
slope_deg = np.degrees(slope_rad)
slope_pct = np.tan(slope_rad) * 100.0

with rasterio.open(
    OUT_DIR / "alos_slope.tif", "w", driver="GTiff",
    height=arr.shape[0], width=arr.shape[1], count=1,
    dtype="float32", crs=crs, transform=transform, nodata=np.nan,
) as dst:
    dst.write(slope_deg.astype(np.float32), 1)

# 2) Aspect (compass degrees, 0 = N, clockwise)
print("[2/5] Computing aspect…")
aspect_rad = np.arctan2(-gx, gy)  # standard convention
aspect_deg = (np.degrees(aspect_rad) + 360.0) % 360.0

with rasterio.open(
    OUT_DIR / "alos_aspect.tif", "w", driver="GTiff",
    height=arr.shape[0], width=arr.shape[1], count=1,
    dtype="float32", crs=crs, transform=transform, nodata=np.nan,
) as dst:
    dst.write(aspect_deg.astype(np.float32), 1)

# 3) Buildability (4 classes)
print("[3/5] Classifying buildability…")
def buildability(sl):
    if np.isnan(sl):
        return 0
    if sl < 8:    return 1  # easily buildable (flat)
    if sl < 15:   return 2  # buildable with care
    if sl < 30:   return 3  # challenging, terracing needed
    return 4  # avoid for buildings, OK for trails/views
bld = np.vectorize(buildability)(slope_pct)
# Recompute by percent slope (more standard for civil engineering)
bld = np.full_like(slope_pct, 0, dtype=np.int8)
bld[(slope_pct < 8) & ~np.isnan(slope_pct)] = 1
bld[(slope_pct >= 8) & (slope_pct < 15) & ~np.isnan(slope_pct)] = 2
bld[(slope_pct >= 15) & (slope_pct < 30) & ~np.isnan(slope_pct)] = 3
bld[(slope_pct >= 30) & ~np.isnan(slope_pct)] = 4

with rasterio.open(
    OUT_DIR / "alos_buildability.tif", "w", driver="GTiff",
    height=arr.shape[0], width=arr.shape[1], count=1,
    dtype="int8", crs=crs, transform=transform, nodata=0,
) as dst:
    dst.write(bld, 1)

# Stats per class
class_names = {0: "nodata", 1: "flat (0-8%)", 2: "buildable (8-15%)", 3: "challenging (15-30%)", 4: "steep (>30%)"}
print("\nBuildability breakdown (pixel count and area):")
total_pixels = (~np.isnan(arr)).sum()
for c in [1, 2, 3, 4]:
    n = (bld == c).sum()
    pct = 100 * n / total_pixels
    area_ha = n * res_x_m * res_y_m / 10_000
    print(f"  class {c} ({class_names[c]}): {n:6d} px  {pct:5.1f}%  ≈ {area_ha:6.1f} ha")

# 4) Hillshade (re-render with class overlay)
print("\n[4/5] Generating visualizations…")
az, alt = 315.0, 45.0
az_r, alt_r = np.deg2rad(90.0 - az), np.deg2rad(alt)
shaded = (np.sin(alt_r) * np.sin(slope_rad) +
          np.cos(alt_r) * np.cos(slope_rad) * np.cos(az_r - aspect_rad))
shaded = np.clip(np.where(np.isnan(shaded), 0, shaded), 0, 1)

# Slope + hillshade overlay
fig, axes = plt.subplots(1, 2, figsize=(18, 9), dpi=110)
extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

im0 = axes[0].imshow(slope_pct, cmap="RdYlGn_r", vmin=0, vmax=60,
                      extent=extent, origin="upper")
axes[0].set_title(f"Slope (%)\nmean {np.nanmean(slope_pct):.1f}%, max {np.nanmax(slope_pct):.0f}%")
axes[0].set_xlabel("Longitude"); axes[0].set_ylabel("Latitude")
plt.colorbar(im0, ax=axes[0], label="slope (%)")

# Buildability map
class_cmap = matplotlib.colors.ListedColormap(["#cccccc", "#2ca02c", "#a1d99b", "#fd8d3c", "#de2d26"])
bounds_c = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
norm = matplotlib.colors.BoundaryNorm(bounds_c, class_cmap.N)
im1 = axes[1].imshow(bld, cmap=class_cmap, norm=norm, extent=extent, origin="upper")
axes[1].set_title("Buildability by slope class")
axes[1].set_xlabel("Longitude"); axes[1].set_ylabel("Latitude")
cbar = plt.colorbar(im1, ax=axes[1], ticks=[0, 1, 2, 3, 4])
cbar.ax.set_yticklabels([class_names[i] for i in range(5)])

plt.tight_layout()
plt.savefig(OUT_DIR / "slope_and_buildability.png", dpi=110, bbox_inches="tight")
plt.close()
print(f"      wrote slope_and_buildability.png")

# Composite: hillshade + buildability + contours
fig, ax = plt.subplots(figsize=(12, 12), dpi=120)
ax.imshow(shaded, cmap="gray", extent=extent, origin="upper", alpha=0.6)
im2 = ax.imshow(bld, cmap=class_cmap, norm=norm, extent=extent, origin="upper", alpha=0.5)
# 10m contours
contour_levels = np.arange(np.floor(np.nanmin(arr) / 10) * 10,
                            np.ceil(np.nanmax(arr) / 10) * 10 + 1, 10)
xs = np.linspace(bounds.left, bounds.right, arr.shape[1])
ys = np.linspace(bounds.top, bounds.bottom, arr.shape[0])
cs = ax.contour(xs, ys, arr, levels=contour_levels, colors="red", linewidths=0.4, alpha=0.5)
ax.clabel(cs, fmt="%d", fontsize=6, colors="red")
ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
ax.set_title("Site diagnostic — hillshade + slope/buildability + 10m contours\n"
             f"Escobar / Mbopicuá, Paraguarí, PY  |  {bounds.left:.3f}°W – {bounds.right:.3f}°E, "
             f"{bounds.bottom:.3f}°S – {bounds.top:.3f}°N")
cbar = plt.colorbar(im2, ax=ax, ticks=[0, 1, 2, 3, 4], fraction=0.046, pad=0.04)
cbar.ax.set_yticklabels([class_names[i] for i in range(5)])
plt.tight_layout()
plt.savefig(OUT_DIR / "site_diagnostic.png", dpi=120, bbox_inches="tight")
plt.close()
print(f"      wrote site_diagnostic.png")

# 5) Elevation-by-class stats
print("\n[5/5] Per-class elevation stats…")
class_stats = {}
for c in [1, 2, 3, 4]:
    mask = bld == c
    if mask.sum() == 0:
        continue
    class_stats[class_names[c]] = {
        "pixels": int(mask.sum()),
        "area_ha": float(mask.sum() * res_x_m * res_y_m / 10_000),
        "elev_min_m": float(np.nanmin(arr[mask])),
        "elev_max_m": float(np.nanmax(arr[mask])),
        "elev_mean_m": float(np.nanmean(arr[mask])),
        "elev_p10_m": float(np.nanpercentile(arr[mask], 10)),
        "elev_p90_m": float(np.nanpercentile(arr[mask], 90)),
    }
    print(f"  {class_names[c]}: {class_stats[class_names[c]]}")

# Write summary
with open(OUT_DIR / "analysis_summary.txt", "w") as f:
    f.write(f"DEM analysis — {datetime.utcnow().isoformat()}Z\n")
    f.write(f"Source: {SRC_TIF.name}\n")
    f.write(f"Bounds: W={bounds.left:.4f}  E={bounds.right:.4f}  S={bounds.bottom:.4f}  N={bounds.top:.4f}\n")
    f.write(f"Pixel: {res_x_m:.0f} × {res_y_m:.0f} m  ({arr.shape[1]} × {arr.shape[0]} px)\n")
    f.write(f"Total valid pixels: {total_pixels}\n\n")
    f.write(f"Elevation: {np.nanmin(arr):.1f} – {np.nanmax(arr):.1f} m AMSL  "
            f"(range {np.nanmax(arr) - np.nanmin(arr):.1f} m)\n")
    f.write(f"Mean: {np.nanmean(arr):.1f} m  Median: {np.nanmedian(arr):.1f} m  Std: {np.nanstd(arr):.1f} m\n\n")
    f.write("Buildability (by slope class):\n")
    f.write(f"  flat (0-8%):     {class_stats.get('flat (0-8%)', {}).get('area_ha', 0):.1f} ha\n")
    f.write(f"  buildable (8-15%): {class_stats.get('buildable (8-15%)', {}).get('area_ha', 0):.1f} ha\n")
    f.write(f"  challenging (15-30%): {class_stats.get('challenging (15-30%)', {}).get('area_ha', 0):.1f} ha\n")
    f.write(f"  steep (>30%):    {class_stats.get('steep (>30%)', {}).get('area_ha', 0):.1f} ha\n\n")
    f.write("Per-class elevation:\n")
    for name, s in class_stats.items():
        f.write(f"  {name}: elev {s['elev_min_m']:.0f}–{s['elev_max_m']:.0f} m "
                f"(mean {s['elev_mean_m']:.0f} m, p10 {s['elev_p10_m']:.0f}, p90 {s['elev_p90_m']:.0f})\n")

print(f"\nSummary: {OUT_DIR / 'analysis_summary.txt'}")
print("DONE.")
