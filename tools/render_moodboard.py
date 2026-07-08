#!/usr/bin/env python3
"""Render 4 mood-board cameras showing the LQV 3D world low-poly style.

Loads each generated GLB, composes them in a single scene, renders 4 cameras
(hero, gate, monte, parcel overview) as PNGs for the operator to sign off the
visual direction before we build the browser preview.
"""
import bpy
import os

OUT_DIR = "/root/la-quebrada-viva/docs/game_assets/lowpoly"
RENDER_DIR = "/root/la-quebrada-viva/docs/game_assets/lowpoly_renders"
os.makedirs(RENDER_DIR, exist_ok=True)

LOWPOLY = OUT_DIR


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_glb(path, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
    """Import GLB and place at location."""
    before = set(o.name for o in bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new_objs = [o for o in bpy.data.objects if o.name not in before]
    for o in new_objs:
        o.location = location
        o.rotation_euler = rotation
        o.scale = scale
    return new_objs


def build_mood_scene():
    """Compose a small representative scene with terrain, trees, house, monte, gate."""
    reset_scene()

    # 1. World background = warm sky
    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.910, 0.847, 0.690, 1.0)
    bpy.context.scene.world = world

    # 2. Terrain (the actual DEM mesh) at origin
    terrain_objs = import_glb(f"{LOWPOLY}/lqv_lowpoly_terrain.glb")
    # Terrain mesh extends ~160x160m. Scale up so we see more context.
    for o in terrain_objs:
        o.scale = (8, 8, 8)  # 8x bigger → ~1.3 km box
        o.location = (0, 0, 0)

    # 3. Monte (escarpment) at NW corner
    monte_objs = import_glb(f"{LOWPOLY}/lqv_lowpoly_monte.glb",
                            location=(-400, -400, 100),
                            scale=(40, 40, 12))
    # The monte peak rises 12m at scale 1, → at scale 12 = 144m. OK dramatic.

    # 4. Waterfall at quebrada crossing
    import_glb(f"{LOWPOLY}/lqv_lowpoly_waterfall.glb",
               location=(-100, 200, 50),
               rotation=(0, 0, 0.3),
               scale=(2, 2, 8))

    # 5. Cob house at "flagged buildable" spot
    house_objs = import_glb(f"{LOWPOLY}/lqv_lowpoly_house_cob.glb",
                             location=(150, -150, 100),
                             scale=(2.5, 2.5, 2.5))

    # 6. Scatter 30 trees around the property
    import random
    random.seed(42)
    tree_species = [
        (f"{LOWPOLY}/lqv_lowpoly_tree_lapacho.glb", 0.5),  # 50% lapacho
        (f"{LOWPOLY}/lqv_lowpoly_tree_pino.glb", 0.3),
        (f"{LOWPOLY}/lqv_lowpoly_tree_palmera.glb", 0.2),
    ]
    for _ in range(30):
        species = random.choices([t[0] for t in tree_species],
                                  weights=[t[1] for t in tree_species])[0]
        x = random.uniform(-500, 500)
        y = random.uniform(-500, 500)
        # Sample the terrain height at this point — approximate from the terrain we know
        # (For the mood render, just put at z=50-150 so they sit above terrain)
        z = random.uniform(50, 200)
        scale = random.uniform(0.8, 1.5)
        import_glb(species, location=(x, y, z), scale=(scale, scale, scale))

    # 7. Gate at the SE entrance
    import_glb(f"{LOWPOLY}/lqv_lowpoly_gate.glb",
               location=(450, 300, 50),
               scale=(2, 2, 2))

    # 8. Trail through the property
    import_glb(f"{LOWPOLY}/lqv_lowpoly_trail.glb",
               location=(0, 0, 60),
               scale=(8, 8, 1))

    # 9. Lighting (3-point + ambient for cel-shading feel)
    # Sun
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 50))
    sun = bpy.context.object
    sun.name = "Sun"
    sun.data.energy = 4.0
    sun.data.color = (1.0, 0.95, 0.85)  # warm
    sun.rotation_euler = (0.7, 0.4, 0.3)
    # Ambient (use AREA lamp pointing down, big diffuse contribution)
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 200))
    ambient = bpy.context.object
    ambient.name = "Ambient"
    ambient.data.energy = 1.5
    ambient.data.color = (0.78, 0.84, 1.0)  # cool sky tint
    ambient.data.size = 50
    # World ambient: bump up the strength too
    bg.inputs[1].default_value = 0.6

    # 10. Render settings
    scene = bpy.context.scene
    try:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    except Exception:
        scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.view_settings.view_transform = 'Standard'

    # Cel-shading: enable EEVEE's "look dev" mode for flat-shaded look
    try:
        scene.eevee.use_taa = True
        scene.eevee.taa_render_samples = 16
    except Exception:
        pass

    # Camera 1: hero shot (aerial view of property)
    bpy.ops.object.camera_add(location=(400, -400, 600), rotation=(0.9, 0, 0.7))
    cam = bpy.context.object
    cam.name = "Cam_Hero"
    cam.data.lens = 35
    scene.camera = cam

    # Camera 2: ground level near gate
    bpy.ops.object.camera_add(location=(420, 280, 70), rotation=(1.4, 0, -2.0))
    cam2 = bpy.context.object
    cam2.name = "Cam_Gate"
    cam2.data.lens = 50

    # Camera 3: looking up at the monte
    bpy.ops.object.camera_add(location=(-200, -200, 50), rotation=(1.0, 0, 0.7))
    cam3 = bpy.context.object
    cam3.name = "Cam_Monte"
    cam3.data.lens = 28

    # Camera 4: aerial oblique (drone shot)
    bpy.ops.object.camera_add(location=(600, 600, 800), rotation=(0.7, 0, -0.8))
    cam4 = bpy.context.object
    cam4.name = "Cam_Drone"
    cam4.data.lens = 24

    return [cam, cam2, cam3, cam4]


def render_all(cameras):
    scene = bpy.context.scene
    labels = ["hero", "gate", "monte", "drone"]
    for cam, label in zip(cameras, labels):
        scene.camera = cam
        out = f"{RENDER_DIR}/moodboard_{label}.png"
        scene.render.filepath = out
        print(f"  Rendering {label}...")
        bpy.ops.render.render(write_still=True)
        print(f"  → {out} ({os.path.getsize(out)/1024:.1f} KB)")


def main():
    print("=" * 60)
    print("LQV 3D World — mood-board render")
    print("=" * 60)
    cams = build_mood_scene()
    render_all(cams)
    print("\nDONE")
    print("Output:")
    for f in sorted(os.listdir(RENDER_DIR)):
        sz = os.path.getsize(f"{RENDER_DIR}/{f}")
        print(f"  {sz/1024:>8.1f} KB  {f}")


if __name__ == "__main__":
    main()
