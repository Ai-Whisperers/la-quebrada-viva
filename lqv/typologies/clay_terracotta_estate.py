"""Typology — Clay Terracotta Estate (African-modern two-storey).

Wesley reference: a two-storey rural villa with clay-plaster walls, terracotta
pitched roof, and a deep latticed timber screen at the upper veranda. Raised
stone foundation (Rule 4); 1.2 m overhanging eaves on all sides (Rule 5); one
gable end shows the underlying clay-block masonry as a tactile contrast.

Footprint ~10.0 × 8.0 m; ground floor + first floor; total height ~7.0 m.
House-scale (sub-render via base.run, HOUSE_CLIP_END_M).
"""
from __future__ import annotations

import math

import bpy

from lqv.furniture import furnish_interior
from lqv.materials import MAT, assign

# ----- public sizing -----
FOOTPRINT_W = 10.0
FOOTPRINT_D = 8.0
FLOOR1_H = 3.2
FLOOR2_H = 2.9
ROOF_PITCH_DEG = 28.0
EAVE_OVERHANG = 1.20
PLINTH_H = 0.45
SPECIES = 'handroanthus_impetiginosus + clay_plaster + terracotta'
SNAP = 'pad'
NOTES = (
    'Two-storey clay-plaster villa on raised sandstone plinth.',
    'Pitched terracotta-tile roof with 1.2 m overhanging eaves on all sides.',
    'Latticed lapacho-timber privacy screen across upper veranda.',
    'One gable end keeps clay-block masonry exposed for tactile contrast.',
)

# Geometry constants
_PLINTH_OVERHANG = 0.30
_WALL_THK = 0.30
_SCREEN_RADIUS = 0.035
_SCREEN_LATH_PITCH = 0.16
_EAVE_THK = 0.10
_TILE_THK = 0.04
_WINDOW_W = 1.20
_WINDOW_H = 1.40
_DOOR_W = 1.10
_DOOR_H = 2.10
_BALCONY_DEPTH = 1.20
_BALCONY_RAIL_H = 1.05

MATERIAL_TAKEOFF: dict = {
    'clay_plaster': {'area_m2': 220.0, 'unit_cost_usd': 8.0},
    'clay_block': {'count': 480, 'unit_cost_usd': 1.10},
    'terracotta_tile': {'area_m2': 130.0, 'unit_cost_usd': 28.0},
    'lapacho_timber': {'volume_m3': 1.40, 'unit_cost_usd': 1800.0},
    'sandstone': {'volume_m3': 6.50, 'unit_cost_usd': 220.0},
    'glass_panes': {'area_m2': 18.0, 'unit_cost_usd': 60.0},
    'rebar_anchors': {'count': 120, 'unit_cost_usd': 2.0},
}


def _ensure_collection(name: str, parent) -> bpy.types.Collection:
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(col)
    return col


