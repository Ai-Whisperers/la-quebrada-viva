"""GEDI L2A extraction via cloud-native S3 streaming (no full-file download).

Fetches short-lived S3 creds from LP DAAC, opens each granule's HDF5 file
directly from `lp-prod-protected` via s3fs + h5py, reads only the rows we
need, filters by bbox + quality, writes a single CSV.

27 granules × ~1.2 GB each = ~32 GB total if downloaded. This approach reads
only the columns we need and streams them — fast, no disk use.

Outputs:
  - docs/site_data/gedi_l2a_points.csv
  - docs/site_data/gedi_l2a_summary.txt
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import h5py
import numpy as np
import pandas as pd
import requests
import s3fs
from dotenv import load_dotenv

HERE = Path(__file__).parent.parent
load_dotenv(dotenv_path=HERE / ".env.local")
TOKEN = os.environ.get("NASA_EARTHDATA_TOKEN")
if not TOKEN:
    print("ERROR: NASA_EARTHDATA_TOKEN not in .env.local", file=sys.stderr)
    sys.exit(1)

BBOX = {
    "south": -25.645,
    "north": -25.615,
    "west": -57.045,
    "east": -57.015,
}
BUCKET = "lp-prod-protected"
S3_CREDS_URL = "https://data.lpdaac.earthdatacloud.nasa.gov/s3credentials"

OUT_DIR = HERE / "docs" / "site_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = OUT_DIR / "gedi_l2a_points.csv"
OUT_SUMMARY = OUT_DIR / "gedi_l2a_summary.txt"
GRANULES_JSON = OUT_DIR / "gedi_granules_index.json"

print("=" * 70)
print("GEDI L2A streaming extraction — Escobar / Mbopicuá / Ybyraty, PY")
print("=" * 70)
print(f"Bbox: W={BBOX['west']} S={BBOX['south']} E={BBOX['east']} N={BBOX['north']}")
print(f"~{((BBOX['east']-BBOX['west'])*111.0)*((BBOX['north']-BBOX['south'])*111.0):.1f} km² search area")
print()

# 1) Refresh S3 creds (1h lifetime)
print("[1/5] Fetching short-lived S3 creds from LP DAAC…")
resp = requests.get(S3_CREDS_URL, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=30)
resp.raise_for_status()
creds = resp.json()
print(f"      access key: {creds['accessKeyId'][:16]}…  expires in 1h")

fs = s3fs.S3FileSystem(
    key=creds["accessKeyId"],
    secret=creds["secretAccessKey"],
    token=creds["sessionToken"],
)

# 2) CMR query (re-run, save the index for future use)
print("\n[2/5] Querying CMR for GEDI02_A v002 granules over the bbox…")
cmr_url = "https://cmr.earthdata.nasa.gov/search/granules.json"
cmr_params = {
    "short_name": "GEDI02_A",
    "version": "002",
    "bounding_box": f"{BBOX['west']},{BBOX['south']},{BBOX['east']},{BBOX['north']}",
    "page_size": 200,
}
cmr = requests.get(cmr_url, params=cmr_params, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=60)
cmr.raise_for_status()
cmr_data = cmr.json()
granules = cmr_data["feed"]["entry"]
print(f"      {len(granules)} granules")
with open(GRANULES_JSON, "w") as f:
    json.dump({
        "bbox": BBOX,
        "n_granules": len(granules),
        "granules": [
            {
                "id": g["id"],
                "title": g.get("title", ""),
                "time_start": g.get("time_start", ""),
                "time_end": g.get("time_end", ""),
                "granule_size_mb": float(g.get("granule_size", 0)) if g.get("granule_size") else None,
                "links": [l for l in g.get("links", []) if l.get("href", "").endswith(".h5")],
            }
            for g in granules
        ],
    }, f, indent=2)
print(f"      granule index saved to {GRANULES_JSON}")

# 3) Build S3 keys from the HTTPS URLs
def s3_key_from_https(href: str) -> str:
    # href like https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/.../file.h5
    prefix = "https://data.lpdaac.earthdatacloud.nasa.gov/"
    if href.startswith(prefix):
        return f"{BUCKET}/" + href[len(prefix):]
    return href

s3_keys = []
for g in granules:
    for l in g.get("links", []):
        href = l.get("href", "")
        if href.endswith(".h5"):
            s3_keys.append(s3_key_from_https(href))
            break
print(f"\n[3/5] {len(s3_keys)} S3 keys ready")

# 4) Stream each granule, extract bbox-relevant shots
print(f"\n[4/5] Streaming {len(s3_keys)} granules via s3fs + h5py…")
all_shots = []
n_processed = 0
n_beams_skipped = 0
t_start = time.time()
for i, s3_path in enumerate(s3_keys, 1):
    fname = s3_path.split("/")[-1]
    try:
        with fs.open(s3_path, "rb") as s3f:
            with h5py.File(s3f, "r") as h5:
                beams = [k for k in h5.keys() if k.startswith("BEAM")]
                for beam in beams:
                    try:
                        lat = h5[f"{beam}/lat_lowestmode"][:]
                        lon = h5[f"{beam}/lon_lowestmode"][:]
                        elev_ground = h5[f"{beam}/elev_lowestmode"][:]
                        elev_highest = h5[f"{beam}/elev_highestreturn"][:]
                        quality = h5[f"{beam}/quality_flag"][:]
                        degrade = h5[f"{beam}/degrade_flag"][:]
                        sensitivity = h5[f"{beam}/sensitivity"][:]
                    except KeyError:
                        n_beams_skipped += 1
                        continue

                    good = (
                        (quality == 0)
                        & (degrade == 0)
                        & (sensitivity > 0.9)
                        & np.isfinite(elev_ground)
                        & np.isfinite(elev_highest)
                    )
                    in_bbox = (
                        (lat >= BBOX["south"])
                        & (lat <= BBOX["north"])
                        & (lon >= BBOX["west"])
                        & (lon <= BBOX["east"])
                    )
                    mask = good & in_bbox
                    if not np.any(mask):
                        continue

                    canopy = elev_highest[mask] - elev_ground[mask]
                    canopy_ok = (canopy >= 0) & (canopy <= 80)
                    if not np.any(canopy_ok):
                        continue

                    df = pd.DataFrame({
                        "latitude": lat[mask][canopy_ok],
                        "longitude": lon[mask][canopy_ok],
                        "ground_elevation_m": elev_ground[mask][canopy_ok],
                        "canopy_height_m": canopy[canopy_ok],
                        "sensitivity": sensitivity[mask][canopy_ok],
                        "beam": beam,
                        "granule": fname,
                    })
                    all_shots.append(df)
        n_processed += 1
        if i % 5 == 0 or i == len(s3_keys):
            elapsed = time.time() - t_start
            print(f"      [{i}/{len(s3_keys)}] {n_processed} ok, {len(all_shots)} shots so far ({elapsed:.0f}s)")
    except Exception as e:
        print(f"      [{i}/{len(s3_keys)}] skipped {fname}: {type(e).__name__}: {str(e)[:100]}")

print(f"\n      processed {n_processed}/{len(s3_keys)} granules, {n_beams_skipped} beams skipped, {len(all_shots)} shot-frames before dedup")

if not all_shots:
    print("No quality-filtered shots. Try expanding bbox or relaxing filter (sensitivity > 0.5).")
    sys.exit(1)

combined = pd.concat(all_shots, ignore_index=True)
combined = combined.drop_duplicates(subset=["latitude", "longitude", "beam"])
combined = combined.sort_values(["latitude", "longitude"]).reset_index(drop=True)
combined.to_csv(OUT_CSV, index=False)

print(f"\n[5/5] WROTE {len(combined)} unique quality-filtered GEDI L2A shots to {OUT_CSV}")

print("\nGround elevation (m AMSL):")
print(combined["ground_elevation_m"].describe().to_string())
print("\nCanopy height (m):")
print(combined["canopy_height_m"].describe().to_string())

with open(OUT_SUMMARY, "w") as f:
    f.write(f"GEDI L2A extraction — {datetime.utcnow().isoformat()}Z\n")
    f.write(f"Bbox: W={BBOX['west']} S={BBOX['south']} E={BBOX['east']} N={BBOX['north']}\n")
    f.write(f"Granules searched: {len(granules)}\n")
    f.write(f"Granules processed: {n_processed}\n")
    f.write(f"Beams skipped (missing fields): {n_beams_skipped}\n")
    f.write(f"Quality-filtered shots (unique): {len(combined)}\n\n")
    f.write("Ground elevation (m AMSL):\n")
    f.write(combined["ground_elevation_m"].describe().to_string() + "\n\n")
    f.write("Canopy height (m):\n")
    f.write(combined["canopy_height_m"].describe().to_string() + "\n\n")
    f.write("Beam distribution:\n")
    f.write(combined["beam"].value_counts().to_string() + "\n\n")
    f.write("Granule distribution (top 10):\n")
    f.write(combined["granule"].value_counts().head(10).to_string() + "\n")
    f.write(f"\nLat range: {combined['latitude'].min():.5f} to {combined['latitude'].max():.5f}\n")
    f.write(f"Lon range: {combined['longitude'].min():.5f} to {combined['longitude'].max():.5f}\n")

print(f"\nSummary written to {OUT_SUMMARY}")
