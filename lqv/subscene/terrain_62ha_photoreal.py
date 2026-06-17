"""Sub-render: photoreal LQV terrain — real DEM + Sentinel-2 albedo blended
with downloaded Poly Haven CC0 PBR ground sets, scattered jacaranda trees,
boulders along the streamline, procedural water, and a sunset HDRI sky.

Replaces the v5 cartoon platforms / icosphere trees / emission stream with
photoreal assets:
  * HDRI         qwantani_sunset_puresky_4k.exr     (sun NW to match albedo)
  * PBR ground   cracked_red_ground_*_4k            (uplands)
                 muddy_tracks_*_4k                  (streambed band)
  * Tree         jacaranda_tree_4k.blend            (purple-flowering)
  * Rocks        rock_moss_set_02_4k.blend          (scatter)
                 boulder_01_4k.blend                (heroes along stream)

Run from project root:

  RENDER_RUN_ID=20260611_dt_run_photoreal \\
  RENDER_CAM_VIEW=oblique RENDER_VARIANT=B \\
    blender --background --python lqv/subscene/terrain_62ha_photoreal.py

Outputs to renders/sub/runs/20260611_dt_run_photoreal_terrain_62ha_photoreal_<view>/<variant>.png.

Invariants:
  * No mutation of lqv.scene / hero composite.
  * RNG seeded once in base.setup(); used here for the scatter only.
  * Camera clip_end forced 20 km — parcel is 900 m wide, default 100 m clips.
"""
from __future__ import annotations

import json
import math
import os
import random
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy

from lqv import cameras
from lqv.flora import gedi_canopy, ndvi_density
from lqv.subscene import base

TERRAIN_DIR = os.path.join(_PROJECT_ROOT, "assets", "terrain")
HDRI_DIR = os.path.join(_PROJECT_ROOT, "assets", "hdris")
TEX_DIR = os.path.join(_PROJECT_ROOT, "assets", "textures")
MODEL_DIR = os.path.join(_PROJECT_ROOT, "assets", "models")

# Env overrides for DEM A/B (ALOS AW3D30 vs COP30 etc) without code edits:
#   LQV_DEM_OVERRIDE_PNG  : path to 16-bit heightmap PNG
#   LQV_DEM_OVERRIDE_JSON : path to sidecar JSON (bbox + z range)
# Both default to the ALOS-derived baseline.
def _path_or_default(env: str, default: str) -> str:
    val = os.environ.get(env, "").strip()
    if not val:
        return default
    return val if os.path.isabs(val) else os.path.join(_PROJECT_ROOT, val)


HEIGHT_PNG = _path_or_default(
    "LQV_DEM_OVERRIDE_PNG", os.path.join(TERRAIN_DIR, "escobar_height.png")
)
HEIGHT_JSON = _path_or_default(
    "LQV_DEM_OVERRIDE_JSON", os.path.join(TERRAIN_DIR, "escobar_height.json")
)
ALBEDO_PNG = os.path.join(TERRAIN_DIR, "escobar_albedo.png")

HDRI_PATH = os.path.join(HDRI_DIR, "qwantani_sunset_puresky_4k.exr")
HDRI_STRENGTH = 1.0
HDRI_ROTATION_DEG = 200.0  # rotate so the sun-disc sits in the NW quadrant
                            # (matches the SUN_AZIMUTH_DEG=340 hillshade bake)

GROUND_UPLAND_DIR = os.path.join(TEX_DIR, "cracked_red_ground")
GROUND_LOW_DIR = os.path.join(TEX_DIR, "muddy_tracks")
GROUND_TEX_TILE_M = 6.0  # tile the PBR set every 6 m across the parcel

TREE_BLEND = os.path.join(MODEL_DIR, "jacaranda_tree", "jacaranda_tree_4k.blend")
ROCK_SMALL_BLEND = os.path.join(MODEL_DIR, "rock_moss_set_02", "rock_moss_set_02_4k.blend")
ROCK_HERO_BLEND = os.path.join(MODEL_DIR, "boulder_01", "boulder_01_4k.blend")

WORLD_SIZE = 900.0
SUBDIV_LEVELS = 8
Z_MIN_M = 116.0
Z_EXAGGERATION = 1.5

# Stream centerline — same waypoints as v5 (kept x,y; Z resampled from DEM).
STREAM_WAYPOINTS = [
    (-0.40,  0.45),
    (-0.20,  0.28),
    (-0.02,  0.05),
    ( 0.08, -0.08),
    ( 0.18, -0.22),
    ( 0.25, -0.32),
    ( 0.34, -0.45),
]
STREAM_HALFWIDTH_M = 6.0     # water surface half-width
STREAM_AVOID_M = 28.0        # no trees within this radius of the stream

