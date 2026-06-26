# Master TODO — La Quebrada Viva, all open work

**Authored 2026-06-25 (T-2 to escritura).** Single source of truth for every open track. Phase numbering aligns with `docs/housing_park_phasing.md` (P1–P4) and adds **P0a** (escritura week), **P0b** (closing day + T+1), and cross-cutting tracks **CC-TOOL**, **CC-DOC**, **CC-SALES**, **CC-BUILD**.

Each item: ID, owner (Ivan/AI/Wesley/Peña), gate, ETA. `[CRIT]` blocks something downstream. `[FRZ]` respects `build_scene.py` byte-freeze at `85e86aa`. `[POST-FRZ]` unblocks 2026-06-28.

---

## P0a — Escritura week (T-2 → T-0, 2026-06-25 → 2026-06-27) `[CRIT, FRZ]`

This is the only work that matters right now. Everything else waits.

### P0a.1 — T-1 evening (2026-06-26 PM)
- [ ] **VERIFY.sh dry-run** — `bash dist/print_pack_2026-06-27/VERIFY.sh` returns clean (3 checks). Owner: AI. Gate: P0a.2.
- [ ] **Bundle SHA re-confirm** — `sha256sum dist/wesley_bundle_20260616-1715.zip` matches `9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c`. Owner: AI.
- [ ] **GPG detached sig** — `gpg --armor --detach-sign --local-user weissvanderpol.ivan@gmail.com --output wesley_bundle_20260616-1715.zip.asc wesley_bundle_20260616-1715.zip`. Owner: **Ivan** (passphrase).
- [ ] **Tag check** — `git tag -l escritura-2026-06-27` resolves to `0081129` (or successor). Owner: AI.
- [ ] **Print pack** — 3× of (deck cover, BoQ p21, English appendix pp25-26, Pelton appendix p27); 1× Pelton contact sheet A4. Owner: Ivan.
- [ ] **USB stick #1 + #2** — zip + `.sha256` + `.asc` on two sticks (redundancy). Owner: Ivan.
- [ ] **Boleto PDF** — confirm `docs/2026-04-28_boleto_compraventa_torrasca-vandecamp.pdf` opens; paper original or notarised copy in folder.
- [ ] **Funds comprobante** — Gs. 2.252.700.000 ready (Cl. CUARTA). Owner: Ivan.
- [ ] **`git status` clean on master** — no uncommitted, no untracked beyond known excludes (`scripts/mcp_daemon.py`, satellite tifs, boleto/escritura PDFs).
- [ ] **`git fetch && git log @{u}..HEAD`** returns empty (master synced).

### P0a.2 — T-0 morning (2026-06-27, ≤08:00 -03)
- [ ] **Send PDF v-final** — `docs/escritura_deck/escritura_deck_v6.pdf` to Wesley + Peña inboxes. Owner: Ivan. Reply-To: Ivan.
- [ ] **Share-link fallback** — WhatsApp upload (per C9 in CONTINGENCIES). Owner: Ivan.
- [ ] **WALLET_CARD in pocket** — `docs/escritura_deck/WALLET_CARD.md` printed bifold. Owner: Ivan.

### P0a.3 — In-room (10:00 -03 at Escribanía Peña)
- [ ] **Verbal**: Cl. OCTAVA (ii) — seller comprobantes within 5 hábiles. Owner: Ivan.
- [ ] **Confirm all 6 padrones** referenced correctly in the escritura draft. Owner: Ivan + Peña.
- [ ] **Hand over USB #1** — Peña-side. Verify reads clean on her machine.
- [ ] **Sign**.

---

## P0b — Closing day + T+1 (2026-06-27 PM → 2026-06-28) `[CRIT]`

### P0b.1 — Same-day
- [ ] **T+1 debrief stub** — fill `docs/T_PLUS_1_DEBRIEF.md` §1 (outcome) within 2 h of signing. Owner: Ivan.
- [ ] **Bundle delivered confirmation** — Peña confirms USB read clean (text/WhatsApp OK). Owner: Ivan.

