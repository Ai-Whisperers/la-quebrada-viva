"""Stamp per-asset CC0 attribution stubs at LICENSES/<id>.txt.

Idempotent. Existing files are NOT overwritten — a stub once written is
considered authoritative (so a manual edit on a specific asset's license
metadata survives reruns).

Two passes:

    1. Manifest pass — iterate the full Poly Haven base + EXTRA slug lists
       (`HDRIS + EXTRA_HDRIS + TEXTURES + EXTRA_TEXTURES + MODELS +
       EXTRA_MODELS`) plus the ambientCG manifest.
    2. Disk pass — enumerate `assets/{hdris,models,textures}` on disk
       using the same slug derivation as `tools/check_licenses.py`. Any
       slug not yet stubbed is classified as ambientCG if present in the
       ACG manifest, else Poly Haven. This catches assets that landed in
       the tree via vendor scripts not in either manifest list.

Slug → URL alias map (`POLYHAVEN_SLUG_ALIASES`) handles a few legacy
project-internal slugs that diverge from Poly Haven's canonical slug
(e.g. `forest_ground_01` directory vs `forrest_ground_01` on PH).

Backed by:
    - LICENSES/CC0-1.0.txt (verbatim CC0 1.0 Universal legal code)
    - LICENSE_BUNDLE.md §7 (license-text mirror-status table)

Run:
    python3 scripts/stamp_license_stubs.py
"""
from __future__ import annotations

import importlib.util
import os
import re
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(PROJECT_ROOT, "scripts")
LICENSES_DIR = os.path.join(PROJECT_ROOT, "LICENSES")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")

HDRI_SUFFIX_RE = re.compile(r"_(?:[0-9]+k|[0-9]+K)$")

POLYHAVEN_SLUG_ALIASES: dict[str, str] = {
    # Poly Haven shipped these with a double-r typo in 2019-2021; the
    # project mirror was checked in under the corrected spelling.
    "forest_ground_01": "forrest_ground_01",
    "forest_ground_03": "forrest_ground_03",
}


def _load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None, f'spec_from_file_location returned None for {path}'
    loader = spec.loader
    assert loader is not None, f'module spec for {name} has no loader'
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


PH_STUB = """\
Asset: {slug}
Source: Poly Haven (https://polyhaven.com/a/{slug})
License: CC0 1.0 Universal
License text: ./CC0-1.0.txt
License URL: https://creativecommons.org/publicdomain/zero/1.0/
Bundle source: Poly Haven blanket CC0 per https://polyhaven.com/license
Source URL: polyhaven.com
Downloaded: {date}
"""

ACG_STUB = """\
Asset: {slug}
Source: ambientCG (https://ambientcg.com/view?id={slug})
License: CC0 1.0 Universal
License text: ./CC0-1.0.txt
License URL: https://creativecommons.org/publicdomain/zero/1.0/
Bundle source: ambientCG blanket CC0 per https://docs.ambientcg.com/license
Source URL: ambientcg.com
Downloaded: {date}
"""


def _write(slug: str, template: str, url_slug: str | None = None) -> str:
    dest = os.path.join(LICENSES_DIR, f"{slug}.txt")
    if os.path.exists(dest):
        return "skip"
    os.makedirs(LICENSES_DIR, exist_ok=True)
    rendered = template.format(slug=url_slug or slug, date=time.strftime("%Y-%m-%d"))
    if url_slug and url_slug != slug:
        # Preserve project-internal slug in the Asset: header so the
        # stub is still discoverable by `tools/check_licenses.py`, which
        # matches by filename, not by the Source URL slug.
        rendered = rendered.replace(
            f"Asset: {url_slug}\n", f"Asset: {slug}\n", 1
        )
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(rendered)
    return "ok"


def _hdri_slug(name: str) -> str:
    base = os.path.splitext(name)[0]
    return HDRI_SUFFIX_RE.sub("", base)


def _is_vendor_wrapper(path: str) -> bool:
    try:
        entries = list(os.scandir(path))
    except OSError:
        return False
    if not entries:
        return False
    return all(e.is_dir() for e in entries)


