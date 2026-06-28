# License Obligations — Assets, Code, and Renders

**Status:** living document. Authoritative reference for what we owe whom when we ship the LQV renders, share the project repo publicly, or deliver to Wesley.

## License posture summary

| Asset class | Allowed | Disallowed | Notes |
|---|---|---|---|
| **HDRIs** | CC0 (Poly Haven) | anything else | Poly Haven HDRIs require no attribution; we credit anyway. |
| **PBR materials** | CC0 (Poly Haven, ambientCG) | CC-BY-SA, paid | CC0 keeps the chain clean for redistribution. |
| **3D models** | CC0 (Poly Haven), CC-BY 4.0 (Sketchfab) | CC-BY-SA, NC, ND, custom | CC-BY-SA poisons the project; ND forbids modification (useless for editing); NC blocks Wesley monetising. |
| **Generated assets** | Hyper3D / Hunyuan3D outputs | — | Generator output policy: we own the output; double-check provider TOS at time of generation. |
| **Photographs** | CC-BY, CC0, public domain | "all rights reserved" | Reference photos in `assets/references/` must have provenance. |
| **Code (lqv/*)** | our own | — | Optional MIT / Apache-2.0 if we open-source. |

## CC0 obligations

CC0 ("No Rights Reserved") imposes **no obligations**. We may use, modify, and redistribute freely.

Best practice (NOT required, but we do it):
- Credit the creator and source in `CREDITS.md`.
- Preserve original file names for traceability when possible.

## CC-BY 4.0 obligations (the strict mode)

CC-BY 4.0 ("Attribution") REQUIRES, when we publish or redistribute the work:

1. **Credit the creator** by name (or pseudonym).
2. **Provide a link to the license** (`https://creativecommons.org/licenses/by/4.0/`).
3. **Indicate if changes were made**.
4. **Provide a link to the original source** (the Sketchfab model page).

In practice, every CC-BY 4.0 asset gets a row in `CREDITS.md`:

> **`mango_canopy_v2.glb`** — Created by *Felipe Vargas*, sourced from Sketchfab (https://sketchfab.com/3d-models/xxxxx), CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Modified: re-UV'd, re-textured, scaled to LQV scene units.

## What CC-BY-SA forbids us from using

CC-BY-SA ("Share-Alike") would require the *entire derivative work* to be re-released under CC-BY-SA. That means:

- If we used a CC-BY-SA model in the LQV scene, the whole `.blend` file might need to ship CC-BY-SA.
- Wesley couldn't monetise renders as commercial advertising for the housing park without licensing complications.
- We'd be forced to open the entire repo under CC-BY-SA.

**Decision:** zero CC-BY-SA assets. Mark and remove any if discovered.

## What "indicate if changes were made" looks like in our pipeline

In `CREDITS.md`, for any CC-BY asset we use:

- `Modified: <summary>` line listing the modifications (re-UV, re-scale, material remap, mesh decompose).

This is **per asset**.

## Render output license

The 18 final renders (A/B/C × 6 cameras) are **work product for Wesley van de Camp** under the AI Whisperers engagement. We retain copyright; Wesley has a perpetual, transferable license to use, distribute, and commercialise them for the LQV project and its derivatives (housing park marketing, escritura meeting, fundraising deck, investor pitch, social media).

If Wesley wants to re-license the renders to a third party (e.g., a film), we should be looped in to verify CC-BY chains are respected.

## Code license (`lqv/*` package)

Currently the code is **all-rights-reserved private**.

If we choose to open-source later, suggested licenses:

- **MIT** — maximally permissive; easy for adoption.
- **Apache-2.0** — patent grant; corporate-friendly.
- **CC0-1.0** — for the docs only, never for code.

Whichever we pick, drop `LICENSE` at repo root and add SPDX headers to the lqv files.

## CREDITS.md vs LICENSE_BUNDLE.md

- **`CREDITS.md`** — human-readable attribution list. Per-asset: source URL, creator, license, modifications. This is what Wesley puts on a project credits page.
- **`LICENSE_BUNDLE.md`** — full license texts (CC0, CC-BY 4.0). One file per license referenced. Required to ship alongside any redistribution.

## Photo references in `assets/references/`

If we save reference photographs of Paraguayan cob houses, lapacho blooms, etc., we need:

- The source URL.
- The creator name.
- The license (CC-BY, CC0, public domain, news / editorial fair use).
- A note "REFERENCE ONLY — not embedded in renders" so we know it can be deleted before public release if license requires it.

If a photo is "all rights reserved" we may keep it for *internal* reference but NOT embed it into a render texture and NOT redistribute the file.

## Practical checklist before publishing

When publishing renders or the repo:

- [ ] Every `assets/sketchfab/*` model has a row in `CREDITS.md` with creator, source URL, CC-BY link, and "Modified:" note.
- [ ] Every `assets/polyhaven/*` asset has a row noting CC0 + source URL.
- [ ] No CC-BY-SA, CC-BY-NC, CC-BY-ND, or "all rights reserved" assets are bundled.
- [ ] `LICENSE_BUNDLE.md` includes full text of every license referenced.
- [ ] `LICENSE` at repo root states code license.
- [ ] `README.md` includes a "Credits & Licenses" section pointing at the two files above.
- [ ] Final renders have a small "© 2026 AI Whisperers, used by Wesley van de Camp under perpetual license" tag in the PNG metadata or a corner watermark for non-print deliverables.

## Open questions for Wesley

1. **Is the LQV brand "Quebrada Viva" or "La Quebrada Viva" trademarked?** If so, supply the registration so we can include the ® on renders.
2. **Does Wesley want the renders to be embeddable on the Wesley/Thijs housing-park marketing site?** That changes the metadata embedded.
3. **Will the renders ship in any printed booklet for the escritura meeting?** Print needs 300 dpi A2 / A3 settings; current 2560×1440 hero is enough for A3 max.

## Variant C procedural recipes — no third-party license obligation (additive 2026-06-10)

Variant C (night / blue hour) shipped 2026-06-10 with two visual signatures that are **procedural code recipes** in `lqv/`, not third-party assets. They generate no license obligation because no third-party work is incorporated:

- **Fireflies** — `lqv/flora/fireflies.py` (~80 emission spheres, procedurally scattered after RNG seed).
- **Warm window glow** — `lqv/house/cob.py:build_window_emission` (emission planes positioned inside hidden `WindowCut_*` Boolean cutter outlines).
- **Cool moonlight + low blue sky strength** — `lqv/lighting.py` Variant C branch (Nishita sky strength reduced, sun colour shifted cool, exposure +0.6 set in `build_scene.py`).

License-posture implication: when bundling the final 18 renders + repo, Variant C imagery does **not** add a CC-BY attribution requirement. The only license obligations for C-imagery flow through the same Poly Haven CC0 HDRI (`qwantani_dusk_2`) and CC0 PBR textures already credited for A and B; nothing C-specific is owed. See `docs/external_assets.md` §"Variant C — procedural recipes (no third-party asset, listed for traceability)" for the parallel narrative.

## Cross-references

- `CREDITS.md` — current attribution list.
- `LICENSE_BUNDLE.md` — license texts.
- `LICENSES/README.md` — verbatim CC0 + CC-BY 4.0 legal-code mirror with vendor-terms pointer table (added 2026-06-10 to close the "where is the actual license text" reachability gap from this doc).
- `docs/asset_plan.md` — what assets we want and where they come from.
- `docs/external_assets.md` — current download status, including Variant C procedural-recipe traceability block.
