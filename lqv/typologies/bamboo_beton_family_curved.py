"""Typology — Bamboo + Beton Family Curved (~110 m², 4-bed crescent).

Family-scale (Phase E wave 2) hybrid: a banana / crescent plan whose **convex**
back hosts a polished-concrete service spine (kitchen + 2× bath + utility),
and whose **concave** front opens onto a small inner-arc courtyard via a
palm-thatch-roofed deep porch carried by Guadua bamboo columns. The roof is a
single curved shed sloping inward — high (~3.8 m) at the convex wall,
low (~2.6 m) at the concave eave — so the back reads as a tall blank
concrete arc and the front reads as a long low thatched gallery.

Vocabulary lineage: this is the **third** use of the ``bamboo + beton``
vocabulary in the family, after ``bamboo_beton_30`` (couple unit, §3.10) and
``bamboo_beton_28`` (small couple variant). Sibling Phase E wave 2 agent is
factoring shared bamboo helpers into ``lqv.house.bamboo_frame``; this module
**inlines** v30-style helpers locally (the factor was not complete at start-of-
session — see the ``test -f lqv/house/bamboo_frame.py`` probe in the brief).
Switching to the import is a one-line change once that module lands.

Plan geometry (world origin at the centre of the chord, courtyard opens -Y):

* Inner radius **R_i = 9.0 m**, outer radius **R_o = 14.0 m** → 5 m deep
  thickness of habitable bar around the courtyard.
* Arc span **120°**, divided into **24 straight segments** at 5° each
  (no NURBS — segments read fine at sub-render scale).
* Convex (outer) curve faces **+Y / north** — concrete service spine,
  exposed off-form concrete, 2.4 m high parapet rising into the shed's
  high eave at 3.8 m above the deck.
* Concave (inner) curve faces **-Y / south** — bedrooms / living open
  outward into a 9 m-radius inner courtyard via curtain-screened
  openings (no doors on the curve — "tropical openness").
* **9 bamboo porch columns** ring the concave face on a ~13° spacing,
  carrying a curved palm-thatch porch eave at 2.6 m.

Roof: single curved shed swept along the arc. Each of the 24 angular slices
is a quad whose outer-edge top sits at z = 3.8 m and inner-edge top sits at
z = 2.6 m; together the 24 quads read as a smoothly bent shed plane.

Foundation: 60 cm sandstone perimeter course following the inner *and* outer
arcs (Rule 4 — bamboo never touches grade). Lapacho deck floor inside the
crescent, on a 30 cm concrete plinth strip under the convex wall (off-form
concrete shoe matches the service spine above it).

Material fallback chains — identical to ``bamboo_beton_30``:

* ``concrete`` → ``concrete_slab_108`` → ``sandstone`` for the service spine
  + plinth strip.
* ``pv_glass`` → ``water_reflective`` for the few small high-up clerestory
  windows pierced through the concrete spine.
* ``bamboo``, ``palm_thatch``, ``lapacho_timber``, ``sandstone``, ``laterite``
  first-lookup (all present in the MAT registry on every render).

Orientation invariant (consumed by ``lqv/subscene/bamboo_beton_family_curved.py``):
the courtyard opens toward ``-Y``. The SE-oblique sub-render camera at
``(+18, -18, 6.0)`` looking at ``(0, -2, 1.5)`` reads the crescent end-on,
catching the concave porch line and the convex concrete back simultaneously.
"""
from __future__ import annotations

import math

import bpy

from lqv.furniture import furnish_interior
from lqv.materials import MAT, assign

# ---------------------------------------------------------------------------
# Geometry constants (crescent plan, ~110 m², 4 PAX, 4 bedrooms)
# ---------------------------------------------------------------------------

FOOTPRINT_M2 = 110.0
SLEEPS = 6                            # 4 BR sleeps up to 6 with sofa-bed
BEDROOMS = 4
ORIENTATION = 'courtyard_opens_to_negative_Y'
FRAME = 'guadua_bamboo + concrete_service_spine + lapacho_deck'
ROOF_TYPE = 'palm_thatch_curved_shed_swept_along_arc'
SNAP = 'pad'

