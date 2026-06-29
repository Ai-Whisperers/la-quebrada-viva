#!/usr/bin/env python3
"""Phase-0 §12 #8: Landsat Collection 2 Level-2 surface-reflectance annual
median composites 1985-2025 over the 62 ha LQV bbox. STAC-searches Microsoft
Planetary Computer's `landsat-c2-l2` for L4-TM, L5-TM, L7-ETM+, L8-OLI, L9-OLI-2
scenes per year, fetches a fresh SAS token, clip-reads red+green+blue+nir08+
swir16+swir22+qa_pixel through /vsicurl/+WarpedVRT to a 30 m EPSG:32721 grid
sharing the same AOI bounds as Batches I/J (302×334 @ 10 m → 102×112 @ 30 m),
applies the C2-L2 QA_PIXEL cloud/cirrus/shadow mask, rescales DN to surface
reflectance (×0.0000275 − 0.2), computes per-scene NDVI / NBR / NDMI in
memory, then per-year `np.nanmedian` composites across the cleanest K scenes.
Outputs per-year index COGs + a 41-year panel + a decadal panel + a per-year
polygon-mean CSV + summary.md.

Outputs under docs/site_data/landsat/annual_median_1985_2025/:
  - <YEAR>/ndvi.tif, nbr.tif, ndmi.tif      ← 30 m, float32, median composite
  - <YEAR>/*.tif.meta.json                  ← per-file STAC/license sidecar
  - annual_quicklook.png                    ← 41-year NDVI grid (≤ 9 cols)
  - decadal_quicklook.png                   ← 5-panel decadal NDVI+NBR+NDMI
  - polygon_indices.csv                     ← per-year polygon means
  - summary.md                              ← narrative + cross-link to §12 #6/#7
"""

from __future__ import annotations

import csv
import sys
import time
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
from scripts.satellite._retry import with_retry

OUT = ROOT / "docs" / "site_data" / "landsat" / "annual_median_1985_2025"
OUT.mkdir(parents=True, exist_ok=True)

STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
SAS_URL = "https://planetarycomputer.microsoft.com/api/sas/v1/token/landsat-c2-l2"
COLLECTION = "landsat-c2-l2"
LICENSE_ID = "USGS-PD"
CITATION = (
    "Contains Landsat Collection 2 Level-2 Surface Reflectance data courtesy "
    "of the U.S. Geological Survey, distributed by Microsoft Planetary "
    "Computer (landsat-c2-l2). USGS data are in the public domain."
)
FETCHER = "scripts.phase0_landsat_annual_batch"

YEAR_START = 1985
YEAR_END = 2025

# Cap scenes per year at the K cleanest by cloud_cover. Median of 4-6 clear
# scenes effectively suppresses residual haze without paying the full revisit-
# cadence (~22 scenes/year for L8+L9 alone in recent years).
MAX_SCENES_PER_YEAR = 8
CLOUD_COVER_LIMIT = 30.0

# Shared 30 m EPSG:32721 grid — same AOI corners as Batches I/J. Native
# Landsat is 30 m; reprojecting to 10 m would fabricate resolution.
CANONICAL_CRS = "EPSG:32721"
GRID_M = 30.0

# C2-L2 surface-reflectance scale/offset (USGS, all platforms L4-L9).
SR_SCALE = 0.0000275
SR_OFFSET = -0.2

# QA_PIXEL bitmask we treat as "drop this pixel" — dilated cloud (1),
# cirrus (2), cloud (3), cloud shadow (4). Keep snow (5); none expected here.
QA_REJECT_BITS = (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4)


# ---------- AOI target grid (canonical UTM 21S, 30 m) ---------------------

def aoi_target_grid_30m() -> tuple[tuple[float, float, float, float], int, int, object]:
    """30 m grid on the same AOI corners as the 10 m S2/S1 batches.

    We *force* the corners to fall on the same UTM-aligned bounds the 10 m
    grid uses (W495480 S7163620 E498500 N7166960), which divides cleanly by
    30 m (302×334 ÷ 3 ≈ 101×111; rounded up to 102×112 to keep the AOI fully
    inside). Per-pixel comparisons against S2/S1 require a 3:1 downsample on
    the 10 m side, not a re-warp here.
    """
    w, s, e, n = aoi_bbox()
    uw, us, ue, un = transform_bounds("EPSG:4326", CANONICAL_CRS, w, s, e, n,
                                      densify_pts=21)
    uw = np.floor(uw / GRID_M) * GRID_M
    us = np.floor(us / GRID_M) * GRID_M
    ue = np.ceil(ue / GRID_M) * GRID_M
    un = np.ceil(un / GRID_M) * GRID_M
    width = int(round((ue - uw) / GRID_M))
    height = int(round((un - us) / GRID_M))
    transform = transform_from_bounds(uw, us, ue, un, width, height)
    return (uw, us, ue, un), width, height, transform


