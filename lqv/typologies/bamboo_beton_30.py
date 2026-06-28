"""Typology — Bamboo + Beton 30 m² (hybrid couple unit, §3.10).

Hybrid micro-house: one polished-concrete service spine on the rear (north,
+Y) carries the kitchen/bath wet wall and gives the building its thermal mass
+ structural cross-bracing; Guadua bamboo culm posts ring the remaining three
sides; palm-thatch shed roof slopes down toward the south porch. 2 PAX.

Vocabulary first use: this is the *first* of four planned ``bamboo_beton_*``
variants (30 / 28 / family_curved / family_rectangular). Do NOT extract any
shared module yet — pattern lives here, refactor candidates come in wave 2.

Material registry mapping (lqv/materials/__init__.py keys, with chain
fallback through ``_resolve``):

* ``concrete_slab_108`` → ``cob_raw`` → ``sandstone`` for the service wall
  + plinth (project has no raw ``concrete`` key; ``concrete_slab_108`` is the
  closest match — polished off-form concrete grey).
* ``bamboo`` for culm posts, ring beam infill, low railings.
* ``palm_thatch`` for the shed roof skin.
* ``lapacho_timber`` for door, louvered windows, ring beam, porch deck.
* ``sandstone`` for the 60 cm perimeter stone foundation course (Rule 4).
* ``pv_glass`` → ``water_reflective`` fallback for the small high windows.
* ``laterite`` left to the driver (neutral ground).

Orientation invariant (consumed by ``lqv/subscene/bamboo_beton_30.py``):
porch + door + louvered windows face ``-Y`` so the SE camera at
``(+12, -12, 4.5)`` looks at the hero face.
"""
from __future__ import annotations

import math

import bpy

from lqv.materials import MAT, assign
from lqv.furniture import furnish_interior

# ---------------------------------------------------------------------------
# Geometry constants (6 m × 5 m footprint, 30 m²; 2 PAX)
# ---------------------------------------------------------------------------

FOOTPRINT_M2 = 30.0
PLATFORM_W = 6.0                   # x-axis (E-W), long dimension
PLATFORM_L = 5.0                   # y-axis (N-S), perpendicular to facade
PLINTH_H = 0.30                    # concrete-block plinth lifting walls off grade
STONE_COURSE_H = 0.60              # Rule 4 — earthen/bamboo never touch ground
WALL_HEIGHT_M = 2.6                # bamboo post height above plinth
ROOF_PITCH_DEG = 15.0
OVERHANG_S = 0.90                  # 90 cm south-porch overhang (Rule 5)
OVERHANG_OTHER = 0.45              # modest overhang on E / W / N
SLEEPS = 2
ORIENTATION = 'porch_and_door_face_negative_Y'
FRAME = 'guadua_bamboo + concrete_service_wall'
ROOF_TYPE = 'palm_thatch_mono_pitch'
SNAP = 'pad'

# Concrete service wall (rear, +Y side, full length)
_SERVICE_WALL_T = 0.25
_SERVICE_WALL_H = 2.4
_SERVICE_WALL_L = PLATFORM_W

# Bamboo posts
_POST_RADIUS = 0.035              # 70 mm Ø
_POST_GRID_M = 1.5
_POST_VERTS = 10

# Lapacho ring beam
_BEAM_W = 0.20
_BEAM_H = 0.15

# Roof
_ROOF_PITCH_RAD = math.radians(ROOF_PITCH_DEG)
_ROOF_THK = 0.10                  # palm-thatch slab thickness
_ROOF_W = PLATFORM_W + 2 * OVERHANG_OTHER     # 6.9 m east-west
_ROOF_L = PLATFORM_L + OVERHANG_S + OVERHANG_OTHER  # 6.35 m N-S

# Door + windows
_DOOR_W = 0.90
_DOOR_H = 2.10
_WINDOW_LOUVER_W = 1.00
_WINDOW_LOUVER_H = 1.00
_WINDOW_LOUVER_SLATS = 5
_HIGH_WINDOW_W = 0.80
_HIGH_WINDOW_H = 0.45
_GLASS_THK = 0.04

# Porch deck (south-facing)
_PORCH_W = PLATFORM_W
_PORCH_L = 1.5
_PORCH_THK = 0.06

