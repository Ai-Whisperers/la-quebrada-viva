# Section View — La Quebrada Viva (NW–SE cut)

**Status:** living document. Describes the diagrammatic section cut through the LQV house and immediate site. The section view is the single most important drawing for explaining the design to non-architects.

The cut runs **NW (upper escarpment) → SE (stream pool)**, slicing through the cob house centred on the corredor. The render-side stub for this is `lqv/site/section_view.py`.

## Section line

- **Start point** (NW, upper site): (−300 m, +300 m), elevation 312 m a.s.l.
- **End point** (SE, stream lower pool): (+350 m, −350 m), elevation 240 m a.s.l.
- **Section length:** ~ 920 m horizontal.
- **Elevation drop:** 72 m over the cut.
- **Section width** (slab to show context): 30 m.

## What the section reveals (NW → SE, left → right)

1. **Cerro Patiño shoulder (NW)** — exposed sandstone bedrock, sparse Atlantic Forest, 312 m.
2. **Spring outlet (~280 m)** — the gravity-fed potable source; small wood collection box visible.
3. **Upper terrace / agroforest** — pindo palms, lapacho saplings, mandioca rows.
4. **Cob/bottle house — building cut** — section through corredor, sala, kitchen, tatakuá, sod roof.
5. **Stone footing at 60 cm** — visible Rule 4 separation; French drain stones below grade.
6. **Lime plaster layers** — 8 mm hard coat + 3 mm wash, exaggerated for clarity.
7. **Roof framing** — lapacho rafter + cana brava cane mat + sod 15 cm.
8. **Lower terrace / kitchen garden** — yuyos, maize, mandioca.
9. **Footbridge** — two stone abutments + lapacho deck.
10. **Stream upper weir** — micro-hydro intake; vertical fall ~1.8 m.
11. **Stream pool** — flat sandstone slabs; the only "still water" allowed (Rule 3 carve-out: this is a mandated flat-rock landscape feature, not standing).
12. **Lower stream chute** — outflow to property boundary.
13. **Cliff edge (SE)** — escarpment drop to the lower property line.

## Annotations to add on the rendered section

- 🟦 **Water arrows** (blue) showing spring → potable header tank → kitchen → greywater wetland → stream pool overflow.
- 🟨 **Solar PV vector** (yellow): summer sun NW–S–SW arc with 35 °C shadow line.
- 🟧 **Winter sun vector** (orange): NNE rise → NNW set; lower altitude; corredor lit deep into the room.
- 🟩 **Cross-ventilation arrow** (green): morning E breeze through bedroom east window, exiting through kitchen east window.
- 🟪 **Earthen wall envelope** (purple shading): the thermal-mass extent.

## Use cases for the section

1. **Wesley's escritura meeting (2026-06-27)** — to show the notary and the seller side that this is a serious project, not speculation.
2. **Municipality anteproyecto submission** — a section view is required by Escobar municipal building code.
3. **Investor pitch** — to explain the off-grid systems integration.
4. **Construction reference** — annotated A2 print for site office.

## Render setup (for when `lqv/site/section_view.py` lands)

- Orthographic camera, clipped to the 30 m section slab.
- View parallel to (NW–SE direction × Z-up), camera height 4 m a.s.l. (above the house ridge).
- Output: A2 portrait, 4961 × 7016 px at 300 dpi.
- Materials simplified to flat fills + outline (toon shader pass), then composited with the AgX final.
- Text labels rendered as Blender text objects, NOT post in Photoshop (keeps it reproducible).

## Cross-references

- `docs/MASTER_BRIEF.md` — design rules referenced in annotations.
- `docs/floor_plan.md` — the plan that this section cuts through.
- `docs/build_sequence.md` — Phase numbers visible in the labeled section.
- `lqv/site/section_view.py` — render stub (dormant).
- `lqv/site/site_plan.py` — the master layout from which the section line was chosen.
