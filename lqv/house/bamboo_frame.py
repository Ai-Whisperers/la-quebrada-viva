"""Shared bamboo-frame primitives — wigwam / container_4pax / beton series.

Per project "factor on second use, not first" policy: the wigwam typology was
first to express the bamboo-frame vocabulary; ``bamboo_container_4pax`` is the
second use, which triggers the extraction below. The future ``bamboo_beton``
family (rectangular post-and-beam pavilions on a concrete spine) will also
import from here.

Public surface
--------------

* :func:`build_bamboo_culm`         — single tapered pole between two points.
* :func:`build_bamboo_lashing`      — torus knot at a joint (rope or fibre).
* :func:`build_bamboo_post_stack`   — vertical posts spaced along a rectangle.
* :func:`build_bamboo_radial_frame` — wigwam-style radial cone + apex lashing.
* :func:`build_bamboo_beam`         — horizontal beam (semantic alias of culm).
* :func:`build_palm_thatch_panel`   — quad thatch panel from 4 corner points.

Each primitive:

* Resolves materials through the project ``MAT`` fallback chain
  (``_mat(primary, fallback, ...)``) so callers stay terse and tolerant of
  registry gaps during early typology bring-up.
* Returns ``bpy.types.Object`` (or a list / tuple thereof) — no side effects
  beyond linking to the active collection.
* Uses 10 vertices per cylinder by default which reads smooth at the close
  sub-render distances (6-15 m camera-to-asset).

Geometry conventions
--------------------

Bamboo culms (Guadua angustifolia) are tapered hollow cylinders 60-120 mm Ø
at the base. The :func:`build_bamboo_culm` API exposes a ``taper_ratio`` so
callers can express butt-vs-tip diameter difference; the implementation
applies the taper as a uniform scale on the top vertex ring, which reads as
a subtle conical shape from any of the sub-render cameras.
"""
from __future__ import annotations

import math

import bpy

from lqv.materials import MAT, assign

# ---------------------------------------------------------------------------
# Material fallback resolver — shared by every primitive in this module.
# ---------------------------------------------------------------------------

def _mat(*keys: str):
    """Return the first MAT key that resolves; ``None`` if none do."""
    for k in keys:
        m = MAT.get(k)
        if m is not None:
            return m
    return None


def _active_collection() -> bpy.types.Collection:
    """Resolve the collection a primitive should be linked to.

    Defaults to the scene root; callers wanting nested grouping should re-link
    the returned object themselves (matching the pattern already used in
    ``lqv.typologies.bamboo_wigwam_lodge`` and friends).
    """
    return bpy.context.scene.collection


def _link(obj: bpy.types.Object, col: bpy.types.Collection) -> None:
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


# ---------------------------------------------------------------------------
# Bamboo culm — single pole between two points
# ---------------------------------------------------------------------------

def build_bamboo_culm(p_start_xyz: tuple[float, float, float],
                     p_end_xyz: tuple[float, float, float],
                     diameter_m: float = 0.10,
                     taper_ratio: float = 0.9,
                     segments: int = 10,
                     material: str = 'bamboo',
                     name: str = 'BambooCulm') -> bpy.types.Object:
    """Build a single bamboo pole as a thin tapered cylinder.

    Parameters
    ----------
    p_start_xyz, p_end_xyz
        World-space endpoints (butt and tip). Length and orientation are
        derived from the vector between them.
    diameter_m
        Butt diameter in metres. 60-120 mm is typical for Guadua structural
        culms; 35-50 mm for top rails / cladding.
    taper_ratio
        Tip-to-butt diameter ratio. 1.0 = no taper (true cylinder); 0.9 reads
        as a natural Guadua taper at most render distances. The ratio is
        applied as a uniform scale on the upper vertex loop after creation.
    segments
        Cylinder vertex count. 10 reads smooth at sub-render distances; bump
        to 16 only for hero close-ups.
    material
        Primary MAT key. Falls back to ``lapacho_timber`` if the requested
        key is missing — bamboo and lapacho share a warm-organic palette so
        a missing-bamboo render still reads as a wood pole rather than a
        plastic stand-in.
    """
    sx, sy, sz = p_start_xyz
    ex, ey, ez = p_end_xyz
    dx, dy, dz = ex - sx, ey - sy, ez - sz
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length < 1e-6:
        length = 1e-6  # avoid divide-by-zero; degenerate poles still get created
    mid = (sx + dx / 2.0, sy + dy / 2.0, sz + dz / 2.0)
    # Euler aligning default-Z cylinder to (dx,dy,dz)
    horiz = math.sqrt(dx * dx + dy * dy)
    rot_x = math.atan2(-dy, math.sqrt(dx * dx + dz * dz)) if horiz > 1e-6 else 0.0
    rot_y = math.atan2(dx, dz)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=diameter_m / 2.0,
        depth=length,
        location=mid,
        rotation=(rot_x, rot_y, 0.0),
        vertices=segments,
    )
    obj = bpy.context.active_object
    obj.name = name

    # Apply taper by scaling the top vertex loop. Cylinder primitives in
    # Blender place verts with +Z = top loop; iterate raw mesh data to scale
    # those vertices radially in local XY.
    if abs(taper_ratio - 1.0) > 1e-4:
        mesh = obj.data
        top_z = max(v.co.z for v in mesh.vertices)
        for v in mesh.vertices:
            if abs(v.co.z - top_z) < 1e-4:
                v.co.x *= taper_ratio
                v.co.y *= taper_ratio
        mesh.update()

    mat = _mat(material, 'lapacho_timber')
    if mat is not None:
        assign(obj, mat)
    _link(obj, _active_collection())
    return obj


