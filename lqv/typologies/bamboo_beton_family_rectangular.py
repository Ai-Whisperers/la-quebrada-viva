"""Typology — Bamboo + Beton Family Rectangular (~110 m², 4-bed rectangle).

Phase E wave 3 sibling of ``bamboo_beton_family_curved``. Same family-scale
hybrid vocabulary (Guadua porch posts + concrete service spine + palm-thatch
shed roof + lapacho deck) but laid out as a **straight rectangle** rather
than a crescent — cheaper to build (no curved formwork, no segmented thatch),
cheaper to bid (~$28-30 k vs. ~$36 k for the curved cousin), and
dimensionally constrained for the long-flat sub-parcels at the western edge
of the 62 ha holding.

Plan geometry (world origin at the building centre, long axis E-W):

* Footprint **6.5 m × 17 m** = 110.5 m² (interior + porch). Long axis E-W
  so the long faces present north and south to the SE-oblique hero camera.
* **North long face**: concrete service spine — kitchen + 2× bath +
  utility wall, 0.18 m thick reinforced concrete, full 17 m length,
  **high eave** at z = 3.6 m (the shed apex).
* **South long face**: bamboo + lapacho post-and-beam open colonnade —
  **9 Guadua posts** along a 17 m × 3 m porch with a palm-thatch shed
  eave at **z = 2.4 m** (the shed low eave).
* **East / west gables**: 0.6 m sandstone foundation course + plywood-and-
  lapacho-board cladding above. The **west gable** carries the master-
  bedroom French doors onto a 3 m × 2 m private lapacho deck; the **east
  gable** stays solid except for one high vent louver.
* **Roof**: single-slope **shed roof**, palm thatch over bamboo rafters at
  ~0.5 m centres — high (3.6 m) on the **north concrete face**, low (2.4 m)
  on the **south porch**. Opposite drop direction from the curved cousin
  (which is high on the convex / north spine and low on the concave / south
  eave) — here the spine is *also* north and the porch is the *low* side,
  so the shed sheds water southward into the porch gutter.
* **Foundation**: 60 cm sandstone perimeter course around the entire
  6.5 m × 17 m footprint (Rule 4 — earthen / bamboo surfaces never touch
  grade).
* **Indoor floor**: lapacho deck planks at z = 0.6 m (top of foundation),
  thickness 8 cm.

Material vocabulary (fallback chains — all identical to the curved sibling
so the family reads as a single design language on the typology-grid render):

* ``concrete_slab_108`` → ``cob_raw`` → ``sandstone`` for the service spine
  + concrete plinth strip under it.
* ``pv_glass`` → ``water_reflective`` for the high east-gable vent louver
  and the small west-gable French door glazing.
* ``bamboo``, ``palm_thatch``, ``lapacho_timber``, ``sandstone``, ``laterite``,
  ``terracotta_tile`` first-lookup (all present in the MAT registry on every
  render).

Lineage notes — Phase E wave 3 explicitly imports the wave-2-factored bamboo
helpers from ``lqv.house.bamboo_frame`` (``build_bamboo_culm``,
``build_bamboo_post_stack``, ``build_bamboo_beam``, ``build_palm_thatch_panel``,
``build_bamboo_lashing``) and the stone-foundation helper from
``lqv.house.stone_wall`` (``build_stone_foundation_course``). The curved
sibling still inlines its v30-style helpers; this rectangular file is the
first family-scale member to consume the factored surface.

Concrete spine is **inlined** here as a 17 m × 0.18 m × 3.3 m cuboid plus a
30 cm plinth strip; a future ``lqv/house/concrete_spine.py`` factor would
collapse the same logic with the curved cousin's spine — TODO for wave 4
(tracked: TaskList #39).

Orientation invariant (consumed by
``lqv/subscene/bamboo_beton_family_rectangular.py``): the building straddles
the X axis (long axis E-W), the concrete spine sits at +Y, the porch sits at
-Y. The SE-oblique sub-render camera at ``(+14, -14, 6)`` looking at
``(0, -1.5, 1.5)`` reads the north spine and the south porch in the same
frame.
"""
from __future__ import annotations

