# TERRAIN_PIVOT — La Quebrada Viva

**Status**: APPROVED 2026-06-11. Source of truth for the house-scale terrain DSL pivot, Wesley typology + amenity catalog, BoQ rollup, and escritura deck. All downstream phases (B–H) of plan `glimmering-tumbling-fiddle` reference this document.

**Author note**: written under the autonomous execution directive that followed Wesley's reference-photo dump and his explicit ask "I really like the idea of creating a 3D model of the terrain and placing the houses digitally on the map. I think that could be very useful for visualizing the project and estimating materials." The plan honors that ask: a parameterized terrain at the scale of a parcel-walk, not at the scale of a satellite tile, and a parametric catalog rich enough that the escritura-day deck can show Wesley exactly what is being bought.

---

## 1. Problem statement

The 62-ha digital twin shipped at commit `4409dba` on 2026-06-11 fuses an ALOS 30 m DEM with a Sentinel-2 cloud-free albedo and renders three A/B/C variants of the whole property. That artifact is correct, and stays — but it is the **wrong abstraction** for what Wesley actually asked for. Three concrete failure modes:

1. **Resolution mismatch.** A 30 m post on ALOS is the size of a Bamboo River House footprint. The DEM cannot describe the creek bank, the swale uphill of the cob house, the saddle between the hill and the upper terrace, or the riparian strip where the river touches the parcel boundary. Wesley's reference photos all live below this resolution.
2. **Inversion of control.** The satellite-DEM workflow treats the land as raw input — fixed pixels we ingest. Wesley's email treats the land as design output — "where the river flows, where the creek goes, where the trees are, where the hill is, where the houses are." That is a design grammar, not a measurement pipeline.
3. **No materials channel.** Wesley's second sentence in the same paragraph is "estimating materials." The DEM has zero hooks for material take-off. There is no `MATERIAL_TAKEOFF` on the satellite pipeline because there is nothing to take off — the terrain has no walls.

The pivot is therefore a **house-construction-scale terrain DSL**: a small Python class whose verbs are the verbs Wesley used in his email (`hill`, `creek`, `river`, `tree_scatter`, `path`, `place_house`), whose units are metres (`width_m`, `depth_m`, `height_m`, `density_per_ha`), and whose output is two artifacts simultaneously — a Blender collection that renders, and a `MATERIAL_TAKEOFF` dict that aggregates.

The satellite digital twin remains the context layer (the 62-ha bowl, the river bend, the ALOS hill in the south-west). The DSL is the focal layer (the 80 m × 60 m smoke scene, the parcels where each typology actually sits). Both ship.

---

## 2. Wesley vocabulary — verbatim phrases mapped to DSL primitives

From the 41 reference images (`docs/references/wesley_2026-06-11/`) and the email of 2026-06-10:

| Wesley phrase                                | DSL primitive                                       | Default values                              |
| -------------------------------------------- | --------------------------------------------------- | ------------------------------------------- |
| "the way the ground is placed"               | `Terrain(width_m, depth_m, cell_m, origin)`         | `cell_m=0.5`, `origin=(0,0)`                |
| "the curvature, the small hills"             | `terrain.hill(center, radius_m, height_m, falloff)` | `falloff='gaussian'`                        |
| "where the creek goes"                       | `terrain.creek(polyline, width_m, depth_m, ...)`    | `width_m=1.5`, `depth_m=0.4`                |
| "where the river flows"                      | `terrain.river(polyline, width_m, depth_m, ...)`    | `width_m=8.0`, `depth_m=1.2`, single-river  |
| "where the trees are"                        | `terrain.tree_scatter(polygon, species, density)`   | `density_per_ha=80`, `jitter=0.3`           |
| "where the houses are"                       | `terrain.place_house(footprint, xy, rot, snap)`     | `snap='pad'`, `pad_size_m=1.0`              |
| "make sense and geographical logic"          | `terrain.validate_geo()`                            | returns issue list; empty == valid          |

The DSL's job is to expose Wesley's nouns as the API surface, do the heightfield maths internally, and produce `bpy` collections only at `to_blender()` time. Validation is its own method so unit tests can call `validate_geo()` without touching Blender.

The reference photos sorted into thirteen typologies and four amenities. Each one is named for what Wesley calls it (or for the closest unambiguous label when he sent a sketch and no caption). The naming is final — Phase C of the plan renames seven existing stubs to fit, deletes seven that no longer match the catalog, and scaffolds ten new ones.

---

## 3. Fifteen typologies — Wesley catalog with build briefs

> Originally a 13-typology catalog (§3.1 – §3.13). Wesley phase-2 (2026-06-23)
> added §3.14 and §3.15. Three house-scale amenity stubs (bamboo_portal,
> bamboo_outdoor_shower, candle_path) live in `lqv.typologies.TYPOLOGY_AMENITIES`
> and are documented in §4-bis below.


