"""Build proper GeoJSON layers from Wesley's on-site GPS walk + Escobar property polygons.

Three perimeter polygons (each is real, none is wrong — they're just different views):

  1. **client_gps_polygon** — Wes's 17-point GPS walk, 2026-06-22 + 2026-06-28
     Captured on the ground by walking the perimeter with Guru Maps on iOS.
     71.37 ha, 4.27 km perimeter. **THE one to trust for the buyer's view.**
  2. **escobar_property_polygon** — KML polygon shared 2026-06-28 post-escritura
     8 vertices, 30.9 ha — looks like an INTERIOR buildable subset. Kept as
     historical/legacy reference, not the main perimeter.
  3. **special_features** — gate, waterfall (quebrada), high point. Three
     named features Wes captured separately.

Plus the older `aoi_62ha_extended` polygon (62 ha cluster outline) for context.

This script is IDEMPOTENT — re-run any time the GPS data updates.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GPS_JSON = ROOT / "docs/site_data/property_gps_walk_2026-06-28/guru_maps_geojson.json"
ESC_OLD = ROOT / "docs/site_data/property_polygon/escobar_property_polygon.geojson"
AOI_EXT = ROOT / "docs/site_data/property_polygon/aoi_62ha_extended.geojson"
OUT_DIR = ROOT / "splats/exports/web/data" / "client_gps"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Wesley's GPS-walk polygon — 17 border points (cat=118) in the order Wes
# actually walked the perimeter. Walking order matters for the polygon ring
# (it must be a non-self-intersecting closed loop).
#
# Derived by ordering the 17 cat=118 points along a greedy nearest-neighbour
# TSP path from the centroid. The README.md in this folder already gave us
# the walking-order coordinates; we replicate that order here so the polygon
# reconstructs Wes's actual walk path.
#
# (lon, lat) — these are the per-vertex coords from id=0..19 in the JSON.
WALKING_ORDER_IDS = [
    19,  # P1  -57.036303 -25.608296
    17,  # P2  -57.030097 -25.615699
    12,  # P3  -57.028713 -25.611854
    14,  # P4  -57.028127 -25.612010
     7,  # P5  -57.027691 -25.612010
     1,  # P6  -57.026126 -25.609991
     0,  # P7  -57.026181 -25.609915
     2,  # P8  -57.025573 -25.608754
    15,  # P9  -57.027457 -25.608112
     6,  # P10 -57.027427 -25.606662
    13,  # P11 -57.029635 -25.607399
     4,  # P12 -57.029413 -25.604455
    16,  # P13 -57.032779 -25.602790
     5,  # P14 -57.033511 -25.603347
    11,  # P15 -57.034487 -25.605104
     8,  # P16 -57.032901 -25.606668
     3,  # P17 -57.034139 -25.606805
]


# ---- Load + classify ----
all_pts = json.load(open(GPS_JSON))
border_pts = [f for f in all_pts if f["properties"].get("cat") == 118]
specials = [f for f in all_pts if f["properties"].get("cat") != 118]
print(f"Border points (cat=118): {len(border_pts)}")
print(f"Special features: {[f['properties'].get('cat') for f in specials]}")

# Build the perimeter polygon
by_id = {f["properties"]["id"]: f for f in all_pts}
ordered = [by_id[i] for i in WALKING_ORDER_IDS]
ring = [[p["geometry"]["coordinates"][0], p["geometry"]["coordinates"][1]] for p in ordered]
# Close the ring
closed_ring = ring + [ring[0]]

# Compute area in m² (equirectangular at centroid latitude)
def polygon_stats(coords):
    n = len(coords)
    cx_lat = sum(c[1] for c in coords) / n
    kx = 111320 * math.cos(math.radians(cx_lat))
    ky = 110540
    s_area = 0
    perim = 0
    for i in range(n):
        x1, y1 = coords[i][0] * kx, coords[i][1] * ky
        x2, y2 = coords[(i+1) % n][0] * kx, coords[(i+1) % n][1] * ky
        s_area += x1 * y2 - x2 * y1
        perim += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    area_m2 = abs(s_area) / 2
    return {
        "area_m2": round(area_m2, 0),
        "area_ha": round(area_m2 / 10000, 2),
        "perimeter_m": round(perim, 0),
        "perimeter_km": round(perim / 1000, 3),
        "centroid_lon": round(sum(c[0] for c in coords) / n, 6),
        "centroid_lat": round(sum(c[1] for c in coords) / n, 6),
    }


def centroid_of(coords):
    """Leaflet-style centroid (simple bbox average — good enough at this scale)."""
    n = len(coords)
    return (
        sum(c[1] for c in coords) / n,
        sum(c[0] for c in coords) / n,
    )


stats = polygon_stats(closed_ring)
print(f"\nClient GPS polygon:")
print(f"  vertices      = {len(closed_ring)-1}")
print(f"  area          = {stats['area_ha']:>7.2f} ha  ({stats['area_m2']:>10,.0f} m²)")
print(f"  perimeter     = {stats['perimeter_km']:>7.3f} km  ({stats['perimeter_m']:>8,.0f} m)")
print(f"  centroid      = {stats['centroid_lon']:.6f}, {stats['centroid_lat']:.6f}")

xs = [c[0] for c in closed_ring]; ys = [c[1] for c in closed_ring]
print(f"  bbox          = lon {min(xs):.5f}..{max(xs):.5f} ({max(xs)-min(xs):.4f}°),"
      f"  lat {min(ys):.5f}..{max(ys):.5f} ({max(ys)-min(ys):.4f}°)")

lat_avg = sum(ys) / len(ys)
width_m  = (max(xs)-min(xs)) * 111 * math.cos(math.radians(lat_avg)) * 1000
height_m = (max(ys)-min(ys)) * 110540
print(f"  width E-W     = {width_m:>7.0f} m")
print(f"  height N-S    = {height_m:>7.0f} m")
print()


# ---- 1. The main client perimeter polygon ----
perimeter_fc = {
    "type": "FeatureCollection",
    "name": "client_gps_polygon",
    "metadata": {
        "source": "Wesley van de Camp GPS walk via Guru Maps iOS",
        "received_utc": "2026-06-28",
        "walk_dates": ["2026-06-22", "2026-06-28"],
        "source_file": "docs/site_data/property_gps_walk_2026-06-28/guru_maps_geojson.json",
        "method": "17 handheld GPS points captured while walking the property perimeter",
        "accuracy_note": "Handheld iPhone GPS accuracy ±3-5 m per point. Survey-grade boundary NOT done — this is a real-world GPS walk, not a cadastre.",
        **stats,
    },
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "La Quebrada Viva — client GPS perimeter",
                "source": "client GPS walk",
                "category": "perimeter",
                "vertex_count": len(closed_ring) - 1,
                "captured_by": "Wesley van de Camp",
                "captured_with": "Guru Maps iOS app",
                "captured_dates": "2026-06-22 + 2026-06-28",
                **stats,
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [closed_ring],
            },
        }
    ],
}
with open(OUT_DIR / "client_gps_polygon.geojson", "w") as f:
    json.dump(perimeter_fc, f, indent=2)
print(f"✓ {OUT_DIR / 'client_gps_polygon.geojson'}")


# ---- 2. The 17 individual border corner points ----
corners_fc = {
    "type": "FeatureCollection",
    "name": "client_gps_corners",
    "metadata": {
        "source": "Wesley van de Camp GPS walk via Guru Maps",
        "category": "border_corner",
        "count": len(ordered),
        "captured_dates": "2026-06-22 + 2026-06-28",
        "note": "Each point corresponds to a corner Wes marked while walking the perimeter. Walking-order preserved.",
    },
    "features": [],
}
for i, (pt, vertex_id) in enumerate(zip(ordered, WALKING_ORDER_IDS)):
    c = pt["geometry"]["coordinates"]
    corners_fc["features"].append({
        "type": "Feature",
        "properties": {
            "name": f"Corner P{i+1}",
            "category": "border_corner",
            "vertex_index": i + 1,
            "original_id": vertex_id,
            "lon": c[0],
            "lat": c[1],
        },
        "geometry": {"type": "Point", "coordinates": c},
    })
with open(OUT_DIR / "client_gps_corners.geojson", "w") as f:
    json.dump(corners_fc, f, indent=2)
print(f"✓ {OUT_DIR / 'client_gps_corners.geojson'}  ({len(ordered)} corners)")


# ---- 3. Special features (gate, waterfall, high point) ----
feature_labels = {
    26: "Waterfall (quebrada)",
    28: "Property gate (entrance)",
    72: "High point (274 m, NE ridge)",
}
feature_styles = {
    26: {"icon": "💧", "color": "#dc2626", "symbol": "W"},
    28: {"icon": "🚪", "color": "#1d4ed8", "symbol": "G"},
    72: {"icon": "⛰️", "color": "#15803d", "symbol": "HP"},
}
features_fc = {
    "type": "FeatureCollection",
    "name": "client_gps_features",
    "metadata": {
        "source": "Wesley van de Camp GPS walk via Guru Maps",
        "category": "named_feature",
        "count": len(specials),
        "note": "Special features captured in addition to the perimeter walk: gate (entrance), waterfall (the quebrada), high point (highest place on the property).",
    },
    "features": [],
}
for f in specials:
    cat = f["properties"].get("cat")
    c = f["geometry"]["coordinates"]
    label = feature_labels.get(cat, f"Feature cat={cat}")
    style = feature_styles.get(cat, {"icon": "📍", "color": "#a855f7", "symbol": "?"})
    desc = f["properties"].get("desc", "")
    elev_match = []
    if "GPS-hoogte" in desc:
        try:
            elev_match = [s for s in desc.split() if s.replace("m", "").replace(".", "").isdigit()]
        except Exception:
            pass
    altitude_m = None
    for t in desc.split():
        if t.endswith("m") and t[:-1].replace(".", "").replace("-", "").isdigit():
            try:
                altitude_m = float(t[:-1])
            except Exception:
                pass
    features_fc["features"].append({
        "type": "Feature",
        "properties": {
            "name": label,
            "category": "named_feature",
            "feature_kind": {26: "waterfall", 28: "gate", 72: "high_point"}.get(cat, f"cat{cat}"),
            "color": style["color"],
            "icon": style["icon"],
            "symbol": style["symbol"],
            "altitude_m": altitude_m,
            "lon": c[0],
            "lat": c[1],
        },
        "geometry": {"type": "Point", "coordinates": c},
    })

# Compare positions vs the polygon — which specials are inside?
def point_in_poly(pt, poly):
    """Ray casting. poly = [[lon,lat], ...] with first=last (closed ring)."""
    if poly[0] == poly[-1]:
        poly = poly[:-1]
    n = len(poly)
    x, y = pt
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj-xi)*(y-yi)/(yj-yi+1e-12) + xi):
            inside = not inside
        j = i
    return inside

for f in features_fc["features"]:
    pt = f["geometry"]["coordinates"]
    f["properties"]["inside_polygon"] = point_in_poly(pt, ring)
with open(OUT_DIR / "client_gps_features.geojson", "w") as f:
    json.dump(features_fc, f, indent=2)
print(f"✓ {OUT_DIR / 'client_gps_features.geojson'}  ({len(specials)} features)")
for f in features_fc["features"]:
    pt = f["geometry"]["coordinates"]
    inside = "INSIDE" if f["properties"]["inside_polygon"] else "OUTSIDE"
    print(f"    {f['properties']['symbol']:3} {f['properties']['name']:35s}  ({pt[0]:.5f}, {pt[1]:.5f})  {inside}")
print()

# ---- 4. Copy the older Escobar polygon + AOI extended as legacy layers ----
esc = json.load(open(ESC_OLD))
esc_poly = esc["features"][0]
old_centroid = esc_poly["properties"].get("centroid_lon"), esc_poly["properties"].get("centroid_lat")
esc_fc = {
    "type": "FeatureCollection",
    "name": "escobar_polygon_legacy",
    "metadata": {
        "source": "Wesley van de Camp KML via Google Earth Pro",
        "received_utc": "2026-06-28",
        "note": "8-vertex polygon shared with the post-escritura site-knowledge package. "
                 "30.9 ha projected — appears to be an INTERIOR buildable subset of the full "
                 "GPS-walk polygon, NOT the full perimeter. Kept for historical reference.",
        "replaced_by": "client_gps_polygon.geojson (the on-the-ground walking perimeter)",
    },
    "features": esc["features"],
}
with open(OUT_DIR / "escobar_polygon_legacy.geojson", "w") as f:
    json.dump(esc_fc, f, indent=2)
print(f"✓ {OUT_DIR / 'escobar_polygon_legacy.geojson'}  (legacy KML subset, kept for reference)")
print()

if AOI_EXT.exists():
    aoi = json.load(open(AOI_EXT))
    aoi_fc = {
        "type": "FeatureCollection",
        "name": "aoi_62_extended_legacy",
        "metadata": {
            "source": "Wes's KML buffer",
            "note": "62 ha cluster outline — buffer around the KML polygon for visualisation. Replaced conceptually by the GPS polygon.",
        },
        "features": aoi["features"],
    }
    with open(OUT_DIR / "aoi_62_extended_legacy.geojson", "w") as f:
        json.dump(aoi_fc, f, indent=2)
    print(f"✓ {OUT_DIR / 'aoi_62_extended_legacy.geojson'}  (legacy 62 ha AOI)")

print(f"\nWritten {4 if AOI_EXT.exists() else 3} GeoJSON files to {OUT_DIR}")
print("Next: deploy via wrangler pages deploy.")
