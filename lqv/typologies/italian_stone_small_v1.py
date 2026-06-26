"""Typology — Italian Stone Small v1.

Small 2-pax rural Italian stone cottage, ~5 m × 4 m footprint, single storey,
low-pitch terracotta-tile gabled roof. Rough sandstone walls with visible
mortar lines + 60 cm stone foundation course (Rule 4 — earthen surfaces never
touch grade). One lapacho-shuttered window per long face (4 windows total),
one lapacho door on the south short face, two-beam lapacho porch with 90 cm
overhang extension over a flagstone-paved entry.

v1 keeps the language single-room and rustic. v2 widens to ~70 m² and adds
a side loggia; per the project plan we factor ``lqv/house/stone_wall.py`` on
the second use, not the first. As of v2 we route the shared primitives —
foundation course, gable roof, chimney — through ``lqv.house.stone_wall`` so
both typologies converge on a single source of truth for the stone-cottage
vocabulary. Bay-specific geometry (4-window grid, 3×2 paving) stays inline.

Procedural primitives only — scaled cubes for walls + foundation + shutters,
verts/faces gable mesh for the roof, cuboid voids placed inside window
openings as glass quads (boolean diff would invalidate the byte-identity
contract on the sister composite, so we instead inset glass panes a few cm
behind the wall face — visually equivalent at the 3/4-front hero camera).
"""
from __future__ import annotations

import math

import bpy

from lqv.furniture import furnish_interior
from lqv.house import stone_wall
from lqv.materials import MAT, assign

FOOTPRINT_M2 = 20.0           # 5 m × 4 m
PLATFORM_W = 5.0              # x (long edge — gable runs along x → gables E/W)
PLATFORM_L = 4.0              # y (short edge — door faces -Y / south)
SLEEPS = 2
STORY_HEIGHT_M = 2.6
WALL_HEIGHT_M = 2.6
ROOF_TYPE = 'terracotta_tile_gabled'
ROOF_PITCH_DEG = 25.0
ORIENTATION = 'door_faces_south'
SNAP = 'pad'
PAD_SIZE_M = 1.6

# Rule 4: 60 cm stone foundation course under the cob/stone walls.
_FOUNDATION_HEIGHT = 0.6
_FOUNDATION_THICKNESS = 0.40
_WALL_THICKNESS = 0.30
_ROOF_EAVE_OVERHANG = 0.9     # Rule 5: 90 cm overhangs
_ROOF_THICKNESS = 0.10
_WINDOW_W = 1.0
_WINDOW_H = 1.0
_DOOR_W = 0.9
_DOOR_H = 2.1
_SHUTTER_W = 0.55
_SHUTTER_H = 1.05
_PORCH_BEAM_R = 0.09
_PORCH_FORWARD = 2.5
_PORCH_OVERHANG_EXT = 0.9
_PAVING_W = 2.0
_PAVING_L = 3.0

NOTES = (
    'Single-room 2-pax stone cottage, ~20 m² interior.',
    'Sandstone walls with visible mortar; 60 cm stone foundation course (Rule 4).',
    'Low-pitch (25°) terracotta-tile gable roof; 90 cm eaves on long sides (Rule 5).',
    '4 windows (one per long-face bay × 2 bays), each 1.0 m × 1.0 m, lapacho shutters.',
    'Single lapacho door on the south short face; flagstone-paved entry apron.',
    '2-beam lapacho porch, 2.5 m forward of the door, supporting a 90 cm overhang ext.',
    'Passive ≤ 35 °C: 30 cm stone walls + thermal mass + cross-vent; no AC.',
    'v2 (sister typology) widens to ~70 m² and adds a side loggia.',
)