### P0b.2 — 2026-06-28 (T+1)
- [ ] **Full debrief** — sections 2–6 of `docs/T_PLUS_1_DEBRIEF.md`. Owner: Ivan + AI.
- [ ] **Tag promote** — `git tag escritura-2026-06-27-signed` on the same commit as `escritura-2026-06-27`. Owner: AI.
- [ ] **Memory update** — `project_state_2026_06_27_signed.md` capturing outcome + new constraints. Owner: AI.
- [ ] **Wesley followup** — confirm phase-2 timeline expectations + any deck feedback. Owner: Ivan.
- [ ] **Lift the freeze** — `build_scene.py` no longer byte-frozen; release flag in memory `feedback_render_run_folders` if any constraint relaxes.

---

## P1 — Post-escritura material sprint + house imagery `[POST-FRZ]`

Starts 2026-06-29. Pre-condition: P0a + P0b complete and signed.

### P1.A — DEFERRED_BUGS triage (week 1)
- [x] **P1.A.1 Bug 1: black-water shader** — shipped at `78433a7` (2026-06-15). Dielectric Principled at `lqv/materials/glass.py:35-66`. ✓
- [x] **P1.A.2 Bug 2: lapacho_timber plastic** — shipped at `78433a7` (2026-06-15). `textured_principled('old_planks_02')` + secondary Voronoi at `lqv/materials/wood.py:77-93`. ✓
- [x] **P1.A.3 Bug 3: photoreal-flora `.003` LOD collision** — shipped at `78433a7` (2026-06-15). `_LOADED_HEROES` + `cached.copy()` at `lqv/flora/photoreal.py:37-82`. ✓
- [ ] **P1.A.4 Stone-foundation plinth (Rule 4)** — per-typology builder edit pass, 60 cm sandstone plinth on the 13 typologies missing it. Owner: AI. Effort: 1.5 days.
- [x] **P1.A.5 HDRI swap** — closed 2026-06-26. Cerrado/Atlantic-Forest-edge biome-correct dispatcher landed at `lqv/lighting.py:19-23`: A=`bryanston_park_sunrise_4k.exr` 0.8, B=`xanderklinge_4k.exr` 1.4, C=`kloppenheim_07_4k.exr` 0.5. Legacy `qwantani_dusk_2_4k.exr` quarantined to `assets/hdris/_quarantine/`. All three CC0 per `LICENSE_BUNDLE.md`.

### P1.B — House imagery shotlist execution (week 2)

Per `docs/HOUSE_IMAGERY_SHOTLIST.md`. 16 houses × ~24 PNGs = **384 finals + 384 previews**.

- [x] **P1.B.1 Furniture stubs** — closed 2026-06-26. `lqv/furniture.py` ships `furnish_interior(col, *, footprint_w, footprint_l, origin_xy, floor_z, pax, style, variant, name_prefix)` with style families bamboo|lapacho|stone|cob|container. Variant-keyed lantern emission `{A: 0.0, B: 0.6, C: 1.0}`. CHANGELOG 2026-06-26.
- [x] **P1.B.2 `RENDER_VIEW` env var + camera helpers** — closed 2026-06-26. Public dispatcher `cameras.make_view_camera(cfg, target, distance, height, lens)` covers `{hero3q, elevation, plan, section, interior, xray}`. Default `RENDER_VIEW=hero3q` at `lqv/config.py:59`. 22 bypass-pattern drivers migrated. CHANGELOG 2026-06-26.
- [x] **P1.B.3 `apply_xray_override`** — closed 2026-06-26. `apply_xray_override` + `XRAY_OPAQUE_MATERIALS` frozenset allowlist landed in `lqv/subscene/base.py`. CHANGELOG 2026-06-26.
- [ ] **P1.B.4 Driver wire-up** — per material family, one PR each: italian, bamboo-shell, beton+villa, hobbit+cob, container, river. Owner: AI. Effort: 2 days.
- [ ] **P1.B.5 Preview batch overnight** — 768 PNGs at 64 samples, `RENDER_RUN_ID=multiview_preview_2026-07-0X`. Owner: AI. Effort: 5.3 h render + 1 h review.
- [ ] **P1.B.6 Framing fix pass** — per-asset camera tuning from contact-sheet review. Owner: AI. Effort: 1 day.
- [ ] **P1.B.7 Final batch (×2 overnights)** — 384 PNGs at 256–512 samples. Owner: AI. Effort: 10.7 h render.
- [ ] **P1.B.8 Render catalogue refresh** — regen `docs/render_catalogue/catalogue.json` + per-asset contact sheets. Owner: AI. Effort: 0.5 day.

