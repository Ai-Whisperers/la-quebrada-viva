#!/usr/bin/env python3
"""Phase-0 §12 #6: Sentinel-2 L2A 12-date timeseries (2020-2025) over the 62 ha
LQV bbox. STAC-searches element84 Earth-Search for the lowest-cloud scene in
each of 12 bi-annual buckets (2020-H1 .. 2025-H2), clip-reads 7 bands
(red/green/blue/nir/swir16/swir22/scl) through /vsicurl/+WarpedVRT to a fixed
EPSG:32721 10 m grid, applies the SCL cloud/shadow mask, computes per-scene
NDVI / NDWI / MNDWI / AWEIsh, builds np.nanmedian composites, renders a
5-panel quicklook, writes per-scene polygon-mean CSV + summary.md.

Outputs under docs/site_data/sentinel2/timeseries_2020_2025/:
  - <SCENE_ID>/<band>.tif                 ← AOI-clipped 10 m COG, 7 bands per scene
  - <SCENE_ID>/<band>.tif.meta.json       ← per-file STAC/license sidecar
  - timeseries_quicklook.png              ← 5-panel RGB+NDVI+NDWI+MNDWI+AWEIsh
  - polygon_indices.csv                   ← per-scene polygon means, +bucket label
  - summary.md                            ← narrative + cross-link to §12 #10/#11
"""

from __future__ import annotations

import csv
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import requests
from rasterio.enums import Resampling
from rasterio.transform import from_bounds as transform_from_bounds
from rasterio.vrt import WarpedVRT
from rasterio.warp import transform_bounds

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.satellite._aoi import aoi_bbox
from scripts.satellite._license import assert_compatible
from scripts.satellite._meta import write_sidecar
from scripts.satellite._retry import skip_if_exists, with_retry

OUT = ROOT / "docs" / "site_data" / "sentinel2" / "timeseries_2020_2025"
OUT.mkdir(parents=True, exist_ok=True)

STAC_URL = "https://earth-search.aws.element84.com/v1/search"
COLLECTION = "sentinel-2-l2a"
LICENSE_ID = "CC-BY-4.0"
CITATION = (
    "Contains modified Copernicus Sentinel data, processed by ESA / element84 "
    "Earth-Search (sentinel-2-l2a)."
)
FETCHER = "scripts.phase0_sentinel2_timeseries_batch"

BANDS = ["red", "green", "blue", "nir", "swir16", "swir22", "scl"]
BAND_RESAMPLING = {  # 10 m bands stay as-is, 20 m bands upsample to 10 m
    "red": Resampling.nearest,
    "green": Resampling.nearest,
    "blue": Resampling.nearest,
    "nir": Resampling.nearest,
    "swir16": Resampling.bilinear,
    "swir22": Resampling.bilinear,
    "scl": Resampling.nearest,
}

# SCL classes to KEEP (vegetation, bare, water, snow). Mask cloud-shadow (3),
# cloud-medium (8), cloud-high (9), thin cirrus (10), saturated (1), dark (2).
SCL_KEEP = (4, 5, 6, 11)

# 12 bi-annual buckets across 2020-01-01 → 2025-12-31.
BUCKETS = []
for y in range(2020, 2026):
    BUCKETS.append((f"{y}-H1", datetime(y, 1, 1, tzinfo=timezone.utc),
                    datetime(y, 6, 30, 23, 59, 59, tzinfo=timezone.utc)))
    BUCKETS.append((f"{y}-H2", datetime(y, 7, 1, tzinfo=timezone.utc),
                    datetime(y, 12, 31, 23, 59, 59, tzinfo=timezone.utc)))

MAX_CLOUD_PCT = 30.0
CANONICAL_CRS = "EPSG:32721"
GRID_M = 10.0  # 10 m output pixels


# ---------- AOI target grid (canonical UTM 21S, 10 m) ---------------------

