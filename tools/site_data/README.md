# `tools/site_data/` — auxiliary site-data ingest

Free public APIs that feed the housing-park engineering brief.
Lives **outside** `lqv/` on purpose — the render pipeline is frozen until
escritura. These ingests write to `docs/site_data/<dataset>/`.

| Module | Source | Auth | License | Adds vs. existing |
| --- | --- | --- | --- | --- |
| `soilgrids` | ISRIC SoilGrids 250 m | none | CC-BY 4.0 | clay/sand/bdod/cec at 6 depths — cob siting + foundation |
| `nasa_power` | NASA POWER Daily Point | none | Public domain (NASA) | engineering-deck-friendly CSV at parcel point |
| `chirps` | UCSB CHIRPS v2.0 monthly | none | Public domain (CHC) | 5 km precip vs. ERA5's ~28 km |
| `sentinel1` | ASF DAAC + HyP3 | Earthdata login | CC0 (Sentinel) | InSAR subsidence — required for build-readiness |

ERA5 already covers temp/precip/wind/solar at ~28 km from
`docs/site_data/climate_era5/`. CHIRPS + NASA POWER are kept anyway: CHIRPS
sharpens precip to 5 km (good for sub-parcel runoff modelling) and POWER
emits a CSV that engineering reviewers consume directly.

## Run

From repo root:

```bash
python3 -m tools.site_data.soilgrids        # ~30 s, no auth
python3 -m tools.site_data.nasa_power       # ~30 s, no auth
python3 -m tools.site_data.chirps           # ~5 min, downloads ~50 MB
python3 -m tools.site_data.sentinel1 --search  # ~1 min, needs EARTHDATA_USER/PASS
```

## Auth

Only Sentinel-1 needs auth (NASA Earthdata for ASF DAAC + HyP3):

```bash
export EARTHDATA_USER="<your-earthdata-username>"
export EARTHDATA_PASS="<your-earthdata-password>"
```

Register at <https://urs.earthdata.nasa.gov/> and accept the ASF DAAC EULA.

## License gate

These ingests touch sources that are all bundle-safe (CC0 / CC-BY 4.0 /
US public-domain). Nothing under `tools/site_data/` is added to the
escritura bundle today — they feed the post-escritura engineering deck,
not the legal pack.

## Outputs

Each module writes to its own `docs/site_data/<name>/` subdir:

- `<name>_point.json` or `<name>_<year>.tif` — raw / structured pull
- `<name>_summary.txt` — terse one-liners for the deck
- `<name>_brochure.md` — narrative paragraph + chart placeholders

Do not commit large raw TIFFs without checking `.gitignore` first — CHIRPS
monthly TIFFs (~3 MB each) are fine; full annual stacks are not.
