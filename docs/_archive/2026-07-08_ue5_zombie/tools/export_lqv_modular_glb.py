"""
LQV house modular GLB export — splits the cob house into discrete parts
for in-game placement (walls, floor, roof, services).

Run via:
    blender --background --python tools/export_lqv_modular_glb.py -- --out-dir DIR

Output files:
    - lqv_house_cob_walls.glb         (cob + bottle walls)
    - lqv_house_foundation.glb        (raised stone perimeter)
    - lqv_house_tatakua.glb           (oven)
    - lqv_house_services.glb          (plumbing + electrical props)
    - lqv_house_windows.glb           (window cones)
    - lqv_house_yard_props.glb        (corredor props)
    - lqv_house_full.glb              (everything combined)
"""
from __future__ import annotations

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(_HERE)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def parse_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    return parser.parse_args(argv)


# Map of part name → list of object name substrings to include
PARTS = {
    "cob_walls": ["Cob", "CobWall", "CobMesh", "cob_wall"],
    "foundation": ["Foundation", "Stone", "Perimeter"],
    "tatakua": ["Tatakua", "Tatakuá", "Oven"],
    "services": ["Service", "Plumbing", "Pelton", "Pipe"],
    "windows": ["Window", "Cone", "Emission"],
    "yard_props": ["Corredor", "Yard", "Prop"],
    "bamboo_frame": ["Bamboo", "Wigwam", "Culm"],
}


def export_selection(args_list: list[str], filepath: str) -> None:
    import bpy
    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.context.scene.objects:
        if obj.type in {"MESH", "CURVE", "SURFACE"}:
            for needle in args_list:
                if needle.lower() in obj.name.lower():
                    obj.select_set(True)
                    break
    selected = [o for o in bpy.context.scene.objects if o.select_get()]
    if not selected:
        print(f"  ⚠ No objects matched for {filepath} — skipping")
        return
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_materials="EXPORT",
        export_normals=True,
        export_lights=False,
        export_cameras=False,
    )
    size_kb = os.path.getsize(filepath) / 1024
    print(f"  ✓ {os.path.basename(filepath)} ({size_kb:.0f} KB, {len(selected)} objects)")


def main():
    import bpy

    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    # Reset + build the scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    import random
    random.seed(42)
    from lqv.materials import build_materials
    build_materials()
    from lqv.house import build_cob_house, build_bottle_wall, build_tatakua, build_services
    from lqv.house import build_window_emission
    from lqv.site import build_ground

    print("[modular] Building ground + house components...")
    build_ground()
    build_cob_house()
    build_bottle_wall()
    build_tatakua()
    build_services()
    try:
        build_window_emission("A")
    except Exception:
        pass

    # Print all object names so we know what to match
    print("\n[modular] Object inventory:")
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            print(f"  - {obj.name}")

    # Export each part
    print(f"\n[modular] Exporting modular parts to {args.out_dir}")
    for part_name, needles in PARTS.items():
        out = os.path.join(args.out_dir, f"lqv_house_{part_name}.glb")
        export_selection(needles, out)

    # Also export the full thing
    bpy.ops.object.select_all(action="DESELECT")
    for obj in bpy.context.scene.objects:
        if obj.type in {"MESH", "CURVE", "SURFACE"}:
            obj.select_set(True)
    out_full = os.path.join(args.out_dir, "lqv_house_full.glb")
    bpy.ops.export_scene.gltf(
        filepath=out_full,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_materials="EXPORT",
        export_normals=True,
        export_lights=False,
        export_cameras=False,
    )
    size_mb = os.path.getsize(out_full) / 1024 / 1024
    print(f"  ✓ lqv_house_full.glb ({size_mb:.1f} MB)")

    print(f"\n✓ Done.")


if __name__ == "__main__":
    main()