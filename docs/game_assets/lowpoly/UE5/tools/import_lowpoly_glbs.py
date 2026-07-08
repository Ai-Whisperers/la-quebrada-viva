"""LQV 3D World — UE5.7 GLB import script.

Run inside UE5.7 editor (Content Browser → right-click → Run Python Script):
  tools/import_lowpoly_glbs.py

Imports every .glb in Content/Imported/ as a Static Mesh under Content/Imported/.

After import, run:
  tools/build_lqv_3dworld_level.py

Both scripts are designed to run on first project open.
"""

import os
import unreal

CONTENT_DIR = "/Game/Imported/"
IMPORT_DIR = os.path.join(
    unreal.Paths.project_content_dir(),
    "Imported"
)

# Discover all GLBs
glb_files = sorted(f for f in os.listdir(IMPORT_DIR) if f.endswith(".glb"))
unreal.log(f"Found {len(glb_files)} GLB files to import")

# Asset import tasks config
task = unreal.AssetImportTask()
task.replace_existing = True
task.automated = True
task.save = True

for filename in glb_files:
    src = os.path.join(IMPORT_DIR, filename)
    dst_name = filename.replace(".glb", "")  # LQV_Terrain, LQV_HouseCob, etc.
    task.filename = src
    task.destination_path = CONTENT_DIR
    task.destination_name = dst_name
    # GLB options
    options = unreal.FbxImportUI()
    options.import_mesh = True
    options.import_textures = False  # materials embedded in GLB
    options.import_materials = True
    options.import_as_skeletal = False
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
    options.static_mesh_import_data.combine_meshes = True
    options.static_mesh_import_data.generate_lightmap_u_vs = True
    options.static_mesh_import_data.auto_generate_collision = True
    task.options = options

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    unreal.log(f"  ✓ Imported {filename} → {CONTENT_DIR}{dst_name}")

unreal.EditorAssetLibrary.save_directory(CONTENT_DIR, only_if_is_dirty=True)
unreal.log("=== Import complete ===")
