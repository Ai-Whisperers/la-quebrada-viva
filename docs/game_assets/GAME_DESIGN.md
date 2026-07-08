# La Quebrada Viva — Game Design Document

**Version:** 0.1 (2026-07-08)
**Author:** Erebus / Ai-Whisperers
**Engine:** Unreal Engine 5.7 + Cesium for Unreal
**Target platform:** Browser (Pixel Streaming) + Desktop (Win/Linux/Mac) + iOS/Android (Phase 3)

---

## 1. Vision

**A real place, walkable before it's built.** A 62-hectare property in
Escobar, Paraguay — currently forest, quebrada, sandstone escarpment —
becomes playable so the buyer (Wesley van de Camp) can experience the site
before committing capital, and so future buyers/visitors can experience the
housing park once it's built.

The game is **not** a simulator in the SimCity sense. It's a **photoreal
spatial planning tool** that doubles as a marketing experience. The "game"
mechanics serve the planning: every action teaches the player something
about the real land.

## 2. Core loop

```
┌─────────────────────────────────────────────────┐
│                                                  │
│   SPAWN at LQV gate (lon -57.030, lat -25.630)  │
│            ↓                                     │
│   FREE WALK (WASD + mouse, 1st-person)          │
│            ↓                                     │
│   DISCOVER 5 hotspots (quebrada, waterfall,      │
│            high point, build zones, gate)        │
│            ↓                                     │
│   TOGGLE MAP OVERLAYS (buildability, solar,      │
│            quebrada, vegetation health)          │
│            ↓                                     │
│   DECIDE where to place the house                │
│            ↓                                     │
│   INSPECT (walk to placement, validate          │
│            view, sun, slope, drainage)           │
│            ↓                                     │
│   SAVE / SHARE placement as .png + URL           │
│                                                  │
└─────────────────────────────────────────────────┘
```

## 3. Three game modes

### 3.1 Free Walk (default)

