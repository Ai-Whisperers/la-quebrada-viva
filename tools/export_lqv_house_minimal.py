"""
LQV house minimal scene builder — for UE5.7 GLB export, no GPU required.

build_scene.py sets up Cycles (which refuses to run without GPU). For GLB
export we only need the geometry + materials, no render engine. This script
calls the same lqv/house/* modules but skips Cycles/render setup.

Run via:
    blender --background --python tools/export_lqv_house_minimal.py -- --out-dir DIR
"""
from __future__ import annotations

import argparse
import os
import random
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
    parser.add_argument("--variant", default="A")
    return parser.parse_args(argv)


def main():
    import bpy

    # Reset scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    random.seed(42)  # deterministic

    # Materials first (build_materials needs empty bpy.data)
    from lqv.materials import build_materials
    build_materials()

    # Import the lqv package path so submodules resolve
    if REPO_ROOT not in sys.path:
        sys.path.insert(0, REPO_ROOT)

    # Build the cob house + sub-elements
    from lqv.house import build_cob_house, build_bottle_wall, build_tatakua, build_services
    from lqv.site import build_ground
    from lqv import materials as lqv_mats

    print("[minimal] Building ground...")
    build_ground()

    print("[minimal] Building cob house...")
    build_cob_house()

    print("[minimal] Building bottle wall...")
    build_bottle_wall()

    print("[minimal] Building tatakua...")
    build_tatakua()

    print("[minimal] Building services...")
    build_services()

    # Don't build escarpment (it's a procedural mesh for the cliff face — not
    # a discrete asset, the terrain itself is the escarpment in UE).

    args = parse_args()
    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)

    # Select all mesh + curve objects
    bpy.ops.object.select_all(action="DESELECT")
    targets = []
    for obj in bpy.context.scene.objects:
        if obj.type in {"MESH", "CURVE", "SURFACE"}:
            targets.append(obj)
            obj.select_set(True)

    print(f"\n[minimal] Exporting {len(targets)} objects → {out_dir}")
    out_full = os.path.join(out_dir, f"riverstone_cob_house.glb")
    bpy.ops.export_scene.gltf(
        filepath=out_full,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_materials="EXPORT",
        export_normals=True,
        export_morph=False,
        export_animations=False,

        export_lights=False,
        export_cameras=False,
    )
    print(f"  ✓ Wrote {out_full} ({os.path.getsize(out_full) / 1024:.1f} KB)")

    # Export just the cob walls + tatakua (the "house itself" without the
    # ground/terrain — useful for placing on top of the UE5 terrain)
    house_names = ["Cob", "Bottle", "Tatakua", "Foundation", "Stone"]
    bpy.ops.object.select_all(action="DESELECT")
    house_objs = [o for o in targets if any(name in o.name for name in house_names)]
    for o in house_objs:
        o.select_set(True)
    if house_objs:
        out_house = os.path.join(out_dir, "riverstone_house_only.glb")
        bpy.ops.export_scene.gltf(
            filepath=out_house,
            export_format="GLB",
            use_selection=True,
            export_apply=True,
            export_yup=True,
            export_materials="EXPORT",
            export_normals=True,
            export_morph=False,
            export_animations=False,
    
            export_lights=False,
            export_cameras=False,
        )
        print(f"  ✓ Wrote {out_house} ({os.path.getsize(out_house) / 1024:.1f} KB, {len(house_objs)} objects)")

    print(f"\n✓ Done. GLB files in {out_dir}")


if __name__ == "__main__":
    main()