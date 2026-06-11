"""RNG / build-order invariants for the 18-final byte-identity at 85e86aa.

These tests parse build_scene.py as text — they do NOT import bpy or run
Blender. They guard the contract documented in CLAUDE.md "Code invariants":

  1. SEED is the frozen project seed (20260609).
  2. random.seed(config.SEED) sits AFTER materials.build_materials() and
     BEFORE the first build_* call in build_scene.py.
  3. The composite call order matches the frozen baseline exactly. Any
     reorder, insertion, or removal in this list invalidates the 18
     finals at 85e86aa and requires re-rendering.

The frozen sequence below is the byte-identity baseline. Do not edit it to
make a regression pass — re-render and re-shoot the finals instead.
"""
from __future__ import annotations

import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_SCENE = os.path.join(PROJECT_ROOT, 'build_scene.py')


FROZEN_CALL_ORDER = [
    'materials.build_materials()',
    'random.seed(config.SEED)',
    'build_escarpment()',
    'build_ground()',
    'build_terraces()',
    'build_cob_house()',
    'build_bottle_wall()',
    'build_tatakua()',
    'build_stream()',
    'build_services()',
    'build_window_emission(cfg.variant)',
    'flora.populate(flowering_lapacho=flowering)',
    'flora.scatter_lapacho_petals(n=100)',
    'flora.scatter_grass_tufts(n=80)',
    'flora.scatter_anthuriums()',
    'flora.scatter_fireflies(n=80, variant=cfg.variant)',
]


def _source() -> str:
    with open(BUILD_SCENE, encoding='utf-8') as f:
        return f.read()


def test_seed_constant_frozen():
    from lqv import config
    assert config.SEED == 20260609, (
        f"SEED changed from frozen baseline 20260609 to {config.SEED}; "
        "this invalidates the 18 finals at 85e86aa.")


def test_build_scene_call_order_matches_frozen():
    """Every frozen call must appear in build_scene.py in the exact order."""
    src = _source()
    last_idx = -1
    for call in FROZEN_CALL_ORDER:
        idx = src.find(call)
        assert idx != -1, (
            f"Frozen call {call!r} missing from build_scene.py. "
            "Removing or renaming this call breaks RNG draw order.")
        assert idx > last_idx, (
            f"Frozen call {call!r} appears out of order in build_scene.py. "
            f"It came at offset {idx} but the previous frozen call ended at {last_idx}. "
            "Reordering the composite invalidates the byte-identity of the 18 finals.")
        last_idx = idx + len(call)


def test_random_seed_after_materials_and_before_first_build():
    src = _source()
    materials_idx = src.find('materials.build_materials()')
    seed_idx = src.find('random.seed(config.SEED)')
    first_build_idx = src.find('build_escarpment()')

    assert materials_idx != -1
    assert seed_idx != -1
    assert first_build_idx != -1

    assert materials_idx < seed_idx, (
        "random.seed() must come AFTER materials.build_materials(). "
        "Materials are deterministic and must not consume RNG state.")
    assert seed_idx < first_build_idx, (
        "random.seed() must come BEFORE the first build_* call. "
        "build_escarpment is the first RNG consumer.")


def test_no_random_call_before_seed():
    """No random.* method invocation may appear before random.seed()."""
    src = _source()
    seed_idx = src.find('random.seed(config.SEED)')
    head = src[:seed_idx]
    forbidden = re.findall(r'\brandom\.(?!seed\b)[a-zA-Z_]+\(', head)
    assert not forbidden, (
        f"random.* calls before the seed: {forbidden}. "
        "Any RNG draw upstream of the seed silently shifts every downstream "
        "scatter and breaks byte-identity.")


def test_petal_scatter_only_inside_flowering_branch():
    """scatter_lapacho_petals must remain gated on Variant A (flowering=True).

    Petals consume RNG state. If they fire on B or C, the post-petal RNG
    draws (grass_tufts, anthuriums, fireflies) shift on those variants.
    """
    src = _source()
    petal_call = 'flora.scatter_lapacho_petals(n=100)'
    petal_idx = src.find(petal_call)
    assert petal_idx != -1, f"{petal_call} missing"
    if_idx = src.rfind('if flowering:', 0, petal_idx)
    assert if_idx != -1, (
        "scatter_lapacho_petals must be inside an `if flowering:` block. "
        "Calling it unconditionally breaks B/C byte-identity.")
    between = src[if_idx:petal_idx]
    assert between.count('\n') <= 3, (
        "scatter_lapacho_petals drifted away from its `if flowering:` guard.")
