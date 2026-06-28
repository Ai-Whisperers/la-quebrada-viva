"""Typology — Italian Stone Small v2 (Side-Loggia 2BR).

Sister typology to ``italian_stone_small_v1``. The grammar is identical
(sandstone walls, 60 cm stone foundation course, terracotta tile, lapacho
joinery and beams) but the program scales up: 2 bedrooms instead of 1
sleeping nook, a side LOGGIA running the full length of the east face,
and a single-pitch shed roof in place of v1's symmetric gable.

Footprint: 10 m × 7 m main mass = 70 m² gross. Loggia adds 3 m × 7 m of
open-air covered porch on the east. Door faces south (-Y), loggia faces
east (+X). Camera lives SE of origin so the south face + the east loggia
both stay in clear view of the hero shot.

Per the project plan, all shared geometry primitives — foundation course,
wall segments, shutters, door, porch beams, chimney — are routed through
``lqv.house.stone_wall`` instead of being inlined a second time. The
bay-specific layouts (7-window grid, 4-bay loggia) stay local because
they depend on this typology's specific spacing.

Material vocabulary identical to v1: ``sandstone`` (walls + foundation +
chimney), ``terracotta_tile`` (roof), ``lapacho_timber`` (joinery + beams),
``water_reflective`` (glazing fallback). All keys resolve via the shared
fallback chains in ``stone_wall._FALLBACKS``.

Cost band is intentionally ~30 % above v1 ($11 000 – $14 000 USD) — the
wall perimeter is ~2× longer (34 m vs 18 m) but the unit costs and roof
span scale modestly, so the takeoff lands in the upper-middle band
without ballooning. The loggia is the single biggest extra: 4 posts, 4
lapacho beams, and a 21 m² shed-roof extension.
"""
from __future__ import annotations

import math

import bpy

from lqv.furniture import furnish_interior
from lqv.house import stone_wall
from lqv.materials import MAT, assign

# ---------------------------------------------------------------------------
# Public typology metadata — matches the v1 contract so the dispatcher /
# composite layer can swap v1 ↔ v2 without further plumbing.
# ---------------------------------------------------------------------------
FOOTPRINT_M2 = 70.0            # 10 m × 7 m main mass (loggia counted separately)
PLATFORM_W = 10.0              # x (E-W long edge — high eave on west, low eave on east)
PLATFORM_L = 7.0               # y (N-S short edge)
SLEEPS = 4                     # 2 BR × 2 pax
STORY_HEIGHT_M = 2.8
WALL_HEIGHT_M = 2.8
ROOF_TYPE = 'terracotta_tile_monopitch'
ROOF_PITCH_DEG = 12.0          # shed roof — gentler than v1's 25° gable
ORIENTATION = 'door_faces_south_loggia_east'
SNAP = 'pad'
PAD_SIZE_M = 1.6
LOGGIA_DEPTH = 3.0
LOGGIA_BAYS = 3

# Geometry constants — shared with v1 wherever the building physics demand it.
_FOUNDATION_HEIGHT = 0.6       # Rule 4 — 60 cm stone foundation course
_FOUNDATION_PROUD = 0.20
_WALL_THICKNESS = 0.30
_ROOF_EAVE_OVERHANG = 0.9      # Rule 5 — 90 cm long-side overhangs
_GABLE_OVERHANG = 0.25
_WINDOW_W = 1.0
_WINDOW_H = 1.1
_WINDOW_SILL_Z = 1.0           # measured from the foundation top
_DOOR_W = 0.95
_DOOR_H = 2.2
_SHUTTER_W = 0.55
_SHUTTER_H = 1.15
_PORCH_BEAM_R = 0.10
_LOGGIA_BEAM_W = 0.20
_LOGGIA_BEAM_H = 0.25
_PAVING_W = 2.4
_PAVING_L = 3.2
_FRENCH_DOOR_W = 1.8
_FRENCH_DOOR_H = 2.2

