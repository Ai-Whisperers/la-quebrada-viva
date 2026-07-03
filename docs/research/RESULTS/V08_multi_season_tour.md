# V08 — Multi-season tour for clients (W1.1 item)

**Method:** MEM + general knowledge
**Confidence:** Low (depends on specific 3DGS pipeline output)
**Date:** 2026-06-30

## What V08 is

**Per RESEARCH_CATALOGUE V08:** "Multi-season tour for clients" — different 3DGS views of the same property at different seasons.

## What this means

**Per the 3DGS pipeline (per B07):**
- 5 phone videos of the property → trained 3DGS model
- The model is one "scene" — could be the property in one season
- Adding more videos (or different seasons) = more "scenes" of the same property

**For RV's marketing:**
- Spring scene (flowers, green, fresh)
- Summer scene (lush, warm, vibrant)
- Autumn scene (cooler, golden, harvest)
- Winter scene (drier, less foliage, moody)

**Per V08 (multi-season tour):**
- Each season = 1 trained 3DGS model
- Each takes ~$0.30-0.50 in compute (Vast.ai rental) + ~30 min processing
- So 4 seasons × ~$1-2 = **total $5-10 in compute**
- Plus 5 phone videos per season × 4 = 20 video captures needed

## Cost estimate

**One-time:**
- 20 video captures (5 per season × 4 seasons)
- Wes captures these on 4 different trips to the property (1 per season)
- Compute: $5-10 total
- Processing: ~2 hours of work

**Ongoing (after first 4 seasons):**
- Update the model if property changes
- 1 video per year may be enough (low-cost maintenance)

## Implementation

**When to capture:**
- Spring: September-November (PY spring)
- Summer: December-February (PY summer)
- Autumn: March-May (PY autumn)
- Winter: June-August (PY winter)

**Per season:**
- 1 trip to the property
- 5 phone videos per trip (per existing capture brief)
- Drone LiDAR survey (per W0.5)
- Post-processing in Vast.ai

**Output:**
- 4 separate 3DGS scenes
- 1 website that lets visitors toggle between seasons
- 4 different "moods" of the same property
- Marketing power: "see RV in any season, any time"

## Wes's action

- [ ] Plan 4 trips to PY over the next year (1 per season)
- [ ] Each trip includes 5 phone videos + drone LiDAR
- [ ] Process each trip's videos → 3DGS model
- [ ] Update website with season toggle

## Status

⚠️ Early. Implementation starts after B07 (3DGS pipeline basics) is working. V08 is the second iteration.
