"""OpenStreetMap Overpass pull v2 — 5 km radius around KML-derived parcel centroid.

Fixes the 2026-06-18 pull (0 features for all categories) which had two bugs:
 1. PROP_CENTER was -57.030,-25.630 (pre-KML; ~0.7 km outside actual polygon).
 2. Queries used `out body; >; out skel qt;` which omits coordinates from way
    geometries, so the GeoJSON conversion silently produced empty FeatureCollections.

This v2 uses `(around:5000,lat,lon)` filters from the true KML centroid + `out geom;`
so way coordinates come back inline. Pulls 8 categories addressing the
data-completeness directive: buildings, water, waterways, springs/wells, trees,
roads, POIs, places, landuse.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "site_data" / "osm"
OUT.mkdir(parents=True, exist_ok=True)

# KML-derived centroid (2026-06-28).
LON, LAT = -57.0355, -25.6073
RADIUS_M = 5000
RADIUS_LARGE_M = 15000  # for place lookup (villages/hamlets)

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
]

session = requests.Session()
retry = Retry(total=4, backoff_factor=2.0, status_forcelist=(429, 500, 502, 503, 504),
              allowed_methods=("GET", "POST"), raise_on_status=False)
session.mount("https://", HTTPAdapter(max_retries=retry))
session.headers.update({"User-Agent": "lqv-phase0/1.0 (research; weissvanderpol.ivan@gmail.com)"})


def query(name: str, body: str, radius_m: int = RADIUS_M) -> dict:
    q = f"[out:json][timeout:120];\n{body.format(r=radius_m, lat=LAT, lon=LON)}\nout geom;"
    last_err = None
    for url in OVERPASS_URLS:
        try:
            r = session.post(url, data={"data": q}, timeout=180)
            if r.status_code == 200:
                return r.json()
            last_err = f"{url} -> HTTP {r.status_code}"
        except Exception as e:
            last_err = f"{url} -> {e}"
            time.sleep(2)
    raise RuntimeError(f"[{name}] all Overpass mirrors failed; last: {last_err}")


CATEGORIES = {
    "buildings": (
        "(way[\"building\"](around:{r},{lat},{lon});"
        "relation[\"building\"](around:{r},{lat},{lon}););"
    ),
    "water": (
        "(way[\"natural\"~\"water|wetland|spring\"](around:{r},{lat},{lon});"
        "way[\"landuse\"=\"reservoir\"](around:{r},{lat},{lon});"
        "way[\"man_made\"~\"reservoir_covered|water_tank|water_well|water_works\"](around:{r},{lat},{lon});"
        "node[\"man_made\"~\"spring|water_well|water_tap|borehole\"](around:{r},{lat},{lon});"
        "node[\"natural\"=\"spring\"](around:{r},{lat},{lon}););"
    ),
    "waterways": (
        "(way[\"waterway\"](around:{r},{lat},{lon});"
        "relation[\"waterway\"](around:{r},{lat},{lon}););"
    ),
    "trees": (
        "(node[\"natural\"=\"tree\"](around:{r},{lat},{lon});"
        "way[\"natural\"=\"tree_row\"](around:{r},{lat},{lon});"
        "way[\"landuse\"~\"forest|orchard|meadow|farmland|vineyard\"](around:{r},{lat},{lon});"
        "way[\"natural\"=\"wood\"](around:{r},{lat},{lon}););"
    ),
    "roads": (
        "(way[\"highway\"](around:{r},{lat},{lon}););"
    ),
    "pois": (
        "(node[\"amenity\"](around:{r},{lat},{lon});"
        "way[\"amenity\"](around:{r},{lat},{lon});"
        "node[\"tourism\"](around:{r},{lat},{lon});"
        "node[\"shop\"](around:{r},{lat},{lon});"
        "node[\"leisure\"](around:{r},{lat},{lon});"
        "way[\"leisure\"](around:{r},{lat},{lon}););"
    ),
    "landuse": (
        "(way[\"landuse\"](around:{r},{lat},{lon});"
        "relation[\"landuse\"](around:{r},{lat},{lon}););"
    ),
}

PLACE_QUERY = (
    "(node[\"place\"](around:{r},{lat},{lon});"
    "way[\"place\"](around:{r},{lat},{lon}););"
)


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r_earth = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r_earth * math.asin(math.sqrt(a))


def feature_centroid(el: dict) -> tuple[float, float] | None:
    if el["type"] == "node":
        return (el["lat"], el["lon"])
    geom = el.get("geometry") or []
    if not geom:
        return None
    lat = sum(g["lat"] for g in geom) / len(geom)
    lon = sum(g["lon"] for g in geom) / len(geom)
    return (lat, lon)


def to_geojson(elements: list[dict]) -> dict:
    features = []
    for el in elements:
        kind = el.get("type")
        tags = el.get("tags") or {}
        if kind == "node":
            lon, lat = el.get("lon"), el.get("lat")
            if lon is None or lat is None:
                continue
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {**tags, "_osm_id": f"node/{el.get('id')}"},
            })
        elif kind == "way":
            coords = [[g["lon"], g["lat"]] for g in (el.get("geometry") or []) if "lon" in g]
            if len(coords) < 2:
                continue
            is_closed = coords[0] == coords[-1] and len(coords) >= 4
            geom_type = "Polygon" if is_closed and ("building" in tags or tags.get("natural") in
                                                   ("water", "wetland", "wood") or
                                                   "landuse" in tags or tags.get("amenity") or
                                                   tags.get("leisure")) else "LineString"
            geom = {"type": geom_type,
                    "coordinates": [coords] if geom_type == "Polygon" else coords}
            features.append({
                "type": "Feature",
                "geometry": geom,
                "properties": {**tags, "_osm_id": f"way/{el.get('id')}"},
            })
    return {"type": "FeatureCollection", "features": features}


def summarize_category(geo: dict) -> dict:
    feats = geo["features"]
    tag_counts: dict[str, dict[str, int]] = {}
    closest = None
    closest_d = float("inf")
    for f in feats:
        # closest-by-centroid
        coords = f["geometry"]["coordinates"]
        if f["geometry"]["type"] == "Point":
            c_lat, c_lon = coords[1], coords[0]
        elif f["geometry"]["type"] == "Polygon":
            ring = coords[0]
            c_lat = sum(p[1] for p in ring) / len(ring)
            c_lon = sum(p[0] for p in ring) / len(ring)
        else:  # LineString
            c_lat = sum(p[1] for p in coords) / len(coords)
            c_lon = sum(p[0] for p in coords) / len(coords)
        d = haversine_m(LAT, LON, c_lat, c_lon)
        if d < closest_d:
            closest_d = d
            closest = f
        # tag tallies for interesting tag keys
        for key in ("amenity", "tourism", "shop", "leisure", "building", "natural", "waterway",
                    "highway", "landuse", "man_made", "place"):
            v = f["properties"].get(key)
            if v:
                tag_counts.setdefault(key, {})
                tag_counts[key][v] = tag_counts[key].get(v, 0) + 1
    return {
        "count": len(feats),
        "tag_counts": tag_counts,
        "closest_distance_m": None if closest is None else round(closest_d, 1),
        "closest_tags": None if closest is None else closest["properties"],
    }


def main() -> None:
    print(f"OSM Overpass around ({LAT:.5f}, {LON:.5f}) r={RADIUS_M} m")
    all_summaries: dict[str, dict] = {}
    for name, body in CATEGORIES.items():
        print(f"[{name}] querying…", flush=True)
        t0 = time.time()
        try:
            data = query(name, body)
        except Exception as e:
            print(f"  FAILED: {e}")
            all_summaries[name] = {"error": str(e)}
            continue
        geo = to_geojson(data.get("elements", []))
        out_path = OUT / f"{name}.geojson"
        out_path.write_text(json.dumps(geo))
        summary = summarize_category(geo)
        all_summaries[name] = summary
        print(f"  {summary['count']} features, {time.time()-t0:.1f}s "
              f"(closest {summary['closest_distance_m']} m)")

    # Places at 15 km
    print(f"[places] querying r={RADIUS_LARGE_M}m…", flush=True)
    try:
        data = query("places", PLACE_QUERY, radius_m=RADIUS_LARGE_M)
        geo = to_geojson(data.get("elements", []))
        (OUT / "places.geojson").write_text(json.dumps(geo))
        summary = summarize_category(geo)
        all_summaries["places"] = summary
        print(f"  {summary['count']} features (closest {summary['closest_distance_m']} m)")
    except Exception as e:
        print(f"  FAILED: {e}")
        all_summaries["places"] = {"error": str(e)}

    # Aggregate summary JSON + Markdown brief
    (OUT / "osm_v2_summary.json").write_text(json.dumps(all_summaries, indent=2))

    lines = [
        "# OSM brief — La Quebrada Viva (5 km radius around KML centroid)\n",
        "Source: OpenStreetMap via Overpass API, ODbL 1.0  ",
        f"Pulled: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}  ",
        f"Centroid: lon={LON}, lat={LAT}  ",
        f"Radius: {RADIUS_M} m for site features, {RADIUS_LARGE_M} m for places\n",
    ]
    lines.append("## Feature counts by category\n")
    lines.append("| Category | Count | Closest to centroid |")
    lines.append("| --- | --- | --- |")
    for name, s in all_summaries.items():
        if "error" in s:
            lines.append(f"| {name} | FAILED | {s['error']} |")
        else:
            closest_tag = ""
            if s["closest_tags"]:
                for key in ("name", "building", "amenity", "natural", "waterway", "highway",
                            "landuse", "place", "leisure", "tourism", "shop"):
                    if s["closest_tags"].get(key):
                        closest_tag = f"{key}={s['closest_tags'][key]}"
                        break
            lines.append(f"| {name} | {s['count']} | {s['closest_distance_m']} m · {closest_tag} |")

    lines.append("\n## Tag breakdown by category\n")
    for name, s in all_summaries.items():
        if "error" in s:
            continue
        lines.append(f"### {name} ({s['count']} features)\n")
        if not s["tag_counts"]:
            lines.append("_(no tagged sub-types)_\n")
            continue
        for key, vc in s["tag_counts"].items():
            top = sorted(vc.items(), key=lambda kv: -kv[1])[:10]
            cells = ", ".join(f"`{v}`×{n}" for v, n in top)
            lines.append(f"- **{key}**: {cells}")
        lines.append("")

    lines.append("## Interpretation\n")
    counts = {name: s.get("count", 0) for name, s in all_summaries.items()}
    if counts.get("buildings", 0) == 0:
        lines.append("- **Buildings: 0 within 5 km** — confirms remote rural location; no neighbouring "
                     "structures visible to OSM. Microsoft Building Footprints or manual Google Earth "
                     "trace recommended to capture unmapped rural housing.")
    else:
        lines.append(f"- **Buildings: {counts['buildings']} within 5 km** — primary cluster identified; "
                     "see `buildings.geojson` for footprints to overlay on the 62-ha digital twin.")
    if counts.get("water", 0) > 0 or counts.get("waterways", 0) > 0:
        lines.append(f"- **Surface water: {counts.get('water', 0)} polygons / "
                     f"{counts.get('waterways', 0)} waterway segments** within 5 km. "
                     "Cross-reference with JRC GSW + Sentinel-2 NDWI for full surface-water inventory.")
    else:
        lines.append("- **Surface water: 0 features mapped** — OSM coverage gap; rely on JRC GSW + "
                     "Sentinel-2 NDWI + ALOS hillshade drainage interpretation.")
    if counts.get("trees", 0) > 0:
        lines.append(f"- **Vegetation: {counts['trees']} forest/tree features** — see `trees.geojson` "
                     "for tagged orchards/forest patches near the parcel.")
    if counts.get("roads", 0) > 0:
        lines.append(f"- **Roads: {counts['roads']} segments** — access network for site servicing.")
    if counts.get("places", 0) > 0:
        lines.append(f"- **Named places within 15 km: {counts['places']}** — see `places.geojson` "
                     "for hamlets/villages relevant to logistics, labour, and amenity catchment.")

    (OUT / "osm_brief.md").write_text("\n".join(lines) + "\n")
    print(f"\nDone. Brief at {OUT/'osm_brief.md'}")


if __name__ == "__main__":
    main()
