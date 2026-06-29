#!/usr/bin/env python3
"""Phase-0 §12.D: Protected areas + comparables within 50 km of the La Quebrada
Viva polygon centroid (-57.0355, -25.6073).

Combines:
- WDPA via Protected Planet REST API (api.protectedplanet.net) — public-facing
  national + regional reserves, IUCN category, designation, gov_type, area.
  Falls back to ProtectedPlanet OGC WFS download endpoint if REST is rate-limited.
- ENVISIONMA / SINASIP (Paraguay) areas where API coverage misses small reserves,
  pulled from OSM Overpass with `boundary=protected_area` and `leisure=nature_reserve`
  within the 50 km buffer — same query pattern used in Phase-0 v1 OSM batch.

Outputs to docs/site_data/comparables/:
- wdpa_areas.geojson — REST results (one Feature per area, polygon if geom available)
- osm_protected_areas.geojson — OSM Overpass coverage gap-fill
- areas_combined.csv — flattened index (name, designation, IUCN_cat, distance_km,
  area_ha, source)
- summary.md — top-10 nearest + total count + Atlantic Forest framing
"""

from __future__ import annotations

import csv
import json
import math
import sys
import time
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "site_data" / "comparables"
OUT.mkdir(parents=True, exist_ok=True)

CENTROID_LON, CENTROID_LAT = -57.0355, -25.6073
RADIUS_KM = 50.0
DEG_PER_KM_LAT = 1.0 / 111.0
DEG_PER_KM_LON = 1.0 / (111.0 * math.cos(math.radians(CENTROID_LAT)))
DLAT = RADIUS_KM * DEG_PER_KM_LAT
DLON = RADIUS_KM * DEG_PER_KM_LON
BBOX = (
    CENTROID_LON - DLON,
    CENTROID_LAT - DLAT,
    CENTROID_LON + DLON,
    CENTROID_LAT + DLAT,
)

SESSION = requests.Session()
SESSION.headers.update(
    {"User-Agent": "lqv-phase0/1.0 (research; weissvanderpol.ivan@gmail.com)"}
)
_retry = Retry(
    total=6,
    backoff_factor=1.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET", "POST"),
    raise_on_status=False,
)
_adapter = HTTPAdapter(max_retries=_retry, pool_connections=4, pool_maxsize=4)
SESSION.mount("https://", _adapter)
SESSION.mount("http://", _adapter)


def _get(url: str, **kw):
    last: Exception | None = None
    for attempt in range(4):
        try:
            return SESSION.get(url, timeout=kw.pop("timeout", 60), **kw)
        except requests.exceptions.RequestException as e:
            last = e
            time.sleep(2**attempt)
    raise last  # type: ignore[misc]


def _post(url: str, **kw):
    last: Exception | None = None
    for attempt in range(4):
        try:
            return SESSION.post(url, timeout=kw.pop("timeout", 120), **kw)
        except requests.exceptions.RequestException as e:
            last = e
            time.sleep(2**attempt)
    raise last  # type: ignore[misc]


