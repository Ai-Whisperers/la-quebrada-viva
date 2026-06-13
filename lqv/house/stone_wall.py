"""Shared stone-cottage primitives — the design vocabulary used by both
``italian_stone_small_v1`` (5×4 m, 1BR) and ``italian_stone_small_v2``
(side-loggia 2BR, ~70 m²).

Factored on the second use, per project plan. Every primitive returns the
``bpy.types.Object(s)`` it creates so callers can re-collection / re-tag /
re-parent without follow-up bpy.ops gymnastics. Each primitive uses MAT
fallback chains identical to v1's first-use inlining (sandstone for stone
foundation, clay_tile for terracotta, lapacho_timber for joinery) — so a
caller passing the canonical key strings will get the same material
selection v1 used before the refactor, even though several of the
"canonical" keys (``terracotta_tile_roof``, ``stone_foundation``,
``lapacho_shutters_doors``, ``lapacho_beams_porch``) do not exist in the
current MAT registry. The fallback chains land all of them on extant
keys.

No side effects beyond mesh creation + material assign + collection link
when ``collection`` is provided. Callers are free to pre-create a
collection and pass it in; if not, the primitive links to the active
scene collection via Blender defaults.
"""
from __future__ import annotations

import math
from typing import Sequence

import bpy

from lqv.materials import MAT, assign


# ---------------------------------------------------------------------------
# Material fallback chains — single source of truth for stone-cottage
# typology palette. Order: ideal key → next-best → guaranteed-extant.
# ---------------------------------------------------------------------------
_FALLBACKS: dict[str, tuple[str, ...]] = {
    'sandstone':                ('sandstone', 'stone_wall', 'limestone'),
    'stone_foundation':         ('stone_foundation', 'sandstone', 'stone_wall', 'limestone'),
    'terracotta_tile_roof':     ('terracotta_tile_roof', 'terracotta_tile', 'clay_tile', 'laterite'),
    'lapacho_shutters_doors':   ('lapacho_shutters_doors', 'lapacho_timber'),
    'lapacho_beams_porch':      ('lapacho_beams_porch', 'lapacho_shutters_doors', 'lapacho_timber'),
    'flagstone':                ('flagstone', 'slate', 'sandstone', 'stone_wall', 'laterite'),
    'glass_glazing':            ('glass_glazing', 'water_reflective', 'glass_bottle_cobalt'),
}


def _resolve(*keys: str):
    """Walk the per-key fallback chains in order, returning the first MAT hit.

    Bare keys not in ``_FALLBACKS`` are tried as-is. Returns ``None`` if no
    chain resolves — callers may still pass ``None`` to the cube/mesh
    helpers, which silently leave the object unassigned.
    """
    for k in keys:
        chain = _FALLBACKS.get(k, (k,))
        for cand in chain:
            m = MAT.get(cand)
            if m is not None:
                return m
    return None


# ---------------------------------------------------------------------------
# Mesh helpers — internal, mirror v1's _cube/_cylinder so geometry is
# byte-identical when callers feed the same params.
# ---------------------------------------------------------------------------
def _cube(name: str, location, scale, mat, collection: bpy.types.Collection | None = None):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        assign(obj, mat)
    if collection is not None:
        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        collection.objects.link(obj)
    return obj


def _cylinder(name: str, location, radius, depth, mat, rotation=(0.0, 0.0, 0.0),
              collection: bpy.types.Collection | None = None):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, rotation=rotation,
    )
    obj = bpy.context.active_object
    obj.name = name
    if mat is not None:
        assign(obj, mat)
    if collection is not None:
        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        collection.objects.link(obj)
    return obj


def _meshobj(name: str, verts, faces, mat,
             collection: bpy.types.Collection | None = None):
    mesh = bpy.data.meshes.new(f'{name}_Mesh')
    mesh.from_pydata(list(verts), [], list(faces))
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    if mat is not None:
        assign(obj, mat)
    if collection is not None:
        collection.objects.link(obj)
    else:
        bpy.context.scene.collection.objects.link(obj)
    return obj


# ---------------------------------------------------------------------------
# Public primitives — the shared stone-cottage vocabulary.
# ---------------------------------------------------------------------------
def build_stone_foundation_course(
    x: float, y: float,
    width_m: float, depth_m: float,
    height_m: float = 0.6,
    material: str = 'stone_foundation',
    fallback: str = 'sandstone',
    name: str = 'StoneFoundation',
    collection: bpy.types.Collection | None = None,
) -> bpy.types.Object:
    """60 cm sandstone plinth (Rule 4 — earthen surfaces never touch grade).

    Sized slightly proud of the wall footprint so it reads as a course
    rather than as the wall continuing into the ground; v1 used a 20 cm
    overhang on each side and we replicate that.
    """
    mat = _resolve(material, fallback)
    return _cube(
        name=name,
        location=(x, y, height_m / 2.0),
        scale=(width_m + 0.20, depth_m + 0.20, height_m),
        mat=mat,
        collection=collection,
    )


