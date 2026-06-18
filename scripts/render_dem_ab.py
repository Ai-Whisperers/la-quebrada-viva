"""4-DEM oblique sub-render orchestrator — visual A/B/C/D cross-check.

Iterates over the four baked heightmaps (ALOS canonical, COP30, SRTM, NASADEM)
and invokes `lqv/subscene/terrain_62ha_photoreal.py` once per DEM, swapping
the heightmap pair via the `LQV_DEM_OVERRIDE_PNG` + `LQV_DEM_OVERRIDE_JSON`
env hooks. Each DEM gets its own run folder via a constant `RENDER_RUN_ID`
plus a per-DEM `RENDER_RUN_TAG`:

  renders/sub/runs/dem_ab_20260618_terrain_62ha_photoreal_oblique_<dem>/A.png

Serial execution only — render parallelism = 1 on the 14 GB host
(~4.3 GB RSS per Blender process OOMs at x3 per memory feedback).

Env knobs:
  RENDER_SKIP=1     dry-run (smoke-test env plumbing without rendering)
  RENDER_RES        preview (default) | final | hero
  RENDER_SAMPLES    Cycles sample count (default 64 for A/B compare)
  DEM_ONLY=<name>   limit to a single DEM (alos|cop30|srtm|nasadem)
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TERRAIN_DIR = PROJECT_ROOT / "assets/terrain"

DEMS: list[tuple[str, Path, Path]] = [
    ("alos",
     TERRAIN_DIR / "escobar_height.png",
     TERRAIN_DIR / "escobar_height.json"),
    ("cop30",
     TERRAIN_DIR / "escobar_height_cop30.png",
     TERRAIN_DIR / "escobar_height_cop30.json"),
    ("srtm",
     TERRAIN_DIR / "escobar_height_srtm.png",
     TERRAIN_DIR / "escobar_height_srtm.json"),
    ("nasadem",
     TERRAIN_DIR / "escobar_height_nasadem.png",
     TERRAIN_DIR / "escobar_height_nasadem.json"),
]

RENDER_RUN_ID = "dem_ab_20260618"
RENDER_CAM_VIEW = "oblique"
RENDER_VARIANT = "A"

BLENDER = "/home/ai-whisperers/.local/bin/blender"
TARGET = PROJECT_ROOT / "lqv/subscene/terrain_62ha_photoreal.py"


def _missing_artifacts() -> list[str]:
    missing: list[str] = []
    for name, png, jsn in DEMS:
        if not png.exists():
            missing.append(f"{name}: {png.relative_to(PROJECT_ROOT)}")
        if not jsn.exists():
            missing.append(f"{name}: {jsn.relative_to(PROJECT_ROOT)}")
    if not Path(BLENDER).exists():
        missing.append(f"blender: {BLENDER}")
    if not TARGET.exists():
        missing.append(f"target: {TARGET.relative_to(PROJECT_ROOT)}")
    return missing


def _expected_output(name: str) -> Path:
    return (PROJECT_ROOT / "renders/sub/runs"
            / f"{RENDER_RUN_ID}_terrain_62ha_photoreal_oblique_{name}"
            / f"{RENDER_VARIANT}.png")


def _render_one(name: str, png: Path, jsn: Path) -> tuple[int, float]:
    env = os.environ.copy()
    env.update({
        "RENDER_RUN_ID": RENDER_RUN_ID,
        "RENDER_RUN_TAG": f"oblique_{name}",
        "RENDER_CAM_VIEW": RENDER_CAM_VIEW,
        "RENDER_VARIANT": RENDER_VARIANT,
        "RENDER_RES": env.get("RENDER_RES", "preview"),
        "RENDER_SAMPLES": env.get("RENDER_SAMPLES", "64"),
        "LQV_DEM_OVERRIDE_PNG": str(png),
        "LQV_DEM_OVERRIDE_JSON": str(jsn),
    })
    cmd = [BLENDER, "--background", "--python", str(TARGET)]
    print(f"\n=== DEM {name.upper()}  ({png.name}) ===", flush=True)
    print(f"  RENDER_RUN_TAG=oblique_{name}", flush=True)
    print(f"  RENDER_RES={env['RENDER_RES']}  RENDER_SAMPLES={env['RENDER_SAMPLES']}", flush=True)
    t0 = time.monotonic()
    proc = subprocess.run(cmd, env=env, cwd=PROJECT_ROOT, check=False)
    dt = time.monotonic() - t0
    out = _expected_output(name)
    rc = proc.returncode
    if rc == 0 and not out.exists():
        print(f"  Blender exit=0 but expected output missing: {out}", flush=True)
        rc = 3
    print(f"  exit={rc}  elapsed={dt:.1f}s", flush=True)
    return rc, dt


def main() -> int:
    missing = _missing_artifacts()
    if missing:
        print("MISSING ARTIFACTS:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 2

    only = os.environ.get("DEM_ONLY", "").strip().lower()
    dems = [d for d in DEMS if not only or d[0] == only]
    if only and not dems:
        print(f"DEM_ONLY={only!r} did not match any DEM", file=sys.stderr)
        return 2

    if os.environ.get("RENDER_SKIP") == "1":
        print("RENDER_SKIP=1 — dry-run, listing planned invocations:")
        for name, png, jsn in dems:
            print(f"  {name:8s}  PNG={png.relative_to(PROJECT_ROOT)}")
            print(f"  {' ':8s}  JSON={jsn.relative_to(PROJECT_ROOT)}")
            print(f"  {' ':8s}  RUN_TAG=oblique_{name}")
        return 0

    failures: list[str] = []
    elapsed: dict[str, float] = {}
    for name, png, jsn in dems:
        rc, dt = _render_one(name, png, jsn)
        elapsed[name] = dt
        if rc != 0:
            failures.append(name)

    print("\n=== SUMMARY ===", flush=True)
    for name, dt in elapsed.items():
        out = _expected_output(name)
        status = "OK" if name not in failures else "FAIL"
        size = f"{out.stat().st_size // 1024} KB" if out.exists() else "MISSING"
        print(f"  {status:4s}  {name:8s}  {dt:6.1f}s  {size:10s}  {out.relative_to(PROJECT_ROOT)}")
    if failures:
        print(f"\n{len(failures)} DEM(s) failed: {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
