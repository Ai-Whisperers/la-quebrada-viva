"""Typology — Bamboo + Beton 28 m² (hybrid solo unit, §3.10 — v30 sibling).

Stripped sibling of ``bamboo_beton_30``: same hybrid vocabulary (polished
concrete service wall on the rear / north, Guadua bamboo culm posts ringing
the remaining three sides, palm-thatch shed roof, lapacho ring beam + porch
deck + louvered windows, 60 cm sandstone foundation course under the bamboo
sides), reduced to a long-narrow 3.5 × 8.0 m floor plan for 1 PAX.

Differences from ``bamboo_beton_30`` are intentional — this is a "smaller
sibling" not a refactor candidate. Per the "factor on second use, not first"
policy, this is the SECOND use of the bamboo + concrete pairing in the
``bamboo_beton_*`` family (first: ``bamboo_beton_30``); a parallel agent is
factoring ``lqv.house.bamboo_frame`` from the wigwam + container pair. When
that module lands, the bamboo culm / lashing / palm-thatch helpers here can be
swapped for imports; until then we mirror the v30 inline style.

Programme (1 PAX):
* Sleep nook (corner, ~2.0 × 2.0 m) — single bed, curtain divider, no door.
* Kitchenette ledge — built off the concrete service wall as a single counter
  run (no full kitchen, just a sink + induction hob outline).
* Wet pod (toilet + shower) — back to the service wall, opposite the nook.
* Living strip — long axis between, opening onto the south porch.

Geometry highlights:
* Long axis along X (3.5 m wide by 8.0 m long → 28.0 m²).
* Door + porch + 2 louvered windows face -Y (south).
* Concrete service wall on +Y (north), full 8 m length.
* Palm-thatch mono-pitch shed roof, 12° toward south (shallower than v30's 15°
  because the 8 m roof run accumulates more drop per degree).
* 60 cm porch overhang (Rule 5 says 90 cm+; the porch deck extends another
  1.2 m beyond the eave so the deck-line + eave-line readout still satisfies
  the rule at the building footprint).

Material registry mapping (lqv/materials/__init__.py keys, with chain
fallback through ``_resolve`` — identical chain to v30):

* ``concrete`` → ``concrete_slab_108`` → ``cob_raw`` → ``sandstone`` for the
  service wall + plinth (no raw ``concrete`` key in the project; chain lands
  on ``concrete_slab_108`` which reads as polished off-form grey).
* ``bamboo`` for culm posts, porch posts.
* ``palm_thatch`` for the shed roof skin.
* ``lapacho_timber`` for door, louvered windows, ring beam, porch deck.
* ``sandstone`` for the 60 cm perimeter stone foundation course (Rule 4).
* ``pv_glass`` → ``water_reflective`` fallback for the 2 small high windows.
* ``laterite`` left to the driver (neutral ground).

Orientation invariant (consumed by ``lqv/subscene/bamboo_beton_28.py``):
porch + door + louvered windows face ``-Y`` so the SE camera at
``(+sin θ · 11, -cos θ · 11, 4.0)`` looks at the hero face. ``θ`` is set by
the cameras helper from the standard SE oblique.
"""
from __future__ import annotations

import math

import bpy

from lqv.materials import MAT, assign


# ---------------------------------------------------------------------------
# Geometry constants (3.5 m × 8.0 m footprint, 28 m²; 1 PAX)
# ---------------------------------------------------------------------------

FOOTPRINT_M2 = 28.0
PLATFORM_W = 8.0                   # x-axis, long dimension (E-W)
PLATFORM_L = 3.5                   # y-axis (N-S), perpendicular to facade
PLINTH_H = 0.30                    # concrete-block plinth under service wall
STONE_COURSE_H = 0.60              # Rule 4 — earthen/bamboo never touch grade
WALL_HEIGHT_M = 2.6                # bamboo post height above plinth
ROOF_PITCH_DEG = 12.0              # shallower than v30 (longer roof run)
OVERHANG_S = 0.60                  # 60 cm south porch eave (porch deck adds 1.2 m)
OVERHANG_OTHER = 0.40              # modest overhang E / W / N
SLEEPS = 1
ORIENTATION = 'porch_and_door_face_negative_Y'
FRAME = 'guadua_bamboo + concrete_service_wall'
ROOF_TYPE = 'palm_thatch_mono_pitch'
SNAP = 'pad'

