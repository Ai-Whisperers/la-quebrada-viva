---
name: verify-render
description: Visual verification checklist for a La Quebrada Viva render image - the 10 design rules, species accuracy, and variant correctness. Use after every preview or final render, before claiming any render is done.
---

# Verify render

Input: a render PNG (`renders/_preview_<V>_<cam>.png` or `renders/<V>_<cam>.png`). **Read the image and judge what is actually visible** — skip checklist items the camera can't see, and say so.

## A. The 10 rules (CLAUDE.md / MASTER_BRIEF §14)

1. Cob walls organic — no straight edges, no right angles, no box silhouette.
2. Walls read as lime-washed earth — warm off-white/ochre, matte; not grey cement.
3. No standing water except the mandated flat-rock stream pool — no puddles, no open containers.
4. Visible raised stone foundation — earth walls never meet the ground directly.
5. Roof overhangs read wide (90cm+) with deep shadow under the eaves.
6. Corredor (veranda) present and reads as usable shaded space.
7. (Detail shots only) micro-hydro/battery visible where expected.
8. Reads Paraguayan — corredor, tatakuá dome, low-pitched living roof; NOT Tuscan/Bali/Earthship.
9. No solar panels on the living roof.
10. (Detail shots only) cistern mesh visible on tanks.

## B. Species accuracy

- Pindo palms: fronds droop (plumose), not stiff coconut/date fans.
- Lapacho: Variant A = bare branches + hot-pink bloom (`#E85A8C`–`#F0A0C8`) + petal carpet; Variant B = green-leafed, **zero pink**.
- Mango: dense dark rounded crowns. Bamboo: clumped near stream, leaning. Agave: rosettes on lower terraces. Tree ferns: riparian, under canopy.

## C. Variant + technical

- A: warm low golden-hour light from NNW, long shadows, exposure reads slightly dark-rich.
- B: flat overcast, soft shadows, slightly lifted exposure.
- Camera matches its brief (hero shows house + escarpment backdrop + stream foreground; petal_macro is a ground-level close-up).
- No black frame, no missing materials (magenta), no floating/intersecting geometry at focal points, footbridge not blocking the hero sightline.

## Output format

```
VERDICT: PASS | FAIL
Checked: <items actually visible from this camera>
Violations: <numbered list with what/where in frame, or "none">
Not assessable from this camera: <items>
```

A FAIL must name the offending object/area so the fix is actionable. Don't pass a render "because it looks nice" — pass it because the checklist passes.
