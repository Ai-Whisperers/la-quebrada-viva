# API Access Guide — La Quebrada Viva (LQV)

**Project:** Cob/bottle earthen house on 62-ha in Escobar, Paraguarí, Paraguay  
**Client:** Wesley van de Camp (75%) + Thijs (25%) — escritura 2026-06-27  
**Operator:** AI Whisperers (Ivan) — autonomous geospatial pipeline  
**Goal of this document:** Get you a step-by-step path to grant me access to every data source I need, in the order that unblocks the most work.

---

## TL;DR — What I need from you

In priority order (top = highest impact, do these first):

| # | Action | Time | Cost | Unblocks |
|---|---|---|---|---|
| 1 | Accept NASA Earthdata cloud-pool EULA + regenerate bearer token | 5 min | free | full GEDI re-pull (~25 → ~hundreds of shots), Sentinel-2 retries, SRTM/NASADEM direct |
| 2 | Register at ECMWF Climate Data Store (CDS) | 10 min | free | ERA5 climate baseline (replaces broken WorldClim) |
| 3 | Create a new Copernicus OAuth client with stronger scopes OR manual-download the LC100 TIF | 5–30 min | free | actual land cover data on disk |
| 4 | Register at ISRIC SoilGrids (optional) | 5 min | free | soil pH, organic carbon, texture for the 62 ha |
| 5 | Register at INPE Brazil catalog | 15 min | free | CBERS-4 (5m panchromatic) and SAOCOM SAR for canopy penetration |
| 6 | (Defer) Drone survey commissioning — post-closing | 2 weeks | ~$1,500 | 1 m DEM, all engineering + render work |
| 7 | (Defer) Planet Labs subscription — post-closing | varies | ~$2–5k/yr | daily 3 m imagery for construction monitoring |

Everything else (Microsoft Planetary Computer, JAXA ALOS, CHIRPS, HydroSHEDS, WorldPop, GHSL, iNaturalist) requires **no auth** and I will just use them.

---

## 1. NASA Earthdata — full access (CRITICAL, 5 min)

**What I have now:** Bearer token in `.env.local` (expires 2026-08-09). CMR granule queries work, but cloud-hosted GEDI / Sentinel-2 / SRTM / NASADEM are blocked at the 303 redirect until you accept the cloud-pool EULA.

**What this unlocks when fixed:**
- Full GEDI L2A re-pull (hundreds of clean shots vs 25) — needed for biomass estimation
- Sentinel-2 retries (currently we got 0.004% cloud scene, but the cloud EULA unlocks 2015-2020 archive)
- SRTM, NASADEM, MCD12Q1 (MODIS land cover), HLSL direct downloads
- All NASA Earthdata cloud data

**Step-by-step:**

1. Open **https://urs.earthdata.nasa.gov/home** and sign in (you are already logged in as `ivanpolweiss`).
2. Go to **https://lpdaac.usgs.gov/terms/** — scroll to the GEDI section, check the box, click "Submit". This accepts the GEDI data use agreement.
3. Open **https://search.earthdata.nasa.gov/search?sp=GEDI&pg=1&collectionId=C2142778263-LPCLOUD** — click "Download" on any GEDI L2A file. A popup will appear titled "Earthdata Cloud Data Pool" — click "Accept". This unlocks the cloud EULA.
4. Go back to **https://urs.earthdata.nasa.gov/profile** → click "Generate Token" → copy the new token.
5. Paste the new token into `/home/ai-whisperers/blender-projects/la-quebrada-viva/.env.local`, replacing the existing `NASA_EARTHDATA_TOKEN=...` line.
6. Tell me you have done it — I will re-run `extract_gedi_https.py` (~30 min) and you will have a full vegetation map.

**Cost:** $0  
**Risk if not done:** Sentinel-2 retry path is blocked, GEDI stays at 25 shots, no MODIS land cover history.

---

## 2. ECMWF Climate Data Store (CDS) — climate baseline (HIGH VALUE, 10 min)

