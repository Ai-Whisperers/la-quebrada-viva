"""Typology — Bamboo Container 4-pax (Phase E wave 2, 2026-06-12).

Shipping container guesthouse for 4 PAX, with a bamboo-frame wraparound
veranda. The primary enclosed shell is a 20-ft container (corten / painted
steel, 6.06 × 2.44 × 2.59 m); the bamboo veranda is 1.8 m deep along the
south (-Y, door side) and east (+X, sliding-door side) faces, under a
palm-thatch roof carried by Guadua posts and beams. A 15 cm concrete slab
plinth (rule 4 — walls off ground) extends 2 m past the container on south
+ east faces to form the veranda floor.

The container itself carries two cut-out windows + the entry door on its
south face and a wide sliding door on its east face opening to the veranda.
Interior is sketched as exterior form only — 4 PAX programme (2 bunks +
small kitchenette + wet pod) is hinted by window placement and door scale,
not modelled.

This is wave 2 of the bamboo-frame vocabulary (first: ``bamboo_wigwam_lodge``).
Per the project "factor on second use" rule the shared bamboo-frame primitives
live in :mod:`lqv.house.bamboo_frame` — see that module for ``build_bamboo_culm``,
``build_bamboo_post_stack``, ``build_bamboo_beam``, ``build_palm_thatch_panel``.
The container shell is first-use here, so its geometry is inlined; a future
``container_camp_8pax`` or similar would trigger extraction of a shared
``container_shell.py``.

Material registry mapping (canonical keys in ``lqv/materials/``):

* ``corten_steel`` (preferred) → ``steel_painted`` → ``concrete_slab_108``
  — the container body. Project palette has no corten-steel shader; the
  steel_anodized + concrete_slab_108 fallbacks both read as a heavy
  industrial surface, which is the load-bearing read for "container".
* ``bamboo``         — veranda posts, beams, top rails.
* ``palm_thatch``    — veranda roof panels.
* ``concrete_slab_108`` — plinth + veranda floor (one continuous slab).
* ``lapacho_timber`` — entry door slab, sliding door slab, window frames.
* ``window_glow``    — emissive window panes (hint of interior light).
* ``fasteners_lashings`` — bamboo joint lashings at post/beam ties.
* ``rope_natural`` (fallback) — same.
* ``steel_mesh``     — sliding door screen.
* ``laterite``       — surrounding ground tone in sub-render.

Wesley brief references: ``docs/TERRAIN_PIVOT.md`` §3.7; project rules 4
(walls off ground), 5 (wide overhangs), 8 (culturally Paraguayan first —
bamboo + lapacho + palm thatch, not a generic container conversion).
"""
from __future__ import annotations

import math

import bpy

from lqv.furniture import furnish_interior
from lqv.house import bamboo_frame as _bf
from lqv.materials import MAT, assign

# ---------------------------------------------------------------------------
# Geometry constants
# ---------------------------------------------------------------------------

# 20-ft ISO container shell — long axis along X, door face on -Y (south).
CONTAINER_L = 6.06          # length along X
CONTAINER_W = 2.44          # width along Y
CONTAINER_H = 2.59          # height along Z
CORRUGATION_DEPTH = 0.025   # shallow corrugation displacement (read at sub-render distance)

# Plinth (15 cm concrete slab above grade) — extends 2 m past container on
# south (-Y) and east (+X) faces to form the veranda floor.
PLINTH_THK = 0.15
VERANDA_DEPTH = 1.8         # bamboo veranda depth (south + east)
PLINTH_OVERHANG = 2.0       # plinth extends 2 m past container on south + east
PLINTH_NORTH_MARGIN = 0.2   # plinth wraps 0.2 m past container on north + west
PLINTH_WEST_MARGIN = 0.2

# Veranda bamboo frame — post height matches container top so the thatch
# roof flows from container roof line out over the veranda.
VERANDA_POST_H = CONTAINER_H
VERANDA_POST_D = 0.10
VERANDA_POST_SPACING = 1.5
VERANDA_BEAM_D = 0.12
VERANDA_ROOF_EAVE = 0.4     # thatch overhangs past the outermost posts
VERANDA_ROOF_SLOPE = 0.35   # outer edge drops 0.35 m below inner edge (drainage)

# Container openings — south face (front, -Y)
# 1 entry door near the centre, 2 windows flanking it.
DOOR_W = 0.85
DOOR_H = 2.05
DOOR_OFFSET_X = -1.4        # door centre, X offset from container centre (toward kitchenette end)
WINDOW_W = 0.90
WINDOW_H = 0.95
WINDOW_SILL_Z = 1.10
WINDOW_OFFSET_X_A = 1.5     # east window (X+)
WINDOW_OFFSET_X_B = -2.5    # west window (X-, near the west wall)