Each entry below is what gets built under `lqv/typologies/<name>.py` plus a matching subscene driver under `lqv/subscene/<name>.py`. All entries carry a `MATERIAL_TAKEOFF` dict whose keys are materials and values are `{quantity_field, unit_cost_usd}` for the BoQ rollup.

### 3.1 Hobbit House (`hobbit_house`)
Earth-bermed circular hut, ~6 m external diameter, ~3.2 m crown height, round timber door, oeil-de-boeuf window, green roof. Cuts into a hill — `place_house(..., snap='cut')`. Reference: WhatsApp ... PM (1).jpeg, two angles. Materials: cob walls 12 m³, sod roof 28 m², round door + frame 1 unit, hobbit window 1 unit.

### 3.2 Italian Stone Small v1 (`italian_stone_small_v1`)
Stone-clad single-volume hut, ~4 m × 5 m, tile roof, single chimney. Pads onto a flat lawn. Material vocabulary borrowed from the dry-stone Tuscan farmhouses Wesley referenced.

### 3.3 Italian Stone Small v2 (`italian_stone_small_v2`)
Sibling of v1 with an attached lean-to porch and timber pergola. Same stone vocabulary, ~5 m × 6 m main + 2 m porch.

### 3.4 Italian River House 4-pax (`italian_river_house_4pax`)
Two-storey stone river house, terracotta hipped roof, riverside terrace. ~7 m × 9 m. Lives directly on the river bank — `place_house(..., snap='pad', pad_size_m=2.0)` then `terrain.path` from front door to the river.

### 3.5 Container River House (`container_river_house`)
Two stacked shipping containers, riverside cantilever, glass end-wall facing the river. ~12 m × 2.6 m footprint per container. Stilts when over riparian buffer — `place_house(..., snap='stilts')`. The container shell is geometry-rich; factor `lqv/house/container_shell.py` on second use (Phase E, not D).

### 3.6 Bamboo River House (`bamboo_river_house`) — **DSL completeness gate**
The Bali-style bamboo river house: woven culm walls, thatched roof, raised platform over the creek/river edge, no glass. This typology is on the critical path because it exercises every DSL hook: `creek`, `river`, raised-platform `snap='stilts'`, `tree_scatter` of bamboo behind. If this builds end-to-end with `validate_geo() == []` and a recognizable sub-render, the DSL is proven.

### 3.7 Bamboo Container 4-pax (`bamboo_container_4pax`)
Shipping container clad in vertical bamboo culms, 4-bed family layout, riverside deck. Conceptually a fusion of 3.5 and 3.6; reuses both shells.

### 3.8 Bamboo Wigwam Lodge (`bamboo_wigwam_lodge`)
Conical lodge of leaning bamboo poles tied at the apex, ~6 m diameter base, ~5 m height. Communal sleeping. Floor pad.

### 3.9 Bamboo Boomhut Treehouse (`bamboo_boomhut_treehouse`)
Treehouse-on-stilts, bamboo platform 4 m × 4 m at 3 m elevation, rope ladder + spiral stair, thatched roof. Snap = `stilts`; a `tree_scatter` of lapacho or large hardwoods within 4 m of the structure for visual context.

### 3.10 Bamboo + Beton 30 m² (`bamboo_beton_30`)
Hybrid 30 m² studio: poured-concrete base slab + low retaining wall, bamboo upper structure, single sloped roof. Couple unit.

### 3.11 Bamboo + Beton 28 m² (`bamboo_beton_28`)
Sibling of 3.10 with a different roof pitch (mono-pitched gull-wing) and a 2 m front porch. Solo unit.

### 3.12 Bamboo + Beton Family Curved (`bamboo_beton_family_curved`)
Family unit, ~70 m², concrete base + curved-roof bamboo structure (banana-leaf roof curvature), two bedrooms + central living. Curved-roof generation = stack of arcs along the long axis.

### 3.13 Bamboo + Beton Family Rectangular (`bamboo_beton_family_rectangular`)
Family unit, ~70 m², rectangular footprint, gabled bamboo roof. Same internal program as 3.12 with the simpler roof.

### 3.14 Bamboo Curved-Roof Villa (`bamboo_curved_roof_villa`) — Wesley phase-2
Signature single-room pavilion, 6.0 × 9.0 m footprint, raised lapacho deck, 11 arched lapacho ribs sweeping front-to-back (eave 2.40 m, crown 4.20 m), palm-thatch skin between ribs, three solid clay-plaster walls (N/W/E), fully glazed south facade with 4 lapacho mullions. Pads onto a flat lawn. Reference: Wesley phase-2 villa elevation, 2026-06-23.