**What this gives:** ERA5 reanalysis — monthly mean temperature, precipitation, humidity, wind, solar radiation at 9 km resolution, from 1940 to present. This is the **definitive replacement for the broken WorldClim** and what we originally wanted from WorldClim.

**Why we need it:**
- Brochure: "always-wet subtropical climate, mean 22°C, rainfall 1,500 mm/yr"
- Passive design verification: Rule 6 of the 10 design rules (≤35°C passive cooling)
- Solar shadow study baseline
- Micro-hydro stream flow estimation (use ERA5 precipitation + DEM)
- Compare to MASTER_BRIEF §3 (climate constraints)

**Step-by-step:**

1. Open **https://cds.climate.copernicus.eu/** and click "Register" (top right).
2. Use the same email as Copernicus Dataspace: **weissvanderpol.ivan@gmail.com**.
3. Accept the license terms.
4. Once logged in, go to **https://cds.climate.copernicus.eu/profile** — copy your UID and API Key.
5. Create the file `~/.cdsapirc` (note the leading dot) with this content:
```
url: https://cds.climate.copernicus.eu/api/v2
key: <your-uid>:<your-api-key>
```

6. Run `pip install cdsapi` (already in the project venv).
7. Tell me you have registered — I will write `scripts/fetch_era5_climate.py` and run it.

**Cost:** $0  
**What I pull:** Monthly 2m temperature, total precipitation, 10m wind, surface solar radiation for the 3.3 km × 3.3 km bbox, 1990-2025 (35 years × 12 months × 4 vars = ~170 small files).

**Expected output:** A `docs/site_data/climate_era5/` directory with:
- `tavg_1990_2025_monthly.tif` (35 × 12 = 420 bands)
- `prec_1990_2025_monthly.tif`
- `wind_1990_2025_monthly.tif`
- `srad_1990_2025_monthly.tif`
- `climate_summary.txt` (annual means, seasonality index, extreme months)
- `climate_brochure.md` (pull-quotes for the escritura: "between 1990 and 2025, the site experienced mean annual X...")

**Risk if not done:** WorldClim stays broken, climate section of the brochure is hand-waved.

---

## 3. Copernicus Dataspace — land cover & Sentinel-1 (CRITICAL, 5–30 min)

**What I have now:** OAuth client `heermes` (client_credentials only). STAC catalog queries work. OData downloads return 401 "Token audience not allowed" because client_credentials tokens cannot access the download API. S3 access requires proper S3 credentials.

**The fix (3 options, pick one):**

### Option A: Manual download via Browser (5 min)
1. Open **https://browser.dataspace.copernicus.eu/**
2. Sign in with `weissvanderpol.ivan@gmail.com`
3. Search for: `PROBAV_LC100_global_v3.1.2_2019_cog`
4. Click the **discrete_classification_map** asset (single TIF, ~3 MB)
5. Download it → save to `/home/ai-whisperers/blender-projects/la-quebrada-viva/docs/site_data/cgls_lcover/lcover.tif`
6. Tell me when done — I will run my existing `fetch_copernicus_lcover.py` which will auto-detect the file and generate the preview + class summary.

### Option B: Create a stronger OAuth client (10 min)
1. Go to **https://dataspace.copernicus.eu/** → User settings → OAuth clients
2. **Delete** the existing "heermes" client (it was leaked in chat)
3. Create a new one with **every scope checked** including any "S3" / "data access" / "STAC + OData" option
4. Note: As of 2026, the platform **only supports CLIENT_CREDENTIALS flow** — no password grant available
5. Try the download again with the new client

### Option C: Request S3 credentials via support (1–2 business days)
1. Open a ticket at **https://help.dataspace.copernicus.eu/**
2. Subject: "Need S3 access keys for OAuth client `heermes` for CLMS LC100 + Sentinel-1 download"
3. Body: "I have an OAuth client `sh-bcc64b75-02d5-4beb-b19d-c305a814d5cb` but I need S3-compatible credentials (access key + secret) to download COG products via boto3. My use case is commercial (Paraguayan real-estate project). Please advise."
4. They will either issue you a key or tell you the canonical pattern.

