#!/usr/bin/env python3
"""Phase-0 §12 #7: Sentinel-1 SAR RTC VV/VH 6-month median over the 62 ha LQV
bbox. STAC-searches Microsoft Planetary Computer for descending-orbit S1 RTC
scenes (gamma0, terrain-corrected, 10 m COG) in the most recent 6-month window,
fetches a fresh SAS token, clip-reads VV+VH through /vsicurl/+WarpedVRT to the
same EPSG:32721 10 m grid as Batch I (S2), converts gamma0-linear → dB, builds
np.nanmedian composites, renders a 3-panel quicklook (VV_dB, VH_dB, RGB
false-color), writes per-scene polygon-mean CSV + summary.md.

Outputs under docs/site_data/sentinel1/rtc_6mo_median/:
  - <SCENE_ID>/vv.tif, vh.tif           ← AOI-clipped 10 m, gamma0-linear COG
  - <SCENE_ID>/*.tif.meta.json          ← per-file STAC/license sidecar
  - sar_quicklook.png                   ← 3-panel VV_dB + VH_dB + RGB false-color
  - polygon_indices.csv                 ← per-scene polygon means (dB)
  - summary.md                          ← narrative + cross-link to §12 #6 (S2)
"""

from __future__ import annotations

import csv
import sys
import time
from datetime import datetime, timedelta, timezone
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

OUT = ROOT / "docs" / "site_data" / "sentinel1" / "rtc_6mo_median"
OUT.mkdir(parents=True, exist_ok=True)

STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
SAS_URL = "https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-1-rtc"
COLLECTION = "sentinel-1-rtc"
LICENSE_ID = "CC-BY-4.0"
CITATION = (
    "Contains modified Copernicus Sentinel-1 data, processed to Radiometrically "
    "Terrain Corrected gamma0 (sentinel-1-rtc) by Microsoft Planetary Computer."
)
FETCHER = "scripts.phase0_sentinel1_sar_batch"

POLARIZATIONS = ("vv", "vh")

# Most recent ~6 months ending today (2026-06-29 at session time). Held constant
# at module load so reruns are reproducible from sidecars.
NOW = datetime.now(timezone.utc)
END = NOW.replace(hour=23, minute=59, second=59, microsecond=0)
START = (END - timedelta(days=183)).replace(hour=0, minute=0, second=0, microsecond=0)

# Pin the orbit pass so all scenes share viewing geometry; descending @ relative
# orbit 68 is the consistent S1A/S1C pass over LQV (verified Q4 2025 probes).
ORBIT_STATE = "descending"
RELATIVE_ORBIT = 68

CANONICAL_CRS = "EPSG:32721"
GRID_M = 10.0


# ---------- AOI target grid (canonical UTM 21S, 10 m) ---------------------

def aoi_target_grid() -> tuple[tuple[float, float, float, float], int, int, object]:
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


TARGET_BOUNDS, TARGET_W, TARGET_H, TARGET_TR = aoi_target_grid()


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


def search_window(start: datetime, end: datetime) -> list[dict]:
    """All descending-orbit S1 RTC scenes in the window that cover the AOI."""
    w, s, e, n = aoi_bbox()
    body = {
        "collections": [COLLECTION],
        "bbox": [w, s, e, n],
        "datetime": f"{start.isoformat()}/{end.isoformat()}",
        "query": {
            "sat:orbit_state": {"eq": ORBIT_STATE},
            "sat:relative_orbit": {"eq": RELATIVE_ORBIT},
            "sar:polarizations": {"eq": ["VV", "VH"]},
        },
        "limit": 100,
    }
    js = _stac_post(body)
    feats = js.get("features", [])

    def covers(f: dict) -> bool:
        b = f.get("bbox") or []
        if len(b) < 4:
            return False
        return b[0] <= w and b[1] <= s and b[2] >= e and b[3] >= n

    feats = [f for f in feats if covers(f)]
    feats.sort(key=lambda f: f["properties"].get("datetime", ""))
    return feats


# ---------- Per-band clip-on-read ----------------------------------------

