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

import csv
import io
import json
import math
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GPS_JSON = ROOT / "docs/site_data/property_gps_walk_2026-06-28/guru_maps_geojson.json"
ESC_OLD = ROOT / "docs/site_data/property_polygon/escobar_property_polygon.geojson"
AOI_EXT = ROOT / "docs/site_data/property_polygon/aoi_62ha_extended.geojson"
GPX_FILE = ROOT / "docs/site_data/property_gps_walk_2026-06-28/guru_maps.gpx"

OUT_DIR = ROOT / "splats/exports/web/data" / "client_gps"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Guru Maps shared URL (live source of truth — re-pull if needed)
GURUMAPS_BASE = "https://shared.gurumaps.app/5f349095-4c7b-49cd-8d8d-0e0acb7e3f8e"


# ---- Optional live re-pull ----
def live_pull() -> dict[str, str]:
    """Re-pull GeoJSON/GPX/KML from the Guru Maps share URL and save into the
    docs/site_data/property_gps_walk_2026-06-28/ folder. Idempotent.

    Returns dict of fetched paths (relative to ROOT).
    """
    fetched = {}
    for ext in ("geojson", "gpx", "kml"):
        url = f"{GURUMAPS_BASE}.{ext}"
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                body = r.read().decode("utf-8")
        except Exception as e:
            print(f"  [live-pull] {ext}: skip ({e})")
            continue
        out = ROOT / "docs/site_data/property_gps_walk_2026-06-28" / f"guru_maps.{ext}"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(body, encoding="utf-8")
        fetched[ext] = str(out.relative_to(ROOT))
        print(f"  [live-pull] {ext}: {len(body):,} bytes → {out}")
    return fetched


# ---- GPX timestamp extraction ----
def parse_gpx_timestamps(gpx_path: Path) -> dict[int, str]:
    """Return {feature_id: ISO8601 timestamp} for waypoints in the GPX.

    Uses the Guru Maps GPX schema extension's <type>118/26/28/72</type> as
    the waypoint ID. Falls back to ordinal position if <type> is missing.
    """
    if not gpx_path.exists():
        return {}
    tree = ET.parse(gpx_path)
    root = tree.getroot()
    ns_g = "{http://www.topografix.com/GPX/1/1}"
    wpts = root.findall(f"{ns_g}wpt")
    times: dict[int, str] = {}
    for i, wpt in enumerate(wpts):
        time_el = wpt.find(f"{ns_g}time")
        type_el = wpt.find(f"{ns_g}type")
        if time_el is not None and type_el is not None:
            try:
                times[int(type_el.text)] = time_el.text
            except (ValueError, TypeError):
                pass
    return times


def parse_kml_timestamps(kml_path: Path) -> dict[int, str]:
    """Fallback: pull <gx:TimeStamp> from each Placemark in the KML, mapped
    by ordinal position → GeoJSON feature id.

    Empirically verified (2026-07-05): Guru Maps KML placemarks appear in
    the same order as the GeoJSON `id` field. So ordinal i in the KML =
    feature.id i in the GeoJSON.
    """
    if not kml_path.exists():
        return {}
    tree = ET.parse(kml_path)
    root = tree.getroot()
    ns_kml = "{http://www.opengis.net/kml/2.2}"
    ns_gx  = "{http://www.google.com/kml/ext/2.2}"
    times: dict[int, str] = {}
    pms = list(root.iter(f"{ns_kml}Placemark"))
    for fid, pm in enumerate(pms):
        ts = pm.find(f"{ns_gx}TimeStamp")
        if ts is not None:
            # Format A: <gx:TimeStamp><when>2026-...Z</when></gx:TimeStamp>
            when = ts.find(f"{ns_gx}when")
            if when is not None and when.text:
                times[fid] = when.text
                continue
            # Format B (Guru Maps): <gx:TimeStamp>2026-...Z</gx:TimeStamp>
            if ts.text and ts.text.strip():
                times[fid] = ts.text.strip()
    return times


# Wesley's GPS-walk polygon — 17 border points (cat=118) in the order Wes
# actually walked the perimeter. Walking order matters for the polygon ring
# (it must be a non-self-intersecting closed loop).
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
SPECIAL_IDS = {
    26: "waterfall",
    28: "gate",
    72: "high_point",
}


def haversine_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    R = 6371.0
    p1, p2 = math.radians(a[1]), math.radians(b[1])
    dp = math.radians(b[1] - a[1])
    dl = math.radians(b[0] - a[0])
    x = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))


