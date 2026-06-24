"""Typology — Bamboo Curved-Roof Villa (signature pavilion).

Wesley reference: a single-room open-facade villa with a long, gently arched
double-curvature roof. Eleven lapacho-ribs sweep front-to-back forming the
arch; the roof skin is palm thatch laid over those ribs. The villa sits on a
raised lapacho deck, with a fully open glass facade to the south.

Footprint ~6.0 × 9.0 m (deck slightly larger). Roof crown ~4.2 m, eave height
~2.4 m. House-scale, single storey.
"""
from __future__ import annotations

import math

import bpy

from lqv.materials import MAT, assign

# ----- public sizing -----
FOOTPRINT_W = 6.0           # along X (rib direction is along Y; ribs span X)
FOOTPRINT_D = 9.0           # along Y (rib pitch along this axis)
DECK_OVERHANG = 0.60
DECK_HEIGHT = 0.60
EAVE_HEIGHT = 2.40
CROWN_HEIGHT = 4.20
RIB_COUNT = 11
SPECIES = 'handroanthus_impetiginosus + palm_thatch'
SNAP = 'pad'
NOTES = (
    'Lapacho deck raised 60 cm above grade (Rule 4 — wood off the laterite).',
    '11 arched lapacho ribs spanning 6 m east-west, pitched 90 cm apart along Y.',
    'Palm-thatch skin laid over ribs; double-curvature read along Y as well.',
    'Open south facade — full-height glass panes between four mullions.',
    'Solid north + east + west walls in lapacho-board with cob infill (here: clay_plaster).',
)

# Geometry
_DECK_THK = 0.10
_RIB_RADIUS = 0.06
_RIB_SEGMENTS = 14            # arc samples per rib
_THATCH_THK = 0.08
_GLASS_THK = 0.04
_WALL_THK = 0.20
_MULLION_W = 0.10
_FOOTING_W = 0.30

