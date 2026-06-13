"""Amenity — Floating Dining.

Open-air dining platform appearing to float over the creek. An 8 m × 5 m
lapacho deck on eight short posts sits 0.9 m above a 14 m × 10 m subtle
reflective water plane; the visual hero is the row of nine bamboo-frame
pendant lanterns suspended from a Guadua ring beam overhead. A 4 m catwalk
to the north shore makes the floating context legible; bamboo clumps and
tree ferns on the surrounding edges anchor the platform in the riparian
zone. No walls, no solid roof — the ring beam is the structure.

Wesley brief (2026-06-13): the platform should read first as "dining over
water", second as "Paraguayan riparian vernacular" (lapacho + Guadua + sisal
lashings). The lanterns are the punctum at dusk; the water reflection is
what sells the float.

Factors shared primitives from :mod:`lqv.amenities._grammar` (the glass-bowl
pendant lantern Wesley introduced on labrisa_lounge) and
:mod:`lqv.house.bamboo_frame` (culm / beam / lashing). Tree ferns and bamboo
clumps come from :mod:`lqv.flora`; if ``RENDER_FLORA_PHOTOREAL=1`` the
photoreal tree-fern asset is used instead of the procedural stand-in.
"""
from __future__ import annotations

import math
import os

import bpy

from lqv.amenities import _grammar
from lqv.house.bamboo_frame import (
    build_bamboo_beam,
    build_bamboo_culm,
    build_bamboo_lashing,
)
from lqv.materials import MAT, assign

# Headline geometry (E-W long axis = +X, N short axis = +Y)
DECK_LEN_X = 8.0
DECK_WIDTH_Y = 5.0
DECK_THICK = 0.06
DECK_ELEVATION = 0.9                     # deck-top sits at z = 0.9 + DECK_THICK/2

WATER_LEN_X = 14.0
WATER_WIDTH_Y = 10.0
WATER_Z = 0.0

# Deck posts (eight short lapacho posts under the deck)
POST_SIDE = 0.18
POST_HEIGHT = 0.9
DECK_POST_COUNT = 8

# Communal slab table + 8 stools
TABLE_LEN_X = 4.0
TABLE_WIDTH_Y = 1.4
TABLE_THICK = 0.05
TABLE_HEIGHT_ABOVE_DECK = 0.78
TABLE_LEG_SIDE = 0.08
TABLE_LEG_COUNT = 6                      # 4 corners + 2 mid-span
STOOL_COUNT = 8

# Bamboo ring-beam canopy (4 corner lapacho posts + Guadua ring + lanterns)
CANOPY_POST_SIDE = 0.15
CANOPY_POST_HEIGHT = 3.0
CANOPY_RING_DIAMETER = 0.10              # 100 mm Guadua culm
LANTERN_COUNT = 9
LANTERN_RADIUS = 0.22
LANTERN_SUSPENSION = 0.5

# Catwalk to north shore
CATWALK_LEN_Y = 4.0
CATWALK_WIDTH_X = 1.2
CATWALK_POST_COUNT = 4

# Flora
GUADUA_CLUMPS_SOUTH = 3
TREE_FERNS_NORTH = 2

ROOF_TYPE = 'none_open_air'
NOTES = (
    'Open-air dining platform: no walls, no solid roof — ring beam canopy only.',
    'Deck sits 0.9 m above a reflective water plane (14 m × 10 m), giving a "float over creek" read.',
    'Communal lapacho slab 4 m × 1.4 m E-W with eight bamboo+lapacho-seat stools.',
    'Nine glass-bowl bamboo-frame pendant lanterns on a 4-culm Guadua ring beam — visual hero at dusk.',
    'Lapacho catwalk 1.2 m × 4 m to the north shore (4 short posts) anchors the float context.',
    'Surround flora: 3 Guadua clumps south edge, 2 tree ferns north shore.',
)


