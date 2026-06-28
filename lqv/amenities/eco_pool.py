"""Amenity — Eco Pool (bamboo + stone wellness pool).

Wesley-brief wellness pool, NOT a suburban concrete rectangle. Reads as a
natural-stone-coped pool with a jacuzzi inset, lapacho plank deck wrapping
three sides, a palm-thatch pergola at the SE corner, a bamboo outdoor shower
at the NW corner, and a row of mossy boulder bench seats along the south
edge of the deck. Two Guadua bamboo clumps and two lapacho saplings frame
the north and east edges so the asset never reads as an isolated tile.

Sub-render-first per ``feedback_sub_render_first``: this typology has a
matching driver at :mod:`lqv.subscene.eco_pool` that bypasses
:func:`lqv.subscene.base.run` and pins ``cam.data.clip_end`` so the parcel-
scale shot doesn't return only HDRI (``feedback_subscene_clip_end``).

The previous "natural swim regen-zone" interpretation has been replaced; the
cascade-weir overflow continuity is delegated to :mod:`labrisa_lounge` and
:mod:`eco_retreat_modern_oasis`, which still front the creek. The pool here
is a closed wellness loop, not a creek-fed bio-filter.

Material vocabulary (CC0 + CC-BY 4.0 only; no downloaded textures):

* Sandstone coping slabs ``MAT['sandstone']``.
* Lapacho deck planks + posts ``MAT['lapacho_timber']``.
* Guadua bamboo culms (pergola posts, shower mast, beam ring) ``MAT['bamboo']``.
* Palm-thatch pergola roof ``MAT['palm_thatch']``.
* Pool + jacuzzi water ``MAT['pool_water']`` (reflective + light SSS).
* Moss-on-stone boulder seating ``MAT['moss']`` (fallback ``MAT['sandstone']``).
* Copper shower head nub ``MAT['steel_anodized']`` (no copper in registry).
"""
from __future__ import annotations

import math
import os

import bpy

from lqv.amenities import _grammar
from lqv.house import bamboo_frame
from lqv.materials import MAT, assign

# ---------------------------------------------------------------------------
# Wesley brief constants
# ---------------------------------------------------------------------------

POOL_LENGTH_M = 8.0           # x dimension (east-west)
POOL_WIDTH_M = 4.0            # y dimension (north-south)
POOL_DEPTH_DEEP_M = 1.2
POOL_DEPTH_SHALLOW_M = 0.6
JACUZZI_SIZE_M = 2.0          # 2 m × 2 m at NE corner
JACUZZI_DEPTH_M = 0.7
JACUZZI_CURB_LIFT_M = 0.15
DECK_LENGTH_M = 12.0          # wraps N/E/W of pool
DECK_WIDTH_M = 8.0
DECK_LIFT_M = 0.15
DECK_POST_COUNT = 24
DECK_POST_SIDE_M = 0.15
DECK_POST_HEIGHT_M = 0.30
PERGOLA_SIZE_M = 3.0          # 3 m × 3 m at SE corner
PERGOLA_HEIGHT_M = 2.6
SHOWER_HEIGHT_M = 2.5
SHOWER_ARM_LEN_M = 0.6
SHOWER_BASE_SIZE_M = 0.6
BOULDER_SEAT_COUNT = 3
COPING_PLANK_WIDTH_M = 0.5    # 0.4-0.6 m slabs (Wesley)
COPING_PLANK_THICKNESS_M = 0.08

NOTES = (
    'Wellness pool, no chlorine signaling — water reads as river-bottom not blue tile.',
    'Jacuzzi raised 0.15 m on its own sandstone curb at NE corner of main pool.',
    'Lapacho deck 0.15 m above grade, 24 posts at ~2 m centres on a 12 m × 8 m plan.',
    'Palm-thatch pergola throws visible shade — 3 m × 3 m on 4 lapacho posts.',
    'Outdoor shower NW: single bamboo culm 2.5 m vertical with horizontal arm.',
    'Three mossy-boulder bench seats line the south edge of the deck.',
    'Two Guadua bamboo clumps + two lapacho saplings frame north + east edges.',
)

# ---------------------------------------------------------------------------
# Material take-off — module-level, 9-12 line items, target USD 22-30 k band.
# Rural-Paraguari rates (boulders quarried locally, lapacho from a Caazapá
# sawmill, palm thatch and Guadua bamboo from co-op producers).
# ---------------------------------------------------------------------------

