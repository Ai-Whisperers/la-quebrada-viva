"""Six camera positions per brief §13.2."""
from __future__ import annotations

import bpy
from mathutils import Vector


def add_camera(name, location, look_at, lens=35.0):
    bpy.ops.object.camera_add(location=location)
    cam = bpy.context.active_object
    cam.name = name
    cam.data.lens = lens
    cam.data.sensor_width = 36.0
    # Point at look_at
    direction = Vector(look_at) - Vector(location)
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = direction.to_track_quat('-Z', 'Y')
    cam.rotation_mode = 'XYZ'
    return cam


def build_cameras():
    cams = {}
    # 1. Hero wide — Z2 pool foreground, cob house mid, escarpment behind.
    #    Pool is at (12,-22,-0.18); pull camera back and tilt down so the pool
    #    fills the lower third of frame and the house sits mid-ground.
    cams['hero'] = add_camera(
        'Cam_Hero', location=(18.0, -33.0, 2.4), look_at=(10.0, -20.0, 0.1), lens=28.0,
    )
    # 2. Stream upstream — from footbridge looking up the channel
    cams['stream_up'] = add_camera(
        'Cam_StreamUp', location=(11.0, -19.0, 1.4), look_at=(11.5, 0.0, 1.0), lens=35.0,
    )
    # 3. Terrace overview — from house position looking downhill
    cams['terrace'] = add_camera(
        'Cam_Terrace', location=(0.0, -4.0, 2.5), look_at=(5.0, -22.0, 0.0), lens=28.0,
    )
    # 4. Cliff backdrop — from glade looking north, pindo palms in foreground
    cams['cliff'] = add_camera(
        'Cam_Cliff', location=(-2.0, -18.0, 1.6), look_at=(-2.0, 35.0, 20.0), lens=24.0,
    )
    # 5. Dusk / blue hour — glade, low angle
    cams['dusk'] = add_camera(
        'Cam_Dusk', location=(2.0, -22.0, 0.8), look_at=(0.0, -5.0, 2.0), lens=35.0,
    )
    # 6. Detail — lapacho petals carpeting laterite. 85mm at 1m framed a 43cm
    # patch and caught ~2 petals; pulled back to 3.5m with 50mm so the dense
    # σ=1.2 cluster around (-3,-10) reads as a carpet.
    cams['petal_macro'] = add_camera(
        'Cam_PetalMacro', location=(-3.0, -13.5, 0.8), look_at=(-3.0, -10.0, 0.2), lens=50.0,
    )
    return cams


def subscene_camera(target=(0.0, 0.0, 1.0), distance: float = 6.0,
                    height: float = 2.4, lens: float = 35.0):
    """Single 3/4-front camera for sub-render drivers.

    Placed at (+distance, -distance, height) so the asset reads from the
    typical south-east hero angle without rebuilding the 6-camera matrix.
    """
    tx, ty, _tz = target
    loc = (tx + distance, ty - distance, height)
    return add_camera('Cam_Subscene', location=loc, look_at=target, lens=lens)


def _make_ortho(name: str, location, look_at, ortho_scale: float):
    cam = add_camera(name, location=location, look_at=look_at, lens=50.0)
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = ortho_scale
    return cam


def subscene_ortho_elevation(target=(0.0, 0.0, 1.5), distance: float = 20.0,
                             height: float = 1.5, ortho_scale: float = 12.0):
    """Orthographic side elevation looking +Y at the asset.

    Placed `distance` metres south of the target, at the target's height, so
    the projected image reads as a clean architectural elevation: no
    perspective foreshortening, lapacho_timber siding aligns to the picture
    plane. ortho_scale = visible width in metres along the long axis.
    """
    tx, ty, tz = target
    look_at = (tx, ty, max(tz, height))
    return _make_ortho(
        'Cam_SubsceneElevation',
        location=(tx, ty - distance, height),
        look_at=look_at,
        ortho_scale=ortho_scale,
    )


def subscene_plan_camera(target=(0.0, 0.0, 0.0), height: float = 25.0,
                         ortho_scale: float = 18.0):
    """Top-down orthographic plan view, camera at (tx, ty, height) looking -Z.

    Used for site-plan and roof-plan shots. `height` sits well above the
    tallest expected roof; `ortho_scale` controls visible site width.
    """
    tx, ty, _tz = target
    cam = _make_ortho(
        'Cam_SubscenePlan',
        location=(tx, ty, height),
        look_at=(tx, ty, 0.0),
        ortho_scale=ortho_scale,
    )
    return cam


def subscene_section_camera(target=(0.0, 0.0, 1.5), distance: float = 14.0,
                            height: float = 1.5, ortho_scale: float = 10.0,
                            section_axis: str = 'x',
                            section_depth: float = 6.0):
    """Orthographic section view with near-clip slicing the asset open.

    Camera looks along ±`section_axis` (so the cut plane is perpendicular).
    `clip_start` is pushed forward by (distance - section_depth/2) so the
    near half of the asset is clipped away, exposing interior framing for
    cutaway diagrams. Pair with `apply_xray_override` (P1.B.3) for the
    "x-ray" reading.
    """
    tx, ty, tz = target
    look_at = (tx, ty, max(tz, height))
    if section_axis.lower() == 'x':
        loc = (tx + distance, ty, height)
    elif section_axis.lower() == 'y':
        loc = (tx, ty - distance, height)
    else:
        raise ValueError(
            f"section_axis must be 'x' or 'y' (got {section_axis!r})")
    cam = _make_ortho(
        'Cam_SubsceneSection',
        location=loc,
        look_at=look_at,
        ortho_scale=ortho_scale,
    )
    cam.data.clip_start = max(0.001, distance - section_depth / 2.0)
    return cam


def subscene_interior_camera(target=(0.0, 0.0, 1.5), distance: float = 2.0,
                             height: float = 1.6, lens: float = 18.0):
    """Wide-FOV perspective placed inside the asset envelope.

    Default 18 mm matches real-estate interior framing on a 36 mm full-frame
    sensor (~90° horizontal FOV). `height` defaults to 1.6 m (standing eye
    level); `distance` is a small backstep from the target so the operator
    can place the camera against an interior wall without clipping into it.
    """
    tx, ty, tz = target
    look_at = (tx, ty, max(tz, height))
    loc = (tx - distance, ty, height)
    return add_camera(
        'Cam_SubsceneInterior', location=loc, look_at=look_at, lens=lens)


def make_view_camera(cfg, target=(0.0, 0.0, 1.0), distance: float = 6.0,
                     height: float = 2.4, lens: float = 35.0):
    """Dispatch on cfg.view to the matching subscene camera helper.

    'hero3q' (default) keeps the legacy 3/4-front perspective so existing
    drivers and shipped finals are unaffected. Orthographic / interior views
    ignore the perspective-specific knobs (distance / height / lens) where
    they would be nonsensical and use the helper's defaults instead.

    Public so parcel-scale drivers that bypass ``base.run()`` (e.g.
    ``bamboo_river_house``) can still honor ``RENDER_VIEW`` without
    re-implementing the dispatch table.
    """
    view = getattr(cfg, 'view', 'hero3q')
    if view == 'elevation':
        return subscene_ortho_elevation(target=target)
    if view == 'plan':
        return subscene_plan_camera(target=target)
    if view == 'section':
        return subscene_section_camera(target=target)
    if view == 'interior':
        return subscene_interior_camera(target=target)
    return subscene_camera(
        target=target, distance=distance, height=height, lens=lens)