### 3.15 Clay Terracotta Estate (`clay_terracotta_estate`) — Wesley phase-2
Two-storey African-modern villa, ~10 × 8 m footprint, clay-plaster walls, terracotta pitched roof with 1.2 m eaves on all sides, raised stone foundation, deep latticed lapacho upper veranda, one gable end exposing clay-block masonry. Total height ~7 m. House-scale; sub-renders use HOUSE_CLIP_END_M.

---

## 4. Four amenities — Wesley catalog with build briefs

### 4.1 Eco Pool (`eco_pool`)
Natural-pool aesthetic: free-form edge, boulder coping, biological-filter shallow zone, no chlorine signaling. ~10 m × 6 m footprint, 1.6 m max depth, plant-bed zone 3 m × 6 m on one side. Located uphill of the creek so overflow can cascade in — Wesley's water-feature continuity preference.

### 4.2 Floating Dining (`floating_dining`)
Floating timber platform 6 m × 6 m on the river (or, more practically, on a still-water inlet near the river bend). Communal table, hanging lanterns, no walls. Mooring lines to two banks.

### 4.3 Labrisa Lounge (`labrisa_lounge`) — Phase F-partial first amenity
"La Brisa": the central social space at the heart of the bamboo-river cluster. Creek runs through, glass-bowl pendant lanterns hang from a bamboo frame, boulder seating along the creek edge. Cascade weir at the upstream end. This amenity factors out `lqv/amenities/_grammar.py` for cascade-weir, stepping-stone, glass-bowl-lantern — all three vocabularies are reused by 4.1 and 4.4.

### 4.4 Eco Retreat / Modern Oasis (`eco_retreat_modern_oasis`)
Wellness-retreat focal building: yoga deck, open-air sauna, plunge tub. Bamboo + glass. ~9 m × 12 m. Sits uphill of the river bend, faces sunrise.

---

## 4-bis. Typology-package amenity stubs (Wesley phase-2, 2026-06-23)

> Three house-scale amenity stubs live under `lqv/typologies/` rather than `lqv/amenities/` because they're ground-clutter scaled to a single dwelling (entry gate, shower booth, lantern walkway) rather than full social-space modules. They share the typology `build(parent, location, variant)` contract so subscene drivers and the BoQ rollup iterate them uniformly with the housing units. They are registered in `lqv.typologies.TYPOLOGY_AMENITIES` and intentionally do **not** count toward the §3 housing total of 15.

### 4-bis.1 Bamboo Portal (`bamboo_portal`)
Entry gateway: 3.2 m wide × 2.8 m tall bamboo pergola with two lapacho posts, woven lattice header, optional climbing-plant scaffold. House-scale.

### 4-bis.2 Bamboo Outdoor Shower (`bamboo_outdoor_shower`)
1.6 m × 1.6 m × 2.2 m three-sided shower booth, woven bamboo screens on E/S/W, open N, lapacho slat floor over a gravel sump, single rain-shower head. Pairs with any bamboo typology.

### 4-bis.3 Candle Path (`candle_path`)
Lantern-lit stepping-stone walkway: 12-stone procedural line, 0.6 m spacing, glass-bowl lanterns alternating on lapacho stakes, low-emission night-pass variant. Connects entry to corredor.

---

## 5. DSL design — house-construction-scale terrain

### 5.1 Public API

```python
# lqv/site/terrain_dsl.py

class Terrain:
    def __init__(
        self,
        width_m: float,
        depth_m: float,
        cell_m: float = 0.5,
        origin: tuple[float, float] = (0.0, 0.0),
        z_clip_end: float = 20000.0,
    ): ...

    def hill(
        self,
        center: tuple[float, float],
        radius_m: float,
        height_m: float,
        falloff: str = 'gaussian',
    ) -> Feature: ...

    def creek(
        self,
        polyline: list[tuple[float, float]],
        width_m: float = 1.5,
        depth_m: float = 0.4,
        bed_material: str = 'river_cobble',
        flow_dir: tuple[float, float] | None = None,
    ) -> Feature: ...

    def river(
        self,
        polyline: list[tuple[float, float]],
        width_m: float = 8.0,
        depth_m: float = 1.2,
        bed_material: str = 'river_sand',
    ) -> Feature:
        """Single-river invariant: raises on a second call."""

    def tree_scatter(
        self,
        polygon: list[tuple[float, float]],
        species: str,
        density_per_ha: float,
        jitter: float = 0.3,
        seed: int | None = None,
    ) -> ScatterCluster: ...

    def path(
        self,
        polyline: list[tuple[float, float]],
        width_m: float = 1.2,
        material: str = 'flagstone',
    ) -> Feature: ...

    def place_house(
        self,
        footprint: tuple[float, float],
        xy: tuple[float, float],
        rotation_deg: float = 0.0,
        snap: str = 'pad',          # 'pad' | 'stilts' | 'cut'
        pad_size_m: float = 1.0,    # extra apron beyond footprint for 'pad'
    ) -> Placement: ...

    def validate_geo(self) -> list[str]:
        """Return list of geographic-logic violations. Empty list == valid.

        Checks:
            - house under water (footprint Z below river surface Z)
            - creek crosses river more than once
            - creek slope <0.5%
            - overlapping houses
            - scatter polygon intersects any house footprint
            - hill center outside terrain bounds
        """

    def to_blender(self, parent_collection=None) -> 'bpy.types.Collection':
        """Materialize. Idempotent. Calls validate_geo first and raises on any
        violation. Sets active camera clip_end >= self.z_clip_end."""
```