def _link(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def _mat(key, fallback=None):
    m = MAT.get(key)
    if m is None and fallback is not None:
        m = MAT.get(fallback)
    return m


def _add_box(col, name, location, scale, material_key, fallback=None):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = _mat(material_key, fallback)
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _add_plinth(col, ox, oy, oz):
    pw = FOOTPRINT_W + 2 * _PLINTH_OVERHANG
    pd = FOOTPRINT_D + 2 * _PLINTH_OVERHANG
    _add_box(col, 'Estate_Plinth',
             (ox, oy, oz + PLINTH_H / 2.0),
             (pw, pd, PLINTH_H),
             'sandstone')


def _add_floor_walls(col, ox, oy, base_z, height, gable_block_side, label):
    """Four perimeter walls — three clay-plaster, one (gable_block_side) exposed clay-block."""
    half_w = FOOTPRINT_W / 2.0
    half_d = FOOTPRINT_D / 2.0
    z = base_z + height / 2.0

    walls = [
        ('S', (ox, oy - half_d, z), (FOOTPRINT_W, _WALL_THK, height)),
        ('N', (ox, oy + half_d, z), (FOOTPRINT_W, _WALL_THK, height)),
        ('W', (ox - half_w, oy, z), (_WALL_THK, FOOTPRINT_D, height)),
        ('E', (ox + half_w, oy, z), (_WALL_THK, FOOTPRINT_D, height)),
    ]
    for side, loc, scl in walls:
        key = 'clay_block' if side == gable_block_side else 'clay_plaster'
        _add_box(col, f'Estate_Wall_{label}_{side}', loc, scl, key)


def _add_floor_slab(col, ox, oy, z, name):
    _add_box(col, name,
             (ox, oy, z + 0.10 / 2.0),
             (FOOTPRINT_W, FOOTPRINT_D, 0.10),
             'concrete_slab_108', fallback='sandstone')


def _add_door(col, ox, oy, base_z, name):
    half_d = FOOTPRINT_D / 2.0
    _add_box(col, name,
             (ox, oy - half_d - 0.01, base_z + _DOOR_H / 2.0),
             (_DOOR_W, 0.06, _DOOR_H),
             'lapacho_timber')


def _add_window(col, x, y, base_z, height_offset, w, h, name):
    z = base_z + height_offset + h / 2.0
    _add_box(col, name, (x, y, z), (w, 0.05, h), 'window_glow', fallback='pv_glass')


def _add_eave(col, ox, oy, ridge_z, pitch_rad, name_prefix):
    """Pitched roof made of two sloped slabs + two gable triangles approximated by tilted boxes."""
    span = FOOTPRINT_D + 2 * EAVE_OVERHANG
    slope_len = span / 2.0 / math.cos(pitch_rad)
    rafter_w = FOOTPRINT_W + 2 * EAVE_OVERHANG
    # Two sloped slabs (N and S).
    for side, sign in (('S', -1), ('N', +1)):
        cy = oy + sign * (span / 4.0) * math.cos(pitch_rad)
        cz = ridge_z - (span / 4.0) * math.sin(pitch_rad)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox, cy, cz))
        obj = bpy.context.active_object
        obj.name = f'{name_prefix}_Slab_{side}'
        obj.scale = (rafter_w, slope_len, _TILE_THK)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        obj.rotation_euler = (sign * pitch_rad, 0.0, 0.0)
        mat = _mat('terracotta_tile')
        if mat is not None:
            assign(obj, mat)
        _link(obj, col)
    # Eave underside trim (lapacho) all around.
    _add_box(col, f'{name_prefix}_EaveTrim_S',
             (ox, oy - FOOTPRINT_D / 2.0 - EAVE_OVERHANG / 2.0,
              ridge_z - (span / 4.0) * math.sin(pitch_rad) - _EAVE_THK),
             (rafter_w, EAVE_OVERHANG, _EAVE_THK), 'lapacho_timber')
    _add_box(col, f'{name_prefix}_EaveTrim_N',
             (ox, oy + FOOTPRINT_D / 2.0 + EAVE_OVERHANG / 2.0,
              ridge_z - (span / 4.0) * math.sin(pitch_rad) - _EAVE_THK),
             (rafter_w, EAVE_OVERHANG, _EAVE_THK), 'lapacho_timber')


def _add_screen(col, x, y, base_z, length, height, axis, name):
    """Latticed lapacho privacy screen — series of vertical battens."""
    count = max(2, int(length / _SCREEN_LATH_PITCH))
    span = (count - 1) * _SCREEN_LATH_PITCH
    for i in range(count):
        t = i * _SCREEN_LATH_PITCH - span / 2.0
        if axis == 'x':
            loc = (x + t, y, base_z + height / 2.0)
        else:
            loc = (x, y + t, base_z + height / 2.0)
        bpy.ops.mesh.primitive_cylinder_add(radius=_SCREEN_RADIUS, depth=height,
                                            location=loc)
        obj = bpy.context.active_object
        obj.name = f'{name}_{i:02d}'
        mat = _mat('lapacho_timber')
        if mat is not None:
            assign(obj, mat)
        _link(obj, col)
    # Top and bottom rails
    if axis == 'x':
        rail_scale = (length, 0.06, 0.06)
    else:
        rail_scale = (0.06, length, 0.06)
    for label, z_off in (('Top', height - 0.03), ('Bot', 0.03)):
        if axis == 'x':
            loc = (x, y, base_z + z_off)
        else:
            loc = (x, y, base_z + z_off)
        _add_box(col, f'{name}_Rail_{label}', loc, rail_scale, 'lapacho_timber')


