"""Sub-render: 62-ha digital-twin terrain with features.

v5 (2026-06-11): redesign over v4 — fixes stream-wall bug + toy geometry.
  * Stream follows the cropped terrain surface (sampled from heightmap),
    not the original sea-level waypoints. v4 anchored Z=380 m at the
    headwaters of the parent 3 km topography, producing a 400 m vertical
    water tube above the 82 m parcel terrain.
  * Trees rebuilt as trunk-cylinder + flattened crown ico-sphere, not
    bare dot primitives.
  * Platforms rebuilt as rectangular cob footprint + pitched gable roof,
    not mushroom dome+cone.
  * Pool moved inward off the parcel edge.
  * Gradient sky world replaces flat slate gray.
  * Albedo gain bumped 5.5 → 9.0 in scripts/make_terrain_albedo.py.
  * North arrow sunk to terrain surface at the NE edge.

Standalone preview of the LQV parcel — mesh-displaced ALOS heightmap,
Sentinel-2 RGB ground texture, stream centerline, pool marker, candidate
platforms. Read-only on the hero scene.

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
  * No random.* calls — purely deterministic geometry. Tree scatter uses
    fixed golden-angle offsets around hand-routed anchors.
  * No imports from lqv.site or lqv.scene — sub-render-first; the
    dormant lqv/site/terrain_62ha.py stub stays untouched.
  * with_ground=False — the terrain IS the ground.
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

WORLD_SIZE = 900.0
SUBDIV_LEVELS = 8

# Heightmap displaces the ground plane from z=0 upward; world z therefore
# spans [0, Z_RANGE_M * Z_EXAGGERATION], not the original [Z_MIN_M, Z_MAX_M].
# Use _anchor_z() to map any real-world elevation to local Blender z.
Z_MIN_M = 116.0

# Vertical relief amplification. The cropped parcel only has ~43 m of relief
# across 900 m — at 1:1 that reads as a near-flat plate. 1.5x lifts slopes
# enough to be legible without distorting feature elevations beyond plausibility.
Z_EXAGGERATION = 1.5

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

POOL_M = (0.15, -0.18, 122.0)

PLATFORMS_M = [
    (-0.15, -0.05, 155.0, "platform_A"),
    ( 0.05,  0.05, 145.0, "platform_B"),
    ( 0.18,  0.12, 135.0, "platform_C"),
]

# Riparian + vegetation-zone tree cluster anchors.
# (nx, ny, z_m_anchor, count, spread_radius_m). All inside the 900m parcel.
TREE_CLUSTERS_M = [
    (-0.32,  0.38, 360.0, 5, 18.0),
    (-0.10,  0.12, 290.0, 6, 22.0),
    ( 0.04, -0.04, 250.0, 5, 20.0),
    ( 0.16, -0.18, 160.0, 7, 26.0),
    ( 0.28, -0.36, 122.0, 6, 24.0),
    (-0.30, -0.30, 135.0, 6, 28.0),
    ( 0.40,  0.20, 200.0, 4, 18.0),
]
TREE_TRUNK_RADIUS_M = 1.4
TREE_TRUNK_HEIGHT_M = 9.0
TREE_CROWN_RADIUS_M = 8.0
TREE_CROWN_FLATTEN = 0.55

# Feature scales — tuned for the 900 m parcel-focused crop (v3 HD).
# v5 drops STREAM_BEVEL_M 8.0→2.5 (the 8 m was reading as a fat pipe).
STREAM_BEVEL_M = 2.5
POOL_RADIUS_M = 35.0
POOL_RING_THICKNESS_M = 6.0
PLATFORM_FOOTPRINT_X_M = 28.0
PLATFORM_FOOTPRINT_Y_M = 22.0
PLATFORM_WALL_HEIGHT_M = 10.0
PLATFORM_ROOF_HEIGHT_M = 9.0
PLATFORM_ROOF_EAVE_M = 3.5
PLATFORM_LABEL_OFFSET_M = 14.0
PLATFORM_LABEL_SIZE_M = 30.0
NORTH_ARROW_RADIUS_M = 15.0
NORTH_ARROW_DEPTH_M = 35.0
BOUNDARY_THICKNESS_M = 8.0


def _anchor_z(z_m: float, offset: float = 0.0) -> float:
    """Convert a real-world elevation (m above sea) to local Blender z,
    accounting for the displaced-from-zero terrain and Z_EXAGGERATION.

    v5 retains this helper for the parcel boundary only — all surface
    features now sit on the actual cropped relief via _sample_terrain_z()."""
    return (z_m - Z_MIN_M) * Z_EXAGGERATION + offset


def _local_xy(nx: float, ny: float) -> tuple[float, float]:
    """Normalized parcel coord → Blender world coord."""
    return nx * WORLD_SIZE, ny * WORLD_SIZE


_HEIGHTMAP_CACHE = None


def _load_heightmap_grid():
    """Load the displaced heightmap into a flat row-major float grid, once.
    Returns (grid: list[list[float]], width, height, z_range_m)."""
    global _HEIGHTMAP_CACHE
    if _HEIGHTMAP_CACHE is not None:
        return _HEIGHTMAP_CACHE
    img = bpy.data.images.load(HEIGHT_PNG, check_existing=True)
    img.colorspace_settings.name = "Non-Color"
    w, h = img.size
    flat = list(img.pixels)
    # Blender image origin is bottom-left, row-major, RGBA — red channel
    # carries the height value (16-bit PNG normalised to 0..1 floats).
    grid = [[flat[(y * w + x) * 4] for x in range(w)] for y in range(h)]
    with open(HEIGHT_JSON) as f:
        meta = json.load(f)
    z_range = float(meta["z_max_m"] - meta["z_min_m"])
    _HEIGHTMAP_CACHE = (grid, w, h, z_range)
    return _HEIGHTMAP_CACHE


def _sample_terrain_z(nx: float, ny: float, offset: float = 0.0) -> float:
    """Bilinearly sample the displaced-terrain surface at normalized parcel
    coords (nx, ny ∈ [-0.5, 0.5]) and return the local Blender Z that the
    Displace modifier produces, plus an optional surface offset.

    The displace modifier samples the same heightmap over UV(0..1) and
    multiplies by `z_range * Z_EXAGGERATION` from z=0 upward, so sampling
    here the same way guarantees features sit on the rendered surface."""
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


def _principled_material(name, base_color, *, roughness=0.7, metallic=0.0,
                         transmission=0.0, ior=1.45):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (
        base_color[0], base_color[1], base_color[2], 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    # Blender 4.2 renamed Transmission inputs; guard both keys.
    for k in ("Transmission Weight", "Transmission"):
        if k in bsdf.inputs:
            bsdf.inputs[k].default_value = transmission
            break
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = ior
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def _water_material(name, tint):
    """Tinted glassy water — transmission BSDF mixed with faint emission so
    it still reads under low ambient light in the diagrammatic world."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (tint[0], tint[1], tint[2], 1.0)
    bsdf.inputs["Roughness"].default_value = 0.08
    bsdf.inputs["Metallic"].default_value = 0.0
    for k in ("Transmission Weight", "Transmission"):
        if k in bsdf.inputs:
            bsdf.inputs[k].default_value = 0.85
            break
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = 1.33
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (tint[0], tint[1], tint[2], 1.0)
    em.inputs["Strength"].default_value = 1.6
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs["Fac"].default_value = 0.35
    nt.links.new(bsdf.outputs["BSDF"], mix.inputs[1])
    nt.links.new(em.outputs["Emission"], mix.inputs[2])
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
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
    disp.strength = z_range * Z_EXAGGERATION
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
    """Bezier curve following the cropped parcel surface. v5 ignores the
    original sea-level waypoint Z (only x,y carry the route) and samples
    the displaced heightmap so the stream rides ~1.5 m above the local
    relief — fixes the v4 stream-wall bug."""
    curve_data = bpy.data.curves.new("stream_centerline", type="CURVE")
    curve_data.dimensions = "3D"
    spline = curve_data.splines.new("BEZIER")
    spline.bezier_points.add(len(STREAM_WAYPOINTS_M) - 1)
    for bp, (nx, ny, _z_unused) in zip(spline.bezier_points, STREAM_WAYPOINTS_M, strict=False):
        x, y = _local_xy(nx, ny)
        bp.co = (x, y, _sample_terrain_z(nx, ny, 1.5))
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    curve_data.bevel_depth = STREAM_BEVEL_M
    curve_data.bevel_resolution = 3
    obj = bpy.data.objects.new("stream_centerline", curve_data)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(_water_material("Stream", (0.12, 0.42, 0.78)))
    return obj