### 5.2 Internal model

- **Heightfield**: `self._z: numpy.ndarray[H, W]` where `H = round(depth_m / cell_m)` and `W = round(width_m / cell_m)`. Initialized to zeros. `hill()` adds (gaussian / cosine / linear) bumps; `creek()` and `river()` carve trenches; `place_house(snap='pad')` flattens; `place_house(snap='cut')` carves.
- **Features**: `self._features: list[Feature]` where `Feature = dataclass(kind, payload, polyline_or_polygon_world_xy, material)`. Each `hill/creek/river/path` call appends one.
- **Scatters**: `self._scatters: list[ScatterCluster]` populated lazily at `to_blender()` time — the polygon + density + species + seed are stored; actual point sampling happens at materialization.
- **Houses**: `self._houses: list[Placement]` records footprint, xy, rotation, snap. Pad/cut flattening is applied immediately to `self._z` so subsequent `validate_geo()` sees the correct surface.

### 5.3 Materialization — what `to_blender()` builds

1. **Ground mesh** — a grid mesh of size H × W with vertex Z = `self._z`. UV-unwrapped grid mapping. Material = `red_laterite_soil_stones` PBR by default; per-tile override possible if any `Feature.material` painted onto a vertex group.
2. **River + creek meshes** — separate flat planes at the carved-trench bottom Z + a thin water layer. Material `river_water` (glossy, IOR 1.33, blue-green tint).
3. **Paths** — extruded curve along polyline, thickness 0.05 m, material per `Feature.material`.
4. **Houses** — for each `Placement`, call the typology builder by name (`lqv.typologies.<name>.build`) with placement xy + rotation passed as kwargs. The typology builder is responsible for its own internals; the DSL only places it.
5. **Tree scatters** — Poisson-disk sample `polygon` at `density_per_ha`, jitter each point by `jitter * cell_m`, place `lqv.flora.<species>` builders (`add_lapacho`, `add_mango`, etc.) at each point. Photoreal swap respected via `RENDER_FLORA_PHOTOREAL=1`.

### 5.4 Smoke scene — 80 m × 60 m

`lqv/subscene/terrain_house_scale.py`:

```python
t = Terrain(width_m=80.0, depth_m=60.0, cell_m=0.5, origin=(0.0, 0.0))
t.hill(center=(20, 40), radius_m=18, height_m=4, falloff='gaussian')
t.river(polyline=[(0, 5), (40, 8), (80, 12)], width_m=8, depth_m=1.2)
t.creek(polyline=[(20, 40), (22, 25), (25, 12)], width_m=1.5, depth_m=0.4)
t.tree_scatter(polygon=[(5, 30), (15, 30), (15, 50), (5, 50)],
               species='lapacho', density_per_ha=80)
t.tree_scatter(polygon=[(60, 25), (75, 25), (75, 45), (60, 45)],
               species='mango', density_per_ha=60)
t.place_house(footprint=(7, 9), xy=(50, 25), rotation_deg=15,
              snap='pad', pad_size_m=2.0)
issues = t.validate_geo()
assert issues == [], issues
col = t.to_blender()
```

The driver must **bypass `base.run()`** and manually call `base.setup()` + place camera + set `cam.data.clip_end = 20000.0` — the parcel-scale clip-end gotcha (memory `feedback_subscene_clip_end`). Output lands at `renders/sub/runs/<RENDER_RUN_ID>_terrain_house_scale/A.png` mirrored to `renders/sub/latest/terrain_house_scale_A.png`.

### 5.5 What the DSL deliberately does NOT do

- **No procedural city generation.** No streets, blocks, lots, subdivisions. This is a single property with a small number of structures.
- **No automatic house spacing.** `place_house` is dumb; the operator picks `xy` by hand and the validator only flags overlaps.
- **No multi-river / delta topology.** Wesley's parcel touches one river. The single-river invariant is intentional — it catches operator error before it becomes a coordinate-space confusion.
- **No vegetation succession or seasonality.** Trees are placed in their adult state. Wesley's reference photos all show mature foliage.
- **No physics-driven water flow.** `creek()` and `river()` carve fixed channels; the flow direction parameter is purely metadata for the BoQ (it affects which bank gets eroded-cobble vs sediment-fines).

