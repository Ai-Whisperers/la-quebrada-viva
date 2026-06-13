"""Concept-model stubs for the 13 housing-park typologies.

Per ``docs/TERRAIN_PIVOT.md`` §3 the 62-ha site holds thirteen distinct
example buildings — Wesley's revised vocabulary supersedes the earlier
8-typology HOUSING_PARK_CONCEPT list. La Quebrada Viva (the cob/bottle
reference) is rendered as a sub-render driver under
``lqv.subscene.cob_bottle_lqv`` rather than a buildable typology — it
predates the typologies package and ships from ``build_scene.py``
directly, so it is intentionally absent from ``TYPOLOGIES``.

The other 13 are creek-/river-/hill-side units in three material families:
italian stone, container, bamboo (with two hybrid bamboo+beton lines).

Each builder follows the same shape::

    def build(parent: bpy.types.Collection | None = None,
              location: tuple[float, float, float] = (0.0, 0.0, 0.0),
              variant: str = 'A') -> bpy.types.Collection: ...

Modules in this package are never imported by ``build_scene.py`` until the
typology is promoted from "concept" to "shipped". Adding a stub here is
zero-risk for current renders. The :data:`TYPOLOGIES` tuple is a contract:
every name must resolve as ``lqv.typologies.<name>`` — see
``tests/test_typology_contract.py``.
"""
TYPOLOGIES = (
    'hobbit_house',                         # §3.1 sod-dome earthen, cut into hill
    'italian_stone_small_v1',               # §3.2 ~20 m², terracotta-gabled
    'italian_stone_small_v2',               # §3.3 ~30 m², porch + pergola
    'italian_river_house_4pax',             # §3.4 2-story stone, ~126 m² total
    'container_river_house',                # §3.5 2x40HC, stilts + cantilever
    'bamboo_river_house',                   # §3.6 stilted, woven culm walls
    'bamboo_container_4pax',                # §3.7 single 40HC + bamboo skin
    'bamboo_wigwam_lodge',                  # §3.8 tied-bamboo cone lodge
    'bamboo_boomhut_treehouse',             # §3.9 elevated treehouse, 3 m up
    'bamboo_beton_30',                      # §3.10 hybrid 30 m² couple
    'bamboo_beton_28',                      # §3.11 hybrid 28 m² solo + porch
    'bamboo_beton_family_curved',           # §3.12 ~70 m² family, curved roof
    'bamboo_beton_family_rectangular',      # §3.13 ~70 m² family, gabled roof
)
