#!/usr/bin/env python3
"""Phase-0 §12 Batch C — pull building footprints from open ML datasets within
the polygon AOI ±1 km buffer:

- Microsoft GlobalMLBuildingFootprints (CSV+GeoJSON tiles indexed by Bing
  quadkey, level 9)
- Google Open Buildings v3 (CSV.gz polygons indexed by S2 level-4 token)

Overture buildings is deliberately skipped — it requires DuckDB or
GeoPandas/Parquet, neither of which is installable here without
`--break-system-packages`. MS + Google together cover Overture's building
contributors for this region (Overture's building theme is largely the
merge of MS + Google + OSM, and OSM was already harvested in v1).

Outputs land under `docs/site_data/infrastructure/buildings/`:
- ms_buildings_<quadkey>.geojson — raw MS rows clipped to AOI bbox
- google_buildings_<tile>.geojson — raw Google rows clipped to AOI bbox
- buildings_combined.geojson — union FeatureCollection (source-tagged)
- summary.md — per-source counts + footprint area + nearest-to-centroid
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import math
import sys
import time
import zipfile
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "site_data" / "infrastructure" / "buildings"
OUT.mkdir(parents=True, exist_ok=True)

# Polygon AOI bbox (Wesley's 30.9 ha buildable) +1 km buffer to catch neighbours
CENTROID_LON, CENTROID_LAT = -57.0355, -25.6073
BUFFER_KM = 1.0
DLAT = BUFFER_KM / 111.0
DLON = BUFFER_KM / (111.0 * math.cos(math.radians(CENTROID_LAT)))
POLY_W, POLY_S, POLY_E, POLY_N = -57.050, -25.625, -57.020, -25.595
AOI_W = POLY_W - DLON
AOI_S = POLY_S - DLAT
AOI_E = POLY_E + DLON
AOI_N = POLY_N + DLAT
print(f"AOI W{AOI_W:.4f} S{AOI_S:.4f} E{AOI_E:.4f} N{AOI_N:.4f}", flush=True)

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "lqv-phase0/1.0 (research; weissvanderpol.ivan@gmail.com)"})
_retry = Retry(
    total=6,
    backoff_factor=1.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET", "HEAD"),
    raise_on_status=False,
)
_adapter = HTTPAdapter(max_retries=_retry, pool_connections=4, pool_maxsize=4)
SESSION.mount("https://", _adapter)
SESSION.mount("http://", _adapter)


def _get(url: str, **kw):
    last: Exception | None = None
    for attempt in range(4):
        try:
            return SESSION.get(url, timeout=kw.pop("timeout", 120), **kw)
        except requests.exceptions.RequestException as e:
            last = e
            time.sleep(2 ** attempt)
    raise last  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Geometry helpers (stdlib only — bbox + centroid + shoelace area)
# ---------------------------------------------------------------------------

def polygon_centroid(coords: list[list[float]]) -> tuple[float, float]:
    """Centroid of a simple polygon (first ring only). coords = [[lon, lat], ...]."""
    n = len(coords)
    if n == 0:
        return (0.0, 0.0)
    cx = 0.0
    cy = 0.0
    a = 0.0
    for i in range(n - 1):
        x0, y0 = coords[i]
        x1, y1 = coords[i + 1]
        cross = x0 * y1 - x1 * y0
        a += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    a *= 0.5
    if abs(a) < 1e-12:
        # degenerate — fall back to bbox center
        xs = [p[0] for p in coords]
        ys = [p[1] for p in coords]
        return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
    return (cx / (6 * a), cy / (6 * a))


def polygon_area_m2(coords: list[list[float]], lat0: float) -> float:
    """Approximate polygon area in m² via local equirectangular projection."""
    if not coords:
        return 0.0
    mx = 111_320.0 * math.cos(math.radians(lat0))
    my = 110_540.0
    pts = [(c[0] * mx, c[1] * my) for c in coords]
    a = 0.0
    n = len(pts)
    for i in range(n - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        a += x0 * y1 - x1 * y0
    return abs(a) * 0.5


def bbox_contains(lon: float, lat: float) -> bool:
    return AOI_W <= lon <= AOI_E and AOI_S <= lat <= AOI_N


def bboxes_intersect(b1: tuple[float, float, float, float],
                     b2: tuple[float, float, float, float]) -> bool:
    return not (b1[2] < b2[0] or b1[0] > b2[2] or b1[3] < b2[1] or b1[1] > b2[3])


def haversine_km(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    r = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


# ---------------------------------------------------------------------------
# Bing quadkey (MS Building Footprints index)
# ---------------------------------------------------------------------------

def lonlat_to_tile(lon: float, lat: float, zoom: int) -> tuple[int, int]:
    """Bing/OSM XYZ tile index for lon/lat at given zoom."""
    lat = max(min(lat, 85.05112878), -85.05112878)
    n = 2 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    sin_lat = math.sin(math.radians(lat))
    y = int((1.0 - math.log((1 + sin_lat) / (1 - sin_lat)) / (2 * math.pi)) / 2 * n)
    return x, y


def tile_to_quadkey(x: int, y: int, zoom: int) -> str:
    qk = []
    for i in range(zoom, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if x & mask:
            digit += 1
        if y & mask:
            digit += 2
        qk.append(str(digit))
    return "".join(qk)


def aoi_quadkeys(zoom: int = 9) -> list[str]:
    xs = []
    ys = []
    for lon, lat in [(AOI_W, AOI_N), (AOI_E, AOI_N), (AOI_E, AOI_S), (AOI_W, AOI_S)]:
        x, y = lonlat_to_tile(lon, lat, zoom)
        xs.append(x)
        ys.append(y)
    qks = set()
    for xi in range(min(xs), max(xs) + 1):
        for yi in range(min(ys), max(ys) + 1):
            qks.add(tile_to_quadkey(xi, yi, zoom))
    return sorted(qks)


# ---------------------------------------------------------------------------
# Microsoft GlobalMLBuildingFootprints
# ---------------------------------------------------------------------------

MS_INDEX_URL = "https://minedbuildings.z5.web.core.windows.net/global-buildings/dataset-links.csv"


def fetch_ms_index() -> list[dict]:
    print("[MS] fetching dataset-links.csv…", flush=True)
    r = _get(MS_INDEX_URL, timeout=120)
    if r.status_code != 200:
        print(f"[MS] !! index HTTP {r.status_code}; skipping MS", flush=True)
        return []
    rdr = csv.DictReader(io.StringIO(r.text))
    return [row for row in rdr]


def ms_filter_quadkeys(index: list[dict], qks: set[str]) -> list[dict]:
    matched = []
    for row in index:
        qk = (row.get("QuadKey") or "").strip()
        if qk in qks:
            matched.append(row)
    return matched


def ms_pull_tile(row: dict) -> list[dict]:
    url = row.get("Url") or ""
    loc = row.get("Location") or ""
    qk = row.get("QuadKey") or ""
    if not url:
        return []
    print(f"  [MS] {loc} qk={qk} → fetching {url.split('/')[-1]}…", flush=True)
    try:
        r = _get(url, timeout=300, stream=True)
        if r.status_code != 200:
            print(f"    !! HTTP {r.status_code}; skipping", flush=True)
            return []
        raw = r.content
    except Exception as e:
        print(f"    !! fetch failed: {type(e).__name__}: {e}", flush=True)
        return []

    features: list[dict] = []

    def _parse_lines(stream) -> None:
        for line in stream:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            geom = rec.get("geometry")
            props = rec.get("properties") or {}
            if not geom:
                continue
            if geom.get("type") not in ("Polygon", "MultiPolygon"):
                continue
            rings = []
            if geom["type"] == "Polygon":
                rings = [geom["coordinates"][0]]
            else:
                rings = [poly[0] for poly in geom["coordinates"]]
            ring = rings[0]
            cx, cy = polygon_centroid(ring)
            if not bbox_contains(cx, cy):
                continue
            features.append(
                {
                    "type": "Feature",
                    "geometry": geom,
                    "properties": {
                        "source": "ms_global_ml",
                        "quadkey": qk,
                        "location": loc,
                        "ms_confidence": props.get("confidence"),
                        "ms_height_m": props.get("height"),
                        "centroid_lon": cx,
                        "centroid_lat": cy,
                        "footprint_m2": polygon_area_m2(ring, cy),
                    },
                }
            )

    if url.endswith(".csv.gz") or "gzip" in (r.headers.get("Content-Type") or "").lower():
        # MS commonly serves a CSV.gz with columns QuadKey,Geometry (GeoJSON) plus
        # optional height/confidence. Try gzip+CSV first; fall back to gzip+JSONL.
        try:
            buf = gzip.decompress(raw)
            try:
                rdr = csv.DictReader(io.StringIO(buf.decode("utf-8")))
                seen_geom_col = False
                for row2 in rdr:
                    geom_str = (
                        row2.get("Geometry")
                        or row2.get("geometry")
                        or row2.get("GEOMETRY")
                        or ""
                    )
                    if not geom_str:
                        continue
                    seen_geom_col = True
                    try:
                        geom = json.loads(geom_str)
                    except json.JSONDecodeError:
                        continue
                    if geom.get("type") not in ("Polygon", "MultiPolygon"):
                        continue
                    if geom["type"] == "Polygon":
                        ring = geom["coordinates"][0]
                    else:
                        ring = geom["coordinates"][0][0]
                    cx, cy = polygon_centroid(ring)
                    if not bbox_contains(cx, cy):
                        continue
                    features.append(
                        {
                            "type": "Feature",
                            "geometry": geom,
                            "properties": {
                                "source": "ms_global_ml",
                                "quadkey": qk,
                                "location": loc,
                                "ms_confidence": row2.get("Confidence"),
                                "ms_height_m": row2.get("Height"),
                                "centroid_lon": cx,
                                "centroid_lat": cy,
                                "footprint_m2": polygon_area_m2(ring, cy),
                            },
                        }
                    )
                if not seen_geom_col:
                    _parse_lines(io.StringIO(buf.decode("utf-8")))
            except Exception:
                _parse_lines(io.StringIO(buf.decode("utf-8")))
        except Exception as e:
            print(f"    !! gunzip failed: {type(e).__name__}: {e}", flush=True)
            return []
    elif url.endswith(".zip"):
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as zf:
                for name in zf.namelist():
                    with zf.open(name) as fh:
                        _parse_lines(io.TextIOWrapper(fh, encoding="utf-8"))
        except Exception as e:
            print(f"    !! unzip failed: {type(e).__name__}: {e}", flush=True)
            return []
    else:
        # Plain JSONL
        _parse_lines(io.StringIO(raw.decode("utf-8", errors="ignore")))

    print(f"    → {len(features)} features inside AOI", flush=True)
    return features


# ---------------------------------------------------------------------------
# Google Open Buildings v3 (S2 level-4 tiles)
# ---------------------------------------------------------------------------

GOOGLE_TILES_URL = (
    "https://sites.research.google/open-buildings/tiles.geojson"
)
GOOGLE_TILE_URL_TEMPLATE = (
    "https://storage.googleapis.com/open-buildings-data/v3/"
    "polygons_s2_level_4_gzip_no_header/{tile_id}_buildings.csv.gz"
)


def fetch_google_tiles_index() -> list[dict]:
    print("[Google] fetching open-buildings tiles index…", flush=True)
    for url in (
        GOOGLE_TILES_URL,
        "https://sites.research.google/gr/open-buildings/tiles.geojson",
    ):
        try:
            r = _get(url, timeout=120)
            if r.status_code == 200 and r.text.lstrip().startswith("{"):
                fc = r.json()
                return fc.get("features") or []
        except Exception as e:
            print(f"  ?? {url} failed: {type(e).__name__}: {e}", flush=True)
    print("[Google] !! tiles index unavailable; skipping Google", flush=True)
    return []


def aoi_bbox() -> tuple[float, float, float, float]:
    return (AOI_W, AOI_S, AOI_E, AOI_N)


def tile_feature_bbox(feat: dict) -> tuple[float, float, float, float] | None:
    geom = feat.get("geometry") or {}
    if geom.get("type") not in ("Polygon", "MultiPolygon"):
        return None
    if geom["type"] == "Polygon":
        ring = geom["coordinates"][0]
    else:
        ring = geom["coordinates"][0][0]
    xs = [p[0] for p in ring]
    ys = [p[1] for p in ring]
    return (min(xs), min(ys), max(xs), max(ys))


def google_pull_tile(tile_id: str) -> list[dict]:
    url = GOOGLE_TILE_URL_TEMPLATE.format(tile_id=tile_id)
    print(f"  [Google] tile {tile_id} → {url.split('/')[-1]}…", flush=True)
    try:
        r = _get(url, timeout=300)
    except Exception as e:
        print(f"    !! fetch failed: {type(e).__name__}: {e}", flush=True)
        return []
    if r.status_code != 200:
        print(f"    !! HTTP {r.status_code}", flush=True)
        return []
    try:
        buf = gzip.decompress(r.content).decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"    !! gunzip failed: {type(e).__name__}: {e}", flush=True)
        return []
    # No header v3 schema: latitude, longitude, area_in_meters, confidence, geometry, full_plus_code
    features: list[dict] = []
    for row in csv.reader(io.StringIO(buf)):
        if len(row) < 5:
            continue
        try:
            lat = float(row[0])
            lon = float(row[1])
        except ValueError:
            continue
        if not bbox_contains(lon, lat):
            continue
        try:
            area = float(row[2])
        except (ValueError, IndexError):
            area = None
        try:
            conf = float(row[3])
        except (ValueError, IndexError):
            conf = None
        wkt = row[4] if len(row) > 4 else ""
        # Parse simple POLYGON WKT
        ring: list[list[float]] = []
        if wkt.startswith("POLYGON"):
            inner = wkt[wkt.index("((") + 2: wkt.rindex("))")]
            for p in inner.split(","):
                xy = p.strip().split(" ")
                if len(xy) == 2:
                    try:
                        ring.append([float(xy[0]), float(xy[1])])
                    except ValueError:
                        pass
        if not ring:
            ring = [[lon, lat]]
        plus_code = row[5] if len(row) > 5 else ""
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": [ring]},
                "properties": {
                    "source": "google_open_buildings_v3",
                    "tile_id": tile_id,
                    "google_confidence": conf,
                    "google_area_m2": area,
                    "centroid_lon": lon,
                    "centroid_lat": lat,
                    "full_plus_code": plus_code,
                    "footprint_m2": polygon_area_m2(ring, lat) if len(ring) > 2 else area,
                },
            }
        )
    print(f"    → {len(features)} features inside AOI", flush=True)
    return features


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def write_geojson(path: Path, features: list[dict]) -> None:
    fc = {"type": "FeatureCollection", "features": features}
    path.write_text(json.dumps(fc), encoding="utf-8")


def main() -> int:
    aoi_bb = aoi_bbox()
    all_features: list[dict] = []
    ms_features: list[dict] = []
    google_features: list[dict] = []
    ms_qks: list[str] = []
    google_tiles_used: list[str] = []

    # -- MS Building Footprints --
    qks = aoi_quadkeys(9)
    print(f"[MS] AOI maps to quadkeys (z=9): {qks}", flush=True)
    qkset = set(qks)
    try:
        index = fetch_ms_index()
    except Exception as e:
        print(f"[MS] index fetch errored: {type(e).__name__}: {e}", flush=True)
        index = []
    if index:
        matches = ms_filter_quadkeys(index, qkset)
        print(f"[MS] {len(matches)} index rows match AOI quadkeys", flush=True)
        for row in matches:
            tile_feats = ms_pull_tile(row)
            ms_features.extend(tile_feats)
            ms_qks.append(row.get("QuadKey") or "")
        if ms_features:
            write_geojson(OUT / "ms_buildings.geojson", ms_features)
            print(f"[MS] wrote ms_buildings.geojson ({len(ms_features)} features)", flush=True)
    else:
        print("[MS] no index rows; skipping", flush=True)

    # -- Google Open Buildings v3 --
    tiles = fetch_google_tiles_index()
    print(f"[Google] tiles index: {len(tiles)} entries", flush=True)
    if tiles:
        cand_ids: list[str] = []
        for feat in tiles:
            tb = tile_feature_bbox(feat)
            if tb and bboxes_intersect(tb, aoi_bb):
                props = feat.get("properties") or {}
                tid = (
                    props.get("tile_id")
                    or props.get("s2_token")
                    or props.get("tileId")
                    or props.get("id")
                )
                if tid:
                    cand_ids.append(str(tid))
        print(f"[Google] candidate tiles intersecting AOI: {cand_ids}", flush=True)
        for tid in cand_ids:
            feats = google_pull_tile(tid)
            google_features.extend(feats)
            google_tiles_used.append(tid)
        if google_features:
            write_geojson(OUT / "google_buildings.geojson", google_features)
            print(
                f"[Google] wrote google_buildings.geojson ({len(google_features)} features)",
                flush=True,
            )

    all_features = ms_features + google_features
    write_geojson(OUT / "buildings_combined.geojson", all_features)
    print(f"[combined] {len(all_features)} features → buildings_combined.geojson", flush=True)

    # -- Summary --
    by_src: dict[str, int] = {}
    total_area: dict[str, float] = {}
    nearest: dict[str, tuple[float, dict]] = {}
    for f in all_features:
        src = (f.get("properties") or {}).get("source") or "?"
        by_src[src] = by_src.get(src, 0) + 1
        a = (f.get("properties") or {}).get("footprint_m2") or 0
        total_area[src] = total_area.get(src, 0.0) + float(a)
        cx = (f.get("properties") or {}).get("centroid_lon")
        cy = (f.get("properties") or {}).get("centroid_lat")
        if cx is None or cy is None:
            continue
        d = haversine_km(cx, cy, CENTROID_LON, CENTROID_LAT)
        cur = nearest.get(src)
        if cur is None or d < cur[0]:
            nearest[src] = (d, f)

    md = ["# Building footprints — MS + Google Open Buildings (AOI ±1 km)", ""]
    md.append(
        f"AOI bbox W{AOI_W:.4f} S{AOI_S:.4f} E{AOI_E:.4f} N{AOI_N:.4f} "
        f"(polygon ±{BUFFER_KM:.1f} km)"
    )
    md.append(f"Centroid: `{CENTROID_LON}, {CENTROID_LAT}`")
    md.append("")
    md.append("## Counts")
    md.append("")
    md.append("| Source | Buildings | Σ footprint m² |")
    md.append("|---|---:|---:|")
    for src in sorted(by_src):
        md.append(f"| {src} | {by_src[src]} | {total_area.get(src, 0):.0f} |")
    md.append(
        f"| **TOTAL** | **{sum(by_src.values())}** | **{sum(total_area.values()):.0f}** |"
    )
    md.append("")
    md.append("## Nearest building to polygon centroid (per source)")
    md.append("")
    if nearest:
        md.append("| Source | Distance (km) | Centroid (lon, lat) | Footprint m² |")
        md.append("|---|---:|---|---:|")
        for src, (d, feat) in sorted(nearest.items(), key=lambda kv: kv[1][0]):
            p = feat.get("properties") or {}
            md.append(
                f"| {src} | {d:.3f} | `{p.get('centroid_lon'):.5f}, {p.get('centroid_lat'):.5f}` | "
                f"{(p.get('footprint_m2') or 0):.0f} |"
            )
    else:
        md.append("_No buildings found inside AOI (±1 km buffer)._")
    md.append("")
    md.append("## Provenance")
    md.append("")
    md.append(f"- MS quadkeys queried (z=9): `{', '.join(qks)}`")
    md.append(f"- MS quadkeys with data returned: `{', '.join(sorted(set(ms_qks))) or '(none)'}`")
    md.append(f"- Google S2 tiles queried: `{', '.join(google_tiles_used) or '(none)'}`")
    md.append("- Overture buildings: **deferred** — requires DuckDB/GeoParquet")
    md.append("  (Overture's building theme is largely the merge of MS + Google + OSM;")
    md.append("  OSM buildings already harvested in v1 at `docs/site_data/property_map/`.)")
    md.append("")
    md.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}")
    (OUT / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("summary.md written", flush=True)
    print("Done.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
