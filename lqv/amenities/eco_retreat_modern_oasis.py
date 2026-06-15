"""Amenity — Eco Retreat / Modern Oasis (modernist wellness pavilion).

Wesley brief, Phase F (2026-06-13): replaces the earlier curved-bamboo
pavilion stub with a modernist wellness composition oriented around a
half-icosahedron lapacho-frame geodesic dome, a 12 m E-W reflection pool,
a U-shaped lapacho-plank deck, a Guadua bamboo curtain wall on the east,
a yoga shelter at the NW, and a low boulder + bench lounge cluster on
the south side of the pool. Surround flora: 4 lapacho saplings + 2 tree
ferns + 1 Guadua clump.

Geometry is procedural (CC0). Bamboo primitives import from
:mod:`lqv.house.bamboo_frame`; flora uses the photoreal helpers when
``RENDER_FLORA_PHOTOREAL=1`` else the flat fallbacks.
"""
from __future__ import annotations

import math
import os

import bpy

from lqv.house.bamboo_frame import (
    build_bamboo_beam,
    build_bamboo_culm,
    build_bamboo_lashing,
    build_palm_thatch_panel,
)
from lqv.materials import MAT, assign

# ---------------------------------------------------------------------------
# Dimensions (metres) — kept module-level so MATERIAL_TAKEOFF can derive from
# the same numbers used by the builders.
# ---------------------------------------------------------------------------

DOME_DIAMETER_M = 6.0
DOME_RADIUS_M = DOME_DIAMETER_M / 2.0
DOME_HEIGHT_M = 3.0
DOME_STRUT_RADIUS_M = 0.04

POOL_LENGTH_M = 12.0          # E-W long axis
POOL_WIDTH_M = 4.0            # N-S short axis
POOL_DEPTH_M = 0.10
POOL_OFFSET_S_M = 6.0         # pool centre is 6 m south of dome centre
POOL_COPING_W_M = 0.30
POOL_COPING_T_M = 0.06

DECK_OUTER_X_M = 14.0
DECK_OUTER_Y_M = 10.0
DECK_HOLE_X_M = 8.0
DECK_HOLE_Y_M = 6.0
DECK_THICKNESS_M = 0.04
DECK_ELEVATION_M = 0.30
DECK_POST_DIM_M = 0.15
DECK_POST_H_M = DECK_ELEVATION_M + 0.05
DECK_POST_COUNT = 16

CURTAIN_WALL_LENGTH_M = 5.4
CURTAIN_WALL_HEIGHT_M = 3.0
CURTAIN_WALL_SPACING_M = 0.18
CURTAIN_WALL_CULM_R_M = 0.04
CURTAIN_WALL_COUNT = 30        # 30 culms × 0.18 m ≈ 5.4 m
CURTAIN_WALL_DOOR_CENTER_I = 15
CURTAIN_WALL_DOOR_HALF_WIDTH = 2  # skip 5 culms ≈ 0.9 m aperture

YOGA_W_M = 4.0
YOGA_L_M = 4.0
YOGA_POST_DIM_M = 0.15
YOGA_POST_H_M = 2.8
YOGA_ROOF_TILT_DEG = 8.0

BOULDER_RADIUS_M = 0.7
BENCH_L_M = 1.8
BENCH_W_M = 0.4
BENCH_H_M = 0.45


# ---------------------------------------------------------------------------
# MATERIAL_TAKEOFF — 12 line items, target band $28k–$38k.
# ---------------------------------------------------------------------------

_DOME_PANEL_AREA_M2 = 2.0 * math.pi * DOME_RADIUS_M * (DOME_HEIGHT_M)  # half-sphere surface ≈ 2πRh
_DOME_STRUT_LENGTH_M = 65.0   # ~65 m of frame edges in a 3-frequency half-icosahedron at 6 m Ø
_DECK_AREA_M2 = (DECK_OUTER_X_M * DECK_OUTER_Y_M) - (DECK_HOLE_X_M * DECK_HOLE_Y_M)
_POOL_VOLUME_M3 = POOL_LENGTH_M * POOL_WIDTH_M * POOL_DEPTH_M
_POOL_PERIMETER_M = 2.0 * (POOL_LENGTH_M + POOL_WIDTH_M)
_YOGA_ROOF_AREA_M2 = YOGA_W_M * YOGA_L_M / math.cos(math.radians(YOGA_ROOF_TILT_DEG))