# Hero pool location — flat water disc on the streambed.
POOL_M = (0.15, -0.18)
POOL_RADIUS_M = 18.0

# Tree scatter — Poisson-jitter grid; trees avoid stream + pool + parcel edges.
# Per-tree scale is now sampled from GEDI L2A canopy heights (see
# lqv/flora/gedi_canopy.py), not a uniform range.
TREE_COUNT_TARGET = 70
TREE_MIN_SPACING_M = 22.0

# Rock scatter — small mossy rocks along the stream; hero boulders at bends.
ROCK_SMALL_COUNT = 36
ROCK_HERO_COUNT = 8
ROCK_SCALE_RANGE = (0.5, 1.4)


# ---------------------------------------------------------------------------
# Heightmap sampler — bit-identical to terrain_62ha.py / honoring the
# Displace modifier output so anything we drop on the surface stays glued.
# ---------------------------------------------------------------------------
_HEIGHTMAP_CACHE = None


def _load_heightmap_grid():
    global _HEIGHTMAP_CACHE
    if _HEIGHTMAP_CACHE is not None:
        return _HEIGHTMAP_CACHE
    img = bpy.data.images.load(HEIGHT_PNG, check_existing=True)
    img.colorspace_settings.name = "Non-Color"
    w, h = img.size
    flat = list(img.pixels)
    grid = [[flat[(y * w + x) * 4] for x in range(w)] for y in range(h)]
    with open(HEIGHT_JSON) as f:
        meta = json.load(f)
    z_range = float(meta["z_max_m"] - meta["z_min_m"])
    _HEIGHTMAP_CACHE = (grid, w, h, z_range)
    return _HEIGHTMAP_CACHE


def _sample_terrain_z(nx: float, ny: float, offset: float = 0.0) -> float:
    grid, w, h, z_range = _load_heightmap_grid()
    nx_c = max(-0.5, min(0.5, nx))
    ny_c = max(-0.5, min(0.5, ny))
    fx = (nx_c + 0.5) * (w - 1)
    fy = (ny_c + 0.5) * (h - 1)
    x0 = int(fx); x1 = min(x0 + 1, w - 1)
    y0 = int(fy); y1 = min(y0 + 1, h - 1)
    tx = fx - x0; ty = fy - y0
    v00 = grid[y0][x0]; v10 = grid[y0][x1]
    v01 = grid[y1][x0]; v11 = grid[y1][x1]
    v0 = v00 * (1.0 - tx) + v10 * tx
    v1 = v01 * (1.0 - tx) + v11 * tx
    v = v0 * (1.0 - ty) + v1 * ty
    return v * z_range * Z_EXAGGERATION + offset


def _local_xy(nx: float, ny: float) -> tuple[float, float]:
    return nx * WORLD_SIZE, ny * WORLD_SIZE


def _dist_to_stream_xy(x: float, y: float) -> float:
    """Minimum 2D distance from (x,y) to any stream segment, in metres."""
    best = float("inf")
    pts = [_local_xy(*p) for p in STREAM_WAYPOINTS]
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:], strict=False):
        dx, dy = x2 - x1, y2 - y1
        seg_len2 = dx * dx + dy * dy
        if seg_len2 == 0.0:
            d2 = (x - x1) ** 2 + (y - y1) ** 2
        else:
            t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / seg_len2))
            px = x1 + t * dx
            py = y1 + t * dy
            d2 = (x - px) ** 2 + (y - py) ** 2
        if d2 < best:
            best = d2
    return math.sqrt(best)


# ---------------------------------------------------------------------------
# Terrain mesh + blended PBR material
# ---------------------------------------------------------------------------
def _build_terrain_mesh():
    with open(HEIGHT_JSON) as f:
        meta = json.load(f)
    z_range = float(meta["z_max_m"] - meta["z_min_m"])

    bpy.ops.mesh.primitive_plane_add(size=WORLD_SIZE, location=(0.0, 0.0, 0.0))
    plane = bpy.context.active_object
    plane.name = "terrain_62ha_photoreal"

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
    disp.strength = z_range * Z_EXAGGERATION
    disp.mid_level = 0.0

    # Auto-smooth shading so the displaced relief reads soft, not faceted.
    bpy.ops.object.shade_smooth()
    if hasattr(plane.data, "use_auto_smooth"):
        plane.data.use_auto_smooth = True
        plane.data.auto_smooth_angle = math.radians(60.0)

    return plane


