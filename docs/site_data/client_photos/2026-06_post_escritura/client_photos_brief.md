# Client photo intake brief — La Quebrada Viva (Phase-0 §12 v1)

> **Empty-pending-photos intake state.** Wesley + Thijs are the first
> human eyes on the parcel post-escritura (2026-06-27). This brief
> mirrors the 14 numbered shot-needs in `index.md` and ties each one to
> the satellite-derived claim it confirms or invalidates. Until photos
> arrive, every row below is a *gap*, not data.

## Headline

- **0 photos landed** as of 2026-06-29 (T+2 post-escritura). All 14 shot-needs still open.
- **First on-site visit pending** — depends on Wesley + Thijs scheduling and Paraguay weather window.
- **14 shot-needs frame R01 (site visit) + R35 (drone) + R37–38 (partnerships)** of `RESEARCH_GAPS.md`.
- **Each shot-need closes one satellite-blind claim** (sub-pixel hydrology, sub-3 m grade, species ID under canopy, infrastructure presence) and unblocks one Phase-1 engineering decision.
- **Photos that arrive without GPS** must still be sorted by shot-need ID; EXIF stripping into `photos_gps.csv` is opportunistic, not required.

## Polygon facts being photographed (load-bearing context)

| Field | Value | Source |
| --- | --- | --- |
| Parcel | 30.9 ha, 8 vertices | [[post_escritura_site_knowledge]] §1 |
| Centroid | (−57.0355, −25.6073) | [[post_escritura_site_knowledge]] §1 |
| Wesley's pin | 166.3 m AMSL (low end, P4 elev) | [[post_escritura_site_knowledge]] §2 |
| Relief | 73.5 m (157.9 → 231.5 m) | [[post_escritura_site_knowledge]] §2 |
| Slope median | 14.2 % | [[post_escritura_site_knowledge]] §2 |
| Flat (<8 %) | 13.8 % = 4.28 ha | [[post_escritura_site_knowledge]] §2 |
| S/SW-facing | 71.6 % | [[post_escritura_site_knowledge]] §2 |
| NDVI median | 0.917 | [[sentinel2_brief]] / [[extended_aoi_brief]] |
| GEDI canopy | 27.7 m mean | [[canopy_chm_brief]] |
| Climate | 22 °C / 1 736 mm/yr | [[climate_era5_brief]] |
| Nearest neighbour | 196 m centroid-distance | [[infrastructure_brief]] |

## Shot-need register (14 rows — index.md mirror with engineering hooks)

| # | Shot need | Satellite-blind claim it tests | Phase-1 decision it unblocks | Status |
| ---: | --- | --- | --- | --- |
| 01 | Quebrada channel — wet/dry sections, width, bed material, ponding | "Zero open water at S-2 10 m" ([[sentinel2_brief]]) — is the channel actually a wet swale or a dry gully? | Micro-hydro feasibility; cistern siting; dengue-risk pool detection | open |
| 02 | Standing structures, ruins, foundations, fences | Building footprints in [[infrastructure_brief]] flag *none* inside polygon — verify | Phase-1 salvage/restore vs greenfield split | open |
| 03 | Driveway, gate, internal paths; wet vs dry condition | OSM only maps southern boundary | Cabana siting (vehicle reach for construction); turnaround geometry | open |
| 04 | Escarpments, terraces, exposed bedrock, boulders | 30 m ALOS smooths sub-3 m drops ([[extended_aoi_brief]]) | Terrace design; stone-foundation sourcing; lithology check | open |
| 05 | Dominant tree species — bark, leaf, fruit, flower | S-2 sees "forest" not species ([[sentinel2_brief]]) | Lapacho / cedro / mango / pindo distribution → render fidelity + restoration species list | open |
| 06 | Outward views from candidate cabana sites (flat 4.28 ha band) | Canopy hides ground-level sightlines from satellite | Cabana orientation; clearing strategy; "view premium" pricing claim | open |
| 07 | Power poles, water meters, well-heads, septic, fence lines | No open data on utilities | Phase-1 utilities capex; ANDE / municipal hookup distance | open |
| 08 | Exposed rock, soil pits, soil colour, erosion scars | Lithology + soil texture for cob feasibility | Cob mix design; foundation depth; lime vs cement defensibility | open |
| 09 | Property edges + adjacent finca use | OSM places only | Buffering / sound / privacy strategy; biosecurity for restoration | open |
| 10 | Morning + evening fog, dew, cool pockets | ERA5 grid is 25 km — microclimate is invisible | Bedroom siting (cool-air drainage); fog-collection feasibility | open |
| 11 | The "escobar wes" pin location IRL | Confirms what Wesley marked at 166.3 m | Anchor for the rest of the parcel's mental map | open |
| 12 | Ridge-top (~230 m NW corner) — view from up there | Highest natural lookout, not in open data | View-corridor pricing; restaurant / event-space site | open |
| 13 | Wildlife sign — tracks, scat, nests, calls (mp4), bird IDs | GBIF coverage is sparse for the AOI | Restoration + ecotourism narrative (R19, R20) | open |
| 14 | Anomalies Wesley didn't expect | Unknown unknowns | TBD | open |