### 5.6 Validation rules in detail

| Rule                                       | Severity | Test                                                                 |
| ------------------------------------------ | -------- | -------------------------------------------------------------------- |
| House footprint below river surface Z      | error    | sample heightfield under footprint; compare to river-surface Z       |
| Creek crosses river more than once         | error    | segment intersection count > 1                                       |
| Creek slope < 0.5%                         | warn     | (max_z - min_z) along creek polyline / total length < 0.005          |
| Two house footprints overlap               | error    | Shapely intersection area > 0                                        |
| Scatter polygon intersects house footprint | warn     | Shapely intersection area > 0; warn (operator may want a forest hut) |
| Hill center outside terrain bounds         | error    | center not in (origin, origin + (width, depth))                      |

`validate_geo` returns a list of strings; empty list is the success case. `to_blender` raises `ValueError` with the joined issue list if any errors are present. Warnings are returned but do not block.

---

## 6. Stub reconciliation map — Phase C

The current `lqv/typologies/` directory holds seven forward-declaration stubs and the current `lqv/amenities/` directory holds six. None of them match Wesley's catalog after the reference dump. Phase C reconciles in two mechanical passes.

### 6.1 Pass 1 — rename seven stubs (typology + matching subscene driver)

| From                           | To                              | Driver line-15 update     |
| ------------------------------ | ------------------------------- | ------------------------- |
| `bamboo_pavilion.py`           | `bamboo_wigwam_lodge.py`        | rename import             |
| `shipping_container_eco.py`    | `bamboo_container_4pax.py`      | rename import             |
| `timber_tree_cabin.py`         | `bamboo_boomhut_treehouse.py`   | rename import             |
| `pool_wellness.py`             | `eco_pool.py`                   | rename import             |
| `reception_shop.py`            | `labrisa_lounge.py`             | rename import             |
| `event_lawn.py`                | `floating_dining.py`            | rename import             |
| `microhydro_centre.py`         | `eco_retreat_modern_oasis.py`   | rename import             |

Each rename: `git mv lqv/typologies/<from>.py lqv/typologies/<to>.py` (or `amenities`), `git mv lqv/subscene/<from>.py lqv/subscene/<to>.py`, then a single edit on the driver line 15 changing `from lqv.typologies.<from> import build` to `from lqv.typologies.<to> import build`.

### 6.2 Pass 1 — delete seven stale stubs

| Typology stub             | Reason for deletion                                       |
| ------------------------- | --------------------------------------------------------- |
| `adobe_courtyard.py`      | Adobe vocabulary already covered by hobbit_house + cob house; courtyard not in Wesley refs |
| `cob_bottle_lqv.py`       | Superseded by the actual cob+bottle build under `lqv/house/`     |
| `rammed_earth_loft.py`    | Not in Wesley refs; no client demand                       |
| `straw_bale_cottage.py`   | Not in Wesley refs; no client demand                       |
| `underground_dome.py`     | Hobbit house covers earth-sheltered vocabulary             |
| `equestrian_zone.py` (amenity) | Phase 1 phasing excludes horses                       |
| `parking_arrival.py` (amenity) | Out of scope for escritura deck; revisit Phase 2     |

Each deletion: `git rm lqv/typologies/<name>.py lqv/subscene/<name>.py` (or `amenities`). The `__init__.py` `TYPOLOGIES` / `AMENITIES` tuples drop the corresponding entries in the same commit.

### 6.3 Pass 2 — scaffold ten new typology stubs

For each of `hobbit_house`, `italian_stone_small_v1`, `italian_stone_small_v2`, `italian_river_house_4pax`, `container_river_house`, `bamboo_river_house`, `bamboo_beton_30`, `bamboo_beton_28`, `bamboo_beton_family_curved`, `bamboo_beton_family_rectangular`:

- `lqv/typologies/<name>.py` — minimal stub with `raise NotImplementedError` body, `MATERIAL_TAKEOFF = {}` placeholder, build signature `def build(xy=(0.0, 0.0), rotation_deg=0.0): ...`.
- `lqv/subscene/<name>.py` — copy from canonical template (the existing `base.run()` invocation pattern from any current driver, e.g. `lqv/subscene/cob_walls.py`), update line-15 import, set camera tuple to the typology's hero shot defaults.

### 6.4 Pass 2 — rewrite catalog tuples

```python
# lqv/typologies/__init__.py
TYPOLOGIES = (
    'hobbit_house',
    'italian_stone_small_v1',
    'italian_stone_small_v2',
    'italian_river_house_4pax',
    'container_river_house',
    'bamboo_river_house',
    'bamboo_container_4pax',
    'bamboo_wigwam_lodge',
    'bamboo_boomhut_treehouse',
    'bamboo_beton_30',
    'bamboo_beton_28',
    'bamboo_beton_family_curved',
    'bamboo_beton_family_rectangular',
)

# lqv/amenities/__init__.py
AMENITIES = (
    'eco_pool',
    'floating_dining',
    'labrisa_lounge',
    'eco_retreat_modern_oasis',
)
```

