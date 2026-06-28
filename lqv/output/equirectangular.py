"""Equirectangular panorama output.

Use case: drop an interactive 360° viewer on the housing-park web page so a
prospective European guest can "stand inside the corredor". Requires a
panoramic camera with equirectangular type, 2:1 aspect, full sphere.

Status: dormant.
"""
from __future__ import annotations

DEFAULT_WIDTH = 4096
DEFAULT_HEIGHT = 2048       # 2:1 enforced
DEFAULT_SAMPLES = 256
PANORAMIC_CAMERA_TYPE = 'PANO'
PANORAMIC_TYPE = 'EQUIRECTANGULAR'

VIEWPOINTS = (
    # (name, location, friendly_label)
    ('PanoCorredor',  (0.0, -3.5, 1.6),  'standing on the corredor'),
    ('PanoLivingRoom',(0.0, 0.0, 1.6),   'centre of the living room'),
    ('PanoStreamPool',(8.0, -22.0, 1.6), 'beside the stream pool'),
)


def add_panoramic_camera(name: str, location):
    """Add a Cycles equirectangular camera at ``location``."""
    raise NotImplementedError('Pending: needs Cycles cam settings + render output configuration.')


def render_panorama(viewpoint_name: str, out_path: str):
    """Render a single 2:1 equirectangular PNG for ``viewpoint_name``."""
    raise NotImplementedError('Pending: only after still-frame deliverables ship.')