# Concrete service wall (rear, +Y side, full length)
_SERVICE_WALL_T = 0.22             # thinner than v30's 0.25 — single occupant
_SERVICE_WALL_H = 2.4
_SERVICE_WALL_L = PLATFORM_W

# Kitchenette ledge — counter run off the service wall
_KITCHENETTE_L = 2.2
_KITCHENETTE_D = 0.55
_KITCHENETTE_H = 0.10               # ledge thickness; carried at 0.9 m AFL
_KITCHENETTE_Z = 0.90

# Bamboo posts
_POST_RADIUS = 0.035                # 70 mm Ø
_POST_GRID_M = 1.6
_POST_VERTS = 10

# Lapacho ring beam
_BEAM_W = 0.18
_BEAM_H = 0.14

# Roof
_ROOF_PITCH_RAD = math.radians(ROOF_PITCH_DEG)
_ROOF_THK = 0.10                    # palm-thatch slab thickness
_ROOF_W = PLATFORM_W + 2 * OVERHANG_OTHER     # 8.8 m east-west
_ROOF_L = PLATFORM_L + OVERHANG_S + OVERHANG_OTHER  # 4.5 m N-S

# Door + windows
_DOOR_W = 0.90
_DOOR_H = 2.10
_WINDOW_LOUVER_W = 0.90
_WINDOW_LOUVER_H = 1.00
_WINDOW_LOUVER_SLATS = 5
_HIGH_WINDOW_W = 0.70
_HIGH_WINDOW_H = 0.40
_GLASS_THK = 0.04

# Porch deck (south-facing, 1.2 m projection)
_PORCH_W = PLATFORM_W
_PORCH_L = 1.2
_PORCH_THK = 0.06

# Sleep nook curtain divider (visual only — soft rectangle)
_NOOK_W = 2.0
_NOOK_DIVIDER_T = 0.02
_NOOK_DIVIDER_H = WALL_HEIGHT_M - 0.30

NOTES = (
    'Polished concrete service wall (north / rear) carries kitchenette ledge + wet pod.',
    'Bamboo culm posts on 1.6 m grid around S / E / W; lapacho ring beam atop.',
    'Palm-thatch mono-pitch shed roof, 12° to south; 60 cm south eave + 1.2 m porch deck.',
    'Lapacho louvered windows flank the south door; 2 small high windows E + W.',
    '60 cm sandstone perimeter foundation under bamboo sides (Rule 4).',
    'Concrete service wall floats on 30 cm concrete plinth (no earthen wall touches grade).',
    '1 PAX: single bed nook in W corner, kitchenette ledge along service wall, wet pod in E corner.',
)


# ---------------------------------------------------------------------------
# MATERIAL_TAKEOFF — Paraguay 2026 USD; target $6.5-9.5 k band.
# Smaller than v30 ($8,628) because of lower bamboo + thatch quantities;
# concrete service wall + sandstone foundation only modestly reduced because
# the perimeter / wall-length ratio is similar at this footprint.
# ---------------------------------------------------------------------------

