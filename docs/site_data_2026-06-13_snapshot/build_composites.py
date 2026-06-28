"""Build the final composites for Blender (S2 is in UTM 21J)."""
import os, numpy as np
import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pyproj import Transformer
from PIL import Image
from AOI import BBOX

W, S, E, N = BBOX
# AOI in UTM 21J
t = Transformer.from_crs("EPSG:4326", "EPSG:32721", always_xy=True)
W_e, S_n = t.transform(W, S)
E_e, N_n = t.transform(E, N)
print(f"AOI in UTM 21J: E [{W_e:.1f}, {E_e:.1f}]  N [{S_n:.1f}, {N_n:.1f}]")

def clip_utm(ds_path, W_e, S_n, E_e, N_n):
    with rasterio.open(ds_path) as ds:
        win = from_bounds(W_e, S_n, E_e, N_n, ds.transform)
        win = win.intersection(rasterio.windows.Window(0, 0, ds.width, ds.height))
        arr = ds.read(1, window=win)
        transform = ds.window_transform(win)
        return arr, transform, ds.crs

print("\nLoading + clipping S2 bands to AOI (UTM 21J)...")
s2 = {}
for b in ["B02", "B03", "B04", "B08", "SCL"]:
    arr, t, crs = clip_utm(f"sentinel2/{b}.tif", W_e, S_n, E_e, N_n)
    s2[b] = arr
    print(f"  {b}: {arr.shape}  res={ds if False else 10}m  range {arr.min()}..{arr.max()}")

B04, B03, B02, nir, scl = s2["B04"], s2["B03"], s2["B02"], s2["B08"], s2["SCL"]
src_transform = t  # for UTM output

# === RGB true-color ===
def stretch(a, p_lo=2, p_hi=98):
    a = a.astype(np.float32)
    valid = a[a > 0]
    if valid.size == 0:
        return np.zeros_like(a, dtype=np.uint8)
    lo, hi = np.percentile(valid, (p_lo, p_hi))
    return np.clip((a - lo) / (hi - lo + 1e-6) * 255, 0, 255).astype(np.uint8)

rgb = np.stack([stretch(B04), stretch(B03), stretch(B02)], axis=-1)
nir_rgb = np.stack([stretch(nir), stretch(B04), stretch(B03)], axis=-1)

# NDVI
ndvi = (nir.astype(np.float32) - B04.astype(np.float32)) / (nir.astype(np.float32) + B04.astype(np.float32) + 1e-6)
ndvi_stretched = np.clip((ndvi + 1) * 127.5, 0, 255).astype(np.uint8)

os.makedirs("analysis", exist_ok=True)
Image.fromarray(rgb).save("analysis/rgb_truecolor_10m.png", optimize=True)
Image.fromarray(nir_rgb).save("analysis/nir_falsecolor_10m.png", optimize=True)
Image.fromarray(ndvi_stretched).save("analysis/ndvi_10m.png", optimize=True)
print(f"\nPNGs written:")
for f in ["rgb_truecolor_10m.png", "nir_falsecolor_10m.png", "ndvi_10m.png"]:
    sz = os.path.getsize(f"analysis/{f}") // 1024
    print(f"  {f}: {sz} KB")

# === Save RGB as GeoTIFF (UTM 21J, 10m) for Blender GIS import ===
print("\nWriting RGB GeoTIFF (UTM 21J, 10m) for Blender GIS...")
profile = {"driver": "GTiff", "height": rgb.shape[0], "width": rgb.shape[1], "count": 3,
           "dtype": "uint8", "crs": "EPSG:32721", "transform": src_transform,
           "compress": "lzw", "tiled": True}
with rasterio.open("analysis/rgb_truecolor_utm21j.tif", "w", **profile) as dst:
    dst.write(np.transpose(rgb, (2, 0, 1)))
print(f"  -> analysis/rgb_truecolor_utm21j.tif  {os.path.getsize('analysis/rgb_truecolor_utm21j.tif')//1024} KB")

# === Hillshade from 10m DEM ===
print("\nBuilding hillshades from 10m DEM...")
with rasterio.open("dem/terrarium_monday_10m_utm21j.tif") as ds:
    elev = ds.read(1).astype(np.float32)
    transform = ds.transform
    bounds = ds.bounds
    print(f"  DEM: {elev.shape}  res={ds.res[0]:.1f}m  range {elev.min():.1f}..{elev.max():.1f}m")

