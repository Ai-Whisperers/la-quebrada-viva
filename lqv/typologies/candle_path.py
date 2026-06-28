"""Typology — Candle Path (amenity, walkway with paired lantern posts).

Wesley reference: a curving night-time approach path made of sandstone stepping
stones, lit by paired short lantern posts every 1.5 m. Each lantern is a small
lapacho box with a `window_glow`-textured emissive panel. A sparse drift of
fireflies hangs above the path height.

Path length default ~6 m, width ~0.9 m. House-scale amenity.
"""
from __future__ import annotations

import math
import random

import bpy

from lqv.materials import MAT, assign

# ----- public sizing -----
PATH_LENGTH = 6.0
PATH_WIDTH = 0.90
STEP_PITCH = 0.50               # along-path spacing of stepping stones
LANTERN_PITCH = 1.50            # along-path spacing of lantern PAIRS
LANTERN_OFFSET = PATH_WIDTH / 2.0 + 0.15
LANTERN_POST_H = 0.55
SPECIES = 'sandstone + lapacho + fireflies'
SNAP = 'pad'
NOTES = (
    'Stepping stones of irregular flat sandstone (50 cm pitch along path).',
    'Paired lantern posts every 1.50 m, 55 cm tall, lapacho with emissive face.',
    'Sparse firefly sprite scatter overhead (40 fireflies along path).',
)

# Geometry constants
_STEP_THK = 0.06
_STEP_RADIUS_MIN = 0.22
_STEP_RADIUS_MAX = 0.30
_POST_W = 0.10
_LANTERN_W = 0.16
_LANTERN_H = 0.20
_FIREFLY_RADIUS = 0.012
_FIREFLY_COUNT = 40

MATERIAL_TAKEOFF: dict = {
    'sandstone': {'count': 14, 'unit_cost_usd': 8.0},
    'lapacho_timber': {'volume_m3': 0.05, 'unit_cost_usd': 1800.0},
    'lantern_glow_panels': {'count': 8, 'unit_cost_usd': 5.0},
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


def _add_step(col, x, y, z, rng, name):
    r = rng.uniform(_STEP_RADIUS_MIN, _STEP_RADIUS_MAX)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=r, depth=_STEP_THK,
        vertices=10,
        location=(x, y, z + _STEP_THK / 2.0),
    )
    obj = bpy.context.active_object
    obj.name = name
    # Squash slightly to elliptical so stones don't look stamped.
    sx = rng.uniform(0.85, 1.15)
    sy = rng.uniform(0.85, 1.15)
    obj.scale = (sx, sy, 1.0)
    obj.rotation_euler = (0.0, 0.0, rng.uniform(0.0, math.pi))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    mat = _mat('sandstone', 'stream_bed')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _add_lantern(col, x, y, base_z, name_prefix):
    """A lapacho post topped with an emissive box (window_glow material)."""
    # Post
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(x, y, base_z + LANTERN_POST_H / 2.0),
    )
    post = bpy.context.active_object
    post.name = f'{name_prefix}_Post'
    post.scale = (_POST_W, _POST_W, LANTERN_POST_H)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat_post = _mat('lapacho_timber')
    if mat_post is not None:
        assign(post, mat_post)
    _link(post, col)

    # Lantern head — emissive panel
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(x, y, base_z + LANTERN_POST_H + _LANTERN_H / 2.0),
    )
    head = bpy.context.active_object
    head.name = f'{name_prefix}_Head'
    head.scale = (_LANTERN_W, _LANTERN_W, _LANTERN_H)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mat_head = _mat('window_glow', 'pv_glass')
    if mat_head is not None:
        assign(head, mat_head)
    _link(head, col)


def _add_firefly(col, x, y, z, name):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=1, radius=_FIREFLY_RADIUS, location=(x, y, z))
    obj = bpy.context.active_object
    obj.name = name
    mat = _mat('firefly', 'window_glow')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)


def build_candle_path(origin=(0.0, 0.0, 0.0), length=None):
    """Build the candle-lit stepping path at ``origin`` extending along +Y.

    Optional ``length`` overrides PATH_LENGTH for the run.
    Returns the holding collection.
    """
    ox, oy, oz = origin
    path_len = length if length is not None else PATH_LENGTH
    col = _ensure_collection('CandlePath', None)
    rng = random.Random(0xC4D1)

    # 1. Stepping stones along +Y.
    step_count = max(2, int(path_len / STEP_PITCH))
    for i in range(step_count):
        # Slight zig-zag for natural feel.
        zig = (i % 2) * 0.06 - 0.03
        sx = ox + zig + rng.uniform(-0.04, 0.04)
        sy = oy + i * STEP_PITCH + rng.uniform(-0.03, 0.03)
        _add_step(col, sx, sy, oz, rng, f'CandlePath_Step_{i:02d}')

    # 2. Paired lantern posts every LANTERN_PITCH.
    pair_count = max(2, int(path_len / LANTERN_PITCH) + 1)
    for i in range(pair_count):
        ly = oy + i * LANTERN_PITCH
        _add_lantern(col, ox - LANTERN_OFFSET, ly, oz, f'CandlePath_LanternW_{i}')
        _add_lantern(col, ox + LANTERN_OFFSET, ly, oz, f'CandlePath_LanternE_{i}')

    # 3. Sparse firefly drift above the path (0.6 — 1.8 m).
    for i in range(_FIREFLY_COUNT):
        fx = ox + rng.uniform(-PATH_WIDTH, PATH_WIDTH)
        fy = oy + rng.uniform(0.0, path_len)
        fz = oz + rng.uniform(0.6, 1.8)
        _add_firefly(col, fx, fy, fz, f'CandlePath_Firefly_{i:02d}')

    return col


# Back-compat: standard typology signature.
def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    return build_candle_path(origin=location)
