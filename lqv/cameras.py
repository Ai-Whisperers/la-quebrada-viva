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
