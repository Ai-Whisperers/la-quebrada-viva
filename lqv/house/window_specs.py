"""Window specifications — sizes, frame types, glazing.

Data-only module documenting every window opening on the LQV house. Current
cob builder bakes window shapes into the wall mesh + hidden ``WindowCut_*``
Boolean cutters; this module is the human-readable table of what those
cutters represent.

Status: dormant — referenced by ``docs/window_specs.md`` once it lands.
"""
from __future__ import annotations

# Each entry: (cutter_name, width_m, height_m, sill_height_m, glazing, frame_material)
WINDOWS = (
    ('WindowCut_KitchenN',   1.20, 0.90, 1.00, 'double_low_e', 'lapacho'),
    ('WindowCut_KitchenE',   0.80, 0.60, 1.30, 'single_clear', 'lapacho'),
    ('WindowCut_LivingS',    2.40, 1.60, 0.40, 'double_low_e', 'lapacho'),
    ('WindowCut_LivingW',    1.80, 1.20, 0.80, 'double_low_e', 'lapacho'),
    ('WindowCut_BedroomE',   1.40, 1.10, 0.90, 'double_low_e', 'lapacho'),
    ('WindowCut_BedroomS',   1.20, 1.00, 0.90, 'double_low_e', 'lapacho'),
    ('WindowCut_BathroomN',  0.60, 0.40, 1.70, 'frosted_single', 'lapacho'),
    ('WindowCut_BottleWestPanel', 2.00, 1.80, 0.55, 'recycled_bottle_ends', 'cob_embedded'),
)
TOTAL_GLAZING_AREA_M2 = round(sum(w * h for _, w, h, *_ in WINDOWS), 2)
NOTES = (
    'All lapacho frames are FSC or salvaged — Wesley to confirm supplier.',
    'Low-E coating on south + west glass to reduce summer heat gain.',
    'Bottle wall is technically not "glazed" — it is structural cob with bottle inserts.',
    'Bathroom window is the only frosted glass (privacy).',
)