### P1.C — Composite refresh (week 3)
- [ ] **P1.C.1 Per-variant lighting differentiation (T1.6)** — A=lapacho-bare-pink ambience, B=neutral, C=blue-hour + fireflies. Was deferred pre-freeze. Owner: AI. Effort: 1 day.
- [ ] **P1.C.2 Background-tree replacement** — photoreal flora gated on Bug 3. Owner: AI. Effort: 0.5 day.
- [ ] **P1.C.3 6-camera composite re-render** — hero/stream_up/terrace/cliff/dusk/petal_macro × A/B/C = 18 finals at the new material quality. Owner: AI. Effort: overnight.
- [ ] **P1.C.4 FINAL_GALLERY refresh** — `docs/FINAL_GALLERY.md` re-pointed at new SHAs. Owner: AI.

---

## P2 — Phase 2 typologies + lodging fill (months 9–18 post-closing)

Per `docs/wesley_phase3_inventory.md` Phase 2 column. Wesley's revenue-anchor build-out.

### P2.A — Event + reception (anchor)
- [ ] **P2.A.1 `lqv/amenities/event_hall.py`** — 150-pax envelope. Cross-vaulted bamboo + concrete. Subscene driver + 24-shot imagery. Owner: AI. Effort: 2 days.
- [ ] **P2.A.2 `lqv/amenities/reception.py`** — entry-control + concierge. **Gate: confirm creek-side vs road-side with Wesley**. Owner: AI + Wesley input. Effort: 1 day post-gate.
- [ ] **P2.A.3 `lqv/amenities/quincho_kitchen.py`** — shared with event hall; delivered Phase 2 (restaurant indoor dining waits for P3). Owner: AI. Effort: 1.5 days.

### P2.B — Lodging fill
- [ ] **P2.B.1 `lqv/typologies/glamping_tent.py`** — safari tent on raised deck, 30 m². Owner: AI. Effort: 1 day.
- [ ] **P2.B.2 `lqv/typologies/dormitory.py`** — 6–10 bed for staff-courses + youth groups. Owner: AI. Effort: 1 day.
- [ ] **P2.B.3 `lqv/typologies/clay_terracotta_family.py`** — brick/clay-plaster family variant on §3.15 estate footprint. Closes the EUROPEAN_TOURISM_SPEC §3.12/§3.13 partial-coverage gap. Owner: AI. Effort: 1.5 days.
- [ ] **P2.B.4 `lqv/typologies/staff_housing.py`** — 2–4 unit cluster, lower spec. Owner: AI. Effort: 1 day.

### P2.C — Site infrastructure (renderable)
- [ ] **P2.C.1 `lqv/site/parking_arrival_court.py`** — hard-surface envelope + bus drop-off. Owner: AI. Effort: 0.5 day.
- [ ] **P2.C.2 Phase-2 master scene** — assemble P2.A + P2.B + P2.C into a `lqv/subscene/phase2_overview.py` aerial. Owner: AI. Effort: 0.5 day.
- [ ] **P2.C.3 Phase-2 BoQ rollup** — `make boq SCOPE=phase2`, regen rollup PDF. Owner: AI.

---

## P3 — Phase 3 hospitality + cultural anchors (year 2+)

Per `docs/wesley_phase3_inventory.md` Phase 3.

### P3.A — European-Dutch restaurant cluster
- [ ] **P3.A.1 `lqv/amenities/restaurant_indoor.py`** — multi-zone dining hall. Wesley priority.
- [ ] **P3.A.2 `lqv/amenities/bar_wine_cellar.py`** — earthen-floor cellar under dining room. Interior subscene mandatory.
- [ ] **P3.A.3 `lqv/amenities/cafe_panaderia.py`** — daytime trade, German-supply-chain hook.
- [ ] **P3.A.4 `lqv/amenities/cooking_school.py`** — shares kitchen fabric with P3.A.1.

### P3.B — Wellness + ritual
- [ ] **P3.B.1 `lqv/amenities/sauna.py`** — extract from `eco_retreat_modern_oasis` into standalone module.
- [ ] **P3.B.2 `lqv/amenities/yoga_deck.py`** — same extraction pattern.
- [ ] **P3.B.3 `lqv/amenities/massage_wellness.py`** — indoor envelope on wellness deck.
- [ ] **P3.B.4 `lqv/amenities/chapel.py`** — ~40 m² earthen-wall, wedding venue.

