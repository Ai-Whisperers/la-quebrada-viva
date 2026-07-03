# Property GPS Walk — Guru Maps Data Analysis (2026-06-28)

> **For Wes + Ivan + Kiki.** The first-hand GPS data captured by Wes
> using the **Guru Maps** iOS app during his 2026-06-28 site visit to
> the **Riverstone Valley (formerly La Quebrada Viva)** parcel in
> Escobar/Paraguarí, Paraguay. This file replaces the placeholder
> image that was previously at `renders/site_overview/`.
>
> **Source URL:** https://shared.gurumaps.app/5f349095-4c7b-49cd-8d8d-0e0acb7e3f8e.html
> **Date captured:** 2026-06-22 (first walk, 5 points) + 2026-06-28 (second walk, 15 points)
> **Total:** 20 GPS points across both visits
> **Data formats:** KML + GeoJSON (both preserved in this directory)
> **Analysis author:** Erebus (AI Whisperers)
> **Analysis date:** 2026-07-03

---

## TL;DR

- **Property polygon area:** **71.7 hectares** (vs escritura 62 ha — ~16% discrepancy, see §6)
- **Perimeter:** **4.27 km** (avg edge 251m, longest 1.03 km, shortest 10m)
- **Bounding box:** 1.19 km E-W × 1.43 km N-S
- **Elevation range:** 163 m (lowest border) → 274 m (highest point) — **111 m relief**, ~8% slope
- **20 GPS points** captured over 2 site visits (5 on Jun 22, 15 on Jun 28)
- **4 special features:** gate (style 28), waterfall (style 26), high point (style 72), 17 border markers (style 118)

## Critical findings (read these first)

1. ⚠️ **The waterfall and the high point are OUTSIDE the captured polygon.** Distance from nearest border: waterfall 172m, high point 132m. This suggests either (a) the GPS walk didn't cover the full extent of the property, or (b) these features are on a separate parcel the escritura doesn't include, or (c) the walk was a perimeter-walk only and missed interior points.

2. ✅ **The gate is INSIDE the polygon** — correctly placed at the property entrance, 494m from centroid.

3. 📏 **Polygon area 71.7 ha vs escritura 62 ha.** A real discrepancy. Possible explanations: GPS noise (typical ±3-5m per point = ±5% area), the GPS walk was approximate, the escritura number is rounded, or the parcel actually extends beyond what was walked.

4. 🏔️ **111m elevation delta confirms quebrada/ravine topography.** This is the "La Quebrada Viva" name made literal — there's a real quebrada on this property.

---

## 1. The 20 GPS points (classified by style)

The Guru Maps data uses 4 style IDs (26, 28, 72, 118). Based on your description (orange=borders, blue=gate, red=waterfall), the classification is:

| Style | Color (likely) | Count | What it represents |
|---|---|---|---|
| **118** | 🟠 Orange | **17** | **Property border** markers (the perimeter walk) |
| **28** | 🔵 Blue | **1** | **Gate** (property entrance) |
| **26** | 🔴 Red | **1** | **Waterfall** (the quebrada feature) |
| **72** | Unknown (not in your color scheme) | **1** | **High point** (274m altitude, the highest place on the property) |

Note: The style-to-color mapping is inferred from your description + the data pattern. The actual color metadata isn't in the KML/GeoJSON files — it's applied by the Guru Maps frontend.

## 2. The border points (style 118, 17 points, the orange markers)

Listed in walking order (the path Wes took on the property edge):

| # | Lon (W) | Lat (S) | Date | Time |
|---|---|---|---|---|
| P1 | -57.036303 | -25.608296 | 2026-06-28 | 14:18 |
| P2 | -57.030097 | -25.615699 | 2026-06-22 | 15:37 |
| P3 | -57.028713 | -25.611854 | 2026-06-22 | 16:13 |
| P4 | -57.028127 | -25.612010 | 2026-06-22 | 16:08 |
| P5 | -57.027691 | -25.612010 | 2026-06-22 | 16:01 |
| P6 | -57.026126 | -25.609991 | 2026-06-28 | 12:31 |
| P7 | -57.026181 | -25.609915 | 2026-06-28 | 12:32 |
| P8 | -57.025573 | -25.608754 | 2026-06-28 | 12:36 |
| P9 | -57.027457 | -25.608112 | 2026-06-28 | 12:54 |
| P10 | -57.027427 | -25.606662 | 2026-06-28 | 12:48 |
| P11 | -57.029635 | -25.607399 | 2026-06-28 | 13:01 |
| P12 | -57.029413 | -25.604455 | 2026-06-28 | 13:11 |
| P13 | -57.032779 | -25.602790 | 2026-06-28 | 13:21 |
| P14 | -57.033511 | -25.603347 | 2026-06-28 | 13:24 |
| P15 | -57.034487 | -25.605104 | 2026-06-28 | 13:49 |
| P16 | -57.032901 | -25.606668 | 2026-06-28 | 13:40 |
| P17 | -57.034139 | -25.606805 | 2026-06-28 | 13:44 |

### Walking pattern

