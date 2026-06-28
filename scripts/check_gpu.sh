#!/usr/bin/env bash
# Print Cycles GPU detection state — what `lqv.engine.configure_engine` will pick.
# Useful for diagnosing why a render fell back to CPU on a machine with a GPU.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$HERE"

blender --background --factory-startup --python-expr '
import bpy
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.refresh_devices()
print("=== compute device types available ===")
for t in ("OPTIX", "CUDA", "HIP", "ONEAPI", "METAL"):
    try:
        prefs.compute_device_type = t
        print(f"  {t}: SUPPORTED")
    except Exception as e:
        print(f"  {t}: not supported ({e!r})")
print()
print("=== devices visible at each backend ===")
for t in ("NONE", "CUDA", "OPTIX", "HIP", "ONEAPI", "METAL"):
    try:
        prefs.compute_device_type = t
    except Exception:
        continue
    devs = prefs.get_devices_for_type(t) if t != "NONE" else []
    if devs:
        print(f"  [{t}]")
        for d in devs:
            print(f"    - {d.type:6s}  use={d.use}  name={d.name!r}")
print()
print("=== lqv.engine pick ===")
import sys, os
sys.path.insert(0, ".")
from lqv import engine
print(f"  selected device: {engine.configure_engine.__doc__!r}")
' 2>&1 | sed -n '/^===/,$p'