# Crescent arc parameters
R_INNER = 9.0                         # inner (concave / courtyard) radius
R_OUTER = 14.0                        # outer (convex / service-spine) radius
ARC_SPAN_DEG = 120.0                  # total angular sweep
ARC_SEGMENTS = 24                     # 5° per segment

# Heights
PLINTH_H = 0.30                       # concrete plinth strip under service spine
STONE_COURSE_H = 0.60                 # Rule 4 — earthen/bamboo never touch grade
DECK_THK = 0.08                       # lapacho deck floor thickness
WALL_LOW_H = 2.6                      # concave-eave (porch) top
WALL_HIGH_H = 3.8                     # convex-spine top (high shed eave)
SERVICE_WALL_T = 0.25                 # off-form concrete spine thickness
INNER_PORCH_DEPTH = 1.2               # how far the curved eave projects beyond R_INNER

# Bamboo posts
POST_RADIUS = 0.045                   # 90 mm Ø — porch column scale (larger than v30)
POST_VERTS = 12
NUM_PORCH_POSTS = 9                   # along the concave face

# Lapacho ring beam atop the porch columns
BEAM_W = 0.22
BEAM_H = 0.18

# Roof
ROOF_THK = 0.10                       # palm-thatch slab thickness
ROOF_OVER_INNER = 1.2                 # eave projection past R_INNER inward
ROOF_OVER_OUTER = 0.6                 # eave projection past R_OUTER outward

# Door + glazing
DOOR_W = 0.95
DOOR_H = 2.10
HIGH_WINDOW_W = 0.60                  # clerestories pierced through the convex spine
HIGH_WINDOW_H = 0.35
HIGH_WINDOW_THK = 0.04
NUM_HIGH_WINDOWS = 6
NUM_CURTAIN_BAYS = 8                  # curtain-screened openings between porch posts

ARC_SPAN_RAD = math.radians(ARC_SPAN_DEG)
ARC_START_RAD = -ARC_SPAN_RAD / 2.0   # so the chord is symmetric about +X = 0
ARC_END_RAD = ARC_SPAN_RAD / 2.0

NOTES = (
    'Crescent plan: 120° arc, R_inner=9 m, R_outer=14 m, ~110 m² liveable.',
    'Convex (north) face = polished concrete service spine, 2.4 m tall, '
    'carries kitchen + 2× bath + laundry.',
    'Concave (south) face = 9 bamboo columns, curtain-screened bedroom + '
    'living openings, palm-thatch porch eave at 2.6 m.',
    'Roof: curved shed swept along the arc, high eave 3.8 m at convex, '
    'low eave 2.6 m at concave. Built as 24 quad slices, no NURBS.',
    '60 cm sandstone foundation course follows both arcs (Rule 4).',
    'Lapacho deck floor at 60 cm above grade, sits on the stone foundation.',
    'No doors on the concave curve — heavy curtains for privacy (tropical '
    'openness). Kitchen / bath enter through the concrete spine.',
)


# ---------------------------------------------------------------------------
# MATERIAL_TAKEOFF — Paraguay 2026 USD; target $28-36 k band.
# ---------------------------------------------------------------------------

# Habitable arc area: annulus sector between R_INNER and R_OUTER over ARC_SPAN.
_arc_area = 0.5 * (R_OUTER ** 2 - R_INNER ** 2) * ARC_SPAN_RAD
# Mid-arc length (used for linear takeoffs along the spine)
_R_MID = (R_INNER + R_OUTER) / 2.0
_arc_len_mid = _R_MID * ARC_SPAN_RAD
_arc_len_inner = R_INNER * ARC_SPAN_RAD
_arc_len_outer = R_OUTER * ARC_SPAN_RAD