def aoi_target_grid() -> tuple[tuple[float, float, float, float], int, int, object]:
    """Reproject the 4326 AOI bbox into EPSG:32721, snap to integer 10 m, and
    return (bounds_utm, width_px, height_px, rasterio_transform)."""
    w, s, e, n = aoi_bbox()
    uw, us, ue, un = transform_bounds("EPSG:4326", CANONICAL_CRS, w, s, e, n,
                                      densify_pts=21)
    # Snap outward to the 10 m grid.
    uw = np.floor(uw / GRID_M) * GRID_M
    us = np.floor(us / GRID_M) * GRID_M
    ue = np.ceil(ue / GRID_M) * GRID_M
    un = np.ceil(un / GRID_M) * GRID_M
    width = int(round((ue - uw) / GRID_M))
    height = int(round((un - us) / GRID_M))
    transform = transform_from_bounds(uw, us, ue, un, width, height)
    return (uw, us, ue, un), width, height, transform


TARGET_BOUNDS, TARGET_W, TARGET_H, TARGET_TR = aoi_target_grid()


# ---------- STAC search ----------------------------------------------------

@with_retry()
def _stac_post(body: dict) -> dict:
    r = requests.post(STAC_URL, json=body, timeout=60)
    r.raise_for_status()
    return r.json()


def search_bucket(label: str, start: datetime, end: datetime) -> dict | None:
    """Return lowest-cloud STAC feature in the bucket whose granule fully covers
    the AOI bbox (4326). Returns None if no usable scene in the window."""
    w, s, e, n = aoi_bbox()
    body = {
        "collections": [COLLECTION],
        "bbox": [w, s, e, n],
        "datetime": f"{start.isoformat()}/{end.isoformat()}",
        "query": {"eo:cloud_cover": {"lt": MAX_CLOUD_PCT}},
        "sortby": [{"field": "properties.eo:cloud_cover", "direction": "asc"}],
        "limit": 50,
    }
    try:
        js = _stac_post(body)
    except Exception as exc:  # network / 5xx — bucket skipped, not fatal
        print(f"  [{label}] STAC error: {type(exc).__name__}: {exc}")
        return None
    feats = js.get("features", [])
    # Filter to scenes whose bbox covers the entire AOI (avoids edge-cuts).
    def covers(f: dict) -> bool:
        b = f.get("bbox") or []
        if len(b) < 4:
            return False
        return b[0] <= w and b[1] <= s and b[2] >= e and b[3] >= n
    feats = [f for f in feats if covers(f)]
    if not feats:
        return None
    feats.sort(key=lambda f: f["properties"].get("eo:cloud_cover", 999))
    return feats[0]


# ---------- Per-band clip-on-read ----------------------------------------

@with_retry()
def clip_band(href: str, out_path: Path, resampling: Resampling, *,
              item_id: str, band: str, cloud_cover: float | None,
              dtype_override: str | None = None) -> Path:
    """Open the source COG via /vsicurl/, warp+window into the target grid,
    write a small deflate-tiled COG to out_path, and write a sidecar."""
    if skip_if_exists(out_path, min_bytes=1024):
        return out_path
    assert_compatible(LICENSE_ID)
    src_url = href if href.startswith(("/vsicurl/", "http")) else f"/vsicurl/{href}"
    if src_url.startswith("http"):
        src_url = f"/vsicurl/{src_url}"
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    t0 = time.time()
    with rasterio.Env(GDAL_HTTP_TIMEOUT=180, CPL_VSIL_CURL_CHUNK_SIZE=524288):
        with rasterio.open(src_url) as src:
            with WarpedVRT(
                src,
                crs=CANONICAL_CRS,
                transform=TARGET_TR,
                width=TARGET_W,
                height=TARGET_H,
                resampling=resampling,
            ) as vrt:
                data = vrt.read(1)
                profile = {
                    "driver": "GTiff",
                    "height": TARGET_H,
                    "width": TARGET_W,
                    "count": 1,
                    "dtype": dtype_override or vrt.dtypes[0],
                    "crs": CANONICAL_CRS,
                    "transform": TARGET_TR,
                    "compress": "deflate",
                    "tiled": True,
                    "blockxsize": 256,
                    "blockysize": 256,
                }
                if vrt.nodata is not None:
                    profile["nodata"] = vrt.nodata
                with rasterio.open(tmp, "w", **profile) as dst:
                    dst.write(data, 1)
    tmp.replace(out_path)
    print(f"    {band:7s} {out_path.stat().st_size // 1024} KB ({time.time()-t0:.1f}s)")
    write_sidecar(
        out_path,
        source=href,
        collection=COLLECTION,
        license_id=LICENSE_ID,
        citation=CITATION,
        fetcher=FETCHER,
        extra={"item_id": item_id, "band": band, "cloud_cover": cloud_cover,
               "target_crs": CANONICAL_CRS, "target_bounds_utm21s": list(TARGET_BOUNDS)},
    )
    return out_path


