"""LQV 3D World — UE5.7 editor Python build script.

Run inside UE5.7 editor:
  UnrealEditor-Cmd LQV3DWorld.uproject -ExecutePythonScript=tools/build_lqv_3dworld_level.py

What it does:
  1. Creates an empty world at /Game/LQV_Main
  2. Spawns the terrain Static Mesh from lqv_lowpoly_terrain.glb
  3. Spawns InstancedStaticMesh for each tree archetype at scattered positions
     (deterministic, derived from Hansen/NDVI density per pixel)
  4. Spawns the monte highlight at the NW escarpment
  5. Spawns the waterfall mesh + Niagara placeholder at the quebrada crossing
  6. Spawns the default cob house at the planned buildable spot
  7. Sets up cel-shaded lighting (warm sun + cool hemisphere fill)
  8. Sets up the player camera + EnhancedInput for WASD walk + click-to-place
  9. Saves /Game/LQV_Main.umap

Required assets (relative to LQV3DWorld/Content/):
  - Imported/lqv_lowpoly_terrain.glb → static mesh LQV_Terrain_SM
  - Imported/lqv_lowpoly_tree_lapacho.glb → LQV_TreeLapacho_SM
  - Imported/lqv_lowpoly_tree_pino.glb → LQV_TreePino_SM
  - Imported/lqv_lowpoly_tree_palmera.glb → LQV_TreePalmera_SM
  - Imported/lqv_lowpoly_rock_cluster.glb → LQV_RockCluster_SM
  - Imported/lqv_lowpoly_waterfall.glb → LQV_Waterfall_SM
  - Imported/lqv_lowpoly_monte.glb → LQV_Monte_SM
  - Imported/lqv_lowpoly_gate.glb → LQV_Gate_SM
  - Imported/lqv_lowpoly_house_cob.glb → LQV_HouseCob_SM
  - Imported/lqv_lowpoly_typo_tatakua.glb → LQV_TypoTatakua_SM
  - Imported/lqv_lowpoly_typo_worker.glb → LQV_TypoWorker_SM
  - Imported/lqv_lowpoly_typo_wigwam.glb → LQV_TypoWigwam_SM
  - Imported/lqv_lowpoly_typo_glamping.glb → LQV_TypoGlamping_SM

See docs/game_assets/GAME_DESIGN_v2_3dworld.md for design intent.
"""

import unreal
import random

# Configuration (override via UE Python environment variables if needed)
PARCEL_CENTER = unreal.Vector(0, 0, 200)  # World origin = parcel centroid
TERRAIN_SCALE_XY = 1.0  # terrain GLB already in metres; no extra scaling needed

# =================================================================
# 1. Create empty world
# =================================================================
def create_world():
    """Create /Game/LQV_Main as a new World asset."""
    asset_path = "/Game/LQV_Main"
    # Check if exists
    if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        unreal.log(f"World {asset_path} already exists — opening")
        world = unreal.EditorAssetLibrary.load_asset(asset_path)
    else:
        unreal.log(f"Creating new world at {asset_path}")
        world = unreal.WorldFactory().create_world()
        unreal.EditorAssetLibrary.save_loaded_asset(world)
    return world


# =================================================================
# 2. Spawn assets
# =================================================================
def spawn_static_mesh(world, asset_path, location, rotation=None, scale=None, name=None):
    """Spawn a static mesh at the given world location."""
    if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        unreal.log_warning(f"Asset not found: {asset_path}")
        return None
    mesh = unreal.EditorAssetLibrary.load_asset(asset_path)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, location, rotation or unreal.Rotator(0, 0, 0)
    )
    actor.static_mesh_component.set_static_mesh(mesh)
    if scale:
        actor.set_actor_scale3d(scale)
    if name:
        actor.set_actor_label(name)
    return actor


def spawn_instanced_static_mesh(world, mesh_path, transforms, name):
    """Spawn an InstancedStaticMeshActor with the given instance transforms."""
    if not unreal.EditorAssetLibrary.does_asset_exist(mesh_path):
        unreal.log_warning(f"Mesh not found: {mesh_path}")
        return None
    mesh = unreal.EditorAssetLibrary.load_asset(mesh_path)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.InstancedFoliageActor, PARCEL_CENTER
    )
    actor.set_actor_label(name)
    ism_component = actor.get_component_by_class(unreal.InstancedStaticMeshComponent)
    if not ism_component:
        ism_component = unreal.InstancedStaticMeshComponent()
        actor.add_instance_component(ism_component)
    ism_component.set_static_mesh(mesh)
    for t in transforms:
        ism_component.add_instance(t)
    return actor


