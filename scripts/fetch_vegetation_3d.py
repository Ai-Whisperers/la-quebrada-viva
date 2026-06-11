#!/usr/bin/env python3
"""
fetch_vegetation.py — batch-download CC-BY 3D models from Sketchfab Data API v3.

Targets the 6 species already in CREDITS.md + the lapacho gap (once chosen).

Setup:
    mkdir -p ~/.config/sketchfab
    echo "<paste token from https://sketchfab.com/settings/account>" > ~/.config/sketchfab/token
    chmod 600 ~/.config/sketchfab/token

Usage:
    python3 scripts/fetch_vegetation.py            # download all
    python3 scripts/fetch_vegetation.py --only lapacho
    python3 scripts/fetch_vegetation.py --dry-run
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path
import urllib.request
import urllib.error

API = "https://api.sketchfab.com/v3"

SHORTLIST: dict[str, dict] = {
    "pindo_palm": {
        "uid": "1fba8da266bc428ebfe8fe8a4f4df987",
        "author": "(verify on download)",
        "species": "Syagrus romanzoffiana",
    },
    "mango_5pack": {
        "uid": "6997814540f14929bf13cf3828b5dc90",
        "author": "Jagobo",
        "species": "Mangifera indica",
    },
    "tree_fern": {
        "uid": "c6bc31d122c043a19346c90f5cbde40e",
        "author": "b_nealie",
        "species": "Dicksonia / Cyathea",
    },
    "bamboo_guadua": {
        "uid": "3c13dc82ffb54d079a71fb8160d0cf90",
        "author": "local.yany",
        "species": "Guadua angustifolia",
    },
    "agave_americana": {
        "uid": "efe126efa459471c81cfc3132357b1b6",
        "author": "LucaDubs",
        "species": "Agave americana",
    },
    "anthurium_plowmanii": {
        "uid": "e6a92c1ddb8941e9b8aa92dc1f0f3c18",
        "author": "Lassi Kaukonen",
        "species": "Anthurium plowmanii",
    },
    # ── lapacho gap: uncomment + fill once UID is picked ──
    # "lapacho": {
    #     "uid": "<TODO>",
    #     "author": "<TODO>",
    #     "species": "Handroanthus impetiginosus",
    # },
}


def http_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def get_metadata(uid):
    return http_json(f"{API}/models/{uid}")


def get_download_url(uid, token):
    data = http_json(
        f"{API}/models/{uid}/download",
        headers={"Authorization": f"Token {token}"},
    )
    for fmt in ("gltf", "usdz", "source"):
        if fmt in data:
            return data[fmt]["url"]
    raise RuntimeError(f"No download format for {uid}: {data}")


def download_to(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"  already have {dest}")
        return
    with urllib.request.urlopen(url, timeout=120) as r, open(dest, "wb") as f:
        while chunk := r.read(64 * 1024):
            f.write(chunk)
    print(f"  -> {dest}  ({dest.stat().st_size // 1024} KB)")


def write_attribution(uid, meta, dest_dir):
    lic = (meta.get("license") or {}).get("label", "Unknown")
    user = meta.get("user", {}).get("username", "unknown")
    display = meta.get("user", {}).get("displayName", user)
    title = meta.get("name", uid)
    url = f"https://sketchfab.com/3d-models/{uid}"
    cc_url = (meta.get("license") or {}).get("url", "")
    (dest_dir / "ATTRIBUTION.txt").write_text(
        f"Title: {title}\n"
        f"Author: {display} (@{user})\n"
        f"UID: {uid}\n"
        f"Source: {url}\n"
        f"License: {lic}\n"
        f"License URL: {cc_url}\n"
        f"Fetched: {time.strftime('%Y-%m-%d')}\n"
    )
    (dest_dir / "LICENSE.txt").write_text(
        f"This asset is licensed under {lic}.\n"
        f"Full text: {cc_url}\n"
        f"\nSee ATTRIBUTION.txt for author + source URL.\n"
    )
    print(f"  wrote ATTRIBUTION.txt + LICENSE.txt ({lic})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated keys to fetch (default: all)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", default="assets/sketchfab", help="output root")
    args = ap.parse_args()

    token = os.environ.get("SKETCHFAB_TOKEN", "").strip()
    if not token:
        token_path = Path.home() / ".config/sketchfab/token"
        if token_path.exists():
            token = token_path.read_text().strip()
    if not token:
        print(
            "error: set SKETCHFAB_TOKEN env or write to ~/.config/sketchfab/token",
            file=sys.stderr,
        )
        return 2

    keys = (
        [k.strip() for k in args.only.split(",") if k.strip()]
        if args.only
        else list(SHORTLIST)
    )
    missing = [k for k in keys if k not in SHORTLIST]
    if missing:
        print(f"error: unknown keys: {missing}", file=sys.stderr)
        return 2

    root = Path(args.root)
    rc = 0
    for key in keys:
        info = SHORTLIST[key]
        uid = info["uid"]
        print(f"[{key}] uid={uid} species={info['species']}")
        dest_dir = root / uid
        if args.dry_run:
            print(f"  would fetch to {dest_dir}")
            continue
        try:
            meta = get_metadata(uid)
            write_attribution(uid, meta, dest_dir)
            signed = get_download_url(uid, token)
            ext = "glb" if "glb" in signed.lower() or "gltf" in signed.lower() else "zip"
            download_to(signed, dest_dir / f"source.{ext}")
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code} {e.reason} — skipping", file=sys.stderr)
            rc = 1
        except Exception as e:
            print(f"  {type(e).__name__}: {e} — skipping", file=sys.stderr)
            rc = 1
        time.sleep(1)
    return rc


if __name__ == "__main__":
    sys.exit(main())