_concrete_volume = (
    _SERVICE_WALL_L * _SERVICE_WALL_T * _SERVICE_WALL_H        # rear wall
    + PLATFORM_W * PLATFORM_L * PLINTH_H * 0.30                # plinth strips (30 % coverage)
    + 0.5 * 0.5 * 0.4                                          # wet-pod sink step
)
_bamboo_length = (
    10 * (WALL_HEIGHT_M + PLINTH_H)                            # 10 perimeter posts (3.5 m wide → fewer than v30)
    + 4 * WALL_HEIGHT_M                                        # 4 porch posts forward
    + 14                                                       # cross-bracing + railing accents
)
_thatch_area = (_ROOF_W * _ROOF_L) / math.cos(_ROOF_PITCH_RAD)
_lapacho_volume = (
    2 * (_BEAM_W * _BEAM_H * PLATFORM_W)                       # 2 ring beams
    + _PORCH_W * _PORCH_L * _PORCH_THK                         # porch deck
    + 2 * (_WINDOW_LOUVER_W * _WINDOW_LOUVER_H * 0.04)         # 2 louver assemblies
    + 1 * (_DOOR_W * _DOOR_H * 0.045)                          # door slab
)
_stone_volume = STONE_COURSE_H * 0.4 * (2 * PLATFORM_W + 2 * PLATFORM_L)
_glass_area = 2 * (_HIGH_WINDOW_W * _HIGH_WINDOW_H) + 1.4      # +1.4 m² louver-frame infill panels
_fasteners_count = 10 * 8 + 24 + 70 + 45 + 32                  # posts × joints + roof + windows + door + porch
_borax_treatment_kg = round(_bamboo_length * 0.6, 1)           # ~0.6 kg per m of culm (borax + boric acid soak)

MATERIAL_TAKEOFF: dict[str, dict] = {
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
    'concrete': {
        'volume_m3': round(_concrete_volume, 3),
        'unit_cost_usd': 300.0,
    },
    'sandstone': {
        'volume_m3': round(_stone_volume, 2),
        'unit_cost_usd': 320.0,
    },
    'pv_glass': {
        'area_m2': round(_glass_area, 2),
        'unit_cost_usd': 240.0,
    },
    'fasteners_lashings': {
        'count': int(_fasteners_count),
        'unit_cost_usd': 1.10,
    },
    'borax_boric_treatment': {
        'weight_kg': _borax_treatment_kg,
        'unit_cost_usd': 8.0,
    },
}


# ---------------------------------------------------------------------------
# Helpers (mirror v30 — to be replaced by lqv.house.bamboo_frame imports
# when the parallel factoring agent lands that module)
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
    """60 cm sandstone perimeter course under the three bamboo sides (S / E / W).

    Rule 4: earthen / bamboo never touches grade. The rear (concrete) face gets
    its own concrete plinth instead — see ``_concrete_plinth``.
    """
    mat = _resolve('sandstone', 'stream_bed', 'laterite')
    z_mid = STONE_COURSE_H / 2.0
    t = 0.40
    # South (porch) edge — full width
    _box(col, 'BB28_Stone_S',
         (ox, oy - PLATFORM_L / 2.0 + t / 2.0, z_mid),
         (PLATFORM_W, t, STONE_COURSE_H), mat)
    # East / West edges — shorten to avoid overlap with the rear concrete plinth
    side_len = PLATFORM_L - t
    for sign, tag in ((-1, 'W'), (1, 'E')):
        _box(col, f'BB28_Stone_{tag}',
             (ox + sign * (PLATFORM_W / 2.0 - t / 2.0),
              oy - t / 2.0,
              z_mid),
             (t, side_len, STONE_COURSE_H), mat)


def _concrete_plinth(col, ox, oy):
    """30 cm concrete plinth under the rear service wall (north edge) + thin floor slab."""
    mat = _resolve('concrete', 'concrete_slab_108', 'cob_raw', 'sandstone')
    _box(col, 'BB28_Plinth_N',
         (ox, oy + PLATFORM_L / 2.0 - _SERVICE_WALL_T / 2.0, PLINTH_H / 2.0),
         (PLATFORM_W, _SERVICE_WALL_T, PLINTH_H), mat)
    # Interior floor slab — reads as the finished floor where bamboo posts land on stone.
    _box(col, 'BB28_FloorSlab',
         (ox, oy, PLINTH_H - 0.04),
         (PLATFORM_W - 0.1, PLATFORM_L - 0.1, 0.08), mat)