def polygon_stats(coords: list[list[float]]) -> dict:
    """Shoelace area + perimeter on a closed ring (first == last assumed)."""
    n = len(coords)
    cx_lat = sum(c[1] for c in coords) / n
    kx = 111_320 * math.cos(math.radians(cx_lat))
    ky = 110_540
    s_area = 0.0
    perim = 0.0
    for i in range(n):
        x1, y1 = coords[i][0] * kx, coords[i][1] * ky
        x2, y2 = coords[(i + 1) % n][0] * kx, coords[(i + 1) % n][1] * ky
        s_area += x1 * y2 - x2 * y1
        perim += math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    area_m2 = abs(s_area) / 2
    return {
        "area_m2": round(area_m2, 0),
        "area_ha": round(area_m2 / 10_000, 2),
        "perimeter_m": round(perim, 0),
        "perimeter_km": round(perim / 1000, 3),
        "centroid_lon": round(sum(c[0] for c in coords) / n, 6),
        "centroid_lat": round(sum(c[1] for c in coords) / n, 6),
    }


def point_in_poly(pt: list[float], ring: list[list[float]]) -> bool:
    """Ray casting. ring is a closed list of [lon, lat] (first == last)."""
    poly = ring[:-1] if ring[0] == ring[-1] else ring
    n = len(poly)
    x, y = pt
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            inside = not inside
        j = i
    return inside


# ---- 0. Live re-pull (optional) ----
print("=== Live re-pull from Guru Maps shared URL ===")
fetched = live_pull()
if fetched:
    print(f"  Refreshed: {list(fetched.keys())}")
print()

# ---- Load source data ----
all_pts = json.load(open(GPS_JSON))
border_pts = [f for f in all_pts if f["properties"].get("cat") == 118]
specials   = [f for f in all_pts if f["properties"].get("cat") != 118]
print(f"Border points (cat=118):   {len(border_pts)}")
print(f"Special features (3 types): {sorted(set(f['properties'].get('cat') for f in specials))}")

# Augment with timestamps from the live GPX (preferred) or KML (fallback)
KML_FILE = GPX_FILE.parent / "guru_maps.kml"
timestamps_gpx = parse_gpx_timestamps(GPX_FILE)
timestamps_kml = parse_kml_timestamps(KML_FILE)
if timestamps_gpx:
    timestamps = timestamps_gpx
    src_used = f"GPX ({GPX_FILE.name})"
elif timestamps_kml:
    timestamps = timestamps_kml
    src_used = f"KML ({KML_FILE.name})"
else:
    timestamps = {}
    src_used = "none"
print(f"Timestamps recovered: {len(timestamps)} (from {src_used})")

# Order border points by ID, inject walking-order index, attach timestamps
by_id = {f["properties"]["id"]: f for f in all_pts}
ordered_border = [by_id[i] for i in WALKING_ORDER_IDS]
ring = [[p["geometry"]["coordinates"][0], p["geometry"]["coordinates"][1]] for p in ordered_border]
closed_ring = ring + [ring[0]]

stats = polygon_stats(closed_ring)
print(f"\nClient GPS polygon:")
print(f"  vertices      = {len(closed_ring)-1}")
print(f"  area          = {stats['area_ha']:>7.2f} ha  ({stats['area_m2']:>10,.0f} m²)")
print(f"  perimeter     = {stats['perimeter_km']:>7.3f} km")
print(f"  centroid      = {stats['centroid_lon']:.6f}, {stats['centroid_lat']:.6f}")
print()


# ============================================================
# 1. The main client perimeter polygon
# ============================================================
perimeter_fc = {
    "type": "FeatureCollection",
    "name": "client_gps_polygon",
    "metadata": {
        "source": "Wesley van de Camp GPS walk via Guru Maps iOS",
        "source_url": GURUMAPS_BASE + ".html",
        "received_utc": "2026-06-28",
        "walk_dates": ["2026-06-22", "2026-06-28"],
        "method": "17 handheld GPS points captured while walking the property perimeter",
        "accuracy_note": "Handheld iPhone GPS accuracy ±3-5 m per point. Survey-grade boundary NOT done.",
        **stats,
    },
    "features": [{
        "type": "Feature",
        "properties": {
            "name": "La Quebrada Viva — client GPS perimeter",
            "source": "client GPS walk",
            "category": "perimeter",
            "vertex_count": len(closed_ring) - 1,
            "captured_by": "Wesley van de Camp",
            "captured_with": "Guru Maps iOS app",
            "captured_dates": "2026-06-22 + 2026-06-28",
            "source_url": GURUMAPS_BASE + ".html",
            **stats,
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [closed_ring],
        },
    }],
}
with open(OUT_DIR / "client_gps_polygon.geojson", "w") as f:
    json.dump(perimeter_fc, f, indent=2)
