# GAPS_ANALYSIS — T+2 post-escritura blindspot + upgrade ledger

> 2026-06-29 (T+2). Authored by AI Whisperers under `/ultrawork`. Reads the repo at HEAD=`0554b77` (Phase-0 §12.D protected-areas + comparables landed) against MASTER_TODO (76 open items), RESEARCH_GAPS (R01–R38), DEFERRED_BUGS (closed at `78433a7`), MCP_STATUS (retired), post_escritura_site_knowledge, and the unmerged work-in-progress on disk (§12.E JRC GSW batch script). Intent: name what is missing, what is upgradeable, what is invisible, in one place — so the next sprint plans against reality, not against the deck.

This document is **negative-space**: it enumerates absence, not presence. The positive-space companion is `docs/research_index.md` + `STATUS.md`. When a fact contradicts STATUS, this file wins for *gaps*; STATUS wins for *delivered state*.

Coverage spans seven domains:

1. Data / GIS / open-data layer
2. Render pipeline + Blender backlog
3. Legal / property / regulatory
4. Engineering + build feasibility
5. Commercial / distribution / market
6. Ops / reproducibility / risk
7. Meta / project-management blindspots

Each row carries: **what is missing**, **why it matters now (T+2 reality)**, **who owns it**, **decision it unblocks**, **cost / effort estimate**, **leverage tier** (P0 = blocks Phase-1 capex, P1 = blocks within 90 days, P2 = blocks within 1 year, P3 = backlog).

---

## 1. Data / GIS / open-data layer

### 1.1 Acquired (cumulative through `dbff483`)

| Dataset | Coverage | Status |
|---|---|---|
| ALOS World3D 30m DEM | 62.57 ha + 60 m buffer | ☑ canonical DEM, 5 m RMSE |
| COP30 DEM | same | ☑ A/B cross-check (±5 m) |
| SRTM, NASADEM | same | ☑ ensemble agreement |
| Sentinel-2 L2A (5 bands, regenerable) | AOI | ☑ NDVI 0.917 wall-to-wall, no open water |
| GEDI L2A (cleaned shots: 25 of 475) | AOI | ☑ canopy 27.7 m median, 74 m max |
| GBIF biodiversity (7 classes, 25 km buffer) | regional | ☑ at `dbff483` |
| iNaturalist 25 km | regional | ☑ at `dbff483` |
| ISRIC SoilGrids 2.0 cube (5×5×9×6×2) | 50 km AOI grid | ☑ at `dbff483` |
| MS GlobalMLBuildingFootprints | ±1 km AOI = 737 buildings | ☑ at `dbff483` |
| OSM (positional reference only) | AOI | ☑ (ODbL — no bundling) |
| ERA5 climate 1990–2025 | 22 °C, 1736 mm/yr | ☑ summarised |
| Wesley KML polygon (30.9 ha buildable) | scope-locked | ☑ at `e3d8cce` |
| 4-DEM fusion | regional | ☑ at `dbff483` topology_lod cube |

### 1.2 Missing — P0 (blocks design, not procurable later for the same money)

| ID | Gap | Why now | Cost / effort | Owner |
|---|---|---|---|---|
| **D1** | **Drone LiDAR 1 m DEM** of the 30.9 ha polygon + 60 m buffer (R35) | Every Phase-1 siting decision is sitting on a 30 m grid = 3 pixels per cabin. Cabin pad, stream centerline, terrace earthwork volumes all wrong by 1–3 m vertically. **Re-evaluate at T+30 after client photos arrive** — flying speculatively burns the quote. | ~$1,500 + 1 week | Wesley + PY drone operator |
| **D2** | **Soil bearing-capacity test** (CC-BUILD.3) | Stone-plinth foundation depth (Rule 4: 60 cm raised) cannot be confirmed without it. Penetrometer or DCP at 4–6 points across the 4.28 ha flat band. | ~$300–800 + 1 day | Ivan + civil eng |
| **D3** | **In-situ stream flow measurement** for Pelton micro-hydro (CC-BUILD.4) | Open-data hydrology shows NDWI < 0 everywhere — quebrada is inferred from topology, not observed. Pelton 200–400 W claim is heightmap-only; flow rate (L/s) gates the whole feasibility. Pair with stream-bed photos from intake list. | ~$200 + 1 day | Ivan + hydraulic eng |
| **D4** | **Client photo intake** (R01, 14 named shots) | Blocks confirmation of: (a) where quebrada actually runs, (b) road condition from ruta to pin, (c) existing structures, (d) canopy species composition (NDVI ≠ species), (e) waterfall/pool location. **No other open-data source can close these.** | $0 + Wesley's schedule | Wesley |
| **D5** | **Anexo I cadastral shapes** (R02) | Two padron-triple hypotheses (A/B) both project to 30.35 ha. Anexo I tie-break decides whether finca 697 Mbopicua + finca 298 Ybyraty (the 32 ha residual) are contiguous reserve or distant. **Escribana Peña Ros owes this.** | $0 + 1 chase email | Wesley + Lawyer |

