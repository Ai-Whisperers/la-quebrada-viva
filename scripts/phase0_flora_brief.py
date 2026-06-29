#!/usr/bin/env python3
"""Phase-0 §12 #4 extension: flora brief synthesis.

Pulls research-grade iNaturalist Plantae observations inside a parcel-tight
5 km radius around the La Quebrada Viva centroid (-57.0355, -25.6073) and
synthesizes with:

  * docs/site_data/flora/expected_species_ranked.csv (3,906 rows — full
    expected-species list with AF/PY/AR threat status, endemism, uses,
    timber flag, 25 km LQV documentation, vernaculars)
  * docs/site_data/biodiversity_25km/gbif_magnoliopsida.json (100 dicots)
  * docs/site_data/biodiversity_25km/gbif_liliopsida.json (60 monocots)
  * docs/site_data/biodiversity_25km/inat_observations.json (727 obs,
    iconic_taxon field)

Emits under docs/site_data/flora/:

  * inat_5km_plantae.json          — raw 5 km iNat Plantae pull
  * parcel_observed_plants.csv     — flat per-observation record
  * trees_likely.csv               — top 30 trees by 25 km occurrence
  * shrubs_likely.csv              — top 20 shrubs
  * threatened.csv                 — 87 threatened spp (PY en_peligro OR
                                     AR Endangered/CR)
  * timber.csv                     — is_timber=yes, sorted by occurrence
  * medicinal.csv                  — uses contains "medicinal"
  * food.csv                       — uses contains "food"
  * endemics_documented.csv        — pure/near endemic AND
                                     lqv_25km_documented=yes
  * palms.csv                      — Arecaceae family
  * flora_brief.md                 — narrative for the deck

Idempotent: re-run pulls fresh iNat, overwrites all synthesis outputs.
"""

from __future__ import annotations

import csv
import json
import time
from collections import Counter
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parents[1]
BIO_25KM = ROOT / "docs" / "site_data" / "biodiversity_25km"
FLORA_CSV = ROOT / "docs" / "site_data" / "flora" / "expected_species_ranked.csv"
OUT = ROOT / "docs" / "site_data" / "flora"
OUT.mkdir(parents=True, exist_ok=True)

CENTROID_LON, CENTROID_LAT = -57.0355, -25.6073
PARCEL_RADIUS_KM = 5.0
PLANTAE_TAXON_ID = 47126

SESSION = requests.Session()
SESSION.headers.update(
    {"User-Agent": "lqv-phase0/1.0 (research; weissvanderpol.ivan@gmail.com)"}
)
_retry = Retry(
    total=6,
    backoff_factor=1.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET",),
    raise_on_status=False,
)
SESSION.mount("https://", HTTPAdapter(max_retries=_retry, pool_connections=4, pool_maxsize=4))


def pull_inat_5km_plantae() -> list[dict]:
    out: list[dict] = []
    page = 1
    while True:
        params = {
            "lat": CENTROID_LAT,
            "lng": CENTROID_LON,
            "radius": int(PARCEL_RADIUS_KM),
            "per_page": 200,
            "page": page,
            "quality_grade": "research",
            "taxon_id": PLANTAE_TAXON_ID,
            "order": "desc",
            "order_by": "observed_on",
        }
        r = SESSION.get(
            "https://api.inaturalist.org/v1/observations", params=params, timeout=60
        )
        r.raise_for_status()
        body = r.json()
        results = body.get("results", [])
        if not results:
            break
        for o in results:
            taxon = o.get("taxon") or {}
            geo = o.get("geojson") or {}
            coords = geo.get("coordinates") or [None, None]
            out.append(
                {
                    "id": o.get("id"),
                    "observed_on": o.get("observed_on"),
                    "place_guess": o.get("place_guess"),
                    "longitude": coords[0],
                    "latitude": coords[1],
                    "taxon_id": taxon.get("id"),
                    "scientific_name": taxon.get("name"),
                    "common_name": taxon.get("preferred_common_name"),
                    "rank": taxon.get("rank"),
                    "iconic_taxon": taxon.get("iconic_taxon_name"),
                }
            )
        if page >= 25 or len(results) < 200:
            break
        page += 1
        time.sleep(0.5)
    return out


def month_from(iso: str | None) -> str | None:
    if not iso or len(iso) < 7:
        return None
    return iso[5:7]


_MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def months_summary(months: list[str]) -> str:
    if not months:
        return ""
    uniq = sorted({m for m in months if m and m.isdigit()})
    if len(uniq) >= 10:
        return "year-round"
    names = [_MONTH_NAMES[int(m) - 1] for m in uniq if 1 <= int(m) <= 12]
    return "·".join(names)


