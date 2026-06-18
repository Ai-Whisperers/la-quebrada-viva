"""Scene reset and Cycles engine setup."""
from __future__ import annotations

import os

import bpy

from .config import Config


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene


def setup_cycles(scene, config: Config):
    scene.render.engine = 'CYCLES'

    prefs = bpy.context.preferences
    cprefs = prefs.addons['cycles'].preferences
    cprefs.refresh_devices()
    selected_backend = None
    try:
        valid_backends = cprefs.bl_rna.properties['compute_device_type'].enum_items.keys()
    except Exception:
        valid_backends = ('NONE', 'CUDA', 'OPTIX', 'HIP', 'METAL', 'ONEAPI')
    for backend in ('OPTIX', 'CUDA', 'HIP', 'METAL', 'ONEAPI'):
        if backend not in valid_backends:
            continue
        try:
            cprefs.compute_device_type = backend
        except TypeError:
            continue
        devices = [d for d in cprefs.devices if d.type == backend]
        if devices:
            for d in cprefs.devices:
                d.use = (d.type == backend)
            scene.cycles.device = 'GPU'
            selected_backend = backend
            break
    if selected_backend is None:
        if os.environ.get('LQV_ALLOW_CPU_FALLBACK') != '1':
            raise RuntimeError(
                "No GPU compute backend available (tried OPTIX/CUDA/HIP/METAL/ONEAPI). "
                "Re-export LQV_ALLOW_CPU_FALLBACK=1 to render on CPU. Refusing to "
                "silently downgrade — a CPU render at parcel scale takes ~40× longer "
                "and has burned past schedules."
            )
        scene.cycles.device = 'CPU'
        print("[cycles] WARN no GPU backend; LQV_ALLOW_CPU_FALLBACK=1 → CPU render")

    print(f"[cycles] device={scene.cycles.device} backend={selected_backend}")

    scene.cycles.samples = config.samples
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = (
        'OPTIX' if (scene.cycles.device == 'GPU' and selected_backend == 'OPTIX')
        else 'OPENIMAGEDENOISE'
    )
    scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'

    scene.cycles.max_bounces = 12
    scene.cycles.transmission_bounces = 12
    scene.cycles.glossy_bounces = 8
    scene.cycles.volume_bounces = 4
    scene.cycles.transparent_max_bounces = 12
    scene.cycles.caustics_reflective = True
    scene.cycles.caustics_refractive = True

    return selected_backend


def setup_render_output(scene, config: Config):
    scene.render.resolution_x = config.res_x
    scene.render.resolution_y = config.res_y
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '16'


def setup_color_management(scene):
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Punchy'
    scene.view_settings.exposure = 0.0
