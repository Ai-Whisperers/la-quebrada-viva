"""Material helpers, palette, and the MAT registry."""
from __future__ import annotations

import os

import bpy


_TEX_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'assets', 'textures',
)


def _load_image(path: str):
    if not os.path.isfile(path):
        return None
    return bpy.data.images.load(path, check_existing=True)


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


def textured_principled(name, asset_id, uv_scale=1.0, tint_color=None, tint_fac=0.0,
                        roughness_bias=0.0, displacement_strength=0.05,
                        normal_strength=1.0):
    """PBR material built from a Poly Haven texture set in assets/textures/<asset_id>/.

    Wires Diffuse (optionally tinted toward `tint_color` via MULTIPLY mix),
    nor_gl, Rough, AO-into-base-color, and true Displacement on Material Output.
    Falls back to a flat principled tint if any diffuse map is missing — keeps
    the build resilient on a fresh clone before scripts/download_assets.sh runs.
    """
    base = tint_color if tint_color is not None else (0.5, 0.5, 0.5, 1.0)
    m = principled(name, base, roughness=0.9)
    nt = m.node_tree
    bsdf = nt.nodes.get('Principled BSDF')

    asset_dir = os.path.join(_TEX_DIR, asset_id)
    diff = _load_image(os.path.join(asset_dir, f'{asset_id}_Diffuse_4k.jpg'))
    if diff is None:
        return m

    norm = _load_image(os.path.join(asset_dir, f'{asset_id}_nor_gl_4k.jpg'))
    rough = _load_image(os.path.join(asset_dir, f'{asset_id}_Rough_4k.jpg'))
    ao = _load_image(os.path.join(asset_dir, f'{asset_id}_AO_4k.jpg'))
    disp = _load_image(os.path.join(asset_dir, f'{asset_id}_Displacement_4k.jpg'))

    # World-space Position from the Geometry node — gives true metric tiling
    # (uv_scale=1/8 ⇒ one tile per 8m), unlike Generated/UV which normalize to
    # the bounding box and would stretch one tile across the whole ground.
    geom = nt.nodes.new('ShaderNodeNewGeometry')
    mapping = nt.nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (uv_scale, uv_scale, uv_scale)
    nt.links.new(geom.outputs['Position'], mapping.inputs['Vector'])

    diff_node = nt.nodes.new('ShaderNodeTexImage')
    diff_node.image = diff
    nt.links.new(mapping.outputs['Vector'], diff_node.inputs['Vector'])
    base_socket = diff_node.outputs['Color']

    if ao is not None:
        ao.colorspace_settings.name = 'Non-Color'
        ao_node = nt.nodes.new('ShaderNodeTexImage')
        ao_node.image = ao
        nt.links.new(mapping.outputs['Vector'], ao_node.inputs['Vector'])
        ao_mul = nt.nodes.new('ShaderNodeMixRGB')
        ao_mul.blend_type = 'MULTIPLY'
        # Cycles already computes its own AO from geometry; texture-baked AO is
        # just a low-frequency cavity hint. Keep contribution gentle.
        ao_mul.inputs['Fac'].default_value = 0.2
        nt.links.new(base_socket, ao_mul.inputs['Color1'])
        nt.links.new(ao_node.outputs['Color'], ao_mul.inputs['Color2'])
        base_socket = ao_mul.outputs['Color']

    if tint_color is not None and tint_fac > 0.0:
        tint = nt.nodes.new('ShaderNodeMixRGB')
        # Plain MIX (linear interpolation) — holds the brief palette luminance
        # while keeping texture variation via the inverse fac toward diffuse.
        tint.blend_type = 'MIX'
        tint.inputs['Fac'].default_value = tint_fac
        tint.inputs['Color2'].default_value = tint_color
        nt.links.new(base_socket, tint.inputs['Color1'])
        base_socket = tint.outputs['Color']

    nt.links.new(base_socket, bsdf.inputs['Base Color'])

    if norm is not None:
        norm.colorspace_settings.name = 'Non-Color'
        norm_node = nt.nodes.new('ShaderNodeTexImage')
        norm_node.image = norm
        nt.links.new(mapping.outputs['Vector'], norm_node.inputs['Vector'])
        nm = nt.nodes.new('ShaderNodeNormalMap')
        nm.inputs['Strength'].default_value = normal_strength
        nt.links.new(norm_node.outputs['Color'], nm.inputs['Color'])
        nt.links.new(nm.outputs['Normal'], bsdf.inputs['Normal'])

    if rough is not None:
        rough.colorspace_settings.name = 'Non-Color'
        rough_node = nt.nodes.new('ShaderNodeTexImage')
        rough_node.image = rough
        nt.links.new(mapping.outputs['Vector'], rough_node.inputs['Vector'])
        if roughness_bias != 0.0:
            add = nt.nodes.new('ShaderNodeMath')
            add.operation = 'ADD'
            add.inputs[1].default_value = roughness_bias
            add.use_clamp = True
            nt.links.new(rough_node.outputs['Color'], add.inputs[0])
            nt.links.new(add.outputs['Value'], bsdf.inputs['Roughness'])
        else:
            nt.links.new(rough_node.outputs['Color'], bsdf.inputs['Roughness'])

    if disp is not None and displacement_strength > 0.0:
        disp.colorspace_settings.name = 'Non-Color'
        disp_node = nt.nodes.new('ShaderNodeTexImage')
        disp_node.image = disp
        nt.links.new(mapping.outputs['Vector'], disp_node.inputs['Vector'])
        disp_shader = nt.nodes.new('ShaderNodeDisplacement')
        disp_shader.inputs['Scale'].default_value = displacement_strength
        disp_shader.inputs['Midlevel'].default_value = 0.5
        nt.links.new(disp_node.outputs['Color'], disp_shader.inputs['Height'])
        out_node = nt.nodes.get('Material Output')
        if out_node is not None:
            nt.links.new(disp_shader.outputs['Displacement'], out_node.inputs['Displacement'])

    return m


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
    'lapacho_bark':   hex_to_rgb('#5C4A3A'),
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
        # Ground PBR per asset_plan.md §C.2. Tint multiplies the Diffuse toward
        # the brief palette so Paraguayan laterite reads warm-red regardless of
        # the Poly Haven source plate.
        'laterite':     textured_principled(
            'Laterite', 'aerial_mud_1',
            uv_scale=1.0 / 8.0,  # 8m tile across hero camera frame
            tint_color=COL['laterite_dry'], tint_fac=0.65,
            displacement_strength=0.04,
        ),
        'sandstone':    textured_principled(
            'Sandstone', 'dry_riverbed_rock',
            uv_scale=1.0 / 4.0,  # ~4m tile so boulder grain reads at hero distance
            tint_color=COL['sandstone_lit'], tint_fac=0.30,
            displacement_strength=0.06,
            normal_strength=1.2,
        ),
        'moss':         textured_principled(
            'Moss', 'aerial_grass_rock',
            uv_scale=1.0 / 6.0,
            tint_color=COL['moss_wet'], tint_fac=0.35,
            displacement_strength=0.03,
        ),
        'lapacho_timber': principled('LapachoTimber', COL['lapacho_timber'], roughness=0.55),
        # Bark for the living trunk + limbs — tree_bark_03 PBR set tinted toward
        # the lapacho_bark palette. uv_scale ~1/0.6 gives one tile every ~60cm,
        # matched to the 40cm-diameter trunk so bark grain reads at hero distance.
        'lapacho_bark': textured_principled(
            'LapachoBark', 'tree_bark_03',
            uv_scale=1.0 / 0.6,
            tint_color=COL['lapacho_bark'], tint_fac=0.25,
            displacement_strength=0.02,
            normal_strength=1.4,
        ),
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
        'anthurium_leaf': principled(
            'AnthuriumLeaf', hex_to_rgb('#2E4A1E'),
            roughness=0.42, sss=(0.08, (0.4, 0.55, 0.3)),
        ),
        'glass_bottle_cobalt': principled('BottleCobalt', COL['bottle_cobalt'], roughness=0.03, ior=1.52, transmission=1.0),
        'glass_bottle_amber':  principled('BottleAmber',  COL['bottle_amber'],  roughness=0.03, ior=1.52, transmission=1.0),
        'glass_bottle_green':  principled('BottleGreen',  COL['bottle_green'],  roughness=0.03, ior=1.52, transmission=1.0),
        'glass_bottle_brown':  principled('BottleBrown',  COL['bottle_brown'],  roughness=0.03, ior=1.52, transmission=1.0),
        'pool_water':   None,
        'stream_bed':   textured_principled(
            'StreamBed', 'dry_riverbed_rock',
            uv_scale=1.0 / 3.0,
            tint_color=hex_to_rgb('#5A4E3C'), tint_fac=0.40,
            displacement_strength=0.04,
        ),
        # Rule 9 / 10 props — solar steel frame, PV cover glass, mesh tank cap.
        # Deterministic principled BSDFs (no random) so the Phase-5 props build
        # without shifting the RNG draw order downstream.
        'steel_anodized': principled(
            'SteelAnodized', hex_to_rgb('#2A2A2C'),
            roughness=0.42, metallic=0.92, ior=1.45,
        ),
        'pv_glass': principled(
            'PvGlass', hex_to_rgb('#0A1A2A'),
            roughness=0.12, metallic=0.0, ior=1.5,
        ),
        # 0.5mm stainless mesh cap (rule 10). Real woven texture would need an
        # alpha-mapped image; this dark metallic + alpha=0.55 reads as a fine
        # porous cover at hero distance, which is what we need to verify rule 10.
        'steel_mesh': principled(
            'SteelMesh', hex_to_rgb('#3A3A3D'),
            roughness=0.32, metallic=0.85, ior=1.45, alpha=0.55,
        ),
    })
    MAT['pool_water'] = _make_pool_water()
    return MAT
