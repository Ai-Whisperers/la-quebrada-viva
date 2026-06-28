"""DEM cross-check contact sheet — 4-panel grid of ALOS / COP30 / SRTM / NASADEM.

Reads the four normalized parcel-window heightmap PNGs that the renderer can
consume via the `LQV_DEM_OVERRIDE_*` env hooks in
`lqv/subscene/terrain_62ha_photoreal.py`:

  assets/terrain/escobar_height.png          ALOS AW3D30 (canonical)
  assets/terrain/escobar_height_cop30.png    Copernicus DEM GLO-30
  assets/terrain/escobar_height_srtm.png     SRTM v3 GL1
  assets/terrain/escobar_height_nasadem.png  NASADEM

Composes a 2x2 panel with title bar, per-panel stats caption, and footer
reporting the worst-case pairwise |Δ| across the four DEMs. Writes
`docs/site_data/dem_ab_contact.png` (path kept for back-compat — `_ab` is
historical from the original 2-panel ALOS/COP30 version).

Justification: PROVENANCE.md and `docs/site_data/DATA_INVENTORY.md` §2 claim
the four 30 m DEMs agree within a ~5 m envelope over the parcel window. This
sheet is the visual cross-check that lets the notary (and Wesley) see that
claim holds rather than taking it on text, and surfaces any outlier DEM
before A/B-rendering with the env override.
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
OUT_PNG = PROJECT_ROOT / "docs/site_data/dem_ab_contact.png"

PANELS: list[tuple[str, str, Path, Path]] = [
    ("ALOS AW3D30", "JAXA optical stereo, ~5 m RMSE — canonical",
     TERRAIN_DIR / "escobar_height.png",
     TERRAIN_DIR / "escobar_height.json"),
    ("Copernicus GLO-30", "ESA, TanDEM-X radar, ~4 m flat / ~10 m forested",
     TERRAIN_DIR / "escobar_height_cop30.png",
     TERRAIN_DIR / "escobar_height_cop30.json"),
    ("SRTM v3 GL1", "NASA/USGS C-band SAR (2000), ~9 m vertical",
     TERRAIN_DIR / "escobar_height_srtm.png",
     TERRAIN_DIR / "escobar_height_srtm.json"),
    ("NASADEM", "SRTM v3 reprocessed with ASTER GDEM + ICESat fill",
     TERRAIN_DIR / "escobar_height_nasadem.png",
     TERRAIN_DIR / "escobar_height_nasadem.json"),
]

PANEL = 384
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


def _load_panel(png_path: Path) -> Image.Image:
    img = Image.open(png_path)
    if img.mode != "L":
        img = img.convert("L")
    if img.size != (PANEL, PANEL):
        img = img.resize((PANEL, PANEL), Image.Resampling.LANCZOS)
    return img.convert("RGB")


def main() -> None:
    panels: list[tuple[str, str, Image.Image, dict]] = []
    for label, sub, png, jsn in PANELS:
        if not png.exists() or not jsn.exists():
            print(f"SKIP {label}: missing {png.name if not png.exists() else jsn.name}",
                  file=sys.stderr)
            continue
        panels.append((label, sub, _load_panel(png), json.loads(jsn.read_text())))

    if len(panels) < 2:
        print("not enough panels to compose contact sheet", file=sys.stderr)
        sys.exit(1)

    cols = 2
    rows = (len(panels) + cols - 1) // cols
    w = MARGIN + cols * PANEL + (cols - 1) * GAP + MARGIN
    h = MARGIN + TITLE_H + rows * (PANEL + CAPTION_H) + (rows - 1) * GAP + FOOTER_H + MARGIN

    canvas = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(canvas)

    title_font = _font(20)
    caption_font = _font(14)
    sub_font = _font(11)
    small_font = _font(11)

    draw.text(
        (MARGIN, MARGIN),
        "La Quebrada Viva — DEM cross-check (62-ha parcel window, 900 m × 900 m, 512×512 norm.)",
        fill=FG,
        font=title_font,
    )

    for i, (label, sub, img, meta) in enumerate(panels):
        r, c = divmod(i, cols)
        px = MARGIN + c * (PANEL + GAP)
        py = MARGIN + TITLE_H + r * (PANEL + CAPTION_H + GAP)
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
            draw.text((px, py + PANEL + 6 + j * 16), line, fill=colour, font=font)

    worst_min = 0.0
    worst_max = 0.0
    worst_mean = 0.0
    worst_pair = ("", "")
    for (la, _, _, ma), (lb, _, _, mb) in combinations(panels, 2):
        dmin = abs(ma["z_observed_min_m"] - mb["z_observed_min_m"])
        dmax = abs(ma["z_observed_max_m"] - mb["z_observed_max_m"])
        dmean = abs(ma["z_observed_mean_m"] - mb["z_observed_mean_m"])
        if dmax > worst_max:
            worst_min, worst_max, worst_mean = dmin, dmax, dmean
            worst_pair = (la, lb)

    footer = (
        f"worst pairwise |Δ| ({worst_pair[0]} vs {worst_pair[1]}):  "
        f"min Δ={worst_min:.1f} m  max Δ={worst_max:.1f} m  mean Δ={worst_mean:.1f} m  "
        f"·  see PROVENANCE.md §6 + DATA_INVENTORY.md §2"
    )
    draw.text((MARGIN, h - MARGIN - 14), footer, fill=DIM, font=small_font)

    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_PNG, optimize=True)
    print(f"WROTE {OUT_PNG.relative_to(PROJECT_ROOT)}  ({OUT_PNG.stat().st_size // 1024} KB)  "
          f"{len(panels)} panel(s)")


if __name__ == "__main__":
    sys.exit(main())
