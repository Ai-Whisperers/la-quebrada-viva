#!/usr/bin/env python3
"""mushroom_cob_house.py — procedural thermally-regulated mushroom cob house.

Blender 4.x. Run headless:
    blender --background --python scripts/mushroom_cob_house.py
Or paste into the Text Editor (Scripting workspace) and press Alt-P.

Architectural concept: bioconstruccion post-and-beam timber cage carrying a
hollow cob wall envelope, capped by a cantilevered mushroom platform, with
an inclined upper dome containing horizontal glass-bottle-brick inlays. A
copper thermal chimney vents the dome through a thatched parasol cap.

All geometry is bmesh-authored — no operator-driven mesh ops — so this
script is safe to run from any Blender 4.x context (background, headless,
or Text Editor in any workspace) without view-layer or active-object
polling bugs.
"""
from __future__ import annotations

import math
import os
import random
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

# --------------------------------------------------------------------------- #
# Dimensions — single source of truth, METRIC meters.
# --------------------------------------------------------------------------- #

# Stem (lower cob): slimmer + taller → silhouette reads as mushroom, not bunker.
# Stem-to-cap ratio target ≈ 1.0 (real mushroom), so stem height ≈ cap height.
INTERNAL_RADIUS         = 2.30
LOWER_WALL_THICKNESS    = 0.50
LOWER_WALL_HEIGHT       = 5.50
LOWER_EXTERNAL_RADIUS   = INTERNAL_RADIUS + LOWER_WALL_THICKNESS   # 2.80

COLUMN_RADIUS           = 0.13
COLUMN_COUNT            = 8

RING_BEAM_Z             = LOWER_WALL_HEIGHT
RING_BEAM_THICKNESS     = 0.18
RING_BEAM_HEIGHT        = 0.22

# Cap underside (alero overhang) — substantially wider than the stem.
CANTILEVER_COUNT        = 20
CANTILEVER_EXTERNAL_R   = 5.10
CANTILEVER_HALF_WIDTH   = 0.07
CANTILEVER_HALF_HEIGHT  = 0.10
SUBFLOOR_THICKNESS      = 0.06
SLIP_PLANE_THICKNESS    = 0.05

# Mushroom cap dome — parabolic Bezier profile (bulges then tapers to peak).
# Bulge radius pushed well past base to give the classic mushroom flange;
# peak Z raised so the cap is as tall as the stem — proper silhouette ratio.
UPPER_WALL_BASE_Z       = RING_BEAM_Z + RING_BEAM_HEIGHT + 0.12     # 5.90
UPPER_WALL_PEAK_Z       = 11.40
UPPER_WALL_THICKNESS    = 0.40                                       # informational only

# 3-point Bezier control: P0=base, P1=bulge midway out, P2=peak.
CAP_OUTER_BASE_R        = CANTILEVER_EXTERNAL_R                      # 5.10 flush w/ alero
CAP_OUTER_BULGE_R       = 7.40                                       # pronounced mushroom flange
CAP_OUTER_BULGE_Z       = UPPER_WALL_BASE_Z + 1.40                   # 7.30
CAP_OUTER_PEAK_R        = 0.55                                       # sharper taper to apex
CAP_INNER_BASE_R        = INTERNAL_RADIUS                            # 2.30
CAP_INNER_BULGE_R       = 2.90
CAP_INNER_BULGE_Z       = UPPER_WALL_BASE_Z + 1.80                   # 7.70
CAP_INNER_PEAK_R        = 0.35
# Legacy names kept for callers that still reference them.
UPPER_BASE_OUTER        = CAP_OUTER_BASE_R
PEAK_OPENING_RADIUS     = CAP_INNER_PEAK_R
PEAK_OUTER_RADIUS       = CAP_OUTER_PEAK_R

# Bottle-brick rings live at 20 / 40 / 55% up the cap (avoid the peak taper).
BOTTLE_RING_T_LEVELS    = (0.18, 0.38, 0.55)
BOTTLES_PER_RING        = 14
BOTTLE_RADIUS           = 0.065
BOTTLE_JUTE_OFFSET      = 0.006

WINDOW_COUNT            = 5
WINDOW_WIDTH            = 0.78
WINDOW_RECT_HEIGHT      = 1.20
WINDOW_SILL_Z           = 1.30
WINDOW_BEVEL_WIDTH      = 0.09
WINDOW_GLASS_THICKNESS  = 0.04

DOOR_WIDTH              = 1.05
DOOR_RECT_HEIGHT        = 1.85
DOOR_SILL_Z             = 0.02
DOOR_AZIMUTH            = -math.pi / 2.0    # door faces -Y (camera side)

VENT_PIPE_RADIUS        = 0.20
VENT_PIPE_TOP_Z         = 12.70
PARASOL_HOVER_GAP       = 0.40
PARASOL_RADIUS          = 1.55
PARASOL_HEIGHT          = 0.48

STAIR_STEPS             = 18
STAIR_OUTER_R           = 1.30
STAIR_INNER_R           = 0.35
STAIR_THICKNESS         = 0.06

HEARTH_RADIUS           = 0.55
HEARTH_HEIGHT           = 0.40
LOFT_INNER_R            = 0.45
LOFT_OUTER_R            = INTERNAL_RADIUS - 0.05
FLOOR_THICKNESS         = 0.05

# Site / terrain
# Ground expanded so tree ring + extra glade beyond stay on terrain (was 25 m
# → black perimeter in aerial). Tree ring pushed outward to clear sightline
# to walls/windows; count reduced so foreground doesn't read as a hedge.
GROUND_RADIUS           = 38.0
GROUND_THICKNESS        = 0.30
PATH_INNER_R            = LOWER_EXTERNAL_RADIUS + 0.40
PATH_OUTER_R            = PATH_INNER_R + 1.00
TREE_RING_INNER         = 19.5
TREE_RING_OUTER         = 32.0
TREE_COUNT              = 16
ROCK_COUNT              = 20

# Sun position — Paraguay (~25.6°S), late-afternoon golden hour.
SUN_ELEVATION_DEG       = 32.0
SUN_AZIMUTH_DEG         = -55.0

# --------------------------------------------------------------------------- #
# Scene + units
# --------------------------------------------------------------------------- #


def clear_scene() -> None:
    """Datablock-level wipe. No operators → no context dependencies."""
    for collection in (
        bpy.data.objects, bpy.data.meshes, bpy.data.materials,
        bpy.data.lights, bpy.data.cameras, bpy.data.curves,
        bpy.data.textures, bpy.data.images, bpy.data.node_groups,
    ):
        for item in list(collection):
            collection.remove(item, do_unlink=True)
    for col in list(bpy.data.collections):
        bpy.data.collections.remove(col)


def setup_units() -> None:
    s = bpy.context.scene
    s.unit_settings.system = 'METRIC'
    s.unit_settings.length_unit = 'METERS'
    s.unit_settings.scale_length = 1.0


def get_or_make_collection(name: str) -> bpy.types.Collection:
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def link_to(obj: bpy.types.Object, col: bpy.types.Collection) -> None:
    """Move obj from any existing collections into target exclusively."""
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


# --------------------------------------------------------------------------- #
# Mesh primitives (bmesh-only, no bpy.ops)
# --------------------------------------------------------------------------- #


def _new_mesh_obj(name: str, bm: bmesh.types.BMesh,
                  location=(0.0, 0.0, 0.0)) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    bpy.context.scene.collection.objects.link(obj)
    return obj


def make_cylinder(name, radius, depth, location=(0, 0, 0), segments=32):
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False,
        segments=segments, radius1=radius, radius2=radius, depth=depth,
    )
    return _new_mesh_obj(name, bm, location)


def make_cone(name, r_bottom, r_top, depth, location=(0, 0, 0), segments=24):
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False,
        segments=segments, radius1=r_bottom, radius2=r_top, depth=depth,
    )
    return _new_mesh_obj(name, bm, location)


def make_box(name, size, location=(0, 0, 0)):
    sx, sy, sz = size
    bm = bmesh.new()
    verts = bmesh.ops.create_cube(bm, size=1.0)['verts']
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=verts)
    return _new_mesh_obj(name, bm, location)


def make_annular_ring(name, inner_r, outer_r, thickness, z=0.0, segments=64):
    """Hollow disk with closed top, bottom, inner, outer faces."""
    bm = bmesh.new()
    rings: dict[tuple[str, str], list] = {}
    for r_key, r in (("inner", inner_r), ("outer", outer_r)):
        for z_key, dz in (("bot", 0.0), ("top", thickness)):
            ring = []
            for i in range(segments):
                a = 2 * math.pi * i / segments
                ring.append(bm.verts.new(
                    (r * math.cos(a), r * math.sin(a), z + dz)
                ))
            rings[(r_key, z_key)] = ring
    for i in range(segments):
        j = (i + 1) % segments
        bm.faces.new([rings[("outer", "bot")][i], rings[("outer", "bot")][j],
                      rings[("outer", "top")][j], rings[("outer", "top")][i]])
        bm.faces.new([rings[("inner", "bot")][j], rings[("inner", "bot")][i],
                      rings[("inner", "top")][i], rings[("inner", "top")][j]])
        bm.faces.new([rings[("inner", "top")][i], rings[("inner", "top")][j],
                      rings[("outer", "top")][j], rings[("outer", "top")][i]])
        bm.faces.new([rings[("outer", "bot")][i], rings[("outer", "bot")][j],
                      rings[("inner", "bot")][j], rings[("inner", "bot")][i]])
    return _new_mesh_obj(name, bm)