def _build_pool():
    """Stone ring + flat water disc. v5 anchors on the sampled surface
    rather than the sea-level waypoint Z, so the pool sits on the real
    cropped relief regardless of where the displacement places it."""
    nx, ny, _z_unused = POOL_M
    x, y = _local_xy(nx, ny)
    z_base = _sample_terrain_z(nx, ny, 0.0)

    bpy.ops.mesh.primitive_torus_add(
        major_radius=POOL_RADIUS_M,
        minor_radius=POOL_RING_THICKNESS_M,
        location=(x, y, z_base + 1.5),
        major_segments=48, minor_segments=12,
    )
    ring = bpy.context.active_object
    ring.name = "pool_ring"
    ring.data.materials.append(_principled_material(
        "PoolRing", (0.55, 0.52, 0.48), roughness=0.85))

    bpy.ops.mesh.primitive_cylinder_add(
        radius=POOL_RADIUS_M - 1.5, depth=3.0,
        location=(x, y, z_base + 3.0))
    pool = bpy.context.active_object
    pool.name = "flat_rock_pool"
    pool.data.materials.append(_water_material("PoolWater", (0.18, 0.55, 0.82)))
    return pool


def _build_platforms():
    """v5: rectangular cob house markers — extruded cuboid walls + pitched
    gable roof (triangular-prism mesh) + floating 3D text label. Reads as
    'small village hall' at parcel scale instead of the v4 mushroom dome."""
    objs = []
    cob_mat = _principled_material(
        "Cob_Walls", (0.78, 0.68, 0.52), roughness=0.92)
    roof_mat = _principled_material(
        "Terracotta_Roof", (0.72, 0.32, 0.20), roughness=0.78)
    label_mat = _emission_material("Platform_Label", (1.0, 1.0, 0.85), 8.0)

    hx = PLATFORM_FOOTPRINT_X_M * 0.5
    hy = PLATFORM_FOOTPRINT_Y_M * 0.5
    wall_h = PLATFORM_WALL_HEIGHT_M
    roof_h = PLATFORM_ROOF_HEIGHT_M
    eave = PLATFORM_ROOF_EAVE_M

    for nx, ny, _z_unused, name in PLATFORMS_M:
        x, y = _local_xy(nx, ny)
        z_base = _sample_terrain_z(nx, ny, 0.0)

        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=(x, y, z_base + wall_h * 0.5),
        )
        walls = bpy.context.active_object
        walls.name = name
        walls.scale = (PLATFORM_FOOTPRINT_X_M, PLATFORM_FOOTPRINT_Y_M, wall_h)
        bpy.ops.object.transform_apply(scale=True)
        walls.data.materials.append(cob_mat)
        objs.append(walls)

        # Pitched gable roof: triangular prism — 6 verts, eaves overhang by
        # PLATFORM_ROOF_EAVE_M on the long sides; ridge runs along +X.
        rx = hx + eave
        ry = hy + eave
        zb = z_base + wall_h
        zt = zb + roof_h
        roof_verts = [
            (-rx, -ry, zb), ( rx, -ry, zb),
            ( rx,  ry, zb), (-rx,  ry, zb),
            (-rx,  0.0, zt), ( rx,  0.0, zt),
        ]
        roof_faces = [
            (0, 1, 5, 4),     # south slope
            (1, 2, 5),        # east gable
            (2, 3, 4, 5),     # north slope
            (3, 0, 4),        # west gable
            (0, 3, 2, 1),     # underside (faces down)
        ]
        roof_mesh = bpy.data.meshes.new(f"{name}_roof_mesh")
        roof_mesh.from_pydata(roof_verts, [], roof_faces)
        roof_mesh.update()
        roof_obj = bpy.data.objects.new(f"{name}_roof", roof_mesh)
        bpy.context.collection.objects.link(roof_obj)
        roof_obj.data.materials.append(roof_mat)
        objs.append(roof_obj)

        bpy.ops.object.text_add(
            location=(x, y, zt + PLATFORM_LABEL_OFFSET_M),
        )
        label = bpy.context.active_object
        label.name = f"{name}_label"
        letter = name.rsplit("_", 1)[-1]
        label.data.body = letter
        label.data.size = PLATFORM_LABEL_SIZE_M
        label.data.align_x = "CENTER"
        label.data.align_y = "CENTER"
        label.data.extrude = 1.2
        label.rotation_euler = (math.radians(90.0), 0.0, 0.0)
        label.data.materials.append(label_mat)
        objs.append(label)
    return objs


