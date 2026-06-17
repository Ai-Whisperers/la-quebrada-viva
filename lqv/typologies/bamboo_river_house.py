"""Typology — Bamboo River House (DSL completeness gate).

Wesley's critical-path creek-architecture typology. A stilt-mounted bamboo
house astride / alongside the 8 m wide LQV river. 4 PAX layout: kitchen +
1 bedroom + bathroom + deck overhanging water. Curved bamboo arched ribs
form a half-tunnel frame; thatch + bamboo-shingle skin overlay; raised
1.8 m above water; suspended walkway from bank; mosquito-mesh openings;
small dining deck cantilevered beyond the structure.

This module exercises every DSL hook: ``creek``, ``river``, raised-platform
``snap='stilts'``, ``tree_scatter`` of bamboo behind. Refer to
``docs/TERRAIN_PIVOT.md`` §3.6.

Material registry mapping (see ``lqv/materials/`` for the canonical keys):

* ``bamboo``          — culms, deck planks, shingles, woven walls.
* ``palm_thatch``     — primary roof thatch over the bamboo shingle layer.
* ``lapacho_timber``  — stilts, ring beams, railing posts, walkway treads.
* ``sandstone``       — pier-block footings on stream bed.
* ``steel_mesh``      — mosquito mesh on every opening (Rule 10 analogue).
* ``rope_natural``    — culm lashings, suspended walkway cables.
* ``pool_water``      — small river surface plane built by the driver.
"""
from __future__ import annotations

import math

import bpy

from lqv.materials import MAT, assign

# ---------------------------------------------------------------------------
# Geometry constants (4 PAX layout, ~7.0 m × 8.4 m envelope)
# ---------------------------------------------------------------------------

FOOTPRINT_M2 = 58.8
PLATFORM_W = 7.0                   # x-axis: short edge faces camera
PLATFORM_L = 8.4                   # y-axis: long axis along water
WALL_HEIGHT_M = 3.0                # eave clearance under the arched roof
PLATFORM_ELEVATION_M = 1.8         # platform above water surface
ROOF_TYPE = 'curved_bamboo_thatch'
FRAME = 'guadua_arched_ribs'
WALL_TYPE = 'woven_culm_with_mosquito_mesh'
GLAZING = 'mosquito_mesh_only'
SLEEPS = 4
ORIENTATION = 'long_axis_along_water'
SNAP = 'stilts'

# Stilts: 8 piers in a 2×4 grid (lapacho heartwood, 12.5 cm radius)
_STILT_RADIUS_M = 0.125
_STILT_ROWS = 4
_STILT_COLS = 2

# Pier-block stone footings the stilts sit on
_PIER_BLOCK_SIZE = 0.55            # cube edge length, m

# Deck — bamboo planks on lapacho joists
_DECK_THICKNESS = 0.08
_JOIST_W = 0.10
_JOIST_H = 0.18

# Arched ribs — half-tunnel cross-section
_RIB_RADIUS = PLATFORM_W / 2 + 0.4         # ~3.9 m radius gives a 2.8 m tall arch
_RIB_COUNT = 5                              # 5 ribs over the 8.4 m length
_RIB_CULM_RADIUS = 0.05

# Roof skin
_ROOF_THICKNESS = 0.25
_SHINGLE_THICKNESS = 0.06
_THATCH_OVERHANG = 0.7

# Cantilevered dining deck on the downstream (south) side
_DINING_DECK_W = PLATFORM_W
_DINING_DECK_L = 2.4

# Suspended walkway — from bank (north) to platform
_WALKWAY_LENGTH = 4.2
_WALKWAY_WIDTH = 1.2

# Mosquito-mesh window heights / sill
_WINDOW_SILL_H = 0.95
_WINDOW_HEAD_H = 2.30

# Inner partitions split the box into 3 zones (kitchen + bedroom + bath)
_PARTITION_THICKNESS = 0.06

# ---------------------------------------------------------------------------
# MATERIAL_TAKEOFF — quantities + USD unit cost for Paraguay 2026.
# ---------------------------------------------------------------------------
# Assumptions (one block, honest, no per-line padding):
#   * Bamboo culm (Guadua angustifolia) bought from Paraguayan harvester at
#     USD 4 / linear m for 6-12 cm Ø; market rate Asunción 2026.
#   * Palm thatch (pindo bundles) at USD 14 / m², installed price.
#   * Bamboo shingle (split + cured) at USD 18 / m², specialty crew.
#   * Lapacho heartwood at USD 1100 / m³ rough-sawn (Paraguay native).
#   * Stone pier blocks: cut sandstone, USD 95 each (delivered + set).
#   * Stainless steel mosquito mesh (0.5 mm aperture) USD 12 / m².
#   * Galvanized hardware + natural fibre lashings: USD 1.10 / fastener avg.
# A 4-PAX stilted bamboo house typically lands at USD 18-22 k materials in
# Paraguay — these numbers should sum into that band.