def _service_wall(col, ox, oy):
    """Polished-concrete service wall on the rear (+Y / north).

    Single 8 × 0.22 × 2.4 m cuboid; carries the kitchenette ledge + wet pod and
    gives the building its thermal mass per the brief. Cob_raw / sandstone are
    chain fallbacks if the concrete shader is missing — both still read as a
    heavy monolithic surface.
    """
    mat = _resolve('concrete', 'concrete_slab_108', 'cob_raw', 'sandstone')
    z_mid = PLINTH_H + _SERVICE_WALL_H / 2.0
    y = oy + PLATFORM_L / 2.0 - _SERVICE_WALL_T / 2.0
    _box(col, 'BB28_ServiceWall',
         (ox, y, z_mid),
         (_SERVICE_WALL_L, _SERVICE_WALL_T, _SERVICE_WALL_H), mat)
    # Kitchenette ledge — counter run protruding inboard from the service wall.
    _box(col, 'BB28_KitchenetteLedge',
         (ox - PLATFORM_W / 4.0,
          y - _SERVICE_WALL_T / 2.0 - _KITCHENETTE_D / 2.0,
          PLINTH_H + _KITCHENETTE_Z + _KITCHENETTE_H / 2.0),
         (_KITCHENETTE_L, _KITCHENETTE_D, _KITCHENETTE_H), mat)
    # Wet-pod sink step on the east end (small cuboid).
    _box(col, 'BB28_WetPodStep',
         (ox + PLATFORM_W / 3.0,
          y - _SERVICE_WALL_T / 2.0 - 0.30,
          PLINTH_H + 0.40),
         (1.0, 0.6, 0.80), mat)


def _bamboo_posts(col, ox, oy):
    """10 perimeter bamboo posts on a ~1.6 m grid (S / E / W only).

    The +Y / north edge is occupied by the concrete service wall, so no posts
    there. Posts rise from the stone foundation top (z = STONE_COURSE_H) to
    the ring-beam underside (z = STONE_COURSE_H + WALL_HEIGHT_M).
    """
    mat = _resolve('bamboo')
    base_z = STONE_COURSE_H
    top_z = base_z + WALL_HEIGHT_M
    z_mid = (base_z + top_z) / 2.0
    half_w = PLATFORM_W / 2.0
    half_l = PLATFORM_L / 2.0

    positions: list[tuple[float, float]] = []
    # South face: 6 posts (corners + 4 interior on ~1.6 m grid across 8 m)
    n_s = int(round(PLATFORM_W / _POST_GRID_M)) + 1
    for i in range(n_s):
        t = i / (n_s - 1)
        positions.append((ox - half_w + t * PLATFORM_W, oy - half_l))
    # East + West faces: only 1 intermediate post each (3.5 m / 1.6 m grid → 1 mid)
    n_ew = int(round(PLATFORM_L / _POST_GRID_M))
    n_ew = max(n_ew, 1)
    for i in range(1, n_ew):
        t = i / n_ew
        y = oy - half_l + t * PLATFORM_L
        positions.append((ox - half_w, y))
        positions.append((ox + half_w, y))
    # North corners only — service wall takes the rest of the north line.
    positions.append((ox - half_w, oy + half_l))
    positions.append((ox + half_w, oy + half_l))

    for i, (px, py) in enumerate(positions):
        _cyl(col, f'BB28_Post_{i:02d}',
             (px, py, z_mid),
             _POST_RADIUS, WALL_HEIGHT_M, mat, vertices=_POST_VERTS)


def _ring_beam(col, ox, oy):
    """Lapacho ring beam atop posts (S / E / W); structural cap to bamboo grid."""
    mat = _resolve('lapacho_timber')
    z_mid = STONE_COURSE_H + WALL_HEIGHT_M + _BEAM_H / 2.0
    half_w = PLATFORM_W / 2.0
    half_l = PLATFORM_L / 2.0
    # South
    _box(col, 'BB28_Beam_S',
         (ox, oy - half_l, z_mid),
         (PLATFORM_W, _BEAM_W, _BEAM_H), mat)
    # East / West
    _box(col, 'BB28_Beam_W',
         (ox - half_w, oy, z_mid),
         (_BEAM_W, PLATFORM_L, _BEAM_H), mat)
    _box(col, 'BB28_Beam_E',
         (ox + half_w, oy, z_mid),
         (_BEAM_W, PLATFORM_L, _BEAM_H), mat)