# ---------------------------------------------------------------------------
# Bamboo lashing — small torus knot at a joint (rope / fibre / wire)
# ---------------------------------------------------------------------------

def build_bamboo_lashing(xyz: tuple[float, float, float],
                        radius_m: float = 0.06,
                        thickness_m: float = 0.02,
                        material: str = 'fasteners_lashings',
                        fallback: str = 'lapacho_timber',
                        name: str = 'BambooLashing') -> bpy.types.Object:
    """Small torus representing rope / cord at a culm joint.

    The wigwam apex knot, container-veranda post-to-beam ties, and any
    decorative mid-height tension band all reuse this primitive.
    """
    bpy.ops.mesh.primitive_torus_add(
        major_radius=radius_m,
        minor_radius=thickness_m,
        location=xyz,
        major_segments=20,
        minor_segments=6,
    )
    obj = bpy.context.active_object
    obj.name = name
    mat = _mat(material, fallback, 'bamboo')
    if mat is not None:
        assign(obj, mat)
    _link(obj, _active_collection())
    return obj


# ---------------------------------------------------------------------------
# Bamboo post stack — vertical poles around a rectangular footprint
# ---------------------------------------------------------------------------

def build_bamboo_post_stack(footprint_corners: list[tuple[float, float]],
                            height_m: float,
                            base_z: float = 0.0,
                            post_diameter_m: float = 0.10,
                            spacing_m: float = 1.0,
                            material: str = 'bamboo',
                            name_prefix: str = 'VerandaPost') -> list[bpy.types.Object]:
    """Vertical posts spaced along a polyline footprint.

    Parameters
    ----------
    footprint_corners
        List of (x, y) corners in order. The polyline is treated as OPEN —
        callers wanting a closed perimeter should repeat the first corner at
        the end of the list (matches the convention used downstream for the
        wraparound veranda where only the south + east faces carry posts).
    height_m
        Post height above ``base_z``. Each post runs from ``base_z`` to
        ``base_z + height_m``.
    spacing_m
        Centre-to-centre target along each polyline segment. The actual
        spacing is rounded to fit the segment length so endpoints land
        exactly on corners (no half-post stragglers).
    """
    posts: list[bpy.types.Object] = []
    for i in range(len(footprint_corners) - 1):
        ax, ay = footprint_corners[i]
        bx, by = footprint_corners[i + 1]
        dx, dy = bx - ax, by - ay
        seg_len = math.sqrt(dx * dx + dy * dy)
        if seg_len < 1e-6:
            continue
        n_posts = max(2, int(round(seg_len / spacing_m)) + 1)
        for j in range(n_posts):
            t = j / (n_posts - 1)
            # Avoid double-placing the shared corner: on segments after the
            # first, skip the j=0 post which sits on the prior segment's tip.
            if i > 0 and j == 0:
                continue
            px = ax + dx * t
            py = ay + dy * t
            obj = build_bamboo_culm(
                p_start_xyz=(px, py, base_z),
                p_end_xyz=(px, py, base_z + height_m),
                diameter_m=post_diameter_m,
                taper_ratio=0.92,
                segments=10,
                material=material,
                name=f'{name_prefix}_{i:02d}_{j:02d}',
            )
            posts.append(obj)
    return posts


# ---------------------------------------------------------------------------
# Bamboo radial frame — wigwam cone of poles + apex lashing
# ---------------------------------------------------------------------------

