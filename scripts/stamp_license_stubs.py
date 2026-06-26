"""Stamp per-asset CC0 attribution stubs at LICENSES/<id>.txt.

Idempotent. Existing files are NOT overwritten — a stub once written is
considered authoritative (so a manual edit on a specific asset's license
metadata survives reruns).

Covers:
    - Poly Haven EXTRA lists from scripts/download_polyhaven_assets.py
    - ambientCG manifest from scripts/download_ambientcg_assets.py

Backed by:
    - LICENSES/CC0-1.0.txt (verbatim CC0 1.0 Universal legal code)
    - LICENSE_BUNDLE.md §7 (license-text mirror-status table)

Run:
    python3 scripts/stamp_license_stubs.py
"""
from __future__ import annotations

import importlib.util
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(PROJECT_ROOT, "scripts")
LICENSES_DIR = os.path.join(PROJECT_ROOT, "LICENSES")


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


def _write(slug: str, template: str) -> str:
    dest = os.path.join(LICENSES_DIR, f"{slug}.txt")
    if os.path.exists(dest):
        return "skip"
    os.makedirs(LICENSES_DIR, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(template.format(slug=slug, date=time.strftime("%Y-%m-%d")))
    return "ok"


def main() -> int:
    ph = _load_module(os.path.join(SCRIPTS, "download_polyhaven_assets.py"), "ph_dl")
    acg = _load_module(os.path.join(SCRIPTS, "download_ambientcg_assets.py"), "acg_dl")

    counts: dict[str, int] = {"ok": 0, "skip": 0}
    by_source: dict[str, dict[str, int]] = {
        "polyhaven": {"ok": 0, "skip": 0},
        "ambientcg": {"ok": 0, "skip": 0},
    }

    ph_slugs = ph.EXTRA_HDRIS + ph.EXTRA_TEXTURES + ph.EXTRA_MODELS
    for slug in ph_slugs:
        r = _write(slug, PH_STUB)
        counts[r] += 1
        by_source["polyhaven"][r] += 1

    for slug in acg.AMBIENT_CG:
        r = _write(slug, ACG_STUB)
        counts[r] += 1
        by_source["ambientcg"][r] += 1

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
        f"[total] new={counts['ok']} already-present={counts['skip']} "
        f"(scanned {len(ph_slugs) + len(acg.AMBIENT_CG)})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
