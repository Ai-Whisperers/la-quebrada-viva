# Property map v2 — data sources to pull (data-first, not tool-first)

> Companion to `property_map_v2_tooling.md`. Where the tooling doc lists *software*, this lists the **specific datasets, registries, herbaria, agencies, and references** we should pull from to make every layer of the map accurate and complete *before* any 3D rendering. Audience: Ivan + Claude in autonomous-work mode, T+1 post-escritura.

**v1 (e3d8cce) data inventory:** Sentinel-2 NDVI (single date), Cop30 DEM 30 m, OSM Overpass. That's it. The KML polygon, the partner pin, the forest screenshot. Everything else is gap.

**Goal of this doc:** make every claim in `property_map.png` defensible from public-record evidence, AND seed the v3 dataset list with everything needed to make a 3D twin that is **factually correct**, not just pretty.

The doc is organised by data domain. Each domain ends with a **`pull_list`** — the specific actions for Phase-0 acquisition (mostly free, mostly today).

---

## 1. Canopy data — beyond Sentinel-2 single date

### 1.1 Free imagery for canopy mapping
| Dataset | Resolution | Cadence | Where to get it | Why we need it |
|---|---|---|---|---|
| **NICFI Planet basemap (tropical)** | 4.77 m RGB+NIR | Monthly since 2020-09 | https://www.planet.com/nicfi/ → free academic/research access | **Single biggest jump** over S2 — 4.5× linear resolution, resolves crown clusters at ~10 m, individual canopy gaps |
| **Sentinel-2 L2A time series 2017–** | 10 m | 5 days | AWS Open Data `s3://sentinel-cogs/`, GEE `COPERNICUS/S2_SR_HARMONIZED` | Phenology — dry-season die-back vs evergreen, deciduous lapacho leafing-out window |
| **Sentinel-1 GRD VV/VH** | 5×20 m | 6–12 days | GEE `COPERNICUS/S1_GRD` | Cloud-penetrating canopy structure proxy, biomass under cloud cover |
| **Landsat Collection 2 (1984–)** | 30 m optical, 100 m thermal | 16 days | USGS EarthExplorer / GEE `LANDSAT/LC09/C02/T1_L2` | 40-year canopy change history (the property *before* current cattle clearing) |
| **MODIS Terra/Aqua MOD13Q1 NDVI** | 250 m | 16-day composites | GEE `MODIS/061/MOD13Q1` | 24-year continuous baseline; multi-decadal phenology |
| **ALOS PALSAR-2 L-band SAR annual mosaic** | 25 m | Annual since 2007 | https://www.eorc.jaxa.jp/ALOS/en/dataset/palsar2_l4_e.htm | L-band penetrates canopy → biomass/structure layer S2 cannot give |
| **GEDI L2A/L2B (already researched)** | 25 m footprint | 2019–2023 | LP DAAC, GEE `LARSE/GEDI/GEDI02_A_002_MONTHLY` | Spaceborne LiDAR — canopy height, vertical structure footprints |
| **GLAD ARD (UMD)** | 30 m | 16 days, 1997– | https://glad.umd.edu/dataset/ard | Cleanest Landsat archive, climate-corrected |
| **Sentinel-5P TROPOMI** | 7×3.5 km | Daily | GEE `COPERNICUS/S5P/OFFL/L3_NO2` | NO₂ / CH₄ — useful for regional context, e.g. burning/clearing nearby |
| **Hansen Global Forest Change v1.11** | 30 m | Annual 2000– | https://earthenginepartners.appspot.com/google.com/science-2013-global-forest | Year-of-tree-loss raster — every cleared cell since 2000 |
| **JRC Tropical Moist Forests** | 30 m | Annual | https://forobs.jrc.ec.europa.eu/TMF/ | Disturbance/degradation distinct from clearing |
| **Mapbiomas Chaco / Paraguay** | 30 m | Annual since 1985 | https://chaco.mapbiomas.org/ + https://paraguay.mapbiomas.org/ | **Paraguay-specific** land-cover series, ground-truthed regionally |

### 1.2 Pre-built canopy / biomass products
| Product | Resolution | Coverage | Source |
|---|---|---|---|
| **ESA WorldCover 2020/2021** | 10 m | Global | https://esa-worldcover.org/ |
| **Dynamic World** (Google) | 10 m | Global, near-real-time | GEE `GOOGLE/DYNAMICWORLD/V1` |
| **Copernicus Global Land Cover (CGLS)** | 100 m | Global, 2015– | GEE `COPERNICUS/Landcover/100m/Proba-V-C3/Global` |
| **WRI Global Land Cover** | 30 m | Global | https://www.wri.org/ |
| **WCMC Carbon Pools** | 300 m | Global | UN Biodiversity Lab |
| **CCI Biomass (ESA)** | 100 m | Global, 2010, 2017, 2018, 2020 | https://climate.esa.int/en/projects/biomass/ |
| **GlobBiomass (JAXA + ESA)** | 100 m | Global, 2010 | http://globbiomass.org/ |
| **Spawn et al. 2020 biomass** | 300 m | Global, 2010 | https://daac.ornl.gov/cgi-bin/dsviewer.pl?ds_id=1763 |
| **PALSAR Forest/Non-Forest** | 25 m | Global, annual | https://www.eorc.jaxa.jp/ALOS/en/palsar_fnf/fnf_index.htm |

