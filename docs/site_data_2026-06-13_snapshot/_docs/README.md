# Pre-Wes-Data-Share Snapshot (2026-06-13)

This directory contains a frozen snapshot of the site_data corpus as it stood
on 2026-06-13, the day before Wes shared the full working file set
(2026-06-14).

## Status

**Git-ignored as of 2026-07-03** (commit `e5c2d6b+` + restructure pass).
Preserved on local disk only. Not part of the canonical repo.

## What's in here (for posterity)

| Subdir | Files | Size | What |
|---|--:|--:|---|
| `dem/` | 11 | 23.5 MB | 2.5 m UTM21J DEM tiles + ALOS + SRTM composites |
| `hd_imagery/` | 278 | 27.7 MB | ESRI z17 2 km stitched + per-tile rasters |
| `landcover/` | 4 | 0.2 MB | MapBiomas 2020 snapshot + derived |
| `references/photos/` | 103 | 169 MB | Saltos del Monday reference photos (Pinterest-grade) |
| `references/styles/` | 2 | small | Style inspiration images |
| `sentinel2/` | 1 | small | Pre-fetch state for Sentinel-2 pipeline |
| `analysis/` | 33 | 31.8 MB | Per-asset analysis PNGs (NOT committed to current site_data) |
| `renders_monday/` | 5 | 9.3 MB | Monday render experiments (predecessors to A/B/C finals) |
| **+ Python scripts** | 13 | small | The fetch/build scripts used on 2026-06-13 |
| **Total** | **455** | **261.9 MB** | — |

## Re-populating

If you ever need to re-populate this snapshot, the data is reproducible
from the source APIs and these fetch scripts (which are still in the
snapshot dir for reference):

- **DEMs:** `fetch_dem_pc.py`, `fetch_dem.py` → ALOS PALSAR + SRTM via OpenTopography + Microsoft Planetary Computer
- **Imagery:** `AOI_2km.py`, `build_2km.py`, `build_composites.py` → ESRI World Imagery tile server
- **Sentinel-2:** `fetch_sentinel2.py` → Element84 / AWS Earth Search STAC
- **OSM:** `fetch_osm.py` → Overpass API
- **Blender integration:** `blender_import_monday.py`, `blender_render_monday.py`

Equivalent fetch scripts also live in `scripts/` and `tools/site_data/`
of the canonical repo. The current `docs/site_data/` corpus is the
post-Wes-data-share, post-reconciliation version — much richer
(26 datasets vs 4 here).

## Why gitignored

- Pre-dates Wes's full data share (2026-06-14).
- 261.9 MB of raw raster + reference photos (38% of tracked repo).
- Fully replaced by current `docs/site_data/` contents (which grew
  264 MB → ~395 MB and added 20+ new datasets).
- 169 MB of reference photos (Saltos del Monday / Anfi Teatro) are
  not referenced from anywhere in the current repo's `*.md` or
  `*.py` source — they're inspiration-grade only.
- Kept on disk only for legal/historical record; can be re-fetched
  deterministically from source APIs.

## Disk-only access

```bash
ls /root/la-quebrada-viva/docs/site_data_2026-06-13_snapshot/
```

---

*Gitignored as part of the 2026-07-03 restructure pass. See `docs/audit/INVENTORY.md`
+ `docs/audit/RESTRUCTURE_PLAN.md` Step 1.*