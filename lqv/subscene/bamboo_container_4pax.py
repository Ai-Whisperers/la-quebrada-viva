"""Sub-render: bamboo + container 4-pax guesthouse (Phase E wave 2).

Bypasses ``base.run()`` so we can:
  * pin ``cam.data.clip_end = base.PARCEL_CLIP_END_M`` BEFORE ``render.run(scene)`` — parcel
    scale clip-gotcha (see ``feedback_subscene_clip_end`` memory),
  * scatter a small Guadua clump behind the veranda so the eye reads
    "bamboo grows nearby" rather than "industrial box on bare grass",
  * sit the asset on neutral laterite ground, which reads as a cleared
    construction pad — the honest baseline for a new build.

Camera frames the south-east corner of the building so both the door face
(-Y) and the veranda + sliding door (+X) are visible in the same shot.

Run:
  RENDER_RUN_ID=phase_e_bamboo_container_4pax_20260612 \
  RENDER_RES=preview RENDER_SAMPLES=32 RENDER_VARIANT=A \
  SEED=20260609 \
  /home/ai-whisperers/.local/bin/blender -b -P lqv/subscene/bamboo_container_4pax.py
"""
from __future__ import annotations

import os
import random
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


from lqv import cameras
from lqv.subscene import base

ASSET = 'bamboo_container_4pax'

# Default RENDER_RUN_ID for this wave — override at the shell if needed.
os.environ.setdefault('RENDER_RUN_ID', 'phase_e_bamboo_container_4pax_20260612')


def _scatter_companion_bamboo(seed: int) -> None:
    """Drop 2-3 small Guadua clumps behind the container (north / west of it).

    Procedural even under ``RENDER_FLORA_PHOTOREAL=1`` — bamboo has no CC0
    photoreal proxy in the Poly Haven catalog.
    """
    try:
        from lqv.flora.bamboo import add_bamboo_clump
    except Exception:
        return
    rng = random.Random(seed ^ 0x4C3A19)
    # Behind (north, +Y) and to the west (-X) of the container, away from the
    # camera so they read as a back-drop framing element.
    placements = (
        (-4.2, 3.1, 1.0),
        (-2.6, 3.6, 0.85),
        (-5.0, 0.4, 0.95),
    )
    for x, y, scale in placements:
        jitter_x = x + rng.uniform(-0.30, 0.30)
        jitter_y = y + rng.uniform(-0.30, 0.30)
        add_bamboo_clump(jitter_x, jitter_y, n=rng.randint(6, 9), scale=scale)


if __name__ == '__main__':
    from lqv.typologies.bamboo_container_4pax import build_bamboo_container_4pax

    scene, cfg = base.setup(ASSET)

    # Neutral ground — laterite reads as cleared construction pad, which is
    # honest for a just-completed container guesthouse.
    base.place_neutral_ground('laterite')

    # Pin RNG AFTER materials.build_materials (inside base.setup) and BEFORE
    # the first build_*, per project RNG invariant.
    asset_seed = base.derive_seed(ASSET, cfg.variant) if hasattr(base, 'derive_seed') else 20260612
    random.seed(asset_seed)

    build_bamboo_container_4pax(origin=(0.0, 0.0, 0.0), variant=cfg.variant)
    _scatter_companion_bamboo(asset_seed)

    # Camera: SE corner-ish view so we see the south face (door + windows)
    # AND the east face / veranda + sliding door in one frame.
    cam = cameras.subscene_camera(
        target=(0.0, 0.0, 1.6),
        distance=14.0,
        height=5.0,
        lens=24.0,
    )
    scene.camera = cam
    cam.data.clip_end = base.PARCEL_CLIP_END_M   # parcel-scale clip gotcha

    base.setup_world(scene, cfg.variant)
    base.save_subrender(scene, ASSET, cfg)
