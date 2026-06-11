# Paraguay Clay & Bottle Smart House — Master Research Document

**Project:** La Quebrada Viva — Clay and bottle earthen smart home, eastern Paraguay  
**Owner:** Ivan Weiss Van Der Pol — Senior Data Engineer / AI Whisperers, Asunción, Paraguay  
**Status:** Research and design phase — Blender render in development  
**Last updated:** June 2026 (v2 — location confirmed, stream analysis complete)

> **Navigation (added 2026-06-11, T1.5).** This doc is the canonical source for **site, geology,
> hydrology, climate, earthen-architecture rules, smart-home stack, water, energy**. For a
> topic-indexed map of every Paraguay-specific concern across the project (including the
> market / community / regulatory material in `EUROPEAN_TOURISM_SPEC.md`), see
> **`docs/paraguay_context.md`** — that doc is the single navigational root.

---

## 1. Project Identity

The house is a cob/earthen structure using Paraguay's red laterite clay as the primary wall material, embedded with glass bottle walls that function as stained-glass light sources, topped with a living sod roof planted with native Paraguayan species including lapacho (tajy). It is designed around Guaraní and Spanish colonial form language: covered gallery (corredor), interior courtyard, tatakuá dome oven, low-pitched roof, lapacho timber structural elements.

The house is fully self-sufficient: solar PV + LiFePO4 battery bank, spring-fed stream water, rainwater cistern, greywater reed bed, composting toilet. A small run-of-stream micro-hydro turbine at the existing weir provides 24/7 baseline power.

The home sits on a confirmed real property in Escobar District, Paraguarí Department, Paraguay. The render is the first deliverable; a real build is the eventual goal.

---

## 2. Confirmed Location — Escobar District, Paraguarí

### 2.1 Administrative location

- **District:** Escobar (Gral. Patricio Escobar)
- **Department:** Paraguarí
- **Country:** Paraguay
- **Distance from Asunción:** ~78km southeast
- **Distance from Paraguarí city:** ~12km east on the Villarrica road
- **Town coordinates:** -25.650, -57.020
- **Elevation:** ~121m above sea level (town); property ~130–200m on the hillside

### 2.2 Satellite search coordinates

| Zone | Coordinates | Description |
|---|---|---|
| Primary search (Zone A) | -25.624, -57.028 | Hillside belt directly north of town — highest probability |
| Ita Cajón anchor | -25.6416, -57.0365 | Known public swim hole with spring-fed stream from the hills — nearest confirmed named landmark, describes the site almost exactly |
| Secondary search (Zone B) | -25.638, -57.012 | Eastern hill arc — Guazú Kua zone with listed stream properties |
| Town reference | -25.650, -57.020 | Escobar town centre |

**How to find on Google Earth / Google Maps:**
1. Navigate to: `-25.6416, -57.0365` (Ita Cajón)
2. Switch to Satellite view, zoom to 1:5,000 scale
3. Look northeast — find the forested cliff edge (sharp dark-green line where flat land meets hill)
4. The stream runs from that cliff face southward through the property
5. Look for: sinuous dark line (stream), faint geometric terrace lines on hillside, small cleared glade, 1–2 building rooflines in the trees

### 2.3 Geological formation

The Cordillera de los Altos sandstone/quartzite belt — the same formation as Cerro Perõ (Paraguarí) and Cerro Hu, extending east as a spur toward Escobar. The cliff face is Arenisca Roja (red sandstone) with quartzite intrusions, grey-orange in colour, vertical fracture lines, heavily vegetated. The property sits on the south-facing slope below this spur.

### 2.4 Topographic profile

The property descends in steps from north to south:

| Level | Feature | Estimated height above glade |
|---|---|---|
| 0 — cliff top | Escarpment summit, rainfall catchment | +40–60m |
| 1 — upper gorge | Boulder field, spring source, natural cascades | +15–25m |
| 2 — flat rock platform | Sandstone pool, upper weir | +8–15m |
| 3 — stone terraces | **RECOMMENDED HOUSE SITE** | +3–6m |
| 4 — glade / weir | Open glade, footbridges, existing structures | 0m reference |
| 5 — lower stream | Bamboo belt, natural channel, downstream | -2–5m |

### 2.5 Orientation (critical for passive design)

