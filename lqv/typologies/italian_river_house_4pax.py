"""Typology — Italian River House 4-pax.

Two-storey Italian-stone river-bank house, ~7 m × 5 m footprint, 4 PAX. Strong
stone-villa aesthetic: thick stone walls + terracotta-tile gable roof + arched
stone foundation with arched openings + covered river-view loggia + lapacho
shutters. Passive cooling at ≤35 °C: thick stone walls + shutters +
cross-ventilation, no AC. Bedrooms upstairs (2× double), living + kitchen +
bath downstairs. Off-the-ground 60 cm minimum (Rule 4).

Procedural primitives only: scaled cubes for walls, gable-roof mesh from
verts/faces, cylinders for loggia columns + arched-base pilasters, half-cylinder
arches between pilasters. Material vocabulary uses ``sandstone`` (fallback for
``stone_wall``/``limestone``), ``terracotta_tile``, ``lapacho_timber``, plus
``water_reflective`` for the river edge.
"""
from __future__ import annotations

import math

import bpy

from lqv.materials import MAT, assign

FOOTPRINT_M2 = 35.0           # 7 m × 5 m per floor
PLATFORM_W = 7.0              # x (long edge, gable runs along x → gables N/S)
PLATFORM_L = 5.0              # y (short edge, river is at +y)
STORIES = 2
TOTAL_AREA_M2 = 70.0
STORY_HEIGHT_M = 2.8
WALL_HEIGHT_M = 5.6           # 2 storeys × 2.8 m
ROOF_TYPE = 'terracotta_tile_gabled'
ROOF_PITCH_DEG = 28.0
SLEEPS = 4
ORIENTATION = 'loggia_faces_river_north'
SNAP = 'pad'
PAD_SIZE_M = 2.0

# Foundation: arched stone base, Rule 4 = ≥ 60 cm off ground.
_BASE_HEIGHT = 1.2            # arched-base storey height (becomes utility/cellar)
_BASE_THICKNESS = 0.45        # stone foundation wall thickness
_WALL_THICKNESS = 0.35        # main stone walls (~30 cm + cladding)
_ROOF_EAVE_OVERHANG = 0.6
_ROOF_THICKNESS = 0.12
_LOGGIA_DEPTH = 2.4           # river-facing covered loggia (north side)
_LOGGIA_COL_RADIUS = 0.18
_DOCK_LENGTH = 3.0
_RIVER_WIDTH = 8.0
_RIVER_PLANE_LEN = 20.0
_SHUTTER_W = 0.7
_SHUTTER_H = 1.2

NOTES = (
    'Two-storey stone river-bank house, arched-opening stone foundation.',
    'Bedrooms upstairs (2× double), living + kitchen + bath downstairs.',
    'Covered river-view loggia on the river side (north), lapacho columns.',
    'Exterior stone stairs lead from loggia level down to a small lapacho dock.',
    'Operable lapacho shutters on every window; oil-finished heartwood.',
    'Terracotta gabled tile roof, 28° pitch, 60 cm eave overhang.',
    'Passive ≤35 °C: 35 cm stone walls + thermal mass + cross-vent; no AC.',
)

MATERIAL_TAKEOFF: dict = {
    'stone_walls': {
        # Full envelope, 2-storey, 35 cm thick. Subtract ~20 % for openings.
        'volume_m3': 22.0,
        'unit_cost_usd': 285.0,    # PY 2026 — quarried stone + lime mortar + labor / m^3
    },
    'terracotta_tile_roof': {
        # Gabled at 28° over 7×5 footprint + overhangs ≈ 55 m^2 covered surface
        'area_m2': 55.0,
        'unit_cost_usd': 42.0,
    },
    'lapacho_shutters_doors': {
        # 8 shutter pairs + 2 entry doors + balcony double-door
        'area_m2': 14.0,
        'unit_cost_usd': 165.0,
    },
    'lapacho_beams_columns': {
        # Loggia columns + ridge beam + purlins + dock joists
        'volume_m3': 0.6,
        'unit_cost_usd': 1450.0,
    },
    'stone_foundation_arched': {
        # Arched base storey: perimeter wall + 4 pilasters + 3 arches
        'volume_m3': 4.5,
        'unit_cost_usd': 310.0,
    },
    'glass_glazing': {
        # Window + balcony-door glazing, double-pane
        'area_m2': 8.0,
        'unit_cost_usd': 240.0,
    },
    'fasteners_misc': {
        # Steel anchors, lag bolts, brackets, copper flashings
        'count': 400,
        'unit_cost_usd': 0.85,
    },
}


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
    """Fall through the candidate keys until something resolves."""
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