# ---------- per-design MATERIAL_TAKEOFF (rural Paraguarí rates 2026) ----------
# Quantities are *single quantity field per line* + ``unit_cost_usd``. The
# downstream BOM tool sums (qty × unit). Target band: $16-22k.
MATERIAL_TAKEOFF: dict[str, dict] = {
    'lapacho_deck_planks': {
        # 8 × 5 m deck, surface area (single layer).
        'area_m2': DECK_LEN_X * DECK_WIDTH_Y,
        'unit_cost_usd': 62.0,
    },
    'lapacho_deck_posts': {
        # 8 short posts 0.18 × 0.18 × 0.9 m, milled lapacho — sold per post.
        'count': DECK_POST_COUNT,
        'unit_cost_usd': 38.0,
    },
    'lapacho_communal_slab_table': {
        # Single live-edge slab 4 × 1.4 × 0.05 m + 6 legs (sold as a set).
        'count': 1,
        'unit_cost_usd': 2200.0,
    },
    'stool_set_bamboo_lapacho': {
        # 8 stools, bamboo frame + lapacho seat — per-stool rural rate.
        'count': STOOL_COUNT,
        'unit_cost_usd': 95.0,
    },
    'lapacho_canopy_posts': {
        # 4 corner posts 0.15 × 0.15 × 3.0 m carrying the ring beam.
        'count': 4,
        'unit_cost_usd': 145.0,
    },
    'guadua_ring_beam_culms': {
        # 4 culms × ~8 m each (long perimeter side) lashed at corners.
        'length_m': 4 * (DECK_LEN_X + 0.4),
        'unit_cost_usd': 11.0,
    },
    'sisal_rope_lashings': {
        # Corner lashings + ring-to-post + lantern hangers; metres of rope.
        'length_m': 90.0,
        'unit_cost_usd': 3.5,
    },
    'bamboo_pendant_lanterns': {
        # 9 bamboo-frame open-sphere pendants with warm 2700K bulb.
        'count': LANTERN_COUNT,
        'unit_cost_usd': 130.0,
    },
    'reflective_water_basin_liner': {
        # 14 × 10 m EPDM pond liner + perimeter seal for the still-water basin.
        'area_m2': WATER_LEN_X * WATER_WIDTH_Y,
        'unit_cost_usd': 18.0,
    },
    'lapacho_catwalk_assembly': {
        # 1.2 m × 4 m gangway + 4 short shore-side posts (priced as 1 assembly).
        'count': 1,
        'unit_cost_usd': 1450.0,
    },
    'low_voltage_lantern_wiring_set': {
        # 24 V LED driver + UV-rated drop cable + dimmer (set for 9 pendants).
        'count': 1,
        'unit_cost_usd': 420.0,
    },
}


# ---------- collection / link / material helpers ----------

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
    """First-resolves MAT key fallback chain. ``None`` if nothing resolves."""
    for k in keys:
        m = MAT.get(k)
        if m is not None:
            return m
    return None


# ---------- geometry builders ----------

def _water_plane(col: bpy.types.Collection, ox: float, oy: float) -> None:
    """Subtle reflective water plane underneath the float — this sells the read."""
    mat = _mat('water_reflective', 'pool_water', 'stream_bed', 'pv_glass')
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(ox, oy, WATER_Z))
    obj = bpy.context.active_object
    obj.name = 'FloatingDining_Water'
    obj.scale = (WATER_LEN_X, WATER_WIDTH_Y, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)


def _deck_posts(col: bpy.types.Collection, ox: float, oy: float) -> None:
    """Eight 0.18 m × 0.18 m × 0.9 m lapacho posts holding up the deck."""
    mat = _mat('lapacho_timber', 'bamboo')
    # 4 corners (inset 0.4 m) + 4 mid-edge posts on the long sides.
    inset = 0.4
    hx = DECK_LEN_X / 2 - inset
    hy = DECK_WIDTH_Y / 2 - inset
    positions = [
        (-hx, -hy), (+hx, -hy), (-hx, +hy), (+hx, +hy),     # 4 corners
        (-hx / 3, -hy), (+hx / 3, -hy),                       # 2 mid-S edge
        (-hx / 3, +hy), (+hx / 3, +hy),                       # 2 mid-N edge
    ]
    z_mid = POST_HEIGHT / 2.0
    for i, (dx, dy) in enumerate(positions):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox + dx, oy + dy, z_mid))
        obj = bpy.context.active_object
        obj.name = f'FloatingDining_DeckPost_{i:02d}'
        obj.scale = (POST_SIDE, POST_SIDE, POST_HEIGHT)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if mat is not None:
            assign(obj, mat)
        _link(obj, col)