MATERIAL_TAKEOFF: dict[str, dict] = {
    # 1. Pool excavation + jacuzzi excavation, combined at one rate.
    'pool_excavation_combined': {
        'volume_m3': (
            POOL_LENGTH_M * POOL_WIDTH_M
            * ((POOL_DEPTH_DEEP_M + POOL_DEPTH_SHALLOW_M) / 2.0)
            + JACUZZI_SIZE_M * JACUZZI_SIZE_M * JACUZZI_DEPTH_M
        ),
        'unit_cost_usd': 22.0,
    },
    # 2. Reinforced concrete shell — pool + jacuzzi walls + slab.
    'reinforced_concrete_shell': {
        'volume_m3': (
            2.0 * (POOL_LENGTH_M + POOL_WIDTH_M) * POOL_DEPTH_DEEP_M * 0.20
            + POOL_LENGTH_M * POOL_WIDTH_M * 0.20
            + 4.0 * JACUZZI_SIZE_M * JACUZZI_DEPTH_M * 0.20
            + JACUZZI_SIZE_M * JACUZZI_SIZE_M * 0.20
        ),
        'unit_cost_usd': 320.0,
    },
    # 3. Sandstone coping slabs around pool + jacuzzi perimeter.
    'sandstone_coping_slabs': {
        'length_m': 2.0 * (POOL_LENGTH_M + POOL_WIDTH_M) + 4.0 * JACUZZI_SIZE_M,
        'unit_cost_usd': 95.0,
    },
    # 4. Lapacho deck planks — 12 m × 8 m wrap, ~85 % active (cutout for pool).
    'lapacho_deck_planks': {
        'area_m2': DECK_LENGTH_M * DECK_WIDTH_M - POOL_LENGTH_M * POOL_WIDTH_M,
        'unit_cost_usd': 110.0,
    },
    # 5. Lapacho deck posts (24 × 0.15 × 0.15 × 0.30 m), priced as count.
    'lapacho_deck_posts': {
        'count': DECK_POST_COUNT,
        'unit_cost_usd': 18.0,
    },
    # 6. Pergola: 4 lapacho posts (3 m) + 4 ring-beam culms + 4 corner thatch.
    'pergola_lapacho_bamboo_frame': {
        'length_m': 4.0 * PERGOLA_HEIGHT_M + 4.0 * PERGOLA_SIZE_M,
        'unit_cost_usd': 26.0,
    },
    # 7. Pergola palm-thatch roof, 3 m × 3 m, low pitch overhang included.
    'pergola_palm_thatch_roof': {
        'area_m2': PERGOLA_SIZE_M * PERGOLA_SIZE_M * 1.15,
        'unit_cost_usd': 28.0,
    },
    # 8. Outdoor shower bamboo column + arm + stone slab base.
    'outdoor_shower_assembly': {
        'count': 1,
        'unit_cost_usd': 480.0,
    },
    # 9. Mossy boulder seats (3 × ~0.7 m sphere boulders).
    'boulder_seat_stones': {
        'count': BOULDER_SEAT_COUNT,
        'unit_cost_usd': 180.0,
    },
    # 10. Pool circulation pump + sand filter + 24 h turnover plumbing.
    'pool_circulation_pump_filter': {
        'count': 1,
        'unit_cost_usd': 1850.0,
    },
    # 11. Surrounding flora — 2 Guadua clumps + 2 lapacho saplings.
    'surround_flora_clumps_saplings': {
        'count': 4,
        'unit_cost_usd': 75.0,
    },
}


# ---------------------------------------------------------------------------
# Helpers
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
    """Resolve the first MAT key that exists; ``None`` if none do."""
    for k in keys:
        m = MAT.get(k)
        if m is not None:
            return m
    return None


def _cube(name, location, scale, mat, col):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


# ---------------------------------------------------------------------------
# Pool shell + jacuzzi + water
# ---------------------------------------------------------------------------