### 6.5 Smoke-test gate

`scripts/smoke_test.sh` must exit 0 after Phase C lands. The smoke test does NOT call any builder; it imports each module by name and verifies the import succeeds and `MATERIAL_TAKEOFF` exists. This catches missed renames, broken `__init__.py` edits, and typos in line-15 imports.

---

## 7. BoQ rollup

### 7.1 `MATERIAL_TAKEOFF` schema

Every typology and amenity module exports a module-level constant:

```python
MATERIAL_TAKEOFF: dict[str, dict] = {
    'cob_walls':       {'volume_m3': 12.0, 'unit_cost_usd': 60.0},
    'sod_roof':        {'area_m2':   28.0, 'unit_cost_usd': 18.0},
    'round_timber_door': {'count':   1,    'unit_cost_usd': 350.0},
    'hobbit_window':   {'count':     1,    'unit_cost_usd': 220.0},
}
```

Exactly one quantity field per material from this enum: `volume_m3`, `area_m2`, `length_m`, `count`, `weight_kg`. The `unit_cost_usd` is the cost per unit of that quantity. The aggregator multiplies the quantity by the cost; it does not need to know which quantity field is present — it picks the single non-`unit_cost_usd` key.

Material names are lowercase snake_case and **shared across modules**. If two typologies both use `cob_walls`, they aggregate under the same row. The vocabulary is curated in `lqv/boq.py` as a frozen set; new materials must be added there to avoid typo-driven row explosions.

### 7.2 Aggregator design — `lqv/boq.py`

```python
import importlib
import pkgutil
import csv
from pathlib import Path

import lqv.typologies as typ_pkg
import lqv.amenities as amen_pkg

PYG_PER_USD = 7300
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def _walk(pkg):
    for mod_info in pkgutil.iter_modules(pkg.__path__):
        if mod_info.name.startswith('_'):
            continue
        yield importlib.import_module(f"{pkg.__name__}.{mod_info.name}")

def aggregate() -> dict[str, dict]:
    rolled: dict[str, dict] = {}
    for mod in list(_walk(typ_pkg)) + list(_walk(amen_pkg)):
        takeoff = getattr(mod, 'MATERIAL_TAKEOFF', {}) or {}
        for mat, spec in takeoff.items():
            qty_key = next(k for k in spec if k != 'unit_cost_usd')
            qty = float(spec[qty_key])
            cost = float(spec.get('unit_cost_usd', 0.0))
            row = rolled.setdefault(mat, {'qty_key': qty_key, 'qty': 0.0, 'unit_cost_usd': cost})
            row['qty'] += qty
    return rolled

def write_csv(rolled, path):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['material', 'quantity', 'unit', 'unit_cost_usd', 'subtotal_usd', 'subtotal_pyg'])
        for mat, row in sorted(rolled.items()):
            sub_usd = row['qty'] * row['unit_cost_usd']
            sub_pyg = sub_usd * PYG_PER_USD
            w.writerow([mat, row['qty'], row['qty_key'], row['unit_cost_usd'], sub_usd, sub_pyg])
```

CSV + Markdown emitted to `docs/boq/boq_rollup.csv` and `docs/boq/boq_rollup.md`. PDF via `pandoc` subprocess if `which pandoc` succeeds; otherwise fall back to `reportlab` (the existing one-pager Wesley deliverable already uses pandoc on this machine, so the fallback should rarely fire).

### 7.3 Currency

USD is the primary computation currency. PYG is computed as `usd × 7300` per the project rate documented in `CLAUDE.md`. The PDF surfaces both columns side by side; the CSV holds both for downstream import. No exchange-rate fetch — the rate is pinned at 7300 PYG / USD for the escritura deck, which Wesley and Cynthia will both verify on closing day.

### 7.4 Spot-check protocol

Before declaring Phase G done, hand-sum three materials (cob, bamboo culm, tile) across all modules and verify the aggregator output matches. Any divergence means a `MATERIAL_TAKEOFF` dict was malformed.

---

## 8. Render output format

### 8.1 Per-asset sub-renders (Phase B/D/E/F)

Existing convention from memory `feedback_render_run_folders` and the gallery script:

```
renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/<variant>.png
renders/sub/latest/<asset>[_<tag>]_<variant>.png
```

Each typology and amenity gets a minimum of `A` variant at preview resolution (1280×720, 32 samples). Hero shots upgraded to 2048×1152 / 128 samples for the escritura deck. Variants `B` and `C` only when the typology is on Wesley's must-show shortlist for closing day.

