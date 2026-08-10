# Wes post-escritura brainstorm — 2026-06-30

5 audio recordings from Wesley van de Camp on 2026-06-30, captured
the evening after the escritura signing. Spans ~3h 19m of brainstorm
content in Dutch (primary), with English and Spanish code-switches.

## Files

| Tag | Length | Source cache file | Status |
|-----|--------|-------------------|--------|
| A   | 39 min | doc_d6daa2988938 (14:52) | local transcription pending |
| B   | 2 min  | doc_859e26d9375d (15:32) | **done** — see `drafts/audio1_short_2min/` |
| C   | 29 min | doc_a07228f3a68e (15:35) | local transcription pending |
| D   | 18 min | doc_f3d2c4eb5428 (16:03) | local transcription pending |
| E   | 1h 50m | doc_c7d61fbc46d7 (16:22) | local transcription pending |

Naming convention used in this repo: `audio{N}_{duration}` where
N is **ascending by file size** (Audio 1 = shortest, Audio 5 = longest).
This matches the transcription-job output directory naming, not the
chronological arrival order. See `turboscribe_manifest.json` for the
chronological → file mapping.

## What's in this directory

- `turboscribe_manifest.txt` + `.json` — single-file Turboscribe upload
  (the `wes_2026-06-30_full_chronological_for_turboscribe.mp3`,
  3h 19m, mono 16kHz mp3, parts separated by 1s silence)
- `drafts/audio{N}_{duration}/raw.txt` — local faster-whisper large-v3
  transcript per audio
- `drafts/audio{N}_{duration}/meta.json` — duration, detected language,
  segment count, model info
- `drafts/audio{N}_{duration}/segments.jsonl` — fine-grained segments
  with timestamps (gitignored — large, regenerable)
- `tmp_mp3/` — intermediate re-encoded mp3s (gitignored)

## Why two transcription pipelines

- **Local faster-whisper large-v3 (in progress)** — free, private,
  audio never leaves the VPS, but slow (~5h wall-clock for 3h 19m
  on CPU int8 with 4-way contention)
- **Turboscribe cloud (paid)** — fast, GPU-backed, but audio leaves
  the VPS

Wes's brainstorm material can include sensitive/cultural context
(see `sonia-assistant` skill, Wes Rule 5: cultural-routing via
Sonja, not direct research; Wes Rule 6: post-escritura relaxed-state
audio ≠ literal deliverables, F-bucket hyperbole filter applies).

The local pipeline is canonical for any private content. Turboscribe
is the secondary/translation-quality check. Final repo transcript
will be the local one with Turboscribe used as a comparison.

## Status (this commit)

- Audio B (2 min) fully transcribed locally — EN casual conversation
- Other 4 audios: transcribing in background, will land in
  follow-up commits as they finish
- Turboscribe bundle ready for upload (binary excluded from repo
  via .gitignore — regenerable from the local cache)

## Reproducing the Turboscribe bundle

From a shell with the original 5 .m4a files in the Messaging document
cache, run:

```bash
python3 /tmp/concat_wes_audios.py   # conversion + concat
python3 /tmp/concat_with_silence.py # 1s silence gaps between parts
python3 /tmp/write_manifest.py      # manifest.json + .txt
```

The combined mp3 is ~95 MB, ~3h 19m, named
`wes_2026-06-30_full_chronological_for_turboscribe.mp3`.