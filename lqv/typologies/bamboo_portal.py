"""Typology — Bamboo Portal (entry gateway).

Wesley reference: timber-and-bamboo gateway marking the housing-park entry.
Two lapacho posts flank a 2.4 m clear opening, joined by a lapacho lintel and
roofed by 12 horizontal bamboo culms forming a slatted pergola. Decorative
vertical bamboo culms hug each post, lashed with hemp rope. Two sandstone
plinths raise the timber off ground (Rule 4 analog: timber never touches
laterite mud).

Footprint ~3.2 × 0.8 m. House-scale (no platform, no interior).
"""
from __future__ import annotations

import math

import bpy

from lqv.materials import MAT, assign

# ----- public sizing constants -----
FOOTPRINT_M2 = 2.6
CLEAR_OPENING_M = 2.4
POST_HEIGHT_M = 3.0
LINTEL_HEIGHT_M = 2.8
SPECIES = 'guadua_angustifolia + handroanthus_impetiginosus'
SNAP = 'pad'
NOTES = (
    'Two lapacho posts 20×20 cm, 3.0 m tall, on sandstone plinths.',
    'Lapacho lintel beam 22×18 cm spanning 3.0 m at z=2.8 m.',
    '12 bamboo-culm slats laid horizontally above the lintel as pergola roof.',
    '4 decorative vertical bamboo culms — 2 per post — lashed with hemp rope.',
    'Mounted on raised sandstone plinths 40×40 cm × 30 cm to lift timber off mud.',
)

# Geometry constants
_POST_SECTION = 0.20            # 20 cm square post
_POST_X = CLEAR_OPENING_M / 2.0 + _POST_SECTION / 2.0     # = 1.30 m from center
_LINTEL_LEN = 2 * _POST_X + _POST_SECTION                 # 3.0 m
_LINTEL_W = 0.18
_LINTEL_H = 0.22
_PLINTH_W = 0.40
_PLINTH_H = 0.30
_SLAT_COUNT = 12
_SLAT_RADIUS = 0.045
_SLAT_LEN = 1.40                 # perpendicular to entry direction
_SLAT_PITCH = 0.22               # spacing between bamboo slats
_DECO_CULM_RADIUS = 0.045
_ROPE_RADIUS = 0.015

MATERIAL_TAKEOFF: dict = {
    'lapacho_timber': {'volume_m3': 0.36, 'unit_cost_usd': 1800.0},
    'bamboo_culm': {'length_m': 28.0, 'unit_cost_usd': 6.0},
    'sandstone_plinth': {'volume_m3': 0.10, 'unit_cost_usd': 220.0},
    'rope_hemp': {'length_m': 4.0, 'unit_cost_usd': 3.5},
    'fasteners_hardware': {'count': 24, 'unit_cost_usd': 0.80},
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


def _add_plinth(col, x, y, z, name):
    bpy.ops.mesh.primitive_cube_add(size=1.0,
                                    location=(x, y, z + _PLINTH_H / 2.0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (_PLINTH_W, _PLINTH_W, _PLINTH_H)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = _mat('sandstone')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _add_post(col, x, y, base_z, name):
    bpy.ops.mesh.primitive_cube_add(size=1.0,
                                    location=(x, y, base_z + POST_HEIGHT_M / 2.0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (_POST_SECTION, _POST_SECTION, POST_HEIGHT_M)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = _mat('lapacho_timber')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _add_lintel(col, ox, oy, base_z, name):
    z = base_z + LINTEL_HEIGHT_M + _LINTEL_H / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox, oy, z))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (_LINTEL_LEN, _LINTEL_W, _LINTEL_H)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat = _mat('lapacho_timber')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _add_bamboo_slat(col, ox, oy, z, name):
    """Single horizontal bamboo culm perpendicular to entry direction."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=_SLAT_RADIUS,
        depth=_SLAT_LEN,
        location=(ox, oy, z),
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = (math.radians(90.0), 0.0, 0.0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    mat = _mat('bamboo_culm', 'bamboo')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _add_deco_culm(col, x, y, base_z, name):
    """Decorative vertical bamboo culm flanking a post."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=_DECO_CULM_RADIUS,
        depth=POST_HEIGHT_M,
        location=(x, y, base_z + POST_HEIGHT_M / 2.0),
    )
    obj = bpy.context.active_object
    obj.name = name
    mat = _mat('bamboo_culm', 'bamboo')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _add_rope_tie(col, x, y, z, name):
    """Visible rope wrap around a bamboo-post junction (torus)."""
    bpy.ops.mesh.primitive_torus_add(
        major_radius=_POST_SECTION * 0.75,
        minor_radius=_ROPE_RADIUS,
        location=(x, y, z),
    )
    obj = bpy.context.active_object
    obj.name = name
    mat = _mat('rope_natural', 'lapacho_bark')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def build_bamboo_portal(origin=(0.0, 0.0, 0.0)):
    """Build the bamboo entry portal at ``origin``.

    Entry axis is +Y (slats run along X).
    Returns the collection holding every part.
    """
    ox, oy, oz = origin
    col = _ensure_collection('BambooPortal', None)

    plinth_top_z = oz + _PLINTH_H

    # 1. Two sandstone plinths.
    _add_plinth(col, ox - _POST_X, oy, oz, 'Portal_PlinthW')
    _add_plinth(col, ox + _POST_X, oy, oz, 'Portal_PlinthE')

    # 2. Two lapacho posts.
    _add_post(col, ox - _POST_X, oy, plinth_top_z, 'Portal_PostW')
    _add_post(col, ox + _POST_X, oy, plinth_top_z, 'Portal_PostE')

    # 3. Lintel beam at z = plinth_top + 2.8 m.
    _add_lintel(col, ox, oy, plinth_top_z, 'Portal_Lintel')

    # 4. 12 bamboo slat pergola above lintel.
    slat_base_z = plinth_top_z + LINTEL_HEIGHT_M + _LINTEL_H + _SLAT_RADIUS
    span_x = (_SLAT_COUNT - 1) * _SLAT_PITCH
    for i in range(_SLAT_COUNT):
        sx = ox - span_x / 2.0 + i * _SLAT_PITCH
        _add_bamboo_slat(col, sx, oy, slat_base_z, f'Portal_Slat_{i:02d}')

    # 5. 4 decorative vertical bamboo culms, 2 per post.
    deco_offset = _POST_SECTION / 2.0 + _DECO_CULM_RADIUS + 0.01
    for side, sx in (('W', ox - _POST_X), ('E', ox + _POST_X)):
        _add_deco_culm(col, sx, oy - deco_offset, plinth_top_z,
                       f'Portal_DecoCulm_{side}_S')
        _add_deco_culm(col, sx, oy + deco_offset, plinth_top_z,
                       f'Portal_DecoCulm_{side}_N')

    # 6. Rope ties at top + mid of each post junction.
    for side, sx in (('W', ox - _POST_X), ('E', ox + _POST_X)):
        for label, z_off in (('Top', 0.20), ('Mid', POST_HEIGHT_M * 0.55)):
            _add_rope_tie(col, sx, oy, plinth_top_z + POST_HEIGHT_M - z_off,
                          f'Portal_Rope_{side}_{label}')

    return col


# Back-compat: keep the standard typology signature alive.
def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    return build_bamboo_portal(origin=location)
