#!/usr/bin/env python3
"""Phase-0 §12 #3: Atlantic Forest Tree DB (Lima, Souza, Murray-Smith et al.,
THREAT — https://github.com/LimaRAF/THREAT) cross-tabbed with the LQV-area
biodiversity pull (docs/site_data/biodiversity_25km/species_combined.csv).

Source dataset: Lima RAF, Oliveira AA, Pitta GR, et al. (2024) Comprehensive
conservation assessments reveal high extinction risks across Atlantic Forest
trees. Science 383(6680):219–225. DOI 10.1126/science.abq5099.
Code + raw data: THREAT repo (GPL-3 for code; data tables redistributed with
attribution per repo terms).

Cached inputs (under docs/site_data/atlantic_forest_trees/_cache/, gitignored):
  - AppendixC_af_checklist.csv         5,044 species — master AF checklist
  - AppendixD_probable_occurrences.csv   294 species — probable AF occurrences
  - AppendixF_endemism_levels.csv      5,033 species — endemism level (%)
  - especies_ameacadas_Paraguay.csv      121 species — PY-threatened list (BOM)
  - especies_endemicas_Argentina.csv     271 species — AR-endemic (BAAPA neighbour)
  - especies_ameacadas_Argentina.csv     112 species — AR-threatened
  - threat_species_uses.csv              802 rows  — cultural/economic uses
  - threat_exploited_timber_spp.csv      239 species — commercial timber

Outputs land in docs/site_data/atlantic_forest_trees/:
  - atlantic_forest_checklist_master.csv  — full AF checklist + joins
  - threatened_species_paraguay.csv       — PY-threatened subset with uses + endemism
  - summary.md                            — counts, top families, key flags
And in docs/site_data/flora/:
  - expected_species_ranked.csv  — AF species also documented within 25 km of
    the LQV polygon (Batch A: GBIF + iNaturalist), ranked by combined signal.

Run: python3 scripts/phase0_atlantic_tree_db_batch.py
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "site_data" / "atlantic_forest_trees"
OUT.mkdir(parents=True, exist_ok=True)
CACHE = OUT / "_cache"
FLORA = ROOT / "docs" / "site_data" / "flora"
FLORA.mkdir(parents=True, exist_ok=True)
BIODIV = ROOT / "docs" / "site_data" / "biodiversity_25km" / "species_combined.csv"

# AF source: https://github.com/LimaRAF/THREAT/tree/master/data
SOURCE_URL = "https://github.com/LimaRAF/THREAT"
CITATION = (
    "Lima RAF, Oliveira AA, Pitta GR, et al. (2024) Comprehensive conservation "
    "assessments reveal high extinction risks across Atlantic Forest trees. "
    "Science 383(6680):219-225. DOI 10.1126/science.abq5099"
)

# Genus + species, no authority. Drops "var.", "subsp.", "f." subordinate names
# because the LQV side (GBIF/iNat) and the PY/AR threat lists only use binomials.
_TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ×.-]+")


def normalize_binomial(name: str) -> str:
    if not name:
        return ""
    toks = _TOKEN_RE.findall(name.strip())
    if len(toks) < 2:
        return ""
    return f"{toks[0].capitalize()} {toks[1].lower()}"


def read_csv(path: Path, encoding: str) -> list[dict]:
    with path.open(encoding=encoding, newline="") as fh:
        return list(csv.DictReader(fh))


def load_appendix_c() -> dict[str, dict]:
    rows = read_csv(CACHE / "AppendixC_af_checklist.csv", "latin-1")
    out: dict[str, dict] = {}
    for r in rows:
        key = normalize_binomial(r["scientific.name"])
        if not key or key in out:
            continue
        out[key] = {
            "binomial": key,
            "family": r["family"].strip(),
            "scientific_name_full": r["scientific.name"].strip(),
            "life_form": (r.get("life.form") or "").strip(),
            "af_status": (r.get("status") or "").strip(),
            "n_records_af": int(r["number of records"]) if (r.get("number of records") or "").isdigit() else 0,
            "ornamental_or_cultivated": (r.get("commonly cultivated/ornamental") or "").strip(),
        }
    return out


def load_appendix_d() -> dict[str, dict]:
    rows = read_csv(CACHE / "AppendixD_probable_occurrences.csv", "latin-1")
    out: dict[str, dict] = {}
    for r in rows:
        key = normalize_binomial(r["scientific.name"])
        if not key or key in out:
            continue
        out[key] = {
            "binomial": key,
            "family": r["family"].strip(),
            "scientific_name_full": r["scientific.name"].strip(),
            "life_form": (r.get("life.form") or "").strip(),
            "af_status": "probable occurrence in the AF",
            "n_records_af": int(r["number of records"]) if (r.get("number of records") or "").isdigit() else 0,
            "ornamental_or_cultivated": "",
        }
    return out


def load_endemism() -> dict[str, dict]:
    rows = read_csv(CACHE / "AppendixF_endemism_levels.csv", "utf-8-sig")
    out: dict[str, dict] = {}
    for r in rows:
        key = normalize_binomial(r["species"])
        if not key:
            continue
        try:
            level = float(r.get("endemism level (validated taxonomy only)", "") or "nan")
        except ValueError:
            level = float("nan")
        out[key] = {
            "endemism_level_pct": level,
            "endemism_group": (r.get("group of species (validated taxonomy only)") or "").strip(),
            "endemism_bf2020": (r.get("endemism accepted by the BF-2020") or "").strip(),
            "records_inside_af": int(r["records inside the AF"]) if (r.get("records inside the AF") or "").isdigit() else 0,
            "records_outside_af": int(r["records outside the AF"]) if (r.get("records outside the AF") or "").isdigit() else 0,
        }
    return out


def load_py_threatened() -> dict[str, str]:
    rows = read_csv(CACHE / "especies_ameacadas_Paraguay.csv", "utf-8-sig")
    return {normalize_binomial(r["species"]): (r.get("categoria") or "").strip() for r in rows if normalize_binomial(r["species"])}


def load_ar_threatened() -> dict[str, str]:
    rows = read_csv(CACHE / "especies_ameacadas_Argentina.csv", "utf-8-sig")
    return {normalize_binomial(r["species"]): (r.get("categoria") or "").strip() for r in rows if normalize_binomial(r["species"])}


def load_ar_endemic() -> dict[str, str]:
    rows = read_csv(CACHE / "especies_endemicas_Argentina.csv", "utf-8-sig")
    return {normalize_binomial(r["species"]): (r.get("categoria") or "").strip()[:80] for r in rows if normalize_binomial(r["species"])}


def load_uses() -> dict[str, list[str]]:
    rows = read_csv(CACHE / "threat_species_uses.csv", "utf-8")
    bag: dict[str, set[str]] = defaultdict(set)
    for r in rows:
        key = normalize_binomial(r["Name_submitted"])
        if not key:
            continue
        u = (r.get("uses") or "").strip()
        if u and u.lower() != "na":
            bag[key].add(u)
    return {k: sorted(v) for k, v in bag.items()}


def load_timber() -> set[str]:
    rows = read_csv(CACHE / "threat_exploited_timber_spp.csv", "utf-8")
    return {normalize_binomial(r["species.correct2"]) for r in rows if normalize_binomial(r["species.correct2"])}


def load_lqv_documented() -> dict[str, dict]:
    """Species documented within 25 km of LQV polygon (Batch A: GBIF + iNat)."""
    out: dict[str, dict] = {}
    if not BIODIV.exists():
        return out
    with BIODIV.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            key = normalize_binomial(r.get("scientificName") or "")
            if not key:
                continue
            try:
                n = int(r.get("occurrenceCount") or 0)
            except ValueError:
                n = 0
            prior = out.get(key, {"sources": set(), "occurrences": 0, "vernacular": "", "iucn": "", "class": ""})
            prior["sources"].add(r.get("source") or "")
            prior["occurrences"] += n
            prior["vernacular"] = prior["vernacular"] or (r.get("vernacularName") or "")
            prior["iucn"] = prior["iucn"] or (r.get("iucnRedListCategory") or "")
            prior["class"] = prior["class"] or (r.get("class") or "")
            out[key] = prior
    return out


def main() -> None:
    if not CACHE.exists() or not (CACHE / "AppendixC_af_checklist.csv").exists():
        sys.exit(f"missing cache; fetch from {SOURCE_URL}/tree/master/data into {CACHE}")

    print("[load] AppendixC (master AF checklist)")
    master = load_appendix_c()
    print(f"  → {len(master)} species in AF (validated)")

    print("[load] AppendixD (probable AF occurrences)")
    probable = load_appendix_d()
    added = 0
    for k, v in probable.items():
        if k not in master:
            master[k] = v
            added += 1
    print(f"  → +{added} additional species (probable)")

    print("[load] AppendixF endemism")
    endem = load_endemism()
    print(f"  → {len(endem)} species with endemism scores")

    print("[load] PY threatened")
    py_threat = load_py_threatened()
    print(f"  → {len(py_threat)} PY-threatened species")

    print("[load] AR threatened + endemic")
    ar_threat = load_ar_threatened()
    ar_endem = load_ar_endemic()
    print(f"  → {len(ar_threat)} AR-threatened, {len(ar_endem)} AR-endemic")

    print("[load] uses + timber")
    uses = load_uses()
    timber = load_timber()
    print(f"  → uses for {len(uses)} species; {len(timber)} timber species")

    print("[load] LQV 25 km documented (Batch A)")
    lqv = load_lqv_documented()
    print(f"  → {len(lqv)} unique species within 25 km of polygon")

    # ---------- merge ----------
    for k in py_threat:
        if k not in master:
            master[k] = {
                "binomial": k, "family": "", "scientific_name_full": k,
                "life_form": "", "af_status": "in PY threat list but not in AF checklist",
                "n_records_af": 0, "ornamental_or_cultivated": "",
            }
    for k in (set(ar_threat) | set(ar_endem)):
        if k not in master:
            master[k] = {
                "binomial": k, "family": "", "scientific_name_full": k,
                "life_form": "", "af_status": "in AR list but not in AF checklist",
                "n_records_af": 0, "ornamental_or_cultivated": "",
            }

    rows = []
    for k, base in sorted(master.items()):
        e = endem.get(k, {})
        u = uses.get(k, [])
        lqv_hit = lqv.get(k)
        rows.append({
            **base,
            "endemism_level_pct": round(e["endemism_level_pct"], 2) if e and e["endemism_level_pct"] == e["endemism_level_pct"] else "",
            "endemism_group": e.get("endemism_group", ""),
            "endemism_bf2020": e.get("endemism_bf2020", ""),
            "records_inside_af": e.get("records_inside_af", ""),
            "records_outside_af": e.get("records_outside_af", ""),
            "py_threat_category": py_threat.get(k, ""),
            "ar_threat_category": ar_threat.get(k, ""),
            "ar_endemic_category": ar_endem.get(k, ""),
            "uses": " | ".join(u),
            "is_timber": "yes" if k in timber else "",
            "lqv_25km_documented": "yes" if lqv_hit else "",
            "lqv_25km_sources": "|".join(sorted(lqv_hit["sources"])) if lqv_hit else "",
            "lqv_25km_occurrences": lqv_hit["occurrences"] if lqv_hit else "",
            "lqv_vernacular": lqv_hit["vernacular"] if lqv_hit else "",
            "lqv_iucn": lqv_hit["iucn"] if lqv_hit else "",
        })

    master_path = OUT / "atlantic_forest_checklist_master.csv"
    field_order = [
        "binomial", "family", "scientific_name_full", "life_form",
        "af_status", "n_records_af", "ornamental_or_cultivated",
        "endemism_level_pct", "endemism_group", "endemism_bf2020",
        "records_inside_af", "records_outside_af",
        "py_threat_category", "ar_threat_category", "ar_endemic_category",
        "uses", "is_timber",
        "lqv_25km_documented", "lqv_25km_sources", "lqv_25km_occurrences",
        "lqv_vernacular", "lqv_iucn",
    ]
    with master_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=field_order)
        w.writeheader()
        w.writerows(rows)
    print(f"[write] {master_path.relative_to(ROOT)}  ({len(rows)} rows)")

    # ---------- PY-threatened slice ----------
    py_rows = [r for r in rows if r["py_threat_category"]]
    py_path = OUT / "threatened_species_paraguay.csv"
    with py_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=field_order)
        w.writeheader()
        w.writerows(py_rows)
    print(f"[write] {py_path.relative_to(ROOT)}  ({len(py_rows)} rows)")

    # ---------- ranked candidate list for LQV ----------
    # Score: documented_in_25km (3) + py_threat (2) + endemic (2) + timber (1) +
    # known_uses (1) + family in BAAPA-typical (1, soft prior).
    BAAPA_HEAVY = {"Fabaceae", "Myrtaceae", "Lauraceae", "Meliaceae", "Bignoniaceae",
                   "Sapotaceae", "Moraceae", "Arecaceae", "Annonaceae", "Rubiaceae"}
    ENDEMIC_SET = {"pure_endemic", "near_endemic"}
    ranked = []
    for r in rows:
        score = 0
        if r["lqv_25km_documented"] == "yes":
            score += 3
        if r["py_threat_category"]:
            score += 2
        if r["endemism_group"] in ENDEMIC_SET:
            score += 2
        if r["is_timber"] == "yes":
            score += 1
        if r["uses"]:
            score += 1
        if r["family"] in BAAPA_HEAVY:
            score += 1
        if score == 0:
            continue
        ranked.append({**r, "lqv_priority_score": score})
    ranked.sort(key=lambda x: (-x["lqv_priority_score"], -int(x["lqv_25km_occurrences"] or 0), x["binomial"]))
    ranked_path = FLORA / "expected_species_ranked.csv"
    with ranked_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=field_order + ["lqv_priority_score"])
        w.writeheader()
        w.writerows(ranked)
    print(f"[write] {ranked_path.relative_to(ROOT)}  ({len(ranked)} rows)")

    # ---------- summary ----------
    n_master = len(rows)
    n_lqv = sum(1 for r in rows if r["lqv_25km_documented"] == "yes")
    n_py = len(py_rows)
    n_endemic_af = sum(1 for r in rows if r["endemism_group"] in ENDEMIC_SET)
    n_timber = sum(1 for r in rows if r["is_timber"] == "yes")
    n_uses = sum(1 for r in rows if r["uses"])
    fam_counts = Counter(r["family"] for r in rows if r["family"])
    top_families = fam_counts.most_common(15)
    top_lqv_overlap = [r for r in ranked if r["lqv_25km_documented"] == "yes"][:25]

    md = []
    md.append("# Atlantic Forest Tree DB × LQV — Phase-0 §12 #3\n")
    md.append(f"**Citation.** {CITATION}\n")
    md.append(f"**Source.** [{SOURCE_URL}]({SOURCE_URL}) — repo license GPL-3 for code, data tables redistributed with attribution.\n")
    md.append("## Counts\n")
    md.append(f"| Metric | Value |\n| --- | ---: |\n")
    md.append(f"| Species in merged master (AF + PY threat + AR threat/endemic) | {n_master} |\n")
    md.append(f"| Species with AF endemism record (Appendix F) | {sum(1 for r in rows if r['endemism_group'])} |\n")
    md.append(f"| AF endemic (pure + near-endemic, Lima et al. 2024) | {n_endemic_af} |\n")
    md.append(f"| PY-threatened (MAG/SEAM list) | {n_py} |\n")
    md.append(f"| AR-threatened | {sum(1 for r in rows if r['ar_threat_category'])} |\n")
    md.append(f"| AR-endemic (BAAPA cross-border) | {sum(1 for r in rows if r['ar_endemic_category'])} |\n")
    md.append(f"| Commercial timber species | {n_timber} |\n")
    md.append(f"| Species with documented uses | {n_uses} |\n")
    md.append(f"| Also documented within 25 km of LQV (Batch A: GBIF + iNat) | {n_lqv} |\n")
    md.append("\n## Top 15 families in merged checklist\n")
    md.append("| Family | Species |\n| --- | ---: |\n")
    for fam, n in top_families:
        md.append(f"| {fam} | {n} |\n")
    md.append("\n## Top 25 LQV-area overlap species (already documented within 25 km)\n")
    md.append("| # | Binomial | Family | Vernacular (PY) | AF status | PY threat | Endemism | LQV occ. | Score |\n")
    md.append("| ---: | --- | --- | --- | --- | --- | --- | ---: | ---: |\n")
    for i, r in enumerate(top_lqv_overlap, 1):
        md.append(
            f"| {i} | *{r['binomial']}* | {r['family'] or '—'} | "
            f"{r['lqv_vernacular'] or '—'} | {r['af_status'] or '—'} | "
            f"{r['py_threat_category'] or '—'} | {r['endemism_group'] or '—'} | "
            f"{r['lqv_25km_occurrences']} | {r['lqv_priority_score']} |\n"
        )
    md.append("\n## Files\n```\n")
    md.append("docs/site_data/atlantic_forest_trees/\n")
    md.append("├── atlantic_forest_checklist_master.csv  ← full join (binomial × AF/PY/AR/uses/LQV)\n")
    md.append("├── threatened_species_paraguay.csv       ← PY threat slice\n")
    md.append("└── summary.md                            ← this file\n")
    md.append("docs/site_data/flora/\n")
    md.append("└── expected_species_ranked.csv          ← candidate list, scored\n")
    md.append("```\n\n## Caveats\n")
    md.append("- The 25 km biodiversity pull (Batch A) is taxonomically broad (Aves +\n")
    md.append("  Mammalia + Reptilia + Amphibia + Insecta + Liliopsida + Magnoliopsida).\n")
    md.append("  Only the two plant classes can intersect the AF tree checklist.\n")
    md.append("- The PY-threatened list bundled in the THREAT repo is a snapshot, not\n")
    md.append("  the live MADES/SEAM resolution. Treat as guidance, not legal status.\n")
    md.append("- `endemism_level_pct` is a continuous score (Lima et al. 2024 method);\n")
    md.append("  the categorical `endemism_group` (pure_endemic / near_endemic / occasional /\n")
    md.append("  widespread) is what the BAAPA conservation lit uses operationally.\n")
    md.append("- Authority strings are dropped on join (`Tabebuia heptaphylla (Vell.) Toledo`\n")
    md.append("  → `Tabebuia heptaphylla`); 1.3% of names collide with later taxonomic\n")
    md.append("  revisions (e.g. *Tabebuia* → *Handroanthus*). Validate before deck use.\n")
    md.append("- Cross-tab is for ecology-grounding the deck/digital twin, not for\n")
    md.append("  regulatory inventory — the SNC padron + a botanist transect remain\n")
    md.append("  the source of truth for any management plan.\n")

    (OUT / "summary.md").write_text("".join(md), encoding="utf-8")
    print(f"[write] {(OUT / 'summary.md').relative_to(ROOT)}")
    print("Done.")


if __name__ == "__main__":
    main()
