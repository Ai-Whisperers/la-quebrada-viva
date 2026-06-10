# External assets catalog — La Quebrada Viva

Phase 7.5 deliverable. Ranked shortlist of downloadable 3D models, PBR textures, and HDRIs to **replace or supplement** procedural code in `lqv/`. Goal: replace the visually weakest procedural species/props with high-fidelity downloads where free, license-clean assets exist; keep procedural code for the things we can't source.

Authoritative for Phase 8–10 asset integration. Pair with `docs/master_plan.md`.

> **MCP socket status:** blender-mcp Sketchfab/Hyper3D in-process import + Poly Haven MCP search are currently DEAD (`Could not connect to Blender. Make sure the Blender addon is running.`). Downloads listed below require either (a) MCP restart, or (b) manual browser download → `assets/<source>/<uid>/`. The catalog is source-agnostic — integration code reads from disk.

---

## Sources and license posture

| Source | License default | Attribution required | Notes |
|---|---|---|---|
| Poly Haven | CC0 | No | HDRIs + PBR textures + some models. Preferred — zero attribution overhead. |
| Sketchfab (free) | CC-BY 4.0 (most) / CC-BY-SA / CC-BY-NC | **Yes** for CC-BY. **REJECT** CC-BY-SA and CC-BY-NC. | UID-based downloads. `CREDITS.md` entry per asset. |
| BlenderKit | "Royalty Free" or CC0/CC-BY | Depends per-asset | Free tier requires account but no per-use attribution beyond the Royalty Free terms. |
| Hyper3D / Hunyuan3D (generation) | Generated → in-house owned | No | Used for species without a clean download (lapacho). |

**Hard rejects** (share-alike or non-commercial propagation risk into the scene):
- `1-3D.com Hammock` UID `b5b2e42309144dafaf2efe9b71a491c8` (CC-BY-SA).
- `knockcg Handmade clay oven` UID `d98456e4673943feb277dab8b45e5db6` — license unverified; do not bundle until confirmed CC-BY or freer.

---

## Category shortlist (ranked: ★★★ = top pick, ★★ = backup, ★ = consider)

### Flora — species per the 10 design rules

#### Pindo palm (*Syagrus romanzoffiana*)
- **Decision:** **KEEP PROCEDURAL** (`lqv/flora/pindo.py`). Phase 6 already added the second DISPLACE leaf-base scarring. No free Syagrus-specific model exists; generic palms (`eucalyp555 Low Poly Palm Tree`, `EFX Palm Tree Pack`) lack plumose drooping fronds and read as date palm or coconut. Procedural is more accurate.

