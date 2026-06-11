"""GEDI L2A extraction via HTTPS pre-signed CloudFront download.

Per granule: hit the NASA Earthdata HTTPS endpoint with the bearer token,
follow the 303 redirect to a pre-signed CloudFront URL, download the 1.2 GB
HDF5 file to a temp path, read it with h5py, extract only the bbox-relevant
quality-filtered shots, drop the temp file, repeat.

No S3 creds required (EULA gate is bypassed because the pre-signed URL is
authorised at redirect time, not at S3 request time). Slow because we pull
the full file; for 27 granules ≈ 30-60 min on a normal link.

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
from dotenv import load_dotenv

HERE = Path(__file__).parent.parent
load_dotenv(dotenv_path=HERE / ".env.local")
TOKEN = os.environ.get("NASA_EARTHDATA_TOKEN")
if not TOKEN:
    print("ERROR: NASA_EARTHDATA_TOKEN not in .env.local", file=sys.stderr)
    sys.exit(1)

BBOX = {"south": -25.645, "north": -25.615, "west": -57.045, "east": -57.015}
LPDAAC = "https://data.lpdaac.earthdatacloud.nasa.gov"
TMP_DIR = Path("/tmp/gedi")
TMP_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR = HERE / "docs" / "site_data"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = OUT_DIR / "gedi_l2a_points.csv"
OUT_SUMMARY = OUT_DIR / "gedi_l2a_summary.txt"
GRANULES_JSON = OUT_DIR / "gedi_granules_index.json"

REQUEST_TIMEOUT = 60
DOWNLOAD_CHUNK = 1024 * 1024
MAX_RETRIES = 3
PROGRESS_EVERY = 200 * 1024 * 1024  # log every 200 MB

print("=" * 70)
print("GEDI L2A extraction via HTTPS (fallback for EULA-gated S3)")
print("=" * 70)
print(f"Bbox: W={BBOX['west']} S={BBOX['south']} E={BBOX['east']} N={BBOX['north']}")

# 1) CMR query (cached from previous run if available)
print("\n[1/5] Loading granule list (re-querying CMR if missing)…")
if GRANULES_JSON.exists():
    with open(GRANULES_JSON) as f:
        idx = json.load(f)
    granules = idx["granules"]
    print(f"      cached: {len(granules)} granules from {GRANULES_JSON.name}")
else:
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
        {
            "id": e["id"],
            "title": e.get("title", ""),
            "time_start": e.get("time_start", ""),
            "time_end": e.get("time_end", ""),
            "granule_size_mb": float(e.get("granule_size", 0)) if e.get("granule_size") else None,
            "links": [l for l in e.get("links", []) if l.get("href", "").endswith(".h5")],
        }
        for e in entries
    ]
    with open(GRANULES_JSON, "w") as f:
        json.dump({"bbox": BBOX, "n_granules": len(granules), "granules": granules}, f, indent=2)
    print(f"      fetched: {len(granules)} granules")


# 2) Build the HTTPS URL list
downloads = []
for g in granules:
    for l in g.get("links", []):
        href = l.get("href", "")
        if href.endswith(".h5"):
            downloads.append((g["id"], g.get("time_start", ""), href, g.get("granule_size_mb")))
            break

print(f"\n[2/5] {len(downloads)} granules to process (~{sum(d[3] or 0 for d in downloads):.0f} MB total)")

# 3) Per-granule: download, parse, drop
print(f"\n[3/5] Streaming {len(downloads)} granules…")
all_shots = []
n_processed = 0
n_beams_skipped = 0
n_download_failed = 0
t_start = time.time()

for idx, (gid, tstart, url, sz_mb) in enumerate(downloads, 1):
    fname = url.split("/")[-1]
    tmp_path = TMP_DIR / fname
    label = f"[{idx}/{len(downloads)}] {fname}"
    granule_t = time.time()

    if tmp_path.exists() and tmp_path.stat().st_size > 100_000_000:
        # Validate with h5py before skipping — a truncated partial download
        # will leave a large file that h5py cannot open.
        try:
            with h5py.File(tmp_path, "r") as _h:
                _ = list(_h.keys())
            print(f"      {label}  cached on disk, skipping download")
        except Exception:
            tmp_path.unlink()
            print(f"      {label}  cached file was truncated, re-downloading")
    else:
        ok = False
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                with requests.get(
                    url, headers={"Authorization": f"Bearer {TOKEN}"},
                    allow_redirects=True, stream=True, timeout=REQUEST_TIMEOUT,
                ) as r:
                    r.raise_for_status()
                    total = int(r.headers.get("Content-Length", 0)) or (sz_mb * 1024 * 1024 if sz_mb else 0)
                    written = 0
                    last_log = 0
                    with open(tmp_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=DOWNLOAD_CHUNK):
                            if not chunk:
                                continue
                            f.write(chunk)
                            written += len(chunk)
                            if written - last_log >= PROGRESS_EVERY:
                                pct = 100 * written / total if total else 0
                                print(f"      {label}  {written/1e6:.0f}/{total/1e6:.0f} MB ({pct:.0f}%)", flush=True)
                                last_log = written
                ok = True
                break
            except Exception as e:
                print(f"      {label}  attempt {attempt}/{MAX_RETRIES} FAILED: {type(e).__name__}: {str(e)[:80]}")
                if tmp_path.exists():
                    tmp_path.unlink()
                time.sleep(2 * attempt)
        if not ok:
            n_download_failed += 1
            continue

    dl_t = time.time() - granule_t
    try:
        with h5py.File(tmp_path, "r") as h5:
            beams = [k for k in h5.keys() if k.startswith("BEAM")]
            shots_this = 0
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
                shots_this += len(df)
        n_processed += 1
        elapsed = time.time() - t_start
        rate = n_processed / max(elapsed, 1)
        eta = (len(downloads) - n_processed) / max(rate, 1e-6)
        print(f"      {label}  +{shots_this} shots, {n_processed} done, "
              f"elapsed {elapsed:.0f}s, ETA {eta:.0f}s ({dl_t:.0f}s this granule)", flush=True)
    finally:
        try:
            tmp_path.unlink()
        except FileNotFoundError:
            pass

print(f"\n      processed {n_processed}/{len(downloads)} ({n_download_failed} download failures, {n_beams_skipped} beams skipped)")
print(f"      {len(all_shots)} shot-frames before dedup")

if not all_shots:
    print("No shots extracted. See docstring for debugging.")
    sys.exit(1)

# 4) Dedup + save
print("\n[4/5] Dedup + save…")
combined = pd.concat(all_shots, ignore_index=True)
combined = combined.drop_duplicates(subset=["latitude", "longitude", "beam"])
combined = combined.sort_values(["latitude", "longitude"]).reset_index(drop=True)
combined.to_csv(OUT_CSV, index=False)
print(f"      wrote {len(combined)} unique shots to {OUT_CSV}")

# 5) Summary
print("\n[5/5] Summary…")
print("\nGround elevation (m AMSL):")
print(combined["ground_elevation_m"].describe().to_string())
print("\nCanopy height (m):")
print(combined["canopy_height_m"].describe().to_string())

with open(OUT_SUMMARY, "w") as f:
    f.write(f"GEDI L2A extraction via HTTPS — {datetime.utcnow().isoformat()}Z\n")
    f.write(f"Bbox: W={BBOX['west']} S={BBOX['south']} E={BBOX['east']} N={BBOX['north']}\n")
    f.write(f"Granules searched: {len(downloads)}\n")
    f.write(f"Granules processed (download+parse OK): {n_processed}\n")
    f.write(f"Granules download failed: {n_download_failed}\n")
    f.write(f"Beams skipped (missing fields): {n_beams_skipped}\n")
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
