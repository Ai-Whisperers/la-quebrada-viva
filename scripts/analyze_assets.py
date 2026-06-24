"""Asset inventory + integration-target classifier.

Walks ``assets/{hdris,models,textures,terrain,references}/`` and emits two
artifacts under ``docs/``:

  * ``docs/ASSETS_INVENTORY.csv`` — one row per asset id with columns:
        id, type, source, license, size_mb, files, resolution_hint,
        integration_target, lqv_use_score, notes

  * ``docs/ASSETS_INTEGRATION_PLAN.md`` — human-readable rollup grouped by
        integration target (typology, amenity, flora, terrain, material,
        lighting) with a ranked top-15 for first-wave integration.

Run from project root::

    python3 scripts/analyze_assets.py

Polygon counts are NOT computed here (would require ``blender -b`` per file).
Resolution comes from filename + on-disk size. License is inferred from source:
Poly Haven & ambientCG = CC0; for any other source put a stub at
``LICENSES/<id>.txt`` containing ``License: <name>`` and this script will read it.
"""
from __future__ import annotations

import csv
import os
import re
import sys
from collections import defaultdict
from typing import Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(PROJECT_ROOT, "assets")
LICENSES = os.path.join(PROJECT_ROOT, "LICENSES")
DOCS = os.path.join(PROJECT_ROOT, "docs")

CSV_OUT = os.path.join(DOCS, "ASSETS_INVENTORY.csv")
MD_OUT = os.path.join(DOCS, "ASSETS_INTEGRATION_PLAN.md")


# ---------------------------------------------------------------------------
# Classification heuristics — slug substring → (target, score, notes)
# ---------------------------------------------------------------------------
# Score 1..5 (5 = clear high-value pick for LQV).
TEXTURE_CLASSIFIERS: list[tuple[re.Pattern[str], str, int, str]] = [
    (re.compile(r"clay|adobe|mud_wall|plaster"), "house/material", 5, "vernacular wall finishes"),
    (re.compile(r"brick|terracotta|fired_clay|baked_clay"), "house/material", 5, "rural Paraguayan masonry"),
    (re.compile(r"thatch|reed|straw|palm_leaf"), "house/roof", 5, "bamboo/wigwam roofing"),
    (re.compile(r"corrugated|metal_roof|rusted_metal|zinc"), "house/roof", 4, "vernacular metal roofing"),
    (re.compile(r"shingle|tile_roof|terracotta_roof"), "house/roof", 4, "tile-roof typologies"),
    (re.compile(r"bamboo|culm"), "house/structure", 5, "bamboo culm dressing for bamboo typologies"),
    (re.compile(r"wood_planks|wood_floor|plank|deck"), "house/floor", 4, "decking + floor finishes"),
    (re.compile(r"bark|tree_bark|trunk_bark"), "flora/material", 4, "tree-bark scatter material"),
    (re.compile(r"laterite|red_ground|cracked_red|red_clay"), "terrain/ground", 5, "Paraguayan red-earth ground"),
    (re.compile(r"grass|lawn|meadow|aerial_grass"), "terrain/ground", 4, "grass scatter ground"),
    (re.compile(r"mud|muddy|wet_mud|tracks"), "terrain/ground", 4, "muddy tracks + creek surrounds"),
    (re.compile(r"riverbed|river_rock|cobble|river_sand|river_pebble"), "terrain/water", 5, "creek/river bed"),
    (re.compile(r"sandstone|cliff|outcrop|basalt|granite|rock"), "terrain/feature", 4, "hill outcrop / boulder"),
    (re.compile(r"moss|lichen"), "flora/material", 3, "moss tint for green-roof + boulders"),
    (re.compile(r"leaf_litter|forest_floor|fallen_leaves"), "terrain/ground", 4, "Atlantic-Forest litter"),
    (re.compile(r"concrete|cement|beton"), "house/material", 3, "bamboo+beton typologies"),
    (re.compile(r"painted|paint"), "house/finish", 2, "painted finishes for amenities"),
    (re.compile(r"fabric|cloth|canvas"), "house/finish", 2, "soft furnishings"),
    (re.compile(r"asphalt|road"), "terrain/path", 2, "rural access roads"),
    (re.compile(r"gravel|pebble"), "terrain/path", 4, "gravel paths"),
]