### 1.3 Missing — P1 (sharpens design, procurable up to ~T+90)

| ID | Gap | Why | Cost / effort |
|---|---|---|---|
| D6 | **Hyperspectral / multispectral species classification** of the canopy (R01 §canopy). Sentinel-2's 10–60 m bands cannot resolve Handroanthus impetiginosus (lapacho) vs Peltophorum dubium (yvyrá-pytá) vs Cordia trichotoma (peterebí). Drone + push-broom MicaSense or PlanetScope 8-band time-series would. Drives flower-season scene authenticity (variant A pink bloom timing). | ~$500–2k (PlanetScope subscription / drone mission) |
| D7 | **AOI polygon vs bbox delta** — current bbox AOI (W-57.050 S-25.625 E-57.020 N-25.595) is 3 × the polygon area; SoilGrids cube and biodiversity sweep both ran on bbox not polygon. Re-clip outputs to polygon for tighter species counts and soil bearing. | 1 day scripting, no data fetch |
| D8 | **Google Open Buildings v3** (deferred at `dbff483`) — second source for the 737 MS footprints. Triangulating with v3 would catch missed neighbouring caseríos / un-roofed permanent structures (e.g. tile-roof tobacco shed Wesley mentioned but no MS hit). | 1 day, free |
| D9 | ~~**Protected-areas + comparables sweep**~~ — **closed** at commit `0554b77` (Phase-0 §12.D: WDPA REST + Overpass `boundary=protected_area` + `leisure=nature_reserve` within 50 km, outputs at `docs/site_data/comparables/`). Successor: **§12.E JRC Global Surface Water** WIP at `scripts/phase0_jrc_gsw_batch.py` — independent water-presence ground-truth (1984–2021) cross-checking Sentinel-2's NDWI<0 finding. Finish + ship before declaring §12 wrapped. | 0.5 day to finish + run |
| D10 | **Acoustic + dark-sky baseline** (R36) — 4 visits × 2–3 days/yr with calibrated SPL + SQM. **Single most cited differentiator in Awasi / Chaa Creek reviews.** Cannot fake; cannot retroactively grab. Need first measurements **before** Phase-1 construction noise contaminates the baseline. | $400 instruments + Ivan's time |
| D11 | **GBIF regression in working tree** — `fetch_gbif_species.py` strips `hasCoordinate` + `basisOfRecord` filters per a prior commit. Means observation set is currently inflated with literature / fossil / unobserved records. Re-add filters and re-run; expect 20–40% record drop, much higher quality. | 2 hours |

### 1.4 Missing — P2 (project-defining if pursued)

| ID | Gap | Why |
|---|---|---|
| D12 | **Microclimate weather station** on-site — ERA5 is gridded reanalysis; on-site temperature/humidity/wind gust matters for passive-cooling Rule 6 (≤35 °C interior under closed envelope). 6-month dataset minimum before Phase-1 sizing. |
| D13 | **Phenology calendar** for the actual 5–8 canopy species, anchored to the on-site station. Drives marketing (when does the lapacho bloom this year?) + variant-A render-vs-reality fidelity check. |
| D14 | **GEDI re-pull via Earthdata Cloud Pool** (EULA blocked at 2026-06-10). 25 → ~300+ usable shots after cloud-pool consent. Already documented in STATUS §1; nobody has gone back. |
| D15 | **Property-line vs cadastral-vector reconciliation** — KML polygon is Google Earth manual draw, not surveyed cadastre. Anexo I shapes + GNSS sweep (CC-BUILD.2) close this. |

---

## 2. Render pipeline + Blender backlog

### 2.1 What ships today

- 18/18 finals at `85e86aa`, byte-pinned, SHA-anchored in deck v6 + bundle (frozen at escritura 2026-06-27).
- 17 typologies + 4 amenities all subscene-driven; sub-render-first standing rule honoured.
- 62-ha digital twin (T-DT) at `4409dba` + `83f3283` with ALOS+S2+GEDI integration.
- Post-polish wave at `78433a7`: water shader fixed, lapacho-timber wood texture wired, photoreal-flora .003 LOD name-collision resolved.
- Provenance tEXt chunks via `lqv/provenance.py` on every PNG.

### 2.2 Open items from MASTER_TODO (P1.B + P1.C, 8 + 4 = 12 rows)