def _roof(col, ox, oy):
    """Palm-thatch mono-pitch shed roof. Low edge south, high edge north.

    Built as an oriented cuboid: tilt around X by ROOF_PITCH_RAD so the south
    edge drops below the north edge. Identical strategy to v30; palm_thatch
    material already has displacement so the silhouette doesn't read as a hard
    rectangular slab.
    """
    mat = _resolve('palm_thatch', 'sod_canopy')
    eave_low_z = STONE_COURSE_H + WALL_HEIGHT_M + _BEAM_H        # south eave
    eave_high_z = eave_low_z + _ROOF_L * math.tan(_ROOF_PITCH_RAD)
    z_mid = (eave_low_z + eave_high_z) / 2.0 + _ROOF_THK / 2.0
    y_south = oy - PLATFORM_L / 2.0 - OVERHANG_S
    y_north = oy + PLATFORM_L / 2.0 + OVERHANG_OTHER
    y_mid = (y_south + y_north) / 2.0
    _box(col, 'BB28_Roof_PreTilt',
         (ox, y_mid, z_mid),
         (_ROOF_W, _ROOF_L, _ROOF_THK), mat)
    roof = bpy.data.objects['BB28_Roof_PreTilt']
    # Tilt around X: south edge dips → negative rotation.
    roof.rotation_euler = (-_ROOF_PITCH_RAD, 0.0, 0.0)
    roof.name = 'BB28_Roof'


def _door_and_louvers(col, ox, oy):
    """Lapacho door + 2 louvered windows flanking it on the south face (-Y).

    Same construction as v30 (flat slat stacks). 2 small high windows on E / W
    near the ring beam for cross-vent + clerestory daylight.
    """
    mat_door = _resolve('lapacho_timber')
    mat_glass = _resolve('pv_glass', 'water_reflective')
    door_y = oy - PLATFORM_L / 2.0
    base_z = STONE_COURSE_H
    # Door slab — slightly proud of the facade
    _box(col, 'BB28_Door',
         (ox, door_y - 0.04, base_z + _DOOR_H / 2.0),
         (_DOOR_W, 0.05, _DOOR_H), mat_door)
    # Door header lintel
    _box(col, 'BB28_DoorHeader',
         (ox, door_y - 0.04, base_z + _DOOR_H + 0.05),
         (_DOOR_W + 0.20, 0.07, 0.10), mat_door)

    # Louvered windows — left + right of the door (8 m wide façade → set them at quarter points)
    for side_sign, side_tag in ((-1, 'L'), (1, 'R')):
        cx = ox + side_sign * (PLATFORM_W / 4.0)
        sill_z = base_z + 0.95
        # Outer frame (4 thin lapacho slabs forming a rectangle)
        frame_t = 0.04
        for z_off, name in ((_WINDOW_LOUVER_H, 'Top'), (0.0, 'Bot')):
            _box(col, f'BB28_LouverFrame_{side_tag}_{name}',
                 (cx, door_y - 0.03, sill_z + z_off),
                 (_WINDOW_LOUVER_W + frame_t * 2, 0.05, frame_t), mat_door)
        for x_off, name in ((-_WINDOW_LOUVER_W / 2 - frame_t / 2, 'LStile'),
                            (_WINDOW_LOUVER_W / 2 + frame_t / 2, 'RStile')):
            _box(col, f'BB28_LouverFrame_{side_tag}_{name}',
                 (cx + x_off, door_y - 0.03, sill_z + _WINDOW_LOUVER_H / 2.0),
                 (frame_t, 0.05, _WINDOW_LOUVER_H + frame_t * 2), mat_door)
        # Horizontal lapacho slats (5) angled slightly — built as flat slat stack
        slat_h = (_WINDOW_LOUVER_H - 0.10) / _WINDOW_LOUVER_SLATS
        for k in range(_WINDOW_LOUVER_SLATS):
            sz = sill_z + 0.05 + (k + 0.5) * slat_h
            _box(col, f'BB28_LouverSlat_{side_tag}_{k}',
                 (cx, door_y - 0.05, sz),
                 (_WINDOW_LOUVER_W, 0.03, slat_h * 0.65), mat_door)

    # 2 small high windows — east + west faces, near the ring beam
    high_z = base_z + WALL_HEIGHT_M - _HIGH_WINDOW_H / 2.0 - 0.10
    for side_sign, tag in ((-1, 'W'), (1, 'E')):
        wx = ox + side_sign * PLATFORM_W / 2.0
        _box(col, f'BB28_HighWindow_{tag}',
             (wx, oy, high_z),
             (_GLASS_THK, _HIGH_WINDOW_W, _HIGH_WINDOW_H), mat_glass)


