"""Cross-reference LICENSES/*.txt against in-repo asset slugs.

Reports three classes of drift so the bundle stays attribution-complete:

    missing : asset on disk has no LICENSES/<slug>.txt
    orphan  : LICENSES/<slug>.txt exists but no asset on disk uses it
    mismatch: license file's `Asset:` header disagrees with its filename slug

Slug derivation:
    assets/hdris/<slug>_4k.{exr,hdr}            -> <slug>
    assets/hdris/_unused_wrong_biome/<slug>_4k* -> <slug> (still on disk -> still requires attribution)
    assets/models/<slug>/                       -> <slug>
    assets/textures/<slug>/                     -> <slug>
    assets/{models,textures}/<vendor>/<slug>/   -> <slug> (vendor wrapper auto-detected
                                                 when the directory contains only
                                                 subdirectories — e.g. assets/textures/ambientcg/)

Umbrella files (CC0-1.0.txt, CC-BY-4.0.txt, README.md) are ignored when
scanning per-asset stubs. assets/terrain/ is project-internal generated
data and is also ignored.

Exit codes:
    0 — clean
    1 — drift (any of: missing, orphan, mismatch)
    2 — usage error / repo layout missing
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from collections.abc import Iterable

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LICENSES_DIR = os.path.join(REPO_ROOT, "LICENSES")
ASSETS_DIR = os.path.join(REPO_ROOT, "assets")

UMBRELLA_FILES = frozenset({"CC0-1.0.txt", "CC-BY-4.0.txt", "README.md"})
HDRI_SUFFIX_RE = re.compile(r"_(?:[0-9]+k|[0-9]+K)$")
ASSET_HEADER_RE = re.compile(r"^Asset:\s*(\S+)\s*$", re.MULTILINE)


def _hdri_slug(filename: str) -> str:
    stem = os.path.splitext(filename)[0]
    return HDRI_SUFFIX_RE.sub("", stem)


def _is_vendor_wrapper(path: str) -> bool:
    """A vendor wrapper is a directory whose immediate children are all subdirs."""
    try:
        entries = list(os.scandir(path))
    except OSError:
        return False
    if not entries:
        return False
    return all(e.is_dir() for e in entries)


def _collect_asset_slugs() -> dict[str, list[str]]:
    by_slug: dict[str, list[str]] = {}

    hdris_root = os.path.join(ASSETS_DIR, "hdris")
    if os.path.isdir(hdris_root):
        for entry in os.listdir(hdris_root):
            full = os.path.join(hdris_root, entry)
            if os.path.isfile(full) and entry.lower().endswith((".exr", ".hdr")):
                slug = _hdri_slug(entry)
                by_slug.setdefault(slug, []).append(f"assets/hdris/{entry}")
            elif os.path.isdir(full) and entry.startswith("_unused"):
                for sub in os.listdir(full):
                    if sub.lower().endswith((".exr", ".hdr")):
                        slug = _hdri_slug(sub)
                        by_slug.setdefault(slug, []).append(
                            f"assets/hdris/{entry}/{sub}"
                        )

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
                    sub_full = os.path.join(full, sub)
                    if os.path.isdir(sub_full):
                        by_slug.setdefault(sub, []).append(
                            f"assets/{kind}/{entry}/{sub}/"
                        )
            else:
                by_slug.setdefault(entry, []).append(f"assets/{kind}/{entry}/")

    return by_slug


def _collect_license_stubs() -> dict[str, str]:
    stubs: dict[str, str] = {}
    if not os.path.isdir(LICENSES_DIR):
        return stubs
    for fname in os.listdir(LICENSES_DIR):
        if not fname.endswith(".txt") or fname in UMBRELLA_FILES:
            continue
        slug = fname[: -len(".txt")]
        stubs[slug] = os.path.join(LICENSES_DIR, fname)
    return stubs


def _header_slug(path: str) -> str | None:
    try:
        with open(path, encoding="utf-8") as f:
            head = f.read(512)
    except OSError:
        return None
    m = ASSET_HEADER_RE.search(head)
    return m.group(1) if m else None


def _fmt(rows: Iterable[str], indent: str = "  ") -> str:
    items = list(rows)
    if not items:
        return f"{indent}(none)"
    return "\n".join(f"{indent}{r}" for r in items)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit LICENSES/<slug>.txt coverage against assets/."
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print the summary line and exit; suppress drift detail.",
    )
    args = parser.parse_args(argv)

    if not os.path.isdir(LICENSES_DIR):
        print(f"error: LICENSES/ missing at {LICENSES_DIR}", file=sys.stderr)
        return 2
    if not os.path.isdir(ASSETS_DIR):
        print(f"error: assets/ missing at {ASSETS_DIR}", file=sys.stderr)
        return 2

    asset_slugs = _collect_asset_slugs()
    stubs = _collect_license_stubs()

    asset_set = set(asset_slugs)
    stub_set = set(stubs)

    missing = sorted(asset_set - stub_set)
    orphan = sorted(stub_set - asset_set)

    mismatches: list[tuple[str, str]] = []
    for slug in sorted(stub_set & asset_set):
        header = _header_slug(stubs[slug])
        if header is not None and header != slug:
            mismatches.append((slug, header))

    drift = bool(missing or orphan or mismatches)
    summary = (
        f"licenses: {len(asset_set)} asset slugs, {len(stub_set)} per-asset stubs, "
        f"{len(missing)} missing, {len(orphan)} orphan, {len(mismatches)} mismatched"
    )
    print(summary)

    if drift and not args.quiet:
        print("\n[missing] assets present but no LICENSES/<slug>.txt:")
        print(_fmt(f"{s}  ({asset_slugs[s][0]})" for s in missing))
        print("\n[orphan] LICENSES/<slug>.txt present but no asset on disk:")
        print(_fmt(orphan))
        print("\n[mismatch] license filename does not match its Asset: header:")
        print(_fmt(f"{slug}  ->  Asset: {hdr}" for slug, hdr in mismatches))

    return 1 if drift else 0


if __name__ == "__main__":
    raise SystemExit(main())