| ID | What | Effort | Blocker | Tier |
|---|---|---|---|---|
| P1.B.4 | Driver wire-up per material family (post-78433a7 second-order regressions: any place that consumed water/wood/flora through the registry but locally overrode) | 1 day | None | P1 |
| P1.B.5 | Preview batch 768 PNGs (17 typologies + 4 amenities × 6 cams × A/B/C @ 128 spp) for catalogue refresh | 2 days wall-clock at serial pace | Disk: 768 × ~6 MB = 4.5 GB. Render-run GC needed first (see §6.5) | P1 |
| P1.B.6 | Framing pass — current per-asset cameras shoot too close on small typologies; revisit FOV + push-back per category | 1 day | None | P1 |
| P1.B.7 | Final batch 384 PNGs (hero-cam finals at 512 spp, others 256) after framing pass approved | ~3 days serial | P1.B.6 + GPU availability | P1 |
| P1.B.8 | `render_catalogue.md` refresh — 17 typologies + 4 amenities each get a contact sheet | 0.5 day | P1.B.7 | P1 |
| P1.C.1 | Per-variant lighting differentiation (T1.6) — A/B/C currently differ in sun_angle + HDRI but share material registry; A should warm-shift wood, C should cool-shift everything | 1 day | None | P1 |
| P1.C.2 | Background-tree replacement — current is procedural billboard, should be the cleaned photoreal canopy from T-DT | 0.5 day | None | P1 |
| P1.C.3 | 18-final re-render at refreshed framing + lighting | 1 day serial | P1.C.1 + P1.C.2 | P1 |
| P1.C.4 | `FINAL_GALLERY.md` refresh + bundle re-spin (post-escritura, not for the signed bundle) | 0.5 day | P1.C.3 | P1 |

### 2.3 Deferred / not in MASTER_TODO

| ID | Gap | Why noted |
|---|---|---|
| R1 | **`lqv/scatter_lapacho_petals` floating-petal sim** is deferred — current scatter is static on ground only. C variant could carry mid-air falling petals via a particle sim with wind force. **DO NOT TOUCH without explicit user authorization** — renderer byte-identity at `85e86aa` is on this module's hash. |
| R2 | **Material registry source-of-truth audit** — water + wood + flora are fixed; ~20 other materials (laterite, lime render, bamboo, fibre roofing, glass, steel, copper, leather, ceramic, etc.) have never had a critique pass. Likely 3–6 of them read as plastic. |
| R3 | **HDRI library coverage** — single HDRI per variant currently. Three more (early-morning fog, late-afternoon golden, post-rain wet) would expand variant-A's expressive range. CC0 only (license gate). |
| R4 | **No interior-render variant** — `RENDER_VIEW=interior` exists (P1.B.2 done at 78433a7) but no asset has been rendered with it. Buyers ask "what's it like inside" — currently answered with floorplans only. |
| R5 | **No section / cutaway render** — same status. P1.B.3 `apply_xray_override` is wired; nobody has produced the deliverable. |
| R6 | **No animation** — CC-SALES.6 ("90-second flythrough") is open. 18 stills → 90 s ken-burns is trivial (0.5 day ffmpeg). Walks the deck, doesn't replace it. |
| R7 | **GPU monoculture risk** — all 18 finals shot on the same OptiX path. Different GPU / different driver / different OIDN denoise version produces ≠ pixel output. Reproducibility doc names the host (`RTX-class + Blender 4.x + OIDN 2.x`); has not been verified on a second host. |
| R8 | **Pytest invariant coverage gap** — 16/16 tests green at all commits since 78433a7, but: RNG seed ordering invariant, MAT registry call-time lookup, and HDRI-not-fireflies are not all individually tested; some are bundled into smoke tests. Targeted unit tests would catch regressions earlier. |

### 2.4 Pyright cascade (CC-TOOL.5)

Status uncertain. Last documented sweep predates `78433a7`. Likely 10–30 new type-error candidates from material registry refactor. Untouched but ought to be re-baselined.

---

## 3. Legal / property / regulatory

### 3.1 Open ledger (RESEARCH_GAPS Tier-1 + Tier-5)

| ID | Gap | Status | Effort | Tier |
|---|---|---|---|---|
| R02 | **Anexo I of the boleto** — linderos / rumbos / medidas of each finca. Escribana Peña Ros owes. | 🔴 — overdue (was due ~5 May 2026, 8 weeks late) | $0 + chase email | P0 |
| R03 | **Municipalidad de Escobar — uso de suelo** for hospedaje + restaurante + eventos. **Entire business model contingent on this single permit family.** | 🔴 — not started | 1–2 weeks + local attorney | P0 |
| R14 | **SENATUR registration** + IVA on platform bookings + foreign-currency remittance through Booking/Airbnb | 🔴 — not started | 2 weeks + ASATUR | P1 |
| R27 | **Tax treaty NL ↔ PY** — Wesley's entity structure, dividend repatriation, capital-gains exposure | 🔴 — not started | 2 weeks + Dutch tax attorney | P1 |
| R28 | **MERCOSUR residency for Dutch nationals** — investment-visa vs retirement-visa path | 🔴 — not started | 4 weeks + Migraciones | P2 |