def _disk_slugs() -> set[str]:
    """Enumerate asset slugs on disk using the same rules as
    `tools/check_licenses.py:_collect_asset_slugs` — including the
    `_unused*` HDRI recursion and the `_`-prefixed model/texture skip."""
    slugs: set[str] = set()

    hdris = os.path.join(ASSETS_DIR, "hdris")
    if os.path.isdir(hdris):
        for entry in os.listdir(hdris):
            full = os.path.join(hdris, entry)
            if os.path.isfile(full) and entry.lower().endswith((".exr", ".hdr")):
                slugs.add(_hdri_slug(entry))
            elif os.path.isdir(full) and entry.startswith("_unused"):
                for sub in os.listdir(full):
                    if sub.lower().endswith((".exr", ".hdr")):
                        slugs.add(_hdri_slug(sub))

    for kind in ("models", "textures"):
        root = os.path.join(ASSETS_DIR, kind)
        if not os.path.isdir(root):
            continue
        for entry in os.listdir(root):
            full = os.path.join(root, entry)
            if not os.path.isdir(full) or entry.startswith("_"):
                continue
            if _is_vendor_wrapper(full):
                for sub in os.listdir(full):
                    if os.path.isdir(os.path.join(full, sub)):
                        slugs.add(sub)
            else:
                slugs.add(entry)

    return slugs


def main() -> int:
    ph = _load_module(os.path.join(SCRIPTS, "download_polyhaven_assets.py"), "ph_dl")
    acg = _load_module(os.path.join(SCRIPTS, "download_ambientcg_assets.py"), "acg_dl")

    counts: dict[str, int] = {"ok": 0, "skip": 0}
    by_source: dict[str, dict[str, int]] = {
        "polyhaven": {"ok": 0, "skip": 0},
        "ambientcg": {"ok": 0, "skip": 0},
        "disk-ph": {"ok": 0, "skip": 0},
        "disk-acg": {"ok": 0, "skip": 0},
    }

    # Manifest stamping is gated on disk presence — listing a slug in
    # a download script does not, by itself, make it a redistributed
    # asset, so we never stamp a license stub for something the bundle
    # doesn't actually ship. (Otherwise `tools/check_licenses.py`
    # flags those stubs as orphans.)
    on_disk = _disk_slugs()

    ph_slugs = (
        ph.HDRIS + ph.EXTRA_HDRIS
        + ph.TEXTURES + ph.EXTRA_TEXTURES
        + ph.MODELS + ph.EXTRA_MODELS
    )
    for slug in ph_slugs:
        if slug not in on_disk:
            continue
        r = _write(slug, PH_STUB)
        counts[r] += 1
        by_source["polyhaven"][r] += 1

    for slug in acg.AMBIENT_CG:
        if slug not in on_disk:
            continue
        r = _write(slug, ACG_STUB)
        counts[r] += 1
        by_source["ambientcg"][r] += 1

    # Disk pass — pick up anything in assets/ that the manifests don't
    # name. Classification: ACG manifest wins, else assume Poly Haven.
    acg_set = set(acg.AMBIENT_CG)
    for slug in sorted(on_disk):
        stub_path = os.path.join(LICENSES_DIR, f"{slug}.txt")
        if os.path.exists(stub_path):
            continue
        if slug in acg_set:
            r = _write(slug, ACG_STUB)
            counts[r] += 1
            by_source["disk-acg"][r] += 1
        else:
            url_slug = POLYHAVEN_SLUG_ALIASES.get(slug)
            r = _write(slug, PH_STUB, url_slug=url_slug)
            counts[r] += 1
            by_source["disk-ph"][r] += 1

    print(
        f"[polyhaven] new={by_source['polyhaven']['ok']} "
        f"already-present={by_source['polyhaven']['skip']} "
        f"(scanned {len(ph_slugs)})"
    )
    print(
        f"[ambientcg] new={by_source['ambientcg']['ok']} "
        f"already-present={by_source['ambientcg']['skip']} "
        f"(scanned {len(acg.AMBIENT_CG)})"
    )
    print(
        f"[disk-ph]   new={by_source['disk-ph']['ok']} "
        f"(disk slugs not in PH manifest, classified Poly Haven)"
    )
    print(
        f"[disk-acg]  new={by_source['disk-acg']['ok']} "
        f"(disk slugs not in ACG manifest but matching ACG set)"
    )
    print(
        f"[total] new={counts['ok']} already-present={counts['skip']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
