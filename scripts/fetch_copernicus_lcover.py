"""Copernicus Global Land Service (CGLS) Land Cover 100m — annual maps.

Free, no auth. Pulls the most recent CGLS-LC100 (Corine-style) annual land cover
map for the 3.3 km bbox. Resolution is 100 m (better than 30 m DEMs for land cover).

CGLS-LC100 uses discrete classification (44 classes in CLC legend) derived from
Sentinel-2 + PROBA-V. Annual products from 2015-2023.

Outputs:
  - docs/site_data/cgls_lcover/metadata.json
  - docs/site_data/cgls_lcover/lcover.tif           (clipped to bbox)
  - docs/site_data/cgls_lcover/lcover_preview.png  (RGB false-color preview)
  - docs/site_data/cgls_lcover/lcover_summary.txt  (class breakdown)
"""
import json
import sys
from pathlib import Path

import numpy as np
import requests
from dotenv import load_dotenv

HERE = Path('/home/ai-whisperers/blender-projects/house-field')
load_dotenv(dotenv_path=HERE / '.env.local')

BBOX = {'south': -25.645, 'north': -25.615, 'west': -57.045, 'east': -57.015}
OUT_DIR = HERE / 'docs' / 'site_data' / 'cgls_lcover'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# CGLS LC100 product — v3 annual tiles
# Collection: CGSL-LC100 — hosted on Creodsa (ESA partner)
# Direct download: https://gws-access.jrc.ec.europa.eu/api/cgislc100v3?tile=R21JVM&year=2022
# Alternative: CopHub API (needs auth) or direct CGI download
# Let's try the direct JRC download first

# Tile naming: R21JVM matches our UTM zone 21S + band J + VM tile
TILE = 'R21JVM'
YEARS = [2022, 2021, 2020]  # try newest first

BASE_URL = 'https://gws-access.jrc.ec.europa.eu/api/cgislc100v3'


def try_download_year(year: int):
    """Try to download LC100 tile for given year."""
    url = f'{BASE_URL}?tile={TILE}&year={year}'
    print(f'  trying {year}: {url[:80]}…', end=' ', flush=True)
    try:
        r = requests.get(url, timeout=60, stream=True)
        if r.status_code == 200:
            content_type = r.headers.get('Content-Type', '')
            content_length = r.headers.get('Content-Length', 'unknown')
            print(f'OK ({content_type}, {content_length} bytes)')
            return r
        else:
            print(f'HTTP {r.status_code}')
            return None
    except Exception as e:
        print(f'{type(e).__name__}: {str(e)[:60]}')
        return None


def crop_to_bbox(in_path: Path, out_path: Path):
    """Crop the GeoTIFF to the site bbox."""
    import rasterio
    from rasterio.windows import from_bounds
    with rasterio.open(in_path) as src:
        win = from_bounds(BBOX['west'], BBOX['south'], BBOX['east'], BBOX['north'], src.transform)
        win = win.intersection(rasterio.windows.Window(0, 0, src.width, src.height))
        if win.width < 1 or win.height < 1:
            print(f'  Window too small ({win.width}x{win.height}), skipping crop')
            return False
        data = src.read(window=win)
        new_transform = src.window_transform(win)
        profile = src.profile.copy()
        profile.update({
            'height': data.shape[1], 'width': data.shape[2],
            'transform': new_transform, 'driver': 'GTiff',
            'count': data.shape[0], 'dtype': data.dtype,
        })
        with rasterio.open(out_path, 'w', **profile) as dst:
            dst.write(data)
    return True


def generate_preview(tif_path: Path, out_png: Path):
    """Generate a false-color RGB preview of the land cover."""
    import matplotlib
    import numpy as np
    import rasterio
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    with rasterio.open(tif_path) as src:
        data = src.read(1).astype(float)

    # Class colors for common CGLS LC100 classes (RGB triplets)
    # Based on CGLS color table: https://lcviewer.copernicus.eu/
    # Key classes relevant to our site:
    CLASS_COLORS = {
        111: (0, 60, 0),       # Closed forest, needle
        112: (30, 90, 0),      # Closed forest, mixed
        113: (40, 100, 0),     # Closed forest, maritime pine
        114: (60, 120, 0),     # Closed forest, eucalypt
        115: (80, 140, 0),     # Closed forest, not reaching temperate
        116: (0, 100, 0),      # Closed forest, flooded
        121: (0, 120, 0),      # Open forest, needle
        122: (60, 100, 0),     # Open forest, mixed
        123: (80, 120, 0),     # Open forest, maritime pine
        124: (100, 140, 0),    # Open forest, eucalypt
        125: (120, 160, 0),    # Open forest, not reaching temperate
        126: (0, 110, 0),      # Open forest, flooded
        131: (80, 60, 0),      # Open forest, burned
        141: (150, 150, 100),  # Agriculture, herbaceous
        142: (200, 180, 100),  # Agriculture, irrigated
        150: (180, 200, 100),  # Agriculture, transitional
        210: (200, 200, 200),  # Bare
        220: (170, 160, 140),  # Grassland
        230: (220, 220, 200),  # Open with sparse vegetation
        40: (120, 100, 80),    # Wetland (shorthand)
        500: (0, 100, 100),    # Water (shorthand)
    }

    # Build color map for all classes
    classes_present = np.unique(data)
    cmap = np.zeros((256, 3), dtype=np.uint8)
    for cls in classes_present:
        if cls in CLASS_COLORS:
            cmap[int(cls)] = CLASS_COLORS.get(int(cls), [128, 128, 128])
        else:
            # Generate a pseudo-color for unknown classes
            import random
            random.seed(int(cls))
            cmap[int(cls)] = [random.randint(60, 180) for _ in range(3)]

    rgb = cmap[data.astype(np.uint8)]

    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
    ax.imshow(rgb, origin='upper', aspect='auto')
    ax.set_title(f'CGLS LC100 — {tif_path.stem}\nEscobar / Mbopicua, PY | Classes: {len(classes_present)}')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle((BBOX['west'], BBOX['south']),
                            BBOX['east']-BBOX['west'],
                            BBOX['north']-BBOX['south'],
                            fill=False, edgecolor='red', linewidth=2,
                            label='62 ha search bbox'))
    ax.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(out_png, dpi=100, bbox_inches='tight')
    plt.close()
    print(f'  preview → {out_png} ({out_png.stat().st_size//1024} KB)')


