"""Sentinel-2 L2A surface reflectance — satellite imagery for the property.

Uses the element84 Earth-Search STAC catalog (no auth, no signup).
Finds the lowest-cloud Sentinel-2 L2A scene over our 3.3 km bbox in
the last 2 years, downloads the RGB + NIR + SWIR bands at 10-20 m,
saves as a multiband GeoTIFF + a quick PNG preview.

Outputs:
  - docs/site_data/sentinel2/metadata.json
  - docs/site_data/sentinel2/sentinel2_<scene_id>_<bands>.tif
  - docs/site_data/sentinel2/preview_rgb.png
"""
import json
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

from scripts.satellite._aoi import aoi_bbox
from scripts.satellite._crs import to_canonical_inplace_path
from scripts.satellite._license import assert_compatible
from scripts.satellite._meta import write_sidecar
from scripts.satellite._retry import skip_if_exists, with_retry

# Repo root = three levels up from this file (scripts/satellite/fetch_sentinel2.py).
HERE = Path(__file__).resolve().parents[2]
load_dotenv(dotenv_path=HERE / '.env.local')

_w, _s, _e, _n = aoi_bbox()
BBOX = {'south': _s, 'north': _n, 'west': _w, 'east': _e}
OUT_DIR = HERE / 'docs' / 'site_data' / 'sentinel2'
OUT_DIR.mkdir(parents=True, exist_ok=True)

STAC_URL = 'https://earth-search.aws.element84.com/v1/search'

# Sentinel-2 L2A (surface reflectance, ~ 5-day revisit, 10 m RGB/NIR, 20 m SWIR)
COLLECTION = 'sentinel-2-l2a'

# Copernicus Sentinel-2 L2A is released under the ESA Legal Notice on the use of
# Copernicus Sentinel data — bundle-eligible, equivalent to CC-BY-4.0 attribution
# requirements. See LICENSE_BUNDLE.md §3.
LICENSE_ID = 'CC-BY-4.0'
CITATION = (
    'Contains modified Copernicus Sentinel data, processed by ESA / element84 '
    'Earth-Search (sentinel-2-l2a).'
)

# Bands we want (element84 STAC uses human-readable keys, not Sentinel-2 band numbers):
#   red=B04, green=B03, blue=B02 (10m), nir=B08 (10m), swir16=B11 (20m), scl=scene-class (20m)
BANDS = ['red', 'green', 'blue', 'nir', 'swir16', 'scl']

MAX_CLOUD_PCT = 20.0  # tightest cloud filter
DAYS_BACK = 730       # last 2 years


@with_retry()
def _download_band(url: str, out: Path) -> None:
    """Stream a single Sentinel-2 band tile to ``out`` atomically via .tmp."""
    tmp = out.with_suffix(out.suffix + '.tmp')
    with requests.get(url, stream=True, timeout=180) as r:
        r.raise_for_status()
        with open(tmp, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 64):
                f.write(chunk)
    tmp.replace(out)


def _process_band(
    band: str,
    url: str,
    out: Path,
    *,
    item_id: str,
    cloud_cover: float | None,
) -> None:
    """Download (with retry) + CRS normalize + write sidecar for one band."""
    # License gate runs first — raises LicenseBlocked if the constant is wrong.
    assert_compatible(LICENSE_ID)

    if skip_if_exists(out):
        print(f"  {band}: cached ({out.stat().st_size // 1024} KB)")
    else:
        print(f"  {band}: downloading from {url[:80]}…", end=' ', flush=True)
        t0 = time.time()
        _download_band(url, out)
        print(f"{out.stat().st_size // 1024} KB  ({time.time() - t0:.1f}s)")

    # Normalize CRS to EPSG:32721 — no-op if the L2A scene is already UTM 21S.
    try:
        to_canonical_inplace_path(out)
    except Exception as e:
        print(f"  {band}: WARN CRS normalize skipped: {type(e).__name__}: {e}")

    write_sidecar(
        out,
        source=url,
        collection=COLLECTION,
        license_id=LICENSE_ID,
        citation=CITATION,
        fetcher='scripts.satellite.fetch_sentinel2',
        extra={
            'item_id': item_id,
            'band': band,
            'cloud_cover': cloud_cover,
        },
    )


def find_best_scene():
    end = datetime.now(UTC)
    start = end - timedelta(days=DAYS_BACK)
    body = {
        'collections': [COLLECTION],
        'bbox': [BBOX['west'], BBOX['south'], BBOX['east'], BBOX['north']],
        'datetime': f'{start.isoformat()}/{end.isoformat()}',
        'query': {'eo:cloud_cover': {'lt': MAX_CLOUD_PCT}},
        'limit': 5,
    }
    r = requests.post(STAC_URL, json=body, timeout=60)
    r.raise_for_status()
    feats = r.json().get('features', [])
    if not feats:
        # Try with relaxed cloud cover
        body['query']['eo:cloud_cover']['lt'] = 50.0
        r = requests.post(STAC_URL, json=body, timeout=60)
        r.raise_for_status()
        feats = r.json().get('features', [])
    # Sort by cloud cover ascending (lowest first)
    feats.sort(key=lambda f: f['properties'].get('eo:cloud_cover', 999))
    return feats


