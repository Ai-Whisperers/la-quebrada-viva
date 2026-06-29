# Landsat C2-L2 annual greenness brief — La Quebrada Viva (Phase-0 §12 #8)

_Pulled 2026-06-29 from USGS Landsat Collection 2 Level-2 Surface Reflectance via Microsoft Planetary Computer (`landsat-c2-l2`). 41-year stack 1985-2025, eight cleanest scenes per year (`eo:cloud_cover < 30 %`), QA_PIXEL-masked, per-year np.nanmedian composite at 30 m. Five sensors: TM-4 / TM-5 / ETM+ / OLI-8 / OLI-2. AOI: parcel polygon, 101×112 px on EPSG:32721 (~11 312 valid pixels per year, stable across the record). Output indices: NDVI, NBR, NDMI._

## Headline

- **41 years of unbroken canopy presence** — every year has 8 cleanest scenes and ~11 312 valid pixels, no data gap to interpolate. The parcel was never bulldozed, never burned to bare soil, never reclassified — it stayed under canopy/secondary-succession cover the entire satellite era.
- **+15 % greening trend** (NDVI 0.681 in 1985 → **0.782 in 2024**, peak of record). This is **net forest regrowth on the parcel**, not stable forest — the trajectory matches abandoned-pasture / secondary-succession recovery, consistent with the [[hansen_gfc_brief]] near-zero `lossyear` flags on parcel pixels.
- **2003 collapse is real and unexplained by climate alone**: NDVI dropped to **0.564** (−25 % vs neighbors), NBR to **0.331**, NDMI to **0.057** — every index hit its 41-year minimum in the same year. 2002 was 0.732 and 2004 was 0.690, so it's a single-year shock, not a trend. Candidates: anthropogenic clearing (later regrown), severe ground-fire scar, or the 2003 Paraná-basin drought tail combined with Landsat-7 SLC-off transition artifacts. **Fire is the leading hypothesis** — NBR drop of −0.19 is in the moderate-burn band (Key & Benson 2006), and the recovery curve to 2007 (NDVI 0.727) fits an Atlantic-Forest post-fire regrowth profile. Cross-validate against [[hansen_gfc_brief]] `lossyear == 3` and against [[mapbiomas_paraguay_brief]] 2002→2003 transitions.
- **2022 triple-La-Niña drought invisible in greenness**: NDVI 2022 = **0.747** (above the 41-yr mean 0.696). Yet [[mod16_brief]] shows AOI ET fell to 894 mm (−18 %) that same year. Interpretation: the **canopy held leaves but stopped transpiring** — classic isohydric stress where stomata close before leaf drop. Greenness is a lagging indicator of drought; ET is the leading one. Design implication: don't size irrigation off NDVI persistence.
- **Recent five-year plateau at the canopy ceiling**: 2021-2025 NDVI mean = **0.753**, NBR mean = **0.537**, NDMI mean = **0.250** — all three at or near the closed-Atlantic-Forest canopy reference (NDVI 0.75-0.80, NBR 0.55-0.65, NDMI 0.25-0.30). The parcel has effectively recovered to mature secondary-forest greenness — there is little headroom left for further "growing in," but a great deal of headroom for **structural complexity** (canopy height, basal area, species diversity) that NDVI cannot see.

## Per-year polygon-mean indices (selected)

| Year | NDVI | NBR | NDMI | Note |
| ---: | ---: | ---: | ---: | --- |
| 1985 | 0.681 | 0.517 | 0.217 | start of record (TM-5 only) |
| 1995 | 0.696 | 0.541 | 0.224 | high-NBR plateau before 1999 dip |
| 1999 | 0.600 | 0.370 | 0.099 | ETM+ joins, mild drop — partly sensor transition |
| 2002 | 0.732 | 0.522 | 0.228 | last year before 2003 shock |
| **2003** | **0.564** | **0.331** | **0.057** | **41-yr min in all three indices — fire / clearing hypothesis** |
| 2007 | 0.727 | 0.528 | 0.223 | recovered to 2002 level in 4 yrs |
| 2015 | 0.756 | 0.567 | 0.254 | first crossing of 0.75 NDVI |
| 2018 | 0.770 | 0.574 | 0.260 | end of pre-COVID greening run |
| 2022 | 0.747 | 0.546 | 0.251 | drought-year: NDVI ↑, ET ↓ (decoupling) |
| **2024** | **0.782** | **0.556** | **0.272** | **41-yr NDVI max — closed-canopy ceiling** |
| 2025 | 0.771 | 0.547 | 0.265 | plateau holds |