def _deck(col: bpy.types.Collection, ox: float, oy: float) -> None:
    """8 m × 5 m lapacho deck, top at z = 0.9 + DECK_THICK/2; planks // long axis."""
    mat = _mat('lapacho_timber', 'bamboo')
    z_mid = DECK_ELEVATION + DECK_THICK / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox, oy, z_mid))
    obj = bpy.context.active_object
    obj.name = 'FloatingDining_Deck'
    obj.scale = (DECK_LEN_X, DECK_WIDTH_Y, DECK_THICK)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)


def _table(col: bpy.types.Collection, ox: float, oy: float) -> None:
    """4 m × 1.4 m lapacho slab table on 6 legs (4 corners + 2 mid-span)."""
    mat_wood = _mat('lapacho_timber', 'bamboo')
    deck_top = DECK_ELEVATION + DECK_THICK

    # Slab top
    top_z = deck_top + TABLE_HEIGHT_ABOVE_DECK + TABLE_THICK / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox, oy, top_z))
    top = bpy.context.active_object
    top.name = 'FloatingDining_Table_Slab'
    top.scale = (TABLE_LEN_X, TABLE_WIDTH_Y, TABLE_THICK)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat_wood is not None:
        assign(top, mat_wood)
    _link(top, col)

    # 6 legs — 4 corner + 2 mid-span
    leg_h = TABLE_HEIGHT_ABOVE_DECK - 0.02
    leg_z = deck_top + leg_h / 2.0
    half_x = TABLE_LEN_X / 2 - 0.15
    half_y = TABLE_WIDTH_Y / 2 - 0.15
    leg_positions = [
        (-half_x, -half_y), (+half_x, -half_y),
        (-half_x, +half_y), (+half_x, +half_y),
        (0.0, -half_y), (0.0, +half_y),
    ]
    for i, (dx, dy) in enumerate(leg_positions):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox + dx, oy + dy, leg_z))
        leg = bpy.context.active_object
        leg.name = f'FloatingDining_Table_Leg_{i:02d}'
        leg.scale = (TABLE_LEG_SIDE, TABLE_LEG_SIDE, leg_h)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if mat_wood is not None:
            assign(leg, mat_wood)
        _link(leg, col)


def _stools(col: bpy.types.Collection, ox: float, oy: float) -> None:
    """8 bamboo+lapacho-seat stools, 4 per long side of the table."""
    mat_seat = _mat('lapacho_timber', 'bamboo')
    deck_top = DECK_ELEVATION + DECK_THICK
    seat_h = 0.46
    seat_radius = 0.18
    leg_radius = 0.022
    leg_h = seat_h - 0.02

    side_y_off = TABLE_WIDTH_Y / 2 + 0.45      # seat edge sits ~0.45 m off table edge
    n_per_side = 4
    span_x = TABLE_LEN_X - 0.5                  # inset so seats land at table span
    for side in (-1, +1):                       # south then north
        sy = side * side_y_off
        for j in range(n_per_side):
            t = (j + 0.5) / n_per_side
            sx = -span_x / 2 + span_x * t
            # Seat disc
            bpy.ops.mesh.primitive_cylinder_add(
                radius=seat_radius,
                depth=0.04,
                location=(ox + sx, oy + sy, deck_top + seat_h),
                vertices=16,
            )
            seat = bpy.context.active_object
            seat.name = f'FloatingDining_Stool_Seat_{int(side)}_{j}'
            if mat_seat is not None:
                assign(seat, mat_seat)
            _link(seat, col)
            # 3 splayed bamboo legs per stool
            for k in range(3):
                theta = (k / 3) * 2.0 * math.pi
                # Splay 8 cm out at the foot
                foot_dx = 0.08 * math.cos(theta)
                foot_dy = 0.08 * math.sin(theta)
                head_dx = 0.03 * math.cos(theta)
                head_dy = 0.03 * math.sin(theta)
                build_bamboo_culm(
                    p_start_xyz=(ox + sx + foot_dx, oy + sy + foot_dy, deck_top),
                    p_end_xyz=(ox + sx + head_dx, oy + sy + head_dy, deck_top + leg_h),
                    diameter_m=leg_radius * 2,
                    taper_ratio=0.95,
                    segments=8,
                    material='bamboo',
                    name=f'FloatingDining_Stool_Leg_{int(side)}_{j}_{k}',
                )


