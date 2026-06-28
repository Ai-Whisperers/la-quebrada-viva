"""Pull high-res DEM for Cataratas del Monday via OpenTopography's bulk API.
Mirrors the pattern from fetch_opentopo_dem.py in the LQV repo.
Uses ALOS World 3D 30 m (canonical) + Copernicus GLO-30 (cross-check).
"""
import sys, time, requests
from AOI import BBOX
import rasterio

API = "https://cloud.sdsc.edu/v1/opentopoapi"
DEM_SOURCES = {
    "alos_aw3d30":  {"name": "ALOS World 3D 30m", "format": "GTiff", "nodata": -9999},
    "cop30":        {"name": "Copernicus GLO-30", "format": "GTiff", "nodata": -9999},
    "srtm_gl1":     {"name": "SRTM GL1 30m",      "format": "GTiff", "nodata": -9999},
    "nasadem":      {"name": "NASADEM 30m",       "format": "GTiff", "nodata": -9999},
}

for key, src in DEM_SOURCES.items():
    out = f"dem/{key}_monday.tif"
    print(f"\n--- {key} ---")
    payload = {
        "demtype":   src["name"],
        "south":     BBOX[1], "north": BBOX[3],
        "west":      BBOX[0], "east":  BBOX[2],
        "outputFormat": src["format"],
        "API_Key":   "",
    }
    try:
        t0 = time.time()
        r = requests.post(API, json=payload, timeout=300, stream=True)
        print(f"  HTTP {r.status_code}, {r.headers.get('Content-Length','?')} bytes, {time.time()-t0:.1f}s")
        if r.status_code == 200 and "tif" in r.headers.get("Content-Type",""):
            with open(out, "wb") as f:
                for chunk in r.iter_content(1 << 20):
                    f.write(chunk)
            with rasterio.open(out) as ds:
                print(f"  -> {ds.width}×{ds.height} px, CRS={ds.crs}, res={ds.res}, dtype={ds.dtypes[0]}")
        else:
            print(f"  body: {r.text[:300]}")
    except Exception as e:
        print(f"  FAIL: {e}")