NOTES = (
    'Polished concrete service wall (north / rear) carries kitchen + bath wet pod.',
    'Bamboo culm posts on 1.5 m grid around S/E/W; lapacho ring beam atop.',
    'Palm-thatch mono-pitch shed roof, 15° to south; 90 cm south overhang.',
    'Lapacho louvered windows flank the south door; 2 small high windows E + W.',
    '60 cm sandstone perimeter foundation under bamboo sides (Rule 4).',
    'Service wall floats on a 30 cm concrete plinth (no earthen wall touches grade).',
)


# ---------------------------------------------------------------------------
# MATERIAL_TAKEOFF — Paraguay 2026 USD; target $8.5-12.5 k.
# ---------------------------------------------------------------------------

_concrete_volume = (
    _SERVICE_WALL_L * _SERVICE_WALL_T * _SERVICE_WALL_H        # rear wall
    + PLATFORM_W * PLATFORM_L * PLINTH_H * 0.35                # plinth strips (35 % coverage)
    + 0.6 * 0.6 * 0.4                                          # interior wet-pod sink step
)
_bamboo_length = (
    12 * (WALL_HEIGHT_M + PLINTH_H)                            # 12 perimeter posts
    + 4 * (WALL_HEIGHT_M)                                      # 4 porch posts forward
    + 20                                                       # cross-bracing + railing accents
)
_thatch_area = (_ROOF_W * _ROOF_L) / math.cos(_ROOF_PITCH_RAD)
_lapacho_volume = (
    2 * (_BEAM_W * _BEAM_H * PLATFORM_W)                       # 2 ring beams
    + _PORCH_W * _PORCH_L * _PORCH_THK                         # porch deck
    + 2 * (_WINDOW_LOUVER_W * _WINDOW_LOUVER_H * 0.04)         # 2 louver assemblies
)
_stone_volume = STONE_COURSE_H * 0.4 * (2 * PLATFORM_W + 2 * PLATFORM_L)
_glass_area = 2 * (_HIGH_WINDOW_W * _HIGH_WINDOW_H)
_fasteners_count = 12 * 8 + 24 + 80 + 50 + 40                  # posts × joints + roof + windows + door + porch

