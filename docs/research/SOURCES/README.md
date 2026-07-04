# docs/research/SOURCES

> **For what to research.** This subdir holds the source catalogues:
> GitHub repos evaluated, data sources identified, vendor targets named.

## What's in here

| File | Purpose |
|---|---|
| [`REPO_CATALOG.md`](./REPO_CATALOG.md) | 141 GitHub repos across 6 domains (Blender GIS, geospatial Python, NASA Earthdata, real estate, Paraguay/Atlantic Forest, vegetation 3D), each with verdict (adopt / reference / skip / dead). 51/97 user-supplied URLs that were 404 are flagged honestly. Top 10 to drop in: pysheds, pyflwdir, whitebox-python, earthaccess, nasa/GEDI-Data-Resources, simonbesnard1/gedidb, joewdavies/geoblender, johnbalvin/pyairbnb, ics-py, melizeche/dolarPy. |
| [`property_map_v2_data_sources.md`](./property_map_v2_data_sources.md) | Property map v2 data sources (13 batches A-K, 86-species candidate pool, 437-species biodiversity envelope, MS Open Buildings 737 polys, etc.) |
| [`r38_san_bernardino_targets.md`](./r38_san_bernardino_targets.md) | San Bernardino supply chain target vendors (R38 from RESEARCH_GAPS) |

## When to use

- Looking for a tool to do X? Start with `REPO_CATALOG.md` (141 entries, ranked).
- Identifying what data sources exist for the parcel? See `property_map_v2_data_sources.md`.
- Finding a vendor in San Ber / Asunción? See `r38_san_bernardino_targets.md`.

## Sister subdirs

- [`../METHODS/`](../METHODS/) — how to do research (routing tables, sprint plans)
- [`../TOOLING/`](../TOOLING/) — the actual tooling (Blender+GIS, asset pipelines, materials)
- [`../RESULTS/`](../RESULTS/) — the 107+ answered research results
- [`../README.md`](../../../README.md) — synthesis index, the single best entry-point

---

*Organized 2026-07-03 (Restructure Pass 4). Previously these files were at the top of `docs/research/`.*