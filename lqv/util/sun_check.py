"""Sun azimuth/elevation sanity check.

Variant A is documented as "winter golden hour, sun NNW, elevation
deliberately 13° in code vs brief's 20° — keep" (CLAUDE.md §44). Anyone
adjusting `lqv/lighting.py` without reading the comment will be tempted to
"fix" the 13° to 20°; this audit makes the deliberate value explicit.

Reads the SUN light's rotation after build and reports azimuth/elevation in
degrees. Run inside Blender after build::

    from lqv.util import sun_check
    sun_check.run()
"""
from __future__ import annotations

import math

import bpy

EXPECTED_BY_VARIANT = {
    'A': {'elevation_deg': 13.0, 'azimuth_deg': 337.5, 'tolerance_deg': 2.5},  # NNW
    'B': {'elevation_deg': 35.0, 'azimuth_deg': 90.0, 'tolerance_deg': 5.0},   # morning E
    'C': {'elevation_deg': -8.0, 'azimuth_deg': 270.0, 'tolerance_deg': 5.0},  # below horizon, moonlight from W
}


def _euler_to_az_el(euler) -> tuple[float, float]:
    """Convert a Blender SUN's Euler to (azimuth_deg, elevation_deg).

    Blender SUN points down -Z by default; rotation rotates the light's local
    axis. Elevation = 90° - angle between sun direction and +Z. Azimuth = atan2
    of the XY component, measured from +Y (north) clockwise.
    """
    rx, ry, rz = euler.x, euler.y, euler.z
    # Direction the light POINTS: rotate (0,0,-1) by Euler XYZ.
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    dx = cz * sy * cx + sz * sx
    dy = sz * sy * cx - cz * sx
    dz = cy * cx
    dx, dy, dz = -dx, -dy, -dz
    elevation = math.degrees(math.asin(dz))
    azimuth = (math.degrees(math.atan2(dx, dy)) + 360.0) % 360.0
    return azimuth, elevation


def run(variant: str | None = None, verbose: bool = True) -> list[str]:
    suns = [o for o in bpy.data.objects if o.type == 'LIGHT' and o.data.type == 'SUN']
    if not suns:
        msg = "no SUN light found — variant probably uses HDRI only"
        if verbose:
            print(f"[sun_check] {msg}")
        return [msg]

    issues: list[str] = []
    for sun in suns:
        az, el = _euler_to_az_el(sun.rotation_euler)
        if verbose:
            print(f"[sun_check] {sun.name}: azimuth={az:.1f}°  elevation={el:.1f}°")
        if variant and variant in EXPECTED_BY_VARIANT:
            exp = EXPECTED_BY_VARIANT[variant]
            d_el = abs(el - exp['elevation_deg'])
            d_az = min(abs(az - exp['azimuth_deg']), 360.0 - abs(az - exp['azimuth_deg']))
            tol = exp['tolerance_deg']
            if d_el > tol or d_az > tol:
                issues.append(
                    f"{sun.name}: variant {variant} expected az={exp['azimuth_deg']:.1f}°±{tol}, "
                    f"el={exp['elevation_deg']:.1f}°±{tol}; got az={az:.1f}°, el={el:.1f}°"
                )
    return issues
