# Blender Render Prompt — Location Scene
# "La Quebrada Viva" — Escobar District, Paraguarí, Paraguay
# No house. The land itself. The world the house will inhabit.
# Updated v2 — confirmed location + full stream analysis

---

## REAL LOCATION REFERENCE

This scene is based on a confirmed real property:
- District: Escobar (Gral. Patricio Escobar), Paraguarí Department, Paraguay
- Approximate coordinates: -25.624, -57.028 (Zone A candidate)
- Anchor landmark: Ita Cajón public swim hole at -25.6416, -57.0365
- 78km southeast of Asunción, 12km east of Paraguarí city on the Villarrica road
- Elevation: ~130–200m above sea level on the hillside
- Geological formation: Cordillera de los Altos sandstone/quartzite belt
- All 28 reference photographs taken on a single overcast winter morning (June 2026)

To find on Google Earth: navigate to -25.6416, -57.0365 (Ita Cajón),
switch to Satellite, zoom 1:5000, look northeast for the forested cliff edge.
The stream runs south from that cliff through the property.

---

## SCENE IDENTITY

Create a photorealistic Blender render of a wild forest ravine in Escobar District, 
Paraguarí Department, Paraguay — in the Cordillera de los Altos sandstone belt.
This is a location scene with NO buildings — the site itself before the house is built.
The scene is called "La Quebrada Viva" (The Living Ravine).

The defining elements are: a spring-fed stream descending from a sandstone escarpment 
through layered subtropical Atlantic Forest, channeled by 50–100 year old colonial stone 
weir infrastructure, spreading over wide flat sandstone bedrock forming a natural pool, 
arriving into an open glade framed by mature mango trees and pindo palms.

This is specifically Escobar District, Paraguarí, Paraguay — Atlantic Forest biome 
in the Cordillera de los Altos sandstone belt. Every plant, rock, soil colour, and 
water character must match this exact ecosystem. No generic tropical, Caribbean, or 
Amazon references.

---

## RENDER ENGINE AND SETTINGS

Engine: Cycles (mandatory — required for glass caustics, volumetric atmosphere, 
       bottle wall light transmission in house renders that follow this)
Samples: minimum 512, aim 1024 for final
Resolution: 4K (3840×2160) minimum
Color management: ACES or Filmic
Denoising: Intel OpenImageDenoise or OptiX
Output: EXR + JPEG

---

## TOPOGRAPHIC ORIENTATION — CRITICAL

The escarpment is to the NORTH / NORTHWEST.
Stream flows SOUTH / SOUTHEAST — downhill away from the cliff.
The glade faces SOUTH / SOUTHEAST — maximum sun exposure.

This is the Southern Hemisphere. North faces the sun.
The south-southeast side of the property is the warm, bright, view side.
The north/northwest side (toward the cliff) is the cool, shaded, cold-air side.

For Variant A (golden hour): Sun comes from NORTH-NORTHWEST at ~20° elevation.
The viewer on the flat-rock pool looks UPHILL / NORTH-NORTHWEST toward the scene.
The sun is behind-left of the camera, raking across the stone and water surfaces.
This means the cliff face catches warm raking light at the top of frame,
while the glade floor is partly in blue-purple shadow.

---

## STREAM COURSE — FIVE ZONES (must model all five)

The stream descends from the escarpment through five distinct morphological zones.
Model them continuously — the camera will eventually move through all five.

### Zone 1 — Upper gorge (background, partially visible)
- Position: ~15–25m above glade level, near the escarpment base
- Character: narrow gorge, large quartzite/sandstone boulders 1–2m, natural cascade 
  drops 0.5–1m over bedrock ledges, dense forest canopy closes completely overhead
- Water: CLEAR — spring water before laterite pickup. Colour: near-transparent 
  over dark grey bedrock. This is the cleanest, most pristine zone.
