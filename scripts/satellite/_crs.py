"""CRS normalization helper.

Canonical projection for La Quebrada Viva site data is **EPSG:32721**
(WGS84 / UTM 21S, +south). Covers Paraguay; near-equal-area for a 62-ha
AOI. Every fetcher reprojects to this CRS before writing so downstream
overlay / area / hydrology math is consistent.

If you need geographic coordinates for a specific output (e.g. raw STAC
search bbox), use EPSG:4326 explicitly via a per-call override.
"""
from __future__ import annotations

CANONICAL_CRS = "EPSG:32721"


def to_canonical(da):
    """Reproject a rioxarray DataArray to EPSG:32721 if not already there.

    No-op if already in the canonical CRS or if rio accessor not loaded.
    """
    try:
        import rioxarray  # noqa: F401
    except ImportError:
        return da
    src_crs = getattr(da.rio, "crs", None)
    if src_crs is None:
        return da
    if str(src_crs).upper() == CANONICAL_CRS.upper():
        return da
    return da.rio.reproject(CANONICAL_CRS)


def to_canonical_inplace_path(path) -> bool:
    """Reproject a GeoTIFF on disk to EPSG:32721 in place (write+rename).

    Returns True if reprojected, False if already canonical or rasterio missing.
    """
    try:
        import rasterio
        from rasterio.warp import calculate_default_transform, reproject
    except ImportError:
        return False
    from pathlib import Path

    path = Path(path)
    with rasterio.open(path) as src:
        if str(src.crs).upper() == CANONICAL_CRS.upper():
            return False
        transform, width, height = calculate_default_transform(
            src.crs, CANONICAL_CRS, src.width, src.height, *src.bounds,
        )
        profile = src.profile.copy()
        profile.update(
            crs=CANONICAL_CRS, transform=transform,
            width=width, height=height, compress="DEFLATE", tiled=True,
        )
        tmp = path.with_suffix(path.suffix + ".reproj.tmp")
        with rasterio.open(tmp, "w", **profile) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform, src_crs=src.crs,
                    dst_transform=transform, dst_crs=CANONICAL_CRS,
                )
    tmp.replace(path)
    return True