### 3.2 Blindspots — items NOT in RESEARCH_GAPS yet

| ID | Gap | Why it matters |
|---|---|---|
| L1 | **MADES environmental licensing** — Atlantic-Forest fragment in INFONA's restoration priority zone may trigger Licencia Ambiental at scale thresholds (commonly 1 ha+ deforestation OR water-extraction OR tourism > 30 beds). Phase 1 (4 cabins) may slip under; Phase 2 (event hall, restaurant, 12+ beds) likely does not. **Not in any current doc.** |
| L2 | **Forest-cover protection law (Ley 422/73 + Ley 2524/04 "Deforestación Cero")** — even mild ground-clearing for cabin pads in mature Atlantic Forest may require INFONA pre-approval. No mention in MASTER_TODO. |
| L3 | **Water-extraction permit** — drilled well OR stream diversion (Pelton inflow) requires SEAM / SENASA permit. Not currently tracked. |
| L4 | **Aboriginal / Guaraní cultural-heritage check** (R31 partial) — Mbopicua is Guaraní. Secretaría de Cultura + DGEEI consultation may be a legal precondition, not a courtesy. |
| L5 | **Insurance** — no fire / liability / construction-all-risk policy scoped. Affects Phase-1 capex by 1–3%. |
| L6 | **Worker safety + IPS registration** — Phase-1 build crew (~6–12 workers) must be IPS-enrolled or contracted via licensed builder. Cob-builder networks (R15) likely operate informally; legal exposure for Wesley as principal. |
| L7 | **Boleto → Escritura → Inscripción Registral** — escritura signed 2026-06-27. **Inscripción at Registro Público de la Propiedad** is the final step; typically 30–90 days post-signing. Status not tracked. **Without inscripción, title is legally complete but third-party-unenforceable.** |
| L8 | **Vendor breach window** — sellers' 5-day-hábil delivery of Anexo I was around 5 May 2026. 8 weeks overdue = boleto's specific-performance / penalty clauses may now be in scope. Lawyer should review whether to invoke. |

---

## 4. Engineering + build feasibility

### 4.1 CC-BUILD ledger (MASTER_TODO §CC-BUILD, 8 items, all 🔴)

| ID | Gap | Effort | Owner |
|---|---|---|---|
| CC-BUILD.1 | Permit-ready set (cardinal elevations + plan + section from P1.B feed) | 1 week post-P1.B | Ivan |
| CC-BUILD.2 | cm-accurate GNSS sweep of 62 ha; reconcile with COP30 | $1,500–3,000 + 2 days | Wesley + surveyor |
| CC-BUILD.3 | Soil bearing test (D2 above) | $300–800 + 1 day | civil eng |
| CC-BUILD.4 | Micro-hydro feasibility (D3 above) | $200 + 1 day | hydraulic eng |
| CC-BUILD.5 | Bottle supply chain — 3,000 wine bottles for cob_bottle wall | 4 weeks + recycling co-op | Wesley |
| CC-BUILD.6 | Cob test panel — 1 m² panel from local laterite, weather 90 days | 90 days + Ivan time | Ivan |
| CC-BUILD.7 | ANDE grid intertie decision — net-metering or off-grid | 2 weeks + ANDE visit | Wesley |
| CC-BUILD.8 | Mosquito vector audit — Rule 10 cistern mesh spec | 1 week + entomologist | Ivan |

### 4.2 Blindspots — items NOT in CC-BUILD