def _add_balcony(col, ox, oy, base_z, name):
    # Decking
    _add_box(col, f'{name}_Deck',
             (ox, oy - FOOTPRINT_D / 2.0 - _BALCONY_DEPTH / 2.0, base_z + 0.05),
             (FOOTPRINT_W * 0.7, _BALCONY_DEPTH, 0.10),
             'lapacho_timber')
    # Privacy screen along the south edge of the balcony.
    _add_screen(col, ox, oy - FOOTPRINT_D / 2.0 - _BALCONY_DEPTH + 0.05,
                base_z + 0.10,
                FOOTPRINT_W * 0.7, _BALCONY_RAIL_H, axis='x',
                name=f'{name}_Screen')


def build_clay_terracotta_estate(origin=(0.0, 0.0, 0.0), variant: str = 'A'):
    """Build the two-storey clay-terracotta estate at ``origin``.

    Entry-facing axis: -Y (south). Returns the holding collection.
    """
    ox, oy, oz = origin
    col = _ensure_collection('ClayTerracottaEstate', None)

    # 1. Raised stone plinth (Rule 4).
    _add_plinth(col, ox, oy, oz)
    plinth_top = oz + PLINTH_H

    # 2. Ground floor.
    _add_floor_slab(col, ox, oy, plinth_top, 'Estate_Slab_GF')
    _add_floor_walls(col, ox, oy, plinth_top + 0.10, FLOOR1_H,
                     gable_block_side='E', label='GF')
    _add_door(col, ox, oy, plinth_top + 0.10, 'Estate_Door_GF')
    # Three south windows
    for i, dx in enumerate((-3.0, +3.0)):
        _add_window(col, ox + dx, oy - FOOTPRINT_D / 2.0 - 0.01,
                    plinth_top + 0.10, 0.95,
                    _WINDOW_W, _WINDOW_H,
                    f'Estate_Window_GF_S_{i}')

    # 3. First floor.
    f2_base = plinth_top + 0.10 + FLOOR1_H
    _add_floor_slab(col, ox, oy, f2_base, 'Estate_Slab_F2')
    _add_floor_walls(col, ox, oy, f2_base + 0.10, FLOOR2_H,
                     gable_block_side='E', label='F2')
    # Four south windows on the upper floor (later screened by the lattice).
    for i, dx in enumerate((-3.5, -1.2, +1.2, +3.5)):
        _add_window(col, ox + dx, oy - FOOTPRINT_D / 2.0 - 0.01,
                    f2_base + 0.10, 0.50,
                    1.05, 1.65,
                    f'Estate_Window_F2_S_{i}')

    # 4. Pitched terracotta roof.
    wall_top = f2_base + 0.10 + FLOOR2_H
    pitch = math.radians(ROOF_PITCH_DEG)
    ridge_z = wall_top + (FOOTPRINT_D / 2.0) * math.tan(pitch)
    _add_eave(col, ox, oy, ridge_z, pitch, 'Estate_Roof')

    # 5. Upper balcony + latticed privacy screen across the south facade.
    _add_balcony(col, ox, oy, f2_base + 0.10, 'Estate_BalconyS')

    # P1.B.1 — interior furniture stubs (RENDER_VIEW=interior readable).
    furnish_interior(
        col,
        footprint_w=FOOTPRINT_W - 2.0,
        footprint_l=FOOTPRINT_D - 2.0,
        origin_xy=(ox, oy),
        floor_z=plinth_top + 0.10,
        pax=4,
        style='stone',
        variant=variant,
        name_prefix='CTE_Furn',
    )

    return col


# Back-compat: standard typology signature.
def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    return build_clay_terracotta_estate(origin=location, variant=variant)
