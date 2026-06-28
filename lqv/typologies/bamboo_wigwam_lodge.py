"""Typology — Bamboo Wigwam Lodge (Phase E, 2026-06-12).

Small glamping unit: a fat-bottomed conical bamboo-frame structure clad in
palm thatch, NOT a canvas tipi. 2 PAX. ~5 m base diameter, ~4.5 m tall to
apex. 16 leaning Guadua culms meet at a clustered apex (lashed, no metal
sleeve). Palm-thatch skin overlaps the cone with a low door arc on the +X
side and a small smoke vent at the apex. Stone foundation ring honours the
"walls off ground" rule (rule 4 — 60 cm sandstone course). Interior: laterite
floor disc + central stone fire-pit ring.

Refer to ``docs/TERRAIN_PIVOT.md`` §3.8 (Wesley brief).

Material registry mapping (canonical keys in ``lqv/materials/``):

* ``bamboo``         — radial culms, lashings band, smoke-vent collar.
* ``palm_thatch``    — conical thatch skin.
* ``sandstone``      — 60 cm stone foundation ring + central fire-pit ring.
* ``laterite``       — tamped earth + laterite-pigment floor disc.
* ``lapacho_timber`` — door frame, door panel, fire-pit ground cap.
* ``rope_natural``   — apex lashing collar, mid-height tension band.
* ``steel_mesh``     — mosquito mesh over door opening (Rule 10 analogue).

Wave-1 use of the conical bamboo frame; per the "factor on second use, not
first" policy this module duplicates intent with ``bamboo_river_house`` but
does NOT extract a shared frame helper. The future ``bamboo_container_4pax``
typology will factor.
"""
from __future__ import annotations

import math

import bpy

from lqv.furniture import furnish_interior
from lqv.house import bamboo_frame as _bf
from lqv.materials import MAT, assign

# ---------------------------------------------------------------------------
# Geometry constants (2 PAX glamping, ~5 m diameter, ~4.5 m apex)
# ---------------------------------------------------------------------------

FOOTPRINT_M2 = math.pi * 2.5 ** 2   # ~19.6 m²
WALL_HEIGHT_M = 4.5                  # apex of the cone
ROOF_TYPE = 'palm_thatch_over_bamboo_cone'
FRAME = 'guadua_radial_leaning_culms'
WALL_TYPE = 'conical_palm_thatch_skin'
GLAZING = 'mosquito_mesh_at_door_only'
SLEEPS = 2
ORIENTATION = 'door_east'              # +X
SPECIES = 'guadua_angustifolia'        # NOT running bamboo
SNAP = 'stone_ring_pad'
NOTES = (
    'Treat all Guadua: borax + boric acid (cm² method).',
    'Apex lashing only — no metal sleeves at the cone tip (Wesley brief).',
    '60 cm sandstone foundation course honours Rule 4 (walls off ground).',
    'Entry: low arched door (~1.4 m tall) on the east (+X) side.',
    'Smoke vent at apex; mosquito mesh on door opening.',
    'NOT a tipi — fat-bottomed bamboo cone with palm thatch, not canvas.',
)

# Cone geometry
_BASE_RADIUS = 2.5                     # base of the cone (where poles meet ground)
_APEX_HEIGHT = 4.5                     # apex z above floor
_APEX_CLUSTER_R = 0.08                 # tiny radius at apex so poles converge to a knot, not a point
_POLE_COUNT = 16
_POLE_RADIUS = 0.035                   # 60-80 mm Ø → ~35 mm radius
_POLE_OVERSHOOT = 0.25                 # culms extend slightly past apex (lashing knot)

# Stone foundation course (rule 4)
_FOUND_OUTER_R = 2.65
_FOUND_INNER_R = 2.40
_FOUND_HEIGHT = 0.60

# Floor disc
_FLOOR_R = 2.40
_FLOOR_THICKNESS = 0.08
_FLOOR_Z = _FOUND_HEIGHT * 0.20         # tamped earth sits inside the ring, low

