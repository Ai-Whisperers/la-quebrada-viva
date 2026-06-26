"""Interior furniture stubs for habitable typologies (P1.B.1).

Single public entry: :func:`furnish_interior`. Place primitive bed / bedside /
dining table / 2 stools / shelf / lantern inside a footprint, parameterised by
the host typology so 16 enclosed habitable modules can opt in with one call
site each. No RNG — fully deterministic; no MAT mutation — call-time lookup
only. The shapes are intentionally low-fidelity (single cubes/cylinders) so
the `RENDER_VIEW=interior` 18 mm wide-FOV camera reads "this is a habitable
room" without committing the renderer to a specific furniture style.

Material fallback chains are minimal — every chain bottoms out on
``lapacho_timber`` which is always present.

The variant emissive ramp on the lantern (A=0.0 / B=0.6 / C=1.0) matches the
existing T-1.6 lighting ramp so the interior view picks up variant cues
without per-typology wiring.
"""
from __future__ import annotations

from typing import Iterable

import bpy

from lqv.materials import MAT, assign


_VARIANT_LANTERN_EMISSION = {'A': 0.0, 'B': 0.6, 'C': 1.0}

_STYLE_CHAINS = {
    'bamboo':    {'frame': ('bamboo_culm', 'lapacho_timber'),
                  'top':   ('lapacho_timber',),
                  'soft':  ('palm_thatch', 'lapacho_timber'),
                  'stool': ('lapacho_timber', 'bamboo_culm')},
    'lapacho':   {'frame': ('lapacho_timber',),
                  'top':   ('lapacho_timber',),
                  'soft':  ('palm_thatch', 'lapacho_timber'),
                  'stool': ('lapacho_timber',)},
    'stone':     {'frame': ('lapacho_timber',),
                  'top':   ('sandstone', 'lapacho_timber'),
                  'soft':  ('palm_thatch', 'lapacho_timber'),
                  'stool': ('sandstone', 'lapacho_timber')},
    'cob':       {'frame': ('lapacho_timber',),
                  'top':   ('lapacho_timber',),
                  'soft':  ('palm_thatch', 'lapacho_timber'),
                  'stool': ('cob_raw', 'sandstone', 'lapacho_timber')},
    'container': {'frame': ('lapacho_timber',),
                  'top':   ('lapacho_timber',),
                  'soft':  ('palm_thatch', 'lapacho_timber'),
                  'stool': ('lapacho_timber',)},
}


def _resolve(keys: Iterable[str]):
    for k in keys:
        m = MAT.get(k)
        if m is not None:
            return m
    return None


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


def _cyl(col, name, location, radius, depth, mat, vertices=10):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, vertices=vertices)
    obj = bpy.context.active_object
    obj.name = name
    if mat is not None:
        assign(obj, mat)
    _link(obj, col)
    return obj


