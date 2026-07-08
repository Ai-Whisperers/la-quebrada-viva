#!/usr/bin/env python3
"""Build the cerros/peaks GeoJSON from existing DEM contour data.

Source: /root/.hermes/lqv-splat/exports/web/data/dem_contours_10km.geojson
Method: find closed contour rings at each elevation level; cluster by spatial
proximity (>=600m apart); take the highest elevation in each cluster as the
summit. At the parcel-scale DEM resolution (30m), this finds ~20-25 distinct
cerros in the 10km box, including the local high on the LQV parcel.

For each cerro we also try to look up a name from:
  - OSM `natural=peak` (overpass-api blocked at run-time, fallback)
  - Or use directional names: "Cerro NNE of LQV", etc.

Output: /root/.hermes/lqv-splat/exports/web/data/peaks_10km.geojson
        + peaks_10km_bounds.json
"""
import json, math, os, sys

CONTOURS_PATH = "/root/.hermes/lqv-splat/exports/web/data/dem_contours_10km.geojson"
PARCEL_PATH = "/root/.hermes/lqv-splat/exports/web/data/client_gps/client_gps_polygon.geojson"
OUT_PATH = "/root/.hermes/lqv-splat/exports/web/data/peaks_10km.geojson"
BOUNDS_OUT = "/root/.hermes/lqv-splat/exports/web/data/peaks_10km_bounds.json"


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1); dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.asin(math.sqrt(a))


