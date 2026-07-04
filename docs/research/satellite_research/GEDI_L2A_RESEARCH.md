# GEDI L2A Python Ecosystem — Research Report

**Goal:** Extract GEDI L2A shots over a 3.3 km × 3.3 km bbox in Paraguay, getting (lat, lon, ground_elevation, canopy_height) with quality filtering.

**TL;DR — the 403 fix and fastest stack:**
1. Your 403 is almost certainly an unaccepted EULA. Fix at https://urs.earthdata.nasa.gov/profile → Approved Applications → accept **GEDI02_A**.
2. Use **`earthaccess` + `h5py` over fsspec** for the actual extraction. Skip Harmony for L2A (GEDI is not on a supported Harmony service yet — see Caveat 1).
3. `GEDI02_A.002` concept_id for cloud: **`C2142771958-LPCLOUD`** (provider `LPCLOUD`, not `LPCUMC`).

---

## 1. Top 5 recommended libraries

| # | Library | What it does | GitHub / Docs | Stars / Recency |
|---|---------|--------------|---------------|-----------------|
| 1 | **`earthaccess`** | One-line EDL auth + CMR search + S3 streaming via fsspec. **Use this for everything.** | https://github.com/earthaccess-dev/earthaccess | 612★ · v0.18.0 (May 2026) · very active |
| 2 | **`h5py`** | Reads GEDI HDF5 files (HDF-EOS5). Pair with fsspec handle from earthaccess for partial reads. | https://h5py.org | Industry standard |
| 3 | **`harmony-py`** | Python client for NASA Harmony (server-side OGC subsetting). Useful for L4A gridded products; limited for L2A shot data. | https://github.com/nasa/harmony-py | 69★ · v1.3.4 (Apr 2026) · active |
| 4 | **`geopandas` + `shapely`** | Bbox filtering, GeoJSON export of GEDI shots for GIS. | https://geopandas.org | Standard |
| 5 | **`requests` (CMR direct)** | Lowest-level fallback: call CMR search API directly. The official LP DAAC `GEDI_Finder` script uses this pattern. | https://github.com/nasa/GEDI-Data-Resources/blob/main/python/scripts/GEDI_Finder/GEDI_Finder.py | (script) |

**Skip these:**
- `rGEDI` — R-only, not useful in Python pipelines.
- `gedi-subsetter` (LP DAAC Bitbucket) — 398-byte README, basically abandoned in favor of earthaccess + Harmony.
- The 21 random `gedi-*` repos on GitHub — most are forks, personal experiments, or empty. The two that matter are `nasa/GEDI-Data-Resources` (official tutorials) and `nasa/gedi-l4a-agb-density-mosaics` (L4A mosaics).

---

## 2. Fastest subsetting method for a 3.3 km × 3.3 km bbox in Paraguay

**Winner: `earthaccess` search + `h5py` over fsspec (cloud, no full-file download).**

Why this beats Harmony here:

1. **GEDI02_A is not in Harmony's supported subsetter services.** Harmony's deployed services that work on HDF5 (`ldds/subset-band-name`, `ldds/geoloco`) target HDF4/HDF-EOS2. GEDI is HDF5 with a non-standard "shot" structure that doesn't map to `sds/trajectory-subsetter` (which is for segmented trajectory data). There IS a `how-to-access-GEDI-data-Harmony.ipynb` tutorial in the official `nasa/GEDI-Data-Resources` repo, but it's labeled as a preview/limited capability — full GEDI L2A spatial subsetting through Harmony is not yet generally available.
2. **Harmony OGC EDR with `bbox=`** works on gridded products; GEDI L2A is point-cloud, so spatial trimming on Harmony is essentially a no-op for L2A.
3. **For a 3.3 km × 3.3 km patch**, you'll get maybe 5–15 intersecting sub-orbit granules. Each granule is ~600 MB–1.2 GB. If you `earthaccess.download()` the full files, you're moving ~5 GB+ for ~200 GEDI shots. With `earthaccess.open()` + `h5py`, you only fetch the ~5 small datasets you need from each file via byte-range HTTP reads — typically <10 MB total.
4. **Harmony WOULD be fastest for `GEDI04_A`** (gridded biomass, ~1 km tiles) — use `harmony-py` with `BBox()` for those, or just download the single GeoTIFF you need.