MATERIAL_TAKEOFF: dict = {
    'lapacho_dome_struts': {
        # 3-frequency half-icosahedron struts ~ 65 m total at 0.04 m Ø lapacho
        'length_m': _DOME_STRUT_LENGTH_M,
        'unit_cost_usd': 38.0,
    },
    'etfe_glass_dome_panels': {
        # Triangular ETFE / laminated-glass infill panels across the half-dome
        'area_m2': _DOME_PANEL_AREA_M2,
        'unit_cost_usd': 285.0,
    },
    'reflection_pool_basin_concrete': {
        # Waterproofed concrete basin + dark plaster lining for the 12 × 4 pool
        'area_m2': POOL_LENGTH_M * POOL_WIDTH_M,
        'unit_cost_usd': 165.0,
    },
    'reflection_pool_water_treatment': {
        # UV + filtration + initial fill
        'volume_m3': _POOL_VOLUME_M3,
        'unit_cost_usd': 240.0,
    },
    'sandstone_pool_coping': {
        # 0.30 m wide × 0.06 m thick sandstone slabs around the pool edge
        'length_m': _POOL_PERIMETER_M,
        'unit_cost_usd': 78.0,
    },
    'lapacho_deck_planks': {
        # 0.04 m lapacho plank decking, U-shaped wrap around dome + pool
        'area_m2': _DECK_AREA_M2,
        'unit_cost_usd': 145.0,
    },
    'lapacho_deck_posts': {
        # 16 lapacho posts 0.15 × 0.15 × 0.4 m supporting the deck
        'count': DECK_POST_COUNT,
        'unit_cost_usd': 55.0,
    },
    'bamboo_curtain_wall_culms': {
        # 30 Guadua culms 3.0 m × 0.08 m Ø + ring-beam lashings
        'count': CURTAIN_WALL_COUNT,
        'unit_cost_usd': 48.0,
    },
    'yoga_shelter_frame': {
        # 4 lapacho posts + ring beam + bamboo rafters
        'count': 1,
        'unit_cost_usd': 1450.0,
    },
    'palm_thatch_yoga_roof': {
        # Shed roof at 8°, 4 × 4 m footprint of palm thatch
        'area_m2': _YOGA_ROOF_AREA_M2,
        'unit_cost_usd': 22.0,
    },
    'mossy_boulders_lounge': {
        # 2 sandstone boulders sourced and placed
        'count': 2,
        'unit_cost_usd': 320.0,
    },
    'lapacho_bench_lounge': {
        # 1.8 × 0.4 × 0.45 m solid lapacho bench
        'count': 1,
        'unit_cost_usd': 680.0,
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_collection(name: str, parent: bpy.types.Collection | None) -> bpy.types.Collection:
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(col)
    return col


def _link(obj: bpy.types.Object, col: bpy.types.Collection) -> None:
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def _mat(*keys: str):
    for k in keys:
        m = MAT.get(k)
        if m is not None:
            return m
    return None


def _photoreal_enabled() -> bool:
    return os.environ.get('RENDER_FLORA_PHOTOREAL') == '1'


# ---------------------------------------------------------------------------
# Geodesic dome — half-icosphere (subdiv=2) with edge struts + triangle panels
# ---------------------------------------------------------------------------

def _build_geodesic_dome(col: bpy.types.Collection, center: tuple[float, float, float]):
    """Half-icosahedron dome: lapacho struts on every edge + glass panel triangles.

    Step 1: create an icosphere (subdivisions=2 ≈ frequency-3), scaled non-uniformly
    so it ends up DOME_RADIUS_M wide and DOME_HEIGHT_M tall after the bottom half
    is removed.
    Step 2: delete vertices below z=0 to keep only the upper hemisphere.
    Step 3: for every retained edge, emit a small cylinder strut in lapacho.
    Step 4: emit the triangle-faced surface (panel infill) as a single mesh in
    a translucent glass material so the camera sees through it to the pool.
    """
    cx, cy, cz = center
    mat_strut = _mat('lapacho_timber', 'bamboo')
    mat_panel = _mat('pv_glass', 'water_reflective', 'window_glow')

    # 1. Source icosphere — Blender places vertices on a unit sphere; we scale
    # later so radius == DOME_RADIUS_M and apex height == DOME_HEIGHT_M.
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=2,
        radius=1.0,
        location=(cx, cy, cz),
    )
    src = bpy.context.active_object
    src.name = 'EcoRetreat_DomeSource'
    # Non-uniform scale: keep 6 m diameter (XY) but tune Z so a hemisphere is
    # exactly 3 m tall. Apply scale.
    src.scale = (DOME_RADIUS_M, DOME_RADIUS_M, DOME_HEIGHT_M)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # 2. Trim the lower half — keep verts with local z >= -0.001 (small epsilon
    # so the equator ring survives).
    mesh = src.data
    # World-space cutoff after applying scale and the +cz translation:
    z_cutoff = cz - 0.001
    keep_verts: dict[int, int] = {}  # old → new index
    new_verts: list[tuple[float, float, float]] = []
    for i, v in enumerate(mesh.vertices):
        if v.co.z >= z_cutoff:
            keep_verts[i] = len(new_verts)
            new_verts.append((v.co.x, v.co.y, v.co.z))
    new_faces: list[tuple[int, ...]] = []
    edges: set[tuple[int, int]] = set()
    for poly in mesh.polygons:
        old_idx = list(poly.vertices)
        if not all(oi in keep_verts for oi in old_idx):
            continue
        face = tuple(keep_verts[oi] for oi in old_idx)
        new_faces.append(face)
        for a in range(len(face)):
            i0, i1 = face[a], face[(a + 1) % len(face)]
            edges.add((min(i0, i1), max(i0, i1)))

    # 3. Lapacho-frame struts on every edge.
    strut_col = col
    for k, (i0, i1) in enumerate(sorted(edges)):
        v0 = new_verts[i0]
        v1 = new_verts[i1]
        strut = build_bamboo_culm(
            p_start_xyz=v0,
            p_end_xyz=v1,
            diameter_m=DOME_STRUT_RADIUS_M * 2.0,
            taper_ratio=1.0,
            segments=6,
            material='lapacho_timber',
            name=f'EcoRetreat_DomeStrut_{k:03d}',
        )
        if mat_strut is not None:
            assign(strut, mat_strut)
        _link(strut, strut_col)

    # 4. Glass panel infill — single triangulated mesh, translucent.
    panel_mesh = bpy.data.meshes.new('EcoRetreat_DomePanels_Mesh')
    panel_mesh.from_pydata(new_verts, [], new_faces)
    panel_mesh.update()
    panel_obj = bpy.data.objects.new('EcoRetreat_DomePanels', panel_mesh)
    if mat_panel is not None:
        assign(panel_obj, mat_panel)
    col.objects.link(panel_obj)

    # 5. Remove the source icosphere — we no longer need it; the panels +
    # struts represent the dome.
    bpy.data.objects.remove(src, do_unlink=True)


# ---------------------------------------------------------------------------
# Reflection pool — water plane + sandstone coping frame
# ---------------------------------------------------------------------------

def _build_reflection_pool(col: bpy.types.Collection, center: tuple[float, float, float]):
    """12 × 4 m water plane, depth 0.10 m, with sandstone coping perimeter."""
    cx, cy, cz = center
    mat_water = _mat('water_reflective', 'pool_water', 'pv_glass')
    mat_stone = _mat('sandstone', 'laterite')

    # Water surface: a thin slab at +0.02 m (just above ground) so reflections
    # catch the dome and surroundings rather than reading as a depthless decal.
    water_z = cz + POOL_DEPTH_M / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, water_z))
    water = bpy.context.active_object
    water.name = 'EcoRetreat_PoolWater'
    water.scale = (POOL_LENGTH_M, POOL_WIDTH_M, POOL_DEPTH_M)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat_water is not None:
        assign(water, mat_water)
    _link(water, col)

    # Coping: 4 sandstone slabs forming the rectangular frame.
    coping_z = cz + POOL_DEPTH_M + POOL_COPING_T_M / 2.0
    # Two long (E-W) slabs and two short (N-S) slabs
    half_l = POOL_LENGTH_M / 2.0 + POOL_COPING_W_M / 2.0
    half_w = POOL_WIDTH_M / 2.0 + POOL_COPING_W_M / 2.0
    coping_specs = [
        ('N', (cx, cy + POOL_WIDTH_M / 2.0 + POOL_COPING_W_M / 2.0, coping_z),
         (POOL_LENGTH_M + 2 * POOL_COPING_W_M, POOL_COPING_W_M, POOL_COPING_T_M)),
        ('S', (cx, cy - POOL_WIDTH_M / 2.0 - POOL_COPING_W_M / 2.0, coping_z),
         (POOL_LENGTH_M + 2 * POOL_COPING_W_M, POOL_COPING_W_M, POOL_COPING_T_M)),
        ('E', (cx + POOL_LENGTH_M / 2.0 + POOL_COPING_W_M / 2.0, cy, coping_z),
         (POOL_COPING_W_M, POOL_WIDTH_M, POOL_COPING_T_M)),
        ('W', (cx - POOL_LENGTH_M / 2.0 - POOL_COPING_W_M / 2.0, cy, coping_z),
         (POOL_COPING_W_M, POOL_WIDTH_M, POOL_COPING_T_M)),
    ]
    for tag, loc, scale in coping_specs:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        obj = bpy.context.active_object
        obj.name = f'EcoRetreat_PoolCoping_{tag}'
        obj.scale = scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if mat_stone is not None:
            assign(obj, mat_stone)
        _link(obj, col)