MATERIAL_TAKEOFF: dict[str, dict] = {
    'concrete_service_wall': {
        'volume_m3': round(_concrete_volume, 3),
        'unit_cost_usd': 300.0,
    },
    'bamboo_culm': {
        'length_m': round(_bamboo_length, 1),
        'unit_cost_usd': 11.0,
    },
    'palm_thatch': {
        'area_m2': round(_thatch_area, 2),
        'unit_cost_usd': 38.0,
    },
    'lapacho_timber': {
        'volume_m3': round(_lapacho_volume, 3),
        'unit_cost_usd': 1100.0,
    },
    'sandstone_foundation': {
        'volume_m3': round(_stone_volume, 2),
        'unit_cost_usd': 320.0,
    },
    'lapacho_door': {
        'count': 1,
        'unit_cost_usd': 380.0,
    },
    'glass_glazing': {
        'area_m2': round(_glass_area + 2.0, 2),    # +2 m² for louver-frame infill panels
        'unit_cost_usd': 240.0,
    },
    'fasteners_lashings': {
        'count': int(_fasteners_count),
        'unit_cost_usd': 1.10,
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve(*keys: str):
    """Return the first MAT key that exists; None if none of them do."""
    for k in keys:
        m = MAT.get(k)
        if m is not None:
            return m
    return None


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


def _box(col, name, location, scale, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _cyl(col, name, location, radius, depth, mat, vertices=12, rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location,
        vertices=vertices, rotation=rotation,
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

def _stone_foundation(col, ox, oy):
    """60 cm sandstone perimeter course under the three bamboo sides + porch.

    Rule 4: earthen / bamboo never touches grade. The rear (concrete) face gets
    its own concrete plinth instead — see ``_concrete_plinth``.
    """
    mat = _resolve('sandstone', 'stream_bed', 'laterite')
    z_mid = STONE_COURSE_H / 2.0
    t = 0.40
    # South (porch) edge — full width
    _box(col, 'BB30_Stone_S',
         (ox, oy - PLATFORM_L / 2.0 + t / 2.0, z_mid),
         (PLATFORM_W, t, STONE_COURSE_H), mat)
    # East / West edges — shorten to avoid overlap with the rear concrete plinth
    side_len = PLATFORM_L - t
    for sign, tag in ((-1, 'W'), (1, 'E')):
        _box(col, f'BB30_Stone_{tag}',
             (ox + sign * (PLATFORM_W / 2.0 - t / 2.0),
              oy - t / 2.0,
              z_mid),
             (t, side_len, STONE_COURSE_H), mat)


def _concrete_plinth(col, ox, oy):
    """30 cm concrete plinth under the rear service wall (north edge)."""
    mat = _resolve('concrete_slab_108', 'cob_raw', 'sandstone')
    _box(col, 'BB30_Plinth_N',
         (ox, oy + PLATFORM_L / 2.0 - _SERVICE_WALL_T / 2.0, PLINTH_H / 2.0),
         (PLATFORM_W, _SERVICE_WALL_T, PLINTH_H), mat)
    # A thin floor slab inside the footprint at plinth height — reads as the
    # finished interior floor where the bamboo posts land on stone.
    _box(col, 'BB30_FloorSlab',
         (ox, oy, PLINTH_H - 0.04),
         (PLATFORM_W - 0.1, PLATFORM_L - 0.1, 0.08), mat)


def _service_wall(col, ox, oy):
    """Polished-concrete service wall on the rear (+Y / north).

    Single 6 × 0.25 × 2.4 m cuboid; carries kitchen + bath wet pod and provides
    thermal mass per the brief. Cob_raw / sandstone are fallbacks if the
    concrete shader is missing — both still read as a heavy monolithic surface.
    """
    mat = _resolve('concrete_slab_108', 'cob_raw', 'sandstone')
    z_mid = PLINTH_H + _SERVICE_WALL_H / 2.0
    y = oy + PLATFORM_L / 2.0 - _SERVICE_WALL_T / 2.0
    _box(col, 'BB30_ServiceWall',
         (ox, y, z_mid),
         (_SERVICE_WALL_L, _SERVICE_WALL_T, _SERVICE_WALL_H), mat)
    # Interior sink step (small cuboid protruding inboard, visible if porch
    # camera angle catches the open south face).
    _box(col, 'BB30_SinkStep',
         (ox - PLATFORM_W / 4.0,
          y - _SERVICE_WALL_T / 2.0 - 0.3,
          PLINTH_H + 0.4),
         (1.2, 0.6, 0.8), mat)


def _bamboo_posts(col, ox, oy):
    """12 perimeter bamboo posts on a 1.5 m grid (S / E / W only).

    The +Y / north edge is occupied by the concrete service wall, so no
    posts there. Posts rise from the stone foundation top (z = STONE_COURSE_H)
    to the ring-beam underside (z = STONE_COURSE_H + WALL_HEIGHT_M).
    """
    mat = _resolve('bamboo')
    base_z = STONE_COURSE_H
    top_z = base_z + WALL_HEIGHT_M
    z_mid = (base_z + top_z) / 2.0
    half_w = PLATFORM_W / 2.0
    half_l = PLATFORM_L / 2.0

    positions: list[tuple[float, float]] = []
    # South face: 5 posts (corners + 3 interior on 1.5 m grid)
    n_s = int(round(PLATFORM_W / _POST_GRID_M)) + 1
    for i in range(n_s):
        t = i / (n_s - 1)
        positions.append((ox - half_w + t * PLATFORM_W, oy - half_l))
    # East + West faces: 3 intermediate posts each (skip corners — already placed)
    n_ew = int(round(PLATFORM_L / _POST_GRID_M))
    for i in range(1, n_ew):
        t = i / n_ew
        y = oy - half_l + t * PLATFORM_L
        positions.append((ox - half_w, y))
        positions.append((ox + half_w, y))
    # North corners only (concrete wall handles the rest of the north line)
    positions.append((ox - half_w, oy + half_l))
    positions.append((ox + half_w, oy + half_l))

    for i, (px, py) in enumerate(positions):
        _cyl(col, f'BB30_Post_{i:02d}',
             (px, py, z_mid),
             _POST_RADIUS, WALL_HEIGHT_M, mat, vertices=_POST_VERTS)


def _ring_beam(col, ox, oy):
    """Lapacho ring beam atop posts — S / E / W; structural cap to the bamboo grid."""
    mat = _resolve('lapacho_timber')
    z_mid = STONE_COURSE_H + WALL_HEIGHT_M + _BEAM_H / 2.0
    half_w = PLATFORM_W / 2.0
    half_l = PLATFORM_L / 2.0
    # South
    _box(col, 'BB30_Beam_S',
         (ox, oy - half_l, z_mid),
         (PLATFORM_W, _BEAM_W, _BEAM_H), mat)
    # East / West
    _box(col, 'BB30_Beam_W',
         (ox - half_w, oy, z_mid),
         (_BEAM_W, PLATFORM_L, _BEAM_H), mat)
    _box(col, 'BB30_Beam_E',
         (ox + half_w, oy, z_mid),
         (_BEAM_W, PLATFORM_L, _BEAM_H), mat)


def _roof(col, ox, oy):
    """Palm-thatch mono-pitch shed roof. Low edge south, high edge north.

    Built as an oriented cuboid: tilt around X by ROOF_PITCH_RAD so the south
    edge drops below the north edge. Simpler than the from_pydata sheet path
    used in container_river_house — palm_thatch already has displacement so the
    silhouette doesn't read as a hard rectangular slab.
    """
    mat = _resolve('palm_thatch', 'sod_canopy')
    eave_low_z = STONE_COURSE_H + WALL_HEIGHT_M + _BEAM_H        # south eave
    # Center the roof so it tilts about the building Y center; the
    # geometric center of the tilted plane sits at z = (low + high) / 2.
    eave_high_z = eave_low_z + _ROOF_L * math.tan(_ROOF_PITCH_RAD)
    z_mid = (eave_low_z + eave_high_z) / 2.0 + _ROOF_THK / 2.0
    # Center Y: roof extends from (south porch tip) to (north back overhang).
    y_south = oy - PLATFORM_L / 2.0 - OVERHANG_S
    y_north = oy + PLATFORM_L / 2.0 + OVERHANG_OTHER
    y_mid = (y_south + y_north) / 2.0
    _box(col, 'BB30_Roof_PreTilt',
         (ox, y_mid, z_mid),
         (_ROOF_W, _ROOF_L, _ROOF_THK), mat)
    roof = bpy.data.objects['BB30_Roof_PreTilt']
    # Tilt around X axis (so south edge dips). Positive rotation tilts +Y down,
    # we want -Y (south) down → negative rotation.
    roof.rotation_euler = (-_ROOF_PITCH_RAD, 0.0, 0.0)
    roof.name = 'BB30_Roof'


def _door_and_louvers(col, ox, oy):
    """Lapacho door (center) + 2 louvered windows flanking it, all on the
    south face (-Y) so the camera reads the hero side.
    """
    mat_door = _resolve('lapacho_timber')
    mat_glass = _resolve('pv_glass', 'water_reflective')
    door_y = oy - PLATFORM_L / 2.0
    base_z = STONE_COURSE_H
    # Door slab (slightly proud of the facade)
    _box(col, 'BB30_Door',
         (ox, door_y - 0.04, base_z + _DOOR_H / 2.0),
         (_DOOR_W, 0.05, _DOOR_H), mat_door)
    # Door header lintel
    _box(col, 'BB30_DoorHeader',
         (ox, door_y - 0.04, base_z + _DOOR_H + 0.05),
         (_DOOR_W + 0.20, 0.07, 0.10), mat_door)

    # Louvered windows — left + right of door
    for side_sign, side_tag in ((-1, 'L'), (1, 'R')):
        cx = ox + side_sign * (PLATFORM_W / 4.0)
        sill_z = base_z + 0.95
        # Outer frame (4 thin lapacho slabs forming a rectangle)
        frame_t = 0.04
        # Top / bottom rails
        for z_off, name in ((_WINDOW_LOUVER_H, 'Top'), (0.0, 'Bot')):
            _box(col, f'BB30_LouverFrame_{side_tag}_{name}',
                 (cx, door_y - 0.03, sill_z + z_off),
                 (_WINDOW_LOUVER_W + frame_t * 2, 0.05, frame_t), mat_door)
        # Left / right stiles
        for x_off, name in ((-_WINDOW_LOUVER_W / 2 - frame_t / 2, 'LStile'),
                            (_WINDOW_LOUVER_W / 2 + frame_t / 2, 'RStile')):
            _box(col, f'BB30_LouverFrame_{side_tag}_{name}',
                 (cx + x_off, door_y - 0.03, sill_z + _WINDOW_LOUVER_H / 2.0),
                 (frame_t, 0.05, _WINDOW_LOUVER_H + frame_t * 2), mat_door)
        # Horizontal lapacho slats (5 of them) angled slightly
        slat_h = (_WINDOW_LOUVER_H - 0.10) / _WINDOW_LOUVER_SLATS
        for k in range(_WINDOW_LOUVER_SLATS):
            sz = sill_z + 0.05 + (k + 0.5) * slat_h
            _box(col, f'BB30_LouverSlat_{side_tag}_{k}',
                 (cx, door_y - 0.05, sz),
                 (_WINDOW_LOUVER_W, 0.03, slat_h * 0.65), mat_door)

    # 2 small high windows — east + west faces, near the roof ring beam
    high_z = base_z + WALL_HEIGHT_M - _HIGH_WINDOW_H / 2.0 - 0.10
    for side_sign, tag in ((-1, 'W'), (1, 'E')):
        wx = ox + side_sign * PLATFORM_W / 2.0
        _box(col, f'BB30_HighWindow_{tag}',
             (wx, oy, high_z),
             (_GLASS_THK, _HIGH_WINDOW_W, _HIGH_WINDOW_H), mat_glass)


def _porch_deck(col, ox, oy):
    """South porch deck (lapacho boards) on 4 short bamboo posts forward of facade."""
    mat_deck = _resolve('lapacho_timber')
    mat_post = _resolve('bamboo')
    base_z = STONE_COURSE_H
    porch_y_mid = oy - PLATFORM_L / 2.0 - _PORCH_L / 2.0
    _box(col, 'BB30_PorchDeck',
         (ox, porch_y_mid, base_z + _PORCH_THK / 2.0),
         (_PORCH_W, _PORCH_L, _PORCH_THK), mat_deck)
    # 4 forward porch posts (carry the south overhang)
    for i, x_off in enumerate((-PLATFORM_W / 2 + 0.2,
                                -PLATFORM_W / 6,
                                PLATFORM_W / 6,
                                PLATFORM_W / 2 - 0.2)):
        _cyl(col, f'BB30_PorchPost_{i}',
             (ox + x_off,
              oy - PLATFORM_L / 2.0 - _PORCH_L + 0.1,
              base_z + WALL_HEIGHT_M / 2.0),
             _POST_RADIUS, WALL_HEIGHT_M, mat_post, vertices=_POST_VERTS)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def build_bamboo_beton_30(origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
                          parent: bpy.types.Collection | None = None,
                          variant: str = 'A') -> bpy.types.Collection:
    """Build the Bamboo + Beton 30 m² typology at ``origin``.

    Parameters mirror the sibling typologies (bamboo_river_house,
    container_river_house). ``variant`` is currently only used for naming —
    lighting is set by the driver's ``setup_world`` call. Idempotent: a
    second invocation re-uses the existing ``BambooBeton_30`` collection
    rather than duplicating.
    """
    col = _ensure_collection('BambooBeton_30', parent)
    ox, oy, _oz = origin

    _stone_foundation(col, ox, oy)
    _concrete_plinth(col, ox, oy)
    _service_wall(col, ox, oy)
    _bamboo_posts(col, ox, oy)
    _ring_beam(col, ox, oy)
    _roof(col, ox, oy)
    _door_and_louvers(col, ox, oy)
    _porch_deck(col, ox, oy)

    # P1.B.1 — interior furniture stubs (RENDER_VIEW=interior readable).
    furn_origin = (ox, oy - (_SERVICE_WALL_T / 2.0 + 0.20))
    furn_w = PLATFORM_W - 1.20
    furn_l = PLATFORM_L - _SERVICE_WALL_T - 0.60
    furnish_interior(
        col, footprint_w=furn_w, footprint_l=furn_l,
        origin_xy=furn_origin, floor_z=STONE_COURSE_H,
        pax=SLEEPS, style='bamboo', variant=variant, name_prefix='BB30_Furn',
    )

    return col


def build(parent: bpy.types.Collection | None = None,
          location: tuple[float, float, float] = (0.0, 0.0, 0.0),
          variant: str = 'A') -> bpy.types.Collection:
    """Legacy alias matching the older typologies API."""
    return build_bamboo_beton_30(origin=location, parent=parent, variant=variant)