# Concrete service spine: full outer-arc wall, 2.4 m tall, 25 cm thick,
# plus 30 cm plinth strip under it, plus the wet-pod interior partitions
# (2 bath dividers + laundry wall) on the inner face of the spine.
_concrete_volume = (
    _arc_len_outer * SERVICE_WALL_T * 2.4                       # spine
    + _arc_len_outer * SERVICE_WALL_T * PLINTH_H                # plinth strip under spine
    + 6.0 * 0.15 * 2.2                                          # 6 m of internal wet-pod partitions
    + _arc_len_mid * (R_OUTER - R_INNER) * 0.0                  # (deck slab is lapacho, not concrete — left zero)
    + 1.2 * 0.8 * 0.5                                           # service-step / sink plinth interior
)

# Palm thatch: curved shed roof area + curved porch eave already included
# (the roof is one continuous swept plane from outer-overhang to inner-overhang).
_roof_inner_edge_R = R_INNER - ROOF_OVER_INNER
_roof_outer_edge_R = R_OUTER + ROOF_OVER_OUTER
# Roof projected (plan) area:
_roof_plan_area = 0.5 * (_roof_outer_edge_R ** 2 - _roof_inner_edge_R ** 2) * ARC_SPAN_RAD
# Slope factor: the shed drops 1.2 m over a 5 m radial run → secant ≈ 1.028
_roof_slope_factor = math.hypot(R_OUTER - R_INNER, WALL_HIGH_H - WALL_LOW_H) / max(R_OUTER - R_INNER, 0.001)
_thatch_area = _roof_plan_area * _roof_slope_factor

# Bamboo posts: 9 porch columns at 3.8 m + cross-bracing + railings + decorative
# clerestory mullions.
_bamboo_length = (
    NUM_PORCH_POSTS * (WALL_LOW_H + STONE_COURSE_H)             # porch columns full height incl. foundation pickup
    + NUM_PORCH_POSTS * 1.2                                     # 1.2 m diagonal brace per column
    + _arc_len_inner * 0.5                                      # railing infill (50 % coverage)
    + 30.0                                                      # misc mullions, eave purlins, ridge tie
)

# Lapacho timber: split into two line items (deck and joinery) for clarity.
# Deck = full crescent interior (annular sector) + porch projection inward
# from R_INNER to (R_INNER - ROOF_OVER_INNER). Both are annular slices:
# 0.5 * (r_out² - r_in²) * span.
_porch_proj_area = 0.5 * (R_INNER ** 2 - (R_INNER - ROOF_OVER_INNER) ** 2) * ARC_SPAN_RAD
_deck_area = _arc_area + _porch_proj_area
_deck_volume = _deck_area * DECK_THK
# Joinery = ring beam atop porch posts + 4 BR door frames + 4 BR interior
# closet doors + kitchen cabinetry + curtain rods.
_joinery_volume = (
    _arc_len_inner * BEAM_W * BEAM_H                            # ring beam along concave
    + 4 * (DOOR_W * DOOR_H * 0.05)                              # 4 lapacho doors into the spine
    + 4 * (1.5 * 2.0 * 0.04)                                    # 4 BR closet doors
    + 6.0 * 0.6 * 0.04                                          # kitchen cabinetry face area
    + NUM_CURTAIN_BAYS * (DOOR_W * 0.06 * 0.06)                 # 8 curtain rod/header pieces
)

# Sandstone foundation: both arcs, 40 cm wide, 60 cm tall.
_stone_volume = STONE_COURSE_H * 0.40 * (_arc_len_inner + _arc_len_outer)

# Glazing: 6 small clerestory windows pierced through the convex spine.
_glass_area = NUM_HIGH_WINDOWS * (HIGH_WINDOW_W * HIGH_WINDOW_H)

# Fasteners + lashings — bamboo joinery, roof tie-downs, ring beam to posts,
# curtain hardware.
_fasteners_count = (
    NUM_PORCH_POSTS * 10                                        # 10 lashings per porch column
    + 24 * 6                                                    # 6 fasteners per roof slice (purlin tie-downs)
    + 80                                                        # joinery hinges + brackets
    + 50                                                        # curtain rings + clips
    + 40                                                        # misc
)

# Borax / boric-acid treatment for bamboo (kg-scale; standard 5 % w/w soak
# per Guadua engineering practice).
_borax_kg = _bamboo_length * 0.18                               # ~180 g of borax per m of culm

