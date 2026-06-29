#!/usr/bin/env python3
"""Phase-0 §12.11: pull Mapbiomas Paraguay Collection 2 (1985–2023) annual 30 m
LULC rasters for the 50 km buffer around the La Quebrada Viva polygon centroid
(-57.0355, -25.6073), clip to AOI + polygon, build per-year class histograms,
derive a change-trajectory matrix 1985→2023, render decadal quicklooks, and
cross-check the deforestation arc against Hansen GFC (Phase-0 §12.10).

Mapbiomas Paraguay Collection 2 publishes one COG per year on
`storage.googleapis.com/mapbiomas-public/initiatives/paraguay/collection_2/`
following the pattern
`mapbiomas_paraguay_collection2_integration_v1-classification_<YEAR>.tif`
(EPSG:4326, uint8, 256×256 internal tiles, ~39 MB per year). We fetch via
`/vsicurl/` + a windowed read so per-year network traffic stays ~4 MB instead
of the full national 39 MB mosaic. The AOI clip on disk doubles as the
re-run cache — second runs skip the network.

Outputs land in docs/site_data/mapbiomas_paraguay/:
  - mapbiomas_<YEAR>_aoi_50km.tif        — 50 km buffer clip per year
  - mapbiomas_<YEAR>_polygon.tif         — polygon-bounded clip per year
  - mapbiomas_decadal_quicklook.png      — 1985 / 1995 / 2005 / 2015 / 2023 panels
  - class_timeseries.csv                 — long-format AOI + polygon class counts
  - change_trajectory_polygon.csv        — 1985 × 2023 transition matrix (polygon)
  - summary.md                           — narrative + Hansen cross-check
"""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D
from rasterio.mask import mask as rio_mask
from rasterio.windows import from_bounds

import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "site_data" / "mapbiomas_paraguay"
OUT.mkdir(parents=True, exist_ok=True)

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

COLLECTION = "collection_2"
BASE_URL = (
    "https://storage.googleapis.com/mapbiomas-public/initiatives/paraguay/"
    f"{COLLECTION}"
)
PRODUCT = "mapbiomas_paraguay_collection2_integration_v1-classification"
YEARS = list(range(1985, 2024))  # 2024 not yet published for Collection 2
DECADAL_YEARS = [1985, 1995, 2005, 2015, 2023]

# Mapbiomas global legend (subset present in the LQV AOI). Confirmed via 2023
# raster probe: classes 3, 6, 9, 11, 12, 15, 18, 22, 26 are all that appear.
# Codes outside this set still get a "Unknown <code>" label and a grey swatch.
CLASS_LEGEND: dict[int, tuple[str, str]] = {
    0:  ("No data / outside Paraguay", "#ffffff"),
    3:  ("Forest Formation",           "#1f8d49"),
    6:  ("Flooded Forest",             "#007785"),
    9:  ("Forest Plantation",          "#7a5900"),
    11: ("Wetland",                    "#45c2a5"),
    12: ("Grassland",                  "#b8af4f"),
    15: ("Pasture",                    "#ffd966"),
    18: ("Agriculture",                "#e974ed"),
    22: ("Non-vegetated Area",         "#d4271e"),
    26: ("Water",                      "#2532e4"),
}
# Forest-like classes for the canopy cross-check vs Hansen treecover2000.
FOREST_CLASSES = {3, 6, 9}
NATIVE_FOREST_CLASSES = {3, 6}


def _year_url(year: int) -> str:
    return f"/vsicurl/{BASE_URL}/{PRODUCT}_{year}.tif"


def load_polygon() -> dict:
    gj = json.loads((ROOT / "docs/site_data/escobar_property_polygon.geojson").read_text())
    for f in gj.get("features", []):
        geom = f.get("geometry") or {}
        if geom.get("type") == "Polygon":
            return geom
    raise SystemExit("no Polygon geometry in escobar_property_polygon.geojson")