def build_sandstone_wall(
    p_start: Sequence[float], p_end: Sequence[float],
    height_m: float, thickness_m: float = 0.4,
    material: str = 'sandstone',
    name: str = 'StoneWall',
    collection: bpy.types.Collection | None = None,
    z_base: float = 0.0,
) -> bpy.types.Object:
    """Straight sandstone wall segment between two XY points.

    Rectilinear per masonry trade convention (the cob "no right angles"
    rule applies only to the cob house, not the Italian stone vocabulary).
    The wall is axis-aligned for segments that run along x or y; for
    arbitrary headings we rotate the box around z. Height is measured from
    ``z_base`` (caller-defined plinth top), so the wall sits on whatever
    foundation course you have built.
    """
    mat = _resolve(material)
    x0, y0 = p_start[0], p_start[1]
    x1, y1 = p_end[0], p_end[1]
    dx = x1 - x0
    dy = y1 - y0
    length = math.hypot(dx, dy)
    cx = (x0 + x1) / 2.0
    cy = (y0 + y1) / 2.0
    cz = z_base + height_m / 2.0
    angle = math.atan2(dy, dx)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (length, thickness_m, height_m)
    obj.rotation_euler = (0.0, 0.0, angle)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if mat is not None:
        assign(obj, mat)
    if collection is not None:
        for c in list(obj.users_collection):
            c.objects.unlink(obj)
        collection.objects.link(obj)
    return obj


def build_terracotta_gable_roof(
    footprint_corners: Sequence[Sequence[float]],
    ridge_axis: str = 'x',
    pitch_rad: float = 0.35,
    overhang_m: float = 0.9,
    gable_overhang_m: float = 0.2,
    eave_z: float = 2.6,
    material: str = 'terracotta_tile_roof',
    name: str = 'TerracottaRoof',
    collection: bpy.types.Collection | None = None,
) -> bpy.types.Object:
    """Low-pitch gable roof sized to a rectangular footprint.

    ``footprint_corners`` is ((x_min, y_min), (x_max, y_max)). ``ridge_axis``
    is ``'x'`` (ridge runs E-W → gables on N/S) or ``'y'`` (ridge runs N-S →
    gables on E/W). ``overhang_m`` is the long-side eave overhang (Rule 5,
    typ. 90 cm); ``gable_overhang_m`` is the shorter overhang on the gable
    ends.
    """
    (x_min, y_min), (x_max, y_max) = footprint_corners
    cx = (x_min + x_max) / 2.0
    cy = (y_min + y_max) / 2.0

    if ridge_axis == 'x':
        # Ridge along x → roof slopes in y. Eaves on N/S long sides extend
        # by overhang_m; gable ends (E/W) extend by gable_overhang_m.
        half_w = (x_max - x_min) / 2.0 + gable_overhang_m
        half_l = (y_max - y_min) / 2.0 + overhang_m
        ridge_y_half = (y_max - y_min) / 2.0
        ridge_z = eave_z + math.tan(pitch_rad) * ridge_y_half
        verts = [
            (cx - half_w, cy - half_l, eave_z),
            (cx + half_w, cy - half_l, eave_z),
            (cx + half_w, cy + half_l, eave_z),
            (cx - half_w, cy + half_l, eave_z),
            (cx - half_w, cy,           ridge_z),
            (cx + half_w, cy,           ridge_z),
        ]
        faces = [(0, 1, 5, 4), (3, 4, 5, 2), (0, 4, 3), (1, 2, 5)]
    else:
        # Ridge along y.
        half_w = (x_max - x_min) / 2.0 + overhang_m
        half_l = (y_max - y_min) / 2.0 + gable_overhang_m
        ridge_x_half = (x_max - x_min) / 2.0
        ridge_z = eave_z + math.tan(pitch_rad) * ridge_x_half
        verts = [
            (cx - half_w, cy - half_l, eave_z),
            (cx + half_w, cy - half_l, eave_z),
            (cx + half_w, cy + half_l, eave_z),
            (cx - half_w, cy + half_l, eave_z),
            (cx,           cy - half_l, ridge_z),
            (cx,           cy + half_l, ridge_z),
        ]
        faces = [(0, 1, 5, 4), (3, 2, 5, 4), (0, 4, 3), (1, 2, 5)]

    mat = _resolve(material)
    return _meshobj(name, verts, faces, mat, collection)