def _pool_shell(col, ox, oy):
    """Main pool basin + jacuzzi basin shells (read as river-bottom stone)."""
    mat_shell = _mat('stream_bed', 'sandstone', 'laterite')

    # Main pool basin — sloped floor approximated as a single shallow box.
    # The basin reads from above with the water plane laid on top, so the
    # interior depth gradient need only show as a darker bottom material; we
    # model a single inverted-depression box at the average depth.
    avg_depth = (POOL_DEPTH_DEEP_M + POOL_DEPTH_SHALLOW_M) / 2.0
    _cube(
        name='EcoPool_Basin',
        location=(ox, oy, -avg_depth / 2.0),
        scale=(POOL_LENGTH_M, POOL_WIDTH_M, avg_depth),
        mat=mat_shell,
        col=col,
    )

    # Jacuzzi basin at the NE corner of the main pool (offset +x and +y).
    jacx = ox + POOL_LENGTH_M / 2.0 - JACUZZI_SIZE_M / 2.0
    jacy = oy + POOL_WIDTH_M / 2.0 + JACUZZI_SIZE_M / 2.0
    _cube(
        name='EcoPool_Jacuzzi_Basin',
        location=(jacx, jacy, JACUZZI_CURB_LIFT_M - JACUZZI_DEPTH_M / 2.0),
        scale=(JACUZZI_SIZE_M, JACUZZI_SIZE_M, JACUZZI_DEPTH_M),
        mat=mat_shell,
        col=col,
    )

    # Jacuzzi sandstone curb — a hollow square frame approximated as 4 slabs.
    mat_curb = _mat('sandstone', 'stream_bed')
    curb_w = 0.25
    curb_z = JACUZZI_CURB_LIFT_M / 2.0
    # South curb
    _cube(
        name='EcoPool_Jacuzzi_Curb_S',
        location=(jacx, jacy - JACUZZI_SIZE_M / 2.0 - curb_w / 2.0, curb_z),
        scale=(JACUZZI_SIZE_M + 2 * curb_w, curb_w, JACUZZI_CURB_LIFT_M),
        mat=mat_curb,
        col=col,
    )
    # North curb
    _cube(
        name='EcoPool_Jacuzzi_Curb_N',
        location=(jacx, jacy + JACUZZI_SIZE_M / 2.0 + curb_w / 2.0, curb_z),
        scale=(JACUZZI_SIZE_M + 2 * curb_w, curb_w, JACUZZI_CURB_LIFT_M),
        mat=mat_curb,
        col=col,
    )
    # East curb
    _cube(
        name='EcoPool_Jacuzzi_Curb_E',
        location=(jacx + JACUZZI_SIZE_M / 2.0 + curb_w / 2.0, jacy, curb_z),
        scale=(curb_w, JACUZZI_SIZE_M, JACUZZI_CURB_LIFT_M),
        mat=mat_curb,
        col=col,
    )
    # West curb
    _cube(
        name='EcoPool_Jacuzzi_Curb_W',
        location=(jacx - JACUZZI_SIZE_M / 2.0 - curb_w / 2.0, jacy, curb_z),
        scale=(curb_w, JACUZZI_SIZE_M, JACUZZI_CURB_LIFT_M),
        mat=mat_curb,
        col=col,
    )


def _water_surfaces(col, ox, oy):
    """Pool + jacuzzi water — reflective planes inset slightly from coping."""
    mat = _mat('pool_water', 'water_reflective')

    # Main pool water — surface at z = -0.05 (just below grade), inset 0.10 m.
    _cube(
        name='EcoPool_Water_Main',
        location=(ox, oy, -0.05),
        scale=(POOL_LENGTH_M - 0.1, POOL_WIDTH_M - 0.1, 0.06),
        mat=mat,
        col=col,
    )

    # Jacuzzi water — surface at z = JACUZZI_CURB_LIFT_M - 0.04 (raised).
    jacx = ox + POOL_LENGTH_M / 2.0 - JACUZZI_SIZE_M / 2.0
    jacy = oy + POOL_WIDTH_M / 2.0 + JACUZZI_SIZE_M / 2.0
    _cube(
        name='EcoPool_Water_Jacuzzi',
        location=(jacx, jacy, JACUZZI_CURB_LIFT_M - 0.04),
        scale=(JACUZZI_SIZE_M - 0.1, JACUZZI_SIZE_M - 0.1, 0.05),
        mat=mat,
        col=col,
    )