def _canopy_posts_and_ring(col: bpy.types.Collection, ox: float, oy: float) -> None:
    """4 corner lapacho posts (0.15 × 0.15 × 3.0 m) + a 4-culm Guadua ring beam.

    The ring beam sits at z = deck_top + canopy_post_height; lashings at each
    corner where the bamboo meets the post. The 9 pendant lanterns drop from
    the long-axis culms below.
    """
    mat_post = _mat('lapacho_timber', 'bamboo')
    deck_top = DECK_ELEVATION + DECK_THICK
    half_x = DECK_LEN_X / 2 - 0.15
    half_y = DECK_WIDTH_Y / 2 - 0.15
    corner_xy = [(-half_x, -half_y), (+half_x, -half_y),
                 (+half_x, +half_y), (-half_x, +half_y)]

    # 4 corner posts
    post_z_mid = deck_top + CANOPY_POST_HEIGHT / 2.0
    for i, (dx, dy) in enumerate(corner_xy):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox + dx, oy + dy, post_z_mid))
        post = bpy.context.active_object
        post.name = f'FloatingDining_CanopyPost_{i}'
        post.scale = (CANOPY_POST_SIDE, CANOPY_POST_SIDE, CANOPY_POST_HEIGHT)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if mat_post is not None:
            assign(post, mat_post)
        _link(post, col)

    # Ring beam (4 Guadua culms — 2 long, 2 short)
    ring_z = deck_top + CANOPY_POST_HEIGHT
    corners_world = [(ox + dx, oy + dy, ring_z) for dx, dy in corner_xy]
    for i in range(4):
        a = corners_world[i]
        b = corners_world[(i + 1) % 4]
        build_bamboo_beam(
            p_start_xyz=a,
            p_end_xyz=b,
            diameter_m=CANOPY_RING_DIAMETER,
            material='bamboo',
            name=f'FloatingDining_RingBeam_{i}',
        )

    # Sisal-rope corner lashings (4 of them)
    for i, (cx, cy, cz) in enumerate(corners_world):
        build_bamboo_lashing(
            xyz=(cx, cy, cz - 0.04),
            radius_m=0.10,
            thickness_m=0.018,
            material='rope_natural',
            fallback='lapacho_timber',
            name=f'FloatingDining_Lashing_{i}',
        )


def _pendant_lantern(col: bpy.types.Collection,
                     location: tuple[float, float, float],
                     bowl_radius: float,
                     suspension_length: float,
                     name_prefix: str) -> None:
    """Bamboo-frame open-sphere pendant lantern with a warm emissive interior.

    Prefers ``_grammar.glass_bowl_lantern`` (already in service on
    labrisa_lounge) — it gives us a hanging cord + glass bowl with the
    project's warm-lantern material. We layer a small emissive UV sphere just
    inside so the lantern reads as illuminated even from outside-frame.
    """
    lx, ly, lz = location
    _grammar.glass_bowl_lantern(
        col,
        location=(lx, ly, lz),
        bowl_radius_m=bowl_radius,
        suspension_length_m=suspension_length,
        name_prefix=name_prefix,
    )
    # Inner emissive node — small UV sphere at 70 % bowl radius, gets the
    # ``window_glow`` material (warm 2700 K emissive in project palette);
    # falls back to firefly emission if window_glow is missing.
    mat_em = _mat('window_glow', 'firefly', 'lantern_paper_warm')
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=bowl_radius * 0.70,
        location=(lx, ly, lz),
        segments=12,
        ring_count=8,
    )
    em = bpy.context.active_object
    em.name = f'{name_prefix}_Emitter'
    if mat_em is not None:
        assign(em, mat_em)
    _link(em, col)


def _pendant_lanterns(col: bpy.types.Collection, ox: float, oy: float) -> None:
    """9 pendants suspended from the ring beam at 1 m intervals along long axis."""
    deck_top = DECK_ELEVATION + DECK_THICK
    ring_z = deck_top + CANOPY_POST_HEIGHT
    hang_z = ring_z - LANTERN_SUSPENSION
    # 9 across the long axis, centred. 1 m spacing -> total span = 8 m.
    span = 8.0
    for i in range(LANTERN_COUNT):
        if LANTERN_COUNT == 1:
            t = 0.5
        else:
            t = i / (LANTERN_COUNT - 1)
        x = ox - span / 2 + span * t
        _pendant_lantern(
            col,
            location=(x, oy, hang_z),
            bowl_radius=LANTERN_RADIUS,
            suspension_length=LANTERN_SUSPENSION,
            name_prefix=f'FloatingDining_Pendant_{i:02d}',
        )


