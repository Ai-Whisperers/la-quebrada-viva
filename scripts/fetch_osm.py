"""OpenStreetMap (Overpass API) — site-context features around the 62-ha property.

Free, no auth. Pulls:
  - roads within 5 km (tracks, paths, residential, tertiary, secondary)
  - buildings within 1 km (existing structures on/near the site)
  - nearby POIs: hotels, restaurants, schools, German bakeries, etc.
  - nearby place names (helps us find San Bernardino-style German colonies)
  - nearby water features (rivers, streams)

Outputs:
  - docs/site_data/osm/roads.geojson
  - docs/site_data/osm/buildings.geojson
  - docs/site_data/osm/pois.geojson
  - docs/site_data/osm/water.geojson
  - docs/site_data/osm/places.geojson
  - docs/site_data/osm_summary.txt
"""
import json
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

HERE = Path('/home/ai-whisperers/blender-projects/la-quebrada-viva')
load_dotenv(dotenv_path=HERE / '.env.local')

PROP_CENTER = (-25.630, -57.030)  # centroid of the 3.3 km bbox
OUT_DIR = HERE / 'docs' / 'site_data' / 'osm'
OUT_DIR.mkdir(parents=True, exist_ok=True)

OVERPASS_URLS = [
    'https://overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
    'https://overpass.private.coffee/api/interpreter',
]

QUERIES = {
    'roads': f"""
[out:json][timeout:60];
way["highway"~"residential|tertiary|secondary|primary|track|path|unclassified|service"]
  ({PROP_CENTER[1]-0.05},{PROP_CENTER[0]-0.05},
   {PROP_CENTER[1]+0.05},{PROP_CENTER[0]+0.05});
out body; >; out skel qt;
""",
    'buildings': f"""
[out:json][timeout:60];
way["building"]
  ({PROP_CENTER[1]-0.01},{PROP_CENTER[0]-0.01},
   {PROP_CENTER[1]+0.01},{PROP_CENTER[0]+0.01});
out body; >; out skel qt;
""",
    'pois': f"""
[out:json][timeout:60];
(
  node["amenity"~"restaurant|cafe|school|place_of_worship|hospital|bank|fire_station|police"]
    ({PROP_CENTER[1]-0.10},{PROP_CENTER[0]-0.10},
     {PROP_CENTER[1]+0.10},{PROP_CENTER[0]+0.10});
  way["amenity"~"restaurant|cafe|school|place_of_worship|hospital"]
    ({PROP_CENTER[1]-0.10},{PROP_CENTER[0]-0.10},
     {PROP_CENTER[1]+0.10},{PROP_CENTER[0]+0.10});
  node["tourism"~"hotel|hostel|guest_house|attraction|museum"]
    ({PROP_CENTER[1]-0.10},{PROP_CENTER[0]-0.10},
     {PROP_CENTER[1]+0.10},{PROP_CENTER[0]+0.10});
  node["shop"~"bakery|supermarket|convenience"]
    ({PROP_CENTER[1]-0.10},{PROP_CENTER[0]-0.10},
     {PROP_CENTER[1]+0.10},{PROP_CENTER[0]+0.10});
);
out body;
""",
    'water': f"""
[out:json][timeout:60];
(
  way["natural"~"water|riverbank|stream"]
    ({PROP_CENTER[1]-0.05},{PROP_CENTER[0]-0.05},
     {PROP_CENTER[1]+0.05},{PROP_CENTER[0]+0.05});
  way["waterway"~"river|stream|canal|drain"]
    ({PROP_CENTER[1]-0.05},{PROP_CENTER[0]-0.05},
     {PROP_CENTER[1]+0.05},{PROP_CENTER[0]+0.05});
);
out body;
""",
    'places': f"""
[out:json][timeout:60];
node["place"~"village|town|hamlet|suburb|locality|neighbourhood"]
  ({PROP_CENTER[1]-0.30},{PROP_CENTER[0]-0.30},
   {PROP_CENTER[1]+0.30},{PROP_CENTER[0]+0.30});
out body;
""",
}

def overpass(query: str, attempts: int = 3):
    last_err = None
    for i in range(attempts):
        for url in OVERPASS_URLS:
            try:
                r = requests.post(url, data={'data': query}, timeout=120)
                r.raise_for_status()
                return r.json()
            except Exception as e:
                last_err = e
                time.sleep(1)
    raise RuntimeError(f"overpass failed after {attempts}×{len(OVERPASS_URLS)} attempts: {last_err}")


def to_geojson(elements):
    """Convert Overpass JSON to GeoJSON FeatureCollection (Points + LineStrings)."""
    features = []
    for el in elements:
        kind = el.get('type')
        tags = el.get('tags', {})
        if kind == 'node':
            lon, lat = el.get('lon'), el.get('lat')
            if lon is None or lat is None:
                continue
            features.append({
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [lon, lat]},
                'properties': tags,
            })
        elif kind == 'way':
            coords = []
            for n in el.get('geometry', []):
                lon, lat = n.get('lon'), n.get('lat')
                if lon is not None and lat is not None:
                    coords.append([lon, lat])
            if len(coords) < 2:
                continue
            features.append({
                'type': 'Feature',
                'geometry': {'type': 'LineString', 'coordinates': coords},
                'properties': tags,
            })
    return {'type': 'FeatureCollection', 'features': features}


def main():
    print("=" * 70)
    print(f"OpenStreetMap (Overpass) — {PROP_CENTER} ±0.05° (~5 km)")
    print("=" * 70)
    summary = []
    for name, query in QUERIES.items():
        print(f"\n[{name}] querying Overpass…", flush=True)
        t0 = time.time()
        try:
            data = overpass(query)
        except Exception as e:
            print(f"  FAILED: {e}")
            summary.append(f"{name}: FAILED {e}")
            continue
        elements = data.get('elements', [])
        geo = to_geojson(elements)
        out = OUT_DIR / f"{name}.geojson"
        with open(out, 'w') as f:
            json.dump(geo, f, indent=2)
        n = len(geo['features'])
        elapsed = time.time() - t0
        print(f"  {n} features, {elapsed:.1f}s  →  {out.relative_to(HERE)}")
        summary.append(f"{name}: {n} features  ({elapsed:.1f}s)")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for s in summary:
        print(f"  {s}")
    with open(OUT_DIR / 'osm_summary.txt', 'w') as f:
        f.write('\n'.join(summary) + '\n')
    print(f"\nSummary written to {OUT_DIR / 'osm_summary.txt'}")


if __name__ == '__main__':
    main()