MODEL_CLASSIFIERS: list[tuple[re.Pattern[str], str, int, str]] = [
    (re.compile(r"fern|tree_fern|blechnum"), "flora/photoreal", 5, "fern photoreal — green-roof + creek banks"),
    (re.compile(r"anthurium|bromeliad|tillandsia"), "flora/photoreal", 5, "epiphyte / aroid placement"),
    (re.compile(r"jacaranda|lapacho|tabebuia"), "flora/tree", 5, "native flowering tree"),
    (re.compile(r"palm|pindo|butia|acrocomia|coconut|date_palm"), "flora/tree", 5, "palm species"),
    (re.compile(r"pachira|aguacate|avocado"), "flora/tree", 4, "subtropical tree"),
    (re.compile(r"euphorbia|cycad"), "flora/tree", 3, "succulent feature"),
    (re.compile(r"banana|musa|heliconia"), "flora/photoreal", 4, "banana / heliconia clump"),
    (re.compile(r"bamboo|guadua"), "flora/photoreal", 5, "bamboo grove backdrop"),
    (re.compile(r"agave|aloe|yucca|succulent"), "flora/photoreal", 3, "drought-tolerant accent"),
    (re.compile(r"vine|liana|creeper"), "flora/photoreal", 3, "vine drape over arches"),
    (re.compile(r"boulder|rock_moss|rock_set"), "terrain/feature", 5, "boulder scatter — Labrisa Lounge seating"),
    (re.compile(r"stump|log|fallen_tree|deadwood"), "flora/decoration", 3, "fallen wood detail"),
    (re.compile(r"shovel|hoe|trowel|pickaxe|hatchet|hammer|saw|wrench|tool"), "props/tools", 2, "hand tools dressing"),
    (re.compile(r"chair|stool|bench|table|seating"), "props/furniture", 3, "typology dressing"),
    (re.compile(r"sprinkler|garden|watering_can"), "props/garden", 2, "garden props"),
    (re.compile(r"lamp|lantern|pendant|bulb|light"), "props/lighting", 3, "amenity lighting"),
    (re.compile(r"door|window|shutter"), "house/feature", 3, "vernacular openings"),
    (re.compile(r"container|crate|barrel"), "house/structure", 3, "container typologies"),
    (re.compile(r"barrel|tank|water_tank|cistern"), "props/water", 3, "rural water infrastructure"),
]

HDRI_CLASSIFIERS: list[tuple[re.Pattern[str], str, int, str]] = [
    (re.compile(r"dawn|sunrise|morning"), "lighting/dawn", 5, "subtropical morning shoot"),
    (re.compile(r"sunset|dusk|evening|golden"), "lighting/dusk", 5, "warm finals / brochure shots"),
    (re.compile(r"night|moon|moonless|starlit"), "lighting/night", 4, "night ambiance"),
    (re.compile(r"overcast|cloudy|grey|fog|mist"), "lighting/overcast", 4, "diffuse lighting / post-storm"),
    (re.compile(r"puresky|clear|midday|noon"), "lighting/midday", 4, "clear-sky default"),
    (re.compile(r"indoor|interior|studio"), "lighting/interior", 3, "interior amenities"),
    (re.compile(r"urban|city|bund|street"), "lighting/urban", 2, "non-LQV default — last resort"),
    (re.compile(r"field|forest|pine|outdoor"), "lighting/exterior", 4, "exterior daytime"),
]


def _classify(slug: str, classifiers: list[tuple[re.Pattern[str], str, int, str]]) -> tuple[str, int, str]:
    for pat, target, score, notes in classifiers:
        if pat.search(slug):
            return target, score, notes
    return "unclassified", 1, ""


# ---------------------------------------------------------------------------
# License resolution
# ---------------------------------------------------------------------------
def _resolve_license(slug: str, source_hint: str) -> tuple[str, str]:
    """Return (license, source). Default: Poly Haven => CC0."""
    license_file = os.path.join(LICENSES, f"{slug}.txt")
    if os.path.exists(license_file):
        with open(license_file, encoding="utf-8") as fh:
            text = fh.read()
        # Look for "License: CC0" / "License: CC BY 4.0" / etc.
        m = re.search(r"License:\s*(.+?)\s*$", text, re.IGNORECASE | re.MULTILINE)
        if m:
            lic = m.group(1).strip()
            m2 = re.search(r"Source URL:\s*(.+?)\s*$", text, re.IGNORECASE | re.MULTILINE)
            src = m2.group(1).strip() if m2 else source_hint
            return lic, src
    return "CC0 1.0", source_hint


