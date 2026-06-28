"""Shared amenity grammar — cascade weir, stepping stones, glass-bowl lanterns.

These three primitives recur across :mod:`labrisa_lounge`,
:mod:`eco_pool` and :mod:`eco_retreat_modern_oasis` per
``docs/TERRAIN_PIVOT.md`` §4.3. Factored here so the vocabulary is one
definition; all three amenities import from this module.

Every function takes a target ``bpy.types.Collection`` plus dimensional
parameters and links the geometry into the collection.

Materials
---------
Old behaviour: ``_mat(key)`` returned ``MAT.get(key)`` and any caller that
forgot to check for ``None`` silently shipped the default principled-white
material — a glass weir would render as a polished white bar and nobody
caught it for two batches because the composite ran the bar under tree
shadow. Two replacements:

- :func:`_require_mat` — for primary materials. Raises ``KeyError`` with
  the registry's available keys so a typo (``sandstoen``) fails at build
  time instead of shipping a wrong-coloured asset.
- :func:`_mat_with_fallback` — for primaries that have a documented
  fallback chain (lantern glass → pv_glass → glass). Warns on each
  fallback step so the materials team sees the slack getting taken up.
"""
from __future__ import annotations

import math
import sys

import bpy

from lqv.materials import MAT, assign


def _link(obj: bpy.types.Object, col: bpy.types.Collection) -> None:
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def _require_mat(key: str):
    """Look up a material that must exist. Raises ``KeyError`` on miss.

    The error message lists the keys the registry actually contains so
    a typo is caught at the next line. Use for materials where a silent
    fallback to principled-white would be visually obvious in the render.
    """
    mat = MAT.get(key)
    if mat is None:
        raise KeyError(
            f"material registry MAT has no key {key!r}; "
            f"available keys: {sorted(MAT.keys())}"
        )
    return mat


def _mat_with_fallback(*keys: str):
    """Return the first material in the registry. Warn on every fallback step.

    Use for slots that explicitly have a fallback chain (e.g. a glass
    bowl: ``lantern_paper_warm`` -> ``pv_glass`` -> ``glass``). Raises
    ``KeyError`` if every candidate misses, listing the chain tried so
    the caller can see the gap.
    """
    if not keys:
        raise ValueError("_mat_with_fallback requires at least one key")
    for i, key in enumerate(keys):
        mat = MAT.get(key)
        if mat is not None:
            if i > 0:
                print(
                    f"[lqv.amenities._grammar] WARN material {keys[0]!r} missing; "
                    f"fell back to {key!r} (chain tried: {list(keys[:i + 1])}).",
                    file=sys.stderr,
                )
            return mat
    raise KeyError(
        f"none of the materials in fallback chain {list(keys)} were registered; "
        f"available keys: {sorted(MAT.keys())}"
    )


# Back-compat shim — only used by code that genuinely wants "principled white
# is fine, no warning needed". New callsites should pick _require_mat or
# _mat_with_fallback. Kept undocumented; deprecation tracked in #13.
def _mat(key: str):
    return MAT.get(key)


def cascade_weir(
    col: bpy.types.Collection,
    center: tuple[float, float],
    width_m: float = 2.0,
    height_m: float = 0.6,
    thickness_m: float = 0.35,
    name_prefix: str = 'CascadeWeir',
):
    """Stone cascade weir — a low dam across a creek that spills water.

    A weir reads as: a low sandstone wall perpendicular to flow with a
    rounded crest; downstream a sloped apron catches the falling water.
    Implemented as a sandstone bar + a sloped apron slab.
    """
    cx, cy = center
    mat_stone = _require_mat('sandstone')

    # Weir bar (across-stream)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, height_m / 2.0))
    bar = bpy.context.active_object
    bar.name = f'{name_prefix}_Bar'
    bar.scale = (width_m, thickness_m, height_m)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(bar, mat_stone)
    _link(bar, col)

    # Downstream apron — sloped slab catching the fall
    apron_len = max(height_m * 1.8, 0.5)
    apron_z = height_m * 0.45
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy + thickness_m / 2.0 + apron_len / 2.0, apron_z))
    apron = bpy.context.active_object
    apron.name = f'{name_prefix}_Apron'
    apron.scale = (width_m, apron_len, 0.10)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    apron.rotation_euler = (math.radians(-15.0), 0.0, 0.0)
    assign(apron, mat_stone)
    _link(apron, col)


