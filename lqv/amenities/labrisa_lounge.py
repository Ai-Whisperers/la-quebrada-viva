"""Amenity — Labrisa Lounge ("La Brisa").

Central social space at the heart of the bamboo-river cluster. Creek runs
through, glass-bowl pendant lanterns hang from a bamboo frame, boulder seating
along the creek edge. Cascade weir at the upstream end. First amenity built;
factors :mod:`lqv.amenities._grammar` out for cascade-weir, stepping-stone,
glass-bowl-lantern — all three vocabularies are reused by :mod:`eco_pool` and
:mod:`eco_retreat_modern_oasis`. Refer to ``docs/TERRAIN_PIVOT.md`` §4.3 for
the Wesley brief.
"""
from __future__ import annotations

import math
import os
import random

import bpy

from lqv.amenities import _grammar
from lqv.materials import MAT, assign

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_BOULDER_MODEL_DIR = os.path.join(_PROJECT_ROOT, 'assets', 'models')
_BOULDER_BLENDS = {
    'large':    os.path.join(_BOULDER_MODEL_DIR, 'boulder_01', 'boulder_01_4k.blend'),
    'medium_a': os.path.join(_BOULDER_MODEL_DIR, 'namaqualand_boulder_02', 'namaqualand_boulder_02_4k.blend'),
    'medium_b': os.path.join(_BOULDER_MODEL_DIR, 'namaqualand_boulder_03', 'namaqualand_boulder_03_4k.blend'),
    'small':    os.path.join(_BOULDER_MODEL_DIR, 'namaqualand_boulder_04', 'namaqualand_boulder_04_4k.blend'),
}

FOOTPRINT_M2 = 72.0           # ~8 m × 9 m roofed area, creek-through
PLATFORM_W = 8.0              # x (across creek)
PLATFORM_L = 9.0              # y (along creek)
DECK_ELEVATION_M = 0.45       # platform above grade
COLUMN_HEIGHT_M = 3.2         # bamboo column from deck to roof eave
ROOF_TYPE = 'palm_thatch_low_pitch'
ROOF_PITCH_DEG = 12.0
FRAME = 'guadua_bamboo'
PENDANTS = 'glass_bowl_lantern'
CREEK_THROUGH = True
CREEK_WIDTH_M = 1.5
CASCADE_WEIR_HEIGHT_M = 0.6
LANTERN_COUNT = 9
NOTES = (
    'Bamboo frame: 4-column grid, lashings + cylindrical bolts only.',
    'Creek passes under the deck via a 1.5 m wide channel; stepping stones at edges.',
    'Pendant lanterns: glass bowl emission planes, warm 2700K, ~9 across the bay.',
    'Boulder seating: sandstone/quartzite range, single-piece cushions in Paraguayan ñandutí pattern.',
    'Acoustic intent: cascade weir provides background white-noise at conversation volume.',
)

_COLUMN_RADIUS = 0.075        # 15 cm diameter guadua column
_ROOF_EAVE_OVERHANG = 0.8
_DECK_THICKNESS = 0.10

MATERIAL_TAKEOFF: dict = {
    'guadua_columns': {
        # 4 columns × COLUMN_HEIGHT_M
        'length_m': 4 * COLUMN_HEIGHT_M,
        'unit_cost_usd': 9.0,
    },
    'guadua_roof_frame': {
        # Perimeter ring beam + 4 hip rafters
        'length_m': 2 * (PLATFORM_W + PLATFORM_L) + 4 * math.hypot(PLATFORM_W / 2, PLATFORM_L / 2),
        'unit_cost_usd': 8.0,
    },
    'palm_thatch_roof': {
        # Low-pitch hipped at 12° → ~1.02 × footprint
        'area_m2': PLATFORM_W * PLATFORM_L * 1.02,
        'unit_cost_usd': 22.0,
    },
    'guadua_deck_culms': {
        # Deck minus creek channel, culms at 0.10 m spacing
        'length_m': (PLATFORM_L - CREEK_WIDTH_M) * (PLATFORM_W / 0.10),
        'unit_cost_usd': 6.0,
    },
    'lapacho_deck_joists': {
        # 4 joists supporting the deck above grade
        'length_m': 4 * PLATFORM_L,
        'unit_cost_usd': 24.0,
    },
    'sandstone_cascade_weir': {
        'volume_m3': 2.0 * 0.35 * CASCADE_WEIR_HEIGHT_M + 2.0 * 0.10 * 1.1,
        'unit_cost_usd': 380.0,
    },
    'sandstone_stepping_stones': {
        # 5 stones × π × r² × thickness
        'count': 10,  # two crossings, 5 each
        'unit_cost_usd': 65.0,
    },
    'sandstone_boulder_seating': {
        # 8 procedural stones (south + north arcs, 4 each) + 6 photoreal Poly Haven
        # boulders dressed in via _add_boulder_seating on the west side of the deck.
        'count': 14,
        'unit_cost_usd': 140.0,
    },
    'glass_bowl_lanterns': {
        'count': LANTERN_COUNT,
        'unit_cost_usd': 110.0,
    },
    'lashings_hardware': {
        'weight_kg': 22.0,
        'unit_cost_usd': 18.0,
    },
}


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


