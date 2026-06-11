"""Merge terrarium tiles (10m) into a single GeoTIFF aligned with S2 grid."""
import os, math, re
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.io import MemoryFile
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
from PIL import Image
from AOI import BBOX

W, S, E, N = BBOX
TARGET_RES_M = 10  # 10m to match S2
deg_per_m = TARGET_RES_M / 111320.0

def decode_terrarium(p):
    img = np.array(Image.open(p).convert("RGB"))
    return img[:,:,0].astype(np.float32)*256.0 + img[:,:,1].astype(np.float32) + img[:,:,2].astype(np.float32)/256.0 - 32768.0

srcs = []
for p in sorted(os.listdir("dem/terrarium_z13")):
    pp = f"dem/terrarium_z13/{p}"
    m = re.match(r"13_(\d+)_(\d+)\.png", p)
    x, y = int(m.group(1)), int(m.group(2))
    z = 13
    lon_w = x / (2**z) * 360.0 - 180.0
    lon_e = (x+1) / (2**z) * 360.0 - 180.0
    lat_n = math.degrees(math.atan(math.sinh(math.pi * (1 - 2*y / (2**z)))))
    lat_s = math.degrees(math.atan(math.sinh(math.pi * (1 - 2*(y+1) / (2**z)))))
    elev = decode_terrarium(pp)
    transform = from_bounds(lon_w, lat_s, lon_e, lat_n, elev.shape[1], elev.shape[0])
    mf = MemoryFile()
    ds = mf.open(driver="GTiff", height=elev.shape[0], width=elev.shape[1], count=1,
                 dtype="float32", crs="EPSG:4326", transform=transform)
    ds.write(elev, 1)
    ds.close()
    srcs.append(mf.open())

mosaic, out_trans = merge(srcs, bounds=(W, S, E, N), res=(deg_per_m, deg_per_m))
arr = mosaic[0]
print(f"WGS84 mosaic: {arr.shape}  range {arr.min():.1f} – {arr.max():.1f}  mean {arr.mean():.1f}  res={out_trans.a*111320:.1f} m")

profile = {"driver": "GTiff", "height": arr.shape[0], "width": arr.shape[1], "count": 1,
           "dtype": "float32", "crs": "EPSG:4326", "transform": out_trans,
           "compress": "lzw", "tiled": True, "nodata": -9999.0}
with rasterio.open("dem/terrarium_monday_10m.tif", "w", **profile) as dst:
    dst.write(arr, 1)
print(f"  -> dem/terrarium_monday_10m.tif  {os.path.getsize('dem/terrarium_monday_10m.tif')//1024} KB")

# UTM 21J reprojection
dst_crs = "EPSG:32721"
transf, w, h = calculate_default_transform("EPSG:4326", dst_crs, arr.shape[1], arr.shape[0], W, S, E, N,
                                           resolution=TARGET_RES_M)
arr_utm = np.empty((h, w), dtype="float32")
reproject(arr, arr_utm, src_crs="EPSG:4326", dst_crs=dst_crs,
          src_transform=out_trans, dst_transform=transf, resampling=Resampling.bilinear)
profile_utm = {**profile, "height": h, "width": w, "crs": dst_crs, "transform": transf}
with rasterio.open("dem/terrarium_monday_10m_utm21j.tif", "w", **profile_utm) as dst:
    dst.write(arr_utm, 1)
print(f"  -> dem/terrarium_monday_10m_utm21j.tif  {os.path.getsize('dem/terrarium_monday_10m_utm21j.tif')//1024} KB")
print(f"     UTM res: {transf.a:.2f} m  shape {arr_utm.shape}")
print(f"     UTM range: {arr_utm.min():.1f} – {arr_utm.max():.1f} m  mean {arr_utm.mean():.1f}")
