# Render runs — `RENDER_RUN_ID` policy

## TL;DR

```bash
RENDER_RUN_ID=20260613_review RENDER_VARIANT=A blender -b -P lqv/subscene/hobbit_house.py
RENDER_RUN_ID=20260613_review RENDER_VARIANT=B blender -b -P lqv/subscene/hobbit_house.py
RENDER_RUN_ID=20260613_review RENDER_VARIANT=C blender -b -P lqv/subscene/hobbit_house.py
```

All three variants land in `renders/sub/runs/20260613_review_hobbit_house/{A,B,C}.png`
so the review/composite scripts can grab the triple as one batch.

## Why this exists

Every sub-render driver imports `lqv.subscene.base`. `base` historically
picked the run id like this:

```python
_RUN_ID = os.environ.get('RENDER_RUN_ID') or datetime.now().strftime('%Y%m%d_%H%M%S')
```

In practice the user starts one Blender process per variant (each variant
needs its own headless `blender --background` invocation because Cycles
holds GPU memory and the seed must reset). When `RENDER_RUN_ID` is unset
each process generates its own timestamp. A typical A/B/C batch ended up
in three different folders:

```
renders/sub/runs/20260613_143512_hobbit_house/A.png
renders/sub/runs/20260613_143619_hobbit_house/B.png
renders/sub/runs/20260613_143727_hobbit_house/C.png
```

The composite pipeline expects a single folder per asset and silently
skipped the orphan variants — we were losing ~30% of every batch and
discovering it in the review meeting.

## The rule

`lqv.subscene.base` now refuses to import unless one of these holds:

1. `RENDER_RUN_ID` is set in the environment (recommended)
2. `LQV_ALLOW_TIMESTAMP_RUN_ID=1` is set (one-off exploratory shots — emits a warning)

Anything else raises `RuntimeError` immediately, before any render starts,
so the failure shows up at submit time instead of 40 minutes later when
the composite script can't find variant C.

## Naming conventions

- Batches: `YYYYMMDD_<purpose>` — `20260613_review`, `20260620_escritura_pdf`
- Hot-fixes: `YYYYMMDD_<purpose>_v2` if you re-run with edits
- Smoke tests: the `smoke_test.sh` script picks `smoke_<timestamp>` automatically
- Build-only flows (e.g. `scripts/build_terrain_62ha_blend.py`): `build_<asset>_<date>`

## Escape hatch

For ad-hoc one-off lighting experiments where the timestamp folder is
fine, set `LQV_ALLOW_TIMESTAMP_RUN_ID=1`. Don't put this in a script the
review pipeline calls — it defeats the point of the policy.

```bash
LQV_ALLOW_TIMESTAMP_RUN_ID=1 blender -b -P lqv/subscene/hobbit_house.py
# WARN RENDER_RUN_ID unset, LQV_ALLOW_TIMESTAMP_RUN_ID=1 set — using timestamp 20260613_143512.
```

## Folder layout reminder

```
renders/sub/
├── runs/
│   └── <RENDER_RUN_ID>_<asset>[_<RENDER_RUN_TAG>]/
│       ├── A.png
│       ├── B.png
│       └── C.png
├── latest/
│   └── <asset>_<variant>.png   # always points at the most recent render
└── <asset>_<variant>.png       # legacy flat path, back-compat
```

`RENDER_RUN_TAG` is the optional sub-tag appended to the folder name
(e.g. `RENDER_RUN_TAG=v2` produces `runs/20260613_review_hobbit_house_v2/`).