### P3.C — Cultural
- [ ] **P3.C.1 `lqv/amenities/visitor_center.py`** — could fold reception, decide after Wesley input.
- [ ] **P3.C.2 `lqv/amenities/performance_venue.py`** — open-air amphitheater near stream. Site-scale.
- [ ] **P3.C.3 `lqv/amenities/artisan_workshop.py`** — pottery/weaving shed.
- [ ] **P3.C.4 `lqv/amenities/gallery.py`** — adjacent to visitor center.

---

## P4 — Phase 4 outdoor + supply chain (year 3+)

Per `docs/wesley_phase3_inventory.md` Phase 4.

### P4.A — Supply-chain (renderable)
- [ ] **P4.A.1 `lqv/amenities/greenhouse.py`** — restaurant supply anchor.
- [ ] **P4.A.2 `lqv/site/veg_garden.py`** — promote from scatter to dedicated module.
- [ ] **P4.A.3 `lqv/site/fruit_orchard.py`** — orchard-row arrangement.
- [ ] **P4.A.4 `lqv/site/fish_pond.py`** — share fabric with `floating_dining` waterline.

### P4.B — Smallholder envelopes
- [ ] **P4.B.1 `lqv/amenities/herb_spiral.py`**
- [ ] **P4.B.2 `lqv/amenities/beekeeping.py`** — hive cluster, low priority.
- [ ] **P4.B.3 `lqv/amenities/chicken_coop.py`**
- [ ] **P4.B.4 `lqv/site/cattle_paddock.py`** — fencing + windbreak.

### P4.C — Education + commerce envelopes
- [ ] **P4.C.1 `lqv/amenities/permaculture_classroom.py`** — outdoor classroom + shaded deck.
- [ ] **P4.C.2 `lqv/amenities/library_herbarium.py`** — could fold into visitor-center.
- [ ] **P4.C.3 `lqv/amenities/small_shop.py`** — reception cluster.
- [ ] **P4.C.4 `lqv/amenities/coworking.py`** — remote-worker stays (EUROPEAN_TOURISM_SPEC angle).

---

## CC-TOOL — Cross-cutting tooling + infra