- Boulders: dark grey (#3C4035 shadow, #6B7060 lit face) with bright chartreuse 
  to olive green moss coverage (#8BA048 wet zones, #3D4F1A dry)
- Reference images: 8:26:16__2, 8:26:17, 8:26:18 (second photo batch)

### Zone 2 — Flat sandstone platform (primary foreground / natural pool)
- Position: ~8–15m above glade level
- Character: wide (8–12m) near-horizontal exposed sandstone bedrock surface over which 
  the stream spreads in a shallow sheet. Red laterite sand deposits in calmer areas.
  Multiple natural cascade lips where bedrock steps down 20–40cm.
- Water: begins to pick up laterite suspension — reddish-amber (#A85832) over sandy 
  bottom, clearing to dark grey-green (#2A3528) over submerged rock
- THIS IS THE HERO CAMERA POSITION — the widest, most photogenic section
- Natural pool: the wide shallow spread of water 20–40cm deep across the rock platform
- Rock surface: red-orange sandstone (#C4522A dry, darker when wet), horizontal 
  bedding planes, smooth water-polished surface, moss in crevices and margins
- Reference images: 8:25:58, 8:25:59, 8:26:00, 8:26:16 (second batch)

### Zone 3 — Colonial weir zone (mid-ground)
- Position: ~3–8m above glade level (where Zone 2 meets the channeled section)
- Character: the stream enters a managed section with colonial concrete/stone weir 
  walls on both sides. 50–100 years old, heavily moss-covered and patinated.
- Weir walls: 40–60cm high, dark warm sandstone blocks with aged concrete, moss 
  colonizing every horizontal surface
- Main weir drop: 1.0–1.5m controlled waterfall — white foam, spray mist around it
- Two crossing structures:
  a) Arched iron footbridge: black painted steel (~3m span), slightly rusted at base,
     wooden deck planks, arches over the channel immediately above the weir
  b) Simple wooden plank bridge further upstream
- The weir creates a still pool above the drop and energetic cascade below
- Reference images: 8:25:49__1, 8:25:51, 8:25:51__1, 8:26:00__1, 8:26:16__1

### Zone 4 — Channeled riparian zone (glade-adjacent)
- Position: at glade level, running alongside the open area
- Character: stream continues between the colonial stone channel walls, now at glade 
  level. Bamboo and riparian vegetation crowds both banks. Red laterite fully suspended.
- Water: reddish-brown (#A85832), stream width 1.5–2.5m
- Channel walls: moss-covered, fern colonies growing from every crevice
- Bamboo (Guadua trinii) clumps arch over both banks, partially enclosing the corridor
- Reference images: 8:25:56, and stream visible from veranda images

### Zone 5 — Lower bamboo belt (distance/background)
- Position: below the glade, downstream
- Character: stream enters natural state. Dense bamboo, large-leaf aroids, heliconia 
  overhangs both banks. Stream nearly hidden by vegetation.
- This zone is background only — do not detail, just suggest with dense vegetation.

---

## TERRAIN GEOMETRY

Build from scratch — do not use stock terrain assets.

**The flat-rock pool (Zone 2 — hero foreground)**
- Width: 8–12m, Depth: 5–8m (camera to downstream lip)
- Nearly horizontal, slight 3–5° downstream tilt
- Natural stone lip at the downstream edge where water overflows in a thin sheet
- Standing pool 20–40cm deep across the rock face
- Surface: smooth water-polished red-orange sandstone (#C4522A), horizontal bedding 
  planes visible, small depressions hold deeper still water
- Margins: red laterite sand deposits, moss patches, fern fronds overhanging
- DO NOT make this blue/clear — the water is reddish-amber over the sandy bottom

**The stream channel (Zone 3 — weir zone)**
- Cuts 1.5–2m below the surrounding glade level
- Concrete/stone weir walls: 40–60cm high, moss-covered aged sandstone blocks
- The weir creates a controlled waterfall drop of 1.0–1.5m
- Still pool 1–2m wide and 2–3m long above the weir drop
- Cascade below: white foam, spray, slightly turbulent pool at the base
- Arched iron footbridge: black painted, 3m span, wooden planks, crosses above the weir

**The glade (middle ground)**
- Open area, slightly domed, bounded by stream on one side and forest on the others
- Approximately 80–120m long × 40–60m wide (do not show the full extent — suggest it)
- Ground: mix of low grass patches (maintained but not manicured), bare red laterite, 
  exposed tree roots, occasional red dirt path
- Path: compressed red laterite, #C4522A dry / #8B3A1A wet, curves through the glade

**The stone terraces (middle ground — upper right of scene)**
- 2–3 courses of dry-stack sandstone retaining walls stepping uphill to the right
- Each wall: 30–60cm high, 2–4m wide treads between levels
- Stone: warm dark sandstone (#5F4A35), moss-covered on every horizontal surface
- Stone steps connecting levels: 4–6 steps, irregular, slightly uneven
- Agave (Agave americana) rosettes colonize the terrace faces
- DO NOT make these look new or clean — they are 50–100 years old, organic, lived-in

**The escarpment (background)**
- Sandstone/quartzite cliff: 40–60m high, rising above the forest
- Partially obscured by foreground canopy — never fully visible
- Rock face: grey-orange (#6B7060), moss and bromeliad in every crevice, lichen patches
- Forest from base to top — the cliff is never bare
- In Variant B (overcast): the cliff dissolves into mist/low cloud at the top
- Do not fully model — sculpted mesh at distance, detail not required beyond 80m

---

## WATER SHADER — CRITICAL — THIS IS NOT BLUE WATER

The stream water carries red laterite sediment in Zones 2–5. It is NOT blue, NOT clear,
NOT generic tropical blue-green. This is one of the most important visual identifiers of 
this specific location.

### Two-layer water shader

Layer 1 — Deep/base:
- Principled BSDF, Transmission = 0.95
- Colour: dark grey-green (#2A3528)
- Shows the dark rock and moss below the surface through the water
- IOR = 1.33

Layer 2 — Shallow/turbid surface:
- Volume Scatter with red-brown colour (#A85832)
- Density: 0.4 — enough to tint but not completely opaque
- This layer dominates in the flat pool, thins over cascades and rapids
- Over the Zone 1 upper gorge: OMIT this layer — water is clear there

Cascade foam:
- White foam (#F8F0E8) at every waterfall lip and in the weir pool below
- Animate with slow scrolling noise texture (0.05–0.1 units/sec)
- Foam dissipates 1–2m below the cascade lip

Enable Cycles caustics:
- The shallow turbid pool over flat rock creates beautiful filtered light patterns below
- The Zone 1 clear water over dark rock creates sharp bright caustic patterns

---

## ROCK AND STONE MATERIALS

One base sandstone/quartzite material, four variants:

**Base rock — dry lit face**
- Base colour: #5F4A35 (warm dark sandstone)
- Roughness: 0.85 — matte, not shiny
- Normal map: strong irregular surface, deep crack detail
- Voronoi + Musgrave noise displacement at two scales:
  Large scale (Musgrave, 0.3 strength): the overall surface undulation
  Fine scale (Voronoi, 0.08 strength): individual grain and fracture texture

**Variant 1 — Submerged / wet rock:**
- Darker overall, roughness drops to 0.25 (wet sheen)
- Slight specular highlight from refracted light
- Moss colour darker (#3D4F1A)

**Variant 2 — Mossy shaded rock:**
- Moss coverage driven by three masks:
  a) Curvature mask: moss collects in crevices and on horizontal faces
  b) Facing-up mask: horizontal surfaces hold more moisture = more moss
  c) AO mask: darker recessed areas = denser moss
- Moss colour: #8BA048 (bright wet, near water) blending to #3D4F1A (dry shade)
- Mix factor: distance-to-water also drives moss brightness

**Variant 3 — Aged concrete (weir walls):**
- Base: #7A7060 (grey-brown aged concrete)
- Roughness: 0.80
- Horizontal surfaces: heavy moss colonization (same moss shader)
- Vertical faces: streaking water stain texture running down from wet zones above
- Micro-cracks: fine Voronoi displacement at very small scale

**Variant 4 — Colonial terrace stone (dry-stack):**
- Same as Variant 2 mossy rock but with more regular block faces (dry-stack cut marks)
- Joints between blocks: deep shadow (#3A2D20), no mortar visible
- Each block slightly different in value — they are individual stones, not a uniform wall

---

## COMPLETE FLORA — EXACT SPECIFICATIONS

### THE PINDO PALM (Syagrus romanzoffiana) — Most important tree in the scene

THIS IS NOT A COCONUT PALM. Do not use any coconut palm asset. Critical differences:

Frond behaviour:
- Each frond droops 45–60° from horizontal — they arch OUTWARD then curve DOWNWARD
- Individual leaflets: 1.5–2cm wide, 60–80cm long, arranged in MULTIPLE PLANES along 
  the rachis — this gives the "plumose" 3D appearance (not flat like a coconut)
- Dead fronds: hang at 80–90° below the live crown for months before falling
  Model 3–4 dead brown fronds (colour #5A3A1A) hanging under each crown

Trunk:
- Single, smooth grey (#6B5A42)
- Ringed with old leaf scars every 25–35cm — horizontal ring marks
- No texture other than these horizontal scars — do not add bark texture

Crown character:
- Irregular, open, slightly messy — NOT symmetrical
- Total crown spread: 4–7m
- Height: 10–15m

Fruit clusters:
- Small orange spherical fruit (~1.5cm diameter), colour #E8701A
- Hanging in dense panicles WITHIN the crown fronds
- 3–5 fruit clusters per tree

Placement: 6 specimens total
- 2 flanking the path in the near glade (10–12m tall)
- 2 taller (14–15m) rising above the forest canopy in background — visible as silhouettes
- 2 mid-distance framing the stream zone (11–13m)

---

### LAPACHO / TAJY (Handroanthus impetiginosus) — Hero of Variant A

Build BOTH versions and switch based on render variant:

FLOWERING VERSION (Variant A — winter golden hour, July):
- Completely bare branches — absolutely NO leaves
- Thousands of hot-pink tubular trumpet flowers clustered at branch terminals
- Flower colour: #D4537E (magenta-pink), tubular 5cm long, 5-lobed
- Crown appears to glow pink — this is the most visually dramatic element in the scene
- Fallen petals on ground: particle system scatter, colour #F4C0D1, irregular distribution
  covering the red laterite ground in a pink carpet up to 3m from the tree base
- Bark: grey-brown (#7A6550), deeply fissured longitudinal cracks, rough texture
- Trunk: straight, 40–60cm diameter at base, branches from ~40% of height

LEAFED VERSION (Variant B — overcast):
- Palmate compound leaves: 5–7 elliptical leaflets per leaf, 10–15cm each
- Leaf colour: dark green #2A4A1A upper, slightly lighter lower, slight gloss
- Sparse, open crown — NOT as dense as the mango

Placement: 4 specimens
- 1 specimen in mid-ground whose petals carpet the path (Variant A hero element)
- 2 in the far middle ground partially visible through the forest
- 1 partially obscured by mango canopy in background

---

### MANGO (Mangifera indica) — Dominant canopy, in every photograph

Trunk: grey-brown (#6B5040), slightly gnarled, 50–80cm diameter at base,
      low branching from ~30% of height
Canopy: massive spreading crown, 10–15m wide per tree, dense foliage
Leaves: large oval, 25–30cm long
        Upper surface: dark green #1A3A1A
        Lower surface: lighter #2D5A2D
        New growth (terminal branches): red-bronze #8B3A1A (important detail — add this)
Form: multi-limbed, horizontal spread — the canopy should feel like a ceiling

Placement: 5–6 mature specimens distributed across the glade zone so their canopies 
overlap overhead, creating forest-floor quality light underneath them.

---

### TREE FERN / CACHI (Cyathea atrovirens) — Atmospheric scene-maker

Trunk: short (30–50cm), dark brown (#3A2010), covered in old frond stubs and fibrous texture
Fronds: 2.5m long, bipinnate (each primary pinna itself subdivided), arching gracefully outward
       Upper surface: dark green #2D5A1A
       Underside: lighter, yellow-green #4A7A1A, slight sheen
Fresh unfurling fronds (croziers): tight spiral, bright lime green #6AAA2A, slightly fuzzy

Place 5 specimens — hand-placed individually, not scattered:
1. At the base of the near stream bank (Zone 2/3 boundary) — lit from above by a canopy gap
   (Variant A: golden shaft of light hits exactly this fern — the most atmospheric moment)
2. On the shaded stream bank between Z2 and Z3
3. On the opposite shaded bank at the same location
4. At the corner of the lower stone terrace wall
5. Partially behind the iron footbridge

---

### ANTHURIUM / GUAIMBÉ (Anthurium plowmanii) — Foreground hero

Leaves: paddle-shaped, 60–90cm long × 30–40cm wide
Texture: bullate (puckered/quilted surface) — NOT smooth. This is the defining detail.
Colour: very dark glossy green #1A3D1A upper, pale midrib and veins in lighter green
Petiole: 40–60cm, slightly reddish at base
Growth: rosette form, 4–8 leaves per plant, low to the ground

Place 6–8 rosettes:
- 3–4 on the flat rock pool margins (Zone 2), some leaves actually overhanging the water
- 2 at the stream bank near the footbridge (Zone 3)
- 2 in deep shade at the base of the terrace wall

---

### BAMBOO / TAKUARA (Guadua trinii)

Culms: 6–10m tall, 4–6cm diameter
Colour: medium green with white ring at nodes
Arching: culms lean outward at 20–30° over the water — they do not stand straight
Leaves: narrow, bright green, clustering at culm terminals

Place dense clumps on BOTH stream banks from Zone 3 through Zone 4.
They create the essential tropical "curtain" that frames the stream corridor.
These are the plants that make the stream feel enclosed and intimate.

---

### AGAVE (Agave americana)

Large blue-grey succulent rosettes, 1–1.5m diameter
Leaf colour: blue-grey (#8A9E80), slightly waxy surface
Leaves: thick, rigid, terminal spine 3–5cm
Place 6–8 specimens in the upper terrace zone between the stone walls.
These create strong geometric contrast to the soft tropical vegetation.

---

### YERBA MATE (Ilex paraguariensis)

Small evergreen tree/shrub, 4–6m, often multi-stemmed
Leaves: oval, 8–12cm, dark glossy green, slightly serrated
Appearance: dense rounded bush
Place 5–8 specimens in the understory and along the path edge.

---

### VARIOUS FERNS (ground cover — three types)

1. Large ground fern (Thelypteris): medium green #4A7A2A, triangular frond 60–80cm
   Scatter across all shaded ground zones using Geometry Nodes density field

2. Wall fern (Asplenium): dark glossy strap leaves 20–30cm
   Hand-place in gaps between terrace wall stones and weir wall crevices

3. Selaginella: bright electric green #6AAA2A, moss-like, 5–10cm tall
   Dense cover on wet shaded rock surfaces near the stream — especially Z1–Z2

---

### MOSSES AND LIVERWORTS (applied to all stone)

4-tone moss material applied as vertex-painted layer on all stone:
- Wet stream moss: bright chartreuse #8BA048
- Moist shaded: medium green #5A7A2A
- Dry shaded: dark olive #3D4F1A
- Dry exposed: grey-green #6A7A5A

Coverage masks:
- Curvature mask → moss collects in crevices
- Facing-up mask → horizontal surfaces hold more moisture
- Distance-to-water mask → proximity to stream = brighter/more moss

---

### EPIPHYTES (detail elements — 2–3 trees closest to camera)

Tillandsia air plants:
- Clusters of 8–15 rosettes per attachment point on upper branches
- Grey-green colour #8A9A7A
- 10–20cm each, completely irregular orientation
- Hand-place on mango and lapacho branches closest to camera only

---

## SCENE LIGHTING — THREE VARIANTS

### VARIANT A: Winter Golden Hour (Primary / Hero Render)

Sun direction: NORTH-NORTHWEST
Sun elevation: 20° above horizon
Sun colour: warm golden #F4A64A
Sun intensity: 3.5 (Cycles)
Time: 16:30, June–July (Southern Hemisphere winter)
Sky: HDRI — warm late-afternoon, partial cloud, not overexposed

Volume scatter: density 0.002, slight warm tint — just enough for light shafts through canopy

Key light effects to achieve:
- The flat rock pool catches orange light, the water glows reddish-gold
- The escarpment cliff face catches raking warm light (upper right of frame)
- The glade floor is partly in blue-purple shadow
- The pink lapacho flowers glow against the dark forest
- Volumetric light shafts pierce the canopy where gaps allow
- The tree fern in Zone 2/3 catches a single golden shaft — the most atmospheric moment

### VARIANT B: Morning Overcast (Atmospheric — matches all 28 site photographs)

No directional sun at all — pure HDRI overcast sky
Sky colour: #B8C4A0 (blue-grey-green) — this is the EXACT sky colour from the photographs
Sky intensity: 1.2 (Cycles)
Time: 08:00, June (the actual conditions of the reference photos)

Mist: add Volume Scatter in the upper distance zone near the cliff
Density: 0.008, white colour
Effect: the cliff dissolves into mist — you can only see the lower 50–60% of it

This variant captures the authentic character of the site as it was photographed.
Soft, deep green, slightly melancholy, wildly alive.

### VARIANT C: Blue Hour / Night

Sky: deep blue #0A1A2A, slight Southern Hemisphere star field visible
No moon (new moon conditions)
Stream: faintly luminous from reflected sky light on the flat pool (#0A1A2A reflected)
Fireflies: 20–40 softly glowing particles at mid and far distance
           Colour #EEFF88, soft glow radius 0.4m, random animated movement
Silhouettes: pindo palms as black shapes against the deep blue sky
Background: cliff barely visible as a darker mass against the sky

---

## CAMERA POSITIONS — SIX SHOTS

### Shot 1 — Hero Wide (primary establishing render)
Position: On the flat rock pool (Zone 2), camera height 60cm
Target: Looking uphill / NORTH-NORTHWEST toward the scene
Focal length: 24–28mm equivalent (wide, full depth)
Depth of field: f/8 (everything sharp — show the full depth)
Frame composition:
  - Foreground L: anthurium rosette with leaves overhanging the water
  - Foreground R: stream surface reddish-amber, caustics on rock below
  - Mid-ground: arched iron footbridge, weir cascade below it
  - Far mid-ground: pindo palms rising above glade level
  - Background L: lapacho tree in full bloom (Variant A) / mango canopy (Variant B)
  - Background R: stone terraces stepping uphill
  - Far background: forest canopy, cliff partially visible above treeline
  Note: This is the camera that will look at the HOUSE in the house render — same position

### Shot 2 — Stream Corridor
Position: Standing at the iron footbridge, looking UPSTREAM (uphill) through the channel
Focal length: 35mm
DoF: f/5.6, focused on the mid-distance cascade (Zone 2 flat rock visible beyond)
The bamboo walls close in from both sides — corridor/tunnel feel
Light visible at the far end of the corridor (Variant A: golden backlight)

### Shot 3 — Upper Terrace (future house position — looking back)
Position: ON the upper stone terrace, camera height 1.5m
Target: Looking DOWNHILL / SOUTH-SOUTHEAST toward the glade
Focal length: 35mm
Frame: stone terrace steps descend in foreground, agave rosettes punctuate the walls,
       glade opening below, stream visible beyond the weir channel, pindo palms in
       mid-distance, escarpment NOT visible from this angle (behind camera)
This shot establishes: this is the right place. The house will stand here.

### Shot 4 — Cliff Backdrop
Position: From the glade level, looking NORTH / NORTH-NORTHWEST
Focal length: 50mm
Frame: escarpment filling the upper 40% of frame, forested cliff, mist at top (Variant B)
       Pindo palms in mid-distance, mango canopy as natural arch at top of frame
       Stream channel visible at lower-left, bamboo fringing it

### Shot 5 — Blue Hour / Night
Position: Same as Shot 1 but blue hour (Variant C)
Sky: deep blue, stars beginning
Stream: pool surface reflects sky
Firefly particles in the glade
Pindo palms: black silhouettes against deep blue sky

### Shot 6 — Detail: Lapacho Petals (Variant A only)
Position: 20cm above the flat rock surface, camera looking straight DOWN (nadir, 90°)
Focal length: 50mm macro equivalent, completely flat/sharp (f/16)
Frame: fallen pink petals (#D4537E fading to #F4C0D1) scattered on wet red rock (#8B3A1A)
       1–2 petals floating on the still pool surface
       One anthurium leaf edge visible at frame left
       Nothing else in frame

---

## BUILD ORDER

1. Terrain mesh — rock pool, stream channel, glade, terraces, escarpment geometry
2. Rock and stone materials — one base, four variants
3. Water shader — two-layer turbid laterite shader + foam animation
4. Ground material atlas — dry laterite, wet laterite, grass, bare soil
5. Mango trees × 5–6 — largest first, they set the light quality for everything below
6. Lapacho trees × 4 — build both flowering and leafed versions
7. Pindo palms × 6 — custom frond model required, NOT a stock coconut palm
8. Background forest mass — instanced trees, canopy volume only, no detail beyond 80m
9. Tree ferns × 5 — hand-placed individually
10. Bamboo clumps — scatter along both stream banks Z3–Z4
11. Anthurium rosettes × 6–8 — hand-placed at stream margins
12. Ground flora scatter — ferns, selaginella, grass via Geometry Nodes
13. Agave rosettes × 6–8 — hand-placed in terrace zone
14. Yerba mate shrubs — scatter in understory
15. Moss application — vertex paint all stone surfaces
16. Epiphytes — 2–3 trees nearest camera, hand-placed Tillandsia clusters
17. Footbridge geometry (arched iron + wooden plank)
18. Weir channel and cascade geometry
19. Colonial terrace walls with stone step detail
20. Lighting rigs — three variants as separate scenes, shared mesh collection
21. Volume scatter / atmosphere per variant
22. Camera positions — 6 saved camera objects with correct settings
23. Final render passes: beauty, depth, AO, cryptomatte for compositing

---

## WHAT TO EXCLUDE

- Any buildings, structures, power poles, fences, or artificial lighting
- Any stock coconut palm asset — the pindo palm must be custom built
- Blue or clear water — the stream is reddish-brown laterite sediment below Zone 1
- Generic jungle / Amazon / Caribbean vegetation
- Flat open fields — this site is enclosed and sheltered by the forest and hillside
- Bright unfiltered direct sunlight on the ground — the canopy filters everything
- Any human figures
- Perfect, maintained, or manicured vegetation — everything is wild and slightly unkempt
- Clean or new-looking stone — all stone is 50–100+ years old with heavy patina and moss

---

## ATMOSPHERE NOTE

The 28 reference photographs were all taken on a single overcast winter morning in June 2026.
Variant B reproduces this actual atmosphere exactly — it is NOT a compromise version.
It is the authentic daily character of the site in the cool season.
The soft diffuse green-grey light, the mist on the cliff, the dark saturated colours — 
this is what the place actually looks like. Both variants are primary deliverables.

---

*Prompt v2 — updated June 2026 with confirmed location coordinates, complete stream zone 
specifications, corrected solar orientation for Southern Hemisphere, photo reference index,
and three lighting variants including the overcast morning that matches all reference photos.*
