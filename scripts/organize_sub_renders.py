"""Build a browse-friendly symlink tree over the flat sub-render layout.

Reads `renders/sub/*.png` and creates relative symlinks under
`renders/sub_by_category/<category>/<group>/<asset>/<variant>.png`,
so the flat back-compat path documented in CLAUDE.md:154 stays
authoritative while humans get a 4-level browsable view.

Idempotent: clears `sub_by_category/` and rebuilds each run.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUB = ROOT / "renders" / "sub"
OUT = ROOT / "renders" / "sub_by_category"

# (category, group, asset_stem) keyed by filename stem prefix.
# Match is longest-prefix-wins on the stem (sans _A/_B/_C suffix).
TAXONOMY: list[tuple[str, str, str]] = [
    # houses / typologies — material first, then asset
    ("01_houses", "bamboo",          "bamboo_beton_28"),
    ("01_houses", "bamboo",          "bamboo_beton_30"),
    ("01_houses", "bamboo",          "bamboo_beton_family_curved"),
    ("01_houses", "bamboo",          "bamboo_beton_family_rectangular"),
    ("01_houses", "bamboo",          "bamboo_boomhut_treehouse"),
    ("01_houses", "bamboo",          "bamboo_container_4pax"),
    ("01_houses", "bamboo",          "bamboo_curved_roof_villa"),
    ("01_houses", "bamboo",          "bamboo_portal"),
    ("01_houses", "bamboo",          "bamboo_river_house"),
    ("01_houses", "bamboo",          "bamboo_wigwam_lodge"),
    ("01_houses", "italian_stone",   "italian_river_house_4pax"),
    ("01_houses", "italian_stone",   "italian_stone_small_v1"),
    ("01_houses", "italian_stone",   "italian_stone_small_v2"),
    ("01_houses", "clay_terracotta", "clay_terracotta_estate"),
    ("01_houses", "hobbit",          "hobbit_house"),
    ("01_houses", "mushroom_cob",    "mushroom_cob_house"),
    ("01_houses", "container",       "container_river_house"),
    ("01_houses", "eco_retreat",     "eco_retreat_modern_oasis"),
    # amenities
    ("02_amenities", "pool",            "eco_pool"),
    ("02_amenities", "lounge",          "labrisa_lounge"),
    ("02_amenities", "dining",          "floating_dining"),
    ("02_amenities", "outdoor_shower",  "bamboo_outdoor_shower"),
    ("02_amenities", "candle_path",     "candle_path"),
    # flora
    ("03_flora", "anthurium",    "flora_anthurium"),
    ("03_flora", "jacaranda",    "flora_jacaranda"),
    ("03_flora", "pachira",      "flora_pachira"),
    ("03_flora", "bamboo_clump", "bamboo_clump"),
    # site / terrain
    ("04_site", "terrain_62ha_dem",       "terrain_62ha"),
    ("04_site", "terrain_62ha_photoreal", "terrain_62ha_photoreal"),
    ("04_site", "terrain_house_scale",    "terrain_house_scale"),
    ("04_site", "boulder_cluster",        "boulder_cluster"),
    # diagnostics / compares
    ("05_compares", "hdri_dusk",    "hdri_dusk_compare"),
    ("05_compares", "material_wall", "material_wall_compare"),
]

# Sort by stem length descending so longer prefixes win
TAXONOMY.sort(key=lambda row: len(row[2]), reverse=True)


def classify(stem: str) -> tuple[str, str, str, str] | None:
    """Return (category, group, asset, variant) or None if unclassified.

    variant is "A", "B", "C", or a free-form tag like "aerial"/"hero".
    """
    for category, group, asset in TAXONOMY:
        if stem == asset:
            return category, group, asset, "default"
        if stem.startswith(asset + "_"):
            tail = stem[len(asset) + 1:]
            return category, group, asset, tail
    return None


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    pngs = sorted(SUB.glob("*.png"))
    linked = 0
    skipped: list[str] = []

    for png in pngs:
        result = classify(png.stem)
        if result is None:
            skipped.append(png.name)
            continue
        category, group, asset, variant = result
        dest_dir = OUT / category / group / asset
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{variant}.png"
        # Relative symlink so the tree survives moves/zips
        rel_target = Path("..", "..", "..", "..", "sub", png.name)
        if dest.is_symlink() or dest.exists():
            dest.unlink()
        dest.symlink_to(rel_target)
        linked += 1

    print(f"linked: {linked}")
    print(f"skipped: {len(skipped)}")
    for name in skipped:
        print(f"  skip {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