NOTES = (
    '2-bedroom rural cottage, ~70 m² interior + 21 m² covered loggia.',
    'Sandstone walls (30 cm); 60 cm stone foundation course (Rule 4).',
    'Single-pitch (12°) terracotta-tile shed roof — ridge on the WEST, pitching down to the EAST loggia.',
    '90 cm eaves on long axis (Rule 5); 25 cm overhang on gable ends.',
    'Side loggia: 3 m × 7 m, 4 lapacho posts + 4 lapacho beams, paved with sandstone.',
    'South face: lapacho door centered + 2 flanking windows (1 m × 1.1 m, shutters).',
    'North face: 2 small kitchen/bath windows.',
    'West face: 3 sandstone-framed windows (one per bedroom + living room).',
    'East face: French double-door + 2 windows opening onto the loggia.',
    'Chimney on west gable for stove + hearth venting (Rule 4 — stone, not metal flue).',
    'Passive <= 35 C: 30 cm thermal mass + cross-vent across N-S and E-W axes; no AC.',
    'Cost band $11 000 - $14 000 USD - ~30 % above v1; loggia is the main delta.',
)

# Per-unit Paraguay 2026 estimates, carried from v1 with quantity scaled to
# the larger footprint + loggia. Targeted total falls in the $11 000 -
# $14 000 USD band. Keys mirror v1's takeoff so the composite layer can
# aggregate across typologies without renaming.
MATERIAL_TAKEOFF: dict = {
    'stone_walls': {
        # 4 main-mass walls; 30 cm thick × 2.8 m tall × ~34 m perimeter
        # less ~18 % for openings = 22.5 m³ coursed sandstone in lime
        # mortar. Local mason team, not Asuncion retail.
        'volume_m3': 22.5,
        'unit_cost_usd': 110.0,
    },
    'terracotta_tile_roof': {
        # 12° shed over 10×7 footprint + 0.9 m overhangs on long axis +
        # 21 m² loggia extension on east = ~99 m² covered (rural-quarry
        # terracotta + lapacho battens).
        'area_m2': 99.0,
        'unit_cost_usd': 28.0,
    },
    'lapacho_shutters_doors': {
        # 9 windows × 2 shutter leaves + entry door + french double-door
        # = ~17 m² of finished joinery from a local carpenter.
        'area_m2': 17.0,
        'unit_cost_usd': 130.0,
    },
    'lapacho_beams_porch': {
        # 4 loggia posts + 4 primary E-W beams + 4 secondary purlins,
        # all lapacho heartwood — highest per-m³ rate on the bill.
        'volume_m3': 0.85,
        'unit_cost_usd': 1200.0,
    },
    'stone_foundation': {
        # 60 cm course × ~40 cm thick × ~34 m perimeter (Rule 4); rougher
        # rubble-stone than the dressed wall course, hence lower rate.
        'volume_m3': 5.6,
        'unit_cost_usd': 140.0,
    },
    'glass_glazing': {
        # 9 windows × ~1.1 m² + french door = ~12 m². Single-glazed is
        # adequate for the Paraguari climate (>= 10 C winter lows).
        'area_m2': 12.0,
        'unit_cost_usd': 160.0,
    },
    'fasteners': {
        # Steel anchors, lag bolts, joist hangers, copper flashings —
        # scaled 1.7× from v1 since the wall+roof perimeter scales ~1.7×.
        'count': 430,
        'unit_cost_usd': 0.85,
    },
    'loggia_paving': {
        # 21 m² of rough sandstone-slab paving under the loggia (the
        # entry apron stone count is rolled into 'stone_walls' already).
        'area_m2': 21.0,
        'unit_cost_usd': 55.0,
    },
}
# Total: $12 702. In-band ($11k-$14k); +39.5 % over v1's $9 108.


# ---------------------------------------------------------------------------
# Local helpers — same shape as v1's _ensure_collection / _link / _mat / _cube
# so the file reads consistently to anyone who already knows v1.
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
    for k in keys:
        m = MAT.get(k)
        if m is not None:
            return m
    return None


