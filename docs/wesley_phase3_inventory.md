# Wesley phase-3 inventory — unmodeled-design backlog

> Diff: `docs/HOUSING_PARK_CONCEPT.md` §5 catalogue × `docs/EUROPEAN_TOURISM_SPEC.md`
> lodging refinement vs. what is actually shipped on `main` (frozen at `85e86aa`).
>
> Scope: anything not in `lqv/typologies/__init__.py::TYPOLOGIES` /
> `TYPOLOGY_AMENITIES` or `lqv/amenities/__init__.py::AMENITIES`. The 15
> typologies + 3 typology-amenities + 4 amenities currently shipped are the
> baseline; everything else here is **unmodeled**.
>
> This is a backlog, not a plan. Phase 1 (P1) houses-first work is already
> covered by the 15 shipped typologies. Phase 2 / Phase 3 / Phase 4 entries
> below are the items Wesley will see in §7 of HOUSING_PARK_CONCEPT and ask
> "do we have visuals for that?" — the answer for each row is in the
> Status column.

## Shipped baseline (`85e86aa`) — reference

**Housing typologies (15, §3 TERRAIN_PIVOT):** hobbit_house · italian_stone_small_v1 ·
italian_stone_small_v2 · italian_river_house_4pax · container_river_house ·
bamboo_river_house · bamboo_container_4pax · bamboo_wigwam_lodge ·
bamboo_boomhut_treehouse · bamboo_beton_30 · bamboo_beton_28 ·
bamboo_beton_family_curved · bamboo_beton_family_rectangular ·
bamboo_curved_roof_villa · clay_terracotta_estate

**Typology-amenities (3):** bamboo_portal · bamboo_outdoor_shower · candle_path

**Amenities (4, §4 TERRAIN_PIVOT):** labrisa_lounge · eco_pool ·
floating_dining · eco_retreat_modern_oasis

**Site-scale sub-renders:** cob_bottle_lqv (the LQV reference), terrain
digital-twin (T-DT), features sub-render. Pelton micro-hydro is a
sub-render driver, not a typology.

---

## Unmodeled — by phase

### Phase 2 (months 9–18 post-closing) — event space + lodging fill

| Catalogue § | Item | Status | Notes |
|---|---|---|---|
| §5 Hospitality | Event hall | **unmodeled** | Wesley P2 anchor. ~150-pax capacity per EUROPEAN_TOURISM_SPEC. Needs its own `lqv/amenities/event_hall.py` + sub-render driver. |
| §5 Hospitality | Restaurant (open-air zone, quincho) | **unmodeled** | Part of P3 Dutch-restaurant build but the quincho is delivered earlier with the event hall (shared kitchen). |
| §5 Lodging | Family suites (Wesley §3.12 / §3.13 cover the 70 m² footprint) | **partially-modeled** | `bamboo_beton_family_curved` + `bamboo_beton_family_rectangular` ship; a brick/clay-plaster family variant on the §3.15 estate footprint is still missing. |
| §5 Lodging | Glamping tents | **unmodeled** | P2 high-margin filler — safari-tent on raised deck, 30 m² envelope. No `lqv/typologies/glamping_tent.py` yet. |
| §5 Lodging | Dormitory | **unmodeled** | 6–10 bed unit for staff-courses + youth groups. No module. |
| §5 Practical | Reception | **unmodeled** | Single entry-control + concierge envelope. Needs `lqv/amenities/reception.py`. Trigger to model: confirm location (creek-side vs. road-side) with Wesley. |
| §5 Practical | Staff housing | **unmodeled** | 2–4 unit cluster — separate from guest typologies, lower spec. |
| §5 Practical | Parking + arrival court | **unmodeled** | Hard-surface envelope + bus drop-off. Currently only the existing farm-track is rendered. |

### Phase 3 (year 2+) — European-Dutch restaurant + cultural anchors

| Catalogue § | Item | Status | Notes |
|---|---|---|---|
| §5 Hospitality | Restaurant indoor dining room | **unmodeled** | Multi-zone build with the quincho. Wesley priority. |
| §5 Hospitality | Bar / wine cellar | **unmodeled** | Earthen-floor cellar under the dining room — needs interior sub-render. |
| §5 Hospitality | Café / panadería | **unmodeled** | German-community supply-chain hook (per Wesley one-pager). Smaller envelope, daytime trade. |
| §5 Hospitality | Sauna | **partially-modeled** | `eco_retreat_modern_oasis` covers the wellness deck; the sauna is implied but not its own renderable object. |
| §5 Hospitality | Yoga deck | **partially-modeled** | Same — folded into `eco_retreat_modern_oasis` but no standalone module. |
| §5 Hospitality | Massage / wellness rooms | **unmodeled** | Indoor envelope on the wellness deck. |
| §5 Hospitality | Chapel | **unmodeled** | Wedding venue support. Small earthen-wall building, ~40 m². |
| §5 Cultural | Cooking school | **unmodeled** | Dependent on restaurant kitchen — shares fabric with the Dutch-restaurant build. |
| §5 Cultural | Visitor center | **unmodeled** | Could fold into reception or stand alone. |
| §5 Cultural | Performance venue | **unmodeled** | Open-air amphitheater near the stream — site-scale feature. |
| §5 Cultural | Artisan workshop | **unmodeled** | Permaculture / weaving / pottery — shed-scale envelope. |
| §5 Cultural | Gallery | **unmodeled** | Adjacent to visitor center. |

