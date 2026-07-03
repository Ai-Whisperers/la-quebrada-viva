# Repo updates — patch plan to merge audio findings

> Generated from in-depth analysis of 5 audios (2026-06-30 14:52-16:22).
> Each section: file → where → what to add/change → source idea(s).
> Apply these patches in order; each is additive and preserves history.

---

## 1. STATUS.md

**Where**: §3 Tier-1 priority block + §9 Cross-references.

**Add**: New "2026-06-30 audio synthesis" subsection in §3 with the
6 P0 items from ACTIONLIST.

**Patch**:
```diff
+ ### 2026-06-30 audio synthesis (post-escritura)
+ - [ ] Push 8 unpushed commits (turboscribe manifest, 4 transcripts, 2 README/synthesis)
+ - [ ] Sonja questionnaire (cultural routing — salary/contract/price)
+ - [ ] 15-onderwerpen materials list → Wes picks 5
+ - [ ] 2 question finalization (name + 5 picks) — audio-friendly
+ - [ ] Update HOUSING_PARK_CONCEPT.md with D1-D14 content
+ - [ ] Update RESEARCH_GAPS.md with R39+ items
```

**Source**: ACTIONLIST P0.1-P0.6.

---

## 2. HOUSING_PARK_CONCEPT.md

**Where**: §0, §1, §2 (new §2.10), §3 (wellness/family add), §6.6
(infrastructure), §6.7 (Sonja-route workers), §6.8 (auto research).

### §0 Context — what changed (line 8-14)

**Add** to end of §0:
```markdown
### 2026-06-30 update (post-escritura)

The escritura signed 2026-06-27. Three days later (2026-06-30),
Wes recorded 5 audio messages totaling ~3h 27m of brainstorm content.
Synthesis is in `docs/audios/2026-06-30-wes-post-escritura/final/`:

- `DREAMLIST_NL.md` — 15 idea-domains (NL, for Wes)
- `ACTIONLIST_ES_EN.md` — 28 prioritized items P0-P4 (ES/EN, for Ivan)
- `IDEAS_LOG.md` — 95 numbered ideas with bucket tags (V/A/S/F)
- `KEY_POINTS.md` — top-20 high-signal bullets
- `REPO_UPDATES.md` — this patch plan

Werknaam: **Riverstone Valley** (not final). Wes's voorkeur:
"mooi Spaans" projectnamen. Horizon: **2030** (Sonia's 60e verjaardag (2030)).
```

### §2 Concept models — add §2.10

**Add** after §2.9 Hybrid:
```markdown
### 2.10 Forest park + family-anchored community (Wes's 2026-06-30 pick)

Forest-park wellness retreat with multiple experience types: wellness
pool (natural water, no chlorine, rain-fed), wedding/ceremony venue,
birthday/family celebration spaces. Family-anchored community component
(1-2 children at home per family, others work in park) — explicitly
NOT Dutch corporate daycare model.

- **Best for**: European wellness travelers + Asunción elite weekend +
  wedding/event market + family multi-gen gatherings
- **Why it fits**: matches Wes's 4-BV + machinepark operational model;
  serves 2030 horizon
- **Watch**: insurance for high-value outdoor amenities; multi-BV
  admin overhead; Sonja-routed labor sourcing for 6-8 fase-1 medewerkers
```

### §3 Core components — add wellness + family

**Add** to §3 component table:
```markdown
| Wellness pool (natural, rain-fed) | Eco-pool / bio-pool, geen chloor; Wes's signature element |
| Wedding / ceremony venue | Multi-experience thesis: ceremonies + family celebrations |
| Family-anchored housing | Permanent bewoning voor park-medewerkers + gezinnen |
```

### §4 Restaurant — refine

**Add** after §4.7:
```markdown
### 4.8 Initial price baseline (offline, Audio 3 2026-06-30)

Wes already has concrete material prices from the post-escritura session:

- Rivierzand (gewassen): 8,70 euro/kuub, "afgeleverd station"
- Rode breuksteen: 5,3 per ton (or 17 euro/ton full vracht)
- Vracht 10 ton: 170 euro

**Sonja krijgt always beter prijs** (Wes's own words, Audio 3). For all
restaurant supply chain, route through Sonja first.
```

### §6.3 Cultural — add wes-specific

**Add** after line 270:
```markdown
- **Wes's own Spanish**: dyslexic, prefers audio over writing.
  Audio-only questionnaires are the right format. Schrijven slecht,
  spreken goed.
```

### §6.6 Tourism — add railroad

**Add** after §6.6:
```markdown
### 6.6.1 Infrastructure tailwind: Ipoh-Karai railroad (Audio E)

Wes mentioned the historic Ipoh-Karai railroad line. There are
rumors of reopening plans ("the railroad that used to go through that
whole valley"). If it happens, Escobar becomes much more reachable
for Asunción weekenders + European tourists.

**Research needed**: Ipoh-Karai plan status. Sub-topic R40 in
RESEARCH_GAPS.md.

Wes also sees suburbanisatie trend (people moving outwards,
"Eskenbach is empty, the houses are empty, but that is all an
opportunity"). Track this for Phase 2+ timing.
```