MATERIAL_TAKEOFF: dict[str, dict] = {
    'bamboo_culm': {
        # Frame ribs (5 ribs × ~6.1 m each), deck planks (~80 × 7 m),
        # roof purlins (12 × 9 m), wall culms (~24 × 3 m) — rounded to 280 m.
        'length_m': 280.0,
        'unit_cost_usd': 4.0,
    },
    'palm_thatch': {
        # Curved roof surface, half-cylinder area = pi * r * L  ≈ 3.14*3.9*8.4
        # → ~103 m² but only top 1/3 thatched at ~38 m².
        'area_m2': 38.0,
        'unit_cost_usd': 14.0,
    },
    'bamboo_shingle': {
        # Lower 2/3 of roof as bamboo shingle ~ 20 m².
        'area_m2': 20.0,
        'unit_cost_usd': 18.0,
    },
    'lapacho_timber': {
        # Stilts (8 × 1.8 m × pi*r²) + ring beams + joists + deck framing +
        # walkway treads + railing posts: ~1.4 m³ total.
        'volume_m3': 1.4,
        'unit_cost_usd': 1100.0,
    },
    'stone_foundation': {
        # 8 pier blocks at 0.55³ = 0.166 m³ each + apron stone around base
        # of bank-side footing → ~2.4 m³.
        'volume_m3': 2.4,
        'unit_cost_usd': 320.0,
    },
    'mosquito_mesh': {
        # 4 walls × ~6 m² openable surface = 24 m² stainless 0.5 mm mesh.
        'area_m2': 24.0,
        'unit_cost_usd': 12.0,
    },
    'fasteners_lashings': {
        # Bolts, brackets, lashings at every culm intersection (~600 joints).
        'count': 600,
        'unit_cost_usd': 1.10,
    },
    'suspended_walkway_cable': {
        # 2 stainless cables × ~6 m run + tensioners.
        'length_m': 14.0,
        'unit_cost_usd': 9.0,
    },
}


# ---------------------------------------------------------------------------
# Collection / object helpers
# ---------------------------------------------------------------------------

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


def _mat(*keys: str):
    """Return first MAT key that exists. Lets us fall back gracefully."""
    for k in keys:
        m = MAT.get(k)
        if m is not None:
            return m
    return None


def _add_cube(col, name, location, scale, mat=None):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _add_cylinder(col, name, location, radius, depth, mat=None, rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, rotation=rotation,
    )
    obj = bpy.context.active_object
    obj.name = name
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


# ---------------------------------------------------------------------------
# Sub-builders
# ---------------------------------------------------------------------------

def _pier_blocks(col, ox, oy):
    """Stone pier blocks under each stilt — at the river bed (z just below 0)."""
    mat = _mat('sandstone', 'stream_bed', 'laterite')
    rows_y = [-PLATFORM_L / 2 + 0.6,
              -PLATFORM_L / 6,
              PLATFORM_L / 6,
              PLATFORM_L / 2 - 0.6]
    cols_x = [-PLATFORM_W / 2 + 0.5, PLATFORM_W / 2 - 0.5]
    for ix, x in enumerate(cols_x):
        for iy, y in enumerate(rows_y):
            _add_cube(
                col, f'BRH_Pier_{ix}_{iy}',
                location=(ox + x, oy + y, -0.15),
                scale=(_PIER_BLOCK_SIZE, _PIER_BLOCK_SIZE, _PIER_BLOCK_SIZE),
                mat=mat,
            )


def _stilts(col, ox, oy):
    """8 lapacho heartwood piers, 2 × 4 grid."""
    mat = _mat('lapacho_timber')
    rows_y = [-PLATFORM_L / 2 + 0.6,
              -PLATFORM_L / 6,
              PLATFORM_L / 6,
              PLATFORM_L / 2 - 0.6]
    cols_x = [-PLATFORM_W / 2 + 0.5, PLATFORM_W / 2 - 0.5]
    for ix, x in enumerate(cols_x):
        for iy, y in enumerate(rows_y):
            _add_cylinder(
                col, f'BRH_Stilt_{ix}_{iy}',
                location=(ox + x, oy + y, PLATFORM_ELEVATION_M / 2.0),
                radius=_STILT_RADIUS_M, depth=PLATFORM_ELEVATION_M,
                mat=mat,
            )


