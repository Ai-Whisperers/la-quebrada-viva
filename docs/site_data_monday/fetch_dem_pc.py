"""Pull high-res DEMs for Cataratas del Monday via Microsoft Planetary Computer.
Free, no auth, signed URLs. Three sources:
  - Copernicus DSM 10m (best, ESA 2010-2015 optical stereo)
  - ALOS-DEM 30m (JAXA, independent cross-check)
  - NASADEM 30m (NASA improved SRTM)
"""
import os, json, time, requests
import pystac_client
import planetary_computer
import rasterio
from AOI import BBOX

CAT = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
os.makedirs("dem", exist_ok=True)

# Each DEM is a global mosaic; we search the catalog for the single tile covering our bbox.
DATASETS = [
    ("cop-dem-glo-10",  "Copernicus DSM 10m (ESA, 2010-2015)"),
    ("cop-dem-glo-30",  "Copernicus DEM 30m (ESA, fallback)"),
    ("alos-dem",        "ALOS-DEM 30m (JAXA)"),
    ("nasadem",         "NASADEM 30m (NASA)"),
    ("sentinel-1-rtc",  "Sentinel-1 RTC SAR — for vegetation penetration"),  # SAR amplitude, used as surface texture
]

results = {}
for cid, name in DATASETS:
    print(f"\n--- {cid}  ({name}) ---")
    try:
        search = CAT.search(
            collections=[cid],
            bbox=list(BBOX),
        )
        items = list(search.items())
        if not items:
            print(f"  no items")
            continue
        item = items[0]
        signed = planetary_computer.sign(item)
        print(f"  {item.id}")
        for asset_key, asset in signed.assets.items():
            if asset.media_type in ("image/tiff; application=geotiff; profile=cloud-optimized",
                                     "image/tiff", "application/octet-stream",
                                     "image/vnd.stac.geotiff; cloud-optimized=true",
                                     "image/tiff; application=geotiff"):
                href = asset.href
                out = f"dem/{cid}_{asset_key}.tif"
                if not os.path.exists(out):
                    print(f"  downloading {asset_key} -> {out}")
                    t0 = time.time()
                    with requests.get(href, stream=True, timeout=300) as r:
                        r.raise_for_status()
                        with open(out, "wb") as f:
                            for chunk in r.iter_content(1 << 20):
                                f.write(chunk)
                    print(f"    {os.path.getsize(out)//1024} KB in {time.time()-t0:.1f}s")
                try:
                    with rasterio.open(out) as ds:
                        print(f"    {ds.width}×{ds.height} px  CRS={ds.crs}  res={ds.res}  dtype={ds.dtypes[0]}")
                        results[cid] = {"path": out, "shape": [ds.width, ds.height], "res": ds.res, "crs": str(ds.crs)}
                except Exception as ex:
                    print(f"    rasterio open failed: {ex}")
        # store item metadata
        with open(f"dem/{cid}_item.json", "w") as f:
            json.dump(dict(item.properties), f, indent=2, default=str)
    except Exception as e:
        print(f"  FAIL: {e}")

with open("dem/manifest.json", "w") as f:
    json.dump(results, f, indent=2)
print("\n=== manifest ===")
print(json.dumps(results, indent=2))
