#!/usr/bin/env python3
"""Phase-0 §12.10: pull Hansen Global Forest Change v1.12 (2000–2024) for the
50 km buffer around the La Quebrada Viva polygon centroid (-57.0355, -25.6073),
clip to AOI, derive polygon-level canopy + loss + gain stats, write quicklooks.

Tile 20S_060W (upper-left corner) covers lat [-30, -20], lon [-60, -50] which
fully contains both the polygon and the 50 km comparables buffer.

Layers (GFC-2024-v1.12):
  - treecover2000:  % canopy cover at 2000 (0–100)
  - lossyear:       year of loss (1=2001, …, 24=2024); 0 = no loss
  - gain:           binary 2000–2012 forest gain flag (v1 product, not updated)
  - datamask:       0=no data, 1=mapped land, 2=permanent water

The standalone `loss` binary band was dropped in v1.12 — derive on the fly as
`(lossyear > 0)`. See the synthesised loss row in summary.md.

Outputs land in docs/site_data/hansen_gfc/:
  - {layer}_aoi_50km.tif    — buffer-clipped raster
  - {layer}_polygon.tif     — polygon-bounded raster
  - {layer}.png             — matplotlib quicklook
  - summary.md              — polygon stats + loss-year histogram
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import requests
from matplotlib.colors import ListedColormap
from rasterio.mask import mask as rio_mask
from rasterio.windows import from_bounds
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "site_data" / "hansen_gfc"
OUT.mkdir(parents=True, exist_ok=True)
CACHE = OUT / "_cache"
CACHE.mkdir(parents=True, exist_ok=True)

CENTROID_LON, CENTROID_LAT = -57.0355, -25.6073
BUFFER_KM = 50.0
DEG_PER_KM_LAT = 1.0 / 111.0
DEG_PER_KM_LON = 1.0 / (111.0 * math.cos(math.radians(CENTROID_LAT)))
DLAT = BUFFER_KM * DEG_PER_KM_LAT
DLON = BUFFER_KM * DEG_PER_KM_LON
AOI_BBOX = (
    CENTROID_LON - DLON,
    CENTROID_LAT - DLAT,
    CENTROID_LON + DLON,
    CENTROID_LAT + DLAT,
)

VERSION = "GFC-2024-v1.12"
TILE = "20S_060W"
BASE_URL = f"https://storage.googleapis.com/earthenginepartners-hansen/{VERSION}"
LAYERS = ("treecover2000", "lossyear", "gain", "datamask")
# `loss` was dropped as a standalone band in GFC-2024-v1.12 (HEAD returns 404).
# It is reconstructed in main() as `(lossyear > 0)` and persisted to disk so the
# downstream summary + quicklook keep the loss row.
DERIVED_LAYERS = ("loss",)
ALL_LAYERS = LAYERS + DERIVED_LAYERS

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "lqv-phase0/1.0 (research; weissvanderpol.ivan@gmail.com)"})
_retry = Retry(
    total=6,
    backoff_factor=1.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET",),
    raise_on_status=False,
)
SESSION.mount("https://", HTTPAdapter(max_retries=_retry, pool_connections=2, pool_maxsize=2))


def _download(layer: str) -> Path:
    """Cache one Hansen GFC tile to disk; return path."""
    fname = f"Hansen_{VERSION}_{layer}_{TILE}.tif"
    url = f"{BASE_URL}/{fname}"
    dst = CACHE / fname
    if dst.exists() and dst.stat().st_size > 1_000_000:
        print(f"  cached: {dst.name} ({dst.stat().st_size / 1e6:.1f} MB)", flush=True)
        return dst
    print(f"  GET {url}", flush=True)
    last: Exception | None = None
    for attempt in range(4):
        try:
            with SESSION.get(url, stream=True, timeout=180) as r:
                r.raise_for_status()
                tmp = dst.with_suffix(".tmp")
                with tmp.open("wb") as f:
                    for chunk in r.iter_content(chunk_size=1 << 20):
                        if chunk:
                            f.write(chunk)
                tmp.rename(dst)
            print(f"  → {dst.name} ({dst.stat().st_size / 1e6:.1f} MB)", flush=True)
            return dst
        except requests.exceptions.RequestException as e:
            last = e
            print(f"  attempt {attempt+1} failed: {e}", flush=True)
            time.sleep(2 ** attempt)
    raise last  # type: ignore[misc]


def load_polygon() -> dict:
    """Property polygon as a single GeoJSON geometry (EPSG:4326)."""
    gj = json.loads((ROOT / "docs/site_data/escobar_property_polygon.geojson").read_text())
    for f in gj.get("features", []):
        geom = f.get("geometry") or {}
        if geom.get("type") == "Polygon":
            return geom
    raise SystemExit("no Polygon geometry in escobar_property_polygon.geojson")


def clip_aoi(src_path: Path, layer: str) -> Path:
    out_path = OUT / f"{layer}_aoi_50km.tif"
    with rasterio.open(src_path) as src:
        w, s, e, n = AOI_BBOX
        window = from_bounds(w, s, e, n, transform=src.transform)
        win = window.round_offsets().round_lengths()
        data = src.read(1, window=win)
        transform = src.window_transform(win)
        profile = src.profile.copy()
        profile.update(
            height=data.shape[0],
            width=data.shape[1],
            transform=transform,
            compress="deflate",
            tiled=True,
            blockxsize=256,
            blockysize=256,
        )
        with rasterio.open(out_path, "w", **profile) as dst:
            dst.write(data, 1)
    print(f"  AOI clip → {out_path.name} {data.shape}", flush=True)
    return out_path


def clip_polygon(aoi_path: Path, polygon: dict, layer: str) -> tuple[Path, np.ndarray, int]:
    out_path = OUT / f"{layer}_polygon.tif"
    with rasterio.open(aoi_path) as src:
        nodata = src.nodata if src.nodata is not None else 255
        try:
            data, transform = rio_mask(src, [polygon], crop=True, nodata=nodata, filled=True)
        except ValueError as e:
            print(f"  polygon mask failed for {layer}: {e}", flush=True)
            return out_path, np.array([], dtype=src.dtypes[0]), 0
        profile = src.profile.copy()
        profile.update(
            height=data.shape[1],
            width=data.shape[2],
            transform=transform,
            nodata=nodata,
            compress="deflate",
            tiled=True,
            blockxsize=128,
            blockysize=128,
        )
        with rasterio.open(out_path, "w", **profile) as dst:
            dst.write(data)
    arr = data[0]
    valid = arr[arr != nodata]
    print(f"  polygon clip → {out_path.name} {arr.shape}, {valid.size} valid cells", flush=True)
    return out_path, valid, int(nodata)


def quicklook(aoi_path: Path, layer: str, polygon: dict) -> Path:
    out_path = OUT / f"{layer}.png"
    with rasterio.open(aoi_path) as src:
        data = src.read(1).astype(np.float32)
        nodata = src.nodata
        if nodata is not None:
            data = np.where(data == nodata, np.nan, data)
        extent: tuple[float, float, float, float] = (
            src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top
        )

    fig, ax = plt.subplots(figsize=(7, 7), dpi=140)
    if layer == "treecover2000":
        im = ax.imshow(data, extent=extent, cmap="Greens", vmin=0, vmax=100,
                       interpolation="nearest")
        fig.colorbar(im, ax=ax, shrink=0.7, label="Canopy cover at 2000 (%)")
        ax.set_title("Hansen GFC tree cover 2000 — 50 km buffer")
    elif layer == "loss":
        im = ax.imshow(data, extent=extent, cmap="Reds", vmin=0, vmax=1,
                       interpolation="nearest")
        fig.colorbar(im, ax=ax, shrink=0.7, label="Loss 2001–2024 (binary)")
        ax.set_title("Hansen GFC stand-replacement loss 2001–2024")
    elif layer == "lossyear":
        cmap = plt.get_cmap("turbo", 25)
        im = ax.imshow(data, extent=extent, cmap=cmap, vmin=0, vmax=24,
                       interpolation="nearest")
        cbar = fig.colorbar(im, ax=ax, shrink=0.7, label="Year of loss (1=2001 … 24=2024)")
        cbar.set_ticks([0, 5, 10, 15, 20, 24])
        cbar.set_ticklabels(["no loss", "2005", "2010", "2015", "2020", "2024"])
        ax.set_title("Hansen GFC year-of-loss — 50 km buffer")
    elif layer == "gain":
        im = ax.imshow(data, extent=extent, cmap="Blues", vmin=0, vmax=1,
                       interpolation="nearest")
        fig.colorbar(im, ax=ax, shrink=0.7, label="Forest gain 2000–2012 (binary)")
        ax.set_title("Hansen GFC forest gain 2000–2012")
    elif layer == "datamask":
        cmap = ListedColormap(["#ffffff", "#c9eac9", "#1f6fc0"])
        im = ax.imshow(data, extent=extent, cmap=cmap, vmin=0, vmax=2,
                       interpolation="nearest")
        cbar = fig.colorbar(im, ax=ax, shrink=0.7, label="0=no data / 1=land / 2=water")
        cbar.set_ticks([0, 1, 2])
        ax.set_title("Hansen GFC land/water datamask")
    else:
        im = ax.imshow(data, extent=extent, cmap="viridis")
        fig.colorbar(im, ax=ax, shrink=0.7)
        ax.set_title(f"Hansen GFC {layer}")

    ring = polygon["coordinates"][0]
    xs = [p[0] for p in ring]
    ys = [p[1] for p in ring]
    ax.plot(xs, ys, "-", color="red", lw=1.6, label="Property")
    ax.plot(CENTROID_LON, CENTROID_LAT, "+", color="red", ms=10)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend(loc="upper left", fontsize=8)
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  quicklook → {out_path.name}", flush=True)
    return out_path


def aoi_stats(aoi_path: Path) -> dict:
    with rasterio.open(aoi_path) as src:
        nodata = src.nodata
        data = src.read(1)
        valid = data if nodata is None else data[data != nodata]
        if valid.size == 0:
            return {"valid_cells": 0}
        return {
            "valid_cells": int(valid.size),
            "min": float(valid.min()),
            "max": float(valid.max()),
            "mean": float(valid.mean()),
            "nonzero_cells": int((valid > 0).sum()),
            "nonzero_pct": float((valid > 0).sum() / valid.size * 100),
        }


def polygon_stats(valid: np.ndarray) -> dict:
    if valid.size == 0:
        return {"valid_cells": 0}
    return {
        "valid_cells": int(valid.size),
        "min": float(valid.min()),
        "max": float(valid.max()),
        "mean": float(valid.mean()),
        "nonzero_cells": int((valid > 0).sum()),
        "nonzero_pct": float((valid > 0).sum() / valid.size * 100),
    }


def lossyear_histogram(valid: np.ndarray) -> dict[int, int]:
    if valid.size == 0:
        return {}
    vals, counts = np.unique(valid, return_counts=True)
    return {int(v): int(c) for v, c in zip(vals, counts)}


def _read_valid(path: Path) -> np.ndarray:
    with rasterio.open(path) as src:
        data = src.read(1)
        nodata = src.nodata
        return data if nodata is None else data[data != nodata]


def write_summary(results: dict) -> None:
    aoi_pixel_ha = 30.0 * 30.0 / 10000.0  # Hansen native ~30 m → 0.09 ha
    md = [
        "# Hansen Global Forest Change v1.12 (2000–2024) — Phase-0 §12.10",
        "",
        f"Centroid `{CENTROID_LON}, {CENTROID_LAT}` — buffer {BUFFER_KM} km",
        f"AOI bbox: W{AOI_BBOX[0]:.4f} S{AOI_BBOX[1]:.4f} "
        f"E{AOI_BBOX[2]:.4f} N{AOI_BBOX[3]:.4f}",
        f"Source tile: `{TILE}` from `{BASE_URL}`",
        "",
        "## Layers pulled",
        "",
        "| Layer | AOI valid cells | AOI nonzero % | Polygon valid cells | "
        "Polygon nonzero % | Polygon mean |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for layer in ALL_LAYERS:
        a = results[layer]["aoi_stats"]
        p = results[layer]["polygon_stats"]
        derived = " (derived from lossyear>0)" if layer in DERIVED_LAYERS else ""
        md.append(
            f"| {layer}{derived} | {a.get('valid_cells', 0)} | "
            f"{a.get('nonzero_pct', 0):.2f} | {p.get('valid_cells', 0)} | "
            f"{p.get('nonzero_pct', 0):.2f} | {p.get('mean', 0):.2f} |"
        )

    md.extend(["", "## Interpretation for La Quebrada Viva polygon", ""])

    tc = results["treecover2000"]["polygon_stats"]
    loss = results["loss"]["polygon_stats"]
    gain = results["gain"]["polygon_stats"]
    dm = results["datamask"]["polygon_stats"]

    if tc.get("valid_cells"):
        md.append(
            f"- **Canopy cover at 2000:** mean **{tc.get('mean', 0):.1f}%**, "
            f"max {tc.get('max', 0):.0f}%, "
            f"{tc.get('nonzero_cells', 0)} of {tc.get('valid_cells', 0)} cells "
            f"with any canopy at 2000."
        )
    if loss.get("valid_cells"):
        n_loss = loss.get("nonzero_cells", 0)
        loss_ha = n_loss * aoi_pixel_ha
        md.append(
            f"- **Stand-replacement loss 2001–2024:** "
            f"{n_loss} pixels (~{loss_ha:.2f} ha at 30 m) flagged as loss."
        )
    if gain.get("valid_cells"):
        md.append(
            f"- **Forest gain 2000–2012:** "
            f"{gain.get('nonzero_cells', 0)} pixels flagged as gain."
        )
    if dm.get("valid_cells"):
        dm_water = int(dm.get("max", 0))
        md.append(
            f"- **Datamask:** mean {dm.get('mean', 0):.2f} "
            f"(1=land, 2=water; polygon is "
            f"{'all land' if dm_water <= 1 else 'mixed land/water'} per Hansen)."
        )

    md.extend(["", "## Loss-year histogram (polygon)", ""])
    md.append("| Year | Loss pixels in polygon | Loss pixels in AOI |")
    md.append("| ---: | ---: | ---: |")
    poly_hist = results["lossyear"].get("hist_in_polygon", {})
    aoi_hist = results["lossyear"].get("hist_in_aoi", {})
    for code in range(0, 25):
        year = "no loss" if code == 0 else str(2000 + code)
        md.append(f"| {year} | {poly_hist.get(code, 0)} | {aoi_hist.get(code, 0)} |")

    md.extend(
        [
            "",
            "## Files",
            "",
            "```",
            "docs/site_data/hansen_gfc/",
            "├── treecover2000_aoi_50km.tif  treecover2000_polygon.tif  treecover2000.png",
            "├── loss_aoi_50km.tif           loss_polygon.tif           loss.png",
            "├── lossyear_aoi_50km.tif       lossyear_polygon.tif       lossyear.png",
            "├── gain_aoi_50km.tif           gain_polygon.tif           gain.png",
            "├── datamask_aoi_50km.tif       datamask_polygon.tif       datamask.png",
            "└── summary.md",
            "```",
            "",
            "## Caveats",
            "",
            "- Hansen v1.12 covers stand-replacement loss only — sub-canopy thinning",
            "  and selective logging are invisible. For degradation use NICFI + Mapbiomas.",
            "- The `gain` band is a 2000–2012 product and has NOT been updated in",
            "  later versions; treat it as historical, not contemporary.",
            "- 1 arcsecond ≈ 30 m at the equator; at lat -25.6 the pixel is",
            "  ~30 m N–S × ~27 m E–W (cos correction). For ha conversions we use",
            f"  the nominal 30 m × 30 m → {aoi_pixel_ha:.4f} ha per pixel.",
            "- The `treecover2000` % threshold for \"forest\" is user-defined; UNFCCC",
            "  Paraguay typically uses ≥10% but the BAAPA ecoregion default is ≥30%.",
            "- For 1985–2000 history use Mapbiomas Paraguay (next §12 item).",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("  summary.md written", flush=True)


def synthesise_loss(polygon: dict) -> dict:
    """Reconstruct the dropped `loss` binary band as `(lossyear > 0)`.

    Hansen GFC v1.12 no longer publishes a standalone `loss` GeoTIFF — every
    pixel with `lossyear > 0` was a stand-replacement loss, so the band is
    fully derivable. We persist it as if it had been downloaded to keep the
    five-output file footprint and the summary/quicklook plumbing untouched.
    """
    src_aoi = OUT / "lossyear_aoi_50km.tif"
    dst_aoi = OUT / "loss_aoi_50km.tif"
    with rasterio.open(src_aoi) as src:
        data = src.read(1)
        nodata = src.nodata
        loss = (data > 0).astype("uint8")
        if nodata is not None:
            loss[data == nodata] = 255
        profile = src.profile.copy()
        profile.update(dtype="uint8", nodata=255, compress="deflate")
        with rasterio.open(dst_aoi, "w", **profile) as dst:
            dst.write(loss, 1)
    print(f"  AOI synth → {dst_aoi.name} {loss.shape}", flush=True)

    _, poly_valid, _ = clip_polygon(dst_aoi, polygon, "loss")
    quicklook(dst_aoi, "loss", polygon)
    return {
        "aoi_stats": aoi_stats(dst_aoi),
        "polygon_stats": polygon_stats(poly_valid),
    }


def main() -> int:
    print(
        f"AOI 50 km bbox: W{AOI_BBOX[0]:.4f} S{AOI_BBOX[1]:.4f} "
        f"E{AOI_BBOX[2]:.4f} N{AOI_BBOX[3]:.4f}",
        flush=True,
    )
    polygon = load_polygon()

    results: dict[str, dict] = {}
    for layer in LAYERS:
        print(f"\n[layer] {layer}", flush=True)
        tile_path = _download(layer)
        aoi_path = clip_aoi(tile_path, layer)
        _, poly_valid, _ = clip_polygon(aoi_path, polygon, layer)
        quicklook(aoi_path, layer, polygon)
        results[layer] = {
            "aoi_stats": aoi_stats(aoi_path),
            "polygon_stats": polygon_stats(poly_valid),
        }
        if layer == "lossyear":
            results[layer]["hist_in_aoi"] = lossyear_histogram(_read_valid(aoi_path))
            results[layer]["hist_in_polygon"] = lossyear_histogram(poly_valid)

    print("\n[derived] loss = (lossyear > 0)", flush=True)
    results["loss"] = synthesise_loss(polygon)

    write_summary(results)
    print("\nDone.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