def build_lapacho_shutter_pair(
    window_xy_z: Sequence[float],
    opening_w: float, opening_h: float,
    face_normal: Sequence[float] = (0.0, -1.0, 0.0),
    material: str = 'lapacho_shutters_doors',
    shutter_w: float | None = None,
    shutter_h: float | None = None,
    name_prefix: str = 'Shutter',
    collection: bpy.types.Collection | None = None,
) -> list[bpy.types.Object]:
    """Two flat lapacho planks bracketing each window opening.

    Self-roast acknowledged from v1: real Italian shutters are SLATTED, not
    flat planks. Modeling each slat per-window would balloon the polycount
    without changing the hero-camera silhouette, so we leave them flat —
    same trade-off as v1. ``face_normal`` is the outward direction of the
    wall face; the shutters sit just outside (4 cm offset) the wall plane.
    Currently only axial normals (±x, ±y) are supported; arbitrary normals
    would require a quaternion alignment of the cube scales.
    """
    mat = _resolve(material)
    sw = shutter_w if shutter_w is not None else max(0.45, opening_w * 0.55)
    sh = shutter_h if shutter_h is not None else max(0.95, opening_h * 1.05)
    cx, cy, cz = window_xy_z
    nx, ny, _nz = face_normal

    objs: list[bpy.types.Object] = []
    if abs(ny) > abs(nx):
        # Wall is N/S; shutters bracket left/right along x.
        offset_y = cy + ny * 0.04
        for leaf_i, sign in enumerate((-1, 1)):
            ox = cx + sign * (opening_w / 2.0 + sw / 2.0 + 0.02)
            objs.append(_cube(
                name=f'{name_prefix}_{leaf_i}',
                location=(ox, offset_y, cz),
                scale=(sw, 0.04, sh),
                mat=mat,
                collection=collection,
            ))
    else:
        # Wall is E/W; shutters bracket front/back along y.
        offset_x = cx + nx * 0.04
        for leaf_i, sign in enumerate((-1, 1)):
            oy = cy + sign * (opening_w / 2.0 + sw / 2.0 + 0.02)
            objs.append(_cube(
                name=f'{name_prefix}_{leaf_i}',
                location=(offset_x, oy, cz),
                scale=(0.04, sw, sh),
                mat=mat,
                collection=collection,
            ))
    return objs


def build_lapacho_door(
    xy_z: Sequence[float],
    width_m: float = 0.9,
    height_m: float = 2.1,
    face_normal: Sequence[float] = (0.0, -1.0, 0.0),
    material: str = 'lapacho_shutters_doors',
    name: str = 'Door',
    collection: bpy.types.Collection | None = None,
    with_trim: bool = True,
) -> bpy.types.Object | list[bpy.types.Object]:
    """Front-door slab with optional lapacho lintel + jamb trim.

    ``xy_z`` is the centre of the door slab. ``face_normal`` is the outward
    wall direction; door sits 3 cm proud of the wall.
    """
    mat = _resolve(material)
    cx, cy, cz = xy_z
    nx, ny, _nz = face_normal
    slab_thick = 0.06

    if abs(ny) > abs(nx):
        slab = _cube(
            name=name,
            location=(cx, cy + ny * 0.03, cz),
            scale=(width_m, slab_thick, height_m),
            mat=mat,
            collection=collection,
        )
    else:
        slab = _cube(
            name=name,
            location=(cx + nx * 0.03, cy, cz),
            scale=(slab_thick, width_m, height_m),
            mat=mat,
            collection=collection,
        )

    if not with_trim:
        return slab

    objs: list[bpy.types.Object] = [slab]
    top_z = cz + height_m / 2.0 + 0.08
    if abs(ny) > abs(nx):
        objs.append(_cube(
            name=f'{name}Lintel',
            location=(cx, cy + ny * 0.04, top_z),
            scale=(width_m + 0.30, 0.10, 0.12),
            mat=mat,
            collection=collection,
        ))
        for sign, suf in ((-1, 'L'), (1, 'R')):
            objs.append(_cube(
                name=f'{name}Jamb_{suf}',
                location=(cx + sign * (width_m / 2.0 + 0.06),
                          cy + ny * 0.04, cz),
                scale=(0.10, 0.10, height_m + 0.10),
                mat=mat,
                collection=collection,
            ))
    else:
        objs.append(_cube(
            name=f'{name}Lintel',
            location=(cx + nx * 0.04, cy, top_z),
            scale=(0.10, width_m + 0.30, 0.12),
            mat=mat,
            collection=collection,
        ))
        for sign, suf in ((-1, 'L'), (1, 'R')):
            objs.append(_cube(
                name=f'{name}Jamb_{suf}',
                location=(cx + nx * 0.04,
                          cy + sign * (width_m / 2.0 + 0.06), cz),
                scale=(0.10, 0.10, height_m + 0.10),
                mat=mat,
                collection=collection,
            ))
    return objs