def _mat(key: str):
    return MAT.get(key)


def _columns(col, ox, oy):
    """4 bamboo columns at the corners (inset slightly from the platform edge)."""
    mat = _mat('bamboo')
    half_w = PLATFORM_W / 2 - 0.5
    half_l = PLATFORM_L / 2 - 0.5
    positions = [(-half_w, -half_l), (half_w, -half_l), (-half_w, half_l), (half_w, half_l)]
    base_z = DECK_ELEVATION_M
    for i, (dx, dy) in enumerate(positions):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=_COLUMN_RADIUS,
            depth=COLUMN_HEIGHT_M,
            location=(ox + dx, oy + dy, base_z + COLUMN_HEIGHT_M / 2.0),
            vertices=12,
        )
        obj = bpy.context.active_object
        obj.name = f'Labrisa_Column_{i}'
        if mat is not None:
            assign(obj, mat)
        _link(obj, col)


def _deck(col, ox, oy):
    """Bamboo deck split around a central creek channel."""
    mat = _mat('bamboo')
    z = DECK_ELEVATION_M
    deck_segment_w = PLATFORM_W
    deck_segment_l = (PLATFORM_L - CREEK_WIDTH_M) / 2.0
    # South half (deck toward viewer)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox, oy - (CREEK_WIDTH_M / 2 + deck_segment_l / 2), z))
    south = bpy.context.active_object
    south.name = 'Labrisa_Deck_South'
    south.scale = (deck_segment_w, deck_segment_l, _DECK_THICKNESS)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        assign(south, mat)
    _link(south, col)
    # North half
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox, oy + (CREEK_WIDTH_M / 2 + deck_segment_l / 2), z))
    north = bpy.context.active_object
    north.name = 'Labrisa_Deck_North'
    north.scale = (deck_segment_w, deck_segment_l, _DECK_THICKNESS)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        assign(north, mat)
    _link(north, col)


def _ring_beam(col, ox, oy):
    """Lapacho ring beam under the deck (joists)."""
    mat = _mat('lapacho_timber')
    z = DECK_ELEVATION_M - 0.12
    half_w = PLATFORM_W / 2 - 0.5
    # 4 joists along the long axis
    for i in range(4):
        x_frac = -0.75 + 0.5 * i
        x = ox + x_frac * (half_w * 2 / 3.0)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, oy, z))
        obj = bpy.context.active_object
        obj.name = f'Labrisa_Joist_{i}'
        obj.scale = (0.10, PLATFORM_L, 0.18)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if mat is not None:
            assign(obj, mat)
        _link(obj, col)


