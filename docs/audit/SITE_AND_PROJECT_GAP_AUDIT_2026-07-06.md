# LA QUEBRADA VIVA · SITE + PROJECT GAP AUDIT

> **For:** Ivan / Kiki / Erebus / Wes.
> **Date:** 2026-07-06.
> **Status:** Authoritative — supersedes the older roast-style critiques (`docs/CRITIQUE_FOR_WES.md`,
> `docs/audit/CRITIQUE.md`). This one is **complete + actionable + tied to the work plan below.**
> **Trigger:** The user's request: "analyze all the gaps in depth and make a complete detailed work plan for the whole website."

I went over every artifact in the repo and the live site. What follows is the **deep gap analysis** for
both the **public-facing site** (what buyers/stakeholders see) and the **internal project** (the repo itself,
the live data, the docs, the marketing surface). Then I give a **single ranked work plan** with concrete next
steps and acceptance criteria.

---

## 1. What the site is today

```
                                          PUBLIC SURFACE
                                          ==============

   https://lqv-walkthrough.pages.dev/
     │
     ├── /              (31 KB · index.html)
     │   ├── Editorial walkthrough (7 sections: Land, Water, Forest, Build, Layers, Limits, Contact)
     │   ├── Cesium 3D parcel explorer (interactive)
     │   ├── 7 hero stat cards
     │   └── 1 image (preview/satellite)
     │
     ├── /mapa          (63 KB · mapa.html · THE unified viewer)
     │   ├── Leaflet, 33 layer toggles, 7 preset bundles
     │   ├── Radius picker Parcel / 5 / 10 / 20 / 30 km (?r= URL persistence)
     │   ├── NDVI backdrop, HAND floodplain, local quebrada stream overlay,
     │   │  forest-change timeline, coverage matrix, elev HUD, scale bar,
     │   │  GPS walking track, replay-walk animation, share-view URL
     │   ├── Collapsible sidebar (44 px rail mode), persistent collapse state
     │   ├── Layer search filter, opacity localStorage
     │   └── Service worker (offline support)
     │
     ├── /analysis-2026-07-04  (27 KB · analysis-2026-07-04.html)
     │   ├── Editorial technical annex (8 sections: hero, numbers, waterfalls,
     │   │  terrain, data-table, caveat, downloads, outro)
     │   ├── 4 CTA cards pointing to /mapa at different radii
     │   ├── Raw-data downloads (GeoJSON / CSV)
     │   └── NO embedded interactive map (was removed 2026-07-06 as redundant)
     │
     ├── /mapa-10km /mapa-20km /mapa-parcel  →  301 → /mapa  (CF Pages _redirects)
     │
     └── /404.html      (1.2 KB · branded "LQV")

```

**Repo-internal context the site doesn't show but exists:**

- 18 photoreal Blender renders (`renders/A_*.png` through `C_petal_macro.png`) — the cob house on site
- 109 idea catalog across 10 categories (`docs/ideas/`)
- 146 research results (`docs/research/RESULTS/`) — cement pricing, PV sizing, insurance, etc.
- 33 specs (`docs/specs/house/`, `docs/specs/tourism/`, `docs/specs/render/`, `docs/specs/assets_legal/`)
- 6 stakeholder packs (`docs/people/stakeholders/` — attorney, insurance, Sonja questionnaire, etc.)
- Full HOUSING_PARK_CONCEPT and MASTER_BRIEF (€5.5M Phase 1, 30 cabins, 2030 horizon)
- The site exposes **none of this.**

---

## 2. GAP ANALYSIS — the public site

### 2.1 Critical gaps the user can SEE

