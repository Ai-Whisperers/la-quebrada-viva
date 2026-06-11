# Blender Integration Plan — Digital Twin of the 62-ha Property

**Goal:** turn the on-disk remote-sensing stack into a Blender scene we can spin around, fly over, drop building pads into, and use as a working digital version of Wesley's parcel. Not photoreal — readable. Mountains/escarpment, stream, cascade, pool, canopy patches, sun direction, candidate platforms. One file we can hand back to the client to show "this is your land in 3D, this is where we are putting things, this is what you would see from each platform."

**Non-goals:** no photoreal vegetation, no per-tree placement, no replacement of the byte-locked 18 finals at `85e86aa`. The digital twin lives next to the hero scene, not inside it.

**Architecture choice:** the dormant `lqv/site/terrain_62ha.py` module stays staged for the post-escritura T2.6 wiring into the hero scene. For the digital twin we build a **sub-render driver** at `lqv/subscene/terrain_62ha.py` that produces its own preview renders without touching the hero composite. This follows the project's sub-render-first rule and keeps the renderer byte-identity safe.

---

## 1. What the digital twin needs to show

Ordered by client value:

1. **62-ha terrain block** — meshed from ALOS AW3D30, exaggeration adjustable, sized to the parcel bbox.
2. **The escarpment** — visible as the steep face on the east edge, since `>20°` slope class is concentrated there.
3. **Stream centerline** — derived from pysheds flow accumulation, threaded from headwaters (~380 m) down to outlet (~116 m).
4. **Cascade band** — the ~250–300 m elevation strip on the stream where the gradient is steepest (the rapids).
5. **Flat-rock pool** — marker near the 120–125 m point where the stream relaxes.
6. **Build envelope** — the 127–169 m flat zone shaded green, escarpment shaded red, in/out via the buildability raster.
7. **Candidate house platforms** — three or four markers in the flat zone for the typology pads.
8. **Sun direction** — ERA5-derived solar position for solstice + equinox, three lighting setups.
9. **Optional canopy patches** — a low-poly visual stand-in keyed to GEDI canopy-height bands, not real flora.

Everything above is doable from data already on disk.

---

## 2. Architecture: where this code lives

```
lqv/
├── site/
│   └── terrain_62ha.py             # DORMANT, T2.6 hero-scene wiring (UNCHANGED until post-escritura)
└── subscene/
    └── terrain_62ha.py             # NEW: digital-twin driver — what this plan adds
docs/site_data/
├── alos_aw3d30_dem.tif             # canonical heightmap source
├── analysis/
│   ├── alos_buildability.tif       # green/yellow/red overlay source
│   └── alos_slope.tif
└── sentinel2/.../TCI.tif           # true-colour ground texture (gitignored)
scripts/
└── make_terrain_heightmap.py       # NEW: GeoTIFF → 16-bit PNG + 32-bit EXR exporter
```

Two new files only: a heightmap exporter and a sub-render driver. The dormant `lqv/site/terrain_62ha.py` is **not** modified — it stays staged for the post-escritura wiring.

**Why this respects the byte-lock:** the digital twin driver runs as a standalone Blender invocation (`blender --background --python lqv/subscene/terrain_62ha.py`), writes to `renders/sub/terrain_62ha/`, and never imports `build_scene.py`. The 18 finals at `85e86aa` are untouched.

---

## 3. Heightmap export pipeline

A one-shot script `scripts/make_terrain_heightmap.py` that produces `assets/terrain/escobar_height.png` and `escobar_height.exr`. Both files are intermediate artifacts written into `assets/terrain/` (a new directory at repo root) so Blender can consume them. Gitignore the EXR (large, regenerable); keep the PNG committed for previews.

Pipeline:

```python
# scripts/make_terrain_heightmap.py
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from PIL import Image
import imageio

SRC = "docs/site_data/alos_aw3d30_dem.tif"
DST_DIR = "assets/terrain"

with rasterio.open(SRC) as src:
    z = src.read(1).astype(np.float32)

z_min, z_max = 116.0, 380.0        # canonical relief from §1 SITE_DIAGNOSTIC
z_norm = np.clip((z - z_min) / (z_max - z_min), 0.0, 1.0)

# 16-bit PNG — Blender displace modifier reads this directly
png = (z_norm * 65535).astype(np.uint16)
Image.fromarray(png, mode="I;16").save(f"{DST_DIR}/escobar_height.png")

# 32-bit EXR — full precision for the sub-render driver
imageio.imwrite(f"{DST_DIR}/escobar_height.exr", z_norm.astype(np.float32))

# Sidecar JSON — bbox, native res, z range, source SHA
import json, hashlib, os
sha = hashlib.sha256(open(SRC, "rb").read()).hexdigest()[:16]
with open(f"{DST_DIR}/escobar_height.json", "w") as f:
    json.dump({
        "source": SRC,
        "source_sha256_16": sha,
        "z_min_m": z_min,
        "z_max_m": z_max,
        "shape": list(z.shape),
        "epsg": 4326,           # ALOS native — leave as WGS84 for now
        "bbox": list(src.bounds),
    }, f, indent=2)
```

