"""Typology — Bamboo Outdoor Shower (amenity).

Wesley reference: an outdoor garden shower booth with four bamboo culm corner
posts, woven bamboo half-wall privacy panels (~1.6 m high), a steel showerhead
arm mounted to the eastern post, a lapacho duckboard floor, and a perimeter of
river stones acting as a drain field.

Footprint ~1.6 × 1.6 m, total height ~2.4 m. House-scale, open-roof.
"""
from __future__ import annotations

import math
import random

import bpy

from lqv.materials import MAT, assign

# ----- public sizing -----
FOOTPRINT_W = 1.6
FOOTPRINT_D = 1.6
TOTAL_HEIGHT = 2.4
PRIVACY_PANEL_H = 1.6
SPECIES = 'guadua_angustifolia + handroanthus_impetiginosus'
SNAP = 'pad'
NOTES = (
    'Four bamboo culm corner posts (~Ø 80 mm).',
    'Three sides clad with woven bamboo half-wall privacy panels, 1.6 m tall.',
    'Open south face for entry.',
    'Steel showerhead arm cantilevered from the east post at 2.1 m.',
    'Lapacho duckboard floor on a river-stone drain bed.',
)

# Geometry constants
_POST_RADIUS = 0.040
_POST_HEIGHT = TOTAL_HEIGHT
_PANEL_THK = 0.05
_PANEL_OFFSET_Z = 0.30        # bottom of panel above ground
_DUCKBOARD_THK = 0.04
_DUCKBOARD_GAP = 0.012
_DUCKBOARD_COUNT = 11
_SHOWER_ARM_LEN = 0.55
_SHOWER_ARM_RADIUS = 0.015
_SHOWER_HEAD_RADIUS = 0.075
_STONE_COUNT = 28
_STONE_RADIUS_MIN = 0.05
_STONE_RADIUS_MAX = 0.10

MATERIAL_TAKEOFF: dict = {
    'bamboo_culm': {'length_m': 9.6 + 14.0, 'unit_cost_usd': 6.0},
    'lapacho_timber': {'volume_m3': 0.04, 'unit_cost_usd': 1800.0},
    'sandstone_drain': {'volume_m3': 0.15, 'unit_cost_usd': 100.0},
    'steel_arm': {'count': 1, 'unit_cost_usd': 28.0},
    'rope_hemp': {'length_m': 5.0, 'unit_cost_usd': 3.5},
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


def _add_post(col, x, y, base_z, name):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=_POST_RADIUS,
        depth=_POST_HEIGHT,
        location=(x, y, base_z + _POST_HEIGHT / 2.0),
    )
    obj = bpy.context.active_object
    obj.name = name
    mat = _mat('bamboo_culm', 'bamboo')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _add_panel(col, x, y, base_z, length, height, axis, name):
    z = base_z + _PANEL_OFFSET_Z + height / 2.0
    if axis == 'x':
        scale = (length, _PANEL_THK, height)
    else:
        scale = (_PANEL_THK, length, height)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = _mat('bamboo_culm', 'bamboo')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _add_duckboard(col, ox, oy, base_z, name_prefix):
    span_x = FOOTPRINT_W * 0.9
    span_y = FOOTPRINT_D * 0.9
    plank_w = (span_x - (_DUCKBOARD_COUNT - 1) * _DUCKBOARD_GAP) / _DUCKBOARD_COUNT
    z = base_z + _DUCKBOARD_THK / 2.0
    for i in range(_DUCKBOARD_COUNT):
        x = ox - span_x / 2.0 + plank_w / 2.0 + i * (plank_w + _DUCKBOARD_GAP)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, oy, z))
        obj = bpy.context.active_object
        obj.name = f'{name_prefix}_{i:02d}'
        obj.scale = (plank_w, span_y, _DUCKBOARD_THK)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        mat = _mat('lapacho_timber')
        if mat is not None:
            assign(obj, mat)
        _link(obj, col)