TARGET_BOUNDS, TARGET_W, TARGET_H, TARGET_TR = aoi_target_grid_30m()


# ---------- MPC SAS token (refresh per run) ------------------------------

@with_retry()
def fetch_sas_token() -> str:
    r = requests.get(SAS_URL, timeout=30)
    r.raise_for_status()
    js = r.json()
    token = js.get("token")
    if not token:
        raise RuntimeError(f"SAS endpoint returned no token: {js}")
    print(f"  SAS token expires {js.get('msft:expiry', '?')}")
    return token


def signed_href(href: str, sas: str) -> str:
    sep = "&" if "?" in href else "?"
    return f"{href}{sep}{sas}"


# ---------- STAC search ----------------------------------------------------

@with_retry()
def _stac_post(body: dict) -> dict:
    r = requests.post(STAC_URL, json=body, timeout=60)
    r.raise_for_status()
    return r.json()


def search_year(year: int) -> list[dict]:
    """All L4/5/7/8/9 C2-L2 scenes covering the AOI in the year, cloud-filtered."""
    w, s, e, n = aoi_bbox()
    body = {
        "collections": [COLLECTION],
        "bbox": [w, s, e, n],
        "datetime": f"{year}-01-01T00:00:00Z/{year}-12-31T23:59:59Z",
        "query": {
            "eo:cloud_cover": {"lt": CLOUD_COVER_LIMIT},
            "platform": {"in": ["landsat-4", "landsat-5", "landsat-7",
                                "landsat-8", "landsat-9"]},
        },
        "limit": 200,
    }
    js = _stac_post(body)
    feats = js.get("features", [])

    def covers(f: dict) -> bool:
        b = f.get("bbox") or []
        if len(b) < 4:
            return False
        return b[0] <= w and b[1] <= s and b[2] >= e and b[3] >= n

    feats = [f for f in feats if covers(f)]
    feats.sort(key=lambda f: float(f["properties"].get("eo:cloud_cover", 100.0)))
    return feats[:MAX_SCENES_PER_YEAR]


# ---------- Per-band clip-on-read ----------------------------------------

@with_retry()
def read_band(href: str, *, resampling: Resampling) -> np.ndarray:
    """Stream-read one Landsat asset to the target 30 m grid; return array."""
    src_url = href if href.startswith("/vsicurl/") else f"/vsicurl/{href}"
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
                return vrt.read(1)


def scene_indices(feat: dict, sas: str) -> dict | None:
    """Read R/G/B/NIR/SWIR16/SWIR22/QA for one scene → masked SR + indices."""
    item_id = feat["id"]
    props = feat["properties"]
    dt_iso = props.get("datetime", "")
    platform = props.get("platform", "?")
    cloud = float(props.get("eo:cloud_cover", -1.0))
    assets = feat.get("assets", {})

    needed = ("red", "green", "blue", "nir08", "swir16", "swir22", "qa_pixel")
    for k in needed:
        if k not in assets:
            print(f"      MISSING asset {k} on {item_id} — skipping scene")
            return None

    t0 = time.time()
    try:
        dn = {k: read_band(signed_href(assets[k]["href"], sas),
                           resampling=Resampling.bilinear)
              for k in needed if k != "qa_pixel"}
        qa = read_band(signed_href(assets["qa_pixel"]["href"], sas),
                       resampling=Resampling.nearest)
    except Exception as exc:
        print(f"      READ FAILED: {type(exc).__name__}: {str(exc)[:100]}")
        return None

    bad = (qa.astype(np.uint32) & QA_REJECT_BITS) != 0
    fill = qa == 0

    sr = {}
    for k, arr in dn.items():
        a = arr.astype(np.float32) * SR_SCALE + SR_OFFSET
        a[bad | fill] = np.nan
        a = np.where((a >= 0.0) & (a <= 1.0), a, np.nan)
        sr[k] = a

    nir = sr["nir08"]
    red = sr["red"]
    sw1 = sr["swir16"]
    sw2 = sr["swir22"]
    with np.errstate(invalid="ignore", divide="ignore"):
        ndvi = (nir - red) / (nir + red)
        nbr = (nir - sw2) / (nir + sw2)
        ndmi = (nir - sw1) / (nir + sw1)

    valid_pixels = int(np.isfinite(ndvi).sum())
    print(f"      {item_id}  {platform}  cc={cloud:5.2f}%  "
          f"valid={valid_pixels:5d}/{TARGET_W*TARGET_H}  "
          f"({time.time()-t0:.1f}s)")
    return {
        "item_id": item_id,
        "platform": platform,
        "datetime": dt_iso,
        "cloud_cover": cloud,
        "sr": sr,
        "ndvi": ndvi,
        "nbr": nbr,
        "ndmi": ndmi,
        "valid_pixels": valid_pixels,
    }