# ---------------------------------------------------------------------------
# Walkers
# ---------------------------------------------------------------------------
def _walk_hdris() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    hdri_dir = os.path.join(ASSETS, "hdris")
    if not os.path.isdir(hdri_dir):
        return out
    for fn in sorted(os.listdir(hdri_dir)):
        if not fn.endswith((".exr", ".hdr")):
            continue
        path = os.path.join(hdri_dir, fn)
        slug = re.sub(r"_4k\.(exr|hdr)$", "", fn)
        size_mb = os.path.getsize(path) / (1024 * 1024)
        target, score, notes = _classify(slug, HDRI_CLASSIFIERS)
        lic, src = _resolve_license(slug, "polyhaven.com")
        out.append({
            "id": slug,
            "type": "hdri",
            "source": src,
            "license": lic,
            "size_mb": round(size_mb, 1),
            "files": fn,
            "resolution_hint": "4k",
            "integration_target": target,
            "lqv_use_score": score,
            "notes": notes,
        })
    return out


def _walk_textures() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    tex_dir = os.path.join(ASSETS, "textures")
    if not os.path.isdir(tex_dir):
        return out
    # `ambientcg/` is a per-source container holding one subdir per ID; flatten
    # those out so each ID becomes its own row (rather than a single "ambientcg"
    # super-row that hides 85 distinct CC0 IDs from the inventory).
    AGGREGATOR_DIRS = {"ambientcg": "ambientcg.com"}
    for slug in sorted(os.listdir(tex_dir)):
        slug_dir = os.path.join(tex_dir, slug)
        if not os.path.isdir(slug_dir):
            continue
        if slug in AGGREGATOR_DIRS:
            src_hint = AGGREGATOR_DIRS[slug]
            for inner in sorted(os.listdir(slug_dir)):
                inner_dir = os.path.join(slug_dir, inner)
                if not os.path.isdir(inner_dir):
                    continue
                maps_present = []
                total_bytes = 0
                res_hint = "?"
                for root, _dirs, files in os.walk(inner_dir):
                    for fn in files:
                        fpath = os.path.join(root, fn)
                        total_bytes += os.path.getsize(fpath)
                        m = re.match(
                            r".+_(Color|Diffuse|Normal|nor_gl|Roughness|Rough|Displacement|AmbientOcclusion|AO)(?:_(\d+K|\d+k))?\.\w+$",
                            fn,
                        )
                        if m:
                            maps_present.append(m.group(1))
                            if m.group(2):
                                res_hint = m.group(2).lower()
                target, score, notes = _classify(inner, TEXTURE_CLASSIFIERS)
                lic, src = _resolve_license(inner, src_hint)
                out.append({
                    "id": inner,
                    "type": "texture",
                    "source": src,
                    "license": lic,
                    "size_mb": round(total_bytes / (1024 * 1024), 1),
                    "files": "|".join(sorted(set(maps_present))) or "?",
                    "resolution_hint": res_hint or "4k",
                    "integration_target": target,
                    "lqv_use_score": score,
                    "notes": notes,
                })
            continue
        maps_present = []
        total_bytes = 0
        res_hint = "?"
        for fn in os.listdir(slug_dir):
            fpath = os.path.join(slug_dir, fn)
            if not os.path.isfile(fpath):
                continue
            total_bytes += os.path.getsize(fpath)
            m = re.match(r".+_(Diffuse|nor_gl|Rough|Displacement|AO)_(\d+k)\.\w+$", fn)
            if m:
                maps_present.append(m.group(1))
                res_hint = m.group(2)
        target, score, notes = _classify(slug, TEXTURE_CLASSIFIERS)
        lic, src = _resolve_license(slug, "polyhaven.com")
        out.append({
            "id": slug,
            "type": "texture",
            "source": src,
            "license": lic,
            "size_mb": round(total_bytes / (1024 * 1024), 1),
            "files": "|".join(sorted(set(maps_present))) or "?",
            "resolution_hint": res_hint,
            "integration_target": target,
            "lqv_use_score": score,
            "notes": notes,
        })
    return out


def _walk_models() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    mod_dir = os.path.join(ASSETS, "models")
    if not os.path.isdir(mod_dir):
        return out
    for slug in sorted(os.listdir(mod_dir)):
        slug_dir = os.path.join(mod_dir, slug)
        if not os.path.isdir(slug_dir):
            continue
        blend_files = []
        total_bytes = 0
        for root, _dirs, files in os.walk(slug_dir):
            for fn in files:
                fpath = os.path.join(root, fn)
                total_bytes += os.path.getsize(fpath)
                if fn.endswith(".blend"):
                    blend_files.append(fn)
        target, score, notes = _classify(slug, MODEL_CLASSIFIERS)
        lic, src = _resolve_license(slug, "polyhaven.com")
        out.append({
            "id": slug,
            "type": "model",
            "source": src,
            "license": lic,
            "size_mb": round(total_bytes / (1024 * 1024), 1),
            "files": "|".join(blend_files) or "?",
            "resolution_hint": "4k",
            "integration_target": target,
            "lqv_use_score": score,
            "notes": notes,
        })
    return out