print(f"✓ {OUT_DIR / 'client_gps_polygon.geojson'}")


# ============================================================
# 2. The 17 individual border corner points — now WITH timestamps + walk order
# ============================================================
corners_features = []
for i, (pt, vertex_id) in enumerate(zip(ordered_border, WALKING_ORDER_IDS)):
    c = pt["geometry"]["coordinates"]
    props = {
        "name": f"Corner P{i+1}",
        "category": "border_corner",
        "vertex_index": i + 1,
        "original_id": vertex_id,
        "lon": round(c[0], 7),
        "lat": round(c[1], 7),
        "captured_at": timestamps.get(vertex_id),
        "walk_session": "2026-06-28" if (timestamps.get(vertex_id) or "").startswith("2026-06-28") else
                       ("2026-06-22" if (timestamps.get(vertex_id) or "").startswith("2026-06-22") else None),
    }
    corners_features.append({
        "type": "Feature",
        "properties": props,
        "geometry": {"type": "Point", "coordinates": c},
    })

corners_fc = {
    "type": "FeatureCollection",
    "name": "client_gps_corners",
    "metadata": {
        "source": "Wesley van de Camp GPS walk via Guru Maps",
        "source_url": GURUMAPS_BASE + ".html",
        "category": "border_corner",
        "count": len(ordered_border),
        "captured_dates": "2026-06-22 + 2026-06-28",
        "walk_session_breakdown": {
            "2026-06-22": sum(1 for f in corners_features if f["properties"].get("walk_session") == "2026-06-22"),
            "2026-06-28": sum(1 for f in corners_features if f["properties"].get("walk_session") == "2026-06-28"),
        },
    },
    "features": corners_features,
}
with open(OUT_DIR / "client_gps_corners.geojson", "w") as f:
    json.dump(corners_fc, f, indent=2)
print(f"✓ {OUT_DIR / 'client_gps_corners.geojson'}  ({len(ordered_border)} corners, {len(timestamps)} with timestamps)")


# ============================================================
# 3. SPECIAL FEATURES — gate, waterfall, summit, with altitude where known
# ============================================================
feature_labels = {
    26: "Waterfall (quebrada)",
    28: "Property gate (entrance)",
    72: "High point (NE ridge)",
}
feature_styles = {
    26: {"icon": "💧", "color": "#0284c7", "symbol": "W",  "fill": "#bae6fd"},
    28: {"icon": "🚪", "color": "#1d4ed8", "symbol": "G",  "fill": "#bfdbfe"},
    72: {"icon": "⛰️", "color": "#15803d", "symbol": "HP", "fill": "#bbf7d0"},
}
features_features = []
for f in specials:
    cat = f["properties"].get("cat")
    c = f["geometry"]["coordinates"]
    label = feature_labels.get(cat, f"Feature cat={cat}")
    style = feature_styles.get(cat, {"icon": "📍", "color": "#a855f7", "symbol": "?", "fill": "#f3e8ff"})
    desc = f["properties"].get("desc", "")
    altitude_m = None
    for t in desc.split():
        if t.endswith("m") and t[:-1].replace(".", "").replace("-", "").isdigit():
            try:
                altitude_m = float(t[:-1])
            except Exception:
                pass
    pts_fid = f["properties"].get("id", 0)
    props = {
        "name": label,
        "category": "named_feature",
        "feature_kind": SPECIAL_IDS.get(cat, f"cat{cat}"),
        "color": style["color"],
        "fill_color": style["fill"],
        "icon": style["icon"],
        "symbol": style["symbol"],
        # Map the Guru Maps bookmark style id (the real icon class).
        # 118 = border (orange), 26 = waterfall (red), 28 = gate (blue),
        # 72 = high point (green). The viewer reads `icon_cat` to pick
        # the right BookmarkStyle_*.png file from
        # ./data/icons/gurumaps/.
        "icon_cat": cat,
        "altitude_m": altitude_m,
        "lon": round(c[0], 7),
        "lat": round(c[1], 7),
        "captured_at": timestamps.get(pts_fid),
    }
    features_features.append({
        "type": "Feature",
        "properties": props,
        "geometry": {"type": "Point", "coordinates": c},
    })

# Containment check
for f in features_features:
    pt = f["geometry"]["coordinates"]
    f["properties"]["inside_polygon"] = point_in_poly(pt, ring)

with open(OUT_DIR / "client_gps_features.geojson", "w") as f:
    json.dump({"type": "FeatureCollection", "name": "client_gps_features", "features": features_features}, f, indent=2)
