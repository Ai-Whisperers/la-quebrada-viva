#!/usr/bin/env python3
"""
ingest_album.py — Wes's Google Photos album → validated captures.

Triggered when Wes hands over a Google Photos album (zip / folder / direct
album link via takeout). For every video found:

  1. Probe with ffprobe (duration, codec, container, resolution).
  2. Compute a motion score via ffmpeg signalstats (mean |ΔY| across frames).
  3. Decide accept / reject based on SKILL.md thresholds.
  4. Stage accepted videos in splats/captures/<YYYY-MM-DD>_<source>/
  5. (--split-safety) split captures > 60 s into < 60 s clips, per the
     task backup-path rule ("split captures into <1 min clips for safety").
  6. Write _ingest_check.json with per-video accept/reject reasons +
     aggregate stats so the train phase can audit before launch.

Class-level: this script is the LQV instance of the class-level
"Wes-side phone video capture" runbook from satellite-to-blender-pipeline.
Thresholds are pinned in lqv-bundle/capture/SKILL.md:
  - min_duration_s: 10.0
  - min_motion_score: 0.30
  - accepted_codecs: [mp4, mov, webm, m4v]

Usage:
  python3 ingest_album.py --input /path/to/album [--source wes] [--date 2026-07-29]
  python3 ingest_album.py --input ~/Downloads/takeout-20260729.zip --source wes
  python3 ingest_album.py --input /path/to/album --split-safety  # task default
  python3 ingest_album.py --input /path/to/album --dry-run       # no copies

Exit codes:
  0 = all accepted (or only warnings)
  2 = some rejected but at least one accepted (continue to train)
  3 = all rejected (stop — surface to operator)

Spec source: lqv-bundle/capture/SKILL.md
Author: Erebus (built under kanban task t_b2ef974f, 2026-07-28)
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ----- Thresholds (pinned from lqv-bundle/capture/SKILL.md) -----
MIN_DURATION_S = 10.0
MIN_MOTION_SCORE = 0.30
ACCEPTED_CODECS = {"mp4", "mov", "webm", "m4v"}
ACCEPTED_CONTAINERS = {"mp4", "mov", "webm", "m4v", "quicktime"}
SPLIT_SAFETY_S = 60  # task body: split captures > 1 min for safety
SPLIT_SAFETY_DEFAULT = True  # default ON per task brief

# Repo root: this script lives at splats/tools/ingest_album.py
SCRIPT_DIR = Path(__file__).resolve().parent
SPLATS_DIR = SCRIPT_DIR.parent  # splats/
CAPTURES_DIR = SPLATS_DIR / "captures"

# Common Google Photos / iPhone export extensions we'll process
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".m4v", ".hevc", ".3gp", ".avi", ".mkv"}


# ----- Helpers -----

def _log(msg: str) -> None:
    print(f"[ingest_album] {msg}", flush=True)


def _run(cmd: list[str], *, timeout: int = 120) -> tuple[int, str, str]:
    """Run a subprocess, return (rc, stdout, stderr). No shell expansion."""
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s: {' '.join(cmd)}"


def probe_video(path: Path) -> dict:
    """Probe a single video file with ffprobe. Returns parsed dict or {error:..}."""
    rc, out, err = _run(
        [
            "ffprobe",
            "-v", "error",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            "-select_streams", "v:0",
            str(path),
        ],
        timeout=60,
    )
    if rc != 0:
        return {"error": f"ffprobe failed: {err.strip()[:500]}", "rc": rc}
    try:
        return json.loads(out)
    except json.JSONDecodeError as exc:
        return {"error": f"ffprobe output not JSON: {exc}", "raw_head": out[:500]}


def _probe_field(probe: dict, *path, default=None):
    """Read a nested dict field by path (str keys + int array indices)."""
    cur: object = probe
    for key in path:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        elif isinstance(cur, list) and isinstance(key, int) and 0 <= key < len(cur):
            cur = cur[key]
        else:
            return default
    return cur


def compute_motion_score(path: Path, *, max_seconds: int = 300) -> float:
    """
    Compute motion score as mean absolute frame-to-frame luma delta.

    Implementation: ffmpeg with signalstats filter, output per-frame
    YAVG to a sidecar ffmetadata file, parse the file, compute
    mean(|YAVG[n] - YAVG[n-1]|).

    For long videos, sample at 1 fps for the first `max_seconds` to keep
    runtime bounded (3 minutes of sample is plenty for a motion proxy).

    Returns 0.0 on failure (caller should treat 0 as inconclusive).
    """
    # 1. ffmetadata sidecar with per-frame YAVG
    # ffmpeg's signalstats prints YAVG via metadata=print:key=lavfi.signalstats.YAVG
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-nostats",
        "-i", str(path),
        "-t", str(max_seconds),
        "-vf", "fps=1,signalstats,metadata=print:file=/tmp/_ingest_yavg.txt:key=lavfi.signalstats.YAVG",
        "-an",
        "-f", "null",
        "-",
    ]
    rc, _, err = _run(cmd, timeout=max_seconds + 60)
    if rc != 0:
        _log(f"  signalstats rc={rc} (treating as motion=0): {err.strip()[:200]}")
        return 0.0
    sidecar = Path("/tmp/_ingest_yavg.txt")
    if not sidecar.exists():
        return 0.0
    samples: list[float] = []
    for line in sidecar.read_text(errors="replace").splitlines():
        line = line.strip()
        if line.startswith("lavfi.signalstats.YAVG="):
            try:
                samples.append(float(line.split("=", 1)[1]))
            except ValueError:
                continue
    sidecar.unlink(missing_ok=True)
    if len(samples) < 2:
        return 0.0
    deltas = [abs(samples[i] - samples[i - 1]) for i in range(1, len(samples))]
    return sum(deltas) / len(deltas) if deltas else 0.0


def split_for_safety(path: Path, out_dir: Path, *, segment_s: int = SPLIT_SAFETY_S) -> list[Path]:
    """
    Split a video into <segment_s> second clips via ffmpeg segment muxer.
    Returns list of clip paths produced.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    pattern = out_dir / f"{path.stem}_clip_%03d{path.suffix}"
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-nostats",
        "-y",
        "-i", str(path),
        "-c", "copy",
        "-f", "segment",
        "-segment_time", str(segment_s),
        "-reset_timestamps", "1",
        str(pattern),
    ]
    rc, _, err = _run(cmd, timeout=600)
    if rc != 0:
        _log(f"  split failed rc={rc}: {err.strip()[:200]}")
        return []
    clips = sorted(out_dir.glob(f"{path.stem}_clip_*{path.suffix}"))
    return clips