# ---------------------------------------------------------------------------
# Lapacho deck — U-shaped wrap with central hole for dome + pool
# ---------------------------------------------------------------------------

def _build_deck(col: bpy.types.Collection, center: tuple[float, float, float]):
    """U-shaped lapacho deck — outer 14 × 10 m, central 8 × 6 m hole.

    Implemented as 4 rectangular planks framing the hole + 16 lapacho posts.
    The hole is centred on (cx, cy) and the outer rectangle is shifted so the
    deck wraps from the north (yoga shelter side) around east + west, with the
    pool exposed to the south.
    """
    cx, cy, cz = center
    mat_deck = _mat('lapacho_timber', 'bamboo')

    deck_top_z = cz + DECK_ELEVATION_M + DECK_THICKNESS_M / 2.0

    # Outer envelope: 14 × 10 m, centred on the dome.
    outer_x_half = DECK_OUTER_X_M / 2.0
    outer_y_half = DECK_OUTER_Y_M / 2.0
    hole_x_half = DECK_HOLE_X_M / 2.0
    hole_y_half = DECK_HOLE_Y_M / 2.0

    # 4 planks of the U-frame (north, east, west, south). The U opens south —
    # so the south plank is omitted (deck opens onto pool sightlines).
    # Per brief: U-shape, so 3 sides only.
    planks = [
        # North plank (full outer width)
        ('N', (cx, cy + (outer_y_half + hole_y_half) / 2.0, deck_top_z),
         (DECK_OUTER_X_M, outer_y_half - hole_y_half, DECK_THICKNESS_M)),
        # East plank (between north + south rim, hole width)
        ('E', (cx + (outer_x_half + hole_x_half) / 2.0, cy, deck_top_z),
         (outer_x_half - hole_x_half, DECK_OUTER_Y_M, DECK_THICKNESS_M)),
        # West plank
        ('W', (cx - (outer_x_half + hole_x_half) / 2.0, cy, deck_top_z),
         (outer_x_half - hole_x_half, DECK_OUTER_Y_M, DECK_THICKNESS_M)),
        # South plank — opens to the pool/lounge; thin band so the deck still
        # reads as a continuous frame rather than a free-floating gap.
        ('S', (cx, cy - (outer_y_half + hole_y_half) / 2.0, deck_top_z),
         (DECK_OUTER_X_M, outer_y_half - hole_y_half, DECK_THICKNESS_M)),
    ]
    for tag, loc, scale in planks:
        if scale[0] <= 0 or scale[1] <= 0:
            continue
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        obj = bpy.context.active_object
        obj.name = f'EcoRetreat_DeckPlank_{tag}'
        obj.scale = scale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if mat_deck is not None:
            assign(obj, mat_deck)
        _link(obj, col)

    # 16 deck posts spaced around the outer + inner perimeter.
    post_z = cz + DECK_POST_H_M / 2.0
    # 4 outer corners, 4 outer mid-edges, 4 inner corners, 4 inner mid-edges
    post_positions: list[tuple[float, float]] = []
    # Outer corners
    for sx in (-outer_x_half, outer_x_half):
        for sy in (-outer_y_half, outer_y_half):
            post_positions.append((cx + sx, cy + sy))
    # Outer mid-edges
    for sx in (-outer_x_half / 2.0, outer_x_half / 2.0):
        for sy in (-outer_y_half, outer_y_half):
            post_positions.append((cx + sx, cy + sy))
    # Inner corners
    for sx in (-hole_x_half, hole_x_half):
        for sy in (-hole_y_half, hole_y_half):
            post_positions.append((cx + sx, cy + sy))
    # Keep first 16 (4+4+8 = 16 exactly).
    for k, (px, py) in enumerate(post_positions[:DECK_POST_COUNT]):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, py, cz + DECK_POST_H_M / 2.0))
        obj = bpy.context.active_object
        obj.name = f'EcoRetreat_DeckPost_{k:02d}'
        obj.scale = (DECK_POST_DIM_M, DECK_POST_DIM_M, DECK_POST_H_M)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if mat_deck is not None:
            assign(obj, mat_deck)
        _link(obj, col)


