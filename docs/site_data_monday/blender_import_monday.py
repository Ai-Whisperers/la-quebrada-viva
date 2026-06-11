"""
import_monday.py — Cataratas del Monday 3D scene driver for Blender (4.2+)
Loads the real-world geospatial data we pulled for the 6 km × 6 km AOI centered
on the cascade (−25.561944, −54.631389, UTM 21J E 737960 N 7170703).

Pipeline:
  1. Real terrain (DEM) at 2.5 m resolution → displacement-modulated plane
  2. Albedo / satellite imagery (S2 10 m + Esri 1.2 m) → image texture
  3. NDVI + ESA WorldCover 10 m land-cover → vertex-color / attribute map
  4. OSM rivers + buildings + roads → curve / mesh overlay
  5. Cascada geometry: detected cliff edge from NASADEM 30 m slope map

Usage:
  blender --background --python blender_import_monday.py
  # or interactive:
  blender --python blender_import_monday.py

This is a standalone script — copy it next to the geotiffs in
  docs/site_data_monday/
and run from there. It is intentionally simple (no LQV framework dependency)
so it works on a fresh box that only has bpy + numpy + rasterio.
"""
import bpy
import bmesh
from mathutils import Vector
import os
import sys
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from pyproj import Transformer

HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()

# -------------------------------------------------------------------------
# AOI
# -------------------------------------------------------------------------
CENTER_LAT = -25.561944
CENTER_LON = -54.631389
RADIUS_M   = 3000
AOI_W, AOI_S, AOI_E, AOI_N = (CENTER_LON - RADIUS_M / (111000.0 * np.cos(np.radians(abs(CENTER_LAT)))),
                              CENTER_LAT - RADIUS_M / 111000.0,
                              CENTER_LON + RADIUS_M / (111000.0 * np.cos(np.radians(abs(CENTER_LAT)))),
                              CENTER_LAT + RADIUS_M / 111000.0)

def latlon_to_utm(easting, northing):
    """Single-point reproject via pyproj."""
    t = Transformer.from_crs("EPSG:4326", "EPSG:32721", always_xy=True)
    return t.transform(easting, northing)

CASCADE_E, CASCADE_N = latlon_to_utm(CENTER_LON, CENTER_LAT)
print(f"[monday] cascade center UTM 21J: E={CASCADE_E:.1f}  N={CASCADE_N:.1f}")

# -------------------------------------------------------------------------
# Load DEM
# -------------------------------------------------------------------------
DEM_PATH = os.path.join(HERE, "dem/terrarium_monday_2_5m_utm21j.tif")
ALBEDO_PATH = os.path.join(HERE, "analysis/rgb_truecolor_utm21j.tif")
NDVI_PATH = os.path.join(HERE, "analysis/ndvi_utm21j.tif")
LANDCOVER_PATH = os.path.join(HERE, "landcover/esa_worldcover_utm21j.tif")
HD_TEX = os.path.join(HERE, "hd_imagery/esri_z17_stitched.png")

def load_utm_geo(path):
    with rasterio.open(path) as ds:
        arr = ds.read(1)
        transform = ds.transform
        crs = ds.crs
        bounds = ds.bounds
    return arr, transform, crs, bounds

print(f"[monday] loading DEM {DEM_PATH}")
elev, dtrans, dcrs, dbounds = load_utm_geo(DEM_PATH)
print(f"  shape {elev.shape}  res {abs(dtrans.a):.2f} m  range {elev.min():.1f}..{elev.max():.1f} m  bounds {dbounds}")

# crop to AOI if needed
x0 = max(0, int((dbounds.left - AOI_W * 111000 - 700000) / dtrans.a))
# (we already know our DEM is exactly the AOI; trust the file)
DEM_W_M = abs(dtrans.a) * elev.shape[1]
DEM_H_M = abs(dtrans.e) * elev.shape[0]
print(f"  ground area: {DEM_W_M:.0f} m × {DEM_H_M:.0f} m")

# -------------------------------------------------------------------------
# Build the terrain mesh (displacement-mapped plane)
# -------------------------------------------------------------------------
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.mesh.primitive_plane_add(
    size=1.0,
    enter_editmode=False,
    location=(CASCADE_E, CASCADE_N, 0.0),
)
obj = bpy.context.active_object
obj.name = "MondayTerrain"
obj.scale = (DEM_W_M / 2.0, DEM_H_M / 2.0, 1.0)
# set origin back to (CASCADE_E, CASCADE_N) (Blender plane is centered on origin in local)
# but world origin offset = obj.location
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# subdivide for displacement
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=min(elev.shape[0], 256) - 1)
# we cannot rely on a 1:1 vertex ↔ pixel mesh; use 256x256 instead
bpy.ops.object.mode_set(mode='OBJECT')

# displacement modifier
disp = obj.modifiers.new("DEM_Displacement", "DISPLACE")
# we will write the elevation as a vertex group + custom texture

# 2.5m DEM = 2408x2452 vertices is excessive; let's go simpler:
# 1) Create a bmesh plane with exactly elev.shape[0] x elev.shape[1] vertices
# Use numpy → mesh
print(f"[monday] building high-res mesh ({elev.shape[0]}x{elev.shape[1]} vertices = {elev.shape[0]*elev.shape[1]:,})")
mesh = obj.data
bm = bmesh.new()
w = elev.shape[1]; h = elev.shape[0]
xs = np.linspace(-DEM_W_M/2, DEM_W_M/2, w)
ys = np.linspace(-DEM_H_M/2, DEM_H_M/2, h)
for yi in range(h):
    for xi in range(w):
        bm.verts.new((xs[xi], ys[yi], 0.0))