### §6.7 Staff/labor — Sonja-route + hovenier

**Add** after §6.7:
```markdown
### 6.7.1 Sonja as canonical for cultural/worker/price questions

Per Wes Rule 5 (sonia-assistant): salary bands, contract types,
"hoe om te gaan met lokale medewerkers" — **route via Sonja, not
Google**. Wes's own confirmation: "Met Sonja krijg je altijd een
beter prijs" (Audio 3).

### 6.7.2 Hovenier deep-research (Wes's explicit AI delegation)

Wes's first explicit task handoff to AI Whisperers (Audio D):
> "Die hovenier, doen we goed een diepe research ernaar. Dat u dit
> voor de AI-jongheid kunt doen. Wat is er mogelijk, wat hebben ze?"

Sources to investigate: College van Ingenieurs Forestales PY, Guyra
Paraguay, Kuikopee Nederlandse forester (Wes named but didn't give
contact), Universiteit ecologie afdeling. R39 in RESEARCH_GAPS.
```

### §6.8 Construction — auto research + Ipakari

**Add** after §6.8:
```markdown
### 6.8.1 Auto voor de bouwfase (Toyota Tundra vs Presio)

Wes is researching Toyota Tundra vs Presio for PY dirt roads (Audio E).
Hermes has already done initial web searches. AI-haggling precedent:
"$4,000 off car market value" via AI-mediated negotiation.

Use this same AI-research pattern for Phase 1 construction supplies.

### 6.8.2 Steengroeve Ipakari (mogelijke lokale bron)

Wes mentioned a quarry/mine ("een mijn") close to Ipakari — likely a
local stone source for fase 1. Worth investigating for hardhout/
breuksteen supply.
```

### §8 Open questions — close several

**Remove or mark as answered**:
- Q1 "personal estate vs commercial" → **answered: commercial multi-experience**
- Q11-13 (restaurant format/cuisine/capacity) → deferred but wellness+weddings added
- Q17 (naming) → **partial answer: Riverstone Valley (working), Wes exploring Spanish alternatives**

**Add** new questions:
```markdown
### Audio-sourced (2026-06-30)

26. **Riverstone Valley: keep as project name, or switch to Villa del
    Cielo / Lluvia Dorada / Cielo Azul / "mooi Spaans" alternative?**
    (Wes is open to switching — wait for his pick.)

27. **5-of-15 materials onderzoek**: which 5 of the
    structureel-hout / cob / roofing / cement / ramen / solar / water /
    septic / bevestiging / vloeren / verf / elektrisch / loodgieterij /
    isolatie / keuken topics to research first?

28. **Hovenier contact in Kuikopee**: do you have the naam of the
    Nederlandse forester, or should I find them via Dutch-community
    channels in PY?

29. **Toyota Tundra vs Presio**: car for the bouwfase — finalize
    pick or keep researching? Existing AI research has price ranges.

30. **Railroad Ipoh-Karai status**: do you want me to research the
    reopening plans, or do you have a local contact who knows?

31. **2030 fase-target**: with Sonia's 60e (2030) as horizon, which fase do
    you want to have visible by then — Fase 1 (utilities + staff)?
    Fase 2 (restaurant + lodging + pool)? Or both?
```

### §11 The single most important question

**Replace** with:
```markdown
## 11. The single most important question (post-escritura, 2026-06-30)

If Wesley only answers one question from §8, the most valuable now is:

> **Werknaam: hou je aan "Riverstone Valley" of kies je een van de
> Spaanse alternatieven? (Villa del Cielo, Cielo Azul, Lluvia Dorada,
> Lluvia de Oro) Of iets anders?**

The name decision is the foundation for: URL, brand voice, marketing
copy, employee/business cards, the website, the brochures. It blocks
5+ downstream artifacts. Answer in audio (don't write).
```

---

## 3. RESEARCH_GAPS.md

**Add new items** to Tier 1 (most are P1 priorities):

