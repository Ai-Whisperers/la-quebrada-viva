"""ambientCG CC0 PBR-texture downloader — project-wide curated manifest.

ambientCG distributes every asset under CC0 1.0 Universal (project-wide, blanket
license; see <https://docs.ambientcg.com/license>). This downloader pulls the
4K-JPG variant zip per ID, extracts it into `assets/textures/ambientcg/<id>/`,
and is idempotent / resume-safe / 404-tolerant.

Layout:
    assets/textures/ambientcg/<id>/<id>_Color.jpg
    assets/textures/ambientcg/<id>/<id>_Normal.jpg
    assets/textures/ambientcg/<id>/<id>_Roughness.jpg
    assets/textures/ambientcg/<id>/<id>_Displacement.jpg
    assets/textures/ambientcg/<id>/<id>_AmbientOcclusion.jpg
    assets/textures/ambientcg/<id>/_zip/<id>_4K-JPG.zip  (kept for audit)

Run:
    python3 scripts/download_ambientcg_assets.py
    # or, to dump manifest only:
    python3 scripts/download_ambientcg_assets.py --dry-run

The downloader auto-emits `LICENSES/<id>.txt` attribution stubs that point at
the shared `LICENSES/CC0-1.0.txt` legal-code mirror.

Curated 2026-06-13. See `docs/research/ASSET_RESEARCH_2026-06-13.md` for the
rationale per ID and the rural-Paraguay surface-vocabulary it covers.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import urllib.error
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections.abc import Iterable

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(PROJECT_ROOT, "assets")
LICENSES_DIR = os.path.join(PROJECT_ROOT, "LICENSES")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

ACG_DL_TEMPLATE = "https://ambientcg.com/get?file={id}_4K-JPG.zip"

CONCURRENCY = 4
TIMEOUT = 240
MAX_RETRIES = 3

# ---------------------------------------------------------------------------
# Curated manifest (85 IDs, all blanket CC0).
# Themes: bricks, wood, ground, metal, concrete, rocks, roofing-tiles, plaster.
# ---------------------------------------------------------------------------

AMBIENT_CG: list[str] = [
    # Bricks (12) — handformed + terracotta + church vernacular
    "Bricks003",
    "Bricks017",
    "Bricks019",
    "Bricks022",
    "Bricks023",
    "Bricks025",
    "Bricks030",
    "Bricks050",
    "Bricks051",
    "Bricks052",
    "Bricks066",
    "Bricks077",
    # Wood (17) — planks, beams, weathered variants for porch + structural
    "Wood005",
    "Wood006",
    "Wood013",
    "Wood017",
    "Wood019",
    "Wood021",
    "Wood022",
    "Wood023",
    "Wood025",
    "Wood026",
    "Wood027",
    "Wood028",
    "Wood036",
    "Wood048",
    "Wood049",
    "Wood050",
    "Wood051",
    # Ground (16) — laterite / dirt / grass / cracked-mud variants
    "Ground003",
    "Ground023",
    "Ground027",
    "Ground029",
    "Ground033",
    "Ground036",
    "Ground037",
    "Ground039",
    "Ground047",
    "Ground048",
    "Ground054",
    "Ground055S",
    "Ground061",
    "Ground067",
    "Ground068",
    "Ground074",
    # Metal (14) — corrugated / zinc / iron / weathered roofing
    "Metal003",
    "Metal007",
    "Metal009",
    "Metal027",
    "Metal028",
    "Metal029",
    "Metal030",
    "Metal031",
    "Metal032",
    "Metal033",
    "Metal034",
    "Metal035",
    "Metal036",
    "Metal038",
    # Concrete (5) — slab + weathered for floor + amenity bases
    "Concrete002",
    "Concrete003",
    "Concrete007",
    "Concrete017",
    "Concrete023",
    # Rocks (8) — escarpment + stream-bank
    "Rocks001",
    "Rocks002",
    "Rocks004",
    "Rocks006",
    "Rocks007",
    "Rocks009",
    "Rocks010",
    "Rocks011",
    # RoofingTiles (6) — terracotta + slate
    "RoofingTiles001",
    "RoofingTiles002",
    "RoofingTiles003",
    "RoofingTiles005",
    "RoofingTiles006",
    "RoofingTiles008",
    # Plaster (7) — lime plaster / cob exterior variants
    "Plaster001",
    "Plaster002",
    "Plaster003",
    "Plaster004",
    "Plaster005",
    "Plaster006",
    "Plaster007",
]

LICENSE_STUB_TEMPLATE = """\
Asset: {asset_id}
Source: ambientCG (https://ambientcg.com/view?id={asset_id})
License: CC0 1.0 Universal
License text: ../LICENSES/CC0-1.0.txt
License URL: https://creativecommons.org/publicdomain/zero/1.0/
Bundle source: ambientCG blanket CC0 per https://docs.ambientcg.com/license
Downloaded: {date}
"""

# ---------------------------------------------------------------------------
# Download primitives
# ---------------------------------------------------------------------------


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _http_download(url: str, dest: str, log) -> tuple[str, str, int]:
    """Download `url` to `dest` if not already present. Returns (status, dest, bytes).

    Follows redirects (ambientCG 302s to a CDN). Resume-safe by file size.
    """
    if os.path.exists(dest) and os.path.getsize(dest) > 1024:
        return ("skip", dest, os.path.getsize(dest))
    _ensure_dir(os.path.dirname(dest))
    tmp = dest + ".part"
    last_err: str | None = None
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "lqv-asset-downloader/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = resp.read()
            with open(tmp, "wb") as fh:
                fh.write(data)
            os.replace(tmp, dest)
            return ("ok", dest, len(data))
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
            if e.code in (404, 410):
                # Hard miss — don't retry.
                break
            time.sleep(2 ** attempt)
        except Exception as e:
            last_err = str(e)
            time.sleep(2 ** attempt)
    if os.path.exists(tmp):
        os.unlink(tmp)
    log(f"  FAIL {url} ({last_err})")
    return ("fail", dest, 0)


def _extract_zip(zip_path: str, out_dir: str, log) -> int:
    """Extract `zip_path` into `out_dir` (creates `out_dir`). Skips existing files."""
    n = 0
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                target = os.path.join(out_dir, info.filename)
                if os.path.exists(target) and os.path.getsize(target) > 0:
                    continue
                _ensure_dir(os.path.dirname(target))
                with zf.open(info) as src, open(target, "wb") as dst:
                    dst.write(src.read())
                n += 1
    except zipfile.BadZipFile as e:
        log(f"  BADZIP {zip_path}: {e}")
    return n


def _write_license_stub(asset_id: str, log) -> bool:
    dest = os.path.join(LICENSES_DIR, f"{asset_id}.txt")
    if os.path.exists(dest):
        return False
    _ensure_dir(LICENSES_DIR)
    with open(dest, "w") as fh:
        fh.write(LICENSE_STUB_TEMPLATE.format(asset_id=asset_id, date=time.strftime("%Y-%m-%d")))
    return True


# ---------------------------------------------------------------------------
# Per-asset orchestration
# ---------------------------------------------------------------------------


def process_one(asset_id: str, log) -> tuple[str, dict]:
    out_dir = os.path.join(ASSETS, "textures", "ambientcg", asset_id)
    zip_dir = os.path.join(out_dir, "_zip")
    zip_path = os.path.join(zip_dir, f"{asset_id}_4K-JPG.zip")
    url = ACG_DL_TEMPLATE.format(id=asset_id)

    status, _, nbytes = _http_download(url, zip_path, log)
    if status == "fail":
        return ("fail", {"id": asset_id, "bytes": 0, "extracted": 0})

    extracted = _extract_zip(zip_path, out_dir, log)
    stub_made = _write_license_stub(asset_id, log)
    return (
        status,
        {"id": asset_id, "bytes": nbytes, "extracted": extracted, "stub": stub_made},
    )


def run(ids: Iterable[str], log) -> dict:
    counts = {"ok": 0, "skip": 0, "fail": 0, "bytes": 0, "extracted": 0, "stubs": 0}
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futures = {ex.submit(process_one, aid, log): aid for aid in ids}
        for fut in as_completed(futures):
            aid = futures[fut]
            status, info = fut.result()
            counts[status] += 1
            counts["bytes"] += info["bytes"]
            counts["extracted"] += info.get("extracted", 0)
            if info.get("stub"):
                counts["stubs"] += 1
            if status == "ok":
                log(
                    f"  + {aid} ({info['bytes'] / 1024:.0f} KiB, "
                    f"extracted {info['extracted']} files)"
                )
            elif status == "skip":
                log(f"  ~ {aid} (zip already on disk)")
    return counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="enumerate plans only")
    parser.add_argument("--only", type=str, help="comma-separated ID prefixes to keep (e.g. Bricks,Wood)")
    args = parser.parse_args()

    ids = AMBIENT_CG
    if args.only:
        keep = tuple(p.strip() for p in args.only.split(","))
        ids = [a for a in AMBIENT_CG if a.startswith(keep)]

    _ensure_dir(LOG_DIR)
    log_path = os.path.join(LOG_DIR, f"ambientcg_download_{int(time.time())}.log")
    log_fh = open(log_path, "w", buffering=1)

    def log(msg: str) -> None:
        print(msg)
        log_fh.write(msg + "\n")

    log(f"[manifest] ambientcg ids={len(ids)} (full={len(AMBIENT_CG)})")
    log(f"[log] {log_path}")

    if args.dry_run:
        for aid in ids:
            log(f"  DRY {aid} → {ACG_DL_TEMPLATE.format(id=aid)}")
        log_fh.close()
        return 0

    counts = run(ids, log)
    log(
        f"\n[grand] ok={counts['ok']} skip={counts['skip']} fail={counts['fail']} "
        f"bytes={counts['bytes'] / 1024 / 1024:.1f} MiB "
        f"extracted={counts['extracted']} stubs={counts['stubs']}"
    )
    log_fh.close()
    return 0 if counts["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