def _add_shower_arm(col, x_post, y_post, base_z, name_prefix):
    """Vertical riser up the east post + horizontal arm + showerhead disc."""
    riser_h = 2.1
    bpy.ops.mesh.primitive_cylinder_add(
        radius=_SHOWER_ARM_RADIUS,
        depth=riser_h,
        location=(x_post + _POST_RADIUS + _SHOWER_ARM_RADIUS + 0.005,
                  y_post, base_z + riser_h / 2.0),
    )
    obj = bpy.context.active_object
    obj.name = f'{name_prefix}_Riser'
    mat = _mat('steel_anodized', 'steel_mesh')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)

    # Horizontal arm pointing into the booth.
    arm_x = x_post + _POST_RADIUS + _SHOWER_ARM_RADIUS + 0.005 - _SHOWER_ARM_LEN / 2.0
    bpy.ops.mesh.primitive_cylinder_add(
        radius=_SHOWER_ARM_RADIUS,
        depth=_SHOWER_ARM_LEN,
        location=(arm_x, y_post, base_z + riser_h + _SHOWER_ARM_RADIUS),
    )
    arm = bpy.context.active_object
    arm.name = f'{name_prefix}_Arm'
    arm.rotation_euler = (0.0, math.radians(90.0), 0.0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    if mat is not None:
        assign(arm, mat)
    _link(arm, col)

    # Showerhead — squat cylinder at the end of the arm.
    head_x = arm_x - _SHOWER_ARM_LEN / 2.0
    bpy.ops.mesh.primitive_cylinder_add(
        radius=_SHOWER_HEAD_RADIUS,
        depth=0.04,
        location=(head_x, y_post, base_z + riser_h + _SHOWER_ARM_RADIUS - 0.04),
    )
    head = bpy.context.active_object
    head.name = f'{name_prefix}_Head'
    if mat is not None:
        assign(head, mat)
    _link(head, col)


def _add_drain_stones(col, ox, oy, base_z, name_prefix):
    """Scatter river stones around the duckboard perimeter."""
    rng = random.Random(0xD3A1)
    for i in range(_STONE_COUNT):
        r = rng.uniform(_STONE_RADIUS_MIN, _STONE_RADIUS_MAX)
        # Pick a point on the perimeter ring.
        angle = rng.uniform(0.0, 2.0 * math.pi)
        ring_r = rng.uniform(FOOTPRINT_W * 0.55, FOOTPRINT_W * 0.78)
        x = ox + ring_r * math.cos(angle)
        y = oy + ring_r * math.sin(angle)
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=2, radius=r, location=(x, y, base_z + r * 0.6))
        obj = bpy.context.active_object
        obj.name = f'{name_prefix}_{i:02d}'
        obj.scale = (1.0, 1.0, 0.55)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        mat = _mat('sandstone', 'stream_bed')
        if mat is not None:
            assign(obj, mat)
        _link(obj, col)


def _add_rope_ring(col, x, y, z, name):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=_POST_RADIUS * 1.4,
        minor_radius=0.012,
        location=(x, y, z),
    )
    obj = bpy.context.active_object
    obj.name = name
    mat = _mat('rope_natural', 'lapacho_bark')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)


def build_bamboo_outdoor_shower(origin=(0.0, 0.0, 0.0)):
    """Build the outdoor shower booth at ``origin``. Entry faces -Y."""
    ox, oy, oz = origin
    col = _ensure_collection('BambooOutdoorShower', None)

    half_w = FOOTPRINT_W / 2.0
    half_d = FOOTPRINT_D / 2.0

    # 1. Four corner posts (NW, NE, SW, SE).
    corners = (
        ('NW', ox - half_w, oy + half_d),
        ('NE', ox + half_w, oy + half_d),
        ('SW', ox - half_w, oy - half_d),
        ('SE', ox + half_w, oy - half_d),
    )
    for label, x, y in corners:
        _add_post(col, x, y, oz, f'Shower_Post_{label}')

    # 2. Three privacy panels (N, W, E). South face open for entry.
    _add_panel(col, ox, oy + half_d, oz, FOOTPRINT_W, PRIVACY_PANEL_H,
               axis='x', name='Shower_Panel_N')
    _add_panel(col, ox - half_w, oy, oz, FOOTPRINT_D, PRIVACY_PANEL_H,
               axis='y', name='Shower_Panel_W')
    _add_panel(col, ox + half_w, oy, oz, FOOTPRINT_D, PRIVACY_PANEL_H,
               axis='y', name='Shower_Panel_E')

    # 3. River-stone drain bed.
    _add_drain_stones(col, ox, oy, oz, 'Shower_Stone')

    # 4. Lapacho duckboard floor (sits just above the stone bed).
    _add_duckboard(col, ox, oy, oz + 0.08, 'Shower_Duck')

    # 5. Steel shower arm + head off the east post.
    _add_shower_arm(col, ox + half_w, oy, oz, 'Shower_Arm')

    # 6. Rope rings at top of each post (decorative).
    for label, x, y in corners:
        _add_rope_ring(col, x, y, oz + _POST_HEIGHT - 0.10,
                       f'Shower_Rope_{label}')

    return col


# Back-compat: standard typology signature.
def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    return build_bamboo_outdoor_shower(origin=location)
