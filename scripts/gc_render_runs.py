"""Garbage-collect old sub-render run folders under `renders/sub/runs/`.

Each render batch produces `renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/`
plus a `latest/` mirror and a flat back-compat path under `renders/sub/`. The
flat path and `latest/` mirror are the operational truth; the timestamped run
folders accumulate ~4-12 MB each and there are already 300+ on disk.

Defaults to dry-run. Pre-escritura (before 2026-06-27 commit `85e86aa` byte-
freeze lifts) call with no `--apply` flag and inspect the report only.

Retention policy:
  - Always keep folders whose name contains one of the protected tags
    (see PROTECTED_TAGS).
  - Otherwise, keep the N most-recent folders per asset (default 3).
  - `--older-than DAYS` is an additional gate: a folder is only considered
    for deletion if its mtime is older than DAYS (default 14).
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "renders" / "sub" / "runs"

# Folder name tokens that pin a run folder against GC.
# `escritura`, `wesley_bundle`, `v_final`, `final` map to deliverables that
# must survive cleanup. `_legacy` is the pre-RENDER_RUN_ID flat-path marker.
PROTECTED_TAGS = (
    "escritura",
    "wesley_bundle",
    "v_final",
    "_final_",
    "_final",
    "_legacy",
    "review_2026-06-",
)

ASSET_RE = re.compile(r"^[0-9]{8}_[A-Za-z0-9]+_(?P<asset>[A-Za-z0-9_]+?)(?:_[A-Z])?$")


def asset_key(folder: Path) -> str:
    """Best-effort asset key for grouping runs (asset name, sans timestamp/tag)."""
    name = folder.name
    # Strip leading `YYYYMMDD_HHMMSS_` or `YYYYMMDD_<tag>_` prefix.
    stripped = re.sub(r"^[0-9]{8}(?:_[0-9]{6})?_", "", name)
    # Strip trailing `_<variant>` if it's a known variant token.
    stripped = re.sub(r"_(A|B|C|preview|hero|final)$", "", stripped)
    return stripped or name


def is_protected(folder: Path) -> bool:
    name = folder.name.lower()
    return any(tag in name for tag in PROTECTED_TAGS)


def folder_size_bytes(folder: Path) -> int:
    total = 0
    for p in folder.rglob("*"):
        if p.is_file() and not p.is_symlink():
            try:
                total += p.stat().st_size
            except OSError:
                pass
    return total


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024  # type: ignore[assignment]
    return f"{n:.1f} TB"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--keep", type=int, default=3,
                    help="Keep N most-recent folders per asset (default: 3).")
    ap.add_argument("--older-than", type=int, default=14,
                    help="Only consider folders older than DAYS (default: 14).")
    ap.add_argument("--apply", action="store_true",
                    help="Actually delete. Default is dry-run.")
    args = ap.parse_args()

    if not RUNS.exists():
        print(f"no runs dir at {RUNS}", file=sys.stderr)
        return 0

    cutoff = time.time() - args.older_than * 86400
    by_asset: dict[str, list[Path]] = defaultdict(list)
    for folder in RUNS.iterdir():
        if folder.is_dir() and not folder.is_symlink():
            by_asset[asset_key(folder)].append(folder)

    kept_protected: list[Path] = []
    kept_recent: list[Path] = []
    kept_young: list[Path] = []
    to_delete: list[Path] = []

    for folders in by_asset.values():
        folders.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        recent_quota = args.keep
        for folder in folders:
            if is_protected(folder):
                kept_protected.append(folder)
                continue
            if recent_quota > 0:
                kept_recent.append(folder)
                recent_quota -= 1
                continue
            if folder.stat().st_mtime > cutoff:
                kept_young.append(folder)
                continue
            to_delete.append(folder)

    bytes_freed = sum(folder_size_bytes(p) for p in to_delete)

    print(f"runs dir:         {RUNS}")
    print(f"groups (assets):  {len(by_asset)}")
    print(f"total folders:    {sum(len(v) for v in by_asset.values())}")
    print(f"protected (tag):  {len(kept_protected)}")
    print(f"kept recent:      {len(kept_recent)}")
    print(f"kept young:       {len(kept_young)}")
    print(f"deletable:        {len(to_delete)}  ({human(bytes_freed)})")
    print()

    if args.apply:
        for folder in to_delete:
            shutil.rmtree(folder)
        print(f"deleted {len(to_delete)} folders, freed ~{human(bytes_freed)}.")
    else:
        print("DRY RUN — no changes made. Re-run with --apply to delete.")
        print("First 10 deletion candidates:")
        for folder in to_delete[:10]:
            print(f"  {folder.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
