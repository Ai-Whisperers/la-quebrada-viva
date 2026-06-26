"""Sub-render: informal boulder seating cluster (Labrisa Lounge dressing).

A 5-7 boulder semicircle that reads as informal seating around a creek edge
or firepit. Uses the Poly Haven CC0 boulder set:

* ``boulder_01_4k.blend``         — large hero stone at the centre
* ``namaqualand_boulder_02_4k.blend`` — medium
* ``namaqualand_boulder_03_4k.blend`` — medium
* ``namaqualand_boulder_04_4k.blend`` — small

Bypasses :func:`lqv.subscene.base.run` so we can pin ``cam.data.clip_end``
above 100 m (parcel-scale-safe per ``feedback_subscene_clip_end``). The RNG
seed is drawn AFTER :func:`materials.build_materials` so the no-RNG-in-
materials contract is preserved.

Shares its placement logic with :func:`lqv.amenities.labrisa_lounge.
_add_boulder_seating` — see that helper for the in-amenity equivalent.
"""
from __future__ import annotations

import math
import os
import random
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy

from lqv import cameras
from lqv.subscene import base

ASSET = 'boulder_cluster'

MODEL_DIR = os.path.join(_PROJECT_ROOT, 'assets', 'models')
BOULDER_BLENDS = {
    'large':   os.path.join(MODEL_DIR, 'boulder_01', 'boulder_01_4k.blend'),
    'medium_a': os.path.join(MODEL_DIR, 'namaqualand_boulder_02', 'namaqualand_boulder_02_4k.blend'),
    'medium_b': os.path.join(MODEL_DIR, 'namaqualand_boulder_03', 'namaqualand_boulder_03_4k.blend'),
    'small':   os.path.join(MODEL_DIR, 'namaqualand_boulder_04', 'namaqualand_boulder_04_4k.blend'),
}


def _append_boulder(blend_path: str) -> bpy.types.Object | None:
    """Append the largest mesh object from ``blend_path`` into the active scene.

    Returns ``None`` if the asset blend is missing (logged + skipped per the
    hard constraint). Mirrors the pattern in
    :func:`lqv.flora.photoreal._append_object_from_blend`.
    """
    if not os.path.exists(blend_path):
        print(f"[boulder_cluster] missing asset {blend_path}, skipping")
        return None
    before = set(bpy.data.objects.keys())
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        data_to.objects = list(data_from.objects)
    new_objs = [bpy.data.objects[n] for n in bpy.data.objects.keys() if n not in before]
    mesh_objs = [o for o in new_objs if o.type == 'MESH' and o.data is not None]
    if not mesh_objs:
        print(f"[boulder_cluster] no mesh in {blend_path}, skipping")
        return None
    mesh_objs.sort(key=lambda o: len(o.data.polygons), reverse=True)
    hero = mesh_objs[0]
    for o in new_objs:
        try:
            bpy.context.collection.objects.unlink(o)
        except RuntimeError:
            pass
    bpy.context.collection.objects.link(hero)
    return hero


def _place_boulder_cluster(center=(0.0, 0.0, 0.0), radius: float = 3.0, count: int = 6):
    """Scatter 5-7 boulders in a loose semicircle facing +Y.

    First boulder is the hero (boulder_01) at the centre; the rest are
    medium/small Namaqualand stones arrayed along the arc with random
    orientation and ±20 % scale jitter. RNG must already be seeded by
    :func:`base.setup` (post-materials.build_materials).
    """
    count = max(5, min(7, count))
    cx, cy, cz = center
    placed: list[bpy.types.Object] = []

    # Hero in the centre — the large boulder reads as the focal piece, all
    # other stones gather around it like a council ring.
    hero = _append_boulder(BOULDER_BLENDS['large'])
    if hero is not None:
        hero.location = (cx, cy, cz)
        hero.rotation_euler = (0.0, 0.0, random.uniform(0.0, 2.0 * math.pi))
        s = 1.0 + random.uniform(-0.20, 0.20)
        hero.scale = (s, s, s)
        placed.append(hero)

    # Arc spans ~200° around the hero — leaves the +Y side open so the camera
    # at (+,−,height) reads through the gap toward the central boulder.
    surround_count = count - 1
    arc_start_deg = -100.0
    arc_span_deg = 200.0
    surround_keys = ['medium_a', 'medium_b', 'small', 'medium_a', 'medium_b', 'small']
    for i in range(surround_count):
        t = i / max(surround_count - 1, 1)
        angle_rad = math.radians(arc_start_deg + t * arc_span_deg)
        r_jit = radius + random.uniform(-0.4, 0.4)
        x = cx + r_jit * math.cos(angle_rad)
        y = cy + r_jit * math.sin(angle_rad)
        key = surround_keys[i % len(surround_keys)]
        obj = _append_boulder(BOULDER_BLENDS[key])
        if obj is None:
            continue
        obj.location = (x, y, cz)
        obj.rotation_euler = (
            random.uniform(-0.15, 0.15),
            random.uniform(-0.15, 0.15),
            random.uniform(0.0, 2.0 * math.pi),
        )
        s = 1.0 + random.uniform(-0.20, 0.20)
        obj.scale = (s, s, s)
        placed.append(obj)

    return placed


if __name__ == '__main__':
    scene, cfg = base.setup(ASSET)
    base.place_neutral_ground('laterite')

    # RNG seeded inside base.setup() AFTER materials.build_materials() — the
    # no-RNG-in-materials contract is intact. Pick a 5-7 count from the seeded
    # stream so the variant changes the cluster size deterministically.
    boulder_count = random.randint(5, 7)
    _place_boulder_cluster(center=(0.0, 0.0, 0.0), radius=3.0, count=boulder_count)

    base.setup_world(scene, cfg.variant)
    cam = cameras.make_view_camera(
        cfg,
        target=(0.0, 0.0, 0.8),
        distance=8.0,
        height=2.5,
        lens=35.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M

    base.save_subrender(scene, ASSET, cfg)