**Recommended stack (in order):**
```
earthaccess.login()  →  auth + 1-time EULA check
earthaccess.search_data(short_name='GEDI02_A', bounding_box=(W,S,E,N),
                        temporal=('2019-04-18','2023-03-16'))
earthaccess.open(results)  →  list of fsspec file handles
h5py.File(fs_hdl)          →  read lat_lowestmode, lon_lowestmode,
                              elev_lowestmode, rh98 from each BEAMXXXX
                              and filter by bbox in numpy
```

---

## 3. Sample code patterns (copy-paste ready)

### 3.1 GEDI auth (EULA is the gotcha — see §4)
```python
import earthaccess
auth = earthaccess.login()  # looks for ~/.netrc, env vars EDL_USERNAME/EDL_PASSWORD, or prompts
# If 403s persist: go to https://urs.earthdata.nasa.gov/profile and accept
# the GEDI02_A application EULA, then wait 5 min.
```

`.netrc` (recommended for scripts/CI):
```
machine urs.earthdata.nasa.gov
login YOUR_EDL_USER
password YOUR_EDL_PASS
```
```bash
chmod 0600 ~/.netrc
```

### 3.2 Search for granules over a 3.3 km × 3.3 km bbox in Paraguay
```python
import earthaccess

# Example bbox: somewhere in eastern Paraguay (Atlantic Forest corridor)
# Adjust to your actual site. Order is (W, S, E, N).
west, south, east, north = -56.5000, -25.2000, -56.4700, -25.1700
# (0.03° lat × 0.03° lon ≈ 3.3 km × 3.3 km at this latitude)

results = earthaccess.search_data(
    short_name='GEDI02_A',
    version='002',
    bounding_box=(west, south, east, north),
    temporal=('2019-04-18', '2023-03-16'),  # full GEDI mission
    cloud_hosted=True,
    count=200,
)
print(f"Found {len(results)} intersecting granules")
```

### 3.3 Stream HDF5 (no full download) + read shots
```python
import h5py
import numpy as np
import earthaccess

fs_files = earthaccess.open(results)  # list of fsspec objects, no download
# Note: pass `persist=True` to keep in-memory after session ends

BEAMS = ['BEAM0000','BEAM0001','BEAM0010','BEAM0011',   # full power
         'BEAM0101','BEAM0110','BEAM1000','BEAM1011']   # coverage

def extract_shots(h5_path):
    """Read + quality-filter one GEDI L2A granule."""
    rows = []
    with h5py.File(h5_path, 'r') as f:
        for b in BEAMS:
            if b not in f:
                continue
            g = f[b]
            # Some paths may be missing on coverage beams
            try:
                lat   = g['lat_lowestmode'][:]
                lon   = g['lon_lowestmode'][:]
                elev  = g['elev_lowestmode'][:]   # ground elevation
                rh    = g['rh'][:]                 # 101 RH metrics per shot
                rh98  = rh[:, 98]                  # canopy height (98th percentile)
                qf    = g['quality_flag'][:]       # 0=poor, 1=good
                deg   = g['degrade_flag'][:]       # 0=not degraded
                sens  = g['sensitivity'][:]        # 0–1
                shot  = g['shot_number'][:]
            except KeyError as e:
                continue

            # Standard GEDI L2A quality filter (per LP DAAC GEDI-Data-Resources tutorial):
            #   quality_flag == 1
            #   degrade_flag == 0
            #   sensitivity  >= 0.95   (strict; default quality_flag uses >=0.9)
            #   rh98 not equal to fill value (-9999)
            mask = (qf == 1) & (deg == 0) & (sens >= 0.95) & (rh98 != -9999) \
                   & (lat > -90) & np.isfinite(elev)

            for i in np.where(mask)[0]:
                rows.append((shot[i], b, lat[i], lon[i], elev[i], rh98[i]))
    return rows

all_shots = []
for fs_hdl in fs_files:
    # earthaccess returns fsspec OpenFile objects; pass .open() to h5py
    with fs_hdl.open() as fp:
        all_shots.extend(extract_shots(fp))

import pandas as pd
df = pd.DataFrame(all_shots,
        columns=['shot_number','beam','lat','lon','ground_elevation','canopy_height'])

# Final bbox clip (in case of edge granule with shots just outside)
in_box = ((df.lon >= west) & (df.lon <= east) &
          (df.lat >= south) & (df.lat <= north))
df = df[in_box].reset_index(drop=True)
print(f"{len(df)} quality-filtered shots in bbox")
df.to_parquet('gedi_l2a_paraguary_3p3km.parquet')
```