def build_bamboo_radial_frame(center_xyz: tuple[float, float, float],
                              base_radius_m: float,
                              apex_height_m: float,
                              count: int = 12,
                              post_diameter_m: float = 0.08,
                              apex_cluster_r: float = 0.08,
                              overshoot_m: float = 0.20,
                              material: str = 'bamboo',
                              name_prefix: str = 'RadialPole'
                              ) -> tuple[list[bpy.types.Object], bpy.types.Object | None]:
    """Wigwam-style radial cone of poles meeting at a clustered apex.

    The apex points are distributed over a tiny cluster radius so the culms
    read as a knotted bundle rather than a perfect mathematical point. An
    apex lashing torus (small rope knot) is added just below the apex.

    Returns
    -------
    (poles, apex_lashing)
        ``poles`` is the list of culm objects (length = ``count``);
        ``apex_lashing`` is the lashing torus (may be ``None`` if MAT
        resolution failed catastrophically — caller can ignore it).
    """
    cx, cy, cz = center_xyz
    base_z = cz
    apex_z = cz + apex_height_m
    poles: list[bpy.types.Object] = []
    for i in range(count):
        theta = (i / count) * 2.0 * math.pi
        bx = cx + base_radius_m * math.cos(theta)
        by = cy + base_radius_m * math.sin(theta)
        # Apex offset rotates one half-step so culms cluster, not co-locate.
        apex_theta = theta + math.pi / count
        ax = cx + apex_cluster_r * math.cos(apex_theta)
        ay = cy + apex_cluster_r * math.sin(apex_theta)
        # Extend overshoot along the pole axis past the apex.
        dx, dy, dz = ax - bx, ay - by, apex_z - base_z
        ln = math.sqrt(dx * dx + dy * dy + dz * dz)
        if ln > 1e-6:
            ux, uy, uz = dx / ln, dy / ln, dz / ln
            ex = ax + ux * overshoot_m
            ey = ay + uy * overshoot_m
            ez = apex_z + uz * overshoot_m
        else:
            ex, ey, ez = ax, ay, apex_z + overshoot_m
        pole = build_bamboo_culm(
            p_start_xyz=(bx, by, base_z),
            p_end_xyz=(ex, ey, ez),
            diameter_m=post_diameter_m,
            taper_ratio=0.85,
            segments=10,
            material=material,
            name=f'{name_prefix}_{i:02d}',
        )
        poles.append(pole)

    apex_lashing = build_bamboo_lashing(
        xyz=(cx, cy, apex_z - 0.05),
        radius_m=apex_cluster_r + 0.06,
        thickness_m=0.02,
        material='rope_natural',
        fallback='lapacho_timber',
        name=f'{name_prefix}_ApexLashing',
    )
    return poles, apex_lashing


# ---------------------------------------------------------------------------
# Bamboo beam — horizontal beam (same as culm, signals intent)
# ---------------------------------------------------------------------------

def build_bamboo_beam(p_start_xyz: tuple[float, float, float],
                      p_end_xyz: tuple[float, float, float],
                      diameter_m: float = 0.12,
                      material: str = 'bamboo',
                      name: str = 'BambooBeam') -> bpy.types.Object:
    """Horizontal beam (semantic alias of culm with thicker default Ø).

    Kept as a distinct entry point so call-sites read as
    ``build_bamboo_beam(...)`` for headers / purlins / collar-ties and
    ``build_bamboo_culm(...)`` for vertical posts / radial rafters.
    """
    return build_bamboo_culm(
        p_start_xyz=p_start_xyz,
        p_end_xyz=p_end_xyz,
        diameter_m=diameter_m,
        taper_ratio=1.0,
        segments=10,
        material=material,
        name=name,
    )


# ---------------------------------------------------------------------------
# Palm-thatch panel — flat or curved quad mesh
# ---------------------------------------------------------------------------

def build_palm_thatch_panel(corners_xyz: list[tuple[float, float, float]],
                            material: str = 'palm_thatch',
                            name: str = 'ThatchPanel',
                            subdivisions: int = 4) -> bpy.types.Object:
    """Flat quad thatch panel from 4 corner points (in order: SW, SE, NE, NW).

    A simple subdivided bilinear patch — sufficient for the wraparound
    veranda roof on container_4pax, the wigwam cone shells, and any future
    pavilion-roof use. The thatch material carries its own displacement so a
    low subdivision count is enough.
    """
    if len(corners_xyz) != 4:
        raise ValueError('build_palm_thatch_panel requires exactly 4 corner points')

    sw, se, ne, nw = corners_xyz
    verts: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []
    cols = subdivisions + 1
    for j in range(cols):
        v = j / subdivisions
        # bilinear interp along the south (sw->se) and north (nw->ne) edges
        for i in range(cols):
            u = i / subdivisions
            # bilinear: P(u,v) = (1-v)*((1-u)*sw + u*se) + v*((1-u)*nw + u*ne)
            x = (1 - v) * ((1 - u) * sw[0] + u * se[0]) + v * ((1 - u) * nw[0] + u * ne[0])
            y = (1 - v) * ((1 - u) * sw[1] + u * se[1]) + v * ((1 - u) * nw[1] + u * ne[1])
            z = (1 - v) * ((1 - u) * sw[2] + u * se[2]) + v * ((1 - u) * nw[2] + u * ne[2])
            verts.append((x, y, z))
    for j in range(subdivisions):
        for i in range(subdivisions):
            a = j * cols + i
            b = a + 1
            c = (j + 1) * cols + i + 1
            d = (j + 1) * cols + i
            faces.append((a, b, c, d))
    mesh = bpy.data.meshes.new(f'{name}_Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    mat = _mat(material, 'sod_canopy', 'lapacho_timber')
    if mat is not None:
        assign(obj, mat)
    _active_collection().objects.link(obj)
    return obj


__all__ = [
    'build_bamboo_culm',
    'build_bamboo_lashing',
    'build_bamboo_post_stack',
    'build_bamboo_radial_frame',
    'build_bamboo_beam',
    'build_palm_thatch_panel',
]