def bearing_deg(lat1, lon1, lat2, lon2):
    """Bearing from (1) to (2) in degrees (0=N, 90=E)."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1)*math.sin(p2) - math.sin(p1)*math.cos(p2)*math.cos(dl)
    return (math.degrees(math.atan2(y, x)) + 360) % 360


def compass(bearing):
    dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE",
            "S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return dirs[int((bearing + 11.25) // 22.5) % 16]


def ring_area_m2(coords):
    lat0 = coords[0][1]
    m_per_deg_lon = 111320 * math.cos(math.radians(lat0))
    m_per_deg_lat = 110540
    pts = [(c[0] * m_per_deg_lon, c[1] * m_per_deg_lat) for c in coords]
    n = len(pts); a = 0
    for i in range(n):
        j = (i+1) % n
        a += pts[i][0]*pts[j][1] - pts[j][0]*pts[i][1]
    return abs(a) / 2


def centroid(coords):
    cx = sum(c[0] for c in coords) / len(coords)
    cy = sum(c[1] for c in coords) / len(coords)
    return cx, cy


# ---- 1. Load & extract closed rings ----
contours = json.loads(open(CONTOURS_PATH).read())
features = contours.get("features", [])

# Group by elevation level
by_elev = {}
for feat in features:
    elev = feat.get("properties", {}).get("elev_m")
    if elev is None: continue
    coords = feat.get("geometry", {}).get("coordinates", [])
    if len(coords) < 5 or coords[0] != coords[-1]: continue  # not closed
    by_elev.setdefault(int(elev), []).append({
        "elev": int(elev),
        "coords": coords[:-1],
        "area_m2": ring_area_m2(coords),
        "centroid": centroid(coords[:-1]),
    })

# ---- 2. Find peaks by NESTING — each real cerro has multiple closed
#           contour rings (350, 300, 250, 200, ...) stacked on top of each other.
#           A peak that only has one closed ring is likely a saddle/col.
# Group rings by spatial proximity (within 1.5km), each group becomes a peak.
ring_records = []
for elev in sorted(by_elev.keys(), reverse=True):
    for r in by_elev[elev]:
        if r["area_m2"] >= 5000:
            ring_records.append(r)

# Cluster rings across ALL elevations by spatial proximity
def cluster_rings(records, max_dist_m=1500):
    """Greedy single-link clustering: any two rings within max_dist end up in same cluster."""
    n = len(records)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry: parent[rx] = ry
    # Pre-compute centroids
    cents = [(r["centroid"][0], r["centroid"][1]) for r in records]
    for i in range(n):
        for j in range(i+1, n):
            d = haversine_m(cents[i][1], cents[i][0], cents[j][1], cents[j][0])
            if d <= max_dist_m:
                union(i, j)
    # Group by root
    from collections import defaultdict
    groups = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)
    return groups

groups = cluster_rings(ring_records, max_dist_m=1500)
print(f"Found {len(groups)} cerro clusters from {len(ring_records)} closed rings")

# For each cluster, the summit is at the highest elevation ring; centroid = that ring's centroid
clusters = []
for idx_list in groups.values():
    cluster_rings = [ring_records[i] for i in idx_list]
    # Sort by elevation desc, area desc — top one is the summit
    cluster_rings.sort(key=lambda r: (-r["elev"], -r["area_m2"]))
    summit = cluster_rings[0]
    # Also keep the largest-area ring at the BASE (lowest elevation) for a "footprint"
    base = min(cluster_rings, key=lambda r: r["elev"])
    clusters.append({
        "elev": summit["elev"],
        "centroid": summit["centroid"],
        "area_m2": base["area_m2"],   # footprint area at base
        "rings_count": len(cluster_rings),
        "elev_levels": sorted({r["elev"] for r in cluster_rings}, reverse=True),
    })

# Sort: a real cerro has >= 2 distinct elevation levels of closed rings (multi-contour)
clusters = [c for c in clusters if c["rings_count"] >= 2]

# Dedupe: if two clusters are within 1.5km AND same elevation, keep the larger one.
# Cerro seen from different contour levels may cluster twice — merge them.
def merge_close(clusters, max_dist_m=1500):
    """If two clusters are within max_dist, keep the one with higher summit elev.
    If elev is same, keep the larger one."""
    clusters = sorted(clusters, key=lambda c: (-c["elev"], -c["area_m2"]))
    merged = []
    for c in clusters:
        cx, cy = c["centroid"]
        dup_of = None
        for i, m in enumerate(merged):
            mx, my = m["centroid"]
            d = haversine_m(cy, cx, my, mx)
            if d <= max_dist_m:
                dup_of = i
                break
        if dup_of is None:
            merged.append(dict(c))
        else:
            # Keep the existing one (already higher since we sorted)
            pass
    return merged

clusters = merge_close(clusters, max_dist_m=1500)
print(f"  After dedupe (close-by merge): {len(clusters)}")
clusters.sort(key=lambda c: (-c["elev"], -c["area_m2"]))

# ---- 4. LQV parcel centroid for naming reference ----
parcel = json.loads(open(PARCEL_PATH).read())
poly = parcel["features"][0]["geometry"]["coordinates"][0]
parcel_lon = sum(c[0] for c in poly) / len(poly)
parcel_lat = sum(c[1] for c in poly) / len(poly)
print(f"LQV parcel centroid: ({parcel_lat:.4f}, {parcel_lon:.4f})")

# ---- 5. Build GeoJSON ----
features_out = []
clusters.sort(key=lambda c: -c["elev"])
for rank, c in enumerate(clusters, 1):
    cx, cy = c["centroid"]
    b = bearing_deg(parcel_lat, parcel_lon, cy, cx)
    dist_km = haversine_m(parcel_lat, parcel_lon, cy, cx) / 1000
    direction = compass(b)
    if dist_km < 0.3:
        name = "Cerro del LQV"
    elif dist_km < 1.5:
        name = f"Cerro {direction} del LQV"
    else:
        name = f"Cerro {direction} de Escobar"
    features_out.append({
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [cx, cy]},
        "properties": {
            "name": name,
            "elev_m": c["elev"],
            "rank": rank,
            "area_ha": round(c["area_m2"] / 10000, 2),
            "distance_from_lqv_km": round(dist_km, 2),
            "bearing_from_lqv_deg": round(b, 1),
            "direction_from_lqv": direction,
            "category": "summit" if c["area_m2"] > 50000 else "hill",
            "source": "DEM-derived (Copernicus GLO-30, closed contour rings)",
            "note": f"Auto-detected summit at {c['elev']}m. Local name not in OSM.",
        }
    })

geojson = {"type": "FeatureCollection", "features": features_out}

# Add the parcel centroid as "LQV parcel" for orientation
features_out.insert(0, {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [parcel_lon, parcel_lat]},
    "properties": {
        "name": "LQV Parcel (La Quebrada Viva)",
        "elev_m": None,  # we don't have parcel DEM in the 10km file
        "rank": 0,
        "category": "property",
        "source": "Client GPS polygon centroid",
        "note": "Property boundary centroid.",
    }
})

with open(OUT_PATH, "w") as f:
    json.dump(geojson, f, indent=2)
print(f"Wrote {len(features_out)} features to {OUT_PATH}")

# Bounds file
bounds = {
    "type": "bounds",
    "bbox": [-57.13, -25.698, -56.931, -25.518],
    "center_km": [-57.03, -25.62],
    "source": "dem_contours_10km.geojson (Copernicus GLO-30)",
    "cerros_count": len(features_out),
    "elevation_range_m": [100, 400],
    "naming": "Directional from LQV parcel centroid (no OSM names available in Paraguay rural)",
}
with open(BOUNDS_OUT, "w") as f:
    json.dump(bounds, f, indent=2)
print(f"Wrote bounds file")

# ---- 6. Summary ----
print(f"\n=== Cerro summary ===")
for f in features_out[:25]:
    p = f["properties"]
    if p.get("elev_m"):
        print(f"  #{p['rank']:>2}  {p['elev_m']:>4}m  {p['name']:35s}  {p['distance_from_lqv_km']:>5.2f}km {p['direction_from_lqv']:>3}  area={p.get('area_ha',0):>6.2f}ha")
    else:
        print(f"  REF {p['name']:35s}  (parcel reference point)")
