#!/usr/bin/env python3
"""Build per-asset contact-sheet JPGs from `docs/render_catalogue/catalogue.json`.

Output: `docs/render_catalogue/contact_sheets/<asset>.jpg` (≤9 tiles, 480px wide
each, 3-column grid, labelled with variant + date). Requires ImageMagick
`montage` on PATH. Skips assets that already have an up-to-date sheet.

Selection policy per asset: latest-first by (date, mtime), capped at 9 tiles,
dedup by (variant, sub_variant) so the sheet shows breadth not duplicates.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CATALOGUE = REPO / "docs/render_catalogue/catalogue.json"
OUT_DIR = REPO / "docs/render_catalogue/contact_sheets"
TILE_W = 480
MAX_TILES = 9
SKIP_ASSETS = {"ESCRITURA_FINALS", "MONDAY_DELIVERABLE", "_PREVIEWS"}


def have_montage() -> bool:
    return shutil.which("montage") is not None


def pick_tiles(renders: list[dict]) -> list[dict]:
    """Pick up to MAX_TILES renders, latest-first, deduped by (variant, sub_variant)."""
    def sort_key(r: dict) -> tuple[str, str]:
        return (r.get("date") or "0000-00-00", r.get("mtime") or "0000-00-00")

    seen: set[tuple[str, str]] = set()
    out: list[dict] = []
    for r in sorted(renders, key=sort_key, reverse=True):
        key = (r.get("variant") or "", r.get("sub_variant") or "")
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
        if len(out) >= MAX_TILES:
            break
    return out


def label_for(r: dict) -> str:
    parts = []
    v = r.get("variant") or ""
    sv = r.get("sub_variant") or ""
    if v and sv:
        parts.append(f"{v}/{sv}")
    elif v:
        parts.append(v)
    elif sv:
        parts.append(sv)
    d = r.get("date") or r.get("mtime") or ""
    if d:
        parts.append(d)
    return "\n".join(parts) or "?"


def build_sheet(asset: str, renders: list[dict]) -> Path | None:
    tiles = pick_tiles(renders)
    if not tiles:
        return None
    out_path = OUT_DIR / f"{asset}.jpg"

    cmd: list[str] = ["montage"]
    for r in tiles:
        src = REPO / r["path"]
        if not src.exists():
            continue
        cmd += ["-label", label_for(r), str(src)]
    if "-label" not in cmd:
        return None

    cmd += [
        "-tile", "3x",
        "-geometry", f"{TILE_W}x{TILE_W}+8+8",
        "-background", "#0f1115",
        "-fill", "#e6e6e6",
        "-pointsize", "16",
        "-quality", "85",
        str(out_path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[fail] {asset}: {res.stderr.strip()[:200]}", file=sys.stderr)
        return None
    return out_path


def main() -> int:
    if not have_montage():
        print("montage not on PATH; install imagemagick", file=sys.stderr)
        return 2
    if not CATALOGUE.exists():
        print(f"catalogue not found: {CATALOGUE}", file=sys.stderr)
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = json.loads(CATALOGUE.read_text())
    assets: dict[str, list[dict]] = data.get("assets", {})

    built: list[str] = []
    for asset, renders in sorted(assets.items()):
        if asset in SKIP_ASSETS:
            continue
        if not renders:
            continue
        out = build_sheet(asset, renders)
        if out is not None:
            built.append(asset)

    print(f"built {len(built)} contact sheets in {OUT_DIR.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
