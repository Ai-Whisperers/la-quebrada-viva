# Paraguay Clay & Bottle Smart House — Master Research Document

**Project:** La Quebrada Viva — Clay and bottle earthen smart home, eastern Paraguay  
**Owner:** Ivan Weiss Van Der Pol — Senior Data Engineer / AI Whisperers, Asunción, Paraguay  
**Status:** Research and design phase — Blender render in development  
**Last updated:** June 2026

---

## 1. Project Identity

The house is a cob/earthen structure using Paraguay's red laterite clay as the primary wall material, embedded with glass bottle walls that function as stained-glass light sources, topped with a living sod roof planted with native Paraguayan species including lapacho (tajy). It is designed around Guaraní and Spanish colonial form language: covered gallery (corredor), interior courtyard, tatakuá dome oven, low-pitched roof, lapacho timber structural elements.

The house is fully self-sufficient: solar PV + LiFePO4 battery bank, spring-fed stream water, rainwater cistern, greywater reed bed, composting toilet. A small run-of-stream micro-hydro turbine at the existing weir provides 24/7 baseline power.

The home sits on a real property in eastern Paraguay's Atlantic Forest region. The render is the first deliverable; a real build is the eventual goal.

---

## 2. The Site — La Quebrada Viva

### 2.1 What the photographs reveal

The property is in Paraguay's eastern Paranaense region (confirmed by red laterite soil, sandstone cliff formation, Atlantic Forest species mix). It contains five distinct zones:

**Zone 1 — Sandstone escarpment:** A dramatic cliff face 40–60m high rising from dense subtropical forest. This creates a permanent cool air drainage effect at night — cold air flows down from the rock face through the forest and pools in the valley. The house should be oriented to receive this nocturnal airflow through north-facing ventilation openings.

**Zone 2 — Entrance and existing structures:** A wooden farm gate on red dirt track. Two existing constructions: a light blue rendered block house with covered gallery (corredor) and a 500L Fibrao roof tank, and a white/grey quincho with corrugated metal roof. ANDE power pole with transformer on site — grid connected but fragile. The existing house validates the corredor gallery as the correct form language for this climate.

**Zone 3 — Colonial stone terraces:** A series of moss-covered dry-stack sandstone terraces cut into the natural slope, clearly 50–100+ years old. Multiple levels connected by stone steps. Agave (Agave americana) colonizing the lower terraces. This is the Jesuit/colonial estancia garden layout. These terraces are the recommended build platform — already elevated, already drained, already bounded by stone walls that can serve as the cob house foundation perimeter.

**Zone 4 — The living stream system (the most important site asset):** A spring-fed stream descending from the escarpment, year-round flow confirmed. The stream has:
- Multiple cascade drops of 1–1.5m each
- A wide flat-rock pool (natural swimming hole, needs only a light sill to raise water level 20–30cm)
- Large moss-covered boulders (grey quartzite/sandstone, 1–2m)
- Concrete weirs with wooden footbridges already installed
- Dense riparian vegetation: bamboo, aroids, tree ferns
- Water carries red laterite sediment — colour #A85832 in shallows, dark grey-green over bedrock

The stream is a micro-hydro energy source. The existing weir creates sufficient head pressure (1–2m drop) for a Pelton wheel or Turgo turbine producing 200–400W continuously, 24 hours a day regardless of cloud cover. This provides always-on baseline power for sensors, networking, and refrigeration.

**Zone 5 — The forest:** Dense subtropical Atlantic Forest fragment. Species mix: mangoes (dominant canopy), pindo palms (Syagrus romanzoffiana), lapacho (Handroanthus impetiginosus), cedro, hardwoods, secondary growth. The canopy is multi-layered and provides massive natural shading — reducing surface temperatures by 10–15°C in summer. Every mature tree must be preserved.

### 2.2 Recommended build position

The house sits on the upper stone terrace platform. Rationale:
- Already elevated above flood risk
- Stone terrace walls serve as foundation retaining walls
- 15–20m from the stream — safe from flooding but audible
- Mature tree canopy above provides year-round shade
- Faces downhill toward the stream and glade — the view
- Back wall faces the escarpment — cool air source
- The micro-hydro turbine house is built at the weir in the same sandstone, 30–40m downhill