def hillshade(elev, transform, azimuth=315, altitude=45):
    az = np.radians(90 - azimuth)
    alt = np.radians(altitude)
    xres = abs(transform.a); yres = abs(transform.e)
    e = elev.astype(np.float32)
    e_p = np.pad(e, 1, mode="edge")
    dz_dx = ((e_p[0:-2,2:] + 2*e_p[1:-1,2:] + e_p[2:,2:]) - (e_p[0:-2,0:-2] + 2*e_p[1:-1,0:-2] + e_p[2:,0:-2])) / (8*xres)
    dz_dy = ((e_p[2:,0:-2] + 2*e_p[2:,1:-1] + e_p[2:,2:]) - (e_p[0:-2,0:-2] + 2*e_p[0:-2,1:-1] + e_p[0:-2,2:])) / (8*yres)
    slope = np.arctan(np.hypot(dz_dx, dz_dy))
    aspect = np.arctan2(dz_dy, -dz_dx)
    return np.clip(np.sin(alt)*np.cos(slope) + np.cos(alt)*np.sin(slope)*np.cos(az-aspect), 0, 1)

# find center cell
cx_pix = int((transform.c - W_e) / -transform.a)  # column of the cascade center
cy_pix = int((transform.f - N_n) / -transform.e)  # row of the cascade center
print(f"  Cascade center pixel: col={cx_pix}  row={cy_pix}")
for label, az in [("az315_sunNW", 315), ("az045_sunNE", 45), ("az180_sunS", 180), ("az225_sunSW", 225), ("az090_sunE_low45", 90)]:
    hs = hillshade(elev, transform, azimuth=az, altitude=35)
    Image.fromarray((hs * 255).astype(np.uint8)).save(f"analysis/hillshade_10m_{label}.png", optimize=True)
    print(f"  hillshade_{label}: {os.path.getsize(f'analysis/hillshade_10m_{label}.png')//1024} KB")

# slope
dz_dx = np.gradient(elev, axis=1) / abs(transform.a)
dz_dy = np.gradient(elev, axis=0) / abs(transform.e)
slope = np.degrees(np.arctan(np.hypot(dz_dx, dz_dy)))
slope_p = np.clip(slope / 60.0 * 255, 0, 255).astype(np.uint8)
Image.fromarray(slope_p).save("analysis/slope_10m.png", optimize=True)

# heightmap vis
elev_norm = np.clip((elev - elev.min()) / (elev.max() - elev.min() + 1e-6) * 255, 0, 255).astype(np.uint8)
Image.fromarray(elev_norm).save("analysis/heightmap_10m.png", optimize=True)

# waterfall-region stats
# 40m radius around cascade = 4 pixels at 10m
y_lo, y_hi = max(0, cy_pix-10), min(elev.shape[0], cy_pix+10)
x_lo, x_hi = max(0, cx_pix-10), min(elev.shape[1], cx_pix+10)
region_elev = elev[y_lo:y_hi, x_lo:x_hi]
region_slope = slope[y_lo:y_hi, x_lo:x_hi]
print(f"\n  Waterfall region (40m×40m):")
print(f"    elev: {region_elev.min():.1f} – {region_elev.max():.1f} m  (drop ≈ {region_elev.max()-region_elev.min():.1f} m)")
print(f"    slope: max {region_slope.max():.1f}°  mean {region_slope.mean():.1f}°")
print(f"    NDVI (waterfall pixel):  {ndvi[cy_pix, cx_pix]:.2f}")
print(f"    RGB pixel (cascade center): R={rgb[cy_pix,cx_pix,0]} G={rgb[cy_pix,cx_pix,1]} B={rgb[cy_pix,cx_pix,2]}")

# === 7) Save final manifest ===
import json
manifest = {
    "aoi_center_wgs84": [W, S, E, N],
    "aoi_center_utm21j": [W_e, S_n, E_e, N_n],
    "dem": {
        "10m_utm21j": "dem/terrarium_monday_10m_utm21j.tif",
        "30m_utm21j_sources": ["dem/nasadem_elevation.tif", "dem/alos-dem_data.tif", "dem/cop-dem-glo-30_data.tif"],
        "elev_range_m": [float(elev.min()), float(elev.max())],
        "elev_mean_m": float(elev.mean()),
    },
    "sentinel2": {
        "scene": "S2B_MSIL2A_20251120T133829_R124_T21JYM",
        "date": "2025-11-20",
        "cloud_cover_pct": 0.002,
        "bands_10m": ["B02.tif", "B03.tif", "B04.tif", "B08.tif"],
        "rgb_composite": "analysis/rgb_truecolor_utm21j.tif",
        "ndvi_composite": "analysis/ndvi_10m.png",
    },
    "osm": {
        "file": "osm/overpass_monday.json",
        "elements": 43779,
        "waterways": 59,
        "buildings": 29979,
        "highways": 2048,
        "natural": 12598,
    },
    "blender_inputs": {
        "heightmap": "dem/terrarium_monday_10m_utm21j.tif",
        "albedo": "analysis/rgb_truecolor_utm21j.tif",
        "hillshades": [f"analysis/hillshade_10m_{l}.png" for l in ["az315_sunNW","az045_sunNE","az180_sunS","az225_sunSW","az090_sunE_low45"]],
        "slope": "analysis/slope_10m.png",
        "ndvi": "analysis/ndvi_10m.png",
    },
}
with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(f"\n-> manifest.json ({os.path.getsize('manifest.json')} bytes)")