- The escarpment is to the **NORTH / NORTHWEST** of the property
- Stream flows **SOUTH / SOUTHEAST** — downhill away from the cliff
- The glade and open areas face **SOUTH / SOUTHEAST** — maximum sun exposure
- Colonial terraces step up toward the **NORTH / NORTHWEST** into the escarpment
- **In the Southern Hemisphere:** the gallery faces south-southeast = away from the equator = the cool, shaded, view-side. This is correct for passive cooling in Paraguay.
- Golden hour sun (Variant A render): from **NORTH-NORTHWEST** at 20° elevation, raking across the bottle wall face of the house. The viewer stands on the flat-rock pool looking uphill — the sun comes from behind-left and hits the house gallery face at an angle.
- Cool air drainage: after sunset, cold air flows DOWN from the escarpment through the forest and pools in the glade. The house on the upper terraces is directly in this cold air path. Stack ventilation openings on the north face draw this cool air through the house every night.

---

## 3. Stream System — Complete Hydrological Analysis

### 3.1 Five stream zones (reconstructed from 28 photographs)

**Zone 1 — Upper gorge (spring source)**
- Near the escarpment base, not directly photographed but confirmed by year-round flow
- Exposed dark quartzite/sandstone bedrock, massive moss-covered boulders 1–2m
- Multiple natural cascade drops of 0.5–1m over bedrock ledges
- Water is CLEAR here — no laterite suspension yet (spring water before surface pickup)
- Dense forest canopy closes overhead
- **This is the potable intake zone** — pipe intake here before laterite begins
- Photographed in: second batch images 8:26:16__2, 8:26:17, 8:26:18

**Zone 2 — Flat-rock sandstone platform**
- Stream spreads over wide flat horizontal sandstone bedrock, 8–12m across
- Multiple shallow cascade lips where water slides over ledge edges
- Red laterite begins appearing in sandy deposits at the margins
- Large boulders with stream threading between them
- **Natural swimming pool**: needs only a 20–30cm stone sill at the downstream cascade lip
- No liner, no concrete, no pumping — self-cleaning, gravity-fed
- Photographed in: 8:25:58, 8:25:59, 8:26:00, 8:26:16 (second batch)

**Zone 3 — Colonial weir zone (energy infrastructure)**
- Stream enters the managed section, channeled by concrete/stone weir walls
- Weir walls: 40–60cm high, dark moss-covered sandstone blocks, 50–100 years old
- Main weir creates a controlled drop of **1.0–1.5m** — the micro-hydro site
- Two crossing structures: arched iron footbridge (black painted, ~3m span, slightly rusted) and upstream wooden plank bridge
- Still pool above the drop, cascade below
- The weir infrastructure appears stable and functional — work with it
- Photographed in: 8:25:49__1, 8:25:49__2, 8:25:51, 8:25:51__1, 8:25:51__2, 8:26:00__1, 8:26:16__1 (second batch)

**Zone 4 — Channeled riparian zone (glade-adjacent)**
- Below the weir, stream flows through a more open zone alongside the main glade
- Stone/concrete channel walls continue on both sides (same colonial infrastructure)
- Stream width: 1.5–2.5m
- Water carries visible red laterite suspension — colour #A85832
- Bamboo and riparian vegetation crowds both banks
- Channel walls are moss-covered, support dense fern colonies
- Photographed in: 8:25:56, 8:26:15 (second batch), stream visible from veranda view

**Zone 5 — Lower bamboo belt (natural channel)**
- Stream enters natural state below channeled zone
- Dense bamboo (Guadua/Chusquea), large-leaf aroids (Anthurium), heliconia-type vegetation completely covers both banks
- Stream nearly hidden by vegetation at ground level
- This is the downstream discharge zone — not developed, not needed
- Photographed in: second batch bamboo images

### 3.2 Stream measurements (estimated from photographs)

| Feature | Measurement |
|---|---|
| Weir drop height | 1.0–1.5m |
| Weir channel width | 1.5–2.5m |
| Flat rock pool width | 8–12m |
| Boulder sizes (Z1–Z2) | 0.5–2.0m diameter |
| Terrace wall height | 30–60cm per course |
| Terrace tread depth | 2–4m |
| Footbridge span | ~3m |
| Glade length (estimate) | 80–120m |
| Glade width (estimate) | 40–60m |
| Stream bank vegetation belt | 3–6m each side |

### 3.3 Water quality by zone

