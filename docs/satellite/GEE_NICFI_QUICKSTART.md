# Satellite terrain mapping — GEE + NICFI + PC + element84 quickstart

> Operator-level quickstart for the four satellite/GIS data paths wired into
> `scripts/satellite/`. Pick a path, run the copy-paste invocation, and the
> license gate + sidecar + CRS-normalize pipeline does the rest.
>
> Scope: the canonical 62-ha La Quebrada Viva AOI (W −57.045, S −25.645,
> E −57.015, N −25.615) at Escobar, Paraguarí. Every fetcher reads the AOI
> from `docs/site_data/aoi_62ha.geojson` and writes under `docs/site_data/<dataset>/`.

---

## 1. Which fetcher do I want?

| If you want… | Use | Why |
|---|---|---|
| Broad multi-collection STAC search (S-2, S-1, Landsat, HLS, WorldCover, JRC GSW, CHIRPS, TerraClimate, MODIS) without auth | `scripts.satellite.pc_stac_quickstart` | Microsoft Planetary Computer signs hrefs in-place via `pc.sign_inplace`; widest catalog under one API. |
| Multi-year reductions: NDVI median + p10/p50/p90 percentile triad | `scripts.satellite.gee_quickstart` | Google Earth Engine runs reducers cloud-side so you don't pay the bandwidth of every scene. |
| One-off Sentinel-2 RGB+NIR+SWIR+SCL grab (no auth) | `scripts.satellite.fetch_sentinel2` | element84 Earth-Search is anonymous and quick; production fetcher already pulls the canonical bands. |
| ~5 m tropical-forest basemap visuals for the deck (canopy texture) | `scripts.satellite.fetch_nicfi` | Planet NICFI basemaps fill the gap between Sentinel-2 (10 m) and drone (sub-meter). **Deck-only license.** |
| WorldCover / JRC Global Surface Water / Hansen forest-loss thematic rasters | `scripts.satellite.fetch_landcover` | Bundle-eligible CC-BY-4.0 mosaics; the three rasters that close the "is this pixel forest / water / lost" question. |
| Daily rainfall (CHIRPS) or monthly climate water balance (TerraClimate) | `scripts.satellite.fetch_climate` | NetCDF + GeoTIFF pull, public-domain / CC-BY equivalent. |

Default choice when in doubt: **Planetary Computer** (`pc_stac_quickstart`). It's
auth-free, covers the widest collection set, and the search output cached at
`docs/site_data/pc_search/<collection>/index.json` is replayable via `--items-file`.

---

## 2. Authentication setup

### 2.1 Google Earth Engine

Two paths. Default is (a) for local exploratory work, (b) for CI / headless runs.

**(a) Interactive — Ivan's laptop:**

```bash
pip install earthengine-api
earthengine authenticate                # one-off browser flow
python -m scripts.satellite.gee_quickstart --start 2025-01-01 --end 2026-06-01
```

**(b) Service account — headless / CI:**

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/ee-service-account.json
export EE_PROJECT=your-gcp-project-id   # must have Earth Engine API enabled
python -m scripts.satellite.gee_quickstart --download
```

`_init_ee()` checks `GOOGLE_APPLICATION_CREDENTIALS` first, then falls back to the
cached interactive credential. If neither works it prints a clear "run
`earthengine authenticate` or set GOOGLE_APPLICATION_CREDENTIALS + EE_PROJECT"
message and exits cleanly — never crashes mid-run.

### 2.2 Planet NICFI

```bash
export PLANET_API_KEY=PLAK9b7570886c70458aabe51cf6fe90fa4f   # supplied 2026-06-17
python -m scripts.satellite.fetch_nicfi --list-mosaics
```

Free for non-commercial / tropical-forest use; signup at
[planet.com/nicfi](https://www.planet.com/nicfi/). No key → `_need_key()` prints
the signup URL and exits 1; nothing scary happens.

### 2.3 Microsoft Planetary Computer

**No auth.** `pystac-client` searches anonymously; `planetary-computer.sign_inplace`
signs the asset hrefs before download. Just:

```bash
pip install planetary-computer pystac-client stackstac rioxarray
```

### 2.4 element84 Earth-Search

**No auth.** The fetcher just hits `https://earth-search.aws.element84.com/v1/search`.
Used by `fetch_sentinel2.py` as the production path.

---

## 3. Copy-paste invocations

All commands are idempotent: `skip_if_exists` short-circuits on cached outputs
with `≥ MIN_VALID_BYTES` (8 KiB); CRS normalize and sidecar still re-run on
cached files so older partial fetches get upgraded.

### 3.1 Planetary Computer search (default first move)