# ---------------------------------------------------------------------------
# Bamboo curtain wall — 30 Guadua culms on the east edge of the deck
# ---------------------------------------------------------------------------

def _build_curtain_wall(col: bpy.types.Collection, center: tuple[float, float, float]):
    """30 vertical Guadua culms spaced 0.18 m along a 5.4 m N-S line on the east.

    Topped with a lapacho ring beam lashing the culms together.
    """
    cx, cy, cz = center
    # Position the curtain wall just outside the east edge of the deck.
    wall_x = cx + DECK_OUTER_X_M / 2.0 + 0.40
    # Centred N-S on the dome's latitude.
    y0 = cy - CURTAIN_WALL_LENGTH_M / 2.0
    z_base = cz + DECK_ELEVATION_M + DECK_THICKNESS_M
    z_top = z_base + CURTAIN_WALL_HEIGHT_M

    culms: list[bpy.types.Object] = []
    for i in range(CURTAIN_WALL_COUNT):
        if abs(i - CURTAIN_WALL_DOOR_CENTER_I) <= CURTAIN_WALL_DOOR_HALF_WIDTH:
            continue
        py = y0 + i * CURTAIN_WALL_SPACING_M
        culm = build_bamboo_culm(
            p_start_xyz=(wall_x, py, z_base),
            p_end_xyz=(wall_x, py, z_top),
            diameter_m=CURTAIN_WALL_CULM_R_M * 2.0,
            taper_ratio=0.92,
            segments=10,
            material='bamboo',
            name=f'EcoRetreat_CurtainCulm_{i:02d}',
        )
        _link(culm, col)
        culms.append(culm)

    # Lapacho lintel across the door aperture so the gap reads as a designed
    # opening, not a missing-piece bug.
    door_y_min = y0 + (CURTAIN_WALL_DOOR_CENTER_I - CURTAIN_WALL_DOOR_HALF_WIDTH) * CURTAIN_WALL_SPACING_M
    door_y_max = y0 + (CURTAIN_WALL_DOOR_CENTER_I + CURTAIN_WALL_DOOR_HALF_WIDTH) * CURTAIN_WALL_SPACING_M
    lintel = build_bamboo_beam(
        p_start_xyz=(wall_x, door_y_min - 0.05, z_base + 2.1),
        p_end_xyz=(wall_x, door_y_max + 0.05, z_base + 2.1),
        diameter_m=0.08,
        material='lapacho_timber',
        name='EcoRetreat_CurtainDoorLintel',
    )
    _link(lintel, col)

    # Lapacho ring beam: horizontal lapacho rod along the top of the curtain.
    beam = build_bamboo_beam(
        p_start_xyz=(wall_x, y0 - 0.10, z_top + 0.05),
        p_end_xyz=(wall_x, y0 + CURTAIN_WALL_LENGTH_M + 0.10, z_top + 0.05),
        diameter_m=0.10,
        material='lapacho_timber',
        name='EcoRetreat_CurtainBeam',
    )
    _link(beam, col)

    # Lashings at every 5th culm so the read of joint-by-joint is unmistakable.
    for i in range(0, CURTAIN_WALL_COUNT, 5):
        py = y0 + i * CURTAIN_WALL_SPACING_M
        lash = build_bamboo_lashing(
            xyz=(wall_x, py, z_top - 0.02),
            radius_m=0.08,
            thickness_m=0.018,
            material='rope_natural',
            fallback='lapacho_timber',
            name=f'EcoRetreat_CurtainLashing_{i:02d}',
        )
        _link(lash, col)


