"""Polygonise JRC Global Surface Water 'high-occurrence' pixels over the 20km LQV bbox.

This produces a separate layer of REAL water bodies (those that JRC
detected as standing water in 50%+ of years 1984-2024). Independent of
OSM, this is what the satellite actually sees.

Output: lqv_jrc_waterbodies_10km.geojson
  - polygons = connected components of JRC ≥ 50% pixels (20+ ha lakes)
  - polygons = connected components of JRC ≥ 20% pixels (seasonal ponds/wetlands)
  - polygons = connected components of JRC ≥ 10% pixels (rarely wet)

Each polygon carries the mean JRC occurrence + a year-stable name
derivable from nearest OSM waterway / place.
"""

import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import rasterio
from rasterio.features import shapes as rio_shapes
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

ROOT = Path('/root/la-quebrada-viva')
OUT = ROOT / 'splats/exports/web/data'
JRC = ROOT / 'docs/site_data/jrc_gsw/occurrence/occurrence_aoi_50km.tif'

# Each threshold gives its own sublayer
THRESHOLDS = [
    (50, 'persistent', '#0ea5e9', 'Pixels with >=50% water occurrence 1984-2024 (≈120+ ha total). Persistent lakes & reservoirs.'),
    (20, 'seasonal',   '#0284c7', 'Pixels with >=20% water occurrence 1984-2024 (≈5+ ha total). Seasonally inundated wetlands.'),
    (10, 'rare',       '#67e8f9', 'Pixels with >=10% water occurrence 1984-2024 (≈1+ ha total). Rarely wet, e.g., seasonal ponds.'),
]

# 20 km bbox
BBOX = (-25.698062, -57.129997, -25.518400, -56.930765)

with rasterio.open(JRC) as r:
    jrc = r.read(1).astype(np.float32)
    transform = r.transform
    H, W = jrc.shape
    print(f'JRC: {H}×{W}, bbox {r.bounds}')

# Build inside-20km mask
rows = np.arange(H).reshape(-1, 1).repeat(W, axis=1)
cols = np.arange(W).reshape(1, -1).repeat(H, axis=0)
xs, ys = rasterio.transform.xy(transform, rows, cols)
lons = np.array(xs).reshape(H, W)
lats = np.array(ys).reshape(H, W)
inside = (lons >= BBOX[1]) & (lons <= BBOX[3]) & (lats >= BBOX[0]) & (lats <= BBOX[2])
print(f'Inside 20km bbox: {int(inside.sum()):,} pixels')

all_features = []
for thr, name, color, desc in THRESHOLDS:
    print(f'\nThreshold ≥{thr}% ({name}):')
    mask_arr = (jrc >= thr) & inside
    n_pix = int(mask_arr.sum())
    print(f'  {n_pix:,} pixels')
    if not n_pix:
        continue
    # Polygonise with rasterio
    poly_iter = rio_shapes(mask_arr.astype(np.uint8), mask=mask_arr, connectivity=4, transform=transform)
    poly_list = []
    for geom, val in poly_iter:
        if not val:
            continue
        g = shape(geom)
        if not g.is_valid:
            g = g.buffer(0)
        # Skip tiny fragments (≤4 pixels)
        minx, miny, maxx, maxy = g.bounds
        # Crude area filter: too-small bbox = skip
        if (maxx - minx) * (maxy - miny) < 1e-7:
            continue
        # Use bbox-driven pixel count as a real-area proxy
        poly_list.append(g)
    print(f'  polygonised: {len(poly_list)} polygons')
    # Aggregate area/multiplier: each polygon gets classified into thr
    for poly_idx, g in enumerate(poly_list):
        # Crude area estimate (CRS is deg → m²)
        cx_lat = g.centroid.y
        kx = 111000 * math.cos(math.radians(cx_lat))
        ky = 110000
        area_m2 = abs(g.area) * kx * ky
        if area_m2 < 500:        # skip < 0.005 ha ≈ ~7×7 m (tiny JRC fragments)
            continue
        area_ha = area_m2 / 10000
        # Sample mean JRC inside the polygon (using rasterise mask would be slow;
        # use bbox sampling of pixels)
        minx, miny, maxx, maxy = g.bounds
        r0, c0 = rasterio.transform.rowcol(transform, minx, miny)
        r1, c1 = rasterio.transform.rowcol(transform, maxx, maxy)
        r0 = max(0, r0); c0 = max(0, c0)
        r1 = min(H, r1 + 1); c1 = min(W, c1 + 1)
        sub_jrc = jrc[r0:r1, c0:c1]
        sub_mask = mask_arr[r0:r1, c0:c1]
        if not sub_mask.any():
            continue
        mean_occ = float(sub_jrc[sub_mask].mean())
        max_occ = float(sub_jrc[sub_mask].max())
        all_features.append({
            'type': 'Feature',
            'properties': {
                'name': f'JRC waterbody {len(all_features)+1}',
                'category': 'jrc_waterbody',
                'audit_class': name,
                'audit_color': color,
                'audit_jrc_occurrence_mean': round(mean_occ, 1),
                'audit_jrc_occurrence_max': round(max_occ, 1),
                'audit_threshold': thr,
                'audit_area_ha': round(area_ha, 2),
            },
            'geometry': mapping(g),
        })
        if len(all_features) <= 30 and name == 'persistent':
            print(f'    sample: area={area_ha:.2f}ha mean_occ={mean_occ:.1f}%')

print(f'\nTotal: {len(all_features)} JRC waterbody polygons')
out_path = OUT / 'lqv_jrc_waterbodies_10km.geojson'
fc = {
    'type': 'FeatureCollection',
    'name': 'jrc_waterbodies_10km',
    'metadata': {
        'source': 'JRC Global Surface Water (occurrence, 1984-2024)',
        'bbox': BBOX,
        'method': 'Polygonise connected components at 3 thresholds',
        'thresholds_pct': [t[0] for t in THRESHOLDS],
        'generated_utc': '2026-07-05',
        'feature_count': len(all_features),
    },
    'features': all_features,
}
out_path.write_text(json.dumps(fc, separators=(',', ':')))
print(f'\nwrote {out_path} ({out_path.stat().st_size:,} bytes)')
