"""Rule 7/9/10 service props — solar steel frame, mesh-capped cistern, battery cabinet.

All deterministic (no random.*) so this builder can slot anywhere in the
build order without disturbing the RNG draw sequence used by flora.populate
and scatter_lapacho_petals.
"""
from __future__ import annotations

import math

import bpy

from ..geometry import add_subdiv_displace
from ..materials import MAT, assign


def build_services():
    objs = []

    # --- Rule 9: Solar PV on a SEPARATE anodized-steel frame, never on the
    # living sod roof. Placed in the east-yard gap between the house roof
    # (extends to x≈+6.9 after 0.9m overhang) and the stream weir (x≈+9.8
    # at the spillway abutments). Southern Hemisphere → panel faces north,
    # so south posts are taller and north posts shorter; panel tilts down
    # toward +Y so its normal points up-and-slightly-south to receive the
    # north-arc winter sun (Paraguari ≈25°S).
    south_h = 3.2
    north_h = 1.6
    span_y = 4.0
    tilt_rad = math.atan2(south_h - north_h, span_y)
    for px in (+7.5, +9.5):
        for py, post_h in ((-2.0, south_h), (+2.0, north_h)):
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.06, depth=post_h, location=(px, py, post_h / 2),
            )
            post = bpy.context.active_object
            post.name = f'SolarPost_x{px:+.1f}_y{py:+.1f}'
            assign(post, MAT['steel_anodized'])
            objs.append(post)
    # Cross rails along x (one per post row) so the panel reads as supported.
    for py, rail_z in ((-2.0, south_h - 0.05), (+2.0, north_h - 0.05)):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(+8.5, py, rail_z))
        rail = bpy.context.active_object
        rail.name = f'SolarRail_y{py:+.1f}'
        rail.scale = (2.2, 0.08, 0.08)
        bpy.ops.object.transform_apply(scale=True)
        assign(rail, MAT['steel_anodized'])
        objs.append(rail)
    # PV panel plane — 2.5m (X) × 4.0m (Y). Rotated about +X by -tilt so the
    # +Y (north) edge drops and the -Y (south) edge sits up against the
    # taller south rail. Centred between rails so it lands at z≈mean(south_h, north_h).
    bpy.ops.mesh.primitive_plane_add(
        size=1, location=(+8.5, 0.0, (south_h + north_h) / 2),
    )
    panel = bpy.context.active_object
    panel.name = 'SolarPanel'
    panel.scale = (2.5, 4.0, 1.0)
    panel.rotation_euler = (-tilt_rad, 0, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    assign(panel, MAT['pv_glass'])
    objs.append(panel)

    # --- Rule 10: Mosquito-proof cistern with visible 0.5mm stainless mesh.
    # Placed NW of the house at (-9, +5), past the 0.9m roof overhang
    # (roof extends to x≈-6.9) so the tank sits in open ground. The mesh
    # cap reads as a dark, porous disc on top of the cob-rendered tank.
    cx, cy = -9.0, 5.0
    # Stone pad
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, 0.10))
    pad = bpy.context.active_object
    pad.name = 'CisternPad'
    pad.scale = (3.6, 3.6, 0.20)
    bpy.ops.object.transform_apply(scale=True)
    add_subdiv_displace(pad, levels=2, noise_scale=4.0, strength=0.03)
    assign(pad, MAT['sandstone'])
    objs.append(pad)
    # Tank — cob-rendered cylinder. Centre at z=1.20 → spans z∈[0.20, 2.20].
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.50, depth=2.00, location=(cx, cy, 1.20),
    )
    tank = bpy.context.active_object
    tank.name = 'CisternTank'
    add_subdiv_displace(tank, levels=2, noise_scale=8.0, strength=0.03)
    assign(tank, MAT['cob_raw'])
    objs.append(tank)
    # Anodized-steel rim at the top edge of the tank
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.50, minor_radius=0.05, location=(cx, cy, 2.20),
    )
    rim = bpy.context.active_object
    rim.name = 'CisternRim'
    assign(rim, MAT['steel_anodized'])
    objs.append(rim)
    # Mesh cap — thin alpha-blended disc just below the rim
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1.48, depth=0.03, location=(cx, cy, 2.18),
    )
    cap = bpy.context.active_object
    cap.name = 'CisternMeshCap'
    assign(cap, MAT['steel_mesh'])
    objs.append(cap)
    # Inlet downspout — anodized-steel pipe from the roof eave toward the
    # tank top. Slight outward tilt so it reads as plumbing, not as a pole.
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.08, depth=1.20, location=(cx + 1.40, cy, 2.65),
    )
    spout = bpy.context.active_object
    spout.name = 'CisternDownspout'
    spout.rotation_euler = (0, math.radians(20), 0)
    bpy.ops.object.transform_apply(rotation=True)
    assign(spout, MAT['steel_anodized'])
    objs.append(spout)

    # --- Rule 7: LiFePO4 battery cabinet — visible utility prop on the
    # NW utilities corner alongside the cistern. Pairs with the pelton
    # micro-hydro at the weir to read as an outage-proof power stack.
    bx, by = cx - 2.4, cy
    bpy.ops.mesh.primitive_cube_add(size=1, location=(bx, by, 0.55))
    cab = bpy.context.active_object
    cab.name = 'BatteryCabinet'
    cab.scale = (0.75, 0.95, 1.00)
    bpy.ops.object.transform_apply(scale=True)
    assign(cab, MAT['steel_anodized'])
    objs.append(cab)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(bx, by, 0.05))
    plinth = bpy.context.active_object
    plinth.name = 'BatteryCabinetPlinth'
    plinth.scale = (0.95, 1.15, 0.10)
    bpy.ops.object.transform_apply(scale=True)
    assign(plinth, MAT['sandstone'])
    objs.append(plinth)

    return objs