MATERIAL_TAKEOFF: dict = {
    'lapacho_timber': {'volume_m3': 2.20, 'unit_cost_usd': 1800.0},
    'palm_thatch': {'area_m2': 95.0, 'unit_cost_usd': 14.0},
    'clay_plaster': {'area_m2': 60.0, 'unit_cost_usd': 8.0},
    'glass_panes': {'area_m2': 14.0, 'unit_cost_usd': 60.0},
    'sandstone_footing': {'volume_m3': 0.80, 'unit_cost_usd': 220.0},
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


def _arch_z(u: float, eave: float, crown: float, half_span: float) -> float:
    """Parabolic arch height at lateral position ``u`` from -half_span to +half_span.

    z(±half_span) = eave; z(0) = crown.
    """
    t = u / half_span
    return crown - (crown - eave) * (t * t)


def _add_arched_rib(col, y_pos, deck_top, name):
    """A single lapacho rib spanning -X to +X with the arch profile."""
    half_w = FOOTPRINT_W / 2.0
    pts = []
    for i in range(_RIB_SEGMENTS + 1):
        u = -half_w + (2.0 * half_w) * (i / _RIB_SEGMENTS)
        z = deck_top + _arch_z(u, EAVE_HEIGHT, CROWN_HEIGHT, half_w)
        pts.append((u, y_pos, z))

    # Build the rib as a connected chain of short cylinders so the curve reads.
    for i in range(len(pts) - 1):
        x0, y0, z0 = pts[i]
        x1, y1, z1 = pts[i + 1]
        mx = 0.5 * (x0 + x1)
        my = 0.5 * (y0 + y1)
        mz = 0.5 * (z0 + z1)
        dx = x1 - x0
        dz = z1 - z0
        seg_len = math.hypot(dx, dz)
        angle = math.atan2(dx, dz)         # rotation about Y axis
        bpy.ops.mesh.primitive_cylinder_add(
            radius=_RIB_RADIUS,
            depth=seg_len,
            location=(mx, my, mz),
        )
        obj = bpy.context.active_object
        obj.name = f'{name}_S{i:02d}'
        obj.rotation_euler = (0.0, angle, 0.0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        mat = _mat('lapacho_timber')
        if mat is not None:
            assign(obj, mat)
        _link(obj, col)


def _add_thatch_panel(col, y_pos, panel_depth, deck_top, name):
    """One ribbon of palm thatch laid between two ribs.

    Approximated as ~_RIB_SEGMENTS short tilted slabs following the arch.
    """
    half_w = FOOTPRINT_W / 2.0
    for i in range(_RIB_SEGMENTS):
        u0 = -half_w + (2.0 * half_w) * (i / _RIB_SEGMENTS)
        u1 = -half_w + (2.0 * half_w) * ((i + 1) / _RIB_SEGMENTS)
        z0 = _arch_z(u0, EAVE_HEIGHT, CROWN_HEIGHT, half_w)
        z1 = _arch_z(u1, EAVE_HEIGHT, CROWN_HEIGHT, half_w)
        mx = 0.5 * (u0 + u1)
        mz = deck_top + 0.5 * (z0 + z1) + _THATCH_THK / 2.0
        slab_dx = u1 - u0
        slab_dz = z1 - z0
        slab_len = math.hypot(slab_dx, slab_dz)
        angle = math.atan2(-slab_dz, slab_dx)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(mx, y_pos, mz))
        obj = bpy.context.active_object
        obj.name = f'{name}_T{i:02d}'
        obj.scale = (slab_len, panel_depth, _THATCH_THK)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        obj.rotation_euler = (0.0, angle, 0.0)
        mat = _mat('palm_thatch', 'sod_canopy')
        if mat is not None:
            assign(obj, mat)
        _link(obj, col)


def build_bamboo_curved_roof_villa(origin=(0.0, 0.0, 0.0)):
    """Build the curved-roof villa at ``origin``. Open facade is -Y."""
    ox, oy, oz = origin
    col = _ensure_collection('BambooCurvedRoofVilla', None)

    half_w = FOOTPRINT_W / 2.0
    half_d = FOOTPRINT_D / 2.0

    # 1. Footings along the perimeter (visible at corners + midpoints).
    footing_z = oz + _FOOTING_W / 2.0
    for fx in (-half_w, 0.0, +half_w):
        for fy in (-half_d, -half_d / 2.0, 0.0, +half_d / 2.0, +half_d):
            if fx == 0.0 and fy not in (-half_d, +half_d):
                continue
            _add_box(col, f'Villa_Footing_{int((fx+10)*10)}_{int((fy+20)*10)}',
                     (ox + fx, oy + fy, footing_z),
                     (_FOOTING_W, _FOOTING_W, _FOOTING_W),
                     'sandstone')

    # 2. Raised lapacho deck.
    deck_w = FOOTPRINT_W + 2 * DECK_OVERHANG
    deck_d = FOOTPRINT_D + 2 * DECK_OVERHANG
    _add_box(col, 'Villa_Deck',
             (ox, oy, oz + DECK_HEIGHT + _DECK_THK / 2.0),
             (deck_w, deck_d, _DECK_THK),
             'lapacho_timber')
    deck_top = oz + DECK_HEIGHT + _DECK_THK

    # 3. Three solid walls (N, W, E) below the eave line in clay_plaster.
    wall_h = EAVE_HEIGHT
    wall_z = deck_top + wall_h / 2.0
    _add_box(col, 'Villa_Wall_N',
             (ox, oy + half_d, wall_z),
             (FOOTPRINT_W, _WALL_THK, wall_h),
             'clay_plaster')
    _add_box(col, 'Villa_Wall_W',
             (ox - half_w, oy, wall_z),
             (_WALL_THK, FOOTPRINT_D, wall_h),
             'clay_plaster')
    _add_box(col, 'Villa_Wall_E',
             (ox + half_w, oy, wall_z),
             (_WALL_THK, FOOTPRINT_D, wall_h),
             'clay_plaster')

    # 4. South facade: glass panes between 4 lapacho mullions.
    mullion_xs = [-half_w + 0.05, -FOOTPRINT_W / 6.0, +FOOTPRINT_W / 6.0,
                  +half_w - 0.05]
    for i, mx in enumerate(mullion_xs):
        _add_box(col, f'Villa_Mullion_{i}',
                 (ox + mx, oy - half_d, deck_top + EAVE_HEIGHT / 2.0),
                 (_MULLION_W, _WALL_THK, EAVE_HEIGHT),
                 'lapacho_timber')
    # Two glass panes between the three gaps (skip the outermost margins).
    for i in range(len(mullion_xs) - 1):
        cx = 0.5 * (mullion_xs[i] + mullion_xs[i + 1])
        pane_w = (mullion_xs[i + 1] - mullion_xs[i]) - _MULLION_W
        _add_box(col, f'Villa_GlassPane_{i}',
                 (ox + cx, oy - half_d, deck_top + EAVE_HEIGHT / 2.0),
                 (pane_w, _GLASS_THK, EAVE_HEIGHT * 0.95),
                 'pv_glass', fallback='window_glow')

    # 5. Arched lapacho ribs along Y.
    rib_pitch = FOOTPRINT_D / (RIB_COUNT - 1)
    rib_ys = [-half_d + i * rib_pitch for i in range(RIB_COUNT)]
    for i, ry in enumerate(rib_ys):
        _add_arched_rib(col, oy + ry, deck_top, f'Villa_Rib_{i:02d}')

    # 6. Palm thatch ribbons between consecutive ribs.
    for i in range(RIB_COUNT - 1):
        y0 = oy + rib_ys[i]
        y1 = oy + rib_ys[i + 1]
        cy = 0.5 * (y0 + y1)
        depth = (y1 - y0) - 2 * _RIB_RADIUS
        _add_thatch_panel(col, cy, depth, deck_top, f'Villa_Thatch_{i:02d}')

    return col


# Back-compat: standard typology signature.
def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    return build_bamboo_curved_roof_villa(origin=location)