**Effort:** 30 min including a sanity-check render of the PNG.

**Why two formats:** PNG is the universally-supported displacement input. EXR is for the optional `Image Texture → Displace` shader-graph path which gives sub-pixel precision on the slope edges.

**Why we don't reproject to UTM 21S yet:** for a flyover/screenshot tool the WGS84 grid is fine — the bbox is small enough that the lat/lon distortion is invisible. UTM reproject becomes mandatory when we wire to the hero scene (T2.6), because then the X/Y axes must match the hand-crafted scene at y=20, y=−25.5 etc. For the digital twin, WGS84 with the script-set X/Y scale is enough.

---

## 4. Sub-render driver — `lqv/subscene/terrain_62ha.py`

This is the file that produces the digital-twin renders. Same shape as the existing 30+ drivers in `lqv/subscene/`, just bigger in scope.

```python
"""Sub-render: 62-ha digital-twin terrain with features.

Standalone preview of Wesley's parcel — mesh-displaced ALOS heightmap,
Sentinel-2 TCI ground texture, stream centerline, cascade band, pool
marker, build-envelope shading, candidate platforms, solar direction.

Does NOT touch the hero scene. Renders to renders/sub/terrain_62ha/.
"""
from __future__ import annotations

import json
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import bpy
from lqv.subscene import base

TERRAIN_DIR = os.path.join(_PROJECT_ROOT, "assets", "terrain")
SENTINEL_TCI = os.path.join(_PROJECT_ROOT, "docs", "site_data",
                            "sentinel2", "S2B_21JVM_20260512_0_L2A", "TCI.tif")

# Parcel size in Blender units. 62 ha ≈ 787 m × 787 m square equivalent.
# We render a 1000 m × 1000 m block so the escarpment edge is in frame.
WORLD_SIZE = 1000.0
SUBDIVISIONS = 256   # 1000m / 256 ≈ 4m per quad — readable, fast


def _build_terrain_block():
    """Plane → subdivide → displace via heightmap PNG."""
    with open(os.path.join(TERRAIN_DIR, "escobar_height.json")) as f:
        meta = json.load(f)
    z_range = meta["z_max_m"] - meta["z_min_m"]   # 264 m

    bpy.ops.mesh.primitive_plane_add(size=WORLD_SIZE, location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.name = "terrain_62ha"

    # Subdivide deterministically — NO random.* calls.
    mod = plane.modifiers.new("Subdivide", "SUBSURF")
    mod.subdivision_type = "SIMPLE"
    mod.levels = 0
    mod.render_levels = 0   # we drive subdivision via Multires-free path

    # Geometry nodes would be cleaner but the displace modifier is enough.
    sub = plane.modifiers.new("Sub", "SUBSURF")
    sub.subdivision_type = "SIMPLE"
    sub.levels = 6          # 2^6 = 64 subdivisions per side from a quad plane
    sub.render_levels = 8   # 256 subdivisions per side at render time

    img = bpy.data.images.load(os.path.join(TERRAIN_DIR, "escobar_height.png"))
    disp = plane.modifiers.new("Disp", "DISPLACE")
    tex = bpy.data.textures.new("HeightTex", type="IMAGE")
    tex.image = img
    disp.texture = tex
    disp.texture_coords = "UV"
    disp.strength = z_range / WORLD_SIZE * 2.0   # height : footprint ratio, no exaggeration
    disp.mid_level = 0.0
    return plane


def _build_ground_texture(plane):
    """Sentinel-2 TCI as albedo. Stand-in for a real ortho until Tier-1 drone."""
    if not os.path.exists(SENTINEL_TCI):
        return  # fall back to a neutral PBR ground material
    mat = bpy.data.materials.new("Terrain_TCI")
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    nodes.clear()
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    out = nodes.new("ShaderNodeOutputMaterial")
    tci = nodes.new("ShaderNodeTexImage")
    tci.image = bpy.data.images.load(SENTINEL_TCI)
    links.new(tci.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    plane.data.materials.append(mat)


def _build_stream_centerline():
    """Bezier curve from headwaters (~380m corner) to outlet (~116m corner).

    Derived offline by running pysheds on the conditioned DEM. For now we
    use a five-point hand-routed polyline that matches the cascade and
    pool elevations from SITE_DIAGNOSTIC.md.
    """
    pts = [
        (-0.40, 0.45, 0.55),   # headwaters, ~380m
        (-0.15, 0.20, 0.42),   # upper gully
        (0.05, -0.05, 0.30),   # CASCADE band, ~250-300m
        (0.20, -0.20, 0.18),   # pool, ~120-125m
        (0.35, -0.45, 0.08),   # outlet, ~116m
    ]
    pts = [(x * WORLD_SIZE / 2, y * WORLD_SIZE / 2, z * 264) for x, y, z in pts]
    # ... bpy curve creation, blue emission material, 1 m radius bevel


def _build_pool_marker():
    """Cyan emission disc at the flat-rock pool."""
    bpy.ops.mesh.primitive_cylinder_add(radius=8.0, depth=0.5,
                                        location=(100, -100, 22))
    # ... cyan emission material


def _build_platform_markers():
    """Three or four 20 m × 20 m platforms in the 127-169 m flat zone."""
    platforms = [
        (-150, -50, 28, "platform_A"),
        (50, 50, 32, "platform_B"),
        (200, 100, 30, "platform_C"),
    ]
    for x, y, z, name in platforms:
        bpy.ops.mesh.primitive_plane_add(size=20.0, location=(x, y, z))
        bpy.context.active_object.name = name
        # ... white emission edge, slight glow


def _build_sun(month: str = "dec"):
    """ERA5-aligned sun. Three presets: dec (peak summer), jun (winter), eq (equinox)."""
    elevations = {"dec": 78, "jun": 32, "eq": 55}
    azimuths = {"dec": 110, "jun": 30, "eq": 70}
    bpy.ops.object.light_add(type="SUN")
    sun = bpy.context.active_object
    sun.data.energy = 5.0
    # rotate via Euler from elev/az ...


def _build():
    plane = _build_terrain_block()
    _build_ground_texture(plane)
    _build_stream_centerline()
    _build_pool_marker()
    _build_platform_markers()
    _build_sun(month="dec")


if __name__ == "__main__":
    base.run(
        asset="terrain_62ha",
        build_fn=_build,
        camera_target=(0.0, 0.0, 50.0),
        camera_distance=800.0,
        camera_height=400.0,
        camera_lens=35.0,
    )
```