### 1.3 Targeted Paraguay forest products
| Product | Source |
|---|---|
| **INFONA forest cover maps (2005, 2011, 2017, 2020, 2023)** | INFONA (Instituto Forestal Nacional) — https://www.infona.gov.py |
| **WWF Paraguay Atlantic Forest Atlas** | https://www.wwf.org.py/que_hacemos/conservacion/bosque_atlantico/ |
| **Guyra Paraguay Atlantic Forest annual monitoring** | https://guyra.org.py — monthly clearing alerts |
| **Mapbiomas Bosque Atlántico** | https://atlanticforest.mapbiomas.org/ |
| **AAPF (Asociación Atlantic Forest)** annual deforestation report | https://www.atlanticforest.org/ |

### `pull_list` for §1
1. GEE auth (`earthengine authenticate` — already noted in tooling doc).
2. NICFI basemap signup (free for tropical research).
3. Pull `LANDSAT/LC09/C02/T1_L2` 1985–2025 annual median over AOI → animated GIF of 40-year canopy change.
4. Pull `MODIS/061/MOD13Q1` 2000–2025 NDVI → monthly phenology line for the polygon.
5. Pull ALOS PALSAR-2 2018–2024 annual L-band mosaic → biomass-proxy heatmap.
6. Pull Hansen tree-loss raster, intersect with polygon → year-of-loss map.
7. Pull Mapbiomas Paraguay 1985–2024 annual land-cover → time-stack PNG.
8. Pull INFONA 2005/2011/2017/2020/2023 forest cover Paraguay → cross-check against §1 above.
9. Output: `docs/site_data/property_map/canopy_history/` with 5 derived rasters + 1 timeline PNG.

---

## 2. Tree identification — species-level data

### 2.1 Regional species reference databases
| Resource | What's in it | URL |
|---|---|---|
| **Tropicos (Missouri Botanical Garden)** | Taxonomic backbone, ~1.3 M species records | https://www.tropicos.org |
| **Flora del Paraguay** (Spichiger, Mereles, Pirie, Ramella series) | Multi-volume monograph; the canonical taxonomy | Conservatoire et Jardin botaniques de Genève (CJBG) catalogue |
| **GBIF Paraguay occurrences** | 1.4 M+ geotagged records — every observation ever logged | https://www.gbif.org/country/PY/ |
| **iNaturalist Paraguay** | Citizen-science observations w/ photos | https://www.inaturalist.org/places/paraguay |
| **iNaturalist Bosque Atlántico project** | Atlantic Forest–scoped observations | https://www.inaturalist.org/projects/bosque-atlantico-interior-paraguay |
| **Pl@ntNet (cross-tropical)** | 30k+ identifications/day; per-species reference photos | https://identify.plantnet.org/ |
| **Atlantic Forest Tree Database** (Lima, Souza, Murray-Smith) | 5,166 tree species records; CSV download | https://www.scielo.br/j/bn/a/MhfBzj9KdgKMYpyXqVw3CCD/?lang=en |
| **Reflora Virtual Herbarium (Brazil)** | 4 M+ herbarium specimens from Brazilian Atlantic Forest | https://reflora.jbrj.gov.br |
| **Encyclopaedia of Life (EOL)** | Per-species pages with photos + traits | https://eol.org |
| **WorldFlora R package** | Taxonomic resolution against accepted World Flora Online list | CRAN `WorldFlora` |
| **TRY Plant Trait Database** | Functional traits (leaf area, wood density) for ~300k species | https://www.try-db.org |
| **BIEN (Botanical Information and Ecology Network)** | New World species ranges + traits | https://bien.nceas.ucsb.edu |

### 2.2 Expected genera at La Quebrada Viva (Upper Paraná Atlantic Forest, BSAU)
**Reference for "what should be there"** — anchored to biome literature + INFONA forest typology + Guyra Paraguay monitoring + GBIF occurrence density within 10 km of the polygon:

| Genus / common name | Likelihood | Why |
|---|---|---|
| *Handroanthus* (lapacho, yvyra-pytã) | Very high | INFONA emblematic, present across BSAU mature canopy |
| *Cordia* (peteribí) | High | Common Atlantic Forest hardwood |
| *Cedrela fissilis* (cedro) | High but logged | Historically dominant, frequently selectively cut |
| *Aspidosperma* (palo rosa, quebracho blanco) | High | Calcareous-soil tolerant |
| *Peltophorum dubium* (yvyrá-pytã/cañafístola) | High | Pioneer hardwood |
| *Chrysophyllum gonocarpum* (aguaí) | High | Mid-canopy common |
| *Balfourodendron riedelianum* (guatambú) | High | Common timber tree |
| *Inga* spp. (ingá) | Very high | N-fixing pioneer, watercourse banks |
| *Syagrus romanzoffiana* (pindo palm) | Very high | Signature understorey palm |
| *Euterpe edulis* (palmito) | Possible | Heavily harvested, mostly remnant |
| *Cecropia* spp. (ambay) | Very high | Disturbance pioneer — abundant in regrowth |
| *Ficus* spp. (higuera) | Common | Stranglers + hemiepiphytes |
| *Myrcianthes* (guabirá) | Common | Native fruit tree |
| *Allophylus edulis* (cocú) | Common | Mid-storey |
| *Eugenia uniflora* (pitanga) | Common | Native fruit |
| *Plinia rivularis* (yvaporoity) | Common | Stream-bank |
| *Patagonula americana* (guayaibí) | Common | Mid-canopy |
| *Tabebuia* spp. (lapacho rosado/amarillo) | High | Distinct from *Handroanthus* in literature |
| Tree ferns (*Alsophila*) | Likely | Humid valleys |
| Bamboo (*Guadua, Chusquea*) | Likely | Watercourses + clearings |