## Engineering implications (what photos will unlock)

- **#01 + #11 settle the Quebrada question.** [[sentinel2_brief]] confirms zero open water at 10 m; [[hydrogeology_brief]] sketches the flow path. Photos decide whether the Blender hero shot needs a perennial stream, an ephemeral creek, or a dry swale with gallery-forest vegetation.
- **#04 settles the escarpment question.** ALOS 30 m smooths anything <3 m vertical — if Wesley's photos reveal a step-cliff, the parcel-tight DEM mesh needs hand-editing or a 1 m LiDAR upgrade ([[topology_lod_brief]]).
- **#05 + #13 swap the placeholder species in `lqv/scatter_*.py` for canon.** Lapacho / piquillín / tajy are currently scattered uniformly; per-zone species rules need ground truth.
- **#06 + #12 set the hero-camera frustum.** Currently arbitrary; sightline photos decide what the camera should actually frame.
- **#07 sets Phase-1 utilities capex.** The MS Buildings layer ([[infrastructure_brief]]) shows nothing inside the polygon, but doesn't catch power infrastructure.
- **#08 sets the cob mix.** Soil colour + texture + exposed rock decide whether the cob walls in Rule 8 ("culturally Paraguayan, not Tuscan / Bali / Earthship") are feasible at all without trucked-in clay.
- **#10 is the only photo set that needs *two visits* in one day** — fog + dew patterns can't be reconstructed from a single midday photo.
- **#02 + #14 are the "what we don't know we don't know" rows.** Treat anything reported here as immediately corrective of `post_escritura_site_knowledge.md`, not additive.

## Sub-render typology

- `lqv/subscene/photo_overlay_polygon.py` — once `photos_gps.csv` lands, render the 8-vertex polygon outline with a coloured pin per shot-need ID at its GPS coordinate; pin colour = `status` (open=grey, landed=green, anomaly=red).
- `lqv/subscene/photo_panel.py` — 14-cell grid panel for the deck appendix, one cell per shot-need; empty cells render as a hatched "pending" placeholder.
- `lqv/subscene/photo_contradiction_flag.py` — only fires if `DECISIONS.md` carries a `2026-06-XX photo correction:` entry; renders the corrected polygon overlay against the prior NDVI / DEM claim.

## Provenance

- Folder + index created 2026-06-28 by AI Whisperers (T+1 post-escritura).
- Filing convention: `NNN_<topic>_<short-desc>.{jpg,png,mp4}`, raw originals under `_raw/`.
- EXIF GPS → `photos_gps.csv` (lon, lat, alt, filename, timestamp).
- Intake checklist (6-step) lives in `index.md` §Intake checklist — do not duplicate.
- Photo arrival triggers update to `RESEARCH_GAPS.md` R01 + the matching row in `post_escritura_site_knowledge.md` §6.
- Any photo that invalidates a satellite-derived claim → `DECISIONS.md` `2026-06-XX photo correction:` entry; never silently rewrite the analysis.

## Carry-forward gaps

- **Scheduling** — site visit date not yet set with Wesley + Thijs. Weather window: prefer May–Sep (dry season) for stream-bed exposure and ground-level photography.
- **Drone footage (R35)** — separate intake. Drone orthophoto would solve #04 + #12 + #06 in a single sortie. Not in this brief.
- **GPS-less camera fallback** — if photos arrive without EXIF GPS, sort by shot-need ID only; do not synthesize coordinates.
- **Single-day visit constraint** — if Wesley + Thijs visit only once, prioritise #01 / #04 / #05 / #07 / #11 over #06 / #10 / #12 (the latter need either time-of-day variation or specific high-points that need scouting).
- **Bilingual captions** — original captions will be voseo PY ES; add EN gloss in the **Notes** column for client deck consumption.
- **Annotation pass** — once photos land, a follow-up pass annotates each frame with the satellite-derived overlay it confirms or contradicts.

## Cross-references

- [[post_escritura_site_knowledge]] §6 — the 14 gaps this intake closes.
- [[sentinel2_brief]] — "zero open water at 10 m" claim photo #01 tests.
- [[extended_aoi_brief]] — sub-3 m DEM smoothing photo #04 tests.
- [[infrastructure_brief]] — building / utility coverage photos #02 + #07 verify.
- [[canopy_chm_brief]] — Meta CHM 1 m mean 10.9 m canopy height photos #05 + #06 confirm at species level.
- [[topology_lod_brief]] — parcel-tight 1 m LiDAR Phase-1 deliverable the escarpment photos motivate.
- [[hydrogeology_brief]] — flow-routing prediction the Quebrada photos validate.