def _roof(col, ox, oy):
    """Low-pitch hipped palm thatch roof on the bamboo frame."""
    pitch_rad = math.radians(ROOF_PITCH_DEG)
    eave_z = DECK_ELEVATION_M + COLUMN_HEIGHT_M
    half_w = PLATFORM_W / 2 + _ROOF_EAVE_OVERHANG
    half_l = PLATFORM_L / 2 + _ROOF_EAVE_OVERHANG
    ridge_half_l = max((PLATFORM_L / 2) - (PLATFORM_W / 2) * 0.4, 0.3)
    ridge_z = eave_z + math.tan(pitch_rad) * (PLATFORM_W / 2)

    verts = [
        (ox - half_w, oy - half_l, eave_z),
        (ox + half_w, oy - half_l, eave_z),
        (ox + half_w, oy + half_l, eave_z),
        (ox - half_w, oy + half_l, eave_z),
        (ox, oy - ridge_half_l, ridge_z),
        (ox, oy + ridge_half_l, ridge_z),
    ]
    faces = [
        (0, 1, 4),
        (2, 3, 5),
        (1, 2, 5, 4),
        (3, 0, 4, 5),
    ]
    mesh = bpy.data.meshes.new('Labrisa_Roof_Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new('Labrisa_Roof', mesh)
    mat = _mat('palm_thatch') or _mat('sod_canopy') or _mat('canopy')
    if mat is not None:
        assign(obj, mat)
    col.objects.link(obj)


def _creek(col, ox, oy):
    """Creek bed running E-W through the deck — flat dark water surface.

    Reads as a 1.5 m wide creek channel at grade. The cascade weir at the
    east end provides the audio focal point.
    """
    mat = _mat('water_reflective') or _mat('pv_glass') or _mat('glass')
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox, oy, 0.02))
    obj = bpy.context.active_object
    obj.name = 'Labrisa_Creek_Surface'
    obj.scale = (PLATFORM_W + 3.0, CREEK_WIDTH_M, 0.04)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)


def _lanterns(col, ox, oy):
    """LANTERN_COUNT glass-bowl pendants in a 3×3 grid below the roof."""
    z_hang = DECK_ELEVATION_M + COLUMN_HEIGHT_M - 0.6
    cols_n = 3
    rows_n = 3
    span_x = PLATFORM_W - 2.0
    span_y = PLATFORM_L - 2.0
    for i in range(cols_n):
        for j in range(rows_n):
            x = ox - span_x / 2 + (span_x / (cols_n - 1)) * i
            y = oy - span_y / 2 + (span_y / (rows_n - 1)) * j
            _grammar.glass_bowl_lantern(
                col,
                location=(x, y, z_hang),
                bowl_radius_m=0.10,
                suspension_length_m=0.7,
                name_prefix=f'Labrisa_Lantern_{i}_{j}',
            )


def _append_boulder_mesh(blend_path: str, target_col: bpy.types.Collection) -> bpy.types.Object | None:
    """Append the largest mesh object from ``blend_path`` and link to ``target_col``.

    Silent log + skip when the asset is missing — matches the hard constraint
    that the build must not fail on absent CC0 downloads. Returns the linked
    object on success, ``None`` otherwise.
    """
    if not os.path.exists(blend_path):
        print(f"[labrisa_lounge] missing boulder asset {blend_path}, skipping")
        return None
    before = set(bpy.data.objects.keys())
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        data_to.objects = list(data_from.objects)
    new_objs = [bpy.data.objects[n] for n in bpy.data.objects.keys() if n not in before]
    mesh_objs = [o for o in new_objs if o.type == 'MESH' and o.data is not None]
    if not mesh_objs:
        print(f"[labrisa_lounge] no mesh in {blend_path}, skipping")
        return None
    mesh_objs.sort(key=lambda o: len(o.data.polygons), reverse=True)
    hero = mesh_objs[0]
    for o in new_objs:
        for c in list(o.users_collection):
            try:
                c.objects.unlink(o)
            except RuntimeError:
                pass
    target_col.objects.link(hero)
    return hero