**Critical invariants — same rules as every other sub-render driver:**

- `base.setup()` handles engine + materials + per-asset SHA-256 RNG seed. Driver code never touches `random.seed()` itself.
- `_build()` runs after `setup()` returns. It must not import `build_scene` and must not call `random.*` — this is the sub-render-first contract from `feedback_sub_render_first`.
- Output goes to `renders/sub/terrain_62ha/` automatically via `base.run()`. The 18 final renders at `85e86aa` are untouched.

---

## 5. Texture stack — what goes on the ground

Three layered approaches, pick one per render:

| Mode | Source | Look | Use when |
|---|---|---|---|
| **TCI** | Sentinel-2 true-colour, draped on the displaced mesh | Photo-realistic from-above, vegetation greens visible | Marketing flyover; "this is the actual ground colour from 2026-05-12" |
| **Buildability** | `analysis/alos_buildability.tif` as a 4-class colour ramp | Green flat / yellow buildable / orange challenging / red steep | Decision-support; "this is where we can build" |
| **NDVI** | derived from B04+B08, viridis ramp | Cool→warm vegetation density | Brochure; "89.88% vegetated, here's the proof" |

All three drive only the Base Color of the same Principled BSDF — switching is one shader-node swap, not a re-displace. Effort to add a CLI flag (`--mode tci/build/ndvi`): 30 min.

---

## 6. Feature overlays — how the stream, escarpment, pool, platforms appear

- **Stream** → Bezier curve with 0.8 m bevel radius, blue (R=0.1 G=0.3 B=0.9) emission shader at strength 1.5. Reads on every angle.
- **Escarpment** → highlighted by a darker buildability class (red); no extra geometry needed.
- **Pool** → 8 m radius disc at the flat-rock elevation, cyan emission strength 2.0.
- **Candidate platforms** → 20×20 m flat squares at the platform elevation, white emission edge, labeled by Blender text objects (`text.bevel.depth = 0.1`).
- **Sun direction** → a Sun light with an Empty arrow child object pointing along the sun vector, visible in the bird's-eye render.

