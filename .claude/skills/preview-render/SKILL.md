---
name: preview-render
description: Build and render a fast 1280x720 preview of the La Quebrada Viva scene for one variant/camera, then visually verify it against the design rules. Use after any code change to lqv/ or when asked to "check the scene", "preview", or "render a test".
---

# Preview render

Goal: one verified preview image, cheap and fast. Never jump straight to finals.

## Steps

1. **Smoke test first** (skip if you just ran one this session):
   ```bash
   scripts/smoke_test.sh
   ```
   Builds the scene with `RENDER_SKIP=1` — no render. If it prints a Python traceback, STOP and fix the code; do not render.

2. **Render the preview** (variant `A` or `B`, camera one of `hero|stream_up|terrace|cliff|dusk|petal_macro`):
   ```bash
   scripts/render_preview.sh A hero
   ```
   Output: `renders/_preview_A_hero.png` (~1–3 min on GPU). Variant `C` is not implemented — refuse it.

3. **Read the PNG with the Read tool and actually look at it.** Then run the `/verify-render` checklist against the image.

4. **Report**: one short paragraph — what changed, PASS/FAIL per checklist item that's relevant, and whether it's ready for a final.

## Remember

- Previews skip the canopy volume: judge geometry, materials, and composition here; judge atmosphere/volumetrics only on finals.
- Every run overwrites `scene.blend` (the script backs it up to `scene.blend.session-backup` first).
- If the image is black or empty, the usual causes are: wrong `RENDER_CAM` (falls back to hero with a warning), or a crashed build — check the script's console output before re-rendering.