import math

import bpy

from lqv.house.bamboo_frame import (
    build_bamboo_beam,
    build_bamboo_culm,
    build_bamboo_lashing,
    build_bamboo_post_stack,
    build_palm_thatch_panel,
)
from lqv.house.stone_wall import build_stone_foundation_course
from lqv.materials import MAT, assign

# ---------------------------------------------------------------------------
# Geometry constants (rectangular plan, ~110 m², 4 BR / 6 PAX)
# ---------------------------------------------------------------------------

FOOTPRINT_M2 = 110.5
SLEEPS = 6                            # 4 BR sleeps up to 6 with sofa-bed
BEDROOMS = 4
ORIENTATION = 'long_axis_east_west_porch_opens_south'
FRAME = 'guadua_bamboo + concrete_service_spine + lapacho_deck'
ROOF_TYPE = 'palm_thatch_single_slope_shed_high_north_low_south'
SNAP = 'pad'

# Rectangle footprint (interior + porch combined)
PLAN_W = 6.5                          # short axis (N-S), interior + porch
PLAN_L = 17.0                         # long axis (E-W)
INTERIOR_W = 4.0                      # interior depth (porch takes 2.5 m)
PORCH_W = 3.0                         # 3 m porch zone overlaps 0.5 m onto interior face

# Heights
PLINTH_H = 0.30                       # concrete plinth strip under spine
STONE_COURSE_H = 0.60                 # Rule 4 — earthen/bamboo never touch grade
DECK_THK = 0.05                       # lapacho tongue-and-groove plank, 5 cm
WALL_LOW_H = 2.4                      # south porch eave (low side)
WALL_HIGH_H = 3.6                     # north spine eave (high side)
SERVICE_WALL_T = 0.18                 # reinforced concrete spine thickness
GABLE_WALL_T = 0.14                   # plywood + lapacho gable cladding thickness

# Bamboo porch
POST_DIAMETER = 0.09                  # 90 mm Ø porch column
NUM_PORCH_POSTS = 9                   # at ~2.0 m centres along 16.2 m run

# Lapacho ring beam atop the porch posts
BEAM_W = 0.20
BEAM_H = 0.16

# Roof
ROOF_THK = 0.10
ROOF_OVER_NORTH = 0.6                 # eave overhang past north spine
ROOF_OVER_SOUTH = 1.2                 # eave overhang past south porch line (Rule 5)
ROOF_OVER_GABLE = 0.6                 # gable-end overhangs (east + west)

# Door + glazing
DOOR_W = 0.95
DOOR_H = 2.10
FRENCH_DOOR_W = 1.6
FRENCH_DOOR_H = 2.10
EAST_LOUVER_W = 0.9
EAST_LOUVER_H = 0.4
EAST_LOUVER_THK = 0.04
NUM_RAFTERS = int(round(PLAN_L / 0.5))  # bamboo rafters at 0.5 m centres → 34

# Private master deck (west gable)
MASTER_DECK_W = 3.0
MASTER_DECK_D = 2.0
MASTER_DECK_THK = 0.05


NOTES = (
    'Rectangle plan: 6.5 m × 17 m, long axis E-W, ~110 m² liveable.',
    'North long face (Y=+3.16) = polished concrete service spine, 17 m × '
    '3.3 m × 0.18 m thick, carries kitchen + 2× bath + laundry.',
    'South long face (Y=-3.15) = 9 Guadua porch posts carrying a lapacho '
    'ring beam + palm-thatch shed eave at z = 2.4 m.',
    'Roof: single-slope shed, high (3.6 m) on north concrete face, low '
    '(2.4 m) on south porch. Bamboo rafters at 0.5 m centres.',
    '60 cm sandstone foundation course around the full perimeter (Rule 4).',
    'Lapacho deck floor at z = 0.6 m sits on the stone foundation.',
    'Master BR (west) opens onto a 3 m × 2 m private lapacho deck via '
    'French doors. East gable is solid except for one high vent louver.',
    'Imports build_bamboo_culm / build_bamboo_post_stack / build_bamboo_beam '
    '/ build_palm_thatch_panel / build_bamboo_lashing from '
    'lqv.house.bamboo_frame; build_stone_foundation_course from '
    'lqv.house.stone_wall. Concrete spine inlined — TODO factor in wave 4 '
    '(tracked: TaskList #40).',
)