# Curtain textile (heavy linen / ñandutí blend) for the 8 concave bays.
_curtain_area = NUM_CURTAIN_BAYS * 2.6 * 2.2                    # 8 bays × ~5.7 m² each

# Ceramic kitchen tile (interior face of the concrete spine where the kitchen sits).
_tile_area = 6.0 * 2.4                                          # 6 m kitchen run × 2.4 m height

MATERIAL_TAKEOFF: dict[str, dict] = {
    'concrete_service_spine': {
        'volume_m3': round(_concrete_volume, 2),
        'unit_cost_usd': 320.0,
    },
    'bamboo_culm': {
        'length_m': round(_bamboo_length, 1),
        'unit_cost_usd': 12.0,
    },
    'palm_thatch': {
        'area_m2': round(_thatch_area, 2),
        'unit_cost_usd': 40.0,
    },
    'lapacho_deck': {
        'volume_m3': round(_deck_volume, 3),
        'unit_cost_usd': 1050.0,
    },
    'lapacho_joinery': {
        'volume_m3': round(_joinery_volume, 3),
        'unit_cost_usd': 1300.0,
    },
    'sandstone_foundation': {
        'volume_m3': round(_stone_volume, 2),
        'unit_cost_usd': 330.0,
    },
    'pv_glass_clerestory': {
        'area_m2': round(_glass_area + 1.5, 2),                 # +1.5 m² for 4 lapacho-framed BR vent panels
        'unit_cost_usd': 260.0,
    },
    'fasteners_lashings': {
        'count': int(_fasteners_count),
        'unit_cost_usd': 1.20,
    },
    'borax_boric_treatment': {
        'weight_kg': round(_borax_kg, 1),
        'unit_cost_usd': 9.0,
    },
    'curtain_textile': {
        'area_m2': round(_curtain_area, 1),
        'unit_cost_usd': 28.0,
    },
    'ceramic_kitchen_tile': {
        'area_m2': round(_tile_area, 1),
        'unit_cost_usd': 36.0,
    },
}


# ---------------------------------------------------------------------------
# Helpers (inlined from bamboo_beton_30 — sibling factor not complete at SOS)
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


def _arc_angles():
    """Yield (segment index, theta_start, theta_end, theta_mid) for the 24 slices."""
    step = ARC_SPAN_RAD / ARC_SEGMENTS
    for i in range(ARC_SEGMENTS):
        a0 = ARC_START_RAD + i * step
        a1 = a0 + step
        am = (a0 + a1) / 2.0
        yield i, a0, a1, am


def _polar(r: float, theta: float, oz: float = 0.0):
    """Convert (r, theta) to a world-space (x, y, z). The arc opens toward -Y,
    so we measure theta from the -Y axis (theta=0 → due south). x = +r sin(θ),
    y = -r cos(θ).
    """
    return (r * math.sin(theta), -r * math.cos(theta), oz)


# ---------------------------------------------------------------------------
# Sub-builders
# ---------------------------------------------------------------------------

def _stone_foundation(col, ox, oy):
    """60 cm sandstone perimeter course following inner + outer arcs (Rule 4).

    Built as 24 short trapezoidal cuboids on each arc — at sub-render scale
    the segments read as a smoothly curved stone bench.
    """
    mat = _resolve('sandstone', 'laterite')
    z_mid = STONE_COURSE_H / 2.0
    t = 0.40                          # 40 cm wide
    step = ARC_SPAN_RAD / ARC_SEGMENTS
    seg_len_inner = R_INNER * step    # chord-arc approximation
    seg_len_outer = R_OUTER * step
    for i, _a0, _a1, am in _arc_angles():
        # inner arc
        cx, cy, _ = _polar(R_INNER, am)
        _box(col, f'BBFCv_StoneI_{i:02d}',
             (ox + cx, oy + cy, z_mid),
             (t, seg_len_inner, STONE_COURSE_H),
             mat,
             rotation=(0.0, 0.0, am))
        # outer arc
        cx, cy, _ = _polar(R_OUTER, am)
        _box(col, f'BBFCv_StoneO_{i:02d}',
             (ox + cx, oy + cy, z_mid),
             (t, seg_len_outer, STONE_COURSE_H),
             mat,
             rotation=(0.0, 0.0, am))


