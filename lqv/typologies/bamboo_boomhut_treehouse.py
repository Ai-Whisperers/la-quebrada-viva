"""Typology — Bamboo Boomhut Treehouse.

Dutch "boomhut" hexagonal bamboo treehouse hosted by 3 lapacho trees. 2 PAX.
Hex platform 3.2 m flat-to-flat at z=4.0 m, bamboo-frame walls 2.4 m, conical
thatch roof, north glass window, mosquito mesh on all openings, spiral stair
wrapped around host trunk #1 (40 turns, helical), suspended bamboo bridge
~5 m to a stair tower trunk, solar PV box on railing.

P0.8 lesson: spiral stair treads must wrap a physical trunk cylinder, never
float in space. Here the stair is a helix anchored to host trunk #1.
"""
from __future__ import annotations

import math

import bpy

from lqv.materials import MAT, assign

# ----- public sizing constants used by SCATTERED CONSUMERS -----
FOOTPRINT_M2 = 8.3                  # hex 3.2 m flat-to-flat ≈ 8.3 m²
PLATFORM_FLAT_TO_FLAT = 3.2
WALL_HEIGHT_M = 2.4
ROOF_TYPE = 'palm_thatch_conical'
ROOF_PITCH_DEG = 45.0
ELEVATION_M = 4.0                   # platform above grade
SPECIES = 'guadua_angustifolia'
SNAP = 'host_trees'                 # 3 lapacho trunks act as stilts
NOTES = (
    'Three host lapacho trunks (~40 cm diameter) substitute for stilts.',
    'Hex bamboo platform 3.2 m flat-to-flat at z=4 m; bamboo-culm wall frame.',
    'Conical pindo-palm thatch roof, 45° pitch.',
    'North glass-panel window for vista; mosquito mesh on every opening.',
    'Spiral stair: 40 lapacho treads wrapping host trunk #1, 9° per tread, 4 m rise.',
    'Suspended bamboo bridge ~5 m from stair top to platform — paired rope catenary + 8 deck planks.',
    'Solar PV box on south railing edge — Rule 7 outage-proof.',
)

# Geometry helpers
_HEX_RADIUS = PLATFORM_FLAT_TO_FLAT / math.sqrt(3.0)   # vertex-to-vertex radius
_HOST_TRUNK_RADIUS = 0.20                              # 40 cm diameter
_HOST_TRUNK_HEIGHT = 12.0                              # canopy stub above platform
_PLATFORM_THICKNESS = 0.20
_RAIL_HEIGHT = 1.05
_CULM_RADIUS = 0.04                                    # 8 cm guadua culm
_THATCH_OVERHANG = 0.45
_STAIR_TREADS = 40
_STAIR_RADIUS = 0.45                                   # from trunk centerline
_BRIDGE_LENGTH = 5.0
_BRIDGE_PLANKS = 8

# Host trunk anchor positions around origin
_HOST_TRUNK_POSITIONS = [
    (1.80, 0.0),                                       # trunk #1 — stair host
    (-0.90, 1.56),                                     # trunk #2
    (-0.90, -1.56),                                    # trunk #3
]

# Stair tower trunk — independent lapacho trunk hosting the spiral, sits ~5 m
# south-east of platform so the suspended bridge has a real anchor point.
_STAIR_TOWER_XY = (6.5, -2.0)

MATERIAL_TAKEOFF: dict = {
    'bamboo_culm': {'length_m': 180.0, 'unit_cost_usd': 6.0},
    'palm_thatch': {'area_m2': 22.0, 'unit_cost_usd': 22.0},
    'lapacho_deck_planks': {'volume_m3': 0.5, 'unit_cost_usd': 1800.0},
    'lapacho_railing_stair': {'volume_m3': 0.4, 'unit_cost_usd': 1800.0},
    'rope_hemp': {'length_m': 60.0, 'unit_cost_usd': 3.5},
    'mosquito_mesh': {'area_m2': 8.0, 'unit_cost_usd': 12.0},
    'solar_pv_panels': {'count': 2, 'unit_cost_usd': 180.0},
    'fasteners_hardware': {'count': 350, 'unit_cost_usd': 0.80},
}