def _coping(col, ox, oy):
    """Sandstone coping slabs around main pool + jacuzzi perimeters.

    Wesley wants 0.4-0.6 m wide slabs; we lay rectangular slabs along each
    edge with a small Y-jitter index so they don't read as a single extrusion.
    """
    mat = _mat('sandstone', 'stream_bed')

    def lay_along(p_start, p_end, name_prefix, slab_thickness):
        sx, sy = p_start
        ex, ey = p_end
        seg_len = math.hypot(ex - sx, ey - sy)
        n = max(1, int(round(seg_len / COPING_PLANK_WIDTH_M)))
        for i in range(n):
            t = (i + 0.5) / n
            cx = sx + (ex - sx) * t
            cy = sy + (ey - sy) * t
            # Axis-aligned: edge is along x or y; slab oriented accordingly.
            if abs(ex - sx) > abs(ey - sy):
                slab_l, slab_w = COPING_PLANK_WIDTH_M, slab_thickness
            else:
                slab_l, slab_w = slab_thickness, COPING_PLANK_WIDTH_M
            _cube(
                name=f'{name_prefix}_{i:02d}',
                location=(cx, cy, COPING_PLANK_THICKNESS_M / 2.0),
                scale=(slab_l, slab_w, COPING_PLANK_THICKNESS_M),
                mat=mat,
                col=col,
            )

    # Main pool coping — 4 edges, 0.40 m wide perimeter band.
    coping_band = 0.40
    half_l = POOL_LENGTH_M / 2.0 + coping_band / 2.0
    half_w = POOL_WIDTH_M / 2.0 + coping_band / 2.0
    lay_along(
        (ox - POOL_LENGTH_M / 2.0, oy - half_w),
        (ox + POOL_LENGTH_M / 2.0, oy - half_w),
        'EcoPool_Coping_S',
        slab_thickness=coping_band,
    )
    lay_along(
        (ox - POOL_LENGTH_M / 2.0, oy + half_w),
        (ox + POOL_LENGTH_M / 2.0, oy + half_w),
        'EcoPool_Coping_N',
        slab_thickness=coping_band,
    )
    lay_along(
        (ox - half_l, oy - POOL_WIDTH_M / 2.0),
        (ox - half_l, oy + POOL_WIDTH_M / 2.0),
        'EcoPool_Coping_W',
        slab_thickness=coping_band,
    )
    # East edge stops short of the jacuzzi inset
    lay_along(
        (ox + half_l, oy - POOL_WIDTH_M / 2.0),
        (ox + half_l, oy + POOL_WIDTH_M / 2.0 - JACUZZI_SIZE_M),
        'EcoPool_Coping_E',
        slab_thickness=coping_band,
    )


# ---------------------------------------------------------------------------
# Lapacho deck wrap + posts
# ---------------------------------------------------------------------------

