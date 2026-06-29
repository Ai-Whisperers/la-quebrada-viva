#!/usr/bin/env python3
"""Phase-0 §12.4: pull GBIF + iNaturalist species occurrences within 25 km of the
La Quebrada Viva polygon centroid (-57.0355, -25.6073). Augments the existing
3 km polygon-bbox pull at docs/site_data/gbif/ with regional context (BSAU
genera reference, mammal expectations, bird hotlist).

Outputs land in docs/site_data/biodiversity_25km/:
- gbif_<class>.json — top-N species per class with counts
- inat_observations.json — raw iNat records inside the buffer
- species_combined.csv — flattened combined index
- summary.md — human-readable digest
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
OUT = ROOT / "docs" / "site_data" / "biodiversity_25km"
OUT.mkdir(parents=True, exist_ok=True)

CENTROID_LON, CENTROID_LAT = -57.0355, -25.6073
RADIUS_KM = 25.0
DEG_PER_KM_LAT = 1.0 / 111.0
DEG_PER_KM_LON = 1.0 / (111.0 * math.cos(math.radians(CENTROID_LAT)))
DLAT = RADIUS_KM * DEG_PER_KM_LAT
DLON = RADIUS_KM * DEG_PER_KM_LON
BBOX = (
    CENTROID_LON - DLON,  # W
    CENTROID_LAT - DLAT,  # S
    CENTROID_LON + DLON,  # E
    CENTROID_LAT + DLAT,  # N
)

GBIF_CLASS_KEYS = {
    "Aves": 212,
    "Mammalia": 359,
    "Magnoliopsida": 220,
    "Liliopsida": 196,
    "Reptilia": 358,
    "Amphibia": 131,
    "Insecta": 216,
}

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "lqv-phase0/1.0 (research; weissvanderpol.ivan@gmail.com)"})
_retry = Retry(
    total=6,
    backoff_factor=1.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET",),
    raise_on_status=False,
)
_adapter = HTTPAdapter(max_retries=_retry, pool_connections=4, pool_maxsize=4)
SESSION.mount("https://", _adapter)
SESSION.mount("http://", _adapter)


def _get(url: str, **kw):
    """Resilient GET: retries on transient socket drops on top of urllib3 retries."""
    last: Exception | None = None
    for attempt in range(4):
        try:
            return SESSION.get(url, timeout=kw.pop("timeout", 60), **kw)
        except requests.exceptions.RequestException as e:
            last = e
            time.sleep(2 ** attempt)
    raise last  # type: ignore[misc]


def gbif_species_facet(class_key: int, facet_limit: int = 150) -> list[dict]:
    """Return top species (by occurrence count) for a class within bbox."""
    params = {
        "classKey": class_key,
        "decimalLatitude": f"{BBOX[1]},{BBOX[3]}",
        "decimalLongitude": f"{BBOX[0]},{BBOX[2]}",
        "facet": "speciesKey",
        "facetLimit": facet_limit,
        "limit": 0,
        "hasCoordinate": "true",
        "hasGeospatialIssue": "false",
    }
    r = _get("https://api.gbif.org/v1/occurrence/search", params=params, timeout=60)
    r.raise_for_status()
    data = r.json()
    facets = data.get("facets", [])
    if not facets:
        return []
    return facets[0].get("counts", [])


def gbif_resolve_species(species_key: int) -> dict | None:
    r = _get(f"https://api.gbif.org/v1/species/{species_key}", timeout=30)
    if r.status_code != 200:
        return None
    return r.json()


def gbif_vernacular(species_key: int) -> str:
    r = _get(
        f"https://api.gbif.org/v1/species/{species_key}/vernacularNames",
        params={"limit": 50},
        timeout=30,
    )
    if r.status_code != 200:
        return ""
    results = r.json().get("results", [])
    # Prefer Spanish then English
    for lang in ("spa", "eng", "por"):
        for v in results:
            if (v.get("language") or "").lower() == lang and v.get("vernacularName"):
                return v["vernacularName"]
    if results:
        return results[0].get("vernacularName") or ""
    return ""


def pull_gbif_class(class_name: str, class_key: int, top_n: int) -> list[dict]:
    print(f"  GBIF {class_name} (top {top_n})…", flush=True)
    counts = gbif_species_facet(class_key, facet_limit=top_n)
    out = []
    for i, c in enumerate(counts[:top_n]):
        sk = int(c["name"])
        sp = gbif_resolve_species(sk)
        if not sp:
            continue
        vern = gbif_vernacular(sk)
        out.append(
            {
                "speciesKey": sk,
                "occurrenceCount": int(c["count"]),
                "canonicalName": sp.get("canonicalName") or sp.get("scientificName"),
                "scientificName": sp.get("scientificName"),
                "vernacularName": vern,
                "kingdom": sp.get("kingdom"),
                "phylum": sp.get("phylum"),
                "class": sp.get("class"),
                "order": sp.get("order"),
                "family": sp.get("family"),
                "genus": sp.get("genus"),
                "rank": sp.get("rank"),
                "iucnRedListCategory": sp.get("iucnRedListCategory"),
            }
        )
        if i % 25 == 0:
            time.sleep(0.1)
    return out


def pull_inat() -> list[dict]:
    print(f"  iNaturalist (25 km radius around {CENTROID_LON}, {CENTROID_LAT})…", flush=True)
    out: list[dict] = []
    page = 1
    while True:
        params = {
            "lat": CENTROID_LAT,
            "lng": CENTROID_LON,
            "radius": int(RADIUS_KM),
            "per_page": 200,
            "page": page,
            "quality_grade": "research",
            "order": "desc",
            "order_by": "observed_on",
        }
        r = _get("https://api.inaturalist.org/v1/observations", params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        if not results:
            break
        for o in results:
            taxon = o.get("taxon") or {}
            out.append(
                {
                    "id": o.get("id"),
                    "observed_on": o.get("observed_on"),
                    "place_guess": o.get("place_guess"),
                    "latitude": (o.get("geojson") or {}).get("coordinates", [None, None])[1],
                    "longitude": (o.get("geojson") or {}).get("coordinates", [None, None])[0],
                    "taxon_id": taxon.get("id"),
                    "scientific_name": taxon.get("name"),
                    "common_name": taxon.get("preferred_common_name"),
                    "rank": taxon.get("rank"),
                    "iconic_taxon": taxon.get("iconic_taxon_name"),
                }
            )
        if page * 200 >= data.get("total_results", 0):
            break
        page += 1
        if page > 25:  # cap at 5000 obs
            break
    return out


def main():
    print(f"BBOX W{BBOX[0]:.4f} S{BBOX[1]:.4f} E{BBOX[2]:.4f} N{BBOX[3]:.4f}")
    combined: list[dict] = []
    for class_name, class_key in GBIF_CLASS_KEYS.items():
        top_n = 100 if class_name in ("Aves", "Magnoliopsida", "Insecta") else 60
        species = pull_gbif_class(class_name, class_key, top_n)
        out_path = OUT / f"gbif_{class_name.lower()}.json"
        out_path.write_text(json.dumps(species, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"    → {len(species)} species → {out_path.name}", flush=True)
        for s in species:
            combined.append({"source": "GBIF", **s})

    inat = pull_inat()
    (OUT / "inat_observations.json").write_text(
        json.dumps(inat, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  iNat → {len(inat)} observations")

    # Combined CSV (GBIF species + iNat aggregated by scientific name)
    csv_path = OUT / "species_combined.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "source",
                "class",
                "order",
                "family",
                "genus",
                "scientificName",
                "vernacularName",
                "occurrenceCount",
                "iucnRedListCategory",
            ]
        )
        for s in combined:
            w.writerow(
                [
                    s.get("source"),
                    s.get("class"),
                    s.get("order"),
                    s.get("family"),
                    s.get("genus"),
                    s.get("canonicalName") or s.get("scientificName"),
                    s.get("vernacularName"),
                    s.get("occurrenceCount"),
                    s.get("iucnRedListCategory"),
                ]
            )
        # roll up iNat by species
        inat_agg: dict[str, dict] = {}
        for o in inat:
            sci = o.get("scientific_name")
            if not sci:
                continue
            k = (o.get("iconic_taxon") or "", sci)
            inat_agg.setdefault(
                sci,
                {
                    "class": o.get("iconic_taxon") or "",
                    "scientificName": sci,
                    "vernacularName": o.get("common_name") or "",
                    "count": 0,
                },
            )
            inat_agg[sci]["count"] += 1
        for a in sorted(inat_agg.values(), key=lambda x: -x["count"]):
            w.writerow(
                [
                    "iNat",
                    a["class"],
                    "",
                    "",
                    a["scientificName"].split(" ")[0],
                    a["scientificName"],
                    a["vernacularName"],
                    a["count"],
                    "",
                ]
            )
    print(f"  CSV → {csv_path}")

    # Summary md
    by_class: dict[str, int] = {}
    iucn_threat: list[dict] = []
    for s in combined:
        by_class[s.get("class") or "?"] = by_class.get(s.get("class") or "?", 0) + 1
        cat = (s.get("iucnRedListCategory") or "").upper()
        if cat in ("VU", "EN", "CR", "NT"):
            iucn_threat.append(s)
    md = ["# Biodiversity 25 km — GBIF + iNaturalist pull", ""]
    md.append(f"Centroid: `{CENTROID_LON}, {CENTROID_LAT}` — radius {RADIUS_KM} km")
    md.append(f"BBox: W{BBOX[0]:.4f} S{BBOX[1]:.4f} E{BBOX[2]:.4f} N{BBOX[3]:.4f}")
    md.append("")
    md.append("## GBIF species counts by class")
    md.append("")
    md.append("| Class | Species |")
    md.append("|---|---:|")
    for k, v in sorted(by_class.items(), key=lambda x: -x[1]):
        md.append(f"| {k} | {v} |")
    md.append("")
    md.append(f"## iNaturalist (research-grade) observations: {len(inat)}")
    md.append("")
    md.append(f"## IUCN-threatened species (NT/VU/EN/CR): {len(iucn_threat)}")
    if iucn_threat:
        md.append("")
        md.append("| Class | Family | Scientific | Vernacular | IUCN |")
        md.append("|---|---|---|---|---|")
        for s in sorted(iucn_threat, key=lambda s: (s.get("class"), s.get("family"))):
            md.append(
                f"| {s.get('class')} | {s.get('family')} | *{s.get('canonicalName')}* | {s.get('vernacularName')} | **{s.get('iucnRedListCategory')}** |"
            )
    (OUT / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("  summary.md written")
    print("Done.")


if __name__ == "__main__":
    sys.exit(main() or 0)