### 2.3 Exact material colour references from photographs

| Material | Description | Approximate hex |
|---|---|---|
| Stream water (shallow/turbid) | Red laterite suspension | #A85832 |
| Stream water (deep/clear) | Over dark bedrock | #2A3528 |
| Laterite ground (dry) | Orange-red compacted soil | #C4522A |
| Laterite ground (wet) | Dark saturated red | #8B3A1A |
| Boulders (shadow face) | Dark grey quartzite | #3C4035 |
| Boulders (lit face) | Medium grey | #6B7060 |
| Moss (wet / stream-adjacent) | Bright chartreuse | #8BA048 |
| Moss (dry / shade) | Dark olive | #3D4F1A |
| Stone terrace wall | Warm dark sandstone | #5F4A35 |
| Stone joint / shadow | Near-black brown | #3A2D20 |
| Mango canopy (dense) | Very dark green | #1A3A1A |
| Mango canopy (lit edge) | Medium green | #4A7A2A |

---

## 3. Paraguay Climate — Hard Constraints

### 3.1 Temperature and humidity

- Summer peak: 38–45°C with 70–77% relative humidity simultaneously (feels like 48°C+)
- Winter average: ~17°C. Cold snaps to -2 to -6°C when Antarctic air pushes north (rare but real)
- Coldest month: July. Warmest month: January
- Annual average: ~23°C
- 2019 was record hottest year: 24.3°C average, 1.5°C above the 1961–1990 baseline

### 3.2 Rainfall

- Annual average: 1,270mm (50 inches)
- Distribution: irregular — weeks without rain, then torrential downpours
- Peak periods: March–May and October–November
- Driest period: July–August
- 85% of yearly rain falls in rainy season

### 3.3 Extreme events

- Flooding: the Paraguay River floods Asunción regularly. 60,000 displaced in 1982–83, 50,000+ in 2015–16. Flash floods from pluvial rain are separate from river flooding
- Less than 20% of flood-vulnerable areas in Asunción are covered by drainage systems
- Severe storms: October–April, can overwhelm any drainage
- Dengue / Zika / Chikungunya: Aedes aegypti mosquitoes active year-round. 2022–23 chikungunya outbreak: 81,000+ cases. 2023 set the Americas record for dengue cases

---

## 4. Infrastructure Problems in Paraguay

These are not abstractions — they are the practical reasons the house must be self-sufficient:

**Power grid:** Frequent outages. The distribution grid was not designed for current demand levels. New construction connects to stressed systems without mandated upgrades. Paraguay's electricity is 99.9% renewable hydropower but the distribution infrastructure is fragile. Off-grid solar is already commercially marketed as the direct alternative.

**Water:** Water distribution network not designed for current demand. Water contamination spikes during flooding. Absence of wastewater treatment in many areas. Even in affluent Asunción neighbourhoods, garbage accumulates and drainage is patchwork.

**Drainage:** Less than 20% of flood-vulnerable areas covered by the city drainage system. Flash flooding from normal rain is routine.

**Pests:** Mosquitoes (dengue vector), termites (year-round in tropical climate), ants, cockroaches. All are active threats in organic-material construction.

---

## 5. Earthen Architecture — Technical Requirements

### 5.1 Cob construction

Cob is a mixture of clay-rich soil, aggregate sand, straw fibre, and water mixed to a stiff dough that can be stacked and sculpted. Paraguay's red laterite clay is ideal as a base material. Key properties: excellent thermal mass, monolithic walls (no cavities for hidden mold), highly sculptable, organic curved forms possible.

### 5.2 Bottle walls

Paired glass bottles (mounted mouth-to-mouth, bottoms facing outward) embedded in sections of the wall using lime mortar (not cob — lime is more water-resistant). Creates a stained-glass effect transmitting coloured light into the interior. Bottle colours: cobalt blue, amber, green, clear brown. Pattern: organic clusters, not uniform grids. Historic precedent: Laurie Baker's buildings in India, Mike Reynolds' Earthships in Taos.

### 5.3 The non-negotiable rules for clay in humid subtropical Paraguay