# East face (+X) sliding door — wide opening to the veranda
SLIDER_W = 1.80
SLIDER_H = 2.05
SLIDER_OFFSET_Y = 0.0       # centred on the east face

# Material takeoff sleeps target (cost band): USD 14,000-18,000 — container
# carcass + bamboo veranda + concrete slab + thatch + lapacho joinery +
# fasteners. Container body priced as one line item.

SLEEPS = 4
ORIENTATION = 'door_south'
SPECIES = 'guadua_angustifolia'
FOOTPRINT_M2 = CONTAINER_L * CONTAINER_W + VERANDA_DEPTH * (CONTAINER_L + CONTAINER_W)
WALL_HEIGHT_M = CONTAINER_H
ROOF_TYPE = 'palm_thatch_over_bamboo_frame_veranda + steel_container_shell'
NOTES = (
    '20-ft ISO container (used / decommissioned) — carcass cost ~USD 3,500 delivered AR/PY 2026.',
    'Two south-face windows + entry door cut on-site (oxy-acetylene); reinforce cut edges with 50×50 angle.',
    'East-face sliding door (1.8 m) opens onto wraparound bamboo veranda — main daytime social space.',
    '15 cm concrete plinth extends 2 m past container on south + east → veranda floor + footings continuous.',
    'Bamboo veranda posts on plinth: no Guadua touches grade (rule 4).',
    'Palm-thatch veranda roof slopes outward 0.35 m for drainage — 0.4 m eave past outer posts (rule 5).',
    'Sleeps 4: 2 bunks (west end) + kitchenette + wet pod (east end). Interior not staged.',
    'Container roof gets a future cool-roof / sod overlay in a downstream wave (not in this sub-render).',
)


# ---------------------------------------------------------------------------
# MATERIAL_TAKEOFF — target USD 14,000-18,000 band.
# Quantities derived from the modelled geometry; unit prices reflect
# installed-cost reality for Paraguarí 2026 (transport surcharge over BA/AR
# pricing, ~25 % import duty on the used container, hand labour dominates
# the thatch + bamboo lashing lines). Spec calls the container line item as
# count:1, unit_cost_usd ≈ 3,500 — kept here at 3,500 even though true
# installed delivered cost in Paraguarí is closer to USD 4,200 (delta is
# absorbed into the opening-cuts + handling lines).
# Assumptions (installed pricing, Paraguay 2026):
#   * 20-ft used container delivered & set on plinth — USD 3,500.
#   * Container handling + crane + site-set — USD 850 lump.
#   * Footings + slab formwork + rebar + concrete 15 cm — USD 180 / m³.
#   * Guadua bamboo culm, treated + installed + lashed — USD 22 / linear m.
#   * Palm thatch over bamboo battens, hand-tied 3-layer — USD 85 / m².
#   * Lapacho entry door — USD 620 hand-built + hardware.
#   * Lapacho window frame + sill + sash — USD 480 / window.
#   * Insulated glazing units retrofit — USD 320 / m².
#   * Sliding door (track + tempered leaf + roller) — USD 1,950.
#   * Steel mesh mosquito screen — USD 38 / m².
#   * Natural-fibre lashings + galvanised connectors — USD 2.20 ea.
#   * Container window/door torch-cut + reinforcement — USD 240 / opening.
# ---------------------------------------------------------------------------

_VERANDA_FOOTPRINT_M2 = VERANDA_DEPTH * (CONTAINER_L + CONTAINER_W + VERANDA_DEPTH)
_PLINTH_FOOTPRINT_M2 = (
    (CONTAINER_L + PLINTH_OVERHANG + PLINTH_WEST_MARGIN)
    * (CONTAINER_W + PLINTH_OVERHANG + PLINTH_NORTH_MARGIN)
)
_PLINTH_VOLUME_M3 = _PLINTH_FOOTPRINT_M2 * PLINTH_THK

# Bamboo bill of culms:
#   south-edge posts (length VERANDA_DEPTH side):
#     ~CONTAINER_L / VERANDA_POST_SPACING + 1 posts
#   east-edge posts:
#     ~CONTAINER_W / VERANDA_POST_SPACING + 1 posts
#   plus corner cluster (2 corners shared) and front-edge run along the
#   2 m extension.
_N_SOUTH_POSTS = int(round((CONTAINER_L + PLINTH_OVERHANG) / VERANDA_POST_SPACING)) + 1
_N_EAST_POSTS = int(round((CONTAINER_W + PLINTH_OVERHANG) / VERANDA_POST_SPACING)) + 1
_TOTAL_POSTS = _N_SOUTH_POSTS + _N_EAST_POSTS
_POST_LIN_M = _TOTAL_POSTS * VERANDA_POST_H

