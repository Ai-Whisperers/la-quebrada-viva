#!/usr/bin/env python3
"""Multi-azimuth hillshades from ALOS AW3D30 DEM."""
import argparse, math, os, subprocess, sys
import numpy as np
import rasterio as rio

BASE = os.path.dirname(os.path.abspath(__file__))
DEM  = os.path.join(BASE, "docs/site_data/alos_aw3d30_dem.tif")
OUT  = os.path.join(BASE, "docs/site_data/analysis")
AZIMUTHS = [315, 45, 135, 225]
ALTITUDE = 35

def hillshade_numpy(dem, azimuth, altitude_deg):
    """Compute hillshade using numpy gradient (gdaldem fallback)."""
    deg2rad = math.pi / 180.0
    az_rad  = azimuth * deg2rad
    alt_rad = altitude_deg * deg2rad
    z_factor = 1.0
    dx, dy = np.gradient(dem)
    slope   = np.arctan(z_factor * np.sqrt(dx*dx + dy*dy))
    aspect  = np.arctan2(-dx, dy)
    hs = np.sin(alt_rad) * np.cos(slope) + \
         np.cos(alt_rad) * np.sin(slope) * np.cos(az_rad - aspect)
    return np.clip(hs, 0, 1)

def write_8bit(filename, hs):
    arr8 = (hs * 255).astype(np.uint8)
    import matplotlib.image
    matplotlib.image.imsave(filename, arr8, cmap="gray")
    print(f"  Wrote {filename}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force",action="store_true")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    out_files = [os.path.join(OUT, f"alos_hillshade_{az}.png") for az in AZIMUTHS]

    if all(os.path.exists(f) for f in out_files) and not args.force:
        print("All hillshades exist. Use --force to overwrite.")
    else:
        print(f"Reading {DEM}...")
        with rio.open(DEM) as src:
            dem = src.read(1).astype(np.float32)
            nodata = src.nodata
        dem[dem == nodata] = np.nan
        for az in AZIMUTHS:
            hs = hillshade_numpy(dem, az, ALTITUDE)
            out = os.path.join(OUT, f"alos_hillshade_{az}.png")
            write_8bit(out, hs)

    # 2x2 composite grid
    grid_path = os.path.join(OUT, "alos_hillshade_composite.png")
    if os.path.exists(grid_path) and not args.force:
        print(f"Composite exists. Use --force to overwrite.")
        return

    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    labels = [f"Azimuth {az}" for az in AZIMUTHS]
    for ax, az, lbl in zip(axes.flat, AZIMUTHS, labels):
        with rio.open(os.path.join(OUT, f"alos_hillshade_{az}.png")) as src:
            arr = src.read(1)
        ax.imshow(arr, cmap="gray")
        ax.set_title(lbl); ax.axis("off")
    fig.suptitle("ALOS AW3D30 Multi-Azimuth Hillshades (35 alt)", fontsize=14)
    fig.savefig(grid_path, dpi=120, bbox_inches="tight")
    print(f"  Wrote {grid_path}")

if __name__=="__main__": main()