**Cost:** $0  
**What I pull:** 100m land cover classification for our 3.3 km × 3.3 km bbox, with all 16+ cover fractions (forest type, tree cover, grass, crop, builtup, bare, snow, water, moss, lichen).

**Expected output:**
- `docs/site_data/cgls_lcover/lcover.tif` — 100 m resolution, single TIF
- `docs/site_data/cgls_lcover/lcover_preview.png` — false-color RGB
- `docs/site_data/cgls_lcover/lcover_summary.txt` — class breakdown: "62% closed broadleaf forest, 18% shrub, 12% agriculture, 8% water/wetland..."

**Risk if not done:** Land cover data is the "I have satellite data, not vibes" credibility item for the escritura bundle. Without it, we have only DEM + GEDI canopy, not the actual land-use class.

---

## 4. Microsoft Planetary Computer — no auth, instant use

**What this gives:** Free STAC catalog with pre-processed datasets:
- Sentinel-2 L2A (atmospherically corrected surface reflectance, ready-to-go)
- Landsat 8/9 (thermal bands → surface temperature)
- MODIS NDVI / EVI (16-day composites, full archive)
- Daymet (daily weather at 1 km, 1980-present — another WorldClim alternative)
- NAIP (US-only — not useful)
- GBIF (mirror of gbif.org)
- HGB (Harmonized Global Biomass — for aboveground carbon estimates)

**Step-by-step:** Nothing. I will just use it. The API requires no auth, no token, no registration. First request is a STAC query, subsequent are signed-URL downloads that work anonymously.

**Cost:** $0  
**What I pull:** Sentinel-2 L2A (alternative to our existing direct fetch), Landsat 8/9 thermal, Daymet climate.

**Risk if not done:** None — pure upside.

---

## 5. ISRIC SoilGrids — soil properties

**What this gives:** Global soil maps at 250 m resolution:
- pH (H2O and KCl)
- Organic carbon (%)
- Bulk density (g/cm³)
- Cation exchange capacity
- Sand/silt/clay fractions
- Depth to bedrock
- For 6 standard depth intervals (0-5cm, 5-15cm, 15-30cm, 30-60cm, 60-100cm, 100-200cm)

**Why we need it:**
- Cob house foundation design (soil bearing capacity → depth of stone foundation)
- Agricultural viability for housing-park lots
- Brochure: "red laterite topsoil 30-50cm deep, pH 5.5-6.0, moderate organic carbon"

**Step-by-step:**

1. Open **https://www.isric.org/explore/soilgrids** and create a free account (email only).
2. Once logged in, go to **https://www.isric.org/explore/soilgrids/faq** — the WCS endpoint is public, no API key needed for most queries.
3. Tell me you have registered — I will write `scripts/fetch_soilgrids.py` and run it.

**Cost:** $0  
**Risk if not done:** None critical — we have a soil description in MASTER_BRIEF that we can use, but SoilGrids gives actual numbers per pixel.

---

## 6. INPE Brazil — CBERS-4 + Amazonia-1 (commercial-grade free data)

**What this gives:**
- **CBERS-4** (China-Brazil Earth Resources Satellite): 5 m panchromatic, 10 m multispectral — high enough to map individual structures (existing block house, quincho, road condition) in our 3.3 km × 3.3 km bbox. Free, no auth.
- **Amazonia-1**: 60 m wide-swath, 64 km swath — useful for regional context but not for the 62 ha
- **SAOCOM-1A/1B** (Argentine L-band SAR): 10 m resolution, penetrates canopy — gives real ground topography even in our dense forest. **Potentially huge** for accurate buildability. Free via CONAE.

**Why we need it:** Sentinel-2 is 10 m, but the cob house is ~10-15 m wide — barely 1 pixel. CBERS-4 panchromatic is 5 m = 2-3 pixels per house, enough to plan a precise site visit.