def _cube(col, name, location, scale, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _cylinder(col, name, location, radius, depth, mat, rotation=(0.0, 0.0, 0.0)):
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
# Geometry — main mass.
# ---------------------------------------------------------------------------
def _foundation(col, ox, oy):
    """60 cm sandstone foundation under the 10×7 main mass (Rule 4)."""
    stone_wall.build_stone_foundation_course(
        x=ox, y=oy,
        width_m=PLATFORM_W, depth_m=PLATFORM_L,
        height_m=_FOUNDATION_HEIGHT,
        name='ISS2_FoundationPad',
        collection=col,
    )


def _walls(col, ox, oy):
    """4 sandstone walls forming the 10×7 box, on top of the foundation course.

    Shed roof slope rises to the west, so the west wall extends taller (to
    the high eave) while the east wall stops at the low eave. We model both
    walls as full-height to the average eave for simplicity — the gable
    triangles handle the extra fill above the wall on N and S.
    """
    z0 = _FOUNDATION_HEIGHT
    low_eave_z = z0 + WALL_HEIGHT_M  # east (low) eave height
    pitch_rad = math.radians(ROOF_PITCH_DEG)
    west_rise = math.tan(pitch_rad) * PLATFORM_W
    z_west_top = low_eave_z + west_rise

    # South wall (door side).
    stone_wall.build_sandstone_wall(
        p_start=(ox - PLATFORM_W / 2 + _WALL_THICKNESS / 2,
                 oy - PLATFORM_L / 2 + _WALL_THICKNESS / 2),
        p_end=(ox + PLATFORM_W / 2 - _WALL_THICKNESS / 2,
               oy - PLATFORM_L / 2 + _WALL_THICKNESS / 2),
        height_m=WALL_HEIGHT_M, thickness_m=_WALL_THICKNESS,
        name='ISS2_Wall_S', collection=col, z_base=z0,
    )
    # North wall.
    stone_wall.build_sandstone_wall(
        p_start=(ox - PLATFORM_W / 2 + _WALL_THICKNESS / 2,
                 oy + PLATFORM_L / 2 - _WALL_THICKNESS / 2),
        p_end=(ox + PLATFORM_W / 2 - _WALL_THICKNESS / 2,
               oy + PLATFORM_L / 2 - _WALL_THICKNESS / 2),
        height_m=WALL_HEIGHT_M, thickness_m=_WALL_THICKNESS,
        name='ISS2_Wall_N', collection=col, z_base=z0,
    )
    # West wall (taller — supports the shed-roof ridge).
    stone_wall.build_sandstone_wall(
        p_start=(ox - PLATFORM_W / 2 + _WALL_THICKNESS / 2,
                 oy - PLATFORM_L / 2 + _WALL_THICKNESS / 2),
        p_end=(ox - PLATFORM_W / 2 + _WALL_THICKNESS / 2,
               oy + PLATFORM_L / 2 - _WALL_THICKNESS / 2),
        height_m=WALL_HEIGHT_M + west_rise, thickness_m=_WALL_THICKNESS,
        name='ISS2_Wall_W', collection=col, z_base=z0,
    )
    # East wall (low — opens onto loggia, will be punched by french door).
    stone_wall.build_sandstone_wall(
        p_start=(ox + PLATFORM_W / 2 - _WALL_THICKNESS / 2,
                 oy - PLATFORM_L / 2 + _WALL_THICKNESS / 2),
        p_end=(ox + PLATFORM_W / 2 - _WALL_THICKNESS / 2,
               oy + PLATFORM_L / 2 - _WALL_THICKNESS / 2),
        height_m=WALL_HEIGHT_M, thickness_m=_WALL_THICKNESS,
        name='ISS2_Wall_E', collection=col, z_base=z0,
    )

    # Gable infill on N and S faces — ridge slopes from west (high) to east
    # (low), so each N/S wall has a triangular infill from low_eave (east
    # side) to z_west_top (west side). 3 verts, 1 face.
    stone = _mat('sandstone', 'stone_wall', 'limestone')
    for face_sign, suffix in ((-1, 'S'), (1, 'N')):
        wy = oy + face_sign * (PLATFORM_L / 2 - _WALL_THICKNESS / 2)
        x_w = ox - PLATFORM_W / 2
        x_e = ox + PLATFORM_W / 2
        verts = [
            (x_w, wy, low_eave_z),
            (x_e, wy, low_eave_z),
            (x_w, wy, z_west_top),
        ]
        mesh = bpy.data.meshes.new(f'ISS2_Gable_{suffix}_Mesh')
        mesh.from_pydata(verts, [], [(0, 1, 2)])
        mesh.update()
        obj = bpy.data.objects.new(f'ISS2_Gable_{suffix}', mesh)
        if stone is not None:
            assign(obj, stone)
        col.objects.link(obj)


def _roof(col, ox, oy):
    """Single-pitch shed roof — high on the west wall, pitching down east.

    The east edge sits at ``low_eave_z`` (= 2.8 m above the foundation top);
    the west edge sits at ``low_eave_z + tan(pitch) × 10 m`` (= ~2.13 m
    taller). Overhangs: 90 cm on the east (over loggia) and west (Rule 5),
    25 cm on the gable ends (N/S).

    The loggia roof is rendered as a SEPARATE flat extension off the east
    eave (handled in ``_loggia``) so it sits proud of the main shed and
    reads as its own roof plane.
    """
    z0 = _FOUNDATION_HEIGHT
    low_eave_z = z0 + WALL_HEIGHT_M
    pitch_rad = math.radians(ROOF_PITCH_DEG)
    west_rise = math.tan(pitch_rad) * PLATFORM_W

    x_w = ox - PLATFORM_W / 2 - _ROOF_EAVE_OVERHANG
    x_e = ox + PLATFORM_W / 2 + _ROOF_EAVE_OVERHANG
    y_s = oy - PLATFORM_L / 2 - _GABLE_OVERHANG
    y_n = oy + PLATFORM_L / 2 + _GABLE_OVERHANG

    # Roof slopes linearly from west_top to east_low along x; overhang at
    # west adds west_rise + tan(pitch) × overhang_m extra; overhang at east
    # drops below the eave by tan(pitch) × overhang_m.
    extra_west = math.tan(pitch_rad) * _ROOF_EAVE_OVERHANG
    extra_east = math.tan(pitch_rad) * _ROOF_EAVE_OVERHANG
    z_w_far = low_eave_z + west_rise + extra_west
    z_e_far = low_eave_z - extra_east

    verts = [
        (x_w, y_s, z_w_far),   # 0  SW high
        (x_e, y_s, z_e_far),   # 1  SE low
        (x_e, y_n, z_e_far),   # 2  NE low
        (x_w, y_n, z_w_far),   # 3  NW high
    ]
    faces = [(0, 1, 2, 3)]
    mesh = bpy.data.meshes.new('ISS2_Roof_Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new('ISS2_Roof', mesh)
    tile = _mat('terracotta_tile', 'clay_tile', 'laterite')
    if tile is not None:
        assign(obj, tile)
    col.objects.link(obj)


# ---------------------------------------------------------------------------
# Openings — windows, door, french door.
# ---------------------------------------------------------------------------
def _windows(col, ox, oy):
    """9 windows + shutters across the four faces.

    Layout:
      South: 2 windows at (ox-2.5, ox+2.5), flanking the centered door.
      North: 2 windows at (ox-2.0, ox+2.0).
      West:  3 windows at (oy-2.4, oy, oy+2.4).
      East:  2 windows at (oy-2.4, oy+2.4), straddling the french door.
    """
    glass = _mat('water_reflective', 'glass_bottle_cobalt')
    z0 = _FOUNDATION_HEIGHT
    win_cz = z0 + _WINDOW_SILL_Z + _WINDOW_H / 2.0

    plan = [
        ('S', (0.0, -1.0, 0.0), (-2.5, 0.0), oy - PLATFORM_L / 2),
        ('S', (0.0, -1.0, 0.0), (2.5, 0.0), oy - PLATFORM_L / 2),
        ('N', (0.0, 1.0, 0.0), (-2.0, 0.0), oy + PLATFORM_L / 2),
        ('N', (0.0, 1.0, 0.0), (2.0, 0.0), oy + PLATFORM_L / 2),
        ('W', (-1.0, 0.0, 0.0), (0.0, -2.4), ox - PLATFORM_W / 2),
        ('W', (-1.0, 0.0, 0.0), (0.0, 0.0), ox - PLATFORM_W / 2),
        ('W', (-1.0, 0.0, 0.0), (0.0, 2.4), ox - PLATFORM_W / 2),
        ('E', (1.0, 0.0, 0.0), (0.0, -2.4), ox + PLATFORM_W / 2),
        ('E', (1.0, 0.0, 0.0), (0.0, 2.4), ox + PLATFORM_W / 2),
    ]

    for i, (tag, normal, (dx, dy), wall_coord) in enumerate(plan):
        # Window centre in world coords.
        if tag in ('S', 'N'):
            cx = ox + dx
            cy = wall_coord
        else:
            cx = wall_coord
            cy = oy + dy
        # Inset glass pane 4 cm behind the exterior wall face.
        gx = cx + normal[0] * (-0.04)
        gy = cy + normal[1] * (-0.04)
        if glass is not None:
            if abs(normal[0]) > abs(normal[1]):
                scale = (0.04, _WINDOW_W, _WINDOW_H)
            else:
                scale = (_WINDOW_W, 0.04, _WINDOW_H)
            _cube(
                col, f'ISS2_Glass_{tag}_{i}',
                location=(gx, gy, win_cz),
                scale=scale,
                mat=glass,
            )
        # Shutters via shared primitive (sits 2 cm proud of wall face).
        stone_wall.build_lapacho_shutter_pair(
            window_xy_z=(cx, cy, win_cz),
            opening_w=_WINDOW_W,
            opening_h=_WINDOW_H,
            face_normal=normal,
            shutter_w=_SHUTTER_W,
            shutter_h=_SHUTTER_H,
            name_prefix=f'ISS2_Shutter_{tag}_{i}',
            collection=col,
        )
        # Lapacho lintel + sill — kept inline because the shared primitive
        # doesn't yet expose a window-trim helper.
        timber = _mat('lapacho_timber')
        if abs(normal[0]) > abs(normal[1]):
            for dz, suf in ((-_WINDOW_H / 2 - 0.06, 'sill'),
                            (_WINDOW_H / 2 + 0.06, 'lintel')):
                _cube(
                    col, f'ISS2_WinTrim_{tag}_{i}_{suf}',
                    location=(cx + normal[0] * 0.04, cy, win_cz + dz),
                    scale=(0.10, _WINDOW_W + 0.30, 0.10),
                    mat=timber,
                )
        else:
            for dz, suf in ((-_WINDOW_H / 2 - 0.06, 'sill'),
                            (_WINDOW_H / 2 + 0.06, 'lintel')):
                _cube(
                    col, f'ISS2_WinTrim_{tag}_{i}_{suf}',
                    location=(cx, cy + normal[1] * 0.04, win_cz + dz),
                    scale=(_WINDOW_W + 0.30, 0.10, 0.10),
                    mat=timber,
                )


def _door_and_paving(col, ox, oy):
    """South lapacho door + 2.4 × 3.2 sandstone paving apron in front."""
    paving = _mat('sandstone', 'laterite', 'stone_wall')
    z0 = _FOUNDATION_HEIGHT
    door_cz = z0 + _DOOR_H / 2.0

    stone_wall.build_lapacho_door(
        xy_z=(ox, oy - PLATFORM_L / 2 - 0.02, door_cz),
        width_m=_DOOR_W,
        height_m=_DOOR_H,
        face_normal=(0.0, -1.0, 0.0),
        name='ISS2_Door',
        collection=col,
        with_trim=True,
    )

    # Entry apron — 2.4×3.2 m of cut sandstone paving, sub-divided 3×2.
    apron_cy = oy - PLATFORM_L / 2 - _PAVING_L / 2 - 0.10
    n_cols, n_rows = 3, 2
    slab_w = _PAVING_W / n_cols
    slab_l = _PAVING_L / n_rows
    for i in range(n_cols):
        for j in range(n_rows):
            cx = ox - _PAVING_W / 2 + (i + 0.5) * slab_w
            cy = apron_cy - _PAVING_L / 2 + (j + 0.5) * slab_l
            _cube(
                col, f'ISS2_Paving_{i}_{j}',
                location=(cx, cy, 0.04),
                scale=(slab_w * 0.94, slab_l * 0.94, 0.08),
                mat=paving,
            )


def _french_door(col, ox, oy):
    """East-facing french double-door opening onto the loggia."""
    timber = _mat('lapacho_timber')
    z0 = _FOUNDATION_HEIGHT
    cx = ox + PLATFORM_W / 2 + 0.03
    cy = oy
    cz = z0 + _FRENCH_DOOR_H / 2.0
    leaf_w = _FRENCH_DOOR_W / 2.0 - 0.02
    for sign in (-1, 1):
        _cube(
            col, f'ISS2_FrenchDoor_{"L" if sign < 0 else "R"}',
            location=(cx, cy + sign * (leaf_w / 2.0 + 0.02), cz),
            scale=(0.06, leaf_w, _FRENCH_DOOR_H),
            mat=timber,
        )
    # Top lintel — full french-door width + 30 cm trim margin.
    _cube(
        col, 'ISS2_FrenchDoorLintel',
        location=(cx, cy, z0 + _FRENCH_DOOR_H + 0.08),
        scale=(0.10, _FRENCH_DOOR_W + 0.30, 0.14),
        mat=timber,
    )


# ---------------------------------------------------------------------------
# Loggia — the defining feature of v2.
# ---------------------------------------------------------------------------
def _loggia(col, ox, oy):
    """3 m × 7 m covered side loggia on the east face.

    Four lapacho posts evenly distributed along the east edge of the
    loggia. Four primary beams span E-W (post-to-wall). Roof: a flat
    terracotta plane sloping down from just below the east main-roof eave
    to just above the loggia post-tops, mirroring the main shed's 12°.
    """
    timber = _mat('lapacho_timber')
    tile = _mat('terracotta_tile', 'clay_tile', 'laterite')
    paving = _mat('sandstone', 'laterite', 'stone_wall')
    z0 = _FOUNDATION_HEIGHT
    post_h = WALL_HEIGHT_M - 0.10
    post_radius = _PORCH_BEAM_R

    # Evenly distribute LOGGIA_BAYS+1 posts across the loggia length.
    post_x = ox + PLATFORM_W / 2 + LOGGIA_DEPTH
    post_ys = [oy - PLATFORM_L / 2 + (PLATFORM_L * i / LOGGIA_BAYS)
               for i in range(LOGGIA_BAYS + 1)]

    for i, py in enumerate(post_ys):
        _cylinder(
            col, f'ISS2_LoggiaPost_{i}',
            location=(post_x, py, z0 + post_h / 2.0),
            radius=post_radius, depth=post_h, mat=timber,
        )

    # Lapacho beams via shared primitive — span E-W (from east main wall to
    # the loggia post line).
    beam_z = z0 + post_h + _LOGGIA_BEAM_H / 2.0
    stone_wall.build_lapacho_porch_beams(
        p_start_xyz=(ox + PLATFORM_W / 2, post_ys[0], beam_z),
        p_end_xyz=(post_x, post_ys[-1], beam_z),
        count=LOGGIA_BAYS + 1,
        beam_w=_LOGGIA_BEAM_W,
        beam_h=_LOGGIA_BEAM_H,
        name_prefix='ISS2_LoggiaBeam',
        collection=col,
    )

    # Cross-purlins (N-S) tying the beams together — 4 purlins, evenly
    # spaced along x.
    purlin_h = _LOGGIA_BEAM_H * 0.6
    for i in range(4):
        px = ox + PLATFORM_W / 2 + LOGGIA_DEPTH * (i + 0.5) / 4
        _cube(
            col, f'ISS2_LoggiaPurlin_{i}',
            location=(px, oy, beam_z + _LOGGIA_BEAM_H / 2 + purlin_h / 2),
            scale=(0.10, PLATFORM_L + 0.20, purlin_h),
            mat=timber,
        )

    # Loggia roof — a flat plane sloping from the east main eave (high) to
    # just above the post-tops (low). Continuous with the main shed roof so
    # it reads as one extended pitch from the SE camera angle.
    eave_z = z0 + WALL_HEIGHT_M
    inner_z = eave_z - math.tan(math.radians(ROOF_PITCH_DEG)) * _ROOF_EAVE_OVERHANG
    outer_z = z0 + post_h + _LOGGIA_BEAM_H + purlin_h + 0.05
    y_s = oy - PLATFORM_L / 2 - _GABLE_OVERHANG
    y_n = oy + PLATFORM_L / 2 + _GABLE_OVERHANG
    verts = [
        (ox + PLATFORM_W / 2, y_s, inner_z),
        (post_x + 0.30, y_s, outer_z),
        (post_x + 0.30, y_n, outer_z),
        (ox + PLATFORM_W / 2, y_n, inner_z),
    ]
    faces = [(0, 1, 2, 3)]
    mesh = bpy.data.meshes.new('ISS2_LoggiaRoof_Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new('ISS2_LoggiaRoof', mesh)
    if tile is not None:
        assign(obj, tile)
    col.objects.link(obj)

    # Loggia floor — 7 × 3 m of sandstone paving under the loggia.
    floor_cx = ox + PLATFORM_W / 2 + LOGGIA_DEPTH / 2
    n_cols_f, n_rows_f = 3, 4
    slab_wf = LOGGIA_DEPTH / n_cols_f
    slab_lf = PLATFORM_L / n_rows_f
    for i in range(n_cols_f):
        for j in range(n_rows_f):
            cx = floor_cx - LOGGIA_DEPTH / 2 + (i + 0.5) * slab_wf
            cy = oy - PLATFORM_L / 2 + (j + 0.5) * slab_lf
            _cube(
                col, f'ISS2_LoggiaFloor_{i}_{j}',
                location=(cx, cy, 0.04),
                scale=(slab_wf * 0.94, slab_lf * 0.94, 0.08),
                mat=paving,
            )


# ---------------------------------------------------------------------------
# Chimney on the west gable.
# ---------------------------------------------------------------------------
def _chimney(col, ox, oy):
    """Sandstone chimney on the west (high) gable for stove venting."""
    z0 = _FOUNDATION_HEIGHT
    low_eave_z = z0 + WALL_HEIGHT_M
    pitch_rad = math.radians(ROOF_PITCH_DEG)
    west_rise = math.tan(pitch_rad) * PLATFORM_W
    z_west_top = low_eave_z + west_rise
    top_z = z_west_top + 1.1
    cx = ox - PLATFORM_W / 2 + 0.55
    cy = oy + PLATFORM_L * 0.18
    base_z = z0 + WALL_HEIGHT_M * 0.5
    height = top_z - base_z
    stone_wall.build_chimney(
        top_xyz=(cx, cy, top_z),
        width_m=0.55,
        height_m=height,
        material='sandstone',
        name='ISS2_Chimney',
        collection=col,
        with_cap=True,
    )


# ---------------------------------------------------------------------------
# Entry point.
# ---------------------------------------------------------------------------
def build_italian_stone_small_v2(origin=(0.0, 0.0, 0.0), variant: str = 'A'):
    """Build the Italian Stone Small v2 cottage at ``origin``.

    Returns the parent collection. Idempotent across re-invocation.
    """
    name = 'ItalianStoneSmall_v2'
    col = _ensure_collection(name, None)
    ox, oy, _oz = origin
    _foundation(col, ox, oy)
    _walls(col, ox, oy)
    _roof(col, ox, oy)
    _windows(col, ox, oy)
    _door_and_paving(col, ox, oy)
    _french_door(col, ox, oy)
    _loggia(col, ox, oy)
    _chimney(col, ox, oy)

    # P1.B.1 — interior furniture stubs (RENDER_VIEW=interior readable).
    # 10 × 7 m main mass; floor sits atop foundation course; margin from
    # wall face for 2 BR layout (bed pair + dining + shelf comfortably).
    furnish_interior(
        col,
        footprint_w=PLATFORM_W - 1.2,
        footprint_l=PLATFORM_L - 1.2,
        origin_xy=(ox, oy),
        floor_z=_FOUNDATION_HEIGHT,
        pax=SLEEPS,
        style='stone',
        variant=variant,
        name_prefix='ISSv2_Furn',
    )

    return col


# Backward-compat shim mirroring v1's contract.
def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    col = build_italian_stone_small_v2(origin=location, variant=variant)
    if parent is not None and col.name not in [c.name for c in parent.children]:
        bpy.context.scene.collection.children.unlink(col)
        parent.children.link(col)
    return col