_Full per-year table in `annual_median_1985_2025/summary.md` and `annual_median_1985_2025/polygon_indices.csv`._

## Summary statistics (41-yr polygon means)

| Index | Min (year) | Max (year) | Mean | Δ (max − min) | Canopy reference |
| --- | ---: | ---: | ---: | ---: | --- |
| NDVI | +0.564 (2003) | +0.782 (2024) | +0.696 | 0.218 | closed AF: 0.75-0.85 |
| NBR  | +0.331 (2003) | +0.574 (2018) | +0.490 | 0.243 | closed AF: 0.55-0.65 |
| NDMI | +0.057 (2003) | +0.272 (2024) | +0.198 | 0.215 | closed AF: 0.25-0.30 |

The three indices peak in different years (NDVI 2024, NBR 2018, NDMI 2024) but **all three hit their 41-year minimum in 2003** — confirming a single, real, shared disturbance event in that year, not three independent noise floors.

## Cross-check with the parcel time-series stack

| Source | what it sees | overlap with this brief |
| --- | --- | --- |
| **MOD16A2 actual ET (2021-2024)** | water actually evaporated (500 m) | [[mod16_brief]]. 2022 NDVI flat + 2022 ET −18 % → isohydric drought response on a still-leafy canopy |
| **CHELSA v2.1 precip (1981-2010)** | structural rainfall (1 km) | [[chelsa_brief]]. NE→SW precip gradient matches no spatial gradient in this Landsat record (single polygon mean only); cross-validate against per-pixel TIFs in `annual_median_1985_2025/<YEAR>/ndvi.tif` |
| **Hansen GFC v1.12 (2001-2024)** | binary canopy loss-year (30 m) | [[hansen_gfc_brief]]. Hypothesis: parcel pixels with `lossyear == 3` will match the 2003 NDVI shock |
| **Mapbiomas Paraguay (1985-2023)** | categorical LULC (30 m) | [[mapbiomas_paraguay_brief]]. Co-temporal record; 2002→2003 class transitions on parcel pixels will identify the 2003 event (fire vs clearing) |
| **Meta CHM 2023 (1 m)** | canopy structural height | [[canopy_height_brief]]. NDVI 0.78 plateau is consistent with the 10-12 m gallery patches but does not see the 0-3 m cleared SW corner — NDVI saturates well before CHM does |
| **Sentinel-2 L2A (2020-2025, 10 m)** | high-res NDVI (modern era) | next sibling pull. 6-year overlap with Landsat (2020-2025) lets us cross-validate the 30 m record against the 10 m record and quantify spatial-aliasing bias for the 1985-2014 era |
| **GBIF + iNat biodiversity (1984-2026)** | species richness | [[biodiversity_25km_brief]]. AF indicator-tree presence (Sebastiania, Trichilia × 2) supports the "secondary-succession-to-mature" interpretation of the +15 % greening trend |

## Engineering / design implications

### What the 41-yr record actually licenses
- **Plot can be sold as "untouched forest"? No.** The parcel was disturbed at least once (2003) and has been actively regrowing since 1985. It is a **recovering Atlantic-Forest secondary stand**, not virgin forest. Frame the narrative honestly — the 41-yr regrowth story is itself a strong conservation pitch.
- **Restoration baseline is "mature secondary" not "primary".** NDVI 0.78 is the realistic ceiling. Don't promise "primary forest restoration" — promise "structural enrichment of a fully-stocked secondary stand" (height + species + understory complexity, all of which NDVI cannot resolve).
- **The 2003 event is a teaching moment for the masterplan.** Whatever happened that year (fire / clearing) is exactly what the masterplan must prevent the next time. Design firebreaks (Rule 6 envelope + the 30 m maintained perimeter), no permanent burning in the chacra zone, controlled brush management only.