def _build_tree_clusters():
    """v5: riparian + vegetation-zone tree proxies as trunk + crown pairs.
    Deterministic golden-angle spiral per cluster anchor. Trunk = brown bark
    cylinder; crown = flattened ico-sphere foliage. Base anchored on
    sampled terrain — trees ride the displaced relief instead of the
    sea-level waypoint Z plane."""
    objs = []
    foliage = _principled_material(
        "Tree_Foliage", (0.10, 0.32, 0.14), roughness=0.95)
    bark = _principled_material(
        "Tree_Bark", (0.18, 0.12, 0.08), roughness=0.92)
    golden = math.radians(137.508)
    trunk_r = TREE_TRUNK_RADIUS_M
    trunk_h = TREE_TRUNK_HEIGHT_M
    crown_r = TREE_CROWN_RADIUS_M
    crown_flat = TREE_CROWN_FLATTEN
    for cluster_idx, (nx, ny, _z_unused, count, radius) in enumerate(TREE_CLUSTERS_M):
        cx, cy = _local_xy(nx, ny)
        for i in range(count):
            r = radius * math.sqrt((i + 0.5) / count)
            theta = (cluster_idx * 0.5 + i) * golden
            tx_off = r * math.cos(theta)
            ty_off = r * math.sin(theta)
            tx = cx + tx_off
            ty = cy + ty_off
            # Per-tree normalized coords for heightmap sampling — convert
            # local Blender XY back to a parcel-normalized [-0.5,0.5] pair.
            tnx = tx / WORLD_SIZE
            tny = ty / WORLD_SIZE
            z_base = _sample_terrain_z(tnx, tny, 0.0)
            h_jitter = 1.0 + 0.18 * ((i % 3) - 1)

            bpy.ops.mesh.primitive_cylinder_add(
                radius=trunk_r,
                depth=trunk_h * h_jitter,
                location=(tx, ty, z_base + trunk_h * 0.5 * h_jitter),
                vertices=10,
            )
            trunk = bpy.context.active_object
            trunk.name = f"tree_c{cluster_idx}_{i:02d}_trunk"
            trunk.data.materials.append(bark)
            objs.append(trunk)

            crown_z = z_base + trunk_h * h_jitter + crown_r * crown_flat * 0.6
            bpy.ops.mesh.primitive_ico_sphere_add(
                radius=crown_r * h_jitter,
                subdivisions=2,
                location=(tx, ty, crown_z),
            )
            crown = bpy.context.active_object
            crown.name = f"tree_c{cluster_idx}_{i:02d}"
            crown.scale = (1.0, 1.0, crown_flat)
            bpy.ops.object.transform_apply(scale=True)
            crown.data.materials.append(foliage)
            objs.append(crown)
    return objs


