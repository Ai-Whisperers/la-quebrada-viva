"""Save .blend + invoke Cycles render."""
from __future__ import annotations

import bpy


def save_blend(path: str):
    bpy.ops.wm.save_as_mainfile(filepath=path)
    print(f'[save] {path}')


def run(scene):
    print(f"[render] starting — {scene.render.filepath}")
    bpy.ops.render.render(write_still=True)
    print(f"[render] complete — {scene.render.filepath}")