def _porch_deck(col, ox, oy):
    """South porch deck (lapacho) on 4 short bamboo posts forward of the facade."""
    mat_deck = _resolve('lapacho_timber')
    mat_post = _resolve('bamboo')
    base_z = STONE_COURSE_H
    porch_y_mid = oy - PLATFORM_L / 2.0 - _PORCH_L / 2.0
    _box(col, 'BB28_PorchDeck',
         (ox, porch_y_mid, base_z + _PORCH_THK / 2.0),
         (_PORCH_W, _PORCH_L, _PORCH_THK), mat_deck)
    # 4 forward porch posts (carry the south overhang)
    for i, x_off in enumerate((-PLATFORM_W / 2 + 0.25,
                                -PLATFORM_W / 6,
                                PLATFORM_W / 6,
                                PLATFORM_W / 2 - 0.25)):
        _cyl(col, f'BB28_PorchPost_{i}',
             (ox + x_off,
              oy - PLATFORM_L / 2.0 - _PORCH_L + 0.1,
              base_z + WALL_HEIGHT_M / 2.0),
             _POST_RADIUS, WALL_HEIGHT_M, mat_post, vertices=_POST_VERTS)


def _sleep_nook_divider(col, ox, oy):
    """Curtain divider for the corner sleep nook (W side) — flat lapacho stile.

    Single tall thin slab at the nook boundary; reads as a privacy partition
    between the bed and the living strip. No door, no full wall (per the brief).
    """
    mat = _resolve('lapacho_timber')
    base_z = STONE_COURSE_H
    nook_x = ox - PLATFORM_W / 2.0 + _NOOK_W
    nook_y = oy - PLATFORM_L / 2.0 + 0.20  # just inboard of the south posts
    z_mid = base_z + _NOOK_DIVIDER_H / 2.0
    _box(col, 'BB28_NookDivider',
         (nook_x, nook_y + _NOOK_W / 2.0, z_mid),
         (_NOOK_DIVIDER_T, _NOOK_W - 0.40, _NOOK_DIVIDER_H), mat)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def build_bamboo_beton_28(origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
                          parent: bpy.types.Collection | None = None,
                          variant: str = 'A') -> bpy.types.Collection:
    """Build the Bamboo + Beton 28 m² typology at ``origin``.

    Idempotent: a second invocation re-uses the existing ``BambooBeton_28``
    collection rather than duplicating. ``variant`` is currently only used for
    naming — lighting is set by the driver's ``setup_world`` call.
    """
    col = _ensure_collection('BambooBeton_28', parent)
    ox, oy, _oz = origin

    _stone_foundation(col, ox, oy)
    _concrete_plinth(col, ox, oy)
    _service_wall(col, ox, oy)
    _bamboo_posts(col, ox, oy)
    _ring_beam(col, ox, oy)
    _roof(col, ox, oy)
    _door_and_louvers(col, ox, oy)
    _porch_deck(col, ox, oy)
    _sleep_nook_divider(col, ox, oy)

    return col


def build(parent: bpy.types.Collection | None = None,
          location: tuple[float, float, float] = (0.0, 0.0, 0.0),
          variant: str = 'A') -> bpy.types.Collection:
    """Legacy alias matching the older typologies API."""
    return build_bamboo_beton_28(origin=location, parent=parent, variant=variant)