def _walk_terrain_and_references() -> list[dict[str, Any]]:
    """Light pass over terrain/ + references/ — these are catch-all dirs."""
    out: list[dict[str, Any]] = []
    for sub, default_target in [("terrain", "terrain/data"), ("references", "references/reading")]:
        sub_dir = os.path.join(ASSETS, sub)
        if not os.path.isdir(sub_dir):
            continue
        for fn in sorted(os.listdir(sub_dir)):
            fpath = os.path.join(sub_dir, fn)
            if not os.path.isfile(fpath):
                continue
            out.append({
                "id": os.path.splitext(fn)[0],
                "type": sub.rstrip("s"),
                "source": "various",
                "license": "?",
                "size_mb": round(os.path.getsize(fpath) / (1024 * 1024), 1),
                "files": fn,
                "resolution_hint": "n/a",
                "integration_target": default_target,
                "lqv_use_score": 3,
                "notes": "manual review",
            })
    return out


# ---------------------------------------------------------------------------
# Report writers
# ---------------------------------------------------------------------------
def _write_csv(rows: list[dict[str, Any]]) -> None:
    os.makedirs(DOCS, exist_ok=True)
    fieldnames = [
        "id", "type", "source", "license", "size_mb", "files",
        "resolution_hint", "integration_target", "lqv_use_score", "notes",
    ]
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_md(rows: list[dict[str, Any]]) -> None:
    os.makedirs(DOCS, exist_ok=True)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        grouped[r["integration_target"]].append(r)

    total_count = len(rows)
    total_size = round(sum(r["size_mb"] for r in rows), 1)
    by_type: dict[str, int] = defaultdict(int)
    for r in rows:
        by_type[r["type"]] += 1
    by_lic: dict[str, int] = defaultdict(int)
    for r in rows:
        by_lic[r["license"]] += 1

    # Top-15 picks: highest lqv_use_score then largest size as tiebreaker.
    top15 = sorted(rows, key=lambda r: (-r["lqv_use_score"], -r["size_mb"]))[:15]

    lines: list[str] = []
    lines.append("# La Quebrada Viva — Asset Integration Plan")
    lines.append("")
    lines.append(f"_Generated by `scripts/analyze_assets.py`._")
    lines.append("")
    lines.append("## Inventory summary")
    lines.append("")
    lines.append(f"- Total assets: **{total_count}**")
    lines.append(f"- Total disk: **{total_size:,.1f} MB**")
    lines.append("- By type: " + ", ".join(f"{k}={v}" for k, v in sorted(by_type.items())))
    lines.append("- By license: " + ", ".join(f"{k}={v}" for k, v in sorted(by_lic.items())))
    lines.append("")
    lines.append("## Top-15 first-wave integration picks")
    lines.append("")
    lines.append("| Rank | ID | Type | Score | Target | Notes |")
    lines.append("|---:|---|---|---:|---|---|")
    for i, r in enumerate(top15, 1):
        lines.append(
            f"| {i} | `{r['id']}` | {r['type']} | {r['lqv_use_score']} | "
            f"{r['integration_target']} | {r['notes']} |"
        )
    lines.append("")
    lines.append("## All assets, grouped by integration target")
    lines.append("")
    for target in sorted(grouped):
        bucket = sorted(grouped[target], key=lambda r: (-r["lqv_use_score"], r["id"]))
        lines.append(f"### {target} — {len(bucket)} asset(s)")
        lines.append("")
        lines.append("| ID | Type | Score | License | Size MB | Files | Notes |")
        lines.append("|---|---|---:|---|---:|---|---|")
        for r in bucket:
            lines.append(
                f"| `{r['id']}` | {r['type']} | {r['lqv_use_score']} | {r['license']} | "
                f"{r['size_mb']} | {r['files']} | {r['notes']} |"
            )
        lines.append("")

    with open(MD_OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main() -> int:
    rows: list[dict[str, Any]] = []
    rows += _walk_hdris()
    rows += _walk_textures()
    rows += _walk_models()
    rows += _walk_terrain_and_references()

    _write_csv(rows)
    _write_md(rows)

    print(f"Wrote {CSV_OUT} ({len(rows)} rows)")
    print(f"Wrote {MD_OUT}")
    print(f"Total disk: {sum(r['size_mb'] for r in rows):,.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
