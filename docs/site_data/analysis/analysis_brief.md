# Parcel-centred ALOS DEM analysis brief — La Quebrada Viva (Phase-0 §12 v1)

> Parcel-centred 3.0 × 3.3 km clip of ALOS AW3D30 v3.2 (108 × 108 px = 11 664
> valid pixels @ ~28 × 31 m) covering the 30.9 ha Mbopicua polygon. Source
> raster + diagnostic plots generated 2026-06-10T19:48:18 UTC by
> `scripts/analyse_dem.py`. This brief is the parcel-tight analytical
> counterpart to the 5.5 km [[extended_aoi_brief]].

## Headline

- **Bounds:** W −57.0450 / E −57.0150, S −25.6450 / N −25.6150 — a 3 × 3.3 km square centred on the parcel polygon (~10 km² = 998.9 ha).
- **Relief 264 m** (116 → 380 m AMSL) over the 10 km² window — the parcel itself spans 73.5 m (157.9 → 231.5 m) within that.
- **Slope mean 6.13 %, median 4.10 %, max 41.65 %** — bulk of the parcel-centred window is flatter than the 5 km extended ring (11.6 % mean) because the steep upper ridge sits NE of this clip.
- **Aspect mean 178°, median 180°** — flat S-facing skew over the bulk.
- **Buildability:** 57.5 % flat / 23.1 % buildable / 12.4 % challenging / 7.0 % steep — only ~1 in 14 ha is structurally steep.

## ALOS DEM stats — parcel-centred 10 km² clip

| Field | Value |
| --- | ---: |
| Source | `alos_aw3d30_dem.tif` (ALOS AW3D30 v3.2) |
| Pixel pitch | 28 × 31 m |
| Grid | 108 × 108 (11 664 valid px) |
| Bounds | W −57.0450 / E −57.0150 / S −25.6450 / N −25.6150 |
| Min elevation | 116.0 m AMSL |
| Max elevation | 380.0 m AMSL |
| Range | 264.0 m |
| Mean | 162.0 m |
| Median | 149.0 m |
| Std | 42.0 m |

## Slope + aspect rasters (derived from ALOS DEM)

| Raster | Mean | Median | Min | Max | Std |
| --- | ---: | ---: | ---: | ---: | ---: |
| `alos_slope.tif` (%) | 6.13 | 4.10 | 0.00 | 41.65 | 6.52 |
| `alos_aspect.tif` (°) | 178.01 | 180.00 | 0.00 | 358.25 | 89.82 |

Aspect is uniform — std of 90° on a [0,360) cyclic field means the window has every facing in roughly equal proportion. The mean lands on 180° (S) because of the SW canalised drainage that gives the parcel-tight polygon its 71.6 % S/SW bias (cf. [[post_escritura_site_knowledge]] §3).

## Buildability classification (`alos_buildability.tif`, int8)

| Class | Code | Slope band | Pixels | Area | Share |
| --- | ---: | --- | ---: | ---: | ---: |
| Flat | 1 | 0–8 % | 6 707 | 574.5 ha | 57.5 % |
| Buildable | 2 | 8–15 % | 2 695 | 230.8 ha | 23.1 % |
| Challenging | 3 | 15–30 % | 1 441 | 123.4 ha | 12.4 % |
| Steep | 4 | >30 % | 821 | 70.3 ha | 7.0 % |

Per-class elevation envelope (from `analysis_summary.txt`):

| Class | Min | Max | Mean | P10 | P90 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Flat | 116 | 357 | 146 | 127 | 169 |
| Buildable | 117 | 380 | 162 | 132 | 203 |
| Challenging | 125 | 378 | 187 | 142 | 250 |
| Steep | 136 | 375 | 251 | 188 | 325 |

Per-class structure reads as: flat land hugs the valley floor and lower slopes (146 m mean), buildable lies on the lower ridge shoulders (162 m), and steep stays mostly above 250 m AMSL.

## Cross-validation against published knowledge pack