def sha256_file(path: Path, *, chunk: int = 1 << 20) -> str:
    """SHA256 of a file (streaming)."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            buf = fh.read(chunk)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


# ----- Per-file decision -----

def decide_one(
    path: Path,
    *,
    split_safety: bool,
    min_duration_s: float = MIN_DURATION_S,
    min_motion_score: float = MIN_MOTION_SCORE,
    max_seconds_probe: int = 300,
) -> dict:
    """
    Run probe + motion score, decide accept/reject, optionally split.

    Returns a dict:
      {
        "src": str,
        "filename": str,
        "size_bytes": int,
        "duration_s": float | None,
        "codec_name": str | None,
        "container": str | None,
        "resolution": str | None,    # e.g. "1920x1080"
        "motion_score": float,
        "decision": "accept" | "reject",
        "reasons": list[str],
        "sha256": str,
        "staged_path": str | None,   # relative to captures/<date>_<source>/
        "split_clips": list[str],    # relative paths if split
      }
    """
    record: dict = {
        "src": str(path),
        "filename": path.name,
        "size_bytes": path.stat().st_size,
    }

    # 1. ffprobe
    probe = probe_video(path)
    if "error" in probe:
        record["decision"] = "reject"
        record["reasons"] = [f"ffprobe: {probe['error']}"]
        record.update({"duration_s": None, "codec_name": None, "container": None,
                       "resolution": None, "motion_score": 0.0})
        return record

    duration_obj: object = _probe_field(probe, "format", "duration", default=None)
    duration_f: Optional[float] = None
    if duration_obj is not None and not isinstance(duration_obj, dict):
        try:
            duration_f = float(str(duration_obj))
        except (TypeError, ValueError):
            duration_f = None

    container_obj: object = _probe_field(probe, "format", "format_name", default="")
    container = (str(container_obj) if container_obj is not None else "").split(",")[0].strip().lower()
    codec_obj: object = _probe_field(probe, "streams", 0, "codec_name", default="")
    codec = (str(codec_obj) if codec_obj is not None else "").lower()
    width: object = _probe_field(probe, "streams", 0, "width", default=None)
    height: object = _probe_field(probe, "streams", 0, "height", default=None)
    resolution = f"{width}x{height}" if width and height else None

    record.update({
        "duration_s": duration_f,
        "codec_name": codec or None,
        "container": container or None,
        "resolution": resolution,
    })

    reasons: list[str] = []

    # 2. Container / codec gate
    if container and container not in ACCEPTED_CONTAINERS:
        reasons.append(f"container '{container}' not in {sorted(ACCEPTED_CONTAINERS)}")

    # 3. Duration gate
    if duration_f is None:
        reasons.append("duration unknown (ffprobe could not parse)")
    elif duration_f < min_duration_s:
        reasons.append(f"duration {duration_f:.1f}s < {min_duration_s}s min")

    # 4. Motion score gate
    motion = compute_motion_score(path, max_seconds=max_seconds_probe)
    record["motion_score"] = round(motion, 4)
    if motion < min_motion_score:
        reasons.append(
            f"motion {motion:.2f} < {min_motion_score} min "
            f"(video too still — phone likely stationary)"
        )

    if reasons:
        record["decision"] = "reject"
        record["reasons"] = reasons
        return record

    # 5. Accept: stage file + optional safety split
    record["decision"] = "accept"
    record["reasons"] = []
    record["sha256"] = sha256_file(path)
    record["staged_path"] = path.name
    record["split_clips"] = []

    return record


# ----- Album-wide driver -----

def discover_videos(input_path: Path) -> list[Path]:
    """Find all video files under input_path (file, folder, or unzipped zip dir)."""
    if input_path.is_file():
        if input_path.suffix.lower() in VIDEO_EXTENSIONS:
            return [input_path]
        return []
    if not input_path.is_dir():
        return []
    out: list[Path] = []
    for p in input_path.rglob("*"):
        if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS:
            out.append(p)
    return sorted(out)


def stage_outputs(
    records: list[dict],
    *,
    date_str: str,
    source: str,
    split_safety: bool,
) -> None:
    """Copy accepted records into captures/<date>_<source>/ and split long ones."""
    out_dir = CAPTURES_DIR / f"{date_str}_{source}"
    out_dir.mkdir(parents=True, exist_ok=True)
    for rec in records:
        if rec["decision"] != "accept":
            continue
        src = Path(rec["src"])
        dest = out_dir / src.name
        if not dest.exists():
            shutil.copy2(src, dest)
        rec["staged_path"] = str(dest.relative_to(CAPTURES_DIR))

        if split_safety and rec["duration_s"] and rec["duration_s"] > SPLIT_SAFETY_S:
            clips = split_for_safety(src, out_dir)
            rec["split_clips"] = [str(c.relative_to(CAPTURES_DIR)) for c in clips]


# ----- Main -----

def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Ingest a Wes capture album into splats/captures/ with quality gates."
    )
    parser.add_argument("--input", required=True, help="Album folder / zip / single video")
    parser.add_argument("--source", default="wes", help="Source tag (default: wes)")
    parser.add_argument("--date", default=None, help="Date tag YYYY-MM-DD (default: today America/Asuncion)")
    parser.add_argument("--split-safety", dest="split_safety",
                        action="store_true", default=SPLIT_SAFETY_DEFAULT,
                        help=f"Split captures > {SPLIT_SAFETY_S}s into clips (default ON)")
    parser.add_argument("--no-split-safety", dest="split_safety",
                        action="store_false", help="Disable safety splits")
    parser.add_argument("--dry-run", action="store_true",
                        help="Probe + score, but do not copy or split")
    parser.add_argument("--min-duration-s", type=float, default=10.0,
                        help=f"Min duration to accept (default {MIN_DURATION_S})")
    parser.add_argument("--min-motion-score", type=float, default=0.30,
                        help=f"Min motion score to accept (default {MIN_MOTION_SCORE})")
    parser.add_argument("--max-seconds-probe", type=int, default=300,
                        help="Cap motion probe to N seconds of input (default 300)")
    args = parser.parse_args(argv)

    # Per-invocation thresholds (don't mutate module globals — keeps script
    # re-entrant under --dry-run followed by a real run).
    min_duration_s = args.min_duration_s
    min_motion_score = args.min_motion_score

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        _log(f"ERROR: input not found: {input_path}")
        return 4

    date_str = args.date or _dt.date.today().isoformat()
    _log(f"input={input_path}  source={args.source}  date={date_str}  "
         f"split_safety={args.split_safety}  dry_run={args.dry_run}")

    videos = discover_videos(input_path)
    if not videos:
        _log("No video files discovered. Check --input path or supported extensions.")
        return 0

    _log(f"discovered {len(videos)} video(s)")

    records: list[dict] = []
    for v in videos:
        _log(f"probing {v.name}")
        rec = decide_one(
            v,
            split_safety=args.split_safety,
            min_duration_s=min_duration_s,
            min_motion_score=min_motion_score,
            max_seconds_probe=args.max_seconds_probe,
        )
        records.append(rec)
        status = rec["decision"].upper()
        reason = "; ".join(rec["reasons"]) if rec["reasons"] else "ok"
        _log(f"  -> {status} ({reason})")

    # Stage accepted
    if not args.dry_run:
        stage_outputs(records, date_str=date_str, source=args.source,
                      split_safety=args.split_safety)

    # Summary + per-batch check JSON
    accepted = sum(1 for r in records if r["decision"] == "accept")
    rejected = len(records) - accepted
    summary = {
        "input": str(input_path),
        "date": date_str,
        "source": args.source,
        "thresholds": {
            "min_duration_s": min_duration_s,
            "min_motion_score": min_motion_score,
            "split_safety_s": SPLIT_SAFETY_S,
        },
        "totals": {
            "discovered": len(records),
            "accepted": accepted,
            "rejected": rejected,
        },
        "records": records,
    }

    if not args.dry_run:
        out_dir = CAPTURES_DIR / f"{date_str}_{args.source}"
        out_dir.mkdir(parents=True, exist_ok=True)
        check_path = out_dir / "_ingest_check.json"
        check_path.write_text(json.dumps(summary, indent=2, sort_keys=True))
        _log(f"wrote {check_path}")

    _log(f"summary: {accepted} accepted / {rejected} rejected of {len(records)}")

    if rejected == 0:
        return 0
    if accepted == 0:
        return 3
    return 2


if __name__ == "__main__":
    sys.exit(main())