1. **Never cement plaster on cob** — it traps moisture and destroys the wall. Always lime plaster: vapor-permeable, alkaline (anti-mould), self-healing micro-cracks
2. **Lime wash finish** — multiple coats over lime plaster. White reflects heat. Breathes. Additional anti-fungal layer
3. **Wide roof overhangs — minimum 90cm on all sides** — the single most important protection for earthen walls in this climate
4. **Raised foundation — minimum 60cm above grade** — stone rubble base. Clay walls must never touch soil directly
5. **Rubble trench drainage** — perforated pipe in gravel trench around the entire perimeter
6. **Termite barrier** — physical stainless steel mesh collar at foundation level
7. **Clay and lime can buffer indoor humidity swings by 10–20%** — this is the passive climate control mechanism

### 5.4 Passive cooling — what works in humid subtropical (not desert)

Works:
- Cross-ventilation: opposing openings at low and high points for stack effect
- Thermal mass: clay walls absorb heat during day, release at night
- Courtyard design (traditional Paraguayan): shaded outdoor room creates convection cooling
- Deep roof overhang shading walls and windows
- Earth berming on south-facing walls (the cool face in Southern Hemisphere)
- Night purging: open all vents after sunset, flush warm air
- Living roof insulating against radiant heat gain from above
- White lime exterior reflecting rather than absorbing solar radiation

Does NOT work in high humidity:
- Evaporative cooling — useless above ~60% relative humidity
- Earth air tunnels — create condensation and mould risk in humid climates
- Heavily sealed buildings — earthen walls need to breathe
- Traditional Earthship south-facing glass wall emphasis — designed for New Mexico desert, causes overheating in subtropical summer

---

## 6. Smart Home Technical Stack

### 6.1 Ivan's existing homelab

- Home Assistant on Ubuntu 24.04 (local, no cloud dependency)
- n8n for workflow automation
- Docker containers
- Claude Code with MCP servers configured
- ROCm for AMD GPU acceleration

### 6.2 Recommended sensor deployment

| Sensor | Location | Purpose |
|---|---|---|
| Temperature + humidity (DHT22 or SHT31 Zigbee) | Each room | Comfort monitoring |
| Wall moisture sensors (capacitive, 3 depths) | In cob walls | Early water intrusion detection |
| Cistern level (ultrasonic) | Cistern | Water security |
| Cistern TDS + pH (ESP32 bridge) | Cistern | Water quality |
| Flood perimeter sensors | Foundation level | Flood early warning |
| CO2 / IAQ (SCD40) | Occupied spaces | Air quality |
| Weather station | Exterior | Full meteorological data |
| Solar production + battery SOC | Inverter/BMS | Energy management |
| Stream level sensor | Stream | Micro-hydro monitoring + flood warning |

### 6.3 Key automations

- **Night ventilation:** auto-open stack vents when exterior temp < interior AND no rain detected
- **Storm lockdown:** close all motorised vents when rain rate exceeds threshold
- **Flood alert:** WhatsApp notification at 3 escalating thresholds (watch / warning / evacuate)
- **Battery low:** shed non-essential loads below 30% SOC, protect water pump and comms
- **Dengue watch:** pull SENEPA outbreak data feed via n8n, alert when neighbourhood risk elevated
- **Pre-cool:** run AC in sleeping areas 17:00–21:00 during solar peak hours

### 6.4 Platform

- **Home Assistant** as local hub — all automations run offline
- **Zigbee** mesh for sensors (better clay wall penetration than WiFi; repeaters in bottle wall sections which have less mass)
- **MQTT** as internal message bus
- **n8n** bridges Home Assistant to WhatsApp, external APIs, logging, SENEPA feeds

---

## 7. Water Systems

### 7.1 Stream-based (new — enabled by site)

- **Run-of-stream micro-hydro:** Pelton or Turgo turbine at the existing weir. 1–2m head, reasonable flow = 200–400W continuous 24/7. Turbine house built in matching sandstone, 30–40m downhill from the house
- **Gravity-fed non-potable supply:** House sits above stream. Pipe feeds garden, reed bed, fire suppression
- **Natural swimming pool:** The flat-rock pool (photographs clearly show this feature) dammed lightly with a stone sill. No liner needed — natural rock basin