**Outputs:** v3 trees-GeoJSON should classify each stem to one of these genera by default, with `species_uncertain=true` for non-field-verified IDs.

### 2.3 Field-walk preparation
- **Trail-guide reference for the field botanist**: print a 1-page key with the 20 genera above + diagnostic photos.
- **Pl@ntNet API key**: free 500 calls/day at https://my.plantnet.org/account — set up before the field walk.
- **iNaturalist project**: create "La Quebrada Viva — Mbopicua cluster" private project to gate observations.
- **Herbarium voucher protocol**: dry-press samples for any unidentified stem, deposit at **CTES (Corrientes herbarium, Argentina, the closest regional reference)** or **PY (Asunción herbarium, MNHNP)**.

### `pull_list` for §2
1. Download Atlantic Forest Tree Database CSV (~5k species).
2. GBIF API pull: all occurrences within 10 km of polygon centroid → filter to Magnoliopsida → output `docs/site_data/flora/gbif_nearby.geojson`.
3. iNaturalist API pull: same bbox + radius → `docs/site_data/flora/inaturalist_nearby.geojson`.
4. Pl@ntNet API key registration.
5. Cross-tab GBIF + iNaturalist + Atlantic Forest Tree DB → ranked candidate-species list for the property, saved as `docs/site_data/flora/expected_species_ranked.csv`.
6. Print field-walk PDF: top-30 species, 1 reference photo each, vernacular Guaraní + Spanish + scientific name.

---

## 3. Surface water — beyond DEM D8

### 3.1 Better DEMs
| DEM | Resolution | Source | Why |
|---|---|---|---|
| **Copernicus DEM 30 m (currently use)** | 30 m | OpenTopography | Default |
| **Copernicus DEM 10 m** | 10 m | Restricted, EUR 0.50/km² | Sub-pixel improvement for streams |
| **TanDEM-X 12 m** (DLR research access) | 12 m | https://geoservice.dlr.de | Free for non-commercial research, application required |
| **ALOS AW3D30 (currently use)** | 30 m | OpenTopography | Independent cross-check |
| **NASADEM (currently use)** | 30 m | OpenTopography | SRTM corrected with ASTER + ICESat |
| **FathomDEM (Fathom Global Flood Map)** | 30 m | Restricted commercial | Probably too restricted |
| **MERIT Hydro** | ~90 m | http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_Hydro/ | Hydrology-corrected DEM for streams |
| **Drone SfM DSM/DTM** (Phase 2) | 5–10 cm | Self-flown / hired | The right answer |
| **Drone LiDAR DTM** (Phase 3) | 30–50 cm | Self-flown / hired | Under-canopy ground |

### 3.2 Pre-built hydrography
| Source | Notes |
|---|---|
| **HydroSHEDS v1 + MERIT-Hydro** | https://www.hydrosheds.org — global river network + watersheds + accumulation |
| **OpenStreetMap `waterway=*`** | OSM coverage in rural Paraguarí is sparse — checked, near-empty for polygon |
| **HAND (Height Above Nearest Drainage)** | https://confluence.ecmwf.int/ — flood-risk proxy |
| **Surface Water Occurrence (JRC)** | https://global-surface-water.appspot.com — 1984–2023 monthly water history at 30 m |
| **DESCRIBE Paraguay Hidrografía** | Cartas DGEC 1:50k, scanned |
| **MOPC Direccón de Hidrología** | https://www.mopc.gov.py — gauging stations, regional flow records |
| **INTA / SENADER Paraguay land-use overlays** | Includes drainage corrections |

### 3.3 Sentinel-2 / 1 water layers
- **NDWI / MNDWI / AWEI** time-series median → seasonal water mask.
- **Sentinel-1 SAR coherence drop** → flooded-vegetation detection (perennial wetlands).
- **JRC Global Surface Water monthly history** in GEE.

### 3.4 Drone / photo water layers
- Phone GPS at every crossing.
- Drone RGB at low water + high water (seasonal pair).
- Time-lapse camera at the salto / pool (CamHi-style trap cam, ~$80, motion-triggered).

### `pull_list` for §3
1. GEE pull JRC Global Surface Water Monthly History 1984–2023 → polygon clip → animated GIF.
2. GEE pull Sentinel-2 NDWI/MNDWI/AWEI median 2020–2025 → `docs/site_data/property_map/raster/water_seasonal.tif`.
3. GEE pull S1 SAR seasonal coherence → flooded-vegetation mask.
4. Pull MOPC Dirección Recursos Hídricos near-station data (Estación Escobar if exists, otherwise nearest in Paraguarí).
5. Re-derive D8 hydrography with `pyflwdir` (D-infinity > D8) on TanDEM-X 12 m if access granted.
6. Output `docs/site_data/property_map/hydrography_v2/` with three rasters + one revised vector.

---

## 4. Groundwater + aquifers — the underground layer

This is the dataset domain v1 ignored entirely. **The Guaraní Aquifer System (Sistema Acuífero Guaraní, SAG)** underlies the entire region; depth + recharge + well-water potability are concrete buildable-zone questions.