**Step-by-step:**

1. Open **http://www.dgi.inpe.br/catalogo/** and click "Register" (top right).
2. Use **weissvanderpol.ivan@gmail.com**.
3. Accept terms.
4. Once logged in, the catalog accepts queries from any IP, no token needed. Tell me when registered.

For SAOCOM:
1. Open **https://catalog.cordoba.conae.gov.co/** (or similar CONAE catalog)
2. Register similarly

**Cost:** $0  
**Risk if not done:** None critical — Sentinel-2 is enough for the escritura; CBERS-4 is a nice-to-have for the marketing close-up.

---

## 7. JAXA Earth API — ALOS PALSAR (canopy-penetrating SAR)

**What this gives:** L-band Synthetic Aperture Radar from JAXA's ALOS-1 and ALOS-2 satellites. L-band penetrates vegetation canopy — gives **real ground elevation even in mature forest**. Sentinel-1 C-band SAR and optical DEMs (SRTM, ASTER) get the canopy top; L-band gets the ground.

**Why we need it:** Our 4 DEMs all show 116-380 m elevation, but in dense Atlantic Forest, the actual ground elevation is hidden by 10-40 m of canopy. ALOS PALSAR would let us subtract the canopy and get the real topography.

**Step-by-step:**

1. Open **https://www.eorc.jaxa.jp/ALOS/en/palsar/index.htm** and read about ALOS PALSAR.
2. Create a JAXA EORC account at **https://www.eorc.jaxa.jp/ALOS/en/palsar/data_access.htm** — free, requires institutional email.
3. Alternatively, OpenTopography (where we already have an API key) hosts some PALSAR-derived DEMs. Check the OpenTopography catalog for "ALOS PALSAR" in the Paraguay region.

**Cost:** $0  
**Risk if not done:** None for escritura. Becomes important for accurate engineering after closing.

---

## 8. Commercial data (DEFER until post-closing)

### Planet Labs PlanetScope — daily 3 m imagery
- **Use case:** Construction monitoring, weekly site updates, social media
- **Cost:** ~$2,000-5,000/year for our 62 ha (Education & Research program discount available)
- **When:** Post-construction start (~July 2026)
- **Action:** Sign up at **https://www.planet.com/** for an account; Wesley's company can be the legal entity

### Maxar / Airbus high-res — 30-50 cm
- **Use case:** One-time marketing imagery, glossy brochure close-ups
- **Cost:** ~$20-50 per km² for tasking, $5-10 for archive
- **When:** After closing, before the brochure prints
- **Action:** Sales contact — Maxar at **https://www.maxar.com/**, Airbus at **https://www.intelligence-airbusds.com/**

### Drone survey (highest-ROI single dataset)
- **Use case:** 1 m DEM, accurate 3D site model, construction progress
- **Cost:** $1,000-2,000 in Paraguay
- **When:** After closing, before detailed engineering
- **Action:** Wesley to commission — we know an operator in Asunción (per `docs/site_data_spike.md`)

---

## What I need from you (Ivan) RIGHT NOW to unblock the most work

If you do **only three things today**, do these:

1. **NASA Earthdata** (5 min, $0) — accept cloud-pool EULA, paste new token
2. **Copernicus manual download** (5 min, $0) — download the 3 MB LC100 TIF and save it to `docs/site_data/cgls_lcover/lcover.tif`
3. **ECMWF CDS** (10 min, $0) — register and paste the `~/.cdsapirc` content

After those three, I can complete:
- Full GEDI vegetation map
- Land cover classification
- 35-year climate baseline for the brochure
- All of which feed into the escritura bundle by 2026-06-27

If you do **everything else this week**, do these in order:

4. **ISRIC SoilGrids** registration (5 min)
5. **INPE** registration for CBERS-4 access (15 min)
6. **JAXA** registration for ALOS PALSAR (15 min, optional)