def _build_parcel_boundary():
    """Bright cyan wireframe square at z=0 — frames the 900 m parcel."""
    half = WORLD_SIZE * 0.5
    verts = [(-half, -half, 4.0), (half, -half, 4.0),
             (half, half, 4.0), (-half, half, 4.0)]
    faces = [(0, 1, 2, 3)]
    mesh = bpy.data.meshes.new("parcel_boundary_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("parcel_boundary", mesh)
    bpy.context.collection.objects.link(obj)
    wf = obj.modifiers.new("Wf", "WIREFRAME")
    wf.thickness = BOUNDARY_THICKNESS_M
    wf.use_replace = True
    wf.use_even_offset = True
    obj.data.materials.append(_emission_material("Boundary", (0.10, 0.95, 0.95), 4.0))
    return obj


def _setup_neutral_world(scene):
    """v5: gradient sky — horizon haze warming up into zenith blue. Replaces
    the v4 flat slate background that gave renders a 'studio gray' feel.
    Function name preserved so scripts/build_terrain_62ha_blend.py still
    calls it without changes. Sun lamp from setup_world stays."""
    world = scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()

    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    grad = nt.nodes.new("ShaderNodeTexGradient")
    grad.gradient_type = "LINEAR"
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "EASE"
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (0.85, 0.78, 0.65, 1.0)  # horizon haze
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = (0.35, 0.55, 0.78, 1.0)  # zenith blue
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = 1.8
    out = nt.nodes.new("ShaderNodeOutputWorld")

    # Rotate generated coords so the gradient runs along world-Z: TexCoord
    # Generated -> Mapping (rotate 90° about X so Z drives the gradient axis)
    # -> Gradient (uses X of input). Resulting V goes from 0 at -Z (horizon)
    # to 1 at +Z (zenith).
    mapping.inputs["Rotation"].default_value = (math.radians(-90.0), 0.0, 0.0)

    nt.links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], grad.inputs["Vector"])
    nt.links.new(grad.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])