All geometry is deterministic — no scatter, no `random.*`, no flora. The flora driver (`lqv/scatter_lapacho_petals`) is **explicitly out of scope** per the no-touch invariant.

---

## 7. Camera setups — three views per render mode

| Camera | Target | Dist | Height | Lens | Use |
|---|---|---|---|---|---|
| **Bird's-eye** | (0, 0, 50) | 800 m | 400 m | 35 mm | Plan overview, all features visible |
| **Iso-NE** | (0, 0, 50) | 700 m | 250 m | 35 mm | Shows the escarpment in profile |
| **Hero-platform** | (200, 100, 30) | 60 m | 25 m | 28 mm | What you would see from candidate platform C |

The `base.run()` API takes one camera, so we either accept one render per CLI invocation (3 invocations × 3 modes = 9 PNGs) or extend `base.py` to accept a list. The single-render-per-invocation path is simpler and shippable today.

**Effort to ship a 3-camera × 3-mode matrix:** ~3 hours including a CLI flag for mode and a small shell script that iterates the 9 combinations. Each render is 128 samples at 1280×720 OIDN-denoised — same render settings as every other sub-render — and takes ~30s on the CPU laptop.

---

## 8. What this does NOT do (intentionally)

- **No real flora.** No scattered trees, no lapacho petals, no canopy mesh. Those live in the hero scene; the digital twin is for terrain readability, not photoreality.
- **No HDRI sky.** Constant grey emission world. Faster, more readable, easier to compare modes side-by-side.
- **No procedural scatter.** Everything is deterministic. RNG-free.
- **No Tier-1-surveyor data.** When the agrimensor delivers the `.dwg`/`.shp` parcel boundary, we add a 4th feature overlay (boundary polyline) — until then, the boundary is implied by the WORLD_SIZE square.
- **No replacement of the hero scene.** The dormant `lqv/site/terrain_62ha.py` stays dormant. T2.6 wiring (DEM into the hero composite, byte-shift acknowledged) is post-escritura.

---

## 9. Shipping order

| Step | Effort | Output | Risk |
|---|---|---|---|
| 1. `scripts/make_terrain_heightmap.py` | 30 min | `assets/terrain/escobar_height.{png,exr,json}` | none |
| 2. `lqv/subscene/terrain_62ha.py` skeleton, TCI mode, bird's-eye cam only | 2 h | one PNG at `renders/sub/terrain_62ha/` | none |
| 3. Stream/pool/platform feature overlays | 1 h | same PNG with annotations | none |
| 4. Buildability mode + NDVI mode | 1.5 h | 3 PNGs in 3 modes | none |
| 5. Iso-NE + hero-platform cameras, 3×3 matrix | 1 h | 9 PNGs | none |
| 6. Sun presets (dec/jun/eq) | 1 h | one chosen preset shipped per render; 2 extras held for sun-study brochure | none |
| 7. Optional: pysheds-derived stream centerline replacing the hand-routed polyline | 2 h | more accurate stream geometry | low — pysheds may struggle on the unconditioned DEM |

**Total core (steps 1–5):** ~6 hours of work, all in pure Python + Blender headless, all read-only against existing data, all sub-render-first compliant. Zero risk to `85e86aa` byte-identity.

Steps 6 and 7 are nice-to-have and can ship post-escritura if needed.

---

## 10. After this ships

What we will be able to do that we cannot do today:

1. **Hand Wesley a 3-up PNG** showing his parcel from above, in iso, and from a candidate platform — backed by Sentinel-2 true colour and ALOS terrain. Real "here's your digital land."
2. **Drop a building-pad mockup** into the digital twin: edit one of the platform coordinates, re-run the driver, see the new pad in context.
3. **Run a quick sun study** by switching the sun preset (dec/jun/eq) — three renders showing summer/winter/equinox shadow direction across the parcel.
4. **Defend the build envelope quantitatively** with the buildability-mode render side-by-side with the TCI render — same terrain, two stories.
5. **Validate the agrimensor's survey when it arrives** by overlaying the real parcel boundary on the digital twin — checks that we are reasoning about the right ~62 ha.
6. **Brief the notary visually** instead of with a flat hillshade PDF — much higher signal at the closing meeting.

This is the digital version of the property, sized for the conversation we actually need to have. Sub-render-first, byte-safe, no scope creep, ships in a working day.