# Thatch
_THATCH_OFFSET = 0.06                   # thatch sits just outside pole frame
_THATCH_OVERHANG = 0.18                 # eave extension past the foundation
_THATCH_ARCH_SEGS = 18
_THATCH_LONG_SEGS = 24

# Door arc on +X side
_DOOR_AZ_HALF = math.radians(14.0)      # ±14° around +X axis ⇒ ~0.9 m wide at radius=2.5
_DOOR_HEAD_Z = 1.40                     # 1.4 m head height
_DOOR_FRAME_R = 0.045

# Smoke vent at apex
_VENT_R = 0.18
_VENT_H = 0.35

# Central fire-pit
_PIT_OUTER_R = 0.40
_PIT_INNER_R = 0.28
_PIT_H = 0.30

# Lashing band (rope) at mid-height for tension control
_LASHING_Z_FRAC = 0.55                  # 55 % of apex height
_LASHING_R = 0.025

# ---------------------------------------------------------------------------
# MATERIAL_TAKEOFF — glamping budget band USD 3,500-5,500.
# ---------------------------------------------------------------------------
# Assumptions (installed pricing, AR/PY market 2026):
#   * Guadua culm — harvest + borate treatment + transport + cut + lashing
#     labour ≈ USD 6.50 / linear m installed.
#   * Palm thatch over bamboo battens, hand-tied — USD 30 / m² installed.
#   * Sandstone foundation course: cut + dry-stacked with masonry labour,
#     USD 380 / m³ installed.
#   * Laterite-finished floor disc (compacted + pigment + lapacho timber
#     edge ring) — USD 26 / m² finished.
#   * Lapacho door (frame + panel + iron hardware, custom): USD 480.
#   * Natural-fibre lashings (jute / sisal, tarred): USD 1.40 each.
#   * Stainless 0.5 mm mosquito mesh + lapacho batten: USD 22 / m² installed.
#   * Borate treatment (borax + boric acid): USD 9 / kg powder, plus dip.
# Cone surface area: pi * r * sqrt(r² + h²) ≈ pi*2.5*sqrt(6.25+20.25)
#                  ≈ 3.14*2.5*5.15 ≈ 40.4 m².
# Pole length: each pole runs from radius 2.5 at base to ~0.08 at apex, so
#   sqrt(2.42² + 4.5²) ≈ 5.11 m per pole × 16 = ~82 m + overshoot ≈ 90 m.

_THATCH_AREA = math.pi * _BASE_RADIUS * math.sqrt(_BASE_RADIUS ** 2 + _APEX_HEIGHT ** 2)
_FOUND_VOLUME = math.pi * (_FOUND_OUTER_R ** 2 - _FOUND_INNER_R ** 2) * _FOUND_HEIGHT
_FLOOR_AREA = math.pi * _FLOOR_R ** 2
_POLE_LENGTH_EACH = math.sqrt((_BASE_RADIUS - _APEX_CLUSTER_R) ** 2 + _APEX_HEIGHT ** 2) + _POLE_OVERSHOOT
_POLE_TOTAL_LENGTH = _POLE_COUNT * _POLE_LENGTH_EACH

