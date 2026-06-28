"""Turntable animation — orbit the camera around the house.

Use case: a short MP4 deliverable for Wesley to show prospective tenants or
investors at the escritura meeting. 12 s @ 24 fps = 288 frames; orbit 360°
at constant elevation around the LQV house.

Status: dormant.
"""
from __future__ import annotations

DEFAULT_RADIUS_M = 22.0
DEFAULT_ELEVATION_M = 7.0
DEFAULT_TARGET = (0.0, 0.0, 2.0)        # house centre, mid-wall height
DEFAULT_FRAMES = 288                     # 12 s @ 24 fps
DEFAULT_FPS = 24


def build_turntable_camera(name: str = 'TurntableCam'):
    """Create + key the orbital camera."""
    raise NotImplementedError('Pending: needs constraint setup + bezier keyframes.')


def render_turntable(out_dir: str, fps: int = DEFAULT_FPS):
    """Render frames to ``out_dir``; mux with ffmpeg externally."""
    raise NotImplementedError('Pending: only after still-frame deliverables ship.')