### 8.2 Typology card composition (Phase H)

Each typology card is a single PDF page (A4 landscape, 297×210 mm) composed of:

- **Hero render** — top-left, 60% of page width, A-variant at hero resolution.
- **Four Dutch elevations** — bottom strip, VOORGEVEL / ACHTERGEVEL / LINKER ZIJGEVEL / RECHTER ZIJGEVEL labels, each ~70 mm wide.
- **Top-down plan** — top-right, 35% of page width.
- **Section A-A** — right-middle, 35% of page width.
- **Two interior details** — right-middle below the section, ~50 mm each.
- **Dutch spec bullets** — bottom-right corner: square meters, materials, capacity, fase (Phase 1/2/3).

The Dutch labels match Wesley's native language. Spec bullets use Dutch (`Oppervlakte`, `Materialen`, `Capaciteit`, `Fase`) per the Wesley-onepager precedent.

### 8.3 Amenity hero (Phase H)

Each amenity gets a single hero render at deck resolution; no elevations required.

### 8.4 Parcel-scale render (Phase B + Phase H)

`renders/sub/latest/terrain_house_scale_A.png` from the smoke scene goes onto the escritura deck cover after the 62-ha context page. The 62-ha frame establishes "this is the property"; the parcel-scale frame establishes "this is what Wesley is buying placed onto it."

### 8.5 Variants policy for escritura day

Variants `B` and `C` exist for marketing iteration, not for closing. The deck uses A across the board for visual consistency and to avoid lighting confusion in front of the escribana. The B/C frames remain in `renders/sub/runs/` for later use.

---

## 9. Asset shortlist — what to download / verify

License policy is **CC0 + CC-BY 4.0 only** (memory: no CC-BY-SA, no CC-BY-NC). Poly Haven is the primary catalog; ambientCG is the fallback for textures. Sketchfab is **blocked while MCP socket is dead** — do not attempt CC-BY model downloads via `mcp__blender__*`.

### 9.1 Confirmed already in repo (from prior phases)

| Slug                         | Type   | License | Path                                      |
| ---------------------------- | ------ | ------- | ----------------------------------------- |
| `red_laterite_soil_stones`   | PBR    | CC0     | `assets/textures/red_laterite_soil_stones`|
| `kiara_1_dawn`               | HDRI   | CC0     | `assets/hdris/kiara_1_dawn`               |
| `misty_pines`                | HDRI   | CC0     | `assets/hdris/misty_pines`                |
| `qwantani_dusk_2`            | HDRI   | CC0     | `assets/hdris/qwantani_dusk_2`            |
| `jacaranda_tree`             | model  | CC0     | `assets/models/jacaranda_tree`            |
| `pachira_aquatica_01`        | model  | CC0     | `assets/models/pachira_aquatica_01`       |
| `fern_02`                    | model  | CC0     | `assets/models/fern_02`                   |
| `quiver_tree_01`             | model  | CC0     | `assets/models/quiver_tree_01`            |
| `anthurium_botany_01`        | model  | CC0     | `assets/models/anthurium_botany_01`       |

### 9.2 Required for Phase D/E/F — to be researched by `asset-researcher` agent

| Need                              | Search hint                            | Used by                                              |
| --------------------------------- | -------------------------------------- | ---------------------------------------------------- |
| Bamboo culm (mature pole, brown)  | Poly Haven `bamboo`, `culm`, `pole`    | bamboo_river_house, bamboo_wigwam, beton_family_*    |
| Terracotta roof tile PBR          | Poly Haven `terracotta`, `roof_tile`   | italian_river_house_4pax, italian_stone_small_v1/v2  |
| River-rock cobble PBR             | Poly Haven `river_rocks`, `cobble`     | creek + river bed, eco_pool coping                    |
| Mossy boulder model / PBR         | Poly Haven `boulder`, `mossy_rocks`    | labrisa_lounge seating, eco_pool                     |
| Glass-bowl pendant lamp           | Poly Haven `pendant_light`, `glass_bowl` | labrisa_lounge                                       |
| Hand-thrown clay jacuzzi mosaic   | Poly Haven `tile`, `mosaic`            | eco_pool optional finish                              |
| Container corrugated steel PBR    | Poly Haven `corrugated_metal`          | container_river_house, bamboo_container_4pax        |
| Sod / green-roof PBR              | Poly Haven `grass`, `sod`              | hobbit_house roof                                    |
| Stone dry-stack PBR (Tuscan)      | Poly Haven `rock_wall`, `stone_wall`   | italian_stone_small_v1/v2, italian_river_house_4pax  |
| Round timber door (decor)         | Poly Haven `wooden_door`, generic round door | hobbit_house                                   |
| Thatch / palm roof PBR            | Poly Haven `thatch`, `palm_leaves`     | bamboo_wigwam, boomhut, river_house roof             |

