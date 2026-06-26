# Deferred renderer bugs — post-escritura sprint queue

**Status as of 2026-06-26.** All three bugs RESOLVED at commit `78433a7` ("feat(materials,subscene,typologies,amenities,flora): post-review polish wave", 2026-06-15). The 85e86aa byte-freeze was superseded under explicit Ivan authorization for the escritura beauty sprint — print-pack at `dist/print_pack_2026-06-27/` remains SHA-pinned independently, so the post-`85e86aa` material work cannot retroactively alter shipped bytes. This doc is retained as the historical reproducer / acceptance record.

Ranked by leverage (assets unblocked per fix):

| # | Bug | Assets gated | Effort | Status |
|---|---|---|---|---|
| 1 | Black-water shader (`pool_water` + river chain) | ~12 | ½ day | ✓ resolved 78433a7 — see `lqv/materials/glass.py:35-66` |
| 2 | `lapacho_timber` plastic-laminate read | 17/17 | 1 day | ✓ resolved 78433a7 — see `lqv/materials/wood.py:77-93` |
| 3 | Photoreal-flora `.003`-LOD name-collision | ~3 | ½ day | ✓ resolved 78433a7 — see `lqv/flora/photoreal.py:37-82` |

---

## Bug 1 — Black-water shader (highest leverage) ✓ RESOLVED at 78433a7

### Symptom
Every water surface — pool, jacuzzi, reflection pond, river, creek — renders as an opaque pure-black slab in variants A (golden hour) and C (blue hour). Variant B (overcast diffuse fill) shows weak reflection because hemispherical light masks the broken specular response. See `renders/sub/latest/eco_pool_{A,B,C}.png`, `floating_dining_{A,B,C}.png`, `bamboo_river_house_{A,B,C}.png`, `italian_river_house_4pax_{A,B,C}.png`, `container_river_house_{A,B,C}.png`, `labrisa_lounge_{A,B,C}.png` for the full pattern.

### Diagnosis
The `pool_water` (and the parallel `river_water`) Principled BSDF is registered with transmission=0, IOR ~1.0, and a black base color — so the surface absorbs every ray instead of behaving as a dielectric. Correct config is a glass-like Principled with base_color near (0.02, 0.06, 0.10), transmission=1.0, IOR=1.33, roughness=0.02–0.06, plus a Bump or Noise-driven normal for the surface.

### Reproducer
```bash
RENDER_RUN_ID=bug1_repro RENDER_VARIANT=A RENDER_RES=preview RENDER_SAMPLES=64 \
PYTHONPATH=. /home/ai-whisperers/.local/bin/blender -b -P lqv/subscene/eco_pool.py
# Inspect renders/sub/latest/eco_pool_A.png — pool reads as black slab with hard rectangular edge.
```

### Fix sketch (post-freeze)
1. Locate the `pool_water` and `river_water` material entries in the material registry (likely `lqv/site/base.py` or `lqv/materials/water.py`).
2. Replace with the dielectric config above. Single source of truth — all 12 assets pick it up via registry lookup, no per-asset code change.
3. Smoke-render the 6 worst offenders at preview res, verify A and C now show specular highlight + tinted transmission.
4. Validate `floating_dining_C` (blue hour) for firefly behavior on water — high IOR + low roughness will fire stars unless variance is clamped.

### Acceptance
A-variant pool render shows sky reflection. C-variant pool render shows tinted blue-hour reflection with no full-black pixels in the water polygon. No regression in non-water assets (RNG seed ordering invariant).

---

## Bug 2 — `lapacho_timber` plastic-laminate ✓ RESOLVED at 78433a7

### Symptom
Decks, planks, coping, handrails, and column sleeves across all 17 typologies render as flat orange-salmon plastic. No wood grain, no plank seams, no UV scale — reads as injection-molded polypropylene "garden furniture." Combined with the orange-placeholder doors/shutters/columns from meta-pattern 2 of `docs/_archive/2026-06-1X/HOUSES_REVIEW_2026-06-14.md`, the entire palette skews 1990s patio set.

### Diagnosis
`lapacho_timber` is registered as a flat base_color (~hex `#D67A4A`) Principled BSDF with no texture inputs. The asset library has a usable wood albedo + roughness + normal trio under `assets/textures/lapacho/` (verify path), but the registry never wires them in.

### Reproducer
```bash
RENDER_RUN_ID=bug2_repro RENDER_VARIANT=A RENDER_RES=preview RENDER_SAMPLES=64 \
PYTHONPATH=. /home/ai-whisperers/.local/bin/blender -b -P lqv/subscene/italian_river_house_4pax.py
# Deck planks show no grain, no seam, no specular variation.
```

