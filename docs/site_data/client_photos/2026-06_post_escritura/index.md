# Client photo intake — 2026-06 post-escritura

> Drop folder for the on-site photos Wesley + Thijs (and any local contact) bring back from the parcel. Tied to gaps identified in `docs/post_escritura_site_knowledge.md` §6 and `docs/RESEARCH_GAPS.md` (R01 site visit, R35 drone, R37–38 partnerships).
>
> Filing convention: `NNN_<topic>_<short-desc>.{jpg,png,mp4}` — fill the table below as photos land. Add timestamps + GPS if the camera has it.

---

## Where the photos plug in

Each row of the table corresponds to a numbered **shot need**. If a photo arrives that we didn't anticipate, append a new row at the bottom with a fresh ID.

| # | Shot need | Gap it closes (from §6) | Decision it unblocks | Files | Notes |
|---|---|---|---|---|---|
| 01 | Quebrada / stream at the low end (~166 m, near Wesley's pin) — wet sections, dry sections, width, bed material, any ponding | Stream presence + flow regime | Micro-hydro feasibility; cistern siting; dengue-risk pool detection | | Aim 6–10 frames along the channel; one frame "looking upstream" + one "downstream" at each station |
| 02 | Any standing structures, ruins, foundations, fence remains, prior owner's improvements | Existing structures invisible to S-2 | Whether Phase 1 has any salvage/restore line, or starts from zero | | |
| 03 | Driveway, gate, internal paths, vehicle access points; condition in dry vs wet | Road / access (only southern boundary mapped in OSM) | Cabana siting (must be vehicle-reachable for construction); turnaround geometry | | |
| 04 | Escarpments, natural terraces, exposed bedrock, boulder fields | Sub-3 m drops flattened by 30 m DEM | Terrace design; stone-foundation sourcing on-site; lithology check | | |
| 05 | Close-ups of dominant tree species — bark, leaf, fruit, flower (if present) | Plant species ID (S-2 sees "forest", not species) | Confirms lapacho / cedro / mango / pindo distribution → render fidelity + restoration species list | | Pindo palm = drooping plumose fronds (NOT coconut); lapacho = bare hot-pink Jul–Sep, leafy rest of year |
| 06 | Views *outward* from candidate cabana sites (e.g., the flat 4.28 ha band) — what's the sightline through the canopy | View corridors (canopy blocks the satellite from telling us) | Cabana orientation; clearing strategy; "view premium" pricing claim | | One photo per cardinal direction at each candidate site |
| 07 | Power poles, water meters, well-heads, septic tanks, fence lines | Existing infrastructure (no open data) | Phase 1 utilities capex; ANDE / municipal hookup distance | | |
| 08 | Exposed rock, soil pits, soil colour, any erosion scars | Lithology + soil texture for cob feasibility | Cob mix design; foundation depth; lime vs cement defensibility | | Especially: any red-laterite vs sandstone exposures |
| 09 | Property edges + what's on the other side (adjacent finca use: pasture, plantation, forest, built) | Neighbour activity (OSM places only) | Buffering / sound / privacy strategy; biosecurity for restoration claims | | |
| 10 | Morning + evening photos showing fog, dew patterns, cool pockets | Microclimate signals (ERA5 grid is 25 km) | Bedroom siting (cool-air drainage zones); fog-collection feasibility | | If the visit is single-day, take dawn + dusk shots if at all possible |
| 11 | The "escobar wes" pin location IRL — what is it? Stream crossing? Pre-existing house plot? Gate? | Confirms what Wesley was marking | Anchor for the rest of the parcel's mental map | | |
| 12 | The ridge-top (~230 m, north-west corner of polygon) — what's the view from up there | Highest natural lookout — not visible in any open data layer | View-corridor pricing; potential restaurant / event-space site | | |
| 13 | Wildlife sign — tracks, scat, nests, calls (mp4), bird species spotted | Biodiversity baseline (GBIF coverage is sparse for the AOI) | Restoration + ecotourism narrative (R19, R20) | | |
| 14 | Anything anomalous Wesley didn't expect | (unknown unknowns) | (whatever they unblock) | | |

---

## Intake checklist (when photos arrive)

1. Copy raw files into this folder, preserving original filenames in a `_raw/` subfolder.
2. Rename working copies to `NNN_<topic>_<short-desc>.<ext>` per the table.
3. Fill the **Files** + **Notes** columns above as the photos arrive.
4. Strip EXIF GPS into a sidecar `photos_gps.csv` (lon, lat, alt, filename, timestamp) so the photos can be plotted on the polygon quicklook.
5. Update the corresponding row in `docs/RESEARCH_GAPS.md` (R01 site visit) and the relevant §6 row in `docs/post_escritura_site_knowledge.md`.
6. If any photo invalidates a satellite-derived claim (e.g., shows a clearing the NDVI missed, or a structure), flag it explicitly in `docs/DECISIONS.md` with a `2026-06-XX photo correction:` entry — don't silently rewrite the analysis.

---

## What we already know from open data (re-stated so the photos can be read against it)

- Polygon: 30.9 ha, 8 vertices, centroid `(-57.0355, -25.6073)`.
- Pin at 166.3 m AMSL — low end of the parcel (P4 of elevation distribution) → likely stream-bottom reference.
- 73.5 m relief inside polygon (157.9 → 231.5 m).
- Median slope 14.2 %; flat (<8 %) only 13.8 % of area (4.28 ha).
- 71.6 % faces S/SW (cool, sun-averted, passive-cooling-friendly).
- NDVI median 0.917 → wall-to-wall forest; no detected clearings; no detected open water.
- Nearby GEDI canopy: 27.7 m (consistent with mature secondary Atlantic Forest).
- Climate: 22 °C annual mean, 1,736 mm/yr, wet 10 mo/12, warmest month 26.8 °C (passive-cool band).

Full analysis: `docs/post_escritura_site_knowledge.md`.

---

*Folder + index created 2026-06-28 (T+1 post-escritura) by AI Whisperers. Awaiting first client photo drop.*