def _pbr_image(path: str, *, colorspace: str):
    img = bpy.data.images.load(path, check_existing=True)
    img.colorspace_settings.name = colorspace
    return img


def _pbr_node_chain(nt, dir_path: str, prefix: str, *, tile_m: float):
    """Build (base_color_socket, roughness_socket, normal_socket) wired from a
    Poly Haven 4k PBR set living in `dir_path` with files
    {prefix}_diff_4k.jpg, _nor_gl_4k.jpg, _rough_4k.jpg, _ao_4k.jpg,
    _disp_4k.png.  The shared TexCoord+Mapping is also returned so the caller
    can chain a separate scale for blending."""
    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    # Tile the PBR set across the parcel.
    scale = WORLD_SIZE / tile_m
    mapping.inputs["Scale"].default_value = (scale, scale, scale)

    nt.links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])

    diff = nt.nodes.new("ShaderNodeTexImage")
    diff.image = _pbr_image(
        os.path.join(dir_path, f"{prefix}_diff_4k.jpg"), colorspace="sRGB")
    diff.interpolation = "Smart"
    nt.links.new(mapping.outputs["Vector"], diff.inputs["Vector"])

    ao = nt.nodes.new("ShaderNodeTexImage")
    ao.image = _pbr_image(
        os.path.join(dir_path, f"{prefix}_ao_4k.jpg"), colorspace="Non-Color")
    nt.links.new(mapping.outputs["Vector"], ao.inputs["Vector"])

    rough = nt.nodes.new("ShaderNodeTexImage")
    rough.image = _pbr_image(
        os.path.join(dir_path, f"{prefix}_rough_4k.jpg"), colorspace="Non-Color")
    nt.links.new(mapping.outputs["Vector"], rough.inputs["Vector"])

    nor = nt.nodes.new("ShaderNodeTexImage")
    nor.image = _pbr_image(
        os.path.join(dir_path, f"{prefix}_nor_gl_4k.jpg"), colorspace="Non-Color")
    nt.links.new(mapping.outputs["Vector"], nor.inputs["Vector"])

    nor_map = nt.nodes.new("ShaderNodeNormalMap")
    nor_map.inputs["Strength"].default_value = 0.85
    nt.links.new(nor.outputs["Color"], nor_map.inputs["Color"])

    # Multiply diffuse × AO to bake the AO into the base color.
    ao_mix = nt.nodes.new("ShaderNodeMixRGB")
    ao_mix.blend_type = "MULTIPLY"
    ao_mix.inputs["Fac"].default_value = 0.55
    nt.links.new(diff.outputs["Color"], ao_mix.inputs["Color1"])
    nt.links.new(ao.outputs["Color"], ao_mix.inputs["Color2"])

    return (ao_mix.outputs["Color"], rough.outputs["Color"], nor_map.outputs["Normal"])


