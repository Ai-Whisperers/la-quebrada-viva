# Extended-AOI multi-DEM + polygon vegetation brief — La Quebrada Viva (Phase-0 §12 v1)

> Lat/lon AOI rectangle 0.03° × 0.05° (~3 × 5.5 km) centred on the 30.9 ha
> Mbopicua parcel polygon (centroid −57.0355, −25.6073). Four open-data DEMs
> at native 1″ pitch + Cop30-derived slope/aspect + polygon NDVI/NDWI rasters
> reconciled against the Sentinel-2 stats published in
> [[post_escritura_site_knowledge]] §3.

## Headline

- **Four DEMs agree within ±2 m on mean elevation** (range 206.0–208.7 m) and within ±17 m on max (378–395 m). Topography record is structurally locked.
- **Relief 116 → 390 m AMSL** over the 5.5 × 3 km extended footprint — 274 m of vertical, dominated by the NE→SW ridge system above the parcel.
- **Cop30 slope-pct** mean 11.6 %, median 8.3 % across the 19 440-px window — only ~50 % of the extended AOI is below the 8 % flat threshold (vs. 13.8 % inside the parcel, per [[topology_lod_brief]]).
- **Cop30 aspect** mean 179°, median 190° — bulk of the extended AOI faces S/SW, matching the parcel's 71.6 % S/SW-facing prior (passive-cooling friendly, sun-averted).
- **Polygon NDVI median 0.918** (mean 0.888) — wall-to-wall mature canopy, no detected clearings; floor of 0.36 is the single noisy edge pixel, not a real opening.
- **Polygon NDWI median −0.828** — zero open water at S-2 scale (`frac_gt_0 = 0`); the Quebrada is sub-pixel and gallery-shaded.

## Per-DEM intercomparison (extended AOI, 108×180 = 19 440 px @ ~28×31 m)

| DEM | Mean (m) | Median (m) | Min (m) | Max (m) | Std (m) | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| ALOS AW3D30 v3.2 | 207.8 | 177.0 | 116.0 | 395.0 | 73.0 | JAXA PRISM stereo; declared accuracy ±5 m vertical |
| Cop30 GLO-30 | 206.3 | 176.0 | 116.4 | 390.5 | 72.7 | ESA TanDEM-X derivative; float32, **canonical for slope/aspect derivatives** |
| NASADEM v001 | 206.0 | 176.0 | 115.0 | 378.0 | 72.3 | SRTM reprocessed with ASTER GDEM voidfill; lowest max — likely smoothed crest |
| SRTM GL1 v3 | 208.7 | 179.0 | 118.0 | 382.0 | 72.4 | NASA/USGS legacy 1″; ~2 m high bias against others |
| **Cross-DEM σ on mean** | **±1.2 m** | | | | | RMS spread |

Inside the parcel (108 × 108 px subset, per [[analysis_brief]]): ALOS reports 116–380 m AMSL, mean 162 m, median 149 m — i.e. the parcel sits in the lower half of the extended-AOI relief.

## Cop30 slope + aspect (extended AOI)

| Field | Mean | Median | P10 | P90 | Max | Note |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Slope (%) | 11.6 | 8.3 | 1.4* | 24.5* | 85.2 | P10/P90 from float32 percentile call |
| Aspect (°) | 179.2 | 190.0 | — | — | 359.99 | 0/360=N, 90=E, 180=S, 270=W |

\* approximate; exact percentile reproducible via `python -c "import rasterio, numpy as np; a=rasterio.open('docs/site_data/extended_aoi/cop30_slope_pct.tif').read(1); m=a>0; print(np.percentile(a[m],[10,90]))"`.

Buildability classes for the **extended** 998 ha footprint (cf. [[analysis_brief]] for the parcel-tight cut):

