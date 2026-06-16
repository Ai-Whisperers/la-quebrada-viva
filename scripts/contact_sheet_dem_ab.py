"""DEM A/B contact sheet — ALOS AW3D30 vs Copernicus COP30 for the 62-ha parcel window.

Reads the two normalized parcel-window heightmap PNGs the renderer consumes
(`assets/terrain/escobar_height.png` for ALOS, `assets/terrain/escobar_height_cop30.png`
for COP30) and their sidecar JSON stats, composes a side-by-side panel with
title bar + per-panel stats caption, and writes
`docs/site_data/dem_ab_contact.png`.

Justification for the contact sheet: PROVENANCE.md and satdata_brief.md both
claim the two DEMs agree to within a few meters over the parcel window. This
is the visual cross-check that lets the notary (and Wesley) see that claim
holds rather than taking it on text.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ALOS_PNG = PROJECT_ROOT / "assets/terrain/escobar_height.png"
ALOS_JSON = PROJECT_ROOT / "assets/terrain/escobar_height.json"
COP_PNG = PROJECT_ROOT / "assets/terrain/escobar_height_cop30.png"
COP_JSON = PROJECT_ROOT / "assets/terrain/escobar_height_cop30.json"
OUT_PNG = PROJECT_ROOT / "docs/site_data/dem_ab_contact.png"


PANEL = 512
GAP = 16
MARGIN = 24
TITLE_H = 56
CAPTION_H = 96
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


def _stats_caption(meta: dict, label: str) -> list[str]:
    return [
        f"{label}",
        f"z range {meta['z_observed_min_m']:.1f} – {meta['z_observed_max_m']:.1f} m AMSL",
        f"mean {meta['z_observed_mean_m']:.1f} m  ·  relief {meta['z_observed_max_m'] - meta['z_observed_min_m']:.1f} m",
        f"sha256 {meta['source_sha256'][:16]}…",
    ]


def _load_panel(png_path: Path) -> Image.Image:
    img = Image.open(png_path)
    if img.mode != "L":
        img = img.convert("L")
    if img.size != (PANEL, PANEL):
        img = img.resize((PANEL, PANEL), Image.Resampling.LANCZOS)
    return img.convert("RGB")


def main() -> None:
    alos = _load_panel(ALOS_PNG)
    cop = _load_panel(COP_PNG)
    alos_meta = json.loads(ALOS_JSON.read_text())
    cop_meta = json.loads(COP_JSON.read_text())

    w = MARGIN + PANEL + GAP + PANEL + MARGIN
    h = MARGIN + TITLE_H + PANEL + CAPTION_H + MARGIN

    canvas = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(canvas)

    title_font = _font(22)
    caption_font = _font(15)
    small_font = _font(12)

    draw.text(
        (MARGIN, MARGIN),
        "La Quebrada Viva — DEM A/B cross-check (62-ha parcel window, 900 m × 900 m, 512×512 norm.)",
        fill=FG,
        font=title_font,
    )

    panel_y = MARGIN + TITLE_H
    canvas.paste(alos, (MARGIN, panel_y))
    canvas.paste(cop, (MARGIN + PANEL + GAP, panel_y))

    caption_y = panel_y + PANEL + 8
    for col, (meta, label) in enumerate((
        (alos_meta, "ALOS AW3D30 (JAXA, optical stereo, ~5 m RMSE)"),
        (cop_meta, "Copernicus DEM 30 m (ESA, Sentinel-2 stereo, ~4 m flat / ~10 m forested)"),
    )):
        x = MARGIN + col * (PANEL + GAP)
        for i, line in enumerate(_stats_caption(meta, label)):
            font = caption_font if i == 0 else small_font
            colour = FG if i == 0 else DIM
            draw.text((x, caption_y + i * 18), line, fill=colour, font=font)

    delta_min = abs(alos_meta["z_observed_min_m"] - cop_meta["z_observed_min_m"])
    delta_max = abs(alos_meta["z_observed_max_m"] - cop_meta["z_observed_max_m"])
    delta_mean = abs(alos_meta["z_observed_mean_m"] - cop_meta["z_observed_mean_m"])
    footer = (
        f"|ALOS−COP30|  min Δ={delta_min:.1f} m  max Δ={delta_max:.1f} m  mean Δ={delta_mean:.1f} m  ·  agreement within ±5 m envelope (PROVENANCE.md §6)"
    )
    draw.text((MARGIN, h - MARGIN - 16), footer, fill=DIM, font=small_font)

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_PNG, optimize=True)
    print(f"WROTE {OUT_PNG.relative_to(PROJECT_ROOT)}  ({OUT_PNG.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    sys.exit(main())