def _build_terrain_material(plane):
    """PBR ground with two zones (upland red clay vs muddy streambed) blended
    by surface elevation, then tinted with the Sentinel-2 albedo so the real
    crop-pattern from the satellite still drives large-scale color.
    """
    mat = bpy.data.materials.new("Terrain_Photoreal")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()

    upland_color, upland_rough, upland_nor = _pbr_node_chain(
        nt, GROUND_UPLAND_DIR, "cracked_red_ground", tile_m=GROUND_TEX_TILE_M)
    low_color, low_rough, low_nor = _pbr_node_chain(
        nt, GROUND_LOW_DIR, "muddy_tracks", tile_m=GROUND_TEX_TILE_M)

    # Geometry node → world-space position; the Z drives the upland/low blend.
    geom = nt.nodes.new("ShaderNodeNewGeometry")
    sep_xyz = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geom.outputs["Position"], sep_xyz.inputs["Vector"])

    # Map Z=[0..6] m → fac=[1..0]: low Z is muddy, mid/high Z is red clay.
    z_ramp = nt.nodes.new("ShaderNodeMapRange")
    z_ramp.inputs["From Min"].default_value = 0.0
    z_ramp.inputs["From Max"].default_value = 8.0
    z_ramp.inputs["To Min"].default_value = 1.0
    z_ramp.inputs["To Max"].default_value = 0.0
    z_ramp.clamp = True
    nt.links.new(sep_xyz.outputs["Z"], z_ramp.inputs["Value"])

    color_mix = nt.nodes.new("ShaderNodeMixRGB")
    color_mix.blend_type = "MIX"
    nt.links.new(z_ramp.outputs["Result"], color_mix.inputs["Fac"])
    nt.links.new(upland_color, color_mix.inputs["Color1"])
    nt.links.new(low_color, color_mix.inputs["Color2"])

    rough_mix = nt.nodes.new("ShaderNodeMixRGB")
    rough_mix.blend_type = "MIX"
    nt.links.new(z_ramp.outputs["Result"], rough_mix.inputs["Fac"])
    nt.links.new(upland_rough, rough_mix.inputs["Color1"])
    nt.links.new(low_rough, rough_mix.inputs["Color2"])

    # Normal — pick by region; mixing normals is mathematically wrong but for
    # a gentle gradient just selecting the dominant one works fine.
    nor_mix = nt.nodes.new("ShaderNodeMixRGB")
    nor_mix.blend_type = "MIX"
    nt.links.new(z_ramp.outputs["Result"], nor_mix.inputs["Fac"])
    nt.links.new(upland_nor, nor_mix.inputs["Color1"])
    nt.links.new(low_nor, nor_mix.inputs["Color2"])

    # Sentinel-2 albedo overlay — multiplied at low strength so satellite
    # color signature still tints the PBR base.
    if os.path.exists(ALBEDO_PNG):
        albedo_tex = nt.nodes.new("ShaderNodeTexImage")
        albedo_tex.image = _pbr_image(ALBEDO_PNG, colorspace="sRGB")
        # UV mapping = stretched to the parcel — same as the displacement.
        uv = nt.nodes.new("ShaderNodeUVMap")
        nt.links.new(uv.outputs["UV"], albedo_tex.inputs["Vector"])

        sat_mix = nt.nodes.new("ShaderNodeMixRGB")
        sat_mix.blend_type = "MULTIPLY"
        sat_mix.inputs["Fac"].default_value = 0.55
        nt.links.new(color_mix.outputs["Color"], sat_mix.inputs["Color1"])
        nt.links.new(albedo_tex.outputs["Color"], sat_mix.inputs["Color2"])
        final_color = sat_mix.outputs["Color"]
    else:
        final_color = color_mix.outputs["Color"]

    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Metallic"].default_value = 0.0
    nt.links.new(final_color, bsdf.inputs["Base Color"])
    nt.links.new(rough_mix.outputs["Color"], bsdf.inputs["Roughness"])
    nt.links.new(nor_mix.outputs["Color"], bsdf.inputs["Normal"])

    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    plane.data.materials.append(mat)


# ---------------------------------------------------------------------------
# Water — bezier strip riding the displaced surface.
# ---------------------------------------------------------------------------
def _water_material(name: str):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (0.05, 0.10, 0.12, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.08
    bsdf.inputs["Metallic"].default_value = 0.0
    for k in ("Transmission Weight", "Transmission"):
        if k in bsdf.inputs:
            bsdf.inputs[k].default_value = 1.0
            break
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = 1.33
    # Subtle bump from a Noise to break the mirror-flat reflection.
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 3.0
    noise.inputs["Detail"].default_value = 6.0
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.08
    nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def _build_stream():
    curve_data = bpy.data.curves.new("stream_curve", type="CURVE")
    curve_data.dimensions = "3D"
    spline = curve_data.splines.new("BEZIER")
    spline.bezier_points.add(len(STREAM_WAYPOINTS) - 1)
    for bp, (nx, ny) in zip(spline.bezier_points, STREAM_WAYPOINTS, strict=False):
        x, y = _local_xy(nx, ny)
        bp.co = (x, y, _sample_terrain_z(nx, ny, 0.3))
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    curve_data.bevel_depth = STREAM_HALFWIDTH_M
    curve_data.bevel_resolution = 2
    obj = bpy.data.objects.new("stream", curve_data)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(_water_material("StreamWater"))
    return obj


def _build_pool():
    nx, ny = POOL_M
    x, y = _local_xy(nx, ny)
    z_base = _sample_terrain_z(nx, ny, 0.5)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=POOL_RADIUS_M, depth=0.8,
        location=(x, y, z_base), vertices=48,
    )
    pool = bpy.context.active_object
    pool.name = "natural_pool"
    pool.data.materials.append(_water_material("PoolWater"))
    return pool