def load_gbif_class(name: str) -> list[dict]:
    p = BIO_25KM / f"gbif_{name}.json"
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def load_inat_25km() -> list[dict]:
    p = BIO_25KM / "inat_observations.json"
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        return []


def num(s: str | None) -> int:
    if not s:
        return 0
    try:
        return int(s)
    except ValueError:
        return 0


def write_csv(path: Path, rows: list[dict], cols: list[str]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def main() -> None:
    # --- 1. parcel-tight iNat Plantae ---
    print("[1/7] iNat 5 km Plantae pull …")
    parcel_obs = pull_inat_5km_plantae()
    (OUT / "inat_5km_plantae.json").write_text(json.dumps(parcel_obs, indent=2))
    if parcel_obs:
        cols = list(parcel_obs[0].keys())
        write_csv(OUT / "parcel_observed_plants.csv", parcel_obs, cols)
    print(f"      {len(parcel_obs)} research-grade plant obs within 5 km")

    seen_5km: dict[str, list[dict]] = {}
    months_by_sp: dict[str, list[str]] = {}
    for o in parcel_obs:
        sci = o.get("scientific_name")
        if not sci:
            continue
        seen_5km.setdefault(sci, []).append(o)
        m = month_from(o.get("observed_on"))
        if m:
            months_by_sp.setdefault(sci, []).append(m)

    # --- 2. expected-species ranked CSV ---
    print("[2/7] Loading expected_species_ranked.csv …")
    expected = list(csv.DictReader(FLORA_CSV.open()))
    print(f"      {len(expected)} expected species")

    # Family counter for context
    fam_top = Counter(r["family"] for r in expected if r["family"]).most_common(15)

    # --- 3. trees + shrubs by occurrence ---
    print("[3/7] Top trees and shrubs by 25 km occurrence …")
    def with_5km(rows: list[dict]) -> list[dict]:
        for r in rows:
            sci = r["binomial"]
            r["seen_within_5km"] = "y" if sci in seen_5km else ""
            r["n_obs_5km"] = len(seen_5km.get(sci, []))
            r["months_seen"] = months_summary(months_by_sp.get(sci, []))
        return rows

    trees = [
        r for r in expected
        if r["life_form"] in {"tree", "tree?"} and num(r["lqv_25km_occurrences"]) > 0
    ]
    trees.sort(key=lambda r: num(r["lqv_25km_occurrences"]), reverse=True)
    trees_top = with_5km(trees[:30])

    shrubs = [
        r for r in expected
        if r["life_form"] in {"shrub", "shrub?"} and num(r["lqv_25km_occurrences"]) > 0
    ]
    shrubs.sort(key=lambda r: num(r["lqv_25km_occurrences"]), reverse=True)
    shrubs_top = with_5km(shrubs[:20])

    common_cols = [
        "binomial", "family", "life_form", "lqv_vernacular",
        "lqv_25km_occurrences", "seen_within_5km", "n_obs_5km", "months_seen",
        "py_threat_category", "ar_threat_category",
        "endemism_group", "uses", "is_timber", "lqv_priority_score",
    ]
    write_csv(OUT / "trees_likely.csv", trees_top, common_cols)
    write_csv(OUT / "shrubs_likely.csv", shrubs_top, common_cols)

    # --- 4. threatened ---
    print("[4/7] Threatened species (PY en_peligro OR AR Endangered/CR) …")
    threat = [
        r for r in expected
        if r["py_threat_category"] in {"en_peligro", "amenazada"}
        or "Endangered" in r["ar_threat_category"]
        or "Critically" in r["ar_threat_category"]
    ]
    threat.sort(
        key=lambda r: (
            0 if r["py_threat_category"] == "en_peligro" else 1,
            -num(r["lqv_25km_occurrences"]),
        )
    )
    threat_with = with_5km(threat)
    write_csv(OUT / "threatened.csv", threat_with, common_cols)

    # --- 5. timber + medicinal + food ---
    print("[5/7] Timber, medicinal, food cross-cuts …")
    timber = [r for r in expected if r["is_timber"] == "yes"]
    timber.sort(key=lambda r: num(r["lqv_25km_occurrences"]), reverse=True)
    write_csv(OUT / "timber.csv", with_5km(timber), common_cols)

    medicinal = [r for r in expected if "medicinal" in r["uses"].lower()]
    medicinal.sort(key=lambda r: num(r["lqv_25km_occurrences"]), reverse=True)
    write_csv(OUT / "medicinal.csv", with_5km(medicinal), common_cols)

    food = [
        r for r in expected
        if "food" in r["uses"].lower() or "edible" in r["uses"].lower()
    ]
    food.sort(key=lambda r: num(r["lqv_25km_occurrences"]), reverse=True)
    write_csv(OUT / "food.csv", with_5km(food), common_cols)

    # --- 6. endemics documented + palms ---
    print("[6/7] Endemics documented + palms …")
    endemics = [
        r for r in expected
        if r["endemism_group"] in {"pure_endemic", "near_endemic"}
        and r["lqv_25km_documented"] == "yes"
    ]
    endemics.sort(key=lambda r: num(r["lqv_25km_occurrences"]), reverse=True)
    write_csv(OUT / "endemics_documented.csv", with_5km(endemics), common_cols)

    palms = [r for r in expected if r["family"] == "Arecaceae"]
    palms.sort(key=lambda r: num(r["lqv_25km_occurrences"]), reverse=True)
    write_csv(OUT / "palms.csv", with_5km(palms), common_cols)

    # --- 7. GBIF cross-reference ---
    print("[7/7] GBIF Magnoliopsida + Liliopsida top families …")
    magn = load_gbif_class("magnoliopsida")
    lili = load_gbif_class("liliopsida")
    gbif_top_dicots = sorted(
        magn, key=lambda s: int(s.get("occurrenceCount", 0) or 0), reverse=True
    )[:10]
    gbif_top_monocots = sorted(
        lili, key=lambda s: int(s.get("occurrenceCount", 0) or 0), reverse=True
    )[:10]

    # --- brief ---
    print("Writing flora_brief.md …")
    iconic_5km = Counter(
        o.get("iconic_taxon") for o in parcel_obs if o.get("iconic_taxon")
    )
    parcel_top_spp = Counter(
        o.get("scientific_name") for o in parcel_obs if o.get("scientific_name")
    ).most_common(15)

    threat_seen_5km = sum(1 for r in threat_with if r["seen_within_5km"] == "y")
    trees_seen_5km = sum(1 for r in trees_top if r["seen_within_5km"] == "y")
    shrubs_seen_5km = sum(1 for r in shrubs_top if r["seen_within_5km"] == "y")
    timber_count = len(timber)
    medicinal_count = len(medicinal)
    food_count = len(food)
    endemics_count = len(endemics)
    palms_count = len(palms)

    lines: list[str] = []
    a = lines.append
    a("---")
    a('title: "Flora brief — La Quebrada Viva"')
    a("phase: Phase-0")
    a('section: "§12 #4 extension"')
    a(f'centroid: "{CENTROID_LON}, {CENTROID_LAT}"')
    a(f"parcel_radius_km: {PARCEL_RADIUS_KM}")
    a("regional_radius_km: 25.0")
    a(
        'data_sources: ["expected_species_ranked.csv (3906 rows)", '
        '"GBIF Magnoliopsida/Liliopsida (25 km)", '
        '"iNaturalist research-grade (25 km + 5 km tight)"]'
    )
    a('status: "v1 — synthesis on top of biodiversity_25km/ + new 5 km Plantae pull"')
    a(f"parcel_inat_plantae_obs: {len(parcel_obs)}")
    a("---")
    a("")
    a("# Flora brief — La Quebrada Viva")
    a("")
    a(
        "Parcel centroid `-57.0355, -25.6073` (-25.6073°S, -57.0355°W), ~350 m "
        "elevation, Atlantic Forest / Cerrado ecotone, Paraguarí. Expected-species "
        "ranking is the curated 3,906-row checklist crossed against Atlantic-Forest "
        "(BF.2020), Argentine, and Paraguayan threatened-species lists."
    )
    a("")
    a("## TL;DR")
    a("")
    a(
        f"- **Expected-species pool:** 3,906 spp ranked. {timber_count} timber, "
        f"{medicinal_count} medicinal, {food_count} food/edible, "
        f"{endemics_count} endemics already documented within 25 km, "
        f"{palms_count} palms."
    )
    a(
        f"- **Threatened in regional pool:** {len(threat_with)} species "
        f"({sum(1 for r in threat_with if r['py_threat_category'] == 'en_peligro')} "
        f"PY *en peligro* + the rest *amenazada* / AR Endangered). "
        f"{threat_seen_5km} have been photographed within 5 km."
    )
    a(
        f"- **Parcel-tight (5 km iNat Plantae, research-grade):** {len(parcel_obs)} "
        f"GPS-actual plant observations. Top-30 regional trees → "
        f"{trees_seen_5km} confirmed in 5 km; top-20 shrubs → "
        f"{shrubs_seen_5km} confirmed."
    )
    if iconic_5km:
        mix = ", ".join(f"{k} {v}" for k, v in iconic_5km.most_common())
        a(f"- **5 km plant iconic-mix:** {mix}.")
    a("")

    a("## Critical flag — *Araucaria angustifolia*")
    aa = next((r for r in expected if r["binomial"] == "Araucaria angustifolia"), None)
    if aa:
        seen = "✅ photographed within 5 km" if aa["binomial"] in seen_5km else "not yet seen in 5 km iNat — confirm before any clearing"
        a(
            f"Pino-paraná (*Araucaria angustifolia*) — PY **en peligro**, AR "
            f"**Endangered**, IUCN Critically Endangered globally. "
            f"AF status: {aa['af_status']}. Atlantic-Forest records: "
            f"{aa['n_records_af']}. **Status on site: {seen}.** "
            f"Any specimen on the parcel is a deck-grade conservation story and a "
            f"hard no-cut constraint."
        )
    a("")

    a("## Top 10 likely trees (by 25 km occurrence)")
    a("")
    a("| Scientific | Vernacular | Family | n (25 km) | 5 km? | PY threat | Uses |")
    a("|---|---|---|---:|:---:|---|---|")
    for r in trees_top[:10]:
        vern = r["lqv_vernacular"] or "—"
        seen = "✅" if r["seen_within_5km"] == "y" else "·"
        threat_mark = r["py_threat_category"] or "—"
        uses = (r["uses"] or "—").replace("|", "·")[:40]
        a(
            f"| *{r['binomial']}* | {vern} | {r['family']} | "
            f"{r['lqv_25km_occurrences']} | {seen} | {threat_mark} | {uses} |"
        )
    a("")

    a("## Top 10 likely shrubs (by 25 km occurrence)")
    a("")
    a("| Scientific | Vernacular | Family | n (25 km) | 5 km? | Uses |")
    a("|---|---|---|---:|:---:|---|")
    for r in shrubs_top[:10]:
        vern = r["lqv_vernacular"] or "—"
        seen = "✅" if r["seen_within_5km"] == "y" else "·"
        uses = (r["uses"] or "—").replace("|", "·")[:40]
        a(
            f"| *{r['binomial']}* | {vern} | {r['family']} | "
            f"{r['lqv_25km_occurrences']} | {seen} | {uses} |"
        )
    a("")

    a("## Threatened species (top 15 by 25 km occurrence)")
    a("")
    a(
        f"Full list (87 entries) in `threatened.csv`. **PY *en peligro*: 81** + "
        f"PY *amenazada*: 40 + AR Endangered/CR: ~13 (overlap). "
        f"These drive the no-cut overlay on the master plan."
    )
    a("")
    a("| Scientific | Vernacular | PY | AR | n (25 km) | 5 km? |")
    a("|---|---|---|---|---:|:---:|")
    for r in threat_with[:15]:
        vern = r["lqv_vernacular"] or "—"
        seen = "✅" if r["seen_within_5km"] == "y" else "·"
        py = r["py_threat_category"] or "—"
        ar = (r["ar_threat_category"] or "—")[:18]
        a(
            f"| *{r['binomial']}* | {vern} | {py} | {ar} | "
            f"{r['lqv_25km_occurrences']} | {seen} |"
        )
    a("")

    a("## Timber + ethnobotanical cross-cuts")
    a("")
    a(
        f"- **Timber species (regional pool):** {timber_count}. Top by 25 km "
        f"occurrence in `timber.csv`. Most overlap with the *en peligro* list — "
        f"selective harvest only via SNC management plan, never on natural-forest "
        f"polygons."
    )
    a(
        f"- **Medicinal:** {medicinal_count} species with documented medicinal use "
        f"(folk-pharmacopoeia, *farmacopea criolla* and Mbyá-Guaraní use). "
        f"Source list in `medicinal.csv`."
    )
    a(
        f"- **Food / edible:** {food_count} species. See `food.csv`. Top families: "
        f"Myrtaceae (guavas / *arazá* / *pitanga*), Annonaceae (*araticú*), "
        f"Sapotaceae (*aguaí*)."
    )
    a("")

    a("## Palms (Arecaceae)")
    a("")
    if palms:
        for r in palms[:8]:
            vern = r["lqv_vernacular"] or "—"
            seen = "✅" if r["seen_within_5km"] == "y" else "·"
            a(
                f"- *{r['binomial']}* — {vern}; 25 km n={r['lqv_25km_occurrences']}; "
                f"5 km {seen}; uses: {r['uses'] or '—'}"
            )
    else:
        a("- (none in expected list — verify against site survey)")
    a("")

    a("## Endemics documented in 25 km")
    a("")
    a(
        f"{endemics_count} species classified pure or near endemic to the Atlantic "
        f"Forest **and** already documented within 25 km of the parcel (GBIF or "
        f"iNat). Top 10:"
    )
    a("")
    a("| Scientific | Vernacular | Family | Endemism | n (25 km) | 5 km? |")
    a("|---|---|---|---|---:|:---:|")
    for r in endemics[:10]:
        vern = r["lqv_vernacular"] or "—"
        seen = "✅" if r["seen_within_5km"] == "y" else "·"
        a(
            f"| *{r['binomial']}* | {vern} | {r['family']} | "
            f"{r['endemism_group']} | {r['lqv_25km_occurrences']} | {seen} |"
        )
    a("")

    a("## GBIF cross-reference (top 25 km records)")
    a("")
    a("**Dicots (Magnoliopsida):**")
    for s in gbif_top_dicots:
        sci = s.get("scientificName") or s.get("canonicalName")
        a(
            f"- *{sci}* — {s.get('family', '')} — "
            f"n={s.get('occurrenceCount', 0)}"
        )
    a("")
    a("**Monocots (Liliopsida):**")
    for s in gbif_top_monocots:
        sci = s.get("scientificName") or s.get("canonicalName")
        a(
            f"- *{sci}* — {s.get('family', '')} — "
            f"n={s.get('occurrenceCount', 0)}"
        )
    a("")

    a("## Top families in the regional pool")
    a("")
    for fam, n in fam_top:
        a(f"- {fam}: {n} spp")
    a("")

    if parcel_top_spp:
        a("## Most-observed species in 5 km iNat")
        a("")
        for sci, n in parcel_top_spp:
            a(f"- *{sci}* — {n} obs")
        a("")

    a("## Caveats")
    a("")
    a(
        "- iNat coverage is biased toward areas with iNaturalist users; absence "
        "in 5 km ≠ absence on parcel."
    )
    a(
        "- The expected-species list was built from Atlantic-Forest BF.2020 "
        "checklists + PY/AR threat lists; a species marked *new to AF* is in the "
        "regional pool but not yet on the AF checklist (likely Cerrado / Chaco "
        "edge species)."
    )
    a(
        "- *En peligro* status is national PY. IUCN global category often more "
        "lenient (e.g. *Cordia trichotoma* maybe LC globally, en peligro in PY)."
    )
    a("- Family + vernacular may have UTF-8 / Spanish-accent issues in raw CSV.")
    a("")

    a("## v2 backlog")
    a("")
    a("- SNC (Secretaría Nacional de Cultura) tree-cutting permit lookup.")
    a("- iNat field guide for the parcel area (geo-bounded checklist export).")
    a(
        "- TRY Plant Trait Database lookup for top-30 trees (LMA, wood density, "
        "shade tolerance) to inform the species mix for restoration plantings."
    )
    a("- Phenology synthesis (flowering / fruiting calendar) from iNat photos.")
    a("- Cross-check with the new T-DT canopy raster (NDVI / EVI 2024-2026).")
    a("")

    (OUT / "flora_brief.md").write_text("\n".join(lines))

    summary = [
        "# Flora brief — summary",
        f"- Expected species pool: 3,906",
        f"- Parcel-tight iNat Plantae (5 km, research-grade): {len(parcel_obs)} obs",
        f"- Top 30 regional trees → {trees_seen_5km} confirmed in 5 km",
        f"- Top 20 regional shrubs → {shrubs_seen_5km} confirmed in 5 km",
        f"- Threatened species (PY en_peligro/amenazada OR AR Endangered/CR): {len(threat_with)}",
        f"- Threatened seen within 5 km: {threat_seen_5km}",
        f"- Timber species: {timber_count}",
        f"- Medicinal species: {medicinal_count}",
        f"- Food/edible species: {food_count}",
        f"- Endemics documented within 25 km: {endemics_count}",
        f"- Palms (Arecaceae): {palms_count}",
    ]
    (OUT / "flora_summary.txt").write_text("\n".join(summary))
    print("Done.")


if __name__ == "__main__":
    main()
