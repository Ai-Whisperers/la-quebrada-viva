"""Sub-render: 62-ha digital-twin terrain with features.

Standalone preview of the LQV parcel — mesh-displaced ALOS heightmap,
Sentinel-2 RGB ground texture, stream centerline, cascade band, pool
marker, candidate platforms. Read-only on the hero scene.

Run from project root (Blender 4.2.3+):

  blender --background --python lqv/subscene/terrain_62ha.py -- \\
      [RENDER_VARIANT=A|B|C] [RENDER_CAM=hero] [RENDER_SAMPLES=128]

Or just smoke-test the build without rendering:

  RENDER_SKIP=1 blender --background --python lqv/subscene/terrain_62ha.py

Outputs to renders/sub/terrain_62ha_<variant>.png.

Inputs (built by scripts/make_terrain_{heightmap,albedo}.py):
  assets/terrain/escobar_height.png   16-bit normalized DEM
  assets/terrain/escobar_height.json  bbox + z range sidecar
  assets/terrain/escobar_albedo.png   Sentinel-2 RGB albedo (optional)

Invariants:
  • No random.* calls — purely deterministic geometry.
  • No imports from lqv.site or lqv.scene — sub-render-first; the
    dormant lqv/site/terrain_62ha.py stub stays untouched.
  • with_ground=False — the terrain IS the ground.
"""
from __future__ import annotations

import json
import math
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy

from lqv import cameras
from lqv.subscene import base

TERRAIN_DIR = os.path.join(_PROJECT_ROOT, "assets", "terrain")
HEIGHT_PNG = os.path.join(TERRAIN_DIR, "escobar_height.png")
HEIGHT_JSON = os.path.join(TERRAIN_DIR, "escobar_height.json")
ALBEDO_PNG = os.path.join(TERRAIN_DIR, "escobar_albedo.png")

WORLD_SIZE = 3000.0
SUBDIV_LEVELS = 7

# Heightmap displaces the ground plane from z=0 upward; world z therefore
# spans [0, Z_RANGE_M], not the original [Z_MIN_M, Z_MAX_M]. Subtract Z_MIN_M
# from any elevation we want to anchor to the surface.
Z_MIN_M = 116.0

# Hand-routed stream waypoints in normalized parcel coords (x,y in [-0.5,0.5],
# z = original elevation in m above sea). Headwaters → cascade band → pool →
# outlet, matched to the SITE_DIAGNOSTIC.md elevations.
STREAM_WAYPOINTS_M = [
    (-0.40,  0.45, 380.0),
    (-0.20,  0.28, 320.0),
    (-0.02,  0.05, 270.0),
    ( 0.08, -0.08, 220.0),
    ( 0.18, -0.22, 145.0),
    ( 0.25, -0.32, 125.0),
    ( 0.34, -0.45, 116.0),
]

POOL_M = (0.20, -0.25, 122.0)

PLATFORMS_M = [
    (-0.15, -0.05, 155.0, "platform_A"),
    ( 0.05,  0.05, 145.0, "platform_B"),
    ( 0.18,  0.12, 135.0, "platform_C"),
]

# Feature scales — oversized so they read at the 3 km parcel scale (1.6 m / px
# at 1280×720). Real-world dimensions are documented in SITE_DIAGNOSTIC.md;
# these markers are for orientation only.
STREAM_BEVEL_M = 30.0
POOL_RADIUS_M = 60.0
PLATFORM_SIZE_M = 80.0
NORTH_ARROW_RADIUS_M = 70.0
NORTH_ARROW_DEPTH_M = 180.0


def _local_xy(nx: float, ny: float) -> tuple[float, float]:
    """Normalized parcel coord → Blender world coord."""
    return nx * WORLD_SIZE, ny * WORLD_SIZE


def _emission_material(name: str, rgb: tuple[float, float, float], strength: float):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
    em.inputs["Strength"].default_value = strength
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return mat