# ---------------------------------------------------------------------------
# MATERIAL_TAKEOFF — Paraguay 2026 USD; target $26-32 k band.
# ---------------------------------------------------------------------------

# Concrete service spine: 17 m × 3.3 m × 0.18 m + 30 cm plinth strip
# below it + 6 m of interior wet-pod partitions.
_spine_h = WALL_HIGH_H - PLINTH_H                 # 3.3 m above the plinth
_concrete_volume = (
    PLAN_L * SERVICE_WALL_T * _spine_h            # spine wall
    + PLAN_L * SERVICE_WALL_T * PLINTH_H          # plinth strip under spine
    + 6.0 * 0.12 * 2.2                            # 6 m of interior wet-pod partitions
    + 1.0 * 0.6 * 0.4                             # service-step / sink plinth
)

# Bamboo: 9 porch posts + rafters at 0.5 m centres + diagonal braces +
# bamboo cladding strip on the south porch ceiling.
_post_h = WALL_LOW_H                              # 2.4 m above stone course top
# Rafter horizontal run: PLAN_W + N overhang + S overhang = 8.3 m.
_rafter_horiz = PLAN_W + ROOF_OVER_NORTH + ROOF_OVER_SOUTH
_rafter_drop = WALL_HIGH_H - WALL_LOW_H           # 1.2 m
_rafter_len = math.hypot(_rafter_horiz, _rafter_drop)
_bamboo_length = (
    NUM_PORCH_POSTS * (_post_h + STONE_COURSE_H)  # full-height porch posts
    + NUM_PORCH_POSTS * 1.2                       # 1.2 m diagonal brace per post
    + NUM_RAFTERS * _rafter_len                   # bamboo rafters at 0.5 m centres
    + 30.0                                        # misc purlins, ridge tie, ceiling slats
)

# Palm thatch: shed roof projected over (PLAN_W + N + S overhangs) × (PLAN_L +
# 2× gable overhangs), times the slope factor (secant of the pitch).
_roof_plan_area = (
    (PLAN_W + ROOF_OVER_NORTH + ROOF_OVER_SOUTH)
    * (PLAN_L + 2 * ROOF_OVER_GABLE)
)
_roof_slope_factor = _rafter_len / max(_rafter_horiz, 0.001)
_thatch_area = _roof_plan_area * _roof_slope_factor

# Lapacho timber: split into deck and joinery for clarity.
_interior_deck_area = INTERIOR_W * PLAN_L
_porch_deck_area = PORCH_W * PLAN_L
_master_deck_area = MASTER_DECK_W * MASTER_DECK_D
_deck_area_total = _interior_deck_area + _porch_deck_area + _master_deck_area
_deck_volume = _deck_area_total * DECK_THK
# Joinery = ring beam (17 m × 0.20 × 0.16) + 4 BR door frames + closet doors +
# kitchen cabinetry face + French door frames + gable cladding boards.
_joinery_volume = (
    PLAN_L * BEAM_W * BEAM_H                      # ring beam along south porch
    + 4 * (DOOR_W * DOOR_H * 0.05)                # 4 lapacho interior doors
    + 4 * (1.5 * 2.0 * 0.04)                      # 4 BR closet doors
    + 6.0 * 0.6 * 0.04                            # kitchen cabinetry face area
    + FRENCH_DOOR_W * FRENCH_DOOR_H * 0.06        # west French door frame
    + 2 * (PLAN_W * 2.4 * 0.025)                  # 2 gable interior cladding boards
)