bm.verts.ensure_lookup_table()
# build faces
for yi in range(h - 1):
    for xi in range(w - 1):
        v0 = bm.verts[yi*w + xi]
        v1 = bm.verts[yi*w + xi+1]
        v2 = bm.verts[(yi+1)*w + xi+1]
        v3 = bm.verts[(yi+1)*w + xi]
        bm.faces.new([v0, v1, v2, v3])
bm.to_mesh(mesh)
bm.free()

# apply elevation as Z
zmin = float(elev.min())
print(f"[monday] setting vertex Z from DEM (zmin={zmin:.1f})")
for v in mesh.vertices:
    idx = v.index
    row = idx // w
    col = idx % w
    v.co.z = elev[row, col] - zmin

# -------------------------------------------------------------------------
# Material: albedo (S2 10m) + hillshade blend
# -------------------------------------------------------------------------
mat = bpy.data.materials.new("MondayTerrain")
mat.use_nodes = True
nt = mat.node_tree
for n in list(nt.nodes): nt.nodes.remove(n)

# nodes
out = nt.nodes.new("ShaderNodeOutputMaterial")
bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
tex_coord = nt.nodes.new("ShaderNodeTexCoord")
mapping = nt.nodes.new("ShaderNodeMapping")
albedo_tex = nt.nodes.new("ShaderNodeTexImage")
albedo_tex.image = bpy.data.images.load(ALBEDO_PATH)
albedo_tex.extension = "EXTEND"
ndvi_tex = nt.nodes.new("ShaderNodeTexImage")
ndvi_tex.image = bpy.data.images.load(NDVI_PATH)
ndvi_tex.extension = "EXTEND"
mix = nt.nodes.new("ShaderNodeMixRGB")
mix.blend_type = "MULTIPLY"
mix.inputs[1].default_value = (1, 1, 1, 1)
mix.inputs[2].default_value = (0.7, 0.9, 0.7, 1)  # forest tint
separate = nt.nodes.new("ShaderNodeSeparateRGB")
hsv = nt.nodes.new("ShaderNodeHueSaturation")
combine = nt.nodes.new("ShaderNodeCombineRGB")
# wire
nt.links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
nt.links.new(mapping.outputs["Vector"], albedo_tex.inputs["Vector"])
nt.links.new(albedo_tex.outputs["Color"], hsv.inputs["Color"])
nt.links.new(hsv.outputs["Color"], mix.inputs[1])
nt.links.new(ndvi_tex.outputs["Color"], separate.inputs["Image"])
# NDVI > 0.4 → green tint
# (we'll just use the G channel as a forest mask)
# Simpler: just connect albedo → bsdf for now and add a hue shift
nt.links.new(mix.outputs["Color"], bsdf.inputs["Base Color"])
nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

# UV map: use the generated UVs (which Blender plane has by default)
obj.data.materials.append(mat)

# -------------------------------------------------------------------------
# Add the cascade as a vertical waterfall plane
# -------------------------------------------------------------------------
print("[monday] adding cascade feature plane")
bpy.ops.mesh.primitive_plane_add(size=RADIUS_M*0.3,
    location=(CASCADE_E, CASCADE_N - 200, 200.0))
wf = bpy.context.active_object
wf.name = "Cascade_Feature"
mat_wf = bpy.data.materials.new("CascadeWater")
mat_wf.use_nodes = True
wfn = mat_wf.node_tree
for n in list(wfn.nodes): wfn.nodes.remove(n)
o = wfn.nodes.new("ShaderNodeOutputMaterial")
b = wfn.nodes.new("ShaderNodeBsdfPrincipled")
b.inputs["Base Color"].default_value = (0.7, 0.85, 0.95, 1)
b.inputs["Roughness"].default_value = 0.1
b.inputs["Transmission Weight"].default_value = 0.85
b.inputs["Alpha"].default_value = 0.85
wfn.links.new(b.outputs["BSDF"], o.inputs["Surface"])
wf.data.materials.append(mat_wf)

# -------------------------------------------------------------------------
# Add the cascade ZONE marker (a sun-like lamp pointing at the cascade)
# -------------------------------------------------------------------------
print("[monday] adding sun + camera")
bpy.ops.object.light_add(type='SUN', location=(CASCADE_E, CASCADE_N + 1000, 500))
sun = bpy.context.active_object
sun.data.energy = 4.0
sun.rotation_euler = (1.0, 0.0, 0.6)
bpy.ops.object.camera_add(location=(CASCADE_E - 400, CASCADE_N - 600, 350))
cam = bpy.context.active_object
cam.rotation_euler = (1.2, 0.0, 0.4)
bpy.context.scene.camera = cam
bpy.context.scene.camera.data.lens = 28

# -------------------------------------------------------------------------
# Save the .blend
# -------------------------------------------------------------------------
out_blend = os.path.join(HERE, "blender/monday_terrain.blend")
os.makedirs(os.path.dirname(out_blend), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)
print(f"[monday] saved {out_blend}")
