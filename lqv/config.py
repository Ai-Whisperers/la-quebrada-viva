"""Env-var control surface — parsed once at driver start."""
from __future__ import annotations

import os
from dataclasses import dataclass

PROJECT_DIR = '/home/ai-whisperers/blender-projects/house-field'
RENDERS_DIR = os.path.join(PROJECT_DIR, 'renders')
BLEND_PATH = os.path.join(PROJECT_DIR, 'scene.blend')

RES_PRESETS = {
    'preview': (1280, 720),
    '720':     (1280, 720),
    'final':   (1920, 1080),
    '1080':    (1920, 1080),
    'hero':    (2560, 1440),
    '1440':    (2560, 1440),
}

SEED = 20260609


@dataclass
class Config:
    variant: str
    cam_name: str
    samples: int
    res_mode: str
    res_x: int
    res_y: int
    is_preview: bool
    skip_render: bool

    @property
    def output_filename(self) -> str:
        return f"{'_preview_' if self.is_preview else ''}{self.variant}_{self.cam_name}.png"

    @property
    def output_path(self) -> str:
        return os.path.join(RENDERS_DIR, self.output_filename)


def parse() -> Config:
    variant = os.environ.get('RENDER_VARIANT', 'A').upper()
    cam_name = os.environ.get('RENDER_CAM', 'hero').lower()
    samples = int(os.environ.get('RENDER_SAMPLES', '128'))
    res_mode = os.environ.get('RENDER_RES', 'preview').lower()
    skip_render = os.environ.get('RENDER_SKIP', '0') == '1'
    res_x, res_y = RES_PRESETS.get(res_mode, RES_PRESETS['preview'])
    is_preview = res_mode in ('preview', '720')
    os.makedirs(RENDERS_DIR, exist_ok=True)
    return Config(
        variant=variant, cam_name=cam_name, samples=samples,
        res_mode=res_mode, res_x=res_x, res_y=res_y,
        is_preview=is_preview, skip_render=skip_render,
    )