```bash
# Probe which LQV-relevant collections are present:
python -m scripts.satellite.pc_stac_quickstart --list-collections

# Recent Sentinel-2 L2A scenes (90-day window, ≤20% cloud):
python -m scripts.satellite.pc_stac_quickstart --collection sentinel-2-l2a --days 90

# Sentinel-1 RTC (all-weather SAR, full year, top 10 scenes):
python -m scripts.satellite.pc_stac_quickstart --collection sentinel-1-rtc --days 365 --max 10

# Replay an earlier search without burning the round-trip:
python -m scripts.satellite.pc_stac_quickstart \
    --items-file docs/site_data/pc_search/sentinel-2-l2a/index.json
```

Output: `docs/site_data/pc_search/<collection>/index.json` (STAC search results
only — not the scene rasters; keeps the repo small).

### 3.2 GEE — NDVI median + percentile triad

```bash
# NDVI median over the last ~17 months (stats-only, no GeoTIFF):
python -m scripts.satellite.gee_quickstart --start 2025-01-01 --end 2026-06-01

# Same, but download the 10 m GeoTIFF:
python -m scripts.satellite.gee_quickstart --download

# Multi-year drought-floor / typical / peak-greenness triad (gap #14):
python -m scripts.satellite.gee_quickstart \
    --percentiles --start 2020-01-01 --end 2026-06-01 --download
```

