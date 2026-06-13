"""Typology — Hobbit House (earth-bermed half-buried dwelling).

~6 m round footprint, ~3 m interior crown, half-dome cob shell embedded into a
slight hill. Round lapacho-disc front door, one round oeil-de-boeuf window,
green-roof berm with anthuriums + tree ferns, stone foundation course at the
front entry (Rule 4), exposed lapacho post visible through the door cut, small
lapacho front porch with two round-bench seats.

MAT keys are resolved via fallback chains because the registry doesn't carry
``cob_walls`` / ``stone_foundation`` / ``glass_glazing`` as first-class entries
yet — we walk to the nearest shipped material (``cob_raw``, ``sandstone``,
``pv_glass``). No new MAT keys are added (would force a re-render of the 18
finals at 85e86aa).

Rules carried: 1 (no right angles in cob — all UV-sphere + cylinder forms),
2 (no cement plaster — cob_raw lime-washable surface), 4 (stone foundation
course at the south door, 60 cm tall), 5 (the berm itself reads as wide
overhang on N/E/W), 8 (lapacho timber for door + porch).
"""
from __future__ import annotations

import math

import bpy

from lqv.materials import MAT, assign

# --- Geometry constants ----------------------------------------------------
DIAMETER_M = 6.0
RADIUS_M = DIAMETER_M / 2.0
WALL_HEIGHT_M = 2.2
CROWN_HEIGHT_M = 3.0          # interior crown
DOME_SEGMENTS = 32
DOME_RINGS = 16

# Foundation course at the front entry (Rule 4 — walls off ground).
FOUNDATION_H = 0.6
FOUNDATION_R = RADIUS_M + 0.12

# Berm — scaled UV sphere wrapped around the back of the dome.
BERM_RADIUS = RADIUS_M + 1.6
BERM_HEIGHT = CROWN_HEIGHT_M + 0.4
BERM_OFFSET_Y = RADIUS_M * 0.6   # push centre toward +Y (away from door)

# Round front door.
DOOR_RADIUS = 0.5             # 1.0 m diameter
DOOR_THK = 0.06
DOOR_FRAME_THK = 0.08

# Oeil-de-boeuf round window flanking the door.
WINDOW_RADIUS = 0.25
WINDOW_THK = 0.04
WINDOW_OFFSET_X = 1.6         # to the east of the door
WINDOW_Z = 1.6

# Lapacho post visible through the door (interior frame hint).
POST_RADIUS = 0.10
POST_HEIGHT = CROWN_HEIGHT_M

# Porch deck (lapacho boards).
PORCH_L = 4.0                 # along X (east-west)
PORCH_W = 2.0                 # along Y (south, in front of door)
PORCH_THK = 0.10
PORCH_Z_OFFSET = FOUNDATION_H + 0.02

# Round bench seats on the porch.
BENCH_RADIUS = 0.30
BENCH_HEIGHT = 0.42

FOOTPRINT_M2 = math.pi * RADIUS_M ** 2
SLEEPS = 2
ORIENTATION = 'door_south'
SNAP = 'cut'

NOTES = (
    'Half-buried cob dome — UV sphere booleaned by ground plane (Rule 1).',
    'Stone foundation ring at the front entry — 60 cm course (Rule 4).',
    'Green roof / berm tinted sod_canopy with scattered anthuriums + tree fern.',
    'Round lapacho door + flanking oeil-de-boeuf window (CC0 species accurate).',
    'No standing water inside (Rule 3); door-mosquito mesh implied at frame.',
)

# Cob wall annular volume (outer minus inner shell), used in takeoff below.
_COB_VOL = (math.pi * (RADIUS_M ** 2 - (RADIUS_M - 0.3) ** 2) * WALL_HEIGHT_M
            + (2.0 / 3.0) * math.pi * (RADIUS_M ** 3 - (RADIUS_M - 0.3) ** 3) * 0.5)