| ID | Gap | Why |
|---|---|---|
| E1 | **Septic / wastewater treatment** — no greywater / blackwater system spec. Atlantic Forest setting precludes leach-field upstream of any watercourse. Constructed wetland or biodigester (Vermifilter, Solifilter) needs scoping. Cost: ~$3–6k per cabin. |
| E2 | **Potable water testing** — quebrada water + any drilled well must be tested for fecal coliform, heavy metals, nitrates before guest use. SENASA does this. ~$150 + 2 weeks. |
| E3 | **Fire-suppression design** — earthen construction is fire-resistant; *thatched roofs are not*. Bottle wall (CC-BUILD.5) is glass-in-cob, also fire-tolerant. But: no extinguisher schedule, no hose-bib map, no defensible-space spec around forest-edge cabins. |
| E4 | **Lightning protection** — Cfa subtropical = 60–80 thunder-days/yr. Raised metal-frame PV (Rule 9 separates from roof) is a lightning rod absent a grounded system. No spec. |
| E5 | **Seismic** — Paraguay is low-seismicity but not zero. Stone-plinth foundation behaviour under PGA 0.05–0.10 g uninvestigated. Probably non-issue; should be stated, not assumed. |
| E6 | **Road / driveway engineering** — internal road from ruta to cluster. Drainage culverts, ford crossings of the quebrada, surface (compacted laterite vs gravel vs concrete on slopes). Not scoped. |
| E7 | **Geotechnical slope-stability** — 73.5 m relief + Cfa rainfall + laterite soils = creep + occasional slumping risk on the 13.87 ha terrace-required band. Slope-stability analysis at terrace-bench heights >2 m is missing. |
| E8 | **PV sizing math review** — `docs/energy_budget.md` exists but predates ANDE intertie decision (CC-BUILD.7). Off-grid sizing differs from net-meter sizing by 2–3× battery capacity. |
| E9 | **Internet / cell + Starlink siting** — Starlink dish needs sky window. Mature canopy at 27.7 m median means line-of-sight to satellites comes from cleared sites only. Where? |
| E10 | **Phase-2 BoQ** — `LQV_BOQ_SCOPE=phase2` exists ($19,371 delta) but no integrated rollup. P2.D in MASTER_TODO open. |

---

## 5. Commercial / distribution / market

### 5.1 Tier-1 to Tier-4 research gaps (R04–R26)

All 23 items remain 🔴 except R37 + R38 (promoted 🟡 at T+1). Highest-leverage single question per RESEARCH_GAPS:

> **R04 — Wesley's personal network in PY**: Determines whether Phase 1 timeline is 9 months (warm network) or 18+ months (cold). 30-minute conversation. Has not happened in repo's recorded history.

### 5.2 Open CC-SALES (6 items, all open)

| ID | Item | Effort |
|---|---|---|
| CC-SALES.1 | Phase-2 sales deck (12 pages, post-P1 + P2.A) | 1 week |
| CC-SALES.2 | Per-typology one-pager × 16 (programmatic from `render_catalogue` + `boq`) | 0.5 day scripting + 16 × auto-gen |
| CC-SALES.3 | European-buyer EN/DE deck — translated P0 deck for Dutch-restaurant + remote-worker angle | 1 week + native EN/DE editor |
| CC-SALES.4 | Interactive web showcase under `paragu-ai.com/s/lqv` | 2 days |
| CC-SALES.5 | Investor data room (Drive/Notion structured) | 1 week + Ivan |
| CC-SALES.6 | 90-second ffmpeg ken-burns video | 0.5 day |

### 5.3 Blindspots — not currently tracked

| ID | Gap | Why |
|---|---|---|
| C1 | **Pricing model + revenue forecast** — capex is anchored ($268,685.45 escritura BoQ; $288,056 full). Revenue side is hand-wave: "Phase 1 = 4 cabins, ADR €X, occupancy Y%". No spreadsheet. R06 (AirDNA), R12 (SENATUR) feed it but the model itself doesn't exist. |
| C2 | **Channel mix strategy** — Booking vs Airbnb vs direct vs Awasi-referral vs San-Ber-cross-promo. R37 + R38 desk research exists; no allocation %. |
| C3 | **Brand identity** — "La Quebrada Viva" is the project name. No logo, no typography, no colour palette beyond material colors. CC-SALES.3 needs this. |
| C4 | **Domain / digital presence** — `paragu-ai.com/s/lqv` is the planned home (CC-SALES.4). Not yet live. No social handles secured. **Squatter risk on `laquebradaviva.com.py` etc.** Cheap to defend ($15 + 30 min). |
| C5 | **Booking-flow stack** — Smoobu / Hostaway / Lodgify / direct on Bookingmood. R33 (Tier-5) covers it. Decision blocks Phase-1-go-live. |
| C6 | **Payment rails** — Bancard local + Stripe / Adyen / Wise for international. PYG/USD/EUR FX exposure unhedged (R29 Tier-5). |
| C7 | **Email + comms infrastructure** — no `@laquebradaviva.com` mail. Wesley's personal Gmail is current point-of-contact. Reputational risk + deliverability. |
| C8 | **Press / PR strategy** — no media list. PY hospitality / sustainability press (ABC Color, La Nación, Última Hora, plus Awasi / Chaa Creek media circles). Affects launch leverage. |
| C9 | **Reservation deposit policy** + cancellation T&C — boilerplate exists in Airbnb; bespoke direct-booking needs drafting. |
| C10 | **Guest-experience design** — arrival, welcome, on-site activity list, departure. The "5 best things to do" page does not exist. Awasi precedent: 14 named experiences. |
| C11 | **Comparables visit reports** (R18) — Iberá / Cafayate / José Ignacio / Mendoza. Owner conversations + lessons. Wesley owes. |