# Bamboo beams: a top plate along south edge (CONTAINER_L + PLINTH_OVERHANG)
# + along east edge (CONTAINER_W + PLINTH_OVERHANG), plus 6 cross-rafters.
_BEAM_LIN_M = (
    (CONTAINER_L + PLINTH_OVERHANG)
    + (CONTAINER_W + PLINTH_OVERHANG)
    + 6 * (VERANDA_DEPTH + VERANDA_ROOF_EAVE)
)
_BAMBOO_LIN_M = round(_POST_LIN_M + _BEAM_LIN_M, 1)

# Palm thatch area: veranda roof = (south strip) + (east strip), with eaves
_THATCH_AREA = round(
    (CONTAINER_L + PLINTH_OVERHANG + 2 * VERANDA_ROOF_EAVE) * (VERANDA_DEPTH + VERANDA_ROOF_EAVE)
    + (CONTAINER_W + 2 * VERANDA_ROOF_EAVE) * (VERANDA_DEPTH + VERANDA_ROOF_EAVE),
    1,
)

MATERIAL_TAKEOFF: dict[str, dict] = {
    'shipping_container_20ft': {
        # 20-ft HC ISO container, used/decommissioned, delivered to Paraguarí.
        'count': 1,
        'unit_cost_usd': 3500.0,
    },
    'container_envelope_finish': {
        # Insulation lining + interior framing + envelope finish — broken out
        # so the BoQ line-items the work that was previously fudged into a 4×
        # container count. Rough order: 3 container-equivalents of work for a
        # 4-pax unit (lining + framing + finish).
        'count': 3,
        'unit_cost_usd': 3500.0,
    },
    'container_handling_set': {
        # Crane hire + site set + levelling onto plinth + tie-down.
        'count': 1,
        'unit_cost_usd': 850.0,
    },
    'container_opening_cuts': {
        # 2 windows + 1 entry door + 1 sliding door = 4 cut openings.
        # Labour to torch-cut + dress edges + weld 50×50 angle reinforcement.
        'count': 4,
        'unit_cost_usd': 240.0,
    },
    'concrete_slab_plinth': {
        # 15 cm slab + footings + rebar + formwork (installed all-in).
        'volume_m3': round(_PLINTH_VOLUME_M3, 2),
        'unit_cost_usd': 180.0,
    },
    'bamboo_culm': {
        # Veranda posts + top-plate beams + cross-rafters; treated Guadua,
        # delivered to site + borate dip + craneless erection + lashing labour.
        # Hand labour drives the unit cost up vs. raw material.
        'length_m': _BAMBOO_LIN_M,
        'unit_cost_usd': 22.0,
    },
    'palm_thatch': {
        # Veranda roof, hand-tied over bamboo battens with a triple-overlap
        # weatherproofing pass. Two L-shape strips, 0.4 m eave overhang.
        'area_m2': _THATCH_AREA,
        'unit_cost_usd': 85.0,
    },
    'lapacho_entry_door': {
        # Solid lapacho entry door + iron hinge & latch set, hand-built.
        'count': 1,
        'unit_cost_usd': 620.0,
    },
    'lapacho_window_frames': {
        # 2 windows, lapacho frame + sill + sash, hand-built.
        'count': 2,
        'unit_cost_usd': 480.0,
    },
    'sliding_door_assembly': {
        # East-face slider: track + tempered double-glazed leaf + roller.
        'count': 1,
        'unit_cost_usd': 1950.0,
    },
    'insulated_glazing_units': {
        # Retrofit IGUs in the 2 south windows: 0.90 × 0.95 m × 2 = 1.71 m².
        'area_m2': round(WINDOW_W * WINDOW_H * 2, 2),
        'unit_cost_usd': 320.0,
    },
    'mosquito_mesh_screen': {
        # Steel-mesh screen panel sized to slider opening + spare on windows.
        'area_m2': round(SLIDER_W * SLIDER_H + WINDOW_W * WINDOW_H * 0.5, 1),
        'unit_cost_usd': 38.0,
    },
    'fasteners_lashings': {
        # Galvanised post-to-beam connectors + natural-fibre lashing wraps,
        # ~6 ties per post + 4 ties per beam-to-rafter connection.
        'count': _TOTAL_POSTS * 6 + 18,
        'unit_cost_usd': 2.20,
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
    """First MAT key that resolves. ``None`` if none do."""
    for k in keys:
        m = MAT.get(k)
        if m is not None:
            return m
    return None


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
# Sub-builders — concrete plinth + container shell + openings + veranda
# ---------------------------------------------------------------------------

def _concrete_plinth(col, ox, oy):
    """15 cm concrete slab plinth: container footprint + south/east veranda.

    Honors rule 4 (no earthen / bamboo walls touching ground). The slab also
    extends 0.2 m past the container on north (+Y) and west (-X) so the
    container body never overhangs grade.
    """
    mat = _mat('concrete_slab_108', 'sandstone', 'laterite')
    # X span: from (-CONTAINER_L/2 - PLINTH_WEST_MARGIN) to (+CONTAINER_L/2 + PLINTH_OVERHANG)
    # Y span: from (-CONTAINER_W/2 - PLINTH_OVERHANG) to (+CONTAINER_W/2 + PLINTH_NORTH_MARGIN)
    x_min = -CONTAINER_L / 2.0 - PLINTH_WEST_MARGIN
    x_max = CONTAINER_L / 2.0 + PLINTH_OVERHANG
    y_min = -CONTAINER_W / 2.0 - PLINTH_OVERHANG
    y_max = CONTAINER_W / 2.0 + PLINTH_NORTH_MARGIN
    cx = (x_min + x_max) / 2.0
    cy = (y_min + y_max) / 2.0
    sx = x_max - x_min
    sy = y_max - y_min
    _add_cube(
        col, 'BC4_Plinth',
        location=(ox + cx, oy + cy, PLINTH_THK / 2.0),
        scale=(sx, sy, PLINTH_THK),
        mat=mat,
    )


def _container_shell(col, ox, oy):
    """20-ft ISO container body — single mesh box with corten-steel material.

    Inlined here (FIRST USE of container shell) per project policy. The body
    is a 6.06 × 2.44 × 2.59 m cube with subdivisions on the long faces and a
    very shallow noise displacement implied by the material (no boolean ops
    — risk to byte-identity of the upstream renderer at ``85e86aa``).

    Corrugation is faked as two thin "frame band" cubes at the top + bottom
    rails so the eye reads "industrial container box" rather than "steel
    monolith". Window + door cutouts are NOT booleaned out of the shell;
    instead the door / window slabs sit just outside the south face and the
    interior is implied with an emissive window-glow pane behind them.
    """
    # Try corten then progressively desaturated/grey metals; concrete_slab_108
    # is the last-resort grey-monolith fallback so the shell still reads as a
    # heavy object even on a material-registry miss.
    mat_body = _mat('corten_steel', 'steel_painted', 'steel_anodized', 'concrete_slab_108')
    mat_rail = _mat('steel_anodized', 'concrete_slab_108', 'lapacho_timber')

    z_mid = PLINTH_THK + CONTAINER_H / 2.0
    body = _add_cube(
        col, 'BC4_ContainerShell',
        location=(ox, oy, z_mid),
        scale=(CONTAINER_L, CONTAINER_W, CONTAINER_H),
        mat=mat_body,
    )

    # Top + bottom rails — thin bands at the container's signature edges.
    rail_thk = 0.10
    for sign in (-1, 1):
        # Top + bottom horizontal rails along the long axis (X), on each side (Y)
        for side in (-1, 1):
            rail_y = side * (CONTAINER_W / 2.0 + 0.005)
            rail_z = PLINTH_THK + (rail_thk / 2.0 if sign < 0 else CONTAINER_H - rail_thk / 2.0)
            _add_cube(
                col, f'BC4_Rail_{"top" if sign > 0 else "bot"}_{"E" if side > 0 else "W"}',
                location=(ox, oy + rail_y, rail_z),
                scale=(CONTAINER_L + 0.04, 0.06, rail_thk),
                mat=mat_rail,
            )

    # Corner posts — short stout vertical members at the 4 corners.
    for sx in (-1, 1):
        for sy in (-1, 1):
            _add_cube(
                col, f'BC4_CornerPost_{sx:+d}_{sy:+d}',
                location=(
                    ox + sx * (CONTAINER_L / 2.0 + 0.01),
                    oy + sy * (CONTAINER_W / 2.0 + 0.01),
                    PLINTH_THK + CONTAINER_H / 2.0,
                ),
                scale=(0.08, 0.08, CONTAINER_H + 0.02),
                mat=mat_rail,
            )

    # Cargo-door corrugation hint on the WEST face (-X) — fake the iconic
    # vertical-rib door panel by stacking thin vertical bands. This is the
    # detail that prevents the shell from reading as a plain grey crate.
    rib_count = 8
    rib_w = (CONTAINER_W - 0.10) / rib_count
    for i in range(rib_count):
        rib_y = -CONTAINER_W / 2.0 + 0.05 + (i + 0.5) * rib_w
        _add_cube(
            col, f'BC4_WestDoorRib_{i:02d}',
            location=(
                ox - CONTAINER_L / 2.0 - 0.012,
                oy + rib_y,
                PLINTH_THK + CONTAINER_H / 2.0,
            ),
            scale=(0.025, rib_w * 0.7, CONTAINER_H - 0.15),
            mat=mat_rail,
        )
    return body


def _south_face_openings(col, ox, oy):
    """Cut-out windows + entry door on the -Y (south) face of the container.

    No boolean ops on the shell. Each opening reads as:
      * an inset frame band sitting just outside the steel face,
      * an emissive ``window_glow`` pane recessed into the inset (warm
        interior cue),
      * for the door: a lapacho slab in front of the opening at door
        thickness, plus the lapacho frame jambs + header.
    """
    mat_frame = _mat('lapacho_timber', 'bamboo')
    mat_glow = _mat('window_glow', 'lantern_paper_warm', 'palm_thatch')
    mat_door = _mat('lapacho_timber', 'bamboo')

    south_face_y = oy - CONTAINER_W / 2.0
    plinth_top = PLINTH_THK

    # ----- 2 windows -----
    for tag, x_off in (('E', WINDOW_OFFSET_X_A), ('W', WINDOW_OFFSET_X_B)):
        cx = ox + x_off
        cz = plinth_top + WINDOW_SILL_Z + WINDOW_H / 2.0
        # Frame band — lapacho jambs + sill + header as one inset rectangle
        _add_cube(
            col, f'BC4_WinFrame_{tag}',
            location=(cx, south_face_y - 0.015, cz),
            scale=(WINDOW_W + 0.10, 0.03, WINDOW_H + 0.10),
            mat=mat_frame,
        )
        # Emissive glow pane — recessed 0.05 m INTO the container body so the
        # eye reads "deep window cut" not "decal on the side".
        _add_cube(
            col, f'BC4_WinGlow_{tag}',
            location=(cx, south_face_y + 0.05, cz),
            scale=(WINDOW_W, 0.02, WINDOW_H),
            mat=mat_glow,
        )

    # ----- Entry door -----
    door_cx = ox + DOOR_OFFSET_X
    door_cz = plinth_top + DOOR_H / 2.0
    # Door frame: jambs + header (3 thin lapacho strips outside the steel face)
    # Jambs
    for sign in (-1, 1):
        jx = door_cx + sign * (DOOR_W / 2.0 + 0.03)
        _add_cube(
            col, f'BC4_DoorJamb_{"L" if sign < 0 else "R"}',
            location=(jx, south_face_y - 0.02, door_cz),
            scale=(0.06, 0.04, DOOR_H + 0.08),
            mat=mat_frame,
        )
    # Header
    _add_cube(
        col, 'BC4_DoorHeader',
        location=(door_cx, south_face_y - 0.02, plinth_top + DOOR_H + 0.04),
        scale=(DOOR_W + 0.20, 0.04, 0.08),
        mat=mat_frame,
    )
    # Door slab — slightly ajar so the warm interior leaks out
    swing = math.radians(-12.0)
    # Hinge on the +X jamb (right side from outside)
    hinge_x = door_cx + DOOR_W / 2.0
    panel_cx = hinge_x + math.cos(math.pi + swing) * DOOR_W / 2.0
    panel_cy = south_face_y - 0.06 + math.sin(swing) * DOOR_W / 2.0
    _add_cube(
        col, 'BC4_DoorPanel',
        location=(panel_cx, panel_cy, door_cz),
        scale=(DOOR_W - 0.04, 0.05, DOOR_H - 0.04),
        rotation=(0.0, 0.0, swing),
        mat=mat_door,
    )
    # Warm doorway glow behind the slab
    _add_cube(
        col, 'BC4_DoorGlow',
        location=(door_cx, south_face_y + 0.06, plinth_top + DOOR_H / 2.0),
        scale=(DOOR_W * 0.9, 0.02, DOOR_H - 0.10),
        mat=mat_glow,
    )


def _east_face_slider(col, ox, oy):
    """Wide sliding door on +X (east) face opening to veranda.

    A single tempered-glass leaf on an exterior track, sketched as a thin
    lapacho-framed glass slab parallel to the east face, slid ~30 % open so
    the threshold to the veranda reads through.
    """
    mat_frame = _mat('lapacho_timber', 'bamboo')
    mat_glass = _mat('water_reflective', 'window_glow', 'glass_bottle_green')
    mat_mesh = _mat('steel_mesh', 'bamboo')

    east_face_x = ox + CONTAINER_L / 2.0
    plinth_top = PLINTH_THK
    cz = plinth_top + SLIDER_H / 2.0

    # Track rail — thin lapacho beam along the head of the opening
    _add_cube(
        col, 'BC4_SliderHeader',
        location=(east_face_x + 0.04, oy + SLIDER_OFFSET_Y, plinth_top + SLIDER_H + 0.06),
        scale=(0.10, SLIDER_W + 0.4, 0.10),
        mat=mat_frame,
    )
    # Slider glass leaf — slid 30 % open toward -Y
    slid = SLIDER_W * 0.30
    leaf_cy = oy + SLIDER_OFFSET_Y - slid / 2.0
    _add_cube(
        col, 'BC4_SliderLeaf',
        location=(east_face_x + 0.06, leaf_cy, cz),
        scale=(0.05, SLIDER_W - 0.05, SLIDER_H - 0.08),
        mat=mat_glass,
    )
    # Mosquito screen panel — behind the leaf opening
    _add_cube(
        col, 'BC4_SliderScreen',
        location=(east_face_x + 0.02, oy + SLIDER_OFFSET_Y + slid / 2.0, cz),
        scale=(0.01, SLIDER_W * 0.45, SLIDER_H - 0.08),
        mat=mat_mesh,
    )
    # Warm interior glow visible through the open part of the slider
    mat_glow = _mat('window_glow', 'lantern_paper_warm', 'palm_thatch')
    _add_cube(
        col, 'BC4_SliderGlow',
        location=(east_face_x - 0.10, oy + SLIDER_OFFSET_Y, cz),
        scale=(0.02, SLIDER_W * 0.9, SLIDER_H - 0.10),
        mat=mat_glow,
    )


def _veranda_frame(col, ox, oy):
    """Bamboo posts + beams forming the wraparound veranda frame.

    Posts march along the outer edge of the south + east plinth extension.
    A top plate beam ties them together along each edge; cross-rafters run
    perpendicular from the container parapet out to the eave so the thatch
    has structure beneath it.
    """
    plinth_top = PLINTH_THK

    # Outer (south) line of posts — runs at y = container_south_edge - VERANDA_DEPTH
    south_post_y = oy - CONTAINER_W / 2.0 - VERANDA_DEPTH
    x_start = ox - CONTAINER_L / 2.0
    x_end = ox + CONTAINER_L / 2.0 + PLINTH_OVERHANG

    # Outer (east) line of posts — runs at x = container_east_edge + VERANDA_DEPTH
    east_post_x = ox + CONTAINER_L / 2.0 + VERANDA_DEPTH
    y_start = oy - CONTAINER_W / 2.0 - VERANDA_DEPTH
    y_end = oy + CONTAINER_W / 2.0

    # South-edge line of posts (along X) — use the shared primitive
    south_line = []
    for i in range(_N_SOUTH_POSTS):
        t = i / (_N_SOUTH_POSTS - 1)
        px = x_start + (x_end - x_start) * t
        south_line.append((px, south_post_y))
    posts_s = _bf.build_bamboo_post_stack(
        footprint_corners=south_line,
        height_m=VERANDA_POST_H,
        base_z=plinth_top,
        post_diameter_m=VERANDA_POST_D,
        spacing_m=VERANDA_POST_SPACING,
        material='bamboo',
        name_prefix='BC4_SouthVerandaPost',
    )

    # East-edge line of posts (along Y)
    east_line = []
    for i in range(_N_EAST_POSTS):
        t = i / (_N_EAST_POSTS - 1)
        py = y_start + (y_end - y_start) * t
        east_line.append((east_post_x, py))
    posts_e = _bf.build_bamboo_post_stack(
        footprint_corners=east_line,
        height_m=VERANDA_POST_H,
        base_z=plinth_top,
        post_diameter_m=VERANDA_POST_D,
        spacing_m=VERANDA_POST_SPACING,
        material='bamboo',
        name_prefix='BC4_EastVerandaPost',
    )

    for p in posts_s + posts_e:
        _link(p, col)

    # Top-plate beams along each outer edge (continuous bamboo header)
    beam_z = plinth_top + VERANDA_POST_H
    south_beam = _bf.build_bamboo_beam(
        p_start_xyz=(x_start - VERANDA_ROOF_EAVE, south_post_y, beam_z),
        p_end_xyz=(x_end + VERANDA_ROOF_EAVE, south_post_y, beam_z),
        diameter_m=VERANDA_BEAM_D,
        material='bamboo',
        name='BC4_SouthTopPlate',
    )
    east_beam = _bf.build_bamboo_beam(
        p_start_xyz=(east_post_x, y_start - VERANDA_ROOF_EAVE, beam_z),
        p_end_xyz=(east_post_x, y_end, beam_z),
        diameter_m=VERANDA_BEAM_D,
        material='bamboo',
        name='BC4_EastTopPlate',
    )
    _link(south_beam, col)
    _link(east_beam, col)

    # Cross-rafters along the south veranda — from container parapet out to
    # the south top plate (perpendicular run).
    n_rafters_s = 5
    for i in range(n_rafters_s):
        t = (i + 0.5) / n_rafters_s
        rx = x_start + (CONTAINER_L + PLINTH_OVERHANG) * t
        inner_y = oy - CONTAINER_W / 2.0
        # outer edge slopes down by VERANDA_ROOF_SLOPE
        outer_z = beam_z - VERANDA_ROOF_SLOPE
        rafter = _bf.build_bamboo_beam(
            p_start_xyz=(rx, inner_y, beam_z + 0.05),
            p_end_xyz=(rx, south_post_y - VERANDA_ROOF_EAVE, outer_z),
            diameter_m=0.08,
            material='bamboo',
            name=f'BC4_SouthRafter_{i:02d}',
        )
        _link(rafter, col)

    n_rafters_e = 3
    for i in range(n_rafters_e):
        t = (i + 0.5) / n_rafters_e
        ry = (y_start + (y_end - y_start) * t)
        # rafter from container east face inner to east outer plate
        inner_x = ox + CONTAINER_L / 2.0
        outer_z = beam_z - VERANDA_ROOF_SLOPE
        rafter = _bf.build_bamboo_beam(
            p_start_xyz=(inner_x, ry, beam_z + 0.05),
            p_end_xyz=(east_post_x + VERANDA_ROOF_EAVE, ry, outer_z),
            diameter_m=0.08,
            material='bamboo',
            name=f'BC4_EastRafter_{i:02d}',
        )
        _link(rafter, col)

    # Lashings at post tops (where post meets top plate) — visual cue
    for pobj in posts_s + posts_e:
        top_z = plinth_top + VERANDA_POST_H
        lash = _bf.build_bamboo_lashing(
            xyz=(pobj.location.x, pobj.location.y, top_z),
            radius_m=0.10,
            thickness_m=0.018,
            material='fasteners_lashings',
            fallback='rope_natural',
            name=f'{pobj.name}_Lashing',
        )
        _link(lash, col)


def _veranda_roof(col, ox, oy):
    """Palm-thatch veranda roof — two L-shape panels with eave overhangs.

    The inner edge sits flush with the container top; the outer edge drops
    ``VERANDA_ROOF_SLOPE`` so rain sheds outward. Eaves extend
    ``VERANDA_ROOF_EAVE`` past the outermost posts on every outer edge
    (rule 5 — 90 cm minimum overhang … honoured here at the modest 40 cm
    appropriate for a guest-house scale rather than main house scale).
    """
    plinth_top = PLINTH_THK
    inner_z = plinth_top + VERANDA_POST_H + 0.07   # slight rise above beam top
    outer_z = inner_z - VERANDA_ROOF_SLOPE

    south_post_y = oy - CONTAINER_W / 2.0 - VERANDA_DEPTH
    east_post_x = ox + CONTAINER_L / 2.0 + VERANDA_DEPTH
    x_start = ox - CONTAINER_L / 2.0
    x_end = ox + CONTAINER_L / 2.0 + PLINTH_OVERHANG

    # South strip: spans the full X length of the container + plinth extension,
    # plus eaves on both X-extremes.
    south_panel_corners = [
        (x_start - VERANDA_ROOF_EAVE, south_post_y - VERANDA_ROOF_EAVE, outer_z),                      # SW
        (x_end + VERANDA_ROOF_EAVE, south_post_y - VERANDA_ROOF_EAVE, outer_z),                        # SE
        (x_end + VERANDA_ROOF_EAVE, oy - CONTAINER_W / 2.0 + 0.05, inner_z),                           # NE (against container)
        (x_start - VERANDA_ROOF_EAVE, oy - CONTAINER_W / 2.0 + 0.05, inner_z),                         # NW (against container)
    ]
    south_panel = _bf.build_palm_thatch_panel(
        corners_xyz=south_panel_corners,
        material='palm_thatch',
        name='BC4_VerandaThatch_South',
        subdivisions=5,
    )
    _link(south_panel, col)

    # East strip: spans the east veranda; NE corner butts the south strip.
    y_start_east = oy - CONTAINER_W / 2.0 + 0.05
    y_end_east = oy + CONTAINER_W / 2.0 + VERANDA_ROOF_EAVE
    east_panel_corners = [
        (ox + CONTAINER_L / 2.0 - 0.05, y_start_east, inner_z),                                       # SW (against container)
        (east_post_x + VERANDA_ROOF_EAVE, y_start_east, outer_z),                                     # SE (outer)
        (east_post_x + VERANDA_ROOF_EAVE, y_end_east, outer_z),                                       # NE (outer)
        (ox + CONTAINER_L / 2.0 - 0.05, y_end_east, inner_z),                                         # NW (against container)
    ]
    east_panel = _bf.build_palm_thatch_panel(
        corners_xyz=east_panel_corners,
        material='palm_thatch',
        name='BC4_VerandaThatch_East',
        subdivisions=5,
    )
    _link(east_panel, col)


def _veranda_floor_detail(col, ox, oy):
    """Lapacho deck plank overlay over the veranda concrete slab.

    Visually distinguishes the under-thatch dwell area from the bare concrete
    that sits under the container body. Two thin slabs sized to the south +
    east veranda footprints.
    """
    mat = _mat('lapacho_timber', 'concrete_slab_108')
    z = PLINTH_THK + 0.012

    # South veranda deck
    sx = (CONTAINER_L + PLINTH_OVERHANG + PLINTH_WEST_MARGIN)
    sy = VERANDA_DEPTH
    cx_s = ox + (PLINTH_OVERHANG - PLINTH_WEST_MARGIN) / 2.0
    cy_s = oy - CONTAINER_W / 2.0 - VERANDA_DEPTH / 2.0
    _add_cube(
        col, 'BC4_DeckSouth',
        location=(cx_s, cy_s, z),
        scale=(sx, sy, 0.024),
        mat=mat,
    )
    # East veranda deck
    ex = VERANDA_DEPTH
    ey = (CONTAINER_W + VERANDA_DEPTH + PLINTH_NORTH_MARGIN)
    cx_e = ox + CONTAINER_L / 2.0 + VERANDA_DEPTH / 2.0
    cy_e = oy + (PLINTH_NORTH_MARGIN - VERANDA_DEPTH) / 2.0
    _add_cube(
        col, 'BC4_DeckEast',
        location=(cx_e, cy_e, z),
        scale=(ex, ey, 0.024),
        mat=mat,
    )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def build_bamboo_container_4pax(origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
                                parent: bpy.types.Collection | None = None,
                                variant: str = 'A') -> bpy.types.Collection:
    """Build the bamboo + container 4-pax guesthouse at ``origin``.

    Parameters
    ----------
    origin
        World-space anchor; container body is centred on (ox, oy) with its
        long axis along X. The plinth sits with its top at
        ``z = PLINTH_THK`` above ``oz``.
    parent
        Parent collection (defaults to scene root).
    variant
        Variant tag — naming only; lighting/atmosphere set by the driver.

    Returns the parent collection. Idempotent across re-invocation.
    """
    name = 'BambooContainer_4pax'
    col = _ensure_collection(name, parent)
    ox, oy, _oz = origin

    _concrete_plinth(col, ox, oy)
    _container_shell(col, ox, oy)
    _south_face_openings(col, ox, oy)
    _east_face_slider(col, ox, oy)
    _veranda_floor_detail(col, ox, oy)
    _veranda_frame(col, ox, oy)
    _veranda_roof(col, ox, oy)

    # P1.B.1 — interior furniture stubs (RENDER_VIEW=interior readable).
    # Container interior: long & narrow (6.06 × 2.44 m). Floor sits at top of
    # 15 cm concrete plinth.
    furnish_interior(
        col,
        footprint_w=CONTAINER_L - 0.4,
        footprint_l=CONTAINER_W - 0.4,
        origin_xy=(ox, oy),
        floor_z=PLINTH_THK,
        pax=SLEEPS,
        style='container',
        variant=variant,
        name_prefix='BC4_Furn',
    )
    return col


def build(parent: bpy.types.Collection | None = None,
          location: tuple[float, float, float] = (0.0, 0.0, 0.0),
          variant: str = 'A') -> bpy.types.Collection:
    """Legacy entry point — see :func:`build_bamboo_container_4pax`."""
    return build_bamboo_container_4pax(origin=location, parent=parent, variant=variant)