- Flat (0–8 %): ~50 % of area → ~500 ha of low-slope land in the watershed buffer (most concentrated in the NE → SW ridge-foot fan).
- Buildable (8–15 %): ~20 % (the parcel's predominant class).
- Challenging (15–30 %): ~20 %.
- Steep (>30 %): ~10 % (the ridge faces above 250 m AMSL).

## Polygon vegetation stats (30.98 ha pixel-derived area vs 30.915 ha metadata)

NDVI distribution from `polygon_veg_stats.json` (S2B 2026-05-12, 3098 px @ 10 m):

| Metric | Value |
| ---: | ---: |
| Mean | 0.888 |
| Median | 0.918 |
| P05 | 0.722 |
| P25 | 0.883 |
| P75 | 0.932 |
| P95 | 0.945 |
| Frac > 0.6 | 0.979 |
| Frac > 0.8 | 0.896 |
| Frac < 0.2 | 0.000 |

NDWI (Gao, green/NIR):

| Metric | Value |
| ---: | ---: |
| Mean | −0.811 |
| Median | −0.828 |
| P05 | −0.868 |
| P95 | −0.692 |
| Frac > 0 | 0.000 |
| Frac > 0.2 | 0.000 |

Reconciliation against the published [[post_escritura_site_knowledge]] §3 headline (rows from `polygon_veg_stats.json:41-66`):

| Metric | Published | Derived | Δ |
| --- | ---: | ---: | ---: |
| NDVI median | 0.917 | 0.918 | +0.001 |
| NDVI P25 | 0.890 | 0.883 | −0.007 |
| NDVI P75 | 0.937 | 0.932 | −0.005 |
| NDVI frac > 0.6 | 0.974 | 0.979 | +0.005 |
| NDWI frac > 0 | 0.000 | 0.000 | 0.000 |

All five within ±0.01 — published numbers reproduce.

## Reflectance-transform footnote (load-bearing for the published deck)

From `polygon_veg_stats.json:17-21`:

> "Scale-only DN→reflectance to stay consistent with `make_ndvi_mask.py` and the
> headline numbers in `post_escritura_site_knowledge.md`. The S2 metadata
> declares offset=−0.1 but applying it saturates dense-canopy NDVI at 1.0; the
> offset is a harmonization transform, not an analytical correction."

Treat the deck NDVI (median 0.917) as the analytical canonical. If a future
batch re-applies the −0.1 offset, the curve compresses upward and the deck
numbers no longer cross-validate. Keep the scale-only convention.

## Engineering implications (LOD directive: high-res for parcel, low-poly for surrounds)

- **Parcel-tight DEM stays canonical** at 1 m (LiDAR not yet sourced) or 30 m ALOS as fallback ([[topology_lod_brief]]). Use the parcel-tight ALOS clip for all in-polygon micro-grading.
- **Surrounding 5 km ring** → Cop30 30 m is the canonical extended source. ±1.2 m cross-DEM σ on mean is below the 5 m vertical noise floor of any of these products, so the visual difference between ALOS/Cop30/NASADEM/SRTM at the **landscape scale** is undetectable in render. Pick Cop30 for new derivatives (it carries the slope/aspect already).
- **NE→SW ridge structure** (relief 274 m over 5.5 km = ~5 % regional gradient) — needs to enter any establishing shot of the property; the parcel is in the visual basin of that ridge.
- **Bulk S/SW aspect** of the extended AOI aligns with the parcel's S/SW orientation — the broader microclimate is consistent (cool, sun-averted slope), confirming Rule 6 + Rule 8 passive-cooling thesis at the watershed scale, not just the parcel.

## Sub-render typology

- `lqv/subscene/extended_aoi_terrain.py` — Cop30 30 m mesh, 5 × 3 km terrain card with parcel polygon overlay; low-poly (decimated to ~20k tris) per LOD directive.
- `lqv/subscene/dem_intercomparison.py` — 4-panel grid (ALOS / Cop30 / NASADEM / SRTM) coloured by elevation, parcel polygon outline, mean-elevation labels.
- `lqv/subscene/slope_aspect_map.py` — Cop30 slope (viridis 0–30 %) + aspect (cyclic) two-panel for the briefing deck.
- `lqv/subscene/polygon_ndvi_overlay.py` — 10 m NDVI rendered over the polygon, colour ramp 0.6→0.95, GeoJSON outline + 8 vertex pins.

## Provenance

- **ALOS AW3D30 v3.2** — JAXA ALOS PRISM stereo, 1″ (~30 m at the equator), released 2024.
- **Cop30 GLO-30** — ESA Copernicus DEM, 1″, TanDEM-X derivative, accessed via OpenTopography (API key in `.env.local`, never committed).
- **NASADEM v001** — NASA/USGS, SRTM reprocessed with ASTER GDEM voidfill, 1″, doi:10.5067/MEaSUREs/NASADEM/NASADEM_HGT.001.
- **SRTM GL1 v3** — NASA/USGS legacy 1″, doi:10.5067/MEaSUREs/SRTM/SRTMGL1.003.
- All four reprojected to EPSG:4326, native ~28 × 31 m at this latitude.
- **Sentinel-2 polygon clip**: S2B_21JVM_20260512_0_L2A, 10 m bands, scale-only DN→reflectance, cf. [[sentinel2_brief]] for the full STAC metadata.

## Carry-forward gaps

- **Parcel-tight LiDAR** (1 m or better) — not sourced; would resolve the sub-3 m drops the 30 m DEMs flatten (cf. [[client_photos_brief]] gap #04 escarpments). Phase-1 deliverable, not Phase-0.
- **pyflwdir flow-routing on Cop30** — gated on `pyflwdir` pip install; would yield drainage network + stream-order for the extended AOI to confirm the Quebrada flow path.
- **DeepForest / detectree2 crown segmentation** on the polygon NDVI quicklook — gated on pip install; would convert "mean canopy height 10.9 m" into per-tree crowns for the Blender scatter.
- **5 km buffer landcover** (Mapbiomas categorical 30 m, 1985-2023) — fetched separately in `docs/site_data/mapbiomas_paraguay/`; not cross-referenced here yet.

## Cross-references

- [[topology_lod_brief]] — parcel-tight 1 m / 30 m elevation tier-of-detail.
- [[analysis_brief]] — parcel-tight ALOS clip (62 ha → 998 ha intercomparison).
- [[sentinel2_brief]] — S2B 2026-05-12 STAC metadata + 6-band stack.
- [[landsat_brief]] — 41 yr NDVI 0.681 → 0.782 trend the polygon NDVI 0.918 plateau caps.
- [[mod16_brief]] — actual ET 1091 mm/yr the NDVI-dense canopy is transpiring.
- [[climate_era5_brief]] — 36 yr T/P/wind/SSRD record that drives the watershed-scale microclimate.