def _build_terrain_block():
    with open(HEIGHT_JSON) as f:
        meta = json.load(f)
    z_range = float(meta["z_max_m"] - meta["z_min_m"])

    bpy.ops.mesh.primitive_plane_add(size=WORLD_SIZE, location=(0.0, 0.0, 0.0))
    plane = bpy.context.active_object
    plane.name = "terrain_62ha"

    sub = plane.modifiers.new("Sub", "SUBSURF")
    sub.subdivision_type = "SIMPLE"
    sub.levels = SUBDIV_LEVELS
    sub.render_levels = SUBDIV_LEVELS

    img = bpy.data.images.load(HEIGHT_PNG)
    tex = bpy.data.textures.new("HeightTex", type="IMAGE")
    tex.image = img
    tex.extension = "EXTEND"

    disp = plane.modifiers.new("Disp", "DISPLACE")
    disp.texture = tex
    disp.texture_coords = "UV"
    disp.strength = z_range
    disp.mid_level = 0.0
    return plane


def _build_ground_material(plane):
    mat = bpy.data.materials.new("Terrain_Albedo")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = 0.85
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    if os.path.exists(ALBEDO_PNG):
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(ALBEDO_PNG)
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (0.30, 0.40, 0.22, 1.0)
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    plane.data.materials.append(mat)


def _build_stream():
    curve_data = bpy.data.curves.new("stream_centerline", type="CURVE")
    curve_data.dimensions = "3D"
    spline = curve_data.splines.new("BEZIER")
    spline.bezier_points.add(len(STREAM_WAYPOINTS_M) - 1)
    for bp, (nx, ny, z_m) in zip(spline.bezier_points, STREAM_WAYPOINTS_M):
        x, y = _local_xy(nx, ny)
        bp.co = (x, y, (z_m - Z_MIN_M) + 6.0)
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    curve_data.bevel_depth = STREAM_BEVEL_M
    curve_data.bevel_resolution = 3
    obj = bpy.data.objects.new("stream_centerline", curve_data)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(_emission_material("Stream", (0.15, 0.45, 0.95), 6.0))
    return obj


def _build_pool():
    nx, ny, z_m = POOL_M
    x, y = _local_xy(nx, ny)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=POOL_RADIUS_M, depth=8.0,
        location=(x, y, (z_m - Z_MIN_M) + 6.0))
    pool = bpy.context.active_object
    pool.name = "flat_rock_pool"
    pool.data.materials.append(_emission_material("Pool", (0.25, 0.85, 0.95), 10.0))
    return pool


def _build_platforms():
    objs = []
    for nx, ny, z_m, name in PLATFORMS_M:
        x, y = _local_xy(nx, ny)
        bpy.ops.mesh.primitive_plane_add(
            size=PLATFORM_SIZE_M, location=(x, y, (z_m - Z_MIN_M) + 8.0))
        plat = bpy.context.active_object
        plat.name = name
        plat.data.materials.append(
            _emission_material(f"Plat_{name}", (1.0, 0.95, 0.6), 12.0))
        objs.append(plat)
    return objs


def _build_north_arrow():
    """Floating marker so renders are oriented at a glance."""
    z_top_m = 380.0 - Z_MIN_M + 80.0  # above the highest terrain
    bpy.ops.mesh.primitive_cone_add(
        radius1=NORTH_ARROW_RADIUS_M, radius2=0.0, depth=NORTH_ARROW_DEPTH_M,
        location=(0.0, WORLD_SIZE * 0.46, z_top_m),
        rotation=(math.radians(180.0), 0.0, 0.0),
    )
    arrow = bpy.context.active_object
    arrow.name = "north_arrow"
    arrow.data.materials.append(_emission_material("North", (1.0, 0.2, 0.2), 15.0))
    return arrow


def _build():
    plane = _build_terrain_block()
    _build_ground_material(plane)
    _build_stream()
    _build_pool()
    _build_platforms()
    _build_north_arrow()


if __name__ == "__main__":
    # Inline of base.run — needed so we can override camera clip_end. The
    # parcel is 3 km wide and the bird's-eye camera sits ~4 km above the
    # surface, well past Blender's default 100 m far clip plane.
    scene, cfg = base.setup("terrain_62ha")
    _build()
    print(f"[terrain_62ha] scene objs: {sorted(o.name for o in scene.objects)}")
    base.setup_world(scene, cfg.variant)
    cam = cameras.add_camera(
        "Cam_Subscene",
        location=(300.0, -300.0, 4200.0),
        look_at=(0.0, 0.0, 100.0),
        lens=28.0,
    )
    cam.data.clip_start = 1.0
    cam.data.clip_end = 20000.0
    scene.camera = cam
    base.save_subrender(scene, "terrain_62ha", cfg)