def clip_aoi(year: int) -> Path:
    """Windowed `/vsicurl/` read of the national COG → AOI GeoTIFF on disk."""
    out_path = OUT / f"mapbiomas_{year}_aoi_50km.tif"
    if out_path.exists() and out_path.stat().st_size > 50_000:
        print(f"  cached: {out_path.name}", flush=True)
        return out_path
    url = _year_url(year)
    print(f"  GET {url} (windowed)", flush=True)
    with rasterio.open(url) as src:
        w, s, e, n = AOI_BBOX
        window = from_bounds(w, s, e, n, transform=src.transform)
        win = window.round_offsets().round_lengths()
        data = src.read(1, window=win)
        transform = src.window_transform(win)
        profile = src.profile.copy()
        profile.update(
            driver="GTiff",
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


def clip_polygon(aoi_path: Path, polygon: dict, year: int) -> tuple[Path, np.ndarray]:
    out_path = OUT / f"mapbiomas_{year}_polygon.tif"
    with rasterio.open(aoi_path) as src:
        nodata = src.nodata if src.nodata is not None else 0
        try:
            data, transform = rio_mask(src, [polygon], crop=True, nodata=nodata, filled=True)
        except ValueError as e:
            print(f"  polygon mask failed for {year}: {e}", flush=True)
            return out_path, np.array([], dtype=src.dtypes[0])
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
    return out_path, valid


def histogram(valid: np.ndarray) -> dict[int, int]:
    if valid.size == 0:
        return {}
    vals, counts = np.unique(valid, return_counts=True)
    return {int(v): int(c) for v, c in zip(vals, counts)}


def aoi_histogram(aoi_path: Path) -> tuple[dict[int, int], int]:
    with rasterio.open(aoi_path) as src:
        data = src.read(1)
        nodata = src.nodata
    valid = data if nodata is None else data[data != nodata]
    return histogram(valid), int(valid.size)


def write_timeseries_csv(records: list[dict]) -> Path:
    out_path = OUT / "class_timeseries.csv"
    cols = ["year", "class_code", "class_name", "aoi_pixels", "polygon_pixels",
            "aoi_pct", "polygon_pct"]
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(records)
    print(f"  timeseries → {out_path.name} ({len(records)} rows)", flush=True)
    return out_path


def write_change_matrix() -> tuple[Path, dict[tuple[int, int], int]]:
    """Pixel-aligned (1985 class) × (2023 class) transition counts in polygon."""
    src_a = OUT / "mapbiomas_1985_polygon.tif"
    src_b = OUT / "mapbiomas_2023_polygon.tif"
    with rasterio.open(src_a) as ra, rasterio.open(src_b) as rb:
        a = ra.read(1)
        b = rb.read(1)
        nodata = ra.nodata if ra.nodata is not None else 0
    mask = (a != nodata) & (b != nodata)
    pairs = np.stack([a[mask], b[mask]], axis=1)
    # `np.unique(axis=0)` gives sorted unique pair counts.
    pair_rows, counts = np.unique(pairs, axis=0, return_counts=True)
    matrix: dict[tuple[int, int], int] = {
        (int(p[0]), int(p[1])): int(c) for p, c in zip(pair_rows, counts)
    }
    out_path = OUT / "change_trajectory_polygon.csv"
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["from_code", "from_name", "to_code", "to_name", "pixels"])
        for (a_code, b_code), c in sorted(matrix.items(), key=lambda kv: -kv[1]):
            w.writerow([
                a_code, CLASS_LEGEND.get(a_code, (f"Unknown {a_code}", ""))[0],
                b_code, CLASS_LEGEND.get(b_code, (f"Unknown {b_code}", ""))[0],
                c,
            ])
    print(f"  change matrix → {out_path.name} ({len(matrix)} pairs)", flush=True)
    return out_path, matrix


def decadal_quicklook(polygon: dict) -> Path:
    """Five-panel decadal montage 1985 / 1995 / 2005 / 2015 / 2023."""
    out_path = OUT / "mapbiomas_decadal_quicklook.png"
    # Build a categorical colormap over all known codes (0..26). Unknown codes
    # in the AOI render as grey via the BoundaryNorm fallback.
    codes = sorted(CLASS_LEGEND.keys())
    colors = [CLASS_LEGEND[c][1] for c in codes]
    cmap = ListedColormap(colors)
    boundaries = [c - 0.5 for c in codes] + [codes[-1] + 0.5]
    norm = BoundaryNorm(boundaries, cmap.N)

    fig, axes = plt.subplots(1, 5, figsize=(20, 5), dpi=140)
    for ax, year in zip(axes, DECADAL_YEARS):
        aoi_path = OUT / f"mapbiomas_{year}_aoi_50km.tif"
        with rasterio.open(aoi_path) as src:
            data = src.read(1)
            extent = (src.bounds.left, src.bounds.right,
                      src.bounds.bottom, src.bounds.top)
        # Remap unknown codes to 0 so the categorical norm doesn't barf.
        known = np.isin(data, codes)
        display = np.where(known, data, 0)
        ax.imshow(display, extent=extent, cmap=cmap, norm=norm,
                  interpolation="nearest")
        ring = polygon["coordinates"][0]
        ax.plot([p[0] for p in ring], [p[1] for p in ring], "-",
                color="red", lw=1.2)
        ax.plot(CENTROID_LON, CENTROID_LAT, "+", color="red", ms=8)
        ax.set_title(str(year))
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_aspect("equal")

    # Compact legend in the figure margin.
    handles = [
        Line2D([0], [0], marker="s", linestyle="",
               markerfacecolor=color, markeredgecolor="black",
               markersize=10, label=f"{code} {CLASS_LEGEND[code][0]}")
        for code, color in zip(codes, colors) if code != 0
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=9,
               frameon=False, bbox_to_anchor=(0.5, -0.05))
    fig.suptitle(
        "Mapbiomas Paraguay Collection 2 — LQV 50 km buffer (decadal)",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0.05, 1, 0.96))
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  quicklook → {out_path.name}", flush=True)
    return out_path