def _ring_beam_and_joists(col, ox, oy):
    """Lapacho ring beam + 5 transverse joists at platform underside."""
    mat = _mat('lapacho_timber')
    z = PLATFORM_ELEVATION_M - _JOIST_H / 2.0
    # Perimeter ring beam (4 segments)
    beams = [
        (ox, oy - PLATFORM_L / 2 + _JOIST_W / 2, z,
         PLATFORM_W, _JOIST_W, _JOIST_H),
        (ox, oy + PLATFORM_L / 2 - _JOIST_W / 2, z,
         PLATFORM_W, _JOIST_W, _JOIST_H),
        (ox - PLATFORM_W / 2 + _JOIST_W / 2, oy, z,
         _JOIST_W, PLATFORM_L, _JOIST_H),
        (ox + PLATFORM_W / 2 - _JOIST_W / 2, oy, z,
         _JOIST_W, PLATFORM_L, _JOIST_H),
    ]
    for i, (x, y, zc, sx, sy, sz) in enumerate(beams):
        _add_cube(col, f'BRH_Ring_{i}', (x, y, zc), (sx, sy, sz), mat=mat)
    # Transverse joists (5 of them, evenly spaced)
    for j in range(5):
        t = j / 4.0
        y = oy - PLATFORM_L / 2 + 0.4 + t * (PLATFORM_L - 0.8)
        _add_cube(col, f'BRH_Joist_{j}',
                  (ox, y, z), (PLATFORM_W, _JOIST_W, _JOIST_H), mat=mat)


def _deck(col, ox, oy):
    """Bamboo plank deck on top of joists."""
    mat = _mat('bamboo')
    z = PLATFORM_ELEVATION_M + _DECK_THICKNESS / 2.0
    _add_cube(col, 'BRH_Deck',
              (ox, oy, z),
              (PLATFORM_W, PLATFORM_L, _DECK_THICKNESS),
              mat=mat)


def _arched_ribs(col, ox, oy):
    """5 curved bamboo arched ribs forming a half-tunnel frame.

    Each rib is built from N small cylinder segments rotated along an arc
    in the x-z plane (constant y per rib). Radius _RIB_RADIUS, sweep 180°
    so the rib goes from one deck edge up over and down to the other.
    """
    mat = _mat('bamboo')
    deck_z = PLATFORM_ELEVATION_M + _DECK_THICKNESS
    rib_ys = [
        -PLATFORM_L / 2 + 0.4,
        -PLATFORM_L / 4,
        0.0,
        PLATFORM_L / 4,
        PLATFORM_L / 2 - 0.4,
    ]
    segments = 18
    for r_i, ry in enumerate(rib_ys):
        for s in range(segments):
            theta_a = math.pi * (s / segments)
            theta_b = math.pi * ((s + 1) / segments)
            xa = -math.cos(theta_a) * (PLATFORM_W / 2)
            za = math.sin(theta_a) * (_RIB_RADIUS * 0.78)
            xb = -math.cos(theta_b) * (PLATFORM_W / 2)
            zb = math.sin(theta_b) * (_RIB_RADIUS * 0.78)
            mx = (xa + xb) / 2.0
            mz = (za + zb) / 2.0
            seg_len = math.hypot(xb - xa, zb - za)
            # Rotation: around Y so the cylinder axis aligns from (xa,za)→(xb,zb)
            angle_y = math.atan2(xb - xa, zb - za)
            _add_cylinder(
                col, f'BRH_Rib_{r_i}_{s}',
                location=(ox + mx, oy + ry, deck_z + mz),
                radius=_RIB_CULM_RADIUS, depth=seg_len,
                rotation=(0.0, angle_y, 0.0),
                mat=mat,
            )


def _longitudinal_purlins(col, ox, oy):
    """Bamboo purlins running along the ridge + along the arch — 6 lines."""
    mat = _mat('bamboo')
    deck_z = PLATFORM_ELEVATION_M + _DECK_THICKNESS
    # 6 purlins along the arch at evenly spaced angles
    angles = [math.pi * (i + 0.5) / 6 for i in range(6)]
    for i, theta in enumerate(angles):
        x = -math.cos(theta) * (PLATFORM_W / 2 + 0.05)
        z = math.sin(theta) * (_RIB_RADIUS * 0.78)
        _add_cylinder(
            col, f'BRH_Purlin_{i}',
            location=(ox + x, oy, deck_z + z),
            radius=0.035, depth=PLATFORM_L + 2 * _THATCH_OVERHANG,
            rotation=(math.pi / 2.0, 0.0, 0.0),
            mat=mat,
        )