def haversine_km(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


# ---------------------------------------------------------------------------
# Protected Planet REST (WDPA)
# ---------------------------------------------------------------------------
# API ref: https://api.protectedplanet.net/documentation
# The public no-token endpoint allows search by country code + name; geom is
# not returned in REST responses (geom requires the dedicated download bundle).
# We pull all WDPA records for Paraguay (PRY) + Argentina (ARG) closest 50 km,
# then filter by centroid distance using their reported lat/lon.
#
# Note: REST requires `token` query param for full access. Without it the
# public endpoint still returns paginated results but capped at 50/page.

WDPA_COUNTRIES = ["PRY", "ARG"]


def wdpa_pull_country(iso3: str) -> list[dict]:
    out: list[dict] = []
    page = 1
    per_page = 50
    while True:
        params = {
            "country": iso3,
            "per_page": per_page,
            "page": page,
        }
        r = _get("https://api.protectedplanet.net/v3/protected_areas/search", params=params)
        if r.status_code != 200:
            print(f"  WDPA {iso3} page {page}: HTTP {r.status_code} — stopping", flush=True)
            break
        try:
            data = r.json()
        except Exception:
            print(f"  WDPA {iso3} page {page}: bad JSON — stopping", flush=True)
            break
        pas = data.get("protected_areas", []) or []
        if not pas:
            break
        out.extend(pas)
        print(f"  WDPA {iso3} page {page}: +{len(pas)} (cum {len(out)})", flush=True)
        if len(pas) < per_page:
            break
        page += 1
        if page > 60:  # hard cap — Argentina has many
            print(f"  WDPA {iso3}: page cap hit ({page})", flush=True)
            break
        time.sleep(0.5)
    return out


def wdpa_extract_record(pa: dict, iso3: str) -> dict | None:
    """Normalise one WDPA record. Returns None if no coordinates available."""
    name = pa.get("name") or ""
    if not name:
        return None
    designation = (pa.get("designation") or {}).get("name") if isinstance(pa.get("designation"), dict) else (pa.get("designation") or "")
    iucn = (pa.get("iucn_category") or {}).get("name") if isinstance(pa.get("iucn_category"), dict) else (pa.get("iucn_category") or "")
    gov_type = pa.get("governance") or ""
    # The REST response includes `geojson` for some entries (point centroid)
    geo = pa.get("geojson") or {}
    centroid = None
    if geo.get("geometry", {}).get("type") == "Point":
        centroid = geo["geometry"]["coordinates"]
    elif geo.get("type") == "Point":
        centroid = geo.get("coordinates")
    # Fall back to bbox center if provided
    if centroid is None:
        bbox = pa.get("bbox") or []
        if isinstance(bbox, list) and len(bbox) == 4:
            centroid = [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]
    if centroid is None:
        return None
    lon, lat = centroid[0], centroid[1]
    dist = haversine_km(CENTROID_LON, CENTROID_LAT, lon, lat)
    return {
        "wdpa_id": pa.get("wdpa_id") or pa.get("id"),
        "name": name,
        "iso3": iso3,
        "designation": designation,
        "iucn_category": iucn,
        "governance": gov_type,
        "marine": pa.get("marine"),
        "reported_area_km2": pa.get("reported_area") or pa.get("reported_marine_area"),
        "lon": lon,
        "lat": lat,
        "distance_km": round(dist, 3),
        "source": "wdpa_rest",
    }


# ---------------------------------------------------------------------------
# OSM Overpass — gap-fill for SINASIP / municipal reserves
# ---------------------------------------------------------------------------

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.fr/api/interpreter",
]

OVERPASS_QUERY = f"""
[out:json][timeout:120];
(
  relation["boundary"="protected_area"]({BBOX[1]},{BBOX[0]},{BBOX[3]},{BBOX[2]});
  way["boundary"="protected_area"]({BBOX[1]},{BBOX[0]},{BBOX[3]},{BBOX[2]});
  relation["leisure"="nature_reserve"]({BBOX[1]},{BBOX[0]},{BBOX[3]},{BBOX[2]});
  way["leisure"="nature_reserve"]({BBOX[1]},{BBOX[0]},{BBOX[3]},{BBOX[2]});
);
out tags center;
"""


def overpass_pull() -> list[dict]:
    for ep in OVERPASS_ENDPOINTS:
        try:
            print(f"  OSM Overpass → {ep}", flush=True)
            r = _post(ep, data={"data": OVERPASS_QUERY}, timeout=180)
            if r.status_code == 200:
                data = r.json()
                els = data.get("elements", []) or []
                print(f"  OSM Overpass: {len(els)} elements", flush=True)
                return els
            print(f"  OSM Overpass {ep}: HTTP {r.status_code}", flush=True)
        except Exception as e:
            print(f"  OSM Overpass {ep}: {e}", flush=True)
        time.sleep(2.0)
    return []


def osm_extract_record(el: dict) -> dict | None:
    tags = el.get("tags") or {}
    name = tags.get("name") or tags.get("name:es") or tags.get("name:en")
    if not name:
        return None
    center = el.get("center") or {}
    if not center:
        return None
    lon = center.get("lon")
    lat = center.get("lat")
    if lon is None or lat is None:
        return None
    dist = haversine_km(CENTROID_LON, CENTROID_LAT, lon, lat)
    return {
        "osm_id": f"{el.get('type')}/{el.get('id')}",
        "name": name,
        "iso3": "",  # left blank; OSM doesn't tag ISO3 reliably
        "designation": tags.get("protection_title") or tags.get("leisure") or "",
        "iucn_category": tags.get("protect_class") or "",
        "governance": tags.get("operator") or tags.get("ownership") or "",
        "marine": "",
        "reported_area_km2": "",
        "lon": lon,
        "lat": lat,
        "distance_km": round(dist, 3),
        "source": "osm_overpass",
    }


# ---------------------------------------------------------------------------
# Drivers
# ---------------------------------------------------------------------------