def _deck(col, ox, oy):
    """Lapacho plank deck wrapping N/E/W of the pool, 0.15 m above grade.

    The deck is modelled as 3 plank slabs (north strip, east strip, west
    strip) so the pool cut-out is implicit (no Boolean needed). South side
    is the boulder-bench edge — no deck there.
    """
    mat = _mat('lapacho_timber', 'bamboo')
    deck_z = DECK_LIFT_M
    deck_thick = 0.04

    # Deck centred on the pool: deck plan 12 × 8, pool 8 × 4 in centre.
    # Plank strips: north (above pool), east (right of pool), west (left of pool).
    pool_north_edge = oy + POOL_WIDTH_M / 2.0
    pool_south_edge = oy - POOL_WIDTH_M / 2.0
    pool_east_edge = ox + POOL_LENGTH_M / 2.0
    pool_west_edge = ox - POOL_LENGTH_M / 2.0

    deck_north_edge = oy + DECK_WIDTH_M / 2.0
    deck_south_edge = oy - DECK_WIDTH_M / 2.0
    deck_east_edge = ox + DECK_LENGTH_M / 2.0
    deck_west_edge = ox - DECK_LENGTH_M / 2.0

    # North strip — full deck width above pool top edge.
    n_strip_y = (pool_north_edge + deck_north_edge) / 2.0
    n_strip_l = deck_north_edge - pool_north_edge
    _cube(
        name='EcoPool_Deck_N',
        location=(ox, n_strip_y, deck_z),
        scale=(DECK_LENGTH_M, n_strip_l, deck_thick),
        mat=mat,
        col=col,
    )
    # West strip — between deck west edge and pool west edge, runs full y of pool
    w_strip_x = (deck_west_edge + pool_west_edge) / 2.0
    w_strip_w = pool_west_edge - deck_west_edge
    _cube(
        name='EcoPool_Deck_W',
        location=(w_strip_x, oy, deck_z),
        scale=(w_strip_w, POOL_WIDTH_M, deck_thick),
        mat=mat,
        col=col,
    )
    # East strip — between pool east edge and deck east edge, runs full y of pool
    e_strip_x = (pool_east_edge + deck_east_edge) / 2.0
    e_strip_w = deck_east_edge - pool_east_edge
    _cube(
        name='EcoPool_Deck_E',
        location=(e_strip_x, oy, deck_z),
        scale=(e_strip_w, POOL_WIDTH_M, deck_thick),
        mat=mat,
        col=col,
    )
    # South strip — narrow boulder-bench strip (the south face of the deck
    # below pool south edge is where the bench boulders sit).
    s_strip_y = (pool_south_edge + deck_south_edge) / 2.0
    s_strip_l = pool_south_edge - deck_south_edge
    _cube(
        name='EcoPool_Deck_S',
        location=(ox, s_strip_y, deck_z),
        scale=(DECK_LENGTH_M, s_strip_l, deck_thick),
        mat=mat,
        col=col,
    )

    # Deck support posts — 24 at ~2 m centres on the perimeter rim.
    mat_post = _mat('lapacho_timber', 'bamboo')
    perim_pts: list[tuple[float, float]] = []
    n_long = 7  # along x at deck north + deck south
    n_short = 5  # along y at deck east + deck west
    for i in range(n_long):
        t = i / (n_long - 1)
        perim_pts.append((deck_west_edge + (deck_east_edge - deck_west_edge) * t, deck_north_edge))
    for i in range(1, n_short - 1):
        t = i / (n_short - 1)
        perim_pts.append((deck_east_edge, deck_north_edge + (deck_south_edge - deck_north_edge) * t))
    for i in range(n_long):
        t = i / (n_long - 1)
        perim_pts.append((deck_east_edge + (deck_west_edge - deck_east_edge) * t, deck_south_edge))
    for i in range(1, n_short - 1):
        t = i / (n_short - 1)
        perim_pts.append((deck_west_edge, deck_south_edge + (deck_north_edge - deck_south_edge) * t))

    # Trim to exactly DECK_POST_COUNT (24) by uniform sampling.
    if len(perim_pts) > DECK_POST_COUNT:
        step = len(perim_pts) / DECK_POST_COUNT
        perim_pts = [perim_pts[int(i * step)] for i in range(DECK_POST_COUNT)]

    for i, (px, py) in enumerate(perim_pts):
        _cube(
            name=f'EcoPool_DeckPost_{i:02d}',
            location=(px, py, DECK_POST_HEIGHT_M / 2.0),
            scale=(DECK_POST_SIDE_M, DECK_POST_SIDE_M, DECK_POST_HEIGHT_M),
            mat=mat_post,
            col=col,
        )


# ---------------------------------------------------------------------------
# Pergola at SE corner
# ---------------------------------------------------------------------------

