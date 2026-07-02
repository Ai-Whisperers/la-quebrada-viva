# LQV Repo Reconciliation — 2026-07-02

## What happened

The repository at `Ai-Whisperers/la-quebrada-viva` had divergent work in
two places that needed to be merged:

1. **HEAD unpushed commits (1210ba3, July 2)** — Wes's 5 audios
   synthesis (3h 27m, ~28k words → 6 final docs, 95 ideas, 137 research
   items)
2. **origin/master (53c95df, June 30)** — repo audit pass + reconcile +
   ideas taxonomy + Paraguay construction prices

This commit unifies both into the canonical `master` branch.

## What this commit adds

- **Audio synthesis deliverables** (the big batch):
  - `docs/audios/2026-06-30-wes-post-escritura/final/DREAMLIST_NL.md`
  - `docs/audios/2026-06-30-wes-post-escritura/final/ACTIONLIST_ES_EN.md`
  - `docs/audios/2026-06-30-wes-post-escritura/final/IDEAS_LOG.md`
  - `docs/audios/2026-06-30-wes-post-escritura/final/KEY_POINTS.md`
  - `docs/audios/2026-06-30-wes-post-escritura/final/REPO_UPDATES.md`
  - `docs/audios/2026-06-30-wes-post-escritura/final/RESEARCH_CATALOGUE.md`
  - All 5 raw transcripts in `docs/audios/2026-06-30-wes-post-escritura/drafts/`
  - Turboscribe bundle manifest

- **Updated canonical docs** with audio-synthesized content:
  - `STATUS.md` — adds 2026-06-30 audio synthesis entry
  - `docs/HOUSING_PARK_CONCEPT.md` — adds §2.10 (Riverstone Valley + family-anchored community), §6.6.1 (Ipoh-Karai railroad), §6.7.1 (Sonja-route workers), §6.7.2 (Hovenier deep-research), §6.8.1 (Toyota + AI-haggling), §6.8.2 (Steengroeve Ipakari), §7.1 (2030 horizon), §8 Q26-33, §11.1 (new top question)
  - `docs/RESEARCH_GAPS.md` — adds R39-R50 items surfaced by audios

- **Buyer pre-sales page** (`splats/exports/web/`):
  - The Cloudflare-Pages-deployed page at https://lqv-walkthrough.pages.dev
  - 19 visual previews (composites, quicklooks, hero renders)
  - 9 data geojsons + 1 SVG overlay
  - Cesium 3D viewer integration
  - Trees estimated from real NDVI raster
  - API keys checklist + map audit document

- **Splats tooling** (`splats/`):
  - `tools/self_host_train.py` — Vast.ai rental launcher + SSH + COLMAP/gsplat
  - `tools/threejs_export.py` — Three.js viewer export + R2 upload
  - `tools/build_atlas.py`, `ingest_album.py` — supporting scripts

## What's NOT committed (and why)

- `docs/audios/.../wes_*.mp3` and `docs/audios/.../tmp_mp3/*.mp3` — 275MB of
  audio recordings. Excluded via .gitignore. Stored externally
  (`/tmp/lqv-keep/audios/` for now; should move to R2 or similar).
- `splats/exports/web/.wrangler/` — Wrangler build cache
- `splats/exports/web/data/.next/` — Next.js cache
- `splats/exports/web/data/lqv-secrets/cesium-token.js` — Cesium ion token,
  already in `~/.lqv/splats.env`. Generated at deploy time by the preflight.

## What should still happen

1. **Push this commit to origin/master** (manual: `git push origin master`)
2. **Re-deploy buyer page** with the consolidated splats/ tree
3. **Move audio files to R2** (`s3 cp wes_2026-06-30_full.mp3 s3://wes3dassets/audios/`)
4. **Re-run preflight** to verify all key data files exist on deployed page
5. **Update buyer page** to communicate the full 62-ha vision (currently
   positions LQV as the whole project; should position as first cob house
   on the larger Riverstone Valley project)

## Author / commit message

```
feat(reconcile): merge audio synthesis + buyer pre-sales into master

- 5 audios → 6 final synthesis docs (DREAMLIST, ACTIONLIST, IDEAS_LOG,
  KEY_POINTS, REPO_UPDATES, RESEARCH_CATALOGUE) + drafts (5 transcripts)
- Updated STATUS.md, HOUSING_PARK_CONCEPT.md, RESEARCH_GAPS.md with
  audio-synthesized content
- splats/ subtree: buyer pre-sales page (live at lqv-walkthrough.pages.dev),
  Vast.ai rental tooling, Three.js viewer export
- New canonical docs: this REPO_RECONCILIATION_2026-07-02.md

🤖 Generated with Claude Code (Erebus)

Co-Authored-By: Claude <noreply@anthropic.com>
```