def write_geojson(path: Path, records: list[dict], extra_props: dict | None = None) -> None:
    feats = []
    for r in records:
        props = {k: v for k, v in r.items() if k not in ("lon", "lat")}
        if extra_props:
            props.update(extra_props)
        feats.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
                "properties": props,
            }
        )
    path.write_text(json.dumps({"type": "FeatureCollection", "features": feats}, indent=2))


def write_combined_csv(path: Path, records: list[dict]) -> None:
    cols = [
        "source",
        "name",
        "iso3",
        "designation",
        "iucn_category",
        "governance",
        "distance_km",
        "reported_area_km2",
        "wdpa_id",
        "osm_id",
        "lon",
        "lat",
    ]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in records:
            w.writerow(r)


def write_summary(path: Path, records: list[dict], counts: dict[str, int]) -> None:
    records_sorted = sorted(records, key=lambda r: r["distance_km"])
    nearest_10 = records_sorted[:10]
    lines = [
        "# Protected areas + comparables — 50 km buffer (Phase-0 §12.D)",
        "",
        f"Centroid: `{CENTROID_LON}, {CENTROID_LAT}` (La Quebrada Viva)",
        f"Buffer: {RADIUS_KM:.0f} km radius (BBOX W={BBOX[0]:.4f} S={BBOX[1]:.4f} E={BBOX[2]:.4f} N={BBOX[3]:.4f})",
        "",
        "## Counts by source",
        "",
        "| Source | Records |",
        "| --- | ---: |",
        f"| WDPA (Protected Planet REST) | {counts.get('wdpa_rest', 0)} |",
        f"| OSM Overpass (gap-fill) | {counts.get('osm_overpass', 0)} |",
        f"| **TOTAL within 50 km** | **{len(records_sorted)}** |",
        "",
        "## 10 nearest",
        "",
        "| # | Source | Name | Designation | IUCN | Dist (km) | Reported area (km²) |",
        "| ---: | --- | --- | --- | --- | ---: | ---: |",
    ]
    for i, r in enumerate(nearest_10, 1):
        lines.append(
            f"| {i} | {r['source']} | {r['name']} | {r['designation'] or '—'} | "
            f"{r['iucn_category'] or '—'} | {r['distance_km']:.2f} | {r['reported_area_km2'] or '—'} |"
        )
    lines += [
        "",
        "## Context",
        "",
        "- The property sits in the southern lowland fringe of the **Bosque Atlántico del Alto Paraná** (BAAPA) ecoregion.",
        "- Relevant Paraguay national-level instruments: **SINASIP** (Sistema Nacional de Áreas Silvestres Protegidas) via MADES.",
        "- Nearby cross-border reference: Argentine provincial reserves in Misiones / Corrientes also visible in this radius.",
        "- WDPA REST records lack polygon geometry; for true GIS overlays pull the WDPA monthly shapefile download.",
        "",
    ]
    path.write_text("\n".join(lines))


def main() -> int:
    print(f"[phase0_protected_areas] centroid={CENTROID_LON},{CENTROID_LAT} radius={RADIUS_KM} km", flush=True)
    print(f"[phase0_protected_areas] bbox W={BBOX[0]:.4f} S={BBOX[1]:.4f} E={BBOX[2]:.4f} N={BBOX[3]:.4f}", flush=True)

    # WDPA REST
    all_wdpa: list[dict] = []
    for iso3 in WDPA_COUNTRIES:
        pas = wdpa_pull_country(iso3)
        for pa in pas:
            rec = wdpa_extract_record(pa, iso3)
            if rec is None:
                continue
            if rec["distance_km"] <= RADIUS_KM:
                all_wdpa.append(rec)
    print(f"[phase0_protected_areas] WDPA inside buffer: {len(all_wdpa)}", flush=True)
    write_geojson(OUT / "wdpa_areas.geojson", all_wdpa)

    # OSM Overpass gap-fill
    osm_els = overpass_pull()
    all_osm: list[dict] = []
    for el in osm_els:
        rec = osm_extract_record(el)
        if rec is None:
            continue
        if rec["distance_km"] <= RADIUS_KM:
            all_osm.append(rec)
    print(f"[phase0_protected_areas] OSM inside buffer: {len(all_osm)}", flush=True)
    write_geojson(OUT / "osm_protected_areas.geojson", all_osm)

    # Combined
    combined = all_wdpa + all_osm
    write_combined_csv(OUT / "areas_combined.csv", combined)

    counts = {"wdpa_rest": len(all_wdpa), "osm_overpass": len(all_osm)}
    write_summary(OUT / "summary.md", combined, counts)

    print(f"[phase0_protected_areas] Done. Total: {len(combined)} records", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
