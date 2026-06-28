"""Polygon-clipped NDVI + NDWI for Wesley's 30.9 ha buildable AOI.

Analytical (not asset-pipeline) re-derive of vegetation/water indices against
the post-escritura polygon at `docs/site_data/escobar_property_polygon.geojson`.

Distinct from `make_ndvi_mask.py`, which serves the Blender scatter pipeline and
must stay byte-stable. This script:

  * Converts DN to reflectance with `scale=0.0001` only (no `-0.1` offset).
    The tile metadata declares both `scale` and `offset`, but the offset
    drives dense-canopy red reflectance to ~0 and saturates NDVI at 1.0 —
    `make_ndvi_mask.py` and the headline numbers in
    `post_escritura_site_knowledge.md` were computed without the offset,
    and we stay consistent with them. The offset is the harmonization
    transform for cross-collection comparison, not an analytical correction.
  * Reprojects the polygon to the S2 tile CRS (EPSG:32721) and uses
    `rasterio.features.geometry_mask` to clip per-pixel statistics to the
    parcel interior — not the rectangular AOI bbox.
  * Writes float32 GeoTIFFs (`polygon_ndvi.tif`, `polygon_ndwi.tif`),
    polygon-overlay PNG quicklooks, and a per-class stats JSON
    (`polygon_veg_stats.json`).
  * Cross-checks against the headline figures published in
    `docs/post_escritura_site_knowledge.md` and prints any divergence.

Inputs (read-only):
  docs/site_data/escobar_property_polygon.geojson
  docs/site_data/sentinel2/S2B_21JVM_20260512_0_L2A_{red,nir,green}.tif
  docs/site_data/sentinel2/metadata.json

Outputs (written to docs/site_data/extended_aoi/):
  polygon_ndvi.tif
  polygon_ndwi.tif
  polygon_ndvi_quicklook.png
  polygon_ndwi_quicklook.png
  polygon_veg_stats.json
"""
from __future__ import annotations

import json
import os
from typing import Tuple

import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.transform import Affine
from rasterio.warp import transform_geom
from rasterio.windows import from_bounds

import matplotlib

matplotlib.use("Agg")  # headless; do not import pyplot before this
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SENTINEL_DIR = os.path.join(PROJECT_ROOT, "docs", "site_data", "sentinel2")
PREFIX = "S2B_21JVM_20260512_0_L2A"
POLY_GEOJSON = os.path.join(
    PROJECT_ROOT, "docs", "site_data", "escobar_property_polygon.geojson"
)
OUT_DIR = os.path.join(PROJECT_ROOT, "docs", "site_data", "extended_aoi")

# Scale-only DN→reflectance — see module docstring for why the metadata
# offset is intentionally NOT applied here.
DN_SCALE = 0.0001
EPS = 1e-6

# Headline numbers already published — script flags divergence rather than
# silently overwriting them.
PUBLISHED = {
    "ndvi_median": 0.917,
    "ndvi_p25": 0.890,
    "ndvi_p75": 0.937,
    "ndvi_frac_gt_0p6": 0.974,
    "ndwi_frac_gt_0": 0.000,
}


def load_polygon() -> dict:
    with open(POLY_GEOJSON) as f:
        gj = json.load(f)
    for feat in gj["features"]:
        if feat["geometry"]["type"] == "Polygon":
            return feat
    raise RuntimeError(f"No Polygon feature found in {POLY_GEOJSON}")


def polygon_bbox_4326(feat: dict) -> Tuple[float, float, float, float]:
    coords = feat["geometry"]["coordinates"][0]
    lons = [c[0] for c in coords]
    lats = [c[1] for c in coords]
    return min(lons), min(lats), max(lons), max(lats)


def read_band(
    band_name: str, geom_utm: dict, pad_m: float = 60.0
) -> Tuple[np.ndarray, Affine, str]:
    """Window-read a single S2 band tight around the polygon (+pad).

    Returns reflectance (float32, scale-only), affine for the window,
    source CRS string.
    """
    path = os.path.join(SENTINEL_DIR, f"{PREFIX}_{band_name}.tif")
    with rasterio.open(path) as src:
        # bbox of polygon in src CRS, then expand by pad to keep the polygon
        # edges away from the window edge.
        coords = geom_utm["coordinates"][0]
        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]
        left = min(xs) - pad_m
        right = max(xs) + pad_m
        bottom = min(ys) - pad_m
        top = max(ys) + pad_m

        window = from_bounds(left, bottom, right, top, transform=src.transform)
        window = window.round_offsets().round_lengths()
        arr_dn = src.read(1, window=window).astype(np.float32)
        win_transform = src.window_transform(window)
        crs_str = src.crs.to_string()

    nodata = arr_dn == 0
    refl = arr_dn * DN_SCALE
    refl[nodata] = np.nan
    return refl, win_transform, crs_str


