"""OpenStreetMap Overpass pull — 20 km radius bbox around LQV centroid.

Replaces the 5 km v2 pull so the buyer walkthrough viewer shows the full
20 km context (roads, water, towns, landuse, trees, buildings, POIs) the
user can toggle in the layer panel.

Canonical centroid (from docs/site_data/property_polygon/escobar_property_polygon.geojson):
  LON, LAT = -57.035502, -25.607336

Strategy:
  * Bbox query (`[bbox:S,W,N,E]`) rather than per-node `around:` so the
    returned geometry already covers the full area without us having to
    post-filter.
  * Run all 8 categories in a single Overpass request so we get one
    atomic snapshot and one network roundtrip.
  * 3 mirror fallback (overpass-api.de / kumi.systems / private.coffee).
  * Output: one GeoJSON FeatureCollection per category under
    docs/site_data/osm_20km/ matching the existing v2 schema (so the
    viewer can load them the same way).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "site_data" / "osm_10km"
OUT.mkdir(parents=True, exist_ok=True)

# Canonical centroid (2026-06-28 KML-derived, reinforced by property_polygon.geojson)
LON, LAT = -57.035502, -25.607336
# Bbox: S,W,N,E. 20 km radius adds 0.180° lat and 0.196° lon at this latitude.
BBOX = (LAT - 0.0898, LON - 0.0996, LAT + 0.0898, LON + 0.0996)

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]

session = requests.Session()
retry = Retry(
    total=4,
    backoff_factor=2.0,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET", "POST"),
    raise_on_status=False,
)
session.mount("https://", HTTPAdapter(max_retries=retry))
session.headers.update({"User-Agent": "lqv-20km-pull/1.0 (research; weissvanderpol.ivan@gmail.com)"})


# ---- OSM element → GeoJSON feature ----

def node_feature(el: dict) -> dict | None:
    if "lat" not in el or "lon" not in el:
        return None
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [el["lon"], el["lat"]]},
        "properties": dict(el.get("tags") or {}),
    }


def way_feature(el: dict) -> dict | None:
    geom = el.get("geometry") or []
    if not geom:
        return None
    coords = [[pt["lon"], pt["lat"]] for pt in geom]
    tags = dict(el.get("tags") or {})
    gtype = tags.get("geometry")
    # Heuristic: treat as polygon ONLY if it has explicit polygon-ish tags.
    # Default is LineString (roads, waterways, paths). area=yes forces polygon.
    natural = tags.get("natural")
    is_polygon = (
        gtype in ("Polygon", "MultiPolygon")
        or "building" in tags
        or "landuse" in tags
        or "landcover" in tags
        or natural in ("water", "wetland", "wood", "scrub", "grassland", "rock", "sand", "mud", "glacier", "bare_rock", "scree")
        or "leisure" in tags
        or "amenity" in tags
        or "aeroway" in tags
        or tags.get("area") == "yes"
    )
    # area=yes is explicit polygon
    if tags.get("area") == "yes":
        is_polygon = True
    if not is_polygon:
        return {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": tags,
        }
    # Polygon: close ring if needed
    if coords and coords[0] != coords[-1]:
        coords = coords + [coords[0]]
    return {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [coords]},
        "properties": tags,
    }


def relation_feature(el: dict) -> dict | None:
    # Outer ways only (rough — fine for rural Paraguay)
    members = el.get("members") or []
    outer_coords: list = []
    for m in members:
        if m.get("type") != "way" or m.get("role") not in ("outer", ""):
            continue
        # We don't have geometry inline for relation members; skip polygon relations
        # (most rural Paraguay data is ways anyway)
        return None
    if not outer_coords:
        return None
    return {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [outer_coords]},
        "properties": dict(el.get("tags") or {}),
    }


def element_to_feature(el: dict) -> dict | None:
    t = el.get("type")
    if t == "node":
        return node_feature(el)
    if t == "way":
        return way_feature(el)
    if t == "relation":
        return relation_feature(el)
    return None


# ---- Overpass queries ----

QUERIES: dict[str, str] = {
    # Roads + paths (all highway types, including tracks)
    "roads": (
        f"(way[\"highway\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}););"
    ),
    # Water (polygons: lakes, reservoirs, wetlands) + springs/wells
    "water": (
        f"(way[\"natural\"~\"^water$\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"way[\"natural\"~\"^wetland$\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"way[\"landuse\"=\"reservoir\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"relation[\"natural\"~\"^water$\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"node[\"natural\"=\"spring\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"node[\"man_made\"~\"water_well|spring|borehole\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}););"
    ),
    # Waterways (lines: streams, rivers, drains)
    "waterways": (
        f"(way[\"waterway\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"way[\"natural\"=\"stream\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"way[\"intermittent\"](\"yes\")[\"waterway\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}););"
    ),
    # Trees (points) + forest/wood polygons + landcover tree-related
    "trees": (
        f"(node[\"natural\"=\"tree\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"way[\"natural\"=\"tree_row\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"way[\"landuse\"~\"forest|orchard|meadow|farmland|vineyard|plant_nursery\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"way[\"natural\"=\"wood\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"way[\"landcover\"~\"trees|forest|scrub|grass|crops\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}););"
    ),
    # Buildings
    "buildings": (
        f"(way[\"building\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"relation[\"building\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}););"
    ),
    # Places (villages, hamlets, towns, suburbs, localities)
    "places": (
        f"(node[\"place\"~\"city|town|village|hamlet|suburb|locality|isolated_dwelling|farm\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"way[\"place\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}););"
    ),
    # POIs (amenity, tourism, shop, leisure)
    "pois": (
        f"(node[\"amenity\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"way[\"amenity\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"node[\"tourism\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"node[\"shop\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"node[\"leisure\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"way[\"leisure\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}););"
    ),
    # Landuse (broad polygons: residential, commercial, industrial, farmland, forest...)
    "landuse": (
        f"(way[\"landuse\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]});"
        f"relation[\"landuse\"]({BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}););"
    ),
}


def run_one_query(name: str, body: str, timeout_s: int = 180) -> list[dict]:
    q = f"[out:json][timeout:{timeout_s}];\n{body}\nout geom;"
    last_err: str | None = None
    for url in OVERPASS_URLS:
        try:
            print(f"  [{name}] → {url}")
            r = session.post(url, data={"data": q}, timeout=timeout_s + 30)
            if r.status_code == 200:
                data = r.json()
                return data.get("elements", [])
            last_err = f"{url} → HTTP {r.status_code}: {r.text[:200]}"
        except Exception as e:
            last_err = f"{url} → {type(e).__name__}: {e}"
        time.sleep(2)
    raise RuntimeError(f"[{name}] all Overpass mirrors failed. Last: {last_err}")


def main() -> int:
    print(f"=== LQV 20km OSM pull ===")
    print(f"Centroid: {LAT:.6f}, {LON:.6f}")
    print(f"Bbox S,W,N,E: {BBOX}")
    print(f"Output: {OUT}")
    print()

    total_features = 0
    for name, body in QUERIES.items():
        print(f"[{name}] querying...")
        t0 = time.time()
        try:
            elements = run_one_query(name, body)
        except Exception as e:
            print(f"  FAILED: {e}")
            # Save the error so the user can retry manually
            (OUT / f"{name}.error.txt").write_text(str(e) + "\n")
            continue
        features = []
        for el in elements:
            f = element_to_feature(el)
            if f is not None:
                features.append(f)
        out_path = OUT / f"{name}.geojson"
        fc = {
            "type": "FeatureCollection",
            "name": f"lqv_20km_{name}",
            "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
            "metadata": {
                "source": "OpenStreetMap via Overpass API",
                "centroid_lon": LON,
                "centroid_lat": LAT,
                "bbox": list(BBOX),
                "radius_km": 20,
                "category": name,
                "feature_count": len(features),
                "element_count": len(elements),
                "pulled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            "features": features,
        }
        out_path.write_text(json.dumps(fc, separators=(",", ":")))
        dt = time.time() - t0
        print(f"  → {len(features):5d} features in {dt:.1f}s ({len(elements)} elements) [{out_path.stat().st_size:,} bytes]")
        total_features += len(features)

    print()
    print(f"=== DONE — {total_features:,} features across {len(QUERIES)} layers ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())