def _deck(col, ox, oy):
    """Lapacho deck floor — annular sector between R_INNER and R_OUTER,
    built as 24 trapezoidal slices at z = STONE_COURSE_H.
    """
    mat = _resolve('lapacho_timber')
    z_mid = STONE_COURSE_H + DECK_THK / 2.0
    step = ARC_SPAN_RAD / ARC_SEGMENTS
    radial_thk = R_OUTER - R_INNER
    tangential_len = _R_MID * step
    for i, _a0, _a1, am in _arc_angles():
        cx, cy, _ = _polar(_R_MID, am)
        _box(col, f'BBFCv_Deck_{i:02d}',
             (ox + cx, oy + cy, z_mid),
             (radial_thk, tangential_len, DECK_THK),
             mat,
             rotation=(0.0, 0.0, am))


def _concrete_plinth(col, ox, oy):
    """30 cm concrete plinth strip beneath the outer (convex) service spine."""
    mat = _resolve('concrete_slab_108', 'cob_raw', 'sandstone')
    z_mid = PLINTH_H / 2.0
    step = ARC_SPAN_RAD / ARC_SEGMENTS
    seg_len = R_OUTER * step
    for i, _a0, _a1, am in _arc_angles():
        cx, cy, _ = _polar(R_OUTER, am)
        _box(col, f'BBFCv_Plinth_{i:02d}',
             (ox + cx, oy + cy, z_mid),
             (SERVICE_WALL_T, seg_len, PLINTH_H),
             mat,
             rotation=(0.0, 0.0, am))


def _service_spine(col, ox, oy):
    """Polished-concrete service spine along the convex (outer) arc.

    24 segments, each 5° wide, 25 cm thick, 2.4 m tall, sitting on top of
    the 30 cm concrete plinth strip. Together they read as a single bent
    concrete wall.
    """
    mat = _resolve('concrete_slab_108', 'cob_raw', 'sandstone')
    spine_h = WALL_HIGH_H - PLINTH_H                              # 3.5 m
    z_mid = PLINTH_H + spine_h / 2.0
    step = ARC_SPAN_RAD / ARC_SEGMENTS
    seg_len = R_OUTER * step
    for i, _a0, _a1, am in _arc_angles():
        cx, cy, _ = _polar(R_OUTER, am)
        _box(col, f'BBFCv_Spine_{i:02d}',
             (ox + cx, oy + cy, z_mid),
             (SERVICE_WALL_T, seg_len, spine_h),
             mat,
             rotation=(0.0, 0.0, am))


def _interior_wet_pod_partitions(col, ox, oy):
    """Three short partitions on the inboard face of the spine: 2 bath
    dividers and 1 laundry / mechanical wall. Visible only obliquely.
    """
    mat = _resolve('concrete_slab_108', 'cob_raw', 'sandstone')
    z_mid = PLINTH_H + 1.1
    # Place at theta = -45°, -10°, +35° on the inboard face
    for i, theta_deg in enumerate((-45.0, -10.0, 35.0)):
        theta = math.radians(theta_deg)
        # Move 1.5 m inboard from R_OUTER
        r = R_OUTER - 1.5
        cx, cy, _ = _polar(r, theta)
        _box(col, f'BBFCv_WetPodPart_{i}',
             (ox + cx, oy + cy, z_mid),
             (1.5, 0.15, 2.2),
             mat,
             rotation=(0.0, 0.0, theta))


