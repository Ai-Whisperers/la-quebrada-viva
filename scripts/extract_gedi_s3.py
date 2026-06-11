"""GEDI L2A extraction — OPTIMIZED via S3 streaming with h5py selective read.

Per granule: get short-lived S3 creds, open the HDF5 file directly from
`lp-prod-protected` via s3fs, then read ONLY the datasets we care about
(lat, lon, elev_ground, elev_highest, quality, degrade, sensitivity for
each beam). h5py fetches only the bytes it needs — typically 50-150 MB
per granule, not the full 1.2 GB.

Speed: 27 granules × 5-15 min = 2.5-7 hours total. Or with EULAs + Harmony
server-side subsetting, this drops to seconds.

Requires: GEDI02_A EULA accepted at Earthdata profile, regenerated
bearer token in .env.local.

Outputs (same as before):
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

BBOX = {"south": -25.645, "north": -25.615, "west": -57.045, "east": -57.015}
S3_CREDS_URL = "https://data.lpdaac.earthdatacloud.nasa.gov/s3credentials"
BUCKET = "lp-prod-protected"

OUT_DIR = HERE / "docs" / "site_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = OUT_DIR / "gedi_l2a_points.csv"
OUT_SUMMARY = OUT_DIR / "gedi_l2a_summary.txt"
GRANULES_JSON = OUT_DIR / "gedi_granules_index.json"

# Only the columns we need (in addition to lat/lon for the bbox mask)
NEEDED_DATASETS = [
    "lat_lowestmode",
    "lon_lowestmode",
    "elev_lowestmode",
    "elev_highestreturn",
    "quality_flag",
    "degrade_flag",
    "sensitivity",
]

print("=" * 70)
print("GEDI L2A — S3 streaming with h5py selective read (EULA-gated)")
print("=" * 70)
print(f"Bbox: W={BBOX['west']} S={BBOX['south']} E={BBOX['east']} N={BBOX['north']}")
print(f"Reads per granule: {len(NEEDED_DATASETS)} datasets × ~8 beams = {len(NEEDED_DATASETS)*8} reads")
print(f"Expected per-granule network: ~50-200 MB (vs 1.2 GB full file)")

# 1) S3 creds (1h lifetime)
print("\n[1/5] Fetching short-lived S3 creds…")
resp = requests.get(S3_CREDS_URL, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=30)
resp.raise_for_status()
creds = resp.json()
fs = s3fs.S3FileSystem(
    key=creds["accessKeyId"],
    secret=creds["secretAccessKey"],
    token=creds["sessionToken"],
)
print(f"      access key: {creds['accessKeyId'][:16]}…")

# 2) CMR query (cached)
print("\n[2/5] Loading granule list…")
if not GRANULES_JSON.exists():
    cmr = requests.get(
        "https://cmr.earthdata.nasa.gov/search/granules.json",
        params={
            "short_name": "GEDI02_A",
            "version": "002",
            "bounding_box": f"{BBOX['west']},{BBOX['south']},{BBOX['east']},{BBOX['north']}",
            "page_size": 200,
        },
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=60,
    )
    cmr.raise_for_status()
    entries = cmr.json()["feed"]["entry"]
    granules = [
        {"id": e["id"], "title": e.get("title", ""),
         "time_start": e.get("time_start", ""), "time_end": e.get("time_end", ""),
         "granule_size_mb": float(e.get("granule_size", 0)) if e.get("granule_size") else None,
         "links": [l for l in e.get("links", []) if l.get("href", "").endswith(".h5")]}
        for e in entries
    ]
    with open(GRANULES_JSON, "w") as f:
        json.dump({"bbox": BBOX, "n_granules": len(granules), "granules": granules}, f, indent=2)
else:
    with open(GRANULES_JSON) as f:
        granules = json.load(f)["granules"]
print(f"      {len(granules)} granules")

# 3) Build S3 keys
s3_keys = []
for g in granules:
    for l in g["links"]:
        href = l["href"]
        if href.endswith(".h5") and href.startswith("https://data.lpdaac.earthdatacloud.nasa.gov/"):
            key = f"{BUCKET}/" + href.replace("https://data.lpdaac.earthdatacloud.nasa.gov/", "")
            s3_keys.append((g["id"], g["time_start"], key, g.get("granule_size_mb")))
            break
print(f"\n[3/5] {len(s3_keys)} S3 keys ready")

# 4) Stream each granule, read ONLY needed datasets
print(f"\n[4/5] Streaming {len(s3_keys)} granules via s3fs + h5py…")
all_shots = []
n_processed = 0
n_skipped_perm = 0
t_start = time.time()

for i, (gid, tstart, key, sz_mb) in enumerate(s3_keys, 1):
    fname = key.split("/")[-1]
    t0 = time.time()
    try:
        with fs.open(key, "rb") as s3f:
            with h5py.File(s3f, "r") as h5:
                beams = [k for k in h5.keys() if k.startswith("BEAM")]
                for beam in beams:
                    # Selective read: only the datasets we need
                    try:
                        columns = {ds: h5[f"{beam}/{ds}"][:] for ds in NEEDED_DATASETS}
                    except KeyError as e:
                        continue
                    lat = columns["lat_lowestmode"]
                    lon = columns["lon_lowestmode"]
                    elev_ground = columns["elev_lowestmode"]
                    elev_highest = columns["elev_highestreturn"]
                    quality = columns["quality_flag"]
                    degrade = columns["degrade_flag"]
                    sensitivity = columns["sensitivity"]

                    good = (
                        (quality == 0) & (degrade == 0) & (sensitivity > 0.9)
                        & np.isfinite(elev_ground) & np.isfinite(elev_highest)
                    )
                    in_bbox = (
                        (lat >= BBOX["south"]) & (lat <= BBOX["north"])
                        & (lon >= BBOX["west"]) & (lon <= BBOX["east"])
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
                        "granule_time_start": tstart,
                    })
                    all_shots.append(df)
        n_processed += 1
        elapsed = time.time() - t_start
        rate = n_processed / max(elapsed, 1)
        eta = (len(s3_keys) - n_processed) / max(rate, 1e-6)
        print(f"      [{i}/{len(s3_keys)}] ok  {len(all_shots)} shots so far  "
              f"elapsed {elapsed:.0f}s, ETA {eta:.0f}s ({time.time()-t0:.0f}s this granule)", flush=True)
    except Exception as e:
        msg = str(e)
        if "Forbidden" in msg or "AccessDenied" in msg or "403" in msg:
            n_skipped_perm += 1
            print(f"      [{i}/{len(s3_keys)}] FORBIDDEN  {fname[:50]}…  (EULAs not yet accepted, see R01 in RESEARCH_GAPS.md)", flush=True)
            if n_skipped_perm >= 3:
                print(f"\n      {n_skipped_perm} consecutive 403s — aborting. Accept the GEDI02_A EULA at\n"
                      f"      https://search.earthdata.nasa.gov/search?q=GEDI02_A\n"
                      f"      and regenerate the bearer token at\n"
                      f"      https://urs.earthdata.nasa.gov/profile\n"
                      f"      then re-run this script.")
                break
        else:
            print(f"      [{i}/{len(s3_keys)}] FAILED  {fname[:50]}…  {type(e).__name__}: {msg[:80]}")

print(f"\n      processed {n_processed}/{len(s3_keys)} ({n_skipped_perm} permission failures)")
print(f"      {len(all_shots)} shot-frames before dedup")

if not all_shots:
    print("No shots extracted. Likely cause: EULAs not accepted yet.")
    sys.exit(1)

# 5) Dedup + save
print("\n[5/5] Dedup + save…")
combined = pd.concat(all_shots, ignore_index=True)
combined = combined.drop_duplicates(subset=["latitude", "longitude", "beam"])
combined = combined.sort_values(["latitude", "longitude"]).reset_index(drop=True)
combined.to_csv(OUT_CSV, index=False)
print(f"      wrote {len(combined)} unique shots to {OUT_CSV}")

print("\nGround elevation (m AMSL):")
print(combined["ground_elevation_m"].describe().to_string())
print("\nCanopy height (m):")
print(combined["canopy_height_m"].describe().to_string())

with open(OUT_SUMMARY, "w") as f:
    f.write(f"GEDI L2A — S3 streaming + h5py selective read — {datetime.utcnow().isoformat()}Z\n")
    f.write(f"Bbox: W={BBOX['west']} S={BBOX['south']} E={BBOX['east']} N={BBOX['north']}\n")
    f.write(f"Granules searched: {len(s3_keys)}\n")
    f.write(f"Granules processed: {n_processed}\n")
    f.write(f"Granules permission-denied: {n_skipped_perm}\n")
    f.write(f"Quality-filtered unique shots: {len(combined)}\n\n")
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

print(f"\nSummary: {OUT_SUMMARY}")
print("DONE.")