### 7.2 Rainwater (backup and potable)

- Metal roof collection section → first-flush diverter (discards first 20L) → underground concrete or food-grade poly cistern
- Sizing: 10,000–15,000L minimum for 2–4 people, sized for 6–8 weeks autonomy (Paraguay's dry August–September)
- UV filter + ceramic filter for potable use
- All cistern vents screened with 0.5mm stainless mesh (dengue protocol absolute)
- Underground cisterns safe from flooding; pumps elevated above flood level

### 7.3 Greywater and waste

- Sink/shower → constructed wetland or reed bed → irrigates garden
- Composting toilet eliminates blackwater, reduces water demand by 30%
- All water infrastructure has manual bypass for grid-down operation

---

## 8. Energy Systems

| System | Specification |
|---|---|
| Micro-hydro (primary baseline) | 200–400W continuous, 24/7, Pelton/Turgo at existing weir |
| Solar PV array | 3–6 kW, on separate steel frame (NOT on living roof) |
| Battery bank | 10–20 kWh LiFePO4, 2–3 days autonomy |
| Grid tie | Paraguay grid as backup only; hybrid inverter with island mode |
| Solar water heating | Thermosiphon collector — hot water off the inverter load |
| AC | Mini-split in sleeping areas only; passive design handles the rest |

**Principle:** Micro-hydro covers the always-on baseline (sensors, networking, refrigeration). Solar covers daily loads. Battery covers nights and cloudy days. Grid is the emergency backup only.

---

## 9. Structural Systems Summary

### 9.1 Foundation

- Stone rubble raised foundation minimum 60cm above grade
- Perforated pipe rubble trench drainage around perimeter
- Stainless steel termite collar at foundation level
- Earthen walls begin 60cm+ above finished ground level

### 9.2 Wall assembly

- Cob: Paraguay red laterite clay + sand + straw + water
- Bottle wall sections: paired bottles in lime mortar, non-structural zones only
- Exterior: lime plaster (NHL for lower 50cm), lime wash finish (white)
- Interior: earthen plaster + lime wash in wet zones
- All finishes vapor-permeable — never sealed

### 9.3 Roof

- Primary structure: lapacho timber (naturally termite-resistant, extremely hard)
- Primary waterproofing: corrugated metal over the living roof structure
- Living roof: root barrier membrane + drainage layer + 4–6cm growing medium + native species
- Living roof planted with: native grasses, lapacho ground cover, Paraguayan wildflowers
- Solar panels: on separate maintenance-accessible steel frame, NOT on living roof
- Rainwater collection: dedicated clean metal surface, separate from living roof, with first-flush diverter

---

## 10. Cultural and Architectural Form Language

The house is Paraguayan first. Key elements:

| Element | Description | Cultural source |
|---|---|---|
| Corredor (gallery) | Covered transition space on north face, open to the glade and stream view | Traditional Paraguayan residential form |
| Tatakuá | Domed clay oven attached to exterior south wall. Vaulted form, built with bricks + mud + molasses | Guaraní traditional cooking oven |
| Lapacho timber | Structural roof elements in lapacho hardwood. Extremely dense, naturally termite-resistant | Indigenous Atlantic Forest material |
| Interior courtyard | Recessed outdoor space within the U-shaped plan | Spanish colonial / Guaraní communal form |
| Red laterite clay | Paraguay's own soil — the wall IS the ground it sits on | Site-specific material identity |
| Quincho space | Covered outdoor hearth area for communal barbecue | Paraguayan domestic culture |
| Bottle glass mix | Amber, cobalt, green, brown — local beer and beverage bottles | Upcycled local material |

---

## 11. Complete Flora Inventory for the Site

### Canopy layer (10–30m)

| Species | Local name | Notes |
|---|---|---|
| Handroanthus impetiginosus | Lapacho / Tajy | National tree. Deciduous — bare branches with hot-pink trumpet flowers July–Sept before leaves appear. Petals carpet the ground |
| Mangifera indica | Mango | Dominant canopy on the site — visible in every photograph. Dense dark-green spreading crown |
| Cedrela fissilis | Cedro | Tall straight Atlantic Forest hardwood. Compound pinnate leaves |
| Enterolobium contortisiliquum | Timbó | Large canopy tree with ear-shaped pods, fine bipinnate feathery leaves |

### Palm layer (8–20m)

| Species | Local name | Notes |
|---|---|---|
| Syagrus romanzoffiana | Pindo | Signature palm of the site, in every photograph. Single smooth grey trunk, DROOPING plumose fronds (not upright) — critical distinction for Blender. Orange fruit clusters |
| Bactris glaucescens | Tucum / Bacatimbo | Clumping riparian palm, spiny stems, 3–5m. Grows in dense colonies on stream banks |

### Sub-canopy (2–8m)

| Species | Local name | Notes |
|---|---|---|
| Ilex paraguariensis | Yerba mate | Small evergreen tree. Dense glossy leaves. Grows in Atlantic Forest understory. Cultural anchor |
| Cyathea atrovirens | Cachi / Tree fern | Arborescent fern native to Paraguay. Trunk 30–60cm, fronds 2.5m, bipinnate. Grows on shaded stream banks |
| Helietta apiculata | Tatarê | Atlantic Forest understory tree. Multi-stemmed, gnarled |

### Ground and riparian layer (0–2m)

| Species | Local name | Notes |
|---|---|---|
| Anthurium plowmanii | Guaimbé | Large-leafed aroid, paddle-shaped leaves 60–90cm, bullate texture. Grows at stream edges and on rock faces |
| Guadua trinii + Chusquea ramosissima | Takuara / Bamboo | Native Atlantic Forest bamboo. Dense clumps along stream banks, arching 6–10m |
| Agave americana | Agave | Large blue-grey rosettes in terrace zone. 1–1.5m diameter. Colonizing the old garden terraces |
| Cyathea corcovadensis | Tree fern | Secondary tree fern species, fronds 2.5m+ |
| Thelypteris / Pteris / Asplenium spp. | Various ferns | Ground cover, wall ferns, stream-margin ferns |
| Selaginella spp. | Moss-fern | Bright electric green, near-moss appearance, covers shaded ground and wet stone |
| Tillandsia spp. | Air plants | Epiphytes on upper tree branches. Grey-green rosettes 10–20cm. Detail element |
| Cattleya spp. | Orchids | Epiphytic, on canopy branches. Pink/purple flowers when in season |

---

## 12. Blender Technical Specifications

### 12.1 Render engine

Cycles for all final renders — required for glass transmission (bottle walls), caustics, volumetric scatter through canopy. EEVEE for quick previews only.

### 12.2 Clay wall material

- Sculpt mode for walls: Clay Strips, Smooth, Grab brushes — no hard edges anywhere
- Procedural material: Musgrave + Voronoi noise layered over terracotta base
- Paraguay clay colour: red-orange laterite, hex range #C4522A to #A03D1A
- Fingerprint/handprint detail: secondary displacement noise at fine scale
- Ambient Occlusion bake for recessed areas between hand-formed lumps
- BlenderKit procedural clay and fingerprint clay textures as base references

### 12.3 Bottle wall material

- Principled BSDF: Transmission = 1.0, Roughness = 0.02–0.04, IOR = 1.52
- Colour variation per bottle: cobalt (#0047AB tinted), amber (#8B6914), green (#2D5A1B), brown
- Bottles placed mouth-to-mouth, bottoms facing outward
- Geometry Nodes or particle system for placement within vertex group on wall mesh

### 12.4 Scene lighting

- Golden hour variant: HDRI + directional sun at 15–25° elevation from north-northwest. Sun from north (Southern Hemisphere — north is the warm face). Volume Scatter density 0.002 in world shader
- Overcast variant: Pure HDRI, soft diffuse, no directional sun. Slight blue-grey cast
- Night variant: Southern Hemisphere Milky Way HDRI, no artificial light, firefly particles

### 12.5 Pindo palm — critical notes

The pindo palm is NOT a coconut palm. Key differences for modelling:
- Fronds droop 45–60° from horizontal — they arch outward and downward
- Individual leaflets are long and thin (1.5–2cm wide, 60–80cm long), arranged in multiple planes along the rachis giving a "plumose" 3D appearance
- Dead fronds hang below the live crown for months before dropping
- Trunk: smooth grey, ring scars every 30–40cm, no sharp features
- Orange fruit clusters hang in dense panicles within the crown

### 12.6 Lapacho — critical notes

Deciduous tree. Two completely different appearances:
- Flowering (July–Sept): completely bare branches, thousands of hot-pink tubular flowers. Flowers fall and carpet the ground #F4C0D1
- Leafed (Oct–June): palmate compound leaves, 5–7 leaflets per leaf, dark green. Sparse globous crown, not dense

### 12.7 Water shader

Two-layer approach:
- Deep base layer: dark grey-green (#2A3528), minimal reflection, transparent to show rock below
- Shallow turbid surface: reddish-amber (#A85832) suspended sediment scattering, strong caustics on stream bed, white foam at cascade edges animated with scrolling noise

---

## 13. Render Variants and Camera Positions

### 13.1 Two lighting variants

**Variant A — Winter golden hour (primary/hero)**
- Time: 16:30, June–July
- Lapacho in full bloom, bare branches, hot-pink flower explosion
- Sun from north-northwest at 20° elevation
- Water catches orange light; forest interior in blue-purple shadow
- Pink petal carpet on red laterite ground
- Volumetric light shafts through canopy

**Variant B — Morning overcast (atmospheric)**
- Time: 08:00, November–December (wet season)
- All trees fully leafed out
- Completely overcast sky, soft diffuse light — matches the actual mood of all site photographs
- Mist in upper valley near cliff
- Stream more full after overnight rain

### 13.2 Six camera positions

1. **Hero wide:** Camera on flat-rock pool, 60cm height, 35mm equivalent. Full depth of site in one frame — foreground pool, mid-ground bridge, background forest and cliff
2. **Stream upstream:** Standing at footbridge, looking uphill through channel. Bamboo walls either side, cascades visible ahead
3. **Terrace overview:** Camera on upper terrace (future house position) looking downhill. Stone walls, agaves, glade, palms and forest stretching away
4. **Cliff backdrop:** From the glade, looking north. Escarpment filling background, pindo palms in foreground
5. **Night/dusk:** Blue hour, glade, stream luminous from sky reflection, firefly particles, pindo silhouettes
6. **Detail — lapacho petals:** Extreme close. Fallen pink petals on wet red rock. One petal floating on pool

---

## 14. The 10 Design Rules — Never Violate

1. No right angles in the cob walls — organic sculpted forms only
2. No cement plaster anywhere on cob — always lime
3. No standing water anywhere on the property — dengue protocol absolute
4. Earthen walls never in ground contact — raised foundation always
5. Wide overhangs (90cm+) on all sides — non-negotiable for clay longevity in humid subtropical
6. Passive design handles comfort to ~35°C — AC is supplementary in sleeping areas only
7. All critical systems (water pump, communications, flood sensors) stay powered during grid outages
8. The house is culturally Paraguayan first — Guaraní form language, local materials, local species
9. Solar panels on a separate maintenance-accessible steel frame — never on the living roof
10. All cisterns and water storage fully mosquito-proofed with physical 0.5mm stainless mesh

---

## 15. Key Reference Sources

- **Architecture:** Earthship Biotecture (Michael Reynolds), Laurie Baker bottle buildings (India), Equipo de Arquitectura Asunción contemporary earth houses
- **Climate data:** Wikipedia Climate of Paraguay, DICF UNEP Paraguay climate change assessment
- **Infrastructure:** Urban Resilience Hub Asunción, World Finance Paraguay infrastructure report, FloodList Paraguay
- **Flora:** Para La Tierra Atlantic Forest Paraguay, Flora Fauna Fun Paraguay native plants, Asunción Times lapacho article, Palmpedia Syagrus romanzoffiana
- **Earthen building:** This Cob House, The Year of Mud, Green Home Building, Mother Earth News
- **Smart home:** Home Assistant documentation, Semtech LoRa IoT, n8n automation platform
- **Health:** PAHO/WHO dengue Asunción, vivirenparaguay.com mosquito guide

---

*Document compiled from research session, June 2026. All data derived from primary sources verified during research.*