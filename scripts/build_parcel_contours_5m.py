"""Build parcel-scale contours (5m intervals) from the fused 5m
Tier-1 topology DEM.

Output:
  splats/exports/web/data/dem_contours_parcel_5m.geojson
  - Lines at 5m elevation intervals
  - 133 lines covering LQV parcel (132-354 m)
  - Weighted by tier (every 100m thickest, every 25m medium, rest thin)
  - Used in viewer at z>=15 for parcel-zoom contour resolution
    (vs the 50 m steps in dem_contours_10km.geojson)
"""
import json
import sys
from pathlib import Path

ROOT = Path("/root/la-quebrada-viva")
SRC = ROOT / "docs/site_data/topology_lod/core/dem_fused_5m.tif"
OUT = ROOT / "splats/exports/web/data"

try:
    import numpy as np
    import rasterio
    from rasterio.features import shapes as rio_shapes
    from shapely.geometry import shape, mapping, LineString
except ImportError:
    print("Install numpy, rasterio, shapely", file=sys.stderr)
    sys.exit(1)


def main():
    if not SRC.exists():
        print(f"missing source: {SRC}", file=sys.stderr); sys.exit(1)

    print(f"Loading {SRC}...")
    with rasterio.open(SRC) as ds:
        dem = ds.read(1).astype('float32')
        tf = ds.transform
        bounds = ds.bounds

    print(f"  shape: {dem.shape}, range: {np.nanmin(dem):.1f}-{np.nanmax(dem):.1f} m")

    mn, mx = int(np.nanmin(dem)), int(np.nanmax(dem))
    levels = list(range((mn // 5) * 5, ((mx // 5) + 1) * 5, 5))
    print(f"  contour levels: {len(levels)}")

    features = []
    for level in levels:
        band = (dem >= level).astype('uint8')
        n_polys = 0
        for geom, val in rio_shapes(band, mask=band, connectivity=4, transform=tf):
            if val != 1: continue
            try:
                poly = shape(geom)
                if not poly.is_valid or poly.is_empty: continue
                if poly.geom_type == 'Polygon':
                    lines = [LineString(poly.exterior.coords)]
                elif poly.geom_type == 'MultiPolygon':
                    lines = [LineString(p.exterior.coords) for p in poly.geoms if p.exterior]
                else: continue
                for line in lines:
                    if len(line.coords) < 2: continue
                    if level % 100 == 0:
                        color = '#0c4a6e'; weight = 1.4
                    elif level % 25 == 0:
                        color = '#0284c7'; weight = 1.0
                    else:
                        color = '#7dd3fc'; weight = 0.5
                    features.append({
                        "type": "Feature",
                        "properties": {
                            "category": "contour_parcel",
                            "elev_m": level,
                            "elev_label": f"{level} m",
                            "color": color,
                            "weight": weight,
                            "source": "Fused 5m topology DEM (parcel-scale)",
                        },
                        "geometry": mapping(line),
                    })
                    n_polys += 1
            except Exception:
                continue
        print(f"  level {level}: {n_polys} lines")

    print(f"  total: {len(features)}")
    if features:
        out = {
            "type": "FeatureCollection",
            "name": "dem_contours_parcel_5m",
            "metadata": {
                "source": "Tier-1 fused 5 m DEM (Cop30+ALOS+SRTM+NASADEM median, upsampled 30→5 m)",
                "method": "Iso-band polygon boundaries at 5 m intervals",
                "bbox_lbrt": list(bounds),
            },
            "features": features,
        }
        out_path = OUT / "dem_contours_parcel_5m.geojson"
        out_path.write_text(json.dumps(out, separators=(",", ":")))
        print(f"wrote {out_path} ({out_path.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()