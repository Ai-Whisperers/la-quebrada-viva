#!/usr/bin/env bash
# Idempotent batch downloader for regenerable assets (Poly Haven CC0).
#
# HDRIs and PBR textures are excluded from git via .gitignore; this script
# re-fetches them on a fresh clone or after a manual delete. Skips any file
# that already exists with non-zero size.
#
# Sketchfab CC-BY models and Hyper3D generations go in assets/models/ and are
# tracked in git directly — they are NOT re-fetched here.
#
# Source IDs come from docs/asset_plan.md §C.1 and §C.2.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HDRI_DIR="$ROOT_DIR/assets/hdris"
TEX_DIR="$ROOT_DIR/assets/textures"

mkdir -p "$HDRI_DIR" "$TEX_DIR"

# --- HDRIs (asset_plan.md §C.1) -----------------------------------------------
# 4K EXR; bump to 8K for hero finals only via a separate manual pull.
HDRIS=(
  kiara_1_dawn
  misty_pines
  qwantani_dusk_2
)

fetch_hdri() {
  local id="$1"
  local dest="$HDRI_DIR/${id}_4k.exr"
  if [[ -s "$dest" ]]; then
    printf '[skip] %s (already %s bytes)\n' "$id" "$(stat -c%s "$dest")"
    return 0
  fi
  local url="https://dl.polyhaven.org/file/ph-assets/HDRIs/exr/4k/${id}_4k.exr"
  printf '[fetch] %s\n' "$url"
  curl --fail --location --silent --show-error --output "$dest" "$url"
  printf '[ok]   %s (%s bytes)\n' "$dest" "$(stat -c%s "$dest")"
}

# --- PBR textures (asset_plan.md §C.2) ---------------------------------------
# Poly Haven textures have multiple maps (Diffuse, Normal, Rough, Displacement).
# The public API at api.polyhaven.com/files/<id> returns a JSON tree:
#   { "<MapName>": { "4k": { "jpg": {"url": "...", "md5": "..."} } } }
# We pull the 4K JPG for each map we know how to use; png-only assets fall
# through to the png branch.

TEXTURES=(
  aerial_mud_1
  aerial_grass_rock
  dry_riverbed_rock
  clay_block_wall
  clay_plaster
  dark_wood
  wood_floor_deck
  tree_bark_03
  palm_tree_bark
  bark_platanus
)

fetch_texture() {
  local id="$1"
  local out_dir="$TEX_DIR/$id"
  mkdir -p "$out_dir"

  # Cache the JSON metadata; refresh only if missing.
  local meta="$out_dir/.files.json"
  if [[ ! -s "$meta" ]]; then
    printf '[meta] %s\n' "$id"
    curl --fail --location --silent --show-error \
      --output "$meta" "https://api.polyhaven.com/files/$id"
  fi

  # Extract 4K URLs (prefer jpg, fall back to png) for the maps Cycles needs.
  # Python is more portable than jq across Linux distros.
  python3 - "$meta" "$out_dir" "$id" <<'PY'
import json
import os
import sys
import urllib.request

meta_path, out_dir, asset_id = sys.argv[1], sys.argv[2], sys.argv[3]
with open(meta_path) as fh:
    meta = json.load(fh)

# Map names Poly Haven uses; pick what's actually present.
wanted = ['Diffuse', 'nor_gl', 'Rough', 'Displacement', 'AO']
for map_name in wanted:
    node = meta.get(map_name)
    if not node:
        continue
    res = node.get('4k')
    if not res:
        # some assets only have 2k — take whatever's largest available
        res = node.get('8k') or node.get('2k') or node.get('1k')
        if not res:
            continue
    for fmt in ('jpg', 'png', 'exr'):
        entry = res.get(fmt)
        if not entry:
            continue
        url = entry.get('url')
        if not url:
            continue
        ext = url.rsplit('.', 1)[-1]
        dest = os.path.join(out_dir, f'{asset_id}_{map_name}_4k.{ext}')
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            print(f'[skip] {os.path.basename(dest)}')
            break
        print(f'[fetch] {url}')
        urllib.request.urlretrieve(url, dest)
        print(f'[ok]   {dest} ({os.path.getsize(dest)} bytes)')
        break
PY
}

main() {
  for id in "${HDRIS[@]}"; do
    fetch_hdri "$id"
  done
  for id in "${TEXTURES[@]}"; do
    fetch_texture "$id"
  done
  printf '\nDONE.  hdris=%d  textures=%d\n' "${#HDRIS[@]}" "${#TEXTURES[@]}"
}

main "$@"