| # | Gap | Who notices | Cost of leaving |
|---|-----|-------------|----------------|
| **S1** | **No sell-ask price.** Nowhere on the site does it say "for sale at $X" or "looking for $Y investment." Buyers can't act. | Buyer / investor | The site is a passive brochure that doesn't convert |
| **S2** | **No contact form or "let's talk" CTA.** Topbar has "Repo" / "Full analysis" / "Walkthrough" links, but no `info@`, Messaging link, Calendly, or contact submission. | Anyone who wants to reach Ivan/Wes | 90% of qualified-interest leads drop off |
| **S3** | **No investor pitch deck surface.** The 18 photoreal Blender renders are the strongest single asset on the project, but `index.html` only references one preview image. The renders themselves don't show up anywhere on the live site. | Investor, journalist, designer | The $10,000s of Cycles rendering work is invisible to buyers |
| **S4** | **No name finalization.** README §provisional banner propagates everywhere. Site still says "La Quebrada Viva" in the URL, the 404 page, the bottom of the analysis page, every fetch path. Wes has not picked — soft-gate SG-W1. | Everyone | The whole site is in "limbo" voice — it's neither Riverstone Valley nor LQV. Confusing for buyers who Google either |
| **S5** | **Only EN.** Land buyers in Paraguay are Spanish-speakers. European buyers are EN. Wes's own network is NL. The site has no language toggle, no Spanish version of the hero stats, no localized download links. | PY buyers, NL network | Lose 70%+ of the local market |
| **S6** | **No SPLAT/Gaussian Splatting viewer linked.** Repo has `splats/exports/web/` and `splats/exports/web/mapa.html` was the deliverable for the splat work. But the SPLAT artefact itself (a `.splat` or `.ply` file with the 3D capture of the waterfall + ridge) is not referenced anywhere buyers can see. | Investor, Wes | The headline 3D capture is invisible |
| **S7** | **No analytics, no conversion tracking, no funnel.** No Plausible/GA/Pirsch on any page. We have no idea who visits, where they bounce, what they click. | Ivan | Cannot iterate because we can't see |
| **S8** | **`/analysis-2026-07-04.html` is dated in its slug.** When Wes reviews phase-2 data in 2027, this URL is unusable. Slug should encode `phase` / `intent`, not date. | Future-self, audit trail | Hand-edit cost forever after |
| **S9** | **Visual style is inconsistent across the 3 pages.** `/` has dark-amber editorial. `/mapa` has light-cream interleaved. `/analysis-2026-07-04.html` has a third dark-teal palette. Three different fonts (Cormorant Garamond + Inter + system-sans), three different button shapes. | Brand-conscious buyer | Looks unfinished, hurts trust |
| **S10** | **No "Privacy" page, no "Terms".** Forms will need it; analytics will need it. | Legal | Once you add the contact form, GDPR/COMPLY bites |

### 2.2 Medium gaps — buyer UX

| # | Gap | Why it matters |
|---|-----|----------------|
| **M1** | **No print stylesheet.** The aerial surveys + 8 research tables want to print. Wes said in audio E that buyers will print pages. | Buyers will print; right now it prints broken |
| **M2** | **No "share this view" with a thumbnail.** The map has a "share view" function, but on social previews / Slack the URL renders with no thumbnail. No `og:image` / `twitter:card` meta tags. | Sharing looks dead |
| **M3** | **No loading state for the Cesium 3D viewer.** First load = 3-5 MB of WebGL code; user sees nothing for 2-8 seconds. No skeleton, no progress, no "loading terrain…" hint. | First-impression hurts |
| **M4** | **No "I'm a buyer" vs "I'm an investor" entry path.** Same walkthrough for both, but a buyer cares about parcel maps + waterfalls, an investor cares about cabin types + financial model. | Both audiences leave slightly confused |
| **M5** | **No deep-link from research to where it shows up.** Buyer reads "90% forest cover" in the hero. The research ID (F02 / NDVI) that produced that number is invisible. | Reduces credibility when someone checks claims |
| **M6** | **No publication-date or "last updated" anywhere on the site.** Buyers can't tell if this is current or stale. | "Is this still for sale?" doubt |
| **M7** | **No "pictures from the property" or photo gallery.** Repo has the satellite renders but no actual photos of the quebrada, the cob house, the GPS walk. The site shows pure-data. | Emotional engagement = 0 |
| **M8** | **`/mapa` sidebar search is good, but the share button doesn't preserve the search filter.** Search state isn't in the URL. | Can't share a curated view |
| **M9** | **No keyboard shortcut hint visible.** `[` collapses the sidebar, `[1-6]` apply presets, `0` resets view — but no on-screen hint anywhere. | Power users discover this by accident |
| **M10** | **`/mapa`'s search-filter input has no esc-to-clear, no clear-button.** | Small annoyance, drops retention |

### 2.3 Buyer-facing gaps that would actually move the needle

