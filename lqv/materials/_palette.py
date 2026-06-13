"""Site palette + hex_to_rgb helper.

Keyed to MASTER_BRIEF §2.3 and §12. Do not retune these without re-rendering
the 18 finals at 85e86aa — Cycles base-color anchors shift the byte-identity.
"""
from __future__ import annotations


def hex_to_rgb(h: str) -> tuple[float, float, float, float]:
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0
    return (r, g, b, 1.0)


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
    'palm_thatch':       hex_to_rgb('#8B6B3A'),
    'terracotta_tile':   hex_to_rgb('#A0492A'),
    'lantern_paper_warm': hex_to_rgb('#FFE0A0'),
    'water_reflective':  hex_to_rgb('#3A5060'),
    'rope_natural':      hex_to_rgb('#A88860'),
    'concrete_slab_108': hex_to_rgb('#9A958F'),
}