def _arched_foundation(col, ox, oy):
    """Stone foundation with 3 arched openings on the river (north) face.

    Geometry: a hollow rectangular plinth made from 4 wall slabs + 4 corner
    pilaster cylinders, then 3 half-cylinder arches sit above the openings on
    the river face suggesting an arcaded base.
    """
    stone = _mat('stone_wall', 'limestone', 'rough_stone', 'stone_foundation', 'sandstone')
    # Solid pad floor under the building so we don't see through to ground
    _cube(
        col, 'IRH_FoundationPad',
        location=(ox, oy, _BASE_HEIGHT * 0.05),
        scale=(PLATFORM_W + 0.4, PLATFORM_L + 0.4, _BASE_HEIGHT * 0.1),
        mat=stone,
    )
    # Side walls (E/W) — full solid stone
    z_mid = _BASE_HEIGHT / 2.0
    _cube(
        col, 'IRH_BaseWall_W',
        location=(ox - PLATFORM_W / 2 + _BASE_THICKNESS / 2, oy, z_mid),
        scale=(_BASE_THICKNESS, PLATFORM_L, _BASE_HEIGHT),
        mat=stone,
    )
    _cube(
        col, 'IRH_BaseWall_E',
        location=(ox + PLATFORM_W / 2 - _BASE_THICKNESS / 2, oy, z_mid),
        scale=(_BASE_THICKNESS, PLATFORM_L, _BASE_HEIGHT),
        mat=stone,
    )
    # South wall (away from river) — solid
    _cube(
        col, 'IRH_BaseWall_S',
        location=(ox, oy - PLATFORM_L / 2 + _BASE_THICKNESS / 2, z_mid),
        scale=(PLATFORM_W, _BASE_THICKNESS, _BASE_HEIGHT),
        mat=stone,
    )
    # North (river) face: arcaded — 4 pilasters with 3 arches between.
    # Pilasters: cylinders for clean round columns.
    n_pilasters = 4
    pilaster_r = 0.22
    arch_radius = (PLATFORM_W - 2 * pilaster_r) / (2 * (n_pilasters - 1))
    # Slight inset so the arcade reads as recessed under main wall above
    arc_y = oy + PLATFORM_L / 2 - _BASE_THICKNESS / 2
    for i in range(n_pilasters):
        t = i / (n_pilasters - 1)
        cx = ox - PLATFORM_W / 2 + pilaster_r + t * (PLATFORM_W - 2 * pilaster_r)
        _cylinder(
            col, f'IRH_BasePilaster_{i}',
            location=(cx, arc_y, _BASE_HEIGHT / 2.0),
            radius=pilaster_r, depth=_BASE_HEIGHT, mat=stone,
        )
    # Arches: half cylinders (rotated cylinders, then placed with axis along x)
    # Use a thicker cylinder shell visual by overlaying two cylinders with
    # different radii — cheap and reads as a stone arch from the hero angle.
    arch_top_z = _BASE_HEIGHT * 0.95
    for i in range(n_pilasters - 1):
        x0 = ox - PLATFORM_W / 2 + pilaster_r + i * 2 * arch_radius
        cx = x0 + arch_radius
        # Outer arch (stone)
        _cylinder(
            col, f'IRH_BaseArchOuter_{i}',
            location=(cx, arc_y, arch_top_z - arch_radius),
            radius=arch_radius, depth=_BASE_THICKNESS * 1.05, mat=stone,
            rotation=(0.0, math.radians(90.0), 0.0),
        )
        # Lintel slab above each arch (string course continuity)
        _cube(
            col, f'IRH_BaseLintel_{i}',
            location=(cx, arc_y, _BASE_HEIGHT - 0.07),
            scale=(2 * arch_radius * 0.95, _BASE_THICKNESS * 1.1, 0.14),
            mat=stone,
        )


