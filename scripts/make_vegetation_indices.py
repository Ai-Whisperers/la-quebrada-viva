#!/usr/bin/env python3
"""NDVI / NDWI / SWIR moisture maps from Sentinel-2 L2A bands."""
import argparse, json, os, sys
import numpy as np
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling

BASE = os.path.dirname(os.path.abspath(__file__))
S2   = os.path.join(BASE, "docs/site_data/sentinel2")
OUT  = os.path.join(BASE, "docs/site_data/analysis")
JSON = os.path.join(BASE, "assets/terrain/escobar_height.json")

BANDS = {
    "red":   f"{S2}/S2B_21JVM_20260512_0_L2A_red.tif",
    "green": f"{S2}/S2B_21JVM_20260512_0_L2A_green.tif",
    "blue":  f"{S2}/S2B_21JVM_20260512_0_L2A_blue.tif",
    "nir":   f"{S2}/S2B_21JVM_20260512_0_L2A_nir.tif",
    "swir16":f"{S2}/S2B_21JVM_20260512_0_L2A_swir16.tif",
}

def load_bbox():
    with open(JSON) as f: d=json.load(f)
    b=d["bbox"]
    return [b["left"],b["bottom"],b["right"],b["top"]]

def reproject_to_wgs84(src_path, bbox_wgs84, width=350):
    with rio.open(src_path) as src:
        dst_crs="EPSG:4326"
        transform, w, h = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        data = src.read(1).astype(np.float32)
    return data

def read_band_utm(path):
    with rio.open(path) as src:
        data = src.read(1).astype(np.float32)
        nodata = src.nodata
    data[data==nodata] = np.nan
    return data / 10000.0

def ratio_idx(a, b):
    num = a-b; den = a+b
    denom = np.where(den==0, 1, den)
    idx = np.where(den==0, 0, num/denom)
    return np.clip(idx, -1, 1)

def _apply_cmap(arr, cmap_name):
    import matplotlib.cm as mcm
    norm = (arr - arr.min()) / (arr.max() - arr.min() + 1e-10)
    cmap = mcm.get_cmap(cmap_name)
    rgb = cmap(norm)
    return (rgb[:,:,:3]*255).astype(np.uint8)

def save_png(arr, out_path, cmap):
    rgb = colormap(arr, cmap)
    from PIL import Image
    Image.fromarray(rgb).save(out_path)
    print(f"  Wrote {out_path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force",action="store_true")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    bbox = load_bbox()

    needed=["ndvi_map.png","ndwi_map.png","swir_moisture_map.png"]
    if all(os.path.exists(os.path.join(OUT,f)) for f in needed) and not args.force:
        print("All indices exist. Use --force to overwrite.")
        return

    print("Loading bands (divide by 10000 for DN->reflectance)...")
    red    = read_band_utm(BANDS["red"])
    green  = read_band_utm(BANDS["green"])
    nir    = read_band_utm(BANDS["nir"])
    swir16 = read_band_utm(BANDS["swir16"])

    # reproject to common grid (use red shape as ref, UTM zone)
    print("Computing indices...")
    ndvi = ratio_idx(nir, red)
    ndwi = ratio_idx(green, nir)
    swir = ratio_idx(nir, swir16)

    save_png(ndvi,  os.path.join(OUT,"ndvi_map.png"),         "Greens")
    save_png(ndwi,  os.path.join(OUT,"ndwi_map.png"),         "Blues_r")
    save_png(swir,  os.path.join(OUT,"swir_moisture_map.png"),"coolwarm")

    pct_veg = np.nanmean(ndvi > 0.3) * 100
    pct_wat = np.nanmean(ndwi > 0.0) * 100
    mean_ndvi = np.nanmean(ndvi)

    line = (f"Vegetation indices — datetime.utcnow().isoformat()Z\n"
            f"NDVI>0.3: {pct_veg:.1f}%  NDWI>0.0: {pct_wat:.1f}%  Mean NDVI: {mean_ndvi:.3f}\n")
    print(line.strip())
    with open(os.path.join(OUT,"analysis_summary.txt"),"a") as f:
        f.write(line)

if __name__=="__main__": main()