# --------------------------------------------------------------------------- #
# Structural columns + ring beam
# --------------------------------------------------------------------------- #


def build_columns(col: bpy.types.Collection) -> list[bpy.types.Object]:
    cols = []
    for i in range(COLUMN_COUNT):
        a = 2 * math.pi * i / COLUMN_COUNT
        x, y = INTERNAL_RADIUS * math.cos(a), INTERNAL_RADIUS * math.sin(a)
        c = make_cylinder(
            f"Column_{i:02d}", COLUMN_RADIUS, LOWER_WALL_HEIGHT,
            location=(x, y, LOWER_WALL_HEIGHT / 2.0),
        )
        link_to(c, col)
        cols.append(c)
    return cols


def build_ring_beam(col: bpy.types.Collection) -> list[bpy.types.Object]:
    """Octagonal ring beam linking the 8 column tops."""
    segs = []
    for i in range(COLUMN_COUNT):
        a0 = 2 * math.pi * i / COLUMN_COUNT
        a1 = 2 * math.pi * ((i + 1) % COLUMN_COUNT) / COLUMN_COUNT
        p0 = Vector((INTERNAL_RADIUS * math.cos(a0),
                     INTERNAL_RADIUS * math.sin(a0), 0))
        p1 = Vector((INTERNAL_RADIUS * math.cos(a1),
                     INTERNAL_RADIUS * math.sin(a1), 0))
        mid = (p0 + p1) * 0.5
        length = (p1 - p0).length + 0.05  # slight overlap at the corners
        angle = math.atan2(p1.y - p0.y, p1.x - p0.x)
        seg = make_box(
            f"RingBeam_{i:02d}",
            size=(length, RING_BEAM_THICKNESS, RING_BEAM_HEIGHT),
            location=(mid.x, mid.y, RING_BEAM_Z + RING_BEAM_HEIGHT / 2.0),
        )
        seg.rotation_euler = (0.0, 0.0, angle)
        link_to(seg, col)
        segs.append(seg)
    return segs


# --------------------------------------------------------------------------- #
# Lower cob wall + arched window cuts + organic noise displace
# --------------------------------------------------------------------------- #


def build_lower_cob_wall(col: bpy.types.Collection) -> bpy.types.Object:
    wall = make_annular_ring(
        "LowerCobWall",
        inner_r=INTERNAL_RADIUS,
        outer_r=LOWER_EXTERNAL_RADIUS,
        thickness=LOWER_WALL_HEIGHT,
        z=0.0,
        segments=96,
    )
    link_to(wall, col)

    # Pre-subdivide so the displace modifier has verts to push around.
    sub = wall.modifiers.new("SubsurfDisplace", type='SUBSURF')
    sub.subdivision_type = 'SIMPLE'
    sub.levels = 3
    sub.render_levels = 3

    tex = bpy.data.textures.new("CobNoiseLower", type='CLOUDS')
    tex.noise_scale = 0.45
    tex.noise_depth = 3
    tex.contrast = 1.4

    disp = wall.modifiers.new("CobDisplace", type='DISPLACE')
    disp.texture = tex
    disp.strength = 0.04
    disp.mid_level = 0.5
    return wall


def _make_arched_cutter(name, width, rect_h, depth, sill_z,
                        radial_x, radial_y, rot_z) -> bpy.types.Object:
    """Cutter mesh = box + half-cylinder cap, oriented radially through wall.

    Local X axis = radial (depth direction through wall).
    Local Y axis = tangential (window width).
    """
    bm = bmesh.new()

    # Rectangular base
    rect_verts = bmesh.ops.create_cube(bm, size=1.0)['verts']
    bmesh.ops.scale(bm, vec=(depth, width, rect_h), verts=rect_verts)
    bmesh.ops.translate(bm, vec=(0.0, 0.0, rect_h / 2.0), verts=rect_verts)

    # Arch cap = horizontal cylinder along Y axis, sitting on top of rect
    cap = bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=24,
        radius1=width / 2.0, radius2=width / 2.0, depth=depth,
    )
    cap_verts = cap['verts']
    bmesh.ops.transform(
        bm, matrix=Matrix.Rotation(math.pi / 2.0, 4, 'X'), verts=cap_verts,
    )
    bmesh.ops.translate(bm, vec=(0.0, 0.0, rect_h), verts=cap_verts)

    cutter = _new_mesh_obj(name, bm, location=(radial_x, radial_y, sill_z))
    cutter.rotation_euler = (0.0, 0.0, rot_z)
    cutter.display_type = 'WIRE'
    cutter.hide_render = True
    return cutter