def _porch_posts(col, ox, oy):
    """9 Guadua bamboo porch columns along the concave (inner) arc.

    Spaced evenly across the 120° span. Each post rises from the top of the
    stone foundation course (z = STONE_COURSE_H) to the ring beam underside
    (z = STONE_COURSE_H + WALL_LOW_H), so column height = WALL_LOW_H = 2.6 m.
    """
    mat = _resolve('bamboo')
    base_z = STONE_COURSE_H
    top_z = base_z + WALL_LOW_H
    z_mid = (base_z + top_z) / 2.0
    height = top_z - base_z
    # Step posts 0..NUM_PORCH_POSTS-1 across the arc (inclusive endpoints)
    for i in range(NUM_PORCH_POSTS):
        t = i / (NUM_PORCH_POSTS - 1)
        theta = ARC_START_RAD + t * ARC_SPAN_RAD
        cx, cy, _ = _polar(R_INNER, theta)
        _cyl(col, f'BBFCv_Post_{i:02d}',
             (ox + cx, oy + cy, z_mid),
             POST_RADIUS, height, mat, vertices=POST_VERTS)
        # Diagonal brace — short kicker from the deck back up to the column
        # 1/3 up from the base. Approximate as a tilted cylinder.
        brace_len = 1.2
        brace_top_z = base_z + height / 3.0
        brace_mid_z = (base_z + brace_top_z) / 2.0
        # Push the brace inboard (toward +R direction) by ~0.6 m
        push = 0.6
        bx = cx + math.sin(theta) * push
        by = cy + (-math.cos(theta)) * push
        _cyl(col, f'BBFCv_Brace_{i:02d}',
             (ox + (cx + bx) / 2.0, oy + (cy + by) / 2.0, brace_mid_z),
             POST_RADIUS * 0.7, brace_len, mat, vertices=8,
             rotation=(math.radians(35.0), 0.0, theta))


def _ring_beam(col, ox, oy):
    """Lapacho ring beam atop the porch posts, following the concave arc.

    24 segments, BEAM_W × BEAM_H, at z = STONE_COURSE_H + WALL_LOW_H.
    """
    mat = _resolve('lapacho_timber')
    z_mid = STONE_COURSE_H + WALL_LOW_H + BEAM_H / 2.0
    step = ARC_SPAN_RAD / ARC_SEGMENTS
    seg_len = R_INNER * step
    for i, _a0, _a1, am in _arc_angles():
        cx, cy, _ = _polar(R_INNER, am)
        _box(col, f'BBFCv_Beam_{i:02d}',
             (ox + cx, oy + cy, z_mid),
             (BEAM_W, seg_len, BEAM_H),
             mat,
             rotation=(0.0, 0.0, am))


def _curved_shed_roof(col, ox, oy):
    """Palm-thatch curved shed roof — single swept plane, high at convex
    (outer) edge, low at concave (inner) edge.

    Built as 24 quad slices. Each slice is a tilted cuboid whose outer
    top corner sits at (R_OUTER+ROOF_OVER_OUTER, WALL_HIGH_H) and whose
    inner top corner sits at (R_INNER-ROOF_OVER_INNER, WALL_LOW_H). The
    cuboid is oriented radially so its tangential dimension matches the
    angular slice width at the mid-radius of the slice.
    """
    mat = _resolve('palm_thatch', 'sod_canopy')
    r_inner_eave = R_INNER - ROOF_OVER_INNER
    r_outer_eave = R_OUTER + ROOF_OVER_OUTER
    radial_span = r_outer_eave - r_inner_eave
    # Height at the outer-eave + inner-eave edges (top of thatch)
    z_high = STONE_COURSE_H + WALL_HIGH_H
    z_low = STONE_COURSE_H + WALL_LOW_H
    # Centroid of the swept slice in the X-Y plane is at the midpoint radius;
    # z-midpoint between the two eaves + half thickness on top.
    r_mid = (r_inner_eave + r_outer_eave) / 2.0
    z_mid = (z_high + z_low) / 2.0 + ROOF_THK / 2.0
    # Slope angle around the *tangent* of the arc (rotation about the local
    # tangential axis, which in world frame is the arc tangent direction).
    drop = z_high - z_low
    slope_rad = math.atan2(drop, radial_span)
    # The slope length (along the tilted plane) — used as the radial scale
    # of the cuboid so the geometry actually spans both eaves.
    slope_len = math.hypot(radial_span, drop)
    step = ARC_SPAN_RAD / ARC_SEGMENTS
    tangential_len_mid = r_mid * step
    for i, _a0, _a1, am in _arc_angles():
        cx, cy, _ = _polar(r_mid, am)
        # Local cuboid scale: radial = slope_len, tangential = arc segment
        # at r_mid, vertical = thickness.
        # We construct the cuboid axis-aligned and then rotate it around Z
        # by `am`, then tilt it around the local tangential axis by
        # `slope_rad`. The local tangential axis at theta=am (radial direction
        # = +sin, -cos) is the orthogonal (+cos, +sin). After Z-rotation by
        # `am`, the local-X aligns with the radial outward direction, so the
        # tilt is around local-Y — which we feed via Euler's Y component
        # *before* the Z rotation (intrinsic XYZ order). Blender's default
        # Euler is XYZ, so passing (0, slope, am) tilts around Y first then
        # rotates around Z — exactly what we want.
        _box(col, f'BBFCv_Roof_{i:02d}',
             (ox + cx, oy + cy, z_mid),
             (slope_len, tangential_len_mid, ROOF_THK),
             mat,
             rotation=(0.0, slope_rad, am))