def _pergola(col, ox, oy):
    """3 m × 3 m bamboo+lapacho pergola with palm-thatch roof, SE corner.

    Sits on the deck at the south-east, casting shade onto the boulder-bench
    strip. Uses :mod:`lqv.house.bamboo_frame` so the beam ring + thatch panel
    read identically to the rest of the bamboo vocabulary.
    """
    # Centre roughly south-east of the deck centre — over the SE deck strip.
    pcx = ox + DECK_LENGTH_M / 2.0 - PERGOLA_SIZE_M / 2.0 - 0.3
    pcy = oy - DECK_WIDTH_M / 2.0 + PERGOLA_SIZE_M / 2.0 + 0.3
    base_z = DECK_LIFT_M
    half = PERGOLA_SIZE_M / 2.0
    corners = [
        (pcx - half, pcy - half),
        (pcx + half, pcy - half),
        (pcx + half, pcy + half),
        (pcx - half, pcy + half),
    ]

    # 4 lapacho posts, 0.12 m diameter approximation (bamboo_frame uses
    # tapered cylinders — fine, the material says lapacho_timber).
    for i, (cx, cy) in enumerate(corners):
        bamboo_frame.build_bamboo_culm(
            p_start_xyz=(cx, cy, base_z),
            p_end_xyz=(cx, cy, base_z + PERGOLA_HEIGHT_M),
            diameter_m=0.14,
            taper_ratio=0.95,
            material='lapacho_timber',
            name=f'EcoPool_Pergola_Post_{i:02d}',
        )

    # 4 ring-beam bamboo culms at the top — close a square frame.
    beam_z = base_z + PERGOLA_HEIGHT_M
    for i in range(4):
        a = corners[i]
        b = corners[(i + 1) % 4]
        bamboo_frame.build_bamboo_beam(
            p_start_xyz=(a[0], a[1], beam_z),
            p_end_xyz=(b[0], b[1], beam_z),
            diameter_m=0.10,
            material='bamboo',
            name=f'EcoPool_Pergola_Beam_{i:02d}',
        )
        # Lashing at each beam-post joint.
        bamboo_frame.build_bamboo_lashing(
            xyz=(a[0], a[1], beam_z - 0.05),
            radius_m=0.10,
            thickness_m=0.018,
            name=f'EcoPool_Pergola_Lash_{i:02d}',
        )

    # Palm-thatch panel roof — flat panel (low pitch is signalled by deck
    # geometry; the brief calls for "palm-thatch panel roof").
    thatch_overhang = 0.30
    sw = (corners[0][0] - thatch_overhang, corners[0][1] - thatch_overhang, beam_z + 0.05)
    se = (corners[1][0] + thatch_overhang, corners[1][1] - thatch_overhang, beam_z + 0.05)
    ne = (corners[2][0] + thatch_overhang, corners[2][1] + thatch_overhang, beam_z + 0.05)
    nw = (corners[3][0] - thatch_overhang, corners[3][1] + thatch_overhang, beam_z + 0.05)
    panel = bamboo_frame.build_palm_thatch_panel(
        corners_xyz=[sw, se, ne, nw],
        material='palm_thatch',
        name='EcoPool_Pergola_Thatch',
        subdivisions=4,
    )
    _link(panel, col)


# ---------------------------------------------------------------------------
# Outdoor shower at NW corner
# ---------------------------------------------------------------------------

def _outdoor_shower(col, ox, oy):
    """Single bamboo culm 2.5 m vertical + horizontal arm + copper head nub.

    Stone slab base 0.6 × 0.6 m at grade. NW corner of the deck.
    """
    sx = ox - DECK_LENGTH_M / 2.0 + SHOWER_BASE_SIZE_M
    sy = oy + DECK_WIDTH_M / 2.0 - SHOWER_BASE_SIZE_M

    # Stone slab base
    mat_stone = _mat('sandstone', 'stream_bed')
    _cube(
        name='EcoPool_Shower_StoneBase',
        location=(sx, sy, 0.025),
        scale=(SHOWER_BASE_SIZE_M, SHOWER_BASE_SIZE_M, 0.05),
        mat=mat_stone,
        col=col,
    )

    # Vertical bamboo culm
    bamboo_frame.build_bamboo_culm(
        p_start_xyz=(sx, sy, 0.05),
        p_end_xyz=(sx, sy, SHOWER_HEIGHT_M),
        diameter_m=0.09,
        taper_ratio=0.9,
        material='bamboo',
        name='EcoPool_Shower_Mast',
    )

    # Horizontal arm at 2.2 m extending +y (into deck interior)
    arm_z = 2.2
    bamboo_frame.build_bamboo_culm(
        p_start_xyz=(sx, sy, arm_z),
        p_end_xyz=(sx + SHOWER_ARM_LEN_M, sy, arm_z),
        diameter_m=0.06,
        taper_ratio=0.9,
        material='bamboo',
        name='EcoPool_Shower_Arm',
    )

    # Lashing at the elbow joint
    bamboo_frame.build_bamboo_lashing(
        xyz=(sx, sy, arm_z - 0.05),
        radius_m=0.07,
        thickness_m=0.015,
        name='EcoPool_Shower_Lash',
    )

    # Copper shower head nub — small sphere at end of arm
    mat_head = _mat('steel_anodized', 'pv_glass', 'lapacho_timber')
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.07,
        location=(sx + SHOWER_ARM_LEN_M, sy, arm_z - 0.06),
        segments=12,
        ring_count=8,
    )
    head = bpy.context.active_object
    head.name = 'EcoPool_Shower_Head'
    if mat_head is not None:
        assign(head, mat_head)
    _link(head, col)


