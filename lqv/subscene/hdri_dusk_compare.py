"""Sub-render: dusk HDRI A/B/C compare.

Neutral test bed for picking which Poly Haven dusk EXR sets the most flattering
late-afternoon mood for the parcel. Layout is intentionally boring — laterite
ground + three mid-gray spheres at z=0.5 spaced 2 m on +X. The differences
between A/B/C are entirely lighting:

* A → ``qwantani_dusk_2_4k.exr`` (warm horizon, the current default)
* B → ``bambanani_sunset_4k.exr`` (saturated sunset, deeper amber)
* C → ``qwantani_sunset_puresky_4k.exr`` (puresky, no foreground silhouettes)

Bypasses :func:`lqv.subscene.base.run` and :func:`lqv.lighting.setup_world_and_sun`
— the latter is variant-bound to a fixed HDRI map, so this driver writes its
own world shader pointing at the per-variant EXR. ``cam.data.clip_end = 20000``
because the puresky variant otherwise gets a clipped horizon.
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy

from lqv import cameras
from lqv.materials import assign, principled
from lqv.subscene import base

ASSET = 'hdri_dusk_compare'

_HDRI_DIR = os.path.join(_PROJECT_ROOT, 'assets', 'hdris')
_HDRI_BY_VARIANT = {
    'A': ('qwantani_dusk_2_4k.exr', 1.0),
    'B': ('bambanani_sunset_4k.exr', 1.0),
    'C': ('qwantani_sunset_puresky_4k.exr', 1.0),
}


def _load_hdri(scene, hdri_path: str, strength: float = 1.0) -> None:
    """Wire ``hdri_path`` into the world Background as the only light source.

    No sun lamp — the point of this test is to read each HDRI's own light
    direction + colour as-is. Falls back to a flat warm gray when the EXR is
    missing so the render still completes (log + skip per the hard constraint).
    """
    world = bpy.data.worlds.new('HDRICompareWorld')
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputWorld')
    bg = nt.nodes.new('ShaderNodeBackground')

    if not os.path.isfile(hdri_path):
        print(f"[hdri_dusk_compare] missing HDRI {hdri_path}, falling back to flat gray")
        bg.inputs['Color'].default_value = (0.35, 0.30, 0.27, 1.0)
        bg.inputs['Strength'].default_value = 1.0
    else:
        env = nt.nodes.new('ShaderNodeTexEnvironment')
        env.image = bpy.data.images.load(hdri_path, check_existing=True)
        bg.inputs['Strength'].default_value = strength
        nt.links.new(env.outputs['Color'], bg.inputs['Color'])

    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])


def _place_test_spheres(z: float = 0.5, spacing: float = 2.0, count: int = 3):
    """Three mid-gray Principled spheres along +X centred on the origin.

    Roughness=0.5 — exactly in the middle of the BRDF range — so the spheres
    pick up both the HDRI's specular highlight (low-rough end) and the
    diffuse colour (high-rough end). Gives the most information-per-pixel
    when comparing dusk EXRs.
    """
    # Standalone mid-gray material so we don't depend on a key in MAT — keeps
    # the HDRI as the only variable across A/B/C.
    mat = principled('HDRICompare_MidGray',
                     base_color=(0.50, 0.50, 0.50, 1.0),
                     roughness=0.5,
                     metallic=0.0)
    start_x = -spacing * (count - 1) / 2.0
    for i in range(count):
        x = start_x + i * spacing
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(x, 0.0, z), segments=48, ring_count=24)
        obj = bpy.context.active_object
        obj.name = f'HDRICompare_Sphere_{i}'
        bpy.ops.object.shade_smooth()
        assign(obj, mat)


if __name__ == '__main__':
    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('laterite')
    _place_test_spheres(z=0.5, spacing=2.0, count=3)

    hdri_name, strength = _HDRI_BY_VARIANT.get(cfg.variant, _HDRI_BY_VARIANT['A'])
    _load_hdri(scene, os.path.join(_HDRI_DIR, hdri_name), strength=strength)

    cam = cameras.subscene_camera(
        target=(0.0, 0.0, 0.5),
        distance=6.0,
        height=2.0,
        lens=50.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.save_subrender(scene, ASSET, cfg)