def _build_north_arrow():
    """v5: rests on the cropped relief at the north edge of the parcel
    instead of floating 450 m up. Compass ring sits flush, arrow points up
    from the surface."""
    nx_arrow = 0.0
    ny_arrow = 0.46
    z_surface = _sample_terrain_z(nx_arrow, ny_arrow, 2.0)
    z_arrow_center = z_surface + NORTH_ARROW_DEPTH_M * 0.5
    arrow_y = WORLD_SIZE * ny_arrow
    bpy.ops.mesh.primitive_cone_add(
        radius1=NORTH_ARROW_RADIUS_M, radius2=0.0, depth=NORTH_ARROW_DEPTH_M,
        location=(0.0, arrow_y, z_arrow_center),
    )
    arrow = bpy.context.active_object
    arrow.name = "north_arrow"
    arrow.data.materials.append(_emission_material("North", (0.95, 0.30, 0.25), 5.0))

    bpy.ops.mesh.primitive_torus_add(
        major_radius=NORTH_ARROW_RADIUS_M * 1.4,
        minor_radius=NORTH_ARROW_RADIUS_M * 0.08,
        location=(0.0, arrow_y, z_surface + 0.5),
        major_segments=48, minor_segments=8,
    )
    ring = bpy.context.active_object
    ring.name = "north_arrow_ring"
    ring.data.materials.append(_emission_material("NorthRing", (0.95, 0.30, 0.25), 3.5))
    return arrow


def _build():
    plane = _build_terrain_block()
    _build_ground_material(plane)
    _build_stream()
    _build_pool()
    _build_platforms()
    _build_tree_clusters()
    _build_north_arrow()
    _build_parcel_boundary()


# Camera presets. Override via env var RENDER_CAM_VIEW=birdseye|plan|oblique.
# v3 (2026-06-11): rescaled for 900 m WORLD_SIZE, parcel-focused HD framing.
_CAM_VIEWS = {
    # Drone-altitude 3/4 SE view. ~600 m horizontal / 600 m up — parcel fills
    # ~85% of the frame; relief reads clearly without crowding the corners.
    "birdseye": dict(location=(600.0, -600.0, 600.0),
                     look_at=(0.0, 0.0, 80.0),
                     lens=35.0, ortho=None),
    # Orthographic top-down — fits the 900 m parcel with a thin margin.
    "plan":     dict(location=(0.0, 0.0, 1500.0),
                     look_at=(0.0, 0.0, 80.0),
                     lens=35.0, ortho=1000.0),
    # Low oblique from SW, ~400 m altitude — maximum relief feel.
    "oblique":  dict(location=(500.0, -500.0, 400.0),
                     look_at=(0.0, 0.0, 100.0),
                     lens=35.0, ortho=None),
}


if __name__ == "__main__":
    # Inline of base.run — needed so we can override camera clip_end. The
    # parcel is 900 m wide and most cameras sit hundreds of metres away,
    # well past Blender's default 100 m far clip plane.
    view_key = os.environ.get("RENDER_CAM_VIEW", "birdseye")
    if view_key not in _CAM_VIEWS:
        raise SystemExit(f"unknown RENDER_CAM_VIEW={view_key!r}; "
                         f"expected one of {sorted(_CAM_VIEWS)}")
    os.environ.setdefault("RENDER_RUN_TAG", view_key)

    scene, cfg = base.setup("terrain_62ha")
    _build()
    print(f"[terrain_62ha] scene objs: {sorted(o.name for o in scene.objects)}")
    base.setup_world(scene, cfg.variant)
    _setup_neutral_world(scene)

    view = _CAM_VIEWS[view_key]
    cam = cameras.add_camera(
        "Cam_Subscene",
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
    print(f"[terrain_62ha] view={view_key} → {view['location']}")
    base.save_subrender(scene, "terrain_62ha", cfg)