### Fix sketch (post-freeze)
1. Wire `lapacho_timber` to an Image Texture node chain: albedo (Color), roughness (Non-Color → Roughness), normal (Non-Color → Normal Map → Normal).
2. UV scale: 1 unit = 1 m, plank tile = 0.15 m × 2.4 m. Use Box mapping if UVs are not unwrapped on placeholders.
3. Add a Voronoi-driven plank-seam mask (BW → mix to darker base color, 5–10% darken).
4. Tint base color toward (0.55, 0.32, 0.18) — current orange is too warm; lapacho heartwood reads brown-red, not salmon.
5. Repeat for `lapacho_petal_pink` and `lapacho_bark` if they share the same flat-color failure mode.

### Acceptance
Side-by-side: pre/post on the same deck plank shows visible grain, plank seam, and specular variation under raking light. Three spot-checked assets (`floating_dining`, `italian_river_house_4pax`, `bamboo_boomhut_treehouse`) re-render with the same camera and read as wood, not plastic.

---

## Bug 3 — Photoreal-flora `.003`-LOD name collision ✓ RESOLVED at 78433a7

### Symptom
`eco_retreat_modern_oasis` (and likely other dense-jacaranda assets) renders fail with `bpy.context.scene.collection.objects.unlink(obj)` errors of the form `Object '*_LOD0.003' not in collection 'Scene Collection'`. Current workaround is `RENDER_FLORA_PHOTOREAL=0`, which falls back to procedural cones-and-spheres flora that itself reads as Fisher-Price toys.

### Diagnosis
`lqv/flora/photoreal.py:_append_object_from_blend` re-appends the same LOD asset multiple times per scene. Blender's `bpy.data.libraries.load(...)` auto-suffixes the second copy with `.001`, third with `.002`, etc. When the loader later tries to unlink by the original name, it hits an orphan suffixed object that lives in `bpy.data.objects` but was never linked to `Scene Collection`.

### Reproducer
```bash
RENDER_RUN_ID=bug3_repro RENDER_VARIANT=A RENDER_RES=preview RENDER_SAMPLES=32 \
RENDER_FLORA_PHOTOREAL=1 \
PYTHONPATH=. /home/ai-whisperers/.local/bin/blender -b -P lqv/subscene/eco_retreat_modern_oasis.py \
  > /tmp/bug3.log 2>&1
grep "not in collection" /tmp/bug3.log
```

### Fix sketch (post-freeze)
1. Make `_append_object_from_blend` idempotent: before `libraries.load`, check `bpy.data.objects.get(name)`; if present, deep-copy via `obj.copy()` + `obj.data = obj.data.copy()` instead of re-appending.
2. Or — track appended-name → bpy.data.object refs in a per-scene dict; on second placement, use `dict[name].copy()` not `libraries.load`.
3. Defensive: in the unlink path, guard with `if obj.name in scene.collection.objects:` before unlinking.
4. Run the workaround disabled (`RENDER_FLORA_PHOTOREAL=1`) on all 17 assets; verify no `.003`-name errors in any log.

### Acceptance
`bash scripts/render_review_2026-06-14.sh` runs end-to-end with `RENDER_FLORA_PHOTOREAL=1` and zero `not in collection` lines across all 51 logs in `renders/sub/runs/review_2026-06-14_logs/`.

---

## Still open (carry-forward to P1.A residue + P1.B)

These were flagged in the critic pass alongside Bug 1/2/3 but were *not* part of the 78433a7 polish wave. Active sprint queue post-escritura:

- **Rule 4 stone-foundation plinth enforcement** (P1.A.4) — endemic violation across ~13 typologies. Per-typology builder edits, not a registry fix. ~1.5 days.
- **HDRI swap to cerrado / Atlantic-Forest-edge** (P1.A.5) — needs asset-researcher pass, CC0 / CC-BY 4.0 only. ~0.5 + 0.5 day.
- **Per-variant lighting differentiation (T1.6)** (P1.C) — A=lapacho-bare-pink golden hour, B=overcast neutral, C=blue-hour + fireflies. Queue after the 384-PNG framing batch.
- **Background-tree asset replacement** (P1.C) — popcorn-blob foliage on stick legs. Photoreal-flora pipeline is now safe (Bug 3 fixed), so the swap is unblocked.

## How the resolved sprint (78433a7) was executed

Recorded for the post-mortem record:
1. Renderer byte-freeze was superseded under Ivan-authorized "escritura beauty sprint" carve-out (2026-06-15). Print-pack SHA pinning held independently on disk, so no shipped bytes were altered.
2. Tackled in order on `master`: Bug 1 → smoke-render the worst water assets → Bug 2 → re-render wood assets → Bug 3 → full batch with `RENDER_FLORA_PHOTOREAL=1`.
3. Commits: `78433a7` (omnibus polish wave) — see `lqv/materials/glass.py`, `lqv/materials/wood.py`, `lqv/flora/photoreal.py` for the in-code fix landmarks.
4. Meta-patterns 9/10/11 from `docs/_archive/2026-06-1X/HOUSES_REVIEW_2026-06-14.md` are now struck.
