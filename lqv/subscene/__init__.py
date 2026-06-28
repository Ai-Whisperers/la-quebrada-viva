"""Per-asset isolated sub-render drivers (UPGRADE_PLAN T1.1).

Each `lqv/subscene/<asset>.py` builds a single typology / amenity / house
component / landscape feature into an empty Blender scene and writes a
preview PNG to `renders/sub/<asset>_<variant>.png`. The composite
`build_scene.py` is untouched until step 8 of `docs/sub_render_strategy.md`
§10 — preserves the renderer byte-identity invariant at commit 85e86aa.

Run a driver headless::

    blender --background --python lqv/subscene/cob_walls.py
    RENDER_VARIANT=B RENDER_SKIP=1 blender --background --python lqv/subscene/cob_walls.py
"""