def quicklook(
    index: np.ndarray,
    mask_inside: np.ndarray,
    transform: Affine,
    polygon_xy: np.ndarray,
    out_path: str,
    title: str,
    vmin: float,
    vmax: float,
    cmap_name: str,
) -> None:
    """Save a polygon-overlay PNG quicklook of the index."""
    # Set outside-polygon to NaN for transparent rendering
    display = np.where(mask_inside, index, np.nan)

    rows, cols = display.shape
    # Bounds for imshow extent: (left, right, bottom, top) in src CRS units
    left = transform.c
    top = transform.f
    px_w = transform.a
    px_h = transform.e  # negative for north-up
    right = left + cols * px_w
    bottom = top + rows * px_h

    fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
    im = ax.imshow(
        display,
        extent=(left, right, bottom, top),
        origin="upper",
        cmap=cmap_name,
        vmin=vmin,
        vmax=vmax,
        interpolation="nearest",
    )
    ax.add_patch(
        MplPolygon(
            polygon_xy,
            closed=True,
            fill=False,
            edgecolor="white",
            linewidth=1.4,
        )
    )
    ax.set_aspect("equal")
    ax.set_xlabel("Easting (m, EPSG:32721)")
    ax.set_ylabel("Northing (m, EPSG:32721)")
    ax.set_title(title)
    cb = fig.colorbar(im, ax=ax, shrink=0.7)
    cb.set_label(title.split(" ")[0])
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def percentile(arr: np.ndarray, q: float) -> float:
    return float(np.nanpercentile(arr, q))


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    feat = load_polygon()
    poly_4326 = feat["geometry"]

    # Reproject polygon to S2 tile CRS (EPSG:32721). We pull the dst CRS from
    # the first band rather than hard-coding it.
    with rasterio.open(
        os.path.join(SENTINEL_DIR, f"{PREFIX}_red.tif")
    ) as src:
        dst_crs = src.crs.to_string()
    poly_utm = transform_geom("EPSG:4326", dst_crs, poly_4326)

    red, transform, src_crs = read_band("red", poly_utm)
    nir, _, _ = read_band("nir", poly_utm)
    green, _, _ = read_band("green", poly_utm)

    if not (red.shape == nir.shape == green.shape):
        raise RuntimeError(
            f"Band shape mismatch: red={red.shape} nir={nir.shape} "
            f"green={green.shape} — windows misaligned"
        )

    # geometry_mask returns True OUTSIDE the polygon by default; invert for clarity.
    inside = ~geometry_mask(
        [poly_utm],
        out_shape=red.shape,
        transform=transform,
        all_touched=False,
        invert=False,
    )

    ndvi = (nir - red) / (nir + red + EPS)
    ndwi = (green - nir) / (green + nir + EPS)
    ndvi = np.clip(ndvi, -1.0, 1.0)
    ndwi = np.clip(ndwi, -1.0, 1.0)

    ndvi_in = ndvi[inside]
    ndwi_in = ndwi[inside]
    if ndvi_in.size == 0:
        raise RuntimeError(
            "No pixels inside polygon — projection or window mismatch"
        )

    # ---- Stats ---------------------------------------------------------
    stats = {
        "source_tile": PREFIX,
        "polygon_path": os.path.relpath(POLY_GEOJSON, PROJECT_ROOT),
        "polygon_area_ha_metadata": feat["properties"].get(
            "area_ha_projected_utm21s"
        ),
        "src_crs": src_crs,
        "pixel_size_m": [float(abs(transform.a)), float(abs(transform.e))],
        "window_shape": [int(red.shape[0]), int(red.shape[1])],
        "n_pixels_inside": int(ndvi_in.size),
        "n_pixels_inside_nan": int(np.isnan(ndvi_in).sum()),
        "approx_area_ha_from_pixels": float(
            np.count_nonzero(~np.isnan(ndvi_in))
            * abs(transform.a)
            * abs(transform.e)
            / 1e4
        ),
        "reflectance_transform": {
            "scale": DN_SCALE,
            "offset_applied": 0.0,
            "note": (
                "Scale-only DN→reflectance to stay consistent with "
                "make_ndvi_mask.py and the headline numbers in "
                "post_escritura_site_knowledge.md. The S2 metadata declares "
                "offset=-0.1 but applying it saturates dense-canopy NDVI at 1.0; "
                "the offset is a harmonization transform, not an analytical "
                "correction."
            ),
        },
        "ndvi": {
            "mean": float(np.nanmean(ndvi_in)),
            "median": percentile(ndvi_in, 50),
            "p05": percentile(ndvi_in, 5),
            "p25": percentile(ndvi_in, 25),
            "p75": percentile(ndvi_in, 75),
            "p95": percentile(ndvi_in, 95),
            "frac_gt_0p6": float(np.nanmean(ndvi_in > 0.6)),
            "frac_gt_0p8": float(np.nanmean(ndvi_in > 0.8)),
            "frac_lt_0p2": float(np.nanmean(ndvi_in < 0.2)),
        },
        "ndwi": {
            "mean": float(np.nanmean(ndwi_in)),
            "median": percentile(ndwi_in, 50),
            "p05": percentile(ndwi_in, 5),
            "p95": percentile(ndwi_in, 95),
            "frac_gt_0": float(np.nanmean(ndwi_in > 0)),
            "frac_gt_0p2": float(np.nanmean(ndwi_in > 0.2)),
        },
    }

    # Divergence check against the published deliverable.
    div = {}
    for key, pub in PUBLISHED.items():
        if key.startswith("ndvi_"):
            sub = key[len("ndvi_") :].replace("p25", "p25").replace("p75", "p75")
            # remap to stats keys
            mapping = {
                "median": ("ndvi", "median"),
                "p25": ("ndvi", "p25"),
                "p75": ("ndvi", "p75"),
                "frac_gt_0p6": ("ndvi", "frac_gt_0p6"),
            }
            cat, sk = mapping[sub]
        else:
            cat, sk = "ndwi", "frac_gt_0"
        got = stats[cat][sk]
        delta = got - pub
        div[key] = {"published": pub, "derived": got, "delta": delta}

    stats["published_reconciliation"] = div

    # ---- Write GeoTIFFs -------------------------------------------------
    profile = {
        "driver": "GTiff",
        "dtype": "float32",
        "count": 1,
        "height": red.shape[0],
        "width": red.shape[1],
        "transform": transform,
        "crs": src_crs,
        "nodata": np.float32(np.nan),
        "compress": "deflate",
        "predictor": 2,
        "tiled": True,
    }
    ndvi_out = np.where(inside, ndvi, np.nan).astype(np.float32)
    ndwi_out = np.where(inside, ndwi, np.nan).astype(np.float32)
    with rasterio.open(
        os.path.join(OUT_DIR, "polygon_ndvi.tif"), "w", **profile
    ) as dst:
        dst.write(ndvi_out, 1)
        dst.update_tags(
            source=PREFIX,
            description="NDVI clipped to Wesley's 30.9 ha polygon",
        )
    with rasterio.open(
        os.path.join(OUT_DIR, "polygon_ndwi.tif"), "w", **profile
    ) as dst:
        dst.write(ndwi_out, 1)
        dst.update_tags(
            source=PREFIX,
            description="NDWI(McFeeters) clipped to Wesley's 30.9 ha polygon",
        )

    # ---- Quicklooks -----------------------------------------------------
    poly_xy = np.asarray(poly_utm["coordinates"][0])
    quicklook(
        ndvi,
        inside,
        transform,
        poly_xy,
        os.path.join(OUT_DIR, "polygon_ndvi_quicklook.png"),
        "NDVI (S2 2026-05-12)",
        vmin=0.4,
        vmax=1.0,
        cmap_name="YlGn",
    )
    quicklook(
        ndwi,
        inside,
        transform,
        poly_xy,
        os.path.join(OUT_DIR, "polygon_ndwi_quicklook.png"),
        "NDWI McFeeters (S2 2026-05-12)",
        vmin=-0.8,
        vmax=0.4,
        cmap_name="Blues",
    )

    # ---- Stats JSON -----------------------------------------------------
    with open(os.path.join(OUT_DIR, "polygon_veg_stats.json"), "w") as f:
        json.dump(stats, f, indent=2)

    # ---- Stdout summary -------------------------------------------------
    print(f"[ndvi/ndwi] tile={PREFIX} CRS={src_crs}")
    print(
        f"[ndvi/ndwi] window={red.shape}, "
        f"polygon pixels={ndvi_in.size}, "
        f"~area={stats['approx_area_ha_from_pixels']:.2f} ha "
        f"(metadata={stats['polygon_area_ha_metadata']} ha)"
    )
    print(
        f"[ndvi]  median={stats['ndvi']['median']:.3f} "
        f"P25={stats['ndvi']['p25']:.3f} P75={stats['ndvi']['p75']:.3f} "
        f">0.6={stats['ndvi']['frac_gt_0p6']:.3f} "
        f">0.8={stats['ndvi']['frac_gt_0p8']:.3f}"
    )
    print(
        f"[ndwi]  median={stats['ndwi']['median']:.3f} "
        f">0={stats['ndwi']['frac_gt_0']:.3f} "
        f">0.2={stats['ndwi']['frac_gt_0p2']:.3f}"
    )
    print("[reconciliation vs post_escritura_site_knowledge.md]")
    for k, v in div.items():
        flag = " OK " if abs(v["delta"]) < 0.02 else "DIVERGE"
        print(
            f"  {flag} {k}: published={v['published']:.3f}  "
            f"derived={v['derived']:.3f}  delta={v['delta']:+.3f}"
        )


if __name__ == "__main__":
    main()