- [x] **CC-TOOL.1 MCP socket revival** — closed 2026-06-26 as **resolved-by-retire** per `docs/MCP_STATUS.md`. Socket stays down for escritura phase; revival recipe documented for post-escritura selective use. `scripts/mcp_daemon.py` exclude rule preserved.
- [x] **CC-TOOL.2 `scripts/organize_sub_renders.py`** — SHIPPED. Tracked since `db4831a` (note "currently untracked" was stale). Idempotent symlink-tree builder: reads flat `renders/sub/*.png` → `renders/sub_by_category/<cat>/<group>/<asset>/<variant>.png`. Taxonomy covers all 106 current sub-renders (0 skipped). Wired into Makefile as `make organize`.
- [x] **CC-TOOL.3 `scripts/download_polyhaven_assets.py`** — resolved at `5958124` (P1.A.5 HDRI dispatcher swap to cerrado / Atlantic-Forest-edge biome). Working tree clean as of 2026-06-26; no orphan `[M]` state remains.
- [x] **CC-TOOL.4 Smoke test broadening** — SHIPPED 2026-06-26. `scripts/smoke_test.sh` now appends a randomized N-driver subscene sample (default 4) after the composite + `ten_rules_check` pass; each driver runs headless with `RENDER_SKIP=1` so `save_subrender` short-circuits before sample burn. Exclude list keeps the 4 `base.run`-bypassing drivers (`terrain_62ha`, `terrain_62ha_photoreal`, `hdri_dusk_compare`, `material_wall_compare`) + `base`/`__init__`/`services` infra modules out. Knobs: `LQV_SMOKE_SUBSCENE_SAMPLE=0` opts out; `LQV_SMOKE_SUBSCENE_N=<n>` overrides sample size. Validated: single driver runs in ~4s on CPU fallback, so 4-driver sample adds ~16s to smoke.
- [x] **CC-TOOL.5 CI green-floor** — closed 2026-06-26. 10 actionable diagnostics fixed across 6 files (dead-expression deletions in 4 typology/amenity/subscene modules; defensive init in `fetch_copernicus_lcover.py`; loader narrowing in `stamp_license_stubs.py`). `pyrightconfig.json` now sets `reportMissingImports=none` to silence ~100 bpy/mathutils/bmesh stub-gap noise; cascade rules (reportAttributeAccessIssue/Index/Operator/Call) stay default so they still catch real bugs in numpy/matplotlib/rasterio/h5py. Residual 101 errors are all cascade hits from bpy's missing upstream stubs (4 legit non-bpy follow-ups logged to `DEFERRED_BUGS.md`).
- [x] **CC-TOOL.6 Render-run garbage collection** — SHIPPED at `db4831a`. `scripts/gc_render_runs.py` groups runs by asset key, keeps N most recent (default 3) per asset, protects tags (escritura/wesley_bundle/v_final/_legacy/review_2026-06-), 14-day mtime cutoff. Dry-run default. Wired into Makefile as `make gc`. Current state (2026-06-26): 312 folders / 2.4 GiB, 0 deletable (all within 14-day window — expected).
- [x] **CC-TOOL.7 BoQ scope expansion** — SHIPPED 2026-06-26. `lqv/boq.py` now honours `LQV_BOQ_SCOPE=phase1|phase2|phase3|phase4` in addition to existing `escritura` (default) + `full`. `_PHASE_MODULES` dict near `_POST_FREEZE_MODULES` is the editable surface — drop new typology/amenity shortnames into `phase3`/`phase4` as drops ship. Unknown scope values now raise `ValueError` instead of silently degrading to "no filter". Validated end-to-end: `escritura`→$268,685.45 (deck-pinned, 17 mods), `phase1`→$268,685.45 (== escritura, pre-freeze baseline), `phase2`→$19,371.30 (5 post-freeze mods), `phase3`/`phase4`→$0 (empty placeholders), `full`→$288,056.75 (== phase1 + phase2 sum). Default scope unchanged so notary deck reproduction is preserved.
- [x] **CC-TOOL.8 Deterministic render harness** — SHIPPED 2026-06-26. `lqv/provenance.py` is the new module: `collect(asset, variant, view, seed, extra)` returns a metadata dict (asset/variant/view/seed/config_seed/git_sha + every set `LQV_*` / `RENDER_*` env in `_TRACKED_ENV`); `inject_into_png(path, data)` writes raw `lqv:<key>` `tEXt` chunks immediately before IEND so the 16-bit Cycles output is preserved bit-for-bit (Pillow re-encode would force 8-bit and trash colour fidelity); `write_sidecar` drops a matching `<stem>.json` for grep-friendly catalogue walks; `read_from_png` + `python3 -m lqv.provenance <png>` round-trip the data back out. `lqv/subscene/base.py:save_subrender` calls all three after `render.run(scene)` and before the latest/ + legacy mirrors (so every copy carries provenance); injection is wrapped in `try/except` so a metadata bug can never invalidate a multi-minute render. Git SHA emits `<short>-dirty` when the worktree has uncommitted edits — keeps "tagged-commit render" vs "WIP-tree render" honest. `make provenance PNG=path/to.png` dumps the chunks; validated on a 1280×720 16-bit `agave_front_A.png` (dims + bit depth preserved post-injection, all 7 keys readable). `scripts/smoke_test.sh` green with the new import.
- [ ] **CC-TOOL.9 Asset license attribution sweep** — periodic `tools/check_licenses.py` to ensure every `LICENSES/*.txt` matches an asset still in use. Effort: 0.5 day.

---

## CC-DOC — Cross-cutting documentation