# Sandstone foundation: perimeter course, 40 cm wide, 60 cm tall.
_perimeter_m = 2 * (PLAN_W + PLAN_L)              # 47 m
_stone_volume = STONE_COURSE_H * 0.40 * _perimeter_m

# Plywood + lapacho gable cladding: 2 gable wall panels above the foundation.
_plywood_area = 2 * PLAN_W * ((WALL_HIGH_H + WALL_LOW_H) / 2.0)

# Glazing: east louver + west French door panes.
_glass_area = (EAST_LOUVER_W * EAST_LOUVER_H) + (FRENCH_DOOR_W * (FRENCH_DOOR_H - 0.3))

# Fasteners + lashings — bamboo joinery + roof tie-downs + door hinges.
_fasteners_count = (
    NUM_PORCH_POSTS * 8                           # 8 lashings per porch column
    + NUM_RAFTERS * 2                             # 2 fasteners per rafter (top + bottom)
    + 80                                          # joinery hinges + brackets
    + 40                                          # misc
)

# Borax / boric-acid treatment for bamboo (kg-scale).
_borax_kg = _bamboo_length * 0.18                 # ~180 g per m of culm

# Ceramic kitchen tile strip on the inboard face of the kitchen.
_tile_area = 6.0 * 2.4

# Reinforcing steel for the concrete spine (rebar — straight bars, no bends).
_rebar_kg = _concrete_volume * 95.0               # 95 kg/m³ reinforced wall standard

