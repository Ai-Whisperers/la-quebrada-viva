"""3-variant satellite-overlay sub-render orchestrator — visual A/B/C check.

Iterates over three overlay strategies on the same canonical ALOS heightmap
and invokes `lqv/subscene/terrain_62ha_photoreal.py` once per variant,
swapping the albedo layer via the `LQV_ALBEDO_*` env hooks:

  - bare     : LQV_ALBEDO_DISABLE=1  → pure procedural PBR, no satellite
  - s2rgb    : (default)              → Sentinel-2 L2A surface-reflectance RGB
  - ndvi     : LQV_ALBEDO_OVERRIDE_PNG=assets/terrain/escobar_ndvi.png →
                NDVI vegetation false-color (green = dense canopy)

Output run folders:

  renders/sub/runs/satellite_overlay_ab_20260618_terrain_62ha_photoreal_oblique_<v>/A.png

Serial execution only — render parallelism = 1 on the 14 GB host
(~4.3 GB RSS per Blender process OOMs at x3 per memory feedback).

Env knobs:
  RENDER_SKIP=1         dry-run (smoke-test env plumbing without rendering)
  RENDER_RES            preview (default) | final | hero
  RENDER_SAMPLES        Cycles sample count (default 32 for cheap A/B/C)
  OVERLAY_ONLY=<name>   limit to a single variant (bare|s2rgb|ndvi)
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TERRAIN_DIR = PROJECT_ROOT / "assets/terrain"

VARIANTS: list[tuple[str, dict[str, str]]] = [
    ("bare",  {"LQV_ALBEDO_DISABLE": "1"}),
    ("s2rgb", {}),
    ("ndvi",  {"LQV_ALBEDO_OVERRIDE_PNG": str(TERRAIN_DIR / "escobar_ndvi.png")}),
]

RENDER_RUN_ID = "satellite_overlay_ab_20260618"
RENDER_CAM_VIEW = "oblique"
RENDER_VARIANT = "A"

BLENDER = "/home/ai-whisperers/.local/bin/blender"
TARGET = PROJECT_ROOT / "lqv/subscene/terrain_62ha_photoreal.py"


def _missing_artifacts() -> list[str]:
    missing: list[str] = []
    if not Path(BLENDER).exists():
        missing.append(f"blender: {BLENDER}")
    if not TARGET.exists():
        missing.append(f"target: {TARGET.relative_to(PROJECT_ROOT)}")
    for name, extra in VARIANTS:
        override = extra.get("LQV_ALBEDO_OVERRIDE_PNG")
        if override and not Path(override).exists():
            missing.append(f"{name}: {Path(override).relative_to(PROJECT_ROOT)}")
    return missing


def _expected_output(name: str) -> Path:
    return (PROJECT_ROOT / "renders/sub/runs"
            / f"{RENDER_RUN_ID}_terrain_62ha_photoreal_oblique_{name}"
            / f"{RENDER_VARIANT}.png")


def _render_one(name: str, extra: dict[str, str]) -> tuple[int, float]:
    env = os.environ.copy()
    env.update({
        "RENDER_RUN_ID": RENDER_RUN_ID,
        "RENDER_RUN_TAG": f"oblique_{name}",
        "RENDER_CAM_VIEW": RENDER_CAM_VIEW,
        "RENDER_VARIANT": RENDER_VARIANT,
        "RENDER_RES": env.get("RENDER_RES", "preview"),
        "RENDER_SAMPLES": env.get("RENDER_SAMPLES", "32"),
        "LQV_ALLOW_CPU_FALLBACK": env.get("LQV_ALLOW_CPU_FALLBACK", "1"),
    })
    env.pop("LQV_ALBEDO_DISABLE", None)
    env.pop("LQV_ALBEDO_OVERRIDE_PNG", None)
    env.update(extra)

    cmd = [BLENDER, "--background", "--python", str(TARGET)]
    print(f"\n=== OVERLAY {name.upper()} ===", flush=True)
    for k, v in extra.items():
        print(f"  {k}={v}", flush=True)
    if not extra:
        print("  (default Sentinel-2 RGB overlay)", flush=True)
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

    only = os.environ.get("OVERLAY_ONLY", "").strip().lower()
    variants = [v for v in VARIANTS if not only or v[0] == only]
    if only and not variants:
        print(f"OVERLAY_ONLY={only!r} did not match any variant", file=sys.stderr)
        return 2

    if os.environ.get("RENDER_SKIP") == "1":
        print("RENDER_SKIP=1 — dry-run, listing planned invocations:")
        for name, extra in variants:
            print(f"  {name:6s}  RUN_TAG=oblique_{name}")
            if extra:
                for k, v in extra.items():
                    print(f"  {' ':6s}  {k}={v}")
            else:
                print(f"  {' ':6s}  (default Sentinel-2 RGB)")
        return 0

    failures: list[str] = []
    elapsed: dict[str, float] = {}
    for name, extra in variants:
        rc, dt = _render_one(name, extra)
        elapsed[name] = dt
        if rc != 0:
            failures.append(name)

    print("\n=== SUMMARY ===", flush=True)
    for name, dt in elapsed.items():
        out = _expected_output(name)
        status = "OK" if name not in failures else "FAIL"
        size = f"{out.stat().st_size // 1024} KB" if out.exists() else "MISSING"
        print(f"  {status:4s}  {name:6s}  {dt:6.1f}s  {size:10s}  {out.relative_to(PROJECT_ROOT)}")
    if failures:
        print(f"\n{len(failures)} variant(s) failed: {', '.join(failures)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