def _make_lantern_material(name: str, emission_strength: float):
    """Tiny self-contained emissive material — bypasses MAT registry so we never
    mutate it from a typology call site (preserves byte-freeze invariant on the
    registry for shipped composite renders)."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (1.0, 0.78, 0.42, 1.0)   # warm amber
    em.inputs['Strength'].default_value = float(emission_strength)
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    return mat


def furnish_interior(
    col: bpy.types.Collection,
    *,
    footprint_w: float,
    footprint_l: float,
    origin_xy: tuple[float, float] = (0.0, 0.0),
    floor_z: float = 0.0,
    pax: int = 2,
    style: str = 'bamboo',
    variant: str = 'A',
    name_prefix: str = 'Furn',
):
    """Drop minimal furniture inside an interior footprint.

    ``footprint_w`` is along +X, ``footprint_l`` along +Y. ``origin_xy`` is the
    centre of the floor zone in world coords. ``floor_z`` is the top of the
    finished floor (furniture rests on it).

    ``pax >= 2`` widens the bed from 0.9 m to 1.4 m. Lantern emission ramp:
    A=off / B=mid / C=full so ``RENDER_VIEW=interior`` reads the variant cue.
    """
    if footprint_w < 1.5 or footprint_l < 1.5:
        # Too small to furnish meaningfully — caller's footprint is wrong, but
        # silently skip rather than fail the render. Drivers can detect via
        # the empty return dict.
        return {}

    style_key = style if style in _STYLE_CHAINS else 'bamboo'
    chains = _STYLE_CHAINS[style_key]
    frame_mat = _resolve(chains['frame'])
    top_mat   = _resolve(chains['top'])
    soft_mat  = _resolve(chains['soft'])
    stool_mat = _resolve(chains['stool'])

    ox, oy = origin_xy
    bed_w = 1.4 if pax >= 2 else 0.9
    bed_l = 1.9
    bed_h_frame = 0.30
    bed_h_mattress = 0.18

    # Margins keep furniture off interior walls so the 18mm camera doesn't
    # frame a leg-against-stud collision.
    margin = 0.30
    half_w = footprint_w / 2.0 - margin
    half_l = footprint_l / 2.0 - margin

    objs: dict = {}

    # Bed against +Y wall, head end (pillow side) at +Y
    bx = ox - half_w + bed_w / 2.0
    by = oy + half_l - bed_l / 2.0
    frame_z = floor_z + bed_h_frame / 2.0
    mat_z   = floor_z + bed_h_frame + bed_h_mattress / 2.0
    objs['bed_frame'] = _box(
        col, f'{name_prefix}_BedFrame', (bx, by, frame_z),
        (bed_w, bed_l, bed_h_frame), frame_mat)
    objs['bed_mattress'] = _box(
        col, f'{name_prefix}_BedMattress', (bx, by, mat_z),
        (bed_w - 0.04, bed_l - 0.04, bed_h_mattress), soft_mat)
    # Pillow at head end (toward +Y)
    pillow_z = floor_z + bed_h_frame + bed_h_mattress + 0.07
    objs['pillow'] = _box(
        col, f'{name_prefix}_Pillow',
        (bx, by + bed_l / 2.0 - 0.30, pillow_z),
        (bed_w - 0.30, 0.45, 0.12), soft_mat)

    # Bedside table next to bed (toward -Y from headboard)
    bs_x = bx + bed_w / 2.0 + 0.20
    if bs_x + 0.25 > ox + half_w:
        bs_x = bx - bed_w / 2.0 - 0.45   # flip to other side if no room
    bs_y = by + bed_l / 2.0 - 0.25
    objs['bedside'] = _box(
        col, f'{name_prefix}_Bedside',
        (bs_x, bs_y, floor_z + 0.30),
        (0.45, 0.45, 0.60), frame_mat)

    # Dining/work table toward -Y end of the room
    table_w = min(1.0, footprint_w - 2 * margin - 0.20)
    table_l = 0.60
    tx = ox
    ty = oy - half_l + table_l / 2.0 + 0.25
    objs['table_top'] = _box(
        col, f'{name_prefix}_TableTop',
        (tx, ty, floor_z + 0.74),
        (table_w, table_l, 0.04), top_mat)
    # Four legs
    leg_inset = 0.05
    for sx in (-1, 1):
        for sy in (-1, 1):
            lx = tx + sx * (table_w / 2.0 - leg_inset - 0.025)
            ly = ty + sy * (table_l / 2.0 - leg_inset - 0.025)
            objs[f'table_leg_{sx:+d}_{sy:+d}'] = _cyl(
                col, f'{name_prefix}_TableLeg_{sx:+d}_{sy:+d}',
                (lx, ly, floor_z + 0.36), 0.025, 0.72, frame_mat)

    # Two stools flanking the table (along table_l short axis facing -Y)
    stool_r = 0.20
    stool_h = 0.45
    stool_y = ty - table_l / 2.0 - stool_r - 0.05
    for sx, tag in ((-1, 'L'), (1, 'R')):
        sx_pos = tx + sx * (table_w / 2.0 - 0.20)
        objs[f'stool_{tag}'] = _cyl(
            col, f'{name_prefix}_Stool_{tag}',
            (sx_pos, stool_y, floor_z + stool_h / 2.0),
            stool_r, stool_h, stool_mat)

    # Shelf against -X wall
    shelf_w = 0.30
    shelf_l = min(1.4, footprint_l - 2 * margin - 0.20)
    shelf_h = 1.6
    sh_x = ox - half_w + shelf_w / 2.0
    sh_y = oy
    objs['shelf'] = _box(
        col, f'{name_prefix}_Shelf',
        (sh_x, sh_y, floor_z + shelf_h / 2.0),
        (shelf_w, shelf_l, shelf_h), frame_mat)

    # Lantern hanging in centre of room (or table-mounted if room is tight)
    emission = _VARIANT_LANTERN_EMISSION.get(variant.upper(), 0.0)
    lantern_mat = _make_lantern_material(
        f'{name_prefix}_LanternEmissive', emission)
    objs['lantern'] = _cyl(
        col, f'{name_prefix}_Lantern',
        (tx, ty, floor_z + 1.85),
        0.09, 0.18, lantern_mat)

    return objs
