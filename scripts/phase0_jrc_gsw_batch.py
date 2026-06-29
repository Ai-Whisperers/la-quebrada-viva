#!/usr/bin/env python3
"""Phase-0 §12.E: pull JRC Global Surface Water v1.4 (1984–2021) for the
50 km buffer around the La Quebrada Viva polygon centroid (-57.0355, -25.6073),
clip to AOI, derive polygon-level stats, and write quicklooks.

Tile 60W_20S (upper-left corner) covers lon [-60, -50], lat [-30, -20] which
fully contains both the polygon and the 50 km comparables buffer.

Layers (JRC GSW v1.4 2021):
  - occurrence:  % of valid observations classified as water, 1984–2021
  - seasonality: months/year with water presence (0–12)
  - recurrence:  % of years with at least one water observation
  - transitions: 10-class change between 1984–1999 and 2000–2021

Outputs land in docs/site_data/jrc_gsw/:
  - {layer}_aoi_50km.tif    — buffer-clipped raster
  - {layer}_polygon.tif     — polygon-bounded raster
  - {layer}.png             — matplotlib quicklook
  - summary.md              — polygon stats + counts
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
OUT = ROOT / "docs" / "site_data" / "jrc_gsw"
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
    CENTROID_LON - DLON,  # W
    CENTROID_LAT - DLAT,  # S
    CENTROID_LON + DLON,  # E
    CENTROID_LAT + DLAT,  # N
)

TILE = "60W_20S"
BASE_URL = "https://storage.googleapis.com/global-surface-water/downloads2021"
LAYERS = ("occurrence", "seasonality", "recurrence", "transitions")

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
    """Cache one JRC GSW tile to disk; return path."""
    url = f"{BASE_URL}/{layer}/{layer}_{TILE}v1_4_2021.tif"
    dst = CACHE / f"{layer}_{TILE}v1_4_2021.tif"
    if dst.exists() and dst.stat().st_size > 1_000_000:
        print(f"  cached: {dst.name} ({dst.stat().st_size / 1e6:.1f} MB)", flush=True)
        return dst
    print(f"  GET {url}", flush=True)
    last: Exception | None = None
    for attempt in range(4):
        try:
            with SESSION.get(url, stream=True, timeout=120) as r:
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
    """Window-read the 50 km bbox from the tile and save as a GeoTIFF."""
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
    """Crop the AOI raster down to the property polygon (rectangular bbox of
    polygon + nodata outside the ring)."""
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
    if layer == "occurrence":
        im = ax.imshow(data, extent=extent, cmap="Blues", vmin=0, vmax=100,
                       interpolation="nearest")
        fig.colorbar(im, ax=ax, shrink=0.7, label="Water occurrence (% of obs)")
        ax.set_title("JRC GSW occurrence 1984–2021 — 50 km buffer")
    elif layer == "seasonality":
        im = ax.imshow(data, extent=extent, cmap="YlGnBu", vmin=0, vmax=12,
                       interpolation="nearest")
        fig.colorbar(im, ax=ax, shrink=0.7, label="Months/year with water (0–12)")
        ax.set_title("JRC GSW seasonality — 50 km buffer")
    elif layer == "recurrence":
        im = ax.imshow(data, extent=extent, cmap="PuBu", vmin=0, vmax=100,
                       interpolation="nearest")
        fig.colorbar(im, ax=ax, shrink=0.7, label="Recurrence (% of years water present)")
        ax.set_title("JRC GSW recurrence — 50 km buffer")
    elif layer == "transitions":
        cmap_colors = [
            "#ffffff",
            "#0000ff",
            "#22b14c",
            "#d1102d",
            "#99d9ea",
            "#b5e61d",
            "#e6a1aa",
            "#ff7f27",
            "#ffc90e",
            "#7092be",
            "#c3c3c3",
        ]
        cmap = ListedColormap(cmap_colors)
        im = ax.imshow(data, extent=extent, cmap=cmap, vmin=0, vmax=10,
                       interpolation="nearest")
        fig.colorbar(im, ax=ax, shrink=0.7, label="Transition class (0–10)")
        ax.set_title("JRC GSW transitions 1984→2021 — 50 km buffer")
    else:
        im = ax.imshow(data, extent=extent, cmap="viridis")
        fig.colorbar(im, ax=ax, shrink=0.7)
        ax.set_title(f"JRC GSW {layer}")

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
    """Buffer-scoped histogram (% water cells, max value, etc.)."""
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


TRANSITION_CLASSES = {
    0: "No change / no data",
    1: "Permanent water (1984–2021)",
    2: "New permanent (became permanent)",
    3: "Lost permanent (was permanent, lost)",
    4: "Seasonal water (both periods)",
    5: "New seasonal (became seasonal)",
    6: "Lost seasonal (was seasonal, lost)",
    7: "Seasonal → Permanent",
    8: "Permanent → Seasonal",
    9: "Ephemeral permanent",
    10: "Ephemeral seasonal",
}


def transition_histogram(valid: np.ndarray) -> dict[int, int]:
    if valid.size == 0:
        return {}
    vals, counts = np.unique(valid, return_counts=True)
    return {int(v): int(c) for v, c in zip(vals, counts)}


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
        if layer == "transitions":
            results[layer]["transitions_in_aoi"] = transition_histogram(
                _read_valid(aoi_path)
            )
            results[layer]["transitions_in_polygon"] = transition_histogram(poly_valid)

    write_summary(results)
    print("\nDone.", flush=True)
    return 0


def _read_valid(path: Path) -> np.ndarray:
    with rasterio.open(path) as src:
        data = src.read(1)
        nodata = src.nodata
        return data if nodata is None else data[data != nodata]


def write_summary(results: dict) -> None:
    md = [
        "# JRC Global Surface Water v1.4 (1984–2021) — Phase-0 §12.E",
        "",
        f"Centroid `{CENTROID_LON}, {CENTROID_LAT}` — buffer {BUFFER_KM} km",
        f"AOI bbox: W{AOI_BBOX[0]:.4f} S{AOI_BBOX[1]:.4f} "
        f"E{AOI_BBOX[2]:.4f} N{AOI_BBOX[3]:.4f}",
        f"Source tile: `{TILE}` from `{BASE_URL}`",
        "",
        "## Layers pulled",
        "",
        "| Layer | AOI valid cells | AOI nonzero % | Polygon valid cells | Polygon nonzero % | Polygon max |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for layer in LAYERS:
        a = results[layer]["aoi_stats"]
        p = results[layer]["polygon_stats"]
        md.append(
            "| {layer} | {a_n} | {a_p:.2f} | {p_n} | {p_p:.2f} | {p_max} |".format(
                layer=layer,
                a_n=a.get("valid_cells", 0),
                a_p=a.get("nonzero_pct", 0.0),
                p_n=p.get("valid_cells", 0),
                p_p=p.get("nonzero_pct", 0.0),
                p_max=("{:.0f}".format(p.get("max"))
                       if p.get("valid_cells", 0) else "—"),
            )
        )
    md += [
        "",
        "## Interpretation for La Quebrada Viva polygon",
        "",
    ]
    occ_p = results["occurrence"]["polygon_stats"]
    seas_p = results["seasonality"]["polygon_stats"]
    rec_p = results["recurrence"]["polygon_stats"]
    if occ_p.get("nonzero_cells", 0) == 0:
        md.append(
            "- **Surface water inside polygon: 0 cells with any historical water occurrence.** "
            "JRC GSW agrees with the Sentinel-2 NDWI finding (`property_map/index.md`): "
            "no permanent or seasonal open water inside the 30.9 ha polygon at 30 m resolution."
        )
    else:
        md.append(
            f"- Polygon contains **{occ_p['nonzero_cells']} cells "
            f"({occ_p['nonzero_pct']:.2f}%)** with historical water occurrence "
            f"(max {occ_p['max']:.0f}% of observations)."
        )
    if seas_p.get("valid_cells", 0):
        md.append(
            f"- Polygon seasonality max: **{seas_p['max']:.0f} months/year** "
            f"(mean {seas_p['mean']:.2f})."
        )
    if rec_p.get("valid_cells", 0):
        md.append(
            f"- Polygon recurrence max: **{rec_p['max']:.0f}%** of years with at least "
            f"one water observation (mean {rec_p['mean']:.2f}%)."
        )
    md += [
        "",
        "## Transitions histogram (1984→2021)",
        "",
        "| Class | Description | AOI cells | Polygon cells |",
        "| ---: | --- | ---: | ---: |",
    ]
    tr = results.get("transitions", {})
    aoi_tr = tr.get("transitions_in_aoi", {})
    poly_tr = tr.get("transitions_in_polygon", {})
    all_classes = sorted(set(aoi_tr) | set(poly_tr))
    for c in all_classes:
        md.append(
            f"| {c} | {TRANSITION_CLASSES.get(c, '?')} | "
            f"{aoi_tr.get(c, 0)} | {poly_tr.get(c, 0)} |"
        )
    md += [
        "",
        "## Files",
        "",
        "```",
        "docs/site_data/jrc_gsw/",
        "├── occurrence_aoi_50km.tif   occurrence_polygon.tif   occurrence.png",
        "├── seasonality_aoi_50km.tif  seasonality_polygon.tif  seasonality.png",
        "├── recurrence_aoi_50km.tif   recurrence_polygon.tif   recurrence.png",
        "├── transitions_aoi_50km.tif  transitions_polygon.tif  transitions.png",
        "└── summary.md",
        "```",
        "",
        "## Caveats",
        "",
        "- JRC GSW v1.4 ends 2021. For 2022–2025 monthly water dynamics, pull",
        "  JRC Monthly History via GEE (`JRC/GSW1_4/MonthlyHistory`).",
        "- Resolution is 30 m — sub-pixel water (< ~900 m² puddles, narrow",
        "  arroyos < 30 m wide) is invisible. The polygon's `arroyo` features",
        "  visible on canopy NDVI/DEM hydrography sit below this resolution",
        "  threshold and correctly read as zero here. This is a *coarse-scale*",
        "  confirmation that no perennial pond/lake exists on-property — not a",
        "  micro-hydrology layer.",
        "- For micro-hydrology use the DEM-derived flow-accum hydrography",
        "  (`property_map/vector/hydrography_dem.geojson`) and pending drone SfM",
        "  + NDWI sub-pixel work in `property_map_v2_data_sources.md` §3.",
    ]
    (OUT / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("  summary.md written", flush=True)


if __name__ == "__main__":
    sys.exit(main() or 0)