@with_retry()
def clip_band(href: str, out_path: Path, *, item_id: str, polarization: str,
              orbit_state: str, relative_orbit: int, scene_dt: str) -> Path:
    if skip_if_exists(out_path, min_bytes=1024):
        return out_path
    assert_compatible(LICENSE_ID)
    src_url = href if href.startswith("/vsicurl/") else f"/vsicurl/{href}"
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
                resampling=Resampling.bilinear,
            ) as vrt:
                data = vrt.read(1)
                profile = {
                    "driver": "GTiff",
                    "height": TARGET_H,
                    "width": TARGET_W,
                    "count": 1,
                    "dtype": vrt.dtypes[0],
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
    print(f"    {polarization:3s} {out_path.stat().st_size // 1024} KB ({time.time()-t0:.1f}s)")
    write_sidecar(
        out_path,
        # Strip SAS query string from sidecar source so it isn't recorded.
        source=href.split("?", 1)[0],
        collection=COLLECTION,
        license_id=LICENSE_ID,
        citation=CITATION,
        fetcher=FETCHER,
        extra={
            "item_id": item_id,
            "polarization": polarization,
            "orbit_state": orbit_state,
            "relative_orbit": relative_orbit,
            "datetime": scene_dt,
            "units": "gamma0_linear_power",
            "target_crs": CANONICAL_CRS,
            "target_bounds_utm21s": list(TARGET_BOUNDS),
        },
    )
    return out_path


def process_scene(feat: dict, sas: str) -> dict | None:
    item_id = feat["id"]
    props = feat["properties"]
    dt_iso = props.get("datetime", "")
    date_iso = dt_iso[:10]
    orbit_state = props.get("sat:orbit_state", ORBIT_STATE)
    rel_orbit = props.get("sat:relative_orbit", RELATIVE_ORBIT)
    assets = feat.get("assets", {})

    scene_dir = OUT / item_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    print(f"  {item_id}  {date_iso}  orbit={orbit_state}/{rel_orbit}")
    out: dict[str, Path] = {}
    for pol in POLARIZATIONS:
        if pol not in assets:
            print(f"    {pol} MISSING from STAC assets — skipping scene")
            return None
        href = signed_href(assets[pol]["href"], sas)
        out_path = scene_dir / f"{pol}.tif"
        try:
            clip_band(href, out_path,
                      item_id=item_id, polarization=pol,
                      orbit_state=orbit_state, relative_orbit=rel_orbit,
                      scene_dt=dt_iso)
            out[pol] = out_path
        except Exception as exc:
            print(f"    {pol} FAILED: {type(exc).__name__}: {str(exc)[:100]}")
            return None
    return {"item_id": item_id, "date": date_iso,
            "orbit_state": orbit_state, "relative_orbit": rel_orbit,
            "bands": out}


# ---------- Indices in dB --------------------------------------------------

def load_scene_arrays(bands: dict[str, Path]) -> dict[str, np.ndarray]:
    out = {}
    for b, p in bands.items():
        with rasterio.open(p) as src:
            out[b] = src.read(1)
    return out


def linear_to_db(arr: np.ndarray) -> np.ndarray:
    """gamma0 linear power → dB. Zeros and negatives become NaN."""
    a = arr.astype(np.float32)
    a = np.where(a > 0.0, a, np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        db = 10.0 * np.log10(a)
    return db.astype(np.float32)


def compute_polarizations_db(arrs: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    vv_db = linear_to_db(arrs["vv"])
    vh_db = linear_to_db(arrs["vh"])
    diff = (vv_db - vh_db).astype(np.float32)
    return {"vv_db": vv_db, "vh_db": vh_db, "vv_minus_vh": diff}


# ---------- Median composite + 3-panel quicklook ------------------------

def median_stack(per_scene_db: list[dict[str, np.ndarray]]) -> dict[str, np.ndarray]:
    keys = ("vv_db", "vh_db", "vv_minus_vh")
    out = {}
    for k in keys:
        stack = np.stack([s[k] for s in per_scene_db], axis=0)
        with np.errstate(all="ignore"):
            out[k] = np.nanmedian(stack, axis=0).astype(np.float32)
    return out


def _norm(arr: np.ndarray, vmin: float, vmax: float) -> np.ndarray:
    out = (arr - vmin) / (vmax - vmin)
    return np.clip(np.nan_to_num(out, nan=0.0), 0.0, 1.0)


def render_quicklook(med: dict[str, np.ndarray], n_scenes: int) -> Path:
    out_path = OUT / "sar_quicklook.png"
    uw, us, ue, un = TARGET_BOUNDS
    extent = (uw, ue, us, un)

    # Sentinel-1 forest-typical ranges: VV roughly -12..-4 dB, VH roughly
    # -20..-10 dB; ratio roughly 4..10 dB. Clamp for the false-color render.
    rgb = np.stack([
        _norm(med["vv_db"],       -18.0, -2.0),
        _norm(med["vh_db"],       -25.0, -8.0),
        _norm(med["vv_minus_vh"],   3.0, 12.0),
    ], axis=-1)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=140)
    panels = [
        ("VV median (dB)",  med["vv_db"], "gray",  -20.0, -2.0),
        ("VH median (dB)",  med["vh_db"], "gray",  -25.0, -6.0),
        ("RGB (R=VV, G=VH, B=VV−VH)", rgb, None, None, None),
    ]
    for ax, (title, data, cmap, vmin, vmax) in zip(axes, panels):
        if cmap is None:
            ax.imshow(data, extent=extent, origin="upper")
        else:
            im = ax.imshow(data, extent=extent, origin="upper",
                           cmap=cmap, vmin=vmin, vmax=vmax)
            fig.colorbar(im, ax=ax, shrink=0.7, label="dB")
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("Easting (m, UTM 21S)")
        ax.set_ylabel("Northing (m, UTM 21S)")
        ax.set_aspect("equal")
    fig.suptitle(
        f"Sentinel-1 RTC {n_scenes}-scene median, "
        f"{START.date()} → {END.date()} — La Quebrada Viva 62 ha AOI",
        fontsize=13,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  quicklook → {out_path.name}")
    return out_path


# ---------- Per-scene polygon-mean CSV ----------------------------------

def write_indices_csv(rows: list[dict]) -> Path:
    out_path = OUT / "polygon_indices.csv"
    cols = ["date", "scene_id", "orbit_state", "relative_orbit",
            "valid_pixels", "vv_db_mean", "vh_db_mean", "vv_minus_vh_mean"]
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"  csv → {out_path.name} ({len(rows)} scenes)")
    return out_path


# ---------- Markdown summary -------------------------------------------

def write_summary(rows: list[dict]) -> Path:
    out_path = OUT / "summary.md"
    vv_vals = [r["vv_db_mean"] for r in rows if r["vv_db_mean"] is not None]
    vh_vals = [r["vh_db_mean"] for r in rows if r["vh_db_mean"] is not None]
    rat_vals = [r["vv_minus_vh_mean"] for r in rows if r["vv_minus_vh_mean"] is not None]

    def mm(vals):
        if not vals:
            return ("n/a", "n/a", "n/a")
        return (f"{min(vals):+.2f}", f"{max(vals):+.2f}",
                f"{sum(vals)/len(vals):+.2f}")

    vv_min, vv_max, vv_mean = mm(vv_vals)
    vh_min, vh_max, vh_mean = mm(vh_vals)
    rat_min, rat_max, rat_mean = mm(rat_vals)

    w, s, e, n = aoi_bbox()
    uw, us, ue, un = TARGET_BOUNDS

    md = [
        "# Sentinel-1 RTC 6-month SAR median — Phase-0 §12 #7",
        "",
        "**Source.** Microsoft Planetary Computer STAC, collection "
        f"`{COLLECTION}` (Copernicus Sentinel-1 GRD, Radiometrically Terrain "
        "Corrected to gamma0 by Microsoft, 10 m COG).",
        f"**License.** {LICENSE_ID} (ESA Sentinel Legal Notice ≈ CC-BY-4.0).",
        f"**AOI bbox (EPSG:4326).** W{w:.4f} S{s:.4f} E{e:.4f} N{n:.4f}",
        f"**Target grid (EPSG:32721, 10 m).** "
        f"W{uw:.0f} S{us:.0f} E{ue:.0f} N{un:.0f}  ({TARGET_W}×{TARGET_H} px)",
        f"**Window.** {START.date()} → {END.date()}  (~6 months).",
        f"**Pass geometry.** {ORBIT_STATE} pass, relative orbit {RELATIVE_ORBIT}, "
        "IW mode, VV+VH dual-pol — pinned so every scene shares viewing geometry.",
        f"**Scenes resolved.** {len(rows)}.",
        "",
        "## Per-scene polygon-mean backscatter (dB)",
        "",
        "| Date | Scene | Orbit | VV (dB) | VH (dB) | VV−VH (dB) |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]
    for r in rows:
        def fmt(v): return "n/a" if v is None else f"{v:+.2f}"
        md.append(
            f"| {r['date']} | `{r['scene_id']}` | "
            f"{r['orbit_state'][:4]}/{r['relative_orbit']} | "
            f"{fmt(r['vv_db_mean'])} | {fmt(r['vh_db_mean'])} | "
            f"{fmt(r['vv_minus_vh_mean'])} |"
        )

    md.extend([
        "",
        "## Summary statistics (across per-scene polygon means)",
        "",
        "| Quantity | Min | Max | Mean |",
        "| --- | ---: | ---: | ---: |",
        f"| VV (dB)    | {vv_min}   | {vv_max}   | {vv_mean}   |",
        f"| VH (dB)    | {vh_min}   | {vh_max}   | {vh_mean}   |",
        f"| VV−VH (dB) | {rat_min}  | {rat_max}  | {rat_mean}  |",
        "",
        "## What the polarizations measure",
        "",
        "- **VV** (vertical send / vertical receive). Dominant scatterers: bare "
        "soil roughness, water surface (specular = very dark), urban double-"
        "bounce (very bright). Forest VV is intermediate (~−7 to −10 dB) and "
        "fairly stable.",
        "- **VH** (vertical send / horizontal receive). Cross-pol; sensitive to "
        "volume scattering inside a canopy. Dense forest VH is typically "
        "−12 to −16 dB; bare ground/water is <−20 dB. **VH is the cleanest "
        "single-band proxy for canopy density** at C-band.",
        "- **VV − VH (dB)** = cross-pol ratio in dB. Smooth surfaces (water, "
        "bare soil) → large ratio (>8 dB) because VV dominates. Volume "
        "scatterers (forest) → small ratio (3–6 dB) because VH catches up. "
        "Practical water-mask is VV<−15 dB AND ratio>10 dB.",
        "",
        "## RTC = gamma0, not sigma0",
        "",
        "Microsoft Planetary Computer's `sentinel-1-rtc` collection is "
        "**Radiometrically Terrain Corrected** to gamma0. The terrain "
        "correction divides backscatter by the local illuminated area derived "
        "from a Copernicus DEM, removing topographic distortion of brightness "
        "— so a forested slope and a forested flat give comparable values. "
        "Values stored are **gamma0 linear power**; this driver converts to dB "
        "(`10·log10(γ⁰)`) before any per-pixel comparison.",
        "",
        "## Cross-references",
        "",
        "- Phase-0 §12 #6 (Sentinel-2 L2A timeseries, "
        "`docs/site_data/sentinel2/timeseries_2020_2025/`) is on the **same** "
        "302×334 EPSG:32721 10 m grid. Per-pixel S2 NDVI median (optical "
        "canopy density) and S1 VH median (radar volume scatter) can be "
        "differenced/regressed without resampling. Expect them to correlate "
        "positively across the 62 ha.",
        "- Phase-0 §12 #10 (Hansen GFC, `docs/site_data/hansen_gfc/`) gives "
        "continuous treecover2000 / loss-year on a 30 m grid — VH median "
        "should track treecover2000 within the same parcel.",
        "- Phase-0 §12 #12 (JRC GSW, `docs/site_data/jrc_gsw/`) gives surface-"
        "water occurrence; SAR water-mask (VV<−15 dB AND ratio>10 dB) is the "
        "high-res LQV-only counterpart. No persistent open water expected "
        "inside the 62 ha bbox — see Batch I AWEIsh result.",
        "",
        "## Files",
        "",
        "```",
        "docs/site_data/sentinel1/rtc_6mo_median/",
        "├── <SCENE_ID>/                     × N scenes",
        "│   ├── vv.tif        (10 m, gamma0 linear power, float32)",
        "│   ├── vh.tif",
        "│   └── *.tif.meta.json (per-file STAC/license sidecar)",
        "├── sar_quicklook.png    ← 3-panel VV_dB + VH_dB + RGB false-color",
        "├── polygon_indices.csv  ← per-scene polygon means (dB)",
        "└── summary.md           ← this file",
        "```",
        "",
        "## Caveats",
        "",
        f"- The window is the most recent ~6 months ending {END.date()}; "
        "regenerate against a different window by editing `START`/`END` in the "
        "driver. Pinning to descending / relative orbit "
        f"{RELATIVE_ORBIT} forces consistent viewing geometry but caps the "
        "scene count at the ~12-day revisit cadence (≈ 15 scenes / 6 months).",
        "- Speckle is **not** filtered here. Per-scene values include "
        "salt-and-pepper noise inherent to single-look SAR; the 6-scene "
        "`np.nanmedian` stack is the speckle suppressor. Don't read single-"
        "pixel values from the per-scene `.tif`s.",
        "- Microsoft's RTC uses the Copernicus DEM (30 m globally; 10 m where "
        "available, which does **not** include Paraguay). Steep slope artifacts "
        "may persist near the escarpment in the SE — visual-cross-check "
        "against the Cop30 hillshade in §12 #5.",
        "- Per-scene `.tif` files are kept on disk for re-runs but are "
        "**git-ignored** (see `.gitignore`: "
        "`docs/site_data/sentinel1/**/*.tif`). The PNG / CSV / MD outputs and "
        "the per-file `.meta.json` sidecars are tracked.",
        "- MPC's SAS tokens expire after ~50 minutes. This driver fetches a "
        "fresh token at startup; if a run lasts longer than that across many "
        "scenes, `clip_band` may 403 mid-run — restart and the cached scenes "
        "will be skipped via `skip_if_exists`.",
    ])
    out_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"  summary → {out_path.name}")
    return out_path


# ---------- Main --------------------------------------------------------

def main() -> int:
    print("=" * 78)
    print("Phase-0 §12 #7 — Sentinel-1 RTC VV/VH 6-month median")
    print(f"AOI 4326: {aoi_bbox()}")
    print(f"AOI 32721 grid: {TARGET_BOUNDS}  ({TARGET_W}×{TARGET_H} px @ 10 m)")
    print(f"Window: {START.date()} → {END.date()}")
    print(f"Pass: {ORBIT_STATE} / relative_orbit={RELATIVE_ORBIT}")
    print("=" * 78)

    feats = search_window(START, END)
    print(f"STAC returned {len(feats)} covering scenes")
    if not feats:
        print("no scenes — aborting")
        return 1

    sas = fetch_sas_token()

    scenes: list[dict] = []
    for feat in feats:
        sc = process_scene(feat, sas)
        if sc is not None:
            scenes.append(sc)

    if not scenes:
        print("no scenes successfully fetched — aborting")
        return 1

    per_scene_db: list[dict[str, np.ndarray]] = []
    csv_rows: list[dict] = []
    for sc in scenes:
        arrs = load_scene_arrays(sc["bands"])
        db = compute_polarizations_db(arrs)
        per_scene_db.append(db)

        valid = np.isfinite(db["vv_db"]) & np.isfinite(db["vh_db"])
        valid_pixels = int(valid.sum())

        def m(name):
            v = db[name]
            v = v[np.isfinite(v)]
            return float(np.nanmean(v)) if v.size else None

        csv_rows.append({
            "date": sc["date"],
            "scene_id": sc["item_id"],
            "orbit_state": sc["orbit_state"],
            "relative_orbit": sc["relative_orbit"],
            "valid_pixels": valid_pixels,
            "vv_db_mean": m("vv_db"),
            "vh_db_mean": m("vh_db"),
            "vv_minus_vh_mean": m("vv_minus_vh"),
        })

    write_indices_csv(csv_rows)

    med = median_stack(per_scene_db)
    render_quicklook(med, n_scenes=len(scenes))

    write_summary(csv_rows)

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