### 4.1 Guaraní Aquifer System (SAG)
- **OEA/GEF SAG Project final atlas (2009)** — https://www.oas.org/dsd/Documents/GEF_Guarani.pdf — depth, recharge, vulnerability, abstraction.
- **CeReGAS (Centro Regional para la Gestión de Aguas Subterráneas)** — Montevideo-based — ongoing SAG monitoring.
- **SAG technical reports (Argentina, Brazil, Paraguay, Uruguay)** — bilateral national reports.
- **Geological Survey of Brazil (CPRM) / SGN Paraguay** — regional hydrogeological maps 1:500k.

### 4.2 Paraguay-specific hydrogeology data
| Source | Content |
|---|---|
| **MOPC Dirección de Recursos Hídricos** | National well registry, hydrogeological mapping |
| **SAS (Secretaría del Ambiente, predecessor of MADES)** historical reports | Aquifer characterisation by department |
| **MADES (Ministerio del Ambiente y Desarrollo Sostenible)** | Environmental impact zones, EIAR/EIAp records |
| **SENASA (Servicio Nacional de Saneamiento Ambiental)** | Drinking-water well permits |
| **ITAIPÚ Binacional Hidrogeología** reports | Eastern Paraguay aquifer monitoring |
| **Yacyretá Hidrogeología** reports | Southern department coverage |
| **DGEEC + INE Paraguay** | Well-density stats by department |
| **Universidad Nacional de Asunción (FCA + FCAcU)** theses | Paraguarí-region hydrogeology theses |
| **CeReGAS Paraguay focal point** | Carlos Vázquez Mateos at MOPC |

### 4.3 What we want to extract for the property
- **Depth to Guaraní aquifer top** at polygon centroid (regional SAG maps).
- **Static water level estimate** in nearest registered wells (MOPC/SENASA).
- **Aquifer vulnerability index** (high/medium/low) for the polygon zone.
- **Recharge zone vs discharge zone** classification.
- **Nearest registered drilled wells** (depth, yield, water quality if reported).
- **Soil-type / lithology profile** to estimate drilling depth/cost.

### 4.4 Practical wells
- **`pozo profundo` quote**: Paraguarí drillers (Servicios Hidrogeológicos PY, Aguatec, Perforaciones del Este) — typical 60–120 m bore in this region, ~$3,500–6,500 turnkey including pump.
- **Static water table** in eastern Paraguay BSAU: typically 8–25 m below surface in valleys, 30–60 m on ridges. The 73.5 m relief on our polygon means there could be a 40+ m water-table gradient across the property.

### 4.5 Geology + soils
| Source | Content |
|---|---|
| **SGN Paraguay (Servicio Geológico Nacional)** | 1:100k geological mapping, lithology, faulting |
| **CONACyT Paraguay** | Research-grade geological + soil products |
| **MAG (Min. de Agricultura) / INFONA soil maps** | Classification at 1:50k |
| **FAO Harmonized World Soil Database (HWSD)** | 1 km global, contextual |
| **SoilGrids (ISRIC)** | 250 m global, raster soil properties (clay %, organic C, depth-to-bedrock) — https://soilgrids.org |
| **OpenLandMap (ENVIROnMENTAL)** | 250 m raster soil + climate |
| **Mapa de Suelos del Paraguay (López et al. 1995)** | Classic regional reference |
| **INTA Argentina border-region soil sheets** | Cross-border carry-over |

### `pull_list` for §4
1. Pull SoilGrids 250 m profile (clay/sand/silt %, organic C %, depth-to-bedrock, pH) for polygon.
2. Pull SAG atlas PDF → screenshot depth-to-aquifer-top + recharge classification for polygon zone.
3. Pull MOPC well-registry list (FOIA if no public portal) — nearest 20 wells with depth + yield + water quality.
4. Pull SGN 1:100k geological sheet — polygon lithology / structural geology.
5. Output `docs/site_data/hydrogeology/` with one CSV (wells) + 4 PNGs + 1 markdown summary.

---

## 5. Buildings — location, kind, appearance

### 5.1 Where buildings exist (registries + remote sensing)
| Source | Content |
|---|---|
| **OpenStreetMap (currently use)** | Overpass `building=*` — 9 returned, all neighbours, 0 on-property |
| **Microsoft Building Footprints** (global) | https://github.com/microsoft/GlobalMLBuildingFootprints — ML-derived from Bing imagery, ~1.7 B buildings; **Paraguay coverage sparse but worth checking** |
| **Google Open Buildings v3** | https://sites.research.google/open-buildings/ — currently Global South + LATAM partial coverage as of 2025 |
| **Overture Maps Foundation** | https://overturemaps.org — open building footprints, refreshed quarterly |
| **DGEEC (Dirección General de Estadística, Encuestas y Censos)** | Paraguay 2022 census + 2012 census — building-count per locality (no per-polygon) |
| **Catastro Nacional (Servicio Nacional de Catastro)** | Property cadastre — buildings as polygons in larger urban areas; rural rare |
| **Municipalidad de Escobar parcelario** | Local-municipality cadastre, paper or PDF |
| **INE 2022 vivienda CSV** | Vivienda count per `distrito` and `localidad` |

### 5.2 What the buildings look like (vernacular architecture references)
| Source | Why |
|---|---|
| **MOPC Vivienda Vernacular Paraguay** reports | Government catalog of rural vernacular |
| **CONAVI (Consejo Nacional de Vivienda)** | Housing-typology data |
| **MUVI (Ministerio de Urbanismo, Vivienda y Hábitat)** publications | Materials, typologies |
| **Universidad Católica Asunción — Facultad de Arquitectura** theses | Vernacular cob + brick studies |
| **Cabildo Asunción archive** | Historical photo reference |
| **National Geographic / Le Monde rural-PY archives** | 20-century photo refs |
| **Wikimedia Commons "rural Paraguay"** | Open-licensed photos |
| **iNaturalist project "rural architecture Paraguay"** (does not yet exist — could be created) | Crowdsource |