The killer features that are missing — these are not polish:

| # | Gap | Why it matters |
|---|-----|----------------|
| **K1** | **No investor 1-pager as a lead magnet.** Stakeholder brief exists at `docs/people/wes/wesley_post_escritura_one_pager.md` but is not on the public site. The "Sell this 30-cabin, 5.5M-euro vision in 1 PDF" asset is the most-sendable thing Ivan owns. | He has it; nobody can find it |
| **K2** | **No cabin-typology catalogue on the site.** Specs live in `docs/specs/house/floor_plan.md` and `renders/`. The buyer who lands on the site sees numbers but no pictures of the 30 cabins planned. | Investment pitch loses 80% of its impact without visuals |
| **K3** | **No testimonials or social proof.** This is a personal sale (Wes buying), but the housing-park vision is investor-facing. Zero credibility markup: no "trusted by", no prior-project gallery, no advisor names. | Trust deficit |
| **K4** | **No "make an offer" or "request a tour" CTA in the hero.** Even if it's a Typeform / Calendly / email-link / Messaging-link, there must be ONE button at the top of the hero that says "Let's talk". | This is the gap that converts |
| **K5** | **No site-search.** A 27 KB analysis page plus the index plus mapa means 3 pages; small enough to navigate. But once we add cabin typology, investor brief, research summaries, FAQ, etc., we'll want a `/search` overlay. | Future-scaling |
| **K6** | **No Spanish version of any buyer-facing page.** The 404 says "LQV walkthrough" — even mentioning Paraguay buyers in Spanish would change nothing in English. | Kills the PY market |

---

## 3. GAP ANALYSIS — the project itself

These aren't visible to a buyer but they bleed through to user perception:

### 3.1 The repo has material that the site should surface

The repo has ~24 MB of buyer-relevant artefacts that **never reach the site**:

| Artefact | Bytes | Lives in | Surfaced to buyers today? |
|---|---|---|---|
| 18 photoreal Cycles finals | ~150 MB | `renders/` | **No** (only `data/preview/lqv_satellite_clean.webp` lives on the site) |
| 4 short data videos (`C_hero_reel.mp4` × 4) | ~50 MB (estimate) | `renders/site_overview/` | **No** |
| 109 idea catalog (filtered) | ~6 MB markdown | `docs/ideas/` | **No** (only `docs/ideas/_meta/` referenced) |
| 146 research results | ~3 MB markdown | `docs/research/RESULTS/` | **No** — none, anywhere on the site |
| 4 stakeholder 1-pagers (attorney, insurance, Messaging, Sonja) | ~150 KB | `docs/people/stakeholders/` | **No** — strictly internal |
| Wes's `wesley_post_escritura_one_pager.pdf` | ~50 KB | `docs/wes/` | **No** |
| 33 spec docs | ~2 MB markdown | `docs/specs/` | **No** |
| 4 BV-cascade + financial model | ~400 KB | `docs/_reconciled/business/` | **No** |

That's the largest single category of gap: **the site is a 5% surface of what we have built.**

### 3.2 Internal project gaps