- [x] **CC-DOC.1 README.md refresh** — current state post-escritura. Owner: AI. Effort: 1 h. *Closed 2026-06-26 — top-level `README.md` did not exist (only `LICENSES/README.md` + `.pytest_cache/README.md`); created from scratch as cold-start entry covering parcel/ownership/escritura date, 4-deliverable priority table, doc-pointer order, quick-run examples, variant+HDRI map, host constraints, license split, GitHub remote. See CHANGELOG.md [2026-06-26] CC-DOC.1.*
- [ ] **CC-DOC.2 `docs/FINAL_GALLERY.md`** — regenerate post-P1.B and P1.C with new SHAs.
- [ ] **CC-DOC.3 `docs/RESULTS_GUIDE.md`** — section on multi-view shotlist + how to read `<asset>_<variant>_<view>.png` filenames.
- [x] **CC-DOC.4 `docs/sub_render_strategy.md`** — closed 2026-06-26. New §3.5 "Camera-view axis (`RENDER_VIEW`)" inserted between §3 and §4 with 6 subsections: default+dispatcher, value set, bypass-pattern drivers (22 migrated), interior furnishing (P1.B.1), xray override v2 (P1.B.3), output filename pattern (run-folder + flat back-compat). Template line 90 swapped to `cameras.make_view_camera(...)`. Cross-references updated.
- [x] **CC-DOC.5 `docs/master_plan.md`** — closed 2026-06-26. Date refresh 2026-06-10→2026-06-26; 12/12→18/18 finals at `85e86aa`; HDRI/CPU/14 GB blocks refreshed; new §1.1 cross-deliverable manifest; hard-gap status flipped (Variant C SHIPPED 2026-06-10, CREDITS.md SHIPPED, MCP RETIRED, CC-BY-SA hammock EXCLUDED). Phase 7 STARTING NOW → DELIVERED 2026-06-10.
- [ ] **CC-DOC.6 `docs/render_catalogue/INDEX.md`** — restructure by `(asset, view, variant)` not just `(asset, variant)`.
- [ ] **CC-DOC.7 `docs/photographic_references.md`** — add multi-view reference photos from comparable Paraguayan + Atlantic-Forest projects.
- [ ] **CC-DOC.8 Internal changelog** — `docs/CHANGELOG.md` tracking material-shader version (Bug 1/2 fix), camera-helper version, build_scene.py freeze status.
- [x] **CC-DOC.9 `docs/CLAUDE.md` reconciliation** — closed 2026-06-26. Task description's `docs/CLAUDE.md` is a phantom file — the in-repo CLAUDE.md lives at the repo root. The sub-render-first rule already lives there at §"Critique-derived standing rules" #1; no further promotion needed.

---

## CC-SALES — Wesley-facing + buyer materials

- [ ] **CC-SALES.1 Phase-2 sales deck** — post-P1 + P2.A done; 12-page pitch with new multi-view imagery. ~July 2026.
- [ ] **CC-SALES.2 Per-typology one-pager** — 16 PDFs, A4, each showing the 6 best views of one typology + spec + BoQ excerpt. Generates from `render_catalogue` + `boq` programmatically.
- [ ] **CC-SALES.3 European-buyer EN/DE deck** — translated variant of P0 deck for the Dutch-restaurant + remote-worker angle.
- [ ] **CC-SALES.4 Interactive web showcase** — static-site export under `paragu-ai.com/s/lqv` showing the contact-sheet grid. Lower priority. Effort: 2 days.
- [ ] **CC-SALES.5 Investor data room** — Drive/Notion structured copy of all Wesley deliverables for cross-checking by external due-diligence. Owner: Ivan.
- [ ] **CC-SALES.6 Video walkthrough** — 90-second flythrough using existing 18 composite finals + new multi-view. Tool: ffmpeg + ken-burns pan. Effort: 0.5 day.

---

## CC-BUILD — Real-construction track (eventual)

Out-of-scope for immediate render delivery, in-scope as project context.

- [ ] **CC-BUILD.1 Permit-ready set** — cardinal elevations + plan + section from P1.B feed into municipal permit packet for Phase 1 (signature villa + cob_bottle).
- [ ] **CC-BUILD.2 Site survey ground-truth** — schedule cm-accurate GNSS sweep of the 62 ha parcel; reconcile with the COP30 DEM. Currently using 30 m/pixel proxy. Owner: Ivan + surveyor.
- [ ] **CC-BUILD.3 Soil bearing-capacity test** — for stone-plinth foundation depth confirmation. Owner: Ivan + civil eng.
- [ ] **CC-BUILD.4 Micro-hydro feasibility study** — confirm 200–400 W continuous from the existing weir. Pelton head map says yes; needs in-person flow measurement. Owner: Ivan + hydraulic eng.
- [ ] **CC-BUILD.5 Bottle supply chain** — source ~3,000 wine bottles for cob_bottle wall. Local recycling co-op. Owner: Ivan.
- [ ] **CC-BUILD.6 Cob test panel** — 1 m² panel from local laterite + sand + straw, weather it 90 days before committing to mix ratio. Owner: Ivan.
- [ ] **CC-BUILD.7 ANDE grid intertie discussion** — net-metering or off-grid? Affects PV sizing. Owner: Ivan.
- [ ] **CC-BUILD.8 Mosquito vector audit** — Rule 10 compliance; cistern mesh spec finalized after entomologist consult. Owner: Ivan.