print(f"✓ {OUT_DIR / 'client_gps_features.geojson'}  ({len(specials)} features)")
for f in features_features:
    pt = f["geometry"]["coordinates"]
    inside = "INSIDE" if f["properties"]["inside_polygon"] else "OUTSIDE"
    elev = f"  {f['properties']['altitude_m']} m" if f["properties"]["altitude_m"] else ""
    print(f"    {f['properties']['symbol']:3} {f['properties']['name']:30s}  ({pt[0]:.5f}, {pt[1]:.5f}){elev}  {inside}")
print()


# ============================================================
# 4. WALKING-PATH polyline — the actual trail Wes followed (time-ordered)
# ============================================================
# Build a chronological polyline of all 20 waypoints (border + features) in
# the order Wes captured them. Useful to see which side he walked first.
all_with_time = []
for pt in all_pts:
    fid = pt["properties"].get("id", 0)
    ts = timestamps.get(fid)
    if ts:
        all_with_time.append((ts, pt))
all_with_time.sort(key=lambda x: x[0])

path_coords = []
path_timestamps = []
path_categories = []
for ts, p in all_with_time:
    lon, lat = p["geometry"]["coordinates"]
    path_coords.append([lon, lat])
    path_timestamps.append(ts)
    path_categories.append(p["properties"].get("cat", "?"))