### 3.4 Bbox search via raw CMR (the GEDI_Finder pattern — no earthaccess needed)
```python
import requests
concept_ids = {
    'GEDI01_B.002': 'C2142749196-LPCLOUD',
    'GEDI02_A.002': 'C2142771958-LPCLOUD',
    'GEDI02_B.002': 'C2142776747-LPCLOUD',
}
cmr = "https://cmr.earthdata.nasa.gov/search/granules.json"
r = requests.get(cmr, params={
    'concept_id': concept_ids['GEDI02_A.002'],
    'provider':   'LPCLOUD',
    'bounding_box': f"{west},{south},{east},{north}",  # W,S,E,N
    'temporal':   '2019-04-18T00:00:00Z/2023-03-16T23:59:59Z',
    'page_size':  2000,
    'pretty':     True,
})
granules = [g['links'][0]['href'] for g in r.json()['feed']['entry']]
```

### 3.5 GEDI04_A biomass (Harmony — gridded, this is where Harmony shines)
```python
from harmony import Client, BBox, Collection, Request
import datetime

harmony = Client()  # uses ~/.netrc

req = Request(
    collection=Collection(id='C2238261578-ORNL_CLOUD'),  # GEDI04_A.002
    spatial=BBox(west, south, east, north),
    temporal={'start': datetime.datetime(2019,4,18),
              'stop':  datetime.datetime(2023,3,16)},
)
job_id = harmony.submit(req)
harmony.wait_for_job(job_id, show_progress=True)
results = harmony.download_all(job_id, directory='./gedi04a/')
```

### 3.6 L4A biomass (no Harmony, direct download from ORNL DAAC)
```python
results = earthaccess.search_data(
    short_name='GEDI_L4A_AGB_Density_V2',
    version='002',
    bounding_box=(west, south, east, north),
    temporal=('2019-04-18', '2023-03-16'),
)
fs_files = earthaccess.open(results)  # ~1 km GeoTIFF tiles
# Open as rasterio datasets, mosaic, clip to your bbox
```

### 3.7 Quality filtering reference (from LP DAAC official tutorial)
From `nasa/GEDI-Data-Resources/python/tutorials/GEDI_L2A_V2_Tutorial.ipynb`:
```python
# Sensitivity threshold:
#   - 0.9 over land is the L2A default (used in quality_flag)
#   - 0.95 for "best" data (denser canopy, less noise)
#
# mask = (quality_flag == 1) & (degrade_flag == 0) & (sensitivity >= 0.95)
#
# Also: check `surface_flag` (0=land, 1=ocean) if you want land-only,
# and `selected_l2a_algorithm` if you want to use the L2A algorithm specifically
# (not the L1B initial estimate).
```

---

## 4. Gotchas

1. **🔥 403 Forbidden = EULA not accepted.** Go to https://urs.earthdata.nasa.gov/profile → "Applications" → "Approved Applications" → find **GEDI02_A** (and GEDI04_A) → click "Approve". Wait ~5 min. Re-run. `earthaccess.login()` does NOT auto-accept the EULA; the user must do it once in the web UI. This is the most common cause of 403s on GEDI downloads.