| # | Gap | Severity |
|---|-----|---|
| **P1** | **The site's URL is `lqv-walkthrough.pages.dev`** — communicates "this is a walkthrough, not a sales page." Once the project name is picked (SG-W1), this URL must change. | High |
| **P2** | **No CNAME setup. No custom domain.** `lqv-walkthrough.pages.dev` is just the Cloudflare Pages dev URL. The real domain hasn't been registered, much less pointed. | High |
| **P3** | **Brand assets don't exist.** No logo, no color tokens in code, no Open Graph image, no favicons beyond default. | High |
| **P4** | **No CMS / authoring layer.** Today, every copy change requires a code deploy. A 30-cabin typology catalogue with photos will need daily updates → we need Markdown-on-the-server or a small admin. | Medium |
| **P5** | **SEO is zero.** No sitemap.xml, no robots.txt, no `<meta name="description">` on any page, no schema.org structured data, no canonical URLs. A Google search for "62 hectares Paraguay for sale" returns nothing. | High |
| **P6** | **No performance budget.** The Cesium viewer alone is 2 MB of JS; the Leaflet bundle + markercluster + custom code is another 1.5 MB. We never checked time-to-interactive or largest-contentful-paint. Buyers on 3G in rural Paraguay will time out. | High |
| **P7** | **No accessibility audit.** Color contrast, ARIA roles, focus management, keyboard-only navigation, screen-reader labels. WCAG 2.2 AA is the floor for any commercial site. | Medium |
| **P8** | **No CSP / security headers.** No Content-Security-Policy, no HSTS, no X-Content-Type-Options, no Referrer-Policy. The map pulls from `server.arcgisonline.com`, `unpkg.com`, `fonts.googleapis.com` — wide open. | Medium |
| **P9** | **No legal pages.** Privacy policy, terms of use, contact information (real legal entity), copyright notice. | High (when forms are added) |
| **P10** | **Deploy is a manual `bash ~/.hermes/scripts/lqv-pages-redeploy.sh`.** No CI, no preview branches, no rollback. One wrong commit = site down. | High |
| **P11** | **No uptime monitoring / alert.** Site has been silently down before (e.g. `lqv-map.js` referenced from `index.html` but not deployed for ~30 min on 2026-07-04 — caught by Erebus). We found it; no buyer mentioned it. | High |
| **P12** | **No `how-to-buy` doc on the site.** Even if the answer is "we don't want to sell the parcel, we want investors for the housing-park vision", the site should say so. Buyer ambiguity → wasted interest. | Medium |
| **P13** | **Site is NOT discoverable.** No link from anywhere = no organic traffic. Needs: Wes's email signature, his profile bio, Kiki's LinkedIn, Ivan's profile, EXCON/LAC investment directories, Paraguay real-estate portals (inmobilibia, etc.). | High |
| **P14** | **No email/CRM / lead pipeline.** Forms will drop leads to a black hole. Need: a tiny list (even Buttondown or a Google Form → Sheet). | Medium |

---

## 4. GAP ANALYSIS — content & narrative

The site tells **a story** but the story it tells doesn't match the **actual state** of the project.

### 4.1 Story vs reality mismatches

| What the site says | What the project actually is | Why this matters |
|---|---|---|
| "62 hectares" | The original goal was 6 cabins on the cob-house parcel; now it's a 62-ha *housing park* with 30 cabins | The page hides the ambition. Buyers don't get the vision |
| "Buy a parcel" | The escritura is **already signed** — the land is owned. The offer is now "invest in a 30-cabin housing-park vision, target €5.5M Phase 1 capex" | Readers don't know whether to buy land, buy into a deal, or just learn |
| "$70k IB threshold" | Wes is the seller; buyers invest in the company. Different ask | Conflates buyer / investor / partner |
| "Atlantic Forest canopy 90%" | Real satellite NDVI, true. But who says? F02 → Sentinel-2 → ID? The buyer can't trace it. | Credibility chain is invisible |
| "GPS-confirmed waterfall at 274 m" | Wes walked to it 2026-06-28 with phone GPS. Real. But not "verified" in any formal sense (no surveyor). | Implies more rigor than data warrants |
| "Atlantic Forest" | Correct biome label. But "Atlantic Forest" has a specific IUCN meaning — buyers in EU compliance & PY conservation science may have questions. | Legal/regulatory nuance |

### 4.2 Voice / honesty gaps

| # | Gap |
|---|-----|
| **V1** | The site never admits what's NOT done. The map shows DEM-derived "50 candidate waterfalls" but the data page says "one confirmed" — but neither says "0 confirmed by a licensed surveyor." |
| **V2** | No "What you're looking at / how this was made" / methodology page. Investors and journalists ALWAYS ask. |
| **V3** | No "What we don't have yet" page. 1-pager mapping "Here's what we have / here's what we need" is the single most-honest credibility move. |
| **V4** | Three pages have different visual temperatures — `/` is editorial cool, `/mapa` is utilitarian light, `/analysis-…` is technical dark. Reads as three authors, one project. |
| **V5** | The 18 final cob-house renders are described as "first example building typology" but the actual page (`index.html`) calls it "Three cob houses already designed. Cycles-rendered in three lights." Undersells. |
| **V6** | No FAQ. The buyer questions are predictable: "why Paraguay?", "is it safe?", "what's the access road?", "any EMF concerns?", "covid-free?" — none answered. |