def cut_windows_in(wall: bpy.types.Object,
                   window_col: bpy.types.Collection,
                   glass_col: bpy.types.Collection,
                   frame_col: bpy.types.Collection) -> tuple[list, list]:
    """Boolean-cut WINDOW_COUNT arched openings, mint glass panes + sills.

    Returns ``(glass_panes, frames)`` so main() can collect them and assign
    glass-pane + wood materials in assign_all.
    """
    mid_r = (INTERNAL_RADIUS + LOWER_EXTERNAL_RADIUS) / 2.0
    depth_through = LOWER_WALL_THICKNESS + 0.40  # punch fully through
    glass_panes: list = []
    frames: list = []
    for i in range(WINDOW_COUNT):
        # Offset by pi/WINDOW_COUNT so windows don't align with columns.
        # Also skip the door azimuth band: re-shuffle so no window overlaps
        # the door wedge at DOOR_AZIMUTH.
        a = 2 * math.pi * i / WINDOW_COUNT + math.pi / WINDOW_COUNT
        cutter = _make_arched_cutter(
            f"WindowCutter_{i:02d}",
            width=WINDOW_WIDTH,
            rect_h=WINDOW_RECT_HEIGHT,
            depth=depth_through,
            sill_z=WINDOW_SILL_Z,
            radial_x=mid_r * math.cos(a),
            radial_y=mid_r * math.sin(a),
            rot_z=a,
        )
        link_to(cutter, window_col)
        mod = wall.modifiers.new(f"WinCut_{i:02d}", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = cutter
        mod.solver = 'EXACT'

        # Glass pane — thin slab in middle of the aperture, tangential width
        # slightly narrower than the cut so a wood frame band remains.
        pane_h = WINDOW_RECT_HEIGHT + WINDOW_WIDTH * 0.5  # rect + arch lobe
        pane = make_box(
            f"WindowGlass_{i:02d}",
            size=(WINDOW_GLASS_THICKNESS,
                  WINDOW_WIDTH - 0.08,
                  pane_h - 0.10),
            location=(mid_r * math.cos(a), mid_r * math.sin(a),
                      WINDOW_SILL_Z + pane_h / 2.0),
        )
        pane.rotation_euler = (0.0, 0.0, a)
        link_to(pane, glass_col)
        glass_panes.append(pane)

        # Wooden sill (small horizontal beam at sill_z, sits inside the cut)
        sill = make_box(
            f"WindowSill_{i:02d}",
            size=(LOWER_WALL_THICKNESS + 0.10,
                  WINDOW_WIDTH + 0.06,
                  0.06),
            location=(mid_r * math.cos(a), mid_r * math.sin(a),
                      WINDOW_SILL_Z - 0.01),
        )
        sill.rotation_euler = (0.0, 0.0, a)
        link_to(sill, frame_col)
        frames.append(sill)

    bevel = wall.modifiers.new("WindowBevel", type='BEVEL')
    bevel.width = WINDOW_BEVEL_WIDTH
    bevel.segments = 3
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = math.radians(35)
    return glass_panes, frames


def cut_door_in(wall: bpy.types.Object,
                cutter_col: bpy.types.Collection,
                door_col: bpy.types.Collection) -> bpy.types.Object:
    """Punch the door aperture at DOOR_AZIMUTH and mint a wooden door slab."""
    mid_r = (INTERNAL_RADIUS + LOWER_EXTERNAL_RADIUS) / 2.0
    depth_through = LOWER_WALL_THICKNESS + 0.40
    a = DOOR_AZIMUTH
    cutter = _make_arched_cutter(
        "DoorCutter",
        width=DOOR_WIDTH,
        rect_h=DOOR_RECT_HEIGHT,
        depth=depth_through,
        sill_z=DOOR_SILL_Z,
        radial_x=mid_r * math.cos(a),
        radial_y=mid_r * math.sin(a),
        rot_z=a,
    )
    link_to(cutter, cutter_col)
    mod = wall.modifiers.new("DoorCut", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    mod.solver = 'EXACT'

    # Eucalyptus plank door slab — thin box, sits in the rectangular portion
    # of the aperture (the arched top remains open as a transom).
    door = make_box(
        "DoorSlab",
        size=(0.06, DOOR_WIDTH - 0.04, DOOR_RECT_HEIGHT - 0.04),
        location=(mid_r * math.cos(a),
                  mid_r * math.sin(a),
                  DOOR_SILL_Z + DOOR_RECT_HEIGHT / 2.0),
    )
    door.rotation_euler = (0.0, 0.0, a)
    link_to(door, door_col)
    return door


# --------------------------------------------------------------------------- #
# Mushroom cap: 16 radial cantilevers + subfloor + slip-plane ring
# --------------------------------------------------------------------------- #


def build_mushroom_cap(col: bpy.types.Collection):
    beams = []
    beam_z_centre = (RING_BEAM_Z + RING_BEAM_HEIGHT
                     + CANTILEVER_HALF_HEIGHT)
    for i in range(CANTILEVER_COUNT):
        a = 2 * math.pi * i / CANTILEVER_COUNT
        beam = make_box(
            f"Cantilever_{i:02d}",
            size=(CANTILEVER_EXTERNAL_R,
                  CANTILEVER_HALF_WIDTH * 2.0,
                  CANTILEVER_HALF_HEIGHT * 2.0),
            location=((CANTILEVER_EXTERNAL_R / 2.0) * math.cos(a),
                      (CANTILEVER_EXTERNAL_R / 2.0) * math.sin(a),
                      beam_z_centre),
        )
        beam.rotation_euler = (0.0, 0.0, a)
        link_to(beam, col)
        beams.append(beam)

    platform_top_z = beam_z_centre + CANTILEVER_HALF_HEIGHT
    platform = make_annular_ring(
        "MushroomCapPlatform",
        inner_r=0.30,
        outer_r=CANTILEVER_EXTERNAL_R,
        thickness=SUBFLOOR_THICKNESS,
        z=platform_top_z,
        segments=96,
    )
    link_to(platform, col)

    # Slip-plane ring under the upper wall footprint — lime/concrete barrier
    # that lets the upper wall move independently from the lower envelope.
    slip = make_annular_ring(
        "SlipPlane",
        inner_r=INTERNAL_RADIUS - 0.05,
        outer_r=UPPER_BASE_OUTER + 0.05,
        thickness=SLIP_PLANE_THICKNESS,
        z=platform_top_z + SUBFLOOR_THICKNESS,
        segments=96,
    )
    link_to(slip, col)
    return beams, platform, slip


# --------------------------------------------------------------------------- #
# Upper inclined dome wall with bottle-brick inlays
# --------------------------------------------------------------------------- #


def _bezier_quad(t: float, p0: float, p1: float, p2: float) -> float:
    """Scalar 1-D quadratic Bezier: B(t) = (1-t)^2 P0 + 2(1-t)t P1 + t^2 P2."""
    u = 1.0 - t
    return u * u * p0 + 2.0 * u * t * p1 + t * t * p2


def _cap_profile_at(t: float) -> tuple[float, float, float, float]:
    """Mushroom cap profile (quadratic Bezier in (r,z)) at t in [0,1].

    Returns ``(inner_r, inner_z, outer_r, outer_z)``. Inner and outer surfaces
    have separate z-bulge control points (CAP_INNER_BULGE_Z, CAP_OUTER_BULGE_Z)
    so the dome thickens through the bulge zone before tapering to the peak —
    that's what gives the silhouette its mushroom-cap profile.
    """
    outer_r = _bezier_quad(t, CAP_OUTER_BASE_R, CAP_OUTER_BULGE_R, CAP_OUTER_PEAK_R)
    outer_z = _bezier_quad(t, UPPER_WALL_BASE_Z, CAP_OUTER_BULGE_Z, UPPER_WALL_PEAK_Z)
    inner_r = _bezier_quad(t, CAP_INNER_BASE_R, CAP_INNER_BULGE_R, CAP_INNER_PEAK_R)
    inner_z = _bezier_quad(t, UPPER_WALL_BASE_Z, CAP_INNER_BULGE_Z, UPPER_WALL_PEAK_Z)
    return inner_r, inner_z, outer_r, outer_z


def build_upper_dome(col: bpy.types.Collection,
                     segments: int = 96, z_layers: int = 16) -> bpy.types.Object:
    bm = bmesh.new()
    layers = []
    for li in range(z_layers + 1):
        t = li / z_layers
        inner_r, inner_z, outer_r, outer_z = _cap_profile_at(t)
        inner_ring, outer_ring = [], []
        for i in range(segments):
            a = 2 * math.pi * i / segments
            inner_ring.append(bm.verts.new(
                (inner_r * math.cos(a), inner_r * math.sin(a), inner_z)))
            outer_ring.append(bm.verts.new(
                (outer_r * math.cos(a), outer_r * math.sin(a), outer_z)))
        layers.append((inner_ring, outer_ring))

    # Side faces between consecutive Z layers
    for li in range(z_layers):
        ib, ob = layers[li]
        it, ot = layers[li + 1]
        for i in range(segments):
            j = (i + 1) % segments
            bm.faces.new([ob[i], ob[j], ot[j], ot[i]])
            bm.faces.new([ib[j], ib[i], it[i], it[j]])

    # Cap bottom annulus
    ib0, ob0 = layers[0]
    for i in range(segments):
        j = (i + 1) % segments
        bm.faces.new([ob0[i], ob0[j], ib0[j], ib0[i]])
    # Cap top annulus (around the peak opening)
    ibN, obN = layers[-1]
    for i in range(segments):
        j = (i + 1) % segments
        bm.faces.new([ibN[i], ibN[j], obN[j], obN[i]])

    dome = _new_mesh_obj("UpperDomeWall", bm)
    link_to(dome, col)

    sub = dome.modifiers.new("DomeSubdiv", type='SUBSURF')
    sub.subdivision_type = 'SIMPLE'
    sub.levels = 3
    sub.render_levels = 3

    # Two-layer displacement: low-freq CLOUDS for the mushroom-flesh undulation,
    # high-freq STUCCI for cob-render pebbling so the cap reads as hand-applied
    # earth plaster, not a smooth balloon (prior strength=0.025 was invisible).
    tex_clouds = bpy.data.textures.new("CobCloudsUpper", type='CLOUDS')
    tex_clouds.noise_scale = 0.85
    tex_clouds.noise_depth = 4
    disp_a = dome.modifiers.new("DomeDisplaceClouds", type='DISPLACE')
    disp_a.texture = tex_clouds
    disp_a.strength = 0.10
    disp_a.mid_level = 0.5

    tex_stucci = bpy.data.textures.new("CobStucciUpper", type='STUCCI')
    tex_stucci.noise_scale = 0.22
    tex_stucci.turbulence = 1.6
    disp_b = dome.modifiers.new("DomeDisplaceStucci", type='DISPLACE')
    disp_b.texture = tex_stucci
    disp_b.strength = 0.045
    disp_b.mid_level = 0.5
    return dome


def build_bottle_inlays(col: bpy.types.Collection):
    bottles, jutes = [], []
    for ring_idx, t in enumerate(BOTTLE_RING_T_LEVELS):
        inner_r, inner_z, outer_r, outer_z = _cap_profile_at(t)
        z = (inner_z + outer_z) * 0.5
        mid_r = (inner_r + outer_r) * 0.5
        # Radial cylinder length spans the wall + slight protrusion both sides
        bottle_len = (outer_r - inner_r) + 0.08

        for i in range(BOTTLES_PER_RING):
            a = (2 * math.pi * i / BOTTLES_PER_RING
                 + ring_idx * math.pi / BOTTLES_PER_RING)
            cx, cy = mid_r * math.cos(a), mid_r * math.sin(a)

            bottle = make_cylinder(
                f"Bottle_r{ring_idx}_{i:02d}",
                radius=BOTTLE_RADIUS, depth=bottle_len,
                segments=14,
                location=(cx, cy, z),
            )
            # bmesh cone is Z-aligned → rotate to radial direction
            bottle.rotation_euler = (math.pi / 2.0, 0.0, a + math.pi / 2.0)
            link_to(bottle, col)
            bottles.append(bottle)

            jute = make_cylinder(
                f"Jute_r{ring_idx}_{i:02d}",
                radius=BOTTLE_RADIUS + BOTTLE_JUTE_OFFSET,
                depth=bottle_len * 0.92,
                segments=14,
                location=(cx, cy, z),
            )
            jute.rotation_euler = (math.pi / 2.0, 0.0, a + math.pi / 2.0)
            link_to(jute, col)
            jutes.append(jute)
    return bottles, jutes


# --------------------------------------------------------------------------- #
# Thermal vent + parasol cap
# --------------------------------------------------------------------------- #


def build_thermal_vent(col: bpy.types.Collection):
    pipe_z_start = UPPER_WALL_PEAK_Z - 0.10  # slight overlap with peak rim
    pipe_z_end   = VENT_PIPE_TOP_Z
    pipe = make_cylinder(
        "CopperVentPipe", VENT_PIPE_RADIUS,
        pipe_z_end - pipe_z_start, segments=28,
        location=(0.0, 0.0, (pipe_z_start + pipe_z_end) / 2.0),
    )
    link_to(pipe, col)

    # 4 angled bamboo struts holding the parasol above the vent
    poles = []
    strut_z_centre = pipe_z_end + PARASOL_HOVER_GAP / 2.0
    for i in range(4):
        a = math.pi / 2 * i + math.pi / 4
        x = (VENT_PIPE_RADIUS + 0.05) * math.cos(a)
        y = (VENT_PIPE_RADIUS + 0.05) * math.sin(a)
        pole = make_cylinder(
            f"ParasolStrut_{i:02d}", 0.022,
            PARASOL_HOVER_GAP + 0.10, segments=8,
            location=(x, y, strut_z_centre),
        )
        link_to(pole, col)
        poles.append(pole)

    parasol_low_z = pipe_z_end + PARASOL_HOVER_GAP
    parasol = make_cone(
        "ParasolCap",
        r_bottom=PARASOL_RADIUS, r_top=0.06,
        depth=PARASOL_HEIGHT, segments=32,
        location=(0.0, 0.0, parasol_low_z + PARASOL_HEIGHT / 2.0),
    )
    link_to(parasol, col)
    return pipe, poles, parasol


# --------------------------------------------------------------------------- #
# Interior: core pillar, spiral staircase, earthen bench, kitchen counter
# --------------------------------------------------------------------------- #


def _make_curved_wedge(name, inner_r, outer_r, angle_start, angle_span,
                       z_bottom, thickness, segments=8) -> bpy.types.Object:
    """Curved annular wedge — used for stair treads, benches, counters."""
    bm = bmesh.new()
    rings: dict[tuple[str, str], list] = {}
    for r_key, r in (("inner", inner_r), ("outer", outer_r)):
        for z_key, dz in (("bot", 0.0), ("top", thickness)):
            ring = []
            for i in range(segments + 1):
                t = i / segments
                a = angle_start + angle_span * t
                ring.append(bm.verts.new(
                    (r * math.cos(a), r * math.sin(a), z_bottom + dz)
                ))
            rings[(r_key, z_key)] = ring
    for i in range(segments):
        bm.faces.new([rings[("inner", "top")][i], rings[("outer", "top")][i],
                      rings[("outer", "top")][i + 1], rings[("inner", "top")][i + 1]])
        bm.faces.new([rings[("inner", "bot")][i + 1], rings[("outer", "bot")][i + 1],
                      rings[("outer", "bot")][i], rings[("inner", "bot")][i]])
        bm.faces.new([rings[("outer", "bot")][i], rings[("outer", "bot")][i + 1],
                      rings[("outer", "top")][i + 1], rings[("outer", "top")][i]])
        bm.faces.new([rings[("inner", "bot")][i + 1], rings[("inner", "bot")][i],
                      rings[("inner", "top")][i], rings[("inner", "top")][i + 1]])
    bm.faces.new([rings[("inner", "bot")][0], rings[("inner", "top")][0],
                  rings[("outer", "top")][0], rings[("outer", "bot")][0]])
    bm.faces.new([rings[("outer", "bot")][segments],
                  rings[("outer", "top")][segments],
                  rings[("inner", "top")][segments],
                  rings[("inner", "bot")][segments]])
    return _new_mesh_obj(name, bm)


def build_interior(col: bpy.types.Collection):
    # Wood plank floor — full disc inside the inner wall radius. Sits just
    # above the slip plane so the lower-wall cob doesn't read as bare dirt.
    floor = make_cylinder(
        "InteriorFloor",
        radius=INTERNAL_RADIUS - 0.02,
        depth=FLOOR_THICKNESS,
        segments=64,
        location=(0.0, 0.0, FLOOR_THICKNESS / 2.0),
    )
    link_to(floor, col)

    pillar_h = LOWER_WALL_HEIGHT + 0.95
    pillar = make_cylinder(
        "CorePillar", 0.18, pillar_h, segments=18,
        location=(0.0, 0.0, FLOOR_THICKNESS + pillar_h / 2.0),
    )
    link_to(pillar, col)

    rise_per_step = LOWER_WALL_HEIGHT / STAIR_STEPS
    angle_per_step = 2 * math.pi / STAIR_STEPS   # one full turn over height
    steps = []
    for i in range(STAIR_STEPS):
        a_start = i * angle_per_step
        z_bot = FLOOR_THICKNESS + i * rise_per_step
        step = _make_curved_wedge(
            f"StairStep_{i:02d}",
            inner_r=STAIR_INNER_R, outer_r=STAIR_OUTER_R,
            angle_start=a_start,
            angle_span=angle_per_step * 0.92,  # small gap between treads
            z_bottom=z_bot,
            thickness=STAIR_THICKNESS,
            segments=6,
        )
        link_to(step, col)
        steps.append(step)

    # Sweeping earthen bench along ~140 deg of inner wall (W arc)
    bench = _make_curved_wedge(
        "EarthenBench",
        inner_r=INTERNAL_RADIUS - 0.55,
        outer_r=INTERNAL_RADIUS - 0.05,
        angle_start=math.radians(105),
        angle_span=math.radians(140),
        z_bottom=FLOOR_THICKNESS, thickness=0.45, segments=24,
    )
    link_to(bench, col)

    # Kitchen counter — narrower band, opposite side (E arc)
    counter = _make_curved_wedge(
        "KitchenCounter",
        inner_r=INTERNAL_RADIUS - 0.70,
        outer_r=INTERNAL_RADIUS - 0.05,
        angle_start=math.radians(-65),
        angle_span=math.radians(90),
        z_bottom=FLOOR_THICKNESS + 0.90, thickness=0.06, segments=24,
    )
    link_to(counter, col)

    # Hearth — fixed terracotta cylinder against inner wall in NE gap between
    # counter end (25°) and bench start (105°). Azimuth = 65°, set back so
    # the rim sits just inside the inner wall.
    hearth_az = math.radians(65.0)
    hearth_off_r = INTERNAL_RADIUS - HEARTH_RADIUS - 0.05
    hearth = make_cylinder(
        "Hearth",
        radius=HEARTH_RADIUS,
        depth=HEARTH_HEIGHT,
        segments=32,
        location=(hearth_off_r * math.cos(hearth_az),
                  hearth_off_r * math.sin(hearth_az),
                  FLOOR_THICKNESS + HEARTH_HEIGHT / 2.0),
    )
    link_to(hearth, col)

    # Loft — half-circle mezzanine over the north half (away from door).
    # Sits at ~55% of lower-wall height so a head clearance band remains
    # under the cap and above ground floor.
    loft_z = LOWER_WALL_HEIGHT * 0.55
    loft = _make_curved_wedge(
        "LoftPlatform",
        inner_r=LOFT_INNER_R,
        outer_r=LOFT_OUTER_R,
        angle_start=math.radians(0.0),
        angle_span=math.radians(180.0),
        z_bottom=loft_z,
        thickness=FLOOR_THICKNESS,
        segments=32,
    )
    link_to(loft, col)

    return pillar, steps, bench, counter, floor, hearth, loft


# --------------------------------------------------------------------------- #
# Ground slab
# --------------------------------------------------------------------------- #


def build_ground(col: bpy.types.Collection) -> tuple[bpy.types.Object, bpy.types.Object]:
    """Grass slab + dirt path leading from door azimuth out into the parcel.

    Returns (grass, path). The path is an annular wedge centred on
    DOOR_AZIMUTH, sitting 1 cm above the grass slab to avoid z-fighting.
    """
    grass = make_cylinder(
        "GrassSlab", GROUND_RADIUS, GROUND_THICKNESS, segments=128,
        location=(0.0, 0.0, -GROUND_THICKNESS / 2.0),
    )
    link_to(grass, col)

    path_span = math.radians(22.0)
    path = _make_curved_wedge(
        "DirtPath",
        inner_r=PATH_INNER_R,
        outer_r=GROUND_RADIUS * 0.55,   # ~14 m out, plenty of approach run
        angle_start=DOOR_AZIMUTH - path_span / 2.0,
        angle_span=path_span,
        z_bottom=0.002,                 # float just above grass top
        thickness=0.018,
        segments=48,
    )
    link_to(path, col)
    return grass, path


# --------------------------------------------------------------------------- #
# Scenery — trees + rocks scattered in a band outside the path ring
# --------------------------------------------------------------------------- #


def _make_cone(
    name: str,
    radius_bot: float,
    radius_top: float,
    depth: float,
    *,
    location=(0.0, 0.0, 0.0),
    segments: int = 24,
) -> bpy.types.Object:
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=True,
        segments=segments,
        radius1=radius_bot,
        radius2=radius_top,
        depth=depth,
    )
    mesh = bpy.data.meshes.new(name + "_mesh")
    bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = Vector(location)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def _make_icosphere(
    name: str,
    radius: float,
    *,
    location=(0.0, 0.0, 0.0),
    subdivisions: int = 2,
) -> bpy.types.Object:
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdivisions, radius=radius)
    mesh = bpy.data.meshes.new(name + "_mesh")
    bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = Vector(location)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def build_scenery(
    col: bpy.types.Collection,
) -> tuple[list, list, list]:
    """Scatter trees + rocks in a band outside the path ring.

    Returns (trunks, foliage, rocks). RNG is assumed to have been seeded
    by the caller after materials are built — placement is deterministic
    across runs as long as the seed is fixed.
    """
    trunks: list = []
    foliage: list = []
    rocks: list = []

    inner = TREE_RING_INNER
    outer = TREE_RING_OUTER
    band = outer - inner

    # Camera→house sightline corridor. Hero camera sits at azimuth -π/4 (SE
    # corner) from origin; trees in this wedge block the cap. Push trees out
    # of a ±0.32 rad (~18°) wedge so the foreground is open.
    sightline_az = -math.pi / 4.0
    corridor = 0.32

    for i in range(TREE_COUNT):
        base_az = (i / TREE_COUNT) * 2 * math.pi
        az = base_az + random.uniform(-0.22, 0.22)
        # Clamp out of the camera-sightline corridor by rotating the offending
        # tree to the nearest corridor edge with a margin.
        delta = math.atan2(math.sin(az - sightline_az), math.cos(az - sightline_az))
        if abs(delta) < corridor:
            az = sightline_az + math.copysign(corridor + 0.05, delta)

        r = inner + random.betavariate(2.4, 1.6) * band
        x = r * math.cos(az)
        y = r * math.sin(az)

        trunk_h = random.uniform(4.5, 7.5)
        trunk_r = random.uniform(0.10, 0.18)
        trunk = make_cylinder(
            f"Tree_{i:02d}_Trunk",
            radius=trunk_r,
            depth=trunk_h,
            segments=12,
            location=(x, y, trunk_h / 2.0),
        )
        trunk.rotation_euler = (
            random.uniform(-0.04, 0.04),
            random.uniform(-0.04, 0.04),
            0.0,
        )
        link_to(trunk, col)
        trunks.append(trunk)

        # Multi-cluster crown — 4 overlapping icospheres at random offsets in a
        # hemispherical envelope above the trunk top. Reads as a lapacho-style
        # irregular crown instead of a single balloon. Per-cluster obj.color
        # drives the Canopy_Foliage shader's ObjectInfo input so each tree
        # picks its own green from the material's color ramp; tiny per-cluster
        # tint jitter inside one tree breaks up the silhouette.
        canopy_tint = random.uniform(0.05, 0.95)
        canopy_base_r = random.uniform(1.9, 2.8)
        canopy_base_z = trunk_h + canopy_base_r * 0.30

        cluster_layout = [
            # (radial_offset, az_phase, height_offset_factor, radius_factor)
            (0.0,            0.0,           0.30, 1.00),
            (canopy_base_r * 0.55, 0.0,     0.05, 0.78),
            (canopy_base_r * 0.55, 2.094,   0.05, 0.78),  # +120°
            (canopy_base_r * 0.55, 4.189,   0.05, 0.78),  # +240°
            (0.0,            0.0,           0.85, 0.62),  # crown cap
        ]
        for ci, (roff, phase, hf, rf) in enumerate(cluster_layout):
            phase_az = az + phase + random.uniform(-0.4, 0.4)
            jitter_r = roff * random.uniform(0.75, 1.15)
            cx = x + jitter_r * math.cos(phase_az)
            cy = y + jitter_r * math.sin(phase_az)
            cr = canopy_base_r * rf * random.uniform(0.85, 1.10)
            cz = canopy_base_z + canopy_base_r * hf + random.uniform(-0.15, 0.15)
            cluster = _make_icosphere(
                f"Tree_{i:02d}_Leaf{ci}",
                radius=cr,
                subdivisions=3,
                location=(cx, cy, cz),
            )
            cluster.scale = (
                random.uniform(0.88, 1.12),
                random.uniform(0.88, 1.12),
                random.uniform(0.78, 1.08),
            )
            cluster.rotation_euler = (
                random.uniform(-0.18, 0.18),
                random.uniform(-0.18, 0.18),
                random.uniform(0.0, 2 * math.pi),
            )
            # Per-cluster tint jitter ±0.06 around tree's base tint so the
            # crown breaks into light/shadow patches in the shader's ramp.
            tint = max(0.0, min(1.0, canopy_tint + random.uniform(-0.06, 0.06)))
            cluster.color = (tint, tint, tint, 1.0)
            link_to(cluster, col)
            foliage.append(cluster)

    for i in range(ROCK_COUNT):
        az = random.uniform(0.0, 2 * math.pi)
        # Rocks sit closer to the house edge — between path band and tree ring
        r = random.uniform(LOWER_EXTERNAL_RADIUS + 1.5, TREE_RING_INNER - 0.5)
        x = r * math.cos(az)
        y = r * math.sin(az)
        rk_r = random.uniform(0.22, 0.55)
        rock = _make_icosphere(
            f"Rock_{i:02d}",
            radius=rk_r,
            subdivisions=2,
            location=(x, y, rk_r * 0.45),
        )
        rock.scale = (
            random.uniform(0.85, 1.25),
            random.uniform(0.85, 1.25),
            random.uniform(0.45, 0.85),
        )
        rock.rotation_euler = (
            random.uniform(-0.25, 0.25),
            random.uniform(-0.25, 0.25),
            random.uniform(0.0, 2 * math.pi),
        )
        link_to(rock, col)
        rocks.append(rock)

    return trunks, foliage, rocks


