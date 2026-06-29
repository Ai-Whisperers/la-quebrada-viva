#!/usr/bin/env python3
"""Phase-0 §12 #9: ALOS-2 PALSAR-2 25 m annual mosaic 2015-2020 HH+HV gamma0
over the 62 ha LQV bbox. Microsoft Planetary Computer's `alos-palsar-mosaic`
holds the JAXA EORC global L-band mosaic — annual tiles, HH+HV dual-pol DN,
mask asset (water/lay-over/shadow/land/no-data). The collection covers the
ALOS-2 era (2015-2020 inclusive on MPC) only; the 2007-2010 ALOS-1 PALSAR
mosaic is not exposed here and is queued as a follow-up batch.

L-band (~23.6 cm) penetrates canopy deeper than C-band Sentinel-1 (~5.6 cm) —
HV cross-pol is the standard above-ground biomass proxy for the Atlantic
Forest remnants on the property, complementing the S1 RTC volume-scatter
record (§12 #7) and the Landsat NBR/NDMI record (§12 #8).

Outputs under docs/site_data/alos_palsar/annual_mosaic_2015_2020/:
  - <YEAR>/hh.tif, hv.tif               ← per-year γ⁰ in dB, float32, NaN nodata
  - <YEAR>/mask_landfrac.tif            ← per-year land-pixel fraction (0..1)
  - <YEAR>/*.tif.meta.json              ← per-file STAC/license sidecar
  - annual_quicklook.png                ← 6-year HH + HV + RGB grid
  - polygon_indices.csv                 ← per-year polygon means (dB)
  - summary.md                          ← narrative + cross-links

JAXA DN→γ⁰: γ⁰[dB] = 10·log10(DN²) − 83.0, with DN==0 = no-data (JAXA EORC
ALOS-2 PALSAR-2 Global 25 m Mosaic User's Guide, formula not in MPC metadata
so it's hard-coded here and recorded in the sidecar `extra`).
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

OUT = ROOT / "docs" / "site_data" / "alos_palsar" / "annual_mosaic_2015_2020"
OUT.mkdir(parents=True, exist_ok=True)

STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
SAS_URL = "https://planetarycomputer.microsoft.com/api/sas/v1/token/alos-palsar-mosaic"
COLLECTION = "alos-palsar-mosaic"
LICENSE_ID = "JAXA-EORC"
CITATION = (
    "© JAXA EORC ALOS-2 PALSAR-2 Global 25 m Mosaic (2015-2020). "
    "Distributed by Microsoft Planetary Computer (alos-palsar-mosaic). "
    "DN→γ⁰ conversion per JAXA EORC user's guide: γ⁰[dB] = 10·log10(DN²) − 83.0."
)
FETCHER = "scripts.phase0_alos_palsar_batch"

POLARIZATIONS = ("HH", "HV")
YEAR_START = 2015
YEAR_END = 2020

CANONICAL_CRS = "EPSG:32721"
GRID_M = 25.0

# JAXA EORC PALSAR mosaic mask asset class codes. The MPC item-asset metadata
# enumerates these as: 0=no_data, 50=water, 100=lay_over, 150=shadowing,
# 255=land. We keep land only (treat everything else as no-data NaN).
MASK_LAND = 255

# JAXA DN→γ⁰ calibration constant (Shimada et al. 2009; reiterated in the
# ALOS-2 PALSAR-2 Global 25 m Mosaic User's Guide v.2.4).
JAXA_CF_DB = -83.0


# ---------- AOI target grid (canonical UTM 21S, 25 m) ---------------------

def aoi_target_grid_25m() -> tuple[tuple[float, float, float, float], int, int, object]:
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


TARGET_BOUNDS, TARGET_W, TARGET_H, TARGET_TR = aoi_target_grid_25m()


# ---------- MPC SAS token ------------------------------------------------

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


# ---------- STAC search --------------------------------------------------

@with_retry()
def _stac_post(body: dict) -> dict:
    r = requests.post(STAC_URL, json=body, timeout=60)
    r.raise_for_status()
    return r.json()


def search_year(year: int) -> list[dict]:
    """Return all mosaic tiles whose footprint intersects the AOI for `year`."""
    w, s, e, n = aoi_bbox()
    body = {
        "collections": [COLLECTION],
        "bbox": [w, s, e, n],
        "datetime": f"{year}-01-01T00:00:00Z/{year}-12-31T23:59:59Z",
        "limit": 50,
    }
    js = _stac_post(body)
    feats = js.get("features", [])
    feats.sort(key=lambda f: f["id"])
    return feats


# ---------- Per-band clip-on-read ---------------------------------------

@with_retry()
def read_band(href: str, *, resampling: Resampling) -> np.ndarray:
    """Open a remote PALSAR mosaic asset and reproject onto the canonical grid."""
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


def dn_to_gamma0_db(dn: np.ndarray) -> np.ndarray:
    """γ⁰[dB] = 10·log10(DN²) − 83.0; DN==0 (no-data) → NaN."""
    a = dn.astype(np.float32)
    a = np.where(a > 0.0, a, np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        db = 10.0 * np.log10(a * a) + JAXA_CF_DB
    return db.astype(np.float32)


# ---------- Per-year processor ------------------------------------------

def write_year_tif(out_path: Path, data: np.ndarray, *, units: str,
                   nodata, dtype: str) -> Path:
    profile = {
        "driver": "GTiff",
        "height": TARGET_H,
        "width": TARGET_W,
        "count": 1,
        "dtype": dtype,
        "crs": CANONICAL_CRS,
        "transform": TARGET_TR,
        "compress": "deflate",
        "tiled": True,
        "blockxsize": 64,
        "blockysize": 64,
        "nodata": nodata,
    }
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    with rasterio.open(tmp, "w", **profile) as dst:
        dst.write(data.astype(dtype), 1)
        dst.update_tags(units=units)
    tmp.replace(out_path)
    return out_path


def process_year(year: int, sas: str) -> dict | None:
    year_dir = OUT / str(year)
    year_dir.mkdir(parents=True, exist_ok=True)
    hh_path = year_dir / "hh.tif"
    hv_path = year_dir / "hv.tif"
    landfrac_path = year_dir / "mask_landfrac.tif"

    # Cache hit — read polygon means out of the cached arrays.
    if hh_path.exists() and hv_path.exists() and landfrac_path.exists():
        with rasterio.open(hh_path) as src:
            hh_db = src.read(1)
            tags = src.tags()
        with rasterio.open(hv_path) as src:
            hv_db = src.read(1)
        with rasterio.open(landfrac_path) as src:
            landfrac = src.read(1)
        n_tiles = int(tags.get("n_tiles", "0") or 0)
        tile_ids = tags.get("tile_ids", "").split("|") if tags.get("tile_ids") else []
        return {
            "year": year,
            "n_tiles": n_tiles,
            "tile_ids": tile_ids,
            "hh_db": hh_db,
            "hv_db": hv_db,
            "landfrac": landfrac,
            "cached": True,
        }

    feats = search_year(year)
    if not feats:
        print(f"  {year}: STAC returned 0 tiles — skipping")
        return None

    assert_compatible(LICENSE_ID)
    hh_db_tiles: list[np.ndarray] = []
    hv_db_tiles: list[np.ndarray] = []
    land_tiles: list[np.ndarray] = []
    tile_ids: list[str] = []

    for feat in feats:
        item_id = feat["id"]
        assets = feat.get("assets", {})
        a_hh = assets.get("HH") or assets.get("hh")
        a_hv = assets.get("HV") or assets.get("hv")
        a_mask = assets.get("mask")
        if not (a_hh and a_hv and a_mask):
            print(f"    {item_id}: missing HH/HV/mask asset — skipping tile")
            continue

        t0 = time.time()
        try:
            hh_dn = read_band(signed_href(a_hh["href"], sas),
                              resampling=Resampling.bilinear)
            hv_dn = read_band(signed_href(a_hv["href"], sas),
                              resampling=Resampling.bilinear)
            mask = read_band(signed_href(a_mask["href"], sas),
                             resampling=Resampling.nearest)
        except Exception as exc:
            print(f"    {item_id} FAILED: {type(exc).__name__}: "
                  f"{str(exc)[:120]} — skipping tile")
            continue

        land = (mask == MASK_LAND).astype(np.float32)
        hh_db = dn_to_gamma0_db(hh_dn)
        hv_db = dn_to_gamma0_db(hv_dn)
        # Drop non-land pixels (water, lay-over, shadow, no-data) to NaN.
        hh_db = np.where(land > 0.5, hh_db, np.nan)
        hv_db = np.where(land > 0.5, hv_db, np.nan)

        hh_db_tiles.append(hh_db)
        hv_db_tiles.append(hv_db)
        land_tiles.append(land)
        tile_ids.append(item_id)
        print(f"    {item_id}: HH/HV/mask read ({time.time()-t0:.1f}s)")

    if not hh_db_tiles:
        print(f"  {year}: 0 tiles read successfully — skipping year")
        return None

    # Median across tiles. The mosaic is built tile-by-tile globally so the AOI
    # usually falls in a single 1°×1° tile — n_tiles==1 in the common case, in
    # which case the nanmedian collapses to passthrough.
    hh_stack = np.stack(hh_db_tiles, axis=0)
    hv_stack = np.stack(hv_db_tiles, axis=0)
    land_stack = np.stack(land_tiles, axis=0)
    with np.errstate(all="ignore"):
        hh_db_med = np.nanmedian(hh_stack, axis=0).astype(np.float32)
        hv_db_med = np.nanmedian(hv_stack, axis=0).astype(np.float32)
    landfrac = np.mean(land_stack, axis=0).astype(np.float32)

    write_year_tif(hh_path, hh_db_med, units="gamma0_dB",
                   nodata=float("nan"), dtype="float32")
    write_year_tif(hv_path, hv_db_med, units="gamma0_dB",
                   nodata=float("nan"), dtype="float32")
    write_year_tif(landfrac_path, landfrac, units="fraction_0_1",
                   nodata=float("nan"), dtype="float32")

    # Stamp tile_ids into a GeoTIFF tag for cache-rehydration on re-runs.
    with rasterio.open(hh_path, "r+") as src:
        src.update_tags(n_tiles=str(len(tile_ids)),
                        tile_ids="|".join(tile_ids))

    common_extra = {
        "year": year,
        "n_tiles": len(tile_ids),
        "tile_ids": tile_ids,
        "target_crs": CANONICAL_CRS,
        "target_bounds_utm21s": list(TARGET_BOUNDS),
        "grid_m": GRID_M,
        "dn_to_gamma0_db_formula": "10*log10(DN^2) + (-83.0)",
        "mask_class_kept": MASK_LAND,
    }
    write_sidecar(hh_path,
                  source=f"mpc:{COLLECTION}:{year}:HH",
                  collection=COLLECTION,
                  license_id=LICENSE_ID,
                  citation=CITATION,
                  fetcher=FETCHER,
                  extra={**common_extra, "polarization": "HH",
                         "units": "gamma0_dB"})
    write_sidecar(hv_path,
                  source=f"mpc:{COLLECTION}:{year}:HV",
                  collection=COLLECTION,
                  license_id=LICENSE_ID,
                  citation=CITATION,
                  fetcher=FETCHER,
                  extra={**common_extra, "polarization": "HV",
                         "units": "gamma0_dB"})
    write_sidecar(landfrac_path,
                  source=f"mpc:{COLLECTION}:{year}:mask",
                  collection=COLLECTION,
                  license_id=LICENSE_ID,
                  citation=CITATION,
                  fetcher=FETCHER,
                  extra={**common_extra, "polarization": "mask_landfrac",
                         "units": "fraction_0_1"})

    return {
        "year": year,
        "n_tiles": len(tile_ids),
        "tile_ids": tile_ids,
        "hh_db": hh_db_med,
        "hv_db": hv_db_med,
        "landfrac": landfrac,
        "cached": False,
    }


# ---------- Quicklook -----------------------------------------------------

def _norm(arr: np.ndarray, vmin: float, vmax: float) -> np.ndarray:
    out = (arr - vmin) / (vmax - vmin)
    return np.clip(np.nan_to_num(out, nan=0.0), 0.0, 1.0)


def render_quicklook(per_year: list[dict]) -> Path:
    out_path = OUT / "annual_quicklook.png"
    uw, us, ue, un = TARGET_BOUNDS
    extent = (uw, ue, us, un)
    n_years = len(per_year)

    fig, axes = plt.subplots(3, n_years, figsize=(2.8 * n_years, 8.2), dpi=140)
    if n_years == 1:
        axes = np.array([[ax] for ax in axes])

    for col, y in enumerate(per_year):
        rgb = np.stack([
            _norm(y["hh_db"], -18.0, -4.0),
            _norm(y["hv_db"], -22.0, -8.0),
            _norm(y["hh_db"] - y["hv_db"], 2.0, 12.0),
        ], axis=-1)
        panels = [
            ("HH γ⁰ (dB)", y["hh_db"], "gray", -20.0, -4.0),
            ("HV γ⁰ (dB)", y["hv_db"], "gray", -24.0, -8.0),
            ("RGB (R=HH, G=HV, B=HH−HV)", rgb, None, None, None),
        ]
        for row, (title, data, cmap, vmin, vmax) in enumerate(panels):
            ax = axes[row, col]
            if cmap is None:
                ax.imshow(data, extent=extent, origin="upper")
            else:
                im = ax.imshow(data, extent=extent, origin="upper",
                               cmap=cmap, vmin=vmin, vmax=vmax)
                if col == n_years - 1:
                    fig.colorbar(im, ax=ax, shrink=0.7, label="dB")
            if row == 0:
                ax.set_title(f"{y['year']}", fontsize=12, fontweight="bold")
            if col == 0:
                ax.set_ylabel(title, fontsize=10)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_aspect("equal")

    fig.suptitle(
        "ALOS-2 PALSAR-2 25 m annual mosaic — La Quebrada Viva 62 ha AOI",
        fontsize=13,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  quicklook → {out_path.name}")
    return out_path


# ---------- CSV + summary -----------------------------------------------

def write_indices_csv(rows: list[dict]) -> Path:
    out_path = OUT / "polygon_indices.csv"
    cols = ["year", "n_tiles", "valid_pixels", "land_fraction",
            "hh_db_mean", "hv_db_mean", "hh_minus_hv_mean"]
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"  csv → {out_path.name} ({len(rows)} years)")
    return out_path


def write_summary(rows: list[dict]) -> Path:
    out_path = OUT / "summary.md"
    hh_vals = [r["hh_db_mean"] for r in rows if r["hh_db_mean"] is not None]
    hv_vals = [r["hv_db_mean"] for r in rows if r["hv_db_mean"] is not None]
    ratio_vals = [r["hh_minus_hv_mean"] for r in rows
                  if r["hh_minus_hv_mean"] is not None]

    def mm(vals):
        if not vals:
            return ("n/a", "n/a", "n/a")
        return (f"{min(vals):+.2f}", f"{max(vals):+.2f}",
                f"{sum(vals)/len(vals):+.2f}")

    hh_min, hh_max, hh_mean = mm(hh_vals)
    hv_min, hv_max, hv_mean = mm(hv_vals)
    ra_min, ra_max, ra_mean = mm(ratio_vals)

    w, s, e, n = aoi_bbox()
    uw, us, ue, un = TARGET_BOUNDS

    md = [
        "# ALOS-2 PALSAR-2 25 m annual mosaic 2015–2020 — Phase-0 §12 #9",
        "",
        "**Source.** Microsoft Planetary Computer STAC, collection "
        f"`{COLLECTION}` (JAXA EORC ALOS-2 PALSAR-2 Global 25 m Mosaic; "
        "L-band SAR @ ~23.6 cm wavelength; HH+HV dual-pol DN; tile-quilted "
        "annual mosaic).",
        "**License.** JAXA-EORC (JAXA Earth Observation Research Center; "
        "free for research use; classified `unknown` by the bundle gate so "
        "raw `.tif` are git-ignored and treated as deck-only until reviewed).",
        f"**AOI bbox (EPSG:4326).** W{w:.4f} S{s:.4f} E{e:.4f} N{n:.4f}",
        f"**Target grid (EPSG:32721, 25 m).** "
        f"W{uw:.0f} S{us:.0f} E{ue:.0f} N{un:.0f}  ({TARGET_W}×{TARGET_H} px)",
        f"**Window.** {YEAR_START}–{YEAR_END}  ({YEAR_END - YEAR_START + 1} years; "
        "ALOS-2 era only — ALOS-1 PALSAR 2007-2010 is a separate JAXA dataset "
        "and is queued as a follow-up batch).",
        f"**Years with data.** {len(rows)} / {YEAR_END - YEAR_START + 1}.",
        "",
        "## Per-year polygon-mean backscatter (dB, land pixels only)",
        "",
        "| Year | n_tiles | land_frac | HH (dB) | HV (dB) | HH−HV (dB) |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in rows:
        def fmt(v): return "n/a" if v is None else f"{v:+.2f}"
        lf = "n/a" if r["land_fraction"] is None else f"{r['land_fraction']:.3f}"
        md.append(
            f"| {r['year']} | {r['n_tiles']} | {lf} | "
            f"{fmt(r['hh_db_mean'])} | {fmt(r['hv_db_mean'])} | "
            f"{fmt(r['hh_minus_hv_mean'])} |"
        )

    md.extend([
        "",
        "## Summary statistics (across per-year polygon means)",
        "",
        "| Quantity | Min | Max | Mean |",
        "| --- | ---: | ---: | ---: |",
        f"| HH (dB)    | {hh_min} | {hh_max} | {hh_mean} |",
        f"| HV (dB)    | {hv_min} | {hv_max} | {hv_mean} |",
        f"| HH−HV (dB) | {ra_min} | {ra_max} | {ra_mean} |",
        "",
        "## DN → γ⁰ conversion",
        "",
        "JAXA EORC ships PALSAR mosaic tiles as 16-bit DN. The standard "
        "calibration (Shimada et al. 2009; reiterated in the ALOS-2 PALSAR-2 "
        "Global 25 m Mosaic User's Guide v2.4) is:",
        "",
        "    γ⁰[dB] = 10·log10(DN²) − 83.0",
        "",
        "and `DN == 0` is the no-data sentinel. The MPC collection metadata "
        "does not expose this formula, so it's hard-coded in this driver and "
        "recorded in every sidecar's `extra.dn_to_gamma0_db_formula`.",
        "",
        "## Mask asset (per-pixel land flag)",
        "",
        "The `mask` asset is a per-pixel class raster with values:",
        "  • 0 = no_data,  50 = water,  100 = lay-over,  150 = shadowing,  255 = land.",
        "Only pixels classed as **land (255)** are kept; everything else "
        "becomes NaN in the per-tile γ⁰ array before the per-year median. "
        "The companion `mask_landfrac.tif` records the fraction of contributing "
        "tiles where each pixel was land — useful for filtering the per-pixel "
        "edge cases near the AOI border.",
        "",
        "## What HH/HV measure at L-band",
        "",
        "- **HH** (horizontal send / horizontal receive). Co-pol; dominated "
        "by surface scattering — rough ground, bare slopes, large trunks. "
        "Forest HH typically lands around −8 to −12 dB at L-band.",
        "- **HV** (horizontal send / vertical receive). Cross-pol; dominated "
        "by volume scattering inside the canopy. **HV is the standard L-band "
        "above-ground biomass proxy** (Mermoz et al. 2015; Bouvet et al. 2018) "
        "with forest HV near −12 to −16 dB and bare ground / water below −18 dB.",
        "- **HH − HV (dB)** = co/cross-pol ratio. Smaller for dense volume "
        "scatterers (forest, 3–6 dB) and larger for surface scatterers (water, "
        "bare soil, > 8 dB). Useful as a fire-scar / clear-cut proxy because "
        "the ratio jumps when canopy volume scatter disappears.",
        "",
        "## L-band vs. C-band (§12 #7 cross-link)",
        "",
        "L-band (~23.6 cm) penetrates much deeper into a canopy than C-band "
        "Sentinel-1 (~5.6 cm). For closed Atlantic Forest:",
        "  • C-band (S1 VH) saturates around 50 t/ha AGB.",
        "  • L-band (PALSAR HV) saturates around 100–150 t/ha AGB.",
        "So this batch is the better single-source AGB proxy on the property; "
        "the S1 record is the better seasonal-dynamic proxy (12-day revisit "
        "vs. PALSAR's once-per-year mosaic).",
        "",
        "## Cross-references",
        "",
        "- Phase-0 §12 #7 (Sentinel-1 RTC 6-month median, "
        "`docs/site_data/sentinel1/rtc_6mo_median/`) is the C-band counterpart. "
        "Both sit on EPSG:32721; a per-pixel comparison needs a 25 m → 10 m "
        "(or 10 m → 25 m block-mean) regrid. Co-located VH (C) and HV (L) "
        "tracks two depths of the canopy.",
        "- Phase-0 §12 #8 (Landsat C2-L2 annual median 1985–2025, "
        "`docs/site_data/landsat/annual_median_1985_2025/`) is the optical "
        "annual record on the same EPSG:32721 grid at 30 m. NDVI/NBR trend vs. "
        "PALSAR HV trend over 2015–2020 — divergence usually means structural "
        "loss (logging, blowdown) under unchanged greenness, or vice-versa.",
        "- Phase-0 §12 #10 (Hansen GFC v1.12, `docs/site_data/hansen_gfc/`) "
        "tree-cover loss-year at 30 m. Any PALSAR HV drop year should match a "
        "Hansen `lossyear` pixel in the same area.",
        "- Phase-0 §12 #11 (Mapbiomas Paraguay, "
        "`docs/site_data/mapbiomas_paraguay/`) categorical LULC. PALSAR HV "
        "should bin cleanly by Mapbiomas forest class.",
        "",
        "## Files",
        "",
        "```",
        "docs/site_data/alos_palsar/annual_mosaic_2015_2020/",
        f"├── <YEAR>/                          × {len(rows)} years with data",
        "│   ├── hh.tif        (25 m, float32, γ⁰ in dB, NaN nodata)",
        "│   ├── hv.tif",
        "│   ├── mask_landfrac.tif",
        "│   └── *.tif.meta.json (per-file STAC/license sidecar incl. tile_ids)",
        "├── annual_quicklook.png   ← grid of per-year HH / HV / RGB panels",
        "├── polygon_indices.csv    ← per-year polygon means",
        "└── summary.md             ← this file",
        "```",
        "",
        "## Caveats",
        "",
        "- The MPC `alos-palsar-mosaic` collection only exposes the **ALOS-2** "
        "annual mosaics (2015–2020). The earlier **ALOS-1** PALSAR global "
        "25 m mosaics (2007–2010) are a separate JAXA distribution not on MPC; "
        "a follow-up batch will pull them direct from JAXA G-Portal if "
        "credentials are wired up.",
        "- An ALOS-2 'annual mosaic' is built per JAXA from one or more passes "
        "per 1°×1° tile in that year — it is **not** a `np.nanmedian` over many "
        "scenes the way the S1 6-month median is. Year-over-year noise is "
        "inherent to the mosaic; trends should be read over ≥3 years.",
        "- L-band mosaics are sensitive to **soil moisture** (especially in HH). "
        "A given year's mosaic anchors on whichever sub-window JAXA picked for "
        "that 1°×1° tile, so a wet vs. dry year selection can shift HH by "
        "1–2 dB across the AOI without any vegetation change. HV is more robust.",
        "- DN==0 is no-data, but the JAXA mask is the authoritative class flag; "
        "we apply both and treat the union as no-data.",
        "- Per-year `.tif` files are kept on disk for re-runs but are "
        "**git-ignored** (see `.gitignore`: "
        "`docs/site_data/alos_palsar/**/*.tif`). The PNG / CSV / MD outputs "
        "and the per-file `.meta.json` sidecars are tracked.",
        "- License is JAXA EORC, which the bundle gate (`scripts/satellite/"
        "_license.py`) does not recognise — it warns and returns "
        "`classification=unknown`. Treat as deck-only until the JAXA EORC "
        "terms are reviewed and either added to the allow-list (likely the "
        "right call: it permits research and educational use) or the deck-only "
        "list.",
        "- MPC's SAS tokens expire after ~50 minutes. This driver fetches a "
        "fresh token at startup; if a run lasts longer than that, `read_band` "
        "may 403 mid-run — restart and the per-year TIF cache will skip "
        "already-completed years.",
    ])
    out_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"  summary → {out_path.name}")
    return out_path


# ---------- Main --------------------------------------------------------

def main() -> int:
    print("=" * 78)
    print("Phase-0 §12 #9 — ALOS-2 PALSAR-2 25 m annual mosaic 2015–2020")
    print(f"AOI 4326: {aoi_bbox()}")
    print(f"AOI 32721 grid: {TARGET_BOUNDS}  ({TARGET_W}×{TARGET_H} px @ 25 m)")
    print(f"Window: {YEAR_START}–{YEAR_END}")
    print("=" * 78)

    sas = fetch_sas_token()

    per_year: list[dict] = []
    csv_rows: list[dict] = []
    for year in range(YEAR_START, YEAR_END + 1):
        print(f"\n{year}:")
        y = process_year(year, sas)
        if y is None:
            csv_rows.append({
                "year": year, "n_tiles": 0, "valid_pixels": 0,
                "land_fraction": None, "hh_db_mean": None,
                "hv_db_mean": None, "hh_minus_hv_mean": None,
            })
            continue
        per_year.append(y)
        hh, hv = y["hh_db"], y["hv_db"]
        ratio = hh - hv
        valid = np.isfinite(hh) & np.isfinite(hv)
        valid_pixels = int(valid.sum())
        landfrac = float(np.nanmean(y["landfrac"])) if y["landfrac"].size else None

        def m(arr):
            v = arr[np.isfinite(arr)]
            return float(np.mean(v)) if v.size else None

        csv_rows.append({
            "year": year,
            "n_tiles": y["n_tiles"],
            "valid_pixels": valid_pixels,
            "land_fraction": landfrac,
            "hh_db_mean": m(hh),
            "hv_db_mean": m(hv),
            "hh_minus_hv_mean": m(ratio),
        })

    if not per_year:
        print("\nno years successfully processed — aborting")
        return 1

    write_indices_csv(csv_rows)
    render_quicklook(per_year)
    write_summary([r for r in csv_rows if r["hh_db_mean"] is not None])

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