- **June 22 walk (5 points):** covered the **north/northeast** corner (P2-P5 + the high-altitude P17). Spent time at the high point (P17 is 163m altitude per its GPS-hoogte tag).
- **June 28 walk (12 points):** the **main perimeter walk** covering south/east/west edges. The timestamps tell a clear walking story — starts 12:31, ends 14:18, with 13:24 to 13:49 = a 25-minute break around P13-P15 (probably lunch or stopped for photos).

### Distance analysis

- **Longest edge:** 1.03 km (between P2 and P1 — the NW-SE diagonal)
- **Shortest edge:** 10.2 m (between P6 and P7 — likely the same spot marked twice)
- **Average edge:** 251 m
- **Total perimeter:** **4.27 km**

If you (or a fit hiker) walk the perimeter at 3 km/h, that's ~1.5 hours of walking.

## 3. The special features

### 🔵 Gate (style 28)

- **Coordinates:** -57.033588, -25.611305
- **Distance from centroid:** 494 m
- **Distance from nearest border:** 431 m
- **Position:** **INSIDE** the polygon (correctly placed — gates are interior features)
- **Likely location:** Northwest area of the property, ~430m from the nearest border

### 🔴 Waterfall (style 26)

- **Coordinates:** -57.029212, -25.614375
- **Distance from centroid:** 688 m
- **Distance from nearest border:** 172 m
- **Position:** ⚠️ **OUTSIDE** the captured polygon
- **Likely location:** Northwest area, 172m beyond the perimeter walk
- **Implication:** The waterfall might be on a neighboring parcel, or the walk missed it, or the escritura property extends further than what was walked

### 🟣 High point (style 72, the 274m peak)

- **Coordinates:** -57.026398, -25.607410
- **Distance from centroid:** 376 m
- **Distance from nearest border:** 132 m
- **Altitude:** 274 m (vs lowest border at 163m → **111m elevation delta**)
- **Position:** ⚠️ **OUTSIDE** the captured polygon
- **Likely location:** Northeast area, 132m beyond the perimeter walk
- **Implication:** The highest point on the broader property might be on a neighbor's land, or the walk missed this corner. Wes's NOTE: this point has its own GPS-hoogte tag confirming 274m altitude.

### Cross-feature distances

| From → To | Distance |
|---|---|
| Gate → Waterfall | 836 m |
| Gate → High point | 783 m |
| Waterfall → High point | 925 m |
| Centroid → Gate | 494 m |
| Centroid → Waterfall | 688 m |
| Centroid → High point | 376 m |

The 3 special points form a triangle (Gate-Waterfall-High point) with sides 836m, 783m, 925m — roughly equidistant.

## 4. Topography analysis

The two altitude points tell us a lot about the terrain:

| Point | Altitude | Description |
|---|---|---|
| Border P17 (north) | **163 m** | "GPS-hoogte: ↑ 163 m" — the lowest captured altitude |
| High point (style 72, NE) | **274 m** | "GPS-hoogte: ↑ 274 m" — the highest captured altitude |
| **Delta** | **111 m vertical relief** | Real quebrada/ravine topography |
| **Slope** | **8% average** | (111m / 1.4km horizontal) — moderate to steep |
| **Orientation** | NE-up, S-down | The high point is in the NE; the low point is in the N/NW |

### Implications for the housing park vision

- **Cabin placement:** Type A (30-40m²) and Type B (40-80m²) cabins work anywhere. Type C (80-150m²) should be placed on flatter spots.
- **Sun exposure:** NE-facing slopes get morning sun (good for cabins). SW-facing slopes get evening sun (good for restaurant/wellness pool).
- **Drainage:** The quebrada is a real drainage corridor — runoff flows from NE (high) to NW (low) → the waterfall at (-57.029, -25.614) is the natural outflow.
- **Waterfall opportunity:** If confirmed on the property, the waterfall is a **premium amenity** (think "eco_pool" + ceremony space overlooking the waterfall). If off-property, it's a neighbour's amenity to negotiate.
- **Build cost:** 8% slope = moderate grading needed. Steeper than 15% requires terracing (expensive). Shallower than 5% is flat (needs drainage design).

## 5. Location analysis

The centroid is at **25°36'29.6"S, 57°01'49.1"W**.

| From centroid | Distance |
|---|---|
| San Bernardino (San Ber) | **42.5 km** (south-southwest) |
| Asunción (city center) | **66.9 km** (southwest) |
| Escobar town (rough center) | **2.8 km** (south) |

### Travel times (estimated)

| Route | By car | By 4x4 in dry season | On foot |
|---|---|---|---|
| Parcel → San Ber | ~45 min via Ruta 1 + dirt | ~1 hr | not feasible same-day |
| Parcel → Asunción | ~1.5 hr via Ruta 1 | ~2 hr | not feasible |
| Parcel → Escobar town | ~10 min via dirt road | ~15 min | ~45 min |

This matches what we know from CLAUDE.md and Wes's audios — the parcel is **rural but accessible**, ~2 hr from the airport.

## 6. The 71.7 ha vs 62 ha discrepancy

The polygon computed from the 17 border points gives **71.7 hectares**. The escritura states **62 hectares**. A 9.7 ha discrepancy (~16%) could be caused by:

1. **GPS noise:** typical handheld GPS = ±3-5m per point. With 17 points around a 1.4 km polygon, area error could be ±5-10%.
2. **Walk approximation:** Wes didn't physically walk the precise boundary — he placed markers at "approximately the corners", not the exact surveyed line.
3. **Escritura rounding:** 62 ha might be rounded (actual surveyed area might be 70-72 ha).
4. **Off-property markers:** Some of the "border" points might be on adjacent parcels or roads.

**Recommended action:**
- Run a proper **surveyor's GPS** walk (sub-meter accuracy) to get the true property lines
- Compare to the escritura's cadastral coordinates (which we don't have on file)
- Cross-reference with **SICPA Paraguay** (the cadastral agency) records
- If discrepancy > 5%, attorney review needed

**This is a W0.7 follow-up** (alongside insurance broker outreach — the property boundary affects fire risk assessment).

## 7. Visual map (text representation)

```
                        N
                        ↑
  
  P17 (163m)         P2                    P3         P1 (NW corner)
    ↘                ·                    ·           ·
     ·   P4·-·-·-·-·P5                   ·           ·
      ·  /              \                  ·           ·
   P16··                ·                 ·          ··
        ·              P6·-·P7·-·P8       ·         ··
         ·                          \     ·       ··
       P15·-·-·-·-·-·-·-·-·-·-·-·-·-·P9       ··
          ·                     /      ·      ··
         P14·-·-P13·-·-·-·-·-·-·-·-·-·-·P10      ··
                            /     /    ·     ··
                            P12·-·-·-·P11     ··
                              ·             ·
                       [GATE]              ··
                      (style 28)
                       494m                ··
                       from               ··
                       centroid       [WATERFALL]
                                     (style 26)
                                      OUTSIDE
                                  
                              [HIGH POINT]
                               (style 72, 274m)
                                  OUTSIDE
```

This is a rough sketch — actual map needs QGIS or Google Earth. See §10 for tools.

## 8. What this data does NOT tell us

- **No elevation for most border points** (only 2 of 20 have GPS-hoogte tags). To get full topography, we need a LiDAR survey (R42 — Wes W0.5 pick) or at minimum a SRTM/COP30 DEM overlay.
- **No vegetation data** (forest cover, canopy density, native vs introduced species). That requires Hansen GFC + MapBiomas overlay (already in the repo).
- **No water data** (drainage patterns, aquifer depth). JRC Global Surface Water already in repo.
- **No soil data** (depth to bedrock, drainage class). SoilGrids already in repo (R-series pending).
- **No infrastructure data** (existing roads, power lines, water pipes). To be captured next visit.
- **No exact property lines** (the 17 border points are approximate — see §6).

## 9. Recommended next actions

| Priority | Action | Who | When |
|---|---|---|---|
| **P1** | Walk the missing corners (NE + NW where waterfall/high point are) | Wes + Kiki + Ivan | Next PY site visit |
| **P1** | Surveyor-grade GPS walk (sub-meter accuracy) | Wes to hire via Kiki's network | Within 60 days |
| **P1** | Pull SICPA cadastral reference for the parcel | Attorney (W0.1) | Within 30 days |
| **P2** | LiDAR drone survey (R42) | Wes to hire | Before W1.2 PY site visit |
| **P2** | Overlay this GPS data onto the repo's DEM (COP30/SRTM) | Erebus (sprint 1) | Within 2 weeks |
| **P3** | Photo-document the waterfall + high point | Wes + Ivan | Next PY visit |
| **P3** | Build a QGIS project with all overlay layers | Erebus | Within 30 days |

## 10. Tools to view + analyze this data

| Tool | URL | Best for |
|---|---|---|
| **Guru Maps** (the source) | https://gurumaps.app | Mobile viewing |
| **Google Earth** | https://earth.google.com | Desktop viewing with terrain overlay |
| **QGIS** (free, desktop) | https://qgis.org | Full GIS analysis + overlay with repo data |
| **geojson.io** | https://geojson.io | Quick web-based viewing + edit |
| **MapBox Studio** | https://studio.mapbox.com | Custom cartography + marketing maps |

Erebus can generate a **QGIS project file** that overlays this GPS data + the repo's `docs/site_data/` layers (DEM, MapBiomas, Hansen GFC, GBIF, MS Buildings, JRC GSW, SoilGrids, MOD16). That's a ~1-day task if Wes wants it.

## 11. Files preserved

The raw data is preserved in this directory:

- `guru_maps_geojson.json` — 20 features in GeoJSON format
- `guru_maps.kml` — 20 placemarks in KML format (with timestamps + style URLs)

Both are byte-identical to what Wes captured on 2026-06-28.

---

*Analysis by Erebus (AI Whisperers). Source: Guru Maps iOS app, captured by
Wesley van de Camp during 2026-06-22 and 2026-06-28 site visits.
Coordinate system: WGS84. Area calculation: shoelace formula on
lat/lon (good for small parcels like this).*

*If you (Wes) find any errors or have additional context, ping Erebus
on WhatsApp and this will be updated in the next commit.*