MATERIAL_TAKEOFF: dict[str, dict] = {
    'concrete_service_spine': {
        'volume_m3': round(_concrete_volume, 2),
        'unit_cost_usd': 295.0,                   # rectangular formwork cheaper than curved 320
    },
    'bamboo_culm': {
        'length_m': round(_bamboo_length, 1),
        'unit_cost_usd': 11.0,
    },
    'palm_thatch': {
        'area_m2': round(_thatch_area, 2),
        'unit_cost_usd': 30.0,                    # flat shed pitches cheaper to lay than curved
    },
    'lapacho_deck': {
        'volume_m3': round(_deck_volume, 3),
        'unit_cost_usd': 880.0,                   # bulk plank lapacho, t&g, locally milled
    },
    'lapacho_joinery': {
        'volume_m3': round(_joinery_volume, 3),
        'unit_cost_usd': 1300.0,
    },
    'sandstone_foundation': {
        'volume_m3': round(_stone_volume, 2),
        'unit_cost_usd': 330.0,
    },
    'plywood_lapacho_gable': {
        'area_m2': round(_plywood_area, 1),
        'unit_cost_usd': 48.0,
    },
    'pv_glass_glazing': {
        'area_m2': round(_glass_area, 2),
        'unit_cost_usd': 240.0,
    },
    'fasteners_lashings': {
        'count': int(_fasteners_count),
        'unit_cost_usd': 1.20,
    },
    'borax_boric_treatment': {
        'weight_kg': round(_borax_kg, 1),
        'unit_cost_usd': 9.0,
    },
    'ceramic_kitchen_tile': {
        'area_m2': round(_tile_area, 1),
        'unit_cost_usd': 36.0,
    },
    'rebar_steel': {
        'weight_kg': round(_rebar_kg, 1),
        'unit_cost_usd': 1.45,
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve(*keys: str):
    """Return the first MAT key that exists; None if none do."""
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


def _box(col, name, location, scale, mat, rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


# ---------------------------------------------------------------------------
# Sub-builders
# ---------------------------------------------------------------------------

def _stone_foundation(col, ox, oy):
    """Rule-4 sandstone perimeter course around the full 6.5 m × 17 m
    footprint. Uses the factored ``build_stone_foundation_course`` helper.

    The helper adds a 20 cm overhang on each side, so we pass the *exact*
    building footprint (6.5 m × 17 m) and the resulting plinth will read as
    6.9 m × 17.4 m — a deliberate course that sits proud of the walls.
    """
    obj = build_stone_foundation_course(
        x=ox + 0.0, y=oy + 0.0,
        width_m=PLAN_L, depth_m=PLAN_W,
        height_m=STONE_COURSE_H,
        material='stone_foundation',
        fallback='sandstone',
        name='BBFRect_StoneFoundation',
        collection=col,
    )
    return obj


def _concrete_plinth(col, ox, oy):
    """30 cm concrete plinth strip under the north service spine.

    Sits between the stone course top (z = 0.6) and the spine base (z = 0.9).
    Spine sits along the north long face at Y = PLAN_W/2 - SERVICE_WALL_T/2.
    """
    mat = _resolve('concrete_slab_108', 'cob_raw', 'sandstone')
    spine_y = PLAN_W / 2.0 - SERVICE_WALL_T / 2.0  # +3.16
    z_mid = STONE_COURSE_H + PLINTH_H / 2.0
    _box(col, 'BBFRect_Plinth',
         (ox + 0.0, oy + spine_y, z_mid),
         (PLAN_L, SERVICE_WALL_T, PLINTH_H),
         mat)


def _service_spine(col, ox, oy):
    """Polished-concrete service spine along the north long face.

    17 m long × 0.18 m thick × 3.3 m tall (sits atop the 30 cm plinth →
    top at z = 0.6 + 0.3 + 3.3 = 4.2 m, matching the shed high eave at
    STONE_COURSE_H + WALL_HIGH_H = 4.2 m). The spine carries kitchen + 2 bath
    + laundry — the entire wet program — and is the north wall of the house.
    """
    mat = _resolve('concrete_slab_108', 'cob_raw', 'sandstone')
    spine_y = PLAN_W / 2.0 - SERVICE_WALL_T / 2.0  # +3.16
    spine_top = STONE_COURSE_H + WALL_HIGH_H       # 4.2
    spine_base = STONE_COURSE_H + PLINTH_H         # 0.9
    spine_h = spine_top - spine_base               # 3.3
    z_mid = (spine_top + spine_base) / 2.0
    _box(col, 'BBFRect_Spine',
         (ox + 0.0, oy + spine_y, z_mid),
         (PLAN_L, SERVICE_WALL_T, spine_h),
         mat)


def _interior_wet_pod_partitions(col, ox, oy):
    """Three short interior partitions on the inboard face of the spine:
    2 bath dividers + 1 laundry / mechanical wall. Visible only obliquely
    from the SE hero camera.
    """
    mat = _resolve('concrete_slab_108', 'cob_raw', 'sandstone')
    z_mid = STONE_COURSE_H + 1.1 + 0.5
    cy = PLAN_W / 2.0 - SERVICE_WALL_T - 0.75
    for i, px in enumerate((-4.5, 0.5, 5.5)):
        _box(col, f'BBFRect_WetPodPart_{i}',
             (ox + px, oy + cy, z_mid),
             (0.12, 1.5, 2.2),
             mat)


def _deck(col, ox, oy):
    """Lapacho deck floor — covers the full 6.5 m × 17 m footprint at
    z = STONE_COURSE_H = 0.6. Porch + interior share the same plane (open-
    deck Paraguayan vernacular convention).
    """
    mat = _resolve('lapacho_timber')
    z_mid = STONE_COURSE_H + DECK_THK / 2.0
    _box(col, 'BBFRect_Deck',
         (ox + 0.0, oy + 0.0, z_mid),
         (PLAN_L, PLAN_W, DECK_THK),
         mat)


def _master_private_deck(col, ox, oy):
    """3 m × 2 m private lapacho deck off the master BR (west gable).

    Sits at z = STONE_COURSE_H + DECK_THK/2 (same plane as main deck) and
    projects westward from the gable by MASTER_DECK_W = 3.0 m.
    """
    mat = _resolve('lapacho_timber')
    z_mid = STONE_COURSE_H + MASTER_DECK_THK / 2.0
    cx = -PLAN_L / 2.0 - MASTER_DECK_W / 2.0
    cy = (PLAN_W - MASTER_DECK_D) / 2.0 - 0.5     # ~+1.25, on the north interior side
    _box(col, 'BBFRect_MasterDeck',
         (ox + cx, oy + cy, z_mid),
         (MASTER_DECK_W, MASTER_DECK_D, MASTER_DECK_THK),
         mat)


def _porch_posts(col, ox, oy):
    """9 Guadua porch posts along the south face.

    Uses the factored ``build_bamboo_post_stack`` helper. Posts span from
    z = STONE_COURSE_H (top of stone plinth) to z = STONE_COURSE_H + WALL_LOW_H
    = 3.0 m above grade.

    Post line runs at Y = -PLAN_W/2 + 0.10 = -3.15 (just inside the south
    foundation course edge), from X = -PLAN_L/2 + 0.4 to X = +PLAN_L/2 - 0.4.
    The factored helper rounds spacing to land posts exactly on the endpoints
    — we give it a target spacing that yields NUM_PORCH_POSTS along the run.
    """
    south_y = -PLAN_W / 2.0 + 0.10
    x0 = -PLAN_L / 2.0 + 0.4
    x1 = +PLAN_L / 2.0 - 0.4
    target_spacing = (x1 - x0) / (NUM_PORCH_POSTS - 1)
    posts = build_bamboo_post_stack(
        footprint_corners=[(x0 + ox, south_y + oy), (x1 + ox, south_y + oy)],
        height_m=WALL_LOW_H,
        base_z=STONE_COURSE_H,
        post_diameter_m=POST_DIAMETER,
        spacing_m=target_spacing,
        material='bamboo',
        name_prefix='BBFRect_PorchPost',
    )
    for p in posts:
        _link(p, col)

    # Diagonal kicker brace per post (1.2 m, pushed inboard toward +Y by 0.6 m).
    for i, p in enumerate(posts):
        px, py, _pz = p.location
        base_z = STONE_COURSE_H
        brace_top_z = base_z + WALL_LOW_H / 3.0
        bx = px
        by = py + 0.6
        bz = brace_top_z
        brace = build_bamboo_culm(
            p_start_xyz=(px, py, base_z),
            p_end_xyz=(bx, by, bz),
            diameter_m=POST_DIAMETER * 0.7,
            taper_ratio=0.9,
            segments=8,
            material='bamboo',
            name=f'BBFRect_PorchBrace_{i:02d}',
        )
        _link(brace, col)

        # Decorative lashing at each post-to-beam joint
        lashing = build_bamboo_lashing(
            xyz=(px, py, base_z + WALL_LOW_H - 0.05),
            radius_m=0.08,
            thickness_m=0.025,
            material='fasteners_lashings',
            fallback='lapacho_timber',
            name=f'BBFRect_PorchLashing_{i:02d}',
        )
        _link(lashing, col)


def _ring_beam(col, ox, oy):
    """Lapacho ring beam atop the porch posts, running the full 17 m length
    along the south porch line at Y = -3.15.

    Uses the factored ``build_bamboo_beam`` helper (semantic alias of culm
    for horizontal members).
    """
    south_y = -PLAN_W / 2.0 + 0.10
    beam_z = STONE_COURSE_H + WALL_LOW_H + BEAM_H / 2.0
    x0 = -PLAN_L / 2.0 + 0.4
    x1 = +PLAN_L / 2.0 - 0.4
    beam = build_bamboo_beam(
        p_start_xyz=(x0 + ox, south_y + oy, beam_z),
        p_end_xyz=(x1 + ox, south_y + oy, beam_z),
        diameter_m=BEAM_W,
        material='lapacho_timber',
        name='BBFRect_RingBeam',
    )
    _link(beam, col)


def _shed_roof(col, ox, oy):
    """Single-slope palm-thatch shed roof — high (3.6 m) on the north
    concrete spine, low (2.4 m) on the south porch ring beam.

    Built as a single bilinear quad panel via the factored
    ``build_palm_thatch_panel`` (4 corners SW, SE, NE, NW), plus a bamboo
    rafter array spaced ~0.5 m along the X axis, each spanning from the
    south-porch beam to the north-spine top.
    """
    south_y = -PLAN_W / 2.0 - ROOF_OVER_SOUTH
    north_y = +PLAN_W / 2.0 + ROOF_OVER_NORTH
    east_x = +PLAN_L / 2.0 + ROOF_OVER_GABLE
    west_x = -PLAN_L / 2.0 - ROOF_OVER_GABLE
    z_south = STONE_COURSE_H + WALL_LOW_H
    z_north = STONE_COURSE_H + WALL_HIGH_H
    corners = [
        (west_x + ox, south_y + oy, z_south),     # SW
        (east_x + ox, south_y + oy, z_south),     # SE
        (east_x + ox, north_y + oy, z_north),     # NE
        (west_x + ox, north_y + oy, z_north),     # NW
    ]
    panel = build_palm_thatch_panel(
        corners_xyz=corners,
        material='palm_thatch',
        name='BBFRect_ThatchRoof',
        subdivisions=6,
    )
    _link(panel, col)

    # Bamboo rafters at ~0.5 m centres along X.
    rafter_offset_z = -0.06                       # rafters sit just under the thatch
    for i in range(NUM_RAFTERS + 1):
        t = i / NUM_RAFTERS
        rx = west_x + t * (east_x - west_x)
        p_start = (rx + ox, south_y + oy, z_south + rafter_offset_z)
        p_end = (rx + ox, north_y + oy, z_north + rafter_offset_z)
        rafter = build_bamboo_culm(
            p_start_xyz=p_start,
            p_end_xyz=p_end,
            diameter_m=0.07,
            taper_ratio=0.95,
            segments=8,
            material='bamboo',
            name=f'BBFRect_Rafter_{i:02d}',
        )
        _link(rafter, col)


def _gable_walls(col, ox, oy):
    """East + west gable cladding — plywood + lapacho board above the
    foundation course. Built as 2 thin cuboids that fill the rectangle
    portion of the gable face; the sloped triangle infill is handled by
    ``_gable_triangles``.
    """
    mat = _resolve('lapacho_timber', 'sandstone')
    avg_h = (WALL_HIGH_H + WALL_LOW_H) / 2.0
    z_mid = STONE_COURSE_H + avg_h / 2.0
    for sign, name in ((+1, 'East'), (-1, 'West')):
        cx = sign * (PLAN_L / 2.0 + GABLE_WALL_T / 2.0)
        _box(col, f'BBFRect_Gable{name}',
             (ox + cx, oy + 0.0, z_mid),
             (GABLE_WALL_T, PLAN_W, avg_h),
             mat)


def _gable_triangles(col, ox, oy):
    """Sloped strip above the rectangle wall capturing the actual roof
    edge. Modelled as a low-height cap rather than a true triangle since
    the roof slope is small (1.2 m drop across 6.5 m run).
    """
    mat = _resolve('lapacho_timber', 'sandstone')
    cap_h = (WALL_HIGH_H - WALL_LOW_H) / 2.0
    z_mid = STONE_COURSE_H + (WALL_HIGH_H + WALL_LOW_H) / 2.0 + cap_h / 2.0
    for sign, name in ((+1, 'East'), (-1, 'West')):
        cx = sign * (PLAN_L / 2.0 + GABLE_WALL_T / 2.0)
        _box(col, f'BBFRect_GableCap{name}',
             (ox + cx, oy + 0.5, z_mid),
             (GABLE_WALL_T, PLAN_W * 0.6, cap_h),
             mat)


def _spine_doors(col, ox, oy):
    """Two lapacho doors through the concrete spine — kitchen entry +
    utility entry. Placed on the inboard (south-facing) face of the spine.
    """
    mat = _resolve('lapacho_timber')
    z_mid = STONE_COURSE_H + DOOR_H / 2.0
    spine_y_inboard = PLAN_W / 2.0 - SERVICE_WALL_T - 0.03
    for i, px in enumerate((-3.0, +4.0)):
        _box(col, f'BBFRect_SpineDoor_{i}',
             (ox + px, oy + spine_y_inboard, z_mid),
             (DOOR_W, 0.06, DOOR_H),
             mat)


def _french_doors(col, ox, oy):
    """French door on the west gable to the master deck.

    Built as a thin pv_glass slab — the lapacho frame is implicit at this
    render scale.
    """
    mat = _resolve('pv_glass', 'water_reflective')
    z_mid = STONE_COURSE_H + FRENCH_DOOR_H / 2.0
    cx = -PLAN_L / 2.0 - GABLE_WALL_T - 0.05
    cy = 0.5                                       # north interior side
    _box(col, 'BBFRect_FrenchDoor',
         (ox + cx, oy + cy, z_mid),
         (0.04, FRENCH_DOOR_W, FRENCH_DOOR_H),
         mat)


def _east_louver(col, ox, oy):
    """High vent louver on the east gable — small pv_glass slab near the
    eave, ventilates the bath stacks.
    """
    mat = _resolve('pv_glass', 'water_reflective')
    z_mid = STONE_COURSE_H + WALL_HIGH_H - 0.5
    cx = +PLAN_L / 2.0 + GABLE_WALL_T + 0.03
    _box(col, 'BBFRect_EastLouver',
         (ox + cx, oy + 1.5, z_mid),
         (EAST_LOUVER_THK, EAST_LOUVER_W, EAST_LOUVER_H),
         mat)


def _kitchen_tile_strip(col, ox, oy):
    """Decorative ceramic tile strip on the inboard face of the kitchen
    section of the concrete spine — 6 m × 0.6 m band at counter height.
    """
    mat = _resolve('terracotta_tile', 'cob_raw', 'sandstone')
    z_mid = STONE_COURSE_H + 1.2
    spine_y_inboard = PLAN_W / 2.0 - SERVICE_WALL_T - 0.05
    _box(col, 'BBFRect_KitchenTile',
         (ox + 1.0, oy + spine_y_inboard, z_mid),
         (6.0, 0.04, 0.6),
         mat)


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------

def build_bamboo_beton_family_rectangular(
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
    parent: bpy.types.Collection | None = None,
    variant: str = 'A',
) -> bpy.types.Collection:
    """Build the Bamboo + Beton Family Rectangular typology at ``origin``.

    Rectangular plan, long axis E-W, porch opens to -Y (south) and concrete
    spine sits at +Y (north). ``variant`` is currently only used for naming
    — lighting is set by the driver's ``setup_world`` call. Idempotent: a
    second invocation re-uses the existing collection rather than
    duplicating.
    """
    col = _ensure_collection('BambooBeton_FamilyRectangular', parent)
    ox, oy, _oz = origin

    _stone_foundation(col, ox, oy)
    _concrete_plinth(col, ox, oy)
    _deck(col, ox, oy)
    _master_private_deck(col, ox, oy)
    _service_spine(col, ox, oy)
    _interior_wet_pod_partitions(col, ox, oy)
    _porch_posts(col, ox, oy)
    _ring_beam(col, ox, oy)
    _shed_roof(col, ox, oy)
    _gable_walls(col, ox, oy)
    _gable_triangles(col, ox, oy)
    _spine_doors(col, ox, oy)
    _french_doors(col, ox, oy)
    _east_louver(col, ox, oy)
    _kitchen_tile_strip(col, ox, oy)

    return col


def build(parent: bpy.types.Collection | None = None,
          location: tuple[float, float, float] = (0.0, 0.0, 0.0),
          variant: str = 'A') -> bpy.types.Collection:
    """Legacy alias matching the older typologies API (sibling typologies use this)."""
    return build_bamboo_beton_family_rectangular(
        origin=location, parent=parent, variant=variant,
    )
