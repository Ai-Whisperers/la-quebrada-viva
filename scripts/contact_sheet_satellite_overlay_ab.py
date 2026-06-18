"""Satellite-overlay A/B/C contact sheet — 3-panel single-row composite.

Companion to ``scripts/contact_sheet_dem_ab_oblique.py``: that one
proves the four DEM choices agree on the same procedural PBR base; this
one holds the DEM fixed (canonical ALOS) and swaps the satellite-derived
albedo overlay across three strategies produced by
``scripts/render_satellite_overlay_ab.py``:

  - bare   : procedural PBR only, no satellite multiply
  - s2rgb  : Sentinel-2 L2A surface reflectance RGB × 0.55 MULTIPLY
  - ndvi   : NDVI false-color (green = dense canopy) × 0.55 MULTIPLY

Reads:

  renders/sub/runs/satellite_overlay_ab_20260618_terrain_62ha_photoreal_oblique_bare/A.png
  renders/sub/runs/satellite_overlay_ab_20260618_terrain_62ha_photoreal_oblique_s2rgb/A.png
  renders/sub/runs/satellite_overlay_ab_20260618_terrain_62ha_photoreal_oblique_ndvi/A.png

Writes:

  docs/site_data/satellite_overlay_ab_contact.png
  docs/site_data/satellite_overlay_ab_contact.png.meta.json

Justification: PROVENANCE.md §3 cites the Sentinel-2 tile but until now
had no visual artifact tying the citation to the rendered scene. This
sheet is that artifact — a notary can read it as "same DEM, same camera,
same lighting; the only knob turned is the satellite-derived colour."
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.satellite._meta import write_sidecar  # noqa: E402

TERRAIN_DIR = PROJECT_ROOT / "assets/terrain"
RUNS_DIR = PROJECT_ROOT / "renders/sub/runs"
OUT_PNG = PROJECT_ROOT / "docs/site_data/satellite_overlay_ab_contact.png"

RENDER_RUN_ID = "satellite_overlay_ab_20260618"
RENDER_VARIANT = "A"
SENTINEL2_TILE = "S2B_21JVM_20260512_0_L2A"

PANELS: list[tuple[str, str, str]] = [
    ("Bare PBR", "no satellite overlay (procedural base only)", "bare"),
    ("Sentinel-2 RGB", f"{SENTINEL2_TILE} surface reflectance, ×0.55 MULTIPLY", "s2rgb"),
    ("NDVI false-colour", "(NIR-Red)/(NIR+Red), green = dense canopy, ×0.55 MULTIPLY", "ndvi"),
]

PANEL_W = 512
PANEL_H = 288  # preserve 16:9 from preview render (1280x720 → /2.5)
GAP = 16
MARGIN = 24
TITLE_H = 56
CAPTION_H = 88
FOOTER_H = 28
BG = (245, 245, 245)
FG = (20, 20, 20)
DIM = (90, 90, 90)


def _font(size: int) -> Any:
    for cand in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
    ):
        if os.path.exists(cand):
            return ImageFont.truetype(cand, size=size)
    return ImageFont.load_default()


def _stats_caption(meta: dict, label: str, sub: str, overlay: str) -> list[str]:
    return [
        label,
        sub,
        f"DEM = ALOS AW3D30  ·  z {meta['z_observed_min_m']:.1f} – {meta['z_observed_max_m']:.1f} m AMSL  ·  relief {meta['z_observed_max_m'] - meta['z_observed_min_m']:.1f} m",
        f"overlay = {overlay}  ·  dem sha256 {meta['source_sha256'][:16]}…",
    ]


def _render_path(name: str) -> Path:
    return (RUNS_DIR
            / f"{RENDER_RUN_ID}_terrain_62ha_photoreal_oblique_{name}"
            / f"{RENDER_VARIANT}.png")


def _load_panel(png_path: Path) -> Image.Image:
    img = Image.open(png_path).convert("RGB")
    if img.size != (PANEL_W, PANEL_H):
        img = img.resize((PANEL_W, PANEL_H), Image.Resampling.LANCZOS)
    return img


def main() -> int:
    dem_sidecar = TERRAIN_DIR / "escobar_height.json"
    if not dem_sidecar.exists():
        print(f"missing canonical DEM sidecar: {dem_sidecar.relative_to(PROJECT_ROOT)}",
              file=sys.stderr)
        return 2
    dem_meta = json.loads(dem_sidecar.read_text())

    panels: list[tuple[str, str, str, Image.Image]] = []
    for label, sub, name in PANELS:
        png = _render_path(name)
        if not png.exists():
            print(f"SKIP {label}: missing render {png.relative_to(PROJECT_ROOT)}",
                  file=sys.stderr)
            continue
        panels.append((label, sub, name, _load_panel(png)))

    if len(panels) < 2:
        print("not enough panels to compose contact sheet", file=sys.stderr)
        return 1

    cols = len(panels)
    rows = 1
    w = MARGIN + cols * PANEL_W + (cols - 1) * GAP + MARGIN
    h = MARGIN + TITLE_H + rows * (PANEL_H + CAPTION_H) + FOOTER_H + MARGIN

    canvas = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(canvas)

    title_font = _font(20)
    caption_font = _font(14)
    sub_font = _font(11)
    small_font = _font(11)

    draw.text(
        (MARGIN, MARGIN),
        "La Quebrada Viva — satellite-overlay A/B/C (oblique render, 62-ha parcel, ALOS DEM held fixed)",
        fill=FG,
        font=title_font,
    )

    for i, (label, sub, name, img) in enumerate(panels):
        px = MARGIN + i * (PANEL_W + GAP)
        py = MARGIN + TITLE_H
        canvas.paste(img, (px, py))
        lines = _stats_caption(dem_meta, label, sub, name)
        for j, line in enumerate(lines):
            if j == 0:
                font = caption_font
                colour = FG
            elif j == 1:
                font = sub_font
                colour = DIM
            else:
                font = small_font
                colour = DIM
            draw.text((px, py + PANEL_H + 6 + j * 16), line, fill=colour, font=font)

    overlay_modes = ",".join(name for _, _, name, _ in panels)
    footer = (
        f"oblique render @ preview 1280×720, Cycles CPU 32 samples  ·  "
        f"DEM constant (ALOS AW3D30), only albedo varies  ·  "
        f"overlays: {overlay_modes}  ·  run_id={RENDER_RUN_ID}"
    )
    draw.text((MARGIN, h - MARGIN - 14), footer, fill=DIM, font=small_font)

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_PNG, optimize=True)

    sidecar = write_sidecar(
        OUT_PNG,
        source="docs/site_data/sentinel2/" + SENTINEL2_TILE,
        collection="sentinel-2-l2a",
        license_id="CC-BY-4.0",
        citation="Contains modified Copernicus Sentinel data 2026 (S2B 21JVM 2026-05-12)",
        fetcher="scripts.contact_sheet_satellite_overlay_ab",
        extra={
            "render_run_id": RENDER_RUN_ID,
            "overlay_modes": [name for _, _, name, _ in panels],
            "sentinel2_tile": SENTINEL2_TILE,
            "dem_source_sha256": dem_meta["source_sha256"],
            "dem_source": dem_meta["source"],
            "render_config": {
                "engine": "cycles_cpu",
                "samples": 32,
                "resolution": [1280, 720],
                "camera_view": "oblique",
                "albedo_fac": 0.55,
            },
        },
    )

    print(f"WROTE {OUT_PNG.relative_to(PROJECT_ROOT)}  "
          f"({OUT_PNG.stat().st_size // 1024} KB)  {len(panels)} panel(s)")
    print(f"WROTE {sidecar.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