# --------------------------------------------------------------------------- #
# PBR materials — node-graph authoring, Cycles-ready
# --------------------------------------------------------------------------- #


def _set_principled(bsdf, alias_or_name: str, value) -> None:
    """Set a Principled BSDF socket, tolerating Blender 3.x → 4.x rename."""
    aliases = {
        "Transmission":   ["Transmission Weight", "Transmission"],
        "Subsurface":     ["Subsurface Weight", "Subsurface"],
        "Specular":       ["Specular IOR Level", "Specular"],
        "Sheen":          ["Sheen Weight", "Sheen"],
        "Coat":           ["Coat Weight", "Coat", "Clearcoat"],
    }
    names = aliases.get(alias_or_name, [alias_or_name])
    for n in names:
        if n in bsdf.inputs:
            bsdf.inputs[n].default_value = value
            return


def _fresh_material(name: str):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (600, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (320, 0)
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat, nt, bsdf


def _build_cob_material(name: str, color):
    mat, nt, bsdf = _fresh_material(name)
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = 0.96
    bsdf.inputs["Metallic"].default_value = 0.0

    coord = nt.nodes.new("ShaderNodeTexCoord"); coord.location = (-720, -100)
    mapping = nt.nodes.new("ShaderNodeMapping"); mapping.location = (-540, -100)
    mapping.inputs["Scale"].default_value = (1.0, 1.0, 1.0)

    # Macro noise for plaster blobs
    noise_big = nt.nodes.new("ShaderNodeTexNoise"); noise_big.location = (-320, -40)
    noise_big.inputs["Scale"].default_value = 6.0
    noise_big.inputs["Detail"].default_value = 6.0
    noise_big.inputs["Roughness"].default_value = 0.70

    # Fine noise for trowel-grain texture
    noise_fine = nt.nodes.new("ShaderNodeTexNoise"); noise_fine.location = (-320, -260)
    noise_fine.inputs["Scale"].default_value = 38.0
    noise_fine.inputs["Detail"].default_value = 10.0
    noise_fine.inputs["Roughness"].default_value = 0.55

    mix = nt.nodes.new("ShaderNodeMixRGB"); mix.location = (-60, -150)
    mix.blend_type = 'MIX'
    mix.inputs["Fac"].default_value = 0.55

    # Tone variation feeds back into base color so cob doesn't read uniform
    tone = nt.nodes.new("ShaderNodeValToRGB"); tone.location = (-60, 80)
    tone.color_ramp.elements[0].position = 0.30
    tone.color_ramp.elements[0].color = (color[0] * 0.78, color[1] * 0.78, color[2] * 0.78, 1.0)
    tone.color_ramp.elements[1].position = 0.85
    tone.color_ramp.elements[1].color = (
        min(color[0] * 1.18, 1.0),
        min(color[1] * 1.18, 1.0),
        min(color[2] * 1.18, 1.0),
        1.0,
    )

    bump = nt.nodes.new("ShaderNodeBump"); bump.location = (160, -260)
    bump.inputs["Strength"].default_value = 0.90
    bump.inputs["Distance"].default_value = 0.06

    nt.links.new(coord.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], noise_big.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], noise_fine.inputs["Vector"])
    nt.links.new(noise_big.outputs["Fac"], mix.inputs["Color1"])
    nt.links.new(noise_fine.outputs["Fac"], mix.inputs["Color2"])
    nt.links.new(noise_big.outputs["Fac"], tone.inputs["Fac"])
    nt.links.new(tone.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(mix.outputs["Color"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def _build_wood_material():
    mat, nt, bsdf = _fresh_material("Eucalyptus_Timber")
    bsdf.inputs["Roughness"].default_value = 0.72

    coord = nt.nodes.new("ShaderNodeTexCoord"); coord.location = (-720, 0)
    mapping = nt.nodes.new("ShaderNodeMapping"); mapping.location = (-540, 0)
    mapping.inputs["Scale"].default_value = (1.0, 1.0, 22.0)

    grain = nt.nodes.new("ShaderNodeTexNoise"); grain.location = (-340, 0)
    grain.inputs["Scale"].default_value = 6.0
    grain.inputs["Detail"].default_value = 8.0
    grain.inputs["Distortion"].default_value = 0.35

    ramp = nt.nodes.new("ShaderNodeValToRGB"); ramp.location = (-140, 0)
    ramp.color_ramp.elements[0].position = 0.30
    ramp.color_ramp.elements[0].color = (0.16, 0.08, 0.04, 1.0)
    ramp.color_ramp.elements[1].position = 0.85
    ramp.color_ramp.elements[1].color = (0.38, 0.22, 0.12, 1.0)

    bump = nt.nodes.new("ShaderNodeBump"); bump.location = (100, -180)
    bump.inputs["Strength"].default_value = 0.25

    nt.links.new(coord.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], grain.inputs["Vector"])
    nt.links.new(grain.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(grain.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def _build_bottle_material(tag: str, color):
    mat, _, bsdf = _fresh_material(f"Glass_Bottle_{tag}")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = 0.05
    bsdf.inputs["IOR"].default_value = 1.46
    _set_principled(bsdf, "Transmission", 1.0)
    return mat


def _build_jute_material():
    mat, _, bsdf = _fresh_material("Jute_Hemp_Wrap")
    bsdf.inputs["Base Color"].default_value = (0.52, 0.40, 0.22, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.98
    _set_principled(bsdf, "Sheen", 0.3)
    return mat


def _build_microcement_material():
    mat, _, bsdf = _fresh_material("Polished_Microcement")
    bsdf.inputs["Base Color"].default_value = (0.78, 0.74, 0.68, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.20
    bsdf.inputs["Metallic"].default_value = 0.0
    return mat


def _build_copper_material():
    mat, _, bsdf = _fresh_material("Weathering_Copper")
    bsdf.inputs["Base Color"].default_value = (0.42, 0.50, 0.40, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.45
    bsdf.inputs["Metallic"].default_value = 0.85
    return mat


def _build_thatch_material():
    mat, nt, bsdf = _fresh_material("Thatched_Parasol")
    # Stretch noise radially along thatch bundles via TexCoord + Mapping
    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-1100, 0)
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.location = (-900, 0)
    mapping.inputs["Scale"].default_value = (8.0, 1.0, 1.0)
    nt.links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])

    # Macro: thatch bundle stripes — golden-brown tonal variation
    noise_macro = nt.nodes.new("ShaderNodeTexNoise")
    noise_macro.location = (-700, 200)
    noise_macro.inputs["Scale"].default_value = 14.0
    noise_macro.inputs["Detail"].default_value = 6.0
    noise_macro.inputs["Roughness"].default_value = 0.65
    nt.links.new(mapping.outputs["Vector"], noise_macro.inputs["Vector"])

    # Fine: straw fibers feeding bump
    noise_fine = nt.nodes.new("ShaderNodeTexNoise")
    noise_fine.location = (-700, -100)
    noise_fine.inputs["Scale"].default_value = 80.0
    noise_fine.inputs["Detail"].default_value = 10.0
    noise_fine.inputs["Roughness"].default_value = 0.60
    nt.links.new(mapping.outputs["Vector"], noise_fine.inputs["Vector"])

    # Color ramp: dark thatch shadow → sun-bleached golden straw
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-450, 200)
    ramp.color_ramp.elements[0].position = 0.30
    ramp.color_ramp.elements[0].color = (0.32, 0.22, 0.12, 1.0)
    ramp.color_ramp.elements[1].position = 0.85
    ramp.color_ramp.elements[1].color = (0.58, 0.44, 0.24, 1.0)
    nt.links.new(noise_macro.outputs["Fac"], ramp.inputs["Fac"])

    # Bump from fine noise — straw fibers
    bump = nt.nodes.new("ShaderNodeBump")
    bump.location = (-200, -100)
    bump.inputs["Strength"].default_value = 0.70
    bump.inputs["Distance"].default_value = 0.03
    nt.links.new(noise_fine.outputs["Fac"], bump.inputs["Height"])

    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Roughness"].default_value = 0.95
    bsdf.inputs["Metallic"].default_value = 0.0
    _set_principled(bsdf, "Sheen Weight", 0.20)
    return mat


def _build_grass_material():
    """Subtropical grass turf — chartreuse-leaning dry-season Paraguarí green
    with two-tier noise so the disk doesn't read as a billiard table."""
    mat, nt, bsdf = _fresh_material("Subtropical_Grass")
    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-1100, 0)

    patch = nt.nodes.new("ShaderNodeTexNoise")
    patch.location = (-850, 200)
    patch.inputs["Scale"].default_value = 4.0
    patch.inputs["Detail"].default_value = 6.0
    patch.inputs["Roughness"].default_value = 0.70
    nt.links.new(tex_coord.outputs["Generated"], patch.inputs["Vector"])

    blade = nt.nodes.new("ShaderNodeTexNoise")
    blade.location = (-850, -100)
    blade.inputs["Scale"].default_value = 120.0
    blade.inputs["Detail"].default_value = 8.0
    blade.inputs["Roughness"].default_value = 0.50
    nt.links.new(tex_coord.outputs["Generated"], blade.inputs["Vector"])

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-550, 200)
    ramp.color_ramp.elements[0].position = 0.25
    ramp.color_ramp.elements[0].color = (0.18, 0.26, 0.10, 1.0)  # shaded green
    ramp.color_ramp.elements[1].position = 0.85
    ramp.color_ramp.elements[1].color = (0.42, 0.52, 0.18, 1.0)  # sun-bleached
    nt.links.new(patch.outputs["Fac"], ramp.inputs["Fac"])

    bump = nt.nodes.new("ShaderNodeBump")
    bump.location = (-300, -100)
    bump.inputs["Strength"].default_value = 0.55
    bump.inputs["Distance"].default_value = 0.02
    nt.links.new(blade.outputs["Fac"], bump.inputs["Height"])

    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Roughness"].default_value = 0.92
    bsdf.inputs["Metallic"].default_value = 0.0
    return mat


def _build_dirt_path_material():
    """Compacted dirt path — sienna/ochre with footfall variance."""
    mat, nt, bsdf = _fresh_material("Compacted_Dirt_Path")
    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-1000, 0)

    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.location = (-750, 100)
    noise.inputs["Scale"].default_value = 12.0
    noise.inputs["Detail"].default_value = 8.0
    noise.inputs["Roughness"].default_value = 0.60
    nt.links.new(tex_coord.outputs["Generated"], noise.inputs["Vector"])

    grit = nt.nodes.new("ShaderNodeTexNoise")
    grit.location = (-750, -150)
    grit.inputs["Scale"].default_value = 55.0
    grit.inputs["Detail"].default_value = 9.0
    nt.links.new(tex_coord.outputs["Generated"], grit.inputs["Vector"])

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-450, 100)
    ramp.color_ramp.elements[0].position = 0.30
    ramp.color_ramp.elements[0].color = (0.32, 0.22, 0.13, 1.0)
    ramp.color_ramp.elements[1].position = 0.80
    ramp.color_ramp.elements[1].color = (0.54, 0.40, 0.24, 1.0)
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])

    bump = nt.nodes.new("ShaderNodeBump")
    bump.location = (-200, -150)
    bump.inputs["Strength"].default_value = 0.45
    bump.inputs["Distance"].default_value = 0.025
    nt.links.new(grit.outputs["Fac"], bump.inputs["Height"])

    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Roughness"].default_value = 0.94
    return mat


