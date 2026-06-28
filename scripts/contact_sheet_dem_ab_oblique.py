"""DEM cross-check oblique render contact sheet — 4-panel grid.

Companion to ``scripts/contact_sheet_dem_ab.py``: that one composes the
raw heightmap PNGs side-by-side; this one composes the actual rendered
oblique sub-renders produced by ``scripts/render_dem_ab.py`` so the
visual A/B/C/D check is on the displaced+lit mesh, not just the
heightmap encoding.

Reads:

  renders/sub/runs/dem_ab_20260618_terrain_62ha_photoreal_oblique_alos/A.png
  renders/sub/runs/dem_ab_20260618_terrain_62ha_photoreal_oblique_cop30/A.png
  renders/sub/runs/dem_ab_20260618_terrain_62ha_photoreal_oblique_srtm/A.png
  renders/sub/runs/dem_ab_20260618_terrain_62ha_photoreal_oblique_nasadem/A.png

Plus the sidecar JSON pairs under ``assets/terrain/`` for stats captions.
Writes ``docs/site_data/dem_ab_oblique_contact.png``.

Justification: the heightmap-PNG sheet proves the encodings agree; this
sheet proves that agreement survives the displace+SUBSURF stack and the
oblique camera framing — i.e. the DEM choice is visually invisible to a
notary inspecting the rendered parcel, which is what PROVENANCE.md §6
actually claims.
"""
from __future__ import annotations

import json
import os
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TERRAIN_DIR = PROJECT_ROOT / "assets/terrain"
RUNS_DIR = PROJECT_ROOT / "renders/sub/runs"
OUT_PNG = PROJECT_ROOT / "docs/site_data/dem_ab_oblique_contact.png"

RENDER_RUN_ID = "dem_ab_20260618"
RENDER_VARIANT = "A"

PANELS: list[tuple[str, str, str]] = [
    ("ALOS AW3D30", "JAXA optical stereo, ~5 m RMSE — canonical", "alos"),
    ("Copernicus GLO-30", "ESA, TanDEM-X radar, ~4 m flat / ~10 m forested", "cop30"),
    ("SRTM v3 GL1", "NASA/USGS C-band SAR (2000), ~9 m vertical", "srtm"),
    ("NASADEM", "SRTM v3 reprocessed with ASTER GDEM + ICESat fill", "nasadem"),
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


def _stats_caption(meta: dict, label: str, sub: str) -> list[str]:
    return [
        label,
        sub,
        f"z {meta['z_observed_min_m']:.1f} – {meta['z_observed_max_m']:.1f} m AMSL  ·  relief {meta['z_observed_max_m'] - meta['z_observed_min_m']:.1f} m",
        f"mean {meta['z_observed_mean_m']:.1f} m  ·  sha256 {meta['source_sha256'][:16]}…",
    ]


def _render_path(name: str) -> Path:
    return (RUNS_DIR
            / f"{RENDER_RUN_ID}_terrain_62ha_photoreal_oblique_{name}"
            / f"{RENDER_VARIANT}.png")


def _heightmap_json(name: str) -> Path:
    if name == "alos":
        return TERRAIN_DIR / "escobar_height.json"
    return TERRAIN_DIR / f"escobar_height_{name}.json"


def _load_panel(png_path: Path) -> Image.Image:
    img = Image.open(png_path).convert("RGB")
    if img.size != (PANEL_W, PANEL_H):
        img = img.resize((PANEL_W, PANEL_H), Image.Resampling.LANCZOS)
    return img


def main() -> int:
    panels: list[tuple[str, str, Image.Image, dict]] = []
    for label, sub, name in PANELS:
        png = _render_path(name)
        jsn = _heightmap_json(name)
        if not png.exists():
            print(f"SKIP {label}: missing render {png.relative_to(PROJECT_ROOT)}",
                  file=sys.stderr)
            continue
        if not jsn.exists():
            print(f"SKIP {label}: missing sidecar {jsn.relative_to(PROJECT_ROOT)}",
                  file=sys.stderr)
            continue
        panels.append((label, sub, _load_panel(png), json.loads(jsn.read_text())))

    if len(panels) < 2:
        print("not enough panels to compose contact sheet", file=sys.stderr)
        return 1

    cols = 2
    rows = (len(panels) + cols - 1) // cols
    w = MARGIN + cols * PANEL_W + (cols - 1) * GAP + MARGIN
    h = MARGIN + TITLE_H + rows * (PANEL_H + CAPTION_H) + (rows - 1) * GAP + FOOTER_H + MARGIN

    canvas = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(canvas)

    title_font = _font(20)
    caption_font = _font(14)
    sub_font = _font(11)
    small_font = _font(11)

    draw.text(
        (MARGIN, MARGIN),
        "La Quebrada Viva — DEM cross-check (oblique render, 62-ha parcel, displace + SUBSURF)",
        fill=FG,
        font=title_font,
    )

    for i, (label, sub, img, meta) in enumerate(panels):
        r, c = divmod(i, cols)
        px = MARGIN + c * (PANEL_W + GAP)
        py = MARGIN + TITLE_H + r * (PANEL_H + CAPTION_H + GAP)
        canvas.paste(img, (px, py))
        lines = _stats_caption(meta, label, sub)
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

    worst_max = 0.0
    worst_mean = 0.0
    worst_pair = ("", "")
    for (la, _, _, ma), (lb, _, _, mb) in combinations(panels, 2):
        dmax = abs(ma["z_observed_max_m"] - mb["z_observed_max_m"])
        dmean = abs(ma["z_observed_mean_m"] - mb["z_observed_mean_m"])
        if dmax > worst_max:
            worst_max, worst_mean = dmax, dmean
            worst_pair = (la, lb)

    footer = (
        f"oblique render @ preview 1280×720, Cycles CPU 32 samples  ·  "
        f"worst pairwise |Δ| ({worst_pair[0]} vs {worst_pair[1]}): "
        f"max Δ={worst_max:.1f} m, mean Δ={worst_mean:.1f} m  ·  "
        f"run_id={RENDER_RUN_ID}"
    )
    draw.text((MARGIN, h - MARGIN - 14), footer, fill=DIM, font=small_font)

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_PNG, optimize=True)
    print(f"WROTE {OUT_PNG.relative_to(PROJECT_ROOT)}  ({OUT_PNG.stat().st_size // 1024} KB)  "
          f"{len(panels)} panel(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