def stepping_stones(
    col: bpy.types.Collection,
    start: tuple[float, float],
    end: tuple[float, float],
    count: int = 5,
    stone_radius_m: float = 0.35,
    stone_height_m: float = 0.18,
    z_base: float = 0.05,
    jitter_m: float = 0.08,
    name_prefix: str = 'SteppingStone',
):
    """Row of flat sandstone stepping stones from ``start`` to ``end``.

    Lateral jitter is deterministic from the index so the layout is
    byte-stable across re-runs.
    """
    mat = _require_mat('sandstone')
    sx, sy = start
    ex, ey = end
    for i in range(count):
        t = (i + 0.5) / count
        x = sx + (ex - sx) * t
        y = sy + (ey - sy) * t
        # Deterministic lateral offset (alternating)
        offset_sign = 1.0 if i % 2 == 0 else -1.0
        x += offset_sign * jitter_m
        z = z_base + stone_height_m / 2.0
        bpy.ops.mesh.primitive_cylinder_add(
            radius=stone_radius_m,
            depth=stone_height_m,
            location=(x, y, z),
            vertices=16,
        )
        obj = bpy.context.active_object
        obj.name = f'{name_prefix}_{i}'
        assign(obj, mat)
        _link(obj, col)


def glass_bowl_lantern(
    col: bpy.types.Collection,
    location: tuple[float, float, float],
    bowl_radius_m: float = 0.10,
    suspension_length_m: float = 0.8,
    name_prefix: str = 'Lantern',
):
    """Single hanging glass-bowl pendant lamp.

    Geometry: a UV sphere bowl (lower half emissive read) suspended by
    a thin lapacho cord. The bowl gets ``pv_glass`` (used here as a dark
    glass stand-in; refined Phase E).
    """
    lx, ly, lz = location
    mat_glass = _mat_with_fallback('lantern_paper_warm', 'pv_glass', 'glass')
    mat_cord = _require_mat('lapacho_timber')

    # Cord
    cord_z_mid = lz + suspension_length_m / 2.0
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.005,
        depth=suspension_length_m,
        location=(lx, ly, cord_z_mid),
        vertices=6,
    )
    cord = bpy.context.active_object
    cord.name = f'{name_prefix}_Cord'
    assign(cord, mat_cord)
    _link(cord, col)

    # Bowl
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=bowl_radius_m,
        location=(lx, ly, lz),
        segments=16,
        ring_count=8,
    )
    bowl = bpy.context.active_object
    bowl.name = f'{name_prefix}_Bowl'
    assign(bowl, mat_glass)
    _link(bowl, col)


def boulder_seating(
    col: bpy.types.Collection,
    center: tuple[float, float],
    arc_radius_m: float = 2.5,
    boulder_count: int = 5,
    boulder_radius_m: float = 0.45,
    arc_span_deg: float = 180.0,
    name_prefix: str = 'Boulder',
):
    """Curved arrangement of seating boulders.

    Reads as a hangout around a central feature (firepit, water bowl,
    creek edge). Deterministic placement.
    """
    cx, cy = center
    mat = _require_mat('sandstone')
    start_deg = -arc_span_deg / 2.0
    for i in range(boulder_count):
        if boulder_count == 1:
            t = 0.5
        else:
            t = i / (boulder_count - 1)
        angle = math.radians(start_deg + t * arc_span_deg)
        x = cx + arc_radius_m * math.cos(angle)
        y = cy + arc_radius_m * math.sin(angle)
        # Slight size variation, deterministic
        r = boulder_radius_m * (0.85 + 0.30 * ((i * 37) % 7) / 7.0)
        bpy.ops.mesh.primitive_ico_sphere_add(
            radius=r,
            subdivisions=2,
            location=(x, y, r * 0.6),
        )
        obj = bpy.context.active_object
        obj.name = f'{name_prefix}_{i}'
        # Squash slightly to read as seat-height boulder
        obj.scale = (1.0, 1.0, 0.65)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        assign(obj, mat)
        _link(obj, col)
