"""Env-var control surface — parsed once at driver start."""
from __future__ import annotations

import os
from dataclasses import dataclass

PROJECT_DIR = os.environ.get(
    'LQV_PROJECT_DIR',
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)
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

VALID_VIEWS = ('hero3q', 'elevation', 'plan', 'section', 'interior')


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
    view: str

    @property
    def output_filename(self) -> str:
        view_tag = '' if self.view == 'hero3q' else f"_{self.view}"
        return f"{'_preview_' if self.is_preview else ''}{self.variant}_{self.cam_name}{view_tag}.png"

    @property
    def output_path(self) -> str:
        return os.path.join(RENDERS_DIR, self.output_filename)


def parse() -> Config:
    variant = os.environ.get('RENDER_VARIANT', 'A').upper()
    if variant not in ('A', 'B', 'C'):
        raise SystemExit(
            f"[config] RENDER_VARIANT={variant!r} not implemented — only A, B, C exist")
    cam_name = os.environ.get('RENDER_CAM', 'hero').lower()
    samples = int(os.environ.get('RENDER_SAMPLES', '128'))
    res_mode = os.environ.get('RENDER_RES', 'preview').lower()
    skip_render = os.environ.get('RENDER_SKIP', '0') == '1'
    view = os.environ.get('RENDER_VIEW', 'hero3q').lower()
    if view not in VALID_VIEWS:
        print(f"[config] WARNING: unknown RENDER_VIEW={view!r}, falling back to "
              f"hero3q (valid: {'|'.join(VALID_VIEWS)})")
        view = 'hero3q'
    if res_mode not in RES_PRESETS:
        print(f"[config] WARNING: unknown RENDER_RES={res_mode!r}, falling back to "
              f"preview 1280x720 (valid: {'|'.join(sorted(set(RES_PRESETS)))})")
        res_mode = 'preview'
    res_x, res_y = RES_PRESETS[res_mode]
    is_preview = res_mode in ('preview', '720')
    os.makedirs(RENDERS_DIR, exist_ok=True)
    return Config(
        variant=variant, cam_name=cam_name, samples=samples,
        res_mode=res_mode, res_x=res_x, res_y=res_y,
        is_preview=is_preview, skip_render=skip_render, view=view,
    )