---

## Sequencing — what to do in what order

```
Now → 2026-06-27   : P0a (escritura prep)        [FROZEN renderer]
2026-06-27         : P0a.3 (sign at Peña)
2026-06-27 PM      : P0b.1 (debrief stub)
2026-06-28         : P0b.2 (full debrief, lift freeze)
2026-06-29 → 07-04 : P1.A (3 bugs + plinth + HDRI)
2026-07-05 → 07-12 : P1.B (multi-view imagery, 384 finals)
2026-07-13 → 07-18 : P1.C (composite refresh + FINAL_GALLERY)
2026-07-19 → 09-30 : P2.A + P2.B + P2.C (event hall + lodging fill)
2026-Q4 → 2027-Q2  : P3 (hospitality cluster)
2027-Q3+           : P4 (outdoor + supply chain)
Continuous         : CC-TOOL.1–9, CC-DOC.1–9, CC-SALES.1–6, CC-BUILD.1–8
```

## Hard dependencies graph

```
P0a → P0b → freeze-lift
              ├─→ P1.A.1 (water) → P1.A.5 (HDRI search can parallel)
              ├─→ P1.A.2 (lapacho) ─┐
              ├─→ P1.A.3 (flora LOD)│
              └─→ P1.A.4 (plinth)   │
                                    └→ P1.B.1 (furniture stubs) → P1.B.2 (camera helpers) → P1.B.3 (xray) → P1.B.4 (drivers) → P1.B.5 (preview) → P1.B.6 (fix) → P1.B.7 (finals) → P1.B.8 (catalogue)
                                                                                                                                                                              └→ P1.C → P2 typologies
```

## Risk register (top 6 only)

| # | Risk | Mitigation |
|---|---|---|
| 1 | Escritura delayed beyond 2026-06-27 | Bundle SHA-pinned; deck/bundle valid against any signing date. CONTINGENCIES.md C1–C6. |
| 2 | DEFERRED_BUGS 1+2 expose more failures when multi-view ships | Order is correct: bugs first, then multi-view. Don't render 384 PNGs on broken materials. |
| 3 | Furniture stubs look childish in interior shots | Time-box at 6 h; if quality is unacceptable, defer interior shots to a later sprint and ship the 8 non-interior views first. |
| 4 | Phase 2 typologies churn Wesley's expectations | One PR per typology; sub-render-first means each can be evaluated solo before assembly. |
| 5 | Host OOMs on a sub-render batch | Memory ceiling per `feedback_render_parallelism`; serialized only. Add per-process RSS log to harness as CC-TOOL.8 side-effect. |
| 6 | Tooling debt (`mcp_daemon` dead, untracked scripts) growing | CC-TOOL.1 + CC-TOOL.2 within first 2 weeks post-escritura. |

## What this TODO is NOT

- A schedule for Wesley to approve. P2/P3/P4 dates assume his go-ahead per phase.
- A commitment to model every catalogue item. Catalogue §5 lists Practical + Outdoor-adventure items explicitly **out-of-scope for visualization** (`maintenance shed`, `laundry`, `helipad`, `hiking trails`, `zip-line`, etc.). They live in operations plans, not in `lqv/`.
- A replacement for `docs/master_plan.md` (overall project) or `docs/housing_park_phasing.md` (Wesley-facing). Those are buyer/operator-facing; this is the engineering-side execution view.

## How to update this doc

- Tick boxes inline, no separate "DONE.md".
- When an entire P-block is done, replace the items with a single line: `**Completed YYYY-MM-DD at <commit>**`.
- New tracks → append a new top-level section, never reorder existing IDs (referenced from commit messages, PR descriptions, and memory).
- After every P-block completion: refresh `MEMORY.md` with a `project_state_YYYY_MM_DD.md` pointer.