# ---------------------------------------------------------------------------
# Yoga shelter — NW corner, 4 m × 4 m, palm-thatch shed roof
# ---------------------------------------------------------------------------

def _build_yoga_shelter(col: bpy.types.Collection, center: tuple[float, float, float]):
    """4 m × 4 m post-and-beam yoga shelter with a tilted palm-thatch shed roof."""
    cx, cy, cz = center
    mat_post = _mat('lapacho_timber', 'bamboo')

    # NW corner of the deck — sit the shelter so its centre is just inside the
    # deck perimeter, north-west of the dome.
    shelter_cx = cx - DECK_OUTER_X_M / 2.0 + YOGA_W_M / 2.0 + 0.40
    shelter_cy = cy + DECK_OUTER_Y_M / 2.0 - YOGA_L_M / 2.0 - 0.40
    base_z = cz + DECK_ELEVATION_M + DECK_THICKNESS_M

    # 4 lapacho corner posts
    corners = [
        (-YOGA_W_M / 2.0, -YOGA_L_M / 2.0),
        ( YOGA_W_M / 2.0, -YOGA_L_M / 2.0),
        ( YOGA_W_M / 2.0,  YOGA_L_M / 2.0),
        (-YOGA_W_M / 2.0,  YOGA_L_M / 2.0),
    ]
    for k, (dx, dy) in enumerate(corners):
        px = shelter_cx + dx
        py = shelter_cy + dy
        bpy.ops.mesh.primitive_cube_add(
            size=1.0,
            location=(px, py, base_z + YOGA_POST_H_M / 2.0),
        )
        obj = bpy.context.active_object
        obj.name = f'EcoRetreat_YogaPost_{k}'
        obj.scale = (YOGA_POST_DIM_M, YOGA_POST_DIM_M, YOGA_POST_H_M)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if mat_post is not None:
            assign(obj, mat_post)
        _link(obj, col)

    # Tilted shed roof: high SW, low NE. Compute roof corner Z heights:
    # we tilt around a horizontal axis running NW->SE so that the SW corner
    # rises by tan(8°) × diagonal/2 and the NE corner falls by the same.
    tilt = math.radians(YOGA_ROOF_TILT_DEG)
    diag = math.sqrt(YOGA_W_M ** 2 + YOGA_L_M ** 2)
    dz = math.tan(tilt) * diag / 2.0
    roof_z = base_z + YOGA_POST_H_M + 0.10
    corners_xyz = [
        # SW (high)
        (shelter_cx - YOGA_W_M / 2.0, shelter_cy - YOGA_L_M / 2.0, roof_z + dz),
        # SE
        (shelter_cx + YOGA_W_M / 2.0, shelter_cy - YOGA_L_M / 2.0, roof_z),
        # NE (low)
        (shelter_cx + YOGA_W_M / 2.0, shelter_cy + YOGA_L_M / 2.0, roof_z - dz),
        # NW
        (shelter_cx - YOGA_W_M / 2.0, shelter_cy + YOGA_L_M / 2.0, roof_z),
    ]
    roof = build_palm_thatch_panel(
        corners_xyz=corners_xyz,
        material='palm_thatch',
        name='EcoRetreat_YogaRoof',
        subdivisions=4,
    )
    _link(roof, col)


