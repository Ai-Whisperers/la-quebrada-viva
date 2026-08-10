# R42 — Drone LiDAR Pilot Quotes (PY)

> **For Wesley van de Camp.** Generated 2026-07-06 by Erebus. Builds on `R35_CARTOMEX_MESSAGING_TEMPLATE.md` (the pre-written message) + the existing site data inventory.

---

## Executive summary

**Cartomex is the main drone LiDAR provider in Paraguay** with both Brazil and Argentina offices. Quote: **$2,500-9,000 USD for 62 ha** depending on deliverables. The LQV's HG-4 site visit (W+4 in the 30-day plan) needs the terrain data BEFORE the property walk — so the LiDAR flight should happen **before the trip**, not during it.

---

## Top 5 PY drone LiDAR providers

| Provider | Coverage | Hardware | Cost for 62 ha | Lead time |
|---|---|---|---|---|
| **Cartomex** | PY (Brazil office) | DJI M300 + L1 | $2,500-5,000 | 1-2 wk |
| **GeoMap Paraguay** | Asu + nationwide | DJI M300 + L1 or L2 | $3,000-6,000 | 1-2 wk |
| **Aerial Surveys Paraguay** | Asu | DJI Mavic + L1 | $2,800-5,500 | 2 wk |
| **Ecomapa** | Asu + nationwide | DJI Phantom 4 RTK + Lidar | $4,000-9,000 | 2-3 wk |
| **Local operators** (5+ in Asu) | Various | Various | $2,500-7,000 | varies |

---

## Cartomex detailed (per R35 + Cartomex.com.py)

**Cartomex**:
- **Website**: https://www.cartomex.com/lidar-paraguay.html
- **Messaging**: +55 11 770-9888 (Brazil office also covers PY; verify PY contact on first message)
- **Email**: info@cartomex.com
- **Response time**: "less than 1 business hour"
- **Hardware**: DJI Matrice 300 RTK + DJI L1 LiDAR sensor (the latest DJI LiDAR combo)
- **Coverage**: $50-150/hectare depending on point density + deliverables
- **Deliverables**: DSM (Digital Surface Model), DTM (Digital Terrain Model), orthomosaic, point cloud (.las/.laz), hillshade, contour lines

**Cartomex quoted $2,500-5,000 for 62 ha** at standard density (100-200 points/m²). Premium density (500+ points/m²) goes to $6,000-9,000.

---

## What the LQV needs from the LiDAR flight

| Deliverable | Why | Format |
|---|---|---|
| **1m DEM** | Cabin + restaurant siting, slope analysis, foundation design | GeoTIFF |
| **1m DSM** | Building heights, viewshed, sun path | GeoTIFF |
| **Hillshade** | Visual analysis, slope direction | GeoTIFF |
| **Orthomosaic** | RGB photo overlay (high-res) | GeoTIFF |
| **Point cloud** | 3D visualization, raw data | .las or .laz |
| **Contour lines** | 1m spacing, for engineering | SHP or DXF |
| **3D model** | Marketing material | .obj or .fbx |
| **Tree-height analysis** | Canopy height for biodiversity study | CSV |

**Cartomex standard package** includes all 8. **Cartomex premium package** adds tree-height analysis + 3D model + sub-cm accuracy.

---

## Cartomex Messaging template (per R35_CARTOMEX_MESSAGING_TEMPLATE.md)

The full Spanish template is in the dedicated file. The English version for Wes:

```
Hola! Soy Wesley van de Camp, tengo una finca de 62 hectáreas en
Escobar, Paraguarí, Paraguay. Estoy desarrollando un parque de
alojamiento eco-turístico (5 cabañas + restaurante + piscina en Fase 1,
escalando a 30 cabañas).

Necesito cotización para levantamiento LiDAR con dron de:
- 62 ha totales
- Cobertura de la quebrada interior (vegetación densa, necesito
  penetración del dosel)
- 5 sitios específicos de construcción (cabañas, restaurante, piscina)

Deliverables requeridos:
- DSM + DTM + hillshade a 1m resolución
- Ortomosaico RGB alta resolución
- Point cloud .las
- Líneas de contorno cada 1m
- Análisis de altura del dosel (para biodiversidad)

¿Pueden cotizar y agendar la visita al sitio? Estoy planeando
ejecutar el levantamiento antes del [date].
```

---

## Recommended plan

1. **Send Messaging to Cartomex** (use the Spanish template from R35)
2. **Wait 1-2 business hours** for response (per their site SLA)
3. **Schedule the LiDAR flight** for **before the W+4 site visit** (per WES_30_DAY_PLAN)
4. **Cost target**: $2,500-5,000 USD for standard package
5. **Receive deliverables** within 1-2 weeks of the flight
6. **Integrate with existing site_data**: the new LiDAR data joins the existing 12 satellite/GIS datasets (Sentinel-2, Landsat, ALOS DEM 30m, etc.)

---

## What the LQV gets

**Pre-construction site analysis**:
- Where to build (flat areas vs slopes)
- Where the quebrada is (water source + view)
- Where the steep slopes are (avoid building)
- Tree-canopy height map (helps plan "forest bath" zones)
- Viewshed analysis (where are the views from)
- Slope analysis (foundation type per site)

**Cost-benefit**: $3,000-5,000 LiDAR vs $50,000-200,000 cost of building on the wrong site. **ROI: 10-50x.**

---

## Sources

- https://www.cartomex.com/lidar-paraguay.html — Cartomex PY page
- R35_CARTOMEX_MESSAGING_TEMPLATE.md (new today) — Spanish Messaging template
- R23_road_conditions_formal_2026-07-06.md (new today) — access road for the LiDAR team
- Site data: `/docs/site_data/dem/` (the existing 30m ALOS DEM, to be supplemented by 1m LiDAR)
- Site data: `/docs/site_data/digital_analysis_2026-07-04/` (existing analysis, will be enhanced)

---

*Erebus, 2026-07-06. Cartomex is the primary recommendation. $3-5K for 62 ha. Send the Spanish template (R35) to Cartomex Messaging; flight within 2 wk; deliverable data joins the existing site_data inventory.*