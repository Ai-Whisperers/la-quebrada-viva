# docs/research/METHODS

> **For how to do research.** This subdir holds the methodology docs:
> how to route a research item, how to dispatch a sprint batch, how
> to decide whether something is MEM-trainable vs needs FETCH or HUMAN.

## What's in here

| File | Purpose |
|---|---|
| [`EXECUTION.md`](./EXECUTION.md) | Routing table (MEM/FETCH/SEARCH/HUMAN-{L,S,W,H}) + per-item method routing for 128 research items + findings log |
| [`SPRINT1_AI_BATCH_PLAN.md`](./SPRINT1_AI_BATCH_PLAN.md) | The Sprint 1 AI batch plan (which research items to dispatch in parallel via subagents) |

## When to use

- Adding a new research item? Check `EXECUTION.md` for the routing table
  before deciding whether it's AI-dispatchable or needs a human (Sonja,
  attorney, ANDE office visit).
- Planning a research sprint? Copy `SPRINT1_AI_BATCH_PLAN.md` as a
  template.

## Sister subdirs

- [`../SOURCES/`](../SOURCES/) — what to research (catalogs of repos, data sources, vendor targets)
- [`../TOOLING/`](../TOOLING/) — the actual tooling (Blender+GIS, asset pipelines, materials)
- [`../RESULTS/`](../RESULTS/) — the 107+ answered research results
- [`../README.md`](../../../README.md) — synthesis index, the single best entry-point

---

*Organized 2026-07-03 (Restructure Pass 4). Previously these files were at the top of `docs/research/`.*