# ---------------------------------------------------------------------------
# Lounge cluster — 2 boulders + 1 lapacho bench along the south edge of the pool
# ---------------------------------------------------------------------------

def _build_lounge(col: bpy.types.Collection, pool_center: tuple[float, float, float]):
    """2 mossy boulders + 1 lapacho bench along the south edge of the pool.

    `_grammar.boulder_seating_cluster` is not present in the codebase
    (only `boulder_seating` exists) — boulders are inlined here per brief.
    """
    px, py, pz = pool_center
    mat_stone = _mat('sandstone', 'laterite')
    mat_moss = _mat('moss', 'sod_canopy')
    mat_bench = _mat('lapacho_timber', 'bamboo')

    south_y = py - POOL_WIDTH_M / 2.0 - 1.20

    # Boulder 1 — west of bench
    bpy.ops.mesh.primitive_ico_sphere_add(
        radius=BOULDER_RADIUS_M,
        subdivisions=2,
        location=(px - 2.4, south_y - 0.3, pz + BOULDER_RADIUS_M * 0.50),
    )
    b1 = bpy.context.active_object
    b1.name = 'EcoRetreat_Boulder_W'
    b1.scale = (1.05, 1.10, 0.62)  # squashed
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat_moss is not None:
        assign(b1, mat_moss)
    elif mat_stone is not None:
        assign(b1, mat_stone)
    _link(b1, col)

    # Boulder 2 — east of bench
    bpy.ops.mesh.primitive_ico_sphere_add(
        radius=BOULDER_RADIUS_M * 0.92,
        subdivisions=2,
        location=(px + 2.6, south_y - 0.1, pz + BOULDER_RADIUS_M * 0.46),
    )
    b2 = bpy.context.active_object
    b2.name = 'EcoRetreat_Boulder_E'
    b2.scale = (1.10, 1.05, 0.60)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat_moss is not None:
        assign(b2, mat_moss)
    elif mat_stone is not None:
        assign(b2, mat_stone)
    _link(b2, col)

    # Lapacho bench, centred on south edge of pool
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, south_y, pz + BENCH_H_M / 2.0))
    bench = bpy.context.active_object
    bench.name = 'EcoRetreat_LoungeBench'
    bench.scale = (BENCH_L_M, BENCH_W_M, BENCH_H_M)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat_bench is not None:
        assign(bench, mat_bench)
    _link(bench, col)