| Zone | Appearance | Use |
|---|---|---|
| Z1 (upper gorge) | Clear to very lightly tinted | Potable intake — install screen + 200L settling tank here |
| Z2 (flat rock) | Slightly turbid, red sandy bottom | Non-potable — natural pool, irrigation |
| Z3–Z5 (below weir) | Red-brown laterite suspension (#A85832) | Non-potable — micro-hydro cooling, reed bed, fire suppression |

**Note:** The red turbidity is geological (laterite iron oxide), not pollution. It is beautiful and defines the visual character of the stream in renders.

### 3.4 Micro-hydro opportunity

- **Location:** Zone 3 weir — existing concrete drop infrastructure already in place
- **Head:** 1.0–1.5m confirmed from photographs
- **Turbine type:** Pelton wheel or Turgo turbine
- **Estimated output:** 200–500W continuous, 24/7, 365 days/year
- **This is more reliable than solar during the rainy season** — exactly when solar production drops
- **Turbine house:** Build at the weir in matching colonial sandstone, same architectural language
- **Penstock:** Buried black HDPE pipe from upper weir pool to turbine
- **Power cable:** Runs up to the house on the terraces (~40m)
- **Critical:** The potable water intake pipe and the penstock are separate circuits — never mix them

---

## 4. Site Features — Complete Inventory

| ID | Feature | Type | Status | Notes |
|---|---|---|---|---|
| F1 | Sandstone escarpment | Geological | Preserve | Cliff 40–60m. Cool air source. All water originates here. |
| F2 | Spring source | Hydrological | Preserve | At cliff base. Never disturb upstream. |
| F3 | Boulder field | Geological | Partial use | Loose/fallen boulders = foundation stone. Never remove in-situ boulders. |
| F4 | Flat-rock pool platform | Recreational | Enhance | Add 20–30cm stone sill only. No concrete, no liner. |
| F5 | Colonial weir + channel | Infrastructure | Preserve + enhance | Micro-hydro turbine to be added. Keep existing walls intact. |
| F6 | Arched iron footbridge | Infrastructure | Preserve | ~3m span, black painted, rusted base. Authentic detail. |
| F7 | Wooden plank bridge | Infrastructure | Preserve or replace | Upstream of iron bridge. May need maintenance. |
| F8 | Open glade | Landscape | Preserve + build on edge | 80–120m × 40–60m. Existing trees must stay. |
| F9 | Colonial stone terraces | Infrastructure | BUILD SITE | Upper terrace = house platform. Lower terraces = garden. |
| F10 | Existing blue house | Structure | Background context | Shows corredor form language. Not the design target. |
| F11 | Existing white quincho | Structure | Background context | Metal-roof quincho. Not the design target. |
| F12 | ANDE power pole | Infrastructure | Background | Grid connection exists but unreliable. Solar + micro-hydro to replace. |
| F13 | Red laterite soil | Material | Use | Clay for cob walls is literally the ground. |
| F14 | Mature mango canopy | Biological | Preserve absolutely | Primary passive cooling. Irreplaceable. |
| F15 | Pindo palm stands | Biological | Preserve absolutely | Visual identity of the site. |
| F16 | Bamboo riparian belt | Biological | Preserve + manage | Bank stabilization. Remove it = stream erosion. |
| F17 | Riparian aroids (Anthurium) | Biological | Preserve | Stream bank ecology. Beautiful in render foreground. |

---

## 5. Site Photographs — Reference Index

All 28 photographs taken June 9, 2026 (overcast winter morning). EXIF/GPS stripped by WhatsApp before upload.

### Batch 1 (8:25:43 PM — 8:26:03 PM)

| Filename | Subject | Key data |
|---|---|---|
| 8:25:43 | Escarpment from open field | Only photo showing the full cliff face — use as background reference |
| 8:25:45 | Farm gate entrance | Red dirt track, pindo palms, ANDE pole, blue house background |
| 8:25:45__1 | Up the track toward structures | Two existing structures visible, chickens |
| 8:25:46 | Blue house close | Corredor gallery, Fibrao tank, satellite dish, chainlink |
| 8:25:49 | Wide glade view | Blue house left, white quincho right, pindo palms |
| 8:25:49__1 | Weir channel + footbridge | Concrete weir walls, wooden bridge, cascade — Zone 3 |
| 8:25:49__2 | Weir zone alternate angle | Arched iron bridge visible, stream cascading |
| 8:25:50 | Glade wide from elevation | Confirms slight elevation above glade level |
| 8:25:51 | Forest interior path | Red dirt path, pindo palm, forest understory |
| 8:25:51__1 | Arched footbridge | Best view of the arched iron bridge, weir cascade below |
| 8:25:51__2 | Footbridge alternate | Channel width and wall height visible |
| 8:25:53 | Veranda looking out | **Confirms build elevation** — looking from elevated terrace through forest to glade |
| 8:25:56 | Stream over bedrock | Flat rock section — Zone 2, small cascade |
| 8:25:57 | Forest path | Dense forest, pindo crown visible |
| 8:25:58 | Flat rock wider view | Zone 2 — flat sandstone platform, stream spreading |
| 8:25:59 | **Widest flat-rock pool** | **Hero natural pool reference** — 8–12m wide, red laterite sand |
| 8:26:00 | Another flat-rock cascade | Zone 2, different angle |
| 8:26:00__1 | Terrace zone overview | Stone terrace walls, steps visible — **build site reference** |
| 8:26:02 | Dense forest | Red dirt path, forest interior |
| 8:26:03 | Forest path | Secondary forest zone |

### Batch 2 (8:26:08 PM — 8:26:18 PM)

| Filename | Subject | Key data |
|---|---|---|
| 8:26:08 | Veranda structure | Covered concrete terrace, forest view ahead |
| 8:26:14__1 | **Stone terrace wall close-up** | **Best foundation reference** — 2–3 courses moss-covered quartzite, stream at base |
| 8:26:15 | Forest with open area | Path through forest, stream glimpse |
| 8:26:16 | Wide stream flat rock | Zone 2 — widest pool view, red sandy bottom |
| 8:26:16__1 | Footbridge and weir | Arched bridge from downstream — best weir infrastructure reference |
| 8:26:16__2 | Turbulent upper cascade | Zone 1/2 boundary — more powerful flow, high water |
| 8:26:17 | **Upper gorge cascade** | Zone 1 — ledge cascade, clear water, overhanging vegetation, best micro-hydro reference |
| 8:26:18 | **Boulder gorge** | Zone 1 — large moss boulders, multiple cascade drops, clear water visible — **best upper gorge reference** |

---

## 6. Material Colour Reference — Complete Palette

| Material | Location in scene | Hex value | Notes |
|---|---|---|---|
| Stream water — shallow turbid | Z3–Z5, flat rock pool | #A85832 | Red laterite suspension |
| Stream water — deep/clear | Z1–Z2, below cascade | #2A3528 | Over dark bedrock |
| Stream water — cascade foam | All waterfalls | #F8F0E8 | Slightly warm white |
| Laterite ground — dry | Paths, glade | #C4522A | Orange-red compacted |
| Laterite ground — wet | Near stream, after rain | #8B3A1A | Dark saturated red |
| Boulders — shadow face | Z1–Z2 boulders | #3C4035 | Dark grey quartzite |
| Boulders — lit face | Z1–Z2 boulders | #6B7060 | Medium grey |
| Moss — wet/stream-adjacent | All stone near water | #8BA048 | Bright chartreuse |
| Moss — dry/shade | Stone walls, boulders | #3D4F1A | Dark olive |
| Moss — intermediate | Most stone surfaces | #5A7A2A | Mid green |
| Stone terrace wall face | Colonial terraces | #5F4A35 | Warm dark sandstone |
| Stone joint / shadow | Wall crevices | #3A2D20 | Near-black brown |
| Concrete weir — weathered | Weir walls | #7A7060 | Grey-brown aged concrete |
| Mango canopy — dense | Canopy interior | #1A3A1A | Very dark green |
| Mango canopy — lit edge | Canopy perimeter | #4A7A2A | Medium green |
| Lapacho flowers | Variant A only | #D4537E | Hot pink-magenta |
| Lapacho petal carpet | Ground under trees | #F4C0D1 | Pale pink |
| Pindo palm trunk | All palms | #6B5A42 | Warm grey-brown |
| Pindo palm frond | All palms | #2D5A1A | Dark feathery green |
| Pindo fruit clusters | Crown of palms | #E8701A | Orange |
| Anthurium leaf — top | Foreground aroids | #1A3D1A | Very dark glossy green |
| Sky — overcast (Variant B) | World sky | #B8C4A0 | Blue-grey-green, matches photos |
| Sky — golden hour (Variant A) | World sky | #F4A64A | Warm orange afternoon |

---

## 7. Paraguay Climate — Hard Constraints

### 7.1 Temperature and humidity

- Summer peak: 38–45°C with 70–77% relative humidity simultaneously (feels like 48°C+)
- Winter average: ~17°C. Cold snaps to -2 to -6°C when Antarctic air pushes north (rare but real)
- Coldest month: July. Warmest month: January
- Annual average: ~23°C
- 2019 was record hottest year: 24.3°C average, 1.5°C above the 1961–1990 baseline
- Escobar specific: average 21°C, max 39°C summer, min 2°C winter

### 7.2 Rainfall

- Annual average: 1,270mm (50 inches)
- Distribution: irregular — weeks without rain, then torrential downpours
- Peak periods: March–May and October–November
- Driest period: July–August (the render golden hour period)
- 85% of yearly rain falls in the rainy season

### 7.3 Extreme events

- Flooding: Paraguay River floods Asunción regularly. 60,000 displaced in 1982–83, 50,000+ in 2015–16
- Less than 20% of flood-vulnerable areas in Asunción covered by drainage systems
- Severe storms: October–April, can overwhelm drainage
- Dengue / Zika / Chikungunya: Aedes aegypti mosquitoes active year-round
- 2022–23 chikungunya outbreak: 81,000+ cases in Paraguay

---

## 8. Infrastructure Problems in Paraguay

**Power grid:** Frequent outages. Grid not designed for current demand. 99.9% renewable hydropower but distribution is fragile. Off-grid solar already commercially marketed as the direct alternative.

**Water:** Distribution network not designed for current demand. Contamination spikes during flooding. Absence of wastewater treatment in many areas.

**Drainage:** Less than 20% of flood-vulnerable areas covered by city drainage. Flash flooding from normal rain is routine.

**Pests:** Mosquitoes (dengue vector), termites (year-round tropical), ants, cockroaches. All active threats in organic-material construction.

---

## 9. Earthen Architecture — Technical Requirements

### 9.1 Cob construction

Cob is a mixture of clay-rich soil, aggregate sand, straw fibre, and water. Paraguay's red laterite clay is ideal — iron-rich, good clay fraction, moderate sand content. Quality confirmed from site photos: the visible plastic red clay in wet areas is directly workable.

### 9.2 Bottle walls

Paired glass bottles (mouth-to-mouth, bottoms facing outward) embedded in lime mortar (not cob). Creates stained-glass light effect. Colours: cobalt blue, amber, green, brown. Pattern: organic clusters. Precedent: Laurie Baker buildings (India), Mike Reynolds Earthships (Taos).

### 9.3 Non-negotiable rules for humid subtropical Paraguay

1. Never cement plaster on cob — always lime plaster (vapor-permeable, alkaline, self-healing)
2. Lime wash finish — multiple coats, white, breathes, anti-fungal
3. Wide roof overhangs — minimum 90cm on ALL sides
4. Raised foundation — minimum 60cm above grade, stone rubble base
5. Rubble trench drainage around the full perimeter
6. Termite barrier — physical stainless steel mesh collar at foundation level
7. Clay and lime buffer indoor humidity swings 10–20% — passive climate control mechanism

### 9.4 Passive cooling for humid subtropical (NOT desert)

Works:
- Cross-ventilation with stack effect (opposing openings at low and high points)
- Thermal mass: clay walls absorb heat during day, release at night
- Courtyard design: shaded outdoor room creates convection cooling
- Deep roof overhang shading walls
- Earth berming on south-facing walls (cool face in Southern Hemisphere)
- Night purging: open all vents after sunset
- Living roof insulating against radiant heat gain
- White lime exterior reflecting solar radiation
- **Nocturnal cool air drainage from the escarpment** (site-specific advantage)

Does NOT work in high humidity:
- Evaporative cooling (useless above ~60% RH)
- Earth air tunnels (condensation and mould risk)
- Heavily sealed buildings (earthen walls need to breathe)
- Traditional Earthship south-facing glass wall emphasis (designed for New Mexico desert)

---

## 10. Smart Home Technical Stack

### 10.1 Ivan's existing homelab

- Home Assistant on Ubuntu 24.04 (local, no cloud dependency)
- n8n for workflow automation
- Docker containers
- Claude Code with MCP servers configured
- ROCm for AMD GPU acceleration

### 10.2 Sensor deployment

| Sensor | Location | Purpose |
|---|---|---|
| Temperature + humidity (SHT31 Zigbee) | Each room | Comfort monitoring |
| Wall moisture sensors (capacitive, 3 depths) | In cob walls | Early water intrusion detection |
| Cistern level (ultrasonic) | Cistern | Water security |
| Cistern TDS + pH (ESP32 bridge) | Cistern | Water quality |
| **Stream level sensor** | **Weir pool** | **Flood early warning + micro-hydro monitoring** |
| **Micro-hydro output monitor** | **Turbine house** | **Power generation tracking** |
| Flood perimeter sensors | Foundation level | Flood early warning |
| CO2 / IAQ (SCD40) | Occupied spaces | Air quality |
| Weather station | Exterior | Full meteorological data |
| Solar production + battery SOC | Inverter/BMS | Energy management |

### 10.3 Key automations

- Night ventilation: auto-open stack vents when exterior temp < interior AND no rain detected
- Storm lockdown: close all motorised vents when rain rate exceeds threshold
- **Flood alert: three-level escalation triggered by stream level sensor — watch / warning / evacuate — WhatsApp notification**
- Battery low: shed non-essential loads below 30% SOC, protect water pump and comms
- Dengue watch: pull SENEPA outbreak data feed via n8n, alert when neighbourhood risk elevated
- Pre-cool: run AC in sleeping areas 17:00–21:00 during solar peak hours
- **Micro-hydro monitoring: alert if turbine output drops below threshold (debris blockage)**

### 10.4 Platform

- Home Assistant as local hub — all automations run offline
- Zigbee mesh (better clay wall penetration than WiFi; repeaters in bottle wall sections)
- MQTT as internal message bus
- n8n bridges Home Assistant to WhatsApp, SENEPA feeds, external APIs

---

## 11. Water Systems

### 11.1 Stream-based (site-specific — the key advantage)

- **Potable intake:** Zone 1/2 boundary (upper gorge, before laterite pickup). Steel mesh screen → 200L concrete settling tank → UV filter + ceramic filter → cistern for drinking water
- **Micro-hydro:** Zone 3 weir. Pelton/Turgo turbine at 1.0–1.5m drop. 200–500W continuous. Turbine house in matching sandstone at the weir. Penstock: buried HDPE from upper pool.
- **Non-potable supply:** Gravity-fed from Zone 3–4. Garden irrigation, reed bed, fire suppression, natural pool maintenance.
- **Natural pool:** Zone 2 flat-rock platform. Single 20–30cm stone sill at downstream lip. No other intervention needed.

### 11.2 Rainwater (backup and potable supplement)

- Metal roof collection → first-flush diverter → underground concrete cistern
- Sizing: 10,000–15,000L for 2–4 people, sized for 6–8 weeks dry-season autonomy
- All cistern vents screened with 0.5mm stainless mesh (dengue protocol)
- Underground cisterns safe from flooding; pumps elevated above flood level

### 11.3 Greywater and waste

- Sink/shower → constructed wetland or reed bed → irrigates garden
- Composting toilet eliminates blackwater, reduces water demand 30%
- All water infrastructure has manual bypass for grid-down operation

---

## 12. Energy Systems

| System | Specification | Notes |
|---|---|---|
| Micro-hydro (always-on baseline) | 200–500W continuous, 24/7 | At Zone 3 weir. Powers sensors, networking, refrigeration. |
| Solar PV array | 3–6 kW, separate steel frame | NOT on living roof. Powers daily loads. |
| Battery bank | 10–20 kWh LiFePO4, 2–3 days autonomy | Lithium iron phosphate preferred for tropical temps. |
| Grid tie | Paraguay grid as emergency backup | Hybrid inverter with island mode for outages. |
| Solar water heating | Thermosiphon collector on roof | Hot water off the inverter load — significant saving. |
| AC | Mini-split in sleeping areas only | Passive design handles the rest. |

**Energy philosophy:** Micro-hydro = always-on baseline. Solar = daily loads. Battery = nights and cloudy days. Grid = emergency only.

---

## 13. Structural Systems

### 13.1 Foundation

- Stone rubble raised foundation minimum 60cm above grade
- Uses the colonial terrace walls as the outer retaining perimeter
- Same sandstone and quartzite as the existing terrace walls — continuous material language
- Perforated pipe rubble trench drainage around perimeter
- Stainless steel termite collar at foundation level

### 13.2 Wall assembly

- Cob: Paraguay red laterite clay + sand + straw + water
- Bottle wall sections: paired bottles in lime mortar, non-structural zones only
- Exterior: lime plaster (NHL for lower 50cm), lime wash finish (white)
- Interior: earthen plaster + lime wash in wet zones
- All finishes vapor-permeable — never sealed

### 13.3 Roof

- Primary structure: lapacho timber (naturally termite-resistant)
- Primary waterproofing: corrugated metal
- Living roof: root barrier membrane + drainage layer + 4–6cm growing medium + native species
- Solar panels: on separate maintenance-accessible steel frame, NOT on living roof
- Rainwater collection: dedicated clean metal surface, separate from living roof

---

## 14. Cultural and Architectural Form Language

| Element | Description | Cultural source |
|---|---|---|
| Corredor (gallery) | Covered transition space on south-southeast face, toward the glade and stream view | Traditional Paraguayan residential form |
| Tatakuá | Domed clay oven on exterior, vaulted form, mud + molasses construction | Guaraní traditional cooking oven |
| Lapacho timber | Structural roof elements, naturally termite-resistant | Indigenous Atlantic Forest material |
| Interior courtyard | Recessed outdoor space within U-shaped plan | Spanish colonial / Guaraní communal form |
| Red laterite clay | Paraguay's own soil — the wall IS the ground it sits on | Site-specific material identity |
| Quincho space | Covered outdoor hearth for communal barbecue | Paraguayan domestic culture |
| Bottle glass mix | Amber, cobalt, green, brown — local beer and beverage bottles | Upcycled local material |

---

## 15. Complete Flora Inventory

### Canopy layer (10–30m)

| Species | Local name | Notes |
|---|---|---|
| Handroanthus impetiginosus | Lapacho / Tajy | National tree. Deciduous — bare branches with hot-pink trumpet flowers July–Sept. Petals carpet the ground. |
| Mangifera indica | Mango | Dominant canopy on site — in nearly every photograph. Dense dark-green spreading crown. 5–6 large specimens. |
| Cedrela fissilis | Cedro | Tall straight Atlantic Forest hardwood. Compound pinnate leaves. |
| Enterolobium contortisiliquum | Timbó | Large canopy tree, ear-shaped pods, fine bipinnate feathery leaves. |

### Palm layer (8–20m)

| Species | Local name | Notes |
|---|---|---|
| Syagrus romanzoffiana | Pindo palm | Signature palm — in every photograph. DROOPING plumose fronds (not upright). Orange fruit clusters. NOT a coconut palm. |
| Bactris glaucescens | Tucum | Clumping riparian palm, spiny stems, 3–5m. Dense colonies on stream banks. |

### Sub-canopy (2–8m)

| Species | Local name | Notes |
|---|---|---|
| Ilex paraguariensis | Yerba mate | Small evergreen tree, dense glossy leaves. Grows in Atlantic Forest understory. Cultural anchor. |
| Cyathea atrovirens | Cachi / Tree fern | Arborescent fern native to Paraguay. Trunk 30–60cm, fronds 2.5m, bipinnate. Grows on shaded stream banks. |
| Helietta apiculata | Tatarê | Atlantic Forest understory tree. Multi-stemmed, gnarled. |

### Ground and riparian layer (0–2m)

| Species | Local name | Notes |
|---|---|---|
| Anthurium plowmanii | Guaimbé | Large-leafed aroid, paddle-shaped leaves 60–90cm, bullate texture. Stream edges and rock faces. Foreground render hero. |
| Guadua trinii + Chusquea ramosissima | Takuara | Native bamboo. Dense clumps along stream banks, arching 6–10m. Bank stabilization — do not remove. |
| Agave americana | Agave | Large blue-grey rosettes 1–1.5m in terrace zone. Colonizing the old garden beds. |
| Cyathea corcovadensis | Tree fern | Secondary tree fern species, fronds 2.5m+. |
| Thelypteris / Pteris / Asplenium spp. | Various ferns | Ground cover, wall ferns, stream-margin ferns. Three distinct types. |
| Selaginella spp. | Moss-fern | Bright electric green, near-moss appearance, covers shaded ground and wet stone. |
| Tillandsia spp. | Air plants | Epiphytes on upper tree branches. Grey-green rosettes 10–20cm. Detail element. |
| Cattleya spp. | Orchids | Epiphytic. Pink/purple flowers when in season. |

---

## 16. Blender Technical Specifications

### 16.1 Render engine

Cycles for all final renders — required for glass transmission (bottle walls), caustics, volumetric scatter through canopy. EEVEE for quick previews only. Samples: min 512, aim 1024. Resolution: 4K (3840×2160).

### 16.2 Clay wall material

- Sculpt mode: Clay Strips, Smooth, Grab brushes — no hard edges anywhere
- Procedural material: Musgrave + Voronoi noise over terracotta base
- Paraguay clay colour: #C4522A to #A03D1A (red-orange laterite)
- Fingerprint/handprint detail: secondary displacement noise at fine scale
- AO bake for recessed areas between hand-formed lumps

### 16.3 Bottle wall material

- Principled BSDF: Transmission = 1.0, Roughness = 0.02–0.04, IOR = 1.52
- Colours: cobalt (#0047AB tinted), amber (#8B6914), green (#2D5A1B), brown (#5C3A1A)
- Bottles placed mouth-to-mouth, bottoms facing outward
- Geometry Nodes or particle system for placement

### 16.4 Scene lighting

- **Variant A — Golden hour:** HDRI + directional sun from **NORTH-NORTHWEST** at 20° elevation. This is because the escarpment is to the north — the sun comes from the same direction as the cool air source, raking across the gallery face. Volume Scatter density 0.002.
- **Variant B — Overcast:** Pure HDRI, soft diffuse, no directional sun. Sky colour #B8C4A0 — matches all 28 site photographs exactly.
- **Variant C — Night:** Southern Hemisphere Milky Way HDRI, firefly particles, interior warmth through bottle holes.

### 16.5 Pindo palm — critical

The pindo palm (Syagrus romanzoffiana) is NOT a coconut palm:
- Fronds droop 45–60° from horizontal
- Leaflets arranged in MULTIPLE PLANES along the rachis (plumose, 3D appearance)
- Dead fronds hang below the live crown for months
- Trunk: smooth grey, ring scars every 25–35cm
- Orange fruit clusters in dense panicles within the crown

### 16.6 Lapacho — two completely different appearances

- **Flowering (July–Sept):** completely bare branches, thousands of hot-pink tubular flowers (#D4537E). Petals carpet the ground (#F4C0D1).
- **Leafed (Oct–June):** palmate compound leaves, 5–7 leaflets per leaf, dark green. Sparse globous crown.

### 16.7 Water shader (critical — this is not blue water)

Two-layer approach:
- Deep base: dark grey-green (#2A3528), transparent to show rock below
- Shallow turbid surface: reddish-amber (#A85832) suspended laterite sediment scattering
- Cascade foam: animated scrolling noise, slightly warm white (#F8F0E8)
- Enable Cycles caustics — the shallow pool caustics on the flat rock are a key beauty element

---

## 17. Render Variants and Camera Positions

### 17.1 Three lighting variants

**Variant A — Winter golden hour (primary/hero)**
- Time: 16:30, June–July (Southern Hemisphere winter)
- Lapacho in full bloom — bare branches, hot-pink flower explosion
- Sun from NORTH-NORTHWEST at 20° elevation (correct for Southern Hemisphere afternoon)
- Water catches orange light; forest interior in blue-purple shadow
- Pink petal carpet on red laterite ground
- Volumetric light shafts through canopy
- Stream running at moderate winter flow

**Variant B — Morning overcast (atmospheric — matches all 28 site photographs)**
- Time: 08:00, June (the actual conditions when all photos were taken)
- All trees fully leafed out OR lapacho bare (winter — either works)
- Completely overcast sky (#B8C4A0) — soft diffuse, no hard shadows
- Mist in upper valley near cliff — escarpment dissolves into cloud
- Stream running energetically (winter can have good rain events)
- Deep green, melancholy, alive — the authentic character of the site

**Variant C — Night / blue hour**
- Time: 20:00, any season
- Deep blue sky (#0A1A2A), Southern Hemisphere stars visible
- Stream faintly luminous from sky reflection
- Firefly particles in the glade (Lampyridae — native to Atlantic Forest Paraguay)
- Silhouettes of pindo palms against sky
- No artificial light at this stage (location render — no house yet)

### 17.2 Six camera positions (location render)

1. **Hero wide:** Flat-rock pool (Z2), 60cm height, 35mm equivalent. Full depth: foreground pool → footbridge → forest → cliff
2. **Stream upstream:** At footbridge, looking uphill through the channel. Bamboo walls either side.
3. **Terrace overview:** Upper terrace (future house position) looking downhill. Stone walls, agaves, glade, stream.
4. **Cliff backdrop:** From the glade looking north. Escarpment filling upper frame, pindo palms foreground.
5. **Blue hour / night:** Same as Shot 1 but dusk. Fireflies, stream reflection, pindo silhouettes.
6. **Detail — lapacho petals:** 20cm above flat rock surface, 90° nadir. Pink petals on wet red rock. One petal floating on pool surface.

---

## 18. The 10 Design Rules — Never Violate

> **Canonical source (T1.5 promoted 2026-06-11):** `docs/MASTER_BRIEF.md` §14 is the single
> authoritative copy of these 10 rules. The list below is preserved verbatim per the
> additions-only directive but is a **mirror, not a source** — if the two ever diverge,
> `MASTER_BRIEF.md` §14 wins. Cross-referenced from `CLAUDE.md` "The 10 design rules" section
> and `docs/research/README.md`.

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

## 19. Key Reference Sources

- **Architecture:** Earthship Biotecture (Michael Reynolds), Laurie Baker bottle buildings (India), Equipo de Arquitectura Asunción contemporary earth houses
- **Location:** Wikipedia Escobar Paraguay (coords -25.65, -57.02), Trip-Suggest Escobar confirmation, InfoCasas Escobar property listings confirming stream+serranía properties
- **Climate data:** Wikipedia Climate of Paraguay, DICF UNEP Paraguay climate change assessment
- **Infrastructure:** Urban Resilience Hub Asunción, World Finance Paraguay infrastructure report, FloodList Paraguay
- **Flora:** Para La Tierra Atlantic Forest Paraguay, Flora Fauna Fun Paraguay native plants, Asunción Times lapacho article, Palmpedia Syagrus romanzoffiana
- **Earthen building:** This Cob House, The Year of Mud, Green Home Building, Mother Earth News
- **Smart home:** Home Assistant documentation, Semtech LoRa IoT, n8n automation platform
- **Health:** PAHO/WHO dengue Asunción, vivirenparaguay.com mosquito guide

---

*Document v2 — updated June 2026 with confirmed location (Escobar District, Paraguarí), complete stream hydrological analysis from 28 photographs, full site feature inventory, topographic profile, satellite search coordinates, and orientation data.*