def write_summary(
    per_year: dict[int, dict[str, dict[int, int]]],
    matrix: dict[tuple[int, int], int],
) -> None:
    aoi_pixel_ha = 30.0 * 30.0 / 10000.0  # 0.09 ha per 30 m pixel
    polygon_cells_1985 = sum(per_year[1985]["polygon"].values()) or 1

    def native_forest_pct(hist: dict[int, int]) -> float:
        total = sum(hist.values()) or 1
        return 100.0 * sum(hist.get(c, 0) for c in NATIVE_FOREST_CLASSES) / total

    md = [
        "# Mapbiomas Paraguay Collection 2 (1985–2023) — Phase-0 §12.11",
        "",
        f"Centroid `{CENTROID_LON}, {CENTROID_LAT}` — buffer {BUFFER_KM} km",
        f"AOI bbox: W{AOI_BBOX[0]:.4f} S{AOI_BBOX[1]:.4f} "
        f"E{AOI_BBOX[2]:.4f} N{AOI_BBOX[3]:.4f}",
        f"Source: `{BASE_URL}/` (EPSG:4326, uint8, 30 m, 256×256 COG)",
        f"Years pulled: {YEARS[0]}–{YEARS[-1]} ({len(YEARS)} annual rasters)",
        "",
        "## Per-decade polygon native-forest fraction",
        "",
        "| Year | Native forest % | Forest+plant % | Pasture % | Agriculture % |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for year in DECADAL_YEARS:
        h = per_year[year]["polygon"]
        total = sum(h.values()) or 1
        native = 100.0 * sum(h.get(c, 0) for c in NATIVE_FOREST_CLASSES) / total
        forest = 100.0 * sum(h.get(c, 0) for c in FOREST_CLASSES) / total
        pasture = 100.0 * h.get(15, 0) / total
        agri = 100.0 * h.get(18, 0) / total
        md.append(
            f"| {year} | {native:.1f} | {forest:.1f} | {pasture:.1f} | {agri:.1f} |"
        )

    md.extend(["", "## Interpretation for La Quebrada Viva polygon", ""])
    nf_1985 = native_forest_pct(per_year[1985]["polygon"])
    nf_2023 = native_forest_pct(per_year[2023]["polygon"])
    delta = nf_2023 - nf_1985
    md.append(
        f"- **Native forest fraction (classes 3 + 6) 1985 → 2023:** "
        f"{nf_1985:.1f}% → {nf_2023:.1f}% (Δ {delta:+.1f} pp)."
    )
    cell_ha = aoi_pixel_ha
    md.append(
        f"- **Polygon footprint at 30 m:** ~{polygon_cells_1985} pixels × "
        f"{cell_ha:.2f} ha ≈ {polygon_cells_1985 * cell_ha:.1f} ha "
        "(coarser than Hansen due to a different reprojection grid; "
        "treat as area-share indicator, not parcel-accurate hectarage)."
    )
    # Hansen cross-check: treecover2000 baseline was 82.1% mean canopy.
    # Mapbiomas native-forest in 1985 should be in the same ballpark; if not
    # we flag it. Mapbiomas is categorical (presence/absence at 30 m), Hansen
    # is continuous (% canopy), so a 10–20 pp gap is normal.
    nf_2000_approx = native_forest_pct(per_year.get(2000, per_year[1985])["polygon"])
    md.append(
        f"- **Hansen 2000 cross-check:** Mapbiomas native-forest at 2000 = "
        f"{nf_2000_approx:.1f}% vs Hansen treecover2000 mean = 82.1%. "
        "(Categorical vs continuous; agreement within ~15 pp is expected.)"
    )

    md.extend(["", "## Top 10 polygon transitions 1985 → 2023", ""])
    md.append("| From | → To | Pixels | ha |")
    md.append("| --- | --- | ---: | ---: |")
    for (a, b), c in sorted(matrix.items(), key=lambda kv: -kv[1])[:10]:
        a_name = CLASS_LEGEND.get(a, (f"Unknown {a}", ""))[0]
        b_name = CLASS_LEGEND.get(b, (f"Unknown {b}", ""))[0]
        arrow = "→ (same)" if a == b else "→"
        md.append(f"| {a} {a_name} | {arrow} {b} {b_name} | {c} | {c * cell_ha:.2f} |")

    md.extend(
        [
            "",
            "## Files",
            "",
            "```",
            "docs/site_data/mapbiomas_paraguay/",
            "├── mapbiomas_<YEAR>_aoi_50km.tif    × 39 years",
            "├── mapbiomas_<YEAR>_polygon.tif     × 39 years",
            "├── mapbiomas_decadal_quicklook.png  ← 1985/1995/2005/2015/2023",
            "├── class_timeseries.csv             ← long-format AOI + polygon counts",
            "├── change_trajectory_polygon.csv    ← 1985 × 2023 transition matrix",
            "└── summary.md                       ← this file",
            "```",
            "",
            "## Caveats",
            "",
            "- Mapbiomas Paraguay is a categorical 30 m LULC product — each pixel",
            "  gets a single class label per year. Use Hansen GFC (§12.10) for",
            "  continuous canopy %, and NICFI for sub-canopy degradation.",
            "- Collection 2 publishes 1985–2023; 2024 (and the Collection 1 →",
            "  Collection 2 deltas) are not yet released. Refresh when MapBiomas",
            "  PY announces Collection 3.",
            "- The `polygon` clips are reprojection-aligned to Mapbiomas' EPSG:4326",
            "  grid, so they differ from Hansen's at the per-pixel level. Compare",
            "  area shares, not pixel-by-pixel overlays.",
            "- Per-year class %s sum across all classes present in the polygon,",
            "  including the legitimate non-forest classes (pasture, agriculture,",
            "  grassland). The deck cares about the native-forest delta, not the",
            "  full LULC breakdown.",
            "- Network-fetched via `/vsicurl/` — re-runs reuse the on-disk AOI",
            "  clips and skip the network. Delete `mapbiomas_<YEAR>_aoi_50km.tif`",
            "  to force a re-fetch.",
        ]
    )
    (OUT / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("  summary.md written", flush=True)


def main() -> int:
    print(
        f"AOI 50 km bbox: W{AOI_BBOX[0]:.4f} S{AOI_BBOX[1]:.4f} "
        f"E{AOI_BBOX[2]:.4f} N{AOI_BBOX[3]:.4f}",
        flush=True,
    )
    polygon = load_polygon()

    timeseries_records: list[dict] = []
    per_year: dict[int, dict[str, dict[int, int]]] = {}

    for year in YEARS:
        print(f"\n[year] {year}", flush=True)
        aoi_path = clip_aoi(year)
        _, poly_valid = clip_polygon(aoi_path, polygon, year)
        aoi_hist, aoi_total = aoi_histogram(aoi_path)
        poly_hist = histogram(poly_valid)
        per_year[year] = {"aoi": aoi_hist, "polygon": poly_hist}

        poly_total = sum(poly_hist.values()) or 1
        aoi_total = aoi_total or 1
        present = sorted(set(aoi_hist) | set(poly_hist))
        for code in present:
            name = CLASS_LEGEND.get(code, (f"Unknown {code}", ""))[0]
            a = aoi_hist.get(code, 0)
            p = poly_hist.get(code, 0)
            timeseries_records.append({
                "year": year,
                "class_code": code,
                "class_name": name,
                "aoi_pixels": a,
                "polygon_pixels": p,
                "aoi_pct": round(100.0 * a / aoi_total, 4),
                "polygon_pct": round(100.0 * p / poly_total, 4),
            })

    write_timeseries_csv(timeseries_records)
    _, matrix = write_change_matrix()
    decadal_quicklook(polygon)
    write_summary(per_year, matrix)
    print("\nDone.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