def process_scene(feat: dict, bucket: str) -> dict | None:
    """Fetch all bands for one scene; return a dict of band→path."""
    item_id = feat["id"]
    cloud = feat["properties"].get("eo:cloud_cover")
    date_iso = feat["properties"].get("datetime", "")[:10]
    scene_dir = OUT / item_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    assets = feat.get("assets", {})
    out: dict[str, Path] = {}
    print(f"  [{bucket}] {item_id}  {date_iso}  cloud {cloud}%")
    for band in BANDS:
        if band not in assets:
            print(f"    {band:7s} MISSING from STAC assets — skipping")
            continue
        href = assets[band]["href"]
        out_path = scene_dir / f"{band}.tif"
        try:
            clip_band(href, out_path, BAND_RESAMPLING[band],
                      item_id=item_id, band=band, cloud_cover=cloud)
            out[band] = out_path
        except Exception as exc:
            print(f"    {band:7s} FAILED: {type(exc).__name__}: {str(exc)[:100]}")
    if len(out) < 7:
        print(f"  [{bucket}] only {len(out)}/7 bands — dropping scene")
        return None
    return {"item_id": item_id, "bucket": bucket, "date": date_iso,
            "cloud": cloud, "bands": out}


# ---------- Index math --------------------------------------------------

def load_scene_arrays(bands: dict[str, Path]) -> dict[str, np.ndarray]:
    out = {}
    for b, p in bands.items():
        with rasterio.open(p) as src:
            out[b] = src.read(1)
    return out