MATERIAL_TAKEOFF: dict = {
    # Cob shell — walls + dome inner skin. PY 2026 unit cost is ~$95/m3
    # delivered on-site cob (clay + sand + chopped fibre).
    'cob_walls': {
        'volume_m3': round(_COB_VOL, 2),
        'unit_cost_usd': 95.0,
    },
    # Stone foundation course at the entry (Rule 4). Sandstone fallback.
    'stone_foundation': {
        'volume_m3': round(math.pi * (FOUNDATION_R ** 2
                                       - (FOUNDATION_R - 0.25) ** 2)
                            * FOUNDATION_H, 2),
        'unit_cost_usd': 140.0,
    },
    # Lapacho timber — porch deck + door + interior post + bench seats.
    'lapacho_timber': {
        'volume_m3': round(PORCH_L * PORCH_W * PORCH_THK
                           + math.pi * (DOOR_RADIUS ** 2) * DOOR_THK
                           + math.pi * (POST_RADIUS ** 2) * POST_HEIGHT
                           + 2.0 * math.pi * (BENCH_RADIUS ** 2) * BENCH_HEIGHT, 3),
        'unit_cost_usd': 1450.0,        # premium hardwood, ~$1450/m3 delivered
    },
    # Green-roof living surface — grass / sod over the dome + berm.
    'sod_roof_grass': {
        'area_m2': round(2.0 * math.pi * RADIUS_M ** 2
                          + math.pi * BERM_RADIUS ** 2 * 0.5, 1),
        'unit_cost_usd': 18.0,
    },
    # Glass glazing — round window pane.
    'glass_glazing': {
        'area_m2': round(math.pi * WINDOW_RADIUS ** 2, 3),
        'unit_cost_usd': 240.0,
    },
    # Round lapacho front door — counted as a unit (hardware + handle + frame).
    'lapacho_round_door': {
        'count': 1,
        'unit_cost_usd': 520.0,
    },
    # Fasteners + ironmongery + porch bolts.
    'fasteners_misc': {
        'count': 180,
        'unit_cost_usd': 1.4,
    },
    # Mosquito mesh at door frame + window vent (Rule 10 carried to openings).
    'stainless_mosquito_mesh': {
        'area_m2': 1.4,
        'unit_cost_usd': 22.0,
    },
}


def _resolve(*keys):
    """Material-key fallback chain. Warns on fallback, raises on full miss.

    Old behaviour returned ``None`` and the caller had to check — half
    the callsites in this file didn't, and shipped principled-white where
    a cob wall should have been. Now: first hit returns silently, any
    later hit prints a warning so the materials team sees the slack, and
    if nothing matches we raise ``KeyError`` listing the chain.
    """
    for i, k in enumerate(keys):
        m = MAT.get(k)
        if m is not None:
            if i > 0:
                import sys
                print(
                    f"[lqv.typologies.hobbit_house] WARN material {keys[0]!r} "
                    f"missing; fell back to {k!r} "
                    f"(chain tried: {list(keys[:i + 1])}).",
                    file=sys.stderr,
                )
            return m
    raise KeyError(
        f"none of the materials in fallback chain {list(keys)} were registered; "
        f"available keys: {sorted(MAT.keys())}"
    )


def _ensure_collection(name: str,
                       parent: bpy.types.Collection | None) -> bpy.types.Collection:
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(col)
    return col


def _link(obj: bpy.types.Object, col: bpy.types.Collection) -> None:
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def _apply_modifier(obj: bpy.types.Object, modifier_name: str) -> None:
    """Apply a modifier in headless-safe fashion.

    Uses ``bpy.context.temp_override`` to feed the operator the right
    active+selected object explicitly (the headless context has no
    active area/region by default, which is what historically caused
    ``RuntimeError: Operator bpy.ops.object.modifier_apply.poll() failed``).
    The previous ``try: ... except RuntimeError: pass`` silently shipped
    cob domes with the boolean cutter mesh still attached as a modifier
    stack entry — usually invisible at the hero camera but it polluted
    the export pipeline and added scene-graph overhead.

    Any real failure (e.g. boolean solver crash) propagates so the build
    log surfaces it instead of producing a quietly-wrong dome.
    """
    win = bpy.context.window or (bpy.context.window_manager.windows[0]
                                 if bpy.context.window_manager.windows else None)
    # Pick a fallback area if none is active (common in --background).
    area = bpy.context.area
    region = bpy.context.region
    if win is not None and (area is None or region is None):
        for a in win.screen.areas:
            if a.type == 'VIEW_3D':
                area = a
                for r in a.regions:
                    if r.type == 'WINDOW':
                        region = r
                        break
                break

    override = {
        'object': obj,
        'active_object': obj,
        'selected_objects': [obj],
        'selected_editable_objects': [obj],
    }
    if win is not None:
        override['window'] = win
        override['screen'] = win.screen
    if area is not None:
        override['area'] = area
    if region is not None:
        override['region'] = region

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    with bpy.context.temp_override(**override):
        bpy.ops.object.modifier_apply(modifier=modifier_name)