### 5.3 Typical building components in rural Paraguarí
- **Walls**: adobe / tapia / brick (`ladrillo común`), cob (`adobe + paja`) less common
- **Roof**: galvanized sheet metal (`chapa`), occasional clay-tile (`teja colonial`)
- **Floor**: tamped earth, brick, or cement
- **Windows**: small, wood-shuttered, no glass in older builds
- **Eaves**: deep overhangs (1.2–1.8 m) for sun + rain
- **Outbuildings**: pozo (well), letrina (latrine), cocina externa (outdoor kitchen), gallinero, tinglado para herramientas, corral
- **Fences**: alambrado de 5 hilos (5-strand barbed wire) standard for cattle parcels
- **Gates**: tranquera (wooden swing gate) at vehicle entrances

These typologies inform the eventual 3D twin: even before we get on-property photos, we know what shapes / textures to model.

### 5.4 Construction asset references for the 3D twin
- **Polyhaven**: galvanized-roof PBR, brick textures, cob/adobe textures.
- **Wikimedia "rural Paraguay" photos** → reference for roof colour, eaves geometry.
- **National Geographic + NGS PY archive** → boundary-fence + barn refs.
- **Wesley's photo intake** (Phase 1) → the actual buildings on his property.

### `pull_list` for §5
1. Microsoft Building Footprints — pull Paraguay tile, intersect polygon + 1 km buffer.
2. Google Open Buildings v3 — same intersection.
3. Overture Maps Foundation buildings — same intersection.
4. DGEEC 2022 census vivienda CSV for distrito Escobar.
5. Catastro Nacional public lookup for the 6 padrones (15-2317, 15-3008, 15-3007, 15-3006, 15-3004, 15-3005) — building polygons if any.
6. Wikimedia Commons "rural Paraguay" CC0/CC-BY photo set → reference images repo at `docs/site_data/references/architecture/`.
7. Output `docs/site_data/buildings_v2/` with three building-footprint GeoJSONs + a references PDF.

---

## 6. Ground / surface / terrain detail

### 6.1 Soil + lithology (overlaps §4)
- SoilGrids 250 m (clay %, sand %, organic C, depth-to-bedrock, pH).
- SGN 1:100k geology.
- MAG soil 1:50k.
- INTA Argentina border (cross-border carry-over).

### 6.2 DEM cascade
- v1: Cop30 30 m + AW3D30 + SRTM + NASADEM cross-check (already done in `docs/site_data/extended_aoi/`).
- v2: TanDEM-X 12 m (apply for research access at DLR).
- v3: Drone SfM 5–10 cm DSM/DTM.
- v4: Drone LiDAR 30–50 cm DTM under canopy.

### 6.3 Slope / aspect / curvature
- Cop30 derivatives shipped in `docs/site_data/extended_aoi/cop30_slope_pct.tif` + `cop30_aspect_deg.tif`.
- Add: TPI (Topographic Position Index), TRI (Roughness), Plan Curvature, Profile Curvature, TWI (Topographic Wetness Index) via `whitebox` or `richdem`.

### 6.4 Surface materials / land cover
- ESA WorldCover 10 m.
- Mapbiomas Paraguay 30 m.
- Dynamic World 10 m near-real-time.
- INFONA forest typology.

### 6.5 Ground photography
- Phone photo every 30 m along internal tracks → produces a `vector/ground_photos.geojson` with EXIF GPS.
- DSLR macro photos of representative leaf-litter, exposed soil, rock outcrops → texture reference for 3D twin.

### `pull_list` for §6
1. Pull SoilGrids 250 m soil-profile cube for polygon AOI.
2. Pull MAG / INTA soil sheets for distrito Escobar.
3. Compute TPI / TRI / Plan + Profile Curvature / TWI from Cop30 — add to `docs/site_data/extended_aoi/`.
4. Apply for TanDEM-X 12 m research access.
5. Output `docs/site_data/property_map/terrain_v2/` with 5 derivative rasters.

---

## 7. Fauna data — what should be there

### 7.1 Citizen-science observation databases
| Source | Coverage | What |
|---|---|---|
| **GBIF Paraguay** | https://www.gbif.org/country/PY/ | 1.4 M+ records all kingdoms — geotagged |
| **iNaturalist Paraguay** | https://www.inaturalist.org/places/paraguay | 200k+ research-grade observations |
| **eBird Paraguay** | https://ebird.org/region/PY | Birds, real-time |
| **WikiAves Brazil + cross-border** | https://www.wikiaves.com.br | Birds, photo-rich |
| **Guyra Paraguay AOC reports** | https://guyra.org.py | Conservation org annual reports |
| **Atlas de Mamíferos del Paraguay** (de la Sancha et al. 2022) | Print atlas | Definitive mammal range data |
| **PNN/INFONA wildlife camera-trap network** | Internal | Mammal records (FOIA-able) |
| **Reptile Database Paraguay** | https://reptile-database.reptarium.cz | Herpetofauna |