```markdown
| R39 | **Hovenier deep-research** — College Ingenieurs Forestales PY, Guyra Paraguay, Kuikopee Dutch forester, universiteit ecologie. Wes's expliciete delegatie "AI-jongheid". | Phase 1 landscaping, native reforestation, terrain beautification | Local arborist directories, Dutch-community PY channels | 2 weeks | H + A | 🔴 | From Audio D 2026-06-30 |
| R40 | **Ipoh-Karai railroad plan status** — historic line, reopening rumors. Wes sees suburbanisatie trend as Phase 2+ tailwind. | Phase 2+ timing, accessibility | ANDE / Ferrocarril del PY, local news | 1 week | A | 🔴 | From Audio E 2026-06-30 |
| R41 | **Toyota Tundra vs Presio PY** — for fase-1 bouwfase auto | Phase 1 mobility cost | Existing AI research, PY dealer quotes | 1 week | A | 🔴 | From Audio E 2026-06-30 |
| R42-R46 | **5-of-15 materials research** — placeholder slots, dependent on Wes's P0.3 picks. D5.1-D5.15 candidates. | Phase 1 capex reality | Supplier quotes, online catalogs | 1-2 weeks each | A | 🔴 | Pending Wes's pick (P0.3) |
| R47 | **Sonja-routed salary bands + contracts** — voor 6-8 fase-1 medewerkers (boer, elektriciëns, hovenier, timmermannen, metselaars, betonwerkers) + IPS/aguinaldo/vacaciones PY | Phase 1 hiring cost | Sonja (canonical, Wes Rule 5) | 1 week | I | 🔴 | From Audio D + C, 2026-06-30 |
| R48 | **Cementprijs-over-tijd PY** — tijdreeks 2010-2026 voor budget realism | Phase 1+ capex realism | SENACSA, ABC Color archives, BCP | 1 week | A | 🔴 | From Audio C 2026-06-30, Wes's expliciete vraag |
| R49 | **Steengroeve Ipakari** — lokale bron voor bouwmaterialen | Phase 1 supply chain | Local directories, ANDE contacts | 1 week | H + A | 🔴 | From Audio C 2026-06-30 |
| R50 | **AI-as-price-negotiator voor vendor relations** — $4,000 off car precedent. Apply to PY material sourcing. | Phase 1+ cost reduction | Build on existing AI tooling | 2 weeks | I + A | 🔴 | From Audio E 2026-06-30 |
```

---

## 4. wesley_brief_onepager.md

**Where**: full rewrite — the current draft is pre-escritura (line 3 says
"DRAFT one-pager for the 27 Jun escritura signing"). Post-escritura, the
one-pager needs to be **the actual post-escritura brief**.

**Patch**: Update opening line, then merge in 4-BV + Riverstone Valley
+ 2030 horizon + family-anchored model. Replace "DRAFT" with v2.0.

---

## 5. EUROPEAN_TOURISM_SPEC.md

**Add** to the open questions section:
```markdown
### 2026-06-30 update

Wes confirmed (Audio E): the project is **not exclusively European** —
Asunción weekend market + wedding market + family celebrations + wellness
travelers all in scope. European tourism is a major vector but not the
sole thesis. Update §16-19 accordingly.
```

---

## 6. CLAUDE.md

**Add** to Document map:
```markdown
- `docs/audios/2026-06-30-wes-post-escritura/final/` — post-escritura
  audio synthesis (DREAMLIST_NL, ACTIONLIST_ES_EN, IDEAS_LOG,
  KEY_POINTS, REPO_UPDATES). Read alongside HOUSING_PARK_CONCEPT.md.
- `docs/audios/2026-06-30-wes-post-escritura/drafts/` — raw transcripts
  per audio (5 audios, ~28k words).
```

---

## 7. SESSION_LOG.md

**Add** tick for 2026-06-30:
```markdown
### Tick 2026-06-30 — post-escritura audio synthesis

- 5 audios received from Wesley (14:52-16:22, 3h 27m, ~28k words)
- Local faster-whisper large-v3 int8 CPU transcription pipeline
  (5 jobs parallel, completed overnight)
- Turboscribe bundle prepared (95.7 MB mp3, 3h 19m, chronological
  with silence gaps)
- Wes Rule 6 protocol applied: 3-file split (raw/dream/action),
  V/A/S/F bucketing (24V/35A/23S/11F + 8 cross-team contacts)
- Final docs: DREAMLIST_NL, ACTIONLIST_ES_EN, IDEAS_LOG,
  KEY_POINTS, REPO_UPDATES
- 5 unpushed commits (pending GH token)

Key new content vs pre-escritura:
- Riverstone Valley werknaam
- 4-BV + machinepark structuur
- Forest park + wellness pool + family-anchored community model
- Hovenier first explicit AI delegation
- Sonja canonical for cultural/worker/price
- Toyota Tundra/Presio + AI-haggling precedent
- Railroad Ipoh-Karai tailwind
- 2030 horizon = Sonia's 60e (2030)
```

---

## Order of operations

1. **Apply §1 (STATUS.md)** — single small add
2. **Apply §2 (HOUSING_PARK_CONCEPT.md)** — biggest patch, 7 sections
3. **Apply §3 (RESEARCH_GAPS.md)** — 8 new R-items
4. **Apply §4 (wesley_brief_onepager.md)** — full rewrite
5. **Apply §5 (EUROPEAN_TOURISM_SPEC.md)** — small clarification
6. **Apply §6 (CLAUDE.md)** — 2-line add to document map
7. **Apply §7 (SESSION_LOG.md)** — new tick
8. **Commit + push** (when GH token available)

Each patch is additive (no overwrites of pre-escritura content).
The pre-escritura 8-concept matrix in HOUSING_PARK_CONCEPT §2
remains — §2.10 just adds Wes's picked variant.