2. **Cloud-hosted URLs use `LPCLOUD` provider, not `LPCUMC`.** All concept_ids for direct S3 access in `lp-prod-protected` use the `LPCLOUD` suffix. The HTTPS download URL pattern:
   ```
   https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/GEDI02_A.002/<GRANULE_NAME>/<GRANULE_NAME>.h5
   ```

3. **8 beams per file, 2 types.** BEAM0000–BEAM0011 are "full power" (always on, dense sampling). BEAM0101–BEAM1011 are "coverage" (alternating, sparser). All 8 may be present in a granule; iterate over all and skip beams that lack a required dataset.

4. **`/rh` is a 2D array `[n_shots, 101]`.** Canopy height `rh98` = `rh[:, 98]`. There is sometimes also a top-level `/rh98` convenience dataset — but always read `/rh` and slice, since not all files have `/rh98` as a direct child.

5. **`sensitivity` is a per-beam scalar attribute in some files** and a per-shot dataset in others. The L2A tutorial reads it as a per-shot array. If you get a shape mismatch, check `g['sensitivity'].attrs['description']` or fall back to the per-beam `g.parent.attrs['sensitivity']` (or just use `quality_flag` which already incorporates it).

6. **CMR `bounding_box` order is `W,S,E,N`** (lon_min, lat_min, lon_max, lat_max), NOT `S,W,N,E`. The official `GEDI_Finder.py` uses this — copy it. `earthaccess.search_data(bounding_box=(...))` expects `(W, S, E, N)` too.

7. **No-data fill value is `-9999`** (not `NaN`). Filter with `!= -9999`, not `np.isfinite()`.

8. **Harmony OGC EDR `bbox=` on GEDI02_A is a preview**, not production. The Harmony tutorial in `nasa/GEDI-Data-Resources/python/how-tos/how-to-access-GEDI-data-Harmony.ipynb` exists, but the service is limited — for shot-level data, just stream with `earthaccess.open()` + `h5py`.

9. **OpenAltimetry.org is a domain squatter (slot-gambling site).** The real OpenAltimetry moved to **`https://openaltimetry.earthdatacloud.nasa.gov/`** (NSIDC, 2023). Old API endpoints like `https://openaltimetry.org/data/api/...` return 404 or redirect to spam.

10. **GEDI04_A is distributed by ORNL DAAC, not LP DAAC.** Different provider, different S3 bucket, different concept_id range (`-ORNL_CLOUD` suffix). Short name is **`GEDI_L4A_AGB_Density_V2`**, not `GEDI04_A`.

11. **GEDI L4A biomass is a 1 km gridded mosaic** — it does NOT give you per-shot biomass. For per-shot AGB estimates, you'd need L2A canopy height + an allometric model (e.g., Jenkins et al. 2003, Chave 2014). L4A is a fitted model on gridded auxiliary data.

12. **The `nasa/gedi-notebooks` repo 404s.** The repo was renamed/migrated to **`nasa/GEDI-Data-Resources`** in June 2023. All current GEDI tutorials live there.

13. **Earthdata Login sessions expire** (default 2 hours for bearer tokens). For long-running scripts, refresh with `earthaccess.login()` periodically, or use a long-lived bearer token from https://urs.earthdata.nasa.gov/user_tokens.

---

## 5. OpenAltimetry — current API endpoints

**Domain change:** `openaltimetry.org` → `openaltimetry.earthdatacloud.nasa.gov` (NSIDC, 2023).

**Landing page:** `https://openaltimetry.earthdatacloud.nasa.gov/`
**Swagger UI:** `https://openaltimetry.earthdatacloud.nasa.gov/openapi/swagger-ui/index.html`

**Base API URL (current):** `https://openaltimetry.earthdatacloud.nasa.gov/api/v1/`

Useful endpoints (NSIDC, May 2024+):
- `GET /api/v1/gediL4A/search` — list GEDI L4A rasters intersecting a bbox
- `GET /api/v1/gediL2A/search` — list GEDI L2A shots in a small area
- `POST /api/v1/gediL2A/data` — bulk shot download given a search area