---

## What I will NOT do without your explicit approval

Per the project operating rules (CLAUDE.md, item 6: "Still ask before destructive or shared-state actions"):

- **Delete the existing Copernicus OAuth client** (the one with the leaked secret) — you need to do this from the UI yourself
- **Rotate the leaked secret** — same, you do it from the UI
- **Send any external messages** on your behalf (email, support tickets, etc.)
- **Post the credential leakage to a public security advisory** (would be a responsible thing to do, but not without your call)

What I will do autonomously without asking:
- Write the new fetch scripts (era5, soilgrids, planetary_computer, alos_palsar)
- Re-run the existing scripts once you provide new credentials
- Stage and commit the new data to the repo (with `Co-Authored-By: Claude` trailer per project convention)
- Update the docs (DATA_INVENTORY.md, site_data_spike.md) with the new data
- Generate the marketing-ready analysis files (climate_brochure.md, soil_summary.txt, etc.)

---

## Reference table — what to use for what

| Need | Best source | Backup | Status |
|---|---|---|---|
| Topo / DEM (30 m global) | ALOS AW3D30 | Copernicus DEM, SRTM, NASADEM | done |
| Topo / DEM (1 m local) | Drone survey (post-closing) | OpenTopography (no PALSAR in our bbox) | post-closing |
| Topo / DEM (canopy-penetrated) | ALOS PALSAR | none | needs JAXA access |
| Land cover class | Copernicus LC100 (CDSE) | ESA WorldCover 10m (no auth) | needs Copernicus download |
| Tree cover % | GEDI L2A | ESA WorldCover tree layer | 25 shots, need 100s |
| Aboveground biomass | GEDI L2A + allometric model | JPL AGB, GEDI L4A | needs more GEDI shots |
| Climate baseline (1990-2025) | ECMWF ERA5 | Daymet via MPC, CHIRPS precip | needs CDS access |
| Soil pH / OC / texture | ISRIC SoilGrids | HWSD v2 | optional |
| Real-color satellite photo | Sentinel-2 L2A | CBERS-4, Landsat 8/9 | done |
| Bird / mammal species | GBIF | iNaturalist, eBird | done (54 spp GBIF) |
| Plant species | GBIF | iNat (richer for plants) | partial |
| Acoustic / dark-sky baseline | none (field measurement) | — | needs R36 fieldwork |
| High-frequency construction monitoring | Planet Labs | drone | post-closing |
| 30-50 cm marketing close-up | Maxar / Airbus | drone | post-closing |

---

## Files I will create in the repo

- `docs/api_access_guide.md` (this document)
- `.env.local` (updates you paste into)
- `scripts/fetch_era5_climate.py` (new)
- `scripts/fetch_planetary_computer.py` (new)
- `scripts/fetch_soilgrids.py` (new)
- `scripts/fetch_alos_palsar.py` (new)
- `scripts/fetch_inpe_cbers.py` (new)
- `docs/site_data/DATA_INVENTORY.md` (update with new data)
- `docs/site_data_spike.md` (update access section)

---

## Timeline relative to escritura 2026-06-27

- **Today / tomorrow:** NASA EULA + Copernicus manual download + ECMWF CDS registration → unblocks climate, GEDI, land cover
- **This week:** SoilGrids + INPE + JAXA registrations → unblocks soil, SAR, higher-res photo
- **Week of escritura:** Final data runs, analysis generation, brochure material
- **Post-closing (July 2026+):** Drone survey, Planet subscription, full 1 m DEM engineering

---

## Questions? Edge cases?

- If you cannot access any of these (e.g., you are traveling without your auth app), tell me which one is blocked and I will work around it
- If you have other ideas about what data we should get (acoustic? biodiversity camera traps? drone thermal?), tell me — I will add them to the list
- If any of the providers require an institutional email (university, etc.), tell me your affiliation and we can route through that

---

*Maintained by AI Whisperers (Ivan). Last touched: this session.*