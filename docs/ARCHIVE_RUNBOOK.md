# Archive Runbook — T+30 freeze

> What to freeze, what to archive, what to delete after the 2026-06-27 escritura signing. Fires on **2026-07-27** (T+30). Goal: stop carrying the closing-prep weight in working tree once the work is closed.

The principle: **freeze artifacts that proved the closing; archive context that explains them; delete only what is regenerable from code or fetchable upstream.**

---

## 1. Freeze (keep in repo, mark immutable)

These are the audit trail of the 2026-06-27 closing. Never edit, never regenerate.

| Artifact | Location | Why frozen |
|---|---|---|
| Bundle ZIP | `dist/print_pack_2026-06-27/wesley_bundle_20260616-1715.zip` | Distributed artifact, SHA pinned |
| Deck PDF | `dist/print_pack_2026-06-27/escritura_deck_v6.pdf` | Distributed artifact, SHA pinned |
| VERIFY.sh | `dist/print_pack_2026-06-27/VERIFY.sh` | 3-check protocol the audit trail anchors on |
| WALLET_CARD | `dist/print_pack_2026-06-27/WALLET_CARD.txt` | Pocket-reference carried at the table |
| MORNING_RUNBOOK | `dist/print_pack_2026-06-27/MORNING_RUNBOOK_2026-06-27.md` | T-0 step log |
| PRINT_MANIFEST | `dist/print_pack_2026-06-27/PRINT_MANIFEST.txt` | What was physically carried |
| Commit `85e86aa` | git history | Byte-frozen `build_scene.py` for the 18 finals |
| 18 final renders | `renders/*.png` (A/B/C × 6 cams) | Concept-art deliverable referenced in the deck |
| T+1 debrief | `docs/T+1_DEBRIEF.md` | Filled-in version of the post-signing record |
| Signed escritura PDF | `docs/2026-06-27_escritura_torrasca-vandecamp.pdf` | gitignored per scope rules; lives on USB + Drive |

**Action at T+30:** tag `escritura-archive-2026-07-27` on the commit that finalizes the T+1 debrief. Do not amend tagged history.

---

## 2. Archive (move out of working tree, keep in repo under `_archive/`)

These were load-bearing during prep but are noise post-closing. Move to `_archive/2026-06-27_escritura/`.

- `docs/CLOSING_DAY_PREP.md` → archive once T+1 debrief is final
- `docs/CONTINGENCIES.md` → archive (post-mortem references it as historical)
- `docs/ROLLBACK_RUNBOOK.md` → archive
- `docs/email_drafts/*` → archive entire directory (drafts; the sent versions live in Gmail)
- `docs/POSTMORTEM_2026-06-17.md` → archive
- `docs/DECISIONS_2026-06-17.md` → archive
- `docs/wesley_brief_onepager.md` → archive (post-signing — the deck v6 superseded it)

Move command (run at T+30):
```bash
mkdir -p _archive/2026-06-27_escritura
git mv docs/CLOSING_DAY_PREP.md _archive/2026-06-27_escritura/
git mv docs/CONTINGENCIES.md _archive/2026-06-27_escritura/
git mv docs/ROLLBACK_RUNBOOK.md _archive/2026-06-27_escritura/
git mv docs/email_drafts _archive/2026-06-27_escritura/
git mv docs/POSTMORTEM_2026-06-17.md _archive/2026-06-27_escritura/
git mv docs/DECISIONS_2026-06-17.md _archive/2026-06-27_escritura/
git mv docs/wesley_brief_onepager.md _archive/2026-06-27_escritura/
```

Update CLAUDE.md doc map to point to the archived locations (one line: "post-escritura: see `_archive/2026-06-27_escritura/`").

---

## 3. Keep in working tree (active beyond escritura)

These remain part of the live project — they describe the durable scope, not the closing.

- `docs/CLIENT.md`
- `docs/HOUSING_PARK_CONCEPT.md`
- `docs/EUROPEAN_TOURISM_SPEC.md`
- `docs/RESEARCH_GAPS.md`
- `docs/MASTER_BRIEF.md`
- `docs/master_plan.md`
- `docs/sub_render_strategy.md`
- `lqv/` package + `build_scene.py`
- `scripts/`
- `STATUS.md`
- `ARCHITECTURE.md`
- `CLAUDE.md`
- `CREDITS.md` + `LICENSE_BUNDLE.md` + `LICENSES/`

---

## 4. Delete (regenerable or stale)

Nothing critical should be deleted. The only deletions:

- `scene.blend.session-backup` if older than 30 days (regenerable from `build_scene.py`)
- `renders/_preview_*.png` (preview renders, not the 18 finals)
- `_archive/build_scene.py.pre-refactor.bak` — DO NOT DELETE; documented reference per CLAUDE.md

---

## 5. T+30 git hygiene

```bash
# Repack after the archive moves
git gc --aggressive --prune=now

# Tag the archive state
git tag -a escritura-archive-2026-07-27 -m "T+30 archive freeze post-2026-06-27 closing"

# Push tags
git push origin escritura-archive-2026-07-27

# (If mirror remote configured per #58) sync mirror
git push mirror --tags
```

---

## 6. T+30 documentation updates

1. **STATUS.md** — add a "Post-escritura state (2026-07-27)" section. Note: 18 finals shipped, closing signed, OCTAVA tracker closed, repo pivoting to Phase 8+ housing-park work.
2. **CLAUDE.md** — update the doc map: archived docs get one-line back-pointers to `_archive/2026-06-27_escritura/`.
3. **HOUSING_PARK_CONCEPT.md** — flip from "concept" framing to "active project" framing (the land is closed; the housing park work begins).

---

## 7. What this runbook does NOT cover

- Tax filings (IVA, IRP, inmobiliarios) — that's a separate workflow Wesley + accountant own.
- Construction permitting — Phase 8+ scope, not escritura scope.
- Title registration follow-up — Peña handles this; the chase tracker is `OCTAVA_VENDOR_TRACKER.md` until 2026-07-04, then closed.
- Insurance — separate decision.

---

## 8. Cross-references

- `docs/T+1_DEBRIEF.md` — feeds the freeze decision (what worked / what to keep)
- `docs/OCTAVA_VENDOR_TRACKER.md` — closes before this runbook fires (2026-07-04 deadline; this runbook 2026-07-27)
- `docs/HOUSING_PARK_CONCEPT.md` — next durable scope after the closing
- `STATUS.md` — gets the post-escritura section appended
- `CLAUDE.md` — doc map updated to point at archive locations
