# Cluster Plan — Cataratas del Monday Test Scene

> Test pipeline for the real client project. We use the Monday site as a stand-in
> to prove the topology-driven house-placement workflow before swapping in the
> real LQV/Paraguarí parcel once Wesley delivers the Anexo I.

## AOI & topology basis

- **Center** (OSM node 4218536799, height 40m, Q880046): -25.5627515, -54.6323698
- **Site box**: 1 km radius from the cascade center
- **DEM**: 2.5 m horizontal (terrarium) — 2.5 m vertical RMSE, 116-235 m AMSL
- **Imagery**: 0.54 m/pixel (Esri z=18) over the 2.5 km box
- **Creek path**: Río Monday (south side) — the natural feature houses cluster around

## Why 4 clusters around a creek

The user's reference set (Labrisa Lounge, Eco Resort, Bamboo River House, etc.) is
**all about a single design idea**: a creek running through a tropical retreat, with
houses that touch the water in different ways. So the test scene is 4 clusters
positioned along a 1-km stretch of the Río Monday, each with 3 houses that show
different house-water relationships. Total 12 houses + 1 community space = 13
structures.

## Cluster layout (2km box, 1km radius from OSM node 4218536799)

UTM 21J center: E 737860, N 7170615

| Cluster | Style | House 1 | House 2 | House 3 | Anchor |
|---|---|---|---|---|---|
| **A — Italian** | Mediterranean villa, stone, arched iron doors | Italian small (5.5x4.0, 22m²) | Italian mid (6.2x4.2, 22m²) | Italian River House 4p (8.5m × 2/3 on stilts) | Upper terrace, cobble path |
| **B — Bamboo** | Curved canopy, thatched, concrete base | Bamboo compact (6.0m round) | Bamboo 2-bed (9.8m dome, 75m²) | Wigwam 7.5m × 6.6m | Mid-slope, palms |
| **C — Over the Creek** | Built on stilts, hang net, glass front | Bamboo River House 7.2m (2x) | Container 12.2m | Edge of the Río Monday, on stilts |
| **D — Earth & Tree** | Earth-sheltered, treehouse, premium glamping | Hobbit House 7.6m round | Bamboo Boomhut 5.5m | Stilt treehouse, hidden in canopy |

**Communal** (1x, between A and C): Labrisa-style lounge with terraced stone
seating, hammock platforms over the creek, central fire pit, yoga deck.

## 12-house count by typology

| Typology | Count | Footprint range |
|---|---|---|
| Italian villa (small) | 1 | 22m² |
| Italian villa (mid) | 1 | 22m² + 12m² terrace |
| Italian River House 4p | 1 | 55m² |
| Bamboo compact | 1 | 28m² |
| Bamboo 2-bed family | 1 | 75m² |
| Bamboo Wigwam | 1 | 42m² |
| Bamboo River House | 2 | 32m² each |
| Container River House | 1 | 28m² |
| Hobbit House | 1 | 38m² |
| Bamboo Boomhut (treehouse) | 1 | 20m² |
| Labrisa community lounge | 1 | (variable) |
| **Total** | **12 + 1 = 13** | |

## Topology data flow

1. Load 2.5m terrarium DEM (`dem/terrarium_monday_2_5m_utm21j.tif`)
2. Compute slope, hillshade, NDVI from S2
3. Identify flat-ish areas (slope < 15°) for house placement
4. Identify creek path from OSM waterway `way 543393748` (cliff way) + NDVI < 0.2 strip
5. Place 12 houses along creek, ~30-50m apart, with 5m setback from cliff edge
6. Add communal lounge near the center of the run, where the creek makes a natural bowl

## What this tests

- Topology-driven placement (real DEM, not a flat plane)
- Multi-typology variation (one scene = 10 different house shapes)
- Material/lighting consistency across typologies
- Render at full LQV quality (Cycles GPU, 256-512 samples, AgX Punchy)
- Cliff edge respect (5m setback from 30°+ slopes)
- Creek proximity (houses at distance 5-30m from water)
- Lighting of bamboo/stone/lime-wash surfaces at sunset (Variant A baseline)

## What this does NOT test (deferred to real client site)

- Anexo I boundary (no real parcel yet)
- Real vegetation species count (we'll use Monday's 41% forest baseline)
- Per-house customization (Wesley's cultural notes)
- SENATUR / municipal constraints
- Real client-specific materials (we use Monday basáltica as proxy)