def main():
    print("=" * 70)
    print("Sentinel-2 L2A (element84 STAC, no auth)")
    print(f"Bbox: W={BBOX['west']} S={BBOX['south']} E={BBOX['east']} N={BBOX['north']}")
    print("=" * 70)

    print("\n[1/4] Searching STAC catalog (last 2y, cloud < 20%)…")
    scenes = find_best_scene()
    if not scenes:
        print("  FAILED — no scenes found, even relaxed to 50% cloud. Try widening bbox.")
        return 1
    print(f"  {len(scenes)} candidates (sorted by cloud cover)")
    for s in scenes:
        cc = s['properties'].get('eo:cloud_cover', '?')
        date = s['properties'].get('datetime', '?')[:10]
        print(f"    {date}  cloud {cc}%  {s['id'][:30]}…")

    best = scenes[0]
    print(f"\n  picking: {best['id']}  ({best['properties'].get('eo:cloud_cover')}% cloud)")
    with open(OUT_DIR / 'metadata.json', 'w') as f:
        # Strip non-serializable parts (Assets dict is fine but keep clean)
        meta = {k: v for k, v in best.items() if k != 'links'}
        meta['bbox_search'] = BBOX
        json.dump(meta, f, indent=2, default=str)
    print(f"  metadata → {OUT_DIR / 'metadata.json'}")

    print(f"\n[2/4] Downloading {len(BANDS)} bands (red green blue nir swir16 scl)…")
    assets = best['assets']
    downloaded = {}
    item_id = best['id']
    cloud_cover = best['properties'].get('eo:cloud_cover')
    for band in BANDS:
        if band not in assets:
            print(f"  {band}: not in scene assets, skipping")
            continue
        url = assets[band]['href']
        out = OUT_DIR / f"{item_id}_{band}.tif"
        try:
            _process_band(band, url, out, item_id=item_id, cloud_cover=cloud_cover)
            downloaded[band] = out
        except Exception as e:
            print(f"  {band}: FAILED after retries: {type(e).__name__}: {str(e)[:120]}")

    if not downloaded:
        print("  no bands downloaded — aborting")
        return 1

    print("\n[3/4] Building composite RGB preview from red/green/blue…")
    try:
        import numpy as np
        import rasterio
        with rasterio.open(downloaded['red']) as r4, \
             rasterio.open(downloaded['green']) as r3, \
             rasterio.open(downloaded['blue']) as r2:
            r = r4.read(1).astype(float)
            g = r3.read(1).astype(float)
            b = r2.read(1).astype(float)
            # reflectance scale: L2A is 0-10000 (scaled), divide to 0-1
            r, g, b = r / 10000.0, g / 10000.0, b / 10000.0
            # simple clip
            r = np.clip(r, 0, 0.3) / 0.3
            g = np.clip(g, 0, 0.3) / 0.3
            b = np.clip(b, 0, 0.3) / 0.3
            rgb = np.stack([r, g, b], axis=-1)
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 10), dpi=120)
            extent = [r4.bounds.left, r4.bounds.right, r4.bounds.bottom, r4.bounds.top]
            ax.imshow(rgb, extent=extent, origin='upper')
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            ax.set_title(f"Sentinel-2 L2A RGB — Escobar / Mbopicua, PY\n"
                         f"Scene: {best['id']}  |  {best['properties'].get('eo:cloud_cover')}% cloud")
            # Overlay our 62 ha search bbox
            from matplotlib.patches import Rectangle
            ax.add_patch(Rectangle((BBOX['west'], BBOX['south']),
                                   BBOX['east']-BBOX['west'],
                                   BBOX['north']-BBOX['south'],
                                   fill=False, edgecolor='red', linewidth=2,
                                   label='search bbox (62 ha)'))
            ax.legend(loc='lower right')
            plt.tight_layout()
            out_png = OUT_DIR / 'preview_rgb.png'
            plt.savefig(out_png, dpi=120, bbox_inches='tight')
            plt.close()
            print(f"  preview → {out_png}")
    except Exception as e:
        print(f"  preview failed: {type(e).__name__}: {str(e)[:100]}")

    print("\n[4/4] Summary")
    print(f"  Scene: {best['id']}")
    print(f"  Date: {best['properties'].get('datetime', '?')[:10]}")
    print(f"  Cloud: {best['properties'].get('eo:cloud_cover')}%")
    print(f"  Bands downloaded: {sorted(downloaded.keys())}")
    print(f"  Total: {sum(p.stat().st_size for p in downloaded.values())//1024} KB")
    print("\nDONE.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
