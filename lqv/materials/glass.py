"""Glass materials: cobalt/amber/green/brown bottles, pool water (volumetric)."""
from __future__ import annotations

import bpy

from lqv.materials._palette import COL
from lqv.materials._shaders import principled


def build(MAT: dict) -> None:
    """Populate MAT with bottle glasses.

    Pool water is built via :func:`make_pool_water` and inserted by the facade
    so dict insertion order matches the pre-split monolith.

    Builder calls + parameters are byte-identical to the pre-split monolith;
    do not retune without re-rendering the 18 finals at 85e86aa.
    """
    MAT['glass_bottle_cobalt'] = principled(
        'BottleCobalt', COL['bottle_cobalt'], roughness=0.03, ior=1.52, transmission=1.0,
    )
    MAT['glass_bottle_amber'] = principled(
        'BottleAmber', COL['bottle_amber'], roughness=0.03, ior=1.52, transmission=1.0,
    )
    MAT['glass_bottle_green'] = principled(
        'BottleGreen', COL['bottle_green'], roughness=0.03, ior=1.52, transmission=1.0,
    )
    MAT['glass_bottle_brown'] = principled(
        'BottleBrown', COL['bottle_brown'], roughness=0.03, ior=1.52, transmission=1.0,
    )
    MAT['lantern_paper_warm'] = principled(
        'LanternPaperWarm', COL['lantern_paper_warm'], roughness=0.55,
        emission_color=COL['lantern_paper_warm'], emission_strength=8.0,
    )
    MAT['water_reflective'] = principled(
        'WaterReflective', COL['water_reflective'],
        roughness=0.04, ior=1.333, transmission=0.85,
    )


def make_pool_water():
    """Pool surface: principled glass shell + volume absorption for depth tint.

    Byte-identical to the monolith's `_make_pool_water`; do not retune without
    re-rendering the 18 finals at 85e86aa.
    """
    m = bpy.data.materials.new('PoolWater')
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = COL['water_deep']
    bsdf.inputs['Roughness'].default_value = 0.02
    bsdf.inputs['IOR'].default_value = 1.333
    bsdf.inputs['Transmission Weight'].default_value = 1.0
    vol = nt.nodes.new('ShaderNodeVolumeAbsorption')
    vol.inputs['Color'].default_value = COL['water_shallow']
    vol.inputs['Density'].default_value = 1.6
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    return m