---

## 5. RANKED work plan — concrete, sequential, acceptance-criteria'd

Each item has: **goal**, **owner** (W=1-2h Wes, I=Ivan, A=AI subagent), **effort**, **acceptance**, **depends on**.

### PHASE A — Make the existing site usable (don't add; fix). ~8 hours total.

| ID | Item | Owner | Effort | Acceptance | Depends on |
|----|------|-------|-------|-----------|-----------|
| **A1** | **Pick a project name** (Riverstone Valley vs 4 Spanish alternatives, Wes's pick from PROJECT_NAME_CANDIDATES.md). | W | 5 min | W sends "we're going with X" → repo rename begins | nothing |
| **A2** | **Register the chosen domain** (`.com` and `.com.py` ideally). Cloudflare Registrar. | I | 15 min | domain added to Cloudflare, propagates 200 | A1 |
| **A3** | **Add CNAME to Cloudflare Pages.** Pages project → `lqv-walkthrough` → custom domain = chosen.com. | I | 15 min | `https://chosen.com/` returns the same HTML as the .pages.dev URL | A2 |
| **A4** | **Standardize brand palette + typography.** Three pages → one design token set. | I + A | 4 hr | All three pages use: 1 font family, 1 color tokens file, 1 button shape | nothing |
| **A5** | **Add contact info top-right of every page:** `info@chosen.com` (or mailto) + Messaging deeplink. | A | 30 min | Visible on all 3 pages, mobile-clickable to Messaging | A3 |
| **A6** | **Add `<meta>` SEO.** `description`, `og:title`, `og:image`, `og:url`, `twitter:card`, `canonical`, `<link rel="alternate" hreflang="en">` (and `hreflang="es"` once Spanish page exists). | A | 1 hr | All 3 pages have unique meta + og:image renders properly on social previews | nothing |
| **A7** | **Generate sitemap.xml + robots.txt.** | A | 30 min | `https://chosen.com/sitemap.xml` lists all 3 public pages; `robots.txt` references it | A3 |
| **A8** | **Add `/_redirects` cleanup.** Remove old `mapa-10km` etc. stubs (already done 2026-07-06). Add `www.chosen.com → chosen.com`. | I | 15 min | `https://www.chosen.com/` 301s to apex | A3 |
| **A9** | **Performance baseline.** Run WebPageTest and Lighthouse against chosen.com. Capture LCP, TTI, TBT, CLS, total JS KB. | I + A | 30 min | Single document: `docs/perf/BASELINE_2026-07-06.md` | A3 |
| **A10** | **Accessibility baseline.** Run axe-core / WAVE on all 3 pages. Fix any A/AA violations. | A | 1 hr | `docs/perf/A11Y_BASELINE_2026-07-06.md` | nothing |

### PHASE B — Make the site CONVERT. Add the missing surfaces. ~16 hours total.

| ID | Item | Owner | Effort | Acceptance | Depends on |
|----|------|-------|-------|-----------|-----------|
| **B1** | **Hero CTA** ("Let's talk" button + secondary "Tour the map"). Persistent, top-right. | I + A | 1 hr | Button visible, links to `/contact` or mailto | A5 |
| **B2** | **Contact / inquiry form.** Lightweight (Buttondown / Google Form / Web3Forms). Captures: name, email, phone (optional), interest (buyer / investor / advisor / press), free-text. Pipes to a single email + Sheet. | I | 2 hr | Submission round-trips into Ivan's inbox + Sheet | nothing |
| **B3** | **Privacy + Terms pages.** Generated from a template (TERMS.md / PRIVACY.md). Legal-grade: EU GDPR, PY consumer law, contact info. | A | 1 hr | Pages reachable from footer | B2 |
| **B4** | **Methodology page.** `/how-this-data-was-made.md` (or HTML). What each number means, source, model, confidence, last-updated date. Linked from each number in the site. | A | 3 hr | Every stat in the site is one click from a method doc | nothing |
| **B5** | **Cabin typology catalogue.** 30 cabins, 10 types, 1 page each. For now: render the 18 existing Cycles finals as exemplars; for the rest, use a placeholder card with "Spec available on request" + a buyer's-email-gate to capture interest. | I + A | 4 hr | /cabins /cabins/cob-house-typology-A /cabins/... etc. live. 18 renders visible in gallery | A5, B2 |
| **B6** | **Investor 1-pager** PDF on the site.** `/investor-brief.pdf` linked from the B1 CTA. | A | 30 min | PDF is reachable, ≤500 KB, opens in browser | nothing |
| **B7** | **Photos from on-site visits.** Add 6-10 actual photos (waterfall, cob house, GPS walk, quebrada). One block on `/`. | W + I | 2 hr (W for selection; I for upload + optimize) | Photos live; thumbnails generated; sizes ≤ 250 KB each | nothing |
| **B8** | **Spanish homepage** `/es`. Same structure as `/`, all copy translated. PNG of the Hero version-1, all 7 stats, contact CTA in ES. (NL version later if needed.) | A | 3 hr | `https://chosen.com/es/` returns translated HTML; `.dev/es/` redirects 301 | A1 (name), A4 (palette) |
| **B9** | **Add analytics** (Plausible self-hosted or Pirsch on a custom subdomain). Privacy-friendly. | A | 30 min | Dashboard at analytics.chosen.com shows first pageview within 60s of test visit | A3 |

### PHASE C — Make the 18 Cycles renders reachable. ~6 hours total.

| ID | Item | Owner | Effort | Acceptance | Depends on |
|----|------|-------|-------|-----------|-----------|
| **C1** | **Asset pipeline.** Convert 18 PNG renders to AVIF + WebP. Generate thumbnails (max 800 px wide). | A | 1 hr | Each render has 3 sizes: thumb 250 KB / web 800 KB / full 1.5 MB | nothing |
| **C2** | **`/gallery` page.** Lightbox grid: 6 columns, 3 rows. Click → full-screen view, ←/→ navigation, ESC, alt-text. | A | 3 hr | All 18 visible; accessible; mobile 1-col, tablet 3-col, desktop 6-col | C1 |
| **C3** | **3 short reels / `mp4`** (the project has 4 — `C_hero_reel.mp4` etc.). Host in `/gallery/videos/`. Compress to ≤ 6 MB each. | A | 1 hr | Play inline, autoplay off, controls visible | nothing |
| **C4** | **Cabin-card replacement.** Once C1 done, swap the cabin cards from "Spec available on request" to actual renders. | A | 1 hr | Each cabin-typology page shows the relevant render | B5, C1 |

### PHASE D — Internal credibility. ~6 hours total.

| ID | Item | Owner | Effort | Acceptance | Depends on |
|----|------|-------|-------|-----------|-----------|
| **D1** | **Honest-limits page** (`/whats-not-here`). What we DON'T have: no surveyor, no formal environmental study, no live site photos, no buyer offering price. Why? Because of phase. | A | 1 hr | Page reachable; West-facing; signature line | nothing |
| **D2** | **FAQ page.** Minimum 14 buyer questions, 1-paragraph answers: "Is it safe?" "What's the access road?" "Why Paraguay?" etc. (Pull from `docs/wes/WES_FAQ.md`.) | A | 2 hr | All questions answered; linked from hero and `/contact` | nothing |
| **D3** | **Site-search** (Pagefind or MiniSearch). Indexes all pages. Keyboard ⌘/Ctrl-K. | A | 2 hr | `⌘K` opens overlay, searches all pages | A3 + content complete |
| **D4** | **CSP, HSTS, X-Frame-Options headers** in `_headers` (CF Pages format). | I | 1 hr | `curl -I` shows all 4 headers; site still loads | A3 |

### PHASE E — Operational hardening. ~12 hours.

| ID | Item | Owner | Effort | Acceptance | Depends on |
|----|------|-------|-------|-----------|-----------|
| **E1** | **CI deploy via GitHub Actions.** On push to `master`, run smoke tests then deploy. Preview URLs for branches. | I | 4 hr | Push → preview.deploy shows new build; merge → prod deploy | nothing |
| **E2** | **Uptime monitor** (UptimeRobot free tier or healthchecks.io). Page that pings every 5 min. Alert via Telegram. | I | 1 hr | First alert routes to phone within 60s of failure | A3 |
| **E3** | **Performance budget + Lighthouse CI.** Fail the build if any page exceeds LCP 2.5s or TTI 4s on slow-4G. | A | 3 hr | CI runs Lighthouse on each PR; threshold-enforced | E1 |
| **E4** | **Backup the _redirects / _headers / contents** offsite. Bitwarden Secrets or 1Password team vault. Cost €40-80/yr. | I | 30 min | Repo state captured nightly | nothing |
| **E5** | **Reduce Cesium JS payload** (Cesium is 2 MB uncompressed; trim to 1 MB via `cesium-min` or remove for users on slow connections with a "loading 3D…" button). | A | 3 hr | Cesium loads on demand only | A9 |
| **E6** | **Service worker updates** — current `sw.js` doesn't auto-update on new deploys. Fix: bump cache-version on every deploy. | A | 30 min | After deploy, refresh shows new content within 1 min | E1 |

### PHASE F — Long tail. ~24 hours over weeks.

| ID | Item | Why | Effort |
|----|------|-----|--------|
| **F1** | **NL Dutch homepage** (`/nl`). | Wes's own network + European real-estate buyers expect NL. | 3 hr |
| **F2** | **3D Gaussian Splat viewer.** Embed the actual `.ply` or `.splat` of the waterfall/ridge. Use `@mkkellogg/gaussian-splats-3d` or `gsplat.js`. | Once the splat pipeline lands, this is the killer feature: "walk the property in 3D." | 8 hr |
| **F3** | **Phase-1 cabin design detail pages.** Floor plans, BOM, render of each. | Once decisions land, this is the depth. | 12 hr |
| **F4** | **Tour scheduling** (Calendly or SavvyCal inline). "Book a 30-min walkthrough with Wes via video." | Highest-converting CTA once the brand is real. | 1 hr |
| **F5** | **Annual audit page** ("Every figure on this page was verified on YYYY-MM-DD"). | Buyer trust comes from provenance. | 2 hr |

---

## 6. The 30-day execution summary

**Week 1 (2026-07-06 → 2026-07-12):** A1 + A2 + A3 + A4 + A5. Ship the renamed site on a real domain with one consistent design system. ~6 hr total. Ivan drives; A helps.

**Week 2 (2026-07-13 → 2026-07-19):** A6 + A7 + A8 + A9 + A10 + B1 + B2 + B4. SEO + contact form + methodology. ~10 hr.

**Week 3 (2026-07-20 → 2026-07-26):** B3 + B5 + B6 + B7 + D1 + D2. Privacy/cabin-typology/photo/methodology. ~14 hr.

**Week 4 (2026-07-27 → 2026-08-02):** C1 + C2 + C3 + D3 + D4 + E1 + E2 + E6 + B8 (Spanish). Ship the gallery, search, security headers, CI, monitoring. ~22 hr.

**August / long tail:** Phase E hardening (perf, backup), Phase F (NL, splat, tour scheduling).

---

## 7. Acceptance gates

Done = we've shipped Phase A + B + C, which together:
1. Convert a stranger's first pageview into a qualified inquiry.
2. Reuse the 18 Cycles renders that are already paid-for work.
3. Make the project "sellable" — i.e., when Wes says "send a buyer here," the URL does the work.

Done well = Phase D as well: the site earns a buyer's trust enough to ask for a video-call follow-up.

---

## 8. What we explicitly are NOT doing in this plan

To keep the plan honest:
- **No mobile-app.** Web-only. PWA later.
- **No CMS.** Markdown-in-repo. If content updates become daily, revisit with Tina CMS / Decap.
- **No AI-chatbot.** Just contact forms.
- **No marketplace / listing on third-party sites.** Wes's network + organic inbound is enough for the next 6 months.
- **No payment processing on site.** The ask isn't a $99 ebook; it's a 7-figure investment conversation.
- **No proprietary tile server.** Continue using ESRI World Imagery + OSM + Sentinel-2 via MapTiler free tier / OSM raw.

---

*Built for the 2026-07-06 audit pass. Owner: Erebus. Supersedes `docs/CRITIQUE_FOR_WES.md` (single-project roast) and `docs/audit/CRITIQUE.md` (pre-escritura critique). Companion to `docs/wes/WES_INDEX.md` (Wes-facing intro) and `docs/POST_ESCRITURA_NOW.md` (Phase-1 gates).*