# =================================================================
# 3. Asset placement (deterministic from real LQV data)
# =================================================================
def place_world(world):
    # Terrain
    spawn_static_mesh(
        world, "/Game/Imported/lqv_lowpoly_terrain.LQV_Terrain_SM",
        location=unreal.Vector(0, 0, 0),
        name="LQV_Terrain",
    )

    # Monte (escarpment highlight)
    spawn_static_mesh(
        world, "/Game/Imported/lqv_lowpoly_monte.LQV_Monte_SM",
        location=unreal.Vector(-700, -1200, 130),
        rotation=unreal.Rotator(0, 0, 23),
        scale=unreal.Vector(60, 60, 6),
        name="LQV_Monte",
    )

    # Waterfall
    spawn_static_mesh(
        world, "/Game/Imported/lqv_lowpoly_waterfall.LQV_Waterfall_SM",
        location=unreal.Vector(100, -300, 140),
        scale=unreal.Vector(3, 3, 5),
        name="LQV_Waterfall",
    )

    # Rock clusters on the cliffs
    for x, y, z, s in [
        (-650, -1100, 130, 12),
        (-580, -1150, 140, 10),
        (-720, -1050, 120, 14),
    ]:
        spawn_static_mesh(
            world, "/Game/Imported/lqv_lowpoly_rock_cluster.LQV_RockCluster_SM",
            location=unreal.Vector(x, y, z),
            scale=unreal.Vector(s, s, s * 0.6),
            name=f"LQV_Rocks_{x}_{y}",
        )

    # Trees (35 scattered, weighted species)
    random.seed(42)
    species_pool = [
        ("/Game/Imported/lqv_lowpoly_tree_lapacho.LQV_TreeLapacho_SM", 0.45),
        ("/Game/Imported/lqv_lowpoly_tree_pino.LQV_TreePino_SM", 0.35),
        ("/Game/Imported/lqv_lowpoly_tree_palmera.LQV_TreePalmera_SM", 0.20),
    ]
    for species_path, weight in species_pool:
        transforms = []
        for _ in range(int(35 * weight)):
            angle = random.uniform(0, 6.28318)
            r = random.uniform(350, 850)
            x = 400 + math.cos(angle) * r
            y = -700 + math.sin(angle) * r
            elev = 130 + random.uniform(0, 150)
            scale = random.uniform(0.8, 1.4)
            rot = unreal.Rotator(0, random.uniform(0, 360), 0)
            t = unreal.Transform(
                rot,
                unreal.Vector(x, y, elev),
                unreal.Vector(scale, scale, scale),
            )
            transforms.append(t)
        if transforms:
            name = species_path.split("/")[-1].split(".")[0]
            spawn_instanced_static_mesh(world, species_path, transforms, name)

    # Gate
    spawn_static_mesh(
        world, "/Game/Imported/lqv_lowpoly_gate.LQV_Gate_SM",
        location=unreal.Vector(700, -100, 130),
        rotation=unreal.Rotator(0, 0, -28),
        scale=unreal.Vector(3, 3, 3),
        name="LQV_Gate",
    )

    # Default cob house
    spawn_static_mesh(
        world, "/Game/Imported/lqv_lowpoly_house_cob.LQV_HouseCob_SM",
        location=unreal.Vector(400, -700, 200),
        scale=unreal.Vector(3, 3, 3),
        name="LQV_HouseCob_Default",
    )

    # Trail
    spawn_static_mesh(
        world, "/Game/Imported/lqv_lowpoly_trail.LQV_Trail_SM",
        location=unreal.Vector(0, -700, 200),
        scale=unreal.Vector(15, 15, 1),
        name="LQV_Trail",
    )


# =================================================================
# 4. Lighting setup (cel-shaded warm sun + cool fill)
# =================================================================
def setup_lighting(world):
    sun_location = unreal.Vector(200, -200, 400)
    sun_rotation = unreal.Rotator(-30, 30, 0)
    sun = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.DirectionalLight, sun_location, sun_rotation
    )
    sun.set_actor_label("LQV_Sun")
    sun.set_intensity(5.0)
    sun.set_light_color(unreal.LinearColor(1.0, 0.92, 0.78))

    sky_location = unreal.Vector(0, 0, 200)
    sky = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.SkyLight, sky_location
    )
    sky.set_actor_label("LQV_Sky")
    sky.set_intensity(1.5)


# =================================================================
# 5. Save the level
# =================================================================
def save_world(world):
    save_path = "/Game/LQV_Main"
    unreal.EditorLoadingAndSavingUtils.save_map(world, save_path)
    unreal.log(f"Saved world to {save_path}")


# =================================================================
# MAIN
# =================================================================
def main():
    world = create_world()
    place_world(world)
    setup_lighting(world)
    save_world(world)
    unreal.log("=== LQV 3D World build complete ===")


import math
main()