def build_lapacho_porch_beams(
    p_start_xyz: Sequence[float],
    p_end_xyz: Sequence[float],
    count: int = 2,
    beam_w: float = 0.18,
    beam_h: float = 0.22,
    material: str = 'lapacho_beams_porch',
    name_prefix: str = 'PorchBeam',
    collection: bpy.types.Collection | None = None,
) -> list[bpy.types.Object]:
    """A row of ``count`` parallel lapacho beams between two XYZ anchors.

    The beams span along the x-axis of the rectangle defined by the two
    anchors; their starts/ends are evenly distributed along y. Used for
    porch / loggia roof framing (lapacho heartwood — the most expensive
    structural material in the Paraguayan vernacular).
    """
    mat = _resolve(material)
    x0, y0, z0 = p_start_xyz
    x1, y1, z1 = p_end_xyz
    span_x = abs(x1 - x0)
    cx = (x0 + x1) / 2.0
    objs: list[bpy.types.Object] = []
    if count <= 1:
        ys = [(y0 + y1) / 2.0]
    else:
        ys = [y0 + (y1 - y0) * i / (count - 1) for i in range(count)]
    cz = (z0 + z1) / 2.0
    for i, by in enumerate(ys):
        objs.append(_cube(
            name=f'{name_prefix}_{i}',
            location=(cx, by, cz),
            scale=(span_x + beam_w, beam_w, beam_h),
            mat=mat,
            collection=collection,
        ))
    return objs


def build_chimney(
    top_xyz: Sequence[float],
    width_m: float = 0.5,
    height_m: float = 1.4,
    material: str = 'sandstone',
    name: str = 'Chimney',
    collection: bpy.types.Collection | None = None,
    with_cap: bool = True,
) -> list[bpy.types.Object]:
    """Gable-end sandstone chimney + cap, anchored at the top centre.

    ``top_xyz`` is where the cap sits — pass the ridge-line z plus
    desired protrusion. The shaft drops from there down to top z minus
    ``height_m``; callers manage interaction with the roof penetration
    (we don't boolean-diff into the roof — visual stack with the cap
    reading above the ridge is enough at the hero distance).
    """
    mat = _resolve(material)
    cx, cy, top_z = top_xyz
    base_z = top_z - height_m
    objs: list[bpy.types.Object] = []
    objs.append(_cube(
        name=name,
        location=(cx, cy, base_z + height_m / 2.0),
        scale=(width_m, width_m, height_m),
        mat=mat,
        collection=collection,
    ))
    if with_cap:
        objs.append(_cube(
            name=f'{name}Cap',
            location=(cx, cy, top_z + 0.05),
            scale=(width_m + 0.18, width_m + 0.18, 0.10),
            mat=mat,
            collection=collection,
        ))
    return objs


# ---------------------------------------------------------------------------
# Small helper exposed for v1's refactor — gable-end triangle infill.
# ---------------------------------------------------------------------------
def build_gable_triangle(
    x: float, y_min: float, y_max: float,
    eave_z: float, ridge_z: float,
    material: str = 'sandstone',
    name: str = 'Gable',
    collection: bpy.types.Collection | None = None,
) -> bpy.types.Object:
    """Triangular sandstone gable infill at a fixed x, between eave and ridge."""
    verts = [
        (x, y_min, eave_z),
        (x, y_max, eave_z),
        (x, (y_min + y_max) / 2.0, ridge_z),
    ]
    faces = [(0, 1, 2)]
    mat = _resolve(material)
    return _meshobj(name, verts, faces, mat, collection)


__all__ = [
    'build_stone_foundation_course',
    'build_sandstone_wall',
    'build_terracotta_gable_roof',
    'build_lapacho_shutter_pair',
    'build_lapacho_door',
    'build_lapacho_porch_beams',
    'build_chimney',
    'build_gable_triangle',
]