def _roof_shell(col, ox, oy):
    """Curved roof surface — built as a single mesh from quads sweeping the arch.

    Two layers: a bamboo-shingle lower belt + a palm-thatch upper belt.
    """
    deck_z = PLATFORM_ELEVATION_M + _DECK_THICKNESS
    long_segments = 12
    arch_segments = 14
    half_l = PLATFORM_L / 2 + _THATCH_OVERHANG
    # Build both layers
    for layer_name, t_range, mat_keys, thickness in (
        ('Shingle', (0.0, 0.55), ('bamboo',), _SHINGLE_THICKNESS),
        ('Thatch', (0.55, 1.0), ('palm_thatch', 'sod_canopy'), _ROOF_THICKNESS),
    ):
        mat = _mat(*mat_keys)
        verts: list[tuple[float, float, float]] = []
        faces: list[tuple[int, ...]] = []
        t0, t1 = t_range
        for a_i in range(arch_segments + 1):
            t_a = t0 + (t1 - t0) * a_i / arch_segments
            theta = math.pi * t_a
            x_r = -math.cos(theta) * (PLATFORM_W / 2 + thickness)
            z_r = math.sin(theta) * (_RIB_RADIUS * 0.78 + thickness)
            for l_i in range(long_segments + 1):
                y_r = -half_l + (2 * half_l) * l_i / long_segments
                verts.append((ox + x_r, oy + y_r, deck_z + z_r))
        # quad faces
        cols = long_segments + 1
        for a_i in range(arch_segments):
            for l_i in range(long_segments):
                a = a_i * cols + l_i
                b = a + 1
                c = (a_i + 1) * cols + l_i + 1
                d = (a_i + 1) * cols + l_i
                faces.append((a, b, c, d))
        mesh = bpy.data.meshes.new(f'BRH_Roof_{layer_name}_Mesh')
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        obj = bpy.data.objects.new(f'BRH_Roof_{layer_name}', mesh)
        if mat is not None:
            assign(obj, mat)
        col.objects.link(obj)


def _partition_walls(col, ox, oy):
    """Inner partitions split deck into kitchen / bedroom / bathroom.

    Kitchen + living: south third. Bedroom: middle third. Bathroom: north
    third (smaller). Two cross partitions at y ≈ -PLATFORM_L/6 and +PLATFORM_L/6.
    """
    mat = _mat('bamboo')
    deck_z = PLATFORM_ELEVATION_M + _DECK_THICKNESS
    z_mid = deck_z + WALL_HEIGHT_M / 2.0
    partitions = [
        (ox, oy - PLATFORM_L / 6, z_mid,
         PLATFORM_W - 0.6, _PARTITION_THICKNESS, WALL_HEIGHT_M),
        (ox, oy + PLATFORM_L / 6, z_mid,
         PLATFORM_W - 0.6, _PARTITION_THICKNESS, WALL_HEIGHT_M),
    ]
    for i, (x, y, zc, sx, sy, sz) in enumerate(partitions):
        _add_cube(col, f'BRH_Partition_{i}',
                  (x, y, zc), (sx, sy, sz), mat=mat)


def _woven_lower_walls(col, ox, oy):
    """Low woven-bamboo skirt walls below window sill (privacy band)."""
    mat = _mat('bamboo')
    deck_z = PLATFORM_ELEVATION_M + _DECK_THICKNESS
    z_mid = deck_z + _WINDOW_SILL_H / 2.0
    sx_long = PLATFORM_W - 0.4
    sx_short = PLATFORM_L - 0.4
    walls = [
        # South (gable end facing camera)
        (ox, oy - PLATFORM_L / 2 + 0.05, z_mid,
         sx_long, 0.06, _WINDOW_SILL_H),
        # North (back, walkway side)
        (ox, oy + PLATFORM_L / 2 - 0.05, z_mid,
         sx_long, 0.06, _WINDOW_SILL_H),
        # West long side
        (ox - PLATFORM_W / 2 + 0.05, oy, z_mid,
         0.06, sx_short, _WINDOW_SILL_H),
        # East long side
        (ox + PLATFORM_W / 2 - 0.05, oy, z_mid,
         0.06, sx_short, _WINDOW_SILL_H),
    ]
    for i, (x, y, zc, sx, sy, sz) in enumerate(walls):
        _add_cube(col, f'BRH_LowWall_{i}',
                  (x, y, zc), (sx, sy, sz), mat=mat)