def _half_dome(col, name, ox, oy, oz, radius, height, mat):
    """UV sphere booleaned flat at z=oz (lower half cut off).

    Implemented as a scaled sphere placed so its equator sits at z=oz, then
    bool-cut by a wide plane. Cheap + Cycles-friendly.
    """
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius,
        location=(ox, oy, oz),
        segments=DOME_SEGMENTS,
        ring_count=DOME_RINGS,
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (1.0, 1.0, height / radius)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_smooth()
    # Boolean cut the lower half via a flat cutter plane.
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(ox, oy, oz - radius),
    )
    cutter = bpy.context.active_object
    cutter.name = f'{name}_Cutter'
    cutter.scale = (radius * 4.0, radius * 4.0, radius * 2.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = obj.modifiers.new(name='HalfCut', type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    # Apply the modifier so the cutter can be discarded. In headless mode
    # the default context can be wrong (no active area/region) — we use
    # ``temp_override`` to feed modifier_apply the right object explicitly
    # rather than swallowing the RuntimeError and shipping a render that
    # silently includes the cutter mesh. Any real failure (e.g. the
    # boolean solver can't resolve the geometry) re-raises so the build
    # log surfaces it instead of producing a quietly-wrong dome.
    _apply_modifier(obj, 'HalfCut')
    # Drop the cutter from any visible collection.
    for c in list(cutter.users_collection):
        c.objects.unlink(cutter)
    cutter.hide_render = True
    cutter.hide_viewport = True
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _cyl(col, name, location, radius, depth, mat, vertices=24,
         rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, vertices=vertices,
    )
    obj = bpy.context.active_object
    obj.name = name
    if rotation != (0.0, 0.0, 0.0):
        obj.rotation_euler = rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


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


def build_hobbit_house(origin=(0.0, 0.0, 0.0), parent=None):
    """Build the Hobbit House typology at ``origin``. Returns the collection."""
    ox, oy, oz = origin
    col = _ensure_collection('HobbitHouse', parent)

    cob = _resolve('cob_raw', 'laterite')
    stone = _resolve('sandstone', 'laterite')
    lapacho = _resolve('lapacho_timber', 'lapacho_bark')
    sod = _resolve('sod_canopy', 'moss', 'canopy')
    berm_mat = _resolve('laterite', 'moss')
    glass = _resolve('pv_glass', 'window_glow')
    bench_mat = _resolve('lapacho_timber', 'sandstone')

    # --- Stone foundation course at the south entry (Rule 4) ---------------
    # Ring of stone ~60 cm tall, only modelled as the visible front arc; in
    # the back it disappears into the berm anyway.
    _cyl(col, 'HH_Foundation',
         (ox, oy, oz + FOUNDATION_H / 2.0),
         FOUNDATION_R, FOUNDATION_H, stone, vertices=DOME_SEGMENTS)

    # --- Half-dome cob shell ----------------------------------------------
    # Sit dome on top of the foundation course so walls don't touch ground.
    _half_dome(col, 'HH_Dome',
               ox, oy, oz + FOUNDATION_H,
               RADIUS_M, CROWN_HEIGHT_M, cob)

    # --- Green-roof tint shell (slightly offset above the cob dome) -------
    # Thin overlay sphere reads as the planted sod over the cob.
    sod_obj = _half_dome(col, 'HH_GreenRoof',
                         ox, oy, oz + FOUNDATION_H + 0.04,
                         RADIUS_M + 0.03, CROWN_HEIGHT_M + 0.04, sod)
    sod_obj.hide_render = False

    # --- Earth berm wrapping the back / sides of the dome -----------------
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=BERM_RADIUS,
        location=(ox, oy + BERM_OFFSET_Y, oz),
        segments=DOME_SEGMENTS,
        ring_count=DOME_RINGS,
    )
    berm = bpy.context.active_object
    berm.name = 'HH_Berm'
    berm.scale = (1.0, 1.25, BERM_HEIGHT / BERM_RADIUS)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_smooth()
    # Cut its lower half too.
    bpy.ops.mesh.primitive_cube_add(size=1.0,
                                    location=(ox, oy + BERM_OFFSET_Y,
                                              oz - BERM_RADIUS))
    cutter = bpy.context.active_object
    cutter.scale = (BERM_RADIUS * 6.0, BERM_RADIUS * 6.0, BERM_RADIUS * 2.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = berm.modifiers.new(name='BermHalfCut', type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    _apply_modifier(berm, 'BermHalfCut')
    for c in list(cutter.users_collection):
        c.objects.unlink(cutter)
    cutter.hide_render = True
    cutter.hide_viewport = True
    if berm_mat is not None:
        assign(berm, berm_mat)
    _link(berm, col)

    # --- Round door (lapacho disc) ----------------------------------------
    # Sits flush on the south face of the dome, centred on the cob equator.
    door_y = oy - RADIUS_M - 0.02
    door_z = oz + FOUNDATION_H + DOOR_RADIUS + 0.05
    _cyl(col, 'HH_Door',
         (ox, door_y, door_z),
         DOOR_RADIUS, DOOR_THK, lapacho, vertices=32,
         rotation=(math.radians(90.0), 0.0, 0.0))
    # Door frame ring — thin lapacho band around the disc.
    _cyl(col, 'HH_DoorFrame',
         (ox, door_y - 0.005, door_z),
         DOOR_RADIUS + 0.04, DOOR_FRAME_THK, lapacho, vertices=48,
         rotation=(math.radians(90.0), 0.0, 0.0))
    # Door handle (small lapacho knob).
    _cyl(col, 'HH_DoorHandle',
         (ox + DOOR_RADIUS * 0.55, door_y - 0.06, door_z),
         0.04, 0.05, lapacho, vertices=12,
         rotation=(math.radians(90.0), 0.0, 0.0))

    # --- Round oeil-de-boeuf window (glass disc) --------------------------
    win_y = oy - RADIUS_M - 0.02 + 0.4  # tucked into curvature of the dome
    win_z = oz + FOUNDATION_H + WINDOW_Z
    win_x = ox + WINDOW_OFFSET_X
    _cyl(col, 'HH_Window',
         (win_x, win_y, win_z),
         WINDOW_RADIUS, WINDOW_THK, glass, vertices=32,
         rotation=(math.radians(90.0), 0.0, 0.0))
    _cyl(col, 'HH_WindowFrame',
         (win_x, win_y - 0.005, win_z),
         WINDOW_RADIUS + 0.05, 0.07, lapacho, vertices=32,
         rotation=(math.radians(90.0), 0.0, 0.0))

    # --- Interior lapacho post (visible through the door cut) -------------
    _cyl(col, 'HH_InteriorPost',
         (ox, oy + 0.6, oz + FOUNDATION_H + POST_HEIGHT / 2.0),
         POST_RADIUS, POST_HEIGHT, lapacho, vertices=16)

    # --- Front porch deck (lapacho boards) --------------------------------
    porch_y = oy - RADIUS_M - PORCH_W / 2.0 - 0.05
    _box(col, 'HH_PorchDeck',
         (ox, porch_y, oz + PORCH_Z_OFFSET),
         (PORCH_L, PORCH_W, PORCH_THK),
         lapacho)
    # Board grooves — 5 narrow inset strips along Y, purely cosmetic.
    for i in range(4):
        gx = ox - PORCH_L / 2.0 + (i + 1) * (PORCH_L / 5.0)
        _box(col, f'HH_PorchGroove_{i}',
             (gx, porch_y, oz + PORCH_Z_OFFSET + PORCH_THK / 2.0 + 0.002),
             (0.015, PORCH_W, 0.01),
             lapacho)

    # --- Round bench seats on the porch (2) -------------------------------
    bench_y = porch_y - PORCH_W / 2.0 + BENCH_RADIUS + 0.15
    for side, dx in enumerate((-PORCH_L / 2.0 + BENCH_RADIUS + 0.25,
                                PORCH_L / 2.0 - BENCH_RADIUS - 0.25)):
        _cyl(col, f'HH_Bench_{side}',
             (ox + dx, bench_y,
              oz + PORCH_Z_OFFSET + PORCH_THK / 2.0 + BENCH_HEIGHT / 2.0),
             BENCH_RADIUS, BENCH_HEIGHT, bench_mat, vertices=24)

    # --- Stone foundation visible band at the south doorway (Rule 4 read) --
    # A short stone course in front of the door so the foundation reads in
    # the hero camera angle.
    _box(col, 'HH_EntrySill',
         (ox, oy - RADIUS_M + 0.05, oz + FOUNDATION_H + 0.02),
         (1.4, 0.18, 0.06),
         stone)

    return col


# Legacy alias — preserved so the existing subscene driver `_build()` path
# (and TYPOLOGIES discovery) keeps working without changes.
def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    return build_hobbit_house(origin=location, parent=parent)
