"""Typology — Container River House (single 20 ft, riverside cantilever).

A repurposed 20 ft shipping container (~6.06 m × 2.44 m × 2.59 m), perched on
the river bank on a steel I-beam frame 1.2 m above grade. River-facing long
side is opened up into a floor-to-ceiling glass wall; the opposite side keeps
corten ribbed cladding. A narrow lapacho-board deck cantilevers along the
river side; an exterior corten stair lands on the bank. 2 PAX layout (bed +
kitchenette + bath + glass-front living). Solar PV lives on its own steel
frame (Rule 9). No cement plaster (Rule 2).

Materials use the project ``MAT`` registry with explicit fallbacks — the brief
calls for ``corten_steel`` / ``glass`` / ``stone_foundation`` etc. but those
keys aren't in the registry yet, so we resolve through a chain to the nearest
shipped material (``steel_anodized``, ``pv_glass``, ``sandstone``).
"""
from __future__ import annotations

import bpy

from lqv.furniture import furnish_interior
from lqv.materials import MAT, assign

# --- Container shell -------------------------------------------------------
CONTAINER_L = 6.06    # 20 ft ISO container long axis (Y)
CONTAINER_W = 2.44    # short axis (X)
CONTAINER_H = 2.59    # height (Z)
FOOTPRINT_M2 = CONTAINER_L * CONTAINER_W
SLEEPS = 2

# --- Stilt / I-beam frame --------------------------------------------------
PIER_LIFT = 1.2       # bottom of container 1.2 m above bank
PIER_W = 0.18         # I-beam stand-in cross-section
PIER_COUNT = 4

# --- Deck (cantilevered along river side, +X) ------------------------------
DECK_L = 6.0
DECK_W = 1.2
DECK_THK = 0.08

# --- Glass river wall ------------------------------------------------------
GLASS_L = 5.5
GLASS_H = 2.4
GLASS_THK = 0.04

# --- Cladding ribs ---------------------------------------------------------
RIB_SPACING = 0.30
RIB_W = 0.04
RIB_DEPTH = 0.02

# --- Stair -----------------------------------------------------------------
STAIR_STEPS = 5
STAIR_TREAD_W = 0.9
STAIR_TREAD_RUN = 0.28
STAIR_TREAD_THK = 0.05

ORIENTATION = 'river_on_+X'
SNAP = 'stilts'
NOTES = (
    'Corten or matte-black ribbed cladding on the three non-river walls + roof.',
    'River-facing long wall is full glazing — frame hidden in floor + roof slot.',
    'Steel I-beam piers 1.2 m above bank (Rule 9 — solar PV on separate frame).',
    'Lapacho deck cantilevers off the +X long edge; no rail modelled (concept).',
    '2 PAX: bed + kitchenette + bath + glass-front living. No interior shown.',
)

MATERIAL_TAKEOFF: dict = {
    'shipping_container_20ft': {
        'count': 1,
        'unit_cost_usd': 3500.0,           # used 20 ft, delivered Asuncion 2026
    },
    'corten_cladding': {
        'area_m2': 32.0,                   # 3 walls + roof, less glass cut-out
        'unit_cost_usd': 48.0,
    },
    'bamboo_accent': {
        'length_m': 24.0,                  # entrance + corner accents
        'unit_cost_usd': 9.0,
    },
    'glass_river_wall': {
        'area_m2': 13.5,                   # ~5.5 × 2.4 frameless
        'unit_cost_usd': 240.0,
    },
    'steel_ibeam_piers': {
        'length_m': 10.0,                  # 4 piers + cross bracing
        'unit_cost_usd': 95.0,
    },
    'lapacho_deck_boards': {
        'area_m2': 7.0,                    # ~6 × 1.2
        'unit_cost_usd': 95.0,
    },
    'lapacho_stair_treads': {
        'count': 5,
        'unit_cost_usd': 38.0,
    },
    'solar_pv_panels': {
        'count': 4,
        'unit_cost_usd': 180.0,
    },
    'fasteners_misc': {
        'count': 250,
        'unit_cost_usd': 1.2,
    },
}


def _resolve(*keys):
    """Walk the MAT key chain; return the first hit (or None)."""
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