def _build_glass_pane_material():
    """Clear glazing for window panes — transmissive, low-roughness."""
    mat, _, bsdf = _fresh_material("Window_Glass_Pane")
    bsdf.inputs["Base Color"].default_value = (0.92, 0.95, 0.97, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.05
    bsdf.inputs["Metallic"].default_value = 0.0
    _set_principled(bsdf, "Transmission", 1.0)
    _set_principled(bsdf, "IOR", 1.45)
    return mat


def _build_door_material():
    """Eucalyptus plank door — vertical-grain tonal striping."""
    mat, nt, bsdf = _fresh_material("Eucalyptus_Door_Plank")
    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-1100, 0)
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.location = (-900, 0)
    mapping.inputs["Scale"].default_value = (1.0, 18.0, 1.0)  # vertical grain
    nt.links.new(tex_coord.outputs["Object"], mapping.inputs["Vector"])

    grain = nt.nodes.new("ShaderNodeTexNoise")
    grain.location = (-700, 100)
    grain.inputs["Scale"].default_value = 8.0
    grain.inputs["Detail"].default_value = 12.0
    grain.inputs["Roughness"].default_value = 0.55
    nt.links.new(mapping.outputs["Vector"], grain.inputs["Vector"])

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-450, 100)
    ramp.color_ramp.elements[0].position = 0.30
    ramp.color_ramp.elements[0].color = (0.25, 0.14, 0.07, 1.0)
    ramp.color_ramp.elements[1].position = 0.85
    ramp.color_ramp.elements[1].color = (0.55, 0.32, 0.16, 1.0)
    nt.links.new(grain.outputs["Fac"], ramp.inputs["Fac"])

    bump = nt.nodes.new("ShaderNodeBump")
    bump.location = (-200, -100)
    bump.inputs["Strength"].default_value = 0.40
    bump.inputs["Distance"].default_value = 0.015
    nt.links.new(grain.outputs["Fac"], bump.inputs["Height"])

    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Roughness"].default_value = 0.70
    return mat


