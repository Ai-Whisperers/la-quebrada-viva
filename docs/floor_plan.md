# Floor Plan — La Quebrada Viva House

**Status:** living document. Annotated room-by-room program for the cob/bottle house. Coordinates are in metres, origin at the geometric centre of the inside floor plate. North is +Y. The house is rotated 0° (axes-aligned with the render scene).

This file is the source-of-truth for room sizes and adjacencies. When `lqv/house/cob.py` walls are sculpted, they wrap this program.

## Overall footprint

- **Conditioned (interior) area:** 95 m².
- **Corredor (covered exterior) area:** 38 m² (wraparound 1.9 m deep on three sides).
- **Total roof area:** 145 m² (includes corredor overhang).
- **Building height to eaves:** 2.8 m.
- **Building height to ridge:** 4.2 m.
- **Roof type:** sod, low-pitch 18°.
- **Roof overhangs:** north 1.2 m, south 0.9 m, east 1.0 m, west 1.5 m (deep west to shade afternoon sun).

## Room program

### Corredor (covered verandah)

- **Dimensions:** wraparound L-shape; 1.9 m deep × 25 m linear.
- **North side (entry):** 4.5 m long, hosts the front door + a wall-mounted Virgin of Caacupé niche.
- **East side (morning):** 8 m long, hosts the hammock + low lapacho table.
- **South side (kitchen extension):** 6 m long, hosts the tatakuá and a long communal dining table.
- **Floor:** sandstone slabs on lime-stabilized base.
- **Furnishings:** see `lqv/house/corredor_props.py`.
- **Lighting:** 4 wrought-iron sconces with 4 W LED warm-white, dusk-on.

### Sala / living-dining (12 m²)

- **Coords:** centred at (0, +1.5), 4.0 m × 3.0 m.
- **Function:** primary social room; mate / tereré central.
- **South window:** 2.4 m × 1.6 m double Low-E sliding (`WindowCut_LivingS`).
- **West window:** 1.8 m × 1.2 m double Low-E (`WindowCut_LivingW`).
- **Floor:** polished red brick.
- **Furnishings:** lapacho dining table (1.8 × 0.9 m), four turned chairs, low chest with ñandutí runner.

### Kitchen (10 m²)

- **Coords:** centred at (−3.0, +1.0), 3.5 m × 2.8 m.
- **Function:** prep + indoor cooking. Tatakuá is OUTSIDE (Rule 8 placement).
- **North window:** 1.2 m × 0.9 m double Low-E (`WindowCut_KitchenN`); over the sink.
- **East window:** 0.8 m × 0.6 m single clear (`WindowCut_KitchenE`); ventilation.
- **Counter:** lapacho slab, 60 cm deep, with under-counter open shelves.
- **Sink:** ceramic single basin; spring-fed cold + PV-heated header-tank hot.
- **Hob:** 2-burner LPG (45 kg cage external south wall); ventilation hood ducted out east wall.
- **Refrigeration:** 12 V DC chest fridge run from LiFePO4.

### Bedroom (12 m²)

- **Coords:** centred at (+3.0, +1.5), 4.0 m × 3.0 m.
- **East window:** 1.4 m × 1.1 m double Low-E (`WindowCut_BedroomE`); morning light.
- **South window:** 1.2 m × 1.0 m double Low-E (`WindowCut_BedroomS`); cross-vent.
- **Bed platform:** built-in lapacho, queen-size; storage drawers below.
- **Wardrobe:** built-in cob alcove, lapacho door.

### Bathroom (5 m²)

- **Coords:** centred at (−1.5, +4.0), 2.5 m × 2.0 m.
- **North window:** 0.6 m × 0.4 m frosted single (`WindowCut_BathroomN`); privacy + vent.
- **Shower:** ceramic floor, rainshower head fed from PV-heated header tank.
- **Composting toilet:** twin-chamber, vault under the floor; vent stack out east wall.
- **Greywater:** to constructed wetland east of building.

### Bottle wall (west façade, structural + decorative)

- **Width:** 4 m × **height:** 2.2 m.
- **Bottle count:** 384 (Fibonacci-spaced grid 24 wide × 16 tall, omitting structural columns).
- **Glazing function:** west-afternoon light filters through colored glass.
- **Behind it:** the back of the sala / dining area. The bottles project light fragments into the dining space all afternoon.

### Loft / storage (8 m²)

- **Coords:** above bedroom, accessed via lapacho ladder.
- **Function:** dry storage; harvest pantry.

## Adjacencies (key culture+climate logic)

1. **Tatakuá ↔ Kitchen ↔ Dining table** = the cooking-eating gradient, all on the south corredor.
2. **Sala / dining ↔ Bedroom** separated only by a half-height cob wall (privacy by curtain) for cross-ventilation in summer.
3. **Bathroom on the north** so the worst-noise / odor exposure is on the cooler quiet side.
4. **Service spine** (refrigerator, water tank, electrical panel) on the **service wall** between kitchen and bathroom; one trench for all rough-in (Phase 7).

## Compliance with the 10 rules

1. **Rule 1 (no right angles):** all interior corners are curved 30 cm radius in cob.
2. **Rule 2 (lime not cement):** lime plaster confirmed in `docs/build_sequence.md` Phase 6.
3. **Rule 3 (no standing water):** stream pool is outside the building; greywater wetland is fast-circulating.
4. **Rule 4 (no ground-touch):** 60 cm stone foundation under all earthen walls.
5. **Rule 5 (wide overhangs):** confirmed 0.9–1.5 m per side.
6. **Rule 6 (passive ≤ 35 °C):** cross-vent through E-W axis; sod roof for thermal mass; corredor shade.
7. **Rule 7 (outage-proof):** micro-hydro intake + LiFePO4 visible from cliff cam.
8. **Rule 8 (Paraguayan first):** corredor, tatakuá, mate ritual all front-and-centre.
9. **Rule 9 (PV on steel, not sod):** confirmed in `lqv/site/services.py` (planned).
10. **Rule 10 (mosquito mesh):** all rainwater tanks meshed.

## Cross-references

- `docs/MASTER_BRIEF.md` — the 10 rules.
- `docs/build_sequence.md` — how this floor plan is built physically.
- `docs/section_view.md` (planned) — NW-SE cut showing roof + corredor + cliff.
- `lqv/house/cob.py` — sculpted walls following this plan.
- `lqv/house/window_specs.py` — every `WindowCut_*` keyed to this plan.
- `lqv/house/corredor_props.py` — furnishings for the corredor described above.