---

## 6. Ops / reproducibility / risk

### 6.1 MCP socket — retired

Status: dead, gitignored, documented in `docs/MCP_STATUS.md`. Revival recipe is in that doc. **Conditions to revive**: Polyhaven download (HTTPS script insufficient), Sketchfab import, Hyper3D/Hunyuan3D generation, viewport screenshot. None of those are currently on the critical path.

**Blindspot O1**: no automated reachability test — if the MCP daemon is revived and silently dies mid-session, only a manual `</dev/tcp/127.0.0.1/9876>` probe surfaces it. A 1-line CI / pre-render check would catch it.

### 6.2 Render-run accumulation

`renders/sub/runs/` holds **312 folders / 2.4 GiB** as of this audit. No GC policy. Most are stale (preview throwaways from 78433a7 development).

**Blindspot O2**: implement `make clean-render-runs` that retains only `runs/<latest 5>` + anything matching `dist/print_pack_*/` pinned SHAs. Cuts ~2 GiB.

### 6.3 Dirty-git-sha tagging

PNG provenance tEXt chunk (`lqv/provenance.py`) writes `git-sha` from `git rev-parse HEAD`. **Does not detect a dirty working tree.** A render produced with uncommitted material edits embeds the *parent commit's* SHA — silently misleading.

**Blindspot O3**: append `-dirty` when `git status --porcelain` returns non-empty. 5-line change.

### 6.4 Single-disk SPOF for satellite rasters

`docs/site_data/sentinel2/*.tif` (5 bands, 58–243 MB each) are gitignored as regenerable via `scripts/fetch_sentinel2.py` from Element84 STAC. **They live on a single local disk.** If the host loses the disk, fetch_sentinel2 can re-pull — *provided Element84 still serves that AOI + timestamp*. Sentinel-2 retention is multi-year so practically safe; not infinite.

**Blindspot O4**: a single tar.gz + cold-storage upload (Backblaze B2, Wasabi, GDrive private) of the regenerable data set costs <$1/month. Currently zero off-site copy.

### 6.5 Render parallelism ceiling

Documented hard ceiling: 1 Blender process at a time on 14 GB host (~4.3 GB RSS / process; OOMs at ×3). MCP daemon adds ~4 GB. **For P1.B.5 (768 PNGs) + P1.C.3 (18 finals re-render) this is the serial-time bound, ~5 wall-clock days.**

**Blindspot O5**: no cloud-render fallback evaluated. RunPod / Vast.ai / Lambda spot RTX 4090 at $0.20–0.40/hr. 768 PNGs ≈ 80 GPU-hours ≈ $20–30. Spot interruption risk handled by per-cam relaunch arch (already designed). Currently considered "not worth the setup"; worth re-evaluating at T+30 if local serial is still the bottleneck.

### 6.6 Backup + recovery

| Layer | State | Gap |
|---|---|---|
| Code (repo) | GitHub private at `Ai-Whisperers/la-quebrada-viva` | None — T0.1 done |
| Render PNGs | Local disk only; tracked in git LFS where used | Off-site copy missing |
| Print pack `dist/print_pack_2026-06-27/` | SHA-pinned, in repo | Should be hash-verified on a 2nd host before T+30 |
| Client photos `docs/site_data/client_photos/` | Empty placeholder | When populated, gitignored binaries need plan: bundle small (<10 MB/photo) into git; larger → GDrive |
| Bundle `wesley_bundle_20260616-1715.zip` (SHA `9ce96b…`) | In repo? Verify. | If not, archive |
| GPG / signing keys | User-side, not project | Document recovery path in `docs/_archive/` |

### 6.7 Continuity / key-person risk

| ID | Risk | Mitigation gap |
|---|---|---|
| K1 | **Ivan is sole AI Whisperers operator** on the digital side. No second-seat documentation for "how to resume" beyond CLAUDE.md + the `/resume-session` skill. Bus factor = 1. |
| K2 | **Escribana Peña Ros** is the only legal counsel touched so far. Anexo I delay (8 weeks) suggests friction — no second counsel evaluated. |
| K3 | **Wesley + Thijs concentration** — 75/25 ownership with no documented operational succession if Wesley exits. Partnership agreement may exist but not in repo. |
| K4 | **No `docs/RUNBOOK.md` for cold-start** — `/resume-session` skill loads, but a human-readable "if Ivan disappears, here's how to ship Phase-1" does not exist. |

### 6.8 Deferred bugs post-78433a7

DEFERRED_BUGS.md is closed (all 3 resolved at 78433a7). **However**: nothing tracks second-order regressions. P1.B.4 hints at "driver wire-up per material family" being the regression backstop. Confirm by running the 18-final smoke set against `dist/print_pack_2026-06-27/` SHAs — *which has not been done since 78433a7 landed*.