def compute_indices(arrs: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Apply SCL keep-mask, scale reflectance 0-10000 → 0-1, compute four indices.
    Returns float32 arrays with NaN where the SCL mask is False or denominators
    are zero."""
    scl = arrs["scl"].astype(np.int16)
    keep = np.isin(scl, SCL_KEEP)

    def b(name: str) -> np.ndarray:
        a = arrs[name].astype(np.float32) / 10000.0
        a = np.where(keep, a, np.nan)
        return a

    red, green, blue = b("red"), b("green"), b("blue")
    nir, swir16, swir22 = b("nir"), b("swir16"), b("swir22")

    def safe_ratio(num: np.ndarray, den: np.ndarray) -> np.ndarray:
        with np.errstate(invalid="ignore", divide="ignore"):
            out = num / den
        out = np.where(np.isfinite(out), out, np.nan)
        return out.astype(np.float32)

    ndvi = safe_ratio(nir - red, nir + red)
    ndwi = safe_ratio(green - nir, green + nir)
    mndwi = safe_ratio(green - swir16, green + swir16)
    aweish = (blue + 2.5 * green - 1.5 * (nir + swir16) - 0.25 * swir22).astype(np.float32)
    return {"ndvi": ndvi, "ndwi": ndwi, "mndwi": mndwi, "aweish": aweish,
            "red": red, "green": green, "blue": blue}


# ---------- Median composite + 5-panel quicklook ------------------------

def median_stack(per_scene_idx: list[dict[str, np.ndarray]]) -> dict[str, np.ndarray]:
    keys = ("ndvi", "ndwi", "mndwi", "aweish", "red", "green", "blue")
    out = {}
    for k in keys:
        stack = np.stack([s[k] for s in per_scene_idx], axis=0)
        with np.errstate(all="ignore"):
            out[k] = np.nanmedian(stack, axis=0).astype(np.float32)
    return out


def render_quicklook(med: dict[str, np.ndarray]) -> Path:
    out_path = OUT / "timeseries_quicklook.png"
    r = np.clip(np.nan_to_num(med["red"], nan=0.0), 0, 0.3) / 0.3
    g = np.clip(np.nan_to_num(med["green"], nan=0.0), 0, 0.3) / 0.3
    b = np.clip(np.nan_to_num(med["blue"], nan=0.0), 0, 0.3) / 0.3
    rgb = np.stack([r, g, b], axis=-1)

    fig, axes = plt.subplots(1, 5, figsize=(22, 5), dpi=140)
    uw, us, ue, un = TARGET_BOUNDS
    extent = (uw, ue, us, un)
    panels = [
        ("RGB median",     rgb,           None,  None,  None),
        ("NDVI median",    med["ndvi"],   "RdYlGn",  -0.2, 0.9),
        ("NDWI median",    med["ndwi"],   "BrBG",    -0.5, 0.5),
        ("MNDWI median",   med["mndwi"],  "BrBG",    -0.5, 0.5),
        ("AWEIsh median",  med["aweish"], "Blues",   -0.5, 0.5),
    ]
    for ax, (title, data, cmap, vmin, vmax) in zip(axes, panels):
        if cmap is None:
            ax.imshow(data, extent=extent, origin="upper")
        else:
            im = ax.imshow(data, extent=extent, origin="upper",
                           cmap=cmap, vmin=vmin, vmax=vmax)
            fig.colorbar(im, ax=ax, shrink=0.7)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("Easting (m, UTM 21S)")
        ax.set_ylabel("Northing (m, UTM 21S)")
        ax.set_aspect("equal")
    fig.suptitle(
        "Sentinel-2 L2A 12-date median 2020-2025 — La Quebrada Viva 62 ha AOI",
        fontsize=13,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  quicklook → {out_path.name}")
    return out_path


# ---------- Per-scene polygon-mean CSV ----------------------------------

def write_indices_csv(rows: list[dict]) -> Path:
    out_path = OUT / "polygon_indices.csv"
    cols = ["bucket", "date", "scene_id", "cloud_pct", "valid_pixels",
            "ndvi_mean", "ndwi_mean", "mndwi_mean", "aweish_mean"]
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"  csv → {out_path.name} ({len(rows)} scenes)")
    return out_path


# ---------- Markdown summary -------------------------------------------

def write_summary(rows: list[dict], scene_count_target: int) -> Path:
    out_path = OUT / "summary.md"
    if rows:
        ndvi_vals = [r["ndvi_mean"] for r in rows if r["ndvi_mean"] is not None]
        ndwi_vals = [r["ndwi_mean"] for r in rows if r["ndwi_mean"] is not None]
        mndwi_vals = [r["mndwi_mean"] for r in rows if r["mndwi_mean"] is not None]
        aweish_vals = [r["aweish_mean"] for r in rows if r["aweish_mean"] is not None]
    else:
        ndvi_vals = ndwi_vals = mndwi_vals = aweish_vals = []

    def mm(vals):
        if not vals:
            return ("n/a", "n/a", "n/a")
        return (f"{min(vals):+.3f}", f"{max(vals):+.3f}",
                f"{sum(vals)/len(vals):+.3f}")

    ndvi_min, ndvi_max, ndvi_mean = mm(ndvi_vals)
    ndwi_min, ndwi_max, ndwi_mean = mm(ndwi_vals)
    mndwi_min, mndwi_max, mndwi_mean = mm(mndwi_vals)
    aweish_min, aweish_max, aweish_mean = mm(aweish_vals)

    w, s, e, n = aoi_bbox()
    uw, us, ue, un = TARGET_BOUNDS

    md = [
        "# Sentinel-2 L2A 12-date timeseries 2020–2025 — Phase-0 §12 #6",
        "",
        "**Source.** element84 Earth-Search STAC, collection "
        f"`{COLLECTION}` (Copernicus Sentinel-2 L2A surface reflectance, 10 m).",
        f"**License.** {LICENSE_ID} (ESA Sentinel Legal Notice ≈ CC-BY-4.0).",
        f"**AOI bbox (EPSG:4326).** W{w:.4f} S{s:.4f} E{e:.4f} N{n:.4f}",
        f"**Target grid (EPSG:32721, 10 m).** "
        f"W{uw:.0f} S{us:.0f} E{ue:.0f} N{un:.0f}  ({TARGET_W}×{TARGET_H} px)",
        f"**Scenes resolved.** {len(rows)} / {scene_count_target} bi-annual buckets "
        f"({rows[0]['date'] if rows else '?'} → {rows[-1]['date'] if rows else '?'}).",
        "",
        "## Per-scene polygon-mean indices",
        "",
        "| Bucket | Date | Scene | Cloud % | NDVI | NDWI | MNDWI | AWEIsh |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in rows:
        def fmt(v): return "n/a" if v is None else f"{v:+.3f}"
        md.append(
            f"| {r['bucket']} | {r['date']} | `{r['scene_id']}` | "
            f"{r['cloud_pct']:.1f} | {fmt(r['ndvi_mean'])} | "
            f"{fmt(r['ndwi_mean'])} | {fmt(r['mndwi_mean'])} | "
            f"{fmt(r['aweish_mean'])} |"
        )

    md.extend([
        "",
        "## Summary statistics (across the 12-scene polygon means)",
        "",
        "| Index | Min | Max | Mean |",
        "| --- | ---: | ---: | ---: |",
        f"| NDVI   | {ndvi_min}   | {ndvi_max}   | {ndvi_mean}   |",
        f"| NDWI   | {ndwi_min}   | {ndwi_max}   | {ndwi_mean}   |",
        f"| MNDWI  | {mndwi_min}  | {mndwi_max}  | {mndwi_mean}  |",
        f"| AWEIsh | {aweish_min} | {aweish_max} | {aweish_mean} |",
        "",
        "## Index definitions",
        "",
        "- **NDVI** = (NIR − Red) / (NIR + Red). Greenness / live biomass. "
        "Native forest is typically 0.7–0.9; bare soil ≤ 0.2.",
        "- **NDWI** (Gao) = (Green − NIR) / (Green + NIR). Canopy / surface "
        "water content. Positive = open water; negative = vegetation.",
        "- **MNDWI** = (Green − SWIR1) / (Green + SWIR1). Better water "
        "discriminator than NDWI in built/turbid scenes (Xu 2006).",
        "- **AWEIsh** = Blue + 2.5·Green − 1.5·(NIR + SWIR1) − 0.25·SWIR2. "
        "Feyisa et al. 2014 — open-water index tuned for shadow rejection. "
        "Positive = water.",
        "",
        "## Cloud / shadow masking (SCL)",
        "",
        "Per-scene Scene Classification (SCL) is the L2A 20 m product band. "
        "We **keep** classes 4 (vegetation), 5 (bare), 6 (water), 11 (snow) "
        "and **mask** 1 (saturated), 2 (dark), 3 (cloud shadow), 8 (cloud "
        "medium-prob), 9 (cloud high-prob), 10 (thin cirrus), 0 (no-data). "
        "Masked pixels become NaN in each index array and are excluded from "
        "both the per-scene polygon mean and the 12-scene `np.nanmedian` "
        "stack.",
        "",
        "## Cross-references",
        "",
        "- Phase-0 §12 #10 (Hansen GFC, `docs/site_data/hansen_gfc/`) gives "
        "continuous treecover2000 / loss-year — pair with NDVI median for the "
        "deck's canopy story.",
        "- Phase-0 §12 #11 (Mapbiomas PY, `docs/site_data/mapbiomas_paraguay/`) "
        "gives categorical 30 m LULC 1985–2023 — pair with MNDWI/AWEIsh "
        "median to check whether Mapbiomas' Flooded Forest (class 6) pixels "
        "actually carry water signal here.",
        "- Phase-0 §12 #12 (JRC GSW, `docs/site_data/jrc_gsw/`) gives global "
        "surface-water occurrence — AWEIsh median is the high-res LQV-only "
        "counterpart.",
        "",
        "## Files",
        "",
        "```",
        "docs/site_data/sentinel2/timeseries_2020_2025/",
        "├── <SCENE_ID>/                     × up to 12 scenes",
        "│   ├── red.tif        (10 m, 0-10000 reflectance)",
        "│   ├── green.tif",
        "│   ├── blue.tif",
        "│   ├── nir.tif",
        "│   ├── swir16.tif     (resampled 20 m → 10 m, bilinear)",
        "│   ├── swir22.tif     (resampled 20 m → 10 m, bilinear)",
        "│   ├── scl.tif        (20 m → 10 m, nearest)",
        "│   └── *.tif.meta.json (per-file STAC/license sidecar)",
        "├── timeseries_quicklook.png  ← 5-panel RGB+NDVI+NDWI+MNDWI+AWEIsh",
        "├── polygon_indices.csv       ← per-scene polygon means + bucket label",
        "└── summary.md                ← this file",
        "```",
        "",
        "## Caveats",
        "",
        "- Bucket coverage is **best-effort**: if every Sentinel-2 pass in a "
        f"half-year exceeds {MAX_CLOUD_PCT:.0f}% cloud, that bucket is empty "
        "and the median composite is computed from the remaining scenes.",
        "- The 12-scene median is **not** a phenology-aware composite — "
        "wet/dry season scenes are mixed into one stack. For a dry-season-only "
        "or wet-season-only median, regenerate with a narrower bucket window.",
        "- Bands are warped to a fixed 10 m EPSG:32721 grid via "
        "`rasterio.vrt.WarpedVRT` (nearest for 10 m bands & SCL, bilinear for "
        "20 m SWIR). The output is exactly aligned across scenes, so per-pixel "
        "differencing between scenes is meaningful.",
        "- Per-scene `.tif` files are kept on disk for re-runs but are "
        "**git-ignored** (see `.gitignore`: "
        "`docs/site_data/sentinel2/**/*.tif`). The PNG / CSV / MD outputs and "
        "the per-file `.meta.json` sidecars are tracked.",
        "- Polygon means here use the full **AOI rectangle** (62 ha bbox), not "
        "the cadastral padron union, because Batch I needs a stable footprint "
        "that doesn't drift if a padron lookup later changes the parcel "
        "polygon. For padron-aligned numbers, intersect the COGs with "
        "`scripts/satellite/_aoi.parcel_polygon_geojson()` downstream.",
    ])
    out_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"  summary → {out_path.name}")
    return out_path


# ---------- Main --------------------------------------------------------

def main() -> int:
    print("=" * 78)
    print("Phase-0 §12 #6 — Sentinel-2 L2A 12-date timeseries (2020-2025)")
    print(f"AOI 4326: {aoi_bbox()}")
    print(f"AOI 32721 grid: {TARGET_BOUNDS}  ({TARGET_W}×{TARGET_H} px @ 10 m)")
    print("=" * 78)

    # 1) STAC search every bucket.
    selected: list[dict] = []
    for label, start, end in BUCKETS:
        feat = search_bucket(label, start, end)
        if feat is None:
            print(f"  [{label}] no covering scene under {MAX_CLOUD_PCT:.0f}% cloud")
            continue
        selected.append({"bucket": label, "feat": feat})

    if not selected:
        print("no scenes selected — aborting")
        return 1

    # 2) Per-scene clip-on-read.
    scenes: list[dict] = []
    for s in selected:
        sc = process_scene(s["feat"], s["bucket"])
        if sc is not None:
            scenes.append(sc)

    if not scenes:
        print("no scenes successfully fetched — aborting")
        return 1

    # 3) Indices + per-scene polygon means.
    per_scene_idx: list[dict[str, np.ndarray]] = []
    csv_rows: list[dict] = []
    for sc in scenes:
        arrs = load_scene_arrays(sc["bands"])
        idx = compute_indices(arrs)
        per_scene_idx.append(idx)

        valid = np.isfinite(idx["ndvi"])
        valid_pixels = int(valid.sum())

        def m(name):
            v = idx[name]
            v = v[np.isfinite(v)]
            return float(np.nanmean(v)) if v.size else None

        csv_rows.append({
            "bucket": sc["bucket"],
            "date": sc["date"],
            "scene_id": sc["item_id"],
            "cloud_pct": sc["cloud"] if sc["cloud"] is not None else float("nan"),
            "valid_pixels": valid_pixels,
            "ndvi_mean": m("ndvi"),
            "ndwi_mean": m("ndwi"),
            "mndwi_mean": m("mndwi"),
            "aweish_mean": m("aweish"),
        })

    write_indices_csv(csv_rows)

    # 4) Median composites + quicklook.
    med = median_stack(per_scene_idx)
    render_quicklook(med)

    # 5) Summary markdown.
    write_summary(csv_rows, scene_count_target=len(BUCKETS))

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
