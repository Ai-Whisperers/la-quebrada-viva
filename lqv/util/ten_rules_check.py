"""Post-build audit for the 10 design rules (CLAUDE.md §48-58).

Run AFTER ``build_scene.py`` has finished, inside the same Blender session::

    from lqv.util import ten_rules_check
    violations = ten_rules_check.run()
    if violations:
        for v in violations: print(f"  - {v}")

Each check is best-effort: a rule the audit cannot verify from the scene
returns "skipped" rather than a false positive. The audit is read-only — it
never mutates objects, materials, or modifiers.
"""
from __future__ import annotations

import bpy


def _check_no_box_walls() -> list[str]:
    """Rule 1: no right angles in cob walls.

    Heuristic: any mesh whose name starts with "CobWall_" must have at least
    one subdivision-surface modifier OR a displacement modifier. A pure box
    has neither.
    """
    out: list[str] = []
    for obj in bpy.data.objects:
        if obj.type != 'MESH' or not obj.name.startswith('CobWall_'):
            continue
        mods = {m.type for m in obj.modifiers}
        if not ({'SUBSURF', 'DISPLACE', 'SUBDIVISION_SURFACE'} & mods):
            out.append(f"rule 1: {obj.name} has no subdiv/displace modifier")
    return out


def _check_no_cement_plaster() -> list[str]:
    """Rule 2: no cement plaster on cob; lime only.

    Heuristic: scan material names for 'cement' or 'concrete' substrings on
    any object whose name starts with CobWall_.
    """
    out: list[str] = []
    forbidden = ('cement', 'concrete')
    for obj in bpy.data.objects:
        if not obj.name.startswith('CobWall_'):
            continue
        for slot in obj.material_slots:
            if slot.material is None:
                continue
            mname = slot.material.name.lower()
            if any(f in mname for f in forbidden):
                out.append(f"rule 2: {obj.name} uses material {slot.material.name!r}")
    return out


def _check_no_standing_water() -> list[str]:
    """Rule 3: no standing water other than the mandated stream pool.

    Heuristic: any mesh whose name contains 'puddle', 'cistern_open', or
    'pond' is a violation.
    """
    out: list[str] = []
    forbidden = ('puddle', 'cistern_open', 'pond')
    for obj in bpy.data.objects:
        n = obj.name.lower()
        if any(f in n for f in forbidden):
            out.append(f"rule 3: {obj.name} suggests standing water")
    return out


def _check_walls_off_ground() -> list[str]:
    """Rule 4: earthen walls never touch ground; 60cm stone foundation."""
    out: list[str] = []
    for obj in bpy.data.objects:
        if obj.type != 'MESH' or not obj.name.startswith('CobWall_'):
            continue
        min_z = min((obj.matrix_world @ v.co).z for v in obj.data.vertices)
        if min_z < 0.55:
            out.append(f"rule 4: {obj.name} min_z={min_z:.2f}m (< 0.55m)")
    return out


def _check_solar_not_on_living_roof() -> list[str]:
    """Rule 9: solar must sit on a separate steel frame, never on the sod roof."""
    out: list[str] = []
    sod_roof = bpy.data.objects.get('SodRoof')
    if sod_roof is None:
        return ['rule 9: skipped — no SodRoof object']
    sod_max_z = max((sod_roof.matrix_world @ v.co).z for v in sod_roof.data.vertices)
    for obj in bpy.data.objects:
        if 'solar' not in obj.name.lower() and 'pv_' not in obj.name.lower():
            continue
        if obj.type == 'MESH':
            min_z = min((obj.matrix_world @ v.co).z for v in obj.data.vertices)
        else:
            min_z = obj.location.z
        if min_z < sod_max_z + 0.20:
            out.append(
                f"rule 9: {obj.name} min_z={min_z:.2f}m close to/below "
                f"SodRoof max_z={sod_max_z:.2f}m"
            )
    return out


CHECKS = (
    ('rule 1 (no box cob walls)', _check_no_box_walls),
    ('rule 2 (no cement plaster)', _check_no_cement_plaster),
    ('rule 3 (no standing water)', _check_no_standing_water),
    ('rule 4 (walls off ground)', _check_walls_off_ground),
    ('rule 9 (solar off sod roof)', _check_solar_not_on_living_roof),
)


def run(verbose: bool = True) -> list[str]:
    """Return real violations only. Skipped checks are printed but excluded
    from the returned list — per the module docstring, "skipped" means the
    audit could not verify the rule and must not be treated as a false
    positive (e.g., by CI gates)."""
    all_violations: list[str] = []
    for label, fn in CHECKS:
        try:
            v = fn()
        except Exception as exc:
            v = [f"{label}: check raised {exc!r}"]
        real = [line for line in v if 'skipped' not in line.lower()]
        if verbose:
            skipped = len(v) - len(real)
            tag = f"{len(real)} issue(s)"
            if skipped:
                tag += f", {skipped} skipped"
            print(f"[ten_rules_check] {label}: {tag}")
            for line in v:
                print(f"  - {line}")
        all_violations.extend(real)
    return all_violations