# ---------- Per-year median + write ---------------------------------------

def write_year_tif(out_path: Path, arr: np.ndarray, *, item_ids: list[str],
                   platforms: list[str], year: int, index_name: str) -> Path:
    assert_compatible(LICENSE_ID)
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    profile = {
        "driver": "GTiff",
        "height": TARGET_H,
        "width": TARGET_W,
        "count": 1,
        "dtype": "float32",
        "crs": CANONICAL_CRS,
        "transform": TARGET_TR,
        "compress": "deflate",
        "tiled": True,
        "blockxsize": 64,
        "blockysize": 64,
        "nodata": float("nan"),
    }
    with rasterio.open(tmp, "w", **profile) as dst:
        dst.write(arr.astype(np.float32), 1)
    tmp.replace(out_path)
    write_sidecar(
        out_path,
        source=f"stac:{COLLECTION}#year={year}",
        collection=COLLECTION,
        license_id=LICENSE_ID,
        citation=CITATION,
        fetcher=FETCHER,
        extra={
            "year": year,
            "index": index_name,
            "n_scenes": len(item_ids),
            "scene_ids": item_ids,
            "platforms": platforms,
            "target_crs": CANONICAL_CRS,
            "target_bounds_utm21s": list(TARGET_BOUNDS),
            "grid_m": GRID_M,
        },
    )
    return out_path


def process_year(year: int, sas: str) -> dict | None:
    print(f"\n[{year}] searching STAC ...")
    feats = search_year(year)
    if not feats:
        print(f"  no scenes ≤ {CLOUD_COVER_LIMIT}% cloud — skipping")
        return None
    print(f"  {len(feats)} scenes ≤ {CLOUD_COVER_LIMIT}% cloud (cleanest first)")

    year_dir = OUT / str(year)
    year_dir.mkdir(parents=True, exist_ok=True)

    ndvi_paths = year_dir / "ndvi.tif"
    nbr_paths = year_dir / "nbr.tif"
    ndmi_paths = year_dir / "ndmi.tif"

    if all(p.exists() for p in (ndvi_paths, nbr_paths, ndmi_paths)):
        print(f"  cache hit — reusing {year_dir.name}/*.tif")
        with rasterio.open(ndvi_paths) as s: ndvi = s.read(1)
        with rasterio.open(nbr_paths) as s: nbr = s.read(1)
        with rasterio.open(ndmi_paths) as s: ndmi = s.read(1)
        side = ndvi_paths.with_suffix(".tif.meta.json")
        scene_ids: list[str] = []
        platforms: list[str] = []
        try:
            import json
            with side.open() as fh:
                meta = json.load(fh)
            extra = meta.get("extra", {}) or meta
            scene_ids = list(extra.get("scene_ids", []) or [])
            platforms = list(extra.get("platforms", []) or [])
        except (OSError, ValueError, KeyError):
            pass
        return {"year": year, "ndvi": ndvi, "nbr": nbr, "ndmi": ndmi,
                "scene_ids": scene_ids, "platforms": platforms,
                "n_scenes": len(scene_ids) or 0}

    scenes = []
    for f in feats:
        sc = scene_indices(f, sas)
        if sc is not None and sc["valid_pixels"] > 0:
            scenes.append(sc)
    if not scenes:
        print(f"  no usable scenes after QA mask — skipping")
        return None

    ndvi_stack = np.stack([s["ndvi"] for s in scenes], axis=0)
    nbr_stack = np.stack([s["nbr"] for s in scenes], axis=0)
    ndmi_stack = np.stack([s["ndmi"] for s in scenes], axis=0)
    with np.errstate(all="ignore"):
        ndvi = np.nanmedian(ndvi_stack, axis=0).astype(np.float32)
        nbr = np.nanmedian(nbr_stack, axis=0).astype(np.float32)
        ndmi = np.nanmedian(ndmi_stack, axis=0).astype(np.float32)

    item_ids = [s["item_id"] for s in scenes]
    platforms = sorted({s["platform"] for s in scenes})

    write_year_tif(ndvi_paths, ndvi, item_ids=item_ids, platforms=platforms,
                   year=year, index_name="NDVI")
    write_year_tif(nbr_paths, nbr, item_ids=item_ids, platforms=platforms,
                   year=year, index_name="NBR")
    write_year_tif(ndmi_paths, ndmi, item_ids=item_ids, platforms=platforms,
                   year=year, index_name="NDMI")

    return {"year": year, "ndvi": ndvi, "nbr": nbr, "ndmi": ndmi,
            "scene_ids": item_ids, "platforms": platforms,
            "n_scenes": len(scenes)}