MATERIAL_TAKEOFF: dict[str, dict] = {
    'bamboo_culm': {
        # 16 leaning Guadua culms + apex overshoot, ~86 linear m. Installed
        # rate includes treatment + transport + cut + lashing labour.
        'length_m': round(_POLE_TOTAL_LENGTH, 1),
        'unit_cost_usd': 6.50,
    },
    'palm_thatch': {
        # Conical lateral surface area, full coverage minus door arc cut.
        'area_m2': round(_THATCH_AREA, 1),
        'unit_cost_usd': 30.0,
    },
    'sandstone_foundation': {
        # 60 cm tall stone ring, OD 2.65 / ID 2.40 m. Volume of the annular
        # cylinder; sit poles on top of this ring (rule 4: walls off ground).
        'volume_m3': round(_FOUND_VOLUME, 2),
        'unit_cost_usd': 380.0,
    },
    'lapacho_floor_mat': {
        # Tamped-earth + laterite-pigment floor disc, r=2.4 m → ~18 m².
        # Pricing reflects compacted earth + light lapacho timber edge ring.
        'area_m2': round(_FLOOR_AREA, 1),
        'unit_cost_usd': 26.0,
    },
    'lapacho_door': {
        # Frame + panel + iron hinge & latch, hand-built. 1 unit.
        'count': 1,
        'unit_cost_usd': 480.0,
    },
    'fasteners_lashings': {
        # Tarred natural-fibre lashings at every culm-to-foundation tie +
        # apex knot + mid-height tension band binds. ~150 joints.
        'count': 150,
        'unit_cost_usd': 1.40,
    },
    'mosquito_mesh': {
        # Door opening: ~0.9 m wide × 1.4 m head = ~1.3 m² + flap overlap ≈ 3 m².
        'area_m2': 3.0,
        'unit_cost_usd': 22.0,
    },
    'borax_boric_treatment': {
        # Guadua treatment kit, ~1.8 kg per culm × 16 culms.
        'weight_kg': _POLE_COUNT * 1.8,
        'unit_cost_usd': 9.0,
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
    """Return the first MAT key that resolves. Graceful fallback only."""
    for k in keys:
        m = MAT.get(k)
        if m is not None:
            return m
    return None


def _add_cylinder(col, name, location, radius, depth, mat=None, rotation=(0.0, 0.0, 0.0), vertices=12):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, rotation=rotation, vertices=vertices,
    )
    obj = bpy.context.active_object
    obj.name = name
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _add_cube(col, name, location, scale, mat=None, rotation=(0.0, 0.0, 0.0)):
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
    """60 cm sandstone ring course honouring rule 4 (walls off ground).

    Built as an outer cylinder + inner cylinder; the interior is implied empty
    (we don't bother with a boolean since the floor disc covers it at the
    expected camera angles).
    """
    mat = _mat('sandstone', 'laterite')
    _add_cylinder(
        col, 'BWL_Foundation_Outer',
        location=(ox, oy, _FOUND_HEIGHT / 2.0),
        radius=_FOUND_OUTER_R, depth=_FOUND_HEIGHT,
        mat=mat, vertices=48,
    )
    inner = _add_cylinder(
        col, 'BWL_Foundation_Inner',
        location=(ox, oy, _FOUND_HEIGHT / 2.0 + 0.001),
        radius=_FOUND_INNER_R, depth=_FOUND_HEIGHT + 0.01,
        mat=_mat('laterite', 'sandstone'),
        vertices=48,
    )
    # Sink the inner cylinder so it reads as a tamped infill rather than a
    # second exterior wall. Keep both as solids — boolean overhead is not
    # warranted at this typology's render budget.
    inner.location.z = _FOUND_HEIGHT / 2.0 - 0.05


def _floor_disc(col, ox, oy):
    """Laterite floor disc inside the foundation ring."""
    mat = _mat('laterite')
    _add_cylinder(
        col, 'BWL_FloorDisc',
        location=(ox, oy, _FOUND_HEIGHT + _FLOOR_THICKNESS / 2.0),
        radius=_FLOOR_R, depth=_FLOOR_THICKNESS,
        mat=mat, vertices=48,
    )


def _radial_poles(col, ox, oy):
    """16 leaning Guadua culms via the shared ``bamboo_frame`` primitive.

    Delegates to :func:`lqv.house.bamboo_frame.build_bamboo_radial_frame` so
    the wigwam + container_4pax veranda + future bamboo_beton typologies all
    share one cone-of-poles implementation. After creation each pole is
    re-linked into the typology collection (the shared primitive links to
    the scene root by default).
    """
    base_z = _FOUND_HEIGHT
    poles, apex_lashing = _bf.build_bamboo_radial_frame(
        center_xyz=(ox, oy, base_z),
        base_radius_m=_BASE_RADIUS,
        apex_height_m=_APEX_HEIGHT,
        count=_POLE_COUNT,
        post_diameter_m=_POLE_RADIUS * 2.0,
        apex_cluster_r=_APEX_CLUSTER_R,
        overshoot_m=_POLE_OVERSHOOT,
        material='bamboo',
        name_prefix='BWL_Pole',
    )
    for p in poles:
        _link(p, col)
    if apex_lashing is not None:
        apex_lashing.name = 'BWL_ApexLashing_FrameKnot'
        _link(apex_lashing, col)


def _thatch_cone(col, ox, oy):
    """Palm-thatch conical skin over the pole frame.

    Built as a quad mesh sweeping the cone azimuthally; the door arc on the
    +X side is cut out by omitting faces in the door azimuth band below the
    door head height. Two slightly displaced shells give a "shaggy" overlap.
    """
    mat = _mat('palm_thatch', 'sod_canopy')
    base_z = _FOUND_HEIGHT
    apex_z = base_z + _APEX_HEIGHT
    arch_segs = _THATCH_ARCH_SEGS
    long_segs = _THATCH_LONG_SEGS

    for shell_i, shell_offset in enumerate((0.0, 0.05)):
        thatch_r_base = _BASE_RADIUS + _THATCH_OFFSET + shell_offset
        # The apex shell sits at the cluster centre but a hair above the
        # poles so the eye reads thatch overlap, not pole-poking-through.
        apex_r = 0.10
        apex_z_shell = apex_z - 0.05 + shell_offset

        verts: list[tuple[float, float, float]] = []
        for a_i in range(arch_segs + 1):
            t = a_i / arch_segs                           # 0 base ... 1 apex
            r = thatch_r_base * (1 - t) + apex_r * t
            z = base_z * (1 - t) + apex_z_shell * t
            # eave overhang at base ring
            if a_i == 0:
                r += _THATCH_OVERHANG
                z -= 0.04
            for l_i in range(long_segs + 1):
                theta = (l_i / long_segs) * 2.0 * math.pi
                x = ox + r * math.cos(theta)
                y = oy + r * math.sin(theta)
                verts.append((x, y, z))

        faces: list[tuple[int, ...]] = []
        cols = long_segs + 1
        # Door cut: skip faces that fall inside the +X door arc and below
        # the door head height (only on the outer shell so the inner shell
        # still provides background mass — reads as door deeper than skin).
        for a_i in range(arch_segs):
            t_lo = a_i / arch_segs
            z_lo = base_z * (1 - t_lo) + apex_z_shell * t_lo
            for l_i in range(long_segs):
                # Azimuthal centre of this quad
                theta_c = ((l_i + 0.5) / long_segs) * 2.0 * math.pi
                # Distance from +X axis (azimuth=0). Wrap to [-pi, pi].
                dtheta = math.atan2(math.sin(theta_c), math.cos(theta_c))
                in_door_az = abs(dtheta) < _DOOR_AZ_HALF
                below_head = z_lo < (_FOUND_HEIGHT + _DOOR_HEAD_Z)
                if shell_i == 0 and in_door_az and below_head:
                    continue
                a = a_i * cols + l_i
                b = a + 1
                c = (a_i + 1) * cols + l_i + 1
                d = (a_i + 1) * cols + l_i
                faces.append((a, b, c, d))

        mesh = bpy.data.meshes.new(f'BWL_Thatch_{shell_i}_Mesh')
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        obj = bpy.data.objects.new(f'BWL_Thatch_{shell_i}', mesh)
        if mat is not None:
            assign(obj, mat)
        col.objects.link(obj)


def _door_frame(col, ox, oy):
    """Lapacho door frame (two jamb culms + arched header lintel) on +X side.

    The door panel itself is a slim lapacho slab swung slightly open so the
    interior fire-pit reads through the opening.
    """
    mat_lap = _mat('lapacho_timber', 'bamboo')
    mat_mesh = _mat('steel_mesh', 'bamboo')

    base_z = _FOUND_HEIGHT
    door_face_r = _BASE_RADIUS - 0.05
    head_z = base_z + _DOOR_HEAD_Z
    half_w = math.sin(_DOOR_AZ_HALF) * _BASE_RADIUS    # half door width at base

    # Jambs — vertical cylinders at the two azimuth limits
    for sign in (-1.0, 1.0):
        theta = sign * _DOOR_AZ_HALF
        jx = ox + door_face_r * math.cos(theta)
        jy = oy + door_face_r * math.sin(theta)
        _add_cylinder(
            col, f'BWL_DoorJamb_{"L" if sign < 0 else "R"}',
            location=(jx, jy, base_z + _DOOR_HEAD_Z / 2.0),
            radius=_DOOR_FRAME_R, depth=_DOOR_HEAD_Z,
            mat=mat_lap, vertices=10,
        )
    # Header lintel — horizontal cylinder spanning across the door (along Y)
    _add_cylinder(
        col, 'BWL_DoorHeader',
        location=(ox + door_face_r - 0.02, oy, head_z),
        radius=_DOOR_FRAME_R, depth=2.0 * half_w,
        rotation=(math.pi / 2.0, 0.0, 0.0),
        mat=mat_lap, vertices=10,
    )

    # Door panel — slim slab, hinged on -Y jamb, swung slightly open (~25°)
    swing = math.radians(-25.0)
    panel_w = 2.0 * half_w - 0.02
    panel_h = _DOOR_HEAD_Z - 0.04
    hinge_x = ox + door_face_r * math.cos(-_DOOR_AZ_HALF) + 0.01
    hinge_y = oy + door_face_r * math.sin(-_DOOR_AZ_HALF)
    # Place pivot then offset along the swung-open direction
    # The panel centre is half a panel out from the hinge, rotated by `swing`
    cx = hinge_x + math.cos(swing) * panel_w / 2.0
    cy = hinge_y + math.sin(swing) * panel_w / 2.0
    _add_cube(
        col, 'BWL_DoorPanel',
        location=(cx, cy, base_z + panel_h / 2.0 + 0.02),
        scale=(panel_w, 0.04, panel_h),
        rotation=(0.0, 0.0, swing),
        mat=mat_lap,
    )

    # Mosquito-mesh flap covering the opening behind the door (slight inset)
    mesh_x = ox + door_face_r - 0.10
    _add_cube(
        col, 'BWL_DoorMesh',
        location=(mesh_x, oy, base_z + _DOOR_HEAD_Z / 2.0),
        scale=(0.02, 2.0 * half_w * 0.9, _DOOR_HEAD_Z * 0.9),
        mat=mat_mesh,
    )


def _smoke_vent(col, ox, oy):
    """Small smoke-vent collar at apex — short open cylinder + rope ring."""
    mat_bamboo = _mat('bamboo')
    mat_rope = _mat('rope_natural', 'bamboo')
    apex_z = _FOUND_HEIGHT + _APEX_HEIGHT
    _add_cylinder(
        col, 'BWL_SmokeVentCollar',
        location=(ox, oy, apex_z + _VENT_H / 2.0),
        radius=_VENT_R, depth=_VENT_H,
        mat=mat_bamboo, vertices=16,
    )
    # Apex lashing knot (rope torus) just below the collar — no metal sleeve.
    bpy.ops.mesh.primitive_torus_add(
        major_radius=_APEX_CLUSTER_R + 0.06,
        minor_radius=0.02,
        location=(ox, oy, apex_z - 0.05),
        major_segments=24, minor_segments=6,
    )
    knot = bpy.context.active_object
    knot.name = 'BWL_ApexLashing'
    if mat_rope is not None:
        assign(knot, mat_rope)
    _link(knot, col)


def _mid_lashing_band(col, ox, oy):
    """Mid-height tension rope band — reads as a horizontal lashing ring."""
    mat = _mat('rope_natural', 'bamboo')
    band_z = _FOUND_HEIGHT + _LASHING_Z_FRAC * _APEX_HEIGHT
    # Linear interp of pole radius at this height
    t = _LASHING_Z_FRAC
    r = _BASE_RADIUS * (1 - t) + _APEX_CLUSTER_R * t + _POLE_RADIUS
    bpy.ops.mesh.primitive_torus_add(
        major_radius=r + 0.01,
        minor_radius=_LASHING_R,
        location=(ox, oy, band_z),
        major_segments=48, minor_segments=6,
    )
    obj = bpy.context.active_object
    obj.name = 'BWL_MidLashing'
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)