def summarize_classes(tif_path: Path, out_txt: Path):
    """Count pixels per class and write summary."""
    import rasterio
    with rasterio.open(tif_path) as src:
        data = src.read(1)
    unique, counts = np.unique(data, return_counts=True)
    total = counts.sum()
    lines = ['CGLS LC100 Class Distribution', '=' * 50, f'Tile: {TILE}', f'Total pixels: {total} (100m res)', f'Coverage: {total * 10000:.0f} m²', '']
    lines.append(f'{"Class":>6}  {"Count":>8}  {"%":>6}  Description')
    lines.append('-' * 50)
    class_names = {
        111: 'Closed forest, needle-leaved', 112: 'Closed forest, mixed',
        113: 'Closed forest, maritime pine', 114: 'Closed forest, eucalypt',
        121: 'Open forest, needle-leaved', 122: 'Open forest, mixed',
        123: 'Open forest, maritime pine', 124: 'Open forest, eucalypt',
        141: 'Agriculture, herbaceous', 142: 'Agriculture, irrigated',
        150: 'Agriculture, transitional', 210: 'Bare rocky', 220: 'Grassland',
        230: 'Open with sparse vegetation', 40: 'Wetland', 500: 'Water bodies',
    }
    for cls, cnt in sorted(zip(unique, counts), key=lambda x: -x[1]):
        pct = cnt / total * 100
        name = class_names.get(int(cls), f'Class {cls}')
        lines.append(f'{int(cls):>6}  {cnt:>8}  {pct:>5.1f}%  {name}')
    with open(out_txt, 'w') as f:
        f.write('\n'.join(lines))
    print(f'  summary → {out_txt}')


def main():
    print('=' * 70)
    print('CGLS Land Cover 100m — v3 annual product')
    print(f'Tile: {TILE} | Bbox: W={BBOX["west"]} S={BBOX["south"]} E={BBOX["east"]} N={BBOX["north"]}')
    print('=' * 70)


    # Try direct JRC API first
    response = None
    for year in YEARS:
        response = try_download_year(year)
        if response is not None:
            break

    if response is None or response.status_code != 200:
        print('\nDirect JRC download unavailable. Trying CopHub STAC…')
        # Try CopHub STAC as fallback
        stac_url = 'https://catalogue.dataspace.copernicus.eu/stac'
        try:
            r = requests.get(f'{stac_url}/collections', timeout=30)
            print(f'  CopHub collections: {r.status_code}')
        except Exception as e:
            print(f'  CopHub also failed: {type(e).__name__}: {str(e)[:80]}')
        print('\n[NOTE] CGLS LC100 requires manual download from:')
        print('  https://lcviewer.copernicus.eu/ → Download → Land Cover → 100m')
        print('  Tile R21JVM covers our site. Save as docs/site_data/cgls_lcover/lcover.tif')
        return 1

    # Save raw tile
    raw = OUT_DIR / f'cgsl_lc100_{TILE}_raw.tif'
    with open(raw, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024 * 64):
            f.write(chunk)
    print(f'  raw tile → {raw} ({raw.stat().st_size//1024//1024} MB)')

    # Crop to bbox
    cropped = OUT_DIR / 'lcover.tif'
    print('  cropping to site bbox…', end=' ', flush=True)
    if crop_to_bbox(raw, cropped):
        print(f'OK ({cropped.stat().st_size//1024} KB)')
        # Generate preview + summary
        import random
        random.seed(42)
        generate_preview(cropped, OUT_DIR / 'lcover_preview.png')
        summarize_classes(cropped, OUT_DIR / 'lcover_summary.txt')
    else:
        print('crop failed')

    # Metadata
    meta = {
        'product': 'CGLS-LC100 v3',
        'tile': TILE,
        'year': year,
        'bbox': BBOX,
        'source': f'{BASE_URL}?tile={TILE}&year={year}',
        'resolution_m': 100,
        'classes': 44,
    }
    with open(OUT_DIR / 'metadata.json', 'w') as f:
        json.dump(meta, f, indent=2)
    print(f'  metadata → {OUT_DIR / "metadata.json"}')
    print('\nDONE.')
    return 0


if __name__ == '__main__':
    sys.exit(main())