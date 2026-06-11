"""Concept-model stubs for the 8 housing-park typologies.

Per ``docs/HOUSING_PARK_CONCEPT.md`` the 62-ha site holds eight distinct
example buildings around the central restaurant + amenities core. La Quebrada
Viva (this repo's current scene) is **#1 only**. The remaining seven each get
their own dormant builder module so the typology can be sketched in code
without dragging it into the active LQV render path.

Each builder follows the same shape::

    def build(parent: bpy.types.Collection | None = None,
              location: tuple[float, float, float] = (0.0, 0.0, 0.0),
              variant: str = 'A') -> bpy.types.Collection: ...

Modules in this package are never imported by ``build_scene.py`` until the
typology is promoted from "concept" to "shipped". Adding a stub here is
zero-risk for current renders.
"""
TYPOLOGIES = (
    'cob_bottle_lqv',           # #1 — existing La Quebrada Viva
    'rammed_earth_loft',        # #2 — 1-story SIREWALL, NW orientation
    'bamboo_pavilion',          # #3 — Guadua frame, palm thatch
    'shipping_container_eco',   # #4 — 2x40' HC, retrofitted, white roof
    'straw_bale_cottage',       # #5 — wheat straw walls, lime plaster
    'adobe_courtyard',          # #6 — adobe block, internal patio
    'timber_tree_cabin',        # #7 — elevated, lapacho posts
    'underground_dome',         # #8 — earthbag dome, partial berm
)