def _fire_pit(col, ox, oy):
    """Central sandstone fire-pit ring sitting on the laterite floor."""
    mat_stone = _mat('sandstone', 'laterite')
    mat_cap = _mat('lapacho_timber', 'sandstone')
    floor_top_z = _FOUND_HEIGHT + _FLOOR_THICKNESS
    # Outer ring
    bpy.ops.mesh.primitive_torus_add(
        major_radius=(_PIT_OUTER_R + _PIT_INNER_R) / 2.0,
        minor_radius=(_PIT_OUTER_R - _PIT_INNER_R) / 2.0,
        location=(ox, oy, floor_top_z + _PIT_H / 2.0),
        major_segments=24, minor_segments=6,
    )
    outer = bpy.context.active_object
    outer.name = 'BWL_FirePit_Ring'
    if mat_stone is not None:
        assign(outer, mat_stone)
    _link(outer, col)
    # Ash bed cap inside the ring
    _add_cylinder(
        col, 'BWL_FirePit_AshCap',
        location=(ox, oy, floor_top_z + 0.04),
        radius=_PIT_INNER_R - 0.02, depth=0.08,
        mat=mat_cap, vertices=20,
    )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def build_bamboo_wigwam_lodge(origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
                              parent: bpy.types.Collection | None = None,
                              variant: str = 'A') -> bpy.types.Collection:
    """Build the bamboo wigwam lodge at ``origin``.

    Parameters
    ----------
    origin
        World-space anchor (x, y, z); the cone axis sits here.
    parent
        Parent collection to nest the typology under (defaults to scene root).
    variant
        Variant tag (A/B/C) — naming only; lighting is set by the world.

    Returns the parent collection. Idempotent across re-invocation.
    """
    name = 'BambooWigwamLodge'
    col = _ensure_collection(name, parent)
    ox, oy, _oz = origin

    _stone_foundation(col, ox, oy)
    _floor_disc(col, ox, oy)
    _radial_poles(col, ox, oy)
    _thatch_cone(col, ox, oy)
    _mid_lashing_band(col, ox, oy)
    _smoke_vent(col, ox, oy)
    _door_frame(col, ox, oy)
    _fire_pit(col, ox, oy)

    # P1.B.1 — interior furniture stubs (RENDER_VIEW=interior readable).
    # Circular plan: inscribed square = _BASE_RADIUS * sqrt(2) ≈ 3.54 m.
    inscribed = _BASE_RADIUS * math.sqrt(2.0) - 0.4
    furn_floor_z = _FOUND_HEIGHT + _FLOOR_THICKNESS
    furnish_interior(
        col, footprint_w=inscribed, footprint_l=inscribed,
        origin_xy=(ox, oy), floor_z=furn_floor_z,
        pax=SLEEPS, style='bamboo', variant=variant, name_prefix='Wigwam_Furn',
    )

    return col


# Backwards-compatible alias matching the typologies API shape used by the
# stub driver and `lqv.typologies.__init__`.
def build(parent: bpy.types.Collection | None = None,
          location: tuple[float, float, float] = (0.0, 0.0, 0.0),
          variant: str = 'A') -> bpy.types.Collection:
    """Legacy entry point — see ``build_bamboo_wigwam_lodge``."""
    return build_bamboo_wigwam_lodge(origin=location, parent=parent, variant=variant)