---

## 7. Meta / project-management blindspots

| ID | Gap | Why |
|---|---|---|
| M1 | **STATUS.md is stale at T+2** — last updated 2026-06-25 (T-2). Doesn't reflect escritura close, T+1 post-escritura pack, Phase-0 §12.A/B/C/D drops, §12.E WIP, KML scope-lock, or this analysis. Doc cohesion erodes. |
| M2 | **`docs/T_PLUS_1_DEBRIEF.md` stub remains unfilled** (per the prior compaction). 1-hour write to fill. |
| M3 | **`docs/AUTONOMOUS_PLAN.md` is T-1 content** — still goal-oriented to "post-78433a7 → escritura-close sprint". Has not been rewritten for T+2 post-escritura sprint. |
| M4 | **Decision-log freshness** — `docs/DECISIONS.md` last update at 2026-06-25 (per `4cca649`). T+1 and T+2 decisions not appended. |
| M5 | **Roast + critique cadence broken** — last honest critique pass predates `78433a7`. The polish wave fixed three named bugs; no fresh critique has surfaced what the *current* worst-three are. Per CLAUDE.md feedback memory (`feedback_critique_honest_roast`), this is a recurring need. |
| M6 | **MASTER_TODO inflation** — 76 open items, 4 levels deep (P1/P2/P3/P4 × A/B/C). No "active sprint" subset. Reading it requires the whole thing. A 10-item "this week" view would help. |
| M7 | **No retrospective on Phase-0 §12** drops (A biodiv ☑, B soilgrids cube ☑, C topology LOD ☑, D protected areas + comparables ☑ `0554b77`, E JRC GSW WIP) — what did the open-data sweep buy us? Quantified into design decisions? Or shelf-ware? Five datasets landed; zero became deck slides. |
| M8 | **Wesley + Thijs comms cadence undefined** — no weekly call, no monthly status note, no async update. T+1 one-pager existed (`docs/post_escritura_one_pager.md`) but next deliverable is undefined. |
| M9 | **The 5 unanswered "what we don't know until photos arrive" gaps** from `post_escritura_one_pager.md` §3 are not tracked as ledger items, only as prose. Move them into RESEARCH_GAPS R01-children for visibility. |
| M10 | **The `scripts/phase0_jrc_gsw_batch.py` work-in-progress on disk** is uncommitted (Phase-0 §12.E JRC Global Surface Water v1.4, 1984–2021, 50 km buffer). Either finish + ship, or park as a stub with TODO header. Stale WIP rots. |

---

## 8. Cross-domain blindspots (the ones that bridge categories)

These are not in any single doc because they span domains:

| ID | Gap | Spans |
|---|---|---|
| X1 | **No "first 4 cabins" siting decision** — 4.28 ha flat band is named; no specific x,y proposed. Drone LiDAR (D1) + client photos (D4) + Anexo I (D5) all converge here, but the *decision* (the polygon of where cabin 1 sits) doesn't exist. | Data + Engineering + Legal |
| X2 | **No Phase-1 timeline with named dates** — "9 months warm, 18 cold" is a placeholder. T+2 is the moment to draft `docs/PHASE_1_TIMELINE.md` with conditional gates (Anexo I in hand → +X, municipal permit → +Y, …). | Legal + Engineering + Commercial |
| X3 | **No public-facing "site truth" doc** — what we tell prospective guests / co-investors / Awasi / press about what's actually there. Today this is scattered across post_escritura_site_knowledge + escritura deck + RESEARCH_GAPS. A single 1-page "this is the land, here are the four numbers, here is the timeline" web copy doesn't exist yet. | Commercial + Meta |
| X4 | **Climate-change exposure (R30) is unscoped** — 20-year outlook on temperature, rainfall variability, dengue / chikungunya range expansion, forest stress (lapacho is moderately drought-sensitive). Affects: insurance pricing, mosquito audit (CC-BUILD.8), passive cooling (Rule 6), tourism seasonality, lender risk if any. | Data + Engineering + Commercial + Legal |
| X5 | **No "what we will NOT do" written down** — the no-go list (no MICE-mass-tourism, no helipad, no shoreline modification, no clear-cuts, no captive wildlife, no event-volume > X) is implicit. Writing it down protects the brand from incremental drift. Awasi has one. | Commercial + Meta + Legal |
| X6 | **No accessibility design pass** — Rule 8 says "culturally Paraguayan" but doesn't address ADA-equivalent or PCD compliance. A premium European-traveller market includes 60+ buyers; aging-in-place ramps + bathroom grab-bars matter. Cob is uniquely tolerant of curved ramps (Rule 1: no right angles). | Engineering + Commercial |
| X7 | **Climate / heritage donations & ESG narrative** — Atlantic Forest is among Earth's most-cleared biomes (93% gone). The site retains intact canopy; legal protection + restoration + GBIF-publishable observations could form a real ESG / B-Corp / GSTC story (R20). Currently used as marketing flavour, not committed-to. | Commercial + Legal + Meta |

