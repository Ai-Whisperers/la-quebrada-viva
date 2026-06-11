# Site Data Spike — Acquiring Real Topo Data for the 62-ha Property

**Status:** living document. Describes the data-acquisition spike needed to replace the procedural terrain (`lqv/site/escarpment.py`, `lqv/site/ground.py`) with a real Digital Elevation Model (DEM) of Wesley's 62 ha in Escobar, Paraguarí.

The current scene uses a hand-crafted heightfield approximation of the cerro-stream-cliff trio. That works for stills, but the housing-park master plan, water-flow studies, micro-hydro head calculation, and solar-shadow studies all need a real DEM.

## Why now

1. **Escritura is 2026-06-27.** A real DEM lets us print accurate parcel + topo overlays for the closing meeting.
2. **Micro-hydro head** depends on actual elevation drops, not vibes. The Pelton wheel needs ≥ 8 m head to be worth installing.
3. **Solar PV summer-shadow study** needs the actual sun-blocked hours per pad.
4. **Surface-water flow** lines need to be validated before locating the second pool.
5. **8 typology pads** in `lqv/site/site_plan.py` are currently in "made-up" coordinates; a DEM lets us validate slope and orientation per pad.

## Data sources (ranked by quality/cost)

### Tier 1 — best fidelity (Wesley pays Paraguayan surveyor)

- **Topographic survey by a Paraguayan agrimensor (surveyor)** with RTK GPS:
  - 1 m horizontal resolution, 5 cm vertical resolution.
  - Property boundary + every existing structure + stream centreline + spring source + key trees.
  - Deliverable: `.dwg` + `.shp` + `.kml` + ground-control photos.
  - Cost estimate: USD 1500–3000 for 62 ha (Paraguay rates, 2026).
  - Lead time: 3–5 weeks.
  - **Recommendation:** Wesley should commission this BEFORE escritura. Notary will want a recent survey anyway.

### Tier 2 — good enough for digital twin (free, low effort)

- **SRTM 30 m DEM** (NASA + USGS) — free, ~30 m resolution.
  - Available at https://earthexplorer.usgs.gov or via Python `elevation` package.
  - License: public domain.
  - Quality: too coarse for individual building pads but OK for landscape-scale.

- **ALOS World 3D 30 m DEM** (JAXA) — free with registration.
  - Available at https://www.eorc.jaxa.jp/ALOS/en/aw3d30/
  - License: free for non-commercial AND commercial; attribution required.
  - Quality: arguably the cleanest 30 m global DEM in vegetated terrain.

- **Copernicus DEM GLO-30** (ESA) — free.
  - Available at https://spacedata.copernicus.eu/
  - License: free with attribution.

### Tier 3 — boutique higher fidelity (mid-effort)

- **OpenTopography 1–5 m DEM** for select Paraguay zones — check coverage.
- **Maxar 30 cm satellite imagery** (commercial) — for orthorectified imagery, not a DEM but useful as ground texture.
- **Sentinel-2 10 m multispectral** — free; for vegetation index analysis (NDVI), not elevation.

### Tier 4 — DIY drone survey (low cost, mid quality)

- **DJI Mavic 3 Enterprise** + Pix4D / WebODM SfM pipeline.
- 5 cm horizontal, 10 cm vertical achievable in clear weather.
- DGAC (Paraguay aviation authority) flight notification required if > 50 m.
- Cost: USD 200–400 for an on-site operator; we know one in Asunción.

## Recommended pipeline

1. **Now (pre-escritura):** download SRTM + ALOS for the 62-ha bounding box. Build a coarse procedural-replacement terrain. (Tier 2, free.)
2. **Pre-escritura (1500-3000 USD):** commission Tier 1 surveyor. Negotiate that the survey doubles as the notary's required mensura.
3. **Post-escritura:** drone survey of building-pad sites once Wesley narrows from 8 typologies to 3–4.

## Render-side integration plan

When DEM arrives:

1. Drop the GeoTIFF in `assets/site_data/escobar_dem_5m.tif` (or similar resolution).
2. `lqv/site/terrain_62ha.py::is_available()` will return True.
3. `lqv/site/terrain_62ha.py::build_terrain(parent, exaggeration=1.0)` will:
   a. Load the GeoTIFF via `rasterio` (Blender bundled, or external pip).
   b. Generate a subdivided plane mesh sized to the bounding box.
   c. Displace vertices by elevation (with optional Z-exaggeration knob).
   d. Apply a satellite-orthophoto texture as a stand-in for ground material.
4. Existing `lqv/site/escarpment.py` + `lqv/site/ground.py` become **building-pad-local** detail meshes layered ON TOP of the broad DEM.

## Coordinate-system notes

- Paraguay national CRS: **POSGAR 2007 / Argentina zone 6** (EPSG:5347) for engineering work; UTM 21S WGS84 (EPSG:32721) common in surveyors' files.
- Reproject everything to a single local Cartesian for Blender (origin at the SE corner of the building pad).
- Z = elevation a.s.l. minus a chosen datum (say 240 m a.s.l.) so Blender Z values stay in [0, ~72].

## Known property bounds (from boleto privado)

- Parcel cuenta corriente catastral: see `docs/contract_summary.md`.
- Cuatro mojones (boundary markers): NE, SE, SW, NW. Surveyor must verify each.
- Total area: 62 ha (per the boleto).
- Average slope: 8% NW→SE.

## Cross-references

- `docs/contract_summary.md` — parcel ID and registered area.
- `docs/paraguay_clay_house_research.md` — site selection rationale.
- `docs/HOUSING_PARK_CONCEPT.md` — the 8 typology pads to validate against the DEM.
- `lqv/site/site_plan.py` — current placeholder coords.
- `lqv/site/terrain_62ha.py` — render-side DEM mesher (dormant).
- `lqv/site/section_view.py` — section line that needs DEM to be accurate.

### Extended back-pointers (additive 2026-06-10)

This file has always been *referenced forward* by adjacent docs but the reverse pointers were never collected here. Listed below with *why* each back-link matters; the 6 outbound bullets above are unchanged.

- `CLAUDE.md` §"Tier-1 docs Claude must read at session start" — entry-point doc names this file as the canonical site-survey-constants source. Cold-start sessions inheriting any positional/topographic question (escarpment line, footbridge y, contour topology, water-line position) begin here. Reciprocal to ARCHITECTURE.md "Positional coupling" invariant.
- `docs/asset_plan.md` §C.1 + §C.2 — HDRI selection (Nishita sky strength + sun angle) and ground PBR selection (laterite/sandstone vs other terrain) are constrained by site_data_spike findings. This file is the empirical input; asset_plan §C is the asset-side response. Any §C revision must re-cite this file's constants.
- `docs/research_index.md` §"Tier-1 references" + §"Coordinate-system notes" + §"Survey constants" — research_index treats this file as Tier-1 reading and points to §coordinate-system-notes from the cross-reference table. Phase 7.5 procurement validates against the survey constants here before any `[USED]` flip.
- `docs/bom.md` Surveyor row (mensura — line 133) — bom.md procures the surveyor mensura *against* this file's Tier-1 spec; the line-item description names this file explicitly. bom is the cost-side response; this file is the scope spec.
- `docs/housing_park_phasing.md` §"2026-08 milestone" — surveyor mensura completion in the phasing timeline points here as the Tier-1 deliverable. Any phasing slippage must update this file's Tier-1 status.
- `docs/energy_budget.md` §"Hydro head" — the 12 m measured drop hydro spec carries a "verify after `site_data_spike` survey" caveat naming this file. Pelton turbine sizing locks once this file's hydro section closes.
- `docs/SESSION_LOG.md` tick 19 (2026-06-10) + STATUS.md §1.1 satellite block — canonical audit-trail entries for the Batch 10 Sentinel-2 + DEM + OSM + GEDI + GBIF site_data spike that landed alongside this doc. Cold-start sessions reconstruct the spike-execution state from those audit entries.