### 7.2 Expected mammals at La Quebrada Viva (Upper Paraná Atlantic Forest)
| Group | Likelihood | Species |
|---|---|---|
| Primates | High | *Sapajus nigritus* (capuchin), *Alouatta caraya* (howler) — confirmed nearby Mbaracayú |
| Felines | Medium | *Leopardus pardalis* (ocelot), *Leopardus wiedii* (margay), *Leopardus geoffroyi* (Geoffroy's cat); *Puma concolor* possible |
| Tapir / large herbivores | Low (extirpated locally?) | *Tapirus terrestris* — rare in fragmented forest |
| Deer | Medium | *Mazama americana* (red brocket), *Mazama gouazoubira* (gray brocket) |
| Pigs | Medium | *Pecari tajacu* (collared peccary) |
| Rodents | High | *Dasyprocta azarae* (agouti), *Cuniculus paca* (paca), *Hydrochoerus hydrochaeris* (capybara) along streams |
| Marsupials | High | *Didelphis* spp., *Marmosa* spp. |
| Anteaters | Possible | *Tamandua tetradactyla* — common |
| Armadillos | High | *Dasypus novemcinctus*, *Euphractus sexcinctus* |
| Carnivores misc | Medium | *Nasua nasua* (coati), *Procyon cancrivorus* (crab-eating raccoon), *Eira barbara* (tayra), *Cerdocyon thous* (crab-eating fox) |
| Bats | High | 30+ species expected, *Artibeus*, *Sturnira*, *Desmodus*, others |

### 7.3 Expected birds (eBird heat for the polygon area)
- Hotspots within 25 km of polygon: Cerro Acatí, Cerro Yaguarón, Lago Ypacaraí, Lago Ypoá, Parque Nacional Ybycuí.
- Expected ~250–350 species across the seasonal cycle including: toucans (*Ramphastos toco*, *Ramphastos dicolorus*), parrots (*Pyrrhura frontalis*, *Pionus maximiliani*), trogons, motmots, woodcreepers, antbirds, manakins, flycatchers, tanagers, hummingbirds (≥10 species).
- **Pull eBird API** (free with key) — produce species checklist for the polygon's 10 km hotspot rim.

### 7.4 Insects + invertebrates
- **GBIF + iNaturalist** for Lepidoptera, Odonata, Coleoptera.
- **PROCITROPICOS-PY** — Pampean / subtropical Lepidoptera lists.
- **Atlantic Forest Insect Conservation Bibliography**.

### `pull_list` for §7
1. eBird API key + pull last-12-month observations within 25 km of polygon centroid.
2. iNaturalist API — vertebrate observations within 25 km.
3. GBIF API — mammals + birds within 25 km, all time.
4. Cross-tab: produce `docs/site_data/fauna/expected_fauna.csv` ranked by occurrence frequency.
5. Output `docs/site_data/fauna/index.md` summarising likely fauna by group + 1 reference photo each (from Wikimedia Commons + iNaturalist CC-licensed).

---

## 8. Nearby reference parcels — "what could the property look like done well"

The user's request "all relevant data … of close by to understand what should be there" maps to **comparable parcels analysis**.

### 8.1 Spatial comparables in 30 km radius
- **Reserva Natural Mbaracayú** (Canindeyú; protected BSAU)
- **Parque Nacional Ybycuí** (Paraguarí; closest national park, ~30 km W)
- **Reserva Natural Tatí Yupí** (ITAIPÚ buffer; closest large protected area E)
- **Reserva Cerro Acatí** (Caapucú/Acahay area)
- **Reserva Natural Morombí** (Itapúa department, distant cross-comparable)
- **Refugio Biológico Yvyty Rokai** (Cordillera de los Altos)

For each: pull boundary GeoJSON, sample DEM/NDVI/canopy stats, compare to our polygon → "where on the spectrum of BSAU integrity does La Quebrada Viva fall?"

### 8.2 Eco-lodge / regenerative-tourism comparables
Operational rural-lodge precedents we can study for buildable program + planning:
| Lodge | Country | Distance | What to copy |
|---|---|---|---|
| **Awasi Iguazu** | AR | ~350 km | Plot-level architecture in similar biome (R37 target) |
| **Pousada Trijunção** | BR | ~700 km | Conservation-tourism business model |
| **Mawe Mawe** | BR | ~600 km | Forest-immersion small lodge |
| **Itacaré Eco Resort** | BR | 1,000+ km | Mature Atlantic-Forest eco-lodge |
| **Estancia La Sirena** (San Pedro) | PY | 350 km | PY-specific operating model |
| **Casa Yvy** (Carapeguá) | PY | 30 km | Local PY tourism reference |
| **Estancia Itabó** (Itapúa) | PY | 300 km | PY estancia operations |

### 8.3 Neighbour-parcel satellite analysis
- Pull NICFI + S2 for all polygons within 2 km of ours.
- Compute NDVI median, slope, canopy class for each.
- Tag "more deforested," "less deforested," "buildings present," "stream-dominated."
- Map → contextualises our polygon's land-use trajectory against neighbours.

### 8.4 Historical photo reference
- **Google Earth Pro** historical imagery slider (2000, 2005, 2010, 2015, 2020, 2024) → screenshot every 5 years → canopy-change timeline.
- **Mapbiomas Paraguay** annual time-stack 1985–2024.
- **Landsat 1985–2025** annual median.

### `pull_list` for §8
1. Pull boundaries of 6 nearby protected areas from WDPA (World Database on Protected Areas) → `docs/site_data/comparables/protected_areas.geojson`.
2. For each protected area: zonal stats (NDVI median + slope + canopy class %) vs our polygon → `docs/site_data/comparables/zonal_stats.csv`.
3. Pull NICFI + S2 for 2 km buffer around our polygon → neighbour-parcel canopy comparison map.
4. Google Earth Pro historical screenshots at 5-year intervals → `docs/site_data/comparables/historical/`.
5. Output `docs/site_data/comparables/index.md` summarising "where does La Quebrada Viva fit on the BSAU integrity spectrum + what does similar elsewhere look like done well?"

---

## 9. Climate, hydrology, weather context

(Adjacent to §3 + §4 but distinct in source.)

| Source | What |
|---|---|
| **ERA5 / ERA5-Land** | Hourly climate reanalysis 1940–, 9 km |
| **WorldClim v2.1** | 1 km climate normals 1970–2000 |
| **CHIRPS** | Daily precipitation, 5 km, 1981– |
| **CHELSA** | Monthly climate 1981–2010, 1 km |
| **MERRA-2** | NASA reanalysis |
| **TerraClimate** | Monthly, 4 km, 1958– |
| **Dirección de Meteorología Paraguay (DMH-DINAC)** | National stations, including possibly Yaguarón or Paraguarí stations |
| **INMet Brazil cross-border stations** | Border-region context |
| **SIPSA (Sist. Inf. de Precios y Salud Animal)** | Agro-climate data |

We have ERA5 climatology in `post_escritura_site_knowledge.md` (22 °C / 1,736 mm/yr / Cfa). For v2, add: precipitation seasonality, dry-month count, drought index (SPEI / PDSI), evapotranspiration (MOD16A2 PET).

### `pull_list` for §9
1. CHIRPS daily precipitation 1981–2025 for polygon → derive: median annual mm, monthly seasonality, dry-month count, 100-year-flood proxy.
2. ERA5-Land monthly 1980–2025 → derive: temperature range, frost incidence, wind direction frequency.
3. WorldClim bioclim variables (bio1–bio19) for polygon.
4. MOD16A2 PET monthly → water-balance estimate.
5. DMH-DINAC nearest station historical data (FOIA if needed).
6. Output `docs/site_data/climate/` with one CSV + four PNG charts.

---

## 10. Cadastral, legal, administrative data

| Source | What |
|---|---|
| **Servicio Nacional de Catastro (SNC)** | Padrón records, parcel boundaries, ownership chain |
| **Dirección General de los Registros Públicos (DGRP)** | Title chain, escritura records |
| **Municipalidad de Escobar** | Local cadastre, IMI tax records |
| **DGEEC + INE** | Census 2022 (housing, population by locality) |
| **MTESS rural-employment registry** | Indirect signal of rural development |
| **Min. Salud Pública network** | Health-post locations (closest hospital reference for site planning) |
| **ANDE (electricity)** | Power-grid extent — critical for buildability |
| **COPACO / Tigo / Personal / Claro coverage maps** | Internet + mobile coverage |
| **MOPC vialidad** | Road network + maintenance class |

For our 6 padrones (15-2317, 15-3008, 15-3007, 15-3006, 15-3004, 15-3005), the SNC public lookup should return area + assessed value + last-transfer date. We already have escritura → cross-check.

### `pull_list` for §10
1. SNC public lookup for the 6 padrones → save assessed-value sheet.
2. ANDE coverage map for distrito Escobar → distance from nearest MV line.
3. COPACO/Tigo/Personal coverage map → cellular signal grade at polygon centroid.
4. MOPC road-class data for `Camino a Escobar` (maintenance class, AADT if surveyed).
5. Output `docs/site_data/infrastructure/` with one CSV + utility-distance summary.

---

## 11. Photo-archive datasets (online reference for the property's appearance)

| Source | Why |
|---|---|
| **Google Street View** | Camino a Escobar likely has at least one drive-by pass; check |
| **Mapillary** | Crowd-sourced street-level imagery; check polygon vicinity |
| **KartaView (formerly OpenStreetCam)** | Same — sparse in PY |
| **iNaturalist photos within 25 km** | Habitat + understorey references |
| **eBird hotspot photos** | Forest interior + edge habitats |
| **Wikimedia Commons "Paraguarí"** | Regional landscape refs |
| **Instagram geo-tag search "Mbopicua" / "Paraguarí" / "Escobar"** | Recent ground-truth |
| **National Geographic / NGS photo archive PY** | Iconic regional references |
| **Cuenca Mbopicua + Tebicuary hydrography photos** | Cross-region water refs |

### `pull_list` for §11
1. Mapillary API pull for polygon + 1 km buffer.
2. Google Street View pass — manual review.
3. iNaturalist photo set within 5 km, all kingdoms → habitat reference repo.
4. Output `docs/site_data/references/` with sub-folders: `architecture/`, `flora/`, `fauna/`, `landscape/`, `nearby/`.

---

## 12. Recommended Phase-0 data pull (the actual to-do list, ranked)

In execution order, all free, none requires Wesley's photos:

1. **GEE auth** — `earthengine authenticate` (10 min).
2. **NICFI signup** — academic free tropical access (10 min).
3. **Atlantic Forest Tree DB CSV download + load** (15 min).
4. **GBIF + iNaturalist + eBird API pulls** within 25 km of polygon (~30 min total).
5. **JRC Global Surface Water Monthly History** clip → animated water-occurrence GIF (~20 min).
6. **Sentinel-2 12-date 2020–2025 median + NDVI/NDWI/MNDWI/AWEI** (~30 min).
7. **Sentinel-1 SAR VV/VH 6-month median** for biomass + flooded-veg layer (~20 min).
8. **Landsat 1985–2025 annual median** for 40-year canopy timeline (~20 min).
9. **ALOS PALSAR-2 2018–2024 annual mosaic** (~20 min).
10. **Hansen tree-loss raster** clip + year-of-loss map (~10 min).
11. **Mapbiomas Paraguay 1985–2024** clip → land-cover time stack (~20 min).
12. **SoilGrids 250 m profile cube** clip for polygon (~10 min).
13. **Microsoft + Google + Overture building footprints** intersect polygon + 1 km (~20 min).
14. **WDPA protected-area boundaries** for 6 nearby reserves (~10 min).
15. **DeepForest + detectree2** crown detection on NICFI tile (~30 min compute).
16. **pyflwdir** re-derivation of stream network on Cop30 (and TanDEM-X 12 m if approved) (~10 min).
17. **CHIRPS + WorldClim + ERA5-Land + MOD16A2** climate cube (~20 min).
18. **SNC padrón public lookup** for 6 padrones (~20 min manual).
19. **Mapillary pull** for polygon + 1 km buffer (~10 min).
20. **Compile** `docs/site_data/property_map_v2/index.md` referencing all of the above.

Estimated total: **~6 hours of compute + 1 hour manual** — feasible in one autonomous session.

---

## 13. What this unlocks

After §12 we will know — **without ever setting foot on the property** — :

- 40-year canopy change history → tells us if this is mature secondary forest, regrowth on old pasture, or always-forested.
- Year-by-year tree-loss inventory → where, when, how much.
- Crown count + crown polygons (NICFI-resolution) → first-pass tree count, even if conservative.
- Genus-ranked candidate species list → the field-walk priors.
- Animated water-occurrence GIF → which DEM-traced channels are actually wet, and when.
- Aquifer depth + recharge classification → well-drilling cost-feasibility.
- Soil profile cube → cob/adobe vs brick decision for vernacular building.
- Climate cube → planting windows, dry-month count, flood return period.
- Fauna candidate list → conservation marketing positioning.
- Nearby-parcel comparable map → "we are richer/poorer in canopy than 80 % of neighbours."
- Protected-area zonal stats → "we are 67 % as canopy-dense as Mbaracayú, 91 % as Cerro Acatí."
- Building footprint cross-check → confirms 0 on-property buildings independent of OSM.
- Mapillary + Street View → first-look photo refs.

That set of derivations is what Wesley and Thijs see in v2.

Then we layer **on top** the things only photos / drone / LiDAR can give (v3+):

- Per-stem positions + heights (drone LiDAR).
- Stream perennial-vs-seasonal classification (photo + drone time-pair).
- On-property structures (photo + drone + Geo-SAM).
- Species ID with confidence ≥ 0.8 (field-walk + Pl@ntNet).
- Under-canopy DTM (LiDAR).
- Cultural features (photo).
- Salto / natural pool location + dimensions (photo + drone).

---

## 14. What stays unknowable until on-the-ground

A short honesty list:

- **Soil pH spot variation** — even SoilGrids 250 m is too coarse for a 30 ha decision; needs in-situ samples sent to UNA-FCA lab (~$80/site).
- **Static water table at any specific drill site** — only a test borehole confirms.
- **Cultural / spiritual sites** (graves, shrines, boundary marks) — never visible from satellite.
- **Tenure ambiguity** (squatter occupation, informal use, neighbour grazing rights) — only Wesley + on-site walk surfaces this.
- **Endangered-species presence** (jaguar, harpy eagle, woolly spider monkey) — requires camera-trap deployment, ~$80/trap × 5 traps × 60 nights.

These are **NOT** included in any v2 / v3 deliverable; they belong in v4 with conservation-org partnership (Guyra Paraguay, Itaipú Biodiversidad, WCS-PY).

---

## 15. Index of related docs

- `docs/research/property_map_v2_tooling.md` — software / pipeline companion
- `docs/site_data/property_map/index.md` — v1 layer manifest
- `docs/site_data/property_map/photo_verification.md` — 14-row shot-list cross-ref
- `docs/site_data/escobar_property_polygon.geojson` — canonical AOI
- `docs/site_data/extended_aoi/` — v1 DEM cascade
- `docs/post_escritura_site_knowledge.md` — current knowledge baseline
- `docs/RESEARCH_GAPS.md` R01, R35
- `docs/research/GEDI_L2A_RESEARCH.md` — spaceborne LiDAR baseline

---

## 16. Next action

Bias is to **execute §12 list now**, in a single autonomous pass, without asking Wesley. Each pull is small + idempotent + deletable on demand. The output is a v2 map that is genuinely complete to the limit of what public data allows, with a clear honesty boundary at "needs photos / drone / LiDAR."

Phase-0 acquisition does not touch:
- The frozen escritura bundle (`85e86aa`, SHA `9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c`).
- `lqv/` rendering code.
- `lqv/scatter_lapacho_petals`.

It adds files under `docs/site_data/property_map_v2/`, `docs/site_data/hydrogeology/`, `docs/site_data/fauna/`, `docs/site_data/flora/`, `docs/site_data/comparables/`, `docs/site_data/climate/`, `docs/site_data/infrastructure/`, `docs/site_data/references/` — all new directories.

