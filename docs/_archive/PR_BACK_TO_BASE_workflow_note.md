# PR Back-to-Base — draft

> Draft of the consolidated pull request that lands the escritura-prep arc on `master`. Opens against `origin/master`. Compose at T+1 once the signing is closed; do NOT open it before signing day (the moving target of the closing prep would force multiple force-pushes).

**Branch:** `escritura-prep` (working branch with the T-10 → T-0 sweep commits)
**Base:** `origin/master`
**Title:** `chore(escritura): T-10 → T+1 closing prep + post-mortem + archive scaffolding`

---

## Summary

This PR lands the closing-prep arc for the 2026-06-27 La Quebrada Viva escritura signing. It bundles three weeks of T-10 → T-0 work plus the day-after debrief scaffolding. The renderer (`build_scene.py` byte-frozen at `85e86aa`) and the 18 finals are unchanged; this is documentation, distribution artifacts, and CI scaffolding only.

## What's in this PR

### Distribution artifacts (frozen)
- `dist/print_pack_2026-06-27/` — bundle ZIP (266 MB, SHA `9ce96b…724a53c`), deck v6 PDF (28 pp, SHA `2e4c26…0701137`), VERIFY.sh 3-check, WALLET_CARD, MORNING_RUNBOOK, PRINT_MANIFEST
- `escritura_deck_v6.pdf` — 28-page deck (frozen at T-10)
- `wesley_bundle_20260616-1715.zip` — distributed bundle (frozen at T-10)

### CI (new workflows)
- `.github/workflows/lint.yml` — ruff 0.6.9 + pytest invariants
- `.github/workflows/smoke.yml` — `RENDER_SKIP=1` build verification
- `.github/workflows/verify.yml` — runs VERIFY.sh + pins bundle/deck SHA-256

### Documentation (T-10 sweep)
- `docs/CONTINGENCIES.md` — C1–C10 closing-day risk playbook (C8/C9 enriched at T-10)
- `docs/POSTMORTEM_2026-06-17.md` — pre-signing risk register
- `docs/DECISIONS_2026-06-17.md` — decisions log
- `docs/ROLLBACK_RUNBOOK.md` — errata + postponement protocol
- `docs/CLIENT.md` — T-10 freshness refresh
- `docs/RESEARCH_GAPS.md` — T-10 freeze note + R35 deferral to T+30

### Post-signing scaffolding (templates, fill at T+1)
- `docs/T_PLUS_1_DEBRIEF.md`
- `docs/OCTAVA_VENDOR_TRACKER.md` — 5-hábiles vendor-comprobante chase (Cl. OCTAVA ii)
- `docs/ARCHIVE_RUNBOOK.md` — T+30 freeze/archive plan
- `docs/PR_BACK_TO_BASE.md` — this draft

### License & bundle hygiene
- `LICENSE_BUNDLE.md` §6 — two gates ticked (CC-BY-SA exclusion verified, STATUS.md 18/18 confirmed) + T-10 sweep note
- `LICENSES/CC0-1.0.txt` + `LICENSES/CC-BY-4.0.txt` (already landed pre-T-10; verified)

### Repo hygiene
- `git gc --aggressive --prune=now` — shrunk `.git` from 580M to 525M
- Explicit-staging-only policy enforced — no `git add -A` used in any commit on this branch

## What's NOT in this PR

- `build_scene.py` — byte-frozen at `85e86aa`. **Zero edits.** Anything that would have required a render change was deferred.
- Signed escritura PDF — gitignored per scope rules (`docs/2026-*_*.pdf`). Lives on USB + Drive.
- Boleto PDF — same exclusion.
- Sub-render backlog — deferred post-escritura (#61–#70 from the implementation plan).
- Hyper3D-generated lapacho meshes — still planned, not yet generated.

## Test plan

- [ ] CI green: lint, smoke, verify all pass on this branch before merge
- [ ] Run `bash dist/print_pack_2026-06-27/VERIFY.sh` locally on the reviewer's machine → 3/3 OK
- [ ] Spot-check 3 random pages of `escritura_deck_v6.pdf` against cifras in `WALLET_CARD.txt` → match
- [ ] Confirm `git log --since=2026-06-07 --oneline` matches the commits expected for the T-10 → T+1 arc
- [ ] Reviewer (Wesley or counsel) confirms the cifras in the deck match the boleto privado

## Reviewers

- **Wesley van de Camp** — final approve on the cifras + scope (the client-facing artifacts)
- **Counsel** (if available pre-signing) — sanity check on Cl. OCTAVA, Cl. NOVENA, Cl. CUARTA references in the deck

## Merge strategy

- Squash merge to `master` with the title above
- After merge, tag `escritura-pr-merged-YYYY-MM-DD` on master
- Do NOT rebase or force-push this branch once the PR is open (the SHA-256 chain in `dist/print_pack_2026-06-27/INTEGRITY.md` is anchored to the commit that ships the bundle; rebasing breaks the audit trail)

## Risk

**Low.** No code edits; documentation + frozen artifacts + CI scaffolding. The only risk surface is the CI workflows — if `verify.yml` flakes on poppler install, the bundle SHA pin still catches drift.

## Post-merge follow-ups

1. T+1 — fill `docs/T_PLUS_1_DEBRIEF.md`
2. T+1 through T+5 — work `docs/OCTAVA_VENDOR_TRACKER.md`
3. T+30 — execute `docs/ARCHIVE_RUNBOOK.md`
4. T+30+ — pivot to Phase 8+ housing-park work per `HOUSING_PARK_CONCEPT.md`

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