def _build_hearth_material():
    """Fired terracotta hearth — warm clay with subtle soot variance."""
    mat, nt, bsdf = _fresh_material("Terracotta_Hearth")
    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-1000, 0)

    soot = nt.nodes.new("ShaderNodeTexNoise")
    soot.location = (-750, 0)
    soot.inputs["Scale"].default_value = 22.0
    soot.inputs["Detail"].default_value = 8.0
    soot.inputs["Roughness"].default_value = 0.65
    nt.links.new(tex_coord.outputs["Generated"], soot.inputs["Vector"])

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-450, 0)
    ramp.color_ramp.elements[0].position = 0.30
    ramp.color_ramp.elements[0].color = (0.18, 0.08, 0.05, 1.0)  # soot
    ramp.color_ramp.elements[1].position = 0.80
    ramp.color_ramp.elements[1].color = (0.58, 0.24, 0.12, 1.0)  # terracotta
    nt.links.new(soot.outputs["Fac"], ramp.inputs["Fac"])

    bump = nt.nodes.new("ShaderNodeBump")
    bump.location = (-200, -100)
    bump.inputs["Strength"].default_value = 0.35
    bump.inputs["Distance"].default_value = 0.02
    nt.links.new(soot.outputs["Fac"], bump.inputs["Height"])

    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Roughness"].default_value = 0.88
    return mat