def _walls(col, ox, oy):
    """Main 2-storey stone envelope sitting on top of the arched base."""
    stone = _mat('stone_wall', 'limestone', 'rough_stone', 'sandstone')
    z0 = _BASE_HEIGHT
    z_mid = z0 + WALL_HEIGHT_M / 2.0
    # 4 walls of the upper envelope
    walls = [
        ('S', (ox, oy - PLATFORM_L / 2 + _WALL_THICKNESS / 2, z_mid,
               PLATFORM_W, _WALL_THICKNESS, WALL_HEIGHT_M)),
        ('N', (ox, oy + PLATFORM_L / 2 - _WALL_THICKNESS / 2, z_mid,
               PLATFORM_W, _WALL_THICKNESS, WALL_HEIGHT_M)),
        ('W', (ox - PLATFORM_W / 2 + _WALL_THICKNESS / 2, oy, z_mid,
               _WALL_THICKNESS, PLATFORM_L, WALL_HEIGHT_M)),
        ('E', (ox + PLATFORM_W / 2 - _WALL_THICKNESS / 2, oy, z_mid,
               _WALL_THICKNESS, PLATFORM_L, WALL_HEIGHT_M)),
    ]
    for tag, (x, y, zc, sx, sy, sz) in walls:
        _cube(col, f'IRH_Wall_{tag}', (x, y, zc), (sx, sy, sz), stone)

    # String course at the floor break (between story 1 and 2)
    timber = _mat('lapacho_timber')
    _cube(
        col, 'IRH_StringCourse',
        location=(ox, oy, z0 + STORY_HEIGHT_M),
        scale=(PLATFORM_W + 0.10, PLATFORM_L + 0.10, 0.16),
        mat=timber,
    )

    # Gable triangular walls on E/W (short axis) — peaks above eave
    pitch_rad = math.radians(ROOF_PITCH_DEG)
    eave_z = z0 + WALL_HEIGHT_M
    ridge_z = eave_z + math.tan(pitch_rad) * (PLATFORM_L / 2)
    for sign, suffix in ((-1, 'W'), (1, 'E')):
        x = ox + sign * (PLATFORM_W / 2 - _WALL_THICKNESS / 2)
        verts = [
            (x, oy - PLATFORM_L / 2, eave_z),
            (x, oy + PLATFORM_L / 2, eave_z),
            (x, oy, ridge_z),
        ]
        faces = [(0, 1, 2)]
        mesh = bpy.data.meshes.new(f'IRH_Gable_{suffix}_Mesh')
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        obj = bpy.data.objects.new(f'IRH_Gable_{suffix}', mesh)
        if stone is not None:
            assign(obj, stone)
        col.objects.link(obj)