# Walk duration analysis
n_walks_22 = n_walks_28 = 0
total_session = 0.0
duration_min: list[float] = []
from datetime import datetime
if path_timestamps:
    duration_min = []
    for i in range(1, len(path_timestamps)):
        t0 = datetime.fromisoformat(path_timestamps[i-1].replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(path_timestamps[i].replace("Z", "+00:00"))
        duration_min.append((t1 - t0).total_seconds() / 60)
    total_session = (datetime.fromisoformat(path_timestamps[-1].replace("Z","+00:00"))
                     - datetime.fromisoformat(path_timestamps[0].replace("Z","+00:00"))).total_seconds() / 60
    n_walks_22 = sum(1 for ts in path_timestamps if ts.startswith("2026-06-22"))
    n_walks_28 = sum(1 for ts in path_timestamps if ts.startswith("2026-06-28"))

walking_path_fc = {
    "type": "FeatureCollection",
    "name": "client_gps_walking_path",
    "metadata": {
        "source": "Wesley van de Camp GPS walk via Guru Maps GPX",
        "source_url": GURUMAPS_BASE + ".gpx",
        "category": "walking_path",
        "points": len(path_coords),
        "sessions": {
            "2026-06-22": n_walks_22,
            "2026-06-28": n_walks_28,
        },
        "start": path_timestamps[0] if path_timestamps else None,
        "end":   path_timestamps[-1] if path_timestamps else None,
        "total_session_minutes": round(total_session, 1) if path_timestamps else None,
        "note": "Chronologically ordered — shows the exact route Wes walked (multi-segment across the two sessions).",
    },
    "features": [{
        "type": "Feature",
        "properties": {
            "name": "Wesley's walking path",
            "category": "walking_path",
            "category_per_point": path_categories,
            "timestamps": path_timestamps,
            "polyline_style": "dashed-by-session" if n_walks_22 and n_walks_28 else "solid",
        },
        "geometry": {"type": "LineString", "coordinates": path_coords},
    }],
}
with open(OUT_DIR / "client_gps_walking_path.geojson", "w") as f:
    json.dump(walking_path_fc, f, indent=2)
print(f"✓ {OUT_DIR / 'client_gps_walking_path.geojson'}  ({len(path_coords)} pts, "
      f"{n_walks_22}+{n_walks_28} pts across 2 sessions)")

# Print walking analysis
def fmt_min(m):
    if m < 60: return f"{m:.1f} min"
    h = int(m // 60); mm = int(m % 60)
    return f"{h}h {mm}m"

print(f"  walking session:")
print(f"    2026-06-22: {n_walks_22} points")
print(f"    2026-06-28: {n_walks_28} points")
if path_timestamps:
    print(f"    span: {path_timestamps[0]} → {path_timestamps[-1]}")
    print(f"    total capture span: {fmt_min(total_session)}")
if duration_min:
    longest_gap_idx = duration_min.index(max(duration_min))
    # Find the two ordered (ts, pt) pairs that bracket the gap
    sorted_ids = [f["properties"]["id"] for _, f in all_with_time]
    # The "between X and next" — name them by feature id (the waypoint index)
    if longest_gap_idx + 1 < len(sorted_ids):
        prev_id = sorted_ids[longest_gap_idx]
        next_id = sorted_ids[longest_gap_idx + 1]
        prev_c = by_id[prev_id]["geometry"]["coordinates"]
        next_c = by_id[next_id]["geometry"]["coordinates"]
        gap_dist_km = haversine_km((prev_c[0], prev_c[1]), (next_c[0], next_c[1]))
        print(f"    longest pause between points: {fmt_min(duration_min[longest_gap_idx])}  "
              f"(id {prev_id}→{next_id}, ~{gap_dist_km:.1f} km)")
    else:
        print(f"    longest pause between points: {fmt_min(duration_min[longest_gap_idx])}")
print()


# ============================================================
# 5. Walking path split by session (so we can style the two days distinctly)
# ============================================================
def session_path(date_prefix):
    pts = [(ts, p) for ts, p in all_with_time if ts.startswith(date_prefix)]
    return pts

splits = {
    "2026-06-22": [p["geometry"]["coordinates"] for _, p in session_path("2026-06-22")],
    "2026-06-28": [p["geometry"]["coordinates"] for _, p in session_path("2026-06-28")],
}
walking_sessions_fc = {
    "type": "FeatureCollection",
    "name": "client_gps_walking_sessions",
    "metadata": {
        "source": "Wesley van de Camp GPS walk via Guru Maps GPX",
        "category": "walking_session",
        "note": "Two separate walks: 2026-06-22 (5 points, north side) + 2026-06-28 (15 points, full perimeter).",
    },
    "features": [],
}
session_meta = {
    "2026-06-22": {"name": "First walk (2026-06-22) — northern corner & high point",
                  "color": "#a855f7", "dashArray": "6 4"},
    "2026-06-28": {"name": "Main perimeter walk (2026-06-28)",
                  "color": "#f59e0b", "dashArray": "8 4"},
}
for k, coords in splits.items():
    if not coords: continue
    meta = session_meta[k]
    walking_sessions_fc["features"].append({
        "type": "Feature",
        "properties": {
            "name": meta["name"],
            "session_date": k,
            "color": meta["color"],
            "dashArray": meta["dashArray"],
            "stroke_width": 3,
            "category": "walking_session",
            "point_count": len(coords),
        },
        "geometry": {"type": "LineString", "coordinates": coords},
    })
with open(OUT_DIR / "client_gps_walking_sessions.geojson", "w") as f:
    json.dump(walking_sessions_fc, f, indent=2)
print(f"✓ {OUT_DIR / 'client_gps_walking_sessions.geojson'}  ({len(walking_sessions_fc['features'])} session lines)")


# ============================================================
# 6. Legacy polygons (escobar KML + 62 ha AOI) — copied from existing repo files
# ============================================================
esc = json.load(open(ESC_OLD))
old_centroid = esc["features"][0]["properties"].get("centroid_lon"), esc["features"][0]["properties"].get("centroid_lat")
esc_fc = {
    "type": "FeatureCollection",
    "name": "escobar_polygon_legacy",
    "metadata": {
        "source": "Wesley van de Camp KML via Google Earth Pro",
        "received_utc": "2026-06-28",
        "note": "8-vertex polygon shared with the post-escritura site-knowledge package. "
                "30.9 ha projected — appears to be an INTERIOR buildable subset of the full "
                "GPS-walk polygon, NOT the full perimeter.",
        "replaced_by": "client_gps_polygon.geojson (the on-the-ground walking perimeter)",
    },
    "features": esc["features"],
}
with open(OUT_DIR / "escobar_polygon_legacy.geojson", "w") as f:
    json.dump(esc_fc, f, indent=2)
print(f"✓ {OUT_DIR / 'escobar_polygon_legacy.geojson'}  (legacy KML subset)")

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

# Also copy the raw KML + GPX into deploy dir for downloadability
deploy_raw = OUT_DIR / "raw"
deploy_raw.mkdir(parents=True, exist_ok=True)
for src_name in ("guru_maps.geojson", "guru_maps.gpx", "guru_maps.kml"):
    src = ROOT / "docs/site_data/property_gps_walk_2026-06-28" / src_name
    if src.exists():
        (deploy_raw / src_name).write_bytes(src.read_bytes())
        print(f"✓ {deploy_raw / src_name}  ({src.stat().st_size:,} bytes, raw mirror)")

print(f"\n=== Summary ===")
print(f"Wrote 6+ GeoJSON files to {OUT_DIR}/ and {len(fetched)} mirrors of the live data")
print(f"Map now has access to: {len(corners_features)} corners + {len(features_features)} features + walking path + 2 walking sessions")