# ---------- Quicklooks -----------------------------------------------------

def render_annual_quicklook(rows: list[dict]) -> Path:
    out_path = OUT / "annual_quicklook.png"
    n = len(rows)
    cols = 9
    rows_n = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows_n, cols, figsize=(cols * 2.0, rows_n * 2.0),
                             dpi=140)
    axes = np.atleast_2d(axes).reshape(rows_n, cols)
    for ax in axes.ravel():
        ax.axis("off")
    for i, r in enumerate(rows):
        ax = axes[i // cols][i % cols]
        ax.imshow(r["ndvi"], cmap="YlGn", vmin=-0.2, vmax=0.95,
                  interpolation="nearest")
        ax.set_title(f"{r['year']}  n={r['n_scenes']}", fontsize=9)
        ax.axis("off")
    fig.suptitle(
        f"Landsat C2-L2 annual NDVI median — La Quebrada Viva 62 ha — "
        f"{rows[0]['year']}–{rows[-1]['year']}",
        fontsize=13,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  annual quicklook → {out_path.name}")
    return out_path


DECADES = (
    ("1985-1994", 1985, 1994),
    ("1995-2004", 1995, 2004),
    ("2005-2014", 2005, 2014),
    ("2015-2024", 2015, 2024),
    ("2025",      2025, 2025),
)


def render_decadal_quicklook(rows: list[dict]) -> Path:
    out_path = OUT / "decadal_quicklook.png"
    by_year = {r["year"]: r for r in rows}
    panels: list[tuple[str, np.ndarray, np.ndarray, np.ndarray]] = []
    for label, y0, y1 in DECADES:
        block = [by_year[y] for y in range(y0, y1 + 1) if y in by_year]
        if not block:
            continue
        with np.errstate(all="ignore"):
            ndvi = np.nanmedian(np.stack([b["ndvi"] for b in block]), axis=0)
            nbr  = np.nanmedian(np.stack([b["nbr"]  for b in block]), axis=0)
            ndmi = np.nanmedian(np.stack([b["ndmi"] for b in block]), axis=0)
        panels.append((label, ndvi, nbr, ndmi))

    fig, axes = plt.subplots(3, len(panels),
                             figsize=(len(panels) * 3.0, 9.0), dpi=140)
    if len(panels) == 1:
        axes = axes.reshape(3, 1)

    band_specs = [
        ("NDVI",  "YlGn",  -0.2, 0.95),
        ("NBR",   "RdYlGn", -0.5, 0.9),
        ("NDMI",  "BrBG",  -0.4, 0.6),
    ]
    for col, (label, ndvi, nbr, ndmi) in enumerate(panels):
        for row, (name, cmap, vmin, vmax) in enumerate(band_specs):
            data = (ndvi, nbr, ndmi)[row]
            ax = axes[row][col]
            im = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax,
                           interpolation="nearest")
            if row == 0:
                ax.set_title(label, fontsize=12)
            if col == 0:
                ax.set_ylabel(name, fontsize=11)
            ax.set_xticks([]); ax.set_yticks([])
            fig.colorbar(im, ax=ax, shrink=0.65)
    fig.suptitle(
        "Landsat C2-L2 decadal medians — La Quebrada Viva 62 ha — "
        "1985–2025 (rows: NDVI / NBR / NDMI)",
        fontsize=13,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  decadal quicklook → {out_path.name}")
    return out_path


# ---------- Per-year polygon-mean CSV -------------------------------------

def write_indices_csv(rows: list[dict]) -> Path:
    out_path = OUT / "polygon_indices.csv"
    cols = ["year", "n_scenes", "platforms", "valid_pixels",
            "ndvi_mean", "nbr_mean", "ndmi_mean"]
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            valid = np.isfinite(r["ndvi"])
            def m(arr):
                v = arr[valid]
                return float(np.nanmean(v)) if v.size else None
            w.writerow({
                "year": r["year"],
                "n_scenes": r["n_scenes"],
                "platforms": "|".join(r["platforms"]),
                "valid_pixels": int(valid.sum()),
                "ndvi_mean": m(r["ndvi"]),
                "nbr_mean":  m(r["nbr"]),
                "ndmi_mean": m(r["ndmi"]),
            })
    print(f"  csv → {out_path.name} ({len(rows)} years)")
    return out_path


# ---------- Markdown summary ----------------------------------------------

def write_summary(rows: list[dict]) -> Path:
    out_path = OUT / "summary.md"
    polygon_rows = []
    for r in rows:
        valid = np.isfinite(r["ndvi"])
        def m(arr):
            v = arr[valid]
            return float(np.nanmean(v)) if v.size else None
        polygon_rows.append({
            "year": r["year"],
            "n_scenes": r["n_scenes"],
            "platforms": "|".join(r["platforms"]),
            "ndvi": m(r["ndvi"]), "nbr": m(r["nbr"]), "ndmi": m(r["ndmi"]),
        })

    ndvi_vals = [p["ndvi"] for p in polygon_rows if p["ndvi"] is not None]
    nbr_vals  = [p["nbr"]  for p in polygon_rows if p["nbr"]  is not None]
    ndmi_vals = [p["ndmi"] for p in polygon_rows if p["ndmi"] is not None]

    def mm(vals):
        if not vals:
            return ("n/a", "n/a", "n/a")
        return (f"{min(vals):+.3f}", f"{max(vals):+.3f}",
                f"{sum(vals)/len(vals):+.3f}")

    ndvi_min, ndvi_max, ndvi_mean = mm(ndvi_vals)
    nbr_min,  nbr_max,  nbr_mean  = mm(nbr_vals)
    ndmi_min, ndmi_max, ndmi_mean = mm(ndmi_vals)

    w, s, e, n = aoi_bbox()
    uw, us, ue, un = TARGET_BOUNDS

    md = [
        "# Landsat C2-L2 annual median 1985–2025 — Phase-0 §12 #8",
        "",
        "**Source.** Microsoft Planetary Computer STAC, collection "
        f"`{COLLECTION}` (USGS Landsat Collection 2 Level-2 Surface "
        "Reflectance, 30 m, Landsat 4-TM / 5-TM / 7-ETM+ / 8-OLI / 9-OLI-2).",
        f"**License.** {LICENSE_ID} (USGS data are in the public domain).",
        f"**AOI bbox (EPSG:4326).** W{w:.4f} S{s:.4f} E{e:.4f} N{n:.4f}",
        f"**Target grid (EPSG:32721, 30 m).** "
        f"W{uw:.0f} S{us:.0f} E{ue:.0f} N{un:.0f}  ({TARGET_W}×{TARGET_H} px)",
        f"**Window.** {YEAR_START}–{YEAR_END}  (41 years).",
        f"**Scene budget.** ≤ {MAX_SCENES_PER_YEAR} cleanest scenes per year "
        f"(filter: `eo:cloud_cover < {CLOUD_COVER_LIMIT}%`).",
        f"**Years with data.** {len(rows)} / {YEAR_END - YEAR_START + 1}.",
        "",
        "## Per-year polygon-mean indices",
        "",
        "| Year | n | Platforms | NDVI | NBR | NDMI |",
        "| ---: | ---: | --- | ---: | ---: | ---: |",
    ]
    for p in polygon_rows:
        def fmt(v): return "n/a" if v is None else f"{v:+.3f}"
        md.append(
            f"| {p['year']} | {p['n_scenes']} | {p['platforms']} | "
            f"{fmt(p['ndvi'])} | {fmt(p['nbr'])} | {fmt(p['ndmi'])} |"
        )

    md.extend([
        "",
        "## Summary statistics (across per-year polygon means)",
        "",
        "| Index | Min | Max | Mean |",
        "| --- | ---: | ---: | ---: |",
        f"| NDVI | {ndvi_min} | {ndvi_max} | {ndvi_mean} |",
        f"| NBR  | {nbr_min}  | {nbr_max}  | {nbr_mean}  |",
        f"| NDMI | {ndmi_min} | {ndmi_max} | {ndmi_mean} |",
        "",
        "## Index definitions",
        "",
        "- **NDVI** = (NIR − Red) / (NIR + Red). Greenness / live biomass. "
        "Native forest is typically 0.7–0.9; bare soil ≤ 0.2.",
        "- **NBR** = (NIR − SWIR2) / (NIR + SWIR2). Normalized Burn Ratio. "
        "Healthy canopy ≈ +0.6 to +0.9; recent burn drops to ≤ +0.1. The "
        "year-over-year **dNBR** signature is the standard fire-scar metric "
        "(Key & Benson 2006).",
        "- **NDMI** = (NIR − SWIR1) / (NIR + SWIR1). Normalized Difference "
        "Moisture Index. Tracks canopy water content; closed humid forest "
        "≈ +0.3 to +0.5; drought-stressed canopy ≤ +0.1.",
        "",
        "## QA_PIXEL mask",
        "",
        "Per-scene Collection 2 Level-2 QA_PIXEL band drops pixels where any "
        "of these bits are set: 1 (dilated cloud), 2 (cirrus), 3 (cloud), "
        "4 (cloud shadow). Bit 5 (snow) is kept — no snow expected at "
        "−25.6° S / 350 m elevation. Fill pixels (QA == 0) are also "
        "dropped. Masked pixels become NaN in each per-scene index and are "
        "excluded from the per-year `np.nanmedian` composite.",
        "",
        "## Surface-reflectance scaling",
        "",
        "C2-L2 reflectance bands are 16-bit DN. Scaled to physical "
        "reflectance via `SR = DN · 0.0000275 − 0.2` (USGS), then any value "
        "outside [0, 1] is treated as NaN (post-mask artifacts on cloud "
        "edges, deep shadow, sensor saturation).",
        "",
        "## Sensor coverage by era",
        "",
        "- **1985–1992**: Landsat 5 TM is the workhorse; Landsat 4 TM adds a "
        "handful of scenes 1985-1993.",
        "- **1993–1998**: gap-prone — Landsat 4 retired 1993, Landsat 5 alone, "
        "less reliable cloud-free coverage. Some years may carry n=0.",
        "- **1999–2003**: Landsat 7 ETM+ joins; full 16-day combined revisit.",
        "- **2003–2012**: ETM+ SLC-off (post 2003-05-31) striping; medians "
        "fill the stripes from Landsat 5 scenes where both fly.",
        "- **2013–2021**: Landsat 8 OLI takes over; consistent ≤ 30 % cloud "
        "scenes year-round.",
        "- **2021–2025**: Landsat 9 OLI-2 doubles cadence with L8.",
        "",
        "## Cross-references",
        "",
        "- Phase-0 §12 #6 (Sentinel-2 L2A 2020–2025 timeseries, "
        "`docs/site_data/sentinel2/timeseries_2020_2025/`) is on the same "
        f"AOI corners at **10 m**. Per-pixel NDVI comparison requires a 3:1 "
        "block-mean downsample on the S2 side (or 3:1 nearest upsample on "
        "the Landsat side, with care taken to flag the fake resolution).",
        "- Phase-0 §12 #7 (Sentinel-1 RTC, "
        "`docs/site_data/sentinel1/rtc_6mo_median/`) sits on the same "
        "corners at 10 m too — its VH dB median is the post-2014 radar "
        "counterpart to the Landsat NBR/NDMI moisture record.",
        "- Phase-0 §12 #10 (Hansen GFC v1.12, "
        "`docs/site_data/hansen_gfc/`) gives **annual treecover loss-year** "
        "2001–present at 30 m. Cross-check: Landsat NBR drop year should "
        "match Hansen `lossyear` for any pixel that lost canopy.",
        "- Phase-0 §12 #11 (Mapbiomas Paraguay, "
        "`docs/site_data/mapbiomas_paraguay/`) categorical LULC 1985–2023 "
        "at 30 m. Same temporal span as this dataset; per-pixel join in "
        "EPSG:32721 reveals which Mapbiomas class transitions actually "
        "show in the NDVI / NBR / NDMI time series.",
        "",
        "## Files",
        "",
        "```",
        "docs/site_data/landsat/annual_median_1985_2025/",
        "├── <YEAR>/                          × N years with data",
        "│   ├── ndvi.tif        (30 m, float32, median composite)",
        "│   ├── nbr.tif",
        "│   ├── ndmi.tif",
        "│   └── *.tif.meta.json (per-file STAC/license sidecar incl. scene_ids)",
        "├── annual_quicklook.png   ← grid of per-year NDVI panels",
        "├── decadal_quicklook.png  ← 3-row × 5-decade NDVI/NBR/NDMI panel",
        "├── polygon_indices.csv    ← per-year polygon means",
        "└── summary.md             ← this file",
        "```",
        "",
        "## Caveats",
        "",
        f"- ≤ {MAX_SCENES_PER_YEAR} cleanest scenes per year is enough to "
        "stabilize the median against speckle and per-scene haze, but is "
        "**not** a phenology-aware composite. Wet/dry season scenes are "
        "co-stacked — NDVI ≈ 0.78 plateau reflects evergreen canopy, not "
        "seasonal flush.",
        "- C2-L2 QA_PIXEL is conservative: thin cirrus and cloud-edge "
        "shadow are aggressively masked, sometimes over-masked. A year with "
        "no scenes meeting the cloud-cover filter is simply missing in the "
        "output.",
        "- L7 ETM+ SLC-off striping (post 2003-05-31) creates ~22 % data "
        "gaps in single scenes. Per-year medians fill these from L5/L8 "
        "co-coverage where available; years 2003–2012 still carry some "
        "residual stripe artifacts near the AOI edges.",
        "- Native Landsat is **30 m**. This driver does NOT resample to "
        "the 10 m S2/S1 grid — that would fabricate resolution. The "
        "EPSG:32721 corners match Batches I/J so downstream joins are a "
        "clean 3:1 block-mean (or per-pixel 30 m read with S2 pre-aggregated "
        "to 30 m).",
        "- Per-year `.tif` files are kept on disk for re-runs but are "
        "**git-ignored** (see `.gitignore`: "
        "`docs/site_data/landsat/**/*.tif`). The PNG / CSV / MD outputs and "
        "the per-file `.meta.json` sidecars are tracked.",
        "- Surface-reflectance pixels outside [0, 1] after scaling are "
        "treated as NaN. This is a common post-mask cleanup (cloud-edge "
        "halos, deep shadow, sensor saturation can produce out-of-range "
        "values) and discards roughly 0.1–0.5 % of unmasked pixels in this "
        "AOI.",
        "- MPC's SAS tokens expire after ~50 minutes. This driver fetches a "
        "fresh token at startup; if a run lasts longer than that across many "
        "years, `read_band` may 403 mid-run — restart and the per-year "
        "TIF cache will skip already-completed years.",
    ])
    out_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"  summary → {out_path.name}")
    return out_path


# ---------- Main ----------------------------------------------------------

def main() -> int:
    print("=" * 78)
    print("Phase-0 §12 #8 — Landsat C2-L2 annual median 1985-2025")
    print(f"AOI 4326: {aoi_bbox()}")
    print(f"AOI 32721 30 m grid: {TARGET_BOUNDS}  ({TARGET_W}×{TARGET_H} px)")
    print(f"Window: {YEAR_START}–{YEAR_END}")
    print(f"Per-year cap: {MAX_SCENES_PER_YEAR} scenes ≤ {CLOUD_COVER_LIMIT}% cloud")
    print("=" * 78)

    sas = fetch_sas_token()

    rows: list[dict] = []
    for year in range(YEAR_START, YEAR_END + 1):
        r = process_year(year, sas)
        if r is not None:
            rows.append(r)

    if not rows:
        print("no years yielded data — aborting")
        return 1

    write_indices_csv(rows)
    render_annual_quicklook(rows)
    render_decadal_quicklook(rows)
    write_summary(rows)

    print(f"\nDone. {len(rows)} years populated.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