Output: `docs/site_data/gee/ndvi_<start>_<end>.tif` and
`docs/site_data/gee/ndvi_percentiles_<start>_<end>.tif` plus `.meta.json`
sidecars. SCL cloud/shadow mask with a 2-pixel dilation buffer (gap #6) and a
30% scene cloud-cover prefilter are already wired in.

### 3.3 element84 Sentinel-2 grab

```bash
python -m scripts.satellite.fetch_sentinel2     # canonical bands → docs/site_data/sentinel2/
```

Note: `docs/site_data/sentinel2/*.tif` is on the **Never stage** list and the
pre-commit hook will reject any attempt to commit those rasters. Keep them
local; downstream sub-renders read them via `lqv/site_data.py`.

### 3.4 Planet NICFI basemap tiles

```bash
python -m scripts.satellite.fetch_nicfi --list-mosaics
python -m scripts.satellite.fetch_nicfi \
    --mosaic planet_medres_visual_2026-04_mosaic --zoom 15
```

Output: `docs/site_data/nicfi/<mosaic>/z15/<x>_<y>.png` + one mosaic-level
`_nicfi.meta.json` sidecar (per-tile sidecars would explode the manifest).
Zoom 15 ≈ 5 m/px at the equator; LQV AOI fits in a handful of tiles.

### 3.5 Landcover triad (WorldCover + JRC GSW + Hansen GFC)

```bash
python -m scripts.satellite.fetch_landcover     # pulls all three at once
```

Output:
- `docs/site_data/landcover/esa_worldcover_2021.tif` (10 m, 11 classes)
- `docs/site_data/landcover/jrc_gsw_occurrence.tif` (30 m, %-of-time water 1984–present)
- `docs/site_data/landcover/hansen_gfc_lossyear_20S_060W.tif` (30 m, year-of-loss 2001–2023)

Hansen comes from the public GCS bucket
(`storage.googleapis.com/earthenginepartners-hansen/GFC-2023-v1.11/`); tile
naming for the LQV AOI is `20S_060W`. All three carry CC-BY-4.0.

### 3.6 Climate (CHIRPS + TerraClimate)

```bash
python -m scripts.satellite.fetch_climate
```

CHIRPS daily rainfall + TerraClimate monthly water balance, AOI-clipped.

---

## 4. License gate — what bundles, what's deck-only, what's blocked

`scripts/satellite/_license.py` is the single source of truth. Every fetcher
calls `assert_compatible(license_id)` *before* touching the network so banned
licenses fail loud at fetch time, not at bundle time.

| Class | License IDs | Where it goes |
|---|---|---|
| **Bundle-eligible** | `CC0-1.0`, `CC-BY-4.0`, `public-domain`, `USGS-PD`, `NASA-PD` | Both the redistribution bundle and the deck. |
| **Deck-only** | `CC-BY-NC-4.0`, `CC-BY-NC-2.0`, `Planet-NICFI-Non-Commercial` | Deck only — the bundle manifest excludes these tiles. |
| **BLOCKED** | `CC-BY-SA-4.0`, `CC-BY-SA-3.0`, `CC-BY-NC-SA-4.0`, `GPL-3.0`, `AGPL-3.0` | `LicenseBlocked` raised; nothing is written. |

Practical translation:

- **Sentinel-2 / Sentinel-1 / Copernicus DEM** → bundle. CC-BY-4.0 equivalent
  under the ESA Copernicus Legal Notice.
- **WorldCover / JRC GSW / Hansen GFC** → bundle. CC-BY-4.0.
- **CHIRPS / TerraClimate** → bundle (public domain / CC-BY-4.0).
- **Planet NICFI** → deck-only. Sidecars record `bundle_eligibility: "deck_only"`;
  the bundle manifest skips them.
- **Anything OpenStreetMap-derived (ODbL share-alike) or CC-BY-SA** → BLOCKED.
  If you find yourself needing OSM data, pre-render it to a non-derivative
  raster (e.g. a contextual basemap PNG used only in the deck), or skip it.

Unknown license IDs warn but pass; the fetcher should treat them as deck-only
until reviewed. Edit `scripts/satellite/_license.py` to add new IDs — that's the
one chokepoint.

---

## 5. Cadastro polygon drop-in (post-escritura)

Every fetcher clips to the AOI rectangle today and writes
`parcel_polygon_pending: true` in the sidecar. Once the escritura (2026-06-27)
delivers the cadastro padron geometry, drop a single file at:

```
docs/site_data/cadastro/padrones.geojson
```

…with the union of padrones `838, 1827, 840, 1096, 629, 454`. From that moment
forward every new fetch automatically:

1. Uses `aoi_polygon_geojson()` (which prefers cadastro over the rectangle).
2. Calls `clip_to_parcel(da)` with `rio.clip(all_touched=True, drop=True)`.
3. Flips `parcel_polygon_pending: false` in the sidecar.

No code changes needed. The fallback chain in `scripts/satellite/_aoi.py` is the
contract. The Paraguay sanity-check guard (`-63.0 ≤ west ≤ -54.0 and
-28.0 ≤ south ≤ -19.0`) still applies. To force the rectangular AOI for a
debug run even after cadastro lands: `export LQV_FORCE_BBOX_AOI=1`.

---

## 6. Pre-commit hook activation

`/.githooks/pre-commit` is **not** wired automatically — per the global "never
update git config" rule, the agent will not run `git config core.hooksPath`
on your behalf. Activate per-clone with:

```bash
git config core.hooksPath .githooks
```

The hook refuses to commit anything matching the **Never stage** patterns
(`scripts/mcp_daemon.py`, `docs/site_data/sentinel2/*.tif`,
`docs/*_boleto_*.pdf`, `docs/*_escritura_*.pdf`, `docs/2026-*_*.pdf`) and
prints the restore hint. Bypass with `--no-verify` only in emergencies — the
"Never stage" list lives in `CLAUDE.md` and the hook regex is the last line of
defense, not the first.

---

## 7. Common gotchas

- **No items returned** → run `python -m scripts.satellite.test_stac` to probe
  the endpoints. Often the AOI is fine and an upstream STAC is down.
- **GEE getDownloadURL fails on big AOIs** → 62 ha is well under the 32 MB
  synchronous-export limit, so this should not bite. If you widen the AOI
  beyond ~5 km × 5 km, switch to `ee.batch.Export.image.toDrive` and pull
  manually.
- **NICFI 429 rate-limited** → `@with_retry()` handles backoff automatically;
  the Retry-After header is logged. Don't tighten the loop, just wait.
- **Sidecar missing** → every fetcher writes one. If you see a raster without a
  `.meta.json` next to it, it was probably pulled by hand outside the
  `scripts/satellite/` pipeline — re-fetch through the fetcher to get the
  license-gate guarantee.
- **CRS mismatch downstream** → `_crs.to_canonical_inplace_path` normalizes to
  EPSG:32721 (WGS84 / UTM 21S +south) on every fetch (re-run too). If a
  raster is still in EPSG:4326, it predates the normalize step; re-run the
  fetcher and it'll be upgraded in place.

---

## 8. See also

- `scripts/satellite/__init__.py` — tier roadmap (T1 / T2 / T3 / T4).
- `docs/site_data/DATA_INVENTORY.md` — what we already have on disk.
- `LICENSE_BUNDLE.md` — bundle license policy in long form.
- `scripts/satellite/_aoi.py` — AOI rectangle, cadastro fallback chain,
  `LQV_FORCE_BBOX_AOI` override.
- `scripts/satellite/_license.py` — frozen sets behind the gate.
- `scripts/satellite/_meta.py` — sidecar schema.
- `scripts/satellite/_retry.py` — `@with_retry()`, `skip_if_exists`,
  `MIN_VALID_BYTES`.