def _add_boulder_seating(parent_collection: bpy.types.Collection, center, radius: float = 3.0, count: int = 6):
    """Photoreal boulder seating cluster dressed onto the lounge's west edge.

    Adds ``count`` (default 6) Poly Haven CC0 boulders in a loose semicircle
    around ``center`` at ``radius`` metres. Mirrors the placement logic of
    :mod:`lqv.subscene.boulder_cluster` so the sub-render preview matches
    what lands in the final composite. Uses the seeded RNG (must already be
    set up by the caller — Labrisa is invoked downstream of
    ``materials.build_materials`` + ``random.seed`` in ``build_scene.py``).
    """
    count = max(3, min(8, count))
    cx, cy = center
    z = 0.0  # boulders sit on grade — deck is at DECK_ELEVATION_M above them
    surround_keys = ['large', 'medium_a', 'medium_b', 'small', 'medium_a', 'medium_b', 'small', 'small']
    arc_start_deg = 100.0   # facing west, away from the deck
    arc_span_deg = 200.0

    placed: list[bpy.types.Object] = []
    for i in range(count):
        t = i / max(count - 1, 1)
        angle_rad = math.radians(arc_start_deg + t * arc_span_deg)
        r_jit = radius + random.uniform(-0.4, 0.4)
        x = cx + r_jit * math.cos(angle_rad)
        y = cy + r_jit * math.sin(angle_rad)
        key = surround_keys[i % len(surround_keys)]
        obj = _append_boulder_mesh(_BOULDER_BLENDS[key], parent_collection)
        if obj is None:
            continue
        obj.name = f'Labrisa_BoulderCluster_{i:02d}'
        obj.location = (x, y, z)
        obj.rotation_euler = (
            random.uniform(-0.15, 0.15),
            random.uniform(-0.15, 0.15),
            random.uniform(0.0, 2.0 * math.pi),
        )
        s = 1.0 + random.uniform(-0.20, 0.20)
        obj.scale = (s, s, s)
        placed.append(obj)
    return placed


def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    """Build the Labrisa Lounge amenity at ``location``."""
    name = 'LabrisaLounge'
    col = _ensure_collection(name, parent)
    ox, oy, _oz = location
    _columns(col, ox, oy)
    _ring_beam(col, ox, oy)
    _deck(col, ox, oy)
    _creek(col, ox, oy)
    _roof(col, ox, oy)
    _lanterns(col, ox, oy)
    # Cascade weir at the upstream (east) end of the creek
    _grammar.cascade_weir(
        col,
        center=(ox + PLATFORM_W / 2 + 0.5, oy),
        width_m=CREEK_WIDTH_M + 0.4,
        height_m=CASCADE_WEIR_HEIGHT_M,
        thickness_m=0.30,
        name_prefix='Labrisa_Weir',
    )
    # Stepping stones — two crossings, one at each creek edge
    _grammar.stepping_stones(
        col,
        start=(ox - PLATFORM_W / 2 - 0.4, oy - CREEK_WIDTH_M / 2 - 0.2),
        end=(ox - PLATFORM_W / 2 - 0.4, oy + CREEK_WIDTH_M / 2 + 0.2),
        count=5,
        stone_radius_m=0.30,
        stone_height_m=0.15,
        name_prefix='Labrisa_Step_W',
    )
    _grammar.stepping_stones(
        col,
        start=(ox + PLATFORM_W / 2 + 0.4, oy - CREEK_WIDTH_M / 2 - 0.2),
        end=(ox + PLATFORM_W / 2 + 0.4, oy + CREEK_WIDTH_M / 2 + 0.2),
        count=5,
        stone_radius_m=0.30,
        stone_height_m=0.15,
        name_prefix='Labrisa_Step_E',
    )
    # Boulder seating arc on the south deck facing the creek
    _grammar.boulder_seating(
        col,
        center=(ox, oy - CREEK_WIDTH_M / 2 - 1.5),
        arc_radius_m=2.2,
        boulder_count=4,
        boulder_radius_m=0.45,
        arc_span_deg=140.0,
        name_prefix='Labrisa_Boulder_S',
    )
    _grammar.boulder_seating(
        col,
        center=(ox, oy + CREEK_WIDTH_M / 2 + 1.5),
        arc_radius_m=2.2,
        boulder_count=4,
        boulder_radius_m=0.45,
        arc_span_deg=140.0,
        name_prefix='Labrisa_Boulder_N',
    )
    # Photoreal boulder cluster on the west (down-creek) side — large hero
    # stone + namaqualand companions, reads as informal gathering ring just
    # off the deck edge. Skipped gracefully if the .blend assets are missing.
    _add_boulder_seating(
        col,
        center=(ox - PLATFORM_W / 2 - 3.5, oy),
        radius=3.0,
        count=6,
    )
    return col
