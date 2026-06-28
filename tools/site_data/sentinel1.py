"""Sentinel-1 SAR scene search + HyP3 InSAR submission helper.

We don't process InSAR locally — pyrosar / ESA SNAP is too heavy for the
escritura window. Instead this module:

  1. searches ASF DAAC (no auth) for Sentinel-1 acquisitions over the
     parcel and writes the scene list to disk;
  2. (optional) submits an InSAR_GAMMA HyP3 job using EARTHDATA_USER /
     EARTHDATA_PASS, so the cloud does the processing and the result
     comes back as a downloadable URL.

ASF Search API: https://api.daac.asf.alaska.edu/services/search/param
HyP3 API:       https://hyp3-api.asf.alaska.edu/  (https://hyp3-docs.asf.alaska.edu)

Run:
    python3 -m tools.site_data.sentinel1 --search
    python3 -m tools.site_data.sentinel1 --submit-insar
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys

import requests

from .common import (
    env_required,
    http_get,
    out_dir,
    parcel_bbox,
    search_bbox,
    write_json,
)

ASF_SEARCH = "https://api.daac.asf.alaska.edu/services/search/param"
HYP3_API = "https://hyp3-api.asf.alaska.edu"


def hyp3_client():
    """Authenticate to HyP3 via URS OAuth using hyp3-sdk."""
    from hyp3_sdk import HyP3
    user = env_required("EARTHDATA_USER")
    pw = env_required("EARTHDATA_PASS")
    return HyP3(username=user, password=pw)


def search(start: str, end: str) -> list[dict]:
    """ASF DAAC search for Sentinel-1 SLC scenes over the parcel."""
    b = search_bbox()
    wkt = (
        f"POLYGON(({b.left} {b.bottom},{b.right} {b.bottom},"
        f"{b.right} {b.top},{b.left} {b.top},{b.left} {b.bottom}))"
    )
    params = {
        "platform": "SENTINEL-1",
        "processingLevel": "SLC",
        "intersectsWith": wkt,
        "start": start,
        "end": end,
        "output": "json",
    }
    r = http_get(ASF_SEARCH, params=params, timeout=120)
    payload = r.json()
    # ASF wraps results in a list of lists.
    if payload and isinstance(payload, list):
        return payload[0]
    return []


def organise(scenes: list[dict]) -> dict[tuple[int, str], list[dict]]:
    """Group by relative orbit + pass direction → coherent InSAR stacks."""
    buckets: dict[tuple[int, str], list[dict]] = {}
    for s in scenes:
        try:
            rel = int(s.get("pathNumber") or s.get("relativeOrbit") or -1)
        except (TypeError, ValueError):
            rel = -1
        direction = (s.get("flightDirection") or "?").upper()
        buckets.setdefault((rel, direction), []).append(s)
    return buckets


def submit_insar(client, ref: str, sec: str, name: str) -> dict:
    """Submit an InSAR_GAMMA job pair to HyP3 via hyp3-sdk."""
    batch = client.submit_insar_job(
        granule1=ref,
        granule2=sec,
        name=name,
        include_look_vectors=True,
        include_displacement_maps=True,
        include_dem=True,
    )
    jobs = [j.to_dict() for j in batch.jobs]
    return {"submitted_jobs": jobs, "count": len(jobs)}


def cli() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--search", action="store_true",
                    help="Run ASF DAAC search (no auth).")
    ap.add_argument("--submit-insar", action="store_true",
                    help="Submit a HyP3 InSAR job for the most-recent valid pair.")
    ap.add_argument("--start", default="2024-01-01",
                    help="ASF search start (YYYY-MM-DD).")
    ap.add_argument("--end",
                    default=dt.datetime.now(dt.UTC).strftime("%Y-%m-%d"),
                    help="ASF search end (YYYY-MM-DD).")
    args = ap.parse_args()

    if not (args.search or args.submit_insar):
        ap.print_help()
        return 2

    out = out_dir("sentinel1")

    if args.search:
        b = parcel_bbox()
        print(f"[sentinel1] ASF search {args.start}..{args.end} "
              f"over parcel ({b.left:.4f},{b.bottom:.4f})..({b.right:.4f},{b.top:.4f})")
        try:
            scenes = search(args.start, args.end)
        except requests.RequestException as e:
            print(f"[sentinel1] ASF search failed: {e}", file=sys.stderr)
            return 1
        write_json(out / "asf_scenes.json", scenes)
        buckets = organise(scenes)
        lines = [
            "# Sentinel-1 SLC scenes — La Quebrada Viva parcel",
            "",
            "Source: ASF DAAC (https://search.asf.alaska.edu), Sentinel: CC0  ",
            f"Window: {args.start} → {args.end}  ",
            f"Pulled: {dt.datetime.now(dt.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}",
            "",
            f"Total scenes returned: **{len(scenes)}**",
            "",
            "## Coherent stacks (relative orbit × pass direction)",
            "",
            "| Rel. orbit | Direction | Scenes | Date range |",
            "| --- | --- | ---:| --- |",
        ]
        for (rel, direction), bs in sorted(buckets.items(),
                                           key=lambda kv: -len(kv[1])):
            dates = sorted(s.get("startTime", "") for s in bs)
            lines.append(
                f"| {rel} | {direction} | {len(bs)} | {dates[0][:10]} → {dates[-1][:10]} |"
            )
        lines += [
            "",
            "## Next step (manual / scripted)",
            "",
            "- Pick the largest bucket above → that's your coherent stack.",
            "- Submit InSAR pairs to HyP3 (cloud processing):",
            "",
            "  ```bash",
            "  export EARTHDATA_USER=...",
            "  export EARTHDATA_PASS=...",
            "  python3 -m tools.site_data.sentinel1 --submit-insar",
            "  ```",
            "",
            "  Submission picks the two most-recent scenes from the largest",
            "  coherent stack. Edit the script if you need a specific pair.",
            "",
            "- Result downloads from `https://hyp3-api.asf.alaska.edu/jobs/<id>` once",
            "  the job finishes (usually under an hour).",
        ]
        (out / "sentinel1_brochure.md").write_text("\n".join(lines))
        (out / "sentinel1_summary.txt").write_text(
            f"ASF search: {len(scenes)} scenes, "
            f"{len(buckets)} orbit×direction buckets\n"
        )
        print(f"[sentinel1] wrote {out}")
        return 0

    if args.submit_insar:
        # Load most recent search; pick the two newest scenes from the largest stack.
        scenes_path = out / "asf_scenes.json"
        if not scenes_path.exists():
            print(f"[sentinel1] run --search first (no {scenes_path})", file=sys.stderr)
            return 2
        import json
        scenes = json.loads(scenes_path.read_text())
        buckets = organise(scenes)
        if not buckets:
            print("[sentinel1] no scenes to submit", file=sys.stderr)
            return 1
        largest = max(buckets.items(), key=lambda kv: len(kv[1]))[1]
        largest = sorted(largest, key=lambda s: s.get("startTime", ""), reverse=True)
        if len(largest) < 2:
            print("[sentinel1] stack too short for a pair", file=sys.stderr)
            return 1
        ref = largest[0]["granuleName"]
        sec = largest[1]["granuleName"]
        client = hyp3_client()
        job_name = "LQV-parcel-insar"
        existing = client.find_jobs(name=job_name)
        if existing.jobs:
            print(
                f"[sentinel1] {len(existing.jobs)} existing job(s) named {job_name};"
                " skipping submit"
            )
            result = {
                "submitted_jobs": [j.to_dict() for j in existing.jobs],
                "count": len(existing.jobs),
                "note": "found pre-existing jobs; not resubmitted",
            }
        else:
            print(f"[sentinel1] submitting HyP3 InSAR_GAMMA: ref={ref} sec={sec}")
            result = submit_insar(client, ref, sec, name=job_name)
        write_json(out / "hyp3_submission.json", result)
        print(f"[sentinel1] submitted; track at {HYP3_API}/jobs")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
