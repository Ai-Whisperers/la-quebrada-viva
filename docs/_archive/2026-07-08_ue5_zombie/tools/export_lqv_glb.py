"""
Headless Blender export script for UE5.7 — invoked by export_lqv_glb.sh.

Run via:
    blender --background --python build_scene.py --python export_lqv_glb.py -- \
            --out-dir /path/to/glb/dir --variant A

Builds the same LQV scene the Cycles renders use (via build_scene.py), then
exports the relevant objects as glTF 2.0 .glb files. Designed to be run AFTER
build_scene.py so all bpy.data is populated.
"""
from __future__ import annotations

import argparse
import os
import sys


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


def export_selection_as_glb(filepath: str) -> None:
    """Export the current selection (or all objects if nothing selected) as a single .glb."""
    import bpy  # only available inside Blender
    # If nothing selected, select all visible mesh objects
    if not any(o.select_get() for o in bpy.context.scene.objects):
        bpy.ops.object.select_all(action="DESELECT")
        for obj in bpy.context.scene.objects:
            if obj.type in {"MESH", "CURVE", "SURFACE"} and obj.visible_get():
                obj.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_materials="EXPORT",
        export_normals=True,
        export_morph=True,
        export_animations=False,
        export_draco_mesh_compression=False,  # UE5 doesn't need Draco
        export_lights=False,
        export_cameras=False,
    )
    print(f"  ✓ Wrote {filepath} ({os.path.getsize(filepath) / 1024:.1f} KB)")


def main():
    import bpy

    args = parse_args()
    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    variant = args.variant

    # Export full scene (all house + props + flora) as one big GLB
    print(f"\nExporting full LQV scene (variant={variant}) → {out_dir}")

    # Deselect everything first
    bpy.ops.object.select_all(action="DESELECT")

    # Select all mesh + curve objects (skip camera/lamp/empty)
    targets = []
    for obj in bpy.context.scene.objects:
        if obj.type in {"MESH", "CURVE", "SURFACE"}:
            targets.append(obj)
            obj.select_set(True)

    print(f"  Selected {len(targets)} objects for export")

    out_path = os.path.join(out_dir, f"riverstone_full_scene_{variant}.glb")
    export_selection_as_glb(out_path)

    # Also export the cob house alone (with all its dependent parts:
    # cob walls, bottle walls, tatakua, windows) — useful for placing
    # duplicate houses in the housing park. We'll do this by name match.
    house_names = ["Cob", "Bottle", "Tatakua", "Window", "Stone", "Foundation"]
    bpy.ops.object.select_all(action="DESELECT")
    house_objs = [o for o in targets if any(name in o.name for name in house_names)]
    for o in house_objs:
        o.select_set(True)
    if house_objs:
        out_house = os.path.join(out_dir, f"riverstone_cob_house_{variant}.glb")
        export_selection_as_glb(out_path)
        export_selection_as_glb(out_house)

    print(f"\n✓ Done. GLB files in {out_dir}")


if __name__ == "__main__":
    main()