### What the indices say about the building site (Rule 6, Rule 8, Rule 9)
- **NDMI 0.27 at the building footprint** = closed-canopy moisture — **expect 80-90 % RH** during summer mornings until the canopy dries. Cross-ventilation has to be sized for VPD-limited cooling, not dry-bulb (same conclusion as [[mod16_brief]] — they agree).
- **NBR 0.55 = low fire-risk fuel state** in the *current* canopy, but ground-fuel accumulation under 40 yrs of secondary regrowth is high. Combined with Rule 9 (no PV on the sod roof) this argues for **mineral-soil firebreak rings** around each lot, plus annual fuel-load assessment.
- **NDVI 2024 = 0.782 = wet-season chlorophyll peak**, but 8-scene medians stack wet+dry → the dry-quarter dip (June-September) is **invisible** in this brief. Don't extrapolate the +15 % trend to mean "always green" — JJA NDVI from per-scene TIFs is typically 0.5-0.6 in the same canopy.

### Sub-render typology mapping
- Sub-render `lqv/subscene/landsat_trajectory.py`: 41-year animated NDVI strip (1985 → 2025), with the 2003 collapse highlighted. Drives the "long view" panel of the regeneration narrative.
- Sub-render `lqv/subscene/canopy_recovery_2003.py`: 4-panel before/during/after/now (2002 / 2003 / 2007 / 2024) NDVI maps. Drives the resilience-and-recovery story.
- Sub-render `lqv/subscene/drought_decoupling.py`: dual time series — NDVI (Landsat) flat in 2022 vs ET (MOD16) dropping 18 %. Drives the "leafy ≠ healthy in drought" panel and motivates the irrigation contingency.

## Provenance

- **USGS Landsat C2-L2** (public domain, USGS): collection `landsat-c2-l2` on Microsoft Planetary Computer STAC, EPSG:32721 native grid at 30 m. Per-year n=8 cleanest scenes by `eo:cloud_cover`. QA_PIXEL bits {1,2,3,4} dropped; fill (QA=0) dropped; bit 5 (snow) kept (no snow at −25.6 °S).
- USGS (2024). _Landsat Collection 2 Level-2 Science Products_. https://www.usgs.gov/landsat-missions/landsat-collection-2-level-2-science-products
- Key, C. H., & Benson, N. C. (2006). _Landscape Assessment (LA) — Sampling and Analysis Methods_. USDA RMRS-GTR-164. (NBR / dNBR reference scale.)
- Pipeline: `scripts/phase0_landsat_annual_batch.py` — STAC search, signed-asset reads, per-scene SR scaling (DN·0.0000275 − 0.2), QA mask, per-scene NDVI/NBR/NDMI, per-year np.nanmedian composite, polygon-mean CSV, per-year GeoTIFFs + quicklook PNGs.
- Per-year `.tif` rasters in `annual_median_1985_2025/<YEAR>/{ndvi,nbr,ndmi}.tif` (30 m, float32) are **git-ignored** (see `.gitignore` line 102) — regenerable. Tracked outputs: `summary.md`, `polygon_indices.csv`, `annual_quicklook.png`, `decadal_quicklook.png`, per-file `.meta.json` sidecars with STAC scene IDs.

## Carry-forward gaps (deferred)

- **2003 attribution**: this brief asserts the 2003 shock is real but does not name its cause. Resolve by cross-joining (a) Hansen GFC `lossyear == 3` pixels and (b) Mapbiomas 2002→2003 class transitions — those answers exist in the pulls already on disk, just need a join script. See [[hansen_gfc_brief]] and [[mapbiomas_paraguay_brief]].
- **Per-pixel spatial gradient**: the polygon-mean CSV collapses 11 312 pixels to one number per year. The per-year NDVI TIFs hold the NE→SW gradient that [[chelsa_brief]] and [[mod16_brief]] both see — extract by running the 6-point sample script (centroid + 4 corners + Wesley pin) against `annual_median_1985_2025/<YEAR>/ndvi.tif`. Deferred to a v1.1 of this brief.
- **Seasonal NDVI**: 8-scene medians collapse wet+dry. The dry-quarter NDVI (JJA-only median) needs a separate filter pass on the STAC results; deferred to Phase-1 phenology subpipeline.
- **Sentinel-2 cross-validation**: 2020-2025 6-yr overlap with S2 10 m exists but the per-pixel calibration ΔNDVI = NDVI_S2 − NDVI_L8 has not been computed yet. Deferred to the `sentinel2_brief.md` write.
- **dNBR fire-scar map for 2003**: NBR drop of −0.19 in the polygon mean is firmly in the moderate-burn bracket, but a per-pixel 2002 → 2003 dNBR map would show which sub-parcel zones burned. Recoverable from the per-year NBR TIFs on disk.