def _build_stone_material():
    """Field stone — grey granite/basalt for scenery rocks."""
    mat, nt, bsdf = _fresh_material("Field_Stone")
    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-1000, 0)

    macro = nt.nodes.new("ShaderNodeTexNoise")
    macro.location = (-750, 100)
    macro.inputs["Scale"].default_value = 8.0
    macro.inputs["Detail"].default_value = 10.0
    macro.inputs["Roughness"].default_value = 0.60
    nt.links.new(tex_coord.outputs["Object"], macro.inputs["Vector"])

    pits = nt.nodes.new("ShaderNodeTexNoise")
    pits.location = (-750, -150)
    pits.inputs["Scale"].default_value = 45.0
    pits.inputs["Detail"].default_value = 10.0
    nt.links.new(tex_coord.outputs["Object"], pits.inputs["Vector"])

    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-450, 100)
    ramp.color_ramp.elements[0].position = 0.30
    ramp.color_ramp.elements[0].color = (0.22, 0.20, 0.18, 1.0)
    ramp.color_ramp.elements[1].position = 0.85
    ramp.color_ramp.elements[1].color = (0.55, 0.52, 0.48, 1.0)
    nt.links.new(macro.outputs["Fac"], ramp.inputs["Fac"])

    bump = nt.nodes.new("ShaderNodeBump")
    bump.location = (-200, -150)
    bump.inputs["Strength"].default_value = 0.70
    bump.inputs["Distance"].default_value = 0.04
    nt.links.new(pits.outputs["Fac"], bump.inputs["Height"])

    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Roughness"].default_value = 0.85
    return mat


