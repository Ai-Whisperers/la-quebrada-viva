# Audio drafts — raw transcription source data

> **For context.** The 5 directories here contain the raw outputs
> from TurboScribe.ai transcription runs of Wesley's 5 audio recordings
> from 2026-06-30 (post-escritura). The cleaned synthesis lives in
> `../final/` (DREAMLIST_NL, ACTIONLIST_ES_EN, IDEAS_LOG, KEY_POINTS,
> RESEARCH_CATALOGUE, REPO_UPDATES, SYNTHESIS).

## What's in here

Each `audio<N>_<duration>/` directory has 3 files:

| File | What |
|---|---|
| `meta.json` | Turboscribe run metadata (timestamps, model version, confidence stats) |
| `segments.jsonl` | Per-segment transcription with timestamps + confidence per segment |
| `raw.txt` | Plain-text concatenated transcript (no timestamps) |

### Audio inventory (Wes's 5 recordings, 2026-06-30)

| # | Duration | Topic (per SYNTHESIS.md) | Segments | Raw size |
|--:|--:|---|--:|--:|
| 1 | 2 min | Short opener — initial reactions | ~12 | 1.2 KB |
| 2 | 29 min | Dream list — 15 domains D1-D15 | ~150 | 20 KB |
| 3 | 39 min | Corporate structure + 4-BV + machinepark | ~200 | 31 KB |
| 4 | 18 min | Worker roles + 4-BV validation + hovenier AI delegation | ~90 | 15 KB |
| 5 | 1h 50min | The big one — full brainstorm + 2030 milestone correction | ~500 | 79 KB |
| **Total** | **3h 19m** | | **~952 segments** | **147 KB** |

## How to use

- **For re-running the audio synthesis pipeline** — the `raw.txt`
  files are the cleanest starting point. The synthesis docs in
  `../final/` were derived by:
  1. Combining all 5 `raw.txt` files into one corpus
  2. Identifying the 15 DREAMLIST domains (D1-D15)
  3. Extracting the 95+ ideas into `IDEAS_LOG.md`
  4. Mapping each idea to an R-item in `RESEARCH_CATALOGUE.md`
  5. Linking each R-item to the 109-idea catalog (`docs/ideas/`)

- **For verifying a specific quote** — search `segments.jsonl`
  for the segment containing the quote; the timestamp lets you
  re-listen to the original audio (Wes's MP3s are gitignored,
  stored in `/tmp/lqv-keep/audios/` per `.gitignore`).

- **For checking transcription quality** — `meta.json` has the
  confidence stats per segment. Most segments are >0.9 confidence.

## How to re-run TurboScribe

The original MP3s are gitignored (in `docs/audios/**/*.mp3` per
`.gitignore`). To re-transcribe:

```bash
# 1. Get the original MP3s from Wes or /tmp/lqv-keep/audios/
# 2. Upload to turboscribe.ai (paid service, ~$0.10/audio min)
# 3. Choose: speaker detection on, NL+ES mixed-language mode, timestamps on
# 4. Export: meta.json + segments.jsonl + raw.txt into the matching audio<N>_*/ dir
# 5. Re-run synthesis pipeline (see `../final/SYNTHESIS.md` for what to extract)
```

## Provenance

- **Source:** Wesley van de Camp, 5 audio recordings, 2026-06-30
- **Transcription:** TurboScribe.ai (NL+ES auto-detect, speaker-aware)
- **Synthesis:** Erebus (AI Whisperers), 2026-06-30
- **Files committed:** 2026-06-30, all 5 audio drafts in this dir

---

*Maintained alongside `../README.md` + `../turboscribe_manifest.json`.*
*The 5 cleaned synthesis docs are in `../final/` and are the canonical references.*