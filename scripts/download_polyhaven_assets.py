"""Poly Haven CC0 asset library downloader — project-wide curated manifest.

Idempotent. 404-tolerant. Concurrency-capped. Resume-safe (skips already-on-disk files).

Layout:
    assets/hdris/<id>_4k.exr
    assets/textures/<id>/<id>_<map>_4k.<ext>
    assets/models/<id>/<id>_4k.blend
    assets/models/<id>/textures/<sidecar files>

Manifest categories (curated against Paraguay parcel + cob-house + typology needs):
    - HDRIs: sky/lighting moods (clear, golden, dusk, night, overcast)
    - Textures: terrain/rock/wood/bark/brick/plaster/mud — surfaces actually used
    - Models: flora extras, shrubs, rocks, structural props, rural containers, tools,
      furniture for typology dressing

Run:
    python3 scripts/download_polyhaven_assets.py
    # or, to dump manifest only:
    python3 scripts/download_polyhaven_assets.py --dry-run

All Poly Haven assets are CC0.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections.abc import Iterable

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(PROJECT_ROOT, "assets")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

POLYHAVEN_API = "https://api.polyhaven.com"
HDRI_DL_TEMPLATE = "https://dl.polyhaven.org/file/ph-assets/HDRIs/exr/4k/{id}_4k.exr"

# Texture map slots we care about (matches existing download_assets.sh).
TEXTURE_MAPS = ["Diffuse", "nor_gl", "Rough", "Displacement", "AO"]
TEXTURE_RES_FALLBACK = ["4k", "8k", "2k", "1k"]
TEXTURE_EXT_PREF = ["jpg", "png", "exr"]
MODEL_RES_FALLBACK = ["4k", "2k", "1k"]

CONCURRENCY = 8
TIMEOUT = 120

# ---------------------------------------------------------------------------
# Curated manifest. Add IDs here; rerun the script. Resume-safe.
# Each list is just Poly Haven slugs. Comments group by purpose.
# ---------------------------------------------------------------------------

HDRIS: list[str] = [
    # Existing baseline (already on disk; kept for idempotency / audit)
    "kiara_1_dawn",
    "misty_pines",
    "qwantani_dusk_2",
    "qwantani_sunset_puresky",
    # Project-wide additions
    "autumn_field_puresky",         # clear midday puresky
    "kloppenheim_02_puresky",       # night puresky
    "bambanani_sunset",             # warm sunset / partly cloudy
    "kloofendal_48d_partly_cloudy_puresky",
    "satara_night",                 # clean overhead night
    "shanghai_bund",                # urban dusk for typology dressing
]

TEXTURES: list[str] = [
    # Existing baseline (already on disk)
    "aerial_mud_1",
    "aerial_grass_rock",
    "dry_riverbed_rock",
    "clay_block_wall",
    "clay_plaster",
    "dark_wood",
    "wood_floor_deck",
    "tree_bark_03",
    "palm_tree_bark",
    "bark_platanus",
    "cracked_red_ground",
    "muddy_tracks",
    # Terrain additions
    "brown_mud",
    "brown_mud_dry",
    "brown_mud_leaves_01",
    "brown_mud_rocks_01",
    "forest_floor",
    "aerial_rocks_02",
    "aerial_sand",
    "aerial_beach_01",
    # Rock additions (for escarpment + stream bank)
    "lichen_rock",
    "gray_rocks",
    "cliff_side",
    "rock_face",
    "rock_wall_10",
    # Wood additions (for bridges, decks, structural props)
    "bark_brown_01",
    "bark_willow",
    "pine_bark",
    "oak_veneer_01",
    "weathered_planks",
    "wood_planks_grey",
    "wood_table_001",
    # Brick / adobe / typology surfaces
    "red_brick_03",
    "castle_brick_02_red",
    "brick_wall_001",
    "broken_brick_wall",
    "weathered_brown_planks",
    # Plaster / cob exterior
    "beige_wall_001",
    "blue_plaster_weathered",
    # Outdoor surfaces (paths, gravel)
    "aerial_asphalt_01",
    "gravel_concrete",
    "rocky_terrain_02",
]

MODELS: list[str] = [
    # Existing baseline flora (already on disk)
    "jacaranda_tree",
    "pachira_aquatica_01",
    "fern_02",
    "anthurium_botany_01",
    "boulder_01",
    "rock_moss_set_02",
    # Extra trees / palm / pine proxies
    "island_tree_01",
    "island_tree_02",
    "tree_small_02",
    "fir_tree_01",
    "pine_tree_01",
    "tree_stump_01",
    "tree_stump_02",
    "dead_tree_trunk_02",
    # Shrubs / groundcover
    "shrub_01",
    "shrub_02",
    "shrub_03",
    "shrub_04",
    "shrub_sorrel_01",
    "moss_01",
    "calathea_orbifolia_01",
    # Succulents / xerophytes (agave-adjacent)
    "crystalline_iceplant",
    "cheiridopsis_succulent",
    # Wildflowers (scatter dressing)
    "celandine_01",
    "dandelion_01",
    "periwinkle_plant",
    "flower_gazania",
    # Grasses
    "grass_medium_01",
    "grass_medium_02",
    # Forest litter / dead wood
    "bark_debris_01",
    "dry_branches_medium_01",
    "pine_roots",
    "root_cluster_01",
    "single_root",
    # Rocks (escarpment + stream + path edges)
    "rock_07",
    "rock_09",
    "rock_face_01",
    "rock_moss_set_01",
    "namaqualand_boulder_02",
    "namaqualand_boulder_03",
    "namaqualand_boulder_04",
    "namaqualand_cliff_01",
    "coast_land_rocks_02",
    # Structures (for typology stubs)
    "stone_fire_pit",
    "large_castle_door",
    "large_iron_gate",
    "modular_chainlink_fence",
    "modular_wooden_pier",
    "modular_electricity_poles",
    "utility_box_01",
    "water_manhole_cover",
    # Containers / rural props
    "planter_pot_clay",
    "ceramic_vase_01",
    "ceramic_vase_02",
    "wicker_basket_01",
    "wooden_bucket_01",
    "watering_can_metal_01",
    "wooden_crate_01",
    "wooden_barrels_01",
    "planter_box_01",
    "seeding_tray_01",
    # Tools (cob-house workshop dressing)
    "wooden_axe_03",
    "wooden_hammer_01",
    "wooden_ladder",
    "rusted_spade_01",
    "trowel_01",
    "hatchet",
    "handsaw_wood",
    "sledgehammer_01",
    "garden_sprinkler_01",
    # Furniture (typology dressing)
    "outdoor_table_chair_set_01",
    "wooden_picnic_table",
    "painted_wooden_bench",
    "painted_wooden_chair_01",
    "painted_wooden_stool",
    "painted_wooden_table",
    "folding_wooden_stool",
    "wooden_stool_01",
    "modular_street_seating",
]

# ---------------------------------------------------------------------------
# Expansion 2026-06-13 — push library past 200 unique CC0 IDs on disk.
# All slugs validated against live Poly Haven catalog before inclusion.
# See docs/research/ASSET_RESEARCH_2026-06-13.md for rationale per asset.
# ---------------------------------------------------------------------------

EXTRA_HDRIS: list[str] = [
    # Dusk variants (warm sunset → low-sun rural moods)
    "belfast_sunset",
    "dikhololo_sunset",
    "evening_field",
    "evening_road_01",
    # Dawn variants (cool sunrise / morning haze)
    "blouberg_sunrise_2",
    "citrus_orchard",
    "drackenstein_quarry",
    "bell_park_dawn",
    # Overcast / soft-sky countryside
    "autumn_field",
    "belfast_open_field",
    "alps_field",
    "abandoned_pathway",
    "blaubeuren_hillside",
    "autumn_meadow",
    "autumn_hilly_field",
    "ahornsteig",
    # Neutral studio for prop turnarounds
    "studio_small_03",
    "studio_small_09",
    # Forest / harvest rural ambience
    "forest_slope",
    "harvest",
    # P1.A.5 cerrado / Atlantic-Forest-edge biome swap (variant dispatcher)
    # A=warm dry-season morning, B=overcast wet-season midday, C=civil-twilight blue hour
    "bryanston_park_sunrise",
    "xanderklinge",
    "kloppenheim_07",
    # Backups in case primary picks fail QA
    "magalies_field_sunset",
    "near_the_river_02",
    "niederwihl_forest",
    "belfast_open_field",
    "kloppenheim_04",
]

EXTRA_TEXTURES: list[str] = [
    # Terracotta clay roof tiles (housing-park vernacular roofs)
    "clay_roof_tiles",
    "clay_roof_tiles_02",
    "clay_roof_tiles_03",
    "red_slate_roof_tiles_01",
    "roof_07",
    "ceramic_roof_01",
    "grey_roof_tiles",
    # Hand-formed / vernacular brick variants
    "brick_4",
    "brick_wall_003",
    "brick_wall_006",
    "brick_wall_08",
    "brick_wall_11",
    "brick_wall_13",
    "brick_pavement",
    "brick_floor",
    "castle_brick_01",
    "castle_brick_02_white",
    "brown_brick_02",
    "church_bricks_02",
    "dark_brick_wall",
    # Mud / adobe-adjacent ground (Paraguayan red earth)
    "brown_mud_02",
    "brown_mud_03",
    "dry_ground_01",
    "dry_ground_rocks",
    "dry_mud_field_001",
    "mud_cracked_dry_03",
    "dirt_floor",
    "dirt_aerial_02",
    "dirt_aerial_03",
    "burned_ground_01",
    # Rural wood (lapacho-finish surrogates, weathered planks)
    "bark_brown_02",
    "bark_willow_02",
    "old_planks_02",
    "brown_planks_03",
    "brown_planks_05",
    "brown_planks_09",
    "dark_planks",
    "dark_wooden_planks",
    "fine_grained_wood",
    "kitchen_wood",
    "medieval_wood",
    "moss_wood",
    "beam_wall_01",
    "green_rough_planks",
    # Weathered metal / zinc roofing (Paraguayan rural vernacular)
    "corrugated_iron",
    "corrugated_iron_02",
    "corrugated_iron_03",
    "rusty_corrugated_iron",
    "worn_corrugated_iron",
    "box_profile_metal_sheet",
    "rusty_metal_sheet",
    "green_metal_rust",
    "rust_coarse_01",
    "rusty_metal_02",
    "rusty_metal_03",
    # River stone / cobblestone (stream bed + paths)
    "clean_pebbles",
    "cobblestone_floor_01",
    "cobblestone_floor_02",
    "cobblestone_floor_03",
    "cobblestone_large_01",
    "cobblestone_color",
    "bicolour_gravel",
    # Lateritic ground (aerial-scale red dirt)
    "aerial_ground_rock",
    # Grass / forest litter
    "forrest_ground_01",
    "forrest_ground_03",
    "leafy_grass",
    "sparse_grass",
    "grass_path_2",
    "grass_path_3",
    "dry_decay_leaves",
    "grass_concrete_pavement",
    # Reed / thatch roof
    "reed_roof_03",
    "reed_roof_04",
    "thatch_roof_angled",
    "riet_01",
    # Lime plaster (cob exterior variants)
    "beige_wall_002",
    "damaged_plaster",
    "clay_floor_001",
]

EXTRA_MODELS: list[str] = [
    # Trees + saplings (early-phase housing-park planting)
    "island_tree_03",
    "fir_sapling",
    "fir_sapling_medium",
    "pine_sapling_medium",
    "pine_sapling_small",
    "dead_tree_trunk",
    "root_cluster_02",
    # Botany / flowers / scrubs (dry-season scatter)
    "didelta_spinosa",
    "othonna_cerarioides",
    "leipoldtia_schultzei",
    "flower_empodium",
    "flower_heliophila",
    "flower_stinkkruid",
    "flower_ursinia",
    "nettle_plant",
    "grass_bermuda_01",
    # Extra rocks (escarpment + stream-bank surrogates)
    "namaqualand_rocks_01",
    "namaqualand_stones_01",
    "coast_land_rocks_03",
    "coast_land_rocks_04",
    "coast_rocks_01",
    "coast_rocks_02",
    "coast_rocks_03",
    "coast_rocks_05",
    "coast_line_01",
    "coast_line_02",
    "coastal_cliff_01",
    # Ceramic + brass kitchen / porch dressing (tereré + brass vernacular)
    "ceramic_vase_03",
    "ceramic_vase_04",
    "antique_ceramic_vase_01",
    "brass_vase_01",
    "brass_vase_02",
    "brass_vase_03",
    "brass_vase_04",
    "brass_pot_01",
    "brass_pot_02",
    "brass_pan_01",
    "jug_01",
    "metal_jug",
    "pot_enamel_01",
    # Planter boxes
    "planter_box_02",
    "planter_box_03",
    # Buckets / barrels / crates (restaurant amenity dressing)
    "wooden_bucket_02",
    "barrel_03",
    "barrel_02",
    "barrel_01",
    "wooden_crate_02",
    "cheesebox_01",
    "wine_barrel_01",
    "barrel_stove",
    # Lanterns / oil lamps (Variant C blue-hour warm sources)
    "lantern_01",
    "vintage_oil_lamp",
    "brass_diya_lantern",
    "wooden_lantern_01",
    "lantern_chandelier_01",
    "street_lamp_01",
    "street_lamp_02",
    # Hand + farm tools (machete = iconic Paraguayan tool)
    "machete",
    "cross_pein_hammer",
    "crowbar_01",
    "hand_plane_no4",
    "flathead_screwdriver",
    "bench_vice_01",
    "bolt_cutters_01",
    "ladder_sectioned_01",
    "hand_truck",
    "dustpan",
    "measuring_tape_01",
    "metal_toolbox",
    "metal_tool_chest",
    "brass_blowtorch",
    # Carts / wheels (ox-cart / carreta vernacular)
    "rusted_wheel_rim_01",
    "rusted_wheel_rim_02",
    "spinning_wheel_01",
    "old_tyre",
    "tire_pump",
    "coffeecart_01",
    # Gates / latches
    "gate_latch_01",
    # Kitchen / hearth (tatakuá amenity)
    "electric_stove",
    "wooden_cutting_board",
    "wooden_spoon",
    "tea_set_01",
    # Misc rural / industrial infrastructure
    "metal_jerrycan",
    "metal_jerrycan_green",
    "compost_bags",
    "compost_bag_02",
    "old_military_crate",
    "fire_hydrant",
    "can_rusted",
    "cleaner_tin_01",
    "propane_tank",
    "small_lpg_tank",
    # Potted plants (porch dressing)
    "potted_plant_01",
    "potted_plant_02",
    "potted_plant_04",
]

# ---------------------------------------------------------------------------
# Download primitives
# ---------------------------------------------------------------------------

def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _http_get(url: str, timeout: int = TIMEOUT) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "lqv-asset-downloader/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _http_json(url: str, timeout: int = TIMEOUT) -> dict:
    return json.loads(_http_get(url, timeout=timeout).decode("utf-8"))


def _download_to(url: str, dest: str, log) -> tuple[str, str, int]:
    """Download `url` to `dest` if not already present. Returns (status, dest, bytes)."""
    if os.path.exists(dest) and os.path.getsize(dest) > 1024:
        return ("skip", dest, os.path.getsize(dest))
    _ensure_dir(os.path.dirname(dest))
    tmp = dest + ".part"
    try:
        data = _http_get(url)
        with open(tmp, "wb") as fh:
            fh.write(data)
        os.replace(tmp, dest)
        return ("ok", dest, len(data))
    except urllib.error.HTTPError as e:
        if os.path.exists(tmp):
            os.unlink(tmp)
        log(f"  HTTP {e.code} {url}")
        return ("fail", dest, 0)
    except Exception as e:
        if os.path.exists(tmp):
            os.unlink(tmp)
        log(f"  ERR  {e!s} {url}")
        return ("fail", dest, 0)


# ---------------------------------------------------------------------------
# Asset-type strategies
# ---------------------------------------------------------------------------

def plan_hdri(slug: str) -> list[tuple[str, str]]:
    url = HDRI_DL_TEMPLATE.format(id=slug)
    dest = os.path.join(ASSETS, "hdris", f"{slug}_4k.exr")
    return [(url, dest)]


def plan_texture(slug: str, log) -> list[tuple[str, str]]:
    try:
        files = _http_json(f"{POLYHAVEN_API}/files/{slug}")
    except Exception as e:
        log(f"[texture] {slug}: API lookup failed: {e}")
        return []
    plans: list[tuple[str, str]] = []
    out_dir = os.path.join(ASSETS, "textures", slug)
    for map_name in TEXTURE_MAPS:
        if map_name not in files:
            continue
        for res in TEXTURE_RES_FALLBACK:
            if res not in files[map_name]:
                continue
            for ext in TEXTURE_EXT_PREF:
                if ext not in files[map_name][res]:
                    continue
                url = files[map_name][res][ext]["url"]
                dest = os.path.join(out_dir, f"{slug}_{map_name}_4k.{ext}")
                plans.append((url, dest))
                break
            break
    return plans


def plan_model(slug: str, log) -> list[tuple[str, str]]:
    try:
        files = _http_json(f"{POLYHAVEN_API}/files/{slug}")
    except Exception as e:
        log(f"[model] {slug}: API lookup failed: {e}")
        return []
    blend_files = files.get("blend", {})
    blend = None
    for res in MODEL_RES_FALLBACK:
        candidate = blend_files.get(res, {}).get("blend")
        if candidate:
            blend = candidate
            log(f"[model] {slug}: using {res} blend")
            break
    if not blend:
        log(f"[model] {slug}: no blend at any of {MODEL_RES_FALLBACK} in API response")
        return []
    out_dir = os.path.join(ASSETS, "models", slug)
    plans: list[tuple[str, str]] = []
    # Keep canonical filename `<slug>_4k.blend` regardless of source resolution so
    # downstream builders that hard-code that path keep working.
    plans.append((blend["url"], os.path.join(out_dir, f"{slug}_4k.blend")))
    for rel_path, entry in blend.get("include", {}).items():
        plans.append((entry["url"], os.path.join(out_dir, rel_path)))
    return plans


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def run(plans: Iterable[tuple[str, str]], log) -> dict:
    counts = {"ok": 0, "skip": 0, "fail": 0, "bytes": 0}
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futures = [ex.submit(_download_to, url, dest, log) for url, dest in plans]
        for fut in as_completed(futures):
            status, dest, nbytes = fut.result()
            counts[status] += 1
            counts["bytes"] += nbytes
            if status == "ok":
                log(f"  + {os.path.relpath(dest, PROJECT_ROOT)} ({nbytes / 1024:.0f} KiB)")
    return counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="enumerate plans only, do not download")
    parser.add_argument("--only", choices=["hdris", "textures", "models"], help="restrict to one asset type")
    args = parser.parse_args()

    _ensure_dir(LOG_DIR)
    log_path = os.path.join(LOG_DIR, f"asset_download_{int(time.time())}.log")
    log_fh = open(log_path, "w", buffering=1)

    def log(msg: str) -> None:
        print(msg)
        log_fh.write(msg + "\n")

    all_hdris = HDRIS + EXTRA_HDRIS
    all_textures = TEXTURES + EXTRA_TEXTURES
    all_models = MODELS + EXTRA_MODELS
    log(
        f"[manifest] hdris={len(all_hdris)} ({len(HDRIS)}+{len(EXTRA_HDRIS)}) "
        f"textures={len(all_textures)} ({len(TEXTURES)}+{len(EXTRA_TEXTURES)}) "
        f"models={len(all_models)} ({len(MODELS)}+{len(EXTRA_MODELS)})"
    )
    log(f"[log] {log_path}")

    types = ("hdris", "textures", "models") if args.only is None else (args.only,)
    grand = {"ok": 0, "skip": 0, "fail": 0, "bytes": 0}

    for t in types:
        log(f"\n=== {t.upper()} ===")
        all_plans: list[tuple[str, str]] = []
        if t == "hdris":
            for slug in all_hdris:
                all_plans.extend(plan_hdri(slug))
        elif t == "textures":
            for slug in all_textures:
                ps = plan_texture(slug, log)
                if not ps:
                    log(f"  ~ skip {slug} (no plan)")
                all_plans.extend(ps)
        elif t == "models":
            for slug in all_models:
                ps = plan_model(slug, log)
                if not ps:
                    log(f"  ~ skip {slug} (no plan)")
                all_plans.extend(ps)

        log(f"[{t}] {len(all_plans)} file plans")
        if args.dry_run:
            for url, dest in all_plans:
                log(f"  DRY {dest}")
            continue
        counts = run(all_plans, log)
        log(f"[{t}] ok={counts['ok']} skip={counts['skip']} fail={counts['fail']} bytes={counts['bytes']}")
        for k in counts:
            grand[k] += counts[k]

    log(f"\n[grand] ok={grand['ok']} skip={grand['skip']} fail={grand['fail']} bytes={grand['bytes']/1024/1024:.1f} MiB")
    log_fh.close()
    return 0 if grand["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