def _ensure_collection(name: str, parent) -> bpy.types.Collection:
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(col)
    return col


def _link(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def _mat(key, fallback=None):
    m = MAT.get(key)
    if m is None and fallback is not None:
        m = MAT.get(fallback)
    return m


def _add_host_trunk(col, x, y, name):
    """Single lapacho host trunk — cylinder representing real tree."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=_HOST_TRUNK_RADIUS,
        depth=_HOST_TRUNK_HEIGHT,
        location=(x, y, _HOST_TRUNK_HEIGHT / 2.0),
    )
    obj = bpy.context.active_object
    obj.name = name
    mat = _mat('lapacho_bark', 'lapacho_timber')
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _hex_platform(col, ox, oy, oz):
    """6-vertex hex platform at z = oz, thickness _PLATFORM_THICKNESS."""
    verts = []
    for i in range(6):
        ang = math.radians(60 * i)
        verts.append((ox + _HEX_RADIUS * math.cos(ang),
                      oy + _HEX_RADIUS * math.sin(ang),
                      oz))
        verts.append((ox + _HEX_RADIUS * math.cos(ang),
                      oy + _HEX_RADIUS * math.sin(ang),
                      oz - _PLATFORM_THICKNESS))
    # Top face (even indices), bottom face (odd indices), side quads
    top = [i * 2 for i in range(6)]
    bot = [i * 2 + 1 for i in range(6)]
    faces = [tuple(top), tuple(reversed(bot))]
    for i in range(6):
        a = i * 2
        b = ((i + 1) % 6) * 2
        faces.append((a, b, b + 1, a + 1))
    mesh = bpy.data.meshes.new('BHT_HexPlatform_Mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new('BHT_HexPlatform', mesh)
    mat = _mat('lapacho_timber')
    if mat is not None:
        assign(obj, mat)
    col.objects.link(obj)


def _bamboo_wall_frame(col, ox, oy, deck_top_z):
    """Vertical bamboo culm posts at every hex vertex + horizontal ring at top.

    Leaves the north face open (deck-level vertex pair) — that's where the
    glass window goes. Mosquito mesh fills the remaining 5 bays.
    """
    mat = _mat('bamboo')
    top_z = deck_top_z + WALL_HEIGHT_M
    # Six corner posts
    for i in range(6):
        ang = math.radians(60 * i)
        x = ox + _HEX_RADIUS * math.cos(ang)
        y = oy + _HEX_RADIUS * math.sin(ang)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=_CULM_RADIUS,
            depth=WALL_HEIGHT_M,
            location=(x, y, deck_top_z + WALL_HEIGHT_M / 2.0),
        )
        post = bpy.context.active_object
        post.name = f'BHT_WallPost_{i}'
        if mat is not None:
            assign(post, mat)
        _link(post, col)
    # Top ring beam (6 segments)
    for i in range(6):
        a1 = math.radians(60 * i)
        a2 = math.radians(60 * (i + 1))
        x1 = ox + _HEX_RADIUS * math.cos(a1)
        y1 = oy + _HEX_RADIUS * math.sin(a1)
        x2 = ox + _HEX_RADIUS * math.cos(a2)
        y2 = oy + _HEX_RADIUS * math.sin(a2)
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        seg_len = math.hypot(x2 - x1, y2 - y1)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=_CULM_RADIUS,
            depth=seg_len,
            location=(mx, my, top_z),
        )
        beam = bpy.context.active_object
        beam.name = f'BHT_TopBeam_{i}'
        beam.rotation_euler = (math.pi / 2.0,
                               0.0,
                               math.atan2(y2 - y1, x2 - x1) + math.pi / 2.0)
        if mat is not None:
            assign(beam, mat)
        _link(beam, col)


def _mosquito_mesh_panels(col, ox, oy, deck_top_z):
    """Translucent mesh skin over 5 of 6 bays. Bay 1 (north) is left for glass."""
    mat = _mat('steel_mesh', 'palm_thatch')
    z_mid = deck_top_z + WALL_HEIGHT_M / 2.0
    for i in range(6):
        if i == 1:                    # leave the north-east-ish bay open for glass
            continue
        a1 = math.radians(60 * i)
        a2 = math.radians(60 * (i + 1))
        x1 = ox + _HEX_RADIUS * math.cos(a1)
        y1 = oy + _HEX_RADIUS * math.sin(a1)
        x2 = ox + _HEX_RADIUS * math.cos(a2)
        y2 = oy + _HEX_RADIUS * math.sin(a2)
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        bay_w = math.hypot(x2 - x1, y2 - y1)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(mx, my, z_mid))
        panel = bpy.context.active_object
        panel.name = f'BHT_MeshPanel_{i}'
        panel.scale = (bay_w * 0.92, 0.02, WALL_HEIGHT_M * 0.9)
        panel.rotation_euler = (0.0, 0.0, math.atan2(y2 - y1, x2 - x1))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        if mat is not None:
            assign(panel, mat)
        _link(panel, col)


def _glass_north_window(col, ox, oy, deck_top_z):
    """Bay 1 north window — clear glass panel for vista."""
    mat = _mat('glass_bottle_cobalt', 'water_reflective')
    a1 = math.radians(60 * 1)
    a2 = math.radians(60 * 2)
    x1 = ox + _HEX_RADIUS * math.cos(a1)
    y1 = oy + _HEX_RADIUS * math.sin(a1)
    x2 = ox + _HEX_RADIUS * math.cos(a2)
    y2 = oy + _HEX_RADIUS * math.sin(a2)
    mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    bay_w = math.hypot(x2 - x1, y2 - y1)
    bpy.ops.mesh.primitive_cube_add(
        size=1.0, location=(mx, my, deck_top_z + WALL_HEIGHT_M / 2.0))
    glass = bpy.context.active_object
    glass.name = 'BHT_NorthGlass'
    glass.scale = (bay_w * 0.9, 0.04, WALL_HEIGHT_M * 0.85)
    glass.rotation_euler = (0.0, 0.0, math.atan2(y2 - y1, x2 - x1))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if mat is not None:
        assign(glass, mat)
    _link(glass, col)


def _conical_thatch_roof(col, ox, oy, eave_z):
    """Cone primitive — thatch, 45° pitch, overhang past hex perimeter."""
    pitch_rad = math.radians(ROOF_PITCH_DEG)
    base_r = _HEX_RADIUS + _THATCH_OVERHANG
    apex_z = eave_z + math.tan(pitch_rad) * base_r
    bpy.ops.mesh.primitive_cone_add(
        vertices=24,
        radius1=base_r,
        radius2=0.0,
        depth=apex_z - eave_z,
        location=(ox, oy, (eave_z + apex_z) / 2.0),
    )
    roof = bpy.context.active_object
    roof.name = 'BHT_ThatchRoof'
    mat = _mat('palm_thatch')
    if mat is not None:
        assign(roof, mat)
    _link(roof, col)


def _perimeter_railing(col, ox, oy, deck_top_z):
    """4 lapacho cylinder rails — 2 around the hex perimeter at top + bottom."""
    mat = _mat('lapacho_timber')
    for rail_z in (deck_top_z + 0.15, deck_top_z + _RAIL_HEIGHT):
        for i in range(6):
            a1 = math.radians(60 * i)
            a2 = math.radians(60 * (i + 1))
            x1 = ox + _HEX_RADIUS * math.cos(a1)
            y1 = oy + _HEX_RADIUS * math.sin(a1)
            x2 = ox + _HEX_RADIUS * math.cos(a2)
            y2 = oy + _HEX_RADIUS * math.sin(a2)
            mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
            seg_len = math.hypot(x2 - x1, y2 - y1)
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.025, depth=seg_len, location=(mx, my, rail_z))
            rail = bpy.context.active_object
            rail.name = f'BHT_Rail_{i}_{rail_z:.2f}'
            rail.rotation_euler = (math.pi / 2.0,
                                   0.0,
                                   math.atan2(y2 - y1, x2 - x1) + math.pi / 2.0)
            if mat is not None:
                assign(rail, mat)
            _link(rail, col)


def _spiral_stair(col, trunk_x, trunk_y):
    """Helix of 40 cube treads physically wrapped around stair-tower trunk.

    P0.8 lesson: tread placement = (trunk_x + r·cos θ, trunk_y + r·sin θ,
    i·rise). r > _HOST_TRUNK_RADIUS so treads don't intersect the trunk core.
    """
    mat = _mat('lapacho_timber')
    tread_rise = ELEVATION_M / _STAIR_TREADS                 # 0.10 m per tread
    tread_arc = math.radians(9.0)                            # 9° per tread → 360°
    for i in range(_STAIR_TREADS):
        ang = i * tread_arc
        x = trunk_x + _STAIR_RADIUS * math.cos(ang)
        y = trunk_y + _STAIR_RADIUS * math.sin(ang)
        z = i * tread_rise + tread_rise / 2.0
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z))
        tread = bpy.context.active_object
        tread.name = f'BHT_StairTread_{i}'
        tread.scale = (0.55, 0.18, tread_rise * 0.9)
        tread.rotation_euler = (0.0, 0.0, ang + math.pi / 2.0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        if mat is not None:
            assign(tread, mat)
        _link(tread, col)


def _suspended_bridge(col, ox, oy, deck_top_z, tower_x, tower_y):
    """Paired rope catenary + 8 lapacho deck planks linking stair tower → platform.

    Anchor at platform edge (closest hex vertex to tower) and at top of stair
    tower. Two catenary ropes flank the deck.
    """
    mat_rope = _mat('rope_natural', 'bamboo')
    mat_wood = _mat('lapacho_timber')
    # Find closest hex vertex to tower for platform anchor
    best, best_d = None, 1e9
    for i in range(6):
        ang = math.radians(60 * i)
        vx = ox + _HEX_RADIUS * math.cos(ang)
        vy = oy + _HEX_RADIUS * math.sin(ang)
        d = math.hypot(vx - tower_x, vy - tower_y)
        if d < best_d:
            best_d = d
            best = (vx, vy)
    px, py = best
    # Tower-side anchor: top of stair where it meets platform-deck level
    tx, ty, _tz = tower_x, tower_y, deck_top_z
    span = math.hypot(tx - px, ty - py) or _BRIDGE_LENGTH

    # Two ropes — offset perpendicular to bridge axis by ±0.4 m
    perp_x = -(ty - py) / span * 0.4
    perp_y = (tx - px) / span * 0.4
    sag = 0.45
    for side in (-1, 1):
        # Approximate catenary as 6 short cylinder segments
        segs = 6
        for s in range(segs):
            t1 = s / segs
            t2 = (s + 1) / segs
            sx1 = px + (tx - px) * t1 + side * perp_x
            sy1 = py + (ty - py) * t1 + side * perp_y
            sz1 = deck_top_z - sag * math.sin(math.pi * t1)
            sx2 = px + (tx - px) * t2 + side * perp_x
            sy2 = py + (ty - py) * t2 + side * perp_y
            sz2 = deck_top_z - sag * math.sin(math.pi * t2)
            mx, my, mz = (sx1 + sx2) / 2, (sy1 + sy2) / 2, (sz1 + sz2) / 2
            seg_len = math.dist((sx1, sy1, sz1), (sx2, sy2, sz2))
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.025, depth=seg_len, location=(mx, my, mz))
            rope = bpy.context.active_object
            rope.name = f'BHT_BridgeRope_{side}_{s}'
            dx, dy, dz = sx2 - sx1, sy2 - sy1, sz2 - sz1
            from mathutils import Vector
            rope.rotation_mode = 'XYZ'
            rope.rotation_euler = Vector((dx, dy, dz)).to_track_quat('Z', 'Y').to_euler()
            if mat_rope is not None:
                assign(rope, mat_rope)
            _link(rope, col)

    # 8 deck planks
    for i in range(_BRIDGE_PLANKS):
        t = (i + 0.5) / _BRIDGE_PLANKS
        cx = px + (tx - px) * t
        cy = py + (ty - py) * t
        cz = deck_top_z - sag * math.sin(math.pi * t) + 0.04
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
        plank = bpy.context.active_object
        plank.name = f'BHT_BridgePlank_{i}'
        plank.scale = (0.85, 0.20, 0.04)
        plank.rotation_euler = (0.0, 0.0, math.atan2(ty - py, tx - px))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        if mat_wood is not None:
            assign(plank, mat_wood)
        _link(plank, col)


def _solar_panel(col, ox, oy, deck_top_z):
    """Flat scaled cube on south railing — Rule 7 outage-proof."""
    mat = _mat('pv_glass', 'glass_bottle_cobalt')
    # South hex vertex side ≈ bay 4 (i=4)
    a1 = math.radians(60 * 4)
    a2 = math.radians(60 * 5)
    x1 = ox + _HEX_RADIUS * math.cos(a1)
    y1 = oy + _HEX_RADIUS * math.sin(a1)
    x2 = ox + _HEX_RADIUS * math.cos(a2)
    y2 = oy + _HEX_RADIUS * math.sin(a2)
    mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    bpy.ops.mesh.primitive_cube_add(
        size=1.0, location=(mx, my, deck_top_z + _RAIL_HEIGHT + 0.10))
    pv = bpy.context.active_object
    pv.name = 'BHT_SolarPV'
    pv.scale = (1.1, 0.55, 0.04)
    pv.rotation_euler = (math.radians(20.0),         # 20° tilt north for Paraguay
                        0.0,
                        math.atan2(y2 - y1, x2 - x1))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    if mat is not None:
        assign(pv, mat)
    _link(pv, col)


def build_bamboo_boomhut_treehouse(origin=(0.0, 0.0, 0.0)):
    """Build the full Bamboo Boomhut Treehouse at ``origin``.

    Returns the collection holding every part.
    """
    ox, oy, oz = origin
    col = _ensure_collection('BambooBoomhutTreehouse', None)

    # 1. Three host lapacho trunks — visual stilts.
    for idx, (dx, dy) in enumerate(_HOST_TRUNK_POSITIONS):
        _add_host_trunk(col, ox + dx, oy + dy, f'BHT_HostTrunk_{idx}')

    # 2. Stair-tower trunk — independent host for the spiral stair.
    tower_x = ox + _STAIR_TOWER_XY[0]
    tower_y = oy + _STAIR_TOWER_XY[1]
    _add_host_trunk(col, tower_x, tower_y, 'BHT_StairTowerTrunk')

    # 3. Hex platform at z=4.
    deck_top_z = oz + ELEVATION_M
    _hex_platform(col, ox, oy, deck_top_z)

    # 4. Bamboo-frame walls 2.4 m tall.
    _bamboo_wall_frame(col, ox, oy, deck_top_z)

    # 5. Mosquito mesh skin (5 of 6 bays).
    _mosquito_mesh_panels(col, ox, oy, deck_top_z)

    # 6. North glass window (bay 1).
    _glass_north_window(col, ox, oy, deck_top_z)

    # 7. Conical thatch roof.
    eave_z = deck_top_z + WALL_HEIGHT_M
    _conical_thatch_roof(col, ox, oy, eave_z)

    # 8. Perimeter railings — top + bottom rails on every hex segment.
    _perimeter_railing(col, ox, oy, deck_top_z)

    # 9. Spiral stair wrapping the stair-tower trunk (P0.8 anchor: physical trunk).
    _spiral_stair(col, tower_x, tower_y)

    # 10. Suspended bamboo bridge from stair top to platform.
    _suspended_bridge(col, ox, oy, deck_top_z, tower_x, tower_y)

    # 11. Solar PV box on south railing.
    _solar_panel(col, ox, oy, deck_top_z)

    return col


# Back-compat: keep the old `build()` signature alive so callers that imported
# the stub keep working.
def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    return build_bamboo_boomhut_treehouse(origin=location)
