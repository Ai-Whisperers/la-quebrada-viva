"""MAT registry and material builders.

`MAT` is a global string-keyed dict; builders look up materials by key at call
time. ``build_materials()`` must be invoked once at the start of a scene
build (before any ``build_*`` call that uses MAT) and AFTER any ``random.seed``
the rest of the build relies on — the no-RNG-in-materials contract is asserted
by ``tests/test_rng_invariants.py``.

The implementation is split into thematic submodules for navigability:

* :mod:`._palette` — COL palette + ``hex_to_rgb`` helper.
* :mod:`._shaders` — Principled BSDF / displacement / PBR primitives.
* :mod:`.earth`   — lime_wash, cob_raw, laterite, sandstone, moss, stream_bed.
* :mod:`.wood`    — lapacho timber/bark, pindo/mango trunks, bamboo.
* :mod:`.foliage` — sod, canopy, leaves, flowers, fronds, agave, anthurium.
* :mod:`.glass`   — bottle cobalt/amber/green/brown, pool water (volumetric).
* :mod:`.props`   — steel anodized/mesh, PV glass, window glow, firefly.

Only ``MAT``, ``assign``, ``build_materials``, and ``COL`` are part of the
public surface — downstream code already imports those by name from
``lqv.materials``.
"""
from __future__ import annotations

from lqv.materials import earth, foliage, glass, props, wood
from lqv.materials._palette import COL
from lqv.materials._shaders import assign

MAT: dict = {}


def build_materials() -> None:
    """(Re)build every entry in :data:`MAT`.

    Submodule builders are invoked thematically. Builder calls + parameters are
    byte-identical to the pre-split monolith — Cycles render output of the 18
    finals at ``85e86aa`` must remain bit-for-bit identical. Do not retune
    without re-rendering.
    """
    MAT.clear()
    earth.build(MAT)
    wood.build(MAT)
    foliage.build(MAT)
    glass.build(MAT)
    props.build(MAT)
    MAT['pool_water'] = glass.make_pool_water()


__all__ = ['MAT', 'COL', 'assign', 'build_materials']
