---
name: final-renders
description: Render the deliverable final images for La Quebrada Viva (12 finals - variants A/B x 6 cameras) at full resolution, verify each, update the STATUS.md manifest, and commit. Use when asked for "finals", "deliverables", or "render everything".
---

# Final renders

Deliverable: **12 finals** — variants A and B × cameras `hero|stream_up|terrace|cliff|dusk|petal_macro`. Variant C is not implemented; never attempt it.

Policy (set by the scripts — don't override): hero camera 512 samples @ 2560×1440; all other cameras 256 samples @ 1920×1080.

## Steps

1. **Preconditions**: working tree committed (`git status` clean for `lqv/` and `build_scene.py`), and a recent preview of the same variant/cam passed `/verify-render`. Never burn a 10–30 min final on unverified code.

2. **Single final**:
   ```bash
   scripts/render_final.sh A hero      # -> renders/A_hero.png
   ```
   **Whole matrix** (long — hours; prefer running it as a background task and checking output as files land):
   ```bash
   scripts/render_all_finals.sh
   ```

3. **Verify each output**: Read the PNG, run the `/verify-render` checklist. A final that fails the checklist is not done — fix and re-render.

4. **Bookkeeping**: tick the render in the STATUS.md manifest (☐ → ☑), then commit — finals are tracked in git:
   ```bash
   git add renders/*.png STATUS.md && git commit -m "render: <variant>_<cam> final"
   ```

## Remember

- Finals include the canopy volume (previews don't) — expect different atmosphere than the preview; that alone is not a failure.
- Variant A: exposure −0.2, bare+flowering lapacho, petal carpet. Variant B: exposure +0.3, fully leafed, overcast. Wrong foliage for the variant = automatic FAIL.