**⚠ OpenAltimetry is for interactive visualization + small-area bulk queries, NOT for large-scale extraction.** For a 3.3 km × 3.3 km Paraguay bbox you could use it, but `earthaccess` + `h5py` is more reproducible and faster. Treat OpenAltimetry as a "sanity check / preview" tool.

If the swagger paths I listed above 404 in the future, the current authoritative doc is on the OpenAltimetry site itself under "API Documentation" → Swagger UI.

---

## 6. NASA Harmony OGC coverages URL for GEDI02_A

**Canonical base:** `https://harmony.earthdata.nasa.gov/`

**Two endpoint shapes (per the official docs at `https://harmony.earthdata.nasa.gov/docs/`):**

### 6.1 OGC Coverages API (variable subset, NOT bbox for GEDI L2A)
```
https://harmony.earthdata.nasa.gov/{collectionId}/ogc-api-coverages/1.0.0/{variable}/coverage/rangeset
```
- For GEDI02_A.002: `{collectionId}` is `C2142771958-LPCLOUD` (or short name `GEDI02_A.002` URL-encoded).
- `{variable}` is the dataset name. GEDI doesn't expose UMM-Var variables cleanly — try `all`.

**But this is the wrong tool for GEDI L2A** — it returns the whole granule, not a bbox subset, because GEDI shot data isn't gridded.

### 6.2 OGC EDR API (cube, with bbox — for gridded data)
```
https://harmony.earthdata.nasa.gov/ogc-api-edr/1.1.0/collections/{collectionId}/cube?bbox=W,S,E,N&datetime=...&parameter-name=all
```
- Example: `https://harmony.earthdata.nasa.gov/ogc-api-edr/1.1.0/collections/GEDI02_A.002/cube?bbox=-56.50,-25.20,-56.47,-25.17&datetime=2019-04-18/2023-03-16&parameter-name=all`
- This is also **limited/unsupported for GEDI L2A** in current Harmony production. Use it for GEDI04_A.

### 6.3 With Python (`harmony-py`)
```python
from harmony import Client, BBox, Collection, Request
import datetime

harmony = Client()
req = Request(
    collection=Collection(id='C2142771958-LPCLOUD'),  # GEDI02_A.002
    # For L2A the BBox will be ignored or return full granules — see caveat 8 above
    spatial=BBox(west=-56.50, south=-25.20, east=-56.47, north=-25.17),
    temporal={'start': datetime.datetime(2019,4,18),
              'stop':  datetime.datetime(2023,3,16)},
)
job_id = harmony.submit(req)
harmony.wait_for_job(job_id, show_progress=True)
harmony.download_all(job_id, directory='./harmony_out/')
```

**Auth for Harmony (any of):**
- `.netrc` with `machine urs.earthdata.nasa.gov` (recommended)
- `EDL_USERNAME` / `EDL_PASSWORD` env vars
- `Client(token='EDL_bearer_token')` — get token at https://urs.earthdata.nasa.gov/user_tokens

---

## 7. Reference URLs (all confirmed working as of June 2026)