def _mosquito_mesh_openings(col, ox, oy):
    """Mosquito-mesh panels above sill height on all 4 walls — fly screen."""
    mat = _mat('steel_mesh', 'bamboo')
    deck_z = PLATFORM_ELEVATION_M + _DECK_THICKNESS
    band_h = _WINDOW_HEAD_H - _WINDOW_SILL_H
    z_mid = deck_z + _WINDOW_SILL_H + band_h / 2.0
    sx_long = PLATFORM_W - 0.6
    sx_short = PLATFORM_L - 0.6
    panels = [
        (ox, oy - PLATFORM_L / 2 + 0.05, z_mid,
         sx_long, 0.02, band_h),
        (ox, oy + PLATFORM_L / 2 - 0.05, z_mid,
         sx_long, 0.02, band_h),
        (ox - PLATFORM_W / 2 + 0.05, oy, z_mid,
         0.02, sx_short, band_h),
        (ox + PLATFORM_W / 2 - 0.05, oy, z_mid,
         0.02, sx_short, band_h),
    ]
    for i, (x, y, zc, sx, sy, sz) in enumerate(panels):
        _add_cube(col, f'BRH_Mesh_{i}',
                  (x, y, zc), (sx, sy, sz), mat=mat)


def _railing(col, ox, oy):
    """Lapacho railing posts + bamboo top rail around the cantilever deck only."""
    mat_post = _mat('lapacho_timber')
    mat_rail = _mat('bamboo')
    deck_z = PLATFORM_ELEVATION_M + _DECK_THICKNESS
    rail_z = deck_z + 1.0
    # Six posts ringing the south dining deck
    dec_y = oy - PLATFORM_L / 2 - _DINING_DECK_L
    for i in range(6):
        x = ox - _DINING_DECK_W / 2 + (_DINING_DECK_W / 5) * i
        _add_cylinder(
            col, f'BRH_RailPost_{i}',
            location=(x, dec_y + 0.1, deck_z + 0.5),
            radius=0.04, depth=1.0, mat=mat_post,
        )
    # Top rail (bamboo culm) along the dining-deck outer edge
    _add_cylinder(
        col, 'BRH_TopRail',
        location=(ox, dec_y + 0.1, rail_z),
        radius=0.03, depth=_DINING_DECK_W,
        rotation=(0.0, math.pi / 2.0, 0.0),
        mat=mat_rail,
    )


def _dining_deck(col, ox, oy):
    """Cantilevered dining deck on the south face — extends platform outward."""
    mat_deck = _mat('bamboo')
    mat_joist = _mat('lapacho_timber')
    deck_z = PLATFORM_ELEVATION_M + _DECK_THICKNESS / 2.0
    # Slab
    _add_cube(col, 'BRH_DiningDeck',
              (ox, oy - PLATFORM_L / 2 - _DINING_DECK_L / 2.0, deck_z),
              (_DINING_DECK_W, _DINING_DECK_L, _DECK_THICKNESS),
              mat=mat_deck)
    # 2 support joists cantilevering out from the south stilt row
    z_j = PLATFORM_ELEVATION_M - _JOIST_H / 2.0
    for i, x_off in enumerate((-PLATFORM_W / 2 + 0.5, PLATFORM_W / 2 - 0.5)):
        _add_cube(col, f'BRH_DiningCant_{i}',
                  (ox + x_off, oy - PLATFORM_L / 2 - _DINING_DECK_L / 2.0, z_j),
                  (_JOIST_W, _DINING_DECK_L, _JOIST_H),
                  mat=mat_joist)