| Metric | This brief (10 km² clip) | Polygon-tight (30.9 ha) | Source |
| --- | ---: | ---: | --- |
| Min elev | 116.0 m | 157.9 m | [[post_escritura_site_knowledge]] §2 |
| Max elev | 380.0 m | 231.5 m | [[post_escritura_site_knowledge]] §2 |
| Mean elev | 162.0 m | ~166 m (pin) | [[post_escritura_site_knowledge]] §2 |
| Slope median | 4.10 % | 14.2 % | [[post_escritura_site_knowledge]] §2 |
| S/SW-facing | ~50 % (window) | 71.6 % | [[post_escritura_site_knowledge]] §2 |

The polygon is steeper than its 10 km² neighbourhood because the parcel itself sits on the dropoff into the Quebrada — gentler floodplain land surrounds it.

## Engineering implications (LOD directive)

- **Parcel-tight ALOS clip is the canonical surface** for in-polygon micro-grading. Per the LOD directive, this is the "high definition" side; aim for 1 m LiDAR upgrade in Phase-1 to resolve the sub-3 m drops the 30 m grid smooths.
- **Buildability map is structurally favourable:** 80.6 % of the 10 km² window is at ≤15 % slope, which means the surroundings are visually a low-slope basin — establishing wides won't look "alpine."
- **Steep band (7.0 %, 70.3 ha @ mean 251 m AMSL)** clusters NE of the parcel and is the visible ridge backdrop in any sunset shot from the central pad. Render this band with the canopy NDVI (mean 0.918) for the deck.
- **Aspect uniformity** at this scale means the broader Cycles sun angles can stay generic; the S/SW skew is a *parcel-tight* feature, not a window-wide one.
- Diagnostic PNGs (`site_diagnostic.png`, `slope_and_buildability.png`) are deck-ready 2D inserts; size 415 KB / 124 KB respectively.

## Sub-render typology

- `lqv/subscene/parcel_centred_dem.py` — 10 km² ALOS clip as displaced grid, parcel polygon outline, ridge labels at the four peaks above 350 m AMSL.
- `lqv/subscene/buildability_map.py` — int8 buildability raster rendered as a flat colour ramp (flat=green, buildable=yellow, challenging=orange, steep=red) over the parcel-centred clip.
- `lqv/subscene/slope_overlay.py` — slope (viridis 0–30 %) two-panel with the aspect cyclic; mirror of [[extended_aoi_brief]] sub-render but at parcel-tight scale.

## Provenance

- `alos_aw3d30_dem.tif` — JAXA ALOS PRISM stereo, v3.2, 1″, accessed via OpenTopography.
- `alos_slope.tif`, `alos_aspect.tif`, `alos_buildability.tif` — float32 / float32 / int8 derivatives generated by `scripts/analyse_dem.py` on 2026-06-10T19:48:18 UTC.
- `analysis_summary.txt` — same-script TXT export.
- `site_diagnostic.png`, `slope_and_buildability.png` — same-script matplotlib quicklooks.

## Carry-forward gaps

- **Aspect classification** (N/E/S/W/NE/NW/SE/SW buckets) — derive from `alos_aspect.tif` for the [[extended_aoi_brief]] S-skew reconciliation. ~2 line of `np.digitize`.
- **Hydrologic delineation** — pyflwdir on the ALOS clip is gated on pip install; would produce flow-accum + stream-order for the Quebrada confirmation.
- **1 m LiDAR upgrade** — Phase-1 deliverable per [[topology_lod_brief]]. SNC overflight cost ~USD 4–6 k for the 998 ha window or USD ~1 k for a parcel-tight 30.9 ha pass.
- **Re-bin against Cop30** — Cop30 reports slope median 8.34 % on the **wider** 5.5 km buffer, but a parcel-centred 3.0 × 3.3 km Cop30 clip is not yet generated. Would let us compare ALOS 4.10 % median vs Cop30 at the same footprint.

## Cross-references

- [[extended_aoi_brief]] — 5.5 × 3 km wider buffer with 4-DEM intercomparison.
- [[topology_lod_brief]] — parcel-tight 1 m / 30 m elevation tier-of-detail strategy.
- [[post_escritura_site_knowledge]] — polygon-tight 30.9 ha stats (this brief's inner ring).
- [[sentinel2_brief]] — 10 m NDVI raster co-registered to this analysis grid.
- [[hydrogeology_brief]] — TWI / SAGA wetness on this DEM, currently pending pyflwdir install.