| Resource | URL |
|---|---|
| `earthaccess` GitHub | https://github.com/earthaccess-dev/earthaccess |
| `earthaccess` docs | https://earthaccess.readthedocs.io/en/latest/ |
| `harmony-py` GitHub | https://github.com/nasa/harmony-py |
| `harmony-py` docs | https://harmony-py.readthedocs.io/en/latest/ |
| Harmony API docs | https://harmony.earthdata.nasa.gov/docs/ |
| **GEDI-Data-Resources** (official tutorials) | https://github.com/nasa/GEDI-Data-Resources |
| GEDI L2A V2 tutorial notebook | https://github.com/nasa/GEDI-Data-Resources/blob/main/python/tutorials/GEDI_L2A_V2_Tutorial.ipynb |
| GEDI Finder (CMR bbox script) | https://github.com/nasa/GEDI-Data-Resources/blob/main/python/scripts/GEDI_Finder/GEDI_Finder.py |
| GEDI04_A mosaics repo | https://github.com/nasa/gedi-l4a-agb-density-mosaics |
| GEDI02_A data pool HTTPS base | `https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/GEDI02_A.002/` |
| CMR granule search base | `https://cmr.earthdata.nasa.gov/search/granules.json` |
| LP DAAC GEDI02_A catalog | https://lpdaac.usgs.gov/data/data-catalog/gedi02_a-v002/ |
| Earthdata Login profile (EULA fix) | https://urs.earthdata.nasa.gov/profile |
| Real OpenAltimetry | https://openaltimetry.earthdatacloud.nasa.gov/ |
| GEDI02_A.002 CMR concept_id | **`C2142771958-LPCLOUD`** |
| GEDI01_B.002 CMR concept_id | `C2142749196-LPCLOUD` |
| GEDI02_B.002 CMR concept_id | `C2142776747-LPCLOUD` |
| GEDI04_A.002 CMR concept_id (ORNL) | `C2238261578-ORNL_CLOUD` (verify in CMR — ORNL collection) |

---

## 8. Recommended one-shot script for your Paraguay 3.3 km × 3.3 km

```python
#!/usr/bin/env python3
"""GEDI L2A extraction: 3.3 km × 3.3 km bbox in Paraguay."""
import earthaccess, h5py, numpy as np, pandas as pd

# 1. AUTH (one-time, prompts or .netrc)
earthaccess.login()

# 2. YOUR BBOX (W, S, E, N) — change this
west, south, east, north = -56.5000, -25.2000, -56.4700, -25.1700

# 3. SEARCH
results = earthaccess.search_data(
    short_name='GEDI02_A', version='002',
    bounding_box=(west, south, east, north),
    temporal=('2019-04-18', '2023-03-16'),
    cloud_hosted=True, count=200,
)
print(f"{len(results)} granules intersect")

# 4. STREAM + READ (no full download)
fs = earthaccess.open(results)
BEAMS = ['BEAM0000','BEAM0001','BEAM0010','BEAM0011',
         'BEAM0101','BEAM0110','BEAM1000','BEAM1011']

shots = []
for fp_obj in fs:
    with fp_obj.open() as fp:
        with h5py.File(fp, 'r') as h5:
            for b in BEAMS:
                if b not in h5: continue
                g = h5[b]
                try:
                    lat  = g['lat_lowestmode'][:]
                    lon  = g['lon_lowestmode'][:]
                    elev = g['elev_lowestmode'][:]
                    rh   = g['rh'][:]
                    rh98 = rh[:, 98]
                    qf   = g['quality_flag'][:]
                    deg  = g['degrade_flag'][:]
                    sens = g['sensitivity'][:]
                    sn   = g['shot_number'][:]
                except KeyError:
                    continue
                m = (qf == 1) & (deg == 0) & (sens >= 0.95) & (rh98 != -9999)
                for i in np.where(m)[0]:
                    if (west <= lon[i] <= east) and (south <= lat[i] <= north):
                        shots.append((sn[i], b, lat[i], lon[i], elev[i], rh98[i]))

df = pd.DataFrame(shots,
    columns=['shot_number','beam','lat','lon','ground_elevation','canopy_height'])
df.to_parquet('gedi_l2a_paraguay_3p3km.parquet')
print(f"{len(df)} shots saved.")
```

---

**Caveats from the field (June 2026):**
- `harmony-py` is healthy (last release Apr 2026); `earthaccess` v0.18.0 (May 2026) is the modern path.
- OpenAltimetry.org is gone — use `.earthdatacloud.nasa.gov` subdomain.
- GEDI's official tutorials moved to `nasa/GEDI-Data-Resources` (the old `gedi-notebooks` repo 404s).
- GEDI02_A is **not yet** a first-class Harmony subsetting target (preview only); use the earthaccess path.
- If the EULA is the 403 cause, fixing it requires a manual web step — there is no programmatic EULA acceptance.