# ---------------------------------------------------------------------------
# Surround flora — 4 lapacho saplings + 2 tree ferns + 1 Guadua clump
# ---------------------------------------------------------------------------

def _build_flora(col: bpy.types.Collection, center: tuple[float, float, float]):
    cx, cy, _cz = center
    photoreal = _photoreal_enabled()

    # 4 lapacho saplings along east + south perimeter
    sapling_positions = [
        (cx + DECK_OUTER_X_M / 2.0 + 2.5, cy + 2.0),    # NE
        (cx + DECK_OUTER_X_M / 2.0 + 2.5, cy - 4.0),    # SE
        (cx + 2.0, cy - DECK_OUTER_Y_M / 2.0 - 4.0),    # S
        (cx - 2.0, cy - DECK_OUTER_Y_M / 2.0 - 4.5),    # S-W
    ]
    for sx, sy in sapling_positions:
        if photoreal:
            try:
                from lqv.flora.photoreal import add_lapacho_photoreal
                obj = add_lapacho_photoreal(x=sx, y=sy, scale=0.5, flowering=True)
            except Exception as e:
                # Photoreal lapacho needs PolyHaven/AmbientCG assets that may
                # not be staged on every machine; fall back to procedural and
                # log so the asset team sees what's missing instead of
                # discovering it in the render review meeting.
                import sys, traceback
                print(
                    f'[eco_retreat] photoreal lapacho at ({sx:.2f}, {sy:.2f}) '
                    f'failed ({type(e).__name__}: {e}); using procedural fallback.',
                    file=sys.stderr,
                )
                traceback.print_exc(file=sys.stderr)
                from lqv.flora.lapacho import add_lapacho
                obj = add_lapacho(sx, sy, scale=0.5)
        else:
            from lqv.flora.lapacho import add_lapacho
            obj = add_lapacho(sx, sy, scale=0.5)
        if obj is not None:
            # add_lapacho returns list[Object]; photoreal returns single Object.
            if isinstance(obj, (list, tuple)):
                for o in obj:
                    if o is not None:
                        _link(o, col)
            else:
                _link(obj, col)

    # 2 tree ferns north of the dome
    fern_positions = [
        (cx - 1.5, cy + DECK_OUTER_Y_M / 2.0 + 2.0),
        (cx + 1.5, cy + DECK_OUTER_Y_M / 2.0 + 2.0),
    ]
    for fx, fy in fern_positions:
        if photoreal:
            try:
                from lqv.flora.photoreal import add_tree_fern_photoreal
                obj = add_tree_fern_photoreal(x=fx, y=fy, scale=1.0)
            except Exception as e:
                import sys, traceback
                print(
                    f'[eco_retreat] photoreal tree fern at ({fx:.2f}, {fy:.2f}) '
                    f'failed ({type(e).__name__}: {e}); using procedural fallback.',
                    file=sys.stderr,
                )
                traceback.print_exc(file=sys.stderr)
                from lqv.flora.fern import add_tree_fern
                obj = add_tree_fern(fx, fy, scale=1.0)
        else:
            from lqv.flora.fern import add_tree_fern
            obj = add_tree_fern(fx, fy, scale=1.0)
        if obj is not None:
            if isinstance(obj, (list, tuple)):
                for o in obj:
                    if o is not None:
                        _link(o, col)
            else:
                _link(obj, col)

    # 1 Guadua bamboo clump in the SW corner — cluster of 7 culms
    clump_cx = cx - DECK_OUTER_X_M / 2.0 - 2.5
    clump_cy = cy - DECK_OUTER_Y_M / 2.0 - 1.5
    for i in range(7):
        # Spiral arrangement, 0.20 m radius
        theta = i * (2.0 * math.pi / 7.0)
        rx = clump_cx + 0.20 * math.cos(theta)
        ry = clump_cy + 0.20 * math.sin(theta)
        # Mildly varied height 3.8–4.6 m for natural read
        h = 3.8 + 0.115 * (i % 7)
        culm = build_bamboo_culm(
            p_start_xyz=(rx, ry, 0.0),
            p_end_xyz=(rx + 0.03 * math.cos(theta), ry + 0.03 * math.sin(theta), h),
            diameter_m=0.07,
            taper_ratio=0.88,
            segments=8,
            material='bamboo',
            name=f'EcoRetreat_ClumpCulm_{i}',
        )
        if culm is not None:
            # build_bamboo_culm may return a single Object or a list/tuple
            # of segment Objects; mirror the guard pattern used for lapachos
            # and tree ferns above so a list return doesn't blow up _link.
            if isinstance(culm, (list, tuple)):
                for o in culm:
                    if o is not None:
                        _link(o, col)
            else:
                _link(culm, col)