# Per-unit costs are Paraguay 2026 estimates carried from the sister river
# house typology. Targeted total falls in the $8 000–$11 000 USD band — about
# half the river-house build cost because the footprint is roughly halved and
# there's no second storey, no arched foundation, no loggia, no dock.
MATERIAL_TAKEOFF: dict = {
    'stone_walls': {
        # 4 walls × ~30 cm thick × 2.6 m tall × ~18 m perimeter, less ~15 % for openings.
        'volume_m3': 14.0,
        'unit_cost_usd': 285.0,
    },
    'terracotta_tile_roof': {
        # Gabled at 25° over 5×4 footprint + 0.9 m overhang per side ≈ 30 m² covered.
        'area_m2': 30.0,
        'unit_cost_usd': 42.0,
    },
    'lapacho_shutters_doors': {
        # 4 windows × 2 shutter leaves + 1 entry door ≈ 8 m² of finished joinery.
        'area_m2': 8.0,
        'unit_cost_usd': 165.0,
    },
    'lapacho_beams_porch': {
        # 2 porch beams + ridge purlin + intermediate purlins, all lapacho heartwood.
        'volume_m3': 0.3,
        'unit_cost_usd': 1450.0,
    },
    'stone_foundation': {
        # 60 cm course × ~40 cm thick × ~18 m perimeter (Rule 4).
        'volume_m3': 3.0,
        'unit_cost_usd': 310.0,
    },
    'glass_glazing': {
        # 4 windows × 1.0 m² double-pane glazing.
        'area_m2': 4.0,
        'unit_cost_usd': 240.0,
    },
    'fasteners': {
        # Steel anchors, lag bolts, brackets, copper flashings.
        'count': 250,
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


def _foundation(col, ox, oy):
    """60 cm stone foundation course — Rule 4. Slightly proud of wall plan to
    read as a course rather than as the wall continuing into the ground.

    Routed through the shared ``stone_wall.build_stone_foundation_course``
    primitive — identical geometry (same +0.20 m proud-of-walls inflation)
    so the output is byte-equivalent to the inlined original.
    """
    obj = stone_wall.build_stone_foundation_course(
        x=ox, y=oy,
        width_m=PLATFORM_W, depth_m=PLATFORM_L,
        height_m=_FOUNDATION_HEIGHT,
        name='ISS1_FoundationPad',
        collection=col,
    )
    return obj


def _walls(col, ox, oy):
    """4 rectangular sandstone walls sitting on the foundation course.

    Walls are 30 cm thick × 2.6 m tall. Material is ``sandstone`` (which
    already has visible mortar grain via its noise displacement at scale=24).
    Rule 1's "no right angles" applies to the cob house, not to this Italian
    typology — sandstone masonry is rectilinear by construction.
    """
    stone = _mat('sandstone', 'stone_wall', 'limestone')
    z0 = _FOUNDATION_HEIGHT
    z_mid = z0 + WALL_HEIGHT_M / 2.0
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
        _cube(col, f'ISS1_Wall_{tag}', (x, y, zc), (sx, sy, sz), stone)

    # Triangular gable infill on the short axis (E/W) — ridge runs along x,
    # so the W and E walls rise to a peak above the eave line.
    pitch_rad = math.radians(ROOF_PITCH_DEG)
    eave_z = z0 + WALL_HEIGHT_M
    ridge_z = eave_z + math.tan(pitch_rad) * (PLATFORM_L / 2)
    for sign, suffix in ((-1, 'W'), (1, 'E')):
        x = ox + sign * (PLATFORM_W / 2 - _WALL_THICKNESS / 2)
        stone_wall.build_gable_triangle(
            x=x,
            y_min=oy - PLATFORM_L / 2,
            y_max=oy + PLATFORM_L / 2,
            eave_z=eave_z, ridge_z=ridge_z,
            name=f'ISS1_Gable_{suffix}',
            collection=col,
        )


def _roof(col, ox, oy):
    """Low-pitch terracotta-tile gable roof, 90 cm eaves on long sides.

    Routed through ``stone_wall.build_terracotta_gable_roof`` — same six
    vertices, same four faces (two quads + two gable triangles).
    """
    pitch_rad = math.radians(ROOF_PITCH_DEG)
    eave_z = _FOUNDATION_HEIGHT + WALL_HEIGHT_M
    obj = stone_wall.build_terracotta_gable_roof(
        footprint_corners=(
            (ox - PLATFORM_W / 2, oy - PLATFORM_L / 2),
            (ox + PLATFORM_W / 2, oy + PLATFORM_L / 2),
        ),
        ridge_axis='x',
        pitch_rad=pitch_rad,
        overhang_m=_ROOF_EAVE_OVERHANG,
        gable_overhang_m=0.20,
        eave_z=eave_z,
        name='ISS1_Roof',
        collection=col,
    )
    return obj


def _windows_and_glazing(col, ox, oy):
    """One window per bay on each long face — 2 bays per long face → 4 windows.

    Glazing is inset 4 cm behind the exterior wall face. Shutters bracket the
    glass on the outside. We do NOT boolean-diff the wall (would risk the
    byte-identity contract on the composite reuse path); the inset glass +
    shutter combination reads as a window at the hero camera distance.
    """
    timber = _mat('lapacho_timber')
    glass = _mat('water_reflective', 'glass_bottle_cobalt')
    z0 = _FOUNDATION_HEIGHT
    win_cz = z0 + 1.35      # window centre height
    bay_offsets = (-1.2, 1.2)  # 2 bays per long face, symmetric around centre

    for face_sign, tag in ((-1, 'S'), (1, 'N')):
        glass_y = oy + face_sign * (PLATFORM_L / 2 - _WALL_THICKNESS - 0.04)
        shutter_y = oy + face_sign * (PLATFORM_L / 2 + 0.02)
        for bay_i, sx in enumerate(bay_offsets):
            # Glass pane inset behind the wall.
            if glass is not None:
                _cube(
                    col, f'ISS1_Glass_{tag}_{bay_i}',
                    location=(ox + sx, glass_y, win_cz),
                    scale=(_WINDOW_W, 0.04, _WINDOW_H),
                    mat=glass,
                )
            # 2 shutter leaves per window.
            for leaf_i, off in enumerate(
                (-_WINDOW_W / 2 - _SHUTTER_W / 2 - 0.02,
                  _WINDOW_W / 2 + _SHUTTER_W / 2 + 0.02)
            ):
                _cube(
                    col, f'ISS1_Shutter_{tag}_{bay_i}_{leaf_i}',
                    location=(ox + sx + off, shutter_y, win_cz),
                    scale=(_SHUTTER_W, 0.04, _SHUTTER_H),
                    mat=timber,
                )
            # Lintel + sill (lapacho beam) reads as window framing.
            for dz, suf in ((-_WINDOW_H / 2 - 0.06, 'sill'),
                            (_WINDOW_H / 2 + 0.06, 'lintel')):
                _cube(
                    col, f'ISS1_WinTrim_{tag}_{bay_i}_{suf}',
                    location=(ox + sx, shutter_y, win_cz + dz),
                    scale=(_WINDOW_W + 0.30, 0.10, 0.10),
                    mat=timber,
                )

    # Side walls (W/E short faces) — no windows in v1 spec; only the front door
    # punctuates the south face below.


def _door_and_paving(col, ox, oy):
    """Lapacho door on the south face + 3×2 m flagstone-paved entry apron.

    The door faces -Y (south). With the subscene camera at (+10, -10, 4) the
    south face is in clear view of the hero shot.
    """
    timber = _mat('lapacho_timber')
    # ``flagstone`` is not in MAT; closest visual analog is ``sandstone``
    # (warm masonry tone) or ``laterite`` (warmer, gravel-like apron). We
    # pick sandstone so the paving reads as cut stone, not gravel.
    paving = _mat('sandstone', 'laterite', 'stone_wall')
    z0 = _FOUNDATION_HEIGHT
    door_cz = z0 + _DOOR_H / 2.0

    # Door slab — sits in the centre of the south face.
    _cube(
        col, 'ISS1_Door',
        location=(ox, oy - PLATFORM_L / 2 - 0.03, door_cz),
        scale=(_DOOR_W, 0.06, _DOOR_H),
        mat=timber,
    )
    # Door lintel + jambs (lapacho framing).
    _cube(
        col, 'ISS1_DoorLintel',
        location=(ox, oy - PLATFORM_L / 2 - 0.04, z0 + _DOOR_H + 0.08),
        scale=(_DOOR_W + 0.30, 0.10, 0.12),
        mat=timber,
    )
    for sign in (-1, 1):
        _cube(
            col, f'ISS1_DoorJamb_{"L" if sign < 0 else "R"}',
            location=(ox + sign * (_DOOR_W / 2 + 0.06),
                      oy - PLATFORM_L / 2 - 0.04, z0 + _DOOR_H / 2.0),
            scale=(0.10, 0.10, _DOOR_H + 0.10),
            mat=timber,
        )

    # 3×2 m flagstone-paved entry apron — sitting at ground level just south
    # of the door. We sub-divide into a 3×2 grid of slabs so it reads as paving.
    apron_cy = oy - PLATFORM_L / 2 - _PAVING_L / 2 - 0.10
    n_cols, n_rows = 3, 2
    slab_w = _PAVING_W / n_cols
    slab_l = _PAVING_L / n_rows
    for i in range(n_cols):
        for j in range(n_rows):
            cx = ox - _PAVING_W / 2 + (i + 0.5) * slab_w
            cy = apron_cy - _PAVING_L / 2 + (j + 0.5) * slab_l
            _cube(
                col, f'ISS1_Paving_{i}_{j}',
                location=(cx, cy, 0.04),
                scale=(slab_w * 0.94, slab_l * 0.94, 0.08),
                mat=paving,
            )


def _porch(col, ox, oy):
    """2-beam lapacho porch, 2.5 m forward of the door, supporting a 90 cm
    overhang extension over the entry."""
    timber = _mat('lapacho_timber')
    tile = _mat('terracotta_tile', 'clay_tile', 'laterite')
    z0 = _FOUNDATION_HEIGHT

    # Two vertical lapacho posts, 2.0 m apart (matches the door width band),
    # placed _PORCH_FORWARD south of the south wall face.
    post_y = oy - PLATFORM_L / 2 - _PORCH_FORWARD
    post_h = WALL_HEIGHT_M - 0.10
    for sign in (-1, 1):
        _cylinder(
            col, f'ISS1_PorchPost_{"L" if sign < 0 else "R"}',
            location=(ox + sign * 1.0, post_y, z0 + post_h / 2.0),
            radius=_PORCH_BEAM_R, depth=post_h, mat=timber,
        )
    # Horizontal beam tying the two posts (visual lintel of the porch).
    _cube(
        col, 'ISS1_PorchBeam',
        location=(ox, post_y, z0 + post_h + 0.05),
        scale=(2.2, 0.14, 0.16),
        mat=timber,
    )
    # Lean-to tile extension covering the porch (slopes from the south eave
    # of the main roof down to the porch beam).
    pitch_rad = math.radians(ROOF_PITCH_DEG)
    eave_inner_z = z0 + WALL_HEIGHT_M + math.tan(pitch_rad) * _ROOF_EAVE_OVERHANG
    eave_outer_z = z0 + post_h + 0.12
    verts = [
        (ox - PLATFORM_W / 2 - 0.20, oy - PLATFORM_L / 2 - _ROOF_EAVE_OVERHANG, eave_inner_z),
        (ox + PLATFORM_W / 2 + 0.20, oy - PLATFORM_L / 2 - _ROOF_EAVE_OVERHANG, eave_inner_z),
        (ox + PLATFORM_W / 2 + 0.20, post_y + 0.10, eave_outer_z),
        (ox - PLATFORM_W / 2 - 0.20, post_y + 0.10, eave_outer_z),
    ]
    faces = [(0, 1, 2, 3)]
    mesh = bpy.data.meshes.new('ISS1_PorchRoof_Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new('ISS1_PorchRoof', mesh)
    if tile is not None:
        assign(obj, tile)
    col.objects.link(obj)


def _chimney(col, ox, oy):
    """Small stone chimney on the east gable for stove venting.

    Routed through ``stone_wall.build_chimney`` — same shaft + cap geometry,
    same sandstone material; we anchor by the top centre at the original
    ridge_z + 0.9 m height.
    """
    pitch_rad = math.radians(ROOF_PITCH_DEG)
    ridge_z = _FOUNDATION_HEIGHT + WALL_HEIGHT_M + math.tan(pitch_rad) * (PLATFORM_L / 2)
    top_z = ridge_z + 0.9
    cx = ox + PLATFORM_W / 2 - 0.6
    cy = oy
    base_z = _FOUNDATION_HEIGHT + WALL_HEIGHT_M * 0.4
    height = top_z - base_z
    stone_wall.build_chimney(
        top_xyz=(cx, cy, top_z),
        width_m=0.45,
        height_m=height,
        material='sandstone',
        name='ISS1_Chimney',
        collection=col,
        with_cap=True,
    )


def build_italian_stone_small_v1(origin=(0.0, 0.0, 0.0), variant: str = 'A'):
    """Build the Italian Stone Small v1 cottage at ``origin``.

    Returns the parent collection. Idempotent across re-invocation.
    """
    name = 'ItalianStoneSmall_v1'
    col = _ensure_collection(name, None)
    ox, oy, _oz = origin
    _foundation(col, ox, oy)
    _walls(col, ox, oy)
    _roof(col, ox, oy)
    _windows_and_glazing(col, ox, oy)
    _door_and_paving(col, ox, oy)
    _porch(col, ox, oy)
    _chimney(col, ox, oy)

    # P1.B.1 — interior furniture stubs (RENDER_VIEW=interior readable).
    # Single-room cottage; floor sits atop foundation course; margin from
    # wall face = ~0.4 m so the bed clears the shutters.
    furnish_interior(
        col,
        footprint_w=PLATFORM_W - 0.8,
        footprint_l=PLATFORM_L - 0.8,
        origin_xy=(ox, oy),
        floor_z=_FOUNDATION_HEIGHT,
        pax=SLEEPS,
        style='stone',
        variant=variant,
        name_prefix='ISSv1_Furn',
    )

    return col


# Backward-compat shim: older drivers (subscene + composite) call ``build(...)``.
def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    col = build_italian_stone_small_v1(origin=location, variant=variant)
    if parent is not None and col.name not in [c.name for c in parent.children]:
        bpy.context.scene.collection.children.unlink(col)
        parent.children.link(col)
    return col