- First-person character controller (UE5 EnhancedInput)
- WASD + mouse look + jump (optional, terrain is steep in places)
- Sprint (Shift) for long distances
- Toggle map overlay (M key) with the 8 LQV data layers:
  - Buildability (4 classes, color-coded)
  - Quebrada + waterfall
  - Solar PV zones
  - OSM roads
  - GPS walk (Wes's actual 20-point walk)
  - Vegetation health (NDVI)
  - Property boundary (62 ha polygon)
  - AOI bbox (1100 ha)
- Hotspot markers (auto-discovered from the GeoJSON):
  - Quebrada confluence → audio: stream
  - Waterfall rank 1 → audio: cascade
  - High point (DEM max within parcel) → audio: wind
  - Build zone centroids → ambient: birds
- Compass HUD (top right): bearing + distance to next undiscovered hotspot

### 3.2 Planning Mode

Builds on Free Walk. Adds:

- **Placement tool**: hand → cursor → click on terrain → spawn house typology
- Typology picker (Tab key, radial menu):
  - Riverstone Cob (the flagship, 14MB GLB)
  - Bamboo Wigwam (planned, future GLB)
  - Tatakua standalone (oven + dining, future)
  - Worker housing (8 rooms × 25m², planned)
- **Buildability enforcement**: placement only valid on slope <15%. Invalid
  → red outline, audio cue
- **Solar PV tool**: auto-place north-facing roof solar on any placed house
- **Cost estimator**: per MASTER_BRIEF reconciled (Paraguay construction
  prices 2026-06-30) — shows USD cost for the placement
- **Save layout**: serializes placed houses + props to JSON, downloadable

### 3.3 Buyer Tour

Cinematic mode for non-interactive visitors. ~15 min:

- Camera spline along the GPS walk path
- Voiceover (placeholder text → TTS in v2): "You're standing at the gate.
  The quebrada runs north-south through the property — that sound you hear
  is water that hasn't been diverted yet. To your right, the escarpment
  rises 60 metres over the next 200 metres. Up there, the sandstone
  plateau catches the afternoon sun 2 hours earlier than down here."
- Day/night cycle compressed: 1 game-hour = 30 real-seconds
- Seasonal cycle (driven by Sentinel-2 NDVI phenology):
  - Peak green (May): NDVI 0.81
  - Trough (October): NDVI 0.74
  - Visualized as foliage density + canopy color shift
- Weather: random cloud cover + occasional rain (rainbow after)
- Audio: layer
  - Stream (loop, varies with proximity to quebrada)
  - Wind (volume tied to height + canopy density)
  - Birds (5-10 species, scripted by time of day)
  - Insects (dusk only)
  - Lapacho petals (May variant A only — falling visual particle)

## 4. NPCs / characters (Phase 2.5)

Per Wes's buyer-experience ideas, the housing park will have:

- **Wes himself** (the developer/owner) — NPC at the gate, first quest giver
- **Sonja** (operations partner) — at the office, gives the build-placement quest
- **Potential buyers** (3-5) — wander the property, each with their own
  dream house, each asking "where would YOU put yours?"
- **Local staff** (3-4) — at the tatakua, the worker housing, the
  restaurant site — scripted daily routines

For v1 (this game): just Wes as the gate NPC. Others in Phase 3.

## 5. Day/Night + Seasonal cycle

The LQV region is **subtropical with no strong seasonal cue** (Sentinel-2
phenology: peak=May NDVI 0.81, trough=Oct NDVI 0.74, amplitude 0.07).
Day/night is more dramatic than seasonal.

- **Day length**: 12 hours game-time = 8 real-minutes (8× speedup)
- **Sun position**: real-time computed from Cesium Globe Anchor at
  (-57.030, -25.630). Uses CesiumSunSky actor.
- **Night lighting**: moon + starlight + bioluminescence (Phase 2.5:
  fireflies per variant C of the Cycles renders)
- **Seasonal**: 4 seasons × 4 minutes each (game-time compressed)
  - Spring (Sep-Nov): NDVI ramp-up, lapacho bloom start
  - Summer (Dec-Feb): hot, dry, NDVI stable high
  - Autumn (Mar-May): NDVI peak, lapacho peak bloom (variant A)
  - Winter (Jun-Aug): cooler, NDVI plateau, occasional fog

## 6. Audio design

| Layer | Source | Notes |
|---|---|---|
| Stream | recorded quebrada (Phase 3) or loop library | volume = 1/(distance+1) to quebrada polyline |
| Wind | loop library | volume tied to (height × canopy density) |
| Birds | 5-10 species via time-of-day table | loop library; Phase 3: Wes captures |
| Insects | dusk-to-dawn only | Phase 3 |
| UI feedback | synth | placement success/fail, hotspot discovery |

For v1: stock loop library from UE5 starter content + freesound.org
(CC0 only). Replace with field recordings in Phase 3.

## 7. Performance targets

| Platform | Target | Min |
|---|---|---|
| Browser (Pixel Streaming, server-rendered) | 1080p @ 60fps | 720p @ 30fps |
| Desktop (RTX 3060 +) | 1440p @ 60fps | 1080p @ 30fps |
| Desktop (GTX 1060 +) | 1080p @ 30fps | 720p @ 30fps |
| Mobile (Phase 3 — not v1) | 720p @ 30fps | 540p @ 30fps |

Lumen GI + Nanite + Cesium is heavy. Pixel Streaming sidesteps client GPU
entirely. For desktop, profile-guided LODs required for low-end hardware.

## 8. Monetization (out of scope for v1, noted for Phase 3)

- **v1 (this)**: free, marketing tool for Wesley
- **v2**: pre-purchase visualization (buyers pay $200 for a "your house
  here" consultation session)
- **v3**: subscription model for buyers to revisit the property post-sale

## 9. Stretch goals (Phase 3+)

- **Multiplayer co-walk** (2-4 buyers exploring together, voice chat)
- **VR mode** (Quest 3 + UE5 VR template + Cesium) — already supported
  by Cesium VR sample
- **Live drone flythrough** (Wes mounts a phone on a drone, captures the
  property, streams the gsplat to the game in real-time)
- **Solar panel placement with real Shadow Analysis** (UE5 Lumen shadows)
- **Seasonal time-lapse** (12 Sentinel-2 scenes → 12 months of foliage)

## 10. Critical references

- `docs/HOUSING_PARK_CONCEPT.md` — Wes's vision
- `docs/_reconciled/MASTER_BRIEF.md` — cabin catalog + financial model
- `docs/ideas/buyer_experience/` — 17 buyer-experience ideas
- `docs/ideas/amenities/` — 11 amenity ideas (restaurant, pool, trail)
- `docs/game_assets/HANDOFF.md` — Phase 1 asset inventory
- `tools/build_lqv_level.py` — Phase 2 build script (runs in UE editor)
- `tools/bootstrap_lqv_on_laptop.sh` — UE5 + Cesium install + project setup
- `tools/deploy_lqv_pixstream.sh` — Hetzner + Cloudflare Calls deploy

## 11. Open design questions for the operator

1. **Default camera height on spawn?** Above the canopy for context, or
   ground-level for immersion?
2. **Inventory/UI overlays on by default, or off (immersion first)?**
3. **Wes NPC voice — synthesized TTS, or record his voice in NL/EN?**
4. **Multi-language support?** (English + Spanish for Paraguay market,
   Dutch for Wes, German optional?)
5. **Save-state persistence?** Browser localStorage vs server-side account?
6. **Telemetry?** What player actions do we log? (Phase 3 buy decision)