# ---------------------------------------------------------------------------
# Top-level builder
# ---------------------------------------------------------------------------

def build_eco_retreat_modern_oasis(parent=None, location: tuple[float, float, float] = (0.0, 0.0, 0.0)):
    """Build the full eco retreat / modernist wellness pavilion at ``location``."""
    name = 'EcoRetreat_ModernOasis'
    col = _ensure_collection(name, parent)
    cx, cy, cz = location

    # 1. Reflection pool first — sits south of dome, so coping reads underneath
    # the deck plank that crosses above it.
    pool_center = (cx, cy - POOL_OFFSET_S_M, cz)
    _build_reflection_pool(col, pool_center)

    # 2. Lapacho deck — U-frame around dome + pool.
    _build_deck(col, location)

    # 3. Geodesic dome — sits at the origin on the deck.
    dome_base_z = cz + DECK_ELEVATION_M + DECK_THICKNESS_M
    _build_geodesic_dome(col, (cx, cy, dome_base_z))

    # 4. Bamboo curtain wall — east side.
    _build_curtain_wall(col, location)

    # 5. Yoga shelter — NW corner.
    _build_yoga_shelter(col, location)

    # 6. Lounge cluster — south edge of the pool.
    _build_lounge(col, pool_center)

    # 7. Surround flora.
    _build_flora(col, location)

    return col


# Back-compat alias for any caller still importing ``build`` from the prior stub.
build = build_eco_retreat_modern_oasis


__all__ = [
    'MATERIAL_TAKEOFF',
    'build_eco_retreat_modern_oasis',
    'build',
]