def _high_clerestory_windows(col, ox, oy):
    """6 small high clerestory windows pierced through the convex spine.

    Placed near the top of the spine, evenly across the arc. These are
    decorative planar glass slabs proud of the concrete — sub-render reads
    them as recessed apertures at the right elevation.
    """
    mat = _resolve('pv_glass', 'water_reflective')
    z_mid = STONE_COURSE_H + WALL_HIGH_H - 0.45                   # near spine top
    for i in range(NUM_HIGH_WINDOWS):
        # Place at fractional positions 0.1, 0.275, 0.45, 0.625, 0.8, 0.95
        t = 0.1 + i * (0.85 / (NUM_HIGH_WINDOWS - 1))
        theta = ARC_START_RAD + t * ARC_SPAN_RAD
        cx, cy, _ = _polar(R_OUTER + 0.13, theta)
        _box(col, f'BBFCv_Cleresto_{i:02d}',
             (ox + cx, oy + cy, z_mid),
             (HIGH_WINDOW_THK, HIGH_WINDOW_W, HIGH_WINDOW_H),
             mat,
             rotation=(0.0, 0.0, theta))


def _spine_doors(col, ox, oy):
    """2 lapacho doors through the concrete spine — kitchen entry + utility
    entry. Placed on the inboard face (R = R_OUTER - SERVICE_WALL_T - 0.03)
    so they read as let-into the concrete wall.
    """
    mat = _resolve('lapacho_timber')
    z_mid = STONE_COURSE_H + DOOR_H / 2.0
    for i, theta_deg in enumerate((-25.0, 30.0)):
        theta = math.radians(theta_deg)
        r = R_OUTER - SERVICE_WALL_T - 0.03
        cx, cy, _ = _polar(r, theta)
        _box(col, f'BBFCv_SpineDoor_{i}',
             (ox + cx, oy + cy, z_mid),
             (0.06, DOOR_W, DOOR_H),
             mat,
             rotation=(0.0, 0.0, theta))