# ---------------------------------------------------------------------------
# Boulder bench seats — south edge of deck
# ---------------------------------------------------------------------------

def _boulder_bench(col, ox, oy):
    """Three mossy boulders along south edge — bench seating.

    Uses :func:`lqv.amenities._grammar.boulder_seating` to share the labrisa
    vocabulary. Wesley's 'boulder seating' Phase E vocab.
    """
    centre_x = ox
    centre_y = oy - DECK_WIDTH_M / 2.0 - 0.7
    _grammar.boulder_seating(
        col,
        center=(centre_x, centre_y),
        arc_radius_m=2.6,
        boulder_count=BOULDER_SEAT_COUNT,
        boulder_radius_m=0.75,
        arc_span_deg=100.0,
        name_prefix='EcoPool_BoulderSeat',
    )


# ---------------------------------------------------------------------------
# Surround flora — 2 Guadua clumps + 2 lapacho saplings
# ---------------------------------------------------------------------------

def _surround_flora(col, ox, oy):
    """North + east edges: 2 bamboo clumps + 2 lapacho saplings."""
    # 2 Guadua clumps — represented as a small radial bundle of 5 culms each.
    clump_locs = [
        (ox - DECK_LENGTH_M / 2.0 - 1.4, oy + DECK_WIDTH_M / 2.0 + 0.8),
        (ox + DECK_LENGTH_M / 2.0 + 1.4, oy + DECK_WIDTH_M / 2.0 + 0.8),
    ]
    for ci, (cx, cy) in enumerate(clump_locs):
        for j in range(5):
            theta = j * (2.0 * math.pi / 5.0)
            r = 0.18
            bx = cx + r * math.cos(theta)
            by = cy + r * math.sin(theta)
            # Slight lean outward + variable height for natural read.
            lean = 0.08
            tx = bx + lean * math.cos(theta)
            ty = by + lean * math.sin(theta)
            height = 4.6 + 0.4 * ((j * 13) % 5) / 5.0
            culm = bamboo_frame.build_bamboo_culm(
                p_start_xyz=(bx, by, 0.0),
                p_end_xyz=(tx, ty, height),
                diameter_m=0.07,
                taper_ratio=0.85,
                material='bamboo',
                name=f'EcoPool_BambooClump_{ci}_{j:02d}',
            )
            _link(culm, col)

    # 2 lapacho saplings — use photoreal if env requests it, else procedural.
    flora_photoreal = os.environ.get('RENDER_FLORA_PHOTOREAL', '0') == '1'
    sap_xy = [
        (ox + DECK_LENGTH_M / 2.0 + 2.0, oy - 0.5),
        (ox + DECK_LENGTH_M / 2.0 + 2.4, oy + 1.8),
    ]
    if flora_photoreal:
        try:
            from lqv.flora.photoreal import add_lapacho_photoreal
            for sx, sy in sap_xy:
                add_lapacho_photoreal(sx, sy, scale=0.5, flowering=True)
        except Exception as exc:  # noqa: BLE001 — fall back if asset missing
            print(f"[eco_pool] photoreal lapacho unavailable ({exc}); using procedural")
            from lqv.flora.lapacho import add_lapacho
            for sx, sy in sap_xy:
                add_lapacho(sx, sy, scale=0.5, flowering=True)
    else:
        from lqv.flora.lapacho import add_lapacho
        for sx, sy in sap_xy:
            add_lapacho(sx, sy, scale=0.5, flowering=True)


# ---------------------------------------------------------------------------
# Public build entry
# ---------------------------------------------------------------------------

def build(parent=None, location=(0.0, 0.0, 0.0), variant: str = 'A'):
    """Build the Eco Pool wellness amenity at ``location``."""
    name = 'EcoPool'
    col = _ensure_collection(name, parent)
    ox, oy, _oz = location
    _pool_shell(col, ox, oy)
    _water_surfaces(col, ox, oy)
    _coping(col, ox, oy)
    _deck(col, ox, oy)
    _pergola(col, ox, oy)
    _outdoor_shower(col, ox, oy)
    _boulder_bench(col, ox, oy)
    _surround_flora(col, ox, oy)
    return col