Gap-fill output goes to `scripts/download_polyhaven_assets.py` manifest patch + a `LICENSES/<id>.txt` stub per new asset. If Poly Haven misses, fall back to ambientCG for textures. Models without a CC0 source stay procedural (the bamboo culm risk: if Poly Haven has nothing, we ship a procedural bamboo culm via array-modifier scaling of a cylinder + bend deformer + bark texture, same as the existing `lqv/flora/bamboo_clump.py`).

### 9.3 Procedural fallback policy

For each typology, if the asset-researcher cannot find a CC0 / CC-BY 4.0 source for a key material, the builder ships with a procedural Cycles material as fallback. The escritura deck must look complete even if one or two textures are placeholder.

---

## 10. Escritura deck plan — Phase H

### 10.1 Deck structure

Target ~30 pages, A4 landscape, single PDF named `docs/escritura_deck/escritura_deck_v1.pdf`.

1. **Cover page** — La Quebrada Viva, parcel coordinates, Wesley van de Camp + Thijs ownership share, escritura date 2026-06-27, escribana Cynthia Andrea Peña Ros.
2. **62-ha context page** — the digital twin from `4409dba` rendered as a single hero shot. "This is the property."
3. **House-scale parcel page** — `renders/sub/latest/terrain_house_scale_A.png`. "This is the proposed siting."
4. **Master plan diagram** — 2D top-down plan of the parcel with house pads, creek, river, paths labeled. Generated by `Terrain.to_topdown_svg()` if time permits, otherwise hand-traced in `docs/escritura_deck/master_plan.svg`.
5. **Phasing page** — Phase 1 (houses, Airbnb/Booking) → Phase 2 (events + houses) → Phase 3 (Dutch-European restaurant). Color-coded by phase on a copy of the master-plan diagram.
6–18. **Thirteen typology cards** — one page each per section 3.x. Format per §8.2.
19–22. **Four amenity hero pages** — one page each per section 4.x.
23. **BoQ summary page** — top 10 materials by spend, USD and PYG, with totals line.
24. **BoQ full table** — generated from `docs/boq/boq_rollup.md`.
25. **Sources page** — license attribution for every CC-BY 4.0 asset used; CC0 assets noted in aggregate.
26. **Signature page** — escritura-day signature block (Wesley, Thijs, sellers Justiniano + María Teresa, Cynthia).

### 10.2 Build script

`scripts/build_escritura_deck.py`:

- Loads each component (rendered PNGs, BoQ MD/CSV, master-plan SVG) and composes pages via PIL.
- Each page assembled as PNG, then merged into a single PDF via `pandoc` (preferred) or `Pillow.Image.save(append_images=...)` fallback.
- Idempotent; safe to rerun. Output overwrites `escritura_deck_v1.pdf`.

### 10.3 Critic-roast gates

Per the plan, six critic-roast gates: A, B, D, E+F, G, H. Each one is a `critic` subagent invocation in honest-roast format (memory `feedback_critique_honest_roast`) with the actual files cited by path + line. The H critic-roast is the final go/no-go before 2026-06-27; if the critic flags any escritura-blocking gap, the scope-cut order in the plan determines which item drops.

### 10.4 Closing-day delivery

The PDF is uploaded to the project's Google Drive folder (Wesley already has read access) and printed double-sided for Cynthia's office. Backup: a PNG-per-page archive in `docs/escritura_deck/pages/` so an emergency reprint is possible without LaTeX.

### 10.5 Post-escritura

After 2026-06-27, the deck shifts from a sales tool to a construction-planning tool. Phase G's BoQ becomes the input to the Phase 1 supplier RFPs (cob, bamboo, container, stone). The DSL stays — Wesley will want to move houses around as the project develops, and that is exactly what the parameterized API is for.

---

## Hard constraints (reproduced from plan)

- License **CC0 + CC-BY 4.0 only**. No CC-BY-SA, no CC-BY-NC.
- Sub-render-first workflow for every new asset (memory `feedback_sub_render_first`).
- Renderer byte-identity at `85e86aa` preserved (no `build_scene.py` edits this sprint).
- Never `git add -A` / `git add .` — explicit staging only.
- Never stage `scripts/mcp_daemon.py`, `docs/site_data/sentinel2/*.tif`, `docs/*_boleto_*.pdf`, `docs/*_escritura_*.pdf`, `docs/2026-*_*.pdf`.
- Never commit unless the user explicitly asks. Conventional Commits + `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`.
- Don't touch `lqv/scatter_lapacho_petals*` or hidden `WindowCut_*` cutters.
- MCP socket dead — Sketchfab path blocked, do not retry `mcp__blender__*`.
- Currency: USD primary, PYG at 7300 PYG/USD secondary.
- Escritura deadline: **2026-06-27** (T-16 days from 2026-06-11).