---

## 9. Ranked recommendations — what to do next (T+2 → T+30)

Priority gradient: **leverage × time-to-procure × time-decay**.

### Critical path (next 7 days)

1. **Chase Anexo I (R02/D5)** — single email from lawyer. Free, blocks everything. 8 weeks overdue.
2. **Photo intake activation (R01/D4)** — Wesley ping. Free, unblocks 5 named gaps.
3. **Finish + ship `phase0_jrc_gsw_batch.py` (D9/M10, §12.E JRC Global Surface Water)** — 4 hours. Closes Phase-0 §12 narrative (A/B/C/D already landed; E is the last open script). Independent ground-truth for the Sentinel-2 NDWI<0 finding.
4. **GBIF regression fix (D11)** — 2 hours.
5. **Fill `T_PLUS_1_DEBRIEF.md` (M2)** — 1 hour.
6. **STATUS.md T+2 update (M1)** — 1 hour.
7. **Rewrite `AUTONOMOUS_PLAN.md` for T+2 (M3)** — 1 hour.

### Sprint 1 (T+7 → T+30)

8. **Municipal land-use (R03/X1 prerequisite)** — local attorney visit. ~$300 retainer.
9. **Soil bearing + flow measurement (D2/D3)** — combined site visit, half-day work for both.
10. **PHASE_1_TIMELINE.md (X2)** with conditional gates.
11. **R04 conversation with Wesley** — single highest-leverage research item.
12. **No-go list (X5)** — 1-hour write-up, Wesley + Thijs sign off.
13. **Render-run GC + dirty-sha provenance (O2 + O3)** — 1-day Ivan work.
14. **Off-site backup of regenerable data (O4)** — $1/month + 1 hour setup.
15. **Honest-roast critique pass (M5)** delegated to `critic` agent — surfaces the *current* top-three issues.

### Sprint 2 (T+30 → T+90)

16. **Drone LiDAR (D1/R35)** — after client photos confirm the polygon is right.
17. **Permit packet (CC-BUILD.1)** post-P1.B framing.
18. **CC-SALES.2 (per-typology one-pager × 16)** — programmatic, week of work.
19. **CC-SALES.6 (90-s video)** — 0.5 day.
20. **Phase-2 BoQ rollup (E10)** — close the `escritura` / `full` scope delta.
21. **MADES + INFONA + water permit triage (L1/L2/L3)** — engagement letter with environmental counsel.
22. **R04, R05, R12, R13, R37, R38** — desk-research items, parallelisable across the sprint.

### Backlog beyond T+90

23. P1.B + P1.C closure (Render pipeline §2.2) — only when client direction + permits are stable enough to justify a 5-day serial render burn.
24. P2 / P3 / P4 typology backlog (event hall, restaurant, glamping, etc.) — gated on R03 + R04.
25. Tier 2–4 commercial research (R09–R26).

---

## 10. Tracking + acceptance

This file lives at `docs/GAPS_ANALYSIS.md` and is the single source of truth for *what is missing*. It refreshes when:

- A gap closes → strike-through with a date + commit SHA + finding pointer.
- A new gap surfaces → add to the matching section's table with a fresh ID (`D##`, `L#`, `E##`, `C##`, `O#`, `M##`, `X#`).
- A sprint completes → §9 ranked-recommendations rewrites against the new state.

Pointers in:
- `STATUS.md` §gaps (to be added)
- `docs/AUTONOMOUS_PLAN.md` §inputs (to be added)
- `docs/MASTER_TODO.md` header (cross-reference link)

Cross-references out:
- `docs/RESEARCH_GAPS.md` — research-ledger source for §1 + §3 + §5
- `docs/MASTER_TODO.md` — backlog source for §2 + §4 + §5
- `docs/DEFERRED_BUGS.md` — closed bugs, retained as history
- `docs/MCP_STATUS.md` — §6.1 source
- `docs/post_escritura_site_knowledge.md` — §1 ground truth
- `docs/post_escritura_one_pager.md` — §7 communication baseline

---

*Generated 2026-06-29 under `/ultrawork`. Renderer byte-identity at `85e86aa` preserved — zero `lqv/`, `assets/`, or `renders/` edits in this commit. No vendor outreach proposed. License-gate constraints unchanged (CC0 + CC-BY 4.0 only in bundled deliverables; CC-BY-SA hammock excluded; OSM ODbL positional-reference only).*