def _build_leaf_material():
    """Subtropical canopy — per-tree green driven by Object Info color.

    Each tree sets ``obj.color`` to a scalar 0..1 in build_scenery; we feed
    obj.color.R into a color ramp spanning lapacho-dark to lapacho-bright so
    the grove reads as a real mixed-age canopy rather than 22 identical blobs.
    A second noise pass adds within-leaf variation for waxy highlights.
    """
    mat, nt, bsdf = _fresh_material("Canopy_Foliage")
    tex_coord = nt.nodes.new("ShaderNodeTexCoord")
    tex_coord.location = (-1300, -100)

    # Per-tree tint: Object Info → separate XYZ → ramp.
    obj_info = nt.nodes.new("ShaderNodeObjectInfo")
    obj_info.location = (-1300, 250)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    sep.location = (-1050, 250)
    nt.links.new(obj_info.outputs["Color"], sep.inputs["Vector"])

    tree_ramp = nt.nodes.new("ShaderNodeValToRGB")
    tree_ramp.location = (-800, 250)
    cr = tree_ramp.color_ramp
    cr.elements[0].position = 0.0
    cr.elements[0].color = (0.05, 0.13, 0.04, 1.0)   # deep lapacho shade
    cr.elements[1].position = 1.0
    cr.elements[1].color = (0.22, 0.36, 0.11, 1.0)   # sun-bleached canopy top
    mid = cr.elements.new(0.55)
    mid.color = (0.12, 0.26, 0.07, 1.0)
    nt.links.new(sep.outputs["X"], tree_ramp.inputs["Fac"])

    # Within-leaf noise variation, mixed atop the per-tree base.
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.location = (-1050, -100)
    noise.inputs["Scale"].default_value = 22.0
    noise.inputs["Detail"].default_value = 8.0
    noise.inputs["Roughness"].default_value = 0.62
    nt.links.new(tex_coord.outputs["Object"], noise.inputs["Vector"])

    leaf_ramp = nt.nodes.new("ShaderNodeValToRGB")
    leaf_ramp.location = (-800, -100)
    leaf_ramp.color_ramp.elements[0].position = 0.30
    leaf_ramp.color_ramp.elements[0].color = (0.04, 0.10, 0.03, 1.0)
    leaf_ramp.color_ramp.elements[1].position = 0.85
    leaf_ramp.color_ramp.elements[1].color = (0.20, 0.36, 0.12, 1.0)
    nt.links.new(noise.outputs["Fac"], leaf_ramp.inputs["Fac"])

    mix = nt.nodes.new("ShaderNodeMixRGB")
    mix.location = (-500, 100)
    mix.blend_type = 'MULTIPLY'
    mix.inputs["Fac"].default_value = 0.55
    nt.links.new(tree_ramp.outputs["Color"], mix.inputs["Color1"])
    nt.links.new(leaf_ramp.outputs["Color"], mix.inputs["Color2"])

    nt.links.new(mix.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.55
    bsdf.inputs["Metallic"].default_value = 0.0
    _set_principled(bsdf, "Sheen Weight", 0.30)
    return mat


def build_materials() -> dict:
    return {
        "cob_lower":    _build_cob_material("Earthen_Cob_Plaster_Lower",
                                            (0.62, 0.46, 0.34, 1.0)),
        "cob_upper":    _build_cob_material("Earthen_Cob_Plaster_Upper",
                                            (0.58, 0.41, 0.28, 1.0)),
        "wood":         _build_wood_material(),
        "bottles": {
            "amber":   _build_bottle_material("Amber",   (0.62, 0.34, 0.10, 1.0)),
            "emerald": _build_bottle_material("Emerald", (0.10, 0.42, 0.18, 1.0)),
            "cobalt":  _build_bottle_material("Cobalt",  (0.08, 0.18, 0.55, 1.0)),
        },
        "jute":         _build_jute_material(),
        "microcement":  _build_microcement_material(),
        "copper":       _build_copper_material(),
        "thatch":       _build_thatch_material(),
        "grass":        _build_grass_material(),
        "dirt_path":    _build_dirt_path_material(),
        "glass_pane":   _build_glass_pane_material(),
        "door":         _build_door_material(),
        "hearth":       _build_hearth_material(),
        "stone":        _build_stone_material(),
        "leaf":         _build_leaf_material(),
    }


# --------------------------------------------------------------------------- #
# Material assignment
# --------------------------------------------------------------------------- #


def assign_material(obj: bpy.types.Object, mat: bpy.types.Material) -> None:
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


def assign_all(mats: dict, *,
               columns, ring_beams, lower_wall, cantilevers, platform, slip,
               upper_wall, bottles, jutes, copper_pipe, parasol_poles, parasol,
               grass_obj, path_obj, pillar, stair_steps, bench, counter,
               floor, hearth, loft,
               glass_panes, frames, door,
               scenery_trunks, scenery_foliage, scenery_rocks) -> None:
    wood = mats["wood"]
    for obj in (*columns, *ring_beams, *cantilevers, *parasol_poles,
                *stair_steps, pillar, platform):
        assign_material(obj, wood)
    assign_material(lower_wall, mats["cob_lower"])
    assign_material(upper_wall, mats["cob_upper"])
    assign_material(bench, mats["cob_lower"])
    assign_material(slip, mats["microcement"])
    assign_material(counter, mats["microcement"])
    assign_material(grass_obj, mats["grass"])
    assign_material(path_obj, mats["dirt_path"])
    assign_material(floor, mats["wood"])
    assign_material(hearth, mats["hearth"])
    assign_material(loft, mats["wood"])
    assign_material(door, mats["door"])
    assign_material(copper_pipe, mats["copper"])
    assign_material(parasol, mats["thatch"])
    for jute in jutes:
        assign_material(jute, mats["jute"])
    for pane in glass_panes:
        assign_material(pane, mats["glass_pane"])
    for frame in frames:
        assign_material(frame, mats["wood"])
    for trunk in scenery_trunks:
        assign_material(trunk, mats["wood"])
    for foliage in scenery_foliage:
        assign_material(foliage, mats["leaf"])
    for rock in scenery_rocks:
        assign_material(rock, mats["stone"])

    bottle_tags = ("amber", "emerald", "cobalt")
    for i, bottle in enumerate(bottles):
        assign_material(bottle, mats["bottles"][bottle_tags[i % 3]])


# --------------------------------------------------------------------------- #
# Camera, lighting, world, render
# --------------------------------------------------------------------------- #


CAMERA_VARIANTS = {
    # Wide hero — pulled beyond TREE_RING_OUTER=32 and raised to Z=14.5 so the
    # sightline shoots above the new ~12 m tree-top band onto the cap. Target
    # lifted to 8.0 keeps the cap centered vertically with walls + door visible
    # below. With the SW foreground arc cleared by build_scenery's az_skip
    # corridor, there is now a clean line from camera → door → opposing trees.
    "hero": dict(
        lens=30.0,
        location=(42.0, -42.0, 19.5),
        target=(0.0, 0.0, 8.5),
    ),
    # 3/4 elevation — half-aerial so foreground tree-tops drop below the
    # sightline; lens at 50 frames stem + cap + voladizo + bottle band.
    "elev": dict(
        lens=50.0,
        location=(36.0, -36.0, 18.0),
        target=(0.0, 0.0, 6.0),
    ),
    # Top-down 3/4 — cap, parasol, vent from above; cantilever spokes
    # radiating below the cap flange.
    "aerial": dict(
        lens=34.0,
        location=(11.0, -11.0, 19.0),
        target=(0.0, 0.0, 5.0),
    ),
}


def setup_camera_and_lights(variant: str = "hero"):
    cfg = CAMERA_VARIANTS.get(variant, CAMERA_VARIANTS["hero"])
    cam_data = bpy.data.cameras.new(f"MainCamera_{variant}")
    cam_data.lens = cfg["lens"]
    cam_data.clip_end = 1000.0  # HOUSE_CLIP_END_M
    cam = bpy.data.objects.new(f"MainCamera_{variant}", cam_data)
    cam.location = cfg["location"]
    target = Vector(cfg["target"])
    direction = target - Vector(cam.location)
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam

    # Key sun: brief says "Angle = 45°" — interpreted as solar elevation
    # (X rotation) for deep dramatic shadows under the alero and arches.
    sun_data = bpy.data.lights.new("KeySun", type='SUN')
    sun_data.energy = 6.0
    sun_data.angle = math.radians(2.0)  # disk size → crisp shadow edges
    sun = bpy.data.objects.new("KeySun", sun_data)
    sun.location = (0.0, 0.0, 15.0)
    sun.rotation_euler = (math.radians(45.0), 0.0, math.radians(35.0))
    bpy.context.scene.collection.objects.link(sun)

    # Soft fill from the camera side so interior cob isn't a pure black void.
    fill_data = bpy.data.lights.new("FillArea", type='AREA')
    fill_data.energy = 120.0
    fill_data.size = 6.0
    fill = bpy.data.objects.new("FillArea", fill_data)
    fill.location = (7.0, -7.0, 4.5)
    fill_dir = Vector((0.0, 0.0, 2.5)) - Vector(fill.location)
    fill.rotation_euler = fill_dir.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.collection.objects.link(fill)

    # Nishita physical sky — subtropical Paraguarí afternoon light, slight
    # haze for the 25.6°S latitude band. Drives realistic horizon gradient
    # + warm key from the same direction as KeySun.
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    wnt = world.node_tree
    for n in list(wnt.nodes):
        wnt.nodes.remove(n)
    w_out = wnt.nodes.new("ShaderNodeOutputWorld"); w_out.location = (400, 0)
    w_bg  = wnt.nodes.new("ShaderNodeBackground");  w_bg.location  = (200, 0)
    w_sky = wnt.nodes.new("ShaderNodeTexSky");      w_sky.location = (-50, 0)
    try:
        w_sky.sky_type = 'NISHITA'
        w_sky.sun_elevation = math.radians(32.0)
        w_sky.sun_rotation = math.radians(-55.0)
        w_sky.air_density = 1.0
        w_sky.dust_density = 0.3
        w_sky.ozone_density = 1.0
        if hasattr(w_sky, "altitude"):
            w_sky.altitude = 120.0
    except (AttributeError, TypeError):
        pass
    w_bg.inputs["Strength"].default_value = 1.0
    wnt.links.new(w_sky.outputs["Color"], w_bg.inputs["Color"])
    wnt.links.new(w_bg.outputs["Background"], w_out.inputs["Surface"])
    return cam, sun


def setup_render():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 256
    scene.cycles.use_denoising = True
    if hasattr(scene.cycles, 'denoiser'):
        try:
            scene.cycles.denoiser = 'OPENIMAGEDENOISE'
        except TypeError:
            pass
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.film_transparent = False

    try:
        scene.view_settings.view_transform = 'AgX'
        scene.view_settings.look = 'AgX - Punchy'
    except (TypeError, AttributeError):
        try:
            scene.view_settings.view_transform = 'Filmic'
        except (TypeError, AttributeError):
            pass


# --------------------------------------------------------------------------- #
# Orchestrator
# --------------------------------------------------------------------------- #


def main() -> None:
    print("[mushroom_cob_house] clearing scene")
    clear_scene()
    setup_units()

    cols = {
        "timber":        get_or_make_collection("Structural_Timber"),
        "lower":         get_or_make_collection("Lower_Cob_Wall"),
        "cap":           get_or_make_collection("Mushroom_Cap_Platform"),
        "upper":         get_or_make_collection("Upper_Dome_Wall"),
        "vent":          get_or_make_collection("Thermal_Vent"),
        "interior":      get_or_make_collection("Interior"),
        "site":          get_or_make_collection("Site"),
        "windows":       get_or_make_collection("_WindowCutters"),
        "window_glass":  get_or_make_collection("WindowGlass"),
        "window_frames": get_or_make_collection("WindowFrames"),
        "door_cutters":  get_or_make_collection("_DoorCutters"),
        "door":          get_or_make_collection("Door"),
        "scenery":       get_or_make_collection("Scenery"),
    }
    # Hide cutter helpers from viewport + render; boolean modifier still resolves.
    for key in ("windows", "door_cutters"):
        cols[key].hide_viewport = True
        cols[key].hide_render = True

    print("[mushroom_cob_house] building materials")
    mats = build_materials()
    # Seed RNG AFTER materials, BEFORE first build_* so scenery scatter
    # + any noise-driven placement is deterministic across runs.
    random.seed(20260617)

    print("[mushroom_cob_house] building geometry")
    grass_obj, path_obj = build_ground(cols["site"])
    columns      = build_columns(cols["timber"])
    ring_beams   = build_ring_beam(cols["timber"])
    lower_wall   = build_lower_cob_wall(cols["lower"])
    glass_panes, frames = cut_windows_in(
        lower_wall, cols["windows"], cols["window_glass"], cols["window_frames"],
    )
    door = cut_door_in(lower_wall, cols["door_cutters"], cols["door"])

    cantilevers, platform, slip = build_mushroom_cap(cols["cap"])
    upper_wall   = build_upper_dome(cols["upper"])
    bottles, jutes = build_bottle_inlays(cols["upper"])
    copper_pipe, parasol_poles, parasol = build_thermal_vent(cols["vent"])
    pillar, stair_steps, bench, counter, floor, hearth, loft = build_interior(
        cols["interior"],
    )
    scenery_trunks, scenery_foliage, scenery_rocks = build_scenery(cols["scenery"])

    print("[mushroom_cob_house] assigning materials")
    assign_all(
        mats,
        columns=columns, ring_beams=ring_beams, lower_wall=lower_wall,
        cantilevers=cantilevers, platform=platform, slip=slip,
        upper_wall=upper_wall, bottles=bottles, jutes=jutes,
        copper_pipe=copper_pipe, parasol_poles=parasol_poles, parasol=parasol,
        grass_obj=grass_obj, path_obj=path_obj,
        pillar=pillar, stair_steps=stair_steps, bench=bench, counter=counter,
        floor=floor, hearth=hearth, loft=loft,
        glass_panes=glass_panes, frames=frames, door=door,
        scenery_trunks=scenery_trunks, scenery_foliage=scenery_foliage,
        scenery_rocks=scenery_rocks,
    )

    print("[mushroom_cob_house] lights + render config")
    setup_render()

    # MUSHROOM_SKIP_RENDER=1 → build + light + place hero cam but no render.
    # Used by `blender --python ...` GUI launches so the design opens in the
    # viewport for inspection instead of rendering a still and exiting.
    if os.environ.get("MUSHROOM_SKIP_RENDER") == "1":
        setup_camera_and_lights("hero")
        print("[mushroom_cob_house] MUSHROOM_SKIP_RENDER=1 — scene built, "
              "no render. GUI session remains open.")
        return

    # MUSHROOM_VARIANTS=all → render every preset; else MUSHROOM_VARIANT (single)
    # → that one preset; default = hero. MUSHROOM_RENDER_OUT (single-variant
    # override) still wins for legacy callers.
    requested = os.environ.get("MUSHROOM_VARIANTS")
    if requested == "all":
        variants = list(CAMERA_VARIANTS.keys())
    else:
        variants = [os.environ.get("MUSHROOM_VARIANT", "hero")]

    project_root = Path(__file__).resolve().parents[1]
    out_dir = project_root / "renders" / "sub"
    out_dir.mkdir(parents=True, exist_ok=True)

    legacy_out = os.environ.get("MUSHROOM_RENDER_OUT") if len(variants) == 1 else None

    for variant in variants:
        print(f"[mushroom_cob_house] camera variant: {variant}")
        setup_camera_and_lights(variant)
        out_path = legacy_out or str(out_dir / f"mushroom_cob_house_{variant}.png")
        bpy.context.scene.render.filepath = out_path
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        print(f"[mushroom_cob_house] rendering → {out_path}")
        bpy.ops.render.render(write_still=True)

    print("[mushroom_cob_house] done.")


if __name__ == "__main__":
    main()
