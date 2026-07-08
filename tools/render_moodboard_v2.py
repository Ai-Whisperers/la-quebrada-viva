#!/usr/bin/env python3
"""LQV 3D World — mood-board render (v2, better composition).

The first version had the camera in the wrong place relative to the scene.
This one centers on the parcel centroid (-57.030, -25.630) with the terrain
scaled correctly and assets placed relative to that anchor.

Units convention: 1 unit = 1 meter.
- Terrain mesh is 160×108m. We'll position it so the parcel centroid is at origin.
- Monte at NW (relative to property).
- Cob house at the planned buildable spot.
- Trees scattered in a 1km radius.
- Camera at human-eye level (1.7m) looking around the property.
"""
import bpy
import os

OUT_DIR = "/root/la-quebrada-viva/docs/game_assets/lowpoly"
RENDER_DIR = "/root/la-quebrada-viva/docs/game_assets/lowpoly_renders"
os.makedirs(RENDER_DIR, exist_ok=True)


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_glb(path, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
    before = set(o.name for o in bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new_objs = [o for o in bpy.data.objects if o.name not in before]
    for o in new_objs:
        o.location = location
        o.rotation_euler = rotation
        o.scale = scale
    return new_objs


def build_mood_scene():
    reset_scene()

    # Sky
    world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.910, 0.847, 0.690, 1.0)
    bpy.context.scene.world = world

    # === TERRAIN ===
    # The 16-bit PNG encodes 160x108m. To cover the ~3km context, scale 12x.
    # That makes the mesh ~1.9km wide which is the 10km box half-width. Good.
    # Place the mesh so its center is at origin.
    terrain_objs = import_glb(f"{OUT_DIR}/lqv_lowpoly_terrain.glb")
    # Apply 12x scale in X+Y, keep Z at original (1m = 1m, no exaggeration needed since
    # the original terrain was already in 1m = 1m units after /100 decoding).
    for o in terrain_objs:
        o.scale = (12, 12, 1)  # 12x bigger in plan, no vertical exaggeration
        # The terrain mesh origin is at (0,0,0) in Blender. After 12x scale, it extends
        # from (-960, -648) to (960, 648) roughly. That's a 1.9km × 1.3km box. Good.

    # === MONTE (escarpment) ===
    # The LQV monte is in the NW quadrant (per operator's GPS data).
    # Mount scale 1x in Blender = 12m tall. At scale 5x = 60m. That's the visible
    # monte in the real terrain.
    import_glb(f"{OUT_DIR}/lqv_lowpoly_monte.glb",
               location=(-700, -400, 80),
               rotation=(0, 0, 0.4),
               scale=(50, 50, 6))  # 50x in plan to spread it across the ridge, 6x vertical

    # === WATERFALL ===
    # The LQV quebrada runs through the property. Place waterfall where the
    # elevation step is steepest. Real elevation drop is ~60m over ~200m horizontally.
    import_glb(f"{OUT_DIR}/lqv_lowpoly_waterfall.glb",
               location=(-100, 250, 50),
               scale=(3, 3, 5))  # 15m tall waterfall

    # === COB HOUSE ===
    # The flagship typology, at the planned buildable spot.
    # Place in middle of the property at the elevation median.
    house_objs = import_glb(f"{OUT_DIR}/lqv_lowpoly_house_cob.glb",
                             location=(200, 0, 90),
                             scale=(3, 3, 3))  # ~12m wide

    # === TATAKUA (outdoor oven) ===
    import_glb(f"{OUT_DIR}/lqv_lowpoly_typo_tatakua.glb",
               location=(280, 80, 90),
               scale=(2, 2, 2))

    # === WORKER HOUSING ===
    import_glb(f"{OUT_DIR}/lqv_lowpoly_typo_worker.glb",
               location=(300, -80, 90),
               scale=(1.5, 1.5, 1.5))

    # === GLAMPING TENT ===
    import_glb(f"{OUT_DIR}/lqv_lowpoly_typo_glamping.glb",
               location=(-200, -50, 100),
               scale=(2, 2, 2))

    # === WIGWAM ===
    import_glb(f"{OUT_DIR}/lqv_lowpoly_typo_wigwam.glb",
               location=(-300, 100, 100),
               scale=(2, 2, 2))

    # === SCATTERED TREES ===
    # 40 trees in a 1.2km radius, biased to avoid the parcel center (keep that clear)
    import random
    random.seed(42)
    species_pool = [
        ("lqv_lowpoly_tree_lapacho.glb", 0.45),  # most common (Atlantic Forest)
        ("lqv_lowpoly_tree_pino.glb", 0.35),
        ("lqv_lowpoly_tree_palmera.glb", 0.20),  # rarer (only near water)
    ]
    for _ in range(40):
        # Polar sampling
        angle = random.uniform(0, 2 * 3.14159)
        # Bias radius: avoid center (parcel), more density at outer ring
        r = random.uniform(400, 900)
        x = r * __import__("math").cos(angle)
        y = r * __import__("math").sin(angle)
        # Sample z at this position — approximate from elevation range
        # (lower near the quebrada, higher near monte)
        if y > 100:
            z = random.uniform(20, 60)  # quebrada corridor (lower)
        elif x < -400:
            z = random.uniform(60, 130)  # monte zone (higher)
        else:
            z = random.uniform(40, 100)
        species = random.choices([s[0] for s in species_pool],
                                  weights=[s[1] for s in species_pool])[0]
        scale = random.uniform(0.8, 1.4)
        import_glb(f"{OUT_DIR}/{species}", location=(x, y, z), scale=(scale, scale, scale))

    # === ROCK CLUSTERS on the cliffs ===
    for i, (x, y, z) in enumerate([(-650, -350, 90), (-600, -380, 100), (-700, -300, 80)]):
        import_glb(f"{OUT_DIR}/lqv_lowpoly_rock_cluster.glb",
                   location=(x, y, z),
                   scale=(15, 15, 8))

    # === TRAIL (Wes's walked path) ===
    import_glb(f"{OUT_DIR}/lqv_lowpoly_trail.glb",
               location=(0, 0, 60),
               scale=(15, 15, 1))

    # === GATE ===
    import_glb(f"{OUT_DIR}/lqv_lowpoly_gate.glb",
               location=(400, 300, 60),
               rotation=(0, 0, -0.5),
               scale=(3, 3, 3))

    # === LIGHTING ===
    # Warm sun (golden hour vibe — Zelda aesthetic)
    # Delete any pre-existing Sun from factory scene
    for o in list(bpy.data.objects):
        if o.name in ("Sun", "Hemi", "Light"):
            bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.object.light_add(type='SUN', location=(100, 100, 80))
    sun = bpy.context.object
    sun.data.energy = 5.0
    sun.data.color = (1.0, 0.92, 0.78)
    sun.rotation_euler = (1.2, -0.3, 0.4)

    # Ambient sky fill
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 300))
    ambient = bpy.context.object
    ambient.data.energy = 1.8
    ambient.data.color = (0.85, 0.92, 1.0)
    ambient.data.size = 80

    # === RENDER SETTINGS ===
    scene = bpy.context.scene
    try:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    except Exception:
        scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.view_settings.view_transform = 'Standard'
    try:
        scene.eevee.use_taa = True
        scene.eevee.taa_render_samples = 32
    except Exception:
        pass

    # === CAMERAS ===
    # The terrain mesh has Z from 116m to 395m (real elevation). X from 0 to 107m,
    # Y from -179 to 0m. Scale 12x → mesh spans X:0-1284, Y:-2148-0, Z:116-395.
    # Camera should be HIGH (z ~ 400-500) looking down at the terrain.

    # Camera 1: Hero — bird's-eye oblique from SW corner, looking NE down
    bpy.ops.object.camera_add(location=(1500, -1200, 600), rotation=(0.85, 0, -1.0))
    cam_hero = bpy.context.object
    cam_hero.data.lens = 35
    cam_hero.name = "Cam_Hero"
    scene.camera = cam_hero

    # Camera 2: Ground-level near the cob house (human eye at ~1.7m above terrain)
    # House is at (200, 0, 90) in 12x scaled space. Camera at (300, -100, 220) looking NE.
    bpy.ops.object.camera_add(location=(300, -100, 240), rotation=(1.45, 0, 0.3))
    cam_house = bpy.context.object
    cam_house.data.lens = 40
    cam_house.name = "Cam_House"

    # Camera 3: Looking at the monte (monte is at (-700, -400, 80) base,
    # peak at z~150 with scale). Camera in middle of property looking W.
    bpy.ops.object.camera_add(location=(200, -300, 260), rotation=(1.0, 0, -1.6))
    cam_monte = bpy.context.object
    cam_monte.data.lens = 32
    cam_monte.name = "Cam_Monte"

    # Camera 4: Near the waterfall / quebrada corridor
    bpy.ops.object.camera_add(location=(-200, 200, 200), rotation=(1.2, 0, -2.5))
    cam_falls = bpy.context.object
    cam_falls.data.lens = 45
    cam_falls.name = "Cam_Falls"

    return [cam_hero, cam_house, cam_monte, cam_falls]


def render_all(cameras):
    scene = bpy.context.scene
    labels = ["hero", "house", "monte", "falls"]
    for cam, label in zip(cameras, labels):
        scene.camera = cam
        out = f"{RENDER_DIR}/moodboard_v2_{label}.png"
        scene.render.filepath = out
        print(f"  Rendering {label}...")
        bpy.ops.render.render(write_still=True)
        print(f"  → {out} ({os.path.getsize(out)/1024:.1f} KB)")


def main():
    print("=" * 60)
    print("LQV 3D World — mood-board render v2")
    print("=" * 60)
    cams = build_mood_scene()
    render_all(cams)
    print("\nDONE")
    print("Output:")
    for f in sorted(os.listdir(RENDER_DIR)):
        if f.startswith("moodboard_v2"):
            sz = os.path.getsize(f"{RENDER_DIR}/{f}")
            print(f"  {sz/1024:>8.1f} KB  {f}")


if __name__ == "__main__":
    main()