def _catwalk(col: bpy.types.Collection, ox: float, oy: float) -> None:
    """1.2 m × 4 m lapacho gangway from deck north edge to shore (+Y direction)."""
    mat_wood = _mat('lapacho_timber', 'bamboo')

    deck_top = DECK_ELEVATION + DECK_THICK
    walk_y_start = oy + DECK_WIDTH_Y / 2
    walk_y_end = walk_y_start + CATWALK_LEN_Y
    walk_y_mid = (walk_y_start + walk_y_end) / 2.0

    # Walking surface at deck height (so guests step off the deck level).
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(ox, walk_y_mid, deck_top - DECK_THICK / 2.0))
    walk = bpy.context.active_object
    walk.name = 'FloatingDining_Catwalk'
    walk.scale = (CATWALK_WIDTH_X, CATWALK_LEN_Y, DECK_THICK)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat_wood is not None:
        assign(walk, mat_wood)
    _link(walk, col)

    # 4 supporting posts — pairs at 1/3 and 2/3 along catwalk length
    for j in range(2):
        cy = walk_y_start + (j + 1) * (CATWALK_LEN_Y / 3.0)
        for side in (-1, +1):
            px = ox + side * (CATWALK_WIDTH_X / 2 - 0.1)
            bpy.ops.mesh.primitive_cube_add(
                size=1.0,
                location=(px, cy, POST_HEIGHT / 2.0),
            )
            post = bpy.context.active_object
            post.name = f'FloatingDining_CatwalkPost_{j}_{int(side)}'
            post.scale = (POST_SIDE, POST_SIDE, POST_HEIGHT)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            if mat_wood is not None:
                assign(post, mat_wood)
            _link(post, col)


def _surround_flora(col: bpy.types.Collection, ox: float, oy: float) -> None:
    """3 Guadua clumps on south water-edge + 2 tree ferns on north shore."""
    from lqv.flora.bamboo import add_bamboo_clump
    if os.environ.get('RENDER_FLORA_PHOTOREAL') == '1':
        try:
            from lqv.flora.photoreal import add_tree_fern_photoreal as _add_tree_fern
        except Exception:
            from lqv.flora.fern import add_tree_fern as _add_tree_fern
    else:
        from lqv.flora.fern import add_tree_fern as _add_tree_fern

    # 3 Guadua clumps along the south water edge — between deck and camera.
    south_y = oy - WATER_WIDTH_Y / 2 + 0.6
    for i in range(GUADUA_CLUMPS_SOUTH):
        t = (i + 0.5) / GUADUA_CLUMPS_SOUTH
        x = ox - WATER_LEN_X / 2 + WATER_LEN_X * t
        try:
            add_bamboo_clump(x, south_y, n=7, scale=1.1)
        except Exception:
            pass

    # 2 tree ferns on the north shore beyond the catwalk.
    north_y = oy + WATER_WIDTH_Y / 2 + 0.8
    for i in range(TREE_FERNS_NORTH):
        # Place left + right of the catwalk so it stays legible.
        x = ox + ((-1) if i == 0 else (+1)) * 2.2
        try:
            _add_tree_fern(x, north_y, scale=1.0)
        except Exception:
            pass


# ---------- public entry point ----------

def build(parent: bpy.types.Collection | None = None,
          location: tuple[float, float, float] = (0.0, 0.0, 0.0),
          variant: str = 'A') -> bpy.types.Collection:
    """Build the floating dining amenity at ``location``.

    Composition order matters: water plane first (under everything), then
    deck-support posts, deck, table + stools, canopy posts + ring beam,
    pendants, catwalk, surround flora. Variant is currently advisory — the
    asset reads identically across A/B/C apart from exposure (set by the
    sub-render driver) and HDRI (set by ``base.setup_world``).
    """
    col = _ensure_collection('FloatingDining', parent)
    ox, oy, _oz = location

    _water_plane(col, ox, oy)
    _deck_posts(col, ox, oy)
    _deck(col, ox, oy)
    _table(col, ox, oy)
    _stools(col, ox, oy)
    _canopy_posts_and_ring(col, ox, oy)
    _pendant_lanterns(col, ox, oy)
    _catwalk(col, ox, oy)
    _surround_flora(col, ox, oy)

    return col


__all__ = [
    'DECK_LEN_X', 'DECK_WIDTH_Y', 'DECK_ELEVATION',
    'MATERIAL_TAKEOFF', 'NOTES', 'ROOF_TYPE',
    'build',
]