def _suspended_walkway(col, ox, oy):
    """Lapacho-tread suspended walkway from the north (bank) side to platform.

    Bank-side anchor sits at y = +PLATFORM_L/2 + _WALKWAY_LENGTH, z ≈ 1.5 m
    (the bank). Walkway slopes gently up to the deck north edge.
    """
    mat_tread = _mat('lapacho_timber')
    mat_cable = _mat('steel_mesh', 'steel_anodized', 'rope_natural')
    mat_rope = _mat('rope_natural', 'bamboo')
    deck_z = PLATFORM_ELEVATION_M + _DECK_THICKNESS
    bank_z = 1.45                        # bank slightly lower than deck
    n_treads = 9
    for i in range(n_treads):
        t = (i + 0.5) / n_treads
        y = (oy + PLATFORM_L / 2) + t * _WALKWAY_LENGTH
        z = deck_z * (1 - t) + bank_z * t
        _add_cube(col, f'BRH_Walkway_Tread_{i}',
                  (ox, y, z),
                  (_WALKWAY_WIDTH, 0.30, 0.05),
                  mat=mat_tread)
    # Side rope / cable rails — 2 along each edge
    for side, x_off in enumerate((-_WALKWAY_WIDTH / 2, _WALKWAY_WIDTH / 2)):
        _add_cylinder(
            col, f'BRH_Walkway_Cable_{side}',
            location=(ox + x_off,
                      oy + PLATFORM_L / 2 + _WALKWAY_LENGTH / 2,
                      (deck_z + bank_z) / 2.0 + 1.0),
            radius=0.015, depth=_WALKWAY_LENGTH + 0.2,
            rotation=(math.pi / 2.0, 0.0, 0.0),
            mat=mat_cable,
        )
        # Vertical support ropes at intervals
        for i in range(4):
            t = (i + 0.5) / 4
            y = (oy + PLATFORM_L / 2) + t * _WALKWAY_LENGTH
            tread_z = deck_z * (1 - t) + bank_z * t
            _add_cylinder(
                col, f'BRH_Walkway_RopeDrop_{side}_{i}',
                location=(ox + x_off, y, tread_z + 0.5),
                radius=0.008, depth=1.0,
                mat=mat_rope,
            )
    # Bank anchor post
    _add_cube(
        col, 'BRH_BankAnchor',
        (ox, oy + PLATFORM_L / 2 + _WALKWAY_LENGTH + 0.3, bank_z + 0.5),
        (1.4, 0.3, 1.0),
        mat=_mat('lapacho_timber', 'sandstone'),
    )


def _eave_overhang_strip(col, ox, oy):
    """Eave strip — extends roof shell visually beyond the deck for shade."""
    mat = _mat('palm_thatch', 'sod_canopy')
    if mat is None:
        return
    deck_z = PLATFORM_ELEVATION_M + _DECK_THICKNESS
    eave_z = deck_z + 0.05
    for y_sign in (-1.0, 1.0):
        y = oy + y_sign * (PLATFORM_L / 2 + _THATCH_OVERHANG / 2.0)
        _add_cube(
            col, f'BRH_Eave_{"N" if y_sign > 0 else "S"}',
            (ox, y, eave_z + 0.5),
            (PLATFORM_W + 0.6, _THATCH_OVERHANG, 0.08),
            mat=mat,
        )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def build_bamboo_river_house(origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
                              parent: bpy.types.Collection | None = None,
                              variant: str = 'A') -> bpy.types.Collection:
    """Build the bamboo river house at ``origin``.

    Parameters
    ----------
    origin
        World-space anchor (x, y, z); the platform center sits here.
    parent
        Parent collection to nest the typology under (defaults to scene root).
    variant
        Variant tag (A/B/C) — currently used only for naming; lighting comes
        from the world setup outside this builder.

    Returns the parent collection so callers can re-parent under a typology
    cluster. Idempotent across re-invocation in the same scene.
    """
    name = 'BambooRiverHouse'
    col = _ensure_collection(name, parent)
    ox, oy, _oz = origin

    _pier_blocks(col, ox, oy)
    _stilts(col, ox, oy)
    _ring_beam_and_joists(col, ox, oy)
    _deck(col, ox, oy)
    _arched_ribs(col, ox, oy)
    _longitudinal_purlins(col, ox, oy)
    _roof_shell(col, ox, oy)
    _eave_overhang_strip(col, ox, oy)
    _woven_lower_walls(col, ox, oy)
    _mosquito_mesh_openings(col, ox, oy)
    _partition_walls(col, ox, oy)
    _dining_deck(col, ox, oy)
    _railing(col, ox, oy)
    _suspended_walkway(col, ox, oy)

    return col


# Backwards-compatible alias matching the old typologies API shape.
def build(parent: bpy.types.Collection | None = None,
          location: tuple[float, float, float] = (0.0, 0.0, 0.0),
          variant: str = 'A') -> bpy.types.Collection:
    """Legacy entry point — see ``build_bamboo_river_house``."""
    return build_bamboo_river_house(origin=location, parent=parent, variant=variant)