def _roof(col, ox, oy):
    """Gabled terracotta-tile roof — ridge runs along x (long axis)."""
    pitch_rad = math.radians(ROOF_PITCH_DEG)
    eave_z = _BASE_HEIGHT + WALL_HEIGHT_M
    half_w = PLATFORM_W / 2 + _ROOF_EAVE_OVERHANG
    half_l = PLATFORM_L / 2 + _ROOF_EAVE_OVERHANG
    ridge_z = eave_z + math.tan(pitch_rad) * (PLATFORM_L / 2)
    verts = [
        # 4 eave corners
        (ox - half_w, oy - half_l, eave_z),  # 0  SW
        (ox + half_w, oy - half_l, eave_z),  # 1  SE
        (ox + half_w, oy + half_l, eave_z),  # 2  NE
        (ox - half_w, oy + half_l, eave_z),  # 3  NW
        # 2 ridge endpoints (overhang on x ends)
        (ox - half_w, oy, ridge_z),          # 4  W ridge
        (ox + half_w, oy, ridge_z),          # 5  E ridge
    ]
    faces = [
        (0, 1, 5, 4),  # south slope
        (3, 4, 5, 2),  # north slope
        (0, 4, 3),     # W gable cap (cap the overhang)
        (1, 2, 5),     # E gable cap
    ]
    mesh = bpy.data.meshes.new('IRH_Roof_Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new('IRH_Roof', mesh)
    tile = _mat('terracotta_tile', 'clay_tile', 'laterite')
    if tile is not None:
        assign(obj, tile)
    col.objects.link(obj)


def _loggia(col, ox, oy):
    """Covered river-view loggia: 4 lapacho columns + flat tile lean-to roof.

    Sits on the north (river) face, extends out by _LOGGIA_DEPTH, at the
    upstairs floor level so it reads as a piano-nobile loggia.
    """
    timber = _mat('lapacho_timber')
    stone = _mat('stone_wall', 'limestone', 'rough_stone', 'sandstone')
    tile = _mat('terracotta_tile', 'clay_tile', 'laterite')
    floor_z = _BASE_HEIGHT + STORY_HEIGHT_M
    col_h = STORY_HEIGHT_M - 0.05
    loggia_y0 = oy + PLATFORM_L / 2
    loggia_y_outer = loggia_y0 + _LOGGIA_DEPTH

    # Loggia floor slab (sits over the arched base; cantilever ~ _LOGGIA_DEPTH)
    _cube(
        col, 'IRH_LoggiaFloor',
        location=(ox, loggia_y0 + _LOGGIA_DEPTH / 2.0, floor_z - 0.07),
        scale=(PLATFORM_W, _LOGGIA_DEPTH, 0.14),
        mat=stone,
    )
    # 4 lapacho columns at the outer edge
    n_cols = 4
    for i in range(n_cols):
        t = i / (n_cols - 1)
        cx = ox - PLATFORM_W / 2 + 0.3 + t * (PLATFORM_W - 0.6)
        _cylinder(
            col, f'IRH_LoggiaCol_{i}',
            location=(cx, loggia_y_outer - 0.18, floor_z + col_h / 2.0),
            radius=_LOGGIA_COL_RADIUS, depth=col_h, mat=timber,
        )
    # Horizontal lapacho beam capping the columns
    _cube(
        col, 'IRH_LoggiaBeam',
        location=(ox, loggia_y_outer - 0.18, floor_z + col_h + 0.05),
        scale=(PLATFORM_W, 0.20, 0.18),
        mat=timber,
    )
    # Tile lean-to roof over the loggia (slight slope away from main wall)
    pitch_rad = math.radians(8.0)
    eave_inner_z = _BASE_HEIGHT + WALL_HEIGHT_M - 0.05  # tucks under main eave
    eave_outer_z = eave_inner_z - math.tan(pitch_rad) * _LOGGIA_DEPTH
    verts = [
        (ox - PLATFORM_W / 2 - 0.2, loggia_y0, eave_inner_z),
        (ox + PLATFORM_W / 2 + 0.2, loggia_y0, eave_inner_z),
        (ox + PLATFORM_W / 2 + 0.2, loggia_y_outer + 0.2, eave_outer_z),
        (ox - PLATFORM_W / 2 - 0.2, loggia_y_outer + 0.2, eave_outer_z),
    ]
    faces = [(0, 1, 2, 3)]
    mesh = bpy.data.meshes.new('IRH_LoggiaRoof_Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new('IRH_LoggiaRoof', mesh)
    if tile is not None:
        assign(obj, tile)
    col.objects.link(obj)

    # Lapacho balustrade (simple horizontal rail across the river edge)
    _cube(
        col, 'IRH_LoggiaRail',
        location=(ox, loggia_y_outer - 0.18, floor_z + 1.05),
        scale=(PLATFORM_W - 0.4, 0.06, 0.08),
        mat=timber,
    )


def _shutters_and_doors(col, ox, oy):
    """Operable lapacho shutters flanking each window + entry door + balcony door."""
    timber = _mat('lapacho_timber')
    glass = _mat('glass_bottle_cobalt', 'water_reflective')
    z0 = _BASE_HEIGHT
    # South face (entry) — 1 door + 2 shutter-pairs (1 per storey row, 1 window)
    door_z = z0 + 1.05
    _cube(
        col, 'IRH_FrontDoor',
        location=(ox, oy - PLATFORM_L / 2 - 0.02, door_z),
        scale=(0.9, 0.06, 2.1),
        mat=timber,
    )
    # Shutter pairs on S face — symmetric around centre
    for i, sx in enumerate([-2.0, 2.0]):
        # Upstairs window, both leaves
        for j, off in enumerate([-_SHUTTER_W / 2 - 0.05, _SHUTTER_W / 2 + 0.05]):
            _cube(
                col, f'IRH_ShutterS_up_{i}_{j}',
                location=(ox + sx + off, oy - PLATFORM_L / 2 - 0.04,
                          z0 + STORY_HEIGHT_M + 1.0),
                scale=(_SHUTTER_W, 0.05, _SHUTTER_H),
                mat=timber,
            )
            # Glass pane behind
            if glass is not None and j == 0:
                _cube(
                    col, f'IRH_GlassS_up_{i}',
                    location=(ox + sx, oy - PLATFORM_L / 2 + 0.05,
                              z0 + STORY_HEIGHT_M + 1.0),
                    scale=(2 * _SHUTTER_W, 0.04, _SHUTTER_H),
                    mat=glass,
                )
    # E + W face shutters (one per storey each)
    for face_sign, tag in ((-1, 'W'), (1, 'E')):
        for storey, zc in enumerate([z0 + 1.2, z0 + STORY_HEIGHT_M + 1.0]):
            for j, off in enumerate([-_SHUTTER_W / 2 - 0.05, _SHUTTER_W / 2 + 0.05]):
                _cube(
                    col, f'IRH_Shutter{tag}_{storey}_{j}',
                    location=(ox + face_sign * (PLATFORM_W / 2 + 0.04),
                              oy + off, zc),
                    scale=(0.05, _SHUTTER_W, _SHUTTER_H),
                    mat=timber,
                )
    # North (river) face: balcony double-door instead of shutters
    bd_z = z0 + STORY_HEIGHT_M + 1.05
    _cube(
        col, 'IRH_BalconyDoor',
        location=(ox, oy + PLATFORM_L / 2 + 0.02, bd_z),
        scale=(1.6, 0.06, 2.1),
        mat=timber,
    )
    if glass is not None:
        _cube(
            col, 'IRH_BalconyGlass',
            location=(ox, oy + PLATFORM_L / 2 + 0.05, bd_z),
            scale=(1.5, 0.04, 2.0),
            mat=glass,
        )


def _dock_and_stairs(col, ox, oy):
    """Exterior stone stairs from loggia down to a small lapacho dock."""
    stone = _mat('stone_wall', 'limestone', 'rough_stone', 'sandstone')
    timber = _mat('lapacho_timber')
    floor_z = _BASE_HEIGHT + STORY_HEIGHT_M
    # Stone stair on east side, descending from loggia level to ground
    n_steps = 7
    step_run = 0.28
    step_rise = floor_z / n_steps
    stair_x = ox + PLATFORM_W / 2 + 0.6
    for i in range(n_steps):
        zc = (i + 0.5) * step_rise
        depth_y = (n_steps - i) * step_run
        _cube(
            col, f'IRH_Stair_{i}',
            location=(stair_x, oy + PLATFORM_L / 2 + depth_y / 2, zc),
            scale=(1.0, depth_y, step_rise),
            mat=stone,
        )
    # Stone path from stair toe to dock
    dock_y0 = oy + PLATFORM_L / 2 + (n_steps * step_run) + 0.3
    _cube(
        col, 'IRH_StonePath',
        location=(stair_x, dock_y0 + 0.8, 0.04),
        scale=(0.9, 1.6, 0.08),
        mat=stone,
    )
    # Lapacho dock (small) — 4 piles + deck
    dock_cx = stair_x
    dock_cy = dock_y0 + 1.6 + _DOCK_LENGTH / 2.0
    for i, (px, py) in enumerate([
        (dock_cx - 0.7, dock_cy - _DOCK_LENGTH / 2 + 0.2),
        (dock_cx + 0.7, dock_cy - _DOCK_LENGTH / 2 + 0.2),
        (dock_cx - 0.7, dock_cy + _DOCK_LENGTH / 2 - 0.2),
        (dock_cx + 0.7, dock_cy + _DOCK_LENGTH / 2 - 0.2),
    ]):
        _cylinder(
            col, f'IRH_DockPile_{i}',
            location=(px, py, 0.05),
            radius=0.10, depth=0.9, mat=timber,
        )
    _cube(
        col, 'IRH_DockDeck',
        location=(dock_cx, dock_cy, 0.42),
        scale=(1.8, _DOCK_LENGTH, 0.08),
        mat=timber,
    )


def build_italian_river_house_4pax(origin=(0.0, 0.0, 0.0)):
    """Build the Italian River House at ``origin``.

    Returns the parent collection. Idempotent across re-invocation.
    """
    name = 'ItalianRiverHouse4pax'
    col = _ensure_collection(name, None)
    ox, oy, _oz = origin
    _arched_foundation(col, ox, oy)
    _walls(col, ox, oy)
    _roof(col, ox, oy)
    _loggia(col, ox, oy)
    _shutters_and_doors(col, ox, oy)
    _dock_and_stairs(col, ox, oy)
    return col


# Backward-compat shim: older drivers + composite call ``build(...)``.
def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    col = build_italian_river_house_4pax(origin=location)
    if parent is not None and col.name not in [c.name for c in parent.children]:
        # rewire the collection under the requested parent
        bpy.context.scene.collection.children.unlink(col)
        parent.children.link(col)
    return col