def _cyl(col, name, location, radius, depth, mat, vertices=12):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, vertices=vertices,
    )
    obj = bpy.context.active_object
    obj.name = name
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def build_container_river_house(origin=(0.0, 0.0, 0.0), variant: str = 'A'):
    """Build the Container River House at ``origin``."""
    ox, oy, oz = origin
    col = _ensure_collection('ContainerRiverHouse', None)

    corten = _resolve('corten_steel', 'steel_anodized')
    steel = _resolve('steel', 'steel_anodized')
    glass = _resolve('glass', 'pv_glass')
    lapacho = _resolve('lapacho_wood', 'lapacho_timber')
    bamboo = _resolve('bamboo_culm', 'bamboo_shingle', 'bamboo')
    stone = _resolve('stone_foundation', 'sandstone')

    # --- Container shell -----------------------------------------------------
    shell_z = oz + PIER_LIFT + CONTAINER_H / 2.0
    _box(col, 'CRH_Shell',
         (ox, oy, shell_z),
         (CONTAINER_W, CONTAINER_L, CONTAINER_H),
         corten)

    # Roof cap (slightly proud, breaks the silhouette for hero shots).
    _box(col, 'CRH_RoofCap',
         (ox, oy, oz + PIER_LIFT + CONTAINER_H + 0.04),
         (CONTAINER_W + 0.08, CONTAINER_L + 0.08, 0.08),
         corten)

    # --- Vertical cladding ribs on the three non-river sides ----------------
    # +X side is the river; ribs on -X long wall + both short walls.
    n_long_ribs = int(CONTAINER_L / RIB_SPACING)
    for i in range(n_long_ribs):
        y = oy - CONTAINER_L / 2.0 + (i + 0.5) * (CONTAINER_L / n_long_ribs)
        _box(col, f'CRH_RibLongMinus_{i}',
             (ox - CONTAINER_W / 2.0 - RIB_DEPTH / 2.0, y, shell_z),
             (RIB_DEPTH, RIB_W, CONTAINER_H),
             corten)
    n_short_ribs = int(CONTAINER_W / RIB_SPACING)
    for i in range(n_short_ribs):
        x = ox - CONTAINER_W / 2.0 + (i + 0.5) * (CONTAINER_W / n_short_ribs)
        for end_sign in (-1, 1):
            y = oy + end_sign * (CONTAINER_L / 2.0 + RIB_DEPTH / 2.0)
            _box(col, f'CRH_RibShort_{end_sign}_{i}',
                 (x, y, shell_z),
                 (RIB_W, RIB_DEPTH, CONTAINER_H),
                 corten)

    # --- Glass river wall (+X long side) ------------------------------------
    glass_x = ox + CONTAINER_W / 2.0 + GLASS_THK / 2.0
    _box(col, 'CRH_GlassWall',
         (glass_x, oy, oz + PIER_LIFT + GLASS_H / 2.0 + 0.05),
         (GLASS_THK, GLASS_L, GLASS_H),
         glass)

    # --- Steel I-beam piers (4) ---------------------------------------------
    half_dx = CONTAINER_W / 2.0 - 0.25
    half_dy = CONTAINER_L / 2.0 - 0.4
    for i, (dx, dy) in enumerate([(-half_dx, -half_dy), (half_dx, -half_dy),
                                   (-half_dx, half_dy), (half_dx, half_dy)]):
        _box(col, f'CRH_Pier_{i}',
             (ox + dx, oy + dy, oz + PIER_LIFT / 2.0),
             (PIER_W, PIER_W, PIER_LIFT),
             steel)
    # Cross-bracing between piers (X plane, both ends).
    for end_sign in (-1, 1):
        _box(col, f'CRH_PierBrace_{end_sign}',
             (ox, oy + end_sign * half_dy, oz + PIER_LIFT - 0.15),
             (CONTAINER_W - 0.4, 0.08, 0.08),
             steel)

    # Stone footings under each pier — riparian rule of thumb.
    for i, (dx, dy) in enumerate([(-half_dx, -half_dy), (half_dx, -half_dy),
                                   (-half_dx, half_dy), (half_dx, half_dy)]):
        _box(col, f'CRH_Footing_{i}',
             (ox + dx, oy + dy, oz + 0.08),
             (0.5, 0.5, 0.16),
             stone)

    # --- Lapacho deck cantilever (+X long side) -----------------------------
    deck_x = ox + CONTAINER_W / 2.0 + GLASS_THK + DECK_W / 2.0
    _box(col, 'CRH_Deck',
         (deck_x, oy, oz + PIER_LIFT - DECK_THK / 2.0),
         (DECK_W, DECK_L, DECK_THK),
         lapacho)
    # Deck support brackets (4) — steel under the lapacho.
    for i in range(4):
        t = (i + 0.5) / 4.0
        y = oy - DECK_L / 2.0 + t * DECK_L
        _box(col, f'CRH_DeckBracket_{i}',
             (deck_x, y, oz + PIER_LIFT - DECK_THK - 0.06),
             (DECK_W - 0.05, 0.06, 0.08),
             steel)

    # --- Exterior corten stair on the -X bank side --------------------------
    stair_x0 = ox - CONTAINER_W / 2.0 - 0.4
    stair_y = oy - CONTAINER_L / 2.0 + 0.6
    rise = PIER_LIFT / STAIR_STEPS
    for i in range(STAIR_STEPS):
        x = stair_x0 - i * STAIR_TREAD_RUN
        z = oz + rise * (i + 0.5)
        _box(col, f'CRH_StairTread_{i}',
             (x, stair_y, z),
             (STAIR_TREAD_RUN, STAIR_TREAD_W, STAIR_TREAD_THK),
             lapacho)
    # Stair stringers (2) — corten.
    stringer_len = STAIR_STEPS * STAIR_TREAD_RUN
    stringer_mid_x = stair_x0 - stringer_len / 2.0 + STAIR_TREAD_RUN / 2.0
    for side_sign in (-1, 1):
        _box(col, f'CRH_StairStringer_{side_sign}',
             (stringer_mid_x,
              stair_y + side_sign * STAIR_TREAD_W / 2.0,
              oz + PIER_LIFT / 2.0),
             (stringer_len, 0.05, PIER_LIFT),
             corten)

    # --- Bamboo accents at the entrance corner ------------------------------
    for i in range(3):
        ax = ox - CONTAINER_W / 2.0 - 0.05 - i * 0.10
        _cyl(col, f'CRH_BambooAccent_{i}',
             (ax, oy - CONTAINER_L / 2.0 - 0.05, oz + PIER_LIFT + CONTAINER_H / 2.0),
             0.045, CONTAINER_H, bamboo, vertices=8)

    # --- HVAC vent box on roof ----------------------------------------------
    _box(col, 'CRH_HVACVent',
         (ox - CONTAINER_W / 4.0,
          oy + CONTAINER_L / 3.0,
          oz + PIER_LIFT + CONTAINER_H + 0.08 + 0.18),
         (0.55, 0.40, 0.35),
         steel)

    # --- Solar PV on separate steel frame (Rule 9) --------------------------
    pv_frame_x = ox - CONTAINER_W / 2.0 - 1.6
    pv_frame_y = oy - CONTAINER_L / 4.0
    # Frame posts (2) on the bank, away from the container.
    for i, dy in enumerate((-0.8, 0.8)):
        _box(col, f'CRH_PVPost_{i}',
             (pv_frame_x, pv_frame_y + dy, oz + 1.1),
             (0.08, 0.08, 2.2),
             steel)
    # Tilted PV array (4 panels).
    for i in range(4):
        _box(col, f'CRH_PVPanel_{i}',
             (pv_frame_x - 0.1, pv_frame_y - 0.9 + i * 0.6, oz + 2.0),
             (0.9, 0.55, 0.04),
             glass)

    # P1.B.1 — interior furniture stubs (RENDER_VIEW=interior readable).
    furnish_interior(
        col,
        footprint_w=CONTAINER_L - 0.4,
        footprint_l=CONTAINER_W - 0.4,
        origin_xy=(ox, oy),
        floor_z=oz + PIER_LIFT,
        pax=SLEEPS,
        style='container',
        variant=variant,
        name_prefix='CRH_Furn',
    )

    return col


# Legacy alias kept so the old subscene driver `_build()` path still works.
def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    return build_container_river_house(origin=location, variant=variant)