# ---------------------------------------------------------------------------
# Asset linking (jacaranda + rocks) from downloaded .blend files.
# ---------------------------------------------------------------------------
def _append_object_from_blend(blend_path: str) -> bpy.types.Object:
    """Append the largest mesh object from `blend_path` and return it.

    Poly Haven 4k blends typically ship a single hero object plus a few
    helpers (collection, empty); we pick the mesh object with the highest
    polygon count so we get the actual asset, not a parent empty.
    """
    if not os.path.exists(blend_path):
        raise SystemExit(f"missing asset blend: {blend_path}")
    before = set(bpy.data.objects.keys())
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        data_to.objects = list(data_from.objects)
    new_objs = [bpy.data.objects[n] for n in bpy.data.objects.keys() if n not in before]
    mesh_objs = [o for o in new_objs if o.type == "MESH" and o.data is not None]
    if not mesh_objs:
        raise SystemExit(f"no mesh objects found in {blend_path}")
    mesh_objs.sort(key=lambda o: len(o.data.polygons), reverse=True)
    hero = mesh_objs[0]
    # Link only the hero object — leave the rest unparented in bpy.data
    # (they don't render unless added to a collection).
    for o in new_objs:
        try:
            bpy.context.collection.objects.unlink(o)
        except RuntimeError:
            pass
    bpy.context.collection.objects.link(hero)
    print(f"[asset] appended {hero.name} ({len(hero.data.polygons)} polys) "
          f"from {os.path.basename(blend_path)}")
    return hero


def _instance(template: bpy.types.Object, *, location, scale, rot_z) -> bpy.types.Object:
    """Linked-data duplicate of `template` at world (location, rot, scale)."""
    inst = template.copy()
    # Share mesh data so 70 trees ≠ 70× memory.
    inst.data = template.data
    inst.location = location
    inst.rotation_euler = (0.0, 0.0, rot_z)
    inst.scale = (scale, scale, scale)
    bpy.context.collection.objects.link(inst)
    return inst


def _scatter_trees(template: bpy.types.Object):
    """Poisson-jitter scatter avoiding the streambed and parcel edges."""
    placed = []
    margin = 0.42  # stay inside [-0.42, +0.42] normalized — 76 m off edges
    attempts = 0
    max_attempts = TREE_COUNT_TARGET * 40
    while len(placed) < TREE_COUNT_TARGET and attempts < max_attempts:
        attempts += 1
        nx = random.uniform(-margin, margin)
        ny = random.uniform(-margin, margin)
        x, y = _local_xy(nx, ny)

        if _dist_to_stream_xy(x, y) < STREAM_AVOID_M:
            continue

        # Skip pool footprint.
        px, py = _local_xy(*POOL_M)
        if (x - px) ** 2 + (y - py) ** 2 < (POOL_RADIUS_M + 12.0) ** 2:
            continue

        # Spacing check against already-placed.
        too_close = False
        for (ox, oy) in placed:
            if (x - ox) ** 2 + (y - oy) ** 2 < TREE_MIN_SPACING_M ** 2:
                too_close = True
                break
        if too_close:
            continue

        # Sentinel-2 NDVI canopy gate — reject points that fall on laterite
        # paths / built / water (low NDVI → low density). Aligns scatter with
        # the real Escobar canopy distribution instead of uniform jitter.
        if random.random() > ndvi_density.density_at(nx, ny):
            continue

        z = _sample_terrain_z(nx, ny, -0.2)
        # GEDI L2A canopy-height driver — empirically sampled scale ratio
        # instead of uniform jitter. See lqv/flora/gedi_canopy.py.
        s = gedi_canopy.sample_scale(random)
        rz = random.uniform(0.0, math.tau)
        _instance(template, location=(x, y, z), scale=s, rot_z=rz)
        placed.append((x, y))
    print(f"[scatter] placed {len(placed)} jacaranda instances "
          f"(target {TREE_COUNT_TARGET}, attempts {attempts})")


def _scatter_rocks_small(template: bpy.types.Object):
    """Small mossy rocks along the streamline (within 0.5*STREAM_AVOID_M)."""
    placed = 0
    attempts = 0
    while placed < ROCK_SMALL_COUNT and attempts < ROCK_SMALL_COUNT * 30:
        attempts += 1
        nx = random.uniform(-0.45, 0.45)
        ny = random.uniform(-0.45, 0.45)
        x, y = _local_xy(nx, ny)
        d = _dist_to_stream_xy(x, y)
        if d < 2.0 or d > 0.55 * STREAM_AVOID_M:
            continue
        z = _sample_terrain_z(nx, ny, -0.4)
        s = random.uniform(*ROCK_SCALE_RANGE)
        rz = random.uniform(0.0, math.tau)
        _instance(template, location=(x, y, z), scale=s, rot_z=rz)
        placed += 1
    print(f"[scatter] placed {placed} small mossy rocks")