#### Lapacho (*Handroanthus impetiginosus*) — Variant A bloom
- **Decision:** **Hyper3D generation path** (Task #12 — depends on MCP). The only direct-match Sketchfab model (`cgaxis Red Lapacho` UID `2beb1bc948d74d18bfd7912dcbe9f938`) is Sketchfab Store paid.
- **Fallback:** procedural-with-bloom (current `lqv/flora/lapacho.py`).

#### Mango — dominant overstory ★★★
- **Top pick:** `Jagobo Tropical Mango Trees Free` UID `6997814540f14929bf13cf3828b5dc90` (CC-BY) — 5 trees, PBR (bark + foliage), largest 285k tris.
- **Alt:** `stealth86 Mango Tree` UID `4b186052228d43d8b3fbb63213677de8` (CC-BY).
- **Wires into:** `lqv/flora/mango.py:add_mango` — replace bmesh trunk + leaf-sphere build with `asset_loader.import_sketchfab('6997814540f14929bf13cf3828b5dc90', loc, rot, scale)`. Pick 1 of 5 variants per spot to avoid clones.

#### Tree fern (*Cyathea*) ★★★
- **Top pick:** `b_nealie Tree Fern 1` UID `c6bc31d122c043a19346c90f5cbde40e` (CC-BY) — photogrammetry Ponga + Mamaku.
- **Frond-detail alt:** `WWU Geology Cyathea pinnata` UID `1cec99d96a5043e1a6997e106d00c09a` (educational, CC-BY).
- **Wires into:** `lqv/flora/fern.py:add_tree_fern` — 4 riparian spots, swap procedural fronds for the photogrammetry asset.

#### Bamboo (*Guadua*/*Chusquea*) ★★
- **No Guadua-specific free model.**
- **Best generic:** `JonhGillessen Free Bamboo Set` UID `e9f9fa5397814f81bf85ad06acf5bf30` (CC-BY).
- **Alt:** `1-3D.com Bamboo` UID `420d5be345904567a51466259c9476a2`.
- **Wires into:** `lqv/flora/bamboo.py:add_bamboo_clump` — retint trunks to Atlantic-Forest pale-green (`#A8B068`) post-import.

#### Agave americana ★★★
- **Top pick:** `LucaDubs Agave Americana` UID `efe126efa459471c81cfc3132357b1b6` (CC-BY) — Canary Islands RealityScan, very high fidelity.
- **Alts:** `clementeCgr` UID `7b737a71cc9045cb9352baa8a535b756`, `Chronos Digital LLC` UID `a0224fac643142c184b769fff119914f`.
- **Wires into:** `lqv/flora/agave.py:add_agave` — 5 lower-terrace spots; photogrammetry visual quality will dwarf procedural rosette.

#### Anthurium plowmanii ★★
- **Top pick:** `Lassi Kaukonen Anthurium` UID `e6a92c1ddb8941e9b8aa92dc1f0f3c18` (CC-BY).
- **Understory pack (15 tropicals):** `MozzarellaARC Tropical Plants Pack M02P` UID `2f093afb792742438f0f7ba7eaab90f0` — Blender 3.3x file; useful for filling understory beyond just epiphytes.
- **Wires into:** `lqv/flora/anthurium.py:_add_rosette` — keep the 4 trunk spots; replace bmesh rosette with import.

#### Manioc / cassava
- **Decision:** **DEFER.** No standout free model. Sketchfab tag pages exist (`/tags/cassava`, `/tags/manioc`) but nothing high-fidelity surfaced. `free3d.com Small Cassava Plant` is a candidate in `.blend` (license check needed). Not in any current camera framing — punt to a future revision.

---

### Paraguayan culture props (Phase 8 — corredor still-life, yard, tatakuá)

#### Hammock ★★★
- **Top pick:** `Andrey3Ds Hammock low poly` UID `c5fd4cef873f44f5a31db1fc6a04c572` (CC-BY).
- **BlenderKit alts** (Royalty Free):
  - `cd594e98-775f-4cc0-87fa-796d8a34c61a` — free hammock.
  - `1d59a74e-fa9e-452b-b067-4d3fe8b2139c` — macramé.
  - `1383b546-fae3-4e83-af03-9e7772812434` — "Hammock Allure".
- **REJECTED:** `1-3D.com Hammock` UID `b5b2e42309144dafaf2efe9b71a491c8` — CC-BY-SA would propagate share-alike to the whole scene.
- **Wires into:** new `lqv/house/corredor_props.py` between `build_services()` and `flora.populate()` in `build_scene.py`. Anchor between two corredor posts.

#### Mate / tereré / guampa ★★★
- **Top pick (still-life diorama):** `Szymon Yerba Mate Diorama` UID `f9c34aac9f594e8ca176e96cb0155259` (CC-BY) — full set, best for corredor close-ups.
- **Single-cup alts:**
  - `afferu Yerba mate cup matero` UID `f8f227f6a07e46d9bb312282c309bbf8`.
  - `Guillermo Sainz Yerba Mate Cup` UID `bdb4a5ed00384621b388491e916178a1`.
  - `ramirosalinasb Matecito` UID `75b6fe7408f44d2b8169de8856051ee1` (RealityScan).
- **Wires into:** `lqv/house/corredor_props.py` — place on the corredor table near the hammock.

#### Cántaro (clay water vessel) ★★★
- **Top pick:** `plaggy CC0 Plant Pot` UID `52bd62403b2e4b1db4e4641ebfd4f241` (**CC0** — best of all worlds, no attribution).
- **Alts:**
  - `Blender Osvo Clay Pot` UID `16ebf15281a34764bfd07a8f6bc362a3` (CC-BY).
  - `bobbycactus Old Clay Pot` UID `8521e9c1692f41d6aea354a2513c3f9e` (CC-BY).
- **Wires into:** `corredor_props.py` (corredor still-life) + `lqv/house/services.py` (NW utilities corner near cistern at (-9, +5)).

#### Chicken coop ★★★
- **Top pick:** `BRNDL Chicken Coop` UID `cbe1217c25804ffab1213b138db7ec76` (CC-BY) — 2024, dimensioned from a real coop.
- **Alts:**
  - `wolfgar74 Chicken Coop (Free)` UID `360923e446994fe8a3db68e016cc57b1`.
  - `synistersyrup Chicken Coop` UID `1f72fd7e01bc4b7bbbad102e623548ef`.
- **BlenderKit shed fallbacks:** `ed77b4bf-da43-45d0-b1b8-8c08b12357a5`, `836aa805-ae59-4a16-9ac9-b7a66744c79d`.
- **Wires into:** east yard around (-11, +8), after `build_services()` in `build_scene.py`. New helper `build_yard_props()` in `lqv/house/yard_props.py`.

#### Firewood ★★★
- **Top pick:** `Seth7Santos Stacked Firewood` UID `24694d04c1704aa1838ac775e1013f07` (CC-BY).
- **Alt:** `Aparicio Silva Firewood Pile` UID `393e8b83dfdc455fa4f03dbd4f116e0c` (CC-BY, 13.2k tris, 2K PBR).
- **Wires into:** `lqv/house/tatakua.py` — retire the Phase 5 procedural firewood pile; place beside the tatakuá lip.

#### Tatakuá ember / clay oven flame ★★
- **Top pick:** `merlinammm Fogata Bonfire` UID `ae5b6e5fcf9340f9bfe487404d547604` (CC-BY) — Blender file, flame is separable. For Variant C: keep embers, hide flame.
- **Verify-before-use:** `knockcg Handmade clay oven` UID `d98456e4673943feb277dab8b45e5db6` — license not confirmed Free in search results. **DO NOT bundle until license verified.**
- **Wires into:** `lqv/house/tatakua.py` — replace the procedural ember plate; gate behind `variant in ('A','C')` for visibility.

---

### Architecture detail (PBR — Poly Haven CC0)

These overlay onto existing materials via masks; they don't replace builders.

#### Clay/terracotta roof tiles
- `clay_roof_tiles_02` (4K/8K, 2.5m tile).
- `clay_roof_tiles_03` (4K/8K, 2.6m).
- `clay_roof_tiles` (4K/8K, 4m).
- `roof_tiles` (4K/8K/16K).
- **Use case:** LQV uses **living-sod / cob roof** on the main house — only useful for the tatakuá lip / service shed / ancillary structures. **Low priority.**

#### Cob wall / lime plaster surface
- `worn_plaster_wall` — closest match; uneven, chipped lime-look.
- **Use case:** subtle blend into the existing `MAT['cob_wall']` node tree to add micro-cracking and lime wash variance. Mask via vertex group `wall_weathered`.

#### Sandstone / cliff face
- `rock_face_03` — weathered cliff.
- `rock_pitted_mossy` — moss-flecked sandstone.
- `rock_boulder_cracked` — orange-tinted.
- `boulder_01` (model) — for one-off hero boulders.
- **Use case:** blend into `MAT['sandstone']` for the escarpment + weir blocks. Already partially handled by laterite; this adds rock-face variance.

---

### Ground PBR (Poly Haven CC0)

Already integrated in Phase 2:
- `red_laterite_soil_stones` (primary laterite).

To add:
- `red_dirt_mud_01` (8K compacted) — pathways.
- `cracked_red_ground` (2m) — dry-season patches on the upper terrace.
- `forest_ground_01` (8K leaf litter).
- `forest_ground_04` (3.2m, 159k DLs) — **under-canopy leaf litter** for the mango overstory shadow zones.
- `coast_sand_rocks_02` — stream pebble bed.

**Wires into:** `lqv/materials.py` ground material — add a `under_canopy` mask layer painted on the ground mesh; mix the existing laterite with `forest_ground_04` based on the mask. Lower-priority polish.

---

### HDRIs (Poly Haven CC0)

Currently in use:
- `kiara_1_dawn_4k.exr` — Variant A (0.8).
- `misty_pines_4k.exr` — Variant B (1.4).
- `qwantani_dusk_2_4k.exr` — designated for Variant C (0.5), not yet wired.

Recommended additions:
- `rainforest_trail` (24K unclipped midday rainforest, dappled sunlight) — strong candidate for a future **Variant D (midday-canopy)** or Variant B alt.
- `kloofendal_misty_morning_puresky` (24K) — softer Variant B alt with cleaner sky.
- `misty_dawn` — Variant B alt with mist already baked in.
- `spruit_dawn` (16K) — soft low-contrast dawn, possible Variant A alt with milder pink.
- `kloppenheim_01` (24K, misty grass at sunrise) — A alt with overcast sky.

**Wires into:** `lqv/lighting.py:_HDRI_BY_VARIANT` — add 'D' entry when variant lifted to support it.

---

## Integration plan

### New module: `lqv/asset_loader.py`

Single import helper that abstracts source:

```python
def import_sketchfab(uid: str, location, rotation=(0,0,0), scale=1.0):
    """Load assets/sketchfab/<uid>/scene.gltf, parent to an Empty, return root."""

def import_blenderkit(asset_id: str, location, rotation=(0,0,0), scale=1.0):
    """Load assets/blenderkit/<asset_id>.blend via append, return root."""

def import_polyhaven_model(slug: str, location, rotation=(0,0,0), scale=1.0):
    """Load assets/polyhaven/models/<slug>/<slug>_4k.blend, return root."""
```

All read from `assets/<source>/<id>/` on disk — source-agnostic, MCP-independent. If the asset folder is missing, log a warning and fall through to the procedural builder.

### Env flag: `USE_EXTERNAL_FLORA`

`lqv/config.py` reads `USE_EXTERNAL_FLORA=1` (default off). When set, `lqv/flora/{mango,fern,agave,anthurium,bamboo}.py` builders try `asset_loader.import_*` first and fall back to procedural on import failure. Pindo + lapacho stay procedural unconditionally.

Lets us A/B procedural vs imported without code surgery.

### License bookkeeping

- **CC0** (Poly Haven, plaggy plant pot): no entry needed.
- **CC-BY**: append entry to `CREDITS.md`:
  ```
  ### <Asset name> by <Author>
  - Source: https://sketchfab.com/3d-models/<slug>-<uid>
  - License: CC-BY 4.0
  - Used in: <module / camera>
  ```
- **CC-BY-SA / CC-BY-NC / paid / unknown**: NOT bundled.
- **Generated (Hyper3D)**: no entry needed; treated as in-house.

### Manual download fallback (MCP socket dead)

For each shortlist asset:
1. Browser → Sketchfab page → "Download 3D Model" → glTF or auto.
2. Unzip into `assets/sketchfab/<uid>/` so the loader finds `scene.gltf`.
3. Poly Haven: browser → "Download" 4K Blend → drop into `assets/polyhaven/{textures,models,hdris}/<slug>/`.
4. BlenderKit: browser → download → `assets/blenderkit/<asset_id>.blend`.

Loader paths are content-addressable — once on disk, integration code Just Works without MCP.

---

## Asset directory layout

```
assets/
  sketchfab/
    6997814540f14929bf13cf3828b5dc90/      # Jagobo mango pack
      scene.gltf
      textures/
    c6bc31d122c043a19346c90f5cbde40e/      # b_nealie tree fern
    efe126efa459471c81cfc3132357b1b6/      # LucaDubs agave
    e6a92c1ddb8941e9b8aa92dc1f0f3c18/      # Lassi anthurium
    e9f9fa5397814f81bf85ad06acf5bf30/      # JonhGillessen bamboo
    c5fd4cef873f44f5a31db1fc6a04c572/      # Andrey3Ds hammock
    f9c34aac9f594e8ca176e96cb0155259/      # Szymon mate diorama
    52bd62403b2e4b1db4e4641ebfd4f241/      # plaggy clay pot (CC0!)
    cbe1217c25804ffab1213b138db7ec76/      # BRNDL chicken coop
    24694d04c1704aa1838ac775e1013f07/      # Seth7Santos firewood
    ae5b6e5fcf9340f9bfe487404d547604/      # merlinammm bonfire
  blenderkit/
    cd594e98-775f-4cc0-87fa-796d8a34c61a.blend
  polyhaven/
    textures/
      forest_ground_04/
      red_dirt_mud_01/
      cracked_red_ground/
      worn_plaster_wall/
      rock_face_03/
      clay_roof_tiles_02/
    hdris/
      rainforest_trail_4k.exr
      kloofendal_misty_morning_puresky_4k.exr
```

`.gitignore`: track this catalog + `CREDITS.md`; do **not** track `assets/` itself (regenerable from download links).

---

## Open questions / blockers

- **MCP socket:** required for in-process import via `mcp__blender__download_sketchfab_model`. Manual downloads work in parallel; either path lands the same files on disk.
- **License verification** for `knockcg` clay oven UID `d98456e4673943feb277dab8b45e5db6` — must be confirmed CC-BY or freer before use. Until then: `merlinammm` bonfire is the embers source.
- **Tris budget:** Jagobo mango set's largest is 285k tris. Cycles handles it, but 4 mango instances + tree ferns + agaves could push the scene past current ~2M tri budget. Plan: instance with `bpy.data.collections.new` + Empty proxies rather than dupe geometry.

---

## Phase 8–10 work order (post this doc)

1. **Phase 8a** — write `lqv/asset_loader.py` + `USE_EXTERNAL_FLORA` config flag.
2. **Phase 8b** — manually download the 11 Sketchfab assets above into `assets/sketchfab/<uid>/` (Ivan's call when convenient; the loader degrades gracefully).
3. **Phase 8c** — wire mango, tree fern, agave, anthurium, bamboo through `asset_loader.import_sketchfab` behind the env flag.
4. **Phase 8d** — add `lqv/house/corredor_props.py` (hammock + mate) and `lqv/house/yard_props.py` (chicken coop), slotted in `build_scene.py` after `build_services()`.
5. **Phase 8e** — replace tatakuá embers + firewood with the bonfire + Seth7Santos imports.
6. **Phase 9** — Poly Haven ground PBR `forest_ground_04` overlay under canopy via `under_canopy` vertex mask.
7. **Phase 10** — Variant C extension (gated on Phase 7 completion).
8. **Phase 11** — re-render 18 finals, populate `CREDITS.md`, tag `v1.0-bundle`.