### Phase 4 (year 3+) — maturation / supply-chain

| Catalogue § | Item | Status | Notes |
|---|---|---|---|
| §5 Outdoor | Veg garden | **partially-modeled** | Implied in feature sub-render scatter; no dedicated module. |
| §5 Outdoor | Greenhouse | **unmodeled** | Needs `lqv/amenities/greenhouse.py` — supply-chain anchor for restaurant. |
| §5 Outdoor | Fruit orchard | **partially-modeled** | Scatter exists in the digital twin; no orchard-row arrangement yet. |
| §5 Outdoor | Herb spiral | **unmodeled** | Small-scale ground-clutter. |
| §5 Outdoor | Beekeeping | **unmodeled** | Hive cluster — visualization-only, low priority. |
| §5 Outdoor | Chicken coop | **unmodeled** | |
| §5 Outdoor | Cattle paddock | **unmodeled** | Fencing + windbreak — currently only existing terraces are rendered. |
| §5 Outdoor | Fish pond | **unmodeled** | Could share fabric with `floating_dining`'s waterline geometry. |
| §5 Cultural | Permaculture courses (envelope) | **unmodeled** | Outdoor classroom + shaded deck. |
| §5 Cultural | Library / herbarium | **unmodeled** | Could fold into visitor-center envelope. |
| §5 Commercial | Small shop | **unmodeled** | Reception-cluster. |
| §5 Commercial | Co-working | **unmodeled** | "Remote-worker stays" — Wesley EUROPEAN_TOURISM_SPEC angle. |

### Practical / infrastructure — never to be rendered

Catalogue §5 Practical also lists: Maintenance shed, Laundry, Generator
room, Water treatment, Sewage, Fuel storage, Composting, Recycling,
Helipad, Bus drop-off; §5 Commercial also lists: Market stand, Vending.
These are **out of scope** for the visualization track — they exist in the
operations plan but do not need renderable assets for Wesley's escritura
deck or P2/P3 sales material.

### Outdoor adventure (not rendered)

§5 Outdoor: Hiking trails, Horseback, MTB, Birding hides, Swimming,
Zip-line, Stargazing deck. These are **landscape overlays / paths**, not
buildings. The terrain digital-twin already carries the topography that
makes them legible; standalone modules are deferred unless a hero render
calls for one (e.g. a stargazing deck silhouette).

---

## Backlog summary

- **Phase 2 anchors (3):** event_hall, restaurant_quincho, reception
- **Phase 2 lodging fill (3):** glamping_tent, dormitory, brick_family_estate
- **Phase 2 ops (2):** staff_housing, parking_court
- **Phase 3 hospitality (6):** restaurant_dining_room, bar_wine_cellar,
  cafe_panaderia, massage_rooms, chapel, sauna_standalone
- **Phase 3 cultural (5):** cooking_school, visitor_center,
  performance_venue, artisan_workshop, gallery
- **Phase 4 land-use (10):** greenhouse, orchard_row, herb_spiral,
  beekeeping, chicken_coop, cattle_paddock, fish_pond,
  permaculture_classroom, library_herbarium, shop_coworking

**Total unmodeled designs: ~29** (excluding overlay/landscape and never-render
infrastructure items).

## Build order recommendation (post-escritura)

When the renderer-freeze is released (after the 27-Jun signing), the
sub-render-first workflow applies to every row above. Suggested order
based on Wesley's revenue path (houses → events → restaurant):

1. `event_hall` (P2 anchor — unlocks the wedding/corporate revenue line)
2. `reception` + `parking_court` (P2 operational unlock — required for
   any guest arrivals at scale)
3. `glamping_tent` (P2 high-margin lodging filler — fastest capex-to-revenue)
4. `restaurant_quincho` + `restaurant_dining_room` (P3 anchors, shared
   fabric)
5. `cafe_panaderia` (P3 daytime trade, German supply-chain hook)
6. `chapel` (P3 wedding-venue completion)
7. `greenhouse` + `orchard_row` (P4 supply-chain visualization for
   restaurant-sourcing story)
8. Remaining cultural / wellness items as Wesley signals demand

Each builds via:

1. Add stub to `lqv/typologies/__init__.py::TYPOLOGIES` (or `AMENITIES`)
2. Write `lqv/<pkg>/<name>.py` with `build(parent, location, variant)` signature
3. Write `lqv/subscene/<name>.py` driver with `PARCEL_CLIP_END_M` /
   `HOUSE_CLIP_END_M` set per [[feedback-subscene-clip-end]]
4. Render A/B/C variants under `renders/sub/runs/<RENDER_RUN_ID>_<name>/`
   per [[feedback-render-run-folders]], serialized per
   [[feedback-render-parallelism]]
5. Append BoQ rows (driver-bulk + per-module) — full-scope only after
   `LQV_BOQ_SCOPE` filter retires post-escritura (see
   [[feedback-boq-scope-filter]])

---

*Written 2026-06-25 (T-2). Backlog only — do not start any of these
builds until after the 27-Jun escritura signing and the renderer-freeze
is released.*