def _curtain_bays(col, ox, oy):
    """Heavy linen curtains hanging in the bays between porch posts.

    Render as thin tall lapacho-coloured rectangles for the curtain header
    and a textile-coloured planar drop. The drop reads as a textile if the
    palm_thatch / sod fallback works, otherwise lapacho fallback.
    """
    mat_rod = _resolve('lapacho_timber')
    # No 'textile' MAT in registry — use a warm fallback that reads as cloth.
    mat_cloth = _resolve('cob_raw', 'lapacho_timber', 'sandstone')
    z_rod = STONE_COURSE_H + WALL_LOW_H - 0.08
    z_cloth_mid = STONE_COURSE_H + (WALL_LOW_H - 0.2) / 2.0 + 0.1
    cloth_h = WALL_LOW_H - 0.4
    # NUM_CURTAIN_BAYS bays between (NUM_PORCH_POSTS = 9) posts → 8 bays.
    for i in range(NUM_CURTAIN_BAYS):
        # Mid-theta between post i and post i+1
        t0 = i / (NUM_PORCH_POSTS - 1)
        t1 = (i + 1) / (NUM_PORCH_POSTS - 1)
        theta = ARC_START_RAD + ((t0 + t1) / 2.0) * ARC_SPAN_RAD
        # Place slightly inboard of R_INNER so the curtain sits behind the porch
        r_cloth = R_INNER + 0.18
        cx, cy, _ = _polar(r_cloth, theta)
        # Curtain bay width = arc length between two adjacent posts at R_INNER
        bay_width = R_INNER * (t1 - t0) * ARC_SPAN_RAD * 0.9
        _box(col, f'BBFCv_Curtain_{i}',
             (ox + cx, oy + cy, z_cloth_mid),
             (0.03, bay_width, cloth_h),
             mat_cloth,
             rotation=(0.0, 0.0, theta))
        # Curtain rod / header (lapacho)
        cx_rod, cy_rod, _ = _polar(R_INNER + 0.10, theta)
        _box(col, f'BBFCv_CurtainRod_{i}',
             (ox + cx_rod, oy + cy_rod, z_rod),
             (0.06, bay_width + 0.10, 0.06),
             mat_rod,
             rotation=(0.0, 0.0, theta))


def _courtyard_step(col, ox, oy):
    """A single low sandstone step at the centre of the inner courtyard —
    landing pad outside the porch line. Reads as the threshold between
    the courtyard ground and the lapacho deck.
    """
    mat = _resolve('sandstone', 'laterite')
    # Place ~3 m south of origin along the courtyard centreline
    cx = 0.0
    cy = -(R_INNER - 3.5)
    _box(col, 'BBFCv_CourtyardStep',
         (ox + cx, oy + cy, 0.10),
         (2.4, 0.6, 0.20),
         mat)


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------

def build_bamboo_beton_family_curved(
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
    parent: bpy.types.Collection | None = None,
    variant: str = 'A',
) -> bpy.types.Collection:
    """Build the Bamboo + Beton Family Curved typology at ``origin``.

    Crescent plan opens toward -Y (south). ``variant`` is currently only
    used for naming — lighting is set by the driver's ``setup_world`` call.
    Idempotent: a second invocation re-uses the existing collection rather
    than duplicating.
    """
    col = _ensure_collection('BambooBeton_FamilyCurved', parent)
    ox, oy, _oz = origin

    _stone_foundation(col, ox, oy)
    _concrete_plinth(col, ox, oy)
    _deck(col, ox, oy)
    _service_spine(col, ox, oy)
    _interior_wet_pod_partitions(col, ox, oy)
    _porch_posts(col, ox, oy)
    _ring_beam(col, ox, oy)
    _curved_shed_roof(col, ox, oy)
    _high_clerestory_windows(col, ox, oy)
    _spine_doors(col, ox, oy)
    _curtain_bays(col, ox, oy)
    _courtyard_step(col, ox, oy)

    # P1.B.1 — interior furniture stubs (RENDER_VIEW=interior readable).
    # Crescent footprint: drop a generous bedroom box on the chord centreline,
    # set into the habitable bar between R_INNER and R_OUTER.
    furnish_interior(
        col,
        footprint_w=4.0,
        footprint_l=6.0,
        origin_xy=(ox, oy + (R_INNER + 1.5)),
        floor_z=STONE_COURSE_H + DECK_THK,
        pax=SLEEPS,
        style='bamboo',
        variant=variant,
        name_prefix='BBFCv_Furn',
    )

    return col


def build(parent: bpy.types.Collection | None = None,
          location: tuple[float, float, float] = (0.0, 0.0, 0.0),
          variant: str = 'A') -> bpy.types.Collection:
    """Legacy alias matching the older typologies API (sibling typologies use this)."""
    return build_bamboo_beton_family_curved(
        origin=location, parent=parent, variant=variant,
    )
