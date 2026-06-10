"""Material helpers, palette, and the MAT registry."""
from __future__ import annotations

import bpy


def hex_to_rgb(h: str) -> tuple[float, float, float, float]:
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0
    return (r, g, b, 1.0)


def principled(name, base_color, roughness=0.7, metallic=0.0, ior=1.45,
               transmission=0.0, alpha=1.0, sss=None, sheen=0.0,
               emission_color=None, emission_strength=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = base_color
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['IOR'].default_value = ior
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = transmission
    bsdf.inputs['Alpha'].default_value = alpha
    if sss is not None and 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = sss[0]
        if 'Subsurface Radius' in bsdf.inputs:
            bsdf.inputs['Subsurface Radius'].default_value = sss[1]
    if 'Sheen Weight' in bsdf.inputs:
        bsdf.inputs['Sheen Weight'].default_value = sheen
    if emission_color is not None:
        bsdf.inputs['Emission Color'].default_value = emission_color
        bsdf.inputs['Emission Strength'].default_value = emission_strength
    return m


def add_noise_displacement(mat, scale=8.0, strength=0.02):
    """Bump-shader noise on a material for fine surface variation."""
    nt = mat.node_tree
    bsdf = nt.nodes.get('Principled BSDF')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = scale
    noise.inputs['Detail'].default_value = 8.0
    noise.inputs['Roughness'].default_value = 0.6
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = strength
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    return mat


def add_color_variegation(mat, scale, lit_color, dark_color, mix_fac=0.5):
    """Mix lit/dark base colors via a low-frequency noise so the surface reads
    as variegated rock/cob rather than one flat tone."""
    nt = mat.node_tree
    bsdf = nt.nodes.get('Principled BSDF')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = scale
    noise.inputs['Detail'].default_value = 4.0
    noise.inputs['Roughness'].default_value = 0.55
    mix = nt.nodes.new('ShaderNodeMixRGB')
    mix.inputs['Color1'].default_value = lit_color
    mix.inputs['Color2'].default_value = dark_color
    mix.inputs['Fac'].default_value = mix_fac
    nt.links.new(noise.outputs['Fac'], mix.inputs['Fac'])
    nt.links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    return mat


def assign(obj, material):
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)


# Site palette — keyed to MASTER_BRIEF §2.3 and §12
COL = {
    'laterite_dry':   hex_to_rgb('#C4522A'),
    'laterite_wet':   hex_to_rgb('#8B3A1A'),
    'cob_lime_white': hex_to_rgb('#E8E2D2'),
    'cob_raw':        hex_to_rgb('#A85838'),
    'sandstone_lit':  hex_to_rgb('#7A7268'),
    'sandstone_dark': hex_to_rgb('#5A5448'),
    'moss_wet':       hex_to_rgb('#8BA048'),
    'moss_dry':       hex_to_rgb('#3D4F1A'),
    'canopy_deep':    hex_to_rgb('#1A3A1A'),
    'canopy_lit':     hex_to_rgb('#4A7A2A'),
    'lapacho_pink':   hex_to_rgb('#F4C0D1'),
    'lapacho_bloom':  hex_to_rgb('#E85A8C'),
    'water_deep':     hex_to_rgb('#2A3528'),
    'water_shallow':  hex_to_rgb('#A85832'),
    'lapacho_timber': hex_to_rgb('#5C2D17'),
    'metal_roof':     hex_to_rgb('#3D3026'),
    'bottle_cobalt':  hex_to_rgb('#0047AB'),
    'bottle_amber':   hex_to_rgb('#8B6914'),
    'bottle_green':   hex_to_rgb('#2D5A1B'),
    'bottle_brown':   hex_to_rgb('#4A2C16'),
    'agave':          hex_to_rgb('#7B8F6A'),
}

MAT: dict = {}


def _make_pool_water():
    """Two-layer water — clear surface + light volume tint for laterite turbidity."""
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


def build_materials():
    """Populate MAT in the order the monolith built them. Must be called
    after engine.reset_scene() — materials need a fresh bpy.data."""
    MAT.clear()
    MAT.update({
        'lime_wash':    add_noise_displacement(principled('LimeWash', COL['cob_lime_white'], roughness=0.92), scale=22.0, strength=0.08),
        'cob_raw':      add_noise_displacement(principled('CobRaw',   COL['cob_raw'],       roughness=0.95), scale=12.0, strength=0.18),
        'laterite':     add_noise_displacement(principled('Laterite', COL['laterite_dry'], roughness=1.0),   scale=2.5,  strength=0.10),
        'sandstone':    add_color_variegation(
            add_noise_displacement(principled('Sandstone', COL['sandstone_lit'], roughness=0.95), scale=4.0, strength=0.20),
            scale=1.8, lit_color=COL['sandstone_lit'], dark_color=COL['sandstone_dark'], mix_fac=0.55,
        ),
        'lapacho_timber': principled('LapachoTimber', COL['lapacho_timber'], roughness=0.55),
        'sod_canopy':   add_noise_displacement(principled('SodRoof',  COL['canopy_lit'],   roughness=0.95, sheen=0.15), scale=10.0, strength=0.06),
        'canopy':       principled('Canopy', COL['canopy_deep'], roughness=0.85),
        'lapacho_leaf': principled('LapachoLeaf', COL['canopy_lit'], roughness=0.7),
        'lapacho_flower': principled('LapachoFlower', COL['lapacho_bloom'], roughness=0.55, sss=(0.2, (0.6, 0.2, 0.4))),
        'pindo_trunk':  principled('PindoTrunk', hex_to_rgb('#6A6258'), roughness=0.85),
        'pindo_frond':  principled('PindoFrond', hex_to_rgb('#3D5828'), roughness=0.75),
        'mango_trunk':  principled('MangoTrunk', hex_to_rgb('#3A2A1E'), roughness=0.9),
        'fern_frond':   principled('FernFrond',  hex_to_rgb('#4A6A28'), roughness=0.75),
        'bamboo':       principled('Bamboo',     hex_to_rgb('#8AA055'), roughness=0.7),
        'agave_blade':  principled('AgaveBlade', COL['agave'], roughness=0.55, sss=(0.1, (0.5, 0.6, 0.4))),
        'glass_bottle_cobalt': principled('BottleCobalt', COL['bottle_cobalt'], roughness=0.03, ior=1.52, transmission=1.0),
        'glass_bottle_amber':  principled('BottleAmber',  COL['bottle_amber'],  roughness=0.03, ior=1.52, transmission=1.0),
        'glass_bottle_green':  principled('BottleGreen',  COL['bottle_green'],  roughness=0.03, ior=1.52, transmission=1.0),
        'glass_bottle_brown':  principled('BottleBrown',  COL['bottle_brown'],  roughness=0.03, ior=1.52, transmission=1.0),
        'pool_water':   None,
        'stream_bed':   add_noise_displacement(principled('StreamBed', hex_to_rgb('#5A4E3C'), roughness=0.95), scale=6.0, strength=0.15),
    })
    MAT['pool_water'] = _make_pool_water()
    return MAT