def _scatter_rocks_hero(template: bpy.types.Object):
    """Hero boulders at the stream bends + around the pool."""
    pool_xy = _local_xy(*POOL_M)
    bend_pts = []
    pts = [_local_xy(*p) for p in STREAM_WAYPOINTS]
    bend_pts.extend(pts[1:-1])      # every interior waypoint
    bend_pts.extend([
        (pool_xy[0] + POOL_RADIUS_M + 6.0, pool_xy[1]),
        (pool_xy[0] - POOL_RADIUS_M - 4.0, pool_xy[1] + 8.0),
    ])
    random.shuffle(bend_pts)
    placed = 0
    for (bx, by) in bend_pts[:ROCK_HERO_COUNT]:
        # Jitter slightly off the waypoint.
        ox = bx + random.uniform(-8.0, 8.0)
        oy = by + random.uniform(-8.0, 8.0)
        nx, ny = ox / WORLD_SIZE, oy / WORLD_SIZE
        z = _sample_terrain_z(nx, ny, -0.6)
        s = random.uniform(0.7, 1.6)
        rz = random.uniform(0.0, math.tau)
        _instance(template, location=(ox, oy, z), scale=s, rot_z=rz)
        placed += 1
    print(f"[scatter] placed {placed} hero boulders")


# ---------------------------------------------------------------------------
# HDRI world — replaces base.setup_world's diagrammatic sky+sun.
# ---------------------------------------------------------------------------
def _setup_hdri_world(scene):
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()

    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Rotation"].default_value = (
        0.0, 0.0, math.radians(HDRI_ROTATION_DEG))

    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(HDRI_PATH, check_existing=True)

    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = HDRI_STRENGTH

    out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])

    # Bias the sky for outdoor shots — turn off the flat-shaded ambient.
    if hasattr(scene, "view_settings"):
        # AgX Punchy stays from engine.setup_color_management; nothing to do.
        pass


# ---------------------------------------------------------------------------
# Camera presets — match v5 so renders are directly comparable.
# ---------------------------------------------------------------------------
_CAM_VIEWS = {
    "birdseye": dict(location=(600.0, -600.0, 600.0),
                     look_at=(0.0, 0.0, 60.0),
                     lens=35.0, ortho=None),
    "plan":     dict(location=(0.0, 0.0, 1500.0),
                     look_at=(0.0, 0.0, 60.0),
                     lens=35.0, ortho=1000.0),
    "oblique":  dict(location=(500.0, -500.0, 320.0),
                     look_at=(0.0, 0.0, 80.0),
                     lens=35.0, ortho=None),
}


def _build():
    plane = _build_terrain_mesh()
    _build_terrain_material(plane)
    _build_stream()
    _build_pool()

    tree_template = _append_object_from_blend(TREE_BLEND)
    _scatter_trees(tree_template)

    small_rock_template = _append_object_from_blend(ROCK_SMALL_BLEND)
    _scatter_rocks_small(small_rock_template)

    hero_rock_template = _append_object_from_blend(ROCK_HERO_BLEND)
    _scatter_rocks_hero(hero_rock_template)


if __name__ == "__main__":
    view_key = os.environ.get("RENDER_CAM_VIEW", "oblique")
    if view_key not in _CAM_VIEWS:
        raise SystemExit(f"unknown RENDER_CAM_VIEW={view_key!r}; "
                         f"expected one of {sorted(_CAM_VIEWS)}")
    os.environ.setdefault("RENDER_RUN_TAG", view_key)

    scene, cfg = base.setup("terrain_62ha_photoreal")
    _build()
    _setup_hdri_world(scene)

    view = _CAM_VIEWS[view_key]
    cam = cameras.add_camera(
        "Cam_Photoreal",
        location=view["location"],
        look_at=view["look_at"],
        lens=view["lens"],
    )
    if view["ortho"] is not None:
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = view["ortho"]
    cam.data.clip_start = 1.0
    cam.data.clip_end = base.PARCEL_CLIP_END_M
    scene.camera = cam
    print(f"[terrain_62ha_photoreal] view={view_key} → {view['location']}")
    base.save_subrender(scene, "terrain_62ha_photoreal", cfg)
